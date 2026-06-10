# Four-Stage Serial Research Pipeline Design

**Date**: 2026-06-10
**Status**: draft

## Problem

The current research framework has a complete data model, validation layer, and HTML renderer, but the actual execution is fragmented. Key gaps:

1. **行业空间 (Industry Space) module is never populated** — the renderer falls back to a "BOM 子系统待拆分" placeholder because no workflow produces `industry_space_evidence_pack` data.
2. **QA tree is hand-written, not derived from the industry overview** — no causal link from the supply chain map and data gaps to the decision questions.
3. **No automated search execution** — `source_plan` defines what to search but no LLM actually executes searches against source universes and the web.
4. **"思考→搜索→解析" loop is absent** — each minimum research unit (BOM node, L3 leaf question) lacks a self-contained think/search/parse cycle.

The framework is a data model + validation layer, not an end-to-end LLM-driven research pipeline.

## Goal

Transform the research workflow into a four-stage serial pipeline where the LLM behaves like a professional analyst:

1. Define the research problem
2. Build the industry overview (five modules), where each minimum unit self-completes via "think → search → parse"
3. Grow a QA tree from the overview's data gaps, where each leaf question self-completes via "think → search → parse"
4. Synthesize target recommendations from verified conclusions only

Each stage has a hard CLI gate — it cannot be skipped and must pass before the next stage begins.

## Design

### Part 1: Four-Stage Pipeline

```
Stage 1: 定义研究问题
    │  Gate: validate-project-schema
    │  Output: project.json (research_type, domain_playbook, as_of_date, object_id)
    ▼
Stage 2: 行业概况 (五个模块)
    │  Gate: validate-industry-overview
    │  Output: supply_chain data + industry_space_evidence_pack +
    │          competition data + chokepoint data + pending_questions
    ▼
Stage 3: 针对性 QA 树
    │  Gate: validate-research-artifacts --require-l3
    │  Output: qa_tree.json + source_extractions.jsonl + leaf_source_reviews.jsonl
    ▼
Stage 4: 标的推荐
       Gate: validate-report-contract --require-l3
       Output: frozen_recommendations.json → labeled_recommendations.json (if backtest)
```

Degenerate paths:
- If a research type has no investment implications, Stage 4 produces a "no actionable target" statement, not fake recommendations.
- If domain_playbook says a module is not applicable (e.g. event research doesn't need BOM space), skip that module but still pass the gate with explicit reason.

### Part 2: Stage 2 — Industry Overview Decomposition

#### Module 1: 产业链与生态位

| Sub-unit | Search target | Output fields |
|----------|--------------|---------------|
| 1.1 Lane/swimlane map | Industry reports, company IR, third-party chain maps | `layers[].players, products, value_flow` |
| 1.2 Value flow | Company segment breakdowns, customer capex announcements | `flow_steps[]` (plain-language Chinese steps) |
| 1.3 BOM/component chain | SemiAnalysis/STH BOM teardowns, product pages | `component_value_chain[].subsystem, component, companies, input, output, metric` |

Each sub-unit runs independently and writes its portion of the chain data, not requiring all sub-units to finish before progressing.

#### Module 2: 行业空间 ← Primary execution target

Each BOM node is an independent minimum research unit:

```
BOM node (e.g. "HBM memory")
    │
    ├─ Think: LLM writes source_plan with 5 public-method buckets:
    │     Each bucket: search_query, expected_fields, priority_sources,
    │     directed_queries, preferred_parser_skill
    │     Priority_sources drawn from config/source_universes.json
    │
    ├─ Search (5 buckets, may execute sequentially or with parallel search calls):
    │     ├─ 公司指引: company IR, earnings call transcripts
    │     ├─ 公司 TAM: investor day slides, 10-K market sections
    │     ├─ 客户侧指引: downstream capex guidance, RPO
    │     ├─ 第三方拆法: SemiAnalysis, TrendForce, Omdia, Dell'Oro, LightCounting etc.
    │     └─ 财务兑现证据: segment revenue, backlog, margin data
    │     Search uses web_search_prime + webfetch (primary) or web-reader.
    │     Collected materials → sources.jsonl (with source_visible_at, cutoff_status)
    │
    ├─ Parse: DeepSeek MCP reads materials per bucket
    │     → source_extractions.jsonl (fills schema_fields)
    │     → GPT verification → leaf_source_reviews.jsonl
    │
    └─ Write node answer:
          node, coreQuestion
          publicSizingMethods (5 categories, each with source_ids + entry details)
          space_horizon: short/mid/long size + confidence
          facts, inferenceChain
          node-level source_ids
```

**5 public-method card contract (per entry)**:
```
space-method-entry:
  公司或机构, 指引内容, BOM 节点, 时间范围, 可验证指标, 置信度
  + space-method-entry-sources (source chips)
```

If a category has no material after 3 rounds of directed search → `status=gap` + `gap_reason`.
GPT must not create a proprietary TAM estimate to fill a gap.

#### Module 3: 竞争格局与利润池

| Sub-unit | Search target | Output |
|----------|--------------|--------|
| Per chain node: competitor map | Company IR market share, third-party reports | Who competes, substitution path, pricing power |
| Technology route matrix (when applicable) | Tech comparison reports, roadmap disclosures | route, best-fit, solved constraint, tradeoff, timing, beneficiaries, refuting trigger |

#### Module 4: 瓶颈点

| Sub-unit | Output |
|----------|--------|
| Per candidate chokepoint: 7-dim score | demand flow, irreplaceability, supply/access constraint, pricing power, financial conversion, market pricing, disconfirming trigger |
| Bottleneck release timeline | current constraint, release signal, observation cadence, downgrade trigger, target implication |

#### Module 5: 关键变量与待验证数据 ← Bridge to Stage 3

This module does NOT run new searches. It aggregates all `gap` fields, `missing_data` markers, and unresolved variables from Modules 1–4 into a `pending_questions` list. Each entry carries:

- `gap_source`: which module and sub-unit produced this gap
- `variable`: what is unknown
- `materiality`: why it matters for investment decision
- `candidate_qa_direction`: which Q1-Q4 direction this should feed into
- `candidate_score_component`: which ranking driver this gap affects

This list is the direct input to Stage 3 QA tree generation.

### Part 3: Stage 3 — QA Tree Generation from Gaps

**LLM does not invent questions.** It reads `pending_questions` from the Stage 2 gate output and maps them:

| Gap source | Maps to L1 direction | Example L3 transformation |
|------------|---------------------|--------------------------|
| Value flow path unclear (chain) | Q2 competition/value capture | "Which node actually controls profit allocation?" |
| BOM sizing method missing (space) | Q1 demand or Q2 chokepoint | "Can HBM supplier revenue elasticity support current capex?" |
| Substitution path unknown (competition) | Q3 disconfirming | "How quickly can custom ASIC replace NVIDIA general-purpose GPU?" |
| Grid queue data missing (chokepoint) | Q3 physical risk | "Is US grid interconnection a hard ceiling on AI factory delivery?" |
| Valuation data incomplete (any) | Q3 pricing risk | "What growth assumptions are embedded in current valuation?" |

**L2 buckets** come from the domain playbook, not from generic labels. The LLM groups L3 questions into the playbook's mechanism buckets (e.g. for AI factory: demand driver tree, supply response, unit economics, value capture, market pricing, counter-supply, second-order beneficiaries).

**L3 → L4/L5 trigger**: decompose only when:
- L3 fact/inference/judgment is still ambiguous ("needs more verification")
- source_plan spans >3 material classes requiring separate parsers
- support and refuting evidence address different sub-mechanisms
- L3 covers multiple companies/nodes requiring per-entity answers

If no trigger fires, stop at L3.

#### Each L3 leaf: same "think → search → parse" loop as Stage 2

```
L3 leaf question
    │
    ├─ Think: LLM writes source_plan
    │     expected_fields, priority_sources, directed_queries, preferred_skill
    │     Each supporting source plan must have a refuting source plan
    │
    ├─ Search: web_search_prime + webfetch → sources.jsonl
    │
    ├─ Parse: DeepSeek → source_extractions.jsonl → GPT verify → leaf_source_reviews.jsonl
    │
    └─ Write L3 answer:
          fact, inference, judgment (differentiated — not three copies)
          gap, trigger, source_links
          skill_dispatch (structured, not bare skill name)
          score_component (points to ranking driver)
          target_implications
          backtest_grounding (in historical mode)
```

### Part 4: Stage 4 — Target Recommendation

Stage 4 does NO new searches. It synthesizes:

1. Aggregate all L3 `score_component` fields into per-target scores
2. Compute four core dimensions from seven audit components:
   - `scarcity_or_monopoly` ← chokepoint_strength
   - `earnings_elasticity` ← future_space
   - `mispricing` ← valuation_odds
   - `risk_control` ← disconfirming_risk_control + monitorability
3. Apply scarcity-first gate: if any of the four dimensions is weak/missing → cap at `watch_only` or `no_action`
4. Attach simplified odds model (base/bull/bear) and kill tests for actionable targets
5. Deterministic ranking: action_state priority → opportunity_fit → total_score → payoff_convexity → thesis_confidence → ticker tie-break
6. Output `frozen_recommendations.json`. In backtest mode, attach labels separately without reordering.

### Part 5: LLM Analyst Behavior Contract

These rules govern how the LLM executes the pipeline and are written into AGENTS.md:

#### 5.1 One unit at a time

Do not plan all 12 BOM nodes' source_plans simultaneously. Write one node's plan → execute search → parse → write → then proceed to the next.

#### 5.2 Think before searching

Before searching, output:
- Why: decision_use
- What: expected_fields
- Where: priority_sources + directed_queries
- How: preferred_parser_skill

This thinking is written into the unit's source_plan as an auditable record.

#### 5.3 Gap is an answer

After 3 rounds of directed search with no usable results, write `status=gap` + `gap_reason`. Do not invent TAM numbers. Gaps flow into Stage 2 Module 5 pending_questions → Stage 3 QA tree.

#### 5.4 Concrete citations

Every fact carries a source_id. No "the industry generally believes" prose. Use company original language, filing numbers, report paragraphs.

#### 5.5 Self-challenge

After completing a supporting source, actively search for one refuting source. If not found, record: "refuting search planned but no public refutation found; risk is bounded but not eliminated."

#### 5.6 No skipping

"No action needed for this module" — only allowed if the domain playbook explicitly exempts this research type. "This question is not important" — only allowed with domain playbook justification. Do not delete L3 questions just because they are difficult to answer.

#### 5.7 Stage gate reporting

At the start of each stage, output:
```
## 执行计划
**当前阶段**: Stage N / [name]
**已完成**: Stage N-1 ✓ (gate passed)
**下一步**: [specific sub-unit to execute]
**待通过门控**: [next gate command]
```

At the end of each minimum unit, report what was found, what remains as gap, and what the next sub-unit is.

#### 5.8 Refresh behavior

When re-running research:
- Stage 2 Module 1 (chain): skip if industry structure unchanged
- Stage 2 Module 2 (space): refresh only time-sensitive data (company guidance, financial evidence)
- Stage 3 QA: add L3 only for new gaps or triggered refutation; do not rewrite answered L3
- Stage 4: always re-synthesize

### Part 6: Runtime Contract Updates

The following files must be updated to encode this pipeline:

| File | Change |
|------|--------|
| `AGENTS.md` | Replace execution plan section with four-stage pipeline + LLM behavior contract |
| `skills/value_invest_research/SKILL.md` | Sync behavior rules |
| `skills/value_invest_research/frameworks/research_goal_qa.md` | Add Stage 2→Stage 3 bridge protocol (Module 5 → QA tree generation) |
| `skills/value_invest_research/frameworks/domain_playbooks.md` | Add `ai_factory_infrastructure` domain playbook with concrete L2 mechanism buckets + BOM node catalog |
| `skills/value_invest_research/frameworks/research_report_contract.md` | No structural change needed; contract already covers the five modules. Add validation note for `industry_space_evidence_pack` data presence |
| `src/value_invest_research/framework_contracts.py` | Add `validate-project-schema` and `validate-industry-overview` CLI commands if not present |

### Implementation Plan

1. **Write AGENTS.md behavior contract** — the LLM behavior rules (Part 5) are the highest-leverage change; they require no Python code
2. **Add Stage 2 gate command** — `validate-industry-overview` CLI that checks industry_space_evidence_pack non-emptiness + 5-module presence
3. **Add `ai_factory_infrastructure` domain playbook** to `domain_playbooks.md` with BOM node catalog, L2 mechanism buckets, extraction schemas
4. **Wire Module 5 → Stage 3 protocol** in `research_goal_qa.md`
5. **Run first end-to-end test** on the existing `ai_factory_live_2026_06_02` project: re-run Stage 2 to populate industry_space_evidence_pack, then validate
6. **Regression test** on existing gold fixtures

### Non-Goals

- No Python state machine orchestrator (Option C rejected — too rigid for OpenCode's interactive model)
- No changes to the HTML renderer or the report presentation contract
- No changes to the canonical component family or card styles
- No automated bulk search — LLM executes searches one unit at a time, mimicking analyst workflow
