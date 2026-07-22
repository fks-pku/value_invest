# Research Report Contract

This is the sole default public-report contract. It defines presentation only; domain questions, metrics, parsers, and thresholds remain in playbooks and internal artifacts.

## Top-Level Order

Public HTML contains exactly four top-level sections:

1. `当前研究的问题`
2. `行业概况`
3. `标的推荐`
4. `来源索引`

Public `下钻 QA` is opt-in. The complete adaptive QA tree, L3-L5 research units, source plans, parser outputs, reviews, and scoring worksheets stay internal by default.

## Report Scopes and File Layout

Industry/theme/S-curve research uses two public report scopes under one project:

```text
<industry_project>/professional_report.html                 # data-report-scope="industry-index"
<industry_project>/boms/manifest.json
<industry_project>/boms/<node_id>/professional_report.html # data-report-scope="bom-node"
```

The `industry-index` is a chain overview and navigation report. It must not embed every BOM's six-question body. The `bom-node` report is an independently refreshable node report and must contain exactly one canonical BOM node. Both scopes keep the same four top-level sections so navigation and frontend behavior remain stable.

The parent `project.json` owns the canonical ordered `bom_projects` manifest. Every child owns `project.json`, filtered `sources.jsonl`, optional `research_run.json`, and its HTML report. `boms/manifest.json`, parent metadata, and child identity must agree exactly on node ID and path. No copied HTML directory is a valid child project.

## 1. Current Research Goal

Render one compact `goal-card` with `constraint-definition` for industry/theme or technology-route work. It states:

- exact research object and time boundary;
- investment decision being tested;
- scope and exclusions;
- current constrained judgment;
- biggest uncertainty.

Do not include framework or execution commentary.

## 2. Industry Overview

Use one `industry-overview-section`.

### Parent Industry Index

The parent `industry-index` contains:

1. `details.industry-module.supply-chain-section` / `01 技术链与BOM呈现`.
2. `details.industry-module.bom-project-index` / `02 BOM 独立研究目录`.

The directory renders one full-width `bom-index-card` per canonical node. Every card links to `boms/<node_id>/professional_report.html`, states node scope and research status, and may show related-target count. The parent must render zero `bom-research-module` and zero `bom-question-card` elements.

### 01 Technology Chain and BOM

Render `details.industry-module.supply-chain-section` with:

- `summary.module-head`, `module-index`, and `chevron`;
- beginner-readable Chinese `chain-explain` and `chain-plain-summary`;
- nested collapsed `chain-detail-panel` cards;
- upstream, midstream, downstream lane view using `chain-lane-map`;
- simple value-flow steps using `chain-value-flow` and `chain-simple-flow`;
- `component-value-chain` and one canonical `bom-taxonomy` registry.

Every BOM node has one stable ID and one public name. It explains inputs, output/product, downstream recipient, representative companies, and financial validation metrics.

### BOM Child Report

Each `bom-node` child report links back to `../../professional_report.html` with `project-back-link`. Its `行业概况` renders exactly one `details.industry-module.bom-research-module`. Use `bom-node-brief` followed by exactly six `details.bom-question-card` nodes:

1. `当前 BOM 的需求是否会被 S 曲线放大拉动？`
2. `供给能否跟上？`
3. `谁控制供给？`
4. `是否已经财务兑现？`
5. `市场是否已定价？`
6. `反证是什么？`

Every completed module must be assembled from that node's own six-question `BomNodePlaybook`, append-only temporal evidence ledger, and reproducible as-of snapshot. The canonical BOM registry, child-project manifest, playbook registry, ledger node IDs, snapshot node IDs, and rendered module IDs must agree. A static renderer answer or generic fallback is not a completed module even when six visible cards exist. A child may exist as `partial_research`, but the status must remain explicit and target action state stays gated.

The six questions are hard logical coordinates. A playbook may provide a short node-specific model, formula, and basic logic hint, but the hint is not a mandatory evidence path and does not restrict new themes discovered in source material.

Each card is an independent minimum research unit. Raw Universe/Exa queries, parser traces, and execution commentary stay internal.

### Question Temporal Sequence

Inside every BOM question card:

1. `details.bom-question-understanding` / `基本理解思路`
2. `section.bom-question-current` / `当前结论`
3. `details.bom-question-change` / `相较上一截面的变化`
4. `details.bom-question-timeline` / `时间演化`
5. `details.bom-question-materials` / `映射材料`
6. `details.bom-question-coverage` / `信息覆盖`

`基本理解思路` contains only:

- the question's professional model and purpose;
- one concise formula or reasoning rule;
- an optional short arrow-separated logic hint;
- an explicit note that the hint is for orientation, not an evidence whitelist.

Do not render one evidence card per logic-hint row. Newly discovered entities, metrics, mechanisms, and counterarguments enter through mapped claims even when the original hint did not mention them.

### Current Conclusion and Change

`当前结论` is visible after the question card opens. It contains conclusion, strength, supporting mechanism, main refutation, target impact, latest material date, and claim-level links.

`相较上一截面的变化` may claim a change only when a real prior structured snapshot exists. A migrated project with no prior snapshot must say it is the baseline and must not reconstruct old conclusions from hindsight.

### Time Evolution and Mapped Materials

`时间演化` is ordered by `published_at` and shows material information in market-visible order. Each row includes date, source, claim type, stance, statement, effective period, target period, and link. Research-revision rows are separate from source rows and preserve previous conclusion, current conclusion, trigger claims, and target impact.

`映射材料` supports fact, forecast, opinion, message, valuation, and refutation records. One document may create several atomic claims and may map to several questions. Each claim preserves:

- `published_at`: when the market could know it;
- `effective_period`: which actual period it describes;
- `target_period`: which future period it forecasts;
- `ingested_at`: when the system received it;
- source type, stance, entity, metric, mapping origin, and confidence when available.

Source material that cannot yet be mapped remains visible in an internal `unmapped/new_theme` queue. It is never silently dropped or forced into an unsuitable question.

Required public temporal components are:

- `bom-temporal-baseline` for an honest first snapshot with no invented history;
- `bom-material-timeline` for publication-order evolution;
- `bom-mapped-material-table` for atomic claim inspection;
- `bom-coverage-status` for question-level completeness and gaps.

### Information Coverage

`信息覆盖` is compact and question-level. It displays:

- actual, forecast, opinion, message, valuation, and refutation claim counts;
- supporting and conflicting claim counts;
- earliest and latest material dates;
- coverage status and explicit gaps;
- whether a prior thesis snapshot exists.

Coverage is not measured by raw source count alone. Completion requires question-specific parsing, source diversity, recency, forward evidence, and observed counterevidence or an explicit gap.

### BOM S-Curve Rollup

Render one collapsed `details.bom-s-curve-stage-card` after the six questions. It contains:

- `bom-stage-source-discipline`
- `bom-stage-current`
- `bom-stage-evidence-grid`
- `bom-stage-next-signal`
- `bom-stage-downgrade-signal`

The stage is pending unless all six questions pass semantic completion. Every question needs persisted source planning, question-specific atomic parsing, temporal coverage, and strengthening evidence. Q6 requires observed refuting evidence, not only a list of hypothetical risks.

### Optional Deepening Modules

`行业空间`, `竞争格局与利润池`, `瓶颈点`, and `关键变量与待验证数据` are optional. Add them only when the user explicitly asks or a playbook requires them for a decision. If enabled, they reuse the canonical BOM taxonomy and the same question-level search/parse discipline. They never become mandatory public sections by accident.

## 3. Target Recommendations

Use one `target-section` containing, in order:

1. `artifact-card` explaining that this is a research observation list.
2. `target-profit-bridge` from BOM demand to revenue, margin, FCF, orders, or backlog.
3. `target-valuation-table` showing as-of valuation evidence and priced-in expectations.
4. `target-odds-model` with `target-odds-table`.
5. dense `target-table`.

Each target must expose:

- canonical `thesis_node_id` and node name;
- `candidate_action_state` and final `action_state`;
- research-gate completion and reasons;
- explicitly verified company exposure and financial bridge, not a status inferred from generic source IDs;
- valuation/mispricing status;
- risks, kill tests, and monitoring cadence.

`actionable_long` is allowed only when BOM six-question completion, explicit refutation, company exposure, valuation, component-specific scoring evidence, and quantitative kill tests all pass. Otherwise show `watch_only`; missing BOM mapping is `no_action`.

Use `state-actionable_long`, `state-watch_only`, and `state-no_action` classes.

The parent report shows the aggregated chain-wide target list. A BOM child shows only targets whose canonical `thesis_node_id` matches that child. Updating one child must not rewrite sibling target evidence; parent aggregation may be regenerated after the child result is accepted.

## 4. Source Index

Render one collapsed `source-collapse` with source ID, linked title, bucket, visible date, and concise use summary.

The parent may index the complete chain source set. A BOM child indexes only sources selected by that node's six questions or its mapped targets.

Claim-level links in the report are mandatory; source chips and the index are audit supplements, not substitutes.

## Interaction and Visual Rules

- Nested content is a collapsed `details` node with direct `summary` and `chevron`.
- Repeated sibling cards are full-width, one card per row.
- Tables use stable columns and local horizontal `table-scroll`.
- Text never overflows or overlaps.
- Keep the existing restrained Apple-like visual language and canonical component family.
- Do not render raw search queries, parser traces, framework explanations, or framework change logs. Thesis-revision history is research content and remains visible.

## Historical Backtest Lock

Public prose reads as if written on `as_of_date`. Only cutoff-visible sources may support it.

Freeze recommendations before attaching labels. Later price data appears only in the rightmost final-target label columns or one isolated label block. Missing non-US labels remain visibly unverified; they do not remove the target.

## Non-Drift Locks

1. Four-section hierarchy lock.
2. Parent/manifest/child path and identity lock.
3. Canonical BOM ID/name lock.
4. BOM six-question semantic gate lock.
5. Backtest time-slice lock.
6. Frontend card and table-scroll lock.
7. Public no-changelog lock.

## Validation Requirements

`framework_contracts.py` and domain quality gates must validate semantics, not only HTML classes:

- four-section order;
- `industry-index` has a supply-chain module and `bom-project-index`, with no embedded six-question modules;
- each `bom-node` child has exactly one BOM module, six cards, one rollup, and a parent link;
- parent manifest and child directories have exact one-to-one identity coverage;
- actual-history and future-expectation separation;
- source links and table overflow;
- six-question completion and Q6 refutation;
- target BOM mapping, valuation, company exposure, score trace, and action-state gate;
- label isolation;
- no public process text.

Run `validate-report-contract`, `validate-research-artifacts --require-l3`, targeted unit tests, and a browser or DOM smoke check before publishing a refreshed report.
