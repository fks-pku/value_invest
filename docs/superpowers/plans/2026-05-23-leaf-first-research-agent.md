# Leaf-first Research Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first working Leaf-first Research Agent: leaf question tasks, provider-agnostic results, source normalization, leaf answers, parent rollups, CLI commands, and dashboard integration.

**Architecture:** Add a focused `leaf_research.py` module that reads existing `qa_tree.json` and writes the new leaf research files. Keep provider adapters behind one interface; the first slice supports `mock` and `manual`, so external search providers can be added later without schema churn. Existing `research_system.py` remains the renderer and will load leaf answers as node-level overrides before rollup.

**Tech Stack:** Python standard library, unittest, JSON/JSONL file artifacts, existing `value_invest_research` CLI and research-system helpers.

**Implementation status (2026-05-23):** Implemented the Leaf-first task builder, provider interface, mock/manual import, Perplexity adapter, generic OpenAI-compatible adapter, source normalization, incremental batch accumulation, leaf answer synthesis, rollup integration, CLI commands, stock QA pipeline flags, and L3 source rendering. Verified with `python tools/run_tests.py` and INTC QA validation; live external-provider execution still requires configuring provider API keys.

---

### Task 1: Leaf Research Data Models And Task Builder

**Files:**
- Create: `src/value_invest_research/leaf_research.py`
- Create: `tests/test_leaf_research.py`

- [ ] **Step 1: Write failing tests for task generation**

Add tests that seed a stock, run `build_research_system`, call `build_leaf_research_tasks`, and assert:

```python
tasks = _read_jsonl(research_dir / "leaf_research_tasks.jsonl")
self.assertEqual(result["tasks"], 2)
self.assertEqual(tasks[0]["ticker"], "XIAOMI")
self.assertIn("question", tasks[0])
self.assertIn("required_evidence", tasks[0])
self.assertEqual(tasks[0]["information_categories"], ["evidence", "research_report", "message", "opinion"])
self.assertTrue(tasks[0]["task_id"].startswith("leaf_"))
```

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_leaf_research
```

Expected: fail because `value_invest_research.leaf_research` does not exist.

- [ ] **Step 2: Implement minimal models and task builder**

Create `leaf_research.py` with:

- constants for `LEAF_TASK_FILE`, `LEAF_RESULT_FILE`, `LEAF_SOURCE_FILE`, `LEAF_ANSWER_FILE`, `ROLLUP_ANSWER_FILE`
- `build_leaf_research_tasks(root, ticker, limit=None, include_completed=False)`
- helpers to read `qa_tree.json`, identify leaf nodes, build stable `task_id`, and write JSONL

- [ ] **Step 3: Verify green**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_leaf_research
```

Expected: task-builder tests pass.

### Task 2: Mock And Manual Provider Interface

**Files:**
- Modify: `src/value_invest_research/leaf_research.py`
- Modify: `tests/test_leaf_research.py`

- [ ] **Step 1: Write failing tests for provider execution**

Add tests for:

```python
result = run_leaf_research(root, "XIAOMI", provider="mock", limit=1)
self.assertEqual(result["provider"], "mock")
self.assertEqual(result["results"], 1)
self.assertTrue((research_dir / "leaf_research_raw").exists())
self.assertTrue((research_dir / "leaf_research_results.jsonl").exists())
rows = _read_jsonl(research_dir / "leaf_research_results.jsonl")
self.assertEqual(rows[0]["provider"], "mock")
self.assertEqual(rows[0]["sources"][0]["information_category"], "research_report")
```

Add manual import test:

```python
manual_path.write_text(json.dumps({...}, ensure_ascii=False) + "\n", encoding="utf-8")
result = import_leaf_research_results(root, "XIAOMI", manual_path)
self.assertEqual(result["records"], 1)
self.assertEqual(result["sources"], 1)
```

Run tests and watch failures for missing functions.

- [ ] **Step 2: Implement provider interface**

Add:

- `ResearchSearchProvider`
- `MockResearchSearchProvider`
- `run_leaf_research(root, ticker, provider="mock", input_path=None, limit=None)`
- `import_leaf_research_results(root, ticker, path)`

The mock provider returns one cited source and a structured answer for each task. Manual provider imports JSONL rows matching the provider result contract.

- [ ] **Step 3: Verify green**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_leaf_research
```

Expected: provider and manual import tests pass.

### Task 3: Source Normalization, Deduplication, And Leaf Answers

**Files:**
- Modify: `src/value_invest_research/leaf_research.py`
- Modify: `tests/test_leaf_research.py`

- [ ] **Step 1: Write failing tests for normalized sources and leaf answers**

Assert that importing two results with the same URL writes one normalized source row but preserves both node bindings:

```python
sources = _read_jsonl(research_dir / "leaf_research_sources.jsonl")
self.assertEqual(len(sources), 1)
self.assertEqual(sorted(sources[0]["node_ids"]), sorted([node_a, node_b]))
```

Assert `synthesize_leaf_answers(root, "XIAOMI")` writes `leaf_answers.jsonl` with:

```python
self.assertIn("facts", answer)
self.assertIn("inferences", answer)
self.assertIn("judgment", answer)
self.assertIn("supporting_evidence", answer)
self.assertEqual(answer["node_id"], node_a)
```

- [ ] **Step 2: Implement normalization and leaf answer synthesis**

Add:

- `_normalize_provider_result`
- `_normalize_source`
- `_write_normalized_sources`
- `synthesize_leaf_answers(root, ticker)`

Low-reliability sources should be listed as `research_leads`, not strengthening evidence.

- [ ] **Step 3: Verify green**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_leaf_research
```

Expected: source and answer tests pass.

### Task 4: Bind Leaf Answers Into QA Tree And Roll Up Parents

**Files:**
- Modify: `src/value_invest_research/leaf_research.py`
- Modify: `src/value_invest_research/research_system.py`
- Modify: `tests/test_leaf_research.py`

- [ ] **Step 1: Write failing tests for binding and rollup**

After leaf answers exist, rebuild the research system and assert:

```python
qa_tree = json.loads((research_dir / "qa_tree.json").read_text(encoding="utf-8"))
node = next(item for item in qa_tree["nodes"] if item["id"] == target_node)
self.assertEqual(node["professional_answer"]["source"], "leaf_research")
self.assertIn("Mock answer", node["professional_answer"]["answer"])
parent = next(item for item in qa_tree["nodes"] if item["id"] == node["parent_id"])
self.assertIn("leaf_research", parent["metadata"]["rollup_sources"])
```

- [ ] **Step 2: Implement leaf answer loading**

In `research_system.py`, load `leaf_answers.jsonl` from `research_dir` and apply those answers after existing synthesis overrides, then call rollup. Preserve existing synthesis override behavior for non-leaf nodes.

Add `rollup_research_answers(root, ticker)` in `leaf_research.py` to write `rollup_answers.jsonl` from the current rebuilt `qa_tree.json`.

- [ ] **Step 3: Verify green**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_leaf_research tests.test_research_system
```

Expected: existing research-system behavior still passes.

### Task 5: CLI Commands

**Files:**
- Modify: `src/value_invest_research/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing CLI tests**

Add tests for:

```python
main(["--root", str(tmp), "build-leaf-research-tasks", "XIAOMI", "--limit", "2"])
main(["--root", str(tmp), "run-leaf-research", "XIAOMI", "--provider", "mock", "--limit", "1"])
main(["--root", str(tmp), "synthesize-leaf-answers", "XIAOMI"])
main(["--root", str(tmp), "rollup-research-answers", "XIAOMI"])
```

Assert output includes file paths:

- `leaf_research_tasks.jsonl`
- `leaf_research_results.jsonl`
- `leaf_answers.jsonl`
- `rollup_answers.jsonl`

- [ ] **Step 2: Add parser entries and command handlers**

Add CLI parser commands:

- `build-leaf-research-tasks`
- `run-leaf-research`
- `import-leaf-research-results`
- `synthesize-leaf-answers`
- `rollup-research-answers`

Handlers import functions from `leaf_research.py` and print concise paths/counts.

- [ ] **Step 3: Verify green**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_cli tests.test_leaf_research
```

Expected: CLI tests pass.

### Task 6: Pipeline Flag And Final Verification

**Files:**
- Modify: `src/value_invest_research/cli.py`
- Modify: `src/value_invest_research/research_pipeline.py`
- Modify: `tests/test_cli.py`
- Test: `tests/test_research_pipeline.py`

- [ ] **Step 1: Write failing tests for pipeline integration**

Assert:

```python
main([
    "--root", str(tmp),
    "run-stock-qa-pipeline", "XIAOMI",
    "--leaf-research-provider", "mock",
    "--leaf-research-limit", "1",
])
```

creates:

- `leaf_research_tasks.jsonl`
- `leaf_research_results.jsonl`
- `leaf_answers.jsonl`
- `rollup_answers.jsonl`

- [ ] **Step 2: Implement pipeline integration**

Add optional pipeline args:

- `--leaf-research-provider`
- `--leaf-research-input`
- `--leaf-research-limit`

When provided, run task builder, provider execution/import, leaf answer synthesis, rollup, and refresh reports.

- [ ] **Step 3: Run final tests**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_leaf_research tests.test_cli tests.test_research_system tests.test_research_pipeline
```

Expected: all selected tests pass.

### Task 7: Run On INTC Smoke Test

**Files:**
- Generated: `stocks/INTC/research_system/leaf_research_tasks.jsonl`
- Generated: `stocks/INTC/research_system/leaf_research_results.jsonl`
- Generated: `stocks/INTC/research_system/leaf_research_sources.jsonl`
- Generated: `stocks/INTC/research_system/leaf_answers.jsonl`
- Generated: `stocks/INTC/research_system/rollup_answers.jsonl`

- [ ] **Step 1: Run mock provider on a narrow INTC slice**

Run:

```powershell
$env:PYTHONPATH='src'; python -m value_invest_research build-leaf-research-tasks INTC --limit 3
$env:PYTHONPATH='src'; python -m value_invest_research run-leaf-research INTC --provider mock --limit 3
$env:PYTHONPATH='src'; python -m value_invest_research synthesize-leaf-answers INTC
$env:PYTHONPATH='src'; python -m value_invest_research rollup-research-answers INTC
```

Expected: new leaf research files appear and the generated L3 pages show leaf-research answers where available.

- [ ] **Step 2: Validate existing QA system**

Run:

```powershell
$env:PYTHONPATH='src'; python -m value_invest_research validate-qa-system INTC --require-professional-report
```

Expected: validation passes.

### Task 8: Perplexity-compatible Search Provider

**Files:**
- Modify: `src/value_invest_research/leaf_research.py`
- Modify: `src/value_invest_research/cli.py`
- Modify: `tests/test_leaf_research.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing tests for a real search provider adapter**

Assert `provider="perplexity"` fails clearly without `PERPLEXITY_API_KEY`, and assert a fake OpenAI-compatible HTTP response writes:

- `leaf_research_raw/<task_id>.json`
- `leaf_research_results.jsonl`
- `leaf_research_sources.jsonl`

The fake response should include `choices[0].message.content`, `search_results`, and `citations`.

- [ ] **Step 2: Implement the adapter**

Add `PerplexityResearchSearchProvider` behind the existing provider interface. It should:

- read `PERPLEXITY_API_KEY`
- default to `PERPLEXITY_MODEL=sonar-pro`
- default to `PERPLEXITY_BASE_URL=https://api.perplexity.ai`
- call the OpenAI-compatible `/chat/completions` endpoint
- ask for strict JSON following the leaf research result contract
- preserve the raw provider response
- parse cited sources into the existing four information buckets

- [ ] **Step 3: Expose through CLI and pipeline**

Add `perplexity` to allowed provider choices for:

- `run-leaf-research --provider perplexity`
- `run-stock-qa-pipeline --leaf-research-provider perplexity`

- [ ] **Step 4: Verify**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_leaf_research tests.test_cli tests.test_research_pipeline
```

Expected: tests pass without making a live Perplexity API call.

### Task 9: Generic OpenAI-compatible Provider

**Files:**
- Modify: `src/value_invest_research/leaf_research.py`
- Modify: `src/value_invest_research/cli.py`
- Modify: `tests/test_leaf_research.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing tests for provider-agnostic HTTP search**

Assert `provider="openai_compatible"`:

- fails clearly without `LEAF_RESEARCH_API_KEY`
- reads `LEAF_RESEARCH_BASE_URL`
- reads `LEAF_RESEARCH_MODEL`
- optionally uses `LEAF_RESEARCH_PROVIDER_NAME` for normalized output rows
- writes normalized provider results and sources from a fake chat-completions response

- [ ] **Step 2: Extract common chat-completions logic**

Move the shared request/response logic into `OpenAICompatibleResearchSearchProvider`. Keep Perplexity as a thin configured subclass using:

- `PERPLEXITY_API_KEY`
- `PERPLEXITY_MODEL`
- `PERPLEXITY_BASE_URL`
- `PERPLEXITY_ENDPOINT`
- `PERPLEXITY_TIMEOUT`

- [ ] **Step 3: Expose through CLI and pipeline**

Add `openai_compatible` to allowed provider choices for:

- `run-leaf-research --provider openai_compatible`
- `run-stock-qa-pipeline --leaf-research-provider openai_compatible`

- [ ] **Step 4: Verify**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_leaf_research tests.test_cli tests.test_research_pipeline
python tools/run_tests.py
```

Expected: tests pass without making a live external API call.
