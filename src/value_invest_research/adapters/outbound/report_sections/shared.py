from __future__ import annotations

from html import escape
import re
from typing import Any

_COMPETITION_PROSE_QUESTIONS = {
    "玩家市场份额分布",
    "头部玩家优势分析",
    "替代玩家赶超希望",
    "格局变化核心变量",
}


def _source_url_lookup(sources: list[dict[str, Any]]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for source in sources:
        if not isinstance(source, dict):
            continue
        source_id = str(source.get("source_id") or source.get("id") or "")
        url = str(source.get("url") or "")
        if source_id and url:
            lookup[source_id] = url
    return lookup


def _render_source_chip(source_id: str, source_url_by_id: dict[str, str]) -> str:
    url = source_url_by_id.get(str(source_id), "")
    if url:
        return f'<a class="source-chip" href="{_e(url)}" target="_blank" rel="noopener">{_e(str(source_id))}</a>'
    return f'<span class="source-chip">{_e(str(source_id))}</span>'


def _render_overview_question_card(
    *,
    question: str,
    answer: Any,
    source_ids: list[Any],
    source_url_by_id: dict[str, str],
    class_name: str = "competition-subcard",
    source_plan: dict[str, Any] | None = None,
) -> str:
    answer_source_ids: list[Any] = []
    if isinstance(answer, dict):
        raw_answer_source_ids = answer.get("sourceIds") or answer.get("source_ids") or []
        if isinstance(raw_answer_source_ids, list):
            answer_source_ids = raw_answer_source_ids
    marked_source_ids = _extract_source_marked_ids(answer)
    all_source_ids = list(dict.fromkeys(marked_source_ids or answer_source_ids))
    chips = "".join(_render_source_chip(str(sid), source_url_by_id) for sid in all_source_ids if sid)
    if not chips:
        chips = '<span class="source-chip source-chip-missing">待补来源</span>'
    if question in _COMPETITION_PROSE_QUESTIONS and not _has_prose_answer(answer):
        if isinstance(answer, dict):
            prose_parts = [
                answer.get("judgment") or answer.get("current_judgment") or answer.get("answer"),
                answer.get("facts") or answer.get("key_facts"),
                answer.get("reasoning") or answer.get("inference"),
                answer.get("evidence") or answer.get("source_read"),
                answer.get("gap") or answer.get("trigger") or answer.get("missing_data"),
            ]
            prose = " ".join(str(part) for part in prose_parts if part not in (None, ""))
            answer = {"paragraphs": [prose or "待补。"]}
        else:
            answer = {"paragraphs": [str(answer or "待补。")]}
    answer_html = _render_overview_answer(answer, source_url_by_id)
    return f"""
            <section class="{class_name} overview-question-card">
              <h4>{_e(question)}</h4>
              {answer_html}
              <div class="overview-answer-sources source-chips">{chips}</div>
            </section>""".rstrip()


def _render_overview_answer(answer: Any, source_url_by_id: dict[str, str] | None = None) -> str:
    if isinstance(answer, dict):
        paragraphs = answer.get("paragraphs") or answer.get("prose")
        if isinstance(paragraphs, list):
            body = "".join(
                f'<p>{_render_source_marked_text(str(paragraph or "待补。"), source_url_by_id or {})}</p>'
                for paragraph in paragraphs
            )
            return f'<div class="overview-answer overview-answer-prose">{body}</div>'
        rows = [
            ("当前判断", answer.get("judgment") or answer.get("current_judgment") or answer.get("answer")),
            ("关键事实", answer.get("facts") or answer.get("key_facts")),
            ("推理链", answer.get("reasoning") or answer.get("inference")),
            ("证据来源", answer.get("evidence") or answer.get("source_read")),
            ("缺口 / 触发器", answer.get("gap") or answer.get("trigger") or answer.get("missing_data")),
        ]
        body = "".join(
            f'<div class="overview-answer-row"><span>{_e(label)}</span><p>{_e(str(value or "待补。"))}</p></div>'
            for label, value in rows
        )
        return f'<div class="overview-answer overview-answer-structured">{body}</div>'
    return f'<p class="overview-answer">{_render_source_marked_text(str(answer or "待补。"), source_url_by_id or {})}</p>'


def _has_prose_answer(answer: Any) -> bool:
    return isinstance(answer, dict) and (
        isinstance(answer.get("paragraphs"), list) or isinstance(answer.get("prose"), list)
    )


def _extract_source_marked_ids(answer: Any) -> list[str]:
    parts: list[Any] = []
    if isinstance(answer, dict):
        paragraphs = answer.get("paragraphs") or answer.get("prose")
        if isinstance(paragraphs, list):
            parts.extend(paragraphs)
        for key in (
            "judgment",
            "current_judgment",
            "answer",
            "facts",
            "key_facts",
            "reasoning",
            "inference",
            "evidence",
            "source_read",
            "gap",
            "trigger",
            "missing_data",
        ):
            value = answer.get(key)
            if value:
                parts.append(value)
    elif answer:
        parts.append(answer)
    pattern = re.compile(r"\[[^\]]+\]\(source:([A-Za-z0-9_.:-]+)\)")
    source_ids: list[str] = []
    for part in parts:
        source_ids.extend(pattern.findall(str(part or "")))
    return list(dict.fromkeys(source_ids))


def _render_source_marked_text(text: str, source_url_by_id: dict[str, str]) -> str:
    pattern = re.compile(r"\[([^\]]+)\]\(source:([A-Za-z0-9_.:-]+)\)")
    html: list[str] = []
    last_index = 0
    for match in pattern.finditer(text):
        html.append(_e(text[last_index : match.start()]))
        label = match.group(1)
        source_id = match.group(2)
        url = source_url_by_id.get(source_id, "")
        if url:
            html.append(f'<a href="{_e(url)}" target="_blank" rel="noopener">{_e(label)}</a>')
        else:
            html.append(_e(label))
        last_index = match.end()
    html.append(_e(text[last_index:]))
    return "".join(html)


def _row_cells(row: Any, max_cells: int) -> list[Any]:
    if isinstance(row, dict):
        return list(row.values())[:max_cells]
    if isinstance(row, list):
        return row[:max_cells]
    return [row]


def _slug(value: str) -> str:
    token = "".join(ch if ch.isalnum() else "-" for ch in value.strip().lower()).strip("-")
    return token or "item"


def _e(value: str) -> str:
    return escape(value, quote=True)
