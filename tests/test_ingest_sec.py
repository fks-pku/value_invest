import json
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from tests.helpers import project_tmp_dir
from value_invest_research.ingest_sec import SecEdgarClient


class SecEdgarClientTests(unittest.TestCase):
    def test_build_cik_map_from_company_tickers(self):
        client = SecEdgarClient(user_agent="Test/1.0")
        sample = json.dumps(
            {"0": {"cik_str": "0000320193", "ticker": "AAPL", "title": "Apple Inc."}}
        ).encode()
        with patch("value_invest_research.ingest_sec.urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = sample
            mock_response.__enter__ = lambda s: s
            mock_response.__exit__ = MagicMock(return_value=False)
            mock_urlopen.return_value = mock_response

            cik_map = client.fetch_cik_map()
            self.assertEqual(cik_map["AAPL"], "0000320193")

    def test_fetch_submissions_stores_raw_and_structured(self):
        with project_tmp_dir() as root:
            stock_dir = root / "stocks" / "AAPL"
            (stock_dir / "raw" / "sec").mkdir(parents=True)
            (stock_dir / "data").mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)

            submissions = {
                "name": "Apple Inc.",
                "ticker": "AAPL",
                "filings": {
                    "recent": {
                        "accessionNumber": ["0001"],
                        "filingDate": ["2026-04-15"],
                        "form": ["10-Q"],
                        "primaryDocument": ["aapl-20260415.htm"],
                        "primaryDocDescription": ["10-Q"],
                    }
                },
            }

            client = SecEdgarClient(user_agent="Test/1.0")
            with patch.object(client, "_fetch_bytes", return_value=json.dumps(submissions).encode()):
                with patch.object(client, "_fetch_json", return_value=submissions):
                    result = client.fetch_submissions(root, "AAPL", "0000320193")

            self.assertTrue((stock_dir / "raw" / "sec" / "submissions.json").exists())
            self.assertEqual(result["name"], "Apple Inc.")


if __name__ == "__main__":
    unittest.main()
