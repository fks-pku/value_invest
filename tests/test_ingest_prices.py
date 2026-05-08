import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from tests.helpers import project_tmp_dir
from value_invest_research.ingest_prices import fetch_price_history


class PriceIngestionTests(unittest.TestCase):
    def test_fetch_prices_stores_csv(self):
        with project_tmp_dir() as root:
            stock_dir = root / "stocks" / "AAPL"
            (stock_dir / "data").mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)

            mock_df = MagicMock()
            mock_df.empty = False
            mock_df.__len__ = lambda self_: 1

            def fake_to_csv(path):
                Path(path).write_text("date,Open,High,Low,Close,Volume\n2026-05-05,200.0,205.0,199.0,204.0,1000000\n", encoding="utf-8")

            mock_df.to_csv = fake_to_csv

            with patch("value_invest_research.ingest_prices.yf.Ticker") as mock_ticker_cls:
                mock_ticker = MagicMock()
                mock_ticker.history.return_value = mock_df
                mock_ticker_cls.return_value = mock_ticker

                fetch_price_history(root, "AAPL", period="1mo")

            csv_path = stock_dir / "data" / "prices.csv"
            self.assertTrue(csv_path.exists())
            self.assertIn("2026-05-05", csv_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
