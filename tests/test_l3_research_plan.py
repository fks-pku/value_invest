import unittest
from pathlib import Path

from value_invest_research.adapters.outbound.standalone_bom_html_renderer import (
    StandaloneBomHtmlRenderer,
)
from value_invest_research.adapters.outbound.standalone_bom_markdown_renderer import (
    StandaloneBomMarkdownRenderer,
)
from value_invest_research.adapters.outbound.standalone_bom_research_plan_html_renderer import (
    StandaloneBomResearchPlanHtmlRenderer,
)

from value_invest_research.application.use_cases.ingest_materials import (
    ingest_material_batch,
)
from value_invest_research.domain.l3_research_plan import (
    attach_l3_plan_summaries,
    build_l3_research_plan_set,
    validate_l3_research_plan_set,
)
from value_invest_research.domain.material_intake import (
    build_material_parse_tasks,
    normalize_material_document,
    validate_material_intake_bundle,
)
from value_invest_research.framework_contracts import (
    validate_research_plan_html_contract,
)


class _LeafContractRepository:
    leaf_search_required = True

    def load_seen_external_ids(self, provider, feed_id):
        return set()

    def persist_material_batch(self, *, documents, parse_tasks, scan_event):
        return {
            "new_documents": len(documents),
            "parse_tasks": len(parse_tasks),
        }


class L3ResearchPlanTests(unittest.TestCase):
    def _plan_set(self):
        parent = {
            "plan_id": "rp-parent",
            "steps": [
                {
                    "step_id": "step:demand.compute",
                    "question_node_id": "demand.compute",
                    "execution_mode": "child_plan_rollup",
                }
            ],
        }
        index, plans = build_l3_research_plan_set(
            l3_nodes=[
                {
                    "logic_node_id": "demand.compute",
                    "lens_id": "demand",
                    "title": "单位任务算力",
                    "question": "单位任务算力是否继续上升？",
                    "indicators": ["tokens per task", "compute per token"],
                    "support_rule": "总算力增速高于效率改善。",
                    "refute_rule": "效率改善完全抵消工作负载增长。",
                    "downstream_node_ids": ["demand.budget"],
                    "company_bridge_fields": ["GPU 数量", "收入"],
                }
            ],
            parent_plan_id="rp-parent",
            research_goal={"run_mode": "live_prediction", "as_of_date": "2026-09-02"},
        )
        return parent, index, plans

    def test_every_l3_has_nested_l4_and_executable_l5_leaf_steps(self):
        parent, index, plans = self._plan_set()
        plan = plans[0]

        self.assertEqual(len(plan["l4_units"]), 7)
        self.assertEqual(len(plan["steps"]), 7)
        self.assertTrue(all(step["level"] == 5 for step in plan["steps"]))
        self.assertTrue(
            all(
                step["collection_contract"]["origin"]
                == "leaf_question_search"
                for step in plan["steps"]
            )
        )
        queries = [
            tuple(
                query
                for source in step["source_plan"]
                for query in source["examples_or_search_queries"]
            )
            for step in plan["steps"]
        ]
        self.assertEqual(len(queries), len(set(queries)))
        validation = validate_l3_research_plan_set(
            parent_plan=parent,
            index=index,
            plans=plans,
        )
        self.assertTrue(validation["ok"], validation["issues"])
        self.assertEqual(validation["summary"]["leaf_steps"], 7)

    def test_same_source_requires_separate_leaf_parse_tasks(self):
        document = normalize_material_document(
            {
                "external_id": "source-1",
                "title": "GPU demand disclosure",
                "published_at": "2026-08-31",
                "source_type": "company_ir",
            },
            ingestion_channel="question_search",
            provider="exa",
            discovered_at="2026-09-02",
            default_bom_node_ids=["gpu_asic"],
            default_question_numbers=[1],
        )
        base = {
            "l3_plan_id": "l3rp-demand",
            "l3_node_id": "demand.compute",
            "l4_question_id": "demand.compute.l4.actual",
            "leaf_step_id": "leaf:demand.compute:actual",
            "search_run_id": "SCAN-1",
        }
        first = build_material_parse_tasks(
            document,
            leaf_context={
                **base,
                "leaf_question_id": "demand.compute.l4.actual.l5.answer",
            },
        )[0]
        second = build_material_parse_tasks(
            document,
            leaf_context={
                **base,
                "l4_question_id": "demand.compute.l4.history",
                "leaf_question_id": "demand.compute.l4.history.l5.answer",
                "leaf_step_id": "leaf:demand.compute:history",
                "search_run_id": "SCAN-2",
            },
        )[0]

        self.assertNotEqual(first["task_id"], second["task_id"])
        self.assertNotEqual(first["leaf_question_id"], second["leaf_question_id"])
        self.assertNotEqual(first["search_run_id"], second["search_run_id"])

    def test_broad_ingestion_is_candidate_only_under_leaf_contract(self):
        result = ingest_material_batch(
            repository=_LeafContractRepository(),
            raw_documents=[
                {
                    "external_id": "ima-1",
                    "title": "GPU industry report",
                    "published_at": "2026-08-31",
                    "source_type": "sell_side_report",
                }
            ],
            provider="ima",
            feed_id="daily",
            ingestion_channel="knowledge_base_scan",
            discovered_at="2026-09-02",
            known_bom_node_ids=["gpu_asic"],
            mode="live_prediction",
            as_of_date="2026-09-02",
            default_bom_node_ids=["gpu_asic"],
        )

        self.assertEqual(result["parse_tasks"], [])
        self.assertEqual(
            result["scan_event"]["evidence_eligibility"],
            "candidate_only",
        )

    def test_question_search_without_leaf_coordinate_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "finest-leaf"):
            ingest_material_batch(
                repository=_LeafContractRepository(),
                raw_documents=[],
                provider="exa",
                feed_id="gpu_asic:q1",
                ingestion_channel="question_search",
                discovered_at="2026-09-02",
                known_bom_node_ids=["gpu_asic"],
                mode="live_prediction",
                as_of_date="2026-09-02",
                default_bom_node_ids=["gpu_asic"],
            )

    def test_v2_parse_task_must_match_active_leaf_coordinate(self):
        document = normalize_material_document(
            {
                "external_id": "source-2",
                "title": "GPU filing",
                "published_at": "2026-08-31",
                "source_type": "company_ir",
            },
            ingestion_channel="question_search",
            provider="exa",
            discovered_at="2026-09-02",
            default_bom_node_ids=["gpu_asic"],
            default_question_numbers=[1],
        )
        task = build_material_parse_tasks(
            document,
            leaf_context={
                "l3_plan_id": "wrong-plan",
                "l3_node_id": "demand.compute",
                "l4_question_id": "demand.compute.l4.actual",
                "leaf_question_id": "demand.compute.l4.actual.l5.answer",
                "leaf_step_id": "leaf:demand.compute:actual",
                "search_run_id": "SCAN-1",
            },
        )[0]
        validation = validate_material_intake_bundle(
            {
                "project": {"mode": "live_prediction"},
                "known_bom_node_ids": ["gpu_asic"],
                "question_numbers_by_node": {"gpu_asic": [1, 2, 3, 4, 5]},
                "documents": [document],
                "node_inboxes": {
                    "gpu_asic": {
                        "materials": [document],
                        "parse_tasks": [task],
                    }
                },
                "leaf_search_contract_active": True,
                "leaf_plan_coordinates": [
                    {
                        "l3_plan_id": "right-plan",
                        "l3_node_id": "demand.compute",
                        "l4_question_id": "demand.compute.l4.actual",
                        "leaf_question_id": "demand.compute.l4.actual.l5.answer",
                        "leaf_step_id": "leaf:demand.compute:actual",
                    }
                ],
            }
        )
        self.assertFalse(validation["ok"])
        self.assertIn(
            "unknown_leaf_plan_coordinate",
            {issue["code"] for issue in validation["issues"]},
        )

    def test_renderers_show_the_independent_plan_under_the_l3(self):
        _, _, plans = self._plan_set()
        node = {
            "logic_node_id": "demand.compute",
            "title": "单位任务算力",
            "question": "单位任务算力是否继续上升？",
            "state": "unresolved",
            "conclusion": "待验证",
            "change_summary": "首个截面",
            "event_history_groups": [],
            "presentation_role": "causal_node",
        }
        lens = {
            "lens_id": "demand",
            "label": "需求侧",
            "logic_chain": "任务增加推动算力需求。",
            "claims": [],
            "logic_nodes": [node],
            "causal_nodes": [node],
            "derived_views": [],
        }
        view = {
            "title": "GPU BOM",
            "bom_node_id": "gpu_asic",
            "as_of_date": "2026-09-02",
            "research_model": "logic_chain_centered",
            "logic_chain_version": "v1",
            "lenses": [lens],
        }
        attach_l3_plan_summaries(view, plans=plans)

        html = StandaloneBomHtmlRenderer(Path(".")).render(view)
        markdown = StandaloneBomMarkdownRenderer().render(view)

        self.assertIn('data-l3-plan-contract="leaf-search-v2"', html)
        self.assertIn('href="research_plan.html"', html)
        self.assertEqual(html.count('class="l4-plan-unit"'), 7)
        self.assertEqual(html.count('class="leaf-plan-step"'), 7)
        self.assertIn("L3 独立研究计划", markdown)
        self.assertEqual(markdown.count("**L5 叶子：**"), 7)

    def test_dedicated_research_plan_html_exposes_full_l3_to_l5_plan(self):
        _, index, plans = self._plan_set()
        html = StandaloneBomResearchPlanHtmlRenderer().render(
            project={
                "title": "GPU BOM",
                "report_date": "2026-09-02",
            },
            bundle={
                "index": index,
                "plans": plans,
                "events_by_node": {},
            },
        )

        self.assertIn('data-report-scope="research-plan"', html)
        self.assertIn('data-plan-contract="leaf-search-v2"', html)
        self.assertEqual(html.count('class="l3-plan"'), 1)
        self.assertEqual(html.count('class="leaf" data-leaf-question-id='), 7)
        self.assertIn("L5 最细叶子问题", html)
        self.assertIn("定向材料与搜索锚点", html)
        self.assertIn("宽泛材料只进入候选池", html)
        self.assertIn('href="professional_report.html"', html)
        validation = validate_research_plan_html_contract(html, plans=plans)
        self.assertTrue(validation["ok"], validation["issues"])
        self.assertEqual(validation["summary"]["l3_plans"], 1)
        self.assertEqual(validation["summary"]["leaf_steps"], 7)


if __name__ == "__main__":
    unittest.main()
