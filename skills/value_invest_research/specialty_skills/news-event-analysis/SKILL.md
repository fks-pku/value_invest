---
name: news-event-analysis
description: Use this skill whenever investment research needs to parse public news, messages, policy headlines, product launches, supply-chain reports, rumors, or unverified market updates. It classifies messages as leads, maps them to hypotheses, and defines verification triggers without upgrading conviction by itself.
---

# News Event Analysis

This skill processes public messages and news. News is usually a lead until verified by primary evidence or repeated high-quality sources.

## Extract

- `headline`
- `publisher`
- `date`
- `event_type`
- `affected_companies_or_nodes`
- `claimed_fact`
- `source_of_claim`
- `verification_status`
- `support_refute_or_lead`
- `hypothesis_affected`
- `near_term_trigger`
- `what_primary_source_would_confirm`
- `what_would_disprove_it`
- `source_link`

## Rules

- Do not treat rumors as facts.
- State whether the claim is confirmed, attributed, anonymous, inferred, or unverified.
- Map every news item to a QA node or discard it.
- Separate immediate price-sensitive messages from fundamental thesis changes.
- Use news to define what to verify next: filings, exchange announcements, management comments, shipment data, order data, regulator documents.

## Output

News output should usually feed:

- Trigger lists.
- Watchlists.
- Disconfirming tests.
- Follow-up data needs.

It should not independently raise target strength.
