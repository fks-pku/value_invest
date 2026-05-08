import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

from tests.helpers import project_tmp_dir
from value_invest_research.cli import main


class CliTests(unittest.TestCase):
    def test_init_stock_command(self):
        with project_tmp_dir() as tmp:
            with redirect_stdout(StringIO()):
                exit_code = main(["--root", str(tmp), "init-stock", "MSFT", "--company-name", "Microsoft Corporation"])
            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmp) / "stocks" / "MSFT" / "investment_memo.md").exists())

    def test_init_event_command(self):
        with project_tmp_dir() as tmp:
            with redirect_stdout(StringIO()):
                exit_code = main(["--root", str(tmp), "init-event", "2026-05-06", "US Iran Conflict"])
            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmp) / "research" / "events" / "2026-05-06_us_iran_conflict").exists())

    def test_research_stock_command_prints_report_path(self):
        with project_tmp_dir() as tmp:
            result = {
                "ticker": "AAPL",
                "report_path": str(Path(tmp) / "stocks" / "AAPL" / "research_reports" / "report.md"),
                "signal_path": str(Path(tmp) / "stocks" / "AAPL" / "research_reports" / "signal.json"),
                "response_length": 100,
            }
            mock_researcher = MagicMock()
            mock_researcher.run_stock_research.return_value = result

            with patch("value_invest_research.cli._get_llm_client", return_value=MagicMock()):
                with patch("value_invest_research.stock_researcher.StockResearcher", return_value=mock_researcher):
                    out = StringIO()
                    with redirect_stdout(out):
                        exit_code = main(["--root", str(tmp), "research-stock", "AAPL", "--api-key", "test"])

            self.assertEqual(exit_code, 0)
            self.assertIn("Stock research saved", out.getvalue())
            self.assertIn("signal.json", out.getvalue())

    def test_build_evidence_command_prints_record_counts(self):
        with project_tmp_dir() as tmp:
            stock_dir = Path(tmp) / "stocks" / "AAPL"
            data_dir = stock_dir / "data"
            data_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
            (stock_dir / "evidence.jsonl").write_text("", encoding="utf-8")
            (data_dir / "prices.csv").write_text("date,Close\n2026-05-05,204\n", encoding="utf-8")

            out = StringIO()
            with redirect_stdout(out):
                exit_code = main(["--root", str(tmp), "build-evidence", "AAPL"])

            self.assertEqual(exit_code, 0)
            self.assertIn("Evidence built for AAPL", out.getvalue())
            self.assertIn("records_new", out.getvalue())


if __name__ == "__main__":
    unittest.main()
