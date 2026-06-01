from __future__ import annotations

from pathlib import Path
from typing import Protocol


class LeafResearchWorkflow(Protocol):
    """Outbound port for leaf research workflow operations during migration."""

    def build_tasks(
        self,
        root: Path,
        ticker: str,
        *,
        limit: int | None = None,
        include_completed: bool = False,
    ) -> dict:
        """Build leaf research tasks."""

    def run_research(
        self,
        root: Path,
        ticker: str,
        *,
        provider: str,
        input_path: Path | None = None,
        limit: int | None = None,
    ) -> dict:
        """Run or import leaf research results."""

    def import_results(self, root: Path, ticker: str, path: Path) -> dict:
        """Import provider-agnostic leaf research results."""

    def synthesize_answers(self, root: Path, ticker: str) -> dict:
        """Synthesize leaf answers from normalized provider results."""

    def rollup_answers(self, root: Path, ticker: str) -> dict:
        """Roll leaf answers up to parent QA nodes."""

