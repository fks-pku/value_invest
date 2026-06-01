from __future__ import annotations

from dataclasses import dataclass

from value_invest_research.ports.repositories import LeafResearchResultRepository


@dataclass(frozen=True)
class PersistLeafResearchResults:
    """Persist normalized leaf research results through a repository port."""

    repository: LeafResearchResultRepository

    def execute(self, rows: list[dict]) -> dict[str, object]:
        counts = self.repository.save_results(rows)
        return {
            "result_path": self.repository.result_path_label,
            "source_path": self.repository.source_path_label,
            "results": counts.get("results", 0),
            "sources": counts.get("sources", 0),
        }

