from __future__ import annotations

from datetime import date
import hashlib
from typing import Any


def archive_ima_day(
    *,
    feed: Any,
    repository: Any,
    knowledge_base_id: str,
    archive_date: str,
    scanned_at: str | None = None,
    root_folder_pattern: str = r"^\d{4}年国际顶级投行研报$",
) -> dict[str, Any]:
    """Mirror every PDF from one IMA day folder into the workspace archive."""

    day = date.fromisoformat(archive_date).isoformat()
    scanned_at = scanned_at or date.today().isoformat()
    knowledge_base_ref = _opaque_reference(knowledge_base_id)
    scan_id = _scan_id(
        provider=feed.provider_name,
        knowledge_base_ref=knowledge_base_ref,
        archive_date=day,
        scanned_at=scanned_at,
    )
    base_event = {
        "scan_id": scan_id,
        "provider": feed.provider_name,
        "knowledge_base_ref": knowledge_base_ref,
        "archive_date": day,
        "scanned_at": scanned_at,
        "root_folder_pattern": root_folder_pattern,
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

    try:
        candidates = feed.list_dated_materials(
            knowledge_base_id=knowledge_base_id,
            start_date=day,
            end_date=day,
            root_folder_pattern=root_folder_pattern,
        )
    except (OSError, ValueError) as exc:
        repository.persist_scan_event(
            {
                **base_event,
                "status": "failed",
                "candidate_count": 0,
                "available_count": 0,
                "downloaded_count": 0,
                "reused_count": 0,
                "unavailable_count": 0,
                "error": str(exc),
            }
        )
        raise

    results: list[dict[str, Any]] = []
    for candidate in candidates:
        external_id = str(
            candidate.get("external_id")
            or candidate.get("media_id")
            or candidate.get("id")
            or ""
        ).strip()
        title = str(candidate.get("title") or external_id or "material.pdf").strip()
        directory_date = str(candidate.get("directory_date") or "").strip()
        record_id = _record_id(
            provider=feed.provider_name,
            external_id=external_id,
            directory_date=directory_date or day,
        )
        common = {
            "record_id": record_id,
            "provider": feed.provider_name,
            "knowledge_base_ref": knowledge_base_ref,
            "external_id": external_id,
            "title": title,
            "directory_date": directory_date,
            "directory_path": str(candidate.get("directory_path") or "").strip(),
            "directory_mapping_status": str(
                candidate.get("directory_mapping_status") or ""
            ).strip(),
            "provider_created_at": str(
                candidate.get("provider_created_at") or ""
            ).strip(),
            "provider_updated_at": str(
                candidate.get("provider_updated_at") or ""
            ).strip(),
            "archived_at": scanned_at,
        }
        if not external_id or directory_date != day:
            result = {
                **common,
                "status": "unavailable",
                "error": (
                    "IMA candidate is missing external_id"
                    if not external_id
                    else (
                        "IMA candidate directory_date does not match requested "
                        f"archive date {day}"
                    )
                ),
            }
            repository.persist_archive_record(result)
            results.append(result)
            continue

        existing = repository.find_available(
            provider=feed.provider_name,
            external_id=external_id,
            directory_date=day,
        )
        if existing:
            result = {
                **existing,
                **common,
                "status": "available",
                "reused_existing": True,
            }
            repository.persist_archive_record(result)
            results.append(result)
            continue

        try:
            payload = feed.fetch_media_content(
                media_id=external_id,
                title=title,
            )
            stored = repository.persist_pdf(
                provider=feed.provider_name,
                external_id=external_id,
                directory_date=day,
                title=title,
                filename=str(payload.get("filename") or title),
                content=payload["content"],
                content_type=str(
                    payload.get("content_type") or "application/pdf"
                ),
            )
            result = {
                **common,
                **stored,
                "status": "available",
                "reused_existing": False,
            }
        except (OSError, ValueError) as exc:
            result = {
                **common,
                "status": "unavailable",
                "error": str(exc),
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
        "candidate_count": len(candidates),
        "available_count": available_count,
        "downloaded_count": available_count - reused_count,
        "reused_count": reused_count,
        "unavailable_count": unavailable_count,
    }
    repository.persist_scan_event(event)
    return {
        "scan_event": event,
        "records": results,
    }


def _opaque_reference(value: str) -> str:
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()[:20]


def _scan_id(
    *,
    provider: str,
    knowledge_base_ref: str,
    archive_date: str,
    scanned_at: str,
) -> str:
    raw = f"{provider}|{knowledge_base_ref}|{archive_date}|{scanned_at}"
    return f"IMA-ARCHIVE-{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:20]}"


def _record_id(
    *,
    provider: str,
    external_id: str,
    directory_date: str,
) -> str:
    raw = f"{provider}|{external_id}|{directory_date}"
    return f"IMA-PDF-{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:20]}"
