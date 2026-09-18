"""Read-only checks for the empirical case and its append-only publication."""
from copy import deepcopy
import hashlib
import json
import unittest

from deepen_gpt6_cost_case import FOLDER, INPUT, calculate, materialize_tables
from gpt6_impact_research import PROJECT, read_lines


class CostCaseChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.revision = json.loads(INPUT.read_text())
        cls.calc = calculate(cls.revision)

    def test_premium_and_break_even_are_reproducible(self):
        self.assertEqual(self.calc["premium_usd"], 1.46)
        self.assertAlmostEqual(self.calc["price_multiple"], 2.49 / 1.03)
        self.assertEqual(self.calc["breakeven_minutes"], {"30": 2.92, "60": 1.46, "120": 0.73})
        for point in self.calc["sensitivity"]:
            self.assertAlmostEqual(point["net_saving_usd"], point["saved_minutes"] * point["labor_usd_per_hour"] / 60 - 1.46)
        self.assertEqual(next(r["net_saving_usd"] for r in self.calc["sensitivity"] if r["saved_minutes"] == 2 and r["labor_usd_per_hour"] == 60), 0.54)

    def test_scores_are_not_used_as_acceptance_probabilities(self):
        altered = deepcopy(self.revision)
        for sample in altered["samples"]:
            sample.update(sonnet_score=1, astra_score=100)
        self.assertEqual(calculate(altered), self.calc)
        self.assertIn("acceptance_rate", self.calc["unmeasured"])

    def test_routing_charges_both_calls_and_has_no_free_retry(self):
        self.assertAlmostEqual(self.calc["routing_threshold"], 1 - 1.03 / 2.49)
        route = next(r for r in self.calc["routing"] if r["escalation_rate"] == 0.3)
        self.assertEqual(route["bill_usd"], 1.777)
        self.assertEqual(route["saving_vs_all_astra_usd"], 0.713)
        self.assertLess(next(r["saving_vs_all_astra_usd"] for r in self.calc["routing"] if r["escalation_rate"] == 0.6), 0)

    def test_tables_stay_with_arguments_in_both_reports(self):
        html = (PROJECT / "professional_report.html").read_text()
        md = (PROJECT / "professional_report.md").read_text()
        parts = materialize_tables(self.revision, self.calc)
        self.assertEqual(sum(len(p.get("tables", [])) for p in parts), 2)
        for part in parts:
            for table in part.get("tables", []):
                for row in table["rows"]:
                    for cell in row:
                        self.assertIn(cell, html)
                        self.assertIn(cell, md)
        self.assertIn("实际企业 ROI 标成已验证", html)
        self.assertIn("98% 是四舍五入后的评估分数，不是 98%", md)

    def test_only_cost_leaf_receives_new_evidence(self):
        claims = [c for c in read_lines(PROJECT / "ledger/claims.jsonl") if "_cost_case_leaf_" in c["claim_id"]]
        self.assertEqual(len(claims), 4)
        self.assertEqual({c["question_node_id"] for c in claims}, {"Q1.1.2.2"})
        self.assertEqual({c["source_id"] for c in claims}, {"S05", "S14", "S15", "S16"})
        run = next(r for r in read_lines(PROJECT / "search_runs.jsonl") if r["search_run_id"] == "search_Q1.1.2.2_cost_case_leaf")
        self.assertEqual(run["performed_on"], "2026-09-18")
        envelopes = {e["claim_id"]: e for e in read_lines(PROJECT / "ledger/claim_temporal_envelopes.jsonl")}
        for claim in claims:
            self.assertLessEqual(envelopes[claim["claim_id"]]["published_at"], "2026-09-10")

    def test_history_other_leaves_and_gates_are_unchanged(self):
        before = json.loads((FOLDER / "before/research_chapters.json").read_text())
        current = json.loads((PROJECT / "research_chapters.json").read_text())
        self.assertEqual([c for c in before if c["id"] != "Q1.1.2.2"], [c for c in current if c["id"] != "Q1.1.2.2"])
        self.assertEqual([(c["id"], c["passed"]) for c in before], [(c["id"], c["passed"]) for c in current])
        for name in ("qa_tree.json", "research_plan.json", "target_gates.json"):
            self.assertEqual((FOLDER / "before" / name).read_bytes(), (PROJECT / name).read_bytes())
        for name, row in json.loads((FOLDER / "before_manifest.json").read_text()).items():
            self.assertEqual(hashlib.sha256((PROJECT / name).read_bytes()[:row["bytes"]]).hexdigest(), row["sha256"])

    def test_readability_revision_only_changes_authored_prose(self):
        folder = PROJECT / "research_revisions/20260918_readability"
        before = json.loads((folder / "before_chapters.json").read_text())
        after = json.loads((PROJECT / "research_chapters.json").read_text())
        for old, new in zip(before, after):
            if old["id"] != "Q1.1.2.2":
                self.assertEqual(old, new)
            else:
                self.assertEqual({k:v for k,v in old.items() if k != "analysis"},
                                 {k:v for k,v in new.items() if k != "analysis"})
                main = [s for s in new["analysis"] if not s.get("supplementary", False)]
                supporting = [s for s in new["analysis"] if s.get("supplementary", False)]
                self.assertTrue(main and supporting)
                html = (PROJECT / "professional_report.html").read_text().split('<article class="node-detail" id="Q1.1.2.2"', 1)[1].split('</article>', 1)[0]
                md = (PROJECT / "professional_report.md").read_text()
                for section in main:
                    self.assertLess(html.index(section["heading"]), html.index('<details class="supplementary-analysis">'))
                    for extra in supporting:
                        self.assertLess(md.index(section["heading"]), md.index(extra["heading"]))


if __name__ == "__main__":
    unittest.main()
