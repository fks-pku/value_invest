from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
import hashlib
import json
import re
from typing import Any, Iterable


MATERIAL_CLASSES = {
    "official_filing",
    "official_company",
    "sell_side_research",
    "authoritative_third_party",
    "market_news",
    "expert_opinion",
    "other",
}

INGESTION_CHANNELS = {
    "question_search",
    "knowledge_base_scan",
    "manual_import",
}

SOURCE_BUCKET_BY_MATERIAL_CLASS = {
    "official_filing": "evidence",
    "official_company": "evidence",
    "sell_side_research": "research_report",
    "authoritative_third_party": "research_report",
    "market_news": "message",
    "expert_opinion": "opinion",
    "other": "message",
}

MAPPING_STATUSES = {
    "pending_bom_mapping",
    "pending_question_parse",
    "mapped",
    "unmapped_new_theme",
    "quarantined_post_cutoff",
    "rejected",
}


@dataclass(frozen=True)
class MaterialDocument:
    """One discovered source before question-specific claim parsing."""

    source_id: str
    external_id: str
    title: str
    url: str
    publisher: str
    published_at: str
    discovered_at: str
    material_class: str
    source_bucket: str
    ingestion_channel: str
    provider: str
    summary: str = ""
    content_hash: str = ""
    knowledge_base_ref: str = ""
    modified_at: str = ""
    matched_bom_node_ids: tuple[str, ...] = field(default_factory=tuple)
    matched_question_numbers: tuple[int, ...] = field(default_factory=tuple)
    mapping_status: str = "pending_bom_mapping"
    allowed_usage: str = "research"
    raw_locator: str = ""

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["matched_bom_node_ids"] = list(self.matched_bom_node_ids)
        payload["matched_question_numbers"] = list(self.matched_question_numbers)
        return payload


def normalize_material_document(
    raw: dict[str, Any],
    *,
    ingestion_channel: str,
    provider: str,
    discovered_at: str,
    default_bom_node_ids: Iterable[str] = (),
    default_question_numbers: Iterable[int] = (),
) -> dict[str, Any]:
    """Normalize search and knowledge-base results into one intake contract."""

    if ingestion_channel not in INGESTION_CHANNELS:
        raise ValueError(f"Unsupported ingestion_channel={ingestion_channel!r}")
    _require_date(discovered_at, "discovered_at")
    external_id = str(
        raw.get("external_id")
        or raw.get("media_id")
        or raw.get("id")
        or raw.get("url")
        or raw.get("title")
        or ""
    ).strip()
    title = str(raw.get("title") or "").strip()
    if not external_id or not title:
        raise ValueError("Material documents require external_id and title")

    material_class = str(raw.get("material_class") or "").strip()
    if not material_class:
        material_class = infer_material_class(raw)
    if material_class not in MATERIAL_CLASSES:
        raise ValueError(f"Unsupported material_class={material_class!r}")
    source_bucket = str(
        raw.get("source_bucket")
        or SOURCE_BUCKET_BY_MATERIAL_CLASS[material_class]
    )
    expected_bucket = SOURCE_BUCKET_BY_MATERIAL_CLASS[material_class]
    if source_bucket != expected_bucket:
        raise ValueError(
            f"{material_class} must map to source_bucket={expected_bucket}, got {source_bucket}"
        )

    published_at = _normalize_date(
        raw.get("published_at")
        or raw.get("source_visible_at")
        or raw.get("created_at")
        or raw.get("modified_at")
        or discovered_at
    )
    modified_at = _normalize_date(raw.get("modified_at") or published_at)
    bom_node_ids = _dedupe_strings(
        [*default_bom_node_ids, *_string_list(raw.get("matched_bom_node_ids"))]
    )
    question_numbers = _dedupe_question_numbers(
        [*default_question_numbers, *_int_list(raw.get("matched_question_numbers"))]
    )
    mapping_status = str(raw.get("mapping_status") or "").strip()
    if not mapping_status:
        mapping_status = (
            "pending_question_parse" if bom_node_ids else "pending_bom_mapping"
        )
    if mapping_status not in MAPPING_STATUSES:
        raise ValueError(f"Unsupported mapping_status={mapping_status!r}")

    source_id = str(raw.get("source_id") or "").strip() or _source_id(
        provider,
        external_id,
    )
    summary = str(
        raw.get("summary")
        or raw.get("highlight_content")
        or raw.get("abstract")
        or ""
    ).strip()
    content_hash = str(raw.get("content_hash") or "").strip() or _content_hash(
        {
            "external_id": external_id,
            "title": title,
            "url": str(raw.get("url") or ""),
            "published_at": published_at,
            "summary": summary,
        }
    )
    document = MaterialDocument(
        source_id=source_id,
        external_id=external_id,
        title=title,
        url=str(raw.get("url") or "").strip(),
        publisher=str(raw.get("publisher") or raw.get("source_name") or provider).strip(),
        published_at=published_at,
        discovered_at=discovered_at,
        material_class=material_class,
        source_bucket=source_bucket,
        ingestion_channel=ingestion_channel,
        provider=provider,
        summary=summary,
        content_hash=content_hash,
        knowledge_base_ref=_opaque_reference(
            raw.get("knowledge_base_ref") or raw.get("knowledge_base_id")
        ),
        modified_at=modified_at,
        matched_bom_node_ids=tuple(bom_node_ids),
        matched_question_numbers=tuple(question_numbers),
        mapping_status=mapping_status,
        allowed_usage=str(raw.get("allowed_usage") or "research").strip(),
        raw_locator=str(raw.get("raw_locator") or "").strip(),
    )
    return document.to_dict()


def apply_time_slice_policy(
    document: dict[str, Any],
    *,
    mode: str,
    as_of_date: str,
) -> dict[str, Any]:
    """Quarantine post-cutoff discoveries before parse-task creation."""

    row = dict(document)
    if mode != "historical_backtest":
        return row
    _require_date(as_of_date, "as_of_date")
    if str(row.get("published_at") or "") > as_of_date:
        row["mapping_status"] = "quarantined_post_cutoff"
        row["allowed_usage"] = "quarantine_only"
    return row


def build_material_parse_tasks(
    document: dict[str, Any],
    *,
    question_ids_by_node: dict[str, dict[int, str]] | None = None,
) -> list[dict[str, Any]]:
    """Create narrow parse tasks without upgrading documents into evidence."""

    question_ids_by_node = question_ids_by_node or {}
    if document.get("mapping_status") in {"quarantined_post_cutoff", "rejected"}:
        return []
    nodes = _string_list(document.get("matched_bom_node_ids"))
    explicit_questions = _dedupe_question_numbers(
        _int_list(document.get("matched_question_numbers"))
    )
    questions = explicit_questions or list(range(1, 7))
    rows: list[dict[str, Any]] = []
    for node_id in nodes:
        question_ids = question_ids_by_node.get(node_id) or {}
        for number in questions:
            question_id = question_ids.get(number) or f"{node_id}_q{number}"
            rows.append(
                {
                    "task_id": (
                        f"PARSE-{_slug(node_id)}-q{number}-"
                        f"{_slug(str(document.get('source_id') or 'source'))}"
                    ),
                    "source_id": document.get("source_id"),
                    "bom_node_id": node_id,
                    "question_number": number,
                    "question_id": question_id,
                    "material_class": document.get("material_class"),
                    "source_bucket": document.get("source_bucket"),
                    "ingestion_channel": document.get("ingestion_channel"),
                    "provider": document.get("provider"),
                    "published_at": document.get("published_at"),
                    "source_title": document.get("title"),
                    "source_url": document.get("url"),
                    "source_summary": document.get("summary"),
                    "preferred_parser": "deepseek",
                    "status": "pending",
                    "required_output": (
                        "question-specific atomic claims with source locator, "
                        "stance, four time fields, gaps, and contradictions"
                    ),
                }
            )
    return rows


def validate_material_document(document: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for field_name in (
        "source_id",
        "external_id",
        "title",
        "published_at",
        "discovered_at",
        "material_class",
        "source_bucket",
        "ingestion_channel",
        "provider",
        "content_hash",
        "mapping_status",
        "allowed_usage",
    ):
        if not str(document.get(field_name) or "").strip():
            issues.append(f"missing_{field_name}")
    if document.get("material_class") not in MATERIAL_CLASSES:
        issues.append("invalid_material_class")
    if document.get("ingestion_channel") not in INGESTION_CHANNELS:
        issues.append("invalid_ingestion_channel")
    if document.get("mapping_status") not in MAPPING_STATUSES:
        issues.append("invalid_mapping_status")
    expected_bucket = SOURCE_BUCKET_BY_MATERIAL_CLASS.get(
        str(document.get("material_class") or "")
    )
    if expected_bucket and document.get("source_bucket") != expected_bucket:
        issues.append("material_class_source_bucket_mismatch")
    for field_name in ("published_at", "discovered_at"):
        try:
            _require_date(str(document.get(field_name) or ""), field_name)
        except ValueError:
            issues.append(f"invalid_{field_name}")
    return issues


def validate_material_intake_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    """Validate intake, routing, and cutoff rules without filesystem knowledge."""

    project = bundle.get("project") if isinstance(bundle.get("project"), dict) else {}
    known_nodes = {
        str(item)
        for item in bundle.get("known_bom_node_ids") or []
        if str(item).strip()
    }
    documents = [
        row for row in bundle.get("documents") or [] if isinstance(row, dict)
    ]
    node_inboxes = (
        bundle.get("node_inboxes")
        if isinstance(bundle.get("node_inboxes"), dict)
        else {}
    )
    issues = list(bundle.get("load_issues") or [])
    mode = str(
        project.get("mode")
        or project.get("run_mode")
        or "historical_backtest"
    )
    as_of_date = str(project.get("as_of_date") or "")
    documents_by_source: dict[str, dict[str, Any]] = {}

    for document in documents:
        source_id = str(document.get("source_id") or "")
        for code in validate_material_document(document):
            _validation_issue(
                issues,
                code,
                f"{source_id or '<unknown>'} failed material validation: {code}",
            )
        if source_id in documents_by_source:
            _validation_issue(
                issues,
                "duplicate_material_source",
                f"duplicate material source_id={source_id}",
            )
        documents_by_source[source_id] = document
        routed_nodes = {
            str(item)
            for item in document.get("matched_bom_node_ids") or []
            if str(item).strip()
        }
        unknown_nodes = sorted(routed_nodes - known_nodes)
        if unknown_nodes:
            _validation_issue(
                issues,
                "unknown_material_bom_route",
                f"{source_id} routes to unknown BOM nodes: {unknown_nodes}",
            )
        if (
            mode == "historical_backtest"
            and as_of_date
            and str(document.get("published_at") or "") > as_of_date
            and document.get("mapping_status") != "quarantined_post_cutoff"
        ):
            _validation_issue(
                issues,
                "post_cutoff_material_not_quarantined",
                f"{source_id} is visible after {as_of_date} but is not quarantined",
            )

    task_count = 0
    for node_id, inbox in node_inboxes.items():
        if node_id not in known_nodes:
            _validation_issue(
                issues,
                "unknown_inbox_bom_node",
                f"inbox belongs to unknown BOM node={node_id}",
            )
        inbox = inbox if isinstance(inbox, dict) else {}
        inbox_materials = [
            row for row in inbox.get("materials") or [] if isinstance(row, dict)
        ]
        parse_tasks = [
            row for row in inbox.get("parse_tasks") or [] if isinstance(row, dict)
        ]
        inbox_source_ids = {
            str(row.get("source_id") or "") for row in inbox_materials
        }
        task_ids: set[str] = set()
        for task in parse_tasks:
            task_count += 1
            task_id = str(task.get("task_id") or "")
            source_id = str(task.get("source_id") or "")
            if not task_id:
                _validation_issue(
                    issues,
                    "missing_material_parse_task_id",
                    f"{node_id} contains a parse task without task_id",
                )
            elif task_id in task_ids:
                _validation_issue(
                    issues,
                    "duplicate_material_parse_task",
                    f"duplicate task_id={task_id} in {node_id}",
                )
            task_ids.add(task_id)
            document = documents_by_source.get(source_id)
            if document is None:
                _validation_issue(
                    issues,
                    "material_parse_source_missing",
                    f"{task_id} points to missing source_id={source_id}",
                )
                continue
            if source_id not in inbox_source_ids:
                _validation_issue(
                    issues,
                    "material_parse_source_not_in_inbox",
                    f"{task_id} source is absent from {node_id}/inbox/materials.jsonl",
                )
            if str(task.get("bom_node_id") or "") != node_id:
                _validation_issue(
                    issues,
                    "material_parse_bom_mismatch",
                    f"{task_id} must stay inside BOM node={node_id}",
                )
            if node_id not in (document.get("matched_bom_node_ids") or []):
                _validation_issue(
                    issues,
                    "material_parse_route_mismatch",
                    f"{task_id} is not covered by the source BOM route",
                )
            question_number = task.get("question_number")
            if question_number not in range(1, 7):
                _validation_issue(
                    issues,
                    "invalid_material_parse_question",
                    f"{task_id} has question_number={question_number!r}",
                )
            if document.get("mapping_status") == "quarantined_post_cutoff":
                _validation_issue(
                    issues,
                    "quarantined_material_has_parse_task",
                    f"{task_id} was created for a post-cutoff quarantined source",
                )
            for field_name in (
                "material_class",
                "source_bucket",
                "ingestion_channel",
            ):
                if task.get(field_name) != document.get(field_name):
                    _validation_issue(
                        issues,
                        "material_parse_metadata_drift",
                        f"{task_id} {field_name} differs from source metadata",
                    )

    return {
        "ok": not any(issue.get("severity") == "error" for issue in issues),
        "issues": issues,
        "summary": {
            "documents": len(documents),
            "parse_tasks": task_count,
            "bom_inboxes": len(node_inboxes),
            "quarantined_documents": sum(
                row.get("mapping_status") == "quarantined_post_cutoff"
                for row in documents
            ),
        },
    }


def infer_material_class(raw: dict[str, Any]) -> str:
    source_type = str(raw.get("source_type") or "").lower()
    title = str(raw.get("title") or "").lower()
    publisher = str(raw.get("publisher") or raw.get("source_name") or "").lower()
    url = str(raw.get("url") or raw.get("source_url") or "").lower()
    tags = " ".join(str(item).lower() for item in raw.get("tags") or [])
    text = " ".join((source_type, title, publisher, url, tags))
    if _contains_any(
        text,
        (
            "10-k",
            "10-q",
            "20-f",
            "annual report",
            "quarterly report",
            "results announcement",
            "earnings release",
            "财报",
            "年报",
            "季报",
            "业绩公告",
            "sec.gov",
            "hkexnews.hk",
        ),
    ):
        return "official_filing"
    if _contains_any(
        text,
        (
            "investor relations",
            "company ir",
            "company_ir",
            "investor day",
            "prepared remarks",
            "earnings call",
            "earnings transcript",
            "公司公告",
            "投资者关系",
        ),
    ):
        return "official_company"
    if _contains_any(
        text,
        (
            "sell-side",
            "sell side",
            "sell_side",
            "sell_side_report",
            "broker research",
            "equity research",
            "research report",
            "research_report",
            "research_report_pdf",
            "深度报告",
            "证券研究",
            "研报",
        ),
    ):
        return "sell_side_research"
    if _contains_any(
        text,
        (
            "industry data",
            "industry_data",
            "industry association",
            "consulting",
            "database",
            "semi analysis",
            "semianalysis",
            "omdia",
            "gartner",
            "idc",
            "trendforce",
            "dell'oro",
            "第三方",
            "行业协会",
        ),
    ):
        return "authoritative_third_party"
    if _contains_any(text, ("expert", "interview", "opinion", "blog", "专家", "访谈", "观点")):
        return "expert_opinion"
    if _contains_any(text, ("news", "media", "rumor", "新闻", "消息", "传闻")):
        return "market_news"
    legacy_bucket = str(
        raw.get("source_bucket") or raw.get("information_category") or ""
    ).strip()
    if legacy_bucket == "evidence":
        return "official_company"
    if legacy_bucket == "research_report":
        return "authoritative_third_party"
    if legacy_bucket == "opinion":
        return "expert_opinion"
    if legacy_bucket == "message":
        return "market_news"
    return "other"


def _source_id(provider: str, external_id: str) -> str:
    digest = hashlib.sha256(
        f"{provider}:{external_id}".encode("utf-8")
    ).hexdigest()[:16]
    return f"SRC-{_slug(provider).upper()}-{digest.upper()}"


def _content_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _opaque_reference(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if text.startswith("ima_kb:"):
        return text
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    return f"ima_kb:{digest}"


def _normalize_date(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError("date value is required")
    normalized = text[:10]
    _require_date(normalized, "date")
    return normalized


def _require_date(value: str, field_name: str) -> None:
    try:
        date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must use YYYY-MM-DD") from exc


def _contains_any(text: str, tokens: tuple[str, ...]) -> bool:
    return any(token in text for token in tokens)


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, (list, tuple, set)):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _int_list(value: Any) -> list[int]:
    if not isinstance(value, (list, tuple, set)):
        return []
    rows: list[int] = []
    for item in value:
        try:
            rows.append(int(item))
        except (TypeError, ValueError):
            continue
    return rows


def _dedupe_strings(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(value).strip() for value in values if str(value).strip()))


def _dedupe_question_numbers(values: Iterable[int]) -> list[int]:
    rows = list(dict.fromkeys(int(value) for value in values))
    invalid = [value for value in rows if value not in range(1, 7)]
    if invalid:
        raise ValueError(f"Question numbers must be 1-6, got {invalid}")
    return rows


def _slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()


def _validation_issue(
    issues: list[dict[str, str]],
    code: str,
    message: str,
) -> None:
    issues.append({"severity": "error", "code": code, "message": message})
