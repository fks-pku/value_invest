# Research Report Contract

This contract defines the locked default final report structure for all future investment research outputs unless the user explicitly asks to iterate on the framework.

## Locked Current Contract

The current locked contract is:

- Top-level order is exactly `当前研究目标` -> `产业链全景` -> `问题下钻` -> `最终标的推荐` -> `来源索引`.
- `产业链全景` is a standalone research map section, not a process appendix. It must show the upstream, midstream, downstream, key players, products/services, dependency links, profit/value flow, and where possible chokepoints sit before the QA drilldown begins. It must also use `supply-chain-panorama-explainer` output so a new reader can understand the chain in Chinese before entering the QA tree.
- `问题下钻` must preserve the full adapted Q1-Q4 QA tree. Complete refreshed reports must render L3 leaf questions, not stop at L2 summaries, unless the user explicitly asks for a shorter executive version.
- Q4 remains the auditable as-of target-selection QA node and must keep child questions when the research has target implications.
- `最终标的推荐` is a standalone presentation rollup, not a replacement for Q4. It synthesizes the QA tree into a ranked target table.
- In historical training/backtest mode, public report prose must read as if written on the `as_of_date`. Later price movement appears only once, as isolated evaluation columns or one adjacent label block in `最终标的推荐`.
- The report must not add process appendices, execution traces, tool traces, iteration notes, or workbench sections unless the user explicitly asks for them.
- The report must not add change logs, upgrade logs, "本轮/本次升级", "本轮/本次更新", "本轮如何落实", mechanism-depth checklists, framework explanations, or meta explanations of what changed in the framework. Framework changes must be visible only through better QA, evidence, scoring, and target reasoning.

## Non-Drift Locks

These five areas are locked requirements for all future reports and refreshed reports. Do not relax, reinterpret, or silently replace them in generated reports, templates, prompts, or renderer code:

1. Hierarchy and format lock: final reports must keep the exact public order `当前研究目标` -> `产业链全景` -> `问题下钻` -> `最终标的推荐` -> `来源索引`; `问题下钻` must render the full adapted Q1-Q4 tree through L1/L2/L3 when L3 exists; every QA card must use the same three-block body order.
2. Backtest time-slice lock: historical training/backtest mode uses only information visible at the frozen cutoff, normally three calendar months before the evaluation/report date unless the user specifies a different horizon. Source collection, source parsing, QA reasoning, target ranking, score fields, odds models, and rationale must not use any post-cutoff information. The only current-time data allowed in the public report is the final-target evaluation label, rendered once in `最终标的推荐`.
3. Frontend card-style lock: refreshed canonical reports must use the shared Apple-inspired card system and canonical component family. QA cards must remain clickable/collapsible through `details.qa-card > summary` with `qa-count` and `chevron`, default `open`. Do not introduce a parallel public layout, alternate card family, static QA card wrapper, per-target card deck, source-bucket layout, process appendix layout, or redesigned visual system unless the user explicitly asks for a frontend redesign.
4. Public no-changelog lock: refreshed canonical reports must not render process/change-log content such as "本轮升级", "本次更新", "本轮新增", "机制深度映射", "本轮如何落实", "what changed in this run", execution/tool traces, or workbench/process explanations. These are internal artifacts unless the user explicitly asks to inspect process.
5. Supply-chain map lock: final reports must include `产业链全景` as a public top-level section before `问题下钻`. This section must use a stable `supply-chain-section` with `chain-explain`, `chain-plain-summary`, `chain-flow-steps`, `chain-layer-grid`, `chain-layer-card`, `chain-chokepoints`, `chain-target-links`, and `chain-map` or `chain-table`; it must map upstream, midstream, downstream, key players, products/services, dependencies, value flow, and candidate chokepoints in beginner-readable Chinese. It is an analytical map used by Q2/Q4, not a decorative industry background.
6. Additive-iteration lock: framework iteration is additive by default. New sections, fields, dimensions, skills, source schemas, or visual affordances may be added only after preserving all existing public section order, canonical component classes, QA interactions, action-state colors, source-collapse behavior, target-table structure, and no-changelog constraints. Removing, renaming, restyling, or replacing any existing public contract element requires an explicit user request for a frontend/report redesign.

Before marking any framework iteration complete, run a regression contract check on at least one newly generated/refreshed report and one existing canonical fixture or sample report. The check must include `validate-report-contract`, `validate-research-artifacts` when artifacts exist, and a browser or DOM smoke check for collapsible QA cards and action-state color classes. A framework iteration is incomplete if a newly added feature passes but an older locked behavior drifts.

Executable enforcement lives in `src/value_invest_research/framework_contracts.py`. Use it to validate report HTML, QA tree schema, time-sliced sources, target score separation, frozen recommendation integrity, label attachment, training samples, prediction reviews, internal workbench separation, and domain playbook selection.

In addition to the public presentation locks, refreshed canonical reports must pass the internal QA professionalism lock. Every L3 record is invalid if it lacks `decision_use`, `materiality`, `support_evidence`, `refute_evidence`, `target_implications`, `score_component`, `minimum_evidence_gate`, `refuting_source_plan`, structured `source_plan`, structured `skill_dispatch`, differentiated `fact`/`inference`/`judgment`, `gap`, `trigger`, and `source_links`. In historical mode, the structured `source_plan` must also carry source-visible date, cutoff status, and availability proof.

## Top-Level HTML Contract

Final user-facing HTML reports must use exactly these five top-level sections, in this order:

1. `当前研究目标`
2. `产业链全景`
3. `问题下钻`
4. `最终标的推荐`
5. `来源索引`

Do not add top-level process sections such as execution plan, quality framework, tool trace, iteration notes, workbench appendix, or full report appendix unless the user explicitly asks to inspect process.

Do not add in-section process or change-log blocks either. A block inside `当前研究目标`, a QA card, or `最终标的推荐` is still contract-invalid if it explains what the framework upgraded, what changed in this run, how a mechanism-depth checklist was implemented, or which internal process produced the report.

## Strict Rendering Invariants

Treat a generated report as contract-invalid if any of these invariants fail:

1. The final HTML has exactly five public top-level sections, in this order: `当前研究目标`, `产业链全景`, `问题下钻`, `最终标的推荐`, `来源索引`.
2. `产业链全景` renders as one `supply-chain-section` with `chain-explain`, `chain-plain-summary`, `chain-flow-steps`, `chain-layer-grid`, `chain-layer-card`, `chain-chokepoints`, `chain-target-links`, and a `chain-map` or `chain-table`; it must cover upstream, midstream, downstream, key players, products/services, dependency links, value/profit flow, and candidate chokepoints in beginner-readable Chinese.
3. `问题下钻` renders Q1-Q4 as `qa-card level-1` cards. Q nodes must not appear as loose top-level sections outside `问题下钻`.
3. Each L1 renders its available L2 children as `qa-card level-2` cards, grouped by meaningful mechanism bucket rather than by generic summary labels.
4. Complete refreshed reports render every available L3 leaf as a `qa-card level-3` card. A report may omit L3 only when the source QA tree truly has no L3 leaves or the user explicitly requested a shorter executive version.
5. Every `qa-card level-1`, `qa-card level-2`, and `qa-card level-3` uses the same three-block body order: `1. 当前结论呈现`, `2. 问题展开（子 QA）`, `3. 待补充的问题`.
6. Every QA card must be an interactive `details.qa-card` element with a direct `summary` header, `qa-count`, and `chevron`, opened by default. Static `article.qa-card`, `div.qa-card`, or non-clickable wrappers are contract-invalid even if hierarchy classes are present.
7. Parent-level artifacts such as scorecards, risk matrices, answer tables, and target-selection tables render inside `1. 当前结论呈现` of the QA node they answer, before child QA expansion.
8. `2. 问题展开（子 QA）` contains either inline child `qa-card` nodes or jump links, not both. Do not duplicate the same child titles in both a summary list and rendered child cards.
9. Q4 remains inside `问题下钻` as the auditable target-selection QA node and keeps its L2/L3 children. The standalone `最终标的推荐` section must never erase, replace, rename, or move Q4.
10. `最终标的推荐` renders as one `target-section` with a dense `target-table` by default. It is a synthesized rollup from Q1-Q4, not an extra QA node and not a process appendix.
11. `来源索引` renders as one collapsed `source-collapse` by default. Source details may expand inside it, but they must not create additional top-level sections.
12. Refreshed canonical reports must use the shared component family: `hero`, `top-nav`, `goal-card`, `supply-chain-section`, `chain-explain`, `chain-plain-summary`, `chain-flow-steps`, `chain-layer-grid`, `chain-layer-card`, `chain-chokepoints`, `chain-target-links`, `chain-map`, `chain-table`, `qa-card level-1`, `qa-card level-2`, `qa-card level-3`, `qa-body`, `qa-block`, `block-title`, `artifact-card`, `target-section`, `target-table`, and `source-collapse`. Do not introduce alternate public component families unless the user explicitly asks for a frontend redesign.
13. Target-table `action_state` cells must render with the canonical status color classes: `state-actionable_long`, `state-watch_only`, or `state-no_action`. Plain uncolored action-state text is contract drift.
14. Historical training/backtest labels are evaluation fields only. They may appear once in the isolated label area of `最终标的推荐`, never inside QA conclusion prose or Q4 child logic.
15. Every visible L3 card must include a compact professional-routing strip with selected `Skill`, actual `Execution` status, `Score Component`, and `Decision Use`. `Skill` is the intended specialty lens; `Execution` must come from `skill_output_status` and `fallback_used`, so a selected skill cannot be mistaken for a completed parser run. Full parser traces still belong in internal files unless explicitly requested.

## Time-Sliced Evaluation Contract

Final reports must declare the run mode in the current research goal section:

- Historical training/backtest mode: show `as_of_date` and information cutoff in the current research goal section. The QA drilldown and target rationale must be written only from information publicly visible on or before `as_of_date`.
- Live prediction mode: show report date, evidence freshness, validation horizon, and next review trigger. Do not show future return labels.

Historical training/backtest reports may use post-cutoff price data only as an ex-post target label after the recommendation list is frozen. Public backtest reports must read as if written by the system on the `as_of_date`: QA conclusions, target rationale, score explanations, odds models, downgrade triggers, and summary prose must not mention ex-post winners, losers, realized returns, calibration lessons, or later price action. Show later price movement only once, visually separated from rationale and score fields, so readers can distinguish as-of prediction evidence from later outcome measurement.

Label availability must not define the investment universe. The frozen target list must start from economically relevant securities or assets across exchanges. If a local/non-US target lacks a verified price label, keep it in the target table and mark the label as `label_unverified_*`; do not replace the target with a convenient US/Nasdaq proxy or omit it from Q4.

The time-slice rule is asymmetric by design:

- Allowed before the frozen recommendation: only source materials, filings, reports, messages, prices, and market context visible on or before `as_of_date`.
- Forbidden before the frozen recommendation: post-cutoff facts, later price action, later revisions, later analyst reports, current knowledge about winners/losers, and any wording that explains the as-of thesis using post-cutoff outcomes.
- Allowed after the frozen recommendation: one current-time label dataset for the final targets only, normally measuring the forward three-month price change from the as-of price date to the evaluation price date.
- Required separation: the label must be stored and rendered as evaluation metadata, not as evidence, score input, odds input, source material, or target-rationale text.

## QA Hierarchy Contract

The default QA hierarchy is three layers:

- `L1`: top-level adapted research direction, normally Q1-Q4.
- `L2`: mechanism bucket selected by the research-type adapter and domain playbook. L2 must group L3 questions by meaningful analytical mechanism.
- `L3`: evidence-collection and answer unit.

L2 must not be a single catch-all wrapper under each L1 when many unrelated L3 questions exist. Split L2 by the analytical mechanisms that matter for the selected research object.

The shared contract defines hierarchy and presentation only. It does not hard-code domain questions, metrics, parsing methods, tracking indicators, or thresholds.

However, refreshed canonical reports are not allowed to use generic L2 buckets when a domain requires a concrete mechanism model. The selected domain playbook must create L2/L3 coverage for the relevant mechanism-depth blocks: demand driver tree, supply/access response, unit economics/profit bridge, competitive value-capture map, market-pricing bridge, disconfirming/counter-supply tests, capital-chain or second-order beneficiaries, and model/口径 reconciliation. These blocks belong inside the QA hierarchy, not in a top-level process appendix.

When a domain playbook uses bottleneck or chokepoint analysis, the scorecard must live inside the relevant Q2 QA node, not in a top-level appendix. The final target recommendation must explicitly use the chokepoint score or score drivers together with future space, valuation odds, evidence quality, and disconfirming-risk control.

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
- supply-chain map schema: upstream, midstream, downstream, players, products/services, dependency links, value/profit flow, candidate chokepoints, Chinese plain summary, flow steps, layer cards, and target/Q2/Q4 links
- mechanism-depth maps that specify the driver tables, formulas, units, periods, and口径 needed to make the research as detailed as a professional model-driven report

Examples may appear inside domain playbooks or research-type adapters, not inside this public report contract.

Inside every QA card, use this display order:

1. `当前结论呈现`
2. `问题展开（子 QA）`
3. `待补充的问题`

If child QA nodes are rendered inline as expandable cards, do not also render a separate child-question list with the same titles.

## Final Target Recommendation Contract

When the research has investment implications, add a standalone `最终标的推荐` section after `问题下钻`.

The standalone `最终标的推荐` section is a presentation rollup, not a replacement for Q4. Q4 must remain inside `问题下钻` as the auditable as-of target-selection QA node with child questions. In historical training/backtest mode, do not create a Q4 child whose purpose is to evaluate later returns; later price movement belongs only in the isolated label area of the final target table.

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

Historical mode evaluation fields are allowed in final HTML because they are part of prediction validation, not process trace. Keep `as_of_date` and information cutoff in `当前研究目标`; keep evaluation dates, label window, benchmark return, and forward return only in the isolated label area of `最终标的推荐` rather than adding new top-level sections.

## Supply-Chain Map Contract

`产业链全景` must appear between `当前研究目标` and `问题下钻` in every refreshed canonical report. It must be more detailed than a one-paragraph background note and must be understandable to a new reader in Chinese before they see the QA tree. It should render a stable explanation plus table/map with these minimum fields:

- chain layer: upstream, midstream, downstream, infrastructure, distribution, software/ecosystem, customer/end demand, as applicable.
- players: listed companies, private companies, platforms, customers, suppliers, and regulators when they determine value flow.
- products/services: what each player actually provides.
- dependencies: who supplies whom, who controls access, who bears cost, and who captures margin.
- value/profit flow: where revenue, margin, cash flow, bargaining power, and capital intensity sit.
- candidate chokepoints: which links are scarce, hard to substitute, protected by qualification, proprietary data/software, trust, regulation, distribution, capacity, or ecosystem lock-in.
- QA link: which Q2/Q4 nodes should use the chain-map evidence.

The public explanation must use:

- `chain-explain`
- `chain-plain-summary`
- `chain-flow-steps`
- `chain-layer-grid`
- `chain-layer-card`
- `chain-chokepoints`
- `chain-target-links`

The `产业链全景` section must also keep `supply-chain-section` and `chain-map` or `chain-table` classes so validators can distinguish it from process appendices or decorative cards. The QA tree may still contain deeper supply-chain questions, but the top-level map is mandatory because all later opportunity analysis needs a shared industry coordinate system.

## L3 Logic Card Contract

Every L3 `logic-grid` must distinguish `Fact`, `Inference`, `Judgment`, and `Gap / Trigger`.

- `Fact` is source-bound: extracted facts, reported numbers, dates, official statements, or source summaries visible at the cutoff.
- `Inference` explains how the facts answer the leaf question.
- `Judgment` states the decision impact on parent conclusion, target strength, `action_state`, valuation odds, or risk control.
- `Fact`, `Inference`, and `Judgment` must not be three copies of the same conclusion. A complete QA tree is invalid when those fields are undifferentiated.

L3 cards must directly answer their leaf question. When the leaf is a mapping, bridge, comparison, scenario, score, target-selection, or kill-test question, the L3 current-conclusion block should include an `artifact-card` with the corresponding structured answer table. Examples: workload-to-product mapping, demand-supply slope table, unit-economics bridge, valuation bridge, target-score table, or kill-test table. Source chips and generic prose are not enough if they leave the reader to infer the actual answer.

The public card may show only the readable logic fields, but the source QA tree must preserve the full L3 audit schema:

- `decision_use`: how the answer changes the parent decision, target rank, odds, or risk control.
- `support_evidence` and `refute_evidence`: what would strengthen or weaken the leaf.
- `target_implications`: how the answer affects final target scoring or `action_state`.
- `score_component`: one or more ranking drivers, such as `future_space`, `chokepoint_strength`, `valuation_odds`, `evidence_quality`, `disconfirming_risk_control`, `monitorability`, `payoff_convexity`, `target_ranking`, or `action_state`.
- `minimum_evidence_gate` and `refuting_source_plan`: the evidence floor and required boundary check before strengthening the conclusion.
- `source_plan`: structured source objects with expected fields, bucket, visible date/cutoff status, allowed usage, preferred parser skill, and historical-mode availability proof.
- `skill_dispatch`: structured object with `task_family`, `selected_skill`, `concrete_materials`, `extraction_schema`, `source_extraction_ids`, `leaf_source_review_ids`, `skill_output_status`, `fallback_used`, and `gpt_verification_status`.

Every persisted source-parser record must include `schema_fields` that fill the L3 `skill_dispatch.extraction_schema`. Generic source summaries without schema-field mapping are not sufficient to strengthen refreshed canonical QA answers until GPT maps and verifies them.

The visible L3 card must surface the minimum routing proof from this schema: selected skill, actual execution status, score component, and decision use. The detailed `source_extractions.jsonl` and `leaf_source_reviews.jsonl` records remain internal by default.

## Visual Contract

Default visual style:

- Apple-inspired light surfaces and SF-system typography.
- Clear L1/L2/L3 hierarchy through spacing, labels, and restrained borders.
- Soft text palette with blue-gray hierarchy accents; avoid heavy black text blocks or black badges unless needed for a small emphasis state.
- Blue links for concrete sources.
- Dense but readable tables for target recommendation and source traceability.
- Historical training/backtest target tables should preserve the canonical `target-section` + `target-table` structure and add compact label columns rather than switching to per-target cards.
- No duplicated titles, duplicated child lists, or repeated summary blocks.
- No decorative elements that reduce scanability.

Canonical frontend component contract:

- Use the same report shell and component classes across refreshed research reports unless the user explicitly asks for a new visual system.
- The canonical report shell is: `hero`, `top-nav`, `goal-card`, `supply-chain-section`, `chain-explain`, `chain-plain-summary`, `chain-flow-steps`, `chain-layer-grid`, `chain-layer-card`, `chain-chokepoints`, `chain-target-links`, `chain-map`, `chain-table`, `qa-card level-1/2/3`, `qa-body`, `qa-block`, `block-title`, `logic-grid`, `logic-card`, `source-chips`, `source-chip`, `more-chip`, `artifact-card`, `target-section`, `target-summary`, `target-table`, `source-collapse`, `source-grid`, and `source-card`.
- `qa-card level-1/2/3` must be implemented as `details.qa-card > summary` with visible `qa-count` and `chevron` affordances. The default state is `open`, and the summary/header is the click target for collapse/expand.
- `最终标的推荐` should render as one synthesized `target-section` with a dense `target-table`, not as separate per-target cards by default.
- `target-table` must color-code `action_state` through `state-actionable_long`, `state-watch_only`, and `state-no_action` classes so watch/no-action/actionable states are visually scannable and consistent across live and backtest reports.
- `来源索引` should render as one collapsed `source-collapse` containing grouped `source-card` entries; avoid separate `source-bucket` components unless the user asks for grouped source browsing.
- Do not introduce alternate component families such as `target-card`, `source-bucket`, `section-lead`, `answer-artifact`, `schema-pill`, or `target-grid` in refreshed canonical reports.

Frontend card-style validation:

- `qa-card level-1/2/3` must show nesting through spacing, subtle borders, and restrained color accents, not through unrelated section templates.
- `qa-card level-1/2/3` must preserve native click-to-collapse behavior. A report that renders QA cards as static `article` or `div` elements has drifted even if the visual style looks similar.
- `artifact-card` is reserved for scorecards, matrices, answer tables, risk tests, and other answer artifacts inside the owning QA node.
- `target-section` plus `target-table` is the default final recommendation format. Do not switch to per-target cards unless the user asks for a redesign.
- `source-collapse` is the only default public source-index wrapper and should be collapsed by default.
- Card style should remain light, quiet, and research-first: white or light-gray surfaces, SF-system typography, restrained borders, stable table sizing, and no decorative backgrounds that compete with the QA hierarchy.
