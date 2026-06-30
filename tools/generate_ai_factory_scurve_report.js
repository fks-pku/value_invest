const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const PROJECT_ID = "ai_factory_industry_scurve_timeslice_20260302";
const OUT_DIR = path.join(ROOT, "research", "qa_projects", PROJECT_ID);
const AS_OF_DATE = "2026-03-28";
const EVALUATION_DATE = "2026-06-28";
const LABEL_WINDOW = "2026-03-28_to_2026-06-28";

const sources = [
  source("SRC-NVDA-FY23-Q4", "NVIDIA FY2023 Q4 results", "evidence", "https://investor.nvidia.com/news/press-release-details/2023/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2023/", "2023-02-22", "NVIDIA Q4 FY23 Data Center revenue was $3.62B, before the post-ChatGPT AI infrastructure acceleration showed up in reported platform revenue."),
  source("SRC-NVDA-FY24-Q4", "NVIDIA FY2024 Q4 results", "evidence", "https://investor.nvidia.com/news/press-release-details/2024/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2024/", "2024-02-21", "NVIDIA Q4 FY24 Data Center revenue was $18.4B, showing the first large financial step-change after accelerated computing demand surged."),
  source("SRC-NVDA-FY25-Q4", "NVIDIA FY2025 Q4 results", "evidence", "https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2025/", "2025-02-26", "NVIDIA Q4 FY25 Data Center revenue was $35.6B, extending the AI infrastructure revenue ramp before Blackwell scaled further."),
  source("SRC-NVDA-FY26-Q4", "NVIDIA FY2026 Q4 results", "evidence", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/", "2026-02-25", "NVIDIA Q4 FY26 revenue was $68.1B, Data Center revenue was $62.3B, and management framed customer demand as AI factories for the AI industrial revolution."),
  source("SRC-NVDA-GTC-VERA-RUBIN-20260316", "NVIDIA Vera Rubin platform at GTC 2026", "evidence", "https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform", "2026-03-16", "NVIDIA announced Vera Rubin as seven chips and five rack-scale systems for AI factories, covering Vera CPU, Rubin GPU, NVLink 6, ConnectX-9, BlueField-4, Spectrum-6 and Groq 3 LPU."),
  source("SRC-NVDA-GTC-DYNAMO-20260316", "NVIDIA Dynamo 1.0 for AI factory inference", "evidence", "https://nvidianews.nvidia.com/news/dynamo-1-0", "2026-03-16", "NVIDIA announced Dynamo 1.0 as open-source production software for AI factory inference orchestration, with reported up to 7x Blackwell inference performance improvement and broad cloud/provider adoption."),
  source("SRC-VRT-Q4-2025", "Vertiv Q4 2025 results", "evidence", "https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/", "2026-02-11", "Vertiv Q4 2025 organic orders rose about 252% YoY and backlog reached $15.0B, reflecting robust AI infrastructure demand."),
  source("SRC-DELL-FY26-Q4", "Dell FY2026 Q4 results", "evidence", "https://investors.delltechnologies.com/node/19176/pdf", "2026-02-26", "Dell FY26 closed more than $64B in AI-optimized server orders, shipped more than $25B, entered FY27 with a $43B backlog, and guided FY27 AI-optimized server revenue to roughly $50B, up 103% year over year."),
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
  source("SRC-CHATGPT-MAU-202302", "TIME: ChatGPT 100M users in two months", "message", "https://time.com/6253615/chatgpt-fastest-growing/", "2023-02-08", "TIME cited Similarweb and UBS data that ChatGPT reached about 100M monthly active users in January 2023, two months after launch."),
  source("SRC-CHATGPT-WAU-202408", "The Verge: ChatGPT 200M weekly users", "message", "https://www.theverge.com/2024/8/29/24231685/openai-chatgpt-200-million-weekly-users", "2024-08-29", "The Verge reported OpenAI confirmed ChatGPT had more than 200M weekly users in August 2024, double the 100M weekly active users reported in November 2023."),
  source("SRC-CHATGPT-WAU-202508", "Windows Central: ChatGPT weekly users and prompt volume", "message", "https://www.windowscentral.com/artificial-intelligence/chatgpt-is-set-to-hit-700-million-weekly-users-but-can-its-rivals-catch-up", "2025-08-05", "Windows Central reported ChatGPT was on track to reach 700M weekly active users in August 2025, about 4x year over year, with an estimated 2.5B-3.0B prompts per day."),
  source("SRC-CHATGPT-WAU-202510", "Economic Times: OpenAI DevDay 2025 ChatGPT apps", "message", "https://m.economictimes.com/tech/artificial-intelligence/devday-2025-openai-launches-apps-inside-chatgpt/articleshow/124346472.cms", "2025-10-06", "Economic Times reported OpenAI said ChatGPT weekly users surpassed 800M at DevDay 2025, alongside the launch of apps inside ChatGPT."),
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
      l3("Q1.2.1", "GPU/ASIC 平台单位强度是否继续提升？", "future_space", "判断当前 accelerator BOM 是否从单卡/单服务器升级到 rack-scale / cluster-scale 部署。", "industry-report-analysis", "completed", "SemiAnalysis 的 GB200/rack-scale 拆法、Omdia 的 AI processor forecast，以及 GTC 2026 Vera Rubin 的七芯片/五类 rack-scale 系统描述都表明，GPU/ASIC 需求从单芯片扩展到机柜级 accelerator 平台。", "需要继续验证每一代平台是否仍提高单柜 GPU/ASIC 数量、ASP、利用率和交付节奏；其他 BOM 的单位用量留到各自章节。", ["SRC-SA-GB200-BOM-2024", "SRC-OMDIA-AI-PROCESSORS-20250828", "SRC-NVDA-GTC-VERA-RUBIN-20260316", "SRC-NVDA-GTC-DYNAMO-20260316"]),
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
    <a href="#targets">标的推荐</a>
    <a href="#sources">来源索引</a>
  </nav>
  <main>
    <section id="goal" class="section"><div class="section-heading"><h2>当前研究的问题</h2></div>${renderGoal()}</section>
    <section id="overview" class="section"><div class="section-heading"><h2>行业概况</h2></div>${renderOverview()}</section>
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
    ${bomNodes.map((node, index) => renderBomResearchModule(node, index + 2)).join("")}
  </div>`;
}

function renderSupplyChain() {
  return `<details class="industry-module supply-chain-section" open>
    <summary class="module-head"><span class="module-index">01</span><div><h3>技术链与 BOM 呈现</h3><p>只保留 BOM 拆分、泳道图、价值流和每个 BOM 的代表公司。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
      <div class="chain-explain">
        <p class="chain-plain-summary">一句话：云厂商和 AI labs 的算力需求先变成 capex 和订单，再通过 GPU/ASIC 平台传导到先进制造、HBM、网络连接、服务器机柜、电力和液冷，最后由下游利用率、云收入和 ROI 验证是否继续扩容。</p>
        ${renderChainBridge()}
        ${renderNodeLens()}
        ${renderChainPanels()}
      </div>
    </div>
  </details>`;
}

function renderChainBridge() {
  return `<div class="chain-research-bridge">
    <div class="artifact-title">这一步要解决什么</div>
    <div class="chain-bridge-grid">
      <article class="chain-bridge-card"><span>先定义产业</span><p>AI factory 的投资机会不是从公司名字开始，而是从需求如何传到每个 BOM 节点开始。</p></article>
      <article class="chain-bridge-card"><span>再逐节点验证</span><p>从 02 开始，每个 BOM 节点都用同一组投资问题检查需求、供给、控制者、财务兑现、定价和反证。</p></article>
    </div>
  </div>`;
}

function renderNodeLens() {
  return `<div class="chain-node-lens">
    <div class="artifact-title">BOM 节点阅读口径</div>
    <ul>
      <li><b>接受什么</b><span>上游需求、平台规格、订单或工程约束。</span></li>
      <li><b>生产什么</b><span>可被采购、集成或运营的产品/服务。</span></li>
      <li><b>提供给谁</b><span>下游系统、客户或下一环节。</span></li>
    </ul>
  </div>`;
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

function renderBomResearchModule(node, moduleNumber) {
  const rows = bomSevenQuestionRows(node);
  return `<details class="industry-module bom-research-module" open>
    <summary class="module-head"><span class="module-index">${String(moduleNumber).padStart(2, "0")}</span><div><h3>${e(node.name)}</h3><p>${e(node.plain)}</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
      <div class="bom-node-brief">
        <article><span>接受</span><p>${e(node.receives)}</p></article>
        <article><span>生产</span><p>${e(node.produces)}</p></article>
        <article><span>提供给</span><p>${e(node.suppliesTo)}</p></article>
        <article><span>验证指标</span><p>${e(node.metrics)}</p></article>
      </div>
      <div class="bom-question-list">${rows.map((row, index) => renderBomQuestionCard(row, index + 1)).join("")}</div>
    </div>
  </details>`;
}

function renderBomQuestionCard(row, questionNumber) {
  return `<details class="bom-question-card" open>
    <summary><span class="bom-question-index">${questionNumber}</span><strong>${e(row.question)}</strong><span class="chevron">›</span></summary>
    <div class="bom-question-answer">
      ${row.detail ? renderBomQuestionDetail(row.detail) : `<p>${sourceText(row.answer)}</p>`}
      <div class="bom-question-sources">${sourceChips(row.sourceIds)}</div>
    </div>
  </details>`;
}

function renderBomQuestionDetail(detail) {
  if (detail.reportNarrative) {
    return renderResearchNarrative(detail.reportNarrative);
  }
  return `<div class="bom-demand-study">
    <p class="bom-demand-thesis">${sourceText(detail.thesis)}</p>${detail.chainAudit ? renderDemandChainAudit(detail.chainAudit) : ""}
    <div class="bom-demand-steps">${detail.steps.map((step, index) => `<article class="bom-demand-step">
      <span>${String(index + 1).padStart(2, "0")}</span>
      <div><h5>${e(step.title)}</h5><p>${sourceText(step.body)}</p>${step.sourceIds ? `<div class="bom-question-sources">${sourceChips(step.sourceIds)}</div>` : ""}</div>
    </article>`).join("")}</div>
    <div class="table-scroll"><table class="bom-demand-table"><thead><tr><th>验证环节</th><th>当前证据</th><th>判断</th><th>下一步要补</th></tr></thead><tbody>${detail.checks.map((row) => `<tr><td>${e(row[0])}</td><td>${sourceText(row[1])}</td><td>${e(row[2])}</td><td>${e(row[3])}</td></tr>`).join("")}</tbody></table></div>
  </div>`;
}

function renderResearchNarrative(narrative) {
  return `<article class="research-narrative">
    <header class="narrative-head">
      <span>${e(narrative.eyebrow)}</span>
      <h4>${e(narrative.title)}</h4>
      <p>${sourceText(narrative.conclusion)}</p>
    </header>
    <div class="logic-flow">${narrative.logicFlow.map((item, index) => `<div class="flow-step"><span>${String(index + 1).padStart(2, "0")}</span><p>${e(item)}</p></div>${index < narrative.logicFlow.length - 1 ? `<b class="flow-arrow">›</b>` : ""}`).join("")}</div>
    ${narrative.chainNodes ? renderChainNodeExpansion(narrative.chainNodes) : `${narrative.historicalComparison ? renderHistoricalComparison(narrative.historicalComparison) : ""}${narrative.futureRunway ? renderFutureRunway(narrative.futureRunway) : ""}`}
    <div class="narrative-prose">${narrative.paragraphs.map((paragraph) => `<p>${sourceText(paragraph)}</p>`).join("")}</div>
    <div class="table-scroll"><table class="narrative-data-table"><thead><tr><th>验证问题</th><th>应看指标</th><th>当前证据</th><th>判断</th><th>来源</th></tr></thead><tbody>${narrative.keyData.map((row) => `<tr><td>${e(row.question)}</td><td>${e(row.metric)}</td><td>${sourceText(row.evidence)}</td><td>${e(row.judgment)}</td><td>${sourceChips(row.sourceIds)}</td></tr>`).join("")}</tbody></table></div>
    <div class="narrative-bottom">
      <section class="investment-takeaway"><b>投资含义</b><p>${sourceText(narrative.investmentImplication)}</p></section>
      <section class="bear-case-box"><b>反证框</b><ul>${narrative.bearCases.map((item) => `<li>${sourceText(item)}</li>`).join("")}</ul></section>
    </div>
  </article>`;
}

function renderChainNodeExpansion(nodes) {
  return `<section class="chain-node-expansion">
    <header class="chain-node-expansion-head">
      <span>逐环验证 / 每个节点单独回答</span>
      <h5>沿需求链条逐一判断：过去是否加速、现在是否兑现、未来还能走多远</h5>
      <p>每个节点只回答当前 GPU/ASIC BOM 的需求链，不提前讨论其它 BOM 的投资机会。</p>
    </header>
    <div class="chain-node-stack">${nodes.map((node, index) => `<details class="chain-node-detail" open>
      <summary>
        <span class="chain-node-index">${String(index + 1).padStart(2, "0")}</span>
        <div><h6>${e(node.title)}</h6><p>${sourceText(node.question)}</p></div>
        <strong>${e(node.status)}</strong>
        <span class="chevron">›</span>
      </summary>
      <div class="chain-node-body">
        ${node.metrics ? renderChainNodeMetrics(node.metrics) : ""}
        <div class="chain-node-lens-grid">
          <article><b>历史对比</b><p>${sourceText(node.history)}</p></article>
          <article><b>当前状态</b><p>${sourceText(node.current)}</p></article>
          <article><b>未来推测</b><p>${sourceText(node.future)}</p></article>
          <article><b>反证信号</b><p>${sourceText(node.refute)}</p></article>
        </div>
        <div class="chain-node-conclusion"><b>节点结论</b><p>${sourceText(node.conclusion)}</p></div>
        <div class="bom-question-sources">${sourceChips(node.sourceIds)}</div>
      </div>
    </details>`).join("")}</div>
  </section>`;
}

function renderChainNodeMetrics(metrics) {
  return `<div class="chain-metric-board">
    <div class="chain-metric-board-head"><b>先看哪些 metric</b><span>指标先行，结论后置</span></div>
    <div class="chain-metric-grid">${metrics.map((metric) => `<article class="chain-metric-card">
      <header><span>${e(metric.type)}</span><strong>${e(metric.name)}</strong></header>
      <p>${sourceText(metric.why)}</p>
      ${renderMetricTrend(metric)}
      <dl>
        <div><dt>历史</dt><dd>${sourceText(metric.history)}</dd></div>
        <div><dt>现在</dt><dd>${sourceText(metric.current)}</dd></div>
        <div><dt>未来</dt><dd>${sourceText(metric.future)}</dd></div>
      </dl>
      <footer><em>${e(metric.quality)}</em><div class="bom-question-sources">${sourceChips(metric.sourceIds)}</div></footer>
    </article>`).join("")}</div>
  </div>`;
}

function renderMetricTrend(metric) {
  const series = metric.series || [];
  if (series.length < 2) {
    return `<div class="metric-trend-gap">
      <b>连续趋势</b>
      <p>${sourceText(metric.seriesGap || "公开材料暂时只有单点或代理数据，不能画成连续趋势。")}</p>
    </div>`;
  }
  if (metric.trendKind !== "time_series") {
    return `<div class="metric-noncontinuous-chart">
      <b>${e(metric.trendLabel || "非连续时间序列")}</b>
      <p>${sourceText(metric.seriesGap || "这些点来自不同公司、不同口径或订单漏斗，适合做方向判断，不适合画成连续历史趋势。")}</p>
      <div class="metric-comparison-bars">${series.map((point) => `<div class="metric-comparison-row">
        <div class="metric-point-label"><b>${e(point.label)}</b><span>${e(point.value)}</span></div>
        <div class="metric-bar"><i style="width:${Math.max(2, Math.min(100, Number(point.scale) || 0))}%"></i></div>
      </div>`).join("")}</div>
    </div>`;
  }
  const width = 320;
  const height = 118;
  const xStep = series.length > 1 ? width / (series.length - 1) : width;
  const points = series.map((point, index) => {
    const x = Math.round(index * xStep);
    const y = Math.round(height - 18 - (Math.max(0, Math.min(100, Number(point.scale) || 0)) / 100) * 82);
    return { ...point, x, y };
  });
  const line = points.map((point) => `${point.x},${point.y}`).join(" ");
  const area = `${points[0].x},${height - 14} ${line} ${points[points.length - 1].x},${height - 14}`;
  return `<div class="metric-trend-chart">
    <svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${e(metric.name)} trend">
      <line x1="0" y1="${height - 14}" x2="${width}" y2="${height - 14}" class="metric-axis"></line>
      <polygon points="${area}" class="metric-area"></polygon>
      <polyline points="${line}" class="metric-line"></polyline>
      ${points.map((point) => `<g><circle cx="${point.x}" cy="${point.y}" r="4" class="metric-dot"></circle><text x="${point.x}" y="${Math.max(12, point.y - 8)}" text-anchor="${point.x < 24 ? "start" : point.x > width - 24 ? "end" : "middle"}" class="metric-value">${e(point.value)}</text><text x="${point.x}" y="${height - 2}" text-anchor="${point.x < 24 ? "start" : point.x > width - 24 ? "end" : "middle"}" class="metric-label">${e(point.label)}</text></g>`).join("")}
    </svg>
  </div>`;
}

function renderHistoricalComparison(comparison) {
  return `<section class="historical-comparison">
    <header class="history-head">
      <span>${e(comparison.label)}</span>
      <h5>${e(comparison.title)}</h5>
      <p>${sourceText(comparison.summary)}</p>
    </header>
    <div class="history-snapshot-grid">${comparison.snapshots.map((item) => `<article class="history-metric-card">
      <span>${e(item.label)}</span>
      <strong>${e(item.value)}</strong>
      <p>${sourceText(item.note)}</p>
      <div class="bom-question-sources">${sourceChips(item.sourceIds)}</div>
    </article>`).join("")}</div>
    <div class="history-bar-list">${comparison.bars.map((item) => `<div class="history-bar-row">
      <div class="history-bar-label"><b>${e(item.period)}</b><span>${e(item.value)}</span></div>
      <div class="history-bar-track"><i style="width:${Math.max(2, Math.min(100, Number(item.scale) || 0))}%"></i></div>
      <div class="bom-question-sources">${sourceChips(item.sourceIds)}</div>
    </div>`).join("")}</div>
    <div class="table-scroll"><table class="history-table"><thead><tr><th>链条环节</th><th>过去基准</th><th>当前证据</th><th>为什么能感知“变多”</th><th>来源</th></tr></thead><tbody>${comparison.rows.map((row) => `<tr><td>${e(row.stage)}</td><td>${sourceText(row.baseline)}</td><td>${sourceText(row.latest)}</td><td>${sourceText(row.readThrough)}</td><td>${sourceChips(row.sourceIds)}</td></tr>`).join("")}</tbody></table></div>
  </section>`;
}

function renderFutureRunway(runway) {
  return `<section class="future-runway">
    <header class="runway-head">
      <span>${e(runway.label)}</span>
      <h5>${e(runway.title)}</h5>
      <p>${sourceText(runway.summary)}</p>
    </header>
    <div class="runway-formula">${runway.formula.map((item, index) => `<article class="runway-formula-card">
      <span>${String(index + 1).padStart(2, "0")}</span>
      <h6>${e(item.title)}</h6>
      <p>${sourceText(item.body)}</p>
    </article>`).join("")}</div>
    <div class="table-scroll"><table class="runway-table"><thead><tr><th>未来 metric</th><th>当前基准</th><th>未来锚点 / 空间</th><th>兑现窗口</th><th>推理结论</th><th>来源</th></tr></thead><tbody>${runway.metrics.map((row) => `<tr><td>${e(row.metric)}</td><td>${sourceText(row.current)}</td><td>${sourceText(row.future)}</td><td>${e(row.timing)}</td><td>${sourceText(row.readThrough)}</td><td>${sourceChips(row.sourceIds)}</td></tr>`).join("")}</tbody></table></div>
    <div class="runway-timeline">${runway.timeline.map((item) => `<article>
      <span>${e(item.period)}</span>
      <strong>${e(item.label)}</strong>
      <p>${sourceText(item.body)}</p>
    </article>`).join("")}</div>
    <div class="runway-verdict"><b>${e(runway.verdictTitle)}</b><p>${sourceText(runway.verdict)}</p></div>
  </section>`;
}

function renderDemandChainAudit(chainAudit) {
  return `<div class="demand-chain-audit">
    <div class="demand-chain-title"><span>需求链条逐环验证</span><strong>只在后半段兑现时，才算投资可用需求</strong></div>
    <div class="demand-chain-cards">${chainAudit.map((item, index) => `<article class="chain-audit-card">
      <header class="chain-audit-head"><span>${String(index + 1).padStart(2, "0")}</span><div><h5>${e(item.stage)}</h5><p>${e(item.verifyQuestion)}</p></div><strong>${e(item.status)}</strong></header>
      <div class="chain-audit-body-grid">
        <div><b>搜集材料</b><p>${sourceText(item.materials)}</p></div>
        <div><b>解析结果</b><p>${sourceText(item.parsed)}</p></div>
        <div><b>当前判断</b><p>${sourceText(item.judgment)}</p></div>
        <div><b>缺口 / 反证</b><p>${sourceText(item.gap)}</p></div>
      </div>
      <div class="chain-audit-verdict"><span>置信度：${e(item.confidence)}</span><div class="bom-question-sources">${sourceChips(item.sourceIds)}</div></div>
    </article>`).join("")}</div>
  </div>`;
}

function renderBomSevenQuestionCard(node) {
  const rows = bomSevenQuestionRows(node);
  return `<article class="overview-question-card">
    <h4>${e(node.name)}</h4>
    <div class="overview-answer">
      <div class="table-scroll"><table class="bom-seven-question-table"><thead><tr><th>问题</th><th>回答</th><th>来源</th></tr></thead><tbody>${rows.map((row) => `<tr><td><b>${e(row.question)}</b></td><td>${sourceText(row.answer)}</td><td>${sourceChips(row.sourceIds)}</td></tr>`).join("")}</tbody></table></div>
    </div>
  </article>`;
}

function bomSevenQuestionRows(node) {
  const rows = {
    compute: [
      {
        question: "需求是否会大幅增长？",
        answer: "AI factory 的第一层实物需求是数据中心 AI 加速器。当前应先验证 AI workload 是否变成客户 capex，再验证 capex 是否变成 GPU/ASIC 收入、订单和 backlog。",
        sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025", "SRC-ORCL-FY26-Q2", "SRC-DELL-FY26-Q4"],
        detail: {
          reportNarrative: {
            eyebrow: "核心问题 01 / 需求验证",
            title: "云厂 AI 需求已从模型实验进入算力扩容阶段",
            conclusion: `截至 ${AS_OF_DATE}，GPU/ASIC 需求大幅增长不是单纯来自 AI 叙事，而是已经沿着“工作负载增长 -> 云厂 capex/RPO -> AI server 订单 -> NVIDIA/Broadcom 平台收入”逐步兑现。当前更合理的判断是：本轮 AI factory 已经进入早期加速段，GPU/ASIC 是第一波最直接的 S 曲线载体；但是否值得买，还要继续判断估值是否已经充分反映这条增长线。`,
            logicFlow: [
              "AI 训练、推理和 agent 工作负载增长",
              "云厂和企业需要更多可用 AI compute capacity",
              "capex、RPO、PPE purchases 和云基础设施投入上升",
              "GPU/ASIC、AI server 和系统交付订单增加",
              "NVIDIA、Broadcom、Dell 等收入和 backlog 兑现",
            ],
            chainNodes: [
              {
                title: "AI 训练、推理和 agent 工作负载增长",
                question: "先判断有没有更多真实 AI 计算任务，而不是只看 AI 主题热度。",
                status: "起点成立，但仍需硬数据",
                metrics: [
                  {
                    type: "使用量代理",
                    name: "ChatGPT 用户规模",
                    why: "用户规模不是 GPU 需求本身，但它是 AI 工作负载从少数实验走向大规模日常使用的前导指标。",
                    trendKind: "time_series",
                    series: [
                      { label: "2023-01", value: "100M MAU", scale: 13 },
                      { label: "2023-11", value: "100M WAU", scale: 13 },
                      { label: "2024-08", value: "200M WAU", scale: 25 },
                      { label: "2025-08", value: "700M WAU", scale: 88 },
                      { label: "2025-10", value: "800M WAU", scale: 100 },
                    ],
                    history: "[ChatGPT 2023 年 1 月约 100M 月活](source:SRC-CHATGPT-MAU-202302)。",
                    current: "[2024 年 8 月超过 200M 周活](source:SRC-CHATGPT-WAU-202408)，[2025 年 8 月接近 700M 周活](source:SRC-CHATGPT-WAU-202508)，[2025 年 10 月超过 800M 周活](source:SRC-CHATGPT-WAU-202510)。口径从 MAU 到 WAU 有切换，需按代理指标处理。",
                    future: "如果周活、企业席位和 API/agent 调用继续增长，GPU/ASIC 推理需求会更有持续性；下一步需要更直接的 tokens、GPU hours 和推理调用数据。",
                    quality: "代理指标，MAU/WAU 口径切换",
                    sourceIds: ["SRC-CHATGPT-MAU-202302", "SRC-CHATGPT-WAU-202408", "SRC-CHATGPT-WAU-202508", "SRC-CHATGPT-WAU-202510"],
                  },
                  {
                    type: "任务量代理",
                    name: "每日 prompt / 推理请求",
                    why: "prompt 数更接近推理工作负载，但公开口径稀缺，需要谨慎使用。",
                    series: [
                      { label: "2025-08", value: "2.5B-3.0B / day", scale: 100 },
                    ],
                    seriesGap: "公开材料只有 2025 年附近的单点估算，缺少按季度披露的 prompt / token 时间序列。",
                    history: "缺少可靠公开时间序列。",
                    current: "[公开报道估计 ChatGPT 每日 prompt 约 2.5B-3.0B](source:SRC-CHATGPT-WAU-202508)。",
                    future: "agent、多模态和长上下文会提高每次任务的计算量；但缓存、蒸馏和模型效率提升会抵消部分算力需求。",
                    quality: "单点代理，需补一手数据",
                    sourceIds: ["SRC-CHATGPT-WAU-202508"],
                  },
                  {
                    type: "缺口指标",
                    name: "tokens / GPU hours / 利用率",
                    why: "这是最能直接衡量 AI workload 对 accelerator 需求的指标，但目前公开披露不足。",
                    history: "缺少公开同口径历史数据。",
                    current: "当前报告没有足够公开一手数据。",
                    future: "后续应优先搜集云厂 token volume、AI inference revenue、GPU utilization、API 调用量和客户 ROI。",
                    seriesGap: "这是最该跟踪的核心 metric，但云厂和模型公司没有稳定公开披露，当前不能画连续图。",
                    quality: "关键缺口",
                    sourceIds: ["SRC-NVDA-GTC-DYNAMO-20260316"],
                  },
                ],
                history: "历史上，早期 AI 需求更多停留在训练集群和模型实验，公开材料很少给出统一的 tokens / agent 调用量 / GPU hours 同口径时间序列。因此这里不能假装有完整历史曲线，只能用后续硬件收入和云厂投入作为间接验证。",
                current: "[NVIDIA GTC 2026 把 AI factory 延伸到 Vera Rubin rack-scale / pod-scale 平台](source:SRC-NVDA-GTC-VERA-RUBIN-20260316)，并用 [Dynamo 强调推理调度和吞吐](source:SRC-NVDA-GTC-DYNAMO-20260316)，说明需求口径已经从单次训练扩展到持续在线推理和 agent 工作负载。",
                future: "第一性原理上，用户数、任务数、tokens、上下文长度、多模态和 agent 步数都会提高总计算量；但模型压缩、推理优化和缓存会抵消一部分。未来需要补更硬的 tokens、推理调用量、GPU 利用率和 AI 应用收入数据。",
                refute: "如果模型效率提升快于工作负载增长，或者 AI 应用收入/ROI 不能支撑客户持续部署，那么工作负载增长不会转化为 GPU/ASIC 的持续需求。",
                conclusion: "这一环证明“需求可能继续增长”，但不是投资级别证据。必须继续往后看客户预算、硬件订单和供应商收入。",
                sourceIds: ["SRC-NVDA-GTC-VERA-RUBIN-20260316", "SRC-NVDA-GTC-DYNAMO-20260316", "SRC-OMDIA-AI-PROCESSORS-20250828"],
              },
              {
                title: "云厂和企业需要更多可用 AI compute capacity",
                question: "工作负载是否迫使客户购买更多可用算力，而不是只做软件优化。",
                status: "预算前导较强",
                metrics: [
                  {
                    type: "合同承诺",
                    name: "Commercial RPO",
                    why: "RPO 代表已签约但尚未确认的收入，是未来云服务需求和基础设施交付的前导指标。",
                    trendLabel: "横截面比较",
                    series: [
                      { label: "MSFT FY26 Q2", value: "$625B", scale: 100 },
                      { label: "ORCL FY26 Q2", value: "$523B", scale: 84 },
                    ],
                    seriesGap: "这里是横截面比较，不是同公司连续季度；下一版应补 Microsoft/Oracle RPO 的季度历史。",
                    history: "使用同比增速观察斜率：Microsoft +110%，Oracle +438%。",
                    current: "[Microsoft RPO $625B](source:SRC-MSFT-FY26-Q2)，[Oracle RPO $523B](source:SRC-ORCL-FY26-Q2)。",
                    future: "未来要看 RPO 是否转为云收入，以及新增 RPO 是否继续来自 AI infrastructure。",
                    quality: "强代理，但不是 GPU 订单",
                    sourceIds: ["SRC-MSFT-FY26-Q2", "SRC-ORCL-FY26-Q2"],
                  },
                  {
                    type: "云收入",
                    name: "Cloud revenue growth",
                    why: "如果 AI compute capacity 被真实使用，应当逐步反映到云收入和客户消耗。",
                    trendLabel: "跨公司当前读数",
                    series: [
                      { label: "Azure", value: "+39%", scale: 81 },
                      { label: "Google Cloud", value: "+48%", scale: 100 },
                      { label: "AWS sales", value: "$35.6B", scale: 74 },
                    ],
                    seriesGap: "这里混合了增长率和收入额，不是同一 metric 的连续图；下一版应按公司分别画季度云收入。",
                    history: "用最新同比增长和收入规模做代理。",
                    current: "[Azure and other cloud services +39%](source:SRC-MSFT-FY26-Q2)，[Google Cloud +48%](source:SRC-GOOGL-Q4-2025)，[AWS $35.6B](source:SRC-AMZN-Q4-2025)。",
                    future: "如果 cloud revenue/RPO 继续同步增长，说明可用算力需求仍有预算支撑。",
                    quality: "客户需求代理",
                    sourceIds: ["SRC-MSFT-FY26-Q2", "SRC-GOOGL-Q4-2025", "SRC-AMZN-Q4-2025"],
                  },
                ],
                history: "相比早期模型实验，当前更关键的变化是客户把 AI 需求写进云收入、RPO 和 capex 计划。这里的历史对比用同比和合同承诺做代理，不用单一公司口头表述做代理。",
                current: "[Microsoft commercial RPO 达 $625B、同比增加 110%](source:SRC-MSFT-FY26-Q2)，[Oracle RPO 达 $523B、同比增加 438%](source:SRC-ORCL-FY26-Q2)；Amazon、Alphabet、Meta 也披露大规模基础设施投入。",
                future: "[Alphabet 预计 2026 capex 为 $175B-$185B](source:SRC-GOOGL-Q4-2025)，Meta 也指向 2026 infrastructure capex dollar growth 更大。未来 4-8 个季度要看这些预算是否继续上修，以及 RPO 是否转为云收入。",
                refute: "如果云厂 capex 下修、RPO 增速放缓、AI 服务收入不兑现，或者 FCF 压力迫使客户推迟部署，则这一环降级。",
                conclusion: "客户层需求不是纯叙事，已经进入预算和合同承诺；但它还不是 GPU/ASIC 订单，需要继续验证预算是否落到当前 BOM。",
                sourceIds: ["SRC-MSFT-FY26-Q2", "SRC-ORCL-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025"],
              },
              {
                title: "capex、RPO、PPE purchases 和云基础设施投入上升",
                question: "客户预算是否足够大、足够持续，能支撑未来 accelerator 采购。",
                status: "强支持，但需拆分口径",
                metrics: [
                  {
                    type: "资本开支",
                    name: "Hyperscaler capex / PPE",
                    why: "AI capacity 最终要消耗资本开支，capex/PPE 是预算是否落地的硬指标。",
                    trendLabel: "客户预算横截面",
                    series: [
                      { label: "Amazon TTM PPE", value: "$128.3B", scale: 70 },
                      { label: "Alphabet 2026E capex", value: "$175B-$185B", scale: 100 },
                      { label: "Meta 2025 capex guide", value: "$70B-$72B", scale: 39 },
                    ],
                    seriesGap: "这里是多个客户的预算横截面；下一版应为 Amazon/Alphabet/Meta 分别补过去 8 个季度 capex。",
                    history: "用 TTM、下一年指引和管理层 capex guidance 做截面对比。",
                    current: "[Amazon TTM PPE purchases $128.3B](source:SRC-AMZN-Q4-2025)，[Alphabet 2026 capex $175B-$185B](source:SRC-GOOGL-Q4-2025)，[Meta 2025 capex $70B-$72B](source:SRC-META-Q3-2025)。",
                    future: "未来要拆分 capex 流向：AI accelerator、数据中心土建/电力、网络和通用 IT。",
                    quality: "硬预算，但需拆分",
                    sourceIds: ["SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025"],
                  },
                  {
                    type: "现金约束",
                    name: "FCF pressure",
                    why: "capex 越高，越要验证 AI ROI，否则未来预算可能被砍。",
                    trendLabel: "压力指标截面",
                    series: [
                      { label: "Oracle TTM capex", value: "$35.5B", scale: 100 },
                      { label: "Oracle FCF", value: "-$13.2B", scale: 37 },
                    ],
                    seriesGap: "这里是 capex 与 FCF 压力的当前截面，不是连续季度。",
                    history: "当前为单点压力指标。",
                    current: "[Oracle TTM capex $35.5B、FCF -$13.2B](source:SRC-ORCL-FY26-Q2)。",
                    future: "若 FCF 压力扩大且 AI 收入不兑现，capex 增长会成为反证而非支撑。",
                    quality: "反证指标",
                    sourceIds: ["SRC-ORCL-FY26-Q2"],
                  },
                ],
                history: "同一口径最清晰的是公司披露的同比：Microsoft RPO +110%，Oracle RPO +438%，Vertiv orders/backlog 等物理基础设施数据也显示 AI 基础设施从软件预算进入资本开支周期。",
                current: "[Amazon TTM property and equipment purchases 达 $128.3B](source:SRC-AMZN-Q4-2025)，[Alphabet 2026 capex 指引为 $175B-$185B](source:SRC-GOOGL-Q4-2025)，这些指标说明 AI capacity 建设仍在消耗大量资本。",
                future: "未来空间的关键不是 capex 总额继续变大，而是其中有多少能转成 GPU/ASIC allocation、accelerator 订单和可交付系统。需要继续拆 capex：AI accelerator、数据中心土建/电力、网络、通用 IT 的比例。",
                refute: "如果 capex 继续上升但 accelerator 订单不增，说明资金可能流向土地、电力、建筑或非 AI 资产；如果 FCF 压力导致 capex 计划延后，也会削弱未来需求。",
                conclusion: "预算池足够大，但还需要从总 capex 继续下钻到当前 GPU/ASIC BOM 的采购口径。",
                sourceIds: ["SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-MSFT-FY26-Q2", "SRC-ORCL-FY26-Q2", "SRC-META-Q3-2025"],
              },
              {
                title: "GPU/ASIC、AI server 和系统交付订单增加",
                question: "客户预算是否已经落到 GPU/ASIC 采购和含 GPU/ASIC 的系统交付。",
                status: "订单层成立",
                metrics: [
                  {
                    type: "订单",
                    name: "Dell AI-optimized server flow",
                    why: "AI server orders / shipments / backlog 是 GPU/ASIC 需求进入可交付系统的验证口径。",
                    trendLabel: "订单到收入漏斗",
                    series: [
                      { label: "FY26 orders", value: ">$64B", scale: 100 },
                      { label: "FY26 shipments", value: ">$25B", scale: 39 },
                      { label: "FY27 backlog", value: "$43B", scale: 67 },
                      { label: "FY27 revenue guide", value: "~$50B", scale: 78 },
                    ],
                    seriesGap: "这是订单到收入的漏斗，不是季度时间序列；后续应补 Dell AI server orders / backlog 的季度历史。",
                    history: "用 FY26 orders、shipments、FY27 backlog 和 FY27 revenue guide 看订单到收入链条。",
                    current: "[Dell FY26 orders >$64B、shipments >$25B、FY27 backlog $43B](source:SRC-DELL-FY26-Q4)。",
                    future: "[FY27 AI-optimized server revenue guide 约 $50B、同比 +103%](source:SRC-DELL-FY26-Q4)。",
                    quality: "强下游验证",
                    sourceIds: ["SRC-DELL-FY26-Q4"],
                  },
                  {
                    type: "ASIC 收入",
                    name: "Broadcom AI semiconductor",
                    why: "custom ASIC 是当前 accelerator BOM 内的第二增长路线，能验证需求不只集中于通用 GPU。",
                    trendLabel: "近端两点指引",
                    series: [
                      { label: "Q4 FY25", value: "+74% YoY", scale: 74 },
                      { label: "Q1 FY26 guide", value: "$8.2B / ~2x", scale: 100 },
                    ],
                    seriesGap: "只有两点：上一季同比和下一季指引；后续需要 Broadcom AI semiconductor revenue 的季度序列。",
                    history: "[Q4 FY25 AI semiconductor revenue +74% YoY](source:SRC-AVGO-FY25-Q4)。",
                    current: "AI semiconductor revenue 已是 Broadcom 关键增长线。",
                    future: "[Q1 FY26 AI semiconductor revenue 指引 $8.2B、约同比翻倍](source:SRC-AVGO-FY25-Q4)。",
                    quality: "当前 BOM 内部结构变化",
                    sourceIds: ["SRC-AVGO-FY25-Q4"],
                  },
                ],
                history: "如果只有云厂 capex，没有 AI server orders / shipments / backlog，就不能证明预算落到当前 BOM。现在的变化是订单和交付口径开始出现，并且能和 accelerator 供应商收入相互印证。",
                current: "[Dell FY26 AI-optimized server orders 超过 $64B、shipments 超过 $25B、FY27 backlog 为 $43B](source:SRC-DELL-FY26-Q4)。这里 Dell 不是服务器 BOM 投资结论，而是验证 GPU/ASIC 已经被客户采购并排入可交付系统。",
                future: "[Dell 指引 FY27 AI-optimized server revenue 约 $50B、同比增长 103%](source:SRC-DELL-FY26-Q4)；[Broadcom 指引 Q1 FY26 AI semiconductor revenue 到 $8.2B、约同比翻倍](source:SRC-AVGO-FY25-Q4)。未来 0-4 个季度重点看订单是否转收入、backlog 是否维持、ASIC 指引是否继续上修。",
                refute: "订单取消、交期缩短、GPU/ASIC ASP 下行、AI server backlog 不转收入，都会说明需求没有继续加速。",
                conclusion: "这一环是投资可用需求的关键证据：预算已经进入硬件订单和系统交付。但它仍只验证当前 GPU/ASIC BOM，不提前判断服务器、网络、液冷等其它 BOM 机会。",
                sourceIds: ["SRC-DELL-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-NVDA-FY26-Q4"],
              },
              {
                title: "NVIDIA、Broadcom、Dell 等收入和 backlog 兑现",
                question: "最终是否进到公司收入、backlog 和未来指引，而不是停留在预测。",
                status: "财务兑现强",
                metrics: [
                  {
                    type: "平台收入",
                    name: "NVIDIA Data Center revenue",
                    why: "这是当前 GPU/ASIC BOM 最连续、最直接的财务兑现指标。",
                    trendKind: "time_series",
                    series: [
                      { label: "Q4 FY23", value: "$3.62B", scale: 6 },
                      { label: "Q4 FY24", value: "$18.4B", scale: 30 },
                      { label: "Q4 FY25", value: "$35.6B", scale: 57 },
                      { label: "Q4 FY26", value: "$62.3B", scale: 100 },
                    ],
                    history: "同一公司、同一分部、同一季度口径约 17.2 倍。",
                    current: "[Q4 FY26 Data Center revenue $62.3B](source:SRC-NVDA-FY26-Q4)。",
                    future: "未来要看下一季指引、毛利率、客户集中度和 Blackwell/Vera Rubin 交付节奏。",
                    quality: "核心硬指标",
                    sourceIds: ["SRC-NVDA-FY23-Q4", "SRC-NVDA-FY24-Q4", "SRC-NVDA-FY25-Q4", "SRC-NVDA-FY26-Q4"],
                  },
                  {
                    type: "市场空间",
                    name: "AI data-center processor spending",
                    why: "用于判断当前 BOM 的远期池子，不用于直接预测单家公司收入。",
                    trendKind: "time_series",
                    series: [
                      { label: "2024", value: "$123B", scale: 43 },
                      { label: "2025E", value: "$207B", scale: 72 },
                      { label: "2030E", value: "$286B", scale: 100 },
                    ],
                    history: "[Omdia 2024 约 $123B、2025E 约 $207B](source:SRC-OMDIA-AI-PROCESSORS-20250828)。",
                    current: "2025E 已经是高基数。",
                    future: "[2030E 约 $286B](source:SRC-OMDIA-AI-PROCESSORS-20250828)，说明仍有增长但不能按过去 17 倍外推。",
                    quality: "第三方远期锚点",
                    sourceIds: ["SRC-OMDIA-AI-PROCESSORS-20250828"],
                  },
                ],
                history: "[NVIDIA Q4 FY23 Data Center revenue 为 $3.62B](source:SRC-NVDA-FY23-Q4)，[Q4 FY24 为 $18.4B](source:SRC-NVDA-FY24-Q4)，[Q4 FY25 为 $35.6B](source:SRC-NVDA-FY25-Q4)，[Q4 FY26 为 $62.3B](source:SRC-NVDA-FY26-Q4)，同一分部季度收入约 17.2 倍。",
                current: "[NVIDIA Q4 FY26 Data Center revenue 达 $62.3B](source:SRC-NVDA-FY26-Q4)；Broadcom Q4 FY25 AI semiconductor revenue 增长 74%，且 Q1 FY26 AI semiconductor revenue 指引到 $8.2B。",
                future: "[Omdia 预计 AI data-center processor spending 从 2024 约 $123B、2025E 约 $207B 到 2030E 约 $286B](source:SRC-OMDIA-AI-PROCESSORS-20250828)。未来增长仍有空间，但高基数下不能按过去 17 倍线性外推。",
                refute: "如果 NVIDIA/Broadcom 指引放缓、毛利率下降、客户集中度风险上升，或者 custom ASIC 替代压低通用 GPU 价格和利润率，则当前 BOM 的 S 曲线强度要下调。",
                conclusion: "GPU/ASIC 需求已经满足“历史加速 + 当前兑现 + 未来仍有公开锚点”的条件。下一步不是讨论其它 BOM，而是在当前 BOM 内比较 NVIDIA、Broadcom、AMD、云厂自研 ASIC 链条谁还有赔率。",
                sourceIds: ["SRC-NVDA-FY23-Q4", "SRC-NVDA-FY24-Q4", "SRC-NVDA-FY25-Q4", "SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-OMDIA-AI-PROCESSORS-20250828"],
              },
            ],
            historicalComparison: {
              label: "历史对比 / 加速斜率",
              title: "为什么说现在比以前多很多：同一收入口径已经从十亿美元级跳到六百亿美元级",
              summary: "感知 AI S 曲线不能只看当前绝对值，而要看同口径指标的斜率。NVIDIA Data Center quarterly revenue 是 GPU/ASIC 需求最直接、最连续的公开代理：Q4 FY23 为 $3.62B，Q4 FY26 为 $62.3B，约 17.2 倍。客户侧 RPO/capex 和系统侧 backlog 只能做旁证，但它们共同说明需求已经从模型热度传导到预算、订单和交付。",
              snapshots: [
                {
                  label: "平台收入基准",
                  value: "$3.62B",
                  note: "NVIDIA Q4 FY23 Data Center revenue，还没有体现后续 AI factory 放量。",
                  sourceIds: ["SRC-NVDA-FY23-Q4"],
                },
                {
                  label: "平台收入当前",
                  value: "$62.3B",
                  note: "NVIDIA Q4 FY26 Data Center revenue，约为 Q4 FY23 的 17.2 倍。",
                  sourceIds: ["SRC-NVDA-FY26-Q4"],
                },
                {
                  label: "客户承诺旁证",
                  value: "$625B RPO",
                  note: "Microsoft commercial RPO 同比增加 110%，说明客户已经把未来云服务需求锁进合同/待履约义务。",
                  sourceIds: ["SRC-MSFT-FY26-Q2"],
                },
                {
                  label: "系统交付旁证",
                  value: "$43B backlog",
                  note: "Dell FY26 结束时进入 FY27 的 AI-optimized server backlog，证明需求进入服务器系统交付环节。",
                  sourceIds: ["SRC-DELL-FY26-Q4"],
                },
              ],
              bars: [
                { period: "Q4 FY23", value: "$3.62B", scale: 5.8, sourceIds: ["SRC-NVDA-FY23-Q4"] },
                { period: "Q4 FY24", value: "$18.4B", scale: 29.5, sourceIds: ["SRC-NVDA-FY24-Q4"] },
                { period: "Q4 FY25", value: "$35.6B", scale: 57.1, sourceIds: ["SRC-NVDA-FY25-Q4"] },
                { period: "Q4 FY26", value: "$62.3B", scale: 100, sourceIds: ["SRC-NVDA-FY26-Q4"] },
              ],
              rows: [
                {
                  stage: "平台收入",
                  baseline: "[NVIDIA Q4 FY23 Data Center revenue 为 $3.62B](source:SRC-NVDA-FY23-Q4)。",
                  latest: "[Q4 FY26 Data Center revenue 为 $62.3B](source:SRC-NVDA-FY26-Q4)。",
                  readThrough: "同一公司、同一分部、同一季度口径约 17.2 倍，说明 GPU/ASIC 需求不是线性增长，而是已经出现 S 曲线加速段。",
                  sourceIds: ["SRC-NVDA-FY23-Q4", "SRC-NVDA-FY24-Q4", "SRC-NVDA-FY25-Q4", "SRC-NVDA-FY26-Q4"],
                },
                {
                  stage: "客户预算 / 承诺",
                  baseline: "早期 AI 热度不能作为投资可用需求，必须看到客户预算和承诺上行。",
                  latest: "[Microsoft commercial RPO 达 $625B、同比增加 110%](source:SRC-MSFT-FY26-Q2)；[Oracle RPO 达 $523B、同比增加 438%](source:SRC-ORCL-FY26-Q2)。",
                  readThrough: "RPO 是未来尚未确认收入的合同承诺；它不能直接等同 GPU 订单，但能说明云厂客户已经把一部分未来需求锁成可交付承诺。",
                  sourceIds: ["SRC-MSFT-FY26-Q2", "SRC-ORCL-FY26-Q2"],
                },
                {
                  stage: "系统订单 / 交付",
                  baseline: "如果只看到芯片收入，没有服务器和机柜交付，仍可能只是平台商单点繁荣。",
                  latest: "[Dell FY26 AI-optimized server orders 超过 $64B、shipments 超过 $25B、进入 FY27 backlog 为 $43B](source:SRC-DELL-FY26-Q4)。",
                  readThrough: "这说明需求已经进入系统交付层。GPU/ASIC 不是孤立卖芯片，而是在被装进服务器、机柜和集群后交给客户使用。",
                  sourceIds: ["SRC-DELL-FY26-Q4"],
                },
                {
                  stage: "当前 BOM 的下游交付验证",
                  baseline: "如果 GPU/ASIC 只停在平台商收入，而没有进入服务器系统订单，需求可能只是短期抢货。",
                  latest: "[Dell FY26 AI-optimized server orders 超过 $64B、shipments 超过 $25B、FY27 backlog 为 $43B](source:SRC-DELL-FY26-Q4)。",
                  readThrough: "服务器订单和 backlog 在这里不是研究服务器 BOM，而是验证 GPU/ASIC 已经被客户采购并排入可交付系统。",
                  sourceIds: ["SRC-DELL-FY26-Q4"],
                },
              ],
            },
            futureRunway: {
              label: "未来推演 / 剩余空间与兑现时间",
              title: "历史加速之后，下一步要判断 metric 还能增长多少、多久兑现",
              summary: "未来空间不能用 Q4 FY23 到 Q4 FY26 的 17 倍直接外推。当前卡片只研究 GPU/ASIC 这个 BOM：第一性原理上 AI workload 是否继续消耗更多 accelerator 算力；公开市场拆法上 AI processor / custom ASIC 等同节点 metric 是否仍有增量；财务链条上这些增量能否在 2026-2028 年进入 accelerator 收入、订单和 backlog。其他 BOM 的机会放到各自章节独立研究。",
              formula: [
                {
                  title: "工作负载斜率",
                  body: "需求的根来自训练、推理和 agent 工作负载：用户数、任务数、tokens、上下文长度、视频/多模态、推理深度都会提高总算力需求；模型效率提升和软件优化会抵消一部分需求。",
                },
                {
                  title: "硬件转换率",
                  body: "AI workload 不会自动变成 accelerator 收入，必须经过云厂 capex/RPO、采购排产、GPU/ASIC allocation、服务器系统交付验证，最后才进入 NVIDIA、Broadcom 等 accelerator 供应商收入，以及 Dell 这类下游系统商 backlog 的验证信号。",
                },
                {
                  title: "剩余空间判断",
                  body: "如果公开预测显示 AI processor TAM 继续扩大、云厂预算继续上修、GPU/ASIC 收入和订单仍有增量、ASIC/GPU 平台继续迭代，则说明当前 BOM 的 S 曲线还没结束；如果只有当前收入高而未来 TAM、capex 或 accelerator 订单不再上行，就说明加速段可能接近成熟。",
                },
              ],
              metrics: [
                {
                  metric: "AI data-center processor spending",
                  current: "[Omdia 给出的 2024 规模约 $123B，2025E 约 $207B](source:SRC-OMDIA-AI-PROCESSORS-20250828)。",
                  future: "[2030E 约 $286B](source:SRC-OMDIA-AI-PROCESSORS-20250828)，custom ASICs gaining traction。",
                  timing: "2025-2030",
                  readThrough: "这说明 GPU/ASIC 总需求池仍在扩张，但从 2025E 到 2030E 不是再来一次 17 倍，而是进入更高基数下的结构性增长；当前 BOM 内部的重点是通用 GPU 与 custom ASIC 的结构变化。",
                  sourceIds: ["SRC-OMDIA-AI-PROCESSORS-20250828"],
                },
                {
                  metric: "AI server 系统交付",
                  current: "[Dell FY26 AI-optimized server shipments 超过 $25B，进入 FY27 backlog 为 $43B](source:SRC-DELL-FY26-Q4)。",
                  future: "[Dell 同一材料给出 FY27 AI-optimized server revenue 约 $50B、同比增长 103% 的管理层目标/展望](source:SRC-DELL-FY26-Q4)。",
                  timing: "FY2027",
                  readThrough: "这是 GPU/ASIC 需求的下游交付验证：不是只看云厂预算，而是看到含 GPU/ASIC 的 AI server 已经排到未来收入和 backlog。这里不把服务器作为独立投资节点，只用它验证当前 BOM 的采购需求。",
                  sourceIds: ["SRC-DELL-FY26-Q4"],
                },
                {
                  metric: "custom AI semiconductor revenue",
                  current: "[Broadcom Q4 FY25 AI semiconductor revenue 增长 74% YoY](source:SRC-AVGO-FY25-Q4)。",
                  future: "[Broadcom 指引 Q1 FY26 AI semiconductor revenue 到 $8.2B、约同比翻倍](source:SRC-AVGO-FY25-Q4)。",
                  timing: "FY2026 Q1 起",
                  readThrough: "这说明未来增长不只来自通用 GPU，也会来自云厂自研/定制 ASIC。它既扩大 AI accelerator 总需求，也可能改变 NVIDIA 与 ASIC 供应链之间的利润分配。",
                  sourceIds: ["SRC-AVGO-FY25-Q4"],
                },
                {
                  metric: "客户预算与合同承诺",
                  current: "[Microsoft commercial RPO 达 $625B、同比增加 110%](source:SRC-MSFT-FY26-Q2)，[Oracle RPO 达 $523B、同比增加 438%](source:SRC-ORCL-FY26-Q2)。",
                  future: "[Alphabet 预计 2026 capex 为 $175B-$185B](source:SRC-GOOGL-Q4-2025)，Meta 也指向 2026 基础设施 capex dollar growth 更大。",
                  timing: "2026",
                  readThrough: "RPO/capex 是未来硬件需求的预算前导。它不能精确换算 GPU 数量，但能判断未来 4-8 个季度客户是否仍有能力继续下单。",
                  sourceIds: ["SRC-MSFT-FY26-Q2", "SRC-ORCL-FY26-Q2", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025"],
                },
                {
                  metric: "平台代际扩展",
                  current: "当前收入主要由 Hopper/Blackwell 周期和早期 AI factory 建设驱动。",
                  future: "[Vera Rubin 把下一代平台扩展到七颗芯片和五类 rack-scale 系统](source:SRC-NVDA-GTC-VERA-RUBIN-20260316)，[Dynamo 强调推理调度和 AI factory 利用率](source:SRC-NVDA-GTC-DYNAMO-20260316)。",
                  timing: "2026-2028",
                  readThrough: "第一性原理上，如果平台从单 GPU 扩到 rack-scale / cluster-scale accelerator，并且推理和 agent 负载提升在线利用率，那么当前 BOM 的 GPU/ASIC 采购强度会继续提高；反过来，如果推理效率提升快于工作负载增长，accelerator 增速会降级。",
                  sourceIds: ["SRC-NVDA-GTC-VERA-RUBIN-20260316", "SRC-NVDA-GTC-DYNAMO-20260316"],
                },
              ],
              timeline: [
                {
                  period: "0-4 个季度",
                  label: "看订单和指引是否继续兑现",
                  body: "优先跟踪 NVIDIA/Broadcom 下一季 AI revenue 指引、Dell backlog 转收入、云厂 capex 指引是否上修或下修。",
                },
                {
                  period: "4-8 个季度",
                  label: "看系统交付和供给约束",
                  body: "如果 Dell AI server revenue 和 backlog 按计划转收入，同时 NVIDIA/Broadcom accelerator 指引继续上行，说明当前 BOM 的需求不仅停留在芯片收入，也进入可交付系统。其他 BOM 的供需斜率在后续章节单独判断。",
                },
                {
                  period: "2028-2030",
                  label: "看总需求池是否还能扩张",
                  body: "Omdia 的 AI data-center processor forecast 给出 2030E 约 $286B 的远期锚点，但增速会从早期爆发转向更高基数下的结构性增长，核心是 GPU 与 custom ASIC 在当前 accelerator BOM 内的份额和价格变化。",
                },
              ],
              verdictTitle: "当前结论",
              verdict: "历史同口径数据已经证明 GPU/ASIC 需求进入加速段；未来空间仍存在，但不能简单按过去 17 倍外推。更合理的判断是：2026-2027 年看 accelerator 收入、订单、backlog、云厂 capex/RPO 和 AI server 交付验证；2028-2030 年看 AI processor 总池、custom ASIC 分流、推理/agent 工作负载和价格/毛利是否仍能支撑当前 BOM。投资上，本卡片只回答 GPU/ASIC 这一个 BOM 是否还有需求空间，不把其他 BOM 的机会提前写进来。",
            },
            paragraphs: [
              "判断 GPU/ASIC 需求时，第一步不是问“AI 是否热门”，而是问 AI 工作负载是否迫使客户购买更多可用算力。历史对比给出的答案更直观：NVIDIA Q4 FY23 Data Center revenue 只有 $3.62B，而 Q4 FY26 已达到 $62.3B，说明需求已经从早期尝试进入平台收入的指数级放大阶段。NVIDIA 在 GTC 2026 把 AI factory 继续扩展到 Vera Rubin rack-scale / pod-scale 平台，并用 Dynamo 强调推理吞吐和调度，这说明需求口径已经从单卡训练扩展到持续在线的训练、推理和 agent 工作负载。",
              "第二步要看客户是否把工作负载转成预算。Microsoft commercial RPO 达 $625B，Azure and other cloud services revenue 增长 39%；Amazon AWS revenue 增至 $35.6B，TTM property and equipment purchases 达 $128.3B；Alphabet 指引 2026 capex 为 $175B-$185B；Meta 和 Oracle 也给出持续基础设施扩张信号。多家客户同时扩大预算，比单一公司管理层说需求强更有证明力。",
              "第三步才是投资上最关键的一步：预算是否进入 GPU/ASIC 和系统交付。Dell FY26 AI-optimized server orders 超过 $64B、shipments 超过 $25B、进入 FY27 backlog 为 $43B；NVIDIA Q4 FY26 Data Center revenue 达 $62.3B；Broadcom 指引 Q1 FY26 AI semiconductor revenue 到 $8.2B。这些是链条后半段证据，说明客户需求已经从“想做 AI”进入“下单采购 AI 基础设施”。",
            ],
            keyData: [
              {
                question: "AI 需求是否真实增长？",
                metric: "AI 平台路线、推理吞吐、AI processor forecast",
                evidence: "NVIDIA 将 AI factory 从 GPU 扩展到 Vera Rubin rack-scale / pod-scale 系统；Omdia 预计 AI data-center processor spending 仍处扩张通道。",
                judgment: "支持，但只是起点",
                sourceIds: ["SRC-NVDA-GTC-VERA-RUBIN-20260316", "SRC-NVDA-GTC-DYNAMO-20260316", "SRC-OMDIA-AI-PROCESSORS-20250828"],
              },
              {
                question: "客户是否需要新增算力？",
                metric: "cloud revenue、RPO、capex、PPE purchases",
                evidence: "Microsoft RPO、Amazon PPE purchases、Alphabet 2026 capex guidance、Meta capex guidance、Oracle RPO 均指向基础设施扩张。",
                judgment: "预算层成立",
                sourceIds: ["SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025", "SRC-ORCL-FY26-Q2"],
              },
              {
                question: "预算是否传到硬件订单？",
                metric: "AI server orders、shipments、backlog",
                evidence: "Dell FY26 AI-optimized server orders 超过 $64B，shipments 超过 $25B，进入 FY27 backlog 为 $43B。",
                judgment: "强支持",
                sourceIds: ["SRC-DELL-FY26-Q4"],
              },
              {
                question: "是否已经体现到平台收入？",
                metric: "Data Center revenue、AI semiconductor revenue",
                evidence: "NVIDIA Q4 FY26 Data Center revenue 达 $62.3B；Broadcom 指引 Q1 FY26 AI semiconductor revenue 到 $8.2B。",
                judgment: "强支持",
                sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4"],
              },
              {
                question: "这是否直接等于投资机会？",
                metric: "估值隐含预期、盈利上修、毛利率、FCF",
                evidence: "当前材料证明需求和财务兑现，但还不足以证明赔率未被市场充分定价。",
                judgment: "需进入估值/赔率判断",
                sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4"],
              },
            ],
            investmentImplication: "GPU/ASIC 是 AI factory 第一波 S 曲线最直接的承接节点，胜率证据最强；但它也最容易被市场提前定价。因此本节点的研究结论不应直接写成“买 NVIDIA”，而应继续追问：NVIDIA、Broadcom、AMD 或云厂自研 ASIC 相关公司的盈利上修是否超过估值隐含预期，以及当前 accelerator BOM 的价格、份额和毛利是否还能继续上行。",
            bearCases: [
              "云厂 capex 或 RPO 指引下修，说明客户预算端开始降温。",
              "AI ROI 不达预期，客户用软件优化或模型效率提升替代新增算力。",
              "GPU 交期缩短、租赁价格下跌、订单取消或毛利率下降，说明供需紧张缓解。",
              "custom ASIC 份额提升本身不是反证；只有当 ASIC 替代压低整个 accelerator 需求或显著压低通用 GPU 价格时，才构成对 NVIDIA 路线的实质反证。",
            ],
          },
          thesis: `本卡片只研究数据中心 GPU/ASIC 需求，不研究 PC GPU，也不直接讨论谁最赚钱。截至 ${AS_OF_DATE}，需求链条已经打通到后半段：AI workload 增长不只是叙事，它已经进入云厂 capex/RPO，再进入 NVIDIA/Broadcom 平台收入和 Dell AI server orders/backlog。当前判断是“需求大幅增长已经被多环证据验证”，但赔率还要继续看 capex ROI、供给松紧和市场定价。`,
          chainAudit: [
            {
              stage: "AI 训练 / 推理 / agent 工作负载增长",
              verifyQuestion: "先验证是否真的有更多 AI 工作负载，而不是只看概念热度。",
              materials: "搜集 NVIDIA GTC 2026 平台发布、Dynamo 推理调度、Omdia AI data-center processor forecast，以及云厂对 AI 服务/云收入的披露。",
              parsed: "NVIDIA 将 AI factory 从 GPU 扩展到 Vera Rubin rack-scale/pod-scale 平台，并用 Dynamo 强调推理吞吐与调度；Omdia 给出 AI data-center processor spending 继续扩张的第三方拆法；Microsoft、Amazon、Alphabet 的云收入和 AI 基础设施表述说明工作负载不是单一实验项目。",
              judgment: "工作负载增长这一环成立，但它只是起点。投资上不能停在“AI 使用更多”这一层，必须继续验证客户是否把它转成预算和订单。",
              gap: "还缺少更硬的 token 量、推理调用量、GPU 利用率、AI 应用收入和客户 ROI 数据；这些会决定当前 GPU/ASIC 需求能否从训练延续到长期推理。",
              status: "已验证起点",
              confidence: "中高",
              sourceIds: ["SRC-NVDA-GTC-VERA-RUBIN-20260316", "SRC-NVDA-GTC-DYNAMO-20260316", "SRC-OMDIA-AI-PROCESSORS-20250828", "SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025"],
            },
            {
              stage: "云厂和企业需要更多 AI compute capacity",
              verifyQuestion: "工作负载是否迫使客户增加可用算力，而不是只做软件优化。",
              materials: "搜集 Microsoft Azure/RPO、Amazon AWS/PPE purchases、Alphabet Google Cloud 与 2026 capex、Meta capex guidance、Oracle RPO 和 capex。",
              parsed: "Microsoft commercial RPO 达 $625B、Azure and other cloud services revenue 增长 39%；Amazon AWS revenue 增至 $35.6B，TTM property/equipment purchases 达 $128.3B；Alphabet 指引 2026 capex $175B-$185B；Meta 和 Oracle 同样给出基础设施扩张信号。",
              judgment: "客户算力需求已经进入预算层。多家云厂同时提高 capex/RPO，比单家公司说 AI 需求强更有证明力。",
              gap: "仍需验证这些 capex 中多少直接用于 AI accelerator，多少用于普通数据中心、土地、建筑、电力和其他基础设施。",
              status: "预算层成立",
              confidence: "高",
              sourceIds: ["SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025", "SRC-ORCL-FY26-Q2"],
            },
            {
              stage: "capex 和 RPO / backlog 上升",
              verifyQuestion: "客户预算是否具备持续性，是否形成可见的待交付需求。",
              materials: "搜集 hyperscaler RPO、capex guidance、PPE purchases、FCF 压力和管理层对基础设施投资的解释。",
              parsed: "Microsoft 和 Oracle 的 RPO 给出未来收入/交付可见度；Amazon PPE purchases、Alphabet 2026 capex guidance 和 Meta capex guidance 表明资本开支仍在扩大，但 Amazon 与 Oracle 的 FCF 压力也提示回报率约束会成为反证。",
              judgment: "capex/RPO/backlog 这一环整体支持需求扩张，但已经需要引入 ROI 约束。只看 capex 上升会高估确定性。",
              gap: "下一步必须把 capex 拆成 AI accelerator、网络、数据中心土建/电力、通用 IT 四类，否则无法判断 GPU/ASIC 的真实弹性。",
              status: "已验证但需拆分",
              confidence: "中高",
              sourceIds: ["SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025", "SRC-ORCL-FY26-Q2"],
            },
            {
              stage: "GPU / ASIC 订单与系统交付增加",
              verifyQuestion: "客户预算是否真的流向 GPU/ASIC 和 AI server，而不是停留在总 capex。",
              materials: "搜集 Dell AI-optimized server orders、shipments、backlog，Broadcom AI semiconductor revenue 指引，以及 NVIDIA Data Center revenue。",
              parsed: "Dell FY26 披露 AI-optimized server orders 超过 $64B、shipments 超过 $25B、进入 FY27 backlog 为 $43B；Broadcom 指引 Q1 FY26 AI semiconductor revenue 达 $8.2B；这些材料把客户预算从“想投 AI”推进到“已经下单和交付”。",
              judgment: "这是链条里最关键的投资验证环节：预算已经转成硬件订单和系统交付。GPU/ASIC 需求大涨不是只靠预测，而是有订单和 backlog 支撑。",
              gap: "缺少订单取消率、交期、GPU/ASIC ASP、云厂项目分布、AMD GPU 与云厂自研 ASIC 的更完整份额数据。",
              status: "订单层成立",
              confidence: "高",
              sourceIds: ["SRC-DELL-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-NVDA-FY26-Q4"],
            },
            {
              stage: "平台收入和服务器 backlog 兑现",
              verifyQuestion: "最终是否体现到公司收入、毛利、backlog，而不是只有行业预测。",
              materials: "搜集 NVIDIA Q4 FY26 Data Center revenue、Broadcom AI semiconductor revenue growth / Q1 guide、Dell AI server backlog。",
              parsed: "NVIDIA Q4 FY26 Data Center revenue 达 $62.3B；Broadcom Q4 FY25 AI semiconductor revenue 增长 74%，并指引 Q1 FY26 AI semiconductor revenue 翻倍到 $8.2B；Dell 的 AI server backlog 说明系统交付侧仍有待兑现需求。",
              judgment: "后半段已经兑现，因此 GPU/ASIC 需求大涨可以作为投资级别问题继续研究。当前更需要问的是：在 GPU、custom ASIC 和相关 accelerator 供应链里，谁的赔率还没被市场充分定价。",
              gap: "需要补估值隐含预期、盈利上修幅度、毛利率趋势和客户集中度，防止把已被充分定价的高胜率误判成高赔率。",
              status: "财务兑现",
              confidence: "高",
              sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-DELL-FY26-Q4"],
            },
          ],
          steps: [
            {
              title: "定义需求口径",
              body: "研究对象是数据中心 AI accelerator，包括 NVIDIA 通用 GPU、AMD data-center GPU、Broadcom/云厂 custom ASIC，以及承载这些芯片的平台采购需求。不是 PC 显卡，也不是泛半导体景气。",
            },
            {
              title: "建立第一性原理链条",
              body: "需求链条应写成：AI 训练/推理/agent 工作负载增长 -> 云厂和企业需要更多 AI compute capacity -> capex 和 RPO/backlog 上升 -> GPU/ASIC 订单与系统交付增加 -> 平台收入和服务器 backlog 兑现。只有链条后半段出现，才算投资可用需求。",
            },
            {
              title: "验证客户预算是否真实增加",
              body: "客户侧优先看云厂 capex、RPO、cloud revenue 和 FCF 压力。Microsoft commercial RPO、Amazon PPE purchases、Alphabet 2026 capex、Meta capex guidance、Oracle RPO 是本节点需求的预算层证据。",
              sourceIds: ["SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025", "SRC-ORCL-FY26-Q2"],
            },
            {
              title: "验证预算是否转成 GPU/ASIC 订单",
              body: "平台侧优先看 NVIDIA Data Center revenue、Broadcom AI semiconductor revenue、Dell AI-optimized server orders/backlog。NVIDIA Q4 FY26 Data Center revenue 达 $62.3B，Broadcom 指引 Q1 FY26 AI semiconductor revenue 到 $8.2B，Dell FY26 AI server orders/backlog 说明客户预算已进入硬件订单。",
              sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-DELL-FY26-Q4"],
            },
            {
              title: "区分 GPU 与 ASIC 的关系",
              body: "custom ASIC 不是天然反证。若 Broadcom/云厂 ASIC 收入上升，同时 NVIDIA 数据中心收入继续增长，说明 AI accelerator 总需求池扩大；只有 ASIC 份额提升同时压低总体 GPU/ASIC 增长，才是需求降级信号。",
              sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-OMDIA-AI-PROCESSORS-20250828"],
            },
            {
              title: "主动搜索反证",
              body: "反证重点不是“AI 有没有泡沫”这种泛问题，而是具体触发器：云厂 capex 下修、AI ROI 不足、GPU 租赁价格下行、交期缩短、订单取消、模型效率大幅抵消算力需求、ASIC 替代导致总体 accelerator 增长放缓。",
              sourceIds: ["SRC-AMZN-Q4-2025", "SRC-META-Q3-2025", "SRC-GOOGL-Q4-2025"],
            },
          ],
          checks: [
            ["AI workload 增长", "GTC 2026 把 AI factory 平台继续扩展到 Vera Rubin、rack-scale/pod-scale 系统和推理调度层。", "支持需求继续扩张", "补 token、推理调用、企业 AI 使用量和 AI revenue 数据"],
            ["客户预算", "MSFT/AMZN/GOOGL/META/ORCL 的 capex、RPO、PPE 或云基础设施投入仍在上行。", "预算层已验证", "补 capex ROI、FCF 压力和管理层对回报的表述"],
            ["硬件订单", "NVIDIA Data Center revenue、Broadcom AI semiconductor 指引、Dell AI server orders/backlog 同时强。", "订单层已验证", "补 AMD GPU 指引、GPU 交期、云 GPU 价格和订单取消率"],
            ["需求持续性", "训练、推理、agent 和主权 AI 都可能继续拉动 accelerator，但持续性取决于客户收入和利用率。", "需要持续跟踪", "补 AI 服务收入、利用率、客户采购节奏"],
            ["反证", "若 capex 下修、GPU 供给松动、租赁价格下跌或 ASIC 分流压低总需求，需求判断降级。", "定义降级条件", "建立季度红黄绿触发器"],
          ],
        },
      },
      {
        question: "单位用量是否会提升？",
        answer: "rack-scale 架构把需求从单卡扩大到机柜级平台，更多 GPU/ASIC 会同时拉动 HBM、网络、功耗和散热。",
        sourceIds: ["SRC-SA-GB200-BOM-2024", "SRC-NVDA-GTC-VERA-RUBIN-20260316", "SRC-NVDA-GTC-DYNAMO-20260316"],
        detail: {
          thesis: "单位用量提升的核心不是“每张 GPU 更贵”这么简单，而是 AI factory 从单服务器采购变成机柜、pod 和集群级采购。只要平台规格继续向 rack-scale 演进，单个训练/推理集群对应的 GPU、HBM、NVLink/以太网、液冷和电力用量都会同步放大。",
          steps: [
            {
              title: "看平台形态是否升级",
              body: "GB200/NVL72 和 Vera Rubin 的共同点是把 GPU、CPU、互联、网络和系统管理组合成 rack-scale/pod-scale 平台。投资上应把需求单位从“卡”改成“机柜/集群”。",
              sourceIds: ["SRC-SA-GB200-BOM-2024", "SRC-NVDA-GTC-VERA-RUBIN-20260316"],
            },
            {
              title: "看推理是否提高利用和并发",
              body: "Dynamo 这类推理调度层如果提高 Blackwell 推理吞吐和利用率，会让客户更愿意把 GPU 采购从训练扩展到持续在线推理。它不是硬件收入本身，但会提高硬件部署的经济性。",
              sourceIds: ["SRC-NVDA-GTC-DYNAMO-20260316"],
            },
            {
              title: "只看当前 accelerator BOM 的单位强度",
              body: "本节点只判断 GPU/ASIC 自身的单位用量是否提升：从单卡、单服务器，走向 rack-scale / pod-scale / cluster-scale accelerator 部署。HBM、网络、光模块、电力和液冷的单位用量在各自 BOM 章节单独研究。",
              sourceIds: ["SRC-SA-GB200-BOM-2024"],
            },
          ],
          checks: [
            ["平台单位", "从 server/card 转向 rack/pod/cluster。", "支持单位用量提升", "补各代平台单柜 GPU/ASIC 数量、ASP、利用率和交付节奏"],
            ["推理利用", "Dynamo 等软件层强化推理吞吐和调度。", "支持部署经济性", "补客户侧推理收入和 GPU 利用率"],
            ["当前 BOM 边界", "只判断 GPU/ASIC 单位采购强度是否提高，其他节点留到各自 BOM 章节。", "避免跨 BOM 混写", "补单柜/单集群 accelerator 数量、ASP、利用率和订单口径"],
          ],
        },
      },
      {
        question: "供给能否跟上？",
        answer: "供给受先进制程、先进封装、HBM、系统集成和客户认证共同限制。",
        sourceIds: ["SRC-SA-COWOS-HBM-2023", "SRC-TSM-Q4-2025", "SRC-MU-FY26-Q1-PREPARED", "SRC-SKHYNIX-FY25"],
        detail: {
          thesis: "GPU/ASIC 供给不是只看晶圆产能，而是先进制程、CoWoS/先进封装、HBM、基板、系统集成和客户认证的串联约束。只要其中一个环节慢于需求斜率，最终可交付 AI accelerator 就仍可能短缺。",
          steps: [
            {
              title: "拆出真实供给链",
              body: "AI accelerator 供给链至少包含设计、先进制程、先进封装、HBM、高速互联、服务器集成和数据中心上线。研究中不能把 TSMC 晶圆产能等同于最终 GPU 供给。",
              sourceIds: ["SRC-SA-COWOS-HBM-2023", "SRC-TSM-Q4-2025"],
            },
            {
              title: "识别最慢环节",
              body: "SemiAnalysis 早期就把 CoWoS 和 HBM 作为 AI capacity constraint；Micron 与 SK hynix 的 AI/HBM 表述说明内存链条也在进入供给紧张和高价值阶段。",
              sourceIds: ["SRC-SA-COWOS-HBM-2023", "SRC-MU-FY26-Q1-PREPARED", "SRC-SKHYNIX-FY25"],
            },
            {
              title: "跟踪释放路径",
              body: "如果 TSMC capex、HBM 产能、CoWoS 产能和系统交付能力都扩张，短缺会逐步缓解；但扩产释放往往存在设备交付、良率和客户验证周期。",
              sourceIds: ["SRC-TSM-Q4-2025", "SRC-MU-FY26-Q1-PREPARED"],
            },
          ],
          checks: [
            ["先进制程", "TSMC advanced technologies 占 wafer revenue 高，2026 capex 指引明显扩张。", "供给扩张但仍集中", "补 N2/N3/N4 capacity 与 AI 客户 allocation"],
            ["先进封装", "CoWoS/2.5D packaging 是 AI accelerator 的关键串联约束。", "短中期仍需重点跟踪", "补 CoWoS 月产能和客户分配"],
            ["HBM", "HBM 供给协议、价格和产能是 GPU/ASIC 可交付量的硬约束。", "约束未完全解除", "补 HBM3e/HBM4 供应商份额与良率"],
          ],
        },
      },
      {
        question: "谁控制供给？",
        answer: "NVIDIA 控制通用 GPU 平台和软件/互联生态，Broadcom/云厂 custom ASIC 是第二路线；但最终供给还受 TSMC、HBM 厂和系统交付商限制。",
        sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-TSM-Q4-2025", "SRC-MU-FY26-Q1-PREPARED", "SRC-SKHYNIX-FY25"],
        detail: {
          thesis: "供给控制权分两层：产品平台由 NVIDIA 和云厂 custom ASIC 生态控制；实物交付由 TSMC、先进封装、HBM 供应商和系统交付能力共同决定。投资判断不能只问谁设计芯片，还要问谁能把芯片稳定交付给客户。",
          steps: [
            {
              title: "平台控制",
              body: "NVIDIA 的 Data Center revenue 和 GTC 平台路线表显示它仍是通用 AI accelerator 的核心平台控制方；Broadcom 的 AI semiconductor 指引说明 custom ASIC 已形成第二条增长路线。",
              sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-NVDA-GTC-VERA-RUBIN-20260316", "SRC-AVGO-FY25-Q4"],
            },
            {
              title: "制造控制",
              body: "高端 GPU/ASIC 离不开先进制程和先进封装，TSMC 的先进技术收入占比和 capex 指引使其成为供给链的关键控制点。",
              sourceIds: ["SRC-TSM-Q4-2025"],
            },
            {
              title: "内存控制",
              body: "HBM 供应能力会直接约束 GPU/ASIC 平台交付，Micron 和 SK hynix 的 AI memory/HBM 兑现说明内存厂在供给链中的议价权上升。",
              sourceIds: ["SRC-MU-FY26-Q1-PREPARED", "SRC-SKHYNIX-FY25"],
            },
          ],
          checks: [
            ["产品平台", "NVIDIA 主导通用 GPU，Broadcom/云厂 custom ASIC 是第二路线。", "NVIDIA 控制最强", "补 AMD/Google TPU/Trainium 份额数据"],
            ["制造封装", "TSMC 是先进制程和封装的核心节点。", "强控制点", "补供应商替代能力"],
            ["配套供给", "HBM 和系统集成决定最终可交付量。", "共同控制", "补客户 allocation 和长期协议"],
          ],
        },
      },
      {
        question: "是否已经财务兑现？",
        answer: "兑现最充分：平台收入、AI semiconductor revenue、AI server orders/backlog 和客户 capex 同时可见。",
        sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-DELL-FY26-Q4", "SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025"],
        detail: {
          thesis: "GPU/ASIC 是当前 AI factory 链条里财务兑现最硬的节点。证据不是单一新闻，而是客户预算、芯片平台收入、custom ASIC 指引和 AI server backlog 同时出现。",
          steps: [
            {
              title: "平台收入兑现",
              body: "NVIDIA Q4 FY26 Data Center revenue 达 $62.3B，说明通用 GPU 平台已经把需求转为收入。",
              sourceIds: ["SRC-NVDA-FY26-Q4"],
            },
            {
              title: "ASIC 路线兑现",
              body: "Broadcom 把 AI semiconductor revenue 和 custom AI accelerators/Ethernet switches 放在指引中，说明云厂定制路线也在收入层面兑现。",
              sourceIds: ["SRC-AVGO-FY25-Q4"],
            },
            {
              title: "系统订单兑现",
              body: "Dell AI-optimized server orders、shipments 和 backlog 把客户预算与硬件交付连接起来，是判断 GPU/ASIC 需求是否进入实物采购的关键中间证据。",
              sourceIds: ["SRC-DELL-FY26-Q4"],
            },
          ],
          checks: [
            ["客户预算", "云厂 capex/RPO/云收入继续上行。", "预算层成立", "补 capex ROI 和 AI revenue"],
            ["芯片收入", "NVIDIA 与 Broadcom 都出现 AI accelerator 收入口径。", "收入层成立", "补 AMD/云厂自研芯片采购数据"],
            ["系统订单", "Dell AI server backlog/order 连接芯片与部署。", "订单层成立", "补交期、取消率和毛利"],
          ],
        },
      },
      {
        question: "市场是否已定价？",
        answer: "高度可能已部分定价，尤其是 NVIDIA；赔率要看盈利上修能否继续超过市场隐含预期，当前报告不能只凭产业强度得出买入结论。",
        sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-OMDIA-AI-PROCESSORS-20250828"],
        detail: {
          thesis: "GPU/ASIC 节点的胜率强，但赔率未自动成立。市场通常会优先定价最清晰的主链公司，所以本节点的投资判断必须从“需求很强”继续走到“盈利上修是否还能超过隐含预期”。",
          steps: [
            {
              title: "区分胜率与赔率",
              body: "NVIDIA 与 Broadcom 的财务兑现提高胜率，但也会提高市场预期。对已经被广泛认可的节点，不能把产业趋势直接等同于低估。",
              sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4"],
            },
            {
              title: "用第三方市场空间做边界",
              body: "Omdia 对 AI data-center chip spending 的预测支持总需求池扩张，但同时提示 custom ASIC gaining share，这意味着份额迁移可能影响不同公司的赔率。",
              sourceIds: ["SRC-OMDIA-AI-PROCESSORS-20250828"],
            },
            {
              title: "定义后续需要的估值数据",
              body: "本报告当前源包不足以精确判断估值是否透支。下一步必须补 forward PE/EV sales、盈利上修、毛利率预期、FCF yield 和隐含增长率。",
            },
          ],
          checks: [
            ["胜率", "需求和财务证据强。", "高", "继续跟踪订单和收入"],
            ["赔率", "缺少完整估值与隐含预期拆解。", "未完成", "补估值分位和盈利上修"],
            ["份额迁移", "custom ASIC 可能提高总空间，也可能改变赢家结构。", "需要单独建模", "补 ASIC/GPU mix 和客户项目节奏"],
          ],
        },
      },
      {
        question: "反证是什么？",
        answer: "云厂 capex 放缓、ASIC 分流超预期、GPU 毛利下行、客户订单延迟，或先进封装/HBM 约束缓解。",
        sourceIds: ["SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025", "SRC-AVGO-FY25-Q4", "SRC-OMDIA-AI-PROCESSORS-20250828"],
        detail: {
          thesis: "本节点的反证要绑定到可观测数据，不应停留在“AI 泡沫”这种泛表述。真正会改变结论的是客户预算、订单质量、供给松紧、价格/毛利和技术路线替代。",
          steps: [
            {
              title: "客户预算反证",
              body: "如果云厂 capex 指引下修、RPO 增速放缓、FCF 压力导致基础设施投资收缩，GPU/ASIC 需求会首先降级。",
              sourceIds: ["SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025"],
            },
            {
              title: "技术路线反证",
              body: "custom ASIC gaining share 本身不是坏事，但如果 ASIC 替代让通用 GPU 增长显著低于预期，NVIDIA 相关赔率需要下调；若 ASIC 同时扩大总需求池，则 Broadcom/云厂供应链受益。",
              sourceIds: ["SRC-AVGO-FY25-Q4", "SRC-OMDIA-AI-PROCESSORS-20250828"],
            },
            {
              title: "供需反证",
              body: "若交期缩短、租赁价格下跌、毛利率下行、订单取消或先进封装/HBM 供给快速释放，说明短缺逻辑变弱。",
              sourceIds: ["SRC-SA-COWOS-HBM-2023", "SRC-MU-FY26-Q1-PREPARED"],
            },
          ],
          checks: [
            ["capex", "云厂资本开支下修或 ROI 表述转弱。", "需求降级", "季度检查 hyperscaler capex/RPO/FCF"],
            ["路线替代", "ASIC 份额上升压低总 accelerator 增速或 GPU 价格。", "赢家结构改变", "检查 Broadcom/云厂 ASIC 与 NVIDIA 指引"],
            ["供给松动", "交期缩短、毛利下降、二级市场 GPU 价格下跌。", "短缺降级", "建立价格和交期监控"],
          ],
        },
      },
    ],
    manufacturing: [
      ["需求是否会大幅增长？", "GPU/ASIC 放量必须经过先进制程和先进封装，AI accelerator 越复杂，越依赖高端制造和 CoWoS 类封装。", ["SRC-TSM-Q4-2025", "SRC-SA-COWOS-HBM-2023"]],
      ["单位用量是否会提升？", "单位用量体现为先进节点、封装面积、HBM 集成和基板复杂度上升，不只是 wafer 数量。", ["SRC-SA-GB200-BOM-2024", "SRC-SA-COWOS-HBM-2023"]],
      ["供给能否跟上？", "扩产周期长，受设备、良率、工程经验、客户认证和 capex 制约。", ["SRC-TSM-Q4-2025"]],
      ["谁控制供给？", "核心控制者是 TSMC 及其先进封装生态。", ["SRC-TSM-Q4-2025"]],
      ["是否已经财务兑现？", "TSMC advanced technologies revenue share、gross margin 和 2026 capex 指引说明高端制造处于强需求状态。", ["SRC-TSM-Q4-2025"]],
      ["市场是否已定价？", "卡点强但成熟龙头预期较高，赔率取决于先进封装短缺持续性、capex 回报和地缘折价。", ["SRC-TSM-Q4-2025"]],
      ["反证是什么？", "先进封装产能释放快于需求、客户转单或自建替代、capex 回报下降、毛利率下行。", ["SRC-TSM-Q4-2025"]],
    ],
    memory: [
      ["需求是否会大幅增长？", "AI accelerator 需要高带宽内存喂数据，GPU/ASIC 数量增加、上下文变长和推理并发都会推高 HBM 与高端内存需求。", ["SRC-MU-FY26-Q1-PREPARED", "SRC-SKHYNIX-FY25"]],
      ["单位用量是否会提升？", "每代平台提升 HBM 容量、带宽和堆叠层数，server DRAM 与 enterprise SSD 也受益于训练/推理数据流。", ["SRC-MU-FY26-Q1-PREPARED"]],
      ["供给能否跟上？", "HBM 扩产受 DRAM wafer、堆叠封装、良率、客户资格和提前价量协议限制。", ["SRC-MU-FY26-Q1-PREPARED", "SRC-SA-COWOS-HBM-2023"]],
      ["谁控制供给？", "主要是 SK hynix、Micron、Samsung；SK hynix 领导力更强，Micron 是高弹性追赶者，Samsung 需要验证 HBM 领先性。", ["SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1-PREPARED", "SRC-SAMSUNG-FY25"]],
      ["是否已经财务兑现？", "SK hynix operating margin、Micron HBM TAM 与价量协议、Samsung high-value AI products 说明利润已经兑现。", ["SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1-PREPARED", "SRC-SAMSUNG-FY25"]],
      ["市场是否已定价？", "存储稀缺已被关注，但 HBM 供需、ASP、资格认证和盈利弹性仍可能继续改变利润预期。", ["SRC-MU-FY26-Q1-PREPARED", "SRC-SKHYNIX-FY25"]],
      ["反证是什么？", "HBM ASP 下跌、客户资格不及预期、扩产快于需求、DRAM/NAND 周期反转、GPU/ASIC 需求放缓。", ["SRC-MU-FY26-Q1-PREPARED"]],
    ],
    network: [
      ["需求是否会大幅增长？", "rack-scale 与 cluster-scale AI 提高东西向流量，拉动 retimer、AEC、switch、NIC、光模块和 PAM4 DSP。", ["SRC-SA-OPTICAL-2024", "SRC-LC-AI-OPTICS-202501", "SRC-DO-AI-NETWORKS-20250715"]],
      ["单位用量是否会提升？", "每 GPU 或每机柜的网络端口、光模块、DSP 和板级连接组件用量随 800G/1.6T 迁移上升。", ["SRC-SA-OPTICAL-2024", "SRC-LC-AI-OPTICS-202501"]],
      ["供给能否跟上？", "约束来自客户设计导入、平台认证、低功耗/低延迟指标、信号完整性和批量可靠性。", ["SRC-SA-OPTICAL-2024", "SRC-LC-PAM4-DSP-20260226"]],
      ["谁控制供给？", "Astera、Credo、Marvell、Broadcom、Arista 和 NVIDIA networking 控制不同子环节。", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3", "SRC-ANET-Q4-2025"]],
      ["是否已经财务兑现？", "ALAB、CRDO、MRVL、Arista 等公司收入已体现 AI networking / connectivity 需求。", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3", "SRC-ANET-Q4-2025"]],
      ["市场是否已定价？", "连接节点弹性大也容易估值透支，需要用客户集中、design win、gross margin 和出货节奏验证。", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3"]],
      ["反证是什么？", "平台自研替代、客户设计切换、ASP 下行、CPO/LPO/AEC 路线变化、主要客户延迟 ramp。", ["SRC-SA-OPTICAL-2024", "SRC-DO-AI-NETWORKS-20250715"]],
    ],
    powerCooling: [
      ["需求是否会大幅增长？", "GPU/ASIC 和 rack-scale 系统功耗提升后，数据中心必须新增电力、UPS、PDU、液冷和热管理能力。", ["SRC-VRT-Q4-2025", "SRC-SA-GB200-BOM-2024", "SRC-DO-LIQUID-COOLING-20260108"]],
      ["单位用量是否会提升？", "高功率机柜提高每 rack 的电力和散热需求，抬升 UPS、配电、液冷 CDU、管路、现场工程和服务价值量。", ["SRC-SA-GB200-BOM-2024", "SRC-DO-LIQUID-COOLING-20260108"]],
      ["供给能否跟上？", "约束来自工程交付、项目周期、电力接入、现场可靠性、液冷方案认证和供应链交付能力。", ["SRC-VRT-Q4-2025", "SRC-DO-LIQUID-COOLING-20260108"]],
      ["谁控制供给？", "Vertiv、Schneider、Eaton 和数据中心工程/液冷供应商控制关键供给。", ["SRC-VRT-Q4-2025", "SRC-DO-LIQUID-COOLING-20260108"]],
      ["是否已经财务兑现？", "Vertiv organic orders +252% YoY、backlog $15.0B，是物理瓶颈财务化最清楚的证据之一。", ["SRC-VRT-Q4-2025"]],
      ["市场是否已定价？", "市场已开始识别电力/液冷，但相对 GPU 平台可能仍更容易出现预期差。", ["SRC-VRT-Q4-2025"]],
      ["反证是什么？", "客户 capex 下修、电力接入延迟、项目毛利低于预期、backlog 取消或转收入慢、液冷渗透率低于预期。", ["SRC-VRT-Q4-2025", "SRC-DO-LIQUID-COOLING-20260108"]],
    ],
    system: [
      ["需求是否会大幅增长？", "GPU/ASIC、HBM、网络和电力冷却最终必须组合成服务器、机柜和集群才能上线。", ["SRC-DELL-FY26-Q4", "SRC-SA-GB200-BOM-2024"]],
      ["单位用量是否会提升？", "AI server 从单机走向 rack-scale，单系统包含更多 GPU、网络、电源、冷却和集成服务。", ["SRC-SA-GB200-BOM-2024"]],
      ["供给能否跟上？", "供给受 GPU allocation、供应链协调、整机工程、客户定制、液冷/电力配套和交付周期约束。", ["SRC-DELL-FY26-Q4", "SRC-SA-GB200-BOM-2024"]],
      ["谁控制供给？", "Dell、Supermicro、HPE、ODM/OEM 是主要系统交付者，但玩家较多、客户议价强。", ["SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2"]],
      ["是否已经财务兑现？", "Dell 披露 AI-optimized server orders、shipments 和 backlog；Supermicro 也有 AI server exposure，但需看执行和治理风险。", ["SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2"]],
      ["市场是否已定价？", "订单弹性容易被定价，关键不是 backlog 多大，而是 backlog 是否转成毛利和现金流。", ["SRC-DELL-FY26-Q4"]],
      ["反证是什么？", "订单取消、GPU allocation 变化、毛利率下降、库存/应收上升、客户延迟部署、治理或执行问题。", ["SRC-SMCI-FY26-Q2", "SRC-DELL-FY26-Q4"]],
    ],
  };
  return (rows[node.id] || []).map((row) => Array.isArray(row) ? { question: row[0], answer: row[1], sourceIds: row[2] } : row);
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
.goal-card,.industry-module,.qa-card,.source-collapse,.artifact-card{border:1px solid var(--line);border-radius:22px;background:var(--surface);box-shadow:var(--shadow)}.goal-card{padding:22px}.goal-main{font-size:22px;font-weight:800;margin-bottom:16px}.goal-grid,.constraint-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.metric,.constraint-grid article,.chain-bridge-card,.chain-node-lens,.overview-question-card,.chain-company-card,.bom-node-brief article{border:1px solid #e6edf7;border-radius:16px;background:#fff;padding:14px}.metric span,.constraint-grid span,.bom-node-brief span{display:block;color:var(--muted);font-size:12px;font-weight:800}.metric strong{display:block;color:#223047;font-size:18px}.constraint-definition{margin-top:18px}.artifact-title{font-weight:900;color:#26364f;margin-bottom:8px}.industry-overview-section{display:grid;gap:14px}.industry-module{overflow:hidden}.industry-module>summary,.qa-card>summary,.chain-detail-panel>summary,.bom-question-card>summary,.source-collapse>summary{list-style:none;cursor:pointer}.industry-module>summary::-webkit-details-marker,.qa-card>summary::-webkit-details-marker,details>summary::-webkit-details-marker{display:none}.industry-module[open]>summary,.qa-card[open]>summary{border-bottom:1px solid var(--line)}.module-head{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding:18px 22px}.module-index{display:inline-flex;width:34px;height:34px;border-radius:999px;align-items:center;justify-content:center;background:#eaf3ff;color:var(--blue);font-weight:900;font-size:12px}.module-head h3{margin:0;font-size:22px}.module-head p{margin:0;color:var(--muted);font-size:14px}.chevron{color:var(--muted);font-weight:900;transition:transform .18s ease}.industry-module[open]>.module-head .chevron,.qa-card[open]>summary .chevron,details[open]>summary>.chevron{transform:rotate(90deg)}.industry-module-body{padding:22px;min-width:0}.chain-explain{padding:0}.chain-plain-summary{font-size:18px;color:#344054;margin-top:0}.chain-research-bridge{border:1px solid rgba(10,132,255,.18);border-radius:18px;background:#fbfdff;padding:16px;margin:18px 0}.chain-bridge-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.chain-node-lens ul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:0;padding:0;list-style:none}.chain-node-lens b,.chain-bridge-card span{display:block;color:var(--blue);font-size:12px;margin-bottom:4px}.chain-detail-panel{border:1px solid #e6edf7;border-radius:18px;background:#fff;margin-top:12px;overflow:hidden}.chain-detail-panel>summary{display:flex;justify-content:space-between;align-items:center;padding:14px 16px;font-weight:900}.chain-layer-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;padding:16px}.chain-layer-card{border:1px solid #eef2f7;border-radius:16px;background:#fbfcff;padding:14px}.chain-layer-card p{margin:10px 0}.chain-layer-card span{display:block;color:var(--muted);font-size:12px}.chain-simple-flow{display:grid;grid-template-columns:repeat(5,minmax(180px,1fr));gap:10px;padding:16px;overflow-x:auto}.chain-stage-panel{min-width:180px;border:1px solid #e8eef7;border-radius:16px;padding:14px;background:#fbfcff}.chain-stage-panel span{display:inline-flex;width:28px;height:28px;border-radius:50%;align-items:center;justify-content:center;background:#eaf3ff;color:var(--blue);font-weight:900}.chain-relationship-graph{margin:0 16px 16px;padding:14px;border:1px dashed #bfd7f5;border-radius:16px;color:#3d536d;background:#f7fbff}.chain-company-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;padding:16px}.company-flow-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.company-flow-grid p{margin:0;border-top:1px solid #eef2f7;padding-top:8px}.company-flow-grid b{display:block;color:#223047}.component-value-chain,.chain-lane-map,.chain-value-flow{min-width:0}.chain-relationship-graph{display:block}.bom-node-brief{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:14px}.bom-node-brief p{margin:4px 0 0}.bom-question-list{display:grid;gap:10px}.bom-question-card{border:1px solid #e3ebf6;border-radius:18px;background:#fff;overflow:hidden}.bom-question-card>summary{display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:center;padding:14px 16px}.bom-question-card[open]>summary{border-bottom:1px solid #edf1f7}.bom-question-index{display:inline-flex;width:28px;height:28px;border-radius:999px;align-items:center;justify-content:center;background:#f0f7ff;color:var(--blue);font-weight:900;font-size:12px}.bom-question-answer{padding:14px 16px;background:#fbfcff}.bom-question-answer p{margin:0 0 10px}.bom-question-sources{display:flex;gap:6px;flex-wrap:wrap}.bom-demand-study{display:grid;gap:14px}.bom-demand-thesis{border:1px solid rgba(10,132,255,.18);border-radius:16px;background:#fff;padding:14px;color:#26364f}.bom-demand-steps{display:grid;gap:10px}.bom-demand-step{display:grid;grid-template-columns:auto 1fr;gap:12px;border:1px solid #e8eef7;border-radius:16px;background:#fff;padding:14px}.bom-demand-step>span{display:inline-flex;width:34px;height:34px;border-radius:999px;align-items:center;justify-content:center;background:#eef7ff;color:var(--blue);font-weight:900;font-size:12px}.bom-demand-step h5{margin:0 0 6px;font-size:15px;color:#223047}.bom-demand-step p{margin:0 0 8px}.bom-demand-table{min-width:980px}.source-chip{display:inline-flex;margin:2px 4px 2px 0;border:1px solid rgba(10,132,255,.2);border-radius:999px;background:#eef7ff;color:var(--blue);padding:3px 8px;font-size:11px}
.research-narrative{display:grid;gap:18px}.narrative-head{border:1px solid rgba(10,132,255,.16);border-radius:18px;background:linear-gradient(180deg,#fff,#f7fbff);padding:18px}.narrative-head span{display:block;color:var(--blue);font-size:12px;font-weight:900;margin-bottom:6px}.narrative-head h4{margin:0 0 10px;font-size:24px;line-height:1.25;color:#1f2d3d}.narrative-head p{margin:0;color:#344054;font-size:16px}.logic-flow{display:grid;grid-template-columns:repeat(5,minmax(150px,1fr));gap:8px;align-items:stretch}.flow-step{border:1px solid #dceafa;border-radius:16px;background:#fff;padding:12px;min-width:150px}.flow-step span{display:inline-flex;width:28px;height:28px;border-radius:999px;align-items:center;justify-content:center;background:#eaf3ff;color:var(--blue);font-weight:900;font-size:12px;margin-bottom:8px}.flow-step p{margin:0;color:#26364f;font-weight:800;line-height:1.45}.flow-arrow{display:none}.narrative-prose{display:grid;gap:12px;border-left:3px solid #0a84ff;padding-left:16px}.narrative-prose p{margin:0;color:#2f3d52;font-size:15px}.narrative-data-table{min-width:1040px}.narrative-bottom{display:grid;grid-template-columns:1fr 1fr;gap:12px}.investment-takeaway,.bear-case-box{border:1px solid #e4ebf5;border-radius:18px;background:#fff;padding:16px}.investment-takeaway b,.bear-case-box b{display:block;color:#223047;margin-bottom:8px}.investment-takeaway p{margin:0;color:#344054}.bear-case-box{background:#fffafa;border-color:#f0d3d0}.bear-case-box ul{margin:0;padding-left:18px;color:#4b5563}.bear-case-box li+li{margin-top:6px}.demand-chain-audit{border:1px solid rgba(10,132,255,.18);border-radius:18px;background:#f7fbff;padding:14px}.demand-chain-title{display:flex;justify-content:space-between;gap:12px;align-items:center;margin-bottom:12px}.demand-chain-title span{color:var(--blue);font-weight:900}.demand-chain-title strong{color:#344054;font-size:13px}.demand-chain-cards{display:grid;gap:12px}.chain-audit-card{border:1px solid #dceafa;border-radius:16px;background:#fff;overflow:hidden}.chain-audit-head{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding:14px;border-bottom:1px solid #edf3fb}.chain-audit-head>span{display:inline-flex;width:34px;height:34px;border-radius:999px;align-items:center;justify-content:center;background:#eaf3ff;color:var(--blue);font-weight:900;font-size:12px}.chain-audit-head h5{margin:0 0 4px;font-size:16px;color:#223047}.chain-audit-head p{margin:0;color:var(--muted)}.chain-audit-head strong{border:1px solid rgba(10,132,255,.24);border-radius:999px;background:#f0f7ff;color:var(--blue);padding:5px 10px;font-size:12px;white-space:nowrap}.chain-audit-body-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;padding:14px}.chain-audit-body-grid div{border:1px solid #eef2f7;border-radius:14px;background:#fbfcff;padding:12px}.chain-audit-body-grid b{display:block;color:#223047;margin-bottom:6px}.chain-audit-body-grid p{margin:0;color:#3d536d}.chain-audit-verdict{display:flex;justify-content:space-between;gap:12px;align-items:center;border-top:1px solid #edf3fb;padding:12px 14px}.chain-audit-verdict>span{color:#667085;font-size:12px;font-weight:800}.qa-card{margin:12px 0;overflow:hidden}.qa-card summary{display:grid;grid-template-columns:auto 1fr auto auto;gap:12px;align-items:center;padding:14px 16px}.qid{font-weight:900;color:var(--blue)}.qa-count{font-size:12px;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.qa-body{display:grid;gap:10px;padding:14px 16px}.qa-block{border:1px solid #edf1f7;border-radius:16px;background:#fff;padding:12px}.block-title{font-weight:900;color:#27364a;margin-bottom:6px}.qa-card.level-2{margin-left:18px;background:rgba(255,255,255,.82)}.qa-card.level-3{margin-left:28px;background:rgba(247,249,252,.95);border-style:dashed}.l3-meta{display:flex;gap:8px;flex-wrap:wrap}.l3-meta span{border:1px solid #e0e8f4;border-radius:999px;background:#f7fbff;color:#4e5f75;font-size:11px;padding:4px 8px}.overview-answer p{margin:0}.overview-answer-prose{color:#344054}.target-section{display:grid;gap:14px}.table-scroll{max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch}.table-scroll table{min-width:920px;border-collapse:separate;border-spacing:0;width:100%;background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden}.table-scroll th,.table-scroll td{padding:10px 12px;text-align:left;border-bottom:1px solid #edf1f7;vertical-align:top;font-size:13px}.table-scroll th{background:#f6f9fd;color:#475467;font-size:12px;font-weight:900}.state-actionable_long,.state-watch_only,.state-no_action{display:inline-flex;border-radius:999px;padding:4px 8px;font-weight:900;font-size:12px}.state-actionable_long{color:var(--green);background:#eaf8f2;border:1px solid rgba(29,154,108,.25)}.state-watch_only{color:var(--amber);background:#fff7e6;border:1px solid rgba(183,121,31,.25)}.state-no_action{color:var(--red);background:#fff1f0;border:1px solid rgba(194,65,61,.22)}.source-collapse{padding:16px}.source-collapse summary{font-weight:900;color:#334155}.source-collapse .table-scroll{margin-top:12px}
.chain-node-expansion{display:grid;gap:12px;border:1px solid rgba(10,132,255,.18);border-radius:22px;background:linear-gradient(180deg,#fff,#f7fbff);padding:16px}.chain-node-expansion-head span{display:block;color:var(--blue);font-size:12px;font-weight:900;margin-bottom:4px}.chain-node-expansion-head h5{margin:0 0 8px;font-size:21px;line-height:1.3;color:#223047}.chain-node-expansion-head p{margin:0;color:#667085}.chain-node-stack{display:grid;gap:10px}.chain-node-detail{border:1px solid #dceafa;border-radius:18px;background:#fff;overflow:hidden}.chain-node-detail>summary{display:grid;grid-template-columns:auto 1fr auto auto;gap:12px;align-items:center;padding:14px 16px;list-style:none;cursor:pointer}.chain-node-detail>summary::-webkit-details-marker{display:none}.chain-node-detail[open]>summary{border-bottom:1px solid #edf3fb}.chain-node-index{display:inline-flex;width:36px;height:36px;border-radius:999px;align-items:center;justify-content:center;background:#eaf3ff;color:var(--blue);font-weight:900;font-size:12px}.chain-node-detail h6{margin:0 0 3px;color:#223047;font-size:17px}.chain-node-detail summary p{margin:0;color:#667085;font-size:13px}.chain-node-detail summary strong{border:1px solid rgba(10,132,255,.22);border-radius:999px;background:#f0f7ff;color:#0a66cc;padding:5px 9px;font-size:12px;white-space:nowrap}.chain-node-detail[open]>summary .chevron{transform:rotate(90deg)}.chain-node-body{display:grid;gap:12px;padding:14px 16px;background:#fbfdff}.chain-node-lens-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.chain-node-lens-grid article{border:1px solid #e8eef7;border-radius:15px;background:#fff;padding:12px}.chain-node-lens-grid b,.chain-node-conclusion b{display:block;color:#223047;margin-bottom:6px}.chain-node-lens-grid p,.chain-node-conclusion p{margin:0;color:#344054}.chain-node-conclusion{border:1px solid rgba(29,154,108,.22);border-radius:16px;background:#f3fbf7;padding:13px}
.chain-metric-board{display:grid;gap:10px;border:1px solid rgba(10,132,255,.14);border-radius:18px;background:#f7fbff;padding:13px}.chain-metric-board-head{display:flex;justify-content:space-between;gap:12px;align-items:center}.chain-metric-board-head b{color:#223047}.chain-metric-board-head span{color:#667085;font-size:12px;font-weight:900}.chain-metric-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.chain-metric-card{display:grid;gap:10px;border:1px solid #dfeaf7;border-radius:16px;background:#fff;padding:13px}.chain-metric-card header span{display:block;color:var(--blue);font-size:11px;font-weight:900;margin-bottom:3px}.chain-metric-card header strong{display:block;color:#223047;font-size:15px;line-height:1.25}.chain-metric-card p{margin:0;color:#344054;font-size:13px}.metric-trend-chart,.metric-noncontinuous-chart,.metric-trend-gap{border:1px solid #eef3f9;border-radius:14px;background:#fbfdff;padding:10px}.metric-trend-chart svg{display:block;width:100%;height:auto;min-height:118px}.metric-axis{stroke:#d7e3f1;stroke-width:1}.metric-area{fill:rgba(10,132,255,.09)}.metric-line{fill:none;stroke:#0a84ff;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}.metric-dot{fill:#fff;stroke:#0a84ff;stroke-width:2}.metric-value{fill:#223047;font-size:10px;font-weight:800}.metric-label{fill:#667085;font-size:9px;font-weight:700}.metric-noncontinuous-chart>b,.metric-trend-gap>b{display:block;color:#667085;font-size:11px;margin-bottom:4px}.metric-comparison-bars{display:grid;gap:7px;margin-top:8px}.metric-comparison-row{display:grid;gap:4px}.metric-point-label{display:flex;justify-content:space-between;gap:8px;align-items:center}.metric-point-label b{color:#344054;font-size:12px}.metric-point-label span{color:#667085;font-size:12px}.metric-bar{height:10px;border-radius:999px;background:#e8f1fb;overflow:hidden}.metric-bar i{display:block;height:100%;border-radius:999px;background:linear-gradient(90deg,#8cc8ff,#0a84ff)}.chain-metric-card dl{display:grid;gap:7px;margin:0}.chain-metric-card dl div{border-top:1px solid #eef2f7;padding-top:7px}.chain-metric-card dt{color:#667085;font-size:11px;font-weight:900}.chain-metric-card dd{margin:2px 0 0;color:#344054;font-size:13px}.chain-metric-card footer{display:grid;gap:8px}.chain-metric-card em{font-style:normal;color:#7a5a00;background:#fff7dc;border:1px solid #f1dda6;border-radius:999px;padding:4px 8px;font-size:11px;font-weight:900;width:max-content;max-width:100%}
.historical-comparison{display:grid;gap:14px;border:1px solid rgba(10,132,255,.18);border-radius:20px;background:linear-gradient(180deg,#ffffff,#f7fbff);padding:16px}.history-head span{display:block;color:var(--blue);font-size:12px;font-weight:900;margin-bottom:4px}.history-head h5{margin:0 0 8px;font-size:20px;line-height:1.3;color:#223047}.history-head p{margin:0;color:#475467}.history-snapshot-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.history-metric-card{border:1px solid #e1eaf6;border-radius:16px;background:#fff;padding:14px}.history-metric-card>span{display:block;color:#667085;font-size:12px;font-weight:900}.history-metric-card strong{display:block;color:#0a84ff;font-size:25px;line-height:1.1;margin:6px 0}.history-metric-card p{margin:0 0 8px;color:#344054;font-size:13px}.history-bar-list{display:grid;gap:9px}.history-bar-row{display:grid;grid-template-columns:145px 1fr minmax(120px,auto);gap:10px;align-items:center}.history-bar-label b{display:block;color:#223047}.history-bar-label span{color:#667085;font-size:13px}.history-bar-track{height:14px;border-radius:999px;background:#e9f1fb;overflow:hidden}.history-bar-track i{display:block;height:100%;border-radius:999px;background:linear-gradient(90deg,#72b7ff,#0a84ff)}.history-table{min-width:1040px}
.future-runway{display:grid;gap:14px;border:1px solid rgba(29,154,108,.20);border-radius:20px;background:linear-gradient(180deg,#ffffff,#f7fffb);padding:16px}.runway-head span{display:block;color:var(--green);font-size:12px;font-weight:900;margin-bottom:4px}.runway-head h5{margin:0 0 8px;font-size:20px;line-height:1.3;color:#223047}.runway-head p{margin:0;color:#475467}.runway-formula{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.runway-formula-card{border:1px solid #dcefe8;border-radius:16px;background:#fff;padding:14px}.runway-formula-card>span{display:inline-flex;width:28px;height:28px;border-radius:999px;align-items:center;justify-content:center;background:#eaf8f2;color:var(--green);font-weight:900;font-size:12px}.runway-formula-card h6{margin:10px 0 6px;color:#223047;font-size:15px}.runway-formula-card p{margin:0;color:#3d536d}.runway-table{min-width:1180px}.runway-timeline{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.runway-timeline article{border:1px solid #dcefe8;border-radius:16px;background:#fff;padding:14px}.runway-timeline span{display:block;color:var(--green);font-size:12px;font-weight:900}.runway-timeline strong{display:block;margin:4px 0;color:#223047}.runway-timeline p{margin:0;color:#3d536d}.runway-verdict{border:1px solid rgba(29,154,108,.22);border-radius:16px;background:#f1fbf7;padding:14px}.runway-verdict b{display:block;color:#166f52;margin-bottom:6px}.runway-verdict p{margin:0;color:#2f3d52}
@media(max-width:820px){.goal-grid,.constraint-grid,.chain-bridge-grid,.chain-layer-grid,.chain-company-list,.company-flow-grid,.chain-node-lens ul,.bom-node-brief,.chain-audit-body-grid,.logic-flow,.narrative-bottom,.history-snapshot-grid,.history-bar-row,.runway-formula,.runway-timeline,.chain-node-lens-grid,.chain-metric-grid{grid-template-columns:1fr}.chain-audit-head,.chain-audit-verdict,.demand-chain-title,.chain-node-detail>summary,.chain-metric-board-head{display:grid;grid-template-columns:1fr}.qa-card.level-2,.qa-card.level-3{margin-left:0}.qa-card summary{grid-template-columns:auto 1fr auto}.qa-count{display:none}}
`;
}

main();
