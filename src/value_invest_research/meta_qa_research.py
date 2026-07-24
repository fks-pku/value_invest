from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any

from value_invest_research.answer_synthesis import apply_synthesis_overrides, load_synthesis_overrides
from value_invest_research.models import EvidenceRecord, ValidationError
from value_invest_research.research_system import (
    INFO_CATEGORY_LABEL_ZH,
    SOURCE_ORIGIN_INFO_ORDER,
    STANCE_LABEL_ZH,
    _apple_research_css,
    _collection_acceptance_criteria,
    _collection_recommended_sources,
    _draft_question_js,
    _evidence_stance_class,
    _information_stance,
    _qa_explorer_css,
    _render_add_question_box,
    _safe_id,
    _truncate_text,
    _write_json,
    _write_jsonl,
    _write_text,
    _zh_text,
)
from value_invest_research.scaffold import slugify


META_QA_OBJECT_TYPES = {"company", "industry", "event", "technology", "target_update", "custom"}


META_QA_BLUEPRINTS: dict[str, list[dict[str, Any]]] = {
    "company": [
        {
            "id": "growth",
            "question": "公司未来增长由什么驱动，空间和持续性如何？",
            "l2": [
                ("growth_driver", "增长来自市场扩张、份额提升、价格、产品周期还是新业务？"),
                ("future_space", "公司可捕获的未来空间有多大，增长期限和约束是什么？"),
            ],
        },
        {
            "id": "value_capture",
            "question": "公司是否具备护城河、单位经济和价值捕获能力？",
            "l2": [
                ("unit_economics", "收入、毛利、费用、现金流和资本开支如何构成单位经济？"),
                ("value_chain", "公司在产业链中靠什么议价权捕获或丢失利润？"),
            ],
        },
        {
            "id": "financial_valuation",
            "question": "财务质量、估值赔率和反证条件是否支持继续跟踪？",
            "l2": [
                ("financial_quality", "利润、现金流、资产负债和会计质量是否匹配业务叙事？"),
                ("valuation_odds", "当前估值隐含了什么增长、利润率和现金流假设？"),
                ("disconfirming_tests", "哪些事实会最快证伪公司增长、护城河或估值判断？"),
            ],
        },
        {
            "id": "observation_decision",
            "question": "应如何形成具体观察结论和后续监控清单？",
            "l2": [
                ("target_strength", "当前研究证据支持什么观察强度，为什么？"),
                ("monitoring_plan", "后续应跟踪哪些季度数据、催化剂和降级触发器？"),
            ],
        },
    ],
    "industry": [
        {
            "id": "demand",
            "question": "行业需求是否真实，未来空间来自哪里？",
            "l2": [
                ("market_size", "行业空间来自真实需求、价格、渗透率还是周期？"),
                ("demand_quality", "需求是否可持续，还是由补贴、库存或短期周期驱动？"),
                ("future_space", "未来空间应拆成总需求、瓶颈节点和公司可捕获空间中的哪几部分？"),
            ],
        },
        {
            "id": "bottleneck",
            "question": "产业链哪些瓶颈最可能捕获增量利润？",
            "l2": [
                ("profit_pool", "哪一段产业链获得主要利润和现金流？"),
                ("bottleneck_nodes", "哪些环节受产能、技术、客户认证或资本开支约束？"),
                ("value_capture", "哪些公司能把瓶颈转化为收入、毛利和现金流？"),
            ],
        },
        {
            "id": "disconfirming",
            "question": "哪些反证和市场定价会削弱当前机会？",
            "l2": [
                ("price_competition", "竞争会不会把增长转化为价格战和利润率下行？"),
                ("priced_in_risk", "市场价格和估值是否已经透支未来增长？"),
                ("disconfirming_signal", "什么数据会证明需求、瓶颈或利润池被高估？"),
            ],
        },
        {
            "id": "targets",
            "question": "哪些具体标的值得进入观察清单，理由和强度是什么？",
            "l2": [
                ("target_mapping", "哪些证券直接映射到已验证瓶颈或利润池？"),
                ("target_strength", "每个标的的未来空间、估值赔率、证据质量和风险如何排序？"),
                ("monitoring_data", "后续哪些数据会触发标的强度上调或下调？"),
            ],
        },
    ],
    "event": [
        {
            "id": "facts",
            "question": "这个事件的事实边界和时间线是什么？",
            "l2": [
                ("timeline", "事件发生了什么，哪些事实已经被确认？"),
                ("uncertainty", "哪些事实仍未确认或存在冲突口径？"),
            ],
        },
        {
            "id": "transmission",
            "question": "事件通过哪些路径影响资产和公司基本面？",
            "l2": [
                ("channels", "事件的价格、需求、成本、政策和情绪传导路径是什么？"),
                ("affected_objects", "哪些公司、行业或地区会最先受到影响？"),
            ],
        },
        {
            "id": "market_baseline",
            "question": "市场当前可能已经定价了什么？",
            "l2": [
                ("priced_in", "市场价格、预期和共识可能隐含了哪些判断？"),
                ("surprise", "什么信息会构成超预期或低于预期？"),
            ],
        },
        {
            "id": "follow_up",
            "question": "后续最重要的跟踪和反证条件是什么？",
            "l2": [
                ("triggers", "哪些公告、数据或行为会触发判断更新？"),
                ("disconfirming_signal", "什么信息会证明事件影响被高估或低估？"),
            ],
        },
    ],
    "technology": [
        {
            "id": "feasibility_demand",
            "question": "技术路线是否可行，采用需求是否真实？",
            "l2": [
                ("technical_feasibility", "关键性能、成本、良率和可靠性是否达到采用门槛？"),
                ("adoption_demand", "客户为什么需要这条技术路线，替代旧方案的收益是什么？"),
            ],
        },
        {
            "id": "ecosystem_bottleneck",
            "question": "生态和产业链瓶颈在哪里？",
            "l2": [
                ("supply_chain_readiness", "上游材料、设备、工艺、软件和客户认证是否准备好？"),
                ("bottleneck_nodes", "哪些环节最稀缺且最可能捕获利润？"),
            ],
        },
        {
            "id": "commercialization_competition",
            "question": "商业化、竞争和反证条件如何影响机会？",
            "l2": [
                ("commercial_timing", "商业化节奏、价格曲线和成本下降路径是否清晰？"),
                ("competing_routes", "替代路线、现有方案和客户自研会如何压制空间？"),
            ],
        },
        {
            "id": "exposed_assets",
            "question": "哪些资产暴露于这条技术路线，如何跟踪？",
            "l2": [
                ("target_mapping", "哪些公司或资产能直接捕获这条技术路线的增量利润？"),
                ("monitoring_data", "哪些技术、订单、财务和估值数据决定观察强度？"),
            ],
        },
    ],
    "target_update": [
        {
            "id": "change",
            "question": "这个标的或资产发生了什么关键变化？",
            "l2": [
                ("fact_change", "新增事实是什么，和上次判断相比变在哪里？"),
                ("source_quality", "新增信息来自官方证据、研报、消息还是观点？"),
            ],
        },
        {
            "id": "thesis_node",
            "question": "变化影响了哪一个原始 thesis node？",
            "l2": [
                ("fundamental_node", "变化影响需求、利润池、财务质量、管理层还是风险？"),
                ("mechanism_change", "变化通过什么机制改变收入、利润、现金流或估值？"),
            ],
        },
        {
            "id": "odds_change",
            "question": "价格、估值和风险回报是否改变？",
            "l2": [
                ("valuation_reset", "当前估值隐含假设是否发生变化？"),
                ("disconfirming_signal", "什么信息会证明本次变化被市场高估或低估？"),
            ],
        },
        {
            "id": "observation_update",
            "question": "观察强度和后续监控应如何调整？",
            "l2": [
                ("strength_change", "应上调、下调还是维持观察强度，证据是什么？"),
                ("monitoring_plan", "下一次更新必须检查哪些数据和触发器？"),
            ],
        },
    ],
    "custom": [
        {
            "id": "facts",
            "question": "为了回答元问题，必须先确认哪些事实？",
            "l2": [
                ("known_unknown", "已知事实、未知事实和冲突口径分别是什么？"),
                ("source_quality", "哪些来源可以直接支撑或反证事实？"),
            ],
        },
        {
            "id": "mechanism",
            "question": "元问题背后的核心机制是什么？",
            "l2": [
                ("drivers", "哪些变量真正驱动结论变化？"),
                ("sensitivity", "结论对哪些假设最敏感？"),
            ],
        },
        {
            "id": "scenarios",
            "question": "应该如何拆分情景和概率？",
            "l2": [
                ("base_case", "基准情景需要哪些证据支撑？"),
                ("variant_perception", "什么信息会导致判断上修或下修？"),
            ],
        },
        {
            "id": "decision_boundary",
            "question": "结论的边界和反证条件是什么？",
            "l2": [
                ("disconfirming_signal", "什么信息会反证当前判断？"),
                ("next_action", "下一步最该搜集哪类信息？"),
            ],
        },
    ],
}


L3_DRILLDOWNS = [
    ("evidence_map", "哪些关键材料能直接回答这个问题，并改变上层结论或标的强度？"),
    ("disconfirming_test", "哪些证据、数据或价格信号会支撑、反证或限制当前判断？"),
]


def build_meta_qa_research(
    root: Path,
    object_type: str,
    object_id: str,
    meta_question: str,
    project_id: str | None = None,
    max_depth: int = 3,
    planner_client: Any | None = None,
    force_plan: bool = False,
) -> dict[str, Any]:
    """Build a generic layered QA research project from one meta-question."""
    project = _project_config(object_type, object_id, meta_question, project_id, max_depth)
    project_dir = _project_dir(root, project["project_id"])
    project_dir.mkdir(parents=True, exist_ok=True)
    _write_json(project_dir / "project.json", project)
    question_plan_path = project_dir / "question_plan.json"
    if question_plan_path.exists() and not force_plan:
        _load_question_plan(project_dir, project)
    else:
        _write_json(question_plan_path, _create_question_plan(project, planner_client))
    if not (project_dir / "evidence.jsonl").exists():
        _write_text(project_dir / "evidence.jsonl", "")
    return _rebuild_meta_qa_project(root, project["project_id"])


def plan_meta_qa_questions(
    root: Path,
    object_type: str,
    object_id: str,
    meta_question: str,
    project_id: str | None = None,
    max_depth: int = 3,
    force: bool = False,
    client: Any | None = None,
) -> dict[str, Any]:
    """Create or refresh the auditable question plan for a generic QA project."""
    project = _project_config(object_type, object_id, meta_question, project_id, max_depth)
    project_dir = _project_dir(root, project["project_id"])
    project_dir.mkdir(parents=True, exist_ok=True)
    project_path = project_dir / "project.json"
    if project_path.exists() and not force:
        project = _load_project(project_dir)
    else:
        _write_json(project_path, project)
    plan_path = project_dir / "question_plan.json"
    if plan_path.exists() and not force:
        plan = _load_question_plan(project_dir, project)
        created = False
    else:
        plan = _create_question_plan(project, client)
        _write_json(plan_path, plan)
        created = True
    if not (project_dir / "evidence.jsonl").exists():
        _write_text(project_dir / "evidence.jsonl", "")
    return {
        "project_id": project["project_id"],
        "project_dir": str(project_dir),
        "question_plan_path": str(plan_path),
        "created": created,
        "l1_questions": len(plan.get("l1", [])),
        "leaf_questions": _planned_leaf_count(plan),
        "planning_mode": plan.get("planning_mode", ""),
    }


def add_meta_qa_question(root: Path, project_id: str, parent_id: str, question: str, terminal: bool = False) -> dict[str, Any]:
    """Persist a user-added question under any generic QA project node."""
    project_dir = _project_dir(root, project_id)
    project = _load_project(project_dir)
    cleaned_question = question.strip()
    if not cleaned_question:
        raise ValueError("question cannot be empty")

    qa_tree = _build_meta_qa_tree(
        project,
        _load_question_plan(project_dir, project),
        _load_project_evidence(project_dir),
        _load_custom_questions(project_dir),
    )
    nodes_by_id = {node.get("id"): node for node in qa_tree.get("nodes", [])}
    if parent_id not in nodes_by_id:
        raise ValueError(f"parent question not found: {parent_id}")

    parent = nodes_by_id[parent_id]
    actual_parent = nodes_by_id.get(parent.get("parent_id", "")) if int(parent.get("level", 0)) >= project["max_depth"] else parent
    actual_parent = actual_parent or parent
    existing = _matching_custom_question(_load_custom_questions(project_dir), parent_id, cleaned_question)
    if existing:
        result = _rebuild_meta_qa_project(root, project_id)
        return {**result, "question_id": existing["id"], "created": False}

    question_id = _custom_question_id(actual_parent.get("id", ""), cleaned_question, {node["id"] for node in qa_tree["nodes"]})
    row = {
        "id": question_id,
        "requested_parent_id": parent_id,
        "parent_id": actual_parent.get("id", ""),
        "level": min(int(actual_parent.get("level", 0)) + 1, project["max_depth"]),
        "question": cleaned_question,
        "terminal": bool(terminal),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "user_added",
    }
    with (project_dir / "custom_questions.jsonl").open("a", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    result = _rebuild_meta_qa_project(root, project_id)
    return {**result, "question_id": question_id, "created": True}


def record_meta_qa_information(
    root: Path,
    project_id: str,
    node_id: str,
    category: str,
    source_type: str,
    source_name: str,
    url: str,
    summary: str,
    reliability: str = "medium",
    materiality: str = "medium",
    published_at: str | None = None,
) -> dict[str, Any]:
    """Attach one collected information item to a generic QA node."""
    project_dir = _project_dir(root, project_id)
    project = _load_project(project_dir)
    if category not in SOURCE_ORIGIN_INFO_ORDER:
        raise ValueError(f"category must be one of {SOURCE_ORIGIN_INFO_ORDER}")

    qa_tree = _build_meta_qa_tree(
        project,
        _load_question_plan(project_dir, project),
        _load_project_evidence(project_dir),
        _load_custom_questions(project_dir),
    )
    if node_id not in {node["id"] for node in qa_tree["nodes"]}:
        raise ValueError(f"question node not found: {node_id}")

    record = _project_evidence_record(
        project=project,
        node_id=node_id,
        category=category,
        source_type=source_type,
        source_name=source_name,
        url=url,
        summary=summary,
        reliability=reliability,
        materiality=materiality,
        published_at=published_at,
    )
    evidence_path = project_dir / "evidence.jsonl"
    upsert = _upsert_project_evidence(evidence_path, record, project["project_id"], node_id)
    result = _rebuild_meta_qa_project(root, project_id)
    return {
        **result,
        "node_id": node_id,
        "category": category,
        "evidence_id": upsert["evidence_id"],
        "evidence_path": str(evidence_path),
        "created": upsert["created"],
        "updated": upsert["updated"],
    }


def _rebuild_meta_qa_project(root: Path, project_id: str) -> dict[str, Any]:
    project_dir = _project_dir(root, project_id)
    project = _load_project(project_dir)
    question_plan = _load_question_plan(project_dir, project)
    evidence = _load_project_evidence(project_dir)
    custom_questions = _load_custom_questions(project_dir)
    synthesis_overrides = load_synthesis_overrides(project_dir)
    qa_tree = _build_meta_qa_tree(project, question_plan, evidence, custom_questions, synthesis_overrides)
    information_rows = _attach_information_collection(qa_tree)

    qa_tree_path = project_dir / "qa_tree.json"
    question_plan_path = project_dir / "question_plan.json"
    information_path = project_dir / "information_collection.jsonl"
    dashboard_path = project_dir / "research_dashboard.html"
    report_path = project_dir / "research_report.html"

    _write_json(qa_tree_path, qa_tree)
    _write_jsonl(information_path, information_rows)
    _write_text(dashboard_path, _render_meta_qa_dashboard(project, qa_tree))
    _write_text(report_path, _render_meta_qa_report(project, qa_tree))

    return {
        "project_id": project["project_id"],
        "project_dir": str(project_dir),
        "question_plan_path": str(question_plan_path),
        "qa_tree_path": str(qa_tree_path),
        "information_collection_path": str(information_path),
        "dashboard_path": str(dashboard_path),
        "report_path": str(report_path),
        "nodes": len(qa_tree["nodes"]),
        "leaf_questions": sum(1 for node in qa_tree["nodes"] if _is_leaf_node(qa_tree, node)),
        "planning_mode": question_plan.get("planning_mode", ""),
    }


def _project_config(
    object_type: str,
    object_id: str,
    meta_question: str,
    project_id: str | None,
    max_depth: int,
) -> dict[str, Any]:
    normalized_type = object_type.strip().lower()
    if normalized_type not in META_QA_OBJECT_TYPES:
        raise ValueError(f"object_type must be one of {sorted(META_QA_OBJECT_TYPES)}")
    cleaned_question = meta_question.strip()
    if not cleaned_question:
        raise ValueError("meta_question cannot be empty")
    if not 1 <= max_depth <= 3:
        raise ValueError("max_depth must be between 1 and 3")
    return {
        "schema_version": "1.0",
        "project_id": project_id.strip() if project_id else _default_project_id(normalized_type, object_id, cleaned_question),
        "object_type": normalized_type,
        "object_id": object_id.strip(),
        "meta_question": cleaned_question,
        "max_depth": max_depth,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def _default_project_id(object_type: str, object_id: str, meta_question: str) -> str:
    base = slugify(object_id) or slugify(meta_question)[:48] or "qa_project"
    digest = hashlib.sha1(f"{object_type}\n{object_id}\n{meta_question}".encode("utf-8")).hexdigest()[:8]
    return _safe_id(f"{object_type}_{base}_{digest}")


def _project_dir(root: Path, project_id: str) -> Path:
    cleaned = _safe_id(project_id)
    if not cleaned:
        raise ValueError("project_id must be non-empty")
    return root / "research" / "bom" / cleaned


def _load_project(project_dir: Path) -> dict[str, Any]:
    path = project_dir / "project.json"
    if not path.exists():
        raise ValueError(f"QA project not found: {project_dir}")
    project = json.loads(path.read_text(encoding="utf-8"))
    project["max_depth"] = int(project.get("max_depth", 3))
    return project


def _load_question_plan(project_dir: Path, project: dict[str, Any]) -> dict[str, Any]:
    path = project_dir / "question_plan.json"
    if not path.exists():
        plan = _deterministic_question_plan(project)
        _write_json(path, plan)
        return plan
    plan = json.loads(path.read_text(encoding="utf-8"))
    _validate_question_plan(plan, path)
    return plan


def _validate_question_plan(plan: dict[str, Any], path: Path) -> None:
    if not isinstance(plan, dict):
        raise ValueError(f"{path}: question plan must be an object")
    if not isinstance(plan.get("l1"), list) or not plan["l1"]:
        raise ValueError(f"{path}: question plan requires non-empty l1 list")
    for l1 in plan["l1"]:
        _validate_plan_node(l1, path, level="l1")


def _validate_plan_node(node: dict[str, Any], path: Path, level: str) -> None:
    if not isinstance(node, dict):
        raise ValueError(f"{path}: {level} plan node must be an object")
    for key in ["id", "question"]:
        if not isinstance(node.get(key), str) or not node[key].strip():
            raise ValueError(f"{path}: {level} plan node requires {key}")


def _create_question_plan(project: dict[str, Any], client: Any | None) -> dict[str, Any]:
    if client is None:
        return _deterministic_question_plan(project)
    return _llm_question_plan(project, client)


def _llm_question_plan(project: dict[str, Any], client: Any) -> dict[str, Any]:
    fallback = _deterministic_question_plan(project)
    response_text = client.chat(_planner_system_prompt(), _planner_user_prompt(project, fallback))
    parsed = _extract_json_object(response_text)
    if not parsed:
        return _fallback_plan(project, fallback, "llm_invalid_fallback", "LLM 未返回可解析 JSON，已回退到确定性问题规划。")
    try:
        return _normalize_llm_question_plan(project, parsed, fallback)
    except ValueError as exc:
        return _fallback_plan(project, fallback, "llm_invalid_fallback", f"LLM 问题规划未通过校验：{exc}。已回退到确定性问题规划。")


def _planner_system_prompt() -> str:
    return (
        "你是专业二级市场投研主管，负责把一个元问题拆成可执行的层级 QA 研究计划。"
        "最多下钻三层；当某个问题不需要继续下钻时，应设置为终端问题并进入四类信息搜集。"
        "不得给出交易建议。输出必须是 JSON 对象。"
    )


def _planner_user_prompt(project: dict[str, Any], fallback: dict[str, Any]) -> str:
    contract = {
        "schema_version": "1.0",
        "planner_rationale": "为什么这样拆问题",
        "detected_signals": ["信号1", "信号2"],
        "l1": [
            {
                "id": "short_snake_case_id",
                "question": "L1 问题",
                "rationale": "为什么需要这个问题",
                "should_drill_down": True,
                "terminal_reason": "",
                "l2": [
                    {
                        "id": "short_snake_case_id",
                        "question": "L2 问题",
                        "rationale": "为什么需要这个问题",
                        "should_drill_down": True,
                        "terminal_reason": "",
                        "l3": [
                            {
                                "id": "short_snake_case_id",
                                "question": "L3 终端问题",
                                "rationale": "为什么到这里开始收集信息",
                                "should_drill_down": False,
                                "should_collect_information": True,
                                "terminal_reason": "已经到达可回答粒度",
                                "information_focus": {
                                    "evidence": "需要哪些公告、官方数据或可验证事实",
                                    "research_report": "需要哪些商业研报或第三方研究",
                                    "message": "需要哪些公开但未完全证实的消息线索",
                                    "opinion": "需要哪些专家、产业人士或投资者观点",
                                },
                            }
                        ],
                    }
                ],
            }
        ],
    }
    compact_project = {
        "object_type": project["object_type"],
        "object_id": project["object_id"],
        "meta_question": project["meta_question"],
        "max_depth": project["max_depth"],
    }
    return "\n".join(
        [
            "请为以下投研元问题生成层级 QA 问题规划，只输出 JSON，不要输出 Markdown。",
            "",
            json.dumps(compact_project, ensure_ascii=False, indent=2, sort_keys=True),
            "",
            "输出结构必须符合：",
            json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True),
            "",
            "约束：",
            "- L1 建议 4 个，按研究类型覆盖增长/需求、瓶颈/价值捕获、反证/估值赔率、具体标的或监控结论。",
            "- L2 每个 L1 建议 1-3 个；L3 每个 L2 建议 1-3 个。",
            "- 若 max_depth 小于 3，按 max_depth 截断，不要强行生成更深层。",
            "- 叶子问题必须能直接进入资料规划和四类信息搜集，并写清 information_focus。",
            "- 每个叶子问题都要能影响上层结论、标的强度、估值赔率或风险控制；不能只问背景介绍。",
            "- question 必须是中文投研问题，避免空泛标题。",
            "- id 使用英文 snake_case，短而稳定。",
            "",
            "如果不确定，可参考但不要照抄这个确定性基线：",
            json.dumps(
                {
                    "planner_rationale": fallback.get("planner_rationale", ""),
                    "detected_signals": fallback.get("detected_signals", []),
                    "l1": fallback.get("l1", []),
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            ),
        ]
    )


def _normalize_llm_question_plan(
    project: dict[str, Any],
    parsed: dict[str, Any],
    fallback: dict[str, Any],
) -> dict[str, Any]:
    raw_l1 = parsed.get("l1")
    if not isinstance(raw_l1, list) or not raw_l1:
        raise ValueError("l1 must be a non-empty list")
    signals = _text_list(parsed.get("detected_signals")) or fallback.get("detected_signals", [])
    subject = _plan_subject(project)
    plan = {
        "schema_version": "1.0",
        "project_id": project["project_id"],
        "object_type": project["object_type"],
        "object_id": project["object_id"],
        "meta_question": project["meta_question"],
        "max_depth": project["max_depth"],
        "planning_mode": "llm",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "planner_rationale": _clean_text(parsed.get("planner_rationale")) or fallback.get("planner_rationale", ""),
        "detected_signals": signals,
        "l1": [],
    }
    for index, raw_node in enumerate(raw_l1[:6], start=1):
        if not isinstance(raw_node, dict):
            continue
        node = _normalize_plan_node(project, subject, raw_node, f"l1_{index}", 1, signals)
        if node:
            plan["l1"].append(node)
    if not plan["l1"]:
        raise ValueError("no valid l1 nodes")
    return plan


def _normalize_plan_node(
    project: dict[str, Any],
    subject: str,
    raw_node: dict[str, Any],
    fallback_id: str,
    level: int,
    signals: list[str],
) -> dict[str, Any] | None:
    question = _clean_text(raw_node.get("question"))
    if not question:
        return None
    node_id = _safe_id(_clean_text(raw_node.get("id"))) or fallback_id
    should_drill = bool(raw_node.get("should_drill_down", level < project["max_depth"]))
    reaches_depth = level >= project["max_depth"]
    should_collect = bool(raw_node.get("should_collect_information", reaches_depth or not should_drill))
    node = {
        "id": node_id,
        "question": question,
        "rationale": _clean_text(raw_node.get("rationale")) or _plan_node_rationale(project, node_id, signals),
        "should_drill_down": bool(should_drill and not reaches_depth),
        "terminal_reason": _clean_text(raw_node.get("terminal_reason")),
    }
    if should_collect:
        node["should_collect_information"] = True
        node["information_focus"] = _normalize_information_focus(project, subject, question, signals, raw_node.get("information_focus"))
    if node["should_drill_down"]:
        child_key = f"l{level + 1}"
        child_cap = 4 if level == 1 else 3
        children = []
        raw_children = raw_node.get(child_key, [])
        if isinstance(raw_children, list):
            for index, raw_child in enumerate(raw_children[:child_cap], start=1):
                if isinstance(raw_child, dict):
                    child = _normalize_plan_node(project, subject, raw_child, f"{node_id}_{child_key}_{index}", level + 1, signals)
                    if child:
                        children.append(child)
        node[child_key] = children
        if not children:
            node["should_drill_down"] = False
            node["should_collect_information"] = True
            node["terminal_reason"] = node["terminal_reason"] or "LLM 未提供有效子问题，本层作为叶子问题进入信息搜集。"
            node["information_focus"] = _normalize_information_focus(project, subject, question, signals, raw_node.get("information_focus"))
    elif not node["terminal_reason"]:
        node["terminal_reason"] = "该问题已达到可回答粒度，进入四类信息搜集。"
    return node


def _normalize_information_focus(
    project: dict[str, Any],
    subject: str,
    question: str,
    signals: list[str],
    raw_focus: Any,
) -> dict[str, str]:
    fallback = _information_focus(project, subject, question, signals)
    if not isinstance(raw_focus, dict):
        return fallback
    return {
        category: _clean_text(raw_focus.get(category)) or fallback[category]
        for category in SOURCE_ORIGIN_INFO_ORDER
    }


def _fallback_plan(project: dict[str, Any], fallback: dict[str, Any], mode: str, reason: str) -> dict[str, Any]:
    plan = dict(fallback)
    plan["planning_mode"] = mode
    plan["planner_rationale"] = reason
    plan["generated_at"] = datetime.now(timezone.utc).isoformat()
    return plan


def _extract_json_object(text: str) -> dict[str, Any]:
    candidates = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    candidates.append(text.strip())
    brace_match = re.search(r"(\{.*\})", text, flags=re.DOTALL)
    if brace_match:
        candidates.append(brace_match.group(1))
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return {}


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _text_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, list):
        return [_clean_text(item) for item in value if _clean_text(item)]
    text = _clean_text(value)
    return [text] if text else []


def _deterministic_question_plan(project: dict[str, Any]) -> dict[str, Any]:
    subject = _plan_subject(project)
    signals = _planning_signals(project)
    l1_nodes = [_planned_l1(project, subject, item, signals) for item in META_QA_BLUEPRINTS[project["object_type"]]]
    return {
        "schema_version": "1.0",
        "project_id": project["project_id"],
        "object_type": project["object_type"],
        "object_id": project["object_id"],
        "meta_question": project["meta_question"],
        "max_depth": project["max_depth"],
        "planning_mode": "deterministic_rule_based",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "planner_rationale": _planner_rationale(project, signals),
        "detected_signals": signals,
        "l1": l1_nodes,
    }


def _planned_l1(
    project: dict[str, Any],
    subject: str,
    blueprint: dict[str, Any],
    signals: list[str],
) -> dict[str, Any]:
    l1_id = blueprint["id"]
    l2_nodes = [
        _planned_l2(project, subject, l1_id, l2_id, l2_question, signals)
        for l2_id, l2_question in blueprint.get("l2", [])
    ]
    return {
        "id": l1_id,
        "question": _tailored_l1_question(project, subject, l1_id, blueprint["question"], signals),
        "rationale": _plan_node_rationale(project, l1_id, signals),
        "should_drill_down": project["max_depth"] >= 2,
        "terminal_reason": "" if project["max_depth"] >= 2 else "用户设置 max_depth=1，本层直接进入信息搜集。",
        "l2": l2_nodes if project["max_depth"] >= 2 else [],
    }


def _planned_l2(
    project: dict[str, Any],
    subject: str,
    l1_id: str,
    l2_id: str,
    question: str,
    signals: list[str],
) -> dict[str, Any]:
    tailored_question = _tailored_l2_question(project, subject, l1_id, l2_id, question, signals)
    l3_nodes = [
        _planned_l3(project, subject, tailored_question, suffix, l3_question, signals)
        for suffix, l3_question in L3_DRILLDOWNS
    ]
    return {
        "id": l2_id,
        "question": tailored_question,
        "rationale": _plan_node_rationale(project, l2_id, signals),
        "should_drill_down": project["max_depth"] >= 3,
        "terminal_reason": "" if project["max_depth"] >= 3 else "达到用户设置的最大深度，本层直接进入信息搜集。",
        "l3": l3_nodes if project["max_depth"] >= 3 else [],
    }


def _planned_l3(
    project: dict[str, Any],
    subject: str,
    parent_question: str,
    suffix: str,
    question: str,
    signals: list[str],
) -> dict[str, Any]:
    focus = _information_focus(project, subject, parent_question, signals)
    return {
        "id": suffix,
        "question": f"{_subject_prefixed_question(subject, parent_question)}：{question}",
        "rationale": "叶子问题用于进入四类信息搜集，并形成可上抛的专业回答。",
        "should_drill_down": False,
        "should_collect_information": True,
        "terminal_reason": "默认三层下钻已到达叶子层，开始按四类信息搜集。",
        "information_focus": focus,
    }


def _tailored_l1_question(project: dict[str, Any], subject: str, l1_id: str, fallback: str, signals: list[str]) -> str:
    object_type = project["object_type"]
    if object_type == "industry":
        mapping = {
            "demand": f"{subject}的需求是否真实，未来空间来自哪里？",
            "bottleneck": f"{subject}产业链哪些瓶颈最可能捕获增量利润？",
            "disconfirming": f"哪些反证和市场定价会削弱{subject}机会？",
            "targets": f"{subject}哪些具体标的值得进入观察清单，理由和强度是什么？",
        }
        return mapping.get(l1_id, fallback)
    if object_type == "company":
        mapping = {
            "growth": f"{subject}未来增长由什么驱动，空间和持续性如何？",
            "value_capture": f"{subject}是否具备护城河、单位经济和价值捕获能力？",
            "financial_valuation": f"{subject}财务质量、估值赔率和反证条件是否支持继续跟踪？",
            "observation_decision": f"{subject}应如何形成具体观察结论和后续监控清单？",
        }
        return mapping.get(l1_id, fallback)
    if object_type == "event":
        mapping = {
            "facts": f"{subject}的事实边界、时间线和未确认点是什么？",
            "transmission": f"{subject}通过哪些路径影响资产和公司基本面？",
            "market_baseline": f"{subject}当前可能已经被市场定价了什么？",
            "follow_up": f"{subject}后续最重要的跟踪和反证条件是什么？",
        }
        return mapping.get(l1_id, fallback)
    if object_type == "technology":
        mapping = {
            "feasibility_demand": f"{subject}技术路线是否可行，采用需求是否真实？",
            "ecosystem_bottleneck": f"{subject}生态和产业链瓶颈在哪里？",
            "commercialization_competition": f"{subject}商业化、竞争和反证条件如何影响机会？",
            "exposed_assets": f"哪些资产暴露于{subject}，如何跟踪？",
        }
        return mapping.get(l1_id, fallback)
    if object_type == "target_update":
        mapping = {
            "change": f"{subject}发生了什么关键变化？",
            "thesis_node": f"{subject}变化影响了哪一个原始 thesis node？",
            "odds_change": f"{subject}价格、估值和风险回报是否改变？",
            "observation_update": f"{subject}观察强度和后续监控应如何调整？",
        }
        return mapping.get(l1_id, fallback)
    return _subject_prefixed_question(subject, fallback)


def _tailored_l2_question(
    project: dict[str, Any],
    subject: str,
    l1_id: str,
    l2_id: str,
    question: str,
    signals: list[str],
) -> str:
    if "smart_ev" in signals and l2_id == "price_competition":
        return f"{subject}竞争会不会演化为价格战、补贴竞争和利润率下行？"
    if "ai" in signals and l2_id in {"policy_technology", "drivers", "bottleneck_nodes", "future_space"}:
        return f"AI、算法、芯片和数据能力如何改变{subject}的竞争结构？"
    if "policy" in signals and l2_id in {"policy_technology", "channels"}:
        return f"政策、监管和补贴变化如何影响{subject}的需求、成本和竞争？"
    if "supply_chain" in signals and l2_id in {"value_chain", "bargaining_power", "bottleneck_nodes", "supply_chain_readiness"}:
        return f"{subject}供应链瓶颈、关键零部件和渠道议价权如何分配经济性？"
    return _subject_prefixed_question(subject, question)


def _planning_signals(project: dict[str, Any]) -> list[str]:
    text = f"{project.get('object_id', '')} {project.get('meta_question', '')}".lower()
    signals: list[str] = []
    patterns = {
        "smart_ev": ["电动车", "新能源车", "ev", "汽车", "智能车"],
        "ai": ["ai", "人工智能", "大模型", "算法", "智能"],
        "policy": ["政策", "监管", "补贴", "关税", "合规"],
        "supply_chain": ["产业链", "供应链", "上游", "下游", "零部件"],
        "long_term_value": ["长期", "投资价值", "复利", "价值"],
        "event_shock": ["事件", "影响", "冲击", "上调", "下调"],
    }
    for signal, keywords in patterns.items():
        if any(keyword in text for keyword in keywords):
            signals.append(signal)
    return signals or ["general_research"]


def _planner_rationale(project: dict[str, Any], signals: list[str]) -> str:
    subject = _plan_subject(project)
    signal_text = "、".join(signals)
    return (
        f"围绕“{project['meta_question']}”，系统先识别研究对象“{subject}”和信号“{signal_text}”，"
        "再按研究类型拆成 Q1-Q4：需求/增长、瓶颈/价值捕获、反证/估值赔率、具体标的或监控结论；"
        "默认三层下钻后进入资料规划、专业解析、GPT 验证和上层汇总。"
    )


def _plan_node_rationale(project: dict[str, Any], node_id: str, signals: list[str]) -> str:
    if any(token in node_id for token in ("demand", "market", "growth", "future", "facts", "change")):
        return "先确认事实、需求、增长空间和基础边界，避免直接跳到标的。"
    if any(token in node_id for token in ("value", "profit", "economics", "transmission", "bottleneck", "moat", "unit")):
        return "再确认价值链、瓶颈、利润池或事件传导机制，判断谁能真实捕获经济性。"
    if any(token in node_id for token in ("valuation", "priced", "risk", "disconfirm", "competition", "scenario", "odds")):
        return "继续拆估值赔率、竞争和反证，识别当前价格是否已经打满。"
    if any(token in node_id for token in ("target", "monitor", "observation", "strength")):
        return "最后映射到具体标的、观察强度、催化剂、风险和跟踪数据。"
    return "设置可验证的问题、触发器和反证条件，保证结论可被更新。"


def _information_focus(
    project: dict[str, Any],
    subject: str,
    parent_question: str,
    signals: list[str],
) -> dict[str, str]:
    return {
        "evidence": f"{subject}与“{parent_question}”相关的公告、财报/季报、法说、监管文件、官方数据、订单/backlog/RPO、现金流、估值基础数据和可验证事实。",
        "research_report": f"第三方对{subject}中“{parent_question}”的市场空间、供需、价格、利润池、竞争格局、估值假设和关键模型。",
        "message": f"公开新闻、产业链进展、政策更新、产品/订单/扩产消息，以及未完全确认但可能影响“{parent_question}”的线索。",
        "opinion": f"专家、产业人士或投资者对“{parent_question}”的机制解释、变体认知、反方质询和需要验证的假设。",
    }


def _planned_leaf_count(plan: dict[str, Any]) -> int:
    count = 0
    for l1 in plan.get("l1", []):
        if not l1.get("l2"):
            count += 1
        for l2 in l1.get("l2", []):
            count += len(l2.get("l3", [])) or 1
    return count


def _plan_subject(project: dict[str, Any]) -> str:
    return project.get("object_id", "").strip() or project.get("meta_question", "").strip() or "该研究对象"


def _subject_prefixed_question(subject: str, question: str) -> str:
    return question if subject in question else f"{subject}：{question}"


def _load_project_evidence(project_dir: Path) -> list[EvidenceRecord]:
    path = project_dir / "evidence.jsonl"
    if not path.exists():
        return []
    records: list[EvidenceRecord] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(EvidenceRecord.from_dict(json.loads(line)))
        except (json.JSONDecodeError, ValidationError) as exc:
            raise ValueError(f"{path}:{line_number}: {exc}") from exc
    return records


def _load_custom_questions(project_dir: Path) -> list[dict[str, Any]]:
    path = project_dir / "custom_questions.jsonl"
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line_number}: custom question must be an object")
        rows.append(row)
    return rows


def _build_meta_qa_tree(
    project: dict[str, Any],
    question_plan: dict[str, Any],
    evidence: list[EvidenceRecord],
    custom_questions: list[dict[str, Any]],
    synthesis_overrides: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    root = {
        "id": "meta.root",
        "level": 0,
        "parent_id": None,
        "question": project["meta_question"],
        "current_answer": "系统先将元问题拆成三层问题树；叶子问题用证据、研究报告、消息和观点四类信息回答，再逐层上抛。",
        "evidence_buckets": _empty_buckets(),
        "synthesis": {
            "facts": [],
            "inferences": ["元问题需要先结构化，不直接写成静态文章。"],
            "judgment": "当前处于层级 QA 研究状态，结论强度取决于叶子问题的信息覆盖。",
            "gaps": ["需要补齐叶子问题的四类信息，尤其是一手或高可靠来源。"],
            "confidence": "low",
        },
        "rollup_to_parent": "",
        "next_question_ids": [],
        "status": "open",
        "metadata": {
            "planner_rationale": question_plan.get("planner_rationale", ""),
            "planning_mode": question_plan.get("planning_mode", ""),
        },
    }
    nodes = [root]
    for l1 in question_plan.get("l1", []):
        l1_id = f"l1.{l1['id']}"
        l1_node = _node(l1_id, 1, "meta.root", l1["question"], project, evidence, l1)
        root["next_question_ids"].append(l1_id)
        nodes.append(l1_node)
        if project["max_depth"] < 2:
            continue
        for l2 in l1.get("l2", []):
            l2_id = f"{l1_id}.{l2['id']}"
            l2_node = _node(l2_id, 2, l1_id, l2["question"], project, evidence, l2)
            l1_node["next_question_ids"].append(l2_id)
            nodes.append(l2_node)
            if project["max_depth"] < 3:
                continue
            for l3 in l2.get("l3", []):
                child_id = f"{l2_id}.{l3['id']}"
                child = _node(child_id, 3, l2_id, l3["question"], project, evidence, l3)
                l2_node["next_question_ids"].append(child_id)
                nodes.append(child)

    tree = {
        "schema_version": "1.0",
        "project_id": project["project_id"],
        "object_type": project["object_type"],
        "object_id": project["object_id"],
        "meta_question": project["meta_question"],
        "default_depth": project["max_depth"],
        "question_plan": question_plan,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "interaction_contract": {
            "node_model": "Every node is a question with evidence buckets, synthesis, rollup, and child links.",
            "information_categories": SOURCE_ORIGIN_INFO_ORDER,
            "new_question_behavior": "Add a question at any level, collect four-bucket information, update the node answer, then rebuild the report.",
        },
        "nodes": nodes,
    }
    _apply_custom_questions(tree, project, custom_questions, evidence)
    _apply_linked_evidence(tree, evidence)
    apply_synthesis_overrides(tree, synthesis_overrides or [])
    _rollup_parent_nodes(tree)
    apply_synthesis_overrides(tree, synthesis_overrides or [])
    return tree


def _node(
    node_id: str,
    level: int,
    parent_id: str,
    question: str,
    project: dict[str, Any],
    evidence: list[EvidenceRecord],
    plan_node: dict[str, Any] | None = None,
) -> dict[str, Any]:
    buckets = _buckets_for_question(project, question, evidence)
    professional_answer = _professional_answer(question, buckets)
    answer = professional_answer["answer"]
    plan_node = plan_node or {}
    task_family = _meta_task_family(question, plan_node)
    selected_skill = _meta_selected_skill(task_family)
    source_plan = _meta_source_plan(question, plan_node, task_family)
    return {
        "id": node_id,
        "level": level,
        "parent_id": parent_id,
        "question": question,
        "current_answer": answer,
        "evidence_buckets": buckets,
        "professional_answer": professional_answer,
        "synthesis": {
            "facts": professional_answer["facts"],
            "inferences": professional_answer["inferences"],
            "judgment": professional_answer["judgment"],
            "gaps": professional_answer["gaps"],
            "confidence": professional_answer["confidence"],
        },
        "rollup_to_parent": _rollup_for_question(question, buckets),
        "next_question_ids": [],
        "status": "open" if professional_answer["facts"] else "needs_data",
        "metadata": {
            "planner_rationale": plan_node.get("rationale", ""),
            "should_drill_down": bool(plan_node.get("should_drill_down", level < project["max_depth"])),
            "should_collect_information": bool(plan_node.get("should_collect_information", level >= project["max_depth"])),
            "terminal_reason": plan_node.get("terminal_reason", ""),
            "information_focus": plan_node.get("information_focus", {}),
            "materiality": _meta_materiality(question, selected_skill),
            "task_family": task_family,
            "selected_skill": selected_skill,
            "source_plan": source_plan,
            "extraction_schema": _meta_extraction_schema(task_family),
            "skill_dispatch_trace": {
                "task_family": task_family,
                "selected_skill": selected_skill,
                "concrete_materials": [item["source_type"] for item in source_plan],
                "skill_output_status": "pending" if level >= project["max_depth"] else "rollup",
                "fallback_used": "",
                "gpt_verification_status": "pending",
            },
        },
    }


def _meta_task_family(question: str, plan_node: dict[str, Any]) -> str:
    text = f"{question} {json.dumps(plan_node.get('information_focus', {}), ensure_ascii=False)}".lower()
    if any(token in text for token in ["估值", "赔率", "pe", "fcf", "dcf", "倍", "市值", "valuation"]):
        return "valuation"
    if any(token in text for token in ["财报", "季报", "年报", "现金流", "毛利", "capex", "rpo", "backlog", "合同负债", "库存", "分部"]):
        return "financial_statement"
    if any(token in text for token in ["研报", "行业报告", "市场空间", "tam", "供需", "价格", "cagr", "第三方"]):
        return "industry_report"
    if any(token in text for token in ["新闻", "消息", "政策", "监管", "事件", "订单", "扩产"]):
        return "news_event"
    if any(token in text for token in ["观点", "专家", "投资者", "访谈", "社媒"]):
        return "opinion"
    if any(token in text for token in ["标的", "证券", "观察清单", "强度", "推荐"]):
        return "target_recommendation"
    return "leaf_research"


def _meta_selected_skill(task_family: str) -> str:
    return {
        "financial_statement": "financial-statement-analysis",
        "valuation": "valuation-analysis",
        "industry_report": "industry-report-analysis",
        "news_event": "news-event-analysis",
        "opinion": "opinion-analysis",
        "target_recommendation": "target-recommendation-analysis",
        "leaf_research": "leaf-research-deepseek",
    }.get(task_family, "leaf-research-deepseek")


def _meta_source_plan(question: str, plan_node: dict[str, Any], task_family: str) -> list[dict[str, str]]:
    focus = plan_node.get("information_focus", {}) if isinstance(plan_node.get("information_focus"), dict) else {}
    preferred = _meta_selected_skill(task_family)
    return [
        {
            "source_bucket": "evidence",
            "source_type": "official filing / earnings release / regulator or exchange document",
            "why_needed": focus.get("evidence", f"用一手证据直接验证“{question}”。"),
            "preferred_skill": preferred if task_family in {"financial_statement", "valuation", "target_recommendation"} else "leaf-research-deepseek",
        },
        {
            "source_bucket": "research_report",
            "source_type": "industry report / sell-side report / third-party dataset",
            "why_needed": focus.get("research_report", f"用第三方模型和数据校验“{question}”。"),
            "preferred_skill": preferred if task_family in {"industry_report", "valuation"} else "industry-report-analysis",
        },
        {
            "source_bucket": "message",
            "source_type": "news / policy update / supply-chain message",
            "why_needed": focus.get("message", f"用消息捕捉“{question}”的最新线索和触发器。"),
            "preferred_skill": "news-event-analysis",
        },
        {
            "source_bucket": "opinion",
            "source_type": "expert view / investor view / interview",
            "why_needed": focus.get("opinion", f"用观点提炼“{question}”的反方质询和待验证假设。"),
            "preferred_skill": "opinion-analysis",
        },
    ]


def _meta_extraction_schema(task_family: str) -> dict[str, Any]:
    common = ["fact", "inference", "judgment", "gap", "trigger", "source_links", "support_refute_or_lead"]
    family_fields = {
        "financial_statement": ["period", "segment_data", "margin", "cash_flow", "capex", "inventory", "backlog_or_rpo"],
        "valuation": ["future_space", "market_snapshot", "priced_in_assumptions", "scenario_table", "valuation_odds"],
        "industry_report": ["market_size", "supply_demand", "price_assumptions", "methodology", "assumptions_to_verify"],
        "news_event": ["event_type", "claim_status", "affected_node", "verification_source", "trigger"],
        "opinion": ["core_claim", "argument_chain", "implicit_assumptions", "counterquestion"],
        "target_recommendation": ["ticker", "thesis_node", "future_space", "valuation_odds", "strength", "downgrade_triggers"],
        "leaf_research": ["selected_materials", "investment_relevance", "uncertainties", "follow_up_data"],
    }.get(task_family, [])
    return {"common_fields": common, "family_specific_fields": family_fields}


def _meta_materiality(question: str, selected_skill: str) -> str:
    return f"本问题必须说明其如何影响上层结论、估值赔率、风险控制或具体标的强度；默认使用 {selected_skill} 进行叶子材料解析。"


def _buckets_for_question(
    project: dict[str, Any],
    question: str,
    evidence: list[EvidenceRecord],
) -> dict[str, list[dict[str, Any]]]:
    buckets = _empty_buckets()
    records = _matching_records(project, question, evidence)
    for record in records[:8]:
        category = record.information_category if record.information_category in buckets else "evidence"
        relation = STANCE_LABEL_ZH.get(_information_stance(record), _information_stance(record))
        buckets[category].append(
            {
                "evidence_id": record.id,
                "relation": relation,
                "point": _truncate_text(_zh_text(record.summary), 96),
                "source_name": record.source_name,
                "url": record.url,
                "summary": _zh_text(record.summary),
                "reliability": record.reliability,
                "materiality": record.materiality,
            }
        )
    return buckets


def _matching_records(project: dict[str, Any], question: str, evidence: list[EvidenceRecord]) -> list[EvidenceRecord]:
    terms = _question_terms(project, question)
    scored: list[tuple[int, EvidenceRecord]] = []
    for record in evidence:
        text = _record_text(record)
        score = sum(1 for term in terms if term and term in text)
        if score >= 2:
            scored.append((score, record))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [record for _score, record in scored]


def _question_terms(project: dict[str, Any], question: str) -> list[str]:
    raw = f"{project.get('object_id', '')} {project.get('meta_question', '')} {question}"
    terms = [term.lower() for term in re.split(r"[\s,，。？?、/：:]+", raw) if len(term) >= 2]
    expansions = {
        "需求": ["demand", "order", "customer", "volume"],
        "利润": ["profit", "margin", "gross", "cash"],
        "竞争": ["competition", "share", "peer", "price"],
        "风险": ["risk", "regulation", "safety", "decline"],
        "事件": ["event", "timeline", "impact", "trigger"],
        "政策": ["policy", "regulation", "tariff"],
    }
    for key, values in expansions.items():
        if key in raw:
            terms.extend(values)
    return list(dict.fromkeys(terms))


def _record_text(record: EvidenceRecord) -> str:
    return " ".join([record.source_type, record.source_name, record.summary, " ".join(record.themes)]).lower()


def _empty_buckets() -> dict[str, list[dict[str, Any]]]:
    return {category: [] for category in SOURCE_ORIGIN_INFO_ORDER}


def _fact_lines_from_buckets(buckets: dict[str, list[dict[str, Any]]]) -> list[str]:
    facts: list[str] = []
    for items in buckets.values():
        for item in items:
            facts.append(f"{item.get('relation', '信息')}：{item.get('point', '')} [{item.get('evidence_id', '')}]")
    return facts


def _professional_answer(question: str, buckets: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    counts = _bucket_counts(buckets)
    support_items, refute_items, lead_items = _bucket_items_by_stance(buckets)
    facts = _fact_lines_from_buckets(buckets)
    answer = _answer_from_bucket_items(question, counts, support_items, refute_items, lead_items)
    judgment = _judgment_from_bucket_items(question, counts, support_items, refute_items, lead_items)
    return {
        "answer": answer,
        "facts": facts[:6],
        "inferences": [_inference_for_question(question, buckets)],
        "supporting_evidence": [_answer_item_line(item) for item in support_items[:4]],
        "refuting_evidence": [_answer_item_line(item) for item in refute_items[:4]],
        "research_leads": [_answer_item_line(item) for item in lead_items[:4]],
        "judgment": judgment,
        "gaps": [_gap_for_question(question, buckets)],
        "next_data": _next_data_for_answer(question, buckets),
        "source_balance": _source_balance(counts, support_items, refute_items, lead_items),
        "confidence": _answer_confidence(counts, support_items, refute_items),
        "rollup": _rollup_for_question(question, buckets),
    }


def _bucket_items_by_stance(
    buckets: dict[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    support: list[dict[str, Any]] = []
    refute: list[dict[str, Any]] = []
    lead: list[dict[str, Any]] = []
    for items in buckets.values():
        for item in items:
            stance = _evidence_stance_class(item.get("relation", ""))
            if stance == "refute":
                refute.append(item)
            elif stance == "lead":
                lead.append(item)
            else:
                support.append(item)
    return support, refute, lead


def _answer_from_bucket_items(
    question: str,
    counts: dict[str, int],
    support_items: list[dict[str, Any]],
    refute_items: list[dict[str, Any]],
    lead_items: list[dict[str, Any]],
) -> str:
    total = sum(counts.values())
    if total == 0:
        return f"当前还不能回答“{question}”。该问题缺少可核验的信息，不能向上层报告输出判断。"

    lead = _truncate_text(_first_point(support_items + refute_items + lead_items), 92)
    if refute_items:
        return (
            f"当前对“{question}”的回答应保持审慎：已有 {total} 条信息，其中存在反证或边界条件。"
            f"核心事实是：{lead}。结论必须先解释这些反向信息，再决定是否上抛。"
        )
    if counts["evidence"] or counts["research_report"]:
        return (
            f"当前对“{question}”可以形成初步专业回答：已有 {total} 条信息，"
            f"其中证据 {counts['evidence']} 条、研报 {counts['research_report']} 条。核心事实是：{lead}。"
            "但仍需要补充缺失信息类别和反证阈值，避免单点来源决定结论。"
        )
    return (
        f"当前对“{question}”只有消息或观点线索，不能形成可上抛判断。"
        f"已有线索指向：{lead}。下一步必须补一手或高可靠第三方来源。"
    )


def _judgment_from_bucket_items(
    question: str,
    counts: dict[str, int],
    support_items: list[dict[str, Any]],
    refute_items: list[dict[str, Any]],
    lead_items: list[dict[str, Any]],
) -> str:
    del support_items, lead_items
    if sum(counts.values()) == 0:
        return "未形成判断。"
    if refute_items:
        return f"“{question}”目前是有反证约束的开放判断，不能直接强化最终结论。"
    if counts["evidence"] and counts["research_report"]:
        return f"“{question}”具备初步证据闭环，可低到中置信上抛。"
    if counts["evidence"] or counts["research_report"]:
        return f"“{question}”有可用研究起点，但还不是完整证据闭环。"
    return f"“{question}”仅能作为研究线索。"


def _first_point(items: list[dict[str, Any]]) -> str:
    for item in items:
        point = _zh_text(item.get("point", "") or item.get("summary", ""))
        if point:
            return point
    return "暂无可摘要事实"


def _answer_item_line(item: dict[str, Any]) -> str:
    source = item.get("source_name", "") or item.get("evidence_id", "")
    relation = item.get("relation", "信息")
    point = _truncate_text(_zh_text(item.get("point", "")), 100)
    evidence_id = item.get("evidence_id", "")
    return f"{relation}：{point}（{source}，{evidence_id}）"


def _next_data_for_answer(question: str, buckets: dict[str, list[dict[str, Any]]]) -> list[str]:
    counts = _bucket_counts(buckets)
    missing = [INFO_CATEGORY_LABEL_ZH[category] for category, count in counts.items() if count == 0]
    if missing:
        return [f"补充{label}来源" for label in missing[:4]]
    if any(token in question for token in ("需求", "出货", "订单", "规模")):
        return ["时间序列数据", "同业对照", "价格和库存口径"]
    if any(token in question for token in ("利润", "毛利", "现金", "价值链")):
        return ["利润率桥接", "现金流桥接", "上下游议价数据"]
    if any(token in question for token in ("事件", "政策", "关税", "监管")):
        return ["官方后续公告", "公司应对动作", "价格/成本传导数据"]
    return ["时间序列", "同业对照", "反证阈值"]


def _source_balance(
    counts: dict[str, int],
    support_items: list[dict[str, Any]],
    refute_items: list[dict[str, Any]],
    lead_items: list[dict[str, Any]],
) -> str:
    return (
        f"信息结构：证据 {counts['evidence']} / 研报 {counts['research_report']} / "
        f"消息 {counts['message']} / 观点 {counts['opinion']}；"
        f"立场结构：支撑 {len(support_items)} / 反证 {len(refute_items)} / 线索 {len(lead_items)}。"
    )


def _answer_confidence(
    counts: dict[str, int],
    support_items: list[dict[str, Any]],
    refute_items: list[dict[str, Any]],
) -> str:
    if sum(counts.values()) == 0:
        return "low"
    if refute_items:
        return "low"
    if counts["evidence"] and counts["research_report"] and len(support_items) >= 2:
        return "medium"
    if counts["evidence"] or counts["research_report"]:
        return "medium"
    return "low"


def _inference_for_question(question: str, buckets: dict[str, list[dict[str, Any]]]) -> str:
    if sum(_bucket_counts(buckets).values()) == 0:
        return f"“{question}”还不能上抛结论，必须先补来源。"
    return f"“{question}”已有信息入口，下一步应区分事实、推论和判断，避免把低可靠消息当成结论。"


def _gap_for_question(question: str, buckets: dict[str, list[dict[str, Any]]]) -> str:
    counts = _bucket_counts(buckets)
    missing = [INFO_CATEGORY_LABEL_ZH[category] for category, count in counts.items() if count == 0]
    if missing:
        return f"需要补充能直接回答“{question}”的{ '、'.join(missing) }。"
    return "需要补时间序列、同业对照、反证阈值和更新触发器。"


def _rollup_for_question(question: str, buckets: dict[str, list[dict[str, Any]]]) -> str:
    if sum(_bucket_counts(buckets).values()) == 0:
        return f"“{question}”尚未形成可上抛结论。"
    return f"“{question}”已有信息支撑，应作为上层结论的可验证分支。"


def _bucket_counts(buckets: dict[str, list[dict[str, Any]]]) -> dict[str, int]:
    return {category: len(buckets.get(category, [])) for category in SOURCE_ORIGIN_INFO_ORDER}


def _apply_custom_questions(
    qa_tree: dict[str, Any],
    project: dict[str, Any],
    custom_questions: list[dict[str, Any]],
    evidence: list[EvidenceRecord],
) -> None:
    nodes = qa_tree["nodes"]
    nodes_by_id = {node["id"]: node for node in nodes}
    for row in custom_questions:
        parent_id = row.get("parent_id") or row.get("requested_parent_id")
        parent = nodes_by_id.get(parent_id)
        if parent is None:
            continue
        node_id = row.get("id") or _custom_question_id(parent_id, row.get("question", ""), set(nodes_by_id))
        if node_id in nodes_by_id:
            continue
        level = min(int(parent.get("level", 0)) + 1, project["max_depth"])
        terminal = bool(row.get("terminal"))
        plan_node = {
            "should_drill_down": False,
            "should_collect_information": True,
            "terminal_reason": "用户标记为终端问题，本层直接进入四类信息搜集。",
        } if terminal else None
        node = _node(node_id, level, parent["id"], row.get("question", ""), project, evidence, plan_node)
        node["status"] = row.get("status", "user_added")
        node["metadata"] = {
            **node.get("metadata", {}),
            "source": "user",
            "created_at": row.get("created_at", ""),
            "should_drill_down": bool(not terminal and level < project["max_depth"]),
            "should_collect_information": bool(terminal or level >= project["max_depth"]),
            "terminal_reason": "用户标记为终端问题，本层直接进入四类信息搜集。" if terminal else node.get("metadata", {}).get("terminal_reason", ""),
        }
        nodes.append(node)
        nodes_by_id[node_id] = node
        parent.setdefault("next_question_ids", [])
        if node_id not in parent["next_question_ids"]:
            parent["next_question_ids"].append(node_id)
        if level < project["max_depth"] and not terminal:
            _append_auto_drilldown_nodes(project, node, nodes, nodes_by_id, evidence)


def _append_auto_drilldown_nodes(
    project: dict[str, Any],
    parent: dict[str, Any],
    nodes: list[dict[str, Any]],
    nodes_by_id: dict[str, dict[str, Any]],
    evidence: list[EvidenceRecord],
) -> None:
    if int(parent.get("level", 0)) >= int(project.get("max_depth", 3)):
        return
    for suffix, suffix_question in L3_DRILLDOWNS:
        node_id = f"{parent['id']}.{suffix}"
        if node_id in nodes_by_id:
            continue
        question = f"{parent['question']}：{suffix_question}"
        child = _node(node_id, int(parent["level"]) + 1, parent["id"], question, project, evidence)
        child["status"] = "auto_drilldown"
        nodes.append(child)
        nodes_by_id[child["id"]] = child
        parent.setdefault("next_question_ids", [])
        if child["id"] not in parent["next_question_ids"]:
            parent["next_question_ids"].append(child["id"])
        _append_auto_drilldown_nodes(project, child, nodes, nodes_by_id, evidence)


def _matching_custom_question(custom_questions: list[dict[str, Any]], requested_parent_id: str, question: str) -> dict[str, Any] | None:
    for row in custom_questions:
        if row.get("requested_parent_id") == requested_parent_id and row.get("question", "").strip() == question:
            return row
    return None


def _custom_question_id(parent_id: str, question: str, existing_ids: set[str]) -> str:
    digest = hashlib.sha1(f"{parent_id}\n{question}".encode("utf-8")).hexdigest()[:10]
    base = f"{parent_id}.custom_{digest}" if parent_id else f"custom_{digest}"
    node_id = base
    index = 2
    while node_id in existing_ids:
        node_id = f"{base}_{index}"
        index += 1
    return node_id


def _apply_linked_evidence(qa_tree: dict[str, Any], evidence: list[EvidenceRecord]) -> None:
    nodes_by_id = {node["id"]: node for node in qa_tree["nodes"]}
    prefix = f"meta_qa:{qa_tree['project_id']}:"
    for record in evidence:
        for link in record.used_in:
            if not link.startswith(prefix):
                continue
            node = nodes_by_id.get(link[len(prefix) :])
            if node is not None:
                _append_record_to_node(node, record)


def _append_record_to_node(node: dict[str, Any], record: EvidenceRecord) -> None:
    buckets = node.setdefault("evidence_buckets", _empty_buckets())
    category = record.information_category if record.information_category in buckets else "evidence"
    if record.id in {item.get("evidence_id") for item in buckets[category]}:
        return
    relation = STANCE_LABEL_ZH.get(_information_stance(record), _information_stance(record))
    item = {
        "evidence_id": record.id,
        "relation": relation,
        "point": _truncate_text(_zh_text(record.summary), 96),
        "source_name": record.source_name,
        "url": record.url,
        "summary": _zh_text(record.summary),
        "reliability": record.reliability,
        "materiality": record.materiality,
    }
    buckets[category].append(item)
    synthesis = node.setdefault("synthesis", {})
    facts = synthesis.setdefault("facts", [])
    fact = f"{relation}：{item['point']} [{record.id}]"
    if fact not in facts:
        facts.append(fact)
    professional_answer = _professional_answer(node["question"], buckets)
    node["professional_answer"] = professional_answer
    node["current_answer"] = professional_answer["answer"]
    node["rollup_to_parent"] = _rollup_for_question(node["question"], buckets)
    synthesis["facts"] = professional_answer["facts"]
    synthesis["inferences"] = professional_answer["inferences"]
    synthesis["judgment"] = professional_answer["judgment"]
    synthesis["gaps"] = professional_answer["gaps"]
    synthesis["confidence"] = professional_answer["confidence"]
    node["status"] = "open"


def _rollup_parent_nodes(qa_tree: dict[str, Any]) -> None:
    nodes_by_id = {node["id"]: node for node in qa_tree["nodes"]}
    for node in sorted(qa_tree["nodes"], key=lambda item: int(item.get("level", 0)), reverse=True):
        child_ids = node.get("next_question_ids", [])
        if not child_ids:
            continue
        children = [nodes_by_id[child_id] for child_id in child_ids if child_id in nodes_by_id]
        if not children:
            continue
        child_rollups = [child.get("rollup_to_parent", "") for child in children if child.get("rollup_to_parent")]
        node["current_answer"] = "；".join(_truncate_text(item, 92) for item in child_rollups[:3]) or node["current_answer"]
        node["rollup_to_parent"] = f"{node['question']}：已由 {len(children)} 个子问题形成初步收敛。"
        node["synthesis"]["facts"] = [
            f"{child.get('question', '')}：{_truncate_text(child.get('current_answer', ''), 100)}"
            for child in children[:4]
        ]
        node["synthesis"]["judgment"] = node["rollup_to_parent"]
        node["synthesis"]["confidence"] = "medium" if any(_has_information(child) for child in children) else "low"


def _has_information(node: dict[str, Any]) -> bool:
    return any(node.get("evidence_buckets", {}).get(category) for category in SOURCE_ORIGIN_INFO_ORDER)


def _attach_information_collection(qa_tree: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for node in qa_tree["nodes"]:
        if not _is_leaf_node(qa_tree, node):
            continue
        collection: dict[str, Any] = {}
        for category in SOURCE_ORIGIN_INFO_ORDER:
            row = _information_collection_row(qa_tree, node, category)
            collection[category] = row
            rows.append(row)
        node["information_collection"] = collection
    return rows


def _is_leaf_node(qa_tree: dict[str, Any], node: dict[str, Any]) -> bool:
    return int(node.get("level", 0)) >= int(qa_tree.get("default_depth", 3)) or not node.get("next_question_ids")


def _information_collection_row(qa_tree: dict[str, Any], node: dict[str, Any], category: str) -> dict[str, Any]:
    items = node.get("evidence_buckets", {}).get(category, [])
    status = "matched" if items else "missing"
    return {
        "project_id": qa_tree["project_id"],
        "node_id": node["id"],
        "parent_id": node.get("parent_id", ""),
        "question": node["question"],
        "category": category,
        "category_label": INFO_CATEGORY_LABEL_ZH.get(category, category),
        "status": status,
        "matched_evidence_ids": [item.get("evidence_id", "") for item in items if item.get("evidence_id")],
        "matched_count": len(items),
        "search_query": _search_query(qa_tree, node, category),
        "next_action": _next_action(category, status),
        "recommended_sources": _collection_recommended_sources(category),
        "acceptance_criteria": _collection_acceptance_criteria(category),
    }


def _search_query(qa_tree: dict[str, Any], node: dict[str, Any], category: str) -> str:
    subject = qa_tree.get("object_id") or qa_tree.get("meta_question", "")
    question = node.get("question", "")
    if category == "evidence":
        return f"{subject} {question} 公告 年报 官方 数据 事实"
    if category == "research_report":
        return f"{subject} {question} 研报 深度报告 行业研究"
    if category == "message":
        return f"{subject} {question} 新闻 消息 进展 未证实"
    return f"{subject} {question} 专家 观点 访谈 大V"


def _next_action(category: str, status: str) -> str:
    if status == "matched":
        return "已匹配本地信息，下一步验证来源质量、口径和反证条件。"
    if category == "evidence":
        return "优先补公告、年报、监管文件、官方数据或可验证事实。"
    if category == "research_report":
        return "补商业研报、卖方报告、行业研究和结构化第三方数据。"
    if category == "message":
        return "补公开消息，但只作为线索，不直接强化结论。"
    return "补专家、产业人士或高质量投资者观点，并保持低权重。"


def _project_evidence_record(
    project: dict[str, Any],
    node_id: str,
    category: str,
    source_type: str,
    source_name: str,
    url: str,
    summary: str,
    reliability: str,
    materiality: str,
    published_at: str | None,
) -> EvidenceRecord:
    cleaned_summary = summary.strip()
    digest = hashlib.sha1(
        f"{project['project_id']}\n{node_id}\n{category}\n{url.strip()}\n{cleaned_summary}".encode("utf-8")
    ).hexdigest()
    return EvidenceRecord.from_dict(
        {
            "id": f"ev_{_safe_id(project['project_id'])}_{digest[:10]}",
            "research_object": f"research/bom/{project['project_id']}",
            "source_type": source_type.strip(),
            "source_name": source_name.strip(),
            "url": url.strip(),
            "published_at": published_at,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "hash": f"sha256:{digest}",
            "tickers": [],
            "sectors": [],
            "themes": ["meta_qa", project["object_type"], category],
            "summary": cleaned_summary,
            "reliability": reliability,
            "materiality": materiality,
            "information_category": category,
            "used_in": [f"meta_qa:{project['project_id']}:{node_id}"],
        }
    )


def _upsert_project_evidence(
    evidence_path: Path,
    record: EvidenceRecord,
    project_id: str,
    node_id: str,
) -> dict[str, Any]:
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    link = f"meta_qa:{project_id}:{node_id}"
    rows: list[dict[str, Any]] = []
    matched: int | None = None
    if evidence_path.exists():
        for line_number, line in enumerate(evidence_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                EvidenceRecord.from_dict(row)
            except (json.JSONDecodeError, ValidationError) as exc:
                raise ValueError(f"{evidence_path}:{line_number}: {exc}") from exc
            if row.get("id") == record.id or (row.get("url") == record.url and row.get("summary") == record.summary):
                matched = len(rows)
            rows.append(row)
    if matched is None:
        with evidence_path.open("a", encoding="utf-8", newline="\n") as file:
            file.write(json.dumps(record.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
        return {"evidence_id": record.id, "created": True, "updated": False}
    used_in = list(rows[matched].get("used_in", []))
    updated = False
    if link not in used_in:
        used_in.append(link)
        rows[matched]["used_in"] = used_in
        updated = True
    if rows[matched].get("information_category") != record.information_category:
        rows[matched]["information_category"] = record.information_category
        updated = True
    if updated:
        _write_jsonl(evidence_path, rows)
    return {"evidence_id": rows[matched].get("id", record.id), "created": False, "updated": updated}


def _render_meta_qa_dashboard(project: dict[str, Any], qa_tree: dict[str, Any]) -> str:
    nodes_by_id = {node["id"]: node for node in qa_tree["nodes"]}
    root = nodes_by_id["meta.root"]
    plan_summary = _render_question_plan_summary(qa_tree)
    l1_cards = "\n".join(_render_dashboard_l1_card(nodes_by_id[node_id], nodes_by_id) for node_id in root["next_question_ids"])
    add_question = _render_add_question_box(project["project_id"], "L0 元问题", "meta.root")
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(project["project_id"])} 层级 QA 研究系统</title>
  <style>{_apple_research_css()}{_qa_explorer_css()}</style>
</head>
<body>
  <header>
    <p class="eyebrow">META QA / {escape(_object_type_label(project["object_type"]))}</p>
    <h1>{escape(project["meta_question"])}</h1>
    <p class="subtitle">系统先扩展问题树，再在叶子问题搜集证据、研究报告、消息和观点，最后逐层上抛形成报告。</p>
    <div class="summary-strip">
      <div class="metric"><span>对象</span><strong>{escape(project["object_id"] or project["object_type"])}</strong></div>
      <div class="metric"><span>最大下钻</span><strong>L{escape(str(project["max_depth"]))}</strong></div>
      <div class="metric"><span>问题节点</span><strong>{len(qa_tree["nodes"])}</strong></div>
      <div class="metric"><span>叶子问题</span><strong>{sum(1 for node in qa_tree["nodes"] if _is_leaf_node(qa_tree, node))}</strong></div>
    </div>
  </header>
  <nav class="nav">
    <a href="#meta-question">元问题</a>
    <a href="#question-plan">问题规划</a>
    <a href="#questions">子问题</a>
    <a href="research_report.html">聚合报告</a>
    <a href="#add-question">新增问题</a>
  </nav>
  <main class="qa-full-research">
    <section id="meta-question">
      <p class="eyebrow">当前要研究的问题</p>
      <h2>{escape(project["meta_question"])}</h2>
      <div class="rule-box"><p>{escape(root["current_answer"])}</p></div>
    </section>
    <section id="question-plan">
      <p class="eyebrow">问题规划</p>
      <h2>系统为什么这样下钻</h2>
      {plan_summary}
    </section>
    <section id="questions">
      <p class="eyebrow">系统扩展出的 L1 问题</p>
      <h2>子问题列表</h2>
      <div class="l2-grid">{l1_cards}</div>
    </section>
    {add_question}
  </main>
  <script>{_draft_question_js()}</script>
</body>
</html>
"""


def _render_dashboard_l1_card(node: dict[str, Any], nodes_by_id: dict[str, dict[str, Any]]) -> str:
    children = [nodes_by_id[child_id] for child_id in node.get("next_question_ids", []) if child_id in nodes_by_id]
    child_items = "".join(f"<li>{escape(child['question'])}</li>" for child in children[:4]) or "<li>暂无子问题。</li>"
    rationale = node.get("metadata", {}).get("planner_rationale", "")
    return (
        '<article class="l2-card">'
        '<p class="eyebrow">L1 问题</p>'
        f"<h3>{escape(node['question'])}</h3>"
        f"<div class=\"field\"><b>规划依据</b><p>{escape(rationale or '按元问题拆出的一级研究主线。')}</p></div>"
        f"<div class=\"field\"><b>子结构汇总结论</b><p>{escape(_truncate_text(node.get('current_answer', ''), 180))}</p></div>"
        f"<div class=\"field\"><b>子问题列表</b><ul>{child_items}</ul></div>"
        f"<div class=\"field\"><b>信息覆盖</b>{_category_meter(node)}</div>"
        "</article>"
    )


def _render_question_plan_summary(qa_tree: dict[str, Any]) -> str:
    plan = qa_tree.get("question_plan", {})
    rationale = plan.get("planner_rationale", "系统按对象类型、元问题和默认三层深度生成问题树。")
    signals = "、".join(plan.get("detected_signals", [])) or "未识别到特殊信号"
    l1_items = []
    for l1 in plan.get("l1", []):
        l2_count = len(l1.get("l2", []))
        leaf_count = sum(len(l2.get("l3", [])) or 1 for l2 in l1.get("l2", [])) or 1
        l1_items.append(
            "<li>"
            f"<strong>{escape(l1.get('question', ''))}</strong>"
            f"<p class=\"note\">{escape(l1.get('rationale', ''))} · L2 {l2_count} 个 · 叶子问题 {leaf_count} 个</p>"
            "</li>"
        )
    return (
        '<div class="rule-box">'
        f"<p>{escape(rationale)}</p>"
        f"<p class=\"note\">规划模式：{escape(plan.get('planning_mode', ''))} · 识别信号：{escape(signals)}</p>"
        "</div>"
        f"<div class=\"field\"><b>L1 规划结果</b><ul>{''.join(l1_items)}</ul></div>"
    )


def _render_meta_qa_report(project: dict[str, Any], qa_tree: dict[str, Any]) -> str:
    nodes_by_id = {node["id"]: node for node in qa_tree["nodes"]}
    root = nodes_by_id["meta.root"]
    l1_sections = "\n".join(_render_report_l1_section(nodes_by_id[node_id], nodes_by_id) for node_id in root["next_question_ids"])
    priority = _render_priority_leaf_questions(qa_tree)
    plan_summary = _render_question_plan_summary(qa_tree)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(project["project_id"])} 专业研究报告</title>
  <style>{_apple_research_css()}{_qa_explorer_css()}</style>
</head>
<body>
  <header>
    <p class="eyebrow">PROFESSIONAL QA REPORT</p>
    <h1>{escape(project["meta_question"])}</h1>
    <p class="subtitle">本报告由层级 QA 树收敛生成。结论只来自已映射的信息和显式缺口，不构成交易指令。</p>
  </header>
  <nav class="nav">
    <a href="research_dashboard.html">返回工作台</a>
    <a href="#summary">摘要</a>
    <a href="#plan">问题规划</a>
    <a href="#priority">优先补证</a>
    <a href="#sections">逐层收敛</a>
  </nav>
  <main class="qa-full-research">
    <section id="summary">
      <p class="eyebrow">一页摘要</p>
      <h2>当前结论</h2>
      <div class="rule-box"><p>{escape(root.get("current_answer", ""))}</p></div>
      <div class="summary-strip">
        <div class="metric"><span>对象类型</span><strong>{escape(_object_type_label(project["object_type"]))}</strong></div>
        <div class="metric"><span>问题节点</span><strong>{len(qa_tree["nodes"])}</strong></div>
        <div class="metric"><span>叶子问题</span><strong>{sum(1 for node in qa_tree["nodes"] if _is_leaf_node(qa_tree, node))}</strong></div>
        <div class="metric"><span>信息覆盖</span><strong>{escape(_coverage_ratio(qa_tree))}</strong></div>
      </div>
    </section>
    <section id="plan">
      <p class="eyebrow">问题规划</p>
      <h2>从元问题到子问题的拆解依据</h2>
      {plan_summary}
    </section>
    <section id="priority">
      <p class="eyebrow">下一步数据</p>
      <h2>最需要优先验证的问题</h2>
      <div class="l2-grid">{priority}</div>
    </section>
    <section id="sections">
      <p class="eyebrow">逐层收敛</p>
      <h2>L1 到叶子问题</h2>
      {l1_sections}
    </section>
  </main>
</body>
</html>
"""


def _render_report_l1_section(node: dict[str, Any], nodes_by_id: dict[str, dict[str, Any]]) -> str:
    l2_cards: list[str] = []
    for child_id in node.get("next_question_ids", []):
        child = nodes_by_id.get(child_id)
        if child is None:
            continue
        leaves = [nodes_by_id[leaf_id] for leaf_id in child.get("next_question_ids", []) if leaf_id in nodes_by_id]
        leaf_items = "".join(
            f"<li><strong>{escape(leaf['question'])}</strong>{_leaf_quality_trace(leaf)}{_render_professional_answer_summary(leaf)}{_category_meter(leaf)}{_leaf_source_refs(leaf)}</li>"
            for leaf in leaves
        )
        l2_cards.append(
            '<article class="l2-card">'
            f"<h3>{escape(child['question'])}</h3>"
            f"<div class=\"field\"><b>L2 收敛</b><p>{escape(_truncate_text(child.get('current_answer', ''), 180))}</p></div>"
            f"<div class=\"field\"><b>L3 叶子问题</b><ul>{leaf_items}</ul></div>"
            "</article>"
        )
    return (
        '<section class="level-frame">'
        f"<p class=\"eyebrow\">L1 收敛</p><h2>{escape(node['question'])}</h2>"
        f"<div class=\"field\"><b>规划依据</b><p>{escape(node.get('metadata', {}).get('planner_rationale', ''))}</p></div>"
        f"<div class=\"rule-box\"><p>{escape(_truncate_text(node.get('current_answer', ''), 240))}</p></div>"
        f"<div class=\"l2-grid\">{''.join(l2_cards)}</div>"
        "</section>"
    )


def _leaf_quality_trace(node: dict[str, Any]) -> str:
    metadata = node.get("metadata", {}) or {}
    selected_skill = metadata.get("selected_skill", "")
    materiality = metadata.get("materiality", "")
    source_plan = metadata.get("source_plan", []) if isinstance(metadata.get("source_plan"), list) else []
    source_labels = [
        f"{item.get('source_bucket', '')}:{item.get('preferred_skill', '')}"
        for item in source_plan[:4]
        if isinstance(item, dict)
    ]
    parts = []
    if selected_skill:
        parts.append(f"解析 skill：{selected_skill}")
    if source_labels:
        parts.append("资料规划：" + " / ".join(source_labels))
    if materiality:
        parts.append(f"重要性：{_truncate_text(materiality, 110)}")
    if not parts:
        return ""
    return "<p class=\"note\">" + escape("；".join(parts)) + "</p>"


def _leaf_source_refs(node: dict[str, Any]) -> str:
    refs: list[str] = []
    for category in SOURCE_ORIGIN_INFO_ORDER:
        for item in node.get("evidence_buckets", {}).get(category, [])[:3]:
            source = item.get("source_name", "")
            evidence_id = item.get("evidence_id", "")
            if source or evidence_id:
                refs.append(f"{source or evidence_id} [{evidence_id}]")
    if not refs:
        return ""
    return "<p class=\"note\">来源：" + "；".join(escape(ref) for ref in refs[:4]) + "</p>"


def _render_professional_answer_summary(node: dict[str, Any]) -> str:
    answer = node.get("professional_answer", {})
    if not answer:
        return f"<p>{escape(_truncate_text(node.get('current_answer', ''), 160))}</p>"
    support = _render_answer_list(answer.get("supporting_evidence", []), "暂无支撑证据。", limit=2)
    refute = _render_answer_list(
        answer.get("refuting_evidence", []) or answer.get("research_leads", []),
        "暂无反证或线索。",
        limit=2,
    )
    next_data = _render_answer_list(answer.get("next_data", []), "暂无下一步数据。", limit=3)
    return (
        '<div class="decision-panel">'
        '<div class="decision-head"><b>专业回答</b>'
        f"<span>{escape(_confidence_label(answer.get('confidence', 'low')))}</span></div>"
        '<div class="decision-grid">'
        f"<div class=\"decision-box judgment\"><h4>当前回答</h4><p>{escape(answer.get('answer', ''))}</p></div>"
        f"<div class=\"decision-box\"><h4>支撑信息</h4>{support}</div>"
        f"<div class=\"decision-box\"><h4>反证/线索</h4>{refute}</div>"
        f"<div class=\"decision-box\"><h4>下一步数据</h4>{next_data}<p class=\"note\">{escape(answer.get('source_balance', ''))}</p></div>"
        "</div>"
        "</div>"
    )


def _render_answer_list(items: list[str], empty: str, limit: int) -> str:
    values = [item for item in items if item]
    if not values:
        return f"<p class=\"note\">{escape(empty)}</p>"
    return "<ul>" + "".join(f"<li>{escape(_truncate_text(item, 120))}</li>" for item in values[:limit]) + "</ul>"


def _confidence_label(confidence: str) -> str:
    labels = {"high": "高置信", "medium": "中置信", "low": "低置信"}
    return labels.get(confidence, confidence)


def _render_priority_leaf_questions(qa_tree: dict[str, Any]) -> str:
    leaves = [node for node in qa_tree["nodes"] if _is_leaf_node(qa_tree, node)]
    leaves.sort(key=lambda node: sum(_bucket_counts(node.get("evidence_buckets", {})).values()))
    cards = []
    for node in leaves[:6]:
        cards.append(
            '<article class="l2-card">'
            f"<p class=\"eyebrow\">L{escape(str(node.get('level', '')))} 待验证</p>"
            f"<h3>{escape(node['question'])}</h3>"
            f"{_render_professional_answer_summary(node)}"
            f"<div class=\"field\"><b>缺口</b><p>{escape(_truncate_text(node.get('synthesis', {}).get('gaps', [''])[0], 120))}</p></div>"
            f"{_category_meter(node)}"
            "</article>"
        )
    return "".join(cards)


def _category_meter(node: dict[str, Any]) -> str:
    counts = _bucket_counts(node.get("evidence_buckets", {}))
    pills = []
    for category in SOURCE_ORIGIN_INFO_ORDER:
        count = counts.get(category, 0)
        css = "filled" if count else "warning" if category == "evidence" else ""
        pills.append(
            f"<span class=\"category-pill {escape(css)}\">{escape(INFO_CATEGORY_LABEL_ZH[category])} <strong>{escape(str(count))}</strong></span>"
        )
    return f"<div class=\"category-meter\">{''.join(pills)}</div>"


def _coverage_ratio(qa_tree: dict[str, Any]) -> str:
    leaves = [node for node in qa_tree["nodes"] if _is_leaf_node(qa_tree, node)]
    if not leaves:
        return "0%"
    covered = sum(1 for node in leaves if _has_information(node))
    return f"{covered}/{len(leaves)}"


def _object_type_label(object_type: str) -> str:
    labels = {
        "company": "公司",
        "industry": "行业",
        "event": "事件",
        "custom": "自定义",
    }
    return labels.get(object_type, object_type)
