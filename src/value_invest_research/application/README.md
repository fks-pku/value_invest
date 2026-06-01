# Application Layer

The application layer coordinates use cases.

Allowed:

- orchestrating domain services
- calling ports
- returning stable result objects

Forbidden:

- direct file reads/writes
- direct model/vendor calls
- direct HTML rendering implementation
- imports from `adapters`

Use cases should be testable with in-memory ports.

Canonical research flow:

1. `PlanResearchGoal` converts `ResearchGoal` into `QuestionArchitecture`.
2. Evidence collection and source parsing fill project artifacts behind repository ports.
3. `BuildReportViewModel` assembles public report data from a `ResearchProjectRepository`.
4. `RenderResearchProjectReport` writes the report through a `CanonicalReportRenderer`.

Leaf research flow:

1. `BuildLeafResearchTasksFromTree` persists provider-agnostic leaf tasks from a QA tree.
2. `ExecuteLeafResearchTasks` runs a provider adapter and stores raw responses through ports.
3. `PersistLeafResearchResults` merges normalized provider results and source indexes.
4. `SynthesizeLeafResearchAnswers` converts results into leaf answer overrides.
5. `BuildRollupResearchAnswers` creates parent rollup rows from the enriched QA tree.

Source parsing flow:

1. `ParseL3SourceMaterials` receives L3 source jobs from orchestration.
2. A `SourceMaterialParser` adapter extracts structured source facts.
3. A `SourceExtractionReviewer` adapter verifies whether the extraction may strengthen conclusions.
4. `SourceParsingArtifactWriter` persists `source_extractions.jsonl` and `leaf_source_reviews.jsonl`.

Application orchestration may sequence these use cases, but must not own domain
question design, direct file I/O, model/vendor calls, or HTML implementation.
