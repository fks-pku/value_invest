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
- Refutation search happens before a conclusion is strengthened.
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

The central archive uses the user's visible, logged-in IMA page. Do not call IMA
OpenAPI, hidden download URLs, `archive-ima-day`, or `archive-ima-daily`; do not
read browser credentials, cookies, tokens, or raw knowledge-base IDs. A frozen
historical project quarantines documents published after its cutoff.

Daily IMA archiving is UI-driven, attended, and independent of research projects.
Reuse the logged-in IMA page, walk the selected year/month/day directory across all
pages or lazy-loaded rows, click every missing PDF's visible download control, and
import completed browser downloads into repository
`source/ima/<directory_date>/`. Persist one manifest record per visible PDF and one
scan event per day. Repeated runs reuse existing verified files and click only
missing or failed originals. BOM routing is a separate downstream operation that persists all
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
`第一性原理逻辑链`, full-width `逻辑节点与原子观点材料`, and optional
`派生证据视图`. Do not render a separate lens-level `全局结论与趋势`; keep the
global synthesis only in the leading `当前投资判断`, with node conclusions attached
to their evidence. The primary evidence hierarchy is
`lens -> causal node -> source row -> numbered atomic claim`. Every causal node
body contains exactly one newest-to-oldest table with
`发布日期 | 报告名称 | 材料类型 | 原子观点 | 对逻辑点的影响`. One source occupies one
row; claims and effects use matching `1, 2, 3...` numbering. The report-name link
is blue. Locator, effective period, and target period remain compact labels in the
atomic-claim cell. Do not render separate public state-history, event-history,
filter, or company/entity audit modules. Internal mappings, real as-of states,
revisions, gaps, and entity states remain append-only and auditable. Precede the five lenses
with one gated `当前投资判断` that separates fundamental, consensus, and priced-in
changes. Its lead paragraph rolls up strengthened causal nodes, main breakpoints,
and failed gates. Keep source-batch or Q2-specific updates in a separate
`本期证据变化` line so a local view never substitutes for the global judgment.

If the user explicitly requests fewer public modules in one lens, keep the full
internal playbook and append-only evidence ledgers, and use that lens's
`public_logic_node_ids` to select the rendered modules in canonical order. A
`logic_chain_centered` playbook must keep every causal node public; narrowing may
omit only derived views and never deletes research history. A visible Q2 demand
quantity matrix must retain its visible Q1 demand-party classification view.

In `logic_chain_centered` research, the playbook declares a versioned
`logic_chain_version`. Atomic claims use a minimum audit envelope instead of one
universal metric table. A separate reviewed mapping records `support`, `refute`,
`boundary`, `constraint`, `new_branch`, `conflict`, `unresolved`, `neutral`, or
`unmapped`, plus node fit, support/refute rule match, claim-specific rationale, and
downstream impacts. `support` and `refute` require direct node fit and an explicit
match to the node rule; forecasts, proxies, contextual inputs, and incomplete
observations use the other effects. A rejected claim-to-node proposal remains
`unmapped`, is excluded from the public node table and node state, and preserves
its audit trail. A claim stays immutable and is interpreted once at its primary
causal node; new mechanisms remain visible for chain revision.

If the demand lens begins with Q1 `需求方`, that node answers only who demands the
BOM. Its public output is two lists: `当前需求方` and `潜在未来需求方`. Keep
business scenarios, tasks/workloads, host systems, component specifications,
procurement channels, quantities, and as-of change assessment out of Q1. Put the
current quantity baseline in Q2 and demand mechanisms in the later nodes. A Q1
node using `render_mode: demand_party_list` does not render entity snapshots or
material tables, although its underlying ledgers remain immutable and auditable.

Treat Q1 and Q2 as `presentation_role: derived_view`. They support navigation and
local quantity comparison but do not replace the demand chain or generate the lens
conclusion. Keep the full causal path from workload through compute intensity,
budget, orders/delivery, and financial realization visible before these views.

Q2 inherits both Q1 demander lists. Render three outer groups in this exact order:
`当前需求方`, `潜在未来需求方`, and `其它分类`. The first two groups contain one
specific category per Q1 demander; the third groups unallocatable totals and
forecasts by their own information category. Every specific category owns one table
and may contain multiple information rows. Each table uses `来源 | 期间 | 信息类型 |
具体信息`; use an explicit gap row when no credible current quantity exists, and
allow a clear empty state for a potential-future category. `信息类型` classifies
source material as `官方财报`, `第三方研究`, `市场消息`, or `机构研报`. Keep the
metric, quantity or forecast, mapping quality, and caveat together in `具体信息`.
Potential-future observations do not enter the current baseline, and other
forecasts never claim a Q1 demander mapping. In HTML, both the outer groups and
their specific categories are collapsed disclosures by default; Markdown mirrors
the same numbered hierarchy. Never allocate an aggregate mechanically or sum
incompatible units, overlapping samples, and supplier values.

The standalone workflow is:

`atomic claim -> reviewed logic-node and entity mapping -> as-of logic state + entity state -> baseline/change revision -> company earnings and valuation bridge -> gated investment snapshot`

Keep atomic claims immutable. Store mappings, node states, revisions, and investment
snapshots in separate append-only ledgers. Entity snapshots live in
`entity_states.jsonl` and use the coordinate
`BOM x lens/question x logic node x company/entity x as_of_date`. A first
structured snapshot establishes a
baseline and never claims a historical change. Unmapped themes remain visible for
review. A new positive industry claim cannot directly change an action state without
passing the company financial, valuation, refutation, and risk-control gates.
Do not compute or display numeric or qualitative confidence scores. Explain the
judgment through supporting claims, refuting claims, source conditions, gaps, and
the next falsifiable validation instead.
The Markdown audit sidecar mirrors each causal node's five-column material table.
Local PDF links navigate in the current tab; only HTTP(S) sources open a new tab.
Do not expose source-search process fields. Company/entity coordinates remain in
the append-only internal ledger and investment snapshot rather than a duplicate
public evidence module.

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
