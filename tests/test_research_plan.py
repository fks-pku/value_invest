import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from value_invest_research.adapters.outbound.filesystem_research_plan import (
    FileSystemResearchPlanRepository,
)
from value_invest_research.application.use_cases.build_research_plan import BuildResearchPlan
from value_invest_research.application.use_cases.plan_research_goal import PlanResearchGoal
from value_invest_research.application.use_cases.research_plan_execution import (
    RecordResearchStepEvent,
    ValidateResearchPlanExecution,
)
from value_invest_research.cli import main
from value_invest_research.domain.research_goal import ResearchGoal
from value_invest_research.domain.research_plan import build_research_plan


class ResearchPlanTests(unittest.TestCase):
    def test_parent_plan_turns_every_l3_into_a_child_plan_rollup(self):
        architecture = PlanResearchGoal().execute(
            ResearchGoal(
                topic="存储行业投资机会",
                research_type="industry",
                domain_hint="memory_industry",
                as_of_date="2026-08-31",
            )
        )

        plan = build_research_plan(architecture)
        leaf_ids = [node.id for node in architecture.nodes if not node.next_question_ids]

        self.assertEqual([step.question_node_id for step in plan.steps], leaf_ids)
        self.assertTrue(all(not step.source_plan for step in plan.steps))
        self.assertTrue(all(step.execution_mode == "child_plan_rollup" for step in plan.steps))
        self.assertTrue(all(step.child_plan_path for step in plan.steps))
        self.assertTrue(all(step.refuting_source_plan for step in plan.steps))
        self.assertTrue(all(step.minimum_evidence_gate for step in plan.steps))
        self.assertTrue(all(step.step_id == f"step:{step.question_node_id}" for step in plan.steps))
        q1_steps = {step.step_id for step in plan.steps if step.stage_id == "Q1"}
        q2_steps = [step for step in plan.steps if step.stage_id == "Q2"]
        self.assertTrue(q2_steps)
        self.assertTrue(all(set(step.depends_on_step_ids) == q1_steps for step in q2_steps))

    def test_step_cannot_complete_without_traceable_evidence_and_answer(self):
        with tempfile.TemporaryDirectory() as tmp:
            repository = FileSystemResearchPlanRepository(Path(tmp))
            architecture = PlanResearchGoal().execute(
                ResearchGoal(topic="测试研究", research_type="custom")
            )
            result = BuildResearchPlan(repository).execute(architecture)
            step_id = result["plan"]["steps"][0]["step_id"]

            with self.assertRaisesRegex(ValueError, "l3_rollup_cannot_complete_from_parent_events"):
                RecordResearchStepEvent(repository, clock=lambda: "2026-09-02T00:00:00+00:00").execute(
                    {
                        "step_id": step_id,
                        "event_type": "gate_evaluated",
                        "evidence_gate": {"passed": True, "reasons": ["claimed complete"]},
                    }
                )

            self.assertEqual(repository.load_step_events(), [])

    def test_append_only_events_project_a_completed_trace(self):
        with tempfile.TemporaryDirectory() as tmp:
            repository = FileSystemResearchPlanRepository(Path(tmp))
            architecture = PlanResearchGoal().execute(
                ResearchGoal(topic="测试研究", research_type="custom")
            )
            result = BuildResearchPlan(repository).execute(architecture)
            parent_plan = result["plan"]
            first_parent_step = parent_plan["steps"][0]
            child_dir = Path(tmp) / first_parent_step["child_plan_path"].removesuffix(
                "/research_plan.json"
            )
            repository = FileSystemResearchPlanRepository(child_dir)
            plan = repository.load_plan()
            first_step = plan["steps"][0]
            plan["plan_id"] = f"{plan['plan_id']}_single"
            plan["steps"] = [{**first_step, "depends_on_step_ids": []}]
            repository.save_plan(plan)
            step_id = first_step["step_id"]
            recorder = RecordResearchStepEvent(
                repository,
                clock=lambda: "2026-09-02T00:00:00+00:00",
            )

            recorder.execute(
                {
                    "step_id": step_id,
                    "event_type": "evidence_attached",
                    "source_ids": ["SRC-1"],
                    "source_extraction_ids": ["EXT-1"],
                    "source_review_ids": ["REV-1"],
                    "search_run_id": "SCAN-LEAF-1",
                }
            )
            recorder.execute(
                {
                    "step_id": step_id,
                    "event_type": "answer_recorded",
                    "answer": "证据支持当前回答，但仍需持续监控。",
                    "supporting_findings": ["一手来源支持。"],
                    "refuting_findings": ["已执行反证检索，当前未发现足以推翻的直接证据。"],
                    "gaps": ["缺少下一季度更新。"],
                    "next_actions": ["下季财报后刷新。"],
                }
            )
            final = recorder.execute(
                {
                    "step_id": step_id,
                    "event_type": "gate_evaluated",
                    "evidence_gate": {"passed": True, "reasons": ["minimum evidence gate passed"]},
                }
            )

            progress = final["progress"]
            self.assertTrue(progress["ok"], progress["issues"])
            self.assertEqual(progress["summary"]["status"], "completed")
            self.assertEqual(progress["summary"]["events"], 3)
            self.assertEqual(progress["step_states"][0]["source_review_ids"], ["REV-1"])
            self.assertTrue((child_dir / "research_plan_history" / f"{plan['plan_id']}.json").exists())

    def test_cli_creates_and_validates_a_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp) / "research" / "demo"
            out = StringIO()
            with redirect_stdout(out):
                exit_code = main(
                    [
                        "--root",
                        tmp,
                        "plan-research",
                        str(project_dir),
                        "--topic",
                        "AI 数据中心产业机会",
                        "--research-type",
                        "industry",
                        "--as-of-date",
                        "2026-08-31",
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertTrue((project_dir / "research_plan.json").exists())
            index = json.loads(
                (project_dir / "l3_research_plans" / "index.json").read_text(
                    encoding="utf-8"
                )
            )
            parent = json.loads(
                (project_dir / "research_plan.json").read_text(encoding="utf-8")
            )
            self.assertEqual(len(index["plans"]), len(parent["steps"]))
            self.assertGreater(len(index["plans"]), 0)
            child = json.loads(
                (project_dir / index["plans"][0]["path"]).read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(len(child["l4_units"]), 7)
            self.assertEqual(len(child["steps"]), 7)
            self.assertTrue(
                all(
                    step["collection_contract"]["origin"]
                    == "leaf_question_search"
                    for step in child["steps"]
                )
            )
            qa_tree = json.loads((project_dir / "qa_tree.json").read_text(encoding="utf-8"))
            leaf = next(node for node in qa_tree["nodes"] if node.get("research_step_id"))
            self.assertEqual(leaf["research_step_id"], f"step:{leaf['id']}")

            out = StringIO()
            with redirect_stdout(out):
                validation_exit = main(
                    ["--root", tmp, "validate-research-plan", str(project_dir)]
                )
            self.assertEqual(validation_exit, 0)
            self.assertIn("status=planned", out.getvalue())

    def test_missing_plan_is_reported_by_use_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = ValidateResearchPlanExecution(
                FileSystemResearchPlanRepository(Path(tmp))
            ).execute()

            self.assertFalse(result["ok"])
            self.assertEqual(result["issues"][0]["code"], "missing_research_plan")

    def test_new_plan_projects_only_its_events_and_keeps_old_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            repository = FileSystemResearchPlanRepository(Path(tmp))
            architecture = PlanResearchGoal().execute(
                ResearchGoal(topic="测试研究", research_type="custom")
            )
            first = BuildResearchPlan(repository).execute(architecture)["plan"]
            first_step_id = first["steps"][0]["step_id"]
            RecordResearchStepEvent(
                repository,
                clock=lambda: "2026-09-02T00:00:00+00:00",
            ).execute(
                {
                    "step_id": first_step_id,
                    "event_type": "collection_started",
                }
            )

            revised_architecture = PlanResearchGoal().execute(
                ResearchGoal(topic="测试研究修订版", research_type="custom")
            )
            revised = BuildResearchPlan(repository).execute(revised_architecture)["plan"]
            validation = ValidateResearchPlanExecution(repository).execute()

            self.assertNotEqual(first["plan_id"], revised["plan_id"])
            self.assertTrue(validation["ok"], validation["issues"])
            self.assertEqual(validation["summary"]["events"], 0)
            self.assertEqual(validation["summary"]["historical_plan_events"], 1)


if __name__ == "__main__":
    unittest.main()
