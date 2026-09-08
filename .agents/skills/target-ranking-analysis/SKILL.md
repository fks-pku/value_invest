---
name: target-ranking-analysis
description: Use this skill after Q1-Q3 have verified demand, chokepoint, company exposure, valuation, and disconfirming-risk evidence, when the task is to rank specific securities deterministically by scarcity, mispricing, earnings elasticity, risk control, payoff odds, and monitorability.
---

# Target Ranking Analysis

This skill converts verified QA conclusions into a deterministic target ranking worksheet. It does not issue buy/sell/hold instructions.

## Preconditions

- Q1 demand/fact boundary has verified evidence.
- Q2 chokepoint score or score drivers exist.
- Q3 disconfirming tests and valuation/priced-in risk exist.
- Each candidate target has company exposure evidence or is capped as watch/no-action.

## Ranking Inputs

For every target, preserve:

- ticker, name, market, thesis node, chokepoint node.
- four core dimensions: `scarcity_or_monopoly`, `mispricing`, `earnings_elasticity`, `risk_control`.
- seven audit components: `chokepoint_strength`, `future_space`, `valuation_odds`, `evidence_quality`, `disconfirming_risk_control`, `monitorability`, `payoff_convexity`.
- `score_subcomponents` with evidence IDs or GPT review IDs.
- simplified odds model: implied expectation, base path, bull path, bear path, upgrade data, downgrade data.
- action state: `actionable_long`, `watch_only`, or `no_action`.
- thesis kill tests for any `actionable_long`.

## Rules

- Default action state is `no_action`.
- Theme exposure cannot create high rank without scarce value capture and financial conversion.
- Missing/stale valuation caps the target at `watch_only`.
- If a target lacks monitorable downgrade triggers, cap it below `actionable_long`.
- Ranking order must follow the executable scoring rule: action-state priority, opportunity fit, total score, payoff convexity, thesis confidence, stable ticker/name tie-break.

## Output

- ranked target worksheet for `investment_workbench.json`.
- public-ready compact target rows for the final report.
- remaining data gaps and next review trigger.
