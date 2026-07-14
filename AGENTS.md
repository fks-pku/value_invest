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

Every canonical node must own a node-specific `BomNodePlaybook` before source search begins. The playbook defines that node's boundary, master equations, six question models, and 4-7 causal stages per question. Every stage defines one primary metric, one or two cross-check metrics, and one refutation metric. Shared question labels do not permit shared generic causal chains: compute, manufacturing, HBM, networking, power/cooling, and system delivery each require node-specific mechanisms and metrics.

The invariant is:

`one canonical BOM node -> one node-specific playbook -> one cutoff-frozen research run -> one report module`

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

1. Define the professional judgment model.
2. Write the concrete causal chain without data.
3. For each chain link, design heterogeneous metric candidates before searching.
4. Search each selected metric independently.
5. Show actual history, forward expectations, and first-principles assessment for the same link.
6. Write the question conclusion and target impact only after evidence/gap review.

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

### 6. Apply semantic completion gates

A BOM question is complete only when:

- `source_universe_plan`, direct/Exa search plan, and `metric_candidate_plan` are non-empty;
- question-level search completed;
- parsing completed;
- selected source IDs and evidence summary exist;
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

`行业概况` renders `01 技术链与BOM呈现`, then one numbered BOM module from `02` onward. Each BOM module contains the six question cards and one S-curve rollup. Optional deepening modules such as industry space, competition/profit pool, and chokepoints are rendered only when explicitly requested or required by a playbook.

Inside each public BOM question card, render one combined `01 研究逻辑链` card. It compiles the internal judgment model, formula, conclusion rule, and node-specific causal stages into one readable chain. Do not render separate public `判断模型` and `具体逻辑链条` cards. The internal playbook must still preserve those fields separately so research rules remain testable and presentation remains replaceable. Evidence cards for the exact causal stages begin at `02`, followed by the question conclusion and target impact.

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
