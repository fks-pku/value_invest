from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable

from value_invest_research.domain.research_plan import (
    prepare_research_step_event,
    validate_research_plan_execution,
    validate_research_step_event,
)
from value_invest_research.domain.l3_research_plan import (
    validate_l3_research_plan_set,
)
from value_invest_research.ports.repositories import ResearchPlanRepository


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class RecordResearchStepEvent:
    """Validate and append one auditable research-step event."""

    repository: ResearchPlanRepository
    clock: Callable[[], str] = _utc_now

    def execute(self, event: dict[str, Any]) -> dict[str, Any]:
        plan = self.repository.load_plan()
        if not plan:
            raise ValueError(f"{self.repository.plan_path_label} does not exist or is empty")
        prior_events = self.repository.load_step_events()
        normalized = prepare_research_step_event(plan, event, recorded_at=self.clock())
        issues = validate_research_step_event(plan, prior_events, normalized)
        if issues:
            detail = "; ".join(f"{item['code']}: {item['message']}" for item in issues)
            raise ValueError(detail)
        appended = self.repository.append_step_event(normalized)
        progress = validate_research_plan_execution(
            plan,
            self.repository.load_step_events(),
        )
        return {
            "appended": appended,
            "event_id": normalized["event_id"],
            "step_id": normalized["step_id"],
            "event_path": self.repository.event_path_label,
            "progress": progress,
        }


@dataclass(frozen=True)
class ValidateResearchPlanExecution:
    """Load and validate one plan plus its append-only execution history."""

    repository: ResearchPlanRepository

    def execute(self) -> dict[str, Any]:
        plan = self.repository.load_plan()
        if not plan:
            return {
                "ok": False,
                "issues": [
                    {
                        "severity": "error",
                        "code": "missing_research_plan",
                        "message": f"{self.repository.plan_path_label} does not exist or is empty",
                        "step_id": "",
                    }
                ],
                "summary": {
                    "plan_id": "",
                    "status": "missing",
                    "steps": 0,
                    "pending": 0,
                    "in_progress": 0,
                    "review_pending": 0,
                    "blocked": 0,
                    "completed": 0,
                    "events": 0,
                    "historical_plan_events": 0,
                },
                "step_states": [],
            }
        parent = validate_research_plan_execution(plan, self.repository.load_step_events())
        if plan.get("plan_type") == "l3_deep_research":
            return parent
        if not hasattr(self.repository, "load_l3_research_plan_bundle"):
            return parent
        bundle = self.repository.load_l3_research_plan_bundle()
        if not bundle.get("index"):
            parent["ok"] = False
            parent["issues"].append(
                {
                    "severity": "error",
                    "code": "missing_l3_research_plan_index",
                    "message": "Every L3 must own an independent research plan.",
                    "step_id": "",
                }
            )
            return parent
        nested = validate_l3_research_plan_set(
            parent_plan=plan,
            index=bundle["index"],
            plans=bundle["plans"],
            events_by_node=bundle["events_by_node"],
        )
        return {
            "ok": parent["ok"] and nested["ok"],
            "issues": [*parent["issues"], *nested["issues"]],
            "summary": {**parent["summary"], "nested": nested["summary"]},
            "step_states": parent["step_states"],
            "l3_plans": nested["plans"],
        }
