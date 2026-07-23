from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

from value_invest_research.domain.report_view_model import ReportViewModel


class ProfessionalReportRenderer(Protocol):
    """Outbound port for writing professional research reports."""

    def write_stock_report(self, root: Path, ticker: str, client: Any | None = None) -> dict[str, Any]:
        """Write a stock professional report and return stable result metadata."""

    def write_meta_qa_report(self, root: Path, project_id: str, client: Any | None = None) -> dict[str, Any]:
        """Write a meta-QA professional report and return stable result metadata."""


class CanonicalReportRenderer(Protocol):
    """Outbound port for rendering the locked research-goal report contract."""

    def render(self, view_model: ReportViewModel) -> str:
        """Render a report view model to the adapter's public format."""

    def write(
        self,
        project_dir: Path,
        view_model: ReportViewModel,
        *,
        filename: str = "professional_report.md",
    ) -> dict[str, Any]:
        """Write the public report and return stable result metadata."""
