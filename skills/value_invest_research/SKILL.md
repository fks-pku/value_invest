---
name: value-invest-research
description: Use for investment research workflows that start from a user research goal and produce an auditable QA drilldown, evidence-linked synthesis, and specific target observation list. This skill has one canonical research-goal QA framework.
---

# Value Invest Research Skill

This Skill turns heterogeneous market information into auditable research artifacts. The default sequence is a single research-goal QA framework with a research-type adapter and specialty skill dispatch:

1. Stage 1: Define the research problem — research type classification, domain playbook selection, run mode, project.json.
2. Stage 2: Build industry overview — current default is the S-curve simplification: `S曲线与产业空间`, `技术链与BOM呈现`, and `关键变量与待验证数据`. Competition/profit-pool and chokepoint modules are optional deepening modules, not first-pass requirements.
3. Stage 3: Generate QA tree from pending_questions — L2 mechanism buckets from domain playbook, L3 decision questions with same "think → search → parse" loop, adaptive L4/L5 decomposition only when triggered.
4. Stage 4: Synthesize target recommendations — deterministic ranking from four core dimensions, scarcity-first gate, freeze before labels.
5. Stage gates: validate-project-schema → validate-industry-overview → validate-research-artifacts --require-l3 → validate-report-contract --require-l3.

## Non-Negotiable Rules

- Do not issue final trading instructions.
- For code changes, follow the hexagonal architecture contract in `docs/architecture/hexagonal_research_system.md`: domain is pure, application depends on domain and ports, adapters implement system edges, and new/refactored modules should move as tested vertical slices.
- New research topics must enter through `ResearchGoal -> DomainPlaybook -> QuestionArchitecture`; do not start from a report template or hard-coded HTML outline.
- Public reports should be assembled through `ResearchProjectRepository -> ReportViewModel -> CanonicalReportRenderer`. Domain/playbook code owns question meaning; renderer adapters own HTML presentation; application orchestrates the sequence.
- Separate facts, inferences, and judgments.
- Cite evidence IDs for every material claim.
- Treat low-reliability sources as research leads only.
- Search for disconfirming evidence before strengthening a thesis.
- Preserve prior thesis history when updating a memo.
- Mark uncertainty directly instead of hiding it.
- Use the canonical research-goal QA framework by default for every new research goal, topic, company, sector, event, or concept.
- Do not combine multiple templates.
- Current effective framework priority is S-curve discovery. Spend roughly 80% of the first-pass research effort on the S curve itself: new-technology prospect, feasibility, future industry space, adoption inflection, and whether demand is becoming irreversible. Keep BOM as a presentation map in the first pass: who is on the chain, what each company/node receives, what it produces, and whom it supplies. Do not force detailed competition/profit-pool/chokepoint analysis until the user asks for the next iteration or the playbook explicitly requires it.
- Before building Q1-Q4, classify the research type and adapt the meaning of Q1-Q4. Do not force every topic into demand/bottleneck/target wording.
- Before building Q1-Q4, create `行业概况` with `supply-chain-panorama-explainer` and relevant domain playbooks. It must contain five public modules: `产业链与生态位`, `行业空间`, `竞争格局与利润池`, `瓶颈点`, and `关键变量与待验证数据`. Each module must render as a clickable collapsed `details.industry-module > summary.module-head` card with `module-index`, `chevron`, and `industry-module-body`. `产业链与生态位` must keep the important chain information: upstream/midstream/downstream swimlane view, beginner-readable value-flow view, and `component-value-chain`. These three long chain components must render as nested clickable `details.chain-detail-panel` cards. `行业空间` must stay scoped to direct BOM-node space reasoning only: current scale anchors are evidence, while the conclusion answers which BOM/subsystem nodes future demand may expand and why. It must render `industry-space-summary` plus `space-bom-reasoning`; every key node must be a collapsed `details.space-node-card` with a single-column `space-node-reasoning` body: `space-node-space-reasoning` first and `space-node-evidence` below it. Do not render separate risk/refute or conclusion cards inside the BOM node. The 空间推理 block must include a compact ordered `space-node-sizing` public-method record: `1 公开拆法`, `2 空间结论`, plus confidence and source chips. Search public sources for company guidance, company TAM, customer-side guidance, third-party sizing, and financial execution evidence before writing this block. The public-method area must render five fixed full-width method cards stacked vertically in order: `公司指引`, `公司 TAM`, `客户侧指引`, `第三方拆法`, and `财务兑现证据`. Each method card should keep source type and count on the left, and show available entries on the right with `公司或机构`, `指引内容`, `BOM 节点`, `时间范围`, `可验证指标`, and `置信度`; every non-empty entry must have its own concrete evidence selection and render `space-method-entry-sources` source chips, rather than borrowing from a coarse BOM-node evidence pool. Missing classes must show `待补` instead of disappearing. GPT may summarize public methods and judge 短期、中期、长期 space from the five evidence classes, but must not output a self-built precision TAM as investment evidence. If reliable public methods are unavailable, show the missing source/data gap rather than inventing precision. It must not answer competition, profit-pool ownership, valuation, or target ranking. `竞争格局与利润池` and `瓶颈点` must also organize by BOM/subsystem node: competition cards answer four fixed questions, `玩家市场份额分布`, `头部玩家优势分析`, `替代玩家赶超希望`, and `格局变化核心变量`; competition answers must render as natural `overview-answer-prose` paragraphs with blue inline source links, not the generic `当前判断` / `关键事实` / `推理链` row template. Inline source links must sit next to the supported number, fact, or claim rather than being clustered only at the paragraph end; source chips remain an audit index and must only list source IDs actually cited or explicitly attached to the current answer. `玩家市场份额分布` must provide concrete share/distribution numbers when a reliable public comparable source exists; otherwise it must explicitly state the comparable-share gap and label any proxy figures. Profit-pool ownership is summarized separately in `profit-pool-table`; chokepoint cards answer concrete constraint, controller, scarcity duration, release/substitution path, score/downgrade rule, and target/monitoring implication. Inside every BOM card, child method/question cards must render as a single-column full-width stack, not side-by-side: `space-method-card-grid`, `competition-question-grid`, and `chokepoint-question-grid` must use `grid-template-columns: 1fr`. The value-flow view must start with plain-language steps and define unclear industry terms such as "系统交付" before showing detailed flow cards. This is the mandatory fact-map input to Q1-Q4 question design, Q2 value-capture analysis, Q3反证, and Q4 target ranking.
- Define one visible BOM taxonomy inside `产业链与生态位` using `bom-taxonomy`, `bom-taxonomy-grid`, and `bom-taxonomy-card`. This taxonomy is the public primary key for the industry overview. `行业空间`, `竞争格局与利润池`, `瓶颈点`, `关键变量与待验证数据`, QA artifacts, and `标的推荐` target mapping must reuse those exact public node names and expand one-to-one for every BOM node defined in `产业链与生态位`. Missing a BOM taxonomy node in a later public module is contract-invalid. Source excerpts may keep narrower original wording, but public node labels must not drift. Demand/customer capex is a supplementary demand-validation layer, not a BOM node, and cannot replace a required BOM-node card.
- Every analytical module inside `行业概况` must follow the same minimum-question execution protocol, not only `行业空间`: split the module into research units, split each research unit into core minimum questions, create a question-level `source_universe_plan`, create a question-level `exa_search_plan`, parse selected materials against that question's dimensions, then write a verified answer with source chips or an explicit gap. The search plans are internal execution artifacts and must not be rendered in final public HTML. The public HTML component family for these question cards is `overview-research-unit`, `overview-question-card`, `overview-answer`, source chips, and inline source links where cited. Inline links should be claim-near; do not write a long paragraph and put all source links only at the end. Bottom source chips must reflect the current card's actual cited/attached evidence, not a broad node-level source pool. In backtest mode, both universe-selected materials and Exa hits must pass cutoff visibility before they can support the answer.
- Do not render a separate high-level structured chain overview table by default. Use nested chain detail panels for the swimlane, value-flow, and component/BOM views; keep any more detailed relationship map in internal workbench artifacts unless the user explicitly asks to expose it.
- Keep `行业概况` and `下钻 QA` complementary. `行业概况` is the map layer: baseline facts, ecosystem coordinates, value/profit flow, candidate chokepoints, key variables, and the open questions it creates. `下钻 QA` is the decision-interrogation layer: it must add evidence verification, financial bridge, contradiction resolution, valuation/odds judgment, company comparison, kill test, or target-ranking impact. Do not repeat overview map/table artifacts inside Q1-Q4 L1 cards; use L1 synthesis prose and deeper L2/L3 decision artifacts instead.
- Industry/theme and technology-route reports must render professional research artifacts in the existing sections: `constraint-definition` in current research goal, `competition-bom-map` and `profit-pool-table` in competition/profit-pool, `chokepoint-bom-map`, `chokepoint-scorecard`, and `bottleneck-release-timeline` in bottlenecks, and `target-profit-bridge` plus `target-valuation-table` in final target recommendation. Public competition/profit-pool modules must not render a separate technology-route matrix table; route comparison should be absorbed into the relevant BOM card questions or kept in internal workbench artifacts.
- Default research types are industry/theme opportunity, single company, event/policy, technology/product route, target update, and custom user-defined type.
- Use `investment-question-architect` before evidence collection. Question quality controls research depth; every L3-L5 research unit must state decision use, required materials, support evidence, refuting evidence, target implications, and preferred specialty skill.
- For event, conference, keynote, product-launch, investor-day, and policy-meeting research, route through the event/conference adapter. The first question layer must establish official fact boundary and new-information delta; later layers must bridge event claims to product route, customer/order evidence, company financial exposure, valuation odds, disconfirming tests, and target ranking.
- Treat every L3-L5 research unit as a decision unit. Refreshed canonical QA trees must store `decision_use`, `materiality`, `support_evidence`, `refute_evidence`, `target_implications`, `score_component`, `minimum_evidence_gate`, and `refuting_source_plan`, so weak or decorative questions can be rejected before source work starts.
- Use `research-source-planner` before reading materials. GPT is responsible for deciding which source universe to use for each research topic and smallest active question. Treat the user as a non-specialist unless they explicitly override the process: the user provides the goal, while GPT classifies the domain, selects/combines the professional universe from `config/source_universes.json`, adds justified candidate sources when needed, and records why each universe was chosen. Exa/Perplexity/OpenAI-compatible search can supplement recall, but must not replace GPT's source-universe routing. Every L3-L5 research unit needs a concrete source plan and at least one refuting or boundary-check source plan. Every minimum question inside `行业概况` also needs a concrete `source_universe_plan` and `exa_search_plan`; this includes competition/profit-pool questions and chokepoint questions, not only industry-space questions. For every `行业空间` BOM/subsystem node, first build a five-bucket source-search matrix after BOM node identification: `公司指引`, `公司 TAM`, `客户侧指引`, `第三方拆法`, and `财务兑现证据`. Do not loosely match a coarse evidence pool to these cards. Each bucket needs search query/terms, expected fields, visible date/cutoff status, allowed usage, preferred parser skill, selected source IDs when found, or `status=gap` with `gap_reason` when not found. Each bucket must also use the domain source universe in `config/source_universes.json` to generate `priority_sources` and site/domain `directed_queries`; for AI factory / semiconductor hardware, this must include professional sources such as SemiAnalysis, TrendForce, Omdia, TechInsights, Dell'Oro, LightCounting, company IR, and customer IR when relevant. Each rendered public-method entry needs its own source IDs. Extract scope, period, formula/decomposition, assumptions, output value, source date, and口径 caveat. GPT may summarize, align, and sanity-check those methods; it must not create a proprietary TAM estimate when no public method exists.
- Source parsing is question-dimensional. Start from the smallest active question, define the source universe, then define all dimensions that matter under that question. Parse every selected material against every requested dimension; do not stop after one matching bucket. A single earnings release, filing, transcript, or research report can simultaneously provide company guidance, company TAM, financial execution evidence, and other clues. Missing dimensions must be explicit gaps with scope caveats, while partial matches such as company-wide outlook should be retained with caveats instead of dropped.
- QA drilldown is adaptive up to five layers. L1 is the adapted Q direction, L2 is the mechanism bucket, L3 is the investment decision question, and L4/L5 are optional bottom-up workbench/research units. Create L4/L5 only when the parent question remains too broad, spans multiple companies or chain nodes, needs a table/model/scorecard, mixes financial bridge and valuation/risk, has more than three material classes in its source plan, or cannot answer beyond "needs verification" without more granular work.
- `source_plan` must be structured by concrete source, expected fields, information bucket, visible date/cutoff status, allowed usage, preferred parser skill, and historical-mode `availability_proof` when applicable. A bare prose source-plan sentence is not sufficient for refreshed canonical reports.
- Every research run must declare its mode before source collection: historical training/backtest mode or live prediction mode. Historical training/backtest mode is the default for new research runs unless the user explicitly asks for current/live/real-time research. Historical mode uses an `as_of_date` cutoff, defaulting to three calendar months before the evaluation date/report date unless the user specifies another cutoff. Live mode uses currently visible information and carries a future review trigger instead of a future return label.
- In historical training/backtest mode, source collection, parsing, QA answers, valuation context, and target ranking may only use information publicly visible on or before `as_of_date`. Materials visible after `as_of_date` are look-ahead data and must be rejected or quarantined, except for the separate price-label dataset attached after the target list is frozen. Public backtest reports must read as if written on the `as_of_date`: no QA conclusion, target rationale, score explanation, odds model, downgrade trigger, or summary text may discuss ex-post winners, losers, realized returns, calibration lessons, or later price action.
- Historical backtests must include anti-leakage controls beyond source dates. A current LLM's background priors are not evidence. Use model prior only to frame hypotheses, then require cutoff-visible source IDs or GPT-verified leaf review IDs for every fact, parent rollup, score subcomponent, target rank, and action state. Store this as `anti_leakage_controls` in `qa_tree.json` and `backtest_grounding` on every L3-L5 research unit.
- When the user changes a report structure, interaction pattern, section order, or presentation logic, treat that change as a persistent default research-system requirement unless the user explicitly says it is one-off.
- In the same change, update `AGENTS.md`, this `SKILL.md`, and `frameworks/research_goal_qa.md` so future reports follow the new structure.
- Research output must be organized by QA directions, not standalone step components. For industry/theme opportunity, default to Q1 confirm industry space and demand, Q2 analyze competitive landscape and identify value-capturing chokepoints, Q3 bind disconfirming tests and priced-in risk, Q4 build valuation odds and target observation list with reasons. For other research types, first define the adapted Q1-Q4 map in the execution plan.
- For industry/theme opportunity and technology/product-route research, Q2 must include an explicit competitive-landscape analysis before chokepoint evaluation. The Q2 flow is: identify competitors and substitutes in each node, test customer bargaining power and supply expansion, then decide which nodes are true chokepoints. The chokepoint scorecard must stay inside the relevant Q2 competition/value-capture node and must evaluate demand flow, irreplaceability, supply/access constraint, pricing power, financial conversion, market pricing, and disconfirming trigger.
- Chokepoint evaluation must use a declared score schema with dimension weights, scoring definitions, and downgrade rules. If a dimension lacks evidence, score it conservatively and list the missing data.
- Scarcity-first opportunity gate: the default action state is `no_action`. Do not search for reasons to recommend a theme. Search for a currently underpriced large opportunity where future demand flows into a company's scarce, hard-to-substitute product/service and can convert into financial value.
- `actionable_long` requires all four core target dimensions: `scarcity_or_monopoly`, `mispricing`, `earnings_elasticity`, and `risk_control`. If one dimension fails, cap the score and use `watch_only` or `no_action` even when the industry is exciting.
- Every level must state what questions to ask, how to collect information, how to connect information into reasoning, and how to present the output.
- Every QA layer must present information in this order: current conclusion, question expansion/child QA, then remaining questions or data gaps.
- Use adaptive QA depth up to five layers by default: Q1, Q1.1, Q1.1.1, Q1.1.1.1, Q1.1.1.1.1. Do not force every branch to L5; stop when the parent conclusion is already evidence-backed and decision-useful.
- Details, scorecards, tables, and jump pages must be nested under the QA layer whose question they answer, not placed as Q-parallel components or unrelated top-level appendices.
- Bottleneck/chokepoint scorecards belong under the relevant Q2 competitive-landscape/value-capture question. They are outputs of competition analysis, not Q-parallel components.
- Final target recommendation must use the Q2 chokepoint evaluation. Target strength is invalid unless it reconciles chokepoint score or score drivers with future space, valuation odds, evidence quality, and Q3 downgrade triggers.
- Final target recommendation must include the four core target dimensions, a compact score breakdown, a target profit bridge, a valuation/odds table, and simplified odds model. The four public dimensions are `scarcity_or_monopoly`, `mispricing`, `earnings_elasticity`, and `risk_control`; the underlying score breakdown must preserve auditable `score_subcomponents` for every component, with subdimension name, score, weight, evidence IDs or GPT review IDs, rationale, and status. The public `target-profit-bridge` must show how demand enters each target's revenue, margin, FCF, or backlog. The public `target-valuation-table` must show whether growth appears underpriced or already reflected. The odds model should state what the current valuation appears to require, the base/bull/bear verification path, and what data would upgrade or downgrade the observation. In public HTML these must render inside `标的推荐` before the dense target table; Q4 should summarize the same odds gate inside the current-conclusion block.
- Final target recommendation must include `action_state`: `actionable_long`, `watch_only`, or `no_action`. Weak scarcity, missing/stale valuation, non-positive expected excess return, generic theme exposure, or uncontrolled disconfirming risk must prevent high strength.
- Final target ranking must be deterministic from frozen score fields: action-state priority, opportunity fit, total score, payoff convexity, thesis confidence, then stable ticker/name tie-break. Do not manually reorder targets after labels are attached.
- Every `actionable_long` target must include hard `thesis_kill_tests` with test, evidence needed, downgrade action, and source plan; otherwise cap it at `watch_only`.
- Disconfirming-test lists belong under the relevant risk question, usually Q3.1.
- Target tables belong under the relevant target-selection question, usually Q4.1.
- In historical training/backtest mode, Q4 must still retain as-of target-selection child questions. Do not replace Q4's child QA with the final label table, and do not create a Q4 child whose purpose is to evaluate later returns.
- Each layer may only roll up conclusions from its child answers and auditable sources.
- L3-L5 answers must separate fact, inference, judgment, gap, and trigger. Fact must be sourced observations or extracted source summaries; inference must explain how those facts answer the unit question; judgment must state the decision impact. These fields must not repeat the same sentence.
- L3-L5 answers must include materiality: why the answer changes the parent conclusion, target strength, valuation odds, or risk controls.
- L3-L5 answers must preserve the question-quality fields: `decision_use`, `support_evidence`, `refute_evidence`, `target_implications`, `score_component`, `minimum_evidence_gate`, and `refuting_source_plan`. The `score_component` must connect the unit to ranking drivers such as future space, chokepoint strength, valuation odds, evidence quality, disconfirming-risk control, monitorability, payoff convexity, target ranking, or action state.
- For every L3-L5 research unit, GPT must decide which materials to search or read, define the extraction schema, and assign those concrete materials to DeepSeek MCP for careful reading.
- Before assigning an L3-L5 research unit, classify its task family and use the most relevant specialized skill when available: `financial-statement-analysis` for filings/financial statements, `valuation-analysis` for valuation/priced-in expectations, `industry-report-analysis` for third-party reports/datasets, `event-to-investment-analysis` for public events/conferences/launches, `conference-transcript-analysis` for keynotes/transcripts/slides/demos, `supply-chain-chokepoint-analysis` for Q2 competition-derived scarcity/chokepoint scoring, `company-exposure-analysis` for mapping a node into company revenue/margin/orders/FCF, `news-event-analysis` for messages/news/policy leads, `opinion-analysis` for expert or investor viewpoints, `leaf-research-deepseek` for long source parsing, `target-recommendation-analysis` for Q4 target observation lists, `target-ranking-analysis` for deterministic target ranking after Q1-Q3 are verified, `quant-research-fks` or `quantitative-research` for systematic strategy questions, and `frontend-design` for HTML/report interface work.
- Every L3-L5 answer must include `skill_dispatch` as a structured object with `task_family`, `selected_skill`, `concrete_materials`, `extraction_schema`, `source_extraction_ids`, `leaf_source_review_ids`, `skill_output_status`, `fallback_used`, and `gpt_verification_status`. A bare skill name or prose chain is contract drift.
- Every research run should persist source-parser outputs in `source_extractions.jsonl` and GPT verification records in `leaf_source_reviews.jsonl`. DeepSeek MCP is the default parser for long materials and selected source excerpts; GPT parses directly only for short materials, failed tool calls, or verification-sensitive cases, and must record the fallback reason.
- Every source-parser output must include `schema_fields` that fill the L3-L5 `skill_dispatch.extraction_schema`; generic summaries without schema-field mapping are insufficient for refreshed canonical answers until GPT maps and verifies them.
- `source_extractions.jsonl` is the token-saving reading layer. It stores DeepSeek/source-parser facts, inferences, uncertainties, and follow-up data by source-to-research-unit pair. `leaf_source_reviews.jsonl` stores GPT corrections, adopted facts, rejected claims, and whether the extraction may strengthen the QA answer.
- If one L3-L5 research unit requires multiple skills, chain them rather than flattening them. Use financial-statement-analysis before valuation-analysis when valuation depends on freshly parsed filings or earnings releases.
- DeepSeek should produce the first structured L3-L5 reading answer from those materials: fact, inference, preliminary judgment, gap, trigger, source links, and support/refute/lead stance.
- GPT must verify DeepSeek's L3-L5 answer against source links or local files, resolve conflicts, correct unsupported claims, and write the final answer and parent rollup.
- If investment implications exist, final output must map to specific securities or assets with ticker/name, bottleneck or thesis node, reason, strength, required verification data, catalysts, risks, and source links.
- Target output must also include chokepoint exposure, chokepoint score or score drivers, future space, current valuation odds or a clear valuation-data gap, downgrade triggers, and monitorability. Do not raise observation strength if valuation is missing or chokepoint capture is weak.
- Every target or major thesis node should preserve a prediction review field: initial claim, validation horizon, required evidence, current status, and review trigger. The final HTML may summarize this inside Q3/Q4; detailed tracking can live in workbench JSON.
- In historical training/backtest mode, freeze the final target list and ranking before attaching ex-post labels. Each target label should include `as_of_date`, `evaluation_date`, `label_window`, adjusted or total-return price at both endpoints, `forward_3m_return`, benchmark or sector return when available, excess return when available, price source, and label status. The label is evaluation metadata only and must not strengthen the historical thesis or alter the frozen recommendation. Render later price movement only once in final HTML, inside an isolated target-table label block or rightmost label columns.
- Label availability must not define the investment universe. Target selection starts from the actual value-capture securities or assets across exchanges. If a non-US/local listing lacks a verified label, keep it in the frozen target list and mark `label_status: label_unverified_*` rather than substituting a convenient US proxy.
- Use `framework_contracts.py` as the executable contract layer: validate report hierarchy/card structure, validate QA tree schema, validate source-extraction schema fields, audit time-sliced sources and availability proof, score targets with separate thesis confidence/payoff convexity plus auditable subcomponents, rank targets deterministically, validate target kill tests, freeze recommendations before labels, attach labels, build training samples, build prediction reviews, and bundle internal workbench traces.
- Use `frameworks/research_quality_gate.md` as the operational completion gate. A complete refreshed report is not done until `qa_tree.json`, `source_extractions.jsonl`, `leaf_source_reviews.jsonl`, and `investment_workbench.json` pass artifact validation.
- In historical mode, artifact validation must pass the anti-leakage gate: exact L3 source-pack grounding, no non-source claims, no label-only source in QA/source parsing, and target score subcomponents linked to cutoff sources or GPT-approved reviews.
- Keep `tests/fixtures/research_quality_gold/` passing as the gold regression fixture for framework changes.
- DeepSeek's primary role in research is parsing concrete source materials: research reports, news/messages, earnings releases, annual reports, filings, transcripts, expert interviews, and other single-source documents.
- Delegate a source to DeepSeek only after GPT has defined the research question, source priority, and extraction schema.
- When multiple dimensions matter, include the dimension list in the DeepSeek prompt and require `dimension_findings` for every requested dimension. DeepSeek/source-parser must scan the whole selected material for all dimensions under the question, not classify the source once and stop. GPT must verify the output and correct bucket mistakes before synthesis.
- DeepSeek should return structured extraction: key facts, numbers, dates, source bucket, support/refute/lead stance, affected QA node, uncertainty, and follow-up data needs.
- For L3-L5 research units, DeepSeek is the default first-pass reader and answer drafter for the selected materials.
- DeepSeek may also support source summarization, key-point extraction, initial classification, and candidate-question drafting.
- For formal investment source parsing, assume DeepSeek can use a very large input context when the MCP server/model supports it. Do not prematurely split a long filing, transcript, report, or source pack only because it exceeds GPT's comfortable reading window; preserve full source context when source integrity matters, up to the server-supported context limit.
- `max_tokens` is the output budget, not the input context window. Call DeepSeek with a large `max_tokens` budget by default: normally 32000-64000 tokens for long-source extraction, at least 24000 tokens for multi-source L3 drafts, and at least 12000 tokens for ordinary single-source parsing unless the task is intentionally tiny.
- Keep DeepSeek calls narrow by research question and extraction schema: prefer one complete source or coherent source bundle for one L3-L5 research unit. Even with a large token budget, require compact output limits unless exhaustive extraction is needed.
- If DeepSeek output is truncated, malformed, empty, or stops mid-field, record the delegation as incomplete. Do not use incomplete output for conclusions; retry with a smaller chunk or use GPT-verified source parsing.
- DeepSeek must not produce final judgments, trading instructions, financial conclusions, architecture decisions, target strength ranking, source reliability adjudication, or unchecked target recommendations.
- GPT remains responsible for source selection, source reliability checks, cross-source conflict resolution, reasoning synthesis, target strength, final report language, and all user-facing conclusions.
- Do not call a company "good" without naming the M driver and the M defect risk.
- Do not promote an idea without a time frame and disconfirming tests.
- For industry/theme opportunity and technology/product-route research, do not stop at a broad Q1-Q4 outline. Build a mechanism-depth map before source collection: demand driver tree, supply or access response, unit economics/profit bridge, competitive value-capture map, market-pricing bridge, counter-supply/disconfirming tests, capital-chain or second-order beneficiaries, and model/口径 reconciliation.
- Domain-specific depth requirements live in `frameworks/domain_playbooks.md`. Use that file when selecting or synthesizing a playbook; for storage/memory research, use its memory industry playbook so the QA tree forces workload-to-memory demand, demand-supply slope mismatch, product price/unit economics, company value capture, capex cycle, market-pricing rerating, counter-supply/substitution, and model口径 reconciliation.

## The "Think → Search → Parse" Loop

Every minimum research unit (BOM node in Stage 2, L3 leaf question in Stage 3) executes this loop:

1. **Think**: GPT writes a `source_plan` before any search. It owns domain classification and universe selection, then states decision_use, expected_fields, priority_sources (from `config/source_universes.json` plus justified candidate sources when needed), directed_queries, and preferred_parser_skill. Written into the unit as an auditable record.
2. **Search**: LLM executes web searches using `web_search_prime` + `webfetch` (primary). Collected materials → `sources.jsonl` with `source_visible_at` and `cutoff_status`.
3. **Parse**: DeepSeek MCP reads materials → `source_extractions.jsonl` (fills `schema_fields`). GPT verifies → `leaf_source_reviews.jsonl`. Verified facts feed into the unit answer.

If 3 rounds of directed search produce no usable results → `status=gap` + `gap_reason`. Do not invent numbers.

## LLM Analyst Behavior Rules

- **One unit at a time**: Complete one BOM node or one L3 leaf before starting the next.
- **Think before searching**: Every search is preceded by a written source_plan stating why, what, where, and how.
- **Gap is an answer**: After 3 rounds of directed search with no usable results, write `status=gap` + `gap_reason`. Do not create proprietary estimates.
- **Concrete citations**: Every fact carries a source_id. No unattributed prose.
- **Self-challenge**: After each supporting source, actively search for one refuting source. Record "no public refutation found" if none exists.
- **No skipping**: Modules skipped only with domain playbook exemption. L3 questions deleted only with domain playbook justification.
- **Stage gate reporting**: At each stage start, output current stage, completed stages, next sub-unit, and pending gate command.
- **Refresh behavior**: Skip chain rebuild if industry structure unchanged; refresh only time-sensitive space data; add L3 only for new gaps; always re-synthesize Stage 4.

## HTML QA Presentation

The final report presentation contract is `frameworks/research_report_contract.md`. Use it as the default for all future research reports unless the user explicitly asks to iterate on the framework.

- Current locked report contract:
  - Top-level order is exactly `当前研究的问题` -> `行业概况` -> `下钻 QA` -> `标的推荐` -> `来源索引`.
  - `行业概况` is mandatory and must render as `industry-overview-section` with clickable `details.industry-module` blocks. Current first-pass default modules are `S曲线与产业空间`, `技术链与BOM呈现`, and `关键变量与待验证数据`. The chain/BOM module must include `supply-chain-section`, `chain-explain`, `chain-research-bridge`, `chain-node-lens`, `chain-plain-summary`, nested `details.chain-detail-panel`, `chain-lane-map`, `chain-value-flow`, `chain-simple-flow`, `component-value-chain`, `bom-taxonomy`, `bom-taxonomy-grid`, `bom-taxonomy-card`, `chain-layer-grid`, `chain-layer-card`, `chain-relationship-graph`, `chain-stage-panel`, `chain-company-list`, and `chain-company-card`. The S-curve space module reuses `industry-space-summary`, `space-bom-reasoning`, `space-node-card`, `space-node-reasoning`, `space-node-evidence`, `space-node-space-reasoning`, `space-node-sizing`, `space-method-step`, `space-step-title`, `space-step-index`, `space-public-methods`, `space-method-card-grid`, `space-method-card`, `space-method-card-body`, `space-method-entry`, `space-method-entry-sources`, `space-method-empty`, `space-horizon-conclusion`, `space-horizon-grid`, `space-horizon-card`, `space-node-sizing-table`, and `space-step-confidence`; every node card presents 空间推理 first, `1 公开拆法`, `2 空间结论`, then 证据 below. Competition/profit-pool and bottleneck components may still be used in optional deepening, but they are no longer mandatory in the first S-curve report.
  - `下钻 QA` preserves the full adapted Q1-Q4 QA tree and must render L3 questions plus any adaptive L4/L5 research units in complete refreshed reports unless the user explicitly asks for a shorter executive version.
  - Q4 remains the auditable as-of target-selection QA node with child questions.
  - `标的推荐` is a standalone presentation rollup, not a replacement for Q4.
  - The hierarchy and format rules in `frameworks/research_report_contract.md` are validation requirements. A complete refreshed report is invalid if it drops L3, moves Q4 out of `下钻 QA`, duplicates child-question lists beside inline cards, replaces the canonical component family, or adds public process appendices.
  - Four non-drift locks must always hold: hierarchy and format lock, industry-overview lock, backtest time-slice lock, and frontend card-style lock. In backtest mode, only cutoff-visible information can drive source collection, QA reasoning, scoring, odds, and target ranking; the only current-time data allowed in final HTML is the final-target evaluation label.
  - Public no-changelog lock: final HTML must not include change-log, upgrade-log, "本轮/本次升级", "本轮/本次更新", "本轮如何落实", mechanism-depth checklist, framework explanation, execution trace, tool trace, or workbench/process commentary unless the user explicitly asks to inspect process. Framework upgrades should change the QA tree, evidence, scoring, and target reasoning, not add public meta text.
  - QA card interaction is part of the frontend lock. Every `qa-card level-1/2/3` must render as clickable `details.qa-card` with `summary`, `qa-count`, and `chevron`, default `open`; static `article/div.qa-card` output is contract drift.
  - In historical training/backtest mode, public prose must read as if written on the `as_of_date`; later price movement appears only once in the isolated final target evaluation fields.
  - Do not add process appendices, execution traces, tool traces, iteration notes, or workbench sections unless explicitly requested.
  - Additive-iteration lock: framework changes are additive by default. New sections, fields, dimensions, skills, source schemas, or visual affordances must preserve existing public section order, canonical component classes, QA interactions, action-state color classes, target-table structure, source-collapse behavior, and no-changelog rules unless the user explicitly asks for a frontend/report redesign.
- Before marking a framework iteration complete, run regression checks on a new/refreshed report and one existing canonical report or fixture: `validate-report-contract`, `validate-research-artifacts` when artifacts exist, and a browser/DOM smoke check for QA card collapse plus action-state color classes when target states appear.
- Final user-facing HTML reports must have exactly five top-level sections: `当前研究的问题`, `行业概况`, `下钻 QA`, `标的推荐`, and `来源索引`.
- `标的推荐` should synthesize all QA information into a ranked observation list with specific targets, win probability, payoff odds, rationale, required verification data, and downgrade triggers.
- Q4 remains the auditable as-of target-selection QA node with child questions. The standalone `标的推荐` section is a presentation rollup and must not erase or replace Q4's child-question hierarchy.
- Historical training/backtest HTML reports should show the as-of cutoff and information cutoff in `当前研究的问题`, and should show later price movement only once inside `标的推荐` as evaluation fields separate from the original rationale. Do not mention evaluation results in QA conclusions or summary prose. Live prediction HTML reports should omit future return labels and show the next review trigger instead.
- For bottleneck/chokepoint-driven research, `标的推荐` must show how chokepoint evaluation affects rank and strength.
- Do not put iteration notes, "what changed", execution traces, quality-framework explanations, tool attribution, DeepSeek usage notes, or workbench appendices in the final HTML. Keep those in workbench JSON, logs, or internal artifacts.
- Do not describe framework changes inside final HTML. Phrases such as "本轮升级", "本次更新", "本轮新增", "机制深度映射", "本轮如何落实", or "what changed in this run" are public meta drift and belong only in internal artifacts or chat replies.
- Preserve the full available QA tree when refreshing a report. Do not compress the report down to only a few questions unless the user explicitly asks for an executive summary.
- Every visible L3-L5 research-unit card must include a compact metadata strip showing selected `Skill`, actual `Execution` status, `Score Component`, and `Decision Use`. This lets the reader verify both the intended professional lens and whether that parser route actually ran, without exposing the full execution trace. `Execution` must come from `skill_output_status` plus `fallback_used`, not from the selected skill name alone.
- Do not overload L3 under a single catch-all L2. L2 should split L3 leaves into meaningful mechanism buckets selected by the research-type adapter and domain playbook.
- The report contract defines presentation and hierarchy only. Concrete question sets, metrics, parsing schemas, tracking indicators, and threshold rules live in domain playbooks or research-type adapters.
- Inside every QA card/details node, use a consistent three-part display: `1. 当前结论呈现`, `2. 问题展开（子 QA）`, `3. 待补充的问题`.
- If child QA nodes are rendered inline as expandable cards, do not also render a separate child-question list with the same titles. Use either jump links or inline child cards, not both.
- The current conclusion should be the shortest defensible rollup of facts, inference, judgment, and uncertainty.
- Parent-level answer artifacts such as `回答呈现`, scorecards,反证清单, target tables, and summary matrices belong under the current-conclusion section, before child QA expansion.
- The question expansion section should contain only child QA nodes or the tables/cards that directly answer that node.
- The remaining-questions section should name specific missing data, next evidence to collect, or disconfirming tests.
- Do not duplicate the same conclusion, child-QA list, or pending-question text in both a generated summary card and the body; use one sequential presentation.
- Keep source indexes collapsed by default unless the user explicitly asks to inspect sources.
- Refreshed canonical reports must reuse the shared report component contract from `frameworks/research_report_contract.md`: `constraint-definition`, `industry-overview-section`, clickable `details.industry-module`, `summary.module-head`, `module-index`, `industry-module-body`, `supply-chain-section`, `chain-explain`, `chain-research-bridge`, `chain-node-lens`, `chain-plain-summary`, `chain-detail-panel`, `chain-lane-map`, `chain-value-flow`, `chain-simple-flow`, `component-value-chain`, `bom-taxonomy`, `bom-taxonomy-grid`, `bom-taxonomy-card`, `chain-layer-grid`, `chain-layer-card`, `chain-relationship-graph`, `chain-stage-panel`, `chain-company-list`, `chain-company-card`, `chain-chokepoints`, `overview-research-unit`, `overview-question-card`, `overview-answer`, `competition-bom-map`, `competition-bom-card`, `competition-question-grid`, `profit-pool-table`, `bottleneck-release-timeline`, `chokepoint-bom-map`, `chokepoint-bom-card`, `chokepoint-question-grid`, `chokepoint-scorecard`, `key-variable-bom-map`, `key-variable-bom-card`, `chain-data-gaps`, `industry-space`, `industry-space-summary`, `space-bom-reasoning`, `space-node-card`, `space-node-reasoning`, `space-node-evidence`, `space-node-space-reasoning`, `space-node-sizing`, `space-method-step`, `space-step-title`, `space-step-index`, `space-public-methods`, `space-method-card-grid`, `space-method-card`, `space-method-card-body`, `space-method-entry`, `space-method-entry-sources`, `space-method-empty`, `space-horizon-conclusion`, `space-horizon-grid`, `space-horizon-card`, `space-node-sizing-table`, `space-step-confidence`, `table-scroll`, `industry-competition`, `industry-chokepoints`, `industry-key-variables`; `qa-card`; `artifact-card`; `target-section` with `target-profit-bridge`, `target-valuation-table`, `target-odds-model`, `target-odds-table`, and `target-table`; and a single collapsed `source-collapse`. Do not swap in alternate report components such as per-target `target-card`, grouped `source-bucket`, or `section-lead` layouts unless the user asks to redesign the frontend. Wide tables and dense card tables must sit inside `table-scroll` so they scroll horizontally instead of overflowing.
- QA cards must preserve built-in expand/collapse behavior by using `details.qa-card > summary`; the click target is the summary/header, and the card is open by default.
- `target-table` action-state cells must render with the canonical color class matching the value: `state-actionable_long`, `state-watch_only`, or `state-no_action`. Plain uncolored action-state text is contract drift.

## DeepSeek Source Parsing Protocol

Use DeepSeek MCP as a source parser, not as the investment analyst of record.

Good DeepSeek inputs:

- A single research report, earnings release, annual report, filing, public message/news item, expert interview, transcript, or extracted passage.
- A narrow extraction request tied to one QA node.
- A required output schema.

Required DeepSeek output fields for source parsing:

- `source_title`
- `source_bucket`: evidence, research_report, opinion, or message
- `key_facts`: factual points with numbers, dates, and page/section hints when available
- `support_refute_or_lead`: support, refute, or lead
- `affected_qa_node`
- `investment_relevance`
- `uncertainties`
- `follow_up_data`
- `schema_fields`: a map from every requested extraction-schema field to value, evidence IDs or review IDs, uncertainty/status, and source anchor when available.

For L3 reading tasks, require these additional fields:

- `l3_question`
- `selected_materials`
- `fact`
- `inference`
- `preliminary_judgment`
- `gap`
- `trigger`
- `source_links`

Review DeepSeek's extraction before using it. Correct bucket errors, verify material facts against links or local files, and discard unsupported claims.

Persist the parser/review trace:

- Write DeepSeek/source-parser outputs to `source_extractions.jsonl`.
- Write GPT verification outputs to `leaf_source_reviews.jsonl`.
- Keep both files as internal artifacts; do not render them in the final HTML unless the user asks to inspect the parsing trace.
- Prefer narrow DeepSeek prompts. Use one L3 question and one source or small source bundle. If a long prompt returns empty, retry smaller before falling back.

## Required Context Loading

Before analysis, load the relevant research object folder:

- Canonical memo.
- `evidence.jsonl`.
- `research_system/` artifacts when present.
- Structured files under `data/`.
- Latest run logs under `logs/`.
- Related stock, sector, theme, or event objects named in the task.

## Workflow Routing

- Default for any user-proposed research goal: use `frameworks/research_goal_qa.md`.
- No other framework, prompt, or checklist file is part of the active skill.
- Project-tracked specialty skill definitions live under `specialty_skills/`; use those as the source of truth for investment research leaf parsing and target analysis.
- Use `specialty_skills/supply-chain-panorama-explainer` for the `产业链与生态位` module inside public `行业概况` before Q1-Q4. It is the source of truth for beginner-readable Chinese chain explanation and must not be replaced by a jargon-only table.
- Within that framework, route each L3-L5 research-unit task through the specialty skill dispatch layer when a relevant skill exists. Specialized skills support extraction and analysis; GPT remains the final research director and verifier.
- Preserve the dispatch trace in generated workbench/report artifacts so the user can see which skill handled each concrete problem and how GPT verified it.

## Quality Pipeline

1. `investment-question-architect` designs the research questions.
   - It must produce a mechanism-depth map for model-heavy industry/theme research, so L2 buckets are real analytical mechanisms rather than generic summaries.
2. `research-source-planner` decides which materials to collect for each L3 question.
   - In historical training/backtest mode, every source plan records `as_of_date`, `source_visible_at`, and cutoff status.
   - For quantitative industry models, source plans must name expected table fields such as period, unit, volume, price, mix, capacity, utilization, cost, margin, capex, FCF, valuation multiple, implied expectation, and口径.
3. Specialty parsers read the materials:
   - `financial-statement-analysis`
   - `valuation-analysis`
   - `industry-report-analysis`
   - `news-event-analysis`
   - `opinion-analysis`
   - `leaf-research-deepseek`
4. Persist parser outputs to `source_extractions.jsonl`.
5. GPT verifies parsed facts in `leaf_source_reviews.jsonl` and writes the final L3 answer.
6. Parent QA nodes roll up only verified child answers.
7. `target-recommendation-analysis` turns verified conclusions into a specific observation list with future space, valuation odds, strength, risks, catalysts, required data, and explicit links back to the mechanism-depth drivers.
8. `target-ranking-analysis` reconciles the observation list into deterministic ranking fields: scarcity/monopoly, mispricing, earnings elasticity, risk control, score subcomponents, action state, payoff odds, and kill tests.
9. `framework_contracts.py` validates hierarchy, source cutoff, scoring separation, frozen recommendations, label attachment, training sample output, prediction review, and internal workbench separation before the final report is treated as canonical.
