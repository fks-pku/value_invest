# Value Invest Research

File-system-first investment research assistant for US equities. The project stores research objects as plain files, keeps structured evidence alongside memos, and provides CLI workflows for stock, event, sector, SEC, price, and LLM-assisted research.

The stock workflow is foundation-first: every company should first get an eight-section company foundation analysis. FengHe 3C3D5M3T is then used as the downstream message-flow layer for events, catalysts, marginal changes, time frames, and thesis updates.

This is not an automated trading system. It does not place orders or issue final buy/sell instructions; it helps preserve evidence and produce auditable research drafts for human review.

## Current Status

- Core scaffolding and validation are implemented.
- CLI commands exist for stocks, events, SEC ingestion, price ingestion, foundation-first stock research, structured research-system generation, memo updates, event research, and sector/theme research.
- A simplified research-system layer currently focuses on foundation coverage, business nodes, KPI snippets, assumptions, risk monitors, eight section detail pages, and a foundation dashboard.
- A deterministic research graph pipeline exists for FengHe consensus baselines, 3T questions, hypotheses, assumption tests, and forward reports.
- The primary stock research sequence is company foundation first, then FengHe message-flow analysis.
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
value-invest-research build-research-system AAPL
value-invest-research build-research-graph AAPL
value-invest-research validate-evidence stocks/AAPL/evidence.jsonl
value-invest-research research-stock AAPL --api-key $env:LLM_API_KEY
```

`research-stock` writes a timestamped Markdown report and structured signal JSON under `stocks/<TICKER>/research_reports/`.
`build-evidence` converts structured SEC facts and price CSV rows into stable evidence IDs under `stocks/<TICKER>/evidence.jsonl`.
`build-research-system` converts local evidence into the foundation-only research layer under `stocks/<TICKER>/research_system/`: `foundation_graph.json`, empty compatibility placeholders for `question_graph.jsonl` and `message_flow.jsonl`, eight section pages under `pages/`, and `research_dashboard.html`.
`build-research-graph` runs the full deterministic graph pipeline and writes `nodes.jsonl`, `edges.jsonl`, and `forward_report.html` under `stocks/<TICKER>/research_graph/`.

Graph stages are also callable one by one:

```powershell
value-invest-research build-consensus AAPL
value-invest-research generate-questions AAPL
value-invest-research build-hypotheses AAPL
value-invest-research test-hypotheses AAPL
value-invest-research write-forward-report AAPL
```

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

## Company Foundation Analysis

Each company memo starts with an eight-section baseline:

1. Source and origin.
2. Company history.
3. Current business.
4. Value chain position.
5. Competitive landscape.
6. Strategy analysis.
7. Organization, culture, and governance.
8. Risk sweep.

This baseline answers "what is this company?" before asking what new information changes the thesis.

## Research System Layer

The research-system layer is the professional stock workspace between raw evidence and final reports. The active generator is intentionally foundation-only: first build the company baseline, then add downstream FengHe message-flow work later.

- `foundation_graph.json`: eight-section foundation coverage, facts, inferences, judgments, gaps, business nodes, KPIs, assumptions, risks, key questions, and four-bucket information mapping.
- `pages/*.html`: one detail page per foundation section.
- `question_graph.jsonl`: empty compatibility placeholder until downstream question generation is re-enabled.
- `message_flow.jsonl`: empty compatibility placeholder until downstream message-flow analysis is re-enabled.
- `research_dashboard.html`: a readable foundation dashboard for the first-layer company baseline.

This layer should be built before writing polished reports. Reports are outputs; the durable research asset at this stage is the structured company baseline.

## Research Graph Pipeline

The graph pipeline is the FengHe message-flow graph. It treats current facts and market consensus as the priced baseline after company foundation work exists. It then creates a local graph:

- Evidence nodes: validated `EvidenceRecord` entries.
- Framework nodes: FengHe 3C, 3D, 5M, and 3T concepts for message-flow analysis.
- Consensus nodes: what the current local evidence can support as baseline.
- Question nodes: what could change by T1/T2/T3.
- Hypothesis nodes: mechanisms that could move D1/D2/D3.
- Assumption-test nodes: what evidence would support or disconfirm each hypothesis.

The forward report is an HTML synthesis of the graph, not a final trading instruction.

## Boundaries

Research outputs must separate facts, inferences, and judgments. Material claims should cite evidence IDs. Low-reliability sources can create research questions, but should not change a thesis by themselves. Generic "good company" language is not enough: every stock view must state foundation status and gaps first, then cycle, marginal change, certainty, dominant D driver, 5M value/defect drivers, time frame, and disconfirming tests when analyzing message flow.
