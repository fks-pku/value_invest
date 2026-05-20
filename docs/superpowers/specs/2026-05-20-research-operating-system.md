# Research Operating System Layer

## Goal

Upgrade stock research from static report generation into a file-system-first research operating system. The durable asset is the structured chain from evidence to foundation coverage, business nodes, KPIs, assumptions, questions, message-flow impact, and risk monitors.

## Artifacts

`value-invest-research build-research-system <TICKER>` writes four files under `stocks/<TICKER>/research_system/`:

- `foundation_graph.json`: eight-section foundation coverage plus facts, inferences, judgments, gaps, business nodes, KPI snippets, assumptions, and risks.
- `question_graph.jsonl`: parent-child question tree with priority, linked sections, linked business nodes, linked assumptions, required evidence, disconfirming signals, and decision rules.
- `message_flow.jsonl`: one analysis row per evidence item with prior baseline, marginal change, affected sections/nodes/KPIs/assumptions, FengHe classification, certainty, impact, and follow-up questions.
- `research_dashboard.html`: readable dashboard for human review.

## Contract

- Evidence remains the source of material claims.
- Low- and medium-reliability evidence may seed questions but cannot strengthen thesis conclusions by itself.
- Each P0 question needs a concrete decision rule and disconfirming signals.
- Message-flow rows must state the prior baseline and marginal change; summary-only news is not enough.
- The dashboard is not a trading instruction and should not contain buy/sell/position guidance.

## Workflow

1. Build or update `evidence.jsonl`.
2. Run `build-research-system`.
3. Review P0 questions and missing foundation sections.
4. Add targeted evidence to close gaps.
5. Use FengHe graph/report workflows only after the foundation and question graph are explicit.
