---
report_scope: standalone-bom
bom_node_id: gpu_asic
as_of_date: 2026-08-04
investment_engine_version: 2.2
---

# GPU / ASIC BOM 实时跟踪

> 研究截面：2026-08-04。时间线按材料发布时间由近及远；同一材料只有经过当前问题的独立解析和复核后，才进入该问题。

### 当前投资判断

**动作状态：** watch_only

Q2新增6份机构研报和6条原子观点，并把信息矩阵扩展到30行。新增材料补强Hyperscaler单位GW情景、Amazon资本开支、Naver AIDC功率、美国数据中心总功率、token活动和Broadcom ASIC/网络收入代理；但它们仍是情景、预测或样本，不能替代官方GPU/ASIC交付、利用率及公司利润桥，维持观察。

| 基本面变化 | 市场共识变化 | 定价变化 |
|---|---|---|
| 相较8月3日，Q2增加6份7月27日机构研报和6条信息。互联网平台与Hyperscaler代理更丰富，其它分类从2类扩为5类；没有新增可直接相加的官方已安装GPU，因此需求数量状态不变。 | 投行对AI基础设施扩张、数据中心功率和定制ASIC收入的方向性预期继续上修，但分歧集中在融资、实际交付、利用率、GPU与ASIC份额及资本回报。 | 本轮没有新增证券价格、一致预期或反向估值；Amazon资本开支、Broadcom收入预测和Naver AIDC规划均不能直接证明证券错价。 |

**研究覆盖：** 27 / 27 个逻辑节点已有截面；62 / 62 条原子观点完成映射。

#### 公司影响、预期差与动作

| 公司 | 敞口 | 盈利传导 | 市场定价 | 当前结论 | 动作 |
|---|---|---|---|---|---|
| AMD（AMD） | MI450/Helios GPU与ROCm平台直接受益于替代需求。 | 2026年第三季度末开始交付、第四季度与2027年爬坡；利润弹性需扣除客户认股权证和研发投入。 | 两份投行报告均为中性，报告股价显著高于385/410美元目标价。 | 产品与订单方向改善，但赔率和股东可得利润尚未通过。 | watch_only |
| Alphabet（GOOGL） | TPU自用并可能通过外部所有权/SPV模式扩大merchant市场。 | 外部TPU数量与backlog情景可提升收入和毛利，但均来自投行模型，巨额资本开支可能压低自由现金流。 | 巴克莱425美元目标价相对报告股价约有34%空间，关键假设仍是外部TPU商业化。 | 潜在预期差存在，但合同、交付和资本强度尚待验证。 | watch_only |
| Meta（META） | AI广告、商业agent、自研MTIA与大规模GPU集群的综合受益者。 | 12.9万颗H100单集群确认基础设施投入，广告回报可覆盖部分投入；整体capex与自研/商用芯片组合仍不透明。 | 本次未更新Meta市场估值，原有投行目标价不是反向估值证据。 | 实际GPU集群证据增强，但它不是纯硬件敞口，需继续穿透资本回报。 | watch_only |
| Intel（INTC） | AI服务器CPU、先进代工和EMIB-T替代封装的间接受益者。 | DCAI收入增长和capex上调提供邻近验证，但外部先进代工收入占比仍低。 | 当前材料没有提供同截面可复现估值。 | 供给侧可选项存在，尚无足够外部客户规模与估值证据。 | watch_only |
| Amazon（AMZN） | AWS是GPU/ASIC云基础设施直接需求方，2026资本开支指引约2000亿美元。 | 德银预计AWS需求和推理容量继续增长，但总资本开支同时覆盖零售、物流、价格上涨、伙伴融资与内部芯片，尚不能穿透到GPU采购和回报。 | 本轮只有德银资本开支和AWS增长预期，没有可复现的反向估值或GPU需求单独定价。 | 需求强度代理增强，GPU数量、交付和资本回报仍未通过。 | watch_only |
| Broadcom（AVGO） | 定制ASIC和数据中心网络直接受益于Hyperscaler及模型公司自研加速器扩张。 | 摩根大通预测2026-2030累计AI收入超过1万亿美元，但该值合并ASIC与网络且不是正式订单，利润桥仍依赖客户项目兑现、HBM/代工成本和收入确认。 | 本轮未建立同截面反向估值；研报目标价不能替代市场已定价分析。 | 价值代理很大但来源单一、口径混合，维持观察。 | watch_only |
| Naver（035420.KS） | Naver作为大型互联网平台和AIDC开发方，计划2028年前200MW、长期1GW算力基础设施。 | 初期100亿美元框架和外部SPV降低表内资本压力，但剩余800MW仍需约400亿美元以上资金并依赖Hyperscaler长期转租；收入和利用率尚未验证。 | 本轮未进行Naver反向估值，野村中性评级和目标价不能证明错价。 | 新增计划容量样本，但融资、客户签约与设备上线都是关键断点。 | watch_only |

## 1. 需求侧

### 简单逻辑链

Q1 只定义谁在需求 GPU，并将主体分为当前需求方与潜在未来需求方；不在 Q1 展开业务、任务、承载系统、GPU 规格、采购通道、数量或截面变化。Q2 再按需求方清单建立当前需求量基线，后续节点分别验证工作负载、单位算力、预算、订单和财务兑现。

### 逻辑节点与公司信息

#### Q1 需求方

**当前需求方**

- 超大规模云服务商
- AI 模型公司
- GPU 云与算力服务商
- 大型互联网平台
- 大型企业与工业客户
- 科研机构
- 主权及公共算力建设主体

**潜在未来需求方**

- 尚未规模化部署 AI 的传统企业
- 从租用算力转向自建集群的 AI 应用公司
- 电信与边缘云运营商
- 机器人及自动驾驶平台运营方
- 新进入的区域公共算力主体

#### Q2 当前需求量基线

##### 1. 当前需求方

###### 超大规模云服务商

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2025-06-10 · [DIGITIMES Research：Global annual AI server shipments, 2024-2025](https://www.digitimes.com/reports/item.php?id=20250604RS400) | 2025E | 第三方研究 | **北美CSP高端AI服务器采购：>70万台（GPU+ASIC合计）**<br>代理映射 · 由高端AI服务器超过100万台及北美CSP占70%得到下限；不是GPU专属数量，也未覆盖全部Hyperscaler。 |
| 2026-07-27 · [大摩：生成式AI投资回报率25%-50%的路径](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/manual/大摩-北美互联网行业：生成式AI投资回报率可达25%-50%的路径-260727.pdf>) | 标准化1GW情景 | 机构研报 | **1GW GB300容量情景：约410,256颗GB300；75%利用率；约390亿美元全口径资本成本**<br>代理映射 · 大摩单位经济性模型，不是任何云厂商已安装或已下单量；代际、网络、电力、软件及利用率会改变换算。 |
| 2026-07-27 · [德银：Amazon 2026年二季报预览](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/manual/德银-亚马逊（AMZN.US）2026年二季报预览：经营利润与AWS收入有望超预期-260727.pdf>) | 2026-2027E | 机构研报 | **Amazon资本开支价值代理：2026指引约2000亿美元；德银2027E约3000亿美元**<br>代理映射 · 资本开支覆盖非GPU业务，且包含新增容量、价格、伙伴融资与内部芯片影响。 |

###### AI 模型公司

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2026-01-06 · [xAI：Series E与2025年末算力规模](https://x.ai/news/series-e?stream=top) | 2025年末 | 市场消息 | **xAI H100 GPU等效存量：>100万颗H100等效**<br>样本映射 · 单一模型公司样本；等效算力不等于同型号物理GPU，也不能外推全部模型公司。 |
| 2025-07-22 · [OpenAI：Stargate与Oracle新增4.5GW合作](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) | 2025-07披露的在建平台 | 市场消息 | **OpenAI Stargate在建芯片容量：>200万颗芯片；>5GW在建**<br>样本映射 · 超过200万颗是整个在建平台规划，不是已安装GPU；芯片口径未拆GPU与其它加速器。 |
| 2025-06-11 · [NVIDIA：欧洲建设区域AI基础设施](https://nvidianews.nvidia.com/news/europe-ai-infrastructure) | 首阶段，2026扩站 | 市场消息 | **Mistral首阶段Grace Blackwell系统：1.8万套系统**<br>样本映射 · 原文单位是systems而非单颗GPU，不能机械换算为1.8万颗GPU。 |
| 2026-07-24 · [巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 2026E-2028E | 机构研报 | **外部TPU容量模型：2026E约100万颗；2027E约203万颗；2028E约474万颗**<br>代理映射 · 巴克莱模型覆盖外部TPU项目，未按Anthropic、OpenAI、Meta等客户分配，也不是公司指引。 |
| 2026-07-24 · [巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 2Q26及长期 | 机构研报 | **外部TPU收入backlog估算：2Q26约880亿美元；长期累计>3000亿美元**<br>代理映射 · 投行依据项目推算的价值代理，不是Google正式披露订单，需以合同与交付验证。 |
| 2026-07-24 · [摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 排至2027年 | 机构研报 | **AMD MI450/Helios客户部署排期：Anthropic、OpenAI、Meta等合计数GW**<br>代理映射 · 投行会议纪要的合计口径，未按客户、GPU颗数或实际交付拆分。 |

###### GPU 云与算力服务商

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2026-03-02 · [CoreWeave 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm) | 2025年末 | 官方财报 | **CoreWeave活跃与签约功率：>850MW活跃；约3.1GW签约**<br>样本映射 · 单一GPU云样本；功率包含非GPU设施，签约功率不是已上线需求。 |
| 2026-05-08 · [IREN Form 10-Q（截至2026年3月31日季度）](https://www.sec.gov/Archives/edgar/data/1878848/000187884826000026/iren-20260331.htm) | 截至2026-03-31 | 官方财报 | **IREN GPU fleet：约15万颗已安装或已下单**<br>样本映射 · 财报把已安装与已下单合并，无法判断当前可用存量。 |
| 2026-05-13 · [Nebius Q1 2026 Letter to Shareholders](https://assets.nebius.com/assets/6aba98d1-946c-4891-a420-d2f0aa60da95/Nebius%20SHL_Q1%202026.pdf?cache-buster=2026-05-13T12%3A54%3A12.130Z) | 2026Q1及2026年末 | 市场消息 | **Nebius签约与连接功率：>3.5GW签约；2026年末>4GW签约、800MW-1GW连接**<br>样本映射 · 签约、连接和活跃功率定义不同，不能互换，也不能直接换算GPU颗数。 |
| 2025-06-11 · [NVIDIA：欧洲建设区域AI基础设施](https://nvidianews.nvidia.com/news/europe-ai-infrastructure) | 第一阶段 | 市场消息 | **Nebius与Nscale英国第一阶段部署：合计1.4万颗Blackwell GPU**<br>样本映射 · 两家云服务商合计计划，无法分配至单一公司，亦未说明全部已上线。 |

###### 大型互联网平台

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2024-02-01 · [Meta Q4 2023 Earnings Call Transcript](https://s21.q4cdn.com/399680738/files/doc_financials/2023/q4/META-Q4-2023-Earnings-Call-Transcript.pdf) | 2024年末预测 | 市场消息 | **Meta H100等效容量计划：约60万颗H100等效，其中约35万颗H100**<br>样本映射 · 公司在2024年初给出的年末计划，当前材料没有独立确认全部转化为实际存量。 |
| 2025-09-29 · [Meta：Infrastructure Evolution and the Advent of AI](https://engineering.fb.com/2025/09/29/data-infrastructure/metas-infrastructure-evolution-and-the-advent-of-ai/) | 截至2025-09披露 | 市场消息 | **Meta已建H100单集群：12.9万颗H100**<br>直接映射 · 只覆盖一个已建集群，不代表Meta全部GPU或自研加速器存量。 |
| 2026-07-27 · [野村：Naver AIDC资本开支与转租能见度](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/manual/野村-Naver（035420.KS）：AIDC资本开支风险出清，转租落地能见度成关键-260727.pdf>) | 2028及长期 | 机构研报 | **Naver AIDC功率与资本框架：2028年前200MW；长期1GW；初期100亿美元框架**<br>样本映射 · 剩余800MW仍需约400亿美元以上融资并依赖Hyperscaler转租；不是已上线GPU容量。 |

###### 大型企业与工业客户

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2025-10-30 · [NVIDIA：韩国政府与产业集团建设AI基础设施](https://nvidianews.nvidia.com/news/south-korea-ai-infrastructure) | 2025-10公布的建设计划 | 市场消息 | **Samsung与SK工业AI工厂：两家分别>5万颗GPU**<br>样本映射 · 两家大型工业集团样本，均是建设计划而非已上线存量，不能外推全部企业客户。 |

###### 科研机构

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2025-09-05 · [EuroHPC：JUPITER启动欧洲百亿亿次计算时代](https://www.eurohpc-ju.europa.eu/jupiter-launching-europes-exascale-era-2025-09-05_en) | 2025-09已启用 | 市场消息 | **JUPITER GH200配置：约2.4万颗GH200**<br>样本映射 · 单一欧洲科研超级计算机样本，不代表全球科研机构总需求。 |

###### 主权及公共算力建设主体

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2025-05-13 · [HUMAIN与NVIDIA沙特AI工厂合作](https://nvidianews.nvidia.com/news/humain-and-nvidia-announce-strategic-partnership-to-build-ai-factories-of-the-future-in-saudi-arabia) | 首阶段及未来五年 | 市场消息 | **HUMAIN主权AI工厂部署计划：首阶段1.8万颗GB300；五年规划数十万颗**<br>样本映射 · 属于已宣布部署计划和远期规划，不是当前已安装存量。 |
| 2025-09-16 · [英国政府：英美技术繁荣协议与12万颗GPU部署](https://www.gov.uk/government/news/us-uk-pact-will-boost-advances-in-drug-discovery-create-tens-of-thousands-of-jobs-and-transform-lives) | 2025-09公布的部署计划 | 市场消息 | **英国国家级先进GPU部署：全英12万颗；其中Nscale最高6万颗**<br>代理映射 · 跨多个公私项目，不能全部视为政府直接采购或已安装存量。 |

##### 2. 潜在未来需求方

###### 尚未规模化部署 AI 的传统企业

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2025-06-11 · [NVIDIA：欧洲建设区域AI基础设施](https://nvidianews.nvidia.com/news/europe-ai-infrastructure) | 2025-06公布的建设计划 | 市场消息 | **德国面向制造商的共享工业AI云：1万颗Blackwell GPU**<br>代理映射 · 这是供给侧共享入口，不是传统企业已采购或已使用1万颗GPU。 |

###### 从租用算力转向自建集群的 AI 应用公司

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2025-10-23 · [KRAFTON：转向AI First并建设GPU集群](https://www.krafton.com/news/press/%ED%81%AC%EB%9E%98%ED%94%84%ED%86%A4-ai-first-%EA%B8%B0%EC%97%85-%EC%A0%84%ED%99%98-%EC%84%A0%EC%96%B8-1000%EC%96%B5-%EC%9B%90-%EC%9D%B4%EC%83%81-%ED%88%AC%EC%9E%90/) | 2025-10公布；2026H2平台目标 | 市场消息 | **KRAFTON自建B300 GPU集群预算：约1000亿韩元**<br>代理映射 · 证明应用公司存在自建路径，但未披露此前租用规模，不能认定为租赁的净替代。 |

###### 电信与边缘云运营商

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2025-06-11 · [NVIDIA：欧洲建设区域AI基础设施](https://nvidianews.nvidia.com/news/europe-ai-infrastructure) | 2025-06试点 | 市场消息 | **Telefónica分布式边缘AI试点：数百颗NVIDIA GPU**<br>样本映射 · 单一运营商试点，不代表电信行业规模部署。 |

###### 机器人及自动驾驶平台运营方

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2025-10-30 · [NVIDIA：韩国政府与产业集团建设AI基础设施](https://nvidianews.nvidia.com/news/south-korea-ai-infrastructure) | 2025-10公布的建设计划 | 市场消息 | **Hyundai物理AI工厂：5万颗Blackwell GPU**<br>样本映射 · 用于制造、自动驾驶和机器人等混合任务，仍是合作建设计划。 |

###### 新进入的区域公共算力主体

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2026-07-16 · [NVIDIA：日本FRONTia国家物理AI基础设施](https://nvidianews.nvidia.com/news/japan-government-industrial-leaders-and-nvidia-launch-the-worlds-first-national-ai-infrastructure) | 2026-07公布的建设计划 | 市场消息 | **日本Noetra FRONTia物理AI工厂：2.75万颗Rubin GPU；140MW**<br>样本映射 · 公共—产业协同的新进入项目，尚未形成已上线存量。 |

##### 3. 其它分类

###### 全球AI服务器出货

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2025-06-10 · [DIGITIMES Research：Global annual AI server shipments, 2024-2025](https://www.digitimes.com/reports/item.php?id=20250604RS400) | 2025E | 第三方研究 | **全球AI服务器出货：181万台；其中高端HBM机型>100万台**<br>不做映射 · 同时包含GPU与ASIC，且无法无重叠地分配到Q1全部需求方。 |

###### 全球GPU型AI服务器

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2025-06-10 · [DIGITIMES Research：Global annual AI server shipments, 2024-2025](https://www.digitimes.com/reports/item.php?id=20250604RS400)<br>2026-01-20 · [TrendForce：2026年全球AI服务器出货与GPU/ASIC结构](https://www.trendforce.com/presscenter/news/20260120-12887.html) | 2026E | 第三方研究 | **全球GPU型AI服务器：约161万台（跨来源机械估算）**<br>不做映射 · 由181万×1.28×69.7%合成，不是机构直接发布值；系统数不能直接换算GPU颗数。 |

###### 美国数据中心功率需求

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2026-07-27 · [摩根大通：行业数据中心需求更新](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/manual/摩根大通-硬件与网络设备：行业数据中心需求更新核心要点-260727.pdf>) | 2030E | 机构研报 | **美国数据中心功率需求：2030年基准118GW；AI芯片情景160GW**<br>不做映射 · BloombergNEF情景经摩根大通转述；含设施负载，不能按需求方或GPU/ASIC无重叠分配。 |

###### LLM Token活动样本

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2026-07-27 · [摩根大通：数据中心观察—Token支出与GPU价格](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/manual/摩根大通-硬件与网络设备｜数据中心观察：Token支出持续增长，GPU价格保持坚挺，存储通胀开始降温-260727.pdf>) | 2026年7月 | 机构研报 | **LLM Token活动样本：2026年7月token量+18%环比、21x同比；支出+7%环比、11x同比**<br>不做映射 · 约300个OpenRouter模型样本，偏开发者/初创/agentic coding并排除第一方端点，不能代表全市场GPU需求。 |

###### 定制ASIC与网络收入预测

| 来源 | 期间 | 信息类型 | 具体信息 |
|---|---|---|---|
| 2026-07-27 · [摩根大通：Broadcom未来五年AI收入预测](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/manual/摩根大通-博通（AVGO.US）：三星多年存储器代工谅解备忘录意味着未来五年博通AI累计收入将超过1万亿美元；重申“增持”-260727.pdf>) | 2026-2030E | 机构研报 | **定制ASIC与网络收入预测：Broadcom 2026-2030累计AI收入>1万亿美元；约60%+ CAGR**<br>不做映射 · 摩根大通分析师模型，合并ASIC与网络且客户项目可能重叠，不是正式订单或芯片颗数。 |

#### 真实 AI 工作负载

训练、推理和 agent 任务是否在真实增长，而非只有主题热度？

**当前结论：** AI 任务需求已有应用侧和公司 TAM 两类信号：Meta 商业 AI 对话快速增长，AMD 将长期加速器 TAM 大幅上调；但当前材料仍以单一应用指标和公司/投行预测为主，尚不足以证明全市场任务量。

##### AMD

**截面变化与评估：** AMD在“真实 AI 工作负载”下，当前最重要的信息是：AMD 将 2030 年 AI 加速器 TAM 上调至约 1.4 万亿美元，相对 2025 年约 2,000 亿美元隐含超过 45% 的五年复合增速；摩根大通判断增长将由训练扩展到推理和 agent 工作负载。该数字是公司口径与投行解释…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第1-2页，AI Accelerator TAM） · 支持**：AMD 将 2030 年 AI 加速器 TAM 上调至约 1.4 万亿美元，相对 2025 年约 2,000 亿美元隐含超过 45% 的五年复合增速；摩根大通判断增长将由训练扩展到推理和 agent 工作负载。该数字是公司口径与投行解释，不是已兑现收入。 |

##### Meta

**截面变化与评估：** Meta在“真实 AI 工作负载”下，当前最重要的信息是：Meta 各消息平台中，用户与商业 AI 的对话约为每周 1,000 万次，较年初增长约十倍；德银把这视为 2027 年可能通过订阅和按量收费变现的应用需求。该指标证明工作负载在增长，但尚未直接披露其对应 GPU/ASIC 用量。。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[德银-Meta：宏大野心需匹配宏大体量](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/德银-Meta（META.US）：宏大野心需匹配宏大体量-260724.pdf>) | 研报 | • **观点 1（第5页，Business agents） · 支持**：Meta 各消息平台中，用户与商业 AI 的对话约为每周 1,000 万次，较年初增长约十倍；德银把这视为 2027 年可能通过订阅和按量收费变现的应用需求。该指标证明工作负载在增长，但尚未直接披露其对应 GPU/ASIC 用量。 |

#### 单位任务算力强度

每项任务所需的 GPU/ASIC 算力是否上升，形成需求弹性？

**当前结论：** 训练、推理和 agent 被认为会扩大算力需求，但现有材料没有把单位任务计算量与效率改善放在同一口径比较，需求弹性尚未被量化。

##### AMD

**截面变化与评估：** AMD在“单位任务算力强度”下，当前最重要的信息是：AMD 将 2030 年 AI 加速器 TAM 上调至约 1.4 万亿美元，相对 2025 年约 2,000 亿美元隐含超过 45% 的五年复合增速；摩根大通判断增长将由训练扩展到推理和 agent 工作负载。该数字是公司口径与投行解释…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第1-2页，AI Accelerator TAM） · 支持**：AMD 将 2030 年 AI 加速器 TAM 上调至约 1.4 万亿美元，相对 2025 年约 2,000 亿美元隐含超过 45% 的五年复合增速；摩根大通判断增长将由训练扩展到推理和 agent 工作负载。该数字是公司口径与投行解释，不是已兑现收入。 |

#### 客户预算与资本承诺

云厂商、模型公司和企业是否把需求转化为可持续预算？

**当前结论：** Meta 2026 年资本开支指引和更高的 2027-2028 年机构估计显示客户预算仍在扩大，外部 TPU 与合作方融资也在增加可用资本；但后续年份主要是分析师情景。

##### Meta

**截面变化与评估：** Meta在“客户预算与资本承诺”下，当前最重要的信息是：Meta 的容量情景由 7GW 升至 14GW，资本开支预期可能升至 2027 年 2,000 亿美元以上；Hyperion 等伙伴融资可能降低报表内直接负担。对治理分析而言，关键不是只看名义 capex，而是追踪担保、租赁、合作方承诺…；Meta 2026 年资本开支指引为 1,250 亿至 1,450 亿美元；德银称市场已把 2027 年约 14GW 容量对应的资本开支预期推至 2,000 亿美元低至中段，并给出 2027 年约 2,100 亿至 2,150 亿美元、…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[德银-Meta：宏大野心需匹配宏大体量](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/德银-Meta（META.US）：宏大野心需匹配宏大体量-260724.pdf>) | 研报 | • **观点 1（第2页，Capex remains a key debate） · 支持**：Meta 2026 年资本开支指引为 1,250 亿至 1,450 亿美元；德银称市场已把 2027 年约 14GW 容量对应的资本开支预期推至 2,000 亿美元低至中段，并给出 2027 年约 2,100 亿至 2,150 亿美元、2028 年约 2,650 亿美元的估计。这是大型客户继续扩大 AI 算力采购的直接预算信号，但后两项属于分析师估计。<br>• **观点 2（第2、5-6页，capacity and funding structure） · 线索**：Meta 的容量情景由 7GW 升至 14GW，资本开支预期可能升至 2027 年 2,000 亿美元以上；Hyperion 等伙伴融资可能降低报表内直接负担。对治理分析而言，关键不是只看名义 capex，而是追踪担保、租赁、合作方承诺及最终风险承担者。 |

##### Alphabet / Google

**截面变化与评估：** Alphabet / Google在“客户预算与资本承诺”下，当前最重要的信息是：巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2、4-5页，External TPU sales framework） · 支持**：巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW，对应约 100 万颗、203 万颗和 474 万颗 TPU。它说明定制 ASIC 正从云厂内部自用扩展到外部客户，但数量是投行模型而非公司正式指引。 |

##### Apollo

**截面变化与评估：** Apollo在“客户预算与资本承诺”下，当前最重要的信息是：巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2、4-5页，External TPU sales framework） · 支持**：巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW，对应约 100 万颗、203 万颗和 474 万颗 TPU。它说明定制 ASIC 正从云厂内部自用扩展到外部客户，但数量是投行模型而非公司正式指引。 |

##### Blackstone

**截面变化与评估：** Blackstone在“客户预算与资本承诺”下，当前最重要的信息是：巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2、4-5页，External TPU sales framework） · 支持**：巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW，对应约 100 万颗、203 万颗和 474 万颗 TPU。它说明定制 ASIC 正从云厂内部自用扩展到外部客户，但数量是投行模型而非公司正式指引。 |

##### Broadcom

**截面变化与评估：** Broadcom在“客户预算与资本承诺”下，当前最重要的信息是：巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2、4-5页，External TPU sales framework） · 支持**：巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW，对应约 100 万颗、203 万颗和 474 万颗 TPU。它说明定制 ASIC 正从云厂内部自用扩展到外部客户，但数量是投行模型而非公司正式指引。 |

##### Hyperion

**截面变化与评估：** Hyperion在“客户预算与资本承诺”下，当前最重要的信息是：Meta 的容量情景由 7GW 升至 14GW，资本开支预期可能升至 2027 年 2,000 亿美元以上；Hyperion 等伙伴融资可能降低报表内直接负担。对治理分析而言，关键不是只看名义 capex，而是追踪担保、租赁、合作方承诺…。综合这些材料，该实体对本节点的截面影响为尚不明确；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[德银-Meta：宏大野心需匹配宏大体量](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/德银-Meta（META.US）：宏大野心需匹配宏大体量-260724.pdf>) | 研报 | • **观点 1（第2、5-6页，capacity and funding structure） · 线索**：Meta 的容量情景由 7GW 升至 14GW，资本开支预期可能升至 2027 年 2,000 亿美元以上；Hyperion 等伙伴融资可能降低报表内直接负担。对治理分析而言，关键不是只看名义 capex，而是追踪担保、租赁、合作方承诺及最终风险承担者。 |

#### 订单与交付可见性

预算是否转化为有客户、有时间表的 GPU/ASIC 与系统订单？

**当前结论：** AMD Helios 和外部 TPU 已出现客户、GW、backlog 与交付窗口等可见性线索，但相当一部分数字来自投行模型或供应商计划，仍需客户采购承诺与实际发货交叉验证。

##### AMD

**截面变化与评估：** AMD在“订单与交付可见性”下，当前最重要的信息是：摩根士丹利称 Helios 在关键客户处的采用进展顺利，客户证言显示 2027 年将强劲爬坡，并把 coding agent 视为 AMD GPU 生态采用的明确加速器；但该报告同时认为 AMD 本代产品仍未取得领导地位。；MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第1、3页，MI450/Helios ramp） · 支持**：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单计划提供了可见性，但实际收入仍取决于系统交付和客户数据中心按期完工。 |
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1页，Key Takeaways） · 支持**：摩根士丹利称 Helios 在关键客户处的采用进展顺利，客户证言显示 2027 年将强劲爬坡，并把 coding agent 视为 AMD GPU 生态采用的明确加速器；但该报告同时认为 AMD 本代产品仍未取得领导地位。 |

##### Alphabet / Google

**截面变化与评估：** Alphabet / Google在“订单与交付可见性”下，当前最重要的信息是：巴克莱依据已披露数据中心供应商项目估算，2026 年第二季度 Google 外部 TPU 收入 backlog 约 880 亿美元，长期累计潜在收入超过 3,000 亿美元；该估计只覆盖首批已识别项目，必须与实际采购承诺和交付节奏交叉验…；巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2、4-5页，External TPU sales framework） · 支持**：巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW，对应约 100 万颗、203 万颗和 474 万颗 TPU。它说明定制 ASIC 正从云厂内部自用扩展到外部客户，但数量是投行模型而非公司正式指引。<br>• **观点 2（第6页，What's Already Been Announced） · 支持**：巴克莱依据已披露数据中心供应商项目估算，2026 年第二季度 Google 外部 TPU 收入 backlog 约 880 亿美元，长期累计潜在收入超过 3,000 亿美元；该估计只覆盖首批已识别项目，必须与实际采购承诺和交付节奏交叉验证。 |

##### Anthropic

**截面变化与评估：** Anthropic在“订单与交付可见性”下，当前最重要的信息是：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第1、3页，MI450/Helios ramp） · 支持**：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单计划提供了可见性，但实际收入仍取决于系统交付和客户数据中心按期完工。 |

##### Apollo

**截面变化与评估：** Apollo在“订单与交付可见性”下，当前最重要的信息是：巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2、4-5页，External TPU sales framework） · 支持**：巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW，对应约 100 万颗、203 万颗和 474 万颗 TPU。它说明定制 ASIC 正从云厂内部自用扩展到外部客户，但数量是投行模型而非公司正式指引。 |

##### Blackstone

**截面变化与评估：** Blackstone在“订单与交付可见性”下，当前最重要的信息是：巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2、4-5页，External TPU sales framework） · 支持**：巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW，对应约 100 万颗、203 万颗和 474 万颗 TPU。它说明定制 ASIC 正从云厂内部自用扩展到外部客户，但数量是投行模型而非公司正式指引。 |

##### Broadcom

**截面变化与评估：** Broadcom在“订单与交付可见性”下，当前最重要的信息是：巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2、4-5页，External TPU sales framework） · 支持**：巴克莱根据 Broadcom/Blackstone/Apollo 的 20GW AI XPV 计划与 Google-Blackstone 合资项目，估计外部 TPU 容量可由 2026 年 1.4GW 增至 2028 年 11.5GW，对应约 100 万颗、203 万颗和 474 万颗 TPU。它说明定制 ASIC 正从云厂内部自用扩展到外部客户，但数量是投行模型而非公司正式指引。 |

##### Meta

**截面变化与评估：** Meta在“订单与交付可见性”下，当前最重要的信息是：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第1、3页，MI450/Helios ramp） · 支持**：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单计划提供了可见性，但实际收入仍取决于系统交付和客户数据中心按期完工。 |

##### OpenAI

**截面变化与评估：** OpenAI在“订单与交付可见性”下，当前最重要的信息是：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第1、3页，MI450/Helios ramp） · 支持**：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单计划提供了可见性，但实际收入仍取决于系统交付和客户数据中心按期完工。 |

##### 数据中心客户

**截面变化与评估：** 数据中心客户在“订单与交付可见性”下，当前最重要的信息是：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第1、3页，MI450/Helios ramp） · 支持**：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单计划提供了可见性，但实际收入仍取决于系统交付和客户数据中心按期完工。 |

#### 收入与利润兑现

订单是否进入收入、毛利、现金流和下一期指引？

**当前结论：** Intel DCAI 的相邻收入增长说明 AI 基础设施支出在扩散，但它不能替代 GPU/ASIC 分部收入、增量毛利和现金流证据；当前材料尚未完成节点到核心公司盈利的闭环。

##### Intel

**截面变化与评估：** Intel在“收入与利润兑现”下，当前最重要的信息是：Intel DCAI 收入在 2026 年第二季度环比增长 24%、同比增长 59%，由云服务商和企业服务器需求及供给改善驱动；管理层预计 2026 年服务器 CPU 需求保持双位数增长，并延续到 2027-2028 年。它是 AI 基…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：PC 与服务器传导分析](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-PC与服务器：英特尔2026年二季度财报及AMD“Advancing AI 2026”大会传导分析-260724.pdf>) | 研报 | • **观点 1（第1页，AI-driven general server demand strength） · 支持**：Intel DCAI 收入在 2026 年第二季度环比增长 24%、同比增长 59%，由云服务商和企业服务器需求及供给改善驱动；管理层预计 2026 年服务器 CPU 需求保持双位数增长，并延续到 2027-2028 年。它是 AI 基础设施扩张的邻近验证，不等同于 GPU/ASIC 自身收入。 |


### 最新结论与趋势

Q2新增6份机构研报和6条原子观点，使信息矩阵从24行增至30行。超大规模云服务商新增大摩1GW约41万颗GB300单位容量情景和Amazon 2026/2027资本开支代理，大型互联网平台新增Naver 200MW至1GW AIDC规划；其它分类新增美国数据中心118GW/160GW功率情景、OpenRouter token活动样本和Broadcom未来五年AI收入预测。材料扩展了数量、功率和价值代理，但均不能替代官方已安装、交付、利用率与可去重采购量。

**趋势变化：** 当前需求方仍为7/7、潜在未来需求方5/5；当前信息行由17增至20，潜在未来维持5行，其它分类由2增至5类、共5行。新增证据全部来自机构研报且多为情景或预测，Q2节点维持弱状态，下一步必须用公司官方文件核验并建立单位、期间和状态一致的数量桥。

## 2. 供给侧

### 简单逻辑链

有效供给取决于先进晶圆、HBM 与封装、系统集成、机房电力和最终可交付系统的最小值。研究不能只看单颗芯片产能，而要定位当前约束、扩产周期、良率、认证以及约束转移。

### 逻辑节点与公司信息

#### 先进制程晶圆

先进逻辑晶圆的产能、良率和客户分配是否限制 GPU/ASIC 供给？

**当前结论：** Intel 上调资本开支表明供给正在响应，但材料没有直接量化 GPU/ASIC 先进晶圆的现有缺口、TSMC 分配和良率，因此不能断言晶圆是当前最强约束。

##### Intel

**截面变化与评估：** Intel在“先进制程晶圆”下，当前最重要的信息是：Intel 将 2026 年资本开支指引上调至超过 200 亿美元，并称 2027 年还会显著增长，用于洁净室扩建和锁定设备订单。供给正在响应高价和短缺，因此当前稀缺性不能外推为永久稀缺。。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：PC 与服务器传导分析](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-PC与服务器：英特尔2026年二季度财报及AMD“Advancing AI 2026”大会传导分析-260724.pdf>) | 研报 | • **观点 1（第2页，Intel capex guidance） · 支持**：Intel 将 2026 年资本开支指引上调至超过 200 亿美元，并称 2027 年还会显著增长，用于洁净室扩建和锁定设备订单。供给正在响应高价和短缺，因此当前稀缺性不能外推为永久稀缺。 |

#### HBM、封装与基板

HBM、先进封装、基板和测试是否成为可交付芯片的约束？

**当前结论：** 投行材料同时把 CoWoS、内存、基板和先进逻辑列为持续约束；Intel EMIB-T 的替代路线仍处于较低良率和小批量阶段，说明短期封装与相关输入仍可能限制供给。

##### Intel

**截面变化与评估：** Intel在“HBM、封装与基板”下，当前最重要的信息是：报告称 Intel EMIB-T 当前良率约 60%，目标 2027 年进入高量产；多个 AI 加速器项目因 CoWoS 紧张而评估 EMIB-T，但预计先从小批量开始，最大项目 TPU v9 或到 2027 年末至 2028 年才量产…；摩根大通把先进逻辑晶圆、硅片、内存和基板列为服务器供应链的持续约束，并预计供给改善会推动 2026 年第四季度收入进一步上行。有效供给仍由多项输入的最小值决定，而不是只看 GPU 晶圆数量。。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：PC 与服务器传导分析](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-PC与服务器：英特尔2026年二季度财报及AMD“Advancing AI 2026”大会传导分析-260724.pdf>) | 研报 | • **观点 1（第1页，AI-driven general server demand strength） · 支持**：摩根大通把先进逻辑晶圆、硅片、内存和基板列为服务器供应链的持续约束，并预计供给改善会推动 2026 年第四季度收入进一步上行。有效供给仍由多项输入的最小值决定，而不是只看 GPU 晶圆数量。<br>• **观点 2（第2页，EMIB-T high volume ramp） · 支持**：报告称 Intel EMIB-T 当前良率约 60%，目标 2027 年进入高量产；多个 AI 加速器项目因 CoWoS 紧张而评估 EMIB-T，但预计先从小批量开始，最大项目 TPU v9 或到 2027 年末至 2028 年才量产。替代封装路线正在形成，但短期无法立刻消除瓶颈。 |

##### AI 服务器供应链

**截面变化与评估：** AI 服务器供应链在“HBM、封装与基板”下，当前最重要的信息是：摩根大通把先进逻辑晶圆、硅片、内存和基板列为服务器供应链的持续约束，并预计供给改善会推动 2026 年第四季度收入进一步上行。有效供给仍由多项输入的最小值决定，而不是只看 GPU 晶圆数量。。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：PC 与服务器传导分析](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-PC与服务器：英特尔2026年二季度财报及AMD“Advancing AI 2026”大会传导分析-260724.pdf>) | 研报 | • **观点 1（第1页，AI-driven general server demand strength） · 支持**：摩根大通把先进逻辑晶圆、硅片、内存和基板列为服务器供应链的持续约束，并预计供给改善会推动 2026 年第四季度收入进一步上行。有效供给仍由多项输入的最小值决定，而不是只看 GPU 晶圆数量。 |

#### 系统集成与调试

ODM、机架、网络和软件调试是否限制芯片转化为可用系统？

**当前结论：** Helios 的分阶段发货明确把 ODM 调试、制造和客户机房对齐列为爬坡条件，说明有效供给单位已经从单颗芯片转为可验收机架系统。

##### AMD

**截面变化与评估：** AMD在“系统集成与调试”下，当前最重要的信息是：Helios 已进入量产，计划 2026 年第三季度开始发货、第四季度爬坡。该进度支持 AMD 供给增加，但客户采用、ODM 调试和机房配套仍决定收入确认速度。；AMD 将 MI450/Helios 的首批交付定在 2026 年第三季度末，再于第四季度和 2027 年上半年提速；管理层称分阶段爬坡是为了给 ODM 调试制造并与客户机房建设对齐。GPU 供给的可用单位已经是按期调试完成的机架系统…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第3-4页，MI450/Helios shipping schedule） · 支持**：AMD 将 MI450/Helios 的首批交付定在 2026 年第三季度末，再于第四季度和 2027 年上半年提速；管理层称分阶段爬坡是为了给 ODM 调试制造并与客户机房建设对齐。GPU 供给的可用单位已经是按期调试完成的机架系统，而非单颗芯片。 |
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1页，Compute leadership） · 支持**：Helios 已进入量产，计划 2026 年第三季度开始发货、第四季度爬坡。该进度支持 AMD 供给增加，但客户采用、ODM 调试和机房配套仍决定收入确认速度。 |

##### ODM / 系统集成商

**截面变化与评估：** ODM / 系统集成商在“系统集成与调试”下，当前最重要的信息是：Helios 已进入量产，计划 2026 年第三季度开始发货、第四季度爬坡。该进度支持 AMD 供给增加，但客户采用、ODM 调试和机房配套仍决定收入确认速度。；AMD 将 MI450/Helios 的首批交付定在 2026 年第三季度末，再于第四季度和 2027 年上半年提速；管理层称分阶段爬坡是为了给 ODM 调试制造并与客户机房建设对齐。GPU 供给的可用单位已经是按期调试完成的机架系统…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第3-4页，MI450/Helios shipping schedule） · 支持**：AMD 将 MI450/Helios 的首批交付定在 2026 年第三季度末，再于第四季度和 2027 年上半年提速；管理层称分阶段爬坡是为了给 ODM 调试制造并与客户机房建设对齐。GPU 供给的可用单位已经是按期调试完成的机架系统，而非单颗芯片。 |
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1页，Compute leadership） · 支持**：Helios 已进入量产，计划 2026 年第三季度开始发货、第四季度爬坡。该进度支持 AMD 供给增加，但客户采用、ODM 调试和机房配套仍决定收入确认速度。 |

##### 数据中心客户

**截面变化与评估：** 数据中心客户在“系统集成与调试”下，当前最重要的信息是：Helios 已进入量产，计划 2026 年第三季度开始发货、第四季度爬坡。该进度支持 AMD 供给增加，但客户采用、ODM 调试和机房配套仍决定收入确认速度。；AMD 将 MI450/Helios 的首批交付定在 2026 年第三季度末，再于第四季度和 2027 年上半年提速；管理层称分阶段爬坡是为了给 ODM 调试制造并与客户机房建设对齐。GPU 供给的可用单位已经是按期调试完成的机架系统…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第3-4页，MI450/Helios shipping schedule） · 支持**：AMD 将 MI450/Helios 的首批交付定在 2026 年第三季度末，再于第四季度和 2027 年上半年提速；管理层称分阶段爬坡是为了给 ODM 调试制造并与客户机房建设对齐。GPU 供给的可用单位已经是按期调试完成的机架系统，而非单颗芯片。 |
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1页，Compute leadership） · 支持**：Helios 已进入量产，计划 2026 年第三季度开始发货、第四季度爬坡。该进度支持 AMD 供给增加，但客户采用、ODM 调试和机房配套仍决定收入确认速度。 |

#### 机房、电力与融资

数据中心电力、冷却、建设和融资是否限制设备上线？

**当前结论：** Meta 容量扩张和外部 TPU 的多主体交付结构显示电力、机房与融资会影响上线节奏；但现有材料以项目情景为主，尚未形成可用容量与延期的统一数据。

##### Alphabet / Google

**截面变化与评估：** Alphabet / Google在“机房、电力与融资”下，当前最重要的信息是：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2-4页，TPU-aaS entity structure and unit economics） · 支持**：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给，也引入跨主体执行和融资风险。 |

##### Apollo

**截面变化与评估：** Apollo在“机房、电力与融资”下，当前最重要的信息是：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2-4页，TPU-aaS entity structure and unit economics） · 支持**：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给，也引入跨主体执行和融资风险。 |

##### Blackstone

**截面变化与评估：** Blackstone在“机房、电力与融资”下，当前最重要的信息是：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2-4页，TPU-aaS entity structure and unit economics） · 支持**：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给，也引入跨主体执行和融资风险。 |

##### Broadcom

**截面变化与评估：** Broadcom在“机房、电力与融资”下，当前最重要的信息是：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2-4页，TPU-aaS entity structure and unit economics） · 支持**：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给，也引入跨主体执行和融资风险。 |

##### Hyperion

**截面变化与评估：** Hyperion在“机房、电力与融资”下，当前最重要的信息是：若 Meta 容量由 2026 年约 7GW 增至 2027 年 14GW，Hyperion 等合作方可能提供 1.0-1.5GW，使 Meta 直接融资的新增容量约为 5.5GW。伙伴资本可以缓解资产负担，但不能消除电力、服务器和建设…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[德银-Meta：宏大野心需匹配宏大体量](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/德银-Meta（META.US）：宏大野心需匹配宏大体量-260724.pdf>) | 研报 | • **观点 1（第5-6页，2027 capex expectations） · 支持**：若 Meta 容量由 2026 年约 7GW 增至 2027 年 14GW，Hyperion 等合作方可能提供 1.0-1.5GW，使 Meta 直接融资的新增容量约为 5.5GW。伙伴资本可以缓解资产负担，但不能消除电力、服务器和建设交付约束。 |

##### Meta

**截面变化与评估：** Meta在“机房、电力与融资”下，当前最重要的信息是：若 Meta 容量由 2026 年约 7GW 增至 2027 年 14GW，Hyperion 等合作方可能提供 1.0-1.5GW，使 Meta 直接融资的新增容量约为 5.5GW。伙伴资本可以缓解资产负担，但不能消除电力、服务器和建设…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[德银-Meta：宏大野心需匹配宏大体量](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/德银-Meta（META.US）：宏大野心需匹配宏大体量-260724.pdf>) | 研报 | • **观点 1（第5-6页，2027 capex expectations） · 支持**：若 Meta 容量由 2026 年约 7GW 增至 2027 年 14GW，Hyperion 等合作方可能提供 1.0-1.5GW，使 Meta 直接融资的新增容量约为 5.5GW。伙伴资本可以缓解资产负担，但不能消除电力、服务器和建设交付约束。 |

##### TSMC

**截面变化与评估：** TSMC在“机房、电力与融资”下，当前最重要的信息是：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2-4页，TPU-aaS entity structure and unit economics） · 支持**：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给，也引入跨主体执行和融资风险。 |

#### 最终可交付供给

所有约束合并后，GPU/ASIC 系统供给能否追上订单？

**当前结论：** 多项输入仍受约束，且 Helios 交付依赖系统与机房同步，因此最终可交付供给短期仍偏紧；不过当前缺少端到端交期、价格和库存序列，证据仍不足。

##### AI 服务器供应链

**截面变化与评估：** AI 服务器供应链在“最终可交付供给”下，当前最重要的信息是：摩根大通把先进逻辑晶圆、硅片、内存和基板列为服务器供应链的持续约束，并预计供给改善会推动 2026 年第四季度收入进一步上行。有效供给仍由多项输入的最小值决定，而不是只看 GPU 晶圆数量。。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：PC 与服务器传导分析](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-PC与服务器：英特尔2026年二季度财报及AMD“Advancing AI 2026”大会传导分析-260724.pdf>) | 研报 | • **观点 1（第1页，AI-driven general server demand strength） · 支持**：摩根大通把先进逻辑晶圆、硅片、内存和基板列为服务器供应链的持续约束，并预计供给改善会推动 2026 年第四季度收入进一步上行。有效供给仍由多项输入的最小值决定，而不是只看 GPU 晶圆数量。 |

##### AMD

**截面变化与评估：** AMD在“最终可交付供给”下，当前最重要的信息是：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第1、3页，MI450/Helios ramp） · 支持**：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单计划提供了可见性，但实际收入仍取决于系统交付和客户数据中心按期完工。 |

##### Anthropic

**截面变化与评估：** Anthropic在“最终可交付供给”下，当前最重要的信息是：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第1、3页，MI450/Helios ramp） · 支持**：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单计划提供了可见性，但实际收入仍取决于系统交付和客户数据中心按期完工。 |

##### Intel

**截面变化与评估：** Intel在“最终可交付供给”下，当前最重要的信息是：摩根大通把先进逻辑晶圆、硅片、内存和基板列为服务器供应链的持续约束，并预计供给改善会推动 2026 年第四季度收入进一步上行。有效供给仍由多项输入的最小值决定，而不是只看 GPU 晶圆数量。。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：PC 与服务器传导分析](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-PC与服务器：英特尔2026年二季度财报及AMD“Advancing AI 2026”大会传导分析-260724.pdf>) | 研报 | • **观点 1（第1页，AI-driven general server demand strength） · 支持**：摩根大通把先进逻辑晶圆、硅片、内存和基板列为服务器供应链的持续约束，并预计供给改善会推动 2026 年第四季度收入进一步上行。有效供给仍由多项输入的最小值决定，而不是只看 GPU 晶圆数量。 |

##### Meta

**截面变化与评估：** Meta在“最终可交付供给”下，当前最重要的信息是：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第1、3页，MI450/Helios ramp） · 支持**：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单计划提供了可见性，但实际收入仍取决于系统交付和客户数据中心按期完工。 |

##### OpenAI

**截面变化与评估：** OpenAI在“最终可交付供给”下，当前最重要的信息是：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第1、3页，MI450/Helios ramp） · 支持**：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单计划提供了可见性，但实际收入仍取决于系统交付和客户数据中心按期完工。 |

##### 数据中心客户

**截面变化与评估：** 数据中心客户在“最终可交付供给”下，当前最重要的信息是：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第1、3页，MI450/Helios ramp） · 支持**：MI450 GPU 与 Helios 机架系统计划于 2026 年 9 月开始交付，2026 年第四季度和 2027 年上半年加速爬坡；报告称 Anthropic、OpenAI、Meta 等客户已有数 GW 部署排至 2027 年。订单计划提供了可见性，但实际收入仍取决于系统交付和客户数据中心按期完工。 |


### 最新结论与趋势

GPU/ASIC 有效供给仍由先进逻辑晶圆、内存、基板、先进封装和机架交付共同决定。摩根大通的供应链检查显示这些环节在 2026 年仍受限，EMIB-T 良率约 60%、高量产要到 2027 年，TPU v9 可能到 2027 年末至 2028 年才放量；AMD 也采用分阶段爬坡，以给 ODM 和客户机房留出调试时间。因此短期瓶颈仍存在。反方向上，Intel 已把 2026 年资本开支上调至 200 亿美元以上，TSMC/Intel/合作资本都在扩大供给，稀缺性不能机械外推。当前判断为：2026-2027 年约束仍有投资意义，但观察重点应从“有没有芯片”转向“整机系统能否按期交付，以及扩产是否开始快于需求”。

**趋势变化：** 本批次把供给问题从抽象的 CoWoS 紧缺细化为良率、ODM 调试、客户机房和融资结构四个可跟踪环节。

## 3. 技术侧

### 简单逻辑链

技术竞争按工作负载适配、性能与 TCO、软件生态、客户采用和平台格局逐级判断。GPU 与 ASIC 的竞争不是单颗芯片峰值比较，而是芯片、内存、互连、机架、编译器和调度软件共同决定的端到端结果。

### 逻辑节点与公司信息

#### 工作负载适配

GPU、云厂 ASIC 和其他加速器各自最适合哪些训练与推理任务？

**当前结论：** 定制 ASIC 在稳定推理和推荐任务上具有明确适配场景，GPU 则仍受益于快速变化的训练和通用任务；现有证据支持分工而非单一路线全面替代。

##### AMD

**截面变化与评估：** AMD在“工作负载适配”下，当前最重要的信息是：摩根大通认为 GPU 在整体 AI 加速器 TAM 中的占比可能由 2025 年约 85% 降至 2030 年 60%-70%，原因是定制 XPU/ASIC 增长更快；但 GPU 绝对市场仍可能以接近 40% 的复合增速扩张。技术替代更…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第2、4页，portfolio and accelerator mix） · 支持**：摩根大通认为 GPU 在整体 AI 加速器 TAM 中的占比可能由 2025 年约 85% 降至 2030 年 60%-70%，原因是定制 XPU/ASIC 增长更快；但 GPU 绝对市场仍可能以接近 40% 的复合增速扩张。技术替代更可能表现为份额稀释，而不是 GPU 需求收缩。 |

##### Meta

**截面变化与评估：** Meta在“工作负载适配”下，当前最重要的信息是：德银预计 Meta 会用 Iris/MTIA 内部芯片承接部分推理和推荐工作负载，以降低相对 merchant GPU 的单位算力成本；在合作方容量和自研芯片共同作用下，直接融资成本可能低于简单按新增 GW 外推。稳定、可控的推理任务是…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[德银-Meta：宏大野心需匹配宏大体量](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/德银-Meta（META.US）：宏大野心需匹配宏大体量-260724.pdf>) | 研报 | • **观点 1（第6页，internal Iris/MTIA roadmap） · 支持**：德银预计 Meta 会用 Iris/MTIA 内部芯片承接部分推理和推荐工作负载，以降低相对 merchant GPU 的单位算力成本；在合作方容量和自研芯片共同作用下，直接融资成本可能低于简单按新增 GW 外推。稳定、可控的推理任务是 ASIC 替代最明确的场景。 |

#### 端到端性能与 TCO

在同一工作负载下，哪条路线提供更好的性能、功耗和总拥有成本？

**当前结论：** AMD 和 TPU 路线均给出成本或性能优势，但分别来自厂商展示和分析师模型，且参数口径不可完全比较；当前不能据此确认端到端 TCO 领先。

##### AMD

**截面变化与评估：** AMD在“端到端性能与 TCO”下，当前最重要的信息是：Helios 由 72 颗 MI455X GPU、18 颗 EPYC Venice CPU 和 Pensando NIC 组成；AMD 声称凭借约 15% 更多计算、50% 更多 HBM 容量/带宽和 50% 更多横向扩展带宽，可较 N…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1页，Compute leadership: Helios） · 支持**：Helios 由 72 颗 MI455X GPU、18 颗 EPYC Venice CPU 和 Pensando NIC 组成；AMD 声称凭借约 15% 更多计算、50% 更多 HBM 容量/带宽和 50% 更多横向扩展带宽，可较 NVIDIA 提供最高约 30% 的每美元推理 token 优势。该结果是公司展示，尚非独立同工作负载基准。 |

##### Alphabet / Google

**截面变化与评估：** Alphabet / Google在“端到端性能与 TCO”下，当前最重要的信息是：巴克莱假设 Google 2026 年以约 2 万美元单价向 SPV 销售 TPU、硬件毛利率约 25%，每 GW 约容纳 70 万颗 TPU；与 GCP 租赁相比，外部 TPU 所有权模型提高客户资本支出和折旧，但给予更强控制权。该比…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第4、6页，Google's Unit Economics） · 支持**：巴克莱假设 Google 2026 年以约 2 万美元单价向 SPV 销售 TPU、硬件毛利率约 25%，每 GW 约容纳 70 万颗 TPU；与 GCP 租赁相比，外部 TPU 所有权模型提高客户资本支出和折旧，但给予更强控制权。该比较是分析师模型，关键参数需用实际合同验证。 |

##### NVIDIA

**截面变化与评估：** NVIDIA在“端到端性能与 TCO”下，当前最重要的信息是：Helios 由 72 颗 MI455X GPU、18 颗 EPYC Venice CPU 和 Pensando NIC 组成；AMD 声称凭借约 15% 更多计算、50% 更多 HBM 容量/带宽和 50% 更多横向扩展带宽，可较 N…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1页，Compute leadership: Helios） · 支持**：Helios 由 72 颗 MI455X GPU、18 颗 EPYC Venice CPU 和 Pensando NIC 组成；AMD 声称凭借约 15% 更多计算、50% 更多 HBM 容量/带宽和 50% 更多横向扩展带宽，可较 NVIDIA 提供最高约 30% 的每美元推理 token 优势。该结果是公司展示，尚非独立同工作负载基准。 |

#### 软件生态与迁移成本

编译器、框架、开发者和运维生态是否形成持续锁定或加速替代？

**当前结论：** ROCm 发布节奏和公司展示性能明显改善，表明 AMD 软件追赶加速；但仍缺少开发者采用、迁移时间和生产稳定性的第三方证据。

##### AMD

**截面变化与评估：** AMD在“软件生态与迁移成本”下，当前最重要的信息是：AMD 将 ROCm 发布周期由约四个月缩短到六周，并展示 coding agent 自动优化 MiniMax M3 在 MI355 上的内核后，token/s 提升 38%；公司还宣称相对 ROCm 7，DeepSeek 模型训练加速…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第2页，Open platforms: ROCm and ROCm.ai） · 支持**：AMD 将 ROCm 发布周期由约四个月缩短到六周，并展示 coding agent 自动优化 MiniMax M3 在 MI355 上的内核后，token/s 提升 38%；公司还宣称相对 ROCm 7，DeepSeek 模型训练加速 2.4 倍、推理加速 3.3 倍。软件迭代速度正在改善，但数据仍来自厂商演示。 |

#### 客户采用与量产

技术优势是否转化为生产部署、复购和规模量产？

**当前结论：** Helios 已进入量产计划，AMD 与 Cerebras 方案及外部 TPU 商业模式拓宽了客户选择；但采用仍多是计划、演示和带激励的生态扩张，复购尚未验证。

##### AMD

**截面变化与评估：** AMD在“客户采用与量产”下，当前最重要的信息是：AMD 与 Cerebras 宣布把 Helios 机架和晶圆级引擎组合成解耦推理方案，目标在超低延迟场景获得约 5 倍吞吐。它表明竞争单位正在从单颗 GPU 转为异构系统，但量产可用性和客户采用尚待验证。；Helios 已进入量产，计划 2026 年第三季度开始发货、第四季度爬坡。该进度支持 AMD 供给增加，但客户采用、ODM 调试和机房配套仍决定收入确认速度。。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1-2页，Cerebras disaggregated inference） · 支持**：AMD 与 Cerebras 宣布把 Helios 机架和晶圆级引擎组合成解耦推理方案，目标在超低延迟场景获得约 5 倍吞吐。它表明竞争单位正在从单颗 GPU 转为异构系统，但量产可用性和客户采用尚待验证。<br>• **观点 2（第1页，Compute leadership） · 支持**：Helios 已进入量产，计划 2026 年第三季度开始发货、第四季度爬坡。该进度支持 AMD 供给增加，但客户采用、ODM 调试和机房配套仍决定收入确认速度。<br>• **观点 3（第1页，Key Takeaways） · 支持**：摩根士丹利称 Helios 在关键客户处的采用进展顺利，客户证言显示 2027 年将强劲爬坡，并把 coding agent 视为 AMD GPU 生态采用的明确加速器；但该报告同时认为 AMD 本代产品仍未取得领导地位。 |

##### Alphabet / Google

**截面变化与评估：** Alphabet / Google在“客户采用与量产”下，当前最重要的信息是：Google 正尝试把 TPU 从 GCP 内的租赁资源变成可由外部 AI lab 通过 SPV 直接控制的 merchant product；客户获得更深的软件定制、纵向整合和独立于单一云协议的算力控制。这扩大了 ASIC 的可服务市…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第1-3页，Background on TPU-As-A-Service） · 支持**：Google 正尝试把 TPU 从 GCP 内的租赁资源变成可由外部 AI lab 通过 SPV 直接控制的 merchant product；客户获得更深的软件定制、纵向整合和独立于单一云协议的算力控制。这扩大了 ASIC 的可服务市场，也使其开始正面争夺 NVIDIA 的外部计算需求。 |

##### Cerebras

**截面变化与评估：** Cerebras在“客户采用与量产”下，当前最重要的信息是：AMD 与 Cerebras 宣布把 Helios 机架和晶圆级引擎组合成解耦推理方案，目标在超低延迟场景获得约 5 倍吞吐。它表明竞争单位正在从单颗 GPU 转为异构系统，但量产可用性和客户采用尚待验证。。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1-2页，Cerebras disaggregated inference） · 支持**：AMD 与 Cerebras 宣布把 Helios 机架和晶圆级引擎组合成解耦推理方案，目标在超低延迟场景获得约 5 倍吞吐。它表明竞争单位正在从单颗 GPU 转为异构系统，但量产可用性和客户采用尚待验证。 |

##### NVIDIA

**截面变化与评估：** NVIDIA在“客户采用与量产”下，当前最重要的信息是：Google 正尝试把 TPU 从 GCP 内的租赁资源变成可由外部 AI lab 通过 SPV 直接控制的 merchant product；客户获得更深的软件定制、纵向整合和独立于单一云协议的算力控制。这扩大了 ASIC 的可服务市…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第1-3页，Background on TPU-As-A-Service） · 支持**：Google 正尝试把 TPU 从 GCP 内的租赁资源变成可由外部 AI lab 通过 SPV 直接控制的 merchant product；客户获得更深的软件定制、纵向整合和独立于单一云协议的算力控制。这扩大了 ASIC 的可服务市场，也使其开始正面争夺 NVIDIA 的外部计算需求。 |

##### ODM / 系统集成商

**截面变化与评估：** ODM / 系统集成商在“客户采用与量产”下，当前最重要的信息是：Helios 已进入量产，计划 2026 年第三季度开始发货、第四季度爬坡。该进度支持 AMD 供给增加，但客户采用、ODM 调试和机房配套仍决定收入确认速度。。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1页，Compute leadership） · 支持**：Helios 已进入量产，计划 2026 年第三季度开始发货、第四季度爬坡。该进度支持 AMD 供给增加，但客户采用、ODM 调试和机房配套仍决定收入确认速度。 |

##### 数据中心客户

**截面变化与评估：** 数据中心客户在“客户采用与量产”下，当前最重要的信息是：Helios 已进入量产，计划 2026 年第三季度开始发货、第四季度爬坡。该进度支持 AMD 供给增加，但客户采用、ODM 调试和机房配套仍决定收入确认速度。。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1页，Compute leadership） · 支持**：Helios 已进入量产，计划 2026 年第三季度开始发货、第四季度爬坡。该进度支持 AMD 供给增加，但客户采用、ODM 调试和机房配套仍决定收入确认速度。 |

#### 平台格局与替代路径

竞争单位转向平台后，GPU 与定制 ASIC 的份额和价值捕获如何变化？

**当前结论：** 定制 ASIC 正从内部自用向外部销售扩展，GPU 份额可能下降但绝对市场仍增长；Intel 先进代工尚未形成外部规模，当前更可能是 NVIDIA 平台主导下的多路线增量竞争。

##### AMD

**截面变化与评估：** AMD在“平台格局与替代路径”下，当前最重要的信息是：摩根大通认为 GPU 在整体 AI 加速器 TAM 中的占比可能由 2025 年约 85% 降至 2030 年 60%-70%，原因是定制 XPU/ASIC 增长更快；但 GPU 绝对市场仍可能以接近 40% 的复合增速扩张。技术替代更…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第2、4页，portfolio and accelerator mix） · 支持**：摩根大通认为 GPU 在整体 AI 加速器 TAM 中的占比可能由 2025 年约 85% 降至 2030 年 60%-70%，原因是定制 XPU/ASIC 增长更快；但 GPU 绝对市场仍可能以接近 40% 的复合增速扩张。技术替代更可能表现为份额稀释，而不是 GPU 需求收缩。 |

##### Alphabet / Google

**截面变化与评估：** Alphabet / Google在“平台格局与替代路径”下，当前最重要的信息是：Google 正尝试把 TPU 从 GCP 内的租赁资源变成可由外部 AI lab 通过 SPV 直接控制的 merchant product；客户获得更深的软件定制、纵向整合和独立于单一云协议的算力控制。这扩大了 ASIC 的可服务市…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第1-3页，Background on TPU-As-A-Service） · 支持**：Google 正尝试把 TPU 从 GCP 内的租赁资源变成可由外部 AI lab 通过 SPV 直接控制的 merchant product；客户获得更深的软件定制、纵向整合和独立于单一云协议的算力控制。这扩大了 ASIC 的可服务市场，也使其开始正面争夺 NVIDIA 的外部计算需求。 |

##### Intel

**截面变化与评估：** Intel在“平台格局与替代路径”下，当前最重要的信息是：Intel 18A 产出环比增长超过 50% 且高于内部目标约 25%，但外部代工收入仅占该分部约 5%；摩根大通预计即使少量 AI 项目采用 Intel，TSMC 在先进前道晶圆仍保持 95% 以上份额。技术可行不等于已形成外部客户规…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：PC 与服务器传导分析](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-PC与服务器：英特尔2026年二季度财报及AMD“Advancing AI 2026”大会传导分析-260724.pdf>) | 研报 | • **观点 1（第2页，18A output and 14A roadmap） · 支持**：Intel 18A 产出环比增长超过 50% 且高于内部目标约 25%，但外部代工收入仅占该分部约 5%；摩根大通预计即使少量 AI 项目采用 Intel，TSMC 在先进前道晶圆仍保持 95% 以上份额。技术可行不等于已形成外部客户规模。 |

##### NVIDIA

**截面变化与评估：** NVIDIA在“平台格局与替代路径”下，当前最重要的信息是：Google 正尝试把 TPU 从 GCP 内的租赁资源变成可由外部 AI lab 通过 SPV 直接控制的 merchant product；客户获得更深的软件定制、纵向整合和独立于单一云协议的算力控制。这扩大了 ASIC 的可服务市…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第1-3页，Background on TPU-As-A-Service） · 支持**：Google 正尝试把 TPU 从 GCP 内的租赁资源变成可由外部 AI lab 通过 SPV 直接控制的 merchant product；客户获得更深的软件定制、纵向整合和独立于单一云协议的算力控制。这扩大了 ASIC 的可服务市场，也使其开始正面争夺 NVIDIA 的外部计算需求。 |

##### TSMC

**截面变化与评估：** TSMC在“平台格局与替代路径”下，当前最重要的信息是：Intel 18A 产出环比增长超过 50% 且高于内部目标约 25%，但外部代工收入仅占该分部约 5%；摩根大通预计即使少量 AI 项目采用 Intel，TSMC 在先进前道晶圆仍保持 95% 以上份额。技术可行不等于已形成外部客户规…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：PC 与服务器传导分析](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-PC与服务器：英特尔2026年二季度财报及AMD“Advancing AI 2026”大会传导分析-260724.pdf>) | 研报 | • **观点 1（第2页，18A output and 14A roadmap） · 支持**：Intel 18A 产出环比增长超过 50% 且高于内部目标约 25%，但外部代工收入仅占该分部约 5%；摩根大通预计即使少量 AI 项目采用 Intel，TSMC 在先进前道晶圆仍保持 95% 以上份额。技术可行不等于已形成外部客户规模。 |


### 最新结论与趋势

技术竞争的单位已经不是单颗 GPU，而是芯片、HBM、互连、机架、编译器和调度软件组成的系统。AMD 用 Helios 和更快的 ROCm 迭代缩小平台差距，但本批次性能数字大多来自厂商展示，且摩根士丹利仍认为其本代产品没有取得领导地位。更重要的结构变化来自 Google TPU：通过 Broadcom 设计、TSMC 制造和 SPV 融资，ASIC 正由云内自用产品变成可被外部 AI lab 控制的商品化算力。当前判断为：GPU 在变化快、通用性强的工作负载上仍占主导，ASIC 会在稳定、规模化、客户可控制软件栈的推理任务中更快夺取份额；这更像分层共存和 GPU 份额稀释，而不是 GPU 绝对需求下降。

**趋势变化：** 相较旧的 GPU 对 GPU 比较，本批次最值得记录的是“外部 merchant ASIC”与“异构机架系统”两条技术商业化路线。

## 4. 估值侧

### 简单逻辑链

估值从基本面盈利路径、市场共识、股价隐含预期、盈利修正和上下行赔率五层判断。产业增长不自动等于证券有赔率；只有盈利上修速度超过已计入预期，并且下行可被监控，才可能形成可行动结论。

### 逻辑节点与公司信息

#### 基本面盈利路径

GPU/ASIC 敞口如何转化为公司收入、毛利、自由现金流和每股收益？

**当前结论：** 外部 TPU 情景可能大幅提高 Alphabet 收入和毛利，但资本开支也可能压低自由现金流；AMD 收入增长还可能被客户认股权证稀释。现有材料揭示盈利桥的两端，却没有形成可复现的公司模型。

##### AMD

**截面变化与评估：** AMD在“基本面盈利路径”下，当前最重要的信息是：摩根士丹利把 AMD 向客户发行的大额认股权证视为营销费用，认为其可能抵消未来数年 GPU 业务的大部分利润。即使收入增长，股东可获得的盈利弹性仍可能被获客成本和稀释削弱。。综合这些材料，该实体对本节点的截面影响为负向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第3页，Thoughts on the stock） · 反证**：摩根士丹利把 AMD 向客户发行的大额认股权证视为营销费用，认为其可能抵消未来数年 GPU 业务的大部分利润。即使收入增长，股东可获得的盈利弹性仍可能被获客成本和稀释削弱。 |

##### Alphabet / Google

**截面变化与评估：** Alphabet / Google在“基本面盈利路径”下，当前最重要的信息是：巴克莱的高情景把 2028 年外部 TPU 收入估至 2,527 亿美元、毛利 632 亿美元，并把 Alphabet 2028 年收入预测上调 40%；但同一模型预计 2027-2028 年资本开支约 3,500 亿和 5,003 亿…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第5、7、11页，estimate changes and company model） · 支持**：巴克莱的高情景把 2028 年外部 TPU 收入估至 2,527 亿美元、毛利 632 亿美元，并把 Alphabet 2028 年收入预测上调 40%；但同一模型预计 2027-2028 年资本开支约 3,500 亿和 5,003 亿美元、自由现金流转负。利润上修与资本强度必须同时计价。 |

#### 市场一致预期

市场当前对收入、利润、份额和资本开支的主流预期是什么？

**当前结论：** 多家投行已在目标价和长期情景中计入 AI 加速器、TPU、Meta 算力和 AMD 产品改善，说明主题并非未被市场发现；但公司间看法分化显著。

##### AMD

**截面变化与评估：** AMD在“市场一致预期”下，当前最重要的信息是：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更…；摩根大通维持 AMD Neutral，2026 年 12 月目标价 385 美元，而报告股价为 552.33 美元；目标价基于约 35 倍市盈率和约 11 美元的 2026 年末盈利能力。报告认可产品改善，但认为长期份额不确定、研发投入…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第1、5页，rating and valuation） · 支持**：摩根大通维持 AMD Neutral，2026 年 12 月目标价 385 美元，而报告股价为 552.33 美元；目标价基于约 35 倍市盈率和约 11 美元的 2026 年末盈利能力。报告认可产品改善，但认为长期份额不确定、研发投入高且股价接近充分定价。 |
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1、3页，rating table and Thoughts on the stock） · 支持**：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更好的选择在别处。 |

##### Alphabet / Google

**截面变化与评估：** Alphabet / Google在“市场一致预期”下，当前最重要的信息是：巴克莱的高情景把 2028 年外部 TPU 收入估至 2,527 亿美元、毛利 632 亿美元，并把 Alphabet 2028 年收入预测上调 40%；但同一模型预计 2027-2028 年资本开支约 3,500 亿和 5,003 亿…；巴克莱维持 Alphabet Overweight 和 425 美元目标价，对应 2026 年 7 月 23 日 317.69 美元股价约 34% 潜在空间；目标价取 2027 年 25 倍 EPS 与 15 倍 EBITDA 的平均结…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第5、7、11页，estimate changes and company model） · 支持**：巴克莱的高情景把 2028 年外部 TPU 收入估至 2,527 亿美元、毛利 632 亿美元，并把 Alphabet 2028 年收入预测上调 40%；但同一模型预计 2027-2028 年资本开支约 3,500 亿和 5,003 亿美元、自由现金流转负。利润上修与资本强度必须同时计价。<br>• **观点 2（第1、8页，rating and valuation worksheet） · 支持**：巴克莱维持 Alphabet Overweight 和 425 美元目标价，对应 2026 年 7 月 23 日 317.69 美元股价约 34% 潜在空间；目标价取 2027 年 25 倍 EPS 与 15 倍 EBITDA 的平均结果。赔率来自 TPU 外部商业化和云利润上修，而非纯 GPU 敞口。 |

##### Meta

**截面变化与评估：** Meta在“市场一致预期”下，当前最重要的信息是：Meta 2026 年资本开支指引为 1,250 亿至 1,450 亿美元；德银称市场已把 2027 年约 14GW 容量对应的资本开支预期推至 2,000 亿美元低至中段，并给出 2027 年约 2,100 亿至 2,150 亿美元、…；德银维持 Meta Buy，将目标价由 810 美元小幅下调至 800 美元；相对 2026 年 7 月 23 日 606.10 美元股价仍有约 32% 空间。估值基于 24 倍 2027 年 GAAP EPS，核心假设是广告回报已覆盖…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[德银-Meta：宏大野心需匹配宏大体量](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/德银-Meta（META.US）：宏大野心需匹配宏大体量-260724.pdf>) | 研报 | • **观点 1（第2页，Capex remains a key debate） · 支持**：Meta 2026 年资本开支指引为 1,250 亿至 1,450 亿美元；德银称市场已把 2027 年约 14GW 容量对应的资本开支预期推至 2,000 亿美元低至中段，并给出 2027 年约 2,100 亿至 2,150 亿美元、2028 年约 2,650 亿美元的估计。这是大型客户继续扩大 AI 算力采购的直接预算信号，但后两项属于分析师估计。<br>• **观点 2（第1-2页，rating and valuation） · 支持**：德银维持 Meta Buy，将目标价由 810 美元小幅下调至 800 美元；相对 2026 年 7 月 23 日 606.10 美元股价仍有约 32% 空间。估值基于 24 倍 2027 年 GAAP EPS，核心假设是广告回报已覆盖部分 AI 投入，订阅和云基础设施提供额外变现。 |

##### Broadcom

**截面变化与评估：** Broadcom在“市场一致预期”下，当前最重要的信息是：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1、3页，rating table and Thoughts on the stock） · 支持**：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更好的选择在别处。 |

##### NVIDIA

**截面变化与评估：** NVIDIA在“市场一致预期”下，当前最重要的信息是：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1、3页，rating table and Thoughts on the stock） · 支持**：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更好的选择在别处。 |

#### 股价隐含预期

当前股价要求公司实现怎样的增长、份额和利润率路径？

**当前结论：** AMD 的现价高于两份机构目标价，Alphabet 和 Meta 则仍有目标价上行空间；但目标价不是股价隐含预期，当前尚无反向 DCF 或隐含份额路径。

##### AMD

**截面变化与评估：** AMD在“股价隐含预期”下，当前最重要的信息是：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更…；摩根大通维持 AMD Neutral，2026 年 12 月目标价 385 美元，而报告股价为 552.33 美元；目标价基于约 35 倍市盈率和约 11 美元的 2026 年末盈利能力。报告认可产品改善，但认为长期份额不确定、研发投入…。综合这些材料，该实体对本节点的截面影响为负向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第1、5页，rating and valuation） · 反证**：摩根大通维持 AMD Neutral，2026 年 12 月目标价 385 美元，而报告股价为 552.33 美元；目标价基于约 35 倍市盈率和约 11 美元的 2026 年末盈利能力。报告认可产品改善，但认为长期份额不确定、研发投入高且股价接近充分定价。 |
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1、3页，rating table and Thoughts on the stock） · 反证**：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更好的选择在别处。 |

##### Alphabet / Google

**截面变化与评估：** Alphabet / Google在“股价隐含预期”下，当前最重要的信息是：巴克莱的高情景把 2028 年外部 TPU 收入估至 2,527 亿美元、毛利 632 亿美元，并把 Alphabet 2028 年收入预测上调 40%；但同一模型预计 2027-2028 年资本开支约 3,500 亿和 5,003 亿…；巴克莱维持 Alphabet Overweight 和 425 美元目标价，对应 2026 年 7 月 23 日 317.69 美元股价约 34% 潜在空间；目标价取 2027 年 25 倍 EPS 与 15 倍 EBITDA 的平均结…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第5、7、11页，estimate changes and company model） · 线索**：巴克莱的高情景把 2028 年外部 TPU 收入估至 2,527 亿美元、毛利 632 亿美元，并把 Alphabet 2028 年收入预测上调 40%；但同一模型预计 2027-2028 年资本开支约 3,500 亿和 5,003 亿美元、自由现金流转负。利润上修与资本强度必须同时计价。<br>• **观点 2（第1、8页，rating and valuation worksheet） · 支持**：巴克莱维持 Alphabet Overweight 和 425 美元目标价，对应 2026 年 7 月 23 日 317.69 美元股价约 34% 潜在空间；目标价取 2027 年 25 倍 EPS 与 15 倍 EBITDA 的平均结果。赔率来自 TPU 外部商业化和云利润上修，而非纯 GPU 敞口。 |

##### Meta

**截面变化与评估：** Meta在“股价隐含预期”下，当前最重要的信息是：德银明确指出 2027 容量、每 GW 成本、利用率、定价和客户需求均有高度不确定性，第三方云收入尚未正式宣布，也未进入其当前盈利预测。把潜在算力销售直接资本化会高估已验证价值。；德银维持 Meta Buy，将目标价由 810 美元小幅下调至 800 美元；相对 2026 年 7 月 23 日 606.10 美元股价仍有约 32% 空间。估值基于 24 倍 2027 年 GAAP EPS，核心假设是广告回报已覆盖…。综合这些材料，该实体对本节点的截面影响为多空并存；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[德银-Meta：宏大野心需匹配宏大体量](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/德银-Meta（META.US）：宏大野心需匹配宏大体量-260724.pdf>) | 研报 | • **观点 1（第1-2页，rating and valuation） · 支持**：德银维持 Meta Buy，将目标价由 810 美元小幅下调至 800 美元；相对 2026 年 7 月 23 日 606.10 美元股价仍有约 32% 空间。估值基于 24 倍 2027 年 GAAP EPS，核心假设是广告回报已覆盖部分 AI 投入，订阅和云基础设施提供额外变现。<br>• **观点 2（第5-6页，cloud sales and capex expectations） · 反证**：德银明确指出 2027 容量、每 GW 成本、利用率、定价和客户需求均有高度不确定性，第三方云收入尚未正式宣布，也未进入其当前盈利预测。把潜在算力销售直接资本化会高估已验证价值。 |

##### Broadcom

**截面变化与评估：** Broadcom在“股价隐含预期”下，当前最重要的信息是：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更…。综合这些材料，该实体对本节点的截面影响为负向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1、3页，rating table and Thoughts on the stock） · 反证**：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更好的选择在别处。 |

##### NVIDIA

**截面变化与评估：** NVIDIA在“股价隐含预期”下，当前最重要的信息是：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更…。综合这些材料，该实体对本节点的截面影响为负向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1、3页，rating table and Thoughts on the stock） · 反证**：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更好的选择在别处。 |

#### 盈利修正与预期差

新信息是否使基本面上修速度快于市场预期和估值扩张？

**当前结论：** 现有报告包含单次目标价和模型调整，但没有连续历史序列，无法判断盈利上修是否持续快于估值扩张。

当前没有映射到具体公司或实体的材料。

#### 上下行赔率与动作

综合情景概率后，上行、下行和可监控性是否支持行动？

**当前结论：** 机构对 Alphabet、Meta 仍给出约三成目标价空间，而 AMD 的报告股价显著高于两家机构目标价；这提示赔率应按公司而非按主题判断。由于缺少统一盈利桥、反向估值和概率情景，当前只支持观察。

##### AMD

**截面变化与评估：** AMD在“上下行赔率与动作”下，当前最重要的信息是：摩根士丹利把 AMD 向客户发行的大额认股权证视为营销费用，认为其可能抵消未来数年 GPU 业务的大部分利润。即使收入增长，股东可获得的盈利弹性仍可能被获客成本和稀释削弱。；摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更…。综合这些材料，该实体对本节点的截面影响为负向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根大通：AMD AAI26 大会纪要](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/摩根大通-超微半导体（AMD.US）AAI26大会纪要：AI与CPU总可寻址市场（TAM）预期上调，MI450与Helios机柜放量在即，AI版图持续拓宽；借CPU东风追赶GPU龙头-260724.pdf>) | 研报 | • **观点 1（第1、5页，rating and valuation） · 反证**：摩根大通维持 AMD Neutral，2026 年 12 月目标价 385 美元，而报告股价为 552.33 美元；目标价基于约 35 倍市盈率和约 11 美元的 2026 年末盈利能力。报告认可产品改善，但认为长期份额不确定、研发投入高且股价接近充分定价。 |
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1、3页，rating table and Thoughts on the stock） · 反证**：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更好的选择在别处。<br>• **观点 2（第3页，Thoughts on the stock） · 反证**：摩根士丹利把 AMD 向客户发行的大额认股权证视为营销费用，认为其可能抵消未来数年 GPU 业务的大部分利润。即使收入增长，股东可获得的盈利弹性仍可能被获客成本和稀释削弱。 |

##### Meta

**截面变化与评估：** Meta在“上下行赔率与动作”下，当前最重要的信息是：德银明确指出 2027 容量、每 GW 成本、利用率、定价和客户需求均有高度不确定性，第三方云收入尚未正式宣布，也未进入其当前盈利预测。把潜在算力销售直接资本化会高估已验证价值。；德银维持 Meta Buy，将目标价由 810 美元小幅下调至 800 美元；相对 2026 年 7 月 23 日 606.10 美元股价仍有约 32% 空间。估值基于 24 倍 2027 年 GAAP EPS，核心假设是广告回报已覆盖…。综合这些材料，该实体对本节点的截面影响为多空并存；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[德银-Meta：宏大野心需匹配宏大体量](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/德银-Meta（META.US）：宏大野心需匹配宏大体量-260724.pdf>) | 研报 | • **观点 1（第5-6页，cloud sales and capex expectations） · 反证**：德银明确指出 2027 容量、每 GW 成本、利用率、定价和客户需求均有高度不确定性，第三方云收入尚未正式宣布，也未进入其当前盈利预测。把潜在算力销售直接资本化会高估已验证价值。<br>• **观点 2（第1-2页，rating and valuation） · 支持**：德银维持 Meta Buy，将目标价由 810 美元小幅下调至 800 美元；相对 2026 年 7 月 23 日 606.10 美元股价仍有约 32% 空间。估值基于 24 倍 2027 年 GAAP EPS，核心假设是广告回报已覆盖部分 AI 投入，订阅和云基础设施提供额外变现。 |

##### Alphabet / Google

**截面变化与评估：** Alphabet / Google在“上下行赔率与动作”下，当前最重要的信息是：巴克莱维持 Alphabet Overweight 和 425 美元目标价，对应 2026 年 7 月 23 日 317.69 美元股价约 34% 潜在空间；目标价取 2027 年 25 倍 EPS 与 15 倍 EBITDA 的平均结…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第1、8页，rating and valuation worksheet） · 支持**：巴克莱维持 Alphabet Overweight 和 425 美元目标价，对应 2026 年 7 月 23 日 317.69 美元股价约 34% 潜在空间；目标价取 2027 年 25 倍 EPS 与 15 倍 EBITDA 的平均结果。赔率来自 TPU 外部商业化和云利润上修，而非纯 GPU 敞口。 |

##### Broadcom

**截面变化与评估：** Broadcom在“上下行赔率与动作”下，当前最重要的信息是：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更…。综合这些材料，该实体对本节点的截面影响为负向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1、3页，rating table and Thoughts on the stock） · 反证**：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更好的选择在别处。 |

##### NVIDIA

**截面变化与评估：** NVIDIA在“上下行赔率与动作”下，当前最重要的信息是：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更…。综合这些材料，该实体对本节点的截面影响为负向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第1、3页，rating table and Thoughts on the stock） · 反证**：摩根士丹利维持 AMD Equal-weight，目标价 410 美元，而 2026 年 7 月 23 日股价为 539.69 美元；报告认为 AMD 叙事改善，但相对 NVIDIA、Broadcom 估值更贵且缺少类似期权，风险收益更好的选择在别处。 |


### 最新结论与趋势

本批次最大的预期差不在产业方向，而在证券价格。两家投行都认可 AMD 的产品和需求改善，却分别给出 385 美元和 410 美元目标价，显著低于报告截面 539.69-552.33 美元的股价；原因包括高估值、长期份额仍不确定、研发投入和客户认股权证侵蚀股东收益。相对而言，巴克莱对 Alphabet 给出约 34% 目标空间，德银对 Meta 给出约 32% 空间，但两者的 AI 赔率来自广告、云和基础设施综合变现，并非纯 GPU/ASIC 暴露。当前判断为：产业需求可以继续强，但 AMD 已被要求以更快盈利兑现来消化价格；GOOGL/META 的赔率更好，却需要接受更低的纯加速器盈利弹性。

**趋势变化：** 本批次首次把产业乐观和证券谨慎同时放在同一截面：需求预测继续上修，但 AMD 的投行目标价反而明显低于现价。

## 5. ESG

### 简单逻辑链

ESG 只研究会改变可交付算力、可服务市场、资本成本和股东回报的约束：能源与水、出口与市场准入、供应和客户集中、治理与资本配置、融资和长期承诺。

### 逻辑节点与公司信息

#### 能源、水与基础设施许可

绝对用电、用水和许可是否限制 GPU/ASIC 部署或推高成本？

**当前结论：** 当前材料没有直接量化 GPU/ASIC 部署的能源、水和许可约束，不能形成结论。

当前没有映射到具体公司或实体的材料。

#### 出口管制与市场准入

出口限制和本地化要求如何改变可服务市场与库存风险？

**当前结论：** 当前材料没有覆盖出口管制、受限收入和替代产品影响，不能形成结论。

当前没有映射到具体公司或实体的材料。

#### 供应与客户集中

关键供应商、客户和地区集中是否放大经营波动？

**当前结论：** 现有材料提及 Google、Broadcom、TSMC 及少数大型客户，但没有系统量化供应商、客户和地区集中度。

当前没有映射到具体公司或实体的材料。

#### 治理与资本配置

补贴、认股权证、并购和关联投资是否损害股东获得的盈利弹性？

**当前结论：** AMD 以客户认股权证推动采用被投行视为高额获客费用，可能显著稀释 GPU 业务未来利润；这是已识别但尚未量化到每股价值的治理风险。

##### AMD

**截面变化与评估：** AMD在“治理与资本配置”下，当前最重要的信息是：摩根士丹利把 AMD 向客户发行的大额认股权证视为营销费用，认为其可能抵消未来数年 GPU 业务的大部分利润。即使收入增长，股东可获得的盈利弹性仍可能被获客成本和稀释削弱。；AMD 通过向客户发行认股权证支持生态采用，摩根士丹利认为这相当于高额获客费用，并可能显著稀释 GPU 业务未来利润。它属于资本配置和股东利益问题，而非单纯产品销量问题。。综合这些材料，该实体对本节点的截面影响为负向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[摩根士丹利：AMD AI 技术发布会复盘](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/大摩-超威半导体（AMD.US）：AMD AI 技术发布会复盘及核心观点-260724.pdf>) | 研报 | • **观点 1（第3页，Thoughts on the stock） · 反证**：摩根士丹利把 AMD 向客户发行的大额认股权证视为营销费用，认为其可能抵消未来数年 GPU 业务的大部分利润。即使收入增长，股东可获得的盈利弹性仍可能被获客成本和稀释削弱。<br>• **观点 2（第3页，customer warrants） · 反证**：AMD 通过向客户发行认股权证支持生态采用，摩根士丹利认为这相当于高额获客费用，并可能显著稀释 GPU 业务未来利润。它属于资本配置和股东利益问题，而非单纯产品销量问题。 |

#### 融资结构与长期承诺

SPV、租赁、采购承诺和表外融资把风险留给谁？

**当前结论：** TPU 和 Meta 扩产越来越依赖 SPV、合作方融资、采购承诺与潜在担保。结构可释放资本，但风险承担和资产利用率透明度下降，应视为需求融资能力与尾部风险的共同变量。

##### Alphabet / Google

**截面变化与评估：** Alphabet / Google在“融资结构与长期承诺”下，当前最重要的信息是：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给…；TPU 即服务依赖 Apollo/Blackstone 融资 SPV、Google/Broadcom 硬件和数据中心运营商的多层结构；巴克莱同时引用 Alphabet 约 8,110 亿美元采购承诺。结构可加快扩张，但会增加对手方、担保…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2-4页，TPU-aaS entity structure and unit economics） · 线索**：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给，也引入跨主体执行和融资风险。<br>• **观点 2（第1-3、7页，TPU-aaS SPV and purchase commitments） · 支持**：TPU 即服务依赖 Apollo/Blackstone 融资 SPV、Google/Broadcom 硬件和数据中心运营商的多层结构；巴克莱同时引用 Alphabet 约 8,110 亿美元采购承诺。结构可加快扩张，但会增加对手方、担保、资产利用率和表外义务的透明度风险。 |

##### Apollo

**截面变化与评估：** Apollo在“融资结构与长期承诺”下，当前最重要的信息是：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给…；TPU 即服务依赖 Apollo/Blackstone 融资 SPV、Google/Broadcom 硬件和数据中心运营商的多层结构；巴克莱同时引用 Alphabet 约 8,110 亿美元采购承诺。结构可加快扩张，但会增加对手方、担保…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2-4页，TPU-aaS entity structure and unit economics） · 线索**：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给，也引入跨主体执行和融资风险。<br>• **观点 2（第1-3、7页，TPU-aaS SPV and purchase commitments） · 支持**：TPU 即服务依赖 Apollo/Blackstone 融资 SPV、Google/Broadcom 硬件和数据中心运营商的多层结构；巴克莱同时引用 Alphabet 约 8,110 亿美元采购承诺。结构可加快扩张，但会增加对手方、担保、资产利用率和表外义务的透明度风险。 |

##### Blackstone

**截面变化与评估：** Blackstone在“融资结构与长期承诺”下，当前最重要的信息是：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给…；TPU 即服务依赖 Apollo/Blackstone 融资 SPV、Google/Broadcom 硬件和数据中心运营商的多层结构；巴克莱同时引用 Alphabet 约 8,110 亿美元采购承诺。结构可加快扩张，但会增加对手方、担保…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2-4页，TPU-aaS entity structure and unit economics） · 线索**：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给，也引入跨主体执行和融资风险。<br>• **观点 2（第1-3、7页，TPU-aaS SPV and purchase commitments） · 支持**：TPU 即服务依赖 Apollo/Blackstone 融资 SPV、Google/Broadcom 硬件和数据中心运营商的多层结构；巴克莱同时引用 Alphabet 约 8,110 亿美元采购承诺。结构可加快扩张，但会增加对手方、担保、资产利用率和表外义务的透明度风险。 |

##### Broadcom

**截面变化与评估：** Broadcom在“融资结构与长期承诺”下，当前最重要的信息是：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给…；TPU 即服务依赖 Apollo/Blackstone 融资 SPV、Google/Broadcom 硬件和数据中心运营商的多层结构；巴克莱同时引用 Alphabet 约 8,110 亿美元采购承诺。结构可加快扩张，但会增加对手方、担保…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2-4页，TPU-aaS entity structure and unit economics） · 线索**：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给，也引入跨主体执行和融资风险。<br>• **观点 2（第1-3、7页，TPU-aaS SPV and purchase commitments） · 支持**：TPU 即服务依赖 Apollo/Blackstone 融资 SPV、Google/Broadcom 硬件和数据中心运营商的多层结构；巴克莱同时引用 Alphabet 约 8,110 亿美元采购承诺。结构可加快扩张，但会增加对手方、担保、资产利用率和表外义务的透明度风险。 |

##### Hyperion

**截面变化与评估：** Hyperion在“融资结构与长期承诺”下，当前最重要的信息是：Meta 的容量情景由 7GW 升至 14GW，资本开支预期可能升至 2027 年 2,000 亿美元以上；Hyperion 等伙伴融资可能降低报表内直接负担。对治理分析而言，关键不是只看名义 capex，而是追踪担保、租赁、合作方承诺…；若 Meta 容量由 2026 年约 7GW 增至 2027 年 14GW，Hyperion 等合作方可能提供 1.0-1.5GW，使 Meta 直接融资的新增容量约为 5.5GW。伙伴资本可以缓解资产负担，但不能消除电力、服务器和建设…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[德银-Meta：宏大野心需匹配宏大体量](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/德银-Meta（META.US）：宏大野心需匹配宏大体量-260724.pdf>) | 研报 | • **观点 1（第5-6页，2027 capex expectations） · 线索**：若 Meta 容量由 2026 年约 7GW 增至 2027 年 14GW，Hyperion 等合作方可能提供 1.0-1.5GW，使 Meta 直接融资的新增容量约为 5.5GW。伙伴资本可以缓解资产负担，但不能消除电力、服务器和建设交付约束。<br>• **观点 2（第2、5-6页，capacity and funding structure） · 支持**：Meta 的容量情景由 7GW 升至 14GW，资本开支预期可能升至 2027 年 2,000 亿美元以上；Hyperion 等伙伴融资可能降低报表内直接负担。对治理分析而言，关键不是只看名义 capex，而是追踪担保、租赁、合作方承诺及最终风险承担者。 |

##### Meta

**截面变化与评估：** Meta在“融资结构与长期承诺”下，当前最重要的信息是：Meta 的容量情景由 7GW 升至 14GW，资本开支预期可能升至 2027 年 2,000 亿美元以上；Hyperion 等伙伴融资可能降低报表内直接负担。对治理分析而言，关键不是只看名义 capex，而是追踪担保、租赁、合作方承诺…；若 Meta 容量由 2026 年约 7GW 增至 2027 年 14GW，Hyperion 等合作方可能提供 1.0-1.5GW，使 Meta 直接融资的新增容量约为 5.5GW。伙伴资本可以缓解资产负担，但不能消除电力、服务器和建设…。综合这些材料，该实体对本节点的截面影响为正向；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[德银-Meta：宏大野心需匹配宏大体量](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/德银-Meta（META.US）：宏大野心需匹配宏大体量-260724.pdf>) | 研报 | • **观点 1（第5-6页，2027 capex expectations） · 线索**：若 Meta 容量由 2026 年约 7GW 增至 2027 年 14GW，Hyperion 等合作方可能提供 1.0-1.5GW，使 Meta 直接融资的新增容量约为 5.5GW。伙伴资本可以缓解资产负担，但不能消除电力、服务器和建设交付约束。<br>• **观点 2（第2、5-6页，capacity and funding structure） · 支持**：Meta 的容量情景由 7GW 升至 14GW，资本开支预期可能升至 2027 年 2,000 亿美元以上；Hyperion 等伙伴融资可能降低报表内直接负担。对治理分析而言，关键不是只看名义 capex，而是追踪担保、租赁、合作方承诺及最终风险承担者。 |

##### TSMC

**截面变化与评估：** TSMC在“融资结构与长期承诺”下，当前最重要的信息是：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给…。综合这些材料，该实体对本节点的截面影响为尚不明确；方向可由下方支持与反证观点逐项核对。

**相较上一截面：** 首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。

| 材料（含链接） | 类型 | 观点列表 |
|---|---|---|
| 2026-07-24<br>[巴克莱：拆解 TPU 即服务](</Users/bytedance/Desktop/vk/value_invest/research/bom/gpu_asic_bom_live/source/ima/2026/07/24/巴克莱-Alphabet（GOOGL.US）：拆解“TPU即服务”-260724.pdf>) | 研报 | • **观点 1（第2-4页，TPU-aaS entity structure and unit economics） · 线索**：外部 TPU 由 Google 与 Broadcom 协同设计、TSMC 制造，再由 Apollo/Blackstone 融资的 SPV 购买并交给数据中心运营商管理。这个结构把芯片设计、晶圆制造、资本和机房交付绑定在一起，可扩大供给，也引入跨主体执行和融资风险。 |


### 最新结论与趋势

这批研报没有提供足够的用电、水耗、出口管制或供应地缘数据，不能据此形成完整 ESG 结论；但资本配置和治理风险已经很清楚。Meta 和 Google 的算力扩张越来越依赖数千亿美元采购承诺、合作方融资和 SPV，AMD 又通过客户认股权证换取生态采用。真正需要跟踪的是谁承担最终资本义务、资产闲置时损失落在哪里、认股权证如何稀释利润，以及伙伴融资是否让风险移出表面口径。当前判断为：治理和融资结构是已验证风险，环境与监管维度仍属本批次证据缺口，不应被空白材料自动判为低风险。

**趋势变化：** 本批次新增的是对伙伴融资、采购承诺和客户认股权证的治理映射；环境与出口管制没有新增可核验数据。
