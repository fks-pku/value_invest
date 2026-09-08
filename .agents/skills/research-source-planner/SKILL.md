---
name: research-source-planner
description: Use this skill after an investment QA tree exists and before reading materials. It creates a source-search plan independently for the current terminal question at L3, L4, or L5, before any deeper question is generated.
---

# Research Source Planner

This skill converts the current deepest unanswered question into a concrete source plan. It is responsible for collecting the right information, not for final synthesis or premature decomposition.

## Source Priority

Use this order unless the question requires otherwise:

1. Primary evidence: filings, annual reports, quarterly reports, earnings releases, exchange announcements, regulator documents, official datasets.
2. Company voice: earnings calls, investor presentations, investor-day materials, management Q&A.
3. Industry data and research reports: sell-side reports, SEMI, Gartner, TrendForce, IDC, S&P, Visible Alpha, trade bodies, reputable databases.
4. News/messages: public news, supply-chain updates, policy headlines, product launch messages.
5. Opinions: expert interviews, investor views, industry commentary.

## Active-Question Source Plan Template

For each current terminal L3/L4/L5 question, output:

- `question_path`: the full L1-to-leaf path.
- `active_question`
- `question_level`
- `required_data`
- `analysis_plan`
- `materiality`: why the answer changes parent conclusion or target strength.
- `source_plan`:
  - `source_bucket`: evidence, research_report, message, opinion.
  - `source_type`
  - `examples_or_search_queries`
  - `why_needed`
  - `expected_fields`
  - `preferred_skill`
  - `deepseek_allowed`: true or false.
- `minimum_evidence_gate`: what must be collected before strengthening the conclusion.
- `refuting_source_plan`: what to search specifically to disprove the thesis.
- `freshness_requirement`: latest quarter, latest filing, historical baseline, or event window.

## Search Discipline

- Never collect sources just because they are easy to find.
- Every source must originate from and map to one current terminal question. A broad pool can preserve candidates but cannot complete the question.
- Start at L3. Do not plan sources for hypothetical L4/L5 questions before the current answerability gate fails.
- For every support source, plan at least one refuting or boundary-check source.
- Low-reliability messages can create leads but cannot strengthen conclusions by themselves.

## DeepSeek Handoff

When DeepSeek MCP is available, prepare a narrow prompt per source or per small source bundle:

- The exact current terminal question, its level, and its parent path.
- Why the source is being read.
- The extraction schema.
- The source bucket.
- The expected support/refute/lead classification.

GPT remains responsible for source selection, source reliability, conflict resolution, and final synthesis.
