from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any


class FileSystemImaArchiveRepository:
    """Persist a provider-level IMA PDF mirror outside research projects."""

    def __init__(self, *, workspace_root: Path, archive_root: Path):
        self.workspace_root = workspace_root.resolve()
        self.archive_root = archive_root.resolve()
        if not self.archive_root.is_relative_to(self.workspace_root):
            raise ValueError("IMA archive_root must stay inside the workspace")
        self.archive_root.mkdir(parents=True, exist_ok=True)

    def find_available(
        self,
        *,
        provider: str,
        external_id: str,
        directory_date: str,
    ) -> dict[str, Any]:
        for row in self._load_manifest():
            if (
                str(row.get("provider") or "") == provider
                and str(row.get("external_id") or "") == external_id
                and str(row.get("directory_date") or "") == directory_date
                and str(row.get("status") or "") == "available"
            ):
                local_path = self.workspace_root / str(
                    row.get("local_path") or ""
                )
                if local_path.is_file():
                    return row
        return {}

    def find_by_title(
        self,
        *,
        provider: str,
        title: str,
        directory_date: str,
    ) -> dict[str, Any]:
        matches = [
            row
            for row in self._load_manifest()
            if (
                str(row.get("provider") or "") == provider
                and str(row.get("title") or "") == title
                and str(row.get("directory_date") or "") == directory_date
            )
        ]
        if not matches:
            return {}
        return next(
            (
                row
                for row in matches
                if str(row.get("status") or "") == "available"
                and (
                    self.workspace_root / str(row.get("local_path") or "")
                ).is_file()
            ),
            matches[-1],
        )

    def persist_pdf(
        self,
        *,
        provider: str,
        external_id: str,
        directory_date: str,
        title: str,
        filename: str,
        content: bytes,
        content_type: str,
    ) -> dict[str, Any]:
        if not content:
            raise ValueError("IMA original material is empty")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", directory_date):
            raise ValueError("directory_date must use YYYY-MM-DD")
        year, month, day = directory_date.split("-")
        day_dir = self.archive_root / year / month / day
        day_dir.mkdir(parents=True, exist_ok=True)
        preferred = _safe_pdf_filename(filename or title)
        content_hash = hashlib.sha256(content).hexdigest()
        target = day_dir / preferred
        if target.exists():
            if hashlib.sha256(target.read_bytes()).hexdigest() != content_hash:
                stem = target.stem
                suffix = target.suffix or ".pdf"
                identity = hashlib.sha256(
                    f"{provider}|{external_id}".encode("utf-8")
                ).hexdigest()[:10]
                target = day_dir / f"{stem}--{identity}{suffix}"
        if not target.exists():
            temporary = target.with_suffix(f"{target.suffix}.part")
            temporary.write_bytes(content)
            temporary.replace(target)
        local_path = target.relative_to(self.workspace_root).as_posix()
        return {
            "local_path": local_path,
            "content_type": content_type,
            "content_sha256": content_hash,
            "size_bytes": len(content),
        }

    def persist_archive_record(self, record: dict[str, Any]) -> None:
        path = self.archive_root / "archive_manifest.jsonl"
        rows = self._load_manifest()
        key = str(record.get("record_id") or "")
        merged = [
            row for row in rows if str(row.get("record_id") or "") != key
        ]
        merged.append(record)
        _write_jsonl(
            path,
            sorted(
                merged,
                key=lambda row: (
                    str(row.get("directory_date") or ""),
                    str(row.get("title") or ""),
                    str(row.get("external_id") or ""),
                ),
            ),
        )

    def persist_scan_event(self, event: dict[str, Any]) -> None:
        path = self.archive_root / "archive_events.jsonl"
        rows = _read_jsonl(path)
        key = str(event.get("scan_id") or "")
        merged = [
            row for row in rows if str(row.get("scan_id") or "") != key
        ]
        merged.append(event)
        _write_jsonl(
            path,
            sorted(
                merged,
                key=lambda row: (
                    str(row.get("archive_date") or ""),
                    str(row.get("scanned_at") or ""),
                ),
            ),
        )

    def _load_manifest(self) -> list[dict[str, Any]]:
        return _read_jsonl(self.archive_root / "archive_manifest.jsonl")

    def load_archive_bundle(self) -> dict[str, Any]:
        return {
            "workspace_root": str(self.workspace_root),
            "archive_root": str(self.archive_root),
            "records": self._load_manifest(),
            "events": _read_jsonl(self.archive_root / "archive_events.jsonl"),
        }


def _safe_pdf_filename(value: str) -> str:
    name = Path(str(value or "").replace("\\", "/")).name.strip()
    name = re.sub(r"[\x00-\x1f\x7f]+", " ", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    if not name:
        name = "material.pdf"
    if not name.casefold().endswith(".pdf"):
        name = f"{name}.pdf"
    if len(name) > 220:
        suffix = ".pdf"
        name = f"{name[: 220 - len(suffix)].rstrip()}{suffix}"
    return name


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if isinstance(row, dict):
            rows.append(row)
    return rows


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
        for row in rows
    )
    temporary = path.with_suffix(f"{path.suffix}.tmp")
    temporary.write_text(body, encoding="utf-8")
    temporary.replace(path)
