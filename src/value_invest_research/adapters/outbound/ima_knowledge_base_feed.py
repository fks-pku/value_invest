from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


class ImaKnowledgeBaseFeed:
    """Read-only IMA OpenAPI adapter for knowledge-base material discovery."""

    provider_name = "ima"

    def __init__(
        self,
        *,
        client_id: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: int | None = None,
    ) -> None:
        self.client_id = (
            client_id or os.environ.get("IMA_OPENAPI_CLIENTID", "")
        ).strip()
        self.api_key = (
            api_key or os.environ.get("IMA_OPENAPI_APIKEY", "")
        ).strip()
        if not self.client_id or not self.api_key:
            raise ValueError(
                "IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY are required. "
                "Generate them at https://ima.qq.com/agent-interface and keep "
                "them outside the repository."
            )
        self.base_url = (
            base_url
            or os.environ.get(
                "IMA_OPENAPI_BASE_URL",
                "https://ima.qq.com/openapi/wiki/v1",
            )
        ).strip().rstrip("/")
        self.timeout = int(
            timeout or os.environ.get("IMA_OPENAPI_TIMEOUT", "60")
        )

    def search_materials(
        self,
        *,
        knowledge_base_id: str,
        query: str,
        max_results: int,
    ) -> list[dict[str, Any]]:
        """Search one IMA knowledge base and return metadata-only candidates."""

        knowledge_base_id = knowledge_base_id.strip()
        query = query.strip()
        if not knowledge_base_id:
            raise ValueError("knowledge_base_id is required")
        if not query:
            raise ValueError("IMA material scan requires a non-empty BOM query")
        rows: list[dict[str, Any]] = []
        cursor = ""
        while len(rows) < max_results:
            raw = self._post(
                "search_knowledge",
                {
                    "query": query,
                    "knowledge_base_id": knowledge_base_id,
                    "cursor": cursor,
                },
            )
            data = _response_data(raw)
            items = data.get("info_list") or data.get("knowledge_list") or []
            if not isinstance(items, list):
                items = []
            for item in items:
                if not isinstance(item, dict) or _is_folder(item):
                    continue
                rows.append(
                    _normalize_ima_item(
                        item,
                        knowledge_base_id=knowledge_base_id,
                        query=query,
                    )
                )
                if len(rows) >= max_results:
                    break
            if len(rows) >= max_results or _is_end(data):
                break
            next_cursor = str(data.get("next_cursor") or "")
            if not next_cursor or next_cursor == cursor:
                break
            cursor = next_cursor
        return rows

    def _post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        request = urllib.request.Request(
            f"{self.base_url}/{endpoint.lstrip('/')}",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "ima-openapi-clientid": self.client_id,
                "ima-openapi-apikey": self.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(
                request,
                timeout=self.timeout,
            ) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ValueError(
                f"IMA request failed with HTTP {exc.code}: {detail}"
            ) from exc
        except urllib.error.URLError as exc:
            raise ValueError(f"IMA request failed: {exc.reason}") from exc
        try:
            raw = json.loads(body)
        except json.JSONDecodeError as exc:
            raise ValueError("IMA returned a non-JSON response") from exc
        if not isinstance(raw, dict):
            raise ValueError("IMA returned an invalid response object")
        code = raw.get("retcode", raw.get("code", 0))
        if code not in (0, "0", None):
            message = raw.get("errmsg") or raw.get("message") or "unknown error"
            raise ValueError(f"IMA request failed: {message}")
        return raw


def _response_data(raw: dict[str, Any]) -> dict[str, Any]:
    data = raw.get("data")
    if isinstance(data, dict):
        return data
    return raw


def _is_folder(item: dict[str, Any]) -> bool:
    return bool(
        int(item.get("media_type") or 0) == 99
        or item.get("folder_id")
        or item.get("file_number") is not None
    )


def _is_end(data: dict[str, Any]) -> bool:
    value = data.get("is_end")
    if value is None:
        return True
    return bool(value)


def _normalize_ima_item(
    item: dict[str, Any],
    *,
    knowledge_base_id: str,
    query: str,
) -> dict[str, Any]:
    media_id = str(item.get("media_id") or item.get("id") or "").strip()
    published_at = (
        item.get("published_at")
        or item.get("create_time")
        or item.get("created_at")
        or item.get("update_time")
        or item.get("modified_at")
        or ""
    )
    modified_at = (
        item.get("update_time")
        or item.get("modified_at")
        or item.get("updated_at")
        or published_at
    )
    return {
        "external_id": media_id,
        "title": str(item.get("title") or media_id),
        "url": str(
            item.get("url")
            or item.get("source_url")
            or item.get("download_url")
            or ""
        ),
        "publisher": str(item.get("publisher") or "IMA knowledge base"),
        "published_at": _date_prefix(published_at),
        "modified_at": _date_prefix(modified_at),
        "summary": str(
            item.get("highlight_content")
            or item.get("summary")
            or item.get("abstract")
            or ""
        ),
        "source_type": _media_source_type(item),
        "raw_locator": f"ima_media:{media_id}",
        "discovery_query": query,
        "media_type": item.get("media_type"),
        "tags": item.get("tags") or [],
    }


def _media_source_type(item: dict[str, Any]) -> str:
    explicit = str(
        item.get("source_type") or item.get("material_type") or ""
    ).strip()
    if explicit:
        return explicit
    media_type = int(item.get("media_type") or 0)
    if media_type == 1:
        return "knowledge_base_pdf"
    if media_type == 6:
        return "market_news"
    if media_type in {2, 7, 11}:
        return "knowledge_base_document"
    if media_type in {3, 4, 5}:
        return "research_report"
    return "other"


def _date_prefix(value: Any) -> str:
    text = str(value or "").strip()
    if len(text) >= 10:
        return text[:10]
    return ""
