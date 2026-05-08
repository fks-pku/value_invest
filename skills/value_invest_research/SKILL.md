---
name: value-invest-research
description: Use for US equity investment research workflows that collect evidence, update stock memos, run sector/theme research, or analyze sudden market events using a value-investing framework.
---

# Value Investment Research Skill

This Skill turns heterogeneous market information into auditable research artifacts. It supports three workflows:

1. `update_stock_memo`: update one company memo using the value-investing framework.
2. `run_sector_or_theme_research`: map an industry or theme and identify companies worth stock-level research.
3. `run_event_research`: analyze a sudden event, build transmission chains, and rank candidate tickers for human review.

## Non-Negotiable Rules

- Do not issue final trading instructions.
- Separate facts, inferences, and judgments.
- Cite evidence IDs for every material claim.
- Treat low-reliability sources as research leads only.
- Search for disconfirming evidence before strengthening a thesis.
- Preserve prior thesis history when updating a memo.
- Mark uncertainty directly instead of hiding it.

## Required Context Loading

Before analysis, load the relevant research object folder:

- Canonical memo.
- `evidence.jsonl`.
- Structured files under `data/`.
- Latest run logs under `logs/`.
- Related stock, sector, theme, or event objects named in the task.

## Workflow Routing

- Use `frameworks/value_investing.md` and `prompts/update_stock_memo.md` for individual companies.
- Use `frameworks/sector_research.md` and `prompts/run_sector_research.md` for industry or theme work.
- Use `frameworks/event_research.md` and `prompts/run_event_research.md` for sudden event research.
- Use `checklists/evidence_quality.md` for all workflows.
- Use `checklists/disconfirming_evidence.md` before any thesis-strengthening output.
- Use `checklists/valuation_review.md` before changing valuation conclusions.
