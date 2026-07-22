from __future__ import annotations

from copy import deepcopy
from typing import Any


REQUIRED_BOM_QUESTION_NUMBERS = tuple(range(1, 7))
COMPLETE_SEARCH_STATUSES = {"complete", "completed", "ok"}
COMPLETE_PARSER_STATUSES = {
    "complete",
    "completed",
    "gpt_verified_source_parse",
    "ok",
    "verified",
    "verified_with_caveats",
}
VERIFIED_STATUSES = {"complete", "completed", "ok", "verified", "verified_with_caveats"}
SCORE_COMPONENT_QUESTIONS = {
    "chokepoint_strength": (2, 3),
    "future_space": (1,),
    "valuation_odds": (5,),
    "evidence_quality": REQUIRED_BOM_QUESTION_NUMBERS,
    "disconfirming_risk_control": (6,),
    "monitorability": (6,),
    "payoff_convexity": (4, 5),
}
SCORE_EVIDENCE_ROLES = {
    "chokepoint_strength": "supply constraint and supply controller",
    "future_space": "BOM demand pull-through and elasticity",
    "valuation_odds": "as-of valuation and priced-in expectations",
    "evidence_quality": "question-level source and parser coverage",
    "disconfirming_risk_control": "observed refuting evidence and kill test",
    "monitorability": "quantified trigger and observation cadence",
    "payoff_convexity": "financial realization and valuation bridge",
}


def build_bom_readiness(workbench: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Summarize whether every BOM node has completed the six-question evidence loop."""

    rows = workbench.get("bom_question_search_artifacts") or []
    by_node: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        node_id = str(row.get("bom_node_id") or "").strip()
        if node_id:
            by_node.setdefault(node_id, []).append(row)

    readiness: dict[str, dict[str, Any]] = {}
    for node_id, node_rows in by_node.items():
        by_question = {
            int(row.get("question_number") or 0): row
            for row in node_rows
            if str(row.get("question_number") or "").isdigit()
        }
        question_statuses: list[dict[str, Any]] = []
        for question_number in REQUIRED_BOM_QUESTION_NUMBERS:
            row = by_question.get(question_number, {})
            search_complete = _normalized(row.get("search_execution_status")) in COMPLETE_SEARCH_STATUSES
            planning_complete = all(
                bool(row.get(field))
                for field in ("source_universe_plan", "exa_search_plan", "claim_mapping_plan")
            )
            source_ids = _string_list(row.get("source_ids"))
            source_parse_records = [
                record
                for record in row.get("source_parse_records", []) or []
                if isinstance(record, dict)
            ]
            parsed_source_ids = {
                str(record.get("source_id") or "").strip()
                for record in source_parse_records
                if _normalized(record.get("parser_status")) in COMPLETE_PARSER_STATUSES
                and _normalized(record.get("gpt_verification_status"))
                in (VERIFIED_STATUSES | {"needs_review", "rejected"})
            }
            strengthening_source_ids = {
                str(record.get("source_id") or "").strip()
                for record in source_parse_records
                if _normalized(record.get("parser_status")) in COMPLETE_PARSER_STATUSES
                and _normalized(record.get("gpt_verification_status")) in VERIFIED_STATUSES
                and record.get("allowed_to_strengthen_conclusion") is True
            }
            parser_complete = (
                _normalized(row.get("parser_status")) in COMPLETE_PARSER_STATUSES
                and bool(source_ids)
                and set(source_ids).issubset(parsed_source_ids)
            )
            evidence_summary = _string_list(row.get("evidence_summary"))
            refuting_source_ids = _string_list(row.get("refuting_source_ids"))
            refutation_summary = _string_list(row.get("refutation_evidence_summary"))
            evidence_complete = bool(source_ids and evidence_summary and strengthening_source_ids)
            refutation_complete = question_number != 6 or bool(
                refuting_source_ids
                and refutation_summary
                and set(refuting_source_ids).issubset(strengthening_source_ids)
            )
            complete = (
                planning_complete
                and search_complete
                and parser_complete
                and evidence_complete
                and refutation_complete
            )
            question_statuses.append(
                {
                    "question_number": question_number,
                    "artifact_id": str(row.get("artifact_id") or ""),
                    "planning_complete": planning_complete,
                    "search_complete": search_complete,
                    "parser_complete": parser_complete,
                    "evidence_complete": evidence_complete,
                    "refutation_complete": refutation_complete,
                    "complete": complete,
                    "source_count": len(source_ids),
                    "parsed_source_count": len(parsed_source_ids),
                    "source_ids": source_ids,
                }
            )

        completed_count = sum(1 for item in question_statuses if item["complete"])
        readiness[node_id] = {
            "bom_node_id": node_id,
            "bom_node": str(node_rows[0].get("bom_node") or node_id),
            "required_question_count": len(REQUIRED_BOM_QUESTION_NUMBERS),
            "completed_question_count": completed_count,
            "complete": completed_count == len(REQUIRED_BOM_QUESTION_NUMBERS),
            "refutation_complete": question_statuses[-1]["complete"],
            "question_statuses": question_statuses,
        }
    return readiness


def target_research_gate_reasons(
    target: dict[str, Any],
    readiness_by_node: dict[str, dict[str, Any]],
) -> list[str]:
    """Return evidence-completion reasons that cap a target below actionable_long."""

    reasons: list[str] = []
    node_id = str(target.get("thesis_node_id") or "").strip()
    readiness = readiness_by_node.get(node_id)
    if not node_id or readiness is None:
        reasons.append("missing_canonical_bom_mapping")
    else:
        if not readiness.get("complete"):
            completed = int(readiness.get("completed_question_count", 0) or 0)
            required = int(readiness.get("required_question_count", 6) or 6)
            reasons.append(f"bom_six_question_incomplete:{completed}/{required}")
        if not readiness.get("refutation_complete"):
            reasons.append("refutation_evidence_unverified")

    valuation_status = _normalized(target.get("valuation_status"))
    if valuation_status not in VERIFIED_STATUSES:
        reasons.append("valuation_unverified")

    exposure_status = _normalized(target.get("company_exposure_status"))
    if exposure_status not in VERIFIED_STATUSES:
        reasons.append("company_exposure_unverified")

    return list(dict.fromkeys(reasons))


def apply_target_research_gates(
    targets: list[dict[str, Any]],
    workbench: dict[str, Any],
) -> list[dict[str, Any]]:
    """Cap action states from the persisted BOM completion and valuation evidence."""

    gate_required = bool(workbench.get("bom_question_search_artifacts")) or any(
        bool(target.get("research_gate_required") or target.get("thesis_node_id"))
        for target in targets
        if isinstance(target, dict)
    )
    if not gate_required:
        return [deepcopy(target) for target in targets]

    readiness_by_node = build_bom_readiness(workbench)
    gated_targets: list[dict[str, Any]] = []
    for raw_target in targets:
        target = deepcopy(raw_target)
        score = deepcopy(target.get("score")) if isinstance(target.get("score"), dict) else {}
        candidate_state = str(
            target.get("candidate_action_state")
            or target.get("action_state")
            or score.get("action_state")
            or "no_action"
        )
        scored_state = str(
            target.get("action_state")
            or score.get("action_state")
            or candidate_state
        )
        reasons = target_research_gate_reasons(target, readiness_by_node)
        final_state = scored_state
        if reasons and scored_state == "actionable_long":
            final_state = "watch_only"
        if "missing_canonical_bom_mapping" in reasons:
            final_state = "no_action"

        node_id = str(target.get("thesis_node_id") or "")
        node_readiness = readiness_by_node.get(node_id, {})
        target["candidate_action_state"] = candidate_state
        target["action_state"] = final_state
        target["research_gate"] = {
            "passed": not reasons,
            "gate_reasons": reasons,
            "bom_node_id": node_id,
            "completed_questions": int(node_readiness.get("completed_question_count", 0) or 0),
            "required_questions": int(node_readiness.get("required_question_count", 6) or 6),
            "valuation_status": str(target.get("valuation_status") or "missing"),
            "refutation_status": "verified" if node_readiness.get("refutation_complete") else "unverified",
        }
        target["research_gate_required"] = True
        target["bom_research_complete"] = bool(node_readiness.get("complete"))
        target["refutation_status"] = target["research_gate"]["refutation_status"]
        if score:
            score["candidate_action_state"] = candidate_state
            score["action_state"] = final_state
            score["gate_reasons"] = list(dict.fromkeys([*(score.get("gate_reasons") or []), *reasons]))
            target["score"] = score
        gated_targets.append(target)
    return gated_targets


def validate_bom_research_decision_gates(
    workbench: dict[str, Any],
    targets: list[dict[str, Any]],
) -> dict[str, Any]:
    """Reject investable conclusions that outrun the persisted BOM research."""

    artifacts = workbench.get("bom_question_search_artifacts") or []
    gate_required = bool(artifacts) or any(
        bool(target.get("research_gate_required") or target.get("thesis_node_id"))
        for target in targets
        if isinstance(target, dict)
    )
    if not gate_required:
        return {
            "ok": True,
            "summary": {"bom_nodes": 0, "targets": len(targets), "gate_required": False},
            "issues": [],
        }

    issues: list[dict[str, str]] = []
    readiness_by_node = build_bom_readiness(workbench)
    for target in targets:
        if not isinstance(target, dict):
            continue
        ticker = str(target.get("ticker") or target.get("name") or "unknown_target")
        reasons = target_research_gate_reasons(target, readiness_by_node)
        action_state = str(
            target.get("action_state")
            or (target.get("score") or {}).get("action_state")
            or "no_action"
        )
        gate = target.get("research_gate") if isinstance(target.get("research_gate"), dict) else None
        if gate is None:
            _issue(
                issues,
                "error",
                "target_missing_research_gate",
                f"{ticker} must persist the BOM, refutation, and valuation research gate",
            )
        else:
            recorded_reasons = {str(item) for item in gate.get("gate_reasons", []) or []}
            missing_reasons = set(reasons) - recorded_reasons
            if missing_reasons:
                _issue(
                    issues,
                    "error",
                    "target_research_gate_drift",
                    f"{ticker} omits gate reasons: {', '.join(sorted(missing_reasons))}",
                )
            expected_passed = not reasons
            if bool(gate.get("passed")) != expected_passed:
                _issue(
                    issues,
                    "error",
                    "target_research_gate_pass_mismatch",
                    f"{ticker} research_gate.passed does not match persisted evidence",
                )
        if action_state == "actionable_long" and reasons:
            _issue(
                issues,
                "error",
                "actionable_target_failed_research_gate",
                f"{ticker} is actionable_long despite: {', '.join(reasons)}",
            )

    for node_id, readiness in readiness_by_node.items():
        for question in readiness.get("question_statuses", []):
            if question.get("complete"):
                continue
            question_number = question.get("question_number")
            _issue(
                issues,
                "warning",
                "bom_question_research_incomplete",
                f"{node_id} question {question_number} has not completed search, parsing, and evidence checks",
            )

    return {
        "ok": not any(issue["severity"] == "error" for issue in issues),
        "summary": {
            "bom_nodes": len(readiness_by_node),
            "complete_bom_nodes": sum(1 for row in readiness_by_node.values() if row.get("complete")),
            "targets": len(targets),
            "gate_required": True,
        },
        "issues": issues,
    }


def build_bom_completion_scoring_inputs(
    targets: list[dict[str, Any]],
    workbench: dict[str, Any],
) -> list[dict[str, Any]]:
    """Build conservative score inputs from persisted BOM completion, not ticker presets."""

    readiness_by_node = build_bom_readiness(workbench)
    output: list[dict[str, Any]] = []
    for raw_target in targets:
        target = deepcopy(raw_target)
        node_id = str(target.get("thesis_node_id") or "")
        readiness = readiness_by_node.get(
            node_id,
            {
                "bom_node_id": "",
                "completed_question_count": 0,
                "complete": False,
                "refutation_complete": False,
                "question_statuses": [],
            },
        )
        question_by_number = {
            int(row.get("question_number") or 0): row
            for row in readiness.get("question_statuses", [])
        }
        question_complete = lambda number: bool(question_by_number.get(number, {}).get("complete"))
        chokepoint_count = sum(1 for number in (2, 3) if question_complete(number))
        financial_count = sum(1 for number in (4, 5) if question_complete(number))
        components = {
            "chokepoint_strength": 4.0 if chokepoint_count == 2 else 2.5 if chokepoint_count == 1 else 1.5,
            "future_space": 4.0 if question_complete(1) else 1.5,
            "valuation_odds": 1.5,
            "evidence_quality": round(1.0 + (int(readiness.get("completed_question_count", 0)) / 6.0) * 3.0, 3),
            "disconfirming_risk_control": 4.0 if question_complete(6) else 1.0,
            "monitorability": 3.5 if question_complete(6) else 1.5,
            "payoff_convexity": 3.5 if financial_count == 2 else 2.5 if financial_count == 1 else 1.5,
        }
        valuation_status = str(target.get("valuation_status") or "incomplete")
        target["valuation_status"] = valuation_status
        target["company_exposure_status"] = str(
            target.get("company_exposure_status")
            or "unverified"
        )
        target["research_gate_required"] = True
        target["bom_research_complete"] = bool(readiness.get("complete"))
        target["refutation_status"] = "verified" if readiness.get("refutation_complete") else "unverified"
        target["score_subcomponents"] = _completion_score_subcomponents(
            target,
            question_by_number,
            components,
            valuation_status,
        )
        target.update(components)
        target["demand_visibility"] = components["future_space"]
        target["irreplaceability"] = components["chokepoint_strength"]
        target["market_underpricing"] = components["valuation_odds"]
        target.setdefault("valuation_tolerance", 2.0)
        target.setdefault("downside_fragility", 3.0)
        target.setdefault("catalyst_proximity", 3.0)
        target.setdefault(
            "thesis_kill_tests",
            [
                {
                    "test": "核心订单、backlog、ASP 或客户资格是否在后续披露中恶化。",
                    "evidence_needed": "季度财报、订单/backlog、毛利、ASP、客户资格或 capex 指引。",
                    "trigger_metric": "当前 BOM 的订单/backlog、ASP、毛利率或客户资格",
                    "threshold": "连续两个披露期弱于管理层指引或出现明确下修",
                    "observation_frequency": "季度",
                    "downgrade_action": "若证据恶化，降为 watch_only 或 no_action。",
                    "source_plan": deepcopy(target.get("evidence_ids") or []),
                }
            ],
        )
        output.append(target)
    return output


def _completion_score_subcomponents(
    target: dict[str, Any],
    question_by_number: dict[int, dict[str, Any]],
    components: dict[str, float],
    valuation_status: str,
) -> dict[str, list[dict[str, Any]]]:
    output: dict[str, list[dict[str, Any]]] = {}
    for component, question_numbers in SCORE_COMPONENT_QUESTIONS.items():
        question_rows = [question_by_number.get(number, {}) for number in question_numbers]
        valuation_gap = component == "valuation_odds" and _normalized(valuation_status) not in VERIFIED_STATUSES
        complete = (
            not valuation_gap
            and len(question_rows) == len(question_numbers)
            and all(row.get("complete") for row in question_rows)
        )
        evidence_ids = list(
            dict.fromkeys(
                source_id
                for row in question_rows
                for source_id in _string_list(row.get("source_ids"))
            )
        )
        gap_reason = (
            "缺少研究截面时点的同口径估值、盈利预期和隐含增长重建。"
            if valuation_gap
            else f"对应 BOM 子问未完成主动搜索、来源解析或反证验证：{', '.join(map(str, question_numbers))}。"
        )
        output[component] = [
            {
                "name": f"{component}_{target.get('thesis_node_id') or 'unmapped'}",
                "score": components[component],
                "weight": 1.0,
                "evidence_ids": evidence_ids if complete else [],
                "review_ids": [],
                "evidence_role": SCORE_EVIDENCE_ROLES[component],
                "rationale": (
                    f"该分项只使用 {target.get('thesis_node') or target.get('thesis_node_id')} 对应子问的已完成证据。"
                    if complete
                    else gap_reason
                ),
                "status": "verified_with_caveats" if complete else "gap",
                "gap_reason": "" if complete else gap_reason,
            }
        ]
    return output


def _normalized(value: Any) -> str:
    return str(value or "").strip().lower()


def _string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def _issue(issues: list[dict[str, str]], severity: str, code: str, message: str) -> None:
    issues.append({"severity": severity, "code": code, "message": message})
