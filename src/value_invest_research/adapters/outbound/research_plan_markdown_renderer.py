from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from value_invest_research.domain.research_plan import validate_research_plan_execution


LENS_LABELS = {
    "demand": "需求侧",
    "supply": "供给侧",
    "technology": "技术侧",
    "valuation": "估值侧",
    "esg": "ESG",
}

LENS_DISPLAY_QUESTIONS = {
    "demand": "真实 AI 工作负载能否转化为算力需求、客户预算、订单和利润？",
    "supply": "先进晶圆、HBM/封装、系统集成与机房约束后，最终可交付供给能否跟上？",
    "technology": "GPU 与 ASIC 在工作负载、性能/TCO、软件生态和客户采用上谁更具优势？",
    "valuation": "盈利增长是否超过市场共识与股价隐含预期，并提供可监控的赔率？",
    "esg": "能源、管制、集中度、治理与融资约束是否改变可交付能力和股东回报？",
}

class ResearchPlanMarkdownRenderer:
    """Render the runtime-growing question hierarchy and active terminal work."""

    def render(
        self,
        *,
        project: dict[str, Any],
        bundle: dict[str, Any],
    ) -> str:
        plans = [row for row in bundle.get("plans") or [] if isinstance(row, dict)]
        events_by_node = dict(bundle.get("events_by_node") or {})
        qa_nodes = [
            row
            for row in (bundle.get("qa_tree") or {}).get("nodes") or []
            if isinstance(row, dict)
        ]
        qa_by_id = {
            str(row.get("id") or ""): row for row in qa_nodes
        }
        title = str(project.get("title") or project.get("topic") or "投资研究")
        report_date = str(
            project.get("report_date") or project.get("as_of_date") or ""
        )
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for plan in plans:
            grouped[str(plan.get("lens_id") or "other")].append(plan)
        l3_title_by_id = {
            str(plan.get("l3_node_id") or ""): str(
                plan.get("l3_title") or plan.get("l3_node_id") or ""
            )
            for plan in plans
            if str(plan.get("l3_node_id") or "")
        }

        lines = [
            "<!-- research-plan-contract: dynamic-question-tree-v4 -->",
            f"# {title}研究计划",
            "",
            f"> 截面：{report_date or '未指定'}｜初始只到 L3｜最多下钻到 L5。",
            "> 先研究当前最深问题；只有证据门槛未通过并形成明确缺口时，才新增下一层。",
            "> 每个当前问题单独搜索、挂接、抽取和复核；宽泛材料池只提供候选，不能直接完成问题。",
            "",
        ]

        l1_nodes = [row for row in qa_nodes if int(row.get("level") or 0) == 1]
        if l1_nodes:
            lines.extend(["## L1 · 顶层问题", ""])
            for position, node in enumerate(l1_nodes, start=1):
                child_labels = [
                    _qa_node_label(qa_by_id.get(str(child_id)) or {})
                    for child_id in node.get("next_question_ids") or []
                ]
                lines.extend(
                    [
                        f"{position}. **{node.get('question') or ''}**",
                        (
                            "   - L2："
                            f"{'；'.join(child_labels) or '见下文'}"
                        ),
                    ]
                )
            lines.append("")

        ordered_lenses = [
            *[lens for lens in LENS_LABELS if lens in grouped],
            *[lens for lens in grouped if lens not in LENS_LABELS],
        ]
        l3_counter = 0
        leaf_counter = 0
        for lens_position, lens_id in enumerate(ordered_lenses, start=1):
            lens_plans = grouped[lens_id]
            l2_node = _lens_parent_node(qa_nodes, lens_id)
            lines.extend(
                [
                    f"## {lens_position}. L2 · {LENS_LABELS.get(lens_id, _qa_node_label(l2_node) or lens_id or '其他')}",
                    "",
                    f"**问题：** {LENS_DISPLAY_QUESTIONS.get(lens_id) or l2_node.get('question') or '需要回答下列 L3 研究问题。'}",
                    "",
                ]
            )
            for plan_position, plan in enumerate(lens_plans, start=1):
                l3_counter += 1
                execution = validate_research_plan_execution(
                    plan,
                    list(events_by_node.get(str(plan.get("l3_node_id") or ""), [])),
                )
                lines.extend(
                    [
                        f"### {lens_position}.{plan_position} L3 · {plan.get('l3_title') or plan.get('l3_node_id') or ''}",
                        "",
                        f"<!-- l3-plan-id:{plan.get('plan_id') or ''} -->",
                        f"**问题：** {plan.get('l3_question') or ''}",
                        (
                            "**进度：** "
                            f"{execution.get('summary', {}).get('completed', 0)} / "
                            f"{execution.get('summary', {}).get('steps', 0)} 个当前终端问题完成"
                        ),
                        "",
                    ]
                )
                root = plan.get("question_tree") or {}
                trigger_gaps = list(
                    (root.get("expansion_trigger") or {}).get("evidence_gaps") or []
                )
                if trigger_gaps:
                    lines.extend(
                        [
                            "**下钻原因：** "
                            + "；".join(str(item).rstrip("。；") for item in trigger_gaps)
                            + "。",
                            "",
                        ]
                    )
                children = list(root.get("children") or [])
                if children:
                    rendered, leaves = _render_children(
                        children,
                        l3_title_by_id=l3_title_by_id,
                        indent=0,
                    )
                else:
                    rendered, leaves = _render_terminal_execution(root, indent=0)
                leaf_counter += leaves
                lines.extend(rendered)
                lines.append("")

        lines.extend(
            [
                "## 执行与验收规则",
                "",
                "1. 初始计划只含 L1、L2、L3；搜索从当前最深未回答问题发起。",
                "2. 先搜集并分析；能回答就结束该分支，不能回答才把具体缺口变成下一层问题。",
                "3. 同一材料跨问题复用时，仍须按问题分别挂接、抽取和复核。",
                "4. 不允许为了显得完整而预生成 L4/L5；每次只新增一层，且不得超过 L5。",
                "",
                f"> 计划覆盖：{l3_counter} 个 L3 问题，{leaf_counter} 个当前终端问题。",
                "",
            ]
        )
        return "\n".join(lines)


def _render_children(
    children: list[dict[str, Any]],
    *,
    l3_title_by_id: dict[str, str],
    indent: int,
) -> tuple[list[str], int]:
    lines: list[str] = []
    leaf_count = 0
    prefix = "   " * indent
    detail_prefix = "   " * (indent + 1)
    for position, node in enumerate(children, start=1):
        if not isinstance(node, dict):
            continue
        level = int(node.get("level") or 0)
        question_id = str(node.get("question_id") or "")
        grandchildren = [
            row for row in node.get("children") or [] if isinstance(row, dict)
        ]
        role = "子问题" if grandchildren else "当前问题"
        lines.append(
            f"{prefix}{position}. **L{level} {role} · {node.get('title') or ''}：** "
            f"{_compact_question(node, l3_title_by_id=l3_title_by_id)}"
        )
        if grandchildren:
            nested, nested_leaves = _render_children(
                grandchildren,
                l3_title_by_id=l3_title_by_id,
                indent=indent + 1,
            )
            lines.extend(nested)
            leaf_count += nested_leaves
            continue

        leaf_count += 1
        execution_lines, _ = _render_terminal_execution(node, indent=indent + 1)
        lines.extend(execution_lines)
    return lines, leaf_count


def _render_terminal_execution(
    node: dict[str, Any],
    *,
    indent: int,
) -> tuple[list[str], int]:
    prefix = "   " * indent
    question_id = str(node.get("question_id") or "")
    return (
        [
            f"{prefix}<!-- active-question-id:{question_id} -->",
            f"{prefix}- **需要搜集的数据：** {_leaf_execution_text(node, field='required_data')}",
            f"{prefix}- **需要做的分析：** {_leaf_execution_text(node, field='analysis_plan')}",
        ],
        1,
    )


def _compact_question(
    node: dict[str, Any],
    *,
    l3_title_by_id: dict[str, str],
) -> str:
    question = str(node.get("question") or "").strip()
    title = str(node.get("title") or "").strip()
    dimension = str(node.get("research_dimension") or "").strip()

    if question.startswith("要回答“") and "每个核心指标的可验证状态" in question:
        return "哪些关键事实决定父问题？"
    if question == "关键事实为什么会改变父问题的答案，并如何传导到下游和财务结果？":
        return "事实如何形成因果，并传导到下游与财务？"
    if dimension == "indicator" and question.startswith("围绕“"):
        return f"{title}如何定义和衡量？当前、历史与前瞻如何？"

    for node_id, node_title in sorted(
        l3_title_by_id.items(), key=lambda item: len(item[0]), reverse=True
    ):
        question = question.replace(node_id, f"“{node_title}”")

    support_match = re.fullmatch(
        r"支持条件“(.+?)。?”是否有直接因果证据，而非只有相关性？",
        question,
    )
    if support_match:
        return f"能否用直接证据验证：{support_match.group(1)}？"

    refute_match = re.fullmatch(
        r"哪些证据会满足反证条件“(.+?)。?”，从而推翻、削弱或限定父问题的答案？",
        question,
    )
    if refute_match:
        return f"哪些证据将支持“{refute_match.group(1)}”，从而削弱父结论？"
    return question


def _leaf_execution_text(node: dict[str, Any], *, field: str) -> str:
    dimension = str(node.get("research_dimension") or "").strip()
    question = str(node.get("question") or "").strip()
    title = str(node.get("title") or "").strip()

    if node.get("expansion_trigger"):
        return _join_items(node.get(field))

    if dimension == "indicator" and question.startswith("围绕“"):
        if field == "required_data":
            return (
                f"{title}的当前值、历史与前瞻；定义、单位、样本、"
                "事实期/预测期、原文位置及缺口"
            )
        return "统一口径，判断趋势与拐点；区分事实、指引和第三方预测"
    if dimension == "mechanism":
        if field == "required_data":
            return "因果链直接证据；客户、供应商或竞争者交叉证据；适用对象、时间、边界和原文位置"
        return "排除相关性和替代解释；判断支持、边界或未决"
    if dimension == "financial_bridge":
        if field == "required_data":
            return "下游节点与公司桥接字段；数量、价格、份额、利润和现金流连接；公司/分部、期间、口径和原文位置"
        return "建立业务量到收入、利润和现金流的可复算桥；测试三种情景与敏感假设"
    if dimension == "refutation":
        if field == "required_data":
            return "同口径反向指标、取消/延期/替代/监管事实；可信反方假设；失效阈值、期限、频率和原文位置"
        return "比较正反证据的直接性、时效与解释力；判断推翻、削弱、边界或未决"
    return _join_items(node.get(field))


def _join_items(value: Any) -> str:
    if isinstance(value, list):
        return "；".join(str(item).strip() for item in value if str(item).strip()) or "待定义"
    text = str(value or "").strip()
    return text or "待定义"


def _lens_parent_node(
    qa_nodes: list[dict[str, Any]],
    lens_id: str,
) -> dict[str, Any]:
    candidates = {lens_id, f"lens.{lens_id}"}
    return next(
        (
            row
            for row in qa_nodes
            if int(row.get("level") or 0) in {1, 2}
            and str(row.get("id") or "") in candidates
        ),
        {},
    )


def _qa_node_label(node: dict[str, Any]) -> str:
    node_id = str(node.get("id") or "")
    if node_id.startswith("lens."):
        return LENS_LABELS.get(node_id.split(".", 1)[1], node_id)
    question = str(node.get("question") or "")
    return question.split("：", 1)[0].strip() or node_id
