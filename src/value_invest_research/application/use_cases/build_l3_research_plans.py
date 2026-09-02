from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from value_invest_research.domain.l3_research_plan import (
    build_l3_research_plan_set,
    upgrade_parent_plan_for_l3_plans,
)
from value_invest_research.ports.repositories import ResearchPlanRepository


@dataclass(frozen=True)
class BuildStandaloneL3ResearchPlans:
    """Build one nested plan for each structured standalone-BOM L3 node."""

    repository: ResearchPlanRepository

    def execute(
        self,
        *,
        profile: dict[str, Any],
        source_universe: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        parent = self.repository.load_plan()
        if not parent:
            raise ValueError("A parent research_plan.json is required")
        parent = upgrade_parent_plan_for_l3_plans(parent)
        nodes = [
            {**node, "lens_id": str(lens.get("lens_id") or "")}
            for lens in profile.get("lenses") or []
            if isinstance(lens, dict)
            for node in lens.get("logic_nodes") or []
            if isinstance(node, dict)
        ]
        goal = {
            **dict(parent.get("research_goal") or {}),
            "logic_chain_version": str(
                profile.get("logic_chain_version") or ""
            ),
        }
        index, plans = build_l3_research_plan_set(
            l3_nodes=nodes,
            parent_plan_id=str(parent.get("plan_id") or ""),
            research_goal=goal,
            source_universe=source_universe or {},
        )
        self.repository.save_plan(parent)
        self.repository.save_l3_research_plans(index, plans)
        self.repository.bind_l3_plans_to_question_architecture(
            parent_plan=parent,
            index=index,
        )
        return {
            "parent_plan_id": parent["plan_id"],
            "l3_plans": len(plans),
            "leaf_steps": sum(len(plan["steps"]) for plan in plans),
            "index_path": (
                f"{self.repository.project_dir_label}/"
                "l3_research_plans/index.json"
            ),
        }
