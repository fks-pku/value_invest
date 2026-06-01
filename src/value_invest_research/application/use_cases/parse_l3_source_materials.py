from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from value_invest_research.application.use_cases.persist_source_parsing import PersistSourceParsingArtifacts
from value_invest_research.ports.repositories import SourceParsingArtifactWriter
from value_invest_research.ports.source_parsers import SourceExtractionReviewer, SourceMaterialParser


@dataclass(frozen=True)
class ParseL3SourceMaterials:
    """Parse and verify concrete source materials for L3 QA nodes."""

    parser: SourceMaterialParser
    reviewer: SourceExtractionReviewer
    writer: SourceParsingArtifactWriter

    def execute(self, jobs: list[dict[str, Any]]) -> dict[str, int]:
        source_extractions: list[dict[str, Any]] = []
        leaf_source_reviews: list[dict[str, Any]] = []
        for job in jobs:
            extraction = self.parser.parse(job)
            source_extractions.append(extraction)
            leaf_source_reviews.append(self.reviewer.review(extraction, job))
        persist_result = PersistSourceParsingArtifacts(self.writer).execute(
            source_extractions=source_extractions,
            leaf_source_reviews=leaf_source_reviews,
        )
        return {
            **persist_result,
            "jobs": len(jobs),
        }
