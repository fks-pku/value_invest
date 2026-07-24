---
report_scope: standalone-bom
bom_node_id: gpu_asic
as_of_date: 2026-07-24
---

# GPU / ASIC BOM 实时跟踪

> 研究截面：2026-07-24。时间线按材料发布时间由近及远；同一材料只有经过当前问题的独立解析和复核后，才进入该问题。

## 1. 需求侧

### 简单逻辑链

需求成立不能只看 AI 话题热度，而要看到同一条传导链逐步兑现：真实训练和推理 工作负载增加，促使云厂商扩大可用算力和资本开支，继而形成 GPU/ASIC 与 AI 服务器订单，最终进入芯片公司的收入、利润和下一期指引。若只有市场规模预测而 没有订单和财务兑现，需求仍停留在主题阶段；若收入、订单与客户资本开支同时 增长，才属于投资可用需求。

### 信息时间线

| 时间 | 信息类型 | Source | 观点列表 |
|---|---|---|---|
| 2026-03-05 | 官方财报 | [Broadcom FY2026 Q1 业绩](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial) | <ul><li>新闻稿开头财务摘要及 CEO 引述：Q1 AI 收入为 84 亿美元，同比增长 106%，高于公司原预测；Q2 AI 半导体收入指引约 107 亿美元。定制 ASIC 和 AI 网络收入仍在加速，说明需求已从 NVIDIA 单一路线扩展到云厂商定制芯片。</li></ul> |
| 2026-02-26 | 官方财报 | [Dell FY2026 Q4 业绩](https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-3) | <ul><li>`AI-optimized servers` 订单、出货和 FY2027 指引段落：FY2026 AI 优化服务器订单超过 640 亿美元、出货超过 250 亿美元，期末 backlog 为 430 亿美元；FY2027 AI 服务器收入指引约 500 亿美元，同比增长 103%。这把芯片需求进一步验证为系统订单和未来交付。</li></ul> |
| 2026-02-25 | 官方财报 | [NVIDIA FY2026 Q4 业绩](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/) | <ul><li>`Q4 and Fiscal 2026 Summary`、`Outlook`、`Data Center`：Q4 总收入 681 亿美元，同比增长 73%；数据中心收入 623 亿美元，同比增长 75%；FY2026 数据中心收入 1,937 亿美元，同比增长 68%。Q1 FY2027 总收入指引 780 亿美元，且未计入中国数据中心计算收入，显示主需求仍可支撑环比增长。</li></ul> |
| 2026-02-05 | 官方财报 | [Amazon 2025 Q4 业绩](https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Fourth-Quarter-Results/default.aspx) | <ul><li>管理层关于 AWS、芯片业务与 2026 资本开支的说明：AWS Q4 销售额增至 356 亿美元；管理层称自研芯片业务同比三位数增长，并预计 2026 年全公司资本开支约 2,000 亿美元，主要投向 AI、芯片、机器人和卫星。GPU 与 ASIC 两条采购路线都获得客户预算支持。</li></ul> |
| 2026-02-04 | 官方财报 | [Alphabet 2025 Q4 业绩](https://s206.q4cdn.com/479360582/files/doc_news/2026/Feb/04/attachments/2025q4-alphabet-earnings-release.pdf) | <ul><li>第 2 页财务摘要及 `Capital expenditures`；[业绩电话会](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx)，Cloud backlog 与 Gemini 使用量段落：Google Cloud Q4 收入 177 亿美元，同比增长 48%，Cloud 年化收入超过 700 亿美元；Cloud backlog 达 2,400 亿美元，环比增长 55%。公司预计 2026 年资本开支 1,750 亿至 1,850 亿美元，用于满足客户需求。</li></ul> |
| 2026-01-28 | 官方财报 | [Microsoft FY2026 Q2 业绩](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q2/press-release-webcast) | <ul><li>`Performance` 与 segment highlights；[电话会](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q2.aspx)，CFO 关于 capex 的说明：Microsoft Cloud 收入 515 亿美元，同比增长 26%；商业 RPO 增长 110% 至 6,250 亿美元，Azure 收入增长 39%。当季资本开支 375 亿美元，其中约三分之二用于 GPU、CPU 等短期资产，管理层仍称客户需求超过供给。</li></ul> |
| 2026-01-15 | 官方公司 | [TSMC 2025 Q4 电话会记录](https://investor.tsmc.com/chinese/encrypt/files/encrypt_file/reports/2026-01/51d09df96cd89ac19d65af39032b038dc2896a24/TSMC%204Q25%20Transcript.pdf) | <ul><li>第 4-5 页 `AI demand and long-term outlook`：AI 加速器相关收入已占 2025 年收入的高十几百分比；TSMC 预计 2024-2029 年该口径收入复合增速为中高 50%，并称已向客户及其客户核验长期算力需求。该口径与终端芯片市场规模不同，但支持先进制造需求继续高速增长。</li></ul> |
| 2025-08-28 | 第三方权威 | [Omdia AI 数据中心芯片预测](https://omdia.tech.informa.com/pr/2025/aug/ai-data-center-chip-market-to-hit-286bn-growth-likely-peaking-as-custom-asics-gain-ground) | <ul><li>市场规模预测及 vendor mix 段落：Omdia 估计 AI 数据中心芯片支出从 2024 年约 1,230 亿美元增至 2025 年约 2,070 亿美元，但到 2030 年仅约 2,860 亿美元，同时定制 ASIC 份额上升。按该口径，2025-2030 年隐含复合增速约 6.7%，是对“长期仍维持当前爆发速度”的重要反证。</li></ul> |
| 2023-08-23 | 官方财报 | [NVIDIA FY2024 Q2 业绩](https://investor.nvidia.com/news/press-release-details/2023/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2024/) | <ul><li>`Data Center`：数据中心季度收入首次跃升至 103.2 亿美元，环比增长 141%、同比增长 171%。这是生成式 AI 需求从叙事进入 GPU 厂商财务报表的早期拐点，可与 2026 年的 623 亿美元季度规模形成同公司、同分部的历史对照。</li></ul> |

### 最新结论与趋势

截至截面日，GPU/ASIC 需求已经完成“资本开支、系统订单、芯片收入”三重验证， 不能再被视为只有远期 TAM 的主题。NVIDIA 数据中心季度收入从 2023 年中期的 103 亿美元升至 2026 年初的 623 亿美元，Dell 仍有 430 亿美元 AI 服务器 backlog，Broadcom 的 AI 收入和下一季指引又证明定制 ASIC 正在接棒扩散。

趋势上需要把“需求仍增长”和“增速永不下降”分开。TSMC 从先进制造口径看到 2024-2029 年中高 50% 的 AI 加速器收入复合增速，而 Omdia 从终端芯片支出口径 预计 2025 年后增长明显放缓。两者并不直接矛盾：前者可能包含先进节点价值量和 份额提升，后者强调终端总额基数变大。当前结论是 **需求强、仍在扩张，但市场已 从单一 GPU 爆发期进入 GPU 与定制 ASIC 并行、增速逐步分化的阶段**。

**趋势变化：** 历史截面迁移为实时跟踪基线。

## 2. 供给侧

### 简单逻辑链

GPU/ASIC 的有效供给不是“有多少晶圆”这么简单，而是先进制程晶圆、HBM、先进 封装、基板、测试和系统组装同时合格后的最小值。供给紧张时，长期交期、不可取消 订单、预付款和容量承诺会上升；但这些承诺也会在需求判断错误时转化为库存和毛利 风险。因此既要识别物理瓶颈，也要判断扩产速度是否正在消除稀缺。

### 信息时间线

| 时间 | 信息类型 | Source | 观点列表 |
|---|---|---|---|
| 2026-02-25 | 官方财报 | [NVIDIA FY2026 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) | <ul><li>Item 1A `Risks Related to Demand, Supply, and Manufacturing`：公司披露部分供应交期曾超过 12 个月；在增长期会提前下不可取消订单、支付溢价或预付款以锁定产能。长交期证明供给并非即时可得，也意味着需求回落时存在采购承诺反噬。</li><li>Item 1 `Manufacturing`：NVIDIA 采用 fabless 模式，晶圆主要依赖 TSMC 和 Samsung，内存来自 SK hynix、Micron、Samsung，使用 CoWoS 封装，并依赖鸿海、纬创、Fabrinet 等组装测试。GPU 供给实际受多个外部环节共同约束。</li><li>合并资产负债表附注与 `Commitments`：期末库存为 214 亿美元，库存采购及长期供应/产能义务为 952 亿美元。该规模说明 NVIDIA 正以资产负债表主动换取未来供给，但也把供需判断错误的成本显著放大。</li></ul> |
| 2026-01-15 | 官方公司 | [TSMC 2025 Q4 电话会记录](https://investor.tsmc.com/chinese/encrypt/files/encrypt_file/reports/2026-01/51d09df96cd89ac19d65af39032b038dc2896a24/TSMC%204Q25%20Transcript.pdf) | <ul><li>第 3 页 `2026 capital budget`，第 4-7 页 AI 需求与问答：TSMC 预计 2026 年资本预算 520 亿至 560 亿美元，其中 70%-80% 用于先进制程、10%-20% 用于先进封装测试等；AI 客户讨论的产能前置期已延长至 2-3 年。供给正在大幅扩张，但新增产能并非短期到位。</li></ul> |
| 2025-12-18 | 官方财报 | [Broadcom FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1730168/000173016825000121/avgo-20251102.htm) | <ul><li>Item 1 `Manufacturing` 与 Item 1A supplier risks：Broadcom 将大部分前道制造外包给 TSMC，封装测试依赖 TSMC、ASE、Foxconn、Amkor 和 SPIL；部分器件因设计与认证周期不能快速替换。定制 ASIC 的供给同样受先进制造与认证约束，并非云厂商有设计就能立即扩量。</li></ul> |
| 2025-10-31 | 第三方权威 | [TrendForce HBM Industry Analysis 4Q25](https://www.trendforce.com/research/download/RP251029MY) | <ul><li>supplier capacity、yield、qualification 章节：TrendForce 指出 HBM 的 TSV 产能、良率、客户认证和后段产能仍限制近期供给，三家主要供应商计划在 2026 年量产 HBM4。对 GPU/ASIC 节点而言，HBM 是必须同步取得的输入，而不是可事后补配的普通元件。</li></ul> |
| 2024-07-17 | 第三方权威 | [SemiAnalysis GB200 架构与 BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | <ul><li>`Hardware Architecture` 与 `Component Supply Chain & BOM`：GB200 从单卡升级为高密度机架系统，牵涉 HBM、CoWoS、NVLink、基板、供电和液冷等协同。其意义是有效供给单位从“芯片颗数”变成“可交付并运行的系统”，任何一个组件不足都会推迟 GPU 收入确认。</li></ul> |

### 最新结论与趋势

当前 GPU/ASIC 供给仍有约束，但约束已经从最初的“拿不到先进晶圆”演化为 **先进晶圆、HBM、CoWoS、基板和整机交付的组合瓶颈**。NVIDIA 披露超过 12 个月的交期和 952 亿美元供应/产能义务，TSMC 又把客户产能讨论提前到 2-3 年， 说明真正合格的供应链仍难以即时复制。

另一方面，TSMC 以 520 亿至 560 亿美元资本开支扩张先进制程和封装，三大内存 厂也在推进 HBM4，供给不是永久固定。最重要的趋势是：**短期稀缺性仍在，但 2026 年以后要从“是否缺货”转向“扩产是否快于需求、预付承诺是否变成库存”**。 NVIDIA 214 亿美元库存和 952 亿美元承诺既是供应控制力，也是周期反转时的主要 风险暴露。

**趋势变化：** 历史截面迁移为实时跟踪基线。

## 3. 技术侧

### 简单逻辑链

技术判断不应只比较芯片峰值 FLOPS，而要按工作负载比较端到端结果：模型变化 速度、训练与推理占比、吞吐/延迟、性能功耗比、每 token 成本、软件迁移成本和 集群利用率。GPU 依靠通用性与软件生态适合快速变化的任务；定制 ASIC 依靠软硬 件协同，在规模大且稳定的工作负载上追求更低 TCO。最终竞争单位正从单颗芯片 转向机架、互连、编译器和推理调度组成的平台。

### 信息时间线

| 时间 | 信息类型 | Source | 观点列表 |
|---|---|---|---|
| 2026-03-16 | 官方公司 | [NVIDIA Vera Rubin 平台](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform) | <ul><li>`News Summary` 与性能比较段落：Rubin 以 GPU、CPU、NVLink、网卡、DPU 和交换机组成机架级平台；公司称相对 Blackwell 可实现最高 10 倍每瓦吞吐、约十分之一 token 成本，并以更少 GPU 运行 MoE 模型。竞争指标已明确转向系统吞吐、功耗和 token 成本。</li></ul> |
| 2026-03-16 | 官方公司 | [NVIDIA Dynamo 1.0](https://nvidianews.nvidia.com/news/dynamo-1-0) | <ul><li>产品说明与 benchmark 段落：NVIDIA 将 Dynamo 作为开源生产级推理编排软件，称可把 Blackwell 推理性能提高最高 7 倍。即使硬件不变，调度、分离式服务和资源利用率也能显著改变有效算力供给，软件栈继续构成平台壁垒。</li></ul> |
| 2026-02-25 | 官方财报 | [NVIDIA FY2026 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) | <ul><li>Item 1 `Competition`：NVIDIA 把竞争变量定义为性能、产品广度、客户渠道、软件支持、标准 API、制造能力、芯片价格和总系统成本；并明确把 AMD、Huawei、Intel 及 Alphabet、Amazon、Microsoft 等云厂商内部芯片列为竞争者。竞争边界已经是平台与 TCO，而非单纯 GPU 对 GPU。</li></ul> |
| 2026-02-03 | 官方财报 | [AMD 2025 Q4 业绩](https://ir.amd.com/news-events/press-releases/detail/1276/amd-reports-fourth-quarter-and-full-year-2025-financial-results) | <ul><li>`Segment Summary` 与产品进展：AMD 数据中心季度收入 54 亿美元，同比增长 39%，由 EPYC 和 Instinct GPU 拉动；公司展示 Helios 机架级路线。AMD 已形成可财务验证的第二 GPU 路线，但披露口径混合 CPU 与 GPU，不能据此直接推导 GPU 份额。</li></ul> |
| 2025-11-06 | 官方公司 | [Google Ironwood TPU 协同设计栈](https://cloud.google.com/blog/products/compute/inside-the-ironwood-tpu-codesigned-ai-stack/) | <ul><li>`Performance and efficiency`、软件栈段落：Google 称 Ironwood 的性能功耗比为上一代 Trillium 的 2 倍、相对 2018 年首代 Cloud TPU 近 30 倍，并通过 JAX、PyTorch 和编译器协同优化。它证明定制 ASIC 在可控工作负载上可凭软硬件一体化争夺 TCO。</li></ul> |
| 2025-08-28 | 第三方权威 | [Omdia AI 数据中心芯片预测](https://omdia.tech.informa.com/pr/2025/aug/ai-data-center-chip-market-to-hit-286bn-growth-likely-peaking-as-custom-asics-gain-ground) | <ul><li>vendor outlook：Omdia 判断 NVIDIA 仍是主导厂商，但 Google TPU、Huawei Ascend 及其他定制 ASIC/ASSP 正在获得采用。技术趋势不是 ASIC 立即替代 GPU，而是随着推理和稳定工作负载扩大，市场结构从单一路线走向分层。</li></ul> |
| 2024-12-11 | 第三方权威 | [Omdia：Google TPU 需求加速](https://omdia.tech.informa.com/pr/2024/dec/omdia-demand-for-googles-tpu-chips-accelerates-challenging-nvidias-dominance) | <ul><li>TPU value estimate 与竞争判断：Omdia 估计 Google TPU 的芯片价值约 60 亿至 90 亿美元，已经足以构成对 NVIDIA 的可见份额侵蚀。定制 ASIC 不再只是内部实验，而是达到可改变供应商收入池的规模。</li></ul> |
| 2024-03-18 | 官方公司 | [NVIDIA GTC 2024 生态资料](https://images.nvidia.com/nvimages/gtc/pdf/gtc24-spring-best-of-highlight.pdf) | <ul><li>CUDA ecosystem highlights：NVIDIA 当时披露 CUDA 接近 500 万开发者、4 万多家公司、3,300 多个 GPU 加速应用和 1,600 多家生成式 AI 公司。该生态规模解释了 GPU 在模型快速变化和多客户场景中的迁移成本优势。</li></ul> |

### 最新结论与趋势

技术格局不是“GPU 或 ASIC 二选一”。GPU 仍在前沿训练、快速变化模型、跨客户 通用云服务中占据优势，原因不只在芯片性能，还在 CUDA、系统互连、推理调度和 开发者生态。与此同时，Google TPU 的规模、Ironwood 的性能功耗比以及 Broadcom 定制 ASIC 收入证明：当工作负载足够稳定、规模足够大、客户能控制软硬件栈时， ASIC 可以用更低 TCO 换取份额。

最新趋势是 **竞争单位由芯片转为完整机架与软件平台，市场由单一 GPU 主导转为 按工作负载分层共存**。Rubin 和 Dynamo 表明 NVIDIA 正用系统协同抵消 ASIC 的 效率优势；Google 则用自研芯片、编译器和云平台缩小通用生态差距。未来需要观察 的不是某个峰值算力数字，而是实际利用率、每 token 成本、部署速度及外部客户 采用范围。

**趋势变化：** 历史截面迁移为实时跟踪基线。

## 4. 估值侧

### 简单逻辑链

估值要把产业增长与证券赔率分开。先在同一截面固定股价，再选择可解释的盈利 口径，计算当前倍数或机构隐含假设，并比较不同机构对未来收入、利润和目标价的 分歧。高增长只有在未来盈利上修快于估值扩张时才创造赔率；若公司大幅超预期后 股价仍下跌，通常意味着市场已提前计入很高的增长门槛。

### 信息时间线

| 时间 | 信息类型 | Source | 观点列表 |
|---|---|---|---|
| 2026-03-27 | 第三方权威 | [NVDA 历史行情](https://www.financecharts.com/stocks/NVDA/summary/price) | <ul><li>、[AVGO 历史行情](https://markets.financialcontent.com/stocks/quote/historical?Symbol=AVGO)、[AMD 历史行情](https://markets.financialcontent.com/stocks/quote/historical?Symbol=amd)，2026-03-27 日线：截面前最后收盘价分别为 NVDA 167.52 美元、AVGO 300.68 美元、AMD 201.99 美元。结合已披露 FY2026 GAAP EPS 4.90 美元，NVDA 静态 GAAP PE 约 34.2 倍；结合 AMD 2025 GAAP/Non-GAAP EPS 2.65/4.17 美元，AMD 对应约 76.2/48.4 倍。</li></ul> |
| 2026-03-18 | 研报 | [Morningstar NVIDIA 报告](https://www.morningstar.com/company-reports/1461841-nvidia-raising-fair-value-to-260-from-240-as-agentic-ai-drives-a-1-trillion-forecast-at-gtc) | <ul><li>标题及 fair-value summary：Morningstar 将 NVIDIA 公允价值从 240 美元上调至 260 美元，依据包括 GTC 后对 2025-2027 年 Blackwell/Rubin 累计收入路径和近期预测的提高，但同时假定长期增速回落。相对 167.52 美元截面价，表面上约有 55% 空间，核心敏感项仍是长期增长折现。</li></ul> |
| 2026-03-17 | 市场消息 | [Morgan Stanley NVIDIA 评级摘要](https://www.investing.com/news/analyst-ratings/morgan-stanley-reiterates-overweight-on-nvidia-stock-260-target-93CH-4565172) | <ul><li>评级与目标价段落：Morgan Stanley 维持 Overweight 和 260 美元目标价，并提到多位分析师上调近期盈利预期。它与 Morningstar 给出相同目标价，但这是目标价共识，不是对尾部风险的独立验证。</li></ul> |
| 2026-03-09 | 研报 | [交银国际 Morning Express](https://files.bocomgroup.com/download/mexp-260309e.pdf) | <ul><li>第 1 页 `Broadcom Inc.`：报告维持 Broadcom 买入和 460 美元目标价；当时股价 332.77 美元、隐含空间 38.2%。报告预计 FY2026E/27E/28E AI 芯片收入约 587/1,098/1,535 亿美元，Non-GAAP EPS 约 11.47/17.82/23.52 美元。按 2026-03-27 股价和 FY2026E EPS，前瞻 PE 约 26.2 倍，但估值高度依赖定制 ASIC 收入如期放量。</li></ul> |
| 2026-03-02 | 市场消息 | [UBS AMD 评级摘要](https://www.investing.com/news/analyst-ratings/ubs-reiterates-buy-rating-on-amd-stock-on-data-center-growth-93CH-4534296) | <ul><li>评级与目标价段落：UBS 维持 AMD 买入和 310 美元目标价，主要押注数据中心增长与 AI 加速器放量。相对 201.99 美元截面价隐含约 53% 空间。</li></ul> |
| 2026-02-26 | 市场消息 | [Kiplinger：NVIDIA 财报后市场反应](https://www.kiplinger.com/investing/stocks/big-nvidia-numbers-take-down-the-nasdaq-stock-market-today) | <ul><li>NVIDIA earnings reaction：NVIDIA 在公布 73% 的收入增长和更高下一季指引后，股价仍下跌约 5.5%，市值减少约 2,600 亿美元。强财务数据未带来正回报，说明短期市场门槛已不只是“继续增长”，而是持续超越极高预期。</li></ul> |
| 2026-02-25 | 官方财报 | [NVIDIA FY2026 Q4 业绩](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/) | <ul><li>FY2026 summary：NVIDIA FY2026 收入 2,159 亿美元，同比增长 65%；GAAP 净利润 1,201 亿美元、EPS 4.90 美元，GAAP 毛利率 71.1%。NVDA 的估值有已实现利润支撑，而不是只依赖远期故事，但毛利率已从 FY2025 的 75.0% 回落。</li></ul> |
| 2026-02-04 | 市场消息 | [Goldman Sachs AMD 评级摘要](https://uk.investing.com/news/analyst-ratings/goldman-sachs-reiterates-neutral-rating-on-amd-stock-with-210-price-target-93CH-4487179) | <ul><li>估值与风险段落：Goldman Sachs 对 AMD 维持 Neutral、目标价 210 美元，理由包括相对同业的估值溢价和更高运营费用。与 UBS 的 310 美元目标价形成明显分歧，表明 AMD 的赔率主要取决于尚未完全兑现的 AI GPU 份额和利润率。</li></ul> |
| 2026-02-03 | 官方财报 | [AMD 2025 Q4 业绩](https://ir.amd.com/news-events/press-releases/detail/1276/amd-reports-fourth-quarter-and-full-year-2025-financial-results) | <ul><li>年度 GAAP 与 Non-GAAP 表格：AMD 2025 年收入 346 亿美元，同比增长 34%；GAAP EPS 2.65 美元、Non-GAAP EPS 4.17 美元。数据中心收入增长 32%，但分部同时包含 EPYC CPU 和 Instinct GPU，因此不能把全部数据中心增长视作纯 GPU 盈利。</li></ul> |

### 最新结论与趋势

截面估值不是简单的“AI 都贵”。NVDA 约 34 倍静态 GAAP PE，盈利基础最扎实， Morningstar 与 Morgan Stanley 均给出 260 美元估值/目标价；AVGO 按交银国际 FY2026E Non-GAAP EPS 约 26 倍，赔率取决于 2027-2028 年定制 ASIC 收入是否 按极高预测兑现；AMD 的静态 GAAP/Non-GAAP PE 约 76/48 倍，且机构目标价从 210 到 310 美元分歧最大，执行敏感度最高。

因此当前排序应是 **NVDA 的盈利确定性最高，AVGO 的盈利弹性最大但客户与项目 集中，AMD 的潜在份额上行最大但估值对兑现速度最敏感**。同时，NVIDIA 在大幅 超预期后仍下跌，说明整个板块已经进入“必须持续上修盈利才能消化估值”的阶段。 这份截面证据支持继续研究，不足以把任一标的直接升级为无条件买入。

**趋势变化：** 历史截面迁移为实时跟踪基线。

## 5. ESG

### 简单逻辑链

GPU/ASIC 的 ESG 不是附属评分，而是会直接改变可交付算力、可服务市场、成本和 估值的约束。性能功耗比改善决定单位算力的资源效率，但绝对工作负载增长可能让 总用电继续上升；出口管制会缩小市场并形成库存损失；供应与客户集中度影响经营 韧性；对客户、初创公司和基础设施的大额投资或担保则会改变治理透明度与资本 配置风险。

### 信息时间线

| 时间 | 信息类型 | Source | 观点列表 |
|---|---|---|---|
| 2026-02-25 | 官方财报 | [NVIDIA FY2026 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) | <ul><li>Item 1 `Government Regulations` 与 Item 1A export-control risks：NVIDIA 称截至 FY2026 末已被实质排除在中国数据中心计算市场之外；H20 出口许可变化造成 45 亿美元库存及采购义务费用。政策约束已直接进入收入机会、库存和毛利，而不是抽象地缘风险。</li><li>客户集中披露及 MD&A investment/guarantee 段落：FY2026 两个直接客户分别占收入 22% 和 14%；公司还向私营公司和基础设施基金投资 175 亿美元，并对早期企业的土地、电力和机房壳体义务提供 35 亿美元担保。客户集中与生态融资提高了需求可见性，也带来关联性、流动性和资本配置风险。</li></ul> |
| 2026-02-04 | 官方财报 | [AMD FY2025 10-K](https://ir.amd.com/financial-information/sec-filings/content/0000002488-26-000018/amd-20251227.htm) | <ul><li>Data Center MD&A 与 export-control charges：美国对 MI308 的出口管制导致 AMD 2025 年约 4.4 亿美元净库存及相关费用。AMD 与 NVIDIA 同时出现政策驱动的真实损益，说明可服务市场和产品重设计风险是 GPU 厂商共同约束。</li></ul> |
| 2025-06-12 | 官方公司 | [AMD 30x25 与 2030 能效目标](https://www.amd.com/en/blogs/2025/amd-surpasses-30x25-goal-sets-ambitious-new-20x-rack-scale-energy-efficiency-target-for-ai-systems-by-2030.html) | <ul><li>`At a Glance`、`Surpassing 30x25`、`A New Goal`：AMD 称相对 2020 基准已实现节点级能效提高 38 倍，同等性能耗电下降 97%；并计划 2024-2030 年机架级训练/推理能效再提高 20 倍。该数据由公司定义工作负载和配置，应视为路线目标，而非行业实测均值。</li></ul> |
| 2025-04-10 | 第三方权威 | [IEA《Energy and AI》执行摘要](https://www.iea.org/reports/energy-and-ai/executive-summary) | <ul><li>`Data centres account for...`、2030 electricity projection、grid delays：2024 年全球数据中心耗电约 415 TWh，占全球用电 1.5%；IEA 预计 2030 年增至约 945 TWh，AI 是主要驱动。约 20% 规划中数据中心项目可能因电网问题延迟，表明芯片能效提高仍可能被总算力扩张抵消，电力接入会反过来限制 GPU/ASIC 交付。</li></ul> |

### 最新结论与趋势

环境、监管和治理仍直接约束 GPU/ASIC 的可交付算力与可服务市场：绝对用电增长可能抵消芯片能效提升，出口管制会形成库存和收入损失，客户集中及前置采购承诺会放大周期反转风险。本轮优先解析的研报没有提供足以替代现有基线的新定量 ESG 数据，因此不人为制造趋势变化；后续扫描应继续优先提取电力接入、出口许可、客户集中度和供应承诺的新增数字。

**趋势变化：** 本轮没有经原文核验的新定量 ESG 变化，维持原结论。
