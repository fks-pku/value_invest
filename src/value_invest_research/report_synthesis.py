from __future__ import annotations

import json
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any

from value_invest_research.research_system import _apple_research_css, _qa_explorer_css


PROFESSIONAL_REPORT_MD = "professional_report.md"
PROFESSIONAL_REPORT_HTML = "professional_report.html"
INVESTMENT_WORKBENCH_JSON = "investment_workbench.json"


def write_stock_professional_report(root: Path, ticker: str, client: Any | None = None) -> dict[str, Any]:
    """Write a professional report from the stock layered QA tree."""
    from value_invest_research.research_system import build_research_system, normalize_ticker

    normalized = normalize_ticker(ticker)
    build_result = build_research_system(root, normalized)
    research_dir = Path(build_result["qa_tree_path"]).parent
    qa_tree = _read_json(research_dir / "qa_tree.json")
    context = _report_context(
        object_type="stock",
        object_id=normalized,
        meta_question=qa_tree.get("nodes", [{}])[0].get("question", f"{normalized} 的公司基础画像如何？"),
        qa_tree=qa_tree,
    )
    workbench = _load_optional_json(research_dir / INVESTMENT_WORKBENCH_JSON)
    markdown = _professional_report_markdown(context, client, workbench)
    md_path, html_path = _write_report_files(research_dir, markdown, title=f"{normalized} 专业投研报告", context=context, workbench=workbench)
    return {
        **build_result,
        "ticker": normalized,
        "professional_report_path": str(html_path),
        "professional_report_md_path": str(md_path),
        "investment_workbench_path": str(research_dir / INVESTMENT_WORKBENCH_JSON) if workbench else "",
        "report_mode": "llm" if client is not None else "deterministic",
        "sections": len(context["top_level"]),
        "leaf_questions": len(context["leaf_nodes"]),
    }


def write_meta_qa_professional_report(root: Path, project_id: str, client: Any | None = None) -> dict[str, Any]:
    """Write a professional report from a generic meta-QA tree."""
    from value_invest_research.meta_qa_research import _rebuild_meta_qa_project

    rebuild_result = _rebuild_meta_qa_project(root, project_id)
    project_dir = Path(rebuild_result["project_dir"])
    qa_tree = _read_json(project_dir / "qa_tree.json")
    context = _report_context(
        object_type=qa_tree.get("object_type", "custom"),
        object_id=qa_tree.get("object_id", project_id),
        meta_question=qa_tree.get("meta_question", ""),
        qa_tree=qa_tree,
    )
    title = f"{project_id} 专业投研报告"
    workbench = _load_optional_json(project_dir / INVESTMENT_WORKBENCH_JSON)
    markdown = _professional_report_markdown(context, client, workbench)
    md_path, html_path = _write_report_files(project_dir, markdown, title=title, context=context, workbench=workbench)
    return {
        **rebuild_result,
        "professional_report_path": str(html_path),
        "professional_report_md_path": str(md_path),
        "investment_workbench_path": str(project_dir / INVESTMENT_WORKBENCH_JSON) if workbench else "",
        "report_mode": "llm" if client is not None else "deterministic",
        "sections": len(context["top_level"]),
        "leaf_questions": len(context["leaf_nodes"]),
    }


def _professional_report_markdown(context: dict[str, Any], client: Any | None, workbench: dict[str, Any] | None = None) -> str:
    if client is None:
        return _deterministic_report_markdown(context, workbench)
    response = client.chat(_llm_report_system_prompt(), _llm_report_user_prompt(context, workbench))
    text = str(response).strip()
    if not text:
        return _deterministic_report_markdown(context, workbench)
    return text


def _report_context(
    object_type: str,
    object_id: str,
    meta_question: str,
    qa_tree: dict[str, Any],
) -> dict[str, Any]:
    nodes = qa_tree.get("nodes", [])
    nodes_by_id = {node.get("id", ""): node for node in nodes}
    root = _root_node(nodes)
    top_level = [nodes_by_id[node_id] for node_id in root.get("next_question_ids", []) if node_id in nodes_by_id]
    leaf_nodes = [node for node in nodes if _is_leaf_node(qa_tree, node)]
    evidence_counts = _evidence_counts(nodes)
    top_sections = [_section_context(qa_tree, node, nodes_by_id) for node in top_level]
    priority_gaps = _priority_gaps(leaf_nodes)
    return {
        "object_type": object_type,
        "object_id": object_id,
        "meta_question": meta_question,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "node_count": len(nodes),
        "root": _compact_node(root),
        "leaf_nodes": [_compact_node(node) for node in leaf_nodes],
        "top_level": top_sections,
        "evidence_counts": evidence_counts,
        "priority_gaps": priority_gaps,
        "root_answer": root.get("current_answer", ""),
        "root_judgment": root.get("synthesis", {}).get("judgment", ""),
        "source_index": _source_index(nodes),
    }


def _section_context(
    qa_tree: dict[str, Any],
    node: dict[str, Any],
    nodes_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    children = [nodes_by_id[node_id] for node_id in node.get("next_question_ids", []) if node_id in nodes_by_id]
    descendants = _descendant_nodes(node, nodes_by_id)
    leaf_nodes = [child for child in descendants if _is_leaf_node(qa_tree, child)]
    return {
        **_compact_node(node),
        "children": [_compact_node(child) for child in children[:8]],
        "l2_sections": [_l2_section_context(qa_tree, child, nodes_by_id) for child in children[:8]],
        "leaf_nodes": [_compact_node(child) for child in leaf_nodes[:16]],
    }


def _l2_section_context(
    qa_tree: dict[str, Any],
    node: dict[str, Any],
    nodes_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    children = [nodes_by_id[node_id] for node_id in node.get("next_question_ids", []) if node_id in nodes_by_id]
    return {
        **_compact_node(node),
        "children": [_compact_node(child) for child in children[:8]],
        "leaf_nodes": [_compact_node(child) for child in children if _is_leaf_node(qa_tree, child)][:8],
    }


def _compact_node(node: dict[str, Any]) -> dict[str, Any]:
    answer = node.get("professional_answer", {})
    synthesis = node.get("synthesis", {})
    return {
        "id": node.get("id", ""),
        "level": node.get("level", ""),
        "question": node.get("question", ""),
        "answer": node.get("current_answer", ""),
        "judgment": answer.get("judgment") or synthesis.get("judgment", ""),
        "rollup": answer.get("rollup") or node.get("rollup_to_parent", ""),
        "confidence": answer.get("confidence") or synthesis.get("confidence", ""),
        "facts": _as_text_list(answer.get("facts") or synthesis.get("facts"))[:4],
        "inferences": _as_text_list(answer.get("inferences") or synthesis.get("inferences"))[:3],
        "gaps": _as_text_list(answer.get("gaps") or synthesis.get("gaps"))[:4],
        "next_data": _as_text_list(answer.get("next_data"))[:4],
        "supporting_evidence": _as_text_list(answer.get("supporting_evidence"))[:4],
        "refuting_evidence": _as_text_list(answer.get("refuting_evidence"))[:4],
        "research_leads": _as_text_list(answer.get("research_leads"))[:4],
        "source_summaries": _source_summary_lines(node)[:8],
        "source_items": _source_items(node)[:8],
        "source_balance": answer.get("source_balance", ""),
        "evidence_counts": _node_evidence_counts(node),
    }


def _deterministic_report_markdown(context: dict[str, Any], workbench: dict[str, Any] | None = None) -> str:
    title = f"{context['object_id'] or context['object_type']} 专业投研报告"
    top_judgments = _top_judgment_lines(context)
    section_blocks = "\n\n".join(_section_markdown(section) for section in context["top_level"])
    gap_lines = "\n".join(f"- {gap}" for gap in context["priority_gaps"][:8]) or "- 暂无明确缺口，但仍需持续补充一手证据、研报和反证信息。"
    workbench_block = _workbench_markdown(workbench)
    return f"""# {title}

## 研究问题
{context['meta_question']}

## 投研摘要
{top_judgments}

## 证据结构
- 问题节点：{context['node_count']}
- 叶子问题：{len(context['leaf_nodes'])}
- 证据：{context['evidence_counts']['evidence']}
- 研究报告：{context['evidence_counts']['research_report']}
- 消息：{context['evidence_counts']['message']}
- 观点：{context['evidence_counts']['opinion']}
{workbench_block}

## 关键判断
{section_blocks}

## 关键缺口和下一步
{gap_lines}

## 使用边界
本报告由层级 QA 系统生成，用于组织研究问题、证据结构、反证条件和下一步数据需求，不构成交易建议。
"""


def _top_judgment_lines(context: dict[str, Any]) -> str:
    lines = []
    for section in context["top_level"][:5]:
        takeaway = _section_takeaway(section)
        if takeaway:
            lines.append(f"- {section['question']}：{_truncate(takeaway, 220)}")
    return "\n".join(lines) or f"- {context.get('root_judgment') or context.get('root_answer') or '当前仍处于资料搜集和问题收敛阶段。'}"


def _section_markdown(section: dict[str, Any]) -> str:
    facts = _section_fact_lines(section, limit=6)
    inferences = _section_inference_lines(section, limit=4)
    leaf_lines = _section_leaf_answer_lines(section, limit=6)
    constraints = _section_constraint_lines(section, limit=4)
    gaps = _section_gap_lines(section, limit=4)
    fact_block = "\n".join(f"- {line}" for line in facts) or "- 暂无足够具体事实，需优先补一手来源和可复核研报。"
    inference_block = "\n".join(f"- {line}" for line in inferences) or "- 当前还不能形成稳定推论。"
    leaf_block = "\n".join(f"- {line}" for line in leaf_lines) or "- 暂无可引用的子问题答案。"
    constraint_block = "\n".join(f"- {line}" for line in constraints) or "- 暂未发现明确反证，但不能把未发现反证等同于已证实。"
    gap_block = "\n".join(f"- {gap}" for gap in gaps) or "- 继续补充该板块的关键事实和反证条件。"
    return f"""### {section['question']}
结论：{_section_takeaway(section)}

事实依据：
{fact_block}

推论：
{inference_block}

关键子问题回答：
{leaf_block}

反证与约束：
{constraint_block}

待验证缺口：
{gap_block}"""


def _section_takeaway(section: dict[str, Any]) -> str:
    facts = _section_fact_lines(section, limit=2)
    constraints = _section_constraint_lines(section, limit=1)
    if facts:
        base = "；".join(facts)
        if constraints:
            return f"已有资料显示，{base}。主要约束是：{constraints[0]}"
        return f"已有资料显示，{base}。"
    fallback = _first_content_line(
        [
            section.get("judgment", ""),
            section.get("answer", ""),
            section.get("rollup", ""),
        ]
    )
    return fallback or "该板块仍需补充可复核事实后再形成结论。"


def _section_fact_lines(section: dict[str, Any], limit: int) -> list[str]:
    lines: list[str] = []
    for node in [*section.get("leaf_nodes", []), *section.get("children", []), section]:
        lines.extend(_clean_report_lines(node.get("source_summaries", [])))
    for node in [section, *section.get("leaf_nodes", []), *section.get("children", [])]:
        lines.extend(_clean_report_lines(node.get("facts", [])))
        if not lines:
            lines.extend(_clean_report_lines(node.get("supporting_evidence", [])))
    return _unique_limited(lines, limit)


def _section_inference_lines(section: dict[str, Any], limit: int) -> list[str]:
    lines: list[str] = []
    for node in [*section.get("leaf_nodes", []), *section.get("children", []), section]:
        lines.extend(_clean_report_lines(node.get("inferences", []), allow_generic=False))
    return _unique_limited(lines, limit)


def _section_leaf_answer_lines(section: dict[str, Any], limit: int) -> list[str]:
    lines: list[str] = []
    for node in section.get("leaf_nodes", []):
        claim = _first_content_line(node.get("facts", [])) or _first_content_line(node.get("supporting_evidence", []))
        if claim:
            lines.append(f"{node.get('question', '')}：{claim}")
    return _unique_limited(lines, limit)


def _section_constraint_lines(section: dict[str, Any], limit: int) -> list[str]:
    lines: list[str] = []
    for node in [*section.get("leaf_nodes", []), *section.get("children", []), section]:
        lines.extend(_clean_report_lines(node.get("refuting_evidence", [])))
        lines.extend(_clean_report_lines(node.get("research_leads", [])))
    return _unique_limited(lines, limit)


def _section_gap_lines(section: dict[str, Any], limit: int) -> list[str]:
    lines: list[str] = []
    for node in [*section.get("leaf_nodes", []), *section.get("children", []), section]:
        lines.extend(_clean_report_lines(node.get("gaps", []), allow_generic=False))
        lines.extend(_clean_report_lines(node.get("next_data", []), allow_generic=False))
    return _unique_limited(lines, limit)


def _source_summary_lines(node: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for item in _source_items(node):
        source = str(item.get("source_name") or "").strip()
        evidence_id = str(item.get("evidence_id") or "").strip()
        summary = str(item.get("summary") or "").strip()
        label = f"{source}：" if source else ""
        suffix = f" [{evidence_id}]" if evidence_id else ""
        lines.append(f"{label}{summary}{suffix}")
    return lines


def _source_items(node: dict[str, Any]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    buckets = node.get("evidence_buckets", {})
    for category in ("evidence", "research_report", "message", "opinion"):
        for item in buckets.get(category, []) or []:
            if item.get("missing_record"):
                continue
            summary = str(item.get("summary") or item.get("point") or "").strip()
            if not summary:
                continue
            source_name = str(item.get("source_name") or item.get("evidence_id") or "").strip()
            evidence_id = str(item.get("evidence_id") or "").strip()
            items.append(
                {
                    "category": category,
                    "evidence_id": evidence_id,
                    "source_name": source_name,
                    "summary": summary,
                    "url": str(item.get("url") or "").strip(),
                    "relation": str(item.get("relation") or "").strip(),
                    "reliability": str(item.get("reliability") or "").strip(),
                }
            )
    return items


def _source_index(nodes: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    index: dict[str, dict[str, str]] = {}
    for node in nodes:
        for item in _source_items(node):
            evidence_id = item.get("evidence_id", "")
            if evidence_id and evidence_id not in index:
                index[evidence_id] = item
    return index


def _first_content_line(values: Any) -> str:
    lines = _clean_report_lines(values)
    return lines[0] if lines else ""


def _clean_report_lines(values: Any, allow_generic: bool = True) -> list[str]:
    lines = []
    for value in _as_text_list(values):
        line = _clean_report_line(value)
        if not line:
            continue
        if _is_structure_summary(line):
            continue
        if _is_generic_placeholder(line):
            continue
        if not allow_generic and _is_generic_process_line(line):
            continue
        lines.append(line)
    return lines


def _clean_report_line(value: Any) -> str:
    text = str(value).strip()
    if not text:
        return ""
    for _ in range(8):
        changed = False
        for prefix in ("证据：", "研报：", "消息：", "观点：", "支撑：", "反证：", "线索："):
            if text.startswith(prefix):
                text = text[len(prefix) :].strip()
                changed = True
                break
        if changed:
            continue
        if "：" not in text:
            break
        left, right = text.split("：", 1)
        if _looks_like_question_label(left) or right.startswith(("证据：", "研报：", "消息：", "观点：")):
            text = right.strip()
            continue
        break
    return text.rstrip("。；; ")


def _looks_like_question_label(text: str) -> bool:
    if text.endswith(("？", "?")):
        return True
    return any(token in text for token in ("是否", "什么", "哪些", "如何", "为什么", "谁", "哪里", "哪一", "能否", "是不是"))


def _is_structure_summary(text: str) -> bool:
    return any(
        token in text
        for token in (
            "当前已覆盖",
            "信息结构为",
            "四类来源覆盖",
            "核心判断是",
            "子问题",
            "本层可以上抛",
            "本层只能上抛",
        )
    )


def _is_generic_process_line(text: str) -> bool:
    return any(
        token in text
        for token in (
            "证据和研报可作为结论主支撑",
            "消息和观点只作为研究线索",
            "信息结构缺口集中在",
            "围绕缺口补充数据",
            "需要补充能直接回答",
            "当前结论不能完整闭环",
        )
    )


def _is_generic_placeholder(text: str) -> bool:
    return any(
        token in text
        for token in (
            "当前生意是否具备可重复的收入、利润和现金转化质量",
            "竞争地位是否足以抵抗价格战、份额流失和利润率压缩",
            "公司是否在产业链中占据能持续捕获经济性的环节",
            "当前风险是否足以改变基础画像或成为反证条件",
        )
    )


def _unique_limited(lines: list[str], limit: int) -> list[str]:
    unique: list[str] = []
    seen: set[str] = set()
    for line in lines:
        cleaned = _truncate(line, 180)
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        unique.append(cleaned)
        if len(unique) >= limit:
            break
    return unique


def _llm_report_system_prompt() -> str:
    return (
        "你是专业二级市场投研分析师，负责把层级 QA 树收敛成一份正式研究报告。"
        "必须用中文；必须区分事实、推论、判断、缺口；不得给出买卖建议；"
        "低可靠消息和观点只能作为线索，不能单独强化结论。"
    )


def _llm_report_user_prompt(context: dict[str, Any], workbench: dict[str, Any] | None = None) -> str:
    compact = {
        "object_type": context["object_type"],
        "object_id": context["object_id"],
        "meta_question": context["meta_question"],
        "evidence_counts": context["evidence_counts"],
        "top_level": context["top_level"],
        "priority_gaps": context["priority_gaps"],
        "investment_workbench": workbench or {},
    }
    return "\n".join(
        [
            "请基于以下层级 QA 研究上下文，写一份 Markdown 专业研究报告。",
            "",
            json.dumps(compact, ensure_ascii=False, indent=2, sort_keys=True),
            "",
            "报告结构必须包含：",
            "1. 研究问题",
            "2. 一页投研摘要",
            "3. 核心判断与依据",
            "4. 投资标的映射和观察池",
            "5. 假设-证据-反证-触发器矩阵",
            "6. 反证条件",
            "7. 信息缺口和下一步数据",
            "8. 使用边界",
            "",
            "要求：每个重要判断都要回到 QA 节点、事实/推论/判断/缺口或来源结构；不要输出交易建议。",
        ]
    )


def _write_report_files(
    container_dir: Path,
    markdown: str,
    title: str,
    context: dict[str, Any] | None = None,
    workbench: dict[str, Any] | None = None,
) -> tuple[Path, Path]:
    md_path = container_dir / PROFESSIONAL_REPORT_MD
    html_path = container_dir / PROFESSIONAL_REPORT_HTML
    md_path.write_text(markdown.rstrip() + "\n", encoding="utf-8")
    html_path.write_text(_markdown_report_html(markdown, title, context=context, workbench=workbench), encoding="utf-8")
    return md_path, html_path


def _markdown_report_html(
    markdown: str,
    title: str,
    context: dict[str, Any] | None = None,
    workbench: dict[str, Any] | None = None,
) -> str:
    qa_html = _render_qa_hierarchy(context, workbench) if context else ""
    nav = _professional_report_nav(context, workbench)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>{_apple_research_css()}{_qa_explorer_css()}{_investment_workbench_css()}</style>
</head>
<body>
  <header>
    <p class="eyebrow">产业链 QA 研究</p>
    <h1>{escape(title)}</h1>
    <p class="subtitle">先明确当前研究问题，再按问题树逐层下钻；每个叶子问题挂接证据、研报、消息和观点。</p>
  </header>
  {nav}
  <main class="qa-full-research">
    {qa_html}
  </main>
</body>
</html>
"""


def _professional_report_nav(context: dict[str, Any] | None, workbench: dict[str, Any] | None = None) -> str:
    links = [("#research-target", "研究问题"), ("#qa-split", "下钻 QA")]
    if workbench and workbench.get("research_execution_plan"):
        links = [("#research-target", "研究问题"), ("#execution-plan", "研究计划"), ("#qa-split", "下钻 QA")]
    if context:
        for index, section in enumerate(context.get("top_level", [])[:6], start=1):
            links.append((f"#qa-l1-{index}", f"Q{index}"))
    if workbench and (workbench.get("specific_targets") or workbench.get("target_mapping")):
        links.append(("#target-recommendations", "标的观察"))
    return "<nav>" + "".join(f'<a href="{escape(href)}">{escape(label)}</a>' for href, label in links) + "</nav>"


def _strip_workbench_markdown_sections(markdown: str) -> str:
    stripped: list[str] = []
    skipping = False
    for line in markdown.splitlines():
        if (
            line.startswith("## 瓶颈研究摘要")
            or line.startswith("## 投资标的映射摘要")
            or line.startswith("## 假设-证据-反证-触发器摘要")
        ):
            skipping = True
            continue
        if skipping and line.startswith("## "):
            skipping = False
        if not skipping:
            stripped.append(line)
    return "\n".join(stripped)


def _workbench_markdown(workbench: dict[str, Any] | None) -> str:
    if not workbench:
        return ""
    target_rows = workbench.get("target_mapping", []) or []
    hypothesis_rows = workbench.get("hypothesis_matrix", []) or []
    bottleneck_rows = workbench.get("bottleneck_scorecard", []) or []
    target_lines = "\n".join(
        f"- {row.get('tier', '')}｜{row.get('target_type', '')}：{row.get('research_action', '')}"
        for row in target_rows[:8]
    )
    hypothesis_lines = "\n".join(
        f"- {row.get('hypothesis', '')}：{row.get('current_judgment', '')}"
        for row in hypothesis_rows[:8]
    )
    if not target_lines:
        target_lines = "- 当前尚未形成可审计的标的映射。"
    if not hypothesis_lines:
        hypothesis_lines = "- 当前尚未形成假设矩阵。"
    bottleneck_lines = "\n".join(
        f"- {row.get('node', '')}：{row.get('current_assessment', '')}"
        for row in bottleneck_rows[:8]
    )
    if not bottleneck_lines:
        bottleneck_lines = "- 当前尚未形成瓶颈评分卡。"
    return f"""

## 瓶颈研究摘要
{bottleneck_lines}

## 投资标的映射摘要
{target_lines}

## 假设-证据-反证-触发器摘要
{hypothesis_lines}
"""


def _render_qa_hierarchy(context: dict[str, Any], workbench: dict[str, Any] | None) -> str:
    root = context.get("root", {})
    plan = (workbench or {}).get("research_execution_plan")
    plan_html = _render_research_execution_plan(plan) if plan else ""
    qa_label = "03" if plan_html else "02"
    target_label = "04" if plan_html else "03"
    l1_sections = "\n".join(
        _render_qa_l1_section(section, index)
        for index, section in enumerate(context.get("top_level", []), start=1)
    )
    target_html = _render_target_recommendations(workbench, context.get("source_index", {}), target_label)
    source_collapse = _render_source_collapse(context.get("source_index", {}))
    metrics = [
        ("问题节点", context.get("node_count", 0)),
        ("叶子问题", len(context.get("leaf_nodes", []))),
        ("证据", context.get("evidence_counts", {}).get("evidence", 0)),
        ("研报/消息/观点", f"{context.get('evidence_counts', {}).get('research_report', 0)} / {context.get('evidence_counts', {}).get('message', 0)} / {context.get('evidence_counts', {}).get('opinion', 0)}"),
    ]
    metric_html = "".join(
        f'<div class="qa-metric"><span>{escape(label)}</span><strong>{escape(str(value))}</strong></div>'
        for label, value in metrics
    )
    direction_html = "".join(
        f"""
        <a class="qa-direction-link" href="#qa-l1-{index}">
          <span>Q{index}</span>
          <strong>{escape(str(section.get("question", "")))}</strong>
          <em>{escape(_source_mix_text(section.get("evidence_counts", {})))}</em>
        </a>
        """
        for index, section in enumerate(context.get("top_level", []), start=1)
    )
    return f"""
    <section id="research-target" class="level-frame qa-target-section">
      <div class="qa-section-title">
        <p class="eyebrow">01 / 当前研究的问题</p>
        <h2>{escape(str(context.get("meta_question", "")))}</h2>
      </div>
      <p class="qa-target-answer">{escape(_node_takeaway(root))}</p>
      <div class="qa-metric-grid">{metric_html}</div>
    </section>
    {plan_html}
    <section id="qa-split" class="level-frame qa-split-section">
      <div class="qa-section-title">
        <p class="eyebrow">{qa_label} / 下钻 QA</p>
        <h2>从研究方向到资料搜集</h2>
        <p class="subtitle-small">阅读顺序：Q1/Q2/Q3/Q4 是研究方向，Qx.y 是机制问题，Qx.y.z 是具体资料搜集和证据判断。</p>
      </div>
      <div class="qa-direction-grid">{direction_html}</div>
    </section>
    {l1_sections}
    {target_html}
    {source_collapse}
    """


def _render_qa_l1_section(section: dict[str, Any], index: int) -> str:
    l2_html = "\n".join(
        _render_qa_l2_section(l2, index, l2_index)
        for l2_index, l2 in enumerate(section.get("l2_sections", []) or [], start=1)
    )
    support = _section_fact_lines(section, limit=3)
    gaps = _section_gap_lines(section, limit=3)
    source_html = _render_source_item_list("主要来源", _section_source_items(section, limit=4))
    support_html = source_html or _render_qa_list("主要事实", support)
    gap_html = _render_qa_list("下一步缺口", gaps)
    return f"""
    <details id="qa-l1-{index}" class="level-frame qa-l1-section qa-card level-1" open>
      <summary class="qa-level-head">
        <span>Q{index}</span>
        <h2>{escape(str(section.get("question", "")))}</h2>
        <em>{escape(_source_mix_text(section.get("evidence_counts", {})))}</em>
      </summary>
      <div class="qa-l1-body">
        <div class="qa-l1-layout">
          <article class="qa-conclusion-card qa-block">
            <h4 class="block-title">1. 当前结论呈现</h4>
            <b>本层结论</b>
            <p>{escape(_node_takeaway(section))}</p>
            <div class="source-coverage-strip">{_render_source_coverage(section.get("evidence_counts", {}))}</div>
          </article>
          <aside class="qa-side-card qa-block">
            <h4 class="block-title">3. 待补充的问题</h4>
            {support_html}
            {gap_html}
          </aside>
        </div>
        <div class="qa-block">
          <h4 class="block-title">2. 问题展开（子 QA）</h4>
          <div class="qa-l2-stack">{l2_html}</div>
        </div>
      </div>
    </details>
    """


def _render_qa_l2_section(section: dict[str, Any], l1_index: int, index: int) -> str:
    prefix = f"{l1_index}.{index}"
    l3_html = "\n".join(
        _render_qa_l3_card(leaf, prefix, i)
        for i, leaf in enumerate(section.get("leaf_nodes", []), start=1)
    )
    return f"""
    <!-- <details class="qa-l2-card" compatibility marker> -->
    <details class="qa-l2-card qa-card level-2" open>
      <summary>
        <span>Q{prefix}</span>
        <strong>{escape(str(section.get("question", "")))}</strong>
        <em>{escape(_source_mix_text(section.get("evidence_counts", {})))}</em>
      </summary>
      <div class="qa-l2-body">
        <div class="qa-l2-answer qa-block">
          <h4 class="block-title">1. 当前结论呈现</h4>
          <b>当前回答</b>
          <p>{escape(_node_takeaway(section))}</p>
        </div>
        <div class="qa-block">
          <h4 class="block-title">2. 问题展开（子 QA）</h4>
          <div class="qa-l3-grid">{l3_html}</div>
        </div>
        <div class="qa-block">
          <h4 class="block-title">3. 待补充的问题</h4>
          {_render_qa_list("缂哄彛", _clean_report_lines(section.get("gaps") or section.get("next_data"), allow_generic=False)[:3])}
        </div>
      </div>
    </details>
    """


def _render_qa_l3_card(node: dict[str, Any], prefix: str, index: int) -> str:
    facts = node.get("facts") or node.get("supporting_evidence") or node.get("source_summaries") or []
    constraints = node.get("refuting_evidence") or node.get("research_leads") or []
    gaps = node.get("gaps") or node.get("next_data") or []
    source_index = _render_source_item_list("资料索引", node.get("source_items", []), limit=4)
    return f"""
    <!-- <details class="qa-l3-card" compatibility marker> -->
    <details class="qa-l3-card qa-card level-3" open>
      <summary class="qa-l3-head">
        <span>Q{prefix}.{index}</span>
        <strong>{escape(str(node.get("question", "")))}</strong>
        <b>{escape(_source_mix_text(node.get("evidence_counts", {})))}</b>
      </summary>
      <div class="qa-l3-body">
        <div class="qa-block">
          <h4 class="block-title">1. 当前结论呈现</h4>
          <p>{escape(_node_takeaway(node))}</p>
        </div>
        <div class="qa-block">
          <h4 class="block-title">2. 问题展开（子 QA）</h4>
        </div>
        <div class="qa-l3-columns">
          {_render_qa_list("事实/支撑", _clean_report_lines(facts)[:3])}
          {_render_qa_list("反证/线索", _clean_report_lines(constraints)[:3])}
          {_render_qa_list("缺口", _clean_report_lines(gaps, allow_generic=False)[:3])}
        </div>
        <div class="qa-block">
          <h4 class="block-title">3. 待补充的问题</h4>
          {_render_qa_list("缂哄彛", _clean_report_lines(gaps, allow_generic=False)[:3])}
        </div>
        {source_index}
      </div>
    </details>
    """


def _render_section_workbench_summary(section: dict[str, Any], workbench: dict[str, Any] | None) -> str:
    if not workbench:
        return ""
    related = _related_workbench_items(section, workbench)
    if not any(related.values()):
        return ""
    cards = []
    labels = {
        "bottlenecks": "相关瓶颈",
        "hypotheses": "相关假设",
        "targets": "标的映射",
        "challenges": "反方质询",
    }
    for key, label in labels.items():
        values = related.get(key, [])
        if not values:
            continue
        cards.append(
            f'<div class="qa-workbench-mini"><b>{escape(label)}</b><ul>'
            + "".join(f"<li>{escape(item)}</li>" for item in values[:4])
            + "</ul></div>"
        )
    return f'<div class="qa-workbench-row">{"".join(cards)}</div>'


def _related_workbench_items(section: dict[str, Any], workbench: dict[str, Any]) -> dict[str, list[str]]:
    text = f"{section.get('id', '')} {section.get('question', '')}".lower()
    if any(token in text for token in ("fact", "timeline", "事实", "边界")):
        mode = "facts"
    elif any(token in text for token in ("transmission", "channel", "affected", "传导", "影响")):
        mode = "transmission"
    elif any(token in text for token in ("market", "priced", "surprise", "市场", "定价")):
        mode = "market"
    elif any(token in text for token in ("follow", "trigger", "disconfirm", "跟踪", "反证")):
        mode = "follow"
    else:
        mode = "general"

    hypotheses = []
    for row in workbench.get("hypothesis_matrix", []) or []:
        linked = " ".join(_as_text_list(row.get("linked_questions", [])))
        haystack = f"{row.get('id', '')} {row.get('hypothesis', '')} {linked}"
        if _mode_matches(mode, haystack):
            hypotheses.append(f"{row.get('id', '')}：{row.get('hypothesis', '')}")
    bottlenecks = []
    for row in workbench.get("bottleneck_scorecard", []) or []:
        haystack = f"{row.get('node', '')} {row.get('current_assessment', '')}"
        if mode in {"transmission", "follow"} or _mode_matches(mode, haystack):
            bottlenecks.append(f"{row.get('node', '')}：{row.get('current_assessment', '')}")
    targets = []
    for row in workbench.get("target_mapping", []) or []:
        haystack = f"{row.get('tier', '')} {row.get('target_type', '')} {row.get('mapping_logic', '')}"
        if mode in {"transmission", "market"} or _mode_matches(mode, haystack):
            targets.append(f"{row.get('tier', '')}｜{row.get('target_type', '')}")
    challenges = []
    for row in workbench.get("adversarial_review", []) or []:
        haystack = f"{row.get('challenge', '')} {row.get('why_it_matters', '')}"
        if mode in {"facts", "market", "follow"} or _mode_matches(mode, haystack):
            challenges.append(f"{row.get('id', '')}：{row.get('challenge', '')}")
    return {
        "bottlenecks": bottlenecks[:4],
        "hypotheses": hypotheses[:4],
        "targets": targets[:4],
        "challenges": challenges[:4],
    }


def _mode_matches(mode: str, text: str) -> bool:
    tokens = {
        "facts": ("事实", "边界", "自然定律", "概念", "重命名"),
        "transmission": ("传导", "供应链", "先进封装", "光互连", "eda", "存储", "利润池"),
        "market": ("市场", "定价", "etf", "拥挤", "主题", "估值"),
        "follow": ("触发", "反证", "良率", "能耗", "散热", "成本", "验证"),
    }.get(mode, ())
    lower = text.lower()
    return any(token.lower() in lower for token in tokens)


def _render_qa_list(label: str, values: list[str]) -> str:
    items = _unique_limited(values, 4)
    if not items:
        return f'<div class="qa-mini-list"><b>{escape(label)}</b><p class="note">待补</p></div>'
    return (
        f'<div class="qa-mini-list"><b>{escape(label)}</b><ul>'
        + "".join(f"<li>{escape(item)}</li>" for item in items)
        + "</ul></div>"
    )


def _section_source_items(section: dict[str, Any], limit: int) -> list[dict[str, str]]:
    nodes = [section, *section.get("children", []), *section.get("leaf_nodes", [])]
    for l2 in section.get("l2_sections", []) or []:
        nodes.append(l2)
        nodes.extend(l2.get("leaf_nodes", []) or [])
    items: list[dict[str, str]] = []
    seen: set[str] = set()
    for node in nodes:
        for item in node.get("source_items", []) or []:
            key = item.get("evidence_id") or item.get("url") or item.get("source_name")
            if not key or key in seen:
                continue
            seen.add(key)
            items.append(item)
            if len(items) >= limit:
                return items
    return items


def _render_source_item_list(label: str, items: Any, limit: int = 4) -> str:
    clean_items = []
    seen: set[str] = set()
    for item in items or []:
        if not isinstance(item, dict):
            continue
        key = str(item.get("evidence_id") or item.get("url") or item.get("source_name") or "").strip()
        if not key or key in seen:
            continue
        seen.add(key)
        clean_items.append(item)
        if len(clean_items) >= limit:
            break
    if not clean_items:
        return ""
    rendered = []
    for item in clean_items:
        source = str(item.get("source_name") or item.get("evidence_id") or "来源").strip()
        url = str(item.get("url") or "").strip()
        category = _category_label(str(item.get("category") or ""))
        relation = str(item.get("relation") or "").strip()
        summary = _truncate(str(item.get("summary") or ""), 150)
        meta = " / ".join(part for part in (category, relation) if part)
        rendered.append(
            "<li>"
            f'<span class="source-chip">{escape(meta or category or "来源")}</span>'
            f"{_source_anchor(source, url)}"
            f"<p>{escape(summary)}</p>"
            "</li>"
        )
    return f'<div class="qa-source-list"><b>{escape(label)}</b><ul>{"".join(rendered)}</ul></div>'


def _source_anchor(label: str, url: str) -> str:
    if url:
        return f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(label)}</a>'
    return f"<strong>{escape(label)}</strong>"


def _category_label(category: str) -> str:
    return {
        "evidence": "证据",
        "research_report": "研报",
        "message": "消息",
        "opinion": "观点",
    }.get(category, category)


def _render_evidence_links(evidence_ids: Any, source_index: dict[str, dict[str, str]]) -> str:
    links = []
    for evidence_id in _as_text_list(evidence_ids)[:5]:
        item = source_index.get(evidence_id, {})
        label = item.get("source_name") or evidence_id
        url = item.get("url", "")
        links.append(f'<span>{_source_anchor(label, url)}</span>')
    if not links:
        return '<p class="note">来源待补</p>'
    return f'<div class="target-source-links">{"".join(links)}</div>'


def _render_source_links(sources: Any) -> str:
    links = []
    for source in sources or []:
        if isinstance(source, dict):
            label = str(source.get("label") or source.get("name") or source.get("url") or "来源").strip()
            url = str(source.get("url") or "").strip()
            category = str(source.get("category") or "").strip()
        else:
            label = str(source).strip()
            url = ""
            category = ""
        if not label:
            continue
        chip = f'<small>{escape(category)}</small>' if category else ""
        links.append(f'<span>{chip}{_source_anchor(label, url)}</span>')
    if not links:
        return '<p class="note">来源待补</p>'
    return f'<div class="target-source-links">{"".join(links)}</div>'


def _render_source_collapse(source_index: dict[str, dict[str, str]]) -> str:
    if not source_index:
        return """
        <details class="source-collapse" id="source-index">
          <summary><h2>来源索引</h2></summary>
          <div class="source-grid"></div>
        </details>
        """
    cards = []
    for evidence_id, item in sorted(source_index.items()):
        label = item.get("source_name") or evidence_id
        category = item.get("category") or "source"
        summary = item.get("summary") or ""
        url = item.get("url") or ""
        cards.append(
            f"""
            <article class="source-card">
              <span class="source-chip">{escape(str(category))}</span>
              <h3>{_source_anchor(str(label), str(url))}</h3>
              <p>{escape(str(summary))}</p>
            </article>
            """
        )
    return f"""
    <details class="source-collapse" id="source-index">
      <summary><h2>来源索引</h2></summary>
      <div class="source-grid">{"".join(cards)}</div>
    </details>
    """


def _render_research_execution_plan(plan: dict[str, Any]) -> str:
    stages = plan.get("stages", []) or []
    stage_cards = []
    for stage in stages:
        questions = "".join(f"<li>{escape(item)}</li>" for item in _as_text_list(stage.get("questions", []))[:5])
        collection = "".join(f"<li>{escape(item)}</li>" for item in _as_text_list(stage.get("collection", []))[:5])
        synthesis = "".join(f"<li>{escape(item)}</li>" for item in _as_text_list(stage.get("synthesis", []))[:5])
        presentation = "".join(f"<li>{escape(item)}</li>" for item in _as_text_list(stage.get("presentation", []))[:4])
        stage_cards.append(
            f"""
            <article class="execution-stage-card">
              <div class="stage-head">
                <span>{escape(str(stage.get("level", "")))}</span>
                <strong>{escape(str(stage.get("name", "")))}</strong>
              </div>
              <p>{escape(str(stage.get("role", "")))}</p>
              <div class="execution-stage-grid">
                <div><b>提出什么问题</b><ul>{questions or "<li>待补。</li>"}</ul></div>
                <div><b>怎么搜集资料</b><ul>{collection or "<li>待补。</li>"}</ul></div>
                <div><b>怎样串起来</b><ul>{synthesis or "<li>待补。</li>"}</ul></div>
                <div><b>如何呈现</b><ul>{presentation or "<li>待补。</li>"}</ul></div>
              </div>
            </article>
            """
        )
    deepseek_role = str(plan.get("deepseek_role") or "").strip()
    deepseek_html = f'<aside class="deepseek-role"><b>DeepSeek 分工</b><p>{escape(deepseek_role)}</p></aside>' if deepseek_role else ""
    return f"""
    <section id="execution-plan" class="level-frame execution-plan-section">
      <div class="qa-section-title">
        <p class="eyebrow">02 / 研究执行计划</p>
        <h2>{escape(str(plan.get("title", "用问题层级控制研究深度")))}</h2>
        <p class="subtitle-small">{escape(str(plan.get("summary", "每一层都必须明确问题、资料、推理链和呈现方式。")))}</p>
      </div>
      {deepseek_html}
      <div class="execution-stage-stack">{"".join(stage_cards)}</div>
    </section>
    """


def _target_strength(row: dict[str, Any]) -> str:
    tier = str(row.get("tier") or "").strip().upper()
    return {
        "A": "强：核心观察池",
        "B": "中强：高弹性观察池",
        "C": "中低：情绪/拥挤度跟踪",
        "D": "弱：排除或降权池",
    }.get(tier, "待定：需要补充证据")


def _render_target_table(rows: list[dict[str, Any]], *, specific: bool) -> str:
    if not rows:
        return ""
    if specific:
        headers = ["rank", "ticker/name", "thesis node", "strength", "rationale", "downgrade risk"]
        body_rows = [
            [
                str(index),
                f"{row.get('ticker', '')} {row.get('company', '')}",
                str(row.get("bottleneck_node", "")),
                str(row.get("strength", "")),
                str(row.get("reason", "")),
                "; ".join(_as_text_list(row.get("risks", []))[:2]),
            ]
            for index, row in enumerate(rows, start=1)
        ]
    else:
        headers = ["rank", "target", "thesis node", "strength", "rationale", "downgrade risk"]
        body_rows = [
            [
                str(index),
                str(row.get("target_type", "")),
                ", ".join(_as_text_list(row.get("linked_hypotheses", []))[:2]),
                _target_strength(row),
                str(row.get("mapping_logic", "")),
                "; ".join(_as_text_list(row.get("disconfirming_tests", []))[:2]),
            ]
            for index, row in enumerate(rows, start=1)
        ]
    header_html = "".join(f"<th>{escape(header)}</th>" for header in headers)
    row_html = "".join(
        "<tr>" + "".join(f"<td>{escape(cell)}</td>" for cell in row) + "</tr>"
        for row in body_rows
    )
    return f'<div class="target-summary"><table class="target-table"><thead><tr>{header_html}</tr></thead><tbody>{row_html}</tbody></table></div>'


def _render_target_recommendations(
    workbench: dict[str, Any] | None,
    source_index: dict[str, dict[str, str]],
    section_label: str = "03",
) -> str:
    specific_rows = (workbench or {}).get("specific_targets", []) or []
    if specific_rows:
        return _render_specific_target_recommendations(specific_rows, section_label)
    rows = (workbench or {}).get("target_mapping", []) or []
    if not rows:
        return ""
    cards = []
    for row in rows:
        risks = _as_text_list(row.get("disconfirming_tests", []))[:4]
        risk_items = "".join(f"<li>{escape(risk)}</li>" for risk in risks) or "<li>风险条件待补。</li>"
        required = _as_text_list(row.get("required_data", []))[:3]
        required_items = "".join(f"<li>{escape(item)}</li>" for item in required) or "<li>验证数据待补。</li>"
        cards.append(
            f"""
            <article class="recommendation-card tier-{escape(_safe_css_token(row.get("tier", "")))}">
              <div class="recommendation-head">
                <span>{escape(str(row.get("tier", "")))}</span>
                <b>{escape(_target_strength(row))}</b>
              </div>
              <h3>{escape(str(row.get("target_type", "")))}</h3>
              <div class="recommendation-grid">
                <div>
                  <b>推荐理由</b>
                  <p>{escape(str(row.get("mapping_logic", "")))}</p>
                  <p class="recommendation-action">{escape(str(row.get("research_action", "")))}</p>
                </div>
                <div>
                  <b>强度</b>
                  <p>{escape(_target_strength(row))}</p>
                  <p class="note">{escape(str(row.get("time_horizon", "")))}</p>
                </div>
                <div>
                  <b>需要验证</b>
                  <ul>{required_items}</ul>
                </div>
                <div>
                  <b>风险提示</b>
                  <ul>{risk_items}</ul>
                </div>
              </div>
              {_render_evidence_links(row.get("evidence_ids", []), source_index)}
            </article>
            """
        )
    return f"""
    <section id="target-recommendations" class="level-frame target-recommendations target-section">
      <div class="qa-section-title">
        <p class="eyebrow">{section_label} / 标的推荐</p>
        <h2>按瓶颈强度和证据质量形成观察优先级</h2>
        <p class="subtitle-small">这里的“推荐”是投研观察优先级：只说明为什么值得跟踪、强度如何、需要什么证据升级，以及哪些风险会导致降权；不构成买卖建议。</p>
      </div>
      {_render_target_table(rows, specific=False)}
      <div class="recommendation-stack">{"".join(cards)}</div>
    </section>
    """


def _render_specific_target_recommendations(rows: list[dict[str, Any]], section_label: str) -> str:
    cards = []
    for row in rows:
        risks = "".join(f"<li>{escape(item)}</li>" for item in _as_text_list(row.get("risks", []))[:4]) or "<li>风险条件待补。</li>"
        verification = "".join(
            f"<li>{escape(item)}</li>" for item in _as_text_list(row.get("verification_data", []))[:4]
        ) or "<li>验证数据待补。</li>"
        catalysts = "".join(f"<li>{escape(item)}</li>" for item in _as_text_list(row.get("catalysts", []))[:3])
        if not catalysts:
            catalysts = "<li>等待订单、收入和客户验证。</li>"
        cards.append(
            f"""
            <article class="recommendation-card specific-target-card tier-{escape(_safe_css_token(row.get("tier", "")))}">
              <div class="recommendation-head">
                <span>{escape(str(row.get("tier", "")))}</span>
                <b>{escape(str(row.get("strength", "")))}</b>
              </div>
              <div class="specific-target-title">
                <h3>{escape(str(row.get("company", "")))}</h3>
                <strong>{escape(str(row.get("ticker", "")))}</strong>
              </div>
              <p class="target-node">{escape(str(row.get("bottleneck_node", "")))}</p>
              <div class="recommendation-grid specific-target-grid">
                <div>
                  <b>推荐理由</b>
                  <p>{escape(str(row.get("reason", "")))}</p>
                </div>
                <div>
                  <b>验证清单</b>
                  <ul>{verification}</ul>
                </div>
                <div>
                  <b>触发器</b>
                  <ul>{catalysts}</ul>
                </div>
                <div>
                  <b>风险提示</b>
                  <ul>{risks}</ul>
                </div>
              </div>
              {_render_source_links(row.get("sources", []))}
            </article>
            """
        )
    return f"""
    <section id="target-recommendations" class="level-frame target-recommendations target-section">
      <div class="qa-section-title">
        <p class="eyebrow">{section_label} / 标的推荐</p>
        <h2>从方向收敛到明确标的，但只给投研观察优先级</h2>
        <p class="subtitle-small">排序依据是“瓶颈位置 × 财务敞口 × 可验证触发器 × 反证风险”。这里不是买卖指令，后续仍需逐个标的补财报、估值、订单和交易拥挤度。</p>
      </div>
      {_render_target_table(rows, specific=True)}
      <div class="recommendation-stack">{"".join(cards)}</div>
    </section>
    """


def _render_source_coverage(counts: dict[str, int]) -> str:
    labels = [("evidence", "证据"), ("research_report", "研报"), ("message", "消息"), ("opinion", "观点")]
    return "".join(
        f'<div class="coverage-item total"><span>{escape(label)}</span><strong>{int(counts.get(key, 0) or 0)}</strong></div>'
        for key, label in labels
    )


def _source_mix_text(counts: dict[str, int]) -> str:
    return (
        f"证/研/消/观 "
        f"{int(counts.get('evidence', 0) or 0)}/"
        f"{int(counts.get('research_report', 0) or 0)}/"
        f"{int(counts.get('message', 0) or 0)}/"
        f"{int(counts.get('opinion', 0) or 0)}"
    )


def _node_takeaway(node: dict[str, Any]) -> str:
    return _first_content_line(
        [
            node.get("answer", ""),
            node.get("judgment", ""),
            node.get("rollup", ""),
            _first_content_line(node.get("facts", [])),
            _first_content_line(node.get("source_summaries", [])),
        ]
    ) or "当前还没有形成可上抛的结论。"


def _render_investment_workbench(workbench: dict[str, Any] | None, appendix: bool = False) -> str:
    if not workbench:
        return ""
    body = "\n".join(
        [
            _render_depth_control(workbench.get("depth_protocol", {})),
            _render_chokepoint_protocol(workbench.get("chokepoint_protocol", {})),
            _render_supply_chain_map(workbench.get("supply_chain_map", [])),
            _render_bottleneck_scorecard(workbench.get("bottleneck_scorecard", [])),
            _render_hypothesis_matrix(workbench.get("hypothesis_matrix", [])),
            _render_target_mapping(workbench.get("target_mapping", [])),
            _render_adversarial_review(workbench.get("adversarial_review", [])),
            _render_tracking_triggers(workbench.get("tracking_triggers", [])),
        ]
    )
    if not appendix:
        return body
    return f"""
    <section id="workbench-appendix" class="level-frame workbench-appendix">
      <p class="eyebrow">Appendix</p>
      <h2>工作台附录</h2>
      <p class="subtitle-small">以下模块用于审计 QA 结论，不作为主阅读路径。先读问题树，再回到这里检查瓶颈、假设、标的和反方质询。</p>
    </section>
    {body}
    """


def _render_depth_control(protocol: dict[str, Any]) -> str:
    levels = protocol.get("levels", []) or []
    checks = protocol.get("quality_gates", []) or []
    level_cards = "".join(
        f"""
        <article class="workbench-card">
          <span>{escape(str(item.get("level", "")))}</span>
          <h3>{escape(str(item.get("name", "")))}</h3>
          <p>{escape(str(item.get("role", "")))}</p>
          <div class="field"><b>下钻条件</b><p>{escape(str(item.get("drill_rule", "")))}</p></div>
          <div class="field"><b>上抛要求</b><p>{escape(str(item.get("rollup_rule", "")))}</p></div>
        </article>
        """
        for item in levels
    )
    gate_items = "".join(f"<li>{escape(str(item))}</li>" for item in checks)
    if not level_cards:
        level_cards = '<p class="note">尚未定义层级深度协议。</p>'
    if not gate_items:
        gate_items = "<li>每个结论都应能追溯到子问题、来源和反证条件。</li>"
    return f"""
    <section id="depth-control" class="level-frame investment-workbench">
      <p class="eyebrow">Depth Control</p>
      <h2>问题层级即研究深度控制器</h2>
      <p class="subtitle-small">{escape(str(protocol.get("summary", "每一层问题都必须回答清楚为什么要问、如何验证、何时上抛。")))}</p>
      <div class="workbench-grid">{level_cards}</div>
      <div class="gate-box">
        <b>质量门槛</b>
        <ul>{gate_items}</ul>
      </div>
    </section>
    """


def _render_chokepoint_protocol(protocol: dict[str, Any]) -> str:
    steps = protocol.get("steps", []) or []
    cards = "".join(
        f"""
        <article class="workbench-card">
          <span>{escape(str(item.get("step", "")))}</span>
          <h3>{escape(str(item.get("name", "")))}</h3>
          <p>{escape(str(item.get("purpose", "")))}</p>
          <div class="field"><b>关键问题</b><p>{escape(str(item.get("key_question", "")))}</p></div>
          <div class="field"><b>输出物</b><p>{escape(str(item.get("output", "")))}</p></div>
        </article>
        """
        for item in steps
    )
    if not cards:
        cards = '<p class="note">尚未定义瓶颈研究协议。</p>'
    return f"""
    <section id="chokepoint-protocol" class="level-frame investment-workbench">
      <p class="eyebrow">Chokepoint Protocol</p>
      <h2>从大主题下钻到最窄瓶颈</h2>
      <p class="subtitle-small">{escape(str(protocol.get("summary", "先拆产业链，再找不可替代节点，最后映射到可验证标的。")))}</p>
      <div class="workbench-grid">{cards}</div>
    </section>
    """


def _render_supply_chain_map(rows: list[dict[str, Any]]) -> str:
    cards = []
    for row in rows:
        cards.append(
            f"""
            <article class="chain-card">
              <div class="card-head">
                <span>{escape(str(row.get("layer", "")))}</span>
                <b>{escape(str(row.get("status", "")))}</b>
              </div>
              <h3>{escape(str(row.get("bottleneck_question", "")))}</h3>
              <p>{escape(str(row.get("current_judgment", "")))}</p>
              <div class="matrix-grid">
                {_render_labeled_list("潜在控制节点", row.get("candidate_nodes", []))}
                {_render_labeled_list("需要的证明", row.get("proof_needed", []))}
                {_render_labeled_list("反证条件", row.get("disconfirming_tests", []))}
                {_render_labeled_list("来源依据", row.get("evidence_ids", []), chip=True)}
              </div>
            </article>
            """
        )
    if not cards:
        cards.append('<p class="note">尚未形成供应链瓶颈地图。</p>')
    return f"""
    <section id="supply-chain-map" class="level-frame investment-workbench">
      <p class="eyebrow">Supply Chain Map</p>
      <h2>产业链瓶颈地图</h2>
      <p class="subtitle-small">每一层只问一个问题：这个节点如果卡住，会不会拖慢整条主线？如果会，谁控制它，如何验证？</p>
      <div class="chain-stack">{''.join(cards)}</div>
    </section>
    """


def _render_bottleneck_scorecard(rows: list[dict[str, Any]]) -> str:
    body_rows = []
    for row in rows:
        body_rows.append(
            "<tr>"
            f"<td><strong>{escape(str(row.get('node', '')))}</strong><p class=\"note\">{escape(str(row.get('asset_mapping', '')))}</p></td>"
            f"<td>{escape(str(row.get('criticality', '')))}</td>"
            f"<td>{escape(str(row.get('scarcity', '')))}</td>"
            f"<td>{escape(str(row.get('pricing_power', '')))}</td>"
            f"<td>{escape(str(row.get('market_awareness', '')))}</td>"
            f"<td>{escape(str(row.get('evidence_quality', '')))}</td>"
            f"<td>{escape(str(row.get('current_assessment', '')))}</td>"
            "</tr>"
        )
    body = "".join(body_rows) or '<tr><td colspan="7">尚未形成瓶颈评分卡。</td></tr>'
    return f"""
    <section id="bottleneck-scorecard" class="level-frame investment-workbench">
      <p class="eyebrow">Bottleneck Scorecard</p>
      <h2>瓶颈评分卡</h2>
      <table class="score-table">
        <thead><tr><th>节点</th><th>关键性</th><th>稀缺性</th><th>定价权</th><th>市场认知</th><th>证据质量</th><th>当前判断</th></tr></thead>
        <tbody>{body}</tbody>
      </table>
    </section>
    """


def _render_hypothesis_matrix(rows: list[dict[str, Any]]) -> str:
    cards = []
    for row in rows:
        cards.append(
            f"""
            <article class="hypothesis-card">
              <div class="card-head">
                <span>{escape(str(row.get("id", "")))}</span>
                <b>{escape(str(row.get("confidence", "")))}</b>
              </div>
              <h3>{escape(str(row.get("hypothesis", "")))}</h3>
              <p>{escape(str(row.get("current_judgment", "")))}</p>
              <div class="matrix-grid">
                {_render_labeled_list("支撑证据", row.get("supporting_evidence", []))}
                {_render_labeled_list("反证/约束", row.get("disconfirming_evidence", []))}
                {_render_labeled_list("触发器", row.get("triggers", []))}
                {_render_labeled_list("对应标的", row.get("target_implications", []))}
              </div>
              <div class="research-path">{_render_path_chips(row.get("linked_questions", []))}</div>
            </article>
            """
        )
    if not cards:
        cards.append('<p class="note">尚未形成假设矩阵。</p>')
    return f"""
    <section id="hypothesis-matrix" class="level-frame investment-workbench">
      <p class="eyebrow">Hypothesis Matrix</p>
      <h2>假设、证据、反证和触发器</h2>
      <p class="subtitle-small">每条投资线索必须先是一条可证伪假设，再映射到标的，而不是直接从主题跳到股票。</p>
      <div class="hypothesis-stack">{''.join(cards)}</div>
    </section>
    """


def _render_target_mapping(rows: list[dict[str, Any]]) -> str:
    cards = []
    for row in rows:
        cards.append(
            f"""
            <article class="target-card tier-{escape(_safe_css_token(row.get("tier", "")))}">
              <div class="target-tier">{escape(str(row.get("tier", "")))}</div>
              <h3>{escape(str(row.get("target_type", "")))}</h3>
              <p>{escape(str(row.get("mapping_logic", "")))}</p>
              <div class="target-action">{escape(str(row.get("research_action", "")))}</div>
              <div class="matrix-grid">
                {_render_labeled_list("需要验证的数据", row.get("required_data", []))}
                {_render_labeled_list("反证条件", row.get("disconfirming_tests", []))}
                {_render_labeled_list("来源依据", row.get("evidence_ids", []), chip=True)}
                {_render_labeled_list("关联假设", row.get("linked_hypotheses", []), chip=True)}
              </div>
              <p class="note">时间尺度：{escape(str(row.get("time_horizon", "")))}；建议性质：研究观察池，不是交易指令。</p>
            </article>
            """
        )
    if not cards:
        cards.append('<p class="note">尚未形成标的映射。</p>')
    return f"""
    <section id="target-mapping" class="level-frame investment-workbench">
      <p class="eyebrow">Target Mapping</p>
      <h2>投资标的映射和观察池</h2>
      <p class="subtitle-small">标的建议按“研究优先级”表达，只给观察、验证和排除规则，不输出买卖指令。</p>
      <div class="target-grid">{''.join(cards)}</div>
    </section>
    """


def _render_adversarial_review(rows: list[dict[str, Any]]) -> str:
    cards = []
    for row in rows:
        cards.append(
            f"""
            <article class="adversarial-card">
              <div class="card-head">
                <span>{escape(str(row.get("id", "")))}</span>
                <b>{escape(str(row.get("severity", "")))}</b>
              </div>
              <h3>{escape(str(row.get("challenge", "")))}</h3>
              <p>{escape(str(row.get("why_it_matters", "")))}</p>
              <div class="matrix-grid">
                {_render_labeled_list("需要补的证据", row.get("evidence_to_collect", []))}
                {_render_labeled_list("若成立的处理", row.get("if_true_action", []))}
              </div>
            </article>
            """
        )
    if not cards:
        cards.append('<p class="note">尚未形成 AI 反方质询。</p>')
    return f"""
    <section id="adversarial-review" class="level-frame investment-workbench">
      <p class="eyebrow">AI Adversarial Review</p>
      <h2>AI 反方质询清单</h2>
      <p class="subtitle-small">把 AI 用作反方分析师：专门攻击瓶颈是否真实、标的是否错配、市场是否已经定价。</p>
      <div class="hypothesis-stack">{''.join(cards)}</div>
    </section>
    """


def _render_tracking_triggers(rows: list[dict[str, Any]]) -> str:
    table_rows = []
    for row in rows:
        table_rows.append(
            "<tr>"
            f"<td>{escape(str(row.get('trigger', '')))}</td>"
            f"<td>{escape(str(row.get('why_it_matters', '')))}</td>"
            f"<td>{escape(str(row.get('update_rule', '')))}</td>"
            f"<td>{escape(str(row.get('owner_view', '')))}</td>"
            "</tr>"
        )
    body = "".join(table_rows) or '<tr><td colspan="4">尚未定义跟踪触发器。</td></tr>'
    return f"""
    <section id="tracking-triggers" class="level-frame investment-workbench">
      <p class="eyebrow">Tracking</p>
      <h2>后续跟踪触发器</h2>
      <table>
        <thead><tr><th>触发器</th><th>为什么重要</th><th>更新规则</th><th>投研动作</th></tr></thead>
        <tbody>{body}</tbody>
      </table>
    </section>
    """


def _render_labeled_list(label: str, values: Any, chip: bool = False) -> str:
    items = _as_text_list(values)
    if chip:
        body = _render_path_chips(items) or '<span class="note">待补</span>'
    else:
        body = "<ul>" + "".join(f"<li>{escape(item)}</li>" for item in items[:6]) + "</ul>" if items else '<p class="note">待补</p>'
    return f'<div class="matrix-box"><b>{escape(label)}</b>{body}</div>'


def _render_path_chips(values: Any) -> str:
    return "".join(f"<span>{escape(item)}</span>" for item in _as_text_list(values)[:10])


def _safe_css_token(value: Any) -> str:
    text = str(value).strip().lower()
    if text.startswith("a"):
        return "a"
    if text.startswith("b"):
        return "b"
    if text.startswith("c"):
        return "c"
    if text.startswith("d"):
        return "d"
    return "".join(ch.lower() if ch.isascii() and ch.isalnum() else "-" for ch in text).strip("-") or "default"


def _investment_workbench_css() -> str:
    return """
    body {
      background: #f5f5f7;
      color: var(--ink);
    }
    header {
      padding: clamp(38px, 5.5vw, 70px) clamp(20px, 6vw, 82px) 28px;
      background: linear-gradient(180deg, #ffffff 0%, #f8f8fa 68%, #f5f5f7 100%);
      border-bottom: 1px solid rgba(0, 0, 0, .06);
    }
    header h1 {
      max-width: 1020px;
      font-size: clamp(34px, 5vw, 62px);
      line-height: 1.04;
      letter-spacing: 0;
    }
    header .subtitle {
      max-width: 760px;
      color: var(--muted);
      font-size: clamp(16px, 1.55vw, 20px);
    }
    nav {
      position: sticky;
      top: 0;
      z-index: 20;
      justify-content: center;
      padding: 10px 16px;
      background: rgba(245, 245, 247, .82);
      border-bottom: 1px solid rgba(0, 0, 0, .07);
      backdrop-filter: saturate(180%) blur(18px);
    }
    nav a {
      border: 1px solid rgba(0, 0, 0, .08);
      background: rgba(255, 255, 255, .72);
      color: #1d1d1f;
      font-weight: 700;
    }
    nav a:hover {
      color: var(--blue);
      border-color: rgba(0, 102, 204, .32);
      background: #fff;
    }
    .qa-full-research {
      width: min(1180px, calc(100% - 32px));
      margin: 24px auto 72px;
      display: grid;
      gap: 24px;
    }
    .qa-target-section,
    .qa-split-section,
    .qa-l1-section,
    .execution-plan-section {
      padding: clamp(22px, 3.5vw, 38px);
      background: rgba(255, 255, 255, .96);
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      box-shadow: 0 12px 34px rgba(0, 0, 0, .045);
    }
    .qa-target-section {
      display: grid;
      gap: 18px;
    }
    .execution-plan-section {
      scroll-margin-top: 76px;
    }
    .qa-section-title {
      display: grid;
      gap: 8px;
      padding-bottom: 18px;
      margin-bottom: 6px;
      border-bottom: 1px solid rgba(0, 0, 0, .08);
    }
    .qa-section-title .eyebrow {
      margin: 0;
      color: #1d1d1f;
      font-size: clamp(28px, 3.8vw, 46px);
      font-weight: 800;
      line-height: 1.08;
      letter-spacing: 0;
      text-transform: none;
    }
    .qa-section-title h2 {
      max-width: 980px;
      margin: 0;
      color: #424245;
      font-size: clamp(20px, 2.5vw, 30px);
      font-weight: 700;
      line-height: 1.22;
    }
    .qa-target-answer {
      max-width: 920px;
      margin: 0;
      color: #333336;
      font-size: clamp(16px, 1.6vw, 20px);
      line-height: 1.75;
    }
    .qa-direction-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin-top: 18px;
    }
    .deepseek-role {
      margin: 18px 0;
      padding: 16px;
      border: 1px solid rgba(0, 102, 204, .18);
      border-radius: 8px;
      background: #f5f9ff;
    }
    .deepseek-role b {
      display: block;
      margin-bottom: 6px;
      color: #0066cc;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .04em;
    }
    .deepseek-role p {
      margin: 0;
      color: #333336;
      line-height: 1.7;
    }
    .execution-stage-stack {
      display: grid;
      gap: 14px;
      margin-top: 16px;
    }
    .execution-stage-card {
      padding: clamp(16px, 2.4vw, 24px);
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      background: #fff;
      box-shadow: 0 8px 24px rgba(0, 0, 0, .04);
    }
    .stage-head {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      margin-bottom: 8px;
    }
    .stage-head span {
      display: inline-flex;
      padding: 5px 9px;
      border-radius: 999px;
      color: #0066cc;
      background: #eef5ff;
      font-size: 12px;
      font-weight: 800;
    }
    .stage-head strong {
      font-size: clamp(18px, 2vw, 24px);
      line-height: 1.25;
    }
    .execution-stage-card > p {
      max-width: 980px;
      margin: 0 0 14px;
      color: #424245;
      line-height: 1.7;
    }
    .execution-stage-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
    }
    .execution-stage-grid > div {
      min-width: 0;
      padding: 12px;
      border: 1px solid rgba(0, 0, 0, .07);
      border-radius: 8px;
      background: #fbfbfd;
    }
    .execution-stage-grid b {
      display: block;
      margin-bottom: 7px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .04em;
    }
    .execution-stage-grid ul {
      margin: 0;
      padding-left: 18px;
    }
    .execution-stage-grid li {
      margin: 4px 0;
      font-size: 13px;
      line-height: 1.55;
    }
    .qa-direction-link {
      display: grid;
      grid-template-columns: auto minmax(0, 1fr);
      gap: 8px 12px;
      align-items: start;
      min-width: 0;
      padding: 16px;
      color: var(--ink);
      text-decoration: none;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      background: #fff;
      transition: border-color .16s ease, background .16s ease, transform .16s ease;
    }
    .qa-direction-link:hover {
      border-color: rgba(0, 102, 204, .36);
      background: #f5f9ff;
      text-decoration: none;
      transform: translateY(-1px);
    }
    .qa-direction-link span {
      display: inline-flex;
      color: var(--blue);
      font-size: 13px;
      font-weight: 800;
      letter-spacing: .04em;
    }
    .qa-direction-link strong {
      min-width: 0;
      overflow-wrap: anywhere;
      font-size: 16px;
      line-height: 1.45;
    }
    .qa-direction-link em {
      grid-column: 2;
      color: var(--muted);
      font-size: 12px;
      font-style: normal;
      font-weight: 800;
    }
    .qa-l1-section {
      overflow: hidden;
      scroll-margin-top: 76px;
    }
    .qa-l1-section summary,
    .qa-l3-card summary {
      cursor: pointer;
      list-style: none;
    }
    .qa-l1-section summary::-webkit-details-marker,
    .qa-l3-card summary::-webkit-details-marker {
      display: none;
    }
    .qa-l1-section summary::after,
    .qa-l2-card summary::after,
    .qa-l3-card summary::after {
      content: "收起";
      justify-self: end;
      align-self: center;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      white-space: nowrap;
    }
    .qa-l1-section:not([open]) summary::after,
    .qa-l2-card:not([open]) summary::after,
    .qa-l3-card:not([open]) summary::after {
      content: "展开";
      color: var(--blue);
    }
    .qa-root-card,
    .qa-conclusion-card,
    .qa-side-card,
    .qa-l2-card,
    .qa-l3-card,
    .qa-workbench-mini {
      min-width: 0;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      background: #fff;
      box-shadow: 0 8px 24px rgba(0, 0, 0, .04);
    }
    .qa-root-card {
      padding: clamp(18px, 3vw, 28px);
      background: #111820;
      color: #fff;
    }
    .qa-root-card h3,
    .qa-root-card p {
      color: #fff;
    }
    .qa-metric-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin: 16px 0;
    }
    .qa-metric {
      padding: 14px;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      background: #f8f8fa;
    }
    .qa-metric span,
    .qa-level-head span,
    .qa-l2-card summary span,
    .qa-l3-head span {
      display: inline-flex;
      color: var(--blue);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .04em;
    }
    .qa-metric strong {
      display: block;
      margin-top: 6px;
      color: var(--ink);
      font-size: clamp(22px, 2.4vw, 32px);
      line-height: 1.1;
    }
    .qa-level-head {
      display: grid;
      grid-template-columns: auto minmax(0, 1fr) auto auto;
      gap: 14px;
      align-items: center;
      padding: 0 0 20px;
      margin-bottom: 18px;
      border-bottom: 1px solid rgba(0, 0, 0, .07);
    }
    .qa-level-head span {
      align-items: center;
      min-height: 36px;
      padding: 7px 11px;
      border-radius: 999px;
      background: #eef5ff;
      font-size: 16px;
    }
    .qa-level-head h2 {
      max-width: 980px;
      margin: 0;
      min-width: 0;
      font-size: clamp(24px, 3.2vw, 38px);
      line-height: 1.16;
    }
    .qa-level-head em {
      color: var(--muted);
      font-size: 12px;
      font-style: normal;
      font-weight: 800;
      white-space: nowrap;
    }
    .qa-l1-body {
      display: grid;
      gap: 16px;
    }
    .qa-l1-layout {
      display: grid;
      grid-template-columns: minmax(0, 1.3fr) minmax(280px, .7fr);
      gap: 14px;
      align-items: start;
    }
    .qa-conclusion-card,
    .qa-side-card {
      padding: clamp(16px, 2.5vw, 24px);
    }
    .qa-conclusion-card {
      background: #f5f8ff;
      border-color: #d6e6ff;
    }
    .qa-conclusion-card b,
    .qa-mini-list b {
      display: block;
      margin-bottom: 8px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .04em;
    }
    .qa-workbench-row {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
      margin: 14px 0;
    }
    .qa-workbench-mini {
      padding: 13px;
      background: #fbfbfd;
    }
    .qa-workbench-mini b {
      display: block;
      margin-bottom: 6px;
      color: var(--blue);
      font-size: 12px;
      font-weight: 800;
    }
    .qa-workbench-mini ul,
    .qa-mini-list ul {
      margin: 0;
      padding-left: 18px;
    }
    .qa-workbench-mini li,
    .qa-mini-list li {
      margin: 4px 0;
      font-size: 13px;
    }
    .qa-l2-stack {
      display: grid;
      gap: 12px;
      margin-top: 16px;
    }
    .qa-l2-card {
      overflow: hidden;
    }
    .qa-l2-card summary {
      display: grid;
      grid-template-columns: auto minmax(0, 1fr) auto auto;
      gap: 10px;
      align-items: center;
      padding: 15px 16px;
      cursor: pointer;
      list-style: none;
      background: #f8f8fa;
    }
    .qa-l2-card summary::-webkit-details-marker {
      display: none;
    }
    .qa-l2-card summary strong {
      min-width: 0;
      overflow-wrap: anywhere;
      color: var(--ink);
      font-size: clamp(17px, 1.8vw, 21px);
      line-height: 1.35;
    }
    .qa-l2-card summary em,
    .qa-l3-head b {
      justify-self: end;
      color: var(--muted);
      font-size: 12px;
      font-style: normal;
      font-weight: 800;
      white-space: nowrap;
    }
    .qa-l2-body {
      padding: 16px;
    }
    .qa-l2-answer {
      margin-bottom: 12px;
      padding: 14px;
      border: 1px solid rgba(0, 0, 0, .07);
      border-radius: 8px;
      background: #fff;
    }
    .qa-l2-answer b {
      display: block;
      margin-bottom: 7px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
    }
    .qa-l3-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }
    .qa-l3-card {
      padding: 0;
      box-shadow: none;
      overflow: hidden;
    }
    .qa-l3-head {
      display: grid;
      grid-template-columns: auto minmax(0, 1fr) auto auto;
      gap: 10px;
      align-items: center;
      padding: 13px 14px;
      background: #fbfbfd;
    }
    .qa-l3-head strong {
      min-width: 0;
      overflow-wrap: anywhere;
      color: var(--ink);
      font-size: 15px;
      line-height: 1.45;
    }
    .qa-l3-body {
      padding: 0 14px 14px;
    }
    .qa-l3-card p {
      color: var(--ink);
      font-size: 13px;
      margin-top: 12px;
    }
    .qa-l3-columns {
      display: grid;
      gap: 8px;
      margin-top: 10px;
    }
    .qa-mini-list {
      padding-top: 9px;
      border-top: 1px solid rgba(0, 0, 0, .07);
    }
    .qa-source-list {
      margin-top: 12px;
      padding-top: 10px;
      border-top: 1px solid rgba(0, 0, 0, .07);
    }
    .qa-source-list b {
      display: block;
      margin-bottom: 8px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .04em;
    }
    .qa-source-list ul {
      display: grid;
      gap: 9px;
      margin: 0;
      padding: 0;
      list-style: none;
    }
    .qa-source-list li {
      display: grid;
      gap: 4px;
      padding: 10px;
      border: 1px solid rgba(0, 0, 0, .06);
      border-radius: 8px;
      background: #fbfbfd;
    }
    .qa-source-list a,
    .target-source-links a {
      color: var(--blue);
      font-weight: 800;
      text-decoration: none;
    }
    .qa-source-list a:hover,
    .target-source-links a:hover {
      text-decoration: underline;
    }
    .qa-source-list p {
      margin: 0;
      color: #424245;
      font-size: 12px;
      line-height: 1.55;
    }
    .source-chip {
      width: max-content;
      padding: 3px 7px;
      border-radius: 999px;
      color: #0066cc;
      background: #eef5ff;
      font-size: 11px;
      font-weight: 800;
    }
    .workbench-appendix {
      background: #111820;
      color: #fff;
    }
    .workbench-appendix h2,
    .workbench-appendix p {
      color: #fff;
    }
    .markdown-report { scroll-margin-top: 70px; }
    .subtitle-small {
      max-width: 920px;
      color: var(--muted);
      font-size: 16px;
      line-height: 1.65;
    }
    .investment-workbench {
      background: rgba(255, 255, 255, .94);
    }
    .workbench-grid,
    .target-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-top: 16px;
    }
    .workbench-card,
    .hypothesis-card,
    .target-card,
    .chain-card,
    .adversarial-card,
    .gate-box {
      min-width: 0;
      padding: clamp(16px, 2.4vw, 24px);
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      background: #fff;
      box-shadow: 0 10px 30px rgba(0, 0, 0, .05);
    }
    .workbench-card span,
    .card-head span,
    .target-tier {
      display: inline-flex;
      margin-bottom: 10px;
      padding: 4px 8px;
      border-radius: 999px;
      background: #eef5ff;
      color: var(--blue);
      font-size: 12px;
      font-weight: 800;
    }
    .gate-box {
      margin-top: 14px;
      background: #111820;
      color: #fff;
    }
    .gate-box b,
    .gate-box li {
      color: #fff;
    }
    .hypothesis-stack {
      display: grid;
      gap: 14px;
      margin-top: 16px;
    }
    .chain-stack {
      display: grid;
      gap: 12px;
      margin-top: 16px;
    }
    .chain-card {
      border-left: 4px solid var(--blue);
    }
    .adversarial-card {
      border-left: 4px solid var(--red);
      background: #fffafa;
    }
    .card-head {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
    }
    .card-head b,
    .target-action {
      display: inline-flex;
      padding: 5px 9px;
      border-radius: 999px;
      color: var(--green);
      background: #f0fbf4;
      font-size: 12px;
      font-weight: 800;
    }
    .matrix-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
      margin-top: 12px;
    }
    .matrix-box {
      min-width: 0;
      padding: 12px;
      border: 1px solid rgba(0, 0, 0, .07);
      border-radius: 8px;
      background: #f8f8fa;
    }
    .matrix-box b {
      display: block;
      margin-bottom: 7px;
      color: var(--muted);
      font-size: 12px;
      letter-spacing: .04em;
    }
    .matrix-box ul {
      margin: 0;
      padding-left: 18px;
    }
    .matrix-box li {
      margin: 3px 0;
      font-size: 13px;
    }
    .target-card {
      border-top: 4px solid var(--blue);
    }
    .target-card.tier-a { border-top-color: var(--green); }
    .target-card.tier-b { border-top-color: var(--blue); }
    .target-card.tier-c { border-top-color: var(--amber); }
    .target-card.tier-d { border-top-color: var(--red); }
    .target-action {
      margin: 8px 0 2px;
      color: var(--blue);
      background: #eef5ff;
    }
    .target-recommendations {
      padding: clamp(22px, 3.5vw, 38px);
      background: rgba(255, 255, 255, .96);
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      box-shadow: 0 12px 34px rgba(0, 0, 0, .045);
      scroll-margin-top: 76px;
    }
    .recommendation-stack {
      display: grid;
      gap: 12px;
      margin-top: 18px;
    }
    .recommendation-card {
      min-width: 0;
      padding: clamp(16px, 2.4vw, 24px);
      border: 1px solid rgba(0, 0, 0, .08);
      border-left: 4px solid var(--blue);
      border-radius: 8px;
      background: #fff;
      box-shadow: 0 8px 24px rgba(0, 0, 0, .04);
    }
    .recommendation-card.tier-a { border-left-color: var(--green); }
    .recommendation-card.tier-b { border-left-color: var(--blue); }
    .recommendation-card.tier-c { border-left-color: var(--amber); }
    .recommendation-card.tier-d { border-left-color: var(--red); }
    .recommendation-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      margin-bottom: 10px;
    }
    .recommendation-head span,
    .recommendation-head b {
      display: inline-flex;
      align-items: center;
      min-height: 26px;
      padding: 4px 9px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 800;
    }
    .recommendation-head span {
      color: var(--blue);
      background: #eef5ff;
    }
    .recommendation-head b {
      color: #1d1d1f;
      background: #f5f5f7;
    }
    .recommendation-card h3 {
      margin: 0 0 12px;
      font-size: clamp(20px, 2.4vw, 28px);
      line-height: 1.2;
    }
    .recommendation-grid {
      display: grid;
      grid-template-columns: 1.4fr .8fr 1fr 1fr;
      gap: 12px;
    }
    .recommendation-grid > div {
      min-width: 0;
      padding: 13px;
      border: 1px solid rgba(0, 0, 0, .07);
      border-radius: 8px;
      background: #fbfbfd;
    }
    .recommendation-grid b {
      display: block;
      margin-bottom: 7px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .04em;
    }
    .recommendation-grid p,
    .recommendation-grid li {
      font-size: 13px;
      line-height: 1.6;
    }
    .recommendation-grid ul {
      margin: 0;
      padding-left: 18px;
    }
    .recommendation-action {
      margin-top: 8px;
      color: #0066cc;
      font-weight: 700;
    }
    .target-source-links {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 12px;
    }
    .target-source-links span {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      max-width: 100%;
      padding: 7px 9px;
      border-radius: 999px;
      background: #f5f9ff;
      border: 1px solid rgba(0, 102, 204, .18);
      font-size: 12px;
    }
    .target-source-links small {
      color: var(--muted);
      font-weight: 800;
    }
    .specific-target-title {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: baseline;
      margin-bottom: 6px;
    }
    .specific-target-title h3 {
      margin: 0;
    }
    .specific-target-title strong {
      color: var(--blue);
      font-size: 14px;
      font-weight: 800;
    }
    .target-node {
      margin: 0 0 14px;
      color: #424245;
      font-size: 14px;
      font-weight: 700;
    }
    .specific-target-grid {
      grid-template-columns: 1.3fr 1fr 1fr 1fr;
    }
    .score-table td,
    .score-table th {
      font-size: 13px;
    }
    .score-table td:first-child {
      min-width: 180px;
    }
    #full-report { scroll-margin-top: 70px; }
    @media (max-width: 900px) {
      .workbench-grid,
      .target-grid,
      .matrix-grid,
      .qa-metric-grid,
      .qa-l1-layout,
      .qa-workbench-row,
      .qa-l3-grid,
      .recommendation-grid,
      .execution-stage-grid {
        grid-template-columns: 1fr;
      }
      .qa-level-head,
      .qa-l2-card summary,
      .qa-l3-head {
        grid-template-columns: 1fr;
      }
      .qa-l1-section summary::after,
      .qa-l2-card summary::after,
      .qa-l3-card summary::after {
        justify-self: start;
      }
      .qa-level-head em,
      .qa-l2-card summary em,
      .qa-l3-head b {
        justify-self: start;
        white-space: normal;
      }
    }
    """


def _markdown_to_html(markdown: str) -> str:
    html: list[str] = []
    in_list = False
    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            if in_list:
                html.append("</ul>")
                in_list = False
            continue
        if line.startswith("# "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h2>{escape(line[2:].strip())}</h2>")
        elif line.startswith("## "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h3>{escape(line[3:].strip())}</h3>")
        elif line.startswith("### "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h4>{escape(line[4:].strip())}</h4>")
        elif line.startswith("- "):
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"<li>{escape(line[2:].strip())}</li>")
        else:
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<p>{escape(line)}</p>")
    if in_list:
        html.append("</ul>")
    return "\n".join(html)


def _root_node(nodes: list[dict[str, Any]]) -> dict[str, Any]:
    for node in nodes:
        if node.get("parent_id") in {None, ""}:
            return node
    return nodes[0] if nodes else {}


def _descendant_nodes(node: dict[str, Any], nodes_by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    descendants: list[dict[str, Any]] = []
    stack = list(node.get("next_question_ids", []) or [])
    seen: set[str] = set()
    while stack:
        node_id = str(stack.pop(0))
        if node_id in seen:
            continue
        seen.add(node_id)
        child = nodes_by_id.get(node_id)
        if child is None:
            continue
        descendants.append(child)
        stack.extend(child.get("next_question_ids", []) or [])
    return descendants


def _is_leaf_node(qa_tree: dict[str, Any], node: dict[str, Any]) -> bool:
    return int(node.get("level", 0)) >= int(qa_tree.get("default_depth", 3)) or not node.get("next_question_ids")


def _evidence_counts(nodes: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"evidence": 0, "research_report": 0, "message": 0, "opinion": 0}
    for node in nodes:
        for category in counts:
            counts[category] += len(node.get("evidence_buckets", {}).get(category, []))
    return counts


def _node_evidence_counts(node: dict[str, Any]) -> dict[str, int]:
    buckets = node.get("evidence_buckets", {})
    return {category: len(buckets.get(category, [])) for category in ["evidence", "research_report", "message", "opinion"]}


def _priority_gaps(nodes: list[dict[str, Any]]) -> list[str]:
    values: list[str] = []
    for node in nodes:
        for gap in _compact_node(node).get("gaps", []):
            line = f"{node.get('question', '')}：{gap}"
            if line not in values:
                values.append(line)
    return values


def _as_text_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def _truncate(text: Any, limit: int) -> str:
    cleaned = str(text).strip()
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[: max(0, limit - 1)]}..."


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_optional_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data
