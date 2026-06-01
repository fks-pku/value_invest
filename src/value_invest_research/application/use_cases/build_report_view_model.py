from __future__ import annotations

from dataclasses import dataclass

from value_invest_research.domain.report_view_model import ReportViewModel, build_report_view_model
from value_invest_research.ports.repositories import ResearchProjectRepository


@dataclass(frozen=True)
class BuildReportViewModel:
    """Load project artifacts and assemble the renderer-facing view model."""

    repository: ResearchProjectRepository

    def execute(self) -> ReportViewModel:
        return build_report_view_model(
            project=self.repository.load_project(),
            qa_tree=self.repository.load_qa_tree(),
            sources=self.repository.load_sources_for_report(),
            targets=self.repository.load_targets_for_report(),
        )
