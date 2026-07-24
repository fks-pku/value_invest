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
- `src/value_invest_research/adapters/`: file system, Exa/search, LLM/DeepSeek, market data, CLI, Markdown, and compatibility HTML implementations.
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
4. Map every claim to `BOM x question x time`, with optional entity, metric, topic, stance, and target-period metadata.
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

For each lens, preserve one concise logic paragraph, one newest-to-oldest evidence
timeline, and one current conclusion/trend synthesized only from that timeline.
Every timeline row must identify publication date, material class, linked source,
original page/section, and the exact lens-specific fact or view. A source may appear
under several lenses only when it is parsed separately for each lens.

This scope is a focused evidence report, not a shortcut around target gates. If the
user later asks for an `actionable_long` decision, the evidence must still satisfy the
canonical demand, supply/control, financial realization, valuation, and refutation
requirements.

### 4B. Self-contained BOM project directory

One BOM research object owns one self-contained project directory:

```text
research/bom/<bom_project_id>/
  project.json
  professional_report.md
  timeline_profile.json
  sources.jsonl
  source/
    ima/YYYY/MM/DD/<original-title>.pdf
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
```

`source/` owns canonical originals. `material_intake/` owns metadata and audit
ledgers only; `material_intake/raw/` is a forbidden canonical location. All local
links in reports, claims, source indexes, and parse tasks are relative to the BOM
project directory. An industry-chain parent follows the same rule for every
`boms/<node_id>/` child and must not own a child's original materials.
Question-specific work remains in `inbox/parse_tasks.jsonl`.

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
explicit review supplies `directory_date` and `directory_path`. Archive provenance
never controls local storage. Store originals under `source/ima/YYYY/MM/DD/` using
`published_at`; if publication date is unresolved, use
`source/ima/unmapped/<source_id>/`. A later PDF-cover verification may move the
same file to its true publication-date directory without changing
`directory_date`.

The system uses two evidence loops:

1. `question_search`: pull research driven by one `BOM x six-question` coverage gap, using the professional universe plus Exa/AI search.
2. `knowledge_base_scan`: push research that walks the user's approved
   year/month/day report directories, audits every PDF against each canonical BOM
   profile, downloads only approved matches, and routes them to the matching BOM
   inbox.

Both loops enter the same material-intake ledger first. A newly discovered document is not evidence yet. It creates narrow `BOM x question x source` parse tasks; only question-specific parsing and GPT review may promote its atomic claims into the temporal evidence ledger. A source that cannot yet be mapped remains in `unmapped/new_theme`; it must not be silently discarded or forced into an unsuitable question.

IMA credentials and knowledge-base IDs stay outside Git. Use `IMA_OPENAPI_CLIENTID`, `IMA_OPENAPI_APIKEY`, and `IMA_KNOWLEDGE_BASE_ID`; persisted feed state may contain only an irreversible knowledge-base reference hash. Historical projects quarantine knowledge-base material published after `as_of_date`; daily feeds should normally target a live successor project rather than mutate a frozen backtest.

For a daily IMA feed such as `环球研报直通车`, the executable sequence is:

`resolve knowledge base by name -> walk year/month/day folders -> audit every PDF against each enabled BOM profile -> download approved matches -> verify PDF publication date -> archive under source/ima/<published_at> -> create one parse task per relevant research coordinate -> specialty/DeepSeek first-pass reading -> GPT review -> append atomic claims -> refresh the question timeline and current conclusion`

The material feed must support both canonical six-question BOM children and
`standalone-bom` five-lens projects. It derives the allowed question coordinates
from the project contract; it must never manufacture a six-question child path for
a standalone project. Original files live under the live project's private
`source/ima/<published_at>/` directory. All directory candidates and relevance decisions
remain auditable in `material_intake/directory_candidates.jsonl`, while short-lived
signed IMA URLs, API credentials, and raw knowledge-base IDs are never persisted.
`config/active_research_feeds.json` is the registry of live projects scanned each day.

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

Industry/theme/S-curve output uses two report scopes. Markdown is canonical and HTML is compatibility-only. The parent `professional_report.md` is an `industry-index`: `行业概况` renders `01 技术链与BOM呈现` and `02 BOM 独立研究目录`, with one relative link to each child. It must not embed the six-question modules. Each `boms/<node_id>/professional_report.md` is a `bom-node` report containing exactly one node's six question modules and one S-curve rollup. Optional deepening modules such as industry space, competition/profit pool, and chokepoints stay inside the relevant BOM child unless they are truly chain-wide.

An explicitly isolated BOM may instead use `report_scope: standalone-bom`. Its public
Markdown contains exactly five numbered H2 sections in this order: `需求侧`, `供给侧`,
`技术侧`, `估值侧`, `ESG`. Each section contains exactly `简单逻辑链`, `信息时间线`,
and `最新结论与趋势`. It does not inherit the four-section industry shell or the
six-question BOM-child layout.

The parent owns chain taxonomy, navigation, and aggregated targets. Each child owns
its `project.json`, filtered `sources.jsonl`, `source/`, `material_intake/`,
`inbox/`, `ledger/`, optional `research_run.json`, report, node-specific refresh
cadence, and node-level targets. A child without a completed node-specific run must
state `partial_research`; it must not imply research completion.

Inside each public BOM question module, render one compact `基本理解思路`, followed by `当前结论`, `相较上一截面的变化`, `时间演化`, `映射材料`, and `信息覆盖`. Do not render mandatory per-stage evidence cards. Logic hints orient the reader; they never constrain which material may enter the ledger. Every mapped material keeps a source link, `material_class`, and `ingestion_channel` next to the supported claim. Past conclusions may be shown only when a real prior snapshot exists. Raw IMA IDs, credentials, internal search queries, and pending parse tasks never appear in public Markdown.

Standalone BOM timelines use exactly `时间 | 信息类型 | Source | 观点列表`.
Render one source per row and group its question-specific atomic claims as a list
with original page or section locators.

Use plain Markdown headings, paragraphs, lists, and tables. Source links sit next to supported claims. The report must remain readable without CSS, JavaScript, HTML cards, or hidden content.

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
4. Run `validate-research-artifacts --require-l3` when artifacts exist.
5. Run a Markdown/static smoke check for the selected report scope: four-section order and parent-child links for industry reports, or five-lens order and reverse-chronological timelines for `standalone-bom`; always verify readable tables, source links, no public process text, and no `actionable_long` target with a failed research gate.
6. Run `git diff --check`.
