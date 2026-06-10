# Domain Playbooks

Domain playbooks are the depth layer under the shared QA/report contract. The public report contract fixes hierarchy and presentation; this file fixes how a domain should become concrete L2/L3 mechanism questions, optional L4/L5 decomposition units, source plans, extraction schemas, and scoring inputs.

## Mechanism Depth Protocol

For industry/theme opportunity and technology/product-route research, the question architect must build a mechanism-depth map before source collection. The map prevents generic "theme looks good" reports by forcing the research to model how demand turns into company cash flow and how the market may already price it.

Before Q1-Q4, the architect must also build the public `产业链全景` map. This map should cover upstream, midstream, downstream, infrastructure/ecosystem layers, key players, products/services, dependency links, company relationship edges, value/profit flow, and candidate chokepoints. Each edge should explain from, to, relationship, product/order/value flow, bottleneck, target mapping, and evidence. It is the coordinate system for Q2 competitive-landscape/value-capture analysis and Q4 target ranking.

Every applicable domain playbook should cover these blocks unless the research object makes a block irrelevant:

1. Demand driver tree: end workload/customer need -> product demand -> volume, price, mix, and duration.
2. Supply or access response: capacity, utilization, inventory, lead time, capex, regulation, distribution, data, or trust constraints.
3. Unit economics and profit bridge: ASP/take rate, cost, gross margin, operating margin, FCF, capex intensity, and working-capital pressure.
4. Competitive value-capture map: which companies or assets capture revenue/profit at each node; what substitution or internalization path can bypass them.
5. Technology or product route comparison when route choice affects value capture: best-fit scenario, solved constraint, cost/power/performance/reliability/serviceability tradeoff, timing/evidence, beneficiaries, and substitution/refuting trigger.
6. Component/BOM value chain: subsystem, component/service, key companies, demand input, supply input, downstream recipient, financial validation metric, and QA link.
7. Bottleneck release timeline: current constraint, expansion/release owner, release/verification signal, observation cadence, downgrade trigger, and target implication.
8. Market-pricing bridge: current market cap/multiples/discount rate/implied growth versus the required fundamental path.
9. Disconfirming and counter-supply tests: what evidence would prove demand is overstated, bottlenecks are temporary, pricing is peaking, or supply will catch up.
10. Capital-chain and second-order beneficiaries: whether high returns pull capex into equipment, materials, infrastructure, channels, or downstream adopters.
11. Model and口径 reconciliation: compare external models by period, unit, currency, revenue/profit/capex scope, and margin definition before adopting numbers.

Each L3-L5 extraction schema should prefer structured rows over prose:

- metric or assumption
- period
- unit/currency
- source value
- formula or derivation when available
- source bucket
- support/refute/lead stance
- uncertainty or口径 caveat
- parent QA node and score component affected

Adaptive depth rule:

- Use L3 for investment decision questions.
- Use L4 when one L3 spans multiple companies, value-chain nodes, source families, financial bridges, valuation cases, or risk tests.
- Use L5 only for atomic work units such as one target financial bridge, one bottleneck score row, one source/model row, one valuation scenario, or one kill-test threshold.
- Do not go beyond L5. If L5 still feels too broad, rewrite L2/L3 instead of creating another level.

Every domain playbook should define a supply-chain map schema with at least:

- layer
- players
- products/services
- dependency links
- value/profit flow
- component/BOM rows when the industry depends on subsystem economics
- technology-route rows when competing routes change profit-pool allocation
- candidate chokepoints
- bottleneck-release rows for scarcity nodes
- downstream demand or customer link
- related Q2/Q4 node

Target scoring should roll component evidence into four core dimensions: `scarcity_or_monopoly`, `mispricing`, `earnings_elasticity`, and `risk_control`. The older component family remains the audit layer under those dimensions.

For final target recommendation, each playbook should define enough inputs to render `target-profit-bridge` and `target-valuation-table`: demand-to-revenue path, margin/FCF bridge, must-verify financial data, valuation-implied expectation, upgrade evidence, downgrade evidence, and action-state cap.

## Memory Industry Playbook

Use this playbook for DRAM, HBM, NAND, eSSD, HDD/nearline, memory controllers, memory equipment, and memory-cycle opportunity research.

Default Q map:

- Q1 Demand reality: convert AI, data-center, and terminal demand into sustainable bit demand, ASP, and product mix by workload and product type.
- Q2 Competitive landscape and value capture: compare suppliers, substitutes, customer bargaining power, supply response, pricing power, and chokepoint strength across HBM/high-end DRAM, NAND/eSSD, nearline HDD, controller/IP, capacity, equipment, materials, and packaging.
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
- Q2 Competitive landscape and value capture: compare suppliers, substitutes, customer bargaining power, supply response, pricing power, and chokepoint strength across lasers, InP/silicon photonics, DSP/driver/TIA, optical components, module integration, qualification, yield, and manufacturing capacity.
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

## Event / Conference Playbook

Use this playbook for conferences, keynotes, product launches, investor days, policy meetings, roadshows, major demos, and other public events where the investment question is whether the event changes future fundamentals or target ranking.

Default Q map:

- Q1 Fact boundary: identify what was officially confirmed, what is only roadmap/marketing language, and what new assumption changed versus pre-event public knowledge.
- Q2 Transmission and chokepoints: map event claims into product route, customer/order evidence, supply-chain bottlenecks, company exposure, margin, FCF, and value capture.
- Q3 Disconfirming tests and priced-in risk: test execution delay, missing customer conversion, substitution, weak ROI, valuation crowding, and already-priced expectations.
- Q4 Target observation list: rank specific securities by direct exposure, scarcity, mispricing, earnings elasticity, risk control, payoff odds, and monitorability.

Required L2 mechanism buckets:

- Official fact boundary: official agenda, keynote, transcript/replay, press releases, product availability, named partners/customers, production status, and exact dates.
- New-information delta: what changed versus prior roadmap, market expectation, or existing customer/supplier disclosures.
- Event-to-commercialization bridge: concept -> prototype -> qualification -> production -> shipment -> revenue -> gross margin -> FCF.
- Customer/order visibility: customer statements, capex, purchase agreements, backlog/RPO, supplier ramp, channel availability, and product launch windows.
- Supply-chain chokepoint: scarcity, qualification, capacity, access, distribution, data, trust, regulation, ecosystem lock-in, and substitute/counter-supply paths.
- Company exposure and profit bridge: segment revenue, product mix, customer concentration, order timing, ASP/take rate, margin, capex, working capital, and FCF.
- Valuation/priced-in risk: current market cap, multiple, consensus revisions, event price reaction, implied growth/margin duration, and downside if the event does not convert.
- Target ranking and kill tests: target universe, score subcomponents, action state, simplified odds model, upgrade data, downgrade data, and validation horizon.

Required extraction schemas:

- `event_fact_boundary`: event, date, speaker/source, claim, official/third-party status, product/customer/timing anchor, source link, and confidence.
- `conference_claim_quality`: claim, claim type, commercialization stage, exact wording cue, commercial anchor, evidence strength, verification needed.
- `event_transmission_chain`: event claim, product route, customer/order signal, revenue bridge, margin/FCF bridge, affected chain node, target implication.
- `chokepoint_scorecard`: node, demand flow, irreplaceability, supply/access constraint, pricing power, financial conversion, market pricing, disconfirming trigger.
- `company_exposure_bridge`: ticker, node exposure, revenue proxy, margin/FCF bridge, customer concentration, dilution, timing, evidence quality, missing data.
- `event_valuation_odds`: ticker, market cap/EV, relevant multiple, implied growth/margin, event delta, base/bull/bear path, upgrade/downgrade data.
- `target_ranking_worksheet`: ticker, core score dimensions, score subcomponents, action state, kill tests, review horizon, evidence/review IDs.

Skill dispatch defaults:

- Event fact and new-information delta -> `event-to-investment-analysis`.
- Keynote, transcript, slides, demos, and management Q&A -> `conference-transcript-analysis`.
- Supply-chain scarcity and Q2 scorecard -> `supply-chain-chokepoint-analysis`.
- Company exposure and profit bridge -> `company-exposure-analysis`, then `financial-statement-analysis` when filings/results are available.
- Valuation and priced-in expectations -> `valuation-analysis`.
- Final deterministic ranking -> `target-ranking-analysis`, with `target-recommendation-analysis` used for the public observation-list fields.
- News/live coverage -> `news-event-analysis`; it is usually a lead until confirmed by official or company evidence.

Scoring adjustments:

- `evidence_quality` must separate official facts, roadmap claims, customer logos, third-party news, and market interpretation.
- `future_space` can only strengthen when the event changes customer demand, shipment timing, adoption duration, or product availability.
- `chokepoint_strength` requires scarcity plus monetization; partner lists without capacity/qualification/pricing evidence are only leads.
- `valuation_odds` must reverse whether the event delta is already priced.
- `disconfirming_risk_control` must include event-specific kill tests such as launch delay, missing order conversion, customer capex pullback, substitution, and valuation crowding.
- `monitorability` must include a concrete review horizon and next evidence to collect.

## AI Factory Infrastructure Playbook

Use this playbook for AI datacenter hardware, GPU/ASIC computing, AI networking, interconnect, HBM/memory, advanced packaging, power/cooling, and AI factory capex cycle research.

Default Q map:

- Q1 Demand reality: convert AI workload, cloud revenue, and customer capex into sustainable demand, order visibility, and physical build-out by compute, memory, networking, and power/cooling nodes.
- Q2 Competitive landscape and value capture: compare suppliers, substitutes, customer bargaining power, supply response, pricing power, and chokepoint strength across GPU platform, custom ASIC, AI networking, HBM/data-center memory, advanced process/packaging, and power/cooling delivery.
- Q3 Disconfirming tests and priced-in risk: capex ROI, customer financing quality, substitution (custom ASIC, CPO, copper, internal builds), supply expansion, geopolitics, grid/power constraints, and valuation already priced in.
- Q4 Target observation list: compute platform, custom ASIC, networking, memory, foundry/packaging, power/cooling, and server/integration names reconciled with scarcity, mispricing, earnings elasticity, risk control, valuation odds, and kill tests.

Required L2 mechanism buckets:

- AI workload demand driver tree: training/inference/agent/RAG workload → GPU/ASIC/TPU demand → HBM/memory attach → network bandwidth → power/cooling per rack, with evidence that it is not merely inventory restocking.
- Supply response and capacity: TSMC CoWoS/advanced packaging, HBM wafer capacity, networking chip supply, power equipment lead time, transformer/grid interconnection, and datacenter construction timeline.
- Unit economics and profit bridge: per-node ASP, cost structure, gross margin, operating margin, capex intensity, FCF conversion, and working-capital pressure.
- Competitive value-capture map: which companies capture revenue/profit at GPU platform, custom ASIC design, AI Ethernet/InfiniBand/NVLink switching, optical interconnect, HBM supply, advanced packaging, power/cooling, and server integration nodes.
- Technology route comparison: GPU vs custom ASIC, pluggable optics vs CPO, air cooling vs liquid cooling, Ethernet vs InfiniBand, discrete GPU vs chiplet.
- Component/BOM value chain: subsystem, component/service, key companies, demand input, supply input, downstream recipient, financial validation metric, and QA link.
- Market-pricing bridge: current market cap/multiples/discount rate/implied growth versus required fundamental path for each node.
- Counter-supply and substitution: customer self-designed chips, China domestic supply, second-source qualification, architecture changes (CPO, CXL, UALink), and cloud capex digestion.
- Capital-chain and second-order beneficiaries: whether high AI factory returns pull capex into equipment, materials, test, infrastructure, channels, or downstream AI service adoption.
- Model口径 reconciliation: compare sell-side/industry/internal models by revenue scope, segment split, calendar/fiscal period, currency, margin definition, and capex classification.

### AI Factory BOM Node Catalog

The following BOM nodes are the default decomposition targets for the 行业空间 module:

| Node | Key Subsystems | Typical Public-Method Sources |
|------|---------------|------------------------------|
| GPU/AI Accelerator | NVIDIA Blackwell/Rubin, AMD MI400, Intel Gaudi | NVIDIA IR, SemiAnalysis, TechInsights |
| Custom ASIC/XPU | Broadcom, Marvell, Amazon Trainium, Google TPU | Broadcom IR, Amazon IR, SemiAnalysis |
| AI Networking | NVLink, InfiniBand, Ethernet switch, NIC/DPU | NVIDIA IR, Broadcom IR, Dell'Oro |
| Optical Interconnect | 800G/1.6T transceivers, LPO/CPO, silicon photonics | LightCounting, Coherent IR, Lumentum IR |
| HBM/Data-Center Memory | HBM3E/HBM4, DDR5, eSSD, CXL memory | Micron IR, SK hynix IR, TrendForce |
| Advanced Process/Packaging | 3nm/2nm, CoWoS, 3D packaging | TSMC IR, TechInsights, SemiAnalysis |
| Power/Cooling Delivery | UPS, switchgear, transformer, liquid cooling, busway | Vertiv IR, Eaton IR, IEA |
| Server/System Integration | AI server, rack-scale, liquid-cooled chassis | Dell IR, Supermicro IR, ServeTheHome |

### AI Factory Extraction Schemas

- `ai_factory_compute_demand`: platform/chip type, workload, cluster scale, unit volume, ASP, revenue, customer attach, period, source.
- `ai_factory_network_demand`: network type (NVLink/IB/Ethernet), port speed, port count, attach rate, switch/NIC revenue, period, source.
- `ai_factory_memory_demand`: memory type (HBM/DDR/eSSD), capacity per GPU/server, attach rate, ASP, revenue, margin, period, source.
- `ai_factory_power_cooling_demand`: product type (UPS/switchgear/transformer/liquid cooling), order/backlog, book-to-bill, margin, lead time, period, source.
- `ai_factory_manufacturing_capacity`: foundry, node, wafer capacity, packaging capacity, utilization, capex, ramp timing, source.
- `ai_factory_unit_economics`: company/product node, ASP, cost, gross margin, operating margin, capex, FCF, period, source.
- `ai_factory_valuation_rerating`: company, market cap/EV, multiples, FCF yield, implied growth/margin, peer set, source.
- `ai_factory_model_reconciliation`: model/source, metric, period, value, unit, scope, formula, difference vs alternative, adoption status.

Scoring adjustments:

- `future_space` must include demand-supply slope mismatch and node-specific attach rate logic, not only TAM.
- `chokepoint_strength` must include supply constraint, qualification difficulty, ecosystem lock-in, and substitution risk.
- `valuation_odds` must check whether node growth and peak margins are already priced into current multiples.
- `disconfirming_risk_control` must include counter-supply, architecture substitution, capex digestion, geopolitics, and grid/power constraint.
- `payoff_convexity` must separate volume growth, mix upgrade, margin expansion, and multiple rerating.
