# FengHe Stock Research Command Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `research-stock TICKER` command that produces a complete FengHe stock research report and structured signal JSON.

**Architecture:** Reuse the existing stock context loader and FengHe system prompt from `memo_updater.py`. Keep this workflow report-only: it writes timestamped artifacts under `stocks/<TICKER>/research_reports/` and does not mutate the canonical memo.

**Tech Stack:** Python 3.11+, unittest, existing LLM client abstraction, Markdown and JSON output files.

---

### Task 1: Define Contract With Tests

**Files:**
- Create: `tests/test_stock_researcher.py`
- Modify: `tests/test_cli.py`

- [x] Assert the stock research prompt requires 3C, 3D, 5M, 3T, `dominant_driver`, and `disconfirming_tests`.
- [x] Assert signal JSON can be extracted from a fenced JSON block.
- [x] Assert `research-stock` prints report and signal paths.

### Task 2: Implement Stock Researcher

**Files:**
- Create: `src/value_invest_research/stock_researcher.py`

- [x] Load stock memo, evidence, SEC facts, and recent price context.
- [x] Build a full FengHe stock research prompt.
- [x] Save the LLM response as `*_fenghe_research.md`.
- [x] Extract and save a structured `*_fenghe_signal.json`.
- [x] Log successful and failed runs.

### Task 3: Wire CLI And Docs

**Files:**
- Modify: `src/value_invest_research/cli.py`
- Modify: `README.md`
- Modify: `AGENTS.md`

- [x] Add `research-stock TICKER`.
- [x] Reuse existing LLM config flags.
- [x] Document output location.

### Task 4: Verify

**Commands:**

```powershell
python tools/run_tests.py
python -m compileall -q src tests tools
```
