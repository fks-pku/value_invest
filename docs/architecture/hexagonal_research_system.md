# Hexagonal Research System Architecture

This document is the target architecture for `value_invest_research`. The goal is to make research modules replaceable: changing source parsing, LLM providers, report rendering, market data ingestion, or CLI behavior should not force changes in unrelated modules.

For a Chinese, example-driven explanation of how the system works end to end, read [`research_system_working_principles.md`](research_system_working_principles.md).

## Dependency Rule

Dependencies point inward:

```text
adapters/inbound  -> application -> domain
adapters/outbound -> ports       -> application
application       -> ports + domain
domain            -> pure Python business rules only
```

Forbidden dependencies:

- `domain` must not import `application`, `ports`, or `adapters`.
- `application` must not import `adapters`.
- `ports` must not import `application` or `adapters`.
- CLI, file system, LLMs, DeepSeek, SEC, yfinance, HTML rendering, and browser concerns stay in adapters.

## Package Layout

```text
src/value_invest_research/
  domain/
    research_goal.py           # research objective and research-type mapping
    domain_playbooks.py        # domain-specific question adapters
    question_architecture.py   # adaptive QA architecture, maximum depth five
    bom_research_readiness.py  # semantic completion, evidence gates, target gating
    report_view_model.py       # renderer-facing public report model
    research_artifacts.py      # pure data objects for research artifacts
    quality_gates.py           # artifact validation rules and result shaping

  application/
    use_cases/
      validate_research_project.py
      plan_research_goal.py
      build_report_view_model.py
      render_research_project_report.py
    orchestration/
      research_orchestrator.py # pipeline sequencing, no direct I/O

  ports/
    repositories.py            # project, artifact, and source-universe protocols
    renderers.py               # report renderer protocols
    llm.py                     # planned: LLM/source parser protocols
    market_data.py             # planned: pricing/filing protocols

  adapters/
    inbound/
      ...                      # planned: CLI adapter split from root cli.py
    outbound/
      filesystem_research_artifacts.py
      filesystem_research_project.py
      canonical_html_report_renderer.py
      report_sections/          # per-section HTML adapters for the locked public report contract
      ...                      # planned: LLM, DeepSeek, SEC, yfinance, HTML renderer adapters
```

The current codebase still has compatibility modules at package root. Migration should be incremental: add ports and use cases first, move one vertical slice, keep tests green, then move the next slice.

## Migrated Vertical Slices

`validate-research-artifacts` is the first hexagonal slice.

Current flow:

```text
CLI command
  -> FileSystemResearchArtifactRepository
  -> ValidateResearchProject use case
  -> domain.quality_gates.validate_research_artifacts
  -> existing contract validators
  -> stable CLI summary
```

Why this slice first:

- It has clear inputs: `qa_tree.json`, `source_extractions.jsonl`, `leaf_source_reviews.jsonl`, `investment_workbench.json`.
- It has clear output: validation status, counts, and issues.
- It touches the research quality gate without changing report generation behavior.
- It creates a pattern for future modules.

`validate-report-contract` follows the same shape:

```text
CLI command
  -> FileSystemReportDocumentRepository
  -> ValidateReportContract use case
  -> domain.quality_gates.validate_report_contract
  -> existing report contract validator
  -> stable CLI summary
```

These slices prove the intended rule: the CLI no longer owns file loading or validation rules for these commands.

`audit-time-slice` is also migrated:

```text
CLI command
  -> FileSystemSourceListRepository
  -> AuditTimeSlice use case
  -> domain.quality_gates.audit_source_time_slice
  -> existing time-slice validator
  -> stable CLI summary
```

Target scoring and source parsing persistence now also have application seams:

```text
target candidates
  -> ScoreTargets use case
  -> domain.bom_research_readiness builds evidence-backed scoring inputs
  -> domain.target_scoring.score_and_rank_targets
  -> semantic BOM/refutation/valuation gates
  -> ranked target observations

source parser/GPT review records
  -> PersistSourceParsingArtifacts use case
  -> SourceParsingArtifactWriter port
  -> file-system or future database adapter
```

L3 source parsing and GPT-style review now have an explicit parser/reviewer seam:

```text
L3 source parsing jobs
  -> SourceMaterialParser port
  -> SourceExtractionReviewer port
  -> ParseL3SourceMaterials use case
  -> SourceParsingArtifactWriter port
  -> source_extractions.jsonl + leaf_source_reviews.jsonl
```

`SummarySourceMaterialParser` is the deterministic adapter for already-summarized materials. `DelegatingSourceMaterialParser` is the adapter shell for DeepSeek MCP or another external parser; the MCP runtime can inject the callable without changing application or domain code.

Source-universe selection is repository-backed and persisted on each leaf task:

```text
L3 question + domain playbook
  -> BuildLeafResearchTasksFromTree use case
  -> SourceUniverseRepository port
  -> FileSystemSourceUniverseRepository(config/source_universes.json)
  -> question-level source_universe_plan + direct/Exa search plan
```

The universe plan chooses where to search; it does not count as evidence. Every selected source still needs its own parse/review record before it can strengthen a conclusion.

Report writing is now port-backed while the current renderer is still the implementation:

```text
CLI command
  -> WriteStockProfessionalReport / WriteMetaQaProfessionalReport use case
  -> ProfessionalReportRenderer port
  -> ProfessionalReportRendererAdapter
  -> existing report_synthesis implementation
```

Leaf research CLI operations are port-backed while the current workflow implementation is still reused:

```text
CLI command
  -> BuildLeafResearchTasks / RunLeafResearch / ImportLeafResearchResults / SynthesizeLeafAnswers / RollupResearchAnswers
  -> LeafResearchWorkflow port
  -> LeafResearchWorkflowAdapter
  -> existing leaf_research implementation
```

The provider execution loop inside leaf research is also migrated:

```text
leaf tasks
  -> ExecuteLeafResearchTasks use case
  -> LeafResearchProvider port
  -> RawProviderResponseStore port
  -> normalized leaf result rows
```

Normalized leaf result persistence is also port-backed:

```text
normalized leaf result rows
  -> PersistLeafResearchResults use case
  -> LeafResearchResultRepository port
  -> FileSystemLeafResearchResultRepository
  -> merged leaf result JSONL + deduplicated source index JSONL
```

Leaf task/result/answer files now use a separate artifact repository:

```text
leaf research task/result/answer rows
  -> Load/Persist leaf research artifact use cases
  -> LeafResearchArtifactRepository port
  -> FileSystemLeafResearchArtifactRepository
  -> task JSONL + result JSONL + leaf answer JSONL + rollup answer JSONL
```

Leaf research transformation rules are now split from the compatibility entry point:

```text
QA tree
  -> domain.leaf_research_tasks.build_leaf_tasks_from_tree
  -> BuildLeafResearchTasksFromTree use case
  -> LeafResearchArtifactRepository

normalized provider results
  -> domain.leaf_answer_synthesis.synthesize_latest_leaf_answers
  -> SynthesizeLeafResearchAnswers use case
  -> leaf answer override JSONL

enriched QA tree
  -> domain.leaf_answer_synthesis.build_rollup_answer_rows
  -> BuildRollupResearchAnswers use case
  -> parent rollup JSONL
```

Provider-specific source parsing/search is also outside the compatibility module:

```text
leaf task
  -> research_search_providers adapter
  -> provider-specific network call / response parsing
  -> ExecuteLeafResearchTasks use case
  -> normalized provider result
```

`leaf_research.py` is now a compatibility facade for existing CLI/pipeline callers. It wires repositories, providers, and use cases, but no longer owns network provider prompts, provider response parsing, leaf task construction, leaf answer synthesis, or parent rollup construction.

Question architecture, report assembly, and canonical HTML rendering now have explicit seams:

```text
ResearchGoal
  -> PlanResearchGoal use case
  -> domain.resolve_domain_playbook + build_question_architecture
  -> QuestionArchitecture

research project files
  -> FileSystemResearchProjectRepository
  -> project.json + qa_tree.json + sources/evidence + investment_workbench.json
  -> BuildReportViewModel use case
  -> domain.report_view_model
  -> CanonicalHtmlReportRenderer
  -> report_sections section registry
  -> locked professional_report.html
```

This is the key decoupling for future iteration:

- Changing domain expertise or QA depth belongs in `domain_playbooks.py` or a future playbook adapter.
- Changing research sequencing belongs in `application/orchestration/research_orchestrator.py` and use cases.
- Changing public presentation belongs in `adapters/outbound/report_sections/` or another `CanonicalReportRenderer` adapter. The top-level renderer only assembles the page shell, CSS, and ordered section registry.
- Changing file layout belongs in `FileSystemResearchProjectRepository` or another `ResearchProjectRepository` adapter.
- Changing internal workbench field names belongs in `domain.report_view_model` normalization or the repository adapter, not in section HTML.

The public report renderer is intentionally split by section:

```text
CanonicalHtmlReportRenderer
  -> DEFAULT_REPORT_SECTIONS
  -> CurrentGoalSection
  -> IndustryOverviewSection
  -> TargetRecommendationsSection
  -> SourcesSection
```

The compact public default is exactly `当前研究的问题 -> 行业概况 -> 标的推荐 -> 来源索引`. Adaptive QA, search plans, parser traces, and workbench records remain internal unless explicitly requested. This is the presentation extension point: if only an industry-overview card changes, edit its section adapter and contract tests; do not change question planning, source parsing, target scoring, or file-system repositories. If the top-level order changes, update the section registry and the report contract together.

## Migration Map

| Compatibility area | Target home | Migration rule |
|---|---|---|
| `framework_contracts.py` validation rules | `domain/quality_gates.py` and focused domain services | Move gradually; keep compatibility imports until call sites are migrated. |
| `research_pipeline.py` | `application/orchestration/` | Orchestrates use cases only; no direct file or LLM calls. |
| `research_system.py` | split across domain/application/adapters | Extract pure rules first, then renderer and repository concerns. |
| `meta_qa_research.py` | QA use cases + renderer adapter | Separate question architecture, evidence synthesis, and HTML rendering. |
| `information_collection.py` | source planning use case + search/fetch adapters | Source plans are application; search/fetch are outbound adapters. |
| `leaf_research.py` | compatibility facade over leaf use cases/adapters | Provider execution, raw-response storage, task/result/answer files, merged result persistence, task construction, leaf answer synthesis, parent rollup construction, and provider prompts/parsing now live in domain/application/adapters. The workflow adapter and stock QA pipeline no longer call this module directly. |
| L3 source parsing | `ports/source_parsers.py` + `application/use_cases/parse_l3_source_materials.py` + parser adapters | Parser and reviewer are separate ports. DeepSeek/GPT review can plug in without touching leaf research, report rendering, or domain playbooks. |
| research question planning | `domain/research_goal.py`, `domain/domain_playbooks.py`, `domain/question_architecture.py` | New topics should start from `ResearchGoal -> DomainPlaybook -> QuestionArchitecture`, adaptively drilling to at most five layers, not from hard-coded report templates. |
| source-universe resolution | `ports/repositories.py` + `adapters/outbound/filesystem_source_universe.py` | Professional source selection is an outbound repository decision persisted per minimum question; report code must not hard-code it. |
| BOM semantic completion and target gates | `domain/bom_research_readiness.py` + `domain/target_scoring.py` | Search status alone is never completion. Per-source parsing, strengthening evidence, Q6 refutation, valuation, and canonical BOM mapping control score confidence and action-state caps. |
| report assembly | `domain/report_view_model.py` + `application/use_cases/build_report_view_model.py` | Report renderers should consume a stable ViewModel instead of reading project files directly. |
| canonical HTML rendering | `ports/renderers.py` + `adapters/outbound/canonical_html_report_renderer.py` + `adapters/outbound/report_sections/` | Frontend format changes should be isolated to section renderer adapters and report contract tests. |
| `llm.py` | `ports/llm.py` + outbound LLM adapters | Application depends on protocol, not vendor implementation. |
| `ingest_prices.py`, `ingest_sec.py` | outbound data adapters | Market and filing data enter through ports. |
| `cli.py` | inbound CLI adapter | Parse args, construct adapters, call use cases. Report validation, artifact validation, time-slice audit, and professional report writing now follow this path. |

## How To Add A New Capability

1. Define the domain object or policy if the capability changes research meaning.
2. Define a port if the capability needs external state, I/O, model calls, search, data, or rendering.
3. Write an application use case that depends only on domain and ports.
4. Implement one adapter for the current infrastructure.
5. Wire it through CLI or another inbound adapter.
6. Add tests at two levels:
   - use case test with in-memory/fake ports.
   - adapter/CLI test for file-system or command behavior.

## Quality Gates

Run these after each migration step:

```bash
PYTHONPATH=src python3 -m unittest
PYTHONPATH=src python3 -m value_invest_research validate-report-contract tests/fixtures/research_quality_gold/professional_report.html --require-l3
PYTHONPATH=src python3 -m value_invest_research validate-research-artifacts tests/fixtures/research_quality_gold --require-l3
```

Architecture-specific regression:

```bash
PYTHONPATH=src python3 -m unittest tests.test_hexagonal_architecture
```

## Next Slices To Migrate

Recommended order:

1. Implement a concrete DeepSeek runtime adapter for `SourceMaterialParser` when Python-side MCP invocation is available.
2. Split `research_pipeline.py` into a first-class application orchestrator with adapters for collection, synthesis, leaf research, and report writing.
3. `report_synthesis.py`: keep compatibility wrappers, but route refreshed reports through `ReportViewModel` and `CanonicalReportRenderer`.
4. Split `research_system.py` into QA tree repository, source binding service, and dashboard renderer.
5. Split `information_collection.py` into source planning, search/fetch adapters, and source-binding use cases.

Do not migrate by moving files wholesale. Move vertical slices that can be tested independently.
