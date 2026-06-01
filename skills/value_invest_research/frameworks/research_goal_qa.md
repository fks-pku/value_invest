# Research Goal QA Framework

This is the only active research framework for this project.

Use it whenever the user proposes a research goal, topic, company, sector, event, concept, or investment question.

Final report presentation is governed by `research_report_contract.md`. Follow that contract for all future user-facing HTML reports unless the user explicitly asks to iterate on the framework.

## Output Order

Final user-facing HTML reports must use exactly this top-level order:

1. Current research goal.
2. Supply-chain panorama / `产业链全景`.
3. Question drilldown.
4. Final target recommendation.
5. Source index.

The final target recommendation is a research conclusion section. It must synthesize all QA evidence into a ranked observation list with specific targets, win probability, payoff odds, rationale, required verification data, and downgrade triggers. It must not issue buy/sell/hold instructions.

`产业链全景` is mandatory. It must map upstream, midstream, downstream, key players, products/services, dependency links, value/profit flow, and candidate chokepoints before the QA drilldown. Use `supply-chain-panorama-explainer` so the public section is beginner-readable Chinese rather than a jargon-only table. Q2 and Q4 should be able to cite this map when judging scarcity, value capture, and target exposure.

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

Every research run must declare one of two modes before source collection:

- Historical training/backtest mode: used when the user wants to train, audit, or evaluate prediction ability. Set an `as_of_date`, defaulting to three calendar months before the evaluation date unless the user specifies another cutoff. All QA reasoning, source parsing, valuation context, and target ranking must only use information publicly visible on or before `as_of_date`.
- Live prediction mode: used when the user wants an investable current research observation. Use information visible up to the report date. Do not attach a future return label; record the next validation horizon and review trigger instead.

Historical training/backtest mode must prevent look-ahead bias:

- Each L3 source plan records `as_of_date`, `source_visible_at`, and cutoff status.
- Materials visible after `as_of_date` are rejected or quarantined as look-ahead data.
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
- Supply-chain validation: verify the report includes a standalone `产业链全景` section with `supply-chain-section`, `chain-explain`, `chain-plain-summary`, `chain-flow-steps`, `chain-layer-grid`, `chain-layer-card`, `chain-chokepoints`, `chain-target-links`, plus `chain-map` or `chain-table`, and that it maps upstream, midstream, downstream, players, products/services, dependencies, value/profit flow, and candidate chokepoints in beginner-readable Chinese.
- Time-slice audit: reject post-cutoff thesis sources and allow current-time data only as final-target label metadata.
- QA schema validation: require L3 question-quality fields, structured source plan, structured skill dispatch, fact, inference, judgment, gap, trigger, and source links before parent rollup. The validator rejects missing `decision_use`, `support_evidence`, `refute_evidence`, `target_implications`, `score_component`, `minimum_evidence_gate`, `refuting_source_plan`, or undifferentiated fact/inference/judgment.
- Research artifact validation: require L3 parser `schema_fields`, source availability proof, auditable target `score_subcomponents`, deterministic target ranking inputs, and hard kill tests for actionable targets.
- Domain playbooks: start from reusable mechanism buckets such as semiconductor hardware HBM/custom ASIC/foundry/WFE buckets, then adapt to the research object.
- Target scoring: roll score evidence into four core target dimensions, `scarcity_or_monopoly`, `mispricing`, `earnings_elasticity`, and `risk_control`, while preserving the seven auditable score components and score subcomponents underneath.
- Freeze and label: create frozen recommendations first, then attach forward-return labels without changing rank, rationale, score, or odds.
- Training samples and prediction reviews: export machine-readable backtest samples and later review scaffolds so the system can learn from both correct and incorrect calls.
- Internal workbench separation: keep parser outputs, GPT reviews, validator output, rejected future sources, scoring worksheets, freeze metadata, and label attach metadata out of the public HTML unless the user asks to inspect them.
- Public no-changelog separation: keep framework-change notes, upgrade summaries, "what changed in this run" text, mechanism-depth maps, and "本轮如何落实" tables out of public HTML. They may live in workbench JSON, logs, or chat responses only.

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
| Industry/theme opportunity | Demand reality | Value-capture bottlenecks | Disconfirming tests and priced-in risk | Target observation list |
| Single company | Growth drivers | Moat, unit economics, and value capture | Financial quality, valuation, and disconfirming tests | Observation decision and monitoring list |
| Event/policy | Event facts and scope | Transmission mechanism | Beneficiaries, losers, and second-order effects | Disconfirming tests and watchlist |
| Technology/product route | Technical feasibility and adoption demand | Bottlenecks and ecosystem readiness | Commercialization, competition, and disconfirming tests | Exposed assets and monitoring list |
| Target update | What changed | Which thesis node changed | Whether price/risk/reward changed | Update action for observation strength |

If the topic does not fit a default type, define a custom Q1-Q4 map in the execution plan. Do not force demand/bottleneck/target wording onto company, event, policy, or technology-route questions when it weakens the research.

## Mechanism Depth Protocol

For industry/theme opportunity and technology/product-route research, the QA tree must be detailed enough to reconstruct the investment mechanism, not just describe the theme. Before source collection, create a mechanism-depth map with these blocks unless a block is explicitly irrelevant:

- Demand driver tree: who needs more of the product/service, what workload or customer behavior causes it, and how it decomposes into volume, price, mix, and duration.
- Supply or access response: what constrains capacity, utilization, inventory, lead time, capex, regulation, distribution, trust, data, or ecosystem access.
- Unit economics and profit bridge: how demand reaches revenue, gross margin, operating margin, FCF, capex intensity, and working-capital pressure.
- Competitive value-capture map: which companies/assets capture value at each node and what substitutes, internal builds, or new entrants could bypass them.
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
   - For model-heavy industry/theme research, require a mechanism-depth map before accepting the L2/L3 tree. L2 buckets should represent analytical mechanisms such as demand driver, supply response, unit economics, value capture, valuation/pricing, counter-supply, or second-order beneficiaries.
   - Each L3 question must be tied to a score driver such as future space, chokepoint strength, valuation odds, evidence quality, disconfirming-risk control, monitorability, payoff convexity, target ranking, or action state.
   - Delete or rewrite questions that cannot change a parent conclusion, target strength, valuation odds, or risk controls.

2. Source planning pass
   - Use `research-source-planner`.
   - Each L3 question must have a concrete source plan across evidence, research_report, message, and opinion where relevant.
   - For mechanism-depth questions, the source plan must name the exact fields needed to fill the model: period, unit/currency, volume, price, mix, capacity, utilization, cost, margin, capex, FCF, valuation multiple, implied expectation, and口径 when relevant.
   - The stored `source_plan` must be structured by concrete source, expected fields, source bucket, visible date/cutoff status, allowed usage, preferred parser skill, and historical-mode `availability_proof` when applicable. A prose-only source plan is insufficient for refreshed canonical reports.
   - Each supporting source plan must have a refuting or boundary-check source plan.
   - The source plan must name the preferred parser skill and whether DeepSeek MCP should do first-pass reading.
   - The source plan must name expected `source_extractions.jsonl` records to create. Each selected concrete source should map to at least one L3 extraction record unless GPT records a direct-parse fallback.
   - In historical training/backtest mode, the source plan must also name the source-visible date, cutoff status, and availability proof for each planned material. Availability proof can be publisher date, filing timestamp, archive timestamp, release page date, or dataset snapshot note; declared dates without proof are not enough for thesis use.

Default QA directions for industry/theme opportunity:

1. Q1: Confirm demand.
2. Q2: Locate bottlenecks.
3. Q3: Bind disconfirming tests.
4. Q4: Target observation list with reasons.

For other research types, use the adapted Q1-Q4 map. Each Q direction should state its own sub-plan and then run the corresponding QA subtree.

## Chokepoint Evaluation Protocol

For industry/theme opportunity and technology/product-route research, the domain playbook must add a chokepoint evaluation whenever value capture depends on scarce supply, workflow control, proprietary data, distribution, trust, regulation, or another hard-to-bypass constraint.

The chokepoint scorecard belongs inside the relevant Q2 bottleneck node, usually Q2.1. It must not become a top-level appendix or a component parallel to the QA tree.

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

## Supply-Chain Panorama

Every refreshed canonical report must include `产业链全景` before `问题下钻`.

This section is the shared map for later reasoning. It must describe:

- upstream, midstream, downstream, infrastructure, ecosystem, and end-demand layers when applicable;
- key listed and private players;
- products and services each player provides;
- dependency links: who supplies whom, who controls access, and who bears cost;
- value/profit flow: revenue, margin, cash flow, bargaining power, and capital intensity;
- candidate chokepoints: scarce, monopolistic, hard-to-substitute, qualification-heavy, proprietary, regulated, trusted, or ecosystem-locked nodes;
- the Q2/Q4 nodes that should use each chain-map insight.

Render this as `supply-chain-section` with:

- `chain-explain` and `chain-plain-summary`: a short Chinese explanation of what the chain does.
- `chain-flow-steps`: 3-7 steps showing who provides what, who pays whom, and how product/order/money/data flows.
- `chain-layer-grid` and `chain-layer-card`: beginner-readable cards for upstream, midstream, downstream, platform/ecosystem, customers, and other relevant layers.
- `chain-chokepoints`: candidate bottlenecks in plain Chinese, with why each is scarce or hard to substitute.
- `chain-target-links`: how those bottlenecks map to possible listed targets and the Q2/Q4 nodes that will test them.
- `chain-map` or `chain-table`: the auditable structured map.

It is not a process appendix and should not describe framework changes. It is a research artifact that prevents target selection from jumping straight to familiar company names.

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
- Simplified odds model: implied expectation, base path, bull path, bear path, and upgrade/downgrade data.
- Prediction review fields: initial claim, validation horizon, required evidence, current status, and next review trigger.
- Action state: `actionable_long`, `watch_only`, or `no_action`, with gate reasons when not actionable.
- Deterministic rank: sort from frozen score fields by action-state priority, opportunity fit, total score, payoff convexity, thesis confidence, then ticker/name tie-break; do not manually reorder after labels.
- Hard thesis kill tests: any `actionable_long` target must list test, evidence needed, downgrade action, and source plan. If kill tests are missing, cap at `watch_only`.

The simplified odds model is not a price target or trading instruction. If current valuation data is stale, incomplete, or source quality is weak, mark odds as unverified and do not raise target strength.

## QA Drilldown

Use at most three layers by default:

- Q1: main research direction.
- Q1.1: mechanism question.
- Q1.1.1: evidence-collection unit.

Do not put too many unrelated L3 leaves under one catch-all L2. L2 should group L3 leaves into mechanism buckets selected by the research-type adapter and domain playbook. If an L1 has only one L2 but many L3 leaves, split the L2 layer before polishing the report.

The report must proceed through the QA tree directly:

- Q1 owns the first adapted research direction. For industry/theme opportunity this is demand analysis.
- Q2 owns the second adapted research direction. For industry/theme opportunity this is bottleneck/value-capture analysis.
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

- Bottleneck scorecards belong under the bottleneck question they answer, usually Q2.1.
- Disconfirming-test lists belong under the risk question they answer, usually Q3.1.
- Target observation tables belong under the target-selection question they answer, usually Q4.1.

Every parent answer must roll up only from child answers and auditable sources.

L3 is the smallest research unit. Each L3 answer must include:

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

An L3 answer must also be structurally sufficient for the question type. If the leaf asks "how does X map to Y", "which is tighter", "how does valuation rerate", "which target captures value", or any other mechanism question, the answer needs a concrete answer artifact inside `当前结论呈现`: mapping table, driver table, bridge table, ranking table, scenario table, score table, or kill-test table. The artifact is not a process appendix; it is the actual answer. A fact paragraph plus source chips is insufficient when the reader cannot see how the evidence answers the L3 question.

For every L3 question:

1. GPT decides which materials to search or read and why.
2. GPT defines the source priority and extraction schema.
3. GPT classifies the leaf task family and routes it through the specialty skill dispatch layer when useful.
4. DeepSeek MCP or the selected specialty skill carefully processes the selected concrete materials and drafts the first structured L3 answer.
5. Persist each source-parser output as one `source_extractions.jsonl` record.
6. Each parser output must fill `schema_fields` for the L3 `extraction_schema`. If the parser returns only a generic note, GPT must either map it into the schema during verification or mark it incomplete.
7. GPT verifies each extraction and writes one `leaf_source_reviews.jsonl` record.
8. The verified draft L3 answer must include fact, inference, preliminary judgment, gap, trigger, source links, and support/refute/lead stance.
9. GPT resolves conflicts, corrects unsupported claims, and writes the final L3 answer.
10. Parent Q1/Q1.1 rollups may only use GPT-verified L3 answers.

Every L3 answer must preserve this dispatch trace:

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
| Supply-chain panorama | `supply-chain-panorama-explainer` | public `产业链全景` explanation before Q1-Q4 | plain Chinese summary, flow steps, layer cards, chokepoints, target/Q2/Q4 links |
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

1. GPT selects one concrete source or a small source bundle for one L3 question.
2. DeepSeek MCP reads only that material and returns structured extraction.
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
  - Top-level order is exactly `当前研究目标` -> `产业链全景` -> `问题下钻` -> `最终标的推荐` -> `来源索引`.
  - `产业链全景` is mandatory and must render as `supply-chain-section` with `chain-explain`, `chain-plain-summary`, `chain-flow-steps`, `chain-layer-grid`, `chain-layer-card`, `chain-chokepoints`, `chain-target-links`, and `chain-map` or `chain-table`, covering upstream, midstream, downstream, key players, products/services, dependencies, value/profit flow, and candidate chokepoints in beginner-readable Chinese.
  - `问题下钻` preserves the full adapted Q1-Q4 QA tree and must render L3 leaf questions in complete refreshed reports unless the user explicitly asks for a shorter executive version.
  - Q4 remains the auditable as-of target-selection QA node with child questions.
  - `最终标的推荐` is a standalone presentation rollup, not a replacement for Q4.
  - The hierarchy and format rules in `research_report_contract.md` are validation requirements. A complete refreshed report is invalid if it drops L3, moves Q4 out of `问题下钻`, duplicates child-question lists beside inline cards, replaces the canonical component family, or adds public process appendices.
  - Four non-drift locks must always hold: hierarchy and format lock, supply-chain map lock, backtest time-slice lock, and frontend card-style lock. In backtest mode, only cutoff-visible information can drive source collection, QA reasoning, scoring, odds, and target ranking; the only current-time data allowed in final HTML is the final-target evaluation label.
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
- Final HTML must use exactly five top-level sections: `当前研究目标`, `产业链全景`, `问题下钻`, `最终标的推荐`, `来源索引`.
- The final target recommendation section must rank specific targets by synthesized win probability and payoff odds, while keeping Q4 as the auditable QA source of the target logic.
- Do not render process metadata, iteration diffs, execution traces, quality-framework explanations, tool/delegation attribution, or workbench appendices in final HTML.
- Preserve full QA depth in the final report; do not replace the QA tree with a compressed Q1-Q4 summary unless the user explicitly requests a brief version.
- Inside every QA card/details node, use a consistent three-part display: `1. 当前结论呈现`, `2. 问题展开（子 QA）`, `3. 待补充的问题`.
- Every visible L3 card must show a compact `Skill` / `Execution` / `Score Component` / `Decision Use` strip inside `1. 当前结论呈现`. `Skill` is the intended specialty lens; `Execution` is the actual parser/delegation state from `skill_output_status` and `fallback_used`. This makes the question architecture and specialty dispatch visible without rendering the full source-parser trace.
- If child QA nodes are rendered inline as expandable cards, do not also render a separate child-question list with the same titles. The question expansion section should contain either jump links or inline child cards, not both.
- Put answer-presentation artifacts under `当前结论呈现` before child QA expansion.
- Keep source indexes collapsed by default unless the user explicitly asks to inspect sources.
- Use the canonical frontend component family defined in `research_report_contract.md` for refreshed reports: `supply-chain-section` with `chain-explain`, `chain-plain-summary`, `chain-flow-steps`, `chain-layer-grid`, `chain-layer-card`, `chain-chokepoints`, `chain-target-links`, and `chain-map` or `chain-table`; `qa-card`; `artifact-card`; `target-section` + `target-table`; and one collapsed `source-collapse`. Do not introduce visually divergent component families unless the user explicitly asks for a frontend redesign.
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
