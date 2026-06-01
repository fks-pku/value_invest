from __future__ import annotations

from dataclasses import dataclass

from value_invest_research.domain.quality_gates import audit_source_time_slice
from value_invest_research.domain.research_artifacts import TimeSliceAuditResult
from value_invest_research.ports.repositories import SourceListRepository


@dataclass(frozen=True)
class AuditTimeSlice:
    """Audit source visibility through a source-list repository port."""

    repository: SourceListRepository

    def execute(self, *, as_of_date: str) -> TimeSliceAuditResult:
        source_list = self.repository.load_sources()
        return audit_source_time_slice(
            source_list,
            path=self.repository.source_path_label,
            as_of_date=as_of_date,
        )

