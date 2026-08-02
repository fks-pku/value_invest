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
    "neutral": "线索",
}

ENTITY_EFFECT_LABELS = {
    "positive": "正向",
    "negative": "负向",
    "mixed": "多空并存",
    "unclear": "待判断",
}


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
                    f"{engine_attribute}>"
                ),
                '<header class="report-header">',
                '  <div class="report-header-inner">',
                '    <div class="report-label">VALUE INVEST · BOM RESEARCH</div>',
                f"    <h1>{escape(title)}</h1>",
                (
                    '    <p class="report-deck">以材料发布时间组织证据，'
                    "把需求、供给、技术、估值与治理放在同一研究截面内。</p>"
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
      <p>{escape(str(decision.get("summary") or ""))}</p>
    </div>
    <span class="action-badge action-{escape(action_state)}">{escape(action_label)}</span>
  </div>
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
        logic_node_rows = "\n".join(
            self._render_logic_node(node) for node in logic_nodes
        )
        logic_state_section = ""
        if logic_nodes:
            logic_state_section = f"""
    <section class="logic-state-section" aria-labelledby="logic-state-{lens_id}">
      <div class="section-heading">
        <div>
          <span>01</span>
          <h3 id="logic-state-{lens_id}">逻辑节点状态</h3>
        </div>
        <p>材料先改变节点，再改变投资判断</p>
      </div>
      <div class="logic-node-list">{logic_node_rows}</div>
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
        conclusion_number = "02"
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
      <h3 id="logic-{lens_id}">简单逻辑链</h3>
      <p>{logic}</p>
    </section>

{logic_state_section}
{timeline_section}

    <section class="conclusion-panel" aria-labelledby="conclusion-{lens_id}">
      <div class="section-heading">
        <div>
          <span>{conclusion_number}</span>
          <h3 id="conclusion-{lens_id}">最新结论与趋势</h3>
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

    def _render_logic_node(self, node: dict[str, Any]) -> str:
        if str(node.get("render_mode") or "") == "demand_party_list":
            return self._render_demand_party_list(node)
        if str(node.get("render_mode") or "") == "demand_quantity_matrix":
            return self._render_demand_quantity_matrix(node)
        state = str(node.get("state") or "unresolved")
        entities = list(node.get("entities") or [])
        entity_modules = "\n".join(
            self._render_entity_module(entity) for entity in entities
        )
        if not entity_modules:
            entity_modules = (
                '<p class="empty-entity">当前没有映射到具体公司或实体的材料。</p>'
            )
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
<article class="logic-node" data-logic-node-id="{escape(str(node.get("logic_node_id") or ""))}">
  <div class="logic-node-heading">
    <div>
      <span>{escape(str(node.get("logic_node_id") or ""))}</span>
      <h4>{escape(str(node.get("title") or ""))}</h4>
    </div>
    <span class="state-badge state-{escape(state)}">{escape(STATE_LABELS.get(state, state))}</span>
  </div>
  <p class="logic-question">{escape(str(node.get("question") or ""))}</p>
  <p class="logic-conclusion">{escape(str(node.get("conclusion") or ""))}</p>
  <div class="logic-node-meta">
    <span>{int(node.get("support_count") or 0)} 支持</span>
    <span>{int(node.get("refute_count") or 0)} 反证</span>
    <span>{int(node.get("mapped_claim_count") or 0)} 条映射观点</span>
    <span>{len(entities)} 个公司 / 实体</span>
  </div>
  <div class="entity-list" aria-label="公司与实体信息">
    {entity_modules}
  </div>
  <details class="logic-node-detail">
    <summary>查看变化、缺口与下一验证</summary>
    <dl>
      <div><dt>本期变化</dt><dd>{escape(str(node.get("change_summary") or ""))}</dd></div>
      <div><dt>证据缺口</dt><dd><ul>{gaps}</ul></dd></div>
      <div><dt>下一验证</dt><dd>{next_validation}</dd></div>
    </dl>
  </details>
</article>
"""

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
        classified_rows = [
            row for row in rows if row.get("forecast_group") == "classified"
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
        classified_html = "".join(
            f"""
        <tr>
          <td><strong>{escape(str(row.get("demand_party") or ""))}</strong></td>
          <td>{escape(str(row.get("quantity") or ""))}</td>
          <td>{escape(str(row.get("metric") or ""))}<br><span>{escape(str(row.get("target_period") or ""))}</span></td>
          <td>{escape(quality_labels.get(str(row.get("mapping_quality") or ""), str(row.get("mapping_quality") or "")))}</td>
          <td>{self._render_demand_quantity_sources(row)}<p>{escape(str(row.get("caveat") or ""))}</p></td>
        </tr>"""
            for row in classified_rows
        )
        other_html = "".join(
            f"""
        <tr>
          <td><strong>{escape(str(row.get("metric") or ""))}</strong></td>
          <td>{escape(str(row.get("quantity") or ""))}</td>
          <td>{escape(str(row.get("target_period") or ""))}</td>
          <td>{self._render_demand_quantity_sources(row)}<p>{escape(str(row.get("caveat") or ""))}</p></td>
        </tr>"""
            for row in other_rows
        )
        return f"""
<article class="logic-node demand-quantity-node" data-logic-node-id="{escape(str(node.get("logic_node_id") or ""))}" data-render-mode="demand-quantity-matrix">
  <div class="logic-node-heading">
    <div>
      <span>{escape(str(node.get("logic_node_id") or ""))}</span>
      <h4>{escape(str(node.get("title") or ""))}</h4>
    </div>
  </div>
  <section class="demand-quantity-group" data-demand-forecast-group="classified">
    <h5>分类映射预测</h5>
    <div class="demand-quantity-table-wrap" role="region" aria-label="分类映射预测" tabindex="0">
      <table class="demand-quantity-table">
        <thead><tr><th>Q1 需求方</th><th>当前数量 / 预测</th><th>口径与期间</th><th>映射质量</th><th>来源与局限</th></tr></thead>
        <tbody>{classified_html}</tbody>
      </table>
    </div>
  </section>
  <section class="demand-quantity-group" data-demand-forecast-group="other">
    <h5>其它预测</h5>
    <div class="demand-quantity-table-wrap" role="region" aria-label="其它预测" tabindex="0">
      <table class="demand-quantity-table demand-quantity-other-table">
        <thead><tr><th>预测对象</th><th>当前数量 / 预测</th><th>期间</th><th>来源与未映射原因</th></tr></thead>
        <tbody>{other_html}</tbody>
      </table>
    </div>
  </section>
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

.logic-node-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.logic-node {
  padding: 20px 22px;
  border: 1px solid var(--line);
  border-left: 3px solid #6f8fa3;
  border-radius: 5px;
  background: var(--surface);
}

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
.demand-quantity-group { margin-top: 18px; }
.demand-quantity-group h5 {
  margin: 0 0 9px;
  color: #244b66;
  font-size: 14px;
}
.demand-quantity-table-wrap {
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: 4px;
}
.demand-quantity-table {
  width: 100%;
  min-width: 920px;
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
.demand-quantity-table tbody tr:last-child td { border-bottom: 0; }
.demand-quantity-table td span { color: var(--muted); }
.demand-quantity-table td p {
  margin: 5px 0 0;
  color: var(--muted);
}
.demand-quantity-other-table { min-width: 760px; }
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
"""
