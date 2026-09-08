---
name: conference-transcript-analysis
description: Use this skill when investment research needs to parse keynotes, conference transcripts, investor-day talks, management Q&A, product demos, or launch presentations and separate official facts, roadmap claims, customer references, commercialization stage, and promotional language.
---

# Conference Transcript Analysis

This skill reads conference/keynote material as management communication. It extracts facts and claim quality before the research system maps them to financial impact.

## Inputs

- Transcript, replay notes, slides, agenda page, press release, or official blog.
- Speaker identity and organization.
- Relevant QA node and extraction schema.

## Extract

- `speaker_claims`: who said what, with date/session anchor.
- `claim_type`: shipped fact, production status, roadmap, partnership, benchmark, customer mention, aspiration, or marketing phrase.
- `commercial_anchor`: shipment timing, named customer, product availability, capacity, performance metric, pricing, backlog, or none.
- `changed_assumption`: demand, supply, bottleneck, timing, margin, competitive position, or valuation.
- `source_bucket`: usually evidence for official company material, message for third-party live coverage.
- `support_refute_or_lead`: support, refute, or lead.
- `verification_needed`: the primary source or future data needed to confirm the claim.

## Rules

- Do not treat performance claims or customer logos as revenue evidence unless shipment/order/payment language exists.
- Flag vague wording such as "planned", "expected", "exploring", "working with", or "ecosystem partner" as lower evidence strength.
- Preserve exact dates and product availability timing.
- Separate product-route evidence from target-specific financial evidence.

## Output

Return structured extraction for `source_extractions.jsonl`:

- key facts with source anchors.
- fact/inference/preliminary judgment/gap/trigger.
- schema_fields required by the L3 node.
- uncertainty and follow-up data.
