# Research Goal QA Framework

This is the only active research framework for this project.

Use it whenever the user proposes a research goal, topic, company, sector, event, concept, or investment question.

## Output Order

1. Current research goal
2. Research execution plan
3. QA drilldown sections
4. Evidence-linked synthesis inside each QA node
5. Specific target observation list inside the target-selection QA node

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

## Research Execution Plan

For every level, explicitly state:

- What questions to ask.
- How to collect information.
- How to connect the information into reasoning.
- How to present the output.

The execution plan is part of the research output. It should make the method auditable before the system starts collecting more detail.

Default QA directions:

1. Q1: Confirm demand.
2. Q2: Locate bottlenecks.
3. Q3: Bind disconfirming tests.
4. Q4: Target observation list with reasons.

Each Q direction should state its own sub-plan and then run the corresponding QA subtree.

## QA Drilldown

Use at most three layers by default:

- Q1: main research direction.
- Q1.1: mechanism question.
- Q1.1.1: evidence-collection unit.

The report must proceed through the QA tree directly:

- Q1 owns demand analysis.
- Q2 owns bottleneck analysis.
- Q3 owns disconfirming tests and risk triggers.
- Q4 owns target observation table, reasons, strength, required verification data, catalysts, and risks.

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
3. DeepSeek MCP carefully reads the selected concrete materials and drafts the first structured L3 answer.
4. The DeepSeek L3 answer must include fact, inference, preliminary judgment, gap, trigger, source links, and support/refute/lead stance.
5. GPT verifies the DeepSeek answer against source links or local files, resolves conflicts, corrects unsupported claims, and writes the final L3 answer.
6. Parent Q1/Q1.1 rollups may only use GPT-verified L3 answers.

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
2. Research execution plan.
3. QA drilldown: Q1 demand, with its QA subtree.
4. QA drilldown: Q2 bottlenecks, with scorecards and detail-page links nested under the relevant bottleneck question.
5. QA drilldown: Q3 disconfirming tests, with trigger lists nested under the relevant risk question.
6. QA drilldown: Q4 target observation list, with target tables nested under the relevant target-selection question.
7. Source index.
