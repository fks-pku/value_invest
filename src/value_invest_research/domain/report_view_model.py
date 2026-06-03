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
        supply_chain=_artifact_supply_chain(project, qa_tree) or _supply_chain_model(resolved_playbook),
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
        "artifact": node.get("artifact") if isinstance(node.get("artifact"), dict) else {},
        "source_ids": source_ids,
        "source_index": source_index,
        "children": children,
    }


def _supply_chain_model(playbook: DomainPlaybook) -> dict[str, Any]:
    layers = playbook.supply_chain_layers or [
        {
            "stage": "上游",
            "node": "待定义",
            "demand_input": "需要领域 playbook 补充下游需求、订单或预算来源。",
            "supply_input": "需要领域 playbook 补充产能、技术、材料或生态输入。",
            "produces": "需要领域 playbook 补充自身产品/服务。",
            "players": "待定义",
            "financial_metrics": "需要领域 playbook 补充收入、毛利、订单、backlog、capex 或现金流指标。",
            "value_flow": "需要领域 playbook 补充瓶颈和利润捕获逻辑。",
            "qa_link": "Q2 / Q4",
        },
        {
            "stage": "中游",
            "node": "待定义",
            "demand_input": "需要领域 playbook 补充客户规格、交付需求或项目订单。",
            "supply_input": "需要领域 playbook 补充上游关键部件、产能、认证或工程资源。",
            "produces": "需要领域 playbook 补充集成、制造、交付或平台能力。",
            "players": "待定义",
            "financial_metrics": "需要领域 playbook 补充收入、毛利、订单、backlog、库存或现金转化。",
            "value_flow": "需要领域 playbook 补充瓶颈和价值捕获逻辑。",
            "qa_link": "Q2 / Q4",
        },
        {
            "stage": "下游",
            "node": "待定义",
            "demand_input": "需要领域 playbook 补充终端需求、使用场景、预算或 ROI 约束。",
            "supply_input": "需要领域 playbook 补充上中游产品、解决方案、渠道或交付能力。",
            "produces": "需要领域 playbook 补充订单、使用率、收入转化、续费或 ROI 信号。",
            "players": "待定义",
            "financial_metrics": "需要领域 playbook 补充 capex、收入、RPO/backlog、使用率、FCF 或 ROI 指标。",
            "value_flow": "需要领域 playbook 补充需求验证和反证逻辑。",
            "qa_link": "Q1 / Q3",
        },
    ]
    stage_groups = [
        {
            "stage": str(layer.get("stage") or layer.get("layer") or "待定义"),
            "summary": str(layer.get("value_flow") or "等待领域 playbook 补充。"),
            "companies": [
                {
                    "name": str(layer.get("players") or "待定义玩家"),
                    "ticker": "",
                    "node_type": str(layer.get("node_type") or layer.get("node") or layer.get("products") or "需要领域 playbook 补充。"),
                    "demand_input": str(layer.get("demand_input") or layer.get("demand") or layer.get("accepts_from") or layer.get("inputs") or "需要领域 playbook 补充。"),
                    "supply_input": str(layer.get("supply_input") or layer.get("supply") or "需要领域 playbook 补充。"),
                    "produces": str(layer.get("produces") or layer.get("products") or "需要领域 playbook 补充。"),
                    "provides_to": str(layer.get("provides_to") or layer.get("outputs") or "需要领域 playbook 补充。"),
                    "financial_metrics": str(layer.get("financial_metrics") or layer.get("metrics") or "需要领域 playbook 补充。"),
                    "bottleneck_strength": str(layer.get("bottleneck_strength") or layer.get("value_flow") or "需要领域 playbook 补充。"),
                    "qa_link": str(layer.get("qa_link") or layer.get("qa") or "需要领域 playbook 补充。"),
                    "evidence": str(layer.get("evidence") or "待验证"),
                }
            ],
        }
        for layer in layers
    ]
    return {
        "plain_summary": "行业概况用于先回答谁提供什么、谁依赖谁、谁付款、利润和瓶颈在哪里，再进入 QA。",
        "flow_steps": [
            "确认终端需求和付费方。",
            "映射上游、中游、下游的产品和依赖。",
            "定位供给、认证、渠道、数据或监管瓶颈。",
            "把瓶颈映射到具体标的和财务敞口。",
            "用反证和估值检查赔率。",
        ],
        "layers": layers,
        "stage_groups": stage_groups,
        "relationships": [
            {
                "from": "上游关键输入",
                "to": "中游价值捕获节点",
                "relationship": "供应、认证、产能或技术依赖",
                "demand_input": "承接下游订单、规格、部署或预算需求。",
                "supply_input": "接受上游产品、产能、认证或技术输入。",
                "produces": "提供可被下游采购或部署的产品/服务。",
                "provides_to": "提供给下游客户、系统商、渠道或生态节点。",
                "financial_metrics": "收入、毛利率、订单、backlog、产能利用率和现金转化。",
                "bottleneck_strength": "等待领域 playbook 明确稀缺资源和替代路径。",
                "qa_link": "Q2 定位瓶颈，Q4 映射具体标的。",
                "evidence": "需要一手来源、公司披露或行业数据验证。",
            },
            {
                "from": "中游价值捕获节点",
                "to": "下游付费客户",
                "relationship": "产品交付、解决方案、渠道或生态绑定",
                "demand_input": "承接终端需求、使用场景、预算和 ROI 约束。",
                "supply_input": "接受中游产品、交付、渠道或生态能力。",
                "produces": "提供预算、订单、使用率、续费和 ROI 反馈。",
                "provides_to": "反馈给中游系统商、上游关键供应商和应用生态。",
                "financial_metrics": "客户 capex、收入、RPO/backlog、续费、使用率和 FCF。",
                "bottleneck_strength": "等待补充分产品收入、毛利率、订单/backlog 和客户验证。",
                "qa_link": "Q4 只允许把可财务化关系转成目标评分。",
                "evidence": "需要客户、财报、订单或价格数据。",
            },
        ],
        "chokepoints": ", ".join(playbook.mechanism_buckets),
        "target_links": "Q2 负责瓶颈评分，Q4 负责把瓶颈、赔率和风险合成具体标的排序。",
    }


def _artifact_supply_chain(project: dict[str, Any], qa_tree: dict[str, Any]) -> dict[str, Any]:
    for candidate in (project.get("supply_chain"), qa_tree.get("supply_chain")):
        if isinstance(candidate, dict) and candidate.get("layers"):
            return candidate
    return {}


def _rollup_text(qa_roots: list[dict[str, Any]]) -> str:
    conclusions = [root.get("conclusion", "") for root in qa_roots if root.get("conclusion")]
    return "；".join(conclusions[:4]) or "当前结论来自 Q1-Q4 子问题上抛。"


def _default_uncertainty(goal: ResearchGoal) -> str:
    if "memory" in goal.domain_hint.lower() or "存储" in goal.topic:
        return "需求增长能否持续转化为价格、毛利率和自由现金流，而不是短期供给周期。"
    return "最关键不确定性取决于证据是否能同时支持增长空间、价值捕获、估值赔率和风险控制。"
