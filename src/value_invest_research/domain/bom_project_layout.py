from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any, Iterable


_SAFE_NODE_ID = re.compile(r"^[A-Za-z0-9_-]+$")


@dataclass(frozen=True)
class BomProjectLayoutEntry:
    node_id: str
    public_name: str
    child_project_id: str
    directory: str
    project_path: str
    report_path: str
    compatibility_html_path: str
    sources_path: str
    research_run_path: str | None
    temporal_manifest_path: str
    ledger_directory: str
    snapshots_directory: str


def build_bom_project_layout(
    parent_project_id: str,
    nodes: Iterable[dict[str, Any]],
    *,
    research_run_node_ids: Iterable[str] = (),
) -> dict[str, Any]:
    """Build the canonical parent-project to BOM-child-project layout."""

    if not parent_project_id.strip():
        raise ValueError("parent_project_id must be non-empty")

    research_nodes = {str(node_id) for node_id in research_run_node_ids}
    entries: list[BomProjectLayoutEntry] = []
    seen: set[str] = set()
    for raw_node in nodes:
        node_id = str(raw_node.get("id") or raw_node.get("node_id") or "").strip()
        public_name = str(raw_node.get("name") or raw_node.get("public_name") or "").strip()
        if not _SAFE_NODE_ID.fullmatch(node_id):
            raise ValueError(f"unsafe BOM node id: {node_id!r}")
        if not public_name:
            raise ValueError(f"BOM node {node_id!r} must have a public name")
        if node_id in seen:
            raise ValueError(f"duplicate BOM node id: {node_id}")
        seen.add(node_id)
        directory = f"boms/{node_id}"
        entries.append(
            BomProjectLayoutEntry(
                node_id=node_id,
                public_name=public_name,
                child_project_id=f"{parent_project_id}__bom__{node_id}",
                directory=directory,
                project_path=f"{directory}/project.json",
                report_path=f"{directory}/professional_report.md",
                compatibility_html_path=f"{directory}/professional_report.html",
                sources_path=f"{directory}/sources.jsonl",
                research_run_path=(
                    f"{directory}/research_run.json" if node_id in research_nodes else None
                ),
                temporal_manifest_path=f"{directory}/temporal_manifest.json",
                ledger_directory=f"{directory}/ledger",
                snapshots_directory=f"{directory}/snapshots",
            )
        )

    if not entries:
        raise ValueError("at least one BOM node is required")
    unknown_research_nodes = research_nodes - seen
    if unknown_research_nodes:
        raise ValueError(
            "research run node ids are outside the canonical BOM registry: "
            + ", ".join(sorted(unknown_research_nodes))
        )

    return {
        "schema_version": "1.0",
        "parent_project_id": parent_project_id,
        "project_scope": "industry_chain",
        "bom_root": "boms",
        "nodes": [asdict(entry) for entry in entries],
    }


def validate_bom_project_layout_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    """Validate parent/manifest/child identity without filesystem knowledge."""

    issues: list[dict[str, str]] = list(bundle.get("load_issues") or [])
    parent = bundle.get("parent_project") or {}
    manifest = bundle.get("manifest") or {}
    children = bundle.get("children") or []
    if parent.get("project_scope") != "industry_chain":
        return {"ok": True, "issues": issues, "summary": {"project_scope": parent.get("project_scope") or "legacy"}}
    if manifest.get("parent_project_id") != parent.get("project_id"):
        _layout_issue(issues, "manifest_parent_mismatch", "BOM manifest parent_project_id must match parent project_id")
    manifest_nodes = manifest.get("nodes") or []
    parent_nodes = parent.get("bom_projects") or []
    manifest_ids = [str(node.get("node_id") or "") for node in manifest_nodes]
    parent_ids = [str(node.get("node_id") or "") for node in parent_nodes]
    if not manifest_ids or manifest_ids != parent_ids:
        _layout_issue(issues, "parent_manifest_node_drift", "parent project and BOM manifest must preserve the same ordered node ids")
    if len(manifest_ids) != len(set(manifest_ids)):
        _layout_issue(issues, "duplicate_manifest_node", "BOM manifest node ids must be unique")

    children_by_id = {str(child.get("node_id") or ""): child for child in children}
    if set(children_by_id) != set(manifest_ids):
        _layout_issue(issues, "child_project_coverage", "every manifest node must have exactly one loaded child project")
    for node in manifest_nodes:
        node_id = str(node.get("node_id") or "")
        expected_directory = f"boms/{node_id}"
        if not _SAFE_NODE_ID.fullmatch(node_id) or node.get("directory") != expected_directory:
            _layout_issue(issues, "unsafe_child_directory", f"{node_id or '<empty>'} must use {expected_directory}")
        child = children_by_id.get(node_id) or {}
        child_project = child.get("project") or {}
        if child_project.get("project_scope") != "bom_node":
            _layout_issue(issues, "child_scope", f"{node_id} child project must use project_scope=bom_node")
        if child_project.get("parent_project_id") != parent.get("project_id"):
            _layout_issue(issues, "child_parent_mismatch", f"{node_id} child parent_project_id does not match")
        if child_project.get("bom_node_id") != node_id:
            _layout_issue(issues, "child_node_mismatch", f"{node_id} child bom_node_id does not match")
        for field in ("report_exists", "sources_exists"):
            if not child.get(field):
                _layout_issue(issues, f"child_{field}", f"{node_id} child is missing {field.replace('_exists', '')}")
        if node.get("research_run_path") and not child.get("research_run_exists"):
            _layout_issue(issues, "child_research_run_missing", f"{node_id} declares a research run that does not exist")
        for field in ("temporal_manifest_exists", "ledger_exists", "snapshot_exists"):
            if not child.get(field):
                _layout_issue(
                    issues,
                    f"child_{field}",
                    f"{node_id} child is missing its temporal research {field.replace('_exists', '')}",
                )

    return {
        "ok": not any(issue.get("severity") == "error" for issue in issues),
        "issues": issues,
        "summary": {
            "project_scope": "industry_chain",
            "bom_nodes": len(manifest_ids),
            "child_projects": len(children_by_id),
        },
    }


def _layout_issue(issues: list[dict[str, str]], code: str, message: str) -> None:
    issues.append({"severity": "error", "code": code, "message": message})
