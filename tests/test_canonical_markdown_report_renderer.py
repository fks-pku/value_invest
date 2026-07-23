import tempfile
import unittest
from pathlib import Path

from value_invest_research.adapters.outbound.canonical_markdown_report_renderer import (
    CanonicalMarkdownReportRenderer,
)
from value_invest_research.domain.report_view_model import ReportViewModel


class CanonicalMarkdownReportRendererTests(unittest.TestCase):
    def test_renders_locked_four_section_markdown(self):
        view_model = ReportViewModel(
            project={
                "project_id": "demo",
                "title": "演示研究",
                "run_mode": "historical_backtest",
                "as_of_date": "2026-03-28",
            },
            goal={
                "topic": "演示行业",
                "decision_boundary": "研究观察",
                "current_judgment": "产业逻辑待验证。",
                "biggest_uncertainty": "估值。",
            },
            supply_chain={"plain_summary": "产业链摘要。", "layers": []},
            qa_roots=[],
            targets=[],
            sources=[
                {
                    "source_id": "SRC-1",
                    "title": "官方材料",
                    "url": "https://example.com/source",
                    "source_bucket": "evidence",
                    "source_visible_at": "2026-01-01",
                    "summary": "用于验证。",
                }
            ],
        )

        renderer = CanonicalMarkdownReportRenderer()
        markdown = renderer.render(view_model)

        self.assertLess(markdown.index("## 1. 当前研究的问题"), markdown.index("## 2. 行业概况"))
        self.assertLess(markdown.index("## 2. 行业概况"), markdown.index("## 3. 标的推荐"))
        self.assertLess(markdown.index("## 3. 标的推荐"), markdown.index("## 4. 来源索引"))
        self.assertIn("[官方材料](https://example.com/source)", markdown)

        with tempfile.TemporaryDirectory() as tmp:
            result = renderer.write(Path(tmp), view_model)
            self.assertTrue(result["report_path"].endswith("professional_report.md"))
            self.assertTrue(Path(result["report_path"]).is_file())


if __name__ == "__main__":
    unittest.main()
