from __future__ import annotations

from typing import Protocol

from value_invest_research.domain.research_artifacts import ReportDocument, ResearchArtifacts, SourceList


class ResearchArtifactRepository(Protocol):
    """Outbound port for loading persisted research artifacts."""

    @property
    def project_dir_label(self) -> str:
        """Stable label used in user-facing validation output."""

    def load_research_artifacts(self) -> ResearchArtifacts:
        """Load the artifacts required by the research quality gate."""


class ReportDocumentRepository(Protocol):
    """Outbound port for loading a rendered public report."""

    @property
    def report_path_label(self) -> str:
        """Stable label used in user-facing validation output."""

    def load_report_document(self) -> ReportDocument:
        """Load report HTML for contract validation."""


class SourceListRepository(Protocol):
    """Outbound port for loading source records used in time-slice audits."""

    @property
    def source_path_label(self) -> str:
        """Stable label used in user-facing audit output."""

    def load_sources(self) -> SourceList:
        """Load source records for cutoff auditing."""


class SourceUniverseRepository(Protocol):
    """Outbound port for resolving a professional source universe for a research object."""

    def resolve_for_research(self, qa_tree: dict) -> dict:
        """Return the best matching source-universe record for the QA tree."""


class ResearchProjectRepository(Protocol):
    """Outbound port for loading a full research project for report assembly."""

    @property
    def project_dir_label(self) -> str:
        """Stable label used in user-facing output."""

    def load_project(self) -> dict:
        """Load project metadata."""

    def load_qa_tree(self) -> dict:
        """Load the structured QA tree."""

    def load_workbench_for_report(self) -> dict:
        """Load structured research workbench artifacts used by public report assembly."""

    def load_sources_for_report(self) -> list[dict]:
        """Load source records for public source indexing."""

    def load_targets_for_report(self) -> list[dict]:
        """Load target ranking records for public report rendering."""


class BomProjectLayoutRepository(Protocol):
    """Outbound port for loading one industry project and its BOM children."""

    @property
    def project_dir_label(self) -> str:
        """Stable label used in validation output."""

    def load_layout_bundle(self) -> dict:
        """Load parent metadata, manifest, and child project existence facts."""


class TemporalResearchLedgerRepository(Protocol):
    """Outbound port for append-only BOM claims, snapshots, and revisions."""

    @property
    def project_dir_label(self) -> str:
        """Stable BOM child-project label."""

    def load_prior_snapshots(self) -> list[dict]:
        """Load prior as-of snapshots without mutating them."""

    def load_documents(self) -> list[dict]:
        """Load the accumulated source-document ledger."""

    def load_claims(self) -> list[dict]:
        """Load accumulated atomic claims for the next snapshot build."""

    def write_temporal_bundle(self, bundle: dict) -> None:
        """Persist documents, claims, revisions, coverage, and current snapshot."""


class SourceParsingArtifactWriter(Protocol):
    """Outbound port for persisting parser and GPT review records."""

    def append_source_extractions(self, records: list[dict]) -> None:
        """Append source-parser records to the project audit trail."""

    def append_leaf_source_reviews(self, records: list[dict]) -> None:
        """Append GPT verification records to the project audit trail."""


class LeafResearchResultRepository(Protocol):
    """Outbound port for merged leaf research result persistence."""

    @property
    def result_path_label(self) -> str:
        """Stable label for the normalized result JSONL file."""

    @property
    def source_path_label(self) -> str:
        """Stable label for the deduplicated source JSONL file."""

    def save_results(self, rows: list[dict]) -> dict[str, int]:
        """Persist normalized rows and return count metadata."""


class LeafResearchArtifactRepository(Protocol):
    """Outbound port for leaf research task/result/answer artifacts."""

    @property
    def task_path_label(self) -> str:
        """Stable label for the leaf task JSONL file."""

    @property
    def result_path_label(self) -> str:
        """Stable label for the normalized result JSONL file."""

    @property
    def answer_path_label(self) -> str:
        """Stable label for the synthesized leaf answer JSONL file."""

    @property
    def rollup_path_label(self) -> str:
        """Stable label for the rollup answer JSONL file."""

    def load_completed_leaf_node_ids(self) -> set[str]:
        """Load node ids that already have synthesized leaf answers."""

    def save_tasks(self, rows: list[dict]) -> int:
        """Persist leaf research tasks and return row count."""

    def load_tasks(self) -> list[dict]:
        """Load persisted leaf research tasks."""

    def load_results(self) -> list[dict]:
        """Load normalized leaf research result rows."""

    def save_leaf_answers(self, rows: list[dict]) -> int:
        """Persist synthesized leaf answers and return row count."""

    def save_rollup_answers(self, rows: list[dict]) -> int:
        """Persist parent rollup answers and return row count."""
