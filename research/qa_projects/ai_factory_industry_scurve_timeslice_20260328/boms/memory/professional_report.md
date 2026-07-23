---
report_scope: bom-node
project_id: ai_factory_industry_scurve_timeslice_20260328__bom__memory
bom_node_id: memory
run_mode: historical_backtest
as_of_date: 2026-03-28
---

# AI 工厂 · HBM BOM 节点研究

[返回 AI 工厂产业总览](../../professional_report.md)

> 研究截面：2026-03-28。本报告只研究 HBM，不把其他 BOM 的结论提前扩散到本节点。

## 1. 当前研究的问题

判断 HBM 是否处在可投资的 S 曲线阶段，并识别需求、供给、控制权、财务兑现、市场定价和反证的证据边界。

| 节点边界 | 内容 |
| --- | --- |
| 接受什么 | GPU/ASIC 平台规格、先进 DRAM die、TSV/堆叠封装能力、客户认证和价量协议。 |
| 生产什么 | HBM3E、HBM4 及后续高带宽堆叠内存。 |
| 提供给谁 | GPU/ASIC 平台方、先进封装与 AI server 系统。 |
| 代表公司 | SK hynix、Micron、Samsung |
| 验证指标 | HBM shipment/revenue、HBM ASP、HBM mix、gross/operating margin、capex、inventory、FCF |

## 2. 行业概况

### HBM

面向 AI accelerator 的高带宽堆叠 DRAM；本节点不混入 server DDR5 或 enterprise SSD。

**研究账本说明：** 六问是稳定逻辑坐标；材料按市场可见时间追加到 `BOM × 六问 × 时间` 账本。本报告只展示结论、真实变化和可审计材料，不展示搜索词、解析提示或工具过程。

### Q1 · 当前 BOM 的需求是否会被 S 曲线放大拉动？

**结论强度：** 中高：数量、单位含量与 TAM 三条证据同向；缺口是全市场 accelerator shipment 和 HBM attach rate 的连续统一序列。  
**最近材料：** 2026-03-16

#### 基本理解思路

- **专业模型：** HBM 需求传导与含量弹性模型
- **研究目的：** 判断 accelerator 需求是否传到 HBM，并被单颗容量、堆叠层数和高端代际占比进一步放大。
- **判断规则：** HBM 需求 = accelerator 出货量 x HBM attach rate x 单颗 accelerator HBM 容量；HBM 市场价值 = HBM bit 需求 x HBM ASP。
- **理解提示：** AI accelerator 数量 → 单颗 accelerator 的 HBM 容量 → 高端 HBM 代际与堆叠占比 → 总 HBM bit 与市场价值

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

截至 2026-03-28，HBM 需求被 AI accelerator S 曲线放大拉动的证据较强：accelerator 订单和平台收入持续增长；单颗 GPU 的 HBM 容量由 H100 的 80GB 提升到 H200 的 141GB、Blackwell 的 192GB、Rubin 的最高 288GB；TrendForce 预计 HBM consumption 在 2024 年增长超过 200%，2025 年再翻倍；Micron 将 HBM TAM 从 2025 年约 350 亿美元上调到 2028 年约 1000 亿美元。核心不是只卖更多 GPU，而是“accelerator 数量 x 单颗 HBM 含量”同时上升。

**支持机制：** 长上下文、推理并发和更高带宽要求推动每颗 accelerator 的 HBM 容量与带宽代际提升；同时 GPU/ASIC 出货和 AI server 交付扩张，形成数量与单位含量的乘法。

**最大反证：** 若 accelerator 订单下修、单位 HBM GB 停止提升、客户延后 HBM4 平台，或 HBM bit/TAM 预测连续下修，需求弹性判断必须降级。

**对标的的影响：** 需求问通过后，SK hynix、Micron、Samsung 才值得继续进入供给与控制权研究；本问只证明 HBM 池子扩大，不决定三家公司谁更值得买。

**关键来源：** [TrendForce HBM Prices to Increase by 5-10% in 2025](https://www.trendforce.com/presscenter/news/20240506-12125.html)；[TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html)；[TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY)；[Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)；[NVIDIA FY2026 Q4 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/)；[Dell FY2026 Q4 results](https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-3)；[NVIDIA platform HBM specification progression](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 截至 2026-03-28，HBM 需求被 AI accelerator S 曲线放大拉动的证据较强：accelerator 订单和平台收入持续增长；单颗 GPU 的 HBM 容量由 H100 的 80GB 提升到 H200 的 141GB、Blackwell 的 192GB、Rubin 的最高 288GB；TrendForce 预计 HBM consumption 在 2024 年增长超过 200%，2025 年再翻倍；Micron 将 HBM TAM 从 2025 年约 350 亿美元上调到 2028 年约 1000 亿美元。核心不是只卖更多 GPU，而是“accelerator 数量 x 单颗 HBM 含量”同时上升。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2024-05-06 | [TrendForce HBM Prices to Increase by 5-10% in 2025](https://www.trendforce.com/presscenter/news/20240506-12125.html) | 事实 / 支持 | [TrendForce 预计 2024 年 HBM consumption 增长超过 200%、2025 年再翻倍](https://www.trendforce.com/presscenter/news/20240808-12248.html)。 [Micron 给出 2025 年约 350 亿美元 HBM TAM](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)，而 [HBM ASP 约为 DDR5 的五倍，2025 年 value share 可能超过 DRAM 的 30%](https://www.trendforce.com/presscenter/news/20240506-12125.html)。 |
| 2024-05-06 | [TrendForce HBM Prices to Increase by 5-10% in 2025](https://www.trendforce.com/presscenter/news/20240506-12125.html) | 预测 / 支持 | [Micron 将 2028 年 HBM TAM 上调到约 1000 亿美元，约 40% CAGR](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 |
| 2024-05-06 | [TrendForce HBM Prices to Increase by 5-10% in 2025](https://www.trendforce.com/presscenter/news/20240506-12125.html) | 事实 / 支持 | TrendForce estimated HBM ASP at several times conventional DRAM and about five times DDR5, while value share could exceed 30% of DRAM in 2025. |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 事实 / 支持 | [NVIDIA 平台从 H100 80GB、H200 141GB、Blackwell 192GB 升至 Blackwell Ultra 288GB；Rubin 最高 288GB HBM4，带宽最高 22TB/s](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/)。 单位容量在 Hopper 到 Blackwell Ultra 显著提升；Rubin 容量不再提升，但 HBM4 接口与带宽跃升说明单位价值量仍可能继续上行。 |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 预测 / 支持 | 下一步不是机械假设 GB 永远增长，而是跟踪 HBM4/HBM4E 的 stack 数、层数、带宽和 ASP。 |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 事实 / 支持 | [TrendForce 预计 NVIDIA HBM3E consumption 2024 年超过 60%、2025 年超过 85%，12-high 在 2025 年约占 HBM3E 40%](https://www.trendforce.com/presscenter/news/20240808-12248.html)。 需求从 HBM3/HBM3E 8-high 向 HBM3E 12-high 和 HBM4 升级，增加 die、堆叠和资格复杂度。 |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 预测 / 支持 | 2026 份额取决于 HBM4 认证，而不只是三家公司名义产能。 |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 预测 / 支持 | [HBM3E/12-high 占比快速上升](https://www.trendforce.com/presscenter/news/20240808-12248.html)。 [三家供应商进入 HBM4 mass production，但 yield 和 certification 约束近端供给](https://www.trendforce.com/research/download/RP251029MY)。 代际 mix 不是总需求；需要和 accelerator 数量共同使用。 |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 事实 / 支持 | [TrendForce 预计 2024 年 HBM consumption 增长超过 200%、2025 年再翻倍](https://www.trendforce.com/presscenter/news/20240808-12248.html)。 [Micron 给出 2025 年约 350 亿美元 HBM TAM](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)，而 [HBM ASP 约为 DDR5 的五倍，2025 年 value share 可能超过 DRAM 的 30%](https://www.trendforce.com/presscenter/news/20240506-12125.html)。 |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 预测 / 支持 | [Micron 将 2028 年 HBM TAM 上调到约 1000 亿美元，约 40% CAGR](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 事实 / 支持 | TrendForce described NVIDIA as the largest HBM buyer, expected procurement share above 70%, with HBM consumption growing more than 200% in 2024 and expected to double again in 2025 as Blackwell raises HBM content. |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 事实 / 支持 | [TrendForce 预计 NVIDIA HBM3E consumption 2024 年超过 60%、2025 年超过 85%，12-high 在 2025 年约占 HBM3E 40%](https://www.trendforce.com/presscenter/news/20240808-12248.html)。 需求从 HBM3/HBM3E 8-high 向 HBM3E 12-high 和 HBM4 升级，增加 die、堆叠和资格复杂度。 |

时间线先展示最早 12 条；完整 31 条见“映射材料”。

#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-03-16 | [NVIDIA platform HBM specification progression](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 单颗 accelerator 的 HBM 容量 | [NVIDIA 平台从 H100 80GB、H200 141GB、Blackwell 192GB 升至 Blackwell Ultra 288GB；Rubin 最高 288GB HBM4，带宽最高 22TB/s](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/)。 单位容量在 Hopper 到 Blackwell Ultra 显著提升；Rubin 容量不再提升，但 HBM4 接口与带宽跃升说明单位价值量仍可能继续上行。 | 未结构化 | 未结构化 |
| 2026-03-16 | [NVIDIA platform HBM specification progression](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 单颗 accelerator 的 HBM 容量 | 下一步不是机械假设 GB 永远增长，而是跟踪 HBM4/HBM4E 的 stack 数、层数、带宽和 ASP。 | 未结构化 | 未结构化 |
| 2026-03-16 | [NVIDIA platform HBM specification progression](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 单颗 accelerator 的 HBM 容量 | [最高 192GB/288GB HBM3E](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/)。 [最高 288GB HBM4、最高 22TB/s，带宽接近 Blackwell 的 3 倍](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/)。 容量持平但带宽/代际升级，未来价值量不能只看 GB。 | Blackwell / Blackwell Ultra | Rubin platform |
| 2026-03-16 | [NVIDIA platform HBM specification progression](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 单颗 accelerator 的 HBM 容量 | NVIDIA platform specifications show H100 at 80GB HBM, H200 at 141GB, Blackwell at 192GB, Blackwell Ultra at 288GB and Rubin at up to 288GB HBM4 with up to 22TB/s bandwidth. | 未结构化 | 未结构化 |
| 2026-02-26 | [Dell FY2026 Q4 results](https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-3) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | AI accelerator 数量 | [NVIDIA Data Center revenue 从 2023 年初的 36.2 亿美元升至 2026 年初的 623 亿美元](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/)；[Dell FY26 AI server orders 超过 640 亿美元、shipped 超过 250 亿美元、FY27 backlog 430 亿美元](https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-3)。 数量底座显著扩大，但收入同时含 ASP/mix，不能把收入倍数直接当出货倍数。 | 未结构化 | 未结构化 |
| 2026-02-26 | [Dell FY2026 Q4 results](https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-3) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | AI accelerator 数量 | NVIDIA Q1 FY27 revenue outlook 与 Dell FY27 AI server revenue guide 说明近端交付仍在扩张。 | 未结构化 | 未结构化 |
| 2026-02-26 | [Dell FY2026 Q4 results](https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-3) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | AI accelerator 数量 | [AI server shipments 超过 250 亿美元，期末 backlog 430 亿美元](https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-3)。 [AI-optimized server revenue 指引约 500 亿美元，同比约 +103%](https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-3)。 系统收入包含非 HBM 部件，只用于确认 accelerator 交付数量底座。 | FY2026 | FY2027E |
| 2026-02-26 | [Dell FY2026 Q4 results](https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-3) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | AI accelerator 数量 | Dell FY26 closed more than $64B in AI-optimized server orders, shipped more than $25B, entered FY27 with a $43B backlog, and guided FY27 AI-optimized server revenue to roughly $50B, up 103% year over year. | 未结构化 | 未结构化 |
| 2026-02-25 | [NVIDIA FY2026 Q4 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | AI accelerator 数量 | [NVIDIA Data Center revenue 从 2023 年初的 36.2 亿美元升至 2026 年初的 623 亿美元](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/)；[Dell FY26 AI server orders 超过 640 亿美元、shipped 超过 250 亿美元、FY27 backlog 430 亿美元](https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-3)。 数量底座显著扩大，但收入同时含 ASP/mix，不能把收入倍数直接当出货倍数。 | 未结构化 | 未结构化 |
| 2026-02-25 | [NVIDIA FY2026 Q4 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | AI accelerator 数量 | NVIDIA Q1 FY27 revenue outlook 与 Dell FY27 AI server revenue guide 说明近端交付仍在扩张。 | 未结构化 | 未结构化 |
| 2026-02-25 | [NVIDIA FY2026 Q4 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | AI accelerator 数量 | [Data Center revenue 623 亿美元](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/)。 [公司总收入指引 780 亿美元 +/-2%](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/)。 收入指引不是 accelerator 出货量，但能验证近端平台需求没有在截面前转弱。 | Q4 FY2026 | Q1 FY2027E |
| 2026-02-25 | [NVIDIA FY2026 Q4 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | AI accelerator 数量 | NVIDIA Q4 FY26 revenue was $68.1B and Data Center revenue was $62.3B, up 75% YoY. FY2026 revenue was $215.9B, GAAP gross margin was 71.1%, operating income was $130.4B and free cash flow was $96.6B. Q1 FY27 revenue outlook was $78.0B +/-2% with no China Data Center compute revenue assumed. | 未结构化 | 未结构化 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 总 HBM bit 与市场价值 | [TrendForce 预计 2024 年 HBM consumption 增长超过 200%、2025 年再翻倍](https://www.trendforce.com/presscenter/news/20240808-12248.html)。 [Micron 给出 2025 年约 350 亿美元 HBM TAM](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)，而 [HBM ASP 约为 DDR5 的五倍，2025 年 value share 可能超过 DRAM 的 30%](https://www.trendforce.com/presscenter/news/20240506-12125.html)。 | 未结构化 | 未结构化 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 总 HBM bit 与市场价值 | [Micron 将 2028 年 HBM TAM 上调到约 1000 亿美元，约 40% CAGR](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 | 未结构化 | 未结构化 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 总 HBM bit 与市场价值 | [HBM TAM约350亿美元](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 [HBM TAM约1000亿美元，约40% CAGR](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 公司 TAM 是市场预期锚，不是 Micron 收入指引；需要用供应商出货与 ASP 逐年验证。 | CY2025E | CY2028E |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 总 HBM bit 与市场价值 | Micron prepared remarks forecast HBM TAM from about $35B in calendar 2025 to around $100B in calendar 2028, about 40% CAGR, and said 2026 HBM supply had completed price and volume agreements. | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 高端 HBM 代际与堆叠占比 | [TrendForce 预计 NVIDIA HBM3E consumption 2024 年超过 60%、2025 年超过 85%，12-high 在 2025 年约占 HBM3E 40%](https://www.trendforce.com/presscenter/news/20240808-12248.html)。 需求从 HBM3/HBM3E 8-high 向 HBM3E 12-high 和 HBM4 升级，增加 die、堆叠和资格复杂度。 | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 高端 HBM 代际与堆叠占比 | 2026 份额取决于 HBM4 认证，而不只是三家公司名义产能。 | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 高端 HBM 代际与堆叠占比 | [HBM3E/12-high 占比快速上升](https://www.trendforce.com/presscenter/news/20240808-12248.html)。 [三家供应商进入 HBM4 mass production，但 yield 和 certification 约束近端供给](https://www.trendforce.com/research/download/RP251029MY)。 代际 mix 不是总需求；需要和 accelerator 数量共同使用。 | 2024-2025E | 2026E |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 高端 HBM 代际与堆叠占比 | TrendForce said SK hynix led with about 150K TSV capacity; yield, certification and backend capacity constrained near-term supply; all three suppliers planned HBM4 mass production in 2026. | 未结构化 | 未结构化 |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 单颗 accelerator 的 HBM 容量 | [NVIDIA 平台从 H100 80GB、H200 141GB、Blackwell 192GB 升至 Blackwell Ultra 288GB；Rubin 最高 288GB HBM4，带宽最高 22TB/s](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/)。 单位容量在 Hopper 到 Blackwell Ultra 显著提升；Rubin 容量不再提升，但 HBM4 接口与带宽跃升说明单位价值量仍可能继续上行。 | 未结构化 | 未结构化 |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 单颗 accelerator 的 HBM 容量 | 下一步不是机械假设 GB 永远增长，而是跟踪 HBM4/HBM4E 的 stack 数、层数、带宽和 ASP。 | 未结构化 | 未结构化 |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 高端 HBM 代际与堆叠占比 | [TrendForce 预计 NVIDIA HBM3E consumption 2024 年超过 60%、2025 年超过 85%，12-high 在 2025 年约占 HBM3E 40%](https://www.trendforce.com/presscenter/news/20240808-12248.html)。 需求从 HBM3/HBM3E 8-high 向 HBM3E 12-high 和 HBM4 升级，增加 die、堆叠和资格复杂度。 | 未结构化 | 未结构化 |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 高端 HBM 代际与堆叠占比 | 2026 份额取决于 HBM4 认证，而不只是三家公司名义产能。 | 未结构化 | 未结构化 |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 高端 HBM 代际与堆叠占比 | [HBM3E/12-high 占比快速上升](https://www.trendforce.com/presscenter/news/20240808-12248.html)。 [三家供应商进入 HBM4 mass production，但 yield 和 certification 约束近端供给](https://www.trendforce.com/research/download/RP251029MY)。 代际 mix 不是总需求；需要和 accelerator 数量共同使用。 | 2024-2025E | 2026E |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 总 HBM bit 与市场价值 | [TrendForce 预计 2024 年 HBM consumption 增长超过 200%、2025 年再翻倍](https://www.trendforce.com/presscenter/news/20240808-12248.html)。 [Micron 给出 2025 年约 350 亿美元 HBM TAM](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)，而 [HBM ASP 约为 DDR5 的五倍，2025 年 value share 可能超过 DRAM 的 30%](https://www.trendforce.com/presscenter/news/20240506-12125.html)。 | 未结构化 | 未结构化 |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 总 HBM bit 与市场价值 | [Micron 将 2028 年 HBM TAM 上调到约 1000 亿美元，约 40% CAGR](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 | 未结构化 | 未结构化 |
| 2024-08-08 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 总 HBM bit 与市场价值 | TrendForce described NVIDIA as the largest HBM buyer, expected procurement share above 70%, with HBM consumption growing more than 200% in 2024 and expected to double again in 2025 as Blackwell raises HBM content. | 未结构化 | 未结构化 |
| 2024-05-06 | [TrendForce HBM Prices to Increase by 5-10% in 2025](https://www.trendforce.com/presscenter/news/20240506-12125.html) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 总 HBM bit 与市场价值 | [TrendForce 预计 2024 年 HBM consumption 增长超过 200%、2025 年再翻倍](https://www.trendforce.com/presscenter/news/20240808-12248.html)。 [Micron 给出 2025 年约 350 亿美元 HBM TAM](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)，而 [HBM ASP 约为 DDR5 的五倍，2025 年 value share 可能超过 DRAM 的 30%](https://www.trendforce.com/presscenter/news/20240506-12125.html)。 | 未结构化 | 未结构化 |
| 2024-05-06 | [TrendForce HBM Prices to Increase by 5-10% in 2025](https://www.trendforce.com/presscenter/news/20240506-12125.html) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 总 HBM bit 与市场价值 | [Micron 将 2028 年 HBM TAM 上调到约 1000 亿美元，约 40% CAGR](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 | 未结构化 | 未结构化 |
| 2024-05-06 | [TrendForce HBM Prices to Increase by 5-10% in 2025](https://www.trendforce.com/presscenter/news/20240506-12125.html) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 总 HBM bit 与市场价值 | TrendForce estimated HBM ASP at several times conventional DRAM and about five times DDR5, while value share could exceed 30% of DRAM in 2025. | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 16 | 15 | 0 | 0 | 0 | 0 | 31 | 0 | 2024-05-06 | 2026-03-16 | 单向覆盖，缺反证 |

### Q2 · 供给能否跟上？

**结论强度：** 中高：售罄/价量协议和认证延迟支持偏紧；供给扩张速度与精确 S-D ratio 仍缺公开连续数据。  
**最近材料：** 2026-03-20

#### 基本理解思路

- **专业模型：** HBM 有效供给漏斗模型
- **研究目的：** 把名义 DRAM 产能逐层折算成完成堆叠、封装、测试和客户认证的合格 HBM 供给。
- **判断规则：** HBM 有效供给 = DRAM wafer 投入 x die yield x stacking yield x packaging/test throughput x qualification pass rate。
- **理解提示：** 先进 DRAM wafer 分配 → DRAM die 良率 → TSV、堆叠与封装吞吐 → 客户认证 → 合格交付与合同覆盖

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

截至截面日，HBM 的名义扩产仍不能直接消除短缺：先进 DRAM wafer、较高 wafer trade ratio、die yield、TSV/堆叠后端和客户认证共同压缩有效供给。Micron 的 2026 全年 HBM 已完成价量协议，TrendForce 仍把 yield、certification 和 back-end capacity 视为近端约束；但 Samsung 已开始 HBM4 商业出货并预计 2026 HBM 销售超过三倍，说明供给释放正在加速。结论应是“2026 仍偏紧，但必须动态监控新增合格供给”，而不是永久短缺。

**支持机制：** HBM 比普通 DRAM 消耗更多 wafer、后端工序更复杂且必须逐客户认证，因此有效供给释放慢于名义 capex。

**最大反证：** Samsung HBM4 量产、三家后端扩产和良率改善会增加合格供给；若 ASP、交期和售罄状态转弱，瓶颈判断应迅速降级。

**对标的的影响：** 供给仍紧支持 HBM chokepoint，但 Samsung 扩产和 HBM4 多供意味着稀缺溢价不是永久的；标的强度必须与各家 qualified capacity 而非总 DRAM 产能绑定。

**关键来源：** [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)；[TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY)；[Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)；[Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)；[TrendForce HBM Market Bulletin March 2026](https://www.trendforce.com/research/download/RP260320WK3)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 截至截面日，HBM 的名义扩产仍不能直接消除短缺：先进 DRAM wafer、较高 wafer trade ratio、die yield、TSV/堆叠后端和客户认证共同压缩有效供给。Micron 的 2026 全年 HBM 已完成价量协议，TrendForce 仍把 yield、certification 和 back-end capacity 视为近端约束；但 Samsung 已开始 HBM4 商业出货并预计 2026 HBM 销售超过三倍，说明供给释放正在加速。结论应是“2026 仍偏紧，但必须动态监控新增合格供给”，而不是永久短缺。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 事实 / 支持 | [SemiAnalysis 早期把 CoWoS 与 HBM 识别为 AI accelerator capacity constraints](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)。 [TrendForce 4Q25 仍把 back-end capacity buildout、yield 和 certification 列为 HBM 供给关键](https://www.trendforce.com/research/download/RP251029MY)。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 预测 / 支持 | 12-high/HBM4 增加后端复杂度，供给释放取决于新线爬坡而非只看 DRAM wafer。 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 事实 / 支持 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 事实 / 支持 | [TrendForce 4Q25 HBM 分析给出 SK hynix 约 150K TSV capacity，并指出三家扩产](https://www.trendforce.com/research/download/RP251029MY)。 [Micron 表示 2026 全部 HBM supply 已完成 price and volume agreements](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)，说明可售先进产能在截面上仍紧。 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 预测 / 支持 | 三家都扩充前后端，名义产能会增长；需跟踪何时转为合格出货。 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 预测 / 支持 | [SK hynix TSV capacity约150K；Micron 2026 supply价量协议完成](https://www.trendforce.com/research/download/RP251029MY)。 三家扩产，但可交付供给仍受后端与认证限制。 产能与合同不是同口径，只用于供给漏斗的不同环节。 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 事实 / 支持 | [TrendForce 把 yield 列为 HBM 近端供给约束](https://www.trendforce.com/research/download/RP251029MY)。 [Samsung 宣称 HBM4 量产初期取得稳定良率并开始商业出货](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)，这是供给释放证据，但不是三家可比 yield 表。 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 预测 / 支持 | 若三家 HBM4 yield 同步稳定，短缺会由 die yield 转向后端和认证。 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 事实 / 支持 | [SemiAnalysis 早期把 CoWoS 与 HBM 识别为 AI accelerator capacity constraints](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)。 [TrendForce 4Q25 仍把 back-end capacity buildout、yield 和 certification 列为 HBM 供给关键](https://www.trendforce.com/research/download/RP251029MY)。 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 预测 / 支持 | 12-high/HBM4 增加后端复杂度，供给释放取决于新线爬坡而非只看 DRAM wafer。 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 预测 / 支持 | [后端扩产、yield、认证共同约束供给](https://www.trendforce.com/research/download/RP251029MY)。 三家扩充 back-end，但量产和认证节奏仍决定实际 shipment。 公开摘要未给月度吞吐数，因此只做方向判断。 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 事实 / 支持 | TrendForce said SK hynix led with about 150K TSV capacity; yield, certification and backend capacity constrained near-term supply; all three suppliers planned HBM4 mass production in 2026. |

时间线先展示最早 12 条；完整 32 条见“映射材料”。

#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-03-20 | [TrendForce HBM Market Bulletin March 2026](https://www.trendforce.com/research/download/RP260320WK3) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 客户认证 | HBM3E/HBM4 都需经过 GPU/ASIC 客户验证，样品和量产资格不能互换。 [Samsung 已宣布 HBM4 商业出货](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)，但 [TrendForce 3 月 20 日仍称更高规格使主要供应商验证延迟，早期 HBM4 shipment 有下修风险](https://www.trendforce.com/research/download/RP260320WK3)。 | 未结构化 | 未结构化 |
| 2026-03-20 | [TrendForce HBM Market Bulletin March 2026](https://www.trendforce.com/research/download/RP260320WK3) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 客户认证 | 资格进度会把需求在 HBM4 与 HBM3E 之间重新分配，并影响客户平台发布时间。 | 未结构化 | 未结构化 |
| 2026-03-20 | [TrendForce HBM Market Bulletin March 2026](https://www.trendforce.com/research/download/RP260320WK3) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 客户认证 | [HBM4 qualification 延迟，早期 shipment 有下修风险](https://www.trendforce.com/research/download/RP260320WK3)。 未满足的 HBM4 需求可能回流 HBM3E，客户也可能推迟下一代平台。 这是明确反向证据：它同时削弱 HBM4 供给和短期平台需求时点。 | 2026-03 | 2026E |
| 2026-03-20 | [TrendForce HBM Market Bulletin March 2026](https://www.trendforce.com/research/download/RP260320WK3) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 客户认证 | TrendForce said stricter HBM4 specifications delayed supplier validation, creating downside risk to early HBM4 shipments and next-generation AI platform timing; unmet HBM4 demand could shift back to HBM3E. | 未结构化 | 未结构化 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | DRAM die 良率 | [TrendForce 把 yield 列为 HBM 近端供给约束](https://www.trendforce.com/research/download/RP251029MY)。 [Samsung 宣称 HBM4 量产初期取得稳定良率并开始商业出货](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)，这是供给释放证据，但不是三家可比 yield 表。 | 未结构化 | 未结构化 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | DRAM die 良率 | 若三家 HBM4 yield 同步稳定，短缺会由 die yield 转向后端和认证。 | 未结构化 | 未结构化 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | DRAM die 良率 | [HBM4 已商业出货，称初期良率稳定](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 [预计 HBM 销售较 2025 年超过三倍并扩充 HBM4 产能](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 销售增长同时受份额、出货和 ASP 影响，不能单独推导 yield。 | 2026-02 | CY2026E |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 客户认证 | HBM3E/HBM4 都需经过 GPU/ASIC 客户验证，样品和量产资格不能互换。 [Samsung 已宣布 HBM4 商业出货](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)，但 [TrendForce 3 月 20 日仍称更高规格使主要供应商验证延迟，早期 HBM4 shipment 有下修风险](https://www.trendforce.com/research/download/RP260320WK3)。 | 未结构化 | 未结构化 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 客户认证 | 资格进度会把需求在 HBM4 与 HBM3E 之间重新分配，并影响客户平台发布时间。 | 未结构化 | 未结构化 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 合格交付与合同覆盖 | [Micron 2026 全年 HBM supply 已完成价量协议](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 合同覆盖支持供需偏紧，但 [Samsung 预计 2026 HBM 销售超过三倍并扩产](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)，说明供给曲线正在上移。 | 未结构化 | 未结构化 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 合格交付与合同覆盖 | 需要把三家 shipment、ASP、lead time 与资格按季度放在一起，才能判断何时由短缺转为平衡。 | 未结构化 | 未结构化 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 合格交付与合同覆盖 | [Micron 2026 supply价量协议完成](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 [Samsung HBM sales预计超过三倍并扩充HBM4产能](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 一边是已锁定需求，一边是新增供给；二者共同说明紧张仍在但不是永久不变。 | 2026 supply status | CY2026E |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 合格交付与合同覆盖 | Samsung announced commercial HBM4 shipments, described stable initial mass-production yields, expected 2026 HBM sales to more than triple versus 2025 and said it was expanding HBM4 capacity. | 未结构化 | 未结构化 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 先进 DRAM wafer 分配 | [TrendForce 4Q25 HBM 分析给出 SK hynix 约 150K TSV capacity，并指出三家扩产](https://www.trendforce.com/research/download/RP251029MY)。 [Micron 表示 2026 全部 HBM supply 已完成 price and volume agreements](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)，说明可售先进产能在截面上仍紧。 | 未结构化 | 未结构化 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 先进 DRAM wafer 分配 | 三家都扩充前后端，名义产能会增长；需跟踪何时转为合格出货。 | 未结构化 | 未结构化 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 先进 DRAM wafer 分配 | [SK hynix TSV capacity约150K；Micron 2026 supply价量协议完成](https://www.trendforce.com/research/download/RP251029MY)。 三家扩产，但可交付供给仍受后端与认证限制。 产能与合同不是同口径，只用于供给漏斗的不同环节。 | 4Q25 / CY2026 supply | 2026E |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 合格交付与合同覆盖 | [Micron 2026 全年 HBM supply 已完成价量协议](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 合同覆盖支持供需偏紧，但 [Samsung 预计 2026 HBM 销售超过三倍并扩产](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)，说明供给曲线正在上移。 | 未结构化 | 未结构化 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 合格交付与合同覆盖 | 需要把三家 shipment、ASP、lead time 与资格按季度放在一起，才能判断何时由短缺转为平衡。 | 未结构化 | 未结构化 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 合格交付与合同覆盖 | [Micron 2026 supply价量协议完成](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 [Samsung HBM sales预计超过三倍并扩充HBM4产能](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 一边是已锁定需求，一边是新增供给；二者共同说明紧张仍在但不是永久不变。 | 2026 supply status | CY2026E |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 合格交付与合同覆盖 | Micron prepared remarks forecast HBM TAM from about $35B in calendar 2025 to around $100B in calendar 2028, about 40% CAGR, and said 2026 HBM supply had completed price and volume agreements. | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 先进 DRAM wafer 分配 | [TrendForce 4Q25 HBM 分析给出 SK hynix 约 150K TSV capacity，并指出三家扩产](https://www.trendforce.com/research/download/RP251029MY)。 [Micron 表示 2026 全部 HBM supply 已完成 price and volume agreements](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)，说明可售先进产能在截面上仍紧。 | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 先进 DRAM wafer 分配 | 三家都扩充前后端，名义产能会增长；需跟踪何时转为合格出货。 | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 先进 DRAM wafer 分配 | [SK hynix TSV capacity约150K；Micron 2026 supply价量协议完成](https://www.trendforce.com/research/download/RP251029MY)。 三家扩产，但可交付供给仍受后端与认证限制。 产能与合同不是同口径，只用于供给漏斗的不同环节。 | 4Q25 / CY2026 supply | 2026E |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | DRAM die 良率 | [TrendForce 把 yield 列为 HBM 近端供给约束](https://www.trendforce.com/research/download/RP251029MY)。 [Samsung 宣称 HBM4 量产初期取得稳定良率并开始商业出货](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)，这是供给释放证据，但不是三家可比 yield 表。 | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | DRAM die 良率 | 若三家 HBM4 yield 同步稳定，短缺会由 die yield 转向后端和认证。 | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | TSV、堆叠与封装吞吐 | [SemiAnalysis 早期把 CoWoS 与 HBM 识别为 AI accelerator capacity constraints](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)。 [TrendForce 4Q25 仍把 back-end capacity buildout、yield 和 certification 列为 HBM 供给关键](https://www.trendforce.com/research/download/RP251029MY)。 | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | TSV、堆叠与封装吞吐 | 12-high/HBM4 增加后端复杂度，供给释放取决于新线爬坡而非只看 DRAM wafer。 | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | TSV、堆叠与封装吞吐 | [后端扩产、yield、认证共同约束供给](https://www.trendforce.com/research/download/RP251029MY)。 三家扩充 back-end，但量产和认证节奏仍决定实际 shipment。 公开摘要未给月度吞吐数，因此只做方向判断。 | 4Q25 | 2026E |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | TSV、堆叠与封装吞吐 | TrendForce said SK hynix led with about 150K TSV capacity; yield, certification and backend capacity constrained near-term supply; all three suppliers planned HBM4 mass production in 2026. | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | TSV、堆叠与封装吞吐 | [SemiAnalysis 早期把 CoWoS 与 HBM 识别为 AI accelerator capacity constraints](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share)。 [TrendForce 4Q25 仍把 back-end capacity buildout、yield 和 certification 列为 HBM 供给关键](https://www.trendforce.com/research/download/RP251029MY)。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | TSV、堆叠与封装吞吐 | 12-high/HBM4 增加后端复杂度，供给释放取决于新线爬坡而非只看 DRAM wafer。 | 未结构化 | 未结构化 |
| 2023-07-05 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | TSV、堆叠与封装吞吐 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15 | 17 | 0 | 0 | 0 | 0 | 32 | 0 | 2023-07-05 | 2026-03-20 | 单向覆盖，缺反证 |

### Q3 · 谁控制供给？

**结论强度：** 中高：三家格局和龙头方向清楚；精确份额口径来自第三方且会随认证快速变化。  
**最近材料：** 2026-03-09

#### 基本理解思路

- **专业模型：** 合格份额与代际控制权模型
- **研究目的：** 识别谁控制的不是普通 DRAM wafer，而是特定代际、特定客户已经认证并能按期交付的 HBM 供给。
- **判断规则：** 有效控制权 = 合格出货份额 + 代际领先 + 客户认证/合同锁定 + yield/time-to-volume - second-source 速度。
- **理解提示：** 合格出货份额 → 代际与客户资格领先 → 良率与量产速度 → 客户与合同锁定 → 替代与 second source

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

HBM 供给控制权集中于 SK hynix、Samsung、Micron，但需要按“合格出货份额”而非普通 DRAM 份额判断。公开资料显示 SK hynix 的 2025 HBM bit output 约 59%，2026E 约 50%；Samsung 约从 20% 升至 28%，Micron 为剩余份额。SK hynix 仍控制最大合格供给和既有客户关系，但 Samsung HBM4 商业出货及认证进展意味着控制权正从单一龙头向三供格局边际扩散；Micron 已锁定 2026 价量，但 HBM4 验证节奏仍需持续跟踪。

**支持机制：** HBM 需要先进工艺、堆叠、客户认证和长期合作，合格供给集中在三家公司，龙头可将技术与交付优势转成 allocation 和份额。

**最大反证：** Samsung HBM4 量产、客户三供策略和 Micron 扩张会降低单一供应商锁定；控制权可能在行业增长中重新分配。

**对标的的影响：** 本问不支持把 HBM 行业增长平均分配给三家公司。SK hynix 胜率最高但份额有下行风险；Samsung 是份额修复路线；Micron 是高弹性但资格需验证的路线。

**关键来源：** [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)；[SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)；[Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)；[TrendForce HBM Market Bulletin February 2026](https://www.trendforce.com/research/download/RP260212TV3)；[TrendForce HBM supplier share outlook](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | HBM 供给控制权集中于 SK hynix、Samsung、Micron，但需要按“合格出货份额”而非普通 DRAM 份额判断。公开资料显示 SK hynix 的 2025 HBM bit output 约 59%，2026E 约 50%；Samsung 约从 20% 升至 28%，Micron 为剩余份额。SK hynix 仍控制最大合格供给和既有客户关系，但 Samsung HBM4 商业出货及认证进展意味着控制权正从单一龙头向三供格局边际扩散；Micron 已锁定 2026 价量，但 HBM4 验证节奏仍需持续跟踪。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 事实 / 支持 | HBM 合同锁定通常早于交付，反映客户为供给确定性付费。 [Micron 2026 全年 HBM supply 已完成 price and volume agreements](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 预测 / 支持 | 协议提高可见度，但不证明 Micron 最终份额或 margin 一定高于同行。 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 预测 / 支持 | [价量协议全部完成](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 已锁定供给将随客户平台资格转为 shipment/revenue。 合同覆盖强，但需实际出货与毛利验证。 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 事实 / 支持 | Micron prepared remarks forecast HBM TAM from about $35B in calendar 2025 to around $100B in calendar 2028, about 40% CAGR, and said 2026 HBM supply had completed price and volume agreements. |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 事实 / 支持 | [SK hynix FY25 业绩将纪录表现归因于 AI memory/HBM leadership](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。 [Samsung HBM4 已进入 mass production/commercial shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)，说明 second source 不再只是样品。 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 预测 / 支持 | 需要季度 shipment 和客户平台覆盖验证量产份额。 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 事实 / 支持 | SK hynix FY2025 revenue was KRW97.1467T, operating profit KRW47.2063T and operating margin 49%, driven by AI memory and HBM leadership. |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 事实 / 支持 | HBM3E 时期 SK hynix 量产和客户关系领先。 [TrendForce 2 月认为 Samsung HBM4 验证领先、SK hynix 保持 volume leadership、Micron 略慢](https://www.trendforce.com/research/download/RP260212TV3)；[Samsung 同日宣布商业出货 HBM4](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 预测 / 支持 | 代际控制权可能与存量 HBM3E 份额不同。 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 事实 / 支持 | [SK hynix FY25 业绩将纪录表现归因于 AI memory/HBM leadership](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。 [Samsung HBM4 已进入 mass production/commercial shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)，说明 second source 不再只是样品。 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 预测 / 支持 | 需要季度 shipment 和客户平台覆盖验证量产份额。 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 预测 / 支持 | [HBM4商业出货](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 [HBM sales预计超过三倍](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 销售增速需拆为份额、量和价。 |

时间线先展示最早 12 条；完整 26 条见“映射材料”。

#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-03-09 | [TrendForce HBM supplier share outlook](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/) | 市场消息 / 历史 / 手动导入 | 事实 / 支持 | 合格出货份额 | [TrendForce 相关公开材料预计 SK hynix 2025 HBM bit output share 约59%、Samsung约20%；2026E SK hynix约50%、Samsung约28%](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/)。 份额高度集中，但龙头并非份额永远上升。Micron 份额为公开数据余量推算，不能当独立披露。 | 未结构化 | 未结构化 |
| 2026-03-09 | [TrendForce HBM supplier share outlook](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/) | 市场消息 / 历史 / 手动导入 | 预测 / 支持 | 合格出货份额 | HBM4 资格会重新分配 2026 份额。 | 未结构化 | 未结构化 |
| 2026-03-09 | [TrendForce HBM supplier share outlook](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/) | 市场消息 / 历史 / 手动导入 | 预测 / 支持 | 合格出货份额 | [SK hynix约59%、Samsung约20% HBM bit output](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/)。 [SK hynix约50%、Samsung约28%](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/)。 同为 bit output forecast，可比较方向；仍非最终实际份额。 | 2025E | 2026E |
| 2026-03-09 | [TrendForce HBM supplier share outlook](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/) | 市场消息 / 历史 / 手动导入 | 事实 / 支持 | 替代与 second source | 客户采用多供是降低单一 HBM 风险的自然结果。 [TrendForce 认为 NVIDIA 可能采用三家供应商；份额预测显示 Samsung 上升、SK hynix 回落](https://www.trendforce.com/research/download/RP260212TV3)。 | 未结构化 | 未结构化 |
| 2026-03-09 | [TrendForce HBM supplier share outlook](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/) | 市场消息 / 历史 / 手动导入 | 预测 / 支持 | 替代与 second source | 若 Samsung/Micron 按期通过关键平台并提升份额，SK hynix 仍是龙头但超额控制权会减弱。 | 未结构化 | 未结构化 |
| 2026-03-09 | [TrendForce HBM supplier share outlook](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/) | 市场消息 / 历史 / 手动导入 | 预测 / 支持 | 替代与 second source | HBM供给高度集中。 [三供策略和Samsung份额修复](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/)。 这是龙头控制权的核心反证。 | 2025E | 2026E |
| 2026-03-09 | [TrendForce HBM supplier share outlook](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/) | 市场消息 / 历史 / 手动导入 | 事实 / 支持 | 替代与 second source | TrendForce-related public reporting projected SK hynix global HBM bit output share at 59% in 2025 and 50% in 2026, while Samsung could rise from 20% to 28%; these are forecasts rather than audited actual shares. | 未结构化 | 未结构化 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 代际与客户资格领先 | HBM3E 时期 SK hynix 量产和客户关系领先。 [TrendForce 2 月认为 Samsung HBM4 验证领先、SK hynix 保持 volume leadership、Micron 略慢](https://www.trendforce.com/research/download/RP260212TV3)；[Samsung 同日宣布商业出货 HBM4](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 | 未结构化 | 未结构化 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 代际与客户资格领先 | 代际控制权可能与存量 HBM3E 份额不同。 | 未结构化 | 未结构化 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 良率与量产速度 | [SK hynix FY25 业绩将纪录表现归因于 AI memory/HBM leadership](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。 [Samsung HBM4 已进入 mass production/commercial shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)，说明 second source 不再只是样品。 | 未结构化 | 未结构化 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 良率与量产速度 | 需要季度 shipment 和客户平台覆盖验证量产份额。 | 未结构化 | 未结构化 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 良率与量产速度 | [HBM4商业出货](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 [HBM sales预计超过三倍](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 销售增速需拆为份额、量和价。 | 2026-02 | CY2026E |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 良率与量产速度 | Samsung announced commercial HBM4 shipments, described stable initial mass-production yields, expected 2026 HBM sales to more than triple versus 2025 and said it was expanding HBM4 capacity. | 未结构化 | 未结构化 |
| 2026-02-12 | [TrendForce HBM Market Bulletin February 2026](https://www.trendforce.com/research/download/RP260212TV3) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 代际与客户资格领先 | HBM3E 时期 SK hynix 量产和客户关系领先。 [TrendForce 2 月认为 Samsung HBM4 验证领先、SK hynix 保持 volume leadership、Micron 略慢](https://www.trendforce.com/research/download/RP260212TV3)；[Samsung 同日宣布商业出货 HBM4](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 | 未结构化 | 未结构化 |
| 2026-02-12 | [TrendForce HBM Market Bulletin February 2026](https://www.trendforce.com/research/download/RP260212TV3) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 代际与客户资格领先 | 代际控制权可能与存量 HBM3E 份额不同。 | 未结构化 | 未结构化 |
| 2026-02-12 | [TrendForce HBM Market Bulletin February 2026](https://www.trendforce.com/research/download/RP260212TV3) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 代际与客户资格领先 | [Samsung 验证领先，SK volume领先，Micron略慢](https://www.trendforce.com/research/download/RP260212TV3)。 NVIDIA 可能采用三供以满足需求。 资格领先不等于全年份额，仍需实际 shipment 验证。 | 2026-02 | Rubin/HBM4 cycle |
| 2026-02-12 | [TrendForce HBM Market Bulletin February 2026](https://www.trendforce.com/research/download/RP260212TV3) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 替代与 second source | 客户采用多供是降低单一 HBM 风险的自然结果。 [TrendForce 认为 NVIDIA 可能采用三家供应商；份额预测显示 Samsung 上升、SK hynix 回落](https://www.trendforce.com/research/download/RP260212TV3)。 | 未结构化 | 未结构化 |
| 2026-02-12 | [TrendForce HBM Market Bulletin February 2026](https://www.trendforce.com/research/download/RP260212TV3) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 替代与 second source | 若 Samsung/Micron 按期通过关键平台并提升份额，SK hynix 仍是龙头但超额控制权会减弱。 | 未结构化 | 未结构化 |
| 2026-02-12 | [TrendForce HBM Market Bulletin February 2026](https://www.trendforce.com/research/download/RP260212TV3) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 替代与 second source | TrendForce assessed Samsung as leading HBM4 validation, SK hynix as retaining volume leadership and Micron as slightly behind, while NVIDIA was expected to use all three suppliers under tight capacity. | 未结构化 | 未结构化 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 良率与量产速度 | [SK hynix FY25 业绩将纪录表现归因于 AI memory/HBM leadership](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。 [Samsung HBM4 已进入 mass production/commercial shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)，说明 second source 不再只是样品。 | 未结构化 | 未结构化 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 良率与量产速度 | 需要季度 shipment 和客户平台覆盖验证量产份额。 | 未结构化 | 未结构化 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 良率与量产速度 | SK hynix FY2025 revenue was KRW97.1467T, operating profit KRW47.2063T and operating margin 49%, driven by AI memory and HBM leadership. | 未结构化 | 未结构化 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 客户与合同锁定 | HBM 合同锁定通常早于交付，反映客户为供给确定性付费。 [Micron 2026 全年 HBM supply 已完成 price and volume agreements](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 | 未结构化 | 未结构化 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 客户与合同锁定 | 协议提高可见度，但不证明 Micron 最终份额或 margin 一定高于同行。 | 未结构化 | 未结构化 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 客户与合同锁定 | [价量协议全部完成](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 已锁定供给将随客户平台资格转为 shipment/revenue。 合同覆盖强，但需实际出货与毛利验证。 | CY2026 supply | CY2026 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 客户与合同锁定 | Micron prepared remarks forecast HBM TAM from about $35B in calendar 2025 to around $100B in calendar 2028, about 40% CAGR, and said 2026 HBM supply had completed price and volume agreements. | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 13 | 13 | 0 | 0 | 0 | 0 | 26 | 0 | 2025-12-17 | 2026-03-09 | 单向覆盖，缺反证 |

### Q4 · 是否已经财务兑现？

**结论强度：** 中高：公司利润和高价值产品 mix 同时改善；HBM 独立收入与毛利披露仍不充分。  
**最近材料：** 2026-01-29

#### 基本理解思路

- **专业模型：** HBM 价量 mix 到利润现金流模型
- **研究目的：** 验证 HBM 稀缺是否已经进入供应商收入、产品 mix、利润率、资本开支和现金流。
- **判断规则：** HBM 财务兑现 = shipment x ASP -> HBM revenue/mix -> gross/operating margin -> operating cash flow/FCF，扣除 capex 与库存占用。
- **理解提示：** HBM 价量 → HBM 收入与产品 mix → 毛利与营业利润率 → 资本开支与库存 → 现金流兑现

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

HBM 已经进入财务兑现阶段，但公司层报表仍混有普通 DRAM/NAND 周期。SK hynix FY2024 至 FY2025 收入由 66.2 万亿韩元增至 97.1 万亿、营业利润由 23.5 万亿增至 47.2 万亿，营业利润率由 35% 升至 49%；Micron FY2023 至 FY2025 收入由 155 亿美元升至 374 亿、毛利率由 -9% 升至约 40%，且 HBM、高容量 DIMM 与低功耗 server DRAM 合计收入在 FY2025 达 100 亿美元、同比超过五倍。利润兑现很强，但不能把全部利润改善都归因于 HBM；仍需分产品收入、capex、库存和 FCF 做桥接。

**支持机制：** HBM 高 ASP、高价值 mix 和已锁定需求推动收入与利润率上升，规模扩大后经营现金流改善。

**最大反证：** 普通 DRAM 价格周期、库存回补或会计减值反转也能改善利润；若 capex/库存增速超过现金流，HBM 利润质量会下降。

**对标的的影响：** SK hynix 的财务兑现确定性最高；Micron 的利润弹性更大但混合周期更强；Samsung 需把 HBM4 份额修复转成可辨认的 Memory/DS 利润。

**关键来源：** [SK hynix FY2024 results](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/)；[Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)；[Micron FY2025 Q4 prepared remarks](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218)；[TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY)；[Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)；[SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)；[Samsung Q4 and FY2025 results](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | HBM 已经进入财务兑现阶段，但公司层报表仍混有普通 DRAM/NAND 周期。SK hynix FY2024 至 FY2025 收入由 66.2 万亿韩元增至 97.1 万亿、营业利润由 23.5 万亿增至 47.2 万亿，营业利润率由 35% 升至 49%；Micron FY2023 至 FY2025 收入由 155 亿美元升至 374 亿、毛利率由 -9% 升至约 40%，且 HBM、高容量 DIMM 与低功耗 server DRAM 合计收入在 FY2025 达 100 亿美元、同比超过五倍。利润兑现很强，但不能把全部利润改善都归因于 HBM；仍需分产品收入、capex、库存和 FCF 做桥接。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2025-01-23 | [SK hynix FY2024 results](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/) | 事实 / 支持 | [SK hynix 4Q24 HBM 已超过 DRAM revenue 的 40%](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/)。 [Micron 高价值 server memory 组合快速增长](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218)；[Samsung Memory 4Q25 因 HBM 等高价值产品创纪录](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results)。 |
| 2025-01-23 | [SK hynix FY2024 results](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/) | 预测 / 支持 | HBM4 mix 能否继续提高决定利润池是否延续。 |
| 2025-01-23 | [SK hynix FY2024 results](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/) | 预测 / 支持 | 三家公司高价值 memory mix 均上升。 HBM4与高端AI memory继续扩张。 各家公司披露维度不同，需分别追踪，不能合并成份额表。 |
| 2025-01-23 | [SK hynix FY2024 results](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/) | 事实 / 支持 | [SK hynix FY2024 operating margin 35%](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/)；[FY2025 升至49%](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。[Micron FY2023-FY2025 gross margin从-9%升至39.8%](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)。 利润率提升与 HBM/高端 mix 同向，但也包含普通 DRAM/NAND 价格回升。 |
| 2025-01-23 | [SK hynix FY2024 results](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/) | 预测 / 支持 | 若 HBM 供需偏紧延续，margin 可维持高位；供给释放和普通 DRAM 周期反转会压低。 |
| 2025-01-23 | [SK hynix FY2024 results](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/) | 事实 / 支持 | SK hynix FY2024 revenue was KRW66.1930T, operating profit KRW23.4673T and operating margin 35%; HBM exceeded 40% of DRAM revenue in Q4 2024. |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 事实 / 支持 | [SK hynix FY2024 operating margin 35%](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/)；[FY2025 升至49%](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。[Micron FY2023-FY2025 gross margin从-9%升至39.8%](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)。 利润率提升与 HBM/高端 mix 同向，但也包含普通 DRAM/NAND 价格回升。 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 预测 / 支持 | 若 HBM 供需偏紧延续，margin 可维持高位；供给释放和普通 DRAM 周期反转会压低。 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 预测 / 支持 | [SK operating margin 49%；Micron gross margin 39.8%](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。 已锁定 HBM 需求支持高端 mix，但没有同口径全年 margin guide。 一个是 operating margin，一个是 gross margin，只比较趋势，不比较绝对值。 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 事实 / 支持 | [Micron FY2025 net capex 138 亿美元](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)。 高 capex 是扩供必要条件，也会提高周期反转时的下行风险。 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 预测 / 支持 | 需要把 capex 转为 qualified capacity，并跟踪库存是否快于收入增长。 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 预测 / 支持 | [Micron capex 138亿美元，三家扩充HBM产能](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)。 供给将增长，但资格和后端决定兑现速度。 capex 不是供给，需经过产能漏斗。 |

时间线先展示最早 12 条；完整 40 条见“映射材料”。

#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01-29 | [Samsung Q4 and FY2025 results](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | HBM 收入与产品 mix | [SK hynix 4Q24 HBM 已超过 DRAM revenue 的 40%](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/)。 [Micron 高价值 server memory 组合快速增长](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218)；[Samsung Memory 4Q25 因 HBM 等高价值产品创纪录](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results)。 | 未结构化 | 未结构化 |
| 2026-01-29 | [Samsung Q4 and FY2025 results](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | HBM 收入与产品 mix | HBM4 mix 能否继续提高决定利润池是否延续。 | 未结构化 | 未结构化 |
| 2026-01-29 | [Samsung Q4 and FY2025 results](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | HBM 收入与产品 mix | 三家公司高价值 memory mix 均上升。 HBM4与高端AI memory继续扩张。 各家公司披露维度不同，需分别追踪，不能合并成份额表。 | 4Q24-FY2025 | 2026E |
| 2026-01-29 | [Samsung Q4 and FY2025 results](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | HBM 收入与产品 mix | Samsung Q4 2025 Memory Business reached record quarterly revenue and operating profit, with HBM, server DDR5 and enterprise SSD as high-value AI products. | 未结构化 | 未结构化 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 毛利与营业利润率 | [SK hynix FY2024 operating margin 35%](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/)；[FY2025 升至49%](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。[Micron FY2023-FY2025 gross margin从-9%升至39.8%](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)。 利润率提升与 HBM/高端 mix 同向，但也包含普通 DRAM/NAND 价格回升。 | 未结构化 | 未结构化 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 毛利与营业利润率 | 若 HBM 供需偏紧延续，margin 可维持高位；供给释放和普通 DRAM 周期反转会压低。 | 未结构化 | 未结构化 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 毛利与营业利润率 | [SK operating margin 49%；Micron gross margin 39.8%](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。 已锁定 HBM 需求支持高端 mix，但没有同口径全年 margin guide。 一个是 operating margin，一个是 gross margin，只比较趋势，不比较绝对值。 | FY2025 | CY2026 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 毛利与营业利润率 | SK hynix FY2025 revenue was KRW97.1467T, operating profit KRW47.2063T and operating margin 49%, driven by AI memory and HBM leadership. | 未结构化 | 未结构化 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | HBM 价量 | [Micron FY2025 HBM、高容量 DIMM 与 LP server DRAM 合计收入达到 100 亿美元、同比超过五倍](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218)。 [FY26 Q1 HBM 和 data-center revenue 再创新高，2026 supply 完成价量协议](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 | 未结构化 | 未结构化 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | HBM 价量 | 实际财务桥仍需 HBM 独立 shipment、ASP 和 revenue。 | 未结构化 | 未结构化 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | HBM 价量 | [高价值 server memory组合收入100亿美元、HBM revenue再创新高](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218)。 [全部HBM供给已完成价量协议](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 组合收入比纯 HBM 更宽，不能直接推 HBM revenue。 | FY2025 / FY26 Q1 | CY2026 supply |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 现金流兑现 | [OCF 175.3亿美元、adjusted FCF 37.2亿美元](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)。 HBM价量协议提高收入可见度，但公开材料未给HBM专属FCF指引。 用公司现金流校验利润质量，不把它全部归因于HBM。 | FY2025 | CY2026 |
| 2025-12-17 | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | HBM 价量 | Micron prepared remarks forecast HBM TAM from about $35B in calendar 2025 to around $100B in calendar 2028, about 40% CAGR, and said 2026 HBM supply had completed price and volume agreements. | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 资本开支与库存 | [Micron FY2025 net capex 138 亿美元](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)。 高 capex 是扩供必要条件，也会提高周期反转时的下行风险。 | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 资本开支与库存 | 需要把 capex 转为 qualified capacity，并跟踪库存是否快于收入增长。 | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 预测 / 支持 | 资本开支与库存 | [Micron capex 138亿美元，三家扩充HBM产能](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)。 供给将增长，但资格和后端决定兑现速度。 capex 不是供给，需经过产能漏斗。 | FY2025 / 4Q25 | 2026E |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 资本开支与库存 | TrendForce said SK hynix led with about 150K TSV capacity; yield, certification and backend capacity constrained near-term supply; all three suppliers planned HBM4 mass production in 2026. | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 毛利与营业利润率 | [SK hynix FY2024 operating margin 35%](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/)；[FY2025 升至49%](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。[Micron FY2023-FY2025 gross margin从-9%升至39.8%](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)。 利润率提升与 HBM/高端 mix 同向，但也包含普通 DRAM/NAND 价格回升。 | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 毛利与营业利润率 | 若 HBM 供需偏紧延续，margin 可维持高位；供给释放和普通 DRAM 周期反转会压低。 | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 毛利与营业利润率 | [SK operating margin 49%；Micron gross margin 39.8%](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。 已锁定 HBM 需求支持高端 mix，但没有同口径全年 margin guide。 一个是 operating margin，一个是 gross margin，只比较趋势，不比较绝对值。 | FY2025 | CY2026 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 资本开支与库存 | [Micron FY2025 net capex 138 亿美元](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)。 高 capex 是扩供必要条件，也会提高周期反转时的下行风险。 | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 资本开支与库存 | 需要把 capex 转为 qualified capacity，并跟踪库存是否快于收入增长。 | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 资本开支与库存 | [Micron capex 138亿美元，三家扩充HBM产能](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)。 供给将增长，但资格和后端决定兑现速度。 capex 不是供给，需经过产能漏斗。 | FY2025 / 4Q25 | 2026E |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 现金流兑现 | [Micron FY2025 operating cash flow 175.3 亿美元，FY2024 为 85.1 亿美元；adjusted FCF 37.2 亿美元](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)。 现金流已改善，但 HBM 专属现金流无法从公开报表分离。 | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 现金流兑现 | 若 HBM mix 和价量协议兑现，OCF 应继续覆盖更高 capex；若库存/应收上升，需降级。 | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 现金流兑现 | [OCF 175.3亿美元、adjusted FCF 37.2亿美元](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)。 HBM价量协议提高收入可见度，但公开材料未给HBM专属FCF指引。 用公司现金流校验利润质量，不把它全部归因于HBM。 | FY2025 | CY2026 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 现金流兑现 | Micron FY2025 revenue was $37.378B, GAAP gross margin was 39.8%, operating cash flow was $17.53B, adjusted free cash flow was $3.72B and net capex was $13.80B. | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 Q4 prepared remarks](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | HBM 价量 | [Micron FY2025 HBM、高容量 DIMM 与 LP server DRAM 合计收入达到 100 亿美元、同比超过五倍](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218)。 [FY26 Q1 HBM 和 data-center revenue 再创新高，2026 supply 完成价量协议](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 Q4 prepared remarks](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | HBM 价量 | 实际财务桥仍需 HBM 独立 shipment、ASP 和 revenue。 | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 Q4 prepared remarks](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | HBM 价量 | [高价值 server memory组合收入100亿美元、HBM revenue再创新高](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218)。 [全部HBM供给已完成价量协议](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9)。 组合收入比纯 HBM 更宽，不能直接推 HBM revenue。 | FY2025 / FY26 Q1 | CY2026 supply |
| 2025-09-23 | [Micron FY2025 Q4 prepared remarks](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | HBM 收入与产品 mix | [SK hynix 4Q24 HBM 已超过 DRAM revenue 的 40%](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/)。 [Micron 高价值 server memory 组合快速增长](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218)；[Samsung Memory 4Q25 因 HBM 等高价值产品创纪录](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results)。 | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 Q4 prepared remarks](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | HBM 收入与产品 mix | HBM4 mix 能否继续提高决定利润池是否延续。 | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 Q4 prepared remarks](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | HBM 收入与产品 mix | 三家公司高价值 memory mix 均上升。 HBM4与高端AI memory继续扩张。 各家公司披露维度不同，需分别追踪，不能合并成份额表。 | 4Q24-FY2025 | 2026E |
| 2025-09-23 | [Micron FY2025 Q4 prepared remarks](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | HBM 收入与产品 mix | Micron said combined HBM, high-capacity DIMM and low-power server DRAM revenue reached $10B in FY2025, more than five times the prior fiscal year. | 未结构化 | 未结构化 |
| 2025-01-23 | [SK hynix FY2024 results](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | HBM 收入与产品 mix | [SK hynix 4Q24 HBM 已超过 DRAM revenue 的 40%](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/)。 [Micron 高价值 server memory 组合快速增长](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218)；[Samsung Memory 4Q25 因 HBM 等高价值产品创纪录](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results)。 | 未结构化 | 未结构化 |
| 2025-01-23 | [SK hynix FY2024 results](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | HBM 收入与产品 mix | HBM4 mix 能否继续提高决定利润池是否延续。 | 未结构化 | 未结构化 |
| 2025-01-23 | [SK hynix FY2024 results](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | HBM 收入与产品 mix | 三家公司高价值 memory mix 均上升。 HBM4与高端AI memory继续扩张。 各家公司披露维度不同，需分别追踪，不能合并成份额表。 | 4Q24-FY2025 | 2026E |
| 2025-01-23 | [SK hynix FY2024 results](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 毛利与营业利润率 | [SK hynix FY2024 operating margin 35%](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/)；[FY2025 升至49%](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。[Micron FY2023-FY2025 gross margin从-9%升至39.8%](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)。 利润率提升与 HBM/高端 mix 同向，但也包含普通 DRAM/NAND 价格回升。 | 未结构化 | 未结构化 |
| 2025-01-23 | [SK hynix FY2024 results](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/) | 公司官方材料 / 历史 / 手动导入 | 预测 / 支持 | 毛利与营业利润率 | 若 HBM 供需偏紧延续，margin 可维持高位；供给释放和普通 DRAM 周期反转会压低。 | 未结构化 | 未结构化 |
| 2025-01-23 | [SK hynix FY2024 results](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 毛利与营业利润率 | SK hynix FY2024 revenue was KRW66.1930T, operating profit KRW23.4673T and operating margin 35%; HBM exceeded 40% of DRAM revenue in Q4 2024. | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 18 | 22 | 0 | 0 | 0 | 0 | 40 | 0 | 2025-01-23 | 2026-01-29 | 单向覆盖，缺反证 |

### Q5 · 市场是否已定价？

**结论强度：** 未完成：保持 watch_only/no_action，不输出赔率结论。  
**最近材料：** 2026-01-29

#### 基本理解思路

- **专业模型：** 市场隐含 HBM 路径与预期差模型
- **研究目的：** 把研究截面的估值、盈利预测和 HBM 利润桥还原成市场已经计入的增长路径。
- **判断规则：** 赔率 = 研究情景下的 HBM 收入/利润路径 - 市场隐含的 HBM 份额、ASP、margin 与终值路径。
- **理解提示：** 研究截面估值 → 市场隐含 HBM 路径 → 盈利上修 → 情景赔率

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

本问未完成。当前证据包能证明 HBM 需求、供给和利润兑现，却没有保存 2026-03-28 截面的 SK hynix、Micron、Samsung 同口径估值、盈利一致预期、盈利上修历史和 reverse-DCF 隐含 HBM 路径。没有这些数据，不能判断市场是否已把 2028 年 HBM 空间、各家份额和高利润率充分定价，也不能把产业强度直接翻译成可买赔率。

**支持机制：** 若市场隐含的 HBM 份额、ASP 和 margin 明显低于可验证基准情景，才存在预期差。

**最大反证：** 若估值已要求龙头长期维持高份额、高 ASP 和高 margin，任何供给释放都会造成估值压缩。

**对标的的影响：** 由于定价问未通过，HBM 相关标的不能升级为 actionable_long；当前只能比较产业胜率，不能给出买入排序。

**关键来源：** [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)；[SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)；[Samsung Q4 and FY2025 results](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 本问未完成。当前证据包能证明 HBM 需求、供给和利润兑现，却没有保存 2026-03-28 截面的 SK hynix、Micron、Samsung 同口径估值、盈利一致预期、盈利上修历史和 reverse-DCF 隐含 HBM 路径。没有这些数据，不能判断市场是否已把 2028 年 HBM 空间、各家份额和高利润率充分定价，也不能把产业强度直接翻译成可买赔率。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 估值 / 支持 | 需求与财务数据可用于后续情景输入，但没有估值起点。 不能计算胜率/赔率。 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 估值 / 支持 | 先补估值和隐含路径，再做悲观/基准/乐观情景。 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 估值 / 支持 | 不能计算胜率/赔率。 未找到与本环节严格对齐的未来指引或预测。 缺口保留，不用模型先验填充。 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 估值 / 支持 | Micron FY2025 revenue was $37.378B, GAAP gross margin was 39.8%, operating cash flow was $17.53B, adjusted free cash flow was $3.72B and net capex was $13.80B. |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 估值 / 支持 | 需求与财务数据可用于后续情景输入，但没有估值起点。 不能计算胜率/赔率。 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 估值 / 支持 | 先补估值和隐含路径，再做悲观/基准/乐观情景。 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 估值 / 支持 | 不能计算胜率/赔率。 未找到与本环节严格对齐的未来指引或预测。 缺口保留，不用模型先验填充。 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 估值 / 支持 | SK hynix FY2025 revenue was KRW97.1467T, operating profit KRW47.2063T and operating margin 49%, driven by AI memory and HBM leadership. |
| 2026-01-29 | [Samsung Q4 and FY2025 results](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results) | 估值 / 支持 | 需求与财务数据可用于后续情景输入，但没有估值起点。 不能计算胜率/赔率。 |
| 2026-01-29 | [Samsung Q4 and FY2025 results](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results) | 估值 / 支持 | 先补估值和隐含路径，再做悲观/基准/乐观情景。 |
| 2026-01-29 | [Samsung Q4 and FY2025 results](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results) | 估值 / 支持 | 不能计算胜率/赔率。 未找到与本环节严格对齐的未来指引或预测。 缺口保留，不用模型先验填充。 |
| 2026-01-29 | [Samsung Q4 and FY2025 results](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results) | 估值 / 支持 | Samsung Q4 2025 Memory Business reached record quarterly revenue and operating profit, with HBM, server DDR5 and enterprise SSD as high-value AI products. |



#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01-29 | [Samsung Q4 and FY2025 results](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 情景赔率 | 需求与财务数据可用于后续情景输入，但没有估值起点。 不能计算胜率/赔率。 | 未结构化 | 未结构化 |
| 2026-01-29 | [Samsung Q4 and FY2025 results](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 情景赔率 | 先补估值和隐含路径，再做悲观/基准/乐观情景。 | 未结构化 | 未结构化 |
| 2026-01-29 | [Samsung Q4 and FY2025 results](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 情景赔率 | 不能计算胜率/赔率。 未找到与本环节严格对齐的未来指引或预测。 缺口保留，不用模型先验填充。 | 见历史与现状 | 待补 |
| 2026-01-29 | [Samsung Q4 and FY2025 results](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 情景赔率 | Samsung Q4 2025 Memory Business reached record quarterly revenue and operating profit, with HBM, server DDR5 and enterprise SSD as high-value AI products. | 未结构化 | 未结构化 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 情景赔率 | 需求与财务数据可用于后续情景输入，但没有估值起点。 不能计算胜率/赔率。 | 未结构化 | 未结构化 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 情景赔率 | 先补估值和隐含路径，再做悲观/基准/乐观情景。 | 未结构化 | 未结构化 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 情景赔率 | 不能计算胜率/赔率。 未找到与本环节严格对齐的未来指引或预测。 缺口保留，不用模型先验填充。 | 见历史与现状 | 待补 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 情景赔率 | SK hynix FY2025 revenue was KRW97.1467T, operating profit KRW47.2063T and operating margin 49%, driven by AI memory and HBM leadership. | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 情景赔率 | 需求与财务数据可用于后续情景输入，但没有估值起点。 不能计算胜率/赔率。 | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 情景赔率 | 先补估值和隐含路径，再做悲观/基准/乐观情景。 | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 情景赔率 | 不能计算胜率/赔率。 未找到与本环节严格对齐的未来指引或预测。 缺口保留，不用模型先验填充。 | 见历史与现状 | 待补 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 情景赔率 | Micron FY2025 revenue was $37.378B, GAAP gross margin was 39.8%, operating cash flow was $17.53B, adjusted free cash flow was $3.72B and net capex was $13.80B. | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 12 | 0 | 12 | 0 | 2025-09-23 | 2026-01-29 | 有材料，结构不完整 |

### Q6 · 反证是什么？

**结论强度：** 中高：已有真实反向来源；量化阈值和估值触发器仍需下一轮补齐。  
**最近材料：** 2026-03-20

#### 基本理解思路

- **专业模型：** HBM 触发器、阈值与降级动作模型
- **研究目的：** 为需求、单位含量、供给、控制权、财务和定价分别定义可观测反证。
- **判断规则：** 反证 = 已观察到的逆向证据 + 可量化阈值 + 检查频率 + 对结论/标的的降级动作。
- **理解提示：** 需求反证 → 单位含量反证 → 供给反证 → 控制权反证 → 财务与定价反证

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

已观察到的反向证据不是“AI 泡沫”这种泛风险，而是三条具体变化：第一，TrendForce 在 2026-03-20 指出更高 HBM4 规格导致验证延迟，可能下修早期 HBM4 shipment 并推迟下一代平台；第二，Samsung 已商业出货 HBM4、预计 2026 HBM 销售超过三倍并扩产，供给释放可能压低中期稀缺溢价；第三，TrendForce 预计 SK hynix HBM bit share 从 2025 年约 59% 降至 2026 年约 50%，Samsung 从约 20% 升至 28%，说明行业增长不等于龙头份额永远稳定。反证已真实存在，但尚缺明确季度阈值和 cutoff 估值触发器。

**支持机制：** HBM 主线仍强，但真实反证能阻止把短缺、份额和利润率线性外推。

**最大反证：** 如果反证被后续实际数据否定，例如验证恢复、份额稳定且 ASP/margin 继续上行，则不应仅凭一次延迟降级长期 S 曲线。

**对标的的影响：** SK hynix 需监控份额和 HBM4 资格，Samsung 需监控扩产是否转利润，Micron 需监控验证和份额；任何标的都必须绑定需求、供给、份额、margin 和估值触发器。

**关键来源：** [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8)；[TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY)；[SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)；[Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)；[TrendForce HBM supplier share outlook](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/)；[NVIDIA platform HBM specification progression](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/)；[TrendForce HBM Market Bulletin March 2026](https://www.trendforce.com/research/download/RP260320WK3)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 已观察到的反向证据不是“AI 泡沫”这种泛风险，而是三条具体变化：第一，TrendForce 在 2026-03-20 指出更高 HBM4 规格导致验证延迟，可能下修早期 HBM4 shipment 并推迟下一代平台；第二，Samsung 已商业出货 HBM4、预计 2026 HBM 销售超过三倍并扩产，供给释放可能压低中期稀缺溢价；第三，TrendForce 预计 SK hynix HBM bit share 从 2025 年约 59% 降至 2026 年约 50%，Samsung 从约 20% 升至 28%，说明行业增长不等于龙头份额永远稳定。反证已真实存在，但尚缺明确季度阈值和 cutoff 估值触发器。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 反证 / 反证 | [SK hynix 与 Micron 利润率/现金流在截面前仍改善](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。 财务反证尚未触发，但由于 Q5 估值数据缺失，无法判断价格端是否已过度定价。 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 反证 / 反证 | 季度监控 gross/operating margin、inventory days、FCF、earnings revisions 和 as-of valuation。 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 反证 / 反证 | 利润率与FCF尚未恶化。 若margin下行、inventory上升、FCF恶化且估值仍高，则降级。 阈值需要公司历史波动和估值数据校准。 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 反证 / 反证 | Micron FY2025 revenue was $37.378B, GAAP gross margin was 39.8%, operating cash flow was $17.53B, adjusted free cash flow was $3.72B and net capex was $13.80B. |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 反证 / 反证 | [TrendForce 记录三家供应商扩充 HBM 前后端](https://www.trendforce.com/research/download/RP251029MY)。 [Samsung HBM4 已商业出货，并预计2026 HBM销售超过三倍](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 反证 / 反证 | 若新增合格供给伴随 ASP/lead time 下行，则 shortage thesis 降级。 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 反证 / 反证 | TrendForce said SK hynix led with about 150K TSV capacity; yield, certification and backend capacity constrained near-term supply; all three suppliers planned HBM4 mass production in 2026. |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 反证 / 反证 | [SK hynix 与 Micron 利润率/现金流在截面前仍改善](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。 财务反证尚未触发，但由于 Q5 估值数据缺失，无法判断价格端是否已过度定价。 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 反证 / 反证 | 季度监控 gross/operating margin、inventory days、FCF、earnings revisions 和 as-of valuation。 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 反证 / 反证 | 利润率与FCF尚未恶化。 若margin下行、inventory上升、FCF恶化且估值仍高，则降级。 阈值需要公司历史波动和估值数据校准。 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 反证 / 反证 | SK hynix FY2025 revenue was KRW97.1467T, operating profit KRW47.2063T and operating margin 49%, driven by AI memory and HBM leadership. |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 反证 / 反证 | [TrendForce 记录三家供应商扩充 HBM 前后端](https://www.trendforce.com/research/download/RP251029MY)。 [Samsung HBM4 已商业出货，并预计2026 HBM销售超过三倍](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 |

时间线先展示最早 12 条；完整 27 条见“映射材料”。

#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-03-20 | [TrendForce HBM Market Bulletin March 2026](https://www.trendforce.com/research/download/RP260320WK3) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 需求反证 | 在强需求背景下，平台时点仍可能因 memory qualification 延后。 [TrendForce 指出 HBM4 验证延迟可能下修早期 shipment，并促使客户推迟下一代 AI 平台](https://www.trendforce.com/research/download/RP260320WK3)。 | 未结构化 | 未结构化 |
| 2026-03-20 | [TrendForce HBM Market Bulletin March 2026](https://www.trendforce.com/research/download/RP260320WK3) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 需求反证 | 若 delay 扩大到 accelerator/server shipment，应降级近端需求。 | 未结构化 | 未结构化 |
| 2026-03-20 | [TrendForce HBM Market Bulletin March 2026](https://www.trendforce.com/research/download/RP260320WK3) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 需求反证 | HBM4 validation delay。 [早期shipment下修、下一代平台可能延迟](https://www.trendforce.com/research/download/RP260320WK3)。 这是需求时点反证，不等于长期TAM消失。 | 2026-03-20 | 2026E |
| 2026-03-20 | [TrendForce HBM Market Bulletin March 2026](https://www.trendforce.com/research/download/RP260320WK3) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 需求反证 | TrendForce said stricter HBM4 specifications delayed supplier validation, creating downside risk to early HBM4 shipments and next-generation AI platform timing; unmet HBM4 demand could shift back to HBM3E. | 未结构化 | 未结构化 |
| 2026-03-16 | [NVIDIA platform HBM specification progression](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 单位含量反证 | [单位 HBM 容量尚未出现代际下降](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/)。 该反证在截面日未触发；Rubin 容量持平/上升且带宽显著提升。 | 未结构化 | 未结构化 |
| 2026-03-16 | [NVIDIA platform HBM specification progression](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 单位含量反证 | 若后续平台通过更少 HBM 达到同等吞吐，则需求弹性下降。 | 未结构化 | 未结构化 |
| 2026-03-16 | [NVIDIA platform HBM specification progression](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 单位含量反证 | 单位HBM容量持续提升。 [最高288GB HBM4、22TB/s](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/)。 暂不构成反证；后续每代复核。 | Hopper-Blackwell | Rubin |
| 2026-03-16 | [NVIDIA platform HBM specification progression](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 单位含量反证 | NVIDIA platform specifications show H100 at 80GB HBM, H200 at 141GB, Blackwell at 192GB, Blackwell Ultra at 288GB and Rubin at up to 288GB HBM4 with up to 22TB/s bandwidth. | 未结构化 | 未结构化 |
| 2026-03-09 | [TrendForce HBM supplier share outlook](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/) | 市场消息 / 历史 / 手动导入 | 反证 / 反证 | 控制权反证 | [TrendForce 份额预测显示 SK hynix 下行、Samsung 上行](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/)。 控制权仍集中，但份额迁移是具体反证。 | 未结构化 | 未结构化 |
| 2026-03-09 | [TrendForce HBM supplier share outlook](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/) | 市场消息 / 历史 / 手动导入 | 反证 / 反证 | 控制权反证 | 若实际出货印证，SK hynix 的行业胜率仍高但公司超额利润需下调；Samsung 反向上调。 | 未结构化 | 未结构化 |
| 2026-03-09 | [TrendForce HBM supplier share outlook](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/) | 市场消息 / 历史 / 手动导入 | 反证 / 反证 | 控制权反证 | SK hynix约59%、Samsung约20%。 [SK hynix约50%、Samsung约28%](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/)。 同口径预测，适合做份额反证。 | 2025E | 2026E |
| 2026-03-09 | [TrendForce HBM supplier share outlook](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/) | 市场消息 / 历史 / 手动导入 | 反证 / 反证 | 控制权反证 | TrendForce-related public reporting projected SK hynix global HBM bit output share at 59% in 2025 and 50% in 2026, while Samsung could rise from 20% to 28%; these are forecasts rather than audited actual shares. | 未结构化 | 未结构化 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 供给反证 | [TrendForce 记录三家供应商扩充 HBM 前后端](https://www.trendforce.com/research/download/RP251029MY)。 [Samsung HBM4 已商业出货，并预计2026 HBM销售超过三倍](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 | 未结构化 | 未结构化 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 供给反证 | 若新增合格供给伴随 ASP/lead time 下行，则 shortage thesis 降级。 | 未结构化 | 未结构化 |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 供给反证 | [HBM4商业出货](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 [HBM sales预计超过三倍并扩产](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 这是供给短缺的直接反证，但最终要看总需求与ASP。 | 2026-02 | CY2026E |
| 2026-02-12 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 供给反证 | Samsung announced commercial HBM4 shipments, described stable initial mass-production yields, expected 2026 HBM sales to more than triple versus 2025 and said it was expanding HBM4 capacity. | 未结构化 | 未结构化 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 财务与定价反证 | [SK hynix 与 Micron 利润率/现金流在截面前仍改善](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。 财务反证尚未触发，但由于 Q5 估值数据缺失，无法判断价格端是否已过度定价。 | 未结构化 | 未结构化 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 财务与定价反证 | 季度监控 gross/operating margin、inventory days、FCF、earnings revisions 和 as-of valuation。 | 未结构化 | 未结构化 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 财务与定价反证 | 利润率与FCF尚未恶化。 若margin下行、inventory上升、FCF恶化且估值仍高，则降级。 阈值需要公司历史波动和估值数据校准。 | FY2025 | 季度监控 |
| 2026-01-28 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 财务与定价反证 | SK hynix FY2025 revenue was KRW97.1467T, operating profit KRW47.2063T and operating margin 49%, driven by AI memory and HBM leadership. | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 供给反证 | [TrendForce 记录三家供应商扩充 HBM 前后端](https://www.trendforce.com/research/download/RP251029MY)。 [Samsung HBM4 已商业出货，并预计2026 HBM销售超过三倍](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)。 | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 供给反证 | 若新增合格供给伴随 ASP/lead time 下行，则 shortage thesis 降级。 | 未结构化 | 未结构化 |
| 2025-10-31 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 供给反证 | TrendForce said SK hynix led with about 150K TSV capacity; yield, certification and backend capacity constrained near-term supply; all three suppliers planned HBM4 mass production in 2026. | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 财务与定价反证 | [SK hynix 与 Micron 利润率/现金流在截面前仍改善](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html)。 财务反证尚未触发，但由于 Q5 估值数据缺失，无法判断价格端是否已过度定价。 | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 财务与定价反证 | 季度监控 gross/operating margin、inventory days、FCF、earnings revisions 和 as-of valuation。 | 未结构化 | 未结构化 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 财务与定价反证 | 利润率与FCF尚未恶化。 若margin下行、inventory上升、FCF恶化且估值仍高，则降级。 阈值需要公司历史波动和估值数据校准。 | FY2025 | 季度监控 |
| 2025-09-23 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 财务与定价反证 | Micron FY2025 revenue was $37.378B, GAAP gross margin was 39.8%, operating cash flow was $17.53B, adjusted free cash flow was $3.72B and net capex was $13.80B. | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 27 | 0 | 27 | 2025-09-23 | 2026-03-20 | 有材料，结构不完整 |

### S 曲线汇总

当前节点的产业逻辑已形成，但仍有 6 个问题未达到高置信。特别是市场定价未闭环时，不能把产业胜率直接写成证券买入赔率。

## 3. 标的推荐

以下只保留映射到当前 BOM 的标的。产业逻辑强不等于证券价格便宜。

| 标的 | 公司 | BOM 节点 | 候选状态 | 最终状态 | 核心理由 | 未来空间 / 赔率 | 主要风险 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 000660.KS | SK hynix | HBM | actionable_long | no_action | HBM 供应能力和 49% operating margin 显示硬约束已经变成利润桥。 | 4 | HBM 供给过快释放、ASP 下行、客户资格落后。 |
| MU | Micron | HBM | watch_only | no_action | HBM TAM、价量协议和云内存利润改善带来高弹性。 | 4 | HBM 份额不及预期、ASP/DRAM 周期反转。 |

## 4. 来源索引

| ID | 来源 | 类别 | 市场可见时间 | 用途摘要 |
| --- | --- | --- | --- | --- |
| SRC-NVDA-FY26-Q4 | [NVIDIA FY2026 Q4 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/) | evidence | 2026-02-25 | NVIDIA Q4 FY26 revenue was $68.1B and Data Center revenue was $62.3B, up 75% YoY. FY2026 revenue was $215.9B, GAAP gross margin was 71.1%, operating income was $130.4B and free cash flow was $96.6B. Q1 FY27 revenue outlook was $78.0B +/-2% with no China Data Center compute revenue assumed. |
| SRC-DELL-FY26-Q4 | [Dell FY2026 Q4 results](https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-3) | evidence | 2026-02-26 | Dell FY26 closed more than $64B in AI-optimized server orders, shipped more than $25B, entered FY27 with a $43B backlog, and guided FY27 AI-optimized server revenue to roughly $50B, up 103% year over year. |
| SRC-MU-FY26-Q1 | [Micron FY2026 Q1 results](https://micron.gcs-web.com/news-releases/news-release-details/micron-technology-inc-reports-results-first-quarter-fiscal-2026) | evidence | 2025-12-17 | Micron FY26 Q1 delivered record revenue and margin expansion, with AI data-center memory demand driving cloud memory and HBM-related strength. |
| SRC-MU-FY26-Q1-PREPARED | [Micron FY2026 Q1 prepared remarks](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9) | evidence | 2025-12-17 | Micron prepared remarks forecast HBM TAM from about $35B in calendar 2025 to around $100B in calendar 2028, about 40% CAGR, and said 2026 HBM supply had completed price and volume agreements. |
| SRC-SKHYNIX-FY25 | [SK hynix FY2025 results](https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html) | evidence | 2026-01-28 | SK hynix FY2025 revenue was KRW97.1467T, operating profit KRW47.2063T and operating margin 49%, driven by AI memory and HBM leadership. |
| SRC-SAMSUNG-FY25 | [Samsung Q4 and FY2025 results](https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results) | evidence | 2026-01-29 | Samsung Q4 2025 Memory Business reached record quarterly revenue and operating profit, with HBM, server DDR5 and enterprise SSD as high-value AI products. |
| SRC-SKHYNIX-FY24 | [SK hynix FY2024 results](https://news.skhynix.com/sk-hynix-announces-4q24-financial-results/) | evidence | 2025-01-23 | SK hynix FY2024 revenue was KRW66.1930T, operating profit KRW23.4673T and operating margin 35%; HBM exceeded 40% of DRAM revenue in Q4 2024. |
| SRC-MU-FY25 | [Micron FY2025 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-fourth-quarter-and-full-8) | evidence | 2025-09-23 | Micron FY2025 revenue was $37.378B, GAAP gross margin was 39.8%, operating cash flow was $17.53B, adjusted free cash flow was $3.72B and net capex was $13.80B. |
| SRC-MU-FY25-Q4-PREPARED | [Micron FY2025 Q4 prepared remarks](https://investors.micron.com/static-files/5fb98d73-2134-4446-8d1b-0f90285f6c02?pubDate=20251218) | evidence | 2025-09-23 | Micron said combined HBM, high-capacity DIMM and low-power server DRAM revenue reached $10B in FY2025, more than five times the prior fiscal year. |
| SRC-NVDA-HBM-SPECS-20260316 | [NVIDIA platform HBM specification progression](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/) | evidence | 2026-03-16 | NVIDIA platform specifications show H100 at 80GB HBM, H200 at 141GB, Blackwell at 192GB, Blackwell Ultra at 288GB and Rubin at up to 288GB HBM4 with up to 22TB/s bandwidth. |
| SRC-SAMSUNG-HBM4-20260212 | [Samsung commercial HBM4 shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | evidence | 2026-02-12 | Samsung announced commercial HBM4 shipments, described stable initial mass-production yields, expected 2026 HBM sales to more than triple versus 2025 and said it was expanding HBM4 capacity. |
| SRC-TF-HBM-INDUSTRY-4Q25 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | research_report | 2025-10-31 | TrendForce said SK hynix led with about 150K TSV capacity; yield, certification and backend capacity constrained near-term supply; all three suppliers planned HBM4 mass production in 2026. |
| SRC-TF-HBM-BULLETIN-20260212 | [TrendForce HBM Market Bulletin February 2026](https://www.trendforce.com/research/download/RP260212TV3) | research_report | 2026-02-12 | TrendForce assessed Samsung as leading HBM4 validation, SK hynix as retaining volume leadership and Micron as slightly behind, while NVIDIA was expected to use all three suppliers under tight capacity. |
| SRC-TF-HBM-BULLETIN-20260320 | [TrendForce HBM Market Bulletin March 2026](https://www.trendforce.com/research/download/RP260320WK3) | research_report | 2026-03-20 | TrendForce said stricter HBM4 specifications delayed supplier validation, creating downside risk to early HBM4 shipments and next-generation AI platform timing; unmet HBM4 demand could shift back to HBM3E. |
| SRC-TF-HBM-SHARE-20260309 | [TrendForce HBM supplier share outlook](https://www.trendforce.com/news/2026/03/09/news-samsung-sk%E2%80%AFhynix-reportedly-tapped-as-nvidia-rubin-hbm4-suppliers-shipments-could-start-in-march/) | message | 2026-03-09 | TrendForce-related public reporting projected SK hynix global HBM bit output share at 59% in 2025 and 50% in 2026, while Samsung could rise from 20% to 28%; these are forecasts rather than audited actual shares. |
| SRC-SA-COWOS-HBM-2023 | [SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share) | research_report | 2023-07-05 | SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer. |
| SRC-TF-HBM-PRICE-20240506 | [TrendForce HBM Prices to Increase by 5-10% in 2025](https://www.trendforce.com/presscenter/news/20240506-12125.html) | research_report | 2024-05-06 | TrendForce estimated HBM ASP at several times conventional DRAM and about five times DDR5, while value share could exceed 30% of DRAM in 2025. |
| SRC-TF-BLACKWELL-HBM-20240808 | [TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption](https://www.trendforce.com/presscenter/news/20240808-12248.html) | research_report | 2024-08-08 | TrendForce described NVIDIA as the largest HBM buyer, expected procurement share above 70%, with HBM consumption growing more than 200% in 2024 and expected to double again in 2025 as Blackwell raises HBM content. |
