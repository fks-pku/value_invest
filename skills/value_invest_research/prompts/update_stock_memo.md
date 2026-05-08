# Update Stock Memo Prompt Contract

Inputs:

- Existing `investment_memo.md`.
- Existing `evidence.jsonl`.
- New evidence records.
- Structured data under `data/`.

Output:

1. Memo update summary.
2. Proposed markdown patch by section.
3. Stock signal YAML.
4. Human review actions.

Required checks:

- Every material claim cites evidence IDs.
- Current view changes require at least one primary or high-reliability evidence item.
- Low-reliability evidence creates open questions only.
