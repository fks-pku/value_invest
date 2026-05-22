from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from value_invest_research.research_system import SOURCE_ORIGIN_INFO_ORDER, normalize_ticker


def validate_stock_qa_system(
    root: Path,
    ticker: str,
    require_professional_report: bool = False,
) -> dict[str, Any]:
    """Validate that a stock QA system satisfies the layered research contract."""
    normalized = normalize_ticker(ticker)
    research_dir = root / "stocks" / normalized / "research_system"
    return _validate_container(
        container_dir=research_dir,
        object_type="stock",
        object_id=normalized,
        require_professional_report=require_professional_report,
    )


def validate_meta_qa_system(
    root: Path,
    project_id: str,
    require_professional_report: bool = False,
) -> dict[str, Any]:
    """Validate that a generic meta-QA project satisfies the layered research contract."""
    project_dir = root / "research" / "qa_projects" / project_id
    return _validate_container(
        container_dir=project_dir,
        object_type="meta_qa",
        object_id=project_id,
        require_professional_report=require_professional_report,
    )


def _validate_container(
    container_dir: Path,
    object_type: str,
    object_id: str,
    require_professional_report: bool,
) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    qa_tree_path = container_dir / "qa_tree.json"
    collection_path = container_dir / "information_collection.jsonl"
    dashboard_path = container_dir / "research_dashboard.html"
    report_path = container_dir / "research_report.html"
    professional_report_path = container_dir / "professional_report.html"

    qa_tree = _read_json_or_issue(qa_tree_path, issues)
    collection_rows = _read_jsonl_or_issue(collection_path, issues)
    _require_file(dashboard_path, issues, "missing_dashboard", "缺少 research_dashboard.html。")
    _require_file(report_path, issues, "missing_research_report", "缺少 research_report.html。")
    if require_professional_report:
        _require_file(
            professional_report_path,
            issues,
            "missing_professional_report",
            "缺少 professional_report.html；需要先运行 write-professional-report 或队列闭环参数。",
        )

    if not qa_tree:
        return _validation_result(object_type, object_id, container_dir, issues, {}, [], collection_rows)

    nodes = [node for node in qa_tree.get("nodes", []) if isinstance(node, dict)]
    nodes_by_id = {str(node.get("id", "")): node for node in nodes if node.get("id")}
    default_depth = int(qa_tree.get("default_depth", 3) or 3)
    root_nodes = [node for node in nodes if _node_level(node, default=-1) == 0]
    if not root_nodes:
        _add_issue(issues, "error", "missing_root_question", "缺少 L0 元问题节点。")
    elif not str(root_nodes[0].get("question", "")).strip():
        _add_issue(issues, "error", "empty_root_question", "L0 元问题节点没有问题文本。")

    for node in nodes:
        node_id = str(node.get("id", ""))
        level = _node_level(node)
        if level > default_depth:
            _add_issue(issues, "error", "depth_exceeded", f"{node_id} 超过默认最大深度 {default_depth}。")
        for child_id in node.get("next_question_ids", []) or []:
            child = nodes_by_id.get(str(child_id))
            if child is None:
                _add_issue(issues, "error", "missing_child_node", f"{node_id} 指向不存在的子问题 {child_id}。")
                continue
            if child.get("parent_id") != node_id:
                _add_issue(issues, "error", "broken_parent_link", f"{child_id} 的 parent_id 与父节点 {node_id} 不一致。")

    leaves = [_node for _node in nodes if _is_leaf(qa_tree, _node)]
    collection_index = _collection_index(collection_rows)
    for leaf in leaves:
        _validate_leaf(leaf, collection_index, issues)

    summary = {
        "nodes": len(nodes),
        "root_questions": len(root_nodes),
        "leaf_questions": len(leaves),
        "default_depth": default_depth,
        "collection_rows": len(collection_rows),
        "dashboard_path": str(dashboard_path),
        "report_path": str(report_path),
        "professional_report_path": str(professional_report_path) if professional_report_path.exists() else "",
    }
    return _validation_result(object_type, object_id, container_dir, issues, summary, leaves, collection_rows)


def _validate_leaf(
    leaf: dict[str, Any],
    collection_index: dict[tuple[str, str], dict[str, Any]],
    issues: list[dict[str, str]],
) -> None:
    node_id = str(leaf.get("id", ""))
    missing_categories = [
        category for category in SOURCE_ORIGIN_INFO_ORDER if (node_id, category) not in collection_index
    ]
    if missing_categories:
        _add_issue(
            issues,
            "error",
            "leaf_missing_information_categories",
            f"{node_id} 缺少四类信息索引：{', '.join(missing_categories)}。",
        )
    answer = leaf.get("professional_answer", {})
    if not isinstance(answer, dict) or not str(answer.get("answer", "")).strip():
        _add_issue(issues, "error", "leaf_missing_professional_answer", f"{node_id} 缺少专业回答。")
    if not str(leaf.get("current_answer", "")).strip():
        _add_issue(issues, "error", "leaf_missing_current_answer", f"{node_id} 缺少当前回答。")


def _is_leaf(qa_tree: dict[str, Any], node: dict[str, Any]) -> bool:
    return _node_level(node) >= int(qa_tree.get("default_depth", 3) or 3) or not node.get("next_question_ids")


def _node_level(node: dict[str, Any], default: int = 0) -> int:
    value = node.get("level", default)
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _collection_index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (str(row.get("node_id", "")), str(row.get("category", ""))): row
        for row in rows
        if isinstance(row, dict)
    }


def _read_json_or_issue(path: Path, issues: list[dict[str, str]]) -> dict[str, Any]:
    if not path.exists():
        _add_issue(issues, "error", "missing_qa_tree", f"缺少 {path.name}。")
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _add_issue(issues, "error", "invalid_qa_tree", f"{path.name} 不是合法 JSON：{exc}。")
        return {}
    if not isinstance(data, dict):
        _add_issue(issues, "error", "invalid_qa_tree", f"{path.name} 顶层必须是对象。")
        return {}
    return data


def _read_jsonl_or_issue(path: Path, issues: list[dict[str, str]]) -> list[dict[str, Any]]:
    if not path.exists():
        _add_issue(issues, "error", "missing_information_collection", f"缺少 {path.name}。")
        return []
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            _add_issue(issues, "error", "invalid_information_collection", f"{path.name}:{line_number}: {exc}。")
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def _require_file(path: Path, issues: list[dict[str, str]], code: str, message: str) -> None:
    if not path.exists():
        _add_issue(issues, "error", code, message)


def _add_issue(issues: list[dict[str, str]], severity: str, code: str, message: str) -> None:
    issues.append({"severity": severity, "code": code, "message": message})


def _validation_result(
    object_type: str,
    object_id: str,
    container_dir: Path,
    issues: list[dict[str, str]],
    summary: dict[str, Any],
    leaves: list[dict[str, Any]],
    collection_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    errors = [issue for issue in issues if issue["severity"] == "error"]
    category_counts = {category: 0 for category in SOURCE_ORIGIN_INFO_ORDER}
    for row in collection_rows:
        category = str(row.get("category", ""))
        if category in category_counts:
            category_counts[category] += 1
    return {
        "ok": not errors,
        "object_type": object_type,
        "object_id": object_id,
        "container_dir": str(container_dir),
        "summary": {
            **summary,
            "leaf_questions": summary.get("leaf_questions", len(leaves)),
            "information_category_rows": category_counts,
            "issues": len(issues),
            "errors": len(errors),
        },
        "issues": issues,
    }
