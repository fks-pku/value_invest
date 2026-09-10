from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from value_invest_research.adapters.outbound.canonical_html_report_renderer import CanonicalHtmlReportRenderer
from value_invest_research.domain.question_tree_report import validate_question_tree_report
from value_invest_research.domain.report_view_model import ReportViewModel
from value_invest_research.framework_contracts import validate_report_contract_html


def sample():
    base = dict(what="回答当前问题。", acceptance_rule="对象、口径、证据与反向解释明确。", data_required=["所需数据"],
                conclusion="待验证的方向性判断。", passed=False, gaps=["没有足够长期数据"], reasons=["观察期不足"],
                analysis=[{"heading":"分析过程", "paragraphs":["比较了当前观察与反向解释。[REF-1]"]}], next_actions=["补采长期数据"])
    source = {"source_id":"REF-1", "title":"测试原始来源", "url":"https://example.com/source", "published_at":"2026-01-01"}
    evidence = {"source":"REF-1", "locator":"结果章节", "fact":"仅为测试数据，不是研究事实。", "boundary":"不能推广", "effect":"boundary"}
    return dict(template_version="question-tree-v1", title="另一个主题", as_of_date="2026-01-01", sources=[source], nodes=[
        dict(deepcopy(base), id="OTHER", parent_id="", level=1, question="另一个元问题？", mode="rollup", evidence=[]),
        dict(deepcopy(base), id="OTHER.child", parent_id="OTHER", level=2, question="足够证据吗？", mode="leaf", evidence=[evidence])])


def vm(data):
    return ReportViewModel(project={"presentation_profile":"question-tree-v1", "question_tree":data}, goal={}, supply_chain={}, qa_roots=[], targets=[], sources=data["sources"])


class QuestionTreeTemplateTests(unittest.TestCase):
    def test_reusable_without_gpt_or_ai_factory_identifiers(self):
        data = sample()
        self.assertEqual(validate_question_tree_report(data), [])
        html = CanonicalHtmlReportRenderer().render(vm(data))
        result = validate_report_contract_html(html)
        self.assertTrue(result["ok"], result["issues"])
        self.assertEqual(result["summary"]["nodes"], 2)
        self.assertNotIn("GPT-6", html)
        self.assertNotIn("AFD-", html)
        self.assertIn('data-child-id="OTHER.child"', html)

    def test_all_four_slots_and_titles_are_locked(self):
        html = CanonicalHtmlReportRenderer().render(vm(sample()))
        missing = html.replace('data-section="analysis"', 'data-section="missing"', 1)
        self.assertFalse(validate_report_contract_html(missing)["ok"])
        renamed = html.replace('<h3>分析正文</h3>', '<h3>随意面板</h3>')
        self.assertFalse(validate_report_contract_html(renamed)["ok"])

    def test_parent_cannot_pass_unanswered_child(self):
        data = sample()
        data["nodes"][0]["passed"] = True
        self.assertTrue(any("mandatory child" in e for e in validate_question_tree_report(data)))
        with self.assertRaises(ValueError):
            CanonicalHtmlReportRenderer().render(vm(data))

    def test_parent_cannot_get_leaf_evidence(self):
        data = sample()
        data["nodes"][0]["evidence"] = deepcopy(data["nodes"][1]["evidence"])
        self.assertTrue(any("masquerade" in e for e in validate_question_tree_report(data)))

    def test_missing_leaf_evidence_is_not_fabricated(self):
        data = sample()
        data["nodes"][1]["evidence"] = []
        html = CanonicalHtmlReportRenderer().render(vm(data))
        self.assertIn("尚无可展示的本题证据", html)
        self.assertNotIn("已逐问题抽取并复核", html)
        data["nodes"][1]["passed"] = True
        self.assertTrue(any("passed leaf requires evidence" in e for e in validate_question_tree_report(data)))

    def test_broken_parent_depth_duplicate_id_are_rejected(self):
        data = sample()
        data["nodes"][1].update(parent_id="MISSING", level=6)
        self.assertGreaterEqual(len(validate_question_tree_report(data)), 2)
        data = sample()
        data["nodes"].append(deepcopy(data["nodes"][1]))
        self.assertTrue(validate_question_tree_report(data))

    def test_html_is_escaped_and_links_are_safe(self):
        data = sample()
        data["nodes"][1]["question"] = '<script>alert("bad")</script>'
        html = CanonicalHtmlReportRenderer().render(vm(data))
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('<script>alert(', html)
        data["sources"][0]["url"] = "javascript:alert(1)"
        with self.assertRaises(ValueError):
            CanonicalHtmlReportRenderer().render(vm(data))

    def test_pre_rendered_print_and_no_js_readability(self):
        html = CanonicalHtmlReportRenderer().render(vm(sample()))
        self.assertIn('id="OTHER.child"', html)
        self.assertIn("仅为测试数据，不是研究事实。", html)
        self.assertNotIn("fetch(", html)
        self.assertNotIn('class="node-detail" hidden', html)
        self.assertIn(".js-ready:not(.show-all)", html)
        self.assertIn("@media print", html)
        self.assertIn("display:block!important", html)
        self.assertIn("popstate", html)

    def test_local_source_uses_current_tab(self):
        data = sample()
        data["sources"][0]["url"] = "source/manual/report.pdf"
        html = CanonicalHtmlReportRenderer().render(vm(data))
        self.assertIn('<a href="source/manual/report.pdf">', html)
        self.assertNotIn('href="source/manual/report.pdf" target=', html)

    def test_write_and_package_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            CanonicalHtmlReportRenderer().write(Path(tmp), vm(sample()))
            self.assertTrue((Path(tmp) / "professional_report.html").exists())
        assets = Path(__file__).parents[1] / "src/value_invest_research/adapters/outbound/report_templates"
        self.assertEqual({p.suffix for p in assets.glob("question_tree_v1.*")}, {".html", ".css", ".js"})

    def test_current_report_has_same_research_content(self):
        project = Path(__file__).parents[1] / "research/events/gpt6_ai_industry_impact_20260910"
        data = json.loads((project / "question_tree_report.json").read_text())
        chapters = json.loads((project / "research_chapters.json").read_text())
        nodes = {n["id"]:n for n in data["nodes"]}
        for chapter in chapters:
            node = nodes[chapter["id"]]
            self.assertEqual(node["conclusion"], chapter["conclusion"])
            self.assertEqual(node["passed"], chapter["passed"])
            self.assertEqual(node["analysis"][:len(chapter["analysis"])], chapter["analysis"])
            self.assertEqual([e["fact"] for e in node["evidence"]], [e["fact"] for e in chapter["evidence"]])
        self.assertTrue(validate_report_contract_html((project / "professional_report.html").read_text())["ok"])


if __name__ == "__main__":
    unittest.main()
