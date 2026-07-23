from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FileSystemBomProjectLayoutRepository:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    @property
    def project_dir_label(self) -> str:
        return str(self.project_dir)

    def load_layout_bundle(self) -> dict[str, Any]:
        load_issues: list[dict[str, str]] = []
        parent = _read_json(self.project_dir / "project.json", load_issues)
        if parent.get("project_scope") != "industry_chain":
            return {"parent_project": parent, "manifest": {}, "children": [], "load_issues": load_issues}
        manifest_path = self.project_dir / str(parent.get("bom_manifest_path") or "boms/manifest.json")
        manifest = _read_json(manifest_path, load_issues)
        children = []
        for node in manifest.get("nodes") or []:
            node_id = str(node.get("node_id") or "")
            child_dir = self.project_dir / str(node.get("directory") or f"boms/{node_id}")
            child_project = _read_json(child_dir / "project.json", load_issues)
            report_name = Path(str(node.get("report_path") or "professional_report.md")).name
            children.append(
                {
                    "node_id": node_id,
                    "project": child_project,
                    "report_exists": (child_dir / report_name).is_file(),
                    "sources_exists": (child_dir / "sources.jsonl").is_file(),
                    "research_run_exists": (child_dir / "research_run.json").is_file(),
                    "temporal_manifest_exists": (child_dir / "temporal_manifest.json").is_file(),
                    "ledger_exists": (child_dir / "ledger" / "claims.jsonl").is_file(),
                    "snapshot_exists": any((child_dir / "snapshots").glob("*/thesis_snapshot.json")),
                }
            )
        return {
            "parent_project": parent,
            "manifest": manifest,
            "children": children,
            "load_issues": load_issues,
        }


def _read_json(path: Path, issues: list[dict[str, str]]) -> dict[str, Any]:
    if not path.is_file():
        issues.append({"severity": "error", "code": "missing_layout_file", "message": f"{path} does not exist"})
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append({"severity": "error", "code": "invalid_layout_file", "message": f"{path}: {exc}"})
        return {}
