from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from value_invest_research.adapters.outbound.filesystem_leaf_research import (
    FileSystemLeafResearchArtifactRepository,
    FileSystemLeafResearchResultRepository,
    FileSystemRawProviderResponseStore,
)
from value_invest_research.adapters.outbound.research_search_providers import provider_for_name
from value_invest_research.application.use_cases.build_leaf_research_tasks_from_tree import (
    BuildLeafResearchTasksFromTree,
)
from value_invest_research.application.use_cases.execute_leaf_research_tasks import ExecuteLeafResearchTasks
from value_invest_research.application.use_cases.leaf_research_artifacts import LoadLeafResearchTasks
from value_invest_research.application.use_cases.persist_leaf_research_results import PersistLeafResearchResults
from value_invest_research.application.use_cases.synthesize_leaf_research_answers import (
    BuildRollupResearchAnswers,
    SynthesizeLeafResearchAnswers,
)
from value_invest_research.domain.leaf_research_results import normalize_provider_result


LEAF_TASK_FILE = "leaf_research_tasks.jsonl"
LEAF_RESULT_FILE = "leaf_research_results.jsonl"
LEAF_SOURCE_FILE = "leaf_research_sources.jsonl"
LEAF_ANSWER_FILE = "leaf_answers.jsonl"
ROLLUP_ANSWER_FILE = "rollup_answers.jsonl"
LEAF_RAW_DIR = "leaf_research_raw"


class StockLeafResearchService:
    """Outbound adapter that wires stock QA files to leaf research use cases."""

    def build_tasks(
        self,
        root: Path,
        ticker: str,
        *,
        limit: int | None = None,
        include_completed: bool = False,
    ) -> dict[str, Any]:
        from value_invest_research.research_system import build_research_system, normalize_ticker

        if limit is not None and limit < 0:
            raise ValueError("limit must be non-negative")
        normalized = normalize_ticker(ticker)
        build_result = build_research_system(root, normalized)
        research_dir = Path(build_result["qa_tree_path"]).parent
        qa_tree = _read_json(research_dir / "qa_tree.json")
        task_result = BuildLeafResearchTasksFromTree(_artifact_repository(research_dir)).execute(
            qa_tree,
            ticker=normalized,
            company_name=_company_name(root, normalized),
            limit=limit,
            include_completed=include_completed,
        )
        return {
            **build_result,
            "ticker": normalized,
            "task_path": str(task_result["task_path"]),
            "tasks": int(task_result["tasks"]),
            "leaf_questions": int(task_result["leaf_questions"]),
            "include_completed": include_completed,
        }

    def run_research(
        self,
        root: Path,
        ticker: str,
        *,
        provider: str,
        input_path: Path | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        if provider == "manual":
            if input_path is None:
                raise ValueError("manual provider requires input_path")
            return self.import_results(root, ticker, input_path)

        task_result = self.build_tasks(root, ticker, limit=limit)
        research_dir = Path(task_result["task_path"]).parent
        artifact_repository = _artifact_repository(research_dir)
        tasks = LoadLeafResearchTasks(artifact_repository).execute()
        raw_dir = research_dir / LEAF_RAW_DIR
        execution_result = ExecuteLeafResearchTasks(
            provider_for_name(provider),
            FileSystemRawProviderResponseStore(raw_dir),
        ).execute(tasks)
        rows = execution_result["rows"]
        source_path, source_count = _save_leaf_results(research_dir, rows)
        return {
            **task_result,
            "provider": provider,
            "result_path": artifact_repository.result_path_label,
            "source_path": str(source_path),
            "raw_dir": execution_result["raw_dir"],
            "results": len(rows),
            "sources": source_count,
        }

    def import_results(self, root: Path, ticker: str, path: Path) -> dict[str, Any]:
        from value_invest_research.research_system import build_research_system, normalize_ticker

        normalized = normalize_ticker(ticker)
        build_result = build_research_system(root, normalized)
        research_dir = Path(build_result["qa_tree_path"]).parent
        rows = [normalize_provider_result(row) for row in _read_jsonl(path)]
        result_path = research_dir / LEAF_RESULT_FILE
        source_path, source_count = _save_leaf_results(research_dir, rows)
        return {
            **build_result,
            "ticker": normalized,
            "input_path": str(path),
            "result_path": str(result_path),
            "source_path": str(source_path),
            "records": len(rows),
            "sources": source_count,
        }

    def synthesize_answers(self, root: Path, ticker: str) -> dict[str, Any]:
        from value_invest_research.research_system import build_research_system, normalize_ticker

        normalized = normalize_ticker(ticker)
        build_result = build_research_system(root, normalized)
        research_dir = Path(build_result["qa_tree_path"]).parent
        result = SynthesizeLeafResearchAnswers(_artifact_repository(research_dir)).execute()
        return {
            **build_result,
            "ticker": normalized,
            "answer_path": str(result["answer_path"]),
            "answers": int(result["answers"]),
            "source_result_path": str(research_dir / LEAF_RESULT_FILE),
        }

    def rollup_answers(self, root: Path, ticker: str) -> dict[str, Any]:
        from value_invest_research.research_system import build_research_system, normalize_ticker

        normalized = normalize_ticker(ticker)
        build_result = build_research_system(root, normalized)
        research_dir = Path(build_result["qa_tree_path"]).parent
        qa_tree = _read_json(research_dir / "qa_tree.json")
        result = BuildRollupResearchAnswers(_artifact_repository(research_dir)).execute(qa_tree)
        return {
            **build_result,
            "ticker": normalized,
            "rollup_path": str(result["rollup_path"]),
            "rollups": int(result["rollups"]),
        }


def _save_leaf_results(research_dir: Path, rows: list[dict[str, Any]]) -> tuple[Path, int]:
    repository = FileSystemLeafResearchResultRepository(
        research_dir,
        result_file=LEAF_RESULT_FILE,
        source_file=LEAF_SOURCE_FILE,
    )
    result = PersistLeafResearchResults(repository).execute(rows)
    return Path(str(result["source_path"])), int(result["sources"])


def _artifact_repository(research_dir: Path) -> FileSystemLeafResearchArtifactRepository:
    return FileSystemLeafResearchArtifactRepository(
        research_dir,
        task_file=LEAF_TASK_FILE,
        result_file=LEAF_RESULT_FILE,
        answer_file=LEAF_ANSWER_FILE,
        rollup_file=ROLLUP_ANSWER_FILE,
    )


def _company_name(root: Path, ticker: str) -> str:
    profile_path = root / "stocks" / ticker / "company_profile.md"
    if not profile_path.exists():
        return ticker
    for line in profile_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"-\s*Company:\s*(.+)", line)
        if match:
            return match.group(1).strip()
    return ticker


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
