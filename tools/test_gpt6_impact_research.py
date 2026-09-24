"""Read-only QA for this event artifact; does not claim full BOM/valuation completion."""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

from gpt6_impact_research import PROJECT, read_lines
from render_gpt6_impact_report import blocks
from value_invest_research.domain.report_view_model import ReportViewModel
from value_invest_research.framework_contracts import validate_report_contract_html


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids, self.hrefs, self.text, self.h2 = [], [], [], []
        self.in_h2 = False
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "a":
            self.hrefs.append(a.get("href", ""))
        self.in_h2 = self.in_h2 or tag == "h2"
    def handle_endtag(self, tag):
        if tag == "h2":
            self.in_h2 = False
    def handle_data(self, data):
        self.text.append(data)
        if self.in_h2:
            self.h2.append(data)


class EventArtifactChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vm = ReportViewModel(**json.loads((PROJECT / "report_view_model.json").read_text()))
        cls.html = (PROJECT / "professional_report.html").read_text()
        cls.md = (PROJECT / "professional_report.md").read_text()
        cls.page = Page(cls.html)
        cls.sources = {s["source_id"]: s for s in cls.vm.sources}

    def test_plan_and_truthful_partial_state(self):
        result = json.loads((PROJECT / "plan_validation.json").read_text())
        self.assertTrue(result["ok"], result["issues"])
        nested = result["summary"]["nested"]
        leaves = [n for n in self.vm.project["question_tree"]["nodes"] if n["mode"] == "leaf"]
        completed = sum(n["passed"] for n in leaves)
        self.assertEqual((nested["leaf_steps"], nested["completed_leaf_steps"], nested["blocked_leaf_steps"]),
                         (len(leaves), completed, len(leaves) - completed))
        self.assertEqual(nested["max_depth"], 3)
        self.assertEqual(self.vm.project["research_status"], "partial_research")

    def test_native_expansion_keeps_prior_failure(self):
        for l3 in ("Q1.1.2", "Q1.2.2"):
            folder = PROJECT / "l3_research_plans" / l3
            plan = json.loads((folder / "research_plan.json").read_text())
            self.assertEqual(len(plan["expansion_history"]), 1)
            old = plan["expansion_history"][0]["from_plan_id"]
            self.assertTrue((folder / "research_plan_history" / f"{old}.json").exists())
            history = read_lines(folder / "research_step_events.jsonl")
            self.assertTrue(any(e["plan_id"] == old and e["event_type"] == "gate_evaluated" and not e["evidence_gate"]["passed"] for e in history))

    def test_question_specific_trace(self):
        claims = read_lines(PROJECT / "ledger/claims.jsonl")
        xs = {r["extraction_id"]:r for r in read_lines(PROJECT / "source_extractions.jsonl")}
        rs = {r["review_id"]:r for r in read_lines(PROJECT / "source_reviews.jsonl")}
        searches = {r["search_run_id"]:r for r in read_lines(PROJECT / "search_runs.jsonl")}
        times = {r["claim_id"]:r for r in read_lines(PROJECT / "ledger/claim_temporal_envelopes.jsonl")}
        active = {n["id"] for n in self.vm.project["question_tree"]["nodes"]}
        for claim in [c for c in claims if c["question_node_id"] in active and "_leaf_20260922_" in c["claim_id"]]:
            self.assertIn(claim["source_id"], self.sources)
            for related in [xs[claim["extraction_id"]], rs[claim["review_id"]], searches[claim["search_run_id"]]]:
                for key in ("l3_plan_id", "l3_node_id", "question_node_id", "question_level", "research_step_id", "search_run_id"):
                    self.assertEqual(claim[key], related[key])
            self.assertTrue(claim["locator"])
            self.assertTrue(searches[claim["search_run_id"]]["refutation_search_result"])
            self.assertIn(claim["claim_id"], times)

    def test_dates_and_no_action(self):
        for source in self.sources.values():
            self.assertLessEqual(source["published_at"], "2026-09-10")
        for target in self.vm.targets:
            self.assertEqual(target["action_state"], "no_action")
            self.assertFalse(target["research_gate"]["passed"])
        states = {s["question_id"]:s for s in read_lines(PROJECT / "ledger/node_states.jsonl")}
        self.assertGreater(len(states["F1"]["gaps"]), 3)
        self.assertFalse(states["F1"]["passed"])

    def test_same_claims_in_html_and_markdown(self):
        visible = ''.join(self.page.text)
        # Current shared renderers consume the question tree, not the legacy
        # authored-input chapter cache or its historical S-digits-only citations.
        for chapter in self.vm.project["question_tree"]["nodes"]:
            self.assertIn(chapter["conclusion"], visible)
            self.assertIn(chapter["conclusion"], self.md)
            self.assertTrue(any(p.strip() for part in chapter["analysis"] if not part.get("supplementary", False) for p in part["paragraphs"]))
            for part in chapter["analysis"]:
                for paragraph in part["paragraphs"]:
                    for segment in re.split(r"\[[A-Za-z0-9_.-]+\]", paragraph):
                        if segment.strip():
                            self.assertIn(segment.strip(), visible)
                            self.assertIn(segment.strip(), self.md)
                    for sid in re.findall(r"\[([A-Za-z0-9_.-]+)\]", paragraph):
                        self.assertIn(self.sources[sid]["url"], self.html)
                        self.assertIn(self.sources[sid]["url"], self.md)
            for pair in chapter["evidence"]:
                self.assertIn(pair["fact"], visible)
                self.assertIn(pair["fact"], self.md)

    def test_markdown_keeps_three_modules_for_every_node_including_root(self):
        content = blocks(self.vm)
        for node in self.vm.project["question_tree"]["nodes"]:
            titles = [b["text"] for b in content if b.get("module_node") == node["id"]]
            expected = (["研究子问题", "子问题核心结论", "欠缺的方向"] if node["mode"] == "rollup"
                        else ["核心观点", "关键论证", "数据列表"])
            self.assertEqual(titles, [f"{i}. {title}" for i, title in enumerate(expected, 1)])
            self.assertIn(f'<a id="{node["id"]}"></a>', self.md)

    def test_links_and_section_order(self):
        self.assertEqual(len(self.page.ids), len(set(self.page.ids)))
        result = validate_report_contract_html(self.html)
        self.assertTrue(result["ok"], result["issues"])
        self.assertEqual(result["summary"]["presentation_profile"], "question-tree-v1")
        self.assertEqual(result["summary"]["leaves"], 10)
        for url in self.page.hrefs:
            if url.startswith("#"):
                self.assertIn(url[1:], self.page.ids)
            elif not url.startswith(("https://", "http://")):
                self.assertTrue((PROJECT / url).exists(), url)
        for source in self.sources.values():
            self.assertIn(source["url"], self.page.hrefs)
        self.assertNotIn("fetch(", self.html)
        self.assertNotRegex(self.html, r'<(?:script|link)[^>]+(?:src|href)="https?://')

    def test_calculations(self):
        self.assertAlmostEqual(.1*4+.02*20, .8)
        self.assertAlmostEqual(.1*10+.02*50, 2)
        self.assertAlmostEqual(1/2.5, .4)
        self.assertEqual(round(1-17332/26098, 3), .336)
        self.assertEqual(round((7.09-7.09/1.15)*60),55)
        upstream = next(c for c in self.vm.qa_roots if c["id"] == "F1.2.1")
        scenarios = next(t for a in upstream["analysis"] for t in a.get("tables", []))
        for _, n, c, h, outcome in scenarios["rows"]:
            self.assertEqual(round(float(n)*float(c)/float(h),3),float(outcome))
        self.assertEqual(round(218.36/(2.22*4), 1), 24.6)
        self.assertEqual(round(492.44/(4.74*4), 1), 26.0)
        self.assertEqual(round(243/10.23, 1), 23.8)
        self.assertEqual(round(243/16.69, 1), 14.6)
        self.assertEqual(round(10*.7*.83/24.285, 3), .239)

    def test_first_principles_tree_and_preserved_links(self):
        tree = self.vm.project["question_tree"]["nodes"]
        groups = [n for n in tree if n["parent_id"] == "F1"]
        self.assertEqual([n["id"] for n in groups], ["F1.1", "F1.2", "F1.3"])
        self.assertTrue(all(len(n["question"]) < 40 for n in tree))
        old = json.loads((PROJECT / "research_revisions/20260922_object_industry_company_execution/before/qa_tree.json").read_text())
        self.assertTrue({n["id"] for n in old["nodes"]}.isdisjoint({n["id"] for n in tree}))
        self.assertEqual({n["id"] for n in tree if n["level"] > 3}, set())

    def test_changed_profit_question_does_not_inherit_pass(self):
        states = read_lines(PROJECT / "ledger/node_states.jsonl")
        profit = [s for s in states if s["question_id"] == "Q1.3.1"]
        self.assertTrue(any(s["passed"] for s in profit[:-1]))
        self.assertFalse(profit[-1]["passed"])
        latest = {s["question_id"]: s for s in states}
        self.assertFalse(latest["Q1.3"]["passed"])
        self.assertTrue(set(profit[-1]["gaps"]).issubset(latest["Q1"]["gaps"]))
        reviews = [r for r in read_lines(PROJECT / "source_reviews.jsonl") if "_first_principles_leaf_" in r["review_id"]]
        self.assertEqual({r["question_node_id"] for r in reviews}, {"Q1.1.2.2", "Q1.3.1"})
        self.assertTrue(all(r["recorded_at"].startswith("2026-09-11") for r in reviews))

    def test_revision_preserves_append_only_history(self):
        import hashlib
        folder = PROJECT / "research_revisions/20260922_object_industry_company_execution"
        manifest = json.loads((folder / "before_manifest.json").read_text())
        for name, row in manifest.items():
            self.assertEqual(hashlib.sha256((PROJECT / name).read_bytes()[:row["bytes"]]).hexdigest(), row["sha256"], name)
        self.assertEqual(self.vm.project["as_of_date"], "2026-09-10")
        self.assertEqual(self.vm.project["revised_on"], "2026-09-22")

    def test_new_cost_refutation_is_question_specific(self):
        pairs = [r for r in read_lines(PROJECT / "source_extractions.jsonl") if r["source_id"] == "S14"]
        self.assertEqual(len(pairs), 2)
        self.assertEqual({r["question_node_id"] for r in pairs}, {"Q1.1.2.2"})
        self.assertTrue(any("_first_principles_leaf_" in r["extraction_id"] for r in pairs))
        self.assertTrue(any("_cost_case_leaf_" in r["extraction_id"] for r in pairs))
        all_sources = {r["source_id"]: r for r in read_lines(PROJECT / "sources.jsonl")}
        self.assertEqual(all_sources["S14"]["published_at"], "2026-09-09")
        self.assertEqual(round(2.49 / 1.03, 2), 2.42)


if __name__ == "__main__":
    unittest.main()
