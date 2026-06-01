# Domain Playbooks

Domain playbooks are the depth layer under the shared QA/report contract. The public report contract fixes hierarchy and presentation; this file fixes how a domain should become concrete L2/L3 mechanism questions, source plans, extraction schemas, and scoring inputs.

## Mechanism Depth Protocol

For industry/theme opportunity and technology/product-route research, the question architect must build a mechanism-depth map before source collection. The map prevents generic "theme looks good" reports by forcing the research to model how demand turns into company cash flow and how the market may already price it.

Before Q1-Q4, the architect must also build the public `产业链全景` map. This map should cover upstream, midstream, downstream, infrastructure/ecosystem layers, key players, products/services, dependency links, value/profit flow, and candidate chokepoints. It is the coordinate system for Q2 value-capture and Q4 target ranking.

Every applicable domain playbook should cover these blocks unless the research object makes a block irrelevant:

1. Demand driver tree: end workload/customer need -> product demand -> volume, price, mix, and duration.
2. Supply or access response: capacity, utilization, inventory, lead time, capex, regulation, distribution, data, or trust constraints.
3. Unit economics and profit bridge: ASP/take rate, cost, gross margin, operating margin, FCF, capex intensity, and working-capital pressure.
4. Competitive value-capture map: which companies or assets capture revenue/profit at each node; what substitution or internalization path can bypass them.
5. Market-pricing bridge: current market cap/multiples/discount rate/implied growth versus the required fundamental path.
6. Disconfirming and counter-supply tests: what evidence would prove demand is overstated, bottlenecks are temporary, pricing is peaking, or supply will catch up.
7. Capital-chain and second-order beneficiaries: whether high returns pull capex into equipment, materials, infrastructure, channels, or downstream adopters.
8. Model and口径 reconciliation: compare external models by period, unit, currency, revenue/profit/capex scope, and margin definition before adopting numbers.

Each L3 extraction schema should prefer structured rows over prose:

- metric or assumption
- period
- unit/currency
- source value
- formula or derivation when available
- source bucket
- support/refute/lead stance
- uncertainty or口径 caveat
- parent QA node and score component affected

Every domain playbook should define a supply-chain map schema with at least:

- layer
- players
- products/services
- dependency links
- value/profit flow
- candidate chokepoints
- downstream demand or customer link
- related Q2/Q4 node

Target scoring should roll component evidence into four core dimensions: `scarcity_or_monopoly`, `mispricing`, `earnings_elasticity`, and `risk_control`. The older component family remains the audit layer under those dimensions.

## Memory Industry Playbook

Use this playbook for DRAM, HBM, NAND, eSSD, HDD/nearline, memory controllers, memory equipment, and memory-cycle opportunity research.

Default Q map:

- Q1 Demand reality: AI data-center, general data-center, device, and non-DC demand by workload and product type.
- Q2 Value-capture bottlenecks: HBM/high-end DRAM, commodity DRAM, NAND/eSSD, nearline HDD, controller/IP, manufacturing capacity, and equipment/process constraints.
- Q3 Disconfirming tests and priced-in risk: capacity additions, inventory, ASP decline, substitute architectures, customer capex digestion, China supply, and valuation already priced in.
- Q4 Target observation list: memory makers, equipment/materials, controllers, storage devices, and regional/local listings reconciled with chokepoint score, financial conversion, valuation odds, and kill tests.

Required L2 mechanism buckets:

- Workload-to-memory demand: token/RAG/Agent/video/inference/training workload -> HBM/DRAM/NAND/eSSD/HDD/LPDDR demand.
- Demand-supply slope mismatch: demand multiplier versus wafer starts, cleanroom, bit growth, HBM stack capacity, NAND layer additions, and HDD capacity.
- Product price and unit economics: ASP, cost per bit, mix, utilization, margin bridge, inventory, and contract/spot pricing.
- Company value capture: Samsung, SK Hynix, Micron, Kioxia/SanDisk/WDC, YMTC/CXMT, controller/device vendors, and other relevant local listings.
- Capital return and capex cycle: capex intensity, FCF conversion, shareholder return, fab payback, and equipment order transmission.
- Market-pricing and rerating: cyclicality discount, risk premium, P/E, P/B, EV/EBITDA, FCF yield, and implied growth/margin expectations.
- Counter-supply and substitution: new fabs, China supply, customer qualification, cloud capex pullback, inventory rebuild exhaustion, HBM supply catch-up, NAND oversupply, and architecture changes.
- Model口径 reconciliation: compare sell-side/industry/internal models by TAM, wafer capacity, bit growth, ASP, revenue, operating profit, capex, and margin definitions.

Required extraction schemas:

- `memory_supply_capacity`: company, product, node/stack/layer, wafer starts or bit capacity, cleanroom status, period, capex, ramp timing, source.
- `memory_demand_driver`: workload/end market, token or data growth driver, product type, demand metric, period, multiplier, price/mix assumption, source.
- `memory_unit_economics`: company/product, ASP, cost per bit or unit cost, bit shipment, utilization, gross margin, operating margin, inventory, period, source.
- `memory_valuation_rerating`: company, market cap/EV, multiples, FCF yield, implied growth/margin, risk premium or discount-rate assumption, peer set, source.
- `memory_capital_chain`: company/node, capex, equipment intensity, payback period, supplier beneficiaries, order/lead indicators, source.
- `memory_model_reconciliation`: model/source, metric, period, value, unit, scope, formula, difference versus alternative model, adoption status.

Scoring adjustments:

- `future_space` must include demand-supply slope mismatch, not only TAM.
- `chokepoint_strength` must include supply/access constraint, qualification difficulty, and ramp lead time.
- `valuation_odds` must include implied cyclicality discount or rerating path when relevant.
- `disconfirming_risk_control` must include counter-supply, inventory, ASP, and customer capex tests.
- `payoff_convexity` must consider operating leverage, mix shift, and multiple rerating separately.
