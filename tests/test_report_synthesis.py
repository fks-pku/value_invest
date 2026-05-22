import json
import unittest
from pathlib import Path

from tests.helpers import project_tmp_dir
from value_invest_research.meta_qa_research import build_meta_qa_research, record_meta_qa_information
from value_invest_research.report_synthesis import (
    _deterministic_report_markdown,
    write_meta_qa_professional_report,
    write_stock_professional_report,
)
from value_invest_research.scaffold import init_stock


class _FakeReportClient:
    def __init__(self):
        self.calls: list[tuple[str, str]] = []

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        self.calls.append((system_prompt, user_prompt))
        return """# LLM 专业报告

## 一页投研摘要
- LLM 报告已经基于 QA 树收敛。

## 核心判断与依据
- 关键判断必须回到问题节点和来源结构。

## 反证条件
- 如果核心来源被反证，报告结论需要更新。

## 使用边界
本报告不是交易建议。
"""


def _seed_stock(root: Path) -> Path:
    stock_dir = init_stock(root, "AAPL", "Apple Inc.")
    record = {
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
    }
    (stock_dir / "evidence.jsonl").write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
    return stock_dir


class ReportSynthesisTests(unittest.TestCase):
    def test_deterministic_report_prioritizes_research_content_over_structure(self):
        markdown = _deterministic_report_markdown(
            {
                "object_id": "XIAOMI",
                "object_type": "stock",
                "meta_question": "公司基础画像如何？",
                "node_count": 4,
                "leaf_nodes": [{"id": "leaf"}],
                "evidence_counts": {"evidence": 1, "research_report": 1, "message": 0, "opinion": 0},
                "priority_gaps": ["需要补充分部毛利。"],
                "top_level": [
                    {
                        "question": "源头溯源：公司为什么出现？",
                        "rollup": "当前已覆盖 2/2 个子问题，信息结构为 3 支持 / 0 反证 / 0 线索。",
                        "judgment": "当前已覆盖 2/2 个子问题，信息结构为 3 支持 / 0 反证 / 0 线索。",
                        "answer": "当前已覆盖 2/2 个子问题。",
                        "facts": [],
                        "inferences": [],
                        "gaps": [],
                        "children": [],
                        "leaf_nodes": [
                            {
                                "question": "MIUI 是否是早期楔子？",
                                "facts": [
                                    "证据：小米成立于 2010 年 4 月，并于 2010 年 8 月推出 MIUI 私测版本。 [ev_origin]"
                                ],
                                "inferences": ["MIUI 先于手机硬件形成用户反馈入口。"],
                                "gaps": ["需要补充 2010-2012 年智能手机渗透率。"],
                                "supporting_evidence": [],
                                "refuting_evidence": [],
                                "research_leads": [],
                            }
                        ],
                    }
                ],
                "root_answer": "",
                "root_judgment": "",
            }
        )

        self.assertIn("小米成立于 2010 年 4 月", markdown)
        self.assertIn("MIUI 先于手机硬件形成用户反馈入口", markdown)
        self.assertNotIn("当前已覆盖 2/2", markdown)
        self.assertNotIn("信息结构为", markdown)

    def test_write_stock_professional_report_from_qa_tree(self):
        with project_tmp_dir() as tmp:
            stock_dir = _seed_stock(tmp)

            result = write_stock_professional_report(tmp, "APPL")

            report = Path(result["professional_report_path"]).read_text(encoding="utf-8")
            markdown = Path(result["professional_report_md_path"]).read_text(encoding="utf-8")
            self.assertEqual(result["ticker"], "AAPL")
            self.assertEqual(result["report_mode"], "deterministic")
            self.assertTrue((stock_dir / "research_system" / "professional_report.html").exists())
            self.assertIn("AAPL 专业投研报告", markdown)
            self.assertIn("投研摘要", report)
            self.assertIn("事实依据", report)
            self.assertIn("不是交易建议", report)

    def test_write_meta_qa_professional_report_from_answers(self):
        with project_tmp_dir() as tmp:
            build_meta_qa_research(
                tmp,
                "industry",
                "机器人",
                "分析人形机器人产业链的投资价值",
                project_id="robotics_chain",
            )
            record_meta_qa_information(
                tmp,
                "robotics_chain",
                "l1.demand.market_size.evidence_map",
                "evidence",
                "industry_data",
                "Robot Shipment Dataset",
                "https://example.com/robotics/shipments",
                "机器人出货、订单和客户验收数据是验证行业空间的核心。",
                reliability="high",
                materiality="high",
            )

            result = write_meta_qa_professional_report(tmp, "robotics_chain")

            report = Path(result["professional_report_path"]).read_text(encoding="utf-8")
            markdown = Path(result["professional_report_md_path"]).read_text(encoding="utf-8")
            self.assertEqual(result["report_mode"], "deterministic")
            self.assertIn("机器人 专业投研报告", markdown)
            self.assertIn("机器人", report)
            self.assertIn("关键缺口", report)

    def test_write_meta_qa_professional_report_can_use_llm_client(self):
        with project_tmp_dir() as tmp:
            build_meta_qa_research(
                tmp,
                "industry",
                "机器人",
                "分析人形机器人产业链的投资价值",
                project_id="robotics_chain",
            )
            client = _FakeReportClient()

            result = write_meta_qa_professional_report(tmp, "robotics_chain", client=client)

            report = Path(result["professional_report_path"]).read_text(encoding="utf-8")
            markdown = Path(result["professional_report_md_path"]).read_text(encoding="utf-8")
            self.assertEqual(result["report_mode"], "llm")
            self.assertEqual(len(client.calls), 1)
            self.assertIn("LLM 专业报告", markdown)
            self.assertIn("LLM 报告已经基于 QA 树收敛", report)


if __name__ == "__main__":
    unittest.main()
