from __future__ import annotations

from dataclasses import dataclass

from value_invest_research.domain.bom_project_layout import validate_bom_project_layout_bundle
from value_invest_research.ports.repositories import BomProjectLayoutRepository


@dataclass(frozen=True)
class ValidateBomProjectLayout:
    repository: BomProjectLayoutRepository

    def execute(self) -> dict:
        return validate_bom_project_layout_bundle(self.repository.load_layout_bundle())
