from __future__ import annotations

from copy import deepcopy
from typing import Any

from value_invest_research.domain.bom_node_playbooks import (
    BomNodePlaybook,
    BomQuestionPlaybook,
    validate_bom_node_playbook,
)


def build_bom_node_research_payload(
    playbook: BomNodePlaybook,
    research_run: dict[str, Any],
) -> dict[str, Any]:
    """Merge a domain playbook with one evidence-backed research run.

    The playbook owns questions and causal stages. The run owns sources,
    observations, gaps, verdicts, and report-period facts.
    """

    validate_bom_node_playbook(playbook)
    _validate_run_identity(playbook, research_run)
    run_questions = {
        str(item.get("question_id") or ""): item
        for item in research_run.get("questions", [])
        if isinstance(item, dict)
    }
    expected_ids = {question.question_id for question in playbook.questions}
    if set(run_questions) != expected_ids:
        missing = sorted(expected_ids - set(run_questions))
        extra = sorted(set(run_questions) - expected_ids)
        raise ValueError(
            f"{playbook.node_id} research run question drift; "
            f"missing={missing}, extra={extra}"
        )

    rows = [
        _build_question_row(question, run_questions[question.question_id])
        for question in playbook.questions
    ]
    return {
        "node": {
            "id": playbook.node_id,
            "name": playbook.public_name,
            "plain": playbook.description,
            "exclusions": list(playbook.exclusions),
            "players": "、".join(playbook.representative_companies),
            "receives": playbook.receives,
            "produces": playbook.produces,
            "suppliesTo": playbook.supplies_to,
            "metrics": "、".join(playbook.financial_validation_metrics),
            "masterEquations": list(playbook.master_equations),
        },
        "questions": rows,
        "run_metadata": deepcopy(research_run.get("run_metadata") or {}),
    }


def _validate_run_identity(playbook: BomNodePlaybook, research_run: dict[str, Any]) -> None:
    node_id = str(research_run.get("node_id") or "")
    if node_id != playbook.node_id:
        raise ValueError(f"Research run node_id={node_id!r} does not match {playbook.node_id!r}")
    if not research_run.get("as_of_date"):
        raise ValueError("Research run must preserve as_of_date")


def _build_question_row(
    question: BomQuestionPlaybook,
    run_question: dict[str, Any],
) -> dict[str, Any]:
    run_stages = {
        str(item.get("stage_id") or ""): item
        for item in run_question.get("stages", [])
        if isinstance(item, dict)
    }
    expected_stage_ids = {stage.stage_id for stage in question.stages}
    if set(run_stages) != expected_stage_ids:
        missing = sorted(expected_stage_ids - set(run_stages))
        extra = sorted(set(run_stages) - expected_stage_ids)
        raise ValueError(
            f"{question.question_id} stage drift; missing={missing}, extra={extra}"
        )

    chain_nodes: list[dict[str, Any]] = []
    future_cards: list[dict[str, Any]] = []
    source_ids: list[str] = []
    for stage in question.stages:
        run_stage = run_stages[stage.stage_id]
        metric = _build_metric(stage, run_stage)
        stage_source_ids = _string_list(run_stage.get("source_ids"))
        metric["sourceIds"] = _dedupe([*metric.get("sourceIds", []), *stage_source_ids])
        source_ids.extend(metric["sourceIds"])
        chain_nodes.append(
            {
                "title": stage.title,
                "question": stage.decision_question,
                "role": stage.role,
                "status": str(run_stage.get("status") or "待验证"),
                "metrics": [metric],
                "sourceIds": metric["sourceIds"],
            }
        )
        future_cards.append(_build_future_card(stage.title, run_stage, metric["sourceIds"]))

    question_source_ids = _dedupe(
        [
            *_string_list(run_question.get("source_ids")),
            *source_ids,
        ]
    )
    search_artifact = deepcopy(run_question.get("search_artifact") or {})
    search_artifact["source_ids"] = _dedupe(
        [*question_source_ids, *_string_list(search_artifact.get("source_ids"))]
    )
    return {
        "question": question.question,
        "answer": str(run_question.get("conclusion") or "当前研究尚未形成可验证结论。"),
        "sourceIds": question_source_ids,
        "model": {
            "name": question.model_name,
            "purpose": question.purpose,
            "formula": question.formula,
            "keyQuestions": [stage.decision_question for stage in question.stages],
            "metricFamilies": [
                f"主指标：{stage.primary_metric}；交叉验证：{'、'.join(stage.cross_check_metrics)}；反证：{stage.refutation_metric}"
                for stage in question.stages
            ],
            "conclusionRule": question.conclusion_rule,
        },
        "metricLogic": str(
            run_question.get("logic_summary")
            or "按领域 playbook 的因果环节逐项检索和验证，不从粗证据池直接生成答案。"
        ),
        "detail": {"reportNarrative": {"chainNodes": chain_nodes}},
        "replaceDefaultMetrics": True,
        "futureCards": future_cards,
        "mechanism": {
            "sustain": str((run_question.get("mechanism") or {}).get("support") or "待补支持机制。"),
            "break": str((run_question.get("mechanism") or {}).get("refute") or "待补反向机制。"),
        },
        "conclusionStrength": str(run_question.get("conclusion_strength") or "待验证"),
        "targetImpact": str(
            run_question.get("target_impact")
            or "本问未完成前不得上调该 BOM 相关标的强度。"
        ),
        "searchArtifact": search_artifact,
    }


def _build_metric(stage: Any, run_stage: dict[str, Any]) -> dict[str, Any]:
    metric = deepcopy(run_stage.get("metric") or {})
    metric.setdefault("type", "主指标")
    metric.setdefault("name", stage.primary_metric)
    metric.setdefault("why", stage.role)
    metric.setdefault(
        "dataRequirement",
        (
            f"主指标：{stage.primary_metric}；交叉验证：{'、'.join(stage.cross_check_metrics)}；"
            f"反证指标：{stage.refutation_metric}。"
        ),
    )
    metric.setdefault("trendKind", "non_time_series")
    metric.setdefault("series", [])
    metric.setdefault("seriesGap", "公开材料没有形成五个以上同口径历史点。")
    metric.setdefault("history", "尚未提取同口径历史数据。")
    metric.setdefault("current", "尚未形成当前截面判断。")
    metric.setdefault("future", "尚未形成对应未来预期。")
    metric.setdefault("quality", "待验证")
    metric["sourceIds"] = _string_list(metric.get("sourceIds") or metric.get("source_ids"))
    metric.pop("source_ids", None)
    return metric


def _build_future_card(
    stage_title: str,
    run_stage: dict[str, Any],
    source_ids: list[str],
) -> dict[str, Any]:
    rows = []
    for raw in run_stage.get("expectation_rows", []) or []:
        if not isinstance(raw, dict):
            continue
        rows.append(
            {
                "entity": str(raw.get("entity") or "待补"),
                "currentPeriod": str(raw.get("current_period") or "待补"),
                "currentActualTime": str(raw.get("current_actual_time") or ""),
                "currentMetric": str(raw.get("current_metric") or ""),
                "guidancePeriod": str(raw.get("guidance_period") or "待补"),
                "guidanceActualTime": str(raw.get("guidance_actual_time") or ""),
                "guidanceMetric": str(raw.get("guidance_metric") or ""),
                "comparability": str(raw.get("comparability") or ""),
                "sourceIds": _string_list(raw.get("source_ids")) or list(source_ids),
            }
        )
    if not rows:
        rows.append(
            {
                "entity": "预期缺口",
                "currentPeriod": "见历史与现状",
                "currentMetric": str((run_stage.get("metric") or {}).get("current") or ""),
                "guidancePeriod": "待补",
                "guidanceMetric": "未找到与本环节严格对齐的未来指引或预测。",
                "comparability": "缺口保留，不用模型先验填充。",
                "sourceIds": list(source_ids),
            }
        )
    return {
        "horizon": stage_title,
        "expectationStatus": str(run_stage.get("expectation_status") or "已检索"),
        "marketExpectation": str(run_stage.get("market_expectation") or "见分实体预期表。"),
        "expectationRows": rows,
        "sourceIds": _dedupe([*source_ids, *[sid for row in rows for sid in row["sourceIds"]]]),
    }


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))
