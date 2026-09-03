from __future__ import annotations

import re
from copy import deepcopy
from datetime import datetime, timezone
from html import unescape
from typing import Any


REPORT_SECTIONS = ["当前研究的问题", "行业概况", "标的推荐", "来源索引"]
QA_BLOCK_TITLES = ["1. 当前结论呈现", "2. 问题展开（子 QA）", "3. 待补充的问题"]
MAX_QA_DEPTH = 5
RESEARCH_UNIT_MIN_LEVEL = 3
SECTION_IDS = {
    REPORT_SECTIONS[0]: ("goal", "research-goal", "current-research-goal"),
    REPORT_SECTIONS[1]: ("overview", "industry-overview", "chain", "supply-chain", "industry-chain"),
    REPORT_SECTIONS[2]: ("targets", "target-recommendations", "final-target-recommendations"),
    REPORT_SECTIONS[3]: ("sources", "source-index"),
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

INDUSTRY_SPACE_SOURCE_SEARCH_CATEGORIES = [
    ("company_guidance", "公司指引"),
    ("company_tam", "公司 TAM"),
    ("customer_guidance", "客户侧指引"),
    ("third_party", "第三方拆法"),
    ("financial_evidence", "财务兑现证据"),
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


def validate_research_plan_markdown_contract(
    markdown: str,
    *,
    plans: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate the runtime-growing L3-to-terminal Markdown research plan."""

    issues: list[dict[str, str]] = []
    if "<!-- research-plan-contract: dynamic-question-tree-v4 -->" not in markdown:
        _issue(
            issues,
            "error",
            "missing_research_plan_scope",
            "research_plan.md must declare the dynamic-question-tree-v4 contract.",
        )
    if "最多下钻到 L5" not in markdown:
        _issue(
            issues,
            "error",
            "missing_maximum_plan_depth",
            "research_plan.md must state that the question tree stops at L5.",
        )
    if "需要搜集的数据" not in markdown or "需要做的分析" not in markdown:
        _issue(
            issues,
            "error",
            "missing_leaf_execution_fields",
            "research_plan.md must show required data and analysis for leaves.",
        )
    if "初始只到 L3" not in markdown or "才新增下一层" not in markdown:
        _issue(
            issues,
            "error",
            "missing_dynamic_expansion_rule",
            "research_plan.md must state the L3-first, evidence-triggered expansion rule.",
        )
    for level_label in ("L1 ·", "L2 ·", "L3 ·"):
        if level_label not in markdown:
            _issue(
                issues,
                "error",
                "missing_question_hierarchy_level",
                f"research_plan.md must visibly include {level_label.strip()} in the hierarchy.",
            )

    expected_leaf_ids = [
        str(step.get("question_node_id") or step.get("leaf_question_id") or "")
        for plan in plans
        for step in plan.get("steps") or []
        if str(step.get("question_node_id") or step.get("leaf_question_id") or "")
    ]
    rendered_l3_ids = re.findall(r"<!-- l3-plan-id:([^>]+) -->", markdown)
    rendered_leaf_ids = re.findall(r"<!-- active-question-id:([^>]+) -->", markdown)
    rendered_l3 = len(rendered_l3_ids)
    rendered_leaves = len(rendered_leaf_ids)
    if rendered_l3 != len(plans):
        _issue(
            issues,
            "error",
            "research_plan_l3_count_mismatch",
            f"Expected {len(plans)} L3 plans, found {rendered_l3}.",
        )
    if rendered_leaves != len(expected_leaf_ids):
        _issue(
            issues,
            "error",
            "research_plan_leaf_count_mismatch",
            f"Expected {len(expected_leaf_ids)} terminal leaves, found {rendered_leaves}.",
        )
    if markdown.count("**需要搜集的数据：**") != len(expected_leaf_ids):
        _issue(
            issues,
            "error",
            "research_plan_leaf_data_count_mismatch",
            "Every current terminal question must render exactly one required-data entry.",
        )
    if markdown.count("**需要做的分析：**") != len(expected_leaf_ids):
        _issue(
            issues,
            "error",
            "research_plan_leaf_analysis_count_mismatch",
            "Every current terminal question must render exactly one analysis entry.",
        )
    for plan in plans:
        plan_id = str(plan.get("plan_id") or "")
        if plan_id and plan_id not in rendered_l3_ids:
            _issue(
                issues,
                "error",
                "missing_rendered_l3_plan",
                f"Missing rendered L3 plan {plan.get('plan_id')!s}.",
            )
    for leaf_id in expected_leaf_ids:
        if leaf_id not in rendered_leaf_ids:
            _issue(
                issues,
                "error",
                "missing_rendered_leaf_question",
                f"Missing rendered current terminal question {leaf_id}.",
            )
    return {
        "ok": not any(issue["severity"] == "error" for issue in issues),
        "issues": issues,
        "summary": {
            "l3_plans": rendered_l3,
            "leaf_steps": rendered_leaves,
        },
    }

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
    "event-to-investment-analysis",
    "conference-transcript-analysis",
    "supply-chain-chokepoint-analysis",
    "company-exposure-analysis",
    "news-event-analysis",
    "opinion-analysis",
    "leaf-research-deepseek",
    "target-recommendation-analysis",
    "target-ranking-analysis",
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
            "Q1": "Technology feasibility: why this S-curve may become real rather than remain a concept",
            "Q2": "Industry space and S-curve stage: whether demand is entering early acceleration and future space is large enough",
            "Q3": "Technical chain and BOM presentation: who sits on the chain, what each node does, and where supply-demand tension may appear",
            "Q4": "Target observation list: companies directly exposed to the S-curve, with watch intensity and verification triggers",
        },
        "mechanism_buckets": [
            "technology_feasibility",
            "adoption_inflection",
            "industry_space",
            "s_curve_stage",
            "simple_bom_map",
            "supply_demand_tension",
            "company_exposure_screen",
            "kill_tests",
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
            "Q1": "Technology feasibility: why the memory/storage S-curve may become real rather than remain a cycle call",
            "Q2": "Industry space and S-curve stage: whether AI/data-center demand is entering early acceleration and future space is large enough",
            "Q3": "Technical chain and BOM presentation: HBM, DRAM, NAND/eSSD, HDD, controllers, equipment, and customers, with supply-demand tension only as a first-pass flag",
            "Q4": "Target observation list: memory/storage companies directly exposed to the S-curve, with watch intensity and verification triggers",
        },
        "mechanism_buckets": [
            "technology_feasibility",
            "adoption_inflection",
            "industry_space",
            "s_curve_stage",
            "simple_bom_map",
            "supply_demand_tension",
            "company_exposure_screen",
            "kill_tests",
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
            "Q1": "Technology feasibility: why optical interconnect demand may become a real S-curve rather than a one-cycle upgrade",
            "Q2": "Industry space and S-curve stage: whether AI cluster networking is entering early acceleration and future space is large enough",
            "Q3": "Technical chain and BOM presentation: lasers, optical chips, DSP/driver/TIA, modules, manufacturing, switches, and customers, with supply-demand tension only as a first-pass flag",
            "Q4": "Target observation list: optical-chain companies directly exposed to the S-curve, with watch intensity and verification triggers",
        },
        "mechanism_buckets": [
            "technology_feasibility",
            "adoption_inflection",
            "industry_space",
            "s_curve_stage",
            "simple_bom_map",
            "supply_demand_tension",
            "company_exposure_screen",
            "kill_tests",
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
    "event_conference": {
        "research_type": "event/policy or technology/product-route event",
        "q_map": {
            "Q1": "Fact boundary: what did the event actually confirm, and what is only roadmap or marketing language?",
            "Q2": "Transmission and chokepoints: which supply-chain nodes can convert the event into orders, revenue, margin, and cash flow?",
            "Q3": "Disconfirming tests and priced-in risk: what would show the event is delayed, non-material, substitutable, or already fully priced?",
            "Q4": "Target observation list: which specific securities have direct exposure, favorable odds, monitorable triggers, and controlled downside?",
        },
        "mechanism_buckets": [
            "official_fact_boundary",
            "new_information_delta",
            "commercialization_stage",
            "event_to_order_revenue_margin_bridge",
            "supply_chain_chokepoint",
            "company_exposure_and_financial_conversion",
            "market_pricing_bridge",
            "disconfirming_and_kill_tests",
            "specific_target_ranking",
        ],
        "mechanism_depth_blocks": [
            "event_fact_boundary",
            "new_information_delta",
            "transmission_chain",
            "supply_or_access_response",
            "unit_economics_profit_bridge",
            "competitive_value_capture_map",
            "market_pricing_bridge",
            "disconfirming_counter_supply_tests",
            "target_ranking",
        ],
        "required_extraction_schemas": [
            "event_fact_boundary",
            "conference_claim_quality",
            "event_transmission_chain",
            "chokepoint_scorecard",
            "company_exposure_bridge",
            "event_valuation_odds",
            "target_ranking_worksheet",
        ],
        "scoring_adjustments": {
            "future_space": "use only event claims that connect to customer demand, product availability, shipment timing, or adoption duration",
            "chokepoint_strength": "require an explicit scarce node; event partner lists without scarcity are only leads",
            "valuation_odds": "test whether the event delta is already embedded in market expectations",
            "evidence_quality": "separate official fact, roadmap, customer logo, third-party lead, and market interpretation",
            "disconfirming_risk_control": "bind each target to launch timing, order conversion, customer capex, substitution, and valuation kill tests",
        },
        "depth_quality_rule": "event research is too shallow if it only summarizes announcements; it must parse the event fact boundary, bridge the event to orders/revenue/margin/FCF, test chokepoints, verify company exposure, reverse priced-in expectations, and rank specific targets with kill tests",
        "default_score_schema": SCORE_WEIGHTS,
    },
    "default": {
        "research_type": "custom",
        "q_map": {
            "Q1": "Technology feasibility: why this S-curve may become real",
            "Q2": "Industry space and S-curve stage: how large the future space may be and where the curve sits now",
            "Q3": "Technical chain and BOM presentation: who is on the chain and what each node does",
            "Q4": "Target observation list and monitoring plan",
        },
        "mechanism_buckets": [
            "technology_feasibility",
            "adoption_inflection",
            "industry_space",
            "s_curve_stage",
            "simple_bom_map",
            "company_exposure_screen",
            "kill_tests",
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
    report_scope = _report_scope(html)
    if report_scope == "standalone-bom":
        return _validate_standalone_bom_report_html(html, mode=mode)
    if report_scope in {"industry-index", "bom-node"}:
        return _validate_split_scope_report_html(html, report_scope=report_scope, mode=mode)

    issues: list[dict[str, str]] = []
    section_positions = _section_positions(html)
    found_sections = [section for section in REPORT_SECTIONS if section in section_positions]
    if found_sections != REPORT_SECTIONS:
        _issue(issues, "error", "top_level_sections", "final HTML must use the locked four-section order")
    else:
        positions = [section_positions[section] for section in REPORT_SECTIONS]
        if positions != sorted(positions):
            _issue(issues, "error", "top_level_order", "top-level sections are out of order")

    level_counts = _qa_level_counts(html)
    has_public_qa = _first_position(
        html,
        ['id="qa"', "id='qa'", 'class="qa-section', "class='qa-section"],
    ) >= 0
    if has_public_qa:
        if level_counts["level1_cards"] == 0:
            _issue(issues, "error", "missing_level1_cards", "下钻 QA must render Q1-Q4 as qa-card level-1")
        if level_counts["level2_cards"] == 0:
            _issue(issues, "error", "missing_level2_cards", "L1 cards must render mechanism buckets as qa-card level-2")
        if require_l3 and level_counts["level3_cards"] == 0:
            _issue(issues, "error", "missing_level3_cards", "complete refreshed reports must render L3 leaves")

    interactive_level_counts = _interactive_qa_level_counts(html)
    if any(
        interactive_level_counts[f"interactive_level{level}_cards"] != level_counts[f"level{level}_cards"]
        for level in range(1, MAX_QA_DEPTH + 1)
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

    industry_overview_sections = _class_count(html, "industry-overview-section")
    if industry_overview_sections == 0:
        _issue(
            issues,
            "error",
            "missing_industry_overview_section",
            "final HTML must include a standalone 行业概况 section before 标的推荐",
        )
    supply_chain_sections = _class_count(html, "supply-chain-section")
    if supply_chain_sections == 0:
        _issue(
            issues,
            "error",
            "missing_supply_chain_section",
            "行业概况 must include a 技术链与 BOM 呈现 module before 标的推荐",
        )
    required_industry_overview_classes = [
        "industry-overview-section",
        "industry-module",
        "industry-module-body",
        "module-index",
        "supply-chain-section",
        "component-value-chain",
        "bom-research-module",
        "bom-node-brief",
        "bom-question-list",
        "bom-question-card",
        "bom-question-index",
        "bom-question-answer",
        "bom-question-sources",
    ]
    missing_industry_overview_classes = [
        class_name for class_name in required_industry_overview_classes if _class_count(html, class_name) == 0
    ]
    if missing_industry_overview_classes:
        _issue(
            issues,
            "error",
            "missing_industry_overview_components",
            "行业概况 must include the technical-chain/BOM presentation module; missing "
            + ", ".join(missing_industry_overview_classes),
        )
    if _class_count(html, "overview-source-plan") or _class_count(html, "source-universe-plan") or _class_count(html, "exa-search-plan"):
        _issue(
            issues,
            "error",
            "public_source_plan_leak",
            "source_universe_plan and exa_search_plan belong to internal artifacts and must not render in final public HTML",
        )
    if _class_count(html, "bom-taxonomy") and _class_count(html, "bom-taxonomy-card") < 2:
        _issue(
            issues,
            "error",
            "incomplete_bom_taxonomy",
            "统一 BOM 口径 must render at least two bom-taxonomy-card definitions so the technical chain and S-curve space share visible node names",
        )
    bom_taxonomy_nodes = _bom_taxonomy_nodes(html)
    if bom_taxonomy_nodes:
        coverage_regions = {
            "S曲线与产业空间": _class_region(html, ("industry-module", "industry-space"), [("industry-module", "industry-competition"), ("industry-module", "industry-chokepoints"), ("industry-module", "industry-key-variables")]),
        }
        for module_name, region in coverage_regions.items():
            missing_nodes = _missing_taxonomy_nodes(region, bom_taxonomy_nodes)
            if missing_nodes:
                _issue(
                    issues,
                    "warn",
                    "missing_bom_taxonomy_coverage",
                    f"{module_name} should reuse the 技术链与 BOM node names where relevant; missing "
                    + ", ".join(missing_nodes),
                )
    required_industry_detail_modules = [
        "supply-chain-section",
    ]
    static_industry_modules = [
        class_name
        for class_name in required_industry_detail_modules
        if _tag_class_count(html, "details", "industry-module", class_name) == 0
    ]
    if static_industry_modules:
        _issue(
            issues,
            "error",
            "missing_interactive_industry_modules",
            "行业概况 modules must render as clickable details.industry-module nodes, not always-expanded static sections; missing "
            + ", ".join(static_industry_modules),
        )
    bom_research_modules = _tag_class_count(html, "details", "industry-module", "bom-research-module")
    if bom_research_modules == 0:
        _issue(
            issues,
            "error",
            "missing_bom_research_modules",
            "行业概况 must expand each BOM node into a clickable details.industry-module.bom-research-module starting from module 02",
        )
    bom_question_cards = _tag_class_count(html, "details", "bom-question-card")
    if bom_research_modules and bom_question_cards < bom_research_modules * 6:
        _issue(
            issues,
            "error",
            "missing_bom_six_question_cards",
            "Each BOM research module must embed six collapsible bom-question-card submodules",
        )
    missing_bom_question_labels = [
        label
        for label in [
            "当前 BOM 的需求是否会被 S 曲线放大拉动？",
            "供给能否跟上？",
            "谁控制供给？",
            "是否已经财务兑现？",
            "市场是否已定价？",
            "反证是什么？",
        ]
        if label not in html
    ]
    if bom_research_modules and missing_bom_question_labels:
        _issue(
            issues,
            "error",
            "missing_bom_six_question_labels",
            "BOM research modules must keep the six core investment questions; missing "
            + ", ".join(missing_bom_question_labels),
        )
    if _class_count(html, "bom-question-stage-flow") or _class_count(html, "bom-question-four-step"):
        missing_bom_stage_flow_titles = [
            title
            for title in [
                "研究逻辑链",
                "Metric 历史与现状",
                "市场的未来预期",
                "第一性原理评估",
                "本问结论",
                "对标的推荐的影响",
            ]
            if title not in html
        ]
        if missing_bom_stage_flow_titles:
            _issue(
                issues,
                "error",
                "missing_bom_stage_flow_titles",
                "BOM question cards must use the locked stage-flow titles; missing "
                + ", ".join(missing_bom_stage_flow_titles),
            )
        logic_row_count = _class_count(html, "bom-logic-chain-row")
        integrated_stage_count = _class_count(html, "bom-stage-integrated-card")
        if logic_row_count < bom_question_cards * 4:
            _issue(
                issues,
                "error",
                "insufficient_bom_logic_chain_rows",
                "Each bom-question-card must compile its judgment rule and several concrete causal rows into one research-logic card",
            )
        if integrated_stage_count < bom_question_cards * 4:
            _issue(
                issues,
                "error",
                "insufficient_bom_stage_integrated_cards",
                "Each bom-question-card must render one integrated stage card per logic-chain row, combining metric history, market expectation, and first-principles assessment",
            )
        if logic_row_count != integrated_stage_count:
            _issue(
                issues,
                "error",
                "bom_logic_stage_count_mismatch",
                "Every public research-logic row must map one-to-one to an integrated evidence stage card",
            )
        if _class_count(html, "bom-step-research-logic") < bom_question_cards:
            _issue(
                issues,
                "error",
                "missing_bom_step_research_logic",
                "Each bom-question-card must compile the question-specific model, formula, conclusion rule, and causal stages into one research-logic card",
            )
        if _class_count(html, "bom-step-model") or _class_count(html, "bom-step-logic"):
            _issue(
                issues,
                "error",
                "legacy_split_bom_research_logic",
                "Public BOM questions must not render separate judgment-model and concrete-logic cards",
            )
        if _class_count(html, "bom-step-question-conclusion") < bom_question_cards:
            _issue(
                issues,
                "error",
                "missing_bom_step_question_conclusion",
                "Each bom-question-card must render the question conclusion after the per-stage evidence cards",
            )
        if _class_count(html, "bom-step-target-impact") < bom_question_cards:
            _issue(
                issues,
                "error",
                "missing_bom_step_target_impact",
                "Each bom-question-card must render target-recommendation impact after the question conclusion",
            )
        if integrated_stage_count and _class_count(html, "bom-stage-subcard") < integrated_stage_count * 3:
            _issue(
                issues,
                "error",
                "insufficient_bom_stage_subcards",
                "Each integrated stage card must contain metric history/current state, market future expectation, and first-principles subcards",
            )
        search_status_count = _class_count(html, "bom-question-research-status")
        search_status_details_count = _tag_class_count(html, "details", "bom-question-research-status")
        if search_status_count < bom_question_cards:
            _issue(
                issues,
                "error",
                "missing_bom_question_search_status",
                "Each bom-question-card must start with a compact search/evidence status before the verdict; local caches cannot replace question-level search artifacts",
            )
        if search_status_count and search_status_details_count != search_status_count:
            _issue(
                issues,
                "error",
                "static_bom_question_search_status",
                "BOM question search/evidence status must render as collapsed details cards",
            )
        if _open_details_class_count(html, "bom-question-research-status"):
            _issue(
                issues,
                "error",
                "expanded_bom_question_search_status",
                "BOM question search/evidence status cards must be collapsed by default",
            )
        stage_card_count = _class_count(html, "bom-s-curve-stage-card")
        stage_card_details_count = _tag_class_count(html, "details", "bom-s-curve-stage-card")
        if bom_research_modules and stage_card_count < bom_research_modules:
            _issue(
                issues,
                "error",
                "missing_bom_s_curve_stage_rollup",
                "Each BOM research module must render one S-curve stage rollup only after its six question cards are complete",
            )
        if stage_card_count and stage_card_details_count != stage_card_count:
            _issue(
                issues,
                "error",
                "static_bom_s_curve_stage_rollup",
                "BOM S-curve stage rollups must render as collapsed details cards",
            )
        if _open_details_class_count(html, "bom-s-curve-stage-card"):
            _issue(
                issues,
                "error",
                "expanded_bom_s_curve_stage_rollup",
                "BOM S-curve stage rollups must be collapsed by default because they are nested rollups",
            )
        for required_class in [
            "bom-stage-current",
            "bom-stage-evidence-grid",
            "bom-stage-next-signal",
            "bom-stage-downgrade-signal",
            "bom-stage-source-discipline",
        ]:
            if stage_card_count and _class_count(html, required_class) == 0:
                _issue(
                    issues,
                    "error",
                    f"missing_{required_class.replace('-', '_')}",
                    "BOM S-curve stage rollups must include current stage, six-question evidence, next confirmation signal, downgrade signal, and source discipline",
                )
        nested_bom_details_requirements = [
            ("bom-step-card", bom_question_cards * 7),
            ("bom-step-research-logic", bom_question_cards),
            ("bom-stage-integrated-card", bom_question_cards * 4),
            ("bom-stage-subcard", bom_question_cards * 12),
            ("bom-mechanism-card", bom_question_cards * 8),
            ("bom-step-question-conclusion", bom_question_cards),
            ("bom-step-target-impact", bom_question_cards),
        ]
        for class_name, minimum_count in nested_bom_details_requirements:
            class_count = _class_count(html, class_name)
            details_count = _tag_class_count(html, "details", class_name)
            if class_count < minimum_count:
                _issue(
                    issues,
                    "error",
                    f"insufficient_{class_name.replace('-', '_')}",
                    f"Nested BOM structure {class_name} must render enough collapsed detail nodes; expected at least {minimum_count}, found {class_count}",
                )
            if class_count and details_count != class_count:
                _issue(
                    issues,
                    "error",
                    f"static_{class_name.replace('-', '_')}",
                    f"Nested BOM structure {class_name} must render as clickable details cards with summary headers",
                )
            open_count = _open_details_class_count(html, class_name)
            if open_count:
                _issue(
                    issues,
                    "error",
                    f"expanded_{class_name.replace('-', '_')}",
                    f"Nested BOM structure {class_name} must be collapsed by default so users can scan nested titles before opening details",
                )
        if not (_class_count(html, "metric-point-count") or _class_count(html, "metric-trend-gap")):
            _issue(
                issues,
                "error",
                "missing_metric_point_count_or_gap",
                "BOM metric history must show point counts for curves or explicit metric-trend-gap when fewer than five same-metric points are available",
            )
        if _class_count(html, "metric-history-table") == 0:
            _issue(
                issues,
                "error",
                "missing_metric_history_table",
                "BOM metric history must directly render metric-level data tables inside Metric 历史与现状",
            )
        if _class_count(html, "metric-history-table") and "实际时间" not in html:
            _issue(
                issues,
                "error",
                "missing_metric_history_calendar_time_column",
                "BOM metric history tables must map reported fiscal period labels into an actual calendar-time column",
            )
        if _class_count(html, "metric-history-caption") == 0:
            _issue(
                issues,
                "error",
                "missing_metric_history_caption",
                "BOM metric history tables must put the metric name and definition once in a table caption instead of repeating them on every data row",
            )
        if _class_count(html, "metric-history-name") == 0:
            _issue(
                issues,
                "error",
                "missing_metric_history_name_link",
                "BOM metric history captions must expose the concrete metric name as a source-linked metric-history-name",
            )
        if _class_count(html, "metric-name-cell") > 0:
            _issue(
                issues,
                "error",
                "legacy_repeated_metric_name_cells",
                "BOM metric history tables must not repeat the Metric column on every row; use metric-history-caption instead",
            )
        if _class_count(html, "bom-expectation-table") == 0:
            _issue(
                issues,
                "error",
                "missing_bom_expectation_table",
                "BOM future expectation subcards must directly render entity expectation tables",
            )
        if _class_count(html, "bom-expectation-table") and (
            "现状实际时间" not in html or "指引实际时间" not in html
        ):
            _issue(
                issues,
                "error",
                "missing_expectation_calendar_time_columns",
                "BOM expectation tables must map fiscal period labels into calendar time columns: 现状实际时间 and 指引实际时间",
            )
    elif bom_question_cards:
        _issue(
            issues,
            "warn",
            "legacy_bom_question_structure",
            "BOM question cards use a legacy structure; refreshed reports should use bom-question-stage-flow with logic-chain tables and integrated per-link history, expectation, and mechanism cards",
        )
    competition_region = _class_region(html, ("industry-module", "industry-competition"), [("industry-module", "industry-chokepoints")])
    if _class_count(html, "industry-competition") and (
        _tag_class_count(html, "details", "competition-bom-card") < 1
        or _class_count(html, "competition-question-grid") == 0
        or _class_count(html, "profit-pool-table") == 0
        or _class_count(html, "overview-question-card") == 0
        or _class_count(competition_region, "overview-answer-prose") == 0
    ):
        _issue(
            issues,
            "error",
            "missing_bom_level_competition_profit_pool",
            "竞争格局与利润池 must organize by BOM/subsystem node with collapsible competition-bom-card, competition-question-grid, prose overview answers, source chips, and profit-pool-table",
        )
    if _class_count(html, "industry-competition"):
        missing_competition_questions = [
            label
            for label in ["玩家市场份额分布", "头部玩家优势分析", "替代玩家赶超希望", "格局变化核心变量"]
            if label not in html
        ]
        if missing_competition_questions:
            _issue(
                issues,
                "error",
                "missing_fixed_competition_profit_pool_questions",
                "竞争格局与利润池 must render the fixed BOM-level questions: "
                + ", ".join(missing_competition_questions),
            )
        source_pool_leaks: list[str] = []
        for card_match in re.finditer(
            r"<section\b[^>]*\boverview-question-card\b[^>]*>(.*?)</section>",
            competition_region,
            flags=re.IGNORECASE | re.DOTALL,
        ):
            card_html = card_match.group(1)
            if "overview-answer-prose" not in card_html or "overview-answer-sources" not in card_html:
                continue
            prose_match = re.search(
                r"<div\b[^>]*\boverview-answer-prose\b[^>]*>(.*?)</div>",
                card_html,
                flags=re.IGNORECASE | re.DOTALL,
            )
            source_match = re.search(
                r"<div\b[^>]*\boverview-answer-sources\b[^>]*>(.*?)</div>",
                card_html,
                flags=re.IGNORECASE | re.DOTALL,
            )
            if not prose_match or not source_match:
                continue
            inline_hrefs = set(
                re.findall(r"<a\b(?![^>]*\bsource-chip\b)[^>]*href\s*=\s*['\"]([^'\"]+)['\"]", prose_match.group(1), flags=re.IGNORECASE)
            )
            chip_hrefs = re.findall(
                r"<a\b[^>]*\bsource-chip\b[^>]*href\s*=\s*['\"]([^'\"]+)['\"]",
                source_match.group(1),
                flags=re.IGNORECASE,
            )
            leaked_hrefs = [href for href in chip_hrefs if href not in inline_hrefs]
            if leaked_hrefs:
                title_match = re.search(r"<h4[^>]*>(.*?)</h4>", card_html, flags=re.IGNORECASE | re.DOTALL)
                title = re.sub(r"<[^>]+>", "", title_match.group(1)).strip() if title_match else "unknown card"
                source_pool_leaks.append(f"{title}: {len(leaked_hrefs)} uncited source chip(s)")
        if source_pool_leaks:
            _issue(
                issues,
                "error",
                "competition_source_chips_not_claim_level",
                "竞争格局与利润池 source chips must only list sources actually cited in that card's prose, not broad node-level source pools: "
                + "; ".join(source_pool_leaks[:5]),
            )
    if _class_count(html, "industry-chokepoints") and (
        _tag_class_count(html, "details", "chokepoint-bom-card") < 1
        or _class_count(html, "chokepoint-question-grid") == 0
        or _class_count(html, "chokepoint-scorecard") == 0
        or _class_count(html, "overview-question-card") == 0
    ):
        _issue(
            issues,
            "error",
            "missing_bom_level_chokepoint_analysis",
            "瓶颈点 must organize by BOM/subsystem node with collapsible chokepoint-bom-card, chokepoint-question-grid, overview question cards, source chips, and chokepoint-scorecard",
        )
    required_industry_space_classes = [
        "industry-space-summary",
        "space-bom-reasoning",
        "space-node-card",
        "space-node-reasoning",
        "space-node-evidence",
        "space-node-space-reasoning",
        "space-node-sizing",
        "space-method-step",
        "space-step-title",
        "space-step-index",
        "space-public-methods",
        "space-method-card-grid",
        "space-method-card",
        "space-method-card-body",
        "space-method-entry",
        "space-method-entry-sources",
        "space-horizon-conclusion",
        "space-horizon-grid",
        "space-horizon-card",
        "space-node-sizing-table",
        "space-step-confidence",
    ]
    missing_industry_space_classes = [
        class_name for class_name in required_industry_space_classes if _class_count(html, class_name) == 0
    ]
    if _class_count(html, "industry-space") and missing_industry_space_classes:
        _issue(
            issues,
            "error",
            "missing_industry_space_bom_reasoning",
            "行业概况/行业空间 must directly render BOM node space reasoning cards with public sizing methods and evidence below; missing "
            + ", ".join(missing_industry_space_classes),
        )
    industry_space_node_cards = _tag_class_count(html, "details", "space-node-card")
    if _class_count(html, "industry-space") and industry_space_node_cards < 1:
        _issue(
            issues,
            "error",
            "missing_interactive_industry_space_node_cards",
            "行业空间 must render each key BOM node as a collapsible details.space-node-card",
        )
    gate_terms = [
        "BOM",
        "证据",
        "空间推理",
        "公开拆法",
        "公司指引",
        "公司 TAM",
        "客户侧指引",
        "第三方拆法",
        "财务兑现证据",
        "公司或机构",
        "指引内容",
        "时间范围",
        "可验证指标",
        "空间结论",
        "短期",
        "中期",
        "长期",
        "置信度",
        "结论",
    ]
    missing_gate_terms = [term for term in gate_terms if term not in html]
    if _class_count(html, "industry-space") and missing_gate_terms:
        _issue(
            issues,
            "error",
            "missing_industry_space_bom_reasoning_terms",
            "行业空间 must organize BOM node reasoning with public sizing methods first and evidence below; missing "
            + ", ".join(missing_gate_terms),
        )
    method_entries = list(
        re.finditer(
            r"<article\b[^>]*class\s*=\s*(['\"])(?=[^'\"]*\bspace-method-entry\b)[^'\"]*\1[^>]*>(.*?)</article>",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
    )
    method_entries_without_sources = [
        match.group(0)
        for match in method_entries
        if "space-method-entry-sources" not in match.group(0)
        or "source-chip" not in match.group(0)
        or "source-chip-missing" in match.group(0)
        or "待补来源" in match.group(0)
    ]
    if method_entries_without_sources:
        _issue(
            issues,
            "error",
            "industry_space_method_entry_missing_sources",
            "Every non-empty 行业空间/公开拆法 entry must carry its own selected evidence source chips; do not rely on a coarse BOM-node evidence pool. Missing or placeholder sources: "
            + str(len(method_entries_without_sources)),
        )
    if _class_count(html, "table-scroll") == 0 or "overflow-x:auto" not in html.replace(" ", ""):
        _issue(
            issues,
            "error",
            "missing_horizontal_table_scroll",
            "Wide report tables and dense card tables must use table-scroll with horizontal overflow so content does not exceed card boundaries",
        )
    if _class_count(html, "table-scroll") and _class_count(html, "bom-question-stage-flow") and (
        "scrollbar-gutter:stable" not in html.replace(" ", "")
        or "min-width:0;max-width:100%" not in html.replace(" ", "")
    ):
        _issue(
            issues,
            "error",
            "missing_nested_table_scroll_sizing",
            "Nested dense tables must keep a visible local horizontal scrollbar and set parent card/table containers to min-width:0 so metric values are not clipped",
        )
    if "<style" in html.lower():
        stacked_bom_child_grids = [
            "space-method-card-grid",
            "competition-question-grid",
            "chokepoint-question-grid",
        ]
        non_stacked_bom_child_grids = [
            class_name
            for class_name in stacked_bom_child_grids
            if _class_count(html, class_name) > 0
            and not _css_class_has_single_column_stack(html, class_name)
        ]
        if non_stacked_bom_child_grids:
            _issue(
                issues,
                "error",
                "missing_single_column_bom_child_card_stack",
                "Every BOM card's child method/question cards must render as a single-column full-width stack, not side-by-side; missing "
                + ", ".join(non_stacked_bom_child_grids),
            )
    required_chain_explainer_classes = [
        "chain-explain",
        "chain-research-bridge",
        "chain-node-lens",
        "chain-plain-summary",
        "chain-detail-panel",
        "chain-layer-grid",
        "chain-layer-card",
        "chain-relationship-graph",
        "chain-lane-map",
        "chain-value-flow",
        "chain-simple-flow",
        "chain-stage-panel",
        "chain-company-list",
        "chain-company-card",
    ]
    missing_chain_explainer_classes = [
        class_name for class_name in required_chain_explainer_classes if _class_count(html, class_name) == 0
    ]
    if missing_chain_explainer_classes:
        _issue(
            issues,
            "error",
            "missing_beginner_chain_explainer",
            "行业概况/技术链与 BOM 呈现 must include beginner-readable Chinese explanation components; missing "
            + ", ".join(missing_chain_explainer_classes),
        )
    chain_detail_panels = _tag_class_count(html, "details", "chain-detail-panel")
    if chain_detail_panels < 3:
        _issue(
            issues,
            "error",
            "missing_interactive_chain_detail_panels",
            "技术链与 BOM 呈现 must keep its long subcomponents collapsible as details.chain-detail-panel nodes for 泳道图, 价值流, and BOM / 组件级链条",
        )
    required_overview_labels = ["技术链与 BOM 呈现", "泳道图", "价值流"]
    missing_overview_labels = [label for label in required_overview_labels if label not in html]
    if industry_overview_sections and missing_overview_labels:
        _issue(
            issues,
            "error",
            "missing_industry_overview_blocks",
            "行业概况必须保留技术链与 BOM 呈现、泳道图、价值流；缺少 "
            + ", ".join(missing_overview_labels),
        )
    overlap_qa_start = _first_position(html, ["下钻 QA"])
    overlap_target_start = section_positions.get("标的推荐", len(html))
    qa_overlap_region = html[overlap_qa_start:overlap_target_start] if overlap_qa_start >= 0 else ""
    duplicated_overview_artifacts = [
        class_name
        for class_name in ("demand-space-model", "competition-landscape")
        if _class_count(qa_overlap_region, class_name) > 0
    ]
    if has_public_qa and industry_overview_sections and duplicated_overview_artifacts:
        _issue(
            issues,
            "error",
            "qa_duplicates_industry_overview",
            "下钻 QA must complement 行业概况 instead of re-rendering overview map/table artifacts; duplicated "
            + ", ".join(duplicated_overview_artifacts),
        )
    l3_metadata_counts = {
        "l3_skill_elements": _class_count(html, "l3-skill"),
        "l3_execution_status_elements": _class_count(html, "l3-execution-status"),
        "l3_score_component_elements": _class_count(html, "l3-score-component"),
        "l3_decision_use_elements": _class_count(html, "l3-decision-use"),
    }
    research_unit_cards = _research_unit_card_count(level_counts)
    if has_public_qa and require_l3 and research_unit_cards > 0 and (
        l3_metadata_counts["l3_skill_elements"] < research_unit_cards
        or l3_metadata_counts["l3_execution_status_elements"] < research_unit_cards
        or l3_metadata_counts["l3_score_component_elements"] < research_unit_cards
        or l3_metadata_counts["l3_decision_use_elements"] < research_unit_cards
    ):
        _issue(
            issues,
            "error",
            "missing_l3_skill_metadata",
            "Research-unit cards from L3 to L5 must visibly show selected skill, execution status, score component, and decision use",
        )

    if has_public_qa:
        for title in QA_BLOCK_TITLES:
            if title not in html:
                _issue(issues, "error", "missing_qa_block_title", f"QA cards must include {title}")

    target_start = section_positions.get("标的推荐", -1)
    source_start = section_positions.get("来源索引", len(html))
    qa_start = _first_position(html, ["下钻 QA"])
    qa_region_end = target_start if target_start >= 0 else len(html)
    qa_region = html[qa_start:qa_region_end] if qa_start >= 0 else html
    q4_relative_position = _first_position(qa_region, ['class="qid">Q4', "class='qid'>Q4", ">Q4<", "id=\"q4", "id='q4", "Q4"])
    q4_position = qa_start + q4_relative_position if qa_start >= 0 and q4_relative_position >= 0 else -1
    if has_public_qa and (q4_position < 0 or (qa_start >= 0 and not (qa_start <= q4_position < max(target_start, qa_start)))):
        _issue(issues, "error", "q4_not_in_question_drilldown", "Q4 must remain inside 下钻 QA")

    if _class_count(html, "target-section") == 0:
        _issue(issues, "error", "missing_target_section", "标的推荐 must render as target-section")
    if _class_count(html, "target-profit-bridge") == 0 or _class_count(html, "target-valuation-table") == 0:
        _issue(
            issues,
            "error",
            "missing_target_financial_bridge",
            "标的推荐 must include target-profit-bridge and target-valuation-table before the final target table",
        )
    if "target-table" not in html:
        _issue(issues, "error", "missing_target_table", "标的推荐 must render a dense target-table")
    if "target-odds-model" not in html or "target-odds-table" not in html:
        _issue(
            issues,
            "error",
            "missing_target_odds_model",
            "标的推荐 must include a simplified target-odds-model with target-odds-table",
        )
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
        "constraint-definition",
        "industry-overview-section",
        "industry-module",
        "industry-module-body",
        "module-index",
        "supply-chain-section",
        "chain-explain",
        "chain-research-bridge",
        "chain-node-lens",
        "chain-plain-summary",
        "chain-detail-panel",
        "chain-layer-grid",
        "chain-layer-card",
        "chain-relationship-graph",
        "chain-lane-map",
        "chain-value-flow",
        "chain-simple-flow",
        "chain-stage-panel",
        "chain-company-list",
        "chain-company-card",
        "component-value-chain",
        "bom-research-module",
        "bom-node-brief",
        "bom-question-list",
        "bom-question-card",
        "bom-question-index",
        "bom-question-answer",
        "bom-question-sources",
        "artifact-card",
        "target-section",
        "target-profit-bridge",
        "target-valuation-table",
        "target-odds-model",
        "target-odds-table",
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
                "current-time label fields may appear only inside 标的推荐",
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


def validate_report_contract_markdown(
    markdown: str,
    *,
    mode: str = "historical_backtest",
    require_l3: bool = False,
) -> dict[str, Any]:
    """Validate the Markdown-first public report contract."""

    issues: list[dict[str, str]] = []
    scope_match = re.search(r"^report_scope:\s*([A-Za-z0-9_-]+)\s*$", markdown, flags=re.MULTILINE)
    report_scope = scope_match.group(1) if scope_match else "research-project"
    headings = re.findall(r"^##\s+(.+?)\s*$", markdown, flags=re.MULTILINE)
    if report_scope == "standalone-bom":
        standalone_expected = [
            "1. 需求侧",
            "2. 供给侧",
            "3. 技术侧",
            "4. 估值侧",
            "5. ESG",
        ]
        if headings != standalone_expected:
            _issue(
                issues,
                "error",
                "markdown_standalone_bom_sections",
                "standalone-bom Markdown must use the locked five-lens H2 order",
            )
    else:
        expected = [f"{index}. {title}" for index, title in enumerate(REPORT_SECTIONS, start=1)]
        top_level = [heading for heading in headings if heading in expected]
        if top_level != expected:
            _issue(
                issues,
                "error",
                "markdown_top_level_sections",
                "Markdown report must use the locked four-section order with numbered H2 headings",
            )
    question_labels = [
        "当前 BOM 的需求是否会被 S 曲线放大拉动？",
        "供给能否跟上？",
        "谁控制供给？",
        "是否已经财务兑现？",
        "市场是否已定价？",
        "反证是什么？",
    ]
    question_count = sum(1 for label in question_labels if markdown.count(label) == 1)
    if report_scope == "standalone-bom":
        is_engine_report = bool(
            re.search(
                r"^investment_engine_version:\s*\S+",
                markdown,
                flags=re.MULTILINE,
            )
        )
        logic_chain_centered = bool(
            re.search(
                r"^research_model:\s*logic-chain-centered\s*$",
                markdown,
                flags=re.MULTILINE,
            )
        )
        subsection_labels = (
            ("第一性原理逻辑链", "逻辑节点与原子观点材料")
            if logic_chain_centered
            else ("简单逻辑链",)
        )
        for label in subsection_labels:
            if markdown.count(f"### {label}") != 5:
                _issue(
                    issues,
                    "error",
                    "markdown_standalone_bom_subsections",
                    f"every standalone BOM lens must include exactly one {label}",
                )
        if is_engine_report:
            node_section_label = (
                "### 逻辑节点与原子观点材料"
                if logic_chain_centered
                else "### 逻辑节点与公司信息"
            )
            if markdown.count(node_section_label) != 5:
                _issue(
                    issues,
                    "error",
                    "markdown_standalone_bom_entity_hierarchy",
                    (
                        "structured standalone BOM reports must render one "
                        "logic-node evidence section per lens"
                    ),
                )
            entity_header = "| 材料（含链接） | 类型 | 观点列表 |"
            if not logic_chain_centered and markdown.count(entity_header) < 1:
                _issue(
                    issues,
                    "error",
                    "markdown_standalone_bom_entity_table",
                    "structured reports require entity-level three-column material tables",
                )
            if "### 信息时间线" in markdown:
                _issue(
                    issues,
                    "error",
                    "markdown_standalone_bom_duplicate_timeline",
                    (
                        "structured reports must place material under entities "
                        "instead of repeating a lens-level timeline"
                    ),
                )
            lens_bodies = re.findall(
                r"^##\s+\d+\.\s+.+?\n(.*?)(?=^##\s+\d+\.|\Z)",
                markdown,
                flags=re.MULTILINE | re.DOTALL,
            )
            l3_blocks = [
                (title, body)
                for lens_body in lens_bodies
                for title, body in re.findall(
                    r"^####\s+([^\n]+)\n(.*?)(?=^####\s+|\Z)",
                    lens_body,
                    flags=re.MULTILINE | re.DOTALL,
                )
            ]
            missing_question_titles = [
                title
                for title, body in l3_blocks
                if not re.search(
                    r"^\*\*研究问题：\*\*\s+\S",
                    body,
                    flags=re.MULTILINE,
                )
            ]
            if not l3_blocks or missing_question_titles:
                _issue(
                    issues,
                    "error",
                    "markdown_standalone_bom_logic_node_question",
                    "every standalone BOM L3 node must visibly render one non-empty research question",
                )
            if logic_chain_centered:
                if not re.search(
                    r"^logic_chain_version:\s*\S+\s*$",
                    markdown,
                    flags=re.MULTILINE,
                ):
                    _issue(
                        issues,
                        "error",
                        "markdown_logic_chain_version",
                        "logic-chain-centered Markdown requires logic_chain_version",
                    )
                causal_node_count = len(
                    re.findall(r"^#### \d{2}\. ", markdown, flags=re.MULTILINE)
                )
                material_header = (
                    "| 发布日期 | 报告名称 | 材料类型 | 原子观点 | 对逻辑点的影响 |"
                )
                if (
                    causal_node_count < 5
                    or markdown.count(material_header) != causal_node_count
                ):
                    _issue(
                        issues,
                        "error",
                        "markdown_logic_node_material_table",
                        (
                            "every causal node must render one locked five-column "
                            "atomic-claim material table"
                        ),
                    )
                for forbidden_heading in (
                    "##### 节点状态历史",
                    "##### 信息事件历史",
                ):
                    if forbidden_heading in markdown:
                        _issue(
                            issues,
                            "error",
                            "markdown_logic_node_legacy_history",
                            "causal nodes must not render the retired dual-history UI",
                        )
            demand_party_match = re.search(
                r"^#### Q1 需求方\s*$([\s\S]*?)(?=^#### |^### (?:最新|全局)结论与趋势)",
                markdown,
                flags=re.MULTILINE,
            )
            if demand_party_match:
                demand_party_block = demand_party_match.group(1)
                current_at = demand_party_block.find("**当前需求方**")
                future_at = demand_party_block.find("**潜在未来需求方**")
                if current_at < 0 or future_at <= current_at:
                    _issue(
                        issues,
                        "error",
                        "markdown_demand_party_groups",
                        (
                            "Q1 demand-party list must render current demanders "
                            "before potential future demanders"
                        ),
                    )
                for forbidden in (
                    "**当前结论：**",
                    "**截面变化与评估：**",
                    "| 材料（含链接） | 类型 | 观点列表 |",
                ):
                    if forbidden in demand_party_block:
                        _issue(
                            issues,
                            "error",
                            "markdown_demand_party_scope",
                            "Q1 demand-party list must not render snapshot or material detail",
                        )
                        break
            demand_quantity_match = re.search(
                r"^#### Q2 当前需求量基线\s*$([\s\S]*?)(?=^#### |^### (?:最新|全局)结论与趋势)",
                markdown,
                flags=re.MULTILINE,
            )
            if demand_quantity_match:
                demand_quantity_block = demand_quantity_match.group(1)
                current_at = demand_quantity_block.find("##### 1. 当前需求方")
                potential_at = demand_quantity_block.find(
                    "##### 2. 潜在未来需求方"
                )
                other_at = demand_quantity_block.find("##### 3. 其它分类")
                valid_group_order = (
                    0 <= current_at < potential_at < other_at
                )
                if not valid_group_order:
                    _issue(
                        issues,
                        "error",
                        "markdown_demand_quantity_groups",
                        (
                            "Q2 demand quantity matrix must render current, "
                            "potential-future, and other groups in order"
                        ),
                    )
                required_header = "| 来源 | 期间 | 信息类型 | 具体信息 |"
                if valid_group_order:
                    group_blocks = (
                        demand_quantity_block[current_at:potential_at],
                        demand_quantity_block[potential_at:other_at],
                        demand_quantity_block[other_at:],
                    )
                    if any(
                        "###### " not in group_block
                        or required_header not in group_block
                        for group_block in group_blocks
                    ):
                        _issue(
                            issues,
                            "error",
                            "markdown_demand_quantity_tables",
                            (
                                "Q2 requires one four-column table per specific "
                                "category in all three groups"
                            ),
                        )
                if "**截面变化与评估：**" in demand_quantity_block:
                    _issue(
                        issues,
                        "error",
                        "markdown_demand_quantity_scope",
                        "Q2 demand quantity matrix must not render entity snapshots",
                    )
            if (
                not logic_chain_centered
                and markdown.count("**截面变化与评估：**") < 1
            ):
                _issue(
                    issues,
                    "error",
                    "markdown_standalone_bom_entity_assessment",
                    "every rendered entity requires an as-of change assessment",
                )
            if markdown.count("### 当前投资判断") != 1:
                _issue(
                    issues,
                    "error",
                    "markdown_standalone_bom_investment_engine",
                    "structured standalone BOM reports require one current investment judgment",
                )
            company_header = "| 公司 | 敞口 | 盈利传导 | 市场定价 | 当前结论 | 动作 |"
            if markdown.count(company_header) != 1:
                _issue(
                    issues,
                    "error",
                    "markdown_standalone_bom_company_bridge",
                    "structured standalone BOM reports require one company impact table",
                )
        else:
            if markdown.count("### 信息时间线") != 5:
                _issue(
                    issues,
                    "error",
                    "markdown_standalone_bom_subsections",
                    "every legacy standalone BOM lens must include one information timeline",
                )
            timeline_header = "| 时间 | 信息类型 | Source | 观点列表 |"
            if markdown.count(timeline_header) != 5:
                _issue(
                    issues,
                    "error",
                    "markdown_standalone_bom_timeline_header",
                    "every standalone BOM lens must include the canonical timeline table",
                )
            section_pattern = re.compile(
                r"^##\s+\d+\.\s+.+?\n(?P<body>.*?)(?=^##\s+\d+\.|\Z)",
                flags=re.MULTILINE | re.DOTALL,
            )
            for section in section_pattern.finditer(markdown):
                dates = re.findall(
                    r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|",
                    section.group("body"),
                    flags=re.MULTILINE,
                )
                if not dates:
                    _issue(
                        issues,
                        "error",
                        "markdown_standalone_bom_empty_timeline",
                        "every standalone BOM lens must include dated timeline rows",
                    )
                elif dates != sorted(dates, reverse=True):
                    _issue(
                        issues,
                        "error",
                        "markdown_standalone_bom_timeline_order",
                        "standalone BOM timeline rows must be ordered newest to oldest",
                    )
    elif report_scope == "industry-index":
        if "技术链与 BOM" not in markdown or "BOM 独立研究目录" not in markdown:
            _issue(
                issues,
                "error",
                "markdown_industry_index",
                "industry-index Markdown must contain the technology chain and BOM child directory",
            )
        if question_count:
            _issue(
                issues,
                "error",
                "markdown_parent_embeds_questions",
                "industry-index Markdown must link to BOM children instead of embedding six-question bodies",
            )
    elif report_scope == "bom-node":
        if question_count != 6:
            _issue(
                issues,
                "error",
                "markdown_bom_six_questions",
                "bom-node Markdown must contain the six canonical BOM questions exactly once",
            )
        for label in ("基本理解思路", "当前结论", "相较上一截面的变化", "时间演化", "映射材料", "信息覆盖"):
            if markdown.count(label) < 6:
                _issue(
                    issues,
                    "error",
                    "markdown_missing_question_subsection",
                    f"every BOM question must include {label}",
                )

    if not re.search(
        r"\[[^\]]+\]\((?:<)?(?:https?://|/|(?:\./)?source/)[^)]+(?:>)?\)",
        markdown,
    ):
        _issue(
            issues,
            "error",
            "markdown_source_links",
            "Markdown report must keep clickable source links next to research content",
        )
    for leaked in ("source_universe_plan", "exa_search_plan", "direct_query", "IMA_OPENAPI_APIKEY"):
        if leaked in markdown:
            _issue(
                issues,
                "error",
                "markdown_process_leak",
                f"public Markdown must not expose internal process field {leaked}",
            )

    return {
        "ok": not any(issue.get("severity") == "error" for issue in issues),
        "issues": issues,
        "summary": {
            "mode": mode,
            "report_scope": report_scope,
            "level1_cards": 5 if report_scope == "standalone-bom" else question_count,
            "level2_cards": 0,
            "level3_cards": 0,
            "require_l3": require_l3,
        },
    }


def _report_scope(html: str) -> str:
    match = re.search(
        r"<body\b[^>]*\bdata-report-scope\s*=\s*(['\"])([^'\"]+)\1",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return match.group(2).strip() if match else ""


def _validate_standalone_bom_report_html(
    html: str,
    *,
    mode: str,
) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    engine_match = re.search(
        r"<body\b[^>]*\bdata-investment-engine-version\s*=\s*(['\"])([^'\"]+)\1",
        html,
        flags=re.IGNORECASE,
    )
    is_engine_report = bool(engine_match)
    logic_chain_centered = bool(
        re.search(
            r"<body\b[^>]*\bdata-research-model\s*=\s*(['\"])logic-chain-centered\1",
            html,
            flags=re.IGNORECASE,
        )
    )
    lens_ids = ("demand", "supply", "technology", "valuation", "esg")
    lens_labels = ("需求侧", "供给侧", "技术侧", "估值侧", "ESG")
    positions = [html.find(f'id="lens-{lens_id}"') for lens_id in lens_ids]
    if any(position < 0 for position in positions):
        _issue(
            issues,
            "error",
            "standalone_html_lenses",
            "standalone BOM HTML must render all five locked lenses",
        )
    elif positions != sorted(positions):
        _issue(
            issues,
            "error",
            "standalone_html_lens_order",
            "standalone BOM HTML lenses are out of order",
        )
    for label in lens_labels:
        if f"<h2>{label}</h2>" not in html:
            _issue(
                issues,
                "error",
                "standalone_html_lens_label",
                f"standalone BOM HTML is missing lens label {label}",
            )
    if not re.search(
        r"<body\b[^>]*\bdata-bom-node-id\s*=\s*(['\"])[^'\"]+\1",
        html,
        flags=re.IGNORECASE,
    ):
        _issue(
            issues,
            "error",
            "standalone_html_bom_identity",
            "standalone BOM HTML must expose data-bom-node-id",
        )
    common_required_classes = (
        "report-header",
        "top-nav",
        "lens-section",
        "logic-note",
    )
    if logic_chain_centered:
        common_required_classes += (
            "logic-chain-map",
            "node-material-table",
        )
    else:
        common_required_classes += ("claim-list", "claim-index")
    for class_name in common_required_classes:
        if _class_count(html, class_name) == 0:
            _issue(
                issues,
                "error",
                "standalone_html_component",
                f"standalone BOM HTML is missing component {class_name}",
            )
    for class_name in (
        "lens-section",
        "logic-note",
    ):
        if _class_count(html, class_name) != 5:
            _issue(
                issues,
                "error",
                "standalone_html_component_count",
                f"standalone BOM HTML must render five {class_name} components",
            )
    if is_engine_report:
        required_engine_classes = [
            "decision-section",
            "logic-state-section",
            "company-table",
        ]
        if logic_chain_centered:
            required_engine_classes.extend(
                [
                    "logic-chain-map",
                    "causal-node",
                    "node-material-table",
                    "atomic-claim-list",
                    "claim-impact-list",
                    "node-material-title",
                ]
            )
        else:
            required_engine_classes.extend(
                [
                    "entity-module",
                    "entity-evaluation",
                    "entity-table-wrap",
                    "entity-table",
                    "entity-source-row",
                ]
            )
        for class_name in required_engine_classes:
            if _class_count(html, class_name) == 0:
                _issue(
                    issues,
                    "error",
                    "standalone_html_investment_engine_component",
                    f"structured standalone BOM HTML is missing {class_name}",
                )
        for class_name, expected_count in (
            ("decision-section", 1),
            ("logic-state-section", 5),
            ("company-table", 1),
        ):
            if _class_count(html, class_name) != expected_count:
                _issue(
                    issues,
                    "error",
                    "standalone_html_investment_engine_component",
                    (
                        "structured standalone BOM HTML must render "
                        f"{expected_count} {class_name} component(s)"
                    ),
                )
        if logic_chain_centered:
            if _class_count(html, "logic-chain-map") != 5:
                _issue(
                    issues,
                    "error",
                    "standalone_html_logic_chain_map",
                    "logic-chain-centered reports require one causal map per lens",
                )
            if not re.search(
                r"<body\b[^>]*\bdata-logic-chain-version\s*=\s*(['\"])[^'\"]+\1",
                html,
                flags=re.IGNORECASE,
            ):
                _issue(
                    issues,
                    "error",
                    "standalone_html_logic_chain_version",
                    "logic-chain-centered reports must expose the logic-chain version",
                )
            causal_node_count = _class_count(html, "causal-node")
            node_table_count = _class_count(html, "node-material-table")
            if node_table_count != causal_node_count:
                _issue(
                    issues,
                    "error",
                    "standalone_html_node_material_table_count",
                    "every causal node must render one atomic-claim material table",
                )
            for label in (
                "发布日期",
                "报告名称",
                "材料类型",
                "原子观点",
                "对逻辑点的影响",
            ):
                if html.count(f'<th scope="col">{label}</th>') != node_table_count:
                    _issue(
                        issues,
                        "error",
                        "standalone_html_node_material_table_header",
                        f"every causal-node table must include the locked header {label}",
                    )
            for table_body in re.findall(
                r'<table\b[^>]*class="[^"]*\bnode-material-table\b[^"]*"[^>]*>(.*?)</table>',
                html,
                flags=re.IGNORECASE | re.DOTALL,
            ):
                dates = re.findall(
                    r'<time\b[^>]*datetime="(\d{4}-\d{2}-\d{2})"',
                    table_body,
                    flags=re.IGNORECASE,
                )
                if dates != sorted(dates, reverse=True):
                    _issue(
                        issues,
                        "error",
                        "standalone_html_node_material_order",
                        "causal-node material rows must be ordered newest to oldest",
                    )
            for row_body in re.findall(
                r'<tr\b[^>]*class="[^"]*\bnode-material-row\b[^"]*"[^>]*>(.*?)</tr>',
                html,
                flags=re.IGNORECASE | re.DOTALL,
            ):
                atomic_match = re.search(
                    r'<ol\b[^>]*class="[^"]*\batomic-claim-list\b[^"]*"[^>]*>(.*?)</ol>',
                    row_body,
                    flags=re.IGNORECASE | re.DOTALL,
                )
                impact_match = re.search(
                    r'<ol\b[^>]*class="[^"]*\bclaim-impact-list\b[^"]*"[^>]*>(.*?)</ol>',
                    row_body,
                    flags=re.IGNORECASE | re.DOTALL,
                )
                atomic_count = (
                    len(re.findall(r"<li\b", atomic_match.group(1), re.IGNORECASE))
                    if atomic_match
                    else 0
                )
                impact_count = (
                    len(re.findall(r"<li\b", impact_match.group(1), re.IGNORECASE))
                    if impact_match
                    else 0
                )
                if not atomic_count or atomic_count != impact_count:
                    _issue(
                        issues,
                        "error",
                        "standalone_html_node_material_numbering",
                        "every atomic claim must have one parallel numbered mapping effect",
                    )
                if not re.search(
                    r'<time\b[^>]*datetime="\d{4}-\d{2}-\d{2}"',
                    row_body,
                    flags=re.IGNORECASE,
                ):
                    _issue(
                        issues,
                        "error",
                        "standalone_html_node_material_date",
                        "every causal-node material row requires a publication date",
                    )
                if not re.search(
                    r'<td\b[^>]*class="[^"]*\bnode-material-title\b[^"]*"[^>]*>\s*<a\b',
                    row_body,
                    flags=re.IGNORECASE,
                ):
                    _issue(
                        issues,
                        "error",
                        "standalone_html_node_material_link",
                        "every causal-node material row requires a linked report name",
                    )
            for retired_class in (
                "node-state-history",
                "claim-month-group",
                "claim-source-group",
                "claim-event",
            ):
                if _class_count(html, retired_class):
                    _issue(
                        issues,
                        "error",
                        "standalone_html_legacy_history",
                        f"causal-node report must not render retired class {retired_class}",
                    )
        entity_table_count = _class_count(html, "entity-table")
        for label in ("材料（含链接）", "类型", "观点列表"):
            if html.count(f'<th scope="col">{label}</th>') != entity_table_count:
                _issue(
                    issues,
                    "error",
                    "standalone_html_entity_table_header",
                    (
                        "every rendered entity audit must keep the locked "
                        f"three-column table; missing header {label}"
                    ),
                )
        if _class_count(html, "timeline"):
            _issue(
                issues,
                "error",
                "standalone_html_duplicate_timeline",
                (
                    "structured reports must place material under entities "
                    "instead of repeating a lens-level timeline"
                ),
            )
        if _class_count(html, "logic-node") < 5:
            _issue(
                issues,
                "error",
                "standalone_html_logic_nodes",
                "structured standalone BOM HTML must render structured logic nodes",
            )
        logic_node_count = _class_count(html, "logic-node")
        question_blocks = re.findall(
            r'<p\b[^>]*class\s*=\s*(["\'])[^"\']*\blogic-node-question\b[^"\']*\1[^>]*>(.*?)</p>',
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        valid_question_count = sum(
            1
            for _, block in question_blocks
            if re.match(r"^研究问题\s*\S", _strip_html(block))
        )
        if (
            _class_count(html, "logic-node-question") != logic_node_count
            or valid_question_count != logic_node_count
        ):
            _issue(
                issues,
                "error",
                "standalone_html_logic_node_question",
                "every standalone BOM L3 node must visibly render one non-empty research question",
            )
        if _class_count(html, "claim-index") < _class_count(html, "entity-source-row"):
            _issue(
                issues,
                "error",
                "standalone_html_claim_bullets",
                "every entity material row must render at least one bullet claim",
            )
        demand_party_nodes = re.findall(
            r'<article\b[^>]*\bdata-render-mode=["\']demand-party-list["\'][^>]*>(.*?)</article>',
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        for demand_party_node in demand_party_nodes:
            current_at = demand_party_node.find(
                'data-demand-party-group="current"'
            )
            future_at = demand_party_node.find(
                'data-demand-party-group="potential_future"'
            )
            if current_at < 0 or future_at <= current_at:
                _issue(
                    issues,
                    "error",
                    "standalone_html_demand_party_groups",
                    (
                        "Q1 demand-party list must render current demanders "
                        "before potential future demanders"
                    ),
                )
            if any(
                marker in demand_party_node
                for marker in (
                    'class="state-badge',
                    'class="logic-conclusion',
                    'class="entity-module',
                    'class="entity-table',
                )
            ):
                _issue(
                    issues,
                    "error",
                    "standalone_html_demand_party_scope",
                    "Q1 demand-party list must not render snapshot or material detail",
                )
        demand_quantity_nodes = re.findall(
            r'<article\b[^>]*\bdata-render-mode=["\']demand-quantity-matrix["\'][^>]*>(.*?)</article>',
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        for demand_quantity_node in demand_quantity_nodes:
            current_at = demand_quantity_node.find(
                'data-demand-forecast-group="current"'
            )
            potential_at = demand_quantity_node.find(
                'data-demand-forecast-group="potential_future"'
            )
            other_at = demand_quantity_node.find(
                'data-demand-forecast-group="other"'
            )
            if not (0 <= current_at < potential_at < other_at):
                _issue(
                    issues,
                    "error",
                    "standalone_html_demand_quantity_groups",
                    (
                        "Q2 demand quantity matrix must render current, "
                        "potential-future, and other groups in order"
                    ),
                )
            tier_tags = re.findall(
                r'<details\b[^>]*class="demand-quantity-tier"[^>]*>',
                demand_quantity_node,
                flags=re.IGNORECASE,
            )
            category_tags = re.findall(
                r'<details\b[^>]*class="demand-quantity-category"[^>]*>',
                demand_quantity_node,
                flags=re.IGNORECASE,
            )
            if (
                len(tier_tags) != 3
                or not category_tags
                or any(re.search(r"\bopen(?:\s|=|>)", tag) for tag in tier_tags)
                or any(
                    re.search(r"\bopen(?:\s|=|>)", tag)
                    for tag in category_tags
                )
            ):
                _issue(
                    issues,
                    "error",
                    "standalone_html_demand_quantity_disclosures",
                    (
                        "Q2 requires three collapsed outer disclosures with "
                        "collapsed specific-category disclosures nested inside"
                    ),
                )
            if (
                'data-demand-category-table' not in demand_quantity_node
                or demand_quantity_node.count(
                    "<th>来源</th><th>期间</th><th>信息类型</th><th>具体信息</th>"
                )
                < 3
            ):
                _issue(
                    issues,
                    "error",
                    "standalone_html_demand_quantity_tables",
                    (
                        "Q2 requires one four-column table per specific "
                        "category in all three groups"
                    ),
                )
            if any(
                marker in demand_quantity_node
                for marker in (
                    'class="entity-module',
                    'class="entity-table',
                    'class="logic-node-detail',
                )
            ):
                _issue(
                    issues,
                    "error",
                    "standalone_html_demand_quantity_scope",
                    "Q2 demand quantity matrix must not render entity snapshots",
                )
        for table_body in re.findall(
            r'<table class="entity-table">(.*?)</table>',
            html,
            flags=re.IGNORECASE | re.DOTALL,
        ):
            dates = re.findall(
                r'<time\b[^>]*datetime="(\d{4}-\d{2}-\d{2})"',
                table_body,
            )
            if dates != sorted(dates, reverse=True):
                _issue(
                    issues,
                    "error",
                    "standalone_html_entity_timeline_order",
                    "entity material tables must be ordered newest to oldest",
                )
    else:
        for class_name in (
            "timeline",
            "timeline-table-wrap",
            "timeline-table",
        ):
            if _class_count(html, class_name) != 5:
                _issue(
                    issues,
                    "error",
                    "standalone_html_component_count",
                    f"standalone BOM HTML must render five {class_name} components",
                )
        if _class_count(html, "source-row") == 0:
            _issue(
                issues,
                "error",
                "standalone_html_component",
                "standalone BOM HTML is missing source-row material",
            )
        for label in ("时间", "信息类型", "报告", "观点列表"):
            if html.count(f'<th scope="col">{label}</th>') != 5:
                _issue(
                    issues,
                    "error",
                    "standalone_html_timeline_header",
                    (
                        "each standalone lens must render the locked four-column "
                        f"timeline table; missing header {label}"
                    ),
                )
        if _class_count(html, "claim-index") < _class_count(html, "source-row"):
            _issue(
                issues,
                "error",
                "standalone_html_claim_bullets",
                "every standalone timeline row must render at least one bullet claim",
            )
    if not re.search(
        r'<a\b[^>]*href\s*=\s*["\'](?:https?://|source/)[^"\']+["\']',
        html,
        flags=re.IGNORECASE,
    ):
        _issue(
            issues,
            "error",
            "standalone_html_source_links",
            "standalone BOM HTML must keep clickable source links",
        )
    if "file://" in html:
        _issue(
            issues,
            "error",
            "standalone_html_file_uri",
            "local HTML source links must use project-relative paths, not file URIs",
        )
    if re.search(r'href\s*=\s*["\']/Users/', html):
        _issue(
            issues,
            "error",
            "standalone_html_absolute_local_path",
            "local HTML source links must stay project-relative",
        )
    local_source_tags = re.findall(
        r'<a\b[^>]*href\s*=\s*["\']source/[^"\']+["\'][^>]*>',
        html,
        flags=re.IGNORECASE,
    )
    if any(re.search(r'\btarget\s*=\s*["\']_blank["\']', tag) for tag in local_source_tags):
        _issue(
            issues,
            "error",
            "standalone_html_local_new_tab",
            "local PDF links must navigate in the current tab",
        )
    if not is_engine_report:
        for lens_id in lens_ids:
            start = html.find(f'id="lens-{lens_id}"')
            next_positions = [position for position in positions if position > start]
            end = min(next_positions) if next_positions else len(html)
            region = html[start:end]
            dates = re.findall(
                r'<time\b[^>]*datetime="(\d{4}-\d{2}-\d{2})"',
                region,
            )
            if not dates and 'class="empty-state"' not in region:
                _issue(
                    issues,
                    "error",
                    "standalone_html_empty_timeline",
                    f"lens {lens_id} must include dated timeline material",
                )
            elif dates != sorted(dates, reverse=True):
                _issue(
                    issues,
                    "error",
                    "standalone_html_timeline_order",
                    f"lens {lens_id} timeline must be newest to oldest",
                )
    if is_engine_report:
        if (
            _class_count(html, "action-actionable_long")
            and _class_count(html, "gate-fail")
        ):
            _issue(
                issues,
                "error",
                "standalone_html_failed_actionable_gate",
                "actionable_long cannot be rendered while a semantic gate fails",
            )
    lowered = html.lower()
    for leaked in (
        "source_universe_plan",
        "exa_search_plan",
        "direct_query",
        "ima_openapi_apikey",
    ):
        if leaked in lowered:
            _issue(
                issues,
                "error",
                "standalone_html_process_leak",
                f"public HTML must not expose internal process field {leaked}",
            )
    return {
        "ok": not any(issue.get("severity") == "error" for issue in issues),
        "issues": issues,
        "summary": {
            "mode": mode,
            "report_scope": "standalone-bom",
            "level1_cards": 5,
            "level2_cards": 0,
            "level3_cards": 0,
        },
    }


def _validate_split_scope_report_html(
    html: str,
    *,
    report_scope: str,
    mode: str,
) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    section_positions = _section_positions(html)
    found_sections = [section for section in REPORT_SECTIONS if section in section_positions]
    if found_sections != REPORT_SECTIONS:
        _issue(issues, "error", "top_level_sections", "split reports must keep the locked four-section order")
    elif [section_positions[section] for section in REPORT_SECTIONS] != sorted(section_positions.values()):
        _issue(issues, "error", "top_level_order", "top-level sections are out of order")

    if _class_count(html, "industry-overview-section") != 1:
        _issue(issues, "error", "industry_overview_scope", "each split report must contain exactly one industry-overview-section")
    for required_class in [
        "hero",
        "top-nav",
        "goal-card",
        "target-section",
        "target-profit-bridge",
        "target-valuation-table",
        "target-odds-model",
        "target-odds-table",
        "target-table",
        "source-collapse",
        "table-scroll",
    ]:
        if _class_count(html, required_class) == 0:
            _issue(
                issues,
                "error",
                "missing_split_report_component",
                f"split report is missing required component {required_class}",
            )

    bom_modules = _tag_class_count(html, "details", "industry-module", "bom-research-module")
    bom_question_cards = _tag_class_count(html, "details", "bom-question-card")
    if report_scope == "industry-index":
        if _tag_class_count(html, "details", "industry-module", "supply-chain-section") != 1:
            _issue(issues, "error", "missing_index_supply_chain", "industry index must contain one technical-chain module")
        if _tag_class_count(html, "details", "industry-module", "bom-project-index") != 1:
            _issue(issues, "error", "missing_bom_project_index", "industry index must contain one BOM child-project index")
        index_cards = _class_count(html, "bom-index-card")
        if index_cards < 1:
            _issue(issues, "error", "missing_bom_index_cards", "industry index must link at least one BOM child report")
        linked_cards = len(
            re.findall(
                r"<a\b[^>]*class\s*=\s*(['\"])(?=[^'\"]*\bbom-index-card\b)[^'\"]*\1[^>]*href\s*=\s*(['\"])boms/[A-Za-z0-9_-]+/professional_report\.html\2",
                html,
                flags=re.IGNORECASE | re.DOTALL,
            )
        )
        if linked_cards != index_cards:
            _issue(issues, "error", "invalid_bom_index_links", "every BOM index card must link to boms/<node_id>/professional_report.html")
        if bom_modules or bom_question_cards:
            _issue(issues, "error", "industry_index_embeds_bom_research", "industry index must not embed BOM six-question modules")
    else:
        if not re.search(r"<body\b[^>]*\bdata-bom-node-id\s*=", html, flags=re.IGNORECASE):
            _issue(issues, "error", "missing_bom_node_identity", "BOM report must expose data-bom-node-id")
        if _class_count(html, "project-back-link") != 1:
            _issue(issues, "error", "missing_project_back_link", "BOM report must link back to its industry index")
        if bom_modules != 1:
            _issue(issues, "error", "bom_report_module_count", "BOM child report must contain exactly one BOM research module")
        if bom_question_cards != 6:
            _issue(issues, "error", "bom_report_question_count", "BOM child report must contain exactly six BOM question cards")
        for label in [
            "当前 BOM 的需求是否会被 S 曲线放大拉动？",
            "供给能否跟上？",
            "谁控制供给？",
            "是否已经财务兑现？",
            "市场是否已定价？",
            "反证是什么？",
        ]:
            if label not in html:
                _issue(issues, "error", "missing_bom_question_label", f"BOM child report is missing {label}")
        if _tag_class_count(html, "details", "bom-s-curve-stage-card") != 1:
            _issue(issues, "error", "bom_stage_rollup_count", "BOM child report must contain one S-curve rollup")
        for required_class in [
            "bom-question-understanding",
            "bom-question-current",
            "bom-question-change",
            "bom-question-timeline",
            "bom-question-materials",
            "bom-question-coverage",
        ]:
            if _class_count(html, required_class) != bom_question_cards:
                _issue(
                    issues,
                    "error",
                    "bom_temporal_question_sequence",
                    f"each BOM question must contain exactly one {required_class}",
                )
        for required_class in [
            "bom-temporal-baseline",
            "bom-material-timeline",
            "bom-mapped-material-table",
            "bom-coverage-status",
            "bom-stage-current",
            "bom-stage-evidence-grid",
            "bom-stage-next-signal",
            "bom-stage-downgrade-signal",
            "bom-stage-source-discipline",
        ]:
            if _class_count(html, required_class) == 0:
                _issue(issues, "error", "missing_bom_child_component", f"BOM child report is missing {required_class}")
        for forbidden_class in [
            "bom-step-research-logic",
            "bom-stage-integrated-card",
            "bom-stage-subcard",
            "bom-question-research-status",
        ]:
            if _class_count(html, forbidden_class):
                _issue(
                    issues,
                    "error",
                    "legacy_fixed_stage_rendering",
                    f"BOM child report must not render fixed-stage component {forbidden_class}",
                )

    if _class_count(html, "overview-source-plan") or _class_count(html, "source-universe-plan") or _class_count(html, "exa-search-plan"):
        _issue(issues, "error", "public_source_plan_leak", "raw search plans must stay internal")
    compact_css = html.replace(" ", "")
    if "overflow-x:auto" not in compact_css or "scrollbar-gutter:stable" not in compact_css:
        _issue(issues, "error", "missing_horizontal_table_scroll", "split reports must preserve local horizontal table scrolling")

    target_start = section_positions.get("标的推荐", -1)
    source_start = section_positions.get("来源索引", len(html))
    target_region = html[target_start:source_start] if target_start >= 0 else ""
    if mode == "historical_backtest":
        non_target_region = html[: max(target_start, 0)] + html[source_start:]
        if any(term in non_target_region for term in LABEL_TERMS):
            _issue(issues, "error", "label_outside_final_targets", "current-time labels may appear only inside target recommendations")
        if not any(term in target_region for term in LABEL_TERMS):
            _issue(issues, "warning", "missing_label_area", "historical backtest reports should include one label area")

    lowered_html = html.lower()
    for term in PUBLIC_META_DRIFT_TERMS:
        if term.lower() in lowered_html:
            _issue(issues, "error", "public_meta_drift", f"final HTML must not include process/change-log term: {term}")

    return {
        "ok": not _any_error(issues),
        "summary": {
            "report_scope": report_scope,
            "top_level_sections": found_sections,
            "bom_research_modules": bom_modules,
            "bom_question_cards": bom_question_cards,
            "bom_index_cards": _class_count(html, "bom-index-card"),
            "mode": mode,
        },
        "issues": issues,
    }


def validate_project_schema(project: dict[str, Any]) -> dict[str, Any]:
    """Validate project.json against the four-stage pipeline schema."""
    issues: list[dict[str, str]] = []
    if not isinstance(project, dict):
        return {"ok": False, "issues": [{"severity": "error", "code": "missing_project", "message": "project dict is absent or not a dict"}], "summary": {}}
    project_id = str(project.get("project_id") or "")
    if not project_id:
        _issue(issues, "error", "missing_project_id", "project.json must include project_id")
    research_type = str(project.get("research_type") or "")
    valid_types = {"industry/theme opportunity", "single company", "event/policy", "technology/product route", "target update"}
    if research_type not in valid_types:
        _issue(issues, "error", "missing_or_invalid_research_type", f"project.json must include research_type in {valid_types}")
    run_mode = str(project.get("run_mode") or "")
    if run_mode not in ("historical_backtest", "live_prediction"):
        _issue(issues, "error", "missing_or_invalid_run_mode", "project.json must declare run_mode as historical_backtest or live_prediction")
    if run_mode == "historical_backtest" and not project.get("as_of_date"):
        _issue(issues, "error", "missing_as_of_date", "historical_backtest mode requires as_of_date in project.json")
    if run_mode == "live_prediction" and not project.get("report_date"):
        _issue(issues, "error", "missing_report_date", "live_prediction mode requires report_date in project.json")
    domain_playbook = str(project.get("domain_playbook") or "")
    if not domain_playbook:
        _issue(issues, "warn", "missing_domain_playbook", "project.json should specify a domain_playbook; defaulting to generic")
    return {"ok": not _any_error(issues), "issues": issues, "summary": {"project_id": project_id, "research_type": research_type, "run_mode": run_mode}}


def validate_industry_overview(project_dir: "str | Path") -> dict[str, Any]:
    """Validate that an industry overview has been populated with non-trivial data before Stage 3."""
    import json
    from pathlib import Path
    issues: list[dict[str, str]] = []
    project_dir = Path(project_dir)

    # Check project.json
    project_file = project_dir / "project.json"
    if not project_file.exists():
        _issue(issues, "error", "missing_project_json", f"{project_dir} has no project.json")
        return {"ok": False, "issues": issues, "summary": {}}
    with open(project_file) as fh:
        project = json.load(fh)
    project_validation = validate_project_schema(project)
    if not project_validation["ok"]:
        issues.extend(project_validation["issues"])

    # Check qa_tree.json for supply_chain
    qa_file = project_dir / "qa_tree.json"
    chain = {}
    if qa_file.exists():
        with open(qa_file) as fh:
            chain = json.load(fh).get("supply_chain") or {}

    # Validate optional industry_space_evidence_pack when a deeper space module is present.
    evidence_pack = (
        chain.get("industry_space_evidence_pack")
        or chain.get("industry_space_bom_reasoning")
        or chain.get("industry_space_rows")
        or []
    )
    if isinstance(evidence_pack, list) and evidence_pack:
        node_count = 0
        has_sizing_data = 0
        for node in evidence_pack:
            if not isinstance(node, dict):
                continue
            node_count += 1
            sizing = node.get("publicSizingMethods") or node.get("public_sizing_methods") or {}
            if isinstance(sizing, dict) and sizing.get("methods"):
                has_sizing_data += 1
        if node_count == 0:
            _issue(issues, "error", "empty_industry_space_evidence_pack", "industry_space_evidence_pack exists but contains no BOM nodes")
        if has_sizing_data == 0:
            _issue(issues, "warn", "no_space_sizing_data", "no BOM node has populated publicSizingMethods; Stage 2 Module 2 may be incomplete")

    # Validate simplified S-curve module presence hints
    found_modules = []
    if chain.get("layers") or chain.get("stage_groups"):
        found_modules.append("技术链与BOM呈现")
    if evidence_pack and len(evidence_pack) > 0:
        found_modules.append("S曲线与产业空间")
    if chain.get("competition") or chain.get("competition_landscape"):
        found_modules.append("竞争格局与利润池")
    if chain.get("chokepoints") or chain.get("candidate_chokepoints"):
        found_modules.append("瓶颈点")
    if chain.get("data_gaps") or chain.get("pending_questions"):
        found_modules.append("关键变量与待验证数据")

    required_modules = ["技术链与BOM呈现"]
    missing_modules = [m for m in required_modules if m not in found_modules]
    for module in missing_modules:
        _issue(issues, "warn", f"missing_module_hint_{module}", f"行业概况 module '{module}' has no detectable data in supply_chain; stage may be incomplete")

    ok = not _any_error(issues)
    return {"ok": ok, "issues": issues, "summary": {"modules_detected": found_modules, "missing_modules": missing_modules, "bom_nodes": len(evidence_pack)}}


def _any_error(issues: list[dict[str, str]]) -> bool:
    return any(i.get("severity") == "error" for i in issues)


def validate_industry_space_source_search_pipeline(workbench: dict[str, Any]) -> dict[str, Any]:
    """Validate that every BOM node has an active five-bucket source-search plan."""
    issues: list[dict[str, str]] = []
    if not isinstance(workbench, dict):
        return {"ok": True, "issues": issues, "summary": {}}
    evidence_pack = workbench.get("industry_space_evidence_pack") or []
    if not isinstance(evidence_pack, list) or not evidence_pack:
        return {"ok": True, "issues": issues, "summary": {"industry_space_nodes": 0}}

    matrix_rows = workbench.get("industry_space_source_search_matrix") or []
    matrix_by_node = {
        str(row.get("node")): row
        for row in matrix_rows
        if isinstance(row, dict) and row.get("node")
    } if isinstance(matrix_rows, list) else {}

    validated_nodes = 0
    for node_row in evidence_pack:
        if not isinstance(node_row, dict):
            continue
        node_name = str(node_row.get("node") or "")
        sizing = node_row.get("publicSizingMethods") or node_row.get("public_sizing_methods") or {}
        matrix_row = matrix_by_node.get(node_name, {})
        source_plan = (
            matrix_row.get("category_search_plan")
            or matrix_row.get("source_search_plan")
            or (sizing.get("sourceSearchPlan") if isinstance(sizing, dict) else None)
            or (sizing.get("source_search_plan") if isinstance(sizing, dict) else None)
        )
        normalized_plan = _normalize_industry_space_source_search_plan(source_plan)
        if not normalized_plan:
            _issue(
                issues,
                "error",
                "missing_industry_space_source_search_plan",
                f"{node_name or '<unknown>'} must actively search 公司指引 / 公司 TAM / 客户侧指引 / 第三方拆法 / 财务兑现证据 after BOM node identification",
            )
            continue
        validated_nodes += 1
        method_counts = _industry_space_method_counts((sizing or {}).get("methods") if isinstance(sizing, dict) else [])
        for category_key, category_label in INDUSTRY_SPACE_SOURCE_SEARCH_CATEGORIES:
            entry = normalized_plan.get(category_key) or normalized_plan.get(category_label)
            if not isinstance(entry, dict):
                _issue(
                    issues,
                    "error",
                    "missing_industry_space_source_search_category",
                    f"{node_name or '<unknown>'} is missing active source-search category {category_label}",
                )
                continue
            status = str(entry.get("status") or entry.get("search_status") or "").strip()
            source_ids = entry.get("sourceIds") or entry.get("source_ids") or []
            if not isinstance(source_ids, list):
                source_ids = [source_ids] if source_ids else []
            if _is_empty(entry.get("search_query")) and _is_empty(entry.get("search_terms")):
                _issue(
                    issues,
                    "error",
                    "industry_space_source_search_missing_query",
                    f"{node_name or '<unknown>'} / {category_label} needs explicit search_query or search_terms",
                )
            if _is_empty(entry.get("expected_fields")):
                _issue(
                    issues,
                    "error",
                    "industry_space_source_search_missing_expected_fields",
                    f"{node_name or '<unknown>'} / {category_label} needs expected_fields for source parsing",
                )
            if _is_empty(entry.get("allowed_usage")):
                _issue(
                    issues,
                    "error",
                    "industry_space_source_search_missing_allowed_usage",
                    f"{node_name or '<unknown>'} / {category_label} needs allowed_usage",
                )
            if _is_empty(entry.get("preferred_parser_skill")):
                _issue(
                    issues,
                    "error",
                    "industry_space_source_search_missing_parser_skill",
                    f"{node_name or '<unknown>'} / {category_label} needs preferred_parser_skill",
                )
            if _is_empty(entry.get("priority_sources")):
                _issue(
                    issues,
                    "error",
                    "industry_space_source_search_missing_priority_sources",
                    f"{node_name or '<unknown>'} / {category_label} needs domain-specific priority_sources such as SemiAnalysis, TrendForce, Omdia, company IR, or customer IR",
                )
            if _is_empty(entry.get("directed_queries")):
                _issue(
                    issues,
                    "error",
                    "industry_space_source_search_missing_directed_queries",
                    f"{node_name or '<unknown>'} / {category_label} needs site/domain directed_queries instead of only broad keyword search",
                )
            if method_counts.get(category_key, 0) > 0 and (status != "found" or not source_ids):
                _issue(
                    issues,
                    "error",
                    "industry_space_source_search_entry_without_found_plan",
                    f"{node_name or '<unknown>'} / {category_label} has rendered entries but source-search plan is not found with source_ids",
                )
            if method_counts.get(category_key, 0) == 0 and status != "gap" and not source_ids:
                _issue(
                    issues,
                    "error",
                    "industry_space_source_search_gap_not_marked",
                    f"{node_name or '<unknown>'} / {category_label} has no selected source; mark status=gap with gap_reason instead of leaving it implicit",
                )
            if status == "gap" and _is_empty(entry.get("gap_reason")):
                _issue(
                    issues,
                    "error",
                    "industry_space_source_search_gap_missing_reason",
                    f"{node_name or '<unknown>'} / {category_label} gap needs gap_reason",
                )

    return {
        "ok": not any(issue["severity"] == "error" for issue in issues),
        "summary": {
            "industry_space_nodes": len([row for row in evidence_pack if isinstance(row, dict)]),
            "validated_source_search_nodes": validated_nodes,
            "required_categories_per_node": len(INDUSTRY_SPACE_SOURCE_SEARCH_CATEGORIES),
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
    adaptive_tree = qa_tree.get("question_tree_contract") == "adaptive-depth-max-5"
    research_unit_nodes = [
        node
        for node in nodes
        if RESEARCH_UNIT_MIN_LEVEL <= _level_number(node.get("level")) <= MAX_QA_DEPTH
        and (not adaptive_tree or not (node.get("next_question_ids") or []))
    ]
    too_deep_nodes = [node for node in nodes if _level_number(node.get("level")) > MAX_QA_DEPTH]

    if not l1_nodes:
        _issue(issues, "error", "missing_l1", "QA tree must include L1 nodes")
    if not l2_nodes:
        _issue(issues, "error", "missing_l2", "QA tree must include L2 mechanism buckets")
    if require_l3 and not l3_nodes:
        _issue(issues, "error", "missing_l3", "complete QA trees must include L3 evidence units")
    for node in too_deep_nodes:
        _issue(
            issues,
            "error",
            "qa_depth_exceeds_max",
            f"{node.get('id', '<unknown>')} exceeds maximum adaptive QA depth L{MAX_QA_DEPTH}",
        )

    for node in nodes:
        node_id = str(node.get("id", ""))
        for child_id in node.get("next_question_ids", []) or []:
            child = nodes_by_id.get(str(child_id))
            if child is None:
                _issue(issues, "error", "missing_child", f"{node_id} points to missing child {child_id}")
                continue
            if str(child.get("parent_id", "")) not in {node_id, ""}:
                _issue(issues, "error", "broken_parent_link", f"{child_id} has a mismatched parent_id")

    if adaptive_tree:
        for node in l3_nodes:
            node_id = str(node.get("id") or "")
            if _is_empty(node.get("child_plan_path")):
                _issue(
                    issues,
                    "error",
                    "l3_missing_child_plan",
                    f"{node_id} must reference its independent L3 child plan",
                )

    for node in research_unit_nodes:
        node_id = str(node.get("id", ""))
        if adaptive_tree:
            for field in (
                "required_data",
                "analysis_plan",
                "research_step_id",
                "source_plan",
                "minimum_evidence_gate",
                "refuting_source_plan",
            ):
                if _is_empty(node.get(field)):
                    _issue(
                        issues,
                        "error",
                        "leaf_missing_field",
                        f"{node_id} is missing {field}",
                    )
            _validate_l3_source_plan(node, node_id, issues)
            continue
        child_plan_rollup = (
            _level_number(node.get("level")) == 3
            and str(node.get("execution_mode") or "")
            == "child_plan_rollup"
        )
        required_fields = [
            field
            for field in L3_REQUIRED_FIELDS
            if not (child_plan_rollup and field == "source_plan")
        ]
        for field in required_fields:
            if _is_empty(node.get(field)):
                _issue(issues, "error", "l3_missing_field", f"{node_id} is missing {field}")
        if child_plan_rollup:
            if _is_empty(node.get("child_plan_path")):
                _issue(
                    issues,
                    "error",
                    "l3_missing_child_plan",
                    f"{node_id} must reference its independent L3 child plan",
                )
        else:
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
            "research_unit_nodes": len(research_unit_nodes),
            "max_depth": max((_level_number(node.get("level")) for node in nodes), default=0),
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
        if not _is_research_unit_level(node.get("level")):
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
        if not _is_research_unit_level(node.get("level")):
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
        strict_research_gate = bool(target.get("research_gate_required") or target.get("research_gate"))
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
                        status = str(row.get("status") or "scored").strip().lower()
                        is_gap = status in {"gap", "missing", "unverified", "incomplete"}
                        if is_gap and _is_empty(row.get("gap_reason")):
                            _issue(
                                issues,
                                "error",
                                "target_score_gap_missing_reason",
                                f"{ticker} {component}.{row.get('name', '')} must explain its evidence gap",
                            )
                        if not is_gap and _is_empty(row.get("evidence_ids")) and _is_empty(row.get("review_ids")):
                            _issue(
                                issues,
                                "error",
                                "target_score_subcomponent_missing_trace",
                                f"{ticker} {component}.{row.get('name', '')} needs evidence_ids or review_ids",
                            )
                        if strict_research_gate and not is_gap:
                            if _is_empty(row.get("evidence_role")):
                                _issue(
                                    issues,
                                    "error",
                                    "target_score_subcomponent_missing_evidence_role",
                                    f"{ticker} {component}.{row.get('name', '')} must identify the evidence role",
                                )
                            if _is_empty(row.get("rationale")):
                                _issue(
                                    issues,
                                    "error",
                                    "target_score_subcomponent_missing_rationale",
                                    f"{ticker} {component}.{row.get('name', '')} must preserve a component-specific rationale",
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
        if strict_research_gate:
            gate = target.get("research_gate")
            if not isinstance(gate, dict):
                _issue(
                    issues,
                    "error",
                    "target_missing_research_gate",
                    f"{ticker} must persist research_gate before recommendation rendering",
                )
            elif action_state == "actionable_long" and not gate.get("passed"):
                _issue(
                    issues,
                    "error",
                    "actionable_target_failed_research_gate",
                    f"{ticker} cannot be actionable_long while research_gate.passed is false",
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
                    required_kill_test_fields = [
                        "test",
                        "evidence_needed",
                        "downgrade_action",
                        "source_plan",
                    ]
                    if strict_research_gate:
                        required_kill_test_fields.extend(
                            ["trigger_metric", "threshold", "observation_frequency"]
                        )
                    if not isinstance(kill_test, dict) or any(
                        _is_empty(kill_test.get(field)) for field in required_kill_test_fields
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

    source_audit = {"summary": {}}
    if as_of_date and sources is not None:
        source_audit = audit_time_slice_sources(sources, as_of_date=as_of_date)
        issues.extend(source_audit.get("issues", []))

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
        if not _is_research_unit_level(node.get("level")):
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
            "post_cutoff_non_label_count": int(
                source_audit.get("summary", {}).get("post_cutoff_non_label_count", 0) or 0
            ),
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
        "event": "event_conference",
        "conference": "event_conference",
        "keynote": "event_conference",
        "launch": "event_conference",
        "gtc": "event_conference",
        "gtc_taipei": "event_conference",
        "大会": "event_conference",
        "发布会": "event_conference",
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


def _open_details_class_count(html: str, *classes: str) -> int:
    count = 0
    for match in re.finditer(r"<details\b([^>]*)>", html, flags=re.IGNORECASE | re.DOTALL):
        attrs = match.group(1)
        if not re.search(r"\bopen\b", attrs, flags=re.IGNORECASE):
            continue
        class_match = re.search(r"class\s*=\s*(['\"])(.*?)\1", attrs, flags=re.IGNORECASE | re.DOTALL)
        if not class_match:
            continue
        class_set = set(class_match.group(2).split())
        if all(class_name in class_set for class_name in classes):
            count += 1
    return count


def _css_class_has_single_column_stack(html: str, class_name: str) -> bool:
    css_rule_pattern = r"([^{}]+)\{([^{}]*)\}"
    class_token = re.compile(rf"(?<![-\w])\.{re.escape(class_name)}(?![-\w])", re.IGNORECASE)
    for match in re.finditer(css_rule_pattern, html, flags=re.IGNORECASE | re.DOTALL):
        selector = match.group(1)
        if not class_token.search(selector):
            continue
        body = re.sub(r"\s+", "", match.group(2)).lower()
        if "grid-template-columns:1fr" in body and "grid-auto-flow:column" not in body:
            return True
    return False


def _css_class_rule_defined(html: str, class_name: str) -> bool:
    return re.search(rf"\.{re.escape(class_name)}\s*\{{", html, flags=re.IGNORECASE) is not None


def _class_position(html: str, *classes: str, start: int = 0) -> int:
    for match in re.finditer(r"class\s*=\s*(['\"])(.*?)\1", html[start:], flags=re.IGNORECASE | re.DOTALL):
        class_set = set(match.group(2).split())
        if all(class_name in class_set for class_name in classes):
            return start + match.start()
    return -1


def _class_region(html: str, start_classes: tuple[str, ...], end_class_options: list[tuple[str, ...]]) -> str:
    start = _class_position(html, *start_classes)
    if start < 0:
        return ""
    ends = [
        pos
        for pos in (_class_position(html, *classes, start=start + 1) for classes in end_class_options)
        if pos >= 0
    ]
    end = min(ends) if ends else len(html)
    return html[start:end]


def _section_region(html: str, start_label: str, end_label: str) -> str:
    start = html.find(start_label)
    if start < 0:
        return ""
    end = html.find(end_label, start + len(start_label))
    return html[start : end if end >= 0 else len(html)]


def _strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    return " ".join(text.split())


def _bom_taxonomy_nodes(html: str) -> list[str]:
    nodes: list[str] = []
    pattern = r"<article\b(?=[^>]*class\s*=\s*(['\"])[^'\"]*\bbom-taxonomy-card\b[^'\"]*\1)[^>]*>(.*?)</article>"
    for match in re.finditer(pattern, html, flags=re.IGNORECASE | re.DOTALL):
        card_html = match.group(2)
        card_text = _strip_html(card_html)
        strong_match = re.search(r"<strong\b[^>]*>(.*?)</strong>", card_html, flags=re.IGNORECASE | re.DOTALL)
        label = _strip_html(strong_match.group(1)) if strong_match else ""
        if not label:
            continue
        if label == "核心 BOM 节点" or "非 BOM" in card_text or "需求验证" in card_text or "客户需求" in label:
            continue
        if label not in nodes:
            nodes.append(label)
    return nodes


def _missing_taxonomy_nodes(region_html: str, nodes: list[str]) -> list[str]:
    region_text = _strip_html(region_html)
    return [node for node in nodes if node not in region_text]


def _qa_level_counts(html: str) -> dict[str, int]:
    return {
        f"level{level}_cards": _class_count(html, "qa-card", f"level-{level}")
        for level in range(1, MAX_QA_DEPTH + 1)
    }


def _interactive_qa_level_counts(html: str) -> dict[str, int]:
    return {
        f"interactive_level{level}_cards": _tag_class_count(html, "details", "qa-card", f"level-{level}")
        for level in range(1, MAX_QA_DEPTH + 1)
    }


def _research_unit_card_count(level_counts: dict[str, int]) -> int:
    return sum(
        level_counts.get(f"level{level}_cards", 0)
        for level in range(RESEARCH_UNIT_MIN_LEVEL, MAX_QA_DEPTH + 1)
    )


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


def _is_research_unit_level(value: Any) -> bool:
    level = _level_number(value)
    return RESEARCH_UNIT_MIN_LEVEL <= level <= MAX_QA_DEPTH


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


def _normalize_industry_space_source_search_plan(source_plan: Any) -> dict[str, dict[str, Any]]:
    normalized: dict[str, dict[str, Any]] = {}
    if isinstance(source_plan, dict):
        for category_key, category_label in INDUSTRY_SPACE_SOURCE_SEARCH_CATEGORIES:
            entry = source_plan.get(category_key) or source_plan.get(category_label)
            if isinstance(entry, dict):
                entry = dict(entry)
                entry.setdefault("category", category_key)
                entry.setdefault("source_type", category_label)
                normalized[category_key] = entry
                normalized[category_label] = entry
        return normalized
    if isinstance(source_plan, list):
        for item in source_plan:
            if not isinstance(item, dict):
                continue
            text = " ".join(str(item.get(field) or "") for field in ("category", "source_type", "label"))
            category_key = _industry_space_category_key(text)
            if not category_key:
                continue
            entry = dict(item)
            label = dict(INDUSTRY_SPACE_SOURCE_SEARCH_CATEGORIES).get(category_key, category_key)
            entry.setdefault("category", category_key)
            entry.setdefault("source_type", label)
            normalized[category_key] = entry
            normalized[label] = entry
    return normalized


def _industry_space_method_counts(methods: Any) -> dict[str, int]:
    counts = {key: 0 for key, _label in INDUSTRY_SPACE_SOURCE_SEARCH_CATEGORIES}
    if not isinstance(methods, list):
        return counts
    for method in methods:
        if isinstance(method, dict):
            text = " ".join(
                str(method.get(field) or "")
                for field in (
                    "sourceType",
                    "source_type",
                    "type",
                    "organization",
                    "company",
                    "source",
                    "guidanceContent",
                    "guidance_content",
                    "guidance",
                    "value",
                    "method",
                )
            )
        elif isinstance(method, (list, tuple)):
            text = " ".join(str(item or "") for item in method[:4])
        else:
            text = str(method or "")
        category_key = _industry_space_category_key(text) or "third_party"
        counts[category_key] = counts.get(category_key, 0) + 1
    return counts


def _industry_space_category_key(text: str) -> str:
    lower = text.lower()
    if "客户侧" in text or "客户指引" in text or "customer" in lower:
        return "customer_guidance"
    if "公司 tam" in lower or "TAM" in text or "市场空间" in text or "可触达市场" in text:
        return "company_tam"
    if "第三方" in text or "研报" in text or "机构" in text or "预测" in text or "数据商" in text or "sell-side" in lower or "forecast" in lower or "industry" in lower:
        return "third_party"
    if "公司指引" in text or "指引" in text or "预计" in text or "guidance" in lower or "outlook" in lower or "expected" in lower:
        return "company_guidance"
    if "经营验证" in text or "财务兑现" in text or "公司财报" in text or "财报" in text or "收入" in text or "订单" in text or "利润" in text or "现金" in text or any(token in lower for token in ("revenue", "order", "backlog", "margin", "cash")):
        return "financial_evidence"
    return ""


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
                "evidence_role": row.get("evidence_role", ""),
                "gap_reason": row.get("gap_reason", ""),
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

    if target.get("research_gate_required"):
        if target.get("bom_research_complete") is not True:
            gate_reasons.append("bom_six_question_incomplete")
            max_total_score = min(max_total_score, 3.49)
        if str(target.get("refutation_status") or "").strip().lower() not in {
            "complete",
            "completed",
            "ok",
            "verified",
            "verified_with_caveats",
        }:
            gate_reasons.append("refutation_evidence_unverified")
            max_total_score = min(max_total_score, 3.49)
        if valuation_status not in {"complete", "completed", "ok", "verified", "verified_with_caveats"}:
            if "valuation_unverified" not in gate_reasons:
                gate_reasons.append("valuation_unverified")
            max_total_score = min(max_total_score, 3.49)
        exposure_status = str(target.get("company_exposure_status") or "").strip().lower()
        if exposure_status not in {
            "complete",
            "completed",
            "ok",
            "verified",
            "verified_with_caveats",
        }:
            gate_reasons.append("company_exposure_unverified")
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
