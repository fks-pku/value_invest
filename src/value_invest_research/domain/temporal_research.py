from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
import re
from typing import Any, Iterable


QUESTION_NUMBERS = tuple(range(1, 7))
CLAIM_TYPES = {
    "actual",
    "forecast",
    "opinion",
    "message",
    "valuation",
    "refutation",
}
STANCE_TYPES = {"support", "refute", "neutral", "lead"}


@dataclass(frozen=True)
class ResearchCoordinate:
    """Stable logical address for one atomic research claim."""

    bom_node_id: str
    question_number: int
    question_id: str
    topic_tags: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class TemporalClaim:
    """One append-only fact, forecast, opinion, message, or refutation."""

    claim_id: str
    source_id: str
    coordinate: ResearchCoordinate
    statement: str
    claim_type: str
    stance: str
    published_at: str
    effective_period: str = ""
    target_period: str = ""
    ingested_at: str = ""
    entity: str = ""
    metric_name: str = ""
    mapping_origin: str = "question_specific_parse"
    mapping_confidence: str = "high"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload.update(payload.pop("coordinate"))
        payload["topic_tags"] = list(payload.get("topic_tags") or [])
        return payload


@dataclass(frozen=True)
class QuestionSnapshot:
    """One as-of conclusion for a BOM six-question coordinate."""

    question_number: int
    question_id: str
    question: str
    conclusion: str
    conclusion_strength: str
    target_impact: str
    source_ids: tuple[str, ...]
    claim_ids: tuple[str, ...]
    latest_material_at: str
    change_state: str
    change_summary: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["source_ids"] = list(self.source_ids)
        payload["claim_ids"] = list(self.claim_ids)
        return payload


def build_temporal_research_bundle(
    *,
    node_id: str,
    as_of_date: str,
    questions: Iterable[dict[str, Any]],
    sources: Iterable[dict[str, Any]],
    claims: Iterable[dict[str, Any]] = (),
    prior_snapshots: Iterable[dict[str, Any]] = (),
) -> dict[str, Any]:
    """Build an append-only evidence ledger and one reproducible thesis snapshot."""

    _require_date(as_of_date, "as_of_date")
    source_rows = [dict(item) for item in sources]
    source_by_id = {
        str(item.get("source_id") or ""): item
        for item in source_rows
        if str(item.get("source_id") or "").strip()
    }
    question_rows = [dict(item) for item in questions]
    _validate_questions(node_id, question_rows)

    claim_rows = _normalize_claims(
        node_id=node_id,
        as_of_date=as_of_date,
        questions=question_rows,
        source_by_id=source_by_id,
        claims=claims,
    )
    prior_by_question = _latest_prior_question_snapshots(prior_snapshots, as_of_date)
    claims_by_question: dict[int, list[dict[str, Any]]] = {
        number: [] for number in QUESTION_NUMBERS
    }
    for claim in claim_rows:
        claims_by_question[int(claim["question_number"])].append(claim)

    snapshots = []
    revisions = []
    coverage = []
    for question in question_rows:
        number = int(question["question_number"])
        question_claims = sorted(
            claims_by_question[number],
            key=lambda item: (item.get("published_at") or "", item.get("claim_id") or ""),
        )
        prior = prior_by_question.get(number)
        snapshot = _build_question_snapshot(
            question=question,
            claims=question_claims,
            prior=prior,
        )
        snapshots.append(snapshot)
        revisions.append(_build_revision(node_id, as_of_date, snapshot, prior))
        coverage.append(_coverage_row(as_of_date, number, question_claims))

    mapped_source_ids = {claim["source_id"] for claim in claim_rows}
    unmapped = [
        {
            "source_id": source_id,
            "title": str(source.get("title") or source_id),
            "published_at": str(source.get("source_visible_at") or source.get("published_at") or ""),
            "reason": "source_not_mapped_to_any_bom_question",
        }
        for source_id, source in source_by_id.items()
        if source_id not in mapped_source_ids
    ]
    return {
        "schema_version": "1.0",
        "node_id": node_id,
        "as_of_date": as_of_date,
        "documents": source_rows,
        "claims": claim_rows,
        "snapshot": {
            "schema_version": "1.0",
            "node_id": node_id,
            "as_of_date": as_of_date,
            "questions": snapshots,
        },
        "revisions": revisions,
        "coverage": coverage,
        "unmapped_sources": unmapped,
    }


def validate_temporal_research_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    node_id = str(bundle.get("node_id") or "")
    as_of_date = str(bundle.get("as_of_date") or "")
    try:
        _require_date(as_of_date, "as_of_date")
    except ValueError as exc:
        _issue(issues, "invalid_as_of_date", str(exc))
    if not node_id:
        _issue(issues, "missing_node_id", "temporal bundle must identify one BOM node")

    source_ids = {
        str(item.get("source_id") or "")
        for item in bundle.get("documents") or []
        if isinstance(item, dict)
    }
    claim_ids: set[str] = set()
    for claim in bundle.get("claims") or []:
        claim_id = str(claim.get("claim_id") or "")
        if not claim_id or claim_id in claim_ids:
            _issue(issues, "duplicate_or_missing_claim_id", claim_id or "claim id is empty")
        claim_ids.add(claim_id)
        if claim.get("bom_node_id") != node_id:
            _issue(issues, "claim_node_mismatch", f"{claim_id} does not map to {node_id}")
        if int(claim.get("question_number") or 0) not in QUESTION_NUMBERS:
            _issue(issues, "claim_question_number", f"{claim_id} must map to one of six questions")
        if claim.get("source_id") not in source_ids:
            _issue(issues, "claim_source_missing", f"{claim_id} references an unknown source")
        if claim.get("claim_type") not in CLAIM_TYPES:
            _issue(issues, "claim_type", f"{claim_id} has an invalid claim_type")
        if claim.get("stance") not in STANCE_TYPES:
            _issue(issues, "claim_stance", f"{claim_id} has an invalid stance")
        published_at = str(claim.get("published_at") or "")
        try:
            _require_date(published_at, f"{claim_id}.published_at")
        except ValueError as exc:
            _issue(issues, "claim_published_at", str(exc))
        if published_at and as_of_date and published_at > as_of_date:
            _issue(issues, "post_cutoff_claim", f"{claim_id} is visible after {as_of_date}")

    snapshot_questions = (bundle.get("snapshot") or {}).get("questions") or []
    numbers = [int(item.get("question_number") or 0) for item in snapshot_questions]
    if numbers != list(QUESTION_NUMBERS):
        _issue(issues, "snapshot_question_coverage", "snapshot must preserve the ordered six questions")
    coverage_numbers = [int(item.get("question_number") or 0) for item in bundle.get("coverage") or []]
    if coverage_numbers != list(QUESTION_NUMBERS):
        _issue(issues, "coverage_question_coverage", "coverage must preserve the ordered six questions")

    return {
        "ok": not issues,
        "issues": issues,
        "summary": {
            "node_id": node_id,
            "claims": len(claim_ids),
            "questions": len(snapshot_questions),
            "unmapped_sources": len(bundle.get("unmapped_sources") or []),
        },
    }


def _normalize_claims(
    *,
    node_id: str,
    as_of_date: str,
    questions: list[dict[str, Any]],
    source_by_id: dict[str, dict[str, Any]],
    claims: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    question_by_number = {int(item["question_number"]): item for item in questions}
    raw_claims = [dict(item) for item in claims]
    if not raw_claims:
        for question in questions:
            for source_id in _string_list(question.get("source_ids")):
                source = source_by_id.get(source_id)
                if not source:
                    continue
                raw_claims.append(
                    {
                        "source_id": source_id,
                        "question_number": question["question_number"],
                        "statement": source.get("summary") or source.get("title") or source_id,
                        "claim_type": _claim_type(source, int(question["question_number"])),
                        "stance": _stance(source, int(question["question_number"])),
                        "mapping_origin": "migrated_question_source_reference",
                        "mapping_confidence": "medium",
                    }
                )

    normalized = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_claims, start=1):
        number = int(raw.get("question_number") or 0)
        question = question_by_number.get(number)
        source_id = str(raw.get("source_id") or "")
        source = source_by_id.get(source_id)
        if not question or not source:
            continue
        published_at = str(
            raw.get("published_at")
            or source.get("source_visible_at")
            or source.get("published_at")
            or ""
        )
        if not published_at or published_at > as_of_date:
            continue
        claim_id = str(raw.get("claim_id") or "") or _claim_id(
            node_id,
            number,
            source_id,
            index,
        )
        if claim_id in seen:
            continue
        seen.add(claim_id)
        claim = TemporalClaim(
            claim_id=claim_id,
            source_id=source_id,
            coordinate=ResearchCoordinate(
                bom_node_id=node_id,
                question_number=number,
                question_id=str(question.get("question_id") or f"{node_id}_q{number}"),
                topic_tags=tuple(_string_list(raw.get("topic_tags"))),
            ),
            statement=str(raw.get("statement") or source.get("summary") or source.get("title") or ""),
            claim_type=str(raw.get("claim_type") or _claim_type(source, number)),
            stance=str(raw.get("stance") or _stance(source, number)),
            published_at=published_at,
            effective_period=str(raw.get("effective_period") or ""),
            target_period=str(raw.get("target_period") or ""),
            ingested_at=str(raw.get("ingested_at") or as_of_date),
            entity=str(raw.get("entity") or ""),
            metric_name=str(raw.get("metric_name") or ""),
            mapping_origin=str(raw.get("mapping_origin") or "question_specific_parse"),
            mapping_confidence=str(raw.get("mapping_confidence") or "high"),
        ).to_dict()
        normalized.append(claim)
    return sorted(normalized, key=lambda item: (item["published_at"], item["claim_id"]))


def _build_question_snapshot(
    *,
    question: dict[str, Any],
    claims: list[dict[str, Any]],
    prior: dict[str, Any] | None,
) -> dict[str, Any]:
    number = int(question["question_number"])
    source_ids = tuple(dict.fromkeys(claim["source_id"] for claim in claims))
    latest = max((claim["published_at"] for claim in claims), default="")
    conclusion = str(question.get("conclusion") or question.get("answer") or "当前尚未形成可验证结论。")
    strength = str(question.get("conclusion_strength") or "待验证")
    if prior:
        changed = (
            str(prior.get("conclusion") or "") != conclusion
            or str(prior.get("conclusion_strength") or "") != strength
        )
        change_state = "changed" if changed else "unchanged"
        change_summary = (
            "当前结论或强度相较上一研究快照发生变化。"
            if changed
            else "当前结论与上一研究快照一致；新增材料只补强或补充边界。"
        )
    else:
        change_state = "baseline_no_prior_snapshot"
        change_summary = "这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。"
    return QuestionSnapshot(
        question_number=number,
        question_id=str(question.get("question_id") or f"q{number}"),
        question=str(question.get("question") or ""),
        conclusion=conclusion,
        conclusion_strength=strength,
        target_impact=str(question.get("target_impact") or ""),
        source_ids=source_ids,
        claim_ids=tuple(claim["claim_id"] for claim in claims),
        latest_material_at=latest,
        change_state=change_state,
        change_summary=change_summary,
    ).to_dict()


def _build_revision(
    node_id: str,
    as_of_date: str,
    snapshot: dict[str, Any],
    prior: dict[str, Any] | None,
) -> dict[str, Any]:
    number = int(snapshot["question_number"])
    return {
        "revision_id": f"REV-{_slug(node_id)}-q{number}-{as_of_date}",
        "bom_node_id": node_id,
        "question_number": number,
        "question_id": snapshot["question_id"],
        "recorded_at": as_of_date,
        "revision_type": "baseline" if prior is None else snapshot["change_state"],
        "previous_conclusion": str((prior or {}).get("conclusion") or ""),
        "current_conclusion": snapshot["conclusion"],
        "change_summary": snapshot["change_summary"],
        "trigger_claim_ids": list(snapshot["claim_ids"]),
        "target_impact": snapshot["target_impact"],
    }


def _coverage_row(as_of_date: str, question_number: int, claims: list[dict[str, Any]]) -> dict[str, Any]:
    types = {claim["claim_type"] for claim in claims}
    dates = [claim["published_at"] for claim in claims if claim.get("published_at")]
    support = sum(claim["stance"] == "support" for claim in claims)
    refute = sum(claim["stance"] == "refute" for claim in claims)
    return {
        "as_of_date": as_of_date,
        "question_number": question_number,
        "material_count": len(claims),
        "actual_count": sum(claim["claim_type"] == "actual" for claim in claims),
        "forecast_count": sum(claim["claim_type"] == "forecast" for claim in claims),
        "opinion_count": sum(claim["claim_type"] == "opinion" for claim in claims),
        "message_count": sum(claim["claim_type"] == "message" for claim in claims),
        "valuation_count": sum(claim["claim_type"] == "valuation" for claim in claims),
        "refutation_count": sum(claim["claim_type"] == "refutation" or claim["stance"] == "refute" for claim in claims),
        "support_count": support,
        "refute_count": refute,
        "latest_material_at": max(dates, default=""),
        "earliest_material_at": min(dates, default=""),
        "coverage_status": _coverage_status(types, support, refute),
    }


def _coverage_status(types: set[str], support: int, refute: int) -> str:
    if support and refute and ("actual" in types or "forecast" in types):
        return "双向覆盖"
    if support and ("actual" in types or "forecast" in types):
        return "单向覆盖，缺反证"
    if support or refute:
        return "有材料，结构不完整"
    return "材料缺口"


def _latest_prior_question_snapshots(
    snapshots: Iterable[dict[str, Any]],
    as_of_date: str,
) -> dict[int, dict[str, Any]]:
    candidates = [
        dict(snapshot)
        for snapshot in snapshots
        if str(snapshot.get("as_of_date") or "") < as_of_date
    ]
    if not candidates:
        return {}
    latest = max(candidates, key=lambda item: str(item.get("as_of_date") or ""))
    return {
        int(item.get("question_number") or 0): dict(item)
        for item in latest.get("questions") or []
        if int(item.get("question_number") or 0) in QUESTION_NUMBERS
    }


def _validate_questions(node_id: str, questions: list[dict[str, Any]]) -> None:
    numbers = [int(item.get("question_number") or 0) for item in questions]
    if numbers != list(QUESTION_NUMBERS):
        raise ValueError(f"{node_id} temporal research must preserve the ordered six questions")
    question_ids = [str(item.get("question_id") or "") for item in questions]
    if not all(question_ids) or len(question_ids) != len(set(question_ids)):
        raise ValueError(f"{node_id} temporal question ids must be non-empty and unique")


def _claim_type(source: dict[str, Any], question_number: int) -> str:
    if question_number == 5:
        return "valuation"
    if question_number == 6:
        return "refutation"
    bucket = str(source.get("source_bucket") or "evidence")
    if bucket == "research_report":
        return "forecast"
    if bucket == "opinion":
        return "opinion"
    if bucket == "message":
        return "message"
    return "actual"


def _stance(source: dict[str, Any], question_number: int) -> str:
    if question_number == 6:
        return "refute"
    bucket = str(source.get("source_bucket") or "evidence")
    if bucket in {"message", "opinion"}:
        return "lead"
    return "support"


def _claim_id(node_id: str, question_number: int, source_id: str, index: int) -> str:
    return f"CLM-{_slug(node_id)}-q{question_number}-{_slug(source_id)}-{index:03d}"


def _slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", str(value)).strip("-").lower()


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, (list, tuple)):
        return []
    return [str(item) for item in value if str(item).strip()]


def _require_date(value: str, field_name: str) -> None:
    try:
        date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must use YYYY-MM-DD") from exc


def _issue(issues: list[dict[str, str]], code: str, message: str) -> None:
    issues.append({"severity": "error", "code": code, "message": message})
