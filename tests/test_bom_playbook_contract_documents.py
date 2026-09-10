from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BomPlaybookContractDocumentTests(unittest.TestCase):
    def test_canonical_contracts_require_one_node_specific_playbook_per_bom(self):
        documents = {
            "AGENTS.md": ROOT / "AGENTS.md",
            "QA contract": ROOT / "skills/value_invest_research/frameworks/research_goal_qa.md",
            "domain playbooks": ROOT / "skills/value_invest_research/frameworks/domain_playbooks.md",
            "report contract": ROOT / "skills/value_invest_research/frameworks/research_report_contract.md",
        }

        for label, path in documents.items():
            with self.subTest(document=label):
                text = path.read_text(encoding="utf-8")
                self.assertRegex(text, r"node-specific|six-question playbook|六问 Playbook|六问 playbook")
                self.assertRegex(text, r"generic fallback|generic-fallback|通用模板|通用静态|通用链条")

    def test_domain_contract_preserves_per_node_temporal_rule_without_extra_skills(self):
        text = (ROOT / "skills/value_invest_research/frameworks/domain_playbooks.md").read_text(encoding="utf-8")
        self.assertIn("one canonical BOM node -> one six-question playbook -> one temporal ledger", text)
        self.assertIn("reproducible as-of snapshots", text)
        self.assertIn("discovering a new mechanism does not require rewriting old evidence", text)

    def test_public_contract_uses_temporal_six_question_sequence(self):
        documents = (
            ROOT / "AGENTS.md",
            ROOT / "skills/value_invest_research/frameworks/research_goal_qa.md",
            ROOT / "skills/value_invest_research/frameworks/domain_playbooks.md",
            ROOT / "skills/value_invest_research/frameworks/research_report_contract.md",
        )

        for path in documents:
            with self.subTest(document=str(path)):
                text = path.read_text(encoding="utf-8")
                self.assertIn("基本理解思路", text)
                self.assertIn("时间演化", text)

        report_contract = (ROOT / "skills/value_invest_research/frameworks/research_report_contract.md").read_text(encoding="utf-8")
        self.assertIn("Basic Understanding", report_contract)
        self.assertIn("Time Evolution", report_contract)
        self.assertIn("evidence whitelist", report_contract)

    def test_public_contract_splits_parent_index_from_bom_child_reports(self):
        contract = (ROOT / "skills/value_invest_research/frameworks/research_report_contract.md").read_text(encoding="utf-8")

        for phrase in [
            "report_scope: industry-index",
            "report_scope: bom-node",
            "boms/<node_id>/professional_report.md",
            "BOM 独立研究目录",
            "relative link",
            "links back to the parent",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, contract)


if __name__ == "__main__":
    unittest.main()
