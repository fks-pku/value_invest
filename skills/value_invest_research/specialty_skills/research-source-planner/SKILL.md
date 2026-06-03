---
name: research-source-planner
description: Use this skill after an investment QA tree exists and before reading materials. It creates a source-search plan for each L3-L5 research unit: which primary filings, earnings calls, industry reports, datasets, news, and opinions to collect, why each source matters, and which specialty parser should read it.
---

# Research Source Planner

This skill converts L3-L5 research units into concrete source plans. It is responsible for collecting the right information, not for final synthesis.

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
- The extraction schema.
- The source bucket.
- The expected support/refute/lead classification.
- The intended context policy and `max_tokens` budget: preserve complete source context when the DeepSeek MCP server/model supports it; normally use `max_tokens` 32000-64000 for long-source extraction, at least 24000 for multi-source L3 drafts, and at least 12000 for ordinary single-source parsing.

The planner should expect two persisted artifacts:

- `source_extractions.jsonl`: DeepSeek/source-parser output by source-to-research-unit pair.
- `leaf_source_reviews.jsonl`: GPT verification, corrections, adopted facts, and rejection decisions.

Do not plan one large DeepSeek job for a whole research report. Prefer one source, one L3-L5 research unit, and one compact schema.

GPT remains responsible for source selection, source reliability, conflict resolution, and final synthesis.
