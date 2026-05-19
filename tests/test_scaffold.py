import unittest
from pathlib import Path

from tests.helpers import project_tmp_dir
from value_invest_research.scaffold import init_event, init_stock, slugify


class ScaffoldTests(unittest.TestCase):
    def test_slugify_normalizes_event_names(self):
        self.assertEqual(slugify("US / Iran Conflict!"), "us_iran_conflict")

    def test_init_stock_creates_required_files(self):
        with project_tmp_dir() as root:
            init_stock(root, "aapl", "Apple Inc.")

            stock_dir = root / "stocks" / "AAPL"
            self.assertTrue((stock_dir / "investment_memo.md").exists())
            self.assertTrue((stock_dir / "evidence.jsonl").exists())
            self.assertTrue((stock_dir / "data" / "fundamentals.json").exists())
            memo = (stock_dir / "investment_memo.md").read_text(encoding="utf-8")
            self.assertIn("Apple Inc.", (stock_dir / "company_profile.md").read_text(encoding="utf-8"))
            self.assertIn("Company Foundation Analysis", memo)
            self.assertIn("Source And Origin", memo)
            self.assertIn("Current Business", memo)
            self.assertIn("Value Chain Position", memo)
            self.assertIn("Competitive Landscape", memo)
            self.assertIn("Risk Sweep", memo)
            self.assertIn("FengHe Message-Flow Analysis", memo)
            self.assertIn("3C: Cycle, Change, Certainty", memo)
            self.assertIn("3D Price Drivers", memo)
            self.assertIn("5M Change Map", memo)
            self.assertIn("3T Time Frame", memo)

    def test_init_event_creates_required_files(self):
        with project_tmp_dir() as root:
            event_dir = init_event(root, "2026-05-06", "US Iran Conflict")

            self.assertEqual(event_dir.name, "2026-05-06_us_iran_conflict")
            self.assertTrue((event_dir / "event_brief.md").exists())
            self.assertTrue((event_dir / "candidate_screen.md").exists())
            self.assertTrue((event_dir / "tickers_to_review.yaml").exists())


if __name__ == "__main__":
    unittest.main()
