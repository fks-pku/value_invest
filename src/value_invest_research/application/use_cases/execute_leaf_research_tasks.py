from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from value_invest_research.domain.leaf_research_results import normalize_provider_result
from value_invest_research.ports.source_parsers import LeafResearchProvider, RawProviderResponseStore


@dataclass(frozen=True)
class ExecuteLeafResearchTasks:
    """Run leaf research tasks through a provider and raw-response store."""

    provider: LeafResearchProvider
    raw_store: RawProviderResponseStore

    def execute(self, tasks: list[dict[str, Any]]) -> dict[str, Any]:
        rows: list[dict[str, Any]] = []
        for task in tasks:
            provider_result = dict(self.provider.search(task))
            provider_result.setdefault("task_id", task.get("task_id", ""))
            provider_result.setdefault("node_id", task.get("node_id", ""))
            provider_result.setdefault("research_step_id", task.get("research_step_id", ""))
            raw_payload = provider_result.pop("_raw_provider_response", provider_result)
            raw_path = self.raw_store.save_raw_response(str(task.get("task_id", "")), raw_payload)
            provider_result["raw_response_path"] = raw_path
            rows.append(normalize_provider_result(provider_result))
        return {
            "rows": rows,
            "raw_dir": self.raw_store.raw_dir_label,
            "results": len(rows),
        }
