import unittest
from pathlib import Path

from value_invest_research.adapters.outbound.standalone_bom_html_renderer import (
    StandaloneBomHtmlRenderer,
)
from value_invest_research.adapters.outbound.standalone_bom_markdown_renderer import (
    StandaloneBomMarkdownRenderer,
)
from value_invest_research.domain.standalone_bom_investment_engine import (
    build_standalone_investment_view,
    normalize_claim_mapping,
    normalize_entity_state,
    normalize_investment_snapshot,
    normalize_logic_state,
    normalize_thesis_revision,
    validate_standalone_bom_investment_bundle,
    validate_standalone_bom_playbook,
)


def _profile():
    return {
        "schema_version": "2.0",
        "bom_node_id": "gpu_asic",
        "lenses": [
            {
                "lens_id": lens_id,
                "logic_chain": f"{lens_id} logic",
                "logic_nodes": [
                    {
                        "logic_node_id": f"{lens_id}.node",
                        "title": f"{label}节点",
                        "question": f"{label}是否成立？",
                        "support_rule": "直接事实支持。",
                        "refute_rule": "直接事实反证。",
                        "downstream_node_ids": [],
                    }
                ],
            }
            for lens_id, label in (
                ("demand", "需求"),
                ("supply", "供给"),
                ("technology", "技术"),
                ("valuation", "估值"),
                ("esg", "ESG"),
            )
        ],
    }


def _claim():
    return {
        "claim_id": "CLM-1",
        "bom_node_id": "gpu_asic",
        "lens_id": "demand",
        "source_id": "SRC-1",
        "published_at": "2026-07-23",
        "material_class": "official_company",
        "ingestion_channel": "question_search",
        "source_title": "Official result",
        "source_url": "https://example.com/result",
        "source_location": "results",
        "statement": "AI accelerator orders increased.",
    }


class StandaloneBomInvestmentEngineTests(unittest.TestCase):
    def test_logic_chain_centered_playbook_requires_version_and_public_causal_nodes(self):
        profile = _profile()
        profile["research_model"] = "logic_chain_centered"
        with self.assertRaisesRegex(ValueError, "logic_chain_version"):
            validate_standalone_bom_playbook(profile)

        profile["logic_chain_version"] = "2026-08-11.v1"
        profile["lenses"][0]["logic_nodes"].append(
            {
                "logic_node_id": "demand.derived",
                "title": "需求方派生视图",
                "question": "谁在产生需求？",
                "support_rule": "主体有可验证采购。",
                "refute_rule": "采购通道被误作最终需求方。",
                "downstream_node_ids": [],
                "presentation_role": "derived_view",
            }
        )
        profile["lenses"][0]["public_logic_node_ids"] = ["demand.derived"]
        with self.assertRaisesRegex(ValueError, "causal nodes"):
            validate_standalone_bom_playbook(profile)

        profile["lenses"][0]["public_logic_node_ids"] = [
            "demand.node",
            "demand.derived",
        ]
        index = validate_standalone_bom_playbook(profile)
        self.assertEqual(
            index["nodes"]["demand.derived"]["presentation_role"],
            "derived_view",
        )

    def test_playbook_requires_all_five_lenses_and_namespaced_nodes(self):
        index = validate_standalone_bom_playbook(_profile())
        self.assertEqual(len(index["nodes"]), 5)

        invalid = _profile()
        invalid["lenses"][0]["logic_nodes"][0]["logic_node_id"] = "supply.wrong"
        with self.assertRaisesRegex(ValueError, "namespaced"):
            validate_standalone_bom_playbook(invalid)

    def test_demand_party_list_requires_two_ordered_non_empty_groups(self):
        profile = _profile()
        demand_node = profile["lenses"][0]["logic_nodes"][0]
        demand_node["render_mode"] = "demand_party_list"
        demand_node["demand_parties"] = {
            "current": ["当前主体"],
            "potential_future": ["未来主体"],
        }
        validate_standalone_bom_playbook(profile)

        demand_node["demand_parties"] = {
            "potential_future": ["未来主体"],
            "current": ["当前主体"],
        }
        with self.assertRaisesRegex(ValueError, "current then potential_future"):
            validate_standalone_bom_playbook(profile)

    def test_claim_mapping_accepts_boundary_effect(self):
        profile = _profile()
        claim = _claim()
        mapping = normalize_claim_mapping(
            {
                "claim_id": "CLM-1",
                "logic_node_id": "demand.node",
                "direction": "boundary",
                "rationale": "该观点改变需求传导成立的适用边界。",
            },
            claims_by_id={"CLM-1": claim},
            profile=profile,
            mapped_at="2026-08-11",
        )
        self.assertEqual(mapping["direction"], "boundary")

    def test_public_logic_node_subset_preserves_internal_research_nodes(self):
        profile = _profile()
        demand_nodes = profile["lenses"][0]["logic_nodes"]
        demand_nodes.append(
            {
                "logic_node_id": "demand.internal",
                "title": "内部研究节点",
                "question": "内部研究是否继续保留？",
                "support_rule": "内部证据支持。",
                "refute_rule": "内部证据反证。",
                "downstream_node_ids": [],
            }
        )
        profile["lenses"][0]["public_logic_node_ids"] = ["demand.node"]

        index = validate_standalone_bom_playbook(profile)
        self.assertEqual(len(index["lens_nodes"]["demand"]), 2)
        self.assertEqual(len(index["public_lens_nodes"]["demand"]), 1)

        view = build_standalone_investment_view(
            project={
                "title": "GPU / ASIC",
                "report_scope": "standalone-bom",
                "bom_node_id": "gpu_asic",
            },
            profile=profile,
            claims=[],
            conclusions=[],
            claim_mappings=[],
            logic_states=[],
            entity_states=[],
            thesis_revisions=[],
            investment_snapshots=[],
            as_of_date="2026-08-06",
        )
        self.assertEqual(
            [node["logic_node_id"] for node in view["lenses"][0]["logic_nodes"]],
            ["demand.node"],
        )
        self.assertEqual(view["engine_coverage"]["logic_nodes"], 6)
        self.assertEqual(view["engine_coverage"]["public_logic_nodes"], 5)
        html = StandaloneBomHtmlRenderer(Path("/tmp")).render(view)
        markdown = StandaloneBomMarkdownRenderer(Path("/tmp")).render(view)
        self.assertNotIn("内部研究节点", html)
        self.assertNotIn("内部研究节点", markdown)

        profile["lenses"][0]["public_logic_node_ids"] = [
            "demand.internal",
            "demand.node",
        ]
        with self.assertRaisesRegex(ValueError, "preserve logic-node order"):
            validate_standalone_bom_playbook(profile)

    def test_public_quantity_matrix_requires_public_q1_classification(self):
        profile = _profile()
        demand_node = profile["lenses"][0]["logic_nodes"][0]
        demand_node.update(
            {
                "title": "Q1 需求方",
                "render_mode": "demand_party_list",
                "demand_parties": {
                    "current": ["云服务商"],
                    "potential_future": ["传统企业"],
                },
            }
        )
        profile["lenses"][0]["logic_nodes"].append(
            {
                "logic_node_id": "demand.quantity",
                "title": "Q2 当前需求量基线",
                "question": "各类需求方当前需求量是多少？",
                "support_rule": "逐类搜索。",
                "refute_rule": "不机械分摊。",
                "downstream_node_ids": [],
                "render_mode": "demand_quantity_matrix",
                "classification_node_id": "demand.node",
            }
        )
        profile["lenses"][0]["public_logic_node_ids"] = ["demand.quantity"]
        with self.assertRaisesRegex(ValueError, "requires classification node"):
            validate_standalone_bom_playbook(profile)

    def test_demand_party_list_renders_only_current_and_future_demanders(self):
        profile = _profile()
        demand_node = profile["lenses"][0]["logic_nodes"][0]
        demand_node.update(
            {
                "title": "Q1 需求方",
                "render_mode": "demand_party_list",
                "demand_parties": {
                    "current": ["超大规模云服务商", "AI 模型公司"],
                    "potential_future": ["传统企业", "电信与边缘云运营商"],
                },
            }
        )
        view = build_standalone_investment_view(
            project={
                "title": "GPU / ASIC",
                "report_scope": "standalone-bom",
                "bom_node_id": "gpu_asic",
            },
            profile=profile,
            claims=[],
            conclusions=[],
            claim_mappings=[],
            logic_states=[],
            entity_states=[],
            thesis_revisions=[],
            investment_snapshots=[],
            as_of_date="2026-08-01",
        )

        html = StandaloneBomHtmlRenderer(Path("/tmp")).render(view)
        party_html = html.split('data-render-mode="demand-party-list"', 1)[1].split(
            "</article>", 1
        )[0]
        self.assertIn('data-demand-party-group="current"', party_html)
        self.assertIn('data-demand-party-group="potential_future"', party_html)
        self.assertIn("超大规模云服务商", party_html)
        self.assertIn("传统企业", party_html)
        self.assertNotIn("state-badge", party_html)
        self.assertNotIn("entity-module", party_html)
        self.assertNotIn("截面变化与评估", party_html)

        markdown = StandaloneBomMarkdownRenderer(Path("/tmp")).render(view)
        party_markdown = markdown.split("#### Q1 需求方", 1)[1].split("####", 1)[0]
        self.assertIn("**当前需求方**", party_markdown)
        self.assertIn("**潜在未来需求方**", party_markdown)
        self.assertNotIn("**当前结论：**", party_markdown)
        self.assertNotIn("**截面变化与评估：**", party_markdown)

    def test_demand_quantity_matrix_inherits_q1_and_separates_other_forecasts(self):
        claims = []
        for claim_id, source_id, material_class, title in (
            ("CLM-OFFICIAL", "SRC-OFFICIAL", "official_filing", "Official filing"),
            ("CLM-SELLSIDE", "SRC-SELLSIDE", "sell_side_research", "Sell-side report"),
            ("CLM-COMPANY", "SRC-COMPANY", "official_company", "Company release"),
            ("CLM-THIRD", "SRC-THIRD", "authoritative_third_party", "Third-party research"),
            ("CLM-FUTURE", "SRC-FUTURE", "market_news", "Future demander news"),
        ):
            claims.append(
                {
                    **_claim(),
                    "claim_id": claim_id,
                    "source_id": source_id,
                    "material_class": material_class,
                    "source_title": title,
                }
            )
        claims_by_id = {row["claim_id"]: row for row in claims}
        profile = _profile()
        demand_node = profile["lenses"][0]["logic_nodes"][0]
        demand_node.update(
            {
                "title": "Q1 需求方",
                "render_mode": "demand_party_list",
                "demand_parties": {
                    "current": ["云服务商", "模型公司"],
                    "potential_future": ["传统企业"],
                },
            }
        )
        profile["lenses"][0]["logic_nodes"].append(
            {
                "logic_node_id": "demand.quantity",
                "title": "Q2 当前需求量基线",
                "question": "各类需求方当前需求量是多少？",
                "support_rule": "逐类搜索。",
                "refute_rule": "不机械分摊。",
                "downstream_node_ids": [],
                "render_mode": "demand_quantity_matrix",
                "classification_node_id": "demand.node",
            }
        )
        state = normalize_logic_state(
            {
                "logic_node_id": "demand.quantity",
                "conclusion": "当前、潜在未来与其它分类已分开。",
                "demand_quantity_rows": [
                    {
                        "forecast_group": "classified",
                        "demand_party": "云服务商",
                        "metric": "GPU数量",
                        "quantity": "10万颗",
                        "target_period": "当前",
                        "mapping_quality": "direct",
                        "claim_ids": ["CLM-OFFICIAL"],
                        "caveat": "官方披露。",
                    },
                    {
                        "forecast_group": "classified",
                        "demand_party": "云服务商",
                        "metric": "供应商收入",
                        "quantity": "100亿元",
                        "target_period": "当前",
                        "mapping_quality": "proxy",
                        "claim_ids": ["CLM-SELLSIDE"],
                        "caveat": "收入是数量代理。",
                    },
                    {
                        "forecast_group": "classified",
                        "demand_party": "模型公司",
                        "metric": "GPU数量",
                        "quantity": "20万颗",
                        "target_period": "当前",
                        "mapping_quality": "sample",
                        "claim_ids": ["CLM-COMPANY"],
                        "caveat": "单一公司样本。",
                    },
                    {
                        "forecast_group": "potential_future",
                        "demand_party": "传统企业",
                        "metric": "试点部署",
                        "quantity": "3个项目",
                        "target_period": "2027E",
                        "mapping_quality": "sample",
                        "claim_ids": ["CLM-FUTURE"],
                        "caveat": "仅为潜在需求方样本。",
                    },
                    {
                        "forecast_group": "other",
                        "metric": "全球AI服务器",
                        "quantity": "100万台",
                        "target_period": "2026E",
                        "mapping_quality": "unmapped",
                        "claim_ids": ["CLM-THIRD"],
                        "caveat": "无法分配到需求方。",
                    },
                ],
            },
            profile=profile,
            claims_by_id=claims_by_id,
            as_of_date="2026-08-01",
        )
        view = build_standalone_investment_view(
            project={
                "title": "GPU / ASIC",
                "report_scope": "standalone-bom",
                "bom_node_id": "gpu_asic",
            },
            profile=profile,
            claims=claims,
            conclusions=[],
            claim_mappings=[],
            logic_states=[state],
            entity_states=[],
            thesis_revisions=[],
            investment_snapshots=[],
            as_of_date="2026-08-01",
        )

        html = StandaloneBomHtmlRenderer(Path("/tmp")).render(view)
        quantity_html = html.split(
            'data-render-mode="demand-quantity-matrix"', 1
        )[1].split("</article>", 1)[0]
        self.assertLess(
            quantity_html.find("当前需求方"),
            quantity_html.find("潜在未来需求方"),
        )
        self.assertLess(
            quantity_html.find("潜在未来需求方"),
            quantity_html.find("其它分类"),
        )
        self.assertIn("云服务商", quantity_html)
        self.assertIn("传统企业", quantity_html)
        self.assertIn("全球AI服务器", quantity_html)
        self.assertEqual(quantity_html.count('class="demand-quantity-tier"'), 3)
        self.assertEqual(
            quantity_html.count('class="demand-quantity-category"'),
            4,
        )
        self.assertEqual(quantity_html.count("data-demand-category-table"), 4)
        self.assertEqual(
            quantity_html.count('data-demand-quantity-category="云服务商"'),
            1,
        )
        self.assertIn('data-demand-forecast-group="current"', quantity_html)
        self.assertIn(
            'data-demand-forecast-group="potential_future"', quantity_html
        )
        self.assertIn('data-demand-forecast-group="other"', quantity_html)
        self.assertNotIn('<details class="demand-quantity-tier" open', quantity_html)
        self.assertNotIn(
            '<details class="demand-quantity-category" open', quantity_html
        )
        self.assertIn("2 条信息", quantity_html)
        self.assertEqual(
            quantity_html.count(
                "<th>来源</th><th>期间</th><th>信息类型</th><th>具体信息</th>"
            ),
            4,
        )
        for label in ("官方财报", "第三方研究", "市场消息", "机构研报"):
            self.assertIn(label, quantity_html)
        self.assertNotIn("entity-module", quantity_html)

        markdown = StandaloneBomMarkdownRenderer(Path("/tmp")).render(view)
        quantity_markdown = markdown.split("#### Q2 当前需求量基线", 1)[1].split(
            "\n#### ", 1
        )[0]
        self.assertLess(
            quantity_markdown.find("##### 1. 当前需求方"),
            quantity_markdown.find("##### 2. 潜在未来需求方"),
        )
        self.assertLess(
            quantity_markdown.find("##### 2. 潜在未来需求方"),
            quantity_markdown.find("##### 3. 其它分类"),
        )
        self.assertEqual(quantity_markdown.count("###### 云服务商"), 1)
        self.assertEqual(quantity_markdown.count("###### 传统企业"), 1)
        self.assertEqual(quantity_markdown.count("###### 全球AI服务器"), 1)
        self.assertIn("GPU数量", quantity_markdown)
        self.assertIn("供应商收入", quantity_markdown)
        self.assertIn("试点部署", quantity_markdown)
        self.assertEqual(
            quantity_markdown.count(
                "| 来源 | 期间 | 信息类型 | 具体信息 |"
            ),
            4,
        )
        for label in ("官方财报", "第三方研究", "市场消息", "机构研报"):
            self.assertIn(label, quantity_markdown)

    def test_mapping_is_separate_from_immutable_claim(self):
        claim = _claim()
        mapping = normalize_claim_mapping(
            {
                "claim_id": "CLM-1",
                "logic_node_id": "demand.node",
                "mapping_role": "primary",
                "direction": "support",
                "evidence_nature": "fact",
                "directness": "direct",
                "novelty": "new",
                "materiality": "high",
                "rationale": "The order fact directly tests demand.",
                "entities": ["AMD"],
            },
            claims_by_id={"CLM-1": claim},
            profile=_profile(),
            mapped_at="2026-07-24",
        )
        self.assertEqual(mapping["logic_node_id"], "demand.node")
        self.assertEqual(mapping["entities"], ["AMD"])
        self.assertNotIn("logic_node_id", claim)

    def test_first_snapshot_can_be_a_baseline_without_fake_previous_state(self):
        claim = _claim()
        revision = normalize_thesis_revision(
            {
                "revision_type": "baseline",
                "logic_node_id": "demand.node",
                "new_state": "strengthening",
                "rationale": "First structured snapshot.",
                "trigger_claim_ids": ["CLM-1"],
            },
            profile=_profile(),
            claims_by_id={"CLM-1": claim},
            as_of_date="2026-07-24",
        )
        self.assertEqual(revision["previous_state"], "")
        self.assertEqual(revision["revision_type"], "baseline")

    def test_actionable_long_requires_every_gate_and_kill_test(self):
        with self.assertRaisesRegex(ValueError, "semantic gates"):
            normalize_investment_snapshot(
                {
                    "action_state": "actionable_long",
                    "summary": "Looks attractive.",
                    "gate_results": {"logic_coverage": True},
                    "kill_tests": [],
                },
                profile=_profile(),
                claims_by_id={"CLM-1": _claim()},
                as_of_date="2026-07-24",
            )

    def test_view_maps_claims_to_logic_state_before_investment_snapshot(self):
        profile = _profile()
        claim = _claim()
        mapping = normalize_claim_mapping(
            {
                "claim_id": "CLM-1",
                "logic_node_id": "demand.node",
                "direction": "support",
                "evidence_nature": "fact",
                "directness": "direct",
                "novelty": "new",
                "materiality": "high",
                "rationale": "Order growth tests the demand node.",
                "entities": ["AMD"],
            },
            claims_by_id={"CLM-1": claim},
            profile=profile,
            mapped_at="2026-07-24",
        )
        secondary_mapping = normalize_claim_mapping(
            {
                "claim_id": "CLM-1",
                "logic_node_id": "supply.node",
                "mapping_role": "secondary",
                "direction": "support",
                "evidence_nature": "fact",
                "directness": "indirect",
                "novelty": "new",
                "materiality": "medium",
                "rationale": "The same order also tests effective supply.",
                "entities": ["AMD"],
            },
            claims_by_id={"CLM-1": claim},
            profile=profile,
            mapped_at="2026-07-24",
        )
        state = normalize_logic_state(
            {
                "logic_node_id": "demand.node",
                "state": "strengthening",
                "conclusion": "Demand evidence is improving.",
                "support_claim_ids": ["CLM-1"],
                "next_validation": "Verify shipment and revenue.",
            },
            profile=profile,
            claims_by_id={"CLM-1": claim},
            as_of_date="2026-07-24",
        )
        entity_state = normalize_entity_state(
            {
                "logic_node_id": "demand.node",
                "entity_name": "AMD",
                "assessment": "AMD order evidence improved.",
                "change_summary": "First entity-level baseline.",
                "investment_effect": "positive",
                "support_claim_ids": ["CLM-1"],
                "next_validation": "Verify shipment and revenue.",
            },
            profile=profile,
            claims_by_id={"CLM-1": claim},
            as_of_date="2026-07-24",
        )
        supply_entity_state = normalize_entity_state(
            {
                "logic_node_id": "supply.node",
                "entity_name": "AMD",
                "assessment": "AMD supply evidence improved.",
                "change_summary": "First entity-level baseline.",
                "investment_effect": "positive",
                "support_claim_ids": ["CLM-1"],
            },
            profile=profile,
            claims_by_id={"CLM-1": claim},
            as_of_date="2026-07-24",
        )
        snapshot = normalize_investment_snapshot(
            {
                "action_state": "watch_only",
                "summary": "Demand improved but valuation is missing.",
                "gate_results": {
                    "logic_coverage": True,
                    "company_financial_bridge": False,
                    "valuation": False,
                    "refutation": False,
                    "risk_control": False,
                },
            },
            profile=profile,
            claims_by_id={"CLM-1": claim},
            as_of_date="2026-07-24",
        )
        view = build_standalone_investment_view(
            project={
                "title": "GPU / ASIC",
                "report_scope": "standalone-bom",
                "bom_node_id": "gpu_asic",
            },
            profile=profile,
            claims=[claim],
            conclusions=[],
            claim_mappings=[mapping, secondary_mapping],
            logic_states=[state],
            entity_states=[entity_state, supply_entity_state],
            thesis_revisions=[],
            investment_snapshots=[snapshot],
            as_of_date="2026-07-24",
        )

        demand = view["lenses"][0]
        self.assertEqual(
            demand["claims"][0]["logic_mappings"][0]["logic_node_id"],
            "demand.node",
        )
        self.assertEqual(
            demand["logic_nodes"][0]["state"],
            "strengthening",
        )
        self.assertEqual(
            demand["logic_nodes"][0]["entities"][0]["entity_name"],
            "AMD",
        )
        self.assertEqual(
            demand["logic_nodes"][0]["entities"][0]["claims"][0]["claim_id"],
            "CLM-1",
        )
        self.assertEqual(
            view["lenses"][1]["logic_nodes"][0]["entities"][0]["claims"][0][
                "claim_id"
            ],
            "CLM-1",
        )
        self.assertEqual(view["decision"]["action_state"], "watch_only")
        html = StandaloneBomHtmlRenderer(Path("/tmp")).render(view)
        self.assertIn('class="entity-module"', html)
        self.assertIn("截面变化与评估", html)
        self.assertIn('<th scope="col">材料（含链接）</th>', html)
        self.assertNotIn("<h3 id=\"timeline-demand\">信息时间线</h3>", html)

        revisions = [
            normalize_thesis_revision(
                {
                    "revision_type": "baseline",
                    "logic_node_id": f"{lens_id}.node",
                    "new_state": (
                        "strengthening" if lens_id == "demand" else "unresolved"
                    ),
                    "rationale": "First structured snapshot.",
                    "trigger_claim_ids": (
                        ["CLM-1"] if lens_id == "demand" else []
                    ),
                },
                profile=profile,
                claims_by_id={"CLM-1": claim},
                as_of_date="2026-07-24",
            )
            for lens_id in (
                "demand",
                "supply",
                "technology",
                "valuation",
                "esg",
            )
        ]
        all_states = [
            state,
            *[
                normalize_logic_state(
                    {
                        "logic_node_id": f"{lens_id}.node",
                        "state": "unresolved",
                        "conclusion": "No evidence yet.",
                    },
                    profile=profile,
                    claims_by_id={"CLM-1": claim},
                    as_of_date="2026-07-24",
                )
                for lens_id in ("supply", "technology", "valuation", "esg")
            ],
        ]
        validation = validate_standalone_bom_investment_bundle(
            project={
                "report_scope": "standalone-bom",
                "bom_node_id": "gpu_asic",
            },
            profile=profile,
            claims=[claim],
            claim_mappings=[mapping, secondary_mapping],
            logic_states=all_states,
            entity_states=[entity_state, supply_entity_state],
            thesis_revisions=revisions,
            investment_snapshots=[snapshot],
            as_of_date="2026-07-24",
        )
        self.assertTrue(validation["ok"], validation["issues"])

    def test_logic_chain_view_separates_causal_nodes_and_derived_views(self):
        profile = _profile()
        profile.update(
            {
                "schema_version": "3.0",
                "research_model": "logic_chain_centered",
                "logic_chain_version": "2026-08-11.v1",
            }
        )
        demand_lens = profile["lenses"][0]
        demand_lens["logic_nodes"][0]["presentation_role"] = "causal_node"
        demand_lens["logic_nodes"].append(
            {
                "logic_node_id": "demand.parties",
                "title": "需求方视图",
                "question": "谁在产生需求？",
                "support_rule": "主体有可验证采购。",
                "refute_rule": "采购通道被误作最终需求方。",
                "downstream_node_ids": [],
                "presentation_role": "derived_view",
                "render_mode": "demand_party_list",
                "demand_parties": {
                    "current": ["云服务商"],
                    "potential_future": ["传统企业"],
                },
            }
        )
        claim = _claim()
        mapping = normalize_claim_mapping(
            {
                "claim_id": "CLM-1",
                "logic_node_id": "demand.node",
                "direction": "boundary",
                "rationale": "订单增长仍受交付窗口约束。",
                "downstream_impacts": ["supply.node"],
            },
            claims_by_id={"CLM-1": claim},
            profile=profile,
            mapped_at="2026-08-11",
        )
        state = normalize_logic_state(
            {
                "logic_node_id": "demand.node",
                "state": "strengthening",
                "conclusion": "订单证据增强，但兑现边界仍需验证。",
                "change_summary": "新增交付窗口约束。",
            },
            profile=profile,
            claims_by_id={"CLM-1": claim},
            as_of_date="2026-08-11",
        )
        older_state = normalize_logic_state(
            {
                "logic_node_id": "demand.node",
                "state": "weak",
                "conclusion": "订单线索存在，但尚未形成可验证交付。",
                "change_summary": "首个结构化截面。",
            },
            profile=profile,
            claims_by_id={"CLM-1": claim},
            as_of_date="2026-08-10",
        )
        baseline_revision = normalize_thesis_revision(
            {
                "revision_type": "baseline",
                "logic_node_id": "demand.node",
                "new_state": "weak",
                "rationale": "建立节点历史基线。",
            },
            profile=profile,
            claims_by_id={"CLM-1": claim},
            as_of_date="2026-08-10",
        )
        change_revision = normalize_thesis_revision(
            {
                "revision_type": "change",
                "logic_node_id": "demand.node",
                "previous_state": "weak",
                "new_state": "strengthening",
                "change_direction": "up",
                "rationale": "订单观点增强，但仍受交付窗口约束。",
                "trigger_claim_ids": ["CLM-1"],
            },
            profile=profile,
            claims_by_id={"CLM-1": claim},
            as_of_date="2026-08-11",
        )
        snapshot = normalize_investment_snapshot(
            {
                "action_state": "watch_only",
                "summary": "本期新增订单材料，但仍需验证交付。",
                "positive_node_ids": ["demand.node"],
                "negative_node_ids": ["valuation.node"],
                "gate_results": {
                    "logic_coverage": True,
                    "company_financial_bridge": False,
                    "valuation": False,
                    "refutation": False,
                    "risk_control": False,
                },
            },
            profile=profile,
            claims_by_id={"CLM-1": claim},
            as_of_date="2026-08-11",
        )
        view = build_standalone_investment_view(
            project={
                "title": "GPU / ASIC",
                "report_scope": "standalone-bom",
                "bom_node_id": "gpu_asic",
            },
            profile=profile,
            claims=[claim],
            conclusions=[],
            claim_mappings=[mapping],
            logic_states=[older_state, state],
            entity_states=[],
            thesis_revisions=[baseline_revision, change_revision],
            investment_snapshots=[snapshot],
            as_of_date="2026-08-11",
        )

        demand = view["lenses"][0]
        self.assertEqual(view["research_model"], "logic_chain_centered")
        self.assertEqual(view["logic_chain_version"], "2026-08-11.v1")
        self.assertIn("需求节点", view["logic_chain_judgment"])
        self.assertIn("估值节点", view["logic_chain_judgment"])
        self.assertIn("公司财务桥", view["logic_chain_judgment"])
        self.assertEqual(
            [node["logic_node_id"] for node in demand["causal_nodes"]],
            ["demand.node"],
        )
        self.assertEqual(
            [node["logic_node_id"] for node in demand["derived_views"]],
            ["demand.parties"],
        )
        event = demand["causal_nodes"][0]["claim_events"][0]
        self.assertEqual(event["direction"], "boundary")
        self.assertEqual(event["rationale"], "订单增长仍受交付窗口约束。")
        self.assertEqual(
            [row["as_of_date"] for row in demand["causal_nodes"][0]["state_history"]],
            ["2026-08-10", "2026-08-11"],
        )
        history_group = demand["causal_nodes"][0]["event_history_groups"][0]
        self.assertEqual(history_group["period_key"], "2026-07")
        self.assertEqual(history_group["claim_count"], 1)
        self.assertEqual(history_group["sources"][0]["claim_count"], 1)
        self.assertEqual(
            event["triggered_revisions"][0]["as_of_date"],
            "2026-08-11",
        )

        html = StandaloneBomHtmlRenderer(Path("/tmp")).render(view)
        self.assertIn('data-research-model="logic-chain-centered"', html)
        self.assertIn('class="logic-chain-map"', html)
        self.assertIn('class="claim-event effect-boundary"', html)
        self.assertIn('class="node-state-history"', html)
        self.assertIn('class="claim-month-group"', html)
        self.assertIn('class="claim-source-group"', html)
        self.assertIn('data-history-filter="boundary"', html)
        self.assertIn("节点状态历史", html)
        self.assertIn("信息事件历史", html)
        self.assertIn("改变边界", html)
        self.assertIn("派生证据视图", html)
        self.assertIn("本期证据变化", html)

        markdown = StandaloneBomMarkdownRenderer(Path("/tmp")).render(view)
        self.assertIn("research_model: logic-chain-centered", markdown)
        self.assertIn("### 第一性原理逻辑链", markdown)
        self.assertIn("### 节点状态与观点时间线", markdown)
        self.assertIn("### 派生证据视图", markdown)
        self.assertIn("##### 节点状态历史", markdown)
        self.assertIn("##### 信息事件历史", markdown)
        self.assertIn("###### 2026年07月", markdown)
        self.assertIn("改变边界", markdown)
        self.assertIn("**本期证据变化：**", markdown)


if __name__ == "__main__":
    unittest.main()
