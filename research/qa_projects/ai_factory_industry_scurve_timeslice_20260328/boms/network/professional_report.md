---
report_scope: bom-node
project_id: ai_factory_industry_scurve_timeslice_20260328__bom__network
bom_node_id: network
run_mode: historical_backtest
as_of_date: 2026-03-28
---

# AI 工厂 · 高速连接与 AI 网络 BOM 节点研究

[返回 AI 工厂产业总览](../../professional_report.md)

> 研究截面：2026-03-28。本报告只研究 高速连接与 AI 网络，不把其他 BOM 的结论提前扩散到本节点。

## 1. 当前研究的问题

判断 高速连接与 AI 网络 是否处在可投资的 S 曲线阶段，并识别需求、供给、控制权、财务兑现、市场定价和反证的证据边界。

| 节点边界 | 内容 |
| --- | --- |
| 接受什么 | 机柜级带宽、延迟、功耗、平台兼容性和客户导入需求。 |
| 生产什么 | retimer、AEC、optical interconnect、switch silicon、Ethernet/InfiniBand 网络。 |
| 提供给谁 | AI server、rack-scale 系统、云厂商集群。 |
| 代表公司 | Astera Labs、Credo、Marvell、Broadcom、Arista、NVIDIA 网络生态 |
| 验证指标 | revenue growth、design win、800G/1.6T ramp、customer concentration、gross margin。 |

## 2. 行业概况

### 高速连接与 AI 网络

把单台服务器、机柜和集群连成可训练/可推理的系统。

**研究账本说明：** 六问是稳定逻辑坐标；材料按市场可见时间追加到 `BOM × 六问 × 时间` 账本。本报告只展示结论、真实变化和可审计材料，不展示搜索词、解析提示或工具过程。

### Q1 · 当前 BOM 的需求是否会被 S 曲线放大拉动？

**结论强度：** 待验证  
**最近材料：** 2025-07-15

#### 基本理解思路

- **专业模型：** S 曲线传导与弹性模型
- **研究目的：** 判断终端 AI 需求是否真实传导到当前 BOM，并且是否具备大于终端需求的弹性。
- **判断规则：** 可投资需求 = 真实工作负载增长 × 客户预算/订单兑现 × 高速连接与 AI 网络 直接拉动 × 单位用量或单位价值量弹性。
- **理解提示：** 由本节点 playbook 提供。

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

rack-scale 与 cluster-scale AI 提高东西向流量，拉动 retimer、AEC、switch、NIC、光模块和 PAM4 DSP；每 GPU 或每机柜的网络端口、光模块、DSP 和板级连接组件用量随 800G/1.6T 迁移上升，因此网络节点可能具备更高单位弹性。

**支持机制：** 需求可持续的第一性原理是：AI 工作负载、用户任务、上下文长度、多模态和 agent 步数提高总计算/基础设施需求，并通过客户预算进入 高速连接与 AI 网络。

**最大反证：** 若 AI 应用 ROI 不足、模型效率提升快于工作负载增长、客户 capex 下修或订单取消，需求趋势就不可持续。

**对标的的影响：** 本问决定 高速连接与 AI 网络 相关标的是否有足够大的收入天花板和增长斜率。若需求链条不能从工作负载穿透到订单、收入和 BOM 弹性，即使公司质量好，也只能保留观察；若需求强成立，后续才值得继续评估供给稀缺、控制者和定价。

**关键来源：** [SemiAnalysis Nvidia Optical Boogeyman NVL72 Infiniband Scale Out 800G and 1.6T Ramp](https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband)；[LightCounting Optics for AI Clusters](https://www.lightcounting.com/newsletter/en/january-2025-optics-for-ai-clusters-319)；[Dell'Oro Group Ethernet AI Backend Network Forecast](https://www.prnewswire.com/news-releases/ethernet-is-winning-the-war-against-infiniband-in-ai-back-end-networks-according-to-delloro-group-302501890.html)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | rack-scale 与 cluster-scale AI 提高东西向流量，拉动 retimer、AEC、switch、NIC、光模块和 PAM4 DSP；每 GPU 或每机柜的网络端口、光模块、DSP 和板级连接组件用量随 800G/1.6T 迁移上升，因此网络节点可能具备更高单位弹性。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2024-03-25 | [SemiAnalysis Nvidia Optical Boogeyman NVL72 Infiniband Scale Out 800G and 1.6T Ramp](https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband) | 事实 / 支持 | rack-scale 与 cluster-scale AI 提高东西向流量，拉动 retimer、AEC、switch、NIC、光模块和 PAM4 DSP；每 GPU 或每机柜的网络端口、光模块、DSP 和板级连接组件用量随 800G/1.6T 迁移上升，因此网络节点可能具备更高单位弹性。 |
| 2025-01-01 | [LightCounting Optics for AI Clusters](https://www.lightcounting.com/newsletter/en/january-2025-optics-for-ai-clusters-319) | 事实 / 支持 | rack-scale 与 cluster-scale AI 提高东西向流量，拉动 retimer、AEC、switch、NIC、光模块和 PAM4 DSP；每 GPU 或每机柜的网络端口、光模块、DSP 和板级连接组件用量随 800G/1.6T 迁移上升，因此网络节点可能具备更高单位弹性。 |
| 2025-07-15 | [Dell'Oro Group Ethernet AI Backend Network Forecast](https://www.prnewswire.com/news-releases/ethernet-is-winning-the-war-against-infiniband-in-ai-back-end-networks-according-to-delloro-group-302501890.html) | 事实 / 支持 | rack-scale 与 cluster-scale AI 提高东西向流量，拉动 retimer、AEC、switch、NIC、光模块和 PAM4 DSP；每 GPU 或每机柜的网络端口、光模块、DSP 和板级连接组件用量随 800G/1.6T 迁移上升，因此网络节点可能具备更高单位弹性。 |



#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-07-15 | [Dell'Oro Group Ethernet AI Backend Network Forecast](https://www.prnewswire.com/news-releases/ethernet-is-winning-the-war-against-infiniband-in-ai-back-end-networks-according-to-delloro-group-302501890.html) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | rack-scale 与 cluster-scale AI 提高东西向流量，拉动 retimer、AEC、switch、NIC、光模块和 PAM4 DSP；每 GPU 或每机柜的网络端口、光模块、DSP 和板级连接组件用量随 800G/1.6T 迁移上升，因此网络节点可能具备更高单位弹性。 | 未结构化 | 未结构化 |
| 2025-01-01 | [LightCounting Optics for AI Clusters](https://www.lightcounting.com/newsletter/en/january-2025-optics-for-ai-clusters-319) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | rack-scale 与 cluster-scale AI 提高东西向流量，拉动 retimer、AEC、switch、NIC、光模块和 PAM4 DSP；每 GPU 或每机柜的网络端口、光模块、DSP 和板级连接组件用量随 800G/1.6T 迁移上升，因此网络节点可能具备更高单位弹性。 | 未结构化 | 未结构化 |
| 2024-03-25 | [SemiAnalysis Nvidia Optical Boogeyman NVL72 Infiniband Scale Out 800G and 1.6T Ramp](https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | rack-scale 与 cluster-scale AI 提高东西向流量，拉动 retimer、AEC、switch、NIC、光模块和 PAM4 DSP；每 GPU 或每机柜的网络端口、光模块、DSP 和板级连接组件用量随 800G/1.6T 迁移上升，因此网络节点可能具备更高单位弹性。 | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 2024-03-25 | 2025-07-15 | 单向覆盖，缺反证 |

### Q2 · 供给能否跟上？

**结论强度：** 待验证  
**最近材料：** 2026-02-26

#### 基本理解思路

- **专业模型：** 产能 / 良率 / 周期 / 认证模型
- **研究目的：** 判断有效供给释放速度是否慢于需求斜率。
- **判断规则：** 有效供给 = 名义产能 × 良率 × 客户认证 × 设备/材料可得性 × 交付周期；若有效供给斜率低于需求斜率，高速连接与 AI 网络 才具备稀缺性。
- **理解提示：** 由本节点 playbook 提供。

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

约束来自客户设计导入、平台认证、低功耗/低延迟指标、信号完整性和批量可靠性。

**支持机制：** 供给约束可持续来自产能、良率、认证、交期、工程交付和客户锁定慢于需求斜率。

**最大反证：** 若扩产、良率、替代供应商和客户认证同步释放，短缺会转为价格和毛利压力。

**对标的的影响：** 本问决定 高速连接与 AI 网络 是否具备 chokepoint 属性。供给跟不上时，控制有效产能和认证资源的公司才可能获得价格、毛利和 backlog 弹性；如果供给快速释放，标的推荐应从“稀缺溢价”降为“行业 beta”。

**关键来源：** [SemiAnalysis Nvidia Optical Boogeyman NVL72 Infiniband Scale Out 800G and 1.6T Ramp](https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband)；[LightCounting AI Capex Flows Down the Supply Chain to DSP Vendors](https://www.lightcounting.com/newsletter/en/ai-capex-flows-down-the-supply-chain-to-dsp-vendors-332)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 约束来自客户设计导入、平台认证、低功耗/低延迟指标、信号完整性和批量可靠性。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2024-03-25 | [SemiAnalysis Nvidia Optical Boogeyman NVL72 Infiniband Scale Out 800G and 1.6T Ramp](https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband) | 事实 / 支持 | 约束来自客户设计导入、平台认证、低功耗/低延迟指标、信号完整性和批量可靠性。 |
| 2026-02-26 | [LightCounting AI Capex Flows Down the Supply Chain to DSP Vendors](https://www.lightcounting.com/newsletter/en/ai-capex-flows-down-the-supply-chain-to-dsp-vendors-332) | 事实 / 支持 | 约束来自客户设计导入、平台认证、低功耗/低延迟指标、信号完整性和批量可靠性。 |



#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-02-26 | [LightCounting AI Capex Flows Down the Supply Chain to DSP Vendors](https://www.lightcounting.com/newsletter/en/ai-capex-flows-down-the-supply-chain-to-dsp-vendors-332) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | 约束来自客户设计导入、平台认证、低功耗/低延迟指标、信号完整性和批量可靠性。 | 未结构化 | 未结构化 |
| 2024-03-25 | [SemiAnalysis Nvidia Optical Boogeyman NVL72 Infiniband Scale Out 800G and 1.6T Ramp](https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | 约束来自客户设计导入、平台认证、低功耗/低延迟指标、信号完整性和批量可靠性。 | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2024-03-25 | 2026-02-26 | 单向覆盖，缺反证 |

### Q3 · 谁控制供给？

**结论强度：** 待验证  
**最近材料：** 2026-03-02

#### 基本理解思路

- **专业模型：** 份额 / 壁垒 / 替代 / 客户锁定模型
- **研究目的：** 判断稀缺供给是否被少数公司控制，并能转成利润池。
- **判断规则：** 控制权 = 份额集中度 + 资格/认证壁垒 + 技术/IP/生态壁垒 + 客户锁定 - 替代与多供速度。
- **理解提示：** 由本节点 playbook 提供。

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

Astera、Credo、Marvell、Broadcom、Arista 和 NVIDIA networking 控制不同子环节。

**支持机制：** 控制权可持续来自技术门槛、生态锁定、客户资格、长期协议、规模经验和不可替代交付能力。

**最大反证：** 若客户多供应商策略成功、替代技术成熟、标准化降低切换成本，控制权就会被稀释。

**对标的的影响：** 本问决定推荐应落到哪些具体公司。只有能控制合格供给、客户资格、生态或交付能力的公司，才可能把 高速连接与 AI 网络 的需求增长转成超额利润；份额分散或替代加速时，不应把整个节点的增长平均分配给所有玩家。

**关键来源：** [Marvell FY2026 Q3 10-Q](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-25-000197/mrvl-20251101.htm)；[Astera Labs Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1736297/000173629726000005/q425exhibit991.htm)；[Arista Q4 2025 results](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Networks-Inc--Reports-Fourth-Quarter-and-Year-End-2025-Financial-Results/default.aspx)；[Credo FY2026 Q3 results](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | Astera、Credo、Marvell、Broadcom、Arista 和 NVIDIA networking 控制不同子环节。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2025-12-03 | [Marvell FY2026 Q3 10-Q](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-25-000197/mrvl-20251101.htm) | 事实 / 支持 | Astera、Credo、Marvell、Broadcom、Arista 和 NVIDIA networking 控制不同子环节。 |
| 2026-02-10 | [Astera Labs Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1736297/000173629726000005/q425exhibit991.htm) | 事实 / 支持 | Astera、Credo、Marvell、Broadcom、Arista 和 NVIDIA networking 控制不同子环节。 |
| 2026-02-12 | [Arista Q4 2025 results](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Networks-Inc--Reports-Fourth-Quarter-and-Year-End-2025-Financial-Results/default.aspx) | 事实 / 支持 | Astera、Credo、Marvell、Broadcom、Arista 和 NVIDIA networking 控制不同子环节。 |
| 2026-03-02 | [Credo FY2026 Q3 results](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm) | 事实 / 支持 | Astera、Credo、Marvell、Broadcom、Arista 和 NVIDIA networking 控制不同子环节。 |



#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-03-02 | [Credo FY2026 Q3 results](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | Astera、Credo、Marvell、Broadcom、Arista 和 NVIDIA networking 控制不同子环节。 | 未结构化 | 未结构化 |
| 2026-02-12 | [Arista Q4 2025 results](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Networks-Inc--Reports-Fourth-Quarter-and-Year-End-2025-Financial-Results/default.aspx) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | Astera、Credo、Marvell、Broadcom、Arista 和 NVIDIA networking 控制不同子环节。 | 未结构化 | 未结构化 |
| 2026-02-10 | [Astera Labs Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1736297/000173629726000005/q425exhibit991.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | Astera、Credo、Marvell、Broadcom、Arista 和 NVIDIA networking 控制不同子环节。 | 未结构化 | 未结构化 |
| 2025-12-03 | [Marvell FY2026 Q3 10-Q](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-25-000197/mrvl-20251101.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | Astera、Credo、Marvell、Broadcom、Arista 和 NVIDIA networking 控制不同子环节。 | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 2025-12-03 | 2026-03-02 | 单向覆盖，缺反证 |

### Q4 · 是否已经财务兑现？

**结论强度：** 待验证  
**最近材料：** 2026-03-02

#### 基本理解思路

- **专业模型：** 收入 / 毛利 / backlog / 现金流模型
- **研究目的：** 判断产业逻辑是否已经进入公司财务，而不是停留在叙事或订单新闻。
- **判断规则：** 财务兑现 = 收入增长 + backlog/RPO 可见度 + 毛利/ASP 改善 + 经营现金流质量 - 库存/应收/取消风险。
- **理解提示：** 由本节点 playbook 提供。

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

ALAB、CRDO、MRVL、Arista 等公司收入已体现 AI networking / connectivity 需求。

**支持机制：** 财务兑现可持续需要 高速连接与 AI 网络 的收入、订单、backlog、毛利率和现金流沿同一方向改善。

**最大反证：** 若收入增长依赖低毛利订单、应收/库存上升或 backlog 转收入变慢，财务兑现质量会下降。

**对标的的影响：** 本问决定标的确定性。收入、毛利、backlog 和现金流已经兑现的公司可进入更高置信候选；只有订单新闻、没有利润和现金兑现的公司，需要降低推荐强度并提高监控频率。

**关键来源：** [Marvell FY2026 Q3 10-Q](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-25-000197/mrvl-20251101.htm)；[Astera Labs Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1736297/000173629726000005/q425exhibit991.htm)；[Arista Q4 2025 results](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Networks-Inc--Reports-Fourth-Quarter-and-Year-End-2025-Financial-Results/default.aspx)；[Credo FY2026 Q3 results](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | ALAB、CRDO、MRVL、Arista 等公司收入已体现 AI networking / connectivity 需求。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2025-12-03 | [Marvell FY2026 Q3 10-Q](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-25-000197/mrvl-20251101.htm) | 事实 / 支持 | ALAB、CRDO、MRVL、Arista 等公司收入已体现 AI networking / connectivity 需求。 |
| 2026-02-10 | [Astera Labs Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1736297/000173629726000005/q425exhibit991.htm) | 事实 / 支持 | ALAB、CRDO、MRVL、Arista 等公司收入已体现 AI networking / connectivity 需求。 |
| 2026-02-12 | [Arista Q4 2025 results](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Networks-Inc--Reports-Fourth-Quarter-and-Year-End-2025-Financial-Results/default.aspx) | 事实 / 支持 | ALAB、CRDO、MRVL、Arista 等公司收入已体现 AI networking / connectivity 需求。 |
| 2026-03-02 | [Credo FY2026 Q3 results](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm) | 事实 / 支持 | ALAB、CRDO、MRVL、Arista 等公司收入已体现 AI networking / connectivity 需求。 |



#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-03-02 | [Credo FY2026 Q3 results](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | ALAB、CRDO、MRVL、Arista 等公司收入已体现 AI networking / connectivity 需求。 | 未结构化 | 未结构化 |
| 2026-02-12 | [Arista Q4 2025 results](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Networks-Inc--Reports-Fourth-Quarter-and-Year-End-2025-Financial-Results/default.aspx) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | ALAB、CRDO、MRVL、Arista 等公司收入已体现 AI networking / connectivity 需求。 | 未结构化 | 未结构化 |
| 2026-02-10 | [Astera Labs Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1736297/000173629726000005/q425exhibit991.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | ALAB、CRDO、MRVL、Arista 等公司收入已体现 AI networking / connectivity 需求。 | 未结构化 | 未结构化 |
| 2025-12-03 | [Marvell FY2026 Q3 10-Q](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-25-000197/mrvl-20251101.htm) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | ALAB、CRDO、MRVL、Arista 等公司收入已体现 AI networking / connectivity 需求。 | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 2025-12-03 | 2026-03-02 | 单向覆盖，缺反证 |

### Q5 · 市场是否已定价？

**结论强度：** 待验证  
**最近材料：** 2026-03-02

#### 基本理解思路

- **专业模型：** 估值 / 预期差 / 盈利上修模型
- **研究目的：** 判断好产业是否仍是好赔率。
- **判断规则：** 赔率 = 未来盈利上修空间 ÷ 已定价增长与风险溢价；产业强度必须超过市场隐含预期才有推荐价值。
- **理解提示：** 由本节点 playbook 提供。

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

连接节点弹性大也容易估值透支，需要用客户集中、design win、gross margin 和出货节奏验证。

**支持机制：** 错价可持续来自市场低估增长持续期、盈利弹性、利润率上行或风险下降。

**最大反证：** 若估值已经把高增长、高毛利和低风险全部计入，基本面继续强也可能没有足够赔率。

**对标的的影响：** 本问直接决定 action state。即使 高速连接与 AI 网络 是正确节点，如果估值和盈利预期已经充分反映，推荐只能是 watch_only；只有基本面继续超预期且估值未完全定价，才可能进入 actionable_long。

**关键来源：** [Astera Labs Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1736297/000173629726000005/q425exhibit991.htm)；[Credo FY2026 Q3 results](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 连接节点弹性大也容易估值透支，需要用客户集中、design win、gross margin 和出货节奏验证。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2026-02-10 | [Astera Labs Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1736297/000173629726000005/q425exhibit991.htm) | 估值 / 支持 | 连接节点弹性大也容易估值透支，需要用客户集中、design win、gross margin 和出货节奏验证。 |
| 2026-03-02 | [Credo FY2026 Q3 results](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm) | 估值 / 支持 | 连接节点弹性大也容易估值透支，需要用客户集中、design win、gross margin 和出货节奏验证。 |



#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-03-02 | [Credo FY2026 Q3 results](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 材料发现 | 连接节点弹性大也容易估值透支，需要用客户集中、design win、gross margin 和出货节奏验证。 | 未结构化 | 未结构化 |
| 2026-02-10 | [Astera Labs Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1736297/000173629726000005/q425exhibit991.htm) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 材料发现 | 连接节点弹性大也容易估值透支，需要用客户集中、design win、gross margin 和出货节奏验证。 | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 2 | 0 | 2 | 0 | 2026-02-10 | 2026-03-02 | 有材料，结构不完整 |

### Q6 · 反证是什么？

**结论强度：** 待验证  
**最近材料：** 2025-07-15

#### 基本理解思路

- **专业模型：** 触发器 / 阈值 / 降级动作模型
- **研究目的：** 把反证从泛泛风险变成可监控的降级纪律。
- **判断规则：** 反证强度 = 领先触发器变化 × 对需求/供给/控制权/财务/定价链条的破坏程度 × 可持续性。
- **理解提示：** 由本节点 playbook 提供。

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

平台自研替代、客户设计切换、ASP 下行、CPO/LPO/AEC 路线变化、主要客户延迟 ramp。

**支持机制：** 有效反证应比财报恶化更早出现：价格、交期、订单、客户预算、供给释放或替代路线先发生变化。

**最大反证：** 如果反证指标连续出现并穿透到收入、毛利、现金流或估值预期，应从观察名单降级。

**对标的的影响：** 本问定义推荐纪律。高速连接与 AI 网络 相关标的必须绑定可观察降级触发器；当需求、供给、控制权、财务兑现或定价任一核心反证触发时，推荐强度应自动下调，而不是事后解释。

**关键来源：** [SemiAnalysis Nvidia Optical Boogeyman NVL72 Infiniband Scale Out 800G and 1.6T Ramp](https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband)；[Dell'Oro Group Ethernet AI Backend Network Forecast](https://www.prnewswire.com/news-releases/ethernet-is-winning-the-war-against-infiniband-in-ai-back-end-networks-according-to-delloro-group-302501890.html)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 平台自研替代、客户设计切换、ASP 下行、CPO/LPO/AEC 路线变化、主要客户延迟 ramp。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2024-03-25 | [SemiAnalysis Nvidia Optical Boogeyman NVL72 Infiniband Scale Out 800G and 1.6T Ramp](https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband) | 反证 / 反证 | 平台自研替代、客户设计切换、ASP 下行、CPO/LPO/AEC 路线变化、主要客户延迟 ramp。 |
| 2025-07-15 | [Dell'Oro Group Ethernet AI Backend Network Forecast](https://www.prnewswire.com/news-releases/ethernet-is-winning-the-war-against-infiniband-in-ai-back-end-networks-according-to-delloro-group-302501890.html) | 反证 / 反证 | 平台自研替代、客户设计切换、ASP 下行、CPO/LPO/AEC 路线变化、主要客户延迟 ramp。 |



#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-07-15 | [Dell'Oro Group Ethernet AI Backend Network Forecast](https://www.prnewswire.com/news-releases/ethernet-is-winning-the-war-against-infiniband-in-ai-back-end-networks-according-to-delloro-group-302501890.html) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 材料发现 | 平台自研替代、客户设计切换、ASP 下行、CPO/LPO/AEC 路线变化、主要客户延迟 ramp。 | 未结构化 | 未结构化 |
| 2024-03-25 | [SemiAnalysis Nvidia Optical Boogeyman NVL72 Infiniband Scale Out 800G and 1.6T Ramp](https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 材料发现 | 平台自研替代、客户设计切换、ASP 下行、CPO/LPO/AEC 路线变化、主要客户延迟 ramp。 | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 | 2024-03-25 | 2025-07-15 | 有材料，结构不完整 |

### S 曲线汇总

当前节点的产业逻辑已形成，但仍有 6 个问题未达到高置信。特别是市场定价未闭环时，不能把产业胜率直接写成证券买入赔率。

## 3. 标的推荐

以下只保留映射到当前 BOM 的标的。产业逻辑强不等于证券价格便宜。

| 标的 | 公司 | BOM 节点 | 候选状态 | 最终状态 | 核心理由 | 未来空间 / 赔率 | 主要风险 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ALAB | Astera Labs | 高速连接与 AI 网络 | watch_only | no_action | 机柜级连接收入高增，直接受益 rack-scale AI。 | 1.5 | 大客户订单延后、平台自研替代、估值压缩。 |
| CRDO | Credo | 高速连接与 AI 网络 | watch_only | no_action | AEC/光互联需求强，收入高弹性。 | 1.5 | 客户订单延迟、价格下行、毛利不达预期。 |
| MRVL | Marvell Technology | custom silicon / 电光互联 | watch_only | no_action | custom products 与 electro-optics 已进入 AI data-center 收入口径。 | 1.5 | 大客户项目延期、客户自研替代、毛利不达预期。 |

## 4. 来源索引

| ID | 来源 | 类别 | 市场可见时间 | 用途摘要 |
| --- | --- | --- | --- | --- |
| SRC-ALAB-Q4-2025 | [Astera Labs Q4 2025 results](https://www.sec.gov/Archives/edgar/data/1736297/000173629726000005/q425exhibit991.htm) | evidence | 2026-02-10 | Astera Labs Q4 revenue was $270.6M, +92% YoY, tied to rack-scale AI infrastructure connectivity. |
| SRC-CRDO-FY26-Q3 | [Credo FY2026 Q3 results](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm) | evidence | 2026-03-02 | Credo FY26 Q3 revenue was $407.0M, +200% YoY, with active electrical cables, optical interconnects and memory connectivity tied to AI infrastructure. |
| SRC-MRVL-FY26-Q3 | [Marvell FY2026 Q3 10-Q](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-25-000197/mrvl-20251101.htm) | evidence | 2025-12-03 | Marvell FY26 Q3 net revenue was $2.075B; data-center sales increased 38% year over year, driven by AI-related demand for custom products and electro-optics. |
| SRC-ANET-Q4-2025 | [Arista Q4 2025 results](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Networks-Inc--Reports-Fourth-Quarter-and-Year-End-2025-Financial-Results/default.aspx) | evidence | 2026-02-12 | Arista FY2025 revenue was $9.006B, +28.6%, and management said it exceeded AI networking and campus expansion goals. |
| SRC-SA-OPTICAL-2024 | [SemiAnalysis Nvidia Optical Boogeyman NVL72 Infiniband Scale Out 800G and 1.6T Ramp](https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband) | research_report | 2024-03-25 | SemiAnalysis linked Blackwell NVL72 system architecture, NVLink scale-up, InfiniBand scale-out, 800G and 1.6T ramps to optical and networking BOM expansion. |
| SRC-LC-AI-OPTICS-202501 | [LightCounting Optics for AI Clusters](https://www.lightcounting.com/newsletter/en/january-2025-optics-for-ai-clusters-319) | research_report | 2025-01-01 | LightCounting estimated AI-cluster optical transceiver, LPO and CPO demand rising from about $5B in 2024 to more than $10B in 2026, with scale-up and scale-out models through 2030. |
| SRC-LC-PAM4-DSP-20260226 | [LightCounting AI Capex Flows Down the Supply Chain to DSP Vendors](https://www.lightcounting.com/newsletter/en/ai-capex-flows-down-the-supply-chain-to-dsp-vendors-332) | research_report | 2026-02-26 | LightCounting reported AI infrastructure capex drove 800G PAM4 chipset shipments to nearly triple in 2025 and expected 800G shipments to more than double in 2026, with 1.6T ports ramping from a small base. |
| SRC-DO-AI-NETWORKS-20250715 | [Dell'Oro Group Ethernet AI Backend Network Forecast](https://www.prnewswire.com/news-releases/ethernet-is-winning-the-war-against-infiniband-in-ai-back-end-networks-according-to-delloro-group-302501890.html) | research_report | 2025-07-15 | Dell'Oro Group forecast AI back-end networks could drive nearly $80B of data-center switch sales over five years and expected Ethernet to gain share from InfiniBand in AI back-end networks. |
