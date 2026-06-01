from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from value_invest_research.domain.domain_playbooks import DomainPlaybook, resolve_domain_playbook
from value_invest_research.domain.research_goal import DEFAULT_RESEARCH_RUN_MODE, ResearchGoal


@dataclass(frozen=True)
class ReportViewModel:
    """Renderer-facing model for the locked professional report contract."""

    project: dict[str, Any]
    goal: dict[str, Any]
    supply_chain: dict[str, Any]
    qa_roots: list[dict[str, Any]]
    targets: list[dict[str, Any]]
    sources: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "project": self.project,
            "goal": self.goal,
            "supply_chain": self.supply_chain,
            "qa_roots": self.qa_roots,
            "targets": self.targets,
            "sources": self.sources,
        }


def build_report_view_model(
    *,
    project: dict[str, Any],
    qa_tree: dict[str, Any],
    sources: list[dict[str, Any]],
    targets: list[dict[str, Any]],
    playbook: DomainPlaybook | None = None,
) -> ReportViewModel:
    """Convert research artifacts into a presentation-neutral report model."""
    goal = _goal_from_project(project, qa_tree)
    resolved_playbook = playbook or resolve_domain_playbook(goal)
    nodes = [node for node in qa_tree.get("nodes", []) if isinstance(node, dict)]
    nodes_by_parent: dict[str, list[dict[str, Any]]] = {}
    for node in nodes:
        nodes_by_parent.setdefault(str(node.get("parent_id", "")), []).append(node)
    qa_roots = [_view_node(node, nodes_by_parent, sources) for node in nodes_by_parent.get("", [])]
    return ReportViewModel(
        project={
            "project_id": project.get("project_id") or qa_tree.get("project_id", ""),
            "title": project.get("title") or qa_tree.get("title") or goal.topic,
            "run_mode": project.get("run_mode") or qa_tree.get("run_mode") or goal.run_mode,
            "report_date": project.get("report_date") or qa_tree.get("report_date") or goal.report_date,
            "as_of_date": project.get("as_of_date") or qa_tree.get("as_of_date") or goal.as_of_date,
        },
        goal={
            "topic": goal.topic,
            "research_type": goal.normalized_type(),
            "decision_boundary": goal.decision_boundary,
            "current_judgment": project.get("current_judgment") or _rollup_text(qa_roots),
            "biggest_uncertainty": project.get("biggest_uncertainty") or _default_uncertainty(goal),
        },
        supply_chain=_supply_chain_model(resolved_playbook),
        qa_roots=qa_roots,
        targets=targets,
        sources=sources,
    )


def _goal_from_project(project: dict[str, Any], qa_tree: dict[str, Any]) -> ResearchGoal:
    topic = project.get("title") or project.get("meta_question") or qa_tree.get("title") or qa_tree.get("project_id", "Research project")
    return ResearchGoal(
        topic=str(topic),
        research_type=str(project.get("object_type") or project.get("research_type") or "industry_theme"),
        object_id=str(project.get("object_id") or project.get("project_id") or qa_tree.get("project_id", "")),
        run_mode=str(project.get("run_mode") or qa_tree.get("run_mode") or DEFAULT_RESEARCH_RUN_MODE),
        report_date=str(project.get("report_date") or qa_tree.get("report_date") or ""),
        as_of_date=str(project.get("as_of_date") or qa_tree.get("as_of_date") or ""),
        decision_boundary=str(project.get("decision_boundary") or "research observation, not trading instruction"),
        domain_hint=str(project.get("domain_playbook") or qa_tree.get("domain_playbook") or project.get("project_id", "")),
    )


def _view_node(
    node: dict[str, Any],
    nodes_by_parent: dict[str, list[dict[str, Any]]],
    sources: list[dict[str, Any]],
) -> dict[str, Any]:
    children = [_view_node(child, nodes_by_parent, sources) for child in nodes_by_parent.get(str(node.get("id", "")), [])]
    source_ids = [str(item) for item in node.get("source_links", []) or []]
    source_index = [source for source in sources if source.get("source_id") in set(source_ids)]
    return {
        "id": str(node.get("id", "")),
        "level": int(node.get("level", 0) or 0),
        "question": str(node.get("question", "")),
        "conclusion": str(node.get("conclusion") or node.get("judgment") or node.get("answer") or ""),
        "decision_use": str(node.get("decision_use", "")),
        "skill": str((node.get("skill_dispatch") or {}).get("selected_skill") or node.get("preferred_specialty_skill", "")),
        "execution_status": str((node.get("skill_dispatch") or {}).get("gpt_verification_status") or "not_applicable"),
        "score_component": str(node.get("score_component", "")),
        "fact": str(node.get("fact", "")),
        "inference": str(node.get("inference", "")),
        "judgment": str(node.get("judgment", "")),
        "gap": str(node.get("gap", "")),
        "trigger": str(node.get("trigger", "")),
        "source_ids": source_ids,
        "source_index": source_index,
        "children": children,
    }


def _supply_chain_model(playbook: DomainPlaybook) -> dict[str, Any]:
    layers = playbook.supply_chain_layers or [
        {"layer": "上游", "products": "待定义", "players": "待定义", "value_flow": "需要领域 playbook 补充。"},
        {"layer": "中游", "products": "待定义", "players": "待定义", "value_flow": "需要领域 playbook 补充。"},
        {"layer": "下游", "products": "待定义", "players": "待定义", "value_flow": "需要领域 playbook 补充。"},
    ]
    return {
        "plain_summary": "产业链全景用于先回答谁提供什么、谁依赖谁、谁付款、利润和瓶颈在哪里，再进入 QA。",
        "flow_steps": [
            "确认终端需求和付费方。",
            "映射上游、中游、下游的产品和依赖。",
            "定位供给、认证、渠道、数据或监管瓶颈。",
            "把瓶颈映射到具体标的和财务敞口。",
            "用反证和估值检查赔率。",
        ],
        "layers": layers,
        "chokepoints": ", ".join(playbook.mechanism_buckets),
        "target_links": "Q2 负责瓶颈评分，Q4 负责把瓶颈、赔率和风险合成具体标的排序。",
    }


def _rollup_text(qa_roots: list[dict[str, Any]]) -> str:
    conclusions = [root.get("conclusion", "") for root in qa_roots if root.get("conclusion")]
    return "；".join(conclusions[:4]) or "当前结论来自 Q1-Q4 子问题上抛。"


def _default_uncertainty(goal: ResearchGoal) -> str:
    if "memory" in goal.domain_hint.lower() or "存储" in goal.topic:
        return "需求增长能否持续转化为价格、毛利率和自由现金流，而不是短期供给周期。"
    return "最关键不确定性取决于证据是否能同时支持增长空间、价值捕获、估值赔率和风险控制。"
