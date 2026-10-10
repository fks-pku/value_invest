**截至 2026 年 10 月 9 日，与 Meta 的 CPU 需求有明确业务联系的核心公司是 AMD、NVIDIA、Arm 和亚马逊 AWS；台积电有可验证的上游制造敞口，博通有 Meta 定制 AI 加速器敞口。Intel 有历史供货关系，但尚不能据此确认 Muse 新增订单。**其中，“向 Meta 供应算力”与“已经获得 Muse 带来的新增收入”是两回事：公开披露足以确认上述业务联系，却不足以分拆各公司的 Muse 专属销量、收入或份额。

这里的 Muse 指 **2026 年 9 月 8 日发布的个人 AI 智能体**，由 Muse Spark 模型驱动。它为用户提供独立的云端虚拟机，运行浏览器、代码、工具和后台任务，因此既涉及执行任务的 CPU，也涉及模型推理使用的加速计算，不能把两者合并成“CPU 订单”。[Meta 发布公告](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)、[Meta 技术说明](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)

下文注明的是资料**发布日期**；网页访问日为 **2026 年 10 月 9 日**。Muse 发布页另标有 **9 月 30 日更新日期**；动态页面的推荐新闻、抓取时间不作为正文事实的发布日期。

### 直接涉及 CPU 的四家公司

| 公司 | 可验证的业务及规模 | 已发生、计划与 Muse 归因边界 |
|---|---|---|
| **AMD** | **CPU：EPYC。**2 月 24 日官方公告确认，Meta 已在全球基础设施部署**数百万颗 EPYC CPU**，并将成为第六代 **Venice** 和后续 **Verano** 的主要客户。7 月 23 日公告进一步确认 Meta 正在实验室验证第六代 EPYC 平台，并测试 Helios 工作负载。[2 月公告](https://newsroom.amd.com/news/amd-and-meta-announce-expanded-strategic-partnersh/)、[7 月进展](https://ir.amd.com/news-events/press-releases/detail/1294/aai-2026-amd-delivers-full-stack-compute-for-the-agentic-ai-era) | 既有 EPYC 部署是已实现业务；新平台验证不能等同于全面部署。AMD 是有 Muse 具体实例线索的供应商，但其数百万颗存量覆盖 Meta 整体业务，不能全部算作 Muse。 |
| **NVIDIA** | **CPU：Grace、Vera；另有 GPU 和网络产品。**2 月 17 日公告确认，双方正为 Meta 生产应用部署 Grace，并称这是首次大规模 **Grace-only** 部署；Vera 的大规模部署则是 **2027 年的潜在安排**。[NVIDIA 原始公告](https://nvidianews.nvidia.com/news/meta-builds-ai-infrastructure-with-nvidia) | Grace-only 表明 NVIDIA 的业务并不限于“GPU 搭配一颗主机 CPU”。但公告没有披露 Grace 数量、Muse 占比，也没有确认 Muse 虚拟机运行于 Grace。Vera 不能计作截止日已经实现的部署。 |
| **Arm** | **CPU 成品：Arm AGI CPU；另有架构/IP 业务。**3 月 24 日，Meta 与 Arm 确认共同开发 AGI CPU，Meta 是主要合作伙伴和共同开发者，产品面向通用计算、AI 编排，并与 MTIA 配合。Arm 公布最高 **136 核、300W TDP**，早期系统当时已可提供，更广泛供货原定下半年。[Meta 公告](https://about.fb.com/news/2026/03/meta-partners-with-arm-to-develop-new-class-of-data-center-silicon/)、[Arm 公告](https://newsroom.arm.com/news/arm-agi-cpu-launch) | 这是具体产品和客户关系，不能只把 Arm 视作抽象的架构受益者。但未披露 Meta 已验收数量或 Muse 部署份额。9 月 8 日更新仍将 Meta 列为围绕 AGI CPU 开发解决方案的伙伴，不能从产品可供货推导 Meta 已完成大规模部署。[9 月更新](https://newsroom.arm.com/news/arm-agi-cpu-neoverse-css-n4-agentic-ai) |
| **亚马逊 AWS** | **云端 CPU 服务：Graviton。**4 月 24 日，Meta 公告将把**数千万个 Graviton 核心**纳入算力组合，首批部署即以数千万核心为目标，明确用于智能体 AI 的 CPU 密集型工作负载，并点名 Graviton5。[Meta 公告](https://about.fb.com/news/2026/04/meta-partners-with-aws-on-graviton-chips-to-power-agentic-ai/)、[亚马逊公告](https://www.aboutamazon.com/news/aws/meta-aws-graviton-ai-partnership) | 这是有明确数量级的协议，AWS 的业务形式是提供云计算能力。**数千万核心不是数千万颗 CPU**；公告没有提供截止日实际启用核心数，也没有说明其中多少用于 Muse。 |

**AMD 与 Muse 的直接联系，需要单独降低证据强度。**9 月 25 日的报道转述两名用户的终端观察：其 Muse 环境显示宿主 CPU 为 **AMD EPYC 9D25（Turin）**，沙箱提供两个 CPU 执行单元和 8GB 内存。这是具体实例的公开线索，但原始社交平台帖文未能读取，不能视为已独立复核的机群配置，更不能据此认定 AMD 独家供货。Meta 的原始技术文档确认了独立 Linux VM、CPU、内存和外部推理通路，**没有公布 CPU 品牌、统一规格或供应商份额**。[实例报道及其原帖链接](https://www.tomshardware.com/pc-components/cpus/meta-muse-runs-agents-on-amd-epyc-turin-hosts-with-two-cores-and-8gb-of-memory-ai-agent-can-pass-terminal-commands-to-ubuntu-host-system)、[Meta 技术原文](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)

因此，AMD 的正式业务证据是“已大量向 Meta 供应 EPYC”；“Muse 至少出现过 EPYC 实例”属于较弱的补充证据。

### 上游、相邻业务和历史供应商

| 公司或公司群 | 能确认的敞口 | 不能据此确认什么 |
|---|---|---|
| **台积电** | Arm 于 **3 月 24 日提交的 6-K** 收录台积电声明，明确其为 **Arm AGI CPU 制造商**，采用 **3nm 工艺**。这构成“Meta—Arm CPU—台积电制造”的具体上游链条。[原始申报文件，第 6 页](https://investors.arm.com/static-files/073df49d-58d8-451e-a196-a725319a9b7e) | 未披露用于 Meta 的晶圆数量、收入及 Muse 占比。只能确认制造关系，不能把台积电全部 AI 业务增长归因于 Muse。 |
| **博通 Broadcom** | Meta 于 **4 月 14 日**确认扩大合作，共同开发多代 **MTIA 定制 AI 加速器**，服务推理、推荐及后续生成式 AI 工作负载。[Meta 原始公告](https://about.fb.com/news/2026/04/meta-partners-with-broadcom-to-co-develop-custom-ai-silicon/) | **MTIA 是加速器，不是通用 CPU，也不应直接称作 GPU。**该合作证明 Meta AI 芯片敞口，但没有证明博通供应 Muse 的 VM CPU，或已获得 Muse 专属加速器收入。 |
| **Intel** | Meta 的前身 Facebook 于 **2016 年 3 月 9 日**披露与 Intel 联合设计 **Xeon-D/Broadwell-D**，用于其前端服务器；历史 CPU 客户关系有原始资料支持。[Meta 工程原文](https://engineering.fb.com/2016/03/09/data-center-engineering/facebook-s-new-front-end-server-design-delivers-on-performance-without-sucking-up-power/) | 历史关系不能证明 2026 年 Muse 采购。截止日可核验资料不足以确认 Muse 使用 Xeon、相关新增订单，或 Intel 因 Muse 丢失多少份额。 |
| **广达、联想、Supermicro、ASRock Rack** | Arm 在 3 月 24 日公告中将它们列为 AGI CPU 的主要 OEM/ODM 合作伙伴，存在具体平台业务联系。[Arm 原始公告](https://newsroom.arm.com/news/arm-agi-cpu-launch) | 平台合作名单不是 Meta 采购清单，不能据此认定这些公司承接了 Muse 服务器订单。 |

类似地，**美光、SK 海力士、三星**出现在 Arm 的生态合作声明中，说明其存储、内存或制造能力与平台相关；这些声明并没有披露 Muse 服务器的物料清单、供货份额或订单金额，因而不足以列为“已确认 Muse 供应商”。[Arm 原始申报文件](https://investors.arm.com/static-files/073df49d-58d8-451e-a196-a725319a9b7e)

### 数量上能确认到哪里

**已知基线包括 AMD 的数百万颗存量 EPYC、AWS 协议的数千万个核心，以及 NVIDIA 的大规模 Grace-only 部署；未知的是其中有多少服务于 Muse，更未知 Muse 发布后净新增了多少采购。**这三个口径分别是芯片颗数、核心数和未量化的部署规模，不能直接相加。

还需把两项容易误读的 GPU 承诺分开：

- **AMD 的最高 6GW 合作属于 Instinct GPU 部署协议。**首个 1GW 配套使用 Venice CPU，原公告计划于 2026 年下半年开始出货；它没有给出可将 6GW 换算成 CPU 颗数的固定配比，也不代表截止日 6GW 已全部交付。[AMD 公告，2026-02-24](https://newsroom.amd.com/news/amd-and-meta-announce-expanded-strategic-partnersh/)
- **NVIDIA 的“数百万”指 Blackwell 和 Rubin GPU 的多年部署安排。**它既不是 Grace/Vera CPU 数量，也不是 Muse 的专属采购量。[NVIDIA 公告，2026-02-17](https://nvidianews.nvidia.com/news/meta-builds-ai-infrastructure-with-nvidia)

即使采用公开实例的“每个 VM 两个 vCPU”作说明，**100 万个同时配置的 VM × 2 vCPU＝200 万个逻辑 vCPU 配额**，也不能推导需要 200 万个物理核心。物理需求还取决于并发活跃程度、超售、调度、每核线程数及内存约束；上述 100 万仅为算术示例，**不是已披露的 Muse 用户数或部署量**。

对父问题的意义是：**Muse 带来的 CPU 需求有明确的潜在承接渠道，而且同时覆盖 x86、Arm CPU 和云服务。**现有证据支持分析这些公司如何承接需求，但尚不支持给任何一家填入“Muse 增量收入”，也不支持把 Meta 整体 AI 扩张等同于 Muse 发布的效果。