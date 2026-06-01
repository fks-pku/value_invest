from __future__ import annotations

import hashlib
from typing import Any


INFO_CATEGORIES = ["evidence", "research_report", "message", "opinion"]


def build_leaf_tasks_from_tree(
    qa_tree: dict[str, Any],
    *,
    ticker: str,
    company_name: str,
    completed_node_ids: set[str] | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """Build provider-agnostic leaf research tasks from a QA tree."""
    completed = completed_node_ids or set()
    nodes_by_id = {node.get("id", ""): node for node in qa_tree.get("nodes", [])}
    tasks: list[dict[str, Any]] = []
    for node in qa_tree.get("nodes", []):
        node_id = node.get("id", "")
        if not node_id or node_id in completed or not is_leaf_node(qa_tree, node):
            continue
        parent = nodes_by_id.get(node.get("parent_id", ""), {})
        tasks.append(build_leaf_task(qa_tree, node, parent, ticker, company_name))
        if limit is not None and len(tasks) >= limit:
            break
    return tasks


def build_leaf_task(
    qa_tree: dict[str, Any],
    node: dict[str, Any],
    parent: dict[str, Any],
    ticker: str,
    company_name: str,
) -> dict[str, Any]:
    node_id = node.get("id", "")
    synthesis = node.get("synthesis", {}) or {}
    professional = node.get("professional_answer", {}) or {}
    gaps = _text_list(professional.get("gaps") or synthesis.get("gaps"))
    required = (
        _text_list(node.get("required_evidence"))
        or _text_list(node.get("information_collection", {}).get("evidence", {}).get("acceptance_criteria"))
        or gaps[:3]
    )
    question = node.get("question", "")
    parent_question = parent.get("question", "")
    task_family = classify_task_family(node, parent)
    selected_skill = selected_skill_for_task_family(task_family)
    source_search_plan = source_search_plan_for_task(node, parent, task_family)
    extraction_schema = extraction_schema_for_task(task_family)
    materiality = materiality_statement(question, parent_question, task_family)
    return {
        "schema_version": "1.0",
        "task_id": _stable_task_id(ticker, node_id),
        "ticker": ticker,
        "company_name": company_name,
        "node_id": node_id,
        "section_id": node.get("section_id", ""),
        "question": question,
        "parent_id": parent.get("id", ""),
        "parent_question": parent_question,
        "framework_context": framework_context(qa_tree, node, parent),
        "materiality": materiality,
        "required_evidence": required,
        "disconfirming_signals": _text_list(node.get("disconfirming_signals"))
        or _text_list(professional.get("refuting_evidence"))
        or ["寻找能直接推翻当前判断的高可靠数据。"],
        "decision_rule": node.get("decision_rule") or "只有当事实、推论、反证和信息来源结构同时闭合时，才上修父问题判断。",
        "information_categories": list(INFO_CATEGORIES),
        "preferred_source_types": preferred_source_types(node),
        "source_search_plan": source_search_plan,
        "task_family": task_family,
        "selected_skill": selected_skill,
        "extraction_schema": extraction_schema,
        "skill_dispatch_trace": {
            "task_family": task_family,
            "selected_skill": selected_skill,
            "concrete_materials": [item["source_type"] for item in source_search_plan],
            "extraction_schema": extraction_schema,
            "skill_output_status": "pending",
            "fallback_used": "",
            "gpt_verification_status": "pending",
        },
        "time_scope": node.get("time_frame") or "latest_available_and_historical_context",
        "max_sources": 8,
        "refresh_policy": "skip_if_complete",
    }


def classify_task_family(node: dict[str, Any], parent: dict[str, Any]) -> str:
    text = " ".join(
        [
            str(node.get("question", "")),
            str(parent.get("question", "")),
            " ".join(preferred_source_types(node)),
        ]
    ).lower()
    if _contains_any(text, ["估值", "赔率", "pe", "fcf", "dcf", "ev/ebitda", "倍", "price", "valuation"]):
        return "valuation"
    if _contains_any(text, ["财报", "年报", "季报", "10-k", "10-q", "20-f", "现金流", "毛利", "库存", "capex", "rpo", "backlog", "合同负债", "分部"]):
        return "financial_statement"
    if _contains_any(text, ["研报", "行业报告", "市场规模", "tam", "供需", "cagr", "trendforce", "gartner", "semi", "idc", "visible alpha"]):
        return "industry_report"
    if _contains_any(text, ["新闻", "消息", "政策", "监管", "公告消息", "传闻", "扩产", "订单消息", "launch"]):
        return "news_event"
    if _contains_any(text, ["观点", "专家", "投资者", "访谈", "社媒", "opinion", "interview"]):
        return "opinion"
    if _contains_any(text, ["标的", "证券", "ticker", "观察清单", "推荐", "strength", "强度"]):
        return "target_recommendation"
    return "leaf_research"


def selected_skill_for_task_family(task_family: str) -> str:
    return {
        "financial_statement": "financial-statement-analysis",
        "valuation": "valuation-analysis",
        "industry_report": "industry-report-analysis",
        "news_event": "news-event-analysis",
        "opinion": "opinion-analysis",
        "target_recommendation": "target-recommendation-analysis",
        "leaf_research": "leaf-research-deepseek",
    }.get(task_family, "leaf-research-deepseek")


def source_search_plan_for_task(node: dict[str, Any], parent: dict[str, Any], task_family: str) -> list[dict[str, str]]:
    question = node.get("question", "")
    parent_question = parent.get("question", "")
    base_plan = [
        {
            "source_bucket": "evidence",
            "source_type": "official filing / earnings release / regulator or exchange announcement",
            "why_needed": "直接验证事实、数字、口径和管理层公开披露。",
            "expected_fields": "收入、利润、现金流、capex、订单/backlog/RPO、分部口径、风险披露、日期。",
        },
        {
            "source_bucket": "research_report",
            "source_type": "industry report / sell-side report / third-party dataset",
            "why_needed": "补充市场空间、供需、价格、竞争格局、估值假设和横向比较。",
            "expected_fields": "TAM、增速、价格、份额、供需、利润池、方法论、关键假设。",
        },
        {
            "source_bucket": "message",
            "source_type": "news / policy update / supply-chain message",
            "why_needed": "捕捉最新变化、触发器和仍需验证的线索。",
            "expected_fields": "事件、时间、影响节点、确认状态、需要什么一手来源验证。",
        },
        {
            "source_bucket": "opinion",
            "source_type": "expert view / investor view / interview",
            "why_needed": "提取机制解释、变体认知、反方质询和盲点。",
            "expected_fields": "核心观点、假设、事实依据、反方问题、待验证数据。",
        },
    ]
    priority = {
        "financial_statement": ["evidence", "research_report", "message", "opinion"],
        "valuation": ["evidence", "research_report", "opinion", "message"],
        "industry_report": ["research_report", "evidence", "message", "opinion"],
        "news_event": ["message", "evidence", "research_report", "opinion"],
        "opinion": ["opinion", "evidence", "research_report", "message"],
        "target_recommendation": ["evidence", "research_report", "message", "opinion"],
        "leaf_research": ["evidence", "research_report", "message", "opinion"],
    }.get(task_family, ["evidence", "research_report", "message", "opinion"])
    by_bucket = {item["source_bucket"]: item for item in base_plan}
    plan = []
    for bucket in priority:
        item = dict(by_bucket[bucket])
        item["question_link"] = question
        item["parent_link"] = parent_question
        item["preferred_skill"] = selected_skill_for_task_family(task_family if bucket in {"evidence", "research_report"} else bucket.replace("message", "news_event"))
        plan.append(item)
    return plan


def extraction_schema_for_task(task_family: str) -> dict[str, Any]:
    common = {
        "fact": "verifiable facts with source context",
        "inference": "mechanism inferred from facts",
        "judgment": "bounded current judgment",
        "gap": "missing data before strengthening conclusion",
        "trigger": "data or event that changes the judgment",
        "support_refute_or_lead": "support|refute|lead",
        "source_links": ["auditable source URLs or local paths"],
    }
    family_fields = {
        "financial_statement": ["period", "currency", "segment_data", "cash_flow_quality", "capex", "inventory", "backlog_or_rpo", "accounting_flags"],
        "valuation": ["market_snapshot", "future_space", "priced_in_assumptions", "scenario_table", "valuation_odds", "margin_of_safety_gap"],
        "industry_report": ["market_size", "supply_demand", "price_or_margin_assumptions", "methodology", "assumptions_to_verify"],
        "news_event": ["event_type", "claim_status", "affected_node", "verification_source", "near_term_trigger"],
        "opinion": ["author", "core_claim", "argument_chain", "implicit_assumptions", "counterquestion"],
        "target_recommendation": ["ticker", "thesis_node", "future_space", "valuation_odds", "strength", "catalysts", "downgrade_triggers"],
        "leaf_research": ["selected_materials", "investment_relevance", "uncertainties", "follow_up_data"],
    }.get(task_family, [])
    return {**common, "family_specific_fields": family_fields}


def materiality_statement(question: str, parent_question: str, task_family: str) -> str:
    skill = selected_skill_for_task_family(task_family)
    return (
        f"该叶子问题用于回答父问题“{parent_question}”。"
        f"若证据成立或被反证，应影响上层结论、目标标的强度、估值赔率或风险触发器；"
        f"默认由 {skill} 处理材料后再由 GPT 验证。"
    )


def preferred_source_types(node: dict[str, Any]) -> list[str]:
    collection = node.get("information_collection", {}) or {}
    source_types: list[str] = []
    for category in INFO_CATEGORIES:
        for item in collection.get(category, {}).get("recommended_sources", []) or []:
            if item and item not in source_types:
                source_types.append(str(item))
    return source_types or ["公司公告/财报/监管文件", "第三方行业数据或深度报告", "主流财经媒体", "专家或产业观点"]


def framework_context(qa_tree: dict[str, Any], node: dict[str, Any], parent: dict[str, Any]) -> str:
    section = node.get("section_id") or parent.get("section_id") or "foundation"
    return (
        f"Object={qa_tree.get('ticker', '')}; Section={section}; "
        f"Parent={parent.get('question', '')}; Leaf={node.get('question', '')}; "
        "Use the research-goal QA framework, classify every input into evidence/research_report/message/opinion, "
        "plan sources before reading, dispatch to specialty parsers when useful, "
        "and separate facts, inferences, judgments, refuting evidence, leads, gaps, and triggers."
    )


def is_leaf_node(qa_tree: dict[str, Any], node: dict[str, Any]) -> bool:
    return int(node.get("level", 0) or 0) >= int(qa_tree.get("default_depth", 3) or 3) or not node.get("next_question_ids")


def leaf_question_count(qa_tree: dict[str, Any]) -> int:
    return sum(1 for node in qa_tree.get("nodes", []) if is_leaf_node(qa_tree, node))


def _contains_any(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


def _stable_task_id(ticker: str, node_id: str) -> str:
    digest = hashlib.sha256(f"{ticker}:{node_id}".encode("utf-8")).hexdigest()[:12]
    return f"leaf_{digest}"


def _text_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []
