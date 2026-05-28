# 半导体硬件投资机会研究待办清单

更新时间：2026-05-28

## 当前状态

- 报告主文件：`professional_report.html`
- Markdown 备份：`professional_report.md`
- QA 树：`qa_tree.json`
- 证据库：`evidence.jsonl`
- 工作底稿：`investment_workbench.json`
- 当前框架：只保留 QA 层级，不再使用 Step、工作台附录、完整报告等并列模块。
- 当前主层级：
  - Q1 需求：AI 基础设施是否仍在真实拉动半导体硬件需求？
  - Q2 瓶颈：产业链哪些环节最可能捕获增量利润？
  - Q3 定价与风险：市场是否已经把机会打满，哪些风险会证伪？
  - Q4 标的：哪些具体证券应进入观察清单，强度和风险如何排序？

## 已完成

- 建立 Q1-Q4 QA 层级。
- 补充 Q2 瓶颈评分卡，并把评分卡放在 Q2.1 内部。
- 补充 Q3 红黄绿反证触发器、季度更新底稿、节点级反证绑定矩阵。
- 补充 Q4 标的观察清单、估值/赔率快照、中国链条财务质量、动态强度调整表。
- 做过视觉收尾：Apple 风格、层级强化、L3 默认折叠、表格可读性优化。
- 最近一次结构校验通过：41 条证据、29 个 QA 节点、HTML details 标签平衡、无证据断链。

## 后续优先待办

### 1. Q4.1.6 标的研究优先级矩阵

目的：把“标的观察清单”升级成“研究团队覆盖优先级”，明确先研究谁、为什么、需要什么验证数据。

放置位置：

- `Q4 标的`
- `Q4.1 全球瓶颈龙头和中国国产替代标的分别如何筛选？`
- 新增 `Q4.1.6 哪些标的应优先进入深度覆盖，研究强度如何排序？`

建议输出：

- 核心跟踪：NVDA、TSM
- 高优先级：AVGO、ASML、HBM 组合
- 验证型：MRVL、AMAT/LRCX/KLAC、中国设备链、澜起科技
- 线索型：长电科技，直到先进封装收入重新放量

必须包含：

- 瓶颈暴露
- 财务兑现证据
- 赔率约束
- 主要反证
- 研究优先级
- 下一季必查数据

注意：

- 这是研究覆盖优先级，不是买卖建议。
- DeepSeek 可用于逐条整理已给材料，但最终优先级判断由 GPT 完成。

### 2. Q2.1.9 瓶颈节点详情页补强

目的：让每个瓶颈节点不只是评分，而是有完整的投资逻辑闭环。

放置位置：

- `Q2 瓶颈`
- `Q2.1 哪些节点有瓶颈属性和财务敞口？`
- 新增或扩展 Q2.1.x 节点详情页

优先节点：

- AI 加速器 / custom ASIC / networking
- HBM / 高端存储
- CoWoS / 先进封装
- 设备链：ASML、AMAT、LRCX、KLAC
- 中国设备：北方华创、中微公司
- 内存接口 / CXL：澜起科技

每个节点要补：

- 产业链位置
- 约束变量
- 谁捕获利润
- 财务科目映射
- 关键标的
- 降级触发器
- 待补数据

### 3. Q3.1.6 反证执行清单

目的：把 Q3 反证从“知道风险”升级成“每季怎么执行审计”。

放置位置：

- `Q3 定价与风险`
- `Q3.1 主要反证来自 AI capex、存储周期、出口管制还是估值拥挤？`
- 新增 `Q3.1.6 每季如何执行反证审计？`

建议输出：

- 云厂 capex 审计表
- HBM ASP / 库存审计表
- 设备订单 / backlog 审计表
- 估值与 EPS/FCF 修正审计表
- 出口管制变更审计表

每个审计项要有：

- 数据来源
- 绿灯标准
- 黄灯标准
- 红灯标准
- 影响的 Q2 节点
- 影响的 Q4 标的

### 4. Q1.1.3 需求质量二次拆分

目的：区分真实算力增量、组件涨价、数据中心土建、客户预付款和 RPO/backlog。

放置位置：

- `Q1 需求`
- `Q1.1 AI capex 如何传导到芯片、存储、网络和设备？`
- 新增 `Q1.1.3 AI capex 中哪些是真实硬件需求，哪些只是价格或土建放大？`

建议补充：

- Microsoft capex 中组件涨价口径
- Amazon PPE 与 FCF 压力
- Alphabet capex、Cloud revenue、RPO
- Oracle RPO、客户预付款、自供 GPU
- Meta capex 和数据中心成本

输出形式：

- capex 质量拆分表
- 支撑 Q2 的真实硬件需求链
- 会削弱 Q2 的名义 capex 放大项

### 5. 证据库增强

目的：让后续结论更可审计。

待补信息类型：

- 研报：AI 半导体、HBM、CoWoS、设备、国产替代、CXL/PCIe
- 官方证据：财报、法说、订单/backlog、年报、交易所公告
- 消息：客户订单、认证、扩产节奏、价格变化
- 观点：产业专家、卖方分歧、反方观点

每条新证据必须写入：

- `evidence.jsonl`
- `qa_tree.json` 对应节点的 `evidence_ids`
- HTML / Markdown 对应 L3 节点的来源链接

### 6. 视觉与交互二次优化

目的：减少报告阅读负担。

建议：

- Q1-Q4 主卡片保留默认展开。
- L2 汇总默认展开。
- L3 默认折叠。
- 关键表格保留横向滚动。
- 每个 L3 顶部固定显示：本问题结论、证据数量、反证数量、下一步数据。
- 如果某个 L3 超过 2 个大表，考虑拆成详情页，但详情页仍归属于对应 QA 节点。

## 下次继续时的建议顺序

1. 先做 `Q4.1.6 标的研究优先级矩阵`。
2. 再做 `Q1.1.3 capex 质量拆分`，避免 Q2/Q4 继续建立在粗糙需求假设上。
3. 再做 `Q2.1.9 瓶颈节点详情页补强`。
4. 最后做 `Q3.1.6 反证执行清单`，形成季度更新机制。

## 校验命令

```bash
node -e "const fs=require('fs'); const base='research/qa_projects/semiconductor_hardware_opportunities'; const qa=JSON.parse(fs.readFileSync(base+'/qa_tree.json','utf8')); const ev=fs.readFileSync(base+'/evidence.jsonl','utf8').trim().split(/\n/).filter(Boolean).map(JSON.parse); const html=fs.readFileSync(base+'/professional_report.html','utf8'); const evIds=new Set(ev.map(e=>e.id)); const nodeIds=new Set(qa.nodes.map(n=>n.id)); const missingRefs=[]; const missingChildren=[]; for (const n of qa.nodes){ for (const id of n.evidence_ids||[]) if(!evIds.has(id)) missingRefs.push([n.id,id]); for (const id of n.next_question_ids||[]) if(!nodeIds.has(id)) missingChildren.push([n.id,id]); } const detailsStart=(html.match(/<details/g)||[]).length; const detailsClose=(html.match(/<\/details>/g)||[]).length; console.log(JSON.stringify({evidence_count:ev.length, qa_nodes:qa.nodes.length, missingRefs, missingChildren, detailsStart, detailsClose, detailsBalanced:detailsStart===detailsClose}, null, 2));"
```
