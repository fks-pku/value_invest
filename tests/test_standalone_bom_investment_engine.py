import unittest
from pathlib import Path

from value_invest_research.adapters.outbound.standalone_bom_html_renderer import (
    StandaloneBomHtmlRenderer,
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
    def test_playbook_requires_all_five_lenses_and_namespaced_nodes(self):
        index = validate_standalone_bom_playbook(_profile())
        self.assertEqual(len(index["nodes"]), 5)

        invalid = _profile()
        invalid["lenses"][0]["logic_nodes"][0]["logic_node_id"] = "supply.wrong"
        with self.assertRaisesRegex(ValueError, "namespaced"):
            validate_standalone_bom_playbook(invalid)

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


if __name__ == "__main__":
    unittest.main()
