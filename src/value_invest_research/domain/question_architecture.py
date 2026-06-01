from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from value_invest_research.domain.domain_playbooks import DomainPlaybook
from value_invest_research.domain.research_goal import ResearchGoal


@dataclass(frozen=True)
class QuestionNode:
    """Question architecture node before evidence collection."""

    id: str
    level: int
    question: str
    parent_id: str = ""
    investment_relevance: str = ""
    decision_use: str = ""
    required_materials: list[str] = field(default_factory=list)
    support_evidence: str = ""
    refute_evidence: str = ""
    target_implications: str = ""
    preferred_specialty_skill: str = ""
    score_component: str = ""
    next_question_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "level": self.level,
            "question": self.question,
            "parent_id": self.parent_id,
            "investment_relevance": self.investment_relevance,
            "decision_use": self.decision_use,
            "required_materials": list(self.required_materials),
            "support_evidence": self.support_evidence,
            "refute_evidence": self.refute_evidence,
            "target_implications": self.target_implications,
            "preferred_specialty_skill": self.preferred_specialty_skill,
            "score_component": self.score_component,
            "next_question_ids": list(self.next_question_ids),
        }


@dataclass(frozen=True)
class QuestionArchitecture:
    """Complete domain-adapted QA plan, independent from report rendering."""

    research_goal: ResearchGoal
    playbook: DomainPlaybook
    planner_rationale: str
    nodes: list[QuestionNode]

    def to_dict(self) -> dict[str, Any]:
        return {
            "research_goal": self.research_goal.to_dict(),
            "playbook": self.playbook.to_dict(),
            "planner_rationale": self.planner_rationale,
            "nodes": [node.to_dict() for node in self.nodes],
        }


def build_question_architecture(goal: ResearchGoal, playbook: DomainPlaybook) -> QuestionArchitecture:
    """Build a max-three-layer QA tree from a goal and domain playbook."""
    nodes: list[QuestionNode] = []
    for qid in ("Q1", "Q2", "Q3", "Q4"):
        l2_templates = playbook.l2_templates.get(qid, [])
        nodes.append(
            QuestionNode(
                id=qid,
                level=1,
                question=playbook.q_map.get(qid, goal.q_map().get(qid, qid)),
                investment_relevance=_l1_relevance(qid),
                next_question_ids=[template.id for template in l2_templates],
            )
        )
        for template in l2_templates:
            l3_ids = [f"{template.id}.{index}" for index, _ in enumerate(template.l3_questions, start=1)]
            nodes.append(
                QuestionNode(
                    id=template.id,
                    level=2,
                    question=template.question,
                    parent_id=qid,
                    investment_relevance=template.why_this_depth,
                    next_question_ids=l3_ids,
                )
            )
            for index, leaf in enumerate(template.l3_questions, start=1):
                node_id = f"{template.id}.{index}"
                nodes.append(
                    QuestionNode(
                        id=node_id,
                        level=3,
                        question=str(leaf.get("question", "")),
                        parent_id=template.id,
                        investment_relevance=str(leaf.get("decision_use", "")),
                        decision_use=str(leaf.get("decision_use", "")),
                        required_materials=[str(item) for item in leaf.get("required_materials", [])],
                        support_evidence=str(leaf.get("support_evidence", "")),
                        refute_evidence=str(leaf.get("refute_evidence", "")),
                        target_implications=str(leaf.get("target_implications", "")),
                        preferred_specialty_skill=str(leaf.get("preferred_specialty_skill", "")),
                        score_component=str(leaf.get("score_component", "")),
                    )
                )
    return QuestionArchitecture(
        research_goal=goal,
        playbook=playbook,
        planner_rationale=(
            f"{playbook.playbook_id} playbook maps the research goal to Q1-Q4, "
            "then decomposes each direction into L2 mechanism buckets and L3 evidence units."
        ),
        nodes=nodes,
    )


def _l1_relevance(qid: str) -> str:
    return {
        "Q1": "Defines whether the opportunity exists and how large it can become.",
        "Q2": "Defines who can capture value and where scarcity sits.",
        "Q3": "Defines what would refute the thesis or cap valuation odds.",
        "Q4": "Converts verified conclusions into specific target observations.",
    }.get(qid, "")
