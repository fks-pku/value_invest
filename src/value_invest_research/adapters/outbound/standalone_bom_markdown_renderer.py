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


class StandaloneBomMarkdownRenderer:
    """Render one five-lens BOM timeline without exposing process artifacts."""

    def __init__(self, project_dir: Path | None = None):
        self.project_dir = project_dir.resolve() if project_dir else None

    def render(self, view: dict[str, Any]) -> str:
        lines = [
            "---",
            "report_scope: standalone-bom",
            f"bom_node_id: {view['bom_node_id']}",
            f"as_of_date: {view['as_of_date']}",
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
        for index, lens in enumerate(view["lenses"], start=1):
            lines.extend(
                [
                    f"## {index}. {lens['label']}",
                    "",
                    "### 简单逻辑链",
                    "",
                    lens["logic_chain"] or "当前逻辑链尚未定义。",
                    "",
                    "### 信息时间线",
                    "",
                    "| 时间 | 信息类型 | Source | 观点列表 |",
                    "|---|---|---|---|",
                ]
            )
            claims = lens.get("claims") or []
            if claims:
                lines.extend(
                    _source_claim_row(group, project_dir=self.project_dir)
                    for group in _group_claims_by_source(claims)
                )
            else:
                lines.append(
                    f"| {view['as_of_date']} | 其他 | 无 | "
                    "尚无经过问题化解析和复核的材料。 |"
                )
            lines.extend(
                [
                    "",
                    "### 最新结论与趋势",
                    "",
                    lens["conclusion"],
                    "",
                ]
            )
            if lens.get("trend"):
                lines.extend([f"**趋势变化：** {lens['trend']}", ""])
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
        viewpoints.append(f"• **{label}**：{statement}")
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
