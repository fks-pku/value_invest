# Research Goal QA Framework

This is the only active research framework for this project.

Use it whenever the user proposes a research goal, topic, company, sector, event, concept, or investment question.

## Output Order

1. Current research goal
2. Research type adaptation layer
3. Research execution plan
4. QA drilldown sections
5. Specialty skill dispatch for L3 leaf tasks
6. Evidence-linked synthesis inside each QA node
7. Specific target observation list inside the target-selection QA node

Do not append a generic full report, workbench appendix, or any other research template.

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

The execution plan is part of the research output. It should make the method auditable before the system starts collecting more detail.

Default QA directions for industry/theme opportunity:

1. Q1: Confirm demand.
2. Q2: Locate bottlenecks.
3. Q3: Bind disconfirming tests.
4. Q4: Target observation list with reasons.

For other research types, use the adapted Q1-Q4 map. Each Q direction should state its own sub-plan and then run the corresponding QA subtree.

## QA Drilldown

Use at most three layers by default:

- Q1: main research direction.
- Q1.1: mechanism question.
- Q1.1.1: evidence-collection unit.

The report must proceed through the QA tree directly:

- Q1 owns the first adapted research direction. For industry/theme opportunity this is demand analysis.
- Q2 owns the second adapted research direction. For industry/theme opportunity this is bottleneck/value-capture analysis.
- Q3 owns disconfirming tests, valuation/odds checks, risk triggers, or the adapted third direction.
- Q4 owns target observation tables, monitoring lists, decision updates, or the adapted fourth direction.

Details, scorecards, tables, and jump pages must live inside the QA layer whose question they answer. Do not place them as Q-parallel components or unrelated top-level appendices.

Presentation artifacts are answer formats, not structural peers:

- Bottleneck scorecards belong under the bottleneck question they answer, usually Q2.1.
- Disconfirming-test lists belong under the risk question they answer, usually Q3.1.
- Target observation tables belong under the target-selection question they answer, usually Q4.1.

Every parent answer must roll up only from child answers and auditable sources.

L3 is the smallest research unit. Each L3 answer must include:

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
- `skill_output_status`
- `fallback_used`
- `gpt_verification_status`

## Specialty Skill Dispatch

Specialized skills are used for leaf-level processing. They do not replace the QA framework and do not make final investment judgments.

Before running an L3 task, classify it into one or more task families:

| Task family | Preferred skill | Use for | Required output discipline |
|---|---|---|---|
| Financial statement / filing parsing | `financial-statement-analysis` | 10-K, 10-Q, 20-F, annual reports, quarterly reports, earnings releases, segment data, capex, inventory, RPO/backlog, cash-flow quality | normalized financial facts, earnings-quality view, gaps, triggers |
| Valuation / priced-in expectations | `valuation-analysis` | multiples, FCF yield, reverse DCF, peer comparison, valuation sensitivity, margin of safety, market-implied growth/margins | market facts, implied assumptions, scenario table, odds judgment, disconfirming tests |
| Long source reading / first L3 draft | `leaf-research-deepseek` plus DeepSeek MCP | long reports, transcripts, filings, policy documents, expert interviews, extracted passages | source extraction with fact/inference/judgment/gap/trigger |
| Quantitative strategy / backtest | `quant-research-fks` or `quantitative-research` | factors, timing rules, systematic screens, backtests, walk-forward validation | hypothesis, data, implementation, backtest, risk limits |
| HTML/report interface | `frontend-design` | HTML dashboard, report readability, visual hierarchy, sticky metadata, table ergonomics | working HTML/CSS with verification |

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
- Required verification data.
- Catalysts.
- Risks.
- Source links.

This section is a research observation list, not a buy/sell instruction.

## HTML Presentation

Use Apple-inspired presentation:

- White/light-gray surfaces.
- SF-system typography.
- Restrained borders.
- Clean spacing.
- Low-noise cards.
- Blue links for concrete sources.

Default page order:

1. Current research goal.
2. Research type adaptation and execution plan.
3. QA drilldown: Q1, using the adapted meaning for the selected research type.
4. QA drilldown: Q2, with scorecards, financial tables, event maps, or detail links nested under the relevant question.
5. QA drilldown: Q3, with disconfirming tests, valuation checks, risk triggers, or policy/technical failure tests nested under the relevant question.
6. QA drilldown: Q4, with target observation lists, monitoring lists, or decision updates nested under the relevant question.
7. Specialty skill trace and source index.
