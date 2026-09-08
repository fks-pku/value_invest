---
name: company-exposure-analysis
description: Use this skill when investment research needs to map a theme, event, product route, or supply-chain node to a specific company's revenue, margin, orders, customers, capex, FCF, and segment exposure before valuation or target ranking.
---

# Company Exposure Analysis

This skill turns a theme or event into company-level financial exposure. It is a bridge between supply-chain analysis and target ranking.

## Inputs

- Company/ticker and candidate thesis node.
- Segment revenue, product mix, customer mix, backlog/RPO/orders, guidance, capex, gross margin, FCF, and valuation snapshot if available.
- Evidence IDs and source links.

## Extract

- `exposure_node`: product, service, customer, geography, or supply-chain chokepoint.
- `revenue_exposure`: current revenue base, segment share, or best available proxy.
- `earnings_bridge`: ASP/take rate -> gross margin -> operating leverage -> FCF.
- `timing`: when the event/theme can affect orders, revenue, margin, and cash flow.
- `customer_concentration`: named customers, dependency, and bargaining risk.
- `dilution`: unrelated business lines, conglomerate mix, or low-margin pass-through.
- `evidence_quality`: direct company evidence, inferred from partner/customer, third-party estimate, or only message lead.
- `missing_data`: what prevents strengthening the conclusion.

## Rules

- Do not accept "partner list" or "industry exposure" as financial exposure.
- If exposure is indirect or diluted, cap target strength until revenue/margin evidence exists.
- Identify whether the company captures price, volume, mix, margin, or only low-margin manufacturing beta.
- Pass verified financial facts to `valuation-analysis`; pass exposure/risk summary to `target-ranking-analysis`.

## Output

- exposure bridge table.
- fact/inference/judgment/gap/trigger for the L3 QA card.
- source IDs and review IDs suitable for target score subcomponents.
