import json
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from tests.helpers import project_tmp_dir
from value_invest_research.stock_researcher import (
    StockResearcher,
    _build_user_prompt,
    _extract_signal_json,
)


class StockResearcherTests(unittest.TestCase):
    def test_build_user_prompt_requires_foundation_first_output(self):
        context = {
            "memo": "# AAPL Memo",
            "key_financial_metrics": {
                "Revenue": {"value": 100, "end": "2025-12-31", "form": "10-K"},
            },
        }

        prompt = _build_user_prompt("AAPL", context)

        self.assertIn("Foundation-First Stock Research", prompt)
        self.assertIn("Company foundation analysis", prompt)
        self.assertIn("source/origin", prompt)
        self.assertIn("value chain position", prompt)
        self.assertIn("competitive landscape", prompt)
        self.assertIn("organization/culture/governance", prompt)
        self.assertIn("risk sweep", prompt)
        self.assertIn("foundation_status", prompt)
        self.assertIn("foundation_gaps", prompt)
        self.assertIn("3C", prompt)
        self.assertIn("3D", prompt)
        self.assertIn("5M", prompt)
        self.assertIn("3T", prompt)
        self.assertIn("stock_research_signal", prompt)
        self.assertIn("dominant_driver", prompt)
        self.assertIn("disconfirming_tests", prompt)

    def test_extract_signal_json_from_markdown_block(self):
        text = """# Report

```json
{"ticker": "AAPL", "dominant_driver": "D1", "time_frame": "T2"}
```
"""
        signal = _extract_signal_json(text)
        self.assertEqual(signal["ticker"], "AAPL")
        self.assertEqual(signal["dominant_driver"], "D1")

    def test_run_stock_research_writes_report_and_signal(self):
        with project_tmp_dir() as root:
            stock_dir = root / "stocks" / "AAPL"
            stock_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
            (stock_dir / "data").mkdir()
            (stock_dir / "investment_memo.md").write_text("# AAPL Memo", encoding="utf-8")
            (stock_dir / "evidence.jsonl").write_text("", encoding="utf-8")

            mock_client = MagicMock()
            mock_client.chat.return_value = """# AAPL Foundation-First Research

## Company Foundation

```json
{
  "ticker": "AAPL",
  "foundation_status": "complete",
  "cycle_state": "mature cycle",
  "change_type": "mixed",
  "certainty_level": "medium",
  "dominant_driver": "D1",
  "time_frame": "T2",
  "disconfirming_tests": ["services margin weakens"]
}
```
"""

            researcher = StockResearcher(mock_client)
            result = researcher.run_stock_research(root, "AAPL")

            report_path = Path(result["report_path"])
            signal_path = Path(result["signal_path"])
            self.assertTrue(report_path.exists())
            self.assertTrue(signal_path.exists())
            self.assertTrue(report_path.name.endswith("_stock_research.md"))
            self.assertTrue(signal_path.name.endswith("_stock_signal.json"))
            self.assertIn("AAPL Foundation-First Research", report_path.read_text(encoding="utf-8"))
            signal = json.loads(signal_path.read_text(encoding="utf-8"))
            self.assertEqual(signal["dominant_driver"], "D1")
            self.assertEqual(signal["foundation_status"], "complete")


if __name__ == "__main__":
    unittest.main()
