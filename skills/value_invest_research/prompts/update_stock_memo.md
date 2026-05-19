# Update Stock Memo Prompt Contract

Inputs:

- Existing `investment_memo.md`.
- Existing `evidence.jsonl`.
- New evidence records.
- Structured data under `data/`.

Output:

1. Memo update summary.
2. Foundation baseline impact across the eight company-foundation sections.
3. Proposed markdown patch by memo section.
4. Stock signal YAML with foundation status and FengHe message-flow fields.
5. Human review actions and disconfirming tests.

Required company foundation sections:

- Source and origin.
- Company history.
- Current business.
- Value chain position.
- Competitive landscape.
- Strategy analysis.
- Organization, culture, and governance.
- Risk sweep.

Required FengHe message-flow sections:

- 3C: Cycle, Change, Certainty.
- 3D: D1 ROE/intrinsic value, D2 marginal change/catalyst, D3 sentiment/valuation.
- 5M: M1 market size, M2 market share, M3 margin, M4 model, M5 management.
- 3T: T1 0-3 months, T2 3-15 months, T3 15+ months.

Required checks:

- Every material claim cites evidence IDs.
- Current view changes require at least one primary or high-reliability evidence item, a foundation baseline check, and a named FengHe driver.
- Low-reliability evidence creates open questions only.
- The output must state the dominant D driver, the time frame, and disconfirming tests.
