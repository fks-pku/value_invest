from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from value_invest_research.domain.report_view_model import ReportViewModel


SECTION_TITLES = (
    "1. 当前研究的问题",
    "2. 行业概况",
    "3. 标的推荐",
    "4. 来源索引",
)


class CanonicalMarkdownReportRenderer:
    """Markdown adapter for the canonical public research-report contract."""

    def render(self, view_model: ReportViewModel) -> str:
        data = view_model.to_dict()
        project = data["project"]
        title = str(project.get("title") or data["goal"].get("topic") or "专业投研报告")
        lines = [
            "---",
            "report_scope: research-project",
            f"project_id: {_yaml_scalar(project.get('project_id', ''))}",
            f"run_mode: {_yaml_scalar(project.get('run_mode', ''))}",
            f"as_of_date: {_yaml_scalar(project.get('as_of_date', ''))}",
            "---",
            "",
            f"# {title}",
            "",
            f"## {SECTION_TITLES[0]}",
            "",
            *_render_goal(data["goal"], project),
            "",
            f"## {SECTION_TITLES[1]}",
            "",
            *_render_industry_overview(data["supply_chain"], data["qa_roots"]),
            "",
            f"## {SECTION_TITLES[2]}",
            "",
            *_render_targets(data["targets"]),
            "",
            f"## {SECTION_TITLES[3]}",
            "",
            *_render_sources(data["sources"]),
            "",
        ]
        return "\n".join(lines)

    def write(
        self,
        project_dir: Path,
        view_model: ReportViewModel,
        *,
        filename: str = "professional_report.md",
    ) -> dict[str, Any]:
        project_dir.mkdir(parents=True, exist_ok=True)
        output_path = project_dir / filename
        output_path.write_text(self.render(view_model), encoding="utf-8")
        return {
            "project_id": view_model.project.get("project_id", ""),
            "report_path": str(output_path),
            "qa_roots": len(view_model.qa_roots),
            "targets": len(view_model.targets),
            "sources": len(view_model.sources),
        }


def _render_goal(goal: dict[str, Any], project: dict[str, Any]) -> list[str]:
    return [
        f"**研究对象：** {_text(goal.get('topic'))}",
        "",
        f"**研究截面：** {_text(project.get('as_of_date') or project.get('report_date'))}",
        "",
        f"**决策边界：** {_text(goal.get('decision_boundary'))}",
        "",
        f"**当前判断：** {_text(goal.get('current_judgment'))}",
        "",
        f"**最大不确定性：** {_text(goal.get('biggest_uncertainty'))}",
    ]


def _render_industry_overview(
    supply_chain: dict[str, Any],
    qa_roots: list[dict[str, Any]],
) -> list[str]:
    lines = [
        _text(supply_chain.get("plain_summary") or "行业概况由技术链、BOM 与结构化研究问题组成。"),
        "",
    ]
    layers = supply_chain.get("layers") or []
    if layers:
        lines.extend(
            [
                "### 技术链与 BOM",
                "",
                "| 环节 | 节点 | 接受什么 | 生产什么 | 代表玩家 | 验证指标 |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for layer in layers:
            lines.append(
                "| "
                + " | ".join(
                    _cell(layer.get(field))
                    for field in (
                        "stage",
                        "node",
                        "demand_input",
                        "produces",
                        "players",
                        "financial_metrics",
                    )
                )
                + " |"
            )
        lines.append("")
    if qa_roots:
        lines.extend(["### 研究问题", ""])
        for node in qa_roots:
            lines.extend(_render_qa_node(node, 4))
    return lines


def _render_qa_node(node: dict[str, Any], level: int) -> list[str]:
    heading_level = min(level, 6)
    lines = [f"{'#' * heading_level} {_text(node.get('question'))}", ""]
    if node.get("conclusion"):
        lines.extend([_text(node["conclusion"]), ""])
    for child in node.get("children") or []:
        lines.extend(_render_qa_node(child, heading_level + 1))
    return lines


def _render_targets(targets: list[dict[str, Any]]) -> list[str]:
    if not targets:
        return ["当前没有通过研究闸门的标的；这不是空白买入建议。"]
    lines = [
        "| 标的 | 节点 | 状态 | 核心理由 | 风险与降级条件 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for target in targets:
        lines.append(
            "| "
            + " | ".join(
                _cell(value)
                for value in (
                    target.get("ticker") or target.get("name"),
                    target.get("thesis_node") or target.get("thesis_node_id"),
                    target.get("action_state"),
                    target.get("rationale") or target.get("thesis"),
                    target.get("downgrade") or target.get("risks"),
                )
            )
            + " |"
        )
    return lines


def _render_sources(sources: Iterable[dict[str, Any]]) -> list[str]:
    rows = list(sources)
    if not rows:
        return ["当前没有公开来源索引。"]
    lines = [
        "| ID | 来源 | 类型 | 市场可见时间 | 用途摘要 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for source in rows:
        title = _text(source.get("title") or source.get("source_id"))
        url = _text(source.get("url"))
        linked_title = f"[{title}]({url})" if url else title
        lines.append(
            "| "
            + " | ".join(
                (
                    _cell(source.get("source_id")),
                    _cell(linked_title),
                    _cell(source.get("material_class") or source.get("source_bucket")),
                    _cell(source.get("source_visible_at") or source.get("published_at")),
                    _cell(source.get("summary")),
                )
            )
            + " |"
        )
    return lines


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _cell(value: Any) -> str:
    return " ".join(_text(value).replace("|", "\\|").splitlines())


def _yaml_scalar(value: Any) -> str:
    return '"' + _text(value).replace("\\", "\\\\").replace('"', '\\"') + '"'
