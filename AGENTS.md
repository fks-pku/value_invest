# Value Invest Research

File-system-first investment research system. Plain research artifacts are the source of truth; Python code owns contracts, orchestration, validation, scoring, and rendering.

## Immutable Investment Logic

Find a large and durable S-curve, identify scarce or hard-to-substitute BOM/value-chain nodes, then select only securities whose earnings path is not fully priced and whose downside is monitorable.

Every investable conclusion must prove:

1. The S-curve is real, feasible, large, and near an adoption inflection.
2. The mapped BOM node is genuinely scarce or difficult to bypass.
3. The company can convert that node into revenue, margin, free cash flow, or rerating.
4. The market has not already priced the full path.
5. The target passes `scarcity_or_monopoly`, `mispricing`, `earnings_elasticity`, and `risk_control`.

Theme exposure, TAM headlines, convenient tickers, and post-cutoff price performance are not investment evidence.

## Architecture Contract

Follow the hexagonal dependency rule in `docs/architecture/hexagonal_research_system.md`:

- `src/value_invest_research/domain/`: pure research rules, entities, scoring, readiness, and quality gates.
- `src/value_invest_research/application/`: use cases. It may depend on domain and ports, never concrete adapters.
- `src/value_invest_research/ports/`: repository, search, parser, renderer, and data protocols.
- `src/value_invest_research/adapters/`: file system, Exa/search, LLM/DeepSeek,
  market data, CLI, default HTML, and Markdown audit renderers.
- `config/source_universes.json`: professional source universe registry.
- `skills/value_invest_research/`: canonical workflow and presentation contracts.

New topics enter through:

`ResearchGoal -> DomainPlaybook -> QuestionArchitecture -> SourcePlan -> SourceParse -> Synthesis -> TargetGate -> ReportViewModel -> CanonicalReportRenderer`

Do not start a new topic from copied reports. Renderers do not design questions or parse sources. Playbooks do not know presentation syntax or CSS classes.

## Canonical Research Workflow

### 1. Define the goal

Record research object, mode, cutoff/report date, investment decision, scope, and biggest uncertainty.

Historical backtest is the default unless the user explicitly asks for live/current research.

### 2. Build the internal question architecture

Use `investment-question-architect` and a domain playbook. Internal QA is adaptive to maximum depth five:

- L1: research direction.
- L2: mechanism bucket.
- L3: investment decision question.
- L4/L5: optional research units when L3 still mixes companies, mechanisms, metrics, or models.

Internal QA depth is preserved in `qa_tree.json`; it is not public Markdown by default.

### 3. Establish the BOM taxonomy

For industry/theme/S-curve work, define one canonical BOM registry. Each node explains:

- what it receives;
- what it produces;
- whom it supplies;
- representative companies;
- financial validation metrics.

The exact node ID and public name are reused by research artifacts, company exposure, target scoring, and report rendering.

Every canonical node must own a node-specific `BomNodePlaybook`. The playbook defines that node's boundary, master equations, and six question models. It may provide a short node-specific logic hint for reader orientation, but the hint is not an evidence whitelist, a mandatory search path, or a completion coordinate. New evidence may introduce themes that the initial playbook did not anticipate.

The project and node invariants are:

`one industry-chain project -> one boms/<node_id>/ child project per canonical BOM node`

`one canonical BOM node -> one six-question playbook -> one append-only temporal ledger -> reproducible as-of snapshots -> one independent BOM report`

Validate exact one-to-one coverage between the canonical BOM registry and the playbook registry. Missing, duplicate, extra, static-renderer, or generic-fallback playbooks are contract failures. Playbooks contain no source IDs, report dates, run facts, verdicts, or CSS; those belong to the research run, evidence artifacts, and renderer respectively.

### 4. Research six questions for every BOM node

Each `BOM node x question` is a minimum research unit:

1. `当前 BOM 的需求是否会被 S 曲线放大拉动？`
2. `供给能否跟上？`
3. `谁控制供给？`
4. `是否已经财务兑现？`
5. `市场是否已定价？`
6. `反证是什么？`

For each question:

1. Keep one concise professional model and basic logic hint so the reader understands the question.
2. Run both pull research from the six-question gaps and push ingestion from external filings, reports, news, opinions, and user databases.
3. Parse every document into atomic claims rather than one document-level summary.
4. Map every claim to `BOM x question x logic node x company/entity x time`, with optional metric, topic, stance, and target-period metadata.
5. Append claims without overwriting prior claims; preserve unmapped/new-theme material for review.
6. Build an as-of question snapshot only after source, contradiction, recency, and coverage review.

### 4A. Standalone BOM five-lens research

When the user explicitly narrows the research object to one BOM node rather than an
industry chain, use `report_scope: standalone-bom`. Interpret the five lenses as:

1. `需求侧`: demand growth, duration, customer adoption, and financial realization.
2. `供给侧`: capacity, yield, lead time, qualification, commitments, and concentration.
3. `技术侧`: route comparison, performance per watt, total cost, software ecosystem, and substitution.
4. `估值侧`: as-of price, earnings basis, priced-in growth, sell-side disagreement, and downside.
5. `ESG`: energy and water, export controls, geographic/customer concentration, governance, and capital-allocation externalities.

Each BOM owns a structured five-lens playbook. Every lens keeps one concise logic
paragraph and several stable `logic_nodes`. Each node defines its decision question,
support/refute rules, observable indicators, downstream nodes, company bridge
fields, and refresh cadence. The playbook is a judgment structure, not a source
whitelist.

Every source is still parsed into immutable atomic claims. Claims are then mapped
through a separate reviewed ledger to one primary logic node and optional secondary
nodes. A mapping records direction, evidence nature, directness, novelty,
materiality, expectation delta, one or more companies/entities, metric, rationale,
and downstream impact.
Never rewrite an atomic claim merely to reuse it in another lens.

For every as-of date, build append-only logic-node states and thesis revisions before
building a lens conclusion or investment decision. A state records support/refute
claims, source-backed evidence conditions, evidence gaps, and next validation. Do
not assign numeric or qualitative confidence scores. The first structured
snapshot is a `baseline`; it must not invent a change versus a nonexistent prior
snapshot. New themes that do not fit the playbook stay unmapped for review rather
than being discarded or forced into a node.

Every mapped `logic node x company/entity` coordinate also owns an append-only
entity state. It records the current evidence-backed assessment, real change versus
the previous entity snapshot, directional investment effect, gaps, and next
validation. The public report must never reuse a generic node paragraph as if it
were an entity-specific change.

Every public entity-material row must identify publication date, material class,
linked source, original page/section, and the exact entity-specific fact or view. A source
may appear under several lenses only when it is parsed separately for each lens.

This scope is a focused evidence report, not a shortcut around target gates. If the
user later asks for an `actionable_long` decision, the evidence must still satisfy the
canonical demand, supply/control, financial realization, valuation, and refutation
requirements.

### 4B. BOM project directory and shared provider archive

One BOM research object owns its research state, while the repository-level IMA
archive owns provider originals:

```text
source/ima/
  archive_manifest.jsonl
  archive_events.jsonl
  YYYY/MM/DD/<original-title>.pdf

research/bom/<bom_project_id>/
  project.json
  professional_report.html
  professional_report.md
  timeline_profile.json
  sources.jsonl
  source/
    ima/YYYY/MM/DD/<selected-original-title>.pdf
    manual/
  material_intake/
    documents.jsonl
    directory_candidates.jsonl
    directory_scan_events.jsonl
    scan_events.jsonl
    feed_state.json
  inbox/
    materials.jsonl
    parse_tasks.jsonl
  ledger/
    claims.jsonl
    conclusions.jsonl
    claim_mappings.jsonl
    logic_states.jsonl
    entity_states.jsonl
    thesis_revisions.jsonl
    investment_snapshots.jsonl
```

`source/ima/` at repository root is the canonical provider mirror for every IMA
original. It is private, ignored by Git, and organized by the verified IMA
`directory_date`; that path is archive provenance, never a claim about publication
date. Once a report passes BOM relevance review and its real publication date is
verified, copy an immutable research snapshot into that BOM project's
`source/ima/<published_at>/`. Project timelines and source links use this local
copy, so the BOM remains portable and never confuses archive date with publication
date. Ledgers and source indexes keep project-relative paths; local HTML and
Markdown use different link forms for their surfaces. HTML keeps project-relative
`source/...` links so a `file://` report opens the neighboring PDF correctly;
Markdown resolves the same ledger path to an absolute filesystem link. Manually
imported originals remain under `source/manual/`.
`material_intake/raw/` is forbidden. Question-specific work remains in
`inbox/parse_tasks.jsonl`.

### 5. Search and parse actively

GPT is the research director and chooses the source universe. For every minimum unit:

- resolve professional sources through the `SourceUniverseRepository` and `config/source_universes.json`;
- create direct/Exa-style searches for the exact question and metric;
- include a refuting or boundary-check source plan;
- enforce cutoff visibility before parsing in backtest mode;
- create one source extraction and one GPT review per `question x source` pair;
- treat messages and opinions as leads unless separately verified;
- parse long material with the appropriate specialty skill or DeepSeek adapter when available;
- preserve explicit gaps instead of filling them with model priors.

The same document may be parsed multiple times for different questions. Every parse must use that question's dimensions.

Every discovered document preserves two orthogonal classifications:

- `material_class`: `official_filing`, `official_company`, `sell_side_research`, `authoritative_third_party`, `market_news`, `expert_opinion`, or `other`;
- `ingestion_channel`: `question_search`, `knowledge_base_scan`, or `manual_import`.

`material_class` is more granular than the compatibility `source_bucket`. Official filings/company material map to `evidence`; sell-side and authoritative third-party material map to `research_report`; market news maps to `message`; expert opinion maps to `opinion`.

Every atomic claim preserves four time fields when available:

- `published_at`: when the market could know it;
- `effective_period`: which actual period the fact describes;
- `target_period`: which future period a forecast addresses;
- `ingested_at`: when the system received it.

For IMA and other knowledge bases, `directory_date`, provider `create_time`,
provider `update_time`, and `published_at` are different fields. Never infer
`published_at` from the archive folder, upload time, discovery time, or modified
time. Resolve it from an explicit provider publication field, a dated report title,
or preferably the original PDF cover/header, and persist
`publication_date_status`, `publication_date_source`, and the page/section locator.
If the real publication date is still unknown, keep `published_at` blank and limit
the document to `date_verification_only`; it cannot enter a public timeline or
historical evidence ledger.

An IMA search hit does not prove its year/month/day archive folder. Persist
`directory_mapping_status=pending_directory_reconciliation` until a dated scan or
explicit review supplies `directory_date` and `directory_path`. The central mirror
stores IMA originals under repository `source/ima/YYYY/MM/DD/` using the verified
IMA `directory_date`. This does not populate `published_at`. A selected report must
still resolve publication date from an explicit provider field, dated title, or
preferably the PDF cover/header before it can enter a public timeline or historical
evidence ledger.

The system uses one provider archive loop and two evidence loops:

1. `ima_daily_archive`: in an attended browser session, open the approved IMA
   year/month/day directory, enumerate every PDF across all pages or lazy-loaded
   rows, and click each visible download control without a BOM relevance filter.
   Import the completed browser downloads into repository
   `source/ima/<directory_date>/`.
2. `question_search`: pull research driven by one `BOM x question` coverage gap,
   using the professional universe plus Exa/AI search.
3. `knowledge_base_scan`: read the central IMA archive manifest, judge each report
   against enabled BOM profiles, verify selected originals, copy them into the
   matching BOM's `source/ima/<published_at>/`, and create local intake/inbox rows.

The archive loop preserves originals and audit metadata only; it does not create
evidence. Both evidence loops enter the BOM material-intake ledger first. A selected
document creates narrow `BOM x question x source` parse tasks; only
question-specific parsing and GPT review may promote atomic claims into the temporal
evidence ledger. A source that cannot yet be mapped remains in
`unmapped/new_theme`; it must not be silently discarded or forced into an unsuitable
question.

The central archive uses the user's visible, logged-in IMA session and must not call
IMA OpenAPI, hidden download URLs, `archive-ima-day`, or `archive-ima-daily`.
Credentials, cookies, tokens, and raw knowledge-base IDs are never read or persisted.
Historical projects quarantine knowledge-base material published after `as_of_date`;
daily feeds should normally target a live successor project rather than mutate a
frozen backtest.

For a daily IMA feed such as `环球研报直通车`, the executable sequence is:

`reuse logged-in IMA page -> open previous year/month/day folder -> enumerate every visible PDF across all pages -> click each visible download control -> import completed PDFs into source/ima/<directory_date> plus archive manifest -> downstream BOM relevance review -> verify selected PDF publication date -> copy selected original into BOM source/ima/<published_at> -> create one parse task per relevant research coordinate -> specialty/DeepSeek first-pass reading -> GPT review -> append atomic claims -> refresh the question timeline and current conclusion`

The material feed must support both canonical six-question BOM children and
`standalone-bom` five-lens projects. It derives the allowed question coordinates
from the project contract; it must never manufacture a six-question child path for
a standalone project. Repository `source/ima/` remains the complete provider
mirror; a BOM project stores only its selected, publication-date-verified copies.
Archive records live in `source/ima/archive_manifest.jsonl`; BOM-specific relevance
decisions remain auditable in each project's
`material_intake/directory_candidates.jsonl`. Short-lived IMA URLs, browser
credentials, cookies, tokens, and raw knowledge-base IDs are never read or persisted.
`config/ima_daily_archive.json` defines the provider mirror. Enabled BOM routing is
configured separately and never controls whether an IMA PDF is downloaded.
The attended daily run archives the previous IMA day and may revisit the configured
recent-day window idempotently. Existing verified originals are reused; only
missing rows are clicked again. UI, login, or download failures remain visible and
are never treated as completion.

### 6. Apply semantic completion gates

A BOM question is complete only when:

- the professional source universe and direct/AI-search plan are recorded;
- both question-driven search and available external-material ingestion have completed;
- selected documents have question-specific atomic parses;
- actual facts, forward expectations, source diversity, recency, and explicit gaps are recorded;
- supporting and conflicting claims remain distinguishable;
- Q6 additionally contains explicit refuting source IDs and refutation evidence.

A BOM S-curve stage may be asserted only after all six questions pass.

A target may be `actionable_long` only when all of the following pass:

- canonical `thesis_node_id` mapping;
- all six questions complete for that BOM;
- explicit refutation evidence verified;
- company financial exposure is explicitly verified by a structured company/segment bridge, not inferred from generic source IDs;
- as-of valuation/mispricing analysis verified;
- component-specific score evidence is traceable;
- quantitative kill tests include metric, threshold, cadence, and downgrade action.

Otherwise cap the target at `watch_only`; missing BOM mapping is `no_action`. Persist both `candidate_action_state` and final `action_state` with `research_gate` reasons.

Score gaps are first-class data. A gap row has `status=gap` and `gap_reason`; it must not borrow unrelated source IDs or receive a high inferred score.

### 7. Freeze, then label

Backtest recommendations are frozen before future-return labels are attached. Labels never alter source selection, prose, score, rank, or action state.

## Public Report Contract

The sole presentation contract is `skills/value_invest_research/frameworks/research_report_contract.md`.

Default industry/project top-level order is exactly:

1. `当前研究的问题`
2. `行业概况`
3. `标的推荐`
4. `来源索引`

Do not render public `下钻 QA`, source plans, raw search queries, parser traces, score worksheets, tool traces, or change logs unless the user explicitly asks for the workbench.

HTML is the default public reading artifact; Markdown is the portable audit
sidecar. Both are generated from the same view model and must contain the same
research claims. Industry/theme/S-curve output uses two report scopes. The parent
`professional_report.html` is an `industry-index` and links to each child HTML.
Each `boms/<node_id>/professional_report.html` is a `bom-node` report containing
exactly one node's six question modules and one S-curve rollup. Optional deepening
modules stay inside the relevant BOM child unless they are truly chain-wide.

An explicitly isolated BOM may instead use `report_scope: standalone-bom`. Its
public HTML contains one `当前投资判断` snapshot followed by five collapsible
top-level sections in this order: `需求侧`, `供给侧`, `技术侧`, `估值侧`, `ESG`.
Each section contains `简单逻辑链`, then full-width logic nodes. Every logic node
contains collapsible company/entity modules, followed by `最新结论与趋势`. It
does not inherit the four-section industry shell or the six-question BOM-child
layout.

The investment snapshot is generated only after logic-node states. It separates
`fundamental_delta`, `consensus_delta`, and `priced_in_delta`, shows company
exposure/earnings/valuation bridges, semantic gates, catalysts, and quantitative
kill tests. `actionable_long` is forbidden unless every required gate passes.

The parent owns chain taxonomy, navigation, and aggregated targets. Each child owns
its `project.json`, filtered `sources.jsonl`, `source/`, `material_intake/`,
`inbox/`, `ledger/`, optional `research_run.json`, report, node-specific refresh
cadence, and node-level targets. A child without a completed node-specific run must
state `partial_research`; it must not imply research completion.

Inside each public BOM question module, render one compact `基本理解思路`, followed by `当前结论`, `相较上一截面的变化`, `时间演化`, `映射材料`, and `信息覆盖`. Do not render mandatory per-stage evidence cards. Logic hints orient the reader; they never constrain which material may enter the ledger. Every mapped material keeps a source link, `material_class`, and `ingestion_channel` next to the supported claim. Past conclusions may be shown only when a real prior snapshot exists. Raw IMA IDs, credentials, internal search queries, and pending parse tasks never appear in public Markdown.

Structured standalone BOM evidence renders in this exact hierarchy:
`BOM x lens/question x logic node x company/entity`. Every company/entity is one
collapsed-by-default, full-width disclosure module. Before its evidence table,
render `截面变化与评估` plus the real change from its previous snapshot. The module
then renders one horizontally scrollable table with exactly
`材料（含链接） | 类型 | 观点列表`. One source occupies one row; publication date
appears inside the material cell, and every bullet preserves `观点 N / 原文位置 /
原子观点 / 支持或反证方向`. Do not repeat the same material in a lens-level
timeline. The Markdown audit sidecar mirrors the same entity hierarchy and
three-column tables. Local PDF links navigate in the current tab; only HTTP(S)
sources may use a new tab. Logic nodes and company impacts render as full-width
rows, not narrow side-by-side cards.

The target section must preserve the profit bridge, valuation evidence, payoff odds, final state, and downgrade triggers in one readable Markdown table. Action states remain `actionable_long`, `watch_only`, or `no_action`.

## Time-Slice Contract

In historical mode:

- only information visible on or before `as_of_date` may support research;
- model prior is hypothesis-only;
- every source preserves visibility proof;
- post-cutoff material is rejected, quarantined, or label-only;
- public prose reads as if written on the cutoff date;
- current-time price data appears only in final-target evaluation labels.

## Persistent Framework Changes

Framework changes are persistent unless the user says they are one-off. Update together:

- `AGENTS.md`
- `skills/value_invest_research/SKILL.md`
- `skills/value_invest_research/frameworks/research_goal_qa.md`
- `skills/value_invest_research/frameworks/research_report_contract.md` for presentation changes
- relevant domain playbooks for domain-specific question/metric changes
- executable validators and regression tests

## Required Validation

Before calling a framework change complete:

1. Run focused unit tests plus the full research-framework suite.
2. Run `validate-report-contract` on a regenerated report.
3. Run `validate-material-intake` when search or knowledge-base intake artifacts exist.
4. Run `validate-ima-archive` after an IMA daily archive run.
5. Run `validate-research-artifacts --require-l3` when artifacts exist.
6. Run a Markdown/static smoke check for the selected report scope: four-section order and parent-child links for industry reports, or five-lens order plus reverse-chronological entity-material tables for `standalone-bom`; always verify readable tables, source links, no public process text, and no `actionable_long` target with a failed research gate.
7. Run `git diff --check`.
