from __future__ import annotations

from datetime import date
from typing import Any

from value_invest_research.domain.standalone_bom_investment_engine import (
    build_standalone_investment_view,
    normalize_claim_mapping,
    normalize_entity_state,
    normalize_investment_snapshot,
    normalize_logic_state,
    normalize_thesis_revision,
)
from value_invest_research.domain.standalone_bom_timeline import (
    STANDALONE_LENSES,
    build_standalone_timeline_view,
    normalize_timeline_claim,
    normalize_timeline_conclusion,
)


def apply_standalone_bom_updates(
    *,
    repository: Any,
    renderer: Any,
    html_renderer: Any | None = None,
    raw_claims: list[dict[str, Any]],
    raw_conclusions: list[dict[str, Any]],
    as_of_date: str | None = None,
) -> dict[str, Any]:
    """Validate reviewed updates and rebuild the public HTML plus Markdown audit view."""

    as_of_date = as_of_date or date.today().isoformat()
    project = repository.load_project()
    bom_node_id = str(project.get("bom_node_id") or "")
    material_documents = (
        repository.load_material_documents()
        if hasattr(repository, "load_material_documents")
        else []
    )
    _validate_claim_publication_dates(raw_claims, material_documents)
    claims = [
        normalize_timeline_claim(
            row,
            bom_node_id=bom_node_id,
            ingested_at=as_of_date,
        )
        for row in raw_claims
    ]
    conclusions = [
        normalize_timeline_conclusion(row, as_of_date=as_of_date)
        for row in raw_conclusions
    ]
    repository.merge_claims(claims)
    repository.merge_sources_from_claims(claims)
    repository.merge_conclusions(conclusions)
    review_result = {"parse_tasks": 0, "documents": 0}
    if hasattr(repository, "finalize_material_reviews"):
        question_numbers = {
            lens_id: number
            for number, (lens_id, _) in enumerate(STANDALONE_LENSES, start=1)
        }
        claim_counts: dict[tuple[str, int], int] = {}
        for claim in claims:
            coordinate = (
                str(claim.get("source_id") or ""),
                question_numbers[str(claim.get("lens_id") or "")],
            )
            claim_counts[coordinate] = claim_counts.get(coordinate, 0) + 1
        reviewed_source_ids = {
            str(source_id)
            for conclusion in conclusions
            for source_id in conclusion.get("source_ids") or []
            if str(source_id).strip()
        }
        reviewed_source_ids.update(
            str(claim.get("source_id") or "")
            for claim in claims
            if str(claim.get("source_id") or "")
        )
        review_result = repository.finalize_material_reviews(
            reviewed_source_ids=reviewed_source_ids,
            claim_counts_by_coordinate=claim_counts,
            reviewed_at=as_of_date,
        )
    return refresh_standalone_bom_report(
        repository=repository,
        renderer=renderer,
        html_renderer=html_renderer,
        as_of_date=as_of_date,
        applied_claims=len(claims),
        applied_conclusions=len(conclusions),
        finalized_parse_tasks=review_result["parse_tasks"],
        finalized_documents=review_result["documents"],
    )


def _validate_claim_publication_dates(
    raw_claims: list[dict[str, Any]],
    material_documents: list[dict[str, Any]],
) -> None:
    documents_by_source = {
        str(row.get("source_id") or ""): row
        for row in material_documents
        if str(row.get("source_id") or "")
    }
    for claim in raw_claims:
        source_id = str(claim.get("source_id") or "")
        document = documents_by_source.get(source_id)
        if document is None:
            continue
        status = str(document.get("publication_date_status") or "")
        if status == "needs_pdf_verification":
            raise ValueError(
                f"{source_id} publication date must be verified from the "
                "original before claims enter the timeline"
            )
        document_date = str(document.get("published_at") or "")
        claim_date = str(claim.get("published_at") or "")
        if document_date and claim_date != document_date:
            raise ValueError(
                f"{source_id} claim published_at={claim_date!r} does not "
                f"match reviewed material date={document_date!r}"
            )


def refresh_standalone_bom_report(
    *,
    repository: Any,
    renderer: Any,
    html_renderer: Any | None = None,
    as_of_date: str | None = None,
    applied_claims: int = 0,
    applied_conclusions: int = 0,
    finalized_parse_tasks: int = 0,
    finalized_documents: int = 0,
) -> dict[str, Any]:
    as_of_date = as_of_date or date.today().isoformat()
    project = repository.load_project()
    profile = repository.load_profile()
    if hasattr(repository, "load_claim_mappings"):
        view = build_standalone_investment_view(
            project=project,
            profile=profile,
            claims=repository.load_claims(),
            conclusions=repository.load_conclusions(),
            claim_mappings=repository.load_claim_mappings(),
            logic_states=repository.load_logic_states(),
            entity_states=repository.load_entity_states(),
            thesis_revisions=repository.load_thesis_revisions(),
            investment_snapshots=repository.load_investment_snapshots(),
            as_of_date=as_of_date,
        )
    else:
        view = build_standalone_timeline_view(
            project=project,
            profile=profile,
            claims=repository.load_claims(),
            conclusions=repository.load_conclusions(),
            as_of_date=as_of_date,
        )
    markdown_path = repository.write_report(renderer.render(view))
    html_path = None
    if html_renderer is not None and hasattr(repository, "write_html_report"):
        html_path = repository.write_html_report(html_renderer.render(view))
    return {
        "report_path": str(html_path or markdown_path),
        "html_report_path": str(html_path) if html_path else "",
        "markdown_report_path": str(markdown_path),
        "as_of_date": as_of_date,
        "claims": sum(len(lens["claims"]) for lens in view["lenses"]),
        "applied_claims": applied_claims,
        "applied_conclusions": applied_conclusions,
        "finalized_parse_tasks": finalized_parse_tasks,
        "finalized_documents": finalized_documents,
    }


def apply_standalone_bom_engine_updates(
    *,
    repository: Any,
    renderer: Any,
    html_renderer: Any | None = None,
    raw_mappings: list[dict[str, Any]],
    raw_logic_states: list[dict[str, Any]],
    raw_entity_states: list[dict[str, Any]],
    raw_revisions: list[dict[str, Any]],
    raw_investment_snapshots: list[dict[str, Any]],
    as_of_date: str | None = None,
) -> dict[str, Any]:
    """Validate reviewed engine artifacts, persist them, and rebuild the report."""

    as_of_date = as_of_date or date.today().isoformat()
    profile = repository.load_profile()
    claims_by_id = {
        str(row.get("claim_id") or ""): row
        for row in repository.load_claims()
        if str(row.get("claim_id") or "")
    }
    mappings = [
        normalize_claim_mapping(
            row,
            claims_by_id=claims_by_id,
            profile=profile,
            mapped_at=as_of_date,
        )
        for row in raw_mappings
    ]
    states = [
        normalize_logic_state(
            row,
            profile=profile,
            claims_by_id=claims_by_id,
            as_of_date=as_of_date,
        )
        for row in raw_logic_states
    ]
    entity_states = [
        normalize_entity_state(
            row,
            profile=profile,
            claims_by_id=claims_by_id,
            as_of_date=as_of_date,
        )
        for row in raw_entity_states
    ]
    revisions = [
        normalize_thesis_revision(
            row,
            profile=profile,
            claims_by_id=claims_by_id,
            as_of_date=as_of_date,
        )
        for row in raw_revisions
    ]
    snapshots = [
        normalize_investment_snapshot(
            row,
            profile=profile,
            claims_by_id=claims_by_id,
            as_of_date=as_of_date,
        )
        for row in raw_investment_snapshots
    ]
    repository.merge_claim_mappings(mappings)
    repository.merge_logic_states(states)
    repository.merge_entity_states(entity_states)
    repository.merge_thesis_revisions(revisions)
    repository.merge_investment_snapshots(snapshots)
    result = refresh_standalone_bom_report(
        repository=repository,
        renderer=renderer,
        html_renderer=html_renderer,
        as_of_date=as_of_date,
    )
    result.update(
        {
            "applied_mappings": len(mappings),
            "applied_logic_states": len(states),
            "applied_entity_states": len(entity_states),
            "applied_revisions": len(revisions),
            "applied_investment_snapshots": len(snapshots),
        }
    )
    return result
