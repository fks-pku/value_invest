from __future__ import annotations

import hashlib
import html
import json
import re
import shlex
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from value_invest_research.models import EvidenceRecord, ValidationError
from value_invest_research.research_system import (
    INFO_CATEGORY_LABEL_ZH,
    SOURCE_ORIGIN_INFO_ORDER,
    build_research_system,
    normalize_ticker,
    record_question_information,
)


EXPECTED_SOURCE_FIELDS = [
    "node_id",
    "category",
    "source_type",
    "source_name",
    "url",
    "summary",
    "reliability",
    "materiality",
    "published_at",
]


RECOMMENDED_SOURCES = {
    "evidence": [
        "公司公告、年报、半年报、业绩发布材料",
        "交易所、监管机构、政府或统计部门公开数据",
        "公司 IR、招股书、投资者日或正式新闻稿",
    ],
    "research_report": [
        "卖方深度报告、行业专题、公司跟踪报告",
        "行业数据库、咨询公司或协会报告",
        "可复核的第三方份额、价格、出货、利润池数据",
    ],
    "message": [
        "主流财经媒体、监管新闻、交易所公告动态",
        "公司新闻发布、渠道和供应链公开进展",
        "需要后续证实的公开消息源",
    ],
    "opinion": [
        "专家访谈、产业人士观点、投资者交流纪要",
        "高质量 KOL 或专业社区观点",
        "能提出机制、反证或关键假设的主观判断",
    ],
}


ACCEPTANCE_CRITERIA = {
    "evidence": [
        "必须能打开或定位到原始来源，并记录发布日期或报告期。",
        "摘要要提取可验证事实、指标、口径或公司正式表述。",
        "默认可靠性为 primary/high；不能把二手转述当作一手证据。",
    ],
    "research_report": [
        "必须记录机构/作者/日期，并说明核心结论与关键假设。",
        "要区分报告事实、模型推导和分析师判断。",
        "只能作为支撑或反证材料，不能单独替代一手证据。",
    ],
    "message": [
        "必须标注消息来源和未证实边界。",
        "摘要要写清楚可能影响的业务节点、假设或触发器。",
        "默认低权重，只能作为研究线索，不能直接强化结论。",
    ],
    "opinion": [
        "必须说明观点来源身份、专业背景或立场可能性。",
        "摘要要提炼可检验机制，而不是只记录态度。",
        "需要配套下一步验证数据，避免把观点当事实。",
    ],
}


DEFAULT_RELIABILITY = {
    "evidence": "primary",
    "research_report": "high",
    "message": "low",
    "opinion": "medium",
}


DEFAULT_MATERIALITY = {
    "evidence": "high",
    "research_report": "medium",
    "message": "medium",
    "opinion": "medium",
}


RELIABILITY_SCORE = {"primary": 4, "high": 3, "medium": 2, "low": 1}
MATERIALITY_SCORE = {"thesis_change": 4, "high": 3, "medium": 2, "low": 1}

OFFICIAL_DOMAIN_TOKENS = (
    "sec.gov",
    "hkexnews.hk",
    "hkex.com.hk",
    "samr.gov.cn",
    "sse.com.cn",
    "szse.cn",
    "gov.cn",
    "ir.",
)
RESEARCH_DOMAIN_TOKENS = ("pdf.dfcfw.com", "research", "securities", "证券", "report", "pdf")
NEWS_DOMAIN_TOKENS = ("reuters", "bloomberg", "wsj", "caixin", "sina", "36kr", "yicai", "cnstock", "stcn")
OPINION_DOMAIN_TOKENS = ("xueqiu", "zhihu", "weixin", "substack", "medium", "blog", "twitter", "x.com")


def build_research_collection_tasks(
    root: Path,
    ticker: str,
    include_matched: bool = False,
    limit: int | None = None,
) -> dict[str, Any]:
    """Create actionable collection tasks for a stock research system."""
    normalized = normalize_ticker(ticker)
    build_result = build_research_system(root, normalized)
    research_dir = Path(build_result["dashboard_path"]).parent
    qa_tree = _read_json(research_dir / "qa_tree.json")
    rows = _read_jsonl(research_dir / "information_collection.jsonl")
    tasks = _tasks_from_collection_rows(
        rows,
        object_type="stock",
        object_id=normalized,
        include_matched=include_matched,
        bind_command_builder=_stock_bind_command,
    )
    tasks = _limit_tasks(tasks, limit)
    task_path = research_dir / "collection_tasks.jsonl"
    _write_jsonl(task_path, tasks)
    return {
        **build_result,
        "task_path": str(task_path),
        "tasks": len(tasks),
        "leaf_questions": _leaf_question_count(qa_tree),
        "include_matched": include_matched,
    }


def build_meta_qa_collection_tasks(
    root: Path,
    project_id: str,
    include_matched: bool = False,
    limit: int | None = None,
) -> dict[str, Any]:
    """Create actionable collection tasks for an existing generic QA project."""
    from value_invest_research.meta_qa_research import _rebuild_meta_qa_project

    rebuild_result = _rebuild_meta_qa_project(root, project_id)
    project_dir = Path(rebuild_result["project_dir"])
    qa_tree = _read_json(project_dir / "qa_tree.json")
    rows = _read_jsonl(project_dir / "information_collection.jsonl")
    tasks = _tasks_from_collection_rows(
        rows,
        object_type="meta_qa",
        object_id=rebuild_result["project_id"],
        include_matched=include_matched,
        bind_command_builder=_meta_qa_bind_command,
    )
    tasks = _limit_tasks(tasks, limit)
    task_path = project_dir / "collection_tasks.jsonl"
    _write_jsonl(task_path, tasks)
    return {
        **rebuild_result,
        "task_path": str(task_path),
        "tasks": len(tasks),
        "leaf_questions": _leaf_question_count(qa_tree),
        "include_matched": include_matched,
    }


def import_question_information(root: Path, ticker: str, path: Path) -> dict[str, Any]:
    """Batch-import collected stock QA sources from JSONL."""
    normalized = normalize_ticker(ticker)
    rows = _read_jsonl(path)
    return _import_rows(
        rows,
        import_one=lambda row: record_question_information(
            root,
            normalized,
            row["node_id"],
            row["category"],
            row["source_type"],
            row["source_name"],
            row["url"],
            row["summary"],
            reliability=row.get("reliability") or DEFAULT_RELIABILITY[row["category"]],
            materiality=row.get("materiality") or DEFAULT_MATERIALITY[row["category"]],
            published_at=row.get("published_at"),
        ),
        result_base={"ticker": normalized, "input_path": str(path)},
    )


def import_meta_qa_information(root: Path, project_id: str, path: Path) -> dict[str, Any]:
    """Batch-import collected generic QA sources from JSONL."""
    from value_invest_research.meta_qa_research import record_meta_qa_information

    rows = _read_jsonl(path)
    return _import_rows(
        rows,
        import_one=lambda row: record_meta_qa_information(
            root,
            project_id,
            row["node_id"],
            row["category"],
            row["source_type"],
            row["source_name"],
            row["url"],
            row["summary"],
            reliability=row.get("reliability") or DEFAULT_RELIABILITY[row["category"]],
            materiality=row.get("materiality") or DEFAULT_MATERIALITY[row["category"]],
            published_at=row.get("published_at"),
        ),
        result_base={"project_id": project_id, "input_path": str(path)},
    )


def fetch_question_information_url(
    root: Path,
    ticker: str,
    node_id: str,
    category: str,
    url: str,
    source_type: str | None = None,
    source_name: str | None = None,
    summary: str | None = None,
    reliability: str | None = None,
    materiality: str | None = None,
    published_at: str | None = None,
    timeout: int = 10,
) -> dict[str, Any]:
    """Fetch one URL, summarize it, attach it to a stock QA node, and rebuild."""
    normalized = normalize_ticker(ticker)
    row, fetched = _url_import_row(
        category=category,
        url=url,
        source_type=source_type,
        source_name=source_name,
        summary=summary,
        reliability=reliability,
        materiality=materiality,
        published_at=published_at,
        timeout=timeout,
    )
    row["node_id"] = node_id
    result = record_question_information(
        root,
        normalized,
        row["node_id"],
        row["category"],
        row["source_type"],
        row["source_name"],
        row["url"],
        row["summary"],
        reliability=row["reliability"],
        materiality=row["materiality"],
        published_at=row.get("published_at"),
    )
    log_path = root / "stocks" / normalized / "research_system" / "fetched_sources.jsonl"
    _append_fetched_source_log(log_path, result, row, fetched)
    return {**result, "source_name": row["source_name"], "summary": row["summary"], "fetched_log_path": str(log_path)}


def fetch_meta_qa_information_url(
    root: Path,
    project_id: str,
    node_id: str,
    category: str,
    url: str,
    source_type: str | None = None,
    source_name: str | None = None,
    summary: str | None = None,
    reliability: str | None = None,
    materiality: str | None = None,
    published_at: str | None = None,
    timeout: int = 10,
) -> dict[str, Any]:
    """Fetch one URL, summarize it, attach it to a generic QA node, and rebuild."""
    from value_invest_research.meta_qa_research import record_meta_qa_information

    row, fetched = _url_import_row(
        category=category,
        url=url,
        source_type=source_type,
        source_name=source_name,
        summary=summary,
        reliability=reliability,
        materiality=materiality,
        published_at=published_at,
        timeout=timeout,
    )
    row["node_id"] = node_id
    result = record_meta_qa_information(
        root,
        project_id,
        row["node_id"],
        row["category"],
        row["source_type"],
        row["source_name"],
        row["url"],
        row["summary"],
        reliability=row["reliability"],
        materiality=row["materiality"],
        published_at=row.get("published_at"),
    )
    log_path = Path(result["project_dir"]) / "fetched_sources.jsonl"
    _append_fetched_source_log(log_path, result, row, fetched)
    return {**result, "source_name": row["source_name"], "summary": row["summary"], "fetched_log_path": str(log_path)}


def run_research_collection_tasks(
    root: Path,
    ticker: str,
    include_matched: bool = False,
    limit: int | None = None,
    min_score: int = 4,
    max_sources_per_task: int = 1,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Run stock collection tasks against the local evidence corpus and bind matches."""
    normalized = normalize_ticker(ticker)
    tasks_result = build_research_collection_tasks(root, normalized, include_matched=include_matched, limit=limit)
    research_dir = Path(tasks_result["dashboard_path"]).parent
    records = _read_evidence_records(root / "stocks" / normalized / "evidence.jsonl")
    tasks = _read_jsonl(Path(tasks_result["task_path"]))
    matches = _local_collection_matches(
        tasks,
        records,
        link_builder=lambda node_id: f"research_system:{node_id}",
        min_score=min_score,
        max_sources_per_task=max_sources_per_task,
    )
    result_path = research_dir / "collection_results.jsonl"
    _write_jsonl(result_path, matches)

    import_result: dict[str, Any] = {}
    if matches and not dry_run:
        import_result = import_question_information(root, normalized, result_path)
    return {
        **tasks_result,
        "result_path": str(result_path),
        "matches": len(matches),
        "dry_run": dry_run,
        "created": import_result.get("created", 0),
        "updated": import_result.get("updated", 0),
        "existing": import_result.get("existing", 0),
        "dashboard_path": import_result.get("dashboard_path", tasks_result.get("dashboard_path", "")),
        "report_path": import_result.get("report_path", tasks_result.get("report_path", "")),
        "information_collection_path": import_result.get(
            "information_collection_path",
            tasks_result.get("information_collection_path", ""),
        ),
    }


def run_meta_qa_collection_tasks(
    root: Path,
    project_id: str,
    include_matched: bool = False,
    limit: int | None = None,
    min_score: int = 4,
    max_sources_per_task: int = 1,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Run generic QA collection tasks against the project evidence corpus and bind matches."""
    tasks_result = build_meta_qa_collection_tasks(root, project_id, include_matched=include_matched, limit=limit)
    project_dir = Path(tasks_result["project_dir"])
    records = _read_evidence_records(project_dir / "evidence.jsonl")
    tasks = _read_jsonl(Path(tasks_result["task_path"]))
    matches = _local_collection_matches(
        tasks,
        records,
        link_builder=lambda node_id: f"meta_qa:{tasks_result['project_id']}:{node_id}",
        min_score=min_score,
        max_sources_per_task=max_sources_per_task,
    )
    result_path = project_dir / "collection_results.jsonl"
    _write_jsonl(result_path, matches)

    import_result: dict[str, Any] = {}
    if matches and not dry_run:
        import_result = import_meta_qa_information(root, tasks_result["project_id"], result_path)
    return {
        **tasks_result,
        "result_path": str(result_path),
        "matches": len(matches),
        "dry_run": dry_run,
        "created": import_result.get("created", 0),
        "updated": import_result.get("updated", 0),
        "existing": import_result.get("existing", 0),
        "dashboard_path": import_result.get("dashboard_path", tasks_result.get("dashboard_path", "")),
        "report_path": import_result.get("report_path", tasks_result.get("report_path", "")),
        "information_collection_path": import_result.get(
            "information_collection_path",
            tasks_result.get("information_collection_path", ""),
        ),
    }


def discover_research_source_candidates(
    root: Path,
    ticker: str,
    include_matched: bool = False,
    limit: int | None = None,
    results_per_task: int = 3,
    min_score: int = 4,
    timeout: int = 10,
    search_results_path: Path | None = None,
) -> dict[str, Any]:
    """Search or import candidate URLs for stock collection tasks."""
    normalized = normalize_ticker(ticker)
    tasks_result = build_research_collection_tasks(root, normalized, include_matched=include_matched, limit=limit)
    research_dir = Path(tasks_result["dashboard_path"]).parent
    tasks = _read_jsonl(Path(tasks_result["task_path"]))
    candidates = _source_candidates_for_tasks(
        tasks,
        object_type="stock",
        object_id=normalized,
        results_per_task=results_per_task,
        min_score=min_score,
        timeout=timeout,
        search_results_path=search_results_path,
        fetch_command_builder=_stock_fetch_candidate_command,
    )
    candidate_path = research_dir / "source_candidates.jsonl"
    _write_jsonl(candidate_path, candidates)
    return {
        **tasks_result,
        "candidate_path": str(candidate_path),
        "candidates": len(candidates),
        "accepted_candidates": sum(1 for row in candidates if row.get("accepted")),
        "search_results_path": str(search_results_path) if search_results_path else "",
    }


def discover_meta_qa_source_candidates(
    root: Path,
    project_id: str,
    include_matched: bool = False,
    limit: int | None = None,
    results_per_task: int = 3,
    min_score: int = 4,
    timeout: int = 10,
    search_results_path: Path | None = None,
) -> dict[str, Any]:
    """Search or import candidate URLs for generic QA collection tasks."""
    tasks_result = build_meta_qa_collection_tasks(root, project_id, include_matched=include_matched, limit=limit)
    project_dir = Path(tasks_result["project_dir"])
    tasks = _read_jsonl(Path(tasks_result["task_path"]))
    candidates = _source_candidates_for_tasks(
        tasks,
        object_type="meta_qa",
        object_id=tasks_result["project_id"],
        results_per_task=results_per_task,
        min_score=min_score,
        timeout=timeout,
        search_results_path=search_results_path,
        fetch_command_builder=_meta_qa_fetch_candidate_command,
    )
    candidate_path = project_dir / "source_candidates.jsonl"
    _write_jsonl(candidate_path, candidates)
    return {
        **tasks_result,
        "candidate_path": str(candidate_path),
        "candidates": len(candidates),
        "accepted_candidates": sum(1 for row in candidates if row.get("accepted")),
        "search_results_path": str(search_results_path) if search_results_path else "",
    }


def apply_research_source_candidates(
    root: Path,
    ticker: str,
    path: Path,
    min_score: int = 4,
    limit: int | None = None,
    dry_run: bool = False,
    timeout: int = 10,
) -> dict[str, Any]:
    """Fetch accepted stock source candidates and bind them to QA nodes."""
    normalized = normalize_ticker(ticker)
    rows = _limit_tasks(_read_jsonl(path), limit)
    applied: list[dict[str, Any]] = []
    for row in rows:
        candidate = _validated_candidate_row(row)
        if not candidate["accepted"] or candidate["score"] < min_score:
            continue
        if dry_run:
            applied.append({**candidate, "applied": False, "dry_run": True})
            continue
        result = fetch_question_information_url(
            root,
            normalized,
            candidate["node_id"],
            candidate["category"],
            candidate["url"],
            source_type=candidate["source_type"],
            source_name=candidate["source_name"],
            reliability=candidate["reliability"],
            materiality=candidate["materiality"],
            timeout=timeout,
        )
        applied.append({**candidate, "applied": True, "evidence_id": result["evidence_id"]})
    research_dir = root / "stocks" / normalized / "research_system"
    result_path = research_dir / "candidate_import_results.jsonl"
    _write_jsonl(result_path, applied)
    return {
        "ticker": normalized,
        "input_path": str(path),
        "result_path": str(result_path),
        "dry_run": dry_run,
        "candidates": len(rows),
        "applied": sum(1 for row in applied if row.get("applied")),
        "skipped": len(rows) - len(applied),
    }


def apply_meta_qa_source_candidates(
    root: Path,
    project_id: str,
    path: Path,
    min_score: int = 4,
    limit: int | None = None,
    dry_run: bool = False,
    timeout: int = 10,
) -> dict[str, Any]:
    """Fetch accepted generic QA source candidates and bind them to QA nodes."""
    rows = _limit_tasks(_read_jsonl(path), limit)
    applied: list[dict[str, Any]] = []
    project_dir = root / "research" / "qa_projects" / project_id
    for row in rows:
        candidate = _validated_candidate_row(row)
        if not candidate["accepted"] or candidate["score"] < min_score:
            continue
        if dry_run:
            applied.append({**candidate, "applied": False, "dry_run": True})
            continue
        result = fetch_meta_qa_information_url(
            root,
            project_id,
            candidate["node_id"],
            candidate["category"],
            candidate["url"],
            source_type=candidate["source_type"],
            source_name=candidate["source_name"],
            reliability=candidate["reliability"],
            materiality=candidate["materiality"],
            timeout=timeout,
        )
        applied.append({**candidate, "applied": True, "evidence_id": result["evidence_id"]})
        project_dir = Path(result["project_dir"])
    result_path = project_dir / "candidate_import_results.jsonl"
    _write_jsonl(result_path, applied)
    return {
        "project_id": project_id,
        "input_path": str(path),
        "result_path": str(result_path),
        "dry_run": dry_run,
        "candidates": len(rows),
        "applied": sum(1 for row in applied if row.get("applied")),
        "skipped": len(rows) - len(applied),
    }


class _HtmlTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self.meta_description = ""
        self._skip_depth = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        normalized = tag.lower()
        if normalized in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1
            return
        if normalized == "title":
            self._in_title = True
            return
        if normalized == "meta":
            attr_map = {key.lower(): (value or "") for key, value in attrs}
            name = attr_map.get("name", "").lower()
            prop = attr_map.get("property", "").lower()
            if name == "description" or prop == "og:description":
                self.meta_description = attr_map.get("content", "").strip()

    def handle_endtag(self, tag: str) -> None:
        normalized = tag.lower()
        if normalized in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1
        if normalized == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        text = _collapse_space(data)
        if not text:
            return
        if self._in_title:
            self.title_parts.append(text)
        elif not self._skip_depth:
            self.text_parts.append(text)

    @property
    def title(self) -> str:
        return _collapse_space(" ".join(self.title_parts))

    @property
    def body_text(self) -> str:
        return _collapse_space(" ".join(self.text_parts))


def _url_import_row(
    category: str,
    url: str,
    source_type: str | None,
    source_name: str | None,
    summary: str | None,
    reliability: str | None,
    materiality: str | None,
    published_at: str | None,
    timeout: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    cleaned_url = url.strip()
    if not cleaned_url:
        raise ValueError("url cannot be empty")
    cleaned_category = category.strip()
    if cleaned_category not in SOURCE_ORIGIN_INFO_ORDER:
        raise ValueError(f"category must be one of {SOURCE_ORIGIN_INFO_ORDER}")
    if timeout <= 0:
        raise ValueError("timeout must be positive")

    fetched = _fetch_url_text(cleaned_url, timeout)
    inferred_source_type = source_type.strip() if source_type else _default_url_source_type(cleaned_category, cleaned_url)
    inferred_source_name = source_name.strip() if source_name else _default_url_source_name(fetched, cleaned_url)
    inferred_summary = summary.strip() if summary else _default_url_summary(fetched)
    return (
        {
            "node_id": "",
            "category": cleaned_category,
            "source_type": inferred_source_type,
            "source_name": inferred_source_name,
            "url": cleaned_url,
            "summary": inferred_summary,
            "reliability": reliability or DEFAULT_RELIABILITY[cleaned_category],
            "materiality": materiality or DEFAULT_MATERIALITY[cleaned_category],
            "published_at": published_at,
        },
        fetched,
    )


def _fetch_url_text(url: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "value-invest-research/0.1 (+https://local/research)",
            "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8",
        },
    )
    fetched_at = datetime.now(timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            final_url = response.geturl() if hasattr(response, "geturl") else url
            headers = getattr(response, "headers", {})
            content_type = headers.get("Content-Type", "") if hasattr(headers, "get") else ""
    except (OSError, TimeoutError, urllib.error.URLError) as exc:
        raise ValueError(f"failed to fetch url {url}: {exc}") from exc
    content_hash = hashlib.sha256(raw).hexdigest()
    text, title, meta_description = _extract_response_text(raw, content_type, url)
    return {
        "url": url,
        "final_url": final_url,
        "content_type": content_type,
        "content_hash": f"sha256:{content_hash}",
        "fetched_at": fetched_at,
        "title": title,
        "meta_description": meta_description,
        "text": text,
    }


def _extract_response_text(raw: bytes, content_type: str, url: str) -> tuple[str, str, str]:
    lowered_type = content_type.lower()
    if "html" in lowered_type or url.lower().endswith((".html", ".htm")):
        text = raw.decode(_charset_from_content_type(content_type), errors="replace")
        parser = _HtmlTextExtractor()
        parser.feed(text)
        return parser.body_text, html.unescape(parser.title), html.unescape(parser.meta_description)
    if "text" in lowered_type or url.lower().endswith((".txt", ".csv", ".json")):
        text = _collapse_space(raw.decode(_charset_from_content_type(content_type), errors="replace"))
        return text, "", ""
    return "", "", ""


def _charset_from_content_type(content_type: str) -> str:
    match = re.search(r"charset=([A-Za-z0-9_\-]+)", content_type or "")
    return match.group(1) if match else "utf-8"


def _default_url_source_type(category: str, url: str) -> str:
    lowered = url.lower()
    if category == "evidence":
        if "sec.gov" in lowered:
            return "sec_filing"
        if any(token in lowered for token in ("gov", "regulator", "samr", "hkex", "sse.com", "szse.cn")):
            return "regulator_notice"
        return "company_ir"
    if category == "research_report":
        return "sell_side_report"
    if category == "opinion":
        return "opinion"
    return "news"


def _default_url_source_name(fetched: dict[str, Any], url: str) -> str:
    title = _collapse_space(fetched.get("title", ""))
    if title:
        return _truncate(title, 96)
    slug = re.sub(r"^https?://", "", url).strip("/")
    return _truncate(slug or "URL 来源", 96)


def _default_url_summary(fetched: dict[str, Any]) -> str:
    description = _collapse_space(fetched.get("meta_description", ""))
    text = _collapse_space(fetched.get("text", ""))
    if description:
        return _truncate(description, 360)
    if text:
        return _truncate(text, 360)
    content_type = fetched.get("content_type", "") or "unknown content type"
    return f"已抓取该 URL，但内容类型为 {content_type}，系统未能自动提取正文；需要人工补充摘要后再强化结论。"


def _append_fetched_source_log(
    path: Path,
    result: dict[str, Any],
    row: dict[str, Any],
    fetched: dict[str, Any],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    log_row = {
        "node_id": row.get("node_id", ""),
        "category": row.get("category", ""),
        "source_type": row.get("source_type", ""),
        "source_name": row.get("source_name", ""),
        "url": row.get("url", ""),
        "summary": row.get("summary", ""),
        "evidence_id": result.get("evidence_id", ""),
        "created": bool(result.get("created")),
        "updated": bool(result.get("updated")),
        "content_hash": fetched.get("content_hash", ""),
        "content_type": fetched.get("content_type", ""),
        "final_url": fetched.get("final_url", ""),
        "fetched_at": fetched.get("fetched_at", ""),
        "title": fetched.get("title", ""),
    }
    with path.open("a", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps(log_row, ensure_ascii=False, sort_keys=True) + "\n")


def _collapse_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def _truncate(value: str, limit: int) -> str:
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"


def _source_candidates_for_tasks(
    tasks: list[dict[str, Any]],
    object_type: str,
    object_id: str,
    results_per_task: int,
    min_score: int,
    timeout: int,
    search_results_path: Path | None,
    fetch_command_builder: Callable[[str, dict[str, Any]], str],
) -> list[dict[str, Any]]:
    if results_per_task <= 0:
        raise ValueError("results_per_task must be positive")
    if min_score < 0:
        raise ValueError("min_score must be non-negative")
    imported_results = _read_search_results_by_task(search_results_path) if search_results_path else {}
    created_at = datetime.now(timezone.utc).isoformat()
    candidates: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for task in tasks:
        raw_results = imported_results.get(task["task_id"])
        if raw_results is None and search_results_path is not None:
            continue
        if raw_results is None:
            raw_results = _duckduckgo_search(task.get("search_query", ""), results_per_task, timeout)
        for raw in raw_results[:results_per_task]:
            candidate = _candidate_from_search_result(
                task,
                raw,
                object_type=object_type,
                object_id=object_id,
                min_score=min_score,
                created_at=created_at,
                fetch_command_builder=fetch_command_builder,
            )
            key = (candidate["node_id"], candidate["category"], candidate["url"])
            if key in seen:
                continue
            seen.add(key)
            candidates.append(candidate)
    candidates.sort(key=lambda row: (-int(row.get("accepted", False)), -int(row.get("score", 0)), row["task_id"], row["url"]))
    return candidates


def _read_search_results_by_task(path: Path | None) -> dict[str, list[dict[str, Any]]]:
    if path is None:
        return {}
    rows = _read_jsonl(path)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for index, row in enumerate(rows, start=1):
        if not isinstance(row.get("task_id"), str) or not row.get("task_id", "").strip():
            raise ValueError(f"search result row {index} missing task_id")
        if not isinstance(row.get("url"), str) or not row.get("url", "").strip():
            raise ValueError(f"search result row {index} missing url")
        grouped.setdefault(row["task_id"].strip(), []).append(row)
    return grouped


def _duckduckgo_search(query: str, limit: int, timeout: int) -> list[dict[str, Any]]:
    if not query.strip():
        return []
    url = "https://duckduckgo.com/html/?" + urllib.parse.urlencode({"q": query})
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "value-invest-research/0.1 (+https://local/research)"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            headers = getattr(response, "headers", {})
            content_type = headers.get("Content-Type", "") if hasattr(headers, "get") else ""
    except (OSError, TimeoutError, urllib.error.URLError) as exc:
        raise ValueError(f"failed to search sources for query {query}: {exc}") from exc
    html_text = raw.decode(_charset_from_content_type(content_type), errors="replace")
    return _parse_duckduckgo_results(html_text, limit)


def _parse_duckduckgo_results(html_text: str, limit: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    result_blocks = re.findall(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html_text, flags=re.I | re.S)
    snippets = re.findall(r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>|<div[^>]+class="result__snippet"[^>]*>(.*?)</div>', html_text, flags=re.I | re.S)
    snippet_texts = [_clean_html_text(left or right) for left, right in snippets]
    for index, (href, title_html) in enumerate(result_blocks[:limit]):
        rows.append(
            {
                "title": _clean_html_text(title_html),
                "url": _normalize_search_url(html.unescape(href)),
                "snippet": snippet_texts[index] if index < len(snippet_texts) else "",
            }
        )
    return rows


def _clean_html_text(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    return _collapse_space(html.unescape(text))


def _normalize_search_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.endswith("duckduckgo.com") and parsed.path.startswith("/l/"):
        query = urllib.parse.parse_qs(parsed.query)
        if query.get("uddg"):
            return query["uddg"][0]
    return url


def _candidate_from_search_result(
    task: dict[str, Any],
    raw: dict[str, Any],
    object_type: str,
    object_id: str,
    min_score: int,
    created_at: str,
    fetch_command_builder: Callable[[str, dict[str, Any]], str],
) -> dict[str, Any]:
    url = _collapse_space(raw.get("url", ""))
    title = _collapse_space(raw.get("title", "")) or _default_url_source_name({"title": ""}, url)
    snippet = _collapse_space(raw.get("snippet", ""))
    category = task.get("category", "")
    score, reasons = _score_source_candidate(task, title, url, snippet)
    source_type = _candidate_source_type(category, url, title)
    candidate = {
        "schema_version": "1.0",
        "candidate_id": _candidate_id(task, url),
        "task_id": task.get("task_id", ""),
        "object_type": object_type,
        "object_id": object_id,
        "node_id": task.get("node_id", ""),
        "category": category,
        "category_label": task.get("category_label", INFO_CATEGORY_LABEL_ZH.get(category, category)),
        "question": task.get("question", ""),
        "search_query": task.get("search_query", ""),
        "title": title,
        "url": url,
        "domain": urllib.parse.urlparse(url).netloc.lower(),
        "snippet": snippet,
        "source_type": source_type,
        "source_name": title,
        "summary": snippet,
        "reliability": _candidate_reliability(category, url, source_type),
        "materiality": DEFAULT_MATERIALITY.get(category, "medium"),
        "score": score,
        "accepted": bool(url and score >= min_score),
        "screening_reason": "；".join(reasons) if reasons else "未命中明确筛选规则。",
        "fetch_command": "",
        "created_at": created_at,
    }
    candidate["fetch_command"] = fetch_command_builder(object_id, candidate)
    return candidate


def _score_source_candidate(task: dict[str, Any], title: str, url: str, snippet: str) -> tuple[int, list[str]]:
    category = task.get("category", "")
    haystack = " ".join([title, url, snippet]).lower()
    matched_terms = [term for term in _keywords(task.get("question", "") + " " + task.get("search_query", "")) if term in haystack]
    score = min(len(matched_terms), 8)
    reasons = [f"匹配关键词 {len(matched_terms)} 个"] if matched_terms else []
    lowered_url = url.lower()
    lowered_title = title.lower()
    if category == "evidence":
        if _contains_any(lowered_url, OFFICIAL_DOMAIN_TOKENS):
            score += 8
            reasons.append("官方/监管/IR 域名")
        if any(token in lowered_title for token in ("annual report", "公告", "年报", "招股书", "results", "业绩")):
            score += 4
            reasons.append("标题包含公告或财报信号")
    elif category == "research_report":
        if _contains_any(lowered_url, RESEARCH_DOMAIN_TOKENS) or lowered_url.endswith(".pdf"):
            score += 7
            reasons.append("研报/PDF/研究域名")
        if any(token in title for token in ("研报", "深度", "证券", "行业研究", "报告")):
            score += 4
            reasons.append("标题包含研究报告信号")
    elif category == "message":
        if _contains_any(lowered_url, NEWS_DOMAIN_TOKENS):
            score += 6
            reasons.append("新闻媒体域名")
        if any(token in title for token in ("新闻", "报道", "消息", "进展", "发布")):
            score += 3
            reasons.append("标题包含消息信号")
    elif category == "opinion":
        if _contains_any(lowered_url, OPINION_DOMAIN_TOKENS):
            score += 6
            reasons.append("观点/社区域名")
        if any(token in title for token in ("访谈", "观点", "纪要", "专家", "解读")):
            score += 4
            reasons.append("标题包含观点信号")
    return score, reasons


def _contains_any(value: str, tokens: tuple[str, ...]) -> bool:
    return any(token in value for token in tokens)


def _candidate_source_type(category: str, url: str, title: str) -> str:
    lowered = f"{url} {title}".lower()
    if category == "evidence":
        if "sec.gov" in lowered:
            return "sec_filing"
        if _contains_any(lowered, OFFICIAL_DOMAIN_TOKENS):
            return "regulator_notice" if "gov" in lowered or "hkex" in lowered else "company_ir"
        return "company_ir"
    if category == "research_report":
        return "sell_side_report"
    if category == "opinion":
        return "opinion"
    return "news"


def _candidate_reliability(category: str, url: str, source_type: str) -> str:
    lowered = url.lower()
    if category == "evidence":
        return "primary" if source_type in {"sec_filing", "regulator_notice", "company_ir"} and _contains_any(lowered, OFFICIAL_DOMAIN_TOKENS) else "high"
    if category == "research_report":
        return "high"
    if category == "message":
        return "low"
    return "medium"


def _candidate_id(task: dict[str, Any], url: str) -> str:
    digest = hashlib.sha1(f"{task.get('task_id', '')}\n{url}".encode("utf-8")).hexdigest()[:12]
    return f"candidate_{digest}"


def _stock_fetch_candidate_command(ticker: str, candidate: dict[str, Any]) -> str:
    return _fetch_candidate_command("fetch-question-information-url", ticker, candidate)


def _meta_qa_fetch_candidate_command(project_id: str, candidate: dict[str, Any]) -> str:
    return _fetch_candidate_command("fetch-meta-qa-information-url", project_id, candidate)


def _fetch_candidate_command(command: str, object_id: str, candidate: dict[str, Any]) -> str:
    parts = ["value-invest-research", command]
    if command == "fetch-question-information-url":
        parts.append(shlex.quote(object_id))
    else:
        parts.extend(["--project-id", shlex.quote(object_id)])
    parts.extend(
        [
            "--node-id",
            shlex.quote(candidate.get("node_id", "")),
            "--category",
            shlex.quote(candidate.get("category", "")),
            "--url",
            shlex.quote(candidate.get("url", "")),
            "--source-type",
            shlex.quote(candidate.get("source_type", "")),
            "--source-name",
            shlex.quote(candidate.get("source_name", "")),
            "--reliability",
            shlex.quote(candidate.get("reliability", "")),
            "--materiality",
            shlex.quote(candidate.get("materiality", "")),
        ]
    )
    return " ".join(parts)


def _validated_candidate_row(row: dict[str, Any]) -> dict[str, Any]:
    required = ["node_id", "category", "url", "source_type", "source_name", "reliability", "materiality"]
    missing = [key for key in required if not isinstance(row.get(key), str) or not row.get(key, "").strip()]
    if missing:
        raise ValueError(f"candidate missing required fields: {', '.join(missing)}")
    category = row["category"].strip()
    if category not in SOURCE_ORIGIN_INFO_ORDER:
        raise ValueError(f"candidate category must be one of {SOURCE_ORIGIN_INFO_ORDER}")
    score = int(row.get("score", 0) or 0)
    return {
        **row,
        "node_id": row["node_id"].strip(),
        "category": category,
        "url": row["url"].strip(),
        "source_type": row["source_type"].strip(),
        "source_name": row["source_name"].strip(),
        "reliability": row["reliability"].strip(),
        "materiality": row["materiality"].strip(),
        "score": score,
        "accepted": bool(row.get("accepted")),
    }


def _tasks_from_collection_rows(
    rows: list[dict[str, Any]],
    object_type: str,
    object_id: str,
    include_matched: bool,
    bind_command_builder: Callable[[str, dict[str, Any]], str],
) -> list[dict[str, Any]]:
    created_at = datetime.now(timezone.utc).isoformat()
    tasks = []
    for row in rows:
        status = row.get("status", "missing")
        if status == "matched" and not include_matched:
            continue
        category = row.get("category", "")
        if category not in SOURCE_ORIGIN_INFO_ORDER:
            continue
        task = {
            "schema_version": "1.0",
            "task_id": _task_id(object_type, object_id, row),
            "object_type": object_type,
            "object_id": object_id,
            "node_id": row.get("node_id", ""),
            "parent_id": row.get("parent_id", ""),
            "section_id": row.get("section_id", ""),
            "question": row.get("question", ""),
            "category": category,
            "category_label": row.get("category_label", INFO_CATEGORY_LABEL_ZH.get(category, category)),
            "status": status,
            "matched_count": int(row.get("matched_count", 0) or 0),
            "priority": _task_priority(row),
            "search_query": row.get("search_query", ""),
            "recommended_sources": RECOMMENDED_SOURCES[category],
            "acceptance_criteria": ACCEPTANCE_CRITERIA[category],
            "expected_output_fields": EXPECTED_SOURCE_FIELDS,
            "default_reliability": DEFAULT_RELIABILITY[category],
            "default_materiality": DEFAULT_MATERIALITY[category],
            "next_action": row.get("next_action", ""),
            "bind_command": bind_command_builder(object_id, row),
            "created_at": created_at,
        }
        tasks.append(task)
    tasks.sort(key=lambda item: (-item["priority"], item["node_id"], SOURCE_ORIGIN_INFO_ORDER.index(item["category"])))
    return tasks


def _local_collection_matches(
    tasks: list[dict[str, Any]],
    records: list[EvidenceRecord],
    link_builder: Callable[[str], str],
    min_score: int,
    max_sources_per_task: int,
) -> list[dict[str, Any]]:
    if min_score < 0:
        raise ValueError("min_score must be non-negative")
    if max_sources_per_task <= 0:
        raise ValueError("max_sources_per_task must be positive")

    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()
    for task in tasks:
        node_id = task.get("node_id", "")
        category = task.get("category", "")
        if not node_id or category not in SOURCE_ORIGIN_INFO_ORDER:
            continue
        link = link_builder(node_id)
        scored = [
            candidate
            for candidate in (
                _score_record_for_task(task, record, link)
                for record in records
                if record.information_category == category and link not in record.used_in
            )
            if candidate["score"] >= min_score
        ]
        scored.sort(
            key=lambda item: (
                -item["score"],
                -RELIABILITY_SCORE.get(item["reliability"], 0),
                -MATERIALITY_SCORE.get(item["materiality"], 0),
                item["source_name"],
            )
        )
        for candidate in scored[:max_sources_per_task]:
            key = (node_id, category, candidate["url"], candidate["summary"])
            if key in seen:
                continue
            seen.add(key)
            rows.append(candidate)
    return rows


def _score_record_for_task(task: dict[str, Any], record: EvidenceRecord, link: str) -> dict[str, Any]:
    task_text = " ".join(
        [
            task.get("question", ""),
            task.get("search_query", ""),
            task.get("section_id", ""),
            task.get("category_label", ""),
        ]
    )
    record_text = " ".join(
        [
            record.source_type,
            record.source_name,
            record.summary,
            " ".join(record.themes),
            " ".join(record.sectors),
        ]
    )
    terms = _keywords(task_text)
    record_text_lower = record_text.lower()
    matched_terms = [term for term in terms if term in record_text_lower]
    direct_match = record.id in task.get("matched_evidence_ids", [])
    if not matched_terms and not direct_match:
        score = 0
    else:
        score = len(matched_terms)
        score += min(RELIABILITY_SCORE.get(record.reliability, 0), 3)
        score += min(MATERIALITY_SCORE.get(record.materiality, 0), 3)
        if record.information_category == task.get("category"):
            score += 2
    if direct_match:
        score += 4
    return {
        "node_id": task.get("node_id", ""),
        "category": task.get("category", ""),
        "source_type": record.source_type,
        "source_name": record.source_name,
        "url": record.url,
        "summary": record.summary,
        "reliability": record.reliability,
        "materiality": record.materiality,
        "published_at": record.published_at,
        "score": score,
        "matched_terms": matched_terms[:12],
        "task_id": task.get("task_id", ""),
        "existing_evidence_id": record.id,
        "existing_link": link,
    }


def _keywords(text: str) -> list[str]:
    lowered = text.lower()
    raw_tokens = re.findall(r"[a-z0-9][a-z0-9_\-]{1,}|[\u4e00-\u9fff]{2,}", lowered)
    terms: list[str] = []
    stopwords = {
        "xiaomi",
        "aapl",
        "公司",
        "问题",
        "回答",
        "需要",
        "什么",
        "是否",
        "哪些",
        "如何",
        "以及",
        "当前",
        "证据",
        "研报",
        "消息",
        "观点",
        "年报",
        "公告",
        "招股书",
        "监管",
        "披露",
        "深度报告",
        "行业研究",
    }
    for token in raw_tokens:
        if token in stopwords:
            continue
        if _is_cjk_token(token):
            terms.extend(_cjk_grams(token))
        else:
            terms.append(token)
    return list(dict.fromkeys(term for term in terms if len(term) >= 2 and term not in stopwords))


def _is_cjk_token(token: str) -> bool:
    return bool(re.fullmatch(r"[\u4e00-\u9fff]+", token))


def _cjk_grams(token: str) -> list[str]:
    if len(token) <= 4:
        return [token]
    grams: list[str] = []
    for size in (2, 3, 4):
        grams.extend(token[index : index + size] for index in range(0, len(token) - size + 1))
    return grams


def _task_priority(row: dict[str, Any]) -> int:
    status_score = {"missing": 100, "needs_source_record": 80, "matched": 20}.get(row.get("status", ""), 50)
    category_score = {"evidence": 30, "research_report": 20, "message": 10, "opinion": 5}.get(row.get("category", ""), 0)
    matched_count = int(row.get("matched_count", 0) or 0)
    return status_score + category_score - min(matched_count, 5)


def _stock_bind_command(ticker: str, row: dict[str, Any]) -> str:
    category = row.get("category", "")
    return " ".join(
        [
            "value-invest-research",
            "record-question-information",
            shlex.quote(ticker),
            "--node-id",
            shlex.quote(row.get("node_id", "")),
            "--category",
            shlex.quote(category),
            "--source-type",
            "<source_type>",
            "--source-name",
            "\"<source_name>\"",
            "--url",
            "\"<url>\"",
            "--summary",
            "\"<summary>\"",
            "--reliability",
            DEFAULT_RELIABILITY.get(category, "medium"),
            "--materiality",
            DEFAULT_MATERIALITY.get(category, "medium"),
        ]
    )


def _meta_qa_bind_command(project_id: str, row: dict[str, Any]) -> str:
    category = row.get("category", "")
    return " ".join(
        [
            "value-invest-research",
            "record-meta-qa-information",
            "--project-id",
            shlex.quote(project_id),
            "--node-id",
            shlex.quote(row.get("node_id", "")),
            "--category",
            shlex.quote(category),
            "--source-type",
            "<source_type>",
            "--source-name",
            "\"<source_name>\"",
            "--url",
            "\"<url>\"",
            "--summary",
            "\"<summary>\"",
            "--reliability",
            DEFAULT_RELIABILITY.get(category, "medium"),
            "--materiality",
            DEFAULT_MATERIALITY.get(category, "medium"),
        ]
    )


def _import_rows(
    rows: list[dict[str, Any]],
    import_one: Callable[[dict[str, Any]], dict[str, Any]],
    result_base: dict[str, Any],
) -> dict[str, Any]:
    created = updated = existing = 0
    last_result: dict[str, Any] = {}
    for index, raw_row in enumerate(rows, start=1):
        row = _validated_import_row(raw_row, index)
        last_result = import_one(row)
        if last_result.get("created"):
            created += 1
        elif last_result.get("updated"):
            updated += 1
        else:
            existing += 1
    return {
        **result_base,
        "records": len(rows),
        "created": created,
        "updated": updated,
        "existing": existing,
        "dashboard_path": last_result.get("dashboard_path", ""),
        "report_path": last_result.get("report_path", ""),
        "information_collection_path": last_result.get("information_collection_path", ""),
    }


def _validated_import_row(row: dict[str, Any], index: int) -> dict[str, Any]:
    if not isinstance(row, dict):
        raise ValueError(f"import row {index} must be an object")
    required = ["node_id", "category", "source_type", "source_name", "url", "summary"]
    missing = [field for field in required if not isinstance(row.get(field), str) or not row.get(field, "").strip()]
    if missing:
        raise ValueError(f"import row {index} missing required fields: {', '.join(missing)}")
    category = row["category"].strip()
    if category not in SOURCE_ORIGIN_INFO_ORDER:
        raise ValueError(f"import row {index} category must be one of {SOURCE_ORIGIN_INFO_ORDER}")
    normalized = {**row, "category": category}
    for key in ["node_id", "source_type", "source_name", "url", "summary"]:
        normalized[key] = row[key].strip()
    return normalized


def _task_id(object_type: str, object_id: str, row: dict[str, Any]) -> str:
    digest = hashlib.sha1(
        f"{object_type}\n{object_id}\n{row.get('node_id', '')}\n{row.get('category', '')}".encode("utf-8")
    ).hexdigest()[:12]
    return f"collect_{digest}"


def _leaf_question_count(qa_tree: dict[str, Any]) -> int:
    nodes = {node.get("id"): node for node in qa_tree.get("nodes", [])}
    return sum(
        1
        for node in nodes.values()
        if int(node.get("level", 0)) >= int(qa_tree.get("default_depth", 3)) or not node.get("next_question_ids")
    )


def _limit_tasks(tasks: list[dict[str, Any]], limit: int | None) -> list[dict[str, Any]]:
    if limit is None:
        return tasks
    if limit < 0:
        raise ValueError("limit must be non-negative")
    return tasks[:limit]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: {exc}") from exc
    return rows


def _read_evidence_records(path: Path) -> list[EvidenceRecord]:
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


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
