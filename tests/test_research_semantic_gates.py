import unittest
from pathlib import Path

from value_invest_research.adapters.outbound.filesystem_source_universe import (
    FileSystemSourceUniverseRepository,
)
from value_invest_research.adapters.outbound.report_sections import DEFAULT_REPORT_SECTIONS
from value_invest_research.domain.bom_research_readiness import (
    apply_target_research_gates,
    build_bom_completion_scoring_inputs,
    build_bom_readiness,
    validate_bom_research_decision_gates,
)
from value_invest_research.domain.leaf_research_tasks import build_leaf_tasks_from_tree
from value_invest_research.framework_contracts import score_target_observation


def _artifact(question_number: int) -> dict:
    row = {
        "artifact_id": f"bom-memory-q{question_number}",
        "bom_node_id": "memory",
        "bom_node": "HBM / 高端内存",
        "question_number": question_number,
        "search_execution_status": "completed",
        "parser_status": "gpt_verified_source_parse",
        "source_universe_plan": {"priority_sources": ["primary filings"]},
        "exa_search_plan": {"direct_query": f"memory question {question_number}"},
        "claim_mapping_plan": {"atomic_claim_types": ["actual", "forecast", "refutation"]},
        "source_ids": [f"SRC-{question_number}"],
        "evidence_summary": [f"question {question_number} evidence"],
        "source_parse_records": [
            {
                "source_id": f"SRC-{question_number}",
                "parser_status": "completed",
                "gpt_verification_status": "verified_with_caveats",
                "allowed_to_strengthen_conclusion": True,
            }
        ],
    }
    if question_number == 6:
        row["refuting_source_ids"] = ["SRC-6"]
        row["refutation_evidence_summary"] = ["Observed evidence that can refute the thesis."]
    return row


def _target() -> dict:
    return {
        "ticker": "MU",
        "thesis_node_id": "memory",
        "candidate_action_state": "actionable_long",
        "action_state": "actionable_long",
        "valuation_status": "verified_with_caveats",
        "company_exposure_status": "verified",
    }


class ResearchSemanticGateTests(unittest.TestCase):
    def test_non_bom_targets_remain_backward_compatible(self):
        target = {"ticker": "EVENT", "action_state": "watch_only"}

        self.assertEqual(apply_target_research_gates([target], {})[0], target)

    def test_six_questions_and_refutation_allow_candidate_to_pass(self):
        workbench = {"bom_question_search_artifacts": [_artifact(index) for index in range(1, 7)]}

        readiness = build_bom_readiness(workbench)["memory"]
        gated = apply_target_research_gates([_target()], workbench)[0]

        self.assertTrue(readiness["complete"])
        self.assertTrue(readiness["refutation_complete"])
        self.assertTrue(gated["research_gate"]["passed"])
        self.assertEqual(gated["action_state"], "actionable_long")

    def test_missing_refuting_evidence_caps_actionable_candidate(self):
        artifacts = [_artifact(index) for index in range(1, 7)]
        artifacts[-1]["refuting_source_ids"] = []
        artifacts[-1]["refutation_evidence_summary"] = []
        workbench = {"bom_question_search_artifacts": artifacts}

        gated = apply_target_research_gates([_target()], workbench)[0]

        self.assertEqual(gated["action_state"], "watch_only")
        self.assertIn("refutation_evidence_unverified", gated["research_gate"]["gate_reasons"])
        self.assertIn("bom_six_question_incomplete:5/6", gated["research_gate"]["gate_reasons"])

    def test_missing_active_research_plan_keeps_question_incomplete(self):
        artifacts = [_artifact(index) for index in range(1, 7)]
        artifacts[0]["claim_mapping_plan"] = {}
        workbench = {"bom_question_search_artifacts": artifacts}

        readiness = build_bom_readiness(workbench)["memory"]

        self.assertFalse(readiness["complete"])
        self.assertFalse(readiness["question_statuses"][0]["planning_complete"])
        self.assertEqual(readiness["completed_question_count"], 5)

    def test_missing_company_exposure_blocks_an_otherwise_complete_target(self):
        workbench = {"bom_question_search_artifacts": [_artifact(index) for index in range(1, 7)]}
        target = _target()
        target.pop("company_exposure_status")

        gated = apply_target_research_gates([target], workbench)[0]

        self.assertEqual(gated["action_state"], "watch_only")
        self.assertIn("company_exposure_unverified", gated["research_gate"]["gate_reasons"])

    def test_research_gate_never_upgrades_a_conservative_score(self):
        workbench = {"bom_question_search_artifacts": [_artifact(index) for index in range(1, 7)]}
        target = _target()
        target["candidate_action_state"] = "actionable_long"
        target["action_state"] = "watch_only"
        target["score"] = {"action_state": "watch_only"}

        gated = apply_target_research_gates([target], workbench)[0]

        self.assertTrue(gated["research_gate"]["passed"])
        self.assertEqual(gated["candidate_action_state"], "actionable_long")
        self.assertEqual(gated["action_state"], "watch_only")

    def test_validator_rejects_actionable_state_that_bypasses_gate(self):
        artifacts = [_artifact(index) for index in range(1, 7)]
        artifacts[-1]["refuting_source_ids"] = []
        workbench = {"bom_question_search_artifacts": artifacts}
        target = _target()
        target["research_gate_required"] = True
        target["research_gate"] = {"passed": True, "gate_reasons": []}

        result = validate_bom_research_decision_gates(workbench, [target])
        codes = {issue["code"] for issue in result["issues"]}

        self.assertFalse(result["ok"])
        self.assertIn("actionable_target_failed_research_gate", codes)
        self.assertIn("target_research_gate_drift", codes)

    def test_scoring_caps_strong_numbers_when_research_is_incomplete(self):
        score = score_target_observation(
            {
                "ticker": "TEST",
                "research_gate_required": True,
                "bom_research_complete": False,
                "refutation_status": "unverified",
                "valuation_status": "incomplete",
                "chokepoint_strength": 5,
                "future_space": 5,
                "valuation_odds": 5,
                "evidence_quality": 5,
                "disconfirming_risk_control": 5,
                "monitorability": 5,
                "payoff_convexity": 5,
                "demand_visibility": 5,
                "irreplaceability": 5,
                "market_underpricing": 5,
            }
        )

        self.assertEqual(score["action_state"], "watch_only")
        self.assertLessEqual(score["total_score"], 3.49)
        self.assertIn("bom_six_question_incomplete", score["gate_reasons"])
        self.assertIn("valuation_unverified", score["gate_reasons"])

    def test_completion_scoring_inputs_keep_question_level_evidence_lineage(self):
        workbench = {"bom_question_search_artifacts": [_artifact(index) for index in range(1, 7)]}
        target = _target()
        target["evidence_ids"] = ["SRC-1", "SRC-2"]
        target["valuation_status"] = "incomplete"

        scoring_input = build_bom_completion_scoring_inputs([target], workbench)[0]

        future_space = scoring_input["score_subcomponents"]["future_space"][0]
        valuation = scoring_input["score_subcomponents"]["valuation_odds"][0]
        self.assertEqual(future_space["status"], "verified_with_caveats")
        self.assertEqual(future_space["evidence_ids"], ["SRC-1"])
        self.assertEqual(future_space["evidence_role"], "BOM demand pull-through and elasticity")
        self.assertEqual(valuation["status"], "gap")
        self.assertEqual(valuation["evidence_ids"], [])
        self.assertIn("估值", valuation["gap_reason"])

    def test_source_universe_is_injected_into_leaf_task(self):
        root = Path(__file__).resolve().parents[1]
        repository = FileSystemSourceUniverseRepository(root / "config" / "source_universes.json")
        qa_tree = {
            "project_id": "ai_factory_memory_test",
            "domain_playbook": "ai_factory",
            "default_depth": 3,
            "nodes": [
                {
                    "id": "Q1.1.1",
                    "level": 3,
                    "question": "HBM 供给为什么跟不上，供需缺口如何验证？",
                    "parent_id": "",
                    "next_question_ids": [],
                }
            ],
        }

        universe = repository.resolve_for_research(qa_tree)
        task = build_leaf_tasks_from_tree(
            qa_tree,
            ticker="THEME",
            company_name="AI Factory",
            source_universe=universe,
        )[0]
        names = {item["name"] for item in task["source_universe_plan"]["priority_sources"]}

        self.assertEqual(task["source_universe_plan"]["domain_id"], "ai_factory")
        self.assertIn("SemiAnalysis", names)
        self.assertIn("TrendForce", names)
        self.assertTrue(task["source_universe_plan"]["directed_queries"])

    def test_default_public_renderer_keeps_four_sections(self):
        self.assertEqual(len(DEFAULT_REPORT_SECTIONS), 4)
        self.assertNotIn("QaSection", {section.__class__.__name__ for section in DEFAULT_REPORT_SECTIONS})


if __name__ == "__main__":
    unittest.main()
