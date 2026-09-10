import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ResearchFrameworkQualityTests(unittest.TestCase):
    def test_dynamic_research_agent_is_the_only_investment_skill(self):
        path = ROOT / ".agents/skills/dynamic-research-agent/SKILL.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("name: dynamic-research-agent", text)
        self.assertIn("description:", text)
        self.assertIn("独立完成研究", text)
        self.assertIn("专业报告的文章化要求", text)
        self.assertFalse((ROOT / "skills/value_invest_research/SKILL.md").exists())
        self.assertEqual(list((ROOT / "skills/value_invest_research/specialty_skills").rglob("SKILL.md")), [])
        retired_skills = [
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
            "conference-transcript-analysis",
            "event-to-investment-analysis",
            "ima-single-day-bom-scan",
            "s-curve-investment-research",
            "supply-chain-chokepoint-analysis",
            "supply-chain-panorama-explainer",
            "quant-research-fks",
            "quantitative-research",
        ]
        for skill in retired_skills:
            with self.subTest(skill=skill):
                self.assertFalse((ROOT / ".agents/skills" / skill / "SKILL.md").exists())
                self.assertNotIn(f"`{skill}`", text)

    def test_one_skill_keeps_material_specific_extraction_and_source_plans(self):
        from value_invest_research.domain.leaf_research_tasks import (
            extraction_schema_for_task,
            selected_skill_for_task_family,
            source_search_plan_for_task,
        )
        from value_invest_research.domain.l3_research_plan import _preferred_skill, _skill_for_source
        from value_invest_research.meta_qa_research import _meta_selected_skill, _meta_source_plan

        families = ["financial_statement", "valuation", "industry_report", "news_event", "opinion", "target_recommendation", "leaf_research", "unknown"]
        for family in families:
            with self.subTest(family=family):
                self.assertEqual(selected_skill_for_task_family(family), "dynamic-research-agent")
                self.assertEqual(_meta_selected_skill(family), "dynamic-research-agent")
                plans = source_search_plan_for_task({"question": "test"}, {}, family) + _meta_source_plan("test", {}, family)
                self.assertTrue(plans)
                self.assertEqual({row["preferred_skill"] for row in plans}, {"dynamic-research-agent"})
        for lens in ["demand", "supply", "technology", "valuation", "esg"]:
            for dimension in ["baseline", "financial_bridge", "refutation"]:
                self.assertEqual(_preferred_skill(lens, dimension), "dynamic-research-agent")
                for source in ["filing", "research", "dataset", "news"]:
                    self.assertEqual(_skill_for_source(source, dimension), "dynamic-research-agent")
        self.assertIn("cash_flow_quality", extraction_schema_for_task("financial_statement")["family_specific_fields"])
        self.assertIn("priced_in_assumptions", extraction_schema_for_task("valuation")["family_specific_fields"])
        self.assertIn("verification_source", extraction_schema_for_task("news_event")["family_specific_fields"])

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
        self.assertIn("exactly four numbered H2 sections", contract)
        self.assertIn("Internal QA trees", contract)

    def test_framework_records_current_execution_pipeline(self):
        combined = "\n".join(self._canonical_docs().values())
        for phrase in [
            "ResearchGoal -> DomainPlaybook -> QuestionArchitecture",
            "maximum depth five",
            "config/source_universes.json",
            "SourceUniverseRepository",
            "direct/Exa",
            "question x source",
            "dynamic-research-agent",
            "ReportViewModel",
            "CanonicalReportRenderer",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, combined)

    def test_framework_records_dual_material_intake_contract(self):
        combined = " ".join("\n".join(self._canonical_docs().values()).split())
        for phrase in [
            "material_class",
            "ingestion_channel",
            "question_search",
            "knowledge_base_scan",
            "official_filing",
            "sell_side_research",
            "authoritative_third_party",
            "market_news",
            "inbox/parse_tasks.jsonl",
            "visible, logged-in IMA",
            "must not call",
            "browser credentials",
            "cookies",
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

    def test_public_html_contract_covers_current_report_scopes(self):
        contract = self._canonical_docs()["research_report_contract.md"]
        for phrase in [
            "HTML is the default public artifact",
            "report_scope: standalone-bom",
            "需求侧",
            "供给侧",
            "技术侧",
            "估值侧",
            "ESG",
            "第一性原理逻辑链",
            "逻辑节点与原子观点材料",
            "派生证据视图",
            "Do not render a separate lens-level `全局结论与趋势`",
            "source row x numbered atomic claim",
            "effective_period",
            "target_period",
            "logic_chain_centered",
            "发布日期 | 报告名称 | 材料类型 | 原子观点 | 对逻辑点的影响",
            "One source occupies one row",
            "GPT-reviewed atomic claims",
            "project-local original-material link",
            "industry-index",
            "bom-node",
            "boms/<node_id>/professional_report.html",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, contract)

    def test_standalone_bom_investment_engine_is_locked_in_contracts(self):
        combined = "\n".join(self._canonical_docs().values())
        for phrase in [
            "logic_nodes",
            "claim_mappings.jsonl",
            "logic_states.jsonl",
            "entity_states.jsonl",
            "thesis_revisions.jsonl",
            "investment_snapshots.jsonl",
            "fundamental_delta",
            "consensus_delta",
            "priced_in_delta",
            "当前投资判断",
            "BOM x lens/question x logic node x company/entity x as_of_date",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, combined)

    def test_canonical_contracts_define_industry_parent_and_bom_children(self):
        combined = "\n".join(self._canonical_docs().values())
        for phrase in [
            "boms/<node_id>",
            "industry-index",
            "bom-node",
            "boms/manifest.json",
            "one industry-chain project",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, combined)

    def test_canonical_contracts_define_central_ima_archive_and_bom_state(self):
        combined = "\n".join(self._canonical_docs().values())
        for phrase in [
            "shared provider archive",
            "research/bom/<bom_project_id>",
            "source/ima/YYYY/MM/DD",
            "archive_manifest.jsonl",
            "material_intake/raw/",
            "click each visible download control",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, combined)

    def test_public_report_keeps_process_artifacts_internal(self):
        contract = self._canonical_docs()["research_report_contract.md"]
        self.assertIn("Do not render raw search queries", contract)
        self.assertIn("change logs", contract)
        self.assertIn("Freeze recommendations before attaching labels", contract)

    @staticmethod
    def _canonical_docs() -> dict[str, str]:
        paths = {
            "AGENTS.md": ROOT / "AGENTS.md",
            "research_goal_qa.md": ROOT / "skills" / "value_invest_research" / "frameworks" / "research_goal_qa.md",
            "research_report_contract.md": ROOT / "skills" / "value_invest_research" / "frameworks" / "research_report_contract.md",
        }
        return {name: path.read_text(encoding="utf-8") for name, path in paths.items()}


if __name__ == "__main__":
    unittest.main()
