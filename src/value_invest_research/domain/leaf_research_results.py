from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any


INFO_CATEGORIES = ["evidence", "research_report", "message", "opinion"]


def normalize_provider_result(row: dict[str, Any]) -> dict[str, Any]:
    """Normalize provider output into the leaf research result contract."""
    executed_at = row.get("executed_at") or _now_iso()
    sources = [_normalize_source(source, executed_at) for source in row.get("sources", [])]
    normalized = {
        "schema_version": "1.0",
        "provider": row.get("provider", "manual"),
        "provider_model": row.get("provider_model", ""),
        "task_id": row.get("task_id", ""),
        "research_step_id": row.get("research_step_id") or f"step:{row.get('node_id', '')}",
        "node_id": row.get("node_id", ""),
        "query": row.get("query", ""),
        "executed_at": executed_at,
        "raw_response_path": row.get("raw_response_path", ""),
        "sources": sources,
        "answer": row.get("answer", ""),
        "facts": _text_list(row.get("facts")),
        "inferences": _text_list(row.get("inferences")),
        "judgment": row.get("judgment", ""),
        "supporting_evidence": _text_list(row.get("supporting_evidence")),
        "refuting_evidence": _text_list(row.get("refuting_evidence")),
        "research_leads": _text_list(row.get("research_leads")),
        "gaps": _text_list(row.get("gaps")),
        "confidence": row.get("confidence", "unknown"),
        "materiality": row.get("materiality", ""),
        "source_plan": row.get("source_plan", []),
        "extraction_schema": row.get("extraction_schema", {}),
        "task_family": row.get("task_family", ""),
        "selected_skill": row.get("selected_skill", ""),
        "skill_dispatch_trace": row.get("skill_dispatch_trace", {}),
    }
    if not normalized["node_id"]:
        raise ValueError("leaf research result missing node_id")
    if not sources:
        raise ValueError(f"leaf research result for {normalized['node_id']} has no sources")
    return normalized


def deduplicate_leaf_sources(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deduplicate source records while preserving node and task bindings."""
    by_key: dict[str, dict[str, Any]] = {}
    for row in rows:
        for source in row.get("sources", []):
            key = _source_key(source)
            existing = by_key.get(key)
            if existing is None:
                existing = {
                    **source,
                    "source_id": _stable_source_id(key),
                    "node_ids": [],
                    "task_ids": [],
                    "result_count": 0,
                }
                by_key[key] = existing
            node_id = row.get("node_id", "")
            task_id = row.get("task_id", "")
            if node_id and node_id not in existing["node_ids"]:
                existing["node_ids"].append(node_id)
            if task_id and task_id not in existing["task_ids"]:
                existing["task_ids"].append(task_id)
            existing["result_count"] += 1
    return sorted(by_key.values(), key=lambda item: (item.get("url", ""), item.get("title", "")))


def merge_leaf_result_rows(
    existing_rows: list[dict[str, Any]],
    new_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Merge leaf result rows by stable task or node/provider/query key."""
    merged = list(existing_rows)
    index_by_key = {_leaf_result_key(row): index for index, row in enumerate(merged)}
    for row in new_rows:
        key = _leaf_result_key(row)
        if key in index_by_key:
            merged[index_by_key[key]] = row
            continue
        index_by_key[key] = len(merged)
        merged.append(row)
    return merged


def _normalize_source(source: dict[str, Any], accessed_at: str) -> dict[str, Any]:
    category = source.get("information_category") or _infer_information_category(source)
    normalized = {
        "url": source.get("url", ""),
        "title": source.get("title", "") or source.get("source_name", ""),
        "publisher": source.get("publisher", ""),
        "author": source.get("author", ""),
        "published_at": source.get("published_at", ""),
        "accessed_at": source.get("accessed_at") or accessed_at,
        "source_type": source.get("source_type", category),
        "information_category": category,
        "reliability": source.get("reliability", _default_reliability(category)),
        "materiality": source.get("materiality", "medium"),
        "summary": source.get("summary", ""),
        "quoted_or_extracted_points": _text_list(source.get("quoted_or_extracted_points")),
    }
    normalized["source_id"] = source.get("source_id") or _stable_source_id(_source_key(normalized))
    return normalized


def _infer_information_category(source: dict[str, Any]) -> str:
    source_type = str(source.get("source_type", "")).lower()
    if source_type in INFO_CATEGORIES:
        return source_type
    if any(token in source_type for token in ["annual", "10-k", "filing", "press", "ir", "regulatory"]):
        return "evidence"
    if any(token in source_type for token in ["report", "research", "database"]):
        return "research_report"
    if any(token in source_type for token in ["news", "media", "message"]):
        return "message"
    if any(token in source_type for token in ["opinion", "expert", "interview"]):
        return "opinion"
    return "research_report"


def _default_reliability(category: str) -> str:
    return {
        "evidence": "primary",
        "research_report": "high",
        "message": "low",
        "opinion": "medium",
    }.get(category, "medium")


def _source_key(source: dict[str, Any]) -> str:
    url = str(source.get("url", "")).strip().lower()
    if url:
        return f"url:{url}"
    return f"title:{source.get('title', '').strip().lower()}:{source.get('publisher', '').strip().lower()}"


def _leaf_result_key(row: dict[str, Any]) -> str:
    task_id = str(row.get("task_id", "")).strip()
    if task_id:
        return f"task:{task_id}"
    return "|".join(
        [
            "node",
            str(row.get("node_id", "")).strip(),
            str(row.get("provider", "")).strip(),
            str(row.get("query", "")).strip(),
        ]
    )


def _stable_source_id(key: str) -> str:
    return f"leaf_source_{hashlib.sha256(key.encode('utf-8')).hexdigest()[:12]}"


def _text_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
