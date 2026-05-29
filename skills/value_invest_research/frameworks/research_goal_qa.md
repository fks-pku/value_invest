# Research Goal QA Framework

This is the only active research framework for this project.

Use it whenever the user proposes a research goal, topic, company, sector, event, concept, or investment question.

Final report presentation is governed by `research_report_contract.md`. Follow that contract for all future user-facing HTML reports unless the user explicitly asks to iterate on the framework.

## Output Order

Final user-facing HTML reports must use exactly this top-level order:

1. Current research goal.
2. Question drilldown.
3. Final target recommendation.
4. Source index.

The final target recommendation is a research conclusion section. It must synthesize all QA evidence into a ranked observation list with specific targets, win probability, payoff odds, rationale, required verification data, and downgrade triggers. It must not issue buy/sell/hold instructions.

Research type adaptation, question architecture, source planning, specialty parsing, GPT verification, tool attribution, and iteration notes are internal process artifacts. Store them in workbench JSON, logs, or internal files; do not render them as top-level HTML report sections unless the user explicitly asks to inspect process.

Do not append a generic full report, workbench appendix, or any other research template.

Do not compress away QA depth when refreshing a report. Preserve the full available QA tree and all answered questions unless the user explicitly asks for an executive version.

## Persistent Framework Changes

When the user changes a report structure, interaction pattern, section order, or presentation logic, treat that change as a persistent default research-system requirement unless the user explicitly says it is one-off.

In the same change, update:

- `AGENTS.md`
- `skills/value_invest_research/SKILL.md`
- `skills/value_invest_research/frameworks/research_goal_qa.md`

Future reports must use the latest framework requirement.

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

Default research types:

| Type | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| Industry/theme opportunity | Demand reality | Value-capture bottlenecks | Disconfirming tests and priced-in risk | Target observation list |
| Single company | Growth drivers | Moat, unit economics, and value capture | Financial quality, valuation, and disconfirming tests | Observation decision and monitoring list |
| Event/policy | Event facts and scope | Transmission mechanism | Beneficiaries, losers, and second-order effects | Disconfirming tests and watchlist |
| Technology/product route | Technical feasibility and adoption demand | Bottlenecks and ecosystem readiness | Commercialization, competition, and disconfirming tests | Exposed assets and monitoring list |
| Target update | What changed | Which thesis node changed | Whether price/risk/reward changed | Update action for observation strength |

If the topic does not fit a default type, define a custom Q1-Q4 map in the execution plan. Do not force demand/bottleneck/target wording onto company, event, policy, or technology-route questions when it weakens the research.

## Research Execution Plan

For every level, explicitly state:

- What questions to ask.
- How to collect information.
- How to connect the information into reasoning.
- How to present the output.

The execution plan is part of the internal workbench output, not the final user-facing HTML by default. It should make the method auditable before the system starts collecting more detail, but the final report should stay research-first and only show the current goal, QA drilldown, final target recommendation, and source index.

Before evidence collection, run two quality-control passes:

1. Question architecture pass
   - Use `investment-question-architect`.
   - Each L3 question must state decision use, materiality, required materials, support evidence, refuting evidence, target implications, and preferred specialty skill.
   - Delete or rewrite questions that cannot change a parent conclusion, target strength, valuation odds, or risk controls.

2. Source planning pass
   - Use `research-source-planner`.
   - Each L3 question must have a concrete source plan across evidence, research_report, message, and opinion where relevant.
   - Each supporting source plan must have a refuting or boundary-check source plan.
   - The source plan must name the preferred parser skill and whether DeepSeek MCP should do first-pass reading.

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

Q4 target observation lists must also include:

- Score breakdown: chokepoint strength, future space, valuation odds, evidence quality, disconfirming-risk control, and monitorability.
- Simplified odds model: implied expectation, base path, bull path, bear path, and upgrade/downgrade data.
- Prediction review fields: initial claim, validation horizon, required evidence, current status, and next review trigger.

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
- Source plan.
- Skill dispatch trace.
- Fact.
- Inference.
- Judgment.
- Gap.
- Trigger.
- Source links.

For every L3 question:

1. GPT decides which materials to search or read and why.
2. GPT defines the source priority and extraction schema.
3. GPT classifies the leaf task family and routes it through the specialty skill dispatch layer when useful.
4. DeepSeek MCP or the selected specialty skill carefully processes the selected concrete materials and drafts the first structured L3 answer.
5. The draft L3 answer must include fact, inference, preliminary judgment, gap, trigger, source links, and support/refute/lead stance.
6. GPT verifies the draft against source links or local files, resolves conflicts, corrects unsupported claims, and writes the final L3 answer.
7. Parent Q1/Q1.1 rollups may only use GPT-verified L3 answers.

Every L3 answer must preserve this dispatch trace:

- `task_family`
- `selected_skill`
- `concrete_materials`
- `extraction_schema`
- `source_plan`
- `skill_output_status`
- `fallback_used`
- `gpt_verification_status`

## Specialty Skill Dispatch

Specialized skills are used for leaf-level processing. They do not replace the QA framework and do not make final investment judgments.

Before running an L3 task, classify it into one or more task families:

| Task family | Preferred skill | Use for | Required output discipline |
|---|---|---|---|
| Question architecture | `investment-question-architect` | Research type classification, Q1-Q4 map, L1/L2/L3 question design | decision-use questions, materiality, support/refute tests, target implications |
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

This section is a research observation list, not a buy/sell instruction.

## HTML Presentation

Use Apple-inspired presentation:

- White/light-gray surfaces.
- SF-system typography.
- Restrained borders.
- Clean spacing.
- Low-noise cards.
- Blue links for concrete sources.
- Final HTML must use exactly four top-level sections: `当前研究目标`, `问题下钻`, `最终标的推荐`, `来源索引`.
- The final target recommendation section must rank specific targets by synthesized win probability and payoff odds, while keeping Q4 as the auditable QA source of the target logic.
- Do not render process metadata, iteration diffs, execution traces, quality-framework explanations, tool/delegation attribution, or workbench appendices in final HTML.
- Preserve full QA depth in the final report; do not replace the QA tree with a compressed Q1-Q4 summary unless the user explicitly requests a brief version.
- Inside every QA card/details node, use a consistent three-part display: `1. 当前结论呈现`, `2. 问题展开（子 QA）`, `3. 待补充的问题`.
- If child QA nodes are rendered inline as expandable cards, do not also render a separate child-question list with the same titles. The question expansion section should contain either jump links or inline child cards, not both.
- Put answer-presentation artifacts under `当前结论呈现` before child QA expansion.
- Keep source indexes collapsed by default unless the user explicitly asks to inspect sources.
- Use the canonical frontend component family defined in `research_report_contract.md` for refreshed reports: `qa-card`, `artifact-card`, `target-section` + `target-table`, and one collapsed `source-collapse`. Do not introduce visually divergent component families unless the user explicitly asks for a frontend redesign.

Default page order:

1. Current research goal.
2. Question drilldown: Q1-Q4 as top-level QA cards, with all scorecards, risk tests, target tables, and supporting details nested under the relevant question.
3. Final target recommendation, synthesized from Q1-Q4.
4. Source index, collapsed by default.
