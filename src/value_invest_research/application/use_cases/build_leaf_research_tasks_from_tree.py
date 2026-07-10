from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from value_invest_research.domain.leaf_research_tasks import build_leaf_tasks_from_tree, leaf_question_count
from value_invest_research.ports.repositories import LeafResearchArtifactRepository, SourceUniverseRepository


@dataclass(frozen=True)
class BuildLeafResearchTasksFromTree:
    """Build and persist provider-agnostic leaf research tasks from a QA tree."""

    repository: LeafResearchArtifactRepository
    source_universe_repository: SourceUniverseRepository | None = None

    def execute(
        self,
        qa_tree: dict[str, Any],
        *,
        ticker: str,
        company_name: str,
        limit: int | None = None,
        include_completed: bool = False,
    ) -> dict[str, Any]:
        completed = set() if include_completed else self.repository.load_completed_leaf_node_ids()
        source_universe = (
            self.source_universe_repository.resolve_for_research(qa_tree)
            if self.source_universe_repository is not None
            else {}
        )
        tasks = build_leaf_tasks_from_tree(
            qa_tree,
            ticker=ticker,
            company_name=company_name,
            source_universe=source_universe,
            completed_node_ids=completed,
            limit=limit,
        )
        return {
            "task_path": self.repository.task_path_label,
            "tasks": self.repository.save_tasks(tasks),
            "leaf_questions": leaf_question_count(qa_tree),
            "include_completed": include_completed,
        }
