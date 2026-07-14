import unittest

from value_invest_research.application.use_cases.build_bom_node_research_payload import (
    build_bom_node_research_payload,
)
from value_invest_research.domain.bom_node_playbooks import (
    compute_node_playbook,
    get_bom_node_playbook,
    hbm_node_playbook,
    validate_bom_playbook_registry,
)


class ComputeBomNodePlaybookTests(unittest.TestCase):
    def test_compute_playbook_has_strict_scope_and_six_question_models(self):
        playbook = compute_node_playbook()

        self.assertEqual(playbook.node_id, "compute")
        self.assertEqual(playbook.public_name, "计算加速器 / GPU / ASIC")
        self.assertIn("HBM/DRAM", playbook.exclusions)
        self.assertNotIn("HBM", playbook.produces)
        self.assertEqual(
            [question.question_number for question in playbook.questions],
            list(range(1, 7)),
        )
        self.assertEqual(playbook.questions[0].model_name, "AI 算力需求传导与弹性模型")
        self.assertEqual(playbook.questions[1].model_name, "GPU/ASIC 合格供给漏斗模型")
        self.assertEqual(playbook.questions[4].model_name, "市场隐含算力路径与预期差模型")

    def test_compute_stages_define_primary_cross_check_and_refutation_metrics(self):
        playbook = compute_node_playbook()

        for question in playbook.questions:
            with self.subTest(question=question.question_id):
                self.assertGreaterEqual(len(question.stages), 4)
                self.assertLessEqual(len(question.stages), 7)
                for stage in question.stages:
                    self.assertTrue(stage.primary_metric)
                    self.assertTrue(stage.refutation_metric)
                    self.assertGreaterEqual(len(stage.cross_check_metrics), 1)
                    self.assertLessEqual(len(stage.cross_check_metrics), 2)

    def test_registry_resolves_compute_and_hbm_without_adapter_dependencies(self):
        compute = get_bom_node_playbook("compute")
        memory = get_bom_node_playbook("memory")

        validate_bom_playbook_registry(
            ("compute", "memory"),
            (compute, memory),
        )
        self.assertEqual(compute, compute_node_playbook())
        self.assertEqual(memory, hbm_node_playbook())

    def test_compute_research_run_must_match_playbook_question_ids(self):
        playbook = compute_node_playbook()
        malformed_run = {
            "node_id": "compute",
            "as_of_date": "2026-03-28",
            "questions": [],
        }

        with self.assertRaisesRegex(ValueError, "compute research run question drift"):
            build_bom_node_research_payload(playbook, malformed_run)

    def test_playbook_contains_no_sources_cutoff_or_run_verdict(self):
        text = str(compute_node_playbook().to_dict())

        self.assertNotIn("SRC-", text)
        self.assertNotIn("2026-03-28", text)
        self.assertNotIn("当前结论", text)


if __name__ == "__main__":
    unittest.main()
