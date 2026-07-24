from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FileSystemStandaloneBomTimelineRepository:
    """Filesystem source of truth for one standalone BOM timeline."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    def load_project(self) -> dict[str, Any]:
        return _read_json(self.project_dir / "project.json")

    def load_profile(self) -> dict[str, Any]:
        return _read_json(self.project_dir / "timeline_profile.json")

    def load_claims(self) -> list[dict[str, Any]]:
        return _read_jsonl(self.project_dir / "ledger" / "claims.jsonl")

    def load_conclusions(self) -> list[dict[str, Any]]:
        return _read_jsonl(self.project_dir / "ledger" / "conclusions.jsonl")

    def load_material_documents(self) -> list[dict[str, Any]]:
        return _read_jsonl(
            self.project_dir / "material_intake" / "documents.jsonl"
        )

    def write_report(self, markdown: str) -> Path:
        path = self.project_dir / "professional_report.md"
        path.write_text(markdown, encoding="utf-8")
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

    def merge_sources_from_claims(self, claims: list[dict[str, Any]]) -> int:
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
            }
            for claim in claims
        ]
        return _merge_jsonl(
            self.project_dir / "sources.jsonl",
            rows,
            key_fields=("source_id",),
        )


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


def _source_bucket(material_class: str) -> str:
    if material_class in {"official_filing", "official_company"}:
        return "evidence"
    if material_class in {"sell_side_research", "authoritative_third_party"}:
        return "research_report"
    if material_class == "expert_opinion":
        return "opinion"
    return "message"
