**Intel 会同时受益于 CPU 需求增长、承受新增需求被竞争对手分走的压力。就 Meta Muse 而言，截至 2026 年 10 月 9 日，竞争对手进入 Meta CPU 供应体系的证据，比 Intel 获得 Muse 专属增量订单的证据更明确。**因此，较有依据的判断是：Intel 有行业增长带来的受益机会，但不能把 Muse 的增长直接计为 Xeon 的增长；即使 Intel 收入增加，市场份额也可能下降。[Intel 第二季度披露](https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-26-000157/intc-20260627.htm)、[Meta 的 CPU 多元化公告](https://about.fb.com/news/2026/04/meta-partners-with-aws-on-graviton-chips-to-power-agentic-ai/)支持这一判断。

这里的 Muse 指 Meta 于 **2026 年 9 月 8 日发布的个人 AI 代理**：它由 Muse Spark 模型驱动，在专属云端虚拟机中使用浏览器、调用工具和执行任务，用户关闭应用后仍可继续工作。它带来的 CPU 机会，主要是运行这些执行环境及配套服务，不能与模型训练、推理所需的 GPU 混为一谈。[Meta 发布公告](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)

以下只采用截止日前发布的信息；网页访问日为 **2026 年 10 月 9 日**。Meta 的 Muse 发布页标示首发日为 9 月 8 日、更新日为 9 月 30 日，其他关键来源的发布日期在对应事实旁注明；访问日不作为发布日期。

**Intel 为什么仍能受益**

Muse 将 AI 从“生成回答”延伸到持续执行任务。浏览器、脚本、文件处理、连接器和隔离环境都会消耗 CPU、内存及存储资源。Meta 的技术说明确认，Muse 采用 Linux 隔离机制，并可在后台工作、调度子代理和构建工具。这支持“代理使用增加会带来 CPU 工作量”的机制，但并不意味着每个账户都永久独占物理核心。[Meta 技术说明，2026-09-08](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)

Intel 已有承接此类负载的产品。其 **2026 年 6 月 1 日**公告推出 Xeon 6+，采用 Intel 18A，最高 288 个能效核、12 通道 DDR5，面向高并发、云原生和代理工作负载。这说明 Intel 具备参与竞争的产品基础；核心数本身不能证明它在 Muse 上的单位任务成本最低，也不是 Meta 采用该产品的证明。[Intel Xeon 6+ 原始公告](https://newsroom.intel.com/data-center/intel-puts-agentic-ai-xeon-6-networking-ai-systems/)

更直接的已实现基线来自 Intel **7 月 24 日提交的第二季度 10-Q**：

- 服务器产品销量同比增长 **9%**，平均售价增长 **48%**；高端产品占比提升是售价增长的主要原因，提价贡献较小。
- 按四舍五入后的披露数复算，收入增幅约为 **1.09 × 1.48 − 1 = 61.3%**，不能将其全部解释为出货量增长。
- 公司同时披露，需求超过内部供给能力，并预计行业供应限制延续至下一年。[Intel 第二季度 10-Q](https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-26-000157/intc-20260627.htm)

**这些增长发生在 Muse 9 月发布之前，不能归因于此次发布。**它们证明 Intel 已受益于服务器市场需求，也说明供货能力会限制它承接后续增量。另需注意，Intel 的 DCAI 部门还包含加速器、网络和专用芯片，整个部门收入不能直接当作 CPU 收入。

**为什么份额压力更具体**

Meta 已公开选择多条 CPU 路线，覆盖自建数据中心、加速器主机和外购云服务：

| CPU 路线 | 截止日前已公开的事实与状态 | 对 Intel 的含义 |
|---|---|---|
| **AMD EPYC** | 2 月 24 日公告称，Meta 已部署数百万颗 EPYC，并将成为 Venice、Verano 的领先客户；7 月 23 日更新称，Meta 正在验证第六代 EPYC 平台和 Helios 工作负载。[2 月公告](https://newsroom.amd.com/news/amd-and-meta-announce-expanded-strategic-partnersh/)、[7 月更新](https://ir.amd.com/news-events/press-releases/detail/1294/aai-2026-amd-delivers-full-stack-compute-for-the-agentic-ai-era) | AMD 已有实际客户基础，并进入下一代平台验证阶段；但不能把验证当成全部部署完成。 |
| **NVIDIA Grace／Vera** | 2 月 17 日公告确认双方推进用于 Meta 生产应用的 Grace CPU 部署，包括大规模纯 Grace 系统；Vera 的大规模部署表述为 **2027 年的可能安排**。[NVIDIA 原始公告](https://nvidianews.nvidia.com/news/meta-builds-ai-infrastructure-with-nvidia) | NVIDIA 直接竞争通用 CPU 预算，其影响不限于销售 GPU。 |
| **AWS Graviton** | Meta 4 月 24 日宣布协议，将数千万个 Graviton 核心纳入算力组合，明确用于代理 AI 的 CPU 密集型工作；这是协议及部署安排，不等于截止日全部交付。[Meta 原始公告](https://about.fb.com/news/2026/04/meta-partners-with-aws-on-graviton-chips-to-power-agentic-ai/) | Meta 外购云算力也可能绕过 Xeon；“数千万核心”不能误写为数千万颗 CPU。 |
| **Arm AGI CPU** | Meta 3 月 24 日宣布作为领先合作伙伴与共同开发者，联合开发多代 CPU，并与自研 MTIA 加速器配合；9 月 8 日 Arm 仍将 Meta 列为围绕该 CPU 开发方案的公司。[Meta 公告](https://about.fb.com/news/2026/03/meta-partners-with-arm-to-develop-new-class-of-data-center-silicon/)、[Arm 更新](https://newsroom.arm.com/news/arm-agi-cpu-neoverse-css-n4-agentic-ai) | 对 Intel 构成长期架构替代压力，但公告没有给出 Muse 专属装机量。 |

这里尤其容易混淆的是 AMD 协议中的 **最高 6GW**：它是多年、多代 **Instinct GPU 部署协议**的口径，不能换算成 6GW 的 CPU 采购，更不能全部归因于 Muse。协议中的 EPYC 合作是独立且明确的 CPU 证据。[AMD 原始公告](https://newsroom.amd.com/news/amd-and-meta-announce-expanded-strategic-partnersh/)

Muse 本身也有偏向 AMD 的早期样本：Clinton Stark 在 **9 月 22 日**发表的亲历记录中，展示了 9 月 20 日由其 Muse 代理报告的配置，包括 **2 个 vCPU、AMD EPYC 9D25、约 7.7GB 内存**。但作者明确说明，这是单一代理对自身环境的报告，Meta 没有发布这些规格，其他账户可能不同。因此，它只能作为个别环境的线索，不能证明 AMD 独家供应，也不能证明 Intel 份额为零。[原始体验记录](https://www.starkinsider.com/2026/09/meta-muse-specs-what-it-runs-on.html)

**增长与份额下降如何同时发生**

按相同收入口径：

> Intel 服务器 CPU 收入＝服务器 CPU 市场收入 × Intel 收入份额。

一个纯说明性的情景：假设市场从 100 增至 130，Intel 份额从 60% 降至 50%，则收入从 60 增至 65，仍增长 **8.3%**。份额下降 10 个百分点，并没有阻止绝对收入增长。这里的数字是情景假设，并非 Intel 实际份额或预测。

对 Muse 的新增采购，则还要经过“工作量增加—现有容量是否足够—新增服务器采购—供应商分配”几步。专属虚拟机代表用户环境隔离，并不自动等于持续占满 CPU；后台等待、并发率、超售、每颗芯片核心数、内存容量和现有余量都会影响采购量。Meta 的公开架构说明没有给出足以完成这一换算的运营数据。[Meta 技术说明](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)

**截至截止日，无法给出 Intel 因 Muse 新增多少颗 CPU、多少收入，或因此损失多少份额的可信数值。**公开资料没有披露 Muse 全部 CPU 供应商分配、Intel 专属订单及新增采购量。这也意味着，竞争对手获得新项目只能证明 Intel 面临增量份额压力，不能据此认定 Meta 已撤换相同数量的 Xeon。

对父问题的意义是：Muse 支持“代理 AI 会扩大 CPU 工作量”的判断，但公司受益并不均匀。**Intel 应被视为具备产品和现有业务基础的潜在增量受益者，同时面临 AMD 与多条 Arm 路线的竞争；目前不能把它列为已证实获得 Muse 专属订单的赢家。**