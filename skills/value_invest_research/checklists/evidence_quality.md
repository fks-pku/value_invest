# Evidence Quality Checklist

Reliability levels:

- `primary`: SEC filings, company investor relations, official transcripts, audited financials.
- `high`: reputable financial press, exchange data, established data providers.
- `medium`: specialist blogs, expert commentary, industry newsletters.
- `low`: social media, unattributed rumors, unsourced summaries.

Materiality levels:

- `low`: background context.
- `medium`: affects a section of a memo.
- `high`: materially affects a candidate, risk, or estimate.
- `thesis_change`: can change current view or confidence.

Rules:

- Low-reliability evidence cannot trigger `thesis_change`.
- Uncited material claims must be rejected.
- Conflicting evidence must be recorded as a conflict, not averaged away.
