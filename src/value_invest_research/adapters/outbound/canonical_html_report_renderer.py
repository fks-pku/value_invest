from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from value_invest_research.domain.report_view_model import ReportViewModel


class CanonicalHtmlReportRenderer:
    """HTML adapter for the locked research-goal report presentation contract."""

    def render(self, view_model: ReportViewModel) -> str:
        data = view_model.to_dict()
        title = str(data["project"].get("title") or data["goal"].get("topic") or "专业投研报告")
        return "\n".join(
            [
                "<!doctype html>",
                '<html lang="zh-CN">',
                "<head>",
                '<meta charset="utf-8">',
                '<meta name="viewport" content="width=device-width, initial-scale=1">',
                f"<title>{_e(title)}</title>",
                "<style>",
                _css(),
                "</style>",
                "</head>",
                "<body>",
                _render_hero(data),
                _render_goal(data),
                _render_chain(data["supply_chain"]),
                _render_qa(data["qa_roots"]),
                _render_targets(data["targets"], data["project"]),
                _render_sources(data["sources"]),
                "</body>",
                "</html>",
            ]
        )

    def write(
        self,
        project_dir: Path,
        view_model: ReportViewModel,
        *,
        filename: str = "professional_report.html",
    ) -> dict[str, Any]:
        project_dir.mkdir(parents=True, exist_ok=True)
        html = self.render(view_model)
        output_path = project_dir / filename
        output_path.write_text(html, encoding="utf-8")
        return {
            "project_id": view_model.project.get("project_id", ""),
            "report_path": str(output_path),
            "qa_roots": len(view_model.qa_roots),
            "targets": len(view_model.targets),
            "sources": len(view_model.sources),
        }


def _render_hero(data: dict[str, Any]) -> str:
    project = data["project"]
    title = project.get("title") or data["goal"].get("topic") or "专业投研报告"
    report_date = project.get("report_date") or ""
    run_mode = project.get("run_mode") or ""
    return f"""
<header class="hero">
  <nav class="top-nav" aria-label="报告导航">
    <a href="#goal">当前研究目标</a>
    <a href="#chain">产业链全景</a>
    <a href="#qa">问题下钻</a>
    <a href="#targets">最终标的推荐</a>
    <a href="#sources">来源索引</a>
  </nav>
  <div class="hero-inner">
    <p class="eyebrow">Research Goal QA</p>
    <h1>{_e(str(title))}</h1>
    <p class="hero-subtitle">以产业链、问题下钻、反证和标的赔率为主线组织研究结论。</p>
    <div class="hero-meta">
      <span>{_e(str(report_date))}</span>
      <span>{_e(str(run_mode))}</span>
    </div>
  </div>
</header>
""".strip()


def _render_goal(data: dict[str, Any]) -> str:
    goal = data["goal"]
    return f"""
<main>
<section id="goal" class="section goal-section">
  <div class="section-heading">
    <span class="section-kicker">01</span>
    <h2>当前研究目标</h2>
  </div>
  <div class="goal-card">
    <div>
      <p class="label">研究对象</p>
      <p class="goal-main">{_e(str(goal.get("topic", "")))}</p>
    </div>
    <div>
      <p class="label">当前结论</p>
      <p>{_e(str(goal.get("current_judgment", "")))}</p>
    </div>
    <div>
      <p class="label">最大不确定性</p>
      <p>{_e(str(goal.get("biggest_uncertainty", "")))}</p>
    </div>
    <div>
      <p class="label">边界</p>
      <p>{_e(str(goal.get("decision_boundary", "")))}</p>
    </div>
  </div>
</section>
""".strip()


def _render_chain(chain: dict[str, Any]) -> str:
    layers = chain.get("layers") or []
    rows = "\n".join(
        f"""
      <tr>
        <td>{_e(str(layer.get("layer", "")))}</td>
        <td>{_e(str(layer.get("products", "")))}</td>
        <td>{_e(str(layer.get("players", "")))}</td>
        <td>{_e(str(layer.get("value_flow", "")))}</td>
      </tr>
""".rstrip()
        for layer in layers
    )
    cards = "\n".join(
        f"""
    <article class="chain-layer-card">
      <p class="label">{_e(str(layer.get("layer", "")))}</p>
      <h3>{_e(str(layer.get("products", "")))}</h3>
      <p>{_e(str(layer.get("value_flow", "")))}</p>
    </article>
""".rstrip()
        for layer in layers
    )
    steps = "\n".join(f"<li>{_e(str(step))}</li>" for step in chain.get("flow_steps") or [])
    return f"""
<section id="chain" class="section supply-chain-section">
  <div class="section-heading">
    <span class="section-kicker">02</span>
    <h2>产业链全景</h2>
  </div>
  <div class="chain-explain">
    <p class="chain-plain-summary">{_e(str(chain.get("plain_summary", "")))}</p>
    <ol class="chain-flow-steps">{steps}</ol>
    <div class="chain-layer-grid">{cards}</div>
    <div class="chain-map">
      <table class="chain-table">
        <thead>
          <tr><th>层级</th><th>产品/服务</th><th>关键玩家</th><th>价值/利润流</th></tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    <div class="chain-chokepoints"><strong>候选瓶颈：</strong>{_e(str(chain.get("chokepoints", "")))}</div>
    <div class="chain-target-links"><strong>标的映射：</strong>{_e(str(chain.get("target_links", "")))}</div>
  </div>
</section>
""".strip()


def _render_qa(roots: list[dict[str, Any]]) -> str:
    cards = "\n".join(_render_qa_card(node) for node in roots)
    return f"""
<section id="qa" class="section qa-section">
  <div class="section-heading">
    <span class="section-kicker">03</span>
    <h2>问题下钻</h2>
  </div>
  <div class="qa-stack">{cards}</div>
</section>
""".strip()


def _render_qa_card(node: dict[str, Any]) -> str:
    level = int(node.get("level") or 1)
    children = node.get("children") or []
    node_id = str(node.get("id", ""))
    child_cards = "\n".join(_render_qa_card(child) for child in children)
    child_summary = child_cards or '<p class="muted">已到 L3 叶子问题，下一步通过来源更新和季度触发器继续验证。</p>'
    conclusion = _node_conclusion(node)
    gap_text = _gap_text(node)
    metadata = _l3_metadata(node) if level == 3 else ""
    source_links = _source_links(node.get("source_index") or [])
    artifact = _artifact_card(node) if level == 3 else f'<div class="artifact-card"><p>{_e(conclusion)}</p></div>'
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


def _render_targets(targets: list[dict[str, Any]], project: dict[str, Any] | None = None) -> str:
    include_label = _include_target_labels(targets, project or {})
    rows = "\n".join(_target_row(target, include_label=include_label) for target in targets)
    if not rows:
        colspan = 13 if include_label else 8
        rows = f'<tr><td colspan="{colspan}">暂无可展示标的。</td></tr>'
    label_headers = (
        "<th>标签窗口</th><th>起点价</th><th>终点价</th><th>三个月涨幅</th><th>标签状态</th>"
        if include_label
        else ""
    )
    return f"""
<section id="targets" class="section target-section">
  <div class="section-heading">
    <span class="section-kicker">04</span>
    <h2>最终标的推荐</h2>
  </div>
  <p class="section-note">该表是研究观察清单，不是买卖指令；排序同时考虑瓶颈强度、未来空间、估值赔率和反证可控性。</p>
  <table class="target-table">
    <thead>
      <tr>
        <th>排序</th><th>标的</th><th>状态</th><th>强度</th><th>瓶颈节点</th><th>核心理由</th><th>赔率/空间</th><th>主要风险</th>{label_headers}
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</section>
""".strip()


def _render_sources(sources: list[dict[str, Any]]) -> str:
    rows = "\n".join(_source_row(source) for source in sources)
    if not rows:
        rows = '<tr><td colspan="5">暂无来源记录。</td></tr>'
    return f"""
<section id="sources" class="section source-section">
  <div class="section-heading">
    <span class="section-kicker">05</span>
    <h2>来源索引</h2>
  </div>
  <details class="source-collapse">
    <summary>展开来源索引</summary>
    <table class="source-table">
      <thead><tr><th>ID</th><th>类别</th><th>立场</th><th>摘要</th><th>链接</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </details>
</section>
</main>
""".strip()


def _target_row(target: dict[str, Any], *, include_label: bool = False) -> str:
    score = target.get("score") or {}
    action_state = str(target.get("action_state") or score.get("action_state") or "")
    target_label = f"{target.get('ticker', '')} {target.get('name', '')}".strip()
    strength = target.get("strength") or score.get("total_score") or ""
    label_cells = _target_label_cells(target) if include_label else ""
    return f"""
<tr>
  <td>{_e(str(target.get("rank", "")))}</td>
  <td>{_e(target_label)}</td>
  <td><span class="state-pill state-{_class_token(action_state)}">{_e(action_state)}</span></td>
  <td>{_e(str(strength))}</td>
  <td>{_e(str(target.get("chokepoint_node") or target.get("thesis_node") or ""))}</td>
  <td>{_e(str(target.get("rationale", "")))}</td>
  <td>{_e(str(target.get("future_space") or target.get("odds") or ""))}</td>
  <td>{_e(str(target.get("risks", "")))}</td>{label_cells}
</tr>
""".strip()


def _include_target_labels(targets: list[dict[str, Any]], project: dict[str, Any]) -> bool:
    if str(project.get("run_mode") or "") == "historical_backtest":
        return True
    return any(isinstance(target.get("label"), dict) for target in targets)


def _target_label_cells(target: dict[str, Any]) -> str:
    label = target.get("label") if isinstance(target.get("label"), dict) else {}
    start_date = label.get("start_date") or label.get("as_of_date") or ""
    end_date = label.get("end_date") or label.get("evaluation_date") or ""
    window = f"{start_date} → {end_date}" if start_date or end_date else label.get("label_window", "")
    return f"""
  <td>{_e(str(window))}</td>
  <td>{_e(_format_price(label.get("start_price")))}</td>
  <td>{_e(_format_price(label.get("end_price")))}</td>
  <td>{_e(_format_return(label.get("forward_3m_return")))}</td>
  <td>{_e(str(label.get("label_status") or "label_missing"))}</td>""".rstrip()


def _source_row(source: dict[str, Any]) -> str:
    url = str(source.get("url", ""))
    link = f'<a href="{_e(url)}" target="_blank" rel="noreferrer">打开</a>' if url else ""
    return f"""
<tr>
  <td>{_e(str(source.get("source_id") or source.get("id") or ""))}</td>
  <td>{_e(str(source.get("source_bucket") or source.get("information_category") or ""))}</td>
  <td>{_e(str(source.get("support_refute_or_lead") or ""))}</td>
  <td>{_e(str(source.get("summary") or source.get("title") or ""))}</td>
  <td>{link}</td>
</tr>
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
    return f"""
<div class="artifact-card l3-artifact">
  <dl>
    <div><dt>事实</dt><dd>{_e(str(node.get("fact", "")))}</dd></div>
    <div><dt>推论</dt><dd>{_e(str(node.get("inference", "")))}</dd></div>
    <div><dt>判断</dt><dd>{_e(str(node.get("judgment", "")))}</dd></div>
    <div><dt>缺口</dt><dd>{_e(str(node.get("gap", "")))}</dd></div>
    <div><dt>触发器</dt><dd>{_e(str(node.get("trigger", "")))}</dd></div>
  </dl>
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


def _class_token(value: str) -> str:
    token = value.strip().lower().replace(" ", "_")
    return token or "no_action"


def _format_price(value: Any) -> str:
    if value is None or value == "":
        return "未验证"
    try:
        return f"{float(value):,.2f}"
    except (TypeError, ValueError):
        return str(value)


def _format_return(value: Any) -> str:
    if value is None or value == "":
        return "未验证"
    try:
        return f"{float(value) * 100:.1f}%"
    except (TypeError, ValueError):
        return str(value)


def _e(value: str) -> str:
    return escape(value, quote=True)


def _css() -> str:
    return """
:root {
  color-scheme: light;
  --bg: #f5f7fb;
  --surface: rgba(255,255,255,.88);
  --surface-strong: #ffffff;
  --text: #1d1d1f;
  --muted: #667085;
  --line: #d9e0ea;
  --blue: #0a84ff;
  --green: #1d9a6c;
  --amber: #b7791f;
  --red: #c2413d;
  --shadow: 0 20px 60px rgba(20, 32, 54, .10);
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif;
  color: var(--text);
  background: radial-gradient(circle at 20% 0%, #e8f2ff 0, transparent 32rem), var(--bg);
  line-height: 1.62;
}
a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }
.hero {
  padding: 24px clamp(20px, 5vw, 72px) 52px;
  background: linear-gradient(180deg, rgba(255,255,255,.94), rgba(255,255,255,.58));
  border-bottom: 1px solid var(--line);
}
.top-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  justify-content: center;
  margin: 0 auto 44px;
}
.top-nav a {
  padding: 8px 12px;
  border: 1px solid rgba(10,132,255,.18);
  border-radius: 999px;
  background: rgba(255,255,255,.72);
  color: #28506f;
  font-size: 13px;
}
.hero-inner { max-width: 1120px; margin: 0 auto; }
.eyebrow, .section-kicker, .label {
  margin: 0 0 8px;
  color: var(--blue);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}
h1 { max-width: 980px; margin: 0; font-size: clamp(34px, 5vw, 68px); line-height: 1.04; letter-spacing: 0; }
.hero-subtitle { max-width: 720px; color: var(--muted); font-size: 19px; }
.hero-meta { display: flex; gap: 10px; flex-wrap: wrap; }
.hero-meta span, .state-pill {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 6px 10px;
  background: rgba(255,255,255,.8);
  border: 1px solid var(--line);
  color: var(--muted);
  font-size: 13px;
}
.section { max-width: 1180px; margin: 0 auto; padding: 48px clamp(18px, 4vw, 36px); }
.section-heading { display: flex; align-items: end; justify-content: space-between; gap: 16px; margin-bottom: 20px; }
.section-heading h2 { margin: 0; font-size: clamp(28px, 3vw, 42px); letter-spacing: 0; }
.section-note, .muted { color: var(--muted); }
.goal-card, .chain-explain, .qa-card, .target-section .target-table, .source-collapse {
  border: 1px solid var(--line);
  border-radius: 22px;
  background: var(--surface);
  box-shadow: var(--shadow);
}
.goal-card {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  padding: 22px;
}
.goal-main { font-size: 22px; font-weight: 700; }
.chain-explain { padding: 22px; }
.chain-plain-summary { margin-top: 0; font-size: 18px; color: #344054; }
.chain-flow-steps { display: grid; gap: 8px; padding-left: 22px; color: #344054; }
.chain-layer-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; margin: 18px 0; }
.chain-layer-card {
  border: 1px solid var(--line);
  border-radius: 16px;
  background: var(--surface-strong);
  padding: 16px;
}
.chain-layer-card h3 { margin: 0 0 8px; font-size: 16px; }
.chain-map { overflow-x: auto; margin: 18px 0; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 12px 14px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
th { color: #475467; font-size: 13px; background: #f7f9fc; }
.chain-chokepoints, .chain-target-links {
  margin-top: 12px;
  padding: 12px 14px;
  border-radius: 14px;
  background: #f7f9fc;
  color: #344054;
}
.qa-stack, .child-stack { display: grid; gap: 14px; }
.qa-card { padding: 0; overflow: clip; }
.qa-card summary {
  cursor: pointer;
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  gap: 12px;
  align-items: center;
  padding: 18px 20px;
  list-style: none;
}
.qa-card summary::-webkit-details-marker { display: none; }
.qid {
  display: inline-flex;
  min-width: 54px;
  justify-content: center;
  padding: 5px 9px;
  border-radius: 999px;
  background: #eaf3ff;
  color: var(--blue);
  font-weight: 700;
  font-size: 13px;
}
.question { font-weight: 700; }
.qa-count { color: var(--muted); font-size: 13px; }
.chevron { color: var(--blue); font-size: 24px; transition: transform .2s ease; }
.qa-card[open] > summary .chevron { transform: rotate(90deg); }
.qa-body { padding: 0 20px 20px; display: grid; gap: 14px; }
.qa-block {
  border: 1px solid rgba(217,224,234,.82);
  border-radius: 16px;
  background: rgba(255,255,255,.68);
  padding: 14px;
}
.block-title { margin: 0 0 10px; font-weight: 800; color: #334155; }
.artifact-card {
  border: 1px solid var(--line);
  border-radius: 14px;
  background: var(--surface-strong);
  padding: 14px;
}
.l3-meta { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
.l3-meta span {
  padding: 5px 8px;
  border-radius: 999px;
  background: #f3f6fa;
  color: #475467;
  font-size: 12px;
}
.l3-artifact dl { display: grid; gap: 10px; margin: 0; }
.l3-artifact dl div { display: grid; grid-template-columns: 74px 1fr; gap: 10px; }
dt { color: var(--blue); font-weight: 800; }
dd { margin: 0; color: #344054; }
.source-links { margin: 10px 0 0; color: var(--muted); font-size: 13px; }
.target-table, .source-table { background: var(--surface-strong); overflow: hidden; }
.target-table { border-radius: 22px; }
.state-actionable_long { color: var(--green); border-color: rgba(29,154,108,.28); background: #eaf8f2; }
.state-watch_only { color: var(--amber); border-color: rgba(183,121,31,.28); background: #fff7e6; }
.state-no_action { color: var(--red); border-color: rgba(194,65,61,.24); background: #fff1f0; }
.source-collapse { padding: 16px 18px; }
.source-collapse summary { cursor: pointer; font-weight: 800; color: #334155; }
.source-table { margin-top: 14px; }
@media (max-width: 760px) {
  .goal-card { grid-template-columns: 1fr; }
  .qa-card summary { grid-template-columns: auto 1fr auto; }
  .qa-count { grid-column: 2 / 3; }
  .target-table, .source-table, .chain-table { font-size: 13px; }
  th, td { padding: 10px; }
}
"""
