from __future__ import annotations

from datetime import date
from typing import Any

from value_invest_research.domain.standalone_bom_timeline import (
    build_standalone_timeline_view,
    normalize_timeline_claim,
    normalize_timeline_conclusion,
)


def apply_standalone_bom_updates(
    *,
    repository: Any,
    renderer: Any,
    raw_claims: list[dict[str, Any]],
    raw_conclusions: list[dict[str, Any]],
    as_of_date: str | None = None,
) -> dict[str, Any]:
    """Validate reviewed updates, append them, and rebuild public Markdown."""

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
    return refresh_standalone_bom_report(
        repository=repository,
        renderer=renderer,
        as_of_date=as_of_date,
        applied_claims=len(claims),
        applied_conclusions=len(conclusions),
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
    as_of_date: str | None = None,
    applied_claims: int = 0,
    applied_conclusions: int = 0,
) -> dict[str, Any]:
    as_of_date = as_of_date or date.today().isoformat()
    view = build_standalone_timeline_view(
        project=repository.load_project(),
        profile=repository.load_profile(),
        claims=repository.load_claims(),
        conclusions=repository.load_conclusions(),
        as_of_date=as_of_date,
    )
    path = repository.write_report(renderer.render(view))
    return {
        "report_path": str(path),
        "as_of_date": as_of_date,
        "claims": sum(len(lens["claims"]) for lens in view["lenses"]),
        "applied_claims": applied_claims,
        "applied_conclusions": applied_conclusions,
    }
