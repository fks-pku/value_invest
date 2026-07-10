from __future__ import annotations

from value_invest_research.adapters.outbound.report_sections.base import ReportRenderContext, ReportSection
from value_invest_research.adapters.outbound.report_sections.goal import CurrentGoalSection, render_hero
from value_invest_research.adapters.outbound.report_sections.industry_overview import IndustryOverviewSection
from value_invest_research.adapters.outbound.report_sections.sources import SourcesSection
from value_invest_research.adapters.outbound.report_sections.targets import TargetRecommendationsSection

DEFAULT_REPORT_SECTIONS: tuple[ReportSection, ...] = (
    CurrentGoalSection(),
    IndustryOverviewSection(),
    TargetRecommendationsSection(),
    SourcesSection(),
)

__all__ = [
    "DEFAULT_REPORT_SECTIONS",
    "ReportRenderContext",
    "ReportSection",
    "render_hero",
]
