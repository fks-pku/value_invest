import unittest

from value_invest_research.application.use_cases.build_bom_node_research_payload import (
    build_bom_node_research_payload,
)
from value_invest_research.domain.bom_node_playbooks import (
    hbm_node_playbook,
    validate_bom_playbook_registry,
)


class HbmBomNodePlaybookTests(unittest.TestCase):
    def test_hbm_playbook_is_hbm_only_and_has_six_questions(self):
        playbook = hbm_node_playbook()

        self.assertEqual(playbook.public_name, "HBM")
        self.assertEqual(set(playbook.exclusions), {"server DDR5", "enterprise SSD"})
        self.assertNotIn("server DDR5", playbook.produces)
        self.assertNotIn("enterprise SSD", playbook.produces)
        self.assertEqual([question.question_number for question in playbook.questions], list(range(1, 7)))

    def test_every_hbm_question_has_optional_reader_orientation_hints(self):
        playbook = hbm_node_playbook()

        for question in playbook.questions:
            with self.subTest(question=question.question_id):
                self.assertGreaterEqual(len(question.stages), 1)
                for stage in question.stages:
                    self.assertTrue(stage.title)
                    self.assertTrue(stage.role)

    def test_playbook_contains_no_run_specific_sources_or_verdicts(self):
        payload = hbm_node_playbook().to_dict()
        text = str(payload)

        self.assertNotIn("SRC-", text)
        self.assertNotIn("2026-03-28", text)
        self.assertNotIn("当前结论", text)

    def test_research_run_can_add_or_omit_hint_topics_without_stage_drift(self):
        playbook = hbm_node_playbook()
        malformed_run = {
            "node_id": "memory",
            "as_of_date": "2026-03-28",
            "questions": [
                {"question_id": question.question_id, "stages": []}
                for question in playbook.questions
            ],
        }

        payload = build_bom_node_research_payload(playbook, malformed_run)

        self.assertEqual(len(payload["questions"]), 6)
        self.assertFalse(payload["questions"][0]["understanding"]["isEvidencePath"])

    def test_bom_registry_requires_one_playbook_per_canonical_node(self):
        playbook = hbm_node_playbook()

        validate_bom_playbook_registry(("memory",), (playbook,))

        with self.assertRaisesRegex(ValueError, r"missing=\['compute'\]"):
            validate_bom_playbook_registry(("compute", "memory"), (playbook,))

    def test_bom_registry_rejects_duplicate_and_extra_playbooks(self):
        playbook = hbm_node_playbook()

        with self.assertRaisesRegex(ValueError, "duplicate node IDs"):
            validate_bom_playbook_registry(("memory",), (playbook, playbook))

        with self.assertRaisesRegex(ValueError, r"extra=\['memory'\]"):
            validate_bom_playbook_registry(("compute",), (playbook,))


if __name__ == "__main__":
    unittest.main()
