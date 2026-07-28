from __future__ import annotations

from datetime import date
import hashlib
import json
from pathlib import Path
import re
import unicodedata
from typing import Any


def archive_ima_ui_downloads(
    *,
    repository: Any,
    archive_date: str,
    candidates: list[dict[str, Any]],
    download_dir: Path,
    scanned_at: str | None = None,
    download_marker: Path | None = None,
    directory_path: str = "",
) -> dict[str, Any]:
    """Import PDFs downloaded through the visible IMA UI into the central mirror."""

    day = date.fromisoformat(archive_date).isoformat()
    scanned_at = scanned_at or date.today().isoformat()
    download_dir = download_dir.expanduser().resolve()
    if not download_dir.is_dir():
        raise ValueError(f"IMA UI download directory does not exist: {download_dir}")
    marker_mtime = None
    if download_marker is not None:
        marker = download_marker.expanduser().resolve()
        if not marker.is_file():
            raise ValueError(f"IMA UI download marker does not exist: {marker}")
        marker_mtime = marker.stat().st_mtime

    normalized = _normalize_candidates(candidates)
    scan_id = _scan_id(archive_date=day, scanned_at=scanned_at)
    base_event = {
        "scan_id": scan_id,
        "provider": "ima",
        "archive_method": "ui_click",
        "archive_date": day,
        "scanned_at": scanned_at,
        "directory_path": directory_path,
    }
    repository.persist_scan_event(
        {
            **base_event,
            "status": "running",
            "candidate_count": 0,
            "available_count": 0,
            "downloaded_count": 0,
            "reused_count": 0,
            "unavailable_count": 0,
        }
    )

    results: list[dict[str, Any]] = []
    claimed_files: set[Path] = set()
    for candidate in normalized:
        title = candidate["title"]
        existing = repository.find_by_title(
            provider="ima",
            title=title,
            directory_date=day,
        )
        external_id = str(existing.get("external_id") or "").strip()
        if not external_id:
            external_id = _ui_external_id(
                directory_date=day,
                title=title,
                ui_key=str(candidate.get("ui_key") or ""),
            )
        record_id = str(existing.get("record_id") or "").strip() or _record_id(
            external_id=external_id,
            directory_date=day,
        )
        common = {
            **existing,
            "record_id": record_id,
            "provider": "ima",
            "archive_method": "ui_click",
            "external_id": external_id,
            "title": title,
            "directory_date": day,
            "directory_path": str(
                candidate.get("directory_path") or directory_path
            ).strip(),
            "directory_mapping_status": "verified",
            "archived_at": scanned_at,
        }
        common.pop("error", None)

        if str(existing.get("status") or "") == "available":
            result = {
                **common,
                "status": "available",
                "reused_existing": True,
            }
            repository.persist_archive_record(result)
            results.append(result)
            continue

        source = _find_download(
            download_dir=download_dir,
            title=str(candidate.get("downloaded_filename") or title),
            marker_mtime=marker_mtime,
            claimed_files=claimed_files,
        )
        if source is None:
            result = {
                **common,
                "status": "unavailable",
                "error": "IMA UI download was not found after the download marker",
                "reused_existing": False,
            }
        else:
            content = source.read_bytes()
            if not content.lstrip().startswith(b"%PDF-"):
                result = {
                    **common,
                    "status": "unavailable",
                    "error": f"IMA UI download is not a PDF: {source.name}",
                    "reused_existing": False,
                }
            else:
                stored = repository.persist_pdf(
                    provider="ima",
                    external_id=external_id,
                    directory_date=day,
                    title=title,
                    filename=title,
                    content=content,
                    content_type="application/pdf",
                )
                claimed_files.add(source)
                result = {
                    **common,
                    **stored,
                    "status": "available",
                    "reused_existing": False,
                }
        repository.persist_archive_record(result)
        results.append(result)

    available_count = sum(row.get("status") == "available" for row in results)
    reused_count = sum(
        row.get("status") == "available" and row.get("reused_existing")
        for row in results
    )
    unavailable_count = len(results) - available_count
    event = {
        **base_event,
        "status": "complete" if unavailable_count == 0 else "partial",
        "candidate_count": len(results),
        "available_count": available_count,
        "downloaded_count": available_count - reused_count,
        "reused_count": reused_count,
        "unavailable_count": unavailable_count,
    }
    repository.persist_scan_event(event)
    return {"scan_event": event, "records": results}


def load_ui_candidate_inventory(
    path: Path,
    *,
    archive_date: str,
) -> tuple[list[dict[str, Any]], str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        candidates = payload
        directory_path = ""
    elif isinstance(payload, dict):
        inventory_date = str(payload.get("directory_date") or "").strip()
        if inventory_date and inventory_date != archive_date:
            raise ValueError(
                "IMA UI inventory directory_date does not match requested date"
            )
        candidates = payload.get("candidates")
        directory_path = str(payload.get("directory_path") or "").strip()
    else:
        raise ValueError("IMA UI candidate inventory must be a JSON object or list")
    if not isinstance(candidates, list):
        raise ValueError("IMA UI candidate inventory requires a candidates list")
    normalized: list[dict[str, Any]] = []
    for item in candidates:
        if isinstance(item, str):
            normalized.append({"title": item})
        elif isinstance(item, dict):
            normalized.append(item)
        else:
            raise ValueError("IMA UI candidates must be strings or objects")
    return normalized, directory_path


def _normalize_candidates(
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    identities: set[str] = set()
    for candidate in candidates:
        title = Path(
            str(candidate.get("title") or "").replace("\\", "/")
        ).name.strip()
        if not title:
            raise ValueError("IMA UI candidate is missing title")
        if not title.casefold().endswith(".pdf"):
            title = f"{title}.pdf"
        ui_key = str(candidate.get("ui_key") or "").strip()
        identity = f"{_canonical_filename(title)}|{ui_key}"
        if identity in identities:
            raise ValueError(f"Duplicate IMA UI candidate: {title}")
        identities.add(identity)
        normalized.append({**candidate, "title": title})
    return normalized


def _find_download(
    *,
    download_dir: Path,
    title: str,
    marker_mtime: float | None,
    claimed_files: set[Path],
) -> Path | None:
    canonical = _canonical_filename(title)
    matches = []
    for path in download_dir.glob("*.pdf"):
        if path in claimed_files:
            continue
        if marker_mtime is not None and path.stat().st_mtime < marker_mtime:
            continue
        if _canonical_filename(path.name) == canonical:
            matches.append(path)
    return max(matches, key=lambda item: item.stat().st_mtime) if matches else None


def _canonical_filename(value: str) -> str:
    name = unicodedata.normalize("NFC", Path(value).name.strip())
    stem = re.sub(r"\s+\(\d+\)$", "", Path(name).stem)
    return f"{stem}{Path(name).suffix}".casefold()


def _ui_external_id(*, directory_date: str, title: str, ui_key: str) -> str:
    raw = f"{directory_date}|{title}|{ui_key}"
    return f"ui:{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:40]}"


def _record_id(*, external_id: str, directory_date: str) -> str:
    raw = f"ima|{external_id}|{directory_date}"
    return f"IMA-PDF-{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:20]}"


def _scan_id(*, archive_date: str, scanned_at: str) -> str:
    raw = f"ima|ui_click|{archive_date}|{scanned_at}"
    return f"IMA-UI-ARCHIVE-{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:20]}"
