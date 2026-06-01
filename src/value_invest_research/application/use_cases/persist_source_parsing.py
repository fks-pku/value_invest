from __future__ import annotations

from dataclasses import dataclass

from value_invest_research.ports.repositories import SourceParsingArtifactWriter


@dataclass(frozen=True)
class PersistSourceParsingArtifacts:
    """Persist source parser outputs and GPT leaf reviews through a writer port."""

    writer: SourceParsingArtifactWriter

    def execute(
        self,
        *,
        source_extractions: list[dict] | None = None,
        leaf_source_reviews: list[dict] | None = None,
    ) -> dict[str, int]:
        extraction_records = list(source_extractions or [])
        review_records = list(leaf_source_reviews or [])
        if extraction_records:
            self.writer.append_source_extractions(extraction_records)
        if review_records:
            self.writer.append_leaf_source_reviews(review_records)
        return {
            "source_extractions": len(extraction_records),
            "leaf_source_reviews": len(review_records),
        }

