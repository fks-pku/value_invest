from __future__ import annotations

from typing import Any

from value_invest_research.adapters.outbound.report_sections.base import ReportRenderContext
from value_invest_research.adapters.outbound.report_sections.shared import _e


class QaSection:
    section_id = "qa"

    def render(self, context: ReportRenderContext) -> str:
        return _render_qa(context.data["qa_roots"])


def _render_qa(roots: list[dict[str, Any]]) -> str:
    cards = "\n".join(_render_qa_card(node) for node in roots)
    return f"""
<section id="qa" class="section qa-section">
  <div class="section-heading">
    <span class="section-kicker">03</span>
    <h2>下钻 QA</h2>
  </div>
  <div class="qa-stack">{cards}</div>
</section>
""".strip()


def _render_qa_card(node: dict[str, Any]) -> str:
    level = int(node.get("level") or 1)
    children = node.get("children") or []
    node_id = str(node.get("id", ""))
    child_cards = "\n".join(_render_qa_card(child) for child in children)
    child_summary = child_cards or '<p class="muted">已到当前最深研究单元，下一步通过来源更新和季度触发器继续验证。</p>'
    conclusion = _node_conclusion(node)
    gap_text = _gap_text(node)
    metadata = _l3_metadata(node) if level >= 3 else ""
    source_links = _source_links(node.get("source_index") or [])
    artifact = _artifact_card(node) if level >= 3 else f'<div class="artifact-card"><p>{_e(conclusion)}</p></div>'
    return f"""
<details id="{_id(node_id)}" class="qa-card level-{level}" open>
  <summary>
    <span class="qid">{_e(node_id)}</span>
    <span class="question">{_e(str(node.get("question", "")))}</span>
    <span class="qa-count">{len(children)} 个子问题</span>
    <span class="chevron">›</span>
  </summary>
  <div class="qa-body">
    <div class="qa-block">
      <p class="block-title">1. 当前结论呈现</p>
      {metadata}
      {artifact}
      {source_links}
    </div>
    <div class="qa-block">
      <p class="block-title">2. 问题展开（子 QA）</p>
      <div class="child-stack">{child_summary}</div>
    </div>
    <div class="qa-block">
      <p class="block-title">3. 待补充的问题</p>
      <p>{_e(gap_text)}</p>
    </div>
  </div>
</details>
""".strip()


def _node_conclusion(node: dict[str, Any]) -> str:
    return str(node.get("conclusion") or node.get("judgment") or node.get("fact") or "该层结论等待子问题继续补充。")


def _gap_text(node: dict[str, Any]) -> str:
    gap = str(node.get("gap") or "").strip()
    trigger = str(node.get("trigger") or "").strip()
    if gap and trigger:
        return f"{gap} 触发器：{trigger}"
    if gap:
        return gap
    if trigger:
        return f"触发器：{trigger}"
    return "继续补齐一手数据、反证来源、估值口径和季度监控阈值。"


def _l3_metadata(node: dict[str, Any]) -> str:
    return f"""
<div class="l3-meta">
  <span class="l3-skill">技能：{_e(str(node.get("skill", "")))}</span>
  <span class="l3-execution-status">状态：{_e(str(node.get("execution_status", "")))}</span>
  <span class="l3-score-component">评分：{_e(str(node.get("score_component", "")))}</span>
  <span class="l3-decision-use">用途：{_e(str(node.get("decision_use", "")))}</span>
</div>
""".strip()


def _artifact_card(node: dict[str, Any]) -> str:
    rendered_artifacts = _render_node_artifacts(node.get("artifact"))
    return f"""
<div class="artifact-card l3-artifact">
  {rendered_artifacts}
  <dl>
    <div><dt>事实</dt><dd>{_e(str(node.get("fact", "")))}</dd></div>
    <div><dt>推论</dt><dd>{_e(str(node.get("inference", "")))}</dd></div>
    <div><dt>判断</dt><dd>{_e(str(node.get("judgment", "")))}</dd></div>
    <div><dt>缺口</dt><dd>{_e(str(node.get("gap", "")))}</dd></div>
    <div><dt>触发器</dt><dd>{_e(str(node.get("trigger", "")))}</dd></div>
  </dl>
</div>
""".strip()


def _render_node_artifacts(artifact: Any) -> str:
    if not isinstance(artifact, dict):
        return ""
    tables = artifact.get("tables")
    if not isinstance(tables, list):
        tables = [artifact] if artifact.get("columns") and artifact.get("rows") else []
    return "\n".join(_render_artifact_table(table) for table in tables if isinstance(table, dict))


def _render_artifact_table(table: dict[str, Any]) -> str:
    columns = [str(column) for column in table.get("columns", []) if str(column)]
    rows = table.get("rows", [])
    if not columns or not isinstance(rows, list):
        return ""
    header = "".join(f"<th>{_e(column)}</th>" for column in columns)
    body_rows = []
    for row in rows:
        if isinstance(row, dict):
            cells = [row.get(column, "") for column in columns]
        elif isinstance(row, list):
            cells = row
        else:
            continue
        body_rows.append("<tr>" + "".join(f"<td>{_e(str(cell))}</td>" for cell in cells) + "</tr>")
    if not body_rows:
        return ""
    title = str(table.get("title") or "")
    title_html = f'<p class="artifact-title">{_e(title)}</p>' if title else ""
    return f"""
<div class="artifact-table-wrap">
  {title_html}
  <table class="artifact-table">
    <thead><tr>{header}</tr></thead>
    <tbody>{''.join(body_rows)}</tbody>
  </table>
</div>
""".strip()


def _source_links(sources: list[dict[str, Any]]) -> str:
    if not sources:
        return ""
    links = []
    for source in sources:
        title = source.get("title") or source.get("source_id") or source.get("id") or "source"
        url = str(source.get("url", ""))
        if url:
            links.append(f'<a href="{_e(url)}" target="_blank" rel="noreferrer">{_e(str(title))}</a>')
        else:
            links.append(_e(str(title)))
    return '<p class="source-links">来源：' + " / ".join(links) + "</p>"


def _id(value: str) -> str:
    return value.lower().replace(".", "-").replace("_", "-")
