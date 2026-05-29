---
name: industry-report-analysis
description: Use this skill whenever investment research needs to parse sell-side reports, industry reports, market datasets, TAM estimates, supply-demand forecasts, price forecasts, competitive maps, or third-party research. It extracts assumptions, methods, numbers, and disagreement points rather than treating reports as facts.
---

# Industry Report Analysis

This skill turns third-party research into auditable assumptions and evidence leads.

## Extract

- `report_title`
- `publisher`
- `date`
- `covered_scope`
- `market_size_or_forecast`
- `supply_demand_assumptions`
- `price_or_margin_assumptions`
- `competitive_landscape`
- `bottleneck_claims`
- `target_or_company_mentions`
- `methodology`
- `key_charts_or_tables`
- `assumptions_to_verify`
- `where_the_report_could_be_wrong`
- `source_links`

## Rules

- Treat industry reports as research_report, not primary evidence.
- Separate reported data, model estimates, and analyst opinions.
- Extract base assumptions before quoting headline TAM or CAGR.
- Identify whether growth is volume, price, mix, penetration, replacement cycle, or inventory rebuild.
- Cross-check third-party claims with primary company filings when possible.
- Use reports to generate questions and triangulate, not to close high-confidence conclusions alone.

## QA Contribution

For an L3 question, return:

- Support/refute/lead stance.
- Which parent hypothesis the report affects.
- The exact data that should be verified by primary sources.
- Any alternative interpretation or bear case embedded in the report.
