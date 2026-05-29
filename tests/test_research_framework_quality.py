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
            "target-recommendation-analysis",
        ]
        for skill in required_skills:
            path = ROOT / "skills" / "value_invest_research" / "specialty_skills" / skill / "SKILL.md"
            with self.subTest(skill=skill):
                self.assertTrue(path.exists(), f"missing skill: {path}")
                text = path.read_text(encoding="utf-8")
                self.assertIn(f"name: {skill}", text)
                self.assertIn("description:", text)

    def test_canonical_framework_records_quality_pipeline(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        skill = (ROOT / "skills" / "value_invest_research" / "SKILL.md").read_text(encoding="utf-8")
        framework = (ROOT / "skills" / "value_invest_research" / "frameworks" / "research_goal_qa.md").read_text(
            encoding="utf-8"
        )
        combined = "\n".join([agents, skill, framework])
        for phrase in [
            "Question architecture",
            "Source planning",
            "financial-statement-analysis",
            "valuation-analysis",
            "industry-report-analysis",
            "news-event-analysis",
            "opinion-analysis",
            "target-recommendation-analysis",
            "future space",
            "valuation odds",
            "chokepoint evaluation",
            "chokepoint score",
            "score breakdown",
            "simplified odds model",
            "prediction review",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, combined)

    def test_final_report_contract_is_canonical(self):
        contract_path = ROOT / "skills" / "value_invest_research" / "frameworks" / "research_report_contract.md"
        contract = contract_path.read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        skill = (ROOT / "skills" / "value_invest_research" / "SKILL.md").read_text(encoding="utf-8")
        framework = (ROOT / "skills" / "value_invest_research" / "frameworks" / "research_goal_qa.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("research_report_contract.md", agents)
        self.assertIn("frameworks/research_report_contract.md", skill)
        self.assertIn("research_report_contract.md", framework)

        for phrase in [
            "当前研究目标",
            "问题下钻",
            "最终标的推荐",
            "来源索引",
            "L2 must not be a single catch-all wrapper",
            "research-type adapter",
            "domain playbook",
            "domain-specific question templates",
            "tracking indicators",
            "win probability",
            "payoff odds",
            "chokepoint score",
            "compact score breakdown",
            "simplified odds model",
            "prediction review",
            "Do not add top-level process sections",
            "No duplicated titles",
            "qa-card",
            "artifact-card",
            "target-table",
            "source-collapse",
            "source-bucket",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, contract)
