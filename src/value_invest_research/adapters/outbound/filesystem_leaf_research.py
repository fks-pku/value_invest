from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from value_invest_research.domain.leaf_research_results import deduplicate_leaf_sources, merge_leaf_result_rows


class FileSystemRawProviderResponseStore:
    """File-system raw response store for leaf research providers."""

    def __init__(self, raw_dir: Path):
        self.raw_dir = raw_dir
        self.raw_dir.mkdir(parents=True, exist_ok=True)

    @property
    def raw_dir_label(self) -> str:
        return str(self.raw_dir)

    def save_raw_response(self, task_id: str, payload: dict[str, Any]) -> str:
        raw_path = self.raw_dir / f"{task_id}.json"
        raw_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        return str(raw_path)


class FileSystemLeafResearchResultRepository:
    """File-system repository for merged leaf research results and source index."""

    def __init__(
        self,
        research_dir: Path,
        *,
        result_file: str = "leaf_research_results.jsonl",
        source_file: str = "leaf_research_sources.jsonl",
    ):
        self.research_dir = research_dir
        self.result_path = research_dir / result_file
        self.source_path = research_dir / source_file

    @property
    def result_path_label(self) -> str:
        return str(self.result_path)

    @property
    def source_path_label(self) -> str:
        return str(self.source_path)

    def save_results(self, rows: list[dict]) -> dict[str, int]:
        existing_rows = _read_jsonl(self.result_path)
        merged_rows = merge_leaf_result_rows(existing_rows, rows)
        _write_jsonl(self.result_path, merged_rows)
        sources = deduplicate_leaf_sources(merged_rows)
        _write_jsonl(self.source_path, sources)
        return {"results": len(rows), "sources": len(sources)}


class FileSystemLeafResearchArtifactRepository:
    """File-system repository for leaf research tasks, results, and answers."""

    def __init__(
        self,
        research_dir: Path,
        *,
        task_file: str = "leaf_research_tasks.jsonl",
        result_file: str = "leaf_research_results.jsonl",
        answer_file: str = "leaf_answers.jsonl",
        rollup_file: str = "rollup_answers.jsonl",
    ):
        self.research_dir = research_dir
        self.task_path = research_dir / task_file
        self.result_path = research_dir / result_file
        self.answer_path = research_dir / answer_file
        self.rollup_path = research_dir / rollup_file

    @property
    def task_path_label(self) -> str:
        return str(self.task_path)

    @property
    def result_path_label(self) -> str:
        return str(self.result_path)

    @property
    def answer_path_label(self) -> str:
        return str(self.answer_path)

    @property
    def rollup_path_label(self) -> str:
        return str(self.rollup_path)

    def load_completed_leaf_node_ids(self) -> set[str]:
        return {str(row.get("node_id", "")) for row in _read_jsonl(self.answer_path) if row.get("node_id")}

    def save_tasks(self, rows: list[dict]) -> int:
        _write_jsonl(self.task_path, rows)
        return len(rows)

    def load_tasks(self) -> list[dict]:
        return _read_jsonl(self.task_path)

    def load_results(self) -> list[dict]:
        return _read_jsonl(self.result_path)

    def save_leaf_answers(self, rows: list[dict]) -> int:
        _write_jsonl(self.answer_path, rows)
        return len(rows)

    def save_rollup_answers(self, rows: list[dict]) -> int:
        _write_jsonl(self.rollup_path, rows)
        return len(rows)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows)
    path.write_text((text + "\n") if text else "", encoding="utf-8")
