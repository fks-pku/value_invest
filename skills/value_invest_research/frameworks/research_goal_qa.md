# Research Goal QA Framework

This is the only active research framework for this project.

Use it whenever the user proposes a research goal, topic, company, sector, event, concept, or investment question.

Final report presentation is governed by `research_report_contract.md`. Follow that contract for all future user-facing HTML reports unless the user explicitly asks to iterate on the framework.

## Current S-Curve Simplification

The current default research flow is S-curve-first. Spend roughly 80% of the first-pass research effort on:

- the new technology's future prospect;
- feasibility and commercialization evidence;
- future industry space;
- adoption inflection and irreversibility;
- whether demand is starting to exceed available supply.

BOM is presentation-only in this first pass. Use it to explain the technical chain clearly: upstream/midstream/downstream, who is on the chain, what each company/node receives, what it produces, and whom it supplies. Do not force detailed `竞争格局与利润池` or `瓶颈点` analysis in the default first-pass report. Those are optional follow-up modules for later iterations.

## System Boundary Contract

New research topics must enter through the domain question architecture path:

`ResearchGoal -> DomainPlaybook -> QuestionArchitecture`

Do not start a new topic from a report template, hard-coded HTML outline, or a copied previous report. Domain playbooks own concrete L2/L3 questions, source schemas, metrics, tracking indicators, and thresholds.

Public report assembly must use the presentation boundary:

`ResearchProjectRepository -> ReportViewModel -> CanonicalReportRenderer`

The report contract owns only section order, hierarchy, interaction, and component classes. If the research view changes, update the playbook/source/QA layer. If the frontend changes, update the renderer and report contract. Keep these concerns separate.

## Output Order

Final user-facing HTML reports must use exactly this top-level order:

1. Current research goal.
2. Industry overview / `行业概况`.
3. Final target recommendation.
4. Source index.

Current compact public report lock: do not render public `下钻 QA` by default. Keep drilldown QA trees, source plans, parser outputs, and workbench traces as internal artifacts unless the user explicitly asks to inspect them.

The final target recommendation is a research conclusion section. It must synthesize all QA evidence into a ranked observation list with specific targets, win probability, payoff odds, rationale, required verification data, and downgrade triggers. It keeps the canonical `target-profit-bridge` and `target-valuation-table` components even when the first pass is S-curve-focused. It must not issue buy/sell/hold instructions.

`行业概况` is mandatory and is the fact-map layer before target synthesis. Current first-pass public reports use `01 技术链与BOM呈现` plus one numbered per-BOM module from `02` onward. Every module renders as a clickable collapsed `details.industry-module > summary.module-head` card with `module-index`, `chevron`, and `industry-module-body`. `技术链与BOM呈现` must keep a readable upstream/midstream/downstream swimlane view, a value-flow view, and a `component-value-chain` so readers can see who provides what before target synthesis. These long chain components must render as nested clickable `details.chain-detail-panel` cards. Each per-BOM module must use six collapsible child cards: `当前 BOM 的需求是否会被 S 曲线放大拉动？`, `供给能否跟上？`, `谁控制供给？`, `是否已经财务兑现？`, `市场是否已定价？`, and `反证是什么？`, with concise answers and source chips. Each `BOM node × child question` is a minimum research unit: before writing or strengthening the child-question verdict, GPT must create and execute a fresh question-level search/source collection pass, record `source_universe_plan` plus direct/Exa-style `exa_search_plan`, parse selected materials against the question dimensions, and mark missing evidence as explicit gaps. Public HTML keeps raw search plans internal but each `details.bom-question-card` must start with collapsed `bom-question-research-status`, then `bom-question-verdict` / `本问结论`, then a stage-flow: `01 具体逻辑链条` renders substantive causal/judgment prose plus a `bom-logic-chain-table` of `bom-logic-chain-row` entries that define only the concrete logic links, not metric names or values; each following `bom-stage-integrated-card` maps to one logic row and contains `Metric 历史与现状`, `市场的未来预期`, and `第一性原理评估` subcards; `Final 整体的未来趋势评估` synthesizes all logic-stage evidence for the whole question. Each logic row must internally define a `metric_candidate_plan` before search: GPT chooses heterogeneous metrics for that logic link, searches/parses each selected metric independently, and renders available data or explicit trend gaps. Each BOM module is an independent research unit: focus on the current BOM's own demand pull-through and unit/system elasticity, supply, controllers, financial realization, market pricing, and refutation. Other BOM nodes may be cited only as upstream/downstream validation evidence; their opportunity analysis belongs in their own BOM module. Source plans, parser traces, search queries, and per-source audit grids remain internal unless the user explicitly asks for the workbench. Do not render public `S曲线与产业空间` or `统一 BOM 口径` panels by default. Optional follow-up modules `S曲线与产业空间`, `关键变量与待验证数据`, `竞争格局与利润池`, and `瓶颈点` may be added later, but they are not mandatory in the first public report.

After the six child questions of a BOM are complete, and only then, the report may evaluate that BOM's S-curve stage. Render this as one collapsed `details.bom-s-curve-stage-card` after the six `bom-question-card` nodes. The rollup must include `bom-stage-source-discipline`, `bom-stage-current`, `bom-stage-evidence-grid`, `bom-stage-next-signal`, and `bom-stage-downgrade-signal`. If any child question lacks fresh search evidence, stage confidence must be downgraded or marked pending rather than asserted from local cached material.

The four BOM question sections are not allowed to describe the template itself. Public body copy must be substantive research prose. The first section states the causal chain, judgment mechanism, or metric-selection logic and then provides the metric map table. The second section must break the chain into per-link cards rather than one loose metric list. Same-metric historical data tables should collect at least five cutoff-visible, same-definition data points whenever possible; if the same metric spans multiple companies, show comparable company series as data tables rather than multi-line charts. If fewer than five same-metric points are available, render a visible trend gap with point count and any available data rows instead of drawing a misleading line. Avoid process phrases such as “这一段/这张卡先讲什么”, “01 只讲”, “02 再展示”, or “本报告会”.

Historical metric cards are actual-history only. Do not mix realized company disclosures with management guidance, consensus forecasts, TAM targets, or next-period outlook in the same historical curve. Forward-looking values should live in the same integrated stage card's `市场的未来预期` subcard or in explanatory future/current prose. If the actual-only series falls below the five-point threshold, render a trend gap rather than filling the curve with guidance.

Inside `Metric 历史与现状`, render direct metric table groups: `Metric 1`, `Metric 2`, etc., each followed by a real `metric-history-table`. If one logic link uses multiple heterogeneous metrics, a compact metric-candidate/coverage strip may appear before the metric tables to show selected metrics and coverage status; it must not expose raw search queries. Do not render a separate generic `本环节应看哪些 Metric` instruction card or prose-first `当前证据读法` card above the table. Put the concrete metric name once in `metric-history-caption` as a blue `metric-history-name` source hyperlink, and preserve the metric definition / data requirement once in `metric-history-definition` so the reader can inspect the exact subject, field, unit, period/frequency, source, and point-count standard in the same view as the data. Do not repeat identical `Metric` or `口径 / 数据要求` columns on every historical data row; data rows should focus on changing observations such as subject when row-specific, period/cutoff, actual calendar time, value, relative change, and notes. Each `metric-history-table` must keep the disclosed `期间 / 截点` label and add `实际时间`; map fiscal labels such as `Q2 FY2026` to natural time windows whenever the fiscal calendar is known.

Primary metric definitions belong inside each `bom-stage-integrated-card` under `Metric 历史与现状`, not in the `01` logic-chain table. Each logic link should select one representative primary metric unless the research explicitly needs multiple heterogeneous metrics or a comparable multi-company same-definition series. The metric label must identify the subject/company or source owner, the exact disclosed field, and the unit. The data requirement must state the subject, field, unit, frequency or period, preferred source, and five-or-more same-definition point requirement; if this cannot be met, the history card must render a trend gap. Vague baskets such as `hyperscaler budget/RPO`, `order funnel`, `usage/workload anchors`, or `revenue checkpoints` are not valid primary metric names. Use them only as supporting cross-checks in prose.

Nested-structure interaction is a default report contract. When a public section renders nested content inside a question, module, method, chain, grid, card stack, table panel, mechanism panel, or repeated same-level card group, that nested structure must be a clickable `details` node with a direct `summary`, visible `chevron`, and concise title. Nested structures default collapsed so readers can locate the relevant layer before opening it. In the BOM stage-flow framework, every `bom-step-card`, `bom-logic-chain-panel`, `bom-stage-integrated-card`, `bom-stage-subcard`, `bom-mechanism-card`, and `bom-step-final-trend` must be collapsed `details` by default. The history and expectation subcards may directly render tables because the subcard itself is already the collapsible layer.

Inside each `bom-stage-integrated-card` / `市场的未来预期`, render direct entity expectation table groups rather than another nested `details.bom-future-card`. Use `实体 1 预期`, `实体 2 预期`, etc., and put one full-width `bom-expectation-table` under each title. The table columns are `公司 / 机构`, `现状期间`, `现状实际时间`, `现状口径 / 数值`, `指引期间`, `指引实际时间`, `预期 / 指引口径 / 数值`, and `口径说明 / 投资含义`; the `公司 / 机构` cell must be a blue source hyperlink. Fiscal periods such as `Q2 FY2026` must be mapped into calendar windows when the fiscal calendar is known. Mixed-entity rows must be marked as mixed-calendar aggregates instead of forcing one company's fiscal year onto all entities. Do not use scattered field cards or a separate `市场现在预期什么？` prose card as the primary presentation. Use the closest same-metric historical baseline for the guidance metric whenever available; if only a proxy is available, explicitly mark the口径 mismatch. Current usage, realized revenue, backlog, RPO, product roadmaps, or monitoring metrics are not market expectations by themselves; label them as baseline, validation, roadmap, or gap unless the source gives explicit guidance, forecast, consensus, TAM, or target values. Third-party forecasts may only appear under the closest matching `01` logic-chain row with a口径 caveat; they must not create a separate public expectation stage unless that stage also exists in `01`.

`产业链与生态位` must also define the report's single public BOM taxonomy through `bom-taxonomy`, `bom-taxonomy-grid`, and `bom-taxonomy-card`. This taxonomy is the public primary key for the industry overview. The same public node names must be reused and expanded one-to-one in `行业空间`, `竞争格局与利润池`, `瓶颈点`, `关键变量与待验证数据`, QA artifacts, and `标的推荐` target mapping. Missing any taxonomy node in a later public module is contract-invalid. Source-level excerpts may keep narrower source wording, but public report node labels cannot drift. Demand/customer capex can be displayed only as a supplementary demand-validation layer, not as a BOM node. `竞争格局与利润池` should display each BOM node's fixed question cards as a single-column full-width `competition-question-grid`, so readers review the four question lenses one card at a time.

Research type adaptation, question architecture, source planning, specialty parsing, GPT verification, tool attribution, and iteration notes are internal process artifacts. Store them in workbench JSON, logs, or internal files; do not render them as top-level HTML report sections unless the user explicitly asks to inspect process.

Final reports also have a public no-changelog lock. Do not render change logs, upgrade logs, "本轮/本次升级", "本轮/本次更新", "本轮如何落实", mechanism-depth checklists, framework explanations, execution traces, tool traces, or workbench/process commentary unless the user explicitly asks to inspect process. Framework upgrades should appear only through better questions, evidence, scoring, and target reasoning.

Do not append a generic full report, workbench appendix, or any other research template.

Do not compress away QA depth when refreshing a report. Preserve the full available QA tree and all answered questions unless the user explicitly asks for an executive version.

## Persistent Framework Changes

When the user changes a report structure, interaction pattern, section order, or presentation logic, treat that change as a persistent default research-system requirement unless the user explicitly says it is one-off.

In the same change, update:

- `AGENTS.md`
- `skills/value_invest_research/SKILL.md`
- `skills/value_invest_research/frameworks/research_goal_qa.md`
- `skills/value_invest_research/frameworks/domain_playbooks.md` when the change affects domain-specific question depth, metrics, source schemas, or scoring drivers

Future reports must use the latest framework requirement.

## Time-Sliced Prediction Evaluation

Every research run must declare one of two modes before source collection. The default is historical training/backtest mode; use live prediction mode only when the user explicitly asks for current/live/real-time research or otherwise states that the run should not be time-sliced:

- Historical training/backtest mode: the default for new research goals. Set an `as_of_date`, defaulting to three calendar months before the evaluation date/report date unless the user specifies another cutoff. All QA reasoning, source parsing, valuation context, and target ranking must only use information publicly visible on or before `as_of_date`.
- Live prediction mode: used only when the user wants an explicitly current research observation. Use information visible up to the report date. Do not attach a future return label; record the next validation horizon and review trigger instead.

Historical training/backtest mode must prevent look-ahead bias:

- Each L3 source plan records `as_of_date`, `source_visible_at`, and cutoff status.
- Materials visible after `as_of_date` are rejected or quarantined as look-ahead data.
- The current LLM's background knowledge is not evidence. It may help generate hypotheses, but it may not strengthen facts, scores, target ranking, or action state unless the claim is grounded in cutoff-visible source IDs.
- `qa_tree.json` must include `anti_leakage_controls` with the as-of date, cutoff source-pack rule, LLM-prior rule, question-tree rule, supply-chain rule, scoring rule, and label isolation rule.
- Every L3 node must include `backtest_grounding`: `allowed_source_ids`, `model_prior_policy`, `post_cutoff_knowledge_policy`, and `non_source_claims`. `non_source_claims` must be empty for conclusions and scores.
- Price data after `as_of_date` is allowed only after the target list and ranking are frozen, and only for the ex-post label.
- The ex-post label must not change source selection, QA answers, target strength, target rank, score weights, or narrative wording that should have been known as of the cutoff.
- Public backtest reports must read as if written by the system on the `as_of_date`. QA conclusions, target rationale, score explanations, odds models, downgrade triggers, and summary prose must not discuss ex-post winners, losers, realized returns, calibration lessons, or later price action.
- Later price movement may appear only once in the final report: inside an isolated label block or the rightmost label columns of the final target table.

For every target in historical training/backtest mode, attach a label block:

- `as_of_date`
- `evaluation_date`
- `label_window`
- adjusted or total-return price at `as_of_date`
- adjusted or total-return price at `evaluation_date`
- `forward_3m_return`
- benchmark or sector return when available
- excess return when available
- price source
- label status

If price history is incomplete, stale, corporate-action-unadjusted, delisted/suspended, or otherwise unreliable, mark the label as unverified. Do not infer prediction success from an unverified label.

Label availability must not define the target universe. The frozen target list should include the economically relevant securities or assets across exchanges first; if a local/non-US target lacks a verified label, keep it in the list with `label_status: label_unverified_*` instead of replacing it with a convenient US proxy.

## Executable Contract Layer

Use `src/value_invest_research/framework_contracts.py` to turn the written framework into reusable checks and artifacts:

- Report contract validation: verify top-level order, Q1-Q4 hierarchy, L1/L2/L3 rendering, Q4 preservation, final target rollup, source collapse, and canonical card classes.
- BOM-first validation: when a report uses `bom-question-stage-flow`, every `bom-question-card` must include collapsed `bom-question-research-status` before `bom-question-verdict`; every BOM module must include one collapsed `bom-s-curve-stage-card` only after its six child questions, with stage source discipline, current stage, six-question evidence rollup, next confirmation signal, and downgrade signal.
- Industry-overview validation: verify the report includes a standalone `行业概况` section with `industry-overview-section`, five clickable `details.industry-module` cards, `summary.module-head`, `module-index`, `industry-module-body`, `supply-chain-section`, `chain-explain`, `chain-research-bridge`, `chain-node-lens`, `chain-plain-summary`, nested `details.chain-detail-panel`, `chain-lane-map`, `chain-value-flow`, `chain-simple-flow`, `component-value-chain`, `bom-taxonomy`, `bom-taxonomy-grid`, `bom-taxonomy-card`, `chain-layer-grid`, `chain-layer-card`, `chain-relationship-graph`, `chain-stage-panel`, `chain-company-list`, `chain-company-card`, `chain-chokepoints`, `overview-research-unit`, `overview-question-card`, `overview-answer`, `competition-bom-map`, `competition-bom-card`, `competition-question-grid`, `profit-pool-table`, `bottleneck-release-timeline`, `chokepoint-bom-map`, `chokepoint-bom-card`, `chokepoint-question-grid`, `chokepoint-scorecard`, `key-variable-bom-map`, `key-variable-bom-card`, `chain-data-gaps`, `industry-space`, `industry-space-summary`, `space-bom-reasoning`, `space-node-card`, `space-node-reasoning`, `space-node-evidence`, `space-node-space-reasoning`, `space-node-sizing`, `space-method-step`, `space-step-title`, `space-step-index`, `space-public-methods`, `space-method-card-grid`, `space-method-card`, `space-method-card-body`, `space-method-entry`, `space-method-entry-sources`, `space-method-empty`, `space-horizon-conclusion`, `space-horizon-grid`, `space-horizon-card`, `space-node-sizing-table`, `space-step-confidence`, `table-scroll`, `industry-competition`, `industry-chokepoints`, and `industry-key-variables`. It must show the ecosystem map, unified BOM taxonomy, one-to-one BOM coverage across industry space, competition/profit-pool, chokepoints, key variables, and targets, BOM-node space reasoning with ordered `1 公开拆法`, `2 空间结论`, evidence below the reasoning card, BOM-level competition/profit pool, BOM-level chokepoints, and key variables in beginner-readable Chinese without forcing all content to be visible at once. Universe/Exa plans must remain internal and are invalid in public HTML.
- Time-slice audit: reject post-cutoff thesis sources and allow current-time data only as final-target label metadata.
- QA schema validation: require L3 question-quality fields, structured source plan, structured skill dispatch, fact, inference, judgment, gap, trigger, and source links before parent rollup. The validator rejects missing `decision_use`, `support_evidence`, `refute_evidence`, `target_implications`, `score_component`, `minimum_evidence_gate`, `refuting_source_plan`, or undifferentiated fact/inference/judgment.
- Research artifact validation: require L3 parser `schema_fields`, source availability proof, auditable target `score_subcomponents`, deterministic target ranking inputs, and hard kill tests for actionable targets.
- Domain playbooks: start from reusable mechanism buckets such as semiconductor hardware HBM/custom ASIC/foundry/WFE buckets, then adapt to the research object.
- Target scoring: roll score evidence into four core target dimensions, `scarcity_or_monopoly`, `mispricing`, `earnings_elasticity`, and `risk_control`, while preserving the seven auditable score components and score subcomponents underneath.
- Freeze and label: create frozen recommendations first, then attach forward-return labels without changing rank, rationale, score, or odds.
- Training samples and prediction reviews: export machine-readable backtest samples and later review scaffolds so the system can learn from both correct and incorrect calls.
- Internal workbench separation: keep parser outputs, GPT reviews, validator output, rejected future sources, scoring worksheets, freeze metadata, and label attach metadata out of the public HTML unless the user asks to inspect them.
- Public no-changelog separation: keep framework-change notes, upgrade summaries, "what changed in this run" text, mechanism-depth maps, and "本轮如何落实" tables out of public HTML. They may live in workbench JSON, logs, or chat responses only.
- Anti-leakage validation: in historical mode, reject reports where L3 reasoning lacks source-pack grounding, source parsing uses label-only or post-cutoff sources, or target score subcomponents reference unverified reviews, post-cutoff evidence, or label fields.

## L0: Current Research Goal

Answer:

- What exactly is being researched?
- What is the investment relevance?
- What is the time frame?
- What decision boundary applies?
- What is the current constrained judgment?
- What is the biggest uncertainty?

The L0 answer must be short and directional. It should define the research object and prevent premature target selection.

## Research Type Adaptation Layer

Before building Q1-Q4, classify the research type and adapt the QA directions. The QA tree remains the universal shape, but the meaning of each Q direction should fit the research object.

After classifying the type, select or synthesize a domain playbook. The playbook owns concrete L2 mechanism buckets, L3 questions, source plans, parsing schemas, domain metrics, tracking indicators, and threshold rules. The public report contract owns only the hierarchy and display order.

Domain playbooks and the mechanism-depth protocol live in `domain_playbooks.md`. Use that file before evidence collection whenever a topic depends on industry structure, technology adoption, product economics, supply constraints, or valuation rerating.

Default research types:

| Type | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| Industry/theme opportunity | Industry space and demand reality | Competitive landscape and value capture, with chokepoint analysis as a submodule | Disconfirming tests and priced-in risk | Valuation odds and target observation list |
| Single company | Growth drivers | Moat, unit economics, and value capture | Financial quality, valuation, and disconfirming tests | Observation decision and monitoring list |
| Event/policy | Event facts and scope | Transmission mechanism | Beneficiaries, losers, and second-order effects | Disconfirming tests and watchlist |
| Technology/product route | Technical feasibility and adoption demand | Bottlenecks and ecosystem readiness | Commercialization, competition, and disconfirming tests | Exposed assets and monitoring list |
| Target update | What changed | Which thesis node changed | Whether price/risk/reward changed | Update action for observation strength |

For conferences, keynotes, product launches, investor days, and other public events, use the event/conference adaptation unless the user explicitly asks for a different lens:

| Type | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| Event/conference investment opportunity | Official fact boundary and new-information delta | Transmission chain and supply-chain chokepoints | Disconfirming tests and priced-in risk | Specific target observation list and ranking |

This adapter is mandatory for event-driven research. The report is too shallow if it only summarizes what was announced. It must parse official facts versus roadmap/marketing language, identify the incremental assumption change, bridge the event into customer/order/revenue/margin/FCF evidence, test which chokepoints can capture value, check valuation odds, and rank specific securities with monitorable kill tests.

If the topic does not fit a default type, define a custom Q1-Q4 map in the execution plan. Do not force demand/bottleneck/target wording onto company, event, policy, or technology-route questions when it weakens the research.

## Mechanism Depth Protocol

For industry/theme opportunity and technology/product-route research, the QA tree must be detailed enough to reconstruct the investment mechanism, not just describe the theme. Before source collection, create a mechanism-depth map with these blocks unless a block is explicitly irrelevant:

- Demand driver tree: who needs more of the product/service, what workload or customer behavior causes it, and how it decomposes into volume, price, mix, and duration.
- Supply or access response: what constrains capacity, utilization, inventory, lead time, capex, regulation, distribution, trust, data, or ecosystem access.
- Unit economics and profit bridge: how demand reaches revenue, gross margin, operating margin, FCF, capex intensity, and working-capital pressure.
- Competitive value-capture map: which companies/assets capture value at each node and what substitutes, internal builds, or new entrants could bypass them.
- Technology route comparison: compare alternative technical/product routes by cost, power/efficiency, performance, reliability, serviceability, timing, beneficiaries, and substitution/refuting trigger when route choice affects value capture.
- Bottleneck release timeline: for each bottleneck, identify the current constraint, who can expand or release it, expected observation cadence, release evidence, downgrade trigger, and target implication.
- Market-pricing bridge: what current valuation implies about growth, margins, cyclicality, discount rate, or risk premium.
- Disconfirming and counter-supply tests: what evidence would prove the demand, bottleneck, pricing, or scarcity thesis wrong.
- Capital-chain and second-order beneficiaries: whether high returns drive capex, equipment, materials, infrastructure, channel, or downstream opportunities.
- Model and口径 reconciliation: how external models differ by period, unit, currency, revenue/profit/capex scope, and margin definition.

This protocol is a question-quality gate. If the initial L2/L3 tree cannot answer these blocks for a model-heavy industry, rewrite the tree before collecting more sources. A refreshed canonical report is too shallow if its L3 answers are mostly narrative summaries and do not capture the driver tables, assumptions, formulas, or disconfirming metrics needed to rebuild the thesis.

For storage/memory research, use the memory industry playbook in `domain_playbooks.md`. It requires explicit L2/L3 coverage for workload-to-memory demand, demand-supply slope mismatch, product price and unit economics, company value capture, capital return/capex cycle, valuation rerating, counter-supply/substitution, and model口径 reconciliation.

## Research Execution Plan

For every level, explicitly state:

- What questions to ask.
- How to collect information.
- How to connect the information into reasoning.
- How to present the output.

Before evidence collection, state the run mode. In historical training/backtest mode, also state the `as_of_date`, evaluation date, evidence cutoff rule, label window, benchmark choice if any, and the rule that forward-return labels are attached only after recommendations are frozen.

The execution plan is part of the internal workbench output, not the final user-facing HTML by default. It should make the method auditable before the system starts collecting more detail, but the final report should stay research-first and only show the current goal, QA drilldown, final target recommendation, and source index.

Before evidence collection, run two quality-control passes:

1. Question architecture pass
   - Use `investment-question-architect`.
   - Each L3 question must state decision use, materiality, required materials, support evidence, refuting evidence, target implications, preferred specialty skill, score component, and minimum evidence gate.
   - For event/conference topics, force L2 buckets for official fact boundary, new-information delta, event-to-order/revenue/margin bridge, supply-chain chokepoint, company exposure, valuation/priced-in risk, and target ranking. Use `event-to-investment-analysis`, `conference-transcript-analysis`, `supply-chain-chokepoint-analysis`, `company-exposure-analysis`, `valuation-analysis`, and `target-ranking-analysis` as the default skill family.
   - For model-heavy industry/theme research, require a mechanism-depth map before accepting the L2/L3 tree. L2 buckets should represent analytical mechanisms such as demand driver, supply response, unit economics, value capture, valuation/pricing, counter-supply, or second-order beneficiaries.
   - Each L3 question must be tied to a score driver such as future space, chokepoint strength, valuation odds, evidence quality, disconfirming-risk control, monitorability, payoff convexity, target ranking, or action state.
   - Delete or rewrite questions that cannot change a parent conclusion, target strength, valuation odds, or risk controls.

2. Source planning pass
   - Use `research-source-planner`.
   - GPT owns source-universe selection as part of the end-to-end research role. The user provides the research goal and constraints; GPT must classify the domain, choose and combine the right professional universes, decide when to add candidate sources, and record the rationale internally. Do not require the user to know which third-party source, company IR, message, or opinion universe is appropriate.
   - Each L3 question must have a concrete source plan across evidence, research_report, message, and opinion where relevant.
   - Every minimum question inside `行业概况` must also have a concrete `source_universe_plan` and `exa_search_plan` before any answer is written. This applies to `行业空间`, `竞争格局与利润池`, `瓶颈点`, and `关键变量与待验证数据`. The source-universe plan records professional priority sources, directed queries, expected fields, parser skill, selected/gap source IDs, cutoff status, and allowed usage. The Exa plan records the exact query, expected fields, retrieval status, cutoff/quarantine rule, and selected/gap source IDs.
   - For every `行业空间` BOM/subsystem node, the source plan must first create a five-bucket source-search matrix after BOM node identification: `公司指引`, `公司 TAM`, `客户侧指引`, `第三方拆法`, and `财务兑现证据`. This is an active search plan, not a coarse node evidence pool. Every bucket must record search query/terms, `priority_sources` from `config/source_universes.json`, site/domain `directed_queries`, expected fields, source bucket, visible date/cutoff status, allowed usage, preferred parser skill, selected source IDs when found, or `status=gap` with `gap_reason` when no reliable material exists. Every non-empty public-method entry needs its own source IDs and must record scope, period, formula/decomposition, assumptions, output value, source date, and口径 caveat. If no reliable public method is found, mark the node as a data gap; do not create a proprietary TAM estimate to fill the blank.
   - Source parsing must be anchored to the smallest active question. For each L3-L5 unit or BOM-node question, define the question-specific source universe first, then define all dimensions to inspect inside each selected source. A source can satisfy multiple dimensions for the same question; for example, an earnings release may contain company guidance, company TAM references, financial execution evidence, margin/capex clues, and missing product-level gaps. The parser must return found/gap for every requested dimension with facts, scope caveat, verification metrics, and support/refute/lead stance. Do not allow a source to disappear from a dimension merely because it was already used in another bucket.
   - For event/conference topics, the source plan must include official event materials first: agenda/session page, keynote/transcript/replay, official press releases/blogs, partner/customer statements, company filings/earnings calls for exposed targets, and valuation/consensus data. Third-party news can map timing and market reaction, but it cannot upgrade conviction unless confirmed by primary evidence.
   - For mechanism-depth questions, the source plan must name the exact fields needed to fill the model: period, unit/currency, volume, price, mix, capacity, utilization, cost, margin, capex, FCF, valuation multiple, implied expectation, and口径 when relevant.
   - The stored `source_plan` must be structured by concrete source, expected fields, source bucket, visible date/cutoff status, allowed usage, preferred parser skill, and historical-mode `availability_proof` when applicable. A prose-only source plan is insufficient for refreshed canonical reports.
   - Each supporting source plan must have a refuting or boundary-check source plan.
   - The source plan must name the preferred parser skill and whether DeepSeek MCP should do first-pass reading.
   - The source plan must name expected `source_extractions.jsonl` records to create. Each selected concrete source should map to at least one L3 extraction record unless GPT records a direct-parse fallback.
   - In historical training/backtest mode, the source plan must also name the source-visible date, cutoff status, and availability proof for each planned material. Availability proof can be publisher date, filing timestamp, archive timestamp, release page date, or dataset snapshot note; declared dates without proof are not enough for thesis use.

Default QA directions for industry/theme opportunity:

1. Q1: Confirm demand.
2. Q2: Analyze competitive landscape and identify value-capturing chokepoints.
3. Q3: Bind disconfirming tests.
4. Q4: Target observation list with reasons.

For other research types, use the adapted Q1-Q4 map. Each Q direction should state its own sub-plan and then run the corresponding QA subtree.

Industry overview and QA must remain complementary:

- `行业概况` is the map layer. It may show baseline facts, who provides what, who depends on whom, where value/profit flows, candidate chokepoints, key variables, and open questions generated by the map.
- The value-flow part of `行业概况` must start with simple plain-language steps before detailed tables or flow cards. If a term is not self-evident to a new reader, define it in the step itself. For example, "系统交付" means turning chips, memory, storage, network, power, cooling, chassis, rack, and integration work into deployable servers, racks, clusters, or data-center capacity.
- `下钻 QA` is the decision-interrogation layer. It must ask and answer what the overview cannot settle: whether a signal is real, why it converts or fails to convert into financial value, how large the impact is, under what condition the thesis breaks, who wins among comparable companies, what is already priced, and what changes target ranking.
- A QA node is weak if it only repeats an overview table. Each L3-L5 unit must add at least one marginal decision input: source verification, driver calculation, company exposure bridge, contradiction/refutation, valuation/odds judgment, kill test, or target-score effect.
- Q1-Q4 L1 cards should summarize the parent judgment and show the next interrogation focus. Large tables already rendered in `行业概况` should not be re-rendered in L1; if needed, put a new table under the L2/L3 node whose specific question it answers.

## Chokepoint Evaluation Protocol

For industry/theme opportunity and technology/product-route research, the domain playbook must add competitive-landscape analysis before chokepoint evaluation whenever value capture depends on scarce supply, workflow control, proprietary data, distribution, trust, regulation, or another hard-to-bypass constraint.

Chokepoint is a conclusion produced by competitive-landscape analysis, not a synonym for the whole competition module. The Q2 flow is: identify competitors and substitutes in each node, test customer bargaining power and supply expansion, then decide which nodes are true chokepoints. The chokepoint scorecard belongs inside the relevant Q2 competition/value-capture node, usually Q2.1. It must not become a top-level appendix or a component parallel to the QA tree.

Each scorecard must declare a score schema with dimension weights, scoring definitions, and downgrade rules. Do not use unexplained qualitative labels as the only score basis. If one dimension lacks evidence, score it conservatively and list the missing data.

Each chokepoint node should answer:

- Demand flow: what incremental demand reaches this node?
- Irreplaceability: can buyers bypass or substitute this node?
- Supply/access constraint: what scarce capacity, data, trust, distribution, compliance, or ecosystem access controls the node?
- Pricing power: can the node raise price, take rate, margin, or backlog quality?
- Financial conversion: does the bottleneck show up in revenue, gross margin, RPO/backlog, FCF, or capex efficiency?
- Market pricing: is the bottleneck already fully priced in?
- Disconfirming trigger: what data would prove this is not a real bottleneck?

Q4 target observation lists must use Q2 chokepoint evaluation as an input to ranking. A target cannot receive high strength from theme exposure alone; it must reconcile chokepoint score or score drivers with future space, valuation odds, evidence quality, and Q3 downgrade tests.
In historical training/backtest mode, Q4 must retain as-of target-selection child questions. Do not replace Q4's child QA with the final label table, and do not create a Q4 child whose purpose is to evaluate later returns.

## Industry Overview

Every refreshed canonical report must include `行业概况` before `下钻 QA`.

This section is the shared fact map for later reasoning. It must include five public modules:

- `产业链与生态位`: upstream, midstream, downstream layers, key players, what each player provides, who depends on whom, how orders/products/capacity/revenue/margin/ROI flow through the ecosystem, and `component-value-chain` so the reader can see subsystem/BOM, component/service, key companies, input, downstream recipient, financial validation metric, and related QA. Use nested `chain-detail-panel` cards for the swimlane, value-flow, and component/BOM panels. Do not render an extra high-level structured chain table by default.
- `行业空间`: direct BOM-node space reasoning only. Current scale anchors are evidence, not the conclusion. Use `industry-space-summary`, `space-bom-reasoning`, and one collapsed `details.space-node-card` per key BOM/subsystem node. Each node card must use single-column `space-node-reasoning` with `space-node-space-reasoning` first and `space-node-evidence` below it. The 空间推理 block must include `space-node-sizing`, `space-method-step`, `space-step-title`, `space-step-index`, `space-public-methods`, `space-method-card-grid`, `space-method-card`, `space-method-card-body`, `space-method-entry`, `space-method-entry-sources`, `space-method-empty`, `space-horizon-conclusion`, `space-horizon-grid`, `space-horizon-card`, `space-node-sizing-table`, and `space-step-confidence`, and must present `1 公开拆法`, `2 空间结论` in that order. Public-method entries must preserve the fixed fields `公司或机构`, `指引内容`, `BOM 节点`, `时间范围`, `可验证指标`, and `置信度`, then judge `短期`, `中期`, and `长期` space in the final 结论. Do not answer competition, profit-pool ownership, valuation, or target ranking in this module.
- `竞争格局与利润池`: organize by key BOM/subsystem node through `competition-bom-map` and collapsed `competition-bom-card` nodes. For each BOM node answer the fixed question set: `玩家市场份额分布`, `头部玩家优势分析`, `替代玩家赶超希望`, and `格局变化核心变量`. Each fixed question must render as `overview-question-card` with a natural `overview-answer-prose` answer, claim-near blue inline source links, and source chips. `玩家市场份额分布` should prioritize concrete share values and clearly labeled proxy figures over generic judgment. Keep route comparison inside the relevant BOM cards, and keep `profit-pool-table` for company/value-capture rows inside the BOM card.
- `瓶颈点`: organize by the same key BOM/subsystem nodes through `chokepoint-bom-map` and collapsed `chokepoint-bom-card` nodes. For each BOM node answer the fixed question set: concrete constraint, controller, scarcity duration, release/substitution path, score and downgrade rule, and target/monitoring implication. Each fixed question must render as `overview-question-card` with answer and source chips. Keep `chokepoint-scorecard` inside the node and `bottleneck-release-timeline` for release cadence.
- `关键变量与待验证数据`: data gaps and Q1-Q4 nodes that should test each industry-map insight.

Render this as `industry-overview-section` with five clickable `details.industry-module` blocks. Each block has a direct `summary.module-head` with `module-index`, concise title text, `chevron`, and an `industry-module-body` that contains the detailed tables/maps. The `产业链与生态位` block uses `supply-chain-section` with:

- `chain-explain`, `chain-research-bridge`, `chain-node-lens`, and `chain-plain-summary`: a short Chinese explanation of what the chain does, how the research goal becomes a supply-chain problem, and what lens is used to screen nodes.
- `chain-lane-map`, `chain-layer-grid`, and `chain-layer-card`: upstream/midstream/downstream swimlane view.
- `chain-value-flow`: value-flow view showing orders, products, capacity, revenue, margin, and ROI movement.
- `component-value-chain`: BOM/subsystem value chain showing what each node receives, makes, supplies, and how to verify it financially.
- `chain-relationship-graph`, `chain-stage-panel`, `chain-company-list`, and `chain-company-card`: concise company/node lists inside each upstream/midstream/downstream panel.
- `chain-detail-panel`: nested collapsible public panels for the swimlane map, value-flow view, and component/BOM value chain.

The remaining modules use:

- `industry-space`: industry-space sizing model with boundary, driver tree, cutoff-visible scale anchors, and validation data.
- `industry-competition` plus `competition-bom-map`, `competition-bom-card`, `competition-question-grid`, `overview-research-unit`, `overview-question-card`, `overview-answer`, and `profit-pool-table`: BOM-level competition, substitute, customer bargaining, supply response, source-backed answer, and value-capture rows. Inside each BOM card, `competition-question-grid` must be a single-column full-width child-card stack.
- `industry-chokepoints` plus `chokepoint-bom-map`, `chokepoint-bom-card`, `chokepoint-question-grid`, `overview-research-unit`, `overview-question-card`, `overview-answer`, `chokepoint-scorecard`, `chain-chokepoints`, and `bottleneck-release-timeline`: BOM-level bottleneck constraints, controllers, scores, release cadence, source-backed answer, and downgrade rules. Inside each BOM card, `chokepoint-question-grid` must be a single-column full-width child-card stack.
- `industry-key-variables` plus `chain-data-gaps`: key variables and data required before strengthening QA conclusions or target scores.

It is not a process appendix and should not describe framework changes. It is a research artifact that prevents target selection from jumping straight to familiar company names.

### Module 5 → Stage 3 Bridge Protocol

Module 5 (`关键变量与待验证数据`) is the bridge from Stage 2 to Stage 3. It does NOT run new searches. It aggregates every `gap`, `missing_data`, and unresolved variable from Modules 1-4 into a `pending_questions` list.

Each entry in `pending_questions`:

- `gap_source`: which module and sub-unit produced this gap (e.g. "行业空间 / HBM 节点 / 公司指引缺失")
- `variable`: what is unknown (e.g. "HBM3E 2026 ASP 指引")
- `materiality`: why it matters for the investment decision
- `candidate_qa_direction`: which Q1-Q4 direction this should feed into
- `candidate_score_component`: which ranking driver this gap affects

LLM reads `pending_questions` and maps them to L3 questions:

| Gap source | Maps to | Example L3 transformation |
|------------|---------|--------------------------|
| Value flow path unclear (chain) | Q2 competition/value capture | "Which node actually controls profit allocation?" |
| BOM sizing method missing (space) | Q1 demand or Q2 chokepoint | "Can HBM supplier revenue elasticity support current capex?" |
| Substitution path unknown (competition) | Q3 disconfirming | "How quickly can custom ASIC replace NVIDIA general-purpose GPU?" |
| Grid constraint data missing (chokepoint) | Q3 physical risk | "Is US grid interconnection a hard ceiling on AI factory delivery?" |
| Valuation data incomplete (any) | Q3 pricing risk | "What growth assumptions are embedded in current valuation?" |

Do NOT generate L3 questions that do not trace back to at least one `pending_questions` entry or one data gap documented in the industry overview.

## Scarcity-First Opportunity Gate

Scarcity-first opportunity gate is a hard action filter, not a style preference.

The framework's default action state is `no_action`. The research goal is not to find something to recommend in every industry; it is to find a currently underpriced large opportunity.

An opportunity may become `actionable_long` only when the as-of evidence supports all four core target dimensions:

- `scarcity_or_monopoly`: buyers cannot easily bypass, substitute, internally build, or commoditize the company's product/service or chokepoint.
- `mispricing`: current market valuation or implied expectation does not already discount the opportunity.
- `earnings_elasticity`: future demand can create large revenue, margin, cash-flow, operating leverage, or rerating upside.
- `risk_control`: downside, disconfirming evidence, execution, policy, cyclicality, financing, and valuation risk are small enough and monitorable enough.

If any of these four dimensions is weak, missing, stale, or unverified, cap the target score and mark the target `watch_only` or `no_action`. Broad theme exposure, TAM size, news momentum, or management narrative cannot by themselves create a high score. The greatest research effort should go into proving or disproving the scarcity/irreplaceability mechanism and whether the market has already priced it.

Target universe selection must not be driven by label convenience. For industry opportunities, include the actual scarce value-capture vehicles even when they trade outside the US, then attach verified or unverified labels separately after ranking is frozen.

Q4 target observation lists must also include:

- Score breakdown: chokepoint strength, future space, valuation odds, evidence quality, disconfirming-risk control, and monitorability.
- Four core target dimensions: `scarcity_or_monopoly`, `mispricing`, `earnings_elasticity`, and `risk_control`.
- Score audit: auditable `score_subcomponents` for all seven core components, with subdimension name, score, weight, evidence IDs or GPT review IDs, rationale, and status.
- Simplified odds model: implied expectation, base path, bull path, bear path, upgrade/downgrade data, and one compact odds judgment per target.
- Prediction review fields: initial claim, validation horizon, required evidence, current status, and next review trigger.
- Action state: `actionable_long`, `watch_only`, or `no_action`, with gate reasons when not actionable.
- Deterministic rank: sort from frozen score fields by action-state priority, opportunity fit, total score, payoff convexity, thesis confidence, then ticker/name tie-break; do not manually reorder after labels.
- Hard thesis kill tests: any `actionable_long` target must list test, evidence needed, downgrade action, and source plan. If kill tests are missing, cap at `watch_only`.

The simplified odds model is not a price target or trading instruction. If current valuation data is stale, incomplete, or source quality is weak, mark odds as unverified and do not raise target strength. Public HTML must show this model inside `标的推荐` as `target-odds-model` with `target-odds-table`, before the dense target table; Q4 should also summarize the odds gate in its current-conclusion block.

## QA Drilldown

Use adaptive depth up to five layers by default:

- Q1: main adapted research direction.
- Q1.1: mechanism bucket.
- Q1.1.1: investment decision question.
- Q1.1.1.1: optional decomposition unit under the decision question.
- Q1.1.1.1.1: optional atomic work unit for one company, chain node, source, table row, or model row.

Stop at the shallowest layer that gives a sourced, decision-useful answer. Do not force every branch to L5.

Create L4/L5 only when at least one trigger is present:

- the parent L3 covers multiple companies, securities, or supply-chain nodes;
- the answer requires a mapping table, driver tree, financial bridge, valuation model, scorecard, scenario table, or kill-test matrix;
- the source plan spans more than three material classes or parser skills;
- support and refuting evidence apply to different submechanisms and should not be averaged into one judgment;
- the conclusion can only say "needs verification" without a more granular sub-question;
- target ranking, action state, valuation odds, or risk control would change depending on a company-specific or node-specific answer.

Do not put too many unrelated L3 questions under one catch-all L2. L2 should group L3 questions into mechanism buckets selected by the research-type adapter and domain playbook. If an L1 has only one L2 but many L3 questions, split the L2 layer before polishing the report. If one L3 still carries multiple companies/nodes/models, split it into L4/L5.

The report must proceed through the QA tree directly:

- Q1 owns the first adapted research direction. For industry/theme opportunity this is demand analysis.
- Q2 owns the second adapted research direction. For industry/theme opportunity this is competitive-landscape and value-capture analysis; chokepoint scoring is a submodule inside that analysis.
- Q3 owns disconfirming tests, valuation/odds checks, risk triggers, or the adapted third direction.
- Q4 owns target observation tables, monitoring lists, decision updates, or the adapted fourth direction.

Details, scorecards, tables, and jump pages must live inside the QA layer whose question they answer. Do not place them as Q-parallel components or unrelated top-level appendices.

Every QA layer must present information in this order:

1. Current conclusion: the shortest defensible rollup of facts, inference, judgment, and uncertainty.
2. Question expansion: child QA nodes or the tables/cards that directly answer that node.
3. Remaining questions: specific missing data, next evidence to collect, or disconfirming tests.

Parent-level answer artifacts such as `回答呈现`, scorecards,反证清单, target tables, and summary matrices belong under the current-conclusion section, before child QA expansion.

Do not duplicate the same conclusion, child-QA list, or pending-question text in both a generated summary card and the body; use one sequential presentation.

Presentation artifacts are answer formats, not structural peers:

- Bottleneck/chokepoint scorecards belong under the competitive-landscape/value-capture question they answer, usually Q2.1.
- Disconfirming-test lists belong under the risk question they answer, usually Q3.1.
- Target observation tables belong under the target-selection question they answer, usually Q4.1.

Every parent answer must roll up only from child answers and auditable sources.

L3-L5 are research units. Each L3-L5 answer must include:

- Materiality.
- Decision use.
- Support evidence.
- Refuting evidence.
- Target implications.
- Score component.
- Minimum evidence gate.
- Refuting source plan.
- Source plan.
- Skill dispatch trace.
- Fact.
- Inference.
- Judgment.
- Gap.
- Trigger.
- Source links.

`Fact`, `Inference`, and `Judgment` must be meaningfully different fields, not three copies of the same conclusion. `Fact` records source-bound observations; `Inference` explains how those facts answer the leaf question; `Judgment` states how the answer changes the parent conclusion, target strength, action state, valuation odds, or risk control.

An L3-L5 answer must also be structurally sufficient for the question type. If the unit asks "how does X map to Y", "which is tighter", "how does valuation rerate", "which target captures value", or any other mechanism question, the answer needs a concrete answer artifact inside `当前结论呈现`: mapping table, driver table, bridge table, ranking table, scenario table, score table, or kill-test table. The artifact is not a process appendix; it is the actual answer. A fact paragraph plus source chips is insufficient when the reader cannot see how the evidence answers the unit question.

For every L3-L5 research unit:

1. GPT decides which source universe and materials to search or read and why.
2. GPT defines the source priority and extraction schema.
3. GPT classifies the leaf task family and routes it through the specialty skill dispatch layer when useful.
4. DeepSeek MCP or the selected specialty skill carefully processes the selected concrete materials and drafts the first structured answer.
5. Persist each source-parser output as one `source_extractions.jsonl` record.
6. Each parser output must fill `schema_fields` for the unit `extraction_schema`. If the parser returns only a generic note, GPT must either map it into the schema during verification or mark it incomplete.
7. GPT verifies each extraction and writes one `leaf_source_reviews.jsonl` record.
8. The verified draft answer must include fact, inference, preliminary judgment, gap, trigger, source links, and support/refute/lead stance.
9. GPT resolves conflicts, corrects unsupported claims, and writes the final research-unit answer.
10. Parent rollups may only use GPT-verified child answers.

Completion gate: apply `frameworks/research_quality_gate.md` before treating a refreshed report as done. The project must contain a valid `qa_tree.json`, `source_extractions.jsonl`, `leaf_source_reviews.jsonl`, and `investment_workbench.json`. Missing parser records, missing GPT review records, or target scores without auditable subcomponents are hard failures.

Every L3-L5 answer must preserve this dispatch trace:

`skill_dispatch` must be a structured object, not a bare skill name or prose chain. It must contain:

- `task_family`
- `selected_skill`
- `concrete_materials`
- `extraction_schema`
- `source_extraction_ids`
- `leaf_source_review_ids`
- `skill_output_status`
- `fallback_used`
- `gpt_verification_status`

The L3 `source_plan` separately preserves source-level `as_of_date` and `source_visible_at` cutoff status when running historical training/backtest mode.

## Specialty Skill Dispatch

Specialized skills are used for leaf-level processing. They do not replace the QA framework and do not make final investment judgments.

Before running an L3 task, classify it into one or more task families:

| Task family | Preferred skill | Use for | Required output discipline |
|---|---|---|---|
| Question architecture | `investment-question-architect` | Research type classification, Q1-Q4 map, L1/L2/L3 question design | decision-use questions, materiality, support/refute tests, target implications |
| S-curve opportunity research | `s-curve-investment-research` | S 曲线机会、早期指数增长、BOM 需求传导、供需缺口、稀缺节点、标的观察框架 | S 曲线验证、BOM 六问、02 metric 历史、03 市场预期、04 第一性原理评估、target gates |
| Supply-chain panorama | `supply-chain-panorama-explainer` | public `行业概况` explanation before Q1-Q4 | plain Chinese summary, flow steps, layer cards, chokepoints, target/Q2/Q4 links |
| Source planning | `research-source-planner` | Material selection before source reading | source priority, concrete sources/searches, extraction schema, refuting-source plan |
| Financial statement / filing parsing | `financial-statement-analysis` | 10-K, 10-Q, 20-F, annual reports, quarterly reports, earnings releases, segment data, capex, inventory, RPO/backlog, cash-flow quality | normalized financial facts, earnings-quality view, gaps, triggers |
| Valuation / priced-in expectations | `valuation-analysis` | multiples, FCF yield, reverse DCF, peer comparison, valuation sensitivity, margin of safety, market-implied growth/margins | market facts, implied assumptions, scenario table, odds judgment, disconfirming tests |
| Industry report / dataset parsing | `industry-report-analysis` | sell-side reports, industry reports, TAM, supply-demand, price forecasts, competitive maps, third-party datasets | assumptions, methodology, estimates, verification needs, disagreement points |
| News / message parsing | `news-event-analysis` | public news, policy updates, supply-chain reports, product launches, unverified market messages | lead classification, affected hypothesis, verification source, near-term trigger |
| Opinion parsing | `opinion-analysis` | expert views, investor opinions, interviews, conference notes, social posts | argument chain, assumptions, fact/opinion separation, counterquestions |
| Long source reading / first L3 draft | `leaf-research-deepseek` plus DeepSeek MCP | long reports, transcripts, filings, policy documents, expert interviews, extracted passages | source extraction with fact/inference/judgment/gap/trigger |
| Quantitative strategy / backtest | `quant-research-fks` or `quantitative-research` | factors, timing rules, systematic screens, backtests, walk-forward validation | hypothesis, data, implementation, backtest, risk limits |
| HTML/report interface | `frontend-design` | HTML dashboard, report readability, visual hierarchy, sticky metadata, table ergonomics | working HTML/CSS with verification |
| Target observation / recommendation | `target-recommendation-analysis` | Q4 specific securities/assets, strength scoring, future space, valuation odds, catalysts, risks | specific targets, no trading instructions, upgrade/downgrade triggers, required data |

When one leaf question spans multiple task families, chain skills in the natural order instead of forcing a single skill. For example, parse filings or earnings releases with `financial-statement-analysis`, verify the extracted facts, then pass only those verified facts into `valuation-analysis` for implied-expectation work.

If a relevant skill is unavailable, record the intended task family and use the closest auditable fallback: primary-source parsing by GPT, DeepSeek source extraction, or a deterministic local script.

GPT remains responsible for:

- Research type selection.
- Question-tree design.
- Source priority and reliability.
- Verification and conflict resolution.
- Final synthesis, target strength, and user-facing conclusions.

## Information Buckets

Classify every input into one of four buckets:

- evidence: official filings, company releases, papers, exchange documents, primary datasets.
- research_report: sell-side reports, industry reports, expert research writeups.
- opinion: expert comments, investor views, interviews, named personal views.
- message: public news, market reports, unverified claims, rumor-like leads.

For every input, mark whether it supports, refutes, or only leads to further research.

Low-reliability information cannot strengthen a conclusion by itself.

## DeepSeek Delegation

DeepSeek's primary role is source parsing for concrete materials, not final research judgment.

Use DeepSeek for:

- Parsing a single research report, earnings release, annual report, filing, news/message item, transcript, expert interview, or extracted passage.
- Drafting the first L3 answer after GPT selects the materials and defines the extraction schema.
- Source summarization and key-point extraction.
- Initial information-bucket classification.
- Candidate question drafting.

Delegate only after the main model has defined the QA node, source priority, and extraction schema.

Persisted DeepSeek/source-parser workflow:

1. GPT selects one concrete source or a small source bundle for one L3 question and defines the dimension list that matters for that question.
2. DeepSeek MCP reads only that material and returns structured extraction for every requested dimension, not only the first matching evidence bucket.
3. The extraction is written to `source_extractions.jsonl`.
4. GPT verifies the extraction against the original source or source link.
5. GPT writes the verification result to `leaf_source_reviews.jsonl`.
6. Final L3 answers may use only facts marked adopted in the review layer.

If DeepSeek returns an empty response, retry with a smaller source chunk or simpler schema when practical. If GPT falls back to direct parsing, record `parser_status: fallback_gpt_direct_parse` and the reason.

For source parsing, request this structure:

- `source_title`
- `source_bucket`: evidence, research_report, opinion, or message.
- `key_facts`: factual points with numbers, dates, and page/section hints when available.
- `support_refute_or_lead`: support, refute, or lead.
- `affected_qa_node`
- `investment_relevance`
- `uncertainties`
- `follow_up_data`
- `dimension_findings`: when the question has multiple dimensions, one record per requested dimension with bucket/dimension, found_or_gap, facts, scope_caveat, verification_metrics, support_refute_or_lead, and missing_data.

For L3 answer drafting, also request:

- `l3_question`
- `selected_materials`
- `fact`
- `inference`
- `preliminary_judgment`
- `gap`
- `trigger`
- `source_links`

DeepSeek must not produce:

- Final investment judgment.
- Trading instruction.
- Financial conclusion.
- Architecture decision.
- Target strength ranking.
- Source reliability adjudication.
- Unchecked target recommendation.

To avoid truncated MCP output, DeepSeek tasks should stay small and bounded:

- Treat input context and output budget separately. When the DeepSeek MCP server/model supports very large context, do not split a long filing, transcript, report, or coherent source pack merely because it exceeds GPT's comfortable reading window; preserve full source context when source integrity matters, up to the server-supported context limit.
- Use a large `max_tokens` output budget for formal investment source parsing: normally 32000-64000 tokens for long-source extraction, at least 24000 tokens for multi-source L3 drafts, and at least 12000 tokens for ordinary single-source parsing unless the task is intentionally tiny.
- Keep each call narrow by research intent: one complete source or coherent source bundle, one L3 question, one extraction schema.
- Even with a large budget, require compact JSON/table output with explicit limits unless the task explicitly asks for exhaustive extraction.
- If the response is truncated, malformed, empty, or stops mid-field, mark the delegation `incomplete`; do not use it for conclusions. Retry with a smaller chunk or fall back to GPT-verified source parsing.

The main model must verify and synthesize every material conclusion against auditable sources.
The main model remains responsible for source selection, source reliability checks, cross-source conflict resolution, reasoning synthesis, target strength, final report language, and all user-facing conclusions.

## Specific Target Observation List

If the research has investment implications, the final section must map conclusions to specific securities or assets rather than broad directions.

For every target, include:

- Ticker/name.
- Bottleneck or thesis node.
- Reason.
- Strength.
- Future space.
- Current valuation odds or explicit valuation-data gap.
- Required verification data.
- Catalysts.
- Risks.
- Source links.
- Downgrade triggers.
- Monitorability.

In historical training/backtest mode, also include:

- As-of cutoff.
- Evaluation date.
- Label window.
- Forward three-month return.
- Benchmark or sector return when available.
- Excess return when available.
- Price source.
- Label status.

These label fields are evaluation metadata, not investment rationale. Keep them visually separate from score breakdown, odds model, and thesis explanation.

This section is a research observation list, not a buy/sell instruction.

## HTML Presentation

Use Apple-inspired presentation:

- Current locked report contract:
  - Top-level order is exactly `当前研究的问题` -> `行业概况` -> `下钻 QA` -> `标的推荐` -> `来源索引`.
  - `行业概况` is mandatory and must render as `industry-overview-section` with five clickable `details.industry-module` blocks: `产业链与生态位`, `行业空间`, `竞争格局与利润池`, `瓶颈点`, and `关键变量与待验证数据`. It must include `summary.module-head`, `module-index`, `industry-module-body`, `supply-chain-section`, `chain-explain`, `chain-research-bridge`, `chain-node-lens`, `chain-plain-summary`, nested `details.chain-detail-panel`, `chain-lane-map`, `chain-value-flow`, `chain-simple-flow`, `component-value-chain`, `chain-layer-grid`, `chain-layer-card`, `chain-relationship-graph`, `chain-stage-panel`, `chain-company-list`, `chain-company-card`, `chain-chokepoints`, `overview-research-unit`, `overview-question-card`, `overview-answer`, `overview-answer-prose`, `competition-bom-map`, `competition-bom-card`, `competition-question-grid`, `profit-pool-table`, `chokepoint-bom-map`, `chokepoint-bom-card`, `chokepoint-question-grid`, `chokepoint-scorecard`, `key-variable-bom-map`, `key-variable-bom-card`, `chain-data-gaps`, `industry-space`, `industry-space-summary`, `space-bom-reasoning`, `space-node-card`, `space-node-reasoning`, `space-node-evidence`, `space-node-space-reasoning`, `space-node-sizing`, `space-method-step`, `space-step-title`, `space-step-index`, `space-public-methods`, `space-method-card-grid`, `space-method-card`, `space-method-card-body`, `space-method-entry`, `space-method-entry-sources`, `space-method-empty`, `space-horizon-conclusion`, `space-horizon-grid`, `space-horizon-card`, `space-node-sizing-table`, `space-step-confidence`, `table-scroll`, `industry-competition`, `industry-chokepoints`, and `industry-key-variables`.
  - `下钻 QA` preserves the full adapted Q1-Q4 QA tree and must render L3 questions plus any adaptive L4/L5 research units in complete refreshed reports unless the user explicitly asks for a shorter executive version.
  - Q4 remains the auditable as-of target-selection QA node with child questions.
  - `标的推荐` is a standalone presentation rollup, not a replacement for Q4.
  - The hierarchy and format rules in `research_report_contract.md` are validation requirements. A complete refreshed report is invalid if it drops L3, moves Q4 out of `下钻 QA`, duplicates child-question lists beside inline cards, replaces the canonical component family, or adds public process appendices.
  - Four non-drift locks must always hold: hierarchy and format lock, industry-overview lock, backtest time-slice lock, and frontend card-style lock. In backtest mode, only cutoff-visible information can drive source collection, QA reasoning, scoring, odds, and target ranking; the only current-time data allowed in final HTML is the final-target evaluation label.
  - Frontend interaction is locked too: every `qa-card level-1/2/3` must be a clickable `details.qa-card` with `summary`, `qa-count`, and `chevron`, default `open`. Static `article/div.qa-card` cards fail the report contract.
  - In historical training/backtest mode, public prose must read as if written on the `as_of_date`; later price movement appears only once in the isolated final target evaluation fields.
  - Do not add process appendices, execution traces, tool traces, iteration notes, or workbench sections unless explicitly requested.
- White/light-gray surfaces.
- SF-system typography.
- Restrained borders.
- Clean spacing.
- Low-noise cards.
- Blue links for concrete sources.
- In historical training/backtest mode, show the as-of cutoff and information cutoff in the current research goal section. Keep evaluation dates, label windows, benchmark returns, and later price movement out of QA conclusions and rationale. Show later price movement only once inside the final target recommendation table. Do not add a separate top-level backtest section unless the user explicitly asks for it.
- Final HTML must use exactly five top-level sections: `当前研究的问题`, `行业概况`, `下钻 QA`, `标的推荐`, `来源索引`.
- The final target recommendation section must rank specific targets by synthesized win probability and payoff odds, while keeping Q4 as the auditable QA source of the target logic.
- Do not render process metadata, iteration diffs, execution traces, quality-framework explanations, tool/delegation attribution, or workbench appendices in final HTML.
- Preserve full QA depth in the final report; do not replace the QA tree with a compressed Q1-Q4 summary unless the user explicitly requests a brief version.
- Inside every QA card/details node, use a consistent three-part display: `1. 当前结论呈现`, `2. 问题展开（子 QA）`, `3. 待补充的问题`.
- Every visible L3-L5 research-unit card must show a compact `Skill` / `Execution` / `Score Component` / `Decision Use` strip inside `1. 当前结论呈现`. `Skill` is the intended specialty lens; `Execution` is the actual parser/delegation state from `skill_output_status` and `fallback_used`. This makes the question architecture and specialty dispatch visible without rendering the full source-parser trace.
- If child QA nodes are rendered inline as expandable cards, do not also render a separate child-question list with the same titles. The question expansion section should contain either jump links or inline child cards, not both.
- Put answer-presentation artifacts under `当前结论呈现` before child QA expansion.
- Keep source indexes collapsed by default unless the user explicitly asks to inspect sources.
- Use the canonical frontend component family defined in `research_report_contract.md` for refreshed reports: `industry-overview-section`, clickable `details.industry-module`, `summary.module-head`, `module-index`, `industry-module-body`, `supply-chain-section`, `chain-explain`, `chain-research-bridge`, `chain-node-lens`, `chain-plain-summary`, `chain-detail-panel`, `chain-lane-map`, `chain-value-flow`, `chain-simple-flow`, `component-value-chain`, `bom-taxonomy`, `bom-taxonomy-grid`, `bom-taxonomy-card`, `chain-layer-grid`, `chain-layer-card`, `chain-relationship-graph`, `chain-stage-panel`, `chain-company-list`, `chain-company-card`, `chain-chokepoints`, `overview-research-unit`, `overview-question-card`, `overview-answer`, `competition-bom-map`, `competition-bom-card`, `competition-question-grid`, `profit-pool-table`, `chokepoint-bom-map`, `chokepoint-bom-card`, `chokepoint-question-grid`, `chokepoint-scorecard`, `key-variable-bom-map`, `key-variable-bom-card`, `chain-data-gaps`, `industry-space`, `industry-space-summary`, `space-bom-reasoning`, `space-node-card`, `space-node-reasoning`, `space-node-evidence`, `space-node-space-reasoning`, `space-node-sizing`, `space-method-step`, `space-step-title`, `space-step-index`, `space-public-methods`, `space-method-card-grid`, `space-method-card`, `space-method-card-body`, `space-method-entry`, `space-method-entry-sources`, `space-method-empty`, `space-horizon-conclusion`, `space-horizon-grid`, `space-horizon-card`, `space-node-sizing-table`, `space-step-confidence`, `table-scroll`, `industry-competition`, `industry-chokepoints`, and `industry-key-variables`; `qa-card`; `artifact-card`; `target-section` + `target-odds-model` + `target-odds-table` + `target-table`; and one collapsed `source-collapse`. Do not introduce visually divergent component families unless the user explicitly asks for a frontend redesign. For every BOM card, child method/question cards must use single-column full-width stacks through `space-method-card-grid`, `competition-question-grid`, and `chokepoint-question-grid`.
- `target-table` action-state cells must keep the matching canonical color class: `state-actionable_long`, `state-watch_only`, or `state-no_action`. Plain action-state text without the class is format drift.
- Additive-iteration lock: framework changes are additive by default. New sections, fields, dimensions, skills, source schemas, or visual affordances must preserve existing public section order, canonical component classes, QA interactions, action-state color classes, target-table structure, source-collapse behavior, and no-changelog rules unless the user explicitly asks for a frontend/report redesign.
- Before marking a framework iteration complete, run regression checks on a new/refreshed report and one existing canonical report or fixture: `validate-report-contract`, `validate-research-artifacts` when artifacts exist, and a browser or DOM smoke check for QA card collapse plus action-state color classes when target states appear.
- Render QA cards as `details.qa-card > summary` so users can click card headers to collapse or expand the QA tree. Preserve the `qa-count` and `chevron` affordances in every generated report.

Default page order:

1. Current research goal.
2. Supply-chain panorama.
3. Question drilldown: Q1-Q4 as top-level QA cards, with all scorecards, risk tests, target tables, and supporting details nested under the relevant question.
4. Final target recommendation, synthesized from Q1-Q4.
5. Source index, collapsed by default.
