# Value Invest Research

File-system-first investment research assistant for US equities. The project stores research objects as plain files, keeps structured evidence alongside memos, and provides CLI workflows for stock, event, sector, SEC, price, and LLM-assisted research.

The stock workflow is foundation-first: every company should first get an eight-section company foundation analysis. FengHe 3C3D5M3T is then used as the downstream message-flow layer for events, catalysts, marginal changes, time frames, and thesis updates.

This is not an automated trading system. It does not place orders or issue final buy/sell instructions; it helps preserve evidence and produce auditable research drafts for human review.

## Current Status

- Core scaffolding and validation are implemented.
- CLI commands exist for stocks, events, SEC ingestion, price ingestion, foundation-first stock research, structured research-system generation, memo updates, event research, and sector/theme research.
- A simplified research-system layer currently focuses on foundation coverage, business nodes, KPI snippets, assumptions, risk monitors, eight section detail pages, and a foundation dashboard.
- A deterministic research graph pipeline exists for FengHe consensus baselines, 3T questions, hypotheses, assumption tests, and forward reports.
- The primary stock research sequence is company foundation first, then FengHe message-flow analysis.
- Third-party integrations are optional. Core commands work without `openai`, `pyyaml`, or `yfinance`; integration commands report a clear install hint when their package is missing.
- The repository includes sample AAPL, event, and sector research artifacts.

## Install

Core editable install:

```powershell
python -m pip install -e . --no-deps
```

Optional integrations:

```powershell
python -m pip install -e ".[all]"
```

Use narrower extras when preferred:

```powershell
python -m pip install -e ".[ingest]"
python -m pip install -e ".[llm]"
python -m pip install -e ".[research]"
```

## Run

Without installing, use `PYTHONPATH=src` or the test runner in this repo.

```powershell
$env:PYTHONPATH = "src"
python -m value_invest_research --help
```

After editable install:

```powershell
value-invest-research --help
```

Examples:

```powershell
value-invest-research init-stock MSFT --company-name "Microsoft Corporation"
value-invest-research init-event 2026-05-06 "US Iran Conflict"
value-invest-research build-evidence AAPL
value-invest-research build-research-system AAPL
value-invest-research validate-qa-system AAPL
value-invest-research run-stock-qa-pipeline AAPL --task-limit 80 --run-local-collection --synthesize-answers
value-invest-research add-research-question AAPL --parent-id foundation.history --question "这次战略转型是否改变利润池？"
value-invest-research add-research-question AAPL --parent-id foundation.history --question "这次历史问题是否已能直接回答？" --terminal
value-invest-research record-question-information AAPL --node-id current_business.profit-cash.segment-profit-pool --category research_report --source-type sell_side_report --source-name "Segment margin note" --url "https://example.com/report" --summary "服务和硬件利润池需要分开验证。"
value-invest-research build-collection-tasks AAPL --limit 20
value-invest-research run-collection-tasks AAPL --limit 20 --min-score 8
value-invest-research discover-source-candidates AAPL --limit 20 --results-per-task 3
value-invest-research apply-source-candidates AAPL --path stocks/AAPL/research_system/source_candidates.jsonl
value-invest-research import-question-information AAPL --path collected_sources.jsonl
value-invest-research fetch-question-information-url AAPL --node-id current_business.profit-cash.segment-profit-pool --category evidence --url "https://example.com/source"
value-invest-research build-synthesis-tasks AAPL --limit 20
value-invest-research run-answer-synthesis AAPL --limit 20
value-invest-research run-answer-synthesis AAPL --limit 20 --use-llm --api-key $env:LLM_API_KEY
value-invest-research import-answer-synthesis AAPL --path synthesized_answers.jsonl
value-invest-research write-professional-report AAPL
value-invest-research write-professional-report AAPL --use-llm --api-key $env:LLM_API_KEY
value-invest-research validate-qa-system AAPL --require-professional-report
value-invest-research apply-question-queue AAPL --path queued_questions.jsonl
value-invest-research apply-question-queue AAPL --path queued_questions.jsonl --synthesize-answers --write-professional-report
value-invest-research build-meta-qa --object-type industry --object-id "AI 眼镜" --meta-question "了解 AI 眼镜行业是否有长期投资价值" --project-id ai_glasses
value-invest-research build-meta-qa --object-type industry --object-id "AI 眼镜" --meta-question "了解 AI 眼镜行业是否有长期投资价值" --project-id ai_glasses --planner-use-llm --planner-api-key $env:LLM_API_KEY --force-plan
value-invest-research run-meta-qa-pipeline --object-type industry --object-id "AI 眼镜" --meta-question "了解 AI 眼镜行业是否有长期投资价值" --project-id ai_glasses --task-limit 80 --synthesize-answers
value-invest-research run-meta-qa-pipeline --object-type industry --object-id "AI 眼镜" --meta-question "了解 AI 眼镜行业是否有长期投资价值" --project-id ai_glasses --planner-use-llm --planner-api-key $env:LLM_API_KEY --force-plan --synthesize-answers --synthesis-use-llm --synthesis-api-key $env:LLM_API_KEY --write-professional-report --professional-report-use-llm --professional-report-api-key $env:LLM_API_KEY
value-invest-research plan-meta-qa --object-type industry --object-id "AI 眼镜" --meta-question "了解 AI 眼镜行业是否有长期投资价值" --project-id ai_glasses
value-invest-research plan-meta-qa --object-type industry --object-id "AI 眼镜" --meta-question "了解 AI 眼镜行业是否有长期投资价值" --project-id ai_glasses --use-llm --api-key $env:LLM_API_KEY --force
value-invest-research add-meta-qa-question --project-id ai_glasses --parent-id l1.demand.market_size --question "AI 眼镜出货是否能形成真实消费电子新品类？"
value-invest-research add-meta-qa-question --project-id ai_glasses --parent-id l1.demand.market_size --question "AI 眼镜留存问题是否已能直接回答？" --terminal
value-invest-research record-meta-qa-information --project-id ai_glasses --node-id <node_id> --category evidence --source-type industry_data --source-name "Shipment tracker" --url "https://example.com/report" --summary "行业数据跟踪出货和留存。"
value-invest-research build-meta-qa-collection-tasks --project-id ai_glasses --limit 20
value-invest-research run-meta-qa-collection-tasks --project-id ai_glasses --limit 20 --min-score 8
value-invest-research discover-meta-qa-source-candidates --project-id ai_glasses --limit 20 --results-per-task 3
value-invest-research apply-meta-qa-source-candidates --project-id ai_glasses --path research/bom/ai_glasses/source_candidates.jsonl
value-invest-research import-meta-qa-information --project-id ai_glasses --path collected_sources.jsonl
value-invest-research fetch-meta-qa-information-url --project-id ai_glasses --node-id <node_id> --category research_report --url "https://example.com/report"
value-invest-research build-meta-qa-synthesis-tasks --project-id ai_glasses --limit 20
value-invest-research run-meta-qa-answer-synthesis --project-id ai_glasses --limit 20
value-invest-research run-meta-qa-answer-synthesis --project-id ai_glasses --limit 20 --use-llm --api-key $env:LLM_API_KEY
value-invest-research import-meta-qa-answer-synthesis --project-id ai_glasses --path synthesized_answers.jsonl
value-invest-research write-meta-qa-professional-report --project-id ai_glasses
value-invest-research write-meta-qa-professional-report --project-id ai_glasses --use-llm --api-key $env:LLM_API_KEY
value-invest-research validate-meta-qa-system --project-id ai_glasses --require-professional-report
value-invest-research apply-meta-qa-question-queue --project-id ai_glasses --path queued_questions.jsonl
value-invest-research apply-meta-qa-question-queue --project-id ai_glasses --path queued_questions.jsonl --synthesize-answers --write-professional-report
value-invest-research build-research-graph AAPL
value-invest-research validate-evidence stocks/AAPL/evidence.jsonl
value-invest-research research-stock AAPL --api-key $env:LLM_API_KEY
```

`research-stock` writes a timestamped Markdown report and structured signal JSON under `stocks/<TICKER>/research_reports/`.
`build-evidence` converts structured SEC facts and price CSV rows into stable evidence IDs under `stocks/<TICKER>/evidence.jsonl`.
`build-research-system` converts local evidence into the layered QA research system under `stocks/<TICKER>/research_system/`: `foundation_graph.json`, `qa_tree.json`, `information_collection.jsonl`, compatibility placeholders for `question_graph.jsonl` and `message_flow.jsonl`, eight section pages under `pages/`, `research_dashboard.html`, and the aggregated `research_report.html`.
`validate-qa-system` checks whether the current stock QA artifacts satisfy the layered research contract: L0 question, node links, max-depth boundary, every terminal question's four information categories, leaf answers, dashboard, and report. Add `--require-professional-report` when the final prose report must also exist.
`run-stock-qa-pipeline` orchestrates the stock layered QA workflow from object to report: build the foundation QA system, optionally run local evidence matching, build collection tasks, optionally discover/apply candidate sources, build answer-synthesis tasks, and, with `--synthesize-answers`, generate/apply professional answers before writing `pipeline_run.json` plus `pipeline_runs.jsonl`. Add `--synthesis-use-llm --synthesis-api-key <KEY>` when the answer synthesis stage should call the configured LLM instead of the deterministic local draft. Add `--write-professional-report` to write `professional_report.md/html`, and `--professional-report-use-llm --professional-report-api-key <KEY>` for an LLM-written final report.
`add-research-question` appends a user question to `stocks/<TICKER>/research_system/custom_questions.jsonl`, attaches it to the requested QA node, expands follow-up questions up to the three-layer limit when needed, and rebuilds the dashboard/report. Add `--terminal` when the question is already at answerable granularity; the system will not add auto drill-down children and will instead create the four information categories directly for that node.
`record-question-information` appends or updates one `evidence.jsonl` source, binds it to a specific QA node through `used_in=research_system:<node_id>`, refreshes the four-bucket information index, and rebuilds the dashboard/report.
`build-collection-tasks` turns the leaf-question information checklist into executable collection tasks under `stocks/<TICKER>/research_system/collection_tasks.jsonl`; each task includes priority, search query, recommended source types, acceptance criteria, expected fields, and the binding command.
`run-collection-tasks` executes those tasks against the local `evidence.jsonl` corpus, writes `collection_results.jsonl`, binds matching sources to the right QA nodes, and refreshes the dashboard/report. Use `--dry-run` to inspect matches before applying them.
`discover-source-candidates` turns collection tasks into `source_candidates.jsonl` by querying the web or consuming a JSONL search-results export with `task_id`, `title`, `url`, and `snippet`. Each candidate is screened by category, domain, source type, reliability, materiality, score, and an executable fetch command.
`apply-source-candidates` fetches accepted candidates from `source_candidates.jsonl`, binds them to the relevant stock QA node, writes `candidate_import_results.jsonl`, and refreshes the evidence/report loop. Use `--dry-run` before applying a candidate set.
`import-question-information` batch-imports collected stock sources from JSONL, validates required fields, binds each source to the target QA node, and refreshes the dashboard/report.
`fetch-question-information-url` fetches one URL, extracts the page title and readable text when possible, writes a `fetched_sources.jsonl` audit row, binds the source to a stock QA node, and refreshes the dashboard/report. Use `--summary` when the source is a PDF or another format that cannot be extracted reliably.
`build-synthesis-tasks` exports `synthesis_tasks.jsonl` for professional answer writing. Each task carries the node question, parent question, current answer, four-bucket source index, source balance, expected output fields, and import command.
`run-answer-synthesis` reads `synthesis_tasks.jsonl`, generates structured professional answers into `synthesized_answers.jsonl`, and applies them by default. By default it uses a deterministic local draft; add `--use-llm --api-key <KEY>` for LLM-written answers. Use `--no-apply` to only draft answers for review.
`import-answer-synthesis` imports `synthesized_answers.jsonl`, appends durable rows to `synthesis_overrides.jsonl`, applies the latest answer per node, and rebuilds the dashboard/report so human or LLM-written professional answers flow back into the QA tree.
`write-professional-report` reads the current stock `qa_tree.json` and writes `professional_report.md` plus `professional_report.html`. It is the final prose synthesis layer after question planning, information collection, and node-level answer synthesis.
`apply-question-queue` batch-applies user-added stock QA questions from JSONL/JSON. Each row needs `parent_id` and `question`; add `"terminal": true` or `"should_drill_down": false` in a row when that question should directly enter four-bucket information collection instead of auto drill-down. The command writes formal custom question nodes, expands auto drill-down children when needed, refreshes the report, and rebuilds collection tasks unless `--no-build-tasks` is passed. Add `--synthesize-answers --write-professional-report` when a queued user question should immediately flow through node answer synthesis and the final `professional_report.md/html`; the same `--synthesis-use-llm` and `--professional-report-use-llm` options are available when those stages should call the configured LLM.
`build-meta-qa` creates a generic layered QA project for a company, industry, event, or custom meta-question under `research/bom/<PROJECT_ID>/`. By default it uses the deterministic planning baseline; add `--planner-use-llm --planner-api-key <KEY>` to let the configured LLM draft `question_plan.json`, and `--force-plan` when intentionally replacing an existing plan.
`run-meta-qa-pipeline` orchestrates the generic meta-question workflow from one question to report: create or refresh the question plan/tree, build collection tasks, optionally run local matching, optionally discover/apply candidate sources, build answer-synthesis tasks, and, with `--synthesize-answers`, generate/apply professional answers before writing pipeline manifests. Add `--planner-use-llm --planner-api-key <KEY>` for LLM question planning, `--synthesis-use-llm --synthesis-api-key <KEY>` to make the synthesis stage use the configured LLM, and `--write-professional-report` to write the final `professional_report.md/html`.
`plan-meta-qa` creates or refreshes the auditable `question_plan.json` used to expand a meta-question into L1/L2/L3 questions. The QA tree and reports are generated from this plan, so the system's question-expansion logic is inspectable before evidence collection. Add `--use-llm --api-key <KEY> --force` when the plan should be generated by the configured LLM instead of the deterministic baseline.
`add-meta-qa-question` and `record-meta-qa-information` provide the same update loop for generic QA projects: add a user question at any layer, bind four-bucket information to the relevant node, and rebuild the dashboard/report. Use `--terminal` when the new question should stop at that layer and become the direct information-collection unit.
`build-meta-qa-collection-tasks`, `run-meta-qa-collection-tasks`, `discover-meta-qa-source-candidates`, `apply-meta-qa-source-candidates`, and `import-meta-qa-information` provide the same task generation, local-corpus execution, candidate discovery, candidate fetching, and batch-import loop for generic QA projects.
`fetch-meta-qa-information-url` provides the same URL fetch, summary extraction, fetched-source audit log, node binding, and report refresh loop for generic QA projects.
`build-meta-qa-synthesis-tasks`, `run-meta-qa-answer-synthesis`, and `import-meta-qa-answer-synthesis` provide the same professional answer task/export, generated answer draft, and answer override/import loop for generic QA projects. `run-meta-qa-answer-synthesis --use-llm --api-key <KEY>` uses the configured LLM for the answer-writing step.
`write-meta-qa-professional-report` reads the current generic QA tree and writes `professional_report.md` plus `professional_report.html`; add `--use-llm --api-key <KEY>` for an LLM-written final research report.
`validate-meta-qa-system` applies the same contract checks to a generic meta-QA project under `research/bom/<PROJECT_ID>/`.
`apply-meta-qa-question-queue` applies queued generic QA questions with the same `parent_id` and `question` row schema; queue rows can also set `"terminal": true` or `"should_drill_down": false`. The command then refreshes the project report and collection tasks. Add `--synthesize-answers --write-professional-report` to run the complete interactive update loop from added question to synthesized node answers and final professional report output.
`build-research-graph` runs the full deterministic graph pipeline and writes `nodes.jsonl`, `edges.jsonl`, and `forward_report.html` under `stocks/<TICKER>/research_graph/`.

Graph stages are also callable one by one:

```powershell
value-invest-research build-consensus AAPL
value-invest-research generate-questions AAPL
value-invest-research build-hypotheses AAPL
value-invest-research test-hypotheses AAPL
value-invest-research write-forward-report AAPL
```

## Test

The repository test runner adds `src` to `sys.path` and avoids platform temp-directory permission issues by using a local ignored `.test_tmp/` folder.

```powershell
python tools/run_tests.py
```

## Layout

- `src/value_invest_research/`: Python package and CLI workflows.
- `tests/`: unittest suite and test helpers.
- `skills/value_invest_research/`: reusable research protocol, frameworks, prompts, and checklists.
- `config/`: editable watchlist, source priority, research objects, and event playbooks.
- `stocks/`: stock-level research objects.
- `research/`: event, sector, and theme research objects.
- `docs/superpowers/`: design specs and implementation plans.

## Company Foundation Analysis

Each company memo starts with an eight-section baseline:

1. Source and origin.
2. Company history.
3. Current business.
4. Value chain position.
5. Competitive landscape.
6. Strategy analysis.
7. Organization, culture, and governance.
8. Risk sweep.

This baseline answers "what is this company?" before asking what new information changes the thesis.

## Research System Layer

The research-system layer is the professional stock workspace between raw evidence and final reports. The active generator is intentionally foundation-only: first build the company baseline, then add downstream FengHe message-flow work later.

- `foundation_graph.json`: eight-section foundation coverage, facts, inferences, judgments, gaps, business nodes, KPIs, assumptions, risks, key questions, and four-bucket information mapping.
- `qa_tree.json`: L0/L1/L2/L3 question nodes with current answer, rollup conclusion, evidence buckets, synthesis, and child links.
- `information_collection.jsonl`: leaf-question collection checklist by evidence, research report, message, and opinion category.
- `collection_tasks.jsonl`: optional executable collection task list generated from the checklist, with priority, source requirements, acceptance criteria, and binding commands.
- `collection_results.jsonl`: optional local-corpus matching output from `run-collection-tasks`, ready to import or already applied depending on `--dry-run`.
- `source_candidates.jsonl`: optional candidate URL pool generated from collection tasks, with category screening, score, source type, reliability, materiality, and fetch commands.
- `candidate_import_results.jsonl`: optional application log from accepted source candidates.
- `synthesis_tasks.jsonl`: optional professional answer task list; each row packages one QA node, parent context, four-bucket source index, source balance, and required answer fields.
- `synthesized_answers.jsonl`: generated professional answer drafts from `run-answer-synthesis`, ready for review or automatic application.
- `synthesis_overrides.jsonl`: append-only imported professional answers. The latest row per `node_id` overrides the generated rule summary and is rolled back into pages and reports.
- `professional_report.md` and `professional_report.html`: final prose report generated from the current QA tree, node answers, source structure, and research gaps.
- `pages/*.html`: one detail page per foundation section.
- `question_graph.jsonl`: empty compatibility placeholder until downstream question generation is re-enabled.
- `message_flow.jsonl`: empty compatibility placeholder until downstream message-flow analysis is re-enabled.
- `research_dashboard.html`: a readable foundation dashboard for the first-layer company baseline.
- `research_report.html`: aggregated QA synthesis that rolls L3 findings into L2, L1, and the company foundation layer.
- `pipeline_run.json` and `pipeline_runs.jsonl`: current and historical end-to-end QA pipeline manifests, listing each stage, output path, and final report artifacts.

This layer should be built before writing polished reports. Reports are outputs; the durable research asset at this stage is the structured company baseline.

## Generic Meta-QA Layer

For non-stock-foundation questions, use `build-meta-qa`. It creates a standalone QA project from one meta-question and expands it into L1/L2/L3 question nodes. Leaf questions receive four-bucket information collection rows:

- Evidence: verified facts, announcements, official data, public reports, and other high-reliability inputs.
- Research report: commercial research, sell-side reports, industry notes, and structured third-party analysis.
- Message: public but unverified news, rumors, or emerging updates.
- Opinion: expert, industry, investor, or KOL views.

Outputs live under `research/bom/<PROJECT_ID>/`: `project.json`, `question_plan.json`, `qa_tree.json`, `information_collection.jsonl`, `collection_tasks.jsonl`, `collection_results.jsonl`, `source_candidates.jsonl`, `candidate_import_results.jsonl`, `synthesis_tasks.jsonl`, `synthesized_answers.jsonl`, `synthesis_overrides.jsonl`, `pipeline_run.json`, `pipeline_runs.jsonl`, `evidence.jsonl`, `research_dashboard.html`, `research_report.html`, `professional_report.md`, and `professional_report.html`.

## Research Graph Pipeline

The graph pipeline is the FengHe message-flow graph. It treats current facts and market consensus as the priced baseline after company foundation work exists. It then creates a local graph:

- Evidence nodes: validated `EvidenceRecord` entries.
- Framework nodes: FengHe 3C, 3D, 5M, and 3T concepts for message-flow analysis.
- Consensus nodes: what the current local evidence can support as baseline.
- Question nodes: what could change by T1/T2/T3.
- Hypothesis nodes: mechanisms that could move D1/D2/D3.
- Assumption-test nodes: what evidence would support or disconfirm each hypothesis.

The forward report is an HTML synthesis of the graph, not a final trading instruction.

## Boundaries

Research outputs must separate facts, inferences, and judgments. Material claims should cite evidence IDs. Low-reliability sources can create research questions, but should not change a thesis by themselves. Generic "good company" language is not enough: every stock view must state foundation status and gaps first, then cycle, marginal change, certainty, dominant D driver, 5M value/defect drivers, time frame, and disconfirming tests when analyzing message flow.
