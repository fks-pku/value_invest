---
report_scope: bom-node
project_id: ai_factory_industry_scurve_timeslice_20260328__bom__manufacturing
bom_node_id: manufacturing
run_mode: historical_backtest
as_of_date: 2026-03-28
---

# AI 工厂 · 先进制程与先进封装 BOM 节点研究

[返回 AI 工厂产业总览](../../professional_report.md)

> 研究截面：2026-03-28。本报告只研究 先进制程与先进封装，不把其他 BOM 的结论提前扩散到本节点。

## 1. 当前研究的问题

判断 先进制程与先进封装 是否处在可投资的 S 曲线阶段，并识别需求、供给、控制权、财务兑现、市场定价和反证的证据边界。

| 节点边界 | 内容 |
| --- | --- |
| 接受什么 | GPU/ASIC 设计、先进节点 wafer 订单、HBM 集成需求。 |
| 生产什么 | 先进晶圆制造、CoWoS 类先进封装、良率和产能。 |
| 提供给谁 | GPU/ASIC 平台方和高端内存/系统供应链。 |
| 代表公司 | TSMC、先进封装生态、设备/材料供应商 |
| 验证指标 | advanced technologies revenue share、capex、gross margin、先进封装产能。 |

## 2. 行业概况

### 先进制程与先进封装

决定高端 GPU/ASIC 能否被制造出来并和 HBM 组合成可交付芯片。

**研究账本说明：** 六问是稳定逻辑坐标；材料按市场可见时间追加到 `BOM × 六问 × 时间` 账本。本报告只展示结论、真实变化和可审计材料，不展示搜索词、解析提示或工具过程。

### Q1 · 当前 BOM 的需求是否会被 S 曲线放大拉动？

**结论强度：** 待验证  
**最近材料：** 2026-01-15

#### 基本理解思路

- **专业模型：** S 曲线传导与弹性模型
- **研究目的：** 判断终端 AI 需求是否真实传导到当前 BOM，并且是否具备大于终端需求的弹性。
- **判断规则：** 可投资需求 = 真实工作负载增长 × 客户预算/订单兑现 × 先进制程与先进封装 直接拉动 × 单位用量或单位价值量弹性。
- **理解提示：** 制造需求是否穿透到 TSMC → 先进封装是否成为 GPU/HBM 集成刚需 → 缺口与监控 3 → 缺口与监控 4

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

先进制程与先进封装的需求增长来自 GPU/ASIC 平台放量和 HBM 集成复杂度上升。TSMC Q4 2025 的高收入、高毛利、高 advanced technologies 占比，以及 2026 高 capex 指引，说明需求已经穿透到制造供给层；但 CoWoS/先进封装的直接产能、交期和价格仍是缺口。

**支持机制：** 只要 GPU/ASIC 平台继续走向更大 die、更高 HBM 带宽和 rack-scale 集成，先进制程与先进封装的需求会随有效供给链继续放大。

**最大反证：** 如果架构优化降低先进封装复杂度，或 capex 快速释放导致 CoWoS/HBM 供给宽松，高毛利和稀缺性会下降。

**对标的的影响：** 本问决定 先进制程与先进封装 相关标的是否有足够大的收入天花板和增长斜率。若需求链条不能从工作负载穿透到订单、收入和 BOM 弹性，即使公司质量好，也只能保留观察；若需求强成立，后续才值得继续评估供给稀缺、控制者和定价。

**关键来源：** [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)；[TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 先进制程与先进封装的需求增长来自 GPU/ASIC 平台放量和 HBM 集成复杂度上升。TSMC Q4 2025 的高收入、高毛利、高 advanced technologies 占比，以及 2026 高 capex 指引，说明需求已经穿透到制造供给层；但 CoWoS/先进封装的直接产能、交期和价格仍是缺口。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 事实 / 支持 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 事实 / 支持 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 事实 / 支持 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 事实 / 支持 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 预测 / 支持 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 预测 / 支持 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 事实 / 支持 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 预测 / 支持 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 |

时间线先展示最早 12 条；完整 23 条见“映射材料”。

#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 制造需求是否穿透到 TSMC | [TSMC Q4 2025 revenue $33.73B、gross margin 62.3%、advanced technologies 77% of wafer revenue](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 [TSMC Q1 2026 revenue guide $34.6B-$35.8B、gross margin guide 63%-65%](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 制造需求是否穿透到 TSMC | [TSMC 2026 capital budget expected $52B-$56B](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)，说明先进制造/封装供给仍在高强度扩张。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 制造需求是否穿透到 TSMC | [Revenue $33.73B，gross margin 62.3%，advanced technologies 77%](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 [Q1 revenue $34.6B-$35.8B，gross margin 63%-65%；2026 capex $52B-$56B](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 Q1 指引验证近端需求，capex 验证供给释放；两者都不能直接等同于 CoWoS 产能。 | Q4 2025 | Q1 2026E / FY2026E |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 先进封装是否成为 GPU/HBM 集成刚需 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 先进封装是否成为 GPU/HBM 集成刚需 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | TSMC Q4 2025 revenue was $33.73B, gross margin 62.3%, advanced technologies were 77% of wafer revenue, and 2026 capex was expected at $52B-$56B. | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 先进封装是否成为 GPU/HBM 集成刚需 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 先进封装是否成为 GPU/HBM 集成刚需 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 先进封装是否成为 GPU/HBM 集成刚需 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 | 2023-2024 | 后续平台周期 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | SemiAnalysis mapped GB200 rack-scale architecture and component implications, including that many data centers cannot support very high rack density without direct-to-chip liquid cooling. | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 先进封装是否成为 GPU/HBM 集成刚需 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 先进封装是否成为 GPU/HBM 集成刚需 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 先进封装是否成为 GPU/HBM 集成刚需 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 | 2023-2024 | 后续平台周期 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 13 | 0 | 0 | 0 | 0 | 23 | 0 | 2023-07-05 | 2026-01-15 | 单向覆盖，缺反证 |

### Q2 · 供给能否跟上？

**结论强度：** 待验证  
**最近材料：** 2026-01-15

#### 基本理解思路

- **专业模型：** 产能 / 良率 / 周期 / 认证模型
- **研究目的：** 判断有效供给释放速度是否慢于需求斜率。
- **判断规则：** 有效供给 = 名义产能 × 良率 × 客户认证 × 设备/材料可得性 × 交付周期；若有效供给斜率低于需求斜率，先进制程与先进封装 才具备稀缺性。
- **理解提示：** 名义扩产与财务强度 → 有效产能串联约束 → 缺口与监控 3 → 缺口与监控 4

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

先进制程与先进封装供给仍受有效产能、良率、设备、客户认证和 capex 周期约束。TSMC 2026 capex $52B-$56B 说明供给会扩张，但扩张不等于即时有效产能；CoWoS/HBM 的专业拆解仍提示先进封装是 AI accelerator 的串联约束。

**支持机制：** 供给约束持续的机制是高端封装和先进节点扩产、良率、认证慢于客户需求斜率。

**最大反证：** 如果 capex 快速变成有效产能、交期缩短、价格松动或客户转向替代封装，供给瓶颈会降级。

**对标的的影响：** 本问决定 先进制程与先进封装 是否具备 chokepoint 属性。供给跟不上时，控制有效产能和认证资源的公司才可能获得价格、毛利和 backlog 弹性；如果供给快速释放，标的推荐应从“稀缺溢价”降为“行业 beta”。

**关键来源：** [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)；[TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 先进制程与先进封装供给仍受有效产能、良率、设备、客户认证和 capex 周期约束。TSMC 2026 capex $52B-$56B 说明供给会扩张，但扩张不等于即时有效产能；CoWoS/HBM 的专业拆解仍提示先进封装是 AI accelerator 的串联约束。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 事实 / 支持 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 事实 / 支持 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 事实 / 支持 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 事实 / 支持 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 预测 / 支持 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 预测 / 支持 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 事实 / 支持 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 预测 / 支持 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 |

时间线先展示最早 12 条；完整 23 条见“映射材料”。

#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 名义扩产与财务强度 | [TSMC Q4 2025 revenue $33.73B、gross margin 62.3%、advanced technologies 77% of wafer revenue](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 [TSMC Q1 2026 revenue guide $34.6B-$35.8B、gross margin guide 63%-65%](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 名义扩产与财务强度 | [TSMC 2026 capital budget expected $52B-$56B](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)，说明先进制造/封装供给仍在高强度扩张。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 名义扩产与财务强度 | [Revenue $33.73B，gross margin 62.3%，advanced technologies 77%](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 [Q1 revenue $34.6B-$35.8B，gross margin 63%-65%；2026 capex $52B-$56B](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 Q1 指引验证近端需求，capex 验证供给释放；两者都不能直接等同于 CoWoS 产能。 | Q4 2025 | Q1 2026E / FY2026E |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 有效产能串联约束 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 有效产能串联约束 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | TSMC Q4 2025 revenue was $33.73B, gross margin 62.3%, advanced technologies were 77% of wafer revenue, and 2026 capex was expected at $52B-$56B. | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 有效产能串联约束 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 有效产能串联约束 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 有效产能串联约束 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 | 2023-2024 | 后续平台周期 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | SemiAnalysis mapped GB200 rack-scale architecture and component implications, including that many data centers cannot support very high rack density without direct-to-chip liquid cooling. | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 有效产能串联约束 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 有效产能串联约束 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 有效产能串联约束 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 | 2023-2024 | 后续平台周期 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 13 | 0 | 0 | 0 | 0 | 23 | 0 | 2023-07-05 | 2026-01-15 | 单向覆盖，缺反证 |

### Q3 · 谁控制供给？

**结论强度：** 待验证  
**最近材料：** 2026-01-15

#### 基本理解思路

- **专业模型：** 份额 / 壁垒 / 替代 / 客户锁定模型
- **研究目的：** 判断稀缺供给是否被少数公司控制，并能转成利润池。
- **判断规则：** 控制权 = 份额集中度 + 资格/认证壁垒 + 技术/IP/生态壁垒 + 客户锁定 - 替代与多供速度。
- **理解提示：** TSMC 是否控制关键制造环节 → 替代难度来自哪里 → 缺口与监控 3 → 缺口与监控 4

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

供给控制权集中在 TSMC 及其先进封装生态，但这种控制权不是只看市场份额，而要看先进节点、封装能力、良率、客户认证和交付可靠性。当前公开证据能证明 TSMC 是核心控制者，但还不足以量化各类先进封装产能份额。

**支持机制：** 控制权持续来自先进节点、先进封装 know-how、客户认证、规模经验和生态配套。

**最大反证：** 若客户多供应、OSAT/竞争代工追赶、或替代封装路线成熟，TSMC 控制权和稀缺溢价会被稀释。

**对标的的影响：** 本问决定推荐应落到哪些具体公司。只有能控制合格供给、客户资格、生态或交付能力的公司，才可能把 先进制程与先进封装 的需求增长转成超额利润；份额分散或替代加速时，不应把整个节点的增长平均分配给所有玩家。

**关键来源：** [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)；[TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 供给控制权集中在 TSMC 及其先进封装生态，但这种控制权不是只看市场份额，而要看先进节点、封装能力、良率、客户认证和交付可靠性。当前公开证据能证明 TSMC 是核心控制者，但还不足以量化各类先进封装产能份额。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 事实 / 支持 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 事实 / 支持 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 事实 / 支持 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 事实 / 支持 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 预测 / 支持 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 预测 / 支持 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 事实 / 支持 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 预测 / 支持 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 |

时间线先展示最早 12 条；完整 23 条见“映射材料”。

#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | TSMC 是否控制关键制造环节 | [TSMC Q4 2025 revenue $33.73B、gross margin 62.3%、advanced technologies 77% of wafer revenue](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 [TSMC Q1 2026 revenue guide $34.6B-$35.8B、gross margin guide 63%-65%](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | TSMC 是否控制关键制造环节 | [TSMC 2026 capital budget expected $52B-$56B](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)，说明先进制造/封装供给仍在高强度扩张。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | TSMC 是否控制关键制造环节 | [Revenue $33.73B，gross margin 62.3%，advanced technologies 77%](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 [Q1 revenue $34.6B-$35.8B，gross margin 63%-65%；2026 capex $52B-$56B](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 Q1 指引验证近端需求，capex 验证供给释放；两者都不能直接等同于 CoWoS 产能。 | Q4 2025 | Q1 2026E / FY2026E |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 替代难度来自哪里 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 替代难度来自哪里 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | TSMC Q4 2025 revenue was $33.73B, gross margin 62.3%, advanced technologies were 77% of wafer revenue, and 2026 capex was expected at $52B-$56B. | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 替代难度来自哪里 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 替代难度来自哪里 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 替代难度来自哪里 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 | 2023-2024 | 后续平台周期 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | SemiAnalysis mapped GB200 rack-scale architecture and component implications, including that many data centers cannot support very high rack density without direct-to-chip liquid cooling. | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 替代难度来自哪里 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 替代难度来自哪里 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 替代难度来自哪里 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 | 2023-2024 | 后续平台周期 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 13 | 0 | 0 | 0 | 0 | 23 | 0 | 2023-07-05 | 2026-01-15 | 单向覆盖，缺反证 |

### Q4 · 是否已经财务兑现？

**结论强度：** 待验证  
**最近材料：** 2026-01-15

#### 基本理解思路

- **专业模型：** 收入 / 毛利 / backlog / 现金流模型
- **研究目的：** 判断产业逻辑是否已经进入公司财务，而不是停留在叙事或订单新闻。
- **判断规则：** 财务兑现 = 收入增长 + backlog/RPO 可见度 + 毛利/ASP 改善 + 经营现金流质量 - 库存/应收/取消风险。
- **理解提示：** 收入和毛利是否兑现 → 封装瓶颈是否能解释财务强度 → 缺口与监控 3 → 缺口与监控 4

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

财务兑现已经较强：TSMC Q4 2025 revenue $33.73B、gross margin 62.3%、advanced technologies 77%，Q1 2026 revenue/gross margin guide 也继续强。问题是这仍是公司整体/先进技术口径，不是 AI 先进封装单独收入；所以可以证明高端制造强，但不能精确证明 CoWoS 利润池大小。

**支持机制：** 如果 advanced technologies 占比和 gross margin 持续高位，同时 capex 能带来高回报，财务兑现可持续。

**最大反证：** 如果 capex 回报下行、产能释放压低毛利、或地缘/客户转单影响利用率，财务兑现质量会下降。

**对标的的影响：** 本问决定标的确定性。收入、毛利、backlog 和现金流已经兑现的公司可进入更高置信候选；只有订单新闻、没有利润和现金兑现的公司，需要降低推荐强度并提高监控频率。

**关键来源：** [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)；[TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 财务兑现已经较强：TSMC Q4 2025 revenue $33.73B、gross margin 62.3%、advanced technologies 77%，Q1 2026 revenue/gross margin guide 也继续强。问题是这仍是公司整体/先进技术口径，不是 AI 先进封装单独收入；所以可以证明高端制造强，但不能精确证明 CoWoS 利润池大小。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 事实 / 支持 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 事实 / 支持 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 事实 / 支持 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 事实 / 支持 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 预测 / 支持 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 预测 / 支持 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 事实 / 支持 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 预测 / 支持 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 |

时间线先展示最早 12 条；完整 23 条见“映射材料”。

#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 收入和毛利是否兑现 | [TSMC Q4 2025 revenue $33.73B、gross margin 62.3%、advanced technologies 77% of wafer revenue](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 [TSMC Q1 2026 revenue guide $34.6B-$35.8B、gross margin guide 63%-65%](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 收入和毛利是否兑现 | [TSMC 2026 capital budget expected $52B-$56B](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)，说明先进制造/封装供给仍在高强度扩张。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 收入和毛利是否兑现 | [Revenue $33.73B，gross margin 62.3%，advanced technologies 77%](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 [Q1 revenue $34.6B-$35.8B，gross margin 63%-65%；2026 capex $52B-$56B](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 Q1 指引验证近端需求，capex 验证供给释放；两者都不能直接等同于 CoWoS 产能。 | Q4 2025 | Q1 2026E / FY2026E |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 封装瓶颈是否能解释财务强度 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 封装瓶颈是否能解释财务强度 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | TSMC Q4 2025 revenue was $33.73B, gross margin 62.3%, advanced technologies were 77% of wafer revenue, and 2026 capex was expected at $52B-$56B. | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 封装瓶颈是否能解释财务强度 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 封装瓶颈是否能解释财务强度 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 封装瓶颈是否能解释财务强度 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 | 2023-2024 | 后续平台周期 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | SemiAnalysis mapped GB200 rack-scale architecture and component implications, including that many data centers cannot support very high rack density without direct-to-chip liquid cooling. | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 封装瓶颈是否能解释财务强度 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 封装瓶颈是否能解释财务强度 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 封装瓶颈是否能解释财务强度 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 | 2023-2024 | 后续平台周期 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 缺口与监控 4 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 13 | 0 | 0 | 0 | 0 | 23 | 0 | 2023-07-05 | 2026-01-15 | 单向覆盖，缺反证 |

### Q5 · 市场是否已定价？

**结论强度：** 待验证  
**最近材料：** 2026-01-15

#### 基本理解思路

- **专业模型：** 估值 / 预期差 / 盈利上修模型
- **研究目的：** 判断好产业是否仍是好赔率。
- **判断规则：** 赔率 = 未来盈利上修空间 ÷ 已定价增长与风险溢价；产业强度必须超过市场隐含预期才有推荐价值。
- **理解提示：** 基本面预期是否强 → 估值赔率缺口 → 缺口与监控 3 → 缺口与监控 4

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

市场对 TSMC 的强需求和高 capex 有预期，但本报告当前缺少 as-of 2026-03-28 的 forward PE、EPS revision、capex ROI 和地缘折价量化表，因此只能判断“基本面强、估值赔率待验证”。不能因为 TSMC 是瓶颈就直接推出买入结论。

**支持机制：** 若盈利上修持续超过估值隐含增长，且地缘风险没有扩大，赔率仍可能存在。

**最大反证：** 若市场已经充分计入高增长和高毛利，或 capex ROI/地缘风险恶化，赔率下降。

**对标的的影响：** 本问直接决定 action state。即使 先进制程与先进封装 是正确节点，如果估值和盈利预期已经充分反映，推荐只能是 watch_only；只有基本面继续超预期且估值未完全定价，才可能进入 actionable_long。

**关键来源：** [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)；[TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 市场对 TSMC 的强需求和高 capex 有预期，但本报告当前缺少 as-of 2026-03-28 的 forward PE、EPS revision、capex ROI 和地缘折价量化表，因此只能判断“基本面强、估值赔率待验证”。不能因为 TSMC 是瓶颈就直接推出买入结论。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 估值 / 支持 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 估值 / 支持 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 估值 / 支持 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 估值 / 支持 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 估值 / 支持 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 估值 / 支持 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 估值 / 支持 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 估值 / 支持 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 估值 / 支持 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 估值 / 支持 | SemiAnalysis mapped GB200 rack-scale architecture and component implications, including that many data centers cannot support very high rack density without direct-to-chip liquid cooling. |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 估值 / 支持 | [TSMC Q4 2025 revenue $33.73B、gross margin 62.3%、advanced technologies 77% of wafer revenue](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 [TSMC Q1 2026 revenue guide $34.6B-$35.8B、gross margin guide 63%-65%](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 估值 / 支持 | [TSMC 2026 capital budget expected $52B-$56B](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)，说明先进制造/封装供给仍在高强度扩张。 |

时间线先展示最早 12 条；完整 19 条见“映射材料”。

#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 基本面预期是否强 | [TSMC Q4 2025 revenue $33.73B、gross margin 62.3%、advanced technologies 77% of wafer revenue](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 [TSMC Q1 2026 revenue guide $34.6B-$35.8B、gross margin guide 63%-65%](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 基本面预期是否强 | [TSMC 2026 capital budget expected $52B-$56B](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)，说明先进制造/封装供给仍在高强度扩张。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 基本面预期是否强 | [Revenue $33.73B，gross margin 62.3%，advanced technologies 77%](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 [Q1 revenue $34.6B-$35.8B，gross margin 63%-65%；2026 capex $52B-$56B](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 Q1 指引验证近端需求，capex 验证供给释放；两者都不能直接等同于 CoWoS 产能。 | Q4 2025 | Q1 2026E / FY2026E |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 估值赔率缺口 | TSMC 基本面强，但估值赔率缺口未补齐。 维持 watch_only 口径，不从基本面强直接跳到高赔率。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 估值赔率缺口 | 下一轮应补 as-of consensus、forward PE、EPS revision、capex ROI 和地缘折价。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 缺口与监控 4 | TSMC Q4 2025 revenue was $33.73B, gross margin 62.3%, advanced technologies were 77% of wafer revenue, and 2026 capex was expected at $52B-$56B. | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 估值 / 支持 | 估值赔率缺口 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 | 2023-2024 | 后续平台周期 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 估值 / 支持 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 估值 / 支持 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 估值 / 支持 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 估值 / 支持 | 缺口与监控 4 | SemiAnalysis mapped GB200 rack-scale architecture and component implications, including that many data centers cannot support very high rack density without direct-to-chip liquid cooling. | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 估值 / 支持 | 估值赔率缺口 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 | 2023-2024 | 后续平台周期 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 估值 / 支持 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 估值 / 支持 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 估值 / 支持 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 估值 / 支持 | 缺口与监控 4 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 19 | 0 | 19 | 0 | 2023-07-05 | 2026-01-15 | 有材料，结构不完整 |

### Q6 · 反证是什么？

**结论强度：** 待验证  
**最近材料：** 2026-01-15

#### 基本理解思路

- **专业模型：** 触发器 / 阈值 / 降级动作模型
- **研究目的：** 把反证从泛泛风险变成可监控的降级纪律。
- **判断规则：** 反证强度 = 领先触发器变化 × 对需求/供给/控制权/财务/定价链条的破坏程度 × 可持续性。
- **理解提示：** 供给释放反证 → 封装瓶颈消退反证 → 缺口与监控 3 → 缺口与监控 4

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

核心反证是：CoWoS/先进封装扩产快于需求、良率改善导致稀缺性下降、客户多供应或替代封装路线成熟、TSMC capex 回报下降、gross margin guide 下行，或地缘风险导致客户转单。当前材料没有显示这些反证已经发生，但缺少交期、价格和客户 allocation 监控。

**支持机制：** 如果交期仍长、毛利率强、capex 仍高回报，反证未出现。

**最大反证：** 如果供给释放超过需求，短缺逻辑会先表现为交期缩短、ASP/毛利下降和 capex 回报走弱。

**对标的的影响：** 本问定义推荐纪律。先进制程与先进封装 相关标的必须绑定可观察降级触发器；当需求、供给、控制权、财务兑现或定价任一核心反证触发时，推荐强度应自动下调，而不是事后解释。

**关键来源：** [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)；[TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 核心反证是：CoWoS/先进封装扩产快于需求、良率改善导致稀缺性下降、客户多供应或替代封装路线成熟、TSMC capex 回报下降、gross margin guide 下行，或地缘风险导致客户转单。当前材料没有显示这些反证已经发生，但缺少交期、价格和客户 allocation 监控。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 反证 / 反证 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 反证 / 反证 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 反证 / 反证 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 反证 / 反证 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 反证 / 反证 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 反证 / 反证 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 反证 / 反证 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 反证 / 反证 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 反证 / 反证 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 反证 / 反证 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 反证 / 反证 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 反证 / 反证 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 |

时间线先展示最早 12 条；完整 23 条见“映射材料”。

#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 供给释放反证 | [TSMC Q4 2025 revenue $33.73B、gross margin 62.3%、advanced technologies 77% of wafer revenue](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 [TSMC Q1 2026 revenue guide $34.6B-$35.8B、gross margin guide 63%-65%](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 供给释放反证 | [TSMC 2026 capital budget expected $52B-$56B](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)，说明先进制造/封装供给仍在高强度扩张。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 供给释放反证 | [Revenue $33.73B，gross margin 62.3%，advanced technologies 77%](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 [Q1 revenue $34.6B-$35.8B，gross margin 63%-65%；2026 capex $52B-$56B](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm)。 Q1 指引验证近端需求，capex 验证供给释放；两者都不能直接等同于 CoWoS 产能。 | Q4 2025 | Q1 2026E / FY2026E |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 封装瓶颈消退反证 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 封装瓶颈消退反证 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2026-01-15 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 缺口与监控 4 | TSMC Q4 2025 revenue was $33.73B, gross margin 62.3%, advanced technologies were 77% of wafer revenue, and 2026 capex was expected at $52B-$56B. | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 封装瓶颈消退反证 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 封装瓶颈消退反证 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 封装瓶颈消退反证 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 | 2023-2024 | 后续平台周期 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 缺口与监控 4 | SemiAnalysis mapped GB200 rack-scale architecture and component implications, including that many data centers cannot support very high rack density without direct-to-chip liquid cooling. | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 封装瓶颈消退反证 | [SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 封装瓶颈消退反证 | 若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 封装瓶颈消退反证 | [CoWoS/HBM 被识别为 AI capacity constraint](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)。 继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。 第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。 | 2023-2024 | 后续平台周期 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 缺口与监控 4 | 当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。 该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 缺口与监控 4 | 下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 缺口与监控 4 | 已补入公开公司披露、管理层指引和第三方预测。 优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。 这是质量控制卡；它说明结论边界，不是新增正面或负面证据。 | 当前报告 as-of source pack | 下一轮刷新 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 缺口与监控 4 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 23 | 0 | 23 | 2023-07-05 | 2026-01-15 | 有材料，结构不完整 |

### S 曲线汇总

当前节点的产业逻辑已形成，但仍有 6 个问题未达到高置信。特别是市场定价未闭环时，不能把产业胜率直接写成证券买入赔率。

## 3. 标的推荐

以下只保留映射到当前 BOM 的标的。产业逻辑强不等于证券价格便宜。

| 标的 | 公司 | BOM 节点 | 候选状态 | 最终状态 | 核心理由 | 未来空间 / 赔率 | 主要风险 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TSM | TSMC ADR | 先进制程与先进封装 | watch_only | no_action | 先进制程和先进封装是硬供给层，财务质量强。 | 4 | 先进封装供给释放、capex 回报下行、地缘风险。 |

## 4. 来源索引

| ID | 来源 | 类别 | 市场可见时间 | 用途摘要 |
| --- | --- | --- | --- | --- |
| SRC-TSM-Q4-2025 | [TSMC Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) | evidence | 2026-01-15 | TSMC Q4 2025 revenue was $33.73B, gross margin 62.3%, advanced technologies were 77% of wafer revenue, and 2026 capex was expected at $52B-$56B. |
| SRC-SA-COWOS-HBM-2023 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | research_report | 2023-07-05 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. |
| SRC-SA-GB200-BOM-2024 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | research_report | 2024-07-17 | SemiAnalysis mapped GB200 rack-scale architecture and component implications, including that many data centers cannot support very high rack density without direct-to-chip liquid cooling. |
