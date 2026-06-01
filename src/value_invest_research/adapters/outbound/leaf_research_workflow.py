from __future__ import annotations

from pathlib import Path

from value_invest_research.adapters.outbound.stock_leaf_research_service import StockLeafResearchService


class LeafResearchWorkflowAdapter:
    """Adapter for stock leaf research workflow operations."""

    def __init__(self, service: StockLeafResearchService | None = None):
        self.service = service or StockLeafResearchService()

    def build_tasks(
        self,
        root: Path,
        ticker: str,
        *,
        limit: int | None = None,
        include_completed: bool = False,
    ) -> dict:
        return self.service.build_tasks(root, ticker, limit=limit, include_completed=include_completed)

    def run_research(
        self,
        root: Path,
        ticker: str,
        *,
        provider: str,
        input_path: Path | None = None,
        limit: int | None = None,
    ) -> dict:
        return self.service.run_research(root, ticker, provider=provider, input_path=input_path, limit=limit)

    def import_results(self, root: Path, ticker: str, path: Path) -> dict:
        return self.service.import_results(root, ticker, path)

    def synthesize_answers(self, root: Path, ticker: str) -> dict:
        return self.service.synthesize_answers(root, ticker)

    def rollup_answers(self, root: Path, ticker: str) -> dict:
        return self.service.rollup_answers(root, ticker)
