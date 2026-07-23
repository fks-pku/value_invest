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
) -> dict[str, Any]:
    """Normalize, deduplicate, route, and queue one material batch."""

    known_nodes = set(str(item) for item in known_bom_node_ids)
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

    parse_tasks = [
        task
        for document in documents
        for task in build_material_parse_tasks(
            document,
            question_ids_by_node=question_ids_by_node,
        )
    ]
    scan_event = {
        "scan_id": _scan_id(provider, feed_id, discovered_at, documents),
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
    }
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
                )
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
) -> dict[str, Any]:
    """Route one Exa/AI-search result through the same material contract."""

    discovered_at = discovered_at or date.today().isoformat()
    return ingest_material_batch(
        repository=repository,
        raw_documents=search_result.get("sources") or [],
        provider=provider,
        feed_id=f"{bom_node_id}:q{question_number}",
        ingestion_channel="question_search",
        discovered_at=discovered_at,
        known_bom_node_ids=known_bom_node_ids,
        mode=mode,
        as_of_date=as_of_date,
        default_bom_node_ids=[bom_node_id],
        default_question_numbers=[question_number],
        question_ids_by_node=question_ids_by_node,
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


def _opaque_feed_scope(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"ref:{digest}"
