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
                self.assertRegex(text, r"node-specific playbook|node-specific `BomNodePlaybook`|节点专属 Playbook")
                self.assertRegex(text, r"generic fallback|generic-fallback|通用模板|通用静态|通用链条")

    def test_both_s_curve_skill_copies_keep_the_per_node_rule(self):
        skill_paths = (
            ROOT / ".agents/skills/s-curve-investment-research/SKILL.md",
            ROOT / "skills/value_invest_research/specialty_skills/s-curve-investment-research/SKILL.md",
        )

        for path in skill_paths:
            with self.subTest(skill=str(path)):
                text = path.read_text(encoding="utf-8")
                self.assertIn("每个 BOM 必须有独立 Playbook", text)
                self.assertIn("一个 BOM 节点 -> 一个节点专属 Playbook", text)
                self.assertIn("底层链条不可以复用", text)

    def test_public_contract_merges_model_and_causal_chain(self):
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
                self.assertIn("研究逻辑链", text)

        report_contract = documents[4].read_text(encoding="utf-8")
        self.assertIn("bom-step-research-logic", report_contract)
        self.assertIn("Do not render separate public `判断模型` or `具体逻辑链条` cards", report_contract)


if __name__ == "__main__":
    unittest.main()
