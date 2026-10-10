**能，但截至 2026 年 10 月 9 日，能够确认的是 NVIDIA 已具备承接 Muse 类 CPU 需求的产品和 Meta 客户关系；尚不能确认 Muse 已为它带来多少新增 CPU 订单或收入。** NVIDIA 的直接受益路径是销售独立的 Grace、Vera CPU；模型推理带来的 GPU 收益则属于另一条路径。Meta 与 NVIDIA 的 CPU 部署合作已有官方公告，但公开的 Muse 单用户沙箱观察指向 AMD EPYC，不能把 Meta 整体采购 NVIDIA 的计划全部归因于 Muse。[NVIDIA–Meta 合作公告，2026-02-17](https://nvidianews.nvidia.com/news/meta-builds-ai-infrastructure-with-nvidia)；[Muse 用户端原始观察，2026-09-22](https://www.starkinsider.com/2026/09/meta-muse-specs-what-it-runs-on.html)

### Muse 为什么会给 NVIDIA 带来 CPU 机会？

这里的 Muse 指 Meta 于 **2026 年 9 月 8 日发布的个人 AI 智能体产品**。它由 Muse Spark 模型驱动，但整个产品还包括每位用户的云端计算环境。Meta 明确说明，Muse Secure VM 是隔离的 Linux 虚拟机，具备 CPU、内存、存储与浏览器能力，可以编译代码、执行工具、运行并发子智能体及定时任务；需要模型推理时，通过代理调用外部基础设施。[Meta 发布公告](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)；[Meta 技术说明，2026-09-08](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)

因此，Muse 的计算需求至少要分成两部分：

| 计算环节 | CPU 需求与 NVIDIA 的关系 |
|---|---|
| 用户虚拟机、工具执行、代码编译、任务调度等 | 能形成独立 CPU 服务器需求。NVIDIA 可以用 Grace、Vera 竞争这些工作负载，无须每个用户沙箱都配一块 GPU。 |
| 模型推理及其配套服务器 | 如果采用 NVIDIA 的 CPU–GPU 平台，可能同时带来主机 CPU 和 GPU 销售；但这是推理基础设施采购，不能与用户沙箱的 CPU 数量混算。 |

这个匹配有具体产品依据：NVIDIA 的 Vera 可以部署为独立 CPU 服务器，也可作为 Vera Rubin 平台的主机处理器；其公布的目标工作负载包括 Python 运行时、沙箱代码执行、编排和数据处理。**这些能力与 Muse 的执行环节相符，但“适合运行”并不等于“已被 Muse 采购”。**[NVIDIA Vera 公告，2026-05-31](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Unveils-Vera-the-CPU-for-Agents/default.aspx)

### NVIDIA 的受益基础已经到哪一步？

| 截止日前的事实 | 可以得出的结论 | 不能据此推出的结论 |
|---|---|---|
| **2 月 17 日**，NVIDIA 公布与 Meta 的多年合作：双方正在为 Meta 数据中心生产应用部署 Arm 架构 Grace CPU，并称之为首个大规模 **Grace-only** 部署。 | NVIDIA 已经进入 Meta 的独立 CPU 部署体系，具有实际客户基础。 | 公告没有披露 Muse 专属用途、CPU 数量、合同金额或部署完成比例。 |
| 同一公告称，双方合作部署 Vera，**有可能在 2027 年大规模部署**。 | Vera 有机会承接 Meta 后续 CPU 扩容。 | 这是未来部署表述，不能当成截至截止日已经完成的 Muse 装机。 |
| **5 月 31 日**，NVIDIA 宣布 Vera 已全面投产，系统厂商和云伙伴的系统计划从当年秋季开始供应。 | Vera 已超出概念和路线图阶段。 | 芯片投产不等于 Meta 或 Muse 已完成规模部署。 |
| **8 月 26 日**，NVIDIA 财报电话会称，Grace 过去 12 个月收入超过 **50 亿美元**，Vera 已向领先伙伴开始出货。 | NVIDIA 的服务器 CPU 业务已有收入基础。 | 这 50 亿美元没有被披露为独立 CPU 服务器收入，更没有被披露为 Muse 收入。 |

来源：[2 月 Meta 合作公告](https://nvidianews.nvidia.com/news/meta-builds-ai-infrastructure-with-nvidia)、[5 月 Vera 公告](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Unveils-Vera-the-CPU-for-Agents/default.aspx)、[8 月 26 日财报电话会记录，第 4 页](https://investor.nvidia.com/files/content_files/TRANSCRIPT_-NVIDIA-Corp-NVDA-US-Q2-2027-Earnings-Call-26-August-2026-5_00-PM-ET.pdf)。

这也说明了归因上的关键限制：**NVIDIA 的 CPU 业务增长和 Meta 的采购合作都早于 Muse 的公开发布。**它们证明 NVIDIA 有能力获得这类业务，却不能单独证明增长由 Muse 引起。

### 当前 Muse 用什么 CPU？NVIDIA 要获益还需要什么条件？

一份可打开的第一手用户观察，由 Clinton Stark 于 **9 月 22 日发表，记录的是 9 月 20 日的测量**：其 Muse 环境显示 **AMD EPYC 9D25、2 vCPU、约 7.7 GB 内存及 x86_64 架构**，该沙箱中未发现本地 GPU。作者明确强调，这是一个账号环境的观察，Meta 未公布这些配置，也不承诺其他账号相同。[原始观察及其限制](https://www.starkinsider.com/2026/09/meta-muse-specs-what-it-runs-on.html)

这项证据支持“**至少已有 Muse 环境使用 AMD CPU**”，并不支持“所有 Muse 都用 AMD”，更不能据此确定 NVIDIA 的份额为零。Meta 的官方架构说明没有给出 CPU 厂商分配。

NVIDIA 若要获得 Muse 沙箱扩容订单，至少需要满足以下条件：

- **获得实际工作负载分配。**Meta 已经采购 Grace，并不意味着所有新增虚拟机都会部署在 Grace 或 Vera 上。
- **完成软件与系统适配。**从已观察到的 x86_64 环境转到 Arm CPU，需要适配镜像、原生依赖、工具和隔离机制。Meta–NVIDIA 合作本身包含 CPU 软件库优化，但没有公布 Muse 迁移结果。
- **在整机成本和任务体验上胜出。**应比较每项任务的 CPU 时间、内存占用、并发能力、功耗和延迟。NVIDIA 公布的 Vera 通用性能优势不能直接当作 Muse 的实测提升。

后两点是根据现有架构与产品差异作出的工程判断；截止日前没有查到 Muse 在 Grace、Vera 与 EPYC 之间的公开对照测试。[Meta 架构说明](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)；[NVIDIA 的部署与软件优化说明](https://nvidianews.nvidia.com/news/meta-builds-ai-infrastructure-with-nvidia)

### 能否估算 NVIDIA 会卖多少 CPU？

**目前不能可靠给出 Muse 为 NVIDIA 带来的 CPU 颗数或收入，但可以明确已知数量的口径。**

以观察到的每个沙箱 **2 vCPU** 为例，假设有 100 万个同配置沙箱，得到的是：

> 100 万个沙箱 × 2 vCPU／沙箱＝200 万个配置上的 vCPU。

这不是 200 万个持续独占的物理核心，也不是对应数量的 CPU 芯片。专属虚拟机描述的是用户环境隔离，不能自动推出物理核心独占；实际服务器需求还取决于活跃率、平均负载、超分配、内存、浏览器池及宿主机开销。上述 100 万只是算例，并非 Muse 已披露的部署规模。

NVIDIA 另于 **3 月 16 日**公布，单个 Vera CPU 机架配置 **256 颗 CPU**，支持超过 **22,500 个并发 CPU 环境**；按公布数字相除，相当于平均每颗 CPU 超过 **87.9 个该口径环境**。但这些环境不是经过验证的 Muse 用户配置，不能据此推算每机架可服务多少 Muse 用户。[NVIDIA Vera 发布公告](https://nvidianews.nvidia.com/news/nvidia-launches-vera-cpu-purpose-built-for-agentic-ai)

截至截止日，缺少的是 **Muse 实际资源消耗、NVIDIA 承接比例、由新增采购满足的比例，以及成交价格**。因此，既不能把全部潜在虚拟机需求算成 NVIDIA 订单，也不能把没有披露的收入写成零。

对父问题的意义是：**NVIDIA 应列入 Muse 所代表的 CPU 需求增长的潜在直接受益公司，而且它已有 Meta 客户基础；但现有 Muse 沙箱观察对 AMD 的指向更直接。**NVIDIA 的一般 CPU 业务增长、Meta 整体采购和 Muse 专属增量，仍需分别表述。

*资料时间口径：以上页面均于 2026-10-09 抓取。文中日期为来源的发布日期或明确的测量日期；Meta 发布页标注首发 2026-09-08、更新 2026-09-30，引用的是截止日前可见版本，抓取日不作发布日期使用。*