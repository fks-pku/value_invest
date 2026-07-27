from __future__ import annotations

import hashlib
from pathlib import Path
import re
from typing import Any


def validate_ima_archive(*, repository: Any) -> dict[str, Any]:
    """Validate manifest-to-file integrity for the central IMA PDF archive."""

    bundle = repository.load_archive_bundle()
    archive_root = Path(bundle["archive_root"]).resolve()
    workspace_root = Path(bundle["workspace_root"]).resolve()
    issues: list[str] = []
    records = bundle["records"]
    events = bundle["events"]

    record_ids: set[str] = set()
    for record in records:
        record_id = str(record.get("record_id") or "").strip()
        if not record_id:
            issues.append("archive record is missing record_id")
        elif record_id in record_ids:
            issues.append(f"duplicate archive record_id: {record_id}")
        record_ids.add(record_id)
        if any(
            forbidden in record
            for forbidden in ("knowledge_base_id", "signed_url", "download_url")
        ):
            issues.append(f"{record_id or '<unknown>'}: persisted private provider field")
        status = str(record.get("status") or "")
        if status not in {"available", "unavailable"}:
            issues.append(f"{record_id or '<unknown>'}: unsupported status={status!r}")
        if status != "available":
            continue
        directory_date = str(record.get("directory_date") or "")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", directory_date):
            issues.append(f"{record_id}: invalid directory_date")
            continue
        local_path = str(record.get("local_path") or "")
        path = (workspace_root / local_path).resolve()
        if not path.is_relative_to(archive_root):
            issues.append(f"{record_id}: local_path escapes archive_root")
            continue
        year, month, day = directory_date.split("-")
        expected_parent = archive_root / year / month / day
        if path.parent != expected_parent:
            issues.append(
                f"{record_id}: local_path does not match directory_date"
            )
        if not path.is_file():
            issues.append(f"{record_id}: archived PDF is missing")
            continue
        content = path.read_bytes()
        if int(record.get("size_bytes") or -1) != len(content):
            issues.append(f"{record_id}: size_bytes mismatch")
        expected_hash = str(record.get("content_sha256") or "")
        if expected_hash != hashlib.sha256(content).hexdigest():
            issues.append(f"{record_id}: content_sha256 mismatch")

    for event in events:
        scan_id = str(event.get("scan_id") or "<unknown>")
        if any(
            forbidden in event
            for forbidden in ("knowledge_base_id", "signed_url", "download_url")
        ):
            issues.append(f"{scan_id}: persisted private provider field")
        if str(event.get("status") or "") not in {
            "running",
            "complete",
            "partial",
            "failed",
        }:
            issues.append(f"{scan_id}: unsupported event status")
        if str(event.get("status") or "") in {"complete", "partial"}:
            candidate_count = int(event.get("candidate_count") or 0)
            available_count = int(event.get("available_count") or 0)
            unavailable_count = int(event.get("unavailable_count") or 0)
            if candidate_count != available_count + unavailable_count:
                issues.append(f"{scan_id}: event counts do not reconcile")

    return {
        "archive_root": str(archive_root),
        "record_count": len(records),
        "event_count": len(events),
        "available_count": sum(
            str(row.get("status") or "") == "available" for row in records
        ),
        "unavailable_count": sum(
            str(row.get("status") or "") == "unavailable" for row in records
        ),
        "issues": issues,
        "ok": not issues,
    }
