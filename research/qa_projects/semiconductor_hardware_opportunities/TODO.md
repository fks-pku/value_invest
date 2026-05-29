# 半导体硬件投资机会研究待办清单

更新时间：2026-05-28

## 当前状态

- 报告主文件：`professional_report.html`
- Markdown 备份：`professional_report.md`
- QA 树：`qa_tree.json`
- 证据库：`evidence.jsonl`
- 工作底稿：`investment_workbench.json`
- 当前框架：只保留 QA 层级，不再使用 Step、工作台附录、完整报告等并列模块。
- 当前主层级：Q1 需求、Q2 瓶颈、Q3 定价与风险、Q4 标的。

## 已完成

- [x] 建立 Q1-Q4 QA 层级。
- [x] 补充 Q2 瓶颈评分卡，并把评分卡放在 Q2.1 内部。
- [x] 补充 Q3 红黄绿反证触发器、季度更新底稿、节点级反证绑定矩阵。
- [x] 补充 Q4 标的观察清单、估值/赔率快照、中国链条财务质量、动态强度调整表。
- [x] Q4.1.6 标的研究优先级矩阵。
- [x] Q1.1.3 需求质量二次拆分。
- [x] Q2.1.9 瓶颈节点详情页补强。
- [x] Q3.1.6 反证执行清单。
- [x] 证据库增强：新增 6 条 evidence，覆盖 NVIDIA 10-Q、SEMI 300mm Fab Outlook、Micron FQ2、Samsung 1Q26 presentation、BIS/Federal Register 规则、ASML 财报监控入口，并绑定到对应 QA 节点。
- [x] 视觉与交互二次优化：L3 顶部 qa-meta 统一展示并 sticky；新增证据增强包表格；长表继续保留横向滚动。

## 本轮核心节点验收口径

### Q4.1.6 标的研究优先级矩阵

- 覆盖优先级：核心跟踪、高优先级、验证型、线索型。
- 包含瓶颈暴露、财务兑现证据、赔率约束、主要反证、研究优先级、下一季必查数据。
- 明确这是研究覆盖优先级，不是买卖建议。

### Q1.1.3 需求质量二次拆分

- 区分真实算力硬件、组件涨价、数据中心土建/电力网络、RPO/backlog 与客户预付款、现金流压力。
- 明确 Cloud 收入、RPO 转收入、客户预付款、GPU/ASIC/networking 订单和供给约束是更高质量需求证据。

### Q2.1.9 瓶颈节点详情页补强

- 覆盖 AI 加速器/custom ASIC/networking、HBM/高端存储、CoWoS/先进封装、全球设备、中国设备、内存接口/CXL/PCIe。
- 每个节点均补充产业链位置、约束变量、利润捕获者、财务科目映射、关键标的、降级触发器、待补数据。

### Q3.1.6 反证执行清单

- 覆盖云厂 capex 质量、HBM ASP/库存、设备订单/backlog、估值与 EPS/FCF、出口管制、中国设备财务质量。
- 每个审计项均有数据来源、绿灯标准、黄灯标准、红灯标准、影响的 Q2 节点和 Q4 标的。

## 证据增强验收

- 新增 evidence 数：6。
- 新增后证据总数：47。
- 信息类型覆盖：evidence、research_report、regulatory rule、monitor lead。
- 每条新增证据均写入 `evidence.jsonl`。
- 每条新增证据均绑定到 `qa_tree.json` 对应节点的 `evidence_ids`。
- HTML / Markdown 已在对应 L3 节点和来源索引中补充来源链接。

## 视觉与交互验收

- Q1-Q4 主卡片保留默认展开。
- L3 默认折叠。
- 关键表格保留横向滚动。
- 每个 L3 顶部展示：本问题结论、证据数量、反证/触发器、下一步数据。
- L3 顶部元信息条设为 sticky，长表阅读时保留上下文。
- 过长表格仍归属于对应 QA 节点，不作为独立 appendix。

## 后续常规维护

后续不再作为本轮阻断 TODO；当下一季财报、订单/backlog、HBM ASP、CoWoS 产能、出口管制或估值快照更新时，按同一证据 schema 追加 evidence，并重新跑结构校验。

## 校验命令

```bash
node -e "const fs=require('fs'); const base='research/qa_projects/semiconductor_hardware_opportunities'; const qa=JSON.parse(fs.readFileSync(base+'/qa_tree.json','utf8')); const ev=fs.readFileSync(base+'/evidence.jsonl','utf8').trim().split(/\n/).filter(Boolean).map(JSON.parse); const html=fs.readFileSync(base+'/professional_report.html','utf8'); const evIds=new Set(ev.map(e=>e.id)); const nodeIds=new Set(qa.nodes.map(n=>n.id)); const missingRefs=[]; const missingChildren=[]; for (const n of qa.nodes){ for (const id of n.evidence_ids||[]) if(!evIds.has(id)) missingRefs.push([n.id,id]); for (const id of n.next_question_ids||[]) if(!nodeIds.has(id)) missingChildren.push([n.id,id]); } const detailsStart=(html.match(/<details/g)||[]).length; const detailsClose=(html.match(/<\/details>/g)||[]).length; console.log(JSON.stringify({evidence_count:ev.length, qa_nodes:qa.nodes.length, missingRefs, missingChildren, detailsStart, detailsClose, detailsBalanced:detailsStart===detailsClose}, null, 2));"
```
