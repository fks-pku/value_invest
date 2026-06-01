from __future__ import annotations

from dataclasses import dataclass

from value_invest_research.domain.quality_gates import validate_research_artifacts
from value_invest_research.domain.research_artifacts import ResearchArtifactValidationResult
from value_invest_research.ports.repositories import ResearchArtifactRepository


@dataclass(frozen=True)
class ValidateResearchProject:
    """Validate a research project through the artifact repository port."""

    repository: ResearchArtifactRepository

    def execute(self, *, require_l3: bool = False) -> ResearchArtifactValidationResult:
        artifacts = self.repository.load_research_artifacts()
        return validate_research_artifacts(
            artifacts,
            project_dir=self.repository.project_dir_label,
            require_l3=require_l3,
        )

