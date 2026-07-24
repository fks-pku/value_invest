from __future__ import annotations

from datetime import date
from io import BytesIO
import re
from typing import Any

from pypdf import PdfReader


class PdfPublicationDateExtractor:
    """Extract the report's publication date from the first PDF pages."""

    _MONTHS = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12,
    }

    def extract(
        self,
        *,
        content: bytes,
        title: str = "",
    ) -> dict[str, Any]:
        """Return a verified cover date, or an explicit unresolved result."""

        try:
            reader = PdfReader(BytesIO(content), strict=False)
        except Exception as exc:
            return _unresolved(f"pdf_read_error:{type(exc).__name__}")

        for page_number, page in enumerate(reader.pages[:3], start=1):
            try:
                text = str(page.extract_text() or "")
            except Exception:
                continue
            match = _find_publication_date(text, months=self._MONTHS)
            if match:
                return {
                    "published_at": match["date"],
                    "publication_date_status": "verified",
                    "publication_date_source": "pdf_cover",
                    "publication_date_locator": (
                        f"第{page_number}页：{match['matched_text']}"
                    ),
                }
        return _unresolved("pdf_first_three_pages_no_date")


def _find_publication_date(
    text: str,
    *,
    months: dict[str, int],
) -> dict[str, str] | None:
    compact = re.sub(r"[ \t]+", " ", str(text or ""))
    patterns = (
        re.compile(
            r"(?<!\d)(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日"
        ),
        re.compile(
            r"(?<!\d)(20\d{2})[-/.](\d{1,2})[-/.](\d{1,2})(?!\d)"
        ),
    )
    for pattern in patterns:
        for match in pattern.finditer(compact):
            normalized = _valid_date(
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3)),
            )
            if normalized:
                return {
                    "date": normalized,
                    "matched_text": match.group(0).strip(),
                }

    day_first = re.compile(
        r"(?<!\d)(\d{1,2})\s+("
        + "|".join(months)
        + r")\s+(20\d{2})(?!\d)",
        flags=re.IGNORECASE,
    )
    for match in day_first.finditer(compact):
        normalized = _valid_date(
            int(match.group(3)),
            months[match.group(2).casefold()],
            int(match.group(1)),
        )
        if normalized:
            return {
                "date": normalized,
                "matched_text": match.group(0).strip(),
            }

    month_first = re.compile(
        r"(?<![A-Za-z])("
        + "|".join(months)
        + r")\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(20\d{2})(?!\d)",
        flags=re.IGNORECASE,
    )
    for match in month_first.finditer(compact):
        normalized = _valid_date(
            int(match.group(3)),
            months[match.group(1).casefold()],
            int(match.group(2)),
        )
        if normalized:
            return {
                "date": normalized,
                "matched_text": match.group(0).strip(),
            }
    return None


def _valid_date(year: int, month: int, day: int) -> str:
    try:
        return date(year, month, day).isoformat()
    except ValueError:
        return ""


def _unresolved(reason: str) -> dict[str, str]:
    return {
        "published_at": "",
        "publication_date_status": "needs_pdf_verification",
        "publication_date_source": "unknown",
        "publication_date_locator": reason,
    }
