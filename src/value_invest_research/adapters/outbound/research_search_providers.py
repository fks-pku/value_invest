from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

from value_invest_research.domain.leaf_research_tasks import INFO_CATEGORIES


class MockResearchSearchProvider:
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


class OpenAICompatibleResearchSearchProvider:
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
                {"role": "system", "content": provider_system_prompt()},
                {"role": "user", "content": provider_user_prompt(task)},
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
        result = provider_result_from_chat_response(task, raw_response, provider=self.name, default_model=self.model)
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


class ExaResearchSearchProvider:
    """Exa search adapter for leaf-level source discovery."""

    name = "exa"

    def __init__(self) -> None:
        api_key = os.environ.get("EXA_API_KEY", "").strip()
        if not api_key:
            raise ValueError("EXA_API_KEY is required for provider=exa. Set the environment variable or use provider=mock/manual.")
        self.api_key = api_key
        self.endpoint = os.environ.get("EXA_ENDPOINT", "https://api.exa.ai/search").strip()
        self.search_type = os.environ.get("EXA_SEARCH_TYPE", "auto").strip() or "auto"
        self.model = f"exa-search-{self.search_type}"
        self.timeout = int(os.environ.get("EXA_TIMEOUT", "60"))
        self.num_results = int(os.environ.get("EXA_NUM_RESULTS", "8"))
        self.text_max_characters = int(os.environ.get("EXA_TEXT_MAX_CHARACTERS", "1500"))

    def search(self, task: dict[str, Any]) -> dict[str, Any]:
        query = exa_query_from_task(task)
        payload = {
            "query": query,
            "type": self.search_type,
            "numResults": max(1, min(int(task.get("max_sources", self.num_results) or self.num_results), self.num_results)),
            "contents": {
                "highlights": True,
                "text": {
                    "maxCharacters": self.text_max_characters,
                },
            },
        }
        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "x-api-key": self.api_key,
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
            raise ValueError(f"Exa request failed with HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ValueError(f"Exa request failed: {exc.reason}") from exc
        raw_response = json.loads(response_body)
        result = provider_result_from_exa_response(task, raw_response, query=query, provider_model=self.model)
        result["_raw_provider_response"] = raw_response
        return result


def provider_for_name(provider: str):
    if provider == "mock":
        return MockResearchSearchProvider()
    if provider == "perplexity":
        return PerplexityResearchSearchProvider()
    if provider == "exa":
        return ExaResearchSearchProvider()
    if provider == "openai_compatible":
        return OpenAICompatibleResearchSearchProvider()
    raise ValueError(f"Unsupported leaf research provider: {provider}")


def provider_system_prompt() -> str:
    return (
        "You are a professional equity research search agent. "
        "Answer one leaf research question with cited sources. "
        "Return only a JSON object. Do not provide trading instructions."
    )


def provider_user_prompt(task: dict[str, Any]) -> str:
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


def provider_result_from_chat_response(
    task: dict[str, Any],
    raw_response: dict[str, Any],
    provider: str,
    default_model: str,
) -> dict[str, Any]:
    content = chat_response_content(raw_response)
    parsed = extract_json_object(content)
    search_sources = sources_from_search_results(raw_response)
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


def provider_result_from_exa_response(
    task: dict[str, Any],
    raw_response: dict[str, Any],
    *,
    query: str,
    provider_model: str,
) -> dict[str, Any]:
    sources = sources_from_exa_results(raw_response)
    titles = [source.get("title", "") for source in sources if source.get("title")]
    facts = [
        f"Exa returned candidate source: {title}"
        for title in titles[:5]
    ]
    return {
        "provider": "exa",
        "provider_model": provider_model,
        "task_id": task.get("task_id", ""),
        "node_id": task.get("node_id", ""),
        "query": query,
        "answer": (
            f"Exa source discovery found {len(sources)} candidate sources for this leaf question. "
            "Use DeepSeek/source-parser to read the selected materials before strengthening the conclusion."
        ),
        "facts": facts,
        "inferences": ["Exa output is treated as a source candidate set, not as a final investment judgment."],
        "judgment": "Source discovery only; GPT must verify source fit and DeepSeek/source-parser must extract question-specific fields.",
        "supporting_evidence": [source.get("summary", "") for source in sources[:5] if source.get("summary")],
        "refuting_evidence": [],
        "research_leads": titles[:8],
        "gaps": task.get("required_evidence", [])[:3] or ["Need source-parser extraction and GPT verification before parent rollup."],
        "confidence": "low",
        "materiality": task.get("materiality", ""),
        "source_plan": task.get("source_search_plan", []),
        "extraction_schema": task.get("extraction_schema", {}),
        "task_family": task.get("task_family", ""),
        "selected_skill": task.get("selected_skill", ""),
        "skill_dispatch_trace": {
            **(task.get("skill_dispatch_trace", {}) if isinstance(task.get("skill_dispatch_trace"), dict) else {}),
            "skill_output_status": "source_discovery",
            "gpt_verification_status": "pending_exa_source_review",
        },
        "sources": sources,
    }


def chat_response_content(raw_response: dict[str, Any]) -> str:
    try:
        content = raw_response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("provider response missing choices[0].message.content") from exc
    if isinstance(content, list):
        return "\n".join(str(item.get("text", item)) if isinstance(item, dict) else str(item) for item in content)
    return str(content)


def extract_json_object(text: str) -> dict[str, Any]:
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


def sources_from_search_results(raw_response: dict[str, Any]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for item in raw_response.get("search_results", []) or []:
        if not isinstance(item, dict):
            continue
        url = str(item.get("url", "")).strip()
        if not url:
            continue
        category = infer_information_category_from_url(url)
        sources.append(
            {
                "url": url,
                "title": item.get("title", ""),
                "publisher": item.get("publisher", ""),
                "author": item.get("author", ""),
                "published_at": item.get("date", "") or item.get("published_at", ""),
                "source_type": item.get("source_type", category),
                "information_category": category,
                "reliability": default_reliability(category),
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
        category = infer_information_category_from_url(url)
        sources.append(
            {
                "url": url,
                "title": url,
                "publisher": "",
                "author": "",
                "published_at": "",
                "source_type": category,
                "information_category": category,
                "reliability": default_reliability(category),
                "materiality": "medium",
                "summary": "Citation returned by provider.",
                "quoted_or_extracted_points": [],
            }
        )
    return sources


def sources_from_exa_results(raw_response: dict[str, Any]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for item in raw_response.get("results", []) or []:
        if not isinstance(item, dict):
            continue
        url = str(item.get("url", "")).strip()
        if not url:
            continue
        category = infer_information_category_from_url(url)
        text = str(item.get("summary") or item.get("text") or "").strip()
        highlights = _text_list(item.get("highlights"))
        if not highlights and text:
            highlights = [text[:500]]
        sources.append(
            {
                "url": url,
                "title": item.get("title", "") or url,
                "publisher": publisher_from_url(url),
                "author": item.get("author", ""),
                "published_at": item.get("publishedDate", "") or item.get("published_at", ""),
                "source_type": category,
                "information_category": category,
                "reliability": default_reliability(category),
                "materiality": "medium",
                "summary": text[:1000],
                "quoted_or_extracted_points": highlights[:5],
            }
        )
    return sources


def exa_query_from_task(task: dict[str, Any]) -> str:
    universe = task.get("source_universe_plan") if isinstance(task.get("source_universe_plan"), dict) else {}
    priority_sources = universe.get("priority_sources") if isinstance(universe.get("priority_sources"), list) else []
    universe_names = ", ".join(
        str(item.get("name") or item.get("domain") or "")
        for item in priority_sources
        if isinstance(item, dict) and (item.get("name") or item.get("domain"))
    )
    parts = [
        str(task.get("question", "")).strip(),
        f"Company: {task.get('company_name', '')} {task.get('ticker', '')}".strip(),
        f"Parent question: {task.get('parent_question', '')}".strip(),
        f"Required evidence: {'; '.join(_text_list(task.get('required_evidence'))[:4])}",
        f"Preferred materials: {source_plan_focus(task.get('source_search_plan', []))}",
        f"Professional source universe: {universe_names}",
    ]
    return "\n".join(part for part in parts if part and not part.endswith(": "))


def source_plan_focus(source_plan: Any) -> str:
    if not isinstance(source_plan, list):
        return ""
    chunks: list[str] = []
    for item in source_plan[:5]:
        if not isinstance(item, dict):
            continue
        chunks.append(
            " / ".join(
                _text_list([
                    item.get("source_bucket", ""),
                    item.get("source_type", ""),
                    item.get("expected_fields", ""),
                ])
            )
        )
    return "; ".join(chunk for chunk in chunks if chunk)


def publisher_from_url(url: str) -> str:
    host = urllib.parse.urlparse(url).netloc.lower()
    return host.removeprefix("www.")


def infer_information_category_from_url(url: str) -> str:
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


def default_reliability(category: str) -> str:
    return {
        "evidence": "primary",
        "research_report": "high",
        "message": "low",
        "opinion": "medium",
    }.get(category, "medium")


def _text_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
