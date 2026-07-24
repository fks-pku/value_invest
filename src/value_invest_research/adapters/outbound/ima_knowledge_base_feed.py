from __future__ import annotations

from datetime import date
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


class ImaKnowledgeBaseFeed:
    """Read-only IMA OpenAPI adapter for discovery and original-material access."""

    provider_name = "ima"

    def __init__(
        self,
        *,
        client_id: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: int | None = None,
        min_interval: float | None = None,
        max_retries: int | None = None,
    ) -> None:
        self.client_id = (
            client_id
            or os.environ.get("IMA_OPENAPI_CLIENTID", "")
            or _read_secret(Path.home() / ".config" / "ima" / "client_id")
        ).strip()
        self.api_key = (
            api_key
            or os.environ.get("IMA_OPENAPI_APIKEY", "")
            or _read_secret(Path.home() / ".config" / "ima" / "api_key")
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
        self.min_interval = float(
            min_interval
            if min_interval is not None
            else os.environ.get("IMA_OPENAPI_MIN_INTERVAL", "0.25")
        )
        self.max_retries = int(
            max_retries
            if max_retries is not None
            else os.environ.get("IMA_OPENAPI_MAX_RETRIES", "5")
        )
        self._last_request_at = 0.0

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

    def list_dated_materials(
        self,
        *,
        knowledge_base_id: str,
        start_date: str,
        end_date: str,
        root_folder_pattern: str = r"^\d{4}年国际顶级投行研报$",
    ) -> list[dict[str, Any]]:
        """Walk year/month/day folders and return every PDF-like material."""

        knowledge_base_id = knowledge_base_id.strip()
        if not knowledge_base_id:
            raise ValueError("knowledge_base_id is required")
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        if start > end:
            raise ValueError("start_date must be on or before end_date")
        try:
            root_pattern = re.compile(root_folder_pattern)
        except re.error as exc:
            raise ValueError("root_folder_pattern must be a valid regex") from exc

        year_folders = self._find_year_folders(
            knowledge_base_id=knowledge_base_id,
            pattern=root_pattern,
        )
        if not year_folders:
            raise ValueError(
                "IMA directory scan found no year folder matching "
                f"{root_folder_pattern!r}"
            )
        rows_by_external_id: dict[str, dict[str, Any]] = {}
        for year_folder in year_folders:
            year = _year_from_title(str(year_folder.get("title") or ""))
            if year is None or year < start.year or year > end.year:
                continue
            for month_folder in self._list_folder(
                knowledge_base_id=knowledge_base_id,
                folder_id=_folder_id(year_folder),
            ):
                if not _is_folder(month_folder):
                    continue
                month = _month_from_title(str(month_folder.get("title") or ""))
                if month is None:
                    continue
                for day_folder in self._list_folder(
                    knowledge_base_id=knowledge_base_id,
                    folder_id=_folder_id(month_folder),
                ):
                    if not _is_folder(day_folder):
                        continue
                    directory_date = _day_folder_date(
                        year=year,
                        month=month,
                        title=str(day_folder.get("title") or ""),
                    )
                    if (
                        directory_date is None
                        or directory_date < start
                        or directory_date > end
                    ):
                        continue
                    directory_path = (
                        f"{year_folder.get('title')}/"
                        f"{month_folder.get('title')}/"
                        f"{day_folder.get('title')}"
                    )
                    for item in self._list_folder(
                        knowledge_base_id=knowledge_base_id,
                        folder_id=_folder_id(day_folder),
                    ):
                        if _is_folder(item) or not _is_pdf_like(item):
                            continue
                        normalized = _normalize_ima_item(
                            item,
                            knowledge_base_id=knowledge_base_id,
                            query="",
                        )
                        normalized["provider"] = self.provider_name
                        normalized["directory_date"] = directory_date.isoformat()
                        normalized["directory_path"] = directory_path
                        normalized["directory_mapping_status"] = "verified"
                        external_id = str(
                            normalized.get("external_id") or ""
                        ).strip()
                        previous = rows_by_external_id.get(external_id)
                        if (
                            previous is None
                            or str(previous.get("directory_date") or "")
                            < directory_date.isoformat()
                        ):
                            rows_by_external_id[external_id] = normalized
        return sorted(
            rows_by_external_id.values(),
            key=lambda row: (
                str(row.get("directory_date") or ""),
                str(row.get("title") or ""),
            ),
            reverse=True,
        )

    def _find_year_folders(
        self,
        *,
        knowledge_base_id: str,
        pattern: re.Pattern[str],
    ) -> list[dict[str, Any]]:
        roots = [
            item
            for item in self._list_folder(
                knowledge_base_id=knowledge_base_id,
                folder_id="",
            )
            if _is_folder(item)
        ]
        matches = [
            item
            for item in roots
            if pattern.search(str(item.get("title") or ""))
        ]
        if matches:
            return matches
        for root in roots:
            children = self._list_folder(
                knowledge_base_id=knowledge_base_id,
                folder_id=_folder_id(root),
            )
            matches.extend(
                item
                for item in children
                if _is_folder(item)
                and pattern.search(str(item.get("title") or ""))
            )
        return matches

    def _list_folder(
        self,
        *,
        knowledge_base_id: str,
        folder_id: str,
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        cursor = ""
        while True:
            payload: dict[str, Any] = {
                "knowledge_base_id": knowledge_base_id,
                "cursor": cursor,
                "limit": 50,
            }
            if folder_id:
                payload["folder_id"] = folder_id
            data = _response_data(self._post("get_knowledge_list", payload))
            items = data.get("knowledge_list") or data.get("info_list") or []
            rows.extend(item for item in items if isinstance(item, dict))
            if _is_end(data):
                break
            next_cursor = str(data.get("next_cursor") or "")
            if not next_cursor or next_cursor == cursor:
                break
            cursor = next_cursor
        return rows

    def resolve_knowledge_base_id(self, name: str) -> str:
        """Resolve an exact knowledge-base name without persisting its raw ID."""

        name = name.strip()
        if not name:
            raise ValueError("knowledge base name is required")
        cursor = ""
        candidates: list[dict[str, Any]] = []
        while True:
            data = _response_data(
                self._post(
                    "search_knowledge_base",
                    {"query": name, "cursor": cursor, "limit": 20},
                )
            )
            items = data.get("info_list") or []
            candidates.extend(item for item in items if isinstance(item, dict))
            if _is_end(data):
                break
            next_cursor = str(data.get("next_cursor") or "")
            if not next_cursor or next_cursor == cursor:
                break
            cursor = next_cursor
        exact = [
            item
            for item in candidates
            if _knowledge_base_name(item) == name
        ]
        if len(exact) != 1:
            names = sorted(
                {
                    _knowledge_base_name(item)
                    for item in candidates
                    if _knowledge_base_name(item)
                }
            )
            raise ValueError(
                f"Expected one IMA knowledge base named {name!r}; "
                f"found {len(exact)} exact matches. Candidates: {names}"
            )
        knowledge_base_id = _knowledge_base_id(exact[0])
        if not knowledge_base_id:
            raise ValueError(f"IMA knowledge base {name!r} has no ID")
        return knowledge_base_id

    def get_media_info(self, media_id: str) -> dict[str, Any]:
        """Return short-lived access metadata for one IMA source."""

        media_id = media_id.strip()
        if not media_id:
            raise ValueError("media_id is required")
        return _response_data(
            self._post("get_media_info", {"media_id": media_id})
        )

    def fetch_media_content(
        self,
        *,
        media_id: str,
        title: str = "",
    ) -> dict[str, Any]:
        """Download one source through IMA's short-lived original-material URL."""

        info = self.get_media_info(media_id)
        url_info = info.get("url_info")
        if not isinstance(url_info, dict) or not str(url_info.get("url") or "").strip():
            if int(info.get("media_type") or 0) == 11:
                raise ValueError(
                    "IMA notes require the notes get_doc_content API and are "
                    "not supported by this report-material feed"
                )
            raise ValueError(
                f"IMA media {media_id!r} does not expose an original-material URL"
            )
        url = str(url_info["url"]).strip()
        headers = {
            str(key): str(value)
            for key, value in (url_info.get("headers") or {}).items()
        }
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                content = response.read()
                content_type = str(
                    response.headers.get_content_type()
                    if hasattr(response.headers, "get_content_type")
                    else response.headers.get("Content-Type") or ""
                )
                content_disposition = str(
                    response.headers.get("Content-Disposition") or ""
                )
                resolved_url = str(response.geturl() or url)
        except urllib.error.HTTPError as exc:
            raise ValueError(
                f"IMA original-material request failed with HTTP {exc.code}"
            ) from exc
        except urllib.error.URLError as exc:
            raise ValueError(
                f"IMA original-material request failed: {exc.reason}"
            ) from exc
        return {
            "content": content,
            "content_type": content_type,
            "filename": _material_filename(
                title=title,
                content_disposition=content_disposition,
                url=resolved_url,
                media_type=int(info.get("media_type") or 0),
            ),
            "media_type": int(info.get("media_type") or 0),
        }

    def _post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        for attempt in range(self.max_retries + 1):
            self._wait_for_rate_limit()
            request = urllib.request.Request(
                f"{self.base_url}/{endpoint.lstrip('/')}",
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                headers={
                    "ima-openapi-clientid": self.client_id,
                    "ima-openapi-apikey": self.api_key,
                    "ima-openapi-ctx": "skill_version=value-invest-research",
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
                self._last_request_at = time.monotonic()
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")
                self._last_request_at = time.monotonic()
                if _is_rate_limit_error(exc.code, detail) and attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue
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
                message = (
                    raw.get("errmsg")
                    or raw.get("message")
                    or raw.get("msg")
                    or "unknown error"
                )
                if _is_rate_limit_error(int(code), str(message)) and attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue
                raise ValueError(f"IMA request failed: {message}")
            return raw
        raise ValueError("IMA request failed after rate-limit retries")

    def _wait_for_rate_limit(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)


def _response_data(raw: dict[str, Any]) -> dict[str, Any]:
    data = raw.get("data")
    if isinstance(data, dict):
        return data
    return raw


def _is_rate_limit_error(code: int, message: str) -> bool:
    text = str(message or "").casefold()
    return code in {200001, 403, 429} and (
        "频率" in text
        or "rate" in text
        or "too many" in text
        or code in {429, 200001}
    )


def _knowledge_base_name(item: dict[str, Any]) -> str:
    return str(item.get("name") or item.get("kb_name") or "").strip()


def _knowledge_base_id(item: dict[str, Any]) -> str:
    return str(item.get("id") or item.get("kb_id") or "").strip()


def _is_folder(item: dict[str, Any]) -> bool:
    return bool(
        int(item.get("media_type") or 0) == 99
        or item.get("folder_id")
        or item.get("file_number") is not None
    )


def _folder_id(item: dict[str, Any]) -> str:
    return str(item.get("folder_id") or item.get("media_id") or "").strip()


def _year_from_title(title: str) -> int | None:
    match = re.search(r"(?<!\d)(20\d{2})(?!\d)", title)
    return int(match.group(1)) if match else None


def _month_from_title(title: str) -> int | None:
    match = re.fullmatch(r"\s*(\d{1,2})月\s*", title)
    if not match:
        return None
    value = int(match.group(1))
    return value if 1 <= value <= 12 else None


def _day_folder_date(*, year: int, month: int, title: str) -> date | None:
    match = re.fullmatch(r"\s*(\d{1,2})[.\-/](\d{1,2})\s*", title)
    if not match:
        return None
    folder_month = int(match.group(1))
    day = int(match.group(2))
    if folder_month != month:
        return None
    try:
        return date(year, month, day)
    except ValueError:
        return None


def _is_pdf_like(item: dict[str, Any]) -> bool:
    return (
        int(item.get("media_type") or 0) == 1
        or str(item.get("title") or "").lower().endswith(".pdf")
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
    provider_published_at = _date_prefix(
        item.get("published_at") or item.get("source_visible_at")
    )
    title_published_at = _date_from_report_title(
        str(item.get("title") or "")
    )
    if provider_published_at:
        published_at = provider_published_at
        publication_date_status = "verified"
        publication_date_source = "provider_published_at"
    elif title_published_at:
        published_at = title_published_at
        publication_date_status = "inferred_from_title"
        publication_date_source = "title_suffix"
    else:
        published_at = ""
        publication_date_status = "needs_pdf_verification"
        publication_date_source = "unknown"
    provider_created_at = _date_prefix(
        item.get("create_time") or item.get("created_at")
    )
    modified_at = (
        item.get("update_time")
        or item.get("modified_at")
        or item.get("updated_at")
        or item.get("create_time")
        or item.get("created_at")
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
        "published_at": published_at,
        "publication_date_status": publication_date_status,
        "publication_date_source": publication_date_source,
        "provider_created_at": provider_created_at,
        "modified_at": _date_prefix(modified_at),
        "directory_mapping_status": "pending_directory_reconciliation",
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
    if media_type in {1, 3, 4}:
        return "sell_side_report"
    if media_type == 6:
        return "market_news"
    if media_type in {2, 7, 11}:
        return "knowledge_base_document"
    if media_type == 5:
        return "research_report"
    return "other"


def _date_prefix(value: Any) -> str:
    text = str(value or "").strip()
    if len(text) >= 10:
        return text[:10]
    return ""


def _date_from_report_title(title: str) -> str:
    """Extract a sell-side YYMMDD date suffix when IMA omits metadata."""

    matches = re.findall(r"(?<!\d)(\d{6})(?!\d)", title)
    for raw in reversed(matches):
        year = 2000 + int(raw[:2])
        month = int(raw[2:4])
        day = int(raw[4:6])
        try:
            return date(year, month, day).isoformat()
        except ValueError:
            continue
    return ""


def _material_filename(
    *,
    title: str,
    content_disposition: str,
    url: str,
    media_type: int,
) -> str:
    clean_title = title.strip()
    extension = _media_extension(media_type)
    if (
        clean_title
        and extension
        and clean_title.lower().endswith(extension)
    ):
        return re.sub(
            r"[\x00-\x1f/\\:]+",
            "_",
            clean_title,
        ).strip(" .")
    match = re.search(
        r"filename\*?=(?:UTF-8''|\"?)([^\";]+)",
        content_disposition,
        flags=re.IGNORECASE,
    )
    if match:
        candidate = urllib.parse.unquote(match.group(1)).strip().strip('"')
    else:
        candidate = urllib.parse.unquote(
            urllib.parse.urlparse(url).path.rsplit("/", 1)[-1]
        ).strip()
    if not candidate or "." not in candidate:
        candidate = title.strip() or f"ima-{media_type or 'material'}"
        if extension and not candidate.lower().endswith(extension):
            candidate = f"{candidate}{extension}"
    candidate = re.sub(r"[\x00-\x1f/\\:]+", "_", candidate).strip(" .")
    return candidate or f"ima-material{extension}"


def _media_extension(media_type: int) -> str:
    return {
        1: ".pdf",
        3: ".docx",
        4: ".pptx",
        5: ".xlsx",
        7: ".md",
        13: ".txt",
        20: ".html",
    }.get(media_type, "")


def _read_secret(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError:
        return ""
