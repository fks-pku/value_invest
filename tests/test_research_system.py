import json
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.helpers import project_tmp_dir
from value_invest_research.information_collection import (
    apply_research_source_candidates,
    build_research_collection_tasks,
    discover_research_source_candidates,
    fetch_question_information_url,
    import_question_information,
    run_research_collection_tasks,
)
from value_invest_research.answer_synthesis import (
    build_stock_synthesis_tasks,
    import_stock_answer_synthesis,
    run_stock_answer_synthesis,
)
from value_invest_research.question_queue import apply_research_question_queue
from value_invest_research.qa_system_validation import validate_stock_qa_system
from value_invest_research.research_system import (
    add_research_question,
    build_research_system,
    record_question_information,
)
from value_invest_research.scaffold import init_stock


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class _FakeUrlResponse:
    def __init__(self, body: str, url: str = "https://example.com/xiaomi/source", content_type: str = "text/html; charset=utf-8"):
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
                "answer": "LLM回答：小米的关键是验证用户、渠道和供应链能力能否继续迁移到汽车等高客单价硬件。",
                "facts": ["LLM事实：现有任务已提供公司披露和研究索引。"],
                "inferences": ["LLM推论：能力迁移需要用利润池和现金流数据验证。"],
                "judgment": "LLM判断：当前是中等置信度的能力迁移假设。",
                "gaps": ["LLM缺口：缺少连续单车经济和售后成本。"],
                "next_data": ["LLM下一步：补充单车收入、单车毛利和召回成本。"],
                "confidence": "medium",
                "source_balance": "LLM来源结构：以现有 source_index 为准。",
                "supporting_evidence": ["LLM支撑：引用任务中的 evidence_id。"],
                "refuting_evidence": ["LLM反证：价格战和召回成本可能削弱判断。"],
                "research_leads": ["LLM线索：跟踪季度交付和监管公告。"],
                "rollup": "LLM上抛：小米能力迁移可成立，但汽车利润池仍需验证。",
            },
            ensure_ascii=False,
        )


def _evidence_record(record_id: str, source_type: str, source_name: str, summary: str, reliability: str = "primary", materiality: str = "high") -> dict:
    return {
        "id": record_id,
        "research_object": "stocks/XIAOMI",
        "source_type": source_type,
        "source_name": source_name,
        "url": "https://example.com/source",
        "published_at": "2026-04-28T00:00:00Z",
        "fetched_at": "2026-05-20T00:00:00+08:00",
        "hash": f"sha256:{record_id}",
        "tickers": ["XIAOMI"],
        "sectors": [],
        "themes": [],
        "summary": summary,
        "reliability": reliability,
        "materiality": materiality,
        "used_in": [],
    }


class ResearchSystemTests(unittest.TestCase):
    def _seed_xiaomi(self, root: Path) -> Path:
        stock_dir = init_stock(root, "XIAOMI", "Xiaomi Corporation")
        records = [
            _evidence_record(
                "ev_xiaomi_profile",
                "company_ir",
                "Xiaomi Company Profile",
                "Xiaomi was founded in April 2010, listed in Hong Kong in 2018, and describes itself as a consumer electronics and smart manufacturing company.",
            ),
            _evidence_record(
                "ev_xiaomi_annual",
                "annual_report",
                "Xiaomi 2025 Annual Report",
                "FY2025 revenue was RMB457.3B, gross profit was RMB101.8B, adjusted net profit was RMB39.2B, operating cash flow was RMB34.1B, and capex was RMB18.2B.",
            ),
            _evidence_record(
                "ev_xiaomi_global_ir_triathlon_20180503",
                "company_ir",
                "Xiaomi Global IR Prospectus Overview",
                "Xiaomi disclosed the triathlon model of hardware, new retail, and internet services; MIUI MAU was about 190M in March 2018 and Mi Fans contributed product feedback.",
            ),
            _evidence_record(
                "ev_xiaomi_wipo_origin_miui_20211101",
                "industry_data",
                "WIPO Xiaomi IP Advantage Case",
                "WIPO describes Xiaomi as founded in April 2010 and launching the first private beta of MIUI in August 2010.",
                reliability="high",
            ),
            _evidence_record(
                "ev_xiaomi_hardware_margin_pledge_2021_ar",
                "annual_report",
                "Xiaomi 2021 Annual Report Hardware Margin Pledge",
                "Xiaomi pledged that hardware business net margin, including smartphones and IoT/lifestyle products, would not exceed 5.0% per year.",
            ),
            _evidence_record(
                "ev_xiaomi_segments",
                "results_announcement",
                "Xiaomi 2025 Results",
                "Smartphone shipments were 165.2M units, connected IoT devices were 1,079.2M, internet services gross margin was 76.5%, and Smart EV deliveries were 411,082 vehicles.",
            ),
            _evidence_record(
                "ev_xiaomi_smartphone_share",
                "industry_data",
                "IDC Q1 2026 Smartphone Market",
                "IDC Q1 2026 data shows Xiaomi smartphone shipments were 33.8M units, share was 11.5%, and shipments declined 19.1% YoY amid memory constraints.",
                reliability="high",
            ),
            _evidence_record(
                "ev_xiaomi_governance",
                "annual_report",
                "Xiaomi WVR Disclosure",
                "Lei Jun held about 61.0% voting rights through weighted voting rights, with governance and control risk for minority shareholders.",
            ),
            _evidence_record(
                "ev_xiaomi_recall",
                "regulator_notice",
                "SAMR SU7 Recall",
                "Xiaomi Auto recalled 116,887 SU7 vehicles because assisted driving could be insufficient in recognizing or handling extreme safety scenarios.",
            ),
        ]
        with (stock_dir / "evidence.jsonl").open("w", encoding="utf-8", newline="\n") as file:
            for record in records:
                file.write(json.dumps(record) + "\n")
        return stock_dir

    def test_build_research_system_writes_operating_system_artifacts(self):
        with project_tmp_dir() as tmp:
            stock_dir = self._seed_xiaomi(tmp)

            result = build_research_system(tmp, "XIAOMI")

            research_dir = stock_dir / "research_system"
            foundation = json.loads((research_dir / "foundation_graph.json").read_text(encoding="utf-8"))
            qa_tree = json.loads((research_dir / "qa_tree.json").read_text(encoding="utf-8"))
            information_rows = _read_jsonl(research_dir / "information_collection.jsonl")
            questions = _read_jsonl(research_dir / "question_graph.jsonl")
            messages = _read_jsonl(research_dir / "message_flow.jsonl")
            dashboard = (research_dir / "research_dashboard.html").read_text(encoding="utf-8")
            report = (research_dir / "research_report.html").read_text(encoding="utf-8")
            source_origin_page = (research_dir / "pages" / "source_origin.html").read_text(encoding="utf-8")
            history_page = (research_dir / "pages" / "history.html").read_text(encoding="utf-8")
            current_business_page = (research_dir / "pages" / "current_business.html").read_text(encoding="utf-8")
            source_origin_l2_page = (research_dir / "pages" / "source_origin" / "source_origin_q1_era.html").read_text(encoding="utf-8")
            history_l2_page = (research_dir / "pages" / "history" / "history_h4_ev_transition.html").read_text(encoding="utf-8")
            current_business_l2_page = (research_dir / "pages" / "current_business" / "current_business_profit_cash.html").read_text(encoding="utf-8")
            current_business_l3_page = (
                research_dir
                / "pages"
                / "current_business"
                / "l3"
                / "current_business_profit_cash_segment_profit_pool.html"
            ).read_text(encoding="utf-8")

            self.assertEqual(result["ticker"], "XIAOMI")
            self.assertTrue(result["dashboard_path"].endswith("research_dashboard.html"))
            self.assertTrue(result["qa_tree_path"].endswith("qa_tree.json"))
            self.assertTrue(result["information_collection_path"].endswith("information_collection.jsonl"))
            self.assertTrue(result["report_path"].endswith("research_report.html"))
            self.assertTrue((research_dir / "information_collection.jsonl").exists())
            self.assertTrue((research_dir / "research_report.html").exists())
            self.assertTrue((research_dir / "pages" / "source_origin.html").exists())
            self.assertTrue((research_dir / "pages" / "history.html").exists())
            self.assertTrue((research_dir / "pages" / "current_business.html").exists())
            self.assertTrue((research_dir / "pages" / "source_origin" / "source_origin_q1_era.html").exists())
            self.assertTrue((research_dir / "pages" / "history" / "history_h4_ev_transition.html").exists())
            self.assertTrue((research_dir / "pages" / "current_business" / "l3" / "current_business_profit_cash_segment_profit_pool.html").exists())
            self.assertIn(foundation["foundation_status"], {"complete", "research_ready_with_specific_gaps"})
            self.assertEqual(len(foundation["sections"]), 8)
            source_origin = next(section for section in foundation["sections"] if section["id"] == "source_origin")
            self.assertGreater(len(source_origin["key_questions"]), 0)
            self.assertIn("evidence", source_origin["information_by_category"])
            self.assertIn("research_report", source_origin["information_by_category"])
            self.assertIn("smart_ev", {node["id"] for node in foundation["business_nodes"]})
            self.assertIn("smartphone", {node["id"] for node in foundation["business_nodes"]})
            self.assertGreater(len(foundation["assumptions"]), 0)
            self.assertGreater(len(foundation["kpis"]), 0)
            self.assertEqual(qa_tree["default_depth"], 3)
            self.assertIn("foundation.history", {node["id"] for node in qa_tree["nodes"]})
            self.assertIn("history.h4-ev-transition.unit-economics", {node["id"] for node in qa_tree["nodes"]})
            self.assertIn("foundation.current_business", {node["id"] for node in qa_tree["nodes"]})
            self.assertIn("current_business.profit-cash.segment-profit-pool", {node["id"] for node in qa_tree["nodes"]})
            self.assertIn("source_origin.q1-era.primary-proof", {node["id"] for node in qa_tree["nodes"]})
            self.assertGreater(len(information_rows), 0)
            self.assertIn("category", information_rows[0])
            self.assertIn("search_query", information_rows[0])
            self.assertIn("next_action", information_rows[0])
            ev_node = next(node for node in qa_tree["nodes"] if node["id"] == "history.h4-ev-transition")
            self.assertEqual(ev_node["level"], 2)
            self.assertIn("history.h4-ev-transition.unit-economics", ev_node["next_question_ids"])
            history_l3_node = next(node for node in qa_tree["nodes"] if node["id"] == "history.h1-model-shift.profit-pool")
            self.assertIn("professional_answer", history_l3_node)
            self.assertIn("supporting_evidence", history_l3_node["professional_answer"])
            self.assertIn("当前回答", history_l3_node["professional_answer"]["answer"])
            self.assertEqual(questions, [])
            self.assertEqual(messages, [])
            self.assertIn("公司基础画像", dashboard)
            self.assertIn("L0 / 公司基础框架", dashboard)
            self.assertIn("当前要研究的问题", dashboard)
            self.assertIn("L1 子问题", dashboard)
            self.assertIn("子结构汇总结论", dashboard)
            self.assertIn("子问题列表", dashboard)
            self.assertIn("高优先级缺口", dashboard)
            self.assertIn("源头溯源：公司是怎么来的", dashboard)
            self.assertNotIn("源头溯源可作为证据较充分的基线使用", dashboard)
            self.assertIn("新增下钻问题", dashboard)
            self.assertIn("data-question-scope=\"XIAOMI:l0\"", dashboard)
            self.assertIn("-apple-system", dashboard)
            self.assertNotIn("消息流冲击分析", dashboard)
            self.assertNotIn("投委会摘要", dashboard)
            self.assertIn("pages/source_origin.html", dashboard)
            self.assertIn("进入 L1 子页面", dashboard)
            self.assertIn("research_report.html", dashboard)
            self.assertIn("层级 QA 聚合研究报告", report)
            self.assertIn("从问题树收敛出的当前判断", report)
            self.assertIn("最需要优先验证的问题", report)
            self.assertIn("八步框架到 L3 研究单元的收敛结果", report)
            self.assertIn("L2 收敛", report)
            self.assertIn("打开 L2 下钻页", report)
            self.assertIn("EV 单车经济是否已经证明模型成立？", report)
            self.assertIn("支持 /", report)
            self.assertIn("源头溯源", source_origin_page)
            self.assertIn("L1：源头溯源", source_origin_page)
            self.assertIn("当前要研究的问题", source_origin_page)
            self.assertIn("L2 子问题", source_origin_page)
            self.assertIn("子结构汇总结论", source_origin_page)
            self.assertIn("子问题列表", source_origin_page)
            self.assertIn("高优先级缺口", source_origin_page)
            self.assertIn("source_origin/source_origin_q1_era.html", source_origin_page)
            self.assertIn("2010", dashboard)
            self.assertIn("2010", source_origin_page)
            self.assertIn("综合子问题信息，本层结论是", dashboard)
            self.assertIn("综合子问题信息，本层结论是", source_origin_page)
            for stale_summary in ("当前已回答", "当前已覆盖", "信息结构为", "四类来源覆盖", "核心判断是"):
                self.assertNotIn(stale_summary, dashboard)
                self.assertNotIn(stale_summary, source_origin_page)
            self.assertIn("data-question-scope=\"XIAOMI:l1:source_origin\"", source_origin_page)
            self.assertIn("data-parent-id=\"foundation.source_origin\"", source_origin_page)
            self.assertIn("apply-question-queue XIAOMI", source_origin_page)
            self.assertIn("队列 JSONL", source_origin_page)
            self.assertNotIn("<b>上抛结论</b>", source_origin_page)
            self.assertNotIn("完整研究 / 源头溯源", source_origin_page)
            self.assertNotIn("源头因果链", source_origin_page)
            self.assertNotIn("qa-data", source_origin_page)
            self.assertIn("时代背景是什么？", source_origin_page)
            self.assertIn("原始问题是什么？", source_origin_page)
            self.assertIn("打开 L2 问题页", source_origin_page)
            self.assertIn("L1：公司历史", history_page)
            self.assertIn("当前要研究的问题", history_page)
            self.assertIn("L2 子问题", history_page)
            self.assertNotIn("qa-data", history_page)
            self.assertIn("哪些历史节点真正改变了商业模型？", history_page)
            self.assertIn("EV 转型是能力延伸，还是能力跃迁？", history_page)
            self.assertIn("-apple-system", history_page)
            self.assertIn("L1：当下生意", current_business_page)
            self.assertIn("当前要研究的问题", current_business_page)
            self.assertIn("L2 子问题", current_business_page)
            self.assertIn("哪个业务真正贡献毛利和现金", current_business_page)
            self.assertIn("-apple-system", current_business_page)
            self.assertIn("L2 问题展开 / 当下生意", current_business_l2_page)
            self.assertIn("打开 L3 详细分析", current_business_l2_page)
            self.assertIn("l3/current_business_profit_cash_segment_profit_pool.html", current_business_l2_page)
            self.assertIn("手机 x AIoT", current_business_l2_page)
            self.assertIn("L3 详细分析 / 当下生意", current_business_l3_page)
            self.assertIn("本问题结论", current_business_l3_page)
            self.assertIn("FY2025 小米的收入基本盘仍是手机 x AIoT", current_business_l3_page)
            self.assertIn("智能 EV/AI/新业务", current_business_l3_page)
            self.assertIn("数据拆解", current_business_l3_page)
            self.assertIn("利润/现金判断", current_business_l3_page)
            self.assertIn("经营现金流", current_business_l3_page)
            self.assertIn("四类信息索引", current_business_l3_page)
            self.assertIn("分业务毛利和经营利润", current_business_l3_page)
            self.assertIn("L2 问题展开 / 源头溯源", source_origin_l2_page)
            self.assertIn("时代背景是什么？", source_origin_l2_page)
            self.assertIn("当前要研究的问题", source_origin_l2_page)
            self.assertIn("L3 子问题", source_origin_l2_page)
            self.assertIn("本层结论", source_origin_l2_page)
            self.assertIn("本问题结论", source_origin_l2_page)
            self.assertIn("信息覆盖", source_origin_l2_page)
            self.assertIn("子问题覆盖", source_origin_l2_page)
            self.assertIn("data-question-scope=\"XIAOMI:l2:source_origin.q1-era\"", source_origin_l2_page)
            self.assertIn("data-parent-id=\"source_origin.q1-era\"", source_origin_l2_page)
            self.assertIn("四类信息索引 / 证据矩阵", source_origin_l2_page)
            self.assertIn("子问题承接表", source_origin_l2_page)
            self.assertIn("当前判断", source_origin_l2_page)
            self.assertIn("支撑信息 / 关键事实", source_origin_l2_page)
            self.assertIn("反证/线索 / 推导逻辑", source_origin_l2_page)
            self.assertIn("下一步数据", source_origin_l2_page)
            self.assertIn("更新触发器", source_origin_l2_page)
            self.assertIn("信息搜集状态", source_origin_l2_page)
            self.assertIn("检索式", source_origin_l2_page)
            self.assertIn("建议来源", source_origin_l2_page)
            self.assertIn("验收标准", source_origin_l2_page)
            self.assertIn("ev_xiaomi_global_ir_triathlon_20180503", source_origin_l2_page)
            self.assertIn("小米全球 IR 招股概要", source_origin_l2_page)
            self.assertIn("L2 问题展开 / 公司历史", history_l2_page)
            self.assertIn("EV 转型是能力延伸，还是能力跃迁？", history_l2_page)
            self.assertIn("L3 子问题", history_l2_page)
            self.assertIn("四类信息索引 / 证据矩阵", history_l2_page)
            self.assertIn("子问题承接表", history_l2_page)
            self.assertIn("最大缺口", history_l2_page)
            self.assertIn("更新触发器", history_l2_page)
            self.assertIn("季度业绩、月度交付", history_l2_page)
            self.assertIn("ev_xiaomi_2025_results_announcement_20260324", history_l2_page)

    def test_build_research_system_accepts_common_aapl_typo(self):
        with project_tmp_dir() as tmp:
            stock_dir = init_stock(tmp, "AAPL", "Apple Inc.")
            record = _evidence_record(
                "ev_aapl_revenue",
                "sec_fact",
                "SEC XBRL Revenue",
                "Revenue was 111184000000 USD for period ending 2026-03-28 in 10-Q.",
            )
            record["research_object"] = "stocks/AAPL"
            record["tickers"] = ["AAPL"]
            (stock_dir / "evidence.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")

            result = build_research_system(tmp, "APPL")

            self.assertEqual(result["ticker"], "AAPL")
            self.assertTrue((stock_dir / "research_system" / "foundation_graph.json").exists())

    def test_add_research_question_persists_and_updates_report(self):
        with project_tmp_dir() as tmp:
            stock_dir = self._seed_xiaomi(tmp)

            result = add_research_question(
                tmp,
                "XIAOMI",
                "history.h4-ev-transition",
                "SU7 订单等待周期是否能验证 EV 真实需求？",
            )

            research_dir = stock_dir / "research_system"
            custom_rows = _read_jsonl(research_dir / "custom_questions.jsonl")
            information_rows = _read_jsonl(research_dir / "information_collection.jsonl")
            qa_tree = json.loads((research_dir / "qa_tree.json").read_text(encoding="utf-8"))
            history_l2_page = (research_dir / "pages" / "history" / "history_h4_ev_transition.html").read_text(encoding="utf-8")
            report = (research_dir / "research_report.html").read_text(encoding="utf-8")
            dashboard = (research_dir / "research_dashboard.html").read_text(encoding="utf-8")

            self.assertTrue(result["created"])
            self.assertTrue(result["question_id"].startswith("history.h4-ev-transition.custom_"))
            self.assertEqual(result["parent_id"], "history.h4-ev-transition")
            self.assertEqual(len(custom_rows), 1)
            self.assertEqual(custom_rows[0]["question"], "SU7 订单等待周期是否能验证 EV 真实需求？")
            custom_node = next(node for node in qa_tree["nodes"] if node["id"] == result["question_id"])
            self.assertEqual(custom_node["level"], 3)
            self.assertEqual(custom_node["parent_id"], "history.h4-ev-transition")
            self.assertIn(result["question_id"], next(node for node in qa_tree["nodes"] if node["id"] == "history.h4-ev-transition")["next_question_ids"])
            self.assertIn("SU7 订单等待周期是否能验证 EV 真实需求？", history_l2_page)
            self.assertIn("SU7 订单等待周期是否能验证 EV 真实需求？", report)
            self.assertTrue(any(row["node_id"] == result["question_id"] for row in information_rows))
            self.assertTrue(any(row["node_id"] == result["question_id"] and row["category"] == "evidence" for row in information_rows))
            self.assertIn("信息搜集状态", history_l2_page)
            self.assertIn("用户新增问题", report)
            self.assertIn("用户新增问题", dashboard)

    def test_add_top_level_stock_question_auto_drills_to_leaf_collection(self):
        with project_tmp_dir() as tmp:
            stock_dir = self._seed_xiaomi(tmp)

            result = add_research_question(
                tmp,
                "XIAOMI",
                "company.foundation",
                "小米长期价值的核心矛盾是什么？",
            )

            research_dir = stock_dir / "research_system"
            qa_tree = json.loads((research_dir / "qa_tree.json").read_text(encoding="utf-8"))
            information_rows = _read_jsonl(research_dir / "information_collection.jsonl")
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

    def test_add_terminal_stock_question_collects_information_without_drilldown(self):
        with project_tmp_dir() as tmp:
            stock_dir = self._seed_xiaomi(tmp)

            result = add_research_question(
                tmp,
                "XIAOMI",
                "foundation.history",
                "这次新增历史问题是否已经能直接回答？",
                terminal=True,
            )

            research_dir = stock_dir / "research_system"
            qa_tree = json.loads((research_dir / "qa_tree.json").read_text(encoding="utf-8"))
            information_rows = _read_jsonl(research_dir / "information_collection.jsonl")
            custom_node = next(node for node in qa_tree["nodes"] if node["id"] == result["question_id"])

            self.assertTrue(result["created"])
            self.assertEqual(custom_node["level"], 2)
            self.assertEqual(custom_node["next_question_ids"], [])
            self.assertTrue(custom_node["metadata"]["should_collect_information"])
            self.assertFalse(custom_node["metadata"]["should_drill_down"])
            self.assertEqual(
                {"evidence", "research_report", "message", "opinion"},
                {row["category"] for row in information_rows if row["node_id"] == result["question_id"]},
            )
            validation = validate_stock_qa_system(tmp, "XIAOMI")
            self.assertTrue(validation["ok"], validation["issues"])

    def test_record_question_information_binds_source_to_node(self):
        with project_tmp_dir() as tmp:
            stock_dir = self._seed_xiaomi(tmp)
            question = add_research_question(
                tmp,
                "XIAOMI",
                "history.h4-ev-transition",
                "SU7 订单等待周期是否能验证 EV 真实需求？",
            )

            result = record_question_information(
                tmp,
                "XIAOMI",
                question["question_id"],
                "message",
                "news",
                "Delivery Wait Tracker",
                "https://example.com/xiaomi/su7-wait",
                "公开信息显示 SU7 订单等待周期仍然较长，可作为真实需求的待验证线索。",
                reliability="low",
                materiality="medium",
            )

            research_dir = stock_dir / "research_system"
            evidence_rows = _read_jsonl(stock_dir / "evidence.jsonl")
            information_rows = _read_jsonl(research_dir / "information_collection.jsonl")
            qa_tree = json.loads((research_dir / "qa_tree.json").read_text(encoding="utf-8"))
            history_l2_page = (research_dir / "pages" / "history" / "history_h4_ev_transition.html").read_text(encoding="utf-8")

            self.assertTrue(result["created"])
            self.assertEqual(result["node_id"], question["question_id"])
            self.assertEqual(result["category"], "message")
            record = next(row for row in evidence_rows if row["id"] == result["evidence_id"])
            self.assertEqual(record["information_category"], "message")
            self.assertIn(f"research_system:{question['question_id']}", record["used_in"])
            custom_node = next(node for node in qa_tree["nodes"] if node["id"] == question["question_id"])
            self.assertTrue(any(item["evidence_id"] == result["evidence_id"] for item in custom_node["evidence_buckets"]["message"]))
            self.assertTrue(
                any(
                    row["node_id"] == question["question_id"]
                    and row["category"] == "message"
                    and row["status"] == "matched"
                    for row in information_rows
                )
            )
            self.assertIn("Delivery Wait Tracker", history_l2_page)
            self.assertIn("公开信息显示 SU7 订单等待周期", history_l2_page)

    def test_collection_tasks_and_batch_import_close_research_loop(self):
        with project_tmp_dir() as tmp:
            stock_dir = self._seed_xiaomi(tmp)
            build_research_system(tmp, "XIAOMI")

            tasks_result = build_research_collection_tasks(tmp, "XIAOMI", limit=6)

            research_dir = stock_dir / "research_system"
            tasks = _read_jsonl(research_dir / "collection_tasks.jsonl")
            self.assertEqual(tasks_result["tasks"], 6)
            self.assertEqual(len(tasks), 6)
            self.assertIn("bind_command", tasks[0])
            self.assertIn("acceptance_criteria", tasks[0])
            self.assertIn("recommended_sources", tasks[0])
            self.assertIn(tasks[0]["category"], {"evidence", "research_report", "message", "opinion"})

            import_path = tmp / "xiaomi_collected_sources.jsonl"
            source_row = {
                "node_id": tasks[0]["node_id"],
                "category": tasks[0]["category"],
                "source_type": "company_ir" if tasks[0]["category"] == "evidence" else "sell_side_report",
                "source_name": "Xiaomi Collected Source",
                "url": "https://example.com/xiaomi/collected-source",
                "summary": "新补充来源直接回应该叶子问题，并提供可追溯的事实或分析摘要。",
                "reliability": tasks[0]["default_reliability"],
                "materiality": tasks[0]["default_materiality"],
            }
            import_path.write_text(json.dumps(source_row, ensure_ascii=False) + "\n", encoding="utf-8")

            import_result = import_question_information(tmp, "XIAOMI", import_path)

            qa_tree = json.loads((research_dir / "qa_tree.json").read_text(encoding="utf-8"))
            imported_node = next(node for node in qa_tree["nodes"] if node["id"] == tasks[0]["node_id"])
            self.assertEqual(import_result["records"], 1)
            self.assertEqual(import_result["created"], 1)
            self.assertTrue(
                any(
                    item.get("source_name") == "Xiaomi Collected Source"
                    for item in imported_node["evidence_buckets"][tasks[0]["category"]]
                )
            )
            report = (research_dir / "research_report.html").read_text(encoding="utf-8")
            self.assertIn("Xiaomi Collected Source", report)

    def test_run_collection_tasks_binds_matching_local_evidence(self):
        with project_tmp_dir() as tmp:
            stock_dir = self._seed_xiaomi(tmp)
            extra = _evidence_record(
                "ev_xiaomi_regional_mix_quality",
                "company_ir",
                "Xiaomi Regional Mix Quality Disclosure",
                "份额变化来自区域结构、产品结构和真实竞争力，需要用区域份额、ASP、毛利和渠道数据验证。",
            )
            extra["url"] = "https://example.com/xiaomi/regional-mix-quality"
            with (stock_dir / "evidence.jsonl").open("a", encoding="utf-8", newline="\n") as file:
                file.write(json.dumps(extra, ensure_ascii=False) + "\n")

            result = run_research_collection_tasks(tmp, "XIAOMI", min_score=8)

            research_dir = stock_dir / "research_system"
            results = _read_jsonl(research_dir / "collection_results.jsonl")
            evidence_rows = _read_jsonl(stock_dir / "evidence.jsonl")
            matched = next(row for row in evidence_rows if row["id"] == "ev_xiaomi_regional_mix_quality")
            self.assertGreater(result["matches"], 0)
            self.assertTrue(any(row["source_name"] == "Xiaomi Regional Mix Quality Disclosure" for row in results))
            self.assertIn("research_system:competition.share-quality.regional-mix", matched["used_in"])
            report = (research_dir / "research_report.html").read_text(encoding="utf-8")
            self.assertIn("Xiaomi Regional Mix Quality Disclosure", report)

    def test_source_candidate_discovery_and_apply_fetches_url(self):
        with project_tmp_dir() as tmp:
            stock_dir = self._seed_xiaomi(tmp)
            tasks_result = build_research_collection_tasks(tmp, "XIAOMI", limit=1)
            research_dir = stock_dir / "research_system"
            task = _read_jsonl(research_dir / "collection_tasks.jsonl")[0]
            search_results_path = tmp / "search_results.jsonl"
            search_results_path.write_text(
                json.dumps({
                    "task_id": task["task_id"],
                    "title": "Xiaomi Official Investor Relations Annual Report",
                    "url": "https://ir.mi.com/xiaomi/annual-report",
                    "snippet": "Official IR disclosure discusses Xiaomi business model, revenue and segment performance.",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            discover_result = discover_research_source_candidates(
                tmp,
                "XIAOMI",
                limit=1,
                results_per_task=1,
                search_results_path=search_results_path,
            )
            candidates = _read_jsonl(research_dir / "source_candidates.jsonl")

            self.assertEqual(discover_result["candidates"], 1)
            self.assertTrue(candidates[0]["accepted"])
            self.assertIn("fetch-question-information-url", candidates[0]["fetch_command"])
            self.assertEqual(candidates[0]["source_type"], "company_ir")

            html = "<html><head><title>Xiaomi Official Investor Relations Annual Report</title></head><body>官方 IR 披露业务模式、收入和分部表现。</body></html>"
            with patch(
                "value_invest_research.information_collection.urllib.request.urlopen",
                return_value=_FakeUrlResponse(html, url="https://ir.mi.com/xiaomi/annual-report"),
            ):
                apply_result = apply_research_source_candidates(
                    tmp,
                    "XIAOMI",
                    Path(discover_result["candidate_path"]),
                    min_score=1,
                )

            evidence_rows = _read_jsonl(stock_dir / "evidence.jsonl")
            report = (research_dir / "research_report.html").read_text(encoding="utf-8")
            self.assertEqual(apply_result["applied"], 1)
            self.assertTrue(any(row["source_name"] == "Xiaomi Official Investor Relations Annual Report" for row in evidence_rows))
            self.assertIn("Xiaomi Official Investor Relations Annual Report", report)

    def test_apply_question_queue_adds_questions_and_refreshes_tasks(self):
        with project_tmp_dir() as tmp:
            stock_dir = self._seed_xiaomi(tmp)
            queue_path = tmp / "queued_questions.jsonl"
            queue_path.write_text(
                json.dumps({
                    "parent_id": "history.h4-ev-transition",
                    "question": "SU7 复购和转介绍是否能验证汽车业务真实口碑？",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            result = apply_research_question_queue(
                tmp,
                "XIAOMI",
                queue_path,
                synthesize_answers=True,
                write_professional_report=True,
            )

            research_dir = stock_dir / "research_system"
            custom_rows = _read_jsonl(research_dir / "custom_questions.jsonl")
            tasks = _read_jsonl(research_dir / "collection_tasks.jsonl")
            report = (research_dir / "research_report.html").read_text(encoding="utf-8")
            detail_page = (research_dir / "pages" / "history" / "history_h4_ev_transition.html").read_text(encoding="utf-8")
            qa_tree = json.loads((research_dir / "qa_tree.json").read_text(encoding="utf-8"))

            self.assertEqual(result["records"], 1)
            self.assertEqual(result["created"], 1)
            self.assertGreater(result["tasks"], 0)
            self.assertGreater(result["synthesized_answers"], 0)
            self.assertTrue(result["professional_report_path"].endswith("professional_report.html"))
            self.assertTrue((research_dir / "synthesized_answers.jsonl").exists())
            self.assertTrue((research_dir / "professional_report.html").exists())
            validation = validate_stock_qa_system(tmp, "XIAOMI", require_professional_report=True)
            self.assertTrue(validation["ok"], validation["issues"])
            self.assertGreater(validation["summary"]["leaf_questions"], 0)
            self.assertTrue(any(row["question"] == "SU7 复购和转介绍是否能验证汽车业务真实口碑？" for row in custom_rows))
            self.assertTrue(any("SU7 复购和转介绍" in node["question"] for node in qa_tree["nodes"]))
            self.assertTrue(any("SU7 复购和转介绍" in task["question"] for task in tasks))
            self.assertIn("层级 QA 聚合研究报告", report)
            self.assertIn("SU7 复购和转介绍是否能验证汽车业务真实口碑？", detail_page)

    def test_fetch_question_information_url_binds_extracted_source(self):
        with project_tmp_dir() as tmp:
            stock_dir = self._seed_xiaomi(tmp)
            html = """
            <html>
              <head><title>Xiaomi Profit Pool Disclosure</title></head>
              <body>
                <main>公司披露互联网服务毛利率和智能电动车交付数据，可用于验证历史转型是否改变利润池。</main>
              </body>
            </html>
            """
            with patch(
                "value_invest_research.information_collection.urllib.request.urlopen",
                return_value=_FakeUrlResponse(html),
            ):
                result = fetch_question_information_url(
                    tmp,
                    "XIAOMI",
                    "history.h1-model-shift.profit-pool",
                    "evidence",
                    "https://example.com/xiaomi/profit-pool",
                )

            research_dir = stock_dir / "research_system"
            evidence_rows = _read_jsonl(stock_dir / "evidence.jsonl")
            fetched_rows = _read_jsonl(research_dir / "fetched_sources.jsonl")
            history_l2_page = (research_dir / "pages" / "history" / "history_h1_model_shift.html").read_text(encoding="utf-8")

            self.assertTrue(result["created"])
            self.assertEqual(result["source_name"], "Xiaomi Profit Pool Disclosure")
            self.assertIn("互联网服务毛利率", result["summary"])
            self.assertTrue(any(row["id"] == result["evidence_id"] for row in evidence_rows))
            self.assertEqual(fetched_rows[-1]["evidence_id"], result["evidence_id"])
            self.assertIn("Xiaomi Profit Pool Disclosure", history_l2_page)
            self.assertIn("子问题承接表", history_l2_page)

    def test_answer_synthesis_tasks_and_import_override_node_answer(self):
        with project_tmp_dir() as tmp:
            stock_dir = self._seed_xiaomi(tmp)
            tasks_result = build_stock_synthesis_tasks(tmp, "XIAOMI", limit=3)
            research_dir = stock_dir / "research_system"
            tasks = _read_jsonl(research_dir / "synthesis_tasks.jsonl")

            self.assertEqual(tasks_result["synthesis_tasks"], 3)
            self.assertIn("expected_output_fields", tasks[0])
            self.assertIn("source_index", tasks[0])
            self.assertIn("import-answer-synthesis XIAOMI", tasks[0]["import_command"])

            target_node = "history.h1-model-shift.profit-pool"
            import_path = tmp / "xiaomi_synthesis.jsonl"
            import_path.write_text(
                json.dumps({
                    "node_id": target_node,
                    "answer": "专业回答：小米历史模型迁移的核心，不是单次品类扩张，而是把用户、渠道和供应链能力反复迁移到更高客单价硬件。",
                    "facts": ["招股材料披露硬件、新零售、互联网服务的铁人三项模型。"],
                    "inferences": ["利润池变化必须同时看互联网服务毛利率和 EV 单车经济。"],
                    "judgment": "当前更适合定义为能力迁移待验证，而不是已经完成利润池重估。",
                    "gaps": ["缺少 EV 单车收入、单车毛利和售后成本的连续披露。"],
                    "next_data": ["EV 单车收入、单车毛利、售后成本和产能利用率。"],
                    "confidence": "medium",
                    "source_balance": "证据 1 / 研报 0 / 消息 0 / 观点 0。",
                    "supporting_evidence": ["ev_xiaomi_global_ir_triathlon_20180503 支撑早期模型。"],
                    "refuting_evidence": ["汽车价格战可能压低 EV 利润池。"],
                    "research_leads": ["跟踪季度 EV 经营数据。"],
                    "rollup": "小米历史模型迁移已形成方法论，但 EV 利润池是否兑现仍需单车经济验证。",
                }, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            result = import_stock_answer_synthesis(tmp, "XIAOMI", import_path)
            qa_tree = json.loads((research_dir / "qa_tree.json").read_text(encoding="utf-8"))
            node = next(node for node in qa_tree["nodes"] if node["id"] == target_node)
            page = (research_dir / "pages" / "history" / "history_h1_model_shift.html").read_text(encoding="utf-8")
            report = (research_dir / "research_report.html").read_text(encoding="utf-8")
            overrides = _read_jsonl(research_dir / "synthesis_overrides.jsonl")

            self.assertEqual(result["records"], 1)
            self.assertEqual(result["applied_nodes"], 1)
            self.assertTrue(overrides)
            self.assertIn("专业回答：小米历史模型迁移", node["current_answer"])
            self.assertEqual(node["professional_answer"]["confidence"], "medium")
            self.assertIn("synthesis_override", node["metadata"])
            self.assertIn("小米历史模型迁移的核心", page)
            self.assertIn("EV 利润池是否兑现仍需单车经济验证", report)

    def test_run_answer_synthesis_generates_and_applies_professional_answers(self):
        with project_tmp_dir() as tmp:
            stock_dir = self._seed_xiaomi(tmp)

            result = run_stock_answer_synthesis(tmp, "XIAOMI", limit=2)

            research_dir = stock_dir / "research_system"
            answers = _read_jsonl(research_dir / "synthesized_answers.jsonl")
            overrides = _read_jsonl(research_dir / "synthesis_overrides.jsonl")
            qa_tree = json.loads((research_dir / "qa_tree.json").read_text(encoding="utf-8"))
            first_node = next(node for node in qa_tree["nodes"] if node["id"] == answers[0]["node_id"])
            report = (research_dir / "research_report.html").read_text(encoding="utf-8")

            self.assertTrue(result["applied"])
            self.assertEqual(result["synthesized_answers"], 2)
            self.assertEqual(result["applied_nodes"], 2)
            self.assertEqual(len(answers), 2)
            self.assertGreaterEqual(len(overrides), 2)
            self.assertIn("专业回答：围绕", answers[0]["answer"])
            self.assertEqual(first_node["metadata"]["synthesis_override"]["source"], "deterministic_batch_synthesis")
            self.assertIn("专业回答：围绕", report)

    def test_run_answer_synthesis_can_use_llm_client(self):
        with project_tmp_dir() as tmp:
            stock_dir = self._seed_xiaomi(tmp)
            client = _FakeLlmClient()

            result = run_stock_answer_synthesis(tmp, "XIAOMI", limit=1, client=client)

            research_dir = stock_dir / "research_system"
            answers = _read_jsonl(research_dir / "synthesized_answers.jsonl")
            qa_tree = json.loads((research_dir / "qa_tree.json").read_text(encoding="utf-8"))
            node = next(node for node in qa_tree["nodes"] if node["id"] == answers[0]["node_id"])
            report = (research_dir / "research_report.html").read_text(encoding="utf-8")

            self.assertEqual(result["synthesis_mode"], "llm")
            self.assertEqual(len(client.calls), 1)
            self.assertEqual(answers[0]["synthesis_source"], "llm")
            self.assertIn("LLM回答：小米", answers[0]["answer"])
            self.assertEqual(node["metadata"]["synthesis_override"]["source"], "llm")
            self.assertIn("LLM上抛", report)


if __name__ == "__main__":
    unittest.main()
