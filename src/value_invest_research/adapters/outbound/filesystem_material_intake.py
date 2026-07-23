from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FileSystemMaterialIntakeRepository:
    """Persist one parent intake ledger and BOM-specific parsing inboxes."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    @property
    def project_dir_label(self) -> str:
        return str(self.project_dir)

    def load_seen_external_ids(self, provider: str, feed_id: str) -> set[str]:
        state = _read_json(self.project_dir / "material_intake" / "feed_state.json")
        feed_key = _feed_key(provider, feed_id)
        return set(
            str(item)
            for item in ((state.get("feeds") or {}).get(feed_key) or {}).get(
                "seen_external_ids",
                [],
            )
            if str(item).strip()
        )

    def persist_material_batch(
        self,
        *,
        documents: list[dict[str, Any]],
        parse_tasks: list[dict[str, Any]],
        scan_event: dict[str, Any],
    ) -> dict[str, int]:
        intake_dir = self.project_dir / "material_intake"
        intake_dir.mkdir(parents=True, exist_ok=True)
        document_path = intake_dir / "documents.jsonl"
        scan_path = intake_dir / "scan_events.jsonl"
        existing_documents = _read_jsonl(document_path)
        merged_documents = _merge_material_documents(
            existing_documents,
            documents,
        )
        _write_jsonl(document_path, merged_documents)
        scan_rows = _merge_rows(
            _read_jsonl(scan_path),
            [scan_event],
            key_fields=("scan_id",),
        )
        _write_jsonl(scan_path, scan_rows)

        routed_documents = 0
        routed_tasks = 0
        for node_id in sorted(
            {
                str(node_id)
                for document in documents
                for node_id in document.get("matched_bom_node_ids") or []
                if str(node_id).strip()
            }
        ):
            node_documents = [
                document
                for document in documents
                if node_id in (document.get("matched_bom_node_ids") or [])
            ]
            node_tasks = [
                task
                for task in parse_tasks
                if str(task.get("bom_node_id") or "") == node_id
            ]
            inbox_dir = self.project_dir / "boms" / node_id / "inbox"
            inbox_dir.mkdir(parents=True, exist_ok=True)
            _write_jsonl(
                inbox_dir / "materials.jsonl",
                _merge_material_documents(
                    _read_jsonl(inbox_dir / "materials.jsonl"),
                    node_documents,
                ),
            )
            _write_jsonl(
                inbox_dir / "parse_tasks.jsonl",
                _merge_rows(
                    _read_jsonl(inbox_dir / "parse_tasks.jsonl"),
                    node_tasks,
                    key_fields=("task_id",),
                ),
            )
            routed_documents += len(node_documents)
            routed_tasks += len(node_tasks)

        self._update_feed_state(scan_event, documents)
        return {
            "project_documents": len(merged_documents),
            "new_documents": len(documents),
            "routed_documents": routed_documents,
            "parse_tasks": routed_tasks,
        }

    def _update_feed_state(
        self,
        scan_event: dict[str, Any],
        documents: list[dict[str, Any]],
    ) -> None:
        state_path = self.project_dir / "material_intake" / "feed_state.json"
        state = _read_json(state_path)
        state.setdefault("schema_version", "1.0")
        feeds = state.setdefault("feeds", {})
        provider = str(scan_event.get("provider") or "")
        feed_id = str(scan_event.get("feed_id") or "")
        feed_key = _feed_key(provider, feed_id)
        previous = feeds.get(feed_key) or {}
        seen = list(
            dict.fromkeys(
                [
                    *previous.get("seen_external_ids", []),
                    *[
                        str(document.get("external_id") or "")
                        for document in documents
                        if str(document.get("external_id") or "").strip()
                    ],
                ]
            )
        )
        feeds[feed_key] = {
            "provider": provider,
            "feed_id": feed_id,
            "last_scan_at": scan_event.get("scanned_at"),
            "last_scan_id": scan_event.get("scan_id"),
            "seen_external_ids": seen,
        }
        _write_json(state_path, state)


class FileSystemMaterialIntakeValidationRepository:
    """Load intake artifacts for a pure domain validation pass."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    @property
    def project_dir_label(self) -> str:
        return str(self.project_dir)

    def load_material_intake_bundle(self) -> dict[str, Any]:
        load_issues: list[dict[str, str]] = []
        project = _load_required_json(
            self.project_dir / "project.json",
            load_issues,
        )
        manifest = _load_required_json(
            self.project_dir / "boms" / "manifest.json",
            load_issues,
        )
        known_nodes = [
            str(row.get("node_id") or "")
            for row in manifest.get("nodes") or []
            if isinstance(row, dict) and str(row.get("node_id") or "").strip()
        ]
        documents = _read_jsonl_for_validation(
            self.project_dir / "material_intake" / "documents.jsonl",
            load_issues,
            required=False,
        )
        node_inboxes: dict[str, dict[str, list[dict[str, Any]]]] = {}
        for node_id in known_nodes:
            inbox_dir = self.project_dir / "boms" / node_id / "inbox"
            materials_path = inbox_dir / "materials.jsonl"
            tasks_path = inbox_dir / "parse_tasks.jsonl"
            if not materials_path.exists() and not tasks_path.exists():
                continue
            node_inboxes[node_id] = {
                "materials": _read_jsonl_for_validation(
                    materials_path,
                    load_issues,
                    required=tasks_path.exists(),
                ),
                "parse_tasks": _read_jsonl_for_validation(
                    tasks_path,
                    load_issues,
                    required=False,
                ),
            }
        return {
            "project": project,
            "known_bom_node_ids": known_nodes,
            "documents": documents,
            "node_inboxes": node_inboxes,
            "load_issues": load_issues,
        }


def _feed_key(provider: str, feed_id: str) -> str:
    return f"{provider}:{feed_id}"


def _merge_rows(
    existing: list[dict[str, Any]],
    incoming: list[dict[str, Any]],
    *,
    key_fields: tuple[str, ...],
) -> list[dict[str, Any]]:
    merged: dict[tuple[str, ...], dict[str, Any]] = {}
    for row in [*existing, *incoming]:
        key = tuple(str(row.get(field) or "") for field in key_fields)
        if not all(key):
            continue
        merged[key] = row
    return [merged[key] for key in sorted(merged)]


def _merge_material_documents(
    existing: list[dict[str, Any]],
    incoming: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for row in [*existing, *incoming]:
        source_id = str(row.get("source_id") or "")
        if not source_id:
            continue
        previous = merged.get(source_id) or {}
        combined = {**previous, **row}
        combined["matched_bom_node_ids"] = list(
            dict.fromkeys(
                [
                    *(previous.get("matched_bom_node_ids") or []),
                    *(row.get("matched_bom_node_ids") or []),
                ]
            )
        )
        combined["matched_question_numbers"] = list(
            dict.fromkeys(
                [
                    *(previous.get("matched_question_numbers") or []),
                    *(row.get("matched_question_numbers") or []),
                ]
            )
        )
        merged[source_id] = combined
    return [merged[key] for key in sorted(merged)]


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            rows.append(payload)
    return rows


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def _load_required_json(
    path: Path,
    issues: list[dict[str, str]],
) -> dict[str, Any]:
    if not path.is_file():
        issues.append(
            {
                "severity": "error",
                "code": "missing_material_intake_context",
                "message": f"{path} does not exist",
            }
        )
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(
            {
                "severity": "error",
                "code": "invalid_material_intake_context",
                "message": f"{path}: {exc}",
            }
        )
        return {}
    return payload if isinstance(payload, dict) else {}


def _read_jsonl_for_validation(
    path: Path,
    issues: list[dict[str, str]],
    *,
    required: bool,
) -> list[dict[str, Any]]:
    if not path.is_file():
        if required:
            issues.append(
                {
                    "severity": "error",
                    "code": "missing_material_intake_file",
                    "message": f"{path} does not exist",
                }
            )
        return []
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            issues.append(
                {
                    "severity": "error",
                    "code": "invalid_material_intake_jsonl",
                    "message": f"{path}:{line_number}: {exc}",
                }
            )
            continue
        if not isinstance(payload, dict):
            issues.append(
                {
                    "severity": "error",
                    "code": "invalid_material_intake_row",
                    "message": f"{path}:{line_number} must be a JSON object",
                }
            )
            continue
        rows.append(payload)
    return rows
