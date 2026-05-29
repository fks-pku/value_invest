# Research Report Contract

This contract defines the default final report structure for all future investment research outputs unless the user explicitly asks to iterate on the framework.

## Top-Level HTML Contract

Final user-facing HTML reports must use exactly these four top-level sections, in this order:

1. `当前研究目标`
2. `问题下钻`
3. `最终标的推荐`
4. `来源索引`

Do not add top-level process sections such as execution plan, quality framework, tool trace, iteration notes, workbench appendix, or full report appendix unless the user explicitly asks to inspect process.

## QA Hierarchy Contract

The default QA hierarchy is three layers:

- `L1`: top-level adapted research direction, normally Q1-Q4.
- `L2`: mechanism bucket selected by the research-type adapter and domain playbook. L2 must group L3 questions by meaningful analytical mechanism.
- `L3`: evidence-collection and answer unit.

L2 must not be a single catch-all wrapper under each L1 when many unrelated L3 questions exist. Split L2 by the analytical mechanisms that matter for the selected research object.

The shared contract defines hierarchy and presentation only. It does not hard-code domain questions, metrics, parsing methods, tracking indicators, or thresholds.

When a domain playbook uses bottleneck or chokepoint analysis, the scorecard must live inside the relevant Q2 QA node, not in a top-level appendix. The final target recommendation must explicitly use the chokepoint score or score drivers together with future space, valuation odds, evidence quality, and disconfirming-risk control.

Chokepoint scorecards must declare their score schema. Final target recommendations must show a compact score breakdown and simplified odds model when the report has investment implications. Prediction review fields can be summarized in Q3/Q4 and stored in workbench JSON.

## Adaptive Domain Layer

Before evidence collection, the research system must:

1. Classify the research type.
2. Select or synthesize a domain playbook.
3. Generate the concrete L1/L2/L3 questions from that playbook.

Domain playbooks own:

- domain-specific question templates
- source plans and preferred source types
- parsing schemas for filings, research reports, news, opinion, or datasets
- metrics, tracking indicators, and threshold design
- source-to-question mapping rules
- target implication logic

Examples may appear inside domain playbooks or research-type adapters, not inside this public report contract.

Inside every QA card, use this display order:

1. `当前结论呈现`
2. `问题展开（子 QA）`
3. `待补充的问题`

If child QA nodes are rendered inline as expandable cards, do not also render a separate child-question list with the same titles.

## Final Target Recommendation Contract

When the research has investment implications, add a standalone `最终标的推荐` section after `问题下钻`.

This section must synthesize all QA evidence into a ranked observation list. It must include:

- ranking
- specific ticker/name
- target class
- chokepoint or thesis node
- chokepoint score or score drivers when bottleneck analysis is used
- win probability
- payoff odds
- strength
- compact score breakdown
- simplified odds model
- prediction review trigger
- recommendation rationale
- downgrade risk
- next verification data
- source links or source anchors

The section is a research observation list, not a buy/sell/hold instruction. Do not include target prices, position sizes, or final trading commands unless the user explicitly changes the system boundary.

## Source Index Contract

`来源索引` must be collapsed by default.

Source entries must be traceable to concrete materials and must classify source type into one of:

- `evidence`
- `research_report`
- `message`
- `opinion`

Low-reliability messages can only be used as leads and cannot strengthen a conclusion by themselves.

## Clean Final HTML Contract

Final HTML must be research-first. Keep these out of final HTML:

- iteration notes
- "what changed in this run"
- quality-framework explanations
- execution traces
- tool attribution
- DeepSeek usage notes
- workbench appendices

Store process metadata in `investment_workbench.json`, run logs, or internal files.

## Visual Contract

Default visual style:

- Apple-inspired light surfaces and SF-system typography.
- Clear L1/L2/L3 hierarchy through spacing, labels, and restrained borders.
- Soft text palette with blue-gray hierarchy accents; avoid heavy black text blocks or black badges unless needed for a small emphasis state.
- Blue links for concrete sources.
- Dense but readable tables for target recommendation and source traceability.
- No duplicated titles, duplicated child lists, or repeated summary blocks.
- No decorative elements that reduce scanability.

Canonical frontend component contract:

- Use the same report shell and component classes across refreshed research reports unless the user explicitly asks for a new visual system.
- The canonical report shell is: `hero`, `top-nav`, `goal-card`, `qa-card level-1/2/3`, `qa-body`, `qa-block`, `block-title`, `logic-grid`, `logic-card`, `source-chips`, `source-chip`, `more-chip`, `artifact-card`, `target-section`, `target-summary`, `target-table`, `source-collapse`, `source-grid`, and `source-card`.
- `最终标的推荐` should render as one synthesized `target-section` with a dense `target-table`, not as separate per-target cards by default.
- `来源索引` should render as one collapsed `source-collapse` containing grouped `source-card` entries; avoid separate `source-bucket` components unless the user asks for grouped source browsing.
- Do not introduce alternate component families such as `target-card`, `source-bucket`, `section-lead`, `answer-artifact`, `schema-pill`, or `target-grid` in refreshed canonical reports.
