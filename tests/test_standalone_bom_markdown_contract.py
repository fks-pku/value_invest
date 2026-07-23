import unittest

from value_invest_research.framework_contracts import validate_report_contract_markdown


def _report(*, reverse_dates: bool = True) -> str:
    dates = ("2026-03-01", "2025-12-01") if reverse_dates else ("2025-12-01", "2026-03-01")
    sections = []
    for index, title in enumerate(("需求侧", "供给侧", "技术侧", "估值侧", "ESG"), start=1):
        sections.append(
            "\n".join(
                [
                    f"## {index}. {title}",
                    "",
                    "### 简单逻辑链",
                    "",
                    "逻辑。",
                    "",
                    "### 信息时间线",
                    "",
                    "| 时间 | 信息类型 | 来源及原文位置 | 内容简介 |",
                    "|---|---|---|---|",
                    f"| {dates[0]} | 官方财报 | [来源](https://example.com/{index}/a) Item 1 | 事实。 |",
                    f"| {dates[1]} | 第三方权威 | [来源](https://example.com/{index}/b) 第 2 页 | 观点。 |",
                    "",
                    "### 最新结论与趋势",
                    "",
                    "结论。",
                ]
            )
        )
    return "\n".join(
        [
            "---",
            "report_scope: standalone-bom",
            "bom_node_id: gpu_asic",
            "---",
            "",
            "# GPU / ASIC",
            "",
            *sections,
        ]
    )


class StandaloneBomMarkdownContractTests(unittest.TestCase):
    def test_accepts_five_lens_reverse_chronological_report(self):
        result = validate_report_contract_markdown(_report())
        self.assertTrue(result["ok"], result["issues"])
        self.assertEqual(result["summary"]["report_scope"], "standalone-bom")
        self.assertEqual(result["summary"]["level1_cards"], 5)

    def test_rejects_oldest_to_newest_timeline(self):
        result = validate_report_contract_markdown(_report(reverse_dates=False))
        self.assertFalse(result["ok"])
        self.assertIn(
            "markdown_standalone_bom_timeline_order",
            {issue["code"] for issue in result["issues"]},
        )


if __name__ == "__main__":
    unittest.main()
