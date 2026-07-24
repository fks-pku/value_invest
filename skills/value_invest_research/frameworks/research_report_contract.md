# Public Research Report Contract

This is the sole default public-report contract. It defines presentation only. Domain questions, metrics, source plans, parsers, thresholds, and scoring rules remain in playbooks and structured research artifacts.

## Primary Format

The canonical public artifact is Markdown:

```text
professional_report.md
```

`professional_report.html` may be generated as a compatibility view, but it is not the source of truth and must not contain research content that is absent from Markdown.

Markdown must be readable as plain text. Do not depend on CSS classes, JavaScript, HTML cards, hidden panels, or browser-only interactions to communicate the research.

## Top-Level Order

Every default industry/project Markdown report contains exactly four numbered H2 sections:

1. `当前研究的问题`
2. `行业概况`
3. `标的推荐`
4. `来源索引`

Internal QA trees, source plans, raw queries, parser outputs, reviews, score worksheets, tool traces, credentials, and change logs are excluded unless the user explicitly asks for a workbench.
Public `下钻 QA` is therefore opt-in. Do not render raw search queries in a public report.

`report_scope: standalone-bom` is the only exception. It contains exactly five
numbered H2 sections: `需求侧`, `供给侧`, `技术侧`, `估值侧`, and `ESG`.

## Report Scopes and Layout

Industry, theme, and S-curve research uses one parent index and one child project per canonical BOM node:

```text
<industry_project>/professional_report.md
<industry_project>/professional_report.html                 # optional compatibility view
<industry_project>/boms/manifest.json
<industry_project>/boms/<node_id>/professional_report.md
<industry_project>/boms/<node_id>/professional_report.html # optional compatibility view
```

The parent front matter uses `report_scope: industry-index`. A child uses `report_scope: bom-node` and declares `bom_node_id`. A project whose complete research object is one isolated BOM uses `report_scope: standalone-bom` and also declares `bom_node_id`.

The standalone report lives beside its own `project.json`, `source/`, `ledger/`,
`inbox/`, and `material_intake/` directories. Project-local links are resolved
relative to that report. Canonical PDFs stay under `source/`; a renderer must never
link to `material_intake/raw/` or to another BOM project.

The parent owns chain taxonomy, navigation, and chain-wide target aggregation. It must not embed every BOM node's six-question body.

Each child owns exactly one BOM node, its `project.json`, filtered `sources.jsonl`,
`source/`, `material_intake/`, `inbox/`, temporal ledger, snapshots, optional
`research_run.json`, report, refresh cadence, and mapped targets.

Every child links back to the parent index. Every completed child uses its node-specific six-question playbook; a generic fallback or copied static report cannot claim completion.

### Standalone BOM

Use this scope when the user is researching one BOM directly and does not need an
industry parent. The report is intentionally narrower than an industry report:

1. `需求侧`
2. `供给侧`
3. `技术侧`
4. `估值侧`
5. `ESG`

Each section contains exactly:

1. `简单逻辑链`: one natural-language paragraph explaining the causal test.
2. `信息时间线`: a newest-to-oldest Markdown table.
3. `最新结论与趋势`: a natural-language synthesis derived from the displayed rows.

The timeline header is:

```text
| 时间 | 信息类型 | Source | 观点列表 |
```

`时间` is `published_at`, not the fiscal period described by the source. `信息类型`
uses the public material classes `官方财报`, `官方公司`, `研报`, `第三方权威`,
`市场消息`, `专家观点`, or `其他`. `Source` contains one clickable official or
project-local original-material link. One source occupies one row within a lens.
`观点列表` groups all GPT-reviewed atomic claims from that source for the current
lens; every bullet preserves its page, item, heading, table, or paragraph locator.
It is not a document-level abstract.

The same source may appear in several timelines only after a separate lens-specific
parse. Rows are never padded with model priors. The conclusion must distinguish
facts, forecasts, disagreement, and the strongest boundary condition. A standalone
BOM report does not require a duplicate source-index section because its timelines
are the claim-level index; `sources.jsonl` remains the structured audit ledger.

## 1. Current Research Goal

Write a compact research brief containing:

- exact research object and time boundary;
- investment decision being tested;
- scope and exclusions;
- current constrained judgment;
- biggest uncertainty.

For a BOM child, add a two-column node-boundary table:

- receives;
- produces;
- supplies to;
- representative companies;
- financial validation metrics.

Do not explain framework iterations or implementation details.

## 2. Industry Overview

### Parent Industry Index

The parent contains:

1. `01 技术链与 BOM`
2. `02 BOM 独立研究目录`

`01 技术链与 BOM` explains the end-to-end value flow and renders one stable table using the canonical BOM registry. Every row includes node name, inputs, output/product, downstream recipient, representative companies, and financial validation metrics.

`02 BOM 独立研究目录` renders one Markdown heading and relative link per BOM child. It states the node's scope, research status, and related-target count. The link points to `boms/<node_id>/professional_report.md`.

### BOM Child

The child contains exactly six H3 question modules:

1. `当前 BOM 的需求是否会被 S 曲线放大拉动？`
2. `供给能否跟上？`
3. `谁控制供给？`
4. `是否已经财务兑现？`
5. `市场是否已定价？`
6. `反证是什么？`

Each question is an independent minimum research unit built from the node's own playbook, append-only temporal ledger, and reproducible as-of snapshot.

The playbook may provide a short professional model, formula, and basic logic hint. These orient the reader but never become an evidence whitelist or a mandatory search path.

### Question Sequence

Every six-question module uses the same visible sequence:

1. `基本理解思路`
2. `当前结论`
3. `相较上一截面的变化`
4. `时间演化`
5. `映射材料`
6. `信息覆盖`

#### Basic Understanding

Show:

- professional model and purpose;
- concise formula or reasoning rule;
- optional arrow-separated logic hint;
- an explicit note that the hint is not an evidence whitelist.

#### Current Conclusion

Show:

- conclusion and strength;
- supporting mechanism;
- strongest refutation;
- target impact;
- latest material date;
- clickable claim-level source links.

Natural-language research conclusions lead. Do not replace an answer with source counts or process status.

#### Change From Previous Snapshot

Claim a change only when a real prior structured snapshot exists. With no prior snapshot, label the current report as a baseline. Never reconstruct historical conclusions with hindsight.

#### Time Evolution

Order evidence by `published_at`, the date when the market could know it. Keep actual period and forecast target period separate.

The compact timeline may show the earliest representative claims first. If it is truncated, state the displayed and full claim counts and keep the complete set in `映射材料`.

#### Mapped Materials

Render a Markdown table with:

- publication date;
- linked material title;
- material class and ingestion channel;
- claim type and stance;
- topic;
- atomic claim;
- effective period;
- target period.

The same document may map to several questions, but every mapped row must be question-specific. A material is not evidence until its atomic claim has been parsed and reviewed.

Every material preserves:

- `material_class`: official filing, official company, sell-side research, authoritative third party, market news, expert opinion, or other;
- `ingestion_channel`: question search, knowledge-base scan, or manual import;
- `published_at`;
- `effective_period`;
- `target_period`;
- `ingested_at`.

Unmapped or unparsed material stays internal. It must not be silently discarded or forced into an unsuitable question.

#### Information Coverage

Render one compact table containing:

- actual, forecast, opinion, message, valuation, and refutation counts;
- supporting and conflicting claim counts;
- earliest and latest material dates;
- coverage status;
- explicit gaps when material is unavailable.

Coverage is semantic, not a raw source-count score.

### BOM S-Curve Rollup

After the six questions, write one short natural-language rollup:

- current S-curve stage;
- which questions are complete or incomplete;
- next confirmation signal;
- downgrade signal;
- whether the evidence permits target ranking.

The stage remains pending until all six questions pass semantic completion. Q6 requires observed refuting evidence, not only hypothetical risks.

## 3. Target Recommendations

The target section is a research observation list, not a trading instruction.

Use one Markdown table containing:

- ticker and company;
- canonical BOM node;
- candidate and final action state;
- core value-capture reason;
- future space and payoff logic;
- research-gate status;
- main risks and quantitative downgrade triggers.

`actionable_long` is allowed only after all six BOM questions, explicit refutation, structured company exposure, as-of valuation, component score evidence, and quantitative kill tests pass.

Otherwise use `watch_only`; missing BOM mapping is `no_action`.

The parent aggregates chain-wide targets. A child shows only targets mapped to its own `thesis_node_id`.

## 4. Source Index

Render a Markdown table with source ID, linked title, material class or compatibility bucket, market-visible date, and concise use summary.

The parent may index the complete chain source set. A child indexes only sources selected by that node's research or mapped targets.

Claim-level links are mandatory. The source index is an audit supplement, not a substitute.

## Historical Backtest Lock

In historical mode:

- only information visible on or before `as_of_date` may support research;
- model prior is hypothesis-only;
- every source preserves visibility proof;
- post-cutoff material is rejected, quarantined, or label-only;
- prose reads as if written on the cutoff date;
- future-return labels are isolated in the target section and never alter research.

Freeze recommendations before attaching labels.

## Non-Drift Locks

1. Markdown is the canonical public artifact.
2. Default industry/project reports keep four numbered H2 sections in exact order; `standalone-bom` keeps the five locked lenses in exact order.
3. Parent, manifest, and child paths preserve one-to-one BOM identity.
4. BOM ID and public name come from the canonical registry.
5. Every `bom-node` child keeps the same six semantic questions; every `standalone-bom` keeps the five professional lenses.
6. Every six-question module keeps its temporal sequence; every standalone lens keeps `简单逻辑链 -> 信息时间线 -> 最新结论与趋势` and claim-level source links.
7. Backtest cutoff and label isolation remain enforced.
8. Public reports contain no raw process traces or change logs.

## Validation

Before publication:

1. run focused tests and the full research-framework suite;
2. run `validate-report-contract` on `professional_report.md`;
3. run `validate-material-intake` when intake artifacts exist;
4. run `validate-research-artifacts --require-l3` when artifacts exist;
5. verify scope-specific section order, parent-child links where applicable, six-question or five-lens identity, timeline order, Markdown tables, source links, and no public process text;
6. run `git diff --check`.

Compatibility HTML may also be smoke-tested, but Markdown validation is the publication gate.
