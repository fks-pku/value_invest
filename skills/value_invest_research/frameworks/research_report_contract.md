# Public Research Report Contract

This is the sole default public-report contract. It defines presentation only. Domain questions, metrics, source plans, parsers, thresholds, and scoring rules remain in playbooks and structured research artifacts.

## Primary Format

HTML is the default public artifact:

```text
professional_report.html
```

`professional_report.md` is generated from the same report view model as a
portable audit sidecar. HTML and Markdown must not diverge in research claims,
source mappings, dates, or conclusions.

If the user explicitly requests a research-plan document, generate
`research_plan.md` beside the professional report. It is a separate human-readable
question hierarchy generated from `research_plan.json` plus the active per-L3 child
plans. The initial document contains only L1/L2/L3. Every L3 is a parent section;
later versions show only child questions actually created by failed answerability
gates, in their hierarchy up to L5. Every current terminal question lists required data, analysis,
and no other repeated execution metadata. Source plans, dependencies, evidence gates,
and ledger-derived status remain in structured artifacts. Display wording may remove
boilerplate but must preserve canonical question IDs. Regenerate the Markdown plan
with plan builds, dynamic expansions, and report refreshes. Do not generate a plan HTML.

HTML must work as a self-contained local file, remain readable without a server,
and link directly to project-local PDF originals. Presentation JavaScript may
enhance navigation but may not hide research content or fetch evidence at runtime.
Markdown remains readable as plain text.

## Top-Level Order

Every default industry/project report contains exactly four numbered H2 sections
in this locked order; HTML renders the same semantic section sequence:

1. `当前研究的问题`
2. `行业概况`
3. `标的推荐`
4. `来源索引`

Internal QA trees, raw source queries, parser outputs, reviews, score worksheets, tool traces, credentials, and change logs are excluded unless the user explicitly asks for a workbench.
Public `下钻 QA` is therefore opt-in. Do not render raw search queries in a public report.
For `standalone-bom`, every L3 research question remains visible in the public
report, but its nested research plan belongs only in `research_plan.md`; do not
duplicate the plan tree in the HTML report or Markdown audit sidecar.

`report_scope: standalone-bom` is the only exception. It contains five collapsible
top-level sections: `需求侧`, `供给侧`, `技术侧`, `估值侧`, and `ESG`.

## Report Scopes and Layout

Industry, theme, and S-curve research uses one parent index and one child project per canonical BOM node:

```text
<industry_project>/professional_report.md
<industry_project>/professional_report.html                 # default public view
<industry_project>/research_plan.md                         # adaptive question hierarchy
<industry_project>/boms/manifest.json
<industry_project>/boms/<node_id>/professional_report.md
<industry_project>/boms/<node_id>/professional_report.html # default public view
```

The parent front matter uses `report_scope: industry-index`. A child uses `report_scope: bom-node` and declares `bom_node_id`. A project whose complete research object is one isolated BOM uses `report_scope: standalone-bom` and also declares `bom_node_id`.

The standalone HTML report lives beside its own `project.json`, Markdown audit
sidecar, `source/`, `ledger/`,
`inbox/`, and `material_intake/` directories. Project-local links are resolved
from portable relative paths in the ledger. When rendering a report for the local
workspace, HTML material links stay project-relative (`source/...`) so a report
opened through `file://` resolves the neighboring PDF correctly. Markdown audit
links may use absolute filesystem paths. Manually imported PDFs stay under the
BOM's `source/`.
The complete IMA provider mirror lives in repository `source/ima/`; reports selected
for this BOM are copied to the project's `source/ima/<published_at>/` and public
timelines link only to those portable project-local copies. A renderer must never
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

The report begins with one `当前投资判断` snapshot. It must show action state,
fundamental/consensus/priced-in deltas, semantic gate results, company exposure and
earnings/valuation bridges, catalysts, and monitorable downgrade tests. In a
logic-chain-centered report, its lead paragraph is the global rollup of strengthened
causal nodes, main breakpoints, failed gates, and action state. Preserve a source
batch or Q2-specific update separately as `本期证据变化`; never present that local
update as the global judgment.

Each HTML section contains exactly:

1. `第一性原理逻辑链`: one natural-language paragraph explaining the causal test.
2. `逻辑节点与原子观点材料`: full-width causal nodes in canonical order. The
   visible node summary labels and shows the exact L3 research question, current
   state, conclusion, and real baseline/change.
   The collapsed body contains exactly one horizontally scrollable table:
   `发布日期 | 报告名称 | 材料类型 | 原子观点 | 对逻辑点的影响`. Rows use
   `published_at` from newest to oldest, and one source occupies one row. The report
   name is a blue link. Atomic claims are numbered `1, 2, 3...`; the final cell
   uses a matching numbered list of `增强`, `减弱`, `边界`, `约束`, `线索`,
   `待判断`, `新分支`, `冲突`, or another explicit active mapping effect. Original
   locator, `effective_period`, and `target_period` stay as compact
   labels in the atomic-claim cell. Do not add public state-history, event-history,
   filter, gap, next-validation, or company/entity audit modules. Those records stay
   in the append-only internal ledgers.
3. Optional `派生证据视图`: Q1/Q2 or another structured projection that supports
   navigation or comparison but does not replace the causal chain or generate the
   lens conclusion.

Do not render a separate lens-level `全局结论与趋势`. The leading
`当前投资判断` is the only public global synthesis. Node conclusions remain visible
with their evidence, while lens conclusions and trend records remain internal inputs
to snapshots and audit ledgers. Do not render confidence scores; show auditable
evidence conditions instead.

An explicit user request may narrow one lens's public logic-node modules through
`public_logic_node_ids`. In a `logic_chain_centered` report, the ordered subset must
retain every causal node and may omit only derived views. Retain omitted views and
all underlying ledgers internally; presentation filtering never deletes evidence.
If Q2 uses `demand_quantity_matrix`, its Q1 `demand_party_list` classification view
must remain in the same public subset.

The demand-side Q1 `需求方` derived view is one narrow rendering exception. If the
playbook declares `render_mode: demand_party_list`, the node renders only two
non-empty groups in this order: `当前需求方`, then `潜在未来需求方`. It does not
render a state badge, current conclusion, change assessment, evidence counts,
company/entity disclosures, or material tables. Business scenarios, tasks,
systems, component specifications, procurement channels, and quantities must not
appear in this block. Its exact L3 research question remains visible in the node
heading. Q2 owns the current quantity baseline.

If the Q2 derived view declares `render_mode: demand_quantity_matrix`, render exactly three outer
groups in this order: `当前需求方`, `潜在未来需求方`, and `其它分类`. The first two
groups reuse their respective Q1 demander lists; `其它分类` groups rows that cannot
be assigned to a Q1 demander by their own information category. Its exact L3 research
question remains visible above the matrix. In HTML, every
outer group is a collapsed disclosure, and every specific demander or other
information category is a second collapsed disclosure nested inside it. Markdown
mirrors the same numbered hierarchy. Every specific category has one separately
titled table and may have multiple information rows. Use an explicit gap row when
no credible current quantity exists; a potential-future category may show a clear
empty state and must not enter the current baseline. Every table uses exactly
`来源 | 期间 | 信息类型 | 具体信息`. `信息类型` normalizes source material into
`官方财报`, `第三方研究`, `市场消息`, or `机构研报`; `具体信息` keeps the metric,
quantity or forecast, mapping quality, and principal limitation together. Other
categories do not claim a Q1 demander mapping. Do not render Q2 entity snapshots or
material tables in parallel with this matrix, and do not sum incompatible rows.

The locked state coordinate remains:

```text
BOM x lens/question x logic node x company/entity x as_of_date
```

For public interpretation, the primary hierarchy is:

```text
BOM x lens x causal logic node x source row x numbered atomic claim
```

The rendered expansion of that coordinate is:

```text
logic node -> newest-to-oldest source rows -> numbered atomic claims
                                       -> matching numbered mapping effects
```

Do not stretch a forecast across the publication axis. A claim published once but
covering several business periods stays one publication event with effective/target
period tags.

Atomic claims use the minimum audit envelope and remain immutable. A separate
reviewed mapping records `support`, `refute`, `boundary`, `constraint`,
`new_branch`, `conflict`, `unresolved`, or compatibility `neutral`, plus rationale
and downstream impacts. Company/entity is a secondary audit dimension under each
causal node, not the organizing spine of the public reasoning. Real node snapshots,
entity snapshots, mapping rationale, downstream impacts, gaps, and next validation
remain in the internal audit structure; they do not create duplicate public tables.

Every causal node contains one horizontally scrollable table with exactly:

```text
发布日期 | 报告名称 | 材料类型 | 原子观点 | 对逻辑点的影响
```

One source occupies one row. `报告名称` is the official or project-local original-material link.
`材料类型` uses the public material classes `官方财报`, `官方公司`,
`研报`, `第三方权威`, `市场消息`, `专家观点`, or `其他`. `原子观点` groups only
the GPT-reviewed atomic claims mapped to the current causal node and numbers them
`1, 2, 3...`. `对逻辑点的影响` uses the same numbering so every impact maps visually
to exactly one claim. Mapping metadata never replaces the source locator. Do not
repeat the same evidence in another public module.

`增强` and `减弱` are reserved for direct claim-to-node relationships that
explicitly satisfy the node support/refute rule. Forecasts, proxies, contextual
inputs, and incomplete observations render as `边界`, `约束`, `线索`, `待判断`,
`新分支`, or `冲突`. Reviewed rejected relationships remain internally as
`unmapped`; they are not rendered in a causal-node table and do not contribute to
node state.

`published_at` is the market-visible publication date, not the fiscal period
described by the source. Local PDF links use the renderer-resolved project-relative
`source/...` path, never `/Users/...`, never `file://`, and never a central archive
path. They navigate in the current tab because opening local files with
`target="_blank"` can produce an empty browser tab. Only HTTP(S) links may use
`target="_blank"`.
The location preserves its page, item, heading, table, or paragraph locator. It is
not a document-level abstract. The Markdown sidecar mirrors the causal-node
five-column table.

```text
| 发布日期 | 报告名称 | 材料类型 | 原子观点 | 对逻辑点的影响 |
```

The same source may appear under several entities or nodes only after a separate
mapping confirms that the atomic claim applies to each coordinate. Rows are never
padded with model priors. The conclusion must distinguish facts, forecasts,
disagreement, and the strongest boundary condition. A standalone BOM report does
not require a duplicate source-index section because its causal-node tables are the
claim-level index; `sources.jsonl` remains the structured audit ledger.

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

1. HTML is the default public artifact; Markdown is the audit sidecar.
2. Default industry/project reports keep four numbered H2 sections in exact order; `standalone-bom` keeps the five locked lenses in exact order.
3. Parent, manifest, and child paths preserve one-to-one BOM identity.
4. BOM ID and public name come from the canonical registry.
5. Every `bom-node` child keeps the same six semantic questions; every `standalone-bom` keeps the five professional lenses.
6. Every six-question module keeps its temporal sequence; every logic-chain-centered standalone report keeps `当前投资判断`, then each lens keeps `第一性原理逻辑链 -> 逻辑节点与原子观点材料 -> 可选派生证据视图`, visibly renders the exact research question on every L3 node, and keeps one five-column claim-level source table per causal node, without a separate lens-level `全局结论与趋势`.
7. Backtest cutoff and label isolation remain enforced.
8. Public reports contain no raw process traces or change logs.
9. When requested, the dedicated plan Markdown preserves exact L3 coverage and renders
   every current terminal question; broad-material counts never imply completion.

## Validation

Before publication:

1. run focused tests and the full research-framework suite;
2. run `validate-report-contract` on `professional_report.html` and the Markdown sidecar;
3. run `validate-material-intake` when intake artifacts exist;
4. run `validate-research-artifacts --require-l3` when artifacts exist;
5. verify scope-specific section order, parent-child links where applicable, six-question or five-lens identity, newest-to-oldest causal-node material tables, parallel claim/effect numbering, source links, and no public process text;
6. run `git diff --check`.
7. when `research_plan.md` is present, verify exact L3/leaf counts, maximum depth
   five, parent-child continuity, leaf data and analysis requirements, and status
   derived from the append-only child ledgers.

HTML visual and contract validation is the publication gate; Markdown validation
protects audit portability.
