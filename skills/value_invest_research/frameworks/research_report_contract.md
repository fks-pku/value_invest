# Research Report Contract

This is the sole default public-report contract. It defines presentation only; domain questions, metrics, parsers, and thresholds remain in playbooks and internal artifacts.

## Top-Level Order

Public HTML contains exactly four top-level sections:

1. `当前研究的问题`
2. `行业概况`
3. `标的推荐`
4. `来源索引`

Public `下钻 QA` is opt-in. The complete adaptive QA tree, L3-L5 research units, source plans, parser outputs, reviews, and scoring worksheets stay internal by default.

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

### 01 Technology Chain and BOM

Render `details.industry-module.supply-chain-section` with:

- `summary.module-head`, `module-index`, and `chevron`;
- beginner-readable Chinese `chain-explain` and `chain-plain-summary`;
- nested collapsed `chain-detail-panel` cards;
- upstream, midstream, downstream lane view using `chain-lane-map`;
- simple value-flow steps using `chain-value-flow` and `chain-simple-flow`;
- `component-value-chain` and one canonical `bom-taxonomy` registry.

Every BOM node has one stable ID and one public name. It explains inputs, output/product, downstream recipient, representative companies, and financial validation metrics.

### 02+ One Module per BOM Node

Render one `details.industry-module.bom-research-module` per canonical node. Use `bom-node-brief` followed by exactly six `details.bom-question-card` nodes:

1. `当前 BOM 的需求是否会被 S 曲线放大拉动？`
2. `供给能否跟上？`
3. `谁控制供给？`
4. `是否已经财务兑现？`
5. `市场是否已定价？`
6. `反证是什么？`

Every module must be assembled from that node's own validated node-specific `BomNodePlaybook` plus its cutoff-frozen research run. The canonical BOM registry, playbook registry, research-run node IDs, and rendered module IDs must have exact one-to-one coverage. A static renderer answer, copied causal chain, or generic fallback is not a valid module even when six visible cards exist.

The shared card sequence is presentation-only. Judgment formulas, causal stages, primary/cross-check/refutation metrics, and conclusion rules must remain specific to the current node.

Each card is an independent minimum research unit and begins with collapsed `bom-question-research-status`. Raw Universe/Exa queries stay internal; the status card shows only completion and evidence-gap discipline.

### Question Evidence Sequence

Inside every BOM question card:

1. `details.bom-step-research-logic` / `研究逻辑链`
2. one `details.bom-stage-integrated-card` per exact logic-chain row, numbered from `02`
3. `details.bom-step-question-conclusion` / `本问结论`
4. `details.bom-step-target-impact` / `对标的推荐的影响`

The internal node playbook continues to store the judgment model and causal stages as separate domain fields. The public `研究逻辑链` compiles them into one card and must contain:

- judgment model name, purpose, formula, and conclusion rule once;
- one row per exact causal stage;
- for each row: why the stage matters, what metric family will test it, and how the stage will be judged;
- no observed metric values, source plans, raw searches, or verdict prose.

Do not render separate public `判断模型` or `具体逻辑链条` cards. Do not repeat the model's key questions or metric families outside their corresponding causal rows.

Every integrated stage card contains three collapsed `bom-stage-subcard` elements:

- `Metric 历史与现状`
- `市场的未来预期`
- `第一性原理评估`

The conclusion appears after evidence, never before it.

### Metric History

For each logic link, choose concrete, collectible metrics before searching. A metric definition names subject/owner, exact field, unit, frequency, preferred source, and point-count expectation.

Render:

- one `metric-history-group` per selected metric;
- metric name once in `metric-history-caption` as a blue `metric-history-name` link;
- definition once in `metric-history-definition`;
- actual observations in `metric-history-table`;
- `期间 / 截点` and mapped `实际时间` for every fiscal period;
- `metric-trend-gap` when fewer than five same-definition actual points exist.

Do not mix guidance, consensus, TAM, or target values into actual history. For multi-company same-definition metrics, use tables rather than multi-line charts. Wide tables must sit inside `table-scroll`.

### Market Expectations

Use direct `expectation-table-group` blocks inside the expectation subcard. One entity/institution gets one full-width `bom-expectation-table`.

Columns are:

- `公司 / 机构`
- `现状期间`
- `现状实际时间`
- `现状口径 / 数值`
- `指引期间`
- `指引实际时间`
- `预期 / 指引口径 / 数值`
- `口径说明 / 投资含义`

The company/institution cell is a blue source link. Current results are baselines, not expectations. Only explicit guidance, forecast, consensus, TAM, target, or customer budget is a forward expectation. Explain proxy or fiscal-calendar mismatches.

### First Principles

For the same logic link, state:

- why the mechanism can continue;
- how efficiency, substitution, supply release, budget, or ROI can break it;
- current judgment and confidence.

### BOM S-Curve Rollup

Render one collapsed `details.bom-s-curve-stage-card` after the six questions. It contains:

- `bom-stage-source-discipline`
- `bom-stage-current`
- `bom-stage-evidence-grid`
- `bom-stage-next-signal`
- `bom-stage-downgrade-signal`

The stage is pending unless all six questions pass semantic completion. Every question needs persisted Universe, direct/Exa, and metric-candidate plans plus completed per-source parsing and strengthening evidence. Q6 requires observed refuting evidence, not only a list of hypothetical risks.

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

## 4. Source Index

Render one collapsed `source-collapse` with source ID, linked title, bucket, visible date, and concise use summary.

Claim-level links in the report are mandatory; source chips and the index are audit supplements, not substitutes.

## Interaction and Visual Rules

- Nested content is a collapsed `details` node with direct `summary` and `chevron`.
- Repeated sibling cards are full-width, one card per row.
- Tables use stable columns and local horizontal `table-scroll`.
- Text never overflows or overlaps.
- Keep the existing restrained Apple-like visual language and canonical component family.
- Do not render raw search queries, parser traces, framework explanations, or change logs.

## Historical Backtest Lock

Public prose reads as if written on `as_of_date`. Only cutoff-visible sources may support it.

Freeze recommendations before attaching labels. Later price data appears only in the rightmost final-target label columns or one isolated label block. Missing non-US labels remain visibly unverified; they do not remove the target.

## Non-Drift Locks

1. Four-section hierarchy lock.
2. Canonical BOM ID/name lock.
3. BOM six-question semantic gate lock.
4. Backtest time-slice lock.
5. Frontend card and table-scroll lock.
6. Public no-changelog lock.

## Validation Requirements

`framework_contracts.py` and domain quality gates must validate semantics, not only HTML classes:

- four-section order;
- required BOM/card sequence;
- actual-history and future-expectation separation;
- source links and table overflow;
- six-question completion and Q6 refutation;
- target BOM mapping, valuation, company exposure, score trace, and action-state gate;
- label isolation;
- no public process text.

Run `validate-report-contract`, `validate-research-artifacts --require-l3`, targeted unit tests, and a browser or DOM smoke check before publishing a refreshed report.
