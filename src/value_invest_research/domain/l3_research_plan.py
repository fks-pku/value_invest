from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from typing import Any, Iterable, Iterator

from value_invest_research.domain.research_plan import validate_research_plan_execution


MAX_QUESTION_DEPTH = 5

ACTIVE_QUESTION_TRACE_FIELDS = (
    "l3_plan_id",
    "l3_node_id",
    "question_node_id",
    "question_level",
    "research_step_id",
    "search_run_id",
)

# Compatibility alias for adapters that have not yet renamed their local variable.
LEAF_TRACE_FIELDS = ACTIVE_QUESTION_TRACE_FIELDS


def upgrade_parent_plan_for_l3_plans(
    parent_plan: dict[str, Any],
) -> dict[str, Any]:
    """Create an immutable parent version whose L3 steps are child rollups."""

    upgraded = {
        **parent_plan,
        "schema_version": "4.0",
        "execution_policy": {
            **dict(parent_plan.get("execution_policy") or {}),
            "question_tree": "adaptive_depth_max_5",
            "completion": "all_required_l3_child_plans_complete",
            "material_collection": "current_terminal_question_only",
            "broad_material_pool": "candidate_only_not_completion_evidence",
        },
        "l3_plan_index_path": "l3_research_plans/index.json",
        "steps": [],
    }
    for step in parent_plan.get("steps") or []:
        if not isinstance(step, dict):
            continue
        node_id = str(step.get("question_node_id") or "")
        upgraded["steps"].append(
            {
                **step,
                "execution_mode": "child_plan_rollup",
                "child_plan_path": l3_plan_path(node_id),
                "source_universe_plan": {},
                "source_plan": [],
                "minimum_evidence_gate": {
                    "rule": (
                        "The L3 rollup completes when its current terminal question "
                        "passes, or after every required child created by a failed "
                        "answerability gate passes."
                    ),
                    "all_mandatory_leaf_steps_required": True,
                    "direct_parent_evidence_forbidden": True,
                },
            }
        )
    identity = {key: value for key, value in upgraded.items() if key != "plan_id"}
    digest = hashlib.sha256(
        json.dumps(identity, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]
    upgraded["plan_id"] = f"rp_l3_{digest}"
    return upgraded


def build_l3_research_plan_set(
    *,
    l3_nodes: Iterable[dict[str, Any]],
    parent_plan_id: str,
    research_goal: dict[str, Any],
    source_universe: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Build one dynamic plan for every L3, initially executable at L3 itself."""

    plans = [
        build_l3_research_plan(
            node=node,
            parent_plan_id=parent_plan_id,
            research_goal=research_goal,
            source_universe=source_universe or {},
        )
        for node in l3_nodes
    ]
    index = {
        "schema_version": "4.0",
        "plan_type": "l3_deep_research_index",
        "parent_research_plan_id": parent_plan_id,
        "execution_policy": {
            "question_tree": "adaptive_depth_max_5",
            "planning_unit": "one_independent_plan_per_l3",
            "initial_depth": "L3_only",
            "executable_unit": "current_terminal_question",
            "material_collection": "active_question_search_only",
            "broad_material_pool": "candidate_only_not_completion_evidence",
            "branch_creation": "only_after_failed_answerability_gate",
            "l3_completion": "current_question_or_required_descendants_complete",
        },
        "plans": [
            {
                "l3_node_id": plan["l3_node_id"],
                "l3_plan_id": plan["plan_id"],
                "path": l3_plan_path(plan["l3_node_id"]),
                "event_path": l3_event_path(plan["l3_node_id"]),
                "active_steps": len(plan["steps"]),
                "leaf_steps": len(plan["steps"]),
                "max_depth": _tree_depth(plan["question_tree"]),
            }
            for plan in plans
        ],
    }
    return index, plans


def build_l3_research_plan(
    *,
    node: dict[str, Any],
    parent_plan_id: str,
    research_goal: dict[str, Any],
    source_universe: dict[str, Any],
) -> dict[str, Any]:
    node_id = str(node.get("logic_node_id") or node.get("id") or "").strip()
    question = str(node.get("question") or "").strip()
    if not node_id or not question:
        raise ValueError("Every L3 research plan requires a node id and question")
    title = str(node.get("title") or question).strip()
    lens_id = str(node.get("lens_id") or _stage_id(node_id)).strip()
    indicators = _text_list(node.get("indicators") or node.get("required_materials"))
    support_rule = str(
        node.get("support_rule") or node.get("support_evidence") or ""
    ).strip()
    refute_rule = str(
        node.get("refute_rule") or node.get("refute_evidence") or ""
    ).strip()
    downstream = _text_list(node.get("downstream_node_ids"))
    bridge_fields = _text_list(node.get("company_bridge_fields"))
    cadence = str(node.get("update_cadence") or "quarterly").strip()

    explicit_children = node.get("child_questions") or node.get("research_questions")
    question_tree = _build_question_tree(
        node_id=node_id,
        title=title,
        question=question,
        indicators=indicators,
        support_rule=support_rule,
        refute_rule=refute_rule,
        downstream=downstream,
        bridge_fields=bridge_fields,
        explicit_children=explicit_children,
    )
    return _assemble_l3_plan(
        question_tree=question_tree,
        parent_plan_id=parent_plan_id,
        node_id=node_id,
        title=title,
        question=question,
        lens_id=lens_id,
        research_goal=research_goal,
        source_universe=source_universe,
        indicators=indicators,
        support_rule=support_rule,
        refute_rule=refute_rule,
        downstream=downstream,
        bridge_fields=bridge_fields,
        cadence=cadence,
        expansion_history=[],
    )


def expand_l3_research_plan(
    plan: dict[str, Any],
    *,
    parent_question_id: str,
    evidence_gap: Any,
    child_questions: list[dict[str, Any]],
    source_universe: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Add exactly one question level after evidence shows the parent cannot answer."""

    gaps = _text_list(evidence_gap)
    if not gaps:
        raise ValueError("Dynamic expansion requires a concrete evidence gap")
    if not child_questions:
        raise ValueError("Dynamic expansion requires at least one child question")
    if any(
        isinstance(row, dict) and (row.get("children") or row.get("child_questions"))
        for row in child_questions
    ):
        raise ValueError("Dynamic expansion may add only one question level at a time")

    question_tree = deepcopy(plan.get("question_tree") or {})
    target = next(
        (
            node
            for node, _ in _walk_tree(question_tree)
            if str(node.get("question_id") or "") == parent_question_id
        ),
        None,
    )
    if target is None:
        raise ValueError(f"Unknown parent question: {parent_question_id}")
    if target.get("children"):
        raise ValueError(f"Question {parent_question_id} is already expanded")
    parent_level = int(target.get("level") or 0)
    if parent_level >= MAX_QUESTION_DEPTH:
        raise ValueError(f"Question tree cannot exceed L{MAX_QUESTION_DEPTH}")
    normalized = _normalize_explicit_children(
        child_questions,
        parent_id=parent_question_id,
        parent_level=parent_level,
        fallback_data=_text_list(target.get("required_data")),
    )
    covered_gaps: set[str] = set()
    for raw, child in zip(child_questions, normalized):
        trigger_gaps = _text_list(
            raw.get("trigger_gaps") or raw.get("trigger_gap")
        )
        if not trigger_gaps and len(gaps) == 1:
            trigger_gaps = list(gaps)
        unknown = [item for item in trigger_gaps if item not in gaps]
        if unknown:
            raise ValueError(
                "Child question trigger_gaps must come from the recorded parent gaps"
            )
        if not trigger_gaps:
            raise ValueError(
                "Every child question must name the parent gap it closes"
            )
        child["expansion_trigger"] = {
            "type": "failed_answerability_gate",
            "evidence_gaps": trigger_gaps,
        }
        covered_gaps.update(trigger_gaps)
    if covered_gaps != set(gaps):
        raise ValueError("Every selected parent gap must map to a child question")
    target["children"] = normalized
    target["expansion_trigger"] = {
        "type": "failed_answerability_gate",
        "evidence_gaps": gaps,
        "from_plan_id": str(plan.get("plan_id") or ""),
    }

    logic = dict(plan.get("logic_contract") or {})
    expansion_history = [
        *list(plan.get("expansion_history") or []),
        {
            "from_plan_id": str(plan.get("plan_id") or ""),
            "parent_question_id": parent_question_id,
            "parent_level": parent_level,
            "child_question_ids": [row["question_id"] for row in normalized],
            "trigger": "failed_answerability_gate",
            "evidence_gaps": gaps,
        },
    ]
    return _assemble_l3_plan(
        question_tree=question_tree,
        parent_plan_id=str(plan.get("parent_research_plan_id") or ""),
        node_id=str(plan.get("l3_node_id") or ""),
        title=str(plan.get("l3_title") or ""),
        question=str(plan.get("l3_question") or ""),
        lens_id=str(plan.get("lens_id") or ""),
        research_goal=dict(plan.get("research_goal") or {}),
        source_universe=source_universe or {},
        indicators=_text_list(logic.get("indicators")),
        support_rule=str(logic.get("support_rule") or ""),
        refute_rule=str(logic.get("refute_rule") or ""),
        downstream=_text_list(logic.get("downstream_node_ids")),
        bridge_fields=_text_list(logic.get("company_bridge_fields")),
        cadence=str(logic.get("update_cadence") or "quarterly"),
        expansion_history=expansion_history,
    )


def _assemble_l3_plan(
    *,
    question_tree: dict[str, Any],
    parent_plan_id: str,
    node_id: str,
    title: str,
    question: str,
    lens_id: str,
    research_goal: dict[str, Any],
    source_universe: dict[str, Any],
    indicators: list[str],
    support_rule: str,
    refute_rule: str,
    downstream: list[str],
    bridge_fields: list[str],
    cadence: str,
    expansion_history: list[dict[str, Any]],
) -> dict[str, Any]:
    identity = {
        "parent_research_plan_id": parent_plan_id,
        "l3_node_id": node_id,
        "question_tree": question_tree,
        "logic_chain_version": research_goal.get("logic_chain_version", ""),
        "expansion_history": expansion_history,
    }
    digest = hashlib.sha256(
        json.dumps(identity, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]
    plan_id = f"l3rp_{_slug(node_id)}_{digest}"

    leaf_rows = list(_leaf_rows(question_tree))
    step_ids_by_question = {
        str(leaf["question_id"]): f"question:{leaf['question_id']}"
        for leaf, _ in leaf_rows
    }
    steps: list[dict[str, Any]] = []
    for sequence, (leaf, path) in enumerate(leaf_rows, start=1):
        dependency_questions = _text_list(leaf.get("depends_on_question_ids"))
        missing = [
            dependency
            for dependency in dependency_questions
            if dependency not in step_ids_by_question
        ]
        if missing:
            raise ValueError(
                f"Question {leaf['question_id']} depends on unknown terminal questions: "
                + ", ".join(missing)
            )
        l4_question_id = next(
            (
                str(item["question_id"])
                for item in path
                if int(item.get("level") or 0) == 4
            ),
            "",
        )
        steps.append(
            _leaf_step(
                plan_id=plan_id,
                node_id=node_id,
                lens_id=lens_id,
                sequence=sequence,
                l4_question_id=l4_question_id,
                leaf=leaf,
                path=path,
                depends_on_step_ids=[
                    step_ids_by_question[item] for item in dependency_questions
                ],
                refute_rule=refute_rule,
                cadence=cadence,
                research_goal=research_goal,
                source_universe=source_universe,
            )
        )

    return {
        "schema_version": "4.0",
        "plan_type": "l3_deep_research",
        "plan_id": plan_id,
        "parent_research_plan_id": parent_plan_id,
        "l3_node_id": node_id,
        "l3_title": title,
        "l3_question": question,
        "lens_id": lens_id,
        "research_goal": dict(research_goal),
        "question_tree_policy": {
            "root_level": 3,
            "maximum_depth": MAX_QUESTION_DEPTH,
            "initial_depth": 3,
            "branching": "only_after_failed_answerability_gate",
            "terminal_definition": "the current deepest unanswered question",
        },
        "logic_contract": {
            "indicators": indicators,
            "support_rule": support_rule,
            "refute_rule": refute_rule,
            "downstream_node_ids": downstream,
            "company_bridge_fields": bridge_fields,
            "update_cadence": cadence,
        },
        "material_collection_policy": {
            "required_origin": "active_question_search",
            "required_trace_fields": list(ACTIVE_QUESTION_TRACE_FIELDS),
            "bulk_pool_mapping_eligible": False,
            "push_ingestion_role": "candidate_only",
            "source_reuse_rule": (
                "The same source may serve another active question only through a "
                "separate attachment, extraction, and GPT review for that question."
            ),
        },
        "completion_policy": {
            "l3_complete_when": "current_question_answerable_or_all_required_descendants_complete",
            "missing_evidence": "block_then_expand_only_the_observed_gap",
            "legacy_broad_search": "audit_only_not_retroactive_completion",
        },
        "expansion_history": expansion_history,
        "question_tree": question_tree,
        "steps": steps,
    }


def validate_l3_research_plan_set(
    *,
    parent_plan: dict[str, Any],
    index: dict[str, Any],
    plans: Iterable[dict[str, Any]],
    events_by_node: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """Validate exact L3 coverage and every adaptive leaf execution contract."""

    issues: list[dict[str, str]] = []
    plans = list(plans)
    events_by_node = events_by_node or {}
    expected_ids = {
        str(step.get("question_node_id") or "")
        for step in parent_plan.get("steps") or []
        if str(step.get("question_node_id") or "")
    }
    plan_ids = [str(plan.get("l3_node_id") or "") for plan in plans]
    actual_ids = set(plan_ids)
    for node_id in sorted(expected_ids - actual_ids):
        issues.append(
            _issue(
                "missing_l3_research_plan",
                f"L3 {node_id} has no independent research plan.",
                node_id,
            )
        )
    for node_id in sorted(actual_ids - expected_ids):
        issues.append(
            _issue(
                "extra_l3_research_plan",
                f"Unexpected L3 research plan for {node_id}.",
                node_id,
            )
        )
    for node_id in sorted({item for item in plan_ids if plan_ids.count(item) > 1}):
        issues.append(
            _issue(
                "duplicate_l3_research_plan",
                f"Duplicate L3 research plan for {node_id}.",
                node_id,
            )
        )

    indexed = {
        str(row.get("l3_node_id") or ""): row
        for row in index.get("plans") or []
        if isinstance(row, dict)
    }
    if str(index.get("parent_research_plan_id") or "") != str(
        parent_plan.get("plan_id") or ""
    ):
        issues.append(
            _issue(
                "l3_index_parent_mismatch",
                "L3 plan index does not reference the active parent plan.",
            )
        )

    results: list[dict[str, Any]] = []
    for plan in plans:
        node_id = str(plan.get("l3_node_id") or "")
        issues.extend(_l3_plan_shape_issues(plan))
        row = indexed.get(node_id)
        if not row or str(row.get("l3_plan_id") or "") != str(
            plan.get("plan_id") or ""
        ):
            issues.append(
                _issue(
                    "l3_plan_index_mismatch",
                    f"L3 plan index is missing or stale for {node_id}.",
                    node_id,
                )
            )
        execution = validate_research_plan_execution(
            plan,
            events_by_node.get(node_id, []),
        )
        issues.extend(execution["issues"])
        results.append(
            {
                "l3_node_id": node_id,
                "plan_id": plan.get("plan_id"),
                "max_depth": _tree_depth(plan.get("question_tree") or {}),
                **execution["summary"],
            }
        )

    leaf_steps = sum(int(row.get("steps") or 0) for row in results)
    completed_leaf_steps = sum(int(row.get("completed") or 0) for row in results)
    blocked_leaf_steps = sum(int(row.get("blocked") or 0) for row in results)
    completed_l3 = sum(row.get("status") == "completed" for row in results)
    status = (
        "completed"
        if results and completed_l3 == len(results)
        else "blocked"
        if blocked_leaf_steps
        else "in_progress"
        if completed_leaf_steps
        else "planned"
    )
    return {
        "ok": not any(row.get("severity") == "error" for row in issues),
        "issues": issues,
        "summary": {
            "parent_plan_id": str(parent_plan.get("plan_id") or ""),
            "status": status,
            "l3_plans": len(results),
            "completed_l3_plans": completed_l3,
            "leaf_steps": leaf_steps,
            "completed_leaf_steps": completed_leaf_steps,
            "blocked_leaf_steps": blocked_leaf_steps,
            "max_depth": max((int(row.get("max_depth") or 0) for row in results), default=0),
        },
        "plans": results,
    }


def l3_plan_path(node_id: str) -> str:
    return f"l3_research_plans/{_safe_node_id(node_id)}/research_plan.json"


def l3_event_path(node_id: str) -> str:
    return f"l3_research_plans/{_safe_node_id(node_id)}/research_step_events.jsonl"


def _build_question_tree(
    *,
    node_id: str,
    title: str,
    question: str,
    indicators: list[str],
    support_rule: str,
    refute_rule: str,
    downstream: list[str],
    bridge_fields: list[str],
    explicit_children: Any,
) -> dict[str, Any]:
    if explicit_children:
        raise ValueError(
            "Initial L3 plans cannot be pre-expanded; use "
            "expand_l3_research_plan after a failed answerability gate"
        )
    children: list[dict[str, Any]] = []
    root = {
        "question_id": node_id,
        "level": 3,
        "title": title,
        "question": question,
        "children": children,
    }
    if not children:
        root.update(
            _leaf_fields(
                dimension="l3_initial",
                required_data=(
                    indicators
                    or [
                        "直接回答当前 L3 问题的事实、对象、期间、口径与原文定位",
                        "至少一项独立交叉证据以及一项反向或边界证据",
                    ]
                ),
                analysis_plan=[
                    "先在 L3 层尝试形成事实、推断、判断和反证分离的答案",
                    "检验证据是否直接、口径一致、来源多样且足以回答当前问题",
                    "若不能回答，只把已观察到的证据缺口转化为下一层子问题",
                ],
                depends_on_question_ids=[],
                requires_refutation_search=True,
            )
        )
    return root


def _default_children(
    *,
    node_id: str,
    question: str,
    indicators: list[str],
    support_rule: str,
    refute_rule: str,
    downstream: list[str],
    bridge_fields: list[str],
) -> list[dict[str, Any]]:
    fact_parent_id = f"{node_id}.facts"
    fact_leaves = []
    for index, indicator in enumerate(indicators, start=1):
        leaf_question, required_data, analysis_plan = _indicator_leaf_spec(
            indicator=indicator,
            parent_question=question,
        )
        fact_leaves.append(
            _leaf_question(
                question_id=f"{fact_parent_id}.indicator_{index:02d}",
                level=5,
                title=indicator,
                question=leaf_question,
                dimension="indicator",
                required_data=required_data,
                analysis_plan=analysis_plan,
            )
        )
    if fact_leaves:
        facts = {
            "question_id": fact_parent_id,
            "level": 4,
            "title": "关键事实",
            "question": f"要回答“{question}”，每个核心指标的可验证状态分别是什么？",
            "children": fact_leaves,
        }
    else:
        facts = _leaf_question(
            question_id=fact_parent_id,
            level=4,
            title="关键事实",
            question=f"哪些直接可观测事实能够回答“{question}”？",
            dimension="indicator",
            required_data=[
                "直接回答父问题的官方事实或可复核数据",
                "对象、口径、单位、期间、发布日期和原文定位",
                "至少一项历史或前瞻参照；不存在时明确记录缺口",
            ],
            analysis_plan=[
                "统一口径并比较事实的方向与量级",
                "区分实际值、预测值与模型假设",
                "判断现有数据能否直接回答父问题",
            ],
        )

    fact_leaf_ids = [
        str(row["question_id"])
        for row, _ in _leaf_rows(facts)
    ]
    support_id = f"{node_id}.mechanism.support"
    bridge_id = f"{node_id}.mechanism.bridge"
    mechanism = {
        "question_id": f"{node_id}.mechanism",
        "level": 4,
        "title": "因果与商业传导",
        "question": "关键事实为什么会改变父问题的答案，并如何传导到下游和财务结果？",
        "children": [
            _leaf_question(
                question_id=support_id,
                level=5,
                title="核心机制",
                question=(
                    f"支持条件“{support_rule or '核心机制成立'}”是否有直接因果证据，而非只有相关性？"
                ),
                dimension="mechanism",
                required_data=[
                    "能够连接原因、约束、行为和结果的直接证据",
                    "客户、供应商或竞争者对同一机制的交叉材料",
                    "机制生效的对象、时间、边界条件与原文定位",
                ],
                analysis_plan=[
                    "还原因果链并区分相关性、领先指标与真实驱动",
                    "检查机制是否跨实体、跨期间成立，并识别替代解释",
                    "明确哪些证据直接支持、仅构成边界或仍待判断",
                ],
                depends_on_question_ids=fact_leaf_ids,
            ),
            _leaf_question(
                question_id=bridge_id,
                level=5,
                title="下游与财务桥",
                question=(
                    "该机制如何传导到"
                    f"{('、'.join(downstream) or '下游决策节点')}，并改变"
                    f"{('、'.join(bridge_fields) or '收入、利润和现金流')}？"
                ),
                dimension="financial_bridge",
                required_data=[
                    f"下游节点：{('、'.join(downstream) or '待明确')} 的可观测变化",
                    f"公司桥接字段：{('、'.join(bridge_fields) or '收入、利润、现金流')} 的披露",
                    "数量、价格、份额、成本、利润率或现金流之间的连接数据",
                    "公司/分部、期间、会计口径与原文定位",
                ],
                analysis_plan=[
                    "建立从业务量到收入、利润和现金流的可复算桥接",
                    "做基准、上行和下行情景，避免把主题暴露当作盈利兑现",
                    "标出最敏感假设和下一节点需要继承的结论",
                ],
                depends_on_question_ids=[support_id],
            ),
        ],
    }
    refutation = _leaf_question(
        question_id=f"{node_id}.refutation",
        level=4,
        title="反证与边界",
        question=(
            f"哪些证据会满足反证条件“{refute_rule or '父问题的核心判断不成立或不具持续性'}”，"
            "从而推翻、削弱或限定父问题的答案？"
        ),
        dimension="refutation",
        required_data=[
            "与支持证据同口径的反向指标、取消、延期、替代或监管事实",
            "最强可信反方观点及其数据和假设",
            "失效阈值、持续时间、监测频率与原文定位",
        ],
        analysis_plan=[
            "主动搜索最强反例，而不是只对支持材料做风险附注",
            "比较正反证据的直接性、时效、口径和解释力",
            "给出推翻、削弱、边界或未决判断，并定义可监测失效条件",
        ],
        depends_on_question_ids=fact_leaf_ids,
        requires_refutation_search=True,
    )
    return [facts, mechanism, refutation]


def _indicator_leaf_spec(
    *,
    indicator: str,
    parent_question: str,
) -> tuple[str, list[str], list[str]]:
    overrides: dict[str, tuple[str, list[str], list[str]]] = {
        "需求主体身份": (
            "哪些具体主体是终端算力需求方，各自主体资格由什么采购、部署或算力消费事实证明？",
            [
                "逐主体名称、主体类型及其终端需求角色",
                "采购、部署或算力消费的直接事实、期间和原文定位",
                "与 OEM、ODM、分销商和融资通道的关系",
            ],
            [
                "区分终端需求方、采购通道、供应商和融资主体",
                "逐主体核验身份并去重关联实体",
                "无法证明终端需求的主体保留为候选而非当前需求方",
            ],
        ),
        "当前或潜在未来标签": (
            "每个需求主体应归入当前需求方还是潜在未来需求方，互斥分类依据是什么？",
            [
                "逐主体当前采购、部署、使用或预算证据",
                "尚未形成规模需求但具备进入条件的可验证事实",
                "分类生效日期、证据来源和边界说明",
            ],
            [
                "按当前已形成需求与未来进入条件做互斥分类",
                "禁止同一主体同时进入两组，并说明边界案例",
                "记录因证据不足无法分类的主体",
            ],
        ),
        "需求形成状态": (
            "每个主体的需求处于意向、预算、采购承诺、订单、部署还是实际使用阶段？",
            [
                "逐主体需求阶段及对应的官方或交易对手证据",
                "预算、合同、交付、上线和使用的关键日期",
                "数量、金额或规模代理及其口径",
            ],
            [
                "按意向到实际使用的漏斗阶段分类",
                "识别阶段跃迁、停滞和重复计算",
                "只把订单、部署或实际使用作为当前需求的强证据",
            ],
        ),
        "Q1需求方覆盖": (
            "Q1 中每个当前需求方和潜在未来需求方是否都拥有独立数量记录或明确数据缺口？",
            [
                "Q1 当前与潜在未来需求方的完整互斥清单",
                "逐主体的直接数量、预测、样本、价值代理或缺口记录",
                "每条记录的来源、期间、单位和映射状态",
            ],
            [
                "将数量记录逐一对齐 Q1 清单并计算覆盖缺口",
                "当前与潜在未来主体分别处理，禁止混入当前基线",
                "没有数量的数据保留显式缺口，不用行业总量填补",
            ],
        ),
        "口径与期间": (
            "各需求数量使用什么对象、单位、期间和统计边界，哪些记录可比或可汇总？",
            [
                "每条数量的对象、单位、期间、地域、产品范围与去重边界",
                "实际值、订单、预测、样本和价值代理的明确标签",
                "定义变化、重叠主体和样本外推限制",
            ],
            [
                "建立口径兼容矩阵，只比较同对象、同单位和同期间数据",
                "识别重复主体、重叠样本和实际值与预测值混加",
                "不可比数据分表保留，不强行加总",
            ],
        ),
        "映射质量": (
            "每条数量对具体 Q1 需求方属于直接、代理、样本、缺口还是不可映射？",
            [
                "数量来源与具体需求方之间的直接关联证据",
                "代理变量、样本范围和外推假设",
                "无法分配到单一需求方的市场总量或预测",
            ],
            [
                "逐条判定 direct、proxy、sample、gap 或 unmapped",
                "审查代理链长度和样本代表性",
                "不可可靠映射的记录转入其它分类，不参与需求方加总",
            ],
        ),
        "其它未映射预测": (
            "哪些市场总量或预测无法可靠分配给 Q1 需求方，应如何单独保留？",
            [
                "无法分配的市场规模、出货、收入或算力预测",
                "预测方法、覆盖范围、期间、单位和重叠风险",
                "不能映射到 Q1 主体的具体原因",
            ],
            [
                "按信息类别而非需求方分类保留",
                "检查与已映射记录的覆盖重叠，禁止重复加总",
                "只作为行业背景或边界，不冒充当前需求方基线",
            ],
        ),
    }
    if indicator in overrides:
        return overrides[indicator]
    return (
        f"围绕“{parent_question}”，{indicator}应按什么口径衡量，当前值、可比历史和已披露前瞻分别是什么？",
        [
            f"{indicator}的实际值或可核验定性事实",
            "统计对象、纳入排除边界、定义、单位与样本范围",
            "发布日期、事实所属期间、预测目标期间与原文定位",
            "至少一项可比历史或前瞻锚点；不存在时明确记录缺口",
        ],
        [
            "统一定义、单位和期间，剔除不可比口径",
            "比较当前、历史与前瞻，判断方向、速度和是否出现拐点",
            "区分实际事实、管理层预期和第三方预测，并记录分歧",
        ],
    )


def _normalize_explicit_children(
    rows: list[Any],
    *,
    parent_id: str,
    parent_level: int,
    fallback_data: list[str],
) -> list[dict[str, Any]]:
    level = parent_level + 1
    if level > MAX_QUESTION_DEPTH:
        raise ValueError(f"Question tree cannot exceed L{MAX_QUESTION_DEPTH}")
    normalized: list[dict[str, Any]] = []
    for index, raw in enumerate(rows, start=1):
        if not isinstance(raw, dict):
            raise ValueError("Every child question must be an object")
        question = str(raw.get("question") or "").strip()
        if not question:
            raise ValueError("Every child question requires non-empty question text")
        question_id = str(raw.get("question_id") or raw.get("id") or "").strip()
        if not question_id:
            question_id = f"{parent_id}.q{index:02d}_{_slug(question)[:32]}"
        children = raw.get("children") or raw.get("child_questions") or []
        base = {
            "question_id": question_id,
            "level": level,
            "title": str(raw.get("title") or question).strip(),
            "question": question,
        }
        if children:
            if not isinstance(children, list):
                raise ValueError(f"{question_id} children must be a list")
            base["children"] = _normalize_explicit_children(
                children,
                parent_id=question_id,
                parent_level=level,
                fallback_data=fallback_data,
            )
        else:
            base.update(
                _leaf_fields(
                    dimension=str(raw.get("research_dimension") or "custom"),
                    required_data=(
                        _text_list(raw.get("required_data") or raw.get("required_materials"))
                        or fallback_data
                        or ["直接回答当前问题的可核验数据或事实"]
                    ),
                    analysis_plan=(
                        _text_list(raw.get("analysis_plan") or raw.get("analysis_methods"))
                        or [
                            "统一口径并比较支持与反向证据",
                            "完成与当前问题一一对应的分析并记录缺口",
                        ]
                    ),
                    depends_on_question_ids=_text_list(raw.get("depends_on_question_ids")),
                    requires_refutation_search=bool(raw.get("requires_refutation_search")),
                )
            )
        normalized.append(base)
    return normalized


def _leaf_question(
    *,
    question_id: str,
    level: int,
    title: str,
    question: str,
    dimension: str,
    required_data: list[str],
    analysis_plan: list[str],
    depends_on_question_ids: list[str] | None = None,
    requires_refutation_search: bool = False,
) -> dict[str, Any]:
    return {
        "question_id": question_id,
        "level": level,
        "title": title,
        "question": question,
        **_leaf_fields(
            dimension=dimension,
            required_data=required_data,
            analysis_plan=analysis_plan,
            depends_on_question_ids=depends_on_question_ids or [],
            requires_refutation_search=requires_refutation_search,
        ),
    }


def _leaf_fields(
    *,
    dimension: str,
    required_data: list[str],
    analysis_plan: list[str],
    depends_on_question_ids: list[str],
    requires_refutation_search: bool,
) -> dict[str, Any]:
    return {
        "research_dimension": dimension,
        "required_data": list(required_data),
        "analysis_plan": list(analysis_plan),
        "depends_on_question_ids": list(depends_on_question_ids),
        "requires_refutation_search": requires_refutation_search,
    }


def _leaf_step(
    *,
    plan_id: str,
    node_id: str,
    lens_id: str,
    sequence: int,
    l4_question_id: str,
    leaf: dict[str, Any],
    path: list[dict[str, Any]],
    depends_on_step_ids: list[str],
    refute_rule: str,
    cadence: str,
    research_goal: dict[str, Any],
    source_universe: dict[str, Any],
) -> dict[str, Any]:
    leaf_id = str(leaf["question_id"])
    dimension = str(leaf.get("research_dimension") or "custom")
    question = str(leaf.get("question") or "")
    question_level = int(leaf.get("level") or 0)
    step_id = f"question:{leaf_id}"
    source_plan = _source_plan(
        dimension=dimension,
        question=question,
        required_data=_text_list(leaf.get("required_data")),
    )
    return {
        "step_id": step_id,
        "stage_id": l4_question_id or node_id,
        "sequence": sequence,
        "question_node_id": leaf_id,
        "question_level": question_level,
        "research_step_id": step_id,
        "l3_plan_id": plan_id,
        "l3_node_id": node_id,
        "l4_question_id": l4_question_id,
        # Compatibility aliases remain readable for existing audit adapters.
        "leaf_question_id": leaf_id,
        "leaf_step_id": step_id,
        "level": question_level,
        "research_dimension": dimension,
        "question": question,
        "question_path": [
            {
                "question_id": str(item.get("question_id") or ""),
                "level": int(item.get("level") or 0),
                "question": str(item.get("question") or ""),
            }
            for item in path
        ],
        "decision_use": f"Answer the current terminal question before rolling up L3 {node_id}.",
        "depends_on_step_ids": depends_on_step_ids,
        "required_data": _text_list(leaf.get("required_data")),
        "required_materials": _text_list(leaf.get("required_data")),
        "analysis_plan": _text_list(leaf.get("analysis_plan")),
        "source_universe_plan": _source_universe_plan(source_universe),
        "source_plan": source_plan,
        "minimum_evidence_gate": {
            "rule": (
                "An active-question search run, source attachment, per-source extraction, "
                "GPT review, answer, support/refute result, refutation-search result, "
                "and dependency closure are required."
            ),
            "active_question_search_run_required": True,
            "search_run_id_required": True,
            "per_source_parse_required": True,
            "gpt_review_required": True,
            "direct_node_fit_required": True,
            "refutation_search_required": True,
            "required_source_buckets": ["evidence"],
        },
        "refuting_source_plan": [
            "Search specifically for evidence that would make this leaf answer false, "
            f"temporary, or bounded; parent refute rule: {refute_rule or 'not specified'}."
        ],
        "freshness_requirement": _freshness_requirement(research_goal, cadence),
        "preferred_specialty_skill": _preferred_skill(lens_id, dimension),
        "collection_contract": {
            "origin": "active_question_search",
            "required_trace_fields": list(ACTIVE_QUESTION_TRACE_FIELDS),
            "query_must_name_active_question": True,
            "bulk_pool_mapping_forbidden": True,
        },
        "answer_contract": {
            "required_fields": [
                "answer",
                "supporting_findings",
                "refuting_findings",
                "gaps",
                "next_actions",
            ],
            "rule": "Answer only the current question; separate facts, inference, judgment, refutation, and gaps.",
        },
        "traceability_contract": {
            "required_references": [
                "search_run_id",
                "source_ids",
                "source_extraction_ids",
                "source_review_ids",
            ],
            "event_ledger": "research_step_events.jsonl",
        },
        "initial_status": "pending",
    }


def _source_plan(
    *,
    dimension: str,
    question: str,
    required_data: list[str],
) -> list[dict[str, Any]]:
    data_text = " / ".join(required_data[:3]) or "direct measurable evidence"
    templates: dict[str, list[tuple[str, str, list[str], str]]] = {
        "indicator": [
            (
                "evidence",
                "official filing, official dataset, customer or supplier disclosure",
                ["published_at", "effective_period", "target_period", "entity", "metric", "value", "unit", "definition", "locator"],
                "Provides the directly measured fact and a comparable time anchor.",
            ),
            (
                "research_report",
                "independent specialist dataset or disclosed-method forecast",
                ["methodology", "sample", "period", "estimate", "assumptions", "limitations"],
                "Tests the official data against an independent measure or forecast.",
            ),
        ],
        "mechanism": [
            (
                "evidence",
                "technical disclosure, customer deployment, or counterparty filing",
                ["cause", "mechanism", "observed_effect", "boundary", "entity", "period", "locator"],
                "Tests causality with observable operating evidence.",
            ),
            (
                "research_report",
                "independent mechanism study or channel cross-check",
                ["methodology", "alternative_explanation", "support", "conflict", "limitation"],
                "Challenges correlation and surfaces alternative explanations.",
            ),
        ],
        "financial_bridge": [
            (
                "evidence",
                "company filing, earnings call, segment disclosure, or counterparty order data",
                ["company", "segment", "volume", "price", "share", "revenue", "margin", "cash_flow", "period", "locator"],
                "Builds a reproducible bridge from operating change to company economics.",
            ),
            (
                "research_report",
                "independent earnings bridge or scenario model with assumptions",
                ["base_case", "upside_case", "downside_case", "sensitivity", "assumptions"],
                "Makes earnings sensitivity and disagreement explicit.",
            ),
        ],
        "refutation": [
            (
                "evidence",
                "official contrary fact, cancellation, substitution, delay, or regulatory record",
                ["refuting_fact", "event_date", "metric", "threshold", "duration", "locator"],
                "Directly searches for evidence that overturns or bounds the parent answer.",
            ),
            (
                "research_report",
                "independent bear case or boundary analysis",
                ["bear_case", "assumptions", "trigger", "monitoring_metric", "limitation"],
                "Defines the strongest credible alternative hypothesis.",
            ),
        ],
        "custom": [
            (
                "evidence",
                "primary source that directly answers this leaf",
                ["published_at", "period", "entity", "fact", "definition", "locator"],
                "Anchors the leaf answer in direct evidence.",
            ),
            (
                "research_report",
                "independent source that supports, challenges, or bounds the answer",
                ["methodology", "finding", "assumption", "conflict", "limitation"],
                "Provides independent verification and a contrary test.",
            ),
        ],
    }
    rows = templates.get(dimension, templates["custom"])
    return [
        {
            "source_bucket": bucket,
            "source_type": source_type,
            "examples_or_search_queries": [f"{question} {data_text}"],
            "why_needed": why_needed,
            "expected_fields": expected_fields,
            "preferred_skill": _skill_for_source(source_type, dimension),
            "deepseek_allowed": bucket == "research_report",
        }
        for bucket, source_type, expected_fields, why_needed in rows
    ]


def _l3_plan_shape_issues(plan: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    node_id = str(plan.get("l3_node_id") or "")
    if plan.get("plan_type") != "l3_deep_research":
        issues.append(
            _issue(
                "invalid_l3_plan_type",
                "L3 plan must use plan_type=l3_deep_research.",
                node_id,
            )
        )
    if not str(plan.get("parent_research_plan_id") or ""):
        issues.append(
            _issue(
                "missing_l3_parent_plan",
                "L3 plan must reference its parent plan.",
                node_id,
            )
        )
    policy = plan.get("material_collection_policy") or {}
    if policy.get("required_origin") != "active_question_search":
        issues.append(
            _issue(
                "invalid_active_question_collection_origin",
                "Material collection must originate from active_question_search.",
                node_id,
            )
        )
    if policy.get("bulk_pool_mapping_eligible") is not False:
        issues.append(
            _issue(
                "bulk_pool_mapping_enabled",
                "A broad material pool cannot be eligible for L3 completion.",
                node_id,
            )
        )
    required_trace = set(policy.get("required_trace_fields") or [])
    if not set(ACTIVE_QUESTION_TRACE_FIELDS).issubset(required_trace):
        issues.append(
            _issue(
                "missing_active_question_trace_fields",
                "L3 plan is missing active-question search trace fields.",
                node_id,
            )
        )

    tree = plan.get("question_tree") or {}
    nodes = list(_walk_tree(tree)) if isinstance(tree, dict) and tree else []
    if not nodes or int(tree.get("level") or 0) != 3:
        issues.append(
            _issue(
                "missing_l3_question_tree",
                "L3 plan must contain a question_tree rooted at L3.",
                node_id,
            )
        )
        return issues
    if _tree_depth(tree) > MAX_QUESTION_DEPTH:
        issues.append(
            _issue(
                "question_tree_too_deep",
                f"Question tree cannot exceed L{MAX_QUESTION_DEPTH}.",
                node_id,
            )
        )
    question_ids: list[str] = []
    for current, parent in nodes:
        question_id = str(current.get("question_id") or "")
        question_ids.append(question_id)
        if not question_id or not str(current.get("question") or "").strip():
            issues.append(
                _issue(
                    "invalid_question_node",
                    "Every question node needs a stable id and non-empty question.",
                    node_id,
                )
            )
        if parent is not None and int(current.get("level") or 0) != int(
            parent.get("level") or 0
        ) + 1:
            issues.append(
                _issue(
                    "non_contiguous_question_depth",
                    f"{question_id} must be exactly one level below its parent.",
                    node_id,
                )
            )
        if current.get("children"):
            continue
        if not _text_list(current.get("required_data")):
            issues.append(
                _issue(
                    "leaf_missing_required_data",
                    f"Leaf {question_id} must state what data to collect.",
                    node_id,
                )
            )
        if not _text_list(current.get("analysis_plan")):
            issues.append(
                _issue(
                    "leaf_missing_analysis_plan",
                    f"Leaf {question_id} must state what analysis to perform.",
                    node_id,
                )
            )
    for duplicate in sorted(
        {item for item in question_ids if item and question_ids.count(item) > 1}
    ):
        issues.append(
            _issue(
                "duplicate_question_id",
                f"Question id {duplicate} is duplicated within the L3 plan.",
                node_id,
            )
        )

    leaves = [current for current, _ in nodes if not current.get("children")]
    steps = [row for row in plan.get("steps") or [] if isinstance(row, dict)]
    leaf_ids = {str(row.get("question_id") or "") for row in leaves}
    step_leaf_ids = {str(step.get("question_node_id") or "") for step in steps}
    if leaf_ids != step_leaf_ids:
        issues.append(
            _issue(
                "terminal_step_coverage_mismatch",
                "Every terminal question must map to exactly one executable step.",
                node_id,
            )
        )
    for step in steps:
        step_id = str(step.get("step_id") or node_id)
        if int(step.get("level") or 0) not in {3, 4, 5}:
            issues.append(
                _issue(
                    "invalid_terminal_level",
                    "Executable terminal questions must be L3, L4, or L5.",
                    step_id,
                )
            )
        if not _text_list(step.get("required_data")):
            issues.append(
                _issue(
                    "step_missing_required_data",
                    "Every terminal step must state the data to collect.",
                    step_id,
                )
            )
        if not _text_list(step.get("analysis_plan")):
            issues.append(
                _issue(
                    "step_missing_analysis_plan",
                    "Every terminal step must state the analysis to perform.",
                    step_id,
                )
            )
        contract = step.get("collection_contract") or {}
        if (
            contract.get("origin") != "active_question_search"
            or contract.get("bulk_pool_mapping_forbidden") is not True
        ):
            issues.append(
                _issue(
                    "invalid_active_question_collection_contract",
                    "Every terminal step must forbid broad-pool mapping and require active-question search.",
                    step_id,
                )
            )
        queries = [
            str(query).strip()
            for source in step.get("source_plan") or []
            for query in source.get("examples_or_search_queries") or []
            if str(query).strip()
        ]
        if not queries:
            issues.append(
                _issue(
                    "terminal_missing_search_query",
                    "Every terminal question must own at least one targeted internal search query.",
                    step_id,
                )
            )
    return issues


def _walk_tree(
    node: dict[str, Any],
    parent: dict[str, Any] | None = None,
) -> Iterator[tuple[dict[str, Any], dict[str, Any] | None]]:
    yield node, parent
    for child in node.get("children") or []:
        if isinstance(child, dict):
            yield from _walk_tree(child, node)


def _leaf_rows(
    node: dict[str, Any],
    path: list[dict[str, Any]] | None = None,
) -> Iterator[tuple[dict[str, Any], list[dict[str, Any]]]]:
    current_path = [*(path or []), node]
    children = [row for row in node.get("children") or [] if isinstance(row, dict)]
    if not children:
        yield node, current_path
        return
    for child in children:
        yield from _leaf_rows(child, current_path)


def _tree_depth(node: dict[str, Any]) -> int:
    return max(
        (int(current.get("level") or 0) for current, _ in _walk_tree(node)),
        default=0,
    )


def _source_universe_plan(source_universe: dict[str, Any]) -> dict[str, Any]:
    return {
        "registry": "config/source_universes.json",
        "domain_id": str(source_universe.get("domain_id") or ""),
        "priority_source_ids": [
            str(row.get("id") or "")
            for row in source_universe.get("priority_sources") or []
            if isinstance(row, dict) and str(row.get("id") or "")
        ][:8],
    }


def _freshness_requirement(goal: dict[str, Any], cadence: str) -> str:
    if str(goal.get("run_mode") or "") == "historical_backtest":
        return (
            f"Only sources visible on or before {goal.get('as_of_date') or 'the cutoff'}; "
            f"preserve visibility proof. Refresh cadence: {cadence}."
        )
    return (
        "Use the latest available source as of "
        f"{goal.get('as_of_date') or goal.get('report_date') or 'the report date'}. "
        f"Refresh cadence: {cadence}."
    )


def _preferred_skill(lens_id: str, dimension: str) -> str:
    if dimension == "refutation":
        return "industry-report-analysis"
    if dimension == "financial_bridge":
        return "financial-statement-analysis"
    return {
        "valuation": "valuation-analysis",
        "esg": "news-event-analysis",
        "technology": "industry-report-analysis",
        "supply": "supply-chain-chokepoint-analysis",
        "demand": "industry-report-analysis",
    }.get(lens_id, "leaf-research-deepseek")


def _skill_for_source(source_type: str, dimension: str) -> str:
    if "filing" in source_type or dimension == "financial_bridge":
        return "financial-statement-analysis"
    if "research" in source_type or "dataset" in source_type or dimension == "refutation":
        return "industry-report-analysis"
    return "leaf-research-deepseek"


def _safe_node_id(node_id: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9._-]+", "-", str(node_id)).strip("-.")
    if not normalized:
        raise ValueError("L3 node id cannot produce an empty plan directory")
    return normalized


def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower() or "node"


def _stage_id(node_id: str) -> str:
    return str(node_id).split(".", 1)[0]


def _text_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value is None:
        return []
    text = str(value).strip()
    return [text] if text else []


def _issue(code: str, message: str, step_id: str = "") -> dict[str, str]:
    return {
        "severity": "error",
        "code": code,
        "message": message,
        "step_id": step_id,
    }
