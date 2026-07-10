from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from value_invest_research.domain.target_scoring import TargetScoringResult, score_and_rank_targets


@dataclass(frozen=True)
class ScoreTargets:
    """Score and rank target observations through domain scoring rules."""

    def execute(
        self,
        targets: list[dict[str, Any]],
        *,
        workbench: dict[str, Any] | None = None,
    ) -> TargetScoringResult:
        return score_and_rank_targets(targets, workbench=workbench)
