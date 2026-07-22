from __future__ import annotations

from typing import Any, Iterable

from value_invest_research.domain.bom_project_layout import build_bom_project_layout


def build_bom_project_manifest(
    parent_project_id: str,
    nodes: Iterable[dict[str, Any]],
    *,
    research_run_node_ids: Iterable[str] = (),
) -> dict[str, Any]:
    return build_bom_project_layout(
        parent_project_id,
        nodes,
        research_run_node_ids=research_run_node_ids,
    )
