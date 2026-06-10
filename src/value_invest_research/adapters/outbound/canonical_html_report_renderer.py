from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from value_invest_research.domain.report_view_model import ReportViewModel


class CanonicalHtmlReportRenderer:
    """HTML adapter for the locked research-goal report presentation contract."""

    def render(self, view_model: ReportViewModel) -> str:
        data = view_model.to_dict()
        source_url_by_id = _source_url_lookup(data.get("sources", []))
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
                _render_industry_overview(data["supply_chain"], source_url_by_id),
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


def _source_url_lookup(sources: list[dict[str, Any]]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for source in sources:
        if not isinstance(source, dict):
            continue
        source_id = str(source.get("source_id") or source.get("id") or "")
        url = str(source.get("url") or "")
        if source_id and url:
            lookup[source_id] = url
    return lookup


def _render_source_chip(source_id: str, source_url_by_id: dict[str, str]) -> str:
    url = source_url_by_id.get(str(source_id), "")
    if url:
        return f'<a class="source-chip" href="{_e(url)}" target="_blank" rel="noopener">{_e(str(source_id))}</a>'
    return f'<span class="source-chip">{_e(str(source_id))}</span>'


def _render_hero(data: dict[str, Any]) -> str:
    project = data["project"]
    title = project.get("title") or data["goal"].get("topic") or "专业投研报告"
    report_date = project.get("report_date") or ""
    run_mode = project.get("run_mode") or ""
    return f"""
<header class="hero">
  <nav class="top-nav" aria-label="报告导航">
    <a href="#goal">当前研究的问题</a>
    <a href="#overview">行业概况</a>
    <a href="#qa">下钻 QA</a>
    <a href="#targets">标的推荐</a>
    <a href="#sources">来源索引</a>
  </nav>
  <div class="hero-inner">
    <p class="eyebrow">Research Goal QA</p>
    <h1>{_e(str(title))}</h1>
    <p class="hero-subtitle">先建立行业概况，再由行业地图生成下钻 QA，最后汇总到标的赔率和观察清单。</p>
    <div class="hero-meta">
      <span>{_e(str(report_date))}</span>
      <span>{_e(str(run_mode))}</span>
    </div>
  </div>
</header>
""".strip()


def _render_goal(data: dict[str, Any]) -> str:
    goal = data["goal"]
    constraint = _render_constraint_definition(goal.get("constraint_definition") or goal.get("key_constraint") or {})
    return f"""
<main>
<section id="goal" class="section goal-section">
  <div class="section-heading">
    <span class="section-kicker">01</span>
    <h2>当前研究的问题</h2>
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
    {constraint}
  </div>
</section>
""".strip()


def _render_constraint_definition(item: dict[str, Any]) -> str:
    if not isinstance(item, dict) or not item:
        item = {
            "theme": "先把研究主题翻译成精确定义的约束，再判断哪些公司能把约束转成财务价值。",
            "precise_constraint": "待补充：核心瓶颈、边界、替代路线和验证周期。",
            "why_now": "待补充：为什么现在进入投资观察窗口。",
            "scope": "待补充：研究范围和不纳入范围。",
            "route_conflict": "待补充：关键技术路线、商业路线或竞争路线冲突。",
            "adoption_horizon": "待补充：验证周期和降级节奏。",
        }
    rows = [
        ("主题边界", item.get("theme", "")),
        ("精确定义", item.get("precise_constraint") or item.get("preciseConstraint") or item.get("constraint", "")),
        ("为什么现在", item.get("why_now") or item.get("whyNow") or ""),
        ("研究范围", item.get("scope", "")),
        ("路线冲突", item.get("route_conflict") or item.get("routeConflict") or ""),
        ("验证周期", item.get("adoption_horizon") or item.get("adoptionHorizon") or ""),
    ]
    cards = "\n".join(
        f"<article><span>{_e(label)}</span><p>{_e(str(value))}</p></article>" for label, value in rows
    )
    return f"""
    <div class="constraint-definition">
      <p class="artifact-title">关键约束定义</p>
      <div class="constraint-grid">{cards}</div>
    </div>
""".strip()


def _render_industry_overview(chain: dict[str, Any], source_url_by_id: dict[str, str]) -> str:
    layers = chain.get("layers") or []
    relationships = chain.get("relationships") or []
    stage_groups = chain.get("stage_groups") or chain.get("stageGroups") or []
    research_bridge = _render_chain_research_bridge(
        chain.get("research_bridge") or chain.get("supply_chain_research_bridge") or {},
        chain.get("node_lenses") or chain.get("supply_chain_node_lenses") or [],
    )
    data_gaps = _render_chain_data_gaps(chain.get("data_gaps") or chain.get("supply_chain_data_gaps") or [])
    lane_map = _render_chain_lane_map(stage_groups, layers, relationships)
    value_flow = _render_chain_value_flow(chain, relationships)
    industry_space = _render_industry_space(chain, source_url_by_id)
    industry_competition = _render_industry_competition(chain, source_url_by_id)
    industry_chokepoints = _render_industry_chokepoints(chain)
    industry_key_variables = _render_industry_key_variables(chain, data_gaps)
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
      {_render_chain_detail_panel("BOM / 组件级链条", "把系统拆成子系统、组件、关键公司、输入输出和财务验证指标。", _render_component_value_chain(chain.get("component_value_chain") or chain.get("componentValueChain") or []), "chain-component-panel")}
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
        rows = grouped.get(category["key"], [])
        if rows:
            rendered_rows = []
            for row in rows:
                source_ids = row.get("source_ids") or []
                source_chips = "".join(_render_source_chip(str(source_id), source_url_by_id) for source_id in source_ids)
                if not source_chips:
                    source_chips = '<span class="source-chip source-chip-missing">待补来源</span>'
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
            body = "".join(rendered_rows)
            count = f"{len(rows)} 条"
        else:
            body, count = _render_public_method_gap(category, normalized_plan.get(category["key"]) or normalized_plan.get(category["label"]))
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
    profit_pool = competition.get("profit_pool_flow") if isinstance(competition.get("profit_pool_flow"), dict) else {}

    if isinstance(node_cards, list) and node_cards:
        cards_html = "".join(_render_competition_node_card(node, i, source_url_by_id) for i, node in enumerate(node_cards))
    else:
        cards_html = ""

    profit_html = ""
    if profit_pool:
        profit_html = _render_profit_pool_flow(profit_pool)

    return f"""
  <details class="industry-module industry-competition">
    <summary class="module-head"><span class="module-index">03</span><div><h3>竞争格局与利润池</h3><p>每个链节点的竞争烈度、主导方、护城河来源和利润流向。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
    {_render_technology_route_matrix(chain.get("technology_route_matrix") or chain.get("technologyRouteMatrix") or [])}
    {profit_html}
    {cards_html if cards_html else _render_competition_fallback_table(chain.get("competition_rows") or chain.get("competitionLandscape") or [])}
    </div>
  </details>
""".strip()


def _render_competition_node_card(node: dict[str, Any], index: int, source_url_by_id: dict[str, str]) -> str:
    node_name = str(node.get("node") or "")
    dominant = str(node.get("dominant_player") or "")
    share = str(node.get("market_share") or "")
    intensity = str(node.get("competitive_intensity") or "待补")
    moat = str(node.get("moat_source") or "")
    profit_dest = str(node.get("profit_destination") or "")
    challengers = str(node.get("challengers") or "")
    dynamics = str(node.get("key_dynamics") or "")
    source_ids = node.get("sourceIds") or node.get("source_ids") or []
    if not isinstance(source_ids, list):
        source_ids = [source_ids] if source_ids else []
    source_chips = "".join(_render_source_chip(str(sid), source_url_by_id) for sid in source_ids)
    intensity_class = {"低": "competition-low", "中低": "competition-midlow", "中": "competition-mid", "中高": "competition-high", "高": "competition-high", "极低": "competition-low"}
    ic = intensity_class.get(intensity, "competition-mid")
    return f"""
        <details class="competition-node-card" open>
          <summary>
            <span class="competition-node-index">{index + 1:02d}</span>
            <strong>{_e(node_name)}</strong>
            <span class="competition-intensity {ic}">竞争烈度：{_e(intensity)}</span>
            <span class="chevron">›</span>
          </summary>
          <div class="competition-node-body">
            <section class="competition-subcard">
              <h4>主要玩家与利润分布</h4>
              <div class="competition-subcard-grid">
                <div class="competition-subcard-item"><span>主导方</span><strong>{_e(dominant)}</strong><small>份额 {_e(share)}</small></div>
                <div class="competition-subcard-item"><span>挑战者</span><p>{_e(challengers)}</p></div>
                <div class="competition-subcard-item col-span"><span>利润流向</span><p>{_e(profit_dest)}</p></div>
              </div>
            </section>
            <section class="competition-subcard">
              <h4>领头羊的护城河</h4>
              <p>{_e(moat)}</p>
            </section>
            <section class="competition-subcard">
              <h4>当前烈度与未来变化</h4>
              <p>{_e(dynamics)}</p>
            </section>
            <div class="space-node-sources">{source_chips}</div>
          </div>
        </details>""".strip()


def _render_competition_fallback_table(rows: list[Any]) -> str:
    if not isinstance(rows, list) or not rows:
        rows = [["核心节点", "竞争者和替代路线待补", "是否形成 chokepoint 待验证", "利润池归属待验证", "供给扩张/客户议价", "进入 Q2 下钻"]]
    body = "\n".join("<tr>" + "".join(f"<td>{_e(str(cell))}</td>" for cell in _row_cells(row, 6)) + "</tr>" for row in rows)
    return f'<div class="table-scroll"><table><thead><tr><th>节点</th><th>竞争格局</th><th>Chokepoint 初判</th><th>利润池/标的含义</th><th>主要反证</th><th>后续 QA</th></tr></thead><tbody>{body}</tbody></table></div>'


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


def _render_industry_chokepoints(chain: dict[str, Any]) -> str:
    text = chain.get("chokepoints") or chain.get("bottlenecks") or "瓶颈点待 Q2 竞争格局验证。"
    return f"""
  <details class="industry-module industry-chokepoints">
    <summary class="module-head"><span class="module-index">04</span><div><h3>瓶颈点</h3><p>瓶颈点是竞争格局和价值捕获分析后的结果，后续需要进入 Q3/Q4 验证估值和反证。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
    <div class="chain-chokepoints">{_e(str(text))}</div>
    {_render_bottleneck_release_timeline(chain.get("bottleneck_release_timeline") or chain.get("bottleneckReleaseTimeline") or [])}
    </div>
  </details>
""".strip()


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


def _render_technology_route_matrix(items: list[Any]) -> str:
    if not isinstance(items, list) or not items:
        rows = [
            ["待补充", "适用场景", "解决的约束", "代价/限制", "验证节奏", "主要受益", "反证"],
        ]
    else:
        rows = [
            [
                item.get("route", ""),
                item.get("best_fit") or item.get("bestFit") or "",
                item.get("solves", ""),
                item.get("tradeoff", ""),
                item.get("timing", ""),
                item.get("beneficiaries", ""),
                item.get("refute", ""),
            ]
            if isinstance(item, dict)
            else _row_cells(item, 7)
            for item in items
        ]
    body = "\n".join("<tr>" + "".join(f"<td>{_e(str(cell))}</td>" for cell in row) + "</tr>" for row in rows)
    return f"""
    <div class="technology-route-matrix">
      <div class="chain-graph-head"><b>技术路线比较矩阵</b><span>先比较路线，再判断利润池和替代风险。</span></div>
      <div class="table-scroll"><table>
        <thead><tr><th>路线</th><th>最适用场景</th><th>解决什么约束</th><th>代价/限制</th><th>验证节奏</th><th>主要受益</th><th>反证</th></tr></thead>
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
    return f"""
  <details class="industry-module industry-key-variables">
    <summary class="module-head"><span class="module-index">05</span><div><h3>关键变量与待验证数据</h3><p>把行业概况转成下钻 QA：哪些数据变化会强化、削弱或推翻当前排序。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
    <div class="key-variable-grid">
      {data_gaps}
      <div class="qa-generation-table table-scroll"><table><thead><tr><th>QA 方向</th><th>来自行业概况的信号</th><th>怎么使用</th></tr></thead><tbody>{rows}</tbody></table></div>
    </div>
    </div>
  </details>
""".strip()


def _row_cells(row: Any, max_cells: int) -> list[Any]:
    if isinstance(row, dict):
        return list(row.values())[:max_cells]
    if isinstance(row, list):
        return row[:max_cells]
    return [row]


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
    <h2>标的推荐</h2>
  </div>
  <p class="section-note">该表是研究观察清单，不是买卖指令；排序同时考虑瓶颈强度、未来空间、估值赔率和反证可控性。</p>
  {_render_target_profit_bridge(targets)}
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


def _render_target_profit_bridge(targets: list[dict[str, Any]]) -> str:
    rows = "\n".join(_target_profit_bridge_row(target) for target in targets)
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


def _target_profit_bridge_row(target: dict[str, Any]) -> str:
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


def _class_token(value: str) -> str:
    token = value.strip().lower().replace(" ", "_")
    return token or "no_action"


def _slug(value: str) -> str:
    token = "".join(ch if ch.isalnum() else "-" for ch in value.strip().lower()).strip("-")
    return token or "item"


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
.constraint-definition {
  grid-column: 1 / -1;
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 18px;
  background: linear-gradient(180deg, #ffffff, #fbfdff);
  padding: 16px;
}
.constraint-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}
.constraint-grid article {
  border: 1px solid #e5edf7;
  border-radius: 16px;
  background: #f8fbff;
  padding: 14px;
}
.constraint-grid span {
  display: block;
  color: var(--blue);
  font-size: 12px;
  font-weight: 900;
  margin-bottom: 6px;
}
.constraint-grid p {
  margin: 0;
  color: #435064;
  font-size: 13px;
}
.goal-main { font-size: 22px; font-weight: 700; }
.industry-overview-section {
  display: grid;
  gap: 14px;
}
.industry-module {
  border: 1px solid var(--line);
  border-radius: 22px;
  background: var(--surface);
  box-shadow: var(--shadow);
  overflow: hidden;
}
.industry-module > summary {
  list-style: none;
  cursor: pointer;
}
.industry-module > summary::-webkit-details-marker {
  display: none;
}
.industry-module[open] > summary {
  border-bottom: 1px solid var(--line);
}
.industry-module-body {
  padding: 22px;
  min-width: 0;
  max-width: 100%;
}
.module-head {
  display: grid;
  grid-template-columns: auto 1fr auto;
  column-gap: 12px;
  row-gap: 3px;
  align-items: center;
  margin: 0;
  padding: 18px 22px;
}
.module-head .module-index {
  display: inline-flex;
  width: 34px;
  height: 34px;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: #eaf3ff;
  color: var(--blue);
  font-size: 12px;
  font-weight: 900;
}
.module-head .chevron {
  color: var(--muted);
  font-size: 18px;
  font-weight: 900;
  transition: transform .18s ease;
}
.industry-module[open] > .module-head .chevron {
  transform: rotate(90deg);
}
.module-head h3 {
  margin: 0;
  font-size: 21px;
}
.module-head p {
  margin: 0;
  color: var(--muted);
  font-size: 14px;
}
.overview-subtitle {
  color: #334155;
  font-size: 13px;
  font-weight: 900;
}
.chain-explain { padding: 22px; }
.chain-plain-summary { margin-top: 0; font-size: 18px; color: #344054; }
.chain-research-bridge, .chain-data-gaps {
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 18px;
  background: linear-gradient(180deg, #ffffff, #fbfdff);
  padding: 16px;
  margin: 18px 0;
}
.chain-bridge-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
.chain-bridge-card {
  border: 1px solid #e5edf7;
  border-radius: 16px;
  background: #f8fbff;
  padding: 14px;
}
.chain-bridge-card span {
  display: block;
  color: var(--muted);
  font-size: 12px;
  font-weight: 800;
  margin-bottom: 6px;
}
.chain-bridge-card strong {
  display: block;
  color: #223047;
  line-height: 1.55;
}
.chain-research-bridge > p {
  margin: 12px 0;
  color: #435064;
  line-height: 1.75;
}
.chain-node-lens {
  border: 1px solid #e7edf6;
  border-radius: 16px;
  background: #fff;
  padding: 14px;
  margin: 14px 0;
}
.chain-node-lens > b {
  display: block;
  color: #27364a;
  margin-bottom: 10px;
}
.chain-node-lens ul {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin: 0;
  padding: 0;
  list-style: none;
}
.chain-node-lens li {
  border: 1px solid #edf1f7;
  border-radius: 14px;
  background: #fbfcff;
  padding: 12px;
}
.chain-node-lens li b {
  display: block;
  color: var(--blue);
  font-size: 12px;
  margin-bottom: 4px;
}
.chain-node-lens li span {
  display: block;
  color: #526071;
  font-size: 12px;
  line-height: 1.55;
}
.chain-data-gaps summary {
  cursor: pointer;
  font-weight: 900;
  color: #344054;
}
.chain-data-gaps ul {
  margin: 10px 0 0;
  padding-left: 20px;
  color: #526071;
  line-height: 1.75;
}
.chain-detail-panel,
.space-detail-panel {
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 18px;
  background: #fbfcff;
  margin: 14px 0;
  overflow: hidden;
}
.chain-detail-panel > summary,
.space-detail-panel > summary {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 10px;
  align-items: center;
  list-style: none;
  cursor: pointer;
  padding: 14px 16px;
}
.chain-detail-panel > summary::-webkit-details-marker,
.space-detail-panel > summary::-webkit-details-marker {
  display: none;
}
.chain-detail-panel > summary span:first-child,
.space-detail-panel > summary span:first-child {
  color: #27364a;
  font-weight: 900;
}
.chain-detail-panel > summary small,
.space-detail-panel > summary small {
  color: var(--muted);
  font-size: 12px;
  line-height: 1.45;
}
.chain-detail-panel[open] > summary,
.space-detail-panel[open] > summary {
  border-bottom: 1px solid var(--line);
}
.chain-detail-body,
.space-detail-body {
  padding: 16px;
  min-width: 0;
  max-width: 100%;
}
.industry-space-summary {
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 18px;
  background: linear-gradient(180deg, #ffffff, #fbfdff);
  padding: 16px;
  margin-bottom: 14px;
}
.industry-space-summary > p {
  margin: 0 0 12px;
  color: #344054;
  font-weight: 760;
  line-height: 1.75;
}
.space-bom-reasoning {
  display: grid;
  gap: 12px;
}
.space-node-card {
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 16px;
  background: #fbfcff;
  overflow: hidden;
}
.space-node-card > summary {
  display: grid;
  grid-template-columns: auto minmax(160px, .45fr) minmax(240px, 1fr) auto;
  gap: 10px;
  align-items: center;
  list-style: none;
  cursor: pointer;
  padding: 14px 16px;
}
.space-node-card > summary::-webkit-details-marker {
  display: none;
}
.space-node-card[open] > summary {
  border-bottom: 1px solid var(--line);
}
.space-node-label {
  display: inline-flex;
  border-radius: 999px;
  background: #eef5ff;
  color: var(--blue);
  border: 1px solid #d8e8ff;
  font-size: 11px;
  font-weight: 900;
  padding: 3px 8px;
}
.space-node-card summary strong {
  color: #27364a;
  font-size: 14px;
}
.space-node-card summary small {
  color: #667085;
  font-size: 12px;
  line-height: 1.45;
}
.space-node-reasoning {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  padding: 14px;
}
.space-node-section {
  border: 1px solid #e2e9f3;
  border-radius: 14px;
  background: #fff;
  padding: 12px;
}
.space-node-space-reasoning {
  border-color: #d9e8fb;
  background: #fbfdff;
}
.space-node-evidence {
  background: #fbfcff;
}
.space-node-section h4 {
  margin: 0 0 8px;
  color: #27364a;
  font-size: 13px;
}
.space-node-section p,
.space-node-section li {
  color: #526071;
  font-size: 12px;
  line-height: 1.65;
}
.space-node-section ul,
.space-node-section ol {
  margin: 0;
  padding-left: 18px;
}
.space-node-sources {
  margin-top: 10px;
}
.space-node-sizing {
  margin-top: 12px;
  border: 1px solid #d9e8fb;
  border-radius: 12px;
  background: linear-gradient(180deg, #f8fbff, #fff);
  padding: 12px;
}
.space-method-step {
  display: grid;
  gap: 8px;
  margin-bottom: 10px;
}
.space-step-title {
  display: flex;
  align-items: center;
  gap: 8px;
}
.space-step-title h5 {
  margin: 0;
  color: var(--blue);
  font-size: 12px;
}
.space-step-index {
  display: inline-flex;
  width: 22px;
  height: 22px;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: var(--blue);
  color: #fff;
  font-style: normal;
  font-size: 11px;
  font-weight: 900;
  flex: 0 0 auto;
}
.space-public-methods {
  margin-bottom: 0;
}
.space-method-card-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
}
.space-method-card {
  border: 1px solid #e1e9f4;
  border-radius: 12px;
  background: #fff;
  display: grid;
  grid-template-columns: minmax(128px, 168px) 1fr;
  gap: 12px;
  padding: 10px;
  min-width: 0;
}
.space-method-card header {
  border-right: 1px solid #edf1f7;
  display: grid;
  align-content: start;
  gap: 7px;
  padding-right: 10px;
}
.space-method-card header span {
  color: #27364a;
  font-size: 12px;
  font-weight: 900;
}
.space-method-card header small {
  width: max-content;
  color: var(--blue);
  background: #eef5ff;
  border: 1px solid #d8e8ff;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 900;
  padding: 2px 7px;
  white-space: nowrap;
}
.space-method-card-body {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 8px;
  min-width: 0;
}
.space-method-entry {
  border: 1px solid #edf1f7;
  border-radius: 10px;
  background: #fbfdff;
  padding: 9px;
  margin: 0;
}
.space-method-entry b {
  display: block;
  color: #1f2937;
  font-size: 12px;
  margin-bottom: 5px;
}
.space-method-entry p {
  margin: 0 0 8px;
  color: #344054;
  font-size: 12px;
  line-height: 1.55;
}
.space-method-entry p strong {
  color: var(--blue);
  font-size: 11px;
  font-weight: 900;
}
.space-method-entry dl {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 5px 10px;
  margin: 0;
}
.space-method-entry dl div {
  display: grid;
  grid-template-columns: 64px 1fr;
  gap: 6px;
}
.space-method-entry dt {
  color: var(--blue);
  font-size: 11px;
  font-weight: 900;
}
.space-method-entry dd {
  margin: 0;
  color: #526071;
  font-size: 11px;
  line-height: 1.45;
}
.space-method-entry-sources {
  margin-top: 8px;
}
.space-method-entry-sources .source-chips {
  gap: 5px;
}
.source-chip-missing {
  color: #956100;
  background: #fff7e6;
  border-color: #f4d28f;
}
.space-method-empty {
  align-self: center;
  margin: 0;
  color: var(--muted);
  font-size: 12px;
  line-height: 1.6;
}
.space-method-gap {
  border: 1px dashed #d8e3f2;
  border-radius: 10px;
  background: #fbfcff;
  padding: 9px;
  color: #5d6675;
}
.space-horizon-conclusion {
  display: grid;
  gap: 8px;
  margin-bottom: 10px;
}
.space-horizon-summary {
  border: 1px solid #e5edf7;
  border-radius: 10px;
  background: #fff;
  padding: 10px;
  margin: 0;
  color: #344054;
  font-size: 12px;
  line-height: 1.65;
}
.space-horizon-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
}
.space-horizon-card {
  border: 1px solid #e5edf7;
  border-radius: 10px;
  background: #fff;
  padding: 10px;
}
.space-horizon-card span {
  display: block;
  color: #667085;
  font-size: 11px;
  font-weight: 900;
  margin-bottom: 4px;
}
.space-horizon-card strong {
  display: inline-flex;
  border-radius: 999px;
  padding: 3px 8px;
  font-size: 12px;
  margin-bottom: 6px;
}
.space-horizon-large {
  color: var(--green);
  background: #e7f6ed;
}
.space-horizon-mid {
  color: var(--amber);
  background: #fff4d6;
}
.space-horizon-low {
  color: var(--red);
  background: #fee4e2;
}
.space-horizon-card p {
  margin: 0;
  color: #344054;
  font-size: 12px;
  line-height: 1.55;
}
.space-step-confidence {
  display: block;
  margin-top: 6px;
  color: #667085;
  font-size: 11px;
  font-weight: 900;
}
.space-node-sizing-table table {
  min-width: 760px;
}
.space-node-sizing-table th,
.space-node-sizing-table td {
  font-size: 12px;
}
.space-summary-grid,
.space-boundary-grid,
.space-driver-tree {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}
.space-summary-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}
.space-boundary-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}
.space-summary-grid article,
.space-boundary-grid article,
.space-driver-card,
.space-model-grid article {
  border: 1px solid #e5edf7;
  border-radius: 16px;
  background: #fff;
  padding: 14px;
}
.space-summary-grid span,
.space-boundary-grid span,
.space-driver-card span,
.space-model-grid span {
  display: block;
  color: var(--blue);
  font-size: 12px;
  font-weight: 900;
  margin-bottom: 6px;
}
.space-summary-grid strong,
.space-model-grid strong,
.space-boundary-grid p,
.space-driver-card b {
  display: block;
  margin: 0;
  color: #344054;
  font-size: 13px;
  line-height: 1.6;
}
.space-driver-card dl {
  display: grid;
  gap: 7px;
  margin: 10px 0 0;
}
.space-driver-card dl div {
  display: grid;
  grid-template-columns: 76px 1fr;
  gap: 8px;
}
.space-driver-card dt {
  color: var(--blue);
  font-size: 12px;
  font-weight: 900;
}
.space-driver-card dd {
  margin: 0;
  color: #526071;
  font-size: 12px;
  line-height: 1.55;
}
.space-gate-model {
  display: grid;
  gap: 12px;
}
.space-model-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}
.space-model-note {
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 16px;
  background: #fff;
  padding: 14px;
}
.space-model-note.warning {
  background: #fffaf0;
  border-color: #f4d28f;
}
.space-model-note b {
  display: block;
  color: #27364a;
  font-size: 13px;
  margin-bottom: 5px;
}
.space-model-note p {
  margin: 0;
  color: #526071;
  font-size: 13px;
  line-height: 1.65;
}
.space-evidence-pack {
  display: grid;
  gap: 12px;
}
.space-evidence-card {
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 16px;
  background: linear-gradient(180deg, #ffffff, #f8fbff);
  padding: 14px;
}
.space-evidence-card header {
  border-bottom: 1px solid #e6edf7;
  margin-bottom: 12px;
  padding-bottom: 10px;
}
.space-evidence-card header span {
  display: inline-flex;
  color: var(--blue);
  background: #edf6ff;
  border: 1px solid #cfe6ff;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 900;
  padding: 3px 8px;
  margin-bottom: 8px;
}
.space-evidence-card h4 {
  margin: 0 0 5px;
  color: #1d2939;
  font-size: 16px;
}
.space-evidence-card header p {
  margin: 0;
  color: #526071;
  font-size: 13px;
  line-height: 1.6;
}
.space-evidence-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}
.space-evidence-grid section {
  border: 1px solid #e2e9f3;
  border-radius: 14px;
  background: #fff;
  padding: 12px;
}
.space-evidence-grid b {
  display: block;
  color: #27364a;
  font-size: 13px;
  margin-bottom: 7px;
}
.space-evidence-grid p,
.space-evidence-grid li {
  color: #526071;
  font-size: 12px;
  line-height: 1.65;
}
.space-evidence-grid ul,
.space-inference-chain {
  margin: 0;
  padding-left: 18px;
}
.space-refute-box {
  grid-column: 1 / -1;
  background: #fffaf0 !important;
  border-color: #f4d28f !important;
}
.space-evidence-sources {
  margin-top: 10px;
}
.space-scenario-table table { min-width: 1600px; }
.space-node-elasticity-table table { min-width: 2200px; }
.space-validation-table table { min-width: 1080px; }
.key-variable-grid {
  display: grid;
  grid-template-columns: minmax(260px, .8fr) minmax(520px, 1.2fr);
  gap: 14px;
}
.qa-generation-table {
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: #fbfcff;
}
.chain-map summary {
  cursor: pointer;
  font-weight: 800;
}
.chain-layer-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; margin: 18px 0; }
.chain-layer-card {
  border: 1px solid var(--line);
  border-radius: 16px;
  background: var(--surface-strong);
  padding: 16px;
}
.chain-layer-card h3 { margin: 0 0 8px; font-size: 16px; }
.chain-stage-panel {
  padding: 0;
  overflow: hidden;
}
.chain-stage-panel .chain-stage-head {
  display: grid;
  gap: 8px;
  padding: 16px 16px 8px;
}
.chain-stage-panel .chain-stage-head strong {
  color: #344054;
  font-size: 13px;
  line-height: 1.55;
}
.chain-stage-panel summary {
  list-style: none;
  cursor: pointer;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto auto;
  gap: 10px;
  align-items: center;
  padding: 16px;
}
.chain-stage-panel summary::-webkit-details-marker { display: none; }
.chain-stage-name {
  display: inline-flex;
  border-radius: 999px;
  background: #eaf3ff;
  color: #0a5dcc;
  font-weight: 900;
  font-size: 12px;
  padding: 4px 10px;
}
.chain-stage-panel summary small {
  color: var(--muted);
  font-weight: 800;
}
.chain-company-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 12px;
  padding: 0 16px 16px;
  margin: 0;
  list-style: none;
}
.chain-company-card {
  background: linear-gradient(180deg, #ffffff, #fbfdff);
}
.chain-company-list li.chain-company-card {
  border: 1px solid #edf1f7;
  border-radius: 12px;
  padding: 12px;
}
.chain-company-list li.chain-company-card b {
  display: block;
  color: #1d2939;
  font-size: 13px;
}
.chain-company-list li.chain-company-card span {
  display: block;
  color: #526071;
  font-size: 12px;
  margin-top: 4px;
}
.chain-company-list li.chain-company-card small {
  display: block;
  color: var(--blue);
  font-size: 11px;
  font-weight: 800;
  margin-top: 6px;
}
.chain-company-head {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: start;
  margin-bottom: 10px;
}
.chain-company-head b { display: block; color: #1d2939; }
.chain-company-head span {
  display: block;
  color: var(--blue);
  font-size: 12px;
  font-weight: 800;
}
.chain-company-head small {
  color: var(--muted);
  font-size: 11px;
  text-align: right;
}
.chain-map {
  overflow-x: auto;
  margin: 18px 0;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: #fbfcff;
  padding: 14px;
}
.chain-relationship-graph,
.chain-map-card,
.component-value-chain,
.technology-route-matrix,
.bottleneck-release-timeline,
.target-profit-bridge,
.target-valuation-table {
  margin: 20px 0;
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 18px;
  background:
    linear-gradient(135deg, rgba(10,132,255,.08), transparent 38%),
    linear-gradient(225deg, rgba(29,154,108,.08), transparent 42%),
    #ffffff;
  padding: 16px;
}
.component-value-chain,
.technology-route-matrix,
.bottleneck-release-timeline,
.target-profit-bridge,
.target-valuation-table {
  overflow-x: auto;
}
.component-value-chain table,
.technology-route-matrix table,
.bottleneck-release-timeline table,
.target-profit-bridge table,
.target-valuation-table table {
  min-width: 1180px;
}
.chain-company-network {
  margin: 20px 0;
  border: 1px solid rgba(10,132,255,.18);
  border-radius: 18px;
  background:
    linear-gradient(135deg, rgba(10,132,255,.08), transparent 38%),
    linear-gradient(225deg, rgba(29,154,108,.08), transparent 42%),
    #ffffff;
  padding: 16px;
}
/* ---- competition node cards ---- */
.competition-node-card {
  border: 1px solid rgba(10,132,255,.16);
  border-radius: 16px;
  background: #fbfcff;
  overflow: hidden;
  margin-bottom: 12px;
}
.competition-node-card > summary {
  display: grid;
  grid-template-columns: auto minmax(160px, .45fr) auto auto;
  gap: 10px;
  align-items: center;
  list-style: none;
  cursor: pointer;
  padding: 14px 16px;
}
.competition-node-card > summary::-webkit-details-marker { display: none; }
.competition-node-card[open] > summary { border-bottom: 1px solid rgba(10,132,255,.16); }
.competition-node-index {
  display: inline-flex;
  border-radius: 999px;
  background: #eef5ff;
  color: #0a84ff;
  border: 1px solid #d8e8ff;
  font-size: 11px;
  font-weight: 900;
  padding: 3px 8px;
}
.competition-node-card summary strong { color: #27364a; font-size: 14px; }
.competition-intensity {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
}
.competition-low { background: #e6f7ec; color: #1d9a6c; }
.competition-midlow { background: #eef5ff; color: #0a84ff; }
.competition-mid { background: #fff3e0; color: #cc7a00; }
.competition-high { background: #ffeaea; color: #c0392b; }
.competition-node-body { padding: 14px; }
.competition-subcard {
  border: 1px solid #edf1f7;
  border-radius: 12px;
  background: #fff;
  padding: 12px;
  margin-bottom: 10px;
}
.competition-subcard h4 {
  margin: 0 0 8px;
  font-size: 13px;
  color: #27364a;
}
.competition-subcard p {
  margin: 0;
  font-size: 12px;
  color: #4a5568;
  line-height: 1.55;
}
.competition-subcard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.competition-subcard-item {
  background: #fbfcff;
  border: 1px solid #edf1f7;
  border-radius: 10px;
  padding: 8px 10px;
}
.competition-subcard-item.col-span { grid-column: span 2; }
.competition-subcard-item > span { display: block; font-size: 11px; color: #667085; margin-bottom: 3px; }
.competition-subcard-item > strong { display: block; font-size: 14px; color: #27364a; }
.competition-subcard-item > small { display: block; font-size: 11px; color: #8896a7; margin-top: 2px; }
.competition-subcard-item > p { margin: 0; font-size: 12px; color: #4a5568; line-height: 1.5; }
.profit-pool-flow { margin: 20px 0; }
.profit-pool-flow .chain-graph-head { margin-bottom: 10px; }
.profit-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
}
.profit-high { background: #e6f7ec; color: #1d9a6c; }
.profit-mid { background: #fff3e0; color: #cc7a00; }
.profit-low { background: #ffeaea; color: #c0392b; }
.profit-rationale { font-size: 12px; color: #667085; line-height: 1.45; max-width: 320px; }
/* ---- end competition node cards ---- */
.chain-network-canvas {
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: 16px;
  background: #fbfcff;
  padding: 14px;
}
.chain-network-stage-grid {
  min-width: 960px;
  display: grid;
  grid-template-columns: repeat(3, minmax(260px, 1fr));
  gap: 14px;
}
.chain-network-stage {
  border: 1px solid rgba(217,224,234,.88);
  border-radius: 16px;
  background: rgba(255,255,255,.92);
  padding: 12px;
}
.chain-network-stage strong { color: #1d2939; }
.chain-network-stage p {
  min-height: 42px;
  margin: 6px 0 10px;
  color: var(--muted);
  font-size: 13px;
}
.chain-network-stage > div {
  display: grid;
  gap: 8px;
}
.chain-network-node {
  display: grid;
  gap: 2px;
  border: 1px solid #dbe7f5;
  border-radius: 12px;
  background: #ffffff;
  padding: 8px 10px;
}
.chain-network-node b { color: #1d2939; }
.chain-network-node small { color: var(--blue); font-weight: 800; }
.chain-network-edge-list {
  min-width: 960px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
  gap: 10px;
  margin-top: 14px;
}
.chain-network-edge-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
  gap: 8px;
  align-items: center;
  border: 1px solid #e2e8f2;
  border-radius: 14px;
  background: #ffffff;
  padding: 10px;
  color: #344054;
}
.chain-network-edge-card b { color: var(--green); font-size: 18px; }
.chain-network-edge-card small {
  grid-column: 1 / -1;
  color: var(--muted);
  font-size: 12px;
}
.chain-simple-flow {
  border: 1px solid #d8e6f7;
  border-radius: 12px;
  background: #f7fbff;
  padding: 12px;
  margin-bottom: 12px;
}
.simple-flow-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}
.simple-flow-head b { color: #27364a; }
.simple-flow-head span {
  color: var(--muted);
  font-size: 12px;
}
.chain-simple-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 8px;
}
.chain-simple-step {
  border: 1px solid #e1e7f0;
  border-radius: 12px;
  background: #fff;
  padding: 10px;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 8px;
  align-items: start;
}
.chain-simple-step > span {
  display: inline-flex;
  width: 26px;
  height: 26px;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: var(--blue);
  color: #fff;
  font-weight: 900;
  font-size: 12px;
}
.chain-simple-step b {
  display: block;
  color: #27364a;
  font-size: 13px;
  margin-bottom: 4px;
}
.chain-simple-step p {
  margin: 0;
  color: #344054;
  font-size: 12px;
  line-height: 1.55;
}
.chain-simple-step small {
  display: block;
  margin-top: 6px;
  color: var(--muted);
  font-size: 11px;
  line-height: 1.45;
}
.chain-value-guide {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 12px;
}
.chain-value-guide div {
  border: 1px solid #e2e8f2;
  border-radius: 12px;
  background: #ffffff;
  padding: 10px;
}
.chain-value-guide b {
  display: block;
  color: #1d2939;
  font-size: 13px;
}
.chain-value-guide span {
  display: block;
  color: var(--muted);
  font-size: 12px;
  margin-top: 4px;
}
.chain-sankey-list {
  display: grid;
  gap: 12px;
}
.chain-sankey-flow {
  display: grid;
  gap: 10px;
  border: 1px solid #e2e8f2;
  border-radius: 14px;
  background: #ffffff;
  padding: 12px;
}
.flow-step {
  display: flex;
  align-items: center;
  gap: 10px;
}
.flow-step span {
  display: inline-flex;
  width: 32px;
  height: 28px;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #eaf3ff;
  color: var(--blue);
  font-weight: 900;
}
.flow-step b { color: #1d2939; }
.flow-route {
  display: grid;
  grid-template-columns: minmax(160px, .9fr) minmax(260px, 1.4fr) minmax(160px, .9fr);
  gap: 10px;
  align-items: center;
}
.flow-from,
.flow-to {
  font-weight: 900;
  color: #1d2939;
  border: 1px solid #e7edf5;
  border-radius: 12px;
  background: #fbfcff;
  padding: 10px;
}
.flow-from small,
.flow-to small {
  display: block;
  color: var(--muted);
  font-size: 11px;
  font-weight: 800;
  margin-bottom: 4px;
}
.flow-band {
  min-height: calc(18px + var(--flow-weight, 3) * 4px);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: #2b6cb0;
  color: #ffffff;
  font-size: 12px;
  font-weight: 900;
  padding: 7px 12px;
  text-align: center;
}
.flow-demand .flow-band { background: #b7791f; }
.flow-feedback .flow-band { background: #667085; }
.flow-fields {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}
.flow-fields div {
  border: 1px solid #edf1f7;
  border-radius: 12px;
  background: #fbfcff;
  padding: 10px;
}
.flow-fields b {
  display: block;
  color: var(--blue);
  font-size: 12px;
  margin-bottom: 4px;
}
.flow-fields p {
  margin: 0;
  color: #526071;
  font-size: 12px;
}
.heat-score { text-align: center; }
.heat-score span {
  display: inline-flex;
  min-width: 30px;
  height: 26px;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-weight: 900;
}
.heat-high span { background: #e7f6ed; color: var(--green); }
.heat-mid span { background: #fff4d6; color: var(--amber); }
.heat-low span { background: #fee4e2; color: var(--red); }
.chain-graph-head {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: end;
  margin-bottom: 12px;
}
.chain-graph-title {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  color: #1d2939;
}
.table-scroll {
  max-width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: #fff;
}
.table-scroll table {
  width: max-content;
  min-width: 100%;
}
table { width: 100%; border-collapse: collapse; }
th, td { padding: 12px 14px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
th { color: #475467; font-size: 13px; background: #f7f9fc; }
.chain-chokepoints {
  margin-top: 12px;
  padding: 12px 14px;
  border-radius: 14px;
  background: #f7f9fc;
  color: #344054;
}
.qa-stack, .child-stack { display: grid; gap: 14px; }
.qa-card { padding: 0; overflow: clip; }
.qa-card.level-4 { background: rgba(255,255,255,.76); border-style: dashed; }
.qa-card.level-5 { background: rgba(247,249,252,.92); border-style: dashed; }
.qa-card.level-4 > summary { padding-left: 28px; }
.qa-card.level-5 > summary { padding-left: 36px; }
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
  min-width: 0;
  max-width: 100%;
}
.artifact-title {
  margin: 0 0 8px;
  font-weight: 800;
  color: #334155;
}
.artifact-table-wrap {
  overflow-x: auto;
  margin-bottom: 14px;
  border: 1px solid rgba(217,224,234,.8);
  border-radius: 12px;
}
.artifact-table th {
  white-space: nowrap;
}
.artifact-table td {
  min-width: 120px;
  font-size: 13px;
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
.target-odds-model {
  border: 1px solid var(--line);
  border-radius: 18px;
  background: rgba(255,255,255,.74);
  padding: 16px;
  margin: 18px 0;
  overflow-x: auto;
}
.target-odds-model h3 { margin: 0 0 6px; font-size: 18px; }
.target-odds-model p,
.target-profit-bridge p:not(.artifact-title),
.target-valuation-table p:not(.artifact-title) { margin: 0 0 12px; color: var(--muted); font-size: 14px; }
.target-table, .target-odds-table, .source-table { background: var(--surface-strong); overflow: hidden; }
.target-table, .target-odds-table { border-radius: 22px; }
.target-odds-table { min-width: 1500px; }
.state-actionable_long { color: var(--green); border-color: rgba(29,154,108,.28); background: #eaf8f2; }
.state-watch_only { color: var(--amber); border-color: rgba(183,121,31,.28); background: #fff7e6; }
.state-no_action { color: var(--red); border-color: rgba(194,65,61,.24); background: #fff1f0; }
.source-collapse { padding: 16px 18px; }
.source-collapse summary { cursor: pointer; font-weight: 800; color: #334155; }
.source-table { margin-top: 14px; }
@media (max-width: 760px) {
  .goal-card { grid-template-columns: 1fr; }
  .chain-bridge-grid,
  .chain-node-lens ul,
  .constraint-grid,
  .chain-qa-grid,
  .chain-value-guide,
  .space-summary-grid,
  .space-node-reasoning,
  .space-horizon-grid,
  .space-method-card-grid,
  .space-boundary-grid,
  .space-driver-tree,
  .space-model-grid,
  .space-evidence-grid,
  .key-variable-grid,
  .flow-route,
  .flow-fields { grid-template-columns: 1fr; }
  .space-node-card > summary { grid-template-columns: 1fr auto; }
  .space-node-label,
  .space-node-card summary strong,
  .space-node-card summary small { grid-column: 1 / 2; }
  .qa-card summary { grid-template-columns: auto 1fr auto; }
  .qa-count { grid-column: 2 / 3; }
  .target-table, .target-odds-table, .source-table, .chain-table { font-size: 13px; }
  .space-method-card { grid-template-columns: 1fr; }
  .space-method-card header {
    border-right: 0;
    border-bottom: 1px solid #edf1f7;
    padding-right: 0;
    padding-bottom: 8px;
  }
  .space-method-entry dl { grid-template-columns: 1fr; }
  th, td { padding: 10px; }
}
"""
