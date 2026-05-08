# Usable Project State Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the repository usable for local development with stable tests, clear entry points, and basic project documentation.

**Architecture:** Keep the existing file-system-first Python package. Treat third-party integrations as optional extras so core scaffolding, validation, and tests can run in a minimal local environment.

**Tech Stack:** Python 3.11+, unittest, pyproject optional dependencies, Markdown project docs.

---

### Task 1: Stabilize Local Tests

**Files:**
- Create: `tests/helpers.py`
- Modify: `tests/test_*.py`

- [x] Replace `tempfile.TemporaryDirectory()` with a project-local test helper because this environment creates non-writable temp directories.
- [x] Verify the original failure is gone by running the unittest suite through `src` on `sys.path`.

### Task 2: Make Optional Integrations Import-Safe

**Files:**
- Modify: `src/value_invest_research/llm.py`
- Modify: `src/value_invest_research/ingest_prices.py`
- Modify: `src/value_invest_research/event_researcher.py`

- [x] Defer `openai` errors until LLM client construction.
- [x] Keep `ingest_prices` importable without `yfinance`, while preserving a patchable `yf.Ticker` boundary for tests.
- [x] Keep event research importable without `pyyaml`; require it only when loading YAML playbooks from disk.

### Task 3: Add Development Entry Points And Docs

**Files:**
- Modify: `pyproject.toml`
- Modify: `.gitignore`
- Create: `tools/run_tests.py`
- Create: `README.md`
- Create: `AGENTS.md`

- [x] Add the `value-invest-research` console script.
- [x] Move integrations into optional extras.
- [x] Add a repo-local test runner that injects `src` into `sys.path`.
- [x] Document install, run, test, layout, and research constraints.

### Task 4: Verify

**Commands:**

```powershell
python tools/run_tests.py
python -m compileall -q src tests tools
python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
$env:PYTHONPATH='src'; python -m value_invest_research --help
```
