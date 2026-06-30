# Value Invest Research

File-system-first equity research assistant. The canonical entry point is now one research-goal QA framework: user research goal -> execution plan -> adaptive QA drilldown up to five layers -> evidence-linked synthesis -> specific target observation list. Plain files are the source of truth; Python code validates contracts, scaffolds research objects, ingests public data, and creates LLM research drafts.

## Immutable First Core Investment Logic

This is the permanent first core of the research framework. Future framework iterations, report templates, playbooks, scoring rules, source workflows, and frontend rendering must preserve this core and may only add implementation detail around it:

> Find an industry, theme, company, or asset entering a large and durable S-curve; identify the truly scarce, hard-to-substitute, monopoly-like, or chokepoint BOM/supply-chain nodes inside that curve; then select only those securities whose future growth and profit path are not yet fully priced by the market, whose earnings elasticity is large, and whose downside risks are controlled and monitorable.

Operationally, every research run must optimize for proving or disproving this chain:

1. Is the S-curve real, large, feasible, and near an adoption inflection rather than only a narrative?
2. Which BOM, supply-chain, workflow, data, distribution, trust, capacity, regulatory, or ecosystem nodes are truly scarce or hard to bypass?
3. Which companies can convert that scarcity into revenue, margin, free cash flow, or valuation rerating?
4. Has the market already priced that growth path, or is there still mispricing?
5. Is the payoff large enough and the risk small enough for the target to pass the four core gates: `scarcity_or_monopoly`, `mispricing`, `earnings_elasticity`, and `risk_control`?

Broad theme exposure, large TAM claims, popular narratives, short-term price labels, convenient ticker availability, or surface-level growth are never sufficient. If the research cannot prove the S-curve, the scarce value-capture node, the underpricing, the earnings elasticity, and the risk-control condition with cutoff-visible evidence, the target must remain `watch_only` or `no_action`.

## Module Index

| Module | Path | Purpose |
|------|------|------|
| Core package | `src/value_invest_research/` | CLI, schemas, scaffolding, ingestion, research-system generation, run logs, and LLM research workflows. |
| Domain layer | `src/value_invest_research/domain/` | Pure research entities, policies, quality gates, scoring, and validation rules. No file, network, LLM, CLI, or rendering dependencies. |
| Application layer | `src/value_invest_research/application/` | Use cases and orchestration. Depends on domain and ports, never concrete adapters. |
| Ports | `src/value_invest_research/ports/` | Protocols for repositories, source parsing, LLMs, data, search, and rendering. |
| Adapters | `src/value_invest_research/adapters/` | Inbound CLI/API adapters and outbound file-system, LLM, DeepSeek, data, search, and renderer implementations. |
| Architecture docs | `docs/architecture/hexagonal_research_system.md` | Hexagonal architecture dependency rules, migration map, and quality gates. |
| Framework contracts | `src/value_invest_research/framework_contracts.py` | Executable validation and audit utilities for report hierarchy, time-sliced backtests, QA schema, scoring, frozen recommendations, labels, training samples, reviews, workbench traces, and domain playbooks. |
| Tests | `tests/` | unittest coverage for schemas, CLI, scaffolding, ingestion, and research workflow prompt/output behavior. |
| Research skill | `skills/value_invest_research/` | Operating protocol, frameworks, prompts, and evidence checklists. |
| Specialty skills | `skills/value_invest_research/specialty_skills/` | Project-tracked investment research leaf skills for question architecture, source planning, source parsing, valuation, and target observation. |
| Config | `config/` | Watchlist, source priority, research object registry, and event playbooks. |
| Source universes | `config/source_universes.json` | Domain-specific professional source priority lists and directed-search templates used before evidence parsing. |
| Stock objects | `stocks/` | Stock memos, evidence logs, structured data, run logs, and proposals. |
| Research objects | `research/` | Sector/theme/event memos, evidence, candidate screens, and run logs. |

## Architecture Contract

The research system is migrating to a hexagonal architecture. New or refactored code must follow the dependency rule in `docs/architecture/hexagonal_research_system.md`:

- `domain` contains pure business rules and must not import `application`, `ports`, or `adapters`.
- `application` coordinates use cases and may import `domain` and `ports`, but not concrete adapters.
- `ports` define protocols and must not import `application` or `adapters`.
- `adapters` implement system edges: CLI, file system, LLM, DeepSeek, market data, search, and HTML rendering.
- Existing root-level modules are legacy-compatible during migration. Prefer moving one tested vertical slice at a time instead of wholesale file moves.
- New research topics must enter through `ResearchGoal -> DomainPlaybook -> QuestionArchitecture`; do not start from a report template or hard-coded HTML outline.
- Public reports should be assembled through `ResearchProjectRepository -> ReportViewModel -> CanonicalReportRenderer`. Report renderers must not own domain question design or source parsing, and domain/playbook code must not know HTML classes.

## Canonical Research Goal Framework

When the user proposes any new research goal, topic, company, sector, event, or concept, use only this framework. Do not mix in any other research template.

The final report presentation contract is `skills/value_invest_research/frameworks/research_report_contract.md`. Treat it as the default for all future research reports unless the user explicitly asks to iterate on the framework.

The current report contract is locked:
- Compact public report lock is the highest-priority current default. Public HTML top-level order is exactly `当前研究的问题` -> `行业概况` -> `标的推荐` -> `来源索引`. Do not render public `下钻 QA` by default; keep drilldown QA, parser outputs, source plans, and workbench traces as internal artifacts unless the user explicitly asks to inspect them.
- In `行业概况`, render `01 技术链与BOM呈现` first, then from `02` onward render one large module per BOM node. Every BOM module must embed seven collapsible child question cards: `需求是否会大幅增长？`, `单位用量是否会提升？`, `供给能否跟上？`, `谁控制供给？`, `是否已经财务兑现？`, `市场是否已定价？`, and `反证是什么？`. Each BOM module is an independent research unit: keep the analysis focused on the current BOM's own demand, unit usage, supply, controllers, financial realization, pricing, and refutation. Other BOM nodes may appear only as upstream/downstream validation evidence, not as current-node investment conclusions; their opportunity analysis belongs in their own BOM module. Do not render public `S曲线与产业空间`, `关键变量与待验证数据`, or `下钻 QA` unless the user explicitly asks for those modules.
- For causal-chain questions inside those BOM child cards, especially `需求是否会大幅增长？`, public HTML must lead with professional report-style narrative rather than audit-workbench cards. Use `research-narrative`: headline conclusion, simple logic flow, then a `chain-node-expansion` section that expands each causal-chain node one by one. Every chain node must start with a metric board (`chain-metric-board`, `chain-metric-card`, `metric-trend-chart`, `metric-noncontinuous-chart`, `metric-trend-gap`) that states which metrics measure the node, why those metrics matter, the available historical/current/future readings, and data-quality caveats; only then show `历史对比`, `当前状态`, `未来推测`, `反证信号`, and `节点结论` with claim-near source links/source chips. Historical baseline / acceleration comparison is required when claiming "more", "rapid growth", or "S-curve"; future runway / remaining-space analysis must answer which metrics can still grow, by how much, and when they may arrive. Future runway must combine cutoff-visible public forecasts, company/customer guidance, financial execution evidence, and first-principles reasoning; do not linearly extrapolate historical growth without source support. If no cutoff-visible historical baseline or YoY/倍数 evidence exists, write "current snapshot is strong" rather than "accelerating"; if no future metric anchor exists, mark future runway as a gap. Keep source plans, parser traces, and per-source audit grids internal unless the user explicitly asks for the research workbench.
- Top-level order is exactly `当前研究的问题` -> `行业概况` -> `标的推荐` -> `来源索引`.
- Current effective priority is the BOM-first seven-question lock. In public HTML, `行业概况` starts with `01 技术链与BOM呈现`, then each BOM node becomes a standalone `details.industry-module.bom-research-module` numbered from `02`. The seven child cards inside each BOM node are the default public research scaffold for finding S-curve waves: demand growth, unit usage, supply constraint, supply controller, financial realization, market pricing, and refutation. `S曲线与产业空间`, `关键变量与待验证数据`, `竞争格局与利润池`, and `瓶颈点` are optional follow-up modules; render or research them only when the user explicitly asks for the next deepening round or when a domain playbook marks them as required for a specific decision. Older references below to mandatory industry modules are superseded by this simplification lock.
- `行业概况` is a mandatory pre-QA analytical layer. It must contain five public modules in this order: `产业链与生态位`, `行业空间`, `竞争格局与利润池`, `瓶颈点`, and `关键变量与待验证数据`. Each module must render as a clickable collapsed `details.industry-module > summary.module-head` card with `module-index`, `chevron`, and `industry-module-body`. `产业链与生态位` must retain the important chain information: a lane/swimlane view by upstream/midstream/downstream and a beginner-readable value-flow view showing how demand, orders, products, capacity, revenue, margin, and ROI move through the ecosystem. The value-flow view must start with plain-language steps and define unclear industry terms such as "系统交付" before showing detailed flow cards. `行业空间` must be a direct BOM-node space reasoning module, not a precision TAM model or a multi-step public methodology panel. Current scale anchors are evidence only; the module answers which BOM/subsystem nodes future demand may expand and why. It must render `industry-space-summary` plus `space-bom-reasoning`, with each key node as a collapsed `details.space-node-card` using a single-column `space-node-reasoning` body: first `space-node-space-reasoning` / 空间推理, then `space-node-evidence` / 证据 underneath. Do not render separate `space-node-risk` or `space-node-conclusion` cards inside industry-space nodes; refutation and target implications belong in Q3/Q4 or competition/chokepoint modules. Inside `space-node-space-reasoning`, every node must render a numbered sequence: `1 公开拆法` from cutoff-visible public sources, then `2 空间结论` that directly combines the five public information classes and judges whether 短期、中期、长期 space is large, with confidence and source chips through `space-node-sizing`, `space-method-step`, `space-step-title`, `space-step-index`, `space-public-methods`, `space-method-card-grid`, `space-method-card`, `space-method-card-body`, `space-method-entry`, `space-method-entry-sources`, `space-method-empty`, `space-horizon-conclusion`, `space-horizon-grid`, `space-horizon-card`, `space-node-sizing-table`, and `space-step-confidence`. The `公开拆法` area must render five fixed full-width method cards stacked vertically in this order: `公司指引`, `公司 TAM`, `客户侧指引`, `第三方拆法`, and `财务兑现证据`. Each method card should keep source type and count on the left, and show available entries on the right with `公司或机构`, `指引内容`, `BOM 节点`, `时间范围`, `可验证指标`, and `置信度`; each non-empty entry must carry its own `sourceIds`/`source_plan` and visible `space-method-entry-sources` source chips, not merely inherit a coarse BOM-node evidence pool. If a class is missing, show an explicit `待补` gap instead of hiding the category. The model may summarize public methods and judge 短期、中期、长期 space from the five evidence classes, but must not invent precision TAM or strengthen a conclusion from an unsourced self-built model. When reliable public methods are unavailable, mark the sizing as a data gap instead of filling it with model estimates. It must not answer competition, profit-pool ownership, valuation, or target ranking.
- Unified BOM taxonomy lock: `产业链与生态位` must define a visible `bom-taxonomy` / `bom-taxonomy-grid` / `bom-taxonomy-card` registry for the report. This registry is the public primary key for the industry overview. `行业空间`, `竞争格局与利润池`, `瓶颈点`, `关键变量与待验证数据`, QA artifacts, and `标的推荐` target mapping must reuse the same public BOM node names and expand one-to-one for every BOM node defined in `产业链与生态位`. Missing a taxonomy node in any later public module is contract-invalid. Source-level fields may preserve narrower wording from filings or reports, but public node labels must not drift across modules. Demand/customer capex can be shown as a supplementary demand-validation layer, but it is not a BOM node and cannot replace any BOM-node card.
- Industry-overview / QA complementarity lock: `行业概况` is the map layer and may show baseline facts, ecosystem coordinates, value/profit flow, candidate chokepoints, key variables, and the open questions it creates. `竞争格局与利润池` and `瓶颈点` must both organize by key BOM/subsystem node, not by one generic table. For each BOM node, competition/profit-pool analysis must answer four fixed minimum questions: `玩家市场份额分布`, `头部玩家优势分析`, `替代玩家赶超希望`, and `格局变化核心变量`. Competition question cards must not use the generic `当前判断` / `关键事实` / `推理链` row template; after the Universe/Exa source plan they must render natural-language `overview-answer-prose` paragraphs with blue inline source links for cited claims. Inline links must sit next to the specific numeric/factual claim they support, not only cluster at the paragraph end; bottom source chips are audit supplements, not a substitute for claim-level citation, and must only list source IDs actually cited or explicitly attached to the current answer. `玩家市场份额分布` must give concrete share/distribution numbers when a reliable public comparable source exists; when no exact comparable share table is available, state the data gap and use clearly labeled source-backed proxies rather than a vague judgment. The module then uses `profit-pool-table` to summarize which companies can keep revenue, gross margin, cash flow, or valuation elasticity at that node. This module exists to decide whether industry growth can be captured as company profit, so it must not only list competitors or repeat industry-space facts. For each BOM node, chokepoint analysis must answer: concrete constraint, controller, scarcity duration, release/substitution path, score/downgrade rule, and target/monitoring implication. `下钻 QA` is the decision-interrogation layer and must add marginal information beyond the overview: evidence verification, financial bridge, contradiction resolution, valuation/odds judgment, company comparison, kill test, or target-ranking impact. Do not re-render the same industry-space, competition/profit-pool, chokepoint, or supply-chain artifact inside Q1-Q4 L1 cards unless the QA artifact adds a new decision dimension not present in `行业概况`.
- Industry-overview research-unit protocol: every analytical module inside `行业概况` must follow the same execution shape, not only `行业空间`. First split the module into research units such as BOM/subsystem nodes, route families, customer groups, or key variables. Then split each research unit into a small fixed set of minimum questions. For every minimum question, GPT must actively create both `source_universe_plan` and `exa_search_plan`: the source-universe plan chooses professional sources from `config/source_universes.json` plus justified additions, while the Exa plan defines the direct query, expected fields, cutoff policy, and gap rule. Selected materials are parsed against that question's dimensions, normally by DeepSeek for long materials, then GPT verifies and writes the answer. Public HTML must not render Universe/Exa search plans; those stay in internal artifacts. Public question cards should show `overview-research-unit`, `overview-question-card`, `overview-answer`, natural conclusions, source chips, and claim-near inline source links where cited. If no reliable material is found, show an explicit gap; do not reuse a coarse evidence pool or model prior to fill the answer.
- `下钻 QA` preserves the full adapted Q1-Q4 QA tree and must render L3 questions plus any adaptive L4/L5 research units in complete refreshed reports unless the user explicitly asks for a shorter executive version.
- The QA tree supports adaptive drilldown with maximum depth five. L1 is the adapted research direction, L2 is the mechanism bucket, L3 is the investment decision question, and L4/L5 are optional deeper workbench/research units used only when needed to answer the L3 rigorously. Do not force every branch to reach L5.
- Q4 remains the auditable as-of target-selection QA node with child questions.
- `标的推荐` is a standalone presentation rollup, not a replacement for Q4.
- The hierarchy and format rules in `research_report_contract.md` are validation requirements, not style suggestions. A complete refreshed report is invalid if it drops L3, moves Q4 out of `下钻 QA`, duplicates child-question lists beside inline cards, replaces the canonical component family, or adds public process appendices.
- Four non-drift locks must always hold: hierarchy and format lock, industry-overview lock, backtest time-slice lock, and frontend card-style lock. In backtest mode, only cutoff-visible information can drive source collection, QA reasoning, scoring, odds, and target ranking; the only current-time data allowed in final HTML is the final-target evaluation label.
- Public no-changelog lock: final HTML must never include change-log, upgrade-log, "本轮/本次升级", "本轮/本次更新", "本轮如何落实", mechanism-depth checklist, framework explanation, execution trace, tool trace, or workbench/process commentary unless the user explicitly asks to inspect process. Framework upgrades must affect the questions, evidence, scoring, and target reasoning invisibly; they are not report content.
- Frontend interaction is part of the locked contract, not optional polish. Every existing `qa-card level-1` through `qa-card level-5` must render as a clickable `<details class="qa-card ...">` node with a `<summary>`, `qa-count`, and `chevron`, opened by default so users can collapse or expand the QA tree without losing the canonical hierarchy.
- In historical training/backtest mode, public prose must read as if written on the `as_of_date`; later price movement appears only once in the isolated final target evaluation fields.
- Do not add process appendices, execution traces, tool traces, iteration notes, or workbench sections unless explicitly requested.
- Additive-iteration lock: framework iteration is additive by default. When adding a new section, field, dimension, skill, source schema, or visual affordance, preserve all existing public section order, canonical component classes, QA expand/collapse behavior, action-state color classes, target-table structure, source-collapse behavior, and no-changelog rules unless the user explicitly asks for a frontend/report redesign.
- Before marking a framework iteration complete, run regression checks on a newly generated/refreshed report and at least one existing canonical report or fixture: `validate-report-contract`, `validate-research-artifacts` when artifacts exist, and a DOM/browser smoke check for QA card collapse plus `state-actionable_long`/`state-watch_only`/`state-no_action` color classes when those states appear.

Framework changes are persistent by default:
- When the user changes a report structure, interaction pattern, section order, or presentation logic, treat that as a new default research-system requirement unless the user explicitly says it is one-off.
- In the same change, update `AGENTS.md`, `skills/value_invest_research/SKILL.md`, and `skills/value_invest_research/frameworks/research_goal_qa.md` so future reports follow the new structure.
- If the change affects final report hierarchy or presentation, also update `skills/value_invest_research/frameworks/research_report_contract.md`.
- Existing generated reports may keep their historical content, but new or refreshed reports must use the latest framework requirement.
- Final user-facing HTML reports must stay clean and research-first. They must use this top-level order: `当前研究的问题`, `行业概况`, `下钻 QA`, `标的推荐`, `来源索引`.
- Effective default public report content is simplified around BOM-first understanding plus seven investment questions per node. In `行业概况`, render `01 技术链与BOM呈现`, then one numbered BOM research module per node from `02` onward. `S曲线与产业空间`, `关键变量与待验证数据`, `竞争格局与利润池`, and `瓶颈点` are optional follow-up deepening modules, not required for the first public report. Do not force every BOM node through separate space, competition/share/profit-pool/chokepoint cards in the first pass.
- `行业概况` should use `industry-overview-section` and five clickable `details.industry-module` cards. Each module uses `summary.module-head`, `module-index`, `chevron`, and `industry-module-body`, default collapsed so long industry maps do not overwhelm the report. Its chain module should use `supply-chain-section`, `chain-explain`, `chain-research-bridge`, `chain-node-lens`, `chain-plain-summary`, and three nested clickable `details.chain-detail-panel` cards for `chain-lane-map`, `chain-value-flow`/`chain-simple-flow`, `component-value-chain`, and `bom-taxonomy`. Do not render a separate high-level chain overview table by default when these components already explain the ecosystem. The `行业空间` module should use `industry-space-summary` and `space-bom-reasoning`. Each key BOM/subsystem node should be a collapsed `details.space-node-card` with a single-column `space-node-reasoning` body that renders `space-node-space-reasoning` first and `space-node-evidence` below it; `space-node-space-reasoning` must include `space-node-sizing`, `space-method-step`, `space-step-title`, `space-step-index`, `space-public-methods`, `space-method-card-grid`, `space-method-card`, `space-method-card-body`, `space-method-entry`, `space-method-entry-sources`, `space-method-empty`, `space-horizon-conclusion`, `space-horizon-grid`, `space-horizon-card`, `space-node-sizing-table`, and `space-step-confidence` for the ordered sequence `1 公开拆法`, `2 空间结论`. `竞争格局与利润池` must use `competition-bom-map`, collapsed `competition-bom-card`, single-column full-width `competition-question-grid`, `overview-research-unit`, `overview-question-card`, `overview-answer`, `overview-answer-prose`, and `profit-pool-table` so every key BOM node answers the four fixed competition questions (`玩家市场份额分布`, `头部玩家优势分析`, `替代玩家赶超希望`, `格局变化核心变量`) with natural-language answer paragraphs and claim-near blue inline source links, then summarizes profit-pool ownership in the table. Do not render a separate technology-route matrix table in the public competition/profit-pool module; route comparison should be absorbed into each BOM card's four-question analysis or kept in internal workbench artifacts. `瓶颈点` must use `chokepoint-bom-map`, collapsed `chokepoint-bom-card`, single-column full-width `chokepoint-question-grid`, `overview-research-unit`, `overview-question-card`, `overview-answer`, `chokepoint-scorecard`, `chain-chokepoints`, and `bottleneck-release-timeline` so every key BOM node answers the fixed bottleneck questions without exposing execution-level search plans. Inside every BOM card, child method/question cards must render as a single-column full-width stack, not side-by-side: `space-method-card-grid`, `competition-question-grid`, and `chokepoint-question-grid` must use `grid-template-columns: 1fr`. `关键变量与待验证数据` must use `key-variable-bom-map` and collapsed `key-variable-bom-card` nodes so every BOM node has its own variables, downgrade triggers, source plan, and target/QA mapping. The overview must also include `industry-competition`, `industry-chokepoints`, and `industry-key-variables` with `chain-data-gaps`. It is the fact-map input for Q1-Q4. Dense tables must use `table-scroll` so users can horizontally inspect content without cards overflowing.
- `行业概况` and `下钻 QA` must be complementary. The overview can answer who/what/where/dependency/value-flow/candidate-bottleneck questions. QA should ask whether/why/how much/under what condition/who wins/what refutes/what changes the target ranking. QA L1 cards should use synthesis prose and focus prompts, while detailed tables should live in L2/L3 only when they answer a specific unresolved decision question.
- Industry/theme and technology-route reports must also carry professional research artifacts inside the existing contract: `constraint-definition` in `当前研究的问题`; `component-value-chain` inside `产业链与生态位`; `competition-bom-map` and `profit-pool-table` inside `竞争格局与利润池`; `chokepoint-bom-map`, `chokepoint-scorecard`, and `bottleneck-release-timeline` inside `瓶颈点`; and `target-profit-bridge` plus `target-valuation-table` inside `标的推荐`. These are research content components, not process notes.
- `标的推荐` is a synthesis section, not a process appendix. It should roll up all QA evidence into a ranked observation list with specific targets, win probability, payoff odds, rationale, and downgrade triggers.
- Do not put iteration notes, "what changed in this run", quality-framework explanations, execution traces, tool attribution, DeepSeek usage notes, or workbench appendices into the final HTML. Store process metadata in workbench JSON, logs, or internal artifacts instead.
- Do not describe framework changes inside the report. Phrases such as "本轮升级", "本次更新", "本轮新增", "机制深度映射", "本轮如何落实", or English equivalents such as "what changed in this run" are contract drift in final HTML. Put those notes only in internal artifacts or user-facing chat replies.
- Do not simplify away QA depth when refreshing a report. Preserve the full available QA tree unless the user explicitly asks for a shorter executive version.
- Do not overload L3 with unrelated questions under a single L2. L2 should group L3 leaves into meaningful mechanism buckets selected by the research-type adapter and domain playbook.
- Do not overload L3 with multi-company, multi-node, or model-heavy work. If an L3 question cannot be answered with one clear fact/inference/judgment artifact, adaptively split it into L4 or L5 units until each unit has one decision use, one source plan, one extraction schema, and one verifiable answer. Stop before L5 if the parent question is already answerable.
- The public report contract defines hierarchy and presentation only. Domain-specific questions, metrics, parsing schemas, tracking indicators, and threshold rules belong in research-type adapters or domain playbooks, not in the shared presentation contract.
- For industry/theme opportunity and technology/product-route research, chokepoint evaluation belongs inside the competitive-landscape/value-capture analysis, not as a standalone top-level module. Q2 must first ask who competes in each node, what substitutes exist, how customers bargain, whether supply can expand, and who has pricing power; only then should it decide which nodes are real chokepoints. The scorecard belongs inside the relevant Q2 competition/value-capture node, and the final target ranking must use this chokepoint score alongside future space, valuation odds, evidence quality, and disconfirming-risk control.
- Chokepoint evaluation must be formula-based, not only narrative. Store a reusable score schema with dimension weights, scoring definitions, and downgrade rules. Final reports should show the score breakdown or score drivers so rankings are comparable across targets and future reports.
- Scarcity-first opportunity gate: the default action state is `no_action`, not long recommendation. The goal is to find a currently underpriced large opportunity. A target becomes `actionable_long` only when the as-of evidence supports all four core target dimensions: `scarcity_or_monopoly` (scarce/monopolistic product, service, or chokepoint), `mispricing` (growth not fully priced), `earnings_elasticity` (large future revenue/margin/FCF or rerating upside), and `risk_control` (small enough, monitorable downside). If any core dimension fails, cap the score and mark the target `watch_only` or `no_action`.
- Do not let broad theme exposure create high scores. Future-space data is useful only after it reaches a scarce, monetizable chokepoint. The highest research effort should go into proving or disproving irreplaceability, substitution barriers, pricing power, and whether the market has already priced the opportunity.
- Mechanism-depth protocol: for industry/theme opportunity and technology/product-route research, the domain playbook must force a driver-tree model before evidence collection. The minimum depth map covers demand driver tree, supply or access response, unit economics and profit bridge, competitive value-capture map, market-pricing bridge, disconfirming/counter-supply tests, capital-chain or second-order beneficiaries, and model/口径 reconciliation. A refreshed canonical report is too shallow if it only states TAM/theme exposure without modeling how demand becomes company revenue, margin, FCF, and valuation rerating.
- Domain-specific depth requirements live in `skills/value_invest_research/frameworks/domain_playbooks.md`. Use it when selecting or synthesizing a playbook; for storage/memory research, use the memory industry playbook so L2/L3 questions cover workload-to-memory demand, demand-supply slope mismatch, product price/unit economics, company value capture, capex cycle, market-pricing rerating, counter-supply/substitution, and model口径 reconciliation.

## Time-Sliced Prediction Evaluation

The research system must support two explicit run modes. The default mode is historical training/backtest; use live prediction only when the user explicitly asks for current/live/real-time research or otherwise states that the run should not be time-sliced.

- Historical training/backtest mode: use an `as_of_date`, defaulting to three calendar months before the evaluation date/report date unless the user specifies another cutoff. Source collection, source parsing, QA answers, valuation context, and target ranking may only use information that was publicly visible on or before `as_of_date`. Later materials are look-ahead data and must not enter the thesis, score, odds model, or target rank.
- Live prediction mode: use only when explicitly requested. Use information visible up to the report date. Do not attach a future return label. Instead, set a validation horizon, required evidence, and next review trigger, normally report date plus three months unless the user specifies another horizon.

Historical training/backtest reports must attach an ex-post label to each final target recommendation:

- `as_of_date`
- `evaluation_date`
- `label_window`
- adjusted or total-return price at `as_of_date`
- adjusted or total-return price at `evaluation_date`
- `forward_3m_return`
- benchmark or sector return when available
- excess return when available
- price source and label status

The forward return label is evaluation metadata only. It must never be used to justify the historical recommendation, strengthen the thesis, select sources, tune the Q2/Q4 score, or rewrite the as-of judgment. Public backtest reports must read as if written by the system on the `as_of_date`: QA conclusions, target rationale, score explanations, odds models, downgrade triggers, and summary text must not mention ex-post winners, losers, realized returns, calibration lessons, or later price action. Show later price movement only in one isolated label block or the rightmost label columns of the final target table. If price data is missing, stale, corporate-action-unadjusted, or affected by delisting/suspension, mark the label as unverified instead of imputing success.

Label availability must not define the investment universe. In historical training/backtest mode, target selection and ranking must start from the economically relevant securities or assets across exchanges. If a non-US or otherwise hard-to-label target lacks a verified price label, keep the target in the frozen observation list with `label_status: label_unverified_*` rather than replacing it with a US/Nasdaq proxy.

Historical backtest anti-leakage controls are mandatory. The system cannot guarantee that a current LLM has no post-cutoff background priors, so backtest conclusions must be source-pack grounded: model priors may frame hypotheses only and must never strengthen facts, scores, target ranking, or action state. Every historical QA tree must declare `anti_leakage_controls`; every L3-L5 research unit must declare `backtest_grounding` with its exact cutoff source IDs and an empty `non_source_claims` list. Target score subcomponents must reference cutoff-visible source IDs or GPT-verified leaf review IDs. Framework/playbook, supply-chain, and model knowledge that cannot be traced to cutoff sources must remain a pending hypothesis, not a scored conclusion.

## Research Quality Pipeline

The framework optimizes research quality before report polish. Run these passes in order:

1. Question architecture
   - Use `investment-question-architect` to classify the research type and design the Q1-Q4 tree.
   - Before building Q1-Q4, build the supply-chain map using `supply-chain-panorama-explainer`. The map must start from the research goal and the core supply-chain investment question, then organize upstream, midstream, and downstream. It must cover products/services, key listed and private players, dependency links, company relationship edges, value/profit flow, candidate chokepoints, node-screening lens, value-capture matrix, supply-chain-to-QA mapping, and key data gaps. It must be written in beginner-readable Chinese and answer: who provides what, who depends on whom, who pays whom, which company connects to which company, each company/node's demand input, supply input, own product/service, downstream recipient, financial validation metrics, bottleneck strength, target/QA mapping, and what evidence remains missing. Public display should rely on nested collapsible chain components: lane/swimlane, value-flow, and component/BOM value chain. Do not add a separate high-level chain overview table by default. Do not begin target ranking or QA evidence collection from company names before this map exists.
   - Question quality is the primary depth control. Each L3-L5 research unit must state decision use, required materials, support evidence, refuting evidence, target implications, and preferred specialty skill.
   - For event, conference, keynote, product-launch, and policy-meeting research, use the event/conference adapter. The QA tree must first establish the official fact boundary and new-information delta, then bridge event claims into product route, customer/order evidence, company financial exposure, valuation odds, disconfirming tests, and target ranking. Do not let a news/event summary replace this bridge.
   - For industry/theme and technology-route research, first build a mechanism-depth map. L2 buckets must represent real analytical mechanisms such as demand drivers, supply response, unit economics, value capture, pricing/valuation, counter-supply, and second-order beneficiaries, not generic summary headings.
   - Each L3-L5 research unit is a decision unit, not a prose subsection. Its structured record must include `decision_use`, `materiality`, `support_evidence`, `refute_evidence`, `target_implications`, `score_component`, `minimum_evidence_gate`, and `refuting_source_plan`.
   - `score_component` must explicitly connect each L3-L5 research unit to one or more ranking drivers such as `future_space`, `chokepoint_strength`, `valuation_odds`, `evidence_quality`, `disconfirming_risk_control`, `monitorability`, `payoff_convexity`, `target_ranking`, or `action_state`.
   - Do not start evidence collection from a generic outline. Start from investment-relevant questions that can change parent conclusions or target strength.

2. Source planning
   - Use `research-source-planner` before reading materials.
   - GPT is the end-to-end research analyst and owns source-universe selection. The user only needs to provide the research goal, constraints, and optional preferences; GPT must classify the domain, select and combine the relevant professional source universes from the registry, explain the selection in internal artifacts, and add candidate sources when the registry is insufficient. Do not ask the user, who may be a non-specialist, to choose SemiAnalysis/TrendForce/company IR/news/opinion universes unless they explicitly want to override the research process.
   - For every L3-L5 research unit, define the concrete source plan: primary evidence, company voice, research reports/data, messages/news, and opinions.
   - For every smallest active question inside `行业概况`, including `行业空间`, `竞争格局与利润池`, `瓶颈点`, and `关键变量与待验证数据`, source planning must create a question-level `source_universe_plan` and `exa_search_plan` before any answer is written. The `source_universe_plan` records professional priority sources, directed site/domain queries, expected fields, parser skill, visible-date/cutoff status, and selected/gap source IDs. The `exa_search_plan` records the exact Exa query, expected fields, cutoff policy, retrieval status, and quarantine rule for post-cutoff hits. This is an active search plan per minimum question, not a generic evidence pool for the whole module.
   - For every `行业空间` BOM/subsystem node, source planning must first create an active five-bucket source-search matrix after BOM node identification, covering `公司指引`, `公司 TAM`, `客户侧指引`, `第三方拆法`, and `财务兑现证据`. This is not a loose match from a coarse evidence pool: each bucket must record search query/terms, expected fields, source bucket, visible date/cutoff status, allowed usage, preferred parser skill, selected source IDs when found, or `status=gap` plus `gap_reason` when no reliable material exists. It must use the domain source universe in `config/source_universes.json` to generate `priority_sources` and site/domain `directed_queries`; broad keyword search without sources such as SemiAnalysis, TrendForce, Omdia, TechInsights, Dell'Oro, LightCounting, company IR, or customer IR is insufficient for AI factory / semiconductor hardware topics. Planning is per public-method subcard and per entry, not only per coarse BOM node: each rendered entry must have its own concrete source IDs. The extraction target is not only the headline number; it must capture scope, period, formula or decomposition, assumptions, output value, source date, and口径 caveat. GPT may align methods and run simple sanity checks, but must not create a proprietary TAM estimate when no public method exists; mark the node as a data gap instead.
   - Source parsing is question-dimensional, not source-dimensional. For each smallest active research question or BOM-node question, GPT must define the information universe and then define the dimensions that matter under that question. The parser must read each selected material against every relevant dimension, and a single material may populate multiple buckets such as `公司指引`, `公司 TAM`, and `财务兑现证据`. Do not stop after the first matching bucket. If a source contains an outlook, segment data, TAM, pricing, margin, or capex clue, extract all of them with scope caveats. Missing dimensions should be marked as explicit gaps, not silently omitted.
   - For model-heavy industries, source plans must specify the tables or fields needed to rebuild the mechanism model: period, unit, currency, volume, price, mix, capacity, utilization, cost, margin, capex, FCF, valuation multiple, implied expectation, and口径. Generic article summaries are not sufficient when the decision depends on a quantitative driver tree.
   - `source_plan` must be structured by concrete source, expected fields, source bucket, visible date/cutoff status, allowed usage, and preferred parser skill. A bare sentence is not sufficient for refreshed canonical reports.
   - Every support source plan needs a refuting or boundary-check source plan.
   - In historical training/backtest mode, every source plan must include `as_of_date`, `source_visible_at`, cutoff status, and auditable `availability_proof` such as publisher date, filing timestamp, archive timestamp, exchange release page, or dataset snapshot note. Reject or quarantine materials whose visible date is after `as_of_date`, except for the separate price-label dataset used only after recommendations are frozen.

3. Specialty parsing
   - Route concrete materials through the relevant leaf skill:
     - `financial-statement-analysis` for filings, results, segment data, capex, inventory, backlog/RPO, and cash quality.
     - `valuation-analysis` for future space, priced-in expectations, multiples, reverse DCF, FCF yield, peer comparison, and odds.
     - `industry-report-analysis` for sell-side reports, industry reports, TAM, supply-demand, price forecasts, and third-party datasets.
     - `event-to-investment-analysis` for conferences, launches, keynotes, investor days, policy meetings, and public events; it converts event facts into transmission chains, evidence gaps, and target implications.
     - `conference-transcript-analysis` for keynotes, transcripts, slides, demos, and management Q&A; it separates official facts, roadmap claims, customer references, commercialization stage, and marketing language.
     - `supply-chain-chokepoint-analysis` for Q2 competition-derived chokepoint scoring when value capture depends on scarce supply, qualification, access, distribution, trust, data, regulation, or ecosystem lock-in.
     - `company-exposure-analysis` for mapping a theme, event, product route, or chokepoint into a specific company's revenue, margin, orders, customers, capex, FCF, and segment exposure.
     - `news-event-analysis` for news, public messages, policy updates, supply-chain reports, and unverified leads.
     - `opinion-analysis` for expert, investor, interview, conference-note, or social-media viewpoints.
     - `leaf-research-deepseek` when DeepSeek MCP reads selected concrete materials and drafts the first L3-L5 extraction.
   - For each selected concrete material, create or append one source-parser record in `source_extractions.jsonl`. This reading layer should normally be produced by DeepSeek MCP for long reports, filings, transcripts, research reports, and multi-paragraph source excerpts.
   - Each source-parser record must fill `schema_fields` according to the L3-L5 `skill_dispatch.extraction_schema`. A parser output that only gives generic summary text cannot strengthen a refreshed canonical answer until GPT verifies and maps it into the required schema fields.
   - Third-party reports and spreadsheets must be parsed as assumption models, not accepted as conclusions. Extract formulas, driver rows, period/unit/currency, methodology, disagreement points, and口径 caveats before using any headline TAM, CAGR, margin, target price, or upside number.
   - Then create or append a matching GPT verification record in `leaf_source_reviews.jsonl`, recording adopted facts, corrected fields, rejected claims, uncertainty, and whether the extraction is allowed to strengthen the final QA answer.
   - L3-L5 `skill_dispatch` must carry the created `source_extraction_ids` and `leaf_source_review_ids` so the final answer can be traced from question to parser output to GPT verification.
   - Do not skip these extraction/review files merely because GPT can read the material directly. GPT may parse directly only for very short materials, failed DeepSeek calls, missing tool access, or high-risk verification; the fallback and reason must be recorded.

4. GPT verification and synthesis
   - GPT verifies parsed facts, resolves source conflicts, separates fact/inference/judgment, and writes final L3-L5 answers.
   - Parent conclusions may only roll up from verified child answers.

5. Target recommendation analysis
   - Use `target-recommendation-analysis` for Q4 when the research has investment implications.
   - Use `target-ranking-analysis` after Q1-Q3 are verified when the task is deterministic target ranking. It reconciles Q2 chokepoint drivers, company exposure, valuation odds, disconfirming-risk control, payoff convexity, and monitorability into the final ranked worksheet.
   - Targets must be specific securities or assets, with chokepoint exposure, future space, valuation odds, strength, catalysts, downgrade triggers, required data, and source links.
   - Observation strength must reflect chokepoint evaluation. Do not rank a target above stronger alternatives solely because its narrative is attractive; it must score on bottleneck criticality, scarcity or substitution barrier, pricing power, financial exposure, evidence quality, valuation odds, and monitorability.
   - Each of the seven component scores must preserve auditable `score_subcomponents` with subdimension name, score, weight, evidence IDs or GPT review IDs, rationale, and status. Direct unexplained component scores are fallback-only and should not be used for refreshed canonical reports.
   - Roll the seven component scores into four core target dimensions: `scarcity_or_monopoly`, `mispricing`, `earnings_elasticity`, and `risk_control`. These four dimensions are the primary public score display and action-state gate.
   - Apply the scarcity-first opportunity gate before ranking. `no_action` is the default. `actionable_long` requires scarce/monopolistic value capture, market mispricing, large earnings elasticity, and controlled risk. Missing valuation, weak scarcity, only generic theme exposure, non-positive expected excess return, weak evidence, low payoff elasticity, or uncontrolled disconfirming risk must cap strength even if the industry narrative is attractive.
   - Final target ranking must be deterministic from the frozen score object: action-state priority, opportunity fit, total score, payoff convexity, thesis confidence, then stable ticker/name tie-break. Do not manually move targets after labels are attached or because later outcomes are known.
   - Any `actionable_long` target must carry hard `thesis_kill_tests` with test, evidence needed, downgrade action, and source plan. If a target lacks such tests, cap it at `watch_only`.
   - Final target tables must include a compact score breakdown and a simple odds model. The odds model should state the implied expectation, base/bull/bear verification path, and the data that would upgrade or downgrade the observation. It must render inside `标的推荐` as `target-odds-model` with `target-odds-table`, before the dense `target-table`, and Q4 should summarize the same odds gate inside its current-conclusion block. If valuation data is stale or incomplete, mark odds as unverified rather than strengthening the target.
   - Keep a prediction review field for every target or major thesis node: initial claim, validation horizon, required evidence, current status, and review trigger. This can live in the workbench and be summarized in the relevant Q3/Q4 node.
   - In historical training/backtest mode, freeze the Q4 target list and ranking before attaching the forward three-month return label. The label may be shown for evaluation, calibration, and later model improvement, but it must not alter the frozen recommendation.
   - This is a research observation list, not a buy/sell/hold instruction.

6. Executable contract validation and learning artifacts
   - Use `framework_contracts.py` to validate final report hierarchy/card structure, validate QA tree schema, validate source-extraction schema fields, audit time-sliced sources and `availability_proof`, score targets with separated thesis confidence/payoff convexity plus auditable subcomponents, rank targets deterministically, validate target kill tests, freeze recommendations before labels, attach forward-return labels, build training samples, build prediction reviews, and keep internal workbench traces out of final HTML.
   - Use `skills/value_invest_research/frameworks/research_quality_gate.md` as the operational quality gate. A complete refreshed report must preserve `qa_tree.json`, `source_extractions.jsonl`, `leaf_source_reviews.jsonl`, and `investment_workbench.json`; missing parser or GPT review layers are hard failures, not presentation gaps.
   - Treat `tests/fixtures/research_quality_gold/` as the gold regression fixture for the current contract. Framework changes must keep this fixture passing or intentionally update the fixture and tests in the same change.
   - Run `value-invest-research validate-report-contract <professional_report.html> --mode historical_backtest --require-l3` after refreshed canonical reports.
   - Run `value-invest-research validate-research-artifacts <project_dir> --require-l3` after refreshed canonical reports. This validates the QA tree, source-parser records, GPT review records, target score subcomponents, score dimensions, and kill tests.
   - Run `value-invest-research audit-time-slice <sources.jsonl> --as-of-date YYYY-MM-DD` before using historical-mode sources for QA, scoring, odds, or ranking.
   - In historical mode, `validate-research-artifacts` must also pass the anti-leakage gate: `anti_leakage_controls`, L3-L5 `backtest_grounding`, cutoff-only source parsing, and target score references to cutoff sources or GPT-verified reviews.

## Four-Stage Serial Research Pipeline

Every research run executes as a four-stage serial pipeline. The LLM must not skip stages or run them out of order.

```
Stage 1: 定义研究问题
    │  Gate: validate-project-schema
    │  Output: project.json (research_type, domain_playbook, as_of_date, object_id)
    ▼
Stage 2: 行业概况 (五个模块)
    │  Gate: validate-industry-overview
    │  Output: supply_chain data + industry_space_evidence_pack +
    │          competition data + chokepoint data + pending_questions
    ▼
Stage 3: 针对性 QA 树
    │  Gate: validate-research-artifacts --require-l3
    │  Output: qa_tree.json + source_extractions.jsonl + leaf_source_reviews.jsonl
    ▼
Stage 4: 标的推荐
       Gate: validate-report-contract --require-l3
       Output: frozen_recommendations.json → labeled_recommendations.json (if backtest)
```

### Stage 1: Define Research Problem

LLM must write `project.json` with these minimum fields:
- `project_id`
- `title`
- `research_type`: one of `industry/theme opportunity`, `single company`, `event/policy`, `technology/product route`, `target update`, or custom
- `domain_playbook`: selected from `domain_playbooks.md` or synthesized
- `run_mode`: `historical_backtest` (default) or `live_prediction`
- `as_of_date` (if backtest), `report_date` (if live)
- `decision_boundary`
- `current_judgment`: short directional judgment
- `biggest_uncertainty`

Run `validate-project-schema <project_dir>` before proceeding to Stage 2.

### Stage 2: Industry Overview (S-Curve First)

Stage 2 first populates three default `行业概况` modules: `S曲线与产业空间`, `技术链与BOM呈现`, and `关键变量与待验证数据`. Each minimum research unit in the S-curve space module executes a self-contained "think → search → parse" loop. `技术链与BOM呈现` is a readable map, not a detailed competition workbook. Do not run full `竞争格局与利润池` or `瓶颈点` unless the user asks for that next iteration or a playbook explicitly requires it.

#### The "think → search → parse" loop (reused in Stage 3)

Every minimum research unit follows this sequence:

1. **Think**: LLM writes a `source_plan` before any search. The plan states:
   - `decision_use`: why this unit matters
   - `expected_fields`: concrete fields to extract
   - `priority_sources`: drawn from `config/source_universes.json` for the domain
   - `directed_queries`: site/domain-specific search queries (not just broad keywords)
   - `preferred_parser_skill`: which specialty skill should parse results

2. **Search**: LLM executes web searches using `web_search_prime` + `webfetch` (primary) or `web-reader`. Collected materials are written to `sources.jsonl` with `source_visible_at` and `cutoff_status`.

3. **Parse**: DeepSeek MCP reads materials → `source_extractions.jsonl` (fills `schema_fields`). GPT verifies → `leaf_source_reviews.jsonl`. Verified facts feed into the unit answer.

If 3 rounds of directed search produce no usable results → write `status=gap` + `gap_reason`. Do not invent TAM numbers.

#### Module 1: S曲线与产业空间 — Space Execution

The primary unit is the S-curve space question. BOM nodes may be used as evidence containers, but the conclusion should answer whether the whole industry is entering a large, feasible, early-acceleration curve. For each active node or space unit, the LLM runs the "think → search → parse" loop across all five public-method buckets:

| Bucket | Sources | Expected fields |
|--------|---------|----------------|
| 公司指引 | Company IR, earnings calls | Revenue guidance, capex, order outlook, capacity plans |
| 公司 TAM | Investor day, 10-K market sections | Market size, CAGR, serviceable market |
| 客户侧指引 | Downstream capex, RPO announcements | Customer spend, backlog, prepayment |
| 第三方拆法 | SemiAnalysis, TrendForce, Omdia, Dell'Oro, LightCounting | TAM, shipment, ASP, supply-demand balance |
| 财务兑现证据 | Segment revenue, backlog, margin | Actual revenue, backlog, margin, FCF |

Every entry must carry independent `source_ids` and render `space-method-entry-sources` source chips. Missing buckets → `待补`.

#### Module 3 → Stage 3 Bridge

Module 3 (`关键变量与待验证数据`) does NOT run new searches by default. It aggregates S-curve, space, and chain/BOM gaps into `pending_questions`. Each entry carries:
- `gap_source`: which module/sub-unit
- `variable`: what is unknown
- `materiality`: why it matters
- `candidate_qa_direction`: which Q direction (Q1-Q4)
- `candidate_score_component`: which ranking driver

This list is the direct input for Stage 3 QA tree generation.

### Stage 3: QA Tree Generation

The LLM reads `pending_questions` from Stage 2 and generates a QA tree. Do not invent questions — derive them from documented gaps.

L2 buckets come from the domain playbook's mechanism buckets. L3 questions are grouped under those buckets.

L3 → L4/L5 decomposition triggers:
- L3 fact/inference/judgment still ambiguous
- source_plan spans >3 material classes
- support and refuting evidence address different sub-mechanisms
- L3 covers multiple companies/nodes

Each L3 leaf runs the same "think → search → parse" loop as Stage 2 modules. Each L3-L5 answer must directly answer the unit question, not merely list adjacent facts. If the question asks for a mapping, bridge, ranking, comparison, formula, scenario, or risk test, the current-conclusion block must include the corresponding structured answer artifact inside the QA card.

Run `validate-research-artifacts --require-l3 <project_dir>` before Stage 4.

### Stage 4: Target Recommendation

Stage 4 does NO new searches. It synthesizes:
1. Aggregate all L3 `score_component` fields into per-target scores
2. Compute four core dimensions from seven audit components
3. Apply scarcity-first gate
4. Deterministic ranking
5. Output frozen_recommendations.json

Run `validate-report-contract --require-l3 <report.html>` to complete.

## LLM Analyst Behavior Contract

The LLM must follow these rules during every research run:

### 1. One unit at a time
Do not plan all BOM nodes' source_plans simultaneously. Complete one node → next node.

### 2. Think before searching
Before every search, output:
- Why: decision_use
- What: expected_fields
- Where: priority_sources + directed_queries
- How: preferred_parser_skill

This is written into the unit's `source_plan` as an auditable record.

### 3. Gap is an answer
After 3 rounds of directed search with no usable results: write `status=gap` + `gap_reason`. Gaps flow to Stage 2 Module 5 → Stage 3 QA tree.

### 4. Concrete citations
Every fact carries a `source_id`. No "the industry generally believes" prose.

### 5. Self-challenge
After each supporting source, actively search for one refuting source. If not found: "refuting search planned but no public refutation found."

### 6. No skipping
Modules may be skipped only if the domain playbook explicitly exempts the research type. L3 questions may be deleted only with domain playbook justification.

### 7. Stage gate reporting
At each stage start, output:
```
## 执行计划
**当前阶段**: Stage N / [name]
**已完成**: Stage N-1 ✓ (gate passed)
**下一步**: [specific sub-unit]
**待通过门控**: [gate command]
```

After each minimum unit, report findings, gaps, and next unit.

### 8. Refresh behavior
- Stage 2 Module 1 (chain): skip if industry structure unchanged
- Stage 2 Module 2 (space): refresh only time-sensitive data
- Stage 3: add L3 only for new gaps; do not rewrite answered L3
- Stage 4: always re-synthesize

## Stage Gate Commands

```
value-invest-research validate-project-schema <project_dir>
value-invest-research validate-industry-overview <project_dir>
value-invest-research validate-research-artifacts <project_dir> --require-l3
value-invest-research validate-report-contract <report.html> --mode historical_backtest --require-l3
```

### 1. Current research goal
   - Define the object, time frame, investment relevance, and decision boundary.
   - Output one constrained current judgment and the biggest uncertainty.

## Commands

```powershell
python tools/run_tests.py
$env:PYTHONPATH = "src"; python -m value_invest_research --help
value-invest-research --help
value-invest-research build-evidence AAPL
value-invest-research build-research-system AAPL
value-invest-research build-research-graph AAPL
value-invest-research research-stock AAPL --api-key $env:LLM_API_KEY
value-invest-research validate-report-contract research/qa_projects/<project>/professional_report.html --mode historical_backtest --require-l3
value-invest-research audit-time-slice research/qa_projects/<project>/sources.jsonl --as-of-date 2026-02-28
value-invest-research validate-research-artifacts research/qa_projects/<project> --require-l3
```

## Key Constraints

- Do not issue final trading instructions.
- Keep material claims tied to evidence IDs.
- Separate facts, inferences, and judgments.
- Classify every research input into one of four information buckets: evidence, research_report, opinion, or message.
- Keep low-reliability evidence as research leads only.
- Preserve existing research history; proposals are safer than silent memo overwrites.
- Optional integrations must fail with clear install guidance when dependencies are missing.
- All generated HTML research pages should use an Apple-inspired visual style: white/light-gray surfaces, SF-system typography, restrained borders, clean spacing, and low-noise cards.
- Research graph outputs must preserve node/edge traceability from evidence to consensus, questions, hypotheses, assumption tests, and reports.

## DeepSeek Source Parsing Protocol

Use DeepSeek MCP as a source parser, not as the investment analyst of record.

Good DeepSeek inputs:
- A single研报、财报、年报、公告、新闻、访谈、会议纪要 or extracted passage.
- A narrow extraction request tied to one QA node.
- A required output schema.

Required DeepSeek output fields for research source parsing:
- `source_title`
- `source_bucket`: evidence, research_report, opinion, or message
- `key_facts`: factual points with numbers, dates, and page/section hints when available
- `support_refute_or_lead`: support, refute, or lead
- `affected_qa_node`
- `investment_relevance`
- `uncertainties`
- `follow_up_data`

Persisted source parsing artifacts:
- `source_extractions.jsonl`: one DeepSeek/source-parser record per source-to-L3/L4/L5 research-unit pair. Required fields: `extraction_id`, `l3_question_id`, `source_id`, `source_title`, `source_bucket`, `parser`, `parser_status`, `schema_fields`, `key_facts`, `inference`, `support_refute_or_lead`, `uncertainties`, `follow_up_data`, and `created_at`. The legacy field name `l3_question_id` may reference L3, L4, or L5. `schema_fields` must map every field requested by the unit `skill_dispatch.extraction_schema` to value, evidence IDs or review IDs, and status.
- Each `source_extractions.jsonl` record should also preserve `question_context`, `extraction_dimensions`, and `dimension_findings` when a question requires multi-dimensional parsing. `dimension_findings` must list every requested dimension with `found/gap`, facts, scope caveat, verification metrics, and support/refute/lead stance. A generic source summary without dimension findings is incomplete for refreshed canonical research when the question requires multiple evidence buckets.
- `leaf_source_reviews.jsonl`: one GPT verification record per extraction. Required fields: `review_id`, `extraction_id`, `l3_question_id`, `source_id`, `gpt_verification_status`, `adopted_facts`, `corrections`, `rejected_claims`, `final_bucket`, `final_support_refute_or_lead`, and `allowed_to_strengthen_conclusion`.
- Final HTML reports must not render these process artifacts unless the user explicitly asks to inspect parsing traces.

Do not let DeepSeek:
- Decide the final thesis.
- Rank target strength.
- Produce buy/sell/hold instructions.
- Resolve conflicting sources without GPT review.
- Strengthen a conclusion from low-reliability information.
