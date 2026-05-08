---
name: value-invest-research
description: Use for US equity investment research workflows that collect evidence, update stock memos, run sector/theme research, or analyze sudden market events using the FengHe 3C3D5M3T framework.
---

# FengHe Investment Research Skill

This Skill turns heterogeneous market information into auditable FengHe-style research artifacts. The primary framework is `3C3D5M3T`; generic value-investing language is secondary and must not override it. It supports three workflows:

1. `update_stock_memo`: update one company memo using 3C, 3D, 5M, and 3T.
2. `run_sector_or_theme_research`: map cycles, marginal changes, 5M company differences, and candidates worth stock-level research.
3. `run_event_research`: analyze a sudden event through cycle, change, certainty, price drivers, and candidate time frames.

## Non-Negotiable Rules

- Do not issue final trading instructions.
- Separate facts, inferences, and judgments.
- Cite evidence IDs for every material claim.
- Treat low-reliability sources as research leads only.
- Search for disconfirming evidence before strengthening a thesis.
- Preserve prior thesis history when updating a memo.
- Mark uncertainty directly instead of hiding it.
- Apply 3C before 3D, 3D before 5M, and 5M before 3T.
- Do not call a company "good" without naming the M driver and the M defect risk.
- Do not promote an idea without a time frame and disconfirming tests.

## Required Context Loading

Before analysis, load the relevant research object folder:

- Canonical memo.
- `evidence.jsonl`.
- Structured files under `data/`.
- Latest run logs under `logs/`.
- Related stock, sector, theme, or event objects named in the task.

## Workflow Routing

- Use `frameworks/fenghe_3c3d5m3t.md` and `prompts/update_stock_memo.md` for individual companies.
- Use `frameworks/sector_research.md` and `prompts/run_sector_research.md` for industry or theme work.
- Use `frameworks/event_research.md` and `prompts/run_event_research.md` for sudden event research.
- Use `checklists/evidence_quality.md` for all workflows.
- Use `checklists/fenghe_research_review.md` for all thesis-strengthening outputs.
- Use `checklists/disconfirming_evidence.md` before any thesis-strengthening output.
- Use `checklists/valuation_review.md` before changing valuation conclusions.
