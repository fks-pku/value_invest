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
    "pending_publication_date",
    "pending_question_parse",
    "mapped",
    "unmapped_new_theme",
    "quarantined_post_cutoff",
    "rejected",
}

PUBLICATION_DATE_STATUSES = {
    "verified",
    "inferred_from_title",
    "needs_pdf_verification",
}

PUBLICATION_DATE_SOURCES = {
    "provider_published_at",
    "source_visible_at",
    "title_suffix",
    "pdf_cover",
    "pdf_header",
    "manual_verification",
    "unknown",
}

DIRECTORY_MAPPING_STATUSES = {
    "verified",
    "pending_directory_reconciliation",
    "not_applicable",
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
    provider_created_at: str = ""
    publication_date_status: str = "verified"
    publication_date_source: str = "provider_published_at"
    publication_date_locator: str = ""
    matched_bom_node_ids: tuple[str, ...] = field(default_factory=tuple)
    matched_question_numbers: tuple[int, ...] = field(default_factory=tuple)
    mapping_status: str = "pending_bom_mapping"
    allowed_usage: str = "research"
    raw_locator: str = ""
    directory_date: str = ""
    directory_path: str = ""
    directory_mapping_status: str = "not_applicable"
    relevance_status: str = ""
    relevance_score: int = 0
    relevance_reason: str = ""

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

    (
        published_at,
        publication_date_status,
        publication_date_source,
    ) = _publication_date(raw)
    modified_at = _normalize_optional_date(
        raw.get("modified_at") or raw.get("provider_modified_at")
    )
    provider_created_at = _normalize_optional_date(
        raw.get("provider_created_at")
    )
    directory_date = _normalize_optional_date(raw.get("directory_date"))
    directory_mapping_status = str(
        raw.get("directory_mapping_status") or ""
    ).strip()
    if not directory_mapping_status:
        if provider == "ima":
            directory_mapping_status = (
                "verified"
                if directory_date
                else "pending_directory_reconciliation"
            )
        else:
            directory_mapping_status = "not_applicable"
    bom_node_ids = _dedupe_strings(
        [*default_bom_node_ids, *_string_list(raw.get("matched_bom_node_ids"))]
    )
    question_numbers = _dedupe_question_numbers(
        [*default_question_numbers, *_int_list(raw.get("matched_question_numbers"))]
    )
    mapping_status = str(raw.get("mapping_status") or "").strip()
    if not mapping_status:
        if publication_date_status == "needs_pdf_verification":
            mapping_status = "pending_publication_date"
        else:
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
        provider_created_at=provider_created_at,
        publication_date_status=publication_date_status,
        publication_date_source=publication_date_source,
        publication_date_locator=str(
            raw.get("publication_date_locator") or ""
        ).strip(),
        matched_bom_node_ids=tuple(bom_node_ids),
        matched_question_numbers=tuple(question_numbers),
        mapping_status=mapping_status,
        allowed_usage=str(
            raw.get("allowed_usage")
            or (
                "date_verification_only"
                if publication_date_status == "needs_pdf_verification"
                else "research"
            )
        ).strip(),
        raw_locator=str(raw.get("raw_locator") or "").strip(),
        directory_date=directory_date,
        directory_path=str(raw.get("directory_path") or "").strip(),
        directory_mapping_status=directory_mapping_status,
        relevance_status=str(raw.get("relevance_status") or "").strip(),
        relevance_score=int(raw.get("relevance_score") or 0),
        relevance_reason=str(raw.get("relevance_reason") or "").strip(),
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
    if row.get("publication_date_status") == "needs_pdf_verification":
        row["mapping_status"] = "pending_publication_date"
        row["allowed_usage"] = "date_verification_only"
        return row
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
    question_labels_by_node: dict[str, dict[int, str]] | None = None,
) -> list[dict[str, Any]]:
    """Create narrow parse tasks without upgrading documents into evidence."""

    question_ids_by_node = question_ids_by_node or {}
    question_labels_by_node = question_labels_by_node or {}
    if document.get("mapping_status") in {"quarantined_post_cutoff", "rejected"}:
        return []
    nodes = _string_list(document.get("matched_bom_node_ids"))
    explicit_questions = _dedupe_question_numbers(
        _int_list(document.get("matched_question_numbers"))
    )
    rows: list[dict[str, Any]] = []
    for node_id in nodes:
        question_ids = question_ids_by_node.get(node_id) or {}
        question_labels = question_labels_by_node.get(node_id) or {}
        questions = (
            explicit_questions
            or sorted(question_ids)
            or sorted(question_labels)
            or list(range(1, 7))
        )
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
                    "question_label": question_labels.get(number, ""),
                    "material_class": document.get("material_class"),
                    "source_bucket": document.get("source_bucket"),
                    "ingestion_channel": document.get("ingestion_channel"),
                    "provider": document.get("provider"),
                    "published_at": document.get("published_at"),
                    "publication_date_status": document.get(
                        "publication_date_status"
                    ),
                    "publication_date_source": document.get(
                        "publication_date_source"
                    ),
                    "publication_date_locator": document.get(
                        "publication_date_locator"
                    ),
                    "source_title": document.get("title"),
                    "source_url": document.get("url"),
                    "source_summary": document.get("summary"),
                    "source_directory_date": document.get("directory_date"),
                    "source_directory_path": document.get("directory_path"),
                    "source_directory_mapping_status": document.get(
                        "directory_mapping_status"
                    ),
                    "preferred_parser": "deepseek",
                    "status": (
                        "pending_date_verification"
                        if document.get("publication_date_status")
                        == "needs_pdf_verification"
                        else "pending"
                    ),
                    "required_output": (
                        "verify the report publication date from the original "
                        "cover/header before question-specific atomic claims; "
                        "then return claims with source locator, "
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
        "discovered_at",
        "material_class",
        "source_bucket",
        "ingestion_channel",
        "provider",
        "content_hash",
        "mapping_status",
        "allowed_usage",
        "publication_date_status",
        "publication_date_source",
        "directory_mapping_status",
    ):
        if not str(document.get(field_name) or "").strip():
            issues.append(f"missing_{field_name}")
    if document.get("material_class") not in MATERIAL_CLASSES:
        issues.append("invalid_material_class")
    if document.get("ingestion_channel") not in INGESTION_CHANNELS:
        issues.append("invalid_ingestion_channel")
    if document.get("mapping_status") not in MAPPING_STATUSES:
        issues.append("invalid_mapping_status")
    publication_status = str(
        document.get("publication_date_status") or ""
    )
    publication_source = str(
        document.get("publication_date_source") or ""
    )
    if publication_status not in PUBLICATION_DATE_STATUSES:
        issues.append("invalid_publication_date_status")
    if publication_source not in PUBLICATION_DATE_SOURCES:
        issues.append("invalid_publication_date_source")
    directory_status = str(
        document.get("directory_mapping_status") or ""
    )
    if directory_status not in DIRECTORY_MAPPING_STATUSES:
        issues.append("invalid_directory_mapping_status")
    if document.get("provider") == "ima":
        directory_date = str(document.get("directory_date") or "")
        directory_path = str(document.get("directory_path") or "")
        if directory_status == "verified":
            try:
                _require_date(directory_date, "directory_date")
            except ValueError:
                issues.append("verified_ima_directory_date_missing")
            if not directory_path:
                issues.append("verified_ima_directory_path_missing")
        elif directory_status == "pending_directory_reconciliation":
            if directory_date or directory_path:
                issues.append("pending_ima_directory_must_be_blank")
    expected_bucket = SOURCE_BUCKET_BY_MATERIAL_CLASS.get(
        str(document.get("material_class") or "")
    )
    if expected_bucket and document.get("source_bucket") != expected_bucket:
        issues.append("material_class_source_bucket_mismatch")
    for field_name in ("discovered_at",):
        try:
            _require_date(str(document.get(field_name) or ""), field_name)
        except ValueError:
            issues.append(f"invalid_{field_name}")
    published_at = str(document.get("published_at") or "")
    if publication_status == "needs_pdf_verification":
        if published_at:
            issues.append("unverified_publication_date_must_be_blank")
        if document.get("mapping_status") != "pending_publication_date":
            issues.append("unverified_publication_date_not_pending")
        if document.get("allowed_usage") != "date_verification_only":
            issues.append("unverified_publication_date_usage")
    else:
        try:
            _require_date(published_at, "published_at")
        except ValueError:
            issues.append("invalid_published_at")
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
    directory_candidates = [
        row
        for row in bundle.get("directory_candidates") or []
        if isinstance(row, dict)
    ]
    node_inboxes = (
        bundle.get("node_inboxes")
        if isinstance(bundle.get("node_inboxes"), dict)
        else {}
    )
    question_numbers_by_node = {
        str(node_id): {
            int(number)
            for number in numbers or []
            if str(number).isdigit() and int(number) > 0
        }
        for node_id, numbers in (
            bundle.get("question_numbers_by_node") or {}
        ).items()
    }
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
            and document.get("published_at")
            and str(document.get("published_at") or "") > as_of_date
            and document.get("mapping_status") != "quarantined_post_cutoff"
        ):
            _validation_issue(
                issues,
                "post_cutoff_material_not_quarantined",
                f"{source_id} is visible after {as_of_date} but is not quarantined",
            )
        local_content_path = str(
            document.get("local_content_path") or ""
        ).strip()
        if (
            local_content_path
            and not local_content_path.startswith("source/")
        ):
            _validation_issue(
                issues,
                "material_original_outside_project_source",
                (
                    f"{source_id} original material must live under the "
                    "BOM project's source/ directory"
                ),
            )

    candidate_ids: set[str] = set()
    for candidate in directory_candidates:
        candidate_id = str(candidate.get("candidate_id") or "")
        if not candidate_id:
            _validation_issue(
                issues,
                "missing_directory_candidate_id",
                "directory candidate is missing candidate_id",
            )
            continue
        if candidate_id in candidate_ids:
            _validation_issue(
                issues,
                "duplicate_directory_candidate",
                f"duplicate directory candidate={candidate_id}",
            )
        candidate_ids.add(candidate_id)
        status = str(candidate.get("relevance_status") or "")
        if status not in {"relevant", "not_relevant", "needs_review"}:
            _validation_issue(
                issues,
                "invalid_directory_relevance_status",
                f"{candidate_id} has invalid relevance_status={status!r}",
            )
        source_id = str(candidate.get("source_id") or "")
        if status == "relevant" and source_id not in documents_by_source:
            _validation_issue(
                issues,
                "relevant_directory_candidate_not_ingested",
                (
                    f"{candidate_id} is relevant but has no matching "
                    "material document"
                ),
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
            allowed_question_numbers = (
                question_numbers_by_node.get(node_id) or set(range(1, 7))
            )
            if question_number not in allowed_question_numbers:
                _validation_issue(
                    issues,
                    "invalid_material_parse_question",
                    (
                        f"{task_id} has question_number={question_number!r}; "
                        f"allowed={sorted(allowed_question_numbers)}"
                    ),
                )
            if document.get("mapping_status") == "quarantined_post_cutoff":
                _validation_issue(
                    issues,
                    "quarantined_material_has_parse_task",
                    f"{task_id} was created for a post-cutoff quarantined source",
                )
            if (
                document.get("publication_date_status")
                == "needs_pdf_verification"
                and task.get("status") != "pending_date_verification"
            ):
                _validation_issue(
                    issues,
                    "unverified_material_parse_task_not_blocked",
                    (
                        f"{task_id} must verify the original publication "
                        "date before claim parsing"
                    ),
                )
            for field_name in (
                "material_class",
                "source_bucket",
                "ingestion_channel",
                "published_at",
                "publication_date_status",
                "publication_date_source",
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
            "directory_candidates": len(directory_candidates),
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


def _normalize_optional_date(value: Any) -> str:
    text = str(value or "").strip()
    return _normalize_date(text) if text else ""


def _publication_date(raw: dict[str, Any]) -> tuple[str, str, str]:
    explicit = raw.get("published_at") or raw.get("source_visible_at")
    status = str(raw.get("publication_date_status") or "").strip()
    source = str(raw.get("publication_date_source") or "").strip()
    if explicit:
        published_at = _normalize_date(explicit)
        return (
            published_at,
            status or "verified",
            source
            or (
                "source_visible_at"
                if raw.get("source_visible_at")
                else "provider_published_at"
            ),
        )
    return (
        "",
        status or "needs_pdf_verification",
        source or "unknown",
    )


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
    invalid = [value for value in rows if value < 1 or value > 99]
    if invalid:
        raise ValueError(f"Question numbers must be between 1 and 99, got {invalid}")
    return rows


def _slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()


def _validation_issue(
    issues: list[dict[str, str]],
    code: str,
    message: str,
) -> None:
    issues.append({"severity": "error", "code": code, "message": message})
