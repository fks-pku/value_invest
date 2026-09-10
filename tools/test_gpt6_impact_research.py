"""Read-only QA for this event artifact; does not claim full BOM/valuation completion."""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from html import unescape

from gpt6_impact_research import PROJECT, read_lines
from render_gpt6_impact_report import blocks, link_tokens
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
        self.assertEqual((nested["leaf_steps"], nested["completed_leaf_steps"], nested["blocked_leaf_steps"]), (8,6,2))
        self.assertEqual(nested["max_depth"], 4)
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
        for claim in claims:
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
        self.assertEqual(len(states["Q1"]["gaps"]), 2)
        self.assertFalse(states["Q1"]["passed"])

    def test_same_claims_in_html_and_markdown(self):
        visible = ''.join(self.page.text)
        for block in blocks(self.vm):
            if block["kind"] == "paragraph":
                self.assertIn(unescape(re.sub(r'<[^>]*>', '', link_tokens(block["text"], self.sources, True))), visible)
                self.assertIn(link_tokens(block["text"], self.sources), self.md)
        for chapter in self.vm.qa_roots:
            self.assertIn(chapter["conclusion"], visible)
            self.assertIn(chapter["conclusion"], self.md)
            self.assertGreater(sum(len(p) for part in chapter["analysis"] for p in part["paragraphs"]), 400)
            for pair in chapter["evidence"]:
                self.assertIn(pair["fact"], visible)
                self.assertIn(pair["fact"], self.md)

    def test_links_and_section_order(self):
        self.assertEqual(len(self.page.ids), len(set(self.page.ids)))
        result = validate_report_contract_html(self.html)
        self.assertTrue(result["ok"], result["issues"])
        self.assertEqual(result["summary"]["presentation_profile"], "question-tree-v1")
        self.assertEqual(result["summary"]["leaves"], 8)
        for url in self.page.hrefs:
            if url.startswith("#"):
                self.assertIn(url[1:], self.page.ids)
            elif not url.startswith("https://"):
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
        scenarios = next(c["scenario_table"] for c in self.vm.qa_roots if c.get("scenario_table"))
        for _, n, c, h, outcome in scenarios["rows"]:
            self.assertEqual(round(float(n)*float(c)/float(h),2),float(outcome))


if __name__ == "__main__":
    unittest.main()
