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
            questions = _read_jsonl(research_dir / "question_graph.jsonl")
            messages = _read_jsonl(research_dir / "message_flow.jsonl")
            dashboard = (research_dir / "research_dashboard.html").read_text(encoding="utf-8")
            source_origin_page = (research_dir / "pages" / "source_origin.html").read_text(encoding="utf-8")

            self.assertEqual(result["ticker"], "XIAOMI")
            self.assertTrue(result["dashboard_path"].endswith("research_dashboard.html"))
            self.assertTrue((research_dir / "pages" / "source_origin.html").exists())
            self.assertIn(foundation["foundation_status"], {"complete", "research_ready_with_specific_gaps"})
            self.assertEqual(len(foundation["sections"]), 8)
            self.assertIn("smart_ev", {node["id"] for node in foundation["business_nodes"]})
            self.assertIn("smartphone", {node["id"] for node in foundation["business_nodes"]})
            self.assertGreater(len(foundation["assumptions"]), 0)
            self.assertGreater(len(foundation["kpis"]), 0)
            self.assertGreaterEqual(len(questions), 8)
            self.assertIn("Can Smart EV become a repeatable profit pool", " ".join(q["question"] for q in questions))
            self.assertIn("shipment weakness", " ".join(q["question"] for q in questions))
            self.assertEqual(len(messages), 6)
            recall_message = next(message for message in messages if message["evidence_id"] == "ev_xiaomi_recall")
            self.assertEqual(recall_message["impact"], "weakening")
            self.assertIn("D2", recall_message["fenghe"]["dominant_d"])
            self.assertTrue(recall_message["follow_up_question_ids"])
            self.assertIn("问题树", dashboard)
            self.assertIn("消息流冲击分析", dashboard)
            self.assertIn("pages/source_origin.html", dashboard)
            self.assertIn("打开详情页", dashboard)
            self.assertIn("ev_xiaomi_recall", dashboard)
            self.assertIn("源头溯源", source_origin_page)
            self.assertIn("这一页要回答什么", source_origin_page)
            self.assertIn("回答到什么粒度", source_origin_page)
            self.assertIn("小米当前证据", source_origin_page)
            self.assertIn("专业报告写法校准", source_origin_page)
            self.assertIn("源头结论", source_origin_page)
            self.assertIn("阶段复盘", source_origin_page)
            self.assertIn("机制拆解", source_origin_page)
            self.assertIn("ev_xiaomi_profile", source_origin_page)

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
