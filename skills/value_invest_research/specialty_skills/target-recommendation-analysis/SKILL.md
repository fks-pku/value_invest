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
- `score_dimensions`: four public target dimensions: `scarcity_or_monopoly`, `mispricing`, `earnings_elasticity`, and `risk_control`.
- `score_breakdown`
- `score_subcomponents`: auditable subcomponent rows for every core score component.
- `mechanism_driver_links`: demand driver, supply/access constraint, unit economics, value-capture node, valuation bridge, and disconfirming tests that justify the target's score.
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
- `thesis_kill_tests`
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

Observation strength must reflect the whole score, not just narrative attractiveness. The public score lens is four-dimensional:

- `scarcity_or_monopoly`: scarce product/service, monopoly-like control, chokepoint power, or hard-to-substitute value capture.
- `mispricing`: market underpricing or an implied expectation that does not already discount the fundamental path.
- `earnings_elasticity`: large future revenue, margin, cash-flow, operating leverage, or rerating upside if the thesis is right.
- `risk_control`: high win probability because the major disconfirming, execution, policy, cyclical, and valuation risks are bounded and monitorable.

The final target ranking must include a compact score breakdown with comparable fields across all targets. Default fields:

- chokepoint strength
- future space
- valuation odds
- evidence quality
- disconfirming-risk control
- monitorability
- payoff convexity

Each core score component must preserve `score_subcomponents`. Each row must include:

- subdimension name
- score
- weight
- evidence IDs or GPT review IDs
- rationale
- status

Do not use unexplained manual component scores in refreshed canonical reports. A direct component score is a fallback only when the source record explains why subcomponent scoring was impossible.

The seven component scores are substructure for the four core target dimensions. Do not let high `future_space` compensate for weak `scarcity_or_monopoly`; do not let a great company score high when `mispricing` is stale, missing, or negative; do not let a cheap stock score high when `earnings_elasticity` is small; do not let an exciting payoff score high when `risk_control` is poor.

The deterministic ranking formula is:

1. `action_state` priority: `actionable_long`, then `watch_only`, then `no_action`.
2. Higher `opportunity_fit`.
3. Higher `total_score`.
4. Higher `payoff_convexity`.
5. Higher `thesis_confidence`.
6. Stable ticker/name tie-break.

Do not manually reorder the list after labels are attached or because later outcomes are known.

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
- mechanism-depth drivers: demand-supply slope, unit economics/profit bridge, capital-chain exposure, market-pricing/rerating bridge, and model口径 caveats where relevant.

## Rules

- Recommend specific securities or assets when investment implications exist.
- Do not stop at sectors or directions unless no tradable target can be responsibly mapped.
- Do not restrict the observation list to securities with convenient US/Nasdaq labels. Include the actual value-capture vehicles across exchanges; if a label is missing, preserve the target and mark the label unverified.
- Do not issue buy/sell/hold instructions.
- Do not raise strength if valuation is missing; mark valuation unverified.
- Do not raise strength if chokepoint capture is weak or unverified; mark it as watch-only or validation-needed.
- Do not mark `actionable_long` unless all four dimensions are strong: scarcity_or_monopoly, mispricing, earnings_elasticity, and risk_control.
- Do not raise strength from a broad industry thesis unless the target's mechanism_driver_links show how demand becomes that target's revenue, margin, FCF, or valuation rerating.
- Do not use a simplified odds model as a target price or trading instruction.
- Separate core observation targets from validation/watchlist targets.
- Every target must have at least one downgrade trigger and one required data item.
- Every `actionable_long` target must include hard `thesis_kill_tests` with test, evidence needed, downgrade action, and source plan. If these tests are missing or not monitorable, cap the target at `watch_only`.
