---
name: value-invest-research
description: Use for investment research workflows that start from a user research goal and produce an auditable QA drilldown, evidence-linked synthesis, and specific target observation list. This skill has one canonical research-goal QA framework.
---

# Value Invest Research Skill

This Skill turns heterogeneous market information into auditable research artifacts. The default sequence is a single research-goal QA framework:

1. Current research goal.
2. Research execution plan.
3. Three-layer QA drilldown.
4. Four-bucket information collection.
5. Evidence-linked synthesis.
6. Specific target observation list.

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
- When the user changes a report structure, interaction pattern, section order, or presentation logic, treat that change as a persistent default research-system requirement unless the user explicitly says it is one-off.
- In the same change, update `AGENTS.md`, this `SKILL.md`, and `frameworks/research_goal_qa.md` so future reports follow the new structure.
- Research output must be organized by QA directions, not standalone step components: Q1 confirm demand, Q2 locate bottlenecks, Q3 bind disconfirming tests, Q4 target observation list with reasons.
- Every level must state what questions to ask, how to collect information, how to connect information into reasoning, and how to present the output.
- Use at most three QA layers by default: Q1, Q1.1, Q1.1.1.
- Details, scorecards, tables, and jump pages must be nested under the QA layer whose question they answer, not placed as Q-parallel components or unrelated top-level appendices.
- Bottleneck scorecards belong under the relevant bottleneck question, usually Q2.1.
- Disconfirming-test lists belong under the relevant risk question, usually Q3.1.
- Target tables belong under the relevant target-selection question, usually Q4.1.
- Each layer may only roll up conclusions from its child answers and auditable sources.
- L3 answers must separate fact, inference, judgment, gap, and trigger.
- For every L3 question, GPT must decide which materials to search or read, define the extraction schema, and assign those concrete materials to DeepSeek MCP for careful reading.
- DeepSeek should produce the first structured L3 reading answer from those materials: fact, inference, preliminary judgment, gap, trigger, source links, and support/refute/lead stance.
- GPT must verify DeepSeek's L3 answer against source links or local files, resolve conflicts, correct unsupported claims, and write the final L3 answer and parent rollup.
- If investment implications exist, final output must map to specific securities or assets with ticker/name, bottleneck or thesis node, reason, strength, required verification data, catalysts, risks, and source links.
- DeepSeek's primary role in research is parsing concrete source materials: research reports, news/messages, earnings releases, annual reports, filings, transcripts, expert interviews, and other single-source documents.
- Delegate a source to DeepSeek only after GPT has defined the research question, source priority, and extraction schema.
- DeepSeek should return structured extraction: key facts, numbers, dates, source bucket, support/refute/lead stance, affected QA node, uncertainty, and follow-up data needs.
- For L3 questions, DeepSeek is the default first-pass reader and answer drafter for the selected materials.
- DeepSeek may also support source summarization, key-point extraction, initial classification, and candidate-question drafting.
- DeepSeek must not produce final judgments, trading instructions, financial conclusions, architecture decisions, target strength ranking, source reliability adjudication, or unchecked target recommendations.
- GPT remains responsible for source selection, source reliability checks, cross-source conflict resolution, reasoning synthesis, target strength, final report language, and all user-facing conclusions.
- Do not call a company "good" without naming the M driver and the M defect risk.
- Do not promote an idea without a time frame and disconfirming tests.

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
