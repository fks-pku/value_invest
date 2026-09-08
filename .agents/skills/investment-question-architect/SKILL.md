---
name: investment-question-architect
description: Use this skill whenever a user proposes an investment research goal and the next step is to design a professional, investment-oriented QA tree. It creates an initial L1-L3 plan and grows deeper questions only when research exposes a concrete answerability gap, never beyond L5.
---

# Investment Question Architect

This skill designs the questions that determine research depth. It does not write the final report and does not make investment recommendations.

## Role

Build a professional question tree from an investment research goal:

1. Classify the research type.
2. Define the Q1-Q4 map.
3. Create the initial L1/L2/L3 questions and stop there.
4. Explain why each question matters for investment judgment.
5. For every current L3, define the data, analysis, gate, and refuting test required for the first research attempt.
6. After research, create L4 only for concrete gaps that blocked the L3 answer. Create L5 only when an L4 research attempt is still blocked. Add one level at a time.

## Research Type Adapter

Use the project default mapping unless the topic clearly requires a custom map:

| Type | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| Industry/theme | Industry space, demand reality, and future space | Competitive landscape and value capture, with chokepoint analysis as a submodule | Disconfirming tests and priced-in risk | Valuation odds and specific target observation list |
| Single company | Growth drivers | Moat, unit economics, and value capture | Financial quality, valuation, and disconfirming tests | Observation decision and monitoring list |
| Event/policy | Fact boundary and scope | Transmission mechanism | Beneficiaries, losers, and second-order effects | Disconfirming tests and watchlist |
| Technology/product route | Technical feasibility and adoption demand | Ecosystem/competitive landscape and value-capturing chokepoints | Commercialization and competition | Exposed assets and monitoring list |
| Target update | What changed | Which thesis node changed | Whether price/risk/reward changed | Observation-strength update |

## Question Quality Bar

For industry/theme opportunity and technology/product-route research, Q2 must analyze competitive landscape before chokepoint evaluation if value capture depends on scarce supply, workflow control, proprietary data, distribution, trust, regulation, or another hard-to-bypass constraint. Chokepoint is not the whole Q2; it is the conclusion after testing who competes in the node, what substitutes exist, how much bargaining power customers have, whether supply can expand, whether pricing power and financial conversion are visible, whether the market has already priced it, and what would refute it.

Every current terminal L3, L4, or L5 question must be:

- Answerable with concrete materials.
- Relevant to future fundamentals, valuation, risk, or target selection.
- Capable of support and refutation.
- Specific enough to assign to a source parser.
- Designed to roll up to its parent node.

An L3 or L4 terminates when its evidence gate passes and one coherent analysis can answer it. Continue one level only when the completed research attempt identifies a concrete unresolved entity, metric, period, route, mechanism, or contradiction. Never exceed L5, never pre-generate deeper branches, and never force every L3 into an identical branch template.

Avoid questions that only ask for background, definitions, or broad summaries unless the topic is genuinely unknown and background facts are the investment bottleneck.

## Required Output

Return a structured plan:

- `research_type`
- `q_map`
- `planner_rationale`
- `l1_questions`
- For each L1:
  - `question`
  - `investment_relevance`
  - `l2_questions`
- For each L2:
  - `question`
  - `why_this_depth`
  - `l3_questions`
- For each L3:
  - `question`
  - `decision_use`
  - `support_evidence`
  - `refute_evidence`
  - `target_implications`
  - `preferred_specialty_skill`
  - `required_data`
  - `analysis_plan`
  - `minimum_evidence_gate`
  - `refuting_source_plan`
- Only after a failed gate, for every newly created child:
  - `question`
  - `parent_question_id`
  - `expansion_trigger` with the concrete evidence gap
  - `required_data`
  - `analysis_plan`
  - `minimum_evidence_gate`
  - `refuting_source_plan`

## Guardrails

- Do not answer the research questions yet.
- Do not create L4/L5 during the initial architecture pass.
- Do not expand without a recorded failed answerability gate and concrete gap.
- Do not produce buy/sell/hold instructions.
- If a question cannot influence investment judgment, remove or rewrite it.
- If Q4 has target implications, require specific securities or assets rather than broad directions.
