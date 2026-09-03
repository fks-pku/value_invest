from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from value_invest_research.domain.l3_research_plan import expand_l3_research_plan
from value_invest_research.domain.research_plan import validate_research_plan_execution
from value_invest_research.ports.repositories import ResearchPlanRepository


@dataclass(frozen=True)
class ExpandL3ResearchPlan:
    """Version one blocked terminal question into its smallest next-level set."""

    repository: ResearchPlanRepository

    def execute(
        self,
        *,
        l3_node_id: str,
        parent_question_id: str,
        child_questions: list[dict[str, Any]],
        evidence_gaps: list[str] | None = None,
        source_universe: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        bundle = self.repository.load_l3_research_plan_bundle()
        plans = [row for row in bundle.get("plans") or [] if isinstance(row, dict)]
        plan = next(
            (row for row in plans if str(row.get("l3_node_id") or "") == l3_node_id),
            None,
        )
        if plan is None:
            raise ValueError(f"Unknown L3 research plan: {l3_node_id}")

        events = list((bundle.get("events_by_node") or {}).get(l3_node_id) or [])
        execution = validate_research_plan_execution(plan, events)
        step = next(
            (
                row
                for row in plan.get("steps") or []
                if str(row.get("question_node_id") or "") == parent_question_id
            ),
            None,
        )
        if step is None:
            raise ValueError(
                f"Question {parent_question_id} is not an active terminal question"
            )
        state = next(
            (
                row
                for row in execution.get("step_states") or []
                if str(row.get("step_id") or "") == str(step.get("step_id") or "")
            ),
            {},
        )
        if state.get("status") != "blocked":
            raise ValueError(
                "Dynamic expansion requires the parent question to be blocked by "
                "a failed answerability gate"
            )
        recorded_gaps = [str(item) for item in state.get("gaps") or [] if str(item)]
        gaps = [str(item).strip() for item in (evidence_gaps or recorded_gaps) if str(item).strip()]
        if any(gap not in recorded_gaps for gap in gaps):
            raise ValueError("Expansion evidence_gaps must match recorded blocked gaps")
        if not gaps:
            raise ValueError("Dynamic expansion requires a recorded concrete gap")

        expanded = expand_l3_research_plan(
            plan,
            parent_question_id=parent_question_id,
            evidence_gap=gaps,
            child_questions=child_questions,
            source_universe=source_universe or {},
        )
        updated_plans = [expanded if row is plan else row for row in plans]
        index = dict(bundle.get("index") or {})
        index["schema_version"] = "4.0"
        index["plans"] = [
            _updated_index_row(row, expanded)
            if str(row.get("l3_node_id") or "") == l3_node_id
            else row
            for row in index.get("plans") or []
            if isinstance(row, dict)
        ]
        self.repository.save_l3_research_plans(index, updated_plans)
        self.repository.bind_l3_plans_to_question_architecture(
            parent_plan=self.repository.load_plan(),
            index=index,
        )
        return {
            "l3_node_id": l3_node_id,
            "parent_question_id": parent_question_id,
            "from_plan_id": str(plan.get("plan_id") or ""),
            "plan_id": str(expanded.get("plan_id") or ""),
            "evidence_gaps": gaps,
            "child_question_ids": list(
                (expanded.get("expansion_history") or [{}])[-1].get(
                    "child_question_ids", []
                )
            ),
            "active_steps": len(expanded.get("steps") or []),
        }


def _updated_index_row(row: dict[str, Any], plan: dict[str, Any]) -> dict[str, Any]:
    levels = [int(step.get("level") or 0) for step in plan.get("steps") or []]
    return {
        **row,
        "l3_plan_id": str(plan.get("plan_id") or ""),
        "active_steps": len(plan.get("steps") or []),
        "leaf_steps": len(plan.get("steps") or []),
        "max_depth": max(levels, default=3),
    }
