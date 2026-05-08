# Stock Evidence Builder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert structured stock data into stable `evidence.jsonl` records that FengHe research reports can cite.

**Architecture:** Add a stock evidence builder that reads `stocks/<TICKER>/data/sec_facts.json` and `prices.csv`, creates validated `EvidenceRecord` instances, appends only new records by ID/hash, and logs each run.

**Tech Stack:** Python 3.11+, standard library CSV/JSON/hashlib, existing `EvidenceRecord` and `RunLog` utilities.

---

### Task 1: Define Evidence Builder Behavior

**Files:**
- Create: `tests/test_evidence_builder.py`
- Modify: `tests/test_cli.py`

- [x] Verify SEC facts create primary evidence records with stable IDs.
- [x] Verify price CSV creates high-reliability market evidence.
- [x] Verify repeated runs are idempotent.
- [x] Verify `build-evidence TICKER` prints fetched/new record counts.

### Task 2: Implement Evidence Builder

**Files:**
- Create: `src/value_invest_research/evidence_builder.py`

- [x] Extract latest SEC XBRL facts for revenue, income, margins, balance sheet, cash, and FCF-adjacent metrics.
- [x] Convert the latest price row into a market evidence record.
- [x] Validate records through `EvidenceRecord.from_dict`.
- [x] Append only records with new IDs and hashes.
- [x] Log the build with `RunLog`.

### Task 3: Wire CLI And Docs

**Files:**
- Modify: `src/value_invest_research/cli.py`
- Modify: `README.md`
- Modify: `AGENTS.md`

- [x] Add `build-evidence TICKER`.
- [x] Document evidence output location and intended use before `research-stock`.

### Task 4: Verify

**Commands:**

```powershell
python tools/run_tests.py
python -m compileall -q src tests tools
python -c "import sys; sys.path.insert(0, 'src'); from value_invest_research.cli import main; raise SystemExit(main(['--help']))"
```
