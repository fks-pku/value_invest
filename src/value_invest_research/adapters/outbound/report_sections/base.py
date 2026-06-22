from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ReportRenderContext:
    """Section renderer input shared by the canonical HTML report sections."""

    data: dict[str, Any]
    source_url_by_id: dict[str, str]


class ReportSection(Protocol):
    """Contract for one public top-level report section."""

    section_id: str

    def render(self, context: ReportRenderContext) -> str:
        """Render this section from the canonical report context."""
