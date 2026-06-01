from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from value_invest_research.ports.research_workflows import LeafResearchWorkflow


@dataclass(frozen=True)
class BuildLeafResearchTasks:
    workflow: LeafResearchWorkflow

    def execute(
        self,
        root: Path,
        ticker: str,
        *,
        limit: int | None = None,
        include_completed: bool = False,
    ) -> dict:
        return self.workflow.build_tasks(root, ticker, limit=limit, include_completed=include_completed)


@dataclass(frozen=True)
class RunLeafResearch:
    workflow: LeafResearchWorkflow

    def execute(
        self,
        root: Path,
        ticker: str,
        *,
        provider: str,
        input_path: Path | None = None,
        limit: int | None = None,
    ) -> dict:
        return self.workflow.run_research(root, ticker, provider=provider, input_path=input_path, limit=limit)


@dataclass(frozen=True)
class ImportLeafResearchResults:
    workflow: LeafResearchWorkflow

    def execute(self, root: Path, ticker: str, path: Path) -> dict:
        return self.workflow.import_results(root, ticker, path)


@dataclass(frozen=True)
class SynthesizeLeafAnswers:
    workflow: LeafResearchWorkflow

    def execute(self, root: Path, ticker: str) -> dict:
        return self.workflow.synthesize_answers(root, ticker)


@dataclass(frozen=True)
class RollupResearchAnswers:
    workflow: LeafResearchWorkflow

    def execute(self, root: Path, ticker: str) -> dict:
        return self.workflow.rollup_answers(root, ticker)

