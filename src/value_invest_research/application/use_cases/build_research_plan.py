from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from value_invest_research.domain.question_architecture import QuestionArchitecture
from value_invest_research.domain.l3_research_plan import build_l3_research_plan_set
from value_invest_research.domain.research_plan import build_research_plan, enrich_question_architecture
from value_invest_research.ports.repositories import ResearchPlanRepository, SourceUniverseRepository


@dataclass(frozen=True)
class BuildResearchPlan:
    """Build and persist an executable plan from a question architecture."""

    repository: ResearchPlanRepository
    source_universe_repository: SourceUniverseRepository | None = None

    def execute(self, architecture: QuestionArchitecture) -> dict[str, Any]:
        architecture_payload = architecture.to_dict()
        source_universe = (
            self.source_universe_repository.resolve_for_research(architecture_payload)
            if self.source_universe_repository is not None
            else {}
        )
        plan = build_research_plan(architecture, source_universe=source_universe)
        plan_payload = plan.to_dict()
        l3_nodes = [
            node.to_dict()
            for node in architecture.nodes
            if node.level == 3
        ]
        l3_index, l3_plans = build_l3_research_plan_set(
            l3_nodes=l3_nodes,
            parent_plan_id=plan.plan_id,
            research_goal=architecture.research_goal.to_dict(),
            source_universe=source_universe,
        )
        self.repository.save_question_architecture(enrich_question_architecture(architecture, plan))
        self.repository.save_plan(plan_payload)
        self.repository.save_l3_research_plans(l3_index, l3_plans)
        return {
            "plan_id": plan.plan_id,
            "plan_path": self.repository.plan_path_label,
            "event_path": self.repository.event_path_label,
            "steps": len(plan.steps),
            "l3_plans": len(l3_plans),
            "leaf_steps": sum(len(row["steps"]) for row in l3_plans),
            "plan": plan_payload,
        }
