import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from value_invest_research.adapters.outbound.filesystem_temporal_research import (
    FileSystemTemporalResearchLedgerRepository,
)

from value_invest_research.domain.temporal_research import (
    build_temporal_research_bundle,
    validate_temporal_research_bundle,
)


def questions(conclusion="当前结论"):
    return [
        {
            "question_number": number,
            "question_id": f"memory_q{number}",
            "question": f"问题{number}",
            "conclusion": conclusion,
            "conclusion_strength": "中",
            "target_impact": "保持观察",
            "source_ids": ["SRC-1"],
        }
        for number in range(1, 7)
    ]


def sources():
    return [
        {
            "source_id": "SRC-1",
            "title": "示例公司指引",
            "source_bucket": "evidence",
            "source_visible_at": "2025-05-10",
            "summary": "公司披露了新的需求与供给信息。",
        },
        {
            "source_id": "SRC-UNMAPPED",
            "title": "新主题材料",
            "source_bucket": "research_report",
            "source_visible_at": "2025-05-12",
            "summary": "出现了初始理解思路没有覆盖的新机制。",
        },
    ]


class TemporalResearchTests(unittest.TestCase):
    def test_builds_six_question_baseline_without_inventing_prior_view(self):
        bundle = build_temporal_research_bundle(
            node_id="memory",
            as_of_date="2025-06-30",
            questions=questions(),
            sources=sources(),
        )

        self.assertEqual(len(bundle["snapshot"]["questions"]), 6)
        self.assertEqual(
            bundle["snapshot"]["questions"][0]["change_state"],
            "baseline_no_prior_snapshot",
        )
        self.assertEqual(bundle["revisions"][0]["revision_type"], "baseline")
        self.assertEqual(bundle["unmapped_sources"][0]["source_id"], "SRC-UNMAPPED")
        self.assertTrue(validate_temporal_research_bundle(bundle)["ok"])

    def test_atomic_claim_keeps_logic_and_four_time_dimensions(self):
        bundle = build_temporal_research_bundle(
            node_id="memory",
            as_of_date="2025-06-30",
            questions=questions(),
            sources=sources(),
            claims=[
                {
                    "source_id": "SRC-1",
                    "question_number": 2,
                    "statement": "有效供给释放时间晚于需求。",
                    "claim_type": "forecast",
                    "stance": "support",
                    "published_at": "2025-05-10",
                    "effective_period": "2025Q1",
                    "target_period": "2026",
                    "ingested_at": "2025-05-11",
                    "topic_tags": ["有效产能"],
                }
            ],
        )

        claim = bundle["claims"][0]
        self.assertEqual(claim["bom_node_id"], "memory")
        self.assertEqual(claim["question_number"], 2)
        self.assertEqual(claim["published_at"], "2025-05-10")
        self.assertEqual(claim["effective_period"], "2025Q1")
        self.assertEqual(claim["target_period"], "2026")
        self.assertEqual(claim["ingested_at"], "2025-05-11")

    def test_prior_snapshot_creates_real_changed_revision(self):
        prior = {
            "as_of_date": "2025-03-31",
            "questions": [
                {
                    "question_number": number,
                    "conclusion": "旧结论",
                    "conclusion_strength": "低",
                }
                for number in range(1, 7)
            ],
        }
        bundle = build_temporal_research_bundle(
            node_id="memory",
            as_of_date="2025-06-30",
            questions=questions("新结论"),
            sources=sources(),
            prior_snapshots=[prior],
        )

        self.assertEqual(bundle["snapshot"]["questions"][0]["change_state"], "changed")
        self.assertEqual(bundle["revisions"][0]["previous_conclusion"], "旧结论")

    def test_rejects_post_cutoff_claim(self):
        bundle = build_temporal_research_bundle(
            node_id="memory",
            as_of_date="2025-06-30",
            questions=questions(),
            sources=sources(),
        )
        bundle["claims"][0]["published_at"] = "2025-07-01"

        result = validate_temporal_research_bundle(bundle)

        self.assertFalse(result["ok"])
        self.assertIn("post_cutoff_claim", {issue["code"] for issue in result["issues"]})

    def test_filesystem_ledger_preserves_prior_claims_and_snapshots(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            repository = FileSystemTemporalResearchLedgerRepository(project_dir)
            first = build_temporal_research_bundle(
                node_id="memory",
                as_of_date="2025-06-30",
                questions=questions("第一截面"),
                sources=sources(),
            )
            repository.write_temporal_bundle(first)
            second_sources = [
                *sources(),
                {
                    "source_id": "SRC-2",
                    "title": "后续公司指引",
                    "source_bucket": "evidence",
                    "source_visible_at": "2025-08-10",
                    "summary": "公司更新了下一阶段指引。",
                },
            ]
            second = build_temporal_research_bundle(
                node_id="memory",
                as_of_date="2025-09-30",
                questions=[
                    {**row, "source_ids": ["SRC-2"], "conclusion": "第二截面"}
                    for row in questions()
                ],
                sources=second_sources,
                prior_snapshots=repository.load_prior_snapshots(),
            )
            repository.write_temporal_bundle(second)

            claim_rows = [
                json.loads(line)
                for line in (project_dir / "ledger" / "claims.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            snapshots = repository.load_prior_snapshots()
            coverage_rows = [
                json.loads(line)
                for line in (project_dir / "ledger" / "coverage.jsonl").read_text(encoding="utf-8").splitlines()
            ]

            self.assertEqual({row["source_id"] for row in claim_rows}, {"SRC-1", "SRC-2"})
            self.assertEqual([row["as_of_date"] for row in snapshots], ["2025-06-30", "2025-09-30"])
            self.assertEqual(len(coverage_rows), 12)
            self.assertEqual(second["snapshot"]["questions"][0]["change_state"], "changed")


if __name__ == "__main__":
    unittest.main()
