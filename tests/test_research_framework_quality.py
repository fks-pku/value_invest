import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ResearchFrameworkQualityTests(unittest.TestCase):
    def test_specialty_skills_exist_for_canonical_dispatch(self):
        required_skills = [
            "investment-question-architect",
            "supply-chain-panorama-explainer",
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
            "Mechanism-depth protocol",
            "demand driver tree",
            "unit economics",
            "market-pricing bridge",
            "model/口径 reconciliation",
            "domain_playbooks.md",
            "supply-chain-panorama-explainer",
            "beginner-readable Chinese",
            "directly answer the leaf question",
            "mapping table",
            "driver table",
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
            "产业链全景",
            "问题下钻",
            "最终标的推荐",
            "来源索引",
            "supply-chain map",
            "upstream, midstream, downstream",
            "chain-explain",
            "chain-plain-summary",
            "chain-flow-steps",
            "chain-layer-grid",
            "chain-layer-card",
            "chain-chokepoints",
            "chain-target-links",
            "L2 must not be a single catch-all wrapper",
            "research-type adapter",
            "domain playbook",
            "domain-specific question templates",
            "mechanism-depth maps",
            "demand driver tree",
            "unit economics/profit bridge",
            "market-pricing bridge",
            "model/口径 reconciliation",
            "tracking indicators",
            "win probability",
            "payoff odds",
            "chokepoint score",
            "compact score breakdown",
            "simplified odds model",
            "prediction review",
            "Scarcity-first opportunity gate",
            "currently underpriced large opportunity",
            "default action state is `no_action`",
            "large future demand",
            "irreplaceability/scarcity",
            "market underpricing",
            "four core target dimensions",
            "scarcity_or_monopoly",
            "mispricing",
            "earnings_elasticity",
            "risk_control",
            "`action_state`: `actionable_long`, `watch_only`, or `no_action`",
            "Do not add top-level process sections",
            "No duplicated titles",
            "Strict Rendering Invariants",
            "Non-Drift Locks",
            "Additive-iteration lock",
            "Hierarchy and format lock",
            "Backtest time-slice lock",
            "Frontend card-style lock",
            "Public no-changelog lock",
            "only information visible at the frozen cutoff",
            "only current-time data allowed",
            "final-target evaluation label",
            "framework_contracts.py",
            "frozen recommendation",
            "training samples",
            "prediction reviews",
            "The time-slice rule is asymmetric by design",
            "Allowed before the frozen recommendation",
            "Forbidden before the frozen recommendation",
            "Required separation",
            "Frontend card-style validation",
            "stable table sizing",
            "本轮升级",
            "what changed in this run",
            "contract-invalid",
            "qa-card level-1",
            "qa-card level-2",
            "qa-card level-3",
            "Every `qa-card level-1`, `qa-card level-2`, and `qa-card level-3`",
            "Q4 remains inside `问题下钻`",
            "must never erase, replace, rename, or move Q4",
            "one `target-section` with a dense `target-table`",
            "one collapsed `source-collapse`",
            "duplicate the same child titles",
            "qa-card",
            "artifact-card",
            "target-table",
            "source-collapse",
            "source-bucket",
            "state-actionable_long",
            "state-watch_only",
            "state-no_action",
            "browser or DOM smoke check",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, contract)

        for doc_name, doc_text in [
            ("AGENTS.md", agents),
            ("SKILL.md", skill),
            ("research_goal_qa.md", framework),
        ]:
            with self.subTest(doc=doc_name):
                self.assertIn("validation requirements", doc_text)
                self.assertIn("产业链全景", doc_text)
                self.assertIn("drops L3", doc_text)
                self.assertIn("moves Q4 out of `问题下钻`", doc_text)
                self.assertIn("duplicates child-question lists beside inline cards", doc_text)
                self.assertIn("Four non-drift locks", doc_text)
                self.assertIn("supply-chain map lock", doc_text)
                self.assertIn("supply-chain-panorama-explainer", doc_text)
                self.assertIn("beginner-readable Chinese", doc_text)
                self.assertIn("Additive-iteration lock", doc_text)
                self.assertIn("backtest time-slice lock", doc_text)
                self.assertIn("frontend card-style lock", doc_text)
                self.assertIn("final-target evaluation label", doc_text)
                self.assertIn("framework_contracts.py", doc_text)
                self.assertIn("Scarcity-first opportunity gate", doc_text)
                self.assertIn("underpriced large opportunity", doc_text)
                self.assertIn("actionable_long", doc_text)
