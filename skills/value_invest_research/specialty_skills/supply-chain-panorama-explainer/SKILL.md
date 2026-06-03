---
name: supply-chain-panorama-explainer
description: Use this skill when an investment research report needs to build or render the `产业链全景` section in beginner-readable Chinese. It turns the research goal into an upstream/midstream/downstream map, dependencies, value flow, chokepoints, QA mapping, data gaps, and target links that a non-specialist can understand before reading the QA tree.
---

# Supply-Chain Panorama Explainer

This skill turns a supply-chain map into a Chinese, beginner-readable investment map. Use it before Q1-Q4 question design and whenever rendering the public `产业链全景` section.

## Output Goal

After reading `产业链全景`, a new reader should be able to answer seven questions:

1. 当前研究目标如何转成产业链问题？
2. 这个行业/事件到底在卖什么产品或服务？
3. 谁在上游、中游、下游，各自负责什么？
4. 产品、订单、数据、认证、流量或资金是怎么传递的？
5. 哪些环节最稀缺、最难替代、最可能卡住整条链？
6. 哪些节点更可能捕获收入、毛利、现金流和估值赔率？
7. 哪些上市标的对应这些稀缺环节，哪些只是普通配套或宽基暴露？

## Language Rules

- Public text must be Simplified Chinese.
- Keep company names, tickers, product names, and standard abbreviations in their original form when needed, but immediately explain their role in Chinese.
- Avoid unexplained labels like `upstream`, `midstream`, `downstream`, `chokepoint`, `unit economics`, or `value capture` in visible prose. Prefer `上游`, `中游`, `下游`, `卡点/瓶颈`, `单机/单项目经济性`, `价值捕获`.
- Use short sentences. Prefer "谁 -> 给谁 -> 提供什么 -> 谁付钱 -> 谁赚钱" over dense sector jargon.
- Do not include framework-change notes, execution traces, or "本轮升级/本次新增" language.

## Required Public Blocks

Render these inside the existing `supply-chain-section`, preserving the canonical report shell:

- `chain-explain`: wrapper for the beginner explanation.
- `chain-research-bridge`: explain how the current research goal turns into supply-chain questions and Q1-Q4.
- `chain-node-lens`: node-screening lens covering demand flow, scarcity, substitution difficulty, monetization, market pricing, and disconfirming trigger.
- `chain-plain-summary`: one-paragraph plain Chinese summary answering "这条产业链一句话是什么".
- `chain-relationship-workbench` with `chain-view-switch`: a coordinated relationship workbench whose default view is `chain-lane-map`; it must also expose `chain-sankey-map` and `chain-chokepoint-heatmap`.
- `chain-lane-map`: upstream/midstream/downstream swimlane view with expandable company/node cards showing what each node receives, produces, and provides.
- `chain-sankey-map`: value/order flow view showing how demand, orders, supply, delivery, revenue, margin, and ROI verification move through the chain.
- `chain-chokepoint-heatmap`: bottleneck score view showing scarcity, substitution difficulty, pricing power, financial elasticity, valuation risk, and disconfirming risk.
- `chain-value-capture-matrix`: table by node showing demand flow, chokepoint mechanism, monetization, targets, verification data, and QA link.
- `chain-qa-mapping`: cards linking supply-chain findings to Q1-Q4 questions.
- `chain-data-gaps`: compact list of missing data required before strengthening QA conclusions or target scores.
- `chain-flow-steps`: 3-7 numbered steps showing product/order/money/data flow.
- `chain-layer-grid` with `chain-layer-card`: cards for upstream, midstream, downstream, ecosystem/platform, customers, or other relevant layers.
- `chain-chokepoints`: concise list of candidate bottlenecks and why they matter.
- `chain-target-links`: table or chips linking each bottleneck to potential listed targets and the Q2/Q4 nodes that will test it.
- Existing `chain-map` or `chain-table`: keep the auditable structured map; the readable blocks explain it, not replace it.

## Internal Schema

Use this structure in workbench artifacts when possible:

```json
{
  "plain_summary": "一句话说明这条产业链如何运转",
  "research_bridge": {
    "objective": "当前研究目标如何转成产业链问题",
    "core_question": "核心供应链投资问题",
    "current_conclusion": "产业链前置结论",
    "output_to_qa": [["Q1", "问题方向", "产业链输入"]]
  },
  "node_lenses": [["需求流入", "判断标准"]],
  "value_capture_matrix": [
    {
      "node": "节点",
      "demand": "需求如何流入",
      "chokepoint": "卡点机制",
      "monetization": "价值捕获方式",
      "targets": "主要标的",
      "verification": "需要继续验证的数据",
      "qa": "Qx.y"
    }
  ],
  "qa_mapping": [
    {"q": "Q1", "signal": "产业链信号", "use": "如何改变研究问题"}
  ],
  "data_gaps": ["关键缺口"],
  "flow_steps": [
    {"step": 1, "label": "需求从哪里来", "plain_chinese": "终端客户为什么需要这个产品/服务"}
  ],
  "layers": [
    {
      "layer": "上游",
      "role": "提供什么",
      "players": ["公司或资产"],
      "depends_on": "依赖谁",
      "paid_by": "谁付钱",
      "profit_pool": "利润/现金流在哪里",
      "beginner_note": "给新手的白话解释"
    }
  ],
  "candidate_chokepoints": [
    {
      "node": "卡点名称",
      "why_scarce": "为什么稀缺/难替代",
      "who_controls_it": ["公司或资产"],
      "how_to_verify": "后续用什么数据验证",
      "qa_link": "Q2.x / Q4.x"
    }
  ],
  "target_links": [
    {
      "target": "ticker/name",
      "chain_node": "对应链条节点",
      "exposure_type": "直接价值捕获 / 间接配套 / 宽基暴露",
      "first_question": "最先要验证的问题"
    }
  ]
}
```

## Quality Gates

- If the section reads like a sell-side terminology table, rewrite it.
- If a reader cannot identify who pays whom and who captures margin, rewrite it.
- If all companies look equally important, add the bottleneck/替代性 distinction.
- If the section cannot feed Q2 chokepoint scoring and Q4 target ranking, it is incomplete.
- Keep the explanation neutral: a clear chain map does not itself justify a long recommendation.
