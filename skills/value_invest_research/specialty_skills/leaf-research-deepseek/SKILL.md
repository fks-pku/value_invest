---
name: leaf-research-deepseek
description: Use this skill for L3 leaf research when concrete materials have already been selected and DeepSeek MCP should carefully read them. It defines the source-reading prompt, extraction schema, and GPT verification checklist for first-pass L3 answers.
---

# Leaf Research DeepSeek

This skill controls DeepSeek usage at the leaf-question level. DeepSeek is a source parser and first-pass drafter, not the final analyst.

## Preconditions

Before using this skill, GPT must define:

- L3 question.
- Parent Q node.
- Selected concrete materials or links.
- Source priority.
- Extraction schema.
- How the answer could support, refute, or only lead to further work.

## DeepSeek Prompt Contract

Call DeepSeek with a large input context and output budget for formal investment source parsing:

- Treat input context separately from `max_tokens`. When the MCP server/model supports very large context, keep a complete filing, transcript, report, or coherent source bundle together if source integrity matters, up to the server-supported context limit.
- Use `max_tokens` 32000-64000 for long-source extraction.
- Use at least `max_tokens` 24000 for multi-source L3 first drafts.
- Use at least `max_tokens` 12000 for ordinary single-source parsing.
- Keep each call narrow even with the larger budget: prefer one complete source or coherent source bundle for one L3 question and one extraction schema.
- If output is truncated, malformed, empty, or stops mid-field, set `parser_status` to `incomplete`; do not use it for conclusions. Retry with a smaller source chunk or fall back to GPT-verified direct parsing.

Ask DeepSeek to return:

- `l3_question`
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
- `schema_fields`: a map for every requested extraction-schema field, each with value, source anchor when available, uncertainty/status, and evidence/review trace placeholders.

## Persisted Artifacts

Write every successful parser result to `source_extractions.jsonl` as one JSON object:

- `extraction_id`
- `l3_question_id`
- `source_id`
- `source_title`
- `source_bucket`
- `parser`: `deepseek_delegate` or another parser name
- `parser_status`: `ok`, `empty_response`, `fallback_gpt_direct_parse`, or `discarded`
- `key_facts`
- `schema_fields`
- `inference`
- `support_refute_or_lead`
- `uncertainties`
- `follow_up_data`
- `created_at`

Then write GPT's review to `leaf_source_reviews.jsonl`:

- `review_id`
- `extraction_id`
- `l3_question_id`
- `source_id`
- `gpt_verification_status`
- `adopted_facts`
- `corrections`
- `rejected_claims`
- `final_bucket`
- `final_support_refute_or_lead`
- `allowed_to_strengthen_conclusion`

Final L3 answers may only use adopted facts from reviewed extractions or GPT-recorded direct parses. A successful parser result for refreshed canonical reports must fill the L3 extraction schema in `schema_fields`; generic summaries without schema-field mapping are incomplete until GPT maps and verifies them.

## GPT Verification Checklist

After DeepSeek returns:

1. Check whether the cited source really supports each material fact.
2. Downgrade unsupported claims to leads or remove them.
3. Separate company facts from industry estimates and opinions.
4. Identify conflicts across sources.
5. Decide whether the evidence gate is satisfied.
6. Write the final L3 answer in fact / inference / judgment / gap / trigger format.
7. Record that DeepSeek was used as source parser only.

## Do Not Let DeepSeek

- Decide final thesis strength.
- Rank targets.
- Resolve conflicts without GPT review.
- Turn messages or opinions into high-confidence evidence.
- Produce trading instructions.
