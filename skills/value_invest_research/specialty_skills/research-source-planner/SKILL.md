---
name: research-source-planner
description: Use this skill after an investment QA tree exists and before reading materials. It creates a source-search plan for each L3-L5 research unit: which primary filings, earnings calls, industry reports, datasets, news, and opinions to collect, why each source matters, and which specialty parser should read it.
---

# Research Source Planner

This skill converts L3-L5 research units into concrete source plans. It is responsible for collecting the right information, not for final synthesis.

GPT is the end-to-end research analyst for source planning. The user may be a non-specialist and should not be expected to choose the correct source universe. For each research topic and smallest active question, GPT must classify the domain, select and combine the relevant professional universe from `config/source_universes.json`, add justified candidate sources when the registry is incomplete, and record why those universes and sources are needed. AI search engines are recall supplements, not replacements for GPT's universe selection.

Before L3-L5 source planning, make sure the run has a source plan for `产业链全景`. This plan should collect enough evidence to map upstream, midstream, downstream, key players, products/services, dependency links, company relationship edges, value/profit flow, and candidate chokepoints. Each material relationship edge should identify from, to, relationship, product/order/value flow, bottleneck, target mapping, and evidence. The chain map is a required public section and should be supported by primary/company/industry sources rather than unsupported background prose.

## Source Priority

Use this order unless the question requires otherwise:

1. Primary evidence: filings, annual reports, quarterly reports, earnings releases, exchange announcements, regulator documents, official datasets.
2. Company voice: earnings calls, investor presentations, investor-day materials, management Q&A.
3. Industry data and research reports: sell-side reports, SEMI, Gartner, TrendForce, IDC, S&P, Visible Alpha, trade bodies, reputable databases.
4. News/messages: public news, supply-chain updates, policy headlines, product launch messages.
5. Opinions: expert interviews, investor views, industry commentary.

For event/conference research, the first source pack must include official event materials before general news: agenda/session page, keynote transcript or replay, official press releases/blogs, speaker/company posts, product availability pages, partner/customer statements, and exposed-company filings or earnings calls. Third-party news may map timing and market reaction, but it is usually a lead until primary evidence confirms commercial impact.

## L3-L5 Source Plan Template

For each L3-L5 research unit, output:

- `l3_question`
- `materiality`: why the answer changes parent conclusion or target strength.
- `source_plan`:
  - `source_id` or stable planned source key.
  - `source_bucket`: evidence, research_report, message, opinion.
  - `source_type`
  - `examples_or_search_queries`
  - `why_needed`
  - `expected_fields`
  - `preferred_skill`
  - `allowed_usage`: thesis, label_only, lead_only, or quarantined.
  - `source_visible_at` and cutoff status when running historical training/backtest mode.
  - `availability_proof` when running historical training/backtest mode: publisher date, filing timestamp, exchange/regulator release page, archive timestamp, or dataset snapshot note.
  - `deepseek_allowed`: true or false.
- `minimum_evidence_gate`: what must be collected before strengthening the conclusion.
- `refuting_source_plan`: what to search specifically to disprove the thesis.
- `freshness_requirement`: latest quarter, latest filing, historical baseline, or event window.
- `planned_source_extractions`: records to create in `source_extractions.jsonl`, one per concrete source or small source bundle.

For event/conference L3-L5 questions, include these extra fields when relevant:

- `event_fact_boundary`: exact claim, speaker/source, date/session, official status, and product/customer/timing anchor.
- `new_information_delta`: what changed versus pre-event public knowledge.
- `commercialization_stage`: concept, prototype, qualification, production, shipment, revenue, or margin evidence.
- `event_to_financial_bridge`: product route -> customer/order -> revenue -> margin/FCF -> valuation.
- `company_exposure_fields`: segment exposure, customer concentration, margin bridge, capex/FCF impact, and dilution.

For supply-chain map sources, also output:

- `chain_layer`
- `players`
- `products_or_services`
- `dependency_links`
- `value_profit_flow`
- `candidate_chokepoints`
- `related_q2_q4_nodes`

## Industry Space BOM Source Search

For `行业空间`, do not start from a coarse evidence pool and loosely match sources to cards. After the supply-chain/component map identifies BOM or subsystem nodes, actively search each node across these five fixed buckets:

1. `公司指引`: company guidance on revenue, capex, orders, backlog, capacity, shipment, mix, pricing, or business growth.
2. `公司 TAM`: company-disclosed TAM, SAM, serviceable market, long-term CAGR, penetration, or market-size bridge.
3. `客户侧指引`: downstream customer capex, budget, RPO/backlog, order, workload, usage, deployment, or adoption guidance.
4. `第三方拆法`: sell-side excerpts, industry data providers, trade bodies, reputable public research, or investor presentations that disclose a sizing method, formula, or forecast.
5. `财务兑现证据`: reported revenue, segment growth, orders, backlog, margin, cash flow, capex, inventory, or utilization that verifies demand is becoming financials.

For every BOM/subsystem node, persist an `industry_space_source_search_matrix` row with one `category_search_plan` entry per bucket. Each bucket entry must include:

- `search_query` or `search_terms`
- `priority_sources`: domain-specific professional sources from `config/source_universes.json`; for AI factory / semiconductor hardware this should include sources such as SemiAnalysis, TrendForce, Omdia, TechInsights, Dell'Oro, LightCounting, ServeTheHome, Semiconductor Engineering, company IR, and customer IR when relevant.
- `directed_queries`: site/domain targeted queries for the priority sources, not only broad keyword search.
- `search_intent`
- `expected_fields`: scope, period, formula/decomposition, assumptions, output value, unit/currency, source date,口径 caveat, and verification metric.
- `source_bucket`
- `visible_date_policy`, `source_visible_at`, cutoff status, and `availability_proof` in historical/backtest mode.
- `allowed_usage`: usually `historical_thesis` or `lead_only`; never use post-cutoff material to strengthen a time-sliced thesis.
- `preferred_parser_skill`
- `parser_assignment`: whether DeepSeek/source-parser should read the concrete material.
- `status`: `found` with `sourceIds` when usable materials exist, or `gap` with `gap_reason` when they do not.
- `selected_materials`: concrete source IDs and why each one belongs to that bucket.

Every non-empty public-method entry rendered in `行业空间` must be traceable to the matching bucket-level `sourceIds`. If a bucket has no reliable source, keep the bucket visible as a searched gap; do not fill the blank with model-created TAM, unsourced estimates, or generic narrative evidence.

If `priority_sources` or `directed_queries` are missing, the source plan is incomplete even if it has a generic query. A gap should distinguish `searched_no_reliable_source`, `paywalled_or_no_access`, `post_cutoff_only`, and `planned_not_executed` when possible.

## Question-Dimensional Parsing

Source planning must start from the smallest active question, not from a generic source list. For each L3-L5 unit or BOM-node question:

- Define the question-specific source universe first, combining newly searched materials with already collected source IDs.
- Define the dimensions that must be inspected inside each source, such as `公司指引`, `公司 TAM`, `客户侧指引`, `第三方拆法`, `财务兑现证据`, margin, capex, backlog, qualification, ASP, customer adoption, or refuting evidence.
- Assign each concrete source to every relevant dimension. A single source may satisfy multiple dimensions and should not be consumed by only the first matching bucket.
- Require DeepSeek/source-parser to return `dimension_findings` for every requested dimension, each with found/gap, facts, scope caveat, verification metrics, support/refute/lead stance, and missing data.
- Preserve scope caveats. A company-wide outlook can support `公司指引` with a caveat even if it is not a pure product-level guide; a product TAM can support `公司 TAM` without proving near-term revenue.
- Keep missing dimensions explicit. Do not hide a bucket simply because another bucket from the same source is strong.

## Mechanism Model Source Discipline

When the L3-L5 research unit belongs to a model-heavy industry or technology route, plan sources for a driver table, not just a prose answer. The source plan must name expected fields such as:

- period, unit, currency, geography, and scope.
- volume, price, mix, penetration, duration, and replacement cycle.
- capacity, utilization, inventory, lead time, qualification status, and capex.
- cost, gross margin, operating margin, FCF, working capital, and capital return.
- valuation multiple, market cap/EV, implied growth, implied margin, discount rate, or risk premium.
- formula, derived metric, and口径 caveat.

If these fields cannot be collected, the source plan should mark the conclusion as `unverified` or `lead_only` rather than allowing a narrative source to strengthen the thesis.

## Search Discipline

- Never collect sources just because they are easy to find.
- Every source must map to a question, hypothesis, or trigger.
- For every support source, plan at least one refuting or boundary-check source.
- A refreshed canonical QA tree must store `source_plan` as structured source objects, not as a prose sentence.
- In historical training/backtest mode, a declared visible date without availability proof is not enough for thesis use.
- Low-reliability messages can create leads but cannot strengthen conclusions by themselves.

## DeepSeek Handoff

When DeepSeek MCP is available, prepare a narrow prompt per source or per small source bundle:

- The exact L3-L5 research-unit question.
- Why the source is being read.
- The extraction schema and the dimension list to inspect.
- The source bucket.
- The expected support/refute/lead classification.
- The intended context policy and `max_tokens` budget: preserve complete source context when the DeepSeek MCP server/model supports it; normally use `max_tokens` 32000-64000 for long-source extraction, at least 24000 for multi-source L3 drafts, and at least 12000 for ordinary single-source parsing.

The planner should expect two persisted artifacts:

- `source_extractions.jsonl`: DeepSeek/source-parser output by source-to-research-unit pair.
- `leaf_source_reviews.jsonl`: GPT verification, corrections, adopted facts, and rejection decisions.

Do not plan one large DeepSeek job for a whole research report. Prefer one source, one L3-L5 research unit, and one compact schema.

GPT remains responsible for source selection, source reliability, conflict resolution, and final synthesis.
