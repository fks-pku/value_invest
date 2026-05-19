# Value Invest Research

File-system-first US equity research assistant built around company foundation analysis first, then FengHe 3C3D5M3T message-flow analysis. Plain files are the source of truth; Python code validates contracts, scaffolds research objects, ingests public data, and creates LLM research drafts.

## Module Index

| Module | Path | Purpose |
|------|------|------|
| Core package | `src/value_invest_research/` | CLI, schemas, scaffolding, ingestion, run logs, and LLM research workflows. |
| Tests | `tests/` | unittest coverage for schemas, CLI, scaffolding, ingestion, and research workflow prompt/output behavior. |
| Research skill | `skills/value_invest_research/` | Operating protocol, frameworks, prompts, and evidence checklists. |
| Config | `config/` | Watchlist, source priority, research object registry, and event playbooks. |
| Stock objects | `stocks/` | Stock memos, evidence logs, structured data, run logs, and proposals. |
| Research objects | `research/` | Sector/theme/event memos, evidence, candidate screens, and run logs. |

## Research Sequence

For individual companies, complete a foundation analysis before using FengHe:

- Source and origin: company gene, founding context, original problem solved.
- Company history: business, governance, financing, M&A, restructuring, and capital allocation.
- Current business: business model, customers, demand, pricing, profitability, and cash conversion.
- Value chain position: supplier/channel/customer power and where economics are captured or lost.
- Competitive landscape: peers, market structure, ranking, share trend, and competition intensity.
- Strategy analysis: mission, corporate strategy, competitive strategy, functional strategy.
- Organization, culture, and governance: leadership, incentives, ownership, control, board, culture.
- Risk sweep: business, financial, accounting, legal, regulatory, technology, governance, and valuation risks.

Use FengHe 3C3D5M3T after that foundation baseline for message flow, events, catalysts, and thesis changes:

- 3C: Cycle, Change, Certainty.
- 3D: D1 ROE/intrinsic value, D2 marginal change/catalyst, D3 sentiment/valuation.
- 5M: M1 market size, M2 market share, M3 margin, M4 model, M5 management.
- 3T: T1 0-3 months, T2 3-15 months, T3 15+ months.

## Commands

```powershell
python tools/run_tests.py
$env:PYTHONPATH = "src"; python -m value_invest_research --help
value-invest-research --help
value-invest-research build-evidence AAPL
value-invest-research build-research-graph AAPL
value-invest-research research-stock AAPL --api-key $env:LLM_API_KEY
```

## Key Constraints

- Do not issue final trading instructions.
- Keep material claims tied to evidence IDs.
- Separate facts, inferences, and judgments.
- Keep low-reliability evidence as research leads only.
- Preserve existing research history; proposals are safer than silent memo overwrites.
- Optional integrations must fail with clear install guidance when dependencies are missing.
- Every stock-level output must state company foundation status and material foundation gaps.
- Every thesis-strengthening output must include a dominant D driver, matching 3T time frame, and disconfirming tests.
- Research graph outputs must preserve node/edge traceability from evidence to consensus, questions, hypotheses, assumption tests, and reports.
