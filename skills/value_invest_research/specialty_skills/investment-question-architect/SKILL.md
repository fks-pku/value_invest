---
name: investment-question-architect
description: Use this skill whenever a user proposes an investment research goal and the next step is to design a professional, investment-oriented QA tree. It turns a topic, company, sector, event, or technology route into a max-three-layer question plan with materiality, source needs, disconfirming tests, and target implications before evidence collection starts.
---

# Investment Question Architect

This skill designs the questions that determine research depth. It does not write the final report and does not make investment recommendations.

## Role

Build a professional question tree from an investment research goal:

1. Classify the research type.
2. Define the supply-chain map schema.
3. Define the Q1-Q4 map.
4. Create L1/L2/L3 questions.
4. Explain why each question matters for investment judgment.
5. Define what evidence would answer or refute each L3 question.

## Research Type Adapter

Use the project default mapping unless the topic clearly requires a custom map:

| Type | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| Industry/theme | Demand reality and future space | Value-capture bottlenecks | Disconfirming tests and priced-in risk | Specific target observation list |
| Single company | Growth drivers | Moat, unit economics, and value capture | Financial quality, valuation, and disconfirming tests | Observation decision and monitoring list |
| Event/policy | Fact boundary and scope | Transmission mechanism | Beneficiaries, losers, and second-order effects | Disconfirming tests and watchlist |
| Event/conference opportunity | Official fact boundary and new-information delta | Transmission chain and supply-chain chokepoints | Disconfirming tests and priced-in risk | Specific target observation list and ranking |
| Technology/product route | Technical feasibility and adoption demand | Bottlenecks and ecosystem readiness | Commercialization and competition | Exposed assets and monitoring list |
| Target update | What changed | Which thesis node changed | Whether price/risk/reward changed | Observation-strength update |

## Question Quality Bar

For every refreshed canonical research plan, create a supply-chain map before Q1-Q4. It should map upstream, midstream, downstream, infrastructure/ecosystem, customers/end demand, key players, products/services, dependency links, value/profit flow, and candidate chokepoints. This prevents the QA tree from jumping directly to familiar tickers before the industry structure is understood.

For conferences, keynotes, product launches, investor days, and other public events, use the event/conference opportunity adapter unless the user asks for a different lens. L2 buckets must cover official fact boundary, new-information delta, event-to-order/revenue/margin bridge, supply-chain chokepoint, company exposure, valuation/priced-in risk, and target ranking. Preferred L3 skills are `event-to-investment-analysis`, `conference-transcript-analysis`, `supply-chain-chokepoint-analysis`, `company-exposure-analysis`, `valuation-analysis`, and `target-ranking-analysis`.

For industry/theme opportunity and technology/product-route research, Q2 must include an explicit chokepoint evaluation if value capture depends on scarce supply, workflow control, proprietary data, distribution, trust, regulation, or another hard-to-bypass constraint. The L2/L3 tree should ask what demand reaches the node, why the node is irreplaceable, what constrains supply or access, whether pricing power and financial conversion are visible, whether the market has already priced it, and what would refute it.

For model-heavy industry/theme research, build a mechanism-depth map before accepting the QA tree. The tree should be able to reconstruct the thesis from drivers, not just summarize the narrative. Cover these blocks when relevant:

- Demand driver tree: end need/workload/customer -> product demand -> volume, price, mix, duration.
- Supply or access response: capacity, utilization, inventory, lead time, capex, qualification, regulation, data, distribution, or trust limits.
- Unit economics and profit bridge: ASP/take rate, cost, gross margin, operating margin, FCF, capex intensity, and working capital.
- Competitive value-capture map: which companies/assets capture value and what substitutes or internal builds bypass them.
- Market-pricing bridge: current valuation, implied growth/margins, cyclicality discount, risk premium, or rerating path.
- Disconfirming and counter-supply tests: evidence that would invalidate demand, bottleneck, pricing, or scarcity.
- Capital-chain or second-order beneficiaries: equipment, materials, infrastructure, channels, or downstream nodes created by high returns.
- Model and口径 reconciliation: period, unit, currency, scope, formula, and margin definition differences across sources.

Every L3 question must be:

- Answerable with concrete materials.
- Relevant to future fundamentals, valuation, risk, or target selection.
- Capable of support and refutation.
- Specific enough to assign to a source parser.
- Designed to roll up to its parent node.
- Tied to a specific scoring or action driver, not merely interesting background.
- Protected by a minimum evidence gate and a refuting-source plan before it can strengthen a thesis.

Avoid questions that only ask for background, definitions, or broad summaries unless the topic is genuinely unknown and background facts are the investment bottleneck.

## Required Output

Return a structured plan:

- `research_type`
- `supply_chain_map`: layers, players, products/services, dependencies, value/profit flow, candidate chokepoints, and Q2/Q4 links
- `q_map`
- `planner_rationale`
- `mechanism_depth_map` for industry/theme or technology-route research, including which blocks are included, omitted, and why
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
  - `materiality`
  - `required_materials`
  - `support_evidence`
  - `refute_evidence`
  - `target_implications`
  - `score_component`
  - `minimum_evidence_gate`
  - `refuting_source_plan`
  - `preferred_specialty_skill`

## Guardrails

- Do not answer the research questions yet.
- Do not produce buy/sell/hold instructions.
- If a question cannot influence investment judgment, remove or rewrite it.
- If Q4 has target implications, require specific securities or assets rather than broad directions.
