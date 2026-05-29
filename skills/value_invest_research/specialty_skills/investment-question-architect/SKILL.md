---
name: investment-question-architect
description: Use this skill whenever a user proposes an investment research goal and the next step is to design a professional, investment-oriented QA tree. It turns a topic, company, sector, event, or technology route into a max-three-layer question plan with materiality, source needs, disconfirming tests, and target implications before evidence collection starts.
---

# Investment Question Architect

This skill designs the questions that determine research depth. It does not write the final report and does not make investment recommendations.

## Role

Build a professional question tree from an investment research goal:

1. Classify the research type.
2. Define the Q1-Q4 map.
3. Create L1/L2/L3 questions.
4. Explain why each question matters for investment judgment.
5. Define what evidence would answer or refute each L3 question.

## Research Type Adapter

Use the project default mapping unless the topic clearly requires a custom map:

| Type | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| Industry/theme | Demand reality and future space | Value-capture bottlenecks | Disconfirming tests and priced-in risk | Specific target observation list |
| Single company | Growth drivers | Moat, unit economics, and value capture | Financial quality, valuation, and disconfirming tests | Observation decision and monitoring list |
| Event/policy | Fact boundary and scope | Transmission mechanism | Beneficiaries, losers, and second-order effects | Disconfirming tests and watchlist |
| Technology/product route | Technical feasibility and adoption demand | Bottlenecks and ecosystem readiness | Commercialization and competition | Exposed assets and monitoring list |
| Target update | What changed | Which thesis node changed | Whether price/risk/reward changed | Observation-strength update |

## Question Quality Bar

For industry/theme opportunity and technology/product-route research, Q2 must include an explicit chokepoint evaluation if value capture depends on scarce supply, workflow control, proprietary data, distribution, trust, regulation, or another hard-to-bypass constraint. The L2/L3 tree should ask what demand reaches the node, why the node is irreplaceable, what constrains supply or access, whether pricing power and financial conversion are visible, whether the market has already priced it, and what would refute it.

Every L3 question must be:

- Answerable with concrete materials.
- Relevant to future fundamentals, valuation, risk, or target selection.
- Capable of support and refutation.
- Specific enough to assign to a source parser.
- Designed to roll up to its parent node.

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
  - `required_materials`
  - `support_evidence`
  - `refute_evidence`
  - `target_implications`
  - `preferred_specialty_skill`

## Guardrails

- Do not answer the research questions yet.
- Do not produce buy/sell/hold instructions.
- If a question cannot influence investment judgment, remove or rewrite it.
- If Q4 has target implications, require specific securities or assets rather than broad directions.
