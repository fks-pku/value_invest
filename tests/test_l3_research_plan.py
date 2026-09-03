import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from value_invest_research.adapters.outbound.standalone_bom_html_renderer import (
    StandaloneBomHtmlRenderer,
)
from value_invest_research.adapters.outbound.standalone_bom_markdown_renderer import (
    StandaloneBomMarkdownRenderer,
)
from value_invest_research.adapters.outbound.research_plan_markdown_renderer import (
    ResearchPlanMarkdownRenderer,
)
from value_invest_research.adapters.outbound.research_plan_structure_html_renderer import (
    ResearchPlanStructureHtmlRenderer,
)
from value_invest_research.adapters.outbound.filesystem_research_plan import (
    FileSystemResearchPlanRepository,
)

from value_invest_research.application.use_cases.ingest_materials import (
    ingest_material_batch,
)
from value_invest_research.application.use_cases.expand_l3_research_plan import (
    ExpandL3ResearchPlan,
)
from value_invest_research.application.use_cases.research_plan_execution import (
    RecordResearchStepEvent,
)
from value_invest_research.domain.l3_research_plan import (
    build_l3_research_plan,
    build_l3_research_plan_set,
    expand_l3_research_plan,
    validate_l3_research_plan_set,
)
from value_invest_research.domain.material_intake import (
    build_material_parse_tasks,
    normalize_material_document,
    validate_material_intake_bundle,
)
from value_invest_research.framework_contracts import (
    validate_research_plan_markdown_contract,
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

    def test_every_l3_starts_as_one_executable_l3_question(self):
        parent, index, plans = self._plan_set()
        plan = plans[0]

        self.assertEqual(plan["question_tree"]["children"], [])
        self.assertEqual(len(plan["steps"]), 1)
        self.assertEqual({step["level"] for step in plan["steps"]}, {3})
        self.assertEqual(plan["steps"][0]["question_node_id"], "demand.compute")
        self.assertTrue(all(step["required_data"] for step in plan["steps"]))
        self.assertTrue(all(step["analysis_plan"] for step in plan["steps"]))
        self.assertTrue(
            all(
                step["collection_contract"]["origin"]
                == "active_question_search"
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
        self.assertEqual(validation["summary"]["leaf_steps"], 1)
        self.assertEqual(validation["summary"]["max_depth"], 3)

    def test_failed_gate_expands_only_one_level_at_a_time(self):
        plan = build_l3_research_plan(
            node={
                "logic_node_id": "technology.route",
                "lens_id": "technology",
                "question": "哪条技术路线更有商业优势？",
            },
            parent_plan_id="rp-parent",
            research_goal={"run_mode": "live_prediction"},
            source_universe={},
        )
        plan = expand_l3_research_plan(
            plan,
            parent_question_id="technology.route",
            evidence_gap="现有材料不能分别验证成本与采用。",
            child_questions=[
                {
                    "id": "technology.route.cost",
                    "question": "当前总拥有成本是否更低？",
                    "required_data": ["硬件、能耗和运维成本"],
                    "analysis_plan": ["统一负载与利用率后比较 TCO"],
                },
                {
                    "id": "technology.route.adoption",
                    "question": "客户采用是否能持续？",
                    "required_data": ["客户采用与部署证据"],
                    "analysis_plan": ["区分试用与生产采用"],
                },
            ],
        )
        plan = expand_l3_research_plan(
            plan,
            parent_question_id="technology.route.adoption",
            evidence_gap="采用材料未区分试用和生产扩容。",
            child_questions=[
                {
                    "id": "technology.route.adoption.production",
                    "question": "是否进入生产环境并扩大部署？",
                    "required_data": ["客户生产部署与扩容数据"],
                    "analysis_plan": ["区分试用、量产和扩容"],
                }
            ],
        )

        self.assertEqual([step["level"] for step in plan["steps"]], [4, 5])
        self.assertEqual(
            {step["leaf_question_id"] for step in plan["steps"]},
            {
                "technology.route.cost",
                "technology.route.adoption.production",
            },
        )

    def test_question_tree_rejects_depth_beyond_l5(self):
        plan = build_l3_research_plan(
            node={"logic_node_id": "technology.route", "question": "路线是否成立？"},
            parent_plan_id="rp-parent",
            research_goal={"run_mode": "live_prediction"},
            source_universe={},
        )
        plan = expand_l3_research_plan(
            plan,
            parent_question_id="technology.route",
            evidence_gap="需要 L4",
            child_questions=[{"id": "technology.route.l4", "question": "L4？"}],
        )
        plan = expand_l3_research_plan(
            plan,
            parent_question_id="technology.route.l4",
            evidence_gap="需要 L5",
            child_questions=[{"id": "technology.route.l5", "question": "L5？"}],
        )
        with self.assertRaisesRegex(ValueError, "cannot exceed L5"):
            expand_l3_research_plan(
                plan,
                parent_question_id="technology.route.l5",
                evidence_gap="不能继续",
                child_questions=[{"question": "L6？"}],
            )

    def test_persisted_expansion_requires_a_recorded_failed_gate(self):
        parent, index, plans = self._plan_set()
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            repository = FileSystemResearchPlanRepository(project_dir)
            repository.save_plan(parent)
            repository.save_l3_research_plans(index, plans)
            expander = ExpandL3ResearchPlan(repository)
            child_questions = [
                {
                    "id": "demand.compute.current",
                    "question": "哪些当前数据可以直接验证？",
                    "required_data": ["当前直接数据"],
                    "analysis_plan": ["核验当前事实"],
                    "trigger_gap": "缺少当前数据",
                }
            ]
            with self.assertRaisesRegex(ValueError, "failed answerability gate"):
                expander.execute(
                    l3_node_id="demand.compute",
                    parent_question_id="demand.compute",
                    child_questions=child_questions,
                )

            child_repo = FileSystemResearchPlanRepository(
                project_dir / "l3_research_plans" / "demand.compute"
            )
            RecordResearchStepEvent(child_repo, clock=lambda: "2026-09-02").execute(
                {
                    "event_type": "gate_evaluated",
                    "step_id": "question:demand.compute",
                    "evidence_gate": {"passed": False, "reasons": ["缺少当前数据"]},
                    "gaps": ["缺少当前数据"],
                    "next_actions": ["新增一个L4问题"],
                }
            )
            result = expander.execute(
                l3_node_id="demand.compute",
                parent_question_id="demand.compute",
                child_questions=child_questions,
            )
            self.assertEqual(result["child_question_ids"], ["demand.compute.current"])
            self.assertNotEqual(result["from_plan_id"], result["plan_id"])

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
            "question_level": "4",
            "research_step_id": "question:demand.compute.l4.actual",
            "search_run_id": "SCAN-1",
        }
        first = build_material_parse_tasks(
            document,
            leaf_context={
                **base,
                "question_node_id": "demand.compute.l4.actual",
            },
        )[0]
        second = build_material_parse_tasks(
            document,
            leaf_context={
                **base,
                "question_node_id": "demand.compute.l4.history",
                "research_step_id": "question:demand.compute.l4.history",
                "search_run_id": "SCAN-2",
            },
        )[0]

        self.assertNotEqual(first["task_id"], second["task_id"])
        self.assertNotEqual(first["question_node_id"], second["question_node_id"])
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
        with self.assertRaisesRegex(ValueError, "current active question"):
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

    def test_v3_parse_task_must_match_active_question_coordinate(self):
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
                "question_node_id": "demand.compute",
                "question_level": "3",
                "research_step_id": "question:demand.compute",
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
                        "question_node_id": "demand.compute",
                        "question_level": "3",
                        "research_step_id": "question:demand.compute",
                    }
                ],
            }
        )
        self.assertFalse(validation["ok"])
        self.assertIn(
            "unknown_active_question_plan_coordinate",
            {issue["code"] for issue in validation["issues"]},
        )

    def test_professional_report_keeps_questions_but_not_the_plan_document(self):
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
        html = StandaloneBomHtmlRenderer(Path(".")).render(view)
        markdown = StandaloneBomMarkdownRenderer().render(view)

        self.assertIn("单位任务算力是否继续上升？", html)
        self.assertIn("**研究问题：** 单位任务算力是否继续上升？", markdown)
        self.assertNotIn("research_plan.html", html)
        self.assertNotIn("L3 独立研究计划", markdown)

    def test_dedicated_research_plan_markdown_exposes_tree_and_leaf_work(self):
        _, index, plans = self._plan_set()
        markdown = ResearchPlanMarkdownRenderer().render(
            project={
                "title": "GPU BOM",
                "report_date": "2026-09-02",
            },
            bundle={
                "index": index,
                "plans": plans,
                "events_by_node": {},
                "qa_tree": {
                    "nodes": [
                        {
                            "id": "gpu.decision",
                            "level": 1,
                            "question": "GPU 是否有投资机会？",
                            "next_question_ids": ["lens.demand"],
                        },
                        {
                            "id": "lens.demand",
                            "level": 2,
                            "question": "需求能否形成商业闭环？",
                            "parent_id": "gpu.decision",
                            "next_question_ids": ["demand.compute"],
                        },
                    ]
                },
            },
        )

        self.assertIn("dynamic-question-tree-v4", markdown)
        self.assertIn("L1 · 顶层问题", markdown)
        self.assertIn("L2 · 需求侧", markdown)
        self.assertNotIn("L4 子问题", markdown)
        self.assertNotIn("L5 叶子", markdown)
        self.assertIn("初始只到 L3", markdown)
        self.assertIn("需要搜集的数据", markdown)
        self.assertIn("需要做的分析", markdown)
        self.assertIn("宽泛材料池只提供候选", markdown)
        self.assertNotIn("优先材料类型", markdown)
        self.assertNotIn("前置叶子", markdown)
        self.assertNotIn("当前状态", markdown)
        validation = validate_research_plan_markdown_contract(markdown, plans=plans)
        self.assertTrue(validation["ok"], validation["issues"])
        self.assertEqual(validation["summary"]["l3_plans"], 1)
        self.assertEqual(validation["summary"]["leaf_steps"], 1)

    def test_structure_html_respects_focused_demand_scope(self):
        _, _, demand_plans = self._plan_set()
        supply_plan = build_l3_research_plan(
            node={
                "logic_node_id": "supply.capacity",
                "lens_id": "supply",
                "title": "供给能力",
                "question": "供给能否跟上？",
            },
            parent_plan_id="rp-parent",
            research_goal={"run_mode": "live_prediction"},
            source_universe={},
        )
        html = ResearchPlanStructureHtmlRenderer().render(
            project={
                "title": "GPU BOM",
                "as_of_date": "2026-09-02",
                "active_research_scope": {
                    "lens_ids": ["demand"],
                    "paused_lens_ids": ["supply"],
                },
            },
            bundle={
                "plans": [*demand_plans, supply_plan],
                "events_by_node": {},
            },
        )

        self.assertIn('data-active-lenses="demand"', html)
        self.assertIn("单位任务算力是否继续上升？", html)
        self.assertNotIn("供给能否跟上？", html)
        self.assertIn("当前只执行：需求侧", html)
        self.assertIn("搜集什么", html)
        self.assertIn("怎么分析", html)


if __name__ == "__main__":
    unittest.main()
