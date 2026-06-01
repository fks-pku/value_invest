# Value Invest Research

File-system-first equity research assistant. The canonical entry point is now one research-goal QA framework: user research goal -> execution plan -> three-layer QA drilldown -> evidence-linked synthesis -> specific target observation list. Plain files are the source of truth; Python code validates contracts, scaffolds research objects, ingests public data, and creates LLM research drafts.

## Module Index

| Module | Path | Purpose |
|------|------|------|
| Core package | `src/value_invest_research/` | CLI, schemas, scaffolding, ingestion, research-system generation, run logs, and LLM research workflows. |
| Framework contracts | `src/value_invest_research/framework_contracts.py` | Executable validation and audit utilities for report hierarchy, time-sliced backtests, QA schema, scoring, frozen recommendations, labels, training samples, reviews, workbench traces, and domain playbooks. |
| Tests | `tests/` | unittest coverage for schemas, CLI, scaffolding, ingestion, and research workflow prompt/output behavior. |
| Research skill | `skills/value_invest_research/` | Operating protocol, frameworks, prompts, and evidence checklists. |
| Specialty skills | `skills/value_invest_research/specialty_skills/` | Project-tracked investment research leaf skills for question architecture, source planning, source parsing, valuation, and target observation. |
| Config | `config/` | Watchlist, source priority, research object registry, and event playbooks. |
| Stock objects | `stocks/` | Stock memos, evidence logs, structured data, run logs, and proposals. |
| Research objects | `research/` | Sector/theme/event memos, evidence, candidate screens, and run logs. |

## Canonical Research Goal Framework

When the user proposes any new research goal, topic, company, sector, event, or concept, use only this framework. Do not mix in any other research template.

The final report presentation contract is `skills/value_invest_research/frameworks/research_report_contract.md`. Treat it as the default for all future research reports unless the user explicitly asks to iterate on the framework.

The current report contract is locked:
- Top-level order is exactly `当前研究目标` -> `产业链全景` -> `问题下钻` -> `最终标的推荐` -> `来源索引`.
- `产业链全景` is a mandatory top-level analytical map. It must show upstream, midstream, downstream, key players, products/services, dependencies, value/profit flow, and candidate chokepoints before the QA tree begins. It must also include a beginner-readable Chinese explanation generated with the `supply-chain-panorama-explainer` lens: one plain summary, step-by-step flow, layer cards, bottleneck explanation, and target/Q2/Q4 links.
- `问题下钻` preserves the full adapted Q1-Q4 QA tree and must render L3 leaf questions in complete refreshed reports unless the user explicitly asks for a shorter executive version.
- Q4 remains the auditable as-of target-selection QA node with child questions.
- `最终标的推荐` is a standalone presentation rollup, not a replacement for Q4.
- The hierarchy and format rules in `research_report_contract.md` are validation requirements, not style suggestions. A complete refreshed report is invalid if it drops L3, moves Q4 out of `问题下钻`, duplicates child-question lists beside inline cards, replaces the canonical component family, or adds public process appendices.
- Four non-drift locks must always hold: hierarchy and format lock, supply-chain map lock, backtest time-slice lock, and frontend card-style lock. In backtest mode, only cutoff-visible information can drive source collection, QA reasoning, scoring, odds, and target ranking; the only current-time data allowed in final HTML is the final-target evaluation label.
- Public no-changelog lock: final HTML must never include change-log, upgrade-log, "本轮/本次升级", "本轮/本次更新", "本轮如何落实", mechanism-depth checklist, framework explanation, execution trace, tool trace, or workbench/process commentary unless the user explicitly asks to inspect process. Framework upgrades must affect the questions, evidence, scoring, and target reasoning invisibly; they are not report content.
- Frontend interaction is part of the locked contract, not optional polish. Every `qa-card level-1/2/3` must render as a clickable `<details class="qa-card ...">` node with a `<summary>`, `qa-count`, and `chevron`, opened by default so users can collapse or expand the QA tree without losing the canonical hierarchy.
- In historical training/backtest mode, public prose must read as if written on the `as_of_date`; later price movement appears only once in the isolated final target evaluation fields.
- Do not add process appendices, execution traces, tool traces, iteration notes, or workbench sections unless explicitly requested.
- Additive-iteration lock: framework iteration is additive by default. When adding a new section, field, dimension, skill, source schema, or visual affordance, preserve all existing public section order, canonical component classes, QA expand/collapse behavior, action-state color classes, target-table structure, source-collapse behavior, and no-changelog rules unless the user explicitly asks for a frontend/report redesign.
- Before marking a framework iteration complete, run regression checks on a newly generated/refreshed report and at least one existing canonical report or fixture: `validate-report-contract`, `validate-research-artifacts` when artifacts exist, and a DOM/browser smoke check for QA card collapse plus `state-actionable_long`/`state-watch_only`/`state-no_action` color classes when those states appear.

Framework changes are persistent by default:
- When the user changes a report structure, interaction pattern, section order, or presentation logic, treat that as a new default research-system requirement unless the user explicitly says it is one-off.
- In the same change, update `AGENTS.md`, `skills/value_invest_research/SKILL.md`, and `skills/value_invest_research/frameworks/research_goal_qa.md` so future reports follow the new structure.
- If the change affects final report hierarchy or presentation, also update `skills/value_invest_research/frameworks/research_report_contract.md`.
- Existing generated reports may keep their historical content, but new or refreshed reports must use the latest framework requirement.
- Final user-facing HTML reports must stay clean and research-first. They must use this top-level order: `当前研究目标`, `产业链全景`, `问题下钻`, `最终标的推荐`, `来源索引`.
- `产业链全景` should use `supply-chain-section` plus `chain-explain`, `chain-plain-summary`, `chain-flow-steps`, `chain-layer-grid`, `chain-layer-card`, `chain-chokepoints`, `chain-target-links`, and `chain-map` or `chain-table`. It is not optional background text: Q2 value-capture analysis and Q4 target ranking must be able to point back to the chain map, while a new reader can understand who does what, who pays whom, where money is made, and where bottlenecks sit.
- `最终标的推荐` is a synthesis section, not a process appendix. It should roll up all QA evidence into a ranked observation list with specific targets, win probability, payoff odds, rationale, and downgrade triggers.
- Do not put iteration notes, "what changed in this run", quality-framework explanations, execution traces, tool attribution, DeepSeek usage notes, or workbench appendices into the final HTML. Store process metadata in workbench JSON, logs, or internal artifacts instead.
- Do not describe framework changes inside the report. Phrases such as "本轮升级", "本次更新", "本轮新增", "机制深度映射", "本轮如何落实", or English equivalents such as "what changed in this run" are contract drift in final HTML. Put those notes only in internal artifacts or user-facing chat replies.
- Do not simplify away QA depth when refreshing a report. Preserve the full available QA tree unless the user explicitly asks for a shorter executive version.
- Do not overload L3 with unrelated questions under a single L2. L2 should group L3 leaves into meaningful mechanism buckets selected by the research-type adapter and domain playbook.
- The public report contract defines hierarchy and presentation only. Domain-specific questions, metrics, parsing schemas, tracking indicators, and threshold rules belong in research-type adapters or domain playbooks, not in the shared presentation contract.
- For industry/theme opportunity and technology/product-route research, the domain playbook must include an explicit chokepoint evaluation when value capture depends on supply, workflow, data, distribution, trust, or regulatory bottlenecks. The scorecard belongs inside the relevant Q2 bottleneck node, and the final target ranking must use this chokepoint score alongside future space, valuation odds, evidence quality, and disconfirming-risk control.
- Chokepoint evaluation must be formula-based, not only narrative. Store a reusable score schema with dimension weights, scoring definitions, and downgrade rules. Final reports should show the score breakdown or score drivers so rankings are comparable across targets and future reports.
- Scarcity-first opportunity gate: the default action state is `no_action`, not long recommendation. The goal is to find a currently underpriced large opportunity. A target becomes `actionable_long` only when the as-of evidence supports all four core target dimensions: `scarcity_or_monopoly` (scarce/monopolistic product, service, or chokepoint), `mispricing` (growth not fully priced), `earnings_elasticity` (large future revenue/margin/FCF or rerating upside), and `risk_control` (small enough, monitorable downside). If any core dimension fails, cap the score and mark the target `watch_only` or `no_action`.
- Do not let broad theme exposure create high scores. Future-space data is useful only after it reaches a scarce, monetizable chokepoint. The highest research effort should go into proving or disproving irreplaceability, substitution barriers, pricing power, and whether the market has already priced the opportunity.
- Mechanism-depth protocol: for industry/theme opportunity and technology/product-route research, the domain playbook must force a driver-tree model before evidence collection. The minimum depth map covers demand driver tree, supply or access response, unit economics and profit bridge, competitive value-capture map, market-pricing bridge, disconfirming/counter-supply tests, capital-chain or second-order beneficiaries, and model/口径 reconciliation. A refreshed canonical report is too shallow if it only states TAM/theme exposure without modeling how demand becomes company revenue, margin, FCF, and valuation rerating.
- Domain-specific depth requirements live in `skills/value_invest_research/frameworks/domain_playbooks.md`. Use it when selecting or synthesizing a playbook; for storage/memory research, use the memory industry playbook so L2/L3 questions cover workload-to-memory demand, demand-supply slope mismatch, product price/unit economics, company value capture, capex cycle, market-pricing rerating, counter-supply/substitution, and model口径 reconciliation.

## Time-Sliced Prediction Evaluation

The research system must support two explicit run modes:

- Historical training/backtest mode: use an `as_of_date`, defaulting to three calendar months before the evaluation date when the user asks to train, audit, or evaluate prediction ability. Source collection, source parsing, QA answers, valuation context, and target ranking may only use information that was publicly visible on or before `as_of_date`. Later materials are look-ahead data and must not enter the thesis, score, odds model, or target rank.
- Live prediction mode: use information visible up to the report date. Do not attach a future return label. Instead, set a validation horizon, required evidence, and next review trigger, normally report date plus three months unless the user specifies another horizon.

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

## Research Quality Pipeline

The framework optimizes research quality before report polish. Run these passes in order:

1. Question architecture
   - Use `investment-question-architect` to classify the research type and design the Q1-Q4 tree.
   - Before building Q1-Q4, build the supply-chain map using `supply-chain-panorama-explainer`. The map must cover upstream, midstream, downstream, products/services, key listed and private players, dependency links, value/profit flow, and candidate chokepoints. It must be written in beginner-readable Chinese and answer: who provides what, who depends on whom, who pays whom, where profit/cash flow sits, which links are scarce, and which targets map to each scarce node. Do not begin target ranking from company names before this map exists.
   - Question quality is the primary depth control. Each L3 question must state decision use, required materials, support evidence, refuting evidence, target implications, and preferred specialty skill.
   - For industry/theme and technology-route research, first build a mechanism-depth map. L2 buckets must represent real analytical mechanisms such as demand drivers, supply response, unit economics, value capture, pricing/valuation, counter-supply, and second-order beneficiaries, not generic summary headings.
   - Each L3 question is a decision unit, not a prose subsection. Its structured record must include `decision_use`, `materiality`, `support_evidence`, `refute_evidence`, `target_implications`, `score_component`, `minimum_evidence_gate`, and `refuting_source_plan`.
   - `score_component` must explicitly connect the L3 question to one or more ranking drivers such as `future_space`, `chokepoint_strength`, `valuation_odds`, `evidence_quality`, `disconfirming_risk_control`, `monitorability`, `payoff_convexity`, `target_ranking`, or `action_state`.
   - Do not start evidence collection from a generic outline. Start from investment-relevant questions that can change parent conclusions or target strength.

2. Source planning
   - Use `research-source-planner` before reading materials.
   - For every L3 question, define the concrete source plan: primary evidence, company voice, research reports/data, messages/news, and opinions.
   - For model-heavy industries, source plans must specify the tables or fields needed to rebuild the mechanism model: period, unit, currency, volume, price, mix, capacity, utilization, cost, margin, capex, FCF, valuation multiple, implied expectation, and口径. Generic article summaries are not sufficient when the decision depends on a quantitative driver tree.
   - `source_plan` must be structured by concrete source, expected fields, source bucket, visible date/cutoff status, allowed usage, and preferred parser skill. A bare sentence is not sufficient for refreshed canonical reports.
   - Every support source plan needs a refuting or boundary-check source plan.
   - In historical training/backtest mode, every source plan must include `as_of_date`, `source_visible_at`, cutoff status, and auditable `availability_proof` such as publisher date, filing timestamp, archive timestamp, exchange release page, or dataset snapshot note. Reject or quarantine materials whose visible date is after `as_of_date`, except for the separate price-label dataset used only after recommendations are frozen.

3. Specialty parsing
   - Route concrete materials through the relevant leaf skill:
     - `financial-statement-analysis` for filings, results, segment data, capex, inventory, backlog/RPO, and cash quality.
     - `valuation-analysis` for future space, priced-in expectations, multiples, reverse DCF, FCF yield, peer comparison, and odds.
     - `industry-report-analysis` for sell-side reports, industry reports, TAM, supply-demand, price forecasts, and third-party datasets.
     - `news-event-analysis` for news, public messages, policy updates, supply-chain reports, and unverified leads.
     - `opinion-analysis` for expert, investor, interview, conference-note, or social-media viewpoints.
     - `leaf-research-deepseek` when DeepSeek MCP reads selected concrete materials and drafts the first L3 extraction.
   - For each selected concrete material, create or append one source-parser record in `source_extractions.jsonl`. This reading layer should normally be produced by DeepSeek MCP for long reports, filings, transcripts, research reports, and multi-paragraph source excerpts.
   - Each source-parser record must fill `schema_fields` according to the L3 `skill_dispatch.extraction_schema`. A parser output that only gives generic summary text cannot strengthen a refreshed canonical L3 answer until GPT verifies and maps it into the required schema fields.
   - Third-party reports and spreadsheets must be parsed as assumption models, not accepted as conclusions. Extract formulas, driver rows, period/unit/currency, methodology, disagreement points, and口径 caveats before using any headline TAM, CAGR, margin, target price, or upside number.
   - Then create or append a matching GPT verification record in `leaf_source_reviews.jsonl`, recording adopted facts, corrected fields, rejected claims, uncertainty, and whether the extraction is allowed to strengthen the final QA answer.
   - L3 `skill_dispatch` must carry the created `source_extraction_ids` and `leaf_source_review_ids` so the final answer can be traced from question to parser output to GPT verification.
   - Do not skip these extraction/review files merely because GPT can read the material directly. GPT may parse directly only for very short materials, failed DeepSeek calls, missing tool access, or high-risk verification; the fallback and reason must be recorded.

4. GPT verification and synthesis
   - GPT verifies parsed facts, resolves source conflicts, separates fact/inference/judgment, and writes final L3 answers.
   - Parent conclusions may only roll up from verified child answers.

5. Target recommendation analysis
   - Use `target-recommendation-analysis` for Q4 when the research has investment implications.
   - Targets must be specific securities or assets, with chokepoint exposure, future space, valuation odds, strength, catalysts, downgrade triggers, required data, and source links.
   - Observation strength must reflect chokepoint evaluation. Do not rank a target above stronger alternatives solely because its narrative is attractive; it must score on bottleneck criticality, scarcity or substitution barrier, pricing power, financial exposure, evidence quality, valuation odds, and monitorability.
   - Each of the seven component scores must preserve auditable `score_subcomponents` with subdimension name, score, weight, evidence IDs or GPT review IDs, rationale, and status. Direct unexplained component scores are fallback-only and should not be used for refreshed canonical reports.
   - Roll the seven component scores into four core target dimensions: `scarcity_or_monopoly`, `mispricing`, `earnings_elasticity`, and `risk_control`. These four dimensions are the primary public score display and action-state gate.
   - Apply the scarcity-first opportunity gate before ranking. `no_action` is the default. `actionable_long` requires scarce/monopolistic value capture, market mispricing, large earnings elasticity, and controlled risk. Missing valuation, weak scarcity, only generic theme exposure, non-positive expected excess return, weak evidence, low payoff elasticity, or uncontrolled disconfirming risk must cap strength even if the industry narrative is attractive.
   - Final target ranking must be deterministic from the frozen score object: action-state priority, opportunity fit, total score, payoff convexity, thesis confidence, then stable ticker/name tie-break. Do not manually move targets after labels are attached or because later outcomes are known.
   - Any `actionable_long` target must carry hard `thesis_kill_tests` with test, evidence needed, downgrade action, and source plan. If a target lacks such tests, cap it at `watch_only`.
   - Final target tables must include a compact score breakdown and a simple odds model. The odds model should state the implied expectation, base/bull/bear verification path, and the data that would upgrade or downgrade the observation. If valuation data is stale or incomplete, mark odds as unverified rather than strengthening the target.
   - Keep a prediction review field for every target or major thesis node: initial claim, validation horizon, required evidence, current status, and review trigger. This can live in the workbench and be summarized in the relevant Q3/Q4 node.
   - In historical training/backtest mode, freeze the Q4 target list and ranking before attaching the forward three-month return label. The label may be shown for evaluation, calibration, and later model improvement, but it must not alter the frozen recommendation.
   - This is a research observation list, not a buy/sell/hold instruction.

6. Executable contract validation and learning artifacts
   - Use `framework_contracts.py` to validate final report hierarchy/card structure, validate QA tree schema, validate source-extraction schema fields, audit time-sliced sources and `availability_proof`, score targets with separated thesis confidence/payoff convexity plus auditable subcomponents, rank targets deterministically, validate target kill tests, freeze recommendations before labels, attach forward-return labels, build training samples, build prediction reviews, and keep internal workbench traces out of final HTML.
   - Run `value-invest-research validate-report-contract <professional_report.html> --mode historical_backtest --require-l3` after refreshed canonical reports.
   - Run `value-invest-research audit-time-slice <sources.jsonl> --as-of-date YYYY-MM-DD` before using historical-mode sources for QA, scoring, odds, or ranking.

1. Current research goal
   - Define the object, time frame, investment relevance, and decision boundary.
   - Output one constrained current judgment and the biggest uncertainty.

2. Research type adaptation layer
   - Before building Q1-Q4, classify the research type: industry/theme opportunity, single company, event/policy, technology/product route, target update, or other user-defined type.
   - Keep the QA skeleton, but adapt the meaning of Q1-Q4 to the research type. Do not force every topic into demand/bottleneck/target wording.
   - Default mappings:
     - Industry/theme opportunity: Q1 demand reality, Q2 value-capture bottlenecks, Q3 disconfirming tests and priced-in risk, Q4 target observation list.
     - Single company: Q1 growth drivers, Q2 moat/unit economics/value capture, Q3 financial quality/valuation/disconfirming tests, Q4 observation decision and monitoring list.
     - Event/policy: Q1 event facts and scope, Q2 transmission mechanism, Q3 beneficiaries/losers and second-order effects, Q4 disconfirming tests and watchlist.
     - Technology/product route: Q1 technical feasibility and adoption demand, Q2 bottlenecks and ecosystem readiness, Q3 commercialization/competition/disconfirming tests, Q4 exposed assets and monitoring list.
   - If the type does not fit a default mapping, define a custom Q1-Q4 map in the execution plan before collecting evidence.

3. Research execution plan
   - Present the execution plan before research output.
   - Use QA directions as the primary structure, not step components. For industry/theme opportunity, default to Q1 confirm demand, Q2 locate bottlenecks, Q3 bind disconfirming tests, Q4 target observation list with reasons. For other research types, use the adapted Q1-Q4 map defined above.
   - For each Q direction, state what questions to ask, how to collect information, how to connect the information into reasoning, and how to present it.

4. QA drilldown
   - Research must proceed through the QA tree directly.
   - Use at most three layers inside each Q direction: Q1, Q1.1, Q1.1.1.
   - Every QA layer must present information in this order: current conclusion, question expansion/child QA, then remaining questions or data gaps.
   - Details, scorecards, tables, and jump pages must live inside the QA layer whose question they answer. Do not put them as Q-parallel components or unrelated top-level appendices.
   - Bottleneck scorecards belong under the relevant bottleneck question, usually Q2.1.
   - Chokepoint scorecards must answer seven questions: demand flow, irreplaceability, supply or access constraint, pricing power, financial conversion, market pricing, and disconfirming trigger.
   - Chokepoint scorecards must use a declared schema with dimension weights. If a dimension cannot be evidenced, score it conservatively and list the missing data.
   - Q4 target ranking must explicitly reference the Q2 chokepoint score or its drivers; target strength is not valid unless it reconciles chokepoint strength with future space, valuation odds, and the Q3 downgrade tests.
   - Disconfirming-test lists belong under the relevant risk question, usually Q3.1.
- Target tables belong under the relevant target-selection question, usually Q4.1.
- In historical training/backtest mode, Q4 must still retain as-of target-selection child questions. Do not replace Q4's child QA with the final label table, and do not create a Q4 child whose purpose is to evaluate later returns.
- Each layer rolls up only from its child answers.
   - Each L3 answer must separate fact, inference, judgment, gap, and trigger. Fact must be sourced observations or extracted source summaries; inference must explain how those facts answer the leaf question; judgment must state the decision impact. These fields must not repeat the same sentence.
   - Each L3 answer must directly answer the leaf question, not merely list adjacent facts. If the question asks for a mapping, bridge, ranking, comparison, formula, scenario, or risk test, the L3 current-conclusion block must include the corresponding structured answer artifact inside the QA card: e.g. mapping table, driver table, bridge table, score table, scenario table, or kill-test table. Source lists alone are insufficient.
   - For every L3 question, GPT must decide which materials to search or read, define the extraction schema, and assign those concrete materials to DeepSeek MCP for careful reading.
   - DeepSeek should produce the first structured L3 reading answer from those materials: fact, inference, preliminary judgment, gap, trigger, source links, and support/refute/lead stance.
   - GPT must then verify DeepSeek's L3 answer against source links or local files, resolve conflicts, correct unsupported claims, and write the final L3 answer and parent rollup.
   - Every L3 question must include a materiality statement: why the answer changes the parent conclusion, target strength, valuation odds, or risk controls.
   - Every L3 question must include a source plan before materials are read.
   - A complete L3 record is invalid if it lacks `decision_use`, `support_evidence`, `refute_evidence`, `target_implications`, `score_component`, `minimum_evidence_gate`, `refuting_source_plan`, structured `source_plan`, structured `skill_dispatch`, or differentiated `fact`/`inference`/`judgment`.

5. Information buckets
   - Classify every input as evidence, research_report, opinion, or message.
   - Mark each item as support, refute, or lead.
   - Attach source links for concrete information.

6. Specialty skill dispatch
   - Before assigning an L3 task, classify its task family and route it to the most relevant specialized skill when available.
   - Project-tracked definitions for these skills live under `skills/value_invest_research/specialty_skills/`; local `.agents/skills/` copies may exist for agent discovery but are not the source of truth.
   - Default task families:
     - Question tree design -> `investment-question-architect`.
     - Supply-chain panorama explanation -> `supply-chain-panorama-explainer`.
     - L3 source planning -> `research-source-planner`.
     - Financial statement or filing parsing -> `financial-statement-analysis`.
     - Valuation, priced-in expectations, multiples, reverse DCF, margin of safety -> `valuation-analysis`.
     - Industry report, market dataset, TAM, supply-demand, price, or competitive-map parsing -> `industry-report-analysis`.
     - News, public message, policy update, supply-chain report, or rumor-like lead parsing -> `news-event-analysis`.
     - Expert, investor, interview, or social-media viewpoint parsing -> `opinion-analysis`.
     - Large source reading, long report/transcript extraction, first-pass L3 drafting -> `leaf-research-deepseek` plus DeepSeek MCP.
     - Specific target observation list and strength scoring -> `target-recommendation-analysis`.
     - Quantitative strategy, factor, backtest, or systematic signal -> `quant-research-fks` or `quantitative-research`.
     - HTML/report presentation design -> `frontend-design`.
   - Every L3 answer must keep `skill_dispatch` as a structured object with `task_family`, `selected_skill`, `concrete_materials`, `extraction_schema`, `source_extraction_ids`, `leaf_source_review_ids`, `skill_output_status`, `fallback_used`, and `gpt_verification_status`. A bare skill name or prose chain is contract drift.
   - When one leaf task spans multiple families, chain skills in the natural order. Example: financial-statement-analysis normalizes filings first, then valuation-analysis turns verified financial facts into priced-in expectations.
   - Specialized skills are assistants for leaf-level processing, not final judges. GPT remains responsible for research type selection, question design, source priority, verification, synthesis, target strength, and final user-facing conclusions.
   - If a needed specialized skill is unavailable, record the task family and use the closest auditable fallback: primary source parsing by GPT, DeepSeek source extraction, or a local deterministic script.

7. DeepSeek delegation
   - DeepSeek's primary research role is parsing concrete source materials: research reports, news/messages, earnings releases, annual reports, filings, transcripts, expert interviews, and other single-source documents.
   - Delegate a source to DeepSeek only after GPT has defined the research question, source priority, and extraction schema.
   - DeepSeek should return structured extraction: key facts, numbers, dates, source bucket, support/refute/lead stance, affected QA node, uncertainty, and follow-up data needs.
   - Persist DeepSeek source-parser outputs in `source_extractions.jsonl`; persist GPT verification in `leaf_source_reviews.jsonl`.
   - For formal investment source parsing, assume DeepSeek can use a very large input context when the MCP server/model supports it. Do not prematurely split a long filing, transcript, report, or source pack only because it is longer than GPT's comfortable reading window; keep the full source context together when source integrity matters, up to the server-supported context limit.
   - `max_tokens` is the output budget, not the input context window. Set a large DeepSeek `max_tokens` budget by default: normally 32000-64000 tokens for long-source extraction, at least 24000 tokens for multi-source L3 drafts, and at least 12000 tokens for ordinary single-source parsing unless the task is intentionally tiny.
   - Prefer narrow DeepSeek jobs by question and schema, but allow large source context inside that narrow job: one complete source or coherent source bundle, one L3 question, one extraction schema. Even with a large token budget, require compact JSON/table output with explicit limits unless the extraction truly needs exhaustive coverage.
   - If a DeepSeek response is truncated, malformed, empty, or stops mid-field, mark that delegation as `incomplete`, do not use it for conclusions, and either retry with a smaller chunk or fall back to GPT-verified source parsing.
   - For L3 questions, DeepSeek is the default first-pass reader and answer drafter for the selected materials.
   - DeepSeek may also do source summarization, key-point extraction, initial classification, and candidate-question drafting.
   - DeepSeek must not produce final investment judgment, trading instruction, financial conclusion, architecture decision, or unrechecked target recommendation.
   - The main model must verify and synthesize all material conclusions against auditable sources.
   - GPT remains responsible for source selection, source reliability checks, cross-source conflict resolution, reasoning synthesis, target strength, final report language, and all user-facing conclusions.

8. Final target observation list
   - If the research has investment implications, map conclusions to specific securities or assets, not only broad directions.
   - Do not restrict the target universe to securities with convenient Nasdaq/Yahoo/US labels. Include economically central non-US listings, ADRs, local shares, or other investable assets when they are the actual value-capture vehicles; use unverified label status if price labeling is not yet collected.
   - For every target, include ticker/name, chokepoint or thesis node, chokepoint score or score drivers, reason, strength, required verification data, catalysts, risks, and source links.
   - Include score breakdown, simplified odds model, and review trigger for each target when the report has enough data. These are required for refreshed reports unless the user asks for a shorter executive view.
   - In historical training/backtest mode, also include the as-of cutoff, label window, forward three-month return, benchmark/sector return and excess return when available, price source, and label status. Keep these fields visually separate from the as-of recommendation rationale.
   - This is a research observation list, not a buy/sell instruction.

9. HTML presentation
   - Use Apple-inspired visual style: white/light-gray surfaces, SF-system typography, restrained borders, clean spacing, and low-noise cards.
   - Final user-facing page order must be exactly: current research goal, supply-chain panorama, question drilldown, final target recommendation, source index.
   - In historical training/backtest mode, show the `as_of_date` and information cutoff in `当前研究目标`, but keep evaluation dates, label windows, benchmark returns, and later price movement out of all QA conclusions and rationale. Show later price movement only once inside `最终标的推荐`, as an isolated label block or rightmost label columns. Do not add a new top-level backtest appendix unless the user explicitly asks for it.
   - The final target recommendation section should be a synthesized ranking of specific securities or assets, emphasizing both win probability and payoff odds. It should not replace the Q4 QA node; Q4 remains the auditable source of target logic.
- Research type adaptation, execution plans, specialty skill traces, tool/delegation traces, iteration changes, and quality-process notes are internal metadata. Keep them out of the final HTML unless the user explicitly asks to inspect process.
- QA drilldown should show Q1-Q4 as the top-level sections, using the adapted Q meanings for the selected research type.
- Q4 remains the auditable as-of target-selection QA node with child questions. The standalone `最终标的推荐` section is a presentation rollup and must not erase or replace Q4's child-question hierarchy.
- Every visible L3 card must show a compact professional-routing strip inside `当前结论呈现`: selected `Skill`, actual `Execution` status, `Score Component`, and `Decision Use`. This is not a process appendix; it is the user's audit handle for whether the leaf question was routed through the proper professional lens and whether that route actually ran. `Skill` is the intended specialty lens; `Execution` must reflect `skill_output_status` and `fallback_used`, not merely the selected skill name. Detailed parser traces remain internal unless explicitly requested.
   - Inside every QA card/details node, use a consistent three-part display: `1. 当前结论呈现`, `2. 问题展开（子 QA）`, `3. 待补充的问题`.
   - If child QA nodes are rendered inline as expandable cards, do not also render a separate child-question list with the same titles. The question expansion section should contain either jump links or inline child cards, not both.
   - Parent-level answer artifacts such as `回答呈现`, scorecards,反证清单, target tables, and summary matrices belong under `当前结论呈现`, before child QA expansion.
   - Do not duplicate the same conclusion, child-QA list, or pending-question text in both a generated summary card and the body; use one sequential presentation.
   - Keep source indexes collapsed by default unless the user explicitly asks to inspect sources.
   - Refreshed canonical reports must reuse the shared frontend component family from `skills/value_invest_research/frameworks/research_report_contract.md`: `supply-chain-section` with `chain-explain`, `chain-plain-summary`, `chain-flow-steps`, `chain-layer-grid`, `chain-layer-card`, `chain-chokepoints`, `chain-target-links`, and `chain-map` or `chain-table`; `qa-card`; `artifact-card`; `target-section` + `target-table`; and one collapsed `source-collapse`. Do not introduce alternate component families unless the user explicitly asks for a frontend redesign.
   - `qa-card` is not a static wrapper. Render every QA card as interactive `details.qa-card` with `summary`, `qa-count`, and `chevron`, default `open`; a static `article/div.qa-card` is contract drift.
   - `target-table` action-state cells must keep canonical color classes: `state-actionable_long`, `state-watch_only`, or `state-no_action`. Showing plain `action_state` text without the status class is frontend contract drift.
   - Visual artifacts are answer formats inside QA nodes, not standalone siblings: scorecards inside the bottleneck Q node, risk triggers inside the disconfirming-test Q node, and target tables inside the target-selection Q node.
   - Avoid appending a generic full report or workbench appendix unless explicitly requested.
   - Preserve complete QA coverage in the final report; do not replace the QA tree with a compressed Q1-Q4 summary unless the user requests a brief version.

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
- `source_extractions.jsonl`: one DeepSeek/source-parser record per source-L3 pair. Required fields: `extraction_id`, `l3_question_id`, `source_id`, `source_title`, `source_bucket`, `parser`, `parser_status`, `schema_fields`, `key_facts`, `inference`, `support_refute_or_lead`, `uncertainties`, `follow_up_data`, and `created_at`. `schema_fields` must map every field requested by the L3 `skill_dispatch.extraction_schema` to value, evidence IDs or review IDs, and status.
- `leaf_source_reviews.jsonl`: one GPT verification record per extraction. Required fields: `review_id`, `extraction_id`, `l3_question_id`, `source_id`, `gpt_verification_status`, `adopted_facts`, `corrections`, `rejected_claims`, `final_bucket`, `final_support_refute_or_lead`, and `allowed_to_strengthen_conclusion`.
- Final HTML reports must not render these process artifacts unless the user explicitly asks to inspect parsing traces.

Do not let DeepSeek:
- Decide the final thesis.
- Rank target strength.
- Produce buy/sell/hold instructions.
- Resolve conflicting sources without GPT review.
- Strengthen a conclusion from low-reliability information.
