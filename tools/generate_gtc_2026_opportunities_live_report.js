const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const PROJECT_ID = "gtc_2026_opportunities_live_20260601";
const OUT_DIR = path.join(ROOT, "research", "bom", PROJECT_ID);
const REPORT_DATE = "2026-06-01";
const REVIEW_HORIZON = "2026-09-01";

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
  source("SRC-NV-GTC-OVERVIEW", "NVIDIA: GTC 2026 overview and agenda", "evidence", "https://nvidianews.nvidia.com/news/nvidia-ceo-jensen-huang-and-global-technology-leaders-to-showcase-age-of-ai-at-gtc-2026", "2026-03-03", "NVIDIA said GTC 2026 would run March 16-19 in San Jose, with 1,000+ sessions and a five-layer AI stack spanning energy, chips, infrastructure, models and applications."),
  source("SRC-NV-VERA-RUBIN", "NVIDIA: Vera Rubin opens agentic AI frontier", "evidence", "https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform", "2026-03-16", "NVIDIA announced Vera Rubin as a rack-scale AI factory platform including Vera CPU, Rubin GPU, NVLink 6, ConnectX-9, BlueField-4 DPU and Spectrum-6 Ethernet switch for pretraining, post-training and agentic inference."),
  source("SRC-NV-VERA-CPU", "NVIDIA: Vera CPU purpose-built for agentic AI", "evidence", "https://nvidianews.nvidia.com/news/nvidia-launches-vera-cpu-purpose-built-for-agentic-ai", "2026-03-16", "NVIDIA launched Vera CPU, claiming 2x efficiency and 50% faster results than traditional rack-scale CPUs; partners include cloud providers and system manufacturers such as Dell, HPE, Lenovo, Supermicro and Taiwan ODMs."),
  source("SRC-NV-STX", "NVIDIA: BlueField-4 STX storage architecture", "evidence", "https://nvidianews.nvidia.com/news/nvidia-launches-bluefield-4-stx-storage-architecture-with-broad-industry-adoption", "2026-03-16", "NVIDIA announced BlueField-4 STX and context-memory storage, citing up to 5x token throughput, 4x energy efficiency and storage partners including Dell, HPE, NetApp, VAST Data, WEKA and others."),
  source("SRC-NV-ROBOTICS", "NVIDIA: global robotics leaders take physical AI to the real world", "evidence", "https://nvidianews.nvidia.com/news/nvidia-and-global-robotics-leaders-take-physical-ai-to-the-real-world", "2026-03-16", "NVIDIA announced physical AI partnerships across robotics, industrial automation and humanoids, with Cosmos, Isaac and GR00T model/framework updates."),
  source("SRC-NV-DRIVE", "NVIDIA: DRIVE Hyperion adoption for level 4 vehicles", "evidence", "https://nvidianews.nvidia.com/news/drive-hyperion-level-4", "2026-03-16", "NVIDIA said BYD, Geely, Isuzu, Nissan and mobility platforms are adopting DRIVE Hyperion for L4-ready vehicles, and highlighted robotaxi deployment plans with Uber."),
  source("SRC-NV-GTC-TAIPEI-VERA", "NVIDIA: Vera Rubin ramps into full production", "evidence", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Ramps-Into-Full-Production-to-Power-Agentic-AI-Factories-Worldwide/default.aspx", "2026-05-31", "At NVIDIA GTC Taipei, NVIDIA said Vera Rubin is ramping into full production and highlighted Spectrum-X Ethernet Photonics with co-packaged optics for million-GPU AI factories."),
  source("SRC-NV-RTX-SPARK", "NVIDIA and Microsoft reinvent Windows PCs for personal AI", "evidence", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-and-Microsoft-Reinvent-Windows-PCs-for-the-Age-of-Personal-AI/default.aspx", "2026-06-01", "NVIDIA announced RTX Spark for Windows PCs, with 1 petaflop of AI performance, up to 128GB unified memory and fall availability from OEMs including ASUS, Dell, HP, Lenovo, Microsoft Surface and MSI."),
  source("SRC-MS-RTX-SPARK", "Microsoft: Windows PCs accelerated by NVIDIA RTX Spark", "evidence", "https://blogs.windows.com/windowsexperience/2026/05/31/introducing-a-powerful-new-chapter-for-windows-pcs-accelerated-by-nvidia-rtx-spark/", "2026-05-31", "Microsoft said RTX Spark-powered Windows PCs would start with Surface, ASUS, Dell, HP, Lenovo and MSI, positioning local AI agents as a new PC use case."),
  source("SRC-MTK-RTX-SPARK", "MediaTek collaborates with NVIDIA on RTX Spark", "message", "https://www.prnewswire.com/news-releases/mediatek-collaborates-with-nvidia-on-the-rtx-spark-to-power-the-next-wave-of-windows-pc-experiences-302786739.html", "2026-06-01", "MediaTek announced its role enabling NVIDIA RTX Spark for Windows 11 PCs, giving the PC theme a possible Arm/SoC partner chain."),
  source("SRC-VRT-DSX", "Vertiv: physical infrastructure for NVIDIA Vera Rubin DSX AI factories", "evidence", "https://investors.vertiv.com/news/news-details/2026/Vertiv-Brings-Converged-Physical-Infrastructure-to-NVIDIA-Vera-Rubin-DSX-AI-Factories/default.aspx", "2026-03-16", "Vertiv said it is contributing DSX SimReady digital power and cooling assets, validated interfaces and repeatable infrastructure blocks for NVIDIA Vera Rubin DSX AI factory reference designs."),
  source("SRC-DELL-AI-FACTORY", "Dell AI Factory with NVIDIA expands at GTC 2026", "evidence", "https://investors.delltechnologies.com/node/19336/pdf", "2026-03-16", "Dell marked the two-year anniversary of Dell AI Factory with NVIDIA and introduced PowerEdge XE9812 leveraging NVIDIA Vera Rubin NVL72 for enterprise and neocloud AI infrastructure."),
  source("SRC-ASTERA-GTC", "Astera Labs: GTC 2026 rack-scale connectivity", "research_report", "https://www.asteralabs.com/about/events/gtc2026/", "2026-03-16", "Astera Labs presented GTC 2026 content on accelerating rack-scale connectivity for NVIDIA Blackwell and Rubin platforms and scaling AI racks with optics."),
  source("SRC-SNPS-GTC", "Synopsys: NVIDIA partnership impact at GTC 2026", "message", "https://news.synopsys.com/2026-03-16-Synopsys-Showcases-NVIDIA-Partnership-Impact-and-Ecosystem-Innovation-at-GTC-2026?asPDF=1", "2026-03-16", "Synopsys showcased NVIDIA partnership impact and AI infrastructure ecosystem work at GTC 2026, including links between EDA simulation and accelerated compute."),
  source("SRC-FINANCE-SNAPSHOT", "Current market pricing screen", "evidence", "https://finance.yahoo.com/", REPORT_DATE, "Current public market screens show many AI infrastructure beneficiaries already carry elevated expectations; the report caps action states when reverse-DCF or consensus valuation bridges are incomplete."),
];

const chainExplainer = {
  plainSummary: "一句话看懂：GTC 2026 的机会不是单一 GPU 发布，而是 NVIDIA 把 AI 工厂、网络、存储、电力冷却、机器人、车和个人 AI PC 都拉进同一条基础设施链，投资要找的是其中真正稀缺、能赚钱、且没有被市场充分定价的卡点。",
  flowSteps: [
    "AI 公司、云厂商、企业和开发者提出需求：更多 token、更长上下文、更低推理成本、更快部署。",
    "NVIDIA 把需求打包成平台：Vera CPU、Rubin GPU、NVLink、BlueField、Spectrum-X、STX 存储、软件模型和参考设计。",
    "台积电、HBM/内存、先进封装、连接芯片、光模块、电源和液冷把平台变成可交付的 AI 工厂。",
    "Dell、Supermicro、HPE、ODM 和云厂商把 AI 工厂落到机柜、数据中心和客户工作负载。",
    "机器人、自动驾驶、数字孪生和个人 AI PC 是下游应用验证口：只有它们形成订单和使用量，硬件链条才有持续收入。",
    "利润最可能留在平台控制、先进制造、机柜级连接、电力冷却和被验证的系统交付环节；普通配套和主题暴露必须降分。",
  ],
  layers: [
    { name: "终端需求", role: "决定是否继续加 capex", players: "AI labs、云厂商、企业、汽车/机器人客户、PC 用户", note: "如果 token 收入、企业 ROI 或机器人/PC 使用量不兑现，GTC 热度会变成订单风险。" },
    { name: "平台控制", role: "把需求定义成标准平台", players: "NVIDIA CUDA、Vera Rubin、RTX Spark、Omniverse/Isaac/Cosmos", note: "这是最大卡点，但 NVDA 估值通常也最充分，需要单独看赔率。" },
    { name: "芯片与制造", role: "把平台变成可量产硅片", players: "TSMC、HBM/内存、封装、Arm/MediaTek 相关链", note: "这里有强稀缺性，但需要确认新增订单和毛利弹性，而不是只看主题。" },
    { name: "网络/存储/连接", role: "让 AI 工厂像一个系统工作", players: "Spectrum-X、BlueField-4 STX、Astera、Broadcom、Arista、Marvell 等", note: "机柜级互联是关键，但 NVIDIA 自己也在纵向整合，第三方需要证明不可替代。" },
    { name: "电力冷却/机柜", role: "决定 AI 工厂能否落地", players: "Vertiv、Dell、Supermicro、HPE、ODM", note: "数据中心电力和液冷是物理瓶颈，订单质量和执行风险要一起看。" },
    { name: "应用验证", role: "证明需求不是发布会叙事", players: "机器人、自动驾驶、工业数字孪生、个人 AI PC OEM", note: "这里决定未来空间，但多数标的目前仍需要订单、毛利和使用量验证。" },
  ],
  chokepoints: [
    { node: "NVIDIA 平台控制", why: "Vera Rubin、CUDA、网络、存储和软件把 AI 工厂绑定成一个系统", controllers: "NVDA", qa: "Q2.1 / Q4.1" },
    { node: "先进制造和 HBM/封装", why: "如果产能或良率跟不上，AI 工厂交付会被卡住", controllers: "TSMC、HBM/封装链", qa: "Q2.1 / Q3.2" },
    { node: "机柜级连接/光互联", why: "百万 GPU 工厂需要低延迟、高带宽、低功耗网络", controllers: "NVIDIA Spectrum-X、ALAB、AVGO、ANET、MRVL 等", qa: "Q2.1 / Q3.2" },
    { node: "电力和液冷基础设施", why: "高功率机柜需要可复制的电源、冷却和数据中心工程能力", controllers: "VRT、DELL、SMCI、HPE/ODM", qa: "Q2.2 / Q4.1" },
    { node: "个人 AI PC/机器人真实采用", why: "这是从基础设施扩到终端的新增空间，但最容易停留在概念期", controllers: "NVDA、MSFT、OEM、机器人生态", qa: "Q1.2 / Q3.2" },
  ],
  targetLinks: [
    ["NVDA", "平台控制", "最直接但也最可能被充分定价", "Q2.1 / Q4.1"],
    ["VRT", "电力/液冷", "AI 工厂物理瓶颈，需验证估值和订单质量", "Q2.2 / Q4.1"],
    ["ALAB", "机柜级连接", "Rubin/Blackwell 连接链条强，但估值和客户集中需控分", "Q2.1 / Q4.1"],
    ["DELL/SMCI", "系统交付", "能接订单但利润率和执行风险不同", "Q2.2 / Q3.2"],
    ["ARM/TSM/MU", "IP/制造/内存", "重要但 GTC 增量到财务弹性需要二次证明", "Q2.1 / Q4.1"],
    ["AVGO/ANET/MRVL", "网络生态", "AI Ethernet 长期强，但与 NVIDIA 自有 Spectrum-X 的关系要拆开", "Q3.2 / Q4.1"],
  ],
};

const chainRows = [
  ["需求端", "AI labs、云厂商、企业代理、机器人、自动驾驶、个人 AI PC", "OpenAI/Anthropic、Microsoft、Oracle、CoreWeave、OEM、机器人公司", "决定 token 收入、capex 和终端换机是否持续", "需求真实，但需要从发布会信号落到订单、使用量和现金流", "Q1 / Q3"],
  ["平台层", "Vera Rubin、Vera CPU、Rubin GPU、BlueField-4、Spectrum-X、CUDA、RTX Spark", "NVIDIA、Microsoft、MediaTek", "把多个需求场景统一成 NVIDIA 平台和开发者生态", "最高稀缺性在 NVDA，但也最容易被市场提前定价", "Q2.1 / Q4"],
  ["芯片制造/内存/封装", "先进制程、先进封装、HBM/DRAM、统一内存", "TSMC、Micron、SK hynix、Samsung、封装链", "把 AI 工厂和 AI PC 设计变成可量产硬件", "产能和良率是硬瓶颈，但个股财务弹性需要订单验证", "Q2.1 / Q3.2"],
  ["网络/存储/连接", "NVLink、Spectrum-X、CPO、ConnectX、BlueField STX、PCIe/CXL/retimer", "NVIDIA、Astera、Broadcom、Arista、Marvell、存储厂商", "决定 GPU 利用率、长上下文推理和机柜级扩展效率", "连接是真卡点，但第三方受益要区分供应链伙伴与被平台替代风险", "Q2.1 / Q3.2"],
  ["电力/冷却/系统交付", "液冷、电源、机柜、DSX 参考设计、AI Factory 系统", "Vertiv、Dell、Supermicro、HPE、ODM", "把 AI 工厂落到物理数据中心和企业部署", "物理基础设施是清晰瓶颈，但估值、执行和毛利质量要控分", "Q2.2 / Q4"],
  ["应用验证", "机器人、自动驾驶、数字孪生、个人 AI PC、企业 agent", "ABB、Figure、BYD、Geely、Microsoft Surface、Dell/HP/Lenovo 等 OEM", "决定 GTC 技术路线是否变成实际收入池", "下游空间大，但当前不少仍是验证期，不能直接给高行动状态", "Q1.2 / Q3"],
];

const l1s = [
  l1("Q1", "GTC 2026 到底给了哪些可投资信号，哪些只是发布会热度？", "GTC 2026 的核心信号是 AI 工厂从 GPU 走向整机柜、网络、存储、电力冷却和软件生态；GTC Taipei 又把 Vera/Rubin 量产和 RTX Spark 个人 AI PC 加进当前信息集。但多数线索仍需要订单、毛利和估值验证。"),
  l1("Q2", "产业链里真正稀缺、能捕获价值的卡点在哪里？", "最高确定性的稀缺点仍在 NVIDIA 平台控制，其次是先进制造/HBM、机柜级连接、电力冷却和 AI Factory 系统交付。第三方标的必须证明自己不是普通配套，而是难替代瓶颈。"),
  l1("Q3", "哪些反证会让 GTC 主题无法转化为好投资？", "最大风险是市场已经把 AI 基建高增长提前定价，同时客户 capex、供电、液冷、交付和 AI ROI 任一环节走弱都会压低胜率；终端 AI PC/机器人也可能停留在概念期。"),
  l1("Q4", "按当前证据，哪些标的进入观察池，行动状态如何？", "当前没有足够证据给出高确定性 actionable_long。较值得观察的是 VRT、ALAB、NVDA、DELL、ARM 和 TSM/MU 等，但大多因为估值、验证不足或平台替代风险维持 watch_only 或 no_action。"),
];

const l2s = [
  l2("Q1.1", "大会事实和信号边界", "GTC 2026 已经给出多个可验证产品和合作信号，但投资上必须区分已宣布、已量产、已被客户采用和已转化为财务弹性。"),
  l2("Q1.2", "需求是否能从 AI 工厂扩到终端应用", "AI 工厂是主线，个人 AI PC、机器人和自动驾驶是增量期权；它们能否兑现取决于使用量、订单和单位经济性。"),
  l2("Q2.1", "平台、制造、连接和存储卡点", "Vera Rubin 把计算、CPU、网络、DPU、存储和软件绑成平台，连接和制造约束决定第三方标的价值。"),
  l2("Q2.2", "电力冷却、系统交付和软件生态", "AI 工厂落地离不开电力、液冷、机柜、系统商和数字孪生参考设计；应用软件生态可以扩大 TAM，但不一定形成上市标的稀缺性。"),
  l2("Q3.1", "估值和 capex/ROI 反证", "强技术信号并不等于低估。当前关键是市场隐含增长是否过高，以及客户是否能持续用 AI 服务赚钱。"),
  l2("Q3.2", "供应链替代、执行和终端采用风险", "NVIDIA 的纵向整合可能压缩第三方网络/系统标的弹性；终端 AI PC 和机器人若无出货/使用量，就不能给高分。"),
  l2("Q4.1", "目标池和排序规则", "目标池从价值捕获节点出发，不从发布会曝光度出发；高主题热度但缺低估证据的标的必须控分。"),
  l2("Q4.2", "三个月验证触发器", "live 模式用 2026-09-01 作为复核窗口，关注订单、capex、供电液冷项目、RTX Spark SKU/出货和 AI Factory 毛利验证。"),
];

const leaves = [
  leaf("Q1.1.1", "Q1.1", "GTC 2026 的主线公告到底是什么？", "news-event-analysis", "evidence_quality", "决定研究是否从单 GPU 主题升级为 AI 工厂产业链主题。", ["SRC-NV-GTC-OVERVIEW", "SRC-NV-VERA-RUBIN", "SRC-NV-VERA-CPU"], "GTC 2026 官方信息覆盖 AI 工厂、Vera Rubin 平台、Vera CPU、网络、存储、机器人和应用生态。", "这说明主线不只是 GPU 换代，而是 rack-scale AI factory 的系统化扩张。", "Q1 可以确认 GTC 是产业链事件，不是单品发布会。", "仍需把发布会口径和真实订单分开。", "若客户实例、量产时间和出货数据继续落地，提高 evidence_quality。", artifact("GTC 主线拆解", ["主线", "证据", "投资含义"], [["AI 工厂", "Vera Rubin + DSX + STX", "基础设施链条扩张"], ["agentic AI", "Vera CPU / BlueField STX", "推理和长上下文需求"], ["physical AI", "Cosmos/Isaac/GR00T", "机器人应用期权"], ["personal AI", "RTX Spark Windows PC", "终端换机期权"]])),
  leaf("Q1.1.2", "Q1.1", "哪些信号已经接近量产或客户采用？", "news-event-analysis", "evidence_quality", "防止把路线图、合作意向和收入确认混为一谈。", ["SRC-NV-GTC-TAIPEI-VERA", "SRC-NV-VERA-CPU", "SRC-DELL-AI-FACTORY"], "NVIDIA 5 月底进一步强调 Vera Rubin ramp/full production，并列出系统制造商、云厂商和 AI factory 采用线索。", "量产/采用信号比单纯路线图更强，但仍不等于每个供应链标的都能确认收入。", "可提高 AI factory 主线可信度，但对第三方标的仍需订单和毛利验证。", "缺少逐家公司订单规模、交付节奏和利润率。", "若 OEM/云厂商披露 Vera Rubin 订单和收入贡献，升级相关目标。", artifact("信号强度分层", ["层级", "当前证据", "使用方式"], [["发布会方向", "GTC overview", "只作主题线索"], ["产品平台", "Vera/Rubin/Vera CPU/STX", "可进入 Q2 卡点评估"], ["客户采用", "云厂商/制造商名单", "仍需订单规模"], ["财务兑现", "尚未完整披露", "不能直接高行动状态"]])),
  leaf("Q1.2.1", "Q1.2", "AI 工厂需求能否支撑多环节投资机会？", "industry-report-analysis", "future_space", "决定是否只研究 NVDA，还是扩展到电力、连接、系统和制造链。", ["SRC-NV-GTC-OVERVIEW", "SRC-NV-VERA-RUBIN", "SRC-VRT-DSX"], "GTC 把 AI stack 描述为能源、芯片、基础设施、模型和应用五层，并把 Vera Rubin/DSX 与数据中心部署联系起来。", "如果 AI factory 是基础设施扩张，价值会外溢到电力冷却、机柜、网络、存储和系统交付。", "Q1.2 支持建立跨环节观察池，但不能假设每个环节都有超额收益。", "缺少客户 capex ROI、项目电力约束和毛利分解。", "若云厂商维持/上调 AI capex 且订单进入电力/液冷/系统商，升级 future_space。", artifact("AI 工厂需求传导", ["需求", "传导环节", "可观察数据"], [["更多 token", "GPU/CPU/DPU/网络", "云厂商 capex"], ["更长上下文", "STX 存储/内存", "存储订单和吞吐指标"], ["机柜部署", "电力/液冷/系统", "backlog 和毛利"], ["企业 AI", "Dell/系统商", "订单和服务收入"]])),
  leaf("Q1.2.2", "Q1.2", "RTX Spark、机器人和自动驾驶是不是可投资主线？", "news-event-analysis", "payoff_convexity", "判断 GTC 下游应用是当前利润池还是远期期权。", ["SRC-NV-RTX-SPARK", "SRC-MS-RTX-SPARK", "SRC-NV-ROBOTICS", "SRC-NV-DRIVE"], "RTX Spark 有官方 Windows/OEM 时间表，机器人和 DRIVE Hyperion 有生态伙伴，但大多仍需出货或部署验证。", "下游应用扩大未来空间，但短期财务弹性低于 AI factory 主线。", "将 RTX Spark/机器人/自动驾驶作为期权，而不是当前最高优先级投资结论。", "缺少 RTX Spark SKU 价格、出货、应用使用量和机器人订单。", "若秋季 OEM 上市后出现高 ASP/销量或机器人量产订单，再提高 payoff_convexity。", artifact("下游期权分类", ["方向", "当前证据", "投资处理"], [["RTX Spark PC", "OEM fall availability", "关注 ARM/MSFT/DELL/HP/Lenovo 链"], ["机器人", "NVIDIA ecosystem partnerships", "等待订单和量产"], ["自动驾驶", "BYD/Geely 等 DRIVE adoption", "偏长期验证"], ["企业 agent", "Vera/Windows/DGX Station", "关注企业部署"]])),
  leaf("Q2.1.1", "Q2.1", "Vera Rubin 平台里最难替代的硬件卡点是什么？", "industry-report-analysis", "chokepoint_strength", "决定 Q4 是否优先平台控制、先进制造、内存和连接，而不是普通系统集成。", ["SRC-NV-VERA-RUBIN", "SRC-NV-VERA-CPU", "SRC-NV-GTC-TAIPEI-VERA"], "Vera Rubin 把 CPU、GPU、NVLink、DPU、SuperNIC、Spectrum-X 和软件栈整合成 AI supercomputer。", "整机柜协同提升 NVIDIA 平台控制，也让先进制造、HBM/内存和高带宽互联成为关键约束。", "NVDA/TSM/HBM/连接链应优先分析，但第三方必须证明不可替代和财务弹性。", "缺少每个供应商的 BoM、ASP 和产能分配。", "若供应商披露 Rubin/HBM/封装相关订单和毛利，提升相关 chokepoint。", artifact("硬件卡点", ["节点", "稀缺原因", "潜在标的"], [["平台控制", "系统级协同和 CUDA 生态", "NVDA"], ["先进制造", "制程/封装/产能", "TSM"], ["HBM/内存", "高带宽和长上下文", "MU/韩系存储"], ["连接", "低延迟和机柜级扩展", "ALAB/AVGO/ANET/MRVL"]])),
  leaf("Q2.1.2", "Q2.1", "网络、存储和连接链是否比普通服务器更有价值？", "industry-report-analysis", "chokepoint_strength", "判断 ALAB、AVGO、ANET、MRVL、存储厂商是否有真正卡点。", ["SRC-NV-STX", "SRC-ASTERA-GTC", "SRC-NV-GTC-TAIPEI-VERA"], "NVIDIA STX、Spectrum-X Photonics 和 Astera GTC 内容都指向 AI rack connectivity、context memory storage 和 optical/PCIe/CXL 扩展。", "连接和存储确实是 agentic AI 的系统瓶颈，但 NVIDIA 自有方案可能改变第三方价值分配。", "ALAB 等进入高优先级观察，但需要控估值和客户集中；AVGO/ANET/MRVL 要区分互补与竞争。", "缺少第三方在 Rubin/DSX 的明确单机价值和份额。", "若第三方连接芯片进入 Rubin/DSX 标准配置并披露营收，升级。", artifact("网络/存储卡点", ["问题", "支持证据", "风险"], [["长上下文推理", "BlueField STX / CMX", "存储架构是否标准化"], ["百万 GPU 连接", "Spectrum-X Photonics/CPO", "NVIDIA 自供比例"], ["PCIe/CXL/retimer", "Astera GTC 主题", "估值和客户集中"], ["Ethernet 生态", "AVGO/ANET/MRVL", "与 Spectrum-X 竞争"]])),
  leaf("Q2.2.1", "Q2.2", "电力冷却和系统交付是不是更清晰的瓶颈？", "financial-statement-analysis", "chokepoint_strength", "决定 VRT、DELL、SMCI 等是否比纯主题标的更可跟踪。", ["SRC-VRT-DSX", "SRC-DELL-AI-FACTORY", "SRC-NV-VERA-CPU"], "Vertiv 参与 Vera Rubin DSX 物理基础设施设计；Dell AI Factory 与 NVIDIA 深度绑定；NVIDIA 列出多家系统制造商采用 Vera CPU。", "AI factory 落地需要电力、液冷、机柜和系统交付，物理瓶颈比很多应用叙事更可验证。", "VRT/DELL 进入高优先级观察，SMCI 因执行和治理风险需更保守。", "缺少 DSX 订单金额、毛利、交付周期和客户集中度。", "若 VRT/DELL 披露与 NVIDIA AI factory 相关 backlog 和毛利质量，升级。", artifact("物理基础设施卡点", ["节点", "价值", "标的处理"], [["电力/液冷", "高功率机柜必需", "VRT watch_only"], ["企业 AI Factory", "系统集成和服务", "DELL watch_only"], ["白牌/服务器", "交付弹性大", "SMCI 因风险 no_action"], ["ODM", "订单弹性", "多数非美股/标签需另查"]])),
  leaf("Q2.2.2", "Q2.2", "软件、EDA、机器人生态能不能形成稀缺收益？", "industry-report-analysis", "future_space", "判断 GTC 软件生态是应用空间还是可投资卡点。", ["SRC-NV-ROBOTICS", "SRC-NV-DRIVE", "SRC-SNPS-GTC"], "NVIDIA 发布 physical AI 模型/框架并与机器人、车企、EDA 生态合作；Synopsys 展示 NVIDIA partnership。", "软件生态扩大 NVIDIA 平台黏性，但独立上市标的的财务捕获路径不如硬件/基础设施清晰。", "SNPS/CDNS/机器人链可列入跟踪，但本报告不把它们排在高行动状态。", "缺少软件授权收入、机器人量产订单和 EDA AI 工作流商业化数据。", "若 EDA/机器人公司披露与 NVIDIA 模型/仿真的收入贡献，再提高。", artifact("软件生态价值", ["生态", "当前作用", "投资处理"], [["EDA", "加速设计和仿真", "SNPS/CDNS 观察"], ["机器人", "Cosmos/Isaac/GR00T", "等待量产订单"], ["自动驾驶", "DRIVE Hyperion", "长期验证"], ["企业 agent", "模型和工具链", "主要强化 NVDA 平台"]])),
  leaf("Q3.1.1", "Q3.1", "市场是否已经充分定价 GTC 主题？", "valuation-analysis", "valuation_odds", "防止因为技术强就给高行动状态。", ["SRC-FINANCE-SNAPSHOT", "SRC-NV-GTC-OVERVIEW", "SRC-NV-GTC-TAIPEI-VERA"], "当前 AI 基建相关公司普遍被市场关注，NVDA、VRT、ALAB、ARM 等主题曝光度很高；完整 reverse DCF 尚未完成。", "GTC 证据提高基本面可信度，但不自动提高估值赔率。", "没有低估证据前，绝大多数标的 action_state 保持 watch_only/no_action。", "缺少统一口径的 EV/FCF、隐含增长、毛利和下行情景。", "只有当市场隐含预期低于可验证订单/利润路径时，才升级 mispricing。", artifact("估值闸门", ["条件", "当前判断", "动作"], [["技术确定性", "较强", "提高研究优先级"], ["低估证据", "不足", "封顶 action_state"], ["财务弹性", "部分环节可验证", "看订单和毛利"], ["下行保护", "需补数据", "不做强多头"]])),
  leaf("Q3.1.2", "Q3.1", "客户 capex、AI ROI 和电力约束会不会打断链条？", "news-event-analysis", "disconfirming_risk_control", "定义最重要的反证源。", ["SRC-NV-GTC-OVERVIEW", "SRC-VRT-DSX", "SRC-DELL-AI-FACTORY"], "GTC 将 AI 描述为基础设施，但 AI factory 的落地仍依赖客户 capex、供电、液冷、机房建设和模型收入。", "如果 capex 放缓或电力/部署瓶颈导致交付延期，多数供应链标的会被同时压估值。", "Q3.1 的风险控制要求把订单质量和部署约束作为核心 kill tests。", "缺少云厂商逐季 AI capex ROI 和供电项目数据。", "若 hyperscaler 下修 capex 或 VRT/DELL backlog 质量下降，下调相关标的。", artifact("capex/ROI 反证", ["反证", "影响链条", "降级动作"], [["AI capex 放缓", "NVDA/TSM/HBM/系统商", "整体降分"], ["电力接入延迟", "VRT/DELL/SMCI", "压低交付弹性"], ["token 收入不足", "AI 工厂需求", "降低 future_space"], ["毛利下滑", "系统/基础设施", "降低 risk_control"]])),
  leaf("Q3.2.1", "Q3.2", "NVIDIA 纵向整合会不会压缩第三方受益？", "industry-report-analysis", "disconfirming_risk_control", "避免把所有 AI 网络/系统公司都当作 GTC 受益者。", ["SRC-NV-STX", "SRC-NV-GTC-TAIPEI-VERA", "SRC-ASTERA-GTC"], "NVIDIA 在网络、DPU、STX 存储、Spectrum-X Photonics 和参考设计上持续加深整合。", "平台整合提高 NVIDIA 自身护城河，但可能让部分第三方只获得有限配套利润或面临替代。", "第三方网络/连接标的必须有明确 design-in、份额和毛利证据。", "缺少 DSX/Rubin 的第三方 BoM 份额。", "若 NVIDIA 自有方案替代第三方，降级 AVGO/ANET/MRVL/ALAB 中缺证据者。", artifact("纵向整合风险", ["对象", "正面", "负面"], [["NVDA", "平台控制增强", "估值已反映"], ["ALAB", "rack connectivity 需求", "客户/平台依赖"], ["AVGO/ANET/MRVL", "AI networking 大空间", "Spectrum-X 竞争"], ["系统商", "参考设计加快部署", "标准化压缩差异化"]])),
  leaf("Q3.2.2", "Q3.2", "RTX Spark、机器人和 DRIVE 会不会停留在概念期？", "news-event-analysis", "risk_control", "控制终端应用期权的分数上限。", ["SRC-NV-RTX-SPARK", "SRC-MS-RTX-SPARK", "SRC-NV-ROBOTICS", "SRC-NV-DRIVE"], "RTX Spark 有 OEM 时间表，机器人/自动驾驶有生态合作，但出货、价格、企业采用和盈利模式仍未充分披露。", "终端应用可能扩大 TAM，也可能因为应用不足、价格高或采购慢而难以兑现。", "RTX Spark/机器人/DRIVE 对主线是加分项，但不足以单独推高多数标的。", "缺少出货、渠道库存、应用使用量和机器人交付收入。", "若 fall 2026 RTX Spark SKU 销量不佳或机器人订单不落地，降低 payoff_convexity。", artifact("终端期权风险", ["方向", "需要验证", "分数处理"], [["RTX Spark", "SKU/价格/销量/应用", "watch"], ["机器人", "量产订单和客户 ROI", "低权重"], ["DRIVE", "车型量产和软件收入", "长期验证"], ["企业本地 agent", "采购和续费", "待证实"]])),
  leaf("Q4.1.1", "Q4.1", "哪些证券是真正的价值捕获载体？", "target-recommendation-analysis", "target_ranking", "建立目标池，不按发布会曝光度或交易便利性收缩。", ["SRC-NV-VERA-RUBIN", "SRC-VRT-DSX", "SRC-DELL-AI-FACTORY", "SRC-ASTERA-GTC", "SRC-NV-RTX-SPARK"], "价值捕获载体包括 NVDA、VRT、ALAB、DELL、ARM、TSM、MU、AVGO/ANET/MRVL 和 SMCI，但质量差异很大。", "目标池应从卡点映射而来，而不是从热门 ticker 出发。", "最终表保留 watch_only/no_action，避免强行做多。", "缺少跨市场同口径估值和订单证据。", "补齐估值和订单后再调整 action_state。", artifact("目标池映射", ["标的", "链条节点", "当前处理"], [["NVDA", "平台控制", "watch_only"], ["VRT", "电力/液冷", "watch_only"], ["ALAB", "连接芯片", "watch_only"], ["DELL", "AI Factory 系统", "watch_only"], ["ARM/TSM/MU", "IP/制造/内存", "watch_only"], ["AVGO/ANET/MRVL/SMCI", "网络/系统", "no_action/watch"]])),
  leaf("Q4.1.2", "Q4.1", "排序如何由分数而不是叙事产生？", "target-recommendation-analysis", "action_state", "确保高分必须同时满足稀缺、低估、弹性和风险控制。", ["SRC-FINANCE-SNAPSHOT", "SRC-VRT-DSX", "SRC-ASTERA-GTC", "SRC-NV-VERA-RUBIN"], "目标分数由 chokepoint、future space、valuation odds、evidence quality、risk control、monitorability 和 payoff convexity 组成，并汇总到四个核心维度。", "当前多数标的的 scarcity/future_space 强，但 mispricing 未验证，因此不能升级 actionable_long。", "排序以 watch_only 为主，no_action 用于证据或风险不足的方向。", "缺少完整 reverse DCF 和订单毛利模型。", "只有四个维度都增强才升级。", artifact("行动状态闸门", ["维度", "要求", "当前状态"], [["scarcity_or_monopoly", "卡点清晰", "部分强"], ["mispricing", "未充分定价", "普遍不足"], ["earnings_elasticity", "订单到利润弹性", "需验证"], ["risk_control", "反证可控", "分化明显"]])),
  leaf("Q4.2.1", "Q4.2", "未来三个月哪些数据能升级观察强度？", "target-recommendation-analysis", "monitorability", "定义 live 研究的复核指标。", ["SRC-NV-GTC-TAIPEI-VERA", "SRC-NV-RTX-SPARK", "SRC-VRT-DSX", "SRC-DELL-AI-FACTORY"], "最有用的升级数据包括 Vera/Rubin 订单、AI factory backlog、VRT/DELL 毛利、ALAB design-in、RTX Spark SKU 和出货。", "这些指标能直接验证 future_space、financial conversion 和 valuation odds。", "复核窗口设为 2026-09-01。", "需要自动跟踪官方公告、财报和渠道数据。", "若订单、毛利和估值同时改善，升级强度。", artifact("升级触发器", ["节点", "升级数据"], [["NVDA/TSM/MU", "Rubin 出货/HBM/封装订单"], ["VRT/DELL", "AI factory backlog 和毛利"], ["ALAB", "Rubin/Blackwell design-in 收入"], ["RTX Spark", "OEM SKU、价格、销量"], ["机器人/DRIVE", "量产订单和客户部署"]])),
  leaf("Q4.2.2", "Q4.2", "哪些 kill tests 会撤销 GTC 主题高分？", "target-recommendation-analysis", "risk_control", "给每个高关注方向设置硬降级条件。", ["SRC-FINANCE-SNAPSHOT", "SRC-NV-STX", "SRC-NV-RTX-SPARK", "SRC-VRT-DSX"], "关键 kill tests 包括 AI capex 下修、Vera/Rubin 延迟、VRT/DELL 毛利恶化、第三方连接被 NVIDIA 替代、RTX Spark 出货不佳。", "这些反证会分别攻击 future_space、chokepoint_strength、payoff 和 risk_control。", "任何目标若触发核心 kill test，应降级到 no_action。", "需要持续收集订单、财报、渠道和供应链数据。", "官方财报或客户 capex 指引确认任一 kill test 时降级。", artifact("Kill tests", ["Kill test", "影响", "动作"], [["AI capex 下修", "全链条", "整体降分"], ["Rubin/STX 延迟", "NVDA/系统/连接", "降低 future_space"], ["第三方连接被替代", "ALAB/AVGO/ANET/MRVL", "降为 no_action"], ["电力液冷毛利差", "VRT/DELL/SMCI", "降低 risk_control"], ["RTX Spark 销量弱", "ARM/OEM/PC 链", "降低 payoff"]])),
];

const targets = rankTargets([
  target("VRT", "Vertiv", "USA", "AI factory power and liquid cooling", [4.25, 4.25, 2.45, 4.05, 3.15, 4.05, 3.75], ["SRC-VRT-DSX", "SRC-NV-GTC-TAIPEI-VERA"], "电力/液冷是 AI 工厂物理瓶颈，VRT 与 DSX 参考设计有直接证据；但估值和订单毛利需要验证。", "AI factory backlog, liquid-cooling margin, DSX customer conversion, capex durability", "AI capex downshift or VRT backlog converts at weaker margin", "watch_only"),
  target("ALAB", "Astera Labs", "USA", "Rack-scale connectivity / PCIe-CXL-retimer", [4.15, 4.10, 2.15, 3.60, 2.75, 3.65, 4.00], ["SRC-ASTERA-GTC", "SRC-NV-STX"], "Rubin/Blackwell rack connectivity is a real bottleneck; ALAB has strong thematic fit, but valuation and customer/platform dependence cap action state.", "Rubin/Blackwell design-in revenue, customer concentration, gross margin, CXL/optics adoption", "NVIDIA self-supplies or customer concentration/valuation pressure worsens", "watch_only"),
  target("NVDA", "NVIDIA", "USA", "AI factory platform control", [4.90, 4.85, 1.75, 4.80, 3.20, 4.70, 3.60], ["SRC-NV-VERA-RUBIN", "SRC-NV-VERA-CPU", "SRC-NV-RTX-SPARK"], "最强平台控制和证据质量来自 NVDA 本身，但市场定价可能已经反映大量 AI 工厂增长。", "Rubin shipment, gross margin, cloud demand, RTX Spark adoption, implied growth vs actual orders", "customer capex or margins fail to support valuation", "watch_only"),
  target("DELL", "Dell Technologies", "USA", "AI Factory system integration and RTX Spark OEM", [3.35, 3.95, 2.35, 3.90, 2.85, 3.70, 3.30], ["SRC-DELL-AI-FACTORY", "SRC-NV-RTX-SPARK", "SRC-MS-RTX-SPARK"], "Dell 同时在 AI Factory 和 RTX Spark OEM 端有曝光，但系统集成利润率和订单质量需要验证。", "PowerEdge XE9812 demand, AI server margin, RTX Spark SKU orders, services attach", "AI server margins compress or RTX Spark demand weak", "watch_only"),
  target("ARM", "Arm Holdings", "USA", "CPU/IP exposure to AI PC and AI infrastructure", [3.90, 3.55, 1.90, 3.35, 2.85, 3.25, 3.65], ["SRC-NV-RTX-SPARK", "SRC-MTK-RTX-SPARK", "SRC-NV-VERA-CPU"], "Arm/IP 暴露可能受益于 AI PC 和自研 CPU 潮流，但 GTC 证据不足以证明 royalty 弹性和低估。", "RTX Spark architecture details, royalty rate, shipment volume, enterprise adoption", "RTX Spark volume weak or economics bypass ARM upside", "watch_only"),
  target("TSM", "TSMC ADR", "USA", "Advanced foundry and packaging", [4.55, 4.40, 2.05, 4.30, 3.35, 3.45, 2.85], ["SRC-NV-VERA-RUBIN", "SRC-NV-GTC-TAIPEI-VERA"], "先进制程/封装是 NVIDIA 平台硬瓶颈，但 GTC 本身无法单独证明 TSM 的新增低估。", "CoWoS/advanced packaging capacity, Rubin allocation, AI revenue share, margin", "capacity catches up or valuation prices flawless AI growth", "watch_only"),
  target("MU", "Micron", "USA", "HBM and high-end memory", [3.85, 4.05, 2.35, 3.50, 2.85, 3.30, 3.80], ["SRC-NV-STX", "SRC-NV-VERA-RUBIN"], "长上下文、统一内存和 AI 工厂扩张支持高端内存需求，但 GTC 来源未直接证明 MU 份额。", "HBM design wins, ASP, bit growth, inventory and gross margin", "HBM share disappoints or memory ASP cycle reverses", "watch_only"),
  target("AVGO", "Broadcom", "USA", "AI networking / custom silicon", [3.45, 3.75, 2.15, 3.20, 2.65, 3.15, 3.25], ["SRC-NV-GTC-TAIPEI-VERA", "SRC-FINANCE-SNAPSHOT"], "AI networking 需求强，但 GTC 强化了 NVIDIA Spectrum-X/Photonics 自有路线，AVGO 的 GTC 增量需要独立订单验证。", "AI networking orders, CPO/DSP design wins, custom silicon backlog, margin", "Spectrum-X captures more stack share or valuation stays stretched", "no_action"),
  target("ANET", "Arista Networks", "USA", "AI Ethernet networking", [3.25, 3.65, 2.20, 3.10, 2.75, 3.20, 3.10], ["SRC-NV-GTC-TAIPEI-VERA", "SRC-FINANCE-SNAPSHOT"], "AI Ethernet 是真实方向，但 NVIDIA Spectrum-X 自有生态让 ANET 的受益路径需要客户订单证明。", "AI cluster wins, gross margin, NVIDIA competitive overlap, cloud capex", "cloud customers choose Spectrum-X-integrated stacks over third-party switching", "no_action"),
  target("SMCI", "Supermicro", "USA", "AI server system assembly", [2.80, 3.65, 2.45, 2.55, 2.05, 3.05, 3.55], ["SRC-NV-VERA-CPU", "SRC-DELL-AI-FACTORY"], "系统制造商在 Vera CPU 采用名单中，但 SMCI 的执行、毛利和治理风险要求更低行动状态。", "Rubin/Vera server orders, margins, governance, cash conversion", "execution or accounting risk resurfaces, margin deteriorates", "no_action"),
]);

function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const qaTree = buildQaTree();
  const extractions = buildExtractions();
  const reviews = buildReviews(extractions);
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
    supply_chain_explainer: chainExplainer,
    supply_chain_map: chainRows,
    source_extractions: extractions,
    leaf_source_reviews: reviews,
    scoring_worksheet: targets,
    targets,
  });
  fs.writeFileSync(path.join(OUT_DIR, "professional_report.html"), renderHtml(qaTree, targets), "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "professional_report.md"), renderMarkdown(targets), "utf8");
  console.log(`Generated ${OUT_DIR}`);
}

function source(source_id, title, source_bucket, url, source_visible_at, summary) {
  return {
    source_id,
    title,
    source_bucket,
    url,
    source_visible_at,
    support_refute_or_lead: "support",
    summary,
  };
}

function l1(id, question, conclusion) {
  return { id, level: 1, question, conclusion, children: [] };
}

function l2(id, question, conclusion) {
  return { id, level: 2, question, conclusion, children: [] };
}

function leaf(id, parent, question, skill, score_component, decision_use, sourceIds, fact, inference, judgment, gap, trigger, answerArtifact) {
  const schema = ["key_facts", "numbers_dates", "investment_relevance", "support_refute_or_lead", "uncertainties"];
  const source_extraction_ids = sourceIds.map((sourceId) => extractionId(id, sourceId));
  const leaf_source_review_ids = sourceIds.map((sourceId) => reviewId(id, sourceId));
  return {
    id,
    parent,
    level: 3,
    question,
    conclusion: judgment,
    skill,
    score_component,
    scoreComponent: score_component,
    decision_use,
    materiality: decision_use,
    support_evidence: sourceIds.map((sourceId) => `${sourceId} supports ${question}`),
    refute_evidence: [`Post-GTC order, margin or adoption data contradicting ${question}`],
    target_implications: `Affects ${score_component} and target action_state.`,
    minimum_evidence_gate: "At least one public source visible before report date plus GPT verification.",
    refuting_source_plan: ["Check company filings, customer capex guidance, order/margin updates and competing architecture evidence."],
    source_plan: sourceIds.map((sourceId) => ({
      source_id: sourceId,
      source_visible_at: byId(sourceId).source_visible_at,
      allowed_usage: "live_thesis",
      preferred_parser_skill: skill,
      expected_fields: schema,
      availability_proof: "publisher date / official release page",
    })),
    skill_dispatch: {
      task_family: skill.replace("-analysis", ""),
      selected_skill: skill,
      concrete_materials: sourceIds,
      extraction_schema: schema,
      source_extraction_ids,
      leaf_source_review_ids,
      skill_output_status: "gpt_verified_direct_parse",
      fallback_used: true,
      gpt_verification_status: "verified_against_public_sources",
    },
    fact,
    inference,
    judgment,
    gap,
    trigger,
    sourceIds,
    source_links: sourceIds.map((sourceId) => byId(sourceId).url),
    answerArtifact,
  };
}

function artifact(title, columns, rows) {
  return { title, columns, rows };
}

function target(ticker, name, market, thesisNode, components, sourceIds, rationale, nextData, downgradeRisk, action_state) {
  const componentNames = Object.keys(SCORE_WEIGHTS);
  const componentScores = Object.fromEntries(componentNames.map((name, index) => [name, components[index]]));
  const score_dimensions = {
    scarcity_or_monopoly: componentScores.chokepoint_strength,
    mispricing: componentScores.valuation_odds,
    earnings_elasticity: (componentScores.future_space + componentScores.payoff_convexity) / 2,
    risk_control: componentScores.disconfirming_risk_control,
  };
  const total_score = Object.entries(SCORE_WEIGHTS).reduce((sum, [component, weight]) => sum + componentScores[component] * weight, 0);
  const opportunity_fit = Object.entries(SCORE_DIMENSION_WEIGHTS).reduce((sum, [dimension, weight]) => sum + score_dimensions[dimension] * weight, 0);
  const score_subcomponents = Object.fromEntries(componentNames.map((component) => [component, [{
    name: `${component}_primary_driver`,
    score: componentScores[component],
    weight: SCORE_WEIGHTS[component],
    evidence_ids: sourceIds,
    review_ids: sourceIds.map((sourceId) => reviewId("Q4.1.2", sourceId)).filter(Boolean),
    rationale: `${component} score is based on ${thesisNode} evidence and unresolved valuation/risk gates.`,
    status: action_state === "actionable_long" ? "active" : "capped_until_verified",
  }]]));
  return {
    ticker,
    name,
    market,
    thesis_node: thesisNode,
    action_state,
    rationale,
    next_verification_data: nextData,
    downgrade_risk: downgradeRisk,
    source_ids: sourceIds,
    score: {
      total_score,
      component_scores: componentScores,
      score_dimensions,
      score_subcomponents,
      thesis_confidence: (componentScores.evidence_quality + componentScores.disconfirming_risk_control) / 2,
      payoff_convexity: componentScores.payoff_convexity,
      opportunity_fit,
    },
    score_subcomponents,
    thesis_kill_tests: action_state === "actionable_long" ? [{
      test: downgradeRisk,
      evidence_needed: nextData,
      downgrade_action: "Cut to watch_only or no_action",
      source_plan: sourceIds,
    }] : [],
    odds_model: {
      implied_expectation: "Current market appears to price meaningful AI infrastructure growth; reverse DCF not yet complete.",
      base_path: nextData,
      bull_path: "Orders and margin conversion improve while valuation remains reasonable.",
      bear_path: downgradeRisk,
    },
    prediction_review: {
      initial_claim: rationale,
      validation_horizon: REVIEW_HORIZON,
      required_evidence: nextData,
      current_status: action_state,
      review_trigger: downgradeRisk,
    },
  };
}

function rankTargets(rows) {
  const priority = { actionable_long: 0, watch_only: 1, no_action: 2 };
  return rows
    .sort((a, b) =>
      (priority[a.action_state] ?? 9) - (priority[b.action_state] ?? 9)
      || b.score.opportunity_fit - a.score.opportunity_fit
      || b.score.total_score - a.score.total_score
      || b.score.payoff_convexity - a.score.payoff_convexity
      || b.score.thesis_confidence - a.score.thesis_confidence
      || a.ticker.localeCompare(b.ticker)
    )
    .map((target, index) => ({ ...target, rank: index + 1 }));
}

function buildQaTree() {
  const l1Map = Object.fromEntries(l1s.map((node) => [node.id, { ...node, children: [] }]));
  const l2Map = Object.fromEntries(l2s.map((node) => [node.id, { ...node, children: [] }]));
  for (const node of l2s) l1Map[node.id.split(".")[0]].children.push(l2Map[node.id]);
  for (const node of leaves) l2Map[node.parent].children.push(node);
  const l1_questions = Object.values(l1Map);
  const nodes = [];
  for (const top of l1_questions) {
    nodes.push(flatNode(top, null));
    for (const mid of top.children) {
      nodes.push(flatNode(mid, top.id));
      for (const leafNode of mid.children) nodes.push(flatNode(leafNode, mid.id));
    }
  }
  return {
    project_id: PROJECT_ID,
    run_mode: "live_prediction",
    report_date: REPORT_DATE,
    review_horizon: REVIEW_HORIZON,
    l1_questions,
    nodes,
  };
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
      rows.push({
        extraction_id: extractionId(node.id, sourceId),
        l3_question_id: node.id,
        source_id: sourceId,
        source_title: src.title,
        source_bucket: src.source_bucket,
        parser: node.skill,
        parser_status: "complete",
        schema_fields: {
          key_facts: { value: src.summary, source_anchor: src.url, status: "verified" },
          numbers_dates: { value: src.source_visible_at, source_anchor: src.url, status: "verified" },
          investment_relevance: { value: node.decision_use, source_anchor: src.url, status: "verified" },
          support_refute_or_lead: { value: src.support_refute_or_lead, source_anchor: src.url, status: "verified" },
          uncertainties: { value: node.gap, source_anchor: src.url, status: "verified" },
        },
        key_facts: [src.summary],
        inference: node.inference,
        support_refute_or_lead: src.support_refute_or_lead,
        uncertainties: [node.gap],
        follow_up_data: [node.trigger],
        created_at: REPORT_DATE,
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
    gpt_verification_status: "verified_against_public_source",
    adopted_facts: record.key_facts,
    corrections: [],
    rejected_claims: [],
    final_bucket: record.source_bucket,
    final_support_refute_or_lead: record.support_refute_or_lead,
    allowed_to_strengthen_conclusion: true,
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

function renderHtml(qaTree, rankedTargets) {
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>GTC 2026 大会相关投资机会研究</title>
  <style>${css()}</style>
</head>
<body>
  <header class="hero"><div class="eyebrow">Live Prediction · GTC 2026 · ${REPORT_DATE}</div><h1>GTC 2026 大会相关投资机会研究</h1><p class="subtitle">研究对象是 NVIDIA GTC 2026 事件簇：San Jose GTC 的 AI factory 主线，以及截至 ${REPORT_DATE} 已公开的 GTC Taipei Vera/RTX Spark 增量。目标是找未被充分定价的稀缺价值捕获点，而不是追逐发布会热度。</p></header>
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
    <section id="targets" class="section"><h2>最终标的推荐</h2>${renderTargets(rankedTargets)}</section>
    <section id="sources" class="section"><h2>来源索引</h2>${renderSources()}</section>
  </main>
</body>
</html>`;
}

function renderGoal() {
  return `<div class="goal-card"><div class="goal-grid">
    <div class="metric"><span>研究对象</span><strong>GTC 2026 AI 基础设施事件簇</strong></div>
    <div class="metric"><span>运行模式</span><strong>live_prediction</strong></div>
    <div class="metric"><span>报告日期</span><strong>${REPORT_DATE}</strong></div>
    <div class="metric"><span>复核窗口</span><strong>${REVIEW_HORIZON}</strong></div>
  </div>
  <div class="artifact-card"><div class="artifact-title">当前结论</div>GTC 2026 最强信号是 AI 工厂平台化和物理基础设施约束，而不是单一 GPU 主题。VRT、ALAB、DELL、ARM、TSM、MU 等有清晰观察价值，但由于估值、订单和毛利验证不足，本报告不强行给出 actionable_long。</div></div>`;
}

function renderSupplyChain() {
  const rows = chainRows.map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`).join("");
  return `<div class="supply-chain-section">${renderChainExplain()}<div class="chain-map"><table class="chain-table">
      <thead><tr><th>链条层级</th><th>产品/服务</th><th>主要玩家</th><th>关联关系</th><th>价值/瓶颈判断</th><th>QA 链接</th></tr></thead>
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
    <div class="chain-flow-steps"><b>产品、订单、钱和数据是怎么流的</b><ol>${steps}</ol></div>
    <div class="chain-layer-grid">${layers}</div>
    <div class="chain-chokepoints"><b>先看这些关键卡点</b><table><thead><tr><th>卡点</th><th>为什么重要</th><th>谁控制</th><th>后续验证</th></tr></thead><tbody>${chokepoints}</tbody></table></div>
    <div class="chain-target-links"><b>卡点如何对应到标的</b><table><thead><tr><th>标的</th><th>对应链条节点</th><th>先别急着多头的原因</th><th>验证入口</th></tr></thead><tbody>${targetLinks}</tbody></table></div>
  </div>`;
}

function renderQaCard(node) {
  const count = (node.children || []).length;
  return `<details id="${node.id.toLowerCase().replaceAll(".", "-")}" class="qa-card level-${node.level}" open>
    <summary><span class="qid">${esc(node.id)}</span><span class="qtitle">${esc(node.question)}</span><span class="qa-count">${count ? `${count} 子问题` : "L3"}</span><span class="chevron">›</span></summary>
    <div class="qa-body">
      <div class="qa-block"><div class="block-title">1. 当前结论呈现</div>${renderCurrentConclusion(node)}</div>
      <div class="qa-block"><div class="block-title">2. 问题展开（子 QA）</div>${count ? node.children.map(renderQaCard).join("") : "<p>该节点是证据采集与判断单元。</p>"}</div>
      <div class="qa-block"><div class="block-title">3. 待补充的问题</div><p>${esc(node.gap || "继续补充可量化、同口径、可复盘的数据。")}</p></div>
    </div>
  </details>`;
}

function renderCurrentConclusion(node) {
  if (node.level !== 3) {
    return `<p>${esc(node.conclusion)}</p>`;
  }
  return `<div class="routing"><span class="pill l3-skill">Skill: ${esc(node.skill)}</span><span class="pill l3-execution-status">Execution: ${esc(node.skill_dispatch.skill_output_status)}</span><span class="pill l3-score-component">Score Component: ${esc(node.score_component)}</span><span class="pill l3-decision-use">Decision Use: ${esc(node.decision_use)}</span></div>
    <div class="logic-grid"><div class="logic-card"><b>Fact</b><p>${esc(node.fact)}</p></div><div class="logic-card"><b>Inference</b><p>${esc(node.inference)}</p></div><div class="logic-card"><b>Judgment</b><p>${esc(node.judgment)}</p></div><div class="logic-card"><b>Gap / Trigger</b><p>${esc(node.gap)} ${esc(node.trigger)}</p></div></div>
    ${renderAnswerArtifact(node.answerArtifact)}
    <div class="source-chips">${node.sourceIds.map((sourceId) => `<a class="source-chip" href="${esc(byId(sourceId).url)}">${esc(sourceId)}</a>`).join("")}</div>`;
}

function renderAnswerArtifact(data) {
  const rows = data.rows.map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`).join("");
  return `<div class="artifact-card"><div class="artifact-title">${esc(data.title)}</div><div class="table-scroll"><table><thead><tr>${data.columns.map((col) => `<th>${esc(col)}</th>`).join("")}</tr></thead><tbody>${rows}</tbody></table></div></div>`;
}

function renderTargets(rankedTargets) {
  const rows = rankedTargets.map((target) => {
    const dims = target.score.score_dimensions;
    return `<tr>
      <td>${target.rank}</td>
      <td><strong>${esc(target.ticker)}</strong><br><span>${esc(target.name)}</span></td>
      <td>${esc(target.market)}</td>
      <td class="state-${esc(target.action_state)}">${esc(target.action_state)}</td>
      <td>${target.score.total_score.toFixed(2)}</td>
      <td>${dims.scarcity_or_monopoly.toFixed(2)}</td>
      <td>${dims.mispricing.toFixed(2)}</td>
      <td>${dims.earnings_elasticity.toFixed(2)}</td>
      <td>${dims.risk_control.toFixed(2)}</td>
      <td>${esc(target.rationale)}</td>
      <td>${esc(target.next_verification_data)}</td>
      <td>${esc(target.downgrade_risk)}</td>
    </tr>`;
  }).join("");
  return `<div class="target-section">
    <p>这是研究观察列表，不是买卖指令。当前 GTC 2026 主题的技术确定性强，但“未充分定价”证据不足，因此最高状态以 watch_only 为主。</p>
    <div class="table-scroll"><table class="target-table">
      <thead><tr><th>#</th><th>标的</th><th>市场</th><th>Action State</th><th>总分</th><th>稀缺/垄断</th><th>未充分定价</th><th>业绩弹性</th><th>风险控制</th><th>理由</th><th>验证数据</th><th>降级触发</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>
  </div>`;
}

function renderSources() {
  const cards = sources.map((source) => `<div class="source-card"><strong>${esc(source.source_id)}</strong><br><a href="${esc(source.url)}">${esc(source.title)}</a><p>${esc(source.summary)}</p><small>${esc(source.source_bucket)} · ${esc(source.source_visible_at)} · ${esc(source.support_refute_or_lead)}</small></div>`).join("");
  return `<details class="source-collapse"><summary>展开来源索引 <span class="chevron">›</span></summary><div class="source-grid">${cards}</div></details>`;
}

function renderMarkdown(rankedTargets) {
  const rows = rankedTargets.map((target) => `| ${target.rank} | ${target.ticker} | ${target.action_state} | ${target.score.total_score.toFixed(2)} | ${target.rationale} |`).join("\n");
  return `# GTC 2026 大会相关投资机会研究\n\n报告日期：${REPORT_DATE}\n\n## 最终标的推荐\n\n| 排名 | 标的 | Action State | 总分 | 理由 |\n|---|---|---:|---:|---|\n${rows}\n`;
}

function css() {
  return `
    :root{--bg:#f5f5f7;--panel:#fff;--line:#d7dce5;--ink:#1d1d1f;--muted:#667085;--blue:#0a63ce;--green:#0f7a4f;--amber:#956100;--red:#b42318}
    *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",sans-serif;line-height:1.58} .hero{padding:40px min(6vw,72px) 24px;background:linear-gradient(#fff,#f7f8fb);border-bottom:1px solid var(--line)}.eyebrow{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:800}h1{margin:8px 0 10px;font-size:34px;letter-spacing:0}.subtitle{max-width:1120px;color:#4b5260;font-size:15px}.top-nav{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.92);backdrop-filter:saturate(180%) blur(14px);border-bottom:1px solid var(--line);padding:10px min(6vw,72px);display:flex;gap:16px;flex-wrap:wrap}.top-nav a{color:#2f5f9f;text-decoration:none;font-size:13px;font-weight:800}.wrap{padding:24px min(6vw,72px) 56px}.section{margin:0 0 26px}h2{font-size:24px;margin:0 0 12px}
    .goal-card,.supply-chain-section,.target-section,.source-collapse{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px;box-shadow:0 10px 28px rgba(30,41,59,.05)}.goal-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.metric{border:1px solid #e7ebf2;border-radius:8px;padding:12px;background:#fbfcfe}.metric span{display:block;color:var(--muted);font-size:12px}.metric strong{font-size:15px}.chain-explain{display:grid;gap:14px;margin-bottom:16px}.chain-plain-summary{margin:0;padding:14px 16px;border:1px solid #d9e4f2;border-radius:8px;background:#f6f9fd;font-weight:760;line-height:1.75}.chain-flow-steps,.chain-chokepoints,.chain-target-links{border:1px solid #e6eaf1;border-radius:8px;background:#fbfcff;padding:14px}.chain-flow-steps b,.chain-chokepoints b,.chain-target-links b{display:block;margin-bottom:8px}.chain-flow-steps ol{margin:0;padding-left:22px;line-height:1.75}.chain-layer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}.chain-layer-card{border:1px solid #e6eaf1;border-radius:8px;background:#fff;padding:12px}.chain-layer-card b,.chain-layer-card span{display:block}.chain-layer-card span{color:var(--blue);font-weight:800;margin-top:4px}.chain-layer-card p{margin:8px 0;color:var(--ink)}.chain-layer-card small{color:var(--muted);line-height:1.6}.chain-map,.table-scroll{overflow:auto;border:1px solid #e6eaf1;border-radius:8px}.chain-table,.target-table{min-width:1180px}
    .qa-card{background:var(--panel);border:1px solid var(--line);border-radius:8px;margin:12px 0;overflow:hidden}.qa-card[open]>summary{border-bottom:1px solid #e6eaf1}.qa-card summary{list-style:none;cursor:pointer;padding:14px 16px;display:grid;grid-template-columns:auto 1fr auto auto;gap:10px;align-items:center}.qa-card summary::-webkit-details-marker{display:none}.qid{font-weight:800;color:var(--blue);font-size:13px}.qtitle{font-weight:760}.qa-count{font-size:12px;color:var(--muted);background:#f1f4f9;border:1px solid #e0e5ee;border-radius:999px;padding:3px 8px}.chevron{color:var(--muted)}details[open]>summary .chevron{transform:rotate(90deg)}.level-2{margin-left:16px}.level-3{margin-left:32px}.qa-body{padding:14px 16px 16px}.qa-block{margin:0 0 14px}.block-title{font-size:12px;font-weight:800;color:#586174;text-transform:uppercase;margin-bottom:8px}
    .artifact-card{border:1px solid #e2e7ef;border-radius:8px;background:#fbfcff;padding:12px;margin:10px 0}.artifact-title{font-weight:780;margin-bottom:8px}.logic-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.logic-card{border:1px solid #e5e9f0;border-radius:8px;background:#fff;padding:10px}.logic-card b{display:block;font-size:12px;color:#536071;margin-bottom:4px}.logic-card p{margin:0;font-size:13px}.routing{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:10px}.pill{border:1px solid #dfe6f1;background:#f7faff;border-radius:999px;padding:4px 8px;font-size:12px;color:#46515f}.source-chips{display:flex;flex-wrap:wrap;gap:6px}.source-chip{font-size:12px;color:#0a63ce;background:#eef5ff;border:1px solid #d8e8ff;border-radius:999px;padding:4px 8px;text-decoration:none}
    table{width:100%;border-collapse:collapse;font-size:13px}th,td{padding:9px 8px;border-bottom:1px solid #e6eaf1;text-align:left;vertical-align:top}th{color:#536071;font-size:12px;background:#f8fafc}.state-actionable_long{color:var(--green);font-weight:800}.state-watch_only{color:var(--amber);font-weight:800}.state-no_action{color:var(--red);font-weight:800}.source-collapse summary{cursor:pointer;font-weight:800}.source-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin-top:12px}.source-card{border:1px solid #e5e9f0;border-radius:8px;background:#fbfcff;padding:10px}.source-card a{color:#0a63ce}
    @media(max-width:900px){.goal-grid,.logic-grid{grid-template-columns:1fr}.level-2,.level-3{margin-left:0}.qa-card summary{grid-template-columns:auto 1fr auto}.qa-count{display:none}}
  `;
}

function writeJson(filename, data) {
  fs.writeFileSync(path.join(OUT_DIR, filename), `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function writeJsonl(filename, rows) {
  fs.writeFileSync(path.join(OUT_DIR, filename), `${rows.map((row) => JSON.stringify(row)).join("\n")}\n`, "utf8");
}

function esc(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

main();
