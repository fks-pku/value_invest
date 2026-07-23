from __future__ import annotations

from dataclasses import dataclass

from value_invest_research.domain.material_intake import (
    validate_material_intake_bundle,
)
from value_invest_research.ports.repositories import (
    MaterialIntakeValidationRepository,
)


@dataclass(frozen=True)
class ValidateMaterialIntake:
    """Validate material intake through a repository port."""

    repository: MaterialIntakeValidationRepository

    def execute(self) -> dict:
        result = validate_material_intake_bundle(
            self.repository.load_material_intake_bundle()
        )
        return {
            **result,
            "project_dir": self.repository.project_dir_label,
        }
