import json
import re
import unittest
from pathlib import Path


REPORT = Path("research/qa_projects/ai_factory_industry_scurve_timeslice_20260302/professional_report.html")
WORKBENCH = Path("research/qa_projects/ai_factory_industry_scurve_timeslice_20260302/investment_workbench.json")


def bom_question_cards(html: str) -> list[str]:
    return details_blocks_by_class(html, "bom-question-card")


def bom_research_modules(html: str) -> list[str]:
    return details_blocks_by_class(html, "bom-research-module")


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


def section_between(card: str, start_class: str, end_class: str) -> str:
    start = card.index(f'class="bom-step-card {start_class}"')
    end = card.index(f'class="bom-step-card {end_class}"')
    return card[start:end]


def opening_tag(block: str) -> str:
    return block.split(">", 1)[0]


class AiFactoryBomFourStepTests(unittest.TestCase):
    FOUR_SECTION_TITLES = [
        "研究逻辑链条与应看 Metric",
        "逻辑环节逐卡：Metric 历史数据",
        "市场对这一子部分的未来预期",
        "第一性原理评估未来趋势",
    ]

    def test_every_bom_question_card_has_new_four_part_structure(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 42)
        for index, card in enumerate(cards, start=1):
            with self.subTest(card=index):
                self.assertIn('<section class="bom-question-verdict"><b>本问结论</b>', card)
                positions = []
                for title in self.FOUR_SECTION_TITLES:
                    self.assertIn(f"<h5>{title}</h5>", card)
                    positions.append(card.index(f"<h5>{title}</h5>"))
                self.assertEqual(positions, sorted(positions))
                self.assertIn("bom-step-metrics", card)
                self.assertIn("bom-step-history", card)
                self.assertIn("bom-step-future", card)
                self.assertIn("bom-step-mechanism", card)

    def test_each_bom_question_is_search_first_before_verdict(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 42)
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

    def test_nested_bom_step_cards_are_collapsible_by_default(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 42)
        for index, card in enumerate(cards, start=1):
            step_cards = details_blocks_by_class(card, "bom-step-card")
            with self.subTest(card=index):
                self.assertNotIn('<article class="bom-step-card', card)
                self.assertEqual(len(step_cards), 4)
                for step_card in step_cards:
                    self.assertIn("<summary>", step_card)
                    self.assertIn('class="chevron"', step_card)
                    self.assertNotIn(" open", opening_tag(step_card))

    def test_first_part_contains_logic_chain_metric_table(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 42)
        for index, card in enumerate(cards, start=1):
            question = re.search(r"<strong>(.*?)</strong>", card).group(1)
            metrics_section = section_between(card, "bom-step-metrics", "bom-step-history")
            rows = re.findall(r'<tr class="bom-logic-chain-row">.*?</tr>', metrics_section, flags=re.DOTALL)
            with self.subTest(card=index, question=question):
                chain_panels = details_blocks_by_class(metrics_section, "bom-logic-chain-panel")
                self.assertEqual(len(chain_panels), 1)
                self.assertIn("<summary>", chain_panels[0])
                self.assertIn('class="chevron"', chain_panels[0])
                self.assertNotIn(" open", opening_tag(chain_panels[0]))
                self.assertIn("bom-logic-chain-table", metrics_section)
                self.assertIn("<th>逻辑环节</th>", metrics_section)
                self.assertIn("<th>应该看的 Metric</th>", metrics_section)
                self.assertIn("<th>为什么看它</th>", metrics_section)
                self.assertGreaterEqual(len(rows), 4)
                self.assertLessEqual(len(rows), 7)
                self.assertNotRegex(metrics_section, r"metric-trend-chart|metric-noncontinuous-chart|metric-trend-gap|<svg")

    def test_second_part_uses_stage_cards_with_metric_history(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 42)
        for index, card in enumerate(cards, start=1):
            question = re.search(r"<strong>(.*?)</strong>", card).group(1)
            metrics_section = section_between(card, "bom-step-metrics", "bom-step-history")
            history_section = section_between(card, "bom-step-history", "bom-step-future")
            logic_rows = re.findall(r'<tr class="bom-logic-chain-row">.*?</tr>', metrics_section, flags=re.DOTALL)
            stage_cards = re.findall(
                r'<details class="bom-logic-stage-card">.*?</details>',
                history_section,
                flags=re.DOTALL,
            )
            with self.subTest(card=index, question=question):
                self.assertIn('class="bom-logic-stage-stack"', history_section)
                self.assertNotIn('<article class="bom-logic-stage-card"', history_section)
                self.assertEqual(len(stage_cards), len(logic_rows))
                for stage_index, stage_card in enumerate(stage_cards, start=1):
                    self.assertIn(f"环节 {stage_index}", stage_card)
                    self.assertIn("<summary>", stage_card)
                    self.assertIn('class="chevron"', stage_card)
                    self.assertRegex(stage_card, r"metric-data-table|metric-trend-gap")
                    self.assertRegex(stage_card, r"<p\b[^>]*>.+?</p>")

    def test_repeated_logic_stage_cards_are_collapsible_by_default(self):
        html = REPORT.read_text(encoding="utf-8")
        history_sections = [
            section_between(card, "bom-step-history", "bom-step-future")
            for card in bom_question_cards(html)
        ]

        self.assertGreaterEqual(len(history_sections), 42)
        for index, history_section in enumerate(history_sections, start=1):
            stage_cards = re.findall(
                r'<details class="bom-logic-stage-card"[^>]*>.*?</details>',
                history_section,
                flags=re.DOTALL,
            )
            with self.subTest(card=index):
                self.assertGreaterEqual(len(stage_cards), 4)
                for stage_card in stage_cards:
                    opening_tag = stage_card.split(">", 1)[0]
                    self.assertNotIn(" open", opening_tag)

    def test_time_series_charts_use_at_least_five_points_or_show_gap(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 42)
        chart_blocks = re.findall(
            r'<div class="metric-trend-chart">.*?</div>',
            html,
            flags=re.DOTALL,
        )
        for chart_index, chart in enumerate(chart_blocks, start=1):
            with self.subTest(chart=chart_index):
                self.assertGreaterEqual(chart.count('class="metric-dot"'), 5)
                self.assertIn("metric-point-count", chart)
        self.assertIn("少于 5 个同口径历史数据点", html)

    def test_metric_history_uses_data_tables_not_visual_charts(self):
        html = REPORT.read_text(encoding="utf-8")
        compute_first_question = bom_question_cards(html)[0]
        history_section = section_between(
            compute_first_question,
            "bom-step-history",
            "bom-step-future",
        )

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

        self.assertIn('class="metric-data-table"', history_section)
        self.assertIn("ChatGPT weekly active users (WAU)", history_section)
        self.assertIn("Microsoft commercial remaining performance obligation", history_section)
        self.assertIn("Dell AI-optimized server ending backlog", history_section)
        self.assertIn("NVIDIA Data Center segment revenue", history_section)
        self.assertIn("Broadcom AI semiconductor revenue ($B)", history_section)
        self.assertIn("Q2 FY25", history_section)
        self.assertIn("&gt;$4.4B", history_section)

    def test_future_and_first_principles_sections_stay_prose_based(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 42)
        for index, card in enumerate(cards, start=1):
            question = re.search(r"<strong>(.*?)</strong>", card).group(1)
            future_section = section_between(card, "bom-step-future", "bom-step-mechanism")
            mechanism_start = card.index('class="bom-step-card bom-step-mechanism"')
            mechanism_section = card[mechanism_start:]
            with self.subTest(card=index, question=question):
                self.assertIn('class="bom-future-grid"', future_section)
                self.assertNotIn("<section>\n        <b>", future_section)
                for future_card in details_blocks_by_class(future_section, "bom-future-card"):
                    self.assertIn("<summary>", future_card)
                    self.assertNotIn(" open", opening_tag(future_card))
                self.assertGreaterEqual(len(details_blocks_by_class(future_section, "bom-future-card")), 2)
                self.assertIn("可持续机制", mechanism_section)
                self.assertIn("不可持续/反证机制", mechanism_section)
                self.assertNotIn("<section><b>可持续机制</b>", mechanism_section)
                mechanism_cards = details_blocks_by_class(mechanism_section, "bom-mechanism-card")
                self.assertEqual(len(mechanism_cards), 2)
                for mechanism_card in mechanism_cards:
                    self.assertIn("<summary>", mechanism_card)
                    self.assertNotIn(" open", opening_tag(mechanism_card))

    def test_compute_demand_future_section_is_basic_fundamental_expectation_audit(self):
        html = REPORT.read_text(encoding="utf-8")
        compute_first_question = bom_question_cards(html)[0]
        future_section = section_between(
            compute_first_question,
            "bom-step-future",
            "bom-step-mechanism",
        )

        self.assertIn('class="bom-future-card bom-expectation-card"', future_section)
        expected_cards = [
            "需求侧预期",
            "客户预算预期",
            "系统交付预期",
            "GPU / ASIC 供应商预期",
            "第三方行业预期",
        ]
        for card_title in expected_cards:
            with self.subTest(card_title=card_title):
                self.assertIn(card_title, future_section)

        expected_labels = [
            "预期来源",
            "对应逻辑环节",
            "对应 metric",
            "预期性质",
            "时间范围",
            "可信度",
            "后续验证点",
        ]
        for label in expected_labels:
            with self.subTest(label=label):
                self.assertIn(label, future_section)

        expected_metrics = [
            "ChatGPT weekly active users",
            "Microsoft Commercial RPO",
            "Dell AI-optimized server ending backlog",
            "NVIDIA Data Center revenue",
            "Broadcom AI semiconductor revenue",
            "Omdia",
        ]
        for metric in expected_metrics:
            with self.subTest(metric=metric):
                self.assertIn(metric, future_section)

        pricing_terms = ["估值", "定价", "EV/Sales", "priced-in", "reverse DCF"]
        for term in pricing_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, future_section)

    def test_s_curve_stage_card_appears_only_after_all_seven_questions(self):
        html = REPORT.read_text(encoding="utf-8")
        modules = bom_research_modules(html)

        self.assertGreaterEqual(len(modules), 6)
        for index, module in enumerate(modules, start=1):
            with self.subTest(module=index):
                question_cards = details_blocks_by_class(module, "bom-question-card")
                stage_cards = details_blocks_by_class(module, "bom-s-curve-stage-card")
                self.assertEqual(len(question_cards), 7)
                self.assertEqual(len(stage_cards), 1)
                self.assertIn("<summary>", stage_cards[0])
                self.assertIn('class="chevron"', stage_cards[0])
                self.assertNotIn(" open", opening_tag(stage_cards[0]))
                self.assertGreater(
                    module.index('class="bom-s-curve-stage-card"'),
                    module.rindex('class="bom-question-card"'),
                )

    def test_s_curve_stage_card_uses_seven_question_rollup_schema(self):
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
        metrics_section = section_between(
            compute_first_question,
            "bom-step-metrics",
            "bom-step-history",
        )

        expected_metrics = [
            "ChatGPT weekly active users (WAU)",
            "Microsoft commercial remaining performance obligation (Commercial RPO, $B)",
            "Dell AI-optimized server ending backlog ($B)",
            "NVIDIA Data Center segment revenue ($B)",
            "Broadcom AI semiconductor revenue ($B)",
            "Public GPU-hours consumed by AI workloads (GPU-hours)",
        ]
        for metric in expected_metrics:
            with self.subTest(metric=metric):
                self.assertIn(metric, metrics_section)

        expected_definitions = [
            "主体：Microsoft；字段：Commercial remaining performance obligation",
            "主体：Dell；字段：AI-optimized server ending backlog",
            "主体：NVIDIA；字段：Data Center segment revenue",
            "主体：Broadcom；字段：AI semiconductor revenue",
        ]
        for definition in expected_definitions:
            with self.subTest(definition=definition):
                self.assertIn(definition, metrics_section)

        vague_metric_names = [
            "ChatGPT / Gemini 使用量与 token 工作负载锚点",
            "Hyperscaler AI budget and committed demand",
            "Dell AI-optimized server order-to-revenue funnel",
            "Broadcom AI semiconductor revenue checkpoints",
            "tokens / GPU hours / utilization / AI ROI direct series",
        ]
        for vague_metric in vague_metric_names:
            with self.subTest(vague_metric=vague_metric):
                self.assertNotIn(vague_metric, metrics_section)

    def test_compute_demand_history_keeps_broadcom_guidance_out_of_actual_curve(self):
        html = REPORT.read_text(encoding="utf-8")
        compute_first_question = bom_question_cards(html)[0]
        history_section = section_between(
            compute_first_question,
            "bom-step-history",
            "bom-step-future",
        )
        broadcom_cards = [
            card
            for card in details_blocks_by_class(history_section, "bom-logic-stage-card")
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
