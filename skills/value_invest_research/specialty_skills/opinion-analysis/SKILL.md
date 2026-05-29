---
name: opinion-analysis
description: Use this skill whenever investment research needs to parse expert views, investor opinions, social posts, interviews, conference notes, or named personal viewpoints. It extracts arguments, assumptions, and dissenting questions without treating opinions as facts.
---

# Opinion Analysis

This skill turns opinions into reasoning inputs and adversarial questions.

## Extract

- `speaker_or_author`
- `date`
- `context`
- `core_claim`
- `argument_chain`
- `implicit_assumptions`
- `evidence_cited_by_author`
- `what_is_fact_vs_opinion`
- `support_refute_or_lead`
- `affected_qa_node`
- `strongest_counterquestion`
- `data_needed_to_verify`
- `source_link`

## Rules

- Opinions are not evidence unless they cite verifiable facts.
- Use opinions to find blind spots, variant perception, and counterarguments.
- Distinguish expert domain competence from market popularity.
- Extract the reasoning, not just the conclusion.
- If an opinion disagrees with official evidence, preserve the disagreement and define a verification test.

## QA Contribution

An opinion can:

- Generate a new L3 question.
- Strengthen a disconfirming-test list.
- Explain market perception.
- Identify what data investors may be missing.

It cannot by itself produce a high-confidence investment judgment.
