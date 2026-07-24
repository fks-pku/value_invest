from __future__ import annotations

from datetime import date
import hashlib
import re
from typing import Any


RELEVANCE_STATUSES = {
    "relevant",
    "not_relevant",
    "needs_review",
}


def classify_bom_material(
    raw: dict[str, Any],
    *,
    bom_node_id: str,
    profile: dict[str, Any],
    scanned_at: str,
) -> dict[str, Any]:
    """Classify one directory material before any original is downloaded."""

    title = str(raw.get("title") or "").strip()
    external_id = str(raw.get("external_id") or raw.get("media_id") or "").strip()
    if not title or not external_id:
        raise ValueError("Directory candidates require title and external_id")
    _require_date(scanned_at, "scanned_at")
    directory_date = _require_date(
        str(raw.get("directory_date") or ""),
        "directory_date",
    )
    normalized_text = _normalize_text(
        " ".join(
            [
                title,
                str(raw.get("summary") or ""),
                " ".join(str(item) for item in raw.get("tags") or []),
            ]
        )
    )
    direct_hits = _matching_terms(normalized_text, profile.get("direct_terms"))
    entity_hits = _matching_terms(normalized_text, profile.get("entity_terms"))
    context_hits = _matching_terms(normalized_text, profile.get("context_terms"))
    supply_hits = _matching_terms(normalized_text, profile.get("supply_terms"))
    exclusion_hits = _matching_terms(normalized_text, profile.get("exclude_terms"))

    score = (
        len(direct_hits) * 5
        + len(entity_hits) * 3
        + len(context_hits)
        + len(supply_hits) * 2
        - len(exclusion_hits) * 4
    )
    if direct_hits:
        status = "relevant"
        reason = "标题或标签直接命中 BOM 核心术语"
    elif entity_hits and (context_hits or supply_hits):
        status = "relevant"
        reason = "命中 BOM 相关公司且同时命中产业语境"
    elif supply_hits and context_hits:
        status = "relevant"
        reason = "命中 BOM 关键供给环节且同时命中 AI/算力语境"
    elif entity_hits or (supply_hits and not exclusion_hits):
        status = "needs_review"
        reason = "存在邻近关联，但仅凭目录元数据不能确认"
    else:
        status = "not_relevant"
        reason = "目录元数据未形成当前 BOM 的直接或组合命中"

    matched_terms = list(
        dict.fromkeys(
            [*direct_hits, *entity_hits, *context_hits, *supply_hits]
        )
    )
    candidate_id = _candidate_id(
        provider=str(raw.get("provider") or "ima"),
        external_id=external_id,
        bom_node_id=bom_node_id,
    )
    return {
        "candidate_id": candidate_id,
        "source_id": str(raw.get("source_id") or "").strip(),
        "external_id": external_id,
        "provider": str(raw.get("provider") or "ima"),
        "bom_node_id": bom_node_id,
        "title": title,
        "directory_date": directory_date,
        "directory_path": str(raw.get("directory_path") or "").strip(),
        "published_at": str(raw.get("published_at") or ""),
        "publication_date_status": str(
            raw.get("publication_date_status") or "needs_pdf_verification"
        ),
        "publication_date_source": str(
            raw.get("publication_date_source") or "unknown"
        ),
        "directory_mapping_status": str(
            raw.get("directory_mapping_status") or "verified"
        ),
        "media_type": raw.get("media_type"),
        "relevance_status": status,
        "relevance_score": score,
        "matched_terms": matched_terms,
        "excluded_terms": exclusion_hits,
        "relevance_reason": reason,
        "review_status": (
            "profile_approved" if status != "needs_review" else "pending_gpt_review"
        ),
        "scanned_at": scanned_at,
    }


def validate_relevance_profile(profile: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if not isinstance(profile, dict):
        return ["material_relevance_profile must be an object"]
    if not _terms(profile.get("direct_terms")):
        issues.append("material_relevance_profile.direct_terms is required")
    if not (
        _terms(profile.get("entity_terms"))
        or _terms(profile.get("supply_terms"))
    ):
        issues.append(
            "material_relevance_profile requires entity_terms or supply_terms"
        )
    if not _terms(profile.get("context_terms")):
        issues.append("material_relevance_profile.context_terms is required")
    return issues


def _matching_terms(text: str, values: Any) -> list[str]:
    return [term for term in _terms(values) if _normalize_text(term) in text]


def _terms(values: Any) -> list[str]:
    if not isinstance(values, (list, tuple)):
        return []
    return list(
        dict.fromkeys(
            str(value).strip()
            for value in values
            if str(value).strip()
        )
    )


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", "", str(value or "").casefold())


def _candidate_id(*, provider: str, external_id: str, bom_node_id: str) -> str:
    digest = hashlib.sha256(
        f"{provider}|{external_id}|{bom_node_id}".encode("utf-8")
    ).hexdigest()[:20]
    return f"CAND-{digest.upper()}"


def _require_date(value: str, field_name: str) -> str:
    try:
        date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must use YYYY-MM-DD") from exc
    return value
