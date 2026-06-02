---
name: event-to-investment-analysis
description: Use this skill when an investment research task starts from a public event, conference, product launch, policy meeting, investor day, or keynote and needs to convert event facts into investment-relevant transmission paths, evidence gaps, disconfirming tests, and target implications.
---

# Event To Investment Analysis

This skill turns an event into an investable research map. It does not rank targets by itself.

## Inputs

- Event name, date, location, organizer, and source links.
- Official agenda, keynote, press releases, transcript, slides, or replay.
- Third-party reports/news when available.
- The parent QA node and decision boundary.

## Extract

- `event_fact_boundary`: what was officially said, by whom, when, and where.
- `new_information_delta`: what is new versus prior public knowledge.
- `commercialization_stage`: concept, prototype, design win, qualification, production, shipment, revenue, or margin evidence.
- `transmission_chain`: event claim -> product route -> customer/order -> revenue -> margin/FCF -> valuation.
- `affected_chain_nodes`: upstream, midstream, downstream, ecosystem, customers, and listed targets.
- `evidence_strength`: primary fact, confirmed company voice, third-party lead, or market interpretation.
- `refuting_tests`: what would prove the event is only marketing, delayed, already priced, or not financially material.
- `next_sources`: filings, earnings calls, supplier disclosures, customer capex, order/backlog, channel checks, valuation data.

## Rules

- Treat event language as a signal, not a conclusion.
- Separate official facts from inference and market reaction.
- Do not upgrade target strength unless the event can be tied to order visibility, revenue timing, margin, FCF, or valuation mispricing.
- For live events, record the next validation horizon and review trigger.
- For backtests, only use event materials visible at the as-of date.

## Output

Return a QA-ready record:

- fact
- inference
- judgment
- gap
- trigger
- support/refute/lead stance
- source links
- target implications
- preferred follow-up skills, usually `conference-transcript-analysis`, `supply-chain-chokepoint-analysis`, `company-exposure-analysis`, `financial-statement-analysis`, `valuation-analysis`, and `target-ranking-analysis`.
