from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SOURCE_CATEGORY_ORDER = ["evidence", "research_report", "message", "opinion"]
SOURCE_CATEGORY_LABELS = {
    "evidence": "证据",
    "research_report": "研报",
    "message": "消息",
    "opinion": "观点",
}
SYNTHESIS_TASK_FILE = "synthesis_tasks.jsonl"
SYNTHESIS_OVERRIDE_FILE = "synthesis_overrides.jsonl"

EXPECTED_SYNTHESIS_FIELDS = [
    "node_id",
    "answer",
    "facts",
    "inferences",
    "judgment",
    "gaps",
    "next_data",
    "confidence",
    "source_balance",
    "supporting_evidence",
    "refuting_evidence",
    "research_leads",
    "rollup",
]


def build_stock_synthesis_tasks(
    root: Path,
    ticker: str,
    leaf_only: bool = True,
    limit: int | None = None,
) -> dict[str, Any]:
    """Export answer-synthesis tasks for stock QA nodes."""
    from value_invest_research.research_system import build_research_system, normalize_ticker

    normalized = normalize_ticker(ticker)
    build_result = build_research_system(root, normalized)
    research_dir = Path(build_result["qa_tree_path"]).parent
    qa_tree = _read_json(research_dir / "qa_tree.json")
    tasks = _synthesis_tasks_from_tree(
        qa_tree,
        object_type="stock",
        object_id=normalized,
        leaf_only=leaf_only,
        limit=limit,
    )
    task_path = research_dir / SYNTHESIS_TASK_FILE
    _write_jsonl(task_path, tasks)
    return {
        **build_result,
        "synthesis_task_path": str(task_path),
        "synthesis_tasks": len(tasks),
        "leaf_only": leaf_only,
    }


def build_meta_qa_synthesis_tasks(
    root: Path,
    project_id: str,
    leaf_only: bool = True,
    limit: int | None = None,
) -> dict[str, Any]:
    """Export answer-synthesis tasks for generic meta QA nodes."""
    from value_invest_research.meta_qa_research import _rebuild_meta_qa_project

    rebuild_result = _rebuild_meta_qa_project(root, project_id)
    project_dir = Path(rebuild_result["project_dir"])
    qa_tree = _read_json(project_dir / "qa_tree.json")
    tasks = _synthesis_tasks_from_tree(
        qa_tree,
        object_type="meta_qa",
        object_id=project_id,
        leaf_only=leaf_only,
        limit=limit,
    )
    task_path = project_dir / SYNTHESIS_TASK_FILE
    _write_jsonl(task_path, tasks)
    return {
        **rebuild_result,
        "synthesis_task_path": str(task_path),
        "synthesis_tasks": len(tasks),
        "leaf_only": leaf_only,
    }


def import_stock_answer_synthesis(root: Path, ticker: str, path: Path) -> dict[str, Any]:
    """Import synthesized stock QA answers and rebuild the generated report."""
    from value_invest_research.research_system import build_research_system, normalize_ticker

    normalized = normalize_ticker(ticker)
    build_result = build_research_system(root, normalized)
    research_dir = Path(build_result["qa_tree_path"]).parent
    qa_tree = _read_json(research_dir / "qa_tree.json")
    overrides = _normalize_import_rows(path)
    _validate_override_node_ids(qa_tree, overrides, path)
    override_path = research_dir / SYNTHESIS_OVERRIDE_FILE
    _append_jsonl(override_path, overrides)
    refreshed = build_research_system(root, normalized)
    return {
        **refreshed,
        "ticker": normalized,
        "input_path": str(path),
        "synthesis_override_path": str(override_path),
        "records": len(overrides),
        "applied_nodes": len({row["node_id"] for row in overrides}),
    }


def import_meta_qa_answer_synthesis(root: Path, project_id: str, path: Path) -> dict[str, Any]:
    """Import synthesized meta QA answers and rebuild the generated report."""
    from value_invest_research.meta_qa_research import _rebuild_meta_qa_project

    rebuild_result = _rebuild_meta_qa_project(root, project_id)
    project_dir = Path(rebuild_result["project_dir"])
    qa_tree = _read_json(project_dir / "qa_tree.json")
    overrides = _normalize_import_rows(path)
    _validate_override_node_ids(qa_tree, overrides, path)
    override_path = project_dir / SYNTHESIS_OVERRIDE_FILE
    _append_jsonl(override_path, overrides)
    refreshed = _rebuild_meta_qa_project(root, project_id)
    return {
        **refreshed,
        "input_path": str(path),
        "synthesis_override_path": str(override_path),
        "records": len(overrides),
        "applied_nodes": len({row["node_id"] for row in overrides}),
    }


def run_stock_answer_synthesis(
    root: Path,
    ticker: str,
    leaf_only: bool = True,
    limit: int | None = None,
    apply: bool = True,
    client: Any | None = None,
) -> dict[str, Any]:
    """Generate professional stock QA answers from synthesis tasks."""
    build_result = build_stock_synthesis_tasks(root, ticker, leaf_only=leaf_only, limit=limit)
    research_dir = Path(build_result["synthesis_task_path"]).parent
    tasks = _read_jsonl(research_dir / SYNTHESIS_TASK_FILE)
    rows = [_synthesize_answer(task, client) for task in tasks]
    answer_path = research_dir / "synthesized_answers.jsonl"
    _write_jsonl(answer_path, rows)
    result = {
        **build_result,
        "synthesized_answer_path": str(answer_path),
        "synthesized_answers": len(rows),
        "synthesis_mode": "llm" if client is not None else "deterministic",
        "applied": False,
        "applied_nodes": 0,
    }
    if apply and rows:
        import_result = import_stock_answer_synthesis(root, build_result["ticker"], answer_path)
        result.update(import_result)
        result["synthesized_answer_path"] = str(answer_path)
        result["synthesized_answers"] = len(rows)
        result["synthesis_mode"] = "llm" if client is not None else "deterministic"
        result["applied"] = True
    return result


def run_meta_qa_answer_synthesis(
    root: Path,
    project_id: str,
    leaf_only: bool = True,
    limit: int | None = None,
    apply: bool = True,
    client: Any | None = None,
) -> dict[str, Any]:
    """Generate professional generic QA answers from synthesis tasks."""
    build_result = build_meta_qa_synthesis_tasks(root, project_id, leaf_only=leaf_only, limit=limit)
    project_dir = Path(build_result["synthesis_task_path"]).parent
    tasks = _read_jsonl(project_dir / SYNTHESIS_TASK_FILE)
    rows = [_synthesize_answer(task, client) for task in tasks]
    answer_path = project_dir / "synthesized_answers.jsonl"
    _write_jsonl(answer_path, rows)
    result = {
        **build_result,
        "synthesized_answer_path": str(answer_path),
        "synthesized_answers": len(rows),
        "synthesis_mode": "llm" if client is not None else "deterministic",
        "applied": False,
        "applied_nodes": 0,
    }
    if apply and rows:
        import_result = import_meta_qa_answer_synthesis(root, project_id, answer_path)
        result.update(import_result)
        result["synthesized_answer_path"] = str(answer_path)
        result["synthesized_answers"] = len(rows)
        result["synthesis_mode"] = "llm" if client is not None else "deterministic"
        result["applied"] = True
    return result


def load_synthesis_overrides(container_dir: Path) -> list[dict[str, Any]]:
    """Load the latest answer override per node from a generated research folder."""
    path = container_dir / SYNTHESIS_OVERRIDE_FILE
    latest: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(_read_jsonl(path), start=1):
        normalized = _normalize_synthesis_row(row, source=f"{path}:{index}", add_imported_at=False)
        latest[normalized["node_id"]] = normalized
    return list(latest.values())


def apply_synthesis_overrides(qa_tree: dict[str, Any], overrides: list[dict[str, Any]]) -> int:
    """Apply professional answer overrides to matching QA nodes."""
    if not overrides:
        return 0
    nodes_by_id = {node.get("id"): node for node in qa_tree.get("nodes", [])}
    applied = 0
    for override in overrides:
        node = nodes_by_id.get(override.get("node_id", ""))
        if not node:
            continue
        _apply_override_to_node(node, override)
        applied += 1
    qa_tree["synthesis_overrides"] = {
        "source": SYNTHESIS_OVERRIDE_FILE,
        "loaded": len(overrides),
        "applied": applied,
    }
    return applied


def _synthesis_tasks_from_tree(
    qa_tree: dict[str, Any],
    object_type: str,
    object_id: str,
    leaf_only: bool,
    limit: int | None,
) -> list[dict[str, Any]]:
    if limit is not None and limit < 0:
        raise ValueError("limit must be non-negative")
    nodes_by_id = {node.get("id"): node for node in qa_tree.get("nodes", [])}
    rows: list[dict[str, Any]] = []
    for node in qa_tree.get("nodes", []):
        if leaf_only and not _is_leaf_node(qa_tree, node):
            continue
        rows.append(_synthesis_task(qa_tree, node, nodes_by_id, object_type, object_id))
        if limit is not None and len(rows) >= limit:
            break
    return rows


def _synthesis_task(
    qa_tree: dict[str, Any],
    node: dict[str, Any],
    nodes_by_id: dict[str, dict[str, Any]],
    object_type: str,
    object_id: str,
) -> dict[str, Any]:
    node_id = node.get("id", "")
    parent = nodes_by_id.get(node.get("parent_id", ""), {})
    synthesis = node.get("synthesis", {})
    source_index = _source_index(node.get("evidence_buckets", {}))
    return {
        "task_id": _task_id(object_type, object_id, node_id),
        "object_type": object_type,
        "object_id": object_id,
        "node_id": node_id,
        "parent_id": node.get("parent_id", ""),
        "level": node.get("level", 0),
        "question": node.get("question", ""),
        "parent_question": parent.get("question", ""),
        "current_answer": node.get("current_answer", ""),
        "current_rollup": node.get("rollup_to_parent", ""),
        "current_synthesis": {
            "facts": synthesis.get("facts", []),
            "inferences": synthesis.get("inferences", []),
            "judgment": synthesis.get("judgment", ""),
            "gaps": synthesis.get("gaps", []),
            "confidence": synthesis.get("confidence", ""),
        },
        "source_index": source_index,
        "source_balance": _source_balance(source_index),
        "expected_output_fields": EXPECTED_SYNTHESIS_FIELDS,
        "output_contract": [
            "只回答当前 node_id 的问题；事实、推论、判断、缺口必须分开。",
            "支撑证据、反证证据、研究线索要引用 source_index 中的 evidence_id 或 source_name。",
            "message 和 opinion 只能作为线索或机制假设，不能单独强化结论。",
            "rollup 字段必须是一句话，说明该节点能向父问题上抛什么结论。",
        ],
        "import_row_template": {
            "node_id": node_id,
            "answer": "",
            "facts": [],
            "inferences": [],
            "judgment": "",
            "gaps": [],
            "next_data": [],
            "confidence": "low",
            "source_balance": "",
            "supporting_evidence": [],
            "refuting_evidence": [],
            "research_leads": [],
            "rollup": "",
        },
        "import_command": _import_command(object_type, object_id),
        "tree_default_depth": qa_tree.get("default_depth", 3),
    }


def _source_index(buckets: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}
    for category in SOURCE_CATEGORY_ORDER:
        items = []
        for item in buckets.get(category, []):
            items.append(
                {
                    "evidence_id": item.get("evidence_id", ""),
                    "relation": item.get("relation", ""),
                    "source_name": item.get("source_name", ""),
                    "url": item.get("url", ""),
                    "point": item.get("point", ""),
                    "summary": item.get("summary", ""),
                    "reliability": item.get("reliability", ""),
                    "materiality": item.get("materiality", ""),
                }
            )
        index[category] = items
    return index


def _source_balance(source_index: dict[str, list[dict[str, Any]]]) -> str:
    category_counts = " / ".join(
        f"{SOURCE_CATEGORY_LABELS[category]} {len(source_index.get(category, []))}"
        for category in SOURCE_CATEGORY_ORDER
    )
    support = refute = lead = 0
    for items in source_index.values():
        for item in items:
            relation = str(item.get("relation", ""))
            if "反证" in relation or "削弱" in relation:
                refute += 1
            elif "线索" in relation or "待验证" in relation:
                lead += 1
            else:
                support += 1
    return f"{category_counts}；关系结构 {support} 支撑 / {refute} 反证 / {lead} 线索。"


def _synthesize_answer(task: dict[str, Any], client: Any | None) -> dict[str, Any]:
    if client is None:
        return _draft_synthesis_from_task(task)
    return _llm_synthesis_from_task(task, client)


def _llm_synthesis_from_task(task: dict[str, Any], client: Any) -> dict[str, Any]:
    fallback = _draft_synthesis_from_task(task)
    response_text = client.chat(_llm_system_prompt(), _llm_user_prompt(task))
    parsed = _extract_json_object(response_text)
    if not parsed:
        return {**fallback, "synthesis_source": "llm_invalid_fallback"}
    row = {
        **fallback,
        **parsed,
        "node_id": task.get("node_id", ""),
        "synthesis_source": parsed.get("synthesis_source") or "llm",
    }
    try:
        return _normalize_synthesis_row(row, source=f"llm:{task.get('node_id', '')}", add_imported_at=False)
    except ValueError:
        return {**fallback, "synthesis_source": "llm_invalid_fallback"}


def _llm_system_prompt() -> str:
    return (
        "你是专业二级市场投研分析师，负责在层级 QA 系统中回答单个研究问题。"
        "必须严格区分事实、推论、判断、缺口；不得给出买卖建议；"
        "所有重要事实必须引用给定 source_index 中的 evidence_id 或 source_name。"
    )


def _llm_user_prompt(task: dict[str, Any]) -> str:
    compact_task = {
        "node_id": task.get("node_id", ""),
        "question": task.get("question", ""),
        "parent_question": task.get("parent_question", ""),
        "current_answer": task.get("current_answer", ""),
        "current_synthesis": task.get("current_synthesis", {}),
        "source_balance": task.get("source_balance", ""),
        "source_index": task.get("source_index", {}),
    }
    return "\n".join(
        [
            "请基于以下 QA 节点任务，输出一个 JSON 对象，不要输出 Markdown。",
            "",
            json.dumps(compact_task, ensure_ascii=False, indent=2, sort_keys=True),
            "",
            "输出字段必须是：",
            json.dumps(EXPECTED_SYNTHESIS_FIELDS, ensure_ascii=False),
            "",
            "写作要求：",
            "- answer 用中文写成专业投研回答，说明当前判断、证据支撑、反证约束、下一步验证。",
            "- facts 是可核验事实列表，必须带 evidence_id 或 source_name。",
            "- inferences 是由事实推出的机制或边界，不要把观点写成事实。",
            "- judgment 是一句当前判断，必须体现置信度约束。",
            "- gaps 是还缺什么信息，next_data 是下一步要收集的具体数据。",
            "- supporting_evidence/refuting_evidence/research_leads 分别引用对应来源。",
            "- message 和 opinion 只能作为线索，不能单独强化结论。",
            "- confidence 只能是 low、medium 或 high。",
            "- rollup 是一句能上抛给父问题的结论。",
        ]
    )


def _extract_json_object(text: str) -> dict[str, Any]:
    candidates = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    candidates.append(text.strip())
    brace_match = re.search(r"(\{.*\})", text, flags=re.DOTALL)
    if brace_match:
        candidates.append(brace_match.group(1))
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return {}


def _draft_synthesis_from_task(task: dict[str, Any]) -> dict[str, Any]:
    source_index = task.get("source_index", {})
    facts = _fact_lines(source_index) or _text_list(task.get("current_synthesis", {}).get("facts"))
    supporting = _relation_lines(source_index, "support")
    refuting = _relation_lines(source_index, "refute")
    leads = _relation_lines(source_index, "lead")
    counts = {category: len(source_index.get(category, [])) for category in SOURCE_CATEGORY_ORDER}
    confidence = _confidence_from_counts(counts, refuting)
    question = _clean_str(task.get("question"))
    judgment = _draft_judgment(question, counts, refuting, confidence)
    gaps = _draft_gaps(task, counts, refuting)
    next_data = _draft_next_data(question, gaps, counts)
    inferences = _draft_inferences(counts, supporting, refuting, leads)
    answer = _draft_answer(question, judgment, supporting, refuting, leads, next_data, confidence)
    return {
        "node_id": task.get("node_id", ""),
        "answer": answer,
        "facts": facts[:6],
        "inferences": inferences,
        "judgment": judgment,
        "gaps": gaps,
        "next_data": next_data,
        "confidence": confidence,
        "source_balance": task.get("source_balance", ""),
        "supporting_evidence": supporting[:5],
        "refuting_evidence": refuting[:5],
        "research_leads": leads[:5],
        "rollup": f"{question}：{judgment}",
        "synthesis_source": "deterministic_batch_synthesis",
    }


def _fact_lines(source_index: dict[str, list[dict[str, Any]]]) -> list[str]:
    lines: list[str] = []
    for category in SOURCE_CATEGORY_ORDER:
        for item in source_index.get(category, []):
            evidence_id = item.get("evidence_id", "")
            point = item.get("point") or item.get("summary") or item.get("source_name", "")
            if not point:
                continue
            prefix = SOURCE_CATEGORY_LABELS.get(category, category)
            line = f"{prefix}：{_truncate(point, 120)}"
            if evidence_id:
                line = f"{line} [{evidence_id}]"
            if line not in lines:
                lines.append(line)
    return lines


def _relation_lines(source_index: dict[str, list[dict[str, Any]]], relation_type: str) -> list[str]:
    lines: list[str] = []
    for category in SOURCE_CATEGORY_ORDER:
        for item in source_index.get(category, []):
            stance = _item_stance(category, item)
            if stance != relation_type:
                continue
            source_name = item.get("source_name") or item.get("evidence_id") or SOURCE_CATEGORY_LABELS.get(category, category)
            point = item.get("point") or item.get("summary") or ""
            evidence_id = item.get("evidence_id", "")
            line = f"{source_name}：{_truncate(point, 110)}"
            if evidence_id:
                line = f"{line} [{evidence_id}]"
            if line not in lines:
                lines.append(line)
    return lines


def _item_stance(category: str, item: dict[str, Any]) -> str:
    relation = str(item.get("relation", ""))
    if "反证" in relation or "削弱" in relation:
        return "refute"
    if category in {"message", "opinion"} or "线索" in relation or "待验证" in relation:
        return "lead"
    return "support"


def _confidence_from_counts(counts: dict[str, int], refuting: list[str]) -> str:
    verified = counts.get("evidence", 0) + counts.get("research_report", 0)
    if verified >= 3 and counts.get("evidence", 0) > 0 and counts.get("research_report", 0) > 0 and not refuting:
        return "high"
    if verified > 0:
        return "medium"
    return "low"


def _draft_judgment(question: str, counts: dict[str, int], refuting: list[str], confidence: str) -> str:
    verified = counts.get("evidence", 0) + counts.get("research_report", 0)
    if not verified:
        return "当前只能形成研究假设，尚不能输出强判断。"
    if refuting:
        return "当前可形成受约束判断，但反证信息要求继续验证边界条件。"
    if confidence == "high":
        return "当前信息足以形成较强的阶段性判断，但仍需跟踪后续更新触发器。"
    return "当前可形成初步判断，结论强度取决于后续一手证据和高可靠研报补充。"


def _draft_gaps(task: dict[str, Any], counts: dict[str, int], refuting: list[str]) -> list[str]:
    existing = _text_list(task.get("current_synthesis", {}).get("gaps"))
    gaps: list[str] = []
    for gap in existing:
        _append_unique(gaps, gap)
    for category in SOURCE_CATEGORY_ORDER:
        if counts.get(category, 0) == 0:
            _append_unique(gaps, f"缺少{SOURCE_CATEGORY_LABELS[category]}类信息，当前结论不能完整闭环。")
    if refuting:
        _append_unique(gaps, "需要量化反证信息对结论的影响阈值和触发条件。")
    if not gaps:
        _append_unique(gaps, "需要继续跟踪后续报告期、经营数据和反证触发器。")
    return gaps[:5]


def _draft_next_data(question: str, gaps: list[str], counts: dict[str, int]) -> list[str]:
    next_data: list[str] = []
    if counts.get("evidence", 0) == 0:
        _append_unique(next_data, f"围绕“{question}”补充公司公告、财报、监管文件或官方数据。")
    if counts.get("research_report", 0) == 0:
        _append_unique(next_data, f"补充覆盖“{question}”的卖方深度、行业专题或第三方数据库。")
    for gap in gaps:
        _append_unique(next_data, _gap_to_next_data(gap))
    return next_data[:4]


def _draft_inferences(
    counts: dict[str, int],
    supporting: list[str],
    refuting: list[str],
    leads: list[str],
) -> list[str]:
    inferences: list[str] = []
    if supporting:
        _append_unique(inferences, "证据和研报可作为结论主支撑，但需要检查口径、时间范围和是否能直接回答问题。")
    if refuting:
        _append_unique(inferences, "反证信息会降低结论强度，应优先定义可量化的证伪阈值。")
    if leads:
        _append_unique(inferences, "消息和观点只作为研究线索，需要回到一手证据或高可靠研报确认。")
    if not inferences:
        _append_unique(inferences, "当前信息覆盖不足，不能把问题答案写成确定结论。")
    missing = [SOURCE_CATEGORY_LABELS[category] for category in SOURCE_CATEGORY_ORDER if counts.get(category, 0) == 0]
    if missing:
        _append_unique(inferences, f"信息结构缺口集中在：{'、'.join(missing)}。")
    return inferences[:4]


def _draft_answer(
    question: str,
    judgment: str,
    supporting: list[str],
    refuting: list[str],
    leads: list[str],
    next_data: list[str],
    confidence: str,
) -> str:
    support_text = _truncate(supporting[0], 150) if supporting else "尚未找到足够的一手证据或高可靠研报作为主支撑"
    refute_text = _truncate(refuting[0], 130) if refuting else "暂未形成明确反证，但不能因此视为已证实"
    lead_text = _truncate(leads[0], 130) if leads else "消息和观点线索不足"
    next_text = _truncate(next_data[0], 130) if next_data else "继续跟踪下一报告期和关键经营数据"
    return (
        f"专业回答：围绕“{question}”，{judgment}"
        f"主要支撑来自：{support_text}。"
        f"主要约束是：{refute_text}；{lead_text}。"
        f"下一步应优先验证：{next_text}。"
        f"当前置信度为{_confidence_label(confidence)}。"
    )


def _confidence_label(confidence: str) -> str:
    return {"high": "高", "medium": "中", "low": "低"}.get(confidence, "中")


def _append_unique(values: list[str], text: str) -> None:
    text = text.strip()
    if text and text not in values:
        values.append(text)


def _truncate(text: Any, limit: int) -> str:
    cleaned = _clean_str(text)
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[: max(0, limit - 1)]}…"


def _normalize_import_rows(path: Path) -> list[dict[str, Any]]:
    rows = []
    for index, row in enumerate(_read_jsonl(path), start=1):
        rows.append(_normalize_synthesis_row(row, source=f"{path}:{index}", add_imported_at=True))
    if not rows:
        raise ValueError(f"{path}: no synthesis rows found")
    return rows


def _normalize_synthesis_row(row: dict[str, Any], source: str, add_imported_at: bool) -> dict[str, Any]:
    if not isinstance(row, dict):
        raise ValueError(f"{source}: synthesis row must be an object")
    node_id = _clean_str(row.get("node_id"))
    answer = _clean_str(row.get("answer") or row.get("current_answer"))
    if not node_id:
        raise ValueError(f"{source}: node_id is required")
    if not answer:
        raise ValueError(f"{source}: answer is required")
    gaps = _text_list(row.get("gaps"))
    normalized = {
        "node_id": node_id,
        "answer": answer,
        "facts": _text_list(row.get("facts")),
        "inferences": _text_list(row.get("inferences")),
        "judgment": _clean_str(row.get("judgment")) or answer,
        "gaps": gaps or ["需要继续验证该节点的关键事实、反证条件和更新触发器。"],
        "next_data": _text_list(row.get("next_data")) or [_gap_to_next_data(gaps[0]) if gaps else "补充可复核的一手证据和高可靠研报。"],
        "confidence": _confidence(row.get("confidence")),
        "source_balance": _clean_str(row.get("source_balance")),
        "supporting_evidence": _text_list(row.get("supporting_evidence")),
        "refuting_evidence": _text_list(row.get("refuting_evidence")),
        "research_leads": _text_list(row.get("research_leads")),
        "rollup": _clean_str(row.get("rollup") or row.get("rollup_to_parent")) or answer,
        "synthesis_source": _clean_str(row.get("synthesis_source") or row.get("source")) or "imported",
    }
    if add_imported_at:
        normalized["imported_at"] = datetime.now(timezone.utc).isoformat()
    elif row.get("imported_at"):
        normalized["imported_at"] = _clean_str(row.get("imported_at"))
    return normalized


def _apply_override_to_node(node: dict[str, Any], override: dict[str, Any]) -> None:
    current_professional = node.get("professional_answer", {})
    current_synthesis = node.get("synthesis", {})
    facts = override["facts"] or current_synthesis.get("facts", [])
    inferences = override["inferences"] or current_synthesis.get("inferences", [])
    gaps = override["gaps"] or current_synthesis.get("gaps", [])
    next_data = override["next_data"] or current_professional.get("next_data", [])
    supporting = override["supporting_evidence"] or current_professional.get("supporting_evidence", [])
    refuting = override["refuting_evidence"] or current_professional.get("refuting_evidence", [])
    leads = override["research_leads"] or current_professional.get("research_leads", [])
    source_balance = override["source_balance"] or current_professional.get("source_balance", "")
    professional_answer = {
        "answer": override["answer"],
        "facts": facts,
        "inferences": inferences,
        "supporting_evidence": supporting,
        "refuting_evidence": refuting,
        "research_leads": leads,
        "judgment": override["judgment"],
        "gaps": gaps,
        "next_data": next_data,
        "source_balance": source_balance,
        "confidence": override["confidence"],
        "rollup": override["rollup"],
    }
    node["professional_answer"] = professional_answer
    node["current_answer"] = override["answer"]
    node["rollup_to_parent"] = override["rollup"]
    node["synthesis"] = {
        "facts": facts,
        "inferences": inferences,
        "judgment": override["judgment"],
        "gaps": gaps,
        "confidence": override["confidence"],
    }
    node["status"] = "open"
    metadata = node.setdefault("metadata", {})
    metadata["synthesis_override"] = {
        "source": override.get("synthesis_source", "imported"),
        "imported_at": override.get("imported_at", ""),
    }


def _validate_override_node_ids(qa_tree: dict[str, Any], overrides: list[dict[str, Any]], path: Path) -> None:
    node_ids = {node.get("id") for node in qa_tree.get("nodes", [])}
    missing = [row["node_id"] for row in overrides if row["node_id"] not in node_ids]
    if missing:
        raise ValueError(f"{path}: node_id not found in current QA tree: {', '.join(missing[:5])}")


def _is_leaf_node(qa_tree: dict[str, Any], node: dict[str, Any]) -> bool:
    return int(node.get("level", 0)) >= int(qa_tree.get("default_depth", 3)) or not node.get("next_question_ids")


def _task_id(object_type: str, object_id: str, node_id: str) -> str:
    digest = hashlib.sha1(f"{object_type}\n{object_id}\n{node_id}".encode("utf-8")).hexdigest()[:12]
    return f"synthesize_{digest}"


def _import_command(object_type: str, object_id: str) -> str:
    if object_type == "stock":
        return f"value-invest-research import-answer-synthesis {object_id} --path synthesized_answers.jsonl"
    return f"value-invest-research import-meta-qa-answer-synthesis --project-id {object_id} --path synthesized_answers.jsonl"


def _confidence(value: Any) -> str:
    text = _clean_str(value).lower()
    return text if text in {"low", "medium", "high"} else "medium"


def _text_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, list):
        items = []
        for item in value:
            text = _clean_str(item)
            if text:
                items.append(text)
        return items
    text = _clean_str(value)
    return [text] if text else []


def _clean_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value).strip()


def _gap_to_next_data(gap: str) -> str:
    gap = gap.strip()
    if not gap:
        return "补充可复核的一手证据和高可靠研报。"
    return f"围绕缺口补充数据：{gap}"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: {exc}") from exc
    return rows


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
