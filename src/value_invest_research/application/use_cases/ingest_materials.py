from __future__ import annotations

from datetime import date
import hashlib
from typing import Any, Iterable

from value_invest_research.domain.material_intake import (
    apply_time_slice_policy,
    build_material_parse_tasks,
    normalize_material_document,
    validate_material_document,
)
from value_invest_research.domain.material_relevance import (
    classify_bom_material,
    validate_relevance_profile,
)


def ingest_material_batch(
    *,
    repository: Any,
    raw_documents: Iterable[dict[str, Any]],
    provider: str,
    feed_id: str,
    ingestion_channel: str,
    discovered_at: str,
    known_bom_node_ids: Iterable[str],
    mode: str,
    as_of_date: str,
    default_bom_node_ids: Iterable[str] = (),
    default_question_numbers: Iterable[int] = (),
    question_ids_by_node: dict[str, dict[int, str]] | None = None,
    question_labels_by_node: dict[str, dict[int, str]] | None = None,
    leaf_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Normalize, deduplicate, route, and queue one material batch."""

    known_nodes = set(str(item) for item in known_bom_node_ids)
    leaf_search_required = bool(
        getattr(repository, "leaf_search_required", False)
    )
    if (
        leaf_search_required
        and ingestion_channel == "question_search"
        and not leaf_context
    ):
        raise ValueError(
            "This project requires the current active question for every material search"
        )
    if leaf_context:
        leaf_context = _normalize_active_question_context(leaf_context)
        missing_leaf_fields = [
            field_name
            for field_name in (
                "l3_plan_id",
                "l3_node_id",
                "question_node_id",
                "question_level",
                "research_step_id",
            )
            if not str(leaf_context.get(field_name) or "").strip()
        ]
        if missing_leaf_fields:
            raise ValueError(
                "Active-question material search is missing trace fields: "
                + ", ".join(missing_leaf_fields)
            )
    defaults = list(dict.fromkeys(str(item) for item in default_bom_node_ids))
    unknown_defaults = sorted(set(defaults) - known_nodes)
    if unknown_defaults:
        raise ValueError(f"Unknown BOM nodes in material route: {unknown_defaults}")
    seen_external_ids = repository.load_seen_external_ids(provider, feed_id)
    documents = []
    skipped_seen = 0
    for raw in raw_documents:
        raw_external_id = str(
            raw.get("external_id")
            or raw.get("media_id")
            or raw.get("id")
            or raw.get("url")
            or raw.get("title")
            or ""
        ).strip()
        if raw_external_id and raw_external_id in seen_external_ids:
            skipped_seen += 1
            continue
        document = normalize_material_document(
            raw,
            ingestion_channel=ingestion_channel,
            provider=provider,
            discovered_at=discovered_at,
            default_bom_node_ids=defaults,
            default_question_numbers=default_question_numbers,
        )
        routed_nodes = set(document.get("matched_bom_node_ids") or [])
        unknown_nodes = sorted(routed_nodes - known_nodes)
        if unknown_nodes:
            raise ValueError(
                f"Material {document['source_id']} maps to unknown BOM nodes: {unknown_nodes}"
            )
        document = apply_time_slice_policy(
            document,
            mode=mode,
            as_of_date=as_of_date,
        )
        issues = validate_material_document(document)
        if issues:
            raise ValueError(
                f"Invalid material {document.get('source_id')}: {', '.join(issues)}"
            )
        documents.append(document)

    scan_id = _scan_id(provider, feed_id, discovered_at, documents)
    resolved_leaf_context = (
        {**dict(leaf_context or {}), "search_run_id": scan_id}
        if leaf_context
        else None
    )
    parse_tasks = (
        [
            task
            for document in documents
            for task in build_material_parse_tasks(
                document,
                question_ids_by_node=question_ids_by_node,
                question_labels_by_node=question_labels_by_node,
                leaf_context=resolved_leaf_context,
            )
        ]
        if not leaf_search_required or resolved_leaf_context
        else []
    )
    scan_event = {
        "scan_id": scan_id,
        "provider": provider,
        "feed_id": feed_id,
        "ingestion_channel": ingestion_channel,
        "scanned_at": discovered_at,
        "mode": mode,
        "as_of_date": as_of_date,
        "discovered_count": len(documents),
        "skipped_seen_count": skipped_seen,
        "quarantined_count": sum(
            document.get("mapping_status") == "quarantined_post_cutoff"
            for document in documents
        ),
        "parse_task_count": len(parse_tasks),
        "evidence_eligibility": (
            "active_question_specific"
            if resolved_leaf_context
            else "candidate_only"
            if leaf_search_required
            else "legacy_question_coordinate"
        ),
    }
    if resolved_leaf_context:
        scan_event.update(resolved_leaf_context)
    persisted = repository.persist_material_batch(
        documents=documents,
        parse_tasks=parse_tasks,
        scan_event=scan_event,
    )
    return {
        "scan_event": scan_event,
        "documents": documents,
        "parse_tasks": parse_tasks,
        "persistence": persisted,
    }


def _normalize_active_question_context(context: dict[str, Any]) -> dict[str, Any]:
    """Accept legacy leaf names while persisting the level-agnostic coordinates."""

    row = dict(context)
    row.setdefault("question_node_id", row.get("leaf_question_id"))
    row.setdefault("question_level", row.get("level"))
    row.setdefault("research_step_id", row.get("leaf_step_id"))
    return row


def scan_knowledge_base_materials(
    *,
    feed: Any,
    repository: Any,
    knowledge_base_id: str,
    bom_queries: dict[str, list[str]],
    known_bom_node_ids: Iterable[str],
    mode: str,
    as_of_date: str,
    discovered_at: str | None = None,
    max_results_per_query: int = 20,
    question_ids_by_node: dict[str, dict[int, str]] | None = None,
    question_labels_by_node: dict[str, dict[int, str]] | None = None,
    fetch_originals: bool = False,
    publication_date_extractor: Any | None = None,
) -> dict[str, Any]:
    """Scan IMA per BOM query and route new reports into parse inboxes."""

    discovered_at = discovered_at or date.today().isoformat()
    known_nodes = set(str(item) for item in known_bom_node_ids)
    unknown = sorted(set(bom_queries) - known_nodes)
    if unknown:
        raise ValueError(f"Knowledge-base queries reference unknown BOM nodes: {unknown}")
    knowledge_base_ref = _opaque_feed_scope(knowledge_base_id)
    runs = []
    for node_id, queries in bom_queries.items():
        for query in queries:
            raw_documents = feed.search_materials(
                knowledge_base_id=knowledge_base_id,
                query=query,
                max_results=max_results_per_query,
            )
            for document in raw_documents:
                document.pop("knowledge_base_id", None)
                document["knowledge_base_ref"] = knowledge_base_ref
            runs.append(
                ingest_material_batch(
                    repository=repository,
                    raw_documents=raw_documents,
                    provider=feed.provider_name,
                    feed_id=(
                        f"{knowledge_base_ref}:{node_id}:"
                        f"{_opaque_feed_scope(query)}"
                    ),
                    ingestion_channel="knowledge_base_scan",
                    discovered_at=discovered_at,
                    known_bom_node_ids=known_nodes,
                    mode=mode,
                    as_of_date=as_of_date,
                    default_bom_node_ids=[node_id],
                    question_ids_by_node=question_ids_by_node,
                    question_labels_by_node=question_labels_by_node,
                )
            )
    new_documents = _unique_documents(
        document
        for run in runs
        for document in run.get("documents") or []
    )
    content_results = (
        fetch_original_materials(
            feed=feed,
            repository=repository,
            documents=new_documents,
            publication_date_extractor=publication_date_extractor,
        )
        if fetch_originals
        else []
    )
    return {
        "provider": feed.provider_name,
        "knowledge_base_ref": knowledge_base_ref,
        "runs": runs,
        "new_documents": sum(
            run["scan_event"]["discovered_count"] for run in runs
        ),
        "quarantined_documents": sum(
            run["scan_event"]["quarantined_count"] for run in runs
        ),
        "parse_tasks": sum(
            run["scan_event"]["parse_task_count"] for run in runs
        ),
        "content_results": content_results,
    }


def scan_knowledge_base_directory_materials(
    *,
    feed: Any,
    repository: Any,
    knowledge_base_id: str,
    bom_node_id: str,
    relevance_profile: dict[str, Any],
    known_bom_node_ids: Iterable[str],
    mode: str,
    as_of_date: str,
    start_date: str,
    end_date: str,
    discovered_at: str | None = None,
    root_folder_pattern: str = r"^\d{4}年国际顶级投行研报$",
    question_ids_by_node: dict[str, dict[int, str]] | None = None,
    question_labels_by_node: dict[str, dict[int, str]] | None = None,
    fetch_originals: bool = True,
    publication_date_extractor: Any | None = None,
) -> dict[str, Any]:
    """Walk IMA date folders, classify every PDF, and ingest only BOM matches."""

    discovered_at = discovered_at or date.today().isoformat()
    known_nodes = set(str(item) for item in known_bom_node_ids)
    if bom_node_id not in known_nodes:
        raise ValueError(f"Unknown BOM node for directory scan: {bom_node_id}")
    profile_issues = validate_relevance_profile(relevance_profile)
    if profile_issues:
        raise ValueError("; ".join(profile_issues))

    raw_documents = feed.list_dated_materials(
        knowledge_base_id=knowledge_base_id,
        start_date=start_date,
        end_date=end_date,
        root_folder_pattern=root_folder_pattern,
    )
    decisions = [
        classify_bom_material(
            raw,
            bom_node_id=bom_node_id,
            profile=relevance_profile,
            scanned_at=discovered_at,
        )
        for raw in raw_documents
    ]
    reviews = {
        str(row.get("candidate_id") or ""): row
        for row in repository.load_directory_relevance_reviews()
        if str(row.get("candidate_id") or "").strip()
    }
    decisions = [
        _apply_relevance_review(row, reviews.get(str(row["candidate_id"])))
        for row in decisions
    ]
    decisions_by_external_id = {
        str(row["external_id"]): row for row in decisions
    }
    relevant_documents = []
    knowledge_base_ref = _opaque_feed_scope(knowledge_base_id)
    for raw in raw_documents:
        decision = decisions_by_external_id.get(
            str(raw.get("external_id") or "")
        )
        if not decision or decision["relevance_status"] != "relevant":
            continue
        relevant_documents.append(
            {
                **raw,
                "knowledge_base_ref": knowledge_base_ref,
                "relevance_status": decision["relevance_status"],
                "relevance_score": decision["relevance_score"],
                "relevance_reason": decision["relevance_reason"],
            }
        )

    feed_id = f"{knowledge_base_ref}:{bom_node_id}:dated-directory"
    directory_event = {
        "scan_id": _directory_scan_id(
            provider=feed.provider_name,
            feed_id=feed_id,
            scanned_at=discovered_at,
            start_date=start_date,
            end_date=end_date,
            candidates=decisions,
        ),
        "provider": feed.provider_name,
        "feed_id": feed_id,
        "ingestion_channel": "knowledge_base_scan",
        "discovery_mode": "dated_directory",
        "scanned_at": discovered_at,
        "start_date": start_date,
        "end_date": end_date,
        "candidate_count": len(decisions),
        "relevant_count": sum(
            row["relevance_status"] == "relevant" for row in decisions
        ),
        "needs_review_count": sum(
            row["relevance_status"] == "needs_review" for row in decisions
        ),
        "not_relevant_count": sum(
            row["relevance_status"] == "not_relevant" for row in decisions
        ),
    }
    ingestion = ingest_material_batch(
        repository=repository,
        raw_documents=relevant_documents,
        provider=feed.provider_name,
        feed_id=feed_id,
        ingestion_channel="knowledge_base_scan",
        discovered_at=discovered_at,
        known_bom_node_ids=known_nodes,
        mode=mode,
        as_of_date=as_of_date,
        default_bom_node_ids=[bom_node_id],
        question_ids_by_node=question_ids_by_node,
        question_labels_by_node=question_labels_by_node,
    )
    relevant_external_ids = [
        str(row.get("external_id") or "")
        for row in relevant_documents
        if str(row.get("external_id") or "").strip()
    ]
    documents = _unique_documents(
        repository.load_material_documents(
            provider=feed.provider_name,
            external_ids=relevant_external_ids,
        )
    )
    source_ids_by_external_id = {
        str(row.get("external_id") or ""): str(row.get("source_id") or "")
        for row in documents
    }
    decisions = [
        {
            **row,
            "source_id": (
                source_ids_by_external_id.get(str(row["external_id"]))
                or row.get("source_id")
                or ""
            ),
        }
        for row in decisions
    ]
    repository.persist_directory_scan(
        candidates=decisions,
        scan_event=directory_event,
    )
    content_results = (
        fetch_original_materials(
            feed=feed,
            repository=repository,
            documents=documents,
            publication_date_extractor=publication_date_extractor,
        )
        if fetch_originals
        else []
    )
    return {
        "provider": feed.provider_name,
        "knowledge_base_ref": knowledge_base_ref,
        "directory_scan": directory_event,
        "ingestion": ingestion,
        "candidates": decisions,
        "new_documents": ingestion["scan_event"]["discovered_count"],
        "quarantined_documents": ingestion["scan_event"]["quarantined_count"],
        "parse_tasks": ingestion["scan_event"]["parse_task_count"],
        "content_results": content_results,
    }


def fetch_original_materials(
    *,
    feed: Any,
    repository: Any,
    documents: Iterable[dict[str, Any]],
    publication_date_extractor: Any | None = None,
) -> list[dict[str, Any]]:
    """Fetch IMA originals without persisting signed provider URLs."""

    results: list[dict[str, Any]] = []
    for document in documents:
        source_id = str(document.get("source_id") or "")
        external_id = str(document.get("external_id") or "")
        existing_path = repository.canonicalize_material_content(document)
        if existing_path:
            extraction = _extract_publication_date(
                repository=repository,
                document=document,
                content=repository.read_material_content(existing_path),
                extractor=publication_date_extractor,
            )
            results.append(
                {
                    "source_id": source_id,
                    "status": "available",
                    "local_content_path": (
                        extraction.get("local_content_path") or existing_path
                    ),
                    "reused_existing": True,
                    **_public_date_result(extraction),
                }
            )
            continue
        try:
            payload = feed.fetch_media_content(
                media_id=external_id,
                title=str(document.get("title") or ""),
            )
            relative_path = repository.persist_material_content(
                document=document,
                content=payload["content"],
                filename=str(payload.get("filename") or "material.bin"),
                content_type=str(
                    payload.get("content_type") or "application/octet-stream"
                ),
            )
            extraction = _extract_publication_date(
                repository=repository,
                document=document,
                content=payload["content"],
                extractor=publication_date_extractor,
            )
            results.append(
                {
                    "source_id": source_id,
                    "status": "available",
                    "local_content_path": (
                        extraction.get("local_content_path") or relative_path
                    ),
                    **_public_date_result(extraction),
                }
            )
        except (OSError, ValueError) as exc:
            results.append(
                {
                    "source_id": source_id,
                    "status": "unavailable",
                    "reason": str(exc),
                }
            )
    return results


def _extract_publication_date(
    *,
    repository: Any,
    document: dict[str, Any],
    content: bytes,
    extractor: Any | None,
) -> dict[str, Any]:
    if extractor is None:
        return {}
    extraction = extractor.extract(
        content=content,
        title=str(document.get("title") or ""),
    )
    if extraction.get("publication_date_status") == "verified":
        final_path = repository.update_publication_date(
            source_id=str(document.get("source_id") or ""),
            published_at=str(extraction.get("published_at") or ""),
            publication_date_status="verified",
            publication_date_source=str(
                extraction.get("publication_date_source") or "pdf_cover"
            ),
            publication_date_locator=str(
                extraction.get("publication_date_locator") or ""
            ),
        )
        return {**extraction, "local_content_path": final_path}

    current_date = str(document.get("published_at") or "").strip()
    current_status = str(
        document.get("publication_date_status") or ""
    ).strip()
    if current_date and current_status == "inferred_from_title":
        final_path = repository.canonicalize_material_content(document)
        return {
            "published_at": current_date,
            "publication_date_status": current_status,
            "publication_date_source": str(
                document.get("publication_date_source") or "title_suffix"
            ),
            "publication_date_locator": str(
                extraction.get("publication_date_locator") or ""
            ),
            "local_content_path": final_path,
        }

    repository.update_publication_date(
        source_id=str(document.get("source_id") or ""),
        published_at="",
        publication_date_status="needs_pdf_verification",
        publication_date_source="unknown",
        publication_date_locator=str(
            extraction.get("publication_date_locator") or ""
        ),
    )
    return extraction


def _public_date_result(extraction: dict[str, Any]) -> dict[str, Any]:
    return {
        key: extraction[key]
        for key in (
            "published_at",
            "publication_date_status",
            "publication_date_source",
            "publication_date_locator",
        )
        if key in extraction
    }


def ingest_question_search_result(
    *,
    search_result: dict[str, Any],
    repository: Any,
    provider: str,
    bom_node_id: str,
    question_number: int,
    known_bom_node_ids: Iterable[str],
    mode: str,
    as_of_date: str,
    discovered_at: str | None = None,
    question_ids_by_node: dict[str, dict[int, str]] | None = None,
    question_labels_by_node: dict[str, dict[int, str]] | None = None,
    leaf_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Route one Exa/AI-search result through the same material contract."""

    discovered_at = discovered_at or date.today().isoformat()
    return ingest_material_batch(
        repository=repository,
        raw_documents=search_result.get("sources") or [],
        provider=provider,
        feed_id=(
            f"{bom_node_id}:q{question_number}:"
            f"{(leaf_context or {}).get('question_node_id') or (leaf_context or {}).get('leaf_question_id')}"
            if leaf_context
            else f"{bom_node_id}:q{question_number}"
        ),
        ingestion_channel="question_search",
        discovered_at=discovered_at,
        known_bom_node_ids=known_bom_node_ids,
        mode=mode,
        as_of_date=as_of_date,
        default_bom_node_ids=[bom_node_id],
        default_question_numbers=[question_number],
        question_ids_by_node=question_ids_by_node,
        question_labels_by_node=question_labels_by_node,
        leaf_context=leaf_context,
    )


def _scan_id(
    provider: str,
    feed_id: str,
    scanned_at: str,
    documents: list[dict[str, Any]],
) -> str:
    identities = ",".join(
        sorted(str(document.get("external_id") or "") for document in documents)
    )
    digest = hashlib.sha256(
        f"{provider}|{feed_id}|{scanned_at}|{identities}".encode("utf-8")
    ).hexdigest()[:16]
    return f"SCAN-{provider.upper()}-{digest.upper()}"


def _directory_scan_id(
    *,
    provider: str,
    feed_id: str,
    scanned_at: str,
    start_date: str,
    end_date: str,
    candidates: list[dict[str, Any]],
) -> str:
    identities = ",".join(
        sorted(str(row.get("external_id") or "") for row in candidates)
    )
    digest = hashlib.sha256(
        (
            f"{provider}|{feed_id}|{scanned_at}|{start_date}|"
            f"{end_date}|{identities}"
        ).encode("utf-8")
    ).hexdigest()[:16]
    return f"DIRSCAN-{provider.upper()}-{digest.upper()}"


def _apply_relevance_review(
    decision: dict[str, Any],
    review: dict[str, Any] | None,
) -> dict[str, Any]:
    if not review:
        return decision
    status = str(review.get("relevance_status") or "")
    if status not in {"relevant", "not_relevant"}:
        raise ValueError(
            "Relevance reviews must set relevant or not_relevant"
        )
    return {
        **decision,
        "relevance_status": status,
        "relevance_reason": str(
            review.get("review_reason")
            or review.get("relevance_reason")
            or "GPT reviewed directory candidate"
        ),
        "review_status": "gpt_reviewed",
        "reviewed_at": str(review.get("reviewed_at") or ""),
    }


def _opaque_feed_scope(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"ref:{digest}"


def _unique_documents(
    documents: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for document in documents:
        source_id = str(document.get("source_id") or "")
        if source_id:
            rows[source_id] = document
    return [rows[source_id] for source_id in sorted(rows)]
