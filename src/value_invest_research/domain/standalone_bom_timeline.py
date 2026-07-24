from __future__ import annotations

from datetime import date
import hashlib
from typing import Any, Iterable

from value_invest_research.domain.material_intake import (
    INGESTION_CHANNELS,
    MATERIAL_CLASSES,
)


STANDALONE_LENSES = (
    ("demand", "需求侧"),
    ("supply", "供给侧"),
    ("technology", "技术侧"),
    ("valuation", "估值侧"),
    ("esg", "ESG"),
)


def normalize_timeline_claim(
    raw: dict[str, Any],
    *,
    bom_node_id: str,
    ingested_at: str,
) -> dict[str, Any]:
    lens_id = str(raw.get("lens_id") or "").strip()
    allowed_lenses = {item[0] for item in STANDALONE_LENSES}
    if lens_id not in allowed_lenses:
        raise ValueError(f"Unknown standalone BOM lens_id={lens_id!r}")
    published_at = _require_date(
        str(raw.get("published_at") or ""),
        "published_at",
    )
    source_id = str(raw.get("source_id") or "").strip()
    statement = str(raw.get("statement") or "").strip()
    if not source_id or not statement:
        raise ValueError("Timeline claims require source_id and statement")
    material_class = str(raw.get("material_class") or "other").strip()
    if material_class not in MATERIAL_CLASSES:
        raise ValueError(f"Invalid material_class={material_class!r}")
    ingestion_channel = str(
        raw.get("ingestion_channel") or "knowledge_base_scan"
    ).strip()
    if ingestion_channel not in INGESTION_CHANNELS:
        raise ValueError(f"Invalid ingestion_channel={ingestion_channel!r}")
    source_url = str(raw.get("source_url") or "").strip()
    claim_id = str(raw.get("claim_id") or "").strip() or _claim_id(
        bom_node_id=bom_node_id,
        lens_id=lens_id,
        source_id=source_id,
        statement=statement,
    )
    return {
        "claim_id": claim_id,
        "bom_node_id": bom_node_id,
        "lens_id": lens_id,
        "source_id": source_id,
        "published_at": published_at,
        "effective_period": str(raw.get("effective_period") or "").strip(),
        "target_period": str(raw.get("target_period") or "").strip(),
        "ingested_at": str(raw.get("ingested_at") or ingested_at).strip(),
        "material_class": material_class,
        "ingestion_channel": ingestion_channel,
        "claim_type": str(raw.get("claim_type") or "opinion").strip(),
        "stance": str(raw.get("stance") or "neutral").strip(),
        "source_title": str(raw.get("source_title") or source_id).strip(),
        "source_url": source_url,
        "source_location": str(raw.get("source_location") or "").strip(),
        "statement": statement,
        "review_status": str(
            raw.get("review_status") or "gpt_verified"
        ).strip(),
    }


def normalize_timeline_conclusion(
    raw: dict[str, Any],
    *,
    as_of_date: str,
) -> dict[str, Any]:
    lens_id = str(raw.get("lens_id") or "").strip()
    if lens_id not in {item[0] for item in STANDALONE_LENSES}:
        raise ValueError(f"Unknown standalone BOM lens_id={lens_id!r}")
    conclusion = str(raw.get("conclusion") or "").strip()
    if not conclusion:
        raise ValueError("Timeline conclusions require conclusion")
    return {
        "lens_id": lens_id,
        "as_of_date": _require_date(
            str(raw.get("as_of_date") or as_of_date),
            "as_of_date",
        ),
        "conclusion": conclusion,
        "trend": str(raw.get("trend") or "").strip(),
        "source_ids": list(
            dict.fromkeys(
                str(item)
                for item in raw.get("source_ids") or []
                if str(item).strip()
            )
        ),
        "review_status": str(
            raw.get("review_status") or "gpt_verified"
        ).strip(),
    }


def build_standalone_timeline_view(
    *,
    project: dict[str, Any],
    profile: dict[str, Any],
    claims: Iterable[dict[str, Any]],
    conclusions: Iterable[dict[str, Any]],
    as_of_date: str,
) -> dict[str, Any]:
    if project.get("report_scope") != "standalone-bom":
        raise ValueError("Standalone timeline view requires report_scope=standalone-bom")
    _require_date(as_of_date, "as_of_date")
    bom_node_id = str(project.get("bom_node_id") or "").strip()
    if not bom_node_id:
        raise ValueError("Standalone BOM project requires bom_node_id")
    claim_rows = [
        dict(row)
        for row in claims
        if str(row.get("published_at") or "") <= as_of_date
    ]
    conclusion_rows = [
        dict(row)
        for row in conclusions
        if str(row.get("as_of_date") or "") <= as_of_date
    ]
    profile_lenses = {
        str(row.get("lens_id") or ""): row
        for row in profile.get("lenses") or []
        if isinstance(row, dict)
    }
    lenses = []
    for lens_id, label in STANDALONE_LENSES:
        lens_claims = sorted(
            (
                row
                for row in claim_rows
                if str(row.get("lens_id") or "") == lens_id
            ),
            key=lambda row: (
                str(row.get("published_at") or ""),
                str(row.get("claim_id") or ""),
            ),
            reverse=True,
        )
        candidates = sorted(
            (
                row
                for row in conclusion_rows
                if str(row.get("lens_id") or "") == lens_id
            ),
            key=lambda row: str(row.get("as_of_date") or ""),
            reverse=True,
        )
        lens_profile = profile_lenses.get(lens_id) or {}
        current = candidates[0] if candidates else {}
        conclusion = str(
            current.get("conclusion")
            or lens_profile.get("baseline_conclusion")
            or ""
        ).strip()
        if not conclusion:
            conclusion = "当前尚无经过问题化解析和复核的材料，不能形成结论。"
        lenses.append(
            {
                "lens_id": lens_id,
                "label": label,
                "logic_chain": str(lens_profile.get("logic_chain") or "").strip(),
                "claims": lens_claims,
                "conclusion": conclusion,
                "trend": str(current.get("trend") or "").strip(),
            }
        )
    return {
        "title": str(project.get("title") or bom_node_id),
        "bom_node_id": bom_node_id,
        "report_scope": "standalone-bom",
        "as_of_date": as_of_date,
        "lenses": lenses,
    }


def _claim_id(
    *,
    bom_node_id: str,
    lens_id: str,
    source_id: str,
    statement: str,
) -> str:
    digest = hashlib.sha256(
        f"{bom_node_id}|{lens_id}|{source_id}|{statement}".encode("utf-8")
    ).hexdigest()[:20]
    return f"CLM-{digest.upper()}"


def _require_date(value: str, field_name: str) -> str:
    try:
        date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must use YYYY-MM-DD") from exc
    return value
