# Research Quality Gate

This gate defines the minimum internal artifacts for a complete refreshed research report. It is execution infrastructure, not public report content.

## Required Artifacts

Every complete refreshed research project must preserve these files in the project directory:

- `professional_report.html`: clean public report using the locked four-section contract: `当前研究的问题` -> `行业概况` -> `标的推荐` -> `来源索引`.
- `qa_tree.json`: full Q1-Q4 tree with L1, L2, L3, and any adaptive L4/L5 research-unit nodes.
- `source_extractions.jsonl`: one parser or DeepSeek extraction per source-to-L3/L4/L5 research-unit pair.
- `leaf_source_reviews.jsonl`: one GPT verification record per extraction.
- `investment_workbench.json`: internal scoring worksheet, frozen recommendations, labels when relevant, and validation output.

For BOM-first S-curve research, `investment_workbench.json` must also preserve one search artifact per `BOM node x six questions`, including one parse/review record for every selected source. Q6 is incomplete without explicit refuting source IDs and refutation evidence.

The gold regression fixture is `tests/fixtures/research_quality_gold/`. New framework changes should keep this fixture passing or intentionally update it with matching tests.

## L3-L5 Quality Gate

An L3-L5 research unit is complete only when all of the following exist:

- decision fields: `materiality`, `decision_use`, `support_evidence`, `refute_evidence`, `target_implications`, `score_component`, `minimum_evidence_gate`, and `refuting_source_plan`.
- structured `source_plan` naming concrete source IDs, expected fields, source bucket, cutoff status, allowed usage, and preferred parser skill.
- structured `skill_dispatch` naming selected skill, concrete materials, extraction schema, source extraction IDs, review IDs, execution status, fallback status, and GPT verification status.
- final answer fields: fact, inference, judgment, gap, trigger, and source links.

Fact, inference, and judgment must be differentiated. A source list without a mapping, driver table, bridge table, score table, scenario table, or kill-test table is insufficient when the research-unit question asks a mechanism question.

For event/conference research, an L3-L5 research unit is incomplete if it only summarizes announcements. The artifact must include at least one structured bridge appropriate to the question: official fact boundary, new-information delta, commercialization stage, event-to-financial transmission chain, chokepoint scorecard, company exposure bridge, valuation odds bridge, or target ranking worksheet.

## Source Parser Gate

`source_extractions.jsonl` must include these fields for every record:

- `extraction_id`
- `l3_question_id`
- `source_id`
- `source_title`
- `source_bucket`: `evidence`, `research_report`, `opinion`, or `message`
- `parser`
- `parser_status`
- `schema_fields`
- `key_facts`
- `inference`
- `support_refute_or_lead`: `support`, `refute`, or `lead`
- `uncertainties`
- `follow_up_data`
- `created_at`

`schema_fields` must fill the fields requested by the matching L3-L5 `skill_dispatch.extraction_schema`. The field name `l3_question_id` is retained in JSONL for backward compatibility, but it may reference an L3, L4, or L5 research unit.

## GPT Review Gate

`leaf_source_reviews.jsonl` must include these fields for every parser record:

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

Only verified or verified-with-caveats records may strengthen a final L3-L5 answer. Rejected or needs-review records can remain in the audit trail, but they cannot support parent conclusions.

## Historical Backtest Anti-Leakage Gate

Historical backtests must reduce both source-time leakage and model-time leakage:

- `qa_tree.json` must include `anti_leakage_controls` with `as_of_date`, cutoff source-pack policy, LLM prior policy, question-tree policy, supply-chain policy, scoring policy, and label isolation policy.
- Every L3-L5 research unit must include `backtest_grounding` with exact `allowed_source_ids`, `model_prior_policy`, `post_cutoff_knowledge_policy`, and empty `non_source_claims`.
- Source parser records must not use label-only or post-cutoff thesis sources.
- Target score subcomponents must reference cutoff-visible source IDs or GPT-approved leaf review IDs.
- Label fields such as `forward_3m_return`, `end_price`, `label_status`, and `excess_return` must not appear in score rationale or QA reasoning.

The current LLM's background knowledge is not evidence. It may frame hypotheses, but it cannot strengthen facts, scores, ranking, or action state without cutoff-source grounding.

## Target Score Gate

Every target in `investment_workbench.json` must preserve:

- seven auditable component score subcomponents: chokepoint strength, future space, valuation odds, evidence quality, disconfirming-risk control, monitorability, and payoff convexity.
- four public gate dimensions: scarcity or monopoly, mispricing, earnings elasticity, and risk control.
- a canonical `thesis_node_id`, candidate action state, final action state, and persisted `research_gate`.
- component-specific evidence IDs or review IDs for verified score subcomponents; gap rows instead use `status=gap` and `gap_reason`.
- hard thesis kill tests with trigger metric, threshold, observation frequency, source plan, and downgrade action for any `actionable_long` target.

The default state is conservative. A target cannot become `actionable_long` unless its canonical BOM mapping, all six questions, explicit refutation, explicitly verified company/segment financial exposure, valuation/mispricing, score trace, scarcity, earnings elasticity, and risk control all pass. Generic evidence IDs cannot stand in for company exposure. Missing evidence caps the target at `watch_only`; missing BOM mapping is `no_action`.

## Validation Commands

Run these checks before treating a complete refreshed report as done:

```bash
PYTHONPATH=src python3 -m value_invest_research validate-report-contract <project_dir>/professional_report.html
PYTHONPATH=src python3 -m value_invest_research validate-research-artifacts <project_dir> --require-l3
```

For historical/backtest mode, also run:

```bash
PYTHONPATH=src python3 -m value_invest_research audit-time-slice <project_dir>/sources.jsonl --as-of-date YYYY-MM-DD
```

Final HTML must not render source parser traces, GPT review traces, tool logs, quality-gate explanations, iteration notes, or workbench appendices unless the user explicitly asks to inspect process.
