from __future__ import annotations

import re
from copy import deepcopy
from datetime import datetime, timezone
from html import unescape
from typing import Any


REPORT_SECTIONS = ["当前研究目标", "产业链全景", "问题下钻", "最终标的推荐", "来源索引"]
QA_BLOCK_TITLES = ["1. 当前结论呈现", "2. 问题展开（子 QA）", "3. 待补充的问题"]
SECTION_IDS = {
    REPORT_SECTIONS[0]: ("goal", "research-goal", "current-research-goal"),
    REPORT_SECTIONS[1]: ("chain", "supply-chain", "industry-chain", "产业链全景"),
    REPORT_SECTIONS[2]: ("qa", "qa-split", "question-drilldown"),
    REPORT_SECTIONS[3]: ("targets", "target-recommendations", "final-target-recommendations"),
    REPORT_SECTIONS[4]: ("sources", "source-index"),
}
LABEL_TERMS = [
    "forward_3m_return",
    "label_window",
    "benchmark_return",
    "excess_return",
    "start_price",
    "end_price",
    "股价变化标签",
    "标签起点",
    "标签终点",
    "标签窗口",
    "三个月涨幅",
]

PUBLIC_META_DRIFT_TERMS = [
    "本轮升级",
    "本次升级",
    "这次升级",
    "本轮更新",
    "本次更新",
    "本轮新增",
    "本次新增",
    "本轮改动",
    "本次改动",
    "本轮优化",
    "本次优化",
    "升级内容",
    "更新内容",
    "改动内容",
    "本轮如何落实",
    "机制深度映射",
    "mechanism_depth_map",
    "what changed in this run",
    "changed in this run",
    "iteration notes",
    "workbench appendix",
    "execution trace",
    "tool trace",
    "quality-framework explanation",
]

L3_REQUIRED_FIELDS = [
    "materiality",
    "decision_use",
    "support_evidence",
    "refute_evidence",
    "target_implications",
    "score_component",
    "minimum_evidence_gate",
    "refuting_source_plan",
    "source_plan",
    "skill_dispatch",
    "fact",
    "inference",
    "judgment",
    "gap",
    "trigger",
    "source_links",
]

L3_SKILL_DISPATCH_REQUIRED_FIELDS = [
    "task_family",
    "selected_skill",
    "concrete_materials",
    "extraction_schema",
    "source_extraction_ids",
    "leaf_source_review_ids",
    "skill_output_status",
    "fallback_used",
    "gpt_verification_status",
]

SOURCE_EXTRACTION_REQUIRED_FIELDS = [
    "extraction_id",
    "l3_question_id",
    "source_id",
    "source_title",
    "source_bucket",
    "parser",
    "parser_status",
    "schema_fields",
    "key_facts",
    "inference",
    "support_refute_or_lead",
    "uncertainties",
    "follow_up_data",
    "created_at",
]

LEAF_SOURCE_REVIEW_REQUIRED_FIELDS = [
    "review_id",
    "extraction_id",
    "l3_question_id",
    "source_id",
    "gpt_verification_status",
    "adopted_facts",
    "corrections",
    "rejected_claims",
    "final_bucket",
    "final_support_refute_or_lead",
    "allowed_to_strengthen_conclusion",
]

BACKTEST_ANTI_LEAKAGE_REQUIRED_FIELDS = [
    "anti_leakage_level",
    "as_of_date",
    "cutoff_source_pack_policy",
    "llm_prior_policy",
    "question_tree_policy",
    "supply_chain_policy",
    "scoring_policy",
    "label_isolation_policy",
]

L3_BACKTEST_GROUNDING_REQUIRED_FIELDS = [
    "allowed_source_ids",
    "model_prior_policy",
    "post_cutoff_knowledge_policy",
    "non_source_claims",
]

KNOWN_SPECIALTY_SKILLS = {
    "investment-question-architect",
    "research-source-planner",
    "financial-statement-analysis",
    "valuation-analysis",
    "industry-report-analysis",
    "supply-chain-panorama-explainer",
    "news-event-analysis",
    "opinion-analysis",
    "leaf-research-deepseek",
    "target-recommendation-analysis",
    "quant-research-fks",
    "quantitative-research",
    "frontend-design",
}

SCORE_WEIGHTS = {
    "chokepoint_strength": 0.26,
    "future_space": 0.18,
    "valuation_odds": 0.18,
    "evidence_quality": 0.14,
    "disconfirming_risk_control": 0.10,
    "monitorability": 0.05,
    "payoff_convexity": 0.09,
}

TARGET_SCORE_DIMENSIONS = [
    "scarcity_or_monopoly",
    "mispricing",
    "earnings_elasticity",
    "risk_control",
]

TARGET_SCORE_DIMENSION_WEIGHTS = {
    "scarcity_or_monopoly": 0.35,
    "mispricing": 0.25,
    "earnings_elasticity": 0.25,
    "risk_control": 0.15,
}

L3_SCORE_COMPONENTS = set(SCORE_WEIGHTS) | {
    "thesis_confidence",
    "payoff_convexity",
    "opportunity_fit",
    "action_state",
    "target_ranking",
    "risk_control",
    "source_quality",
}

DOMAIN_PLAYBOOKS = {
    "semiconductor_hardware": {
        "research_type": "industry/theme opportunity",
        "q_map": {
            "Q1": "Demand reality: AI capex, accelerator demand, memory demand, and endpoint risk",
            "Q2": "Value-capture bottlenecks: HBM, custom ASIC, networking, advanced foundry, packaging, and process control",
            "Q3": "Disconfirming tests and priced-in risk: ROI, capex digestion, memory cycle, WFE orders, and valuation",
            "Q4": "Target observation list: ranked securities reconciled with chokepoint score, odds, and downgrade triggers",
        },
        "mechanism_buckets": [
            "AI accelerator demand",
            "HBM and high-end memory bottleneck",
            "custom ASIC and Ethernet networking",
            "advanced foundry and advanced packaging",
            "wafer-fab equipment and process control",
            "valuation, payoff convexity, and disconfirming triggers",
        ],
        "mechanism_depth_blocks": [
            "demand_driver_tree",
            "supply_or_access_response",
            "unit_economics_profit_bridge",
            "competitive_value_capture_map",
            "market_pricing_bridge",
            "disconfirming_counter_supply_tests",
            "capital_chain_second_order_beneficiaries",
            "model_reconciliation",
        ],
        "required_extraction_schemas": [
            "demand_driver_tree",
            "capacity_or_access_response",
            "unit_economics_bridge",
            "valuation_rerating_bridge",
            "model_reconciliation",
        ],
        "depth_quality_rule": "do_not_accept_generic_theme_exposure_without_driver_tree_from_demand_to_target_revenue_margin_fcf_and_valuation_odds",
        "default_score_schema": SCORE_WEIGHTS,
    },
    "memory_industry": {
        "research_type": "industry/theme opportunity",
        "q_map": {
            "Q1": "Demand reality: convert AI, data-center, and terminal demand into sustainable bit demand, ASP, and product mix",
            "Q2": "Value-capture bottlenecks: test scarcity, pricing power, and financial conversion across HBM, high-end DRAM, NAND/eSSD, nearline HDD, controllers, capacity, equipment, materials, and packaging",
            "Q3": "Disconfirming tests and priced-in risk: supply response, inventory, ASP decline, substitute architectures, customer capex digestion, China supply, mid-cycle downside, and valuation",
            "Q4": "Target observation list: specific assets reconciled with scarcity, mispricing, earnings elasticity, risk control, valuation odds, and kill tests",
        },
        "mechanism_buckets": [
            "Workload-to-product demand",
            "Price-volume-mix-inventory bridge",
            "Demand-supply slope mismatch",
            "HBM/high-end DRAM scarcity",
            "NAND/eSSD/nearline HDD cash-flow economics",
            "Controller/IP and firmware capture",
            "Capacity/equipment/materials second-order chain",
            "Company value capture",
            "Counter-supply and substitution",
            "Market-pricing and rerating",
            "Monitoring and kill tests",
            "Model口径 reconciliation",
        ],
        "mechanism_depth_blocks": [
            "demand_driver_tree",
            "supply_or_access_response",
            "unit_economics_profit_bridge",
            "competitive_value_capture_map",
            "market_pricing_bridge",
            "disconfirming_counter_supply_tests",
            "capital_chain_second_order_beneficiaries",
            "model_reconciliation",
        ],
        "required_extraction_schemas": [
            "memory_supply_capacity",
            "memory_demand_driver",
            "memory_unit_economics",
            "memory_valuation_rerating",
            "memory_capital_chain",
            "memory_model_reconciliation",
        ],
        "scoring_adjustments": {
            "future_space": "include demand-supply slope mismatch, not only TAM",
            "chokepoint_strength": "include supply/access constraint, qualification difficulty, and ramp lead time",
            "valuation_odds": "include implied cyclicality discount or rerating path when relevant",
            "disconfirming_risk_control": "include counter-supply, inventory, ASP, and customer capex tests",
            "payoff_convexity": "separate operating leverage, mix shift, and multiple rerating",
        },
        "depth_quality_rule": "memory research is too shallow if it lacks workload-to-product demand, capacity response, ASP/cost/mix, company financial conversion, valuation rerating, and model口径 reconciliation",
        "default_score_schema": SCORE_WEIGHTS,
    },
    "optical_module": {
        "research_type": "industry/theme opportunity",
        "q_map": {
            "Q1": "Demand reality: AI cluster networking, 800G/1.6T port demand, customer capex, and order visibility",
            "Q2": "Value-capture bottlenecks: lasers, InP/silicon photonics, DSP/driver/TIA, components, module integration, qualification, yield, and manufacturing capacity",
            "Q3": "Disconfirming tests and priced-in risk: LPO/CPO/substitution, copper/OCS architecture, capacity expansion, ASP erosion, customer concentration, geopolitics, and valuation",
            "Q4": "Target observation list: specific module, laser/component, manufacturing, and chip assets reconciled with chokepoint score, financial conversion, valuation odds, and kill tests",
        },
        "mechanism_buckets": [
            "AI cluster network demand",
            "800G/1.6T speed transition",
            "Customer order visibility and concentration",
            "Laser/InP/silicon photonics bottleneck",
            "DSP/driver/TIA value capture",
            "Module integration, yield, and qualification",
            "LPO/CPO/copper/OCS substitution",
            "Manufacturing capacity and EMS beta",
            "Company financial conversion",
            "Market-pricing and rerating",
            "Monitoring and kill tests",
        ],
        "mechanism_depth_blocks": [
            "demand_driver_tree",
            "supply_or_access_response",
            "unit_economics_profit_bridge",
            "competitive_value_capture_map",
            "market_pricing_bridge",
            "disconfirming_counter_supply_tests",
            "capital_chain_second_order_beneficiaries",
            "model_reconciliation",
        ],
        "required_extraction_schemas": [
            "optical_port_demand",
            "optical_component_capacity",
            "optical_module_unit_economics",
            "optical_customer_order_visibility",
            "optical_valuation_rerating",
            "optical_model_reconciliation",
        ],
        "scoring_adjustments": {
            "future_space": "include AI cluster port count, speed mix, attach rate, and customer capex durability",
            "chokepoint_strength": "include laser/component scarcity, customer qualification, yield, capacity reservation, and substitution risk",
            "valuation_odds": "include whether 800G/1.6T growth and high margins are already priced",
            "disconfirming_risk_control": "include CPO/LPO/copper/OCS substitution, ASP erosion, capacity expansion, and customer concentration",
            "payoff_convexity": "separate module revenue growth, component margin leverage, manufacturing beta, and multiple rerating",
        },
        "depth_quality_rule": "optical module research is too shallow if it does not model AI port demand, speed transition, component/module bottlenecks, customer qualification, price erosion, financial conversion, valuation, and technology substitution kill tests",
        "default_score_schema": SCORE_WEIGHTS,
    },
    "default": {
        "research_type": "custom",
        "q_map": {
            "Q1": "Demand or primary driver reality",
            "Q2": "Value-capture mechanism and bottlenecks",
            "Q3": "Disconfirming tests, financial quality, and priced-in risk",
            "Q4": "Specific target observation list and monitoring plan",
        },
        "mechanism_buckets": [
            "primary driver",
            "value capture",
            "risk and valuation",
            "target mapping",
        ],
        "mechanism_depth_blocks": [
            "demand_driver_tree",
            "supply_or_access_response",
            "unit_economics_profit_bridge",
            "competitive_value_capture_map",
            "market_pricing_bridge",
            "disconfirming_counter_supply_tests",
            "capital_chain_second_order_beneficiaries",
            "model_reconciliation",
        ],
        "default_score_schema": SCORE_WEIGHTS,
    },
}


def validate_report_contract_html(
    html: str,
    *,
    mode: str = "historical_backtest",
    require_l3: bool = False,
) -> dict[str, Any]:
    """Validate the public HTML report against the locked presentation contract."""
    issues: list[dict[str, str]] = []
    section_positions = _section_positions(html)
    found_sections = [section for section in REPORT_SECTIONS if section in section_positions]
    if found_sections != REPORT_SECTIONS:
        _issue(issues, "error", "top_level_sections", "final HTML must use the locked five-section order")
    else:
        positions = [section_positions[section] for section in REPORT_SECTIONS]
        if positions != sorted(positions):
            _issue(issues, "error", "top_level_order", "top-level sections are out of order")

    level_counts = {
        "level1_cards": _class_count(html, "qa-card", "level-1"),
        "level2_cards": _class_count(html, "qa-card", "level-2"),
        "level3_cards": _class_count(html, "qa-card", "level-3"),
    }
    if level_counts["level1_cards"] == 0:
        _issue(issues, "error", "missing_level1_cards", "问题下钻 must render Q1-Q4 as qa-card level-1")
    if level_counts["level2_cards"] == 0:
        _issue(issues, "error", "missing_level2_cards", "L1 cards must render mechanism buckets as qa-card level-2")
    if require_l3 and level_counts["level3_cards"] == 0:
        _issue(issues, "error", "missing_level3_cards", "complete refreshed reports must render L3 leaves")

    interactive_level_counts = {
        "interactive_level1_cards": _tag_class_count(html, "details", "qa-card", "level-1"),
        "interactive_level2_cards": _tag_class_count(html, "details", "qa-card", "level-2"),
        "interactive_level3_cards": _tag_class_count(html, "details", "qa-card", "level-3"),
    }
    if (
        interactive_level_counts["interactive_level1_cards"] != level_counts["level1_cards"]
        or interactive_level_counts["interactive_level2_cards"] != level_counts["level2_cards"]
        or interactive_level_counts["interactive_level3_cards"] != level_counts["level3_cards"]
    ):
        _issue(
            issues,
            "error",
            "missing_interactive_qa_cards",
            "QA cards must render as clickable details.qa-card nodes, not static article/div cards",
        )
    total_qa_cards = sum(level_counts.values())
    interaction_affordance_counts = {
        "summary_elements": _tag_count(html, "summary"),
        "qa_count_elements": _class_count(html, "qa-count"),
        "chevron_elements": _class_count(html, "chevron"),
    }
    if (
        interaction_affordance_counts["summary_elements"] < total_qa_cards
        or interaction_affordance_counts["qa_count_elements"] < total_qa_cards
        or interaction_affordance_counts["chevron_elements"] < total_qa_cards
    ):
        _issue(
            issues,
            "error",
            "missing_qa_interaction_affordance",
            "QA cards must include qa-count and chevron interaction affordances",
        )

    supply_chain_sections = _class_count(html, "supply-chain-section")
    if supply_chain_sections == 0:
        _issue(
            issues,
            "error",
            "missing_supply_chain_section",
            "final HTML must include a standalone 产业链全景 section before 问题下钻",
        )
    if "chain-table" not in html and "chain-map" not in html:
        _issue(
            issues,
            "error",
            "missing_supply_chain_map",
            "产业链全景 must render an auditable chain map/table of upstream, midstream, downstream, players, and value links",
        )
    required_chain_explainer_classes = [
        "chain-explain",
        "chain-plain-summary",
        "chain-flow-steps",
        "chain-layer-grid",
        "chain-layer-card",
        "chain-chokepoints",
        "chain-target-links",
    ]
    missing_chain_explainer_classes = [
        class_name for class_name in required_chain_explainer_classes if _class_count(html, class_name) == 0
    ]
    if missing_chain_explainer_classes:
        _issue(
            issues,
            "error",
            "missing_beginner_chain_explainer",
            "产业链全景 must include beginner-readable Chinese explanation components; missing "
            + ", ".join(missing_chain_explainer_classes),
        )

    l3_metadata_counts = {
        "l3_skill_elements": _class_count(html, "l3-skill"),
        "l3_execution_status_elements": _class_count(html, "l3-execution-status"),
        "l3_score_component_elements": _class_count(html, "l3-score-component"),
        "l3_decision_use_elements": _class_count(html, "l3-decision-use"),
    }
    if require_l3 and level_counts["level3_cards"] > 0 and (
        l3_metadata_counts["l3_skill_elements"] < level_counts["level3_cards"]
        or l3_metadata_counts["l3_execution_status_elements"] < level_counts["level3_cards"]
        or l3_metadata_counts["l3_score_component_elements"] < level_counts["level3_cards"]
        or l3_metadata_counts["l3_decision_use_elements"] < level_counts["level3_cards"]
    ):
        _issue(
            issues,
            "error",
            "missing_l3_skill_metadata",
            "L3 cards must visibly show selected skill, execution status, score component, and decision use",
        )

    for title in QA_BLOCK_TITLES:
        if title not in html:
            _issue(issues, "error", "missing_qa_block_title", f"QA cards must include {title}")

    target_start = section_positions.get("最终标的推荐", -1)
    source_start = section_positions.get("来源索引", len(html))
    qa_start = section_positions.get("问题下钻", -1)
    qa_region_end = target_start if target_start >= 0 else len(html)
    qa_region = html[qa_start:qa_region_end] if qa_start >= 0 else html
    q4_relative_position = _first_position(qa_region, ['class="qid">Q4', "class='qid'>Q4", ">Q4<", "id=\"q4", "id='q4", "Q4"])
    q4_position = qa_start + q4_relative_position if qa_start >= 0 and q4_relative_position >= 0 else -1
    if q4_position < 0 or (qa_start >= 0 and not (qa_start <= q4_position < max(target_start, qa_start))):
        _issue(issues, "error", "q4_not_in_question_drilldown", "Q4 must remain inside 问题下钻")

    if _class_count(html, "target-section") == 0:
        _issue(issues, "error", "missing_target_section", "最终标的推荐 must render as target-section")
    if "target-table" not in html:
        _issue(issues, "error", "missing_target_table", "最终标的推荐 must render a dense target-table")
    if "source-collapse" not in html:
        _issue(issues, "error", "missing_source_collapse", "来源索引 must render as a collapsed source-collapse")

    target_region = html[target_start:source_start] if target_start >= 0 else ""
    action_state_terms = ("actionable_long", "watch_only", "no_action")
    missing_action_state_classes = [
        f"state-{action_state}"
        for action_state in action_state_terms
        if action_state in target_region and f"state-{action_state}" not in target_region
    ]
    if missing_action_state_classes:
        _issue(
            issues,
            "error",
            "missing_action_state_color_class",
            "target-table action_state cells must keep the canonical color classes: "
            + ", ".join(missing_action_state_classes),
        )

    canonical_component_classes = [
        "hero",
        "top-nav",
        "goal-card",
        "supply-chain-section",
        "chain-explain",
        "chain-plain-summary",
        "chain-flow-steps",
        "chain-layer-grid",
        "chain-layer-card",
        "chain-chokepoints",
        "chain-target-links",
        "chain-map",
        "chain-table",
        "qa-body",
        "qa-block",
        "block-title",
        "artifact-card",
        "target-section",
        "target-table",
        "source-collapse",
    ]
    missing_component_classes = [
        class_name for class_name in canonical_component_classes if _class_count(html, class_name) == 0
    ]
    if missing_component_classes:
        _issue(
            issues,
            "error",
            "missing_canonical_component_class",
            "refreshed canonical reports must reuse the shared frontend component family; missing "
            + ", ".join(missing_component_classes),
        )

    if mode == "historical_backtest":
        non_target_region = html[: max(target_start, 0)] + html[source_start:]
        if any(term in non_target_region for term in LABEL_TERMS):
            _issue(
                issues,
                "error",
                "label_outside_final_targets",
                "current-time label fields may appear only inside 最终标的推荐",
            )
        if not any(term in target_region for term in LABEL_TERMS):
            _issue(issues, "warning", "missing_label_area", "historical backtest reports should include one label area")

    lowered_html = html.lower()
    for term in PUBLIC_META_DRIFT_TERMS:
        if term.lower() in lowered_html:
            _issue(
                issues,
                "error",
                "public_meta_drift",
                f"final HTML must not include process/change-log term: {term}",
            )

    return {
        "ok": not any(issue["severity"] == "error" for issue in issues),
        "summary": {
            "top_level_sections": found_sections,
            "supply_chain_sections": supply_chain_sections,
            **level_counts,
            **interactive_level_counts,
            **interaction_affordance_counts,
            **l3_metadata_counts,
            "mode": mode,
        },
        "issues": issues,
    }


def validate_qa_tree_schema(qa_tree: dict[str, Any], *, require_l3: bool = False) -> dict[str, Any]:
    """Validate the structured QA tree shape used before HTML rendering."""
    issues: list[dict[str, str]] = []
    nodes = [node for node in qa_tree.get("nodes", []) if isinstance(node, dict)]
    nodes_by_id = {str(node.get("id")): node for node in nodes if node.get("id")}
    l1_nodes = [node for node in nodes if _level_number(node.get("level")) == 1]
    l2_nodes = [node for node in nodes if _level_number(node.get("level")) == 2]
    l3_nodes = [node for node in nodes if _level_number(node.get("level")) == 3]

    if not l1_nodes:
        _issue(issues, "error", "missing_l1", "QA tree must include L1 nodes")
    if not l2_nodes:
        _issue(issues, "error", "missing_l2", "QA tree must include L2 mechanism buckets")
    if require_l3 and not l3_nodes:
        _issue(issues, "error", "missing_l3", "complete QA trees must include L3 evidence units")

    for node in nodes:
        node_id = str(node.get("id", ""))
        for child_id in node.get("next_question_ids", []) or []:
            child = nodes_by_id.get(str(child_id))
            if child is None:
                _issue(issues, "error", "missing_child", f"{node_id} points to missing child {child_id}")
                continue
            if str(child.get("parent_id", "")) not in {node_id, ""}:
                _issue(issues, "error", "broken_parent_link", f"{child_id} has a mismatched parent_id")

    for node in l3_nodes:
        node_id = str(node.get("id", ""))
        for field in L3_REQUIRED_FIELDS:
            if _is_empty(node.get(field)):
                _issue(issues, "error", "l3_missing_field", f"{node_id} is missing {field}")
        _validate_l3_source_plan(node, node_id, issues)
        _validate_l3_skill_dispatch(node, node_id, issues)
        _validate_l3_score_component(node, node_id, issues)
        logic_values = {
            field: _normalized_logic_text(node.get(field))
            for field in ("fact", "inference", "judgment")
            if not _is_empty(node.get(field))
        }
        if (
            len(logic_values) == 3
            and len(set(logic_values.values())) == 1
        ):
            _issue(
                issues,
                "error",
                "l3_undifferentiated_logic",
                f"{node_id} must separate fact, inference, and judgment instead of repeating one conclusion",
            )

    return {
        "ok": not any(issue["severity"] == "error" for issue in issues),
        "summary": {
            "nodes": len(nodes),
            "l1_nodes": len(l1_nodes),
            "l2_nodes": len(l2_nodes),
            "l3_nodes": len(l3_nodes),
        },
        "issues": issues,
    }


def audit_time_slice_sources(sources: list[dict[str, Any]], *, as_of_date: str) -> dict[str, Any]:
    """Audit whether sources obey the historical backtest cutoff."""
    issues: list[dict[str, str]] = []
    cutoff = _parse_date(as_of_date)
    post_cutoff_non_label_count = 0
    label_only_count = 0
    quarantined_count = 0

    for source in sources:
        source_id = str(source.get("source_id") or source.get("id") or "")
        visible_at = _parse_date(str(source.get("source_visible_at") or source.get("published_at") or ""))
        usage = str(source.get("allowed_usage") or "thesis")
        used_in = [str(item) for item in source.get("used_in", []) or []]
        if usage == "label_only":
            label_only_count += 1
            if any("label" not in item and "final" not in item for item in used_in):
                _issue(issues, "error", "label_source_used_in_thesis", f"{source_id} label-only source is used in QA")
        if usage == "quarantined":
            quarantined_count += 1
        if usage not in {"label_only", "quarantined"} and _is_empty(source.get("availability_proof")):
            _issue(
                issues,
                "error",
                "source_missing_availability_proof",
                f"{source_id} needs an auditable availability_proof for historical-mode thesis use",
            )
        if visible_at and visible_at > cutoff and usage not in {"label_only", "quarantined"}:
            post_cutoff_non_label_count += 1
            _issue(issues, "error", "post_cutoff_thesis_source", f"{source_id} is visible after {as_of_date}")

    return {
        "ok": not any(issue["severity"] == "error" for issue in issues),
        "summary": {
            "sources": len(sources),
            "as_of_date": as_of_date,
            "post_cutoff_non_label_count": post_cutoff_non_label_count,
            "label_only_count": label_only_count,
            "quarantined_count": quarantined_count,
        },
        "issues": issues,
    }


def score_target_observation(target: dict[str, Any]) -> dict[str, Any]:
    """Score a target around four investable-opportunity dimensions."""
    direct_components = {key: _score_value(target.get(key, 0)) for key in SCORE_WEIGHTS}
    subcomponent_audit: dict[str, list[dict[str, Any]]] = {}
    components = {
        key: _score_from_subcomponents(key, target, direct_components[key], subcomponent_audit)
        for key in SCORE_WEIGHTS
    }
    score_dimensions = _target_score_dimensions(target, components)
    raw_total_score = round(
        sum(score_dimensions[key] * weight for key, weight in TARGET_SCORE_DIMENSION_WEIGHTS.items()),
        3,
    )
    thesis_confidence = round(
        components["chokepoint_strength"] * 0.30
        + components["future_space"] * 0.15
        + components["valuation_odds"] * 0.10
        + components["evidence_quality"] * 0.25
        + components["disconfirming_risk_control"] * 0.15
        + components["monitorability"] * 0.05,
        3,
    )
    payoff_convexity = round(
        components["payoff_convexity"] * 0.45
        + _score_value(target.get("valuation_tolerance", 0)) * 0.20
        + (6 - _score_value(target.get("downside_fragility", 0))) * 0.20
        + _score_value(target.get("catalyst_proximity", 0)) * 0.15,
        3,
    )
    gate = _opportunity_gate(target, components, thesis_confidence, payoff_convexity)
    total_score = round(min(raw_total_score, gate["max_total_score"]), 3)
    return {
        "ticker": str(target.get("ticker", "")),
        "score_components": components,
        "score_dimensions": score_dimensions,
        "score_subcomponents": subcomponent_audit,
        "weights": dict(SCORE_WEIGHTS),
        "dimension_weights": dict(TARGET_SCORE_DIMENSION_WEIGHTS),
        "raw_total_score": raw_total_score,
        "total_score": total_score,
        "thesis_confidence": thesis_confidence,
        "payoff_convexity": payoff_convexity,
        "opportunity_fit": gate["opportunity_fit"],
        "action_state": gate["action_state"],
        "gate_reasons": gate["gate_reasons"],
        "strength": _strength_bucket(total_score, thesis_confidence, payoff_convexity),
    }


def rank_target_observations(targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Rank targets deterministically from action state, fit, score, and convexity."""
    action_priority = {"actionable_long": 0, "watch_only": 1, "no_action": 2}

    def sort_key(target: dict[str, Any]) -> tuple[Any, ...]:
        score = target.get("score", {}) if isinstance(target.get("score"), dict) else {}
        action_state = str(target.get("action_state") or score.get("action_state") or "no_action")
        return (
            action_priority.get(action_state, 3),
            -_optional_float(score.get("opportunity_fit") or 0),
            -_optional_float(score.get("total_score") or 0),
            -_optional_float(score.get("payoff_convexity") or 0),
            -_optional_float(score.get("thesis_confidence") or 0),
            str(target.get("ticker") or target.get("name") or ""),
        )

    ranked = [deepcopy(target) for target in sorted(targets, key=sort_key)]
    for index, target in enumerate(ranked, start=1):
        target["rank"] = index
    return ranked


def validate_source_extraction_schema(
    source_extractions: list[dict[str, Any]],
    qa_tree: dict[str, Any],
) -> dict[str, Any]:
    """Validate that source-parser outputs filled the selected specialty schema."""
    issues: list[dict[str, str]] = []
    l3_ids: set[str] = set()
    expected_extraction_ids: set[str] = set()
    required_by_l3: dict[str, dict[str, Any]] = {}
    for node in qa_tree.get("nodes", []) or []:
        if _level_number(node.get("level")) != 3:
            continue
        node_id = str(node.get("id") or "")
        if not node_id:
            continue
        l3_ids.add(node_id)
        dispatch = node.get("skill_dispatch") if isinstance(node.get("skill_dispatch"), dict) else {}
        schema = dispatch.get("extraction_schema") or []
        expected_extraction_ids.update(str(item) for item in dispatch.get("source_extraction_ids", []) or [] if str(item))
        if isinstance(schema, (list, tuple)):
            required_by_l3[node_id] = {
                "fields": [str(item) for item in schema if str(item)],
                "schema_name": "",
            }
        elif isinstance(schema, dict):
            required_by_l3[node_id] = {
                "fields": [str(item) for item in schema.keys() if str(item)],
                "schema_name": str(schema.get("schema") or schema.get("name") or ""),
            }
        elif isinstance(schema, str) and schema.strip():
            required_by_l3[node_id] = {"fields": [], "schema_name": schema.strip()}

    extraction_ids = {str(record.get("extraction_id") or "") for record in source_extractions if record.get("extraction_id")}
    for extraction_id in sorted(expected_extraction_ids - extraction_ids):
        _issue(
            issues,
            "error",
            "l3_missing_source_extraction",
            f"L3 skill_dispatch references missing source extraction {extraction_id}",
        )

    for record in source_extractions:
        extraction_id = str(record.get("extraction_id") or "")
        l3_id = str(record.get("l3_question_id") or "")
        for field in SOURCE_EXTRACTION_REQUIRED_FIELDS:
            if field not in record or (field not in {"uncertainties", "follow_up_data"} and _is_empty(record.get(field))):
                _issue(
                    issues,
                    "error",
                    "source_extraction_missing_field",
                    f"{extraction_id or '<missing extraction_id>'} is missing required field {field}",
                )
        if l3_id and l3_ids and l3_id not in l3_ids:
            _issue(
                issues,
                "error",
                "source_extraction_unknown_l3",
                f"{extraction_id} points to unknown L3 node {l3_id}",
            )
        if extraction_id and expected_extraction_ids and extraction_id not in expected_extraction_ids:
            _issue(
                issues,
                "warning",
                "source_extraction_not_referenced",
                f"{extraction_id} is not referenced by any L3 skill_dispatch.source_extraction_ids",
            )
        if str(record.get("source_bucket") or "") not in {"evidence", "research_report", "opinion", "message"}:
            _issue(
                issues,
                "error",
                "source_extraction_invalid_bucket",
                f"{extraction_id} source_bucket must be evidence, research_report, opinion, or message",
            )
        if str(record.get("support_refute_or_lead") or "") not in {"support", "refute", "lead"}:
            _issue(
                issues,
                "error",
                "source_extraction_invalid_stance",
                f"{extraction_id} support_refute_or_lead must be support, refute, or lead",
            )
        required_spec = required_by_l3.get(l3_id, {})
        required = list(required_spec.get("fields", []) or [])
        schema_name = str(required_spec.get("schema_name") or "")
        schema_fields = record.get("schema_fields")
        if (required or schema_name) and not isinstance(schema_fields, dict):
            _issue(
                issues,
                "error",
                "source_extraction_missing_schema_fields",
                f"{extraction_id} must include schema_fields for L3 {l3_id}",
            )
            continue
        for field in required:
            field_value = schema_fields.get(field) if isinstance(schema_fields, dict) else None
            if _is_empty(field_value) or (isinstance(field_value, dict) and _is_empty(field_value.get("value"))):
                _issue(
                    issues,
                    "error",
                    "source_extraction_missing_schema_field",
                    f"{extraction_id} is missing schema field {field}",
                )
        if schema_name and isinstance(schema_fields, dict) and str(schema_fields.get("schema") or "") != schema_name:
            _issue(
                issues,
                "error",
                "source_extraction_schema_name_mismatch",
                f"{extraction_id} schema_fields.schema must match L3 extraction_schema {schema_name}",
            )
        if str(record.get("parser_status") or "").lower() not in {"ok", "complete", "completed"}:
            _issue(
                issues,
                "error",
                "source_extraction_not_complete",
                f"{extraction_id} parser_status must be complete before strengthening conclusions",
            )

    return {
        "ok": not any(issue["severity"] == "error" for issue in issues),
        "summary": {
            "source_extractions": len(source_extractions),
            "l3_schema_nodes": len(required_by_l3),
            "expected_source_extractions": len(expected_extraction_ids),
        },
        "issues": issues,
    }


def validate_leaf_source_review_schema(
    leaf_source_reviews: list[dict[str, Any]],
    source_extractions: list[dict[str, Any]],
    qa_tree: dict[str, Any],
) -> dict[str, Any]:
    """Validate GPT review records that approve or reject parser outputs."""
    issues: list[dict[str, str]] = []
    extraction_by_id = {
        str(record.get("extraction_id")): record
        for record in source_extractions
        if isinstance(record, dict) and record.get("extraction_id")
    }
    expected_extraction_ids: set[str] = set()
    expected_review_ids: set[str] = set()
    for node in qa_tree.get("nodes", []) or []:
        if _level_number(node.get("level")) != 3:
            continue
        dispatch = node.get("skill_dispatch") if isinstance(node.get("skill_dispatch"), dict) else {}
        expected_extraction_ids.update(str(item) for item in dispatch.get("source_extraction_ids", []) or [] if str(item))
        expected_review_ids.update(str(item) for item in dispatch.get("leaf_source_review_ids", []) or [] if str(item))

    review_ids = {str(record.get("review_id") or "") for record in leaf_source_reviews if record.get("review_id")}
    reviewed_extraction_ids = {
        str(record.get("extraction_id") or "") for record in leaf_source_reviews if record.get("extraction_id")
    }
    for review_id in sorted(expected_review_ids - review_ids):
        _issue(
            issues,
            "error",
            "l3_missing_leaf_source_review",
            f"L3 skill_dispatch references missing leaf source review {review_id}",
        )
    for extraction_id in sorted(expected_extraction_ids - reviewed_extraction_ids):
        _issue(
            issues,
            "error",
            "source_extraction_missing_gpt_review",
            f"{extraction_id} must have a matching GPT verification record in leaf_source_reviews.jsonl",
        )

    for record in leaf_source_reviews:
        review_id = str(record.get("review_id") or "")
        for field in LEAF_SOURCE_REVIEW_REQUIRED_FIELDS:
            if field not in record or (field not in {"corrections", "rejected_claims"} and _is_empty(record.get(field))):
                _issue(
                    issues,
                    "error",
                    "leaf_source_review_missing_field",
                    f"{review_id or '<missing review_id>'} is missing required field {field}",
                )
        if review_id and expected_review_ids and review_id not in expected_review_ids:
            _issue(
                issues,
                "warning",
                "leaf_source_review_not_referenced",
                f"{review_id} is not referenced by any L3 skill_dispatch.leaf_source_review_ids",
            )
        extraction_id = str(record.get("extraction_id") or "")
        extraction = extraction_by_id.get(extraction_id)
        if extraction_id and extraction is None:
            _issue(
                issues,
                "error",
                "leaf_source_review_unknown_extraction",
                f"{review_id} points to unknown source extraction {extraction_id}",
            )
        elif extraction is not None:
            if str(record.get("source_id") or "") != str(extraction.get("source_id") or ""):
                _issue(
                    issues,
                    "error",
                    "leaf_source_review_source_mismatch",
                    f"{review_id} source_id must match extraction {extraction_id}",
                )
            if str(record.get("l3_question_id") or "") != str(extraction.get("l3_question_id") or ""):
                _issue(
                    issues,
                    "error",
                    "leaf_source_review_l3_mismatch",
                    f"{review_id} l3_question_id must match extraction {extraction_id}",
                )
        status = str(record.get("gpt_verification_status") or "").lower()
        allowed = record.get("allowed_to_strengthen_conclusion")
        if status not in {"verified", "verified_with_caveats", "rejected", "needs_review"} and not status.startswith("verified_"):
            _issue(
                issues,
                "error",
                "leaf_source_review_invalid_status",
                f"{review_id} gpt_verification_status must be verified, verified_with_caveats, rejected, or needs_review",
            )
        if allowed is True and not (status == "verified" or status.startswith("verified_") or status == "verified_with_caveats"):
            _issue(
                issues,
                "error",
                "leaf_source_review_allows_unverified_extraction",
                f"{review_id} cannot strengthen conclusions unless GPT verification is verified",
            )
        if str(record.get("final_bucket") or "") not in {"evidence", "research_report", "opinion", "message"}:
            _issue(
                issues,
                "error",
                "leaf_source_review_invalid_bucket",
                f"{review_id} final_bucket must be evidence, research_report, opinion, or message",
            )
        if str(record.get("final_support_refute_or_lead") or "") not in {"support", "refute", "lead"}:
            _issue(
                issues,
                "error",
                "leaf_source_review_invalid_stance",
                f"{review_id} final_support_refute_or_lead must be support, refute, or lead",
            )

    return {
        "ok": not any(issue["severity"] == "error" for issue in issues),
        "summary": {
            "leaf_source_reviews": len(leaf_source_reviews),
            "expected_leaf_source_reviews": len(expected_review_ids),
            "reviewed_source_extractions": len(reviewed_extraction_ids),
        },
        "issues": issues,
    }


def validate_target_observation_contract(targets: list[dict[str, Any]]) -> dict[str, Any]:
    """Validate target observation scoring audit and hard disconfirming tests."""
    issues: list[dict[str, str]] = []
    for target in targets:
        ticker = str(target.get("ticker") or target.get("name") or "")
        score = target.get("score") if isinstance(target.get("score"), dict) else {}
        subcomponents = target.get("score_subcomponents") or score.get("score_subcomponents")
        if not isinstance(subcomponents, dict):
            _issue(
                issues,
                "error",
                "target_missing_score_subcomponents",
                f"{ticker} must preserve auditable score_subcomponents for every score component",
            )
        else:
            for component in SCORE_WEIGHTS:
                rows = subcomponents.get(component)
                if not isinstance(rows, list) or not rows:
                    _issue(
                        issues,
                        "error",
                        "target_missing_score_component_subcomponents",
                        f"{ticker} is missing score_subcomponents.{component}",
                    )
                else:
                    for row in rows:
                        if not isinstance(row, dict) or _is_empty(row.get("score")):
                            _issue(
                                issues,
                                "error",
                                "target_invalid_score_subcomponent",
                                f"{ticker} has an invalid subcomponent under {component}",
                            )
                            continue
                        if _is_empty(row.get("evidence_ids")) and _is_empty(row.get("review_ids")):
                            _issue(
                                issues,
                                "error",
                                "target_score_subcomponent_missing_trace",
                                f"{ticker} {component}.{row.get('name', '')} needs evidence_ids or review_ids",
                            )
        action_state = str(target.get("action_state") or score.get("action_state") or "")
        dimensions = score.get("score_dimensions")
        if not isinstance(dimensions, dict):
            _issue(
                issues,
                "error",
                "target_missing_score_dimensions",
                f"{ticker} must preserve four core score_dimensions",
            )
        else:
            for dimension in TARGET_SCORE_DIMENSIONS:
                if _is_empty(dimensions.get(dimension)):
                    _issue(
                        issues,
                        "error",
                        "target_missing_score_dimension",
                        f"{ticker} is missing score_dimensions.{dimension}",
                    )
        if action_state == "actionable_long":
            kill_tests = target.get("thesis_kill_tests")
            if not isinstance(kill_tests, list) or not kill_tests:
                _issue(
                    issues,
                    "error",
                    "actionable_target_missing_kill_tests",
                    f"{ticker} actionable_long target needs hard thesis_kill_tests",
                )
            else:
                for kill_test in kill_tests:
                    if not isinstance(kill_test, dict) or any(
                        _is_empty(kill_test.get(field))
                        for field in ("test", "evidence_needed", "downgrade_action", "source_plan")
                    ):
                        _issue(
                            issues,
                            "error",
                            "target_invalid_kill_test",
                            f"{ticker} has an incomplete thesis_kill_test",
                        )

    return {
        "ok": not any(issue["severity"] == "error" for issue in issues),
        "summary": {"targets": len(targets)},
        "issues": issues,
    }


def validate_backtest_leakage_controls(
    qa_tree: dict[str, Any],
    source_extractions: list[dict[str, Any]],
    leaf_source_reviews: list[dict[str, Any]],
    targets: list[dict[str, Any]],
    sources: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Validate controls that reduce model-time and framework-time leakage in backtests."""
    issues: list[dict[str, str]] = []
    if str(qa_tree.get("run_mode") or "") != "historical_backtest":
        return {"ok": True, "summary": {"mode": qa_tree.get("run_mode", "")}, "issues": issues}

    as_of_date = str(qa_tree.get("as_of_date") or "")
    controls = qa_tree.get("anti_leakage_controls")
    if not isinstance(controls, dict):
        _issue(
            issues,
            "error",
            "missing_backtest_anti_leakage_controls",
            "historical backtests must declare anti_leakage_controls before QA, scoring, and labels are trusted",
        )
        controls = {}
    for field in BACKTEST_ANTI_LEAKAGE_REQUIRED_FIELDS:
        if _is_empty(controls.get(field)):
            _issue(
                issues,
                "error",
                "backtest_anti_leakage_control_missing_field",
                f"anti_leakage_controls is missing {field}",
            )
    if as_of_date and controls.get("as_of_date") and str(controls.get("as_of_date")) != as_of_date:
        _issue(
            issues,
            "error",
            "backtest_anti_leakage_as_of_mismatch",
            "anti_leakage_controls.as_of_date must match qa_tree.as_of_date",
        )
    if str(controls.get("llm_prior_policy") or "") != "model_prior_is_not_evidence":
        _issue(
            issues,
            "error",
            "backtest_llm_prior_policy_not_strict",
            "LLM prior knowledge must be explicitly marked as non-evidence in historical backtests",
        )
    if str(controls.get("label_isolation_policy") or "") != "labels_attached_after_frozen_recommendations_only":
        _issue(
            issues,
            "error",
            "backtest_label_policy_not_strict",
            "labels must be attached only after frozen recommendations and must not feed scoring",
        )

    thesis_source_ids = _cutoff_thesis_source_ids(sources or [], as_of_date)
    label_source_ids = {
        str(source.get("source_id") or source.get("id") or "")
        for source in (sources or [])
        if str(source.get("allowed_usage") or "") == "label_only"
    }
    review_by_id = {
        str(review.get("review_id")): review
        for review in leaf_source_reviews
        if isinstance(review, dict) and review.get("review_id")
    }
    extraction_by_id = {
        str(extraction.get("extraction_id")): extraction
        for extraction in source_extractions
        if isinstance(extraction, dict) and extraction.get("extraction_id")
    }
    source_ids = thesis_source_ids | label_source_ids

    for node in qa_tree.get("nodes", []) or []:
        if _level_number(node.get("level")) != 3:
            continue
        node_id = str(node.get("id") or "")
        grounding = node.get("backtest_grounding")
        if not isinstance(grounding, dict):
            _issue(
                issues,
                "error",
                "l3_missing_backtest_grounding",
                f"{node_id} must declare backtest_grounding for source-pack-only reasoning",
            )
            continue
        for field in L3_BACKTEST_GROUNDING_REQUIRED_FIELDS:
            if _is_empty(grounding.get(field)) and field != "non_source_claims":
                _issue(
                    issues,
                    "error",
                    "l3_backtest_grounding_missing_field",
                    f"{node_id} backtest_grounding is missing {field}",
                )
        if grounding.get("non_source_claims") not in ([], (), None):
            _issue(
                issues,
                "error",
                "l3_backtest_has_non_source_claims",
                f"{node_id} has non-source claims in a historical backtest",
            )
        if str(grounding.get("model_prior_policy") or "") != "hypothesis_only_not_scoring_evidence":
            _issue(
                issues,
                "error",
                "l3_model_prior_policy_not_strict",
                f"{node_id} model prior may not strengthen conclusions or scores",
            )
        allowed = {str(item) for item in grounding.get("allowed_source_ids", []) or [] if str(item)}
        node_sources = {str(item) for item in node.get("source_links", []) or [] if str(item)}
        if allowed != node_sources:
            _issue(
                issues,
                "error",
                "l3_grounding_source_mismatch",
                f"{node_id} backtest_grounding.allowed_source_ids must match source_links",
            )
        if label_source_ids & node_sources:
            _issue(
                issues,
                "error",
                "l3_uses_label_source",
                f"{node_id} must not use label-only sources in QA reasoning",
            )
        if thesis_source_ids and not node_sources <= thesis_source_ids:
            _issue(
                issues,
                "error",
                "l3_uses_non_cutoff_source",
                f"{node_id} source_links must be cutoff-visible thesis sources only",
            )

    for extraction_id, extraction in extraction_by_id.items():
        source_id = str(extraction.get("source_id") or "")
        if label_source_ids and source_id in label_source_ids:
            _issue(
                issues,
                "error",
                "source_extraction_uses_label_source",
                f"{extraction_id} must not parse label-only sources for L3 reasoning",
            )
        if thesis_source_ids and source_id not in thesis_source_ids:
            _issue(
                issues,
                "error",
                "source_extraction_uses_non_cutoff_source",
                f"{extraction_id} must use a cutoff-visible thesis source",
            )

    for target in targets:
        ticker = str(target.get("ticker") or target.get("name") or "")
        score = target.get("score") if isinstance(target.get("score"), dict) else {}
        subcomponents = target.get("score_subcomponents") or score.get("score_subcomponents") or {}
        if not isinstance(subcomponents, dict):
            continue
        for component, rows in subcomponents.items():
            for row in rows or []:
                if not isinstance(row, dict):
                    continue
                row_review_ids = [str(item) for item in row.get("review_ids", []) or [] if str(item)]
                row_evidence_ids = [str(item) for item in row.get("evidence_ids", []) or [] if str(item)]
                if not row_review_ids and not row_evidence_ids:
                    continue
                for review_id in row_review_ids:
                    review = review_by_id.get(review_id)
                    if review is None:
                        _issue(
                            issues,
                            "error",
                            "target_score_unknown_review_id",
                            f"{ticker} {component} references unknown review_id {review_id}",
                        )
                    elif review.get("allowed_to_strengthen_conclusion") is not True:
                        _issue(
                            issues,
                            "error",
                            "target_score_uses_unapproved_review",
                            f"{ticker} {component} uses review_id {review_id} that was not approved by GPT verification",
                        )
                if thesis_source_ids:
                    for evidence_id in row_evidence_ids:
                        if evidence_id not in thesis_source_ids:
                            _issue(
                                issues,
                                "error",
                                "target_score_uses_non_cutoff_evidence",
                                f"{ticker} {component} evidence_id {evidence_id} is not a cutoff-visible thesis source",
                            )
                for forbidden in ("forward_3m_return", "label_status", "end_price", "excess_return"):
                    if forbidden in str(row.get("rationale") or ""):
                        _issue(
                            issues,
                            "error",
                            "target_score_mentions_label_data",
                            f"{ticker} {component} score rationale must not mention label data",
                        )

    return {
        "ok": not any(issue["severity"] == "error" for issue in issues),
        "summary": {
            "mode": "historical_backtest",
            "thesis_sources": len(thesis_source_ids),
            "label_sources": len(label_source_ids),
            "targets": len(targets),
        },
        "issues": issues,
    }


def freeze_recommendations(
    recommendations: list[dict[str, Any]],
    *,
    as_of_date: str,
    frozen_at: str | None = None,
) -> dict[str, Any]:
    """Freeze as-of recommendations before any forward-return labels are attached."""
    frozen_targets = []
    label_keys = set(LABEL_TERMS) | {
        "label",
        "evaluation_date",
        "label_status",
        "price_source",
        "benchmark_return",
        "excess_return",
    }
    for index, target in enumerate(sorted(recommendations, key=lambda row: int(row.get("rank", 9999))), start=1):
        clean = {key: deepcopy(value) for key, value in target.items() if key not in label_keys}
        clean["rank"] = int(clean.get("rank") or index)
        frozen_targets.append(clean)
    return {
        "as_of_date": as_of_date,
        "frozen_at": frozen_at or _now_iso(),
        "label_status": "unattached",
        "targets": frozen_targets,
    }


def attach_forward_return_labels(
    frozen_recommendations: dict[str, Any],
    labels_by_ticker: dict[str, dict[str, Any]],
    *,
    attached_at: str | None = None,
) -> dict[str, Any]:
    """Attach forward-return labels without modifying frozen ranks or rationales."""
    labeled = deepcopy(frozen_recommendations)
    labeled["label_status"] = "attached"
    labeled["label_attach"] = {
        "attached_at": attached_at or _now_iso(),
        "rule": "labels are evaluation metadata only and must not alter frozen recommendations",
    }
    for target in labeled.get("targets", []):
        ticker = str(target.get("ticker", ""))
        target["label"] = deepcopy(labels_by_ticker.get(ticker, {"label_status": "missing"}))
    return labeled


def build_training_sample(
    labeled_recommendations: dict[str, Any],
    *,
    research_goal: str,
    benchmark: str | None = None,
) -> dict[str, Any]:
    """Build a machine-readable backtest sample from frozen recommendations and labels."""
    targets = []
    for target in labeled_recommendations.get("targets", []) or []:
        score = target.get("score", {})
        targets.append(
            {
                "ticker": target.get("ticker", ""),
                "name": target.get("name", ""),
                "rank": target.get("rank"),
                "thesis_node": target.get("thesis_node") or target.get("bottleneck_node", ""),
                "rationale": target.get("rationale", ""),
                "score_components": score.get("score_components", score),
                "thesis_confidence": score.get("thesis_confidence"),
                "payoff_convexity": score.get("payoff_convexity"),
                "label": deepcopy(target.get("label", {})),
            }
        )
    return {
        "research_goal": research_goal,
        "as_of_date": labeled_recommendations.get("as_of_date", ""),
        "benchmark": benchmark or "",
        "targets": targets,
    }


def build_prediction_review(
    labeled_recommendations: dict[str, Any],
    realized_facts_by_ticker: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Create a review scaffold that separates evidence failures from weighting mistakes."""
    reviews = []
    for target in labeled_recommendations.get("targets", []) or []:
        ticker = str(target.get("ticker", ""))
        facts = realized_facts_by_ticker.get(ticker, {})
        reviews.append(
            {
                "ticker": ticker,
                "rank": target.get("rank"),
                "initial_claim": target.get("rationale", ""),
                "label": deepcopy(target.get("label", {})),
                "current_status": facts.get("status", "needs_review"),
                "notes": list(facts.get("notes", []) or []),
                "failed_l3": list(facts.get("failed_l3", []) or []),
            }
        )
    return {
        "as_of_date": labeled_recommendations.get("as_of_date", ""),
        "review_questions": [
            "which_l3_was_falsified",
            "evidence_or_weight_error",
            "payoff_convexity_error",
            "time_window_mismatch",
            "lead_misused_as_evidence",
        ],
        "targets": reviews,
    }


def build_internal_workbench(
    *,
    source_extractions: list[dict[str, Any]],
    leaf_source_reviews: list[dict[str, Any]],
    scoring_worksheet: list[dict[str, Any]],
    validator_output: dict[str, Any],
    rejected_future_sources: list[dict[str, Any]],
    frozen_recommendations: dict[str, Any],
    label_attach: dict[str, Any],
) -> dict[str, Any]:
    """Bundle internal audit artifacts that should stay out of final HTML."""
    return {
        "source_extractions": deepcopy(source_extractions),
        "leaf_source_reviews": deepcopy(leaf_source_reviews),
        "scoring_worksheet": deepcopy(scoring_worksheet),
        "validator_output": deepcopy(validator_output),
        "rejected_future_sources": deepcopy(rejected_future_sources),
        "frozen_recommendations": deepcopy(frozen_recommendations),
        "label_attach": deepcopy(label_attach),
        "public_html_policy": "do_not_render_internal_trace_unless_user_requests_it",
    }


def get_domain_playbook(name: str) -> dict[str, Any]:
    """Return a reusable domain playbook for concrete L2/L3 question design."""
    key = name.strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "memory": "memory_industry",
        "storage": "memory_industry",
        "storage_industry": "memory_industry",
        "memory_storage": "memory_industry",
        "storage_memory": "memory_industry",
        "存储": "memory_industry",
        "存储行业": "memory_industry",
        "optical": "optical_module",
        "optical_module": "optical_module",
        "optical_transceiver": "optical_module",
        "光模块": "optical_module",
        "光通信": "optical_module",
    }
    key = aliases.get(key, key)
    return deepcopy(DOMAIN_PLAYBOOKS.get(key, DOMAIN_PLAYBOOKS["default"]))


def _section_positions(html: str) -> dict[str, int]:
    positions: dict[str, int] = {}
    for section in REPORT_SECTIONS:
        pos = _id_position(html, SECTION_IDS[section])
        if pos < 0:
            pos = html.find(section)
        if pos >= 0:
            positions[section] = pos
    return positions


def _id_position(html: str, ids: tuple[str, ...]) -> int:
    positions: list[int] = []
    for element_id in ids:
        for needle in (f'id="{element_id}"', f"id='{element_id}'"):
            pos = html.find(needle)
            if pos >= 0:
                positions.append(pos)
    return min(positions) if positions else -1


def _class_count(html: str, *classes: str) -> int:
    count = 0
    for match in re.finditer(r"class\s*=\s*(['\"])(.*?)\1", html, flags=re.IGNORECASE | re.DOTALL):
        class_set = set(match.group(2).split())
        if all(class_name in class_set for class_name in classes):
            count += 1
    return count


def _tag_class_count(html: str, tag: str, *classes: str) -> int:
    count = 0
    pattern = rf"<{re.escape(tag)}\b[^>]*class\s*=\s*(['\"])(.*?)\1"
    for match in re.finditer(pattern, html, flags=re.IGNORECASE | re.DOTALL):
        class_set = set(match.group(2).split())
        if all(class_name in class_set for class_name in classes):
            count += 1
    return count


def _tag_count(html: str, tag: str) -> int:
    return len(re.findall(rf"<{re.escape(tag)}\b", html, flags=re.IGNORECASE))


def _first_position(text: str, needles: list[str]) -> int:
    positions = [text.find(needle) for needle in needles if text.find(needle) >= 0]
    return min(positions) if positions else -1


def _level_number(value: Any) -> int:
    if isinstance(value, int):
        return value
    text = str(value or "").strip().lower()
    if text.startswith("level-"):
        text = text.split("-", 1)[1]
    try:
        return int(text)
    except ValueError:
        return 0


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, tuple, dict, set)):
        return len(value) == 0
    return False


def _normalized_logic_text(value: Any) -> str:
    if isinstance(value, dict):
        parts = [f"{key}:{_normalized_logic_text(val)}" for key, val in sorted(value.items())]
        text = " ".join(parts)
    elif isinstance(value, (list, tuple, set)):
        text = " ".join(_normalized_logic_text(item) for item in value)
    else:
        text = str(value or "")
    text = unescape(text).lower()
    return re.sub(r"\s+", " ", text).strip()


def _cutoff_thesis_source_ids(sources: list[dict[str, Any]], as_of_date: str) -> set[str]:
    cutoff = _parse_date(as_of_date)
    source_ids: set[str] = set()
    for source in sources:
        source_id = str(source.get("source_id") or source.get("id") or "")
        if not source_id:
            continue
        if str(source.get("allowed_usage") or "thesis") in {"label_only", "quarantined"}:
            continue
        visible_at = _parse_date(str(source.get("source_visible_at") or source.get("published_at") or ""))
        if cutoff and visible_at and visible_at > cutoff:
            continue
        source_ids.add(source_id)
    return source_ids


def _validate_l3_source_plan(node: dict[str, Any], node_id: str, issues: list[dict[str, str]]) -> None:
    source_plan = node.get("source_plan")
    if _is_empty(source_plan):
        return
    if not isinstance(source_plan, (list, tuple, dict)):
        _issue(
            issues,
            "error",
            "l3_source_plan_not_structured",
            f"{node_id} source_plan must be structured by source, cutoff, bucket, and intended use",
        )


def _validate_l3_skill_dispatch(node: dict[str, Any], node_id: str, issues: list[dict[str, str]]) -> None:
    dispatch = node.get("skill_dispatch")
    if _is_empty(dispatch):
        return
    if not isinstance(dispatch, dict):
        _issue(
            issues,
            "error",
            "l3_skill_dispatch_not_structured",
            f"{node_id} skill_dispatch must be a structured object, not a bare skill name",
        )
        return

    for field in L3_SKILL_DISPATCH_REQUIRED_FIELDS:
        if _is_empty(dispatch.get(field)):
            _issue(
                issues,
                "error",
                "l3_skill_dispatch_missing_field",
                f"{node_id} skill_dispatch is missing {field}",
            )

    selected_skill = str(dispatch.get("selected_skill") or "").strip()
    if selected_skill and selected_skill not in KNOWN_SPECIALTY_SKILLS:
        _issue(
            issues,
            "error",
            "l3_unknown_specialty_skill",
            f"{node_id} selected unknown specialty skill {selected_skill}",
        )


def _validate_l3_score_component(node: dict[str, Any], node_id: str, issues: list[dict[str, str]]) -> None:
    score_component = node.get("score_component")
    if _is_empty(score_component):
        return
    if isinstance(score_component, str):
        components = [score_component]
    elif isinstance(score_component, (list, tuple, set)):
        components = [str(item) for item in score_component]
    else:
        _issue(
            issues,
            "error",
            "l3_score_component_not_parseable",
            f"{node_id} score_component must be a string or list of strings",
        )
        return

    for component in components:
        normalized = component.strip()
        if normalized and normalized not in L3_SCORE_COMPONENTS:
            _issue(
                issues,
                "error",
                "l3_invalid_score_component",
                f"{node_id} uses unknown score_component {normalized}",
            )


def _parse_date(value: str) -> datetime | None:
    if not value:
        return None
    normalized = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


def _score_value(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(5.0, score))


def _score_from_subcomponents(
    component: str,
    target: dict[str, Any],
    default_score: float,
    audit_out: dict[str, list[dict[str, Any]]],
) -> float:
    score_subcomponents = target.get("score_subcomponents")
    rows = score_subcomponents.get(component) if isinstance(score_subcomponents, dict) else None
    evidence_ids = target.get("score_evidence_ids") or target.get("evidence_ids") or []
    review_ids = target.get("score_review_ids") or target.get("review_ids") or []
    if not isinstance(rows, list) or not rows:
        audit_out[component] = [
            {
                "name": "direct_component_score",
                "score": round(default_score, 3),
                "weight": 1.0,
                "evidence_ids": deepcopy(evidence_ids),
                "review_ids": deepcopy(review_ids),
                "status": "direct_score_without_subcomponent_formula",
            }
        ]
        return round(default_score, 3)

    normalized_rows: list[dict[str, Any]] = []
    total_weight = 0.0
    weighted_score = 0.0
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            continue
        score = _score_value(row.get("score"))
        weight = _optional_float(row.get("weight"))
        if weight is None or weight <= 0:
            weight = 1.0
        total_weight += weight
        weighted_score += score * weight
        normalized_rows.append(
            {
                "name": str(row.get("name") or f"{component}_{index}"),
                "score": round(score, 3),
                "weight": round(weight, 3),
                "evidence_ids": deepcopy(row.get("evidence_ids") or evidence_ids),
                "review_ids": deepcopy(row.get("review_ids") or review_ids),
                "rationale": row.get("rationale", ""),
                "status": row.get("status", "scored"),
            }
        )
    if not normalized_rows or total_weight <= 0:
        audit_out[component] = [
            {
                "name": "direct_component_score",
                "score": round(default_score, 3),
                "weight": 1.0,
                "evidence_ids": deepcopy(evidence_ids),
                "review_ids": deepcopy(review_ids),
                "status": "invalid_subcomponents_fallback",
            }
        ]
        return round(default_score, 3)
    audit_out[component] = normalized_rows
    return round(weighted_score / total_weight, 3)


def _opportunity_gate(
    target: dict[str, Any],
    components: dict[str, float],
    thesis_confidence: float,
    payoff_convexity: float,
) -> dict[str, Any]:
    demand_visibility = _score_value(target.get("demand_visibility", components["future_space"]))
    irreplaceability = _score_value(target.get("irreplaceability", components["chokepoint_strength"]))
    market_underpricing = _score_value(target.get("market_underpricing", components["valuation_odds"]))
    opportunity_fit = round(
        demand_visibility * 0.30 + irreplaceability * 0.40 + market_underpricing * 0.30,
        3,
    )
    gate_reasons: list[str] = []
    max_total_score = 5.0

    if demand_visibility < 3.5:
        gate_reasons.append("future_demand_below_gate")
        max_total_score = min(max_total_score, 3.49)
    if irreplaceability < 3.8:
        gate_reasons.append("scarcity_or_irreplaceability_below_gate")
        max_total_score = min(max_total_score, 2.69 if irreplaceability < 3.0 else 3.49)
    if market_underpricing < 3.2:
        gate_reasons.append("market_underpricing_below_gate")
        max_total_score = min(max_total_score, 2.69 if market_underpricing < 2.5 else 3.49)
    if components["evidence_quality"] < 2.5:
        gate_reasons.append("evidence_quality_below_gate")
        max_total_score = min(max_total_score, 3.49)
    if components["disconfirming_risk_control"] < 2.5:
        gate_reasons.append("disconfirming_risk_control_below_gate")
        max_total_score = min(max_total_score, 3.49)

    valuation_status = str(target.get("valuation_status", "")).strip().lower()
    if valuation_status in {"missing", "stale", "unverified", "incomplete"}:
        gate_reasons.append("valuation_unverified")
        max_total_score = min(max_total_score, 3.49)

    expected_excess_return = _optional_float(target.get("expected_excess_return"))
    if expected_excess_return is not None and expected_excess_return <= 0:
        gate_reasons.append("expected_excess_return_not_positive")
        max_total_score = min(max_total_score, 2.69)

    if max_total_score <= 2.69 or opportunity_fit < 3.0:
        action_state = "no_action"
    elif gate_reasons:
        action_state = "watch_only"
    elif opportunity_fit >= 3.8 and thesis_confidence >= 3.5 and payoff_convexity >= 3.2:
        action_state = "actionable_long"
    else:
        action_state = "watch_only"

    return {
        "opportunity_fit": opportunity_fit,
        "action_state": action_state,
        "gate_reasons": gate_reasons,
        "max_total_score": max_total_score,
    }


def _target_score_dimensions(target: dict[str, Any], components: dict[str, float]) -> dict[str, float]:
    scarcity = _blend_scores(
        [
            (components["chokepoint_strength"], 0.70),
            (_score_value(target.get("irreplaceability", components["chokepoint_strength"])), 0.30),
        ]
    )
    mispricing = _blend_scores(
        [
            (components["valuation_odds"], 0.70),
            (_score_value(target.get("market_underpricing", components["valuation_odds"])), 0.30),
        ]
    )
    earnings_elasticity = _blend_scores(
        [
            (components["future_space"], 0.40),
            (components["payoff_convexity"], 0.40),
            (_score_value(target.get("catalyst_proximity", components["payoff_convexity"])), 0.20),
        ]
    )
    risk_control = _blend_scores(
        [
            (components["disconfirming_risk_control"], 0.40),
            (components["evidence_quality"], 0.35),
            (components["monitorability"], 0.25),
        ]
    )
    return {
        "scarcity_or_monopoly": scarcity,
        "mispricing": mispricing,
        "earnings_elasticity": earnings_elasticity,
        "risk_control": risk_control,
    }


def _blend_scores(weighted_scores: list[tuple[float, float]]) -> float:
    total_weight = sum(weight for _, weight in weighted_scores)
    if total_weight <= 0:
        return 0.0
    return round(sum(score * weight for score, weight in weighted_scores) / total_weight, 3)


def _optional_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _strength_bucket(total_score: float, thesis_confidence: float, payoff_convexity: float) -> str:
    if total_score >= 4.2 and thesis_confidence >= 4.0:
        return "A"
    if total_score >= 3.5 and (thesis_confidence >= 3.3 or payoff_convexity >= 4.0):
        return "B"
    if total_score >= 2.7:
        return "C"
    return "D"


def _issue(issues: list[dict[str, str]], severity: str, code: str, message: str) -> None:
    issues.append({"severity": severity, "code": code, "message": unescape(message)})


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
