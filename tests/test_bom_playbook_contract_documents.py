from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BomPlaybookContractDocumentTests(unittest.TestCase):
    def test_canonical_contracts_require_one_node_specific_playbook_per_bom(self):
        documents = {
            "AGENTS.md": ROOT / "AGENTS.md",
            "canonical skill": ROOT / "skills/value_invest_research/SKILL.md",
            "QA contract": ROOT / "skills/value_invest_research/frameworks/research_goal_qa.md",
            "domain playbooks": ROOT / "skills/value_invest_research/frameworks/domain_playbooks.md",
            "report contract": ROOT / "skills/value_invest_research/frameworks/research_report_contract.md",
        }

        for label, path in documents.items():
            with self.subTest(document=label):
                text = path.read_text(encoding="utf-8")
                self.assertRegex(text, r"node-specific|six-question playbook|六问 Playbook|六问 playbook")
                self.assertRegex(text, r"generic fallback|generic-fallback|通用模板|通用静态|通用链条")

    def test_both_s_curve_skill_copies_keep_the_per_node_temporal_rule(self):
        skill_paths = (
            ROOT / ".agents/skills/s-curve-investment-research/SKILL.md",
            ROOT / "skills/value_invest_research/specialty_skills/s-curve-investment-research/SKILL.md",
        )

        for path in skill_paths:
            with self.subTest(skill=str(path)):
                text = path.read_text(encoding="utf-8")
                self.assertIn("每个 BOM 必须有独立 Playbook", text)
                self.assertIn("一个 BOM 节点 -> 一个六问 Playbook", text)
                self.assertIn("时间证据账本", text)
                self.assertIn("不需要先修改逻辑链", text)

    def test_public_contract_uses_temporal_six_question_sequence(self):
        documents = (
            ROOT / "AGENTS.md",
            ROOT / "skills/value_invest_research/SKILL.md",
            ROOT / "skills/value_invest_research/frameworks/research_goal_qa.md",
            ROOT / "skills/value_invest_research/frameworks/domain_playbooks.md",
            ROOT / "skills/value_invest_research/frameworks/research_report_contract.md",
            ROOT / "skills/value_invest_research/specialty_skills/s-curve-investment-research/SKILL.md",
            ROOT / ".agents/skills/s-curve-investment-research/SKILL.md",
        )

        for path in documents:
            with self.subTest(document=str(path)):
                text = path.read_text(encoding="utf-8")
                self.assertIn("基本理解思路", text)
                self.assertIn("时间演化", text)

        report_contract = documents[4].read_text(encoding="utf-8")
        self.assertIn("bom-question-understanding", report_contract)
        self.assertIn("bom-question-timeline", report_contract)
        self.assertIn("not an evidence whitelist", report_contract)

    def test_public_contract_splits_parent_index_from_bom_child_reports(self):
        contract = (ROOT / "skills/value_invest_research/frameworks/research_report_contract.md").read_text(encoding="utf-8")

        for phrase in [
            'data-report-scope="industry-index"',
            'data-report-scope="bom-node"',
            "boms/<node_id>/professional_report.html",
            "bom-project-index",
            "bom-index-card",
            "project-back-link",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, contract)


if __name__ == "__main__":
    unittest.main()
