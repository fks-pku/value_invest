from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from value_invest_research.answer_synthesis import (
    build_meta_qa_synthesis_tasks,
    build_stock_synthesis_tasks,
    run_meta_qa_answer_synthesis,
    run_stock_answer_synthesis,
)
from value_invest_research.information_collection import (
    apply_meta_qa_source_candidates,
    apply_research_source_candidates,
    build_meta_qa_collection_tasks,
    build_research_collection_tasks,
    discover_meta_qa_source_candidates,
    discover_research_source_candidates,
    run_meta_qa_collection_tasks,
    run_research_collection_tasks,
)
from value_invest_research.adapters.outbound.leaf_research_workflow import LeafResearchWorkflowAdapter
from value_invest_research.application.use_cases.leaf_research_workflow import (
    RollupResearchAnswers,
    RunLeafResearch,
    SynthesizeLeafAnswers,
)
from value_invest_research.meta_qa_research import build_meta_qa_research
from value_invest_research.report_synthesis import write_meta_qa_professional_report, write_stock_professional_report
from value_invest_research.research_system import build_research_system, normalize_ticker
from value_invest_research.runlog import RunLog, RunStatus


def run_stock_qa_pipeline(
    root: Path,
    ticker: str,
    task_limit: int | None = None,
    run_local_collection: bool = False,
    discover_candidates: bool = False,
    apply_candidates: bool = False,
    candidate_path: Path | None = None,
    search_results_path: Path | None = None,
    results_per_task: int = 3,
    candidate_min_score: int = 4,
    dry_run_candidates: bool = False,
    synthesize_answers: bool = False,
    synthesis_client: Any | None = None,
    write_professional_report: bool = False,
    professional_report_client: Any | None = None,
    leaf_research_provider: str | None = None,
    leaf_research_input: Path | None = None,
    leaf_research_limit: int | None = None,
    timeout: int = 10,
) -> dict[str, Any]:
    """Run the stock foundation QA workflow from object to report artifacts."""
    normalized = normalize_ticker(ticker)
    started_at = _now()
    stages: list[dict[str, Any]] = []

    build_result = build_research_system(root, normalized)
    research_dir = Path(build_result["dashboard_path"]).parent
    stages.append(_stage("build_research_system", build_result))

    if run_local_collection:
        local_result = run_research_collection_tasks(root, normalized, limit=task_limit, min_score=candidate_min_score)
        stages.append(_stage("run_local_collection", local_result))
        build_result = {**build_result, **_report_paths(local_result)}

    tasks_result = build_research_collection_tasks(root, normalized, limit=task_limit)
    stages.append(_stage("build_collection_tasks", tasks_result))
    active_candidate_path = candidate_path

    if discover_candidates:
        candidate_result = discover_research_source_candidates(
            root,
            normalized,
            limit=task_limit,
            results_per_task=results_per_task,
            min_score=candidate_min_score,
            timeout=timeout,
            search_results_path=search_results_path,
        )
        stages.append(_stage("discover_source_candidates", candidate_result))
        active_candidate_path = Path(candidate_result["candidate_path"])

    if apply_candidates:
        active_candidate_path = active_candidate_path or research_dir / "source_candidates.jsonl"
        apply_result = apply_research_source_candidates(
            root,
            normalized,
            active_candidate_path,
            min_score=candidate_min_score,
            dry_run=dry_run_candidates,
            timeout=timeout,
        )
        stages.append(_stage("apply_source_candidates", apply_result))
        build_result = build_research_system(root, normalized)
        stages.append(_stage("refresh_report_after_candidates", build_result))

    leaf_research_result: dict[str, Any] = {}
    leaf_answer_result: dict[str, Any] = {}
    rollup_result: dict[str, Any] = {}
    if leaf_research_provider:
        leaf_limit = leaf_research_limit if leaf_research_limit is not None else task_limit
        leaf_workflow = LeafResearchWorkflowAdapter()
        leaf_research_result = RunLeafResearch(leaf_workflow).execute(
            root,
            normalized,
            provider=leaf_research_provider,
            input_path=leaf_research_input,
            limit=leaf_limit,
        )
        stages.append(_stage("run_leaf_research", leaf_research_result))
        leaf_answer_result = SynthesizeLeafAnswers(leaf_workflow).execute(root, normalized)
        stages.append(_stage("synthesize_leaf_answers", leaf_answer_result))
        rollup_result = RollupResearchAnswers(leaf_workflow).execute(root, normalized)
        stages.append(_stage("rollup_research_answers", rollup_result))
        build_result = {**build_result, **_report_paths(rollup_result)}

    synthesis_result: dict[str, Any] = {}
    if synthesize_answers:
        synthesis_result = run_stock_answer_synthesis(root, normalized, limit=task_limit, apply=True, client=synthesis_client)
        stages.append(_stage("run_answer_synthesis", synthesis_result))
        build_result = build_research_system(root, normalized)
        stages.append(_stage("refresh_report_after_synthesis", build_result))
        synthesis_tasks_result = {
            "synthesis_task_path": synthesis_result.get("synthesis_task_path", ""),
        }
    else:
        synthesis_tasks_result = build_stock_synthesis_tasks(root, normalized, limit=task_limit)
        stages.append(_stage("build_synthesis_tasks", synthesis_tasks_result))

    professional_report_result: dict[str, Any] = {}
    if write_professional_report:
        professional_report_result = write_stock_professional_report(root, normalized, client=professional_report_client)
        stages.append(_stage("write_professional_report", professional_report_result))

    manifest = _pipeline_manifest(
        pipeline="stock_qa_pipeline",
        object_type="stock",
        object_id=normalized,
        started_at=started_at,
        stages=stages,
        final={
            "dashboard_path": build_result.get("dashboard_path", ""),
            "report_path": build_result.get("report_path", ""),
            "information_collection_path": build_result.get("information_collection_path", ""),
            "task_path": tasks_result.get("task_path", ""),
            "synthesis_task_path": synthesis_tasks_result.get("synthesis_task_path", ""),
            "synthesized_answer_path": synthesis_result.get("synthesized_answer_path", ""),
            "synthesis_mode": synthesis_result.get("synthesis_mode", ""),
            "professional_report_path": professional_report_result.get("professional_report_path", ""),
            "professional_report_md_path": professional_report_result.get("professional_report_md_path", ""),
            "professional_report_mode": professional_report_result.get("report_mode", ""),
            "candidate_path": str(active_candidate_path or ""),
            "leaf_research_provider": leaf_research_result.get("provider", ""),
            "leaf_research_task_path": leaf_research_result.get("task_path", ""),
            "leaf_research_result_path": leaf_research_result.get("result_path", ""),
            "leaf_research_source_path": leaf_research_result.get("source_path", ""),
            "leaf_answer_path": leaf_answer_result.get("answer_path", ""),
            "rollup_answer_path": rollup_result.get("rollup_path", ""),
        },
    )
    _write_pipeline_manifest(research_dir, manifest)
    RunLog(root / "stocks" / normalized / "logs").append(
        "stock_qa_pipeline",
        RunStatus.SUCCESS,
        tickers=[normalized],
        records_fetched=_sum_stage_int(stages, "matches") + _sum_stage_int(stages, "candidates"),
        records_new=_sum_stage_int(stages, "created") + _sum_stage_int(stages, "applied"),
    )
    return manifest


def run_meta_qa_pipeline(
    root: Path,
    object_type: str,
    object_id: str,
    meta_question: str,
    project_id: str | None = None,
    max_depth: int = 3,
    task_limit: int | None = None,
    run_local_collection: bool = False,
    discover_candidates: bool = False,
    apply_candidates: bool = False,
    candidate_path: Path | None = None,
    search_results_path: Path | None = None,
    results_per_task: int = 3,
    candidate_min_score: int = 4,
    dry_run_candidates: bool = False,
    planner_client: Any | None = None,
    force_plan: bool = False,
    synthesize_answers: bool = False,
    synthesis_client: Any | None = None,
    write_professional_report: bool = False,
    professional_report_client: Any | None = None,
    timeout: int = 10,
) -> dict[str, Any]:
    """Run a generic layered QA workflow from a meta-question to report artifacts."""
    started_at = _now()
    stages: list[dict[str, Any]] = []

    build_result = build_meta_qa_research(
        root,
        object_type,
        object_id,
        meta_question,
        project_id=project_id,
        max_depth=max_depth,
        planner_client=planner_client,
        force_plan=force_plan,
    )
    project_dir = Path(build_result["project_dir"])
    resolved_project_id = build_result["project_id"]
    stages.append(_stage("build_meta_qa", build_result))

    if run_local_collection:
        local_result = run_meta_qa_collection_tasks(root, resolved_project_id, limit=task_limit, min_score=candidate_min_score)
        stages.append(_stage("run_local_collection", local_result))
        build_result = {**build_result, **_report_paths(local_result)}

    tasks_result = build_meta_qa_collection_tasks(root, resolved_project_id, limit=task_limit)
    stages.append(_stage("build_collection_tasks", tasks_result))
    active_candidate_path = candidate_path

    if discover_candidates:
        candidate_result = discover_meta_qa_source_candidates(
            root,
            resolved_project_id,
            limit=task_limit,
            results_per_task=results_per_task,
            min_score=candidate_min_score,
            timeout=timeout,
            search_results_path=search_results_path,
        )
        stages.append(_stage("discover_source_candidates", candidate_result))
        active_candidate_path = Path(candidate_result["candidate_path"])

    if apply_candidates:
        active_candidate_path = active_candidate_path or project_dir / "source_candidates.jsonl"
        apply_result = apply_meta_qa_source_candidates(
            root,
            resolved_project_id,
            active_candidate_path,
            min_score=candidate_min_score,
            dry_run=dry_run_candidates,
            timeout=timeout,
        )
        stages.append(_stage("apply_source_candidates", apply_result))
        build_result = build_meta_qa_research(
            root,
            object_type,
            object_id,
            meta_question,
            project_id=resolved_project_id,
            max_depth=max_depth,
        )
        stages.append(_stage("refresh_report_after_candidates", build_result))

    synthesis_result: dict[str, Any] = {}
    if synthesize_answers:
        synthesis_result = run_meta_qa_answer_synthesis(root, resolved_project_id, limit=task_limit, apply=True, client=synthesis_client)
        stages.append(_stage("run_answer_synthesis", synthesis_result))
        build_result = build_meta_qa_research(
            root,
            object_type,
            object_id,
            meta_question,
            project_id=resolved_project_id,
            max_depth=max_depth,
        )
        stages.append(_stage("refresh_report_after_synthesis", build_result))
        synthesis_tasks_result = {
            "synthesis_task_path": synthesis_result.get("synthesis_task_path", ""),
        }
    else:
        synthesis_tasks_result = build_meta_qa_synthesis_tasks(root, resolved_project_id, limit=task_limit)
        stages.append(_stage("build_synthesis_tasks", synthesis_tasks_result))

    professional_report_result: dict[str, Any] = {}
    if write_professional_report:
        professional_report_result = write_meta_qa_professional_report(root, resolved_project_id, client=professional_report_client)
        stages.append(_stage("write_professional_report", professional_report_result))

    manifest = _pipeline_manifest(
        pipeline="meta_qa_pipeline",
        object_type=object_type,
        object_id=object_id,
        started_at=started_at,
        stages=stages,
        final={
            "project_id": resolved_project_id,
            "project_dir": str(project_dir),
            "planning_mode": build_result.get("planning_mode", ""),
            "dashboard_path": build_result.get("dashboard_path", ""),
            "report_path": build_result.get("report_path", ""),
            "information_collection_path": build_result.get("information_collection_path", ""),
            "task_path": tasks_result.get("task_path", ""),
            "synthesis_task_path": synthesis_tasks_result.get("synthesis_task_path", ""),
            "synthesized_answer_path": synthesis_result.get("synthesized_answer_path", ""),
            "synthesis_mode": synthesis_result.get("synthesis_mode", ""),
            "professional_report_path": professional_report_result.get("professional_report_path", ""),
            "professional_report_md_path": professional_report_result.get("professional_report_md_path", ""),
            "professional_report_mode": professional_report_result.get("report_mode", ""),
            "candidate_path": str(active_candidate_path or ""),
        },
    )
    _write_pipeline_manifest(project_dir, manifest)
    return manifest


def _pipeline_manifest(
    pipeline: str,
    object_type: str,
    object_id: str,
    started_at: str,
    stages: list[dict[str, Any]],
    final: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "pipeline": pipeline,
        "object_type": object_type,
        "object_id": object_id,
        "started_at": started_at,
        "finished_at": _now(),
        "status": "success",
        "stages": stages,
        "final": final,
    }


def _stage(name: str, result: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": name,
        "status": "success",
        "finished_at": _now(),
        "result": result,
    }


def _report_paths(result: dict[str, Any]) -> dict[str, str]:
    return {
        "dashboard_path": result.get("dashboard_path", ""),
        "report_path": result.get("report_path", ""),
        "information_collection_path": result.get("information_collection_path", ""),
    }


def _write_pipeline_manifest(base_dir: Path, manifest: dict[str, Any]) -> None:
    base_dir.mkdir(parents=True, exist_ok=True)
    current_path = base_dir / "pipeline_run.json"
    history_path = base_dir / "pipeline_runs.jsonl"
    current_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with history_path.open("a", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps(manifest, ensure_ascii=False, sort_keys=True) + "\n")


def _sum_stage_int(stages: list[dict[str, Any]], key: str) -> int:
    return sum(int(stage.get("result", {}).get(key, 0) or 0) for stage in stages)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
