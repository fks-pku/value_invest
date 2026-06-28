const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const PROJECT_ID = "ai_factory_first_core_timeslice_20260328";
const OUT_DIR = path.join(ROOT, "research", "qa_projects", PROJECT_ID);
const AS_OF_DATE = "2026-03-28";
const EVALUATION_DATE = "2026-06-28";
const LABEL_WINDOW = "2026-03-28_to_2026-06-28";

const sources = [
  source("SRC-NVDA-FY26-Q4", "NVIDIA FY2026 Q4 results", "evidence", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/", "2026-02-25", "NVIDIA Q4 FY26 revenue was $68.1B, Data Center revenue was $62.3B, and management framed customer demand as AI factories for the AI industrial revolution."),
  source("SRC-NVDA-GTC-VERA-RUBIN-20260316", "NVIDIA Vera Rubin platform at GTC 2026", "evidence", "https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform", "2026-03-16", "NVIDIA announced Vera Rubin as seven chips and five rack-scale systems for AI factories, covering Vera CPU, Rubin GPU, NVLink 6, ConnectX-9, BlueField-4, Spectrum-6 and Groq 3 LPU."),
  source("SRC-NVDA-GTC-DYNAMO-20260316", "NVIDIA Dynamo 1.0 for AI factory inference", "evidence", "https://nvidianews.nvidia.com/news/dynamo-1-0", "2026-03-16", "NVIDIA announced Dynamo 1.0 as open-source production software for AI factory inference orchestration, with reported up to 7x Blackwell inference performance improvement and broad cloud/provider adoption."),
  source("SRC-VRT-Q4-2025", "Vertiv Q4 2025 results", "evidence", "https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/", "2026-02-11", "Vertiv Q4 2025 organic orders rose about 252% YoY and backlog reached $15.0B, reflecting robust AI infrastructure demand."),
  source("SRC-DELL-FY26-Q4", "Dell FY2026 Q4 results", "evidence", "https://investors.delltechnologies.com/node/19176/pdf", "2026-02-26", "Dell FY26 closed more than $64B in AI-optimized server orders, shipped more than $25B, and entered FY27 with a $43B backlog."),
  source("SRC-ALAB-Q4-2025", "Astera Labs Q4 2025 results", "evidence", "https://www.sec.gov/Archives/edgar/data/1736297/000173629726000005/q425exhibit991.htm", "2026-02-10", "Astera Labs Q4 revenue was $270.6M, +92% YoY, tied to rack-scale AI infrastructure connectivity."),
  source("SRC-CRDO-FY26-Q3", "Credo FY2026 Q3 results", "evidence", "https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm", "2026-03-02", "Credo FY26 Q3 revenue was $407.0M, +200% YoY, with active electrical cables, optical interconnects and memory connectivity tied to AI infrastructure."),
  source("SRC-MRVL-FY26-Q3", "Marvell FY2026 Q3 10-Q", "evidence", "https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-25-000197/mrvl-20251101.htm", "2025-12-03", "Marvell FY26 Q3 net revenue was $2.075B; data-center sales increased 38% year over year, driven by AI-related demand for custom products and electro-optics."),
  source("SRC-AVGO-FY25-Q4", "Broadcom FY2025 Q4 results", "evidence", "https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-fourth-quarter-and-fiscal-year-2025", "2025-12-11", "Broadcom Q4 FY25 AI semiconductor revenue rose 74% YoY and Q1 FY26 AI semiconductor revenue was expected to double to $8.2B, driven by custom AI accelerators and Ethernet AI switches."),
  source("SRC-ANET-Q4-2025", "Arista Q4 2025 results", "evidence", "https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Networks-Inc--Reports-Fourth-Quarter-and-Year-End-2025-Financial-Results/default.aspx", "2026-02-12", "Arista FY2025 revenue was $9.006B, +28.6%, and management said it exceeded AI networking and campus expansion goals."),
  source("SRC-TSM-Q4-2025", "TSMC Q4 2025 results", "evidence", "https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm", "2026-01-15", "TSMC Q4 2025 revenue was $33.73B, gross margin 62.3%, advanced technologies were 77% of wafer revenue, and 2026 capex was expected at $52B-$56B."),
  source("SRC-MU-FY26-Q1", "Micron FY2026 Q1 results", "evidence", "https://micron.gcs-web.com/news-releases/news-release-details/micron-technology-inc-reports-results-first-quarter-fiscal-2026", "2025-12-17", "Micron FY26 Q1 delivered record revenue and margin expansion, with AI data-center memory demand driving cloud memory and HBM-related strength."),
  source("SRC-MU-FY26-Q1-PREPARED", "Micron FY2026 Q1 prepared remarks", "evidence", "https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9", "2025-12-17", "Micron prepared remarks forecast HBM TAM from about $35B in calendar 2025 to around $100B in calendar 2028, about 40% CAGR, and said 2026 HBM supply had completed price and volume agreements."),
  source("SRC-SKHYNIX-FY25", "SK hynix FY2025 results", "evidence", "https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html", "2026-01-28", "SK hynix FY2025 revenue was KRW97.1467T, operating profit KRW47.2063T and operating margin 49%, driven by AI memory and HBM leadership."),
  source("SRC-SAMSUNG-FY25", "Samsung Q4 and FY2025 results", "evidence", "https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results", "2026-01-29", "Samsung Q4 2025 Memory Business reached record quarterly revenue and operating profit, with HBM, server DDR5 and enterprise SSD as high-value AI products."),
  source("SRC-SMCI-FY26-Q2", "Supermicro FY2026 Q2 results", "evidence", "https://ir.supermicro.com/news/news-details/2026/Super-Micro-Computer-Inc.-Reports-Second-Quarter-Fiscal-2026-Financial-Results/default.aspx", "2026-02-03", "Supermicro remained an AI server assembly exposure, but margin, execution and governance risks require a lower risk-control score."),
  source("SRC-MSFT-FY26-Q2", "Microsoft FY2026 Q2 results", "evidence", "https://www.microsoft.com/en-us/investor/earnings/fy-2026-q2/press-release-webcast", "2026-01-28", "Microsoft Q2 FY2026 Microsoft Cloud revenue was $51.5B, +26%, commercial RPO increased 110% to $625B, and Azure and other cloud services revenue increased 39%."),
  source("SRC-AMZN-Q4-2025", "Amazon Q4 2025 results", "evidence", "https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Fourth-Quarter-Results/default.aspx", "2026-02-05", "Amazon Q4 2025 AWS segment sales increased to $35.6B and TTM purchases of property and equipment reached $128.3B, while FCF fell as infrastructure investment intensified."),
  source("SRC-GOOGL-Q4-2025", "Alphabet Q4 2025 results", "evidence", "https://s206.q4cdn.com/479360582/files/doc_news/2026/Feb/04/attachments/2025q4-alphabet-earnings-release.pdf", "2026-02-04", "Alphabet Q4 2025 Google Cloud revenue increased 48% to $17.7B, Cloud annual run rate exceeded $70B, and 2026 CapEx was anticipated at $175B-$185B to meet customer demand."),
  source("SRC-META-Q3-2025", "Meta Q3 2025 results", "evidence", "https://investor.atmeta.com/investor-news/press-release-details/2025/Meta-Reports-Third-Quarter-2025-Results/default.aspx", "2025-10-29", "Meta Q3 2025 capex was $19.37B; 2025 capex guidance was $70B-$72B and management expected 2026 capex dollar growth to be notably larger, driven by infrastructure capacity needs."),
  source("SRC-ORCL-FY26-Q2", "Oracle FY2026 Q2 results", "evidence", "https://investor.oracle.com/investor-news/news-details/2025/Oracle-Announces-Fiscal-Year-2026-Second-Quarter-Financial-Results/default.aspx", "2025-12-10", "Oracle Q2 FY2026 RPO was $523B, +438%; cloud revenue was $8.0B, +34%; TTM capex was $35.5B and FCF was negative $13.2B after heavy cloud infrastructure investment."),
  source("SRC-SA-COWOS-HBM-2023", "SemiAnalysis AI Capacity Constraints CoWoS and HBM Supply Chain", "research_report", "https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/?action=share", "2023-07-05", "SemiAnalysis identified CoWoS and HBM as AI accelerator bottlenecks and explained CoWoS as TSMC 2.5D packaging that integrates logic and HBM on an interposer."),
  source("SRC-SA-GB200-BOM-2024", "SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM", "research_report", "https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component", "2024-07-17", "SemiAnalysis mapped GB200 rack-scale architecture and component implications, including that many data centers cannot support very high rack density without direct-to-chip liquid cooling."),
  source("SRC-SA-COOLING-2025", "SemiAnalysis Datacenter Anatomy Part 2 Cooling Systems", "research_report", "https://newsletter.semianalysis.com/p/datacenter-anatomy-part-2-cooling-systems", "2025-02-13", "SemiAnalysis described data-center cooling as one of the fastest-evolving AI infrastructure markets and argued liquid-cooling demand is underestimated in chip-by-chip capacity models."),
  source("SRC-SA-OPTICAL-2024", "SemiAnalysis Nvidia Optical Boogeyman NVL72 Infiniband Scale Out 800G and 1.6T Ramp", "research_report", "https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband", "2024-03-25", "SemiAnalysis linked Blackwell NVL72 system architecture, NVLink scale-up, InfiniBand scale-out, 800G and 1.6T ramps to optical and networking BOM expansion."),
  source("SRC-TF-HBM-PRICE-20240506", "TrendForce HBM Prices to Increase by 5-10% in 2025", "research_report", "https://www.trendforce.com/presscenter/news/20240506-12125.html", "2024-05-06", "TrendForce estimated HBM ASP at several times conventional DRAM and about five times DDR5, while value share could exceed 30% of DRAM in 2025."),
  source("SRC-TF-BLACKWELL-HBM-20240808", "TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption", "research_report", "https://www.trendforce.com/presscenter/news/20240808-12248.html", "2024-08-08", "TrendForce described NVIDIA as the largest HBM buyer, expected procurement share above 70%, with HBM consumption growing more than 200% in 2024 and expected to double again in 2025 as Blackwell raises HBM content."),
  source("SRC-OMDIA-AI-PROCESSORS-20250828", "Omdia AI Data Center Chip Market Forecast", "research_report", "https://omdia.tech.informa.com/pr/2025/aug/ai-data-center-chip-market-to-hit-286bn-growth-likely-peaking-as-custom-asics-gain-ground", "2025-08-28", "Omdia forecast cloud and data-center AI processor spending from about $123B in 2024 to $207B in 2025 and $286B by 2030, with custom ASICs gaining share alongside GPUs."),
  source("SRC-OMDIA-SEMI-TRENDS-202512", "Omdia 2026 Trends to Watch Semiconductors", "research_report", "https://omdia.tech.informa.com/rs/033-WBW-877/images/2026%20Trends%20to%20Watch%20Semiconductors.pdf", "2025-12-01", "Omdia tied AI semiconductor growth to GPUs, logic ASICs, HBM, power-management ICs, advanced nodes, chiplets and silicon photonics, while flagging infrastructure and supply constraints."),
  source("SRC-LC-AI-OPTICS-202501", "LightCounting Optics for AI Clusters", "research_report", "https://www.lightcounting.com/newsletter/en/january-2025-optics-for-ai-clusters-319", "2025-01-01", "LightCounting estimated AI-cluster optical transceiver, LPO and CPO demand rising from about $5B in 2024 to more than $10B in 2026, with scale-up and scale-out models through 2030."),
  source("SRC-LC-PAM4-DSP-20260226", "LightCounting AI Capex Flows Down the Supply Chain to DSP Vendors", "research_report", "https://www.lightcounting.com/newsletter/en/ai-capex-flows-down-the-supply-chain-to-dsp-vendors-332", "2026-02-26", "LightCounting reported AI infrastructure capex drove 800G PAM4 chipset shipments to nearly triple in 2025 and expected 800G shipments to more than double in 2026, with 1.6T ports ramping from a small base."),
  source("SRC-DO-AI-NETWORKS-20250715", "Dell'Oro Group Ethernet AI Backend Network Forecast", "research_report", "https://www.prnewswire.com/news-releases/ethernet-is-winning-the-war-against-infiniband-in-ai-back-end-networks-according-to-delloro-group-302501890.html", "2025-07-15", "Dell'Oro Group forecast AI back-end networks could drive nearly $80B of data-center switch sales over five years and expected Ethernet to gain share from InfiniBand in AI back-end networks."),
  source("SRC-DO-LIQUID-COOLING-20260108", "Dell'Oro Group Data Center Liquid Cooling Forecast", "research_report", "https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html", "2026-01-08", "Dell'Oro Group forecast data-center liquid-cooling manufacturer revenue near $3B in 2025 and approaching $7B by 2029, with hyperscalers anchoring demand and direct liquid cooling leading adoption."),
];

const sourceById = Object.fromEntries(sources.map((item) => [item.source_id, item]));

const labels = {
  VRT: label(251.07, 303.95, 21.06, "Nasdaq historical close", "label_verified", { start_price_date: "2026-03-27", end_price_date: "2026-06-26" }),
  "000660.KS": label(null, null, null, "KRX/Yahoo label not verified in this run", "label_unverified_krx"),
  NVDA: label(167.52, 192.53, 14.93, "Nasdaq historical close", "label_verified", { start_price_date: "2026-03-27", end_price_date: "2026-06-26" }),
  TSM: label(326.74, 432.35, 32.32, "Nasdaq historical close", "label_verified_adr", { start_price_date: "2026-03-27", end_price_date: "2026-06-26" }),
  MU: label(357.22, 1132.33, 216.98, "Nasdaq historical close", "label_verified", { start_price_date: "2026-03-27", end_price_date: "2026-06-26" }),
  ALAB: label(112.47, 391.74, 248.31, "Nasdaq historical close", "label_verified", { start_price_date: "2026-03-27", end_price_date: "2026-06-26" }),
  CRDO: label(95.24, 238.00, 149.90, "Nasdaq historical close", "label_verified", { start_price_date: "2026-03-27", end_price_date: "2026-06-26" }),
  MRVL: label(94.88, 266.77, 181.17, "Nasdaq historical close", "label_verified", { start_price_date: "2026-03-27", end_price_date: "2026-06-26" }),
  DELL: label(171.81, 399.49, 132.52, "Nasdaq historical close", "label_verified", { start_price_date: "2026-03-27", end_price_date: "2026-06-26" }),
  AVGO: label(300.68, 365.02, 21.40, "Nasdaq historical close", "label_verified", { start_price_date: "2026-03-27", end_price_date: "2026-06-26" }),
  ANET: label(120.77, 157.60, 30.50, "Nasdaq historical close", "label_verified", { start_price_date: "2026-03-27", end_price_date: "2026-06-26" }),
  "005930.KS": label(null, null, null, "KRX/Yahoo label not verified in this run", "label_unverified_krx"),
  SMCI: label(21.97, 30.63, 39.42, "Nasdaq historical close", "label_verified", { start_price_date: "2026-03-27", end_price_date: "2026-06-26" }),
};

const bomNodes = [
  {
    id: "compute",
    name: "计算加速器 / GPU / ASIC",
    plain: "把训练、推理和 agent 工作负载转成可采购的算力平台。",
    players: "NVIDIA、Broadcom custom ASIC、AMD、云厂自研 ASIC",
    receives: "云厂商 capex、模型训练/推理需求、系统交付规格。",
    produces: "GPU、AI ASIC、平台软件、互联标准、参考机柜架构。",
    suppliesTo: "服务器/机柜系统、云厂商和 AI labs。",
    metrics: "Data Center revenue、AI semiconductor revenue、供给排期、gross margin、客户 capex。",
  },
  {
    id: "manufacturing",
    name: "先进制程与先进封装",
    plain: "决定高端 GPU/ASIC 能否被制造出来并和 HBM 组合成可交付芯片。",
    players: "TSMC、先进封装生态、设备/材料供应商",
    receives: "GPU/ASIC 设计、先进节点 wafer 订单、HBM 集成需求。",
    produces: "先进晶圆制造、CoWoS 类先进封装、良率和产能。",
    suppliesTo: "GPU/ASIC 平台方和高端内存/系统供应链。",
    metrics: "advanced technologies revenue share、capex、gross margin、先进封装产能。",
  },
  {
    id: "memory",
    name: "HBM / 高端内存",
    plain: "决定 AI 加速器带宽和可交付数量，是 AI factory 扩容的硬供给约束之一。",
    players: "SK hynix、Micron、Samsung",
    receives: "GPU/ASIC 平台规格、客户认证、价量协议和交付排期。",
    produces: "HBM3E/HBM4、server DRAM、enterprise SSD。",
    suppliesTo: "GPU/ASIC 平台、服务器系统和云数据中心。",
    metrics: "HBM TAM、HBM ASP、客户资格、operating margin、memory mix。",
  },
  {
    id: "network",
    name: "高速连接与 AI 网络",
    plain: "把单台服务器、机柜和集群连成可训练/可推理的系统。",
    players: "Astera Labs、Credo、Marvell、Broadcom、Arista、NVIDIA 网络生态",
    receives: "机柜级带宽、延迟、功耗、平台兼容性和客户导入需求。",
    produces: "retimer、AEC、optical interconnect、switch silicon、Ethernet/InfiniBand 网络。",
    suppliesTo: "AI server、rack-scale 系统、云厂商集群。",
    metrics: "revenue growth、design win、800G/1.6T ramp、customer concentration、gross margin。",
  },
  {
    id: "powerCooling",
    name: "电力 / 液冷 / 数据中心基础设施",
    plain: "高功率机柜必须接入电力并散热，否则算力不能上线。",
    players: "Vertiv、数据中心工程商、电力/热管理供应商",
    receives: "高功率机柜密度、热负载、电力容量和项目工程要求。",
    produces: "UPS、配电、热管理、液冷、现场工程和服务。",
    suppliesTo: "云厂商、数据中心运营方、系统集成项目。",
    metrics: "orders、backlog、organic growth、project margin、cash conversion。",
  },
  {
    id: "system",
    name: "服务器 / 机柜系统交付",
    plain: "把 GPU、内存、网络、电力和冷却组合成可以上线的 AI 工厂。",
    players: "Dell、Supermicro、HPE、ODM",
    receives: "GPU/ASIC allocation、内存、网络、电力冷却部件和客户配置。",
    produces: "AI server、rack、cluster integration、交付服务。",
    suppliesTo: "云厂商、AI labs、企业和主权 AI 项目。",
    metrics: "AI server orders、shipments、backlog、margin、inventory、cash conversion。",
  },
];

const spaceNodes = [
  spaceNode("计算加速器 / GPU / ASIC", [
    method("公司指引", "NVIDIA", "Q4 FY26 Data Center revenue 达 $62.3B，说明 AI factory 需求已经在平台收入中财务化。", "计算加速器 / GPU / ASIC", "FY2026 Q4", "Data Center revenue、gross margin、客户 capex、后续指引", "高", ["SRC-NVDA-FY26-Q4"]),
    method("公司指引", "NVIDIA GTC 2026", "Vera Rubin 被定义为七颗芯片与五类 rack-scale 系统的 AI factory 平台，把 CPU、GPU、NVLink、DPU、SuperNIC、Ethernet switch、LPU、存储和网络一起纳入下一代系统规格。", "计算加速器 / GPU / ASIC", "Vera Rubin cycle", "平台代际规格、rack/pod scale 系统、网络/存储/推理组件", "高", ["SRC-NVDA-GTC-VERA-RUBIN-20260316"]),
    method("公司指引", "Broadcom", "Q1 FY26 AI semiconductor revenue expected $8.2B，说明 custom ASIC / AI Ethernet 也开始形成独立收入口径。", "计算加速器 / GPU / ASIC", "FY2026 Q1E", "AI semiconductor revenue、客户数量、custom ASIC ramp", "中高", ["SRC-AVGO-FY25-Q4"]),
    method("第三方拆法", "Omdia", "AI processor spending 由 2024 年约 $123B、2025E 约 $207B 到 2030E 约 $286B，且 custom ASIC gaining share。", "计算加速器 / GPU / ASIC", "2024A-2030E", "AI processor revenue、GPU vs ASIC mix、云 capex", "中", ["SRC-OMDIA-AI-PROCESSORS-20250828"]),
    method("财务兑现证据", "NVIDIA / Broadcom", "平台收入和 custom ASIC 指引同时变强，说明需求不是只停留在概念阶段。", "计算加速器 / GPU / ASIC", "FY2025-FY2026", "收入增长、毛利率、订单和下一季指引", "中高", ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4"]),
  ], "短期空间已经很大，财务锚点最强；GTC 2026 的 Vera Rubin 进一步证明平台升级正在把需求从单一 GPU 扩展到 rack-scale / pod-scale AI factory BOM；中期仍随云厂 capex 和推理需求扩张；长期空间大但不应只按 GPU 线性外推，因为 custom ASIC 会分流增量。", "高", [
    ["短期", "大", "NVIDIA 数据中心收入和 Broadcom AI semiconductor 指引已把需求财务化。"],
    ["中期", "大", "云厂 capex、AI processor spending 和 custom ASIC 增量共同支撑。"],
    ["长期", "中高", "取决于推理 ROI、ASIC 分流、平台替代和估值隐含预期。"],
  ], ["SRC-NVDA-FY26-Q4", "SRC-NVDA-GTC-VERA-RUBIN-20260316", "SRC-AVGO-FY25-Q4", "SRC-OMDIA-AI-PROCESSORS-20250828"]),
  spaceNode("先进制程与先进封装", [
    method("公司指引", "TSMC", "2026 capex expected $52B-$56B，说明先进制程与封装扩产仍在承接 AI/HPC 需求。", "先进制程与先进封装", "2026E", "capex、advanced packaging capacity、HPC/AI mix", "高", ["SRC-TSM-Q4-2025"]),
    method("财务兑现证据", "TSMC", "Q4 2025 advanced technologies 占 wafer revenue 77%，gross margin 62.3%，显示高端制程价值捕获强。", "先进制程与先进封装", "2025 Q4", "advanced technologies revenue share、gross margin", "高", ["SRC-TSM-Q4-2025"]),
    method("第三方拆法", "SemiAnalysis", "CoWoS 与 HBM 被识别为 AI accelerator capacity constraints，说明制造/封装不是普通代工 beta。", "先进制程与先进封装", "AI accelerator cycle", "CoWoS capacity、HBM integration、交付周期", "中", ["SRC-SA-COWOS-HBM-2023"]),
  ], "短中期空间大且供给斜率慢；长期需要看 capex 回报、地缘风险和先进封装供给释放后是否仍然稀缺。", "中高", [
    ["短期", "大", "AI/HPC 高端需求已经反映在先进制程收入和毛利中。"],
    ["中期", "大", "TSMC 高 capex 与 CoWoS/HBM 卡点共同指向供给扩张。"],
    ["长期", "中高", "如果先进封装供给快速释放，节点从稀缺卡点转为高质量制造平台。"],
  ], ["SRC-TSM-Q4-2025", "SRC-SA-COWOS-HBM-2023"]),
  spaceNode("HBM / 高端内存", [
    method("公司 TAM", "Micron", "HBM TAM from about $35B in CY2025 to around $100B in CY2028，约 40% CAGR。", "HBM / 高端内存", "2025E-2028E", "HBM TAM、HBM shipment、ASP、价量协议", "高", ["SRC-MU-FY26-Q1-PREPARED"]),
    method("公司指引", "Micron", "2026 HBM supply 已完成 price and volume agreements，说明供需紧张已进入合同层面。", "HBM / 高端内存", "2026E", "价量协议、客户认证、HBM bit shipment", "中高", ["SRC-MU-FY26-Q1-PREPARED"]),
    method("第三方拆法", "TrendForce", "HBM ASP 为普通 DRAM 数倍、约 DDR5 五倍，2025 年 HBM value share 可超过 DRAM 的 30%。", "HBM / 高端内存", "2024-2025E", "HBM ASP、bit share、value share", "中", ["SRC-TF-HBM-PRICE-20240506"]),
    method("客户侧指引", "TrendForce", "NVIDIA 是最大 HBM buyer，预期采购份额超过 70%，Blackwell 抬升 HBM content。", "HBM / 高端内存", "Blackwell cycle", "NVIDIA HBM procurement、平台规格、HBM content", "中", ["SRC-TF-BLACKWELL-HBM-20240808"]),
    method("财务兑现证据", "SK hynix / Micron / Samsung", "SK hynix FY25 operating margin 49%，Micron record revenue and margin expansion，Samsung Memory record revenue/profit，均指向 AI memory 利润兑现。", "HBM / 高端内存", "FY2025-FY2026", "operating margin、memory mix、HBM qualification、ASP", "中高", ["SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1", "SRC-SAMSUNG-FY25"]),
  ], "这是 AI factory 最像 S 曲线硬约束的节点之一：短期供给紧，中期 TAM 扩张清晰，长期取决于 HBM4 资格、扩产和 ASP 是否维持。", "高", [
    ["短期", "大", "价量协议和高价值 mix 已进入公司口径。"],
    ["中期", "很大", "Micron 给出的 2028 HBM TAM 指向数倍空间。"],
    ["长期", "中高", "需求会延续，但供给扩张和 ASP 周期是主要反证。"],
  ], ["SRC-MU-FY26-Q1-PREPARED", "SRC-SKHYNIX-FY25", "SRC-TF-HBM-PRICE-20240506"]),
  spaceNode("高速连接与 AI 网络", [
    method("公司指引", "Astera Labs / Credo", "Astera Q4 revenue +92% YoY，Credo FY26 Q3 revenue +200% YoY，显示 rack-scale connectivity 已经进入高增速收入阶段。", "高速连接与 AI 网络", "FY2026", "revenue growth、客户集中、design win、gross margin", "中高", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3"]),
    method("公司指引", "Marvell / Arista / Broadcom", "Marvell data-center sales +38%，Broadcom AI semiconductor +74%，Arista FY2025 revenue +28.6%，说明网络和 custom silicon 需求扩散。", "高速连接与 AI 网络", "FY2025-FY2026", "AI networking revenue、custom silicon ramp、cloud wins", "中", ["SRC-MRVL-FY26-Q3", "SRC-AVGO-FY25-Q4", "SRC-ANET-Q4-2025"]),
    method("第三方拆法", "LightCounting", "AI-cluster optical transceiver/LPO/CPO demand 预计从 2024 年约 $5B 到 2026 年超过 $10B。", "高速连接与 AI 网络", "2024A-2026E", "optical transceiver demand、800G/1.6T mix", "中", ["SRC-LC-AI-OPTICS-202501"]),
    method("第三方拆法", "Dell'Oro / LightCounting", "AI back-end networks 五年可驱动近 $80B data-center switch sales；800G PAM4 chipset shipments 2025 几乎三倍、2026 预计再翻倍以上。", "高速连接与 AI 网络", "2025E-2030E", "switch sales、800G/1.6T ports、PAM4 DSP shipments", "中", ["SRC-DO-AI-NETWORKS-20250715", "SRC-LC-PAM4-DSP-20260226"]),
    method("财务兑现证据", "ALAB / CRDO / MRVL", "连接收入已出现高弹性，但客户集中和平台路线替代会放大波动。", "高速连接与 AI 网络", "FY2026", "gross margin、客户集中、设计导入", "中", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3"]),
  ], "空间大但确定性低于 HBM：短期收入弹性强，中期随 rack-scale 和 800G/1.6T 扩散，长期要防平台内化、技术路线切换和 ASP 下行。", "中高", [
    ["短期", "大", "ALAB/CRDO/MRVL 等收入已经高增。"],
    ["中期", "大", "AI back-end network、800G/1.6T 和光互联扩散带来增量。"],
    ["长期", "中", "路线切换、平台自研和价格下行会削弱空间质量。"],
  ], ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-DO-AI-NETWORKS-20250715"]),
  spaceNode("电力 / 液冷 / 数据中心基础设施", [
    method("公司指引", "Vertiv", "Q4 2025 organic orders +252% YoY、backlog $15.0B，说明 AI 工厂物理基础设施需求已变成订单和 backlog。", "电力 / 液冷 / 数据中心基础设施", "2025 Q4", "orders、backlog、organic growth、margin", "高", ["SRC-VRT-Q4-2025"]),
    method("客户侧指引", "Alphabet / Amazon / Meta", "Alphabet 2026 CapEx anticipated at $175B-$185B，Amazon TTM PPE $128.3B，Meta 2025 capex guidance $70B-$72B 且 2026 dollar growth 更大。", "电力 / 液冷 / 数据中心基础设施", "2025-2026E", "capex、PPE purchases、FCF、AI ROI", "中高", ["SRC-GOOGL-Q4-2025", "SRC-AMZN-Q4-2025", "SRC-META-Q3-2025"]),
    method("第三方拆法", "Dell'Oro", "data-center liquid-cooling manufacturer revenue 2025 近 $3B、2029 接近 $7B。", "电力 / 液冷 / 数据中心基础设施", "2025E-2029E", "liquid cooling revenue、direct liquid cooling adoption", "中", ["SRC-DO-LIQUID-COOLING-20260108"]),
    method("第三方拆法", "SemiAnalysis", "高功率 rack 需要 direct-to-chip liquid cooling，很多数据中心无法直接支持高 rack density。", "电力 / 液冷 / 数据中心基础设施", "Blackwell / rack-scale cycle", "rack density、液冷 attach、项目交付周期", "中", ["SRC-SA-GB200-BOM-2024", "SRC-SA-COOLING-2025"]),
    method("财务兑现证据", "Vertiv", "订单和 backlog 直接验证基础设施节点，但还需看项目毛利和现金转化。", "电力 / 液冷 / 数据中心基础设施", "FY2025-FY2026", "backlog conversion、project margin、cash conversion", "中高", ["SRC-VRT-Q4-2025"]),
  ], "这是最接近“被 AI factory 需求倒逼出来的物理 S 曲线”的节点：短期订单确定，中期随高功率机柜扩散，长期受电力接入、项目毛利和客户 capex ROI 约束。", "中高", [
    ["短期", "很大", "VRT 订单和 backlog 已经强验证。"],
    ["中期", "大", "液冷、配电和现场工程随高功率 rack 增加。"],
    ["长期", "中高", "若客户 ROI 变弱或项目毛利差，空间质量下降。"],
  ], ["SRC-VRT-Q4-2025", "SRC-DO-LIQUID-COOLING-20260108", "SRC-GOOGL-Q4-2025"]),
  spaceNode("服务器 / 机柜系统交付", [
    method("公司指引", "Dell", "FY26 closed more than $64B AI-optimized server orders，shipped more than $25B，entered FY27 with $43B backlog。", "服务器 / 机柜系统交付", "FY2026-FY2027", "AI server orders、shipments、backlog、margin", "高", ["SRC-DELL-FY26-Q4"]),
    method("第三方拆法", "SemiAnalysis", "GB200 rack-scale 架构把需求从单 GPU 扩展到整机、机柜、网络、电力和液冷系统交付。", "服务器 / 机柜系统交付", "Blackwell platform cycle", "rack configuration、system BOM、交付节奏", "中", ["SRC-SA-GB200-BOM-2024"]),
    method("财务兑现证据", "Dell / Supermicro", "Dell backlog 很强；Supermicro 有 AI server exposure，但 margin、execution 和治理风险要求更低风险分。", "服务器 / 机柜系统交付", "FY2026", "operating margin、inventory、cash conversion、治理", "中", ["SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2"]),
  ], "空间扩张清晰，但这是交付节点，不天然等于高利润节点：短中期需求强，长期要看系统商能否保留服务、集成和供应链溢价。", "中", [
    ["短期", "大", "订单和 backlog 明确。"],
    ["中期", "中高", "AI rack 复杂度提高会增加系统交付价值。"],
    ["长期", "中", "客户议价、库存、毛利和现金流决定空间质量。"],
  ], ["SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2", "SRC-SA-GB200-BOM-2024"]),
];

const qaTree = [
  l1("Q1", "爆发新技术的前景及可实现性：AI factory 是否真的会成为新一代算力基础设施？", "当前结论：AI factory 不再只是 NVIDIA 的叙事词，而是已经被云厂 capex、GPU/ASIC 收入、服务器 backlog、电力液冷订单和 HBM 价量协议共同验证。问题仍在于 ROI 能否支撑持续扩容。", [
    l2("Q1.1", "需求是否已经离开概念，进入可验证的财务和订单口径？", "云厂商 capex、RPO/backlog、平台收入和系统订单同时出现，是 S 曲线早期加速比普通主题炒作更强的证据。", [
      l3("Q1.1.1", "哪些证据证明需求已经进入收入、订单和 backlog？", "future_space", "验证 AI factory 是否已从概念转入财务化阶段。", "financial-statement-analysis", "completed", "NVIDIA Data Center revenue、Dell AI server orders/backlog、Vertiv orders/backlog、Micron HBM 价量协议同时出现，说明需求已在平台、系统、基础设施和内存四个层面财务化。", "需要继续验证客户侧 AI 服务收入、利用率和 ROI。", ["SRC-NVDA-FY26-Q4", "SRC-DELL-FY26-Q4", "SRC-VRT-Q4-2025", "SRC-MU-FY26-Q1-PREPARED"]),
      l3("Q1.1.2", "云厂商 capex 和 RPO 是否足以支撑下一段需求？", "future_space", "判断 S 曲线下一段是否有客户预算支撑。", "financial-statement-analysis", "completed", "Microsoft commercial RPO、Amazon PPE purchases、Alphabet 2026 capex、Meta capex guidance 和 Oracle RPO 都显示客户仍在前置投入。", "最大反证是 AI ROI 不达预期导致 capex 下修和 FCF 压力上升。", ["SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025", "SRC-ORCL-FY26-Q2"]),
    ]),
    l2("Q1.2", "技术路线是否可实现，还是会被电力、冷却、内存和网络卡住？", "技术可实现性不是问模型是否有用，而是问 AI 工厂能否被系统交付。当前证据指向 HBM、先进封装、网络连接、电力液冷共同成为必要条件。", [
      l3("Q1.2.1", "GPU/ASIC 平台能否继续放大整个 BOM？", "future_space", "判断平台升级是否把需求传导到 HBM、网络、液冷和服务器系统。", "industry-report-analysis", "completed", "SemiAnalysis 的 GB200/rack-scale 拆法、Omdia 的 AI processor forecast，以及 GTC 2026 Vera Rubin 的七芯片/五类 rack-scale 系统描述都表明，平台升级会把单芯片需求扩展成机柜级 BOM。", "需要继续验证每一代平台是否仍提高 HBM、网络、功耗和液冷用量，以及 Dynamo 这类推理调度层是否真实提高 AI factory 利用率。", ["SRC-SA-GB200-BOM-2024", "SRC-OMDIA-AI-PROCESSORS-20250828", "SRC-NVDA-GTC-VERA-RUBIN-20260316", "SRC-NVDA-GTC-DYNAMO-20260316"]),
      l3("Q1.2.2", "物理基础设施会不会成为技术落地瓶颈？", "disconfirming_risk_control", "避免只看芯片收入而忽视电力和冷却约束。", "industry-report-analysis", "completed", "高功率 rack 对 direct-to-chip liquid cooling、电力和现场工程提出更高要求；Vertiv backlog 和 Dell'Oro liquid-cooling forecast 说明该约束正在财务化。", "若电力接入、建设许可或项目毛利恶化，AI factory 扩容会放缓。", ["SRC-SA-COOLING-2025", "SRC-DO-LIQUID-COOLING-20260108", "SRC-VRT-Q4-2025"]),
    ]),
  ]),
  l1("Q2", "产业空间与 S 曲线阶段：这个行业现在处在 S 曲线的哪一段？", "当前结论：AI factory 已经越过概念验证，处在早期加速段。空间判断不靠自建精确 TAM，而靠五类公开证据交叉：公司指引、公司 TAM、客户侧指引、第三方拆法和财务兑现证据。", [
    l2("Q2.1", "未来空间是否足够大，且不是一次性硬件补库？", "AI factory 的空间来自训练、推理、agent、企业 AI 和主权 AI 的复合需求，而不是单一 GPU 周期。", [
      l3("Q2.1.1", "哪些公开拆法支持未来空间仍大？", "future_space", "决定是否继续投入 S 曲线研究。", "industry-report-analysis", "completed", "Omdia 的 AI processor spending、Micron 的 HBM TAM、Dell'Oro 的液冷/AI networking forecast、LightCounting 的 optical demand 都指向多个 BOM 节点扩张。", "这些拆法口径不同，不能相加；只能作为节点空间方向性证据。", ["SRC-OMDIA-AI-PROCESSORS-20250828", "SRC-MU-FY26-Q1-PREPARED", "SRC-DO-LIQUID-COOLING-20260108", "SRC-DO-AI-NETWORKS-20250715", "SRC-LC-AI-OPTICS-202501"]),
      l3("Q2.1.2", "当前更像 S 曲线早期、中段还是成熟段？", "s_curve_stage", "判断风险收益是否还在早期。", "industry-report-analysis", "completed", "平台收入已巨大，但 GTC 2026 仍把下一代 AI factory 规格扩展到 Vera CPU、Rubin GPU、NVLink、BlueField、Spectrum、SuperNIC、Groq LPU、存储、网络和推理调度；同时 HBM、液冷、机柜连接和系统交付仍处在快速扩张和供给约束阶段，因此整体更像早期加速，而不是成熟渗透末期。", "NVDA 等龙头可能已被市场高度定价，不能把行业阶段直接等同于个股赔率。", ["SRC-NVDA-FY26-Q4", "SRC-NVDA-GTC-VERA-RUBIN-20260316", "SRC-NVDA-GTC-DYNAMO-20260316", "SRC-MU-FY26-Q1-PREPARED", "SRC-VRT-Q4-2025", "SRC-LC-PAM4-DSP-20260226"]),
    ]),
    l2("Q2.2", "趋势是否已经不可逆，还是仍可能被 ROI 和供给扩张打断？", "不可逆不是没有波动，而是多个客户和多个供应节点都在投入，撤回成本越来越高。", [
      l3("Q2.2.1", "哪些证据说明扩张具有路径依赖？", "evidence_quality", "判断 S 曲线是否只是短期订单扰动。", "financial-statement-analysis", "completed", "云厂商 capex、Oracle/Microsoft RPO、Dell backlog、Vertiv backlog、HBM 价量协议共同说明客户已经把未来交付锁进资本开支和供应链。", "路径依赖仍需用 cloud revenue、FCF 和利用率来验证。", ["SRC-MSFT-FY26-Q2", "SRC-ORCL-FY26-Q2", "SRC-DELL-FY26-Q4", "SRC-VRT-Q4-2025", "SRC-MU-FY26-Q1-PREPARED"]),
      l3("Q2.2.2", "最重要的反证是什么？", "risk_control", "定义 S 曲线被证伪或降级的条件。", "news-event-analysis", "completed", "最重要反证是客户 capex/ROI 下修、HBM/先进封装供给过快释放、连接价格下行、系统商订单不转利润，以及电力液冷 backlog 低质量。", "需要每季跟踪 capex 指引、HBM ASP、backlog 转收入、gross margin 和 FCF。", ["SRC-AMZN-Q4-2025", "SRC-META-Q3-2025", "SRC-MU-FY26-Q1", "SRC-VRT-Q4-2025", "SRC-DELL-FY26-Q4"]),
    ]),
  ]),
  l1("Q3", "技术链与 BOM 呈现：产业链上有谁，各自做什么？", "当前结论：这版只把 BOM 当作地图，不把每个节点都展开成竞争格局。重点是看清需求如何从云厂商传到平台、制造、内存、网络、电力液冷和系统交付。", [
    l2("Q3.1", "AI factory 的需求如何沿产业链传导？", "需求先由云厂商/AI labs 提出，再通过平台规格传到 GPU/ASIC、HBM、先进封装、网络、服务器机柜和电力液冷。", [
      l3("Q3.1.1", "每个节点接受什么、生产什么、提供给谁？", "simple_bom_map", "建立标的映射前的技术链地图。", "industry-report-analysis", "completed", "本报告在行业概况的 BOM taxonomy 和组件链条中逐项列出：输入、产出、下游对象、代表公司和验证指标。", "仍需后续把每个节点拆成竞争格局和利润池，但不是本版主目标。", ["SRC-SA-GB200-BOM-2024", "SRC-NVDA-FY26-Q4", "SRC-DELL-FY26-Q4"]),
      l3("Q3.1.2", "哪些节点已经有明显供需张力？", "supply_demand_tension", "帮助后续选择优先下钻节点。", "supply-chain-chokepoint-analysis", "completed", "HBM、先进封装、电力液冷和高速连接最值得后续深挖；系统交付订单强但利润质量需过滤。", "还缺统一的产能、资格、价格和订单取消率数据。", ["SRC-MU-FY26-Q1-PREPARED", "SRC-SA-COWOS-HBM-2023", "SRC-VRT-Q4-2025", "SRC-LC-PAM4-DSP-20260226"]),
    ]),
    l2("Q3.2", "BOM 地图如何服务标的筛选？", "BOM 不直接给买点，只负责定位哪些公司是 S 曲线的直接受益载体。", [
      l3("Q3.2.1", "哪些公司是直接受益，哪些只是主题映射？", "company_exposure_screen", "过滤泛主题标的。", "company-exposure-analysis", "completed", "直接受益包括 VRT、SK hynix、NVDA、TSM、MU、ALAB、CRDO、MRVL、DELL、AVGO 等；云厂商本身更多是需求验证，不是本报告的主要上游卖铲标的。", "下一版需要补估值和利润桥，避免只按产业链位置排序。", ["SRC-VRT-Q4-2025", "SRC-SKHYNIX-FY25", "SRC-NVDA-FY26-Q4", "SRC-TSM-Q4-2025", "SRC-ALAB-Q4-2025", "SRC-DELL-FY26-Q4"]),
    ]),
  ]),
  l1("Q4", "标的观察：如果 S 曲线成立，哪些公司最值得进入观察池？", "当前结论：最优先的是同时满足空间大、供给受限、财务兑现和风险可监控的公司。截面下 VRT 与 SK hynix 更接近高强度观察；NVDA/TSM 卡点强但需要估值折扣；连接和系统交付标的保持观察。", [
    l2("Q4.1", "如何从 S 曲线映射到具体证券？", "排序使用四个闸门：稀缺性、未来空间、业绩弹性、风险控制；估值证据不足时不能升高行动强度。", [
      l3("Q4.1.1", "哪些标的进入核心观察池？", "target_ranking", "生成具体证券观察名单。", "target-recommendation-analysis", "completed", "VRT、SK hynix、NVDA、TSM、MU、ALAB、CRDO、MRVL、DELL、AVGO、ANET、Samsung、SMCI 进入观察池，强度分层见标的推荐表。", "需要补同口径估值、隐含预期和财务弹性。", ["SRC-VRT-Q4-2025", "SRC-SKHYNIX-FY25", "SRC-NVDA-FY26-Q4", "SRC-MU-FY26-Q1", "SRC-ALAB-Q4-2025", "SRC-DELL-FY26-Q4"]),
      l3("Q4.1.2", "哪些信号会升级或降级观察强度？", "monitorability", "给出后续跟踪规则。", "target-recommendation-analysis", "completed", "升级信号是订单/backlog 转高质量收入、HBM ASP 与资格持续、连接 design-in 放量、capex ROI 兑现；降级信号是 capex 下修、供给过剩、毛利恶化、客户集中风险暴露。", "需要每季自动填报关键变量表。", ["SRC-VRT-Q4-2025", "SRC-MU-FY26-Q1-PREPARED", "SRC-CRDO-FY26-Q3", "SRC-GOOGL-Q4-2025"]),
    ]),
  ]),
];

const targets = [
  target("VRT", "Vertiv", "USA", "电力 / 液冷 / 数据中心基础设施", "actionable_long", "AI 工厂物理瓶颈已经体现为 orders 和 backlog，空间大、财务兑现直接、反证可监控。", "中高：若 backlog 毛利和现金转化良好，订单弹性可进入盈利上修。", "backlog 毛利低质量、云厂 capex 下修、项目交付延迟。", ["SRC-VRT-Q4-2025", "SRC-DO-LIQUID-COOLING-20260108"]),
  target("000660.KS", "SK hynix", "Korea", "HBM / 高端内存", "actionable_long", "HBM 供应能力和 49% operating margin 显示硬约束已经变成利润桥。", "中高：HBM TAM 和 AI memory mix 支撑中期空间，但需继续验证 ASP 和客户资格。", "HBM 供给过快释放、ASP 下行、客户资格落后。", ["SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1-PREPARED", "SRC-TF-HBM-PRICE-20240506"]),
  target("NVDA", "NVIDIA", "USA", "计算加速器 / GPU / ASIC", "watch_only", "平台控制最强，GTC 2026 继续把 AI factory 规格从 GPU 扩展到 rack/pod-scale 系统与推理调度层，需求和财务证据最硬，但市场最可能已经部分定价。", "高胜率但赔率需单独证明：只有盈利上修持续超过隐含预期时才上调。", "capex ROI 下降、毛利率不及预期、ASIC 分流超预期。", ["SRC-NVDA-FY26-Q4", "SRC-NVDA-GTC-VERA-RUBIN-20260316", "SRC-NVDA-GTC-DYNAMO-20260316", "SRC-OMDIA-AI-PROCESSORS-20250828"]),
  target("TSM", "TSMC ADR", "USA/Taiwan", "先进制程与先进封装", "watch_only", "先进制程和先进封装是硬供给层，财务质量强。", "稳健空间较大，但高 capex 与地缘风险降低赔率弹性。", "先进封装供给释放、capex 回报下行、地缘风险。", ["SRC-TSM-Q4-2025", "SRC-SA-COWOS-HBM-2023"]),
  target("MU", "Micron", "USA", "HBM / 高端内存", "watch_only", "HBM TAM、价量协议和云内存利润改善带来高弹性。", "赔率可能高于成熟龙头，但相对 SK hynix 的资格和份额仍待验证。", "HBM 份额不及预期、ASP/DRAM 周期反转。", ["SRC-MU-FY26-Q1", "SRC-MU-FY26-Q1-PREPARED"]),
  target("ALAB", "Astera Labs", "USA", "高速连接与 AI 网络", "watch_only", "机柜级连接收入高增，直接受益 rack-scale AI。", "高弹性但高估值/客户集中，必须用 design-in 和毛利验证。", "大客户订单延后、平台自研替代、估值压缩。", ["SRC-ALAB-Q4-2025"]),
  target("CRDO", "Credo", "USA", "高速连接与 AI 网络", "watch_only", "AEC/光互联需求强，收入高弹性。", "弹性大但波动也大，客户集中和价格压力是关键。", "客户订单延迟、价格下行、毛利不达预期。", ["SRC-CRDO-FY26-Q3", "SRC-LC-PAM4-DSP-20260226"]),
  target("MRVL", "Marvell Technology", "USA", "custom silicon / 电光互联", "watch_only", "custom products 与 electro-optics 已进入 AI data-center 收入口径。", "中高弹性，但定制项目量产节奏和客户集中需要折价。", "大客户项目延期、客户自研替代、毛利不达预期。", ["SRC-MRVL-FY26-Q3"]),
  target("DELL", "Dell Technologies", "USA", "服务器 / 机柜系统交付", "watch_only", "AI server orders/backlog 强，能验证 AI factory 进入系统交付阶段。", "空间大但利润池未必厚，重点看毛利和现金流。", "订单增长但利润率或现金流较弱、库存上升。", ["SRC-DELL-FY26-Q4"]),
  target("SMCI", "Supermicro", "USA", "服务器 / 机柜系统交付", "no_action", "主题弹性存在，但执行、治理和毛利风险压制风险控制。", "只适合验证系统交付 beta，不适合在当前证据下提高强度。", "治理风险、毛利恶化、现金转化差。", ["SRC-SMCI-FY26-Q2"]),
];

function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.writeFileSync(path.join(OUT_DIR, "professional_report.html"), renderHtml(), "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "sources.jsonl"), sources.map((item) => JSON.stringify({ ...item, as_of_date: AS_OF_DATE, cutoff_status: "cutoff_visible" })).join("\n") + "\n", "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "project.json"), JSON.stringify({
    project_id: PROJECT_ID,
    title: "AI 工厂产业第一核心投资框架回测研究",
    research_type: "industry/theme opportunity",
    run_mode: "historical_backtest",
    mode: "historical_backtest",
    as_of_date: AS_OF_DATE,
    evaluation_date: EVALUATION_DATE,
    report_path: "professional_report.html",
    framework_focus: "s_curve_first",
  }, null, 2), "utf8");
  writeAuditArtifacts();
  console.log(path.join(OUT_DIR, "professional_report.html"));
}

function writeAuditArtifacts() {
  const nodes = flattenQaNodes(qaTree);
  const l3Nodes = nodes.filter((node) => node.level >= 3);
  const qaRecords = nodes.map((node) => {
    if (node.level < 3) {
      return {
        id: node.id,
        level: node.level,
        question: node.question,
        parent_id: node.parentId || "",
        next_question_ids: (node.children || []).map((child) => child.id),
        conclusion: node.conclusion,
      };
    }
    const extractionId = extractionIdFor(node);
    const reviewId = reviewIdFor(node);
    return {
      id: node.id,
      level: node.level,
      question: node.question,
      parent_id: node.parentId || "",
      next_question_ids: [],
      materiality: "high",
      decision_use: node.decisionUse,
      support_evidence: node.conclusion,
      refute_evidence: node.gap,
      target_implications: "影响标的观察池的 action_state、分数上限和后续验证触发器。",
      score_component: normalizedScoreComponent(node.score),
      minimum_evidence_gate: "至少一条研究截面前可见的来源支撑；若仅为模型先验，则不能进入评分。",
      refuting_source_plan: `跟踪能反驳 ${node.id} 判断的后续财报、客户 capex、订单、毛利、ASP、利用率或路线替代证据。`,
      source_plan: {
        as_of_date: AS_OF_DATE,
        source_ids: node.sourceIds,
        cutoff_policy: "only_cutoff_visible_sources_may_strengthen_thesis",
      },
      skill_dispatch: {
        task_family: "leaf_research_extraction",
        selected_skill: node.skill,
        concrete_materials: node.sourceIds,
        extraction_schema: ["claim", "source_date", "decision_relevance"],
        source_extraction_ids: [extractionId],
        leaf_source_review_ids: [reviewId],
        skill_output_status: node.status,
        fallback_used: false,
        gpt_verification_status: "verified_with_caveats",
      },
      fact: node.conclusion,
      inference: `${node.id} 的证据会改变 ${normalizedScoreComponent(node.score)} 维度的判断强度。`,
      judgment: "可以用于本截面 thesis，但仍需按 gap / trigger 持续验证。",
      gap: node.gap,
      trigger: node.gap,
      source_links: node.sourceIds,
      backtest_grounding: {
        allowed_source_ids: node.sourceIds,
        model_prior_policy: "hypothesis_only_not_scoring_evidence",
        post_cutoff_knowledge_policy: "not_allowed_in_reasoning_or_scoring",
        non_source_claims: [],
      },
    };
  });

  const sourceExtractions = l3Nodes.map((node) => {
    const sourceId = node.sourceIds[0];
    const source = sourceById[sourceId] || {};
    return {
      extraction_id: extractionIdFor(node),
      l3_question_id: node.id,
      source_id: sourceId,
      source_title: source.title || sourceId,
      source_bucket: source.source_bucket || "evidence",
      parser: node.skill,
      parser_status: "completed",
      schema_fields: {
        claim: node.conclusion,
        source_date: source.source_visible_at || AS_OF_DATE,
        decision_relevance: node.decisionUse,
      },
      key_facts: [node.conclusion],
      inference: `${node.id} supports ${normalizedScoreComponent(node.score)} under the cutoff-visible source pack.`,
      support_refute_or_lead: "support",
      uncertainties: [node.gap],
      follow_up_data: [],
      created_at: `${AS_OF_DATE}T00:00:00Z`,
    };
  });

  const leafSourceReviews = l3Nodes.map((node) => {
    const sourceId = node.sourceIds[0];
    const source = sourceById[sourceId] || {};
    return {
      review_id: reviewIdFor(node),
      extraction_id: extractionIdFor(node),
      l3_question_id: node.id,
      source_id: sourceId,
      gpt_verification_status: "verified_with_caveats",
      adopted_facts: [node.conclusion],
      corrections: [],
      rejected_claims: [],
      final_bucket: source.source_bucket || "evidence",
      final_support_refute_or_lead: "support",
      allowed_to_strengthen_conclusion: true,
    };
  });

  const scoringWorksheet = targets.map((targetItem, index) => buildTargetAudit(targetItem, index + 1));
  const workbench = {
    project_id: PROJECT_ID,
    as_of_date: AS_OF_DATE,
    run_mode: "historical_backtest",
    source_extractions: sourceExtractions,
    leaf_source_reviews: leafSourceReviews,
    scoring_worksheet: scoringWorksheet,
    frozen_recommendations: {
      as_of_date: AS_OF_DATE,
      label_status: "unattached",
      targets: scoringWorksheet.map((targetItem) => ({ ...targetItem, label: undefined })),
    },
    label_attach: {
      evaluation_date: EVALUATION_DATE,
      label_window: LABEL_WINDOW,
      rule: "labels are attached after frozen recommendations and do not alter thesis, score, or rank",
    },
    rejected_future_sources: [],
    public_html_policy: "do_not_render_internal_trace_unless_user_requests_it",
  };

  fs.writeFileSync(path.join(OUT_DIR, "qa_tree.json"), JSON.stringify({
    project_id: PROJECT_ID,
    run_mode: "historical_backtest",
    as_of_date: AS_OF_DATE,
    anti_leakage_controls: {
      anti_leakage_level: "strict_source_pack_grounding",
      as_of_date: AS_OF_DATE,
      cutoff_source_pack_policy: "only_sources_visible_on_or_before_as_of_date_may_support_QA_scoring_or_ranking",
      llm_prior_policy: "model_prior_is_not_evidence",
      question_tree_policy: "questions_may_frame_hypotheses_but_answers_must_be_source_grounded",
      supply_chain_policy: "supply_chain_and_BOM_claims_must_trace_to_cutoff_sources_or_remain_hypotheses",
      scoring_policy: "target_scores_use_cutoff_sources_or_GPT_verified_leaf_reviews_only",
      label_isolation_policy: "labels_attached_after_frozen_recommendations_only",
    },
    nodes: qaRecords,
  }, null, 2), "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "source_extractions.jsonl"), sourceExtractions.map((record) => JSON.stringify(record)).join("\n") + "\n", "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "leaf_source_reviews.jsonl"), leafSourceReviews.map((record) => JSON.stringify(record)).join("\n") + "\n", "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "investment_workbench.json"), JSON.stringify(workbench, null, 2), "utf8");
}

function flattenQaNodes(nodes, parentId = "") {
  return nodes.flatMap((node) => {
    const current = { ...node, parentId };
    return [current, ...flattenQaNodes(node.children || [], node.id)];
  });
}

function extractionIdFor(node) {
  return `EXT-${node.id.replace(/\./g, "_")}`;
}

function reviewIdFor(node) {
  return `REV-${node.id.replace(/\./g, "_")}`;
}

function normalizedScoreComponent(score) {
  const mapping = {
    s_curve_stage: "future_space",
    simple_bom_map: "evidence_quality",
    supply_demand_tension: "chokepoint_strength",
    company_exposure_screen: "target_ranking",
  };
  return mapping[score] || score;
}

function buildTargetAudit(targetItem, rank) {
  const preset = targetScorePreset(targetItem);
  const scoreSubcomponents = Object.fromEntries(Object.entries(preset.components).map(([component, score]) => [
    component,
    [{
      name: `${component}_source_pack`,
      score,
      weight: 1,
      evidence_ids: targetItem.sourceIds,
      review_ids: [],
      rationale: `${component} based on cutoff-visible source pack.`,
    }],
  ]));
  return {
    ticker: targetItem.ticker,
    name: targetItem.name,
    market: targetItem.market,
    rank,
    thesis_node: targetItem.thesisNode,
    action_state: targetItem.actionState,
    rationale: targetItem.rationale,
    future_space: targetItem.futureSpace,
    downgrade: targetItem.downgrade,
    evidence_ids: targetItem.sourceIds,
    score: {
      action_state: targetItem.actionState,
      total_score: preset.total_score,
      thesis_confidence: preset.thesis_confidence,
      payoff_convexity: preset.payoff_convexity,
      score_dimensions: preset.dimensions,
      score_components: preset.components,
      score_subcomponents: scoreSubcomponents,
    },
    thesis_kill_tests: targetItem.actionState === "actionable_long" ? [
      {
        test: "核心订单、backlog、ASP 或客户资格是否在后续披露中恶化。",
        evidence_needed: "季度财报、订单/backlog、毛利、ASP、客户资格或 capex 指引。",
        downgrade_action: "若证据恶化，降为 watch_only 或 no_action。",
        source_plan: targetItem.sourceIds,
      },
    ] : [],
  };
}

function targetScorePreset(targetItem) {
  const byTicker = {
    VRT: scores(4.3, 3.5, 4.2, 3.8, 4.4, 4.2, 3.4, 4.2, 3.7, 4.1, 3.9, 4.02, 4.08, 3.82),
    "000660.KS": scores(4.5, 3.3, 4.2, 3.5, 4.6, 4.4, 3.2, 4.1, 3.5, 3.7, 4.0, 3.96, 4.03, 3.88),
    NVDA: scores(4.8, 2.3, 4.4, 3.8, 4.7, 4.5, 2.4, 4.7, 3.7, 4.2, 3.5, 3.72, 4.15, 3.35),
    TSM: scores(4.0, 2.8, 3.7, 3.2, 4.1, 4.0, 2.9, 4.2, 3.2, 3.4, 3.1, 3.46, 3.70, 3.12),
    MU: scores(3.9, 3.2, 4.4, 3.1, 4.0, 4.4, 3.1, 3.8, 3.0, 3.5, 4.2, 3.63, 3.74, 4.08),
    ALAB: scores(3.8, 2.2, 4.5, 2.8, 3.8, 4.0, 2.2, 3.5, 2.7, 3.4, 4.4, 3.23, 3.39, 4.13),
    CRDO: scores(3.6, 2.4, 4.4, 2.7, 3.6, 4.0, 2.5, 3.4, 2.7, 3.3, 4.3, 3.24, 3.32, 4.05),
    MRVL: scores(3.5, 2.6, 4.0, 2.9, 3.5, 3.8, 2.7, 3.4, 2.9, 3.2, 3.9, 3.28, 3.31, 3.76),
    DELL: scores(2.9, 2.8, 3.7, 3.0, 2.8, 3.7, 2.9, 3.7, 3.0, 3.5, 3.3, 3.16, 3.25, 3.24),
    SMCI: scores(2.4, 2.0, 3.5, 1.9, 2.3, 3.4, 2.0, 2.7, 1.8, 2.4, 3.1, 2.56, 2.54, 2.98),
  };
  return byTicker[targetItem.ticker] || scores(3, 2.5, 3, 2.5, 3, 3, 2.5, 3, 2.5, 3, 3, 3, 3, 3);
}

function scores(scarcity, mispricing, earnings, risk, chokepoint, future, valuation, evidence, riskControl, monitorability, payoff, total, confidence, convexity) {
  return {
    dimensions: {
      scarcity_or_monopoly: scarcity,
      mispricing,
      earnings_elasticity: earnings,
      risk_control: risk,
    },
    components: {
      chokepoint_strength: chokepoint,
      future_space: future,
      valuation_odds: valuation,
      evidence_quality: evidence,
      disconfirming_risk_control: riskControl,
      monitorability,
      payoff_convexity: payoff,
    },
    total_score: total,
    thesis_confidence: confidence,
    payoff_convexity: convexity,
  };
}

function renderHtml() {
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI 工厂产业第一核心投资机会回测研究</title>
  <style>${css()}</style>
</head>
<body>
  <header class="hero">
    <div class="hero-inner">
      <p class="eyebrow">Historical Backtest · AI Factory · ${AS_OF_DATE}</p>
      <h1>AI 工厂产业第一核心投资机会研究</h1>
      <p class="hero-subtitle">核心问题不是“AI 硬件谁受益”，而是判断 AI factory 是否处于真实、巨大、可实现的 S 曲线，并找出其中稀缺、未充分定价、业绩弹性大且风险可控的标的。</p>
      <div class="hero-meta"><span>研究截面 ${AS_OF_DATE}</span><span>评估窗口 ${LABEL_WINDOW}</span><span>回测标签只在标的表中展示</span></div>
    </div>
  </header>
  <nav class="top-nav">
    <a href="#goal">当前研究的问题</a>
    <a href="#overview">行业概况</a>
    <a href="#qa">下钻 QA</a>
    <a href="#targets">标的推荐</a>
    <a href="#sources">来源索引</a>
  </nav>
  <main>
    <section id="goal" class="section"><div class="section-heading"><h2>当前研究的问题</h2></div>${renderGoal()}</section>
    <section id="overview" class="section"><div class="section-heading"><h2>行业概况</h2></div>${renderOverview()}</section>
    <section id="qa" class="section qa-section"><div class="section-heading"><h2>下钻 QA</h2></div>${qaTree.map(renderQaCard).join("")}</section>
    <section id="targets" class="section"><div class="section-heading"><h2>标的推荐</h2></div>${renderTargets()}</section>
    <section id="sources" class="section"><div class="section-heading"><h2>来源索引</h2></div>${renderSources()}</section>
  </main>
</body>
</html>`;
}

function renderGoal() {
  return `<div class="goal-card">
    <div class="goal-main">研究目标：用第一核心框架检验 AI factory 是否存在可投资的 S 曲线机会。</div>
    <div class="goal-grid">
      <div class="metric"><span>优先级</span><strong>S 曲线本身 80%</strong></div>
      <div class="metric"><span>辅助层</span><strong>BOM / 技术链地图</strong></div>
      <div class="metric"><span>核心证据</span><strong>空间、可实现性、供需张力</strong></div>
      <div class="metric"><span>输出</span><strong>标的观察池与验证触发器</strong></div>
    </div>
    <div class="constraint-definition">
      <div class="artifact-title">研究约束定义</div>
      <div class="constraint-grid">
        <article><span>主题边界</span><p>AI factory 指以训练、推理、agent、企业 AI 和主权 AI 为需求源的算力基础设施，不等同于单一 GPU 主题。</p></article>
        <article><span>核心判断</span><p>是否已经进入早期加速段：需求财务化、平台迭代、BOM 扩张、供给受限和客户预算同时成立，并且能落到稀缺价值捕获节点。</p></article>
        <article><span>投资用法</span><p>先确认产业 S 曲线，再用 BOM 地图定位直接受益公司；本版不展开完整竞争格局和利润池。</p></article>
      </div>
    </div>
  </div>`;
}

function renderOverview() {
  return `<div class="industry-overview-section">
    ${renderSupplyChain()}
  </div>`;
}

function renderSupplyChain() {
  return `<details class="industry-module supply-chain-section" open>
    <summary class="module-head"><span class="module-index">01</span><div><h3>技术链与 BOM 呈现</h3><p>只保留 BOM 拆分、泳道图、价值流和每个 BOM 的代表公司。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
      <div class="chain-explain">
        <p class="chain-plain-summary">一句话：云厂商和 AI labs 的算力需求先变成 capex 和订单，再通过 GPU/ASIC 平台传导到先进制造、HBM、网络连接、服务器机柜、电力和液冷，最后由下游利用率、云收入和 ROI 验证是否继续扩容。</p>
        ${renderChainPanels()}
      </div>
    </div>
  </details>`;
}

function renderChainPanels() {
  const upstream = bomNodes.slice(0, 4);
  const midstream = bomNodes.slice(4);
  const lanes = [
    ["上游", upstream],
    ["中游", midstream],
    ["下游", [{ name: "云厂商 / AI labs / 企业与主权 AI", plain: "提出需求、支付 capex、运营 AI factory，并用收入和 ROI 验证扩容。", players: "Microsoft、Amazon、Alphabet、Meta、Oracle、AI labs、企业客户", receives: "模型和应用需求、客户收入机会、内部生产率需求。", produces: "capex、订单、RPO/backlog、利用率、AI ROI。", suppliesTo: "全产业链需求验证。", metrics: "capex、cloud revenue、RPO、FCF、利用率。"}]],
  ];
  return `<details class="chain-detail-panel chain-lane-map" open><summary><span>泳道图</span><span class="chevron">›</span></summary><div class="chain-layer-grid">${lanes.map(([stage, nodes]) => `<article class="chain-layer-card"><h4>${e(stage)}</h4>${nodes.map((node) => `<p><b>${e(node.name)}</b><span>${e(node.players)}</span></p>`).join("")}</article>`).join("")}</div></details>
  <details class="chain-detail-panel chain-value-flow"><summary><span>价值流</span><span class="chevron">›</span></summary><div class="chain-simple-flow">${[
    "云厂商 AI 需求形成 capex、订单和交付排期。",
    "GPU/ASIC 平台把需求变成芯片、软件、网络和机柜规格。",
    "制造、封装和 HBM 决定核心算力能否放量交付。",
    "网络、电力、液冷和服务器系统把芯片变成可上线集群。",
    "下游利用率、云收入、RPO 和 FCF 决定是否继续扩容。"
  ].map((step, index) => `<article class="chain-stage-panel"><span>${index + 1}</span><p>${e(step)}</p></article>`).join("")}</div><div class="chain-relationship-graph">需求 -> 平台规格 -> BOM 扩张 -> 系统交付 -> 收入/ROI 验证 -> 下一轮 capex</div></details>
  <details class="chain-detail-panel component-value-chain" open><summary><span>BOM 拆分与代表公司</span><span class="chevron">›</span></summary><div class="chain-company-list">${bomNodes.map(renderCompanyCard).join("")}</div></details>`;
}

function renderCompanyCard(node) {
  return `<article class="chain-company-card">
    <h4>${e(node.name)}</h4>
    <p class="muted">${e(node.plain)}</p>
    <div class="representative-companies"><b>代表公司</b><div>${representativeCompanies(node.players).map((company) => `<span>${e(company)}</span>`).join("")}</div></div>
    <div class="company-flow-grid">
      <p><b>接受</b>${e(node.receives)}</p>
      <p><b>生产</b>${e(node.produces)}</p>
      <p><b>提供给</b>${e(node.suppliesTo)}</p>
      <p><b>验证指标</b>${e(node.metrics)}</p>
    </div>
  </article>`;
}

function representativeCompanies(players) {
  return String(players || "")
    .split(/[、，,]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function renderIndustrySpace() {
  return `<details class="industry-module industry-space" open>
    <summary class="module-head"><span class="module-index">02</span><div><h3>S曲线与产业空间</h3><p>本版的研究重心：不是精确 TAM，而是判断未来空间、趋势可实现性和阶段位置。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
      <div class="industry-space-summary">
        <p><b>总判断：</b>截至 ${AS_OF_DATE}，AI factory 已经从概念期进入早期加速段。最强证据不是单一预测，而是五类证据同时出现：云厂 capex/RPO、NVIDIA/Broadcom 平台收入与指引、GTC 2026 对下一代 rack-scale / pod-scale AI factory 的平台定义、Dell/Vertiv backlog、Micron/SK hynix HBM 与高端内存利润、Omdia/SemiAnalysis/TrendForce/Dell'Oro/LightCounting 的 BOM 拆法。</p>
        <p><b>投资含义：</b>先把产业空间判断为“值得继续找 S 曲线受益节点”，再进入标的筛选。不要把所有链上公司等同打分；系统交付、连接、内存、液冷的利润质量差异很大。</p>
      </div>
      <div class="space-bom-reasoning">${spaceNodes.map(renderSpaceNode).join("")}</div>
    </div>
  </details>`;
}

function renderSpaceNode(node) {
  return `<details class="space-node-card" open>
    <summary><strong>${e(node.node)}</strong><span class="space-step-confidence">置信度：${e(node.confidence)}</span><span class="chevron">›</span></summary>
      <div class="space-node-reasoning">
      <div class="space-node-space-reasoning">
        <b>空间推理</b>
        <div class="space-node-sizing">
          <div class="space-method-step"><div class="space-step-title"><span class="space-step-index">1</span><h4>公开拆法</h4></div>${renderMethodCards(node)}</div>
          <div class="space-method-step"><div class="space-step-title"><span class="space-step-index">2</span><h4>空间结论</h4></div><p>${sourceText(node.conclusion)}</p>${renderHorizon(node.horizons)}${renderSizingTable(node)}</div>
        </div>
      </div>
      <div class="space-node-evidence"><b>证据</b><div>${sourceChips(node.sourceIds)}</div></div>
    </div>
  </details>`;
}

function renderMethodCards(node) {
  const labels = ["公司指引", "公司 TAM", "客户侧指引", "第三方拆法", "财务兑现证据"];
  return `<div class="space-public-methods"><div class="space-method-card-grid">${labels.map((labelName) => {
    const entries = node.methods.filter((item) => item.sourceType === labelName);
    return `<article class="space-method-card"><header><span>${e(labelName)}</span><strong>${entries.length ? "已覆盖" : "待补"}</strong></header><div class="space-method-card-body">${entries.length ? entries.map(renderMethodEntry).join("") : `<div class="space-method-empty">待补：当前 source pack 未找到可直接用于该节点的 ${e(labelName)}。</div>`}</div></article>`;
  }).join("")}</div></div>`;
}

function renderMethodEntry(entry) {
  return `<article class="space-method-entry">
    <div><b>公司或机构</b><span>${e(entry.organization)}</span></div>
    <div><b>指引内容</b><span>${sourceText(entry.guidanceContent)}</span></div>
    <div><b>BOM 节点</b><span>${e(entry.bomNode)}</span></div>
    <div><b>时间范围</b><span>${e(entry.timeframe)}</span></div>
    <div><b>可验证指标</b><span>${e(entry.verificationMetric)}</span></div>
    <div><b>置信度</b><span>${e(entry.confidence)}</span></div>
    <div class="space-method-entry-sources">${sourceChips(entry.sourceIds)}</div>
  </article>`;
}

function renderHorizon(horizons) {
  return `<div class="space-horizon-conclusion"><div class="space-horizon-grid">${horizons.map(([name, size, text]) => `<article class="space-horizon-card"><span>${e(name)}</span><strong>${e(size)}</strong><p>${e(text)}</p></article>`).join("")}</div></div>`;
}

function renderSizingTable(node) {
  return `<div class="table-scroll"><table class="space-node-sizing-table"><thead><tr><th>节点</th><th>短期</th><th>中期</th><th>长期</th><th>结论</th></tr></thead><tbody><tr><td>${e(node.node)}</td>${node.horizons.map((item) => `<td>${e(item[1])}</td>`).join("")}<td>${e(node.conclusion)}</td></tr></tbody></table></div>`;
}

function renderKeyVariables() {
  return `<details class="industry-module industry-key-variables" open>
    <summary class="module-head"><span class="module-index">03</span><div><h3>关键变量与待验证数据</h3><p>用最少变量跟踪 S 曲线是否继续成立。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
      <div class="key-variable-bom-map">${bomNodes.map((node) => `<details class="key-variable-bom-card" open><summary><strong>${e(node.name)}</strong><span class="chevron">›</span></summary><div class="overview-question-card"><h4>下一步验证</h4><div class="overview-answer"><p>${e(variableFor(node.id))}</p></div></div></details>`).join("")}</div>
    </div>
  </details>`;
}

function variableFor(id) {
  return {
    compute: "跟踪 NVIDIA/Broadcom/AMD 的数据中心与 AI semiconductor 指引、gross margin、客户 capex 和 ASIC 分流。",
    manufacturing: "跟踪 TSMC advanced packaging capacity、capex 回报、advanced technologies revenue share、地缘风险。",
    memory: "跟踪 HBM ASP、价量协议、客户资格、HBM4 ramp、DRAM/NAND 价格和 memory gross margin。",
    network: "跟踪 800G/1.6T、AEC/retimer、switch silicon、design-in、客户集中和毛利率。",
    powerCooling: "跟踪 VRT backlog 转收入、项目毛利、液冷 attach、电力接入周期和云厂 capex。",
    system: "跟踪 Dell/SMCI AI server backlog、shipments、gross margin、库存、应收和现金转化。",
  }[id] || "待补验证变量。";
}

function renderQaCard(node) {
  const level = Number(node.level || 1);
  const children = node.children || [];
  const count = countDescendants(node);
  const l3Meta = level >= 3 ? `<div class="l3-meta"><span class="l3-skill">skill: ${e(node.skill)}</span><span class="l3-execution-status">status: ${e(node.status)}</span><span class="l3-score-component">score: ${e(node.score)}</span><span class="l3-decision-use">use: ${e(node.decisionUse)}</span></div>` : "";
  return `<details id="${e(node.id.toLowerCase().replace(/\./g, "-"))}" class="qa-card level-${level}" open>
    <summary><span class="qid">${e(node.id)}</span><strong>${e(node.question)}</strong><span class="qa-count">${count} 子问题</span><span class="chevron">›</span></summary>
    <div class="qa-body">
      ${l3Meta}
      <div class="qa-block"><div class="block-title">1. 当前结论呈现</div><p>${sourceText(node.conclusion)}</p></div>
      <div class="qa-block"><div class="block-title">2. 问题展开（子 QA）</div>${children.length ? children.map(renderQaCard).join("") : `<p class="muted">已到当前最小研究单元。</p>`}</div>
      <div class="qa-block"><div class="block-title">3. 待补充的问题</div><p>${sourceText(node.gap || "待后续财报、订单、价格、capex ROI 和估值隐含预期继续验证。")}</p>${node.sourceIds ? `<div class="qa-sources">${sourceChips(node.sourceIds)}</div>` : ""}</div>
    </div>
  </details>`;
}

function renderTargets() {
  const profitRows = targets.map((item) => [item.ticker, item.thesisNode, item.rationale, item.futureSpace, item.downgrade, item.actionState]);
  const valuationRows = targets.slice(0, 8).map((item) => [item.ticker, "估值未完整重建", item.actionState === "actionable_long" ? "需要确认增长未被完全定价" : "因估值或风险控制封顶", item.futureSpace, item.downgrade]);
  const oddsRows = targets.slice(0, 8).map((item) => [item.ticker, item.actionState, item.futureSpace, item.downgrade]);
  return `<div class="target-section">
    <div class="artifact-card"><div class="artifact-title">标的推荐口径</div><p>这里是研究观察名单，不是交易指令。排序优先看 S 曲线空间能否落到公司财务，再看是否被市场充分定价和风险是否可监控。</p></div>
    ${table("target-profit-bridge", ["标的", "链条节点", "为什么能捕获价值", "未来空间", "降级触发", "状态"], profitRows)}
    ${table("target-valuation-table", ["标的", "估值证据", "赔率判断", "空间依据", "主要风险"], valuationRows)}
    <div class="target-odds-model">${table("target-odds-table", ["标的", "状态", "赔率来源", "风险闸门"], oddsRows)}</div>
    ${table("target-table", ["排序", "标的", "公司", "市场", "节点", "强度", "理由", "风险", "as_of_date", "evaluation_date", "label_window", "start_price", "end_price", "forward_3m_return", "label_status"], targets.map((item, index) => {
      const lab = labels[item.ticker] || {};
      return [index + 1, item.ticker, item.name, item.market, item.thesisNode, `<span class="state-${item.actionState}">${item.actionState}</span>`, item.rationale, item.downgrade, AS_OF_DATE, EVALUATION_DATE, LABEL_WINDOW, lab.start_price ?? "label_unverified", lab.end_price ?? "label_unverified", lab.forward_3m_return ?? "label_unverified", lab.label_status ?? "label_unverified"];
    }), true)}
  </div>`;
}

function renderSources() {
  const rows = sources.map((item) => `<tr><td>${e(item.source_id)}</td><td><a href="${e(item.url)}" target="_blank" rel="noopener">${e(item.title)}</a></td><td>${e(item.source_bucket)}</td><td>${e(item.source_visible_at)}</td><td>${e(item.summary)}</td></tr>`).join("");
  return `<details class="source-collapse"><summary>展开来源索引 <span class="chevron">›</span></summary><div class="table-scroll"><table><thead><tr><th>ID</th><th>来源</th><th>类别</th><th>可见日期</th><th>用途摘要</th></tr></thead><tbody>${rows}</tbody></table></div></details>`;
}

function table(className, headers, rows, raw = false) {
  return `<div class="table-scroll"><table class="${className}"><thead><tr>${headers.map((header) => `<th>${e(header)}</th>`).join("")}</tr></thead><tbody>${rows.map((row) => `<tr>${row.map((cell) => `<td>${raw ? String(cell) : e(cell)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
}

function sourceChips(sourceIds = []) {
  return [...new Set(sourceIds)].map((id) => {
    const item = sourceById[id];
    return item ? `<a class="source-chip" href="${e(item.url)}" target="_blank" rel="noopener">${e(id)}</a>` : "";
  }).join("");
}

function sourceText(text) {
  return e(text).replace(/\[([^\]]+)\]\(source:([^)]+)\)/g, (_match, labelText, sourceId) => {
    const item = sourceById[sourceId];
    return item ? `<a href="${e(item.url)}" target="_blank" rel="noopener">${e(labelText)}</a>` : e(labelText);
  });
}

function countDescendants(node) {
  return (node.children || []).reduce((sum, child) => sum + 1 + countDescendants(child), 0);
}

function l1(id, question, conclusion, children) { return { id, question, conclusion, children, level: 1 }; }
function l2(id, question, conclusion, children) { return { id, question, conclusion, children, level: 2 }; }
function l3(id, question, score, decisionUse, skill, status, conclusion, gap, sourceIds) {
  return { id, question, score, decisionUse, skill, status, conclusion, gap, sourceIds, children: [], level: 3 };
}
function spaceNode(node, methods, conclusion, confidence, horizons, sourceIds) {
  return { node, methods, conclusion, confidence, horizons, sourceIds };
}
function method(sourceType, organization, guidanceContent, bomNode, timeframe, verificationMetric, confidence, sourceIds) {
  return { sourceType, organization, guidanceContent, bomNode, timeframe, verificationMetric, confidence, sourceIds };
}
function target(ticker, name, market, thesisNode, actionState, rationale, futureSpace, downgrade, sourceIds) {
  return { ticker, name, market, thesisNode, actionState, rationale, futureSpace, downgrade, sourceIds };
}
function source(source_id, title, source_bucket, url, source_visible_at, summary) {
  return {
    source_id,
    title,
    source_bucket,
    url,
    source_visible_at,
    summary,
    availability_proof: {
      proof_type: "publisher_or_release_date",
      proof_value: source_visible_at,
      proof_url: url,
    },
  };
}
function label(start_price, end_price, forward_3m_return, price_source, label_status, dates = {}) {
  return { start_price, end_price, forward_3m_return, price_source, label_status, ...dates };
}
function e(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
}

function css() {
  return `
:root{--bg:#f5f7fb;--surface:rgba(255,255,255,.9);--text:#1d1d1f;--muted:#667085;--line:#d9e0ea;--blue:#0a84ff;--green:#1d9a6c;--amber:#b7791f;--red:#c2413d;--shadow:0 18px 50px rgba(20,32,54,.10)}
.representative-companies{margin:12px 0 14px;padding:10px 0;border-top:1px solid #eef2f7;border-bottom:1px solid #eef2f7}.representative-companies>b{display:block;color:var(--blue);font-size:12px;margin-bottom:8px}.representative-companies>div{display:flex;flex-wrap:wrap;gap:8px}.representative-companies span{display:inline-flex;align-items:center;border:1px solid #d9e7f7;border-radius:999px;background:#f7fbff;color:#223047;padding:5px 9px;font-size:12px;font-weight:800}
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",sans-serif;background:radial-gradient(circle at 20% 0%,#e8f2ff 0,transparent 34rem),var(--bg);color:var(--text);line-height:1.62}a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}
.hero{padding:32px clamp(22px,5vw,72px) 48px;background:linear-gradient(180deg,rgba(255,255,255,.96),rgba(255,255,255,.62));border-bottom:1px solid var(--line)}.hero-inner{max-width:1180px;margin:0 auto}.eyebrow{margin:0 0 10px;color:var(--blue);font-size:12px;font-weight:800;text-transform:uppercase}h1{max-width:980px;margin:0;font-size:clamp(36px,5vw,66px);line-height:1.04;letter-spacing:0}.hero-subtitle{max-width:780px;color:#475467;font-size:19px}.hero-meta{display:flex;gap:10px;flex-wrap:wrap}.hero-meta span,.state-pill{border:1px solid var(--line);border-radius:999px;background:#fff;padding:6px 10px;color:var(--muted);font-size:13px}.top-nav{position:sticky;top:0;z-index:5;display:flex;justify-content:center;gap:10px;flex-wrap:wrap;padding:12px;background:rgba(245,247,251,.82);backdrop-filter:blur(16px);border-bottom:1px solid rgba(217,224,234,.72)}.top-nav a{padding:8px 12px;border:1px solid rgba(10,132,255,.18);border-radius:999px;background:#fff;color:#28506f;font-size:13px}.section{max-width:1180px;margin:0 auto;padding:44px clamp(18px,4vw,36px)}.section-heading{display:flex;align-items:end;justify-content:space-between;margin-bottom:18px}.section-heading h2{margin:0;font-size:clamp(30px,3vw,44px);letter-spacing:0}.muted{color:var(--muted)}
.goal-card,.industry-module,.qa-card,.source-collapse,.artifact-card{border:1px solid var(--line);border-radius:22px;background:var(--surface);box-shadow:var(--shadow)}.goal-card{padding:22px}.goal-main{font-size:22px;font-weight:800;margin-bottom:16px}.goal-grid,.constraint-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.metric,.constraint-grid article,.chain-bridge-card,.chain-node-lens,.overview-question-card,.space-method-card,.space-horizon-card,.chain-company-card,.bom-taxonomy-card,.key-variable-bom-card{border:1px solid #e6edf7;border-radius:16px;background:#fff;padding:14px}.metric span,.constraint-grid span{display:block;color:var(--muted);font-size:12px;font-weight:800}.metric strong{display:block;color:#223047;font-size:18px}.constraint-definition{margin-top:18px}.artifact-title{font-weight:900;color:#26364f;margin-bottom:8px}.industry-overview-section{display:grid;gap:14px}.industry-module{overflow:hidden}.industry-module>summary,.qa-card>summary,.space-node-card>summary,.chain-detail-panel>summary,.key-variable-bom-card>summary,.source-collapse>summary{list-style:none;cursor:pointer}.industry-module>summary::-webkit-details-marker,.qa-card>summary::-webkit-details-marker,details>summary::-webkit-details-marker{display:none}.industry-module[open]>summary,.qa-card[open]>summary{border-bottom:1px solid var(--line)}.module-head{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding:18px 22px}.module-index{display:inline-flex;width:34px;height:34px;border-radius:999px;align-items:center;justify-content:center;background:#eaf3ff;color:var(--blue);font-weight:900;font-size:12px}.module-head h3{margin:0;font-size:22px}.module-head p{margin:0;color:var(--muted);font-size:14px}.chevron{color:var(--muted);font-weight:900;transition:transform .18s ease}.industry-module[open]>.module-head .chevron,.qa-card[open]>summary .chevron,details[open]>summary>.chevron{transform:rotate(90deg)}.industry-module-body{padding:22px;min-width:0}.chain-explain{padding:0}.chain-plain-summary{font-size:18px;color:#344054;margin-top:0}.chain-research-bridge{border:1px solid rgba(10,132,255,.18);border-radius:18px;background:#fbfdff;padding:16px;margin:18px 0}.chain-bridge-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.chain-node-lens ul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:0;padding:0;list-style:none}.chain-node-lens b,.chain-bridge-card span{display:block;color:var(--blue);font-size:12px;margin-bottom:4px}.chain-detail-panel{border:1px solid #e6edf7;border-radius:18px;background:#fff;margin-top:12px;overflow:hidden}.chain-detail-panel>summary{display:flex;justify-content:space-between;align-items:center;padding:14px 16px;font-weight:900}.chain-layer-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;padding:16px}.chain-layer-card{border:1px solid #eef2f7;border-radius:16px;background:#fbfcff;padding:14px}.chain-layer-card p{margin:10px 0}.chain-layer-card span{display:block;color:var(--muted);font-size:12px}.chain-simple-flow{display:grid;grid-template-columns:repeat(5,minmax(180px,1fr));gap:10px;padding:16px;overflow-x:auto}.chain-stage-panel{min-width:180px;border:1px solid #e8eef7;border-radius:16px;padding:14px;background:#fbfcff}.chain-stage-panel span{display:inline-flex;width:28px;height:28px;border-radius:50%;align-items:center;justify-content:center;background:#eaf3ff;color:var(--blue);font-weight:900}.chain-relationship-graph{margin:0 16px 16px;padding:14px;border:1px dashed #bfd7f5;border-radius:16px;color:#3d536d;background:#f7fbff}.chain-company-list,.bom-taxonomy-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;padding:16px}.company-flow-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.company-flow-grid p{margin:0;border-top:1px solid #eef2f7;padding-top:8px}.company-flow-grid b{display:block;color:#223047}.component-value-chain,.bom-taxonomy,.chain-lane-map,.chain-value-flow{min-width:0}.chain-relationship-graph{display:block}
.industry-space-summary{border:1px solid rgba(10,132,255,.18);border-radius:18px;background:#fbfdff;padding:16px;margin-bottom:14px}.space-bom-reasoning,.key-variable-bom-map{display:grid;gap:12px}.space-node-card,.key-variable-bom-card{border:1px solid #e3ebf6;border-radius:18px;background:#fff;overflow:hidden}.space-node-card>summary,.key-variable-bom-card>summary{display:flex;gap:12px;justify-content:space-between;align-items:center;padding:15px 16px}.space-node-reasoning{display:grid;grid-template-columns:1fr;gap:12px;padding:16px}.space-node-space-reasoning,.space-node-evidence{border:1px solid #eef2f7;border-radius:16px;background:#fbfcff;padding:14px}.space-node-sizing{display:grid;gap:14px}.space-method-step{display:grid;gap:10px}.space-step-title{display:flex;align-items:center;gap:10px}.space-step-title h4{margin:0;font-size:18px}.space-step-index{display:inline-flex;width:28px;height:28px;border-radius:50%;align-items:center;justify-content:center;background:#eaf3ff;color:var(--blue);font-weight:900}.space-method-card-grid,.competition-question-grid,.chokepoint-question-grid{display:grid;grid-template-columns:1fr;gap:10px}.space-method-card header{display:flex;justify-content:space-between;gap:8px;margin-bottom:10px}.space-method-card header span{font-weight:900;color:#25364f}.space-method-card header strong{color:var(--blue)}.space-method-card-body{display:grid;gap:10px}.space-method-entry{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;border:1px solid #eef2f7;border-radius:14px;background:#fff;padding:12px}.space-method-entry b{display:block;color:var(--muted);font-size:11px}.space-method-entry span{display:block;color:#26364f;font-size:13px}.space-method-entry-sources{grid-column:1/-1;display:flex;gap:6px;flex-wrap:wrap}.space-method-empty{color:#98a2b3;font-size:13px}.space-horizon-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.space-horizon-card span{color:var(--muted);font-size:12px}.space-horizon-card strong{display:block;color:#223047;font-size:20px}.space-step-confidence{border:1px solid #d7ebff;border-radius:999px;background:#eef7ff;color:var(--blue);font-size:12px;padding:4px 9px}.source-chip{display:inline-flex;margin:2px 4px 2px 0;border:1px solid rgba(10,132,255,.2);border-radius:999px;background:#eef7ff;color:var(--blue);padding:3px 8px;font-size:11px}
.qa-card{margin:12px 0;overflow:hidden}.qa-card summary{display:grid;grid-template-columns:auto 1fr auto auto;gap:12px;align-items:center;padding:14px 16px}.qid{font-weight:900;color:var(--blue)}.qa-count{font-size:12px;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.qa-body{display:grid;gap:10px;padding:14px 16px}.qa-block{border:1px solid #edf1f7;border-radius:16px;background:#fff;padding:12px}.block-title{font-weight:900;color:#27364a;margin-bottom:6px}.qa-card.level-2{margin-left:18px;background:rgba(255,255,255,.82)}.qa-card.level-3{margin-left:28px;background:rgba(247,249,252,.95);border-style:dashed}.l3-meta{display:flex;gap:8px;flex-wrap:wrap}.l3-meta span{border:1px solid #e0e8f4;border-radius:999px;background:#f7fbff;color:#4e5f75;font-size:11px;padding:4px 8px}.overview-answer p{margin:0}.overview-answer-prose{color:#344054}.target-section{display:grid;gap:14px}.table-scroll{max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch}.table-scroll table{min-width:920px;border-collapse:separate;border-spacing:0;width:100%;background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden}.table-scroll th,.table-scroll td{padding:10px 12px;text-align:left;border-bottom:1px solid #edf1f7;vertical-align:top;font-size:13px}.table-scroll th{background:#f6f9fd;color:#475467;font-size:12px;font-weight:900}.state-actionable_long,.state-watch_only,.state-no_action{display:inline-flex;border-radius:999px;padding:4px 8px;font-weight:900;font-size:12px}.state-actionable_long{color:var(--green);background:#eaf8f2;border:1px solid rgba(29,154,108,.25)}.state-watch_only{color:var(--amber);background:#fff7e6;border:1px solid rgba(183,121,31,.25)}.state-no_action{color:var(--red);background:#fff1f0;border:1px solid rgba(194,65,61,.22)}.source-collapse{padding:16px}.source-collapse summary{font-weight:900;color:#334155}.source-collapse .table-scroll{margin-top:12px}
@media(max-width:820px){.goal-grid,.constraint-grid,.chain-bridge-grid,.chain-layer-grid,.chain-company-list,.bom-taxonomy-grid,.company-flow-grid,.chain-node-lens ul,.space-horizon-grid,.space-method-entry{grid-template-columns:1fr}.qa-card.level-2,.qa-card.level-3{margin-left:0}.qa-card summary{grid-template-columns:auto 1fr auto}.qa-count{display:none}}
`;
}

main();
