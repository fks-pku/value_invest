---
name: supply-chain-panorama-explainer
description: Use this skill when an investment research report needs to build or render the `产业链全景` section in beginner-readable Chinese. It turns upstream/midstream/downstream maps, dependencies, value flow, chokepoints, and target links into a clear Chinese explanation that a non-specialist can understand before reading the QA tree.
---

# Supply-Chain Panorama Explainer

This skill turns a supply-chain map into a Chinese, beginner-readable investment map. Use it before Q1-Q4 question design and whenever rendering the public `产业链全景` section.

## Output Goal

After reading `产业链全景`, a new reader should be able to answer five questions:

1. 这个行业/事件到底在卖什么产品或服务？
2. 谁在上游、中游、下游，各自负责什么？
3. 产品、订单、数据、认证、流量或资金是怎么传递的？
4. 哪些环节最稀缺、最难替代、最可能卡住整条链？
5. 哪些上市标的对应这些稀缺环节，哪些只是普通配套或宽基暴露？

## Language Rules

- Public text must be Simplified Chinese.
- Keep company names, tickers, product names, and standard abbreviations in their original form when needed, but immediately explain their role in Chinese.
- Avoid unexplained labels like `upstream`, `midstream`, `downstream`, `chokepoint`, `unit economics`, or `value capture` in visible prose. Prefer `上游`, `中游`, `下游`, `卡点/瓶颈`, `单机/单项目经济性`, `价值捕获`.
- Use short sentences. Prefer "谁 -> 给谁 -> 提供什么 -> 谁付钱 -> 谁赚钱" over dense sector jargon.
- Do not include framework-change notes, execution traces, or "本轮升级/本次新增" language.

## Required Public Blocks

Render these inside the existing `supply-chain-section`, preserving the canonical report shell:

- `chain-explain`: wrapper for the beginner explanation.
- `chain-plain-summary`: one-paragraph plain Chinese summary answering "这条产业链一句话是什么".
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
