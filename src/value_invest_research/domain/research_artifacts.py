from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


Issue = dict[str, str]


@dataclass(frozen=True)
class ResearchArtifacts:
    """Structured artifacts needed to validate a complete research project."""

    qa_tree: dict[str, Any] = field(default_factory=dict)
    sources: list[dict[str, Any]] = field(default_factory=list)
    source_extractions: list[dict[str, Any]] = field(default_factory=list)
    leaf_source_reviews: list[dict[str, Any]] = field(default_factory=list)
    workbench: dict[str, Any] = field(default_factory=dict)
    targets: list[dict[str, Any]] = field(default_factory=list)
    load_issues: list[Issue] = field(default_factory=list)


@dataclass(frozen=True)
class ResearchArtifactValidationResult:
    """Application-facing validation result with stable CLI summary fields."""

    ok: bool
    project_dir: str
    qa_nodes: int
    source_extractions: int
    leaf_source_reviews: int
    targets: int
    issues: list[Issue]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "project_dir": self.project_dir,
            "summary": {
                "qa_nodes": self.qa_nodes,
                "source_extractions": self.source_extractions,
                "leaf_source_reviews": self.leaf_source_reviews,
                "targets": self.targets,
            },
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class ReportDocument:
    """A rendered public report loaded from an external source."""

    html: str = ""
    load_issues: list[Issue] = field(default_factory=list)


@dataclass(frozen=True)
class ReportContractValidationResult:
    """Application-facing report contract validation result."""

    ok: bool
    path: str
    mode: str
    level1_cards: int
    level2_cards: int
    level3_cards: int
    issues: list[Issue]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "path": self.path,
            "summary": {
                "mode": self.mode,
                "level1_cards": self.level1_cards,
                "level2_cards": self.level2_cards,
                "level3_cards": self.level3_cards,
            },
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class SourceList:
    """Source records loaded for time-slice auditing."""

    sources: list[dict[str, Any]] = field(default_factory=list)
    load_issues: list[Issue] = field(default_factory=list)


@dataclass(frozen=True)
class TimeSliceAuditResult:
    """Application-facing time-slice audit result."""

    ok: bool
    path: str
    as_of_date: str
    sources: int
    post_cutoff_non_label_count: int
    label_only_count: int
    quarantined_count: int
    issues: list[Issue]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "path": self.path,
            "summary": {
                "as_of_date": self.as_of_date,
                "sources": self.sources,
                "post_cutoff_non_label_count": self.post_cutoff_non_label_count,
                "label_only_count": self.label_only_count,
                "quarantined_count": self.quarantined_count,
            },
            "issues": list(self.issues),
        }
