from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Iterable

from value_invest_research.domain.research_plan import validate_research_plan_execution


L4_RESEARCH_UNITS = (
    ("scope", "边界与口径"),
    ("actual", "当前事实"),
    ("history", "历史变化"),
    ("forward", "前瞻路径"),
    ("mechanism", "因果与财务传导"),
    ("triangulation", "交叉验证"),
    ("refutation", "反证与失效条件"),
)

LEAF_TRACE_FIELDS = (
    "l3_plan_id",
    "l3_node_id",
    "l4_question_id",
    "leaf_question_id",
    "leaf_step_id",
    "search_run_id",
)


def upgrade_parent_plan_for_l3_plans(
    parent_plan: dict[str, Any],
) -> dict[str, Any]:
    """Create a new immutable parent version whose L3 steps are child rollups."""

    upgraded = {
        **parent_plan,
        "schema_version": "2.0",
        "execution_policy": {
            **dict(parent_plan.get("execution_policy") or {}),
            "completion": "all_required_l3_child_plans_complete",
            "material_collection": "finest_leaf_question_only",
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
                        "The L3 rollup completes only after every mandatory "
                        "leaf step in its independent child plan passes."
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
    """Build one independent, leaf-search-driven plan for every L3 node."""

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
        "schema_version": "2.0",
        "plan_type": "l3_deep_research_index",
        "parent_research_plan_id": parent_plan_id,
        "execution_policy": {
            "planning_unit": "one_independent_plan_per_l3",
            "executable_unit": "finest_leaf_question",
            "material_collection": "leaf_question_search_only",
            "broad_material_pool": "candidate_only_not_completion_evidence",
            "l3_completion": "all_mandatory_leaf_steps_complete",
        },
        "plans": [
            {
                "l3_node_id": plan["l3_node_id"],
                "l3_plan_id": plan["plan_id"],
                "path": l3_plan_path(plan["l3_node_id"]),
                "event_path": l3_event_path(plan["l3_node_id"]),
                "leaf_steps": len(plan["steps"]),
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
    indicators = _text_list(
        node.get("indicators") or node.get("required_materials")
    )
    support_rule = str(
        node.get("support_rule") or node.get("support_evidence") or ""
    ).strip()
    refute_rule = str(
        node.get("refute_rule") or node.get("refute_evidence") or ""
    ).strip()
    downstream = _text_list(node.get("downstream_node_ids"))
    bridge_fields = _text_list(node.get("company_bridge_fields"))
    cadence = str(node.get("update_cadence") or "quarterly").strip()

    identity = {
        "parent_research_plan_id": parent_plan_id,
        "l3_node_id": node_id,
        "question": question,
        "indicators": indicators,
        "support_rule": support_rule,
        "refute_rule": refute_rule,
        "logic_chain_version": research_goal.get("logic_chain_version", ""),
    }
    digest = hashlib.sha256(
        json.dumps(identity, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]
    plan_id = f"l3rp_{_slug(node_id)}_{digest}"
    l4_units: list[dict[str, Any]] = []
    steps: list[dict[str, Any]] = []
    step_ids: dict[str, str] = {}

    for sequence, (unit_id, label) in enumerate(L4_RESEARCH_UNITS, start=1):
        l4_id = f"{node_id}.l4.{unit_id}"
        leaf_id = f"{l4_id}.l5.answer"
        step_id = f"leaf:{node_id}:{unit_id}"
        step_ids[unit_id] = step_id
        leaf_question = _leaf_question(
            unit_id=unit_id,
            l3_question=question,
            indicators=indicators,
            support_rule=support_rule,
            refute_rule=refute_rule,
            downstream=downstream,
            bridge_fields=bridge_fields,
        )
        l4_units.append(
            {
                "l4_question_id": l4_id,
                "level": 4,
                "title": label,
                "question": _l4_question(unit_id, question),
                "leaf_question_ids": [leaf_id],
            }
        )
        steps.append(
            _leaf_step(
                plan_id=plan_id,
                node_id=node_id,
                lens_id=lens_id,
                sequence=sequence,
                unit_id=unit_id,
                l4_id=l4_id,
                leaf_id=leaf_id,
                step_id=step_id,
                question=leaf_question,
                indicators=indicators,
                refute_rule=refute_rule,
                cadence=cadence,
                research_goal=research_goal,
                source_universe=source_universe,
            )
        )

    dependencies = {
        "scope": [],
        "actual": [step_ids["scope"]],
        "history": [step_ids["scope"]],
        "forward": [step_ids["actual"], step_ids["history"]],
        "mechanism": [step_ids["actual"], step_ids["forward"]],
        "triangulation": [step_ids["actual"]],
        "refutation": [step_ids["actual"]],
    }
    for step in steps:
        step["depends_on_step_ids"] = dependencies[step["research_dimension"]]

    return {
        "schema_version": "2.0",
        "plan_type": "l3_deep_research",
        "plan_id": plan_id,
        "parent_research_plan_id": parent_plan_id,
        "l3_node_id": node_id,
        "l3_title": title,
        "l3_question": question,
        "lens_id": lens_id,
        "research_goal": dict(research_goal),
        "logic_contract": {
            "indicators": indicators,
            "support_rule": support_rule,
            "refute_rule": refute_rule,
            "downstream_node_ids": downstream,
            "company_bridge_fields": bridge_fields,
            "update_cadence": cadence,
        },
        "material_collection_policy": {
            "required_origin": "leaf_question_search",
            "required_trace_fields": list(LEAF_TRACE_FIELDS),
            "bulk_pool_mapping_eligible": False,
            "push_ingestion_role": "candidate_only",
            "source_reuse_rule": (
                "The same source may serve another leaf only through a separate "
                "leaf attachment, extraction, and GPT review for that leaf."
            ),
        },
        "completion_policy": {
            "l3_complete_when": "all_mandatory_leaf_steps_complete",
            "missing_leaf_evidence": "blocked_not_inferred",
            "legacy_broad_search": "audit_only_not_retroactive_completion",
        },
        "l4_units": l4_units,
        "steps": steps,
    }


def validate_l3_research_plan_set(
    *,
    parent_plan: dict[str, Any],
    index: dict[str, Any],
    plans: Iterable[dict[str, Any]],
    events_by_node: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """Validate exact L3 coverage and every nested leaf execution contract."""

    issues: list[dict[str, str]] = []
    plans = list(plans)
    events_by_node = events_by_node or {}
    expected_ids = {
        str(step.get("question_node_id") or "")
        for step in parent_plan.get("steps") or []
        if str(step.get("execution_mode") or "") == "child_plan_rollup"
    }
    if not expected_ids:
        expected_ids = {
            str(step.get("question_node_id") or "")
            for step in parent_plan.get("steps") or []
            if str(step.get("question_node_id") or "")
        }
    plan_ids = [str(plan.get("l3_node_id") or "") for plan in plans]
    actual_ids = set(plan_ids)
    for node_id in sorted(expected_ids - actual_ids):
        issues.append(_issue("missing_l3_research_plan", f"L3 {node_id} has no independent research plan.", node_id))
    for node_id in sorted(actual_ids - expected_ids):
        issues.append(_issue("extra_l3_research_plan", f"Unexpected L3 research plan for {node_id}.", node_id))
    for node_id in sorted({item for item in plan_ids if plan_ids.count(item) > 1}):
        issues.append(_issue("duplicate_l3_research_plan", f"Duplicate L3 research plan for {node_id}.", node_id))

    indexed = {
        str(row.get("l3_node_id") or ""): row
        for row in index.get("plans") or []
        if isinstance(row, dict)
    }
    if str(index.get("parent_research_plan_id") or "") != str(parent_plan.get("plan_id") or ""):
        issues.append(_issue("l3_index_parent_mismatch", "L3 plan index does not reference the active parent plan."))

    results: list[dict[str, Any]] = []
    for plan in plans:
        node_id = str(plan.get("l3_node_id") or "")
        issues.extend(_l3_plan_shape_issues(plan))
        row = indexed.get(node_id)
        if not row or str(row.get("l3_plan_id") or "") != str(plan.get("plan_id") or ""):
            issues.append(_issue("l3_plan_index_mismatch", f"L3 plan index is missing or stale for {node_id}.", node_id))
        execution = validate_research_plan_execution(
            plan,
            events_by_node.get(node_id, []),
        )
        issues.extend(execution["issues"])
        results.append(
            {
                "l3_node_id": node_id,
                "plan_id": plan.get("plan_id"),
                **execution["summary"],
            }
        )

    leaf_steps = sum(int(row.get("steps") or 0) for row in results)
    completed_leaf_steps = sum(int(row.get("completed") or 0) for row in results)
    blocked_leaf_steps = sum(int(row.get("blocked") or 0) for row in results)
    completed_l3 = sum(
        row.get("status") == "completed" for row in results
    )
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
        },
        "plans": results,
    }


def attach_l3_plan_summaries(
    view: dict[str, Any],
    *,
    plans: Iterable[dict[str, Any]],
    events_by_node: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """Attach a reader-safe plan outline without exposing raw search queries."""

    events_by_node = events_by_node or {}
    summaries: dict[str, dict[str, Any]] = {}
    for plan in plans:
        node_id = str(plan.get("l3_node_id") or "")
        execution = validate_research_plan_execution(
            plan,
            events_by_node.get(node_id, []),
        )
        state_by_step = {
            str(row.get("step_id") or ""): row
            for row in execution.get("step_states") or []
        }
        steps_by_leaf = {
            str(row.get("leaf_question_id") or ""): row
            for row in plan.get("steps") or []
            if isinstance(row, dict)
        }
        units = []
        for unit in plan.get("l4_units") or []:
            leaves = []
            for leaf_id in unit.get("leaf_question_ids") or []:
                step = steps_by_leaf.get(str(leaf_id)) or {}
                state = state_by_step.get(str(step.get("step_id") or "")) or {}
                leaves.append(
                    {
                        "leaf_question_id": str(leaf_id),
                        "leaf_step_id": str(step.get("step_id") or ""),
                        "question": str(step.get("question") or ""),
                        "status": str(state.get("status") or "pending"),
                        "required_source_types": [
                            str(source.get("source_type") or "")
                            for source in step.get("source_plan") or []
                            if str(source.get("source_type") or "")
                        ],
                    }
                )
            units.append(
                {
                    "l4_question_id": str(unit.get("l4_question_id") or ""),
                    "title": str(unit.get("title") or ""),
                    "question": str(unit.get("question") or ""),
                    "leaves": leaves,
                }
            )
        summaries[node_id] = {
            "plan_id": str(plan.get("plan_id") or ""),
            "status": str(execution.get("summary", {}).get("status") or "planned"),
            "leaf_steps": int(execution.get("summary", {}).get("steps") or 0),
            "completed_leaf_steps": int(execution.get("summary", {}).get("completed") or 0),
            "material_collection_policy": "按每个 L5 叶子问题单独搜索、单独解析、单独复核",
            "l4_units": units,
        }

    for lens in view.get("lenses") or []:
        for node in lens.get("logic_nodes") or []:
            node["research_plan"] = summaries.get(
                str(node.get("logic_node_id") or ""),
                {},
            )
    view["l3_plan_coverage"] = {
        "planned_l3_nodes": len(summaries),
        "completed_l3_nodes": sum(
            row.get("status") == "completed" for row in summaries.values()
        ),
        "leaf_steps": sum(
            int(row.get("leaf_steps") or 0) for row in summaries.values()
        ),
        "completed_leaf_steps": sum(
            int(row.get("completed_leaf_steps") or 0)
            for row in summaries.values()
        ),
    }
    return view


def l3_plan_path(node_id: str) -> str:
    return f"l3_research_plans/{_safe_node_id(node_id)}/research_plan.json"


def l3_event_path(node_id: str) -> str:
    return f"l3_research_plans/{_safe_node_id(node_id)}/research_step_events.jsonl"


def _leaf_step(
    *,
    plan_id: str,
    node_id: str,
    lens_id: str,
    sequence: int,
    unit_id: str,
    l4_id: str,
    leaf_id: str,
    step_id: str,
    question: str,
    indicators: list[str],
    refute_rule: str,
    cadence: str,
    research_goal: dict[str, Any],
    source_universe: dict[str, Any],
) -> dict[str, Any]:
    source_plan = _source_plan(
        unit_id=unit_id,
        question=question,
        indicators=indicators,
    )
    return {
        "step_id": step_id,
        "stage_id": l4_id,
        "sequence": sequence,
        "question_node_id": leaf_id,
        "l3_plan_id": plan_id,
        "l3_node_id": node_id,
        "l4_question_id": l4_id,
        "leaf_question_id": leaf_id,
        "leaf_step_id": step_id,
        "level": 5,
        "research_dimension": unit_id,
        "question": question,
        "decision_use": f"Complete the {unit_id} evidence unit for L3 {node_id}.",
        "depends_on_step_ids": [],
        "required_materials": indicators or ["direct question-fit evidence"],
        "source_universe_plan": _source_universe_plan(source_universe),
        "source_plan": source_plan,
        "minimum_evidence_gate": {
            "rule": (
                "A leaf-specific search run, source attachment, per-source extraction, "
                "GPT review, answer, explicit support/refute result, and dependency closure are required."
            ),
            "leaf_search_run_required": True,
            "search_run_id_required": True,
            "per_source_parse_required": True,
            "gpt_review_required": True,
            "direct_node_fit_required": True,
            "refutation_search_required": unit_id == "refutation",
            "required_source_buckets": ["evidence"] if unit_id in {"scope", "actual", "history", "forward", "mechanism"} else [],
        },
        "refuting_source_plan": [
            f"Search specifically for evidence that establishes: {refute_rule or 'the L3 answer is wrong, temporary, or bounded'}"
        ],
        "freshness_requirement": _freshness_requirement(research_goal, cadence),
        "preferred_specialty_skill": _preferred_skill(lens_id, unit_id),
        "collection_contract": {
            "origin": "leaf_question_search",
            "required_trace_fields": list(LEAF_TRACE_FIELDS),
            "query_must_name_leaf_question": True,
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
            "rule": "Answer only this leaf; separate facts, inference, judgment, refutation, and gaps.",
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
    unit_id: str,
    question: str,
    indicators: list[str],
) -> list[dict[str, Any]]:
    indicator_text = " / ".join(indicators[:5]) or "direct measurable evidence"
    templates: dict[str, list[tuple[str, str, str, list[str], str]]] = {
        "scope": [
            ("evidence", "official definition, standard, or company methodology", f"{question} 官方 定义 统计口径", ["definition", "inclusion", "exclusion", "unit", "locator"], "Fixes the denominator and prevents category drift."),
        ],
        "actual": [
            ("evidence", "latest filing, official dataset, customer or supplier disclosure", f"{question} {indicator_text} actual latest filing", ["published_at", "effective_period", "entity", "metric", "value", "unit", "locator"], "Anchors the current answer in observed facts."),
        ],
        "history": [
            ("evidence", "same-definition historical filing or official dataset", f"{question} {indicator_text} historical series YoY", ["period", "metric", "value", "unit", "definition_change", "locator"], "Tests direction and acceleration on a comparable basis."),
        ],
        "forward": [
            ("evidence", "official guidance, backlog, order, capacity, or customer plan", f"{question} guidance backlog capacity target period", ["published_at", "target_period", "guidance", "commitment", "assumption", "locator"], "Establishes a dated forward anchor."),
            ("research_report", "independent forecast with disclosed assumptions", f"{question} independent forecast bear case assumptions", ["target_period", "forecast", "methodology", "assumptions", "bear_case"], "Makes forecast disagreement and failure conditions visible."),
        ],
        "mechanism": [
            ("evidence", "engineering disclosure plus company segment economics", f"{question} mechanism revenue margin cash flow segment", ["mechanism", "downstream_entity", "revenue_bridge", "margin_bridge", "cash_flow_bridge", "locator"], "Connects the node to delivery and investable financial outcomes."),
        ],
        "triangulation": [
            ("evidence", "counterparty filing or customer/supplier disclosure", f"{question} customer supplier cross check", ["counterparty", "period", "confirming_fact", "conflict", "locator"], "Checks the claim from the other side of the transaction."),
            ("research_report", "independent specialist dataset or channel study", f"{question} independent dataset methodology", ["methodology", "sample", "metric", "period", "limitation"], "Tests whether official claims survive independent measurement."),
        ],
        "refutation": [
            ("evidence", "official contrary fact, cancellation, substitution, or regulatory record", f"{question} contrary evidence cancellation substitution delay", ["refuting_fact", "event_date", "metric", "threshold", "duration", "locator"], "Directly searches for evidence that would weaken or overturn the L3 conclusion."),
            ("research_report", "independent bear case or boundary analysis", f"{question} bear case downside boundary", ["bear_case", "assumptions", "trigger", "probability", "monitoring_metric"], "Defines the strongest credible alternative explanation."),
        ],
    }
    return [
        {
            "source_bucket": bucket,
            "source_type": source_type,
            "examples_or_search_queries": [query],
            "why_needed": why_needed,
            "expected_fields": expected_fields,
            "preferred_skill": _skill_for_source(source_type, unit_id),
            "deepseek_allowed": bucket == "research_report",
        }
        for bucket, source_type, query, expected_fields, why_needed in templates[unit_id]
    ]


def _leaf_question(
    *,
    unit_id: str,
    l3_question: str,
    indicators: list[str],
    support_rule: str,
    refute_rule: str,
    downstream: list[str],
    bridge_fields: list[str],
) -> str:
    metrics = "、".join(indicators[:5]) or "直接可观测指标"
    return {
        "scope": f"回答“{l3_question}”时，研究对象、纳入排除边界、指标口径、单位和期间分别是什么？",
        "actual": f"围绕“{l3_question}”，当前有哪些关于{metrics}的可验证实际事实？",
        "history": f"围绕“{l3_question}”，{metrics}在同口径历史序列中如何变化，是否存在结构性拐点？",
        "forward": f"围绕“{l3_question}”，已披露的指引、订单、产能、客户计划或独立预测给出怎样的前瞻路径和假设？",
        "mechanism": (
            f"围绕“{l3_question}”，证据通过什么因果机制传导到"
            f"{('、'.join(downstream) or '下游节点')}以及"
            f"{('、'.join(bridge_fields) or '收入、利润和现金流')}？"
        ),
        "triangulation": f"围绕“{l3_question}”，客户、供应商、竞争者或独立数据能否交叉验证，主要冲突和样本偏差是什么？",
        "refutation": (
            f"哪些直接证据能够满足反证条件“{refute_rule or '核心机制不成立或影响不具持续性'}”，"
            f"并推翻、削弱或限定支持规则“{support_rule or '当前判断'}”？"
        ),
    }[unit_id]


def _l4_question(unit_id: str, question: str) -> str:
    label = dict(L4_RESEARCH_UNITS)[unit_id]
    return f"{label}：需要回答哪些最细问题，才能完成 L3“{question}”？"


def _l3_plan_shape_issues(plan: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    node_id = str(plan.get("l3_node_id") or "")
    if plan.get("plan_type") != "l3_deep_research":
        issues.append(_issue("invalid_l3_plan_type", "L3 plan must use plan_type=l3_deep_research.", node_id))
    if not str(plan.get("parent_research_plan_id") or ""):
        issues.append(_issue("missing_l3_parent_plan", "L3 plan must reference its parent plan.", node_id))
    policy = plan.get("material_collection_policy") or {}
    if policy.get("required_origin") != "leaf_question_search":
        issues.append(_issue("invalid_leaf_collection_origin", "Material collection must originate from leaf_question_search.", node_id))
    if policy.get("bulk_pool_mapping_eligible") is not False:
        issues.append(_issue("bulk_pool_mapping_enabled", "A broad material pool cannot be eligible for L3 completion.", node_id))
    required_trace = set(policy.get("required_trace_fields") or [])
    if not set(LEAF_TRACE_FIELDS).issubset(required_trace):
        issues.append(_issue("missing_leaf_trace_fields", "L3 plan is missing leaf-search trace fields.", node_id))
    units = [row for row in plan.get("l4_units") or [] if isinstance(row, dict)]
    steps = [row for row in plan.get("steps") or [] if isinstance(row, dict)]
    if [str(row.get("l4_question_id") or "").rsplit(".", 1)[-1] for row in units] != [unit_id for unit_id, _ in L4_RESEARCH_UNITS]:
        issues.append(_issue("invalid_l4_unit_order", "L3 plan must contain all seven L4 research units in canonical order.", node_id))
    leaf_ids = {str(step.get("leaf_question_id") or "") for step in steps}
    for unit in units:
        owned = [str(item) for item in unit.get("leaf_question_ids") or []]
        if not owned or any(item not in leaf_ids for item in owned):
            issues.append(_issue("l4_unit_missing_leaf", f"{unit.get('l4_question_id')} has no executable L5 leaf.", node_id))
    for step in steps:
        if int(step.get("level") or 0) != 5:
            issues.append(_issue("invalid_leaf_level", "Every executable child step must be an L5 leaf.", str(step.get("step_id") or node_id)))
        contract = step.get("collection_contract") or {}
        if contract.get("origin") != "leaf_question_search" or contract.get("bulk_pool_mapping_forbidden") is not True:
            issues.append(_issue("invalid_leaf_collection_contract", "Every L5 step must forbid broad-pool mapping and require leaf search.", str(step.get("step_id") or node_id)))
        queries = [
            str(query).strip()
            for source in step.get("source_plan") or []
            for query in source.get("examples_or_search_queries") or []
            if str(query).strip()
        ]
        if not queries:
            issues.append(_issue("leaf_missing_search_query", "Every L5 leaf must own at least one targeted search query.", str(step.get("step_id") or node_id)))
    return issues


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
        return f"Only sources visible on or before {goal.get('as_of_date') or 'the cutoff'}; preserve visibility proof. Refresh cadence: {cadence}."
    return f"Use the latest available source as of {goal.get('as_of_date') or goal.get('report_date') or 'the report date'}. Refresh cadence: {cadence}."


def _preferred_skill(lens_id: str, unit_id: str) -> str:
    if unit_id == "refutation":
        return "industry-report-analysis"
    return {
        "valuation": "valuation-analysis",
        "esg": "news-event-analysis",
        "technology": "industry-report-analysis",
        "supply": "supply-chain-chokepoint-analysis",
        "demand": "industry-report-analysis",
    }.get(lens_id, "leaf-research-deepseek")


def _skill_for_source(source_type: str, unit_id: str) -> str:
    if "filing" in source_type or "segment economics" in source_type:
        return "financial-statement-analysis"
    if "research" in source_type or "dataset" in source_type or unit_id == "refutation":
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
