import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from tests.helpers import project_tmp_dir
from value_invest_research.memo_updater import MemoUpdater, _build_system_prompt, _build_user_prompt, _load_stock_context


class MemoUpdaterTests(unittest.TestCase):
    def test_load_stock_context_reads_memo(self):
        with project_tmp_dir() as stock_dir:
            (stock_dir / "investment_memo.md").write_text("# AAPL Memo\nTest content", encoding="utf-8")
            (stock_dir / "data").mkdir()
            (stock_dir / "data" / "fundamentals.json").write_text("{}", encoding="utf-8")
            (stock_dir / "data" / "prices.csv").write_text("date,close\n2026-01-01,200\n", encoding="utf-8")

            context = _load_stock_context(stock_dir)
            self.assertIn("AAPL Memo", context["memo"])
            self.assertIn("2026-01-01", context["recent_prices"])

    def test_build_user_prompt_includes_key_sections(self):
        context = {"memo": "# Test Memo", "key_financial_metrics": {"Revenue": {"value": 100, "end": "2025-12-31", "form": "10-K"}}}
        prompt = _build_user_prompt("AAPL", context)
        self.assertIn("AAPL", prompt)
        self.assertIn("Revenue", prompt)
        self.assertIn("Stock Signal", prompt)
        self.assertIn("Foundation Baseline Impact", prompt)
        self.assertIn("foundation_status", prompt)
        self.assertIn("foundation_gaps", prompt)
        self.assertIn("3C", prompt)
        self.assertIn("3D", prompt)
        self.assertIn("5M", prompt)
        self.assertIn("3T", prompt)
        self.assertIn("dominant_driver", prompt)
        self.assertIn("disconfirming_tests", prompt)

    def test_system_prompt_uses_foundation_before_fenghe(self):
        prompt = _build_system_prompt()
        self.assertIn("Company Foundation Analysis Framework", prompt)
        self.assertIn("Eight Required Sections", prompt)
        self.assertIn("Risk sweep", prompt)
        self.assertIn("FengHe 3C3D5M3T Framework", prompt)
        self.assertIn("Cycle", prompt)
        self.assertIn("D1", prompt)
        self.assertIn("M1", prompt)
        self.assertIn("T1", prompt)

    def test_update_stock_memo_creates_proposal(self):
        with project_tmp_dir() as root:
            stock_dir = root / "stocks" / "AAPL"
            stock_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
            (stock_dir / "data").mkdir()
            (stock_dir / "investment_memo.md").write_text("# AAPL Memo", encoding="utf-8")
            (stock_dir / "evidence.jsonl").write_text("", encoding="utf-8")

            mock_client = MagicMock()
            mock_client.chat.return_value = "# Memo Update\n\nTest proposal content"

            updater = MemoUpdater(mock_client)
            result = updater.update_stock_memo(root, "AAPL")

            self.assertEqual(result["ticker"], "AAPL")
            self.assertIn("proposal_path", result)
            proposal_path = Path(result["proposal_path"])
            self.assertTrue(proposal_path.exists())
            self.assertIn("Test proposal content", proposal_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
