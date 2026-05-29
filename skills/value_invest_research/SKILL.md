---
name: value-invest-research
description: Use for investment research workflows that start from a user research goal and produce an auditable QA drilldown, evidence-linked synthesis, and specific target observation list. This skill has one canonical research-goal QA framework.
---

# Value Invest Research Skill

This Skill turns heterogeneous market information into auditable research artifacts. The default sequence is a single research-goal QA framework with a research-type adapter and specialty skill dispatch:

1. Current research goal.
2. Research type adaptation layer.
3. Question architecture pass.
4. Source planning pass.
5. Specialty parsing for L3 leaf tasks.
6. GPT verification and evidence-linked synthesis.
7. Specific target observation list.
8. HTML QA presentation.

## Non-Negotiable Rules

- Do not issue final trading instructions.
- Separate facts, inferences, and judgments.
- Cite evidence IDs for every material claim.
- Treat low-reliability sources as research leads only.
- Search for disconfirming evidence before strengthening a thesis.
- Preserve prior thesis history when updating a memo.
- Mark uncertainty directly instead of hiding it.
- Use the canonical research-goal QA framework by default for every new research goal, topic, company, sector, event, or concept.
- Do not combine multiple templates.
- Before building Q1-Q4, classify the research type and adapt the meaning of Q1-Q4. Do not force every topic into demand/bottleneck/target wording.
- Default research types are industry/theme opportunity, single company, event/policy, technology/product route, target update, and custom user-defined type.
- Use `investment-question-architect` before evidence collection. Question quality controls research depth; every L3 question must state decision use, required materials, support evidence, refuting evidence, target implications, and preferred specialty skill.
- Use `research-source-planner` before reading materials. Every L3 question needs a concrete source plan and at least one refuting or boundary-check source plan.
- When the user changes a report structure, interaction pattern, section order, or presentation logic, treat that change as a persistent default research-system requirement unless the user explicitly says it is one-off.
- In the same change, update `AGENTS.md`, this `SKILL.md`, and `frameworks/research_goal_qa.md` so future reports follow the new structure.
- Research output must be organized by QA directions, not standalone step components. For industry/theme opportunity, default to Q1 confirm demand, Q2 locate bottlenecks, Q3 bind disconfirming tests, Q4 target observation list with reasons. For other research types, first define the adapted Q1-Q4 map in the execution plan.
- For industry/theme opportunity and technology/product-route research, Q2 must include an explicit chokepoint evaluation when value capture depends on scarce supply, workflow control, proprietary data, distribution, trust, or regulation. The scorecard must stay inside the relevant Q2 node and must evaluate demand flow, irreplaceability, supply/access constraint, pricing power, financial conversion, market pricing, and disconfirming trigger.
- Chokepoint evaluation must use a declared score schema with dimension weights, scoring definitions, and downgrade rules. If a dimension lacks evidence, score it conservatively and list the missing data.
- Every level must state what questions to ask, how to collect information, how to connect information into reasoning, and how to present the output.
- Every QA layer must present information in this order: current conclusion, question expansion/child QA, then remaining questions or data gaps.
- Use at most three QA layers by default: Q1, Q1.1, Q1.1.1.
- Details, scorecards, tables, and jump pages must be nested under the QA layer whose question they answer, not placed as Q-parallel components or unrelated top-level appendices.
- Bottleneck scorecards belong under the relevant bottleneck question, usually Q2.1.
- Final target recommendation must use the Q2 chokepoint evaluation. Target strength is invalid unless it reconciles chokepoint score or score drivers with future space, valuation odds, evidence quality, and Q3 downgrade triggers.
- Final target recommendation must include a compact score breakdown and simplified odds model. The score breakdown should show chokepoint strength, future space, valuation odds, evidence quality, disconfirming-risk control, and monitorability. The odds model should state what the current valuation appears to require, the base/bull/bear verification path, and what data would upgrade or downgrade the observation.
- Disconfirming-test lists belong under the relevant risk question, usually Q3.1.
- Target tables belong under the relevant target-selection question, usually Q4.1.
- Each layer may only roll up conclusions from its child answers and auditable sources.
- L3 answers must separate fact, inference, judgment, gap, and trigger.
- L3 answers must include materiality: why the answer changes the parent conclusion, target strength, valuation odds, or risk controls.
- For every L3 question, GPT must decide which materials to search or read, define the extraction schema, and assign those concrete materials to DeepSeek MCP for careful reading.
- Before assigning an L3 question, classify its task family and use the most relevant specialized skill when available: `financial-statement-analysis` for filings/financial statements, `valuation-analysis` for valuation/priced-in expectations, `industry-report-analysis` for third-party reports/datasets, `news-event-analysis` for messages/news/policy leads, `opinion-analysis` for expert or investor viewpoints, `leaf-research-deepseek` for long source parsing, `target-recommendation-analysis` for Q4 target observation lists, `quant-research-fks` or `quantitative-research` for systematic strategy questions, and `frontend-design` for HTML/report interface work.
- Every L3 answer must include a skill dispatch trace: task family, selected skill, concrete materials, extraction schema, output status, fallback used if any, and GPT verification status.
- If one L3 question requires multiple skills, chain them rather than flattening them. Use financial-statement-analysis before valuation-analysis when valuation depends on freshly parsed filings or earnings releases.
- DeepSeek should produce the first structured L3 reading answer from those materials: fact, inference, preliminary judgment, gap, trigger, source links, and support/refute/lead stance.
- GPT must verify DeepSeek's L3 answer against source links or local files, resolve conflicts, correct unsupported claims, and write the final L3 answer and parent rollup.
- If investment implications exist, final output must map to specific securities or assets with ticker/name, bottleneck or thesis node, reason, strength, required verification data, catalysts, risks, and source links.
- Target output must also include chokepoint exposure, chokepoint score or score drivers, future space, current valuation odds or a clear valuation-data gap, downgrade triggers, and monitorability. Do not raise observation strength if valuation is missing or chokepoint capture is weak.
- Every target or major thesis node should preserve a prediction review field: initial claim, validation horizon, required evidence, current status, and review trigger. The final HTML may summarize this inside Q3/Q4; detailed tracking can live in workbench JSON.
- DeepSeek's primary role in research is parsing concrete source materials: research reports, news/messages, earnings releases, annual reports, filings, transcripts, expert interviews, and other single-source documents.
- Delegate a source to DeepSeek only after GPT has defined the research question, source priority, and extraction schema.
- DeepSeek should return structured extraction: key facts, numbers, dates, source bucket, support/refute/lead stance, affected QA node, uncertainty, and follow-up data needs.
- For L3 questions, DeepSeek is the default first-pass reader and answer drafter for the selected materials.
- DeepSeek may also support source summarization, key-point extraction, initial classification, and candidate-question drafting.
- DeepSeek must not produce final judgments, trading instructions, financial conclusions, architecture decisions, target strength ranking, source reliability adjudication, or unchecked target recommendations.
- GPT remains responsible for source selection, source reliability checks, cross-source conflict resolution, reasoning synthesis, target strength, final report language, and all user-facing conclusions.
- Do not call a company "good" without naming the M driver and the M defect risk.
- Do not promote an idea without a time frame and disconfirming tests.

## HTML QA Presentation

The final report presentation contract is `frameworks/research_report_contract.md`. Use it as the default for all future research reports unless the user explicitly asks to iterate on the framework.

- Final user-facing HTML reports must have exactly four top-level sections: `当前研究目标`, `问题下钻`, `最终标的推荐`, and `来源索引`.
- `最终标的推荐` should synthesize all QA information into a ranked observation list with specific targets, win probability, payoff odds, rationale, required verification data, and downgrade triggers.
- For bottleneck/chokepoint-driven research, `最终标的推荐` must show how chokepoint evaluation affects rank and strength.
- Do not put iteration notes, "what changed", execution traces, quality-framework explanations, tool attribution, DeepSeek usage notes, or workbench appendices in the final HTML. Keep those in workbench JSON, logs, or internal artifacts.
- Preserve the full available QA tree when refreshing a report. Do not compress the report down to only a few questions unless the user explicitly asks for an executive summary.
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
- Refreshed canonical reports must reuse the shared report component contract from `frameworks/research_report_contract.md`: `qa-card`, `artifact-card`, `target-section` with `target-table`, and a single collapsed `source-collapse`. Do not swap in alternate report components such as per-target `target-card`, grouped `source-bucket`, or `section-lead` layouts unless the user asks to redesign the frontend.

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
- Within that framework, route each L3 leaf task through the specialty skill dispatch layer when a relevant skill exists. Specialized skills support extraction and analysis; GPT remains the final research director and verifier.
- Preserve the dispatch trace in generated workbench/report artifacts so the user can see which skill handled each concrete problem and how GPT verified it.

## Quality Pipeline

1. `investment-question-architect` designs the research questions.
2. `research-source-planner` decides which materials to collect for each L3 question.
3. Specialty parsers read the materials:
   - `financial-statement-analysis`
   - `valuation-analysis`
   - `industry-report-analysis`
   - `news-event-analysis`
   - `opinion-analysis`
   - `leaf-research-deepseek`
4. GPT verifies parsed facts and writes the final L3 answer.
5. Parent QA nodes roll up only verified child answers.
6. `target-recommendation-analysis` turns verified conclusions into a specific observation list with future space, valuation odds, strength, risks, catalysts, and required data.
