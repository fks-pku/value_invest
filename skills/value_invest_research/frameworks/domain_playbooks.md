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

- Q1 Demand reality: convert AI, data-center, and terminal demand into sustainable bit demand, ASP, and product mix by workload and product type.
- Q2 Value-capture bottlenecks: test whether HBM/high-end DRAM, NAND/eSSD, nearline HDD, controller/IP, capacity, equipment, materials, and packaging constraints have scarcity, pricing power, and financial conversion.
- Q3 Disconfirming tests and priced-in risk: capacity additions, inventory, ASP decline, substitute architectures, customer capex digestion, China supply, mid-cycle downside, and valuation already priced in.
- Q4 Target observation list: memory makers, equipment/materials, controllers, storage devices, and regional/local listings reconciled with scarcity, mispricing, earnings elasticity, risk control, valuation odds, and kill tests.

Required L2 mechanism buckets:

- Workload-to-product demand: training/inference/RAG/Agent/database/data-lake/terminal workload -> HBM/DDR5/LPDDR/NAND/eSSD/nearline HDD demand, with evidence that it is not merely inventory restocking.
- Price/volume/mix/inventory bridge: split revenue and profit growth into bit shipment, ASP, mix, utilization, inventory, contract price, spot price, prepayment, and long-term agreement drivers.
- Demand-supply slope mismatch: demand multiplier versus wafer starts, cleanroom, bit growth, HBM conversion, NAND layer additions, HDD exabyte capacity, and ramp timing.
- HBM/high-end DRAM scarcity: customer qualification, TSV/stacking, advanced packaging, yield, HBM3E/HBM4 migration, share shift, prepayment, long-term agreements, ASP, and gross margin.
- NAND/eSSD/nearline HDD cash-flow economics: eSSD/NAND margin and FCF conversion, HDD supply discipline, long-term agreements, exabyte shipments, and whether the node is a structural bottleneck or cyclical beta.
- Controller/IP and firmware capture: controller revenue, design wins, customer concentration, margin durability, and internalization risk by NAND makers or hyperscalers.
- Capacity/equipment/materials second-order chain: capex plan, equipment order/backlog, lead time, packaging/test bottlenecks, supplier exposure, and whether second-order beneficiaries have stronger or weaker payoff convexity than memory makers.
- Company value capture: map Micron, SK Hynix, Samsung, Kioxia/SanDisk/WDC, Seagate, Silicon Motion, YMTC/CXMT, equipment/material names, and relevant local listings to node exposure, margin, capex, inventory, FCF, and shareholder return.
- Counter-supply and substitution: new fabs, China supply, customer qualification, cloud capex pullback, inventory rebuild exhaustion, HBM supply catch-up, NAND oversupply, customer self-design, memory-intensity optimization, and architecture changes.
- Market-pricing and rerating: reverse current market cap, P/E, P/B, EV/EBITDA, FCF yield, implied bit growth, ASP, margin, and mid-cycle downside before upgrading target strength.
- Monitoring and kill tests: define red/yellow/green quarterly thresholds by node and target. A high-conviction target must have observable data that can downgrade it.
- Model口径 reconciliation: compare sell-side/industry/internal models by TAM, wafer capacity, bit growth, ASP, revenue, operating profit, capex, margin definitions, period, unit, and currency before adopting numbers.

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

## Optical Module Playbook

Use this playbook for optical transceivers, AI datacenter optical modules, 800G/1.6T/3.2T upgrades, LPO/CPO, silicon photonics, lasers, optical components, and optical manufacturing capacity research.

Default Q map:

- Q1 Demand reality: AI datacenter network upgrades, switch port count, 800G/1.6T speed transition, customer capex, and order visibility.
- Q2 Value-capture bottlenecks: lasers, InP/silicon photonics, DSP/driver/TIA, optical components, module integration, qualification, yield, and manufacturing capacity.
- Q3 Disconfirming tests and priced-in risk: LPO/CPO/substitution, copper and OCS architecture changes, capacity expansion, ASP erosion, customer concentration, geopolitics, and valuation already priced in.
- Q4 Target observation list: module makers, laser/component suppliers, EMS/manufacturing names, silicon-photonics/chip beneficiaries, and regional listings reconciled with chokepoint score, financial conversion, valuation odds, and kill tests.

Required L2 mechanism buckets:

- AI cluster network demand: GPU/ASIC cluster size, scale-out/scale-up network, switch radix, port count, optical attach rate, and customer capex.
- Speed transition and product mix: 400G -> 800G -> 1.6T/3.2T shipment, ASP, product mix, power, thermal envelope, customer qualification, and platform timing.
- Customer order visibility: NVIDIA/hyperscaler purchase agreements, capacity reservations, long-term orders, customer concentration, backlog, and inventory risk.
- Laser/InP/silicon photonics bottleneck: EML/InP wafer, laser capacity, silicon photonics adoption, component shortage, gross margin, and supplier qualification.
- DSP/driver/TIA and electrical bottleneck: DSP suppliers, linear-drive/LPO architecture, driver/TIA, BOM share, and whether value shifts from module makers to chip vendors.
- Module integration, yield, and qualification: module manufacturing, thermal design, testing, yield, delivery stability, qualification barrier, and margin bridge.
- Manufacturing and EMS beta: Fabrinet/EMS capacity, utilization, customer mix, margin, capex, and whether the node is scarce or only follows volume.
- Technology substitution: LPO/CPO, co-packaged optics, copper reach, optical circuit switching, silicon photonics integration, and whether these raise or reduce the value of pluggable modules.
- Market-pricing and rerating: current market cap, P/E, EV/EBITDA, revenue/margin expectations, implied growth duration, and downside if ASP or capex rolls over.
- Monitoring and kill tests: quarterly revenue, gross margin, backlog, capex, customer order, ASP, qualification win/loss, inventory, and technology roadmap changes.
- Model口径 reconciliation: compare market reports and company disclosures by shipment unit, speed mix, ASP, revenue scope, module/component split, calendar/fiscal period, and currency.

Required extraction schemas:

- `optical_port_demand`: customer/platform, cluster scale, switch speed, port count, optical attach rate, module speed, shipment estimate, period, source.
- `optical_component_capacity`: component type, supplier, capacity, lead time, shortage status, expansion timing, margin, qualification, source.
- `optical_module_unit_economics`: company/product, 800G/1.6T mix, ASP, gross margin, revenue, inventory, capex, cash flow, period, source.
- `optical_customer_order_visibility`: customer, supplier, order/backlog, prepayment/capacity reservation, qualification status, concentration risk, source.
- `optical_valuation_rerating`: company, market cap/EV, multiples, revenue/earnings expectations, implied growth, margin assumption, peer set, source.
- `optical_model_reconciliation`: model/source, shipment, ASP, revenue, product split, period, unit, scope, formula, adoption status.

Scoring adjustments:

- `future_space` must include port-count logic, speed mix, optical attach rate, and customer capex durability.
- `chokepoint_strength` must include component scarcity, qualification, yield, capacity reservation, and substitution risk.
- `valuation_odds` must check whether 800G/1.6T growth and high margins are already priced.
- `disconfirming_risk_control` must include CPO/LPO/copper/OCS substitution, ASP erosion, capacity expansion, customer concentration, and geopolitics.
- `payoff_convexity` must separate module revenue growth, component margin leverage, manufacturing beta, and multiple rerating.
