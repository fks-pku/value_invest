**能，但截至 2026 年 10 月 9 日，能够确认的是 AMD 的 EPYC 服务器 CPU 存在受益路径，尚不能确认 Muse 已为 AMD 带来多少新增 CPU 收入。** Muse 把个人 AI 的工作扩展到云端浏览器、代码执行和后台任务，这些都需要 CPU；如果这些负载超出现有服务器的承载能力，并由新增 EPYC 承接，就会增加 AMD 的 CPU 销售。Meta 已经是 EPYC 的大客户，因此这条路径具有实际业务基础。[Meta 技术说明，2026-09-08](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)、[AMD—Meta 合作公告，2026-02-24](https://ir.amd.com/financial-information/sec-filings/content/0000002488-26-000045/pressreleasedatedfebruary2.htm)

这里的 Muse 指 Meta **9 月 8 日发布的个人 AI 代理**，而不只是此前发布的 Muse Spark 模型。以下资料均于 **2026-10-09 抓取**；文中的日期指来源发布日期，动态页面的抓取时间不代表其发布日期。

**Muse 为什么会带来 CPU 需求**

Meta 的原始技术文档明确说明：每位用户的 Muse 拥有独立的 Linux 云端虚拟机，内含浏览器、CPU、内存和存储，可以编译代码、运行工具、处理并发子代理和定时任务；模型推理则通过受约束的接口连接外部基础设施。也就是说，模型生成行动方案之外，还需要一台计算机实际执行这些行动。[Meta 技术说明，2026-09-08](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)

由此可以推导出两条 CPU 收入路径：

- **代理执行服务器扩容。** 更多用户、更长的后台运行时间、更多浏览器和代码任务，会增加 CPU 执行负载。若新增服务器采用 EPYC，AMD 就能获得相应销售。
- **模型基础设施扩容带动配套 CPU。** Muse 的推理需求可能推动 AI 服务器扩容，其中也有主机 CPU。不过这部分必须按实际系统配置计算，不能把 GPU 采购金额计入 CPU 收入。

这里最重要的限制是：**“每人一台虚拟机”不等于“每人独占一颗物理 CPU”，也不证明每位用户一直占用固定的物理核心。** 注册用户数、日活用户数和同时需要执行任务的虚拟机数量，是不同口径。Meta 公布的架构没有给出可据此计算采购量的并发率、物理核心分配或资源复用数据。

**AMD 已有的业务基础，和不能归给 Muse 的部分**

| 已知事实 | 对 AMD CPU 收入的意义 | 归因边界 |
|---|---|---|
| AMD 在 2026 年 2 月披露，Meta 已部署**数百万颗 EPYC CPU** | AMD 已进入 Meta 的大规模生产基础设施，有现成供货关系 | 是跨代、全基础设施的部署量，不是 Muse 专用数量，更不是 2026 年新增销量 |
| Meta 将成为第六代 EPYC **Venice** 及下一代 **Verano** 的主要早期客户 | CPU 合作明确延续，未来扩容有承接基础 | 公告没有给出 Muse 对应的 CPU 订单、单价或收入 |
| 双方签署最高 **6GW 的 Instinct GPU** 合作，首个 1GW 项目原计划于 2026 年下半年开始供货，系统包含 Venice CPU | GPU 系统也可能带来配套 CPU 销售 | 6GW 是 GPU 合作规模；供货计划不等于全部交付，更不能把整个合作视为 Muse 增量 |

以上均来自 [AMD 2026 年 2 月 24 日原始公告](https://ir.amd.com/financial-information/sec-filings/content/0000002488-26-000045/pressreleasedatedfebruary2.htm)。这些合作早于 Muse 的公开发布，支持“AMD 有能力承接需求”，不能单独证明“采购是 Muse 新增带来的”。

关于 Muse 当前硬件，还有一项更直接但范围较小的观察：Tom’s Hardware 在 **9 月 30 日的自行测试**中报告，其 Muse 实例对应 EPYC 9D25，虚拟机显示约两个核心、7.75GB 内存。这属于测试者的一手样本证据，支持至少被测实例使用 AMD 平台，**不等于 Meta 对全量部署、专用物理核心或采购数量的确认**。[测试原文，2026-09-30](https://www.tomshardware.com/tech-industry/artificial-intelligence/geekbench-7-results-suggest-openais-dots-agent-runs-on-nine-core-amd-epyc-vms-with-nearly-10gb-of-memory-newest-runs-score-about-six-times-meta-muse-in-multi-core)

**收入能增加多少：已知基线与可复算的条件**

AMD 于 **8 月 4 日**公布的第二季度业绩，是 Muse 9 月公开发布前的财务基线：数据中心收入约 **67 亿美元，同比增长 107%**，增长由 EPYC CPU 和 Instinct GPU 共同推动。这是混合口径，不能当作 EPYC 单独收入，更不能用其增速代表 Muse 带来的 CPU 增长。[AMD 第二季度财报](https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results)

截至截止日，所查原始披露没有提供 **Muse 专属 EPYC 出货量、成交均价或已确认收入**，所以无法给出实际增量金额，也不能给出它占 AMD CPU 收入的百分比。未知不等于零：上线前可能已经采购，上线后也可能首先消耗已有容量。

下面仅说明数量级如何变化，**全部参数均为演示假设，不是 Meta 实测或 AMD 预测**：

假定某个新增部署阶段需要额外支持 100 万个 Muse 用户；每个同时运行的实例需要 2 个“物理核心等效”的处理能力；每颗 CPU 扣除系统开销后可提供 128 个此类核心等效容量；没有可复用的闲置容量；全部新增 CPU 采用 AMD，净售价每颗假设为 5,000 美元。

| 假设的同时运行比例 | 同时运行实例 | CPU 数量，向上取整 | 对应 CPU 销售额 |
|---|---:|---:|---:|
| 1% | 10,000 | 10,000 × 2 ÷ 128 → **157 颗** | **78.5 万美元** |
| 10% | 100,000 | 100,000 × 2 ÷ 128 → **1,563 颗** | **781.5 万美元** |
| 100% | 1,000,000 | 1,000,000 × 2 ÷ 128 → **15,625 颗** | **7,812.5 万美元** |

这个演示说明，同样是新增 100 万用户，资源是否常驻、同时运行比例是多少，会使采购需求相差很大。虚拟机显示的“两个核心”不能直接代入“两个物理核心等效”；实际还受内存容量、峰值冗余和工作负载影响。上述金额也是**部署采购对应的销售额，不是每年自动重复的收入**，且尚未考虑交付和收入确认时间。

现实中还要扣除三类因素：

- **已有容量和原定采购。** Muse 如果使用闲置服务器，或只是使用原本就会购买的 EPYC，短期未必增加 AMD 收入；它也可能只是把采购时间提前。
- **每颗 CPU 可承载的任务增加。** 更高核心密度、调度优化和软件效率提高，都可能让工作量增长快于 CPU 颗数增长。
- **供应商分流。** Meta 同时采用其他 CPU。NVIDIA 在 **2 月 17 日**宣布与 Meta 扩大独立 Grace CPU 部署，并讨论可能于 2027 年大规模部署 Vera。因此不能假设 Muse 的所有新增 CPU 需求都归 AMD；这份公告本身也没有证明 Muse 已使用 Grace 或 Vera。[NVIDIA 原始公告](https://nvidianews.nvidia.com/news/meta-builds-ai-infrastructure-with-nvidia)

因此，对“AMD 的 CPU 收入能否因 Muse 增长”的准确判断是：**可以，最直接的是 EPYC 承接代理执行负载；已有客户关系和被测实例提供了支持，但新增采购规模、收入金额和增长幅度尚未披露。** 没有相应证据可把这一路径扩展为 Ryzen 客户端 CPU 的已实现增长，也不能把 Instinct GPU 收入混入其中。

对父问题的意义是：Muse 说明个人 AI 代理能够增加独立于模型推理的 CPU 执行需求，AMD 是有实际承接基础的受益公司之一；但行业工作量增长、AMD 获得的订单，以及其中真正由 Muse 新增的部分，仍是三个不同层次。