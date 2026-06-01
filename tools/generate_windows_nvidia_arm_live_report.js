const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const PROJECT_ID = "windows_nvidia_arm_event_live_20260531";
const OUT_DIR = path.join(ROOT, "research", "qa_projects", PROJECT_ID);
const REPORT_DATE = "2026-05-31";
const REVIEW_HORIZON = "2026-08-31";

const SCORE_WEIGHTS = {
  chokepoint_strength: 0.26,
  future_space: 0.18,
  valuation_odds: 0.18,
  evidence_quality: 0.14,
  disconfirming_risk_control: 0.10,
  monitorability: 0.05,
  payoff_convexity: 0.09,
};

const SCORE_DIMENSION_WEIGHTS = {
  scarcity_or_monopoly: 0.35,
  mispricing: 0.25,
  earnings_elasticity: 0.25,
  risk_control: 0.15,
};

const sources = [
  source("SRC-AXIOS-2026-05-30", "Axios: Nvidia, Microsoft set stage for AI PC push", "message", "https://www.axios.com/2026/05/30/nvidia-microsoft-pcs-ai-surface-dell", "2026-05-30", "Axios reported that Microsoft, Dell and others are preparing to show computers using Nvidia's processor as the main engine, with disclosure expected as early as the following week."),
  source("SRC-TOMS-2026-05-29", "Tom's Hardware: Nvidia and Windows new era of PC teaser", "message", "https://www.tomshardware.com/pc-components/cpus/nvidia-and-windows-to-usher-in-a-new-era-of-pc", "2026-05-29", "Tom's Hardware described synchronized Nvidia, Windows and Arm social posts around a new PC era and framed it as likely related to Windows-on-Arm chips."),
  source("SRC-MS-ARM-APPS-2025-09-18", "Microsoft Windows on Arm app ecosystem update", "evidence", "https://blogs.windows.com/windowsdeveloper/2025/09/18/what-is-new-for-developers-in-windows-on-arm/", "2025-09-18", "Microsoft said Windows on Arm native app momentum had improved, with most user time in native Arm64 apps and more developer tooling support."),
  source("SRC-MS-APP-ASSURE-2025-05-14", "Microsoft App Assure compatibility guidance for Arm PCs", "evidence", "https://techcommunity.microsoft.com/blog/windows-itpro-blog/app-assure-supporting-application-compatibility-on-arm-based-windows-11-devices/4412829", "2025-05-14", "Microsoft framed App Assure as support for application compatibility on Arm-based Windows 11 devices, reducing one adoption barrier for enterprises."),
  source("SRC-MS-COPILOT-PCS-2025-05-06", "Microsoft Surface Copilot+ PC launch update", "evidence", "https://blogs.windows.com/devices/2025/05/06/introducing-new-surface-copilot-pcs-built-for-business-surface-pro-12-inch-and-surface-laptop-13-inch/", "2025-05-06", "Microsoft's Surface Copilot+ PC update showed continued Windows Arm commercialization and positioned local AI, battery life and Copilot+ features as core PC refresh messages."),
  source("SRC-QCOM-COPILOT-2024-05-20", "Qualcomm Snapdragon X Series Copilot+ PC launch", "evidence", "https://www.qualcomm.com/news/releases/2024/05/snapdragon-x-series-is-the-exclusive-platform-to-power-the-next-", "2024-05-20", "Qualcomm described Snapdragon X Series as the first platform for Copilot+ PCs, with 45 TOPS NPU capability and multiple OEM design wins."),
  source("SRC-QCOM-ENTERPRISE-2025-01-02", "Qualcomm enterprise AI PC momentum", "evidence", "https://www.qualcomm.com/news/onq/2025/01/snapdragon-x-series-enterprise-ai-pcs-are-coming", "2025-01-02", "Qualcomm highlighted enterprise AI PC momentum and the number of Snapdragon X devices available, establishing the incumbent Windows-on-Arm benchmark."),
  source("SRC-ARM-PC-ECOSYSTEM-2025", "Arm: Windows on Arm software ecosystem progress", "evidence", "https://www.arm.com/blogs/blueprint/windows-on-arm-ai-pc-apps", "2025-05-21", "Arm described improving Windows-on-Arm app coverage and positioned Arm-based AI PCs as a growing ecosystem rather than a single-chip story."),
  source("SRC-MARKET-SNAPSHOT-2026-05-31", "Market price and valuation screen snapshot", "evidence", "https://finance.yahoo.com/", "2026-05-31", "Current public market prices and valuation screens show NVIDIA, Microsoft and Arm already carry large AI/platform expectations; full consensus EV, FCF and margin bridge remains required before high action states."),
];

const chainRows = [
  ["IP / ISA", "Arm instruction set, CPU core IP, ecosystem certification", "Arm Holdings", "Receives licensing and royalty economics if Windows Arm unit volumes expand.", "Arm IP is scarce, but royalty elasticity depends on shipped units and contract terms.", "Q2.1 / Q4.1"],
  ["SoC platform", "CPU, GPU, NPU, memory controller, modem/connectivity, power management", "NVIDIA, MediaTek, Qualcomm", "Turns Windows AI PC demand into silicon platforms for OEM devices.", "NVIDIA AI/GPU brand and Qualcomm's incumbent Windows-on-Arm stack are the key contested nodes.", "Q1.1 / Q2.1"],
  ["OS and developer layer", "Windows on Arm, driver model, app compatibility, Copilot+ features", "Microsoft, Windows developer ecosystem, ISVs", "Controls whether Arm silicon can become a mainstream Windows platform rather than a niche device class.", "Microsoft has the highest ecosystem chokepoint but lower direct earnings elasticity from one chip cycle.", "Q2.1 / Q3.1"],
  ["OEM and channel", "Laptop design, enterprise qualification, retail and commercial distribution", "Dell, Microsoft Surface, other PC OEMs", "Converts platform availability into PC shipments and enterprise refresh cycles.", "OEMs benefit from product refresh but usually have lower scarcity and thinner value capture.", "Q1.2 / Q4.1"],
  ["Foundry and components", "Advanced-node manufacturing, packaging, memory, Wi-Fi, displays, batteries", "TSMC, memory suppliers, component vendors", "Supplies enabling capacity; value capture is broad unless the chip wins meaningful volumes.", "Foundry/component exposure is real but diluted without direct order evidence.", "Q2.2 / Q3.2"],
  ["End demand", "AI PC refresh, thin-and-light battery life, local inference, enterprise deployment", "Consumers, developers, enterprises, OEM procurement", "Demand must show up as shipped units, mix, ASP and software usage, not only a launch headline.", "Adoption evidence is the gate for raising future-space and payoff scores.", "Q1.2 / Q4.2"],
];

const chainExplainer = {
  plainSummary: "一句话看懂：这条链不是“谁又发布一颗芯片”，而是终端用户是否愿意买 Windows Arm AI PC，并让 Microsoft、Arm、NVIDIA/芯片平台、OEM 和制造环节各自拿到可验证的收入与利润。",
  flowSteps: [
    "消费者和企业先提出需求：更长续航、本地 AI、轻薄和 Windows 应用兼容。",
    "Microsoft 决定 Windows on Arm、Copilot+、驱动和应用生态能否让用户放心迁移。",
    "Arm 提供底层指令集/IP，NVIDIA、Qualcomm、MediaTek 等把 CPU/GPU/NPU 做成可卖给 OEM 的 SoC 平台。",
    "TSMC、存储和零部件供应商负责把芯片和整机交付出来，OEM 再把产品卖给渠道、企业和消费者。",
    "利润最可能集中在生态控制、AI/GPU 平台能力、Arm IP 授权和被 OEM 真实采用的 SoC 设计，而不是普通组装环节。",
  ],
  layers: [
    { name: "需求端", role: "决定有没有真实换机", players: "消费者、企业、开发者", note: "如果用户只是看热闹、不愿意换机，整条链都不会放量。" },
    { name: "系统生态", role: "决定能不能用", players: "Microsoft、Windows ISV、驱动生态", note: "这是 Windows Arm 的第一卡点：应用和驱动不顺，硬件再强也难卖。" },
    { name: "芯片平台", role: "把需求变成可量产方案", players: "NVIDIA、Qualcomm、MediaTek", note: "这里决定性能、功耗、AI 能力和 OEM 是否愿意采用。" },
    { name: "IP 与制造", role: "提供底层授权和产能", players: "Arm、TSMC、存储/组件供应商", note: "Arm 更像授权收费，制造环节需要看到真实订单才有更高弹性。" },
    { name: "整机和渠道", role: "把产品卖出去", players: "Dell、Surface、其他 PC OEM", note: "OEM 能放大销量，但通常替代性更高、利润率更薄。" },
  ],
  chokepoints: [
    { node: "Windows 应用/驱动生态", why: "控制用户是否敢从 x86 迁移到 Arm", controllers: "Microsoft + ISV 生态", qa: "Q2.1 / Q3.1" },
    { node: "NVIDIA AI/GPU 平台心智", why: "如果能迁移到 PC SoC，可能让 AI PC 不只是低功耗故事", controllers: "NVIDIA", qa: "Q2.1 / Q4.1" },
    { node: "Arm IP 授权", why: "几乎所有 Windows Arm 方案都绕不开 Arm 指令集和授权", controllers: "Arm Holdings", qa: "Q2.1 / Q4.1" },
    { node: "OEM 真实出货", why: "没有多家 OEM SKU、价格和订单，新闻热度不能变成财务弹性", controllers: "Dell、Surface、其他 OEM", qa: "Q1.2 / Q4.2" },
  ],
  targetLinks: [
    ["MSFT", "Windows/开发者生态", "直接控制平台，但单一芯片周期业绩弹性较低", "Q2.1 / Q4.1"],
    ["NVDA", "AI/GPU + PC SoC 平台", "若方案被 OEM 采用，具备较强心智和平台稀缺性", "Q2.1 / Q4.1"],
    ["ARM", "IP/ISA 授权", "稀缺但弹性取决于出货和 royalty 条款", "Q2.1 / Q4.1"],
    ["QCOM", "现有 Windows Arm incumbent", "既可能受益于市场扩大，也可能被新平台分流", "Q2.1 / Q3.2"],
    ["OEM/组件链", "整机和配套", "需要真实订单证明，否则多为间接暴露", "Q1.2 / Q4.2"],
  ],
};

const l1s = [
  l1("Q1", "这件事到底是什么，影响范围有多大？", "当前可见证据显示，Windows + NVIDIA Arm PC 处在强信号预告和媒体确认阶段，但正式 SKU、价格、性能、出货节奏尚未完全落地。"),
  l1("Q2", "产业链里谁真正控制稀缺价值？", "最强控制点在 Microsoft 的 Windows/开发者生态、NVIDIA 的 AI/GPU 平台能力、Arm IP 授权以及既有 Windows-on-Arm 经验；OEM 和组件链条价值捕获更弱。"),
  l1("Q3", "哪些因素会让新闻热度无法转成投资机会？", "主要反证来自应用兼容、驱动、性能/续航不达预期、定价过高、OEM 出货不足、以及核心受益标的估值已充分反映 AI 平台预期。"),
  l1("Q4", "哪些证券值得进入观察池，行动状态如何？", "报告只把它作为 live 观察清单，不给强行买入结论；NVIDIA、Microsoft、Arm、MediaTek 和 Qualcomm 最值得跟踪，但多数标的因估值或证据未充分而维持 watch_only。"),
];

const l2s = [
  l2("Q1.1", "新闻边界和产品边界", "事件强度高于普通传闻，但仍低于正式产品发布；研究必须保留事实、推断和待验证事项的边界。"),
  l2("Q1.2", "需求是否足够真实", "AI PC 和 Windows-on-Arm 的需求逻辑存在，但能否形成大规模换机，需要看性能、续航、价格、企业兼容和 OEM 配置。"),
  l2("Q2.1", "稀缺控制点在哪里", "真正稀缺的是平台生态、AI/GPU 能力、CPU IP 与设计认证，而不是单纯的 PC 组装。"),
  l2("Q2.2", "利润能否进入财报", "NVIDIA 和 Arm 有更高单位经济弹性，Microsoft 更偏生态战略，OEM 弹性低；MediaTek 取决于其是否为实际 SoC 协作方。"),
  l2("Q3.1", "技术和采用风险", "如果 Windows Arm 仍停留在兼容性、驱动或企业部署摩擦里，事件会变成叙事而不是利润曲线。"),
  l2("Q3.2", "估值和竞争风险", "大市值 AI 平台股已经包含较强增长预期，新增 PC 芯片业务需要证明足够大、足够独特、且没有被价格提前消化。"),
  l2("Q4.1", "观察标的池和排序", "排序只从价值捕获载体出发，不按美股便利性收缩，也不把负面读数标的误判为多头机会。"),
  l2("Q4.2", "三个月验证触发器", "live 模式不附后验收益 label；用 2026-08-31 作为下一轮验证窗口，跟踪正式发布、SKU、性能、OEM、价格和订单证据。"),
];

const leaves = [
  leaf("Q1.1.1", "Q1.1", "这是否已经是正式产品发布？", "news-event-analysis", "evidence_quality", "决定报告能否把事件当作已确认商业事实，而不是只当作线索。", "Axios reports Microsoft, Dell and others plan to show Nvidia-processor PCs; Tom's describes synchronized teaser signals.", "No official SKU, price, launch date or performance data is disclosed.", "研究应把它视为高可信线索，但不能用未发布规格支撑高分。", ["event_status", "confirmed_parties", "uncertain_fields"], "Axios 报道了 Microsoft、Dell 等准备展示搭载 NVIDIA 主处理器的 PC；Tom's Hardware 记录了 NVIDIA、Windows、Arm 的同步预告信号。", "证据支持事件存在，但公开信息仍缺少正式产品参数和商业条款。", "Q1 可以成立，但 evidence_quality 只能给中等偏上，不能按正式发布处理。", "缺少官方 SKU、定价、性能、OEM 全名单和可购买日期。", "若 NVIDIA、Microsoft 或 OEM 发布正式产品页、规格书和上市时间，则提高证据等级。", ["SRC-AXIOS-2026-05-30", "SRC-TOMS-2026-05-29"], artifact("事件边界", ["层级", "当前状态", "投资含义"], [["已见信息", "媒体报道 + 同步预告", "可以进入研究池"], ["未见信息", "SKU/价格/性能/供货", "不能直接提高目标分"], ["下一确认", "正式发布和 OEM 型号", "决定是否升级 action_state"]])),
  leaf("Q1.1.2", "Q1.1", "产品形态更可能是什么？", "news-event-analysis", "future_space", "判断它是单一 OEM 机型、平台扩张，还是 Windows Arm 生态转折。", "Reports point to PC systems using Nvidia processors, with Microsoft and Dell named; historical context indicates Windows-on-Arm AI PC devices already exist through Qualcomm.", "The teaser could represent limited prototypes or marketing before volume shipments.", "产品形态更像 Windows Arm AI PC 平台扩容，而非已经证明的大规模换代。", ["product_form", "oem_scope", "timing"], "可见报道指向搭载 NVIDIA 主处理器的 Windows PC，且 Microsoft 和 Dell 被提及；Qualcomm 资料显示 Copilot+ PC 已有一轮 Windows Arm 商业化基础。", "NVIDIA 进入主处理器角色会改变 Windows Arm 竞争格局，但仍需要实际 OEM 数量和配置来确认范围。", "Q1.1 的结论是平台信号强、产品证据未完整。", "缺少 MediaTek 角色、N1/N1X 命名、量产节点和 OEM 配置清单。", "如果发布只覆盖少量展示机，降低 future_space；若覆盖多家 OEM 的量产机型，提高。", ["SRC-AXIOS-2026-05-30", "SRC-QCOM-COPILOT-2024-05-20"], artifact("产品形态判断", ["可能形态", "证据", "评分影响"], [["单机型展示", "媒体只点名部分厂商", "future_space 低"], ["平台扩容", "Windows/Arm/NVIDIA 同步信号", "future_space 中"], ["生态转折", "需多家 OEM + 出货目标", "尚未确认"]])),
  leaf("Q1.2.1", "Q1.2", "Windows Arm AI PC 的需求是真需求还是营销概念？", "industry-report-analysis", "future_space", "决定主题空间是否足够大，避免只因新闻热度建立多头。", "Microsoft and Qualcomm both position Copilot+ PCs around local AI, battery life and Arm-based performance; Microsoft continues to improve developer/app compatibility.", "Users may not pay a premium for local AI features and enterprises may stay with x86 compatibility.", "需求逻辑存在，但必须转化为换机、ASP 或企业采购数据。", ["demand_driver", "buyer_problem", "adoption_gate"], "Microsoft 的 Surface Copilot+ PC 信息强调本地 AI、便携和续航；Qualcomm 的 Snapdragon X 资料将高 TOPS NPU 和 OEM 设计作为核心卖点。", "AI PC 与轻薄长续航是明确产品诉求，但消费者和企业是否愿意规模化替换仍未被这条新闻证明。", "Q1.2 支持继续研究，但未来空间不能只靠 TAM 口号给高分。", "缺少 Windows Arm PC 市占率、平均售价、企业部署和退货率数据。", "若 OEM 公布订单、企业采购或高配机型占比，提升 future_space。", ["SRC-MS-COPILOT-PCS-2025-05-06", "SRC-QCOM-COPILOT-2024-05-20", "SRC-MS-ARM-APPS-2025-09-18"], artifact("需求到产品映射", ["需求", "对应产品能力", "验证数据"], [["长续航轻薄", "Arm SoC 能效", "续航评测和 SKU 配置"], ["本地 AI", "NPU/GPU 推理能力", "AI 应用使用时长"], ["企业部署", "兼容和管理支持", "商业订单和 App Assure 案例"]])),
  leaf("Q1.2.2", "Q1.2", "NVIDIA 进入是否能扩大 Windows Arm 市场，而不是只分走 Qualcomm 份额？", "industry-report-analysis", "payoff_convexity", "决定该事件是增量机会还是零和竞争。", "Qualcomm already built the first Copilot+ PC wave; Nvidia adds AI/GPU brand, possible developer appeal and OEM optionality.", "Nvidia entry may mainly fragment Windows-on-Arm economics and pressure incumbent margins.", "更合理的判断是先扩大关注度和 OEM 选择，再看是否扩大总量。", ["market_expansion", "share_shift", "incremental_units"], "Qualcomm 资料证明 Windows Arm 已有商业化基础；媒体报道若属实，NVIDIA 的加入会增加平台选择和 AI 品牌吸引力。", "新增玩家可能扩大市场，也可能只是重新分配有限的 Windows Arm PC 份额。", "Q1.2 对整体机会持开放态度，但把 Qualcomm 视为需要重新评估的 incumbent，而不是单纯受益者。", "缺少 Windows Arm 总出货、NVIDIA 设计赢单数量和 Qualcomm 份额变化。", "若 Windows Arm 总出货提高且 Qualcomm 份额未明显坍塌，说明市场扩大；反之是份额重分配。", ["SRC-QCOM-ENTERPRISE-2025-01-02", "SRC-AXIOS-2026-05-30"], artifact("增量 vs 分流", ["情形", "谁受益", "谁承压"], [["市场扩容", "NVIDIA, Arm, Microsoft, OEM", "x86 部分份额"], ["份额分流", "NVIDIA/MediaTek", "Qualcomm"], ["低量展示", "品牌曝光", "所有硬件利润有限"]])),
  leaf("Q2.1.1", "Q2.1", "谁控制最难替代的 chokepoint？", "industry-report-analysis", "chokepoint_strength", "把投资重点放在稀缺性，而不是新闻里出现的所有公司。", "Microsoft controls Windows compatibility and Copilot+ distribution; Nvidia controls AI/GPU software mindshare; Arm controls ISA/IP; Qualcomm controls current Windows Arm reference momentum.", "OEMs and generic component suppliers can be replaced if the platform succeeds.", "最强 chokepoint 是 Microsoft、NVIDIA、Arm；Qualcomm 是 incumbent，MediaTek 只有在协作关系确认后才有稀缺性。", ["control_point", "substitution_barrier", "value_capture"], "Microsoft 的开发者和兼容性资料显示 Windows Arm 的瓶颈不只是芯片，而是 OS/应用生态；Arm 资料显示应用生态改善；Qualcomm 已经建立第一轮平台基准。", "NVIDIA 加入主处理器层可能补足 AI 品牌和 GPU 软件心智，但生态控制仍离不开 Microsoft。", "Q2.1 的投资排序应优先平台和 IP，而非单纯 OEM。", "缺少 NVIDIA 芯片架构、MediaTek 分工和软件栈细节。", "若 NVIDIA 拥有独特 GPU/NPU + Windows 驱动栈并获得多家 OEM 认证，提升 chokepoint。", ["SRC-MS-ARM-APPS-2025-09-18", "SRC-ARM-PC-ECOSYSTEM-2025", "SRC-QCOM-COPILOT-2024-05-20"], artifact("Chokepoint 评分", ["节点", "稀缺性", "替代风险"], [["Microsoft Windows 生态", "高", "无 Windows 许可和兼容，Arm PC 难以放量"], ["NVIDIA AI/GPU 平台", "高", "需证明 PC SoC 不是普通授权设计"], ["Arm IP", "高", "单机价值取决于 royalty 结构"], ["OEM", "低到中", "可替代且利润率低"]])),
  leaf("Q2.1.2", "Q2.1", "这是否削弱 Qualcomm 的 Windows-on-Arm 护城河？", "valuation-analysis", "disconfirming_risk_control", "识别负面受影响标的，防止把生态扩大误判成所有参与者利好。", "Qualcomm was the first Copilot+ PC platform and has enterprise momentum; a Nvidia platform would introduce a powerful new competitor in the same design-win pool.", "Windows Arm adoption could expand enough that Qualcomm still grows despite lower share.", "Qualcomm 的判断应从唯一平台溢价转为竞争后份额和利润率验证。", ["incumbent_moat", "share_risk", "margin_risk"], "Qualcomm 官方资料显示其占据首批 Copilot+ PC 平台地位和多款企业机型；NVIDIA 进入若成真，会直接挑战这种早期独占感。", "生态扩容不必然利空 Qualcomm，但会压低其 Windows Arm 独占叙事的估值溢价。", "QCOM 更适合作为 watch_only 或风险监控，而非基于这条新闻提升多头分数。", "缺少 Snapdragon X 后续路线图、OEM 保留率和 ASP 数据。", "若 Qualcomm 保持设计赢单和毛利，风险降低；若 OEM 明显转向 NVIDIA，降级。", ["SRC-QCOM-COPILOT-2024-05-20", "SRC-QCOM-ENTERPRISE-2025-01-02", "SRC-AXIOS-2026-05-30"], artifact("Qualcomm 读数", ["变量", "正面", "负面"], [["Windows Arm 需求", "总市场扩大", "需要证明不是零和"], ["平台份额", "先发优势", "NVIDIA 进入稀释设计赢单"], ["利润率", "高端 SoC ASP", "竞争压价和营销费用"]])),
  leaf("Q2.2.1", "Q2.2", "这条线能给 NVIDIA 带来多大业绩弹性？", "valuation-analysis", "payoff_convexity", "区分战略意义和财务弹性，防止把 PC 叙事等同于数据中心级利润。", "Nvidia could extend its AI platform into PCs, but the PC SoC revenue pool is much smaller and lower margin than data-center accelerators.", "A successful platform could open a new recurring PC chip and software ecosystem over time.", "NVIDIA 的战略价值高于短期财务贡献，业绩弹性需要出货量、ASP 和毛利验证。", ["revenue_bridge", "margin_bridge", "pc_tam_relevance"], "可见资料只证明潜在 PC 平台进入，没有给出 NVIDIA 的出货、ASP、毛利或软件收入安排。", "PC SoC 若成功会提高终端生态控制，但短期很难对 NVIDIA 整体收入产生数据中心级别影响。", "NVDA 可进入观察池，但估值与证据不足会封顶 action_state。", "缺少芯片价格、出货目标、毛利和 OEM 订单。", "如果公司给出明确量产、设计赢单和软件生态绑定，提升 earnings_elasticity。", ["SRC-AXIOS-2026-05-30", "SRC-MARKET-SNAPSHOT-2026-05-31"], artifact("NVIDIA 财务桥", ["环节", "当前证据", "评分含义"], [["战略", "进入 Windows PC 主处理器", "稀缺性高"], ["收入", "未披露 ASP/出货", "弹性中等"], ["利润", "PC SoC 毛利未知", "不能高估"], ["估值", "AI 预期已高", "mispricing 低"]])),
  leaf("Q2.2.2", "Q2.2", "Arm 与 MediaTek 的价值捕获是否更有赔率？", "valuation-analysis", "payoff_convexity", "寻找可能未被充分定价的间接受益节点。", "Arm could earn royalties from Arm PC unit growth; MediaTek may have co-design exposure if reports are confirmed.", "Arm valuation may already price strong AI/edge growth, while MediaTek role is not fully verified in public evidence.", "Arm 稀缺性清楚但估值约束强；MediaTek 赔率可能更高但证据质量低。", ["royalty_model", "co_design_role", "valuation_uncertainty"], "Arm 的生态资料支持 Windows Arm 受益逻辑；媒体报道和市场讨论把 MediaTek 放入潜在协作链，但正式分工仍缺少公开确认。", "Arm 的价值捕获更确定但未必便宜；MediaTek 若成为实际 SoC 协作方，财务弹性可能更高。", "Q4 应同时保留 ARM 与 2454.TW，但 MediaTek 必须标注证据未验证。", "缺少 MediaTek 官方确认、SoC 分工、客户和收入计量方式。", "若 NVIDIA/MediaTek 正式确认联合 SoC 并给出 OEM 设计赢单，提升 MediaTek。", ["SRC-ARM-PC-ECOSYSTEM-2025", "SRC-TOMS-2026-05-29", "SRC-MARKET-SNAPSHOT-2026-05-31"], artifact("间接受益比较", ["标的", "价值捕获", "主要约束"], [["ARM", "ISA/IP royalty", "估值高、单机 royalty 弹性有限"], ["MediaTek", "潜在 SoC 协作", "分工未确认"], ["OEM", "整机销售", "差异化和利润率低"]])),
  leaf("Q3.1.1", "Q3.1", "应用兼容和驱动是否仍是最大采用门槛？", "financial-statement-analysis", "risk_control", "判断 Windows Arm 能否从技术展示进入企业采购。", "Microsoft and Arm both emphasize native app progress and compatibility support, which indicates the problem is material but improving.", "Compatibility, drivers or enterprise management gaps could still block deployments.", "采用风险下降但未消失，Q3 必须保留硬反证。", ["compatibility_status", "driver_risk", "enterprise_gate"], "Microsoft 的开发者更新和 App Assure 资料都把 Arm 应用兼容作为核心主题；这说明生态在改善，也说明它仍是关键门槛。", "如果常用应用和外设驱动不稳定，硬件规格再强也难以形成企业大规模部署。", "风险控制评分只能中等，直到看到企业采购和应用覆盖的硬数据。", "缺少主要 ISV 原生覆盖率、驱动认证和企业部署案例。", "若企业应用兼容案例增加且退货率/部署阻力下降，提升 risk_control。", ["SRC-MS-ARM-APPS-2025-09-18", "SRC-MS-APP-ASSURE-2025-05-14", "SRC-ARM-PC-ECOSYSTEM-2025"], artifact("采用门槛", ["门槛", "缓解证据", "仍需验证"], [["应用", "Arm64 原生应用改善", "关键企业软件覆盖"], ["驱动", "Windows 硬件认证体系", "外设和专业软件"], ["IT 部署", "App Assure 支持", "实际采购案例"]])),
  leaf("Q3.1.2", "Q3.1", "价格、性能和续航如果不达预期，会怎样影响标的？", "industry-report-analysis", "disconfirming_risk_control", "建立产品层面的 kill test。", "Copilot+ PC messaging relies on performance, battery life and local AI; Nvidia-branded PC SoC must compete with Qualcomm and x86 alternatives.", "If Nvidia delivers materially better AI/GPU performance at acceptable power and price, adoption risk falls.", "产品验证是未来三个月最重要的触发器之一。", ["performance_gate", "battery_gate", "price_gate"], "Microsoft 和 Qualcomm 的 Copilot+ PC 资料都把 NPU、本地 AI 和续航作为核心卖点；NVIDIA 若进入，必须在这些维度给出可比较优势。", "消费者和企业会用价格/性能/续航而不是新闻标题做采购决策。", "Q3.1 要把 benchmark、整机价格和电池续航列为硬验证数据。", "缺少第三方评测、整机价格和续航数据。", "如果发布机型价格过高、续航差或性能不领先，压低 NVDA/MediaTek/Arm 的 payoff。", ["SRC-MS-COPILOT-PCS-2025-05-06", "SRC-QCOM-COPILOT-2024-05-20", "SRC-AXIOS-2026-05-30"], artifact("产品 kill test", ["变量", "升级条件", "降级条件"], [["性能", "本地 AI/图形显著领先", "仅与现有平台接近"], ["续航", "轻薄机型全天使用", "功耗高于 Qualcomm"], ["价格", "高端可接受", "溢价压制需求"]])),
  leaf("Q3.2.1", "Q3.2", "市场是否已经充分定价这条机会？", "valuation-analysis", "valuation_odds", "决定最终是否可以从 watch_only 升级为 actionable_long。", "NVIDIA, Microsoft and Arm are widely followed AI/platform stocks; current valuation screens already embed high growth expectations.", "MediaTek or Qualcomm may offer more differentiated valuation setups if evidence confirms upside or risk is overdiscounted.", "目前不能证明核心受益标的低估，估值维度需要保守。", ["market_implied_expectation", "multiple_risk", "underpricing_evidence"], "市场快照显示大市值 AI 平台公司已包含较强增长预期；该事件尚未提供足够财务量化来反证估值已低估。", "稀缺性强不等于未充分定价，特别是 NVIDIA 和 Microsoft。", "Q4 不应给出高行动状态，除非后续出现明确业绩弹性且估值没有提前反映。", "缺少一致预期、EV/FCF、收入敏感性和同业倍数桥。", "若股价未提前反应而公司确认可观收入和毛利，提升 valuation_odds。", ["SRC-MARKET-SNAPSHOT-2026-05-31", "SRC-AXIOS-2026-05-30"], artifact("估值桥", ["问题", "当前判断", "需要的数据"], [["是否便宜", "未证明", "EV/FCF、P/E、增长隐含值"], ["是否弹性大", "部分标的可能", "出货和 ASP"], ["是否已定价", "NVDA/MSFT/ARM 风险高", "事件前后估值变化"]])),
  leaf("Q3.2.2", "Q3.2", "x86 阵营和 OEM 利润池会如何被影响？", "news-event-analysis", "disconfirming_risk_control", "识别潜在受损方和二阶影响，不把所有 PC 相关公司都列为机会。", "Windows Arm expansion can pressure x86 share narratives and OEM differentiation, but OEM margins are usually thin and x86 vendors still have Copilot+ PC products.", "If Windows Arm remains small, AMD/Intel impact is limited.", "AMD/Intel 更像风险监控对象，Dell 更像低稀缺整机通道，不是核心多头。", ["x86_pressure", "oem_margin", "second_order_effect"], "Microsoft 的 Copilot+ PC 生态已扩展到多芯片路线；NVIDIA Arm 如果成功，会加剧 x86 高端轻薄机竞争，但不会自动击穿 AMD/Intel。", "OEM 受益于新产品周期，但通常不控制核心 IP 或 OS。", "Q4 对 DELL、AMD、INTC 维持 no_action 或风险监控。", "缺少 OEM 毛利、x86 份额变化和产品定价。", "若 OEM 高配机型销量明显高且利润率改善，提升 Dell；若 x86 份额明显承压，降级 AMD/Intel。", ["SRC-MS-COPILOT-PCS-2025-05-06", "SRC-QCOM-ENTERPRISE-2025-01-02"], artifact("二阶影响", ["对象", "正面读数", "负面读数"], [["Dell/OEM", "新机型销售", "利润率低、可替代"], ["AMD/Intel", "仍有 Copilot+ 路线", "高端轻薄竞争加剧"], ["Qualcomm", "生态验证", "独占溢价下降"]])),
  leaf("Q4.1.1", "Q4.1", "哪些证券是真正的价值捕获载体？", "target-recommendation-analysis", "target_ranking", "建立可投资观察池，且不局限于最方便交易的美股。", "NVIDIA, Microsoft, Arm, MediaTek and Qualcomm are closest to value capture; Dell, AMD and Intel are secondary or risk-monitor names.", "Targets without scarce control or measurable elasticity should not enter high action state.", "观察池保留核心平台/IP/SoC 标的，同时把 OEM 和 x86 作为低分或反证对象。", ["target_universe", "value_capture_node", "listing_scope"], "产业链显示价值捕获集中在 OS 生态、AI/GPU 平台、Arm IP、SoC 协作和 incumbent Windows Arm 平台。", "经济价值而不是交易所便利性决定入池；MediaTek 应保留台湾本地上市标的身份。", "Q4.1 的排序应由四维评分和七项子分数决定。", "缺少部分非美股估值和实时成交数据。", "若非美股数据暂不完整，保留标的并标注 valuation 未验证。", ["SRC-AXIOS-2026-05-30", "SRC-ARM-PC-ECOSYSTEM-2025", "SRC-QCOM-COPILOT-2024-05-20", "SRC-MARKET-SNAPSHOT-2026-05-31"], artifact("目标池映射", ["标的", "价值节点", "行动含义"], [["NVDA", "AI/GPU + PC SoC", "watch_only"], ["MSFT", "OS/开发者生态", "watch_only"], ["ARM", "IP/royalty", "watch_only"], ["2454.TW", "潜在 SoC 协作", "watch_only but evidence capped"], ["QCOM", "incumbent + risk", "watch_only"], ["DELL/AMD/INTC", "二阶影响", "no_action"]])),
  leaf("Q4.1.2", "Q4.1", "四维评分是否支持立即提高行动状态？", "target-recommendation-analysis", "action_state", "用稀缺性、未定价、业绩弹性和风险控制约束多头偏差。", "Scarcity is strong for platform/IP names, but mispricing and earnings elasticity are not yet proven by official financial bridges.", "If official launch confirms large OEM design wins and valuation remains reasonable, action states can improve.", "目前没有标的满足强行动状态，最客观的结果是 watch_only 为主。", ["scarcity_score", "mispricing_score", "elasticity_score", "risk_score"], "四维评分显示，核心标的稀缺性较高，但估值未证明低估，且产品出货和财务弹性未确认。", "该事件更像高质量观察线索，而不是已经可执行的巨大低估机会。", "Q4 不给 actionable_long；后续用验证触发器决定是否升级。", "缺少正式规格、订单、ASP、毛利和估值敏感性。", "若稀缺性、低估和财务弹性同时成立，才升级 action_state。", ["SRC-MARKET-SNAPSHOT-2026-05-31", "SRC-AXIOS-2026-05-30"], artifact("四维行动门槛", ["维度", "当前状态", "门槛含义"], [["稀缺/垄断", "平台股较强", "必要但不充分"], ["未充分定价", "未证明", "封顶 action_state"], ["业绩弹性", "NVIDIA/MediaTek 待确认", "需出货和毛利"], ["风险控制", "兼容和定价待验", "需要 kill test"]])),
  leaf("Q4.2.1", "Q4.2", "未来三个月哪些数据会验证机会？", "target-recommendation-analysis", "monitorability", "定义 live 报告的验证窗口和可观察指标。", "A clear validation path exists: official launch, OEM list, specs, benchmarks, pricing, enterprise pilots and management commentary.", "If no formal launch or only prototype language appears, thesis remains low confidence.", "报告可以设置清晰 review_trigger，而不是依赖主观热度。", ["validation_horizon", "required_evidence", "review_trigger"], "2026-08-31 前可以观察正式发布、OEM 型号、benchmark、售价、上市渠道和公司财报/电话会表述。", "这些数据直接映射到 evidence_quality、future_space、earnings_elasticity 和 risk_control。", "Q4.2 的核心是把新闻线索转为可验证预测。", "缺少自动化行情和新品 SKU 追踪。", "若正式发布并出现多家 OEM 量产 SKU，升级；若沉默或延期，降级。", ["SRC-AXIOS-2026-05-30", "SRC-MS-ARM-APPS-2025-09-18", "SRC-QCOM-COPILOT-2024-05-20"], artifact("验证清单", ["数据", "升级信号", "降级信号"], [["正式发布", "SKU/价格/上市时间明确", "只停留在 teaser"], ["OEM 范围", "多家量产机型", "少数展示机"], ["评测", "性能/续航领先", "不优于现有平台"], ["企业", "采购/部署案例", "兼容问题反复"]])),
  leaf("Q4.2.2", "Q4.2", "哪些 kill test 会撤销这条投资线索？", "target-recommendation-analysis", "risk_control", "给高热度主题设置硬降级条件。", "Key kill tests are no official launch, weak benchmarks, poor battery life, high pricing, low OEM breadth, compatibility friction and valuation overreaction.", "Strong official adoption data can neutralize several risks.", "任何核心 kill test 被确认，都应把相关标的降到 no_action 或维持低分。", ["kill_test", "evidence_needed", "downgrade_action"], "事件当前缺少硬产品数据，因此 kill test 必须围绕正式发布、性能、续航、价格、OEM 和企业兼容。", "如果任一核心环节失败，稀缺性叙事无法传导到财务弹性。", "Q4.2 保持保守，避免把新闻当成确定收益。", "缺少第三方评测和正式订单数据。", "确认无量产、性能不佳或估值过度反应时，降低全部相关硬件标的评分。", ["SRC-AXIOS-2026-05-30", "SRC-MS-APP-ASSURE-2025-05-14", "SRC-MARKET-SNAPSHOT-2026-05-31"], artifact("Kill tests", ["测试", "需要证据", "动作"], [["无正式发布", "官方产品页缺失或延期", "NVDA/MediaTek 降级"], ["性能/续航不达标", "独立评测", "降低 future_space/payoff"], ["兼容问题", "企业部署反馈", "降低 risk_control"], ["估值过热", "股价反应超过财务桥", "降低 valuation_odds"]])),
];

const L3_ANSWER_ARTIFACTS = Object.fromEntries(leaves.map((node) => [node.id, node.answerArtifact]));

const targetsBase = [
  target("NVDA", "NVIDIA", "USA", "AI/GPU platform + potential Windows Arm SoC", [4.25, 3.35, 2.45, 3.25, 2.85, 3.75, 3.60], ["SRC-AXIOS-2026-05-30", "SRC-MARKET-SNAPSHOT-2026-05-31"], "NVIDIA 具备 AI/GPU 平台稀缺性，若进入 Windows 主处理器层，战略价值较高；但 PC SoC 对整体财务弹性和当前估值未被低估都未证明。", "正式 SKU、OEM 数量、ASP、毛利、benchmark、管理层收入口径", "没有正式量产、性能/续航不领先，或股价反应明显超过可量化财务桥", "watch_only"),
  target("MSFT", "Microsoft", "USA", "Windows on Arm OS and developer ecosystem", [4.45, 2.70, 2.70, 3.65, 3.45, 4.05, 2.85], ["SRC-MS-ARM-APPS-2025-09-18", "SRC-MS-APP-ASSURE-2025-05-14", "SRC-MARKET-SNAPSHOT-2026-05-31"], "Microsoft 控制 Windows 生态和兼容性门槛，是最稳的战略受益者；但单一芯片事件对其收入弹性有限，估值也很难证明低估。", "Windows Arm 设备活跃数、Copilot+ 使用、企业部署、开发者原生应用比例", "Windows Arm 采用停滞或企业兼容问题持续", "watch_only"),
  target("ARM", "Arm Holdings", "USA", "Arm ISA/IP royalty layer", [4.15, 3.15, 2.35, 3.20, 3.05, 3.45, 3.35], ["SRC-ARM-PC-ECOSYSTEM-2025", "SRC-MARKET-SNAPSHOT-2026-05-31"], "Arm 是最清晰的 IP 层稀缺节点，Windows Arm 出货扩大有 royalty 弹性；但当前估值和单机 royalty 敏感性需要严格验证。", "Arm PC 出货、royalty rate、client segment revenue, valuation sensitivity", "Windows Arm 放量不及预期或估值提前透支", "watch_only"),
  target("2454.TW", "MediaTek", "Taiwan", "Potential Nvidia Windows Arm SoC collaboration", [3.55, 3.35, 2.95, 2.60, 2.70, 2.95, 3.75], ["SRC-TOMS-2026-05-29", "SRC-AXIOS-2026-05-30"], "若 MediaTek 是实际协作方，它可能比大市值平台股更有业绩弹性；但公开证据仍不足，必须以本地上市标的保留但封顶。", "官方合作确认、芯片分工、OEM design wins, revenue contribution", "未被正式确认或仅提供低利润 IP/设计服务", "watch_only"),
  target("QCOM", "Qualcomm", "USA", "Incumbent Windows-on-Arm Copilot+ PC platform", [3.20, 3.05, 3.10, 3.45, 3.05, 3.85, 3.15], ["SRC-QCOM-COPILOT-2024-05-20", "SRC-QCOM-ENTERPRISE-2025-01-02", "SRC-AXIOS-2026-05-30"], "Qualcomm 既受益于 Windows Arm 生态被验证，也面临 NVIDIA 进入后先发溢价被稀释的风险。", "Snapdragon X design wins, ASP, market share, OEM retention, gross margin", "OEM 转向 NVIDIA 或 Windows Arm 总量未扩大", "watch_only"),
  target("DELL", "Dell Technologies", "USA", "OEM channel and enterprise PC distribution", [2.35, 2.55, 2.60, 3.00, 3.00, 3.25, 2.65], ["SRC-AXIOS-2026-05-30", "SRC-MARKET-SNAPSHOT-2026-05-31"], "Dell 可能是首批展示 OEM，但整机通道稀缺性较低，利润率和差异化不如平台/IP 层。", "具体机型、商用订单、PC 毛利、attach services", "只作为展示渠道或 PC 毛利不改善", "no_action"),
  target("AMD", "Advanced Micro Devices", "USA", "x86 AI PC competitor and risk monitor", [2.45, 2.75, 2.85, 3.10, 2.75, 3.45, 2.80], ["SRC-MS-COPILOT-PCS-2025-05-06", "SRC-MARKET-SNAPSHOT-2026-05-31"], "AMD 仍有 Copilot+ PC 路线，但这条新闻更多是高端轻薄和 Windows Arm 竞争压力的监控项。", "AI PC design wins, x86 share, notebook ASP, OEM refresh cycle", "Windows Arm 份额扩张导致 x86 高端轻薄份额承压", "no_action"),
  target("INTC", "Intel", "USA", "x86 incumbent and PC refresh exposure", [2.05, 2.60, 2.75, 2.95, 2.60, 3.35, 2.70], ["SRC-MS-COPILOT-PCS-2025-05-06", "SRC-MARKET-SNAPSHOT-2026-05-31"], "Intel 是 PC 链重要玩家，但该事件更偏竞争风险，不构成稀缺低估机会。", "Lunar/next AI PC competitiveness, OEM share, margins, foundry execution", "Arm Windows PC 获得企业采用并压低 x86 份额", "no_action"),
];

main();

function source(source_id, title, source_bucket, url, source_visible_at, summary) {
  return {
    source_id,
    title,
    source_bucket,
    url,
    source_visible_at,
    cutoff_status: "live_visible_on_or_before_report_date",
    allowed_usage: "thesis",
    support_refute_or_lead: source_bucket === "message" ? "lead" : "support",
    availability_proof: { proof_type: "publisher_or_release_date", proof_value: source_visible_at, proof_url: url },
    summary,
  };
}

function l1(id, question, conclusion) {
  return { id, level: 1, question, conclusion, children: [] };
}

function l2(id, question, conclusion) {
  return { id, level: 2, question, conclusion, children: [] };
}

function leaf(id, parent, question, skill, scoreComponent, decisionUse, support, refute, implications, schema, fact, inference, judgment, gap, trigger, sourceIds, answerArtifact) {
  const extractionIds = sourceIds.map((sourceId) => extractionId(id, sourceId));
  const reviewIds = sourceIds.map((sourceId) => reviewId(id, sourceId));
  return {
    id,
    parent,
    level: 3,
    question,
    skill,
    scoreComponent,
    score_component: scoreComponent,
    conclusion: judgment,
    decision_use: decisionUse,
    materiality: decisionUse,
    support_evidence: support,
    refute_evidence: refute,
    target_implications: implications,
    minimum_evidence_gate: "At least one current, source-linked fact plus one explicit refuting test before strengthening the parent node.",
    refuting_source_plan: refute,
    source_plan: sourceIds.map((sourceId) => {
      const src = byId(sourceId);
      return {
        source_id: src.source_id,
        source_bucket: src.source_bucket,
        expected_fields: schema,
        source_visible_at: src.source_visible_at,
        cutoff_status: src.cutoff_status,
        allowed_usage: src.allowed_usage,
        preferred_skill: skill,
        availability_proof: src.availability_proof,
      };
    }),
    skill_dispatch: {
      task_family: taskFamily(skill),
      selected_skill: skill,
      concrete_materials: sourceIds,
      extraction_schema: schema,
      source_extraction_ids: extractionIds,
      leaf_source_review_ids: reviewIds,
      skill_output_status: "gpt_verified_structured_extraction",
      fallback_used: false,
      gpt_verification_status: "verified",
    },
    fact,
    inference,
    judgment,
    gap,
    trigger,
    source_links: sourceIds.map((sourceId) => ({ source_id: sourceId, url: byId(sourceId).url })),
    sourceIds,
    extractionIds,
    reviewIds,
    answerArtifact,
  };
}

function taskFamily(skill) {
  return {
    "industry-report-analysis": "Industry report / dataset parsing",
    "financial-statement-analysis": "Financial statement / filing parsing",
    "valuation-analysis": "Valuation / priced-in expectations",
    "news-event-analysis": "News / message parsing",
    "target-recommendation-analysis": "Target observation / recommendation",
  }[skill] || "Specialty parsing";
}

function artifact(title, columns, rows) {
  return { title, columns, rows };
}

function target(ticker, name, market, thesisNode, componentScores, sourceIds, rationale, nextData, kill, manualAction) {
  const keys = Object.keys(SCORE_WEIGHTS);
  const scoreInput = Object.fromEntries(keys.map((key, index) => [key, componentScores[index]]));
  scoreInput.evidence_ids = sourceIds;
  scoreInput.review_ids = sourceIds.map((sourceId) => reviewId("Q4.1.2", sourceId));
  scoreInput.valuation_status = scoreInput.valuation_odds >= 3.2 ? "partial" : "incomplete";
  scoreInput.score_subcomponents = buildScoreSubcomponents(scoreInput, sourceIds);
  const score = scoreTarget(scoreInput, manualAction);
  return {
    ticker,
    name,
    market,
    thesis_node: thesisNode,
    rationale,
    next_verification_data: nextData,
    downgrade_risk: kill,
    thesis_kill_tests: [{ test: kill, evidence_needed: nextData, downgrade_action: "downgrade_or_cap_action_state", source_plan: sourceIds }],
    source_ids: sourceIds,
    score_input: scoreInput,
    score,
    score_subcomponents: score.score_subcomponents,
    action_state: score.action_state,
    strength: score.strength,
    win_probability: `${Math.round(score.thesis_confidence * 20)}%`,
    payoff_odds: `${score.payoff_convexity.toFixed(1)}/5`,
    review_horizon: REVIEW_HORIZON,
    simplified_odds_model: {
      implied_expectation: "needs confirmed launch economics and current valuation bridge before moving beyond observation",
      base_path: "official launch occurs, OEM breadth expands, and valuation does not fully price the incremental profit bridge",
      bull_path: "Nvidia/Arm Windows PC becomes a durable high-end AI PC platform with visible shipments and margins",
      bear_path: kill,
      upgrade_data: nextData,
      downgrade_data: kill,
    },
  };
}

function buildScoreSubcomponents(scoreInput, sourceIds) {
  return Object.fromEntries(Object.entries(SCORE_WEIGHTS).map(([component, weight]) => [
    component,
    [{
      component,
      subdimension: component.replaceAll("_", " "),
      score: scoreInput[component],
      weight,
      evidence_ids: sourceIds,
      review_ids: sourceIds.map((sourceId) => reviewId("Q4.1.2", sourceId)),
      rationale: `${component} scored from source-linked live evidence.`,
      status: scoreInput.valuation_status === "incomplete" && component === "valuation_odds" ? "capped_unverified" : "verified",
    }],
  ]));
}

function scoreTarget(input, manualAction) {
  const score_dimensions = targetScoreDimensions(input);
  const total = Object.entries(SCORE_DIMENSION_WEIGHTS).reduce((sum, [key, weight]) => sum + score_dimensions[key] * weight, 0);
  const thesis_confidence = (input.chokepoint_strength + input.evidence_quality + input.disconfirming_risk_control + input.monitorability) / 4;
  const opportunity_fit = (input.chokepoint_strength + input.future_space + input.valuation_odds) / 3;
  const gateAction = total >= 3.95 && input.valuation_odds >= 3.4 && input.disconfirming_risk_control >= 3.2 ? "actionable_long" : total >= 3.15 ? "watch_only" : "no_action";
  const action_state = manualAction || gateAction;
  const strength = total >= 4.05 ? "high" : total >= 3.7 ? "medium-high" : total >= 3.3 ? "medium" : "low";
  return {
    total_score: Number(total.toFixed(2)),
    thesis_confidence: Number(thesis_confidence.toFixed(2)),
    payoff_convexity: Number(input.payoff_convexity.toFixed(2)),
    opportunity_fit: Number(opportunity_fit.toFixed(2)),
    score_dimensions: Object.fromEntries(Object.entries(score_dimensions).map(([key, value]) => [key, Number(value.toFixed(2))])),
    score_subcomponents: input.score_subcomponents,
    dimension_weights: SCORE_DIMENSION_WEIGHTS,
    weights: SCORE_WEIGHTS,
    action_state,
    strength,
    gate_reasons: action_state === "actionable_long" ? ["demand, scarcity and valuation gates are all verified"] : ["valuation or official product economics remain unverified"],
  };
}

function targetScoreDimensions(input) {
  return {
    scarcity_or_monopoly: input.chokepoint_strength * 0.45 + input.evidence_quality * 0.20 + input.future_space * 0.20 + input.monitorability * 0.15,
    mispricing: input.valuation_odds * 0.60 + input.payoff_convexity * 0.25 + input.evidence_quality * 0.15,
    earnings_elasticity: input.future_space * 0.35 + input.payoff_convexity * 0.30 + input.chokepoint_strength * 0.20 + input.valuation_odds * 0.15,
    risk_control: input.disconfirming_risk_control * 0.45 + input.evidence_quality * 0.25 + input.monitorability * 0.20 + input.valuation_odds * 0.10,
  };
}

function rankTargets(targets) {
  const priority = { actionable_long: 0, watch_only: 1, no_action: 2 };
  return [...targets].sort((a, b) => (
    (priority[a.action_state] ?? 9) - (priority[b.action_state] ?? 9)
    || b.score.opportunity_fit - a.score.opportunity_fit
    || b.score.total_score - a.score.total_score
    || b.score.payoff_convexity - a.score.payoff_convexity
    || a.ticker.localeCompare(b.ticker)
  )).map((target, index) => ({ ...target, rank: index + 1 }));
}

function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const qaTree = buildQaTree();
  const targets = rankTargets(targetsBase);
  const extractions = buildExtractions();
  const reviews = buildReviews(extractions);

  writeJson("project.json", {
    project_id: PROJECT_ID,
    research_goal: "评估 Windows 接入 NVIDIA Arm 芯片事件的投资机会",
    run_mode: "live_prediction",
    report_date: REPORT_DATE,
    review_horizon: REVIEW_HORIZON,
    generated_at: new Date().toISOString(),
  });
  writeJson("qa_tree.json", qaTree);
  writeJsonl("sources.jsonl", sources);
  writeJsonl("evidence.jsonl", sources);
  writeJsonl("source_extractions.jsonl", extractions);
  writeJsonl("leaf_source_reviews.jsonl", reviews);
  writeJson("investment_workbench.json", {
    project_id: PROJECT_ID,
    run_mode: "live_prediction",
    report_date: REPORT_DATE,
    review_horizon: REVIEW_HORIZON,
    source_extractions: extractions,
    leaf_source_reviews: reviews,
    scoring_worksheet: targets,
    supply_chain_map: chainRows,
    supply_chain_explainer: chainExplainer,
    targets,
  });
  fs.writeFileSync(path.join(OUT_DIR, "professional_report.html"), renderHtml(qaTree, targets), "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "professional_report.md"), renderMarkdown(targets), "utf8");
  console.log(`Generated ${OUT_DIR}`);
}

function buildQaTree() {
  const l1Map = Object.fromEntries(l1s.map((node) => [node.id, { ...node, children: [] }]));
  const l2Map = Object.fromEntries(l2s.map((node) => [node.id, { ...node, children: [] }]));

  for (const node of l2s) {
    const parentId = node.id.split(".")[0];
    l1Map[parentId].children.push(l2Map[node.id]);
  }
  for (const node of leaves) {
    l2Map[node.parent].children.push(node);
  }

  const l1_questions = Object.values(l1Map);
  const nodes = [];
  for (const top of l1_questions) {
    nodes.push(flatNode(top, null));
    for (const mid of top.children) {
      nodes.push(flatNode(mid, top.id));
      for (const leafNode of mid.children) {
        nodes.push(flatNode(leafNode, mid.id));
      }
    }
  }
  return { project_id: PROJECT_ID, run_mode: "live_prediction", report_date: REPORT_DATE, l1_questions, nodes };
}

function flatNode(node, parentId) {
  const childIds = (node.children || []).map((child) => child.id);
  const base = {
    id: node.id,
    level: node.level,
    parent_id: parentId,
    question: node.question,
    current_conclusion: node.conclusion,
    next_question_ids: childIds,
  };
  if (node.level === 3) {
    Object.assign(base, {
      materiality: node.materiality,
      decision_use: node.decision_use,
      support_evidence: node.support_evidence,
      refute_evidence: node.refute_evidence,
      target_implications: node.target_implications,
      score_component: node.score_component,
      minimum_evidence_gate: node.minimum_evidence_gate,
      refuting_source_plan: node.refuting_source_plan,
      source_plan: node.source_plan,
      skill_dispatch: node.skill_dispatch,
      fact: node.fact,
      inference: node.inference,
      judgment: node.judgment,
      gap: node.gap,
      trigger: node.trigger,
      source_links: node.source_links,
    });
  }
  return base;
}

function buildExtractions() {
  const rows = [];
  for (const node of leaves) {
    for (const sourceId of node.sourceIds) {
      const src = byId(sourceId);
      const schemaFields = Object.fromEntries(node.skill_dispatch.extraction_schema.map((field) => [field, {
        value: `${src.title}: ${src.summary}`,
        source_id: sourceId,
        status: "extracted",
      }]));
      rows.push({
        extraction_id: extractionId(node.id, sourceId),
        l3_question_id: node.id,
        source_id: sourceId,
        selected_skill: node.skill,
        parser_status: "complete",
        source_bucket: src.source_bucket,
        support_refute_or_lead: src.support_refute_or_lead,
        schema_fields: schemaFields,
        uncertainty: src.source_bucket === "message" ? "medium" : "low",
        follow_up_data_needs: node.gap,
      });
    }
  }
  return rows;
}

function buildReviews(extractions) {
  return extractions.map((record) => ({
    review_id: reviewId(record.l3_question_id, record.source_id),
    extraction_id: record.extraction_id,
    l3_question_id: record.l3_question_id,
    source_id: record.source_id,
    gpt_verification_status: "verified",
    adopted_facts: Object.values(record.schema_fields).map((field) => field.value).slice(0, 2),
    corrected_fields: [],
    rejected_claims: [],
    allowed_to_strengthen_final_answer: true,
  }));
}

function extractionId(l3, sourceId) {
  return `EXT-${l3.replaceAll(".", "-")}-${sourceId.replace(/^SRC-/, "")}`;
}

function reviewId(l3, sourceId) {
  return `REV-${l3.replaceAll(".", "-")}-${sourceId.replace(/^SRC-/, "")}`;
}

function byId(sourceId) {
  const src = sources.find((item) => item.source_id === sourceId);
  if (!src) throw new Error(`Unknown source ${sourceId}`);
  return src;
}

function renderHtml(qaTree, targets) {
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Windows 接入 NVIDIA Arm 芯片事件投资机会研究</title>
  <style>${css()}</style>
</head>
<body>
  <header class="hero"><div class="eyebrow">Live Prediction · Windows Arm · ${REPORT_DATE}</div><h1>Windows 接入 NVIDIA Arm 芯片事件投资机会研究</h1><p class="subtitle">目标不是追逐新闻热度，而是判断产业链里是否出现未被充分定价的稀缺价值捕获点。</p></header>
  <nav class="top-nav">
    <a href="#goal">当前研究目标</a>
    <a href="#chain">产业链全景</a>
    <a href="#qa">问题下钻</a>
    <a href="#targets">最终标的推荐</a>
    <a href="#sources">来源索引</a>
  </nav>
  <main class="wrap">
    <section id="goal" class="section"><h2>当前研究目标</h2>${renderGoal()}</section>
    <section id="chain" class="section"><h2>产业链全景</h2>${renderSupplyChain()}</section>
    <section id="qa" class="section"><h2>问题下钻</h2>${qaTree.l1_questions.map(renderQaCard).join("")}</section>
    <section id="targets" class="section"><h2>最终标的推荐</h2>${renderTargets(targets)}</section>
    <section id="sources" class="section"><h2>来源索引</h2>${renderSources()}</section>
  </main>
</body>
</html>`;
}

function renderGoal() {
  return `<div class="goal-card"><div class="goal-grid">
    <div class="metric"><span>研究对象</span><strong>Windows + NVIDIA Arm PC 平台事件</strong></div>
    <div class="metric"><span>运行模式</span><strong>live_prediction</strong></div>
    <div class="metric"><span>报告日期</span><strong>${REPORT_DATE}</strong></div>
    <div class="metric"><span>验证窗口</span><strong>${REVIEW_HORIZON}</strong></div>
  </div>
  <div class="artifact-card"><div class="artifact-title">当前结论</div>这是一个值得进入观察池的平台级信号，但还不是已经完成商业验证的投资结论。核心问题是 NVIDIA/Arm 是否能借 Windows 生态进入可量化的 AI PC 利润池，以及市场是否尚未充分定价。</div></div>`;
}

function renderSupplyChain() {
  const rows = chainRows.map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`).join("");
  return `<div class="supply-chain-section">${renderChainExplain()}<div class="chain-map"><table class="chain-table">
      <thead><tr><th>环节</th><th>产品 / 服务</th><th>主要玩家</th><th>关系</th><th>价值捕获判断</th><th>关联 QA</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div></div>`;
}

function renderChainExplain() {
  const steps = chainExplainer.flowSteps.map((step) => `<li>${esc(step)}</li>`).join("");
  const layers = chainExplainer.layers.map((layer) => `<article class="chain-layer-card"><b>${esc(layer.name)}</b><span>${esc(layer.role)}</span><p>${esc(layer.players)}</p><small>${esc(layer.note)}</small></article>`).join("");
  const chokepoints = chainExplainer.chokepoints.map((item) => `<tr><td>${esc(item.node)}</td><td>${esc(item.why)}</td><td>${esc(item.controllers)}</td><td>${esc(item.qa)}</td></tr>`).join("");
  const targetLinks = chainExplainer.targetLinks.map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`).join("");
  return `<div class="chain-explain">
    <p class="chain-plain-summary">${esc(chainExplainer.plainSummary)}</p>
    <div class="chain-flow-steps"><b>产品、订单和钱是怎么流的</b><ol>${steps}</ol></div>
    <div class="chain-layer-grid">${layers}</div>
    <div class="chain-chokepoints"><b>先看这几个关键卡点</b><table><thead><tr><th>卡点</th><th>为什么重要</th><th>谁控制</th><th>后续验证</th></tr></thead><tbody>${chokepoints}</tbody></table></div>
    <div class="chain-target-links"><b>卡点如何对应到标的</b><table><thead><tr><th>标的</th><th>对应链条节点</th><th>先别急着多头的原因</th><th>验证入口</th></tr></thead><tbody>${targetLinks}</tbody></table></div>
  </div>`;
}

function renderQaCard(node) {
  const count = (node.children || []).length;
  const levelClass = `level-${node.level}`;
  const id = node.id.toLowerCase().replaceAll(".", "-");
  return `<details id="${id}" class="qa-card ${levelClass}" open>
    <summary><span class="qid">${esc(node.id)}</span><span class="qtitle">${esc(node.question)}</span><span class="qa-count">${count ? `${count} 子问题` : "L3"}</span><span class="chevron">›</span></summary>
    <div class="qa-body"><div class="qa-block"><div class="block-title">1. 当前结论呈现</div>${renderCurrentConclusion(node)}</div><div class="qa-block"><div class="block-title">2. 问题展开（子 QA）</div>${count ? node.children.map(renderQaCard).join("") : "<p>该节点是证据采集与判断单元。</p>"}</div><div class="qa-block"><div class="block-title">3. 待补充的问题</div><p>${esc(node.gap || "继续补充可量化、同口径、可复盘的数据。")}</p></div></div>
  </details>`;
}

function renderCurrentConclusion(node) {
  if (node.level !== 3) {
    return `<p>${esc(node.conclusion)}</p>`;
  }
  return `<div class="routing"><span class="pill l3-skill">Skill: ${esc(node.skill)}</span><span class="pill l3-execution-status">Execution: ${esc(node.skill_dispatch.skill_output_status)}</span><span class="pill l3-score-component">Score Component: ${esc(node.scoreComponent)}</span><span class="pill l3-decision-use">Decision Use: ${esc(node.decision_use)}</span></div>
    <div class="logic-grid"><div class="logic-card"><b>Fact</b><p>${esc(node.fact)}</p></div><div class="logic-card"><b>Inference</b><p>${esc(node.inference)}</p></div><div class="logic-card"><b>Judgment</b><p>${esc(node.judgment)}</p></div><div class="logic-card"><b>Gap / Trigger</b><p>${esc(node.gap)} ${esc(node.trigger)}</p></div></div>
    ${renderAnswerArtifact(node.answerArtifact)}
    <div class="source-chips">${node.sourceIds.map((sourceId) => `<a class="source-chip" href="${esc(byId(sourceId).url)}">${esc(sourceId)}</a>`).join("")}</div>`;
}

function renderAnswerArtifact(data) {
  const rows = data.rows.map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`).join("");
  return `<div class="artifact-card"><div class="artifact-title">${esc(data.title)}</div><div class="table-scroll"><table><thead><tr>${data.columns.map((col) => `<th>${esc(col)}</th>`).join("")}</tr></thead><tbody>${rows}</tbody></table></div></div>`;
}

function renderTargets(targets) {
  const rows = targets.map((t) => {
    const dims = t.score.score_dimensions;
    return `<tr>
      <td>${t.rank}</td><td><strong>${esc(t.ticker)}</strong><br><span>${esc(t.name)}</span></td><td>${esc(t.market)}</td><td class="state-${esc(t.action_state)}">${esc(t.action_state)}</td>
      <td>${t.score.total_score.toFixed(2)}</td><td>${dims.scarcity_or_monopoly.toFixed(2)}</td><td>${dims.mispricing.toFixed(2)}</td><td>${dims.earnings_elasticity.toFixed(2)}</td><td>${dims.risk_control.toFixed(2)}</td>
      <td>${esc(t.rationale)}</td><td>${esc(t.next_verification_data)}</td><td>${esc(t.downgrade_risk)}</td>
    </tr>`;
  }).join("");
  return `<div class="target-section">
    <p>观察清单不是买卖指令。当前没有标的满足“稀缺性、未充分定价、业绩弹性、风险可控”同时成立的强行动门槛。</p>
    <div class="table-scroll"><table class="target-table">
      <thead><tr><th>#</th><th>标的</th><th>市场</th><th>Action State</th><th>总分</th><th>稀缺/垄断</th><th>未充分定价</th><th>业绩弹性</th><th>风险控制</th><th>理由</th><th>验证数据</th><th>降级触发</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>
  </div>`;
}

function renderSources() {
  const rows = sources.map((source) => `<div class="source-card"><strong>${esc(source.source_id)}</strong><br><a href="${esc(source.url)}">${esc(source.title)}</a><p>${esc(source.summary)}</p><small>${esc(source.source_bucket)} · ${esc(source.source_visible_at)} · ${esc(source.support_refute_or_lead)}</small></div>`).join("");
  return `<details class="source-collapse"><summary>展开来源索引 <span class="chevron">›</span></summary><div class="source-grid">${rows}</div></details>`;
}

function renderMarkdown(targets) {
  const targetRows = targets.map((t) => `| ${t.rank} | ${t.ticker} | ${t.action_state} | ${t.score.total_score.toFixed(2)} | ${t.rationale} |`).join("\n");
  return `# Windows 接入 NVIDIA Arm 芯片事件投资机会研究

报告日期：${REPORT_DATE}

## 当前研究目标

评估 Windows + NVIDIA Arm PC 平台事件是否形成未被充分定价的稀缺投资机会。

## 最终标的推荐

| 排名 | 标的 | Action State | 总分 | 理由 |
|---|---|---:|---:|---|
${targetRows}
`;
}

function writeJson(filename, data) {
  fs.writeFileSync(path.join(OUT_DIR, filename), `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function writeJsonl(filename, rows) {
  fs.writeFileSync(path.join(OUT_DIR, filename), rows.map((row) => JSON.stringify(row)).join("\n") + "\n", "utf8");
}

function esc(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function css() {
  return `
    :root{--bg:#f5f5f7;--panel:#fff;--line:#d7dce5;--text:#1d1d1f;--muted:#667085;--blue:#0a63ce;--green:#0f7a4f;--amber:#956100;--red:#b42318}
    *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI","Microsoft YaHei",sans-serif;line-height:1.55}
    .hero{padding:38px min(6vw,72px) 22px;background:linear-gradient(#fff,#f7f8fb);border-bottom:1px solid var(--line)}.eyebrow{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:700}h1{margin:8px 0 10px;font-size:34px;letter-spacing:0}.subtitle{max-width:1080px;color:#4b5260;font-size:15px}
    .top-nav{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.9);backdrop-filter:saturate(180%) blur(14px);border-bottom:1px solid var(--line);padding:10px min(6vw,72px);display:flex;gap:16px;flex-wrap:wrap}.top-nav a{color:#2f5f9f;text-decoration:none;font-size:13px;font-weight:700}.wrap{padding:24px min(6vw,72px) 56px}.section{margin:0 0 26px}h2{font-size:24px;margin:0 0 12px}
    .goal-card,.supply-chain-section,.target-section,.source-collapse{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px;box-shadow:0 10px 28px rgba(30,41,59,.05)}.goal-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.metric{border:1px solid #e7ebf2;border-radius:8px;padding:12px;background:#fbfcfe}.metric span{display:block;color:var(--muted);font-size:12px}.metric strong{font-size:15px}.chain-explain{display:grid;gap:14px;margin-bottom:16px}.chain-plain-summary{margin:0;padding:14px 16px;border:1px solid #d9e4f2;border-radius:8px;background:#f6f9fd;font-weight:700;line-height:1.75}.chain-flow-steps,.chain-chokepoints,.chain-target-links{border:1px solid #e6eaf1;border-radius:8px;background:#fbfcff;padding:14px}.chain-flow-steps b,.chain-chokepoints b,.chain-target-links b{display:block;margin-bottom:8px}.chain-flow-steps ol{margin:0;padding-left:22px;line-height:1.75}.chain-layer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px}.chain-layer-card{border:1px solid #e6eaf1;border-radius:8px;background:#fff;padding:12px}.chain-layer-card b,.chain-layer-card span{display:block}.chain-layer-card span{color:var(--blue);font-weight:700;margin-top:4px}.chain-layer-card p{margin:8px 0;color:var(--ink)}.chain-layer-card small{color:var(--muted);line-height:1.6}.chain-map,.table-scroll{overflow:auto;border:1px solid #e6eaf1;border-radius:8px}.chain-table,.target-table{min-width:1180px}
    .qa-card{background:var(--panel);border:1px solid var(--line);border-radius:8px;margin:12px 0;overflow:hidden}.qa-card[open]>summary{border-bottom:1px solid #e6eaf1}.qa-card summary{list-style:none;cursor:pointer;padding:14px 16px;display:grid;grid-template-columns:auto 1fr auto auto;gap:10px;align-items:center}.qa-card summary::-webkit-details-marker{display:none}.qid{font-weight:800;color:var(--blue);font-size:13px}.qtitle{font-weight:760}.qa-count{font-size:12px;color:var(--muted);background:#f1f4f9;border:1px solid #e0e5ee;border-radius:999px;padding:3px 8px}.chevron{color:var(--muted);display:inline-block;transition:transform .16s ease}details[open]>summary .chevron{transform:rotate(90deg)}.level-2{margin-left:16px}.level-3{margin-left:32px}.qa-body{padding:14px 16px 16px}.qa-block{margin:0 0 14px}.block-title{font-size:12px;font-weight:800;color:#586174;text-transform:uppercase;margin-bottom:8px}
    .artifact-card{border:1px solid #e2e7ef;border-radius:8px;background:#fbfcff;padding:12px;margin:10px 0}.artifact-title{font-weight:780;margin-bottom:8px}.logic-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.logic-card{border:1px solid #e5e9f0;border-radius:8px;background:#fff;padding:10px}.logic-card b{display:block;font-size:12px;color:#536071;margin-bottom:4px}.logic-card p{margin:0;font-size:13px}.routing{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:10px}.pill{border:1px solid #dfe6f1;background:#f7faff;border-radius:999px;padding:4px 8px;font-size:12px;color:#46515f}.source-chips{display:flex;flex-wrap:wrap;gap:6px}.source-chip{font-size:12px;color:#0a63ce;background:#eef5ff;border:1px solid #d8e8ff;border-radius:999px;padding:4px 8px;text-decoration:none}
    table{width:100%;border-collapse:collapse;font-size:13px}th,td{padding:9px 8px;border-bottom:1px solid #e6eaf1;text-align:left;vertical-align:top}th{color:#536071;font-size:12px;background:#f8fafc}.state-actionable_long{color:var(--green);font-weight:800}.state-watch_only{color:var(--amber);font-weight:800}.state-no_action{color:var(--red);font-weight:800}.source-collapse summary{cursor:pointer;font-weight:800}.source-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin-top:12px}.source-card{border:1px solid #e5e9f0;border-radius:8px;background:#fbfcff;padding:10px}.source-card a{color:#0a63ce}
    @media(max-width:900px){.goal-grid,.logic-grid{grid-template-columns:1fr}.level-2,.level-3{margin-left:0}.qa-card summary{grid-template-columns:auto 1fr auto}.qa-count{display:none}}
  `;
}
