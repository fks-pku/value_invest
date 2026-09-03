from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any

from value_invest_research.domain.leaf_research_tasks import (
    classify_task_family,
    research_step_id,
    selected_skill_for_task_family,
)
from value_invest_research.domain.question_architecture import QuestionArchitecture, QuestionNode


RESEARCH_STEP_EVENT_TYPES = {
    "collection_started",
    "evidence_attached",
    "answer_recorded",
    "gate_evaluated",
    "step_blocked",
    "step_reopened",
}

EVENT_STATUS = {
    "collection_started": "in_progress",
    "evidence_attached": "in_progress",
    "answer_recorded": "review_pending",
    "gate_evaluated": "completed",
    "step_blocked": "blocked",
    "step_reopened": "in_progress",
}


@dataclass(frozen=True)
class ResearchPlanStep:
    """One evidence-gated L3 rollup linked to its dynamic child plan."""

    step_id: str
    stage_id: str
    sequence: int
    question_node_id: str
    question: str
    decision_use: str
    depends_on_step_ids: list[str] = field(default_factory=list)
    required_materials: list[str] = field(default_factory=list)
    source_universe_plan: dict[str, Any] = field(default_factory=dict)
    source_plan: list[dict[str, Any]] = field(default_factory=list)
    minimum_evidence_gate: dict[str, Any] = field(default_factory=dict)
    refuting_source_plan: list[str] = field(default_factory=list)
    freshness_requirement: str = ""
    preferred_specialty_skill: str = ""
    execution_mode: str = "child_plan_rollup"
    child_plan_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "stage_id": self.stage_id,
            "sequence": self.sequence,
            "question_node_id": self.question_node_id,
            "question": self.question,
            "decision_use": self.decision_use,
            "depends_on_step_ids": list(self.depends_on_step_ids),
            "required_materials": list(self.required_materials),
            "source_universe_plan": dict(self.source_universe_plan),
            "source_plan": [dict(item) for item in self.source_plan],
            "minimum_evidence_gate": dict(self.minimum_evidence_gate),
            "refuting_source_plan": list(self.refuting_source_plan),
            "freshness_requirement": self.freshness_requirement,
            "preferred_specialty_skill": self.preferred_specialty_skill,
            "execution_mode": self.execution_mode,
            "child_plan_path": self.child_plan_path,
            "answer_contract": {
                "required_fields": [
                    "answer",
                    "supporting_findings",
                    "refuting_findings",
                    "gaps",
                    "next_actions",
                ],
                "rule": "Separate facts, inference, judgment, refutation, gaps, and next validation.",
            },
            "traceability_contract": {
                "required_references": [
                    "source_ids",
                    "source_extraction_ids",
                    "source_review_ids",
                ],
                "event_ledger": "research_step_events.jsonl",
            },
            "initial_status": "pending",
        }


@dataclass(frozen=True)
class ResearchPlan:
    """Immutable execution plan connecting questions to evidence and answers."""

    plan_id: str
    research_goal: dict[str, Any]
    playbook_id: str
    planner_rationale: str
    steps: list[ResearchPlanStep]
    schema_version: str = "4.0"

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "plan_id": self.plan_id,
            "research_goal": dict(self.research_goal),
            "question_architecture": {
                "artifact_path": "qa_tree.json",
                "playbook_id": self.playbook_id,
                "planner_rationale": self.planner_rationale,
            },
            "execution_policy": {
                "question_tree": "adaptive_depth_max_5",
                "initial_depth": "L3_only",
                "within_stage": "parallel_when_independent",
                "between_stages": "dependency_gated",
                "event_log": "append_only",
                "completion": "all_required_l3_child_plans_complete",
                "material_collection": "current_terminal_question_only",
                "branch_creation": "only_after_failed_answerability_gate",
                "broad_material_pool": "candidate_only_not_completion_evidence",
            },
            "l3_plan_index_path": "l3_research_plans/index.json",
            "steps": [step.to_dict() for step in self.steps],
        }


def build_research_plan(
    architecture: QuestionArchitecture,
    *,
    source_universe: dict[str, Any] | None = None,
) -> ResearchPlan:
    """Convert initial L3 questions into ordered child-plan rollups."""
    leaves = [node for node in architecture.nodes if not node.next_question_ids]
    nodes_by_id = {node.id: node for node in architecture.nodes}
    stage_step_ids: dict[str, list[str]] = {}
    steps: list[ResearchPlanStep] = []

    for sequence, node in enumerate(leaves, start=1):
        stage_id = _stage_id(node.id)
        previous_stage = _previous_stage_id(stage_id)
        parent = nodes_by_id.get(node.parent_id)
        step = _build_step(
            architecture,
            node,
            parent,
            sequence=sequence,
            depends_on_step_ids=stage_step_ids.get(previous_stage, []),
            source_universe=source_universe or {},
        )
        steps.append(step)
        stage_step_ids.setdefault(stage_id, []).append(step.step_id)

    identity = {
        "research_goal": architecture.research_goal.to_dict(),
        "playbook_id": architecture.playbook.playbook_id,
        "steps": [step.to_dict() for step in steps],
    }
    digest = hashlib.sha256(
        json.dumps(identity, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]
    return ResearchPlan(
        plan_id=f"rp_{digest}",
        research_goal=architecture.research_goal.to_dict(),
        playbook_id=architecture.playbook.playbook_id,
        planner_rationale=architecture.planner_rationale,
        steps=steps,
    )


def enrich_question_architecture(
    architecture: QuestionArchitecture,
    plan: ResearchPlan,
) -> dict[str, Any]:
    """Bind QA leaves to their executable plan steps without changing questions."""
    payload = architecture.to_dict()
    steps_by_node = {step.question_node_id: step.to_dict() for step in plan.steps}
    for node in payload.get("nodes", []):
        step = steps_by_node.get(str(node.get("id") or ""))
        if step is None:
            continue
        node.update(
            {
                "research_step_id": step["step_id"],
                "materiality": step["decision_use"],
                "minimum_evidence_gate": step["minimum_evidence_gate"],
                "source_plan": step["source_plan"],
                "refuting_source_plan": step["refuting_source_plan"],
                "freshness_requirement": step["freshness_requirement"],
                "execution_mode": step["execution_mode"],
                "child_plan_path": step["child_plan_path"],
            }
        )
    payload["research_plan_id"] = plan.plan_id
    payload["research_plan_path"] = "research_plan.json"
    payload["l3_plan_index_path"] = "l3_research_plans/index.json"
    return payload


def prepare_research_step_event(
    plan: dict[str, Any],
    event: dict[str, Any],
    *,
    recorded_at: str,
) -> dict[str, Any]:
    """Normalize one append-only event and give it a deterministic event id."""
    event_type = str(event.get("event_type") or "").strip()
    step_id = str(event.get("step_id") or "").strip()
    normalized = {
        "schema_version": "1.0",
        "plan_id": str(plan.get("plan_id") or ""),
        "step_id": step_id,
        "event_type": event_type,
        "recorded_at": str(event.get("recorded_at") or recorded_at),
        "answer": str(event.get("answer") or "").strip(),
        "search_run_id": str(event.get("search_run_id") or "").strip(),
        "source_ids": _text_list(event.get("source_ids")),
        "source_extraction_ids": _text_list(event.get("source_extraction_ids")),
        "source_review_ids": _text_list(event.get("source_review_ids")),
        "supporting_findings": _text_list(event.get("supporting_findings")),
        "refuting_findings": _text_list(event.get("refuting_findings")),
        "gaps": _text_list(event.get("gaps")),
        "next_actions": _text_list(event.get("next_actions")),
        "evidence_gate": _normalize_gate(event.get("evidence_gate")),
    }
    event_identity = json.dumps(normalized, ensure_ascii=False, sort_keys=True)
    normalized["event_id"] = str(event.get("event_id") or "") or (
        "rse_" + hashlib.sha256(event_identity.encode("utf-8")).hexdigest()[:16]
    )
    return normalized


def validate_research_step_event(
    plan: dict[str, Any],
    prior_events: list[dict[str, Any]],
    event: dict[str, Any],
) -> list[dict[str, str]]:
    """Validate a prospective event, including completion dependencies."""
    issues = _event_shape_issues(plan, event)
    if issues:
        return issues
    result = validate_research_plan_execution(plan, [*prior_events, event])
    event_step_id = str(event.get("step_id") or "")
    return [
        issue
        for issue in result["issues"]
        if issue.get("step_id") in {"", event_step_id}
        and issue.get("severity") == "error"
    ]


def validate_research_plan_execution(
    plan: dict[str, Any],
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate plan structure and project the latest auditable state per step."""
    issues = _plan_shape_issues(plan)
    active_plan_id = str(plan.get("plan_id") or "")
    steps = [item for item in plan.get("steps", []) if isinstance(item, dict)]
    step_ids = {str(step.get("step_id") or "") for step in steps}
    active_events: list[dict[str, Any]] = []
    for event in events:
        event_plan_id = str(event.get("plan_id") or "")
        if not event_plan_id:
            issues.append(
                _issue(
                    "missing_event_plan_id",
                    "Research step event must identify its immutable plan version.",
                    str(event.get("step_id") or ""),
                )
            )
            continue
        if event_plan_id != active_plan_id:
            continue
        active_events.append(event)
        issues.extend(_event_shape_issues(plan, event))

    states = {step_id: _empty_step_state(step_id) for step_id in step_ids if step_id}
    event_counts = {step_id: 0 for step_id in states}
    for event in active_events:
        step_id = str(event.get("step_id") or "")
        if step_id not in states:
            continue
        states[step_id] = _apply_event(states[step_id], event)
        event_counts[step_id] += 1

    for step in steps:
        step_id = str(step.get("step_id") or "")
        if not step_id or step_id not in states:
            continue
        state = states[step_id]
        if state["status"] == "completed":
            issues.extend(_completion_issues(step, state, states))
        if state["status"] == "blocked":
            if not state["gaps"]:
                issues.append(_issue("blocked_step_missing_gap", "Blocked step must record a concrete gap.", step_id))
            if not state["next_actions"]:
                issues.append(_issue("blocked_step_missing_next_action", "Blocked step must record the next validation action.", step_id))

    ordered_states = []
    for step in sorted(steps, key=lambda item: int(item.get("sequence", 0) or 0)):
        step_id = str(step.get("step_id") or "")
        if step_id in states:
            ordered_states.append({**states[step_id], "event_count": event_counts[step_id]})
    counts = {
        status: sum(1 for state in ordered_states if state["status"] == status)
        for status in ("pending", "in_progress", "review_pending", "blocked", "completed")
    }
    if counts["completed"] == len(ordered_states) and ordered_states:
        overall_status = "completed"
    elif counts["blocked"]:
        overall_status = "blocked"
    elif counts["in_progress"] or counts["review_pending"] or counts["completed"]:
        overall_status = "in_progress"
    else:
        overall_status = "planned"
    return {
        "ok": not any(issue.get("severity") == "error" for issue in issues),
        "issues": issues,
        "summary": {
            "plan_id": str(plan.get("plan_id") or ""),
            "status": overall_status,
            "steps": len(ordered_states),
            **counts,
            "events": len(active_events),
            "historical_plan_events": len(events) - len(active_events),
        },
        "step_states": ordered_states,
    }


def _build_step(
    architecture: QuestionArchitecture,
    node: QuestionNode,
    parent: QuestionNode | None,
    *,
    sequence: int,
    depends_on_step_ids: list[str],
    source_universe: dict[str, Any],
) -> ResearchPlanStep:
    node_payload = node.to_dict()
    parent_payload = parent.to_dict() if parent is not None else {}
    task_family = classify_task_family(node_payload, parent_payload)
    refute_rule = node.refute_evidence or "Find boundary evidence that would reverse or cap the answer."
    return ResearchPlanStep(
        step_id=research_step_id(node.id),
        stage_id=_stage_id(node.id),
        sequence=sequence,
        question_node_id=node.id,
        question=node.question,
        decision_use=node.decision_use or node.investment_relevance,
        depends_on_step_ids=list(depends_on_step_ids),
        required_materials=list(node.required_materials),
        source_universe_plan={},
        source_plan=[],
        minimum_evidence_gate={
            "rule": (
                "The L3 rollup completes when its active question is answerable, "
                "or when every required descendant created by a failed gate passes."
            ),
            "all_mandatory_leaf_steps_required": True,
            "direct_parent_evidence_forbidden": True,
        },
        refuting_source_plan=[f"Search for primary or independent evidence that would establish: {refute_rule}"],
        freshness_requirement=_freshness_requirement(architecture),
        preferred_specialty_skill=node.preferred_specialty_skill or selected_skill_for_task_family(task_family),
        execution_mode="child_plan_rollup",
        child_plan_path=f"l3_research_plans/{node.id}/research_plan.json",
    )


def _freshness_requirement(architecture: QuestionArchitecture) -> str:
    goal = architecture.research_goal
    if goal.run_mode == "historical_backtest":
        cutoff = goal.as_of_date or "the as-of date"
        return f"Only sources visible on or before {cutoff}; preserve historical baseline and visibility proof."
    return "Use the latest filing/quarter or relevant event window and preserve publication time."


def _stage_id(node_id: str) -> str:
    return str(node_id).split(".", 1)[0]


def _previous_stage_id(stage_id: str) -> str:
    if len(stage_id) == 2 and stage_id[0].upper() == "Q" and stage_id[1].isdigit():
        number = int(stage_id[1])
        return f"Q{number - 1}" if number > 1 else ""
    return ""


def _plan_shape_issues(plan: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if not str(plan.get("plan_id") or ""):
        issues.append(_issue("missing_plan_id", "Research plan must have a stable plan_id."))
    steps = plan.get("steps")
    if not isinstance(steps, list) or not steps:
        return [*issues, _issue("missing_plan_steps", "Research plan must contain executable steps.")]
    seen: set[str] = set()
    all_ids = {str(step.get("step_id") or "") for step in steps if isinstance(step, dict)}
    for step in steps:
        if not isinstance(step, dict):
            issues.append(_issue("invalid_plan_step", "Every research plan step must be an object."))
            continue
        step_id = str(step.get("step_id") or "")
        if not step_id:
            issues.append(_issue("missing_step_id", "Every research plan step must have a stable step_id."))
            continue
        if step_id in seen:
            issues.append(_issue("duplicate_step_id", "Research plan step ids must be unique.", step_id))
        seen.add(step_id)
        for field_name in ("question_node_id", "question", "decision_use", "freshness_requirement"):
            if not step.get(field_name):
                issues.append(_issue(f"missing_step_{field_name}", f"Step must record {field_name}.", step_id))
        execution_mode = str(step.get("execution_mode") or "direct_evidence_step")
        if execution_mode == "child_plan_rollup" and not step.get("child_plan_path"):
            issues.append(_issue("missing_child_plan_path", "L3 rollup step must reference its independent child plan.", step_id))
        if execution_mode not in {"child_plan_rollup", "direct_evidence_step"}:
            issues.append(_issue("invalid_step_execution_mode", f"Unsupported execution_mode={execution_mode!r}.", step_id))
        if not step.get("source_plan") and execution_mode != "child_plan_rollup":
            issues.append(_issue("missing_step_source_plan", "Step must have a question-specific source plan.", step_id))
        elif step.get("source_plan") and any(
            not isinstance(source, dict)
            or not all(
                field_name in source
                for field_name in (
                    "source_bucket",
                    "source_type",
                    "examples_or_search_queries",
                    "why_needed",
                    "expected_fields",
                    "preferred_skill",
                    "deepseek_allowed",
                )
            )
            for source in step.get("source_plan", [])
        ):
            issues.append(_issue("incomplete_step_source_plan", "Every source-plan row must satisfy the source-planner contract.", step_id))
        if not isinstance(step.get("source_universe_plan"), dict):
            issues.append(_issue("missing_step_source_universe", "Step must record source-universe resolution.", step_id))
        if not step.get("minimum_evidence_gate"):
            issues.append(_issue("missing_step_evidence_gate", "Step must declare its minimum evidence gate.", step_id))
        if not step.get("refuting_source_plan"):
            issues.append(_issue("missing_step_refuting_plan", "Step must plan a refuting or boundary search.", step_id))
        if not step.get("answer_contract"):
            issues.append(_issue("missing_step_answer_contract", "Step must declare its answer contract.", step_id))
        if not step.get("traceability_contract"):
            issues.append(_issue("missing_step_traceability_contract", "Step must declare its traceability contract.", step_id))
        for dependency in step.get("depends_on_step_ids", []) or []:
            if dependency not in all_ids:
                issues.append(_issue("unknown_step_dependency", f"Unknown dependency {dependency}.", step_id))
            if dependency == step_id:
                issues.append(_issue("self_step_dependency", "A step cannot depend on itself.", step_id))
    for step_id in _dependency_cycle_ids(steps):
        issues.append(_issue("cyclic_step_dependency", "Research plan dependencies must be acyclic.", step_id))
    return issues


def _event_shape_issues(plan: dict[str, Any], event: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    step_id = str(event.get("step_id") or "")
    known_steps = {
        str(step.get("step_id") or "")
        for step in plan.get("steps", [])
        if isinstance(step, dict)
    }
    if str(event.get("plan_id") or "") != str(plan.get("plan_id") or ""):
        issues.append(_issue("event_plan_mismatch", "Event plan_id does not match the active research plan.", step_id))
    if step_id not in known_steps:
        issues.append(_issue("unknown_event_step", "Event step_id is not present in the research plan.", step_id))
    event_type = str(event.get("event_type") or "")
    if event_type not in RESEARCH_STEP_EVENT_TYPES:
        issues.append(_issue("invalid_step_event_type", f"Unsupported event_type {event_type}.", step_id))
    if not str(event.get("event_id") or ""):
        issues.append(_issue("missing_step_event_id", "Research step event must have an event_id.", step_id))
    if not str(event.get("recorded_at") or ""):
        issues.append(_issue("missing_step_event_time", "Research step event must record recorded_at.", step_id))
    if event_type == "evidence_attached" and not any(
        event.get(field_name)
        for field_name in ("source_ids", "source_extraction_ids", "source_review_ids")
    ):
        issues.append(_issue("evidence_event_missing_references", "Evidence event must attach traceable references.", step_id))
    step = next(
        (
            row
            for row in plan.get("steps", [])
            if str(row.get("step_id") or "") == step_id
        ),
        {},
    )
    if (
        event_type == "evidence_attached"
        and (step.get("collection_contract") or {}).get("origin")
        == "active_question_search"
        and not str(event.get("search_run_id") or "").strip()
    ):
        issues.append(
            _issue(
                "active_question_evidence_missing_search_run",
                "Evidence must reference the active-question search run that collected it.",
                step_id,
            )
        )
    if event_type == "answer_recorded" and not str(event.get("answer") or "").strip():
        issues.append(_issue("answer_event_missing_answer", "Answer event must contain the step answer.", step_id))
    if event_type == "gate_evaluated" and not isinstance(event.get("evidence_gate"), dict):
        issues.append(_issue("gate_event_missing_result", "Gate event must contain evidence_gate.", step_id))
    if event_type == "step_blocked":
        if not event.get("gaps"):
            issues.append(_issue("blocked_event_missing_gap", "Blocked event must state the evidence gap.", step_id))
        if not event.get("next_actions"):
            issues.append(_issue("blocked_event_missing_next_action", "Blocked event must state the next action.", step_id))
    return issues


def _completion_issues(
    step: dict[str, Any],
    state: dict[str, Any],
    all_states: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    step_id = str(step.get("step_id") or "")
    issues: list[dict[str, str]] = []
    if str(step.get("execution_mode") or "direct_evidence_step") == "child_plan_rollup":
        issues.append(
            _issue(
                "l3_rollup_cannot_complete_from_parent_events",
                "An L3 rollup completes only from all mandatory child leaf steps, not direct parent evidence events.",
                step_id,
            )
        )
        return issues
    required = {
        "answer": bool(state["answer"]),
        "source_ids": bool(state["source_ids"]),
        "source_extraction_ids": bool(state["source_extraction_ids"]),
        "source_review_ids": bool(state["source_review_ids"]),
        "findings": bool(state["supporting_findings"] or state["refuting_findings"]),
        "refuting_findings": bool(state["refuting_findings"]),
        "passed_evidence_gate": bool(state["evidence_gate"].get("passed")),
    }
    if (step.get("collection_contract") or {}).get("origin") == "active_question_search":
        required["search_run_id"] = bool(state["search_run_id"])
    for field_name, present in required.items():
        if not present:
            issues.append(_issue(f"completed_step_missing_{field_name}", f"Completed step is missing {field_name}.", step_id))
    for dependency in step.get("depends_on_step_ids", []) or []:
        if all_states.get(dependency, {}).get("status") != "completed":
            issues.append(_issue("completed_step_dependency_open", f"Dependency {dependency} is not completed.", step_id))
    return issues


def _empty_step_state(step_id: str) -> dict[str, Any]:
    return {
        "step_id": step_id,
        "status": "pending",
        "answer": "",
        "search_run_id": "",
        "source_ids": [],
        "source_extraction_ids": [],
        "source_review_ids": [],
        "supporting_findings": [],
        "refuting_findings": [],
        "gaps": [],
        "next_actions": [],
        "evidence_gate": {"passed": False, "reasons": []},
        "latest_event_id": "",
        "latest_recorded_at": "",
    }


def _apply_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    updated = dict(state)
    for field_name in (
        "source_ids",
        "source_extraction_ids",
        "source_review_ids",
        "supporting_findings",
        "refuting_findings",
        "gaps",
        "next_actions",
    ):
        updated[field_name] = _ordered_union(updated[field_name], event.get(field_name))
    if str(event.get("answer") or "").strip():
        updated["answer"] = str(event["answer"]).strip()
    if str(event.get("search_run_id") or "").strip():
        updated["search_run_id"] = str(event["search_run_id"]).strip()
    if event.get("event_type") == "gate_evaluated":
        updated["evidence_gate"] = _normalize_gate(event.get("evidence_gate"))
        updated["status"] = "completed" if updated["evidence_gate"]["passed"] else "blocked"
    else:
        updated["status"] = EVENT_STATUS.get(str(event.get("event_type") or ""), updated["status"])
        if event.get("event_type") in {"step_blocked", "step_reopened"}:
            updated["evidence_gate"] = {"passed": False, "reasons": []}
    updated["latest_event_id"] = str(event.get("event_id") or "")
    updated["latest_recorded_at"] = str(event.get("recorded_at") or "")
    return updated


def _normalize_gate(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {"passed": False, "reasons": []}
    return {
        "passed": bool(value.get("passed", False)),
        "reasons": _text_list(value.get("reasons")),
    }


def _dependency_cycle_ids(steps: list[dict[str, Any]]) -> set[str]:
    graph = {
        str(step.get("step_id") or ""): [str(item) for item in step.get("depends_on_step_ids", []) or []]
        for step in steps
        if isinstance(step, dict) and step.get("step_id")
    }
    visiting: set[str] = set()
    stack: list[str] = []
    visited: set[str] = set()
    cycle_ids: set[str] = set()

    def visit(step_id: str) -> None:
        if step_id in visiting:
            cycle_ids.update(stack[stack.index(step_id):])
            return
        if step_id in visited:
            return
        visiting.add(step_id)
        stack.append(step_id)
        for dependency in graph.get(step_id, []):
            if dependency in graph:
                visit(dependency)
        stack.pop()
        visiting.remove(step_id)
        visited.add(step_id)

    for step_id in graph:
        visit(step_id)
    return cycle_ids


def _ordered_union(left: list[Any], right: Any) -> list[str]:
    result = [str(item) for item in left if str(item)]
    for item in _text_list(right):
        if item not in result:
            result.append(item)
    return result


def _text_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def _issue(code: str, message: str, step_id: str = "") -> dict[str, str]:
    return {
        "severity": "error",
        "code": code,
        "message": message,
        "step_id": step_id,
    }
