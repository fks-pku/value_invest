from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from value_invest_research.domain.leaf_answer_synthesis import (
    build_rollup_answer_rows,
    synthesize_latest_leaf_answers,
)
from value_invest_research.ports.repositories import LeafResearchArtifactRepository


@dataclass(frozen=True)
class SynthesizeLeafResearchAnswers:
    """Synthesize persisted provider results into leaf answer override rows."""

    repository: LeafResearchArtifactRepository

    def execute(self) -> dict[str, Any]:
        answers = synthesize_latest_leaf_answers(self.repository.load_results())
        return {
            "answer_path": self.repository.answer_path_label,
            "answers": self.repository.save_leaf_answers(answers),
        }


@dataclass(frozen=True)
class BuildRollupResearchAnswers:
    """Build parent-level rollup rows from an enriched QA tree."""

    repository: LeafResearchArtifactRepository

    def execute(self, qa_tree: dict[str, Any]) -> dict[str, Any]:
        rows = build_rollup_answer_rows(qa_tree)
        return {
            "rollup_path": self.repository.rollup_path_label,
            "rollups": self.repository.save_rollup_answers(rows),
        }
