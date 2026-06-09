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
            "directly answer the unit question",
            "maximum depth five",
            "mapping table",
            "driver table",
            "Industry-overview / QA complementarity lock",
            "decision-interrogation layer",
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
            "当前研究的问题",
            "行业概况",
            "下钻 QA",
            "标的推荐",
            "来源索引",
            "industry-overview-section",
            "industry-module",
            "details.industry-module",
            "summary.module-head",
            "module-index",
            "industry-module-body",
            "constraint-definition",
            "upstream, midstream, downstream",
            "产业链与生态位",
            "行业空间",
            "竞争格局与利润池",
            "瓶颈点",
            "关键变量与待验证数据",
            "chain-explain",
            "chain-research-bridge",
            "chain-node-lens",
            "chain-plain-summary",
            "chain-lane-map",
            "chain-value-flow",
            "chain-simple-flow",
            "chain-detail-panel",
            "component-value-chain",
            "chain-layer-grid",
            "chain-layer-card",
            "chain-relationship-graph",
            "chain-stage-panel",
            "chain-company-list",
            "chain-company-card",
            "chain-chokepoints",
            "technology-route-matrix",
            "bottleneck-release-timeline",
            "industry-space",
            "industry-space-summary",
            "space-bom-reasoning",
            "space-node-card",
            "space-node-reasoning",
            "space-node-evidence",
            "space-node-space-reasoning",
            "space-node-sizing",
            "space-method-step",
            "space-step-title",
            "space-step-index",
            "space-public-methods",
            "space-method-card-grid",
            "space-method-card",
            "space-method-card-body",
            "space-method-entry",
            "space-method-entry-sources",
            "space-method-empty",
            "space-horizon-conclusion",
            "space-horizon-grid",
            "space-horizon-card",
            "space-node-sizing-table",
            "space-step-confidence",
            "table-scroll",
            "industry-competition",
            "industry-chokepoints",
            "industry-key-variables",
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
            "qa-card level-4",
            "qa-card level-5",
            "Every `qa-card level-1` through `qa-card level-5`",
            "details.industry-module",
            "Q4 remains inside `下钻 QA`",
            "must never erase, replace, rename, or move Q4",
            "one `target-section` with `target-profit-bridge`, `target-valuation-table`, a `target-odds-model`, `target-odds-table`, and dense `target-table`",
            "one collapsed `source-collapse`",
            "duplicate the same child titles",
            "qa-card",
            "artifact-card",
            "target-table",
            "target-profit-bridge",
            "target-valuation-table",
            "complementary, not duplicative",
            "simple value-flow steps",
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
                self.assertIn("行业概况", doc_text)
                self.assertIn("drops L3", doc_text)
                self.assertIn("moves Q4 out of `下钻 QA`", doc_text)
                self.assertIn("duplicates child-question lists beside inline cards", doc_text)
                self.assertIn("Four non-drift locks", doc_text)
                self.assertIn("industry-overview lock", doc_text)
                self.assertIn("supply-chain-panorama-explainer", doc_text)
                self.assertIn("beginner-readable Chinese", doc_text)
                self.assertIn("component-value-chain", doc_text)
                self.assertIn("chain-simple-flow", doc_text)
                self.assertIn("chain-detail-panel", doc_text)
                self.assertIn("space-bom-reasoning", doc_text)
                self.assertIn("space-node-card", doc_text)
                self.assertIn("space-node-evidence", doc_text)
                self.assertIn("space-node-space-reasoning", doc_text)
                self.assertIn("space-node-sizing", doc_text)
                self.assertIn("space-method-step", doc_text)
                self.assertIn("space-step-title", doc_text)
                self.assertIn("space-step-index", doc_text)
                self.assertIn("space-public-methods", doc_text)
                self.assertIn("space-method-card-grid", doc_text)
                self.assertIn("space-method-card", doc_text)
                self.assertIn("space-method-card-body", doc_text)
                self.assertIn("space-method-entry", doc_text)
                self.assertIn("space-method-entry-sources", doc_text)
                self.assertIn("space-method-empty", doc_text)
                self.assertIn("space-horizon-conclusion", doc_text)
                self.assertIn("space-horizon-grid", doc_text)
                self.assertIn("space-horizon-card", doc_text)
                self.assertIn("space-node-sizing-table", doc_text)
                self.assertIn("space-step-confidence", doc_text)
                self.assertIn("证据", doc_text)
                self.assertIn("空间推理", doc_text)
                self.assertIn("公开拆法", doc_text)
                self.assertIn("公司指引", doc_text)
                self.assertIn("公司 TAM", doc_text)
                self.assertIn("客户侧指引", doc_text)
                self.assertIn("第三方拆法", doc_text)
                self.assertIn("财务兑现证据", doc_text)
                self.assertIn("公司或机构", doc_text)
                self.assertIn("指引内容", doc_text)
                self.assertIn("时间范围", doc_text)
                self.assertIn("可验证指标", doc_text)
                self.assertIn("空间结论", doc_text)
                self.assertIn("短期", doc_text)
                self.assertIn("中期", doc_text)
                self.assertIn("长期", doc_text)
                self.assertIn("结论", doc_text)
                self.assertIn("BOM", doc_text)
                self.assertIn("table-scroll", doc_text)
                self.assertIn("technology-route-matrix", doc_text)
                self.assertIn("bottleneck-release-timeline", doc_text)
                self.assertIn("target-profit-bridge", doc_text)
                self.assertIn("target-valuation-table", doc_text)
                self.assertIn("decision-interrogation layer", doc_text)
                self.assertIn("Additive-iteration lock", doc_text)
                self.assertIn("backtest time-slice lock", doc_text)
                self.assertIn("frontend card-style lock", doc_text)
                self.assertIn("final-target evaluation label", doc_text)
                self.assertIn("framework_contracts.py", doc_text)
                self.assertIn("Scarcity-first opportunity gate", doc_text)
                self.assertIn("underpriced large opportunity", doc_text)
                self.assertIn("actionable_long", doc_text)
