# BOM Seven-Question Four-Step Design

## Goal

Make every public BOM seven-question card answer through the same evidence sequence: choose metrics, show historical chart or explicit trend gap, discuss future metric movement, then explain the first-principles mechanism that makes the trend sustainable or unsustainable.

## Scope

This is a persistent research-framework presentation and reasoning change for BOM-first public reports. It applies to the seven fixed questions under every BOM node:

- `需求是否会大幅增长？`
- `单位用量是否会提升？`
- `供给能否跟上？`
- `谁控制供给？`
- `是否已经财务兑现？`
- `市场是否已定价？`
- `反证是什么？`

## Public Report Contract

Each `details.bom-question-card` must render a single-column four-step body:

1. `bom-step-metrics`: which metrics prove the question, why they matter, source chips, and known metric gaps.
2. `bom-step-history`: quarterly or annual historical values rendered as `metric-trend-chart`, `metric-noncontinuous-chart`, or an explicit `metric-trend-gap`.
3. `bom-step-future`: how the same metrics should move over near, medium, and long horizons, including public anchors and data gaps.
4. `bom-step-mechanism`: first-principles mechanism, sustainability logic, and invalidation logic.

The final answer and source chips remain visible inside the card, but they come after the four-step evidence sequence. Search plans, parser traces, and workbench metadata remain internal.

## AI Factory Refresh

The current AI Factory S-curve report generator should produce the four-step structure for all 6 BOM nodes x 7 questions. The first demand card may keep its richer `research-narrative` content, but it must still expose the same four public step classes so the report is structurally consistent.

## Verification

Add a regression test against `research/bom/ai_factory_industry_scurve_timeslice_20260302/professional_report.html` that fails unless every `bom-question-card` contains:

- `bom-step-metrics`
- `bom-step-history`
- at least one chart/gap class: `metric-trend-chart`, `metric-noncontinuous-chart`, or `metric-trend-gap`
- `bom-step-future`
- `bom-step-mechanism`

