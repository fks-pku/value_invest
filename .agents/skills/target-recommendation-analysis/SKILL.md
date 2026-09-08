---
name: target-recommendation-analysis
description: Use this skill whenever a research report must translate verified QA conclusions into a specific target observation list with tickers, thesis nodes, future space, valuation odds, strength, catalysts, risks, and monitoring triggers. It is for research recommendations, not trading instructions.
---

# Target Recommendation Analysis

This skill converts verified research into a specific observation list.

## Preconditions

Use this skill only after Q1-Q3 have produced verified conclusions:

- Demand or growth driver is defined.
- Bottleneck or value-capture node is identified.
- Disconfirming tests are listed.
- Valuation or priced-in expectations have been checked or marked missing.

## Target Table Fields

For every target, include:

- `ticker_or_asset`
- `name`
- `market`
- `thesis_node`
- `chokepoint_node`
- `chokepoint_score`
- `chokepoint_score_drivers`
- `score_breakdown`
- `why_it_captures_value`
- `future_space`
- `valuation_odds`
- `simplified_odds_model`
- `prediction_review`
- `strength`: high, medium-high, medium, low, or watch-only.
- `evidence_quality`
- `key_sources`
- `catalysts`
- `downgrade_triggers`
- `required_next_data`
- `risk_notes`

## Scoring Rubric

Score each target from 1-5 on:

- Fundamental strength.
- Bottleneck capture.
- Chokepoint criticality and irreplaceability.
- Chokepoint financial conversion.
- Future space.
- Valuation odds.
- Evidence quality.
- Disconfirming-risk control.
- Monitorability.

Observation strength must reflect the whole score, not just narrative attractiveness.

The final target ranking should include a compact score breakdown with comparable fields across all targets. Default fields:

- chokepoint strength
- future space
- valuation odds
- evidence quality
- disconfirming-risk control
- monitorability

The simplified odds model should state:

- what the current valuation appears to require,
- base path,
- bull path,
- bear path,
- data that upgrades the observation,
- data that downgrades the observation.

Prediction review should preserve:

- initial claim,
- validation horizon,
- required evidence,
- current status,
- next review trigger.

For bottleneck/chokepoint-driven research, target ranking must explicitly reconcile:

- the Q2 chokepoint score or score drivers,
- Q1 demand strength and future space,
- Q3 disconfirming tests,
- valuation odds,
- evidence quality and monitorability.

## Rules

- Recommend specific securities or assets when investment implications exist.
- Do not stop at sectors or directions unless no tradable target can be responsibly mapped.
- Do not issue buy/sell/hold instructions.
- Do not raise strength if valuation is missing; mark valuation unverified.
- Do not raise strength if chokepoint capture is weak or unverified; mark it as watch-only or validation-needed.
- Do not use a simplified odds model as a target price or trading instruction.
- Separate core observation targets from validation/watchlist targets.
- Every target must have at least one downgrade trigger and one required data item.
