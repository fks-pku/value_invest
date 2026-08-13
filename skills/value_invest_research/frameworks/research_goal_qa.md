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

The invariants are:

`industry-chain project -> boms/<node_id>/ child project`

`canonical node -> six-question playbook -> temporal ledger -> as-of snapshots -> independent BOM report`

Each node playbook owns only stable domain logic:

- scope and explicit exclusions;
- inputs, product/output, downstream recipients, representative companies, and financial validation metrics;
- node-specific master equations or causal formulas for demand, market value, effective supply, and investment odds;
- exactly six question definitions;
- an optional concise logic hint per question for reader orientation;
- question-level formula, purpose, conclusion rule, and failure condition.

The playbook must not contain source IDs, cutoff dates, observations, verdicts, gaps, target states, or HTML classes. Those belong respectively to the research run, evidence artifacts, target gate, and renderer.

The shared six question labels do not imply one generic explanation. HBM and power/cooling may use different logic hints, but those hints remain revisable and must not exclude newly discovered evidence.

Each atomic claim must match one canonical node and one or more of its six question IDs. Claims preserve market-visible time, actual period, forecast period, source, stance, and mapping provenance. Each as-of snapshot preserves all six question conclusions and explicit coverage gaps.

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

### 4.2 Standalone BOM five-lens adaptation

If the user explicitly chooses one BOM as the complete research object, the public
coordinate changes to five professional lenses:

| Lens | Decision question |
|---|---|
| Demand | Is demand real, accelerating, durable, and financially visible? |
| Supply | Can qualified effective supply keep up, and where are the constraints? |
| Technology | Which route wins by workload, performance per watt, TCO, and ecosystem? |
| Valuation | How much growth is already priced at the as-of date? |
| ESG | Which environmental, policy, concentration, and governance factors can change cash flow or the multiple? |

The internal source workflow remains unchanged: active question search and external
material ingestion feed atomic claims. Each reviewed claim maps to
`BOM x lens x logic node x company/entity x published_at`. The five-lens playbook
then provides stable logic nodes with a question, indicators, support and refute
rules, downstream dependencies, company bridge fields, and cadence.

Research proceeds as:

`atomic claim -> reviewed claim-to-node/entity mapping -> as-of node and entity state -> thesis revision -> company earnings/expectation/valuation bridge -> investment snapshot`

Mappings are separate from immutable claims and preserve direction, node fit,
support/refute rule match, directness, novelty, materiality, expectation delta,
entities, and claim-specific rationale. `support`/`refute` require direct node fit
and an explicit rule match. Topic-related forecasts, proxies, and context use
boundary, constraint, lead, unresolved, conflict, or new-branch effects. Rejected
claim-to-node proposals remain `unmapped` in the audit ledger and do not enter node
state or the public node table. Each public lens
shows its concise logic paragraph, then logic nodes. Every node shows one
newest-to-oldest source table with exactly
`发布日期 | 报告名称 | 材料类型 | 原子观点 | 对逻辑点的影响`; claims and effects use
matching numbered lists. Real state history, revisions, gaps, and company/entity
assessments remain append-only internal coordinates. The report begins with a gated
investment snapshot. This structure does not waive canonical target recommendation gates.

## 5. Minimum Research Unit Execution

For every minimum question:

### A. Judgment model

Define object, formula/causal frame, evidence handles, conclusion rule, and failure condition.

### B. Basic reasoning hint

Write a short node-specific explanation that helps a non-specialist understand the question. It may name typical mechanisms, but it is not a search checklist.

The public renderer shows the model and hint once under `基本理解思路`. It must not generate one evidence card per hint row.

The public temporal sequence is `基本理解思路 -> 当前结论 -> 相较上一截面的变化 -> 时间演化 -> 映射材料 -> 信息覆盖`.

### C. Dual-loop material collection

Pull research searches gaps under the six questions. Push ingestion scans available external reports and approved feeds. Both loops enter the same material-intake ledger, but discovery alone never creates evidence claims.

Every material has:

- `material_class`: `official_filing`, `official_company`, `sell_side_research`, `authoritative_third_party`, `market_news`, `expert_opinion`, or `other`;
- `ingestion_channel`: `question_search`, `knowledge_base_scan`, or `manual_import`;
- provider identity, external ID, content hash, publication/discovery time, matched BOMs, mapping status, and cutoff usage.

Before either evidence loop, the attended `ima_daily_archive` reuses a visible
logged-in IMA page, enumerates the approved year/month/day folder across all pages
or lazy-loaded rows, and clicks every missing PDF's visible download control. The
completed browser downloads are imported into repository
`source/ima/<directory_date>/`. This preserves an archive manifest but creates no
claims and does not call IMA OpenAPI. `question_search` starts from one
`BOM x question` gap and queues parsing
only for that question. `knowledge_base_scan` reads the central archive manifest,
judges relevance against each canonical BOM profile, verifies `published_at`, copies
the selected original into that BOM's `source/ima/<published_at>/`, and queues one
parse task for every potentially relevant question. One document may route to
several BOMs. Evidence ledgers retain portable project-relative paths. Public local
HTML keeps the relative `source/...` path so a neighboring PDF opens from a
`file://` report and navigates in the current tab, while Markdown resolves it to
an absolute filesystem link.

The same intake contract also serves `standalone-bom`. In that scope, the stable
coordinates are the five professional lenses rather than the six S-curve questions.
Downstream database routing therefore resolves coordinates from `project.json`; it
must not assume six questions. Each relevant document is archived once, but parsed
separately against every potentially affected lens. Only non-empty, GPT-reviewed
lens claims enter the temporal ledger. A second reviewed step maps each claim to one
primary logic node, optional secondary nodes, and one or more companies/entities.
For a `logic_chain_centered` profile, the versioned causal chain is the primary
research schema. Atomic claims keep only a minimum audit envelope; a separate
mapping records `support`, `refute`, `boundary`, `constraint`, `new_branch`,
`conflict`, `unresolved`, or `neutral`, plus rationale and downstream impacts.
Claims remain immutable, and mechanisms that do not fit remain visible for chain
revision.

HTML renders the primary hierarchy
`lens -> causal logic node -> source row -> numbered atomic claim`. Every node
contains one table with exactly
`发布日期 | 报告名称 | 材料类型 | 原子观点 | 对逻辑点的影响`, ordered by market-known
`published_at` from newest to oldest. One source occupies one row. Atomic claims
and mapping effects use parallel `1, 2, 3...` numbering; locator-backed
`effective_period` and `target_period` stay in the claim cell. Internal real state
history, revisions, mapping rationale, downstream effects, and company/entity
coordinates are retained but are not expanded into duplicate public modules.
The public lens stops after its causal-node evidence and any explicitly retained
derived view. It does not render a separate lens-level `全局结论与趋势`; the leading
`当前投资判断` owns global synthesis, while internal lens conclusions and trends
remain available for audit and snapshot construction.

For a demand-side question tree, Q1 is a pure demander taxonomy. It asks only:
`当前有哪些需求方？哪些主体是潜在未来需求方？` The two groups must be
mutually exclusive at the selected as-of date. Do not put business, task,
workload, system, specification, channel, quantity, or snapshot-change branches
under Q1. Q2 measures current demand by the Q1 groups; later leaves test workload,
intensity, budget, orders, and realization.

Q1 and Q2 are `presentation_role: derived_view`. They are useful classification and
quantity projections of the evidence but are not the demand research backbone.
The public lens must preserve every causal node from workload through compute
intensity, budget, orders/delivery, and financial realization before rendering the
collapsed Q1/Q2 supporting views.

Q2 has three child groups: `当前需求方`, `潜在未来需求方`, and `其它分类`.
`当前需求方` searches every Q1 current demander for the best available current
quantity, forecast, disclosed sample, or value proxy and records whether the mapping
is direct, proxy, sample, or gap. `潜在未来需求方` reuses every Q1 potential-future
demander and preserves its relevant observations without adding them to the current
base. `其它分类` preserves industry totals and useful forecasts that cannot be
allocated without false precision, grouped by their own information category. All
current Q1 demanders must be covered; potential-future categories may show a clear
empty state until evidence arrives. One specific category may own multiple relevant
facts, forecasts, samples, or proxies. Render one table per specific category rather
than flattening categories into one row each. Every table uses exactly `来源 | 期间 |
信息类型 | 具体信息`. `信息类型` is the normalized source-material class:
`官方财报`, `第三方研究`, `市场消息`, or `机构研报`. The final cell keeps the metric,
value, mapping quality, and caveat together. HTML uses collapsed outer disclosures
with collapsed specific-category disclosures nested inside; Markdown mirrors the
same numbered hierarchy.

Public module selection does not rewrite this internal question architecture. When
the user narrows a lens for reading, preserve all internal leaves and append-only
evidence, and record the public subset separately with `public_logic_node_ids` in
canonical order. In `logic_chain_centered` mode this subset must keep every causal
node; it may omit only derived views. Q2 cannot be exposed without its Q1
classification view.

Each standalone BOM keeps its report, source index, selected IMA originals, inbox,
temporal ledger, and intake audit at `research/bom/<bom_project_id>/`. Repository
`source/ima/` remains the complete provider mirror; project copies are intentionally
limited to relevant, date-verified reports so a BOM never depends on sibling or
parent project directories.

Choose concrete fields, not baskets. Example: `Microsoft commercial RPO ($B)` is valid; `cloud budget proxy` is not.

### D. Active search

For each identified evidence gap:

1. Review the current six-question coverage gap.
2. Resolve professional Universe sources from `config/source_universes.json` through `SourceUniverseRepository`.
3. Add official company/customer filings and justified specialist sources.
4. Create direct/Exa queries for the missing fact, forecast, opinion, valuation, or refutation evidence and enforce the cutoff.
5. Ingest user-provided reports and other approved external materials through `classify -> deduplicate -> cutoff gate -> BOM route -> parse inbox`.
6. Record selected source IDs or an explicit gap reason.

One broad query cannot stand in for active question-specific research. The reader-facing logic hint is not a search whitelist.

### E. Per-source parsing

Create one extraction per `question x source`. Parse the source against the current question's dimensions, even if the same document was parsed elsewhere. Unparsed intake documents remain pending materials, not support/refute evidence.

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

Split every source into atomic claims and map each claim to `BOM x six-question coordinate x published_at`. Preserve `effective_period`, `target_period`, `ingested_at`, `material_class`, and `ingestion_channel`. Facts, forecasts, opinions, messages, valuations, and refutations must remain distinguishable. Archive-folder, provider-upload, provider-update, and discovery dates never substitute for `published_at`; unresolved publication dates block claim promotion until the original is verified.

The same source may yield several claims and map to several questions. Unmapped material remains in `unmapped/new_theme`; it is not silently dropped. Actual history never includes guidance or forecasts. Claiming acceleration requires same-definition history or explicit YoY/multiple evidence. Claiming runway requires a cutoff-visible forward anchor and mechanism.

## 6. Semantic Completion

A BOM question is complete only when `source_universe_plan`, direct/Exa search plan, and `claim_mapping_plan` are non-empty and active search, per-source parsing, source IDs, and evidence summary are complete. `claim_mapping_plan` must preserve atomic claim types, the four time fields, and the unmapped-material policy. Q6 additionally requires explicit `refuting_source_ids` and `refutation_evidence_summary`.

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

For industry/theme/S-curve work, rendering uses this artifact topology:

```text
<industry_project>/
  project.json
  professional_report.html          # default public industry-index
  professional_report.md            # portable audit sidecar
  boms/manifest.json
  boms/<node_id>/
    project.json
    sources.jsonl
    research_run.json               # optional until the node is independently completed
    professional_report.html        # default public BOM report
    professional_report.md          # portable audit sidecar
```

The parent report owns the chain map, BOM navigation, and aggregated targets. It does not duplicate child question content. A BOM child can be searched, parsed, scored, regenerated, and validated without regenerating the research content of sibling nodes. The manifest and canonical BOM registry must have exact ordered node-ID coverage.

## 10. Validation

Before publication:

- validate QA and per-source parser/review schemas;
- validate BOM semantic readiness and target research gates;
- validate cutoff visibility and label isolation;
- validate the four-section Markdown contract and source-link/static structure;
- verify no failed-gate target is `actionable_long`.
