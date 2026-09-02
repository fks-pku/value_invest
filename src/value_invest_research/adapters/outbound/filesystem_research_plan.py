from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FileSystemResearchPlanRepository:
    """Filesystem adapter for plan versions and append-only execution events."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.plan_path = project_dir / "research_plan.json"
        self.event_path = project_dir / "research_step_events.jsonl"
        self.plan_history_dir = project_dir / "research_plan_history"

    @property
    def project_dir_label(self) -> str:
        return str(self.project_dir)

    @property
    def plan_path_label(self) -> str:
        return str(self.plan_path)

    @property
    def event_path_label(self) -> str:
        return str(self.event_path)

    def save_question_architecture(self, qa_tree: dict) -> None:
        self._write_json(self.project_dir / "qa_tree.json", qa_tree)

    def save_plan(self, plan: dict) -> None:
        plan_id = str(plan.get("plan_id") or "").strip()
        if not plan_id:
            raise ValueError("research plan missing plan_id")
        self.plan_history_dir.mkdir(parents=True, exist_ok=True)
        history_path = self.plan_history_dir / f"{plan_id}.json"
        if history_path.exists():
            existing = json.loads(history_path.read_text(encoding="utf-8"))
            if existing != plan:
                raise ValueError(f"research plan history collision for {plan_id}")
        else:
            self._write_json(history_path, plan)
        self._write_json(self.plan_path, plan)

    def load_plan(self) -> dict[str, Any]:
        if not self.plan_path.exists():
            return {}
        payload = json.loads(self.plan_path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}

    def append_step_event(self, event: dict) -> bool:
        event_id = str(event.get("event_id") or "").strip()
        if not event_id:
            raise ValueError("research step event missing event_id")
        if event_id in {
            str(row.get("event_id") or "")
            for row in self.load_step_events()
        }:
            return False
        self.event_path.parent.mkdir(parents=True, exist_ok=True)
        with self.event_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        return True

    def load_step_events(self) -> list[dict[str, Any]]:
        if not self.event_path.exists():
            return []
        return [
            json.loads(line)
            for line in self.event_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def save_l3_research_plans(
        self,
        index: dict[str, Any],
        plans: list[dict[str, Any]],
    ) -> None:
        """Persist every L3 plan independently with immutable history."""

        base = self.project_dir / "l3_research_plans"
        base.mkdir(parents=True, exist_ok=True)
        for plan in plans:
            node_id = str(plan.get("l3_node_id") or "").strip()
            plan_id = str(plan.get("plan_id") or "").strip()
            if not node_id or not plan_id:
                raise ValueError("L3 research plan requires l3_node_id and plan_id")
            plan_dir = base / node_id
            history_dir = plan_dir / "research_plan_history"
            history_dir.mkdir(parents=True, exist_ok=True)
            history_path = history_dir / f"{plan_id}.json"
            if history_path.exists():
                existing = json.loads(history_path.read_text(encoding="utf-8"))
                if existing != plan:
                    raise ValueError(f"L3 research plan history collision for {plan_id}")
            else:
                self._write_json(history_path, plan)
            self._write_json(plan_dir / "research_plan.json", plan)
        self._write_json(base / "index.json", index)

    def load_l3_research_plan_bundle(self) -> dict[str, Any]:
        base = self.project_dir / "l3_research_plans"
        index = _read_json(base / "index.json")
        plans: list[dict[str, Any]] = []
        events_by_node: dict[str, list[dict[str, Any]]] = {}
        for row in index.get("plans") or []:
            if not isinstance(row, dict):
                continue
            node_id = str(row.get("l3_node_id") or "")
            plan_path = self.project_dir / str(row.get("path") or "")
            plan = _read_json(plan_path)
            if plan:
                plans.append(plan)
            event_path = self.project_dir / str(row.get("event_path") or "")
            events_by_node[node_id] = _read_jsonl(event_path)
        return {
            "index": index,
            "plans": plans,
            "events_by_node": events_by_node,
        }

    def write_research_plan_html(self, html: str) -> str:
        path = self.project_dir / "research_plan.html"
        path.write_text(html, encoding="utf-8")
        return str(path)

    def bind_l3_plans_to_question_architecture(
        self,
        *,
        parent_plan: dict[str, Any],
        index: dict[str, Any],
    ) -> None:
        qa_path = self.project_dir / "qa_tree.json"
        qa_tree = _read_json(qa_path)
        if not qa_tree:
            return
        indexed = {
            str(row.get("l3_node_id") or ""): row
            for row in index.get("plans") or []
            if isinstance(row, dict)
        }
        parent_steps = {
            str(row.get("question_node_id") or ""): row
            for row in parent_plan.get("steps") or []
            if isinstance(row, dict)
        }
        for node in qa_tree.get("nodes") or []:
            if not isinstance(node, dict):
                continue
            node_id = str(node.get("id") or "")
            plan_row = indexed.get(node_id)
            parent_step = parent_steps.get(node_id)
            if not plan_row or not parent_step:
                continue
            node.update(
                {
                    "execution_mode": "child_plan_rollup",
                    "child_plan_path": str(plan_row.get("path") or ""),
                    "source_universe_plan": {},
                    "source_plan": [],
                    "minimum_evidence_gate": dict(
                        parent_step.get("minimum_evidence_gate") or {}
                    ),
                }
            )
        qa_tree["research_plan_id"] = str(parent_plan.get("plan_id") or "")
        qa_tree["research_plan_path"] = "research_plan.json"
        qa_tree["l3_plan_index_path"] = "l3_research_plans/index.json"
        self._write_json(qa_path, qa_tree)

    @staticmethod
    def _write_json(path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
