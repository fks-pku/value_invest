from __future__ import annotations

from typing import Any

from value_invest_research.adapters.outbound.report_sections.base import ReportRenderContext
from value_invest_research.adapters.outbound.report_sections.shared import _e


class TargetRecommendationsSection:
    section_id = "targets"

    def render(self, context: ReportRenderContext) -> str:
        return _render_targets(context.data["targets"], context.data["project"])


def _render_targets(targets: list[dict[str, Any]], project: dict[str, Any] | None = None) -> str:
    project = project or {}
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
    <h2>标的推荐</h2>
  </div>
  <div class="artifact-card"><p class="section-note">该表是研究观察清单，不是买卖指令；排序同时考虑瓶颈强度、未来空间、估值赔率和反证可控性。</p></div>
  {_render_target_profit_bridge(project.get("target_profit_bridge") or targets)}
  {_render_target_valuation_table(targets)}
  {_render_target_odds_model(targets)}
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


def _render_target_profit_bridge(rows_source: list[Any]) -> str:
    rows = "\n".join(_target_profit_bridge_row(row) for row in rows_source)
    if not rows:
        rows = '<tr><td colspan="7">暂无可展示财务桥。</td></tr>'
    return f"""
  <div class="target-profit-bridge">
    <p class="artifact-title">标的财务桥</p>
    <p>把主题受益落到账面科目；只有能进入收入、利润、现金流且可验证的节点，才支持更高观察强度。</p>
    <table>
      <thead><tr><th>标的</th><th>核心节点</th><th>需求传导</th><th>财务桥</th><th>必须验证</th><th>降级触发</th><th>状态</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
""".strip()


def _target_profit_bridge_row(target: Any) -> str:
    if not isinstance(target, dict):
        cells = list(target) if isinstance(target, (list, tuple)) else [target]
        cells = (cells + [""] * 7)[:7]
        return f"""
<tr>
  <td>{_e(str(cells[0]))}</td>
  <td>{_e(str(cells[1]))}</td>
  <td>{_e(str(cells[2]))}</td>
  <td>{_e(str(cells[3]))}</td>
  <td>{_e(str(cells[4]))}</td>
  <td>{_e(str(cells[5]))}</td>
  <td>{_e(str(cells[6]))}</td>
</tr>
""".strip()
    target_label = f"{target.get('ticker', '')} {target.get('name', '')}".strip()
    node = target.get("thesis_node") or target.get("chokepoint") or target.get("bottleneck_node") or ""
    demand = target.get("demand_bridge") or target.get("rationale") or ""
    financial = target.get("financial_bridge") or target.get("future_space") or target.get("odds") or ""
    verify = target.get("next_verification_data") or target.get("required_evidence") or ""
    downgrade = target.get("downgrade_risk") or target.get("risks") or ""
    state = target.get("action_state") or target.get("strength") or ""
    return f"""
<tr>
  <td>{_e(target_label)}</td>
  <td>{_e(str(node))}</td>
  <td>{_e(str(demand))}</td>
  <td>{_e(str(financial))}</td>
  <td>{_e(str(verify))}</td>
  <td>{_e(str(downgrade))}</td>
  <td>{_e(str(state))}</td>
</tr>
""".strip()


def _render_target_valuation_table(targets: list[dict[str, Any]]) -> str:
    rows = "\n".join(_target_valuation_row(target) for target in targets)
    if not rows:
        rows = '<tr><td colspan="9">暂无可展示估值赔率表。</td></tr>'
    return f"""
  <div class="target-valuation-table">
    <p class="artifact-title">估值与赔率表</p>
    <p>胜率之外必须看是否仍有错配。估值缺失或已充分反映时，行动状态应保守。</p>
    <table>
      <thead><tr><th>标的</th><th>总分</th><th>稀缺/垄断</th><th>未充分定价</th><th>业绩弹性</th><th>风险控制</th><th>估值读数</th><th>隐含预期</th><th>下一步验证</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
""".strip()


def _target_valuation_row(target: dict[str, Any]) -> str:
    target_label = f"{target.get('ticker', '')} {target.get('name', '')}".strip()
    score = target.get("score") if isinstance(target.get("score"), dict) else {}
    dimensions = score.get("score_dimensions") if isinstance(score.get("score_dimensions"), dict) else {}
    total = score.get("total_score") or target.get("strength_score") or target.get("score") or ""
    scarcity = dimensions.get("scarcity_or_monopoly", "")
    mispricing = dimensions.get("mispricing", "")
    elasticity = dimensions.get("earnings_elasticity", "")
    risk = dimensions.get("risk_control", "")
    valuation_read = target.get("valuation_read") or target.get("valuation_odds") or target.get("odds") or "待验证"
    odds = target.get("odds_model") if isinstance(target.get("odds_model"), dict) else {}
    implied = odds.get("implied_expectation") or target.get("implied_expectation") or ""
    verify = target.get("next_verification_data") or target.get("required_evidence") or ""
    return f"""
<tr>
  <td>{_e(target_label)}</td>
  <td>{_e(str(total))}</td>
  <td>{_e(str(scarcity))}</td>
  <td>{_e(str(mispricing))}</td>
  <td>{_e(str(elasticity))}</td>
  <td>{_e(str(risk))}</td>
  <td>{_e(str(valuation_read))}</td>
  <td>{_e(str(implied))}</td>
  <td>{_e(str(verify))}</td>
</tr>
""".strip()


def _render_target_odds_model(targets: list[dict[str, Any]]) -> str:
    rows = "\n".join(_target_odds_row(target) for target in targets)
    if not rows:
        rows = '<tr><td colspan="8">暂无可展示赔率模型。</td></tr>'
    return f"""
  <div class="target-odds-model">
    <h3>简化赔率模型</h3>
    <p>该表只展示研究截面下的隐含预期、情景路径和升级/降级数据，不使用后续价格标签。</p>
    <table class="target-odds-table">
      <thead><tr><th>标的</th><th>隐含预期</th><th>Base 路径</th><th>Bull 路径</th><th>Bear 路径</th><th>升级数据</th><th>降级数据</th><th>赔率判断</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
""".strip()


def _target_odds_row(target: dict[str, Any]) -> str:
    odds = target.get("odds_model") if isinstance(target.get("odds_model"), dict) else {}
    target_label = f"{target.get('ticker', '')} {target.get('name', '')}".strip()
    implied = odds.get("implied_expectation") or target.get("implied_expectation") or "待补充当前市场隐含预期。"
    base = odds.get("base_path") or target.get("next_verification_data") or target.get("required_evidence") or "待补充 base 验证路径。"
    bull = odds.get("bull_path") or "待补充 bull 情景验证路径。"
    bear = odds.get("bear_path") or target.get("downgrade_risk") or target.get("risks") or "待补充 bear 情景和降级条件。"
    upgrade = odds.get("upgrade_data") or base
    downgrade = odds.get("downgrade_data") or bear
    judgment = odds.get("odds_judgment") or target.get("odds") or target.get("future_space") or "赔率未验证。"
    return f"""
<tr>
  <td>{_e(target_label)}</td>
  <td>{_e(str(implied))}</td>
  <td>{_e(str(base))}</td>
  <td>{_e(str(bull))}</td>
  <td>{_e(str(bear))}</td>
  <td>{_e(str(upgrade))}</td>
  <td>{_e(str(downgrade))}</td>
  <td>{_e(str(judgment))}</td>
</tr>
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
