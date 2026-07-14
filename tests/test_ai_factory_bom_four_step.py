import json
import re
import unittest
from pathlib import Path


REPORT = Path("research/qa_projects/ai_factory_industry_scurve_timeslice_20260328/professional_report.html")
WORKBENCH = Path("research/qa_projects/ai_factory_industry_scurve_timeslice_20260328/investment_workbench.json")
PROJECT = Path("research/qa_projects/ai_factory_industry_scurve_timeslice_20260328/project.json")


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
                self.assertIn('<section class="bom-question-stage-flow">', card)
                self.assertIn("<h5>研究逻辑链</h5>", card)
                self.assertIn("Metric 历史与现状", card)
                self.assertIn("市场的未来预期", card)
                self.assertIn("第一性原理评估", card)
                self.assertIn("<h5>本问结论</h5>", card)
                self.assertIn("<h5>对标的推荐的影响</h5>", card)
                self.assertEqual(len(details_blocks_by_class(card, "bom-step-research-logic")), 1)
                self.assertNotIn("<h5>判断模型</h5>", card)
                self.assertNotIn("<h5>具体逻辑链条</h5>", card)
                self.assertNotIn("bom-step-model", card)
                self.assertNotIn("bom-step-logic", card)
                self.assertIn("bom-step-question-conclusion", card)
                self.assertIn("bom-step-target-impact", card)
                self.assertNotIn("<h5>整体的未来趋势评估</h5>", card)
                self.assertNotIn("bom-step-final-trend", card)
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
                    card.index('class="bom-step-card bom-step-research-logic"'),
                )

    def test_nested_bom_stage_cards_are_collapsible_by_default(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 36)
        for index, card in enumerate(cards, start=1):
            with self.subTest(card=index):
                for class_name in [
                    "bom-step-card",
                    "bom-step-research-logic",
                    "bom-stage-integrated-card",
                    "bom-stage-subcard",
                    "bom-mechanism-card",
                    "bom-step-question-conclusion",
                    "bom-step-target-impact",
                ]:
                    blocks = details_blocks_by_class(card, class_name)
                    self.assertGreaterEqual(len(blocks), 1)
                    for block in blocks:
                        self.assertIn("<summary>", block)
                        self.assertIn('class="chevron"', block)
                        self.assertNotIn(" open", opening_tag(block))

    def test_first_step_compiles_model_and_logic_chain_once(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 36)
        for index, card in enumerate(cards, start=1):
            question = re.search(r"<strong>(.*?)</strong>", card).group(1)
            logic_section = section_between(card, "bom-step-research-logic", "bom-stage-integrated-card")
            rows = re.findall(r'<tr class="bom-logic-chain-row">.*?</tr>', logic_section, flags=re.DOTALL)
            with self.subTest(card=index, question=question):
                self.assertIn("<h5>研究逻辑链</h5>", logic_section)
                self.assertIn("判断公式", logic_section)
                self.assertIn("整问结论规则", logic_section)
                self.assertIn("bom-logic-chain-table", logic_section)
                self.assertIn("<th>逻辑环节</th>", logic_section)
                self.assertIn("<th>为什么看</th>", logic_section)
                self.assertIn("<th>看什么</th>", logic_section)
                self.assertIn("<th>如何判定</th>", logic_section)
                self.assertNotIn("ChatGPT weekly active users", logic_section)
                self.assertNotIn("Microsoft commercial remaining performance obligation", logic_section)
                self.assertNotRegex(logic_section, r"metric-history-table|metric-trend-gap|bom-expectation-table|source-chip|<svg")
                self.assertGreaterEqual(len(rows), 4)
                self.assertLessEqual(len(rows), 7)

    def test_each_logic_row_has_one_integrated_stage_card(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 36)
        for index, card in enumerate(cards, start=1):
            logic_section = section_between(card, "bom-step-research-logic", "bom-stage-integrated-card")
            logic_rows = re.findall(r'<tr class="bom-logic-chain-row">.*?</tr>', logic_section, flags=re.DOTALL)
            stage_cards = details_blocks_by_class(card, "bom-stage-integrated-card")
            with self.subTest(card=index):
                self.assertEqual(len(stage_cards), len(logic_rows))
                for stage_index, stage_card in enumerate(stage_cards, start=1):
                    self.assertIn(f'<span class="stage-index">{stage_index + 1:02d}</span>', stage_card)
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
                    self.assertIn("<th>实际时间</th>", history_card)
                    self.assertIn("<th>数值</th>", history_card)
                    if "metric-history-name-gap" in history_card:
                        self.assertNotRegex(history_card, r'<span class="metric-history-name metric-history-name-gap"[^>]*href=')
                    else:
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
                    self.assertIn("<th>现状实际时间</th>", future_card)
                    self.assertIn("<th>指引期间</th>", future_card)
                    self.assertIn("<th>指引实际时间</th>", future_card)
                    self.assertIn("<th>预期 / 指引口径 / 数值</th>", future_card)
                    if '<td class="expectation-entity-cell">预期缺口</td>' in future_card:
                        self.assertNotIn('<td class="expectation-entity-cell"><a ', future_card)
                    else:
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

    def test_nested_metric_tables_keep_visible_horizontal_scroll(self):
        html = REPORT.read_text(encoding="utf-8")

        self.assertIn("scrollbar-gutter:stable", html)
        self.assertIn(".table-scroll::-webkit-scrollbar", html)
        self.assertIn("min-width:0;max-width:100%;box-sizing:border-box", html)
        self.assertIn(".metric-data-table,.metric-trend-gap{overflow:visible}", html)
        self.assertIn(".metric-history-table td strong{white-space:nowrap}", html)

    def test_compute_demand_question_keeps_history_expectation_and_mechanism_by_stage(self):
        html = REPORT.read_text(encoding="utf-8")
        compute_first_question = bom_question_cards(html)[0]

        expected_stage_titles = [
            "真实 AI 工作负载",
            "单任务计算强度",
            "客户算力资本承诺",
            "GPU/ASIC 与系统订单",
            "平台收入与市场价值",
        ]
        for title in expected_stage_titles:
            with self.subTest(title=title):
                self.assertIn(title, compute_first_question)

        expected_metrics = [
            "AI 用户、token 与企业任务量",
            "单任务 token、推理步骤与服务效率",
            "云厂 capex、RPO 与长期算力承诺",
            "AI server 订单、交付与 backlog",
            "GPU/ASIC 平台收入与 AI processor spending",
            "ChatGPT WAU 约100M",
            "Dell AI backlog约$9B",
            "Data Center $62.3B",
            "AI revenue $8.4B",
        ]
        for metric in expected_metrics:
            with self.subTest(metric=metric):
                self.assertIn(metric, compute_first_question)

        self.assertIn("AI 算力需求传导与弹性模型", compute_first_question)
        self.assertIn("主指标：AI 用户/调用/token/任务量", compute_first_question)

        expected_expectation_labels = [
            "公司 / 机构",
            "现状期间",
            "现状实际时间",
            "现状口径 / 数值",
            "指引期间",
            "指引实际时间",
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

        expected_calendar_mappings = [
            "2025-10至2025-12",
            "2025-11至2026-01",
            "2026-02至2026-04",
        ]
        for mapping in expected_calendar_mappings:
            with self.subTest(mapping=mapping):
                self.assertIn(mapping, compute_first_question)

    def test_question_conclusion_and_target_impact_close_after_stage_evidence(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = bom_question_cards(html)

        self.assertGreaterEqual(len(cards), 36)
        for index, card in enumerate(cards, start=1):
            with self.subTest(card=index):
                conclusion_cards = details_blocks_by_class(card, "bom-step-question-conclusion")
                target_impact_cards = details_blocks_by_class(card, "bom-step-target-impact")
                self.assertEqual(len(conclusion_cards), 1)
                self.assertEqual(len(target_impact_cards), 1)
                conclusion_card = conclusion_cards[0]
                target_impact_card = target_impact_cards[0]
                self.assertIn("<h5>本问结论</h5>", conclusion_card)
                self.assertIn("综合判断", conclusion_card)
                self.assertIn("支持机制", conclusion_card)
                self.assertIn("主要反证", conclusion_card)
                self.assertIn("结论强度", conclusion_card)
                self.assertIn("<h5>对标的推荐的影响</h5>", target_impact_card)
                self.assertIn("推荐含义", target_impact_card)
                self.assertGreater(
                    card.index('class="bom-step-card bom-step-question-conclusion"'),
                    card.rindex("bom-stage-integrated-card"),
                )
                self.assertGreater(
                    card.index('class="bom-step-card bom-step-target-impact"'),
                    card.index('class="bom-step-card bom-step-question-conclusion"'),
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
        self.assertIn("metric_candidate_plan", artifacts["BOM-SEARCH-compute_q1"])
        compute_first_question = bom_question_cards(html)[0]
        self.assertIn("AI 用户、token 与企业任务量", compute_first_question)
        self.assertIn("单任务 token、推理步骤与服务效率", compute_first_question)
        self.assertNotIn("待逐问搜索完成后判定", compute_first_question)

    def test_compute_module_uses_domain_run_and_preserves_valuation_gap(self):
        html = REPORT.read_text(encoding="utf-8")
        modules = [
            module
            for module in bom_research_modules(html)
            if "<h3>计算加速器 / GPU / ASIC</h3>" in module
        ]
        workbench = json.loads(WORKBENCH.read_text(encoding="utf-8"))
        artifacts = {
            item["question_number"]: item
            for item in workbench["bom_question_search_artifacts"]
            if item["bom_node_id"] == "compute"
        }

        self.assertEqual(len(modules), 1)
        module = modules[0]
        self.assertIn("计算加速器 / GPU / ASIC 研究主线", module)
        self.assertIn("AI 算力需求传导与弹性模型", module)
        self.assertIn("GPU/ASIC 合格供给漏斗模型", module)
        self.assertIn("平台控制权与替代速度模型", module)
        self.assertIn("市场隐含算力路径与预期差模型", module)
        self.assertNotIn("HBM 需求传导与含量弹性模型", module)

        self.assertEqual(set(artifacts), set(range(1, 7)))
        for question_number in [1, 2, 3, 4, 6]:
            with self.subTest(question=question_number):
                self.assertEqual(artifacts[question_number]["search_execution_status"], "completed")
                self.assertEqual(artifacts[question_number]["parser_status"], "gpt_verified_source_parse")
                self.assertTrue(artifacts[question_number]["evidence_summary"])
        self.assertEqual(artifacts[5]["parser_status"], "pending")
        self.assertFalse(artifacts[5]["evidence_summary"])
        self.assertEqual(
            set(artifacts[6]["refuting_source_ids"]),
            {
                "SRC-OMDIA-AI-PROCESSORS-20250828",
                "SRC-GOOGL-Q4-2025-CALL",
                "SRC-OMDIA-TPU-202412",
                "SRC-AMD-Q4-2025",
                "SRC-MSFT-FY26-Q2-CALL",
            },
        )

    def test_hbm_module_uses_the_domain_research_run_and_hbm_only_scope(self):
        html = REPORT.read_text(encoding="utf-8")
        modules = [module for module in bom_research_modules(html) if "<h3>HBM</h3>" in module]

        self.assertEqual(len(modules), 1)
        module = modules[0]
        self.assertIn("HBM 研究主线", module)
        self.assertIn("HBM 需求传导与含量弹性模型", module)
        self.assertIn("HBM 有效供给漏斗模型", module)
        self.assertIn("市场隐含 HBM 路径与预期差模型", module)
        self.assertIn("AI accelerator 数量", module)
        self.assertIn("单颗 accelerator 的 HBM 容量", module)
        self.assertIn("DRAM die 良率", module)
        self.assertNotIn("生产</span><p>HBM3E/HBM4、server DRAM、enterprise SSD", module)

    def test_hbm_search_artifacts_preserve_completed_research_and_valuation_gap(self):
        workbench = json.loads(WORKBENCH.read_text(encoding="utf-8"))
        artifacts = {
            item["question_number"]: item
            for item in workbench["bom_question_search_artifacts"]
            if item["bom_node_id"] == "memory"
        }

        self.assertEqual(set(artifacts), set(range(1, 7)))
        for question_number in [1, 2, 3, 4, 6]:
            with self.subTest(question=question_number):
                self.assertEqual(artifacts[question_number]["search_execution_status"], "completed")
                self.assertEqual(artifacts[question_number]["parser_status"], "gpt_verified_source_parse")
                self.assertTrue(artifacts[question_number]["evidence_summary"])
        self.assertEqual(artifacts[5]["parser_status"], "pending")
        self.assertFalse(artifacts[5]["evidence_summary"])
        self.assertEqual(
            set(artifacts[6]["refuting_source_ids"]),
            {"SRC-TF-HBM-BULLETIN-20260320", "SRC-SAMSUNG-HBM4-20260212"},
        )

    def test_compute_demand_question_uses_specific_primary_metric_per_stage(self):
        html = REPORT.read_text(encoding="utf-8")
        compute_first_question = bom_question_cards(html)[0]

        expected_definitions = [
            "主指标：AI 用户/调用/token/任务量",
            "主指标：每任务 token/步骤/推理时长",
            "主指标：AI/数据中心 capex 与 RPO/backlog",
            "主指标：accelerator/AI server orders 与 backlog",
            "主指标：Data Center/AI semiconductor revenue",
        ]
        for definition in expected_definitions:
            with self.subTest(definition=definition):
                self.assertIn(definition, compute_first_question)

        vague_metric_names = ["TAM headlines", "PC GPU share", "single generic demand proxy"]
        for vague_metric in vague_metric_names:
            with self.subTest(vague_metric=vague_metric):
                self.assertNotIn(vague_metric, compute_first_question)

    def test_compute_demand_history_keeps_broadcom_guidance_out_of_actual_curve(self):
        html = REPORT.read_text(encoding="utf-8")
        compute_first_question = bom_question_cards(html)[0]
        market_value_cards = [
            card
            for card in details_blocks_by_class(compute_first_question, "bom-stage-integrated-card")
            if "GPU/ASIC 平台收入与 AI processor spending" in card
        ]

        self.assertEqual(len(market_value_cards), 1)
        market_value_card = market_value_cards[0]
        history_cards = details_blocks_by_class(market_value_card, "bom-stage-history-card")
        future_cards = details_blocks_by_class(market_value_card, "bom-stage-future-card")
        self.assertEqual(len(history_cards), 1)
        self.assertEqual(len(future_cards), 1)
        self.assertIn("NVIDIA 2025-11至2026-01", history_cards[0])
        self.assertNotIn("$10.7B", history_cards[0])
        self.assertIn("$10.7B", future_cards[0])

    def test_every_selected_bom_source_has_a_question_specific_parse_record(self):
        workbench = json.loads(WORKBENCH.read_text(encoding="utf-8"))

        for artifact in workbench["bom_question_search_artifacts"]:
            with self.subTest(artifact=artifact["artifact_id"]):
                parsed_ids = {row["source_id"] for row in artifact["source_parse_records"]}
                self.assertEqual(parsed_ids, set(artifact["source_ids"]))
                for row in artifact["source_parse_records"]:
                    self.assertEqual(row["parser_status"], "completed")
                    self.assertTrue(row["question_dimensions"])

    def test_failed_research_gate_never_renders_actionable_state(self):
        workbench = json.loads(WORKBENCH.read_text(encoding="utf-8"))

        invalid = [
            target
            for target in workbench["scoring_worksheet"]
            if target["action_state"] == "actionable_long" and not target["research_gate"]["passed"]
        ]

        self.assertEqual(invalid, [])
        self.assertTrue(any(target["candidate_action_state"] == "actionable_long" for target in workbench["scoring_worksheet"]))
        self.assertTrue(all(target["thesis_node_id"] for target in workbench["scoring_worksheet"]))
        self.assertTrue(all(target["score"].get("weights") for target in workbench["scoring_worksheet"]))
        self.assertTrue(all(target["score"].get("dimension_weights") for target in workbench["scoring_worksheet"]))

    def test_public_report_keeps_four_sections_and_internal_plans_private(self):
        html = REPORT.read_text(encoding="utf-8")
        positions = [html.index(f'<section id="{section_id}"') for section_id in ["goal", "overview", "targets", "sources"]]

        self.assertEqual(positions, sorted(positions))
        for internal_term in ["source_universe_plan", "exa_search_plan", "direct_query", "search_query"]:
            self.assertNotIn(internal_term, html)

    def test_project_id_matches_the_historical_cutoff(self):
        project = json.loads(PROJECT.read_text(encoding="utf-8"))

        self.assertEqual(project["as_of_date"], "2026-03-28")
        self.assertTrue(project["project_id"].endswith("20260328"))


if __name__ == "__main__":
    unittest.main()
