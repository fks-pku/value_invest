from __future__ import annotations

from html import escape
from typing import Any

from value_invest_research.domain.research_plan import (
    validate_research_plan_execution,
)


LENS_LABELS = {
    "demand": "需求侧",
    "supply": "供给侧",
    "technology": "技术侧",
    "valuation": "估值侧",
    "esg": "ESG",
}

LENS_ORDER = tuple(LENS_LABELS)

STATUS_LABELS = {
    "planned": "待执行",
    "pending": "待执行",
    "in_progress": "研究中",
    "review_pending": "待复核",
    "blocked": "有缺口",
    "completed": "已完成",
}


class StandaloneBomResearchPlanHtmlRenderer:
    """Render the dedicated L3 -> L4 -> L5 execution plan document."""

    def render(
        self,
        *,
        project: dict[str, Any],
        bundle: dict[str, Any],
    ) -> str:
        plans = list(bundle.get("plans") or [])
        events_by_node = dict(bundle.get("events_by_node") or {})
        grouped = {lens_id: [] for lens_id in LENS_ORDER}
        validations: dict[str, dict[str, Any]] = {}
        for plan in plans:
            node_id = str(plan.get("l3_node_id") or "")
            lens_id = str(plan.get("lens_id") or "")
            grouped.setdefault(lens_id, []).append(plan)
            validations[node_id] = validate_research_plan_execution(
                plan,
                events_by_node.get(node_id) or [],
            )

        leaf_count = sum(len(plan.get("steps") or []) for plan in plans)
        completed_leaf_count = sum(
            int(result.get("summary", {}).get("completed", 0) or 0)
            for result in validations.values()
        )
        completed_l3_count = sum(
            result.get("summary", {}).get("status") == "completed"
            for result in validations.values()
        )
        nav = "".join(
            f'<a href="#lens-{escape(lens_id)}">{escape(label)}</a>'
            for lens_id, label in LENS_LABELS.items()
            if grouped.get(lens_id)
        )
        sections = "\n".join(
            self._render_lens(
                lens_id=lens_id,
                label=LENS_LABELS.get(lens_id, lens_id),
                plans=grouped.get(lens_id) or [],
                validations=validations,
            )
            for lens_id in [*LENS_ORDER, *sorted(set(grouped) - set(LENS_ORDER))]
            if grouped.get(lens_id)
        )
        title = str(project.get("title") or "BOM 研究")
        report_date = str(project.get("report_date") or "")
        plan_id = str(
            (bundle.get("index") or {}).get("parent_research_plan_id") or ""
        )
        return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} · 研究计划书</title>
  <style>{_plan_css()}</style>
</head>
<body data-report-scope="research-plan" data-plan-contract="leaf-search-v2">
  <header class="masthead">
    <div class="masthead-inner">
      <div class="eyebrow">VALUE INVEST · EXECUTABLE RESEARCH PLAN</div>
      <div class="title-row">
        <div>
          <h1>{escape(title)}<span>研究计划书</span></h1>
          <p>每个 L3 独立成计划；材料从最细 L5 叶子问题发起搜索，并逐叶解析、复核和回答。</p>
        </div>
        <a class="report-link" href="professional_report.html">返回专业报告 <b>↗</b></a>
      </div>
      <div class="metrics" aria-label="计划规模">
        <div><strong>{len(plans)}</strong><span>L3 独立计划</span></div>
        <div><strong>{leaf_count}</strong><span>L5 最细叶子</span></div>
        <div><strong>{completed_l3_count}</strong><span>已完成 L3</span></div>
        <div><strong>{completed_leaf_count}</strong><span>已完成叶子</span></div>
      </div>
      <div class="document-meta">
        <span>计划版本 <code>{escape(plan_id)}</code></span>
        <span>计划日期 <time>{escape(report_date)}</time></span>
      </div>
    </div>
  </header>

  <nav class="lens-nav" aria-label="研究计划章节">
    <div><a class="method-link" href="#method">执行规则</a>{nav}</div>
  </nav>

  <main>
    <section id="method" class="method">
      <div class="section-kicker">00 · EXECUTION CONTRACT</div>
      <div class="method-grid">
        <div>
          <h2>计划不是问题清单，<br>而是一组可验收的研究任务。</h2>
        </div>
        <div class="rule-card">
          <span>01</span><strong>L3 独立计划</strong>
          <p>根计划只做汇总。每个 L3 单独维护版本、依赖、证据门禁和追加式事件账本。</p>
        </div>
        <div class="rule-card">
          <span>02</span><strong>L5 定向搜集</strong>
          <p>每次搜索必须绑定一个最细叶子。宽泛材料只进入候选池，不能直接计入完成度。</p>
        </div>
        <div class="rule-card">
          <span>03</span><strong>逐叶验收</strong>
          <p>搜索、来源附件、逐源解析、GPT 复核、回答、反证和依赖全部闭环后，叶子才完成。</p>
        </div>
      </div>
      <div class="flow" aria-label="研究执行路径">
        <span>根研究计划</span><i>→</i><span>L3 独立计划</span><i>→</i>
        <span>L4 研究维度</span><i>→</i><span class="accent">L5 叶子搜索</span><i>→</i>
        <span>解析与复核</span><i>→</i><span>L3 汇总</span>
      </div>
    </section>
    {sections}
  </main>

  <footer>
    <p>这是一份由版本化计划数据生成的执行文档。完成状态来自各 L3 的追加式事件账本，不由已有材料数量推断。</p>
  </footer>
</body>
</html>
"""

    def _render_lens(
        self,
        *,
        lens_id: str,
        label: str,
        plans: list[dict[str, Any]],
        validations: dict[str, dict[str, Any]],
    ) -> str:
        rows = "\n".join(
            self._render_l3_plan(
                plan,
                position=position,
                validation=validations[str(plan.get("l3_node_id") or "")],
            )
            for position, plan in enumerate(plans, start=1)
        )
        return f"""
<section id="lens-{escape(lens_id)}" class="lens-section">
  <div class="lens-heading">
    <div><span>{LENS_ORDER.index(lens_id) + 1 if lens_id in LENS_ORDER else 0:02d}</span><p>RESEARCH LENS</p></div>
    <h2>{escape(label)}</h2>
    <p>{len(plans)} 个 L3 · {sum(len(plan.get('steps') or []) for plan in plans)} 个 L5</p>
  </div>
  <div class="l3-list">{rows}</div>
</section>
"""

    def _render_l3_plan(
        self,
        plan: dict[str, Any],
        *,
        position: int,
        validation: dict[str, Any],
    ) -> str:
        node_id = str(plan.get("l3_node_id") or "")
        summary = dict(validation.get("summary") or {})
        status = str(summary.get("status") or "planned")
        completed = int(summary.get("completed", 0) or 0)
        total = len(plan.get("steps") or [])
        state_by_step = {
            str(row.get("step_id") or ""): row
            for row in validation.get("step_states") or []
        }
        unit_by_id = {
            str(row.get("l4_question_id") or ""): row
            for row in plan.get("l4_units") or []
        }
        leaves = "\n".join(
            self._render_leaf(
                step,
                unit=unit_by_id.get(str(step.get("l4_question_id") or "")) or {},
                state=state_by_step.get(str(step.get("step_id") or "")) or {},
            )
            for step in plan.get("steps") or []
        )
        logic = dict(plan.get("logic_contract") or {})
        indicators = "".join(
            f"<li>{escape(str(item))}</li>" for item in logic.get("indicators") or []
        ) or "<li>待计划补充</li>"
        return f"""
<details class="l3-plan" data-l3-node-id="{escape(node_id)}" data-l3-plan-id="{escape(str(plan.get('plan_id') or ''))}">
  <summary>
    <span class="l3-sequence">{position:02d}</span>
    <div class="l3-identity"><code>{escape(node_id)}</code><h3>{escape(str(plan.get('l3_title') or ''))}</h3></div>
    <p class="l3-question"><b>研究问题</b>{escape(str(plan.get('l3_question') or ''))}</p>
    <div class="l3-progress"><strong>{completed} / {total}</strong><span>叶子完成</span></div>
    <span class="status status-{escape(status)}">{escape(STATUS_LABELS.get(status, status))}</span>
    <i class="chevron" aria-hidden="true"></i>
  </summary>
  <div class="l3-body">
    <section class="logic-contract">
      <div><span>观察指标</span><ul>{indicators}</ul></div>
      <div><span>支持规则</span><p>{escape(str(logic.get('support_rule') or '待定义'))}</p></div>
      <div><span>反证规则</span><p>{escape(str(logic.get('refute_rule') or '待定义'))}</p></div>
    </section>
    <div class="leaf-list">{leaves}</div>
  </div>
</details>
"""

    def _render_leaf(
        self,
        step: dict[str, Any],
        *,
        unit: dict[str, Any],
        state: dict[str, Any],
    ) -> str:
        sequence = int(step.get("sequence", 0) or 0)
        status = str(state.get("status") or step.get("initial_status") or "pending")
        source_rows = "".join(
            self._render_source_plan(source)
            for source in step.get("source_plan") or []
        ) or '<p class="empty">尚未定义定向来源。</p>'
        dependencies = list(step.get("depends_on_step_ids") or [])
        dependency_text = "、".join(str(item) for item in dependencies) or "无，可直接启动"
        gate = dict(step.get("minimum_evidence_gate") or {})
        gate_items = [
            "叶子搜索批次",
            "逐来源解析",
            "GPT 复核",
            "支持与反证结果",
            "叶子回答",
            "依赖闭环",
        ]
        if gate.get("refutation_search_required"):
            gate_items.append("独立反证搜索")
        gates = "".join(f"<li>{escape(item)}</li>" for item in gate_items)
        return f"""
<article class="leaf" data-leaf-question-id="{escape(str(step.get('leaf_question_id') or ''))}">
  <header>
    <span>{sequence:02d}</span>
    <div><p>L4 · {escape(str(unit.get('title') or step.get('research_dimension') or ''))}</p><h4>{escape(str(unit.get('question') or ''))}</h4></div>
    <span class="status status-{escape(status)}">{escape(STATUS_LABELS.get(status, status))}</span>
  </header>
  <div class="leaf-question"><b>L5 最细叶子问题</b><p>{escape(str(step.get('question') or ''))}</p></div>
  <div class="leaf-grid">
    <section><h5>定向材料与搜索锚点</h5>{source_rows}</section>
    <section><h5>完成门禁</h5><ul class="gate-list">{gates}</ul></section>
  </div>
  <footer><span>依赖</span><code>{escape(dependency_text)}</code><span>刷新</span><p>{escape(str(step.get('freshness_requirement') or ''))}</p></footer>
</article>
"""

    def _render_source_plan(self, source: dict[str, Any]) -> str:
        queries = "".join(
            f"<li><code>{escape(str(item))}</code></li>"
            for item in source.get("examples_or_search_queries") or []
        ) or "<li><code>待补充</code></li>"
        fields = "".join(
            f"<li>{escape(str(item))}</li>"
            for item in source.get("expected_fields") or []
        )
        return f"""
<div class="source-plan">
  <div><span>{escape(str(source.get('source_bucket') or 'source'))}</span><strong>{escape(str(source.get('source_type') or ''))}</strong></div>
  <p>{escape(str(source.get('why_needed') or ''))}</p>
  <ol>{queries}</ol>
  <ul class="field-list">{fields}</ul>
</div>
"""


def _plan_css() -> str:
    return r"""
:root {
  --ink: #17242c;
  --muted: #687780;
  --line: #ccd4d8;
  --paper: #f5f2eb;
  --panel: #fffdf8;
  --blue: #245b78;
  --blue-soft: #e9f0f3;
  --rust: #a3482b;
  --green: #2f6754;
  --shadow: 0 18px 45px rgba(26, 44, 54, .08);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  background:
    linear-gradient(rgba(23,36,44,.025) 1px, transparent 1px),
    var(--paper);
  background-size: 100% 28px;
  font-family: "Songti SC", "STSong", "Noto Serif CJK SC", Georgia, serif;
  font-size: 15px;
  line-height: 1.72;
}
a { color: inherit; }
.masthead { color: #edf2f3; background: #18303d; border-bottom: 5px solid var(--rust); }
.masthead-inner { max-width: 1380px; margin: 0 auto; padding: 54px 42px 32px; }
.eyebrow, .section-kicker { color: #d89574; font: 700 11px/1.2 ui-monospace, SFMono-Regular, Menlo, monospace; letter-spacing: .18em; }
.title-row { display: flex; align-items: end; justify-content: space-between; gap: 40px; margin: 22px 0 34px; }
h1 { margin: 0; font-size: clamp(36px, 5vw, 68px); line-height: 1.02; letter-spacing: -.045em; font-weight: 700; }
h1 span { display: block; color: #d8e2e5; font-size: .42em; letter-spacing: .08em; margin-top: 14px; }
.title-row p { max-width: 760px; margin: 20px 0 0; color: #bfcdd2; font-size: 17px; }
.report-link { flex: 0 0 auto; padding: 11px 0; text-decoration: none; border-bottom: 1px solid #7192a0; font: 700 13px/1.2 ui-monospace, SFMono-Regular, Menlo, monospace; }
.report-link b { color: #e09976; margin-left: 8px; }
.metrics { display: grid; grid-template-columns: repeat(4, 1fr); border: 1px solid #46606c; }
.metrics div { display: grid; gap: 2px; padding: 18px 22px; border-right: 1px solid #46606c; }
.metrics div:last-child { border-right: 0; }
.metrics strong { color: white; font-size: 28px; line-height: 1; }
.metrics span, .document-meta { color: #aebfc6; font: 600 11px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace; letter-spacing: .05em; }
.document-meta { display: flex; justify-content: space-between; gap: 20px; margin-top: 16px; }
.document-meta code { color: #d7e1e4; }
.lens-nav { position: sticky; top: 0; z-index: 10; background: rgba(245,242,235,.96); border-bottom: 1px solid var(--line); backdrop-filter: blur(10px); }
.lens-nav > div { max-width: 1380px; margin: auto; padding: 0 42px; display: flex; overflow-x: auto; }
.lens-nav a { flex: 0 0 auto; padding: 16px 18px; text-decoration: none; color: #52636c; font: 700 12px/1 ui-monospace, SFMono-Regular, Menlo, monospace; }
.lens-nav a:hover { color: var(--rust); }
.lens-nav .method-link { color: var(--rust); padding-left: 0; }
main { max-width: 1380px; margin: 0 auto; padding: 54px 42px 100px; }
.method { scroll-margin-top: 70px; padding-bottom: 62px; border-bottom: 1px solid var(--line); }
.method-grid { display: grid; grid-template-columns: 1.4fr repeat(3, 1fr); gap: 18px; margin-top: 24px; }
.method h2 { margin: 0; font-size: 31px; line-height: 1.28; letter-spacing: -.025em; }
.rule-card { min-height: 190px; padding: 22px; background: var(--panel); border-top: 3px solid var(--blue); box-shadow: var(--shadow); }
.rule-card span { color: var(--rust); font: 700 11px ui-monospace, monospace; }
.rule-card strong { display: block; margin: 32px 0 8px; font-size: 17px; }
.rule-card p { margin: 0; color: var(--muted); font-size: 13px; }
.flow { display: flex; align-items: center; gap: 12px; margin-top: 25px; padding: 17px 20px; border: 1px solid var(--line); overflow-x: auto; white-space: nowrap; font: 700 12px ui-monospace, monospace; }
.flow span { padding: 6px 9px; background: #ebe7de; }
.flow .accent { color: white; background: var(--rust); }
.flow i { color: #91a0a7; font-style: normal; }
.lens-section { scroll-margin-top: 70px; padding-top: 68px; }
.lens-heading { display: grid; grid-template-columns: 180px 1fr auto; align-items: end; gap: 24px; padding-bottom: 17px; border-bottom: 3px solid var(--ink); }
.lens-heading > div { display: flex; align-items: center; gap: 12px; }
.lens-heading span { color: var(--rust); font: 700 20px ui-monospace, monospace; }
.lens-heading p { margin: 0; color: var(--muted); font: 700 11px ui-monospace, monospace; letter-spacing: .09em; }
.lens-heading h2 { margin: 0; font-size: 35px; line-height: 1; }
.l3-list { border-left: 1px solid var(--line); border-right: 1px solid var(--line); }
.l3-plan { background: rgba(255,253,248,.82); border-bottom: 1px solid var(--line); }
.l3-plan > summary { display: grid; grid-template-columns: 48px minmax(180px,.8fr) minmax(300px,1.5fr) 80px 72px 18px; align-items: center; gap: 18px; min-height: 126px; padding: 20px 24px; cursor: pointer; list-style: none; }
.l3-plan > summary::-webkit-details-marker { display: none; }
.l3-plan > summary:hover { background: white; }
.l3-sequence { color: var(--rust); font: 700 13px ui-monospace, monospace; }
.l3-identity code { color: var(--blue); font: 700 10px ui-monospace, monospace; }
.l3-identity h3 { margin: 7px 0 0; font-size: 20px; line-height: 1.3; }
.l3-question { margin: 0; color: #43545d; line-height: 1.55; }
.l3-question b { display: block; margin-bottom: 5px; color: var(--rust); font: 700 10px ui-monospace, monospace; letter-spacing: .08em; }
.l3-progress { text-align: right; }
.l3-progress strong { display: block; font: 700 18px ui-monospace, monospace; }
.l3-progress span { color: var(--muted); font-size: 11px; }
.status { display: inline-flex; justify-content: center; border: 1px solid #aab5ba; padding: 5px 7px; color: var(--muted); font: 700 10px/1 ui-monospace, monospace; white-space: nowrap; }
.status-completed { color: var(--green); border-color: #6e9d8b; }
.status-in_progress, .status-review_pending { color: var(--blue); border-color: #7da3b7; }
.status-blocked { color: var(--rust); border-color: #bd806b; }
.chevron { width: 9px; height: 9px; border-right: 2px solid #73858e; border-bottom: 2px solid #73858e; transform: rotate(45deg); transition: transform .2s ease; }
.l3-plan[open] .chevron { transform: rotate(225deg); }
.l3-body { padding: 0 24px 30px 90px; background: #edf1f1; border-top: 1px solid var(--line); }
.logic-contract { display: grid; grid-template-columns: 1fr 1.25fr 1.25fr; gap: 1px; background: #cbd4d7; border: 1px solid #cbd4d7; }
.logic-contract > div { background: #f8faf9; padding: 16px; }
.logic-contract span, .leaf h5, .leaf-question b, .leaf footer > span { color: var(--rust); font: 700 10px ui-monospace, monospace; letter-spacing: .08em; }
.logic-contract p, .logic-contract ul { margin: 8px 0 0; padding-left: 18px; font-size: 12px; color: #53646d; }
.leaf-list { display: grid; gap: 12px; margin-top: 22px; }
.leaf { background: var(--panel); border: 1px solid #d6dddf; box-shadow: 0 7px 20px rgba(26,44,54,.045); }
.leaf > header { display: grid; grid-template-columns: 38px 1fr auto; align-items: start; gap: 14px; padding: 17px 18px; border-bottom: 1px solid #e1e6e7; }
.leaf > header > span:first-child { color: var(--rust); font: 700 12px ui-monospace, monospace; }
.leaf > header p { margin: 0 0 5px; color: var(--blue); font: 700 11px ui-monospace, monospace; }
.leaf h4 { margin: 0; font-size: 14px; font-weight: 500; line-height: 1.5; }
.leaf-question { padding: 18px; background: #fff; border-bottom: 1px solid #e1e6e7; }
.leaf-question p { margin: 7px 0 0; font-size: 16px; font-weight: 650; line-height: 1.65; }
.leaf-grid { display: grid; grid-template-columns: minmax(0,1.6fr) minmax(230px,.65fr); gap: 22px; padding: 18px; }
.leaf h5 { margin: 0 0 9px; }
.source-plan { border-left: 3px solid #8eabb8; padding-left: 13px; margin: 13px 0 20px; }
.source-plan > div { display: flex; gap: 8px; align-items: baseline; }
.source-plan > div span { color: var(--blue); font: 700 10px ui-monospace, monospace; text-transform: uppercase; }
.source-plan > div strong { font-size: 13px; }
.source-plan p { margin: 5px 0; color: var(--muted); font-size: 12px; }
.source-plan ol { margin: 8px 0; padding-left: 20px; }
.source-plan ol code { color: #344852; white-space: normal; font-size: 11px; }
.field-list, .gate-list { display: flex; flex-wrap: wrap; gap: 6px; margin: 9px 0 0; padding: 0; list-style: none; }
.field-list li, .gate-list li { padding: 4px 7px; background: var(--blue-soft); color: #46606d; font: 600 10px ui-monospace, monospace; }
.gate-list li { background: #eeeae1; color: #625d53; }
.leaf > footer { display: grid; grid-template-columns: auto minmax(220px,.6fr) auto 1fr; align-items: baseline; gap: 9px; padding: 12px 18px; color: var(--muted); background: #f5f5f1; font-size: 11px; }
.leaf > footer code { white-space: normal; }
.leaf > footer p { margin: 0; }
body > footer { border-top: 1px solid var(--line); padding: 30px 42px 60px; color: var(--muted); text-align: center; font-size: 12px; }
@media (max-width: 980px) {
  .method-grid { grid-template-columns: 1fr 1fr; }
  .method-grid > div:first-child { grid-column: 1 / -1; }
  .l3-plan > summary { grid-template-columns: 36px 1fr auto 16px; }
  .l3-question { grid-column: 2 / -1; }
  .l3-progress { display: none; }
  .l3-body { padding-left: 24px; }
  .logic-contract, .leaf-grid { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .masthead-inner, main { padding-left: 20px; padding-right: 20px; }
  .title-row { display: block; }
  .report-link { display: inline-block; margin-top: 22px; }
  .metrics { grid-template-columns: 1fr 1fr; }
  .metrics div:nth-child(2) { border-right: 0; }
  .metrics div:nth-child(-n+2) { border-bottom: 1px solid #46606c; }
  .document-meta { display: grid; }
  .lens-nav > div { padding: 0 20px; }
  .method-grid { grid-template-columns: 1fr; }
  .method-grid > div:first-child { grid-column: auto; }
  .lens-heading { grid-template-columns: 1fr auto; }
  .lens-heading > div { grid-column: 1 / -1; }
  .lens-heading h2 { font-size: 29px; }
  .l3-plan > summary { padding: 17px 14px; gap: 11px; }
  .l3-identity h3 { font-size: 17px; }
  .l3-question { grid-column: 1 / -1; }
  .status { font-size: 9px; }
  .l3-body { padding: 0 12px 22px; }
  .leaf > header { grid-template-columns: 28px 1fr; }
  .leaf > header .status { grid-column: 2; justify-self: start; }
  .leaf-grid { padding: 14px; }
  .leaf > footer { grid-template-columns: auto 1fr; }
}
"""
