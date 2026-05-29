# Value Invest Research

File-system-first equity research assistant. The canonical entry point is now one research-goal QA framework: user research goal -> execution plan -> three-layer QA drilldown -> evidence-linked synthesis -> specific target observation list. Plain files are the source of truth; Python code validates contracts, scaffolds research objects, ingests public data, and creates LLM research drafts.

## Module Index

| Module | Path | Purpose |
|------|------|------|
| Core package | `src/value_invest_research/` | CLI, schemas, scaffolding, ingestion, research-system generation, run logs, and LLM research workflows. |
| Tests | `tests/` | unittest coverage for schemas, CLI, scaffolding, ingestion, and research workflow prompt/output behavior. |
| Research skill | `skills/value_invest_research/` | Operating protocol, frameworks, prompts, and evidence checklists. |
| Config | `config/` | Watchlist, source priority, research object registry, and event playbooks. |
| Stock objects | `stocks/` | Stock memos, evidence logs, structured data, run logs, and proposals. |
| Research objects | `research/` | Sector/theme/event memos, evidence, candidate screens, and run logs. |

## Canonical Research Goal Framework

When the user proposes any new research goal, topic, company, sector, event, or concept, use only this framework. Do not mix in any other research template.

Framework changes are persistent by default:
- When the user changes a report structure, interaction pattern, section order, or presentation logic, treat that as a new default research-system requirement unless the user explicitly says it is one-off.
- In the same change, update `AGENTS.md`, `skills/value_invest_research/SKILL.md`, and `skills/value_invest_research/frameworks/research_goal_qa.md` so future reports follow the new structure.
- Existing generated reports may keep their historical content, but new or refreshed reports must use the latest framework requirement.

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
   - Details, scorecards, tables, and jump pages must live inside the QA layer whose question they answer. Do not put them as Q-parallel components or unrelated top-level appendices.
   - Bottleneck scorecards belong under the relevant bottleneck question, usually Q2.1.
   - Disconfirming-test lists belong under the relevant risk question, usually Q3.1.
   - Target tables belong under the relevant target-selection question, usually Q4.1.
   - Each layer rolls up only from its child answers.
   - Each L3 answer must separate fact, inference, judgment, gap, and trigger.
   - For every L3 question, GPT must decide which materials to search or read, define the extraction schema, and assign those concrete materials to DeepSeek MCP for careful reading.
   - DeepSeek should produce the first structured L3 reading answer from those materials: fact, inference, preliminary judgment, gap, trigger, source links, and support/refute/lead stance.
   - GPT must then verify DeepSeek's L3 answer against source links or local files, resolve conflicts, correct unsupported claims, and write the final L3 answer and parent rollup.

5. Information buckets
   - Classify every input as evidence, research_report, opinion, or message.
   - Mark each item as support, refute, or lead.
   - Attach source links for concrete information.

6. Specialty skill dispatch
   - Before assigning an L3 task, classify its task family and route it to the most relevant specialized skill when available.
   - Default task families:
     - Financial statement or filing parsing -> `financial-statement-analysis`.
     - Valuation, priced-in expectations, multiples, reverse DCF, margin of safety -> `valuation-analysis`.
     - Large source reading, long report/transcript extraction, first-pass L3 drafting -> `leaf-research-deepseek` plus DeepSeek MCP.
     - Quantitative strategy, factor, backtest, or systematic signal -> `quant-research-fks` or `quantitative-research`.
     - HTML/report presentation design -> `frontend-design`.
   - Every L3 answer must keep a skill dispatch trace: task family, selected skill, concrete materials, extraction schema, output status, fallback used if any, and GPT verification status.
   - When one leaf task spans multiple families, chain skills in the natural order. Example: financial-statement-analysis normalizes filings first, then valuation-analysis turns verified financial facts into priced-in expectations.
   - Specialized skills are assistants for leaf-level processing, not final judges. GPT remains responsible for research type selection, question design, source priority, verification, synthesis, target strength, and final user-facing conclusions.
   - If a needed specialized skill is unavailable, record the task family and use the closest auditable fallback: primary source parsing by GPT, DeepSeek source extraction, or a local deterministic script.

7. DeepSeek delegation
   - DeepSeek's primary research role is parsing concrete source materials: research reports, news/messages, earnings releases, annual reports, filings, transcripts, expert interviews, and other single-source documents.
   - Delegate a source to DeepSeek only after GPT has defined the research question, source priority, and extraction schema.
   - DeepSeek should return structured extraction: key facts, numbers, dates, source bucket, support/refute/lead stance, affected QA node, uncertainty, and follow-up data needs.
   - For L3 questions, DeepSeek is the default first-pass reader and answer drafter for the selected materials.
   - DeepSeek may also do source summarization, key-point extraction, initial classification, and candidate-question drafting.
   - DeepSeek must not produce final investment judgment, trading instruction, financial conclusion, architecture decision, or unrechecked target recommendation.
   - The main model must verify and synthesize all material conclusions against auditable sources.
   - GPT remains responsible for source selection, source reliability checks, cross-source conflict resolution, reasoning synthesis, target strength, final report language, and all user-facing conclusions.

8. Final target observation list
   - If the research has investment implications, map conclusions to specific securities or assets, not only broad directions.
   - For every target, include ticker/name, bottleneck or thesis node, reason, strength, required verification data, catalysts, risks, and source links.
   - This is a research observation list, not a buy/sell instruction.

9. HTML presentation
   - Use Apple-inspired visual style: white/light-gray surfaces, SF-system typography, restrained borders, clean spacing, and low-noise cards.
   - Page order should be: current research goal, research type adaptation and execution plan, QA drilldown sections, specialty skill trace when relevant, source index.
   - QA drilldown should show Q1-Q4 as the top-level sections, using the adapted Q meanings for the selected research type.
   - Visual artifacts are answer formats inside QA nodes, not standalone siblings: scorecards inside the bottleneck Q node, risk triggers inside the disconfirming-test Q node, and target tables inside the target-selection Q node.
   - Avoid appending a generic full report or workbench appendix unless explicitly requested.

## Commands

```powershell
python tools/run_tests.py
$env:PYTHONPATH = "src"; python -m value_invest_research --help
value-invest-research --help
value-invest-research build-evidence AAPL
value-invest-research build-research-system AAPL
value-invest-research build-research-graph AAPL
value-invest-research research-stock AAPL --api-key $env:LLM_API_KEY
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

Do not let DeepSeek:
- Decide the final thesis.
- Rank target strength.
- Produce buy/sell/hold instructions.
- Resolve conflicting sources without GPT review.
- Strengthen a conclusion from low-reliability information.
