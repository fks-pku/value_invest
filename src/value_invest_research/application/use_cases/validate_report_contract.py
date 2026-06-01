from __future__ import annotations

from dataclasses import dataclass

from value_invest_research.domain.quality_gates import validate_report_contract
from value_invest_research.domain.research_artifacts import ReportContractValidationResult
from value_invest_research.ports.repositories import ReportDocumentRepository


@dataclass(frozen=True)
class ValidateReportContract:
    """Validate public report HTML through a report repository port."""

    repository: ReportDocumentRepository

    def execute(
        self,
        *,
        mode: str = "historical_backtest",
        require_l3: bool = False,
    ) -> ReportContractValidationResult:
        document = self.repository.load_report_document()
        return validate_report_contract(
            document,
            path=self.repository.report_path_label,
            mode=mode,
            require_l3=require_l3,
        )
