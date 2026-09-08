---
name: leaf-research-deepseek
description: Use this skill for a current terminal L3/L4/L5 question when concrete materials have already been selected and DeepSeek MCP should carefully read them. It defines the source-reading prompt, extraction schema, and GPT verification checklist for first-pass answers.
---

# Leaf Research DeepSeek

This skill controls DeepSeek usage at the current-question level. DeepSeek is a source parser and first-pass drafter, not the final analyst.

## Preconditions

Before using this skill, GPT must define:

- Current question and level.
- Parent Q node.
- Selected concrete materials or links.
- Source priority.
- Extraction schema.
- How the answer could support, refute, or only lead to further work.

## DeepSeek Prompt Contract

Ask DeepSeek to return:

- `active_question`
- `question_level`
- `selected_materials`
- `source_title`
- `source_bucket`: evidence, research_report, message, or opinion.
- `key_facts`: numbers, dates, segment names, management statements, page/section hints.
- `inference`: what the facts imply, separated from facts.
- `preliminary_judgment`: bounded and clearly provisional.
- `support_refute_or_lead`
- `affected_qa_node`
- `investment_relevance`
- `uncertainties`
- `gap`
- `trigger`
- `follow_up_data`
- `source_links`

## GPT Verification Checklist

After DeepSeek returns:

1. Check whether the cited source really supports each material fact.
2. Downgrade unsupported claims to leads or remove them.
3. Separate company facts from industry estimates and opinions.
4. Identify conflicts across sources.
5. Decide whether the evidence gate is satisfied.
6. Write the current-question answer in fact / inference / judgment / gap / trigger format.
7. If the gate fails, create only the smallest next-level questions implied by the recorded gap; never pre-generate deeper branches.
8. Record that DeepSeek was used as source parser only.

## Do Not Let DeepSeek

- Decide final thesis strength.
- Rank targets.
- Resolve conflicts without GPT review.
- Turn messages or opinions into high-confidence evidence.
- Produce trading instructions.
