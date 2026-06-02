---
name: supply-chain-chokepoint-analysis
description: Use this skill when a research question asks which supply-chain node can capture value because of scarcity, irreplaceability, qualification, capacity, access, distribution, trust, data, regulation, or ecosystem lock-in. It builds the Q2 chokepoint score inputs.
---

# Supply Chain Chokepoint Analysis

This skill evaluates whether a supply-chain node is a real investment bottleneck or only theme exposure.

## Inputs

- Supply-chain map.
- Demand driver and product route.
- Candidate node and candidate listed targets.
- Source excerpts: company disclosures, customer requirements, industry reports, capacity data, pricing/margin data, and refuting evidence.

## Scorecard

Use this seven-part scorecard. Keep scores conservative when evidence is missing.

| Dimension | What To Test |
|---|---|
| demand_flow | Does incremental demand actually reach this node? |
| irreplaceability | Can customers bypass, substitute, dual-source, or internalize it? |
| supply_access_constraint | What scarce capacity, certification, data, trust, ecosystem, or regulation controls access? |
| pricing_power | Can the node raise price, take rate, margin, backlog quality, or prepayment? |
| financial_conversion | Does the node show up in revenue, gross margin, FCF, capex efficiency, or order visibility? |
| market_pricing | Is the scarcity already fully priced? |
| disconfirming_trigger | What data would prove the bottleneck temporary or false? |

## Rules

- A chokepoint requires both scarcity and monetization. Scarcity without company-level financial exposure is not enough.
- Customer qualification and switching cost matter more than broad TAM.
- Always name the strongest substitution path and the fastest counter-supply path.
- Output must feed Q2 and Q4 target ranking; it should not become a standalone report section.

## Output

- chokepoint score table with dimension scores, weights, evidence IDs/review IDs, and missing data.
- fact/inference/judgment/gap/trigger for the L3 QA card.
- target implications: which securities get upgraded, capped, or rejected by this node.
