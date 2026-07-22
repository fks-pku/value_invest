from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FileSystemTemporalResearchLedgerRepository:
    """File-system adapter for one BOM node's temporal research ledger."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    @property
    def project_dir_label(self) -> str:
        return str(self.project_dir)

    def load_prior_snapshots(self) -> list[dict[str, Any]]:
        snapshots_dir = self.project_dir / "snapshots"
        if not snapshots_dir.is_dir():
            return []
        rows = []
        for path in sorted(snapshots_dir.glob("*/thesis_snapshot.json")):
            try:
                rows.append(json.loads(path.read_text(encoding="utf-8")))
            except (OSError, json.JSONDecodeError):
                continue
        return rows

    def load_documents(self) -> list[dict[str, Any]]:
        return _read_jsonl(self.project_dir / "ledger" / "documents.jsonl")

    def load_claims(self) -> list[dict[str, Any]]:
        return _read_jsonl(self.project_dir / "ledger" / "claims.jsonl")

    def write_temporal_bundle(self, bundle: dict[str, Any]) -> None:
        ledger_dir = self.project_dir / "ledger"
        snapshot_dir = self.project_dir / "snapshots" / str(bundle["as_of_date"])
        ledger_dir.mkdir(parents=True, exist_ok=True)
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        _write_jsonl(
            ledger_dir / "documents.jsonl",
            _merge_rows(
                _read_jsonl(ledger_dir / "documents.jsonl"),
                bundle.get("documents") or [],
                key_fields=("source_id",),
            ),
        )
        _write_jsonl(
            ledger_dir / "claims.jsonl",
            _merge_rows(
                _read_jsonl(ledger_dir / "claims.jsonl"),
                bundle.get("claims") or [],
                key_fields=("claim_id",),
            ),
        )
        _write_jsonl(
            ledger_dir / "thesis_revisions.jsonl",
            _merge_rows(
                _read_jsonl(ledger_dir / "thesis_revisions.jsonl"),
                bundle.get("revisions") or [],
                key_fields=("revision_id",),
            ),
        )
        _write_jsonl(
            ledger_dir / "coverage.jsonl",
            _merge_rows(
                _read_jsonl(ledger_dir / "coverage.jsonl"),
                bundle.get("coverage") or [],
                key_fields=("as_of_date", "question_number"),
            ),
        )
        _write_jsonl(ledger_dir / "unmapped_sources.jsonl", bundle.get("unmapped_sources") or [])
        _write_json(snapshot_dir / "thesis_snapshot.json", bundle.get("snapshot") or {})
        _write_json(
            self.project_dir / "temporal_manifest.json",
            {
                "schema_version": bundle.get("schema_version") or "1.0",
                "node_id": bundle.get("node_id"),
                "current_as_of_date": bundle.get("as_of_date"),
                "documents_path": "ledger/documents.jsonl",
                "claims_path": "ledger/claims.jsonl",
                "revisions_path": "ledger/thesis_revisions.jsonl",
                "coverage_path": "ledger/coverage.jsonl",
                "unmapped_sources_path": "ledger/unmapped_sources.jsonl",
                "current_snapshot_path": (
                    f"snapshots/{bundle.get('as_of_date')}/thesis_snapshot.json"
                ),
            },
        )


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    content = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    path.write_text(content, encoding="utf-8")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def _merge_rows(
    existing: list[dict[str, Any]],
    incoming: list[dict[str, Any]],
    *,
    key_fields: tuple[str, ...],
) -> list[dict[str, Any]]:
    """Keep old ledger rows and deterministically replace only the same identity."""

    merged: dict[tuple[str, ...], dict[str, Any]] = {}
    for row in [*existing, *incoming]:
        key = tuple(str(row.get(field) or "") for field in key_fields)
        if not all(key):
            continue
        merged[key] = row
    return [merged[key] for key in sorted(merged)]
