#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

from value_invest_research.adapters.outbound.filesystem_temporal_research import (
    FileSystemTemporalResearchLedgerRepository,
)
from value_invest_research.application.use_cases.build_bom_temporal_research import (
    build_bom_temporal_research,
)


def main() -> int:
    payload = json.load(sys.stdin)
    project_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
    repository = (
        FileSystemTemporalResearchLedgerRepository(project_dir)
        if project_dir is not None
        else None
    )
    sources = _merge_records(
        repository.load_documents() if repository is not None else [],
        payload.get("sources") or [],
        identity=lambda row: str(row.get("source_id") or ""),
    )
    claims = _merge_claim_records(
        repository.load_claims() if repository is not None else [],
        payload.get("claims") or [],
    )
    result = build_bom_temporal_research(
        node_id=str(payload.get("node_id") or ""),
        as_of_date=str(payload.get("as_of_date") or ""),
        questions=payload.get("questions") or [],
        sources=sources,
        claims=claims,
        prior_snapshots=(
            payload.get("prior_snapshots")
            or (repository.load_prior_snapshots() if repository is not None else [])
        ),
    )
    if repository is not None:
        repository.write_temporal_bundle(result)
    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def _merge_records(existing: list[dict], incoming: list[dict], *, identity) -> list[dict]:
    merged = {}
    for row in [*existing, *incoming]:
        if not isinstance(row, dict):
            continue
        key = identity(row)
        if key:
            merged[key] = row
    return list(merged.values())


def _claim_identity(row: dict) -> str:
    fields = (
        row.get("source_id"),
        row.get("question_number"),
        row.get("statement"),
        row.get("claim_type"),
        row.get("stance"),
        row.get("effective_period"),
        row.get("target_period"),
    )
    return "|".join(str(value or "") for value in fields)


def _merge_claim_records(existing: list[dict], incoming: list[dict]) -> list[dict]:
    merged = {}
    for row in existing:
        if isinstance(row, dict) and _claim_identity(row):
            merged[_claim_identity(row)] = row
    for row in incoming:
        if not isinstance(row, dict) or not _claim_identity(row):
            continue
        key = _claim_identity(row)
        prior = merged.get(key) or {}
        next_row = {**prior, **row}
        if prior.get("claim_id"):
            next_row["claim_id"] = prior["claim_id"]
        merged[key] = next_row
    return list(merged.values())


if __name__ == "__main__":
    raise SystemExit(main())
