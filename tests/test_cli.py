import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

from tests.helpers import project_tmp_dir
from value_invest_research.cli import main


class _FakeUrlResponse:
    def __init__(self, body: str, url: str = "https://example.com/source", content_type: str = "text/html; charset=utf-8"):
        self._body = body.encode("utf-8")
        self._url = url
        self.headers = {"Content-Type": content_type}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self) -> bytes:
        return self._body

    def geturl(self) -> str:
        return self._url


class _FakeLlmClient:
    def __init__(self):
        self.calls: list[tuple[str, str]] = []

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        self.calls.append((system_prompt, user_prompt))
        return json.dumps(
            {
                "answer": "LLM回答：CLI 已把 synthesis task 转成专业答案。",
                "facts": ["LLM事实：CLI 传入了任务。"],
                "inferences": ["LLM推论：答案可回写报告。"],
                "judgment": "LLM判断：CLI 链路可用。",
                "gaps": ["LLM缺口：真实研究仍需外部资料。"],
                "next_data": ["LLM下一步：补公告和研报。"],
                "confidence": "medium",
                "source_balance": "LLM来源结构：按任务 source_index。",
                "supporting_evidence": ["LLM支撑：任务来源索引。"],
                "refuting_evidence": [],
                "research_leads": ["LLM线索：继续补资料。"],
                "rollup": "LLM上抛：CLI LLM 答案合成链路已接通。",
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
                "planner_rationale": "LLM规划：围绕新品类成立条件拆问题。",
                "detected_signals": ["ai", "long_term_value"],
                "l1": [
                    {
                        "id": "product_market_fit",
                        "question": "AI 眼镜是否已经证明产品市场匹配？",
                        "rationale": "新品类投资价值需要先看真实用户需求。",
                        "should_drill_down": True,
                        "l2": [
                            {
                                "id": "retention_loop",
                                "question": "出货、留存和使用频次是否形成正向循环？",
                                "rationale": "留存决定硬件新品类是否可持续。",
                                "should_drill_down": True,
                                "l3": [
                                    {
                                        "id": "usage_evidence",
                                        "question": "哪些证据能验证 AI 眼镜使用频次和留存？",
                                        "rationale": "该问题可直接进入四类信息搜集。",
                                        "should_drill_down": False,
                                        "should_collect_information": True,
                                        "terminal_reason": "已到达可回答粒度。",
                                        "information_focus": {
                                            "evidence": "公司公告、出货数据、留存数据。",
                                            "research_report": "商业研报对使用场景和留存的分析。",
                                            "message": "新品发布、渠道反馈和未证实销量消息。",
                                            "opinion": "专家和产业人士观点。",
                                        },
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
            ensure_ascii=False,
        )


class CliTests(unittest.TestCase):
    def test_init_stock_command(self):
        with project_tmp_dir() as tmp:
            with redirect_stdout(StringIO()):
                exit_code = main(["--root", str(tmp), "init-stock", "MSFT", "--company-name", "Microsoft Corporation"])
            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmp) / "stocks" / "MSFT" / "investment_memo.md").exists())

    def test_init_event_command(self):
        with project_tmp_dir() as tmp:
            with redirect_stdout(StringIO()):
                exit_code = main(["--root", str(tmp), "init-event", "2026-05-06", "US Iran Conflict"])
            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmp) / "research" / "events" / "2026-05-06_us_iran_conflict").exists())

    def test_research_stock_command_prints_report_path(self):
        with project_tmp_dir() as tmp:
            result = {
                "ticker": "AAPL",
                "report_path": str(Path(tmp) / "stocks" / "AAPL" / "research_reports" / "report.md"),
                "signal_path": str(Path(tmp) / "stocks" / "AAPL" / "research_reports" / "signal.json"),
                "response_length": 100,
            }
            mock_researcher = MagicMock()
            mock_researcher.run_stock_research.return_value = result

            with patch("value_invest_research.cli._get_llm_client", return_value=MagicMock()):
                with patch("value_invest_research.stock_researcher.StockResearcher", return_value=mock_researcher):
                    out = StringIO()
                    with redirect_stdout(out):
                        exit_code = main(["--root", str(tmp), "research-stock", "AAPL", "--api-key", "test"])

            self.assertEqual(exit_code, 0)
            self.assertIn("Stock research saved", out.getvalue())
            self.assertIn("signal.json", out.getvalue())

    def test_build_evidence_command_prints_record_counts(self):
        with project_tmp_dir() as tmp:
            stock_dir = Path(tmp) / "stocks" / "AAPL"
            data_dir = stock_dir / "data"
            data_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
            (stock_dir / "evidence.jsonl").write_text("", encoding="utf-8")
            (data_dir / "prices.csv").write_text("date,Close\n2026-05-05,204\n", encoding="utf-8")

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main(["--root", str(tmp), "build-evidence", "AAPL"])

            self.assertEqual(exit_code, 0)
            self.assertIn("Evidence built for AAPL", out.getvalue())
            self.assertIn("records_new", out.getvalue())

    def test_build_research_graph_command_prints_graph_paths(self):
        with project_tmp_dir() as tmp:
            stock_dir = Path(tmp) / "stocks" / "AAPL"
            stock_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
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
                    "summary": "Revenue was 111184000000 USD for period ending 2026-03-28 in 10-Q.",
                    "reliability": "primary",
                    "materiality": "medium",
                    "used_in": [],
                }) + "\n",
                encoding="utf-8",
            )

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main(["--root", str(tmp), "build-research-graph", "APPL"])

            self.assertEqual(exit_code, 0)
            self.assertIn("Research graph built for AAPL", out.getvalue())
            self.assertIn("forward_report.html", out.getvalue())

    def test_build_research_system_command_prints_dashboard_path(self):
        with project_tmp_dir() as tmp:
            stock_dir = Path(tmp) / "stocks" / "AAPL"
            stock_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
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
                    "summary": "Revenue was 111184000000 USD for period ending 2026-03-28 in 10-Q.",
                    "reliability": "primary",
                    "materiality": "medium",
                    "used_in": [],
                }) + "\n",
                encoding="utf-8",
            )

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main(["--root", str(tmp), "build-research-system", "APPL"])

            self.assertEqual(exit_code, 0)
            self.assertIn("Research system built for AAPL", out.getvalue())
            self.assertIn("research_dashboard.html", out.getvalue())
            self.assertIn("research_report.html", out.getvalue())
            self.assertIn("information_collection.jsonl", out.getvalue())

    def test_stock_qa_pipeline_command_prints_run_manifest(self):
        with project_tmp_dir() as tmp:
            stock_dir = Path(tmp) / "stocks" / "AAPL"
            stock_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
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

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "run-stock-qa-pipeline",
                    "APPL",
                    "--task-limit",
                    "3",
                    "--leaf-research-provider",
                    "mock",
                    "--leaf-research-limit",
                    "1",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Stock QA pipeline completed for AAPL", out.getvalue())
            self.assertIn("pipeline_run.json", out.getvalue())
            self.assertIn("leaf_research_results.jsonl", out.getvalue())
            self.assertTrue((stock_dir / "research_system" / "pipeline_run.json").exists())
            self.assertTrue((stock_dir / "research_system" / "leaf_answers.jsonl").exists())

    def test_add_research_question_command_prints_paths(self):
        with project_tmp_dir() as tmp:
            stock_dir = Path(tmp) / "stocks" / "AAPL"
            stock_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
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
                    "summary": "Revenue was 111184000000 USD for period ending 2026-03-28 in 10-Q.",
                    "reliability": "primary",
                    "materiality": "medium",
                    "used_in": [],
                }) + "\n",
                encoding="utf-8",
            )

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "add-research-question",
                    "APPL",
                    "--parent-id",
                    "foundation.current_business",
                    "--question",
                    "服务收入质量是否改善？",
                    "--terminal",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Research question created for AAPL", out.getvalue())
            self.assertIn("terminal=True", out.getvalue())
            self.assertIn("custom_questions.jsonl", out.getvalue())
            self.assertIn("research_report.html", out.getvalue())
            self.assertIn("information_collection.jsonl", out.getvalue())

    def test_record_question_information_command_prints_paths(self):
        with project_tmp_dir() as tmp:
            stock_dir = Path(tmp) / "stocks" / "AAPL"
            stock_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
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

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "record-question-information",
                    "APPL",
                    "--node-id",
                    "current_business.profit-cash.segment-profit-pool",
                    "--category",
                    "research_report",
                    "--source-type",
                    "sell_side_report",
                    "--source-name",
                    "Apple Segment Margin Note",
                    "--url",
                    "https://example.com/aapl/segment-margin",
                    "--summary",
                    "第三方研究认为服务和硬件利润池需要分开验证。",
                ])

            rows = [
                json.loads(line)
                for line in (stock_dir / "evidence.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(exit_code, 0)
            self.assertIn("Question information created for AAPL", out.getvalue())
            self.assertIn("evidence=", out.getvalue())
            self.assertIn("research_report.html", out.getvalue())
            self.assertTrue(
                any(
                    row.get("source_name") == "Apple Segment Margin Note"
                    and "research_system:current_business.profit-cash.segment-profit-pool" in row.get("used_in", [])
                    for row in rows
                )
            )

    def test_collection_task_commands_print_paths(self):
        with project_tmp_dir() as tmp:
            stock_dir = Path(tmp) / "stocks" / "AAPL"
            stock_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
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

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "build-collection-tasks",
                    "APPL",
                    "--limit",
                    "3",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Collection tasks built for AAPL", out.getvalue())
            self.assertIn("collection_tasks.jsonl", out.getvalue())
            self.assertTrue((stock_dir / "research_system" / "collection_tasks.jsonl").exists())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "run-collection-tasks",
                    "APPL",
                    "--limit",
                    "1",
                    "--min-score",
                    "0",
                    "--dry-run",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Collection tasks run for AAPL", out.getvalue())
            self.assertIn("collection_results.jsonl", out.getvalue())

            import_path = Path(tmp) / "aapl_collected.jsonl"
            import_path.write_text(
                json.dumps({
                    "node_id": "current_business.profit-cash.segment-profit-pool",
                    "category": "evidence",
                    "source_type": "company_ir",
                    "source_name": "Apple Segment Facts",
                    "url": "https://example.com/aapl/segment-facts",
                    "summary": "公司材料补充披露分部利润池和服务收入质量。",
                    "reliability": "primary",
                    "materiality": "high",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "import-question-information",
                    "APPL",
                    "--path",
                    str(import_path),
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Question information imported for AAPL", out.getvalue())
            self.assertIn("created=1", out.getvalue())
            self.assertIn("research_report.html", out.getvalue())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "build-synthesis-tasks",
                    "APPL",
                    "--limit",
                    "2",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Answer synthesis tasks built for AAPL", out.getvalue())
            self.assertIn("synthesis_tasks.jsonl", out.getvalue())

            synthesis_path = Path(tmp) / "aapl_synthesis.jsonl"
            synthesis_path.write_text(
                json.dumps({
                    "node_id": "current_business.profit-cash.segment-profit-pool",
                    "answer": "专业回答：服务与硬件利润池需要拆开验证，当前只能形成中等置信度判断。",
                    "judgment": "利润池判断需要分部毛利和现金流共同验证。",
                    "gaps": ["缺少更细分业务口径。"],
                    "confidence": "medium",
                    "rollup": "当前生意质量要回到服务与硬件利润池拆分验证。",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "import-answer-synthesis",
                    "APPL",
                    "--path",
                    str(synthesis_path),
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Answer synthesis imported for AAPL", out.getvalue())
            self.assertIn("synthesis_overrides.jsonl", out.getvalue())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "run-answer-synthesis",
                    "APPL",
                    "--limit",
                    "2",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Answer synthesis applied for AAPL", out.getvalue())
            self.assertIn("mode=deterministic", out.getvalue())
            self.assertIn("synthesized_answers.jsonl", out.getvalue())

            client = _FakeLlmClient()
            out = StringIO()
            with patch("value_invest_research.cli._get_llm_client", return_value=client):
                with redirect_stdout(out):
                    exit_code = main([
                        "--root",
                        str(tmp),
                        "run-answer-synthesis",
                        "APPL",
                        "--limit",
                        "1",
                        "--use-llm",
                        "--api-key",
                        "test",
                    ])

            self.assertEqual(exit_code, 0)
            self.assertEqual(len(client.calls), 1)
            self.assertIn("Answer synthesis applied for AAPL", out.getvalue())
            self.assertIn("mode=llm", out.getvalue())

            task = [
                json.loads(line)
                for line in (stock_dir / "research_system" / "collection_tasks.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ][0]
            search_results_path = Path(tmp) / "aapl_search_results.jsonl"
            search_results_path.write_text(
                json.dumps({
                    "task_id": task["task_id"],
                    "title": "Apple Official Investor Relations",
                    "url": "https://ir.example.com/aapl/source",
                    "snippet": "Official IR disclosure for Apple segment facts.",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "discover-source-candidates",
                    "APPL",
                    "--limit",
                    "1",
                    "--results-per-task",
                    "1",
                    "--search-results-path",
                    str(search_results_path),
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Source candidates discovered for AAPL", out.getvalue())
            self.assertIn("source_candidates.jsonl", out.getvalue())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "apply-source-candidates",
                    "APPL",
                    "--path",
                    str(stock_dir / "research_system" / "source_candidates.jsonl"),
                    "--dry-run",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Source candidates applied for AAPL", out.getvalue())
            self.assertIn("dry-run", out.getvalue())

            queue_path = Path(tmp) / "aapl_questions.jsonl"
            queue_path.write_text(
                json.dumps({
                    "parent_id": "foundation.current_business",
                    "question": "服务收入增长是否来自价格还是用户规模？",
                    "terminal": True,
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "apply-question-queue",
                    "APPL",
                    "--path",
                    str(queue_path),
                    "--limit",
                    "5",
                    "--synthesize-answers",
                    "--write-professional-report",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Question queue applied for AAPL", out.getvalue())
            self.assertIn("created=1", out.getvalue())
            self.assertIn("collection_tasks.jsonl", out.getvalue())
            self.assertIn("synthesis_mode=deterministic", out.getvalue())
            self.assertIn("professional_report.html", out.getvalue())
            self.assertTrue((stock_dir / "research_system" / "professional_report.html").exists())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "validate-qa-system",
                    "APPL",
                    "--require-professional-report",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Stock QA validation OK", out.getvalue())
            self.assertIn("professional_report.html", out.getvalue())

    def test_leaf_research_commands_print_paths(self):
        with project_tmp_dir() as tmp:
            stock_dir = Path(tmp) / "stocks" / "XIAOMI"
            stock_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
            (stock_dir / "company_profile.md").write_text(
                "# XIAOMI Company Profile\n\n- Company: Xiaomi Corporation\n- Ticker: XIAOMI\n",
                encoding="utf-8",
            )
            (stock_dir / "evidence.jsonl").write_text(
                json.dumps({
                    "id": "ev_xiaomi_cli_foundation",
                    "research_object": "stocks/XIAOMI",
                    "source_type": "annual_report",
                    "source_name": "Xiaomi Annual Report",
                    "url": "https://example.com/xiaomi/annual",
                    "published_at": "2026-04-28T00:00:00Z",
                    "fetched_at": "2026-05-23T00:00:00+08:00",
                    "hash": "sha256:ev_xiaomi_cli_foundation",
                    "tickers": ["XIAOMI"],
                    "sectors": [],
                    "themes": [],
                    "summary": "Xiaomi disclosed revenue, gross margin, cash flow, smartphone shipments, IoT, internet services, and EV progress.",
                    "reliability": "primary",
                    "materiality": "high",
                    "used_in": [],
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "build-leaf-research-tasks",
                    "XIAOMI",
                    "--limit",
                    "2",
                ])
            self.assertEqual(exit_code, 0)
            self.assertIn("Leaf research tasks built for XIAOMI", out.getvalue())
            self.assertIn("leaf_research_tasks.jsonl", out.getvalue())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "run-leaf-research",
                    "XIAOMI",
                    "--provider",
                    "mock",
                    "--limit",
                    "1",
                ])
            self.assertEqual(exit_code, 0)
            self.assertIn("Leaf research run for XIAOMI", out.getvalue())
            self.assertIn("leaf_research_results.jsonl", out.getvalue())
            self.assertTrue((stock_dir / "research_system" / "leaf_research_sources.jsonl").exists())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "synthesize-leaf-answers",
                    "XIAOMI",
                ])
            self.assertEqual(exit_code, 0)
            self.assertIn("Leaf answers synthesized for XIAOMI", out.getvalue())
            self.assertIn("leaf_answers.jsonl", out.getvalue())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "rollup-research-answers",
                    "XIAOMI",
                ])
            self.assertEqual(exit_code, 0)
            self.assertIn("Leaf research rollups written for XIAOMI", out.getvalue())
            self.assertIn("rollup_answers.jsonl", out.getvalue())

    def test_perplexity_leaf_research_cli_reports_missing_api_key(self):
        with project_tmp_dir() as tmp:
            stock_dir = Path(tmp) / "stocks" / "XIAOMI"
            stock_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
            (stock_dir / "evidence.jsonl").write_text(
                json.dumps({
                    "id": "ev_xiaomi_cli_foundation",
                    "research_object": "stocks/XIAOMI",
                    "source_type": "annual_report",
                    "source_name": "Xiaomi Annual Report",
                    "url": "https://example.com/xiaomi/annual",
                    "published_at": "2026-04-28T00:00:00Z",
                    "fetched_at": "2026-05-23T00:00:00+08:00",
                    "hash": "sha256:ev_xiaomi_cli_foundation",
                    "tickers": ["XIAOMI"],
                    "sectors": [],
                    "themes": [],
                    "summary": "Xiaomi disclosed revenue, gross margin, cash flow, smartphone shipments, IoT, internet services, and EV progress.",
                    "reliability": "primary",
                    "materiality": "high",
                    "used_in": [],
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            out = StringIO()
            err = StringIO()
            with patch.dict("os.environ", {}, clear=True):
                with redirect_stdout(out), redirect_stderr(err):
                    exit_code = main([
                        "--root",
                        str(tmp),
                        "run-leaf-research",
                        "XIAOMI",
                        "--provider",
                        "perplexity",
                        "--limit",
                        "1",
                    ])

            self.assertEqual(exit_code, 2)
            self.assertIn("PERPLEXITY_API_KEY", err.getvalue())

    def test_openai_compatible_leaf_research_cli_reports_missing_api_key(self):
        with project_tmp_dir() as tmp:
            stock_dir = Path(tmp) / "stocks" / "XIAOMI"
            stock_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
            (stock_dir / "evidence.jsonl").write_text(
                json.dumps({
                    "id": "ev_xiaomi_cli_foundation",
                    "research_object": "stocks/XIAOMI",
                    "source_type": "annual_report",
                    "source_name": "Xiaomi Annual Report",
                    "url": "https://example.com/xiaomi/annual",
                    "published_at": "2026-04-28T00:00:00Z",
                    "fetched_at": "2026-05-23T00:00:00+08:00",
                    "hash": "sha256:ev_xiaomi_cli_foundation",
                    "tickers": ["XIAOMI"],
                    "sectors": [],
                    "themes": [],
                    "summary": "Xiaomi disclosed revenue, gross margin, cash flow, smartphone shipments, IoT, internet services, and EV progress.",
                    "reliability": "primary",
                    "materiality": "high",
                    "used_in": [],
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            err = StringIO()
            with patch.dict("os.environ", {}, clear=True):
                with redirect_stderr(err):
                    exit_code = main([
                        "--root",
                        str(tmp),
                        "run-leaf-research",
                        "XIAOMI",
                        "--provider",
                        "openai_compatible",
                        "--limit",
                        "1",
                    ])

            self.assertEqual(exit_code, 2)
            self.assertIn("LEAF_RESEARCH_API_KEY", err.getvalue())

    def test_fetch_question_information_url_command_prints_paths(self):
        with project_tmp_dir() as tmp:
            stock_dir = Path(tmp) / "stocks" / "AAPL"
            stock_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
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
            html = "<html><head><title>Apple Segment Facts</title></head><body>公司材料补充分部利润池。</body></html>"

            out = StringIO()
            with patch(
                "value_invest_research.information_collection.urllib.request.urlopen",
                return_value=_FakeUrlResponse(html),
            ):
                with redirect_stdout(out):
                    exit_code = main([
                        "--root",
                        str(tmp),
                        "fetch-question-information-url",
                        "APPL",
                        "--node-id",
                        "current_business.profit-cash.segment-profit-pool",
                        "--category",
                        "evidence",
                        "--url",
                        "https://example.com/aapl/segment-facts",
                    ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Question information URL fetched", out.getvalue())
            self.assertIn("Apple Segment Facts", out.getvalue())
            self.assertIn("fetched_sources.jsonl", out.getvalue())

    def test_meta_qa_commands_print_paths(self):
        with project_tmp_dir() as tmp:
            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "build-meta-qa",
                    "--object-type",
                    "industry",
                    "--object-id",
                    "AI 眼镜",
                    "--meta-question",
                    "了解 AI 眼镜行业是否有长期投资价值",
                    "--project-id",
                    "ai_glasses",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA research built", out.getvalue())
            self.assertIn("question_plan.json", out.getvalue())
            self.assertIn("research_dashboard.html", out.getvalue())
            self.assertTrue((Path(tmp) / "research" / "qa_projects" / "ai_glasses" / "question_plan.json").exists())
            self.assertTrue((Path(tmp) / "research" / "qa_projects" / "ai_glasses" / "qa_tree.json").exists())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "plan-meta-qa",
                    "--object-type",
                    "industry",
                    "--object-id",
                    "AI 眼镜",
                    "--meta-question",
                    "了解 AI 眼镜行业是否有长期投资价值",
                    "--project-id",
                    "ai_glasses",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA question plan existing", out.getvalue())
            self.assertIn("question_plan.json", out.getvalue())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "add-meta-qa-question",
                    "--project-id",
                    "ai_glasses",
                    "--parent-id",
                    "l1.demand.market_size",
                    "--question",
                    "AI 眼镜出货是否能形成真实消费电子新品类？",
                    "--terminal",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA question created", out.getvalue())
            self.assertIn("terminal=True", out.getvalue())
            question_id = out.getvalue().split("question_id=", 1)[1].split(",", 1)[0]

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "record-meta-qa-information",
                    "--project-id",
                    "ai_glasses",
                    "--node-id",
                    question_id,
                    "--category",
                    "evidence",
                    "--source-type",
                    "regulator_notice",
                    "--source-name",
                    "AI Glasses Shipment Tracker",
                    "--url",
                    "https://example.com/ai-glasses",
                    "--summary",
                    "行业数据跟踪 AI 眼镜出货和用户留存。",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA information created", out.getvalue())
            self.assertIn("evidence=", out.getvalue())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "build-meta-qa-collection-tasks",
                    "--project-id",
                    "ai_glasses",
                    "--limit",
                    "2",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA collection tasks built", out.getvalue())
            self.assertIn("collection_tasks.jsonl", out.getvalue())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "run-meta-qa-collection-tasks",
                    "--project-id",
                    "ai_glasses",
                    "--limit",
                    "1",
                    "--min-score",
                    "0",
                    "--dry-run",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA collection tasks run", out.getvalue())
            self.assertIn("collection_results.jsonl", out.getvalue())

            import_path = Path(tmp) / "ai_glasses_collected.jsonl"
            import_path.write_text(
                json.dumps({
                    "node_id": question_id,
                    "category": "research_report",
                    "source_type": "sell_side_report",
                    "source_name": "AI Glasses Research Note",
                    "url": "https://example.com/ai-glasses-note",
                    "summary": "第三方报告讨论 AI 眼镜出货、留存和硬件利润池假设。",
                    "reliability": "high",
                    "materiality": "medium",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "import-meta-qa-information",
                    "--project-id",
                    "ai_glasses",
                    "--path",
                    str(import_path),
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA information imported", out.getvalue())
            self.assertIn("created=1", out.getvalue())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "build-meta-qa-synthesis-tasks",
                    "--project-id",
                    "ai_glasses",
                    "--limit",
                    "2",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA answer synthesis tasks built", out.getvalue())
            self.assertIn("synthesis_tasks.jsonl", out.getvalue())

            synthesis_path = Path(tmp) / "ai_glasses_synthesis.jsonl"
            synthesis_path.write_text(
                json.dumps({
                    "node_id": question_id,
                    "answer": "专业回答：AI 眼镜是否成立，关键看出货、留存和应用频次能否形成闭环。",
                    "judgment": "维持待验证判断。",
                    "gaps": ["缺少连续留存和复购数据。"],
                    "confidence": "low",
                    "rollup": "AI 眼镜新品类判断需要先验证用户留存闭环。",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "import-meta-qa-answer-synthesis",
                    "--project-id",
                    "ai_glasses",
                    "--path",
                    str(synthesis_path),
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA answer synthesis imported", out.getvalue())
            self.assertIn("synthesis_overrides.jsonl", out.getvalue())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "run-meta-qa-answer-synthesis",
                    "--project-id",
                    "ai_glasses",
                    "--limit",
                    "2",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA answer synthesis applied", out.getvalue())
            self.assertIn("mode=deterministic", out.getvalue())
            self.assertIn("synthesized_answers.jsonl", out.getvalue())

            client = _FakeLlmClient()
            out = StringIO()
            with patch("value_invest_research.cli._get_llm_client", return_value=client):
                with redirect_stdout(out):
                    exit_code = main([
                        "--root",
                        str(tmp),
                        "run-meta-qa-answer-synthesis",
                        "--project-id",
                        "ai_glasses",
                        "--limit",
                        "1",
                        "--use-llm",
                        "--api-key",
                        "test",
                    ])

            self.assertEqual(exit_code, 0)
            self.assertEqual(len(client.calls), 1)
            self.assertIn("Meta QA answer synthesis applied", out.getvalue())
            self.assertIn("mode=llm", out.getvalue())

            project_dir = Path(tmp) / "research" / "qa_projects" / "ai_glasses"
            task = [
                json.loads(line)
                for line in (project_dir / "collection_tasks.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ][0]
            search_results_path = Path(tmp) / "ai_glasses_search_results.jsonl"
            search_results_path.write_text(
                json.dumps({
                    "task_id": task["task_id"],
                    "title": "AI Glasses Research Report PDF",
                    "url": "https://research.example.com/ai-glasses/report.pdf",
                    "snippet": "Research report discusses AI glasses shipment and retention.",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "discover-meta-qa-source-candidates",
                    "--project-id",
                    "ai_glasses",
                    "--limit",
                    "1",
                    "--results-per-task",
                    "1",
                    "--search-results-path",
                    str(search_results_path),
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA source candidates discovered", out.getvalue())
            self.assertIn("source_candidates.jsonl", out.getvalue())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "apply-meta-qa-source-candidates",
                    "--project-id",
                    "ai_glasses",
                    "--path",
                    str(project_dir / "source_candidates.jsonl"),
                    "--dry-run",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA source candidates applied", out.getvalue())
            self.assertIn("dry-run", out.getvalue())

            queue_path = Path(tmp) / "ai_glasses_questions.jsonl"
            queue_path.write_text(
                json.dumps({
                    "parent_id": "l1.demand.market_size",
                    "question": "AI 眼镜用户留存是否足以支撑新品类判断？",
                    "terminal": True,
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "apply-meta-qa-question-queue",
                    "--project-id",
                    "ai_glasses",
                    "--path",
                    str(queue_path),
                    "--limit",
                    "5",
                    "--synthesize-answers",
                    "--write-professional-report",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA question queue applied", out.getvalue())
            self.assertIn("created=1", out.getvalue())
            self.assertIn("collection_tasks.jsonl", out.getvalue())
            self.assertIn("synthesis_mode=deterministic", out.getvalue())
            self.assertIn("professional_report.html", out.getvalue())
            self.assertTrue((project_dir / "professional_report.html").exists())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "validate-meta-qa-system",
                    "--project-id",
                    "ai_glasses",
                    "--require-professional-report",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA validation OK", out.getvalue())
            self.assertIn("professional_report.html", out.getvalue())

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "run-meta-qa-pipeline",
                    "--object-type",
                    "industry",
                    "--object-id",
                    "AI 眼镜",
                    "--meta-question",
                    "了解 AI 眼镜行业是否有长期投资价值",
                    "--project-id",
                    "ai_glasses",
                    "--task-limit",
                    "2",
                ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA pipeline completed", out.getvalue())
            self.assertIn("pipeline_run.json", out.getvalue())

            html = "<html><head><title>AI Glasses User Data</title></head><body>行业数据跟踪 AI 眼镜用户留存和复购。</body></html>"
            out = StringIO()
            with patch(
                "value_invest_research.information_collection.urllib.request.urlopen",
                return_value=_FakeUrlResponse(html),
            ):
                with redirect_stdout(out):
                    exit_code = main([
                        "--root",
                        str(tmp),
                        "fetch-meta-qa-information-url",
                        "--project-id",
                        "ai_glasses",
                        "--node-id",
                        question_id,
                        "--category",
                        "research_report",
                        "--url",
                        "https://example.com/ai-glasses/user-data",
                    ])

            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA information URL fetched", out.getvalue())
            self.assertIn("AI Glasses User Data", out.getvalue())
            self.assertIn("fetched_sources.jsonl", out.getvalue())

    def test_plan_meta_qa_command_can_use_llm(self):
        with project_tmp_dir() as tmp:
            client = _FakePlannerClient()
            out = StringIO()
            with patch("value_invest_research.cli._get_llm_client", return_value=client):
                with redirect_stdout(out):
                    exit_code = main([
                        "--root",
                        str(tmp),
                        "plan-meta-qa",
                        "--object-type",
                        "industry",
                        "--object-id",
                        "AI 眼镜",
                        "--meta-question",
                        "了解 AI 眼镜行业是否有长期投资价值",
                        "--project-id",
                        "ai_glasses_llm_plan",
                        "--use-llm",
                        "--api-key",
                        "test",
                    ])

            plan_path = Path(tmp) / "research" / "qa_projects" / "ai_glasses_llm_plan" / "question_plan.json"
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            self.assertEqual(exit_code, 0)
            self.assertEqual(len(client.calls), 1)
            self.assertIn("planning_mode=llm", out.getvalue())
            self.assertEqual(plan["planning_mode"], "llm")
            self.assertEqual(plan["l1"][0]["id"], "product_market_fit")

    def test_write_meta_qa_professional_report_command_prints_paths(self):
        with project_tmp_dir() as tmp:
            with redirect_stdout(StringIO()):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "build-meta-qa",
                    "--object-type",
                    "industry",
                    "--object-id",
                    "AI 眼镜",
                    "--meta-question",
                    "了解 AI 眼镜行业是否有长期投资价值",
                    "--project-id",
                    "ai_glasses",
                ])
            self.assertEqual(exit_code, 0)

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main([
                    "--root",
                    str(tmp),
                    "write-meta-qa-professional-report",
                    "--project-id",
                    "ai_glasses",
                ])

            report_path = Path(tmp) / "research" / "qa_projects" / "ai_glasses" / "professional_report.html"
            self.assertEqual(exit_code, 0)
            self.assertIn("Meta QA professional report written", out.getvalue())
            self.assertIn("professional_report.html", out.getvalue())
            self.assertTrue(report_path.exists())


if __name__ == "__main__":
    unittest.main()
