from __future__ import annotations

from typing import Any

from value_invest_research.adapters.outbound.report_sections.base import ReportRenderContext
from value_invest_research.adapters.outbound.report_sections.shared import (
    _e,
    _render_overview_question_card,
    _render_source_chip,
    _row_cells,
    _slug,
)


class IndustryOverviewSection:
    section_id = "overview"

    def render(self, context: ReportRenderContext) -> str:
        return _render_industry_overview(context.data["supply_chain"], context.source_url_by_id)


def _render_industry_overview(chain: dict[str, Any], source_url_by_id: dict[str, str]) -> str:
    layers = chain.get("layers") or []
    relationships = chain.get("relationships") or []
    stage_groups = chain.get("stage_groups") or chain.get("stageGroups") or []
    research_bridge = _render_chain_research_bridge(
        chain.get("research_bridge") or chain.get("supply_chain_research_bridge") or {},
        chain.get("node_lenses") or chain.get("supply_chain_node_lenses") or [],
    )
    lane_map = _render_chain_lane_map(stage_groups, layers, relationships)
    value_flow = _render_chain_value_flow(chain, relationships)
    industry_space = _render_industry_space(chain, source_url_by_id)
    industry_competition = _render_industry_competition(chain, source_url_by_id)
    industry_chokepoints = _render_industry_chokepoints(chain, source_url_by_id)
    industry_key_variables = _render_industry_key_variables(
        chain,
        _render_chain_data_gaps(chain.get("data_gaps") or chain.get("supply_chain_data_gaps") or []),
    )
    component_value_chain = chain.get("component_value_chain") or chain.get("componentValueChain") or []
    bom_taxonomy = _render_bom_taxonomy(
        chain.get("bom_taxonomy") or chain.get("bomTaxonomy") or chain.get("canonical_bom_nodes") or chain.get("canonicalBomNodes") or [],
        component_value_chain,
    )
    return f"""
<section id="overview" class="section industry-overview-section">
  <div class="section-heading">
    <span class="section-kicker">02</span>
    <h2>行业概况</h2>
  </div>
  <details class="industry-module supply-chain-section">
    <summary class="module-head"><span class="module-index">01</span><div><h3>产业链与生态位</h3><p>先看清楚谁提供什么、谁依赖谁、订单和利润沿什么路径流动。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
    <div class="chain-explain">
      {research_bridge}
      <p class="chain-plain-summary">{_e(str(chain.get("plain_summary", "")))}</p>
      {_render_chain_detail_panel("泳道图", "按上游 / 中游 / 下游看生态位、公司关系和依赖方向。", lane_map, "chain-lane-panel")}
      {_render_chain_detail_panel("价值流", "用白话步骤解释需求如何变成订单、系统交付、收入和利润验证。", value_flow, "chain-value-panel")}
      {_render_chain_detail_panel("BOM / 组件级链条", "把系统拆成子系统、组件、关键公司、输入输出和财务验证指标。", _render_component_value_chain(component_value_chain), "chain-component-panel")}
      {_render_chain_detail_panel("统一 BOM 口径", "后续行业空间、竞争格局、瓶颈点和标的映射均使用同一套节点定义。", bom_taxonomy, "bom-taxonomy-panel")}
    </div>
    </div>
  </details>
  {industry_space}
  {industry_competition}
  {industry_chokepoints}
  {industry_key_variables}
</section>
""".strip()


def _render_chain_detail_panel(title: str, description: str, body: str, class_name: str) -> str:
    return f"""
      <details class="chain-detail-panel {class_name}">
        <summary><span>{_e(title)}</span><small>{_e(description)}</small><span class="chevron">›</span></summary>
        <div class="chain-detail-body">{body}</div>
      </details>
""".strip()


def _render_bom_taxonomy(nodes: list[Any], component_value_chain: list[Any]) -> str:
    normalized: list[dict[str, str]] = []
    if isinstance(nodes, list):
        for node in nodes:
            if isinstance(node, dict):
                label = str(node.get("label") or node.get("node") or node.get("name") or "")
                if not label:
                    continue
                normalized.append(
                    {
                        "label": label,
                        "layer": str(node.get("layer") or node.get("stage") or "BOM 节点"),
                        "role": str(node.get("role") or node.get("description") or node.get("definition") or "用于统一行业空间、竞争格局、瓶颈点和标的映射。"),
                    }
                )
            elif str(node).strip():
                normalized.append({"label": str(node), "layer": "BOM 节点", "role": "用于统一行业空间、竞争格局、瓶颈点和标的映射。"})
    if not normalized and isinstance(component_value_chain, list):
        seen: set[str] = set()
        for item in component_value_chain:
            cells = _row_cells(item, 6)
            label = str(cells[0]).strip() if cells else ""
            if label and label not in seen:
                seen.add(label)
                normalized.append({"label": label, "layer": "BOM 节点", "role": "从组件级链条提取的公共节点口径。"})
            if len(normalized) >= 8:
                break
    if len(normalized) < 2:
        normalized = [
            {"label": "核心 BOM 节点", "layer": "待补", "role": "需要在产业链与生态位中补充统一节点定义。"},
            {"label": "需求验证层", "layer": "非 BOM", "role": "客户预算、capex、订单或 ROI 信号，用于验证需求，不作为 BOM 节点。"},
        ]
    cards = "".join(
        f'<article class="bom-taxonomy-card"><span>{_e(node["layer"])}</span><strong>{_e(node["label"])}</strong><p>{_e(node["role"])}</p></article>'
        for node in normalized
    )
    return f"""
      <div class="bom-taxonomy">
        <p>本报告后续所有公共模块必须复用以下节点名；来源材料里的更细口径只作为证据字段，不改变公共 BOM 命名。</p>
        <div class="bom-taxonomy-grid">{cards}</div>
      </div>
""".strip()


def _extract_bom_taxonomy_nodes(chain: dict[str, Any]) -> list[dict[str, str]]:
    nodes = chain.get("bom_taxonomy") or chain.get("canonical_bom_nodes") or chain.get("bom_nodes") or []
    component_value_chain = chain.get("component_value_chain") or []
    normalized: list[dict[str, str]] = []
    if isinstance(nodes, list):
        for node in nodes:
            if isinstance(node, dict):
                label = str(node.get("label") or node.get("node") or node.get("name") or "").strip()
                layer = str(node.get("layer") or node.get("stage") or "BOM 节点").strip()
                role = str(node.get("role") or node.get("description") or node.get("definition") or "统一公共 BOM 节点。").strip()
            else:
                label = str(node).strip()
                layer = "BOM 节点"
                role = "统一公共 BOM 节点。"
            if label and "需求验证" not in label and "客户需求" not in label:
                normalized.append({"label": label, "layer": layer, "role": role})
    if not normalized and isinstance(component_value_chain, list):
        seen: set[str] = set()
        for item in component_value_chain:
            cells = _row_cells(item, 7)
            label = str(cells[0]).strip() if cells else ""
            if label and "需求" not in label and label not in seen:
                seen.add(label)
                normalized.append({"label": label, "layer": "BOM 节点", "role": "从组件级价值链提取。"})
            if len(normalized) >= 8:
                break
    if not normalized:
        normalized = [{"label": "核心 BOM 节点", "layer": "待补", "role": "需要在产业链与生态位中补充统一节点定义。"}]
    return normalized


def _render_chain_research_bridge(bridge: dict[str, Any], node_lenses: list[Any]) -> str:
    if not isinstance(bridge, dict):
        bridge = {}
    return f"""
    <div class="chain-research-bridge">
      <div class="chain-bridge-grid">
        <div class="chain-bridge-card"><span>研究目标如何转成产业链问题</span><strong>{_e(str(bridge.get("objective") or "先用产业链理清需求、供给、价值捕获和反证，再生成 QA。"))}</strong></div>
        <div class="chain-bridge-card"><span>核心投资问题</span><strong>{_e(str(bridge.get("core_question") or bridge.get("coreQuestion") or "哪些节点能把主题需求转成可持续收入、利润、现金流和赔率？"))}</strong></div>
      </div>
      <p>{_e(str(bridge.get("current_conclusion") or bridge.get("currentConclusion") or "行业概况需要先回答谁提供什么、谁依赖谁、钱流向哪里、瓶颈在哪里，以及这些结论如何生成下钻 QA。"))}</p>
      {_render_chain_node_lens(node_lenses)}
    </div>
""".strip()


def _chain_research_bridge_qa_row(row: list[Any] | dict[str, Any]) -> str:
    if isinstance(row, dict):
        cells = [
            row.get("q", ""),
            row.get("direction", "") or row.get("question", ""),
            row.get("input", "") or row.get("signal", ""),
        ]
    else:
        cells = row
    return "<tr>" + "".join(f"<td>{_e(str(cell))}</td>" for cell in cells[:3]) + "</tr>"


def _render_chain_node_lens(node_lenses: list[Any]) -> str:
    if not isinstance(node_lenses, list) or not node_lenses:
        node_lenses = [
            ["需求流入", "是否有明确客户预算、订单、收入或 backlog 流入该节点。"],
            ["稀缺供给", "是否控制短期难扩张的产能、资格、生态或工程交付能力。"],
            ["替代难度", "客户能否绕开、双供、内化，或被平台路线替代。"],
            ["货币化能力", "稀缺是否能体现为价格、毛利、收入增长、现金流或更高 backlog 质量。"],
            ["市场定价", "当前估值是否已经充分反映增长和利润率上修。"],
            ["反证触发", "哪些数据会证明瓶颈只是暂时的、低利润的，或已被供给扩张消化。"],
        ]
    items = "\n".join(_chain_node_lens_item(row) for row in node_lenses[:4])
    return f'<div class="chain-node-lens"><b>节点筛选口径</b><ul>{items}</ul></div>'


def _render_chain_lane_map(
    stage_groups: list[dict[str, Any]],
    layers: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
) -> str:
    groups = stage_groups if stage_groups else _fallback_stage_groups(layers, relationships)
    cards = "\n".join(_chain_key_stage_card(group) for group in groups if isinstance(group, dict))
    return f"""
    <div class="chain-relationship-graph chain-lane-map">
      <div class="chain-graph-head">
        <p class="chain-graph-title">按上游 / 中游 / 下游展开公司关系</p>
        <p class="muted">泳道图保留关键生态位，用来生成后续 QA。</p>
      </div>
      <div class="chain-layer-grid">{cards}</div>
    </div>
""".strip()


def _chain_key_stage_card(group: dict[str, Any]) -> str:
    companies = group.get("companies") if isinstance(group.get("companies"), list) else []
    items = "\n".join(_chain_key_company_item(company) for company in companies[:5] if isinstance(company, dict))
    return f"""
    <article class="chain-layer-card chain-stage-panel">
      <div class="chain-stage-head">
        <span class="chain-stage-name">{_e(str(group.get("stage", "")))}</span>
        <strong>{_e(str(group.get("summary", "")))}</strong>
      </div>
      <ul class="chain-company-list">{items}</ul>
    </article>
""".rstrip()


def _chain_key_company_item(company: dict[str, Any]) -> str:
    return f"""
        <li class="chain-company-card">
          <b>{_e(str(company.get("name", "")))}</b>
          <span>{_e(str(company.get("produces", "") or company.get("node_type", "")))}</span>
          <small>{_e(str(company.get("bottleneck_strength") or company.get("bottleneck", "")))} · {_e(str(company.get("qa_link", "")))}</small>
        </li>
""".rstrip()


def _render_chain_value_flow(chain: dict[str, Any], relationships: list[dict[str, Any]]) -> str:
    flows = chain.get("value_flows") or chain.get("valueFlow") or []
    if not isinstance(flows, list) or not flows:
        flows = [
            {
                "step": "01",
                "title": "需求预算进入关键供给",
                "from": "下游客户预算",
                "to": "核心供给节点",
                "what": "订单、规格、产能预约或长期采购需求。",
                "beneficiaries": "能控制稀缺供给或客户入口的公司。",
                "metric": "收入、订单、backlog、毛利率、现金流。",
                "investment_read": "这是行业空间能否进入公司财务的第一段验证。",
                "weight": 3,
            },
            {
                "step": "02",
                "title": "关键供给传导到系统交付",
                "from": "核心供给节点",
                "to": "系统集成 / 渠道 / 应用节点",
                "what": "产品、产能、工程能力或生态标准向下游传导。",
                "beneficiaries": "能把供给约束转成价格、份额或利润率的公司。",
                "metric": "ASP、产品 mix、订单兑现、项目毛利。",
                "investment_read": "价值流要继续通过竞争格局和瓶颈点评估。",
                "weight": 2,
            },
        ]
    simple_flow = _render_chain_simple_flow(chain)
    cards = "\n".join(_render_chain_value_flow_card(flow) for flow in flows if isinstance(flow, dict))
    return f"""
    <div class="chain-map-card chain-value-flow">
      <div class="chain-graph-head"><b>订单和价值如何在链条里流动</b><span>看需求、供给、交付、收入和 ROI 如何依次验证。</span></div>
      {simple_flow}
      <div class="chain-sankey-list">{cards}</div>
    </div>
""".strip()


def _render_chain_simple_flow(chain: dict[str, Any]) -> str:
    raw_steps = chain.get("simple_value_flow") or chain.get("chain_simple_flow") or chain.get("flow_steps") or []
    if not isinstance(raw_steps, list) or not raw_steps:
        raw_steps = [
            "下游需求或预算先变成订单、规格和交付要求。",
            "订单传导到关键供给节点，形成收入、产能和价格验证。",
            "系统交付后，再用客户 ROI、使用率和续费验证持续性。",
        ]
    cards = []
    for index, item in enumerate(raw_steps[:6], start=1):
        if isinstance(item, dict):
            title = str(item.get("title") or f"步骤 {index}")
            plain = str(item.get("plain") or item.get("description") or item.get("step") or "")
            investment = str(item.get("investment") or item.get("investment_read") or "对应到收入、毛利、订单或现金流验证。")
        else:
            title = f"步骤 {index}"
            plain = str(item)
            investment = "对应到收入、毛利、订单或现金流验证。"
        cards.append(
            f"""
        <article class="chain-simple-step">
          <span>{index}</span>
          <div><b>{_e(title)}</b><p>{_e(plain)}</p><small>{_e(investment)}</small></div>
        </article>
""".strip()
        )
    return f"""
      <div class="chain-simple-flow">
        <div class="simple-flow-head"><b>先按这条主线理解</b><span>需求 -> 订单 -> 供给 -> 交付 -> 财务验证</span></div>
        <div class="chain-simple-grid">{"".join(cards)}</div>
      </div>
""".strip()


def _render_chain_value_flow_card(flow: dict[str, Any]) -> str:
    return f"""
      <article class="chain-sankey-flow" style="--flow-weight:{_e(str(flow.get("weight", 2)))}">
        <div class="flow-step"><span>{_e(str(flow.get("step", "")))}</span><b>{_e(str(flow.get("title", "")))}</b></div>
        <div class="flow-route">
          <div class="flow-from"><small>发起方</small>{_e(str(flow.get("from", "")))}</div>
          <div class="flow-band"><span>{_e(str(flow.get("what", "")))}</span></div>
          <div class="flow-to"><small>接收方</small>{_e(str(flow.get("to", "")))}</div>
        </div>
        <div class="flow-fields">
          <div><b>可能受益</b><p>{_e(str(flow.get("beneficiaries", "")))}</p></div>
          <div><b>财务验证</b><p>{_e(str(flow.get("metric", "")))}</p></div>
          <div><b>投资含义</b><p>{_e(str(flow.get("investment_read", "")))}</p></div>
        </div>
      </article>
""".rstrip()


def _render_industry_space(chain: dict[str, Any], source_url_by_id: dict[str, str]) -> str:
    rows = (
        chain.get("industry_space_evidence_pack")
        or chain.get("industry_space_bom_reasoning")
        or chain.get("industry_space_node_elasticity_rows")
        or chain.get("industry_space_sizing_rows")
        or chain.get("industry_space_rows")
        or chain.get("industrySpace")
        or []
    )
    if not isinstance(rows, list) or not rows:
        rows = [
            {
                "node": "BOM 子系统待拆分",
                "elasticityQuestion": "行业扩张会放大哪个必不可少节点？",
                "directionalElasticity": str(chain.get("plain_summary", "")) or "节点弹性待判断。",
                "whyMatters": "空间门槛只用于决定是否值得继续做 chokepoint 下钻。",
                "currentEvidence": "收入、订单、backlog、capex 锚点待补。",
                "expansionMechanism": "工作负载增长传导到 BOM 子系统。",
                "capOrRisk": "客户 ROI、供给扩张和交付质量。",
                "confidence": "中",
                "nextData": "进入 Q1/Q2 下钻。",
            }
        ]
    conclusion = chain.get("industry_space_conclusion") if isinstance(chain.get("industry_space_conclusion"), dict) else {}
    summary = str(
        conclusion.get("judgment")
        or "本节只回答一个问题：未来需求会放大哪些 BOM 节点。空间判断必须先记录公司指引、公司 TAM、客户侧指引、第三方拆法和财务兑现证据，再直接结合这五类信息判断短期、中期、长期空间是否足够大；找不到可靠公开拆法时，应明确标为数据缺口，不由模型自行补精确 TAM。"
    )
    return f"""
  <details class="industry-module industry-space">
    <summary class="module-head"><span class="module-index">02</span><div><h3>行业空间</h3><p>公开拆法优先记录 BOM 节点空间：先看推理，再看证据来源。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
      <div class="industry-space-summary">
        <p>{_e(summary)}</p>
      </div>
      {_render_space_bom_reasoning(rows, source_url_by_id)}
    </div>
  </details>
""".strip()


def _render_space_bom_reasoning(rows: list[Any], source_url_by_id: dict[str, str]) -> str:
    cards = [_render_space_node_card(row, source_url_by_id) for row in rows]
    return f'<div class="space-bom-reasoning">{"".join(cards)}</div>'


def _render_space_node_card(row: Any, source_url_by_id: dict[str, str]) -> str:
    if not isinstance(row, dict):
        cells = _row_cells(row, 6)
        row = {
            "node": cells[0] if len(cells) > 0 else "BOM 节点",
            "coreQuestion": cells[1] if len(cells) > 1 else "该节点是否被未来空间放大？",
            "facts": [cells[2]] if len(cells) > 2 else [],
            "inferenceChain": [cells[3]] if len(cells) > 3 else [],
            "refuteData": cells[4] if len(cells) > 4 else "",
            "chokepointImplication": cells[5] if len(cells) > 5 else "",
            "sourceIds": [],
        }
    facts = row.get("facts")
    if not isinstance(facts, list) or not facts:
        evidence = row.get("currentEvidence") or row.get("current_evidence") or row.get("currentAnchor") or row.get("current_anchor") or row.get("evidence") or "证据待补。"
        facts = [evidence]
    inference = row.get("inferenceChain") or row.get("inference_chain")
    if not isinstance(inference, list) or not inference:
        mechanism = row.get("expansionMechanism") or row.get("expansion_mechanism") or row.get("whyMatters") or row.get("why_matters") or "空间推理待补。"
        elasticity = row.get("nodeElasticity") or row.get("node_elasticity") or row.get("directionalElasticity") or row.get("directional_elasticity") or ""
        inference = [mechanism, elasticity] if elasticity else [mechanism]
    source_ids = row.get("sourceIds") or row.get("source_ids") or []
    if not isinstance(source_ids, list):
        source_ids = [source_ids] if source_ids else []
    fact_items = "".join(f"<li>{_e(str(fact))}</li>" for fact in facts if str(fact).strip())
    reasoning_items = "".join(f"<li>{_e(str(step))}</li>" for step in inference if str(step).strip())
    source_chips = "".join(_render_source_chip(str(source_id), source_url_by_id) for source_id in source_ids)
    numeric_sizing = _render_space_node_sizing(row.get("publicSizingMethods") or row.get("public_sizing_methods") or row.get("numericSizing") or row.get("numeric_sizing"), source_url_by_id)
    return f"""
      <details class="space-node-card">
        <summary>
          <span class="space-node-label">BOM 节点</span>
          <strong>{_e(str(row.get("node") or row.get("segment") or ""))}</strong>
          <small>{_e(str(row.get("coreQuestion") or row.get("core_question") or row.get("elasticityQuestion") or row.get("elasticity_question") or ""))}</small>
          <span class="chevron">›</span>
        </summary>
        <div class="space-node-reasoning">
          <section class="space-node-section space-node-space-reasoning"><h4>空间推理</h4><ol>{reasoning_items}</ol>{numeric_sizing}</section>
          <section class="space-node-section space-node-evidence"><h4>证据</h4><ul>{fact_items}</ul><div class="space-node-sources">{source_chips}</div></section>
        </div>
      </details>
""".strip()


def _public_method_categories() -> list[dict[str, str]]:
    return [
        {"key": "company_guidance", "label": "公司指引", "hint": "管理层给出的未来收入、capex、订单、业务增速或产能口径。"},
        {"key": "company_tam", "label": "公司 TAM", "hint": "公司披露的市场空间、长期 CAGR、服务市场或可触达市场。"},
        {"key": "customer_guidance", "label": "客户侧指引", "hint": "下游客户的 capex、RPO、订单、预算和使用量，验证真实需求来源。"},
        {"key": "third_party", "label": "第三方拆法", "hint": "研报、行业机构或数据商给出的拆分模型、TAM、出货量、价格或供需预测。"},
        {"key": "financial_evidence", "label": "财务兑现证据", "hint": "收入、订单、backlog、利润率、现金流等已经落地的经营数据。"},
    ]


def _normalize_public_method(method: Any) -> dict[str, str]:
    if isinstance(method, dict):
        source_ids = method.get("sourceIds") or method.get("source_ids") or method.get("sources") or []
        if not isinstance(source_ids, list):
            source_ids = [source_ids] if source_ids else []
        return {
            "source_type": str(method.get("sourceType") or method.get("source_type") or method.get("type") or ""),
            "organization": str(method.get("organization") or method.get("company") or method.get("source") or ""),
            "content": str(method.get("guidanceContent") or method.get("guidance_content") or method.get("guidance") or method.get("value") or method.get("method") or ""),
            "bom_node": str(method.get("bomNode") or method.get("bom_node") or method.get("node") or method.get("scope") or ""),
            "timeframe": str(method.get("timeframe") or method.get("period") or ""),
            "metric": str(method.get("verificationMetric") or method.get("verification_metric") or method.get("metric") or method.get("assumption") or method.get("keyAssumption") or method.get("key_assumption") or ""),
            "confidence": str(method.get("confidence") or ""),
            "source_ids": [str(source_id) for source_id in source_ids if source_id],
        }
    cells = (_row_cells(method, 8) + [""] * 8)[:8]
    source_ids = cells[7] if len(cells) > 7 else []
    if not isinstance(source_ids, list):
        source_ids = [source_ids] if source_ids else []
    return {
        "source_type": str(cells[0]),
        "organization": str(cells[1]),
        "content": str(cells[2]),
        "bom_node": str(cells[3]),
        "timeframe": str(cells[4]),
        "metric": str(cells[5]),
        "confidence": str(cells[6]),
        "source_ids": [str(source_id) for source_id in source_ids if source_id],
    }


def _classify_public_method(method: dict[str, str]) -> str:
    explicit = str(method.get("source_type") or "")
    category_map = {
        "公司指引": "company_guidance", "company_guidance": "company_guidance",
        "公司 TAM": "company_tam", "company_tam": "company_tam",
        "客户侧指引": "customer_guidance", "customer_guidance": "customer_guidance",
        "第三方拆法": "third_party", "third_party": "third_party",
        "财务兑现证据": "financial_evidence", "financial_evidence": "financial_evidence",
    }
    if explicit in category_map:
        return category_map[explicit]
    text = " ".join(str(method.get(key) or "") for key in ("organization", "guidance_content", "content"))
    text_lower = text.lower()
    if any(token in text for token in ("客户侧", "客户指引")) or "customer" in text_lower:
        return "customer_guidance"
    if any(token in text for token in ("公司 TAM", "TAM", "市场空间", "可触达市场")):
        return "company_tam"
    if any(token in text for token in ("第三方", "研报", "机构", "预测", "数据商")) or "sell-side" in text_lower or "forecast" in text_lower or "industry" in text_lower:
        return "third_party"
    if any(token in text for token in ("公司指引", "指引", "预计")) or "guidance" in text_lower or "outlook" in text_lower or "expected" in text_lower:
        return "company_guidance"
    if any(token in text for token in ("经营验证", "财务兑现", "公司财报", "财报", "收入", "订单", "利润", "现金")) or any(token in text_lower for token in ("revenue", "order", "backlog", "margin", "cash")):
        return "financial_evidence"
    return "third_party"


def _normalize_public_method_source_search_plan(source_search_plan: Any) -> dict[str, dict[str, Any]]:
    normalized: dict[str, dict[str, Any]] = {}
    categories = _public_method_categories()
    if isinstance(source_search_plan, dict):
        for category in categories:
            entry = source_search_plan.get(category["key"]) or source_search_plan.get(category["label"])
            if isinstance(entry, dict):
                normalized[category["key"]] = entry
                normalized[category["label"]] = entry
    elif isinstance(source_search_plan, list):
        for entry in source_search_plan:
            if not isinstance(entry, dict):
                continue
            category_key = _classify_public_method(
                {
                    "source_type": str(entry.get("category") or entry.get("source_type") or entry.get("label") or ""),
                    "organization": "",
                    "content": "",
                }
            )
            label = next((category["label"] for category in categories if category["key"] == category_key), category_key)
            normalized[category_key] = entry
            normalized[label] = entry
    return normalized


def _render_public_method_gap(category: dict[str, str], plan_entry: dict[str, Any] | None) -> tuple[str, str]:
    if isinstance(plan_entry, dict) and str(plan_entry.get("status") or plan_entry.get("search_status") or "").strip() == "gap":
        search_intent = str(plan_entry.get("search_intent") or plan_entry.get("search_query") or category["hint"])
        gap_reason = str(plan_entry.get("gap_reason") or "当前 source pack 未找到可用材料。")
        priority_sources = plan_entry.get("priority_sources") if isinstance(plan_entry.get("priority_sources"), list) else []
        priority_text = "、".join(
            str(source.get("name") or source.get("id") or "")
            for source in priority_sources[:4]
            if isinstance(source, dict) and (source.get("name") or source.get("id"))
        )
        directed_queries = plan_entry.get("directed_queries") if isinstance(plan_entry.get("directed_queries"), list) else []
        first_query = ""
        if directed_queries and isinstance(directed_queries[0], dict):
            first_query = str(directed_queries[0].get("query") or "")
        query_line = f"<br>示例 query：{_e(first_query)}" if first_query else ""
        return (
            f'<p class="space-method-empty space-method-gap">已规划专业源搜索：{_e(search_intent)}<br>优先源：{_e(priority_text or "待配置")}{query_line}<br>缺口：{_e(gap_reason)}</p>',
            "已搜索 / 缺口",
        )
    return f'<p class="space-method-empty">待补：{_e(category["hint"])}</p>', "待补"


def _source_ids_from_plan(plan_entry: dict[str, Any] | None) -> list[str]:
    if not isinstance(plan_entry, dict):
        return []
    raw_ids = (
        plan_entry.get("selected_source_ids")
        or plan_entry.get("selectedSourceIds")
        or plan_entry.get("source_ids")
        or plan_entry.get("sourceIds")
        or []
    )
    if not isinstance(raw_ids, list):
        raw_ids = [raw_ids] if raw_ids else []
    source_ids = [str(source_id) for source_id in raw_ids if source_id]
    selected_sources = plan_entry.get("selected_sources") or plan_entry.get("selectedSources") or []
    if isinstance(selected_sources, list):
        for source in selected_sources:
            if isinstance(source, dict):
                source_id = source.get("source_id") or source.get("sourceId") or source.get("id")
                if source_id:
                    source_ids.append(str(source_id))
            elif source:
                source_ids.append(str(source))
    return list(dict.fromkeys(source_ids))


def _render_public_method_cards(methods: list[Any], source_search_plan: Any = None, source_url_by_id: dict[str, str] | None = None) -> str:
    if source_url_by_id is None:
        source_url_by_id = {}
    categories = _public_method_categories()
    normalized_plan = _normalize_public_method_source_search_plan(source_search_plan)
    grouped: dict[str, list[dict[str, str]]] = {category["key"]: [] for category in categories}
    for raw_method in methods:
        method = _normalize_public_method(raw_method)
        grouped[_classify_public_method(method)].append(method)
    cards = []
    for category in categories:
        plan_entry = normalized_plan.get(category["key"]) or normalized_plan.get(category["label"])
        plan_source_ids = _source_ids_from_plan(plan_entry)
        raw_rows = grouped.get(category["key"], [])
        rows = []
        for row in raw_rows:
            if not row.get("source_ids") and plan_source_ids:
                row = {**row, "source_ids": plan_source_ids}
            rows.append(row)
        rows = [row for row in rows if row.get("source_ids")]
        missing_source_count = len(raw_rows) - len(rows)
        missing_source_note = ""
        if missing_source_count:
            missing_source_note = (
                f'<p class="space-method-empty space-method-gap">待补：'
                f'{missing_source_count} 条公开拆法材料缺少该子卡片自己的来源 ID，'
                f'已降级为缺口，需按本问题重新绑定 sourceIds 后才能作为结论展示。</p>'
            )
        if rows:
            rendered_rows = []
            for row in rows:
                source_ids = row.get("source_ids") or []
                source_chips = "".join(_render_source_chip(str(source_id), source_url_by_id) for source_id in source_ids)
                rendered_rows.append(
                    f"""
                <article class="space-method-entry">
                  <b>公司或机构：{_e(row.get("organization") or "待补")}</b>
                  <p><strong>指引内容：</strong>{_e(row.get("content") or "待补")}</p>
                  <dl>
                    <div><dt>BOM 节点</dt><dd>{_e(row.get("bom_node") or "待补")}</dd></div>
                    <div><dt>时间范围</dt><dd>{_e(row.get("timeframe") or "待补")}</dd></div>
                    <div><dt>可验证指标</dt><dd>{_e(row.get("metric") or "待补")}</dd></div>
                    <div><dt>置信度</dt><dd>{_e(row.get("confidence") or "待补")}</dd></div>
                  </dl>
                  <div class="space-method-entry-sources"><div class="source-chips">{source_chips}</div></div>
                </article>
""".strip()
                )
            body = "".join(rendered_rows) + missing_source_note
            count = f"{len(rows)} 条" if not missing_source_count else f"{len(rows)} 条 / {missing_source_count} 待补"
        else:
            body, count = _render_public_method_gap(category, plan_entry)
            body += missing_source_note
        cards.append(
            f"""
            <section class="space-method-card space-method-{_e(category["key"])}">
              <header><span>{_e(category["label"])}</span><small>{_e(count)}</small></header>
              <div class="space-method-card-body">{body}</div>
            </section>
""".strip()
        )
    return f'<div class="space-public-methods space-method-card-grid space-node-sizing-table">{"".join(cards)}</div>'


def _render_space_node_sizing(sizing: Any, source_url_by_id: dict[str, str]) -> str:
    if not isinstance(sizing, dict):
        sizing = {}
    methods = sizing.get("methods") if isinstance(sizing.get("methods"), list) else []
    source_search_plan = sizing.get("sourceSearchPlan") or sizing.get("source_search_plan") or {}
    if methods:
        source_ids = sizing.get("sourceIds") or sizing.get("source_ids") or []
        if not isinstance(source_ids, list):
            source_ids = [source_ids] if source_ids else []
        source_chips = "".join(_render_source_chip(str(source_id), source_url_by_id) for source_id in source_ids)
        return f"""
          <div class="space-node-sizing">
          <div class="space-method-step">
            <div class="space-step-title"><span class="space-step-index">1</span><h5>公开拆法</h5></div>
            {_render_public_method_cards(methods, source_search_plan, source_url_by_id)}
          </div>
          {_render_space_horizon_conclusion(sizing)}
          <div class="space-node-sources">{source_chips}</div>
        </div>
""".strip()
    formula = str(sizing.get("formula") or "待补。")
    current_anchor = str(sizing.get("currentAnchor") or sizing.get("current_anchor") or "待补。")
    future_assumption = str(sizing.get("futureAssumption") or sizing.get("future_assumption") or "待补。")
    confidence = str(sizing.get("confidence") or "低：缺少可验证锚点。")
    source_ids = sizing.get("sourceIds") or sizing.get("source_ids") or []
    if not isinstance(source_ids, list):
        source_ids = [source_ids] if source_ids else []
    scenarios = sizing.get("scenarios") if isinstance(sizing.get("scenarios"), list) else []
    if not scenarios:
        scenarios = [["待补", "待补", "需要补充 Bear/Base/Bull 或代理锚点。"]]
    rows = []
    for scenario in scenarios:
        if isinstance(scenario, dict):
            cells = [
                scenario.get("case") or scenario.get("name") or scenario.get("scenario") or "",
                scenario.get("range") or scenario.get("value") or scenario.get("anchor") or "",
                scenario.get("logic") or scenario.get("meaning") or scenario.get("note") or "",
            ]
        else:
            cells = _row_cells(scenario, 3)
        cells = (cells + [""] * 3)[:3]
        rows.append("<tr>" + "".join(f"<td>{_e(str(cell))}</td>" for cell in cells) + "</tr>")
    source_chips = "".join(_render_source_chip(str(source_id), source_url_by_id) for source_id in source_ids)
    return f"""
          <div class="space-node-sizing">
          <div class="space-method-step">
            <div class="space-step-title"><span class="space-step-index">1</span><h5>公开拆法</h5></div>
            {_render_public_method_cards([{"source_type": "旧字段兼容", "organization": "内部代理口径", "content": formula, "bom_node": current_anchor, "timeframe": "待补", "metric": future_assumption, "confidence": confidence}], source_search_plan, source_url_by_id)}
          </div>
          {_render_space_horizon_conclusion({"conclusion": str(sizing.get("conclusion") or "旧字段兼容展示，需迁移为五类公开信息。"), "confidence": confidence})}
          <div class="space-node-sizing-table table-scroll">
            <table>
              <thead><tr><th>情景</th><th>空间区间 / 代理锚点</th><th>推理含义</th></tr></thead>
              <tbody>{"".join(rows)}</tbody>
            </table>
          </div>
          <div class="space-node-sources">{source_chips}</div>
        </div>
""".strip()


def _render_space_horizon_conclusion(sizing: dict[str, Any]) -> str:
    horizon = sizing.get("horizonConclusion") or sizing.get("horizon_conclusion")
    if not isinstance(horizon, dict):
        conclusion = str(sizing.get("conclusion") or "现有公开信息不足，不能给出高置信空间判断。")
        horizon = {
            "summary": f"结论：{conclusion}",
            "confidence": str(sizing.get("confidence") or "低：缺少完整公开方法。"),
            "horizons": [
                {"label": "短期", "size": "中", "reason": "主要看公司指引和财务兑现证据能否继续支持近端需求。"},
                {"label": "中期", "size": "中", "reason": "主要看公司 TAM、客户侧指引和第三方拆法能否共同指向扩张。"},
                {"label": "长期", "size": "待验证", "reason": "长期空间需要继续验证供给扩张、价格、替代路线和客户 ROI。"},
            ],
        }
    horizons = horizon.get("horizons") if isinstance(horizon.get("horizons"), list) else []
    if not horizons:
        horizons = [
            {"label": "短期", "size": "待验证", "reason": "需要补充近端指引。"},
            {"label": "中期", "size": "待验证", "reason": "需要补充中期公开拆法。"},
            {"label": "长期", "size": "待验证", "reason": "需要补充长期需求和供给材料。"},
        ]
    cards = []
    for item in horizons:
        if not isinstance(item, dict):
            continue
        size = str(item.get("size") or "待验证")
        cards.append(
            f"""
            <article class="space-horizon-card">
              <span>{_e(str(item.get("label") or "待补"))}</span>
              <strong class="{_e(_horizon_size_class(size))}">{_e(size)}</strong>
              <p>{_e(str(item.get("reason") or "待补。"))}</p>
            </article>
""".strip()
        )
    return f"""
          <div class="space-horizon-conclusion">
            <div class="space-step-title"><span class="space-step-index">2</span><h5>空间结论</h5></div>
            <p class="space-horizon-summary">{_e(str(horizon.get("summary") or "待补。"))}</p>
            <div class="space-horizon-grid">{"".join(cards)}</div>
            <small class="space-step-confidence">置信度：{_e(str(horizon.get("confidence") or sizing.get("confidence") or "待补。"))}</small>
          </div>
""".strip()


def _horizon_size_class(size: str) -> str:
    if "大" in size:
        return "space-horizon-size space-horizon-large"
    if "中" in size:
        return "space-horizon-size space-horizon-mid"
    if "小" in size or "低" in size:
        return "space-horizon-size space-horizon-low"
    return "space-horizon-size"


def _render_space_detail_panel(title: str, description: str, body: str, class_name: str) -> str:
    return f"""
      <details class="space-detail-panel {class_name}">
        <summary><span>{_e(title)}</span><small>{_e(description)}</small><span class="chevron">›</span></summary>
        <div class="space-detail-body">{body}</div>
      </details>
""".strip()


def _render_space_boundary(chain: dict[str, Any]) -> str:
    rows = chain.get("industry_space_boundary") if isinstance(chain.get("industry_space_boundary"), list) else []
    if not rows:
        rows = [
            ["纳入口径", "与研究主题直接相关的需求、订单、收入、backlog、capex 和交付空间。"],
            ["排除口径", "竞争份额、利润池归属、估值和标的排序不在行业空间模块回答。"],
            ["时间口径", "使用截止日前可见材料，观察未来 12-36 个月验证数据。"],
            ["测算方法", "先把当前截面数据作为证据锚点，再拆 BOM 扩张机制、未来空间和验证数据。"],
        ]
    cards = []
    for row in rows:
        cells = (_row_cells(row, 2) + ["", ""])[:2]
        cards.append(f"<article><span>{_e(str(cells[0]))}</span><p>{_e(str(cells[1]))}</p></article>")
    return f'<div class="space-boundary-grid">{"".join(cards)}</div>'


def _render_space_driver_tree(chain: dict[str, Any]) -> str:
    rows = chain.get("industry_space_driver_tree") if isinstance(chain.get("industry_space_driver_tree"), list) else []
    if not rows:
        rows = [
            {"layer": "1. 需求源头", "driver": "工作负载、客户预算和订单。", "measurable": "capex、收入、RPO/backlog、订单。", "output": "形成行业空间。"},
            {"layer": "2. 规格传导", "driver": "平台规格提高 BOM 和基础设施要求。", "measurable": "产品 mix、单位价值量、功耗/带宽。", "output": "放大硬件空间。"},
            {"layer": "3. 交付验证", "driver": "系统交付把订单变成上线产能。", "measurable": "shipments、backlog conversion、现金流。", "output": "验证空间质量。"},
        ]
    cards = []
    for row in rows:
        if isinstance(row, dict):
            layer = row.get("layer", "")
            driver = row.get("driver", "")
            measurable = row.get("measurable", "")
            output = row.get("output", "")
        else:
            cells = _row_cells(row, 4) + ["", "", "", ""]
            layer, driver, measurable, output = cells[:4]
        cards.append(
            f"""
        <article class="space-driver-card">
          <span>{_e(str(layer))}</span>
          <b>{_e(str(driver))}</b>
          <dl><div><dt>可观测指标</dt><dd>{_e(str(measurable))}</dd></div><div><dt>空间输出</dt><dd>{_e(str(output))}</dd></div></dl>
        </article>
""".strip()
        )
    return f'<div class="space-driver-tree">{"".join(cards)}</div>'


def _render_space_node_elasticity_table(rows: list[Any]) -> str:
    body_rows = []
    for row in rows:
        if isinstance(row, dict):
            cells = [
                row.get("node") or row.get("segment", ""),
                row.get("elasticityQuestion") or row.get("elasticity_question") or row.get("formula", ""),
                row.get("directionalElasticity") or row.get("directional_elasticity") or row.get("futureSpace") or row.get("future_space") or row.get("read", ""),
                row.get("whyMatters") or row.get("why_matters") or row.get("investment_read") or "用于判断该节点是否值得进入 Q2 chokepoint 下钻。",
                row.get("currentEvidence") or row.get("current_evidence") or row.get("currentAnchor") or row.get("current_anchor", ""),
                row.get("expansionMechanism") or row.get("expansion_mechanism") or row.get("sizingMethod") or row.get("sizing_method", ""),
                row.get("capOrRisk") or row.get("cap_or_risk") or row.get("upperBound") or row.get("upper_bound") or row.get("growthDriver") or row.get("growth_driver", ""),
                row.get("confidence", ""),
                ", ".join(str(item) for item in row.get("sourceIds", row.get("source_ids", []))) if isinstance(row.get("sourceIds", row.get("source_ids", [])), list) else row.get("sourceIds", row.get("source_ids", "")),
                row.get("nextData") or row.get("next_data", ""),
            ]
        else:
            cells = _row_cells(row, 10)
            if len(cells) == 5:
                cells = [cells[0], "弹性问题待补。", cells[1], "用于判断 chokepoint 下钻优先级。", cells[2], "用截面证据作为空间锚点。", "客户 ROI、供给扩张和交付质量。", "中", "", cells[4]]
        cells = (cells + [""] * 10)[:10]
        body_rows.append("<tr>" + "".join(f"<td>{_e(str(cell))}</td>" for cell in cells) + "</tr>")
    return """
      <div class="space-node-elasticity-table table-scroll"><table>
        <thead><tr><th>BOM 节点</th><th>弹性问题</th><th>方向性弹性</th><th>为什么影响 chokepoint</th><th>当前截面证据</th><th>扩张机制</th><th>上限 / 风险</th><th>可信度</th><th>来源</th><th>下一步数据</th></tr></thead>
        <tbody>{}</tbody>
      </table></div>
""".format("".join(body_rows)).strip()


def _render_space_evidence_pack(rows: list[Any]) -> str:
    if not rows:
        rows = [
            {
                "node": "节点证据包待补",
                "coreQuestion": "哪些 cutoff-visible 事实能支持或反证该节点的未来空间弹性？",
                "facts": ["收入、订单、backlog、capex、RPO、价格、库存和毛利证据待补。"],
                "inferenceChain": ["事实锚点 -> 空间弹性 -> chokepoint 影响 -> 反证数据。"],
                "nodeElasticity": "节点弹性待判断。",
                "chokepointImplication": "证据包用于把行业空间传递给 Q2 chokepoint 和 Q4 target ranking。",
                "refuteData": "需要补充能推翻空间弹性的客户、供给、价格和现金流数据。",
                "sourceIds": [],
            }
        ]
    cards = []
    for row in rows:
        if not isinstance(row, dict):
            cells = _row_cells(row, 6)
            row = {
                "node": cells[0] if len(cells) > 0 else "节点证据包",
                "coreQuestion": cells[1] if len(cells) > 1 else "该节点是否被行业空间放大？",
                "facts": [cells[2]] if len(cells) > 2 else [],
                "inferenceChain": [cells[3]] if len(cells) > 3 else [],
                "nodeElasticity": cells[4] if len(cells) > 4 else "",
                "refuteData": cells[5] if len(cells) > 5 else "",
                "sourceIds": [],
            }
        facts = row.get("facts") if isinstance(row.get("facts"), list) else [row.get("facts", "")]
        inference = row.get("inferenceChain") or row.get("inference_chain")
        inference_steps = inference if isinstance(inference, list) else [inference or ""]
        source_ids = row.get("sourceIds") or row.get("source_ids") or []
        if not isinstance(source_ids, list):
            source_ids = [source_ids] if source_ids else []
        fact_items = "".join(f"<li>{_e(str(fact))}</li>" for fact in facts if str(fact).strip())
        chain_items = "".join(f"<li>{_e(str(step))}</li>" for step in inference_steps if str(step).strip())
        source_chips = "".join(_render_source_chip(str(source_id), {}) for source_id in source_ids)
        cards.append(
            f"""
        <article class="space-evidence-card">
          <header>
            <span>节点证据包</span>
            <h4>{_e(str(row.get("node", "")))}</h4>
            <p>{_e(str(row.get("coreQuestion") or row.get("core_question") or ""))}</p>
          </header>
          <div class="space-evidence-grid">
            <section><b>事实锚点</b><ul>{fact_items}</ul><div class="space-evidence-sources">{source_chips}</div></section>
            <section><b>推理链条</b><ol class="space-inference-chain">{chain_items}</ol></section>
            <section><b>节点弹性</b><p>{_e(str(row.get("nodeElasticity") or row.get("node_elasticity") or ""))}</p></section>
            <section><b>对 chokepoint 的影响</b><p>{_e(str(row.get("chokepointImplication") or row.get("chokepoint_implication") or ""))}</p></section>
            <section class="space-refute-box"><b>反证数据</b><p>{_e(str(row.get("refuteData") or row.get("refute_data") or ""))}</p></section>
          </div>
        </article>
""".strip()
        )
    return f'<div class="space-evidence-pack">{"".join(cards)}</div>'


def _render_space_gate_model(model: dict[str, Any]) -> str:
    horizon = str(model.get("horizon") or "未来 12-36 个月，使用截止日前可见材料作为判断起点。")
    space_level = str(model.get("spaceLevel") or model.get("space_level") or model.get("totalRange") or model.get("total_range") or "空间等级待判断。")
    expansion = str(model.get("expansionCertainty") or model.get("expansion_certainty") or model.get("dedupedDefinition") or model.get("deduped_definition") or "扩张确定性待判断。")
    amplification = str(model.get("chokepointAmplification") or model.get("chokepoint_amplification") or "chokepoint 放大作用待判断。")
    confidence = str(model.get("confidence") or "中：当前证据用于决定是否继续下钻，不用于精确总盘。")
    method = str(model.get("method") or "用收入、订单、backlog、capex 作为锚点，判断产业扩张是否足以放大稀缺节点。")
    not_used = str(model.get("notUsed") or model.get("not_used") or model.get("nonAdditiveWarning") or model.get("non_additive_warning") or "不使用手工精确 TAM 作为标的评分依据。")
    return f"""
      <div class="space-gate-model">
        <div class="space-model-grid">
          <article><span>判断 horizon</span><strong>{_e(horizon)}</strong></article>
          <article><span>空间等级</span><strong>{_e(space_level)}</strong></article>
          <article><span>扩张确定性</span><strong>{_e(expansion)}</strong></article>
          <article><span>瓶颈放大作用</span><strong>{_e(amplification)}</strong></article>
        </div>
        <div class="space-model-note"><b>使用方法</b><p>{_e(method)}</p></div>
        <div class="space-model-note warning"><b>不用作精确 TAM</b><p>{_e(not_used)}</p></div>
        <div class="space-model-note"><b>可信度</b><p>{_e(confidence)}</p></div>
      </div>
""".strip()


def _render_space_scenario_table(rows: list[Any]) -> str:
    if not rows:
        rows = [
            {
                "scenario": "门槛通过 / 待验证扩张",
                "gateResult": "空间等级待判断",
                "futureSpace": "未来空间是否扩张取决于需求和规格能否放大必不可少节点。",
                "keyAssumptions": "客户 capex、订单、backlog 和 ROI 不明显恶化。",
                "expansionPath": "需求 -> BOM 子系统 -> 系统交付 -> 收入和现金流。",
                "upperBound": "客户 ROI、供给扩张、交付质量和价格压力。",
                "watchData": "capex、收入、订单、backlog、价格、库存和毛利。",
            }
        ]
    body_rows = []
    for row in rows:
        if isinstance(row, dict):
            cells = [
                row.get("scenario", ""),
                row.get("gateResult") or row.get("gate_result") or row.get("estimated2028") or row.get("estimated_2028") or row.get("numericRange") or row.get("numeric_range", ""),
                row.get("futureSpace") or row.get("future_space", ""),
                row.get("keyAssumptions") or row.get("key_assumptions", ""),
                row.get("expansionPath") or row.get("expansion_path", ""),
                row.get("upperBound") or row.get("upper_bound", ""),
                row.get("watchData") or row.get("watch_data", ""),
            ]
        else:
            cells = _row_cells(row, 7)
        cells = (cells + [""] * 7)[:7]
        body_rows.append("<tr>" + "".join(f"<td>{_e(str(cell))}</td>" for cell in cells) + "</tr>")
    return """
      <div class="space-scenario-table table-scroll"><table>
        <thead><tr><th>情景</th><th>空间门槛</th><th>未来空间判断</th><th>关键假设</th><th>扩张路径</th><th>削弱条件</th><th>后续验证数据</th></tr></thead>
        <tbody>{}</tbody>
      </table></div>
""".format("".join(body_rows)).strip()


def _render_space_validation_table(chain: dict[str, Any]) -> str:
    rows = chain.get("industry_space_validation_rows") if isinstance(chain.get("industry_space_validation_rows"), list) else []
    if not rows:
        rows = [
            ["客户需求", "capex、收入、RPO/backlog、FCF", "证明需求能转成商业回报", "capex 增长但收入/现金流不跟随"],
            ["系统交付", "shipments、backlog conversion、取消率", "证明订单能转成上线产能", "backlog 增长但交付延迟"],
            ["供给扩张", "产能、价格、库存、项目毛利", "证明空间没有被供给快速压缩", "价格下行或库存上升"],
        ]
    body = "\n".join("<tr>" + "".join(f"<td>{_e(str(cell))}</td>" for cell in (_row_cells(row, 4) + ["", "", "", ""])[:4]) + "</tr>" for row in rows)
    return f'<div class="space-validation-table table-scroll"><table><thead><tr><th>验证对象</th><th>跟踪数据</th><th>说明什么</th><th>削弱信号</th></tr></thead><tbody>{body}</tbody></table></div>'


def _render_industry_competition(chain: dict[str, Any], source_url_by_id: dict[str, str]) -> str:
    competition = chain.get("competition") if isinstance(chain.get("competition"), dict) else {}
    node_cards = competition.get("chain_node_competition") or chain.get("competition_cards") or []

    if isinstance(node_cards, list) and node_cards:
        cards_html = "".join(_render_competition_node_card(node, i, source_url_by_id) for i, node in enumerate(node_cards))
        body_html = f'<div class="competition-bom-map">{cards_html}</div>'
    else:
        body_html = _render_competition_fallback_table(
            chain.get("competition_rows") or chain.get("competitionLandscape") or [],
            source_url_by_id,
        )

    return f"""
  <details class="industry-module industry-competition">
    <summary class="module-head"><span class="module-index">03</span><div><h3>竞争格局与利润池</h3><p>每个 BOM 节点按四问展开：玩家市场份额分布、头部玩家优势、替代玩家赶超希望、格局变化核心变量。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
    {body_html}
    </div>
  </details>
""".strip()


def _render_competition_node_card(node: dict[str, Any], index: int, source_url_by_id: dict[str, str]) -> str:
    node_name = str(node.get("node") or "")
    intensity = str(node.get("competitive_intensity") or "待补")
    questions = node.get("questions") if isinstance(node.get("questions"), list) else []
    intensity_class = {"低": "competition-low", "中低": "competition-midlow", "中": "competition-mid", "中高": "competition-high", "高": "competition-high", "极低": "competition-low"}
    ic = intensity_class.get(intensity, "competition-mid")
    subcards = ""
    for q in questions:
        if not isinstance(q, dict):
            continue
        q_text = str(q.get("question") or "")
        q_answer = q.get("answer_sections") if isinstance(q.get("answer_sections"), dict) else q.get("answer")
        if not q_answer:
            q_answer = ""
        q_sids = q.get("sourceIds") or q.get("source_ids") or []
        if not isinstance(q_sids, list):
            q_sids = [q_sids] if q_sids else []
        subcards += _render_overview_question_card(
            question=q_text,
            answer=q_answer,
            source_ids=q_sids,
            source_url_by_id=source_url_by_id,
            source_plan=q.get("source_plan") if isinstance(q.get("source_plan"), dict) else q,
        )
    profit_pool_table = _render_node_profit_pool_table(node)
    return f"""
        <details class="competition-node-card competition-bom-card">
          <summary>
            <span class="competition-node-index">{index + 1:02d}</span>
            <strong>{_e(node_name)}</strong>
            <span class="competition-intensity {ic}">竞争烈度：{_e(intensity)}</span>
            <span class="chevron">›</span>
          </summary>
          <div class="competition-node-body">
            <div class="overview-research-unit">
              <div class="overview-unit-head"><b>研究单元</b><span>{_e(node_name)} · 围绕四个竞争问题给出结论。</span></div>
              <div class="competition-question-grid">{subcards}</div>
            </div>
            {profit_pool_table}
          </div>
        </details>""".strip()


def _render_node_profit_pool_table(node: dict[str, Any]) -> str:
    profit_pool_owner = str(node.get("profit_pool_owner") or node.get("profit_pool") or node.get("profit") or "待验证")
    financial_metric = str(node.get("financial_metric") or node.get("financial_validation_metric") or "收入、毛利、现金流和估值弹性")
    refute = str(node.get("profit_pool_refute") or node.get("refuting_trigger") or node.get("refute") or "供给扩张、客户议价或替代路线导致利润池迁移")
    return f"""
            <div class="profit-pool-table table-scroll">
              <table>
                <thead><tr><th>利润池归属</th><th>可财务化指标</th><th>反证/迁移触发器</th></tr></thead>
                <tbody><tr><td>{_e(profit_pool_owner)}</td><td>{_e(financial_metric)}</td><td>{_e(refute)}</td></tr></tbody>
              </table>
            </div>""".strip()


def _render_competition_fallback_table(rows: list[Any], source_url_by_id: dict[str, str]) -> str:
    if not isinstance(rows, list) or not rows:
        rows = [["核心节点", "竞争者和替代路线待补", "是否形成 chokepoint 待验证", "利润池归属待验证", "供给扩张/客户议价", "进入 Q2 下钻"]]
    body = "\n".join("<tr>" + "".join(f"<td>{_e(str(cell))}</td>" for cell in _row_cells(row, 6)) + "</tr>" for row in rows)
    return f"""
    <div class="competition-bom-map">
      <details class="competition-node-card competition-bom-card">
        <summary><span class="competition-node-index">01</span><strong>核心 BOM 节点</strong><span class="competition-intensity competition-mid">竞争烈度：待补</span><span class="chevron">›</span></summary>
        <div class="competition-node-body">
          <div class="overview-research-unit">
            <div class="overview-unit-head"><b>研究单元</b><span>核心 BOM 节点 · 围绕四个竞争问题给出结论。</span></div>
            <div class="competition-question-grid">
              {_render_overview_question_card(question="玩家市场份额分布", answer="待补。", source_ids=[], source_url_by_id=source_url_by_id)}
              {_render_overview_question_card(question="头部玩家优势分析", answer="待补。", source_ids=[], source_url_by_id=source_url_by_id)}
              {_render_overview_question_card(question="替代玩家赶超希望", answer="待补。", source_ids=[], source_url_by_id=source_url_by_id)}
              {_render_overview_question_card(question="格局变化核心变量", answer="待补。", source_ids=[], source_url_by_id=source_url_by_id)}
            </div>
          </div>
          <div class="profit-pool-table table-scroll"><table><thead><tr><th>节点</th><th>竞争格局</th><th>Chokepoint 初判</th><th>利润池/标的含义</th><th>主要反证</th><th>后续 QA</th></tr></thead><tbody>{body}</tbody></table></div>
        </div>
      </details>
    </div>""".strip()


def _render_profit_pool_flow(profit_pool: dict[str, Any]) -> str:
    summary = str(profit_pool.get("summary") or "")
    nodes = profit_pool.get("nodes") if isinstance(profit_pool.get("nodes"), list) else []
    rows = ""
    for n in nodes:
        if not isinstance(n, dict):
            continue
        rows += f"""
          <tr>
            <td><strong>{_e(str(n.get('node') or ''))}</strong></td>
            <td>{_e(str(n.get('estimated_revenue') or ''))}</td>
            <td>{_e(str(n.get('gross_margin') or ''))}</td>
            <td><span class="profit-badge profit-{n.get('profit_retention','中').replace('极高','high').replace('高','high').replace('中高','mid').replace('中','mid').replace('低','low').replace('极低','low')}">{_e(str(n.get('profit_retention') or ''))}</span></td>
            <td class="profit-rationale">{_e(str(n.get('rationale') or ''))}</td>
          </tr>"""
    return f"""
      <div class="profit-pool-flow">
        <div class="chain-graph-head"><b>利润池流向</b><span>{_e(summary)}</span></div>
        <div class="table-scroll"><table>
          <thead><tr><th>节点</th><th>估算收入规模</th><th>毛利率区间</th><th>利润截留</th><th>依据</th></tr></thead>
          <tbody>{rows}</tbody>
        </table></div>
      </div>""".strip()


def _render_industry_chokepoints(chain: dict[str, Any], source_url_by_id: dict[str, str]) -> str:
    nodes = chain.get("chokepoint_nodes") or []
    if isinstance(nodes, list) and nodes:
        cards = '<div class="chokepoint-bom-map">' + "".join(_render_chokepoint_node_card(node, i, source_url_by_id) for i, node in enumerate(nodes)) + "</div>"
    else:
        text = chain.get("chokepoints") or "瓶颈点待 Q2 竞争格局验证。"
        cards = f"""
    <div class="chain-chokepoints">{_e(str(text))}</div>
    <div class="chokepoint-bom-map">
      <details class="competition-node-card chokepoint-card chokepoint-bom-card" open>
        <summary><span class="competition-node-index chokepoint-index">01</span><strong>核心 BOM 节点</strong><span class="chevron">›</span></summary>
        <div class="competition-node-body">
          <div class="overview-research-unit">
            <div class="overview-unit-head"><b>研究单元</b><span>核心 BOM 节点 · 围绕瓶颈约束、控制者和降级规则给出结论。</span></div>
            <div class="chokepoint-question-grid">
              {_render_overview_question_card(question="具体约束是什么", answer="待补。", source_ids=[], source_url_by_id=source_url_by_id)}
              {_render_overview_question_card(question="谁控制该约束", answer="待补。", source_ids=[], source_url_by_id=source_url_by_id)}
              {_render_overview_question_card(question="稀缺会持续多久", answer="待补。", source_ids=[], source_url_by_id=source_url_by_id)}
              {_render_overview_question_card(question="扩产/替代/释放路径", answer="待补。", source_ids=[], source_url_by_id=source_url_by_id)}
              {_render_overview_question_card(question="量化评分与降级规则", answer="待补。", source_ids=[], source_url_by_id=source_url_by_id)}
              {_render_overview_question_card(question="标的影响/监控触发器", answer="待补。", source_ids=[], source_url_by_id=source_url_by_id)}
            </div>
          </div>
          <div class="chokepoint-scorecard">评分待补。</div>
        </div>
      </details>
    </div>"""
    return f"""
  <details class="industry-module industry-chokepoints">
    <summary class="module-head"><span class="module-index">04</span><div><h3>瓶颈点</h3><p>四问每个链节点：瓶颈在哪、有多紧、会释放还是会加剧、有没有中小市值卡点。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
    <div class="chain-chokepoints" hidden></div>
    <div class="bottleneck-release-timeline" hidden></div>
    {cards}
    </div>
  </details>
""".strip()


def _render_chokepoint_node_card(node: dict[str, Any], index: int, source_url_by_id: dict[str, str]) -> str:
    node_name = str(node.get("node") or "")
    questions = node.get("questions") if isinstance(node.get("questions"), list) else []
    subcards = ""
    for q in questions:
        if not isinstance(q, dict):
            continue
        q_text = str(q.get("question") or "")
        q_answer = str(q.get("answer") or "")
        q_sids = q.get("sourceIds") or q.get("source_ids") or []
        if not isinstance(q_sids, list):
            q_sids = [q_sids] if q_sids else []
        subcards += _render_overview_question_card(
            question=q_text,
            answer=q_answer,
            source_ids=q_sids,
            source_url_by_id=source_url_by_id,
            source_plan=q.get("source_plan") if isinstance(q.get("source_plan"), dict) else q,
        )
    scorecard = _render_chokepoint_scorecard(node)
    return f"""
        <details class="competition-node-card chokepoint-card chokepoint-bom-card" open>
          <summary>
            <span class="competition-node-index chokepoint-index">{index + 1:02d}</span>
            <strong>{_e(node_name)}</strong>
            <span class="chevron">›</span>
          </summary>
          <div class="competition-node-body">
            <div class="overview-research-unit">
              <div class="overview-unit-head"><b>研究单元</b><span>{_e(node_name)} · 围绕瓶颈约束、控制者和降级规则给出结论。</span></div>
              <div class="chokepoint-question-grid">{subcards}</div>
            </div>
            {scorecard}
          </div>
        </details>""".strip()


def _render_chokepoint_scorecard(node: dict[str, Any]) -> str:
    score = node.get("score") or node.get("scores") or node.get("chokepoint_score") or "待补"
    downgrade = str(node.get("downgrade_rule") or node.get("refuting_trigger") or node.get("release_trigger") or "供给释放、替代路线成熟或利润率下行则降级")
    return f"""
            <div class="chokepoint-scorecard">
              <strong>量化评分与降级规则</strong>
              <p>评分：{_e(str(score))}</p>
              <p>降级：{_e(downgrade)}</p>
            </div>""".strip()


def _render_component_value_chain(items: list[Any]) -> str:
    if not isinstance(items, list) or not items:
        rows = [
            ["待补充", "子系统/组件", "关键公司", "接受什么输入", "提供给谁", "财务验证指标", "相关 QA"],
        ]
    else:
        rows = [_row_cells(item, 7) for item in items]
    body = "\n".join("<tr>" + "".join(f"<td>{_e(str(cell))}</td>" for cell in row) + "</tr>" for row in rows)
    return f"""
    <div class="component-value-chain">
      <div class="chain-graph-head"><b>BOM / 组件级价值链</b><span>从系统拆到子系统、供应商和财务验证指标。</span></div>
      <div class="table-scroll"><table>
        <thead><tr><th>子系统</th><th>组件/服务</th><th>关键公司</th><th>接受什么</th><th>提供给谁</th><th>财务验证</th><th>相关 QA</th></tr></thead>
        <tbody>{body}</tbody>
      </table></div>
    </div>
""".strip()


def _render_bottleneck_release_timeline(items: list[Any]) -> str:
    if not isinstance(items, list) or not items:
        rows = [
            ["待补充", "当前约束", "释放/验证信号", "观察节奏", "降级触发", "标的含义"],
        ]
    else:
        rows = [_row_cells(item, 6) for item in items]
    body = "\n".join("<tr>" + "".join(f"<td>{_e(str(cell))}</td>" for cell in row) + "</tr>" for row in rows)
    return f"""
    <div class="bottleneck-release-timeline">
      <div class="chain-graph-head"><b>瓶颈释放时间表</b><span>瓶颈必须跟踪扩产、缓解和降级触发。</span></div>
      <div class="table-scroll"><table>
        <thead><tr><th>瓶颈</th><th>当前约束</th><th>释放/验证信号</th><th>观察节奏</th><th>降级触发</th><th>标的含义</th></tr></thead>
        <tbody>{body}</tbody>
      </table></div>
    </div>
""".strip()


def _render_industry_key_variables(chain: dict[str, Any], data_gaps: str) -> str:
    qa_mapping = chain.get("qa_mapping") or chain.get("output_to_qa") or []
    if not isinstance(qa_mapping, list) or not qa_mapping:
        qa_mapping = [["Q1-Q4", "行业概况里的空间、竞争、瓶颈和反证信号。", "用于生成下钻 QA 和标的排序。"]]
    rows = "\n".join("<tr>" + "".join(f"<td>{_e(str(cell))}</td>" for cell in _row_cells(row, 3)) + "</tr>" for row in qa_mapping)
    bom_nodes = _extract_bom_taxonomy_nodes(chain)
    component_value_chain = chain.get("component_value_chain") or []
    bottleneck_timeline = chain.get("bottleneck_release_timeline") or chain.get("release_timeline") or []
    node_cards: list[str] = []
    for node in bom_nodes:
        label = node["label"]
        component = next((row for row in component_value_chain if _row_cells(row, 7) and str(_row_cells(row, 7)[0]).strip() == label), None)
        timeline = next((row for row in bottleneck_timeline if _row_cells(row, 6) and str(_row_cells(row, 6)[0]).strip() == label), None)
        component_cells = _row_cells(component, 7) if component is not None else []
        timeline_cells = _row_cells(timeline, 6) if timeline is not None else []
        verification = str(component_cells[5] if len(component_cells) > 5 else (timeline_cells[2] if len(timeline_cells) > 2 else "订单、收入、毛利、现金流和反证触发器。"))
        key_variable = str(timeline_cells[2] if len(timeline_cells) > 2 else verification)
        downgrade = str(timeline_cells[4] if len(timeline_cells) > 4 else "待补该 BOM 节点的降级触发器。")
        target = str(timeline_cells[5] if len(timeline_cells) > 5 else "待补标的映射。")
        qa = str(component_cells[6] if len(component_cells) > 6 else "Q1-Q4")
        node_cards.append(
            f"""
        <details class="key-variable-bom-card overview-research-unit">
          <summary><strong>{_e(label)}</strong><span>{_e(node.get("layer", "BOM 节点"))} · {_e(qa)}</span><span class="chevron">›</span></summary>
          <div class="overview-question-card overview-answer overview-answer-structured">
            <div class="overview-answer-row"><span>当前要验证什么</span><p>{_e(verification)}</p></div>
            <div class="overview-answer-row"><span>关键变量</span><p>{_e(key_variable)}</p></div>
            <div class="overview-answer-row"><span>降级触发器</span><p>{_e(downgrade)}</p></div>
            <div class="overview-answer-row"><span>标的映射</span><p>{_e(target)}</p></div>
          </div>
        </details>
""".strip()
        )
    bom_map = f'<div class="key-variable-bom-map">{"".join(node_cards)}</div>' if node_cards else ""
    return f"""
  <details class="industry-module industry-key-variables">
    <summary class="module-head"><span class="module-index">05</span><div><h3>关键变量与待验证数据</h3><p>把行业概况转成下钻 QA：哪些数据变化会强化、削弱或推翻当前排序。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
    <div class="key-variable-grid">
      {bom_map}
      {data_gaps}
      <div class="qa-generation-table table-scroll"><table><thead><tr><th>QA 方向</th><th>来自行业概况的信号</th><th>怎么使用</th></tr></thead><tbody>{rows}</tbody></table></div>
    </div>
    </div>
  </details>
""".strip()


def _chain_node_lens_item(row: Any) -> str:
    if isinstance(row, dict):
        title = row.get("name") or row.get("title") or row.get("dimension") or ""
        desc = row.get("description") or row.get("test") or row.get("question") or ""
    elif isinstance(row, list) and row:
        title = row[0]
        desc = row[1] if len(row) > 1 else ""
    else:
        title = str(row)
        desc = ""
    return f"<li><b>{_e(str(title))}</b><span>{_e(str(desc))}</span></li>"


def _render_chain_value_capture_matrix(items: list[dict[str, Any]]) -> str:
    if not isinstance(items, list) or not items:
        rows = '<tr><td colspan="7">价值捕获矩阵仍待补充：需要逐节点说明需求如何流入、卡点机制、价值捕获方式、对应标的、验证数据和 QA 链接。</td></tr>'
    else:
        rows = "\n".join(_chain_value_capture_row(item) for item in items if isinstance(item, dict))
    return f"""
    <div class="chain-value-capture-matrix">
      <div class="chain-graph-head">
        <p class="chain-graph-title">价值捕获矩阵</p>
        <p class="muted">从需求流入一路看到账面利润、估值赔率和后续验证问题。</p>
      </div>
      <div class="table-scroll"><table>
        <thead><tr><th>节点</th><th>需求如何流入</th><th>卡点机制</th><th>价值捕获方式</th><th>主要标的</th><th>继续验证</th><th>后续 QA</th></tr></thead>
        <tbody>{rows}</tbody>
      </table></div>
    </div>
""".strip()


def _chain_value_capture_row(item: dict[str, Any]) -> str:
    return f"""
        <tr>
          <td><strong>{_e(str(item.get("node") or item.get("name") or ""))}</strong></td>
          <td>{_e(str(item.get("demand") or item.get("demand_flow") or ""))}</td>
          <td>{_e(str(item.get("chokepoint") or item.get("bottleneck") or ""))}</td>
          <td>{_e(str(item.get("monetization") or item.get("value_capture") or ""))}</td>
          <td>{_e(str(item.get("targets") or item.get("players") or ""))}</td>
          <td>{_e(str(item.get("verification") or item.get("data_needed") or ""))}</td>
          <td>{_e(str(item.get("qa") or item.get("qa_link") or ""))}</td>
        </tr>
""".rstrip()


def _render_chain_qa_mapping(items: list[dict[str, Any]]) -> str:
    if not isinstance(items, list) or not items:
        cards = '<article><span>Q1-Q4</span><b>待映射</b><p>需要把产业链节点、价值流和反证点转成下钻 QA。</p></article>'
    else:
        cards = "\n".join(_chain_qa_mapping_card(item) for item in items if isinstance(item, dict))
    return f"""
    <div class="chain-qa-mapping">
      <div class="chain-graph-head">
        <p class="chain-graph-title">产业链如何生成下钻 QA</p>
        <p class="muted">QA 不是独立模板，而是由链条卡点、价值流和反证点推出来。</p>
      </div>
      <div class="chain-qa-grid">{cards}</div>
    </div>
""".strip()


def _chain_qa_mapping_card(item: dict[str, Any]) -> str:
    return f"""
        <article>
          <span>{_e(str(item.get("q") or item.get("question_id") or ""))}</span>
          <b>{_e(str(item.get("signal") or item.get("question") or ""))}</b>
          <p>{_e(str(item.get("use") or item.get("decision_use") or ""))}</p>
        </article>
""".rstrip()


def _render_chain_data_gaps(items: list[Any]) -> str:
    if not isinstance(items, list) or not items:
        items = ["补充每个关键节点的订单、价格、毛利、现金流、估值、客户集中和反证触发器。"]
    lis = "\n".join(f"<li>{_e(str(item))}</li>" for item in items[:3])
    return f"""
    <details class="chain-data-gaps">
      <summary>待补充的关键数据 <span class="chevron">›</span></summary>
      <ul>{lis}</ul>
    </details>
""".strip()


def _render_chain_relationship_workbench(
    chain: dict[str, Any],
    stage_groups: list[dict[str, Any]],
    layers: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
) -> str:
    stage_panels = _render_chain_stage_panels(stage_groups, layers, relationships)
    value_flow = _render_chain_sankey_flow(
        chain.get("sankey_flows")
        or chain.get("value_flows")
        or chain.get("supply_chain_sankey")
        or chain.get("sankey")
        or []
    )
    heatmap = _render_chain_chokepoint_heatmap(
        chain.get("chokepoint_heatmap")
        or chain.get("supply_chain_chokepoint_heatmap")
        or chain.get("bottleneck_scores")
        or []
    )
    return f"""
    <div class="chain-relationship-workbench">
      <input class="chain-view-radio" type="radio" name="chain-view" id="chain-view-lanes" checked>
      <input class="chain-view-radio" type="radio" name="chain-view" id="chain-view-sankey">
      <input class="chain-view-radio" type="radio" name="chain-view" id="chain-view-heatmap">
      <div class="chain-view-switch" role="tablist" aria-label="产业链关系视图">
        <label for="chain-view-lanes">泳道图</label>
        <label for="chain-view-sankey">价值流</label>
        <label for="chain-view-heatmap">瓶颈热力</label>
      </div>
      <div class="chain-view-panels">
        <section class="chain-view-panel chain-lane-map">{stage_panels}</section>
        <section class="chain-view-panel chain-sankey-map">{value_flow}</section>
        <section class="chain-view-panel chain-chokepoint-heatmap">{heatmap}</section>
      </div>
    </div>
""".strip()


def _render_chain_sankey_flow(flows: list[dict[str, Any]]) -> str:
    if not isinstance(flows, list) or not flows:
        flow_cards = '<p class="muted">价值流仍待补充：需要把需求、订单、供给、交付、收入和利润流向连成可验证路径。</p>'
    else:
        flow_cards = "\n".join(_chain_value_flow_card(flow) for flow in flows if isinstance(flow, dict))
    return f"""
    <div class="chain-map-card">
      <div class="chain-graph-head">
        <p class="chain-graph-title">订单和价值如何在链条里流动</p>
        <p class="muted">按“需求预算 -> 关键供给 -> 系统交付 -> 收入/ROI 验证”阅读。</p>
      </div>
      <div class="chain-value-guide">
        <div><b>先看谁付钱</b><span>下游 capex、订单、规格。</span></div>
        <div><b>再看谁卡住供给</b><span>关键硬件、工程交付和资格认证。</span></div>
        <div><b>最后看钱留在哪</b><span>收入、毛利、backlog、现金流和估值上修。</span></div>
      </div>
      <div class="chain-sankey-list">{flow_cards}</div>
    </div>
""".strip()


def _chain_value_flow_card(flow: dict[str, Any]) -> str:
    kind = _slug(str(flow.get("kind") or flow.get("type") or "supply"))
    weight = flow.get("weight") or flow.get("score") or 3
    try:
        weight_text = str(max(1, min(5, int(float(weight)))))
    except (TypeError, ValueError):
        weight_text = "3"
    return f"""
        <article class="chain-sankey-flow flow-{kind}" style="--flow-weight:{weight_text}">
          <div class="flow-step"><span>{_e(str(flow.get("step") or ""))}</span><b>{_e(str(flow.get("title") or "价值流"))}</b></div>
          <div class="flow-route">
            <div class="flow-from"><small>发起方</small>{_e(str(flow.get("from") or flow.get("source") or ""))}</div>
            <div class="flow-band"><span>{_e(str(flow.get("what") or flow.get("relationship") or flow.get("label") or ""))}</span></div>
            <div class="flow-to"><small>接收方</small>{_e(str(flow.get("to") or flow.get("target") or ""))}</div>
          </div>
          <div class="flow-fields">
            <div><b>可能受益</b><p>{_e(str(flow.get("beneficiaries") or flow.get("targets") or ""))}</p></div>
            <div><b>财务验证</b><p>{_e(str(flow.get("metric") or flow.get("financial_metrics") or ""))}</p></div>
            <div><b>投资含义</b><p>{_e(str(flow.get("investment_read") or flow.get("judgment") or ""))}</p></div>
          </div>
        </article>
""".rstrip()


def _render_chain_chokepoint_heatmap(items: list[dict[str, Any]]) -> str:
    dimensions = ["稀缺性", "替代难度", "定价权", "财务弹性", "估值风险", "反证风险"]
    if not isinstance(items, list) or not items:
        rows = '<tr><td colspan="10">瓶颈热力图仍待补充：需要按稀缺性、替代难度、定价权、财务弹性、估值风险和反证风险打分。</td></tr>'
    else:
        rows = "\n".join(_chain_chokepoint_heatmap_row(item, dimensions) for item in items if isinstance(item, dict))
    return f"""
    <div class="chain-map-card">
      <div class="chain-graph-head">
        <p class="chain-graph-title">瓶颈热力图</p>
        <p class="muted">1-5 分。高分仍需经过 Q4 的未定价和风险控制闸门。</p>
      </div>
      <div class="table-scroll">
        <table>
          <thead><tr><th>节点</th><th>控制者</th>{''.join(f'<th>{_e(dimension)}</th>' for dimension in dimensions)}<th>当前判断</th><th>QA</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>
""".strip()


def _chain_chokepoint_heatmap_row(item: dict[str, Any], dimensions: list[str]) -> str:
    scores = item.get("scores") if isinstance(item.get("scores"), dict) else item
    score_cells = "".join(_heat_score_cell(scores.get(dimension)) for dimension in dimensions)
    return f"""
        <tr>
          <td><strong>{_e(str(item.get("node") or item.get("name") or ""))}</strong><br><span>{_e(str(item.get("role") or item.get("node_type") or ""))}</span></td>
          <td>{_e(str(item.get("controllers") or item.get("players") or ""))}</td>
          {score_cells}
          <td>{_e(str(item.get("conclusion") or item.get("judgment") or ""))}</td>
          <td>{_e(str(item.get("qa_link") or item.get("qa") or ""))}</td>
        </tr>
""".rstrip()


def _heat_score_cell(value: Any) -> str:
    try:
        score = int(float(value))
    except (TypeError, ValueError):
        score = 0
    klass = "heat-high" if score >= 4 else "heat-mid" if score >= 3 else "heat-low"
    text = str(score) if score else "-"
    return f'<td class="heat-score {klass}"><span>{text}</span></td>'


def _render_chain_stage_panels(
    stage_groups: list[dict[str, Any]],
    layers: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
) -> str:
    groups = stage_groups if stage_groups else _fallback_stage_groups(layers, relationships)
    panels = "\n".join(_chain_stage_panel(group) for group in groups if isinstance(group, dict))
    return f"""
    <div class="chain-relationship-graph">
      <div class="chain-graph-head">
        <p class="chain-graph-title">按上游 / 中游 / 下游展开公司关系</p>
        <p class="muted">每家公司固定看：需求输入、供给输入、自己生产、提供给谁、财务验证指标和瓶颈强度。</p>
      </div>
      <div class="chain-layer-grid">{panels}</div>
    </div>
""".strip()


def _render_chain_company_network(
    stage_groups: list[dict[str, Any]],
    layers: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
    network: dict[str, Any],
) -> str:
    groups = stage_groups if stage_groups else _fallback_stage_groups(layers, relationships)
    explicit_edges = network.get("edges") if isinstance(network.get("edges"), list) else []
    edge_source = explicit_edges or relationships
    stage_columns = "\n".join(_chain_network_stage_column(group) for group in groups if isinstance(group, dict))
    edge_cards = "\n".join(_chain_network_edge_card(edge) for edge in edge_source if isinstance(edge, dict))
    if not edge_cards:
        edge_cards = '<p class="muted">关系边仍待补充：需要明确需求、供给、交付和验证如何在公司之间传导。</p>'
    return f"""
    <div class="chain-company-network">
      <div class="chain-graph-head">
        <p class="chain-graph-title">公司关系总图</p>
        <p class="muted">先把所有公司放在一张图里，再用箭头标明需求、供给、交付和验证关系。</p>
      </div>
      <div class="chain-network-canvas">
        <div class="chain-network-stage-grid">{stage_columns}</div>
        <div class="chain-network-edge-list">{edge_cards}</div>
      </div>
    </div>
""".strip()


def _chain_network_stage_column(group: dict[str, Any]) -> str:
    companies = group.get("companies") if isinstance(group.get("companies"), list) else []
    nodes = "\n".join(
        f"""
          <span class="chain-network-node">
            <b>{_e(str(company.get("name", "")))}</b>
            <small>{_e(str(company.get("ticker", "")))}</small>
          </span>
""".rstrip()
        for company in companies
        if isinstance(company, dict)
    )
    return f"""
        <div class="chain-network-stage">
          <strong>{_e(str(group.get("stage", "")))}</strong>
          <p>{_e(str(group.get("summary", "")))}</p>
          <div>{nodes}</div>
        </div>
""".rstrip()


def _chain_network_edge_card(edge: dict[str, Any]) -> str:
    source = str(edge.get("from") or edge.get("source") or "")
    target = str(edge.get("to") or edge.get("target") or "")
    label = str(edge.get("label") or edge.get("relationship") or edge.get("type") or "")
    flow = str(edge.get("flow") or edge.get("type") or "")
    return f"""
          <div class="chain-network-edge-card">
            <span>{_e(source)}</span>
            <b>→</b>
            <span>{_e(target)}</span>
            <small>{_e(label)}{(" / " + _e(flow)) if flow else ""}</small>
          </div>
""".rstrip()


def _fallback_stage_groups(
    layers: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if relationships:
        by_stage: dict[str, list[dict[str, str]]] = {"上游": [], "中游": [], "下游": []}
        for item in relationships:
            stage = str(item.get("stage") or item.get("layer") or "中游")
            if stage not in by_stage:
                stage = "中游"
            by_stage[stage].append(
                {
                    "name": str(item.get("to") or item.get("target") or "待定义节点"),
                    "ticker": "",
                    "node_type": str(item.get("node_type") or item.get("relationship") or "待补充。"),
                    "demand_input": str(item.get("demand_input") or item.get("receiver_accepts") or item.get("flow") or item.get("value_flow") or "待补充。"),
                    "supply_input": str(item.get("supply_input") or "待补充。"),
                    "produces": str(item.get("produces") or item.get("receiver_provides") or item.get("relationship") or "待补充。"),
                    "provides_to": str(item.get("provides_to") or item.get("target_map") or item.get("target_links") or "待补充。"),
                    "financial_metrics": str(item.get("financial_metrics") or "待补充。"),
                    "bottleneck_strength": str(item.get("bottleneck_strength") or item.get("bottleneck") or "待补充。"),
                    "qa_link": str(item.get("qa_link") or item.get("target_map") or "待补充。"),
                    "evidence": str(item.get("evidence") or "待补充。"),
                }
            )
        return [{"stage": stage, "summary": "从关系边自动归并。", "companies": companies} for stage, companies in by_stage.items() if companies]
    if layers:
        return [
            {
                "stage": str(layer.get("stage") or layer.get("layer") or "待定义"),
                "summary": str(layer.get("value_flow") or layer.get("judgment") or "待补充。"),
                "companies": [
                    {
                        "name": str(layer.get("players") or "待定义玩家"),
                        "ticker": "",
                        "node_type": str(layer.get("node_type") or layer.get("node") or layer.get("products") or "待补充。"),
                        "demand_input": str(layer.get("demand_input") or layer.get("demand") or layer.get("accepts_from") or layer.get("inputs") or "待补充。"),
                        "supply_input": str(layer.get("supply_input") or layer.get("supply") or "待补充。"),
                        "produces": str(layer.get("produces") or layer.get("products") or "待补充。"),
                        "provides_to": str(layer.get("provides_to") or layer.get("outputs") or "待补充。"),
                        "financial_metrics": str(layer.get("financial_metrics") or layer.get("metrics") or "待补充。"),
                        "bottleneck_strength": str(layer.get("bottleneck_strength") or layer.get("value_flow") or layer.get("judgment") or "待补充。"),
                        "qa_link": str(layer.get("qa_link") or layer.get("qa") or "待补充。"),
                        "evidence": str(layer.get("evidence") or "待补充。"),
                    }
                ],
            }
            for layer in layers
        ]
    return [
        {"stage": "上游", "summary": "等待领域 playbook 补充上游公司。", "companies": []},
        {"stage": "中游", "summary": "等待领域 playbook 补充中游公司。", "companies": []},
        {"stage": "下游", "summary": "等待领域 playbook 补充下游公司。", "companies": []},
    ]


def _chain_stage_panel(group: dict[str, Any]) -> str:
    companies = group.get("companies") if isinstance(group.get("companies"), list) else []
    company_cards = "\n".join(_chain_company_card(company) for company in companies if isinstance(company, dict))
    return f"""
    <details class="chain-layer-card chain-stage-panel">
      <summary>
        <span class="chain-stage-name">{_e(str(group.get("stage", "")))}</span>
        <span>{_e(str(group.get("summary", "")))}</span>
        <small>{len(companies)} 个公司/节点</small>
        <span class="chevron">›</span>
      </summary>
      <div class="chain-company-list">{company_cards}</div>
    </details>
""".rstrip()


def _chain_company_card(company: dict[str, Any]) -> str:
    return f"""
        <article class="chain-relation-card chain-company-card">
          <div class="chain-company-head">
            <div><b>{_e(str(company.get("name", "")))}</b><span>{_e(str(company.get("ticker", "")))}</span></div>
            <small>{_e(str(company.get("evidence", "")))}</small>
          </div>
          <dl class="chain-relation-meta">
            <div><dt>节点类型</dt><dd>{_e(str(company.get("node_type", "")))}</dd></div>
            <div><dt>需求输入</dt><dd>{_e(str(company.get("demand_input") or company.get("accepts_from", "")))}</dd></div>
            <div><dt>供给输入</dt><dd>{_e(str(company.get("supply_input", "")))}</dd></div>
            <div><dt>自己生产</dt><dd>{_e(str(company.get("produces", "")))}</dd></div>
            <div><dt>提供给谁</dt><dd>{_e(str(company.get("provides_to", "")))}</dd></div>
            <div><dt>财务指标</dt><dd>{_e(str(company.get("financial_metrics", "")))}</dd></div>
            <div><dt>瓶颈强度</dt><dd>{_e(str(company.get("bottleneck_strength") or company.get("bottleneck", "")))}</dd></div>
            <div><dt>对应 QA</dt><dd>{_e(str(company.get("qa_link", "")))}</dd></div>
          </dl>
        </article>
""".rstrip()


def _render_chain_relationship_graph(relationships: list[dict[str, Any]]) -> str:
    if not relationships:
        return """
    <div class="chain-relationship-graph">
      <p class="chain-graph-title">公司关系图</p>
      <p class="muted">当前产业链关系仍待补充：需要明确上游供应、平台依赖、客户订单、价值流和标的映射。</p>
    </div>
""".strip()
    cards = "\n".join(_chain_relationship_card(item) for item in relationships if isinstance(item, dict))
    return f"""
    <div class="chain-relationship-graph">
      <div class="chain-graph-head">
        <p class="chain-graph-title">公司关系图</p>
        <p class="muted">阅读方式：左侧公司或节点提供产品/能力，右侧公司或节点承接需求；每条边说明钱、订单或瓶颈如何传导。</p>
      </div>
      <div class="chain-relationship-grid">{cards}</div>
    </div>
""".strip()


def _chain_relationship_card(item: dict[str, Any]) -> str:
    source = str(item.get("from") or item.get("source") or "")
    target = str(item.get("to") or item.get("target") or "")
    relation = str(item.get("relationship") or item.get("relation") or "")
    demand_input = str(item.get("demand_input") or item.get("receiver_accepts") or item.get("flow") or item.get("value_flow") or "")
    supply_input = str(item.get("supply_input") or "")
    produces = str(item.get("produces") or item.get("receiver_provides") or item.get("relationship") or "")
    provides_to = str(item.get("provides_to") or item.get("target_map") or item.get("target_links") or "")
    financial_metrics = str(item.get("financial_metrics") or "")
    bottleneck = str(item.get("bottleneck_strength") or item.get("bottleneck") or "")
    qa_link = str(item.get("qa_link") or item.get("target_map") or item.get("target_links") or "")
    evidence = str(item.get("evidence") or "")
    return f"""
        <article class="chain-relation-card">
          <div class="chain-relation-line">
            <span class="chain-company">{_e(source)}</span>
            <span class="chain-arrow">→</span>
            <span class="chain-company">{_e(target)}</span>
          </div>
          <p class="chain-relation-type">{_e(relation)}</p>
          <dl class="chain-relation-meta">
            <div><dt>需求输入</dt><dd>{_e(demand_input)}</dd></div>
            <div><dt>供给输入</dt><dd>{_e(supply_input)}</dd></div>
            <div><dt>自己生产</dt><dd>{_e(produces)}</dd></div>
            <div><dt>提供给谁</dt><dd>{_e(provides_to)}</dd></div>
            <div><dt>财务指标</dt><dd>{_e(financial_metrics)}</dd></div>
            <div><dt>瓶颈强度</dt><dd>{_e(bottleneck)}</dd></div>
            <div><dt>对应 QA</dt><dd>{_e(qa_link)}</dd></div>
            <div><dt>证据</dt><dd>{_e(evidence)}</dd></div>
          </dl>
        </article>
""".rstrip()
