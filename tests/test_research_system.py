import json
import unittest
from pathlib import Path

from tests.helpers import project_tmp_dir
from value_invest_research.research_system import build_research_system
from value_invest_research.scaffold import init_stock


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


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
            questions = _read_jsonl(research_dir / "question_graph.jsonl")
            messages = _read_jsonl(research_dir / "message_flow.jsonl")
            dashboard = (research_dir / "research_dashboard.html").read_text(encoding="utf-8")
            source_origin_page = (research_dir / "pages" / "source_origin.html").read_text(encoding="utf-8")
            history_page = (research_dir / "pages" / "history.html").read_text(encoding="utf-8")
            current_business_page = (research_dir / "pages" / "current_business.html").read_text(encoding="utf-8")
            source_origin_l2_page = (research_dir / "pages" / "source_origin" / "source_origin_q1_era.html").read_text(encoding="utf-8")
            history_l2_page = (research_dir / "pages" / "history" / "history_h4_ev_transition.html").read_text(encoding="utf-8")

            self.assertEqual(result["ticker"], "XIAOMI")
            self.assertTrue(result["dashboard_path"].endswith("research_dashboard.html"))
            self.assertTrue(result["qa_tree_path"].endswith("qa_tree.json"))
            self.assertTrue((research_dir / "pages" / "source_origin.html").exists())
            self.assertTrue((research_dir / "pages" / "history.html").exists())
            self.assertTrue((research_dir / "pages" / "current_business.html").exists())
            self.assertTrue((research_dir / "pages" / "source_origin" / "source_origin_q1_era.html").exists())
            self.assertTrue((research_dir / "pages" / "history" / "history_h4_ev_transition.html").exists())
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
            ev_node = next(node for node in qa_tree["nodes"] if node["id"] == "history.h4-ev-transition")
            self.assertEqual(ev_node["level"], 2)
            self.assertIn("history.h4-ev-transition.unit-economics", ev_node["next_question_ids"])
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
            self.assertIn("源头溯源", source_origin_page)
            self.assertIn("L1：源头溯源", source_origin_page)
            self.assertIn("当前要研究的问题", source_origin_page)
            self.assertIn("L2 子问题", source_origin_page)
            self.assertIn("子结构汇总结论", source_origin_page)
            self.assertIn("子问题列表", source_origin_page)
            self.assertIn("高优先级缺口", source_origin_page)
            self.assertIn("source_origin/source_origin_q1_era.html", source_origin_page)
            self.assertIn("当前回答优先由", source_origin_page)
            self.assertIn("该源头问题向上提供的能力边界", source_origin_page)
            self.assertIn("data-question-scope=\"XIAOMI:l1:source_origin\"", source_origin_page)
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
            self.assertIn("L2 问题展开 / 源头溯源", source_origin_l2_page)
            self.assertIn("时代背景是什么？", source_origin_l2_page)
            self.assertIn("当前要研究的问题", source_origin_l2_page)
            self.assertIn("L3 子问题", source_origin_l2_page)
            self.assertIn("子结构汇总结论", source_origin_l2_page)
            self.assertIn("data-question-scope=\"XIAOMI:l2:source_origin.q1-era\"", source_origin_l2_page)
            self.assertIn("四类信息索引 / 证据矩阵", source_origin_l2_page)
            self.assertIn("当前判断", source_origin_l2_page)
            self.assertIn("关键事实", source_origin_l2_page)
            self.assertIn("推导逻辑", source_origin_l2_page)
            self.assertIn("下一步数据", source_origin_l2_page)
            self.assertIn("更新触发器", source_origin_l2_page)
            self.assertIn("ev_xiaomi_global_ir_triathlon_20180503", source_origin_l2_page)
            self.assertIn("小米全球 IR 招股概要", source_origin_l2_page)
            self.assertIn("L2 问题展开 / 公司历史", history_l2_page)
            self.assertIn("EV 转型是能力延伸，还是能力跃迁？", history_l2_page)
            self.assertIn("L3 子问题", history_l2_page)
            self.assertIn("四类信息索引 / 证据矩阵", history_l2_page)
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


if __name__ == "__main__":
    unittest.main()
