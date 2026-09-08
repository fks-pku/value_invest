---
name: financial-statement-analysis
description: Use this skill whenever investment research needs to parse financial statements, annual reports, 10-K/10-Q/20-F filings, earnings releases, segment data, capex, inventory, backlog/RPO, cash-flow quality, or accounting risk. It turns filings into normalized facts, quality checks, gaps, and triggers before valuation or synthesis.
---

# Financial Statement Analysis

This skill extracts investment-relevant financial facts from official financial materials. It does not decide target strength by itself.

## Use For

- Annual reports, 10-K, 10-Q, 20-F, quarterly reports.
- Earnings releases and result announcements.
- Segment revenue, gross margin, operating profit, capex, inventory, deferred revenue, contract liabilities, backlog, RPO.
- Cash-flow quality, working-capital pressure, accounting red flags.

## Extraction Schema

Return:

- `source`
- `period`
- `currency`
- `business_segments`
- `revenue_bridge`
- `gross_margin_bridge`
- `operating_margin_bridge`
- `cash_flow_bridge`
- `capex_and_capacity`
- `inventory_and_working_capital`
- `backlog_or_rpo`
- `customer_or_supplier_concentration`
- `management_guidance`
- `accounting_quality_flags`
- `what_changed_vs_prior_period`
- `what_it_proves`
- `what_it_does_not_prove`
- `next_quarter_triggers`
- `source_links`

## Analysis Rules

- Distinguish reported numbers, adjusted numbers, and management commentary.
- Separate growth from price, volume, mix, FX, and accounting reclassification when possible.
- Treat segment data as more decision-useful than group revenue when the question is about value capture.
- For cash quality, reconcile profit, operating cash flow, capex, free cash flow, inventory, receivables, payables, and contract liabilities.
- For backlog/RPO/order data, state whether it is binding, cancellable, timing-sensitive, or only directional.
- Always state the missing denominator if a company gives a numerator but hides volume, ASP, units, or margin.

## Output Into QA

Write the final L3 contribution as:

- Facts.
- Inferences.
- Judgment.
- Gaps.
- Triggers.
- Parent rollup implication.

If valuation is needed, pass only verified financial facts to `valuation-analysis`.
