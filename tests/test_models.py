import unittest

from value_invest_research.models import (
    EvidenceRecord,
    SignalDriver,
    StockSignal,
    ValidationError,
)


class EvidenceRecordTests(unittest.TestCase):
    def test_valid_evidence_round_trips_to_dict(self):
        record = EvidenceRecord.from_dict(
            {
                "id": "ev_20260506_aapl_10q_001",
                "research_object": "stocks/AAPL",
                "source_type": "sec_filing",
                "source_name": "10-Q",
                "url": "https://www.sec.gov/example",
                "published_at": "2026-05-01T00:00:00Z",
                "fetched_at": "2026-05-06T08:00:00Z",
                "hash": "sha256:abc123",
                "tickers": ["AAPL"],
                "sectors": ["technology_hardware"],
                "themes": ["services_growth"],
                "summary": "Revenue and margin facts extracted from a filing.",
                "reliability": "primary",
                "materiality": "medium",
                "used_in": ["investment_memo.md"],
            }
        )

        self.assertEqual(record.to_dict()["id"], "ev_20260506_aapl_10q_001")
        self.assertEqual(record.to_dict()["tickers"], ["AAPL"])

    def test_rejects_low_reliability_thesis_change(self):
        with self.assertRaisesRegex(ValidationError, "low-reliability"):
            EvidenceRecord.from_dict(
                {
                    "id": "ev_20260506_aapl_rumor_001",
                    "research_object": "stocks/AAPL",
                    "source_type": "social_media",
                    "source_name": "Unattributed post",
                    "url": "https://example.com/rumor",
                    "published_at": None,
                    "fetched_at": "2026-05-06T08:00:00Z",
                    "hash": "sha256:def456",
                    "tickers": ["AAPL"],
                    "sectors": [],
                    "themes": [],
                    "summary": "Unverified claim.",
                    "reliability": "low",
                    "materiality": "thesis_change",
                    "used_in": [],
                }
            )

    def test_requires_material_claims_to_have_evidence(self):
        with self.assertRaisesRegex(ValidationError, "evidence_id"):
            StockSignal(
                ticker="AAPL",
                date="2026-05-06",
                view="watch",
                confidence="medium",
                signal_strength=2,
                time_horizon="long_term",
                changed_since_last_run=True,
                drivers=[SignalDriver(type="positive", item="FCF durability improved", evidence_id="")],
                action_for_human=["Review valuation assumptions"],
            ).validate()


if __name__ == "__main__":
    unittest.main()
