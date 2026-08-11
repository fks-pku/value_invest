from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any


MATERIAL_LABELS = {
    "official_filing": "官方财报",
    "official_company": "官方公司",
    "sell_side_research": "研报",
    "authoritative_third_party": "第三方权威",
    "market_news": "市场消息",
    "expert_opinion": "专家观点",
    "other": "其他",
}

DEMAND_INFORMATION_TYPE_LABELS = {
    "official_filing": "官方财报",
    "authoritative_third_party": "第三方研究",
    "sell_side_research": "机构研报",
    "official_company": "市场消息",
    "market_news": "市场消息",
    "expert_opinion": "市场消息",
    "other": "市场消息",
}

STATE_LABELS = {
    "unresolved": "待验证",
    "weak": "证据偏弱",
    "strengthening": "正在增强",
    "confirmed": "已验证",
    "weakening": "正在减弱",
    "refuted": "已反证",
}

ACTION_LABELS = {
    "actionable_long": "可行动多头",
    "watch_only": "观察",
    "no_action": "不行动",
}

GATE_LABELS = {
    "logic_coverage": "逻辑覆盖",
    "company_financial_bridge": "公司财务桥",
    "valuation": "估值",
    "refutation": "反证",
    "risk_control": "风险控制",
}

DIRECTION_LABELS = {
    "support": "支持",
    "refute": "反证",
    "boundary": "改变边界",
    "constraint": "新增约束",
    "new_branch": "新增分支",
    "conflict": "证据冲突",
    "unresolved": "暂未判断",
    "neutral": "线索",
}

EVIDENCE_NATURE_LABELS = {
    "fact": "事实",
    "forecast": "预测",
    "opinion": "观点",
    "lead": "线索",
}

ENTITY_EFFECT_LABELS = {
    "positive": "正向",
    "negative": "负向",
    "mixed": "多空并存",
    "unclear": "待判断",
}


def _direction_filter_group(direction: str) -> str:
    if direction == "support":
        return "support"
    if direction in ("refute", "conflict"):
        return "adverse"
    if direction in ("boundary", "constraint"):
        return "boundary"
    if direction == "new_branch":
        return "branch"
    return "unresolved"


class StandaloneBomHtmlRenderer:
    """Render one standalone BOM timeline as the default local reading view."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir.resolve()

    def render(self, view: dict[str, Any]) -> str:
        title = str(view.get("title") or "BOM 投资研究")
        lenses = list(view.get("lenses") or [])
        claims = [
            claim
            for lens in lenses
            for claim in lens.get("claims") or []
        ]
        source_count = len(
            {
                str(claim.get("source_id") or "")
                for claim in claims
                if str(claim.get("source_id") or "")
            }
        )
        engine_version = str(view.get("investment_engine_version") or "")
        decision_nav = (
            '<a href="#investment-decision">00 投资判断</a>'
            if engine_version
            else ""
        )
        nav = decision_nav + "".join(
            (
                f'<a href="#lens-{escape(str(lens["lens_id"]))}">'
                f'{index:02d} {escape(str(lens["label"]))}</a>'
            )
            for index, lens in enumerate(lenses, start=1)
        )
        sections = "\n".join(
            self._render_lens(lens, index)
            for index, lens in enumerate(lenses, start=1)
        )
        decision = self._render_decision(view) if engine_version else ""
        engine_attribute = (
            f' data-investment-engine-version="{escape(engine_version)}"'
            if engine_version
            else ""
        )
        research_model = str(view.get("research_model") or "")
        model_attribute = (
            ' data-research-model="logic-chain-centered"'
            if research_model == "logic_chain_centered"
            else ""
        )
        logic_chain_version = str(view.get("logic_chain_version") or "")
        chain_attribute = (
            f' data-logic-chain-version="{escape(logic_chain_version)}"'
            if logic_chain_version
            else ""
        )
        html = "\n".join(
            [
                "<!doctype html>",
                '<html lang="zh-CN">',
                "<head>",
                '<meta charset="utf-8">',
                '<meta name="viewport" content="width=device-width, initial-scale=1">',
                f"<title>{escape(title)}</title>",
                f"<style>{_report_css()}</style>",
                "</head>",
                (
                    '<body data-report-scope="standalone-bom" '
                    f'data-bom-node-id="{escape(str(view.get("bom_node_id") or ""))}"'
                    f"{engine_attribute}{model_attribute}{chain_attribute}>"
                ),
                '<header class="report-header">',
                '  <div class="report-header-inner">',
                '    <div class="report-label">VALUE INVEST · BOM RESEARCH</div>',
                f"    <h1>{escape(title)}</h1>",
                (
                    '    <p class="report-deck">以第一性原理逻辑链组织研究；'
                    "原子观点先改变节点，再改变全局投资判断。</p>"
                ),
                '    <div class="report-meta" aria-label="报告元数据">',
                (
                    '      <div><span>研究截面</span>'
                    f'<strong>{escape(str(view.get("as_of_date") or ""))}</strong></div>'
                ),
                f"      <div><span>研究视角</span><strong>{len(lenses)}</strong></div>",
                f"      <div><span>映射材料</span><strong>{source_count}</strong></div>",
                f"      <div><span>原子观点</span><strong>{len(claims)}</strong></div>",
                "    </div>",
                "  </div>",
                "</header>",
                '<nav class="top-nav" aria-label="报告章节">',
                f'  <div class="top-nav-inner">{nav}</div>',
                "</nav>",
                '<main class="report-main">',
                decision,
                sections,
                "</main>",
                '<footer class="report-footer">',
                "  <p>本报告由结构化材料账本生成；事实、预测和观点按原文位置保留。</p>",
                "</footer>",
                f"<script>{_report_script()}</script>",
                "</body>",
                "</html>",
                "",
            ]
        )
        return "\n".join(line.rstrip() for line in html.splitlines()) + "\n"

    def _render_decision(self, view: dict[str, Any]) -> str:
        decision = dict(view.get("decision") or {})
        coverage = dict(view.get("engine_coverage") or {})
        stored_summary = str(decision.get("summary") or "")
        logic_chain_judgment = str(
            view.get("logic_chain_judgment") or stored_summary
        )
        evidence_update = (
            stored_summary
            if stored_summary and stored_summary != logic_chain_judgment
            else ""
        )
        action_state = str(decision.get("action_state") or "watch_only")
        action_label = ACTION_LABELS.get(action_state, "观察")
        gate_results = dict(decision.get("gate_results") or {})
        gates = "".join(
            (
                f'<li class="gate-{"pass" if gate_results.get(gate) else "fail"}">'
                f'<span aria-hidden="true">{"✓" if gate_results.get(gate) else "·"}</span>'
                f"{escape(label)}</li>"
            )
            for gate, label in GATE_LABELS.items()
        )
        company_rows = "".join(
            self._render_company_impact(row)
            for row in decision.get("company_impacts") or []
        )
        if not company_rows:
            company_rows = (
                '<tr><td colspan="6" class="empty-state">'
                "尚无通过公司财务桥和估值门槛的标的结论。</td></tr>"
            )
        catalysts = "".join(
            f"<li>{escape(str(item))}</li>"
            for item in decision.get("next_catalysts") or []
        )
        if not catalysts:
            catalysts = "<li>等待下一批问题化材料进入逻辑账本。</li>"
        return f"""
<section id="investment-decision" class="decision-section">
  <div class="decision-kicker">CURRENT INVESTMENT SNAPSHOT</div>
  <div class="decision-heading">
    <div>
      <h2>当前投资判断</h2>
      <p>{escape(logic_chain_judgment)}</p>
    </div>
    <span class="action-badge action-{escape(action_state)}">{escape(action_label)}</span>
  </div>
  {f'<div class="decision-update"><strong>本期证据变化</strong><p>{escape(evidence_update)}</p></div>' if evidence_update else ''}
  <div class="delta-list">
    <article>
      <span>基本面变化</span>
      <p>{escape(str(decision.get("fundamental_delta") or "待验证"))}</p>
    </article>
    <article>
      <span>市场共识变化</span>
      <p>{escape(str(decision.get("consensus_delta") or "待验证"))}</p>
    </article>
    <article>
      <span>定价变化</span>
      <p>{escape(str(decision.get("priced_in_delta") or "待验证"))}</p>
    </article>
  </div>
  <div class="decision-audit">
    <div>
      <h3>研究门槛</h3>
      <ul class="gate-list">{gates}</ul>
    </div>
    <div>
      <h3>覆盖状态</h3>
      <p>{coverage.get("state_nodes", 0)} / {coverage.get("logic_nodes", 0)} 个逻辑节点已有截面；{coverage.get("mapped_claims", 0)} / {coverage.get("total_claims", 0)} 条原子观点完成映射。</p>
    </div>
    <div>
      <h3>下一催化剂</h3>
      <ul>{catalysts}</ul>
    </div>
  </div>
  <div class="section-heading decision-table-heading">
    <div><span>00</span><h3>公司影响、预期差与动作</h3></div>
  </div>
  <div class="company-table-wrap" role="region" aria-label="公司影响与动作" tabindex="0">
    <table class="company-table">
      <thead><tr>
        <th>公司</th><th>敞口</th><th>盈利传导</th><th>市场定价</th><th>当前结论</th><th>动作</th>
      </tr></thead>
      <tbody>{company_rows}</tbody>
    </table>
  </div>
</section>
"""

    def _render_company_impact(self, row: dict[str, Any]) -> str:
        action_state = str(row.get("action_state") or "watch_only")
        name = escape(str(row.get("company") or ""))
        ticker = escape(str(row.get("ticker") or ""))
        return f"""
<tr>
  <td><strong>{name}</strong>{f'<small>{ticker}</small>' if ticker else ''}</td>
  <td>{escape(str(row.get("exposure") or ""))}</td>
  <td>{escape(str(row.get("earnings_bridge") or ""))}</td>
  <td>{escape(str(row.get("priced_in") or ""))}</td>
  <td>{escape(str(row.get("conclusion") or ""))}</td>
  <td><span class="action-inline action-{escape(action_state)}">{escape(ACTION_LABELS.get(action_state, "观察"))}</span></td>
</tr>
"""

    def _render_lens(self, lens: dict[str, Any], index: int) -> str:
        lens_id = escape(str(lens.get("lens_id") or ""))
        label = escape(str(lens.get("label") or ""))
        logic = escape(str(lens.get("logic_chain") or "当前逻辑链尚未定义。"))
        conclusion = escape(str(lens.get("conclusion") or "当前尚不能形成结论。"))
        trend = escape(str(lens.get("trend") or "当前为首个研究截面。"))
        groups = _group_claims_by_source(list(lens.get("claims") or []))
        source_rows = "\n".join(
            self._render_source_row(group)
            for group in groups
        )
        if not source_rows:
            source_rows = (
                '<tr><td class="empty-state" colspan="4">'
                "尚无经过问题化解析和复核的材料。</td></tr>"
            )
        claim_count = sum(len(group.get("claims") or []) for group in groups)
        logic_nodes = list(lens.get("logic_nodes") or [])
        causal_nodes = list(lens.get("causal_nodes") or logic_nodes)
        derived_views = list(lens.get("derived_views") or [])
        logic_node_rows = "\n".join(
            self._render_logic_node(node, position=position)
            for position, node in enumerate(causal_nodes, start=1)
        )
        logic_state_section = ""
        if logic_nodes:
            logic_state_section = f"""
    <section class="logic-state-section" aria-labelledby="logic-state-{lens_id}">
      <div class="section-heading">
        <div>
          <span>01</span>
          <h3 id="logic-state-{lens_id}">节点状态与观点时间线</h3>
        </div>
        <p>点击节点查看原子观点如何增强、削弱或改变因果关系</p>
      </div>
      <div class="logic-chain-map">{logic_node_rows}</div>
    </section>
"""
        derived_section = ""
        if derived_views:
            derived_rows = "\n".join(
                self._render_logic_node(node, position=position)
                for position, node in enumerate(derived_views, start=1)
            )
            derived_section = f"""
    <section class="derived-view-section" aria-labelledby="derived-{lens_id}">
      <div class="section-heading">
        <div>
          <span>02</span>
          <h3 id="derived-{lens_id}">派生证据视图</h3>
        </div>
        <p>用于查阅需求方、数量矩阵等局部证据，不直接替代因果判断</p>
      </div>
      <div class="derived-view-list">{derived_rows}</div>
    </section>
"""
        timeline_section = ""
        if not logic_nodes:
            timeline_section = f"""
    <section class="timeline" aria-labelledby="timeline-{lens_id}">
      <div class="section-heading">
        <div>
          <span>01</span>
          <h3 id="timeline-{lens_id}">信息时间线</h3>
        </div>
        <p>按市场可见日期由近及远</p>
      </div>
      <div class="timeline-table-wrap" role="region" aria-label="{label}信息时间线" tabindex="0">
        <table class="timeline-table">
          <colgroup>
            <col class="col-date">
            <col class="col-type">
            <col class="col-report">
            <col class="col-claims">
          </colgroup>
          <thead>
            <tr>
              <th scope="col">时间</th>
              <th scope="col">信息类型</th>
              <th scope="col">报告</th>
              <th scope="col">观点列表</th>
            </tr>
          </thead>
          <tbody>
            {source_rows}
          </tbody>
        </table>
      </div>
    </section>
"""
        conclusion_number = "03" if derived_views else "02"
        return f"""
<details id="lens-{lens_id}" class="lens-section" open>
  <summary class="lens-heading">
    <span class="lens-number">{index:02d}</span>
    <div>
      <p>RESEARCH LENS</p>
      <h2>{label}</h2>
    </div>
    <span class="lens-count">{len(groups)} 份材料 · {claim_count} 条观点</span>
    <span class="lens-chevron" aria-hidden="true"></span>
  </summary>
  <div class="lens-body">
    <section class="logic-note" aria-labelledby="logic-{lens_id}">
      <h3 id="logic-{lens_id}">第一性原理逻辑链</h3>
      <p>{logic}</p>
    </section>

{logic_state_section}
{derived_section}
{timeline_section}

    <section class="conclusion-panel" aria-labelledby="conclusion-{lens_id}">
      <div class="section-heading">
        <div>
          <span>{conclusion_number}</span>
          <h3 id="conclusion-{lens_id}">全局结论与趋势</h3>
        </div>
      </div>
      <p class="conclusion-text">{conclusion}</p>
      <div class="trend-line">
        <strong>趋势变化</strong>
        <p>{trend}</p>
      </div>
    </section>
  </div>
</details>
"""

    def _render_logic_node(
        self,
        node: dict[str, Any],
        *,
        position: int = 1,
    ) -> str:
        if str(node.get("render_mode") or "") == "demand_party_list":
            return self._render_demand_party_list(node)
        if str(node.get("render_mode") or "") == "demand_quantity_matrix":
            return self._render_demand_quantity_matrix(node)
        state = str(node.get("state") or "unresolved")
        entities = list(node.get("entities") or [])
        entity_modules = "\n".join(
            self._render_entity_module(entity) for entity in entities
        )
        entity_audit = ""
        if entity_modules:
            entity_audit = f"""
  <details class="node-audit">
    <summary>按公司 / 实体查看原始材料</summary>
    <div class="entity-list" aria-label="公司与实体信息">{entity_modules}</div>
  </details>"""
        state_history = self._render_state_history(node)
        event_history = self._render_event_history(node)
        gaps = "".join(
            f"<li>{escape(str(item))}</li>"
            for item in node.get("evidence_gaps") or []
        )
        if not gaps:
            gaps = "<li>当前未登记额外缺口。</li>"
        next_validation = escape(
            str(node.get("next_validation") or "等待下一份相关材料验证。")
        )
        return f"""
<details class="logic-node causal-node" data-logic-node-id="{escape(str(node.get("logic_node_id") or ""))}">
  <summary class="logic-node-summary">
    <span class="logic-step">{position:02d}</span>
    <div class="logic-node-heading">
      <span>{escape(str(node.get("logic_node_id") or ""))}</span>
      <h4>{escape(str(node.get("title") or ""))}</h4>
      <p>{escape(str(node.get("conclusion") or ""))}</p>
      <small>本期变化：{escape(str(node.get("change_summary") or ""))}</small>
    </div>
    <span class="state-badge state-{escape(state)}">{escape(STATE_LABELS.get(state, state))}</span>
    <span class="logic-node-chevron" aria-hidden="true"></span>
  </summary>
  <div class="logic-node-body">
    <section class="node-thesis">
      <span>要验证的因果命题</span>
      <p>{escape(str(node.get("question") or ""))}</p>
    </section>
    {state_history}
    <section class="claim-event-section">
      <div class="node-subheading">
        <div><span>MARKET-KNOWN TIME</span><h5>信息事件历史</h5></div>
        <span>{int(node.get("mapped_claim_count") or 0)} 条观点 · {len(entities)} 个实体</span>
      </div>
      {event_history}
    </section>
    <dl class="node-follow-up">
      <div><dt>证据缺口</dt><dd><ul>{gaps}</ul></dd></div>
      <div><dt>下一验证</dt><dd>{next_validation}</dd></div>
    </dl>
    {entity_audit}
  </div>
</details>
"""

    def _render_state_history(self, node: dict[str, Any]) -> str:
        history = list(node.get("state_history") or [])
        if not history:
            return """
    <section class="node-state-history">
      <div class="node-subheading"><div><span>NODE STATE</span><h5>节点状态历史</h5></div></div>
      <p class="empty-entity">当前没有可复现的节点状态截面。</p>
    </section>"""
        points = []
        for index, snapshot in enumerate(history):
            state = str(snapshot.get("state") or "unresolved")
            previous_state = str(snapshot.get("previous_state") or "")
            revision_type = str(snapshot.get("revision_type") or "")
            if revision_type == "baseline" or not previous_state:
                transition = "建立基线"
            else:
                transition = (
                    f"{STATE_LABELS.get(previous_state, previous_state)} → "
                    f"{STATE_LABELS.get(state, state)}"
                )
            current_class = " is-current" if index == len(history) - 1 else ""
            points.append(
                f"""
        <li class="state-history-item{current_class}">
          <button class="state-history-point state-{escape(state)}" type="button"
            data-history-cutoff="{escape(str(snapshot.get('as_of_date') or ''))}"
            data-history-state-label="{escape(STATE_LABELS.get(state, state), quote=True)}"
            data-history-conclusion="{escape(str(snapshot.get('conclusion') or ''), quote=True)}"
            aria-pressed="false"
            title="{escape(str(snapshot.get('conclusion') or ''), quote=True)}">
            <time>{escape(str(snapshot.get('as_of_date') or ''))}</time>
            <span class="state-history-dot" aria-hidden="true"></span>
            <strong>{escape(STATE_LABELS.get(state, state))}</strong>
            <small>{escape(transition)}</small>
            <em>{escape(str(snapshot.get('change_summary') or snapshot.get('revision_rationale') or ''))}</em>
          </button>
        </li>"""
            )
        current = history[-1]
        current_state = str(current.get("state") or "unresolved")
        current_title = (
            f"当前截面 · {current.get('as_of_date') or ''} · "
            f"{STATE_LABELS.get(current_state, current_state)}"
        )
        return f"""
    <section class="node-state-history">
      <div class="node-subheading">
        <div><span>NODE STATE</span><h5>节点状态历史</h5></div>
        <button class="history-reset" type="button" data-history-reset>显示全部历史</button>
      </div>
      <p class="state-history-help">从左到右为真实研究截面；点击某个截面，只回看当时已经公开的信息。</p>
      <div class="state-history-scroll">
        <ol class="state-history-track">{''.join(points)}</ol>
      </div>
      <div class="history-selection" aria-live="polite">
        <strong data-history-selection-title>{escape(current_title)}</strong>
        <span data-history-selection-conclusion>{escape(str(current.get('conclusion') or ''))}</span>
      </div>
    </section>"""

    def _render_event_history(self, node: dict[str, Any]) -> str:
        groups = list(node.get("event_history_groups") or [])
        if not groups:
            return '<p class="empty-entity">当前没有映射到该节点的原子观点。</p>'
        filter_specs = (
            ("all", "全部"),
            ("support", "支持"),
            ("adverse", "反证 / 冲突"),
            ("boundary", "边界 / 约束"),
            ("branch", "新分支"),
            ("unresolved", "待判断"),
        )
        filters = "".join(
            (
                f'<button type="button" data-history-filter="{filter_id}"'
                f' class="history-filter{" is-active" if filter_id == "all" else ""}"'
                f' aria-pressed="{"true" if filter_id == "all" else "false"}">{label}</button>'
            )
            for filter_id, label in filter_specs
        )
        rendered_groups = []
        source_serial = 0
        for group_index, group in enumerate(groups):
            source_blocks = []
            for source in group.get("sources") or []:
                source_serial += 1
                source_blocks.append(
                    self._render_claim_source_group(
                        source,
                        open_by_default=group_index == 0 and source_serial <= 2,
                    )
                )
            revisions = list(group.get("state_revisions") or [])
            if revisions:
                revision_text = "；".join(
                    str(row.get("rationale") or "") for row in revisions
                )
                period_note = (
                    '<p class="period-interpretation"><strong>本期节点修订：</strong>'
                    f"{escape(revision_text)}</p>"
                )
            else:
                period_note = (
                    '<p class="period-interpretation">本期信息已进入节点账本；'
                    "是否改变判断以上方状态历史线为准。</p>"
                )
            open_attribute = " open" if group_index == 0 else ""
            rendered_groups.append(
                f"""
      <details class="claim-month-group" data-period="{escape(str(group.get('period_key') or ''))}"{open_attribute}>
        <summary>
          <span class="month-label">{escape(str(group.get('period_label') or ''))}</span>
          <span>{int(group.get('claim_count') or 0)} 条观点 · {len(group.get('sources') or [])} 份材料</span>
        </summary>
        <div class="claim-month-body">
          {period_note}
          {''.join(source_blocks)}
        </div>
      </details>"""
            )
        return f"""
      <div class="event-history-toolbar" role="toolbar" aria-label="信息事件筛选">
        <div class="history-filters">{filters}</div>
        <button type="button" class="history-expand" data-history-expand aria-pressed="false">展开全部历史</button>
      </div>
      <div class="claim-event-list">{''.join(rendered_groups)}</div>"""

    def _render_claim_source_group(
        self,
        source_group: dict[str, Any],
        *,
        open_by_default: bool,
    ) -> str:
        title = escape(
            str(source_group.get("source_title") or source_group.get("source_id") or "来源")
        )
        source_url = _rendered_source_url(
            str(source_group.get("source_url") or ""),
            project_dir=self.project_dir,
        )
        if source_url:
            escaped_url = escape(source_url, quote=True)
            if source_url.startswith(("http://", "https://")):
                source_link = (
                    f'<a href="{escaped_url}" target="_blank" rel="noopener">打开原文 ↗</a>'
                )
            else:
                source_link = f'<a href="{escaped_url}">打开原文 PDF</a>'
        else:
            source_link = '<span>原文链接未登记</span>'
        events = "".join(
            self._render_claim_event(event)
            for event in source_group.get("events") or []
        )
        open_attribute = " open" if open_by_default else ""
        published_at = escape(str(source_group.get("published_at") or "日期未明"))
        material_label = escape(
            MATERIAL_LABELS.get(
                str(source_group.get("material_class") or "other"), "其他"
            )
        )
        return f"""
          <details class="claim-source-group" data-published-at="{published_at}"{open_attribute}>
            <summary>
              <time datetime="{published_at}">{published_at}</time>
              <span class="source-group-title">{title}</span>
              <span class="source-group-count">{int(source_group.get('claim_count') or 0)} 条</span>
            </summary>
            <div class="claim-source-body">
              <div class="source-group-origin"><span class="material-tag">{material_label}</span>{source_link}</div>
              {events}
            </div>
          </details>"""

    def _render_claim_event(self, event: dict[str, Any]) -> str:
        direction = str(event.get("direction") or "neutral")
        direction_label = DIRECTION_LABELS.get(direction, "线索")
        published_at = escape(str(event.get("published_at") or ""))
        effect_group = _direction_filter_group(direction)
        period_parts = []
        effective_period = str(event.get("effective_period") or "").strip()
        target_period = str(event.get("target_period") or "").strip()
        if effective_period:
            period_parts.append(
                f'<span class="period-chip actual-period">实际：{escape(effective_period)}</span>'
            )
        if target_period:
            period_parts.append(
                f'<span class="period-chip target-period">预测：{escape(target_period)}</span>'
            )
        entities = "".join(
            f'<span class="entity-tag">{escape(str(entity))}</span>'
            for entity in event.get("entities") or []
        )
        downstream = "、".join(
            escape(str(item)) for item in event.get("downstream_impacts") or []
        )
        revisions = list(event.get("triggered_revisions") or [])
        revision_marker = ""
        if revisions:
            revision = revisions[0]
            previous_state = str(revision.get("previous_state") or "")
            new_state = str(revision.get("new_state") or "unresolved")
            transition = (
                f"{STATE_LABELS.get(previous_state, previous_state)} → "
                f"{STATE_LABELS.get(new_state, new_state)}"
                if previous_state
                else f"建立{STATE_LABELS.get(new_state, new_state)}基线"
            )
            revision_marker = (
                '<p class="claim-revision-marker"><strong>触发节点修订：</strong>'
                f"{escape(transition)}；{escape(str(revision.get('rationale') or ''))}</p>"
            )
        return f"""
<article class="claim-event effect-{escape(direction)}" data-direction="{escape(direction)}" data-effect-group="{escape(effect_group)}" data-published-at="{published_at}">
  <div class="claim-event-rail" aria-hidden="true"></div>
  <div class="claim-event-content">
    <div class="claim-event-meta">
      <span class="effect-label">{escape(direction_label)}</span>
      <span class="evidence-nature">{escape(EVIDENCE_NATURE_LABELS.get(str(event.get('evidence_nature') or 'opinion'), '观点'))}</span>
      {entities}
      {''.join(period_parts)}
    </div>
    <div class="claim-event-source"><span>{escape(str(event.get("source_location") or "原文位置未标注"))}</span></div>
    <p class="claim-event-statement">{escape(str(event.get("statement") or ""))}</p>
    <p class="claim-event-rationale"><strong>影响逻辑：</strong>{escape(str(event.get("rationale") or "尚未记录映射依据。"))}</p>
    {revision_marker}
    {f'<p class="claim-event-downstream"><strong>向下游传导：</strong>{downstream}</p>' if downstream else ''}
  </div>
</article>"""

    def _render_demand_party_list(self, node: dict[str, Any]) -> str:
        demand_parties = dict(node.get("demand_parties") or {})
        group_specs = (
            ("current", "当前需求方"),
            ("potential_future", "潜在未来需求方"),
        )
        groups = []
        for group_id, label in group_specs:
            items = "".join(
                f"<li>{escape(str(party))}</li>"
                for party in demand_parties.get(group_id) or []
            )
            groups.append(
                f"""
    <section class="demand-party-group" data-demand-party-group="{group_id}">
      <h5>{label}</h5>
      <ul>{items}</ul>
    </section>"""
            )
        return f"""
<article class="logic-node demand-party-node" data-logic-node-id="{escape(str(node.get("logic_node_id") or ""))}" data-render-mode="demand-party-list">
  <div class="logic-node-heading">
    <div>
      <span>{escape(str(node.get("logic_node_id") or ""))}</span>
      <h4>{escape(str(node.get("title") or ""))}</h4>
    </div>
  </div>
  <div class="demand-party-grid">
    {''.join(groups)}
  </div>
</article>
"""

    def _render_demand_quantity_matrix(self, node: dict[str, Any]) -> str:
        rows = list(node.get("demand_quantity_rows") or [])
        current_rows = [
            row for row in rows if row.get("forecast_group") == "classified"
        ]
        potential_future_rows = [
            row for row in rows if row.get("forecast_group") == "potential_future"
        ]
        other_rows = [
            row for row in rows if row.get("forecast_group") == "other"
        ]
        quality_labels = {
            "direct": "直接映射",
            "proxy": "代理映射",
            "sample": "样本映射",
            "gap": "数据缺口",
            "unmapped": "不做映射",
        }

        def render_row(row: dict[str, Any]) -> str:
            mapping_quality = str(row.get("mapping_quality") or "")
            information_types = list(
                dict.fromkeys(
                    DEMAND_INFORMATION_TYPE_LABELS.get(
                        str(source.get("material_class") or "other"),
                        "市场消息",
                    )
                    for source in row.get("sources") or []
                )
            )
            information_type_text = " / ".join(information_types) or "暂无来源"
            return f"""
        <tr>
          <td>{self._render_demand_quantity_sources(row)}</td>
          <td>{escape(str(row.get("target_period") or ""))}</td>
          <td>{escape(information_type_text)}</td>
          <td><strong>{escape(str(row.get("metric") or ""))}</strong><div class="demand-quantity-value">{escape(str(row.get("quantity") or ""))}</div><p>{escape(quality_labels.get(mapping_quality, mapping_quality))} · {escape(str(row.get("caveat") or ""))}</p></td>
        </tr>"""

        def group_by_party(
            group_rows: list[dict[str, Any]],
        ) -> dict[str, list[dict[str, Any]]]:
            grouped: dict[str, list[dict[str, Any]]] = {}
            for row in group_rows:
                grouped.setdefault(str(row.get("demand_party") or ""), []).append(
                    row
                )
            return grouped

        def render_category(
            category: str,
            category_rows: list[dict[str, Any]],
        ) -> str:
            table_rows = "".join(render_row(row) for row in category_rows)
            if not table_rows:
                table_rows = (
                    '<tr><td colspan="4" class="empty-state">'
                    "暂无已登记信息。</td></tr>"
                )
            return f"""
    <details class="demand-quantity-category" data-demand-quantity-category="{escape(category, quote=True)}">
      <summary>
        <strong>{escape(category)}</strong>
        <span>{len(category_rows)} 条信息</span>
      </summary>
      <div class="demand-quantity-table-wrap" role="region" aria-label="{escape(category, quote=True)}需求信息" tabindex="0" data-demand-category-table>
        <table class="demand-quantity-table">
          <thead><tr><th>来源</th><th>期间</th><th>信息类型</th><th>具体信息</th></tr></thead>
          <tbody>{table_rows}</tbody>
        </table>
      </div>
    </details>"""

        current_by_party = group_by_party(current_rows)
        potential_by_party = group_by_party(potential_future_rows)
        demand_parties = dict(node.get("demand_parties") or {})
        current_categories = [
            (str(party), current_by_party.get(str(party), []))
            for party in demand_parties.get("current") or []
        ]
        potential_categories = [
            (str(party), potential_by_party.get(str(party), []))
            for party in demand_parties.get("potential_future") or []
        ]
        other_by_category: dict[str, list[dict[str, Any]]] = {}
        for row in other_rows:
            other_by_category.setdefault(
                str(row.get("metric") or "其它信息"), []
            ).append(row)
        other_categories = list(other_by_category.items())

        def render_tier(
            number: int,
            label: str,
            group_id: str,
            categories: list[tuple[str, list[dict[str, Any]]]],
        ) -> str:
            category_html = "\n".join(
                render_category(category, category_rows)
                for category, category_rows in categories
            )
            information_count = sum(
                len(category_rows) for _, category_rows in categories
            )
            return f"""
  <details class="demand-quantity-tier" data-demand-forecast-group="{group_id}">
    <summary>
      <span class="demand-tier-number">{number:02d}</span>
      <strong>{escape(label)}</strong>
      <span class="demand-tier-count">{len(categories)} 类 · {information_count} 条信息</span>
    </summary>
    <div class="demand-quantity-tier-body">{category_html}</div>
  </details>"""

        tiers_html = "\n".join(
            (
                render_tier(1, "当前需求方", "current", current_categories),
                render_tier(
                    2,
                    "潜在未来需求方",
                    "potential_future",
                    potential_categories,
                ),
                render_tier(3, "其它分类", "other", other_categories),
            )
        )
        return f"""
<article class="logic-node demand-quantity-node" data-logic-node-id="{escape(str(node.get("logic_node_id") or ""))}" data-render-mode="demand-quantity-matrix">
  <div class="logic-node-heading">
    <div>
      <span>{escape(str(node.get("logic_node_id") or ""))}</span>
      <h4>{escape(str(node.get("title") or ""))}</h4>
    </div>
  </div>
  <div class="demand-quantity-tier-list">{tiers_html}</div>
</article>
"""

    def _render_demand_quantity_sources(self, row: dict[str, Any]) -> str:
        links = []
        for source in row.get("sources") or []:
            title = escape(
                str(source.get("source_title") or source.get("source_id") or "来源")
            )
            url = _rendered_source_url(
                str(source.get("source_url") or ""),
                project_dir=self.project_dir,
            )
            published_at = escape(str(source.get("published_at") or ""))
            if url:
                escaped_url = escape(url, quote=True)
                if url.startswith(("http://", "https://")):
                    link = (
                        f'<a href="{escaped_url}" target="_blank" rel="noopener">'
                        f"{title}</a>"
                    )
                else:
                    link = f'<a href="{escaped_url}">{title}</a>'
            else:
                link = title
            links.append(f"{published_at} · {link}" if published_at else link)
        return "<br>".join(links) if links else "暂无独立来源"

    def _render_entity_module(self, entity: dict[str, Any]) -> str:
        entity_name = escape(str(entity.get("entity_name") or "未命名实体"))
        effect = str(entity.get("investment_effect") or "unclear")
        effect_label = escape(ENTITY_EFFECT_LABELS.get(effect, "待判断"))
        groups = _group_claims_by_source(list(entity.get("claims") or []))
        rows = "\n".join(
            self._render_entity_source_row(group) for group in groups
        )
        if not rows:
            rows = (
                '<tr><td colspan="3" class="empty-state">'
                "当前没有经过复核的实体级材料。</td></tr>"
            )
        gaps = "；".join(
            escape(str(item)) for item in entity.get("evidence_gaps") or []
        )
        next_validation = escape(str(entity.get("next_validation") or ""))
        supplemental = ""
        if gaps or next_validation:
            supplemental = f"""
        <dl class="entity-next">
          {f'<div><dt>仍缺什么</dt><dd>{gaps}</dd></div>' if gaps else ''}
          {f'<div><dt>下一验证</dt><dd>{next_validation}</dd></div>' if next_validation else ''}
        </dl>
"""
        return f"""
<details class="entity-module" data-entity-id="{escape(str(entity.get("entity_id") or ""))}">
  <summary class="entity-heading">
    <div>
      <strong>{entity_name}</strong>
      <span>{int(entity.get("material_count") or 0)} 份材料 · {int(entity.get("claim_count") or 0)} 条观点</span>
    </div>
    <span class="entity-effect effect-{escape(effect)}">{effect_label}</span>
    <span class="entity-chevron" aria-hidden="true"></span>
  </summary>
  <div class="entity-body">
    <section class="entity-evaluation">
      <h5>截面变化与评估</h5>
      <p>{escape(str(entity.get("assessment") or ""))}</p>
      <div class="entity-change">
        <strong>相较上一截面</strong>
        <p>{escape(str(entity.get("change_summary") or ""))}</p>
      </div>
      {supplemental}
    </section>
    <div class="entity-table-wrap" role="region" aria-label="{entity_name}材料与观点" tabindex="0">
      <table class="entity-table">
        <colgroup>
          <col class="col-material">
          <col class="col-type">
          <col class="col-claims">
        </colgroup>
        <thead>
          <tr>
            <th scope="col">材料（含链接）</th>
            <th scope="col">类型</th>
            <th scope="col">观点列表</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
</details>
"""

    def _render_entity_source_row(self, group: dict[str, Any]) -> str:
        title = escape(
            str(group.get("source_title") or group.get("source_id") or "来源")
        )
        published_at = escape(str(group.get("published_at") or ""))
        material_class = str(group.get("material_class") or "other")
        material_label = escape(MATERIAL_LABELS.get(material_class, "其他"))
        source_url = _rendered_source_url(
            str(group.get("source_url") or ""),
            project_dir=self.project_dir,
        )
        source_link = title
        if source_url:
            escaped_url = escape(source_url, quote=True)
            if source_url.startswith(("http://", "https://")):
                source_link = (
                    f'<a href="{escaped_url}" target="_blank" rel="noopener">'
                    f"{title}<span aria-hidden=\"true\">↗</span></a>"
                )
            else:
                source_link = (
                    f'<a href="{escaped_url}">{title}'
                    '<span aria-hidden="true">PDF</span></a>'
                )
        bullets = "\n".join(
            _render_entity_claim(claim, index)
            for index, claim in enumerate(group.get("claims") or [], start=1)
        )
        return f"""
<tr class="entity-source-row">
  <td class="source-report">
    <time datetime="{published_at}">{published_at}</time>
    {source_link}
  </td>
  <td class="source-type"><span class="material-tag">{material_label}</span></td>
  <td class="source-claims"><ul class="claim-list">{bullets}</ul></td>
</tr>
"""

    def _render_source_row(self, group: dict[str, Any]) -> str:
        title = escape(
            str(group.get("source_title") or group.get("source_id") or "来源")
        )
        published_at = escape(str(group.get("published_at") or ""))
        material_class = str(group.get("material_class") or "other")
        material_label = escape(MATERIAL_LABELS.get(material_class, "其他"))
        source_url = _rendered_source_url(
            str(group.get("source_url") or ""),
            project_dir=self.project_dir,
        )
        source_link = title
        if source_url:
            escaped_url = escape(source_url, quote=True)
            if source_url.startswith(("http://", "https://")):
                source_link = (
                    f'<a href="{escaped_url}" target="_blank" rel="noopener">'
                    f'{title}<span aria-hidden="true">↗</span></a>'
                )
            else:
                source_link = (
                    f'<a href="{escaped_url}">{title}'
                    '<span aria-hidden="true">PDF</span></a>'
                )
        bullets = "\n".join(
            _render_claim(claim, index)
            for index, claim in enumerate(group.get("claims") or [], start=1)
        )
        return f"""
<tr class="source-row">
  <td class="source-date"><time datetime="{published_at}">{published_at}</time></td>
  <td class="source-type"><span class="material-tag">{material_label}</span></td>
  <td class="source-report">{source_link}</td>
  <td class="source-claims">
    <ul class="claim-list">
      {bullets}
    </ul>
  </td>
</tr>
"""


def _render_claim(claim: dict[str, Any], index: int) -> str:
    location = escape(str(claim.get("source_location") or "原文位置未标注"))
    statement = escape(str(claim.get("statement") or ""))
    mappings = sorted(
        list(claim.get("logic_mappings") or []),
        key=lambda row: (
            0 if str(row.get("mapping_role") or "") == "primary" else 1,
            str(row.get("logic_node_id") or ""),
        ),
    )
    mapping_tags = "".join(
        (
            f'<span class="mapping-tag mapping-{escape(str(row.get("direction") or "neutral"))}">'
            f'{escape(str(row.get("logic_node_title") or row.get("logic_node_id") or ""))}'
            f' · {escape(DIRECTION_LABELS.get(str(row.get("direction") or "neutral"), "线索"))}</span>'
        )
        for row in mappings
    )
    return f"""
<li>
  <div class="claim-heading">
    <span class="claim-index">观点 {index:02d}</span>
    <span class="claim-location">{location}</span>
  </div>
  {f'<div class="mapping-tags">{mapping_tags}</div>' if mapping_tags else ''}
  <p>{statement}</p>
</li>
"""


def _render_entity_claim(claim: dict[str, Any], index: int) -> str:
    location = escape(str(claim.get("source_location") or "原文位置未标注"))
    statement = escape(str(claim.get("statement") or ""))
    mapping = next(iter(claim.get("logic_mappings") or []), {})
    direction = str(mapping.get("direction") or "neutral")
    return f"""
<li>
  <div class="claim-heading">
    <span class="claim-index">观点 {index:02d}</span>
    <span class="mapping-tag mapping-{escape(direction)}">{escape(DIRECTION_LABELS.get(direction, "线索"))}</span>
    <span class="claim-location">{location}</span>
  </div>
  <p>{statement}</p>
</li>
"""


def _group_claims_by_source(
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for claim in claims:
        source_id = str(claim.get("source_id") or "")
        if source_id not in grouped:
            grouped[source_id] = {
                "source_id": source_id,
                "published_at": claim.get("published_at"),
                "material_class": claim.get("material_class"),
                "source_title": claim.get("source_title"),
                "source_url": claim.get("source_url"),
                "claims": [],
            }
            order.append(source_id)
        grouped[source_id]["claims"].append(claim)
    return [grouped[source_id] for source_id in order]


def _rendered_source_url(url: str, *, project_dir: Path) -> str:
    if not url:
        return ""
    if url.startswith(("http://", "https://")):
        return url
    path = Path(url)
    if path.is_absolute():
        try:
            return path.resolve().relative_to(project_dir).as_posix()
        except ValueError:
            return ""
    return path.as_posix()


def _report_css() -> str:
    return """
:root {
  color-scheme: light;
  --page: #f3f5f7;
  --surface: #ffffff;
  --surface-soft: #eef3f7;
  --ink: #273342;
  --muted: #697887;
  --line: #d9e0e6;
  --line-strong: #bdc8d2;
  --blue: #245f83;
  --blue-soft: #e7f0f5;
  --rust: #a95e46;
  --green: #39705d;
  --shadow: 0 12px 32px rgba(36, 55, 72, 0.08);
}

* { box-sizing: border-box; }

html {
  scroll-behavior: smooth;
  background: var(--page);
}

body {
  margin: 0;
  background: var(--page);
  color: var(--ink);
  font-family: "Avenir Next", "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", sans-serif;
  font-size: 16px;
  line-height: 1.75;
  letter-spacing: 0;
}

a { color: var(--blue); }

.report-header {
  background: var(--surface);
  border-bottom: 1px solid var(--line);
}

.report-header-inner,
.top-nav-inner,
.report-main,
.report-footer {
  width: min(1180px, calc(100% - 48px));
  margin: 0 auto;
}

.report-header-inner {
  padding: 62px 0 42px;
}

.report-label {
  color: var(--rust);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.12em;
}

h1 {
  max-width: 860px;
  margin: 12px 0 10px;
  color: #18364d;
  font-family: "Baskerville", "Songti SC", serif;
  font-size: clamp(36px, 5vw, 62px);
  font-weight: 600;
  line-height: 1.08;
  letter-spacing: 0;
}

.report-deck {
  max-width: 780px;
  margin: 0;
  color: var(--muted);
  font-size: 18px;
}

.report-meta {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  max-width: 760px;
  margin-top: 34px;
  border-top: 1px solid var(--line);
}

.report-meta div {
  min-width: 0;
  padding: 16px 20px 0 0;
}

.report-meta span {
  display: block;
  color: var(--muted);
  font-size: 12px;
}

.report-meta strong {
  display: block;
  margin-top: 2px;
  color: #24445c;
  font-size: 19px;
  font-weight: 650;
}

.top-nav {
  position: sticky;
  z-index: 30;
  top: 0;
  overflow-x: auto;
  border-bottom: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: saturate(140%) blur(14px);
}

.top-nav-inner {
  display: flex;
  min-width: max-content;
}

.top-nav a {
  padding: 14px 18px;
  border-bottom: 2px solid transparent;
  color: var(--muted);
  font-size: 13px;
  font-weight: 650;
  text-decoration: none;
  transition: color 160ms ease, border-color 160ms ease;
}

.top-nav a:first-child { padding-left: 0; }
.top-nav a:hover,
.top-nav a.is-active {
  border-color: var(--blue);
  color: var(--blue);
}

.report-main { padding: 24px 0 80px; }

.decision-section {
  margin: 0 0 34px;
  padding: 34px 0 44px;
  border-bottom: 1px solid var(--line-strong);
}

.decision-kicker {
  color: var(--rust);
  font-size: 11px;
  font-weight: 760;
  letter-spacing: 0.12em;
}

.decision-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 28px;
  margin-top: 8px;
}

.decision-heading h2 {
  margin: 0;
  color: #183f5b;
  font-family: "Baskerville", "Songti SC", serif;
  font-size: 32px;
  line-height: 1.2;
}

.decision-heading p {
  max-width: 860px;
  margin: 10px 0 0;
  color: #455565;
}

.decision-update {
  display: grid;
  grid-template-columns: 108px minmax(0, 1fr);
  gap: 14px;
  margin: -8px 0 28px;
  padding: 14px 16px;
  border-left: 2px solid var(--rust);
  background: #f7f9fa;
}

.decision-update strong {
  color: var(--rust);
  font-size: 11px;
  letter-spacing: .08em;
}

.decision-update p {
  margin: 0;
  color: #52616e;
  font-size: 13px;
}

.action-badge,
.action-inline {
  display: inline-block;
  flex: 0 0 auto;
  border: 1px solid currentColor;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 760;
  white-space: nowrap;
}

.action-badge { padding: 5px 10px; }
.action-inline { padding: 2px 7px; }
.action-actionable_long { color: var(--green); background: #eaf3ef; }
.action-watch_only { color: #8a6232; background: #f7f0e7; }
.action-no_action { color: #8a4f48; background: #f8eae7; }

.delta-list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  margin-top: 28px;
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
}

.delta-list article {
  min-width: 0;
  padding: 18px 24px 18px 0;
  border-right: 1px solid var(--line);
}

.delta-list article + article { padding-left: 24px; }
.delta-list article:last-child { border-right: 0; }
.delta-list span {
  color: var(--rust);
  font-size: 11px;
  font-weight: 760;
}
.delta-list p {
  margin: 5px 0 0;
  color: #354a5a;
  font-size: 14px;
}

.decision-audit {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
  margin-top: 24px;
}

.decision-audit > div { min-width: 0; }
.decision-audit h3 {
  margin: 0 0 8px;
  color: #36596f;
  font-size: 13px;
}
.decision-audit p,
.decision-audit ul {
  margin: 0;
  color: var(--muted);
  font-size: 13px;
}
.decision-audit ul { padding-left: 18px; }

.gate-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 10px;
  padding: 0 !important;
  list-style: none;
}
.gate-list li {
  display: flex;
  gap: 4px;
  align-items: center;
}
.gate-pass { color: var(--green) !important; }
.gate-fail { color: var(--muted) !important; }

.decision-table-heading { margin-top: 32px; }
.company-table {
  width: 100%;
  min-width: 1120px;
  border-collapse: collapse;
  table-layout: fixed;
}
.company-table th,
.company-table td {
  padding: 13px 14px;
  border-bottom: 1px solid var(--line);
  font-size: 13px;
  text-align: left;
  vertical-align: top;
}
.company-table th {
  background: #edf2f5;
  color: #526575;
  font-size: 11px;
}
.company-table th:nth-child(1) { width: 130px; }
.company-table th:nth-child(2) { width: 180px; }
.company-table th:nth-child(3) { width: 260px; }
.company-table th:nth-child(4) { width: 220px; }
.company-table th:nth-child(6) { width: 100px; }
.company-table td strong { display: block; color: #264a64; }
.company-table td small { display: block; color: var(--muted); }
.company-table tr:last-child td { border-bottom: 0; }

.lens-section {
  border-bottom: 1px solid var(--line-strong);
  background: transparent;
}

.lens-heading {
  display: grid;
  grid-template-columns: 58px minmax(0, 1fr) auto 18px;
  gap: 18px;
  align-items: center;
  padding: 34px 0;
  cursor: pointer;
  list-style: none;
}

.lens-heading::-webkit-details-marker { display: none; }

.lens-number {
  color: var(--rust);
  font-family: "Baskerville", serif;
  font-size: 28px;
}

.lens-heading p {
  margin: 0 0 2px;
  color: var(--muted);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.12em;
}

.lens-heading h2 {
  margin: 0;
  color: #1d4967;
  font-size: 26px;
  line-height: 1.2;
  letter-spacing: 0;
}

.lens-count {
  color: var(--muted);
  font-size: 13px;
}

.lens-chevron {
  width: 10px;
  height: 10px;
  border-right: 2px solid var(--blue);
  border-bottom: 2px solid var(--blue);
  transform: rotate(45deg);
  transition: transform 180ms ease;
}

.lens-section:not([open]) .lens-chevron { transform: rotate(-45deg); }

.lens-body {
  padding: 0 0 56px 76px;
  animation: reveal 220ms ease both;
}

@keyframes reveal {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

.logic-note {
  max-width: 920px;
  padding: 20px 24px;
  border-left: 3px solid var(--rust);
  background: var(--surface);
  box-shadow: var(--shadow);
}

.logic-note h3,
.logic-note p { margin: 0; }

.logic-note h3 {
  color: var(--rust);
  font-size: 12px;
  font-weight: 750;
}

.logic-note p {
  margin-top: 7px;
  color: #455565;
}

.logic-state-section,
.timeline,
.conclusion-panel {
  margin-top: 42px;
}

.logic-node-list,
.logic-chain-map,
.derived-view-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.logic-chain-map { gap: 0; }

.derived-view-section { margin-top: 42px; }
.derived-view-list { gap: 10px; }

.logic-node {
  padding: 20px 22px;
  border: 1px solid var(--line);
  border-left: 3px solid #6f8fa3;
  border-radius: 5px;
  background: var(--surface);
}

.causal-node {
  position: relative;
  padding: 0;
  border-left-width: 1px;
  border-radius: 0;
  overflow: visible;
}

.causal-node + .causal-node { margin-top: 18px; }
.causal-node:not(:last-child)::after {
  position: absolute;
  z-index: 2;
  bottom: -19px;
  left: 42px;
  width: 1px;
  height: 18px;
  background: var(--rust);
  content: "";
}

.logic-node-summary {
  display: grid;
  grid-template-columns: 52px minmax(0, 1fr) auto 18px;
  gap: 16px;
  align-items: center;
  min-height: 116px;
  padding: 18px 20px;
  cursor: pointer;
  list-style: none;
  background: linear-gradient(90deg, #ffffff 0%, #fbfcfd 100%);
}
.logic-node-summary::-webkit-details-marker { display: none; }
.logic-step {
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  border: 1px solid #c8d7df;
  border-radius: 50%;
  background: #f2f6f8;
  color: var(--blue);
  font-family: "Baskerville", "Songti SC", serif;
  font-size: 17px;
}
.causal-node .logic-node-heading {
  display: block;
  min-width: 0;
}
.causal-node .logic-node-heading > span {
  display: block;
  color: var(--muted);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: .03em;
}
.causal-node .logic-node-heading h4 { margin-top: 2px; }
.causal-node .logic-node-heading p {
  margin: 6px 0 0;
  color: #344957;
  font-size: 14px;
}
.causal-node .logic-node-heading small {
  display: block;
  margin-top: 5px;
  color: var(--muted);
  font-size: 11px;
}
.logic-node-chevron {
  width: 9px;
  height: 9px;
  border-right: 2px solid var(--blue);
  border-bottom: 2px solid var(--blue);
  transform: rotate(45deg);
  transition: transform 180ms ease;
}
.causal-node[open] .logic-node-chevron { transform: rotate(225deg); }
.logic-node-body {
  padding: 0 20px 24px 88px;
  border-top: 1px solid var(--line);
  background: #fcfdfd;
  animation: reveal 180ms ease both;
}
.node-thesis {
  display: grid;
  grid-template-columns: 142px minmax(0, 1fr);
  gap: 18px;
  padding: 17px 0;
  border-bottom: 1px solid var(--line);
}
.node-thesis span,
.node-subheading span {
  color: var(--muted);
  font-size: 11px;
  font-weight: 700;
}
.node-thesis p {
  margin: 0;
  color: #334b5b;
  font-size: 14px;
}
.node-state-history {
  padding: 20px 0 22px;
  border-bottom: 1px solid var(--line);
}
.node-subheading > div > span {
  display: block;
  margin-bottom: 3px;
  color: var(--rust);
  font-size: 9px;
  font-weight: 780;
  letter-spacing: .12em;
}
.history-reset,
.history-expand,
.history-filter {
  border: 1px solid var(--line-strong);
  border-radius: 3px;
  background: #fff;
  color: #536676;
  cursor: pointer;
  font: inherit;
  font-size: 10px;
  font-weight: 700;
}
.history-reset,
.history-expand { padding: 6px 9px; }
.history-reset:hover,
.history-expand:hover,
.history-filter:hover,
.history-filter.is-active {
  border-color: #6d8899;
  background: #eef3f6;
  color: var(--blue);
}
.state-history-help,
.history-selection {
  margin: 8px 0 0;
  color: var(--muted);
  font-size: 11px;
}
.history-selection {
  color: #5a6e7c;
  font-weight: 650;
}
.history-selection {
  display: grid;
  gap: 3px;
  padding: 9px 11px;
  border-left: 2px solid #8da4b2;
  background: #f5f8f9;
}
.history-selection strong { color: #31536a; font-size: 11px; }
.history-selection span { color: #637381; font-size: 11px; font-weight: 500; }
.state-history-scroll {
  overflow-x: auto;
  margin-top: 14px;
  padding: 4px 2px 10px;
}
.state-history-track {
  display: flex;
  min-width: max-content;
  margin: 0;
  padding: 0;
  list-style: none;
}
.state-history-item {
  position: relative;
  width: 196px;
  padding-right: 24px;
}
.state-history-item:not(:last-child)::after {
  position: absolute;
  top: 32px;
  right: -1px;
  left: 18px;
  height: 1px;
  background: #b8c8d1;
  content: "";
}
.state-history-point {
  position: relative;
  z-index: 1;
  display: grid;
  justify-items: start;
  width: 100%;
  padding: 0;
  border: 0;
  background: transparent;
  color: inherit;
  cursor: pointer;
  text-align: left;
}
.state-history-point time {
  color: var(--muted);
  font-family: "Baskerville", "Songti SC", serif;
  font-size: 12px;
}
.state-history-dot {
  width: 12px;
  height: 12px;
  margin: 7px 0 8px;
  border: 3px solid #fff;
  border-radius: 50%;
  outline: 1px solid #8aa0ad;
  background: #90a4b1;
}
.state-strengthening .state-history-dot,
.state-confirmed .state-history-dot { background: var(--green); }
.state-weakening .state-history-dot,
.state-refuted .state-history-dot { background: #a45345; }
.state-weak .state-history-dot { background: #b47a34; }
.state-history-point[aria-pressed="true"] .state-history-dot,
.state-history-item.is-current .state-history-dot {
  outline: 2px solid var(--rust);
  outline-offset: 2px;
}
.state-history-point strong {
  color: #274b63;
  font-size: 12px;
}
.state-history-point small {
  margin-top: 2px;
  color: var(--rust);
  font-size: 10px;
  font-weight: 700;
}
.state-history-point em {
  display: -webkit-box;
  overflow: hidden;
  margin-top: 4px;
  color: var(--muted);
  font-size: 10px;
  font-style: normal;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}
.claim-event-section { padding-top: 20px; }
.node-subheading {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 18px;
}
.node-subheading h5 {
  margin: 0;
  color: #234b66;
  font-size: 15px;
}
.claim-event-list {
  display: grid;
  gap: 10px;
  margin-top: 14px;
}
.event-history-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 12px;
  padding: 9px 10px;
  border: 1px solid var(--line);
  background: #f7f9fa;
}
.history-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}
.history-filter { padding: 5px 8px; }
.claim-month-group,
.claim-source-group {
  border: 1px solid var(--line);
  background: #fff;
}
.claim-month-group > summary,
.claim-source-group > summary {
  display: grid;
  align-items: center;
  cursor: pointer;
  list-style: none;
}
.claim-month-group > summary::-webkit-details-marker,
.claim-source-group > summary::-webkit-details-marker { display: none; }
.claim-month-group > summary {
  grid-template-columns: minmax(120px, .5fr) minmax(0, 1fr);
  gap: 16px;
  padding: 12px 15px;
  background: #edf2f5;
  color: var(--muted);
  font-size: 11px;
}
.month-label {
  color: #234b66;
  font-family: "Baskerville", "Songti SC", serif;
  font-size: 16px;
  font-weight: 700;
}
.claim-month-body {
  padding: 10px;
  background: #f8fafb;
}
.period-interpretation {
  margin: 0 0 9px;
  padding: 8px 10px;
  border-left: 2px solid var(--rust);
  background: #fff;
  color: #637381;
  font-size: 11px;
}
.claim-source-group + .claim-source-group { margin-top: 8px; }
.claim-source-group > summary {
  grid-template-columns: 92px minmax(0, 1fr) auto;
  gap: 12px;
  padding: 11px 12px;
  color: #3c5262;
}
.claim-source-group > summary time {
  color: var(--blue);
  font-size: 11px;
  font-weight: 760;
}
.source-group-title {
  overflow: hidden;
  font-size: 12px;
  font-weight: 680;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.source-group-count {
  color: var(--muted);
  font-size: 10px;
}
.claim-source-body {
  padding: 0 12px 12px;
  border-top: 1px solid var(--line);
}
.source-group-origin {
  display: flex;
  gap: 8px;
  align-items: center;
  padding: 9px 0;
  color: var(--muted);
  font-size: 11px;
}
.source-group-origin a { font-weight: 700; text-decoration: none; }
.source-group-origin a:hover { text-decoration: underline; }
.claim-event + .claim-event { margin-top: 9px; }
.claim-month-group[hidden],
.claim-source-group[hidden],
.claim-event[hidden] { display: none; }
.claim-event {
  display: grid;
  grid-template-columns: 5px minmax(0, 1fr);
  gap: 13px;
}
.claim-event-rail {
  border-radius: 3px;
  background: #90a4b1;
}
.effect-support .claim-event-rail { background: var(--green); }
.effect-refute .claim-event-rail,
.effect-conflict .claim-event-rail { background: #a45345; }
.effect-boundary .claim-event-rail,
.effect-constraint .claim-event-rail { background: #b47a34; }
.effect-new_branch .claim-event-rail { background: #526f9a; }
.claim-event-content {
  padding: 14px 16px;
  border: 1px solid var(--line);
  background: #fff;
}
.claim-event-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 9px;
  align-items: center;
  color: var(--muted);
  font-size: 10px;
}
.claim-event-meta time {
  color: #244b66;
  font-size: 11px;
  font-weight: 760;
}
.effect-label {
  padding: 1px 6px;
  border: 1px solid currentColor;
  border-radius: 3px;
  color: #77604a;
  font-weight: 720;
}
.effect-support .effect-label { color: var(--green); }
.effect-refute .effect-label,
.effect-conflict .effect-label { color: #995344; }
.effect-new_branch .effect-label { color: #4c6791; }
.evidence-nature,
.entity-tag,
.period-chip {
  padding: 2px 6px;
  border-radius: 2px;
  background: #eef2f4;
  color: #5c6d79;
  font-size: 9px;
  font-weight: 680;
}
.entity-tag { background: #f4f0ea; color: #755f49; }
.actual-period { background: #edf5f1; color: #486f5c; }
.target-period { background: #eef1f7; color: #536b91; }
.claim-event-source {
  display: flex;
  flex-wrap: wrap;
  gap: 7px 12px;
  margin-top: 7px;
  font-size: 12px;
  font-weight: 680;
}
.claim-event-source a { text-decoration: none; }
.claim-event-source a:hover { text-decoration: underline; }
.claim-event-source span { color: var(--muted); font-weight: 500; }
.claim-event-statement {
  margin: 9px 0 0;
  color: #344957;
  font-size: 14px;
}
.claim-event-rationale,
.claim-event-downstream,
.claim-revision-marker {
  margin: 7px 0 0;
  color: #637381;
  font-size: 12px;
}
.claim-event-rationale strong,
.claim-event-downstream strong,
.claim-revision-marker strong { color: #486274; }
.claim-revision-marker {
  padding: 7px 9px;
  border-left: 2px solid var(--rust);
  background: #fbf6ef;
  color: #735c43;
}
.node-follow-up {
  margin: 20px 0 0;
  padding: 14px 16px;
  border: 1px solid var(--line);
  background: #f4f7f9;
}
.node-follow-up > div {
  display: grid;
  grid-template-columns: 88px minmax(0, 1fr);
  gap: 12px;
}
.node-follow-up > div + div { margin-top: 8px; }
.node-follow-up dt { color: var(--muted); font-size: 11px; }
.node-follow-up dd { margin: 0; color: #455565; font-size: 12px; }
.node-follow-up ul { margin: 0; padding-left: 17px; }
.node-audit {
  margin-top: 18px;
  border-top: 1px solid var(--line-strong);
}
.node-audit > summary {
  padding: 12px 0;
  color: var(--blue);
  cursor: pointer;
  font-size: 12px;
  font-weight: 700;
}
.node-audit .entity-list { margin-top: 0; }

.logic-node-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
}
.logic-node-heading > div { min-width: 0; }
.logic-node-heading > div > span {
  display: block;
  color: var(--muted);
  font-size: 10px;
  font-weight: 700;
}
.logic-node h4 {
  margin: 2px 0 0;
  color: #244b66;
  font-size: 17px;
  line-height: 1.35;
}
.demand-party-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  margin-top: 18px;
}
.demand-party-group {
  padding: 16px 18px;
  border: 1px solid var(--line);
  border-radius: 4px;
  background: #f7fafb;
}
.demand-party-group h5 {
  margin: 0;
  color: #244b66;
  font-size: 14px;
}
.demand-party-group ul {
  margin: 10px 0 0;
  padding-left: 18px;
  color: #354856;
}
.demand-party-group li + li { margin-top: 7px; }
.demand-quantity-tier-list {
  display: grid;
  gap: 10px;
  margin-top: 16px;
}
.demand-quantity-tier {
  border: 1px solid #d9e3e8;
  border-radius: 6px;
  background: #fbfcfc;
  overflow: hidden;
}
.demand-quantity-tier > summary,
.demand-quantity-category > summary {
  list-style: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  user-select: none;
}
.demand-quantity-tier > summary::-webkit-details-marker,
.demand-quantity-category > summary::-webkit-details-marker {
  display: none;
}
.demand-quantity-tier > summary {
  padding: 13px 15px;
  color: #183e58;
  background: #f5f8f9;
  font-size: 13px;
}
.demand-quantity-tier > summary::after,
.demand-quantity-category > summary::after {
  content: "+";
  margin-left: auto;
  color: #607887;
  font-size: 16px;
  font-weight: 650;
}
.demand-quantity-tier[open] > summary::after,
.demand-quantity-category[open] > summary::after {
  content: "−";
}
.demand-tier-number {
  color: #7391a3;
  font-size: 10px;
  letter-spacing: .08em;
}
.demand-tier-count {
  margin-left: 2px;
  color: var(--muted);
  font-size: 11px;
}
.demand-quantity-tier-body {
  display: grid;
  gap: 9px;
  padding: 11px;
  border-top: 1px solid #d9e3e8;
}
.demand-quantity-category {
  border: 1px solid #e0e7ea;
  border-radius: 5px;
  background: #fff;
  overflow: hidden;
}
.demand-quantity-category > summary {
  padding: 10px 12px;
  color: #244b66;
  font-size: 12px;
}
.demand-quantity-category > summary span {
  color: var(--muted);
  font-size: 11px;
}
.demand-quantity-category .demand-quantity-table-wrap {
  border: 0;
  border-top: 1px solid var(--line);
  border-radius: 0;
}
.demand-quantity-table-wrap {
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: 4px;
  background: #fff;
}
.demand-quantity-table {
  width: 100%;
  min-width: 820px;
  border-collapse: collapse;
  font-size: 12px;
}
.demand-quantity-table th,
.demand-quantity-table td {
  padding: 11px 12px;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
  text-align: left;
}
.demand-quantity-table th {
  color: #526a79;
  background: #f4f7f8;
  font-size: 11px;
}
.demand-quantity-table th:nth-child(1) { width: 29%; }
.demand-quantity-table th:nth-child(2) { width: 14%; }
.demand-quantity-table th:nth-child(3) { width: 13%; }
.demand-quantity-table th:nth-child(4) { width: 44%; }
.demand-quantity-table tbody tr:last-child td { border-bottom: 0; }
.demand-quantity-table td span { color: var(--muted); }
.demand-quantity-value {
  margin-top: 4px;
  color: #213a49;
}
.demand-quantity-table td p {
  margin: 5px 0 0;
  color: var(--muted);
}
.demand-quantity-other-table { min-width: 820px; }
.state-badge {
  flex: 0 0 auto;
  padding: 2px 7px;
  border: 1px solid currentColor;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 720;
}
.state-confirmed,
.state-strengthening { color: var(--green); background: #edf6f2; }
.state-weakening,
.state-refuted { color: #9a5547; background: #faeeeb; }
.state-weak,
.state-unresolved { color: #7b6b54; background: #f5f1ea; }
.logic-question {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: 13px;
}
.logic-conclusion {
  margin: 8px 0 0;
  color: #354856;
  font-size: 14px;
}
.logic-node-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 14px;
  margin-top: 12px;
  color: #607483;
  font-size: 11px;
}
.entity-list {
  margin-top: 18px;
  border-top: 1px solid var(--line-strong);
}
.entity-module {
  border-bottom: 1px solid var(--line);
}
.entity-module:last-child { border-bottom: 0; }
.entity-heading {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto 16px;
  align-items: center;
  gap: 14px;
  min-height: 64px;
  padding: 12px 2px;
  cursor: pointer;
  list-style: none;
}
.entity-heading::-webkit-details-marker { display: none; }
.entity-heading > div { min-width: 0; }
.entity-heading strong {
  display: block;
  color: #25485f;
  font-size: 15px;
  font-weight: 760;
}
.entity-heading > div > span {
  display: block;
  margin-top: 2px;
  color: var(--muted);
  font-size: 11px;
}
.entity-effect {
  padding: 2px 7px;
  border: 1px solid currentColor;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 730;
}
.effect-positive { color: var(--green); background: #edf6f2; }
.effect-negative { color: #995344; background: #faeeeb; }
.effect-mixed { color: #7b654c; background: #f7f1e8; }
.effect-unclear { color: #607483; background: #eef3f6; }
.entity-chevron {
  width: 8px;
  height: 8px;
  border-right: 2px solid var(--blue);
  border-bottom: 2px solid var(--blue);
  transform: rotate(45deg);
  transition: transform 180ms ease;
}
.entity-module[open] .entity-chevron { transform: rotate(225deg); }
.entity-body {
  padding: 0 2px 22px;
  animation: reveal 180ms ease both;
}
.entity-evaluation {
  padding: 16px 18px;
  border-left: 3px solid var(--blue);
  background: #f4f7f9;
}
.entity-evaluation h5 {
  margin: 0;
  color: #315a75;
  font-size: 12px;
}
.entity-evaluation > p {
  margin: 6px 0 0;
  color: #344957;
  font-size: 14px;
}
.entity-change {
  display: grid;
  grid-template-columns: 112px minmax(0, 1fr);
  gap: 12px;
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid var(--line);
}
.entity-change strong {
  color: var(--muted);
  font-size: 12px;
}
.entity-change p {
  margin: 0;
  color: #455565;
  font-size: 13px;
}
.entity-next {
  margin: 10px 0 0;
}
.entity-next > div {
  display: grid;
  grid-template-columns: 112px minmax(0, 1fr);
  gap: 12px;
  padding-top: 5px;
}
.entity-next dt {
  color: var(--muted);
  font-size: 12px;
}
.entity-next dd {
  margin: 0;
  color: #455565;
  font-size: 13px;
}
.empty-entity {
  margin: 16px 0 0;
  color: var(--muted);
  font-size: 13px;
}
.logic-node-detail {
  margin-top: 13px;
  padding-top: 10px;
  border-top: 1px solid var(--line);
}
.logic-node-detail summary {
  cursor: pointer;
  color: var(--blue);
  font-size: 12px;
  font-weight: 680;
}
.logic-node-detail dl { margin: 12px 0 0; }
.logic-node-detail dl > div {
  display: grid;
  grid-template-columns: 88px minmax(0, 1fr);
  gap: 10px;
  padding: 5px 0;
}
.logic-node-detail dt {
  color: var(--muted);
  font-size: 12px;
}
.logic-node-detail dd {
  margin: 0;
  color: #455565;
  font-size: 13px;
}
.logic-node-detail ul { margin: 0; padding-left: 17px; }

.section-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.section-heading > div {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.section-heading span {
  color: var(--rust);
  font-size: 11px;
  font-weight: 750;
}

.section-heading h3 {
  margin: 0;
  color: #264a64;
  font-size: 19px;
  letter-spacing: 0;
}

.section-heading > p {
  margin: 0;
  color: var(--muted);
  font-size: 12px;
}

.timeline-table-wrap,
.company-table-wrap,
.entity-table-wrap {
  width: 100%;
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--surface);
  box-shadow: 0 4px 18px rgba(36, 55, 72, 0.045);
  scrollbar-color: #aebdc8 transparent;
  scrollbar-width: thin;
}

.timeline-table-wrap:focus-visible,
.company-table-wrap:focus-visible,
.entity-table-wrap:focus-visible {
  outline: 2px solid var(--blue);
  outline-offset: 3px;
}

.timeline-table {
  width: 100%;
  min-width: 980px;
  border-collapse: collapse;
  table-layout: fixed;
}

.entity-table-wrap { margin-top: 12px; }
.entity-table {
  width: 100%;
  min-width: 860px;
  border-collapse: collapse;
  table-layout: fixed;
}
.entity-table .col-material { width: 300px; }
.entity-table .col-type { width: 112px; }
.entity-table .col-claims { width: auto; }
.entity-table th {
  padding: 11px 14px;
  border-bottom: 1px solid var(--line-strong);
  background: #edf2f5;
  color: #526575;
  font-size: 11px;
  font-weight: 760;
  text-align: left;
  vertical-align: bottom;
}
.entity-table td {
  padding: 16px 14px;
  border-bottom: 1px solid var(--line);
  color: #3c4b5a;
  font-size: 14px;
  text-align: left;
  vertical-align: top;
}
.entity-table tbody tr:last-child td { border-bottom: 0; }
.entity-table tbody tr:hover { background: #f9fbfc; }
.entity-table .source-report time {
  display: block;
  margin-bottom: 5px;
  color: var(--muted);
  font-size: 11px;
  font-weight: 650;
}

.timeline-table .col-date { width: 118px; }
.timeline-table .col-type { width: 112px; }
.timeline-table .col-report { width: 260px; }
.timeline-table .col-claims { width: auto; }

.timeline-table th {
  padding: 12px 16px;
  border-bottom: 1px solid var(--line-strong);
  background: #edf2f5;
  color: #526575;
  font-size: 11px;
  font-weight: 760;
  text-align: left;
  vertical-align: bottom;
}

.timeline-table td {
  padding: 18px 16px;
  border-bottom: 1px solid var(--line);
  color: #3c4b5a;
  font-size: 14px;
  text-align: left;
  vertical-align: top;
}

.timeline-table tbody tr:last-child td { border-bottom: 0; }

.timeline-table tbody tr:hover { background: #f9fbfc; }

.source-date time {
  color: #315a75;
  font-size: 13px;
  font-weight: 720;
}

.source-report {
  font-weight: 680;
  line-height: 1.55;
  overflow-wrap: anywhere;
}

.material-tag {
  display: inline-block;
  padding: 1px 7px;
  border: 1px solid #c9d8e2;
  border-radius: 4px;
  background: var(--blue-soft);
  color: var(--blue);
  font-size: 11px;
  font-weight: 700;
}

.source-report a {
  text-decoration: none;
}

.source-report a:hover { text-decoration: underline; }
.source-report a span {
  margin-left: 6px;
  color: var(--rust);
  font-size: 10px;
  font-weight: 760;
}

.claim-list {
  margin: 0;
  padding-left: 18px;
  list-style: disc;
}

.claim-list li {
  padding: 0 0 14px 3px;
}

.claim-list li:last-child { padding-bottom: 0; }

.claim-list li::marker { color: var(--rust); }

.claim-heading {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 10px;
  align-items: baseline;
  margin-bottom: 4px;
}

.claim-index {
  color: var(--rust);
  font-size: 12px;
  font-weight: 760;
}

.claim-location {
  color: var(--green);
  font-size: 12px;
  font-weight: 680;
}

.claim-list p {
  margin: 0;
  color: #3c4b5a;
  font-size: 14px;
}

.mapping-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin: 3px 0 6px;
}
.mapping-tag {
  display: inline-block;
  padding: 1px 6px;
  border-radius: 3px;
  background: #eef2f4;
  color: #5d6b77;
  font-size: 10px;
  font-weight: 680;
}
.mapping-support { background: #eaf3ef; color: var(--green); }
.mapping-refute { background: #f8eae7; color: #9a5547; }

.conclusion-panel {
  padding: 26px 28px;
  border-top: 3px solid var(--blue);
  background: var(--blue-soft);
}

.conclusion-panel .section-heading { margin-bottom: 12px; }

.conclusion-text {
  margin: 0;
  color: #28475e;
  font-size: 16px;
  font-weight: 520;
}

.trend-line {
  display: grid;
  grid-template-columns: 90px minmax(0, 1fr);
  gap: 16px;
  margin-top: 18px;
  padding-top: 16px;
  border-top: 1px solid #c6d8e3;
}

.trend-line strong {
  color: var(--rust);
  font-size: 12px;
}

.trend-line p {
  margin: 0;
  color: #526777;
  font-size: 14px;
}

.empty-state {
  padding: 24px;
  color: var(--muted);
  text-align: center;
}

.report-footer {
  padding: 26px 0 40px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 12px;
}

.report-footer p { margin: 0; }

@media (max-width: 760px) {
  .report-header-inner,
  .top-nav-inner,
  .report-main,
  .report-footer {
    width: min(100% - 28px, 1180px);
  }

  .report-header-inner { padding: 38px 0 28px; }
  h1 { font-size: 38px; }
  .report-deck { font-size: 16px; }
  .report-meta { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .decision-heading { flex-direction: column; gap: 12px; }
  .decision-update { grid-template-columns: 1fr; gap: 4px; }
  .delta-list,
  .decision-audit { grid-template-columns: 1fr; }
  .delta-list article,
  .delta-list article + article {
    padding: 15px 0;
    border-right: 0;
    border-bottom: 1px solid var(--line);
  }
  .delta-list article:last-child { border-bottom: 0; }

  .lens-heading {
    grid-template-columns: 42px minmax(0, 1fr) 16px;
    gap: 12px;
    padding: 26px 0;
  }

  .lens-count {
    grid-column: 2;
    grid-row: 2;
  }

  .lens-chevron {
    grid-column: 3;
    grid-row: 1 / span 2;
  }

  .lens-body { padding: 0 0 42px; }
  .logic-node-summary {
    grid-template-columns: 42px minmax(0, 1fr) 16px;
    gap: 10px;
    padding: 16px 14px;
  }
  .logic-step { width: 38px; height: 38px; }
  .logic-node-summary .state-badge {
    grid-column: 2;
    justify-self: start;
  }
  .logic-node-chevron {
    grid-column: 3;
    grid-row: 1 / span 2;
  }
  .logic-node-body { padding: 0 14px 20px; }
  .node-thesis,
  .node-follow-up > div { grid-template-columns: 1fr; gap: 3px; }
  .event-history-toolbar { align-items: stretch; flex-direction: column; }
  .history-expand { align-self: flex-start; }
  .state-history-item { width: 168px; }
  .claim-month-group > summary { grid-template-columns: 1fr; gap: 2px; }
  .claim-source-group > summary {
    grid-template-columns: 78px minmax(0, 1fr);
  }
  .source-group-count { grid-column: 2; }
  .timeline-table { min-width: 880px; }
  .section-heading { align-items: flex-start; flex-direction: column; }
  .trend-line { grid-template-columns: 1fr; gap: 4px; }
  .logic-node-detail dl > div { grid-template-columns: 1fr; gap: 2px; }
  .demand-party-grid { grid-template-columns: 1fr; }
  .demand-quantity-table { min-width: 840px; }
  .entity-change,
  .entity-next > div { grid-template-columns: 1fr; gap: 2px; }
  .entity-table { min-width: 760px; }
}

@media print {
  .top-nav { display: none; }
  .report-main { padding-top: 0; }
  .lens-section { break-inside: avoid; }
  .timeline-table-wrap { overflow: visible; box-shadow: none; }
  .company-table-wrap { overflow: visible; box-shadow: none; }
  .entity-table-wrap { overflow: visible; box-shadow: none; }
  .timeline-table { min-width: 0; }
  .entity-table { min-width: 0; }
}
"""


def _report_script() -> str:
    return """
const navLinks = Array.from(document.querySelectorAll('.top-nav a'));
const sections = Array.from(document.querySelectorAll('.lens-section'));
const linkById = new Map(navLinks.map((link) => [link.hash.slice(1), link]));
const observer = new IntersectionObserver((entries) => {
  const visible = entries
    .filter((entry) => entry.isIntersecting)
    .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
  if (!visible) return;
  navLinks.forEach((link) => link.classList.remove('is-active'));
  linkById.get(visible.target.id)?.classList.add('is-active');
}, { rootMargin: '-18% 0px -72% 0px', threshold: [0.05, 0.2, 0.5] });
sections.forEach((section) => observer.observe(section));

document.querySelectorAll('.causal-node').forEach((node) => {
  let activeFilter = 'all';
  let cutoff = '';
  const events = Array.from(node.querySelectorAll('.claim-event'));
  const sources = Array.from(node.querySelectorAll('.claim-source-group'));
  const months = Array.from(node.querySelectorAll('.claim-month-group'));
  const filterButtons = Array.from(node.querySelectorAll('[data-history-filter]'));
  const statePoints = Array.from(node.querySelectorAll('[data-history-cutoff]'));
  const selectionTitle = node.querySelector('[data-history-selection-title]');
  const selectionConclusion = node.querySelector('[data-history-selection-conclusion]');
  const currentPoint = statePoints[statePoints.length - 1];

  const applyHistoryView = () => {
    events.forEach((event) => {
      const matchesFilter = activeFilter === 'all'
        || event.dataset.effectGroup === activeFilter;
      const eventDate = event.dataset.publishedAt || '';
      const matchesCutoff = !cutoff || (!!eventDate && eventDate <= cutoff);
      event.hidden = !(matchesFilter && matchesCutoff);
    });
    sources.forEach((source) => {
      source.hidden = !Array.from(source.querySelectorAll('.claim-event'))
        .some((event) => !event.hidden);
      if (!source.hidden && (activeFilter !== 'all' || cutoff)) source.open = true;
    });
    months.forEach((month) => {
      month.hidden = !Array.from(month.querySelectorAll('.claim-source-group'))
        .some((source) => !source.hidden);
      if (!month.hidden && (activeFilter !== 'all' || cutoff)) month.open = true;
    });
    filterButtons.forEach((button) => {
      const active = button.dataset.historyFilter === activeFilter;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    statePoints.forEach((point) => {
      point.setAttribute(
        'aria-pressed',
        String(!!cutoff && point.dataset.historyCutoff === cutoff),
      );
    });
    const selectedPoint = cutoff
      ? statePoints.find((point) => point.dataset.historyCutoff === cutoff)
      : currentPoint;
    if (selectionTitle && selectedPoint) {
      selectionTitle.textContent = cutoff
        ? `回看截面 · ${cutoff} · ${selectedPoint.dataset.historyStateLabel || ''}`
        : `当前截面 · ${selectedPoint.dataset.historyCutoff || ''} · ${selectedPoint.dataset.historyStateLabel || ''}`;
    }
    if (selectionConclusion && selectedPoint) {
      selectionConclusion.textContent = selectedPoint.dataset.historyConclusion || '';
    }
  };

  filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
      activeFilter = button.dataset.historyFilter || 'all';
      applyHistoryView();
    });
  });
  statePoints.forEach((point) => {
    point.addEventListener('click', () => {
      cutoff = point.dataset.historyCutoff || '';
      applyHistoryView();
    });
  });
  node.querySelector('[data-history-reset]')?.addEventListener('click', () => {
    cutoff = '';
    applyHistoryView();
  });
  node.querySelector('[data-history-expand]')?.addEventListener('click', (event) => {
    const button = event.currentTarget;
    const expanded = button.getAttribute('aria-pressed') === 'true';
    months.forEach((month) => { if (!month.hidden) month.open = !expanded; });
    sources.forEach((source) => { if (!source.hidden) source.open = !expanded; });
    button.setAttribute('aria-pressed', String(!expanded));
    button.textContent = expanded ? '展开全部历史' : '收起历史材料';
  });
});
"""
