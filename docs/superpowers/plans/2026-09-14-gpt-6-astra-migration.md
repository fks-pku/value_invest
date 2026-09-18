**GPT-6 Astra migration plan — Value Invest Research**

Prepared 2026-09-14. Status: proposed implementation plan; no runtime migration or paid API evaluation has been performed.

Migrate the project's Python model integrations to `gpt-6-astra`, using the existing research contracts as acceptance criteria. This scope concerns the application runtime; the Codex task's selected model is a separate setting. Introduce Astra behind explicit provider configuration, validate it on isolated research copies, then change defaults. Keep alternative search providers and optional first-pass readers available for their existing roles.

**Verified starting point**

| Surface | Checked-in behavior | Migration implication |
| --- | --- | --- |
| [General LLM client](/Users/bytedance/Desktop/vk/value_invest/src/value_invest_research/llm.py:13) | Defaults to `glm-5.1` on Z.ai; both methods use Chat Completions, `max_tokens=4096`, and `temperature=0.3`. | Add an Astra request path and preserve the callers' text-returning interface. |
| [CLI configuration](/Users/bytedance/Desktop/vk/value_invest/src/value_invest_research/cli.py:440) | Many planner, synthesis, report, memo, stock, event, and sector commands repeat GLM/Z.ai defaults. `_get_llm_client` constructs its own config. | Changing `LlmConfig.from_env()` alone will not migrate these commands. |
| [Research providers](/Users/bytedance/Desktop/vk/value_invest/src/value_invest_research/adapters/outbound/research_search_providers.py:62) | Separate generic Chat Completions provider sends `temperature=0.2`, defaults to placeholder `search-model`, and parses `choices`. Perplexity inherits this implementation; Exa is separate. | Add a distinct OpenAI Responses search adapter. Preserve the existing providers' protocols. |
| [Parser/reviewer boundary](/Users/bytedance/Desktop/vk/value_invest/src/value_invest_research/ports/source_parsers.py:24) | Separate parser and reviewer protocols exist. Implementations include a delegate shell and a pass-through reviewer for already-verified input. | Automated Astra source review needs a concrete adapter and runtime wiring; a model-name change cannot provide it. |
| [Dependencies](/Users/bytedance/Desktop/vk/value_invest/pyproject.toml:5) | Python `>=3.11`; optional LLM extra declares `openai>=1.0.0`. The inspected shell runs Python 3.9.6. | Select a supported interpreter and validate an SDK version that supports the actual Responses fields used. |
| [Research instructions](/Users/bytedance/Desktop/vk/value_invest/AGENTS.md:1) | Evidence gates, publication-time discipline, append-only ledgers, and canonical rendering govern completion. | Treat these as invariants throughout migration. |

These are source-code defaults, not claims about private environment overrides or account access. Seven inspected modules call the general client's `chat()` method: stock, event, sector, memo, question planning, answer synthesis, and report synthesis. No repository `.codex` configuration was found.

**Official compatibility baseline**

Astra's exact API identifier is `gpt-6-astra`. Supported API reasoning efforts are `low`, `medium`, `high`, `xhigh`, and `max`. Tool calling requires Responses; text-only Chat Completions remains supported. Remove `temperature`, `top_p`, and `top_logprobs` on Astra requests. The migration guide also calls for auditing instruction files for conflicting guidance. [Astra migration guidance](https://developers.openai.com/api/docs/guides/latest-model), [model specification](https://developers.openai.com/api/docs/models/gpt-6-astra).

The Responses adapter should use `input` and the SDK's `output_text` accessor. Explicitly select storage behavior; propose `store=false` for the initial stateless implementation, with local artifacts remaining authoritative. [Responses migration guide](https://developers.openai.com/api/docs/guides/migrate-to-responses).

**1. Establish a reproducible baseline and shared configuration**

Create a small provider configuration under `config/llm_providers.json` and a loader at the adapter/composition boundary. These are proposed new files. Store provider, model, API mode, endpoint, reasoning effort, output budget, timeout, and environment-variable names for credentials; never store credential values.

Use explicit CLI options first, environment overrides second, and the selected configuration profile last. Make argparse defaults optional so they cannot mask environment/configuration values. Maintain compatibility with existing `LLM_*` and `LEAF_RESEARCH_*` settings, scoped to the selected provider; document OpenAI authentication separately and never reuse another provider's credential implicitly. Retain an explicit GLM profile for rollback.

Route planning, synthesis, report drafting, and review separately even when they select the same Astra model. The present client has no configured reasoning effort to preserve. Use `medium` as a proposed initial general-purpose setting, then compare `low` and `high` by workload before choosing defaults. Keep search-provider selection independent.

Capture baseline prompts, input/source hashes, output artifacts, config, commit, Python/SDK versions, and existing test results. Record pre-existing failures separately. Use Python 3.11+ with the project's declared dependencies, including `pypdf`; update the SDK requirement only to a version actually validated during implementation.

Exit condition: every affected CLI command resolves the intended provider/model consistently, explicit overrides work, and the baseline is reproducible.

**2. Add a Responses client without breaking existing callers**

Implement the OpenAI client in `adapters/outbound/`, leaving `llm.py` as a compatibility facade. Preserve `chat(system_prompt, user_prompt) -> str` and `chat_with_context(messages) -> str`, including message order and instruction roles. Provider-specific SDK calls must stay outside application/domain code, following the [architecture contract](/Users/bytedance/Desktop/vk/value_invest/docs/architecture/hexagonal_research_system.md:7).

For Astra, use `responses.create`, explicit reasoning, and `max_output_tokens`. Treat output budgets as workload-specific: the old 4,096-token cap should be evaluated for truncation before adoption. Structured Outputs documentation demonstrates this field and incomplete-response handling. [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs).

Reject refusals, incomplete responses, and empty output as unsuccessful generation. Use bounded retries for transient failures; expose authentication, schema, and unsupported-parameter errors clearly. Avoid nested retry loops. A deterministic fallback must remain labeled as fallback, not recorded as an Astra success.

Record requested/returned model, response/request identifiers when available, prompt version, token usage, latency, retry count, and terminal status in internal run telemetry. Keep telemetry separate from evidence claims and public reports. Do not invent dated model snapshots or overwrite historic provider metadata.

Exit condition: mocked transport tests cover valid text, context ordering, unsupported-parameter omission, refusal, truncation, and errors; all existing callers keep their output contracts.

**3. Introduce Astra research search as a separate provider**

Add `OpenAIResponsesResearchSearchProvider` implementing `LeafResearchProvider`, register an explicit provider name such as `openai_responses`, and expose it in the BOM, leaf, and stock-pipeline CLI choices. Do not send Astra requests through Perplexity's inherited adapter.

Use Responses `web_search` for discovery. Preserve tool-call evidence, URL citation annotations, and the consulted-source list via `web_search_call.action.sources`; citations displayed publicly must stay clickable. [Web search documentation](https://developers.openai.com/api/docs/guides/tools-web-search).

Create a Responses-specific normalizer. Only retrieved URLs or explicitly supplied local-source IDs can become source candidates; model-written URLs alone are insufficient. Keep discovery separate from parsing and verification. If a discovery run performs no search, record that outcome rather than labeling it completed collection.

Pass the current terminal question's full context to the adapter: cutoff, source universe, refuting search plan, `l3_plan_id`, `l3_node_id`, `question_node_id`, `question_level`, `research_step_id`, and `search_run_id`. The existing compact generic prompt omits several of these; the BOM search call also needs explicit context forwarding. Copy identity fields from trusted task metadata rather than asking the model to regenerate them.

For backtests, use verified material visible at the cutoff for evidence and synthesis. Live search can discover candidates but cannot itself establish historical visibility; quarantine unknown or post-cutoff publication dates before parsing. A newer model's prior knowledge must not supply missing historical facts. Keep IMA's attended directory archive workflow and local publication-date verification intact.

Exit condition: one real search can be traced to one active question and its candidate intake; missing dates, invented citations, and search failures cannot complete an evidence step.

**4. Preserve structured outputs and make review substantive**

First preserve each existing output shape. Some callers expect Markdown containing a JSON block; others expect pure JSON. Do not force every caller into a universal schema during the client migration.

For new extraction/review adapters and existing pure-JSON tasks, define explicit schemas with Structured Outputs and local semantic validation. Schema conformance does not prove source accuracy. [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs).

Implement an Astra `SourceExtractionReviewer` that receives the original source text/page locators, the extraction, and the exact question. Verify numbers, dates, fact-versus-forecast classification, relevance, and support/refute direction; record adopted and rejected claims plus corrections. Wire it through `ParseL3SourceMaterials`. Add an Astra parser only when replacing a reader is part of the selected rollout. Optional DeepSeek first-pass reading remains a distinct role.

Do not use `PassThroughSourceExtractionReviewer` as verification of fresh model output. Missing originals or unresolved evidence must produce a blocked/pending review. Preserve separate extraction and review IDs even if Astra performs both calls, and evaluate the reviewer against independently labeled examples.

Audit the active prompts, `AGENTS.md`, and `dynamic-research-agent` instructions together. Preserve initial L1/L2/L3 planning, gap-triggered L4/L5 expansion, source-specific review, four time fields, append-only events, refutation, and target gates. Standalone BOM states use evidence conditions and gaps, not confidence scores; legacy provider confidence fields must not become a public completion signal.

Exit condition: the pipeline can demonstrate a genuine source review and reject a plausible but unsupported claim. The core client migration can ship separately, but cannot be described as full automated research-review migration until this gate passes.

**5. Evaluate before changing defaults**

Build a fixed, independently reviewed set of approximately 30 cases spanning planning, extraction, contradiction handling, answer synthesis, report output, and failure handling. Include Chinese and English sources, unknown publication dates, forecasts mistaken for actuals, misleading search snippets, unsupported company exposure, missing valuation/refutation, and instructions embedded in source text. Run the baseline and Astra against identical approved inputs; repeat the highest-risk cases to detect variability.

Acceptance gates:

- All affected contract/transport tests pass; no new architecture or report-contract regression.
- Every promoted claim retains source, extraction, review, question, and step lineage.
- Zero accepted post-cutoff facts, fabricated citations, or completion/`actionable_long` upgrades without required evidence in the evaluation set.
- A completed/blocked/expanded decision matches the independently reviewed expectations; disagreements remain explicit failures or reviewed exceptions.
- Report claims match their audit sidecars; source links and the applicable public presentation profile remain valid.
- Quality does not regress against the baseline. Measure cost per accepted answer and median/p95 latency by workload; set the operating budget before live evaluation and use it as a cutover gate.

Run focused tests first: new client/provider tests plus existing `test_cli`, `test_leaf_research`, affected researcher/synthesis tests, `test_hexagonal_architecture`, `test_l3_research_plan`, `test_research_plan`, `test_temporal_research`, and `test_research_semantic_gates`. Include standalone/report-contract suites when those paths change. Run `python tools/run_tests.py` once under the supported interpreter before cutover; resolve or explicitly account for baseline failures.

Current Standard token rates are $10/M input, $1/M cached input, $12.50/M cache writes, and $50/M output. Requests above 272K input tokens have higher full-request rates; tools have separate charges. Use actual usage, including retries and review calls, to estimate the cost per accepted research result. [Astra pricing](https://developers.openai.com/api/docs/models/gpt-6-astra).

**6. Roll out by workload with a tested rollback**

Verify the target OpenAI project's model access, credentials, and limits with a small smoke test during implementation. Access has not been tested for this plan. Begin with isolated copies of one stock project and one standalone BOM project. Compare Astra output to the baseline without promoting experimental artifacts into their canonical ledgers.

Enable the general client first, then research search, then substantive source review. Change the default profile only after the relevant evaluation gates pass. Keep deterministic renderers, search alternatives, historical records, and explicit fallback profiles intact. Update README installation/configuration instructions and add the migration runbook alongside the implementation.

Rollback selects the previous provider profile for subsequent runs. Preserve all experimental results and failed attempts under their own run IDs. If a bad result was already promoted, use the repository's append-only reopening/correction process; do not rewrite old research history. Test rollback before default cutover.

Async tools, mid-turn steering, remote MCP orchestration, and caching optimizations are follow-up projects, not prerequisites for this migration. Finish by recording the selected model/effort per workload, tested SDK version, evaluation results, measured cost/latency, and rollback evidence.

**Suggested implementation sequence**

| Change set | Deliverable | Dependency |
| --- | --- | --- |
| A | Baseline, provider config, Responses client, CLI resolution, client tests | Supported runtime and validated SDK |
| B | Astra search provider, response normalization, full question/cutoff trace, provider tests | A |
| C | Concrete source reviewer, optional parser, scoped schemas/prompt updates, review tests | A; B for live-search integration |
| D | Paired evaluations, isolated canaries, documented budget, default cutover, rollback runbook | Relevant A–C gates pass |

Planning validation was read-only inspection of code, contracts, and current official OpenAI documentation. No test suite, model-access probe, paid model call, or research rerun was executed while preparing this document.
