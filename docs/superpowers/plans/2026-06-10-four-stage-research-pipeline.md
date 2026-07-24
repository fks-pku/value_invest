# Four-Stage Serial Research Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Encode the four-stage serial research pipeline + LLM analyst behavior contract into AGENTS.md, SKILL.md, framework docs, and validation CLI commands.

**Architecture:** This is a contract-and-documentation change. No new Python modules — all edits are to existing markdown files (AGENTS.md, SKILL.md, research_goal_qa.md, domain_playbooks.md) and augmentation of existing validation code (framework_contracts.py, cli.py) with two new gate commands.

**Tech Stack:** Python 3.11+ (existing validation framework), Markdown (AGENTS.md, skill files)

---

### Task 1: Update AGENTS.md with Four-Stage Pipeline + LLM Behavior Contract

**Files:**
- Modify: `AGENTS.md`

This is the highest-leverage change — AGENTS.md is read by OpenCode at session start and governs LLM behavior.

- [ ] **Step 1: Locate the insertion point in AGENTS.md**

Read `AGENTS.md` and find the section titled `## Canonical Research Goal Framework`. After that section's opening line, find the line that starts with `1. Current research goal` and the `## Key Constraints` section.

- [ ] **Step 2: Replace the `1. Current research goal` through `9. HTML presentation` numbered execution list with the four-stage pipeline contract**

In `AGENTS.md`, the block starting from:
```
1. Current research goal
   - Define the object, time frame, investment relevance, and decision boundary.
...
9. HTML presentation
```
Replace with the new four-stage pipeline contract. The replacement text:

```markdown
## Four-Stage Serial Research Pipeline

Every research run executes as a four-stage serial pipeline. The LLM must not skip stages or run them out of order.

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

### Stage 1: Define Research Problem

LLM must write `project.json` with these minimum fields:
- `project_id`
- `title`
- `research_type`: one of `industry/theme opportunity`, `single company`, `event/policy`, `technology/product route`, `target update`, or custom
- `domain_playbook`: selected from `domain_playbooks.md` or synthesized
- `run_mode`: `historical_backtest` (default) or `live_prediction`
- `as_of_date` (if backtest), `report_date` (if live)
- `decision_boundary`
- `current_judgment`: short directional judgment
- `biggest_uncertainty`

Run `validate-project-schema <project_dir>` before proceeding to Stage 2.

### Stage 2: Industry Overview (Five Modules)

Stage 2 populates all five `行业概况` modules. Each minimum research unit (BOM node, chokepoint, competition node) executes a self-contained "think → search → parse" loop. Do not skip to Stage 3 until `validate-industry-overview` passes.

#### The "think → search → parse" loop (reused in Stage 3)

Every minimum research unit follows this sequence:

1. **Think**: LLM writes a `source_plan` before any search. The plan states:
   - `decision_use`: why this unit matters
   - `expected_fields`: concrete fields to extract
   - `priority_sources`: drawn from `config/source_universes.json` for the domain
   - `directed_queries`: site/domain-specific search queries (not just broad keywords)
   - `preferred_parser_skill`: which specialty skill should parse results

2. **Search**: LLM executes web searches using `web_search_prime` + `webfetch` (primary) or `web-reader`. Collected materials are written to `sources.jsonl` with `source_visible_at` and `cutoff_status`.

3. **Parse**: DeepSeek MCP reads materials → `source_extractions.jsonl` (fills `schema_fields`). GPT verifies → `leaf_source_reviews.jsonl`. Verified facts feed into the unit answer.

If 3 rounds of directed search produce no usable results → write `status=gap` + `gap_reason`. Do not invent TAM numbers.

#### Module 2: 行业空间 — BOM Node Execution

Each BOM node is an independent minimum unit. For each node, the LLM runs the "think → search → parse" loop across all five public-method buckets:

| Bucket | Sources | Expected fields |
|--------|---------|----------------|
| 公司指引 | Company IR, earnings calls | Revenue guidance, capex, order outlook, capacity plans |
| 公司 TAM | Investor day, 10-K market sections | Market size, CAGR, serviceable market |
| 客户侧指引 | Downstream capex, RPO announcements | Customer spend, backlog, prepayment |
| 第三方拆法 | SemiAnalysis, TrendForce, Omdia, Dell'Oro, LightCounting | TAM, shipment, ASP, supply-demand balance |
| 财务兑现证据 | Segment revenue, backlog, margin | Actual revenue, backlog, margin, FCF |

Every entry must carry independent `source_ids` and render `space-method-entry-sources` source chips. Missing buckets → `待补`.

#### Module 5 → Stage 3 Bridge

Module 5 (`关键变量与待验证数据`) does NOT run new searches. It aggregates all `gap` fields from Modules 1–4 into `pending_questions`. Each entry carries:
- `gap_source`: which module/sub-unit
- `variable`: what is unknown
- `materiality`: why it matters
- `candidate_qa_direction`: which Q direction (Q1-Q4)
- `candidate_score_component`: which ranking driver

This list is the direct input for Stage 3 QA tree generation.

### Stage 3: QA Tree Generation

The LLM reads `pending_questions` from Stage 2 and generates a QA tree. Do not invent questions — derive them from documented gaps.

L2 buckets come from the domain playbook's mechanism buckets. L3 questions are grouped under those buckets.

L3 → L4/L5 decomposition triggers:
- L3 fact/inference/judgment still ambiguous
- source_plan spans >3 material classes
- support and refuting evidence address different sub-mechanisms
- L3 covers multiple companies/nodes

Each L3 leaf runs the same "think → search → parse" loop as Stage 2 modules.

Run `validate-research-artifacts --require-l3 <project_dir>` before Stage 4.

### Stage 4: Target Recommendation

Stage 4 does NO new searches. It synthesizes:
1. Aggregate all L3 `score_component` fields into per-target scores
2. Compute four core dimensions from seven audit components
3. Apply scarcity-first gate
4. Deterministic ranking
5. Output frozen_recommendations.json

Run `validate-report-contract --require-l3 <report.html>` to complete.

## LLM Analyst Behavior Contract

The LLM must follow these rules during every research run:

### 1. One unit at a time
Do not plan all BOM nodes' source_plans simultaneously. Complete one node → next node.

### 2. Think before searching
Before every search, output:
- Why: decision_use
- What: expected_fields
- Where: priority_sources + directed_queries
- How: preferred_parser_skill

This is written into the unit's `source_plan` as an auditable record.

### 3. Gap is an answer
After 3 rounds of directed search with no usable results: write `status=gap` + `gap_reason`. Gaps flow to Stage 2 Module 5 → Stage 3 QA tree.

### 4. Concrete citations
Every fact carries a `source_id`. No "the industry generally believes" prose.

### 5. Self-challenge
After each supporting source, actively search for one refuting source. If not found: "refuting search planned but no public refutation found."

### 6. No skipping
Modules may be skipped only if the domain playbook explicitly exempts the research type. L3 questions may be deleted only with domain playbook justification.

### 7. Stage gate reporting
At each stage start, output:
```
## 执行计划
**当前阶段**: Stage N / [name]
**已完成**: Stage N-1 ✓ (gate passed)
**下一步**: [specific sub-unit]
**待通过门控**: [gate command]
```

After each minimum unit, report findings, gaps, and next unit.

### 8. Refresh behavior
- Stage 2 Module 1 (chain): skip if industry structure unchanged
- Stage 2 Module 2 (space): refresh only time-sensitive data
- Stage 3: add L3 only for new gaps; do not rewrite answered L3
- Stage 4: always re-synthesize

## Stage Gate Commands

```
value-invest-research validate-project-schema <project_dir>
value-invest-research validate-industry-overview <project_dir>
value-invest-research validate-research-artifacts <project_dir> --require-l3
value-invest-research validate-report-contract <report.html> --mode historical_backtest --require-l3
```

### 1. Current research goal
   - Define the object, time frame, investment relevance, and decision boundary.
   - Output one constrained current judgment and the biggest uncertainty.
```

- [ ] **Step 3: Verify the edit**

Read `AGENTS.md` and confirm the replacement is clean — no leftover fragments from the old 1-9 numbered section.

- [ ] **Step 4: Commit**

```bash
git add AGENTS.md
git commit -m "feat: encode four-stage serial research pipeline in AGENTS.md"
```

---

### Task 2: Sync SKILL.md Behavior Rules

**Files:**
- Modify: `skills/value_invest_research/SKILL.md`

SKILL.md is the canonical skill definition. The numbered execution sequence (items 1-10) and the "Non-Negotiable Rules" section must reflect the four-stage pipeline.

- [ ] **Step 1: Update the execution sequence (lines 8-18)**

Replace the 1-10 list:
```
1. Current research goal.
2. Research type adaptation layer.
3. Supply-chain map pass.
4. Question architecture pass.
5. Source planning pass.
6. Specialty parsing for L3-L5 research units.
7. GPT verification and evidence-linked synthesis.
8. Specific target observation list.
9. Executable contract validation, time-slice audit, frozen recommendation label attach, training sample, and prediction review artifacts.
10. HTML QA presentation.
```

With:
```
1. Stage 1: Define the research problem — research type classification, domain playbook selection, run mode, project.json.
2. Stage 2: Build industry overview — five modules (产业链与生态位, 行业空间, 竞争格局与利润池, 瓶颈点, 关键变量与待验证数据), each minimum unit executing "think → search → parse" loop. Module 5 aggregates gaps into pending_questions for Stage 3.
3. Stage 3: Generate QA tree from pending_questions — L2 mechanism buckets from domain playbook, L3 decision questions with same "think → search → parse" loop, adaptive L4/L5 decomposition only when triggered.
4. Stage 4: Synthesize target recommendations — deterministic ranking from four core dimensions, scarcity-first gate, freeze before labels.
5. Stage gates: validate-project-schema → validate-industry-overview → validate-research-artifacts --require-l3 → validate-report-contract --require-l3.
```

- [ ] **Step 2: Add the "think → search → parse" loop description**

After the list of stage gate commands, add:

```markdown
## The "Think → Search → Parse" Loop

Every minimum research unit (BOM node in Stage 2, L3 leaf question in Stage 3) executes this loop:

1. **Think**: LLM writes a `source_plan` before any search. States decision_use, expected_fields, priority_sources (from `config/source_universes.json`), directed_queries, and preferred_parser_skill. Written into the unit as an auditable record.
2. **Search**: LLM executes web searches using `web_search_prime` + `webfetch` (primary). Collected materials → `sources.jsonl` with `source_visible_at` and `cutoff_status`.
3. **Parse**: DeepSeek MCP reads materials → `source_extractions.jsonl` (fills `schema_fields`). GPT verifies → `leaf_source_reviews.jsonl`. Verified facts feed into the unit answer.

If 3 rounds of directed search produce no usable results → `status=gap` + `gap_reason`. Do not invent numbers.
```

- [ ] **Step 3: Add the LLM behavior rules**

At the end of the "Non-Negotiable Rules" section, append:

```markdown
- **One unit at a time**: Complete one BOM node or one L3 leaf before starting the next.
- **Think before searching**: Every search is preceded by a written source_plan stating why, what, where, and how.
- **Gap is an answer**: After 3 rounds of directed search with no usable results, write `status=gap` + `gap_reason`. Do not create proprietary estimates.
- **Concrete citations**: Every fact carries a source_id. No unattributed prose.
- **Self-challenge**: After each supporting source, actively search for one refuting source. Record "no public refutation found" if none exists.
- **No skipping**: Modules skipped only with domain playbook exemption. L3 questions deleted only with domain playbook justification.
- **Stage gate reporting**: At each stage start, output current stage, completed stages, next sub-unit, and pending gate command.
- **Refresh behavior**: Skip chain rebuild if industry structure unchanged; refresh only time-sensitive space data; add L3 only for new gaps; always re-synthesize Stage 4.
```

- [ ] **Step 4: Commit**

```bash
git add skills/value_invest_research/SKILL.md
git commit -m "feat: sync SKILL.md with four-stage pipeline and analyst behavior contract"
```

---

### Task 3: Add ai_factory_infrastructure Domain Playbook

**Files:**
- Modify: `skills/value_invest_research/frameworks/domain_playbooks.md`

The `ai_factory_infrastructure` domain playbook defines BOM nodes, L2 mechanism buckets, and extraction schemas for AI factory research. It is the missing piece that the renderer's industry-space module depends on.

- [ ] **Step 1: Append the AI Factory Infrastructure playbook to domain_playbooks.md**

Add after the Optical Module Playbook section (after line 146):

```markdown
## AI Factory Infrastructure Playbook

Use this playbook for AI datacenter hardware, GPU/ASIC computing, AI networking, interconnect, HBM/memory, advanced packaging, power/cooling, and AI factory capex cycle research.

Default Q map:

- Q1 Demand reality: convert AI workload, cloud revenue, and customer capex into sustainable demand, order visibility, and physical build-out by compute, memory, networking, and power/cooling nodes.
- Q2 Competitive landscape and value capture: compare suppliers, substitutes, customer bargaining power, supply response, pricing power, and chokepoint strength across GPU platform, custom ASIC, AI networking, HBM/data-center memory, advanced process/packaging, and power/cooling delivery.
- Q3 Disconfirming tests and priced-in risk: capex ROI, customer financing quality, substitution (custom ASIC, CPO, copper, internal builds), supply expansion, geopolitics, grid/power constraints, and valuation already priced in.
- Q4 Target observation list: compute platform, custom ASIC, networking, memory, foundry/packaging, power/cooling, and server/integration names reconciled with scarcity, mispricing, earnings elasticity, risk control, valuation odds, and kill tests.

Required L2 mechanism buckets:

- AI workload demand driver tree: training/inference/agent/RAG workload → GPU/ASIC/TPU demand → HBM/memory attach → network bandwidth → power/cooling per rack, with evidence that it is not merely inventory restocking.
- Supply response and capacity: TSMC CoWoS/advanced packaging, HBM wafer capacity, networking chip supply, power equipment lead time, transformer/grid interconnection, and datacenter construction timeline.
- Unit economics and profit bridge: per-node ASP, cost structure, gross margin, operating margin, capex intensity, FCF conversion, and working-capital pressure.
- Competitive value-capture map: which companies capture revenue/profit at GPU platform, custom ASIC design, AI Ethernet/InfiniBand/NVLink switching, optical interconnect, HBM supply, advanced packaging, power/cooling, and server integration nodes.
- Technology route comparison: GPU vs custom ASIC, pluggable optics vs CPO, air cooling vs liquid cooling, Ethernet vs InfiniBand, discrete GPU vs chiplet.
- Component/BOM value chain: subsystem, component/service, key companies, demand input, supply input, downstream recipient, financial validation metric, and QA link.
- Market-pricing bridge: current market cap/multiples/discount rate/implied growth versus required fundamental path for each node.
- Counter-supply and substitution: customer self-designed chips, China domestic supply, second-source qualification, architecture changes (CPO, CXL, UALink), and cloud capex digestion.
- Capital-chain and second-order beneficiaries: whether high AI factory returns pull capex into equipment, materials, test, infrastructure, channels, or downstream AI service adoption.
- Model口径 reconciliation: compare sell-side/industry/internal models by revenue scope, segment split, calendar/fiscal period, currency, margin definition, and capex classification.

### AI Factory BOM Node Catalog

The following BOM nodes are the default decomposition targets for the 行业空间 module:

| Node | Key Subsystems | Typical Public-Method Sources |
|------|---------------|------------------------------|
| GPU/AI Accelerator | NVIDIA Blackwell/Rubin, AMD MI400, Intel Gaudi | NVIDIA IR, SemiAnalysis, TechInsights |
| Custom ASIC/XPU | Broadcom, Marvell, Amazon Trainium, Google TPU | Broadcom IR, Amazon IR, SemiAnalysis |
| AI Networking | NVLink, InfiniBand, Ethernet switch, NIC/DPU | NVIDIA IR, Broadcom IR, Dell'Oro |
| Optical Interconnect | 800G/1.6T transceivers, LPO/CPO, silicon photonics | LightCounting, Coherent IR, Lumentum IR |
| HBM/Data-Center Memory | HBM3E/HBM4, DDR5, eSSD, CXL memory | Micron IR, SK hynix IR, TrendForce |
| Advanced Process/Packaging | 3nm/2nm, CoWoS, 3D packaging | TSMC IR, TechInsights, SemiAnalysis |
| Power/Cooling Delivery | UPS, switchgear, transformer, liquid cooling, busway | Vertiv IR, Eaton IR, IEA |
| Server/System Integration | AI server, rack-scale, liquid-cooled chassis | Dell IR, Supermicro IR, ServeTheHome |

### AI Factory Extraction Schemas

- `ai_factory_compute_demand`: platform/chip type, workload, cluster scale, unit volume, ASP, revenue, customer attach, period, source.
- `ai_factory_network_demand`: network type (NVLink/IB/Ethernet), port speed, port count, attach rate, switch/NIC revenue, period, source.
- `ai_factory_memory_demand`: memory type (HBM/DDR/eSSD), capacity per GPU/server, attach rate, ASP, revenue, margin, period, source.
- `ai_factory_power_cooling_demand`: product type (UPS/switchgear/transformer/liquid cooling), order/backlog, book-to-bill, margin, lead time, period, source.
- `ai_factory_manufacturing_capacity`: foundry, node, wafer capacity, packaging capacity, utilization, capex, ramp timing, source.
- `ai_factory_unit_economics`: company/product node, ASP, cost, gross margin, operating margin, capex, FCF, period, source.
- `ai_factory_valuation_rerating`: company, market cap/EV, multiples, FCF yield, implied growth/margin, peer set, source.
- `ai_factory_model_reconciliation`: model/source, metric, period, value, unit, scope, formula, difference vs alternative, adoption status.

Scoring adjustments:

- `future_space` must include demand-supply slope mismatch and node-specific attach rate logic, not only TAM.
- `chokepoint_strength` must include supply constraint, qualification difficulty, ecosystem lock-in, and substitution risk.
- `valuation_odds` must check whether node growth and peak margins are already priced into current multiples.
- `disconfirming_risk_control` must include counter-supply, architecture substitution, capex digestion, geopolitics, and grid/power constraint.
- `payoff_convexity` must separate volume growth, mix upgrade, margin expansion, and multiple rerating.
```

- [ ] **Step 2: Commit**

```bash
git add skills/value_invest_research/frameworks/domain_playbooks.md
git commit -m "feat: add ai_factory_infrastructure domain playbook with BOM node catalog"
```

---

### Task 4: Add Stage 2→Stage 3 Bridge Protocol

**Files:**
- Modify: `skills/value_invest_research/frameworks/research_goal_qa.md`

- [ ] **Step 1: Add Module 5 → QA Tree protocol after the Industry Overview section (around line 256)**

After the five module descriptions in the Industry Overview section, add:

```markdown

### Module 5 → Stage 3 Bridge Protocol

Module 5 (`关键变量与待验证数据`) is the bridge from Stage 2 to Stage 3. It does NOT run new searches. It aggregates every `gap`, `missing_data`, and unresolved variable from Modules 1-4 into a `pending_questions` list.

Each entry in `pending_questions`:

- `gap_source`: which module and sub-unit produced this gap (e.g. "行业空间 / HBM 节点 / 公司指引缺失")
- `variable`: what is unknown (e.g. "HBM3E 2026 ASP 指引")
- `materiality`: why it matters for the investment decision
- `candidate_qa_direction`: which Q1-Q4 direction this should feed into
- `candidate_score_component`: which ranking driver this gap affects

LLM reads `pending_questions` and maps them to L3 questions:

| Gap source | Maps to | Example L3 transformation |
|------------|---------|--------------------------|
| Value flow path unclear (chain) | Q2 competition/value capture | "Which node actually controls profit allocation?" |
| BOM sizing method missing (space) | Q1 demand or Q2 chokepoint | "Can HBM supplier revenue elasticity support current capex?" |
| Substitution path unknown (competition) | Q3 disconfirming | "How quickly can custom ASIC replace NVIDIA general-purpose GPU?" |
| Grid constraint data missing (chokepoint) | Q3 physical risk | "Is US grid interconnection a hard ceiling on AI factory delivery?" |
| Valuation data incomplete (any) | Q3 pricing risk | "What growth assumptions are embedded in current valuation?" |

Do NOT generate L3 questions that do not trace back to at least one `pending_questions` entry or one data gap documented in the industry overview.
```

- [ ] **Step 2: Commit**

```bash
git add skills/value_invest_research/frameworks/research_goal_qa.md
git commit -m "feat: add Stage 2→Stage 3 bridge protocol from pending_questions to QA tree"
```

---

### Task 5: Add validate-industry-overview CLI Command

**Files:**
- Modify: `src/value_invest_research/framework_contracts.py`
- Modify: `src/value_invest_research/cli.py`

Two new validator functions and two new CLI commands.

- [ ] **Step 1: Add `validate_project_schema` function to framework_contracts.py**

Add after the `validate_report_contract_html` function (after line ~881):

```python
def validate_project_schema(project: dict[str, Any]) -> dict[str, Any]:
    """Validate project.json against the four-stage pipeline schema."""
    issues: list[dict[str, str]] = []
    if not isinstance(project, dict):
        return {"ok": False, "issues": [{"severity": "error", "code": "missing_project", "message": "project dict is absent or not a dict"}], "summary": {}}
    project_id = str(project.get("project_id") or "")
    if not project_id:
        _issue(issues, "error", "missing_project_id", "project.json must include project_id")
    research_type = str(project.get("research_type") or "")
    valid_types = {"industry/theme opportunity", "single company", "event/policy", "technology/product route", "target update"}
    if research_type not in valid_types:
        _issue(issues, "error", "missing_or_invalid_research_type", f"project.json must include research_type in {valid_types}")
    run_mode = str(project.get("run_mode") or "")
    if run_mode not in ("historical_backtest", "live_prediction"):
        _issue(issues, "error", "missing_or_invalid_run_mode", "project.json must declare run_mode as historical_backtest or live_prediction")
    if run_mode == "historical_backtest" and not project.get("as_of_date"):
        _issue(issues, "error", "missing_as_of_date", "historical_backtest mode requires as_of_date in project.json")
    if run_mode == "live_prediction" and not project.get("report_date"):
        _issue(issues, "error", "missing_report_date", "live_prediction mode requires report_date in project.json")
    domain_playbook = str(project.get("domain_playbook") or "")
    if not domain_playbook:
        _issue(issues, "warn", "missing_domain_playbook", "project.json should specify a domain_playbook; defaulting to generic")
    return {"ok": len(issues) == 0, "issues": issues, "summary": {"project_id": project_id, "research_type": research_type, "run_mode": run_mode}}
```

- [ ] **Step 2: Add `validate_industry_overview` function to framework_contracts.py**

Add after the new `validate_project_schema`:

```python
def validate_industry_overview(project_dir: str | Path) -> dict[str, Any]:
    """Validate that an industry overview has been populated with non-trivial data before Stage 3."""
    import json
    from pathlib import Path
    issues: list[dict[str, str]] = []
    project_dir = Path(project_dir)
    
    # Check project.json
    project_file = project_dir / "project.json"
    if not project_file.exists():
        _issue(issues, "error", "missing_project_json", f"{project_dir} has no project.json")
        return {"ok": False, "issues": issues, "summary": {}}
    with open(project_file) as fh:
        project = json.load(fh)
    project_validation = validate_project_schema(project)
    if not project_validation["ok"]:
        issues.extend(project_validation["issues"])
    
    # Check qa_tree.json for supply_chain
    qa_file = project_dir / "qa_tree.json"
    chain = {}
    if qa_file.exists():
        with open(qa_file) as fh:
            chain = json.load(fh).get("supply_chain") or {}
    
    # Validate industry_space_evidence_pack presence
    evidence_pack = (
        chain.get("industry_space_evidence_pack")
        or chain.get("industry_space_bom_reasoning")
        or chain.get("industry_space_rows")
        or []
    )
    if not isinstance(evidence_pack, list) or not evidence_pack:
        _issue(
            issues,
            "error",
            "missing_industry_space_evidence_pack",
            "Stage 2 must populate industry_space_evidence_pack with at least one BOM node before Stage 3",
        )
    else:
        node_count = 0
        has_sizing_data = 0
        for node in evidence_pack:
            if not isinstance(node, dict):
                continue
            node_count += 1
            sizing = node.get("publicSizingMethods") or node.get("public_sizing_methods") or {}
            if isinstance(sizing, dict) and sizing.get("methods"):
                has_sizing_data += 1
        if node_count == 0:
            _issue(issues, "error", "empty_industry_space_evidence_pack", "industry_space_evidence_pack exists but contains no BOM nodes")
        if has_sizing_data == 0:
            _issue(issues, "warn", "no_space_sizing_data", "no BOM node has populated publicSizingMethods; Stage 2 Module 2 may be incomplete")
    
    # Validate five module presence hints
    found_modules = []
    if chain.get("layers") or chain.get("stage_groups"):
        found_modules.append("产业链与生态位")
    if evidence_pack and len(evidence_pack) > 0:
        found_modules.append("行业空间")
    if chain.get("competition") or chain.get("competition_landscape"):
        found_modules.append("竞争格局与利润池")
    if chain.get("chokepoints") or chain.get("candidate_chokepoints"):
        found_modules.append("瓶颈点")
    if chain.get("data_gaps") or chain.get("pending_questions"):
        found_modules.append("关键变量与待验证数据")
    
    missing_modules = [m for m in ["产业链与生态位", "行业空间", "竞争格局与利润池", "瓶颈点", "关键变量与待验证数据"] if m not in found_modules]
    for module in missing_modules:
        _issue(issues, "warn", f"missing_module_hint_{module}", f"行业概况 module '{module}' has no detectable data in supply_chain; stage may be incomplete")
    
    threshold = 1 if _any_error(issues) else 0
    ok = len([i for i in issues if i.get("severity") == "error"]) <= threshold
    return {"ok": ok, "issues": issues, "summary": {"modules_detected": found_modules, "missing_modules": missing_modules, "bom_nodes": len(evidence_pack)}}


def _any_error(issues: list[dict[str, str]]) -> bool:
    return any(i.get("severity") == "error" for i in issues)
```

- [ ] **Step 3: Wire two new CLI commands in cli.py**

In `cli.py`, add subparsers after line ~83 (after `validate-research-artifacts`):

```python
    project_schema_parser = subparsers.add_parser(
        "validate-project-schema",
        help="Validate project.json against the four-stage pipeline schema",
    )
    project_schema_parser.add_argument("project_dir")

    industry_overview_parser = subparsers.add_parser(
        "validate-industry-overview",
        help="Validate that industry overview data is populated before Stage 3",
    )
    industry_overview_parser.add_argument("project_dir")
```

Add command dispatch after line ~623:

```python
        if args.command == "validate-project-schema":
            return run_validate_project_schema_cmd(root, args)
        if args.command == "validate-industry-overview":
            return run_validate_industry_overview_cmd(root, args)
```

Add handler functions at the end of cli.py (before the final `except` block, around line 710):

```python
def run_validate_project_schema_cmd(root: Path, args: argparse.Namespace) -> int:
    import json
    from value_invest_research.framework_contracts import validate_project_schema
    project_file = root / args.project_dir / "project.json"
    if not project_file.exists():
        print(json.dumps({"ok": False, "issues": [{"severity": "error", "code": "missing_project_json", "message": str(project_file) + " not found"}], "summary": {}}, ensure_ascii=False))
        return 1
    with open(project_file) as fh:
        project = json.load(fh)
    result = validate_project_schema(project)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


def run_validate_industry_overview_cmd(root: Path, args: argparse.Namespace) -> int:
    from value_invest_research.framework_contracts import validate_industry_overview
    project_dir = root / args.project_dir
    result = validate_industry_overview(project_dir)
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1
```

Add `import argparse` at the top of cli.py if not already present (check by reading the imports).

- [ ] **Step 4: Test the new commands**

```bash
PYTHONPATH=src python -m value_invest_research validate-project-schema research/bom/ai_factory_live_2026_06_02
```

Expected: OK (project has research_type, run_mode, report_date).

```bash
PYTHONPATH=src python -m value_invest_research validate-industry-overview research/bom/ai_factory_live_2026_06_02
```

Expected: FAIL with "missing_industry_space_evidence_pack" error (current report lacks BOM nodes — this is the expected behavior, confirming the gate works).

- [ ] **Step 5: Commit**

```bash
git add src/value_invest_research/framework_contracts.py src/value_invest_research/cli.py
git commit -m "feat: add validate-project-schema and validate-industry-overview CLI gates"
```

---

### Task 6: Regression Test

**Files:**
- No new files. Run existing tests + gold fixture validation.

- [ ] **Step 1: Run the Python test suite**

```bash
PYTHONPATH=src python tools/run_tests.py
```

Expected: All existing tests pass (no functional changes to existing code paths).

- [ ] **Step 2: Validate the gold fixture report**

```bash
PYTHONPATH=src python -m value_invest_research validate-report-contract tests/fixtures/research_quality_gold/professional_report.html --mode historical_backtest --require-l3
```

Expected: PASS (gold fixture should still meet contract).

- [ ] **Step 3: Run contract validation on the existing AI factory live report**

```bash
PYTHONPATH=src python -m value_invest_research validate-report-contract research/bom/ai_factory_live_2026_06_02/professional_report.html --mode live_prediction --require-l3
```

Expected: FAIL with "missing_industry_space" error (the existing report doesn't have the `行业空间` module — this is expected and documented).

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: verify regression — all existing tests and gold fixture pass"
```
```

---

### Implementation Order

Tasks 1-4 are pure documentation edits (no test dependency). Task 5 adds executable validation. Task 6 is verification.

Execute in order: 1 → 2 → 3 → 4 → 5 → 6.
