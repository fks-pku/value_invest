# Research Report Contract

This contract defines the locked default final report structure for all future investment research outputs unless the user explicitly asks to iterate on the framework.

The public report contract is a presentation boundary, not a domain-question template. New or refreshed reports should be assembled as `ResearchProjectRepository -> ReportViewModel -> CanonicalReportRenderer`. Domain-specific questions, source schemas, metrics, and tracking thresholds belong in playbooks and QA artifacts before rendering.

## Locked Current Contract

The current locked contract is:

- Top-level order is exactly `当前研究的问题` -> `行业概况` -> `下钻 QA` -> `标的推荐` -> `来源索引`.
- `当前研究的问题` must include a compact `constraint-definition` card for industry/theme and technology-route reports: theme boundary, precise bottleneck/constraint, why now, scope, route conflict, and validation horizon.
- Current effective priority is S-curve discovery. The first-pass report should spend roughly 80% of research effort on `S曲线与产业空间`: new-technology prospect, feasibility, future industry space, adoption inflection, and whether the trend is becoming irreversible. BOM is a presentation map in this pass: explain upstream/midstream/downstream, who is on the chain, what each company/node receives, what it produces, and whom it supplies. `竞争格局与利润池` and `瓶颈点` are optional follow-up modules, not mandatory first-pass modules.
- `行业概况` is a standalone pre-QA analytical layer, not a process appendix. It must contain five public modules in this order: `产业链与生态位`, `行业空间`, `竞争格局与利润池`, `瓶颈点`, and `关键变量与待验证数据`. Each module must render as a clickable collapsed `details.industry-module > summary.module-head` card with `module-index`, `chevron`, and `industry-module-body`. The `产业链与生态位` module must keep the important chain information: a lane/swimlane view by upstream/midstream/downstream, a value-flow view showing how demand, orders, products, capacity, revenue, margin, and ROI move through the ecosystem, and a `component-value-chain` table that decomposes the system into BOM/subsystem, component/service, key companies, input, downstream recipient, financial validation metric, and QA link. These three long chain components must render as nested clickable `details.chain-detail-panel` cards, and public reports should not render a separate high-level chain overview table by default. The `行业空间` module must stay scoped to direct BOM-node space reasoning only: current scale anchors are evidence, while the module answers which BOM/subsystem nodes future demand may expand and why. It must render `industry-space-summary` plus `space-bom-reasoning`; each key BOM/subsystem node must be a collapsed `details.space-node-card` with a single-column `space-node-reasoning` body: `space-node-space-reasoning` / 空间推理 first, then `space-node-evidence` / 证据 underneath. Do not render separate `space-node-risk` or `space-node-conclusion` cards inside industry-space nodes. The `space-node-space-reasoning` block must include `space-node-sizing`, `space-method-step`, `space-step-title`, `space-step-index`, `space-public-methods`, `space-method-card-grid`, `space-method-card`, `space-method-card-body`, `space-method-entry`, `space-method-entry-sources`, `space-method-empty`, `space-horizon-conclusion`, `space-horizon-grid`, `space-horizon-card`, `space-node-sizing-table`, and `space-step-confidence` to show the ordered sequence `1 公开拆法`, `2 空间结论`, plus source chips and confidence. Public sizing methods must be traced to cutoff-visible company guidance, company TAM, customer-side guidance, third-party sizing, financial execution evidence, sell-side excerpts, investor presentations, or reputable public research. The public-method area must render five fixed full-width method cards stacked vertically in order: `公司指引`, `公司 TAM`, `客户侧指引`, `第三方拆法`, and `财务兑现证据`. These cards must come from an active five-bucket source-search matrix for every BOM node, not from loose matching against a coarse evidence pool. The source-search matrix must include domain-specific `priority_sources` and site/domain `directed_queries` from `config/source_universes.json`; broad keyword search alone is contract-invalid for refreshed reports. Each method card should keep source type and count on the left, and list available entries on the right with `公司或机构`, `指引内容`, `BOM 节点`, `时间范围`, `可验证指标`, and `置信度`; every non-empty entry must have entry-level `sourceIds`/`source_plan` and visible `space-method-entry-sources` source chips. A coarse BOM-node evidence pool may supplement the node but cannot support an individual entry by implication. Missing classes must remain visible as searched `gap`/`待补` gaps with a reason, not hidden or silently filled. GPT may summarize public methods and judge 短期、中期、长期 space from the five evidence classes, but must not create a proprietary precision TAM when public methods are missing. It must not answer competition, profit-pool ownership, valuation, or target ranking.
- Industry-overview research-unit protocol: every analytical module inside `行业概况` must decompose into research units and minimum questions. For each minimum question, the report artifact must carry a `source_universe_plan` and an `exa_search_plan` before writing the answer. The source-universe plan chooses professional sources from `config/source_universes.json` plus justified additions; the Exa plan defines the direct query, expected fields, cutoff policy, retrieval status, and gap rule. Selected materials must be parsed against the question dimensions, normally by DeepSeek for long materials, and verified by GPT before synthesis. Public HTML must not render Universe/Exa search plans or their raw query text. Public cards show `overview-research-unit`, `overview-question-card`, `overview-answer`, source chips, and either natural `overview-answer-prose` paragraphs or structured `overview-answer-structured` / `overview-answer-row` blocks when a module explicitly needs row labels. Inline source links must be claim-near: place the blue link beside the specific number, fact, or inference it supports instead of clustering all sources at the end of a long paragraph. Source chips are an audit index, not a substitute for claim-level citation, and should only show the current card's actually cited or explicitly attached source IDs rather than a broad BOM-node source pool. In backtest mode, both universe-selected materials and Exa hits must be cutoff-visible before they can support the answer; post-cutoff hits are quarantine-only. This protocol applies to `竞争格局与利润池`, `瓶颈点`, and `关键变量与待验证数据` as well as to `行业空间`.
- `竞争格局与利润池` must organize only by BOM/subsystem node with `competition-bom-map`, collapsed `competition-bom-card` nodes, `competition-question-grid`, `overview-research-unit`, `overview-question-card`, `overview-answer`, `overview-answer-prose`, and `profit-pool-table`. Every BOM node must use four fixed competition question cards: `玩家市场份额分布`, `头部玩家优势分析`, `替代玩家赶超希望`, and `格局变化核心变量`. Each card answers a minimum question as natural analysis paragraphs with claim-near blue inline links for cited sources; it must not use the generic `当前判断` / `关键事实` / `推理链` row template. `玩家市场份额分布` must give concrete public share/distribution values when a reliable comparable source exists; if no exact share table exists, it must explicitly state the comparable-source gap and label any proxy values. `profit-pool-table` then summarizes which companies can keep revenue, gross margin, cash flow, or valuation elasticity at that node. Public reports must not render a separate technology-route matrix table in this module; route comparison belongs inside the relevant BOM node cards or internal workbench artifacts.
- Inside every BOM card, child method/question cards must render as a single-column full-width stack, not side-by-side. This rule applies at minimum to `space-method-card-grid`, `competition-question-grid`, and `chokepoint-question-grid`; each must use `grid-template-columns: 1fr` so the reader reviews `玩家市场份额分布`, `头部玩家优势分析`, `替代玩家赶超希望`, `格局变化核心变量` and similar lenses one card at a time.
- `瓶颈点` must organize by BOM/subsystem node with `chokepoint-bom-map`, collapsed `chokepoint-bom-card` nodes, single-column full-width `chokepoint-question-grid`, `overview-research-unit`, `overview-question-card`, `overview-answer`, `chokepoint-scorecard`, and `bottleneck-release-timeline`. The timeline names the current constraint, release/expansion signal, observation cadence, downgrade trigger, and target implication, and every row should map back to a BOM node.
- Unified BOM taxonomy: `产业链与生态位` must define a visible BOM registry through `bom-taxonomy`, `bom-taxonomy-grid`, and `bom-taxonomy-card`. This registry is the public primary key for industry overview modules. The same public BOM node names must be reused and expanded one-to-one by `行业空间`, `竞争格局与利润池`, `瓶颈点`, `关键变量与待验证数据`, QA artifacts, and `标的推荐` target mapping. Missing any BOM taxonomy node in a later public module is contract-invalid. Source-level fields may retain narrower wording from filings, calls, or reports; public node labels cannot drift across modules. Demand/customer capex may be shown as a supplementary demand-validation layer, but not as a BOM node and cannot replace any BOM-node card.
- `下钻 QA` must preserve the full adapted Q1-Q4 QA tree. Complete refreshed reports must render L3 questions and any available adaptive L4/L5 drilldown units, not stop at L2 summaries, unless the user explicitly asks for a shorter executive version.
- Maximum public/internal QA depth is five. L1 is the adapted research direction, L2 is the mechanism bucket, L3 is the investment decision question, and L4/L5 are optional deeper workbench/research units used only when needed. Do not force all branches to reach L5.
- Q4 remains the auditable as-of target-selection QA node and must keep child questions when the research has target implications.
- `标的推荐` is a standalone presentation rollup, not a replacement for Q4. It synthesizes the QA tree into a ranked target table, and must include `target-profit-bridge` plus `target-valuation-table` before the odds model for opportunity reports with target recommendations.
- In historical training/backtest mode, public report prose must read as if written on the `as_of_date`. Later price movement appears only once, as isolated evaluation columns or one adjacent label block in `标的推荐`.
- The report must not add process appendices, execution traces, tool traces, iteration notes, or workbench sections unless the user explicitly asks for them.
- The report must not add change logs, upgrade logs, "本轮/本次升级", "本轮/本次更新", "本轮如何落实", mechanism-depth checklists, framework explanations, or meta explanations of what changed in the framework. Framework changes must be visible only through better QA, evidence, scoring, and target reasoning.

## Non-Drift Locks

These six areas are locked requirements for all future reports and refreshed reports. Do not relax, reinterpret, or silently replace them in generated reports, templates, prompts, or renderer code:

1. Hierarchy and format lock: final reports must keep the exact public order `当前研究的问题` -> `行业概况` -> `下钻 QA` -> `标的推荐` -> `来源索引`; `下钻 QA` must render the full adapted Q1-Q4 tree through L1/L2/L3 and any adaptive L4/L5 units when they exist; every QA card must use the same three-block body order.
2. Backtest time-slice lock: historical training/backtest mode uses only information visible at the frozen cutoff, normally three calendar months before the evaluation/report date unless the user specifies a different horizon. Source collection, source parsing, QA reasoning, target ranking, score fields, odds models, and rationale must not use any post-cutoff information. The only current-time data allowed in the public report is the final-target evaluation label, rendered once in `标的推荐`.
3. Frontend card-style lock: refreshed canonical reports must use the shared Apple-inspired card system and canonical component family. QA cards must remain clickable/collapsible through `details.qa-card > summary` with `qa-count` and `chevron`, default `open`. Industry-overview modules must remain clickable/collapsible through `details.industry-module > summary.module-head` with `module-index`, `chevron`, and `industry-module-body`, default collapsed to prevent long pre-QA sections from overwhelming the report. Do not introduce a parallel public layout, alternate card family, static QA card wrapper, static industry-overview wrapper, per-target card deck, source-bucket layout, process appendix layout, or redesigned visual system unless the user explicitly asks for a frontend redesign.
4. Public no-changelog lock: refreshed canonical reports must not render process/change-log content such as "本轮升级", "本次更新", "本轮新增", "机制深度映射", "本轮如何落实", "what changed in this run", execution/tool traces, or workbench/process explanations. These are internal artifacts unless the user explicitly asks to inspect process.
5. Industry-overview lock: final reports must include `行业概况` as a public top-level section before `下钻 QA`. This section must use `industry-overview-section` and five clickable `details.industry-module` cards, and must render: `产业链与生态位` with `supply-chain-section`, `chain-explain`, `chain-research-bridge`, `chain-node-lens`, `chain-plain-summary`, nested `details.chain-detail-panel`, `chain-lane-map`, `chain-value-flow`, `chain-simple-flow`, `component-value-chain`, `bom-taxonomy`, `bom-taxonomy-grid`, `bom-taxonomy-card`, `chain-layer-grid`, `chain-layer-card`, `chain-relationship-graph`, `chain-stage-panel`, `chain-company-list`, and `chain-company-card`; `行业空间` with `industry-space`, `industry-space-summary`, `space-bom-reasoning`, `space-node-card`, `space-node-reasoning`, `space-node-evidence`, `space-node-space-reasoning`, `space-node-sizing`, `space-method-step`, `space-step-title`, `space-step-index`, `space-public-methods`, single-column full-width `space-method-card-grid`, `space-method-card`, `space-method-card-body`, `space-method-entry`, `space-method-entry-sources`, `space-method-empty`, `space-horizon-conclusion`, `space-horizon-grid`, `space-horizon-card`, `space-node-sizing-table`, and `space-step-confidence`; `竞争格局与利润池` with `industry-competition`, `competition-bom-map`, `competition-bom-card`, single-column full-width `competition-question-grid`, `overview-research-unit`, `overview-question-card`, `overview-answer`, `overview-answer-prose`, and `profit-pool-table`; `瓶颈点` with `industry-chokepoints`, `chain-chokepoints`, `chokepoint-bom-map`, `chokepoint-bom-card`, single-column full-width `chokepoint-question-grid`, `overview-research-unit`, `overview-question-card`, `overview-answer`, `chokepoint-scorecard`, and `bottleneck-release-timeline`; and `关键变量与待验证数据` with `industry-key-variables`, `key-variable-bom-map`, `key-variable-bom-card`, and `chain-data-gaps`. `行业空间`, `竞争格局与利润池`, `瓶颈点`, `关键变量与待验证数据`, and `标的推荐` must each cover every BOM node defined in the `产业链与生态位` taxonomy. It is the fact-map input to Q1-Q4, not decorative background. Wide tables and dense card tables must use `table-scroll` horizontal overflow handling. BOM child cards must stay single-column and full-width through `space-method-card-grid`, `competition-question-grid`, and `chokepoint-question-grid`.
6. Additive-iteration lock: framework iteration is additive by default. New sections, fields, dimensions, skills, source schemas, or visual affordances may be added only after preserving all existing public section order, canonical component classes, QA interactions, action-state colors, source-collapse behavior, target-table structure, and no-changelog constraints. Removing, renaming, restyling, or replacing any existing public contract element requires an explicit user request for a frontend/report redesign.

Before marking any framework iteration complete, run a regression contract check on at least one newly generated/refreshed report and one existing canonical fixture or sample report. The check must include `validate-report-contract`, `validate-research-artifacts` when artifacts exist, and a browser or DOM smoke check for collapsible QA cards and action-state color classes. A framework iteration is incomplete if a newly added feature passes but an older locked behavior drifts.

Executable enforcement lives in `src/value_invest_research/framework_contracts.py`. Use it to validate report HTML, QA tree schema, time-sliced sources, target score separation, frozen recommendation integrity, label attachment, training samples, prediction reviews, internal workbench separation, and domain playbook selection.

In addition to the public presentation locks, refreshed canonical reports must pass the internal QA professionalism lock. Every L3-L5 research-unit record is invalid if it lacks `decision_use`, `materiality`, `support_evidence`, `refute_evidence`, `target_implications`, `score_component`, `minimum_evidence_gate`, `refuting_source_plan`, structured `source_plan`, structured `skill_dispatch`, differentiated `fact`/`inference`/`judgment`, `gap`, `trigger`, and `source_links`. In historical mode, the structured `source_plan` must also carry source-visible date, cutoff status, and availability proof.

## Top-Level HTML Contract

Final user-facing HTML reports must use exactly these five top-level sections, in this order:

1. `当前研究的问题`
2. `行业概况`
3. `下钻 QA`
4. `标的推荐`
5. `来源索引`

Do not add top-level process sections such as execution plan, quality framework, tool trace, iteration notes, workbench appendix, or full report appendix unless the user explicitly asks to inspect process.

Do not add in-section process or change-log blocks either. A block inside `当前研究的问题`, a QA card, or `标的推荐` is still contract-invalid if it explains what the framework upgraded, what changed in this run, how a mechanism-depth checklist was implemented, or which internal process produced the report.

## Strict Rendering Invariants

Treat a generated report as contract-invalid if any of these invariants fail:

1. The final HTML has exactly five public top-level sections, in this order: `当前研究的问题`, `行业概况`, `下钻 QA`, `标的推荐`, `来源索引`.
2. `行业概况` renders as `industry-overview-section` with five clickable `details.industry-module` blocks: `产业链与生态位`, `行业空间`, `竞争格局与利润池`, `瓶颈点`, and `关键变量与待验证数据`. Each module uses `summary.module-head`, `module-index`, `chevron`, and `industry-module-body`; static always-expanded `section.industry-module` blocks are contract-invalid. The chain module body must include a readable swimlane/lane map, value-flow view, and `component-value-chain` before the QA tree begins.
3. `下钻 QA` renders Q1-Q4 as `qa-card level-1` cards. Q nodes must not appear as loose top-level sections outside `下钻 QA`.
3. Each L1 renders its available L2 children as `qa-card level-2` cards, grouped by meaningful mechanism bucket rather than by generic summary labels.
4. Complete refreshed reports render every available L3 question and adaptive L4/L5 research unit as `qa-card level-3`, `qa-card level-4`, or `qa-card level-5`. A report may omit L3 only when the source QA tree truly has no L3 leaves or the user explicitly requested a shorter executive version.
5. Every `qa-card level-1` through `qa-card level-5` uses the same three-block body order: `1. 当前结论呈现`, `2. 问题展开（子 QA）`, `3. 待补充的问题`.
6. Every QA card must be an interactive `details.qa-card` element with a direct `summary` header, `qa-count`, and `chevron`, opened by default. Static `article.qa-card`, `div.qa-card`, or non-clickable wrappers are contract-invalid even if hierarchy classes are present.
7. Parent-level artifacts such as scorecards, risk matrices, answer tables, and target-selection tables render inside `1. 当前结论呈现` of the QA node they answer, before child QA expansion.
8. `2. 问题展开（子 QA）` contains either inline child `qa-card` nodes or jump links, not both. Do not duplicate the same child titles in both a summary list and rendered child cards.
9. Q4 remains inside `下钻 QA` as the auditable target-selection QA node and keeps its L2/L3 children. The standalone `标的推荐` section must never erase, replace, rename, or move Q4.
10. `标的推荐` renders as one `target-section` with `target-profit-bridge`, `target-valuation-table`, a `target-odds-model`, `target-odds-table`, and dense `target-table` by default. It is a synthesized rollup from Q1-Q4, not an extra QA node and not a process appendix.
11. `来源索引` renders as one collapsed `source-collapse` by default. Source details may expand inside it, but they must not create additional top-level sections.
12. Refreshed canonical reports must use the shared component family: `hero`, `top-nav`, `goal-card`, `constraint-definition`, `industry-overview-section`, `industry-module`, `module-head`, `module-index`, `industry-module-body`, `supply-chain-section`, `chain-explain`, `chain-research-bridge`, `chain-node-lens`, `chain-plain-summary`, `chain-detail-panel`, `chain-lane-map`, `chain-value-flow`, `chain-simple-flow`, `component-value-chain`, `bom-taxonomy`, `bom-taxonomy-grid`, `bom-taxonomy-card`, `chain-layer-grid`, `chain-layer-card`, `chain-relationship-graph`, `chain-stage-panel`, `chain-company-list`, `chain-company-card`, `chain-chokepoints`, `overview-research-unit`, `overview-question-card`, `overview-answer`, `overview-answer-prose`, `overview-answer-structured`, `overview-answer-row`, `competition-bom-map`, `competition-bom-card`, `competition-question-grid`, `profit-pool-table`, `bottleneck-release-timeline`, `chokepoint-bom-map`, `chokepoint-bom-card`, `chokepoint-question-grid`, `chokepoint-scorecard`, `key-variable-bom-map`, `key-variable-bom-card`, `chain-data-gaps`, `industry-space`, `industry-space-summary`, `space-bom-reasoning`, `space-node-card`, `space-node-reasoning`, `space-node-evidence`, `space-node-space-reasoning`, `space-node-sizing`, `space-method-step`, `space-step-title`, `space-step-index`, `space-public-methods`, `space-method-card-grid`, `space-method-card`, `space-method-card-body`, `space-method-entry`, `space-method-entry-sources`, `space-method-empty`, `space-horizon-conclusion`, `space-horizon-grid`, `space-horizon-card`, `space-node-sizing-table`, `space-step-confidence`, `table-scroll`, `industry-competition`, `industry-chokepoints`, `industry-key-variables`, `qa-card level-1`, `qa-card level-2`, `qa-card level-3`, optional `qa-card level-4`, optional `qa-card level-5`, `qa-body`, `qa-block`, `block-title`, `artifact-card`, `target-section`, `target-profit-bridge`, `target-valuation-table`, `target-odds-model`, `target-odds-table`, `target-table`, and `source-collapse`. Do not introduce alternate public component families unless the user explicitly asks for a frontend redesign.
13. Target-table `action_state` cells must render with the canonical status color classes: `state-actionable_long`, `state-watch_only`, or `state-no_action`. Plain uncolored action-state text is contract drift.
14. Historical training/backtest labels are evaluation fields only. They may appear once in the isolated label area of `标的推荐`, never inside QA conclusion prose or Q4 child logic.
15. Every visible L3-L5 research-unit card must include a compact professional-routing strip with selected `Skill`, actual `Execution` status, `Score Component`, and `Decision Use`. `Skill` is the intended specialty lens; `Execution` must come from `skill_output_status` and `fallback_used`, so a selected skill cannot be mistaken for a completed parser run. Full parser traces still belong in internal files unless explicitly requested.

## Time-Sliced Evaluation Contract

Final reports must declare the run mode in the current research goal section. Historical training/backtest is the default mode for refreshed research reports; live prediction is valid only when the user explicitly asks for current/live/real-time research or a non-time-sliced run:

- Historical training/backtest mode: show `as_of_date` and information cutoff in the current research goal section. The QA drilldown and target rationale must be written only from information publicly visible on or before `as_of_date`.
- Live prediction mode: show report date, evidence freshness, validation horizon, and next review trigger. Do not show future return labels.

Historical training/backtest reports may use post-cutoff price data only as an ex-post target label after the recommendation list is frozen. Public backtest reports must read as if written by the system on the `as_of_date`: QA conclusions, target rationale, score explanations, odds models, downgrade triggers, and summary prose must not mention ex-post winners, losers, realized returns, calibration lessons, or later price action. Show later price movement only once, visually separated from rationale and score fields, so readers can distinguish as-of prediction evidence from later outcome measurement.

Label availability must not define the investment universe. The frozen target list must start from economically relevant securities or assets across exchanges. If a local/non-US target lacks a verified price label, keep it in the target table and mark the label as `label_unverified_*`; do not replace the target with a convenient US/Nasdaq proxy or omit it from Q4.

The time-slice rule is asymmetric by design:

- Allowed before the frozen recommendation: only source materials, filings, reports, messages, prices, and market context visible on or before `as_of_date`.
- Forbidden before the frozen recommendation: post-cutoff facts, later price action, later revisions, later analyst reports, current knowledge about winners/losers, and any wording that explains the as-of thesis using post-cutoff outcomes.
- Model-time leakage rule: the current LLM's background knowledge is not evidence. Historical reports must be grounded in a cutoff source pack. Framework/playbook and supply-chain priors may structure hypotheses, but scored conclusions require cutoff-visible source IDs or GPT-verified leaf review IDs.
- Allowed after the frozen recommendation: one current-time label dataset for the final targets only, normally measuring the forward three-month price change from the as-of price date to the evaluation price date.
- Required separation: the label must be stored and rendered as evaluation metadata, not as evidence, score input, odds input, source material, or target-rationale text.

Historical project artifacts must include an internal anti-leakage declaration, but final HTML should stay research-first. Store `anti_leakage_controls` in `qa_tree.json` and `backtest_grounding` on each L3 node. The public page should show the as-of cutoff and label fields, not an execution appendix, unless the user explicitly asks to inspect process.

## QA Hierarchy Contract

The default QA hierarchy is adaptive with maximum depth five:

- `L1`: top-level adapted research direction, normally Q1-Q4.
- `L2`: mechanism bucket selected by the research-type adapter and domain playbook. L2 must group L3 questions by meaningful analytical mechanism.
- `L3`: investment decision question. It should be able to change a parent conclusion, score component, target rank, action state, valuation odds, or risk control.
- `L4`: optional decomposition unit under an L3 when the L3 spans multiple companies, supply-chain nodes, financial bridges, valuation cases, or source families.
- `L5`: optional atomic work unit for one company/node/source/model row when L4 is still too broad. L5 is the maximum depth; if more depth seems necessary, rewrite the higher-level question instead of creating L6.

L2 must not be a single catch-all wrapper under each L1 when many unrelated L3 questions exist. Split L2 by the analytical mechanisms that matter for the selected research object.

Adaptive drilldown triggers:

- the parent question covers multiple companies, securities, or value-chain nodes;
- the answer requires a mapping table, driver tree, financial bridge, valuation model, scorecard, scenario table, or kill-test matrix;
- the source plan spans more than three material classes or parser skills;
- the conclusion can only say "needs verification" without a more granular sub-question;
- support and refuting evidence apply to different submechanisms and should not be averaged into one judgment;
- target ranking would change depending on a company-specific or node-specific answer.

Do not create L4/L5 for cosmetic completeness. Stop at the shallowest level that gives a sourced, decision-useful answer.

The shared contract defines hierarchy and presentation only. It does not hard-code domain questions, metrics, parsing methods, tracking indicators, or thresholds.

However, refreshed canonical reports are not allowed to use generic L2 buckets when a domain requires a concrete mechanism model. The selected domain playbook must create L2/L3 coverage for the relevant mechanism-depth blocks: demand driver tree, supply/access response, unit economics/profit bridge, competitive value-capture map, market-pricing bridge, disconfirming/counter-supply tests, capital-chain or second-order beneficiaries, and model/口径 reconciliation. These blocks belong inside the QA hierarchy, not in a top-level process appendix.

When a domain playbook uses bottleneck or chokepoint analysis, the scorecard must live inside the relevant Q2 competitive-landscape/value-capture QA node, not in a top-level appendix. Chokepoint is a conclusion produced by competition analysis: first compare competitors, substitutes, customer bargaining power, supply expansion, and pricing power; then decide which nodes are true chokepoints. The final target recommendation must explicitly use the chokepoint score or score drivers together with future space, valuation odds, evidence quality, and disconfirming-risk control.

Chokepoint scorecards must declare their score schema. Final target recommendations must show a compact score breakdown and simplified odds model when the report has investment implications. Prediction review fields can be summarized in Q3/Q4 and stored in workbench JSON.

The compact score breakdown is not just display text. Refreshed canonical reports must preserve auditable `score_subcomponents` for all seven core components: `chokepoint_strength`, `future_space`, `valuation_odds`, `evidence_quality`, `disconfirming_risk_control`, `monitorability`, and `payoff_convexity`. Each subcomponent row must include subdimension name, score, weight, evidence IDs or GPT review IDs, rationale, and status.

The public target score must roll these components into four core target dimensions:

- `scarcity_or_monopoly`: whether the company provides a scarce, monopolistic, hard-to-substitute product/service or chokepoint.
- `mispricing`: whether current market valuation has not fully priced the future growth and profit path; this carries the earlier market underpricing test.
- `earnings_elasticity`: whether large future demand can create large revenue, margin, cash-flow, or multiple-revaluation upside.
- `risk_control`: whether downside, disconfirming evidence, execution, policy, cyclical, and valuation risks are small enough and monitorable enough to support a high win probability.

These four core target dimensions are the primary display and action-state gate. The seven component scores are the auditable substructure under them. A target cannot become `actionable_long` unless all four dimensions are sufficiently strong; high theme exposure alone must remain `watch_only` or `no_action`.
`scarcity_or_monopoly` keeps the earlier irreplaceability/scarcity requirement but makes it more explicit about chokepoints, monopoly-like control, and substitution barriers.

## Adaptive Domain Layer

Before evidence collection, the research system must:

1. Classify the research type.
2. Select or synthesize a domain playbook.
3. Generate the concrete supply-chain map with `supply-chain-panorama-explainer`, then generate L1/L2/L3 questions from that playbook.

Domain playbooks own:

- domain-specific question templates
- source plans and preferred source types
- parsing schemas for filings, research reports, news, opinion, or datasets
- metrics, tracking indicators, and threshold design
- source-to-question mapping rules
- target implication logic
- supply-chain map schema: upstream, midstream, downstream, key players/nodes, products/services, dependency links, bottleneck strength, value/profit flow, candidate chokepoints, Chinese plain summary, key-node cards, key data gaps, and target/Q2/Q4 links. More detailed relationship edges and value/order flow can stay internal.
- mechanism-depth maps that specify the driver tables, formulas, units, periods, and口径 needed to make the research as detailed as a professional model-driven report

Examples may appear inside domain playbooks or research-type adapters, not inside this public report contract.

Inside every QA card, use this display order:

1. `当前结论呈现`
2. `问题展开（子 QA）`
3. `待补充的问题`

If child QA nodes are rendered inline as expandable cards, do not also render a separate child-question list with the same titles.

## Final Target Recommendation Contract

When the research has investment implications, add a standalone `标的推荐` section after `下钻 QA`.

The standalone `标的推荐` section is a presentation rollup, not a replacement for Q4. Q4 must remain inside `下钻 QA` as the auditable as-of target-selection QA node with child questions. In historical training/backtest mode, do not create a Q4 child whose purpose is to evaluate later returns; later price movement belongs only in the isolated label area of the final target table.

This section must synthesize all QA evidence into a ranked observation list. It must include:

- ranking
- specific ticker/name
- target class
- chokepoint or thesis node
- chokepoint score or score drivers when bottleneck analysis is used
- win probability
- payoff odds
- strength
- four core target dimensions: scarcity_or_monopoly, mispricing, earnings_elasticity, and risk_control
- compact score breakdown
- auditable score subcomponents for every core score component
- simplified odds model
- public `target-odds-model` / `target-odds-table` showing implied expectation, base path, bull path, bear path, upgrade data, downgrade data, and odds judgment before the dense target table
- prediction review trigger
- recommendation rationale
- downgrade risk
- next verification data
- hard thesis kill tests for every `actionable_long` target
- source links or source anchors
- `action_state`: `actionable_long`, `watch_only`, or `no_action`
- gate reasons when a target is not actionable

The final target table must be objective about inaction. Scarcity-first opportunity gate: the default action state is `no_action` until the target proves a currently underpriced large opportunity through all four dimensions: scarcity/monopoly, mispricing, earnings elasticity, and risk control. If the research finds no target that passes this gate, the final section should say so directly and show the best watch-only candidates or the missing trigger data rather than forcing bullish recommendations.

Weak scarcity, generic theme exposure, stale/missing valuation, non-positive expected excess return, weak evidence quality, or uncontrolled disconfirming risk must cap target strength even when the industry narrative is attractive.

Ranking must be deterministic from the frozen score object: action-state priority, opportunity fit, total score, payoff convexity, thesis confidence, then stable ticker/name tie-break. The report or workbench must not manually reorder targets after labels are attached or because later outcomes are known.

Every `actionable_long` target must include hard thesis kill tests with test, evidence needed, downgrade action, and source plan. If kill tests are missing or not monitorable, the target must be capped at `watch_only`.

In historical training/backtest mode, the target table must also include evaluation columns or an adjacent label block:

- as-of cutoff
- evaluation date
- label window
- adjusted or total-return start price
- adjusted or total-return end price
- forward three-month return
- benchmark or sector return when available
- excess return when available
- price source
- label status

These label fields are not part of target strength, win probability, payoff odds, or recommendation rationale. They evaluate the frozen historical recommendation only. In final HTML, render them only once, preferably as the rightmost columns of the final target table or as one adjacent label block.

If a target lacks verified price fields, render `n/a` in the label price/return columns and a clear `label_unverified_*` status. This is preferable to dropping economically central non-US targets from the final table.

The section is a research observation list, not a buy/sell/hold instruction. Do not include target prices, position sizes, or final trading commands unless the user explicitly changes the system boundary.

## Source Index Contract

`来源索引` must be collapsed by default.

Source entries must be traceable to concrete materials and must classify source type into one of:

- `evidence`
- `research_report`
- `message`
- `opinion`

Low-reliability messages can only be used as leads and cannot strengthen a conclusion by themselves.

In historical training/backtest mode, source entries should include `source_visible_at`, cutoff status, and `availability_proof`. Post-cutoff sources should be absent from the research source index unless they are clearly labeled as price-label data rather than thesis evidence.

## Clean Final HTML Contract

Final HTML must be research-first. Keep these out of final HTML:

- iteration notes
- "what changed in this run"
- "本轮升级", "本次更新", "本轮新增", "本轮如何落实", and similar change-log phrasing
- mechanism-depth maps or checklists as standalone public artifacts
- quality-framework explanations
- execution traces
- tool attribution
- DeepSeek usage notes
- workbench appendices

Store process metadata in `investment_workbench.json`, run logs, or internal files.

Source parsing traces such as `source_extractions.jsonl` and `leaf_source_reviews.jsonl` are internal files. They should be generated and preserved for auditability and token efficiency, but final HTML should not render them unless the user explicitly asks to inspect parsing traces.

The operational completion gate is `frameworks/research_quality_gate.md`. It validates internal artifacts and should not be explained inside the final HTML report. The public report remains limited to the locked research sections, while parser records, GPT review records, target scorebooks, validation output, and framework QA traces stay in internal files.

Historical mode evaluation fields are allowed in final HTML because they are part of prediction validation, not process trace. Keep `as_of_date` and information cutoff in `当前研究的问题`; keep evaluation dates, label window, benchmark return, and forward return only in the isolated label area of `标的推荐` rather than adding new top-level sections.

## Industry Overview Contract

`行业概况` must appear between `当前研究的问题` and `下钻 QA` in every refreshed canonical report. It must be more detailed than a one-paragraph background note and must be understandable to a new reader in Chinese before they see the QA tree, but it must not sprawl as a fully expanded wall of tables. It is the fact-map layer that generates the QA questions, so it must include these five public modules as clickable collapsed `details.industry-module` cards:

1. `产业链与生态位`: use `supply-chain-section` to show the research-goal bridge, plain summary, node-screening lens, lane/swimlane map, beginner-readable value-flow view, `component-value-chain`, and a visible unified BOM taxonomy. The lane/swimlane map, value-flow view, component/BOM value chain, and taxonomy must be nested collapsible `details.chain-detail-panel` components. Do not render a separate high-level chain overview table by default.
2. `行业空间`: use `industry-space` as a direct BOM-node space reasoning module only. It must include `industry-space-summary` and `space-bom-reasoning`; every key BOM/subsystem node must render as a collapsed `details.space-node-card` with single-column `space-node-reasoning`, where `space-node-space-reasoning` appears first and `space-node-evidence` appears below it. The 空间推理 block must include `space-node-sizing`, `space-method-step`, `space-step-title`, `space-step-index`, `space-public-methods`, `space-method-card-grid`, `space-method-card`, `space-method-card-body`, `space-method-entry`, `space-method-entry-sources`, `space-method-empty`, `space-horizon-conclusion`, `space-horizon-grid`, `space-horizon-card`, `space-node-sizing-table`, and `space-step-confidence`, showing ordered `1 公开拆法`, `2 空间结论`, source chips, and confidence. It should show how public methods imply future node expansion, with cutoff-visible evidence below the reasoning card. It must not answer competition, profit-pool ownership, valuation, or target ranking.

   **Five public-method classification contract** — LLM must classify every data point into one of five buckets by its **source identity**, not by what the data says:

   | Bucket | 来源身份 | 判据 | 正确示例 | 错误示例 |
   |--------|---------|------|---------|---------|
   | **公司指引** | BOM 节点核心供应商公司的管理层预测 | 公司在财报/earnings call 中给出的自身经营指引（收入、capex、出货量、利润率预期）。必须是公司说自己的数字。 | NVIDIA 给出 Q1 FY27 收入指引 $78B | Bank of America 预测 HBM 市场 $54.6B（BofA 是投行，归第三方） |
   | **公司 TAM** | BOM 节点核心供应商公司对行业总规模的估计 | 公司在 Investor Day/10-K/prepared remarks 中引用的市场空间数字。必须是公司说市场的数字。 | Micron 估计 HBM TAM $35B→$100B | Dell'Oro 预测液冷市场 $7B（Dell'Oro 是第三方研究机构） |
   | **客户侧指引** | BOM 节点产品的下游买家 | 下游客户的 capex、订单、RPO、采购计划。证明需求是真实支付，不是口号。 | Amazon/Meta/Alphabet capex 指引，NVIDIA 采购 HBM 量 | 公司自己说"客户需求很强"（这是一手消息，不是客户侧一手数据） |
   | **第三方拆法** | 独立于买卖双方的第三方机构 | 投行（UBS/BofA）、市场研究机构（Omdia/TrendForce/Dell'Oro/LightCounting/SemiAnalysis/TechInsights）、独立分析师。不能是 BOM 节点供应商，也不能是它的客户。 | UBS 预测 HBM ASP +18.5%，Omdia 预测 AI 芯片 $286B | TSMC 在 earnings call 中说 CoWoS 满产（TSMC 是供应商，归公司指引或财务兑现） |
   | **财务兑现证据** | BOM 节点核心供应商公司的已落地经营数据 | 公司已经实现的收入、利润率、backlog、RPO。不是预测，不是指引，是已发生的数字。 | NVIDIA Q4 FY26 DC 收入 $62.3B（已实现），SK hynix OPM 49%（已实现） | Broadcom 给出 Q2 FY26 指引 $22B（这是指引，归公司指引） |

   **硬性规则**：
   - "公司指引"和"公司 TAM"只能来自 BOM 节点核心供应商公司自身，不能来自投行、第三方研究机构、或下游客户
   - "第三方拆法"不能来自 BOM 节点供应商公司或其客户——即使该公司在财报中引用了第三方数据，也应标注原第三方机构为来源
   - 当一条数据同时涉及多个身份时（如 Broadcom 既给自身指引又讨论市场），拆成两条分别归类
   - 找不到符合身份的真实来源时，写 `status=gap`，不要用错误身份来源填充
3. `竞争格局与利润池`: use `industry-competition`, `competition-bom-map`, and one collapsed `details.competition-bom-card` per key BOM/subsystem node. Each BOM card must answer four fixed investment questions through a single-column full-width `competition-question-grid`: `玩家市场份额分布`, `头部玩家优势分析`, `替代玩家赶超希望`, and `格局变化核心变量`. Each fixed question must render as an `overview-question-card` inside an `overview-research-unit` and show natural `overview-answer-prose` paragraphs, claim-near blue inline source links for cited claims, and source chips. The module must include `profit-pool-table` or equivalent rows inside the BOM card so readers see which companies can keep revenue, gross margin, cash flow, or valuation elasticity at that node. It should compare routes and companies inside BOM cards; it must not render a separate route-matrix table or collapse all nodes into one generic competition table.
4. `瓶颈点`: use `industry-chokepoints`, `chain-chokepoints`, `chokepoint-bom-map`, `chokepoint-bom-card`, single-column full-width `chokepoint-question-grid`, `chokepoint-scorecard`, and `bottleneck-release-timeline`. It must also organize by key BOM/subsystem node. Each BOM card must answer a fixed bottleneck question set: `具体约束是什么`, `谁控制该约束`, `稀缺会持续多久`, `扩产/替代/释放路径`, `量化评分与降级规则`, and `标的影响/监控触发器`. Each fixed question must render as an `overview-question-card` inside an `overview-research-unit` and show `overview-answer` and source chips. The scorecard belongs inside the node card, and the release timeline can be node-level or an aggregate table, but every row must map back to a BOM node.
5. `关键变量与待验证数据`: use `industry-key-variables` and `chain-data-gaps` to show the variables that convert the industry map into Q1-Q4 drilldown questions.

`行业概况` and `下钻 QA` must be complementary, not duplicative. The overview answers the map questions: who, what, where, dependency, value/profit flow, candidate bottleneck, and key variable. QA answers the decision questions: whether, why, how much, under what condition, who wins, what refutes, what is priced, and what changes target ranking. Complete reports are invalid when Q1-Q4 L1 cards simply re-render the same `industry-space`, `industry-competition`, `industry-chokepoints`, or supply-chain artifacts already shown in `行业概况`. QA L1 cards should use synthesis prose and next-interrogation focus; detailed tables belong in L2/L3 only when they add source verification, financial bridge, contradiction resolution, valuation/odds judgment, company comparison, kill test, or target-score impact.

The `产业链与生态位` module should render a stable explanation plus table/map with these minimum fields:

- chain layer: upstream, midstream, downstream, infrastructure, distribution, software/ecosystem, customer/end demand, as applicable.
- players: listed companies, private companies, platforms, customers, suppliers, and regulators when they determine value flow.
- products/services: what each player actually provides.
- dependencies: who supplies whom, who controls access, who bears cost, and who captures margin.
- high-level chain table: do not render a separate high-level chain overview table by default. If the user explicitly asks to inspect one, keep it outside the default public report or make it a concise temporary artifact that does not duplicate `component-value-chain`.
- relationship edges: detailed company-to-company or node-to-node edges should live in the lane/company cards, `component-value-chain`, or internal workbench. When used for component-level analysis, keep fields such as `from`, `to`, `relationship`, `demand_input`, `supply_input`, `produces`, `provides_to`, `financial_metrics`, `bottleneck_strength`, `qa_link`, and `evidence`; do not force all of them into a public high-level chain table.
- value/profit flow: where revenue, margin, cash flow, bargaining power, and capital intensity sit.
- simple value-flow steps: before detailed value-flow cards, show `chain-simple-flow` with plain-language steps explaining how demand becomes orders, orders become products/systems, and systems become revenue/ROI validation. Define unclear terms in place. For AI infrastructure, "系统交付" means turning chips, memory, storage, network, power, cooling, chassis, rack, and integration work into deployable servers, racks, clusters, or data-center capacity.
- component/BOM map: the subsystem or component, component/service, key companies, input, downstream recipient, financial validation metric, and related QA node.
- candidate chokepoints: which links are scarce, hard to substitute, protected by qualification, proprietary data/software, trust, regulation, distribution, capacity, or ecosystem lock-in.
- research bridge: how the current research goal turns into supply-chain questions and then into Q1-Q4.
- node-screening lens: demand flow, scarcity, substitution difficulty, monetization, market pricing, and disconfirming trigger.
- QA link: which Q1-Q4 nodes should use the supply-chain evidence.
- data gaps: missing data that must be collected before strengthening QA answers or target scores.

The public industry overview explanation must use:

- `industry-overview-section`
- `industry-module`
- `module-head`
- `module-index`
- `industry-module-body`
- `chain-explain`
- `chain-research-bridge`
- `chain-node-lens`
- `chain-plain-summary`
- `chain-lane-map`
- `chain-value-flow`
- `chain-simple-flow`
- `chain-detail-panel`
- `component-value-chain`
- `chain-layer-grid`
- `chain-layer-card`
- `chain-relationship-graph`
- `chain-stage-panel`
- `chain-company-list`
- `chain-company-card`
- `chain-chokepoints`
- `overview-research-unit`
- `overview-question-card`
- `overview-answer`
- `competition-bom-map`
- `competition-bom-card`
- `competition-question-grid`
- `profit-pool-table`
- `chokepoint-bom-map`
- `chokepoint-bom-card`
- `bom-taxonomy`
- `bom-taxonomy-grid`
- `bom-taxonomy-card`
- `chokepoint-question-grid`
- `chokepoint-scorecard`
- `bottleneck-release-timeline`
- `industry-space`
- `industry-competition`
- `industry-chokepoints`
- `industry-key-variables`
- `key-variable-bom-map`
- `key-variable-bom-card`
- `chain-data-gaps`

The `行业概况` section must also keep `supply-chain-section`, `chain-research-bridge`, `chain-node-lens`, `chain-lane-map`, `chain-value-flow`, `chain-simple-flow`, nested `details.chain-detail-panel`, `component-value-chain`, `bom-taxonomy`, `bom-taxonomy-grid`, `bom-taxonomy-card`, `chain-relationship-graph`, `chain-stage-panel`, `chain-company-list`, `chain-company-card`, `chain-chokepoints`, `overview-research-unit`, `overview-question-card`, `overview-answer`, `competition-bom-map`, `competition-bom-card`, `competition-question-grid`, `profit-pool-table`, `bottleneck-release-timeline`, `chokepoint-bom-map`, `chokepoint-bom-card`, `chokepoint-question-grid`, `chokepoint-scorecard`, `key-variable-bom-map`, `key-variable-bom-card`, `industry-space`, `industry-space-summary`, `space-bom-reasoning`, `space-node-card`, `space-node-reasoning`, `space-node-evidence`, `space-node-space-reasoning`, `space-node-sizing`, `space-method-step`, `space-step-title`, `space-step-index`, `space-public-methods`, `space-method-card-grid`, `space-method-card`, `space-method-card-body`, `space-method-entry`, `space-method-entry-sources`, `space-method-empty`, `space-horizon-conclusion`, `space-horizon-grid`, `space-horizon-card`, `space-node-sizing-table`, `space-step-confidence`, `table-scroll`, `industry-competition`, `industry-chokepoints`, and `industry-key-variables` classes so validators can distinguish it from process appendices or decorative cards. The five industry modules must be `details` elements with direct `summary` headers and `chevron` affordances. Every post-taxonomy module must cover the BOM taxonomy nodes one-to-one; aggregate demand-validation rows may supplement but never replace a BOM node. The QA tree may still contain deeper supply-chain questions and the internal workbench may keep more detailed maps, but the public industry overview should emphasize decision-relevant modules.

## L3-L5 Logic Card Contract

Every L3-L5 `logic-grid` must distinguish `Fact`, `Inference`, `Judgment`, and `Gap / Trigger`.

- `Fact` is source-bound: extracted facts, reported numbers, dates, official statements, or source summaries visible at the cutoff.
- `Inference` explains how the facts answer the leaf question.
- `Judgment` states the decision impact on parent conclusion, target strength, `action_state`, valuation odds, or risk control.
- `Fact`, `Inference`, and `Judgment` must not be three copies of the same conclusion. A complete QA tree is invalid when those fields are undifferentiated.

L3-L5 cards must directly answer their unit question. When the unit is a mapping, bridge, comparison, scenario, score, target-selection, or kill-test question, the current-conclusion block should include an `artifact-card` with the corresponding structured answer table. Examples: workload-to-product mapping, demand-supply slope table, unit-economics bridge, valuation bridge, target-score table, or kill-test table. Source chips and generic prose are not enough if they leave the reader to infer the actual answer.

The public card may show only the readable logic fields, but the source QA tree must preserve the full L3-L5 audit schema:

- `decision_use`: how the answer changes the parent decision, target rank, odds, or risk control.
- `support_evidence` and `refute_evidence`: what would strengthen or weaken the leaf.
- `target_implications`: how the answer affects final target scoring or `action_state`.
- `score_component`: one or more ranking drivers, such as `future_space`, `chokepoint_strength`, `valuation_odds`, `evidence_quality`, `disconfirming_risk_control`, `monitorability`, `payoff_convexity`, `target_ranking`, or `action_state`.
- `minimum_evidence_gate` and `refuting_source_plan`: the evidence floor and required boundary check before strengthening the conclusion.
- `source_plan`: structured source objects with expected fields, bucket, visible date/cutoff status, allowed usage, preferred parser skill, and historical-mode availability proof.
- `skill_dispatch`: structured object with `task_family`, `selected_skill`, `concrete_materials`, `extraction_schema`, `source_extraction_ids`, `leaf_source_review_ids`, `skill_output_status`, `fallback_used`, and `gpt_verification_status`.

Every persisted source-parser record must include `schema_fields` that fill the L3-L5 `skill_dispatch.extraction_schema`. Generic source summaries without schema-field mapping are not sufficient to strengthen refreshed canonical QA answers until GPT maps and verifies them.

The visible L3-L5 card must surface the minimum routing proof from this schema: selected skill, actual execution status, score component, and decision use. The detailed `source_extractions.jsonl` and `leaf_source_reviews.jsonl` records remain internal by default.

## Visual Contract

Default visual style:

- Apple-inspired light surfaces and SF-system typography.
- Clear L1/L2/L3/L4/L5 hierarchy through spacing, labels, and restrained borders.
- Soft text palette with blue-gray hierarchy accents; avoid heavy black text blocks or black badges unless needed for a small emphasis state.
- Blue links for concrete sources.
- Dense but readable tables for target recommendation and source traceability.
- Historical training/backtest target tables should preserve the canonical `target-section` + `target-table` structure and add compact label columns rather than switching to per-target cards.
- No duplicated titles, duplicated child lists, or repeated summary blocks.
- No decorative elements that reduce scanability.

Canonical frontend component contract:

- Use the same report shell and component classes across refreshed research reports unless the user explicitly asks for a new visual system.
- The canonical report shell is: `hero`, `top-nav`, `goal-card`, `constraint-definition`, `industry-overview-section`, `industry-module`, `module-head`, `module-index`, `industry-module-body`, `supply-chain-section`, `chain-explain`, `chain-research-bridge`, `chain-node-lens`, `chain-plain-summary`, `chain-detail-panel`, `chain-lane-map`, `chain-value-flow`, `chain-simple-flow`, `component-value-chain`, `bom-taxonomy`, `bom-taxonomy-grid`, `bom-taxonomy-card`, `chain-layer-grid`, `chain-layer-card`, `chain-relationship-graph`, `chain-stage-panel`, `chain-company-list`, `chain-company-card`, `chain-chokepoints`, `overview-research-unit`, `overview-question-card`, `overview-answer`, `competition-bom-map`, `competition-bom-card`, `competition-question-grid`, `profit-pool-table`, `bottleneck-release-timeline`, `chokepoint-bom-map`, `chokepoint-bom-card`, `chokepoint-question-grid`, `chokepoint-scorecard`, `chain-data-gaps`, `industry-space`, `industry-space-summary`, `space-bom-reasoning`, `space-node-card`, `space-node-reasoning`, `space-node-evidence`, `space-node-space-reasoning`, `space-node-sizing`, `space-method-step`, `space-step-title`, `space-step-index`, `space-public-methods`, `space-method-card-grid`, `space-method-card`, `space-method-card-body`, `space-method-entry`, `space-method-entry-sources`, `space-method-empty`, `space-horizon-conclusion`, `space-horizon-grid`, `space-horizon-card`, `space-node-sizing-table`, `space-step-confidence`, `table-scroll`, `industry-competition`, `industry-chokepoints`, `industry-key-variables`, `qa-card level-1/2/3`, `qa-body`, `qa-block`, `block-title`, `logic-grid`, `logic-card`, `source-chips`, `source-chip`, `more-chip`, `artifact-card`, `target-section`, `target-profit-bridge`, `target-valuation-table`, `target-summary`, `target-odds-model`, `target-odds-table`, `target-table`, `source-collapse`, `source-grid`, and `source-card`.
- `qa-card level-1/2/3` must be implemented as `details.qa-card > summary` with visible `qa-count` and `chevron` affordances. The default state is `open`, and the summary/header is the click target for collapse/expand.
- `标的推荐` should render as one synthesized `target-section` with `target-profit-bridge`, `target-valuation-table`, a `target-odds-model`, `target-odds-table`, and dense `target-table`, not as separate per-target cards by default.
- `target-table` must color-code `action_state` through `state-actionable_long`, `state-watch_only`, and `state-no_action` classes so watch/no-action/actionable states are visually scannable and consistent across live and backtest reports.
- `来源索引` should render as one collapsed `source-collapse` containing grouped `source-card` entries; avoid separate `source-bucket` components unless the user asks for grouped source browsing.
- Do not introduce alternate component families such as `target-card`, `source-bucket`, `section-lead`, `answer-artifact`, `schema-pill`, or `target-grid` in refreshed canonical reports.

Frontend card-style validation:

- `qa-card level-1/2/3` must show nesting through spacing, subtle borders, and restrained color accents, not through unrelated section templates.
- `qa-card level-1/2/3` must preserve native click-to-collapse behavior. A report that renders QA cards as static `article` or `div` elements has drifted even if the visual style looks similar.
- `artifact-card` is reserved for scorecards, matrices, answer tables, risk tests, and other answer artifacts inside the owning QA node.
- `target-section` plus `target-profit-bridge`, `target-valuation-table`, `target-odds-model`, `target-odds-table`, and `target-table` is the default final recommendation format. Do not switch to per-target cards unless the user asks for a redesign.
- `source-collapse` is the only default public source-index wrapper and should be collapsed by default.
- Card style should remain light, quiet, and research-first: white or light-gray surfaces, SF-system typography, restrained borders, stable table sizing, and no decorative backgrounds that compete with the QA hierarchy.
