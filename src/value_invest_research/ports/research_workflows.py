from __future__ import annotations

from pathlib import Path
from typing import Protocol


class LeafResearchWorkflow(Protocol):
    """Outbound port for leaf research workflow operations during migration."""

    def build_tasks(
        self,
        root: Path,
        ticker: str,
        *,
        limit: int | None = None,
        include_completed: bool = False,
    ) -> dict:
        """Build leaf research tasks."""

    def run_research(
        self,
        root: Path,
        ticker: str,
        *,
        provider: str,
        input_path: Path | None = None,
        limit: int | None = None,
    ) -> dict:
        """Run or import leaf research results."""

    def import_results(self, root: Path, ticker: str, path: Path) -> dict:
        """Import provider-agnostic leaf research results."""

    def synthesize_answers(self, root: Path, ticker: str) -> dict:
        """Synthesize leaf answers from normalized provider results."""

    def rollup_answers(self, root: Path, ticker: str) -> dict:
        """Roll leaf answers up to parent QA nodes."""


class KnowledgeBaseMaterialFeed(Protocol):
    """Outbound feed used to scan a user-owned knowledge base."""

    @property
    def provider_name(self) -> str:
        """Stable provider name stored in the material ledger."""

    def search_materials(
        self,
        *,
        knowledge_base_id: str,
        query: str,
        max_results: int,
    ) -> list[dict]:
        """Return matching knowledge-base materials without classifying claims."""

    def list_dated_materials(
        self,
        *,
        knowledge_base_id: str,
        start_date: str,
        end_date: str,
        root_folder_pattern: str,
    ) -> list[dict]:
        """Enumerate every material inside year/month/day folders."""

    def fetch_media_content(
        self,
        *,
        media_id: str,
        title: str = "",
    ) -> dict:
        """Download one original material without exposing signed URLs."""


class PublicationDateExtractor(Protocol):
    """Outbound parser that verifies a document's actual publication date."""

    def extract(
        self,
        *,
        content: bytes,
        title: str = "",
    ) -> dict:
        """Return publication date fields derived from document contents."""
