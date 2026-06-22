from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FileSystemResearchProjectRepository:
    """Filesystem adapter for full research-project report assembly."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    @property
    def project_dir_label(self) -> str:
        return str(self.project_dir)

    def load_project(self) -> dict[str, Any]:
        return _read_json(self.project_dir / "project.json")

    def load_qa_tree(self) -> dict[str, Any]:
        return _read_json(self.project_dir / "qa_tree.json")

    def load_workbench_for_report(self) -> dict[str, Any]:
        return _read_json(self.project_dir / "investment_workbench.json")

    def load_sources_for_report(self) -> list[dict[str, Any]]:
        sources_path = self.project_dir / "sources.jsonl"
        evidence_path = self.project_dir / "evidence.jsonl"
        if sources_path.exists():
            return _read_jsonl(sources_path)
        if evidence_path.exists():
            return _read_jsonl(evidence_path)
        return []

    def load_targets_for_report(self) -> list[dict[str, Any]]:
        workbench = _read_json(self.project_dir / "investment_workbench.json")
        return workbench.get("scoring_worksheet") or workbench.get("targets") or []


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows
