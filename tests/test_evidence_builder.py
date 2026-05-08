import json
import unittest
from pathlib import Path

from tests.helpers import project_tmp_dir
from value_invest_research.evidence_builder import build_stock_evidence
from value_invest_research.models import EvidenceRecord


class EvidenceBuilderTests(unittest.TestCase):
    def test_build_stock_evidence_from_sec_facts_and_prices(self):
        with project_tmp_dir() as root:
            stock_dir = root / "stocks" / "AAPL"
            data_dir = stock_dir / "data"
            data_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
            (stock_dir / "evidence.jsonl").write_text("", encoding="utf-8")

            sec_facts = {
                "cik": 320193,
                "facts": {
                    "us-gaap": {
                        "RevenueFromContractWithCustomerExcludingAssessedTax": {
                            "units": {
                                "USD": [
                                    {"val": 100, "end": "2025-12-31", "filed": "2026-01-31", "form": "10-Q"},
                                    {"val": 120, "end": "2026-03-31", "filed": "2026-04-30", "form": "10-Q"},
                                ]
                            }
                        },
                        "NetIncomeLoss": {
                            "units": {
                                "USD": [
                                    {"val": 20, "end": "2026-03-31", "filed": "2026-04-30", "form": "10-Q"}
                                ]
                            }
                        },
                    }
                },
            }
            (data_dir / "sec_facts.json").write_text(json.dumps(sec_facts), encoding="utf-8")
            (data_dir / "prices.csv").write_text(
                "date,Open,High,Low,Close,Volume\n"
                "2026-05-04,198,202,197,200,1000\n"
                "2026-05-05,200,205,199,204,2000\n",
                encoding="utf-8",
            )

            result = build_stock_evidence(root, "AAPL")

            self.assertEqual(result["ticker"], "AAPL")
            self.assertGreaterEqual(result["records_new"], 3)

            records = [
                EvidenceRecord.from_dict(json.loads(line))
                for line in (stock_dir / "evidence.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            ids = {record.id for record in records}
            self.assertIn("ev_aapl_sec_revenue_20260331", ids)
            self.assertIn("ev_aapl_sec_net_income_20260331", ids)
            self.assertIn("ev_aapl_price_20260505", ids)
            self.assertTrue(all(record.research_object == "stocks/AAPL" for record in records))

    def test_build_stock_evidence_is_idempotent(self):
        with project_tmp_dir() as root:
            stock_dir = root / "stocks" / "AAPL"
            data_dir = stock_dir / "data"
            data_dir.mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)
            (stock_dir / "evidence.jsonl").write_text("", encoding="utf-8")
            (data_dir / "prices.csv").write_text(
                "date,Close\n2026-05-04,200\n2026-05-05,204\n",
                encoding="utf-8",
            )

            first = build_stock_evidence(root, "AAPL")
            second = build_stock_evidence(root, "AAPL")

            self.assertEqual(first["records_new"], 1)
            self.assertEqual(second["records_new"], 0)
            lines = [line for line in (stock_dir / "evidence.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
            self.assertEqual(len(lines), 1)


if __name__ == "__main__":
    unittest.main()
