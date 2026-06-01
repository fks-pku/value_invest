from __future__ import annotations

from dataclasses import dataclass, field
from copy import deepcopy
from typing import Any

from value_invest_research.framework_contracts import (
    SCORE_WEIGHTS,
    rank_target_observations,
    score_target_observation,
    validate_target_observation_contract,
)


@dataclass(frozen=True)
class TargetScoringResult:
    """Scored and ranked target observations."""

    ok: bool
    scored_targets: list[dict[str, Any]] = field(default_factory=list)
    ranked_targets: list[dict[str, Any]] = field(default_factory=list)
    issues: list[dict[str, str]] = field(default_factory=list)


def score_and_rank_targets(targets: list[dict[str, Any]]) -> TargetScoringResult:
    """Score raw targets and rank them deterministically."""
    scored_targets: list[dict[str, Any]] = []
    for target in targets:
        scoring_input = _target_scoring_input(target)
        score = score_target_observation(scoring_input)
        scored_targets.append({**target, "score": score, "action_state": score["action_state"]})
    ranked_targets = rank_target_observations(scored_targets)
    validation = validate_target_observation_contract(ranked_targets)
    issues = list(validation.get("issues", []))
    return TargetScoringResult(
        ok=not any(issue.get("severity") == "error" for issue in issues),
        scored_targets=scored_targets,
        ranked_targets=ranked_targets,
        issues=issues,
    )


def _target_scoring_input(target: dict[str, Any]) -> dict[str, Any]:
    scoring_input = deepcopy(target)
    existing_score = scoring_input.get("score") if isinstance(scoring_input.get("score"), dict) else {}
    score_components = existing_score.get("score_components") if isinstance(existing_score.get("score_components"), dict) else {}
    for component in SCORE_WEIGHTS:
        if component not in scoring_input and component in score_components:
            scoring_input[component] = score_components[component]
    if "score_subcomponents" not in scoring_input and isinstance(existing_score.get("score_subcomponents"), dict):
        scoring_input["score_subcomponents"] = existing_score["score_subcomponents"]
    return scoring_input
