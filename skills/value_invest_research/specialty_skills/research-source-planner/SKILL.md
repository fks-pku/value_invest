---
name: research-source-planner
description: Use this skill after an investment QA tree exists and before reading materials. It creates a source-search plan for each L3 question: which primary filings, earnings calls, industry reports, datasets, news, and opinions to collect, why each source matters, and which specialty parser should read it.
---

# Research Source Planner

This skill converts L3 questions into concrete source plans. It is responsible for collecting the right information, not for final synthesis.

## Source Priority

Use this order unless the question requires otherwise:

1. Primary evidence: filings, annual reports, quarterly reports, earnings releases, exchange announcements, regulator documents, official datasets.
2. Company voice: earnings calls, investor presentations, investor-day materials, management Q&A.
3. Industry data and research reports: sell-side reports, SEMI, Gartner, TrendForce, IDC, S&P, Visible Alpha, trade bodies, reputable databases.
4. News/messages: public news, supply-chain updates, policy headlines, product launch messages.
5. Opinions: expert interviews, investor views, industry commentary.

## L3 Source Plan Template

For each L3 question, output:

- `l3_question`
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
- Every source must map to a question, hypothesis, or trigger.
- For every support source, plan at least one refuting or boundary-check source.
- Low-reliability messages can create leads but cannot strengthen conclusions by themselves.

## DeepSeek Handoff

When DeepSeek MCP is available, prepare a narrow prompt per source or per small source bundle:

- The exact L3 question.
- Why the source is being read.
- The extraction schema.
- The source bucket.
- The expected support/refute/lead classification.

GPT remains responsible for source selection, source reliability, conflict resolution, and final synthesis.
