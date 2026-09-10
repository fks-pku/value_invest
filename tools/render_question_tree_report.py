"""Render an existing question_tree_report.json with the repository's shared template."""
import argparse
import json
from pathlib import Path

from value_invest_research.adapters.outbound.canonical_html_report_renderer import CanonicalHtmlReportRenderer
from value_invest_research.domain.report_view_model import ReportViewModel
from value_invest_research.framework_contracts import validate_report_contract_html


def render(input_path, output_dir):
    data = json.loads(input_path.read_text(encoding="utf-8"))
    vm = ReportViewModel(project={"title": data["title"], "presentation_profile": "question-tree-v1", "question_tree": data},
                         goal={}, supply_chain={}, qa_roots=[], targets=[], sources=data["sources"])
    renderer = CanonicalHtmlReportRenderer()
    html = renderer.render(vm)
    result = validate_report_contract_html(html)
    if not result["ok"]:
        raise ValueError(result["issues"])
    renderer.write(output_dir, vm)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    render(args.input, args.output_dir or args.input.parent)
