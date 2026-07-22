from __future__ import annotations

from typing import Any, Iterable

from value_invest_research.domain.temporal_research import (
    build_temporal_research_bundle,
    validate_temporal_research_bundle,
)


def build_bom_temporal_research(
    *,
    node_id: str,
    as_of_date: str,
    questions: Iterable[dict[str, Any]],
    sources: Iterable[dict[str, Any]],
    claims: Iterable[dict[str, Any]] = (),
    prior_snapshots: Iterable[dict[str, Any]] = (),
) -> dict[str, Any]:
    """Create one BOM evidence ledger plus its current six-question snapshot."""

    bundle = build_temporal_research_bundle(
        node_id=node_id,
        as_of_date=as_of_date,
        questions=questions,
        sources=sources,
        claims=claims,
        prior_snapshots=prior_snapshots,
    )
    validation = validate_temporal_research_bundle(bundle)
    if not validation["ok"]:
        details = "; ".join(issue["message"] for issue in validation["issues"])
        raise ValueError(f"Invalid BOM temporal research bundle: {details}")
    bundle["validation"] = validation["summary"]
    return bundle
