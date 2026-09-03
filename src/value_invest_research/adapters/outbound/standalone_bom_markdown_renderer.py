from __future__ import annotations

from pathlib import Path
from typing import Any


MATERIAL_LABELS = {
    "official_filing": "官方财报",
    "official_company": "官方公司",
    "sell_side_research": "研报",
    "authoritative_third_party": "第三方权威",
    "market_news": "市场消息",
    "expert_opinion": "专家观点",
    "other": "其他",
}

DEMAND_INFORMATION_TYPE_LABELS = {
    "official_filing": "官方财报",
    "authoritative_third_party": "第三方研究",
    "sell_side_research": "机构研报",
    "official_company": "市场消息",
    "market_news": "市场消息",
    "expert_opinion": "市场消息",
    "other": "市场消息",
}

DIRECTION_LABELS = {
    "support": "支持",
    "refute": "反证",
    "boundary": "改变边界",
    "constraint": "新增约束",
    "new_branch": "新增分支",
    "conflict": "证据冲突",
    "unresolved": "暂未判断",
    "neutral": "线索",
    "unmapped": "不映射",
}

CLAIM_IMPACT_LABELS = {
    "support": "增强",
    "refute": "减弱",
    "boundary": "改变边界",
    "constraint": "新增约束",
    "new_branch": "新增分支",
    "conflict": "冲突",
    "unresolved": "待判断",
    "neutral": "线索",
    "unmapped": "不映射",
}


class StandaloneBomMarkdownRenderer:
    """Render one five-lens BOM timeline without exposing process artifacts."""

    def __init__(self, project_dir: Path | None = None):
        self.project_dir = project_dir.resolve() if project_dir else None

    def render(self, view: dict[str, Any]) -> str:
        front_matter = [
            "---",
            "report_scope: standalone-bom",
            f"bom_node_id: {view['bom_node_id']}",
            f"as_of_date: {view['as_of_date']}",
        ]
        if view.get("investment_engine_version"):
            front_matter.append(
                f"investment_engine_version: {view['investment_engine_version']}"
            )
        logic_chain_centered = (
            str(view.get("research_model") or "") == "logic_chain_centered"
        )
        if logic_chain_centered:
            front_matter.extend(
                [
                    "research_model: logic-chain-centered",
                    f"logic_chain_version: {view.get('logic_chain_version') or ''}",
                ]
            )
        lines = [
            *front_matter,
            "---",
            "",
            f"# {view['title']}",
            "",
            (
                f"> 研究截面：{view['as_of_date']}。时间线按材料发布时间由近及远；"
                "同一材料只有经过当前问题的独立解析和复核后，才进入该问题。"
            ),
            "",
        ]
        if view.get("investment_engine_version"):
            lines.extend(_investment_snapshot_lines(view))
        for index, lens in enumerate(view["lenses"], start=1):
            lines.extend(
                [
                    f"## {index}. {lens['label']}",
                    "",
                    (
                        "### 第一性原理逻辑链"
                        if logic_chain_centered
                        else "### 简单逻辑链"
                    ),
                    "",
                    lens["logic_chain"] or "当前逻辑链尚未定义。",
                    "",
                ]
            )
            logic_nodes = list(lens.get("logic_nodes") or [])
            if logic_nodes:
                if logic_chain_centered:
                    lines.extend(["### 逻辑节点与原子观点材料", ""])
                    for position, node in enumerate(
                        lens.get("causal_nodes") or [], start=1
                    ):
                        lines.extend(
                            _logic_chain_node_lines(
                                node,
                                position=position,
                                project_dir=self.project_dir,
                            )
                        )
                    derived_views = list(lens.get("derived_views") or [])
                    if derived_views:
                        lines.extend(["### 派生证据视图", ""])
                        for node in derived_views:
                            lines.extend(
                                _logic_node_lines(
                                    node,
                                    project_dir=self.project_dir,
                                )
                            )
                else:
                    lines.extend(["### 逻辑节点与公司信息", ""])
                    for node in logic_nodes:
                        lines.extend(
                            _logic_node_lines(node, project_dir=self.project_dir)
                        )
            else:
                lines.extend(
                    [
                        "### 信息时间线",
                        "",
                        "| 时间 | 信息类型 | Source | 观点列表 |",
                        "|---|---|---|---|",
                    ]
                )
                claims = lens.get("claims") or []
                if claims:
                    lines.extend(
                        _source_claim_row(
                            group,
                            project_dir=self.project_dir,
                        )
                        for group in _group_claims_by_source(claims)
                    )
                else:
                    lines.append(
                        f"| {view['as_of_date']} | 其他 | 无 | "
                        "尚无经过问题化解析和复核的材料。 |"
                    )
        return "\n".join(lines).rstrip() + "\n"


def _source_claim_row(
    group: dict[str, Any],
    *,
    project_dir: Path | None,
) -> str:
    title = _escape_cell(
        str(group.get("source_title") or group.get("source_id") or "来源")
    )
    url = str(group.get("source_url") or "").strip()
    url = _rendered_source_url(url, project_dir=project_dir)
    source = f"[{title}]({_markdown_link_target(url)})" if url else title
    viewpoints = []
    for index, claim in enumerate(group.get("claims") or [], start=1):
        location = _escape_cell(
            str(claim.get("source_location") or "").strip()
        )
        statement = _escape_cell(str(claim.get("statement") or ""))
        label = f"观点 {index}"
        if location:
            label += f"（{location}）"
        mappings = [
            (
                str(row.get("logic_node_title") or row.get("logic_node_id") or ""),
                DIRECTION_LABELS.get(
                    str(row.get("direction") or "neutral"),
                    "线索",
                ),
            )
            for row in sorted(
                claim.get("logic_mappings") or [],
                key=lambda item: (
                    0
                    if str(item.get("mapping_role") or "") == "primary"
                    else 1,
                    str(item.get("logic_node_id") or ""),
                ),
            )
        ]
        mapping_text = ""
        if mappings:
            mapping_text = "；映射：" + " / ".join(
                f"{_escape_cell(title)}（{_escape_cell(direction)}）"
                for title, direction in mappings
            )
        viewpoints.append(f"• **{label}**：{statement}{mapping_text}")
    return (
        f"| {_escape_cell(str(group.get('published_at') or ''))} "
        f"| {MATERIAL_LABELS.get(str(group.get('material_class') or ''), '其他')} "
        f"| {source} "
        f"| {'<br>'.join(viewpoints)} |"
    )


def _group_claims_by_source(
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for claim in claims:
        source_id = str(claim.get("source_id") or "")
        if source_id not in grouped:
            grouped[source_id] = {
                "source_id": source_id,
                "published_at": claim.get("published_at"),
                "material_class": claim.get("material_class"),
                "source_title": claim.get("source_title"),
                "source_url": claim.get("source_url"),
                "claims": [],
            }
            order.append(source_id)
        grouped[source_id]["claims"].append(claim)
    return [grouped[source_id] for source_id in order]


def _escape_cell(value: str) -> str:
    return " ".join(value.replace("|", "\\|").splitlines()).strip()


def _rendered_source_url(url: str, *, project_dir: Path | None) -> str:
    if not url or project_dir is None:
        return url
    if url.startswith(("http://", "https://", "/")):
        return url
    return str((project_dir / url).resolve())


def _markdown_link_target(url: str) -> str:
    if url.startswith("/"):
        return f"<{url}>"
    return url


def _investment_snapshot_lines(view: dict[str, Any]) -> list[str]:
    decision = dict(view.get("decision") or {})
    coverage = dict(view.get("engine_coverage") or {})
    stored_summary = str(decision.get("summary") or "")
    logic_chain_judgment = str(
        view.get("logic_chain_judgment") or stored_summary
    )
    lines = [
        "### 当前投资判断",
        "",
        f"**动作状态：** {decision.get('action_state', 'watch_only')}",
        "",
        logic_chain_judgment,
        "",
    ]
    if stored_summary and stored_summary != logic_chain_judgment:
        lines.extend([f"**本期证据变化：** {stored_summary}", ""])
    lines.extend([
        "| 基本面变化 | 市场共识变化 | 定价变化 |",
        "|---|---|---|",
        (
            f"| {_escape_cell(str(decision.get('fundamental_delta') or '待验证'))} "
            f"| {_escape_cell(str(decision.get('consensus_delta') or '待验证'))} "
            f"| {_escape_cell(str(decision.get('priced_in_delta') or '待验证'))} |"
        ),
        "",
        (
            f"**研究覆盖：** {coverage.get('state_nodes', 0)} / "
            f"{coverage.get('logic_nodes', 0)} 个逻辑节点已有截面；"
            f"{coverage.get('mapped_claims', 0)} / "
            f"{coverage.get('total_claims', 0)} 条原子观点完成映射。"
        ),
        "",
        "#### 公司影响、预期差与动作",
        "",
        "| 公司 | 敞口 | 盈利传导 | 市场定价 | 当前结论 | 动作 |",
        "|---|---|---|---|---|---|",
    ])
    impacts = list(decision.get("company_impacts") or [])
    if impacts:
        for row in impacts:
            company = str(row.get("company") or "")
            ticker = str(row.get("ticker") or "")
            if ticker:
                company += f"（{ticker}）"
            lines.append(
                f"| {_escape_cell(company)} "
                f"| {_escape_cell(str(row.get('exposure') or ''))} "
                f"| {_escape_cell(str(row.get('earnings_bridge') or ''))} "
                f"| {_escape_cell(str(row.get('priced_in') or ''))} "
                f"| {_escape_cell(str(row.get('conclusion') or ''))} "
                f"| {_escape_cell(str(row.get('action_state') or 'watch_only'))} |"
            )
    else:
        lines.append("| 尚无 | - | - | - | 尚未通过公司财务桥与估值门槛 | watch_only |")
    lines.append("")
    return lines


def _logic_node_row(node: dict[str, Any]) -> str:
    return (
        f"| {_escape_cell(str(node.get('title') or ''))} "
        f"| {_escape_cell(str(node.get('state') or 'unresolved'))} "
        f"| {_escape_cell(str(node.get('conclusion') or ''))} "
        f"| {_escape_cell(str(node.get('change_summary') or ''))} "
        f"| {_escape_cell(str(node.get('next_validation') or ''))} |"
    )


def _logic_chain_node_lines(
    node: dict[str, Any],
    *,
    position: int,
    project_dir: Path | None,
) -> list[str]:
    lines = [
        f"#### {position:02d}. {node.get('title') or node.get('logic_node_id') or '逻辑节点'}",
        "",
        f"**研究问题：** {node.get('question') or ''}",
        "",
        f"**当前节点状态：** {node.get('state') or 'unresolved'}",
        "",
        f"**当前结论：** {node.get('conclusion') or ''}",
        "",
        f"**相较上一截面：** {node.get('change_summary') or ''}",
        "",
        "| 发布日期 | 报告名称 | 材料类型 | 原子观点 | 对逻辑点的影响 |",
        "|---|---|---|---|---|",
    ]
    source_groups = [
        source
        for period_group in node.get("event_history_groups") or []
        for source in period_group.get("sources") or []
    ]
    if source_groups:
        lines.extend(
            _logic_chain_material_row(source, project_dir=project_dir)
            for source in source_groups
        )
    else:
        lines.append("| — | 暂无报告 | 其他 | 当前没有映射到该节点的原子观点。 | 待判断 |")
    return lines + [""]


def _logic_chain_material_row(
    source_group: dict[str, Any],
    *,
    project_dir: Path | None,
) -> str:
    title = _escape_cell(
        str(source_group.get("source_title") or source_group.get("source_id") or "来源")
    )
    url = _rendered_source_url(
        str(source_group.get("source_url") or ""),
        project_dir=project_dir,
    )
    report_name = f"[{title}]({_markdown_link_target(url)})" if url else title
    atomic_claims = []
    impacts = []
    for index, event in enumerate(source_group.get("events") or [], start=1):
        labels = []
        if event.get("source_location"):
            labels.append(str(event["source_location"]))
        if event.get("effective_period"):
            labels.append(f"实际：{event['effective_period']}")
        if event.get("target_period"):
            labels.append(f"预测：{event['target_period']}")
        suffix = f"（{'；'.join(labels)}）" if labels else ""
        atomic_claims.append(
            f"{index}. {_escape_cell(str(event.get('statement') or ''))}{_escape_cell(suffix)}"
        )
        impact = CLAIM_IMPACT_LABELS.get(
            str(event.get("direction") or "neutral"),
            "待判断",
        )
        impacts.append(f"{index}. {_escape_cell(impact)}")
    return (
        f"| {_escape_cell(str(source_group.get('published_at') or '日期未明'))} "
        f"| {report_name} "
        f"| {_escape_cell(MATERIAL_LABELS.get(str(source_group.get('material_class') or ''), '其他'))} "
        f"| {'<br>'.join(atomic_claims) or '暂无原子观点'} "
        f"| {'<br>'.join(impacts) or '待判断'} |"
    )


def _logic_node_lines(
    node: dict[str, Any],
    *,
    project_dir: Path | None,
) -> list[str]:
    if str(node.get("render_mode") or "") == "demand_party_list":
        demand_parties = dict(node.get("demand_parties") or {})
        lines = [
            f"#### {node.get('title') or node.get('logic_node_id') or '需求方'}",
            "",
            f"**研究问题：** {node.get('question') or ''}",
            "",
        ]
        for group_id, label in (
            ("current", "当前需求方"),
            ("potential_future", "潜在未来需求方"),
        ):
            lines.extend([f"**{label}**", ""])
            lines.extend(
                f"- {party}"
                for party in demand_parties.get(group_id) or []
            )
            lines.append("")
        return lines
    if str(node.get("render_mode") or "") == "demand_quantity_matrix":
        rows = list(node.get("demand_quantity_rows") or [])
        quality_labels = {
            "direct": "直接映射",
            "proxy": "代理映射",
            "sample": "样本映射",
            "gap": "数据缺口",
            "unmapped": "不做映射",
        }

        def table_row(row: dict[str, Any]) -> str:
            source_text = _demand_quantity_source_text(
                row,
                project_dir=project_dir,
            )
            information_type = _demand_quantity_information_type(row)
            mapping_quality = quality_labels.get(
                str(row.get("mapping_quality") or ""),
                str(row.get("mapping_quality") or ""),
            )
            return (
                f"| {source_text} "
                f"| {_escape_cell(str(row.get('target_period') or ''))} "
                f"| {_escape_cell(information_type)} "
                f"| **{_escape_cell(str(row.get('metric') or ''))}："
                f"{_escape_cell(str(row.get('quantity') or ''))}**<br>"
                f"{_escape_cell(mapping_quality)} · "
                f"{_escape_cell(str(row.get('caveat') or ''))} |"
            )

        def append_category(
            target: list[str],
            category: str,
            category_rows: list[dict[str, Any]],
        ) -> None:
            target.extend(
                [
                    f"###### {category}",
                    "",
                    "| 来源 | 期间 | 信息类型 | 具体信息 |",
                    "|---|---|---|---|",
                ]
            )
            if category_rows:
                target.extend(table_row(row) for row in category_rows)
            else:
                target.append("| 暂无独立来源 | — | — | 暂无已登记信息。 |")
            target.append("")

        def group_by_party(
            group_rows: list[dict[str, Any]],
        ) -> dict[str, list[dict[str, Any]]]:
            grouped: dict[str, list[dict[str, Any]]] = {}
            for row in group_rows:
                grouped.setdefault(str(row.get("demand_party") or ""), []).append(
                    row
                )
            return grouped

        current_by_party = group_by_party(
            [row for row in rows if row.get("forecast_group") == "classified"]
        )
        potential_by_party = group_by_party(
            [row for row in rows if row.get("forecast_group") == "potential_future"]
        )
        demand_parties = dict(node.get("demand_parties") or {})
        lines = [
            f"#### {node.get('title') or node.get('logic_node_id') or '需求量'}",
            "",
            f"**研究问题：** {node.get('question') or ''}",
            "",
            "##### 1. 当前需求方",
            "",
        ]
        for party in demand_parties.get("current") or []:
            append_category(lines, str(party), current_by_party.get(str(party), []))
        lines.extend(["##### 2. 潜在未来需求方", ""])
        for party in demand_parties.get("potential_future") or []:
            append_category(
                lines,
                str(party),
                potential_by_party.get(str(party), []),
            )
        lines.extend(["##### 3. 其它分类", ""])
        other_by_category: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            if row.get("forecast_group") == "other":
                other_by_category.setdefault(
                    str(row.get("metric") or "其它信息"), []
                ).append(row)
        for category, category_rows in other_by_category.items():
            append_category(lines, category, category_rows)
        return lines
    lines = [
        f"#### {node.get('title') or node.get('logic_node_id') or '逻辑节点'}",
        "",
        f"**研究问题：** {node.get('question') or ''}",
        "",
        f"**当前结论：** {node.get('conclusion') or ''}",
        "",
    ]
    entities = list(node.get("entities") or [])
    if not entities:
        return [
            *lines,
            "当前没有映射到具体公司或实体的材料。",
            "",
        ]
    for entity in entities:
        lines.extend(
            [
                f"##### {entity.get('entity_name') or '未命名实体'}",
                "",
                (
                    "**截面变化与评估：** "
                    f"{entity.get('assessment') or ''}"
                ),
                "",
                (
                    "**相较上一截面：** "
                    f"{entity.get('change_summary') or ''}"
                ),
                "",
                "| 材料（含链接） | 类型 | 观点列表 |",
                "|---|---|---|",
            ]
        )
        groups = _group_claims_by_source(list(entity.get("claims") or []))
        if groups:
            lines.extend(
                _entity_source_claim_row(
                    group,
                    project_dir=project_dir,
                )
                for group in groups
            )
        else:
            lines.append("| 无 | 其他 | 尚无经过复核的实体级材料。 |")
        lines.append("")
    return lines


def _demand_quantity_source_text(
    row: dict[str, Any],
    *,
    project_dir: Path | None,
) -> str:
    links = []
    for source in row.get("sources") or []:
        title = _escape_cell(
            str(source.get("source_title") or source.get("source_id") or "来源")
        )
        url = _rendered_source_url(
            str(source.get("source_url") or ""),
            project_dir=project_dir,
        )
        link = f"[{title}]({_markdown_link_target(url)})" if url else title
        published_at = _escape_cell(str(source.get("published_at") or ""))
        links.append(f"{published_at} · {link}" if published_at else link)
    return "<br>".join(links) if links else "暂无独立来源"


def _demand_quantity_information_type(row: dict[str, Any]) -> str:
    labels = list(
        dict.fromkeys(
            DEMAND_INFORMATION_TYPE_LABELS.get(
                str(source.get("material_class") or "other"),
                "市场消息",
            )
            for source in row.get("sources") or []
        )
    )
    return " / ".join(labels) or "暂无来源"


def _entity_source_claim_row(
    group: dict[str, Any],
    *,
    project_dir: Path | None,
) -> str:
    title = _escape_cell(
        str(group.get("source_title") or group.get("source_id") or "来源")
    )
    url = _rendered_source_url(
        str(group.get("source_url") or "").strip(),
        project_dir=project_dir,
    )
    source = f"[{title}]({_markdown_link_target(url)})" if url else title
    published_at = _escape_cell(str(group.get("published_at") or ""))
    if published_at:
        source = f"{published_at}<br>{source}"
    viewpoints = []
    for index, claim in enumerate(group.get("claims") or [], start=1):
        location = _escape_cell(str(claim.get("source_location") or ""))
        statement = _escape_cell(str(claim.get("statement") or ""))
        mapping = next(iter(claim.get("logic_mappings") or []), {})
        direction = DIRECTION_LABELS.get(
            str(mapping.get("direction") or "neutral"),
            "线索",
        )
        label = f"观点 {index}"
        if location:
            label += f"（{location}）"
        viewpoints.append(
            f"• **{label} · {_escape_cell(direction)}**：{statement}"
        )
    return (
        f"| {source} "
        f"| {MATERIAL_LABELS.get(str(group.get('material_class') or ''), '其他')} "
        f"| {'<br>'.join(viewpoints)} |"
    )
