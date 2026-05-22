import json
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.helpers import project_tmp_dir
from value_invest_research.information_collection import (
    apply_meta_qa_source_candidates,
    build_meta_qa_collection_tasks,
    discover_meta_qa_source_candidates,
    fetch_meta_qa_information_url,
    import_meta_qa_information,
    run_meta_qa_collection_tasks,
)
from value_invest_research.answer_synthesis import (
    build_meta_qa_synthesis_tasks,
    import_meta_qa_answer_synthesis,
    run_meta_qa_answer_synthesis,
)
from value_invest_research.question_queue import apply_meta_qa_question_queue
from value_invest_research.qa_system_validation import validate_meta_qa_system
from value_invest_research.meta_qa_research import (
    add_meta_qa_question,
    build_meta_qa_research,
    plan_meta_qa_questions,
    record_meta_qa_information,
)


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class _FakeUrlResponse:
    def __init__(self, body: str, url: str = "https://example.com/meta/source", content_type: str = "text/html; charset=utf-8"):
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
                "answer": "LLM回答：机器人行业空间不能只看远期 TAM，必须先验证订单、交付、验收和毛利闭环。",
                "facts": ["LLM事实：任务提供了问题和 source_index。"],
                "inferences": ["LLM推论：订单质量决定收入确认和利润兑现。"],
                "judgment": "LLM判断：当前维持待验证判断。",
                "gaps": ["LLM缺口：缺少客户验收和分品类价格数据。"],
                "next_data": ["LLM下一步：补客户验收、订单转收入周期和 ASP。"],
                "confidence": "low",
                "source_balance": "LLM来源结构：按任务 source_index 复核。",
                "supporting_evidence": ["LLM支撑：引用任务中的高可靠来源。"],
                "refuting_evidence": ["LLM反证：若订单无法转化为验收，空间假设需要下修。"],
                "research_leads": ["LLM线索：跟踪行业数据库和公司公告。"],
                "rollup": "LLM上抛：行业空间判断必须先过订单到利润的闭环验证。",
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
                "planner_rationale": "LLM规划：先验证利润池，再验证需求质量和反证条件。",
                "detected_signals": ["smart_ev", "unit_economics"],
                "l1": [
                    {
                        "id": "unit_economics",
                        "question": "智能电动车行业的单车经济是否支持长期利润池？",
                        "rationale": "长期投资价值必须先证明毛利、售后成本和规模之间的关系。",
                        "should_drill_down": True,
                        "l2": [
                            {
                                "id": "margin_bridge",
                                "question": "单车收入、毛利和售后成本之间是否形成正向闭环？",
                                "rationale": "这是行业利润池是否真实的核心验证。",
                                "should_drill_down": True,
                                "l3": [
                                    {
                                        "id": "gross_margin_evidence",
                                        "question": "哪些公司公告和行业数据可以验证单车毛利是否可持续？",
                                        "rationale": "该问题已经可以进入资料搜集。",
                                        "should_drill_down": False,
                                        "should_collect_information": True,
                                        "terminal_reason": "已到达可直接搜集资料的粒度。",
                                        "information_focus": {
                                            "evidence": "车企财报、交付公告、监管公告和分部毛利披露。",
                                            "research_report": "商业研报对单车收入、单车毛利和产能利用率的拆分。",
                                            "message": "价格调整、交付等待周期和召回消息。",
                                            "opinion": "产业专家对价格战和售后成本的判断。",
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


class MetaQaResearchTests(unittest.TestCase):
    def test_build_meta_qa_research_creates_three_layer_project(self):
        with project_tmp_dir() as tmp:
            result = build_meta_qa_research(
                tmp,
                "industry",
                "中国智能电动车",
                "了解中国智能电动车行业的长期投资价值",
                project_id="china_smart_ev",
            )

            project_dir = Path(result["project_dir"])
            qa_tree = json.loads((project_dir / "qa_tree.json").read_text(encoding="utf-8"))
            question_plan = json.loads((project_dir / "question_plan.json").read_text(encoding="utf-8"))
            information_rows = _read_jsonl(project_dir / "information_collection.jsonl")
            dashboard = (project_dir / "research_dashboard.html").read_text(encoding="utf-8")
            report = (project_dir / "research_report.html").read_text(encoding="utf-8")

            self.assertEqual(result["project_id"], "china_smart_ev")
            self.assertTrue(result["question_plan_path"].endswith("question_plan.json"))
            self.assertEqual(qa_tree["meta_question"], "了解中国智能电动车行业的长期投资价值")
            self.assertEqual(qa_tree["default_depth"], 3)
            self.assertEqual(question_plan["planning_mode"], "deterministic_rule_based")
            self.assertIn("smart_ev", question_plan["detected_signals"])
            self.assertIn("中国智能电动车竞争会不会演化为价格战", json.dumps(question_plan, ensure_ascii=False))
            self.assertIn("question_plan", qa_tree)
            self.assertIn("meta.root", {node["id"] for node in qa_tree["nodes"]})
            self.assertTrue(any(node["level"] == 1 for node in qa_tree["nodes"]))
            self.assertTrue(any(node["level"] == 2 for node in qa_tree["nodes"]))
            self.assertTrue(any(node["level"] == 3 for node in qa_tree["nodes"]))
            first_leaf = next(node for node in qa_tree["nodes"] if node["level"] == 3)
            self.assertTrue(first_leaf["metadata"]["should_collect_information"])
            self.assertIn("information_focus", first_leaf["metadata"])
            self.assertIn("professional_answer", first_leaf)
            self.assertIn("supporting_evidence", first_leaf["professional_answer"])
            self.assertGreater(len(information_rows), 0)
            self.assertEqual({"evidence", "research_report", "message", "opinion"}, {row["category"] for row in information_rows[:4]})
            self.assertIn("层级 QA 研究系统", dashboard)
            self.assertIn("问题规划", dashboard)
            self.assertIn("系统为什么这样下钻", dashboard)
            self.assertIn("系统扩展出的 L1 问题", dashboard)
            self.assertIn("data-parent-id=\"meta.root\"", dashboard)
            self.assertIn("apply-meta-qa-question-queue", dashboard)
            self.assertIn("队列 JSONL", dashboard)
            self.assertIn("专业研究报告", report)
            self.assertIn("从元问题到子问题的拆解依据", report)
            self.assertIn("最需要优先验证的问题", report)

    def test_plan_meta_qa_questions_writes_auditable_plan(self):
        with project_tmp_dir() as tmp:
            result = plan_meta_qa_questions(
                tmp,
                "event",
                "关税上调",
                "分析关税上调对消费电子产业链的影响",
                project_id="tariff_event",
            )

            project_dir = Path(result["project_dir"])
            plan = json.loads((project_dir / "question_plan.json").read_text(encoding="utf-8"))

            self.assertTrue(result["created"])
            self.assertEqual(result["l1_questions"], 4)
            self.assertGreater(result["leaf_questions"], 0)
            self.assertIn("policy", plan["detected_signals"])
            self.assertIn("关税上调的事实边界、时间线和未确认点是什么？", json.dumps(plan, ensure_ascii=False))

    def test_build_meta_qa_research_can_use_llm_question_plan(self):
        with project_tmp_dir() as tmp:
            client = _FakePlannerClient()

            result = build_meta_qa_research(
                tmp,
                "industry",
                "中国智能电动车",
                "了解中国智能电动车行业的长期投资价值",
                project_id="smart_ev_llm_plan",
                planner_client=client,
            )

            project_dir = Path(result["project_dir"])
            plan = json.loads((project_dir / "question_plan.json").read_text(encoding="utf-8"))
            qa_tree = json.loads((project_dir / "qa_tree.json").read_text(encoding="utf-8"))
            information_rows = _read_jsonl(project_dir / "information_collection.jsonl")
            report = (project_dir / "research_report.html").read_text(encoding="utf-8")

            self.assertEqual(result["planning_mode"], "llm")
            self.assertEqual(len(client.calls), 1)
            self.assertEqual(plan["planning_mode"], "llm")
            self.assertIn("unit_economics", {node["id"] for node in plan["l1"]})
            self.assertIn("l1.unit_economics.margin_bridge.gross_margin_evidence", {node["id"] for node in qa_tree["nodes"]})
            self.assertTrue(
                any(
                    row["node_id"] == "l1.unit_economics.margin_bridge.gross_margin_evidence"
                    and row["category"] == "evidence"
                    for row in information_rows
                )
            )
            self.assertIn("单车经济是否支持长期利润池", report)

    def test_add_question_and_record_information_update_report(self):
        with project_tmp_dir() as tmp:
            build_meta_qa_research(
                tmp,
                "event",
                "关税上调",
                "分析关税上调对消费电子产业链的影响",
                project_id="tariff_event",
            )

            question = add_meta_qa_question(
                tmp,
                "tariff_event",
                "l1.transmission.channels",
                "关税上调是否会改变终端品牌的定价权？",
            )
            result = record_meta_qa_information(
                tmp,
                "tariff_event",
                question["question_id"],
                "evidence",
                "regulator_notice",
                "Tariff Official Notice",
                "https://example.com/tariff/notice",
                "官方公告确认部分消费电子品类关税上调，可能影响品牌定价和渠道补贴。",
                reliability="primary",
                materiality="high",
            )

            project_dir = Path(result["project_dir"])
            evidence_rows = _read_jsonl(project_dir / "evidence.jsonl")
            qa_tree = json.loads((project_dir / "qa_tree.json").read_text(encoding="utf-8"))
            information_rows = _read_jsonl(project_dir / "information_collection.jsonl")
            report = (project_dir / "research_report.html").read_text(encoding="utf-8")

            self.assertTrue(question["created"])
            self.assertTrue(result["created"])
            self.assertTrue(question["question_id"].startswith("l1.transmission.channels.custom_"))
            evidence_row = next(row for row in evidence_rows if row["id"] == result["evidence_id"])
            self.assertIn(f"meta_qa:tariff_event:{question['question_id']}", evidence_row["used_in"])
            custom_node = next(node for node in qa_tree["nodes"] if node["id"] == question["question_id"])
            self.assertTrue(any(item["evidence_id"] == result["evidence_id"] for item in custom_node["evidence_buckets"]["evidence"]))
            self.assertIn("professional_answer", custom_node)
            self.assertIn("当前对", custom_node["professional_answer"]["answer"])
            self.assertTrue(
                any("Tariff Official Notice" in item for item in custom_node["professional_answer"]["supporting_evidence"])
            )
            self.assertTrue(
                any(
                    row["node_id"] == question["question_id"]
                    and row["category"] == "evidence"
                    and row["status"] == "matched"
                    for row in information_rows
                )
            )
            self.assertIn("关税上调是否会改变终端品牌的定价权？", report)
            self.assertIn("Tariff Official Notice", report)
            self.assertIn("专业回答", report)
            self.assertIn("支撑信息", report)
            self.assertIn("下一步数据", report)

    def test_meta_qa_collection_tasks_and_batch_import(self):
        with project_tmp_dir() as tmp:
            build_meta_qa_research(
                tmp,
                "industry",
                "机器人",
                "分析人形机器人产业链的投资价值",
                project_id="robotics_chain",
            )

            tasks_result = build_meta_qa_collection_tasks(tmp, "robotics_chain", limit=4)
            project_dir = Path(tasks_result["project_dir"])
            tasks = _read_jsonl(project_dir / "collection_tasks.jsonl")

            self.assertEqual(tasks_result["tasks"], 4)
            self.assertEqual(len(tasks), 4)
            self.assertIn("value-invest-research record-meta-qa-information", tasks[0]["bind_command"])
            self.assertIn("acceptance_criteria", tasks[0])

            import_path = tmp / "robotics_sources.jsonl"
            source_row = {
                "node_id": tasks[0]["node_id"],
                "category": tasks[0]["category"],
                "source_type": "industry_data",
                "source_name": "Robot Industry Tracker",
                "url": "https://example.com/robotics/tracker",
                "summary": "第三方行业数据跟踪人形机器人出货、价格和供应链验证进展。",
                "reliability": tasks[0]["default_reliability"],
                "materiality": tasks[0]["default_materiality"],
            }
            import_path.write_text(json.dumps(source_row, ensure_ascii=False) + "\n", encoding="utf-8")

            import_result = import_meta_qa_information(tmp, "robotics_chain", import_path)

            qa_tree = json.loads((project_dir / "qa_tree.json").read_text(encoding="utf-8"))
            imported_node = next(node for node in qa_tree["nodes"] if node["id"] == tasks[0]["node_id"])
            self.assertEqual(import_result["records"], 1)
            self.assertEqual(import_result["created"], 1)
            self.assertTrue(
                any(
                    item.get("source_name") == "Robot Industry Tracker"
                    for item in imported_node["evidence_buckets"][tasks[0]["category"]]
                )
            )
            report = (project_dir / "research_report.html").read_text(encoding="utf-8")
            self.assertIn("Robot Industry Tracker", report)

    def test_run_meta_qa_collection_tasks_binds_local_project_evidence(self):
        with project_tmp_dir() as tmp:
            build_meta_qa_research(
                tmp,
                "industry",
                "机器人",
                "分析人形机器人产业链的投资价值",
                project_id="robotics_chain",
            )
            project_dir = Path(tmp) / "research" / "qa_projects" / "robotics_chain"
            record = {
                "id": "ev_robotics_market_size",
                "research_object": "research/qa_projects/robotics_chain",
                "source_type": "industry_data",
                "source_name": "Robot Market Size Dataset",
                "url": "https://example.com/robotics/market-size",
                "published_at": "2026-05-01T00:00:00Z",
                "fetched_at": "2026-05-20T00:00:00+08:00",
                "hash": "sha256:robotics_market_size",
                "tickers": [],
                "sectors": ["机器人"],
                "themes": ["meta_qa", "industry", "evidence"],
                "summary": "机器人行业空间来自真实需求、渗透率、价格和周期，需要用出货、订单和客户验证。",
                "reliability": "high",
                "materiality": "high",
                "information_category": "evidence",
                "used_in": [],
            }
            with (project_dir / "evidence.jsonl").open("a", encoding="utf-8", newline="\n") as file:
                file.write(json.dumps(record, ensure_ascii=False) + "\n")

            result = run_meta_qa_collection_tasks(tmp, "robotics_chain", min_score=8)

            evidence_rows = _read_jsonl(project_dir / "evidence.jsonl")
            matched = next(row for row in evidence_rows if row["id"] == "ev_robotics_market_size")
            self.assertGreater(result["matches"], 0)
            self.assertTrue(any(link.startswith("meta_qa:robotics_chain:") for link in matched["used_in"]))
            report = (project_dir / "research_report.html").read_text(encoding="utf-8")
            self.assertIn("Robot Market Size Dataset", report)

    def test_meta_qa_source_candidate_discovery_and_apply(self):
        with project_tmp_dir() as tmp:
            build_meta_qa_research(
                tmp,
                "industry",
                "机器人",
                "分析人形机器人产业链的投资价值",
                project_id="robotics_chain",
            )
            tasks_result = build_meta_qa_collection_tasks(tmp, "robotics_chain", limit=1)
            project_dir = Path(tasks_result["project_dir"])
            task = _read_jsonl(project_dir / "collection_tasks.jsonl")[0]
            search_results_path = tmp / "robotics_search_results.jsonl"
            search_results_path.write_text(
                json.dumps({
                    "task_id": task["task_id"],
                    "title": "Robot Industry Research Report PDF",
                    "url": "https://research.example.com/robotics/report.pdf",
                    "snippet": "Research report discusses robot shipments, pricing and customer validation.",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            discover_result = discover_meta_qa_source_candidates(
                tmp,
                "robotics_chain",
                limit=1,
                results_per_task=1,
                min_score=0,
                search_results_path=search_results_path,
            )
            candidates = _read_jsonl(project_dir / "source_candidates.jsonl")

            self.assertEqual(discover_result["candidates"], 1)
            self.assertTrue(candidates[0]["accepted"])
            self.assertIn("fetch-meta-qa-information-url", candidates[0]["fetch_command"])

            html = "<html><head><title>Robot Industry Research Report PDF</title></head><body>研报讨论机器人出货、价格和客户验证。</body></html>"
            with patch(
                "value_invest_research.information_collection.urllib.request.urlopen",
                return_value=_FakeUrlResponse(html, url="https://research.example.com/robotics/report.pdf"),
            ):
                apply_result = apply_meta_qa_source_candidates(
                    tmp,
                    "robotics_chain",
                    Path(discover_result["candidate_path"]),
                    min_score=0,
                )

            evidence_rows = _read_jsonl(project_dir / "evidence.jsonl")
            report = (project_dir / "research_report.html").read_text(encoding="utf-8")
            self.assertEqual(apply_result["applied"], 1)
            self.assertTrue(any(row["source_name"] == "Robot Industry Research Report PDF" for row in evidence_rows))
            self.assertIn("Robot Industry Research Report PDF", report)

    def test_fetch_meta_qa_information_url_binds_extracted_source(self):
        with project_tmp_dir() as tmp:
            build_meta_qa_research(
                tmp,
                "industry",
                "机器人",
                "分析人形机器人产业链的投资价值",
                project_id="robotics_chain",
            )
            question = add_meta_qa_question(
                tmp,
                "robotics_chain",
                "l1.demand.market_size",
                "人形机器人真实订单是否足以支撑行业空间？",
            )
            html = """
            <html>
              <head><title>Robot Orders Tracker</title></head>
              <body>行业跟踪数据讨论人形机器人订单、出货和客户验收节奏。</body>
            </html>
            """
            with patch(
                "value_invest_research.information_collection.urllib.request.urlopen",
                return_value=_FakeUrlResponse(html),
            ):
                result = fetch_meta_qa_information_url(
                    tmp,
                    "robotics_chain",
                    question["question_id"],
                    "research_report",
                    "https://example.com/robotics/orders",
                )

            project_dir = Path(result["project_dir"])
            evidence_rows = _read_jsonl(project_dir / "evidence.jsonl")
            fetched_rows = _read_jsonl(project_dir / "fetched_sources.jsonl")
            report = (project_dir / "research_report.html").read_text(encoding="utf-8")

            self.assertTrue(result["created"])
            self.assertEqual(result["source_name"], "Robot Orders Tracker")
            self.assertIn("人形机器人订单", result["summary"])
            self.assertTrue(any(row["id"] == result["evidence_id"] for row in evidence_rows))
            self.assertEqual(fetched_rows[-1]["evidence_id"], result["evidence_id"])
            self.assertIn("Robot Orders Tracker", report)

    def test_apply_meta_qa_question_queue_refreshes_tasks(self):
        with project_tmp_dir() as tmp:
            build_meta_qa_research(
                tmp,
                "industry",
                "机器人",
                "分析人形机器人产业链的投资价值",
                project_id="robotics_chain",
            )
            queue_path = tmp / "meta_queued_questions.jsonl"
            queue_path.write_text(
                json.dumps({
                    "parent_id": "l1.demand.market_size",
                    "question": "机器人客户验收节奏是否足以支撑收入确认？",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            result = apply_meta_qa_question_queue(
                tmp,
                "robotics_chain",
                queue_path,
                synthesize_answers=True,
                write_professional_report=True,
            )

            project_dir = Path(result["dashboard_path"]).parent
            custom_rows = _read_jsonl(project_dir / "custom_questions.jsonl")
            tasks = _read_jsonl(project_dir / "collection_tasks.jsonl")
            report = (project_dir / "research_report.html").read_text(encoding="utf-8")

            self.assertEqual(result["records"], 1)
            self.assertEqual(result["created"], 1)
            self.assertGreater(result["tasks"], 0)
            self.assertGreater(result["synthesized_answers"], 0)
            self.assertTrue(result["professional_report_path"].endswith("professional_report.html"))
            self.assertTrue((project_dir / "synthesized_answers.jsonl").exists())
            self.assertTrue((project_dir / "professional_report.html").exists())
            validation = validate_meta_qa_system(tmp, "robotics_chain", require_professional_report=True)
            self.assertTrue(validation["ok"], validation["issues"])
            self.assertGreater(validation["summary"]["leaf_questions"], 0)
            self.assertTrue(any(row["question"] == "机器人客户验收节奏是否足以支撑收入确认？" for row in custom_rows))
            self.assertTrue(any("机器人客户验收节奏" in task["question"] for task in tasks))
            self.assertIn("机器人客户验收节奏是否足以支撑收入确认？", report)

    def test_add_top_level_meta_question_auto_drills_to_leaf_collection(self):
        with project_tmp_dir() as tmp:
            build_meta_qa_research(
                tmp,
                "industry",
                "机器人",
                "分析人形机器人产业链的投资价值",
                project_id="robotics_chain",
            )

            result = add_meta_qa_question(
                tmp,
                "robotics_chain",
                "meta.root",
                "机器人行业长期价值的核心矛盾是什么？",
            )

            project_dir = Path(result["project_dir"])
            qa_tree = json.loads((project_dir / "qa_tree.json").read_text(encoding="utf-8"))
            information_rows = _read_jsonl(project_dir / "information_collection.jsonl")
            custom_node = next(node for node in qa_tree["nodes"] if node["id"] == result["question_id"])
            child_nodes = [node for node in qa_tree["nodes"] if node.get("parent_id") == result["question_id"]]
            leaf_nodes = [
                node
                for node in qa_tree["nodes"]
                if node["id"].startswith(f"{result['question_id']}.")
                and int(node.get("level", 0)) == qa_tree["default_depth"]
            ]

            self.assertTrue(result["created"])
            self.assertEqual(custom_node["level"], 1)
            self.assertGreaterEqual(len(child_nodes), 2)
            self.assertGreaterEqual(len(leaf_nodes), 4)
            self.assertTrue(all(node["status"] == "auto_drilldown" for node in child_nodes))
            for leaf in leaf_nodes:
                self.assertEqual(
                    {"evidence", "research_report", "message", "opinion"},
                    {row["category"] for row in information_rows if row["node_id"] == leaf["id"]},
                )

    def test_add_terminal_meta_question_collects_information_without_drilldown(self):
        with project_tmp_dir() as tmp:
            build_meta_qa_research(
                tmp,
                "industry",
                "机器人",
                "分析人形机器人产业链的投资价值",
                project_id="robotics_chain",
            )

            result = add_meta_qa_question(
                tmp,
                "robotics_chain",
                "meta.root",
                "机器人行业是否已经有可回答的单一关键矛盾？",
                terminal=True,
            )

            project_dir = Path(result["project_dir"])
            qa_tree = json.loads((project_dir / "qa_tree.json").read_text(encoding="utf-8"))
            information_rows = _read_jsonl(project_dir / "information_collection.jsonl")
            custom_node = next(node for node in qa_tree["nodes"] if node["id"] == result["question_id"])

            self.assertTrue(result["created"])
            self.assertEqual(custom_node["level"], 1)
            self.assertEqual(custom_node["next_question_ids"], [])
            self.assertTrue(custom_node["metadata"]["should_collect_information"])
            self.assertFalse(custom_node["metadata"]["should_drill_down"])
            self.assertEqual(
                {"evidence", "research_report", "message", "opinion"},
                {row["category"] for row in information_rows if row["node_id"] == result["question_id"]},
            )
            validation = validate_meta_qa_system(tmp, "robotics_chain")
            self.assertTrue(validation["ok"], validation["issues"])

    def test_meta_qa_answer_synthesis_tasks_and_import_override(self):
        with project_tmp_dir() as tmp:
            build_meta_qa_research(
                tmp,
                "industry",
                "机器人",
                "分析人形机器人产业链的投资价值",
                project_id="robotics_chain",
            )

            tasks_result = build_meta_qa_synthesis_tasks(tmp, "robotics_chain", limit=2)
            project_dir = Path(tasks_result["project_dir"])
            tasks = _read_jsonl(project_dir / "synthesis_tasks.jsonl")
            target_node = tasks[0]["node_id"]

            self.assertEqual(tasks_result["synthesis_tasks"], 2)
            self.assertIn("source_index", tasks[0])
            self.assertIn("import-meta-qa-answer-synthesis", tasks[0]["import_command"])

            import_path = tmp / "robotics_synthesis.jsonl"
            import_path.write_text(
                json.dumps({
                    "node_id": target_node,
                    "answer": "专业回答：机器人产业链的当前关键不是讲空间，而是证明订单、交付、验收和毛利之间已经形成闭环。",
                    "facts": ["当前任务缺少足够一手订单与验收数据。"],
                    "inferences": ["若订单无法转化为验收和收入确认，市场空间假设需要下修。"],
                    "judgment": "维持待验证判断，优先补订单质量和收入确认证据。",
                    "gaps": ["缺少客户验收、交付周期和分品类价格数据。"],
                    "next_data": ["客户验收公告、订单转收入周期、分品类 ASP。"],
                    "confidence": "low",
                    "source_balance": "证据 0 / 研报 0 / 消息 0 / 观点 0。",
                    "research_leads": ["先找行业数据库与公司公告交叉验证。"],
                    "rollup": "机器人行业空间判断必须先通过订单到收入的闭环验证。",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            result = import_meta_qa_answer_synthesis(tmp, "robotics_chain", import_path)
            qa_tree = json.loads((project_dir / "qa_tree.json").read_text(encoding="utf-8"))
            node = next(node for node in qa_tree["nodes"] if node["id"] == target_node)
            report = (project_dir / "research_report.html").read_text(encoding="utf-8")

            self.assertEqual(result["records"], 1)
            self.assertEqual(result["applied_nodes"], 1)
            self.assertIn("专业回答：机器人产业链", node["current_answer"])
            self.assertEqual(node["professional_answer"]["confidence"], "low")
            self.assertIn("synthesis_override", node["metadata"])
            self.assertIn("订单到收入的闭环验证", report)

    def test_run_meta_qa_answer_synthesis_generates_and_applies_answers(self):
        with project_tmp_dir() as tmp:
            build_meta_qa_research(
                tmp,
                "industry",
                "机器人",
                "分析人形机器人产业链的投资价值",
                project_id="robotics_chain",
            )

            result = run_meta_qa_answer_synthesis(tmp, "robotics_chain", limit=2)
            project_dir = Path(result["project_dir"])
            answers = _read_jsonl(project_dir / "synthesized_answers.jsonl")
            qa_tree = json.loads((project_dir / "qa_tree.json").read_text(encoding="utf-8"))
            first_node = next(node for node in qa_tree["nodes"] if node["id"] == answers[0]["node_id"])
            report = (project_dir / "research_report.html").read_text(encoding="utf-8")

            self.assertTrue(result["applied"])
            self.assertEqual(result["synthesized_answers"], 2)
            self.assertEqual(result["applied_nodes"], 2)
            self.assertIn("专业回答：围绕", answers[0]["answer"])
            self.assertEqual(first_node["metadata"]["synthesis_override"]["source"], "deterministic_batch_synthesis")
            self.assertIn("专业回答：围绕", report)

    def test_run_meta_qa_answer_synthesis_can_use_llm_client(self):
        with project_tmp_dir() as tmp:
            build_meta_qa_research(
                tmp,
                "industry",
                "机器人",
                "分析人形机器人产业链的投资价值",
                project_id="robotics_chain",
            )
            client = _FakeLlmClient()

            result = run_meta_qa_answer_synthesis(tmp, "robotics_chain", limit=1, client=client)
            project_dir = Path(result["project_dir"])
            answers = _read_jsonl(project_dir / "synthesized_answers.jsonl")
            qa_tree = json.loads((project_dir / "qa_tree.json").read_text(encoding="utf-8"))
            node = next(node for node in qa_tree["nodes"] if node["id"] == answers[0]["node_id"])
            report = (project_dir / "research_report.html").read_text(encoding="utf-8")

            self.assertEqual(result["synthesis_mode"], "llm")
            self.assertEqual(len(client.calls), 1)
            self.assertEqual(answers[0]["synthesis_source"], "llm")
            self.assertIn("LLM回答：机器人", answers[0]["answer"])
            self.assertEqual(node["metadata"]["synthesis_override"]["source"], "llm")
            self.assertIn("LLM上抛", report)


if __name__ == "__main__":
    unittest.main()
