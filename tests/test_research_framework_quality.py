import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ResearchFrameworkQualityTests(unittest.TestCase):
    def test_specialty_skills_exist_for_canonical_dispatch(self):
        required_skills = [
            "investment-question-architect",
            "research-source-planner",
            "leaf-research-deepseek",
            "financial-statement-analysis",
            "valuation-analysis",
            "industry-report-analysis",
            "news-event-analysis",
            "opinion-analysis",
            "company-exposure-analysis",
            "target-recommendation-analysis",
            "target-ranking-analysis",
        ]
        for skill in required_skills:
            path = ROOT / "skills" / "value_invest_research" / "specialty_skills" / skill / "SKILL.md"
            with self.subTest(skill=skill):
                self.assertTrue(path.exists(), f"missing skill: {path}")
                text = path.read_text(encoding="utf-8")
                self.assertIn(f"name: {skill}", text)
                self.assertIn("description:", text)

    def test_canonical_documents_share_one_four_section_contract(self):
        docs = self._canonical_docs()
        four_section_terms = ["当前研究的问题", "行业概况", "标的推荐", "来源索引"]
        stale_five_section_order = "当前研究的问题` -> `行业概况` -> `下钻 QA`"

        for name, text in docs.items():
            with self.subTest(document=name):
                for term in four_section_terms:
                    self.assertIn(term, text)
                self.assertIn("下钻 QA", text)
                self.assertNotIn(stale_five_section_order, text)

        contract = docs["research_report_contract.md"]
        self.assertIn("exactly four top-level sections", contract)
        self.assertIn("Public `下钻 QA` is opt-in", contract)

    def test_framework_records_current_execution_pipeline(self):
        combined = "\n".join(self._canonical_docs().values())
        for phrase in [
            "ResearchGoal -> DomainPlaybook -> QuestionArchitecture",
            "maximum depth five",
            "config/source_universes.json",
            "SourceUniverseRepository",
            "direct/Exa",
            "question x source",
            "financial-statement-analysis",
            "valuation-analysis",
            "industry-report-analysis",
            "news-event-analysis",
            "opinion-analysis",
            "leaf-research-deepseek",
            "ReportViewModel",
            "CanonicalReportRenderer",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, combined)

    def test_semantic_gates_are_documented_consistently(self):
        docs = self._canonical_docs()
        required = [
            "thesis_node_id",
            "refuting_source_ids",
            "refutation_evidence_summary",
            "company exposure",
            "valuation",
            "score_subcomponents",
            "research_gate",
            "candidate_action_state",
            "actionable_long",
            "watch_only",
            "no_action",
        ]
        combined = "\n".join(docs.values())
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, combined)

        contract = docs["research_report_contract.md"]
        self.assertIn("Q6 requires observed refuting evidence", contract)
        self.assertIn("all six questions pass semantic completion", contract)

    def test_public_component_contract_covers_current_bom_report(self):
        contract = self._canonical_docs()["research_report_contract.md"]
        for phrase in [
            "industry-overview-section",
            "supply-chain-section",
            "chain-detail-panel",
            "chain-lane-map",
            "chain-value-flow",
            "component-value-chain",
            "bom-taxonomy",
            "bom-research-module",
            "bom-question-card",
            "bom-question-research-status",
            "bom-step-model",
            "bom-step-logic",
            "bom-stage-integrated-card",
            "metric-history-table",
            "metric-trend-gap",
            "expectation-table-group",
            "bom-expectation-table",
            "bom-s-curve-stage-card",
            "target-profit-bridge",
            "target-valuation-table",
            "target-odds-model",
            "target-table",
            "source-collapse",
            "table-scroll",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, contract)

    def test_public_report_keeps_process_artifacts_internal(self):
        contract = self._canonical_docs()["research_report_contract.md"]
        self.assertIn("Do not render raw search queries", contract)
        self.assertIn("change logs", contract)
        self.assertIn("Freeze recommendations before attaching labels", contract)

    @staticmethod
    def _canonical_docs() -> dict[str, str]:
        paths = {
            "AGENTS.md": ROOT / "AGENTS.md",
            "SKILL.md": ROOT / "skills" / "value_invest_research" / "SKILL.md",
            "research_goal_qa.md": ROOT / "skills" / "value_invest_research" / "frameworks" / "research_goal_qa.md",
            "research_report_contract.md": ROOT / "skills" / "value_invest_research" / "frameworks" / "research_report_contract.md",
        }
        return {name: path.read_text(encoding="utf-8") for name, path in paths.items()}


if __name__ == "__main__":
    unittest.main()
