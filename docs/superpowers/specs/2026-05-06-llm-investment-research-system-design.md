# LLM Investment Research Assistant Design

Date: 2026-05-06

## 1. Goal

Build a file-system-first LLM research assistant for US equities. The first version covers a small watchlist of 5-20 stocks, automatically collects public information, maintains long-lived research documents, and helps a human investor identify candidates for deeper work.

The system is not an automated trading system. It does not place orders, manage a portfolio, or issue final buy/sell instructions. Its job is to preserve evidence, update investment views, surface disconfirming information, and produce auditable research signals for human review.

## 2. First-Version Scope

The first version supports three research modes:

1. Stock research: maintain a FengHe 3C3D5M3T memo for each tracked company.
2. Sector and theme research: map industries, themes, value chains, key metrics, and candidate companies.
3. Event research: rapidly analyze sudden market events, build transmission chains, and identify investable candidates for further stock-level research.

Initial constraints:

- Market: US equities.
- Stock universe: manually curated watchlist of 5-20 names.
- Primary framework: FengHe 3C3D5M3T.
- Data ingestion: automatic, with human review gates for important thesis changes.
- Storage model: files are the source of truth; structured JSON/CSV outputs are kept so a database can be added later.

## 3. Design Principles

- Evidence before opinion: every material claim links to source evidence.
- Separate facts, inference, and judgment: the memo must make clear what is observed, what is inferred, and what is concluded.
- Preserve research history: old thesis changes are archived instead of silently overwritten.
- Prefer narrow automation: automatic ingestion and draft updates are allowed; final investment decisions remain manual.
- Make the Skill the research protocol: prompts, checklists, framework rules, and output contracts live in a reusable Skill.
- Design for later database migration: every evidence item and signal has stable IDs and structured metadata.

## 4. Repository Layout

```text
value_invest/
  skills/
    value_invest_research/
      SKILL.md
      frameworks/
        fenghe_3c3d5m3t.md
        value_investing.md
        sector_research.md
        event_research.md
      checklists/
        evidence_quality.md
        fenghe_research_review.md
        valuation_review.md
        disconfirming_evidence.md
      prompts/
        update_stock_memo.md
        run_sector_research.md
        run_event_research.md

  research/
    sectors/
      semiconductors/
        sector_memo.md
        industry_map.md
        value_chain.md
        key_metrics.md
        companies.yaml
        evidence.jsonl
        data/
        raw/
        logs/
    themes/
      ai_infrastructure/
        theme_memo.md
        transmission_map.md
        companies.yaml
        evidence.jsonl
        data/
        raw/
        logs/
    events/
      YYYY-MM-DD_event_slug/
        event_brief.md
        transmission_map.md
        candidate_screen.md
        tickers_to_review.yaml
        evidence.jsonl
        data/
        raw/
        logs/

  stocks/
    AAPL/
      company_profile.md
      investment_memo.md
      hypotheses.md
      signals.md
      evidence.jsonl
      data/
        fundamentals.json
        prices.csv
        sec_filings.json
        news.jsonl
      raw/
        sec/
        earnings_calls/
        news/
      logs/
        runs.jsonl

  pipelines/
    ingest_sec.py
    ingest_prices.py
    ingest_news.py
    ingest_company_ir.py
    run_event_research.py
    run_sector_research.py
    update_stock_memo.py
    route_evidence.py

  config/
    watchlist.yaml
    research_objects.yaml
    event_playbooks.yaml
    source_priority.yaml
    pipeline_schedule.yaml

  docs/
    system_design.md
```

## 5. Research Object Model

The system treats stock, sector, theme, and event folders as research objects. Each object has:

- A canonical memo.
- Raw source files.
- Structured data extracts.
- An evidence log.
- Run logs.
- Links to related research objects.

The common evidence record is stored in JSON Lines:

```json
{
  "id": "ev_20260506_aapl_10q_001",
  "research_object": "stocks/AAPL",
  "source_type": "sec_filing",
  "source_name": "10-Q",
  "url": "https://...",
  "published_at": "2026-05-01T00:00:00Z",
  "fetched_at": "2026-05-06T08:00:00Z",
  "hash": "sha256:...",
  "tickers": ["AAPL"],
  "sectors": ["technology_hardware"],
  "themes": ["services_growth"],
  "summary": "Short factual summary only.",
  "reliability": "primary",
  "materiality": "medium",
  "used_in": ["investment_memo.md"]
}
```

Reliability levels:

- primary: SEC filings, company investor relations, official transcripts, audited financials.
- high: reputable financial press, exchange data, established data providers.
- medium: specialist blogs, expert commentary, industry newsletters.
- low: social media, unattributed rumors, unsourced summaries.

Low-reliability evidence can trigger research questions but cannot by itself change a thesis.

## 6. Stock Research Memo

Each tracked stock has a persistent `investment_memo.md`. The memo is a living research ledger, not a one-off report.

Required sections:

```text
# TICKER Investment Memo

## 0. Current View
- View: Watch / Attractive / Expensive / Avoid / Needs Review
- Confidence: Low / Medium / High
- Last Updated:
- FengHe Summary:
- Most Important Uncertainty:

## 1. 3C Investment Philosophy
- Cycle
- Change
- Certainty

## 2. 3D Price Drivers
- D1 ROE / intrinsic value
- D2 marginal change / catalyst
- D3 sentiment / valuation
- Dominant driver

## 3. 5M Value Analysis
- M1 market size
- M2 market share
- M3 margin
- M4 model
- M5 management
- Key value driver
- Key defect risk

## 4. 3T Time Frame
- T1 0-3 months
- T2 3-15 months
- T3 15+ months
- Active time frame

## 5. Certainty, Risk, And Disconfirming Evidence
- Evidence that supports certainty
- Thesis breakers
- Disconfirming tests

## 6. Valuation And Risk/Reward
- Normalized earnings or FCF
- Conservative assumptions
- Downside case
- Base case
- Upside case
- Margin of safety

## 7. Evidence Log
- New facts
- Source IDs
- Reliability
- Impact on thesis

## 8. Human Review Questions
- What needs more research
- What would change the view
```

The Skill updates the memo by appending dated changes to the evidence log and revising current sections only when the evidence threshold is met.

## 7. Sector And Theme Research

Sector and theme research exists to discover companies worth deeper investigation and to maintain context that individual company memos cannot capture.

Sector memo sections:

```text
# Sector Memo

## 1. Current Sector View
- Attractiveness
- Cycle position
- Key thesis
- Confidence

## 2. Industry Structure
- Value chain
- Profit pools
- Competitive dynamics
- Barriers to entry

## 3. Demand Drivers
- End markets
- Secular growth
- Cyclical factors

## 4. Key Metrics
- Revenue growth
- Gross margin
- Capex
- Inventory
- Pricing
- Utilization

## 5. Company Map
- Leaders
- Challengers
- Niche compounders
- Cyclical candidates
- Avoid or watchlist

## 6. Cross-Company Comparison
- Quality
- Growth
- Balance sheet
- Valuation
- Risks

## 7. Signals To Individual Stocks
- Companies to add
- Companies to downgrade
- Thesis changes
- Open questions

## 8. Evidence Log
```

Theme research uses the same structure but emphasizes cross-sector transmission. For example, AI infrastructure can connect semiconductors, cloud platforms, utilities, data centers, networking, cooling, and capital equipment.

## 8. Event Research

Event research is the rapid-response mode for sudden shocks such as geopolitical conflict, regulatory decisions, major product breakthroughs, commodity disruptions, or financial stress.

The event workflow:

1. Create an event folder under `research/events/`.
2. Collect confirmed facts and separate them from rumors.
3. Build transmission chains.
4. Map affected sectors, themes, and companies.
5. Screen candidate stocks by mechanism, exposure, financial sensitivity, and valuation.
6. Output a ranked candidate list for human review.
7. Promote selected candidates into stock-level research.

Event folder structure:

```text
research/events/YYYY-MM-DD_event_slug/
  event_brief.md
  transmission_map.md
  candidate_screen.md
  tickers_to_review.yaml
  evidence.jsonl
  data/
  raw/
  logs/
```

Candidate screen format:

```yaml
event: us_iran_conflict
goal: find_investable_candidates
generated_at: 2026-05-06T08:00:00Z
candidates:
  - ticker: XOM
    tier: 1
    direction: positive
    mechanism: oil price upside may increase cash flow
    key_tests:
      - production exposure
      - hedge position
      - balance sheet
      - valuation sensitivity to oil price
    disconfirming_tests:
      - oil price response fades quickly
      - company is already priced for elevated crude
      - political pressure reduces realized benefit
    required_next_step: update stock memo
```

Candidate tiers:

- Tier 1: worth immediate deep research.
- Tier 2: add to watchlist or monitor.
- Tier 3: evidence is too weak or the effect is likely noise.
- Negative Watch: likely harmed by the event.

## 9. Event Playbooks

Event playbooks encode common transmission templates. They accelerate the first hour of research without forcing a conclusion.

Example:

```yaml
geopolitical_conflict:
  first_questions:
    - What happened, and what is confirmed?
    - Which geographies, commodities, supply chains, or military systems are directly involved?
    - What is the plausible duration and escalation path?
  transmission_channels:
    - energy_prices
    - shipping_routes
    - insurance_costs
    - defense_spending
    - inflation_expectations
    - currency_safe_haven
  affected_sectors:
    potential_positive:
      - energy_producers
      - defense_contractors
      - shipping
      - commodity_infrastructure
    potential_negative:
      - airlines
      - chemicals
      - travel
      - import_dependent_retail
  mandatory_checks:
    - Does the company have direct exposure?
    - Is the impact material to earnings or free cash flow?
    - Is the move already priced in?
    - What evidence would falsify the event thesis?
```

## 10. Skill Responsibilities

The `value_invest_research` Skill is the core operating protocol. It must instruct the LLM to:

- Load the relevant research object memo, evidence log, structured data, and run logs before analysis.
- Classify each new item as fact, inference, opinion, rumor, or irrelevant.
- Assign reliability and materiality.
- Link every material conclusion to evidence IDs.
- Look for disconfirming evidence before strengthening any thesis.
- Avoid changing the current view based only on low-reliability sources.
- Preserve historical reasoning when updating a memo.
- Produce a structured research signal for human review.

The Skill should expose three workflows:

- `update_stock_memo`: update one company using the value-investing framework.
- `run_sector_or_theme_research`: map an industry or theme and produce candidate companies.
- `run_event_research`: analyze a sudden event and produce a candidate screen.

## 11. Research Signals

Signals are research outputs, not trading instructions.

Stock signal:

```yaml
ticker: AAPL
date: 2026-05-06
view: watch
confidence: medium
signal_strength: 2
time_horizon: long_term
changed_since_last_run: true
drivers:
  - type: positive
    item: free cash flow durability improved
    evidence_id: ev_20260506_aapl_10q_001
  - type: negative
    item: valuation leaves limited margin of safety
    evidence_id: ev_20260506_aapl_price_001
action_for_human:
  - review valuation assumptions
  - compare current margins with normalized cycle assumptions
```

Event signal:

```yaml
event: us_iran_conflict
date: 2026-05-06
status: active_research
top_candidate_count: 5
highest_priority_next_step: update Tier 1 stock memos
major_uncertainties:
  - event duration
  - oil price persistence
  - shipping disruption severity
```

## 12. Data Pipelines

The first version needs small, reliable pipelines:

- SEC ingestion: submissions, 10-K, 10-Q, 8-K, company facts, and filing metadata.
- Price ingestion: daily price and volume history for watchlist and candidate tickers.
- News ingestion: financial news, company investor relations pages, press releases, and trusted RSS feeds.
- Transcript ingestion: earnings call transcripts when provider access is available.
- Routing: assign each evidence item to stocks, sectors, themes, or events.
- Memo update: run the Skill against new evidence and create proposed changes.

Recommended cadence:

- Daily: prices, news, source routing, watchlist memo checks.
- Weekly: full watchlist memo refresh.
- On filing: SEC filing ingestion and stock memo update.
- On demand: event research and sector/theme deep dives.

## 13. Human Review Gates

The system can draft updates automatically, but these changes require human review before becoming canonical:

- Current view changes.
- Confidence upgrades.
- Candidate promoted from event research into the stock watchlist.
- Valuation assumption changes.
- Any thesis change based partly on medium- or low-reliability evidence.

Low-risk automatic updates:

- Append new primary-source evidence.
- Refresh prices and structured financial data.
- Add open questions.
- Mark duplicate or irrelevant news items.

## 14. Error Handling And Data Quality

The system should treat ingestion and analysis failures as research-state events, not silent errors.

Rules:

- Every pipeline run appends to `logs/runs.jsonl`.
- Failed fetches record source, error, retry count, and next retry time.
- Duplicate sources are detected by URL and content hash.
- Source summaries are regenerated only when the source hash changes.
- If conflicting evidence appears, the memo gets a conflict note instead of forcing one conclusion.
- If source reliability is low, the output can create an open question but cannot change the thesis.
- If the LLM cannot cite evidence IDs for a material claim, the claim is rejected.

## 15. Testing And Verification

Testing should focus on data integrity and research discipline:

- Unit tests for evidence parsing, hashing, deduplication, routing, and signal schema validation.
- Golden-file tests for Skill outputs on known research cases.
- Integration tests for one stock folder from raw source to proposed memo update.
- Event-research fixture test for a geopolitical event playbook.
- Regression tests that reject uncited thesis changes.
- Manual review checklist for first 10 production runs.

Acceptance criteria for the first usable version:

- A watchlist ticker can be initialized into a complete stock folder.
- New SEC filings and news items are stored with evidence IDs.
- The Skill can update `investment_memo.md` with cited evidence.
- An event research run can create a transmission map and ranked candidate screen.
- Candidate stocks can be promoted into stock-level research.
- All material claims in generated memos link back to evidence records.

## 16. Build Roadmap

Phase 1: repository skeleton and document templates.

- Create Skill directory and framework files.
- Create stock, sector, theme, and event memo templates.
- Define evidence and signal schemas.
- Create sample folders for one stock and one event.

Phase 2: ingestion foundation.

- Implement SEC, price, and news ingestion.
- Store raw files and normalized evidence.
- Add deduplication, hashing, and run logs.

Phase 3: Skill-driven memo updates.

- Implement `update_stock_memo`.
- Add human-review output format.
- Test against one or two watchlist companies.

Phase 4: event research.

- Implement event playbooks.
- Create `run_event_research`.
- Produce candidate screens and promotion workflow.

Phase 5: sector and theme research.

- Implement industry maps and cross-company comparisons.
- Connect sector/theme findings to stock memo updates.

Phase 6: optional database layer.

- Import evidence, signals, and facts into SQLite or Postgres.
- Add vector search for source retrieval.
- Add cross-stock dashboards and ranking views.

## 17. Open Design Decisions

The following decisions are intentionally deferred until implementation planning because they depend on available API keys, budget, and preferred runtime:

- Exact market data provider.
- Exact news provider.
- Whether to use SQLite from the start or defer it.
- Whether memo updates are committed through Git or stored as dated snapshots.
- Which LLM model runs each workflow.

The file contracts above are designed so these choices can change without rewriting the research model.
