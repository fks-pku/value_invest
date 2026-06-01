from __future__ import annotations

from pathlib import Path
from typing import Any

from value_invest_research.adapters.outbound.research_search_providers import (
    MockResearchSearchProvider,
    OpenAICompatibleResearchSearchProvider,
    PerplexityResearchSearchProvider,
    provider_for_name,
)
from value_invest_research.adapters.outbound.stock_leaf_research_service import StockLeafResearchService
from value_invest_research.domain.leaf_research_results import (
    deduplicate_leaf_sources,
    normalize_provider_result,
)
from value_invest_research.domain.leaf_research_tasks import leaf_question_count


ResearchSearchProvider = Any


def build_leaf_research_tasks(
    root: Path,
    ticker: str,
    limit: int | None = None,
    include_completed: bool = False,
) -> dict[str, Any]:
    """Compatibility wrapper for building stock leaf research tasks."""
    return StockLeafResearchService().build_tasks(root, ticker, limit=limit, include_completed=include_completed)


def run_leaf_research(
    root: Path,
    ticker: str,
    provider: str = "mock",
    input_path: Path | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """Compatibility wrapper for running stock leaf research."""
    return StockLeafResearchService().run_research(root, ticker, provider=provider, input_path=input_path, limit=limit)


def import_leaf_research_results(root: Path, ticker: str, path: Path) -> dict[str, Any]:
    """Compatibility wrapper for importing stock leaf research results."""
    return StockLeafResearchService().import_results(root, ticker, path)


def synthesize_leaf_answers(root: Path, ticker: str) -> dict[str, Any]:
    """Compatibility wrapper for synthesizing stock leaf answers."""
    return StockLeafResearchService().synthesize_answers(root, ticker)


def rollup_research_answers(root: Path, ticker: str) -> dict[str, Any]:
    """Compatibility wrapper for rolling stock leaf answers up to parents."""
    return StockLeafResearchService().rollup_answers(root, ticker)


def _provider_for_name(provider: str) -> Any:
    return provider_for_name(provider)


def _deduplicated_sources(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return deduplicate_leaf_sources(rows)


def _normalize_provider_result(row: dict[str, Any]) -> dict[str, Any]:
    return normalize_provider_result(row)


def _leaf_question_count(qa_tree: dict[str, Any]) -> int:
    return leaf_question_count(qa_tree)
