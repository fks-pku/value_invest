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

`ResearchGoal -> DomainPlaybook -> QuestionArchitecture -> ResearchPlan -> PlanStepExecution -> SourceParse -> StepAnswer -> Synthesis -> TargetGate -> ReportViewModel -> CanonicalReportRenderer`

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
- L4: child questions created only after L3 research exposes a concrete evidence gap.
- L5: optional further child questions created only after an L4 answerability gate fails.

The initial QA and plan stop at L3. Every L3 is initially a terminal, executable
question and states the data to collect and the analysis to perform. Search,
parsing, review, and answer synthesis start there. If the current question passes
its evidence and answerability gate, stop that branch. If it fails, record the
specific gap or contradiction and create only the smallest required questions at
the next level. Add one level per failed gate and never exceed L5. Do not
pre-generate a complete L4/L5 tree.

Internal QA depth is preserved in `qa_tree.json`; it is not public Markdown by default.

After the QA tree is fixed, persist an executable `research_plan.json`. The parent
plan treats every L3 as a rollup and points to one independent versioned plan under
`l3_research_plans/<l3_node_id>/research_plan.json`. Each L3 plan starts with its
L3 root as the only executable terminal question. A failed answerability gate may
create L4, and a failed L4 gate may create L5. Every current terminal question
becomes one stable step with a
`research_step_id`, dependency, question-specific source plan, freshness rule, minimum
evidence gate, refuting source plan, specialty parser, answer contract, and
traceability contract. Persist parent and L3 plan revisions immutably in their
respective `research_plan_history/<plan_id>.json` directories.

Once expanded, a parent stops owning new searches and rolls up its children.
Material collection always originates from the current deepest unanswered
question, which may be L3, L4, or L5. Every evidence-eligible parse task must carry
`l3_plan_id`, `l3_node_id`, `question_node_id`, `question_level`,
`research_step_id`, and `search_run_id`. A broad material pool, provider archive, or
knowledge-base scan may preserve candidates, but cannot create completion evidence
by bulk-mapping those candidates to questions. Reusing one source across questions
requires a separate attachment, extraction, and GPT review for each question.

Step execution is append-only in `research_step_events.jsonl`. Collection, source
attachment, answer recording, gate evaluation, blocking, and reopening are events;
do not overwrite history with a mutable status field. Project the current state
from the ledger. A step is complete only when it has a non-empty answer, source IDs,
question-specific extraction IDs, GPT review IDs, support/refute findings, a recorded
refutation-search result, a passed evidence gate, and completed dependencies.
Missing evidence records a blocked step with gaps and next actions; it is never
silently upgraded to completion.

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

Standalone BOM research is logic-chain-centered, not table-centered. The playbook
declares `research_model: logic_chain_centered` and a versioned
`logic_chain_version`. Its causal nodes form the first-principles chain that explains
how heterogeneous facts can change BOM commercial scale and investment value.
Atomic claims keep only the minimum audit envelope needed to preserve source,
locator, market-known time, evidence nature, and any reliably stated business
period. Do not require every claim to fit one universal metric table.

Every reviewed claim-to-node mapping records how the claim changes the chain:
`support`, `refute`, `boundary`, `constraint`, `new_branch`, `conflict`,
`unresolved`, `neutral`, or `unmapped`. `support` and `refute` are reserved for
claims that directly fit the node and explicitly satisfy its support or refute
rule. Topic relevance, forecasts, proxies, and contextual inputs use the other
effects; they never become support merely because they concern the same BOM.
`unmapped` is a reviewed decision that the proposed claim-to-node relationship
does not hold; the rejected node remains only as an audit coordinate and is not
rendered or counted in node state. The original claim remains immutable.
One primary node avoids duplicate interpretation; optional secondary nodes and
downstream impacts preserve real multi-node effects. New mechanisms that do not fit
the current chain remain visible for chain revision instead of being forced into a
convenient node.

When the demand lens begins with Q1 `需求方`, keep that node strictly about who
demands the BOM. Render two mutually exclusive lists: `当前需求方` and
`潜在未来需求方`. Do not mix business scenarios, workloads/tasks, host systems,
component specifications, procurement channels, quantities, or as-of change
assessment into Q1. Q2 owns the current quantity baseline; later demand nodes own
workload, intensity, budget, orders, and financial realization.

Q1 and Q2 are `presentation_role: derived_view`, not the demand research backbone.
The public demand lens must retain every causal node from workload through compute
intensity, budget, orders, and financial realization. Q1/Q2 may appear afterwards
as collapsed supporting views. A quantity matrix never substitutes for the
first-principles causal chain or directly generates the lens conclusion.

Q2 must inherit the exact Q1 taxonomy and separate its public quantity work into
three groups in this order: `当前需求方`, `潜在未来需求方`, and `其它分类`.
The first two groups reuse their respective Q1 demander lists; each specific
demander may own multiple quantities, forecasts, samples, or value proxies with
mapping quality and caveats. Potential-future observations remain separate from
the current quantity baseline. `其它分类` contains market totals or forecasts that
cannot be allocated reliably and groups them by their own information category.
Imperfect material stays visible, but must never be forced into a Q1 category or
summed across incompatible units, periods, samples, or overlapping demanders.

Every source is still parsed into immutable atomic claims. Claims are then mapped
through a separate reviewed ledger to one primary logic node and optional secondary
nodes. A mapping records effect direction, evidence nature, directness, novelty,
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
  research_plan.json
  research_plan_history/<plan_id>.json
  research_step_events.jsonl
  l3_research_plans/
    index.json
    <l3_node_id>/
      research_plan.json
      research_plan_history/<plan_id>.json
      research_step_events.jsonl
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
- start every pull search from the current active terminal question and persist its
  full question/search trace; L3 search is valid before any gap-triggered expansion,
  but results may never be fanned out across later children;
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
2. `question_search`: pull research driven by one unfinished
   `BOM x L3 plan x current terminal question` gap, using the professional universe
   plus Exa/AI search and preserving the question/search-run trace.
3. `knowledge_base_scan`: read the central IMA archive manifest, judge each report
   against enabled BOM profiles, verify selected originals, copy them into the
   matching BOM's `source/ima/<published_at>/`, and create local intake/inbox rows.

The archive loop preserves originals and audit metadata only; it does not create
evidence. Both loops enter the BOM material-intake ledger first. Knowledge-base
routing creates candidates only. A specific active-question search or selection creates narrow
`BOM x L3 plan x active question x level x search-run x source` parse tasks; only question-specific parsing
and GPT review may promote atomic claims into the temporal evidence ledger. A source that cannot yet be mapped remains in
`unmapped/new_theme`; it must not be silently discarded or forced into an unsuitable
question.

The central archive uses the user's visible, logged-in IMA session and must not call
IMA OpenAPI, hidden download URLs, `archive-ima-day`, or `archive-ima-daily`.
Credentials, cookies, tokens, and raw knowledge-base IDs are never read or persisted.
Historical projects quarantine knowledge-base material published after `as_of_date`;
daily feeds should normally target a live successor project rather than mutate a
frozen backtest.

For a daily IMA feed such as `环球研报直通车`, the executable sequence is:

`reuse logged-in IMA page -> open previous year/month/day folder -> enumerate every visible PDF across all pages -> click each visible download control -> import completed PDFs into source/ima/<directory_date> plus archive manifest -> downstream BOM relevance review -> candidate intake -> select the current terminal question -> verify selected PDF publication date -> copy selected original into BOM source/ima/<published_at> -> create one question-specific parse task -> specialty/DeepSeek first-pass reading -> GPT review -> append atomic claims -> answerability gate -> stop or expand one level`

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
- its linked research-plan step passes the step evidence gate and retains source,
  extraction, review, answer, refutation-search, and dependency traceability.
- its current terminal L3 step passes, or every mandatory descendant created by a
  failed answerability gate passes; direct evidence events on the parent project
  rollup never complete it.

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

When the user explicitly asks for a research-plan document, generate a separate
`research_plan.md` beside the professional report. It is the human-readable
question hierarchy, not a substitute for `professional_report.html`. It starts
with L1/L2/L3 only. It must show every L3 and any child questions actually created
by failed answerability gates, up to L5; each current terminal question shows the
required data and analysis. Keep the Markdown concise:
source plans, dependencies, detailed evidence gates, and event-derived status remain
in the structured plan and append-only ledgers instead of being repeated under every
question. Display wording may remove boilerplate without changing canonical question
IDs. Regenerate it whenever a plan is built, expanded, or the standalone report is
refreshed. Do not generate `research_plan.html`.

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
Each section renders `第一性原理逻辑链`, then `逻辑节点与原子观点材料`, optional
`派生证据视图`. Do not render a separate lens-level `全局结论与趋势`; global
synthesis belongs only in the leading `当前投资判断`, while node conclusions stay
beside their evidence. Causal nodes are full-width,
collapsed-by-default disclosures. Their visible summary shows the exact research
question, current node state, conclusion, and real change. Their body contains exactly one horizontally scrollable
table with `发布日期 | 报告名称 | 材料类型 | 原子观点 | 对逻辑点的影响`. Rows use
`published_at` and run newest to oldest; one source occupies one row. The report
name is a blue source link. Atomic claims are numbered `1, 2, 3...`, and the final
cell keeps a parallel numbered list using `增强`, `减弱`, `边界`, `约束`, `线索`,
`待判断`, `新分支`, `冲突`, or another explicit active mapping effect. Original
locator, effective period, and target period stay compact
labels inside the atomic-claim cell. Local sources navigate in the current tab;
only HTTP(S) sources open a new tab. Do not render separate public state-history,
event-history, filter, or company/entity audit modules. The append-only state,
revision, mapping, and entity ledgers remain the internal audit source. The report
does not inherit the four-section industry shell or the six-question BOM-child layout.

When the user explicitly narrows one lens's public modules, the playbook may set
`public_logic_node_ids` for that lens. In a logic-chain-centered profile, this list
must retain every causal node in canonical order; it may omit only derived views.
All omitted derived-view modules, mappings, states, and claims remain in the
internal append-only research structure. A public Q2 demand quantity matrix must
keep its Q1 demand-party classification view visible with it.

The investment snapshot is generated only after logic-node states. It separates
`fundamental_delta`, `consensus_delta`, and `priced_in_delta`, shows company
exposure/earnings/valuation bridges, semantic gates, catalysts, and quantitative
kill tests. In logic-chain-centered reports, `当前投资判断` leads with a rollup of
the strengthened nodes, main breakpoints, and failed gates; source-batch or Q2
changes appear separately as `本期证据变化`. `actionable_long` is forbidden unless
every required gate passes.

The parent owns chain taxonomy, navigation, and aggregated targets. Each child owns
its `project.json`, filtered `sources.jsonl`, `source/`, `material_intake/`,
`inbox/`, `ledger/`, optional `research_run.json`, report, node-specific refresh
cadence, and node-level targets. A child without a completed node-specific run must
state `partial_research`; it must not imply research completion.

Inside each public BOM question module, render one compact `基本理解思路`, followed by `当前结论`, `相较上一截面的变化`, `时间演化`, `映射材料`, and `信息覆盖`. The exact L3 research question remains visible, but the question hierarchy belongs only in `research_plan.md`; do not duplicate the plan inside `professional_report.html` or `professional_report.md`. Do not expose raw queries or parser traces. Logic hints orient the reader; they never constrain which material may enter the ledger. Every mapped material keeps a source link, `material_class`, and `ingestion_channel` next to the supported claim. Past conclusions may be shown only when a real prior snapshot exists. Raw IMA IDs, credentials, internal search queries, and pending parse tasks never appear in public Markdown.

Structured standalone BOM evidence renders publicly in this exact hierarchy:
`BOM x lens x causal logic node x source row x numbered atomic claim`. Every
causal node owns the same five-column table:
`发布日期 | 报告名称 | 材料类型 | 原子观点 | 对逻辑点的影响`. The Markdown audit
sidecar mirrors that table. The internal parallel coordinates remain
`logic node x as_of_date` and
`logic node x company/entity x as_of_date`; they preserve real snapshots,
mapping rationale, downstream impact, gaps, and next validation without expanding
the public page. Logic nodes and company impacts render as full-width rows, not
narrow side-by-side cards.

The Q1 `需求方` derived view is the sole presentation exception. When its playbook uses
`render_mode: demand_party_list`, render only two compact groups—`当前需求方` and
`潜在未来需求方`—and omit node state, conclusion, change assessment, evidence
counts, company/entity disclosures, and material tables from that Q1 block. The
L3 research question remains visible in the heading. The underlying evidence ledgers
remain append-only and available to downstream nodes.

When the Q2 derived view uses `render_mode: demand_quantity_matrix`, render exactly three outer
groups in this order: `当前需求方`, `潜在未来需求方`, and `其它分类`. HTML renders
each outer group as a collapsed disclosure and every specific demander or other
information category as a second collapsed disclosure inside it. Markdown mirrors
the same numbered hierarchy. Its L3 research question remains visible above the
matrix. Every current Q1 demander owns one separate table and
may contain multiple information rows; use an explicit `数据缺口` row when no
quantity is available. Every potential-future Q1 demander also owns a table and may
show an empty state without entering the current baseline. `其它分类` groups
unallocatable rows by their own information category. Every table uses exactly
`来源 | 期间 | 信息类型 | 具体信息`. `信息类型` classifies source material as
`官方财报`, `第三方研究`, `市场消息`, or `机构研报`; `具体信息` keeps the metric,
quantity or forecast, mapping quality, and principal limitation together. Other
forecasts must not claim a Q1 demander mapping.

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
6. Run a Markdown/static smoke check for the selected report scope: four-section order and parent-child links for industry reports, or five-lens order plus one newest-to-oldest five-column atomic-claim material table per causal node for `standalone-bom`; always verify readable tables, source links, parallel claim/effect numbering, no separate lens-level `全局结论与趋势`, no retired dual-history UI, no public process text, and no `actionable_long` target with a failed research gate.
7. Verify causal `support`/`refute` mappings have direct node fit and explicitly
   match the node support/refute rule; proxies, context, and rejected relations use
   another effect including `unmapped`.
8. Run `git diff --check`.
9. Run `validate-research-plan` whenever `research_plan.json` exists and verify that
   no completed step is missing source, extraction, GPT review, answer, refutation,
   search-run, or dependency evidence; verify every expansion has a recorded failed
   answerability gate and concrete gap; also verify exact one-to-one L3 child-plan
   coverage and that parent L3 rollups are not completed by direct evidence events.
