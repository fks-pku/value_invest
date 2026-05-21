from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


class ValidationError(ValueError):
    """Raised when a research record violates the evidence contract."""


RELIABILITY_LEVELS = {"primary", "high", "medium", "low"}
MATERIALITY_LEVELS = {"low", "medium", "high", "thesis_change"}
INFORMATION_CATEGORIES = {"evidence", "research_report", "opinion", "message"}
VIEWS = {"watch", "attractive", "expensive", "avoid", "needs_review"}
CONFIDENCE_LEVELS = {"low", "medium", "high"}


OFFICIAL_SOURCE_TYPES = {
    "annual_report",
    "company_ir",
    "ipo_prospectus",
    "regulator_notice",
    "results_announcement",
    "sec_fact",
    "sec_filing",
}
RESEARCH_REPORT_SOURCE_TYPES = {
    "industry_data",
    "sell_side_report",
    "sell_side_report_summary",
}
OPINION_SOURCE_TYPES = {
    "blog",
    "expert_call",
    "interview",
    "opinion",
    "social_media",
}
MESSAGE_SOURCE_TYPES = {
    "media",
    "media_transcript",
    "news",
    "rumor",
}


def _require_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{key} must be a non-empty string")
    return value.strip()


def _string_list(data: dict[str, Any], key: str) -> list[str]:
    value = data.get(key, [])
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValidationError(f"{key} must be a list of strings")
    return [item.strip() for item in value if item.strip()]


def _validate_datetime(value: str | None, key: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{key} must be an ISO timestamp or null")
    normalized = value.replace("Z", "+00:00")
    try:
        datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValidationError(f"{key} must be an ISO timestamp") from exc
    return value


def infer_information_category(source_type: str, reliability: str) -> str:
    """Map source metadata into the four research information buckets."""
    normalized = source_type.strip().lower()
    if normalized in OFFICIAL_SOURCE_TYPES:
        return "evidence"
    if normalized in RESEARCH_REPORT_SOURCE_TYPES:
        return "research_report"
    if normalized in OPINION_SOURCE_TYPES:
        return "opinion"
    if normalized in MESSAGE_SOURCE_TYPES:
        return "message"
    if reliability == "primary":
        return "evidence"
    if reliability == "low":
        return "message"
    return "research_report"


@dataclass(frozen=True)
class EvidenceRecord:
    id: str
    research_object: str
    source_type: str
    source_name: str
    url: str
    published_at: str | None
    fetched_at: str
    hash: str
    tickers: list[str] = field(default_factory=list)
    sectors: list[str] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)
    summary: str = ""
    reliability: str = "medium"
    materiality: str = "low"
    information_category: str = "message"
    used_in: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvidenceRecord":
        reliability = _require_string(data, "reliability")
        if reliability not in RELIABILITY_LEVELS:
            raise ValidationError(f"reliability must be one of {sorted(RELIABILITY_LEVELS)}")

        materiality = _require_string(data, "materiality")
        if materiality not in MATERIALITY_LEVELS:
            raise ValidationError(f"materiality must be one of {sorted(MATERIALITY_LEVELS)}")
        if reliability == "low" and materiality == "thesis_change":
            raise ValidationError("low-reliability evidence cannot trigger a thesis_change")

        information_category = data.get("information_category")
        if information_category is None:
            information_category = infer_information_category(_require_string(data, "source_type"), reliability)
        elif not isinstance(information_category, str) or information_category not in INFORMATION_CATEGORIES:
            raise ValidationError(f"information_category must be one of {sorted(INFORMATION_CATEGORIES)}")

        return cls(
            id=_require_string(data, "id"),
            research_object=_require_string(data, "research_object"),
            source_type=_require_string(data, "source_type"),
            source_name=_require_string(data, "source_name"),
            url=_require_string(data, "url"),
            published_at=_validate_datetime(data.get("published_at"), "published_at"),
            fetched_at=_validate_datetime(_require_string(data, "fetched_at"), "fetched_at") or "",
            hash=_require_string(data, "hash"),
            tickers=_string_list(data, "tickers"),
            sectors=_string_list(data, "sectors"),
            themes=_string_list(data, "themes"),
            summary=_require_string(data, "summary"),
            reliability=reliability,
            materiality=materiality,
            information_category=information_category,
            used_in=_string_list(data, "used_in"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "research_object": self.research_object,
            "source_type": self.source_type,
            "source_name": self.source_name,
            "url": self.url,
            "published_at": self.published_at,
            "fetched_at": self.fetched_at,
            "hash": self.hash,
            "tickers": list(self.tickers),
            "sectors": list(self.sectors),
            "themes": list(self.themes),
            "summary": self.summary,
            "reliability": self.reliability,
            "materiality": self.materiality,
            "information_category": self.information_category,
            "used_in": list(self.used_in),
        }


@dataclass(frozen=True)
class SignalDriver:
    type: str
    item: str
    evidence_id: str

    def validate(self) -> None:
        if self.type not in {"positive", "negative", "mixed", "neutral"}:
            raise ValidationError("driver type must be positive, negative, mixed, or neutral")
        if not self.item.strip():
            raise ValidationError("driver item must be non-empty")
        if not self.evidence_id.strip():
            raise ValidationError("signal drivers must include evidence_id")


@dataclass(frozen=True)
class StockSignal:
    ticker: str
    date: str
    view: str
    confidence: str
    signal_strength: int
    time_horizon: str
    changed_since_last_run: bool
    drivers: list[SignalDriver]
    action_for_human: list[str]

    def validate(self) -> None:
        if not self.ticker.strip():
            raise ValidationError("ticker must be non-empty")
        if self.view not in VIEWS:
            raise ValidationError(f"view must be one of {sorted(VIEWS)}")
        if self.confidence not in CONFIDENCE_LEVELS:
            raise ValidationError(f"confidence must be one of {sorted(CONFIDENCE_LEVELS)}")
        if not -3 <= self.signal_strength <= 3:
            raise ValidationError("signal_strength must be between -3 and 3")
        if not self.drivers:
            raise ValidationError("stock signal requires at least one driver")
        for driver in self.drivers:
            driver.validate()
        if not self.action_for_human:
            raise ValidationError("action_for_human must contain at least one review action")
