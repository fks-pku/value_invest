from __future__ import annotations

from datetime import date
from io import BytesIO
import json
from pathlib import Path
import re
from typing import Any

from pypdf import PdfReader


class ImaArchiveMaterialFeed:
    """Expose the central IMA mirror as a downstream research-material feed."""

    provider_name = "ima"

    def __init__(self, *, workspace_root: Path, archive_root: Path):
        self.workspace_root = workspace_root.resolve()
        self.archive_root = archive_root.resolve()
        if not self.archive_root.is_relative_to(self.workspace_root):
            raise ValueError("IMA archive_root must stay inside the workspace")
        self._records = _read_jsonl(self.archive_root / "archive_manifest.jsonl")

    def search_materials(
        self,
        *,
        knowledge_base_id: str,
        query: str,
        max_results: int,
    ) -> list[dict[str, Any]]:
        del knowledge_base_id
        terms = [
            item.casefold()
            for item in str(query or "").split()
            if item.strip()
        ]
        rows = [
            self._as_material(row)
            for row in self._records
            if all(
                term in str(row.get("title") or "").casefold()
                for term in terms
            )
        ]
        return rows[:max_results]

    def list_dated_materials(
        self,
        *,
        knowledge_base_id: str,
        start_date: str,
        end_date: str,
        root_folder_pattern: str,
    ) -> list[dict[str, Any]]:
        del knowledge_base_id, root_folder_pattern
        return [
            self._as_material(row)
            for row in sorted(
                self._records,
                key=lambda item: (
                    str(item.get("directory_date") or ""),
                    str(item.get("title") or ""),
                    str(item.get("external_id") or ""),
                ),
            )
            if start_date
            <= str(row.get("directory_date") or "")
            <= end_date
        ]

    def fetch_media_content(
        self,
        *,
        media_id: str,
        title: str = "",
    ) -> dict[str, Any]:
        row = next(
            (
                item
                for item in self._records
                if str(item.get("external_id") or "") == media_id
            ),
            {},
        )
        if str(row.get("status") or "") != "available":
            raise ValueError(
                f"Central IMA archive original is unavailable: {title or media_id}"
            )
        path = self._local_path(row)
        return {
            "content": path.read_bytes(),
            "filename": path.name,
            "content_type": str(
                row.get("content_type") or "application/pdf"
            ),
        }

    def _as_material(self, row: dict[str, Any]) -> dict[str, Any]:
        local_path = str(row.get("local_path") or "")
        title = str(row.get("title") or "")
        title_date = _publication_date_from_title(title)
        summary = ""
        if str(row.get("status") or "") == "available" and local_path:
            path = self._local_path(row)
            summary = _extract_screening_text(path.read_bytes())
        return {
            "external_id": str(row.get("external_id") or ""),
            "title": title,
            "publisher": _publisher_from_title(title),
            "source_type": "sell_side_report",
            "material_class": "sell_side_research",
            "provider": "ima",
            "summary": summary,
            "directory_date": str(row.get("directory_date") or ""),
            "directory_path": str(row.get("directory_path") or ""),
            "directory_mapping_status": str(
                row.get("directory_mapping_status") or "verified"
            ),
            "published_at": title_date,
            "publication_date_status": (
                "inferred_from_title"
                if title_date
                else "needs_pdf_verification"
            ),
            "publication_date_source": (
                "title_suffix" if title_date else "unknown"
            ),
            "raw_locator": local_path,
            "archive_status": str(row.get("status") or ""),
        }

    def _local_path(self, row: dict[str, Any]) -> Path:
        path = (self.workspace_root / str(row.get("local_path") or "")).resolve()
        if not path.is_relative_to(self.archive_root) or not path.is_file():
            raise ValueError(
                "Central IMA archive manifest points to a missing or unsafe file: "
                f"{row.get('local_path')}"
            )
        return path


def _extract_screening_text(content: bytes, *, max_pages: int = 3) -> str:
    """Extract enough text to review ambiguous titles without parsing claims."""

    try:
        reader = PdfReader(BytesIO(content), strict=False)
    except Exception:
        return ""
    chunks = []
    for page in reader.pages[:max_pages]:
        try:
            text = str(page.extract_text() or "").strip()
        except Exception:
            continue
        if text:
            chunks.append(text)
        if sum(len(item) for item in chunks) >= 12000:
            break
    text = "\n".join(chunks)[:12000]
    return text if _looks_readable(text) else ""


def _looks_readable(text: str) -> bool:
    words = re.findall(r"[A-Za-z]{3,}", text)
    if len(words) < 80:
        return False
    normalized = text.casefold()
    anchors = (
        "research",
        "revenue",
        "company",
        "market",
        "investment",
        "earnings",
        "estimate",
    )
    return sum(anchor in normalized for anchor in anchors) >= 2


def _publisher_from_title(title: str) -> str:
    prefixes = {
        "大摩-": "Morgan Stanley",
        "摩根大通-": "J.P. Morgan",
        "巴克莱-": "Barclays",
        "德银-": "Deutsche Bank",
        "高盛-": "Goldman Sachs",
        "汇丰-": "HSBC",
        "瑞银-": "UBS",
    }
    return next(
        (publisher for prefix, publisher in prefixes.items() if title.startswith(prefix)),
        "IMA research archive",
    )


def _publication_date_from_title(title: str) -> str:
    for raw in reversed(re.findall(r"(?<!\d)(\d{6})(?!\d)", title)):
        try:
            return date(
                2000 + int(raw[:2]),
                int(raw[2:4]),
                int(raw[4:6]),
            ).isoformat()
        except ValueError:
            continue
    return ""


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            payload = json.loads(line)
            if isinstance(payload, dict):
                rows.append(payload)
    return rows
