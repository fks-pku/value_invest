from __future__ import annotations

from dataclasses import dataclass
from typing import Any


RESEARCH_TYPE_MAP = {
    "industry": "industry_theme",
    "theme": "industry_theme",
    "industry_theme": "industry_theme",
    "single_company": "single_company",
    "company": "single_company",
    "event": "event_policy",
    "policy": "event_policy",
    "event_policy": "event_policy",
    "technology": "technology_route",
    "product": "technology_route",
    "technology_route": "technology_route",
    "target_update": "target_update",
    "custom": "custom",
}

DEFAULT_Q_MAP = {
    "industry_theme": {
        "Q1": "Demand reality and future space",
        "Q2": "Value-capture bottlenecks and chokepoints",
        "Q3": "Disconfirming tests and priced-in risk",
        "Q4": "Specific target observation list",
    },
    "single_company": {
        "Q1": "Growth drivers",
        "Q2": "Moat, unit economics, and value capture",
        "Q3": "Financial quality, valuation, and disconfirming tests",
        "Q4": "Observation decision and monitoring list",
    },
    "event_policy": {
        "Q1": "Event facts and scope",
        "Q2": "Transmission mechanism",
        "Q3": "Beneficiaries, losers, and second-order effects",
        "Q4": "Disconfirming tests and watchlist",
    },
    "technology_route": {
        "Q1": "Technical feasibility and adoption demand",
        "Q2": "Bottlenecks and ecosystem readiness",
        "Q3": "Commercialization, competition, and disconfirming tests",
        "Q4": "Exposed assets and monitoring list",
    },
    "target_update": {
        "Q1": "What changed",
        "Q2": "Which thesis node changed",
        "Q3": "Whether price, risk, or reward changed",
        "Q4": "Observation-strength update",
    },
    "custom": {
        "Q1": "Primary driver reality",
        "Q2": "Value-capture mechanism",
        "Q3": "Risk, valuation, and disconfirming tests",
        "Q4": "Specific observation list",
    },
}

DEFAULT_RESEARCH_RUN_MODE = "historical_backtest"


@dataclass(frozen=True)
class ResearchGoal:
    """Research objective before domain-specific question design."""

    topic: str
    research_type: str = "custom"
    object_id: str = ""
    run_mode: str = DEFAULT_RESEARCH_RUN_MODE
    report_date: str = ""
    as_of_date: str = ""
    decision_boundary: str = "research observation, not trading instruction"
    domain_hint: str = ""

    def normalized_type(self) -> str:
        return normalize_research_type(self.research_type)

    def q_map(self) -> dict[str, str]:
        return dict(DEFAULT_Q_MAP[self.normalized_type()])

    def to_dict(self) -> dict[str, Any]:
        return {
            "topic": self.topic,
            "research_type": self.normalized_type(),
            "object_id": self.object_id,
            "run_mode": self.run_mode,
            "report_date": self.report_date,
            "as_of_date": self.as_of_date,
            "decision_boundary": self.decision_boundary,
            "domain_hint": self.domain_hint,
            "q_map": self.q_map(),
        }


def normalize_research_type(value: str) -> str:
    key = str(value or "custom").strip().lower().replace("-", "_").replace("/", "_")
    return RESEARCH_TYPE_MAP.get(key, "custom")
