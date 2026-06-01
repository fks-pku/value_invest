from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from value_invest_research.ports.renderers import ProfessionalReportRenderer


@dataclass(frozen=True)
class WriteStockProfessionalReport:
    """Write a stock report through the report renderer port."""

    renderer: ProfessionalReportRenderer

    def execute(self, root: Path, ticker: str, client: Any | None = None) -> dict[str, Any]:
        return self.renderer.write_stock_report(root, ticker, client=client)


@dataclass(frozen=True)
class WriteMetaQaProfessionalReport:
    """Write a meta-QA report through the report renderer port."""

    renderer: ProfessionalReportRenderer

    def execute(self, root: Path, project_id: str, client: Any | None = None) -> dict[str, Any]:
        return self.renderer.write_meta_qa_report(root, project_id, client=client)

