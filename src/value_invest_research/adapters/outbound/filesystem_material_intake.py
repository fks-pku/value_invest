from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
from typing import Any


class FileSystemMaterialIntakeRepository:
    """Persist one intake ledger and research-object parsing inboxes."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        project = _read_json(project_dir / "project.json")
        self.standalone_node_id = (
            str(project.get("bom_node_id") or "").strip()
            if project.get("report_scope") == "standalone-bom"
            else ""
        )

    @property
    def project_dir_label(self) -> str:
        return str(self.project_dir)

    @property
    def leaf_search_required(self) -> bool:
        return (self.project_dir / "l3_research_plans" / "index.json").is_file()

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
            inbox_dir = self._inbox_dir(node_id)
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

    def persist_material_content(
        self,
        *,
        document: dict[str, Any],
        content: bytes,
        filename: str,
        content_type: str,
    ) -> str:
        source_id = str(document.get("source_id") or "").strip()
        if not source_id:
            raise ValueError("Material content requires source_id")
        safe_filename = _safe_filename(filename)
        content_dir = self.project_dir / _dated_source_dir(document)
        content_dir.mkdir(parents=True, exist_ok=True)
        content_path = _non_conflicting_path(
            content_dir / safe_filename,
            source_id=source_id,
            content=content,
        )
        content_path.write_bytes(content)
        relative_path = content_path.relative_to(self.project_dir).as_posix()
        patch = {
            "local_content_path": relative_path,
            "content_type": content_type,
            "content_status": "available",
        }
        self._patch_source_records(source_id, patch)
        return relative_path

    def canonicalize_material_content(
        self,
        document: dict[str, Any],
    ) -> str:
        """Move a legacy original into the BOM project's canonical source tree."""

        source_id = str(document.get("source_id") or "").strip()
        if not source_id:
            return ""
        stored = next(
            (
                row
                for row in _read_jsonl(
                    self.project_dir / "material_intake" / "documents.jsonl"
                )
                if str(row.get("source_id") or "") == source_id
            ),
            {},
        )
        current_relative = str(stored.get("local_content_path") or "").strip()
        if not current_relative:
            return ""
        current_path = self.project_dir / current_relative
        if not current_path.is_file():
            return ""
        target_dir = self.project_dir / _dated_source_dir(
            {**stored, **document}
        )
        target_dir.mkdir(parents=True, exist_ok=True)
        preferred_name = _preferred_material_filename(
            document={**stored, **document},
            fallback=current_path.name,
        )
        target_path = _non_conflicting_path(
            target_dir / preferred_name,
            source_id=source_id,
            content=current_path.read_bytes(),
        )
        if current_path == target_path:
            relative_path = current_relative
        elif current_relative.startswith("source/ima/"):
            current_path.replace(target_path)
            _prune_empty_directories(
                current_path.parent,
                stop=self.project_dir / "source" / "ima",
            )
            relative_path = target_path.relative_to(self.project_dir).as_posix()
        else:
            if target_path.exists():
                current_path.unlink()
            else:
                current_path.replace(target_path)
            _prune_empty_directories(
                current_path.parent,
                stop=self.project_dir / "material_intake" / "raw",
            )
            relative_path = target_path.relative_to(self.project_dir).as_posix()
        self._patch_source_records(
            source_id,
            {
                "local_content_path": relative_path,
                "content_type": str(
                    stored.get("content_type") or "application/pdf"
                ),
                "content_status": "available",
            },
        )
        return relative_path

    def read_material_content(self, relative_path: str) -> bytes:
        path = self.project_dir / str(relative_path)
        if not path.is_file():
            raise ValueError(f"Material original does not exist: {relative_path}")
        return path.read_bytes()

    def load_material_documents(
        self,
        *,
        provider: str,
        external_ids: list[str],
    ) -> list[dict[str, Any]]:
        wanted = {str(item).strip() for item in external_ids if str(item).strip()}
        return [
            row
            for row in _read_jsonl(
                self.project_dir / "material_intake" / "documents.jsonl"
            )
            if str(row.get("provider") or "") == provider
            and str(row.get("external_id") or "") in wanted
        ]

    def update_publication_date(
        self,
        *,
        source_id: str,
        published_at: str,
        publication_date_status: str,
        publication_date_source: str,
        publication_date_locator: str = "",
    ) -> str:
        """Propagate one publication date and canonicalize its local original."""

        if publication_date_status == "needs_pdf_verification":
            patch = {
                "published_at": "",
                "publication_date_status": publication_date_status,
                "publication_date_source": publication_date_source,
                "publication_date_locator": publication_date_locator,
                "mapping_status": "pending_publication_date",
                "allowed_usage": "date_verification_only",
            }
        else:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", published_at):
                raise ValueError("published_at must use YYYY-MM-DD")
            patch = {
                "published_at": published_at,
                "publication_date_status": publication_date_status,
                "publication_date_source": publication_date_source,
                "publication_date_locator": publication_date_locator,
                "mapping_status": "pending_question_parse",
                "allowed_usage": "research",
            }
        self._patch_source_records(source_id, patch)
        return self.canonicalize_material_content(
            {"source_id": source_id, **patch}
        )

    def update_directory_location(
        self,
        *,
        source_id: str,
        directory_date: str,
        directory_path: str,
        directory_mapping_status: str,
    ) -> str:
        """Review one IMA archive location and move its original if present."""

        if directory_mapping_status == "verified":
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", directory_date):
                raise ValueError("directory_date must use YYYY-MM-DD")
            if not directory_path.strip():
                raise ValueError("verified IMA directory requires directory_path")
            patch = {
                "directory_date": directory_date,
                "directory_path": directory_path.strip(),
                "directory_mapping_status": "verified",
            }
        elif directory_mapping_status == "pending_directory_reconciliation":
            patch = {
                "directory_date": "",
                "directory_path": "",
                "directory_mapping_status": directory_mapping_status,
            }
        else:
            raise ValueError(
                "IMA directory status must be verified or "
                "pending_directory_reconciliation"
            )
        self._patch_source_records(source_id, patch)
        return self.canonicalize_material_content(
            {"source_id": source_id, **patch}
        )

    def persist_directory_scan(
        self,
        *,
        candidates: list[dict[str, Any]],
        scan_event: dict[str, Any],
    ) -> dict[str, int]:
        intake_dir = self.project_dir / "material_intake"
        intake_dir.mkdir(parents=True, exist_ok=True)
        candidate_path = intake_dir / "directory_candidates.jsonl"
        event_path = intake_dir / "directory_scan_events.jsonl"
        merged_candidates = _merge_directory_candidates(
            _read_jsonl(candidate_path),
            candidates,
        )
        merged_events = _merge_rows(
            _read_jsonl(event_path),
            [scan_event],
            key_fields=("scan_id",),
        )
        _write_jsonl(candidate_path, merged_candidates)
        _write_jsonl(event_path, merged_events)
        return {
            "candidates": len(merged_candidates),
            "scan_events": len(merged_events),
        }

    def load_directory_relevance_reviews(self) -> list[dict[str, Any]]:
        return _read_jsonl(
            self.project_dir
            / "material_intake"
            / "relevance_reviews.jsonl"
        )

    def reset_research_state(self) -> dict[str, int]:
        """Remove derived research state while preserving the project contract."""

        removed_files = 0
        removed_directories = 0
        for relative in (
            "source/ima",
            "material_intake",
            "inbox",
            "ledger",
        ):
            path = self.project_dir / relative
            if path.is_dir():
                removed_files += sum(item.is_file() for item in path.rglob("*"))
                shutil.rmtree(path)
                removed_directories += 1
            elif path.is_file():
                path.unlink()
                removed_files += 1
        for relative in (
            "sources.jsonl",
            "professional_report.md",
            "professional_report.html",
        ):
            path = self.project_dir / relative
            if path.is_file():
                path.unlink()
                removed_files += 1
        for relative in ("material_intake", "inbox", "ledger"):
            (self.project_dir / relative).mkdir(parents=True, exist_ok=True)

        profile_path = self.project_dir / "timeline_profile.json"
        profile = _read_json(profile_path)
        if profile:
            for lens in profile.get("lenses") or []:
                if isinstance(lens, dict):
                    lens.pop("baseline_conclusion", None)
            _write_json(profile_path, profile)
        return {
            "removed_files": removed_files,
            "removed_directories": removed_directories,
        }

    def _inbox_dir(self, node_id: str) -> Path:
        if self.standalone_node_id:
            if node_id != self.standalone_node_id:
                raise ValueError(
                    f"Standalone BOM project only accepts node={self.standalone_node_id}"
                )
            return self.project_dir / "inbox"
        return self.project_dir / "boms" / node_id / "inbox"

    def _patch_source_records(
        self,
        source_id: str,
        patch: dict[str, Any],
    ) -> None:
        project_documents_path = (
            self.project_dir / "material_intake" / "documents.jsonl"
        )
        _write_jsonl(
            project_documents_path,
            [
                {**row, **patch}
                if str(row.get("source_id") or "") == source_id
                else row
                for row in _read_jsonl(project_documents_path)
            ],
        )
        candidate_path = (
            self.project_dir
            / "material_intake"
            / "directory_candidates.jsonl"
        )
        if candidate_path.exists():
            _write_jsonl(
                candidate_path,
                [
                    {**row, **_candidate_patch(patch)}
                    if str(row.get("source_id") or "") == source_id
                    else row
                    for row in _read_jsonl(candidate_path)
                ],
            )
        node_ids = {
            str(node_id)
            for row in _read_jsonl(project_documents_path)
            if str(row.get("source_id") or "") == source_id
            for node_id in row.get("matched_bom_node_ids") or []
        }
        for node_id in node_ids:
            inbox_dir = self._inbox_dir(node_id)
            inbox_dir.mkdir(parents=True, exist_ok=True)
            materials_path = inbox_dir / "materials.jsonl"
            _write_jsonl(
                materials_path,
                [
                    {**row, **patch}
                    if str(row.get("source_id") or "") == source_id
                    else row
                    for row in _read_jsonl(materials_path)
                ],
            )
            tasks_path = inbox_dir / "parse_tasks.jsonl"
            _write_jsonl(
                tasks_path,
                [
                    {**row, **_parse_task_patch(patch)}
                    if str(row.get("source_id") or "") == source_id
                    else row
                    for row in _read_jsonl(tasks_path)
                ],
            )
            for reviewed_path in inbox_dir.glob(
                "reviewed_claims*.jsonl"
            ):
                _write_jsonl(
                    reviewed_path,
                    [
                        {**row, **_reviewed_claim_patch(patch)}
                        if (
                            str(row.get("source_id") or "") == source_id
                            and str(row.get("ingestion_channel") or "")
                            == "knowledge_base_scan"
                        )
                        else row
                        for row in _read_jsonl(reviewed_path)
                    ],
                )
        claims_path = self.project_dir / "ledger" / "claims.jsonl"
        if claims_path.exists():
            _write_jsonl(
                claims_path,
                [
                    {**row, **_reviewed_claim_patch(patch)}
                    if (
                        str(row.get("source_id") or "") == source_id
                        and str(row.get("ingestion_channel") or "")
                        == "knowledge_base_scan"
                    )
                    else row
                    for row in _read_jsonl(claims_path)
                ],
            )
        sources_path = self.project_dir / "sources.jsonl"
        if sources_path.exists():
            _write_jsonl(
                sources_path,
                [
                    {**row, **_source_index_patch(patch)}
                    if (
                        str(row.get("source_id") or "") == source_id
                        and str(row.get("ingestion_channel") or "")
                        == "knowledge_base_scan"
                    )
                    else row
                    for row in _read_jsonl(sources_path)
                ],
            )

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
        standalone_node_id = (
            str(project.get("bom_node_id") or "").strip()
            if project.get("report_scope") == "standalone-bom"
            else ""
        )
        if standalone_node_id:
            known_nodes = [standalone_node_id]
        else:
            manifest = _load_required_json(
                self.project_dir / "boms" / "manifest.json",
                load_issues,
            )
            known_nodes = [
                str(row.get("node_id") or "")
                for row in manifest.get("nodes") or []
                if isinstance(row, dict) and str(row.get("node_id") or "").strip()
            ]
        question_numbers_by_node = {
            node_id: list(range(1, len(project.get("question_labels") or []) + 1))
            for node_id in known_nodes
            if standalone_node_id and project.get("question_labels")
        }
        documents = _read_jsonl_for_validation(
            self.project_dir / "material_intake" / "documents.jsonl",
            load_issues,
            required=False,
        )
        directory_candidates = _read_jsonl_for_validation(
            self.project_dir
            / "material_intake"
            / "directory_candidates.jsonl",
            load_issues,
            required=False,
        )
        node_inboxes: dict[str, dict[str, list[dict[str, Any]]]] = {}
        for node_id in known_nodes:
            inbox_dir = (
                self.project_dir / "inbox"
                if standalone_node_id
                else self.project_dir / "boms" / node_id / "inbox"
            )
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
        l3_index = _read_json(
            self.project_dir / "l3_research_plans" / "index.json"
        )
        leaf_plan_coordinates: list[dict[str, str]] = []
        for plan_row in l3_index.get("plans") or []:
            if not isinstance(plan_row, dict):
                continue
            plan = _read_json(
                self.project_dir / str(plan_row.get("path") or "")
            )
            for step in plan.get("steps") or []:
                if not isinstance(step, dict):
                    continue
                leaf_plan_coordinates.append(
                    {
                        field_name: str(step.get(field_name) or "")
                        for field_name in (
                            "l3_plan_id",
                            "l3_node_id",
                            "l4_question_id",
                            "leaf_question_id",
                            "leaf_step_id",
                        )
                    }
                )
        return {
            "project": project,
            "known_bom_node_ids": known_nodes,
            "question_numbers_by_node": question_numbers_by_node,
            "documents": documents,
            "directory_candidates": directory_candidates,
            "node_inboxes": node_inboxes,
            "leaf_search_contract_active": bool(l3_index),
            "leaf_plan_coordinates": leaf_plan_coordinates,
            "load_issues": load_issues,
        }


def _feed_key(provider: str, feed_id: str) -> str:
    return f"{provider}:{feed_id}"


def _candidate_patch(patch: dict[str, Any]) -> dict[str, Any]:
    return {
        key: patch[key]
        for key in (
            "published_at",
            "publication_date_status",
            "publication_date_source",
            "publication_date_locator",
            "directory_date",
            "directory_path",
            "directory_mapping_status",
        )
        if key in patch
    }


def _parse_task_patch(patch: dict[str, Any]) -> dict[str, Any]:
    task_patch = _candidate_patch(patch)
    if "local_content_path" in patch:
        task_patch["source_content_path"] = patch["local_content_path"]
    if "content_type" in patch:
        task_patch["source_content_type"] = patch["content_type"]
    if "directory_date" in patch:
        task_patch["source_directory_date"] = patch["directory_date"]
    if "directory_path" in patch:
        task_patch["source_directory_path"] = patch["directory_path"]
    if "directory_mapping_status" in patch:
        task_patch["source_directory_mapping_status"] = patch[
            "directory_mapping_status"
        ]
    if patch.get("publication_date_status") == "needs_pdf_verification":
        task_patch["status"] = "pending_date_verification"
    elif "publication_date_status" in patch:
        task_patch["status"] = "pending"
    return task_patch


def _reviewed_claim_patch(patch: dict[str, Any]) -> dict[str, Any]:
    claim_patch = _candidate_patch(patch)
    if "local_content_path" in patch:
        claim_patch["source_url"] = patch["local_content_path"]
    return claim_patch


def _source_index_patch(patch: dict[str, Any]) -> dict[str, Any]:
    source_patch = _candidate_patch(patch)
    if "local_content_path" in patch:
        source_patch["url"] = patch["local_content_path"]
    return source_patch


def _safe_filename(filename: str) -> str:
    cleaned = re.sub(r"[\x00-\x1f/\\:]+", "_", str(filename or "")).strip(" .")
    return cleaned or "material.bin"


def _dated_source_dir(document: dict[str, Any]) -> Path:
    provider = str(document.get("provider") or "")
    source_id = str(document.get("source_id") or "").strip()
    is_ima = provider == "ima" or (
        not provider and source_id.startswith("SRC-IMA-")
    )
    if not is_ima:
        return Path("source") / "manual"
    raw_date = str(document.get("published_at") or "")
    if not raw_date:
        if not source_id:
            raise ValueError("Unmapped IMA originals require source_id")
        return Path("source") / "ima" / "unmapped" / source_id
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw_date):
        raise ValueError(
            "Material originals require a valid storage date"
        )
    year, month, day = raw_date.split("-")
    return Path("source") / "ima" / year / month / day


def _non_conflicting_path(
    preferred: Path,
    *,
    source_id: str,
    content: bytes,
) -> Path:
    if not preferred.exists() or preferred.read_bytes() == content:
        return preferred
    suffix = preferred.suffix
    stem = preferred.stem
    return preferred.with_name(f"{stem}__{source_id[-8:]}{suffix}")


def _preferred_material_filename(
    *,
    document: dict[str, Any],
    fallback: str,
) -> str:
    title = str(document.get("title") or "").strip()
    if title.lower().endswith((".pdf", ".docx", ".pptx", ".xlsx", ".md", ".txt")):
        return _safe_filename(title)
    return _safe_filename(fallback)


def _prune_empty_directories(start: Path, *, stop: Path) -> None:
    current = start
    while current == stop or stop in current.parents:
        try:
            current.rmdir()
        except OSError:
            return
        if current == stop:
            return
        current = current.parent


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
        combined["ingestion_channel"] = (
            previous.get("ingestion_channel")
            or row.get("ingestion_channel")
        )
        combined["ingestion_channels"] = list(
            dict.fromkeys(
                [
                    *(previous.get("ingestion_channels") or []),
                    *(
                        [previous.get("ingestion_channel")]
                        if previous.get("ingestion_channel")
                        else []
                    ),
                    *(
                        [row.get("ingestion_channel")]
                        if row.get("ingestion_channel")
                        else []
                    ),
                ]
            )
        )
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


def _merge_directory_candidates(
    existing: list[dict[str, Any]],
    incoming: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for row in [*existing, *incoming]:
        candidate_id = str(row.get("candidate_id") or "")
        if not candidate_id:
            continue
        previous = merged.get(candidate_id) or {}
        combined = {**previous, **row}
        if not str(row.get("source_id") or "").strip():
            combined["source_id"] = previous.get("source_id", "")
        if previous.get("review_status") == "gpt_reviewed":
            for field_name in (
                "relevance_status",
                "relevance_reason",
                "review_status",
                "reviewed_at",
            ):
                combined[field_name] = previous.get(field_name)
        merged[candidate_id] = combined
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
