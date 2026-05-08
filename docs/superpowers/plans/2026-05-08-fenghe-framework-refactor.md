# FengHe Framework Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make FengHe 3C3D5M3T the strict primary research framework across stock, sector/theme, and event workflows.

**Architecture:** Keep the existing file-system-first package and Skill layout. Add a dedicated FengHe framework file, load it into every LLM workflow, and update templates/prompts so outputs must include 3C, 3D, 5M, 3T, and disconfirming tests.

**Tech Stack:** Python 3.11+, unittest, Markdown Skill files, file-system research objects.

---

### Task 1: Lock The New Contract With Tests

**Files:**
- Modify: `tests/test_scaffold.py`
- Modify: `tests/test_memo_updater.py`
- Modify: `tests/test_event_researcher.py`
- Modify: `tests/test_sector_researcher.py`

- [x] Add failing assertions that stock memo templates include 3C, 3D, 5M, and 3T.
- [x] Add failing assertions that stock, event, and sector system prompts load `FengHe 3C3D5M3T Framework`.
- [x] Add failing assertions that stock update prompts include `dominant_driver` and `disconfirming_tests`.

### Task 2: Add FengHe Protocol Files

**Files:**
- Create: `skills/value_invest_research/frameworks/fenghe_3c3d5m3t.md`
- Create: `skills/value_invest_research/checklists/fenghe_research_review.md`
- Modify: `skills/value_invest_research/SKILL.md`
- Modify: `skills/value_invest_research/prompts/update_stock_memo.md`

- [x] Define 3C: Cycle, Change, Certainty.
- [x] Define 3D: D1 ROE/intrinsic value, D2 marginal change/catalyst, D3 sentiment/valuation.
- [x] Define 5M: market size, market share, margin, model, management.
- [x] Define 3T: T1 0-3 months, T2 3-15 months, T3 15+ months.

### Task 3: Route Workflows Through FengHe

**Files:**
- Modify: `src/value_invest_research/memo_updater.py`
- Modify: `src/value_invest_research/event_researcher.py`
- Modify: `src/value_invest_research/sector_researcher.py`
- Modify: `src/value_invest_research/scaffold.py`

- [x] Load FengHe framework into each workflow system prompt.
- [x] Update stock memo update output to require FengHe sections and structured signal fields.
- [x] Update event candidate screening to require 3C, dominant 3D driver, and 3T.
- [x] Update sector/theme analysis to compare companies through 3C, 3D, 5M, and 3T.

### Task 4: Update Project Docs And Samples

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `docs/superpowers/specs/2026-05-06-llm-investment-research-system-design.md`
- Modify: `stocks/AAPL/investment_memo.md`
- Modify: sample research object templates under `research/`

- [x] Make FengHe the documented primary framework.
- [x] Update existing sample memo and research object shells.
- [x] Leave historical generated proposals intact as old research artifacts.

### Task 5: Verify

**Commands:**

```powershell
python tools/run_tests.py
python -m compileall -q src tests tools
```
