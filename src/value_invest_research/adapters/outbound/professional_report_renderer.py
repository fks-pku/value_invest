from __future__ import annotations

from pathlib import Path


class ProfessionalReportRendererAdapter:
    """Adapter around the current professional report renderer implementation."""

    def write_stock_report(self, root: Path, ticker: str, client=None) -> dict:
        from value_invest_research.report_synthesis import write_stock_professional_report

        return write_stock_professional_report(root, ticker, client=client)

    def write_meta_qa_report(self, root: Path, project_id: str, client=None) -> dict:
        from value_invest_research.report_synthesis import write_meta_qa_professional_report

        return write_meta_qa_professional_report(root, project_id, client=client)
