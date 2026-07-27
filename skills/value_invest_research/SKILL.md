---
name: value-invest-research
description: Use for end-to-end investment research that starts from a research goal, adapts professional questions by domain, actively searches and parses evidence, evaluates S-curve/BOM opportunities, and produces a gated target observation report.
---

# Value Invest Research Skill

Use this skill for all investment research in this repository.

## Canonical References

- Internal question/execution contract: `frameworks/research_goal_qa.md`
- Public Markdown contract: `frameworks/research_report_contract.md`
- Domain playbooks: `frameworks/domain_playbooks.md`
- Architecture: `../../docs/architecture/hexagonal_research_system.md`
- Professional source registry: `../../config/source_universes.json`
- Material classes and feed profiles: `../../config/material_feeds.json`

Do not mix another report template into this workflow.

## End-to-End Sequence

1. Convert the request into `ResearchGoal` with mode, date, decision, scope, and domain hint.
2. Use `investment-question-architect` plus the domain playbook to build internal QA to maximum depth five.
3. For S-curve work, define a canonical BOM taxonomy and run the six-question research loop for every node.
4. Mirror all PDFs from the user's IMA daily directory into the central provider archive, then run two evidence loops: question-driven Universe/Exa search and BOM routing from that archive.
5. Classify every discovered document by `material_class` and `ingestion_channel`, route it to the matching BOM inbox, and create narrow question-specific parse tasks.
6. Parse one source at a time against the current question with the appropriate specialty skill. DeepSeek may perform first-pass reading when available; GPT verifies every adopted claim.
7. Roll facts, inference, judgment, gaps, refutation, and triggers upward.
8. Run company exposure and as-of valuation analysis.
9. Score and rank only after semantic completion gates.
10. Freeze historical recommendations, then attach labels.
11. Build `ReportViewModel` and render the four-section public report.

## Non-Negotiable Research Rules

- Facts, inferences, judgments, leads, and gaps are distinct.
- Every material claim has a claim-near source link or traceable source ID.
- Messages/opinions are leads unless independently verified.
- The same source is re-parsed for every question dimension it serves.
- Search is active and question-level. A general source pool cannot replace a fresh minimum-unit search.
- Active search starts from explicit evidence gaps, while external reports may introduce previously unknown metrics or mechanisms through atomic claim mapping.
- Discovery is not evidence: unparsed search or IMA material stays in the intake ledger and BOM inbox until question-specific parsing plus GPT review.
- Actual history and forward expectations remain separate.
- Acceleration claims need same-definition history or explicit YoY/multiple evidence.
- Future runway needs cutoff-visible guidance/forecast/TAM/customer budget plus first-principles support.
- Refutation search happens before confidence is strengthened.
- In backtests, model prior is not evidence and later price data is label-only.

## S-Curve and BOM Loop

Before researching any node, create or load its own `BomNodePlaybook`. The six public question labels are shared. Each playbook must define:

- exact node boundary, inputs, outputs, downstream recipients, representative companies, and financial validation metrics;
- node-specific demand, market-value, effective-supply, and investment-odds equations or equivalent causal formulas;
- exactly six question playbooks;
- a concise node-specific reasoning hint for each question; the hint is optional guidance, not a mandatory evidence path;
- conclusion rules that state when the question passes, remains pending, or is refuted.

Enforce:

`one industry-chain project -> one boms/<node_id>/ child project per canonical BOM node`

`one canonical BOM node -> one six-question playbook -> one temporal ledger -> reproducible snapshots -> one independent BOM report`

The canonical BOM registry and playbook registry must have exact one-to-one node-ID coverage. Never reuse HBM's chain for compute, networking, manufacturing, power/cooling, or system delivery. Never let a renderer's static prose or a generic fallback stand in for a missing node playbook. Playbooks contain no run-specific sources, dates, facts, verdicts, or presentation classes.

For every canonical BOM node, research:

1. Demand pull-through and unit/system elasticity.
2. Effective supply response: capacity, yield, qualification, equipment, materials, and cycle.
3. Supply controller: share, IP, ecosystem, qualification, substitution, and customer lock-in.
4. Financial realization: revenue, margin, orders/backlog, cash flow, and guidance.
5. Pricing: as-of valuation, implied expectations, revisions, and payoff odds.
6. Refutation: observed contrary evidence, threshold, cadence, and downgrade action.

Every question keeps one compact judgment model and optional logic hint. The public report uses:

`基本理解思路 -> 当前结论 -> 相较上一截面的变化 -> 时间演化 -> 映射材料 -> 信息覆盖`

Do not require one evidence card per logic-hint row. Evidence is stored as atomic claims mapped to `BOM x question x time`, so new themes can enter even when the initial hint did not anticipate them.

A BOM stage is pending until all six questions complete. Completion requires source planning, pull search, ingestion of available external materials, question-specific atomic parsing, temporal coverage, and strengthening evidence. Q6 is incomplete without explicit refuting evidence.

## Source Planning and Parsing

GPT decides the source Universe based on topic and minimum question. Resolve candidates from `config/source_universes.json`, then add justified official/company/customer sources.

Every document carries:

- `material_class`: official filing, official company, sell-side research, authoritative third party, market news, expert opinion, or other;
- `ingestion_channel`: question search, IMA knowledge-base scan, or manual import;
- provider/external identity, content hash, publication/discovery time, matched BOM nodes, mapping status, and cutoff usage.

Knowledge-base dates remain orthogonal: an IMA year/month/day folder and provider
create/update timestamps describe archive or ingestion activity, not market
publication. `published_at` may come only from an explicit publication field, a
dated report title, or the original cover/header. Preserve date status, provenance,
and locator. An unresolved date stays blank and blocks claim promotion until the
original PDF is verified.

The repository-level `source/ima/YYYY/MM/DD/` tree mirrors IMA's verified
`directory_date` and stores every PDF, regardless of current BOM relevance. The
archive path never supplies `published_at`. Its manifest preserves directory
provenance, content hash, size, and local path without raw knowledge-base IDs or
signed URLs.

Question search routes only to the requested `BOM x question`. Downstream IMA
routing reads the central archive, searches each configured BOM profile, and creates
question-specific parse tasks for matched reports. A matched report is copied into
that project's `source/ima/<published_at>/` only after publication-date verification;
the complete provider mirror remains in repository `source/ima/<directory_date>/`.
A report may route to several BOMs and must be parsed separately for each relevant
question. Persist the source path relative to the BOM project. The local HTML
renderer keeps that project-relative `source/...` link so browser clicks resolve
beside the report; the Markdown renderer uses an absolute filesystem link.

The intake sequence is:

`daily full-PDF archive -> BOM classify -> deduplicate -> publication-date/cutoff gate -> copy selected original into BOM -> parse inbox -> DeepSeek/specialty parse -> GPT review -> atomic claim ledger`

Credentials and the raw knowledge-base ID never enter Git. Read IMA access from `IMA_OPENAPI_CLIENTID`, `IMA_OPENAPI_APIKEY`, and `IMA_KNOWLEDGE_BASE_ID`; persisted feed state stores only an irreversible reference hash. A frozen historical project quarantines documents published after its cutoff.

Daily IMA archiving is provider-driven and independent of research projects.
Resolve the configured knowledge-base name, walk the selected year/month/day
directory with full pagination, and download every PDF to repository
`source/ima/<directory_date>/`. Persist one manifest record per PDF and one scan
event per day. Repeated runs reuse existing verified files and retry only missing or
failed originals. The scheduled job archives the previous day and rechecks the configured
recent-day window so quota-limited gaps can recover on later days. BOM routing is a
separate downstream operation that persists all
relevance decisions so omissions remain auditable and creates tasks from that
project's own coordinate registry.
Canonical BOM children produce six tasks; a `standalone-bom` project produces its
five lens tasks. The parser must answer the current coordinate from the original
report, record page/section, data or argument, time fields, stance, and gaps, then
GPT reviews the result before it enters `ledger/claims.jsonl`. Only reviewed claims
and a reviewed conclusion update may rebuild the public Markdown timeline.

Each leaf task stores:

- `source_universe_plan`
- `source_search_plan`
- direct/Exa queries
- selected source IDs or gap reasons
- expected extraction fields
- refuting source plan
- cutoff policy

Create one `source_extractions.jsonl` row and one `leaf_source_reviews.jsonl` row per `question x source`. Never attach a multi-source conclusion to only the first source.

Route materials through:

- `financial-statement-analysis`
- `valuation-analysis`
- `industry-report-analysis`
- `news-event-analysis`
- `opinion-analysis`
- `company-exposure-analysis`
- `supply-chain-chokepoint-analysis`
- `leaf-research-deepseek`

## Target Gate

The default action state is conservative. `actionable_long` requires all of:

- canonical BOM mapping;
- six questions complete;
- explicit refuting evidence verified;
- company exposure and financial bridge explicitly verified, never inferred from a generic target evidence list;
- as-of valuation/mispricing verified;
- auditable component-specific score evidence;
- quantitative kill tests.

Otherwise use `watch_only`; missing BOM mapping is `no_action`.

Every score subcomponent is either verified with evidence/review IDs and `evidence_role`, or a `gap` with `gap_reason`. Do not reuse the same broad evidence list for every component.

## Public Output

The default user-facing artifact is `professional_report.html`; the same view model
also writes `professional_report.md` as a portable audit sidecar. The default
industry/project report contains exactly:

1. `当前研究的问题`
2. `行业概况`
3. `标的推荐`
4. `来源索引`

Industry/S-curve output is split by scope. The parent
`professional_report.html` declares `report_scope: industry-index` and links to
`boms/<node_id>/professional_report.html`. It never embeds all six-question
modules. Each child declares `report_scope: bom-node`, contains exactly one BOM
module, preserves the six questions and S-curve rollup, and links back to the
parent. Markdown mirrors the public content for auditability.

When the research object is explicitly one BOM rather than an industry chain, use
`report_scope: standalone-bom`. Render five collapsible top-level HTML sections:
`需求侧`, `供给侧`, `技术侧`, `估值侧`, and `ESG`. Every section contains one
`简单逻辑链`, one newest-to-oldest `信息时间线`, and one `最新结论与趋势`.
The HTML timeline uses one full-width, horizontally scrollable table per lens with
exactly `时间 | 信息类型 | 报告 | 观点列表`. One material occupies one row; the
report title links directly to the original PDF, and multiple atomic claims from
the same source and lens stay in one real bullet list using
`观点 N / 原文位置 / 原子观点`. The Markdown audit sidecar mirrors the compact
four-column table. Local PDF links navigate in the current tab; only HTTP(S)
sources open a new tab. Do not expose source-search process fields.

Every standalone BOM and every `boms/<node_id>/` child is a self-contained project
directory. It owns `project.json`, `professional_report.html`,
`professional_report.md`, `sources.jsonl`,
`source/`, `material_intake/`, `inbox/`, and `ledger/`. Canonical originals live
only under `source/<provider>/YYYY/MM/DD/`; `material_intake/` stores discovery and
audit metadata, never a second canonical PDF store. The parent owns only
`boms/manifest.json`, canonical taxonomy, navigation, and aggregated targets.
Public `下钻 QA`, raw Universe/Exa/IMA queries, provider IDs, parser traces,
workbench data, and framework-change notes remain hidden unless requested.

Use nested collapsed `details`, claim-near blue links, one full-width sibling card per row, and local `table-scroll` for wide tables. Keep the public report clean and research-first.

## Validation

Before completion:

- run focused and framework unit tests;
- run `validate-report-contract`;
- run `validate-material-intake` after question search or knowledge-base scanning;
- run `validate-research-artifacts --require-l3`;
- inspect Markdown/static invariants;
- confirm no failed research gate renders as `actionable_long`;
- run `git diff --check`.
