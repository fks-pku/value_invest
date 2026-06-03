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
            self.assertIn("当前研究的问题", report)
            self.assertIn("下钻 QA", report)
            self.assertIn("Q1", report)

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
            self.assertIn("当前研究的问题", report)
            self.assertIn("下钻 QA", report)
            self.assertIn("qa-source-list", report)
            self.assertIn('href="https://example.com/robotics/shipments"', report)

    def test_write_meta_qa_professional_report_renders_investment_workbench(self):
        with project_tmp_dir() as tmp:
            result = build_meta_qa_research(
                tmp,
                "event",
                "tau_law",
                "分析韬定律对半导体投资研究的意义",
                project_id="tau_law",
            )
            project_dir = Path(result["project_dir"])
            workbench = {
                "research_execution_plan": {
                    "title": "用问题层级控制研究深度",
                    "summary": "先问问题，再收资料，最后上抛结论。",
                    "deepseek_role": "DeepSeek 只做资料摘要，不做最终判断。",
                    "stages": [
                        {
                            "level": "L1",
                            "name": "主线拆分",
                            "role": "拆出研究方向。",
                            "questions": ["哪里会卡住？"],
                            "collection": ["收集一手证据。"],
                            "synthesis": ["串成机制链。"],
                            "presentation": ["展示结论和来源。"],
                        }
                    ],
                },
                "depth_protocol": {
                    "summary": "用问题层级保证研究深度。",
                    "levels": [
                        {
                            "level": "L3",
                            "name": "证据单元",
                            "role": "最小研究任务。",
                            "drill_rule": "不能回答时继续拆窄。",
                            "rollup_rule": "事实、推论、判断、缺口上抛。",
                        }
                    ],
                    "quality_gates": ["没有反证条件时不能标为高置信。"],
                },
                "chokepoint_protocol": {
                    "summary": "从大主题拆到窄瓶颈。",
                    "steps": [
                        {
                            "step": "01",
                            "name": "拆供应链",
                            "purpose": "找到最窄节点。",
                            "key_question": "哪里会卡住？",
                            "output": "瓶颈地图。",
                        }
                    ],
                },
                "supply_chain_map": [
                    {
                        "layer": "先进封装",
                        "bottleneck_question": "混合键合是否是瓶颈？",
                        "current_judgment": "需要订单验证。",
                        "status": "核心观察",
                        "candidate_nodes": ["混合键合"],
                        "proof_needed": ["客户订单"],
                        "disconfirming_tests": ["无收入"],
                        "evidence_ids": ["ev_tau"],
                    }
                ],
                "bottleneck_scorecard": [
                    {
                        "node": "先进封装",
                        "asset_mapping": "封测公司",
                        "criticality": "高",
                        "scarcity": "中高",
                        "pricing_power": "待验证",
                        "market_awareness": "升温",
                        "evidence_quality": "中等",
                        "current_assessment": "优先下钻。",
                    }
                ],
                "hypothesis_matrix": [
                    {
                        "id": "H1",
                        "hypothesis": "先进封装可能是核心受益环节。",
                        "current_judgment": "需要订单验证。",
                        "confidence": "中等",
                        "linked_questions": ["L1 传导机制"],
                        "supporting_evidence": ["ev_tau"],
                        "disconfirming_evidence": ["缺少订单"],
                        "triggers": ["客户订单"],
                        "target_implications": ["先进封装观察池"],
                    }
                ],
                "target_mapping": [
                    {
                        "tier": "A",
                        "target_type": "先进封装链条",
                        "mapping_logic": "直接对应 3D 集成。",
                        "research_action": "核心观察池。",
                        "time_horizon": "T2",
                        "linked_hypotheses": ["H1"],
                        "evidence_ids": ["ev_tau"],
                        "required_data": ["订单"],
                        "disconfirming_tests": ["无收入占比"],
                    }
                ],
                "specific_targets": [
                    {
                        "tier": "A",
                        "company": "测试封装公司",
                        "ticker": "000001.SZ",
                        "strength": "A-：核心观察",
                        "bottleneck_node": "先进封装",
                        "reason": "直接对应瓶颈。",
                        "verification_data": ["订单"],
                        "catalysts": ["客户验证"],
                        "risks": ["无收入占比"],
                        "sources": [
                            {"label": "测试来源", "url": "https://example.com/source", "category": "证据"}
                        ],
                    }
                ],
                "adversarial_review": [
                    {
                        "id": "A1",
                        "severity": "高",
                        "challenge": "是否只是概念重命名？",
                        "why_it_matters": "避免主题外推。",
                        "evidence_to_collect": ["技术对照"],
                        "if_true_action": ["降级结论"],
                    }
                ],
                "tracking_triggers": [
                    {
                        "trigger": "产品评测",
                        "why_it_matters": "验证技术是否落地。",
                        "update_rule": "通过则提高置信度。",
                        "owner_view": "技术验证",
                    }
                ],
            }
            (project_dir / "investment_workbench.json").write_text(
                json.dumps(workbench, ensure_ascii=False),
                encoding="utf-8",
            )

            report_result = write_meta_qa_professional_report(tmp, "tau_law")

            report = Path(report_result["professional_report_path"]).read_text(encoding="utf-8")
            markdown = Path(report_result["professional_report_md_path"]).read_text(encoding="utf-8")
            self.assertTrue(report_result["investment_workbench_path"].endswith("investment_workbench.json"))
            self.assertIn("当前研究的问题", report)
            self.assertIn("研究执行计划", report)
            self.assertIn("DeepSeek 只做资料摘要", report)
            self.assertIn("下钻 QA", report)
            self.assertIn("Q1", report)
            self.assertIn("Q1.1", report)
            self.assertIn("Q1.1.1", report)
            self.assertIn("标的推荐", report)
            self.assertIn("测试封装公司", report)
            self.assertIn("000001.SZ", report)
            self.assertIn("A-：核心观察", report)
            self.assertIn('<details id="qa-l1-1"', report)
            self.assertIn('<details class="qa-l2-card"', report)
            self.assertIn('<details class="qa-l3-card"', report)
            self.assertNotIn("工作台附录", report)
            self.assertNotIn("完整报告", report)
            self.assertNotIn("AI 反方质询清单", report)
            self.assertNotIn("瓶颈研究摘要", report)
            self.assertIn("瓶颈研究摘要", markdown)
            self.assertIn("投资标的映射摘要", markdown)

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
            self.assertIn("LLM 报告已经基于 QA 树收敛", markdown)
            self.assertIn("当前研究的问题", report)


if __name__ == "__main__":
    unittest.main()
