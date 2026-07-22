---
name: value-invest-research
description: Use for end-to-end investment research that starts from a research goal, adapts professional questions by domain, actively searches and parses evidence, evaluates S-curve/BOM opportunities, and produces a gated target observation report.
---

# Value Invest Research Skill

Use this skill for all investment research in this repository.

## Canonical References

- Internal question/execution contract: `frameworks/research_goal_qa.md`
- Public HTML contract: `frameworks/research_report_contract.md`
- Domain playbooks: `frameworks/domain_playbooks.md`
- Architecture: `../../docs/architecture/hexagonal_research_system.md`
- Professional source registry: `../../config/source_universes.json`

Do not mix another report template into this workflow.

## End-to-End Sequence

1. Convert the request into `ResearchGoal` with mode, date, decision, scope, and domain hint.
2. Use `investment-question-architect` plus the domain playbook to build internal QA to maximum depth five.
3. For S-curve work, define a canonical BOM taxonomy and run the six-question research loop for every node.
4. Use `research-source-planner`; GPT selects the professional Universe and direct/Exa search plan from each six-question coordinate's current coverage gaps.
5. Parse one source at a time against the current question with the appropriate specialty skill. DeepSeek may perform first-pass reading when available; GPT verifies every adopted claim.
6. Roll facts, inference, judgment, gaps, refutation, and triggers upward.
7. Run company exposure and as-of valuation analysis.
8. Score and rank only after semantic completion gates.
9. Freeze historical recommendations, then attach labels.
10. Build `ReportViewModel` and render the four-section public report.

## Non-Negotiable Research Rules

- Facts, inferences, judgments, leads, and gaps are distinct.
- Every material claim has a claim-near source link or traceable source ID.
- Messages/opinions are leads unless independently verified.
- The same source is re-parsed for every question dimension it serves.
- Search is active and question-level. A general source pool cannot replace a fresh minimum-unit search.
- Active search starts from explicit evidence gaps, while external reports may introduce previously unknown metrics or mechanisms through atomic claim mapping.
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

The default HTML contains exactly:

1. `当前研究的问题`
2. `行业概况`
3. `标的推荐`
4. `来源索引`

Industry/S-curve output is split by scope. The parent `professional_report.html` uses `data-report-scope="industry-index"`: `行业概况` contains `01 技术链与BOM呈现` plus `02 BOM 独立研究目录`, and each full-width `bom-index-card` links to `boms/<node_id>/professional_report.html`. It never embeds all six-question modules. Each child report uses `data-report-scope="bom-node"`, contains exactly one BOM module, preserves the six questions and S-curve rollup, and links back to the parent.

Each BOM child owns `project.json`, node-filtered `sources.jsonl`, a temporal ledger, as-of snapshots, optional compatibility `research_run.json`, and its report. The parent owns `boms/manifest.json`, canonical taxonomy, navigation, and aggregated targets. Public `下钻 QA`, raw Universe/Exa plans, parser traces, workbench data, and framework-change notes remain hidden unless requested.

Use nested collapsed `details`, claim-near blue links, one full-width sibling card per row, and local `table-scroll` for wide tables. Keep the public report clean and research-first.

## Validation

Before completion:

- run focused and framework unit tests;
- run `validate-report-contract`;
- run `validate-research-artifacts --require-l3`;
- inspect DOM/static invariants;
- confirm no failed research gate renders as `actionable_long`;
- run `git diff --check`.
