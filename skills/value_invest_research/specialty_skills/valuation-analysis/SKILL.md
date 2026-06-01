---
name: valuation-analysis
description: Use this skill whenever investment research needs valuation, priced-in expectations, future growth space, multiples, FCF yield, reverse DCF, peer comparison, scenario odds, margin of safety, or target recommendation strength. It converts verified facts into risk/reward and valuation-pressure analysis without issuing trading instructions.
---

# Valuation Analysis

This skill evaluates whether fundamentals and future space are already priced in.

## Inputs

Use verified inputs only:

- Current price or market cap if available.
- Revenue, margin, EPS, FCF, capex, net cash/debt.
- Segment exposure or bottleneck node.
- Growth drivers and disconfirming tests.
- Peer multiples and historical ranges.
- Consensus or management guidance when available.

## Required Output

- `valuation_snapshot`: market cap, EV, PE, EV/EBITDA, EV/Sales, P/FCF, FCF yield, or relevant local metrics.
- `future_space`: TAM, node profit pool, company capture rate, growth duration, margin potential.
- `priced_in_assumptions`: what revenue growth, margin, or FCF conversion the current price appears to require.
- `market_pricing_bridge`: multiples, FCF yield, implied cyclicality discount, risk premium or discount-rate assumption when relevant, and what would justify rerating or derating.
- `scenario_table`: bear/base/bull with drivers, numbers, and probability if defensible.
- `upside_drivers`
- `downside_drivers`
- `disconfirming_tests`
- `valuation_gap`: what data is missing before strengthening the view.
- `odds_judgment`: favorable, neutral, stretched, or unverified.
- `simplified_odds_model`: implied expectation, base path, bull path, bear path, upgrade data, downgrade data.
- `prediction_review`: initial claim, validation horizon, required evidence, current status, next review trigger.

## Rules

- Do not use valuation multiples without explaining what they imply.
- Do not call a stock cheap or expensive without naming the growth/margin assumptions.
- When the thesis is a category rerating, separate fundamental improvement from multiple/risk-premium compression. A low multiple is not favorable odds unless the driver tree can justify why the market's discount should narrow.
- Separate industry future space from company-capturable future space.
- Treat high-quality fundamentals and attractive odds as different conclusions.
- If current price data is stale or missing, mark valuation as unverified and list what to fetch.
- No buy/sell/hold instructions.
- Do not turn a scenario or simplified odds model into a target price unless the user explicitly asks to change the boundary. Keep it as risk/reward research.

## Target Recommendation Use

For each target, valuation must feed:

- Observation strength.
- Required verification data.
- Upgrade triggers.
- Downgrade triggers.
- Why risk/reward is or is not attractive relative to other targets.
