from __future__ import annotations

import json
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any

from value_invest_research.research_system import _apple_research_css, _qa_explorer_css


PROFESSIONAL_REPORT_MD = "professional_report.md"
PROFESSIONAL_REPORT_HTML = "professional_report.html"


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
    markdown = _professional_report_markdown(context, client)
    md_path, html_path = _write_report_files(research_dir, markdown, title=f"{normalized} 专业投研报告")
    return {
        **build_result,
        "ticker": normalized,
        "professional_report_path": str(html_path),
        "professional_report_md_path": str(md_path),
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
    markdown = _professional_report_markdown(context, client)
    md_path, html_path = _write_report_files(project_dir, markdown, title=title)
    return {
        **rebuild_result,
        "professional_report_path": str(html_path),
        "professional_report_md_path": str(md_path),
        "report_mode": "llm" if client is not None else "deterministic",
        "sections": len(context["top_level"]),
        "leaf_questions": len(context["leaf_nodes"]),
    }


def _professional_report_markdown(context: dict[str, Any], client: Any | None) -> str:
    if client is None:
        return _deterministic_report_markdown(context)
    response = client.chat(_llm_report_system_prompt(), _llm_report_user_prompt(context))
    text = str(response).strip()
    if not text:
        return _deterministic_report_markdown(context)
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
        "leaf_nodes": [_compact_node(node) for node in leaf_nodes],
        "top_level": top_sections,
        "evidence_counts": evidence_counts,
        "priority_gaps": priority_gaps,
        "root_answer": root.get("current_answer", ""),
        "root_judgment": root.get("synthesis", {}).get("judgment", ""),
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
        "leaf_nodes": [_compact_node(child) for child in leaf_nodes[:16]],
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
        "source_balance": answer.get("source_balance", ""),
        "evidence_counts": _node_evidence_counts(node),
    }


def _deterministic_report_markdown(context: dict[str, Any]) -> str:
    title = f"{context['object_id'] or context['object_type']} 专业投研报告"
    top_judgments = _top_judgment_lines(context)
    section_blocks = "\n\n".join(_section_markdown(section) for section in context["top_level"])
    gap_lines = "\n".join(f"- {gap}" for gap in context["priority_gaps"][:8]) or "- 暂无明确缺口，但仍需持续补充一手证据、研报和反证信息。"
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
    buckets = node.get("evidence_buckets", {})
    for category in ("evidence", "research_report", "message", "opinion"):
        for item in buckets.get(category, []) or []:
            if item.get("missing_record"):
                continue
            summary = str(item.get("summary") or item.get("point") or "").strip()
            if not summary:
                continue
            source = str(item.get("source_name") or "").strip()
            evidence_id = str(item.get("evidence_id") or "").strip()
            label = f"{source}：" if source else ""
            suffix = f" [{evidence_id}]" if evidence_id else ""
            lines.append(f"{label}{summary}{suffix}")
    return lines


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


def _llm_report_user_prompt(context: dict[str, Any]) -> str:
    compact = {
        "object_type": context["object_type"],
        "object_id": context["object_id"],
        "meta_question": context["meta_question"],
        "evidence_counts": context["evidence_counts"],
        "top_level": context["top_level"],
        "priority_gaps": context["priority_gaps"],
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
            "4. 反证条件",
            "5. 信息缺口和下一步数据",
            "6. 使用边界",
            "",
            "要求：每个重要判断都要回到 QA 节点、事实/推论/判断/缺口或来源结构；不要输出交易建议。",
        ]
    )


def _write_report_files(container_dir: Path, markdown: str, title: str) -> tuple[Path, Path]:
    md_path = container_dir / PROFESSIONAL_REPORT_MD
    html_path = container_dir / PROFESSIONAL_REPORT_HTML
    md_path.write_text(markdown.rstrip() + "\n", encoding="utf-8")
    html_path.write_text(_markdown_report_html(markdown, title), encoding="utf-8")
    return md_path, html_path


def _markdown_report_html(markdown: str, title: str) -> str:
    body = _markdown_to_html(markdown)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>{_apple_research_css()}{_qa_explorer_css()}</style>
</head>
<body>
  <header>
    <p class="eyebrow">Professional Research Report</p>
    <h1>{escape(title)}</h1>
    <p class="subtitle">由层级 QA 树、四类信息索引和节点答案收敛生成；不是交易建议。</p>
  </header>
  <main class="qa-full-research">
    <section class="level-frame markdown-report">
      {body}
    </section>
  </main>
</body>
</html>
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
