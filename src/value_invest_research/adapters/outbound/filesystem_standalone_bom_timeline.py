from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FileSystemStandaloneBomTimelineRepository:
    """Filesystem source of truth for one standalone BOM timeline."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    @property
    def project_dir_label(self) -> str:
        return str(self.project_dir)

    def load_project(self) -> dict[str, Any]:
        return _read_json(self.project_dir / "project.json")

    def load_profile(self) -> dict[str, Any]:
        return _read_json(self.project_dir / "timeline_profile.json")

    def load_claims(self) -> list[dict[str, Any]]:
        return _read_jsonl(self.project_dir / "ledger" / "claims.jsonl")

    def load_conclusions(self) -> list[dict[str, Any]]:
        return _read_jsonl(self.project_dir / "ledger" / "conclusions.jsonl")

    def load_claim_mappings(self) -> list[dict[str, Any]]:
        return _read_jsonl(
            self.project_dir / "ledger" / "claim_mappings.jsonl"
        )

    def load_logic_states(self) -> list[dict[str, Any]]:
        return _read_jsonl(
            self.project_dir / "ledger" / "logic_states.jsonl"
        )

    def load_entity_states(self) -> list[dict[str, Any]]:
        return _read_jsonl(
            self.project_dir / "ledger" / "entity_states.jsonl"
        )

    def load_thesis_revisions(self) -> list[dict[str, Any]]:
        return _read_jsonl(
            self.project_dir / "ledger" / "thesis_revisions.jsonl"
        )

    def load_investment_snapshots(self) -> list[dict[str, Any]]:
        return _read_jsonl(
            self.project_dir / "ledger" / "investment_snapshots.jsonl"
        )

    def load_material_documents(self) -> list[dict[str, Any]]:
        return _read_jsonl(
            self.project_dir / "material_intake" / "documents.jsonl"
        )

    def write_report(self, markdown: str) -> Path:
        path = self.project_dir / "professional_report.md"
        path.write_text(markdown, encoding="utf-8")
        return path

    def write_html_report(self, html: str) -> Path:
        path = self.project_dir / "professional_report.html"
        path.write_text(html, encoding="utf-8")
        return path

    def merge_claims(self, rows: list[dict[str, Any]]) -> int:
        return _merge_jsonl(
            self.project_dir / "ledger" / "claims.jsonl",
            rows,
            key_fields=("claim_id",),
        )

    def merge_conclusions(self, rows: list[dict[str, Any]]) -> int:
        return _merge_jsonl(
            self.project_dir / "ledger" / "conclusions.jsonl",
            rows,
            key_fields=("lens_id", "as_of_date"),
        )

    def merge_claim_mappings(self, rows: list[dict[str, Any]]) -> int:
        return _merge_jsonl(
            self.project_dir / "ledger" / "claim_mappings.jsonl",
            rows,
            key_fields=("mapping_id",),
        )

    def merge_logic_states(self, rows: list[dict[str, Any]]) -> int:
        return _merge_jsonl(
            self.project_dir / "ledger" / "logic_states.jsonl",
            rows,
            key_fields=("logic_node_id", "as_of_date"),
        )

    def merge_entity_states(self, rows: list[dict[str, Any]]) -> int:
        return _merge_jsonl(
            self.project_dir / "ledger" / "entity_states.jsonl",
            rows,
            key_fields=("logic_node_id", "entity_id", "as_of_date"),
        )

    def merge_thesis_revisions(self, rows: list[dict[str, Any]]) -> int:
        return _merge_jsonl(
            self.project_dir / "ledger" / "thesis_revisions.jsonl",
            rows,
            key_fields=("revision_id",),
        )

    def merge_investment_snapshots(self, rows: list[dict[str, Any]]) -> int:
        return _merge_jsonl(
            self.project_dir / "ledger" / "investment_snapshots.jsonl",
            rows,
            key_fields=("as_of_date",),
        )

    def merge_sources_from_claims(self, claims: list[dict[str, Any]]) -> int:
        documents_by_source = {
            str(row.get("source_id") or ""): row
            for row in self.load_material_documents()
            if str(row.get("source_id") or "")
        }
        rows = [
            {
                "source_id": claim["source_id"],
                "title": claim["source_title"],
                "material_class": claim["material_class"],
                "ingestion_channel": claim["ingestion_channel"],
                "source_bucket": _source_bucket(claim["material_class"]),
                "url": claim["source_url"],
                "published_at": claim["published_at"],
                "original_location": claim["source_location"],
                "summary": claim["statement"],
                "availability_proof": _availability_proof(
                    documents_by_source.get(str(claim["source_id"])) or {},
                    published_at=str(claim["published_at"]),
                ),
            }
            for claim in claims
        ]
        return _merge_jsonl(
            self.project_dir / "sources.jsonl",
            rows,
            key_fields=("source_id",),
        )

    def finalize_material_reviews(
        self,
        *,
        reviewed_source_ids: set[str],
        claim_counts_by_coordinate: dict[tuple[str, int], int],
        reviewed_at: str,
    ) -> dict[str, int]:
        """Close question-specific parse tasks after GPT-reviewed claims land."""

        if not reviewed_source_ids:
            return {"parse_tasks": 0, "documents": 0}

        tasks_path = self.project_dir / "inbox" / "parse_tasks.jsonl"
        tasks = _read_jsonl(tasks_path)
        finalized_tasks = 0
        for task in tasks:
            source_id = str(task.get("source_id") or "")
            if source_id not in reviewed_source_ids:
                continue
            question_number = int(task.get("question_number") or 0)
            claim_count = claim_counts_by_coordinate.get(
                (source_id, question_number),
                0,
            )
            task.update(
                {
                    "status": "completed",
                    "review_status": "gpt_verified",
                    "reviewed_at": reviewed_at,
                    "claim_count": claim_count,
                    "review_note": (
                        "question-specific atomic claims promoted"
                        if claim_count
                        else "reviewed; no lens-specific atomic claim promoted"
                    ),
                }
            )
            finalized_tasks += 1
        if tasks_path.is_file():
            _write_jsonl(tasks_path, tasks)

        finalized_documents = 0
        for path in (
            self.project_dir / "material_intake" / "documents.jsonl",
            self.project_dir / "inbox" / "materials.jsonl",
        ):
            documents = _read_jsonl(path)
            changed = False
            for document in documents:
                if str(document.get("source_id") or "") not in reviewed_source_ids:
                    continue
                document["mapping_status"] = "mapped"
                document["review_status"] = "gpt_verified"
                document["reviewed_at"] = reviewed_at
                finalized_documents += path.name == "documents.jsonl"
                changed = True
            if changed:
                _write_jsonl(path, documents)

        return {
            "parse_tasks": finalized_tasks,
            "documents": finalized_documents,
        }


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            payload = json.loads(line)
            if isinstance(payload, dict):
                rows.append(payload)
    return rows


def _merge_jsonl(
    path: Path,
    incoming: list[dict[str, Any]],
    *,
    key_fields: tuple[str, ...],
) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    merged: dict[tuple[str, ...], dict[str, Any]] = {}
    for row in [*_read_jsonl(path), *incoming]:
        key = tuple(str(row.get(field) or "") for field in key_fields)
        if all(key):
            merged[key] = row
    rows = [merged[key] for key in sorted(merged)]
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    return len(rows)


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def _source_bucket(material_class: str) -> str:
    if material_class in {"official_filing", "official_company"}:
        return "evidence"
    if material_class in {"sell_side_research", "authoritative_third_party"}:
        return "research_report"
    if material_class == "expert_opinion":
        return "opinion"
    return "message"


def _availability_proof(
    document: dict[str, Any],
    *,
    published_at: str,
) -> dict[str, str]:
    proof_type = str(
        document.get("publication_date_source") or "claim_published_at"
    ).strip()
    locator = str(document.get("publication_date_locator") or "").strip()
    return {
        "proof_type": proof_type,
        "proof_value": published_at,
        "locator": locator,
    }
