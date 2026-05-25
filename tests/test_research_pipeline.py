import json
import unittest
from pathlib import Path

from tests.helpers import project_tmp_dir
from value_invest_research.research_pipeline import run_meta_qa_pipeline, run_stock_qa_pipeline
from value_invest_research.scaffold import init_stock


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class _FakeLlmClient:
    def __init__(self):
        self.calls: list[tuple[str, str]] = []

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        self.calls.append((system_prompt, user_prompt))
        return json.dumps(
            {
                "answer": "LLM回答：pipeline 已把四类信息合成为可上抛的专业判断。",
                "facts": ["LLM事实：pipeline 传入了 QA 任务。"],
                "inferences": ["LLM推论：答案可写回 synthesis_overrides。"],
                "judgment": "LLM判断：链路已接通。",
                "gaps": ["LLM缺口：仍需真实外部资料增强。"],
                "next_data": ["LLM下一步：补真实公告和研报。"],
                "confidence": "medium",
                "source_balance": "LLM来源结构：以任务为准。",
                "supporting_evidence": ["LLM支撑：任务来源索引。"],
                "refuting_evidence": [],
                "research_leads": ["LLM线索：继续收集。"],
                "rollup": "LLM上抛：pipeline 可生成并回写专业答案。",
            },
            ensure_ascii=False,
        )


class _FakePlannerClient:
    def __init__(self):
        self.calls: list[tuple[str, str]] = []

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        self.calls.append((system_prompt, user_prompt))
        return json.dumps(
            {
                "planner_rationale": "LLM规划：先拆需求验证，再拆利润池。",
                "detected_signals": ["smart_ev"],
                "l1": [
                    {
                        "id": "demand_validation",
                        "question": "智能电动车需求是否由真实用户价值驱动？",
                        "rationale": "需求质量决定行业长期投资价值。",
                        "should_drill_down": True,
                        "l2": [
                            {
                                "id": "order_quality",
                                "question": "订单、交付和退订是否能证明需求质量？",
                                "rationale": "订单质量比口径总量更重要。",
                                "should_drill_down": True,
                                "l3": [
                                    {
                                        "id": "delivery_evidence",
                                        "question": "哪些证据能验证订单到交付的真实转化？",
                                        "rationale": "叶子问题进入资料搜集。",
                                        "should_drill_down": False,
                                        "should_collect_information": True,
                                        "terminal_reason": "已到达可回答粒度。",
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
            ensure_ascii=False,
        )


class ResearchPipelineTests(unittest.TestCase):
    def test_stock_qa_pipeline_writes_manifest_and_tasks(self):
        with project_tmp_dir() as tmp:
            stock_dir = init_stock(tmp, "AAPL", "Apple Inc.")
            (stock_dir / "evidence.jsonl").write_text(
                json.dumps({
                    "id": "ev_aapl_sec_revenue_20260328",
                    "research_object": "stocks/AAPL",
                    "source_type": "sec_fact",
                    "source_name": "SEC XBRL Revenue",
                    "url": "local://stocks/AAPL/data/sec_facts.json",
                    "published_at": "2026-05-01T00:00:00Z",
                    "fetched_at": "2026-05-08T17:46:28+00:00",
                    "hash": "sha256:test",
                    "tickers": ["AAPL"],
                    "sectors": [],
                    "themes": [],
                    "summary": "Revenue was 111184000000 USD and gross profit was 51200000000 USD.",
                    "reliability": "primary",
                    "materiality": "medium",
                    "used_in": [],
                }) + "\n",
                encoding="utf-8",
            )

            result = run_stock_qa_pipeline(tmp, "APPL", task_limit=5)

            research_dir = stock_dir / "research_system"
            current = json.loads((research_dir / "pipeline_run.json").read_text(encoding="utf-8"))
            history = _read_jsonl(research_dir / "pipeline_runs.jsonl")
            self.assertEqual(result["object_id"], "AAPL")
            self.assertEqual(current["pipeline"], "stock_qa_pipeline")
            self.assertEqual([stage["name"] for stage in current["stages"]], ["build_research_system", "build_collection_tasks", "build_synthesis_tasks"])
            self.assertTrue(current["final"]["report_path"].endswith("research_report.html"))
            self.assertTrue(current["final"]["task_path"].endswith("collection_tasks.jsonl"))
            self.assertTrue(current["final"]["synthesis_task_path"].endswith("synthesis_tasks.jsonl"))
            self.assertEqual(history[-1]["pipeline"], "stock_qa_pipeline")

    def test_meta_qa_pipeline_with_imported_search_results_discovers_candidates(self):
        with project_tmp_dir() as tmp:
            initial = run_meta_qa_pipeline(
                tmp,
                "industry",
                "机器人",
                "分析人形机器人产业链的投资价值",
                project_id="robotics_chain",
                task_limit=1,
            )
            project_dir = Path(initial["final"]["project_dir"])
            task = _read_jsonl(project_dir / "collection_tasks.jsonl")[0]
            search_results_path = tmp / "search_results.jsonl"
            search_results_path.write_text(
                json.dumps({
                    "task_id": task["task_id"],
                    "title": "Robot Industry Research Report PDF",
                    "url": "https://research.example.com/robotics/report.pdf",
                    "snippet": "Research report discusses robot shipments, pricing and customer validation.",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            result = run_meta_qa_pipeline(
                tmp,
                "industry",
                "机器人",
                "分析人形机器人产业链的投资价值",
                project_id="robotics_chain",
                task_limit=1,
                discover_candidates=True,
                search_results_path=search_results_path,
                candidate_min_score=0,
            )

            current = json.loads((project_dir / "pipeline_run.json").read_text(encoding="utf-8"))
            candidates = _read_jsonl(project_dir / "source_candidates.jsonl")
            self.assertEqual(result["final"]["project_id"], "robotics_chain")
            self.assertEqual(current["pipeline"], "meta_qa_pipeline")
            self.assertIn("discover_source_candidates", [stage["name"] for stage in current["stages"]])
            self.assertTrue(candidates)
            self.assertTrue(candidates[0]["accepted"])
            self.assertTrue(current["final"]["candidate_path"].endswith("source_candidates.jsonl"))

    def test_meta_qa_pipeline_can_use_llm_question_planner(self):
        with project_tmp_dir() as tmp:
            client = _FakePlannerClient()

            result = run_meta_qa_pipeline(
                tmp,
                "industry",
                "中国智能电动车",
                "了解中国智能电动车行业的长期投资价值",
                project_id="smart_ev_pipeline_llm_plan",
                task_limit=1,
                planner_client=client,
            )

            project_dir = Path(result["final"]["project_dir"])
            current = json.loads((project_dir / "pipeline_run.json").read_text(encoding="utf-8"))
            report = (project_dir / "research_report.html").read_text(encoding="utf-8")
            self.assertEqual(result["final"]["planning_mode"], "llm")
            self.assertEqual(current["final"]["planning_mode"], "llm")
            self.assertEqual(len(client.calls), 1)
            self.assertIn("智能电动车需求是否由真实用户价值驱动", report)

    def test_stock_qa_pipeline_can_apply_answer_synthesis(self):
        with project_tmp_dir() as tmp:
            stock_dir = init_stock(tmp, "AAPL", "Apple Inc.")
            (stock_dir / "evidence.jsonl").write_text(
                json.dumps({
                    "id": "ev_aapl_sec_revenue_20260328",
                    "research_object": "stocks/AAPL",
                    "source_type": "sec_fact",
                    "source_name": "SEC XBRL Revenue",
                    "url": "local://stocks/AAPL/data/sec_facts.json",
                    "published_at": "2026-05-01T00:00:00Z",
                    "fetched_at": "2026-05-08T17:46:28+00:00",
                    "hash": "sha256:test",
                    "tickers": ["AAPL"],
                    "sectors": [],
                    "themes": [],
                    "summary": "Revenue was 111184000000 USD and gross profit was 51200000000 USD.",
                    "reliability": "primary",
                    "materiality": "medium",
                    "used_in": [],
                }) + "\n",
                encoding="utf-8",
            )

            result = run_stock_qa_pipeline(tmp, "AAPL", task_limit=2, synthesize_answers=True)

            research_dir = stock_dir / "research_system"
            current = json.loads((research_dir / "pipeline_run.json").read_text(encoding="utf-8"))
            report = (research_dir / "research_report.html").read_text(encoding="utf-8")
            self.assertIn("run_answer_synthesis", [stage["name"] for stage in current["stages"]])
            self.assertIn("refresh_report_after_synthesis", [stage["name"] for stage in current["stages"]])
            self.assertTrue(result["final"]["synthesized_answer_path"].endswith("synthesized_answers.jsonl"))
            self.assertIn("专业回答：围绕", report)

    def test_stock_qa_pipeline_can_run_leaf_first_research(self):
        with project_tmp_dir() as tmp:
            stock_dir = init_stock(tmp, "AAPL", "Apple Inc.")
            (stock_dir / "evidence.jsonl").write_text(
                json.dumps({
                    "id": "ev_aapl_sec_revenue_20260328",
                    "research_object": "stocks/AAPL",
                    "source_type": "sec_fact",
                    "source_name": "SEC XBRL Revenue",
                    "url": "local://stocks/AAPL/data/sec_facts.json",
                    "published_at": "2026-05-01T00:00:00Z",
                    "fetched_at": "2026-05-08T17:46:28+00:00",
                    "hash": "sha256:test",
                    "tickers": ["AAPL"],
                    "sectors": [],
                    "themes": [],
                    "summary": "Revenue was 111184000000 USD and gross profit was 51200000000 USD.",
                    "reliability": "primary",
                    "materiality": "medium",
                    "used_in": [],
                }) + "\n",
                encoding="utf-8",
            )

            result = run_stock_qa_pipeline(
                tmp,
                "AAPL",
                task_limit=2,
                leaf_research_provider="mock",
                leaf_research_limit=1,
            )

            research_dir = stock_dir / "research_system"
            current = json.loads((research_dir / "pipeline_run.json").read_text(encoding="utf-8"))
            stage_names = [stage["name"] for stage in current["stages"]]
            self.assertIn("run_leaf_research", stage_names)
            self.assertIn("synthesize_leaf_answers", stage_names)
            self.assertIn("rollup_research_answers", stage_names)
            self.assertTrue((research_dir / "leaf_research_tasks.jsonl").exists())
            self.assertTrue((research_dir / "leaf_research_results.jsonl").exists())
            self.assertTrue((research_dir / "leaf_answers.jsonl").exists())
            self.assertTrue((research_dir / "rollup_answers.jsonl").exists())
            self.assertEqual(result["final"]["leaf_research_provider"], "mock")
            self.assertTrue(result["final"]["leaf_research_result_path"].endswith("leaf_research_results.jsonl"))
            self.assertTrue(result["final"]["leaf_answer_path"].endswith("leaf_answers.jsonl"))
            self.assertTrue(result["final"]["rollup_answer_path"].endswith("rollup_answers.jsonl"))

    def test_stock_qa_pipeline_can_use_llm_answer_synthesis(self):
        with project_tmp_dir() as tmp:
            stock_dir = init_stock(tmp, "AAPL", "Apple Inc.")
            (stock_dir / "evidence.jsonl").write_text(
                json.dumps({
                    "id": "ev_aapl_sec_revenue_20260328",
                    "research_object": "stocks/AAPL",
                    "source_type": "sec_fact",
                    "source_name": "SEC XBRL Revenue",
                    "url": "local://stocks/AAPL/data/sec_facts.json",
                    "published_at": "2026-05-01T00:00:00Z",
                    "fetched_at": "2026-05-08T17:46:28+00:00",
                    "hash": "sha256:test",
                    "tickers": ["AAPL"],
                    "sectors": [],
                    "themes": [],
                    "summary": "Revenue was 111184000000 USD and gross profit was 51200000000 USD.",
                    "reliability": "primary",
                    "materiality": "medium",
                    "used_in": [],
                }) + "\n",
                encoding="utf-8",
            )
            client = _FakeLlmClient()

            result = run_stock_qa_pipeline(tmp, "AAPL", task_limit=1, synthesize_answers=True, synthesis_client=client)

            research_dir = stock_dir / "research_system"
            report = (research_dir / "research_report.html").read_text(encoding="utf-8")
            self.assertEqual(result["final"]["synthesis_mode"], "llm")
            self.assertEqual(len(client.calls), 1)
            self.assertIn("LLM回答：pipeline", report)

    def test_meta_qa_pipeline_can_write_professional_report(self):
        with project_tmp_dir() as tmp:
            result = run_meta_qa_pipeline(
                tmp,
                "industry",
                "机器人",
                "分析人形机器人产业链的投资价值",
                project_id="robotics_chain",
                task_limit=1,
                write_professional_report=True,
            )

            project_dir = Path(result["final"]["project_dir"])
            current = json.loads((project_dir / "pipeline_run.json").read_text(encoding="utf-8"))
            report_path = Path(result["final"]["professional_report_path"])
            markdown_path = Path(result["final"]["professional_report_md_path"])
            self.assertIn("write_professional_report", [stage["name"] for stage in current["stages"]])
            self.assertEqual(current["final"]["professional_report_mode"], "deterministic")
            self.assertTrue(report_path.exists())
            self.assertTrue(markdown_path.exists())
            self.assertIn("专业投研报告", markdown_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
