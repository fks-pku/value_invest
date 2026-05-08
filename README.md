# Value Invest Research

File-system-first FengHe-style investment research assistant for US equities. The project stores research objects as plain files, keeps structured evidence alongside memos, and provides CLI workflows for stock, event, sector, SEC, price, and LLM-assisted research.

This is not an automated trading system. It does not place orders or issue final buy/sell instructions; it helps preserve evidence and produce auditable research drafts for human review.

## Current Status

- Core scaffolding and validation are implemented.
- CLI commands exist for stocks, events, SEC ingestion, price ingestion, FengHe stock research, memo updates, event research, and sector/theme research.
- The primary research framework is FengHe 3C3D5M3T: Cycle, Change, Certainty; D1/D2/D3 price drivers; M1-M5 value analysis; and T1/T2/T3 time frames.
- Third-party integrations are optional. Core commands work without `openai`, `pyyaml`, or `yfinance`; integration commands report a clear install hint when their package is missing.
- The repository includes sample AAPL, event, and sector research artifacts.

## Install

Core editable install:

```powershell
python -m pip install -e . --no-deps
```

Optional integrations:

```powershell
python -m pip install -e ".[all]"
```

Use narrower extras when preferred:

```powershell
python -m pip install -e ".[ingest]"
python -m pip install -e ".[llm]"
python -m pip install -e ".[research]"
```

## Run

Without installing, use `PYTHONPATH=src` or the test runner in this repo.

```powershell
$env:PYTHONPATH = "src"
python -m value_invest_research --help
```

After editable install:

```powershell
value-invest-research --help
```

Examples:

```powershell
value-invest-research init-stock MSFT --company-name "Microsoft Corporation"
value-invest-research init-event 2026-05-06 "US Iran Conflict"
value-invest-research build-evidence AAPL
value-invest-research validate-evidence stocks/AAPL/evidence.jsonl
value-invest-research research-stock AAPL --api-key $env:LLM_API_KEY
```

`research-stock` writes a timestamped Markdown report and structured signal JSON under `stocks/<TICKER>/research_reports/`.
`build-evidence` converts structured SEC facts and price CSV rows into stable evidence IDs under `stocks/<TICKER>/evidence.jsonl`.

## Test

The repository test runner adds `src` to `sys.path` and avoids platform temp-directory permission issues by using a local ignored `.test_tmp/` folder.

```powershell
python tools/run_tests.py
```

## Layout

- `src/value_invest_research/`: Python package and CLI workflows.
- `tests/`: unittest suite and test helpers.
- `skills/value_invest_research/`: reusable research protocol, frameworks, prompts, and checklists.
- `config/`: editable watchlist, source priority, research objects, and event playbooks.
- `stocks/`: stock-level research objects.
- `research/`: event, sector, and theme research objects.
- `docs/superpowers/`: design specs and implementation plans.

## Boundaries

Research outputs must separate facts, inferences, and judgments. Material claims should cite evidence IDs. Low-reliability sources can create research questions, but should not change a thesis by themselves. Generic "good company" language is not enough: every stock view must state the cycle, marginal change, certainty, dominant D driver, 5M value/defect drivers, time frame, and disconfirming tests.
