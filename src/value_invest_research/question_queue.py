from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from value_invest_research.information_collection import (
    build_meta_qa_collection_tasks,
    build_research_collection_tasks,
    run_meta_qa_collection_tasks,
    run_research_collection_tasks,
)
from value_invest_research.research_system import add_research_question, normalize_ticker


def apply_research_question_queue(
    root: Path,
    ticker: str,
    path: Path,
    build_tasks: bool = True,
    run_local_collection: bool = False,
    limit: int | None = None,
    min_score: int = 4,
    synthesize_answers: bool = False,
    synthesis_client: Any | None = None,
    write_professional_report: bool = False,
    professional_report_client: Any | None = None,
) -> dict[str, Any]:
    """Apply queued user questions to a stock QA system and refresh downstream artifacts."""
    normalized = normalize_ticker(ticker)
    rows = _read_question_queue(path)
    results = _apply_rows(
        rows,
        add_one=lambda row: add_research_question(
            root,
            normalized,
            row["parent_id"],
            row["question"],
            terminal=bool(row.get("terminal")),
        ),
    )
    collection_result: dict[str, Any] = {}
    if run_local_collection:
        collection_result = run_research_collection_tasks(root, normalized, limit=limit, min_score=min_score)
    elif build_tasks:
        collection_result = build_research_collection_tasks(root, normalized, limit=limit)
    synthesis_result: dict[str, Any] = {}
    if synthesize_answers:
        from value_invest_research.answer_synthesis import run_stock_answer_synthesis

        synthesis_result = run_stock_answer_synthesis(root, normalized, limit=limit, apply=True, client=synthesis_client)
    professional_report_result: dict[str, Any] = {}
    if write_professional_report:
        from value_invest_research.report_synthesis import write_stock_professional_report

        professional_report_result = write_stock_professional_report(root, normalized, client=professional_report_client)
    last = results[-1]["result"] if results else {}
    return {
        "ticker": normalized,
        "input_path": str(path),
        "records": len(rows),
        "created": sum(1 for item in results if item["result"].get("created")),
        "existing": sum(1 for item in results if not item["result"].get("created")),
        "question_ids": [item["result"].get("question_id", "") for item in results],
        "dashboard_path": collection_result.get("dashboard_path", last.get("dashboard_path", "")),
        "report_path": collection_result.get("report_path", last.get("report_path", "")),
        "information_collection_path": collection_result.get(
            "information_collection_path",
            last.get("information_collection_path", ""),
        ),
        "task_path": collection_result.get("task_path", ""),
        "result_path": collection_result.get("result_path", ""),
        "tasks": collection_result.get("tasks", 0),
        "matches": collection_result.get("matches", 0),
        "synthesized_answers": synthesis_result.get("synthesized_answers", 0),
        "synthesized_answer_path": synthesis_result.get("synthesized_answer_path", ""),
        "synthesis_mode": synthesis_result.get("synthesis_mode", ""),
        "applied_nodes": synthesis_result.get("applied_nodes", 0),
        "professional_report_path": professional_report_result.get("professional_report_path", ""),
        "professional_report_md_path": professional_report_result.get("professional_report_md_path", ""),
        "professional_report_mode": professional_report_result.get("report_mode", ""),
    }


def apply_meta_qa_question_queue(
    root: Path,
    project_id: str,
    path: Path,
    build_tasks: bool = True,
    run_local_collection: bool = False,
    limit: int | None = None,
    min_score: int = 4,
    synthesize_answers: bool = False,
    synthesis_client: Any | None = None,
    write_professional_report: bool = False,
    professional_report_client: Any | None = None,
) -> dict[str, Any]:
    """Apply queued user questions to a generic QA project and refresh downstream artifacts."""
    from value_invest_research.meta_qa_research import add_meta_qa_question

    rows = _read_question_queue(path)
    results = _apply_rows(
        rows,
        add_one=lambda row: add_meta_qa_question(
            root,
            project_id,
            row["parent_id"],
            row["question"],
            terminal=bool(row.get("terminal")),
        ),
    )
    collection_result: dict[str, Any] = {}
    if run_local_collection:
        collection_result = run_meta_qa_collection_tasks(root, project_id, limit=limit, min_score=min_score)
    elif build_tasks:
        collection_result = build_meta_qa_collection_tasks(root, project_id, limit=limit)
    synthesis_result: dict[str, Any] = {}
    if synthesize_answers:
        from value_invest_research.answer_synthesis import run_meta_qa_answer_synthesis

        synthesis_result = run_meta_qa_answer_synthesis(root, project_id, limit=limit, apply=True, client=synthesis_client)
    professional_report_result: dict[str, Any] = {}
    if write_professional_report:
        from value_invest_research.report_synthesis import write_meta_qa_professional_report

        professional_report_result = write_meta_qa_professional_report(root, project_id, client=professional_report_client)
    last = results[-1]["result"] if results else {}
    return {
        "project_id": project_id,
        "input_path": str(path),
        "records": len(rows),
        "created": sum(1 for item in results if item["result"].get("created")),
        "existing": sum(1 for item in results if not item["result"].get("created")),
        "question_ids": [item["result"].get("question_id", "") for item in results],
        "dashboard_path": collection_result.get("dashboard_path", last.get("dashboard_path", "")),
        "report_path": collection_result.get("report_path", last.get("report_path", "")),
        "information_collection_path": collection_result.get(
            "information_collection_path",
            last.get("information_collection_path", ""),
        ),
        "task_path": collection_result.get("task_path", ""),
        "result_path": collection_result.get("result_path", ""),
        "tasks": collection_result.get("tasks", 0),
        "matches": collection_result.get("matches", 0),
        "synthesized_answers": synthesis_result.get("synthesized_answers", 0),
        "synthesized_answer_path": synthesis_result.get("synthesized_answer_path", ""),
        "synthesis_mode": synthesis_result.get("synthesis_mode", ""),
        "applied_nodes": synthesis_result.get("applied_nodes", 0),
        "professional_report_path": professional_report_result.get("professional_report_path", ""),
        "professional_report_md_path": professional_report_result.get("professional_report_md_path", ""),
        "professional_report_mode": professional_report_result.get("report_mode", ""),
    }


def _apply_rows(
    rows: list[dict[str, Any]],
    add_one: Callable[[dict[str, Any]], dict[str, Any]],
) -> list[dict[str, Any]]:
    results = []
    for index, row in enumerate(rows, start=1):
        normalized = _validated_question_row(row, index)
        results.append({"row": normalized, "result": add_one(normalized)})
    return results


def _read_question_queue(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise ValueError(f"question queue not found: {path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if text.startswith("["):
        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError("question queue JSON must be a list")
        return data
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: {exc}") from exc
        rows.append(row)
    return rows


def _validated_question_row(row: dict[str, Any], index: int) -> dict[str, Any]:
    if not isinstance(row, dict):
        raise ValueError(f"question row {index} must be an object")
    parent_id = row.get("parent_id") or row.get("requested_parent_id")
    question = row.get("question")
    missing = []
    if not isinstance(parent_id, str) or not parent_id.strip():
        missing.append("parent_id")
    if not isinstance(question, str) or not question.strip():
        missing.append("question")
    if missing:
        raise ValueError(f"question row {index} missing required fields: {', '.join(missing)}")
    return {
        "parent_id": parent_id.strip(),
        "question": question.strip(),
        "terminal": _terminal_question_flag(row),
    }


def _terminal_question_flag(row: dict[str, Any]) -> bool:
    if "terminal" in row:
        return _as_bool(row.get("terminal"))
    if "should_collect_information" in row:
        return _as_bool(row.get("should_collect_information"))
    if "should_drill_down" in row:
        return not _as_bool(row.get("should_drill_down"))
    return False


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "terminal"}
    return bool(value)
