from __future__ import annotations

from typing import Any, Protocol


class LeafResearchProvider(Protocol):
    """Outbound port for a provider that researches one leaf task."""

    def search(self, task: dict[str, Any]) -> dict[str, Any]:
        """Return a provider-specific leaf research result."""


class RawProviderResponseStore(Protocol):
    """Outbound port for storing raw provider responses."""

    @property
    def raw_dir_label(self) -> str:
        """Stable label for result metadata."""

    def save_raw_response(self, task_id: str, payload: dict[str, Any]) -> str:
        """Persist the raw provider response and return its path label."""


class SourceMaterialParser(Protocol):
    """Outbound port for parsing one concrete source against one L3 question."""

    def parse(self, job: dict[str, Any]) -> dict[str, Any]:
        """Return a source_extractions.jsonl-compatible extraction record."""


class SourceExtractionReviewer(Protocol):
    """Outbound port for GPT-style verification of one parser extraction."""

    def review(self, extraction: dict[str, Any], job: dict[str, Any]) -> dict[str, Any]:
        """Return a leaf_source_reviews.jsonl-compatible verification record."""
