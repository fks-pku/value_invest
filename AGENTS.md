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
- `src/value_invest_research/adapters/`: file system, Exa/search, LLM/DeepSeek, market data, CLI, and HTML implementations.
- `config/source_universes.json`: professional source universe registry.
- `skills/value_invest_research/`: canonical workflow and presentation contracts.

New topics enter through:

`ResearchGoal -> DomainPlaybook -> QuestionArchitecture -> SourcePlan -> SourceParse -> Synthesis -> TargetGate -> ReportViewModel -> CanonicalReportRenderer`

Do not start a new topic from copied HTML. Renderers do not design questions or parse sources. Playbooks do not know CSS classes.

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

Internal QA depth is preserved in `qa_tree.json`; it is not public HTML by default.

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

Every atomic claim preserves four time fields when available:

- `published_at`: when the market could know it;
- `effective_period`: which actual period the fact describes;
- `target_period`: which future period a forecast addresses;
- `ingested_at`: when the system received it.

The system uses two evidence loops. Pull research is driven by six-question coverage gaps. Push research continuously ingests the user's external report database and other approved feeds. Both loops write to the same append-only ledger. A source that cannot yet be mapped remains in `unmapped/new_theme`; it must not be silently discarded or forced into an unsuitable question.

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

Default top-level order is exactly:

1. `当前研究的问题`
2. `行业概况`
3. `标的推荐`
4. `来源索引`

Do not render public `下钻 QA`, source plans, raw search queries, parser traces, score worksheets, tool traces, or change logs unless the user explicitly asks for the workbench.

Industry/theme/S-curve output uses two report scopes. The parent `professional_report.html` is an `industry-index`: `行业概况` renders `01 技术链与BOM呈现` and `02 BOM 独立研究目录`, with one `bom-index-card` linking to each child. It must not embed the six-question modules. Each `boms/<node_id>/professional_report.html` is a `bom-node` report containing exactly one node's six question cards and one S-curve rollup. Optional deepening modules such as industry space, competition/profit pool, and chokepoints stay inside the relevant BOM child unless they are truly chain-wide.

The parent owns chain taxonomy, navigation, and aggregated targets. Each child owns its `project.json`, filtered `sources.jsonl`, optional `research_run.json`, report, node-specific refresh cadence, and node-level targets. A child without a completed node-specific run must state `partial_research`; it must not imply research completion.

Inside each public BOM question card, render one compact `基本理解思路`, followed by `当前结论`, `相较上一截面的变化`, `时间演化`, `映射材料`, and `信息覆盖`. Do not render mandatory per-stage evidence cards. Logic hints orient the reader; they never constrain which material may enter the ledger. Every mapped material keeps a source link next to the supported claim, and past conclusions may be shown only when a real prior snapshot exists.

Nested structures are collapsed `details` cards. Wide tables use `table-scroll`. Source links sit next to supported claims. The source index is collapsed.

The target section must include `target-profit-bridge`, `target-valuation-table`, `target-odds-model`, `target-odds-table`, and `target-table`. Action states keep `state-actionable_long`, `state-watch_only`, or `state-no_action` classes.

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
3. Run `validate-research-artifacts --require-l3` when artifacts exist.
4. Run a DOM/static smoke check for four-section order, collapsed cards, table overflow, action-state colors, no public process text, and no `actionable_long` target with a failed research gate.
5. Run `git diff --check`.
