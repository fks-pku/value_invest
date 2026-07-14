# Research Goal QA Framework

This is the only active internal research framework. Public presentation is governed by `research_report_contract.md`.

## Purpose

Turn a user goal into an auditable decision chain:

`ResearchGoal -> DomainPlaybook -> QuestionArchitecture -> SourcePlan -> Per-Source Parse -> Evidence Synthesis -> Target Gate`

The framework is universal; concrete questions, metrics, sources, and thresholds adapt by domain.

## 1. Define the Research Goal

Record:

- topic and investment decision;
- research type: industry/theme, company, event/policy, technology/product route, target update, or custom;
- historical backtest or live mode;
- cutoff/report date and security universe;
- scope, exclusions, and current uncertainty.

Default to historical backtest unless the user explicitly asks for live/current research.

## 2. Select a Domain Playbook

Use the playbook to own:

- professional L2 mechanism buckets;
- L3 decision questions;
- metric families and threshold rules;
- source universe aliases;
- specialty parser routing;
- update triggers and kill tests.

Do not put domain-specific questions into the public presentation contract.

## 3. Build Adaptive Internal QA

Maximum depth is five:

- L1: adapted research direction.
- L2: one coherent mechanism bucket.
- L3: one investment decision question.
- L4/L5: optional minimum units when L3 still mixes mechanisms, companies, routes, metrics, or models.

Every L3-L5 unit records:

- `decision_use`
- `materiality`
- `support_evidence`
- `refute_evidence`
- `target_implications`
- `score_component`
- `minimum_evidence_gate`
- `source_plan`
- `refuting_source_plan`
- `skill_dispatch`
- `fact`, `inference`, `judgment`, `gap`, `trigger`, `source_links`

Stop drilling down when one source plan and one extraction schema can answer the unit clearly.

## 4. S-Curve and BOM Adaptation

For industry/theme S-curve research, first establish one canonical BOM taxonomy. Each node has a stable ID, public name, input, output, downstream recipient, representative companies, and financial metrics.

### 4.1 Per-Node Playbook Contract

Before source planning, every canonical BOM node must resolve to exactly one node-specific `BomNodePlaybook`. Exact node-ID coverage is required: no canonical node may be missing, duplicated, or silently handled by a generic fallback.

The invariant is:

`canonical node -> node-specific playbook -> cutoff-frozen research run -> report module`

Each node playbook owns only stable domain logic:

- scope and explicit exclusions;
- inputs, product/output, downstream recipients, representative companies, and financial validation metrics;
- node-specific master equations or causal formulas for demand, market value, effective supply, and investment odds;
- exactly six question definitions;
- 4-7 causal stages per question;
- one primary metric, one or two cross-check metrics, and one refutation metric per stage;
- question-level formula, purpose, conclusion rule, and failure condition.

The playbook must not contain source IDs, cutoff dates, observations, verdicts, gaps, target states, or HTML classes. Those belong respectively to the research run, evidence artifacts, target gate, and renderer.

The shared six question labels do not imply shared causal stages. For example, HBM effective supply is a wafer/yield/stacking/packaging/qualification funnel, while power/cooling effective supply is an equipment/lead-time/site/grid/commissioning funnel. Reusing generic stages across unlike nodes is a contract failure.

Each cutoff-frozen node research run must match the playbook's question and stage IDs exactly and store stage-level actual history, forward expectations, first-principles assessment, source IDs, explicit gaps, and search/parse status.

Each BOM node receives six internal/public research questions:

1. Is demand amplified by the S-curve, including unit/system elasticity?
2. Can effective supply keep up?
3. Who controls supply and why?
4. Has the thesis reached revenue, margin, backlog/orders, or cash flow?
5. Is the growth path already priced?
6. What observed evidence can refute the thesis?

Each question uses a question-specific model:

| Question | Model |
|---|---|
| Demand | S-curve transmission and elasticity |
| Supply | capacity, yield, cycle, qualification |
| Controller | share, barriers, substitution, customer lock-in |
| Financial realization | revenue, margin, backlog, cash flow |
| Pricing | valuation, priced-in expectations, earnings revisions |
| Refutation | trigger, threshold, cadence, downgrade action |

## 5. Minimum Research Unit Execution

For every minimum question:

### A. Judgment model

Define object, formula/causal frame, evidence handles, conclusion rule, and failure condition.

### B. Logic chain

Write concrete links for the current BOM only. Do not put metric values into the chain.

The model and logic chain remain separate internal inputs: the model owns the formula and pass/fail rule, while the chain owns the node-specific causal stages. The public report renderer must compile both into one `研究逻辑链` card. It must not expose two adjacent cards named `判断模型` and `具体逻辑链条`.

### C. Per-link metric planning

Before search, choose heterogeneous candidates appropriate to that link: direct demand, usage intensity, workflow complexity, enterprise adoption, budget/order, BOM pull-through, supply/price, financial realization, valuation, or refutation.

Choose concrete fields, not baskets. Example: `Microsoft commercial RPO ($B)` is valid; `cloud budget proxy` is not.

### D. Active search

For each selected metric:

1. Resolve professional Universe sources from `config/source_universes.json` through `SourceUniverseRepository`.
2. Add official company/customer filings and justified specialist sources.
3. Create a direct/Exa query for the exact question, logic link, metric, and cutoff.
4. Search for at least one boundary/refuting source.
5. Record selected source IDs or an explicit gap reason.

One broad query cannot stand in for per-metric research.

### E. Per-source parsing

Create one extraction per `question x source`. Parse the source against the current question's dimensions, even if the same document was parsed elsewhere.

Use:

- `financial-statement-analysis`
- `valuation-analysis`
- `industry-report-analysis`
- `news-event-analysis`
- `opinion-analysis`
- `company-exposure-analysis`
- `leaf-research-deepseek` for long selected materials when available

Create one GPT verification record per extraction. Messages/opinions remain leads unless primary evidence verifies them.

### F. Evidence synthesis

For every logic link, keep together:

- actual metric history/current observations;
- explicit forward expectations;
- first-principles support and break mechanisms;
- source-backed conclusion and confidence.

Actual history never includes guidance or forecasts. Claiming acceleration requires same-definition history or explicit YoY/multiple evidence. Claiming runway requires a cutoff-visible forward anchor and mechanism.

## 6. Semantic Completion

A BOM question is complete only when `source_universe_plan`, direct/Exa search plan, and `metric_candidate_plan` are non-empty and search, per-source parsing, source IDs, and evidence summary are complete. Q6 additionally requires explicit `refuting_source_ids` and `refutation_evidence_summary`.

All six questions must pass before a BOM S-curve stage becomes a formal conclusion.

Missing data is not completion. Persist `gap`, scope caveat, and next evidence needed.

## 7. Company Exposure and Target Selection

Map each security to exactly one primary canonical `thesis_node_id`; secondary exposure may be recorded separately.

Before scoring, verify:

- segment/revenue exposure;
- margin and cash-flow bridge;
- customers/orders/backlog where relevant;
- capex and working-capital burden;
- as-of valuation and priced-in expectations;
- observed refutation evidence.

Score four public dimensions:

- `scarcity_or_monopoly`
- `mispricing`
- `earnings_elasticity`
- `risk_control`

Preserve component-specific `score_subcomponents`. A verified row has evidence/review IDs, `evidence_role`, and rationale. A missing row has `status=gap` and `gap_reason`; it cannot borrow a general source pool.

`actionable_long` requires:

- canonical BOM mapping;
- six questions complete;
- explicit refutation evidence;
- company exposure explicitly verified through a company/segment financial bridge rather than inferred from generic source IDs;
- valuation/mispricing verified;
- quantitative kill tests with metric, threshold, cadence, and downgrade action.

Otherwise the final state is `watch_only`; missing mapping is `no_action`. Preserve candidate and final states plus `research_gate` reasons.

## 8. Backtest Discipline

In historical mode:

- only sources visible by `as_of_date` support reasoning;
- availability proof is required;
- model prior is hypothesis-only;
- post-cutoff sources are quarantine or label-only;
- recommendations freeze before labels;
- labels do not change the research artifacts.

## 9. Public Rendering

Assemble through:

`ResearchProjectRepository -> ReportViewModel -> CanonicalReportRenderer`

Default public order:

1. `当前研究的问题`
2. `行业概况`
3. `标的推荐`
4. `来源索引`

Do not render internal `下钻 QA`, source plans, parser traces, or execution logs unless explicitly requested.

## 10. Validation

Before publication:

- validate QA and per-source parser/review schemas;
- validate BOM semantic readiness and target research gates;
- validate cutoff visibility and label isolation;
- validate the four-section HTML contract and DOM interaction;
- verify no failed-gate target is `actionable_long`.
