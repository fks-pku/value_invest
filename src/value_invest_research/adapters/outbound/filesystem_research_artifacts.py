from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from value_invest_research.domain.research_artifacts import Issue, ReportDocument, ResearchArtifacts, SourceList


class FileSystemResearchArtifactRepository:
    """File-system implementation of the research artifact repository port."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    @property
    def project_dir_label(self) -> str:
        return str(self.project_dir)

    def load_research_artifacts(self) -> ResearchArtifacts:
        qa_path = self.project_dir / "qa_tree.json"
        source_extractions_path = self.project_dir / "source_extractions.jsonl"
        leaf_source_reviews_path = self.project_dir / "leaf_source_reviews.jsonl"
        sources_path = self.project_dir / "sources.jsonl"
        workbench_path = self.project_dir / "investment_workbench.json"

        issues: list[Issue] = []
        qa_tree: dict[str, Any] = {}
        sources: list[dict[str, Any]] = []
        source_extractions: list[dict[str, Any]] = []
        leaf_source_reviews: list[dict[str, Any]] = []
        workbench: dict[str, Any] = {}
        targets: list[dict[str, Any]] = []

        if qa_path.exists():
            qa_tree = json.loads(qa_path.read_text(encoding="utf-8"))
        else:
            issues.append({"severity": "error", "code": "missing_qa_tree", "message": f"{qa_path} does not exist"})

        if source_extractions_path.exists():
            source_extractions = _read_jsonl(source_extractions_path)
        else:
            issues.append({
                "severity": "error",
                "code": "missing_source_extractions",
                "message": f"{source_extractions_path} does not exist",
            })

        if sources_path.exists():
            sources = _read_jsonl(sources_path)

        if leaf_source_reviews_path.exists():
            leaf_source_reviews = _read_jsonl(leaf_source_reviews_path)
        else:
            issues.append({
                "severity": "error",
                "code": "missing_leaf_source_reviews",
                "message": f"{leaf_source_reviews_path} does not exist",
            })

        if workbench_path.exists():
            workbench = json.loads(workbench_path.read_text(encoding="utf-8"))
            targets = workbench.get("scoring_worksheet") or workbench.get("targets") or []
        else:
            issues.append({"severity": "error", "code": "missing_workbench", "message": f"{workbench_path} does not exist"})

        return ResearchArtifacts(
            qa_tree=qa_tree,
            sources=sources,
            source_extractions=source_extractions,
            leaf_source_reviews=leaf_source_reviews,
            workbench=workbench,
            targets=targets,
            load_issues=issues,
        )


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
    return rows


class FileSystemReportDocumentRepository:
    """File-system implementation of the report document repository port."""

    def __init__(self, report_path: Path):
        self.report_path = report_path

    @property
    def report_path_label(self) -> str:
        return str(self.report_path)

    def load_report_document(self) -> ReportDocument:
        if not self.report_path.exists():
            return ReportDocument(
                load_issues=[
                    {
                        "severity": "error",
                        "code": "missing_report_document",
                        "message": f"{self.report_path} does not exist",
                    }
                ]
            )
        content = self.report_path.read_text(encoding="utf-8")
        if self.report_path.suffix.lower() in {".md", ".markdown"}:
            return ReportDocument(markdown=content)
        return ReportDocument(html=content)


class FileSystemSourceListRepository:
    """File-system implementation of the source-list repository port."""

    def __init__(self, source_path: Path):
        self.source_path = source_path

    @property
    def source_path_label(self) -> str:
        return str(self.source_path)

    def load_sources(self) -> SourceList:
        if not self.source_path.exists():
            return SourceList(
                load_issues=[
                    {
                        "severity": "error",
                        "code": "missing_sources_jsonl",
                        "message": f"{self.source_path} does not exist",
                    }
                ]
            )
        return SourceList(sources=_read_jsonl(self.source_path))


class FileSystemSourceParsingArtifactWriter:
    """File-system writer for source parser and GPT review audit records."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    def append_source_extractions(self, records: list[dict]) -> None:
        _append_jsonl(self.project_dir / "source_extractions.jsonl", records)

    def append_leaf_source_reviews(self, records: list[dict]) -> None:
        _append_jsonl(self.project_dir / "leaf_source_reviews.jsonl", records)


def _append_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
