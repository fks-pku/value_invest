import json
import re
import unittest
from pathlib import Path


PROJECT_DIR = Path("research/bom/ai_factory_industry_scurve_timeslice_20260328")
INDUSTRY_REPORT = PROJECT_DIR / "professional_report.html"
INDUSTRY_MARKDOWN = PROJECT_DIR / "professional_report.md"
BOM_NODE_IDS = ["compute", "manufacturing", "memory", "network", "powerCooling", "system"]
BOM_REPORTS = [PROJECT_DIR / "boms" / node_id / "professional_report.html" for node_id in BOM_NODE_IDS]
BOM_MARKDOWN_REPORTS = [PROJECT_DIR / "boms" / node_id / "professional_report.md" for node_id in BOM_NODE_IDS]
WORKBENCH = PROJECT_DIR / "investment_workbench.json"
PROJECT = PROJECT_DIR / "project.json"


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


@unittest.skipUnless(
    PROJECT.is_file(),
    "legacy AI factory static fixture is not part of the BOM-only workspace",
)
class AiFactoryTemporalBomTests(unittest.TestCase):
    def test_markdown_is_canonical_parent_and_child_report(self):
        parent = INDUSTRY_MARKDOWN.read_text(encoding="utf-8")

        self.assertIn("report_scope: industry-index", parent)
        self.assertEqual(
            re.findall(r"^## [1-4]\. .+$", parent, flags=re.MULTILINE),
            [
                "## 1. 当前研究的问题",
                "## 2. 行业概况",
                "## 3. 标的推荐",
                "## 4. 来源索引",
            ],
        )
        for node_id, report_path in zip(BOM_NODE_IDS, BOM_MARKDOWN_REPORTS):
            with self.subTest(node_id=node_id):
                self.assertTrue(report_path.is_file())
                self.assertIn(f"(boms/{node_id}/professional_report.md)", parent)
                child = report_path.read_text(encoding="utf-8")
                self.assertIn("report_scope: bom-node", child)
                self.assertIn(f"bom_node_id: {node_id}", child)
                self.assertEqual(len(re.findall(r"^### Q[1-6] · ", child, flags=re.MULTILINE)), 6)
                for label in (
                    "#### 基本理解思路",
                    "#### 当前结论",
                    "#### 相较上一截面的变化",
                    "#### 时间演化",
                    "#### 映射材料",
                    "#### 信息覆盖",
                ):
                    self.assertEqual(child.count(label), 6)
                self.assertRegex(child, r"\[[^\]]+\]\(https?://[^)]+\)")

    def test_parent_report_is_navigation_only_and_children_own_research(self):
        parent_html = INDUSTRY_REPORT.read_text(encoding="utf-8")

        self.assertIn('data-report-scope="industry-index"', parent_html)
        self.assertEqual(parent_html.count('class="bom-index-card"'), len(BOM_NODE_IDS))
        self.assertNotIn('class="industry-module bom-research-module"', parent_html)
        self.assertNotIn('class="bom-question-card"', parent_html)
        for node_id, report_path in zip(BOM_NODE_IDS, BOM_REPORTS):
            with self.subTest(node_id=node_id):
                self.assertTrue(report_path.is_file())
                self.assertIn(f'href="boms/{node_id}/professional_report.html"', parent_html)
                child_html = report_path.read_text(encoding="utf-8")
                self.assertIn('data-report-scope="bom-node"', child_html)
                self.assertIn(f'data-bom-node-id="{node_id}"', child_html)
                self.assertEqual(len(bom_question_cards(child_html)), 6)
                self.assertIn('class="project-back-link" href="../../professional_report.html"', child_html)

    def test_every_bom_child_owns_temporal_ledger_and_snapshot(self):
        project = json.loads(PROJECT.read_text(encoding="utf-8"))
        manifest = json.loads((PROJECT_DIR / "boms" / "manifest.json").read_text(encoding="utf-8"))

        self.assertEqual([node["node_id"] for node in manifest["nodes"]], BOM_NODE_IDS)
        for node in manifest["nodes"]:
            child_dir = PROJECT_DIR / node["directory"]
            child = json.loads((child_dir / "project.json").read_text(encoding="utf-8"))
            temporal_manifest = json.loads((child_dir / "temporal_manifest.json").read_text(encoding="utf-8"))
            with self.subTest(node_id=node["node_id"]):
                self.assertEqual(child["parent_project_id"], project["project_id"])
                self.assertEqual(child["evidence_ledger_path"], "ledger/claims.jsonl")
                self.assertTrue((child_dir / "ledger" / "documents.jsonl").is_file())
                self.assertTrue((child_dir / "ledger" / "claims.jsonl").is_file())
                self.assertTrue((child_dir / "ledger" / "thesis_revisions.jsonl").is_file())
                self.assertTrue((child_dir / "ledger" / "coverage.jsonl").is_file())
                self.assertEqual(temporal_manifest["node_id"], node["node_id"])
                self.assertTrue((child_dir / temporal_manifest["current_snapshot_path"]).is_file())

    def test_six_questions_use_temporal_sequence_without_fixed_stage_cards(self):
        for report_path in BOM_REPORTS:
            html = report_path.read_text(encoding="utf-8")
            cards = bom_question_cards(html)
            self.assertEqual(len(cards), 6)
            for index, card in enumerate(cards, start=1):
                with self.subTest(report=report_path.name, question=index):
                    self.assertIn("基本理解思路", card)
                    self.assertIn("当前结论", card)
                    self.assertIn("相较上一截面的变化", card)
                    self.assertIn("时间演化", card)
                    self.assertIn("映射材料", card)
                    self.assertIn("信息覆盖", card)
                    self.assertEqual(len(details_blocks_by_class(card, "bom-question-understanding")), 1)
                    self.assertEqual(card.count('class="bom-question-current"'), 1)
                    self.assertEqual(len(details_blocks_by_class(card, "bom-question-change")), 1)
                    self.assertEqual(len(details_blocks_by_class(card, "bom-question-timeline")), 1)
                    self.assertEqual(len(details_blocks_by_class(card, "bom-question-materials")), 1)
                    self.assertEqual(len(details_blocks_by_class(card, "bom-question-coverage")), 1)
                    self.assertNotIn("bom-stage-integrated-card", card)
                    self.assertNotIn("bom-step-research-logic", card)
                    self.assertNotIn("bom-question-research-status", card)

    def test_logic_hint_is_explicitly_not_an_evidence_whitelist(self):
        compute_html = BOM_REPORTS[0].read_text(encoding="utf-8")
        first_question = bom_question_cards(compute_html)[0]

        self.assertIn("大致判断公式", first_question)
        self.assertIn("理解提示", first_question)
        self.assertIn("不是材料准入清单", first_question)
        self.assertNotIn("<th>逻辑环节</th>", first_question)

    def test_current_snapshot_is_visible_and_no_history_is_invented(self):
        for report_path in BOM_REPORTS:
            html = report_path.read_text(encoding="utf-8")
            with self.subTest(report=report_path):
                self.assertIn("这是时间账本的基线快照", html)
                self.assertIn("此前未保存结构化研究快照", html)
                self.assertIn("无历史快照", html)

    def test_mapped_materials_are_chronological_and_claim_near_linked(self):
        compute_html = BOM_REPORTS[0].read_text(encoding="utf-8")
        first_question = bom_question_cards(compute_html)[0]

        self.assertIn('class="bom-material-timeline"', first_question)
        self.assertIn('class="table-scroll bom-mapped-material-table"', first_question)
        self.assertIn("<th>发布时间</th>", first_question)
        self.assertIn("<th>材料</th>", first_question)
        self.assertIn("<th>类型 / 立场</th>", first_question)
        self.assertIn("<th>实际期间</th>", first_question)
        self.assertIn("<th>预测期间</th>", first_question)
        self.assertRegex(first_question, r'<td><a href="https?://')

    def test_coverage_is_question_level_and_keeps_counterevidence_visible(self):
        compute_html = BOM_REPORTS[0].read_text(encoding="utf-8")
        cards = bom_question_cards(compute_html)

        for card in cards:
            self.assertIn('class="bom-coverage-status"', card)
            self.assertIn("事实", card)
            self.assertIn("预测", card)
            self.assertIn("估值", card)
            self.assertIn("反证", card)
            self.assertIn("支持材料", card)
            self.assertIn("反向材料", card)

    def test_s_curve_rollup_remains_after_six_questions(self):
        for report_path in BOM_REPORTS:
            html = report_path.read_text(encoding="utf-8")
            question_cards = bom_question_cards(html)
            stage_cards = details_blocks_by_class(html, "bom-s-curve-stage-card")
            with self.subTest(report=report_path):
                self.assertEqual(len(stage_cards), 1)
                self.assertGreater(html.index('class="bom-s-curve-stage-card"'), html.rindex('class="bom-question-card"'))

    def test_workbench_preserves_search_artifacts_but_public_report_hides_process(self):
        workbench = json.loads(WORKBENCH.read_text(encoding="utf-8"))
        self.assertIn("bom_question_search_artifacts", workbench)
        self.assertIn("append_only_temporal_claim_ledger", workbench["bom_stage_rollup_policy"]["workflow_order"])
        for report_path in BOM_REPORTS:
            html = report_path.read_text(encoding="utf-8")
            self.assertNotIn("Exa", html)
            self.assertNotIn("source_universe_plan", html)
            self.assertNotIn("metric_candidate_plan", html)

    def test_wide_temporal_tables_keep_local_scroll(self):
        html = BOM_REPORTS[0].read_text(encoding="utf-8")

        self.assertIn("scrollbar-gutter:stable", html)
        self.assertIn(".bom-mapped-material-table table{min-width:1100px}", html)
        self.assertIn('class="table-scroll bom-mapped-material-table"', html)


if __name__ == "__main__":
    unittest.main()
