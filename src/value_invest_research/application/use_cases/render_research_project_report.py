from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from value_invest_research.application.use_cases.build_report_view_model import BuildReportViewModel
from value_invest_research.ports.renderers import CanonicalReportRenderer
from value_invest_research.ports.repositories import ResearchProjectRepository


@dataclass(frozen=True)
class RenderResearchProjectReport:
    """Orchestrate project artifact loading, view-model assembly, and HTML writing."""

    repository: ResearchProjectRepository
    renderer: CanonicalReportRenderer

    def execute(self, *, filename: str = "professional_report.html") -> dict[str, Any]:
        view_model = BuildReportViewModel(self.repository).execute()
        return self.renderer.write(Path(self.repository.project_dir_label), view_model, filename=filename)
