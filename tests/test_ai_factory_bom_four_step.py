import json
import re
import unittest
from pathlib import Path


REPORT = Path("research/qa_projects/ai_factory_industry_scurve_timeslice_20260302/professional_report.html")
WORKBENCH = Path("research/qa_projects/ai_factory_industry_scurve_timeslice_20260302/investment_workbench.json")


def details_blocks_by_class(html: str, class_name: str) -> list[str]:
    start_pattern = re.compile(
        rf'<details\b[^>]*class="[^"]*\b{re.escape(class_name)}\b[^"]*"[^>]*>',
        flags=re.DOTALL,
    )
    tag_pattern = re.compile(r"<details\b|</details>", flags=re.IGNORECASE)
    blocks = []
    for start_match in start_pattern.finditer(html):
        depth = 0
        for tag_match in tag_pattern.finditer(html, start_match.start()):
            if tag_match.group(0).lower().startswith("<details"):
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    blocks.append(html[start_match.start() : tag_match.end()])
                    break
    return blocks


def bom_question_cards(html: str) -> list[str]:
    return details_blocks_by_class(html, "bom-question-card")


def bom_research_modules(html: str) -> list[str]:
    return details_blocks_by_class(html, "bom-research-module")


def section_between(card: str, start_class: str, end_class: str) -> str:
    start_match = re.search(
        rf'class="[^"]*\bbom-step-card\b[^"]*\b{re.escape(start_class)}\b[^"]*"',
        card,
    )
    end_match = re.search(
        rf'class="[^"]*\bbom-step-card\b[^"]*\b{re.escape(end_class)}\b[^"]*"',
        card,
    )
    if not start_match or not end_match:
        raise ValueError(f"Could not locate step section {start_class} -> {end_class}")
    return card[start_match.start() : end_match.start()]


def opening_tag(block: str) -> str:
    return block.split(">", 1)[0]


class AiFactoryBomStageFlowTests(unittest.TestCase):
    def test_every_bom_question_card_uses_integrated_stage_flow(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 36)
        for index, card in enumerate(cards, start=1):
            with self.subTest(card=index):
                self.assertIn('<section class="bom-question-verdict"><b>本问结论</b>', card)
                self.assertIn('<section class="bom-question-stage-flow">', card)
                self.assertIn("<h5>具体逻辑链条</h5>", card)
                self.assertIn("Metric 历史与现状", card)
                self.assertIn("市场的未来预期", card)
                self.assertIn("第一性原理评估", card)
                self.assertIn("<h5>整体的未来趋势评估</h5>", card)
                self.assertIn("bom-step-final-trend", card)
                self.assertNotIn("逻辑环节逐卡：Metric 列表与历史数据", card)
                self.assertNotIn("逻辑环节逐卡：市场预期", card)
                self.assertNotIn("第一性原理评估未来趋势", card)

    def test_each_bom_question_is_search_first_before_verdict(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 36)
        for index, card in enumerate(cards, start=1):
            with self.subTest(card=index):
                status_cards = details_blocks_by_class(card, "bom-question-research-status")
                self.assertEqual(len(status_cards), 1)
                self.assertIn("<summary>", status_cards[0])
                self.assertIn('class="chevron"', status_cards[0])
                self.assertNotIn(" open", opening_tag(status_cards[0]))
                self.assertLess(
                    card.index('class="bom-question-research-status"'),
                    card.index('class="bom-question-verdict"'),
                )

    def test_nested_bom_stage_cards_are_collapsible_by_default(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 36)
        for index, card in enumerate(cards, start=1):
            with self.subTest(card=index):
                for class_name in [
                    "bom-step-card",
                    "bom-logic-chain-panel",
                    "bom-stage-integrated-card",
                    "bom-stage-subcard",
                    "bom-mechanism-card",
                    "bom-step-final-trend",
                ]:
                    blocks = details_blocks_by_class(card, class_name)
                    self.assertGreaterEqual(len(blocks), 1)
                    for block in blocks:
                        self.assertIn("<summary>", block)
                        self.assertIn('class="chevron"', block)
                        self.assertNotIn(" open", opening_tag(block))

    def test_first_step_contains_logic_chain_only(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 36)
        for index, card in enumerate(cards, start=1):
            question = re.search(r"<strong>(.*?)</strong>", card).group(1)
            logic_section = section_between(card, "bom-step-metrics", "bom-stage-integrated-card")
            rows = re.findall(r'<tr class="bom-logic-chain-row">.*?</tr>', logic_section, flags=re.DOTALL)
            with self.subTest(card=index, question=question):
                chain_panels = details_blocks_by_class(logic_section, "bom-logic-chain-panel")
                self.assertEqual(len(chain_panels), 1)
                self.assertIn("bom-logic-chain-table", logic_section)
                self.assertIn("<th>逻辑环节</th>", logic_section)
                self.assertIn("<th>本环节要判断什么</th>", logic_section)
                self.assertIn("<th>为什么放在链条里</th>", logic_section)
                self.assertNotIn("<th>应该看的 Metric</th>", logic_section)
                self.assertNotIn("ChatGPT weekly active users", logic_section)
                self.assertNotIn("Microsoft commercial remaining performance obligation", logic_section)
                self.assertNotRegex(logic_section, r"metric-data-table|metric-trend-gap|metric-point-count|<svg")
                self.assertGreaterEqual(len(rows), 4)
                self.assertLessEqual(len(rows), 7)

    def test_each_logic_row_has_one_integrated_stage_card(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 36)
        for index, card in enumerate(cards, start=1):
            logic_section = section_between(card, "bom-step-metrics", "bom-stage-integrated-card")
            logic_rows = re.findall(r'<tr class="bom-logic-chain-row">.*?</tr>', logic_section, flags=re.DOTALL)
            stage_cards = details_blocks_by_class(card, "bom-stage-integrated-card")
            with self.subTest(card=index):
                self.assertEqual(len(stage_cards), len(logic_rows))
                for stage_index, stage_card in enumerate(stage_cards, start=1):
                    self.assertIn(f"环节 {stage_index}", stage_card)
                    self.assertIn("Metric 历史与现状", stage_card)
                    self.assertIn("市场的未来预期", stage_card)
                    self.assertIn("第一性原理评估", stage_card)
                    self.assertEqual(len(details_blocks_by_class(stage_card, "bom-stage-history-card")), 1)
                    self.assertEqual(len(details_blocks_by_class(stage_card, "bom-stage-future-card")), 1)
                    self.assertEqual(len(details_blocks_by_class(stage_card, "bom-stage-mechanism-card")), 1)
                    self.assertIn("bom-expectation-table", stage_card)
                    self.assertGreaterEqual(len(details_blocks_by_class(stage_card, "bom-mechanism-card")), 2)

    def test_integrated_stage_history_directly_renders_metric_tables(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 36)
        for index, card in enumerate(cards, start=1):
            stage_cards = details_blocks_by_class(card, "bom-stage-integrated-card")
            with self.subTest(card=index):
                for stage_card in stage_cards:
                    history_card = details_blocks_by_class(stage_card, "bom-stage-history-card")[0]
                    self.assertNotIn("本环节应看哪些 Metric", history_card)
                    self.assertNotIn("当前证据读法", history_card)
                    self.assertIn("metric-history-group", history_card)
                    self.assertIn("metric-history-table", history_card)
                    self.assertIn("metric-history-caption", history_card)
                    self.assertIn("metric-history-name", history_card)
                    self.assertIn("metric-history-definition", history_card)
                    self.assertNotIn("<th>Metric</th>", history_card)
                    self.assertNotIn("<th>口径 / 数据要求</th>", history_card)
                    self.assertNotIn('class="metric-name-cell"', history_card)
                    self.assertIn("<th>期间 / 截点</th>", history_card)
                    self.assertIn("<th>数值</th>", history_card)
                    self.assertRegex(history_card, r'<a class="metric-history-name" ')
                    self.assertRegex(stage_card, r"metric-data-table|metric-trend-gap")

    def test_integrated_stage_future_directly_renders_entity_expectation_tables(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 36)
        for index, card in enumerate(cards, start=1):
            stage_cards = details_blocks_by_class(card, "bom-stage-integrated-card")
            with self.subTest(card=index):
                for stage_card in stage_cards:
                    future_card = details_blocks_by_class(stage_card, "bom-stage-future-card")[0]
                    self.assertNotIn("市场现在预期什么？", future_card)
                    self.assertNotIn("bom-expectation-grid", future_card)
                    self.assertNotIn("bom-expectation-field", future_card)
                    self.assertNotIn('class="bom-future-card', future_card)
                    self.assertIn("expectation-table-group", future_card)
                    self.assertIn("bom-expectation-table", future_card)
                    self.assertIn("<th>公司 / 机构</th>", future_card)
                    self.assertIn("<th>现状期间</th>", future_card)
                    self.assertIn("<th>预期 / 指引口径 / 数值</th>", future_card)
                    self.assertRegex(future_card, r'<td class="expectation-entity-cell"><a ')

    def test_metric_history_uses_tables_not_visual_charts(self):
        html = REPORT.read_text(encoding="utf-8")

        forbidden_visual_classes = [
            'class="metric-trend-chart"',
            'class="metric-noncontinuous-chart"',
            'class="metric-multi-line-chart"',
            'class="metric-comparison-bars"',
            'class="metric-bar"',
            'class="metric-line"',
            'class="metric-dot"',
            "<svg",
            "<polyline",
        ]
        for forbidden in forbidden_visual_classes:
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, html)

    def test_compute_demand_question_keeps_history_expectation_and_mechanism_by_stage(self):
        html = REPORT.read_text(encoding="utf-8")
        compute_first_question = bom_question_cards(html)[0]

        expected_stage_titles = [
            "应用/任务",
            "预算/RPO",
            "订单/交付",
            "BOM弹性",
            "GPU财务兑现",
            "ASIC财务兑现",
            "反证/缺口",
        ]
        for title in expected_stage_titles:
            with self.subTest(title=title):
                self.assertIn(title, compute_first_question)

        expected_metrics = [
            "ChatGPT weekly active users (WAU)",
            "Microsoft commercial remaining performance obligation (Commercial RPO, $B)",
            "Dell AI-optimized server ending backlog ($B)",
            "NVIDIA Data Center segment revenue ($B)",
            "Broadcom AI semiconductor revenue ($B)",
            "Public GPU-hours consumed by AI workloads (GPU-hours)",
            "Q2 FY25",
            "&gt;$4.4B",
        ]
        for metric in expected_metrics:
            with self.subTest(metric=metric):
                self.assertIn(metric, compute_first_question)

        expected_expectation_labels = [
            "公司 / 机构",
            "现状期间",
            "现状口径 / 数值",
            "指引期间",
            "预期 / 指引口径 / 数值",
            "口径说明 / 投资含义",
        ]
        for label in expected_expectation_labels:
            with self.subTest(label=label):
                self.assertIn(label, compute_first_question)

        pricing_terms = ["EV/Sales", "priced-in", "reverse DCF"]
        for term in pricing_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, compute_first_question)

    def test_final_trend_card_collects_whole_question_future_assessment(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 36)
        for index, card in enumerate(cards, start=1):
            with self.subTest(card=index):
                final_cards = details_blocks_by_class(card, "bom-step-final-trend")
                self.assertEqual(len(final_cards), 1)
                final_card = final_cards[0]
                self.assertIn("<h5>整体的未来趋势评估</h5>", final_card)
                self.assertIn("支持未来继续的机制", final_card)
                self.assertIn("削弱或推翻趋势的机制", final_card)
                self.assertGreater(
                    card.index('class="bom-step-card bom-step-final-trend"'),
                    card.rindex("bom-stage-integrated-card"),
                )

    def test_s_curve_stage_card_appears_only_after_all_six_questions(self):
        html = REPORT.read_text(encoding="utf-8")
        modules = bom_research_modules(html)

        self.assertGreaterEqual(len(modules), 6)
        for index, module in enumerate(modules, start=1):
            with self.subTest(module=index):
                question_cards = details_blocks_by_class(module, "bom-question-card")
                stage_cards = details_blocks_by_class(module, "bom-s-curve-stage-card")
                self.assertEqual(len(question_cards), 6)
                self.assertEqual(len(stage_cards), 1)
                self.assertNotIn(" open", opening_tag(stage_cards[0]))
                self.assertGreater(
                    module.index('class="bom-s-curve-stage-card"'),
                    module.rindex('class="bom-question-card"'),
                )

    def test_s_curve_stage_card_uses_six_question_rollup_schema(self):
        html = REPORT.read_text(encoding="utf-8")
        stage_cards = details_blocks_by_class(html, "bom-s-curve-stage-card")

        self.assertGreaterEqual(len(stage_cards), 6)
        for index, stage_card in enumerate(stage_cards, start=1):
            with self.subTest(stage=index):
                self.assertIn('class="bom-stage-current"', stage_card)
                self.assertIn('class="bom-stage-evidence-grid"', stage_card)
                self.assertIn('class="bom-stage-next-signal"', stage_card)
                self.assertIn('class="bom-stage-downgrade-signal"', stage_card)
                self.assertIn('class="bom-stage-source-discipline"', stage_card)

    def test_compute_demand_question_can_be_strictly_completed_without_stage_leak(self):
        html = REPORT.read_text(encoding="utf-8")
        workbench = json.loads(WORKBENCH.read_text(encoding="utf-8"))
        artifacts = {
            item["artifact_id"]: item
            for item in workbench["bom_question_search_artifacts"]
        }

        self.assertEqual(
            artifacts["BOM-SEARCH-compute_q1"]["search_execution_status"],
            "completed",
        )
        self.assertIn("SRC-OPENAI-DEVDAY-2025", artifacts["BOM-SEARCH-compute_q1"]["source_ids"])
        self.assertIn("SRC-NVDA-FY26-Q4", artifacts["BOM-SEARCH-compute_q1"]["source_ids"])
        self.assertIn("待逐问搜索完成后判定", html)

    def test_compute_demand_question_uses_specific_primary_metric_per_stage(self):
        html = REPORT.read_text(encoding="utf-8")
        compute_first_question = bom_question_cards(html)[0]

        expected_definitions = [
            "主体：Microsoft；字段：Commercial remaining performance obligation",
            "主体：Dell；字段：AI-optimized server ending backlog",
            "主体：NVIDIA；字段：Data Center segment revenue",
            "主体：Broadcom；字段：AI semiconductor revenue",
        ]
        for definition in expected_definitions:
            with self.subTest(definition=definition):
                self.assertIn(definition, compute_first_question)

        vague_metric_names = [
            "ChatGPT / Gemini 使用量与 token 工作负载锚点",
            "Hyperscaler AI budget and committed demand",
            "Dell AI-optimized server order-to-revenue funnel",
            "Broadcom AI semiconductor revenue checkpoints",
            "tokens / GPU hours / utilization / AI ROI direct series",
        ]
        for vague_metric in vague_metric_names:
            with self.subTest(vague_metric=vague_metric):
                self.assertNotIn(vague_metric, compute_first_question)

    def test_compute_demand_history_keeps_broadcom_guidance_out_of_actual_curve(self):
        html = REPORT.read_text(encoding="utf-8")
        compute_first_question = bom_question_cards(html)[0]
        broadcom_cards = [
            card
            for card in details_blocks_by_class(compute_first_question, "bom-stage-integrated-card")
            if "Broadcom AI semiconductor revenue ($B)" in card
        ]

        self.assertEqual(len(broadcom_cards), 1)
        broadcom_card = broadcom_cards[0]
        self.assertIn('class="metric-trend-gap"', broadcom_card)
        self.assertIn("Q2 FY25", broadcom_card)
        self.assertIn("Q3 FY25", broadcom_card)
        self.assertIn("Q1 FY26", broadcom_card)
        self.assertNotIn("Q4 FY25 guide", broadcom_card)
        self.assertNotIn("Q2 FY26 guide", broadcom_card)
        self.assertNotIn("actual / guidance checkpoints", broadcom_card)


if __name__ == "__main__":
    unittest.main()
