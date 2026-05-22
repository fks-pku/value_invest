# Leaf-first Research Agent Design

Date: 2026-05-23

## Goal

Upgrade the foundation research system from a question-tree renderer plus local evidence matcher into a leaf-first research agent.

The durable research unit becomes the lowest-level question. Each leaf question should trigger a provider-agnostic research task, collect the most relevant external information, preserve source traceability, produce a detailed answer, and then roll the answer upward into parent questions, section pages, dashboards, and final reports.

The system remains file-system-first and does not issue trading instructions.

## Current Gap

The current research system already creates hierarchical questions under `stocks/<TICKER>/research_system/qa_tree.json` and renders L1/L2/L3 HTML pages.

The weak link is the bottom layer:

- Leaf questions mostly use local evidence matching.
- `collection_tasks.jsonl` records search intent but does not run professional search.
- `synthesized_answers.jsonl` can be deterministic and template-like because the underlying material is thin.
- Missing categories such as `research_report`, `message`, and `opinion` remain marked as gaps instead of being actively researched.

The desired system should treat each L3 question as a mini research assignment, not as a passive display node.

## Design Principles

- Leaf first: answer the smallest useful question before summarizing parent nodes.
- Provider agnostic: Perplexity, Tavily, Exa, OpenAI search, manual import, or a future in-house search service should all use the same internal contract.
- Source traceability: every material claim links back to source URLs and information-category records.
- Category discipline: every input is classified as `evidence`, `research_report`, `message`, or `opinion`.
- Facts before inference: leaf answers must separate facts, inferences, judgments, disconfirming evidence, and remaining gaps.
- Human review friendly: preserve raw provider output, normalized source records, synthesized answers, and rollup decisions as separate files.
- Incremental and resumable: rerunning a stock should skip completed leaf tasks unless inputs changed or the user requests refresh.

## Architecture

```text
qa_tree.json
  -> leaf research task builder
    -> provider-agnostic search interface
      -> provider adapters
        -> raw provider responses
    -> source normalizer
    -> information classifier
    -> leaf answer synthesizer
    -> node binder
  -> parent rollup synthesizer
  -> dashboard/report renderer
```

## Provider Interface

The first implementation should define a generic interface before binding to any one service.

```python
class ResearchSearchProvider:
    name: str

    def search(self, task: LeafResearchTask) -> ProviderSearchResult:
        raise NotImplementedError
```

The provider receives a structured leaf task and returns structured search results. Provider-specific clients live behind adapters.

Initial adapters:

- `manual`: reads imported JSONL results for offline testing and human-provided research.
- `mock`: deterministic adapter for unit tests.

Later adapters:

- `perplexity`
- `tavily`
- `exa`
- `openai_search`

## Leaf Research Task Contract

Each leaf task should include:

- `task_id`
- `ticker`
- `company_name`
- `node_id`
- `section_id`
- `question`
- `parent_question`
- `framework_context`
- `required_evidence`
- `disconfirming_signals`
- `decision_rule`
- `information_categories`
- `preferred_source_types`
- `time_scope`
- `max_sources`
- `refresh_policy`

The prompt sent to a provider should ask for:

- direct answer to the leaf question
- most relevant sources, with URLs and publication dates
- source classification into the four information buckets
- facts extracted from each source
- inferences and assumptions
- evidence that supports, refutes, or only leads
- missing data and next verification steps

## Provider Result Contract

Each provider result should include:

- `provider`
- `provider_model`
- `task_id`
- `node_id`
- `query`
- `executed_at`
- `raw_response_path`
- `sources`
- `answer`
- `facts`
- `inferences`
- `judgment`
- `supporting_evidence`
- `refuting_evidence`
- `research_leads`
- `gaps`
- `confidence`

Sources should include:

- `url`
- `title`
- `publisher`
- `author`
- `published_at`
- `accessed_at`
- `source_type`
- `information_category`
- `reliability`
- `materiality`
- `summary`
- `quoted_or_extracted_points`

## Files

Under `stocks/<TICKER>/research_system/`:

- `leaf_research_tasks.jsonl`: one task per leaf question and information gap.
- `leaf_research_results.jsonl`: normalized provider results.
- `leaf_research_raw/`: raw provider responses, one file per task run.
- `leaf_research_sources.jsonl`: normalized source records.
- `leaf_answers.jsonl`: detailed answer per leaf node.
- `rollup_answers.jsonl`: synthesized L2/L1/section answers.
- `pipeline_run.json`: records provider, mode, counts, failures, and refresh policy.

Existing files should remain:

- `qa_tree.json`
- `information_collection.jsonl`
- `synthesized_answers.jsonl`
- `research_dashboard.html`
- `professional_report.html`

The new files become the richer input layer; existing renderers can read from them.

## Workflow

1. Build or update the foundation system with `build-research-system`.
2. Build leaf research tasks from open L3 nodes and category gaps.
3. Run tasks through a configured provider.
4. Store raw provider output.
5. Normalize sources and classify each source into one information bucket.
6. Generate a detailed answer for each leaf node.
7. Bind sources and leaf answers back to `qa_tree.json` and `information_collection.jsonl`.
8. Roll up child answers into parent answers.
9. Regenerate dashboard and reports.

## CLI Shape

Proposed commands:

```powershell
value-invest-research build-leaf-research-tasks INTC
value-invest-research run-leaf-research INTC --provider manual --input path\to\results.jsonl
value-invest-research run-leaf-research INTC --provider mock
value-invest-research import-leaf-research-results INTC --path path\to\results.jsonl
value-invest-research synthesize-leaf-answers INTC
value-invest-research rollup-research-answers INTC
```

The existing pipeline can later expose:

```powershell
value-invest-research run-stock-qa-pipeline INTC --leaf-research-provider perplexity
```

## Error Handling

- Missing provider credentials should fail with clear setup guidance.
- Provider timeouts should write failed task rows and allow resume.
- Duplicate URLs should be deduplicated while preserving node bindings.
- Low-reliability sources should be saved as leads, not thesis-strengthening evidence.
- Any provider answer without citations should be rejected or marked incomplete.
- If a leaf answer has no primary or high-reliability support, parent rollup must keep the conclusion provisional.

## Testing

Unit tests should cover:

- building leaf tasks from `qa_tree.json`
- provider interface with mock adapter
- importing manual results
- source classification and deduplication
- binding results to leaf nodes
- preserving facts/inferences/judgments separately
- rollup behavior when leaf evidence is weak or contradictory
- CLI output paths and resume behavior

Integration tests should use the mock adapter and a small sample stock fixture.

## First Implementation Slice

The first slice should not call a paid external API.

It should implement:

- generic data models
- task builder
- mock provider
- manual import provider
- result normalizer
- leaf answer writer
- basic rollup writer
- dashboard rendering of richer leaf research fields
- tests

After that is stable, a Perplexity adapter can be added behind the same interface.

## Success Criteria

- A stock with an existing `qa_tree.json` can generate leaf research tasks.
- Each L3 page can show detailed leaf answers sourced from `leaf_answers.jsonl`.
- Raw and normalized source records are preserved separately.
- The system can run with `mock` or `manual` provider without external credentials.
- The implementation does not hard-code Perplexity-specific fields into core schemas.
- Existing foundation dashboard generation continues to work.
