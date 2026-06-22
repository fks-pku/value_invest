from __future__ import annotations

from pathlib import Path
from typing import Any

from value_invest_research.adapters.outbound.report_sections import (
    DEFAULT_REPORT_SECTIONS,
    ReportRenderContext,
    ReportSection,
    render_hero,
)
from value_invest_research.adapters.outbound.report_sections.shared import _e, _source_url_lookup
from value_invest_research.adapters.outbound.report_sections.styles import report_css
from value_invest_research.domain.report_view_model import ReportViewModel


class CanonicalHtmlReportRenderer:
    """HTML adapter for the locked research-goal report presentation contract."""

    def __init__(self, sections: tuple[ReportSection, ...] = DEFAULT_REPORT_SECTIONS):
        self.sections = sections

    def render(self, view_model: ReportViewModel) -> str:
        data = view_model.to_dict()
        source_url_by_id = _source_url_lookup(data.get("sources", []))
        context = ReportRenderContext(data=data, source_url_by_id=source_url_by_id)
        title = str(data["project"].get("title") or data["goal"].get("topic") or "专业投研报告")
        section_html = [section.render(context) for section in self.sections]
        return "\n".join(
            [
                "<!doctype html>",
                '<html lang="zh-CN">',
                "<head>",
                '<meta charset="utf-8">',
                '<meta name="viewport" content="width=device-width, initial-scale=1">',
                f"<title>{_e(title)}</title>",
                "<style>",
                report_css(),
                "</style>",
                "</head>",
                "<body>",
                render_hero(data),
                *section_html,
                "</body>",
                "</html>",
            ]
        )

    def write(
        self,
        project_dir: Path,
        view_model: ReportViewModel,
        *,
        filename: str = "professional_report.html",
    ) -> dict[str, Any]:
        project_dir.mkdir(parents=True, exist_ok=True)
        html = self.render(view_model)
        output_path = project_dir / filename
        output_path.write_text(html, encoding="utf-8")
        return {
            "project_id": view_model.project.get("project_id", ""),
            "report_path": str(output_path),
            "qa_roots": len(view_model.qa_roots),
            "targets": len(view_model.targets),
            "sources": len(view_model.sources),
        }
