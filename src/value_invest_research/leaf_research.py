from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LEAF_TASK_FILE = "leaf_research_tasks.jsonl"
LEAF_RESULT_FILE = "leaf_research_results.jsonl"
LEAF_SOURCE_FILE = "leaf_research_sources.jsonl"
LEAF_ANSWER_FILE = "leaf_answers.jsonl"
ROLLUP_ANSWER_FILE = "rollup_answers.jsonl"
LEAF_RAW_DIR = "leaf_research_raw"
INFO_CATEGORIES = ["evidence", "research_report", "message", "opinion"]


def build_leaf_research_tasks(
    root: Path,
    ticker: str,
    limit: int | None = None,
    include_completed: bool = False,
) -> dict[str, Any]:
    """Create provider-agnostic research tasks for terminal QA nodes."""
    from value_invest_research.research_system import build_research_system, normalize_ticker

    if limit is not None and limit < 0:
        raise ValueError("limit must be non-negative")
    normalized = normalize_ticker(ticker)
    build_result = build_research_system(root, normalized)
    research_dir = Path(build_result["qa_tree_path"]).parent
    qa_tree = _read_json(research_dir / "qa_tree.json")
    completed = _completed_leaf_node_ids(research_dir) if not include_completed else set()
    tasks = _leaf_tasks_from_tree(
        qa_tree,
        ticker=normalized,
        company_name=_company_name(root, normalized),
        completed_node_ids=completed,
        limit=limit,
    )
    task_path = research_dir / LEAF_TASK_FILE
    _write_jsonl(task_path, tasks)
    return {
        **build_result,
        "ticker": normalized,
        "task_path": str(task_path),
        "tasks": len(tasks),
        "leaf_questions": _leaf_question_count(qa_tree),
        "include_completed": include_completed,
    }


class ResearchSearchProvider:
    """Provider-agnostic search interface for leaf research."""

    name = "base"
    model = "base"

    def search(self, task: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class MockResearchSearchProvider(ResearchSearchProvider):
    """Deterministic provider for tests and dry runs."""

    name = "mock"
    model = "mock-leaf-research-v1"

    def search(self, task: dict[str, Any]) -> dict[str, Any]:
        question = task.get("question", "")
        source_url = f"https://example.com/mock-leaf-research/{task.get('task_id', '')}"
        return {
            "provider": self.name,
            "provider_model": self.model,
            "task_id": task.get("task_id", ""),
            "node_id": task.get("node_id", ""),
            "query": question,
            "task_family": task.get("task_family", ""),
            "selected_skill": task.get("selected_skill", ""),
            "source_plan": task.get("source_search_plan", []),
            "extraction_schema": task.get("extraction_schema", {}),
            "skill_dispatch_trace": task.get("skill_dispatch_trace", {}),
            "answer": f"Mock answer: {question} needs primary evidence, third-party research, timely messages, and expert opinions before parent rollup.",
            "facts": [f"Mock fact: task {task.get('task_id', '')} preserves the leaf question and required evidence contract."],
            "inferences": ["Mock inference: a leaf-level answer should be sourced before being rolled up."],
            "judgment": "Mock judgment: provisional until a real search provider supplies cited material.",
            "supporting_evidence": ["Mock support: provider result contains one cited research-report source."],
            "refuting_evidence": [],
            "research_leads": ["Replace mock output with Perplexity/Tavily/Exa/OpenAI Search adapter results."],
            "gaps": task.get("required_evidence", [])[:3] or ["Need direct sources for the leaf question."],
            "confidence": "low",
            "sources": [
                {
                    "url": source_url,
                    "title": f"Mock source for {question[:40]}",
                    "publisher": "Mock Research Provider",
                    "author": "value-invest-research",
                    "published_at": _now_iso(),
                    "source_type": "research_report",
                    "information_category": "research_report",
                    "reliability": "high",
                    "materiality": "medium",
                    "summary": "Synthetic source used to verify provider-agnostic plumbing.",
                    "quoted_or_extracted_points": ["Leaf answers must remain citation-backed."],
                }
            ],
        }


class OpenAICompatibleResearchSearchProvider(ResearchSearchProvider):
    """Generic OpenAI-compatible chat completions provider."""

    name = "openai_compatible"

    def __init__(
        self,
        *,
        provider_name: str | None = None,
        api_key_env: str = "LEAF_RESEARCH_API_KEY",
        model_env: str = "LEAF_RESEARCH_MODEL",
        base_url_env: str = "LEAF_RESEARCH_BASE_URL",
        endpoint_env: str = "LEAF_RESEARCH_ENDPOINT",
        timeout_env: str = "LEAF_RESEARCH_TIMEOUT",
        default_provider_name: str = "openai_compatible",
        default_model: str = "search-model",
        default_base_url: str = "https://api.openai.com/v1",
    ) -> None:
        api_key = os.environ.get(api_key_env, "").strip()
        if not api_key:
            raise ValueError(
                f"{api_key_env} is required for provider={default_provider_name}. "
                "Set the environment variable or use provider=mock/manual."
            )
        self.api_key = api_key
        self.name = provider_name or os.environ.get("LEAF_RESEARCH_PROVIDER_NAME", default_provider_name).strip() or default_provider_name
        self.model = os.environ.get(model_env, default_model).strip() or default_model
        base_url = os.environ.get(base_url_env, default_base_url).strip().rstrip("/")
        self.endpoint = os.environ.get(endpoint_env, f"{base_url}/chat/completions").strip()
        self.timeout = int(os.environ.get(timeout_env, "60"))

    def search(self, task: dict[str, Any]) -> dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": _provider_system_prompt()},
                {"role": "user", "content": _provider_user_prompt(task)},
            ],
            "temperature": 0.2,
        }
        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                response_body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ValueError(f"Perplexity request failed with HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ValueError(f"Perplexity request failed: {exc.reason}") from exc
        raw_response = json.loads(response_body)
        result = _provider_result_from_chat_response(task, raw_response, provider=self.name, default_model=self.model)
        result["_raw_provider_response"] = raw_response
        return result


class PerplexityResearchSearchProvider(OpenAICompatibleResearchSearchProvider):
    """Perplexity Sonar adapter using the OpenAI-compatible chat completions API."""

    def __init__(self) -> None:
        super().__init__(
            provider_name="perplexity",
            api_key_env="PERPLEXITY_API_KEY",
            model_env="PERPLEXITY_MODEL",
            base_url_env="PERPLEXITY_BASE_URL",
            endpoint_env="PERPLEXITY_ENDPOINT",
            timeout_env="PERPLEXITY_TIMEOUT",
            default_provider_name="perplexity",
            default_model="sonar-pro",
            default_base_url="https://api.perplexity.ai",
        )


def run_leaf_research(
    root: Path,
    ticker: str,
    provider: str = "mock",
    input_path: Path | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """Run leaf research tasks through a configured provider."""
    if provider == "manual":
        if input_path is None:
            raise ValueError("manual provider requires input_path")
        return import_leaf_research_results(root, ticker, input_path)

    task_result = build_leaf_research_tasks(root, ticker, limit=limit)
    research_dir = Path(task_result["task_path"]).parent
    tasks = _read_jsonl(Path(task_result["task_path"]))
    raw_dir = research_dir / LEAF_RAW_DIR
    raw_dir.mkdir(parents=True, exist_ok=True)
    search_provider = _provider_for_name(provider)
    rows: list[dict[str, Any]] = []
    for task in tasks:
        provider_result = search_provider.search(task)
        raw_path = raw_dir / f"{task['task_id']}.json"
        raw_payload = provider_result.pop("_raw_provider_response", provider_result)
        raw_path.write_text(json.dumps(raw_payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        provider_result["raw_response_path"] = str(raw_path)
        rows.append(_normalize_provider_result(provider_result))
    result_path = research_dir / LEAF_RESULT_FILE
    source_path, source_count = _save_leaf_results(research_dir, rows)
    return {
        **task_result,
        "provider": provider,
        "result_path": str(result_path),
        "source_path": str(source_path),
        "raw_dir": str(raw_dir),
        "results": len(rows),
        "sources": source_count,
    }


def _provider_for_name(provider: str) -> ResearchSearchProvider:
    if provider == "mock":
        return MockResearchSearchProvider()
    if provider == "perplexity":
        return PerplexityResearchSearchProvider()
    if provider == "openai_compatible":
        return OpenAICompatibleResearchSearchProvider()
    raise ValueError(f"Unsupported leaf research provider: {provider}")


def _provider_system_prompt() -> str:
    return (
        "You are a professional equity research search agent. "
        "Answer one leaf research question with cited sources. "
        "Return only a JSON object. Do not provide trading instructions."
    )


def _provider_user_prompt(task: dict[str, Any]) -> str:
    compact_task = {
        "ticker": task.get("ticker", ""),
        "company_name": task.get("company_name", ""),
        "node_id": task.get("node_id", ""),
        "section_id": task.get("section_id", ""),
        "question": task.get("question", ""),
        "parent_question": task.get("parent_question", ""),
        "framework_context": task.get("framework_context", ""),
        "required_evidence": task.get("required_evidence", []),
        "disconfirming_signals": task.get("disconfirming_signals", []),
        "decision_rule": task.get("decision_rule", ""),
        "information_categories": task.get("information_categories", INFO_CATEGORIES),
        "task_family": task.get("task_family", ""),
        "selected_skill": task.get("selected_skill", ""),
        "source_search_plan": task.get("source_search_plan", []),
        "extraction_schema": task.get("extraction_schema", {}),
        "skill_dispatch_trace": task.get("skill_dispatch_trace", {}),
        "max_sources": task.get("max_sources", 8),
    }
    output_contract = {
        "answer": "direct answer to the leaf question",
        "facts": ["verifiable facts with source context"],
        "inferences": ["mechanisms or assumptions inferred from facts"],
        "judgment": "bounded current judgment",
        "materiality": "why this answer changes parent conclusion, target strength, valuation odds, or risk controls",
        "source_plan": ["source plan items actually used or still needed"],
        "extraction_schema": {"field": "extracted value discipline"},
        "skill_dispatch_trace": {
            "task_family": "selected task family",
            "selected_skill": "selected specialty skill",
            "concrete_materials": ["materials read"],
            "skill_output_status": "drafted|partial|failed|fallback",
            "fallback_used": "",
            "gpt_verification_status": "pending_provider_output",
        },
        "supporting_evidence": ["source-backed support"],
        "refuting_evidence": ["source-backed refutation or disconfirming material"],
        "research_leads": ["low-confidence leads only"],
        "gaps": ["remaining missing data"],
        "confidence": "low|medium|high",
        "sources": [
            {
                "url": "source URL",
                "title": "source title",
                "publisher": "publisher",
                "author": "author if available",
                "published_at": "publication date if available",
                "source_type": "annual_report|press_release|research_report|news|opinion|database|other",
                "information_category": "evidence|research_report|message|opinion",
                "reliability": "primary|high|medium|low",
                "materiality": "low|medium|high|thesis_change",
                "summary": "source-specific summary",
                "quoted_or_extracted_points": ["short extracted points"],
            }
        ],
    }
    return "\n".join(
        [
            "Research this leaf question. Prefer primary filings/company releases, then high-quality third-party research, then messages/news, then opinions.",
            "Classify every source into exactly one information category: evidence, research_report, message, or opinion.",
            "Separate facts, inferences, judgment, refuting evidence, research leads, and gaps.",
            "Return JSON only with this output contract:",
            json.dumps(output_contract, ensure_ascii=False, indent=2),
            "",
            "Leaf task:",
            json.dumps(compact_task, ensure_ascii=False, indent=2, sort_keys=True),
        ]
    )


def import_leaf_research_results(root: Path, ticker: str, path: Path) -> dict[str, Any]:
    """Import provider-agnostic leaf research results from JSONL."""
    from value_invest_research.research_system import build_research_system, normalize_ticker

    normalized = normalize_ticker(ticker)
    build_result = build_research_system(root, normalized)
    research_dir = Path(build_result["qa_tree_path"]).parent
    rows = [_normalize_provider_result(row) for row in _read_jsonl(path)]
    result_path = research_dir / LEAF_RESULT_FILE
    source_path, source_count = _save_leaf_results(research_dir, rows)
    return {
        **build_result,
        "ticker": normalized,
        "input_path": str(path),
        "result_path": str(result_path),
        "source_path": str(source_path),
        "records": len(rows),
        "sources": source_count,
    }


def _provider_result_from_chat_response(
    task: dict[str, Any],
    raw_response: dict[str, Any],
    provider: str,
    default_model: str,
) -> dict[str, Any]:
    content = _chat_response_content(raw_response)
    parsed = _extract_json_object(content)
    search_sources = _sources_from_search_results(raw_response)
    sources = parsed.get("sources") if isinstance(parsed.get("sources"), list) else []
    if not sources:
        sources = search_sources
    return {
        "provider": provider,
        "provider_model": raw_response.get("model") or default_model,
        "task_id": task.get("task_id", ""),
        "node_id": task.get("node_id", ""),
        "query": task.get("question", ""),
        "answer": parsed.get("answer") or content,
        "facts": _text_list(parsed.get("facts")),
        "inferences": _text_list(parsed.get("inferences")),
        "judgment": parsed.get("judgment", ""),
        "supporting_evidence": _text_list(parsed.get("supporting_evidence")),
        "refuting_evidence": _text_list(parsed.get("refuting_evidence")),
        "research_leads": _text_list(parsed.get("research_leads")),
        "gaps": _text_list(parsed.get("gaps")),
        "confidence": parsed.get("confidence", "unknown"),
        "materiality": parsed.get("materiality") or task.get("materiality", ""),
        "source_plan": parsed.get("source_plan") if isinstance(parsed.get("source_plan"), list) else task.get("source_search_plan", []),
        "extraction_schema": parsed.get("extraction_schema") if isinstance(parsed.get("extraction_schema"), dict) else task.get("extraction_schema", {}),
        "task_family": parsed.get("task_family") or task.get("task_family", ""),
        "selected_skill": parsed.get("selected_skill") or task.get("selected_skill", ""),
        "skill_dispatch_trace": parsed.get("skill_dispatch_trace")
        if isinstance(parsed.get("skill_dispatch_trace"), dict)
        else task.get("skill_dispatch_trace", {}),
        "sources": sources,
    }


def _chat_response_content(raw_response: dict[str, Any]) -> str:
    try:
        content = raw_response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("provider response missing choices[0].message.content") from exc
    if isinstance(content, list):
        return "\n".join(str(item.get("text", item)) if isinstance(item, dict) else str(item) for item in content)
    return str(content)


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


def _sources_from_search_results(raw_response: dict[str, Any]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for item in raw_response.get("search_results", []) or []:
        if not isinstance(item, dict):
            continue
        url = str(item.get("url", "")).strip()
        if not url:
            continue
        category = _infer_information_category_from_url(url)
        sources.append(
            {
                "url": url,
                "title": item.get("title", ""),
                "publisher": item.get("publisher", ""),
                "author": item.get("author", ""),
                "published_at": item.get("date", "") or item.get("published_at", ""),
                "source_type": item.get("source_type", category),
                "information_category": category,
                "reliability": _default_reliability(category),
                "materiality": "medium",
                "summary": item.get("snippet", "") or item.get("summary", ""),
                "quoted_or_extracted_points": [],
            }
        )
    known_urls = {source["url"] for source in sources}
    for url in raw_response.get("citations", []) or []:
        url = str(url).strip()
        if not url or url in known_urls:
            continue
        category = _infer_information_category_from_url(url)
        sources.append(
            {
                "url": url,
                "title": url,
                "publisher": "",
                "author": "",
                "published_at": "",
                "source_type": category,
                "information_category": category,
                "reliability": _default_reliability(category),
                "materiality": "medium",
                "summary": "Citation returned by provider.",
                "quoted_or_extracted_points": [],
            }
        )
    return sources


def synthesize_leaf_answers(root: Path, ticker: str) -> dict[str, Any]:
    """Turn normalized provider results into detailed leaf-node answers."""
    from value_invest_research.research_system import build_research_system, normalize_ticker

    normalized = normalize_ticker(ticker)
    build_result = build_research_system(root, normalized)
    research_dir = Path(build_result["qa_tree_path"]).parent
    results = _read_jsonl(research_dir / LEAF_RESULT_FILE)
    latest_by_node: dict[str, dict[str, Any]] = {}
    for row in results:
        latest_by_node[row.get("node_id", "")] = row
    answers = [_leaf_answer_from_result(row) for row in latest_by_node.values() if row.get("node_id")]
    answer_path = research_dir / LEAF_ANSWER_FILE
    _write_jsonl(answer_path, answers)
    return {
        **build_result,
        "ticker": normalized,
        "answer_path": str(answer_path),
        "answers": len(answers),
        "source_result_path": str(research_dir / LEAF_RESULT_FILE),
    }


def rollup_research_answers(root: Path, ticker: str) -> dict[str, Any]:
    """Persist parent-level rollups after leaf answers have been applied."""
    from value_invest_research.research_system import build_research_system, normalize_ticker

    normalized = normalize_ticker(ticker)
    build_result = build_research_system(root, normalized)
    research_dir = Path(build_result["qa_tree_path"]).parent
    qa_tree = _read_json(research_dir / "qa_tree.json")
    rows = []
    for node in qa_tree.get("nodes", []):
        rollup_sources = node.get("metadata", {}).get("rollup_sources", [])
        if _is_leaf_node(qa_tree, node) or not rollup_sources:
            continue
        professional = node.get("professional_answer", {})
        rows.append(
            {
                "schema_version": "1.0",
                "source": "leaf_research_rollup",
                "node_id": node.get("id", ""),
                "parent_id": node.get("parent_id", ""),
                "level": node.get("level", 0),
                "section_id": node.get("section_id", ""),
                "question": node.get("question", ""),
                "answer": professional.get("answer") or node.get("current_answer", ""),
                "facts": _text_list(professional.get("facts")),
                "inferences": _text_list(professional.get("inferences")),
                "judgment": professional.get("judgment", ""),
                "gaps": _text_list(professional.get("gaps")),
                "confidence": professional.get("confidence", "unknown"),
                "source_balance": professional.get("source_balance", ""),
                "supporting_evidence": _text_list(professional.get("supporting_evidence")),
                "refuting_evidence": _text_list(professional.get("refuting_evidence")),
                "research_leads": _text_list(professional.get("research_leads")),
                "rollup": professional.get("rollup", ""),
                "rollup_sources": rollup_sources,
            }
        )
    rollup_path = research_dir / ROLLUP_ANSWER_FILE
    _write_jsonl(rollup_path, rows)
    return {
        **build_result,
        "ticker": normalized,
        "rollup_path": str(rollup_path),
        "rollups": len(rows),
    }


def _save_leaf_results(research_dir: Path, rows: list[dict[str, Any]]) -> tuple[Path, int]:
    result_path = research_dir / LEAF_RESULT_FILE
    existing_rows = _read_jsonl(result_path)
    merged_rows = _merge_leaf_result_rows(existing_rows, rows)
    _write_jsonl(result_path, merged_rows)
    sources = _deduplicated_sources(merged_rows)
    source_path = research_dir / LEAF_SOURCE_FILE
    _write_jsonl(source_path, sources)
    return source_path, len(sources)


def _merge_leaf_result_rows(existing_rows: list[dict[str, Any]], new_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = list(existing_rows)
    index_by_key = {_leaf_result_key(row): index for index, row in enumerate(merged)}
    for row in new_rows:
        key = _leaf_result_key(row)
        if key in index_by_key:
            merged[index_by_key[key]] = row
            continue
        index_by_key[key] = len(merged)
        merged.append(row)
    return merged


def _leaf_result_key(row: dict[str, Any]) -> str:
    task_id = str(row.get("task_id", "")).strip()
    if task_id:
        return f"task:{task_id}"
    return "|".join(
        [
            "node",
            str(row.get("node_id", "")).strip(),
            str(row.get("provider", "")).strip(),
            str(row.get("query", "")).strip(),
        ]
    )


def _deduplicated_sources(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key: dict[str, dict[str, Any]] = {}
    for row in rows:
        for source in row.get("sources", []):
            key = _source_key(source)
            existing = by_key.get(key)
            if existing is None:
                existing = {
                    **source,
                    "source_id": _stable_source_id(key),
                    "node_ids": [],
                    "task_ids": [],
                    "result_count": 0,
                }
                by_key[key] = existing
            node_id = row.get("node_id", "")
            task_id = row.get("task_id", "")
            if node_id and node_id not in existing["node_ids"]:
                existing["node_ids"].append(node_id)
            if task_id and task_id not in existing["task_ids"]:
                existing["task_ids"].append(task_id)
            existing["result_count"] += 1
    return sorted(by_key.values(), key=lambda item: (item.get("url", ""), item.get("title", "")))


def _leaf_answer_from_result(row: dict[str, Any]) -> dict[str, Any]:
    sources = row.get("sources", [])
    source_balance = _source_balance(sources)
    strengthening_sources = [source for source in sources if source.get("reliability") != "low"]
    low_reliability_sources = [source for source in sources if source.get("reliability") == "low"]
    supporting = list(row.get("supporting_evidence", [])) if strengthening_sources else []
    supporting.extend(_source_support_lines(strengthening_sources))
    leads = list(row.get("research_leads", []))
    leads.extend(_source_support_lines(low_reliability_sources))
    return {
        "schema_version": "1.0",
        "source": "leaf_research",
        "synthesis_source": "leaf_research",
        "node_id": row.get("node_id", ""),
        "answer": row.get("answer", ""),
        "facts": _text_list(row.get("facts")),
        "inferences": _text_list(row.get("inferences")),
        "judgment": row.get("judgment", ""),
        "gaps": _text_list(row.get("gaps")),
        "next_data": _text_list(row.get("gaps")),
        "confidence": row.get("confidence", "unknown"),
        "source_balance": source_balance,
        "supporting_evidence": supporting,
        "refuting_evidence": _text_list(row.get("refuting_evidence")),
        "research_leads": leads,
        "rollup": f"{row.get('query', '')}：{row.get('judgment') or row.get('answer', '')}",
        "provider": row.get("provider", ""),
        "provider_model": row.get("provider_model", ""),
        "task_id": row.get("task_id", ""),
        "source_index": sources,
        "source_urls": [source.get("url", "") for source in sources if source.get("url")],
    }


def _source_support_lines(sources: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for source in sources:
        title = source.get("title") or source.get("url") or "source"
        summary = source.get("summary", "")
        lines.append(f"{title}：{summary}".strip("："))
    return lines


def _source_balance(sources: list[dict[str, Any]]) -> str:
    counts = {category: 0 for category in INFO_CATEGORIES}
    for source in sources:
        category = source.get("information_category", "")
        if category in counts:
            counts[category] += 1
    return f"证据 {counts['evidence']} / 研报 {counts['research_report']} / 消息 {counts['message']} / 观点 {counts['opinion']}"


def _source_key(source: dict[str, Any]) -> str:
    url = str(source.get("url", "")).strip().lower()
    if url:
        return f"url:{url}"
    return f"title:{source.get('title', '').strip().lower()}:{source.get('publisher', '').strip().lower()}"


def _stable_source_id(key: str) -> str:
    return f"leaf_source_{hashlib.sha256(key.encode('utf-8')).hexdigest()[:12]}"


def _normalize_provider_result(row: dict[str, Any]) -> dict[str, Any]:
    executed_at = row.get("executed_at") or _now_iso()
    sources = [_normalize_source(source, executed_at) for source in row.get("sources", [])]
    normalized = {
        "schema_version": "1.0",
        "provider": row.get("provider", "manual"),
        "provider_model": row.get("provider_model", ""),
        "task_id": row.get("task_id", ""),
        "node_id": row.get("node_id", ""),
        "query": row.get("query", ""),
        "executed_at": executed_at,
        "raw_response_path": row.get("raw_response_path", ""),
        "sources": sources,
        "answer": row.get("answer", ""),
        "facts": _text_list(row.get("facts")),
        "inferences": _text_list(row.get("inferences")),
        "judgment": row.get("judgment", ""),
        "supporting_evidence": _text_list(row.get("supporting_evidence")),
        "refuting_evidence": _text_list(row.get("refuting_evidence")),
        "research_leads": _text_list(row.get("research_leads")),
        "gaps": _text_list(row.get("gaps")),
        "confidence": row.get("confidence", "unknown"),
        "materiality": row.get("materiality", ""),
        "source_plan": row.get("source_plan", []),
        "extraction_schema": row.get("extraction_schema", {}),
        "task_family": row.get("task_family", ""),
        "selected_skill": row.get("selected_skill", ""),
        "skill_dispatch_trace": row.get("skill_dispatch_trace", {}),
    }
    if not normalized["node_id"]:
        raise ValueError("leaf research result missing node_id")
    if not sources:
        raise ValueError(f"leaf research result for {normalized['node_id']} has no sources")
    return normalized


def _normalize_source(source: dict[str, Any], accessed_at: str) -> dict[str, Any]:
    category = source.get("information_category") or _infer_information_category(source)
    return {
        "url": source.get("url", ""),
        "title": source.get("title", "") or source.get("source_name", ""),
        "publisher": source.get("publisher", ""),
        "author": source.get("author", ""),
        "published_at": source.get("published_at", ""),
        "accessed_at": source.get("accessed_at") or accessed_at,
        "source_type": source.get("source_type", category),
        "information_category": category,
        "reliability": source.get("reliability", _default_reliability(category)),
        "materiality": source.get("materiality", "medium"),
        "summary": source.get("summary", ""),
        "quoted_or_extracted_points": _text_list(source.get("quoted_or_extracted_points")),
    }


def _infer_information_category(source: dict[str, Any]) -> str:
    source_type = str(source.get("source_type", "")).lower()
    if source_type in INFO_CATEGORIES:
        return source_type
    if any(token in source_type for token in ["annual", "10-k", "filing", "press", "ir", "regulatory"]):
        return "evidence"
    if any(token in source_type for token in ["report", "research", "database"]):
        return "research_report"
    if any(token in source_type for token in ["news", "media", "message"]):
        return "message"
    if any(token in source_type for token in ["opinion", "expert", "interview"]):
        return "opinion"
    return "research_report"


def _infer_information_category_from_url(url: str) -> str:
    clean = url.lower()
    if any(token in clean for token in ["sec.gov", "hkexnews", "ir.", "investor", "newsroom", "press-release", "annual-report"]):
        return "evidence"
    if any(token in clean for token in ["research", "report", "pdf", "gartner", "idc", "counterpoint", "mercury"]):
        return "research_report"
    if any(token in clean for token in ["reuters", "bloomberg", "wsj", "cnbc", "caixin", "yicai", "36kr"]):
        return "message"
    if any(token in clean for token in ["xueqiu", "zhihu", "substack", "medium", "blog", "x.com"]):
        return "opinion"
    return "research_report"


def _default_reliability(category: str) -> str:
    return {
        "evidence": "primary",
        "research_report": "high",
        "message": "low",
        "opinion": "medium",
    }.get(category, "medium")


def _leaf_tasks_from_tree(
    qa_tree: dict[str, Any],
    ticker: str,
    company_name: str,
    completed_node_ids: set[str],
    limit: int | None,
) -> list[dict[str, Any]]:
    nodes_by_id = {node.get("id", ""): node for node in qa_tree.get("nodes", [])}
    tasks: list[dict[str, Any]] = []
    for node in qa_tree.get("nodes", []):
        node_id = node.get("id", "")
        if not node_id or node_id in completed_node_ids or not _is_leaf_node(qa_tree, node):
            continue
        parent = nodes_by_id.get(node.get("parent_id", ""), {})
        tasks.append(_leaf_task(qa_tree, node, parent, ticker, company_name))
        if limit is not None and len(tasks) >= limit:
            break
    return tasks


def _leaf_task(
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
    required = _text_list(node.get("required_evidence")) or _text_list(node.get("information_collection", {}).get("evidence", {}).get("acceptance_criteria")) or gaps[:3]
    question = node.get("question", "")
    parent_question = parent.get("question", "")
    task_family = _classify_task_family(node, parent)
    selected_skill = _selected_skill_for_task_family(task_family)
    source_search_plan = _source_search_plan(node, parent, task_family)
    extraction_schema = _extraction_schema_for_task(task_family)
    materiality = _materiality_statement(question, parent_question, task_family)
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
        "framework_context": _framework_context(qa_tree, node, parent),
        "materiality": materiality,
        "required_evidence": required,
        "disconfirming_signals": _text_list(node.get("disconfirming_signals")) or _text_list(professional.get("refuting_evidence")) or ["寻找能直接推翻当前判断的高可靠数据。"],
        "decision_rule": node.get("decision_rule") or "只有当事实、推论、反证和信息来源结构同时闭合时，才上修父问题判断。",
        "information_categories": list(INFO_CATEGORIES),
        "preferred_source_types": _preferred_source_types(node),
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


def _classify_task_family(node: dict[str, Any], parent: dict[str, Any]) -> str:
    text = " ".join(
        [
            str(node.get("question", "")),
            str(parent.get("question", "")),
            " ".join(_preferred_source_types(node)),
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


def _contains_any(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


def _selected_skill_for_task_family(task_family: str) -> str:
    return {
        "financial_statement": "financial-statement-analysis",
        "valuation": "valuation-analysis",
        "industry_report": "industry-report-analysis",
        "news_event": "news-event-analysis",
        "opinion": "opinion-analysis",
        "target_recommendation": "target-recommendation-analysis",
        "leaf_research": "leaf-research-deepseek",
    }.get(task_family, "leaf-research-deepseek")


def _source_search_plan(node: dict[str, Any], parent: dict[str, Any], task_family: str) -> list[dict[str, str]]:
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
        item["preferred_skill"] = _selected_skill_for_task_family(task_family if bucket in {"evidence", "research_report"} else bucket.replace("message", "news_event"))
        plan.append(item)
    return plan


def _extraction_schema_for_task(task_family: str) -> dict[str, Any]:
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


def _materiality_statement(question: str, parent_question: str, task_family: str) -> str:
    skill = _selected_skill_for_task_family(task_family)
    return (
        f"该叶子问题用于回答父问题“{parent_question}”。"
        f"若证据成立或被反证，应影响上层结论、目标标的强度、估值赔率或风险触发器；"
        f"默认由 {skill} 处理材料后再由 GPT 验证。"
    )


def _preferred_source_types(node: dict[str, Any]) -> list[str]:
    collection = node.get("information_collection", {}) or {}
    source_types: list[str] = []
    for category in INFO_CATEGORIES:
        for item in collection.get(category, {}).get("recommended_sources", []) or []:
            if item and item not in source_types:
                source_types.append(str(item))
    return source_types or ["公司公告/财报/监管文件", "第三方行业数据或深度报告", "主流财经媒体", "专家或产业观点"]


def _framework_context(qa_tree: dict[str, Any], node: dict[str, Any], parent: dict[str, Any]) -> str:
    section = node.get("section_id") or parent.get("section_id") or "foundation"
    return (
        f"Object={qa_tree.get('ticker', '')}; Section={section}; "
        f"Parent={parent.get('question', '')}; Leaf={node.get('question', '')}; "
        "Use the research-goal QA framework, classify every input into evidence/research_report/message/opinion, "
        "plan sources before reading, dispatch to specialty parsers when useful, "
        "and separate facts, inferences, judgments, refuting evidence, leads, gaps, and triggers."
    )


def _is_leaf_node(qa_tree: dict[str, Any], node: dict[str, Any]) -> bool:
    return int(node.get("level", 0) or 0) >= int(qa_tree.get("default_depth", 3) or 3) or not node.get("next_question_ids")


def _leaf_question_count(qa_tree: dict[str, Any]) -> int:
    return sum(1 for node in qa_tree.get("nodes", []) if _is_leaf_node(qa_tree, node))


def _completed_leaf_node_ids(research_dir: Path) -> set[str]:
    return {str(row.get("node_id", "")) for row in _read_jsonl(research_dir / LEAF_ANSWER_FILE) if row.get("node_id")}


def _stable_task_id(ticker: str, node_id: str) -> str:
    digest = hashlib.sha256(f"{ticker}:{node_id}".encode("utf-8")).hexdigest()[:12]
    return f"leaf_{digest}"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _company_name(root: Path, ticker: str) -> str:
    profile_path = root / "stocks" / ticker / "company_profile.md"
    if not profile_path.exists():
        return ticker
    for line in profile_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"-\s*Company:\s*(.+)", line)
        if match:
            return match.group(1).strip()
    return ticker


def _text_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows)
    path.write_text((text + "\n") if text else "", encoding="utf-8")
