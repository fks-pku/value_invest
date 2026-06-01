from __future__ import annotations

from dataclasses import dataclass

from value_invest_research.domain.domain_playbooks import DomainPlaybook, resolve_domain_playbook
from value_invest_research.domain.question_architecture import QuestionArchitecture, build_question_architecture
from value_invest_research.domain.research_goal import ResearchGoal


@dataclass(frozen=True)
class PlanResearchGoal:
    """Convert one research objective into a domain-adapted QA architecture."""

    def execute(self, goal: ResearchGoal, *, playbook: DomainPlaybook | None = None) -> QuestionArchitecture:
        resolved_playbook = playbook or resolve_domain_playbook(goal)
        return build_question_architecture(goal, resolved_playbook)
