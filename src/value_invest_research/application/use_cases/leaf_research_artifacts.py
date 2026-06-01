from __future__ import annotations

from dataclasses import dataclass

from value_invest_research.ports.repositories import LeafResearchArtifactRepository


@dataclass(frozen=True)
class LoadCompletedLeafNodeIds:
    """Load already-synthesized leaf node ids through a repository port."""

    repository: LeafResearchArtifactRepository

    def execute(self) -> set[str]:
        return self.repository.load_completed_leaf_node_ids()


@dataclass(frozen=True)
class PersistLeafResearchTasks:
    """Persist leaf research tasks through a repository port."""

    repository: LeafResearchArtifactRepository

    def execute(self, rows: list[dict]) -> dict[str, object]:
        return {
            "task_path": self.repository.task_path_label,
            "tasks": self.repository.save_tasks(rows),
        }


@dataclass(frozen=True)
class LoadLeafResearchTasks:
    """Load leaf research tasks through a repository port."""

    repository: LeafResearchArtifactRepository

    def execute(self) -> list[dict]:
        return self.repository.load_tasks()


@dataclass(frozen=True)
class LoadLeafResearchResults:
    """Load normalized leaf research results through a repository port."""

    repository: LeafResearchArtifactRepository

    def execute(self) -> list[dict]:
        return self.repository.load_results()


@dataclass(frozen=True)
class PersistLeafAnswers:
    """Persist synthesized leaf answers through a repository port."""

    repository: LeafResearchArtifactRepository

    def execute(self, rows: list[dict]) -> dict[str, object]:
        return {
            "answer_path": self.repository.answer_path_label,
            "answers": self.repository.save_leaf_answers(rows),
        }


@dataclass(frozen=True)
class PersistRollupAnswers:
    """Persist parent rollup answers through a repository port."""

    repository: LeafResearchArtifactRepository

    def execute(self, rows: list[dict]) -> dict[str, object]:
        return {
            "rollup_path": self.repository.rollup_path_label,
            "rollups": self.repository.save_rollup_answers(rows),
        }
