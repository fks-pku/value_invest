from __future__ import annotations

from typing import Any

from value_invest_research.domain.leaf_research_tasks import INFO_CATEGORIES, is_leaf_node


def synthesize_leaf_answer_from_result(row: dict[str, Any]) -> dict[str, Any]:
    """Turn one normalized leaf result into a leaf answer override row."""
    sources = row.get("sources", [])
    source_balance = source_balance_text(sources)
    strengthening_sources = [source for source in sources if source.get("reliability") != "low"]
    low_reliability_sources = [source for source in sources if source.get("reliability") == "low"]
    supporting = list(row.get("supporting_evidence", [])) if strengthening_sources else []
    supporting.extend(source_support_lines(strengthening_sources))
    leads = list(row.get("research_leads", []))
    leads.extend(source_support_lines(low_reliability_sources))
    return {
        "schema_version": "1.0",
        "source": "leaf_research",
        "synthesis_source": "leaf_research",
        "node_id": row.get("node_id", ""),
        "answer": row.get("answer", ""),
        "facts": _text_list(row.get("facts")),
        "inferences": _text_list(row.get("inferences")),
        "judgment": row.get("judgment", ""),
        "gaps": _text_list(row.get("gaps")),
        "next_data": _text_list(row.get("gaps")),
        "confidence": row.get("confidence", "unknown"),
        "source_balance": source_balance,
        "supporting_evidence": supporting,
        "refuting_evidence": _text_list(row.get("refuting_evidence")),
        "research_leads": leads,
        "rollup": f"{row.get('query', '')}：{row.get('judgment') or row.get('answer', '')}",
        "provider": row.get("provider", ""),
        "provider_model": row.get("provider_model", ""),
        "task_id": row.get("task_id", ""),
        "source_index": sources,
        "source_urls": [source.get("url", "") for source in sources if source.get("url")],
    }


def synthesize_latest_leaf_answers(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep the latest row per node and synthesize answer override rows."""
    latest_by_node: dict[str, dict[str, Any]] = {}
    for row in results:
        latest_by_node[row.get("node_id", "")] = row
    return [synthesize_leaf_answer_from_result(row) for row in latest_by_node.values() if row.get("node_id")]


def build_rollup_answer_rows(qa_tree: dict[str, Any]) -> list[dict[str, Any]]:
    """Build parent rollup rows from QA nodes already enriched by leaf answers."""
    rows = []
    for node in qa_tree.get("nodes", []):
        rollup_sources = node.get("metadata", {}).get("rollup_sources", [])
        if is_leaf_node(qa_tree, node) or not rollup_sources:
            continue
        professional = node.get("professional_answer", {})
        rows.append(
            {
                "schema_version": "1.0",
                "source": "leaf_research_rollup",
                "node_id": node.get("id", ""),
                "parent_id": node.get("parent_id", ""),
                "level": node.get("level", 0),
                "section_id": node.get("section_id", ""),
                "question": node.get("question", ""),
                "answer": professional.get("answer") or node.get("current_answer", ""),
                "facts": _text_list(professional.get("facts")),
                "inferences": _text_list(professional.get("inferences")),
                "judgment": professional.get("judgment", ""),
                "gaps": _text_list(professional.get("gaps")),
                "confidence": professional.get("confidence", "unknown"),
                "source_balance": professional.get("source_balance", ""),
                "supporting_evidence": _text_list(professional.get("supporting_evidence")),
                "refuting_evidence": _text_list(professional.get("refuting_evidence")),
                "research_leads": _text_list(professional.get("research_leads")),
                "rollup": professional.get("rollup", ""),
                "rollup_sources": rollup_sources,
            }
        )
    return rows


def source_support_lines(sources: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for source in sources:
        title = source.get("title") or source.get("url") or "source"
        summary = source.get("summary", "")
        lines.append(f"{title}：{summary}".strip("："))
    return lines


def source_balance_text(sources: list[dict[str, Any]]) -> str:
    counts = {category: 0 for category in INFO_CATEGORIES}
    for source in sources:
        category = source.get("information_category", "")
        if category in counts:
            counts[category] += 1
    return f"证据 {counts['evidence']} / 研报 {counts['research_report']} / 消息 {counts['message']} / 观点 {counts['opinion']}"


def _text_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []
