from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from value_invest_research.application.use_cases.plan_research_goal import PlanResearchGoal
from value_invest_research.application.use_cases.render_research_project_report import RenderResearchProjectReport
from value_invest_research.domain.question_architecture import QuestionArchitecture
from value_invest_research.domain.research_goal import ResearchGoal
from value_invest_research.ports.renderers import CanonicalReportRenderer
from value_invest_research.ports.repositories import ResearchProjectRepository


@dataclass(frozen=True)
class ResearchOrchestrator:
    """Application-level coordinator for the canonical research workflow.

    The orchestrator keeps sequencing decisions outside domain models and outside
    adapters. Domain code designs questions; adapters load files or render HTML.
    """

    question_planner: PlanResearchGoal = field(default_factory=PlanResearchGoal)

    def plan(self, goal: ResearchGoal) -> QuestionArchitecture:
        return self.question_planner.execute(goal)

    def render_report(
        self,
        repository: ResearchProjectRepository,
        renderer: CanonicalReportRenderer,
        *,
        filename: str = "professional_report.md",
    ) -> dict[str, Any]:
        return RenderResearchProjectReport(repository, renderer).execute(filename=filename)
