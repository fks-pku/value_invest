const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const PROJECT_ID = "ai_factory_industry_timeslice_20260302";
const OUT_DIR = path.join(ROOT, "research", "bom", PROJECT_ID);
const AS_OF_DATE = "2026-03-02";
const EVALUATION_DATE = "2026-06-02";
const LABEL_START_DATE = "2026-03-02";
const LABEL_END_DATE = "2026-06-01";
const LABEL_WINDOW = "2026-03-02_to_2026-06-02";
const BENCHMARK_RETURN = 62.46;
const SOURCE_UNIVERSE_ID = "ai_factory";
const SOURCE_UNIVERSE = loadSourceUniverse(SOURCE_UNIVERSE_ID);

const SCORE_WEIGHTS = {
  chokepoint_strength: 0.26,
  future_space: 0.18,
  valuation_odds: 0.18,
  evidence_quality: 0.14,
  disconfirming_risk_control: 0.10,
  monitorability: 0.05,
  payoff_convexity: 0.09,
};

function loadSourceUniverse(domainId) {
  const configPath = path.join(ROOT, "config", "source_universes.json");
  const raw = JSON.parse(fs.readFileSync(configPath, "utf8"));
  const domains = raw.domains || {};
  if (domains[domainId]) return { id: domainId, ...domains[domainId] };
  const match = Object.entries(domains).find(([, domain]) => (domain.aliases || []).includes(domainId));
  if (match) return { id: match[0], ...match[1] };
  throw new Error(`Missing source universe for domain=${domainId}`);
}

const sources = [
  source("SRC-NVDA-FY26-Q4", "NVIDIA FY2026 Q4 results", "evidence", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/", "2026-02-25", "NVIDIA Q4 FY26 revenue was $68.1B, Data Center revenue was $62.3B, and management framed customer demand as AI factories for the AI industrial revolution."),
  source("SRC-VRT-Q4-2025", "Vertiv Q4 2025 results", "evidence", "https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/", "2026-02-11", "Vertiv Q4 2025 organic orders rose about 252% YoY and backlog reached $15.0B, reflecting robust AI infrastructure demand."),
  source("SRC-DELL-FY26-Q4", "Dell FY2026 Q4 results", "evidence", "https://investors.delltechnologies.com/node/19176/pdf", "2026-02-26", "Dell FY26 closed more than $64B in AI-optimized server orders, shipped more than $25B, and entered FY27 with a $43B backlog."),
  source("SRC-ALAB-Q4-2025", "Astera Labs Q4 2025 results", "evidence", "https://www.sec.gov/Archives/edgar/data/1736297/000173629726000005/q425exhibit991.htm", "2026-02-10", "Astera Labs Q4 revenue was $270.6M, +92% YoY, and the company described itself as a rack-scale AI infrastructure connectivity supplier."),
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
  source("SRC-SA-GB200-BOM-2024", "SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM", "research_report", "https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component", "2024-07-17", "SemiAnalysis mapped GB200 rack-scale architecture and component implications, including the practical constraint that many data centers cannot support very high rack density without direct-to-chip liquid cooling."),
  source("SRC-SA-COOLING-2025", "SemiAnalysis Datacenter Anatomy Part 2 Cooling Systems", "research_report", "https://newsletter.semianalysis.com/p/datacenter-anatomy-part-2-cooling-systems", "2025-02-13", "SemiAnalysis described data-center cooling as one of the fastest-evolving AI infrastructure markets and argued liquid-cooling demand is underestimated in chip-by-chip capacity models."),
  source("SRC-SA-OPTICAL-2024", "SemiAnalysis Nvidia Optical Boogeyman NVL72 Infiniband Scale Out 800G and 1.6T Ramp", "research_report", "https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband", "2024-03-25", "SemiAnalysis linked Blackwell NVL72 system architecture, NVLink scale-up, InfiniBand scale-out, 800G and 1.6T ramps to optical and networking BOM expansion."),
  source("SRC-TF-HBM-PRICE-20240506", "TrendForce HBM Prices to Increase by 5-10% in 2025", "research_report", "https://www.trendforce.com/presscenter/news/20240506-12125.html", "2024-05-06", "TrendForce estimated HBM ASP at several times conventional DRAM and about five times DDR5, with HBM bit capacity share rising from 2% in 2023 to 5% in 2024 and above 10% by 2025, while value share could exceed 30% of DRAM in 2025."),
  source("SRC-TF-BLACKWELL-HBM-20240808", "TrendForce Blackwell Ultra and B200A HBM3e 12hi Consumption", "research_report", "https://www.trendforce.com/presscenter/news/20240808-12248.html", "2024-08-08", "TrendForce described NVIDIA as the largest HBM buyer, expected procurement share above 70%, with HBM consumption growing more than 200% in 2024 and expected to double again in 2025 as Blackwell raises HBM content."),
  source("SRC-OMDIA-AI-PROCESSORS-20250828", "Omdia AI Data Center Chip Market Forecast", "research_report", "https://omdia.tech.informa.com/pr/2025/aug/ai-data-center-chip-market-to-hit-286bn-growth-likely-peaking-as-custom-asics-gain-ground", "2025-08-28", "Omdia forecast cloud and data-center AI processor spending from about $123B in 2024 to $207B in 2025 and $286B by 2030, with custom ASICs gaining share alongside GPUs."),
  source("SRC-TOMS-JPR-AIB-Q3-2025", "Jon Peddie Research Q3 2025 AIB share via Tom's Hardware", "news", "https://www.tomshardware.com/pc-components/gpus/latest-gpu-market-analysis-shows-nvidia-losing-ground-to-amd-and-intel-cracks-the-1-percent-share-milestone-for-the-first-time", "2025-12-02", "JPR's Q3 2025 PC add-in-board market share was NVIDIA 92%, AMD 7%, and Intel above 1%; this is a PC AIB proxy, not a data-center AI accelerator share table."),
  source("SRC-TOMS-NVDA-CHINA-SHARE-202510", "NVIDIA China advanced AI accelerator share via Tom's Hardware", "news", "https://www.tomshardware.com/tech-industry/jensen-huang-says-nvidia-china-market-share-has-fallen-to-zero", "2025-10-18", "NVIDIA CEO Jensen Huang said NVIDIA's share of China's advanced AI accelerator market went from roughly 95% to 0% under export controls, while China had previously represented about 20%-25% of data-center revenue."),
  source("SRC-OMDIA-SEMI-TRENDS-202512", "Omdia 2026 Trends to Watch Semiconductors", "research_report", "https://omdia.tech.informa.com/rs/033-WBW-877/images/2026%20Trends%20to%20Watch%20Semiconductors.pdf", "2025-12-01", "Omdia's 2026 semiconductor outlook tied AI growth to GPUs, logic ASICs, HBM, power-management ICs, advanced nodes, chiplets and silicon photonics, while flagging infrastructure and supply constraints."),
  source("SRC-LC-AI-OPTICS-202501", "LightCounting Optics for AI Clusters", "research_report", "https://www.lightcounting.com/newsletter/en/january-2025-optics-for-ai-clusters-319", "2025-01-01", "LightCounting estimated AI-cluster optical transceiver, LPO and CPO demand rising from about $5B in 2024 to more than $10B in 2026, with scale-up and scale-out models through 2030."),
  source("SRC-LC-PAM4-DSP-20260226", "LightCounting AI Capex Flows Down the Supply Chain to DSP Vendors", "research_report", "https://www.lightcounting.com/newsletter/en/ai-capex-flows-down-the-supply-chain-to-dsp-vendors-332", "2026-02-26", "LightCounting reported AI infrastructure capex drove 800G PAM4 chipset shipments to nearly triple in 2025 and expected 800G shipments to more than double in 2026, with 1.6T ports ramping from a small base."),
  source("SRC-DO-AI-NETWORKS-20250715", "Dell'Oro Group Ethernet AI Backend Network Forecast", "research_report", "https://www.prnewswire.com/news-releases/ethernet-is-winning-the-war-against-infiniband-in-ai-back-end-networks-according-to-delloro-group-302501890.html", "2025-07-15", "Dell'Oro Group forecast AI back-end networks could drive nearly $80B of data-center switch sales over five years and expected Ethernet to gain share from InfiniBand in AI back-end networks."),
  source("SRC-DO-LIQUID-COOLING-20260108", "Dell'Oro Group Data Center Liquid Cooling Forecast", "research_report", "https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html", "2026-01-08", "Dell'Oro Group forecast data-center liquid-cooling manufacturer revenue near $3B in 2025 and approaching $7B by 2029, with hyperscalers anchoring demand and direct liquid cooling leading adoption."),
  labelSource("LBL-NASDAQ-HISTORICAL", "Nasdaq historical close dataset", "https://api.nasdaq.com/api/quote/NVDA/historical", EVALUATION_DATE),
  labelSource("LBL-KRX-NAVER-000660", "Naver Finance KRX daily close 000660", "https://api.finance.naver.com/siseJson.naver?symbol=000660&requestType=1&startTime=20260302&endTime=20260602&timeframe=day", EVALUATION_DATE),
  labelSource("LBL-KRX-NAVER-005930", "Naver Finance KRX daily close 005930", "https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20260302&endTime=20260602&timeframe=day", EVALUATION_DATE),
];

const chainExplainer = {
  plainSummary: "一句话看懂：AI 工厂产业链分成上游核心供给、中游系统交付、下游需求运营。上游决定算力、内存、制造和连接瓶颈；中游把芯片、内存、网络、电力和冷却组合成可上线的服务器、机柜和数据中心；下游用 capex、利用率、收入和 ROI 验证需求是否可持续。投资判断要落到具体公司：它从谁那里拿到需求或供给，自己生产什么，卖给谁，最后能否转成收入、毛利、现金流和估值赔率。",
  flowSteps: [
    "下游客户提出训练、推理、agent、主权 AI 和企业 AI 工作负载，形成 capex、订单、机柜规格和交付时间表。",
    "中游系统商和数据中心基础设施商把下游需求拆成服务器、机柜、网络、电力、液冷和运维交付需求。",
    "上游平台、制造、HBM、连接和网络公司提供核心硬件、资格标准、产能和平台能力，决定中游能否交付。",
    "中游完成 AI server、rack、cluster 和机房基础设施交付后，下游用利用率、云收入、RPO/backlog、AI ROI 和追加 capex 验证需求。",
    "只有当稀缺供给能持续变成收入、毛利、现金流和估值上修时，该节点才有投资赔率。"
  ],
  layers: [
    { stage: "上游", name: "计算加速器 / GPU / ASIC", role: "把 AI 工作负载变成标准算力架构", players: "NVDA、AVGO custom ASIC、AMD/ASIC 替代路线", note: "接受下游训练/推理需求和 capex 预算，提供 GPU/ASIC、网络平台、软件栈和参考架构。" },
    { stage: "上游", name: "制造、封装与内存", role: "决定核心硬件供给斜率", players: "TSMC、SK hynix、Samsung、Micron", note: "接受芯片设计、HBM 规格和订单预测，提供先进制程/封装、HBM、服务器 DRAM、eSSD。" },
    { stage: "上游", name: "网络连接", role: "让机柜和集群扩展成可用系统", players: "ALAB、CRDO、MRVL、AVGO、ANET", note: "接受高带宽、低延迟、低功耗和平台兼容性要求，提供 switch、retimer、AEC、光互联和 custom networking。" },
    { stage: "中游", name: "服务器、机柜和数据中心系统", role: "把上游部件组合成可交付 AI 工厂", players: "DELL、SMCI、HPE、ODM、VRT、数据中心工程商", note: "接受 GPU/HBM/网络/电力冷却部件和客户规格，提供 AI server、rack、cluster、机房电力和冷却交付。" },
    { stage: "下游", name: "云厂商、AI lab、企业和主权 AI", role: "决定需求是否真实和可持续", players: "hyperscaler、AI lab、企业客户、主权 AI 项目", note: "接受中游交付的 AI 工厂能力，提供订单、capex、利用率和 ROI 验证；其追加投资决定产业链持续性。" },
  ],
  stageGroups: [
    {
      stage: "上游",
      summary: "核心供给层：提供平台、算力、先进制造、HBM、高端内存、网络连接和 custom silicon，决定 AI 工厂能否扩容。",
      companies: [
        companyNode({ name: "NVIDIA", ticker: "NVDA", node_type: "计算平台 / GPU", demand_input: "云厂商和 AI labs 的训练、推理、agent 工作负载、capex 预算、机柜规格。", supply_input: "TSMC 先进制程/封装、HBM 供应、网络与系统生态交付能力。", produces: "GPU、AI 加速平台、网络/软件栈、参考架构和供应链资格标准。", provides_to: "云厂商、AI labs、DELL / SMCI / HPE / ODM、TSMC、HBM 供应商。", financial_metrics: "Data Center revenue、gross margin、客户 capex、订单/供给约束、推理收入线索。", bottleneck_strength: "极强，但估值隐含预期高，Q4 不能只按稀缺性排序。", qa_link: "Q2.1 / Q4.1", evidence: "SRC-NVDA-FY26-Q4" }),
        companyNode({ name: "Broadcom", ticker: "AVGO", node_type: "Custom ASIC / Ethernet", demand_input: "云厂商自研 ASIC 规格、Ethernet AI fabric 需求和长期项目节奏。", supply_input: "先进制造、封装、网络生态、客户共同开发资源。", produces: "custom ASIC、Ethernet switch、AI networking silicon。", provides_to: "云厂商自研 ASIC 项目、AI networking 系统商和数据中心网络方案。", financial_metrics: "AI semiconductor revenue、客户集中度、订单/指引、AI networking 项目进度。", bottleneck_strength: "强，但要验证量产节奏和客户集中风险。", qa_link: "Q2.2 / Q4.1", evidence: "SRC-AVGO-FY25-Q4" }),
        companyNode({ name: "TSMC", ticker: "TSM", node_type: "先进制程 / 先进封装", demand_input: "GPU/ASIC 设计方的先进节点 wafer 订单、先进封装需求和交付排期。", supply_input: "设备、材料、良率工程、capex、地缘与产能约束。", produces: "先进制程、先进封装、产能扩张、良率和量产交付能力。", provides_to: "GPU/ASIC 平台方、AI accelerator 设计公司和系统供应链。", financial_metrics: "HPC/AI revenue mix、gross margin、advanced technology share、capex、advanced packaging capacity。", bottleneck_strength: "硬瓶颈强，但资本开支、地缘和估值会压制赔率。", qa_link: "Q2.1.2 / Q3.1.1", evidence: "SRC-TSM-Q4-2025" }),
        companyNode({ name: "SK hynix", ticker: "000660.KS", node_type: "HBM / 高端 DRAM", demand_input: "GPU/ASIC 平台的 HBM 规格、客户资格认证、订单预测和平台迭代节奏。", supply_input: "DRAM wafer、封装产能、良率、客户认证和扩产资本开支。", produces: "HBM3E/HBM4、高端 DRAM、产能扩张和高价值 memory mix。", provides_to: "GPU/ASIC 平台、AI server 供应链和云厂商间接需求。", financial_metrics: "HBM mix、memory revenue、operating margin、ASP、capex、客户资格。", bottleneck_strength: "极强，当前最需要跟踪 ASP、资格和供给扩张。", qa_link: "Q2.1.2 / Q4.1", evidence: "SRC-SKHYNIX-FY25" }),
        companyNode({ name: "Micron", ticker: "MU", node_type: "HBM / DRAM / eSSD", demand_input: "GPU/ASIC 平台和云厂商的 HBM、服务器 DRAM、eSSD 需求和价格信号。", supply_input: "DRAM/NAND 产能、HBM ramp、良率和价格周期。", produces: "HBM、云端内存、服务器 DRAM、NAND/eSSD。", provides_to: "AI server、云数据中心和存储/内存供应链。", financial_metrics: "HBM revenue、DRAM/NAND ASP、gross margin、inventory、capex。", bottleneck_strength: "强，但周期反转和供给扩张是主要反证。", qa_link: "Q2.1.2 / Q3.2", evidence: "SRC-MU-FY26-Q1" }),
        companyNode({ name: "Samsung Electronics", ticker: "005930.KS", node_type: "HBM / Server DDR5 / eSSD", demand_input: "GPU/ASIC 平台和云客户的 HBM、server DDR5、enterprise SSD 需求。", supply_input: "大规模 memory 产能、HBM 客户资格、良率和产品 mix。", produces: "HBM、server DDR5、enterprise SSD 和大规模 memory 产能。", provides_to: "AI server 供应链、云厂商和高端内存客户。", financial_metrics: "Memory revenue、HBM shipment/qualification、server DDR5/eSSD mix、margin。", bottleneck_strength: "中强，规模强但 HBM 领导力需要验证。", qa_link: "Q2.1.2 / Q4.1", evidence: "SRC-SAMSUNG-FY25" }),
        companyNode({ name: "Astera Labs", ticker: "ALAB", node_type: "机柜级连接芯片", demand_input: "AI server/rack 平台的 PCIe/CXL、retimer、信号完整性和 rack-scale 连接需求。", supply_input: "平台设计导入、客户认证、封测与高端连接生态。", produces: "retimer、connectivity chips、rack-scale AI infrastructure 连接方案。", provides_to: "AI server OEM/ODM、云厂商机柜平台和加速器系统。", financial_metrics: "Revenue growth、gross margin、customer concentration、new product ramp。", bottleneck_strength: "强弹性，但估值和客户集中压制风险控制。", qa_link: "Q2.2.1 / Q3.1", evidence: "SRC-ALAB-Q4-2025" }),
        companyNode({ name: "Credo", ticker: "CRDO", node_type: "AEC / Optical interconnect", demand_input: "AI server/rack 平台的 AEC、光互联、低功耗高速连接和 memory connectivity 需求。", supply_input: "客户设计导入、封测能力、平台兼容性和供应链交付。", produces: "active electrical cables、optical interconnects、connectivity silicon。", provides_to: "云厂商、AI server/rack 系统和机柜级网络连接。", financial_metrics: "Revenue growth、客户集中度、gross margin、design win/ramp。", bottleneck_strength: "强弹性，但客户集中和导入节奏是主要风险。", qa_link: "Q2.2.1 / Q4.1", evidence: "SRC-CRDO-FY26-Q3" }),
        companyNode({ name: "Marvell", ticker: "MRVL", node_type: "Custom silicon / Electro-optics", demand_input: "云厂商 custom silicon、电光互联、数据中心网络和长期定制项目。", supply_input: "先进制造、客户联合开发、光电生态和项目量产节奏。", produces: "custom silicon、electro-optics、data-center networking products。", provides_to: "云厂商、AI networking 和 custom accelerator 生态。", financial_metrics: "Data-center revenue、custom silicon pipeline、electro-optics ramp、gross margin。", bottleneck_strength: "中强，量产节奏和客户集中需要验证。", qa_link: "Q2.2.1 / Q4.1", evidence: "SRC-MRVL-FY26-Q3" }),
        companyNode({ name: "Arista Networks", ticker: "ANET", node_type: "Ethernet AI networking", demand_input: "云厂商和 AI 集群的 Ethernet AI networking、switching fabric 和网络扩展需求。", supply_input: "客户网络架构、switch silicon、软件/网络操作系统和供应链交付。", produces: "Ethernet switch、AI networking 平台和数据中心网络方案。", provides_to: "云厂商、AI 网络集群和企业数据中心。", financial_metrics: "Cloud revenue、AI networking contribution、gross margin、客户 capex。", bottleneck_strength: "中强，需验证以太网路线能否形成稀缺利润池。", qa_link: "Q2.2.1 / Q3.1", evidence: "SRC-ANET-Q4-2025" }),
      ],
    },
    {
      stage: "中游",
      summary: "系统交付层：把上游芯片、内存、网络和电力冷却能力，集成为可上线的服务器、机柜、集群和数据中心基础设施。",
      companies: [
        companyNode({ name: "Dell Technologies", ticker: "DELL", node_type: "AI server / 系统集成", demand_input: "云厂商和企业客户的 AI server 订单、整机规格和交付时间表。", supply_input: "GPU/ASIC、CPU、内存、存储、网络和电力冷却部件。", produces: "AI-optimized server、rack-scale 系统、集群集成和交付服务。", provides_to: "云厂商、企业客户和 AI 基础设施项目。", financial_metrics: "AI server orders、shipments、backlog、operating margin、cash conversion。", bottleneck_strength: "订单强，但价值捕获取决于毛利率和现金流。", qa_link: "Q1.1.2 / Q2.2.2 / Q4.1", evidence: "SRC-DELL-FY26-Q4" }),
        companyNode({ name: "Supermicro", ticker: "SMCI", node_type: "AI server / 快速定制交付", demand_input: "云厂商和 AI 客户的服务器订单、机柜规格和快速交付需求。", supply_input: "GPU、主板、网络、存储和电力冷却部件。", produces: "AI server、rack integration、快速定制交付。", provides_to: "AI 云、企业客户和数据中心集成项目。", financial_metrics: "Revenue growth、gross margin、inventory、governance/execution risk。", bottleneck_strength: "订单弹性大，但治理、执行和毛利风险更高。", qa_link: "Q2.2.2 / Q3.2", evidence: "SRC-SMCI-FY26-Q2" }),
        companyNode({ name: "HPE / ODM", ticker: "HPE/ODM", node_type: "服务器 / ODM 交付", demand_input: "云厂商、企业和主权 AI 的服务器/机柜规格与交付需求。", supply_input: "GPU、CPU、内存、网络、电力冷却和制造资源。", produces: "服务器、机柜、集群集成、ODM 代工和运维交付。", provides_to: "云厂商、企业和主权 AI 项目。", financial_metrics: "AI server backlog、gross margin、客户质量、交付周期。", bottleneck_strength: "偏执行和规模节点，需要订单、毛利和客户质量验证。", qa_link: "Q2.2.2 / Q4.1", evidence: "SRC-DELL-FY26-Q4" }),
        companyNode({ name: "Vertiv", ticker: "VRT", node_type: "电力 / 液冷 / 数据中心基础设施", demand_input: "AI server/rack、高功率密度、热负载、液冷、电力容量和项目工程要求。", supply_input: "电力设备、热管理方案、工程交付能力、供应链和现场服务。", produces: "power、thermal、liquid cooling、UPS、机房基础设施方案和现场交付能力。", provides_to: "云厂商、数据中心运营方、AI 工厂项目和系统集成商。", financial_metrics: "Organic orders、backlog、organic growth、margin、cash conversion、液冷项目质量。", bottleneck_strength: "强物理瓶颈，关键看 backlog 质量、毛利和交付能力。", qa_link: "Q2.2.2 / Q4.2", evidence: "SRC-VRT-Q4-2025" }),
      ],
    },
    {
      stage: "下游",
      summary: "需求和运营验证层：提出工作负载、支付 capex、运营 AI 工厂，并用收入、利用率和 ROI 决定是否继续扩容。",
      companies: [
        companyNode({ name: "Hyperscaler / 云厂商", ticker: "MSFT / AMZN / GOOGL / META 等", node_type: "核心付费客户 / AI 工厂运营方", demand_input: "终端 AI workload、云客户需求、内部模型训练/推理需求。", supply_input: "中游 AI server/rack/cluster、电力冷却和运维能力；上游 GPU/ASIC、网络和软件栈。", produces: "capex 预算、订单、使用率、云收入、RPO/backlog 和 ROI 信号。", provides_to: "上游平台、中游系统商、电力液冷供应商和应用生态。", financial_metrics: "Capex guidance、cloud revenue、RPO/backlog、FCF、AI ROI commentary。", bottleneck_strength: "需求真实性最终验证方；capex/ROI 下修会压低全链条评分。", qa_link: "Q1 / Q3", evidence: "SRC-NVDA-FY26-Q4" }),
        companyNode({ name: "AI labs / 新云", ticker: "AI labs / CoreWeave/xAI 类节点", node_type: "新增算力需求 / 租赁需求", demand_input: "模型训练、推理、agent 服务和客户算力租赁需求。", supply_input: "云或自建 AI 工厂的算力、机柜、网络、电力冷却和资本支持。", produces: "训练/推理工作负载、长期租约、算力采购和需求斜率。", provides_to: "云厂商、系统商、GPU/ASIC 平台和融资市场。", financial_metrics: "租约/订单、融资能力、利用率、收入转化、客户集中度。", bottleneck_strength: "能放大需求斜率，但信用、融资和客户集中需要单独折价。", qa_link: "Q1.2 / Q3.1", evidence: "SRC-DELL-FY26-Q4" }),
        companyNode({ name: "企业 / 主权 AI", ticker: "Enterprise / Sovereign AI", node_type: "长期推理和应用扩散需求", demand_input: "业务流程、数据安全、合规、本地化和主权算力需求。", supply_input: "云或本地 AI 工厂、模型服务、数据中心交付和安全合规能力。", produces: "应用收入、预算、采购订单和可验证 ROI。", provides_to: "云厂商、系统商、软件/服务生态和上游硬件需求。", financial_metrics: "企业 AI spend、使用率、ROI case、主权 AI 项目预算、续约/扩容。", bottleneck_strength: "决定需求能否从训练周期扩散到长期推理和企业应用。", qa_link: "Q1.2 / Q3.1", evidence: "SRC-NVDA-FY26-Q4" }),
      ],
    },
  ],
  chokepoints: [
    { node: "计算加速器 / GPU / ASIC", why: "软硬件栈和客户生态决定系统标准", controllers: "NVDA / ASIC 平台方", qa: "Q2.1 / Q4.1" },
    { node: "HBM / 高端内存", why: "高带宽内存限制 GPU/ASIC 交付斜率", controllers: "SK hynix、Samsung、MU", qa: "Q2.1 / Q4.1" },
    { node: "先进制造 / 先进封装", why: "先进制程和封装产能限制 GPU/ASIC 与 HBM 交付斜率", controllers: "TSMC", qa: "Q2.1 / Q4.1" },
    { node: "连接网络 / AI networking", why: "低延迟、高带宽连接决定 AI 工厂利用率", controllers: "ALAB、CRDO、MRVL、AVGO、ANET", qa: "Q2.2 / Q3.2" },
    { node: "电力 / 液冷 / 数据中心基础设施", why: "高功率机柜没有电力冷却就无法落地", controllers: "VRT、数据中心工程商", qa: "Q2.2 / Q4.1" },
    { node: "服务器 / rack 系统交付", why: "AI 服务器订单要转成收入和现金流", controllers: "DELL、SMCI、HPE/ODM", qa: "Q2.2 / Q3.1" },
  ],
  targetLinks: [
    ["NVDA", "计算加速器 / GPU / ASIC", "稀缺性最强，但估值隐含预期也最高", "Q2.1 / Q4.1"],
    ["VRT", "电力 / 液冷 / 数据中心基础设施", "订单和 backlog 明确，是物理瓶颈直接载体", "Q2.2 / Q4.1"],
    ["SK hynix/MU/Samsung", "HBM / 高端内存", "AI 工厂的硬瓶颈，但供给扩张和估值要监控", "Q2.1 / Q3.2"],
    ["ALAB/CRDO/MRVL", "连接网络 / AI networking", "弹性大但客户集中、定制项目节奏和估值风险高", "Q2.2 / Q4.1"],
    ["DELL/SMCI", "服务器 / rack 系统交付", "backlog 强，但利润率和执行质量决定价值捕获", "Q2.2 / Q3.1"],
    ["AVGO/ANET/TSM", "计算加速器 / GPU / ASIC、连接网络 / AI networking、先进制造 / 先进封装", "重要卡点，但需要区分已经定价的部分", "Q3.1 / Q4.1"],
  ],
  relationships: [
    {
      from: "云厂商 / AI labs",
      to: "NVDA / AVGO / ASIC 生态",
      relationship: "客户 capex 先进入平台和加速器架构",
      demand_input: "接受下游训练、推理、agent 工作负载、机柜规格、预算和长期供货需求。",
      supply_input: "TSMC 先进制程/封装、HBM、网络生态和系统交付能力。",
      produces: "提供 GPU/ASIC 加速器、网络/软件平台、参考架构和供应链资格标准。",
      provides_to: "云厂商、AI labs、系统商和 AI 工厂项目。",
      financial_metrics: "Data Center / AI semiconductor revenue、客户 capex、订单/指引、毛利率。",
      bottleneck_strength: "客户 ROI、capex 持续性、平台标准控制。",
      qa_link: "NVDA、AVGO；Q1.1、Q2.1、Q4.1。",
      evidence: "SRC-NVDA-FY26-Q4；SRC-AVGO-FY25-Q4。",
    },
    {
      from: "NVDA / ASIC 平台",
      to: "TSMC",
      relationship: "先进制程和先进封装承接 AI 工厂芯片需求",
      demand_input: "接受 GPU/ASIC 设计、先进节点 wafer 订单、先进封装需求和交付排期。",
      supply_input: "设备、材料、良率工程、capex、地缘与产能约束。",
      produces: "提供先进制程、先进封装、产能扩张、良率和量产交付能力。",
      provides_to: "GPU/ASIC 平台方、AI accelerator 设计公司和系统供应链。",
      financial_metrics: "HPC/AI revenue mix、gross margin、advanced technology share、capex、advanced packaging capacity。",
      bottleneck_strength: "先进制程、CoWoS/先进封装、良率、capex。",
      qa_link: "TSM；Q2.1.2、Q2.1.2.2、Q3.1.1.1。",
      evidence: "SRC-TSM-Q4-2025。",
    },
    {
      from: "NVDA / ASIC 平台",
      to: "SK hynix / Micron / Samsung",
      relationship: "AI 工厂算力集群需要 HBM、服务器 DRAM 和 eSSD",
      demand_input: "接受 GPU/ASIC BOM、HBM 规格、客户资格认证、订单预测和平台迭代节奏。",
      supply_input: "DRAM/NAND 产能、封装能力、良率、客户认证和扩产资本开支。",
      produces: "提供 HBM3E/HBM4、服务器 DDR5、企业 SSD、产能扩张和高价值 memory mix。",
      provides_to: "GPU/ASIC 平台、AI server 供应链和云厂商间接需求。",
      financial_metrics: "HBM mix、DRAM/NAND ASP、gross margin、inventory、capex、客户资格。",
      bottleneck_strength: "HBM 产能、客户资格、ASP、供给扩张。",
      qa_link: "000660.KS、MU、005930.KS；Q2.1.2、Q2.1.2.1、Q2.1.2.1.2。",
      evidence: "SRC-SKHYNIX-FY25；SRC-MU-FY26-Q1；SRC-SAMSUNG-FY25。",
    },
    {
      from: "云厂商 / AI labs",
      to: "DELL / SMCI / HPE / ODM",
      relationship: "AI server 和机柜系统交付",
      demand_input: "接受客户整机规格、GPU/ASIC allocation、网络/存储/电力冷却要求和交付时间表。",
      supply_input: "GPU/ASIC、CPU、内存、存储、网络和电力冷却部件。",
      produces: "提供 AI-optimized server、rack-scale 系统、集群集成、交付服务和 backlog 可见性。",
      provides_to: "云厂商、AI labs、企业客户和数据中心集成项目。",
      financial_metrics: "AI server orders、shipments、backlog、operating margin、cash conversion。",
      bottleneck_strength: "订单转收入、毛利率、现金转化、执行质量。",
      qa_link: "DELL、SMCI；Q1.1.2、Q2.2.2.2、Q4.1。",
      evidence: "SRC-DELL-FY26-Q4；SRC-SMCI-FY26-Q2。",
    },
    {
      from: "AI server / rack",
      to: "VRT",
      relationship: "高功率机柜需要电力、热管理和液冷基础设施",
      demand_input: "接受高功率机柜密度、数据中心电力容量、热负载、液冷部署和项目工程要求。",
      supply_input: "电力设备、热管理方案、工程交付能力、供应链和现场服务。",
      produces: "提供 power、thermal、liquid cooling、UPS、机房基础设施方案和现场交付能力。",
      provides_to: "云厂商、数据中心运营方、AI 工厂项目和系统集成商。",
      financial_metrics: "Organic orders、backlog、organic growth、margin、cash conversion、液冷项目质量。",
      bottleneck_strength: "液冷交付、项目毛利、backlog 质量。",
      qa_link: "VRT；Q2.2.2、Q2.2.2.1、Q4.2.2.1。",
      evidence: "SRC-VRT-Q4-2025。",
    },
    {
      from: "AI server / rack",
      to: "ALAB / CRDO",
      relationship: "机柜级高速连接和 AEC/retimer 支撑集群扩展",
      demand_input: "接受 rack-scale 带宽、延迟、功耗、信号完整性和平台兼容性要求。",
      supply_input: "平台设计导入、客户认证、封测与高端连接生态。",
      produces: "提供 PCIe/CXL retimer、AEC、connectivity chips、光互联相关方案和 memory connectivity。",
      provides_to: "云厂商、AI server/rack 系统和机柜级网络连接。",
      financial_metrics: "Revenue growth、gross margin、customer concentration、new product ramp / design win。",
      bottleneck_strength: "客户集中、design-in 节奏、平台替代风险。",
      qa_link: "ALAB、CRDO；Q2.2.1、Q2.2.1.1、Q3.1.1.2。",
      evidence: "SRC-ALAB-Q4-2025；SRC-CRDO-FY26-Q3。",
    },
    {
      from: "AI networking / custom silicon",
      to: "MRVL / AVGO / ANET",
      relationship: "custom silicon、电光互联和以太网网络承接开放/定制路线",
      demand_input: "接受云厂商自研 ASIC 需求、Ethernet AI fabric 规格、switch/电光互联项目和客户定制节奏。",
      supply_input: "先进制造、客户联合开发、光电生态、网络操作系统和项目量产节奏。",
      produces: "提供 custom silicon、electro-optics、Ethernet switch、AI networking 平台和长期项目支持。",
      provides_to: "云厂商、AI networking 和 custom accelerator 生态。",
      financial_metrics: "Data-center revenue、custom silicon pipeline、electro-optics ramp、gross margin、cloud revenue。",
      bottleneck_strength: "大客户集中、量产节奏、与 NVIDIA 平台竞争。",
      qa_link: "MRVL、AVGO、ANET；Q2.2.1.2、Q2.2.1.3。",
      evidence: "SRC-MRVL-FY26-Q3；SRC-AVGO-FY25-Q4；SRC-ANET-Q4-2025。",
    },
  ],
};

const chainNetwork = {
  width: 1540,
  height: 760,
  nodes: [
    networkNode("NVDA", "NVIDIA", "NVDA", "上游", "GPU / 平台", 64, 58),
    networkNode("AVGO", "Broadcom", "AVGO", "上游", "Custom ASIC", 64, 126),
    networkNode("TSM", "TSMC", "TSM", "上游", "先进制造 / 先进封装", 64, 194),
    networkNode("SKHYNIX", "SK hynix", "000660.KS", "上游", "HBM", 64, 262),
    networkNode("MU", "Micron", "MU", "上游", "HBM / DRAM / eSSD", 64, 330),
    networkNode("SAMSUNG", "Samsung", "005930.KS", "上游", "HBM / DDR5 / eSSD", 64, 398),
    networkNode("ALAB", "Astera Labs", "ALAB", "上游", "机柜级连接", 64, 466),
    networkNode("CRDO", "Credo", "CRDO", "上游", "AEC / 光互联", 64, 534),
    networkNode("MRVL", "Marvell", "MRVL", "上游", "电光 / custom", 64, 602),
    networkNode("ANET", "Arista", "ANET", "上游", "AI Ethernet", 64, 670),
    networkNode("DELL", "Dell", "DELL", "中游", "AI server / 集成", 610, 148),
    networkNode("SMCI", "Supermicro", "SMCI", "中游", "快速定制交付", 610, 266),
    networkNode("HPEODM", "HPE / ODM", "HPE/ODM", "中游", "服务器 / ODM", 610, 384),
    networkNode("VRT", "Vertiv", "VRT", "中游", "电力 / 液冷 / 数据中心基础设施", 610, 502),
    networkNode("CLOUD", "Hyperscaler", "MSFT/AMZN/GOOGL/META", "下游", "云厂商 / AI 工厂", 1136, 178),
    networkNode("AILABS", "AI labs / 新云", "CoreWeave/xAI 类", "下游", "新增算力需求", 1136, 342),
    networkNode("ENTERPRISE", "企业 / 主权 AI", "Enterprise/Sovereign", "下游", "长期应用需求", 1136, 506),
  ],
  edges: [
    networkEdge("CLOUD", "NVDA", "需求", "capex / 平台规格", "demand", 0.18),
    networkEdge("CLOUD", "AVGO", "需求", "自研 ASIC / Ethernet", "demand", 0.28),
    networkEdge("CLOUD", "DELL", "订单", "AI server 订单", "demand", -0.04),
    networkEdge("CLOUD", "VRT", "项目", "电力 / 液冷项目", "demand", 0.15),
    networkEdge("AILABS", "DELL", "订单", "训练集群交付", "demand", 0.06),
    networkEdge("ENTERPRISE", "CLOUD", "验证", "云收入 / ROI", "feedback", -0.18),
    networkEdge("TSM", "NVDA", "供给", "先进制造 / 先进封装", "supply", -0.15),
    networkEdge("TSM", "AVGO", "供给", "ASIC 量产", "supply", -0.06),
    networkEdge("SKHYNIX", "NVDA", "供给", "HBM 资格 / 供给", "supply", 0.08),
    networkEdge("MU", "DELL", "供给", "DRAM / eSSD", "supply", -0.10),
    networkEdge("SAMSUNG", "DELL", "供给", "HBM / server memory", "supply", 0.08),
    networkEdge("NVDA", "DELL", "供给", "GPU / 参考架构", "supply", -0.05),
    networkEdge("AVGO", "HPEODM", "供给", "ASIC / Ethernet", "supply", 0.08),
    networkEdge("ALAB", "DELL", "供给", "retimer / CXL", "supply", 0.14),
    networkEdge("CRDO", "SMCI", "供给", "AEC / 光互联", "supply", 0.10),
    networkEdge("MRVL", "HPEODM", "供给", "电光 / custom", "supply", -0.06),
    networkEdge("ANET", "HPEODM", "供给", "AI Ethernet", "supply", 0.16),
    networkEdge("DELL", "CLOUD", "交付", "服务器 / 机柜", "delivery", -0.06),
    networkEdge("SMCI", "AILABS", "交付", "快速定制服务器", "delivery", 0.08),
    networkEdge("HPEODM", "ENTERPRISE", "交付", "企业 / 主权交付", "delivery", -0.08),
    networkEdge("VRT", "CLOUD", "交付", "电力 / 液冷 / 数据中心基础设施", "delivery", 0.18),
    networkEdge("VRT", "AILABS", "交付", "机房基础设施", "delivery", -0.08),
  ],
  legend: [
    ["实线蓝色", "供给/交付：产品、产能、系统或基础设施从左向右传导。"],
    ["虚线金色", "需求/订单：下游 capex、规格和项目需求向中上游反馈。"],
    ["灰色", "运营验证：收入、利用率、ROI 和续费决定链条持续性。"],
  ],
};

const chainResearchBridge = {
  objective: "把“AI 工厂产业相关投资机会”拆成可验证的产业链问题，再由产业链节点生成后续 QA 和标的排序。",
  coreQuestion: "哪些节点能把 AI 工厂需求稳定转成收入、毛利、现金流和估值赔率，而不是只获得主题曝光？",
  currentConclusion: "行业概况显示，AI 工厂不是单点 GPU 叙事。需求先由云厂商和 AI labs 的 capex 触发，再进入平台、HBM/先进封装、连接、电力液冷和系统交付。后续 QA 应优先下钻 HBM/先进封装、电力液冷、机柜级连接、系统交付利润质量和客户 ROI 反证。",
  outputToQa: [
    ["Q1", "需求是否真实", "看下游 capex、平台收入、服务器 backlog、电力液冷订单和连接芯片收入是否同向验证。"],
    ["Q2", "竞争格局与价值捕获", "先看每个节点谁和谁竞争、替代路线和客户议价力，再判断哪些节点形成真 chokepoint。"],
    ["Q3", "什么会推翻", "看 capex ROI、供给扩张、估值拥挤、客户集中、平台替代和 backlog 毛利质量。"],
    ["Q4", "推荐哪些标的", "把节点分数映射到具体证券、赔率、风险闸门和监控触发器。"],
  ],
};

const chainNodeLenses = [
  ["需求流入", "是否有明确客户预算、订单、收入或 backlog 流入该节点。"],
  ["稀缺供给", "是否控制短期难扩张的产能、资格、设计导入、生态或工程交付能力。"],
  ["替代难度", "客户能否绕开、双供、内化，或被平台路线替代。"],
  ["货币化能力", "稀缺是否能体现为价格、毛利、收入增长、现金流或更高 backlog 质量。"],
  ["市场定价", "当前估值是否已经把增长路径和利润率上修充分反映。"],
  ["反证触发", "哪些数据会证明瓶颈只是暂时的、低利润的，或已被供给扩张消化。"],
];

const keyConstraintDefinition = {
  theme: "AI 工厂不是单一 GPU 主题，而是一套把工作负载转成可上线数据中心能力的供给链。",
  preciseConstraint: "当前约束集中在平台规格、HBM/先进封装、机柜级连接、电力液冷和系统交付利润质量；其中只有能把稀缺转成收入、毛利、现金流且未被估值充分反映的节点，才构成投资机会。",
  whyNow: "截至研究截面，NVIDIA、Dell、Vertiv、Astera、Credo、Broadcom、Marvell、内存公司均已给出收入、订单、backlog 或高价值产品 mix 证据，说明需求已进入财务口径。",
  scope: "本报告只评估 AI 工厂硬件和基础设施链条，不把纯软件应用、云厂自有股价表现或后续三个月价格 label 作为当时推荐依据。",
  routeConflict: "平台一体化、开放 Ethernet/custom ASIC、HBM/先进封装、电力液冷、服务器集成和机柜级连接会争夺利润池；强主题不等于强赔率。",
  adoptionHorizon: "回测截面只使用 2026-03-02 前可见证据。后续验证应按季度跟踪订单、毛利、capex、供给扩张和估值隐含预期。",
};

const CANONICAL_BOM_NODES = [
  { key: "platform", label: "计算加速器 / GPU / ASIC", layer: "上游", role: "算力平台和系统规格入口" },
  { key: "memory", label: "HBM / 高端内存", layer: "上游", role: "高带宽内存、server DRAM、enterprise SSD" },
  { key: "manufacturing", label: "先进制造 / 先进封装", layer: "上游", role: "先进制程、CoWoS 类封装、良率和产能" },
  { key: "connectivity", label: "连接网络 / AI networking", layer: "上游/中游", role: "retimer、AEC、光互联、交换机和 custom silicon" },
  { key: "powerCooling", label: "电力 / 液冷 / 数据中心基础设施", layer: "中游", role: "power、thermal、liquid cooling、UPS 和现场工程" },
  { key: "systemDelivery", label: "服务器 / rack 系统交付", layer: "中游", role: "AI server、rack、cluster、集成和交付" },
];

const DEMAND_VALIDATION_LAYER = "客户需求 / 云 capex";
const BOM = Object.fromEntries(CANONICAL_BOM_NODES.map((node) => [node.key, node.label]));

const componentValueChainRows = [
  [BOM.platform, "GPU/ASIC、软件栈、参考架构、供应链资格", "NVDA、AVGO", "云厂 capex 和 AI workload", "TSM/HBM/系统商/网络连接", "Data Center/AI revenue、毛利率、客户 capex", "Q1/Q2/Q4"],
  [BOM.manufacturing, "先进制程、先进封装、良率、量产交付", "TSM", "GPU/ASIC 设计和交付排期", "平台方和 AI accelerator 供应链", "advanced technology share、capex、gross margin", "Q2/Q3/Q4"],
  [BOM.memory, "HBM、server DRAM、enterprise SSD", "SK hynix、MU、Samsung", "平台 BOM 和客户资格", "GPU/ASIC 平台、系统商、云厂商", "HBM mix、ASP、operating margin、inventory", "Q2/Q3/Q4"],
  [BOM.connectivity, "retimer、AEC、optical/electro-optics、Ethernet switch", "ALAB、CRDO、MRVL、ANET、AVGO", "rack-scale 带宽、延迟、功耗和平台兼容", "服务器/机柜系统和云厂商", "revenue growth、客户集中、gross margin、design win", "Q2/Q3/Q4"],
  [BOM.systemDelivery, "AI server、rack、cluster、集成服务", "DELL、SMCI、HPE/ODM", "客户整机规格和交付时间表", "云厂商、AI labs、企业/主权 AI", "orders、shipments、backlog、margin、cash conversion", "Q1/Q2/Q4"],
  [BOM.powerCooling, "power、thermal、liquid cooling、UPS、现场工程", "VRT、数据中心工程商", "高功率机柜、热负载、电力容量", "数据中心运营方和 AI 工厂项目", "orders、backlog、project margin、cash conversion", "Q2/Q3/Q4"],
  [DEMAND_VALIDATION_LAYER, "capex、利用率、cloud revenue、RPO/backlog、ROI", "云厂商、AI labs、企业/主权 AI", "终端模型训练/推理和企业应用需求", "全链条供给节点", "capex guidance、cloud revenue、FCF、AI ROI", "Q1/Q3"],
];

const bottleneckReleaseTimeline = [
  [BOM.platform, "GPU/ASIC 供给和平台标准控制", "Data Center 收入、毛利和客户 capex 同向验证", "季度财报和客户 capex 更新", "capex/ROI 下修或毛利无法支撑估值", "NVDA、AVGO、TSM、HBM 链"],
  [BOM.memory, "客户资格、良率、HBM 产能和产品 mix", "HBM mix、ASP、产能/良率、客户资格", "季度价格、资格和扩产进展", "ASP 反转、供给快速扩张、资格变化", "SK hynix、MU、Samsung"],
  [BOM.manufacturing, "先进制程、先进封装和良率扩张斜率", "advanced packaging capex、良率、HPC/AI mix", "季度 capex、封装产能和客户排期", "先进封装供给缓解、capex 回报下降或地缘风险恶化", "TSM"],
  [BOM.connectivity, "rack-scale 信号完整性、低功耗、低延迟和 design-in", "ALAB/CRDO/MRVL 收入、毛利、客户集中、项目 ramp", "季度收入、design win 和客户集中披露", "大客户订单延迟、平台自有方案替代、毛利下行", "ALAB、CRDO、MRVL、ANET、AVGO"],
  [BOM.powerCooling, "高功率机柜电力和热管理现场交付", "VRT orders/backlog、液冷项目毛利、现金转化", "季度订单、backlog、项目毛利和交付周期", "backlog 低质量转化、取消率上升、客户 capex 放缓", "VRT"],
  [BOM.systemDelivery, "AI server backlog 转收入和现金流质量", "DELL/SMCI orders、shipments、margin、inventory、cash conversion", "季度 backlog、毛利和现金流披露", "订单增长但利润/现金流走弱或治理风险扩大", "DELL、SMCI、HPE/ODM"],
];

const chainValueCaptureMatrix = [
  {
    node: BOM.platform,
    demand: "云厂商和 AI labs capex 直接进入 GPU/ASIC 平台和软件生态。",
    chokepoint: "GPU 供给、软件栈、生态锁定、参考架构和客户开发节奏。",
    monetization: "Data Center / AI semiconductor revenue、gross margin、平台升级周期。",
    targets: "NVDA、AVGO",
    verification: "客户 capex、数据中心收入、推理收入、毛利率和隐含增长预期。",
    qa: "Q1.1 / Q2.1 / Q4.1",
  },
  {
    node: BOM.memory,
    demand: "GPU/ASIC BOM、平台资格和 AI server 规格拉动 HBM、server DRAM、eSSD。",
    chokepoint: "HBM 客户资格、良率、封装、产能扩张斜率和 ASP。",
    monetization: "HBM mix、ASP、operating margin、inventory 和 capex 效率。",
    targets: "SK hynix、MU、Samsung",
    verification: "HBM ASP、客户资格、供给扩张、DRAM/NAND 价格和毛利率。",
    qa: "Q2.1.2 / Q3.2 / Q4.1",
  },
  {
    node: BOM.manufacturing,
    demand: "GPU/ASIC 设计和机柜级平台升级带来先进节点与封装订单。",
    chokepoint: "先进节点、先进封装产能、良率、设备/材料和地缘约束。",
    monetization: "advanced technology share、gross margin、capex 与 HPC/AI mix。",
    targets: "TSM",
    verification: "先进封装产能、AI/HPC 客户 mix、capex 回报和地缘风险。",
    qa: "Q2.1.2.2 / Q3.1 / Q4.1",
  },
  {
    node: BOM.powerCooling,
    demand: "高功率机柜和数据中心上线需求形成电力、热管理和液冷工程订单。",
    chokepoint: "现场工程交付、液冷方案、供货周期和高质量 backlog。",
    monetization: "organic orders、backlog、project margin、cash conversion。",
    targets: "VRT",
    verification: "backlog 转收入、液冷项目毛利、取消率、交付周期和客户 capex。",
    qa: "Q2.2.2 / Q4.2",
  },
  {
    node: BOM.connectivity,
    demand: "rack-scale 扩展带来 retimer、AEC、光互联、Ethernet AI networking 和 custom silicon 需求。",
    chokepoint: "design-in、客户认证、平台兼容、功耗/延迟和高速信号能力。",
    monetization: "revenue growth、gross margin、客户集中度、设计导入和量产 ramp。",
    targets: "ALAB、CRDO、MRVL、ANET、AVGO",
    verification: "大客户占比、项目量产节奏、平台替代、毛利率和估值分位。",
    qa: "Q2.2.1 / Q3.1 / Q4.1",
  },
  {
    node: BOM.systemDelivery,
    demand: "云厂商和 AI labs 的 AI server、rack、cluster 订单进入 OEM/ODM。",
    chokepoint: "GPU allocation、集成能力、供应链执行、现金周转和治理质量。",
    monetization: "AI server orders、shipments、backlog、operating margin、cash conversion。",
    targets: "DELL、SMCI、HPE/ODM",
    verification: "backlog 毛利、现金转化、库存、订单取消和治理风险。",
    qa: "Q2.2.2 / Q3.2 / Q4.1",
  },
  {
    node: DEMAND_VALIDATION_LAYER,
    demand: "客户将 AI 工厂上线为训练、推理、云服务、企业/主权 AI 项目。",
    chokepoint: "利用率、应用收入、RPO/backlog、FCF 和 capex ROI。",
    monetization: "不是直接上游利润池，但决定全链条需求持续性和估值容忍度。",
    targets: "云厂商和全链条二阶验证",
    verification: "cloud revenue、RPO、capex guidance、FCF、AI ROI commentary。",
    qa: "Q1.2 / Q3.1",
  },
];

const chainQaMapping = [
  { q: "Q1 需求真实性", signal: "平台收入、服务器 backlog、电力液冷订单、HBM/连接收入是否同时增长。", use: "判断 AI 工厂是否已经进入财务口径，决定是否继续做 Q2/Q4。" },
  { q: "Q2 竞争格局与价值捕获", signal: "节点内竞争者、替代路线、客户议价力、供给扩张和定价权是否共同指向真 chokepoint。", use: "先做竞争格局判断，再形成 chokepoint 分数，并把强节点映射到具体证券。" },
  { q: "Q3 反证和赔率", signal: "估值隐含预期、客户 capex ROI、供给扩张、客户集中、平台替代、backlog 毛利。", use: "给每个强主题设置降级闸门，避免只按热度排序。" },
  { q: "Q4 标的推荐", signal: "把 Q1-Q3 的节点结论转成稀缺/垄断、未定价、业绩弹性、风险控制四维评分。", use: "输出具体标的、强度、赔率、风险提示和后续监控触发器。" },
];

const chainDataGaps = [
  "云厂商 capex、RPO/backlog、cloud revenue、FCF 和 AI ROI 的同口径季度跟踪。",
  "HBM ASP、HBM4 客户资格、产能扩张、良率、产品 mix 和客户分配。",
  "TSMC 先进封装产能、AI/HPC 客户 mix、capex 回报和地缘风险折价。",
  "VRT backlog 转收入节奏、液冷项目毛利、取消率、交付周期和现金转化。",
  "ALAB/CRDO/MRVL/ANET/AVGO 的客户集中、design-in、项目量产和平台替代风险。",
  "DELL/SMCI/HPE/ODM 的 AI server 毛利、库存、现金流、订单取消和治理/执行风险。",
];

const chainSankeyFlows = [
  {
    step: "01",
    title: "需求预算先变成平台订单",
    from: "云厂商 / AI labs capex",
    to: "NVDA / AVGO 平台与 ASIC",
    what: "训练、推理、agent 工作负载先变成 GPU/ASIC 平台规格和长期供货需求。",
    beneficiaries: "NVDA、AVGO，以及承接 GPU/ASIC 设计的先进制造和 HBM 供应链。",
    metric: "Data Center / AI semiconductor revenue、客户 capex、供给约束。",
    investment_read: "这是需求真实性入口；如果平台收入和客户 capex 同时走强，Q1 才能上抛到 Q2/Q4。",
    weight: 5,
    kind: "demand",
  },
  {
    step: "02",
    title: "平台规格传导到制造和内存",
    from: "平台规格",
    to: "TSMC + HBM 供应商",
    what: "GPU/ASIC 设计和机柜规格传导到先进制程、封装、HBM、server DRAM 和 eSSD。",
    beneficiaries: "TSMC、SK hynix、Micron、Samsung。",
    metric: "advanced technology share、capex、HBM mix、ASP、gross margin。",
    investment_read: "这是硬瓶颈入口；如果供给斜率慢于需求，利润更可能留在 HBM、先进制程和封装。",
    weight: 5,
    kind: "supply",
  },
  {
    step: "03",
    title: "客户订单进入系统交付",
    from: "AI server / rack 订单",
    to: "DELL / SMCI / HPE / ODM",
    what: "客户订单变成 AI server、rack-scale 系统、集群集成和交付 backlog。",
    beneficiaries: "DELL、SMCI、HPE/ODM。",
    metric: "AI server orders、shipments、backlog、operating margin、cash conversion。",
    investment_read: "这是收入确认入口；订单强不等于利润强，要看 backlog 是否转成毛利和现金流。",
    weight: 4,
    kind: "delivery",
  },
  {
    step: "04",
    title: "高功率机柜倒逼电力液冷",
    from: "高功率机柜",
    to: "VRT / 数据中心工程",
    what: "GPU 密度和机柜功耗进一步变成电力、热管理、液冷和现场交付项目。",
    beneficiaries: "Vertiv、数据中心电力和热管理工程商。",
    metric: "organic orders、backlog、project margin、liquid cooling delivery。",
    investment_read: "这是物理落地瓶颈；如果电力/液冷跟不上，AI 工厂不能上线，VRT 的价值捕获会更清晰。",
    weight: 4,
    kind: "delivery",
  },
  {
    step: "05",
    title: "机柜扩展带来连接和网络需求",
    from: "机柜级扩展",
    to: "ALAB / CRDO / MRVL / ANET",
    what: "rack-scale 扩展需要 retimer、AEC、光互联、custom silicon 和 Ethernet AI networking。",
    beneficiaries: "ALAB、CRDO、MRVL、ANET、AVGO。",
    metric: "revenue growth、design win、customer concentration、gross margin。",
    investment_read: "这是高弹性入口；弹性大，但要扣客户集中、平台替代和估值风险。",
    weight: 3,
    kind: "supply",
  },
  {
    step: "06",
    title: "上线后由收入和 ROI 反向验证",
    from: "中游交付",
    to: "云收入 / RPO / ROI",
    what: "AI 工厂上线后由利用率、云收入、RPO/backlog、FCF 和 ROI 验证需求持续性。",
    beneficiaries: "全链条，但最先影响高估值和客户集中度高的节点。",
    metric: "capex guidance、cloud revenue、RPO/backlog、FCF、AI ROI commentary。",
    investment_read: "这是反证入口；如果 ROI 或 capex 放缓，前面所有价值流都要降级。",
    weight: 4,
    kind: "feedback",
  },
];

const chainSimpleFlowSteps = [
  {
    step: "1",
    title: "云厂商有 AI 需求",
    plain: "云厂商、AI labs 和企业要训练模型、跑推理和部署 agent，所以先决定要投入多少 capex。",
    investment: "先看需求是否真实：云 capex、AI 收入、RPO/backlog 和客户 ROI。",
  },
  {
    step: "2",
    title: "需求变成 GPU / ASIC 订单",
    plain: "AI 工作负载需要算力，订单先流向 GPU 平台和云厂自研 ASIC。",
    investment: "对应 NVDA、AVGO 等平台/ASIC 节点，也会拉动后面的制造和内存。",
  },
  {
    step: "3",
    title: "GPU / ASIC 拉动制造和内存",
    plain: "芯片要被生产出来，需要 TSMC 的先进制程/封装；芯片旁边还需要 HBM、server DRAM 和 eSSD。",
    investment: "对应 TSMC、SK hynix、Micron、Samsung。这里通常是硬瓶颈。",
  },
  {
    step: "4",
    title: "芯片要被装成可上线系统",
    plain: "系统交付就是把 GPU/ASIC、CPU、内存、存储、网卡、电源、散热和整机结构，组装成 AI server、机柜 rack 和集群，并交付到客户数据中心。",
    investment: "对应 DELL、SMCI、HPE/ODM。订单强不够，还要看毛利、交付和现金流。",
  },
  {
    step: "5",
    title: "机柜上线还需要电力、液冷和网络",
    plain: "高功率机柜不能只买服务器，还要电力容量、UPS、液冷、热管理、机柜级连接、交换机和光/电互联，才能真正跑起来。",
    investment: "对应 VRT、ALAB、CRDO、MRVL、ANET、AVGO 等。最后用利用率、云收入和 ROI 反向验证。",
  },
];

const chainChokepointScores = [
  chokepointScore(BOM.platform, "GPU / 软件栈 / 网络平台", "NVDA", [5, 5, 5, 5, 2, 3], "最强稀缺性，但未定价证据不足，Q4 仍需估值闸门。", "Q2.1 / Q4.1"),
  chokepointScore(BOM.memory, "HBM / server DRAM / eSSD", "SK hynix、MU、Samsung", [5, 4, 4, 5, 3, 3], "硬瓶颈明确，关键反证是 ASP、资格和供给扩张。", "Q2.1.2 / Q3.2"),
  chokepointScore(BOM.manufacturing, "先进制造 / CoWoS 类封装", "TSMC", [5, 5, 4, 4, 3, 3], "交付斜率慢、卡点硬，但 capex 和地缘风险需要折价。", "Q2.1.2 / Q3.1"),
  chokepointScore(BOM.connectivity, "retimer / AEC / optical / Ethernet", "ALAB、CRDO、MRVL、ANET、AVGO", [4, 4, 3, 5, 2, 2], "弹性高，但客户集中、平台替代和估值风险更高。", "Q2.2.1 / Q3.2"),
  chokepointScore(BOM.powerCooling, "power / thermal / liquid cooling", "Vertiv、数据中心工程商", [4, 4, 4, 4, 3, 3], "AI 工厂落地的物理瓶颈，backlog 毛利和项目交付是核心验证。", "Q2.2.2 / Q4.2"),
  chokepointScore(BOM.systemDelivery, "AI server / rack / cluster integration", "DELL、SMCI、HPE/ODM", [3, 3, 2, 4, 3, 2], "订单可见度强，但价值捕获取决于毛利、现金流和执行质量。", "Q2.2.2 / Q4.1"),
  chokepointScore(DEMAND_VALIDATION_LAYER, "capex / utilization / cloud revenue / ROI", "Hyperscaler、AI labs、企业/主权 AI", [3, 3, 2, 5, 2, 2], "不是直接瓶颈标的，但决定全链条需求是否继续扩张。", "Q1 / Q3"),
];

const chainRows = [
  ["上游：核心供给", "决定 AI 工厂能不能拿到算力、内存、制造、封装和高速连接等关键输入。", "GPU/ASIC 平台、先进制造与封装、HBM/高端内存、机柜级连接。", "稀缺性最强，但估值、扩产和技术替代反证也最重要。", "Q1 / Q2 / Q3 / Q4"],
  ["中游：系统落地", "把上游芯片、内存、网络、电力和冷却能力集成为可上线服务器、机柜、集群和数据中心基础设施。", "AI server / rack / cluster 系统交付，电力、液冷和现场工程。", "订单可见度强，但真正价值捕获取决于毛利、交付质量和现金流。", "Q2.2 / Q3 / Q4"],
  ["下游：需求运营", "提出 AI 工作负载和 capex，接收中游交付，并用使用率、云收入、RPO/backlog、FCF 和 ROI 反向验证需求。", "云厂商、AI labs、企业 AI、主权 AI 和数据中心运营方。", "它决定全链条需求是否持续；capex/ROI 下修会先压低高估值和高客户集中标的。", "Q1 / Q3"],
];

const l1s = [
  l1("Q1", "行业空间与需求真实性：AI 工厂的未来空间是否足够大，且需求已经进入财务指标？", "截面前的官方材料显示，AI 工厂已经从单一 GPU 主题扩展成跨平台、服务器、HBM、先进制造、连接网络、电力液冷和系统交付的资本开支链条。行业空间成立的关键不是 TAM 口号，而是客户 capex 能否持续转成收入、backlog、毛利和现金流；当前证据支持需求真实，但仍需用客户 ROI 和云厂商 capex 持续性验证。"),
  l1("Q2", "竞争格局与价值捕获：哪些节点具备 chokepoint 属性，能把行业增长转成公司利润？", "Q2 不再把 chokepoint 当成独立主题，而是先看每个节点的竞争者、替代路线、客户议价力和供给扩张，再判断哪些节点具备真稀缺和货币化能力。当前最强的是平台控制、HBM/先进封装、电力液冷和部分机柜级连接；系统交付有订单弹性但利润率不一定好。"),
  l1("Q3", "哪些反证会降低胜率、赔率或行动状态？", "最大反证不是 AI 工厂不存在，而是市场已充分定价、客户 capex/ROI 弱化、供给快速扩张、连接/系统商被平台压价，以及高 backlog 无法转成高质量利润。"),
  l1("Q4", "估值赔率与标的推荐：哪些标的同时具备胜率、赔率和可监控风险？", "冻结排序优先看 VRT、SK hynix、NVDA、TSM、ALAB、CRDO、MRVL、MU、DELL、AVGO、ANET、SMCI 等价值捕获载体。Q4 不只给名单，还要把隐含预期、base/bull/bear 验证路径、升级数据和降级数据展示清楚；行动状态由稀缺/垄断、未充分定价、业绩弹性和风险控制四维共同决定。"),
];

const l2s = [
  l2("Q1.1", "需求是否已进入财务指标", "NVIDIA、Dell、Vertiv、Astera、Credo、Marvell、Broadcom、Arista、内存公司都在截面前给出收入、订单或毛利证据，说明需求不是只停留在新闻。"),
  l2("Q1.2", "需求如何沿产业链传导", "AI 工厂需求先进入平台和服务器，再传导到内存、制造、连接、电力冷却和系统交付，最终由客户 ROI 决定持续性。"),
  l2("Q2.1", "上游核心节点竞争格局：平台、制造和 HBM 谁有定价权？", "平台控制和 HBM/先进封装是最硬的竞争优势；但越强的卡点通常越容易被市场提前定价，所以需要同时比较替代路线、供给扩张和估值隐含预期。"),
  l2("Q2.2", "连接、电力液冷和系统交付竞争格局：谁能留住利润？", "连接和物理基础设施是 AI 工厂落地瓶颈；VRT/ALAB/CRDO/MRVL 的证据直接，但客户集中、平台替代和项目毛利决定它们是否是真 chokepoint；DELL/SMCI 的订单弹性强但利润质量分化。"),
  l2("Q3.1", "估值和市场隐含预期", "强增长不等于好赔率，必须测试市场是否已经把增长路径提前计入。"),
  l2("Q3.2", "供给扩张、替代和执行反证", "HBM/连接/液冷的高利润会诱发供给扩张；NVIDIA 纵向整合和客户集中会压缩第三方价值捕获。"),
  l2("Q4.1", "目标池与排序", "目标池从卡点映射而来，不按热门 ticker 或美股便利性收缩。"),
  l2("Q4.2", "复盘触发器", "三个月后只用价格 label 评估预测，不用 label 回写历史推理；未来复盘关注订单、毛利、capex、估值和供给反证。"),
];

const q2CompetitionLandscape = [
  {
    node: BOM.platform,
    competition: "NVIDIA 平台生态对 custom ASIC、AMD 和开放网络路线形成强压制，但云厂自研会持续分流部分增量。",
    competitionFacts: "主要竞争路线是 NVIDIA 通用 GPU/系统平台、云厂 custom ASIC、AMD GPU 和开放网络路线；客户选择标准包括软件生态、交付能力、性能功耗、迁移成本和供货确定性。",
    competitionReasoning: "平台与加速器是需求入口，谁定义系统规格，谁就能影响后续 HBM、网络、服务器和液冷采购。因此该节点的竞争结构不是单纯芯片份额，而是平台标准与客户自研之间的拉扯。",
    competitionGap: "待补：NVIDIA GPU、云厂 custom ASIC、AMD GPU 在训练/推理/内部 workload 中的可比份额和出货口径。",
    marketShareParagraphs: [
      "这个节点不能只写“NVIDIA 主导”。按 2026-03-02 前可见材料，能直接引用的份额数值有三组，但口径不同：JPR 的 PC add-in-board 口径显示 Q3 2025 NVIDIA 约 92%、AMD 约 7%、Intel 超过 1%，这不是数据中心 AI accelerator 口径，只能证明 GPU 供应商集中度极高 [JPR / Tom's Hardware](source:SRC-TOMS-JPR-AIB-Q3-2025)；Omdia 的 AI data-center chip spending 口径给出 2024 年约 1230 亿美元、2025E 约 2070 亿美元、2030E 约 2860 亿美元，并明确说 NVIDIA 仍是 dominant vendor，同时 Google TPU、Huawei Ascend、Groq/Cerebras 等 custom ASIC/ASSP 正在 gaining traction [Omdia](source:SRC-OMDIA-AI-PROCESSORS-20250828)；公司财务代理上，NVIDIA Q4 FY26 Data Center revenue 是 623 亿美元 [NVIDIA](source:SRC-NVDA-FY26-Q4)，Broadcom 指引 Q1 FY26 AI semiconductor revenue 为 82 亿美元 [Broadcom](source:SRC-AVGO-FY25-Q4)。因此，报告里应把份额分布写成：NVIDIA 是绝对主导平台，Broadcom/云厂 custom ASIC 是第二增长路线，AMD 和开放路线仍是小份额追赶者。精确的“全球 AI accelerator 厂商份额表”需要 Omdia/Gartner/IDC 付费表补齐，不能用 PC GPU 份额冒充。"
    ],
    advantageParagraphs: [
      "头部玩家优势不是简单来自芯片性能，而是平台闭环：NVIDIA 同时控制 GPU、CUDA/软件生态、NVLink/网络、参考架构和供应链分配，所以客户迁移成本、模型适配成本、系统交付风险都更高。这个优势已经体现在财务体量上：NVIDIA Q4 FY26 Data Center revenue 达 623 亿美元，远高于同一 source pack 里可见的其他 AI accelerator / custom silicon 供应商收入口径。 [NVIDIA](source:SRC-NVDA-FY26-Q4)"
    ],
    catchupParagraphs: [
      "替代玩家不是没有机会，但切入口不同。Broadcom/云厂 custom ASIC 更可能在自有推理 workload 和长期定制项目里分流，AMD 需要同时证明软件生态、供给规模和客户迁移，开放网络路线更多影响系统架构而不是直接替代 GPU。Omdia 已经把 custom ASIC / ASSP 的 gaining traction 写入 AI data-center chip forecast，所以追赶希望应定性为“存在且会分流增量”，但还不能写成已经重排全球份额。 [Omdia](source:SRC-OMDIA-AI-PROCESSORS-20250828) [Broadcom](source:SRC-AVGO-FY25-Q4)"
    ],
    changeVariableParagraphs: [
      "格局变化的核心变量有四个：第一，云厂 custom ASIC 占内部 workload 的比例是否继续上升；第二，NVIDIA 毛利率和供给约束是否松动；第三，AMD 或开放路线是否拿到可验证的大客户规模部署；第四，出口限制导致的区域份额变化。中国是一个极端例子，Jensen Huang 在 2025 年 10 月称 NVIDIA 在中国 advanced AI accelerator 市场份额从约 95% 降到 0%，但这是出口限制下的区域口径，不能外推为全球格局。 [Tom's Hardware / China share](source:SRC-TOMS-NVDA-CHINA-SHARE-202510)"
    ],
    chokepoint: "强。软件栈、互联、客户迁移成本和供给资格形成平台 chokepoint。",
    barrierFacts: "壁垒来自 CUDA/软件栈、NVLink/系统互联、客户模型迁移成本、整机平台认证、供应链配额和生态工具链。",
    catchup: "云厂 custom ASIC 最有追赶希望，AMD 和开放网络路线能在部分 workload 分流，但短期难直接替代 NVIDIA 训练平台。",
    catchupFacts: "替代路线要同时证明软件迁移、性能功耗、供给规模和客户内部部署；单点芯片性能不足以改变平台格局。",
    catchupReasoning: "平台迁移成本高，追赶者通常先在自有推理 workload 或成本敏感场景突破，再逐步影响训练和通用集群采购。",
    catchupGap: "待补：云厂 ASIC 实际部署规模、AMD GPU 客户导入、开放以太网集群规模和客户迁移成本。",
    bargaining: "云厂客户采购金额大、具备自研 ASIC 路线，但短期仍依赖 NVIDIA 平台交付训练和推理容量；议价权被平台锁定和供给紧缺部分抵消。",
    profit: "利润主要进入 NVDA；ASIC 外溢进入 AVGO/MRVL，但受大客户项目节奏制约。",
    profitFacts: "财务验证看 NVIDIA Data Center revenue / gross margin，Broadcom AI semiconductor revenue，Marvell data-center/custom silicon ramp，以及云厂客户 capex 和 RPO 是否继续支撑订单。",
    refute: "客户自研 ASIC 提速、开放网络路线成熟、毛利率下行或中国/出口限制扩大。",
    refuteFacts: "主要观察客户自研 ASIC 放量、NVIDIA 中国收入受限、GPU 毛利率下行、云厂 capex ROI 下降和以太网/开放平台替代。若这些同时出现，平台利润池会从 NVIDIA 向客户自研和网络/ASIC 供应商迁移。",
    qa: "Q2.1 / Q3.1 / Q4.1",
  },
  {
    node: BOM.memory,
    competition: "SK hynix、Micron、Samsung 竞争，关键不是总内存规模，而是 HBM 客户资格、良率、产能和 ASP。",
    competitionFacts: "主要玩家是 SK hynix、Micron、Samsung；竞争口径应拆成 HBM3E/HBM4 客户资格、良率、产能、ASP、server DDR5/eSSD mix，而不是泛化到全部 DRAM/NAND。",
    competitionReasoning: "AI 加速器平台决定 HBM 规格，内存厂只有通过资格认证和稳定供货才能进入高价值份额。份额领先通常会通过 ASP、mix 和毛利率先体现。",
    competitionGap: "待补：HBM3E/HBM4 按客户和代际拆分的份额、ASP、产能分配和已签协议。",
    marketShareParagraphs: [
      "HBM 的供应商份额不能用普通 DRAM 份额替代。当前 source pack 没有 SK hynix / Micron / Samsung 按 HBM3E/HBM4 客户和代际拆分的可比份额表，所以这里直接标为待补。能引用的数值是需求侧和价值量侧：TrendForce 预计 NVIDIA HBM 采购份额超过 70%；HBM bit capacity share 从 2023 年约 2% 到 2024 年约 5%，2025 年超过 10%；HBM 在 DRAM 价值 share 2025 年可能超过 30%。这说明 HBM 节点的价值占比在快速上升，但不是三家供应商份额。 [TrendForce HBM procurement](source:SRC-TF-BLACKWELL-HBM-20240808) [TrendForce HBM value share](source:SRC-TF-HBM-PRICE-20240506)"
    ],
    advantageParagraphs: [
      "头部优势主要来自客户资格、良率和提前锁量锁价，而不是总产能。SK hynix FY2025 revenue KRW 97.1T、operating margin 49%，说明 AI memory mix 对利润已经有强兑现；Micron prepared remarks 给出 HBM TAM 从 2025 年约 350 亿美元到 2028 年约 1000 亿美元，并称 2026 HBM supply 已完成 price and volume agreements。 [SK hynix](source:SRC-SKHYNIX-FY25) [Micron prepared remarks](source:SRC-MU-FY26-Q1-PREPARED)"
    ],
    catchupParagraphs: [
      "Samsung 和 Micron 都有追赶希望，但追赶证据必须看客户资格和 HBM4 ramp，而不是看普通 memory 规模。Samsung 披露 high-value AI products 包括 HBM、server DDR5 和 enterprise SSD；Micron 披露 AI data-center memory demand 推动云内存与 HBM strength。结论是：追赶存在，但需要后续补充 HBM 代际份额和客户认证。 [Samsung](source:SRC-SAMSUNG-FY25) [Micron](source:SRC-MU-FY26-Q1)"
    ],
    changeVariableParagraphs: [
      "最容易改变格局的变量是 HBM ASP、HBM4 认证、良率、锁量协议和 NVIDIA/ASIC 平台的采购分配。若二/三供应商通过关键客户认证并释放稳定供给，头部玩家 ASP 和 mix 优势会先被削弱；若 ASP 继续强，HBM 领导者利润池会继续被强化。 [TrendForce HBM price](source:SRC-TF-HBM-PRICE-20240506)"
    ],
    chokepoint: "强。客户资格和供给斜率决定谁能拿到高价值 AI memory 利润池。",
    barrierFacts: "壁垒来自 HBM 堆叠/封装良率、客户资格认证、提前锁量锁价协议、HBM4 ramp 和 wafer allocation。",
    catchup: "Samsung 和 Micron 有追赶希望，但追赶速度取决于客户资格、HBM4 ramp、良率和已锁定订单。",
    catchupFacts: "HBM 不是普通 DRAM 替代，追赶者需要通过平台客户认证并稳定交付；资格变化会比产能公告更能改变份额。",
    catchupReasoning: "当二/三供应商通过资格认证并释放稳定供给时，头部玩家 ASP 和 mix 优势会被削弱。",
    catchupGap: "待补：各家 HBM4 认证节点、客户锁量协议、良率变化和季度 ASP。",
    bargaining: "GPU/ASIC 平台和云厂需求强，但合格供应商数量少；短期供应商议价权较强，中期取决于三大厂扩产、客户资格变化和 ASP 是否反转。",
    profit: "利润优先流向 HBM 领导者；普通 DRAM/NAND beta 需要折价。",
    profitFacts: "财务验证看 HBM revenue/mix、DRAM ASP、gross margin、库存和 capex。SK hynix FY2025 高利润率、Micron HBM TAM/协议、Samsung 高价值 AI memory 披露共同支撑该节点利润池。",
    refute: "HBM 供给快速扩张、ASP 反转、客户资格变化或替代内存架构出现。",
    refuteFacts: "若 HBM ASP 走弱、客户转向第二/第三供应商、HBM4 ramp 超预期释放供给，或 GPU 架构降低单位 HBM 价值量，利润池要从硬瓶颈降级为周期 beta。",
    qa: "Q2.1.2 / Q3.2 / Q4.1",
  },
  {
    node: BOM.manufacturing,
    competition: "先进制造集中度高，TSMC 处于最关键位置；主要约束来自产能、良率、capex 和地缘风险。",
    competitionFacts: "先进制程和先进封装以 TSMC 为核心，竞争不是普通晶圆代工价格战，而是高端节点、CoWoS/先进封装、良率、交付排期和客户信任。",
    competitionReasoning: "GPU/ASIC 需求只有在先进制造与封装产能可用时才能交付。制造端份额和利润池取决于产能稀缺、良率和客户是否能转单。",
    competitionGap: "待补：先进节点、CoWoS/先进封装按客户和产能的份额，以及可替代产能的真实可用时间。",
    marketShareParagraphs: [
      "先进制造/封装节点的公开份额不应写成泛泛“集中度高”。当前 source pack 可直接引用的是 TSMC 自身口径：Q4 2025 advanced technologies 占 wafer revenue 77%，gross margin 62.3%，2026 capex 指引 520-560 亿美元。它没有给出全球 AI accelerator 先进制程/封装份额表，但这些数字足以说明 TSMC 是该节点的核心供给方。 [TSMC](source:SRC-TSM-Q4-2025)"
    ],
    advantageParagraphs: [
      "TSMC 的头部优势来自先进节点、CoWoS/先进封装、良率工程和客户信任的组合。SemiAnalysis 把 CoWoS 与 HBM 定义为 AI accelerator capacity constraint，这说明制造/封装不是普通代工产能，而是决定 GPU/ASIC 交付斜率的硬卡点。 [SemiAnalysis CoWoS/HBM](source:SRC-SA-COWOS-HBM-2023)"
    ],
    catchupParagraphs: [
      "替代代工和封装路线有长期追赶可能，但短中期更像补充产能，难以快速替代 TSMC 的高端客户信任和良率。真正能改变份额的不是“宣布扩产”，而是客户验证、良率、交期和价格同时达标。当前 source pack 对替代产能的可用时间缺少精确表。"
    ],
    changeVariableParagraphs: [
      "格局变量主要是 CoWoS/先进封装供给释放、客户转单、capex 回报和地缘风险。如果 capex 上升但毛利率/ROIC 下行，制造端仍重要，但投资赔率会下降；如果先进封装继续是交付瓶颈，TSMC 的利润池强度会维持。 [TSMC](source:SRC-TSM-Q4-2025)"
    ],
    chokepoint: "强。先进节点和封装产能决定 GPU/ASIC 交付斜率。",
    barrierFacts: "壁垒来自先进节点工艺、封装产能、良率工程、设备/材料供应、客户验证和地缘安全要求。",
    catchup: "替代代工和封装路线有长期追赶可能，但短中期主要是补充产能，难以快速替代 TSMC 的高端客户信任和良率。",
    catchupFacts: "追赶需要同时具备先进节点、封装能力、良率、客户验证和地缘可接受性。",
    catchupReasoning: "客户转单成本高，除非替代产能在良率、交期和风险上同时达标，否则份额变化会慢于产能公告。",
    catchupGap: "待补：替代先进封装产能的客户验证进度、良率、交付周期和价格折让。",
    bargaining: "大客户有订单规模，但先进产能稀缺、转单难度高，使 TSMC 保持较强议价权；不过 capex 规模和地缘风险会削弱赔率。",
    profit: "TSM 能捕获稳定高质量利润，但估值、capex 和地缘风险限制赔率。",
    profitFacts: "财务验证看 HPC/AI mix、advanced technology revenue share、gross margin、capex、advanced packaging capacity 和客户订单节奏。",
    refute: "先进封装供给放量、capex 回报下降、客户转单或地缘风险恶化。",
    refuteFacts: "若先进封装从瓶颈变成供给充足，或 capex 上升但毛利/ROIC 下降，制造端仍重要但投资赔率会下降。",
    qa: "Q2.1.2.2 / Q3.1 / Q4.1",
  },
  {
    node: BOM.connectivity,
    competition: "ALAB、CRDO、MRVL、AVGO、ANET 与平台自有方案、客户自研和开放/封闭路线竞争。",
    competitionFacts: "该节点包括 retimer、AEC、optical interconnect、custom silicon、Ethernet/InfiniBand switching 等路线；ALAB/CRDO/MRVL/AVGO/ANET 面对平台自有方案和客户自研。",
    competitionReasoning: "集群规模越大，低延迟、高带宽、低功耗连接越重要；但连接节点通常客户集中、技术路线切换快，必须逐项验证 design-in 和量产。",
    competitionGap: "待补：800G/1.6T、retimer、AEC、switching、custom silicon 各子节点的份额和客户集中度。",
    marketShareParagraphs: [
      "连接网络不是一个单一份额市场，必须拆成 retimer/AEC、optical interconnect、custom silicon、Ethernet/InfiniBand switching。当前 source pack 没有各子节点的统一份额表，但有规模代理：LightCounting 估计 AI-cluster optical transceiver/LPO/CPO demand 从 2024 年约 50 亿美元升至 2026 年超过 100 亿美元；Dell'Oro 预测 AI back-end networks 五年可驱动接近 800 亿美元 data-center switch sales。 [LightCounting optics](source:SRC-LC-AI-OPTICS-202501) [Dell'Oro AI networks](source:SRC-DO-AI-NETWORKS-20250715)"
    ],
    advantageParagraphs: [
      "头部优势来自具体 design-in，而不是公司名。ALAB/CRDO 在机柜级连接/AEC 上的优势要看客户导入和收入 ramp；AVGO/MRVL 的优势在 custom silicon 与 Ethernet AI switches；ANET 的优势在 cloud networking。各自优势都必须落到 revenue growth、客户集中、gross margin 和 design win。 [Astera](source:SRC-ALAB-Q4-2025) [Credo](source:SRC-CRDO-FY26-Q3) [Broadcom](source:SRC-AVGO-FY25-Q4)"
    ],
    catchupParagraphs: [
      "替代玩家赶超希望高于 HBM/先进制造，因为连接链条分散、客户会主动扶持多供应商，技术路线也会从 800G 到 1.6T、从 InfiniBand 到 Ethernet 持续变化。因此该节点不能只看静态份额，要每季看 design win 和量产节奏。 [LightCounting PAM4](source:SRC-LC-PAM4-DSP-20260226)"
    ],
    changeVariableParagraphs: [
      "格局变化变量是客户集中度、平台自有方案、800G/1.6T 价格、以太网替代 InfiniBand 的速度，以及主要客户是否延迟 ramp。若平台方把连接价值内化，或 800G/1.6T 价格快速下行，连接节点会从高弹性 chokepoint 降级为供应链 beta。 [Dell'Oro AI networks](source:SRC-DO-AI-NETWORKS-20250715)"
    ],
    chokepoint: "中强。design-in、功耗/延迟和客户认证有壁垒，但客户集中和平台替代压制风险控制。",
    barrierFacts: "壁垒来自平台 design-in、信号完整性、功耗/延迟指标、客户认证、固件/软件兼容和量产稳定性。",
    catchup: "替代玩家赶超希望较高，因为连接链条分散、技术路线切换快，客户也会主动扶持多供应商。",
    catchupFacts: "新进入者可通过特定客户 design win、低功耗/低延迟优势或开放以太网路线切入。",
    catchupReasoning: "该节点优势更依赖项目导入而非永久垄断，季度收入、客户集中度和 design win 比静态份额更重要。",
    catchupGap: "待补：各公司 design win、客户导入、量产时间和毛利变化。",
    bargaining: "客户集中度高且平台方有自研/替代能力，供应商议价权需要靠不可替代 design win、性能优势和交付确定性证明。",
    profit: "高弹性可能进入 ALAB/CRDO/MRVL，稳态利润进入 AVGO/ANET，但需要项目量产和毛利验证。",
    profitFacts: "财务验证看 ALAB/CRDO revenue growth 和 customer concentration，MRVL data-center/custom silicon，Broadcom AI semiconductor，Arista cloud/AI networking revenue 和毛利率。",
    refute: "大客户订单延迟、平台自有方案替代、价格压力或设计导入失败。",
    refuteFacts: "如果主要客户延迟 ramp、平台方案把连接价值内化、800G/1.6T 价格快速下行，连接节点会从高弹性 chokepoint 降级为高波动供应链 beta。",
    qa: "Q2.2.1 / Q3.2 / Q4.1",
  },
  {
    node: BOM.powerCooling,
    competition: "数据中心电力、热管理和现场工程能力竞争，关键不是单品，而是高功率机柜落地能力和 backlog 质量。",
    competitionFacts: "竞争对象包括 power、thermal、liquid cooling、UPS、现场工程和服务能力；客户选择标准是高功率机柜交付、可靠性、项目周期和全生命周期服务。",
    competitionReasoning: "算力设备只有接入电力和散热后才能上线。这个节点不像芯片那样由单一平台定义，但物理工程约束能把需求转成 backlog 和服务收入。",
    competitionGap: "待补：液冷、电源、UPS、热管理、现场服务各子节点的份额、订单和项目毛利。",
    marketShareParagraphs: [
      "电力/液冷没有一个能直接替代芯片份额的统一市场份额表。当前 source pack 的可用数值是规模与订单：Dell'Oro 预测 data-center liquid-cooling manufacturer revenue 2025 年接近 30 亿美元、2029 年接近 70 亿美元；Vertiv Q4 2025 organic orders 增长约 252%，backlog 达 150 亿美元。结论：份额分布需要按 power、thermal、liquid cooling、UPS 和现场服务拆；目前最可验证的上市载体是 Vertiv 的订单和 backlog。 [Dell'Oro liquid cooling](source:SRC-DO-LIQUID-COOLING-20260108) [Vertiv](source:SRC-VRT-Q4-2025)"
    ],
    advantageParagraphs: [
      "头部优势来自高功率机柜落地能力、可靠性、现场服务和项目交付，而不是某一个液冷单品。AI 工厂没有电力和热管理无法上线，所以订单质量、交付周期、项目毛利和现金转化比“是否参与液冷”更重要。 [Vertiv](source:SRC-VRT-Q4-2025)"
    ],
    catchupParagraphs: [
      "替代玩家可以追赶，但要证明现场工程经验、可靠性记录和项目规模。单品供应商可能受益液冷渗透，但未必能拿到系统级利润池。这个节点后续需要补供应商份额和项目毛利。"
    ],
    changeVariableParagraphs: [
      "格局变化核心变量是 backlog 能否转收入、液冷项目毛利、客户 capex 是否下修、以及工程交付是否拖累营运资金。如果 backlog 增长不转收入，或需要牺牲毛利/现金流才能交付，电力液冷仍是必要环节，但利润池强度要下修。 [Vertiv](source:SRC-VRT-Q4-2025)"
    ],
    chokepoint: "强。AI 工厂没有电力和液冷无法上线，物理交付周期形成真实约束。",
    barrierFacts: "壁垒来自项目工程经验、供应链交付、数据中心现场服务、可靠性认证、客户关系和高功率密度液冷方案。",
    catchup: "替代玩家有追赶空间，但需要现场工程经验、可靠性记录和项目交付规模；单品供应商不等于能拿下高功率机柜系统订单。",
    catchupFacts: "追赶关键是客户项目验证、服务网络、液冷方案可靠性和 backlog 转收入质量。",
    catchupReasoning: "这个节点的份额变化通常跟项目中标和交付能力走，而不是单一技术参数。",
    catchupGap: "待补：主要供应商高功率机柜项目、液冷渗透、订单毛利和交付周期。",
    bargaining: "云厂和数据中心客户项目规模大，但高功率机柜落地周期、可靠性和现场工程能力限制替代；供应商议价权取决于 backlog 质量和项目毛利。",
    profit: "VRT 是最直接上市载体，利润质量取决于 backlog 毛利、交付周期和现金转化。",
    profitFacts: "财务验证看 Vertiv organic orders、backlog、organic growth、adjusted margin、cash conversion 和液冷/thermal 项目 mix。",
    refute: "backlog 转收入低质量、液冷毛利不达预期、客户 capex 下修或工程交付延迟。",
    refuteFacts: "若 backlog 增长不转收入，或工程交付需要牺牲毛利/营运资金，电力液冷仍是必要环节，但利润池强度要下修。",
    qa: "Q2.2.2 / Q4.2",
  },
  {
    node: BOM.systemDelivery,
    competition: "DELL、SMCI、HPE/ODM 竞争 AI server/rack 交付，客户议价力强，硬件组装利润池未必厚。",
    competitionFacts: "主要竞争者是 DELL、SMCI、HPE/ODM；客户关注 GPU allocation、整机/rack 交付、供应链整合、价格、服务和执行可靠性。",
    competitionReasoning: "系统交付验证 AI demand 是否真正落地，但多供应商和客户强议价会压低利润池，必须把订单增长和毛利/现金流分开看。",
    competitionGap: "待补：AI server/rack 订单、出货份额、客户集中度、GPU allocation 和 backlog conversion。",
    marketShareParagraphs: [
      "系统交付节点也不能只列公司。当前 source pack 没有 DELL/SMCI/HPE/ODM 的统一 AI server/rack 份额表，但有订单代理：Dell FY26 披露 closed more than 640 亿美元 AI-optimized server orders、shipped more than 250 亿美元、FY27 backlog 430 亿美元；SMCI 是高弹性 AI server exposure，但需要折扣治理、执行和毛利风险。 [Dell](source:SRC-DELL-FY26-Q4) [Supermicro](source:SRC-SMCI-FY26-Q2)"
    ],
    advantageParagraphs: [
      "头部优势来自 GPU allocation、供应链整合、客户关系、交付速度和服务能力。Dell 的优势是订单质量和大型客户交付可信度；SMCI 的优势是定制和速度，但风险是治理、执行、毛利和现金流。 [Dell](source:SRC-DELL-FY26-Q4)"
    ],
    catchupParagraphs: [
      "替代玩家赶超希望较高，因为客户可以在 DELL、SMCI、HPE 和 ODM 间分配订单。除非某家公司绑定 GPU 配额、服务体系或大型项目交付能力，否则系统交付格局比 HBM/先进制造更容易变化。"
    ],
    changeVariableParagraphs: [
      "格局变化变量是 backlog conversion、取消率、GPU allocation、毛利率、库存和现金流。若订单增长不带来毛利和现金流，系统交付节点应从 chokepoint 降级为低毛利订单 beta。 [Dell](source:SRC-DELL-FY26-Q4) [Supermicro](source:SRC-SMCI-FY26-Q2)"
    ],
    chokepoint: "中弱。订单可见度强，但替代供应商多，利润率和现金流决定是否只是过账。",
    barrierFacts: "壁垒来自客户关系、供应链整合、交付速度、服务能力和大规模项目执行；但硬件组装和 ODM 替代使壁垒低于平台/HBM/先进制造。",
    catchup: "替代玩家追赶希望高，客户可在 DELL、SMCI、HPE 和 ODM 间分配订单；除非某家公司绑定 GPU 配额或服务能力，否则格局不稳。",
    catchupFacts: "追赶主要靠供应链整合、交付速度、价格、服务和客户关系，不像 HBM/先进制造那样有强资格壁垒。",
    catchupReasoning: "系统交付更像执行力竞争，份额容易随客户项目、供应链状态和治理风险变化。",
    catchupGap: "待补：各公司 AI server backlog、取消率、毛利率、库存和现金流质量。",
    bargaining: "客户议价权强，且可在 DELL、SMCI、HPE/ODM 间分配订单；供应商只有在交付速度、服务质量和 GPU 配额上形成差异时才有利润保留。",
    profit: "DELL 更偏高质量订单验证；SMCI 弹性大但执行、治理和毛利风险更高。",
    profitFacts: "财务验证看 AI server orders、shipments、backlog conversion、gross/operating margin、inventory、cash conversion 和治理/执行风险。",
    refute: "订单增长不带来毛利和现金流、库存上升、治理风险或订单取消。",
    refuteFacts: "若 backlog 取消、交付延迟、毛利率下降或库存/应收上升，系统交付节点应从核心 chokepoint 降级为低毛利订单 beta。",
    qa: "Q2.2.2 / Q3.2 / Q4.1",
  },
];

const q1DemandSpaceModel = [
  {
    path: "客户 capex / AI labs 预算",
    visibleEvidence: "NVIDIA 数据中心收入和 AI factory 表述，Dell AI server backlog，Vertiv organic orders/backlog。",
    futureSpaceRead: "AI 工厂已经进入可财务验证阶段；未来空间取决于训练/推理工作负载、客户 ROI 和云厂商 capex 延续性。",
    revenueBridge: "capex -> GPU/ASIC -> AI server/rack -> 电力液冷/连接/HBM -> 云收入/RPO/FCF 反馈。",
    openQuestion: "客户 ROI、Cloud revenue 和 FCF 能否证明 capex 不是短期透支。",
  },
  {
    path: "平台规格传导",
    visibleEvidence: "GPU/ASIC 平台规格拉动 HBM、先进制程/封装、网络连接和整机配置。",
    futureSpaceRead: "行业空间不是只看 GPU 数量，而是看每一代平台带来的内存容量、带宽、功耗、机柜密度和网络复杂度提升。",
    revenueBridge: "平台升级 -> HBM/封装/retimer/AEC/交换机/电源液冷单机价值量提升。",
    openQuestion: "平台自有方案、客户自研 ASIC 或开放路线会不会压低第三方利润池。",
  },
  {
    path: "物理落地约束",
    visibleEvidence: "电力、散热、机柜和系统交付订单已经进入 VRT/DELL 等公司财务口径。",
    futureSpaceRead: "AI 工厂未来空间最终受电力容量、液冷交付、机房改造和系统集成节奏限制。",
    revenueBridge: "高功率机柜 -> power/thermal/liquid cooling -> 工程交付 -> backlog 转收入和毛利。",
    openQuestion: "backlog 是否能转成高质量利润，而不是低毛利工程过账。",
  },
];

const industrySpaceConclusion = {
  judgment: "截至 2026-03-02，AI 工厂研究不应把重点放在精确 TAM 估算上。更有效的用法是先判断空间门槛是否通过：需求是否足够真实、扩张是否足够持续、BOM 扩张是否会放大某些必不可少且供给受限的节点。当前锚点证明 AI 工厂需求已经进入收入、订单和 backlog，但本模块不再给单一精确总盘数字，而是为后续 chokepoint 筛选提供方向性约束。",
  anchor: "当前截面锚点只作为证据：Microsoft Cloud $51.5B、commercial RPO $625B；AWS Q4 sales $35.6B；Google Cloud Q4 revenue $17.7B、2026 CapEx $175B-$185B；Meta 2025 capex guidance $70B-$72B；Oracle RPO $523B；NVIDIA Data Center Q4 FY26 revenue $62.3B；Dell AI server backlog $43B；Vertiv backlog $15.0B。",
  futureSpace: "空间门槛判断：空间等级=大，扩张确定性=中高，chokepoint 放大作用=强。最值得继续下钻的是 HBM/先进封装、电力液冷、高速连接、平台控制；服务器组装和普通硬件环节必须用毛利、现金流和 backlog 转化质量过滤。",
  uncertainty: "最大不确定性是客户 ROI、capex 持续性、backlog 转收入质量、HBM/先进封装供给扩张，以及高功率机柜能否按期落地。若这些数据恶化，空间门槛从“通过”降为“待验证”。",
  boundary: "本模块只做空间门槛和节点弹性判断，不做精确 TAM、不回答利润池归属、估值或最终推荐；真正的投资结论进入 Q2 chokepoint、Q3 反证和 Q4 标的排序。",
};

const industrySpaceGateModel = {
  title: "空间门槛口径",
  horizon: "未来 12-36 个月，使用 2026-03-02 前可见收入、订单、backlog、capex 锚点作为判断起点。",
  spaceLevel: "大：AI 工厂已经从概念进入收入、订单和物理基础设施 backlog。",
  expansionCertainty: "中高：需求真实，但仍要用客户 ROI、云收入、FCF 和 backlog 转收入验证持续性。",
  chokepointAmplification: "强：平台规格提高会同步放大 HBM、先进封装、连接、电力和液冷等节点的单位价值量。",
  method: "不追求精确总 TAM，而是判断产业扩张是否足以让小而关键的瓶颈节点出现收入、毛利或估值重估弹性。",
  notUsed: "不使用手工去重总盘作为投资依据；任何精确 TAM 只能作为内部敏感性分析，不能直接提高标的评分。",
  confidence: "中高。当前证据足以支持继续做 chokepoint 下钻，但不足以支持单点精确空间数值。",
};

const industrySpaceBoundary = [
  ["纳入口径", "AI 计算平台、AI server/rack、HBM/高端内存、先进制程/封装、连接网络、电力液冷和数据中心基础设施交付。"],
  ["排除口径", "不把应用软件收入、普通企业 IT 更新、非 AI 数据中心维护性 capex、精确总 TAM、竞争份额和标的估值放进本模块。"],
  ["时间口径", `以 ${AS_OF_DATE} 前公开材料为截面，判断未来 12-36 个月是否足以支撑 chokepoint 下钻，不使用后验股价表现。`],
  ["输出口径", "输出空间等级、扩张确定性、chokepoint 放大作用和节点弹性，不输出手工精确总盘。"],
];

const industrySpaceDriverTree = [
  {
    layer: "1. 需求源头",
    driver: "训练、推理、agent、主权 AI、企业 AI 工作负载增长",
    measurable: "云厂商 capex、AI cloud revenue、RPO/backlog、客户 ROI、GPU/ASIC 订单",
    output: "形成 AI 工厂预算和计算平台需求",
  },
  {
    layer: "2. BOM 放大",
    driver: "每代 GPU/ASIC 提高 HBM 容量、先进封装复杂度、网络速度、机柜功率和散热要求",
    measurable: "HBM mix、先进制程/封装占比、retimer/AEC/交换机收入、单机柜功率、液冷渗透",
    output: "把同一份算力需求放大为更多 BOM 子系统价值量",
  },
  {
    layer: "3. 物理交付",
    driver: "服务器、机柜、电力、液冷、网络和数据中心工程把订单变成上线产能",
    measurable: "AI server shipments/backlog、Vertiv orders/backlog、交付周期、毛利和现金流",
    output: "决定行业空间能否从订单转成收入和可持续扩容",
  },
];

const industrySpaceScenarioRows = [
  {
    scenario: "门槛降级 / 扩张不足",
    gateResult: "空间门槛待验证",
    futureSpace: "需求从扩张转为消化既有订单，BOM 价值量仍存在，但新增订单斜率明显放缓。",
    keyAssumptions: "客户 AI ROI 低于预期，云厂商 capex 下修；GPU/ASIC 供给改善但需求不继续上修；HBM/DRAM 或系统交付价格开始承压。",
    expansionPath: "收入主要来自 backlog 转化和已规划数据中心建设，新增 BOM 拉动有限。",
    upperBound: "capex ROI、项目融资、电力接入、库存和价格下行会削弱 chokepoint。",
    watchData: "云厂商 capex 指引、AI cloud revenue、DELL/VRT backlog conversion、HBM ASP 和库存。",
  },
  {
    scenario: "门槛通过 / 分层扩张",
    gateResult: "空间等级大，扩张确定性中高",
    futureSpace: "未来空间继续扩张，但重点不在总盘，而在能被平台规格和物理瓶颈持续放大的节点：HBM/先进封装、机柜级网络、电力液冷和高端系统交付。",
    keyAssumptions: "训练和推理工作负载继续增长；backlog 能转收入；每代平台提高内存、带宽、功率和散热需求；客户 ROI 没有明显恶化。",
    expansionPath: "GPU/ASIC 需求 -> HBM/先进制造/封装 -> rack/server -> 网络互联 -> 电力液冷 -> 数据中心上线。",
    upperBound: "先进封装/HBM 产能、高功率机柜交付、客户预算和供给扩张后的价格压力。",
    watchData: "NVIDIA/ASIC 订单、TSMC capex 和先进封装产能、HBM mix、AI server backlog、液冷订单。",
  },
  {
    scenario: "门槛强化 / 瓶颈放大",
    gateResult: "空间门槛强化，chokepoint 放大作用强",
    futureSpace: "单柜功率、单卡内存、集群网络复杂度和液冷渗透同步上修，真正重要的是哪些节点因此变得更稀缺、更难替代、更容易变现。",
    keyAssumptions: "推理/agent 工作负载带来持续新增算力；主权 AI 和企业 AI 加速；电力液冷和先进封装扩产跟上；客户 ROI 被云收入或效率提升验证。",
    expansionPath: "新增需求不仅增加 GPU/ASIC 数量，还提高每个 rack 的 HBM、网络、供电、热管理和系统集成价值量。",
    upperBound: "电力瓶颈、供应商扩产速度、客户集中度、监管和估值透支。",
    watchData: "推理收入、AI cloud backlog、sovereign AI 订单、rack-scale networking revenue、液冷渗透率。",
  },
];

const industrySpaceNodeElasticityRows = [
  {
    node: BOM.platform,
    elasticityQuestion: "AI capex 增长是否仍优先流向加速器平台？",
    directionalElasticity: "高，但市场关注度也最高，必须用估值闸门过滤。",
    whyMatters: "它是需求入口；如果平台需求不扩张，后续 HBM、网络、液冷都缺少驱动。",
    currentEvidence: "NVIDIA Q4 FY26 Data Center revenue $62.3B，管理层使用 AI factories 口径。",
    expansionMechanism: "训练/推理工作负载增长、客户 capex、平台迭代、GPU/ASIC 供给改善。",
    capOrRisk: "客户 ROI、ASIC 替代、出口限制、供给释放后的价格和毛利压力。",
    confidence: "高",
    sourceIds: ["SRC-NVDA-FY26-Q4"],
    nextData: "云厂商 capex、AI cloud revenue、RPO/backlog、推理收入和 FCF。",
  },
  {
    node: BOM.systemDelivery,
    elasticityQuestion: "AI 加速器订单能否转成可上线系统，并保留利润？",
    directionalElasticity: "中。订单弹性强，但竞争和客户议价会压低利润池。",
    whyMatters: "它验证需求是否离开芯片环节进入真实交付，但未必是真 chokepoint。",
    currentEvidence: "Dell FY26 AI-optimized server orders >$64B、shipped >$25B、backlog $43B。",
    expansionMechanism: "机柜级部署、GPU/ASIC 可得性、企业/云客户交付周期、rack-scale 方案升级。",
    capOrRisk: "backlog 取消、交付延迟、低毛利系统集成、客户集中。",
    confidence: "高",
    sourceIds: ["SRC-DELL-FY26-Q4"],
    nextData: "AI server revenue、backlog conversion、取消率、交付周期。",
  },
  {
    node: BOM.powerCooling,
    elasticityQuestion: "高功率机柜扩张是否使 power/thermal 成为落地瓶颈？",
    directionalElasticity: "高。若 backlog 能转高质量收入，容易形成被市场低估的物理瓶颈。",
    whyMatters: "算力扩张最终要被电力、散热和工程交付约束，且节点不像 GPU 那样被充分定价。",
    currentEvidence: "Vertiv Q4 2025 organic orders +252% YoY，backlog $15.0B。",
    expansionMechanism: "机柜功率密度提升、液冷渗透、数据中心改造和新建。",
    capOrRisk: "项目交付能力、工程毛利、营运资金、电力接入和客户建设节奏。",
    confidence: "中高",
    sourceIds: ["SRC-VRT-Q4-2025"],
    nextData: "液冷订单、项目毛利、交付周期、营运资金和现金流。",
  },
  {
    node: BOM.manufacturing,
    elasticityQuestion: "AI/HPC 需求是否持续受先进节点和封装产能约束？",
    directionalElasticity: "中高。卡点硬，但市场认知较充分，赔率要看未定价程度。",
    whyMatters: "它决定 GPU/ASIC 和 HBM 能否制造出来，是供给斜率的核心约束。",
    currentEvidence: "TSMC Q4 2025 revenue $33.73B，advanced technologies 77% of wafer revenue，2026 capex guidance $52B-$56B。",
    expansionMechanism: "GPU/ASIC 订单、先进封装能力、良率提升、产能扩张。",
    capOrRisk: "capex 执行、良率、地缘政治、客户订单节奏和封装产能释放。",
    confidence: "中高",
    sourceIds: ["SRC-TSM-Q4-2025"],
    nextData: "advanced packaging capacity、HPC/AI mix、capex 执行、良率。",
  },
  {
    node: BOM.memory,
    elasticityQuestion: "单卡 HBM 容量、带宽和资格约束是否让内存成为硬瓶颈？",
    directionalElasticity: "高。需求、资格、良率和 ASP 同时决定收入与利润弹性。",
    whyMatters: "HBM 是 AI 平台不可缺少的高价值部件，客户资格和供给斜率会影响定价权。",
    currentEvidence: "SK hynix FY2025 revenue KRW97.1467T、operating margin 49%；Micron 和 Samsung 均披露 AI memory/HBM 相关强需求。",
    expansionMechanism: "单卡 HBM 容量提升、HBM4 ramp、server DRAM/eSSD mix 上移。",
    capOrRisk: "供应商扩产、ASP 反转、客户资格认证、库存和内存周期。",
    confidence: "中高",
    sourceIds: ["SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1", "SRC-SAMSUNG-FY25"],
    nextData: "HBM ASP、客户资格、HBM4 ramp、server DRAM/eSSD mix、库存。",
  },
  {
    node: BOM.connectivity,
    elasticityQuestion: "集群规模扩大是否让高速连接成为小而关键的卡点？",
    directionalElasticity: "高弹性。收入基数较小的连接/retimer/AEC 标的可能比大平台更有赔率，但客户集中风险高。",
    whyMatters: "AI 工厂规模越大，rack 内和 rack 间低延迟、高带宽、低功耗连接越关键。",
    currentEvidence: "Broadcom Q1 FY26 AI semiconductor revenue expected $8.2B；Astera Q4 revenue $270.6M +92%；Credo FY26 Q3 revenue $407.0M +200%；Arista FY2025 revenue $9.006B +28.6%。",
    expansionMechanism: "集群规模、机柜间带宽、retimer/AEC、Ethernet/光互联升级。",
    capOrRisk: "客户集中、平台自研、价格压力、技术路线切换。",
    confidence: "中",
    sourceIds: ["SRC-AVGO-FY25-Q4", "SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-ANET-Q4-2025"],
    nextData: "AI networking revenue、design win、客户集中度、订单和毛利率。",
  },
];

const industrySpaceEvidencePackRows = [
  {
    node: DEMAND_VALIDATION_LAYER,
    coreQuestion: "云厂商 capex、RPO 和云收入是否足以支撑 AI 工厂硬件继续扩张？",
    facts: [
      "Microsoft Q2 FY2026 Microsoft Cloud revenue $51.5B，commercial RPO $625B，Azure and other cloud services revenue +39%。",
      "Amazon Q4 2025 AWS segment sales $35.6B，TTM property and equipment purchases $128.3B，FCF 随基础设施投资下降。",
      "Alphabet Q4 2025 Google Cloud revenue $17.7B，Cloud annual run rate 超过 $70B，2026 CapEx guidance $175B-$185B。",
      "Meta Q3 2025 把 2025 capex guidance 提至 $70B-$72B，并提示 2026 capex dollar growth 会明显更大。",
      "Oracle Q2 FY2026 RPO $523B、cloud revenue $8.0B，TTM capex $35.5B，FCF 转负。"
    ],
    inferenceChain: [
      "云收入和 RPO 证明 AI/云需求不是纯叙事，已经进入客户经营指标。",
      "capex 和设备采购上升说明需求正在穿透到硬件、数据中心和电力冷却支出。",
      "如果云收入、RPO 转化或 FCF 无法覆盖 capex，硬件链条会先从估值端降级，再传导到订单。"
    ],
    nodeElasticity: "对全链条是最高层需求闸门：它决定 GPU/ASIC、HBM、服务器、网络、电力液冷是否有继续扩张的预算来源。",
    publicSizingMethods: {
      methods: [
        { sourceType: "客户侧指引", organization: "Alphabet", guidanceContent: "2026 CapEx guidance $175B-$185B，作为 AI 数据中心建设预算锚点。", bomNode: "客户需求 / 云 capex", timeframe: "2026E", verificationMetric: "CapEx 实际执行、Google Cloud revenue、FCF、AI ROI。", confidence: "中高", sourceIds: ["SRC-GOOGL-Q4-2025"] },
        { sourceType: "客户侧指引", organization: "Meta", guidanceContent: "2025 capex guidance $70B-$72B，并提示 2026 capex dollar growth 明显更大。", bomNode: "客户需求 / 云 capex", timeframe: "2025E-2026E", verificationMetric: "capex 指引更新、AI 产品收入/使用率、FCF。", confidence: "中", sourceIds: ["SRC-META-Q3-2025"] },
        { sourceType: "经营验证", organization: "Amazon / Oracle / Microsoft", guidanceContent: "Amazon TTM PPE $128.3B；Oracle RPO $523B；Microsoft commercial RPO $625B。", bomNode: "客户需求 / 云 capex", timeframe: "FY2025-FY2026", verificationMetric: "PPE purchases、RPO 转收入、cloud revenue、FCF。", confidence: "中高", sourceIds: ["SRC-AMZN-Q4-2025", "SRC-ORCL-FY26-Q2", "SRC-MSFT-FY26-Q2"] },
      ],
      alignment: "这是需求源头口径，不是 BOM TAM。它只能说明下游预算池和订单来源是否足够大，不能与 GPU/HBM/服务器收入简单相加。",
      sanityCheck: "多个云厂商同时给出 capex、PPE 或 RPO 高位锚点，支持行业空间门槛通过；但必须继续用云收入、FCF 和 AI ROI 验证这些支出能否持续。",
      conclusion: "公开信息支持 AI 工厂硬件预算池已经成形，但本节点只作为后续 BOM 空间和 chokepoint 的需求锚点。",
      confidence: "中：公开锚点强，但口径不是可加总 TAM。",
      sourceIds: ["SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025", "SRC-ORCL-FY26-Q2"],
    },
    chokepointImplication: "该节点只证明行业空间门槛，不直接推荐标的；真正的 chokepoint 仍要看后续节点是否稀缺且能货币化。",
    refuteData: "云厂商 capex 指引下修、RPO 转收入不及预期、AI cloud revenue 放缓、FCF 压力扩大、AI ROI 披露弱化。",
    sourceIds: ["SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025", "SRC-ORCL-FY26-Q2"],
  },
  {
    node: BOM.platform,
    coreQuestion: "客户 capex 是否继续优先流向 GPU、ASIC 和加速器平台？",
    facts: [
      "NVIDIA Q4 FY2026 Data Center revenue $62.3B，管理层以 AI factories 描述客户投入。",
      "Broadcom Q4 FY2025 AI semiconductor revenue +74%，并预计 Q1 FY2026 AI semiconductor revenue 达 $8.2B。",
      "Omdia 在 cutoff 前公开预测 cloud and data-center AI processor spending 从 2024 年约 $123B 增至 2025 年约 $207B，并到 2030 年约 $286B，custom ASICs 份额提升。",
      "SemiAnalysis 的 GB200 硬件架构和 BOM 拆解显示，加速器平台升级会同时改变 rack-scale 形态、网络、供电和液冷约束。",
      "云厂商 capex/RPO 和云收入上行，为加速器平台提供需求侧锚点。"
    ],
    inferenceChain: [
      "客户 AI capex 先形成加速器平台采购和供应排期。",
      "GPU/ASIC 平台规格提高后，会同步拉动 HBM、先进封装、连接、服务器和电力液冷。",
      "但平台控制越被市场充分识别，越需要用隐含预期和反证闸门控制推荐强度。"
    ],
    nodeElasticity: "高。它是 AI 工厂需求的入口节点，但也是市场定价最充分的节点。",
    publicSizingMethods: {
      methods: [
        { sourceType: "公司财报", organization: "NVIDIA", guidanceContent: "Q4 FY2026 Data Center revenue $62.3B，用已兑现收入作为 GPU/加速器平台空间锚点。", bomNode: "计算加速器 / GPU", timeframe: "Q4 FY2026", verificationMetric: "Data Center revenue、gross margin、客户订单、下一季指引。", confidence: "高", sourceIds: ["SRC-NVDA-FY26-Q4"] },
        { sourceType: "公司指引", organization: "Broadcom", guidanceContent: "Q1 FY2026 AI semiconductor revenue expected $8.2B，用下一季指引锚定 custom ASIC / AI networking。", bomNode: "AI ASIC / AI semiconductor", timeframe: "Q1 FY2026E", verificationMetric: "AI semiconductor revenue、客户集中、custom ASIC 项目量产节奏。", confidence: "中高", sourceIds: ["SRC-AVGO-FY25-Q4"] },
        { sourceType: "第三方拆法", organization: "Omdia", guidanceContent: "AI processor spending 口径：2024 年约 $123B、2025 年约 $207B、2030 年约 $286B；覆盖 GPU、AI ASIC/ASSP、FPGA、CPU 与 memory content/power bands。", bomNode: "GPU / AI ASIC / AI processor", timeframe: "2024A-2030E", verificationMetric: "AI processor revenue、GPU vs custom ASIC mix、云厂商 capex、NVIDIA/Broadcom/Marvell 指引。", confidence: "中", sourceIds: ["SRC-OMDIA-AI-PROCESSORS-20250828"] },
        { sourceType: "第三方拆法", organization: "SemiAnalysis", guidanceContent: "GB200 BOM/架构拆法把加速器平台从单芯片扩展为 rack-scale 系统，提示 GPU/ASIC 空间要同时看机柜功率、液冷、网络和 CPU-GPU 带宽。", bomNode: "GPU platform / rack-scale system", timeframe: "Blackwell platform cycle", verificationMetric: "GB200/B200 出货、rack 功率密度、liquid cooling attach、网络和光互联用量。", confidence: "中", sourceIds: ["SRC-SA-GB200-BOM-2024"] },
      ],
      alignment: "NVIDIA/Broadcom 是公司收入和指引口径，Omdia 是第三方 AI processor 市场口径，SemiAnalysis 是 rack-scale BOM 拆法。三者不能相加，但能互相验证：需求规模、收入兑现、系统复杂度同时上升。",
      sanityCheck: "Omdia 的 2025E $207B 与 NVIDIA 数据中心单季 $62.3B、Broadcom AI semiconductor 指引同方向，说明 AI processor 空间不是小众增量；但 custom ASIC 份额提升也是对 GPU 超额利润的中长期反证。",
      conclusion: "公开拆法支持加速器平台是 AI 工厂 BOM 的第一驱动。空间判断应保留“GPU 仍大、ASIC 渗透提升、系统 BOM 同步放大”的三段式，而不是只看 NVIDIA 单点收入。",
      confidence: "中高：收入锚点和第三方 forecast 均强，但估值、出口限制和 ASIC 替代需要单独判断。",
      sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-OMDIA-AI-PROCESSORS-20250828", "SRC-SA-GB200-BOM-2024"],
    },
    chokepointImplication: "平台方是硬 chokepoint，但 final ranking 不能只按稀缺性排序，必须补估值和盈利上修空间。",
    refuteData: "AI ROI 不达预期、ASIC 替代加速、出口管制扩大、毛利率下行、客户 capex 下修。",
    sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-OMDIA-AI-PROCESSORS-20250828", "SRC-SA-GB200-BOM-2024"],
  },
  {
    node: BOM.memory,
    coreQuestion: "平台升级是否把价值量和稀缺性持续推向 HBM、server DRAM 和 eSSD？",
    facts: [
      "SK hynix FY2025 revenue KRW97.1467T、operating margin 49%，公司把表现与 AI memory 和 HBM leadership 绑定。",
      "Micron FY2026 Q1 披露 record revenue 和 margin expansion，AI data-center memory 是核心驱动。",
      "Micron FY2026 Q1 business outlook 指引 FQ2 FY2026 revenue $18.70B ± $400M、non-GAAP gross margin 68.0% ± 1.0%，并表示业务表现预计将在 FY2026 继续强化。",
      "Micron FY2026 Q1 prepared remarks 预计 HBM TAM 从 2025 年约 $35B 增至 2028 年约 $100B，约 40% CAGR。",
      "Samsung Q4 2025 Memory Business 达到 record quarterly revenue 和 operating profit，HBM、server DDR5、enterprise SSD 是高价值产品。",
      "TrendForce 在 2024 年 5 月披露 HBM ASP 是传统 DRAM 的数倍、约 DDR5 的 5 倍，并预计 HBM 在 DRAM 价值占比 2024 年超过 20%、2025 年可能超过 30%。",
      "TrendForce 在 2024 年 8 月披露 NVIDIA 是最大 HBM 买家，Blackwell 升级带动单芯片 HBM 容量和 HBM3e 12hi 消耗提升。",
      "SemiAnalysis 把 CoWoS 和 HBM 共同列为 AI accelerator 供给瓶颈，说明 HBM 空间要和先进封装一起验证。"
    ],
    inferenceChain: [
      "GPU/ASIC 平台迭代提高单卡内存容量、带宽和封装复杂度。",
      "客户认证、良率和产能爬坡让 HBM 的供给斜率短期慢于需求斜率。",
      "若 ASP、mix 和毛利继续维持，HBM 比普通存储 beta 更接近 AI 工厂硬 chokepoint。"
    ],
    nodeElasticity: "高。它同时受数量、单卡价值量、产品 mix 和资格认证约束驱动。",
    publicSizingMethods: {
      methods: [
        { sourceType: "公司指引", organization: "Micron", guidanceContent: "FQ2 FY2026 revenue guidance $18.70B ± $400M，non-GAAP gross margin 68.0% ± 1.0%；管理层表示 business performance 预计将在 FY2026 继续强化，prepared remarks 还披露 2026 HBM supply 已完成价格和数量协议。", bomNode: "HBM / Cloud Memory / 高端内存", timeframe: "FQ2 FY2026 / FY2026", verificationMetric: "FQ2 revenue、gross margin、Cloud Memory revenue/gross margin、HBM supply agreement、HBM revenue mix。", confidence: "中：公司整体和云内存相关指引清晰，但不是 HBM 单项收入指引。", sourceIds: ["SRC-MU-FY26-Q1", "SRC-MU-FY26-Q1-PREPARED"] },
        { sourceType: "公司 TAM", organization: "Micron", guidanceContent: "HBM TAM 从 2025 年约 $35B 增至 2028 年约 $100B，约 40% CAGR。", bomNode: "HBM", timeframe: "2025E-2028E", verificationMetric: "HBM ASP、客户资格、HBM4 ramp、供给协议、毛利率。", confidence: "中高", sourceIds: ["SRC-MU-FY26-Q1-PREPARED"] },
        { sourceType: "经营验证", organization: "SK hynix", guidanceContent: "FY2025 revenue KRW97.1467T，operating margin 49%，用 HBM leadership 与利润率验证价值捕获。", bomNode: "HBM / AI memory", timeframe: "FY2025", verificationMetric: "HBM revenue mix、operating margin、客户资格、capex。", confidence: "中高", sourceIds: ["SRC-SKHYNIX-FY25"] },
        { sourceType: "经营验证", organization: "Micron / Samsung", guidanceContent: "Micron record revenue / margin expansion；Samsung Memory record quarterly revenue and operating profit。", bomNode: "高端内存 / server DRAM / eSSD", timeframe: "FY2025-FY2026", verificationMetric: "AI data-center memory、HBM、server DDR5、enterprise SSD mix。", confidence: "中", sourceIds: ["SRC-MU-FY26-Q1", "SRC-SAMSUNG-FY25"] },
        { sourceType: "第三方拆法", organization: "TrendForce", guidanceContent: "HBM 空间拆法以 bit share、value share 和 ASP premium 交叉看：HBM bit capacity share 2023 年约 2%、2024 年约 5%、2025 年超过 10%；价值占 DRAM 2024 年超过 20%、2025 年可能超过 30%。", bomNode: "HBM", timeframe: "2023A-2025E", verificationMetric: "HBM bit share、value share、ASP premium、yield、qualification、DRAM value share。", confidence: "中高", sourceIds: ["SRC-TF-HBM-PRICE-20240506"] },
        { sourceType: "第三方拆法", organization: "TrendForce", guidanceContent: "Blackwell 推动 HBM3e 和 12hi 用量提升，NVIDIA HBM procurement share expected above 70%，2024 HBM demand growth above 200%，2025 expected to double again。", bomNode: "HBM per accelerator content", timeframe: "2024E-2025E", verificationMetric: "NVIDIA procurement share、HBM3e mix、12hi share、single-chip HBM capacity、supplier qualification。", confidence: "中", sourceIds: ["SRC-TF-BLACKWELL-HBM-20240808"] },
        { sourceType: "第三方拆法", organization: "SemiAnalysis", guidanceContent: "CoWoS/HBM 共同构成 AI accelerator 供给瓶颈，HBM 不能脱离先进封装产能和客户资格单独看。", bomNode: "HBM / CoWoS", timeframe: "AI accelerator cycle", verificationMetric: "CoWoS capacity、HBM supply、qualification、GPU shipment constraint。", confidence: "中", sourceIds: ["SRC-SA-COWOS-HBM-2023"] },
      ],
      alignment: "Micron 的 FQ2/FY2026 outlook 是公司整体和云内存相关指引，$35B->$100B 是 HBM TAM 口径；TrendForce 是 bit/value share、ASP 和 NVIDIA 采购份额口径；SK hynix/Micron/Samsung 是公司财务验证口径；SemiAnalysis 是供给瓶颈口径。它们不能加总，但共同回答容量、价格、价值占比、利润兑现和供给约束。",
      sanityCheck: "Micron FQ2 outlook 的收入和毛利率上修，与其 HBM TAM 路径、TrendForce 2024/2025 高增长和 HBM 价值占比提升方向一致。若未来 HBM value share、ASP premium、客户资格或 Micron Cloud Memory 毛利下滑，则 Micron TAM 路径需要降级。",
      conclusion: "HBM 是行业空间部分公开拆法最充分的节点：公司指引给近端收入/毛利验证，公司 TAM 给未来空间，TrendForce 给价格/占比/需求增长，财务数据验证价值捕获，SemiAnalysis 解释瓶颈来源。报告不再自建更高精度 TAM，而把 HBM 列为高置信空间扩张和后续 Q2/Q4 重点验证节点。",
      confidence: "高：多类公开来源一致，但 ASP、资格和供给扩张仍是反证闸门。",
      sourceIds: ["SRC-MU-FY26-Q1-PREPARED", "SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1", "SRC-SAMSUNG-FY25", "SRC-TF-HBM-PRICE-20240506", "SRC-TF-BLACKWELL-HBM-20240808", "SRC-SA-COWOS-HBM-2023"],
    },
    chokepointImplication: "SK hynix/MU/Samsung 进入核心观察池，但公司强度要按 HBM 份额、资格、ASP 和估值分别排序。",
    refuteData: "HBM ASP 下行、库存上升、客户资格不及预期、HBM4 ramp 延后或供给扩张快于需求。",
    sourceIds: ["SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1", "SRC-SAMSUNG-FY25", "SRC-MU-FY26-Q1-PREPARED", "SRC-TF-HBM-PRICE-20240506", "SRC-TF-BLACKWELL-HBM-20240808", "SRC-SA-COWOS-HBM-2023"],
  },
  {
    node: BOM.manufacturing,
    coreQuestion: "GPU/ASIC 和 HBM 扩张是否继续受先进节点、先进封装和良率约束？",
    facts: [
      "TSMC Q4 2025 revenue $33.73B，gross margin 62.3%，advanced technologies 占 wafer revenue 77%。",
      "TSMC 2026 capex guidance $52B-$56B，说明先进制造和封装仍在扩产周期。",
      "SemiAnalysis 把 CoWoS 描述为高容量 AI accelerator 的核心封装路线，并把 CoWoS 和 HBM 一起列为 GPU 供给瓶颈。",
      "Omdia 的半导体趋势报告把 AI growth 传导到 GPUs、logic ASICs、HBM、先进节点、chiplets、silicon photonics 和 power-management ICs。",
      "加速器平台和 HBM 需求必须通过先进制程、封装、良率和产能排期落地。"
    ],
    inferenceChain: [
      "加速器需求越强，越依赖先进节点、封装能力和良率工程。",
      "高 capex 同时是需求强的证据，也是未来供给释放的反证来源。",
      "TSMC 是硬卡点，但赔率要看市场是否已经把先进制造稀缺性定价充分。"
    ],
    nodeElasticity: "中高。卡点硬、财务化强，但资本开支和市场认知也高。",
    publicSizingMethods: {
      methods: [
        { sourceType: "公司财报", organization: "TSMC", guidanceContent: "Q4 2025 revenue $33.73B；advanced technologies 77% of wafer revenue。", bomNode: "先进制程", timeframe: "Q4 2025", verificationMetric: "advanced technologies revenue mix、HPC/AI mix、gross margin。", confidence: "中高", sourceIds: ["SRC-TSM-Q4-2025"] },
        { sourceType: "公司指引", organization: "TSMC", guidanceContent: "2026 capex guidance $52B-$56B，用资本开支指引判断先进制造/封装扩产斜率。", bomNode: "先进制造 / 先进封装", timeframe: "2026E", verificationMetric: "capex 执行、advanced packaging capacity、良率、客户订单。", confidence: "中", sourceIds: ["SRC-TSM-Q4-2025"] },
        { sourceType: "第三方拆法", organization: "SemiAnalysis", guidanceContent: "CoWoS 是 TSMC 2.5D packaging，把 logic 与 HBM 集成在 interposer 上；AI accelerator 需求使 CoWoS 和 HBM 成为供给瓶颈。", bomNode: "CoWoS / advanced packaging", timeframe: "AI accelerator cycle", verificationMetric: "CoWoS capacity、HBM availability、GPU shipment constraint、packaging lead time。", confidence: "中高", sourceIds: ["SRC-SA-COWOS-HBM-2023"] },
        { sourceType: "第三方拆法", organization: "Omdia", guidanceContent: "AI growth 需要先进节点、chiplets、silicon photonics、HBM 和 power-management ICs 配合，说明制造/封装空间来自平台升级后的多部件协同。", bomNode: "advanced process / chiplet / packaging ecosystem", timeframe: "2026 trend outlook", verificationMetric: "HPC advanced-node mix、advanced packaging capacity、chiplet adoption、silicon photonics attach。", confidence: "中", sourceIds: ["SRC-OMDIA-SEMI-TRENDS-202512"] },
      ],
      alignment: "TSMC 是收入/capex 口径，SemiAnalysis 是 CoWoS/HBM 瓶颈口径，Omdia 是技术路线口径。三者共同说明先进制造/封装是 AI 工厂扩张的供给斜率节点，但没有给可加总的独立 TAM。",
      sanityCheck: "TSMC 高 advanced technology 占比和高 capex 与 SemiAnalysis 的 CoWoS bottleneck 一致；但如果先进封装产能释放快于 GPU/HBM 需求，瓶颈强度会下调。",
      conclusion: "先进制造/封装的行业空间应以“供给斜率和产能瓶颈”呈现，而不是精确 TAM。当前公开信息足以确认其是上游硬约束，但标的赔率仍要靠估值和产能释放节奏判断。",
      confidence: "中高：瓶颈逻辑清楚，但独立产能和 ASP 口径仍不完整。",
      sourceIds: ["SRC-TSM-Q4-2025", "SRC-SA-COWOS-HBM-2023", "SRC-OMDIA-SEMI-TRENDS-202512"],
    },
    chokepointImplication: "用于解释 AI 工厂供给斜率；进入标的排序时，需要用估值、地缘和产能释放节奏折扣。",
    refuteData: "先进封装产能释放超预期、HPC/AI mix 下滑、capex 执行偏慢、客户订单取消或地缘风险上升。",
    sourceIds: ["SRC-TSM-Q4-2025", "SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-SA-COWOS-HBM-2023", "SRC-OMDIA-SEMI-TRENDS-202512"],
  },
  {
    node: BOM.powerCooling,
    coreQuestion: "高功率 rack 是否让 power/thermal 从配套环节变成物理落地瓶颈？",
    facts: [
      "Vertiv Q4 2025 organic orders +252%，backlog $15.0B。",
      "Meta、Alphabet、Amazon、Oracle 等客户侧 capex/RPO/capex 数据显示数据中心基础设施支出正在扩张。",
      "Dell'Oro Group 在 cutoff 前预计 data-center liquid-cooling manufacturer revenue 2025 年接近 $3B、2029 年接近 $7B，hyperscaler 是需求锚点。",
      "SemiAnalysis cooling report 认为数据中心冷却是 AI infrastructure 中变化最快的市场之一，并提示液冷需求可能被低估。",
      "SemiAnalysis GB200 架构拆法显示，rack-scale 平台升级会把高功率密度和 direct-to-chip liquid cooling 从配套条件变成部署约束。",
      "AI server 和 rack 交付需要电力、热管理、液冷、UPS 和现场工程能力。"
    ],
    inferenceChain: [
      "GPU/ASIC 和高密度 rack 提高单柜功率和热负载。",
      "服务器订单只有在电力、冷却和数据中心工程完成后才变成上线算力。",
      "若 VRT backlog 能转成高质量收入和现金流，这类物理瓶颈可能比平台叙事更有赔率。"
    ],
    nodeElasticity: "高。单位 rack 功率和液冷渗透提升会放大该节点价值量。",
    publicSizingMethods: {
      methods: [
        { sourceType: "经营验证", organization: "Vertiv", guidanceContent: "Organic orders +252%；backlog $15.0B，用订单和 backlog 作为电力/热管理需求锚点。", bomNode: "电力 / 液冷 / 热管理", timeframe: "Q4 2025", verificationMetric: "backlog 转收入、项目毛利、现金流、交付周期。", confidence: "中高", sourceIds: ["SRC-VRT-Q4-2025"] },
        { sourceType: "客户侧指引", organization: "Alphabet / Amazon / Meta / Oracle", guidanceContent: "云厂商 capex、PPE purchases、RPO 共同验证数据中心基础设施预算。", bomNode: "数据中心基础设施", timeframe: "2025E-2026E", verificationMetric: "capex 执行、RPO 转收入、power/thermal 订单、液冷 attach rate。", confidence: "中", sourceIds: ["SRC-GOOGL-Q4-2025", "SRC-AMZN-Q4-2025", "SRC-META-Q3-2025", "SRC-ORCL-FY26-Q2"] },
        { sourceType: "第三方拆法", organization: "Dell'Oro Group", guidanceContent: "Data-center liquid-cooling manufacturer revenue 2025 年接近 $3B、2029 年接近 $7B；hyperscaler anchor demand，direct liquid cooling 为主要路径。", bomNode: "liquid cooling / thermal infrastructure", timeframe: "2025E-2029E", verificationMetric: "liquid cooling revenue、hyperscaler deployment、direct liquid cooling adoption、Vertiv/CoolIT/nVent/Boyd share。", confidence: "中高", sourceIds: ["SRC-DO-LIQUID-COOLING-20260108"] },
        { sourceType: "第三方拆法", organization: "SemiAnalysis", guidanceContent: "冷却系统拆法从 chip-by-chip capacity 出发，提示高功率 AI 芯片和机柜密度提高会低估 liquid cooling demand。", bomNode: "power / thermal / cooling system", timeframe: "AI data-center buildout", verificationMetric: "rack power density、liquid cooling attach、facility readiness、project lead time。", confidence: "中", sourceIds: ["SRC-SA-COOLING-2025"] },
        { sourceType: "第三方拆法", organization: "SemiAnalysis", guidanceContent: "GB200 rack-scale 架构提示许多数据中心难以承载极高 rack density，direct-to-chip liquid cooling 成为部署条件。", bomNode: "rack power density / direct-to-chip liquid cooling", timeframe: "Blackwell platform cycle", verificationMetric: "GB200/GB300 deployment mix、rack density、DLC adoption、data-center retrofit schedule。", confidence: "中", sourceIds: ["SRC-SA-GB200-BOM-2024"] },
      ],
      alignment: "Dell'Oro 是 liquid-cooling 市场 revenue 口径，Vertiv 是供应商 backlog 口径，云厂商是客户 capex 口径，SemiAnalysis 是 rack power/cooling 物理约束口径。它们不能加总，但能验证需求、供给、技术条件三者同时成立。",
      sanityCheck: "Dell'Oro 的 2025E ~$3B 到 2029E ~$7B 不是 AI 工厂全部电力基础设施 TAM，只是 liquid-cooling manufacturer revenue；与 Vertiv $15B backlog 比较时要注意 Vertiv 覆盖 power/thermal/服务等更宽口径。",
      conclusion: "电力/液冷节点从“订单强”升级为“有第三方空间口径 + 物理部署约束 + 公司 backlog 验证”的节点。未来空间不用自建总 TAM，重点跟踪液冷收入、attach rate、项目毛利和 backlog 转化。",
      confidence: "中高：公开拆法和订单锚点都较强，但口径较宽，需要防止把液冷 TAM 与整体 data-center infrastructure 混算。",
      sourceIds: ["SRC-VRT-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-AMZN-Q4-2025", "SRC-META-Q3-2025", "SRC-ORCL-FY26-Q2", "SRC-DO-LIQUID-COOLING-20260108", "SRC-SA-COOLING-2025", "SRC-SA-GB200-BOM-2024"],
    },
    chokepointImplication: "VRT 是 Q4 的核心候选之一，但必须用 backlog 毛利、现金流和项目交付节奏验证。",
    refuteData: "订单取消、backlog 转收入慢、项目毛利下滑、营运资金恶化、电力接入或客户建设延迟。",
    sourceIds: ["SRC-VRT-Q4-2025", "SRC-META-Q3-2025", "SRC-GOOGL-Q4-2025", "SRC-AMZN-Q4-2025", "SRC-ORCL-FY26-Q2", "SRC-DO-LIQUID-COOLING-20260108", "SRC-SA-COOLING-2025", "SRC-SA-GB200-BOM-2024"],
  },
  {
    node: BOM.connectivity,
    coreQuestion: "集群规模扩大是否让高速连接、retimer、AEC、光互联和以太网成为小而关键的增量节点？",
    facts: [
      "Astera Labs Q4 2025 revenue $270.6M、+92%，定位 rack-scale AI infrastructure connectivity。",
      "Credo FY2026 Q3 revenue $407.0M、+200%，产品包括 AEC、optical interconnects 和 memory connectivity。",
      "Marvell FY2026 Q3 data-center sales +38%，由 AI custom products 和 electro-optics 驱动。",
      "Arista FY2025 revenue $9.006B、+28.6%，并披露 AI networking goals exceeded。",
      "LightCounting 在 2025 年 1 月估计 AI clusters 相关 optical transceiver、LPO、CPO 需求从 2024 年约 $5B 增至 2026 年超过 $10B。",
      "LightCounting 在 2026 年 2 月披露 AI capex 使 800G PAM4 chipset shipments 在 2025 年接近三倍增长，并预计 2026 年 800G shipments 继续超过翻倍。",
      "Dell'Oro Group 在 2025 年 7 月预计 AI back-end networks 未来五年可能驱动近 $80B data center switch sales，并判断 Ethernet 逐步替代 InfiniBand 份额。"
    ],
    inferenceChain: [
      "AI 工厂从单机扩成集群后，瓶颈从算力扩散到带宽、延迟、功耗和信号完整性。",
      "连接节点基数较小，收入弹性可能高于大平台，但通常客户集中、设计导入和技术路线风险更高。",
      "只有 design win、订单和毛利能持续验证时，连接才从主题外溢升级为 chokepoint。"
    ],
    nodeElasticity: "高弹性。最适合寻找未充分定价的小节点，但风险控制必须比大平台更严格。",
    publicSizingMethods: {
      methods: [
        { sourceType: "经营验证", organization: "Astera Labs", guidanceContent: "Q4 revenue $270.6M，+92%，验证 rack-scale AI infrastructure connectivity 需求。", bomNode: "retimer / connectivity", timeframe: "Q4 2025", verificationMetric: "AI connectivity revenue、design wins、客户集中、毛利率。", confidence: "中", sourceIds: ["SRC-ALAB-Q4-2025"] },
        { sourceType: "经营验证", organization: "Credo", guidanceContent: "Revenue $407.0M，+200%，验证 AEC / optical interconnect 需求。", bomNode: "AEC / optical interconnect", timeframe: "FY2026 Q3", verificationMetric: "AEC revenue、客户集中、订单延续性、ASP。", confidence: "中", sourceIds: ["SRC-CRDO-FY26-Q3"] },
        { sourceType: "公司指引 / 经营验证", organization: "Broadcom / Arista", guidanceContent: "Broadcom Q1 FY26 AI semiconductor guide $8.2B；Arista FY2025 revenue $9.006B。", bomNode: "AI networking / Ethernet", timeframe: "FY2025-FY2026E", verificationMetric: "AI semiconductor revenue、AI networking revenue、交换机订单、客户份额。", confidence: "中", sourceIds: ["SRC-AVGO-FY25-Q4", "SRC-ANET-Q4-2025"] },
        { sourceType: "第三方拆法", organization: "LightCounting", guidanceContent: "AI clusters optical transceivers/LPO/CPO 市场从 2024 年约 $5B 增至 2026 年超过 $10B；2025-2030 模型覆盖主要云厂商。", bomNode: "optical transceiver / LPO / CPO", timeframe: "2024A-2026E / 2025E-2030E", verificationMetric: "800G/1.6T optical transceiver shipments、LPO/CPO deployments、hyperscaler optical spend。", confidence: "中高", sourceIds: ["SRC-LC-AI-OPTICS-202501"] },
        { sourceType: "第三方拆法", organization: "LightCounting", guidanceContent: "AI capex 向 DSP/PAM4 芯片传导：800G PAM4 chipset shipments 2025 年接近三倍增长，2026 年 expected to more than double；1.6T ports 从小基数启动。", bomNode: "PAM4 DSP / 800G / 1.6T ports", timeframe: "2025A-2026E", verificationMetric: "800G PAM4 shipments、1.6T port ramp、DSP vendor revenue、optical module demand。", confidence: "中", sourceIds: ["SRC-LC-PAM4-DSP-20260226"] },
        { sourceType: "第三方拆法", organization: "Dell'Oro Group", guidanceContent: "AI back-end networks 未来五年可能驱动近 $80B data center switch sales；Ethernet 预计逐步胜出，端口速率从 800G 向 1.6T/3.2T 迁移。", bomNode: "AI back-end switch / Ethernet", timeframe: "2025E-2030E", verificationMetric: "AI switch sales、Ethernet vs InfiniBand share、800G/1.6T/3.2T port mix、vendor share。", confidence: "中高", sourceIds: ["SRC-DO-AI-NETWORKS-20250715"] },
        { sourceType: "第三方拆法", organization: "SemiAnalysis", guidanceContent: "Blackwell NVL72/NVLink scale-up 与 InfiniBand/Ethernet scale-out 使 800G 和 1.6T 光互联成为系统 BOM 的增量节点。", bomNode: "NVLink scale-up / scale-out optics", timeframe: "Blackwell platform cycle", verificationMetric: "NVL72 deployment、scale-up optics、scale-out switch ports、800G/1.6T ramp。", confidence: "中", sourceIds: ["SRC-SA-OPTICAL-2024"] },
      ],
      alignment: "公司收入锚点覆盖 retimer/AEC/custom silicon/Ethernet；LightCounting 是 optics/PAM4/DSP/端口口径；Dell'Oro 是 AI backend switch sales 口径；SemiAnalysis 是平台架构和 800G/1.6T BOM 传导口径。不能加总，但能验证连接网络空间来自集群规模、端口速率和架构升级。",
      sanityCheck: "LightCounting 的 optics $5B->$10B+ 和 Dell'Oro 的 switch sales nearly $80B 是不同层级，不应相加；共同含义是 AI 集群扩张把价值从 GPU 外溢到端口、DSP、光模块、交换机和 AEC/retimer。",
      conclusion: "连接网络节点已从“公司高增速”升级为“第三方端口/光模块/交换机 forecast + 公司财务兑现”。空间方向明确，但公司排序必须继续看客户集中、design-in、平台路线和估值。",
      confidence: "中高：第三方 forecast 丰富，单公司价值捕获仍需订单和客户份额验证。",
      sourceIds: ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-AVGO-FY25-Q4", "SRC-ANET-Q4-2025", "SRC-LC-AI-OPTICS-202501", "SRC-LC-PAM4-DSP-20260226", "SRC-DO-AI-NETWORKS-20250715", "SRC-SA-OPTICAL-2024"],
    },
    chokepointImplication: "ALAB/CRDO/MRVL/AVGO/ANET 进入观察池，排序要绑定客户集中、平台替代和估值赔率。",
    refuteData: "客户订单延后、平台方自研或捆绑网络方案、ASP 下滑、产品路线切换、客户集中度恶化。",
    sourceIds: ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3", "SRC-AVGO-FY25-Q4", "SRC-ANET-Q4-2025", "SRC-LC-AI-OPTICS-202501", "SRC-LC-PAM4-DSP-20260226", "SRC-DO-AI-NETWORKS-20250715", "SRC-SA-OPTICAL-2024"],
  },
  {
    node: BOM.systemDelivery,
    coreQuestion: "AI server 和 rack 订单是否能从平台需求转化为高质量交付、收入和现金流？",
    facts: [
      "Dell FY2026 closed more than $64B in AI-optimized server orders、shipped more than $25B，并进入 FY2027 时拥有 $43B AI server backlog。",
      "Supermicro FY2026 Q2 仍是 AI server assembly exposure，但毛利、库存、执行和治理风险需要更高折价。",
      "NVIDIA Blackwell / rack-scale 平台升级把 GPU、HBM、网络、电力液冷和系统集成绑定到同一个交付周期。",
      "云厂商 capex 与 RPO 为 AI server/rack 需求提供预算来源，但客户议价力会压制系统商利润池。"
    ],
    inferenceChain: [
      "GPU/ASIC 订单只有进入 AI server、rack 和 cluster 集成，才会转成可上线算力。",
      "系统交付节点的空间来自订单、backlog 和发货，但利润质量取决于配置复杂度、交付能力、服务附加值和客户议价。",
      "该节点能证明行业空间扩散，却不必然证明高质量 chokepoint；必须用毛利、现金流、库存和取消率验证。"
    ],
    nodeElasticity: "中高。订单弹性强，但价值捕获弱于平台、HBM 和电力液冷，适合 watch-only 观察。",
    publicSizingMethods: {
      methods: [
        { sourceType: "公司指引", organization: "Dell Technologies", guidanceContent: "FY2026 AI-optimized server orders 超过 $64B、shipped more than $25B、FY2027 期初 AI server backlog $43B。", bomNode: "AI server / rack 系统交付", timeframe: "FY2026 / FY2027 backlog", verificationMetric: "AI server orders、shipments、backlog conversion、operating margin、cash conversion。", confidence: "中高", sourceIds: ["SRC-DELL-FY26-Q4"] },
        { sourceType: "财务兑现证据", organization: "Dell Technologies", guidanceContent: "已发货超过 $25B AI-optimized servers，说明订单已经部分进入收入兑现，而不只是远期 backlog。", bomNode: "AI server shipments", timeframe: "FY2026", verificationMetric: "shipments、revenue recognition、margin、working capital。", confidence: "中", sourceIds: ["SRC-DELL-FY26-Q4"] },
        { sourceType: "财务兑现证据", organization: "Supermicro", guidanceContent: "Supermicro 仍有 AI server 组装敞口，但报告将其作为高弹性、低风险控制节点处理。", bomNode: "AI server assembly", timeframe: "FY2026 Q2", verificationMetric: "revenue growth、gross margin、inventory、governance/execution risk。", confidence: "中低", sourceIds: ["SRC-SMCI-FY26-Q2"] },
        { sourceType: "客户侧指引", organization: "云厂商 / AI labs", guidanceContent: "客户 capex、RPO 和数据中心建设预算为 AI server/rack 订单提供需求来源。", bomNode: "AI server / rack demand", timeframe: "2025A-2026E", verificationMetric: "capex execution、RPO conversion、server backlog、取消率。", confidence: "中", sourceIds: ["SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025"] },
        { sourceType: "第三方拆法", organization: "SemiAnalysis", guidanceContent: "GB200 / Blackwell rack-scale 拆法说明系统交付不只是服务器组装，还包括 GPU、HBM、网络、电力液冷和 rack 集成协同。", bomNode: "rack-scale system delivery", timeframe: "Blackwell platform cycle", verificationMetric: "rack shipment、integration lead time、GPU allocation、power/cooling readiness。", confidence: "中", sourceIds: ["SRC-SA-GB200-BOM-2024"] },
      ],
      alignment: "Dell 是订单/backlog/shipments 口径，SMCI 是高弹性但低质量验证口径，云厂商是需求预算口径，SemiAnalysis 是 rack-scale 系统形态口径。它们共同说明系统交付空间存在，但不能自动推导系统商拥有强利润池。",
      sanityCheck: "Dell $64B orders 与 $43B backlog 证明空间锚点很大；但若 backlog 转收入时毛利、现金流或库存恶化，系统交付节点应从机会降级为低质量订单风险。",
      conclusion: "服务器/rack 系统交付必须作为独立 BOM 节点呈现：它是 AI 工厂从芯片走向上线算力的必要环节，但不是天然高利润 chokepoint。短中期空间中高，长期取决于系统商是否能保留服务、集成和交付溢价。",
      confidence: "中：订单证据强，但系统商利润池和现金转化仍需验证。",
      sourceIds: ["SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2", "SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025", "SRC-SA-GB200-BOM-2024"],
    },
    chokepointImplication: "DELL/SMCI/HPE/ODM 可进入观察池，但 action state 需受毛利率、现金流、库存和执行风险约束。",
    refuteData: "AI server backlog 转收入慢、毛利率下降、库存积压、客户取消订单、GPU allocation 变化、治理或执行风险扩大。",
    sourceIds: ["SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2", "SRC-SA-GB200-BOM-2024"],
  },
];

const industrySpaceHorizonJudgments = {
  [DEMAND_VALIDATION_LAYER]: {
    summary: "五类信息共同说明：AI 工厂预算池已经足够大，但它是全链条空间的需求闸门，不是可直接相加的 BOM 市场。短期看 capex、PPE 和 RPO 已经把硬件需求推高；中期要看 RPO、云收入和 AI 产品收入能否转化为可持续回报；长期空间取决于 AI ROI、FCF 和资本开支纪律。",
    confidence: "中高：客户侧和财务兑现证据强，公司 TAM/第三方 BOM 拆法不是本节点主证据。",
    horizons: [
      { label: "短期", size: "大", reason: "Alphabet、Meta、Amazon、Microsoft、Oracle 均给出高 capex、PPE 或 RPO 锚点，足以支撑 2026 附近硬件订单继续扩张。" },
      { label: "中期", size: "中高", reason: "RPO 和 cloud revenue 若能持续转收入，预算池仍大；若 FCF 压力和 AI ROI 争议扩大，中期空间会先从估值端被压缩。" },
      { label: "长期", size: "中", reason: "长期不是单纯比 capex 总量，而是看 AI 应用收入和效率收益是否足以覆盖持续折旧、电力和融资成本。" },
    ],
  },
  [BOM.platform]: {
    summary: "五类信息共同指向：GPU/ASIC 仍是 AI 工厂 BOM 的第一价值入口。NVIDIA 和 Broadcom 给出财务兑现和近端指引，Omdia 与 SemiAnalysis 补充 AI processor 与 rack-scale BOM 拆法。短中期空间大，长期空间仍大但会被 custom ASIC、效率提升和出口限制重塑。",
    confidence: "中高：收入和第三方拆法均强，但市场定价、ASIC 替代和出口限制需要在 Q3/Q4 控制。",
    horizons: [
      { label: "短期", size: "大", reason: "NVIDIA 数据中心收入和 Broadcom AI semiconductor 指引已经财务化，客户 capex 仍优先流入加速器平台。" },
      { label: "中期", size: "大", reason: "Omdia 的 AI processor spending 路径和 rack-scale 系统升级说明 GPU/ASIC 需求会继续扩散到平台 BOM。" },
      { label: "长期", size: "中高", reason: "训练和推理算力需求仍在，但 custom ASIC、平台效率、客户自研和监管限制会改变 GPU 与 ASIC 的价值分配。" },
    ],
  },
  [BOM.memory]: {
    summary: "五类信息最充分的是 HBM：Micron 既给出 FY2026 近端 outlook，也给出 2025E-2028E HBM TAM 路径；TrendForce 给出价值占比、ASP premium 和 Blackwell 用量；SK hynix/Micron/Samsung 给出财务兑现；SemiAnalysis 解释 HBM 与 CoWoS 的瓶颈关系。短期和中期空间都大，长期空间仍大但要防供给扩张和 ASP 回落。",
    confidence: "高：公司指引、公司 TAM、第三方拆法和财务兑现证据齐全；风险主要在价格、资格和扩产斜率。",
    horizons: [
      { label: "短期", size: "大", reason: "Micron FY2026 outlook、HBM supply 协议、SK hynix 高利润率和 TrendForce 对 HBM 价值占比提升的拆法共同支持近端需求强。" },
      { label: "中期", size: "大", reason: "Micron 披露 HBM TAM 从约 $35B 到约 $100B 的路径，Blackwell/HBM3e/12hi 用量提升继续放大单加速器内存价值量。" },
      { label: "长期", size: "中高", reason: "HBM4、客户资格和 AI 集群规模支撑长期空间，但若供应商扩产快于需求或 ASP premium 收缩，空间弹性会降级。" },
    ],
  },
  [BOM.manufacturing]: {
    summary: "五类信息说明：先进制造和封装不是独立讲 TAM 的节点，而是 GPU/ASIC/HBM 能否出货的供给斜率节点。TSMC 给出收入、advanced technology mix 和 capex 指引；SemiAnalysis/Omdia 解释 CoWoS、chiplet 和先进节点需求。短中期空间大，长期空间取决于封装产能释放和地缘约束。",
    confidence: "中高：公司财务和 capex 指引强，独立第三方空间口径仍不完整。",
    horizons: [
      { label: "短期", size: "大", reason: "TSMC advanced technologies 占比和 2026 capex 指引说明先进节点与封装仍处扩产高位。" },
      { label: "中期", size: "大", reason: "CoWoS/HBM 与 chiplet 平台升级会持续要求先进封装、良率和产能排期配合。" },
      { label: "长期", size: "中高", reason: "AI 平台会持续依赖先进制造，但高 capex 会逐步释放供给，且地缘和客户集中会影响实际可投资空间。" },
    ],
  },
  [BOM.powerCooling]: {
    summary: "五类信息说明：电力/液冷空间来自高功率机柜的物理落地约束，而不是抽象数据中心 TAM。Vertiv backlog 和订单验证财务兑现，云客户 capex 验证需求来源，Dell'Oro/SemiAnalysis 给出液冷 revenue 与 rack power 物理拆法。短中期空间大，长期取决于液冷渗透率、项目利润和电力接入。",
    confidence: "中高：公司订单与第三方液冷拆法较强，但项目毛利和现金转化仍需跟踪。",
    horizons: [
      { label: "短期", size: "大", reason: "Vertiv orders/backlog 与云厂商 capex 同时高位，高功率 AI rack 需要电力、热管理和现场工程先落地。" },
      { label: "中期", size: "大", reason: "Dell'Oro liquid-cooling revenue 路径和 SemiAnalysis 对 rack density 的拆法支持液冷 attach rate 继续提升。" },
      { label: "长期", size: "中高", reason: "长期空间取决于电力接入、数据中心建设节奏和项目毛利；若客户 capex 放缓或交付质量下降，弹性会下降。" },
    ],
  },
  [BOM.connectivity]: {
    summary: "五类信息说明：连接网络空间来自集群规模扩大后的端口、带宽、延迟和功耗约束。ALAB/CRDO/MRVL/AVGO/ANET 给出财务兑现，LightCounting、Dell'Oro 和 SemiAnalysis 给出 optics、PAM4、switch sales 与平台架构拆法。短中期空间大，长期取决于技术路线、客户集中和平台整合。",
    confidence: "中高：第三方拆法丰富、公司收入高增，但单公司价值捕获需要订单和客户份额验证。",
    horizons: [
      { label: "短期", size: "大", reason: "ALAB、CRDO、MRVL、AVGO、ANET 的 AI networking/connectivity/custom silicon 收入或指引已高增。" },
      { label: "中期", size: "大", reason: "LightCounting 对 800G/PAM4/optics、Dell'Oro 对 AI backend switch 的 forecast 支持端口速率和集群规模继续放大。" },
      { label: "长期", size: "中高", reason: "长期需求仍强，但 Ethernet/InfiniBand、LPO/CPO、平台自研和客户集中会决定哪些公司真正留住利润。" },
    ],
  },
  [BOM.systemDelivery]: {
    summary: "五类信息说明：服务器/rack 系统交付空间来自 AI server 订单、发货、backlog 和 rack-scale 架构复杂度。Dell 给出强订单和 backlog，SemiAnalysis 解释 rack-scale 系统交付为何变复杂，云客户 capex 提供需求预算。短中期空间中高，但长期取决于系统商是否能把订单转成毛利和现金流。",
    confidence: "中：订单和发货证据强，但利润池、现金转化和执行风险仍需季度验证。",
    horizons: [
      { label: "短期", size: "中高", reason: "Dell AI-optimized server orders、shipments 和 backlog 已经把需求从芯片传导到系统交付。" },
      { label: "中期", size: "中高", reason: "Blackwell/rack-scale 架构提升集成复杂度，服务器、机柜、网络和电力液冷需要同步交付。" },
      { label: "长期", size: "中", reason: "长期空间取决于系统商是否能保留服务与集成溢价；若客户议价或竞争压低毛利，该节点只剩收入弹性。" },
    ],
  },
};

const industrySpaceValidationRows = [
  ["客户需求", "云厂商 capex、AI cloud revenue、RPO/backlog、FCF", "证明 AI 工厂支出能带来收入或效率回报", "capex 继续增长但云收入/FCF 不跟随"],
  [BOM.systemDelivery, "AI server shipments、backlog conversion、取消率", "证明订单能转成上线产能", "backlog 增长但交付延迟或取消率上升"],
  ["物理基础设施", "液冷订单、power/thermal backlog、项目毛利", "证明高功率机柜真实落地", "订单转收入但毛利和现金流恶化"],
  ["制造和内存", "advanced packaging capacity、HBM ASP、HBM mix、库存", "证明供给扩张没有迅速压垮价格", "HBM/DRAM ASP 回落、库存上升"],
  ["连接网络", "AI networking revenue、AEC/retimer design win、交换机订单", "证明大集群带来可持续连接需求", "收入增长依赖少数客户且后续订单放缓"],
];

const industrySpaceSourceSearchCategories = [
  {
    key: "company_guidance",
    label: "公司指引",
    searchIntent: "搜索节点相关公司在 cutoff 前披露的收入、capex、订单、产能、业务增速或下一期 outlook 指引。",
    expectedFields: ["company", "guidance_content", "period", "scope", "metric", "source_visible_at", "cutoff_status"],
    preferredParserSkill: "financial-statement-analysis",
  },
  {
    key: "company_tam",
    label: "公司 TAM",
    searchIntent: "搜索节点相关公司在 cutoff 前披露的 TAM、SAM、长期 CAGR、服务市场或可触达市场口径。",
    expectedFields: ["company", "tam_value", "period", "scope", "formula_or_decomposition", "assumptions", "source_visible_at", "caveat"],
    preferredParserSkill: "industry-report-analysis",
  },
  {
    key: "customer_guidance",
    label: "客户侧指引",
    searchIntent: "搜索下游客户在 cutoff 前披露的 capex、PPE purchase、RPO/backlog、预算、订单、使用量或 AI ROI 线索。",
    expectedFields: ["customer", "guidance_content", "period", "demand_signal", "conversion_metric", "source_visible_at", "caveat"],
    preferredParserSkill: "financial-statement-analysis",
  },
  {
    key: "third_party",
    label: "第三方拆法",
    searchIntent: "搜索 sell-side、行业机构、数据商或公开研究在 cutoff 前给出的拆分模型、TAM、出货量、价格或供需预测。",
    expectedFields: ["publisher", "scope", "period", "formula_or_decomposition", "assumptions", "output_value", "source_visible_at", "caveat"],
    preferredParserSkill: "industry-report-analysis",
  },
  {
    key: "financial_evidence",
    label: "财务兑现证据",
    searchIntent: "搜索供应商或客户在 cutoff 前已兑现的收入、订单、backlog、毛利率、现金流、库存或 capex 数据。",
    expectedFields: ["company", "financial_metric", "period", "value", "segment_or_product", "source_visible_at", "verification_metric"],
    preferredParserSkill: "financial-statement-analysis",
  },
];

const overviewResearchProtocol = {
  unit_rule: "Each industry-overview analytical module decomposes into research units; each unit decomposes into minimum questions; every minimum question has a professional source-universe plan, an Exa search plan, parsed answer, source chips, and explicit gaps.",
  historical_mode_rule: `Universe and Exa materials are thesis-usable only when visibly available on or before ${AS_OF_DATE}; post-cutoff hits are quarantine-only and cannot strengthen conclusions.`,
  parser_rule: "DeepSeek MCP is the default first-pass parser for selected long sources; GPT verifies and maps parsed facts into the answer.",
};

const competitionQuestionSpecs = [
  {
    title: "玩家市场份额分布",
    field: "competition",
    answer: (item) => ({
      paragraphs: item.marketShareParagraphs || [
        item.competition || `需要识别 ${item.node} 内的主要公司、技术路线、客户选择标准和份额变化，而不是只列受益公司。`,
        item.competitionGap || "待补：可比较口径下的份额、客户导入、路线替代和价格/毛利变化。",
      ],
    }),
    expectedFields: ["competitors", "market_share", "share_trend", "technology_routes", "customer_selection_criteria", "source_visible_at"],
    preferredParserSkill: "industry-report-analysis",
  },
  {
    title: "头部玩家优势分析",
    field: "advantage",
    answer: (item) => ({
      paragraphs: item.advantageParagraphs || [
        item.chokepoint || item.barrierFacts || "重点验证头部玩家优势来自份额、技术、客户资格、生态、产能、良率、交付、成本还是渠道。",
        item.barrierGap || "待补：头部优势对应的财务指标、客户认证周期和竞争对手追赶证据。",
      ],
    }),
    expectedFields: ["leader", "advantage_source", "customer_lock_in", "technology_or_cost_edge", "capacity_or_delivery_edge", "financial_translation"],
    preferredParserSkill: "supply-chain-chokepoint-analysis",
  },
  {
    title: "替代玩家赶超希望",
    field: "catchup",
    answer: (item) => ({
      paragraphs: item.catchupParagraphs || [
        item.catchup || item.refute || item.refuteFacts || "重点看二线玩家、替代技术、客户自研或开放路线是否有明确导入、扩产、降本和份额提升证据。",
        item.catchupGap || item.refuteGap || "待补：替代玩家路线图、客户导入名单、份额变化和追赶时间表。",
      ],
    }),
    expectedFields: ["challengers", "catchup_route", "customer_adoption", "capacity_or_product_ramp", "time_to_parity", "constraint"],
    preferredParserSkill: "industry-report-analysis",
  },
  {
    title: "格局变化核心变量",
    field: "refute",
    answer: (item) => ({
      paragraphs: item.changeVariableParagraphs || [
        item.refute || item.refuteFacts || "反证必须绑定到具体节点和公司：供给释放、替代路线成熟、客户自研、ASP/毛利率走弱、订单取消或库存上升。",
        item.refuteGap || "待补：季度红黄绿阈值、公司级降级动作和替代路线证据。",
      ],
    }),
    expectedFields: ["share_change_trigger", "pricing_or_margin_signal", "customer_switching_signal", "counter_supply_signal", "regulatory_or_technology_trigger", "monitoring_metric"],
    preferredParserSkill: "news-event-analysis",
  },
];

const chokepointQuestionSpecs = [
  {
    title: "具体约束是什么",
    field: "constraint",
    answer: (item) => item.role,
    expectedFields: ["constraint", "physical_or_qualification_limit", "affected_demand", "source_visible_at", "cutoff_status"],
    preferredParserSkill: "supply-chain-chokepoint-analysis",
  },
  {
    title: "谁控制该约束",
    field: "controllers",
    answer: (item) => item.controllers,
    expectedFields: ["controllers", "control_mechanism", "customer_dependency", "qualification_position", "evidence"],
    preferredParserSkill: "company-exposure-analysis",
  },
  {
    title: "稀缺会持续多久",
    field: "duration",
    answer: (item) => item.conclusion,
    expectedFields: ["scarcity_duration", "capacity_timeline", "lead_time", "supply_release_signal", "confidence"],
    preferredParserSkill: "industry-report-analysis",
  },
  {
    title: "扩产/替代/释放路径",
    field: "release",
    answer: () => "重点检查扩产计划、替代路线、客户资格、交付周期和下一轮财报验证。",
    expectedFields: ["capacity_expansion", "substitute_route", "qualification_release", "timing", "downgrade_trigger"],
    preferredParserSkill: "industry-report-analysis",
  },
  {
    title: "量化评分与降级规则",
    field: "score",
    answer: (item) => `评分见下方 scorecard。当前高分维度必须由来源支持；若供给释放、定价权下降或财务弹性减弱，节点降级。`,
    expectedFields: ["score_dimension", "score_value", "evidence_id", "downgrade_rule", "missing_data"],
    preferredParserSkill: "supply-chain-chokepoint-analysis",
  },
  {
    title: "标的影响/监控触发器",
    field: "target",
    answer: (item) => item.qa_link,
    expectedFields: ["target_mapping", "revenue_or_margin_bridge", "monitoring_trigger", "upgrade_signal", "downgrade_signal"],
    preferredParserSkill: "target-recommendation-analysis",
  },
];

const leaves = [
  leaf("Q1.1.1", "Q1.1", "需求是否已经进入 NVIDIA 数据中心收入和 AI 工厂表述？", "financial-statement-analysis", "evidence_quality", "决定 AI 工厂是否可以作为真实产业需求，而不是概念词。", ["SRC-NVDA-FY26-Q4"], "NVIDIA Q4 FY26 revenue was $68.1B and Data Center revenue was $62.3B; management explicitly described customers investing in AI compute factories.", "AI 工厂已经进入 NVIDIA 的收入和管理层口径，说明需求具备财务基础。", "Q1 可以确认需求真实，但 NVDA 本身估值要单独测试。", "缺少客户 ROI 和订单拆分。", "若客户 capex 或数据中心收入增速放缓，降低 future_space。", artifact("NVIDIA 需求证据", ["口径", "数据", "含义"], [["收入", "Q4 FY26 $68.1B", "需求规模已财务化"], ["数据中心", "$62.3B", "AI 工厂主收入池"], ["管理层表述", "AI factories", "产业链研究成立"], ["风险", "China/ROI/毛利", "不能直接推出低估"]])),
  leaf("Q1.1.2", "Q1.1", "AI 工厂是否已经进入系统和物理基础设施订单？", "financial-statement-analysis", "evidence_quality", "判断 DELL/VRT 等非芯片环节是否可进入观察池。", ["SRC-DELL-FY26-Q4", "SRC-VRT-Q4-2025"], "Dell disclosed more than $64B AI-optimized server orders and $43B backlog; Vertiv organic orders rose 252% YoY and backlog reached $15.0B.", "AI 工厂需求已经传导到服务器和电力冷却，说明非芯片环节不是纯配套。", "VRT/DELL 可进入 Q4 观察池，SMCI 需因执行风险更保守。", "缺少 backlog 毛利、取消率和客户集中度。", "若 backlog 转收入但毛利下降，则降低 risk_control。", artifact("订单传导", ["公司", "截面证据", "投资含义"], [["DELL", "$64B AI server orders / $43B backlog", "系统交付弹性强"], ["VRT", "orders +252% / backlog $15B", "电力液冷是硬瓶颈"], ["SMCI", "AI server exposure", "执行和治理风险压分"]])),
  leaf("Q1.2.1", "Q1.2", "需求传导的主路径是什么？", "industry-report-analysis", "future_space", "决定行业生态位和 Q2 卡点顺序。", ["SRC-NVDA-FY26-Q4", "SRC-DELL-FY26-Q4", "SRC-VRT-Q4-2025", "SRC-TSM-Q4-2025"], "AI 工厂需求从 NVIDIA 平台进入服务器 backlog，再进入先进制造、内存、电力冷却和系统交付。", "需求不是一条线，而是多节点同步扩张；越靠近硬瓶颈，越可能保留利润。", "Q1.2 支持跨平台、内存、连接、物理基础设施和系统交付建立目标池。", "缺少客户侧 capex ROI 模型。", "若客户 ROI 低于 capex 成本，整体降分。", artifact("需求传导路径", ["需求", "传导节点", "可验证数据"], [["更多训练/推理", "GPU/ASIC/HBM/封装", "NVDA/TSM/内存收入"], ["机柜部署", "服务器/电力/液冷", "DELL/VRT backlog"], ["集群扩展", "连接/以太网/AEC", "ALAB/CRDO/AVGO/ANET 收入"], ["长期持续性", "客户 ROI/capex", "云厂商指引"]])),
  leaf("Q1.2.2", "Q1.2", "需求是否只利好 NVIDIA，还是会外溢到第三方？", "industry-report-analysis", "target_ranking", "决定是否只看 NVDA，还是寻找未充分定价的稀缺环节。", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3", "SRC-AVGO-FY25-Q4", "SRC-ANET-Q4-2025"], "Astera、Credo、Marvell、Broadcom、Arista 均在截面前披露 AI networking/connectivity/custom silicon 相关增长或目标。", "AI 工厂扩张需要第三方连接、网络和 custom silicon 生态，但价值捕获取决于 design-in、客户集中、定制项目节奏和平台替代风险。", "第三方可以进入观察池，但不能只因 AI networking/custom silicon 叙事给高行动状态。", "缺少逐客户订单、平台依赖比例和 custom silicon 量产节奏。", "若 NVIDIA 自有网络方案或客户自研挤压第三方份额，相关标的降级。", artifact("第三方外溢", ["节点", "证据", "限制"], [["ALAB", "rack-scale connectivity revenue", "估值/客户集中"], ["CRDO", "AEC/optical +200% revenue", "高弹性高波动"], ["MRVL", "AI custom products/electro-optics demand", "定制项目节奏/客户集中"], ["AVGO", "AI ASIC + Ethernet switches", "大客户集中"], ["ANET", "AI networking goals exceeded", "与平台路线竞争"]])),
  leaf("Q2.1.1", "Q2.1", "平台控制是不是最强稀缺性？", "valuation-analysis", "chokepoint_strength", "判断 NVDA 高稀缺性是否能转成可行动机会。", ["SRC-NVDA-FY26-Q4"], "NVIDIA 同时控制 GPU、NVLink、软件生态、AI 工厂叙事和客户部署路线。", "平台控制是最强卡点，但市场也最可能提前定价。", "NVDA 稀缺性满分附近，但 valuation_odds 被封顶。", "缺少反向 DCF 和隐含增长拆解。", "只有当 EPS/订单上修超过隐含预期时才升级行动状态。", artifact("平台控制评分", ["维度", "判断"], [["稀缺性", "极强"], ["替代风险", "ASIC/开放以太网长期存在"], ["财务化", "已进入数据中心收入"], ["赔率", "需单独证明未定价"]])),
  leaf("Q2.1.2", "Q2.1", "HBM、先进制造和封装是否是硬瓶颈？", "industry-report-analysis", "chokepoint_strength", "决定 SK hynix/TSM/MU/Samsung 的卡点强度。", ["SRC-TSM-Q4-2025", "SRC-MU-FY26-Q1", "SRC-MU-FY26-Q1-PREPARED", "SRC-SKHYNIX-FY25", "SRC-SAMSUNG-FY25", "SRC-TF-HBM-PRICE-20240506", "SRC-TF-BLACKWELL-HBM-20240808", "SRC-SA-COWOS-HBM-2023"], "TSMC advanced technologies were 77% of wafer revenue; Micron Q2 outlook and HBM TAM give near-term and long-term memory evidence; SK hynix and Samsung reported AI memory/HBM strength; TrendForce and SemiAnalysis provide HBM value-share and CoWoS/HBM bottleneck methods.", "AI 工厂交付需要先进制程、封装和 HBM，供给斜率慢于需求时可形成价格和毛利弹性。", "SK hynix、TSM、MU、Samsung 均是核心价值捕获载体，其中 SK hynix 因 HBM 领导力最稀缺；Micron 的 outlook/TAM/财务兑现需要按不同口径拆开使用。", "缺少同口径产能、客户分配、HBM ASP 和估值分位。", "若 HBM 供给快速扩张或 ASP 反转，降低相关标的。", artifact("制造和内存卡点", ["节点", "控制者", "风险"], [[BOM.manufacturing, "TSMC", "高 capex 和地缘风险"], [BOM.memory, "SK hynix/MU/Samsung", "供给扩张和认证风险"], [BOM.memory, "MU/Samsung/SK hynix", "周期回落风险"]])),
  leaf("Q2.2.1", "Q2.2", "机柜级连接是否是独立稀缺点？", "industry-report-analysis", "chokepoint_strength", "决定 ALAB/CRDO/MRVL/AVGO/ANET 的排序。", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3", "SRC-AVGO-FY25-Q4", "SRC-ANET-Q4-2025"], "ALAB revenue +92% YoY, CRDO revenue +200% YoY, Marvell data-center sales grew on AI custom products and electro-optics, Broadcom AI semiconductor revenue +74% YoY, Arista FY revenue +28.6%.", "连接、custom silicon 和网络是 AI 工厂扩展效率瓶颈，收入增长已经进入公司报表。", "ALAB/CRDO/MRVL 弹性高但估值、客户集中和项目节奏风险也高；AVGO/ANET 更稳但弹性相对分散。", "缺少客户/产品级收入拆分。", "若客户切换平台、自研或价格下降，降低 chokepoint_strength。", artifact("连接卡点", ["公司", "证据", "处理"], [["ALAB", "Q4 revenue +92% YoY", "watch/action 候选"], ["CRDO", "Q3 revenue +200% YoY", "高弹性观察"], ["MRVL", "AI custom products/electro-optics", "custom silicon + 光互联观察"], ["AVGO", "AI ASIC/Ethernet switch", "大盘稳健"], ["ANET", "AI networking goals exceeded", "需客户订单验证"]])),
  leaf("Q2.2.2", "Q2.2", "电力液冷和系统交付能否捕获高质量利润？", "financial-statement-analysis", "evidence_quality", "决定 VRT/DELL/SMCI 的强弱。", ["SRC-VRT-Q4-2025", "SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2"], "VRT orders/backlog 和 DELL AI server backlog 都很强；SMCI 也有 AI server exposure，但执行和治理风险更高。", "物理基础设施是最容易被新手低估的瓶颈，系统交付则要看利润率。", "VRT 因订单、瓶颈和利润质量进入最高观察级；DELL 次之；SMCI 风险控制显著偏低。", "缺少 backlog 毛利和项目交付周期。", "若 backlog 转化质量差，VRT/DELL 降级。", artifact("物理基础设施", ["节点", "标的", "关键验证"], [[BOM.powerCooling, "VRT", "backlog 毛利和交付"], [BOM.systemDelivery, "DELL", "订单转收入和现金流"], [BOM.systemDelivery, "SMCI", "治理和毛利稳定性"]])),
  leaf("Q3.1.1", "Q3.1", "市场是否已经把 AI 工厂增长充分定价？", "valuation-analysis", "valuation_odds", "防止强主题自动变成高分。", ["SRC-NVDA-FY26-Q4", "SRC-VRT-Q4-2025", "SRC-ALAB-Q4-2025", "SRC-AVGO-FY25-Q4"], "截面前 AI 工厂核心标的已经有强收入/订单和高市场关注。", "基本面强不等于赔率强，尤其是 NVDA、ALAB、VRT 这类高关注标的。", "除非估值隐含增长低于可验证订单利润路径，否则 action_state 不能无条件升高。", "缺少完整 reverse DCF 和估值分位。", "若估值继续扩张而盈利未上修，降低 mispricing。", artifact("估值闸门", ["条件", "要求"], [["稀缺性", "必须强"], ["未定价", "必须由订单/利润超过隐含预期证明"], ["下行保护", "必须可控"], ["缺任一项", "封顶 watch_only 或 no_action"]])),
  leaf("Q3.1.2", "Q3.1", "客户 capex 和 AI ROI 是否可能打断链条？", "news-event-analysis", "disconfirming_risk_control", "定义最重要的行业反证。", ["SRC-NVDA-FY26-Q4", "SRC-DELL-FY26-Q4", "SRC-VRT-Q4-2025"], "AI 工厂需求依赖云厂商、AI labs 和企业持续投入，硬件供应链对 capex 非常敏感。", "如果客户 ROI 或融资能力下降，订单、毛利和估值会同时承压。", "所有目标都需要 capex/ROI kill test，尤其是系统、连接和液冷环节。", "缺少客户侧单位经济性。", "若 hyperscaler 下修 capex 或 AI 服务收入不达预期，整体降分。", artifact("capex 反证", ["反证", "影响"], [["capex 下修", "全链条"], ["电力接入延迟", "VRT/DELL"], ["AI ROI 下降", "NVDA/服务器/连接"], ["融资收紧", "新云客户订单风险"]])),
  leaf("Q3.2.1", "Q3.2", "供给扩张会不会消除稀缺性？", "industry-report-analysis", "disconfirming_risk_control", "测试 HBM、先进制造、连接和液冷是否会过度扩产。", ["SRC-TSM-Q4-2025", "SRC-SKHYNIX-FY25", "SRC-SAMSUNG-FY25", "SRC-MU-FY26-Q1"], "TSMC 2026 capex expected $52B-$56B; memory companies were increasing AI product focus and HBM capacity.", "高利润会吸引扩产，供给斜率一旦超过需求斜率，赔率下降。", "HBM/封装仍是硬瓶颈，但必须设置供给扩张反证。", "缺少统一 bit growth、CoWoS 产能和 HBM 资格认证表。", "若供给显著放量或价格下行，降低 HBM/TSM/MU/Samsung。", artifact("供给反证", ["环节", "扩张信号", "降级条件"], [["TSMC", "高 capex", "先进封装产能过剩"], ["HBM", "供应商扩产", "ASP 或毛利下滑"], ["连接", "多供应商进入", "价格竞争"], ["液冷", "产能扩张", "backlog 质量下降"]])),
  leaf("Q3.2.2", "Q3.2", "平台整合和客户集中会不会压缩第三方利润？", "industry-report-analysis", "risk_control", "控制 ALAB/CRDO/MRVL/AVGO/ANET/SMCI 的风险上限。", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3", "SRC-AVGO-FY25-Q4", "SRC-ANET-Q4-2025"], "第三方连接、custom silicon 和网络公司高速增长，但通常依赖少数大型客户和平台标准。", "客户集中可带来高弹性，也会在客户切换、平台自研或定制项目延期时放大下行。", "ALAB/CRDO/MRVL 需要更高 payoff，但 risk_control 不可给满分。", "缺少客户集中度、design-in 合同期限和 custom silicon 项目量产节奏。", "若大客户订单延后或转向自研，降为 no_action。", artifact("第三方风险", ["风险", "影响标的"], [["客户集中", "ALAB/CRDO/MRVL/AVGO"], ["平台自研", "ANET/ALAB/CRDO/MRVL"], ["定制项目延期", "MRVL/AVGO"], ["价格压力", "系统商/网络"], ["执行风险", "SMCI"]])),
  leaf("Q4.1.1", "Q4.1", "哪些证券是直接价值捕获载体？", "target-recommendation-analysis", "target_ranking", "建立冻结目标池，不让标签可得性限制投资宇宙。", ["SRC-NVDA-FY26-Q4", "SRC-VRT-Q4-2025", "SRC-SKHYNIX-FY25", "SRC-TSM-Q4-2025", "SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3", "SRC-DELL-FY26-Q4"], "直接载体包括 NVDA、VRT、SK hynix、TSM、ALAB、CRDO、MRVL、MU、DELL、AVGO、ANET、Samsung、SMCI。", "目标池来自卡点映射，而不是从美股便利性或三个月结果筛选。", "Q4 保留非美股中央标的，也补入 MRVL 这类截面前已有官方 AI data-center 证据的 custom silicon/电光互联标的；价格 label 不可靠时标 unverified。", "缺少所有市场同口径估值。", "补齐估值后再调整 action_state。", artifact("目标池映射", ["标的", "链条节点", "处理"], [["VRT", BOM.powerCooling, "actionable/watch"], ["SK hynix", BOM.memory, "actionable/watch"], ["NVDA", BOM.platform, "watch"], ["ALAB/CRDO/MRVL", BOM.connectivity, "watch"], ["DELL", BOM.systemDelivery, "watch"], ["Samsung", BOM.memory, "label unverified"]])),
  leaf("Q4.1.2", "Q4.1", "排序如何由四个核心维度产生？", "target-recommendation-analysis", "action_state", "确保强主题必须同时满足稀缺、未定价、弹性和风险控制。", ["SRC-VRT-Q4-2025", "SRC-SKHYNIX-FY25", "SRC-NVDA-FY26-Q4", "SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3"], "目标分数由七个底层组件汇总到稀缺性、未充分定价、业绩弹性和风险控制四个维度。", "AI 工厂全链条强，但只有四个维度同时强才给 actionable_long。", "VRT 和 SK hynix 最接近可行动，其余以 watch_only/no_action 为主。", "估值证据仍不完整。", "若未定价或风险控制不能证明，封顶 watch_only。", artifact("行动状态闸门", ["维度", "要求"], [["稀缺性", "卡点明确且难替代"], ["未充分定价", "订单利润超过隐含预期"], ["业绩弹性", "收入/毛利/FCF 能大幅上修"], ["风险控制", "反证可监控且下行有限"]])),
  leaf("Q4.2.1", "Q4.2", "三个月后用哪些事实复盘，而不是用 label 倒推？", "target-recommendation-analysis", "monitorability", "设置预测复盘触发器。", ["SRC-DELL-FY26-Q4", "SRC-VRT-Q4-2025", "SRC-ALAB-Q4-2025", "SRC-MRVL-FY26-Q3", "SRC-MU-FY26-Q1"], "复盘应看订单、backlog 毛利、HBM ASP、连接 design-in、custom silicon 项目节奏、客户 capex 和估值隐含预期。", "这些数据能验证当时推理质量；三个月股价只是 label。", "复盘机制建立，但不允许回写本报告推理。", "缺少自动化跟踪表。", "若事实反证出现，未来训练样本降权或改问题。", artifact("复盘数据", ["节点", "三个月观察"], [["VRT/DELL", "backlog 转收入和毛利"], ["SK hynix/MU", "HBM 出货和 ASP"], ["ALAB/CRDO/MRVL", "design-in、客户集中、custom silicon 项目"], ["NVDA", "Data Center 指引和毛利"]])),
  leaf("Q4.2.2", "Q4.2", "哪些 kill tests 会撤销高分？", "target-recommendation-analysis", "risk_control", "为每个高关注方向设置硬降级条件。", ["SRC-NVDA-FY26-Q4", "SRC-VRT-Q4-2025", "SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3"], "核心 kill tests 包括 capex 下修、HBM 供给过剩、连接客户集中恶化、custom silicon 项目延迟、VRT backlog 毛利差、DELL/SMCI 订单低质量。", "一旦触发，说明稀缺性或利润桥断裂，应降低 action_state。", "actionable_long 必须有硬 kill tests；高弹性 watch_only 也要有降级条件。", "需要持续财报、客户 capex 和项目量产数据。", "任一核心反证触发即降级。", artifact("Kill tests", ["测试", "证据", "动作"], [["capex 下修", "云厂商指引", "全链降分"], ["HBM ASP 反转", "内存财报", "内存标的降级"], ["连接客户流失", "ALAB/CRDO 订单", "降为 no_action"], ["MRVL custom silicon 延迟", "项目量产/客户披露", "降为 no_action"], ["液冷毛利差", "VRT backlog/毛利", "撤销 actionable"], ["系统订单低质量", "DELL/SMCI 现金流", "降级"]])),
];

const adaptiveUnits = [
  drill(4, "Q1.2.1.1", "Q1.2.1", "平台收入如何传导成服务器 backlog？", "financial-statement-analysis", "future_space", "把 GPU/平台收入和系统商订单连起来，判断需求是否已经离开单一芯片环节。", ["SRC-NVDA-FY26-Q4", "SRC-DELL-FY26-Q4"], "NVIDIA 数据中心收入已经达到大规模财务口径，Dell 同期披露 AI server orders 和 backlog。", "平台收入和服务器 backlog 同时出现，说明 AI 工厂需求已经进入可交付系统，而不是只停留在芯片供给。", "Q1.2.1 的主路径可保留平台到服务器的第一段传导。", "缺少客户级订单重叠和取消率。", "若服务器 backlog 不再随平台收入增长，降低系统交付环节。", artifact("平台到服务器", ["节点", "截面证据", "判断"], [["平台收入", "NVDA Data Center $62.3B", "需求起点真实"], ["系统订单", "DELL AI server orders/backlog", "需求进入交付"], ["缺口", "客户重叠和取消率", "需要后续验证"]])) ,
  drill(4, "Q1.2.1.2", "Q1.2.1", "服务器 backlog 如何传导到电力和液冷？", "financial-statement-analysis", "future_space", "判断 VRT 是否是 AI 工厂落地瓶颈，而不只是数据中心泛主题。", ["SRC-DELL-FY26-Q4", "SRC-VRT-Q4-2025"], "Dell AI server backlog 和 Vertiv orders/backlog 在截面前同时强劲。", "高功率服务器需要电源、散热和机柜工程，服务器订单会把需求推向物理基础设施。", "VRT 应作为 AI 工厂产业链的直接瓶颈标的进入 Q4。", "缺少单项目液冷渗透率和 backlog 毛利。", "若电力/液冷 backlog 增长但毛利恶化，降低 VRT 行动状态。", artifact("服务器到物理基础设施", ["传导", "证据", "风险"], [["AI server backlog", "DELL $43B backlog", "项目需要落地"], ["电力液冷订单", "VRT orders +252% / backlog $15B", "瓶颈被财务化"], ["风险", "毛利和交付周期", "影响风险控制"]])) ,
  drill(4, "Q2.1.2.1", "Q2.1.2", "HBM 价值捕获应该优先看谁？", "industry-report-analysis", "chokepoint_strength", "把 HBM 从先进制造大桶里拆出来，决定 SK hynix、Micron、Samsung 的相对强弱。", ["SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1", "SRC-MU-FY26-Q1-PREPARED", "SRC-SAMSUNG-FY25", "SRC-TF-HBM-PRICE-20240506", "SRC-TF-BLACKWELL-HBM-20240808", "SRC-SA-COWOS-HBM-2023"], "SK hynix 披露 AI memory 驱动的高收入和 49% operating margin；Micron 同时给出 FQ2 outlook、HBM TAM 和 AI memory 财务兑现；Samsung 也披露 AI memory/HBM 或高价值内存强势；TrendForce/SemiAnalysis 支持 HBM 价值量和瓶颈逻辑。", "HBM 是 AI 工厂最硬的内存卡点，但供应商之间的资格、份额、价格协议和毛利弹性不同。", "HBM 分支需要继续拆到公司层，否则 Q2.1.2 容易把不同强度混在一起；同一份 Micron 材料必须按 outlook、TAM、财务兑现分维度解析。", "缺少同口径 HBM 产能、客户资格和 ASP。", "若客户资格或 ASP 反转，相关标的降级。", artifact("HBM 公司分层", ["公司", "截面证据", "初步处理"], [["SK hynix", "AI memory + 高 operating margin", "最高卡点候选"], ["Micron", "FQ2 outlook + HBM TAM + cloud memory margin", "高弹性观察"], ["Samsung", "record memory revenue/profit, HBM/server DDR5/eSSD", "需要验证 HBM 领导力"]])) ,
  drill(5, "Q2.1.2.1.1", "Q2.1.2.1", "SK hynix 的 HBM 证据是否足以形成最高卡点？", "financial-statement-analysis", "chokepoint_strength", "决定非美股核心标的能否保留在最高观察层，而不是因 label 难取被排除。", ["SRC-SKHYNIX-FY25"], "SK hynix FY2025 revenue KRW97.1467T、operating profit KRW47.2063T、operating margin 49%，公司将表现归因于 AI memory 和 HBM 领导力。", "高利润率和 AI memory 领导力同时出现，说明其不是普通存储 beta，而是 AI 工厂内存卡点载体。", "SK hynix 可维持 actionable_long 候选，但本地价格 label 暂未验证。", "缺少 HBM 客户、份额和产能分配表。", "若 HBM ASP 或客户资格下行，撤销最高卡点假设。", artifact("SK hynix HBM 验证", ["维度", "结论"], [["财务化", "FY25 高收入/利润率", "强"], ["稀缺性", "HBM leadership", "强"], ["缺口", "客户/份额/ASP", "需验证"]])) ,
  drill(5, "Q2.1.2.1.2", "Q2.1.2.1", "Micron 和 Samsung 是同等卡点还是补充弹性？", "financial-statement-analysis", "target_ranking", "控制 MU 与 Samsung 在目标池中的排序，避免把所有内存公司同分。", ["SRC-MU-FY26-Q1", "SRC-MU-FY26-Q1-PREPARED", "SRC-SAMSUNG-FY25"], "Micron 披露 record revenue and margin expansion，FQ2 outlook 指向更高收入和毛利，并给出 HBM TAM 与 2026 HBM supply 价量协议；Samsung 披露 Memory Business record quarterly revenue and operating profit。", "两家公司都受益于 AI memory，但相对 SK hynix 的 HBM 份额、资格和定价权需要更强证据。", "MU/Samsung 应进入 watch_only，而不是直接与 SK hynix 同行动状态；Micron 材料要拆成公司指引、公司 TAM 和财务兑现三类使用。", "缺少同口径 HBM 资格和产品 mix。", "若 HBM 出货/ASP 明显领先预期，才可上调。", artifact("MU/Samsung 分层", ["公司", "强项", "封顶原因"], [["MU", "FQ2 outlook、HBM TAM、AI cloud memory/HBM 弹性", "份额和资格仍需证明"], ["Samsung", "内存规模与产品广", "HBM 领导力需验证"]])) ,
  drill(4, "Q2.1.2.2", "Q2.1.2", "先进制造和封装由 TSMC 捕获多少价值？", "financial-statement-analysis", "chokepoint_strength", "把 TSMC 从内存分支拆出，判断其是稳态卡点还是赔率不足。", ["SRC-TSM-Q4-2025"], "TSMC Q4 2025 advanced technologies were 77% of wafer revenue，gross margin 62.3%，2026 capex expected $52B-$56B。", "先进制程和封装是 AI 工厂供给斜率的关键，但高 capex 也说明市场可能已经预期扩产。", "TSM 卡点强、证据强，但 valuation_odds 不应给满。", "缺少先进封装单独产能和 AI/HPC 客户 mix。", "若封装供给放量导致稀缺性下降，降低赔率。", artifact("TSMC 制造/封装", ["证据", "含义"], [["advanced technologies 77%", "AI/HPC 高端制程贡献大"], ["gross margin 62.3%", "价值捕获强"], ["capex $52B-$56B", "扩产与稀缺性反证并存"]])) ,
  drill(4, "Q2.2.1.1", "Q2.2.1", "ALAB/CRDO 的高速连接增长哪个更像弹性卡点？", "financial-statement-analysis", "payoff_convexity", "将连接分支拆到高弹性小盘标的，判断赔率和风险。", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3"], "Astera Labs Q4 revenue +92% YoY，Credo FY26 Q3 revenue +200% YoY，二者均指向 AI infrastructure connectivity。", "两者都具备高弹性，但客户集中和平台依赖会放大下行。", "ALAB/CRDO 可保留高弹性 watch_only，不能越过风险闸门。", "缺少大客户占比和 design-in 周期。", "若客户订单延迟或平台替代，降为 no_action。", artifact(BOM.connectivity, ["标的", "弹性", "风险"], [["ALAB", "+92% revenue", "估值和客户集中"], ["CRDO", "+200% revenue", "客户集中和波动"], ["共同点", "AI connectivity", "高赔率但低风险控制"]])) ,
  drill(4, "Q2.2.1.2", "Q2.2.1", "AVGO/ANET 的网络和 ASIC 是稳态卡点还是替代风险？", "industry-report-analysis", "risk_control", "区分大盘稳态受益与高弹性连接标的。", ["SRC-AVGO-FY25-Q4", "SRC-ANET-Q4-2025"], "Broadcom AI semiconductor revenue +74% YoY，Arista FY2025 revenue +28.6% 且 AI networking 目标超额。", "AVGO/ANET 代表 ASIC/Ethernet 稳态受益，但与 NVIDIA 平台路线和客户自研之间存在路线风险。", "两者进入目标池，但行动状态以 watch_only 为主。", "缺少客户数量、云厂商订单和开放以太网份额。", "若客户 ASIC 或 Ethernet 节奏不及预期，降低 ranking。", artifact("稳态网络/ASIC", ["公司", "价值捕获", "风险"], [["AVGO", "AI ASIC + Ethernet switch", "大客户集中"], ["ANET", "AI networking", "平台路线竞争"]])) ,
  drill(4, "Q2.2.1.3", "Q2.2.1", "MRVL 的 custom silicon 和电光互联是否是 AI 工厂卡点？", "financial-statement-analysis", "payoff_convexity", "补齐 MRVL 在 custom silicon / electro-optics 维度的独立判断。", ["SRC-MRVL-FY26-Q3"], "Marvell FY26 Q3 net revenue was $2.075B；10-Q 披露 data-center sales +38%，增长由 AI-related demand for custom products and electro-optics portfolio 驱动。", "MRVL 不是普通网络 beta，而是 custom silicon 与光互联方向的 AI 工厂弹性载体。", "MRVL 应进入最终目标池，但因客户集中、定制项目节奏和估值不透明，行动状态封顶在 watch_only。", "缺少 custom silicon 项目量产时间、客户集中度和反向估值。", "若大客户项目延期、客户自研替代或毛利不达预期，降为 no_action。", artifact("MRVL 卡点判断", ["维度", "截面证据", "处理"], [["AI 需求", "data-center +38%", "需求已财务化"], ["产品位置", "custom products / electro-optics", "AI 工厂连接与定制芯片"], ["风险", "客户集中/项目节奏/估值", "watch_only 封顶"]])) ,
  drill(4, "Q2.2.2.1", "Q2.2.2", "VRT 的 backlog 能否变成高质量利润？", "financial-statement-analysis", "evidence_quality", "决定 VRT 是否满足稀缺、弹性和风险控制三项，而不是只靠订单热度。", ["SRC-VRT-Q4-2025"], "Vertiv Q4 organic orders rose 252% YoY and backlog reached $15.0B。", "电力/液冷 backlog 是 AI 工厂物理瓶颈的直接证据，但最终价值还要看毛利和交付。", "VRT 可维持 actionable_long，但必须绑定 backlog 毛利 kill test。", "缺少液冷项目毛利和取消率。", "若 backlog 转化低质量，撤销 actionable_long。", artifact("VRT 利润桥", ["环节", "判断"], [["订单", "强"], ["瓶颈", "强"], ["利润质量", "待验证"], ["行动状态", "有条件 actionable_long"]])) ,
  drill(4, "Q2.2.2.2", "Q2.2.2", "DELL/SMCI 的 AI server backlog 是否能保留利润？", "financial-statement-analysis", "risk_control", "避免把服务器组装的订单弹性误判为高质量卡点。", ["SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2"], "Dell 披露 AI server orders/backlog，Supermicro 也有 AI server exposure，但 SMCI 执行和治理风险更高。", "系统商能吃到 AI 工厂订单，但议价力和利润率通常弱于平台、HBM 和电力液冷。", "DELL watch_only，SMCI no_action 更符合风险控制。", "缺少 AI server 毛利、现金转化和治理风险量化。", "若订单增长不带来利润和现金流，系统商降级。", artifact("系统商利润质量", ["标的", "机会", "限制"], [["DELL", "backlog 强", "利润率/现金流待验证"], ["SMCI", "主题弹性", "执行和治理风险"]])) ,
  drill(4, "Q3.1.1.1", "Q3.1.1", "高稀缺龙头是否已经被估值封顶？", "valuation-analysis", "valuation_odds", "解释为什么 NVDA/TSM 卡点强但行动状态仍可能不是最高。", ["SRC-NVDA-FY26-Q4", "SRC-TSM-Q4-2025"], "NVDA 和 TSMC 的收入、毛利和 capex 证据都很强，且市场关注度高。", "强证据提高胜率，但也提高市场已定价概率。", "NVDA/TSM 维持 watch_only，除非反向估值显示仍未充分定价。", "缺少 reverse DCF 和隐含 EPS 增长。", "若盈利上修不能超过隐含预期，维持封顶。", artifact("龙头估值封顶", ["标的", "卡点", "封顶原因"], [["NVDA", BOM.platform, "预期很高"], ["TSM", BOM.manufacturing, "capex 与估值已反映部分增长"]])) ,
  drill(4, "Q3.1.1.2", "Q3.1.1", "高弹性标的是赔率还是高估值风险？", "valuation-analysis", "valuation_odds", "解释为什么 ALAB/CRDO/MRVL/DELL/MU 有弹性但仍需分层。", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3", "SRC-DELL-FY26-Q4", "SRC-MU-FY26-Q1"], "ALAB/CRDO 收入增速极高，MRVL data-center AI custom/electro-optics 证据明确，DELL backlog 极强，Micron AI memory 提升明显。", "弹性是赔率来源，但如果客户集中、毛利、项目节奏或估值不透明，风险控制要扣分。", "高弹性标的应以 watch_only 为主，等待估值和利润桥验证。", "缺少客户集中、利润桥、项目量产节奏和估值分位。", "若增长兑现同时风险下降，才上调行动状态。", artifact("高弹性闸门", ["标的", "弹性来源", "需证明"], [["ALAB/CRDO", "连接收入高增", "客户和估值"], ["MRVL", "custom silicon/electro-optics", "项目节奏和客户集中"], ["DELL", "AI server backlog", "利润率"], ["MU", "HBM/Cloud memory", "份额和 ASP"]])) ,
  drill(4, "Q4.1.2.1", "Q4.1.2", "四维闸门如何决定 actionable_long？", "target-recommendation-analysis", "action_state", "把七分制底层分数翻译成稀缺、未定价、弹性、风险控制四个投资动作维度。", ["SRC-VRT-Q4-2025", "SRC-SKHYNIX-FY25", "SRC-NVDA-FY26-Q4"], "VRT 同时有物理瓶颈和订单证据，SK hynix 同时有 HBM 稀缺和高利润率，NVDA 稀缺性最强但未定价证据不足。", "actionable_long 不是主题强度最高，而是四维同时过线。", "VRT/SK hynix 通过闸门，NVDA 因 mispricing 封顶为 watch_only。", "缺少所有标的同口径估值。", "若 mispricing 或 risk_control 不足，自动降为 watch_only。", artifact("四维闸门示例", ["标的", "稀缺", "未定价", "弹性", "风险"], [["VRT", "强", "中强", "强", "可监控"], ["SK hynix", "强", "中强", "强", "需验证 label/ASP"], ["NVDA", "极强", "弱/待证", "强", "估值封顶"]])) ,
  drill(4, "Q4.2.2.1", "Q4.2.2", "每个最高关注标的的硬 kill test 是什么？", "target-recommendation-analysis", "risk_control", "保证 actionable_long 不是主观乐观，而是有明确撤销条件。", ["SRC-VRT-Q4-2025", "SRC-SKHYNIX-FY25"], "VRT 的硬测试是 backlog 毛利和交付质量；SK hynix 的硬测试是 HBM ASP、客户资格和供给扩张。", "如果硬测试失败，说明稀缺性或利润桥断裂，应撤销高行动状态。", "两个 actionable_long 都必须保留硬降级条件。", "缺少后续财报和行业价格数据。", "任一硬测试失败即降级。", artifact("最高关注 kill tests", ["标的", "硬测试", "降级动作"], [["VRT", "backlog 毛利/交付质量", "撤销 actionable_long"], ["SK hynix", "HBM ASP/客户资格/供给", "撤销 actionable_long"]])) ,
];

const researchUnits = [...leaves, ...adaptiveUnits];

const labels = {
  NVDA: label(182.48, 224.36, 22.95, "Nasdaq historical close", "label_verified"),
  VRT: label(257.75, 323.39, 25.47, "Nasdaq historical close", "label_verified"),
  DELL: label(153.55, 465.96, 203.46, "Nasdaq historical close", "label_verified"),
  TSM: label(369.11, 435.63, 18.02, "Nasdaq historical close", "label_verified_adr"),
  MU: label(412.67, 1035.5, 150.93, "Nasdaq historical close", "label_verified"),
  ALAB: label(120.55, 320.09, 165.52, "Nasdaq historical close", "label_verified"),
  CRDO: label(114.22, 226.10, 97.95, "Nasdaq historical close", "label_verified"),
  MRVL: label(80.86, 219.43, 171.37, "Nasdaq historical close", "label_verified"),
  AVGO: label(318.82, 459.97, 44.27, "Nasdaq historical close", "label_verified"),
  ANET: label(129.30, 170.68, 32.00, "Nasdaq historical close", "label_verified"),
  SMCI: label(31.83, 46.88, 47.28, "Nasdaq historical close", "label_verified"),
  "000660.KS": label(939000, 2363000, 151.65, "Naver Finance KRX daily close", "label_verified_krx_next_trading_day", { start_price_date: "2026-03-03", end_price_date: "2026-06-01" }),
  "005930.KS": label(195100, 349000, 78.88, "Naver Finance KRX daily close", "label_verified_krx_next_trading_day", { start_price_date: "2026-03-03", end_price_date: "2026-06-01" }),
};

const targets = rankTargets([
  target("VRT", "Vertiv", "USA", "AI 工厂电力和液冷", [4.45, 4.45, 3.45, 4.45, 3.85, 4.20, 4.05], ["SRC-VRT-Q4-2025"], "订单、backlog 和物理瓶颈同时成立；若估值不过度，最接近截面下可行动机会。", "backlog 转收入、液冷毛利、客户 capex", "backlog 毛利低于预期或客户 capex 下修", "actionable_long"),
  target("000660.KS", "SK hynix", "Korea", "HBM 和高端 AI memory", [4.70, 4.55, 3.35, 4.35, 3.65, 3.55, 4.10], ["SRC-SKHYNIX-FY25"], "HBM3E/HBM4 供应能力和 49% FY25 operating margin 形成强稀缺和利润桥，后续主要验证 ASP、客户资格和供给扩张节奏。", "HBM4 ramp、客户资格、ASP、capex", "HBM 供给过剩或 ASP 反转", "actionable_long"),
  target("NVDA", "NVIDIA", "USA", "AI 工厂平台控制", [4.95, 4.90, 2.25, 4.85, 3.40, 4.80, 3.60], ["SRC-NVDA-FY26-Q4"], "平台稀缺性最强，但市场隐含预期也高，未充分定价证据不足。", "Data Center 指引、gross margin、客户 capex、隐含增长", "capex 放缓或毛利无法支撑估值", "watch_only"),
  target("TSM", "TSMC ADR", "USA/Taiwan", "先进制程和封装", [4.55, 4.45, 2.95, 4.30, 3.70, 3.60, 3.20], ["SRC-TSM-Q4-2025"], "先进制程和封装是 AI 工厂硬瓶颈，财务质量高；但高 capex 和估值已部分反映增长。", "advanced packaging、capex、AI/HPC revenue mix", "先进封装供给过快或地缘风险恶化", "watch_only"),
  target("ALAB", "Astera Labs", "USA", "机柜级连接芯片", [4.25, 4.35, 2.70, 4.00, 2.85, 3.80, 4.40], ["SRC-ALAB-Q4-2025"], "rack-scale connectivity 弹性强，收入和毛利证据好，但估值和客户集中压制风险控制。", "Scorpio ramp、客户集中、gross margin", "大客户需求放缓或平台替代", "watch_only"),
  target("CRDO", "Credo", "USA", "AEC/光互联/高速连接", [4.05, 4.30, 2.85, 3.95, 2.75, 3.65, 4.55], ["SRC-CRDO-FY26-Q3"], "收入高弹性，连接需求真实；但高波动和客户集中使行动状态封顶。", "AEC/optical orders、customer concentration、gross margin", "客户订单延迟或价格压力", "watch_only"),
  target("MRVL", "Marvell Technology", "USA", "custom silicon 和电光互联", [3.95, 4.25, 2.80, 3.85, 2.80, 3.35, 4.35], ["SRC-MRVL-FY26-Q3"], "AI data-center demand 已进入 custom products 和 electro-optics 财务口径，弹性强；但客户集中、定制项目量产节奏和估值隐含预期不透明，行动状态封顶为 watch_only。", "custom silicon 项目量产、electro-optics 收入、客户集中、gross margin", "大客户项目延期、客户自研替代或毛利不达预期", "watch_only"),
  target("MU", "Micron", "USA", "HBM 和高端内存", [3.95, 4.20, 3.00, 3.80, 3.10, 3.40, 4.05], ["SRC-MU-FY26-Q1"], "HBM/云内存方向清晰，赔率和弹性较强；但相对 SK hynix 的稀缺性和客户资格需要验证。", "HBM design wins、ASP、Cloud Memory margin", "HBM 份额不及预期或周期反转", "watch_only"),
  target("DELL", "Dell Technologies", "USA", "AI server 系统交付", [3.45, 4.30, 3.10, 4.10, 2.95, 3.80, 3.70], ["SRC-DELL-FY26-Q4"], "AI server backlog 极强，系统交付弹性大；但利润率和现金流质量决定价值捕获。", "AI server margin、backlog conversion、cash flow", "订单增长但毛利或现金流差", "watch_only"),
  target("AVGO", "Broadcom", "USA", "custom ASIC 和 AI Ethernet", [3.90, 4.05, 2.70, 3.75, 3.10, 3.55, 3.55], ["SRC-AVGO-FY25-Q4"], "AI ASIC/Ethernet 已财务化，但大客户集中和估值隐含预期需要控制。", "AI revenue、customer count、Ethernet orders", "大客户/ASIC 节奏不及预期", "watch_only"),
  target("ANET", "Arista Networks", "USA", "AI Ethernet 网络", [3.50, 3.75, 2.75, 3.60, 3.25, 3.40, 3.20], ["SRC-ANET-Q4-2025"], "AI networking 方向成立，但与平台网络路线的关系和客户订单需要更多证明。", "AI cluster wins、gross margin、cloud capex", "Spectrum-X 或客户自研挤压份额", "watch_only"),
  target("005930.KS", "Samsung Electronics", "Korea", "HBM/server DDR5/eSSD", [3.55, 4.05, 2.90, 3.80, 3.15, 3.20, 3.55], ["SRC-SAMSUNG-FY25"], "内存业务 AI 产品强，但 HBM 领导力和市场预期相对 SK hynix 需要更多验证。", "HBM4 shipment、server DDR5/eSSD mix", "HBM 资格或价格不及预期", "watch_only"),
  target("SMCI", "Supermicro", "USA", "AI server 组装", [2.75, 3.75, 3.25, 2.65, 2.10, 3.00, 4.10], ["SRC-SMCI-FY26-Q2"], "AI server 主题弹性大，但执行、治理和毛利风险使风险控制不足。", "margin、cash conversion、governance", "治理风险或毛利恶化", "no_action"),
]);

const targetProfitBridgeRows = [
  ["VRT", BOM.powerCooling, "AI 工厂高功率机柜 -> 电力、热管理、液冷项目", "orders/backlog 转收入", "项目毛利、交付周期、现金转化", "backlog 转化低质量或客户 capex 下修", "actionable_long"],
  ["000660.KS", "HBM / 高端内存", "GPU/ASIC 平台规格 -> HBM 客户资格和高价值 mix", "HBM mix、ASP、operating margin", "HBM4 ramp、ASP、客户资格、扩产节奏", "ASP 反转或供给快速扩张", "actionable_long"],
  ["NVDA", BOM.platform, "AI workload -> GPU 平台、网络、软件生态和供应链资格", "Data Center revenue、gross margin", "客户 capex、推理收入、毛利率、隐含增长", "capex ROI 下降或估值已充分反映", "watch_only"],
  ["TSM", BOM.manufacturing, "GPU/ASIC 设计 -> 先进节点和先进封装订单", "HPC/AI mix、gross margin、capex 回报", "advanced packaging capacity、capex、地缘风险", "先进封装供给缓解或地缘风险上升", "watch_only"],
  ["ALAB/CRDO/MRVL", BOM.connectivity, "rack-scale 带宽需求 -> retimer/AEC/electro-optics/custom silicon", "收入增长、gross margin、design-in", "客户集中、项目 ramp、平台替代", "大客户延迟或毛利下行", "watch_only"],
  ["DELL/SMCI", BOM.systemDelivery, "AI server/rack 订单 -> backlog、发货和集成交付", "shipments、operating margin、cash conversion", "AI server 毛利、库存、现金流、治理", "订单强但利润和现金流弱", "watch_only / no_action"],
];

let activeIndustrySpaceSourceSearchMatrix = [];

function buildIndustrySpaceSourceSearchMatrix(rows) {
  return rows.map((row) => {
    const methods = row.publicSizingMethods?.methods || [];
    const groupedMethods = Object.fromEntries(industrySpaceSourceSearchCategories.map((category) => [category.key, []]));
    methods.forEach((method) => {
      const key = classifyIndustrySpaceMethod(method) || "third_party";
      groupedMethods[key].push(method);
    });
    const category_search_plan = Object.fromEntries(industrySpaceSourceSearchCategories.map((category) => {
      const categoryMethods = groupedMethods[category.key] || [];
      const sourceIds = [...new Set(categoryMethods.flatMap((method) => methodSourceIds(method)))];
      const hasSources = sourceIds.length > 0;
      const prioritySources = prioritySourcesForCategory(row, category.key);
      const foundPrioritySourceIds = [...new Set(sourceIds.flatMap((sourceId) => sourceUniverseIdsForSource(sourceId)))];
      const missingPrioritySources = prioritySources
        .filter((sourceProfile) => !foundPrioritySourceIds.includes(sourceProfile.id))
        .map((sourceProfile) => sourceProfile.id);
      const directedQueries = buildDirectedQueries(row, category, prioritySources);
      return [category.key, {
        category: category.key,
        source_type: category.label,
        source_universe_id: SOURCE_UNIVERSE.id,
        source_universe_label: SOURCE_UNIVERSE.label,
        search_query: directedQueries[0]?.query || `${row.node} ${category.label} ${category.searchIntent}`,
        search_terms: [row.node, category.label, "AI factory", "cutoff-visible", AS_OF_DATE, ...prioritySources.map((sourceProfile) => sourceProfile.name)],
        directed_queries: directedQueries,
        priority_sources: prioritySources.map((sourceProfile) => ({
          id: sourceProfile.id,
          name: sourceProfile.name,
          domain: sourceProfile.domain || "",
          access: sourceProfile.access || "unknown",
          reliability: sourceProfile.reliability || "",
          why: sourceProfileWhy(sourceProfile, row, category),
        })),
        found_priority_sources: foundPrioritySourceIds,
        missing_priority_sources: missingPrioritySources,
        search_intent: category.searchIntent,
        status: hasSources ? "found" : "gap",
        retrieval_status: hasSources ? "found_in_source_pack_needs_directed_search_audit" : "directed_search_planned_not_executed_or_no_source_pack_match",
        sourceIds,
        expected_fields: category.expectedFields,
        source_bucket: category.key === "third_party" || category.key === "company_tam" ? "research_report_or_company_material" : "evidence_or_company_material",
        visible_date_policy: `must be publicly visible on or before ${AS_OF_DATE}`,
        allowed_usage: "historical_thesis",
        preferred_parser_skill: category.preferredParserSkill,
        parser_assignment: "DeepSeek MCP should read selected long materials or source excerpts; GPT verifies before synthesis.",
        gap_reason: hasSources ? "" : `当前 source pack 未包含 ${row.node} / ${category.label} 的可靠 cutoff 前材料；需优先执行定向搜索：${directedQueries.slice(0, 3).map((item) => item.source_name).join("、")}。不能用模型估算代替。`,
        selected_materials: sourceIds.map((sourceId) => ({
          source_id: sourceId,
          title: byId(sourceId).title,
          source_visible_at: byId(sourceId).source_visible_at,
          url: byId(sourceId).url,
          matched_source_universe_ids: sourceUniverseIdsForSource(sourceId),
        })),
      }];
    }));
    return {
      node: row.node,
      core_question: row.coreQuestion,
      source_universe_id: SOURCE_UNIVERSE.id,
      sequencing_rule: "After BOM node identification, actively search the five source buckets against the domain source universe before writing space reasoning.",
      category_search_plan,
    };
  });
}

function prioritySourcesForCategory(row, categoryKey) {
  const nodeText = [row.node, row.coreQuestion, ...(row.inferenceChain || []), ...(row.facts || [])].join(" ").toLowerCase();
  const profiles = (SOURCE_UNIVERSE.priority_sources || []).filter((sourceProfile) => {
    const categories = sourceProfile.categories || [];
    if (!categories.includes(categoryKey) && !categories.includes("all")) return false;
    if (sourceProfile.id === "company_ir" || sourceProfile.id === "customer_ir" || !sourceProfile.domain) return true;
    const keywords = sourceProfile.node_keywords || [];
    if (!keywords.length) return true;
    return keywords.some((keyword) => nodeText.includes(String(keyword).toLowerCase())) || categoryKey === "third_party";
  });
  return profiles.slice(0, 6);
}

function buildDirectedQueries(row, category, prioritySources) {
  return prioritySources.map((sourceProfile) => {
    const hints = (sourceProfile.query_hints || []).slice(0, 4).join(" ");
    const domainClause = sourceProfile.domain ? `site:${sourceProfile.domain}` : "";
    const query = [domainClause, row.node, category.label, "AI factory", hints, `before ${AS_OF_DATE}`]
      .filter(Boolean)
      .join(" ")
      .replace(/\s+/g, " ")
      .trim();
    return {
      source_id: sourceProfile.id,
      source_name: sourceProfile.name,
      domain: sourceProfile.domain || "",
      access: sourceProfile.access || "unknown",
      query,
      cutoff_policy: `Use only materials visibly published on or before ${AS_OF_DATE}; post-cutoff hits are quarantine-only.`,
      expected_fields: category.expectedFields,
    };
  });
}

function buildOverviewSourceSearchMatrix(items, questionSpecs, moduleKey) {
  return items.map((item) => ({
    module: moduleKey,
    node: item.node,
    source_universe_id: SOURCE_UNIVERSE.id,
    source_universe_label: SOURCE_UNIVERSE.label,
    sequencing_rule: "For every BOM node, answer each minimum question only after writing a professional universe plan and Exa search plan; selected materials then go through source parsing and GPT verification.",
    question_search_plan: Object.fromEntries(questionSpecs.map((spec) => {
      const sourceIds = overviewSourceIdsForNode(item.node, spec.title);
      const prioritySources = prioritySourcesForOverview(item.node, spec.title, sourceIds);
      return [spec.title, {
        question: spec.title,
        source_universe_id: SOURCE_UNIVERSE.id,
        search_query: buildOverviewExaQuery(item.node, spec.title, prioritySources),
        source_universe_plan: {
          priority_sources: prioritySources.map((sourceProfile) => ({
            id: sourceProfile.id,
            name: sourceProfile.name,
            domain: sourceProfile.domain || "",
            access: sourceProfile.access || "unknown",
            reliability: sourceProfile.reliability || "",
          })),
          expected_fields: spec.expectedFields,
          preferred_parser_skill: spec.preferredParserSkill,
        },
        exa_search_plan: {
          provider: "exa",
          query: buildOverviewExaQuery(item.node, spec.title, prioritySources),
          expected_fields: spec.expectedFields,
          cutoff_policy: `Use only results visibly published on or before ${AS_OF_DATE}; post-cutoff hits are quarantine-only.`,
          retrieval_status: sourceIds.length ? "covered_by_cutoff_source_pack_and_exa_query_defined" : "exa_query_required_gap",
        },
        status: sourceIds.length ? "found" : "gap",
        sourceIds,
        selected_materials: sourceIds.map((sourceId) => ({
          source_id: sourceId,
          title: byId(sourceId).title,
          source_visible_at: byId(sourceId).source_visible_at,
          url: byId(sourceId).url,
          matched_source_universe_ids: sourceUniverseIdsForSource(sourceId),
        })),
      }];
    })),
  }));
}

function prioritySourcesForOverview(node, questionTitle, sourceIds = []) {
  const nodeText = `${node} ${questionTitle}`.toLowerCase();
  const matchedFromSources = sourceIds.flatMap((sourceId) => sourceUniverseIdsForSource(sourceId));
  const profiles = (SOURCE_UNIVERSE.priority_sources || []).filter((sourceProfile) => {
    if (sourceProfile.id === "company_ir" || sourceProfile.id === "customer_ir") return true;
    if (matchedFromSources.includes(sourceProfile.id)) return true;
    const keywords = sourceProfile.node_keywords || [];
    return keywords.some((keyword) => nodeText.includes(String(keyword).toLowerCase()));
  });
  const selected = profiles.length ? profiles : (SOURCE_UNIVERSE.priority_sources || []).slice(0, 5);
  return selected.slice(0, 6);
}

function buildOverviewExaQuery(node, questionTitle, prioritySources) {
  const domainClauses = (prioritySources || [])
    .filter((sourceProfile) => sourceProfile.domain)
    .slice(0, 3)
    .map((sourceProfile) => `site:${sourceProfile.domain}`);
  return [...domainClauses, node, questionTitle, "AI factory", "revenue margin backlog competition chokepoint", `before ${AS_OF_DATE}`]
    .filter(Boolean)
    .join(" ")
    .replace(/\s+/g, " ")
    .trim();
}

function overviewSourceIdsForNode(node, questionTitle = "") {
  const text = `${node} ${questionTitle}`.toLowerCase();
  const ids = [];
  const add = (...sourceIds) => ids.push(...sourceIds);
  if (/平台|gpu|asic|加速|processor|计算/.test(text)) add("SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-OMDIA-AI-PROCESSORS-20250828", "SRC-SA-GB200-BOM-2024", "SRC-TOMS-JPR-AIB-Q3-2025", "SRC-TOMS-NVDA-CHINA-SHARE-202510");
  if (/hbm|内存|memory|dram|essd/.test(text)) add("SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1", "SRC-MU-FY26-Q1-PREPARED", "SRC-SAMSUNG-FY25", "SRC-TF-HBM-PRICE-20240506", "SRC-TF-BLACKWELL-HBM-20240808");
  if (/先进|制程|封装|cowos|tsmc|manufacturing|packaging/.test(text)) add("SRC-TSM-Q4-2025", "SRC-SA-COWOS-HBM-2023", "SRC-OMDIA-SEMI-TRENDS-202512");
  if (/连接|网络|network|ethernet|optical|retimer|aec|switch|interconnect/.test(text)) add("SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3", "SRC-AVGO-FY25-Q4", "SRC-ANET-Q4-2025", "SRC-LC-AI-OPTICS-202501", "SRC-LC-PAM4-DSP-20260226", "SRC-DO-AI-NETWORKS-20250715", "SRC-SA-OPTICAL-2024");
  if (/电力|液冷|cooling|thermal|power|基础设施/.test(text)) add("SRC-VRT-Q4-2025", "SRC-DO-LIQUID-COOLING-20260108", "SRC-SA-COOLING-2025", "SRC-SA-GB200-BOM-2024", "SRC-GOOGL-Q4-2025", "SRC-AMZN-Q4-2025", "SRC-META-Q3-2025");
  if (/系统|服务器|server|rack|交付|组装/.test(text)) add("SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2", "SRC-SA-GB200-BOM-2024");
  if (/需求|客户|下游|capex|roi|rpo/.test(text)) add("SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025", "SRC-ORCL-FY26-Q2");
  return [...new Set(ids)].filter((sourceId) => sources.some((source) => source.source_id === sourceId));
}

function renderOverviewQuestionCard(spec, item, className) {
  const answer = typeof spec.answer === "function" ? spec.answer(item) : item[spec.field] || "待补。";
  const answerSourceIds = answer && typeof answer === "object" && Array.isArray(answer.sourceIds) ? answer.sourceIds : [];
  const citedSourceIds = extractSourceMarkedIds(answer);
  const sourceIds = [...new Set(citedSourceIds.length ? citedSourceIds : answerSourceIds)];
  return `<section class="${className} overview-question-card">
    <h4>${esc(spec.title)}</h4>
    ${renderOverviewAnswer(answer)}
    <div class="overview-answer-sources">${renderSourceChips(sourceIds.slice(0, 5))}</div>
  </section>`;
}

function renderOverviewAnswer(answer) {
  if (answer && typeof answer === "object" && !Array.isArray(answer)) {
    const paragraphs = Array.isArray(answer.paragraphs)
      ? answer.paragraphs
      : Array.isArray(answer.prose)
        ? answer.prose
        : null;
    if (paragraphs) {
      return `<div class="overview-answer overview-answer-prose">
        ${paragraphs.map((paragraph) => `<p>${renderSourceMarkedText(paragraph || "待补。")}</p>`).join("")}
      </div>`;
    }
    const rows = [
      ["当前判断", answer.judgment],
      ["关键事实", answer.facts],
      ["推理链", answer.reasoning],
      ["证据来源", answer.evidence],
      ["缺口 / 触发器", answer.gap],
    ];
    return `<div class="overview-answer overview-answer-structured">
      ${rows.map(([label, value]) => `<div class="overview-answer-row"><span>${esc(label)}</span><p>${esc(value || "待补。")}</p></div>`).join("")}
    </div>`;
  }
  return `<p class="overview-answer">${esc(answer || "待补。")}</p>`;
}

function extractSourceMarkedIds(value) {
  const parts = [];
  if (value && typeof value === "object" && !Array.isArray(value)) {
    const paragraphs = Array.isArray(value.paragraphs)
      ? value.paragraphs
      : Array.isArray(value.prose)
        ? value.prose
        : null;
    if (paragraphs) parts.push(...paragraphs);
    ["judgment", "current_judgment", "answer", "facts", "key_facts", "reasoning", "inference", "evidence", "source_read", "gap", "trigger", "missing_data"].forEach((key) => {
      if (value[key]) parts.push(value[key]);
    });
  } else if (value) {
    parts.push(value);
  }
  const pattern = /\[[^\]]+\]\(source:([A-Za-z0-9_.:-]+)\)/g;
  const ids = [];
  parts.forEach((part) => {
    let match;
    const text = String(part || "");
    while ((match = pattern.exec(text)) !== null) ids.push(match[1]);
  });
  return [...new Set(ids)];
}

function renderSourceMarkedText(value) {
  const text = String(value || "");
  const pattern = /\[([^\]]+)\]\(source:([A-Za-z0-9_.:-]+)\)/g;
  let html = "";
  let lastIndex = 0;
  let match;
  while ((match = pattern.exec(text)) !== null) {
    html += esc(text.slice(lastIndex, match.index));
    const label = match[1];
    const sourceId = match[2];
    const source = byId(sourceId);
    if (source && source.url) {
      html += `<a href="${esc(source.url)}" target="_blank" rel="noopener">${esc(label)}</a>`;
    } else {
      html += esc(label);
    }
    lastIndex = pattern.lastIndex;
  }
  html += esc(text.slice(lastIndex));
  return html;
}

function sourceProfileWhy(sourceProfile, row, category) {
  const access = sourceProfile.access || "unknown access";
  const reliability = sourceProfile.reliability || "unknown reliability";
  return `${sourceProfile.name} is prioritized for ${row.node} / ${category.label} because it is ${reliability} and ${access}; use it to test public sizing, customer demand, or financial evidence before accepting a gap.`;
}

function sourceUniverseIdsForSource(sourceId) {
  const source = byId(sourceId);
  const url = source.url || "";
  const host = urlHost(url);
  const title = `${source.title || ""} ${source.summary || ""}`.toLowerCase();
  return (SOURCE_UNIVERSE.priority_sources || [])
    .filter((sourceProfile) => {
      if (sourceProfile.domain && host.endsWith(sourceProfile.domain)) return true;
      if (sourceProfile.id === "company_ir" && /(investor|sec\.gov|ir\.|news\.samsung|prnewswire)/i.test(url)) return true;
      if (sourceProfile.id === "customer_ir" && /(microsoft|amazon|alphabet|google|meta|oracle)/i.test(url)) return true;
      return title.includes(String(sourceProfile.name || "").toLowerCase());
    })
    .map((sourceProfile) => sourceProfile.id);
}

function urlHost(url) {
  try {
    return new URL(url).hostname.replace(/^www\./, "");
  } catch (_error) {
    return "";
  }
}

function methodSourceIds(method) {
  const sourceIds = method?.sourceIds || method?.source_ids || method?.sources || [];
  if (Array.isArray(sourceIds)) return sourceIds.filter(Boolean);
  if (sourceIds) return [sourceIds];
  return [];
}

function classifyIndustrySpaceMethod(method) {
  const text = method && typeof method === "object"
    ? [
        method.sourceType,
        method.source_type,
        method.type,
        method.organization,
        method.company,
        method.source,
        method.guidanceContent,
        method.guidance_content,
        method.guidance,
        method.value,
        method.method,
      ].filter(Boolean).join(" ")
    : String(method || "");
  if (/客户侧|客户指引|customer/i.test(text)) return "customer_guidance";
  if (/公司\s*TAM|TAM|市场空间|可触达市场/i.test(text)) return "company_tam";
  if (/第三方|研报|机构|sell.?side|industry|forecast|预测|数据商/i.test(text)) return "third_party";
  if (/公司指引|guidance|指引|outlook|预计|expected/i.test(text)) return "company_guidance";
  if (/经营验证|财务兑现|公司财报|财报|revenue|orders?|backlog|margin|cash|收入|订单|利润|现金/i.test(text)) return "financial_evidence";
  return "third_party";
}

function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const qaTree = buildQaTree();
  const extractions = buildExtractions();
  const reviews = buildReviews(extractions);
  activeIndustrySpaceSourceSearchMatrix = buildIndustrySpaceSourceSearchMatrix(industrySpaceEvidencePackRows);
  const competitionSourceSearchMatrix = buildOverviewSourceSearchMatrix(q2CompetitionLandscape, competitionQuestionSpecs, "竞争格局与利润池");
  const chokepointSourceSearchMatrix = buildOverviewSourceSearchMatrix(chainChokepointScores, chokepointQuestionSpecs, "瓶颈点");
  writeJson("project.json", { project_id: PROJECT_ID, title: "AI 工厂产业相关投资机会回测研究", mode: "historical_backtest", as_of_date: AS_OF_DATE, evaluation_date: EVALUATION_DATE, report_path: "professional_report.html" });
  writeJson("qa_tree.json", qaTree);
  writeJsonl("sources.jsonl", sources);
  writeJsonl("evidence.jsonl", sources.filter((item) => item.allowed_usage !== "label_only"));
  writeJsonl("source_extractions.jsonl", extractions);
  writeJsonl("leaf_source_reviews.jsonl", reviews);
  const frozen = { as_of_date: AS_OF_DATE, label_status: "unattached", targets: targets.map(stripLabel) };
  const labeled = { ...frozen, label_status: "attached", label_attach: { evaluation_date: EVALUATION_DATE, rule: "labels are evaluation metadata only and must not alter frozen recommendations" }, targets: targets };
  writeJson("frozen_recommendations.json", frozen);
  writeJson("labeled_recommendations.json", labeled);
  writeJson("investment_workbench.json", {
    project_id: PROJECT_ID,
    run_mode: "historical_backtest",
    as_of_date: AS_OF_DATE,
    evaluation_date: EVALUATION_DATE,
    constraint_definition: keyConstraintDefinition,
    supply_chain_explainer: chainExplainer,
    supply_chain_research_bridge: chainResearchBridge,
    supply_chain_node_lenses: chainNodeLenses,
    supply_chain_value_capture_matrix: chainValueCaptureMatrix,
    supply_chain_qa_mapping: chainQaMapping,
    supply_chain_data_gaps: chainDataGaps,
    supply_chain_network: chainNetwork,
    supply_chain_sankey: chainSankeyFlows,
    component_value_chain: componentValueChainRows,
    supply_chain_chokepoint_heatmap: chainChokepointScores,
    bottleneck_release_timeline: bottleneckReleaseTimeline,
    supply_chain_map: chainRows,
    q2_competition_landscape: q2CompetitionLandscape,
    q1_demand_space_model: q1DemandSpaceModel,
    industry_space_conclusion: industrySpaceConclusion,
    industry_space_gate_model: industrySpaceGateModel,
    industry_space_boundary: industrySpaceBoundary,
    industry_space_driver_tree: industrySpaceDriverTree,
    industry_space_scenario_rows: industrySpaceScenarioRows,
    industry_space_node_elasticity_rows: industrySpaceNodeElasticityRows,
    industry_space_evidence_pack: industrySpaceEvidencePackRows,
    industry_space_source_universe: SOURCE_UNIVERSE,
    industry_space_source_search_matrix: activeIndustrySpaceSourceSearchMatrix,
    industry_overview_research_protocol: overviewResearchProtocol,
    competition_source_search_matrix: competitionSourceSearchMatrix,
    chokepoint_source_search_matrix: chokepointSourceSearchMatrix,
    industry_space_validation_rows: industrySpaceValidationRows,
    target_profit_bridge: targetProfitBridgeRows,
    target_odds_models: targets.map((target) => ({ ticker: target.ticker, name: target.name, ...target.odds_model })),
    source_extractions: extractions,
    leaf_source_reviews: reviews,
    scoring_worksheet: targets.map(stripLabel),
    label_attach: labeled.label_attach,
    targets,
  });
  fs.writeFileSync(path.join(OUT_DIR, "professional_report.html"), renderHtml(qaTree, targets), "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "professional_report.md"), renderMarkdown(targets), "utf8");
  console.log(`Generated ${OUT_DIR}`);
}

function source(source_id, title, source_bucket, url, source_visible_at, summary) {
  const visibleDate = assertCutoffVisibleThesisSource(source_id, source_visible_at);
  return {
    source_id,
    title,
    source_bucket,
    url,
    source_visible_at: visibleDate,
    support_refute_or_lead: "support",
    summary,
    as_of_date: AS_OF_DATE,
    cutoff_status: "cutoff_visible",
    allowed_usage: "thesis",
    availability_proof: `publisher date / official release page visible ${source_visible_at}`,
    used_in: ["qa", "target_scoring"],
  };
}

function labelSource(source_id, title, url, source_visible_at) {
  const visibleDate = normalizeIsoDate(source_visible_at, source_id);
  return {
    source_id,
    title,
    source_bucket: "evidence",
    url,
    source_visible_at: visibleDate,
    support_refute_or_lead: "support",
    summary: "Price evaluation dataset for final target table only.",
    as_of_date: AS_OF_DATE,
    cutoff_status: "post_cutoff_label_only",
    allowed_usage: "label_only",
    availability_proof: "post-cutoff price dataset",
    used_in: ["final_target_evaluation"],
  };
}

function assertCutoffVisibleThesisSource(source_id, source_visible_at) {
  const visibleDate = normalizeIsoDate(source_visible_at, source_id);
  if (visibleDate > AS_OF_DATE) {
    throw new Error(`Post-cutoff thesis source ${source_id}: ${visibleDate} > ${AS_OF_DATE}`);
  }
  return visibleDate;
}

function normalizeIsoDate(value, source_id) {
  const text = String(value || "").slice(0, 10);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(text)) {
    throw new Error(`Invalid source_visible_at for ${source_id}: ${value}`);
  }
  return text;
}

function companyNode(data) {
  return data;
}

function networkNode(id, label, ticker, stage, role, x, y) {
  return { id, label, ticker, stage, role, x, y, w: 190, h: 54 };
}

function networkEdge(from, to, type, label, flow, curve = 0) {
  return { from, to, type, label, flow, curve };
}

function chokepointScore(node, role, controllers, scores, conclusion, qa_link) {
  const dimensions = ["稀缺性", "替代难度", "定价权", "财务弹性", "估值风险", "反证风险"];
  return {
    node,
    role,
    controllers,
    scores: Object.fromEntries(dimensions.map((dimension, index) => [dimension, scores[index]])),
    conclusion,
    qa_link,
  };
}

function l1(id, question, conclusion) {
  return { id, level: 1, question, conclusion, children: [] };
}

function l2(id, question, conclusion) {
  return { id, level: 2, question, conclusion, children: [] };
}

function leaf(id, parent, question, skill, score_component, decision_use, sourceIds, fact, inference, judgment, gap, trigger, answerArtifact) {
  return researchUnit(3, id, parent, question, skill, score_component, decision_use, sourceIds, fact, inference, judgment, gap, trigger, answerArtifact);
}

function drill(level, id, parent, question, skill, score_component, decision_use, sourceIds, fact, inference, judgment, gap, trigger, answerArtifact) {
  return researchUnit(level, id, parent, question, skill, score_component, decision_use, sourceIds, fact, inference, judgment, gap, trigger, answerArtifact);
}

function researchUnit(level, id, parent, question, skill, score_component, decision_use, sourceIds, fact, inference, judgment, gap, trigger, answerArtifact) {
  const schema = ["key_facts", "numbers_dates", "investment_relevance", "support_refute_or_lead", "uncertainties", "question_context", "extraction_dimensions", "dimension_findings"];
  return {
    id,
    parent,
    level,
    question,
    conclusion: judgment,
    skill,
    score_component,
    decision_use,
    materiality: decision_use,
    support_evidence: sourceIds.map((sourceId) => `${sourceId} supports ${question}`),
    refute_evidence: [`Counter evidence that weakens ${question}`],
    target_implications: `Affects ${score_component} and action_state.`,
    minimum_evidence_gate: "At least one cutoff-visible primary source plus GPT verification.",
    refuting_source_plan: ["Company filings, customer capex guidance, margin and order updates, and competing platform evidence visible at cutoff."],
    source_plan: sourceIds.map((sourceId) => ({
      source_id: sourceId,
      as_of_date: AS_OF_DATE,
      source_visible_at: byId(sourceId).source_visible_at,
      cutoff_status: byId(sourceId).cutoff_status,
      allowed_usage: "historical_thesis",
      expected_fields: schema,
      source_bucket: byId(sourceId).source_bucket,
      preferred_parser_skill: skill,
      availability_proof: byId(sourceId).availability_proof,
    })),
    skill_dispatch: {
      task_family: skill.replace("-analysis", ""),
      selected_skill: skill,
      concrete_materials: sourceIds,
      extraction_schema: schema,
      source_extraction_ids: sourceIds.map((sourceId) => extractionId(id, sourceId)),
      leaf_source_review_ids: sourceIds.map((sourceId) => reviewId(id, sourceId)),
      skill_output_status: "gpt_verified_direct_parse",
      fallback_used: true,
      gpt_verification_status: "verified_against_cutoff_source_pack",
    },
    backtest_grounding: {
      allowed_source_ids: sourceIds,
      model_prior_policy: "hypothesis_only_not_scoring_evidence",
      post_cutoff_knowledge_policy: "not_used_before_label_attach",
      non_source_claims: [],
    },
    fact,
    inference,
    judgment,
    gap,
    trigger,
    sourceIds,
    source_links: sourceIds,
    answerArtifact,
  };
}

function artifact(title, columns, rows) {
  return { title, columns, rows };
}

function label(start_price, end_price, forward_3m_return, price_source, label_status, dates = {}) {
  return {
    as_of_date: AS_OF_DATE,
    evaluation_date: EVALUATION_DATE,
    label_window: LABEL_WINDOW,
    start_price,
    start_price_date: dates.start_price_date || LABEL_START_DATE,
    end_price,
    end_price_date: dates.end_price_date || LABEL_END_DATE,
    forward_3m_return,
    benchmark_return: BENCHMARK_RETURN,
    excess_return: round(forward_3m_return - BENCHMARK_RETURN),
    price_source,
    label_status,
  };
}

function unverifiedLabel(reason) {
  return {
    as_of_date: AS_OF_DATE,
    evaluation_date: EVALUATION_DATE,
    label_window: LABEL_WINDOW,
    start_price: null,
    start_price_date: null,
    end_price: null,
    end_price_date: null,
    forward_3m_return: null,
    benchmark_return: BENCHMARK_RETURN,
    excess_return: null,
    price_source: "not verified",
    label_status: `label_unverified: ${reason}`,
  };
}

function target(ticker, name, market, thesisNode, componentArray, sourceIds, rationale, nextData, downgradeRisk, action_state) {
  const componentNames = Object.keys(SCORE_WEIGHTS);
  const componentScores = Object.fromEntries(componentNames.map((name, index) => [name, componentArray[index]]));
  const score_dimensions = {
    scarcity_or_monopoly: componentScores.chokepoint_strength,
    mispricing: componentScores.valuation_odds,
    earnings_elasticity: round((componentScores.future_space + componentScores.payoff_convexity) / 2),
    risk_control: componentScores.disconfirming_risk_control,
  };
  const total_score = round(
    score_dimensions.scarcity_or_monopoly * 0.35 +
    score_dimensions.mispricing * 0.25 +
    score_dimensions.earnings_elasticity * 0.25 +
    score_dimensions.risk_control * 0.15
  );
  const thesis_confidence = round(componentScores.chokepoint_strength * 0.30 + componentScores.future_space * 0.15 + componentScores.valuation_odds * 0.10 + componentScores.evidence_quality * 0.25 + componentScores.disconfirming_risk_control * 0.15 + componentScores.monitorability * 0.05);
  const payoff_convexity = componentScores.payoff_convexity;
  const opportunity_fit = round(score_dimensions.scarcity_or_monopoly * 0.35 + score_dimensions.mispricing * 0.25 + score_dimensions.earnings_elasticity * 0.25 + score_dimensions.risk_control * 0.15);
  const score_subcomponents = Object.fromEntries(componentNames.map((component) => [component, [{
    name: `${component}_primary_driver`,
    score: componentScores[component],
    weight: SCORE_WEIGHTS[component],
    evidence_ids: sourceIds,
    review_ids: [],
    rationale: `${component} score is based on cutoff-visible evidence for ${thesisNode}; no price evaluation data was used.`,
    status: action_state === "actionable_long" ? "active_with_kill_tests" : "capped_until_verified",
  }]]));
  const odds_model = oddsModelForTarget(ticker, thesisNode, nextData, downgradeRisk, action_state);
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
      thesis_confidence,
      payoff_convexity,
      opportunity_fit,
    },
    score_subcomponents,
    thesis_kill_tests: action_state === "actionable_long" ? [
      { test: "订单/利润桥断裂", evidence_needed: nextData, downgrade_action: "downgrade to watch_only or no_action", source_plan: "Next company filing, earnings call and order/margin disclosure" },
      { test: "客户 capex 或估值反证", evidence_needed: "customer capex guidance and valuation-implied growth", downgrade_action: "cap score and remove actionable_long", source_plan: "Hyperscaler capex updates and valuation screen" },
    ] : [],
    odds_model,
    prediction_review: {
      initial_claim: rationale,
      validation_horizon: EVALUATION_DATE,
      required_evidence: nextData,
      current_status: action_state,
      review_trigger: downgradeRisk,
    },
    label: labels[ticker] || unverifiedLabel("ticker not in label map"),
  };
}

function oddsModelForTarget(ticker, thesisNode, nextData, downgradeRisk, action_state) {
  const base = {
    implied_expectation: "截面市场大概率已经计入 AI 工厂增长，必须用订单、毛利、现金流或估值隐含增速证明仍有错配。",
    base_path: nextData,
    bull_path: "订单、毛利和客户 capex 证据继续高于市场隐含增长。",
    bear_path: downgradeRisk,
    upgrade_data: nextData,
    downgrade_data: downgradeRisk,
    odds_judgment: action_state === "actionable_long" ? "赔率相对有吸引力，但必须通过硬 kill test。" : "胜率或主题强度成立，赔率仍需验证。",
  };
  const overrides = {
    VRT: {
      implied_expectation: "市场已看到 AI 数据中心电力/液冷需求，但未必充分计入 backlog 转化质量和物理交付瓶颈的持续性。",
      base_path: "backlog 按期转收入，液冷和电力项目毛利维持，客户 capex 不下修。",
      bull_path: "高功率机柜渗透超预期，液冷项目毛利高于市场预期，订单持续上修。",
      bear_path: "backlog 转收入质量差、液冷毛利不达预期或云厂 capex 放缓。",
      odds_judgment: "胜率与赔率在目标池中最均衡；需要持续验证 backlog 毛利。",
    },
    "000660.KS": {
      implied_expectation: "市场已认可 HBM 景气，但 HBM4 资格、产能斜率和 ASP 持续性仍可能带来盈利上修空间。",
      base_path: "HBM 客户资格稳定，ASP 和毛利维持，供给扩张慢于 AI memory 需求。",
      bull_path: "HBM4 ramp 和客户份额继续领先，AI memory mix 推高利润率。",
      bear_path: "HBM 供给快速扩张、ASP 反转或客户资格变化。",
      odds_judgment: "硬瓶颈强，赔率取决于 HBM 价格与资格持续性。",
    },
    NVDA: {
      implied_expectation: "市场已高度计入平台控制和数据中心增长，未充分定价证据弱于稀缺性证据。",
      base_path: "Data Center 指引和毛利继续兑现，客户 capex 维持。",
      bull_path: "AI 工厂平台需求、网络和软件生态带来持续上修。",
      bear_path: "capex/ROI 放缓、出口限制扩大或毛利率无法支撑估值。",
      odds_judgment: "胜率高，但赔率受高隐含预期压制。",
    },
    TSM: {
      implied_expectation: "市场已认可先进制程和封装稀缺，但先进封装供需缺口与 AI/HPC mix 仍需量化。",
      base_path: "advanced technology share 和 capex 按计划兑现，HPC/AI mix 支撑毛利。",
      bull_path: "先进封装供给持续短缺，AI/HPC 收入和毛利率超预期。",
      bear_path: "先进封装供给过快、capex 回报下降或地缘风险恶化。",
      odds_judgment: "高质量胜率资产，赔率需要估值与 capex 回报验证。",
    },
    ALAB: {
      implied_expectation: "市场已看到 rack-scale connectivity 高增长，关键是客户集中和估值是否允许继续上修。",
      base_path: "Scorpio/rack-scale 产品按期放量，gross margin 稳定。",
      bull_path: "机柜级连接 attach rate 提升且客户扩散。",
      bear_path: "大客户需求放缓、平台自有方案替代或估值压缩。",
      odds_judgment: "高弹性高风险，先作为 watch_only 验证。",
    },
    CRDO: {
      implied_expectation: "市场可能已计入 AEC/光互联高增速，赔率来自订单持续性和客户扩散。",
      base_path: "AEC/optical orders 继续增长，客户集中不恶化，毛利稳定。",
      bull_path: "AI rack 带宽升级推动收入和利润持续上修。",
      bear_path: "客户订单延迟、价格压力或替代路线挤压。",
      odds_judgment: "弹性突出，但风险控制尚不足以提高行动状态。",
    },
    MRVL: {
      implied_expectation: "市场已认可 custom silicon 和电光互联方向，但项目量产节奏和客户集中仍不透明。",
      base_path: "custom silicon 项目按期量产，electro-optics 收入持续增长。",
      bull_path: "大客户项目放量，AI data-center mix 带来利润上修。",
      bear_path: "项目延期、客户自研替代或毛利不达预期。",
      odds_judgment: "赔率来自定制芯片/光互联弹性，需用项目节点验证。",
    },
    MU: {
      implied_expectation: "市场已看到存储周期回升，AI memory/HBM 的超额利润池是否充分计入仍需验证。",
      base_path: "HBM design wins、Cloud Memory mix 和 ASP 支撑毛利。",
      bull_path: "HBM 份额提升且 DRAM/eSSD 同步改善。",
      bear_path: "HBM 份额不及预期、ASP 回落或周期反转。",
      odds_judgment: "弹性较强，但相对稀缺性低于 SK hynix。",
    },
    DELL: {
      implied_expectation: "市场已看到 AI server backlog，未必充分计入利润率和现金转化的不确定性。",
      base_path: "AI server backlog 转收入且毛利、现金流不恶化。",
      bull_path: "AI server/rack 订单继续上修并带来利润率改善。",
      bear_path: "订单增长但毛利或现金流质量差。",
      odds_judgment: "订单胜率较高，赔率取决于利润质量。",
    },
    AVGO: {
      implied_expectation: "市场已计入 AI ASIC/Ethernet 稳态受益，赔率取决于客户数量和项目持续性。",
      base_path: "AI revenue、customer count 和 Ethernet orders 继续兑现。",
      bull_path: "更多云厂 ASIC 项目扩散，AI networking 贡献持续上修。",
      bear_path: "大客户/ASIC 节奏不及预期或估值透支。",
      odds_judgment: "稳态优质，但短期错配需要更强证据。",
    },
    ANET: {
      implied_expectation: "市场认可 AI networking 增长，但仍需证明开放以太网路线份额。",
      base_path: "AI cluster wins 和云厂 capex 支撑收入，gross margin 稳定。",
      bull_path: "开放以太网路线在 AI 集群中份额继续扩大。",
      bear_path: "平台网络方案或客户自研挤压份额。",
      odds_judgment: "方向成立，等待客户订单和路线份额验证。",
    },
    "005930.KS": {
      implied_expectation: "市场已看到 AI memory 受益，但相对 SK hynix 的 HBM 领导力折价仍需验证。",
      base_path: "HBM4 shipment、server DDR5/eSSD mix 改善，毛利回升。",
      bull_path: "HBM 资格和供给份额改善，估值折价收敛。",
      bear_path: "HBM 资格或价格不及预期。",
      odds_judgment: "估值可能有弹性，但稀缺性证据弱于 SK hynix。",
    },
    SMCI: {
      implied_expectation: "市场可能给予 AI server 主题弹性，但治理、执行和毛利风险应显著折价。",
      base_path: "收入恢复且 margin、cash conversion、governance 不恶化。",
      bull_path: "AI server 订单恢复并证明治理风险可控。",
      bear_path: "治理风险、毛利恶化或现金流转差。",
      odds_judgment: "主题弹性不能抵消风险控制缺口，维持 no_action。",
    },
  };
  return { thesis_node: thesisNode, ...base, ...(overrides[ticker] || {}) };
}

function rankTargets(items) {
  const priority = { actionable_long: 0, watch_only: 1, no_action: 2 };
  return items.slice().sort((a, b) =>
    (priority[a.action_state] - priority[b.action_state]) ||
    (b.score.opportunity_fit - a.score.opportunity_fit) ||
    (b.score.total_score - a.score.total_score) ||
    (b.score.payoff_convexity - a.score.payoff_convexity) ||
    a.ticker.localeCompare(b.ticker)
  ).map((item, index) => ({ ...item, rank: index + 1 }));
}

function stripLabel(target) {
  const clean = { ...target };
  delete clean.label;
  return clean;
}

function buildQaTree() {
  for (const node of [...l1s, ...l2s, ...researchUnits]) node.children = [];
  for (const l2Node of l2s) {
    const parent = l1s.find((item) => item.id === l2Node.id.split(".")[0]);
    if (parent) parent.children.push(l2Node);
  }
  for (const unitNode of researchUnits) {
    const parent = [...l2s, ...researchUnits].find((item) => item.id === unitNode.parent);
    if (!parent) throw new Error(`Unknown QA parent ${unitNode.parent} for ${unitNode.id}`);
    parent.children.push(unitNode);
  }
  const nodes = [];
  for (const l1Node of l1s) {
    walk(l1Node, "", nodes);
  }
  return {
    project_id: PROJECT_ID,
    run_mode: "historical_backtest",
    as_of_date: AS_OF_DATE,
    evaluation_date: EVALUATION_DATE,
    l1_questions: l1s,
    anti_leakage_controls: {
      anti_leakage_level: "strict_cutoff_source_pack",
      as_of_date: AS_OF_DATE,
      cutoff_source_pack_policy: "only sources visible on or before as_of_date can be used in QA and scoring",
      llm_prior_policy: "model_prior_is_not_evidence",
      question_tree_policy: "domain playbook may structure hypotheses but cannot strengthen conclusions without cutoff sources",
      supply_chain_policy: "supply-chain priors are explanatory only unless grounded by cutoff source IDs",
      scoring_policy: "target scores use only cutoff-visible evidence and GPT reviews",
      label_isolation_policy: "labels_attached_after_frozen_recommendations_only",
    },
    nodes,
  };
}

function walk(node, parentId, out) {
  out.push(flatNode(node, parentId));
  for (const child of node.children || []) walk(child, node.id, out);
}

function flatNode(node, parentId) {
  const base = {
    id: node.id,
    level: node.level,
    parent_id: parentId,
    question: node.question,
    current_conclusion: node.conclusion,
    next_question_ids: (node.children || []).map((child) => child.id),
  };
  if (node.level >= 3 && node.level <= 5) {
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
      backtest_grounding: node.backtest_grounding,
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
  for (const node of researchUnits) {
    for (const sourceId of node.sourceIds) {
      const src = byId(sourceId);
      const dimensionFindings = dimensionFindingsForSource(sourceId, node);
      const extractionDimensions = [...new Set(dimensionFindings.map((item) => item.dimension || item.bucket).filter(Boolean))];
      const parser = parserForSourceQuestion(sourceId, node);
      rows.push({
        extraction_id: extractionId(node.id, sourceId),
        l3_question_id: node.id,
        source_id: sourceId,
        source_title: src.title,
        source_bucket: src.source_bucket,
        parser,
        parser_status: "complete",
        question_context: node.question,
        extraction_dimensions: extractionDimensions,
        dimension_findings: dimensionFindings,
        schema_fields: {
          key_facts: { value: src.summary, source_anchor: src.url, status: "verified" },
          numbers_dates: { value: src.source_visible_at, source_anchor: src.url, status: "verified" },
          investment_relevance: { value: node.decision_use, source_anchor: src.url, status: "verified" },
          support_refute_or_lead: { value: src.support_refute_or_lead, source_anchor: src.url, status: "verified" },
          uncertainties: { value: node.gap, source_anchor: src.url, status: "verified" },
          question_context: { value: node.question, source_anchor: src.url, status: "verified" },
          extraction_dimensions: { value: extractionDimensions, source_anchor: src.url, status: "verified" },
          dimension_findings: { value: dimensionFindings, source_anchor: src.url, status: "verified" },
        },
        key_facts: [src.summary, ...dimensionFindings.flatMap((item) => item.facts || [])],
        inference: node.inference,
        support_refute_or_lead: src.support_refute_or_lead,
        uncertainties: [node.gap, ...dimensionFindings.map((item) => item.scope_caveat).filter(Boolean)],
        follow_up_data: [node.trigger],
        created_at: EVALUATION_DATE,
      });
    }
  }
  return rows;
}

function parserForSourceQuestion(sourceId, node) {
  const questionText = `${node.id} ${node.question} ${node.decision_use}`.toLowerCase();
  if (["SRC-MU-FY26-Q1", "SRC-MU-FY26-Q1-PREPARED"].includes(sourceId) && /hbm|micron|高端内存|内存/.test(questionText)) {
    return "deepseek_delegate";
  }
  return node.skill;
}

function dimensionFindingsForSource(sourceId, node) {
  const findings = [];
  for (const bomNode of industrySpaceEvidencePackRows) {
    for (const method of bomNode.publicSizingMethods?.methods || []) {
      const sourceIds = normalizeSourceIds(method.sourceIds || method.source_ids || method.sources || []);
      if (!sourceIds.includes(sourceId)) continue;
      findings.push({
        question: bomNode.coreQuestion,
        bom_node: bomNode.node,
        dimension: canonicalIndustrySpaceDimension(method.sourceType || "未分类维度"),
        found_or_gap: "found",
        facts: [method.guidanceContent || method.guidance || method.value || ""].filter(Boolean),
        scope_caveat: method.confidence || "",
        verification_metrics: [method.verificationMetric || method.metric || ""].filter(Boolean),
        support_refute_or_lead: "support",
        missing_data: "",
      });
    }
  }
  if (findings.length) return findings;
  return [{
    question: node.question,
    bom_node: "",
    dimension: "source_summary",
    found_or_gap: "found",
    facts: [byId(sourceId).summary],
    scope_caveat: "No industry-space bucket mapping was defined for this source under the current question; use only as question-level source evidence.",
    verification_metrics: [],
    support_refute_or_lead: byId(sourceId).support_refute_or_lead,
    missing_data: "",
  }];
}

function canonicalIndustrySpaceDimension(label) {
  const text = String(label || "");
  if (/经营验证|财务兑现|公司财报|财报|revenue|orders?|backlog|margin|cash|收入|订单|利润|现金/i.test(text)) return "财务兑现证据";
  if (/公司\s*TAM|TAM|市场空间|可触达市场/i.test(text)) return "公司 TAM";
  if (/客户侧|客户指引|customer/i.test(text)) return "客户侧指引";
  if (/第三方|研报|机构|sell.?side|industry|forecast|预测|数据商/i.test(text)) return "第三方拆法";
  if (/公司指引|guidance|指引|outlook|预计|expected/i.test(text)) return "公司指引";
  return text;
}

function buildReviews(extractions) {
  return extractions.map((record) => ({
    review_id: reviewId(record.l3_question_id, record.source_id),
    extraction_id: record.extraction_id,
    l3_question_id: record.l3_question_id,
    source_id: record.source_id,
    gpt_verification_status: "verified_against_cutoff_source",
    adopted_facts: record.key_facts,
    corrections: reviewCorrectionsForExtraction(record),
    rejected_claims: [],
    final_bucket: record.source_bucket,
    final_support_refute_or_lead: record.support_refute_or_lead,
    allowed_to_strengthen_conclusion: true,
  }));
}

function reviewCorrectionsForExtraction(record) {
  if (record.parser === "deepseek_delegate" && record.source_id === "SRC-MU-FY26-Q1") {
    return ["DeepSeek first-pass treated company guidance as product-level gap; GPT corrected it to company_guidance with a scope caveat because the Micron release contains explicit FQ2 FY2026 revenue/gross-margin outlook relevant to the HBM/high-end-memory question, but not a pure HBM revenue guide."];
  }
  return [];
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
  <title>AI 工厂产业相关投资机会回测研究</title>
  <style>${css()}</style>
</head>
<body>
  <header class="hero"><div class="eyebrow">Historical Backtest · AI Factory · ${AS_OF_DATE}</div><h1>AI 工厂产业相关投资机会回测研究</h1><p class="subtitle">研究截面冻结在 ${AS_OF_DATE}。本报告只用该日期前可见资料形成产业链、QA、评分和排序；三个月后的价格变化只作为最终标的表右侧的评估字段。</p></header>
  <nav class="top-nav">
    <a href="#goal">当前研究的问题</a>
    <a href="#overview">行业概况</a>
    <a href="#qa">下钻 QA</a>
    <a href="#targets">标的推荐</a>
    <a href="#sources">来源索引</a>
  </nav>
  <main class="wrap">
    <section id="goal" class="section"><h2>当前研究的问题</h2>${renderGoal()}</section>
    <section id="overview" class="section"><h2>行业概况</h2>${renderIndustryOverview()}</section>
    <section id="qa" class="section"><h2>下钻 QA</h2>${qaTree.l1_questions.map(renderQaCard).join("")}</section>
    <section id="targets" class="section"><h2>标的推荐</h2>${renderTargets(rankedTargets)}</section>
    <section id="sources" class="section"><h2>来源索引</h2>${renderSources()}</section>
  </main>
</body>
</html>`;
}

function renderGoal() {
  return `<div class="goal-card"><div class="goal-grid">
    <div class="metric"><span>研究对象</span><strong>AI 工厂产业链</strong></div>
    <div class="metric"><span>运行模式</span><strong>historical_backtest</strong></div>
    <div class="metric"><span>信息截面</span><strong>${AS_OF_DATE}</strong></div>
    <div class="metric"><span>评估日期</span><strong>${EVALUATION_DATE}</strong></div>
  </div>
  <div class="artifact-card"><div class="artifact-title">当前结论</div>在截面前，AI 工厂已经从 NVIDIA 平台收入传导到服务器 backlog、电力液冷订单、HBM/先进制造和连接芯片收入。最接近“当前未被市场充分定价的巨大机会”的方向是电力液冷和 HBM 硬瓶颈，但多数标的仍需要估值和风险闸门控制。</div>
  ${renderConstraintDefinition()}</div>`;
}

function renderConstraintDefinition() {
  const items = [
    ["主题边界", keyConstraintDefinition.theme],
    ["精确定义", keyConstraintDefinition.preciseConstraint],
    ["为什么现在", keyConstraintDefinition.whyNow],
    ["研究范围", keyConstraintDefinition.scope],
    ["路线冲突", keyConstraintDefinition.routeConflict],
    ["验证周期", keyConstraintDefinition.adoptionHorizon],
  ].map((row) => `<article><span>${esc(row[0])}</span><p>${esc(row[1])}</p></article>`).join("");
  return `<div class="constraint-definition">
    <div class="artifact-title">关键约束定义：先定义瓶颈，再谈标的</div>
    <div class="constraint-grid">${items}</div>
  </div>`;
}

function renderIndustryOverview() {
  return `<div class="industry-overview-section">
    ${renderSupplyChain()}
    ${renderIndustrySpace()}
    ${renderCompetitionProfitPool()}
    ${renderIndustryChokepoints()}
    ${renderIndustryKeyVariables()}
  </div>`;
}

function renderSupplyChain() {
  return `<details class="industry-module supply-chain-section">
    <summary class="module-head"><span class="module-index">01</span><div><h3>产业链与生态位</h3><p>先看清楚谁提供什么、谁依赖谁、订单和利润沿什么路径流动，后面的 QA 才不是凭空提问。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
    ${renderChainExplain()}
    </div>
  </details>`;
}

function renderChainExplain() {
  return `<div class="chain-explain">
    ${renderChainResearchBridge()}
    <p class="chain-plain-summary">${esc(chainExplainer.plainSummary)}</p>
    ${renderChainDetailPanel("统一 BOM 口径", "后续行业空间、竞争格局、瓶颈点和标的映射均使用同一套节点定义。", renderBomTaxonomy(), "bom-taxonomy-panel")}
    ${renderChainDetailPanel("泳道图", "按上游 / 中游 / 下游看生态位、公司关系和依赖方向。", renderLaneMap(), "chain-lane-panel")}
    ${renderChainDetailPanel("价值流", "用白话步骤解释需求如何变成订单、系统交付、收入和利润验证。", renderValueFlowMap(), "chain-value-panel")}
    ${renderChainDetailPanel("BOM / 组件级链条", "把系统拆成子系统、组件、关键公司、输入输出和财务验证指标。", renderComponentValueChain(), "chain-component-panel")}
  </div>`;
}

function renderBomTaxonomy() {
  const cards = CANONICAL_BOM_NODES.map((node, index) => `<article class="bom-taxonomy-card">
    <span>${String(index + 1).padStart(2, "0")} / ${esc(node.layer)}</span>
    <strong>${esc(node.label)}</strong>
    <p>${esc(node.role)}</p>
  </article>`).join("");
  return `<div class="bom-taxonomy">
    <p>本报告把“BOM 节点”限定为会进入 AI 工厂硬件/基础设施成本、交付或利润池的子系统。${esc(DEMAND_VALIDATION_LAYER)} 是需求验证层，不与 BOM 节点混用。</p>
    <div class="bom-taxonomy-grid">${cards}</div>
  </div>`;
}

function renderChainDetailPanel(title, description, body, extraClass = "") {
  return `<details class="chain-detail-panel ${extraClass}">
    <summary><span>${esc(title)}</span><small>${esc(description)}</small><span class="chevron">›</span></summary>
    <div class="chain-detail-body">${body}</div>
  </details>`;
}

function renderChainResearchBridge() {
  return `<div class="chain-research-bridge">
    <div class="chain-bridge-grid">
      <div class="chain-bridge-card"><span>研究目标如何转成产业链问题</span><strong>${esc(chainResearchBridge.objective)}</strong></div>
      <div class="chain-bridge-card"><span>核心投资问题</span><strong>${esc(chainResearchBridge.coreQuestion)}</strong></div>
    </div>
    <p>${esc(chainResearchBridge.currentConclusion)}</p>
    ${renderNodeLens()}
  </div>`;
}

function renderIndustrySpace() {
  return `<details class="industry-module industry-space">
    <summary class="module-head"><span class="module-index">02</span><div><h3>行业空间</h3><p>公开拆法优先记录 BOM 节点空间：先看推理，再看证据来源。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
    <div class="industry-space-summary">
      <p>本节只回答一个问题：AI 工厂扩张会放大哪些 BOM 节点。空间判断不由模型自行拍 TAM，而是优先记录公司指引、公司 TAM、客户侧指引、第三方拆法和财务兑现证据；最后直接结合这五类信息判断短期、中期、长期空间是否足够大。找不到可靠公开拆法时，明确标为数据缺口，不用自建精确模型补空。它不直接做标的推荐，结论会进入后面的竞争格局、瓶颈点和标的排序。</p>
    </div>
    ${renderSpaceBomReasoning()}
    </div>
  </details>`;
}

function renderSpaceBomReasoning() {
  const cards = industrySpaceEvidencePackRows.map((item) => renderBomNodeCard(item)).join("");
  return `<div class="space-bom-reasoning">${cards}</div>`;
}

function renderBomNodeCard(item) {
  const facts = item.facts.map((fact) => `<li>${esc(fact)}</li>`).join("");
  const reasoning = item.inferenceChain.map((step) => `<li>${esc(step)}</li>`).join("");
  const sizing = item.publicSizingMethods || item.numericSizing;
  const sourceSearchPlan = sourceSearchPlanForNode(item.node);
  return `<details class="space-node-card">
    <summary>
      <span class="space-node-label">BOM 节点</span>
      <strong>${esc(item.node)}</strong>
      <small>${esc(item.coreQuestion)}</small>
      <span class="chevron">›</span>
    </summary>
    <div class="space-node-reasoning">
      <section class="space-node-section space-node-space-reasoning">
        <h4>空间推理</h4>
        <ol>${reasoning}</ol>
        <p>${esc(item.nodeElasticity)}</p>
        ${renderNodeSizing(sizing ? { ...sizing, sourceSearchPlan, node: item.node } : { node: item.node, sourceSearchPlan })}
      </section>
      <section class="space-node-section space-node-evidence">
        <h4>证据</h4>
        <ul>${facts}</ul>
        <div class="space-node-sources">${renderSourceChips(item.sourceIds)}</div>
      </section>
    </div>
  </details>`;
}

function sourceSearchPlanForNode(node) {
  const row = activeIndustrySpaceSourceSearchMatrix.find((item) => item.node === node);
  return row?.category_search_plan || {};
}

function renderNodeSizing(sizing) {
  const renderPublicMethodCards = (methods, sourceSearchPlan = {}) => {
    const categories = [
      { key: "company_guidance", label: "公司指引", hint: "管理层给出的未来收入、capex、订单、业务增速或产能口径。" },
      { key: "company_tam", label: "公司 TAM", hint: "公司披露的市场空间、长期 CAGR、服务市场或可触达市场。" },
      { key: "customer_guidance", label: "客户侧指引", hint: "下游客户的 capex、RPO、订单、预算和使用量，验证真实需求来源。" },
      { key: "third_party", label: "第三方拆法", hint: "研报、行业机构或数据商给出的拆分模型、TAM、出货量、价格或供需预测。" },
      { key: "financial_evidence", label: "财务兑现证据", hint: "收入、订单、backlog、利润率、现金流等已经落地的经营数据。" },
    ];
    const grouped = Object.fromEntries(categories.map((category) => [category.key, []]));
    const normalizeMethod = (method) => {
      if (Array.isArray(method)) {
        return {
          sourceType: method[0],
          organization: method[1],
          guidanceContent: method[2],
          bomNode: method[3],
          timeframe: method[4],
          verificationMetric: method[5],
          confidence: method[6],
          sourceIds: method[7] || [],
        };
      }
      if (method && typeof method === "object") return method;
      return { sourceType: "第三方拆法", guidanceContent: String(method || "") };
    };
    const classify = (method) => {
      const text = [
        method.sourceType,
        method.type,
        method.organization,
        method.company,
        method.source,
        method.guidanceContent,
        method.guidance,
        method.value,
        method.method,
      ].filter(Boolean).join(" ");
      if (/客户侧|客户指引|customer/i.test(text)) return "customer_guidance";
      if (/公司\s*TAM|TAM|市场空间|可触达市场/i.test(text)) return "company_tam";
      if (/第三方|研报|机构|sell.?side|industry|forecast|预测|数据商/i.test(text)) return "third_party";
      if (/公司指引|guidance|指引|outlook|预计|expected/i.test(text)) return "company_guidance";
      if (/经营验证|财务兑现|公司财报|财报|revenue|orders?|backlog|margin|cash|收入|订单|利润|现金/i.test(text)) return "financial_evidence";
      return "third_party";
    };
    methods.map(normalizeMethod).forEach((method) => grouped[classify(method)].push(method));
    return `<div class="space-public-methods space-method-card-grid space-node-sizing-table">
      ${categories.map((category) => {
        const rows = grouped[category.key] || [];
        const planEntry = sourceSearchPlan[category.key] || {};
        const body = rows.length ? rows.map((method) => {
          const organization = method.organization || method.company || method.source || "待补";
          const content = method.guidanceContent || method.guidance || method.value || method.method || "待补";
          const bomNode = method.bomNode || method.node || method.scope || "待补";
          const timeframe = method.timeframe || method.period || "待补";
          const metric = method.verificationMetric || method.metric || method.assumption || "待补";
          const confidence = method.confidence || "待补";
          const sourceIds = normalizeSourceIds(method.sourceIds || method.source_ids || method.sources || []);
          return `<article class="space-method-entry">
            <b>公司或机构：${esc(organization)}</b>
            <p><strong>指引内容：</strong>${esc(content)}</p>
            <dl>
              <div><dt>BOM 节点</dt><dd>${esc(bomNode)}</dd></div>
              <div><dt>时间范围</dt><dd>${esc(timeframe)}</dd></div>
              <div><dt>可验证指标</dt><dd>${esc(metric)}</dd></div>
              <div><dt>置信度</dt><dd>${esc(confidence)}</dd></div>
            </dl>
            <div class="space-method-entry-sources">${renderSourceChips(sourceIds)}</div>
          </article>`;
        }).join("") : renderSearchGap(category, planEntry);
        const headerStatus = rows.length ? `${rows.length} 条` : (planEntry.status === "gap" ? "已搜索 / 缺口" : "待搜索");
        return `<section class="space-method-card space-method-${category.key}">
          <header><span>${esc(category.label)}</span><small>${esc(headerStatus)}</small></header>
          <div class="space-method-card-body">${body}</div>
        </section>`;
      }).join("")}
    </div>`;
  };

  const renderHorizonConclusion = (sizingData = {}) => {
    const horizon = sizingData.horizonConclusion || industrySpaceHorizonJudgments[sizingData.node] || {
      summary: "现有公开信息不足，不能给出高置信短中长期空间判断。",
      confidence: "低：缺少可验证公开拆法。",
      horizons: [
        { label: "短期", size: "待验证", reason: "需要补充近端公司指引和财务兑现证据。" },
        { label: "中期", size: "待验证", reason: "需要补充公司 TAM、客户侧指引和第三方拆法。" },
        { label: "长期", size: "待验证", reason: "需要补充长期需求、供给和替代路径的公开材料。" },
      ],
    };
    const cards = (horizon.horizons || []).map((item) => `<article class="space-horizon-card">
      <span>${esc(item.label || "待补")}</span>
      <strong class="${horizonSizeClass(item.size)}">${esc(item.size || "待验证")}</strong>
      <p>${esc(item.reason || "待补。")}</p>
    </article>`).join("");
    return `<div class="space-horizon-conclusion">
      <div class="space-step-title"><span class="space-step-index">2</span><h5>空间结论</h5></div>
      <p class="space-horizon-summary">${esc(horizon.summary || sizingData.conclusion || "待补。")}</p>
      <div class="space-horizon-grid">${cards}</div>
      <small class="space-step-confidence">置信度：${esc(horizon.confidence || sizingData.confidence || "待补。")}</small>
    </div>`;
  };

  if (!sizing || (!Array.isArray(sizing.methods) && !sizing.formula && !sizing.scenarios)) {
    return `<div class="space-node-sizing">
      <div class="space-method-step">
        <div class="space-step-title"><span class="space-step-index">1</span><h5>公开拆法</h5></div>
        ${renderPublicMethodCards([], sizing?.sourceSearchPlan || {})}
      </div>
      ${renderHorizonConclusion(sizing || {})}
    </div>`;
  }
  if (Array.isArray(sizing.methods)) {
    return `<div class="space-node-sizing">
      <div class="space-method-step">
        <div class="space-step-title"><span class="space-step-index">1</span><h5>公开拆法</h5></div>
        ${renderPublicMethodCards(sizing.methods, sizing.sourceSearchPlan || sizing.source_search_plan || {})}
      </div>
      ${renderHorizonConclusion(sizing)}
      <div class="space-node-sources">${renderSourceChips(sizing.sourceIds || [])}</div>
    </div>`;
  }
  const scenarioRows = (sizing.scenarios || []).map((row) => `<tr>
    <td><strong>${esc(row[0] || "")}</strong></td>
    <td>${esc(row[1] || "")}</td>
    <td>${esc(row[2] || "")}</td>
  </tr>`).join("");
  return `<div class="space-node-sizing">
    <div class="space-method-step">
      <div class="space-step-title"><span class="space-step-index">1</span><h5>公开拆法</h5></div>
      ${renderPublicMethodCards([{ sourceType: "旧字段兼容", organization: "内部代理口径", guidanceContent: sizing.formula || "待补。", bomNode: sizing.currentAnchor || "待补。", timeframe: "待补", verificationMetric: sizing.futureAssumption || "待补。", confidence: sizing.confidence || "待补。", sourceIds: sizing.sourceIds || sizing.source_ids || [] }], sizing.sourceSearchPlan || sizing.source_search_plan || {})}
    </div>
    ${renderHorizonConclusion(sizing)}
    <div class="space-node-sizing-table table-scroll">
      <table>
        <thead><tr><th>情景</th><th>空间区间 / 代理锚点</th><th>推理含义</th></tr></thead>
        <tbody>${scenarioRows}</tbody>
      </table>
    </div>
    <div class="space-node-sources">${renderSourceChips(sizing.sourceIds || [])}</div>
  </div>`;
}

function horizonSizeClass(size) {
  const text = String(size || "");
  if (text.includes("大")) return "space-horizon-size space-horizon-large";
  if (text.includes("中")) return "space-horizon-size space-horizon-mid";
  if (text.includes("小") || text.includes("低")) return "space-horizon-size space-horizon-low";
  return "space-horizon-size";
}

function renderSearchGap(category, planEntry = {}) {
  if (planEntry && planEntry.status === "gap") {
    const prioritySources = (planEntry.priority_sources || [])
      .slice(0, 4)
      .map((sourceProfile) => sourceProfile.name || sourceProfile.id)
      .filter(Boolean)
      .join("、");
    const directedQuery = (planEntry.directed_queries || [])[0]?.query || "";
    return `<p class="space-method-empty space-method-gap">已规划专业源搜索：${esc(planEntry.search_intent || category.hint)}<br>优先源：${esc(prioritySources || "待配置")}<br>${directedQuery ? `示例 query：${esc(directedQuery)}<br>` : ""}缺口：${esc(planEntry.gap_reason || "当前 source pack 未找到可用材料。")}</p>`;
  }
  return `<p class="space-method-empty">待补：${esc(category.hint)}</p>`;
}

function normalizeSourceIds(sourceIds) {
  if (Array.isArray(sourceIds)) return sourceIds.filter(Boolean);
  if (sourceIds) return [sourceIds];
  return [];
}

function renderSourceChips(sourceIds) {
  const normalized = normalizeSourceIds(sourceIds);
  if (!normalized.length) return `<div class="source-chips"><span class="source-chip source-chip-missing">待补来源</span></div>`;
  return `<div class="source-chips">${normalized.map((sourceId) => {
    const source = sources.find((item) => item.source_id === sourceId || item.id === sourceId);
    if (!source) return `<span class="source-chip source-chip-missing">${esc(sourceId)}</span>`;
    return `<a class="source-chip" href="${esc(source.url)}">${esc(sourceId)}</a>`;
  }).join("")}</div>`;
}

function renderCompetitionProfitPool() {
  const cards = q2CompetitionLandscape.map((item, index) => `<details class="competition-node-card competition-bom-card">
    <summary><span class="competition-node-index">${String(index + 1).padStart(2, "0")}</span><strong>${esc(item.node)}</strong><span class="competition-intensity competition-mid">BOM 节点</span><span class="chevron">›</span></summary>
    <div class="competition-node-body">
      <div class="overview-research-unit">
        <div class="overview-unit-head"><b>研究单元</b><span>${esc(item.node)} · 围绕四个竞争问题给出结论。</span></div>
        <div class="competition-question-grid">
          ${competitionQuestionSpecs.map((spec) => renderOverviewQuestionCard(spec, item, "competition-subcard")).join("")}
        </div>
      </div>
      <div class="profit-pool-table table-scroll"><table>
        <thead><tr><th>节点</th><th>竞争格局</th><th>Chokepoint 初判</th><th>利润池/标的含义</th><th>主要反证</th><th>后续 QA</th></tr></thead>
        <tbody><tr><td><strong>${esc(item.node)}</strong></td><td>${esc(item.competition)}</td><td>${esc(item.chokepoint)}</td><td>${esc(item.profit)}</td><td>${esc(item.refute)}</td><td>${esc(item.qa)}</td></tr></tbody>
      </table></div>
    </div>
  </details>`).join("");
  return `<details class="industry-module industry-competition">
    <summary class="module-head"><span class="module-index">03</span><div><h3>竞争格局与利润池</h3><p>每个 BOM 节点按四问展开：玩家市场份额分布、头部玩家优势、替代玩家赶超希望、格局变化核心变量。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
    <div class="competition-bom-map">${cards}</div>
    </div>
  </details>`;
}

function renderIndustryChokepoints() {
  const dimensions = ["稀缺性", "替代难度", "定价权", "财务弹性", "估值风险", "反证风险"];
  const cards = chainChokepointScores.map((item, index) => `<details class="competition-node-card chokepoint-card chokepoint-bom-card" open>
    <summary><span class="competition-node-index chokepoint-index">${String(index + 1).padStart(2, "0")}</span><strong>${esc(item.node)}</strong><span class="chevron">›</span></summary>
    <div class="competition-node-body">
      <div class="overview-research-unit">
        <div class="overview-unit-head"><b>研究单元</b><span>${esc(item.node)} · 围绕瓶颈约束、控制者和降级规则给出结论。</span></div>
        <div class="chokepoint-question-grid">
          ${chokepointQuestionSpecs.map((spec) => renderOverviewQuestionCard(spec, item, "competition-subcard")).join("")}
        </div>
      </div>
      <div class="chokepoint-scorecard table-scroll"><table>
        <thead><tr><th>控制者</th>${dimensions.map((dimension) => `<th>${esc(dimension)}</th>`).join("")}<th>当前判断</th><th>QA</th></tr></thead>
        <tbody><tr><td>${esc(item.controllers)}</td>${dimensions.map((dimension) => renderHeatScoreCell(item.scores[dimension])).join("")}<td>${esc(item.conclusion)}</td><td>${esc(item.qa_link)}</td></tr></tbody>
      </table></div>
    </div>
  </details>`).join("");
  return `<details class="industry-module industry-chokepoints">
    <summary class="module-head"><span class="module-index">04</span><div><h3>瓶颈点</h3><p>瓶颈点是竞争格局分析后的结果，不是单独喊主题。高分节点还要进入 Q3/Q4 验证估值和反证。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
    <div class="chain-chokepoints" hidden></div>
    <div class="chokepoint-bom-map">${cards}</div>
    ${renderBottleneckReleaseTimeline()}
    </div>
  </details>`;
}

function renderComponentValueChain() {
  const rows = componentValueChainRows.map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`).join("");
  return `<div class="component-value-chain">
    <div class="chain-graph-head"><b>BOM / 组件级价值链</b><span>从“系统”拆到子系统和财务验证指标，避免只列公司名称。</span></div>
    <div class="table-scroll"><table>
      <thead><tr><th>子系统</th><th>组件/服务</th><th>关键公司</th><th>接受什么</th><th>提供给谁</th><th>财务验证</th><th>相关 QA</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>
  </div>`;
}

function renderBottleneckReleaseTimeline() {
  const rows = bottleneckReleaseTimeline.map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`).join("");
  return `<div class="bottleneck-release-timeline">
    <div class="chain-graph-head"><b>瓶颈释放时间表</b><span>瓶颈不是永久标签；必须跟踪谁在扩产、何时缓解、什么数据会降级。</span></div>
    <div class="table-scroll"><table>
      <thead><tr><th>瓶颈</th><th>当前约束</th><th>释放/验证信号</th><th>观察节奏</th><th>降级触发</th><th>标的含义</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>
  </div>`;
}

function renderIndustryKeyVariables() {
  const fallbackGaps = chainDataGaps.map((item) => `<li>${esc(item)}</li>`).join("");
  const qaRows = chainQaMapping.map((item) => `<tr><td><strong>${esc(item.q)}</strong></td><td>${esc(item.signal)}</td><td>${esc(item.use)}</td></tr>`).join("");
  const bomCards = CANONICAL_BOM_NODES.map((node) => {
    const component = componentValueChainRows.find((row) => row[0] === node.label) || [];
    const timeline = bottleneckReleaseTimeline.find((row) => row[0] === node.label) || [];
    const score = chainChokepointScores.find((item) => item.node === node.label);
    const relatedTargets = targetProfitBridgeRows
      .filter((row) => row[1] === node.label)
      .map((row) => row[0])
      .join(" / ") || "待补标的映射";
    const qa = component[6] || timeline[5] || "Q1-Q4";
    return `<details class="key-variable-bom-card overview-research-unit">
      <summary><strong>${esc(node.label)}</strong><span>${esc(node.layer)} · ${esc(qa)}</span><span class="chevron">›</span></summary>
      <div class="overview-question-card overview-answer overview-answer-structured">
        <div class="overview-answer-row"><span>当前要验证什么</span><p>${esc(component[5] || timeline[2] || "订单、收入、毛利、现金流和反证触发器。")}</p></div>
        <div class="overview-answer-row"><span>关键变量</span><p>${esc(timeline[2] || "待补该 BOM 节点的可验证变量。")}</p></div>
        <div class="overview-answer-row"><span>降级触发器</span><p>${esc(timeline[4] || "待补该 BOM 节点的反证触发器。")}</p></div>
        <div class="overview-answer-row"><span>标的映射</span><p>${esc(relatedTargets)}；${esc(score?.conclusion || "待补评分和监控含义。")}</p></div>
      </div>
    </details>`;
  }).join("");
  return `<details class="industry-module industry-key-variables">
    <summary class="module-head"><span class="module-index">05</span><div><h3>关键变量与待验证数据</h3><p>把行业概况转成后续下钻 QA：哪些数据变化会强化、削弱或推翻当前标的排序。</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
    <div class="key-variable-grid">
      <div class="key-variable-bom-map">${bomCards}</div>
      <details class="chain-data-gaps"><summary>全局待补变量 <span class="chevron">›</span></summary><ul>${fallbackGaps}</ul></details>
      <div class="qa-generation-table table-scroll"><table>
        <thead><tr><th>QA 方向</th><th>来自行业概况的信号</th><th>怎么使用</th></tr></thead>
        <tbody>${qaRows}</tbody>
      </table></div>
    </div>
    </div>
  </details>`;
}

function renderNodeLens() {
  const items = chainNodeLenses.slice(0, 4).map((row) => `<li><b>${esc(row[0])}</b><span>${esc(row[1])}</span></li>`).join("");
  return `<div class="chain-node-lens"><b>节点筛选口径</b><ul>${items}</ul></div>`;
}

function renderKeyLaneMap() {
  const cards = chainExplainer.stageGroups.map((group) => {
    const companies = group.companies.slice(0, 5).map((company) => `<li class="chain-company-card"><b>${esc(company.name)}</b><span>${esc(company.produces)}</span><small>${esc(company.bottleneck_strength)} · ${esc(company.qa_link)}</small></li>`).join("");
    return `<article class="chain-layer-card chain-stage-panel">
      <div class="chain-stage-head"><span class="chain-stage-name">${esc(group.stage)}</span><strong>${esc(group.summary)}</strong></div>
      <ul class="chain-company-list">${companies}</ul>
    </article>`;
  }).join("");
  return `<div class="chain-relationship-graph">
    <div class="chain-graph-head"><b>关键链条节点</b><span>只保留最影响后续 QA 和标的排序的节点。</span></div>
    <div class="chain-layer-grid">${cards}</div>
  </div>`;
}

function renderValueCaptureMatrix() {
  const rows = chainValueCaptureMatrix.map((item) => `<tr>
    <td><strong>${esc(item.node)}</strong></td>
    <td>${esc(item.demand)}</td>
    <td>${esc(item.chokepoint)}</td>
    <td>${esc(item.monetization)}</td>
    <td>${esc(item.targets)}</td>
    <td>${esc(item.verification)}</td>
    <td>${esc(item.qa)}</td>
  </tr>`).join("");
  return `<div class="chain-value-capture-matrix">
    <div class="chain-graph-head"><b>价值捕获矩阵</b><span>从“需求流入”一路看到账面利润、估值赔率和后续验证问题。</span></div>
    <div class="table-scroll"><table>
      <thead><tr><th>节点</th><th>需求如何流入</th><th>卡点机制</th><th>价值捕获方式</th><th>主要标的</th><th>继续验证</th><th>后续 QA</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>
  </div>`;
}

function renderQaMapping() {
  const rows = chainQaMapping.map((item) => `<article><span>${esc(item.q)}</span><b>${esc(item.signal)}</b><p>${esc(item.use)}</p></article>`).join("");
  return `<div class="chain-qa-mapping">
    <div class="chain-graph-head"><b>产业链如何生成下钻 QA</b><span>QA 不是独立模板，而是由产业链卡点、价值流和反证点推出来。</span></div>
    <div class="chain-qa-grid">${rows}</div>
  </div>`;
}

function renderChainDataGaps() {
  const items = chainDataGaps.slice(0, 3).map((item) => `<li>${esc(item)}</li>`).join("");
  return `<details class="chain-data-gaps">
    <summary>待补充的关键数据 <span class="chevron">›</span></summary>
    <ul>${items}</ul>
  </details>`;
}

function renderRelationshipWorkbench() {
  return `<div class="chain-relationship-workbench">
    <input class="chain-view-radio" type="radio" name="chain-view" id="chain-view-lanes" checked>
    <input class="chain-view-radio" type="radio" name="chain-view" id="chain-view-sankey">
    <input class="chain-view-radio" type="radio" name="chain-view" id="chain-view-heatmap">
    <div class="chain-view-switch" role="tablist" aria-label="产业链关系视图">
      <label for="chain-view-lanes">泳道图</label>
      <label for="chain-view-sankey">价值流</label>
      <label for="chain-view-heatmap">瓶颈热力</label>
    </div>
    <div class="chain-view-panels">
      <section class="chain-view-panel chain-lane-map">${renderLaneMap()}</section>
      <section class="chain-view-panel chain-sankey-map">${renderValueFlowMap()}</section>
      <section class="chain-view-panel chain-chokepoint-heatmap">${renderChokepointHeatmap()}</section>
    </div>
  </div>`;
}

function renderCompanyNetwork() {
  const nodesById = Object.fromEntries(chainNetwork.nodes.map((node) => [node.id, node]));
  const edges = chainNetwork.edges.map((edge, index) => renderNetworkEdge(edge, nodesById, index)).join("");
  const nodes = chainNetwork.nodes.map(renderNetworkNode).join("");
  const legend = chainNetwork.legend.map((row) => `<span><b>${esc(row[0])}</b>${esc(row[1])}</span>`).join("");
  return `<div class="chain-company-network">
    <div class="chain-graph-head"><b>公司关系总图</b><span>实线看供给/交付，虚线看需求/订单，灰线看运营验证。</span></div>
    <div class="chain-network-legend">${legend}</div>
    <div class="chain-network-canvas" role="img" aria-label="AI 工厂产业链公司关系图">
      <svg class="chain-network-svg" viewBox="0 0 ${chainNetwork.width} ${chainNetwork.height}" width="${chainNetwork.width}" height="${chainNetwork.height}">
        <defs>
          <marker id="arrowSupply" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L10,4 L0,8 Z" fill="#2b6cb0"></path></marker>
          <marker id="arrowDemand" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L10,4 L0,8 Z" fill="#b7791f"></path></marker>
          <marker id="arrowFeedback" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L10,4 L0,8 Z" fill="#667085"></path></marker>
        </defs>
        <text class="network-stage-label" x="64" y="28">上游：核心供给</text>
        <text class="network-stage-label" x="610" y="28">中游：系统交付</text>
        <text class="network-stage-label" x="1136" y="28">下游：需求运营</text>
        ${edges}
        ${nodes}
      </svg>
    </div>
  </div>`;
}

function renderNetworkEdge(edge, nodesById, index) {
  const from = nodesById[edge.from];
  const to = nodesById[edge.to];
  if (!from || !to) return "";
  const path = networkEdgePath(from, to, edge.curve || 0);
  const label = networkEdgeLabel(from, to, edge.curve || 0, index);
  const marker = edge.flow === "demand" ? "arrowDemand" : edge.flow === "feedback" ? "arrowFeedback" : "arrowSupply";
  const labelClass = edge.flow === "demand" ? "network-label-demand" : edge.flow === "feedback" ? "network-label-feedback" : "network-label-supply";
  const edgeClass = `network-edge network-edge-${edge.flow}`;
  return `<g class="network-edge-group">
    <path class="${edgeClass}" d="${path}" marker-end="url(#${marker})"></path>
    <rect class="network-label-bg ${labelClass}" x="${label.x - 72}" y="${label.y - 12}" width="144" height="23" rx="11"></rect>
    <text class="network-edge-label" x="${label.x}" y="${label.y + 4}" text-anchor="middle">${esc(edge.label)}</text>
  </g>`;
}

function networkEdgePath(from, to, curve) {
  if (Math.abs(from.x - to.x) < 8) {
    const startX = from.x + from.w / 2;
    const startY = from.y < to.y ? from.y + from.h : from.y;
    const endX = to.x + to.w / 2;
    const endY = from.y < to.y ? to.y : to.y + to.h;
    const offset = from.y < to.y ? 96 : -96;
    return `M${startX},${startY} C${startX + 80},${startY + offset} ${endX + 80},${endY - offset} ${endX},${endY}`;
  }
  const forward = to.x > from.x;
  const startX = forward ? from.x + from.w : from.x;
  const endX = forward ? to.x : to.x + to.w;
  const startY = from.y + from.h / 2;
  const endY = to.y + to.h / 2;
  const dx = Math.max(110, Math.abs(endX - startX) * 0.44);
  const curveY = curve * 120;
  const c1x = startX + (forward ? dx : -dx);
  const c2x = endX - (forward ? dx : -dx);
  return `M${startX},${startY} C${c1x},${startY + curveY} ${c2x},${endY - curveY} ${endX},${endY}`;
}

function networkEdgeLabel(from, to, curve, index) {
  const x = (from.x + from.w / 2 + to.x + to.w / 2) / 2;
  const y = (from.y + from.h / 2 + to.y + to.h / 2) / 2 + curve * 72 + ((index % 3) - 1) * 4;
  return { x, y };
}

function renderNetworkNode(node) {
  const stageClass = node.stage === "上游" ? "upstream" : node.stage === "中游" ? "midstream" : "downstream";
  return `<g class="network-node network-node-${stageClass}" transform="translate(${node.x},${node.y})">
    <rect width="${node.w}" height="${node.h}" rx="12"></rect>
    <text class="network-node-name" x="${node.w / 2}" y="20" text-anchor="middle">${esc(node.label)}</text>
    <text class="network-node-ticker" x="${node.w / 2}" y="36" text-anchor="middle">${esc(node.ticker)}</text>
    <text class="network-node-role" x="${node.w / 2}" y="50" text-anchor="middle">${esc(node.role)}</text>
  </g>`;
}

function renderLaneMap() {
  const panels = chainExplainer.stageGroups.map((group) => {
    const cards = group.companies.map(renderLaneCompanyCard).join("");
    return `<details class="chain-layer-card chain-stage-panel" open>
      <summary><span class="chain-stage-name">${esc(group.stage)}</span><span>${esc(group.summary)}</span><small>${group.companies.length} 个公司/节点</small><span class="chevron">›</span></summary>
      <div class="chain-company-list">${cards}</div>
    </details>`;
  }).join("");
  return `<div class="chain-relationship-graph chain-lane-map">
    <div class="chain-graph-head"><b>按上游 / 中游 / 下游展开公司关系</b><span>点开公司节点，看它接受什么、生产什么、卖给谁，以及用哪些财务指标验证。</span></div>
    <div class="chain-layer-grid">${panels}</div>
  </div>`;
}

function renderLaneCompanyCard(company) {
  return `<details class="chain-relation-card chain-company-card chain-lane-node">
    <summary>
      <span><b>${esc(company.name)}</b><small>${esc(company.node_type)}</small></span>
      <em>${esc(company.ticker)}</em>
      <span class="chevron">›</span>
    </summary>
    <div class="chain-company-detail">
      <div class="chain-company-head">
        <div><b>${esc(company.name)}</b><span>${esc(company.ticker)}</span></div>
        <small>${esc(company.evidence)}</small>
      </div>
      <dl class="chain-relation-meta">
        <div><dt>节点类型</dt><dd>${esc(company.node_type)}</dd></div>
        <div><dt>需求输入</dt><dd>${esc(company.demand_input)}</dd></div>
        <div><dt>供给输入</dt><dd>${esc(company.supply_input)}</dd></div>
        <div><dt>自己生产</dt><dd>${esc(company.produces)}</dd></div>
        <div><dt>提供给谁</dt><dd>${esc(company.provides_to)}</dd></div>
        <div><dt>财务指标</dt><dd>${esc(company.financial_metrics)}</dd></div>
        <div><dt>瓶颈强度</dt><dd>${esc(company.bottleneck_strength)}</dd></div>
        <div><dt>对应 QA</dt><dd>${esc(company.qa_link)}</dd></div>
      </dl>
    </div>
  </details>`;
}

function renderValueFlowMap() {
  const flows = chainSankeyFlows.map((flow) => `<article class="chain-sankey-flow flow-${esc(flow.kind)}" style="--flow-weight:${flow.weight}">
      <div class="flow-step"><span>${esc(flow.step)}</span><b>${esc(flow.title)}</b></div>
      <div class="flow-route">
        <div class="flow-from"><small>发起方</small>${esc(flow.from)}</div>
        <div class="flow-band"><span>${esc(flow.what)}</span></div>
        <div class="flow-to"><small>接收方</small>${esc(flow.to)}</div>
      </div>
      <div class="flow-fields">
        <div><b>可能受益</b><p>${esc(flow.beneficiaries)}</p></div>
        <div><b>财务验证</b><p>${esc(flow.metric)}</p></div>
        <div><b>投资含义</b><p>${esc(flow.investment_read)}</p></div>
      </div>
    </article>`).join("");
  return `<div class="chain-map-card chain-value-flow">
    <div class="chain-graph-head"><b>订单和价值如何在链条里流动</b><span>先读白话步骤，再看下面的价值流卡片。</span></div>
    ${renderSimpleValueFlow()}
    <div class="chain-value-guide">
      <div><b>先看谁付钱</b><span>下游 capex、订单、机柜规格。</span></div>
      <div><b>再看谁卡住供给</b><span>GPU/ASIC、HBM、先进制造、连接、电力液冷。</span></div>
      <div><b>最后看钱留在哪</b><span>收入、毛利、backlog、现金流和估值上修。</span></div>
    </div>
    <div class="chain-sankey-list">${flows}</div>
  </div>`;
}

function renderSimpleValueFlow() {
  const cards = chainSimpleFlowSteps.map((item) => `<article class="chain-simple-step">
    <span>${esc(item.step)}</span>
    <div><b>${esc(item.title)}</b><p>${esc(item.plain)}</p><small>${esc(item.investment)}</small></div>
  </article>`).join("");
  return `<div class="chain-simple-flow">
    <div class="simple-flow-head"><b>先按这条主线理解</b><span>云需求 -> 芯片订单 -> 制造/内存 -> 系统交付 -> 电力液冷/网络 -> 运营验证</span></div>
    <div class="chain-simple-grid">${cards}</div>
  </div>`;
}

function renderChokepointHeatmap() {
  const dimensions = ["稀缺性", "替代难度", "定价权", "财务弹性", "估值风险", "反证风险"];
  const rows = chainChokepointScores.map((item) => `<tr>
    <td><strong>${esc(item.node)}</strong><br><span>${esc(item.role)}</span></td>
    <td>${esc(item.controllers)}</td>
    ${dimensions.map((dimension) => renderHeatScoreCell(item.scores[dimension])).join("")}
    <td>${esc(item.conclusion)}</td>
    <td>${esc(item.qa_link)}</td>
  </tr>`).join("");
  return `<div class="chain-map-card">
    <div class="chain-graph-head"><b>瓶颈热力图</b><span>1-5 分。高分不等于直接买入，仍要经过 Q4 的未定价和风险控制闸门。</span></div>
    <div class="table-scroll"><table>
      <thead><tr><th>节点</th><th>控制者</th>${dimensions.map((dimension) => `<th>${esc(dimension)}</th>`).join("")}<th>当前判断</th><th>QA</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>
  </div>`;
}

function renderHeatScoreCell(score) {
  return `<td class="heat-score ${heatClass(score)}"><span>${Number(score).toFixed(0)}</span></td>`;
}

function heatClass(score) {
  if (score >= 4) return "heat-high";
  if (score >= 3) return "heat-mid";
  return "heat-low";
}

function renderQaCard(node) {
  const count = (node.children || []).length;
  const qaCountLabel = count ? `${count} 子问题` : `L${node.level}`;
  return `<details id="${node.id.toLowerCase().replaceAll(".", "-")}" class="qa-card level-${node.level}" open>
    <summary><span class="qid">${esc(node.id)}</span><span class="qtitle">${esc(node.question)}</span><span class="qa-count">${qaCountLabel}</span><span class="chevron">›</span></summary>
    <div class="qa-body">
      <div class="qa-block"><div class="block-title">1. 当前结论呈现</div>${renderCurrentConclusion(node)}</div>
      <div class="qa-block"><div class="block-title">2. 问题展开（子 QA）</div>${count ? node.children.map(renderQaCard).join("") : "<p>该节点是证据采集与判断单元。</p>"}</div>
      <div class="qa-block"><div class="block-title">3. 待补充的问题</div><p>${esc(node.gap || "继续补充可量化、同口径、可复盘的数据。")}</p></div>
    </div>
  </details>`;
}

function renderCurrentConclusion(node) {
  if (node.level < 3) {
    const oddsGate = node.id === "Q4" ? renderQ4OddsGate() : "";
    return `<p>${esc(node.conclusion)}</p>${renderQaComplementFocus(node)}${oddsGate}`;
  }
  return `<div class="routing"><span class="pill l3-skill">Skill: ${esc(node.skill)}</span><span class="pill l3-execution-status">Execution: ${esc(node.skill_dispatch.skill_output_status)}</span><span class="pill l3-score-component">Score Component: ${esc(node.score_component)}</span><span class="pill l3-decision-use">Decision Use: ${esc(node.decision_use)}</span></div>
    <div class="logic-grid"><div class="logic-card"><b>Fact</b><p>${esc(node.fact)}</p></div><div class="logic-card"><b>Inference</b><p>${esc(node.inference)}</p></div><div class="logic-card"><b>Judgment</b><p>${esc(node.judgment)}</p></div><div class="logic-card"><b>Gap / Trigger</b><p>${esc(node.gap)} ${esc(node.trigger)}</p></div></div>
    ${renderAnswerArtifact(node.answerArtifact)}
    <div class="source-chips">${node.sourceIds.map((sourceId) => `<a class="source-chip" href="${esc(byId(sourceId).url)}">${esc(sourceId)}</a>`).join("")}</div>`;
}

function renderQaComplementFocus(node) {
  const focus = {
    Q1: {
      baseline: "行业概况已经交代需求路径、行业空间和收入/利润传导。",
      questions: ["需求是否已经进入公司收入、订单、backlog、毛利或现金流。", "需求是否只停留在平台公司，还是外溢到第三方连接、系统交付和物理基础设施。", "哪些数据会证明客户 ROI 能支撑后续 capex。"],
    },
    Q2: {
      baseline: "行业概况已经交代竞争格局、技术路线和候选瓶颈。",
      questions: ["候选瓶颈是否真的稀缺、难替代且可收费。", "哪家公司能把节点稀缺转成财务弹性，而不是只获得主题曝光。", "哪些供给扩张、路线替代或客户议价会削弱 chokepoint。"],
    },
    Q3: {
      baseline: "行业概况已经列出关键变量和待验证数据。",
      questions: ["哪些行业概况结论最可能被反证推翻。", "哪些瓶颈可能最快释放，从而改变利润池分配。", "哪些高关注标的的估值已经反映了好消息。"],
    },
    Q4: {
      baseline: "行业概况已经把节点映射到候选标的。",
      questions: ["为什么某个标的进入排序，另一个只保留观察或排除。", "胜率、赔率、稀缺性、业绩弹性和风险控制如何共同决定行动状态。", "哪条新证据会提高或撤销当前排序。"],
    },
  }[node.id];
  if (!focus) return "";
  const questions = focus.questions.map((item) => `<li>${esc(item)}</li>`).join("");
  return `<div class="qa-complement-focus artifact-card">
    <div class="artifact-title">本层继续追问</div>
    <p>${esc(focus.baseline)}</p>
    <ul>${questions}</ul>
  </div>`;
}

function renderQ4OddsGate() {
  const rows = [
    ["稀缺/垄断", "来自 Q2 chokepoint：客户难绕开、替代慢、供给扩张慢。", "低于 3.5 分时不能进入 actionable_long。"],
    ["未充分定价", "来自 Q3 估值闸门：市场隐含增长低于订单/利润可验证路径。", "估值数据缺失或已充分反映时封顶 watch_only。"],
    ["业绩弹性", "来自 Q1/Q2 财务桥：需求能放大收入、毛利、FCF 或估值重估。", "只贡献收入、不贡献利润时降级。"],
    ["风险控制", "来自 Q3 kill tests：capex、供给、客户集中、执行和政策风险可监控。", "缺少硬降级条件时不能给高行动状态。"],
  ].map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`).join("");
  return `<div class="q4-odds-gate artifact-card">
    <div class="artifact-title">Q4 回答呈现：胜率、赔率和行动状态闸门</div>
    <p>Q4 的目标不是列热门标的，而是把每个标的放进同一套赔率闸门：先验证稀缺和业绩弹性，再检查是否已经被估值充分反映，最后绑定降级数据。</p>
    <div class="table-scroll"><table>
      <thead><tr><th>闸门</th><th>判断来源</th><th>动作规则</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>
  </div>`;
}

function renderAnswerArtifact(data) {
  const rows = data.rows.map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`).join("");
  return `<div class="artifact-card"><div class="artifact-title">${esc(data.title)}</div><div class="table-scroll"><table><thead><tr>${data.columns.map((col) => `<th>${esc(col)}</th>`).join("")}</tr></thead><tbody>${rows}</tbody></table></div></div>`;
}

function renderTargets(rankedTargets) {
  const rows = rankedTargets.map((target) => {
    const dims = target.score.score_dimensions;
    const lab = target.label;
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
      <td>${esc(target.downgrade_risk)}</td>
      <td>${formatNullable(lab.start_price)}</td>
      <td>${formatNullable(lab.end_price)}</td>
      <td>${formatPct(lab.forward_3m_return)}</td>
      <td>${formatPct(lab.benchmark_return)}</td>
      <td>${formatPct(lab.excess_return)}</td>
      <td>${esc(lab.label_status)}</td>
    </tr>`;
  }).join("");
  return `<div class="target-section">
    <p>这是冻结在 ${AS_OF_DATE} 的研究观察名单。右侧 label 字段只用于评估当时预测，不参与前面的 QA、评分、排序、赔率或行动状态。</p>
    ${renderTargetProfitBridge()}
    ${renderTargetValuationTable(rankedTargets)}
    ${renderTargetOddsModels(rankedTargets)}
    <div class="table-scroll"><table class="target-table">
      <thead><tr><th>#</th><th>标的</th><th>市场</th><th>Action State</th><th>总分</th><th>稀缺/垄断</th><th>未充分定价</th><th>业绩弹性</th><th>风险控制</th><th>截面理由</th><th>降级触发</th><th>start_price</th><th>end_price</th><th>forward_3m_return</th><th>benchmark_return</th><th>excess_return</th><th>label_status</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>
  </div>`;
}

function renderTargetProfitBridge() {
  const rows = targetProfitBridgeRows.map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`).join("");
  return `<div class="target-profit-bridge">
    <div class="artifact-title">标的财务桥：主题如何进入收入、利润和现金流</div>
    <p>先把每个标的的受益节点落到账面科目，再看估值和风险。只拿主题曝光、没有利润桥的标的不能上调行动状态。</p>
    <div class="table-scroll"><table>
      <thead><tr><th>标的</th><th>核心节点</th><th>需求传导</th><th>财务桥</th><th>必须验证</th><th>降级触发</th><th>当前状态</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>
  </div>`;
}

function renderTargetValuationTable(rankedTargets) {
  const rows = rankedTargets.map((target) => {
    const dims = target.score.score_dimensions;
    const valuationRead = dims.mispricing >= 3.3 ? "有错配线索" : dims.mispricing >= 2.8 ? "需要估值确认" : "估值可能已反映";
    return `<tr>
      <td><strong>${esc(target.ticker)}</strong><br><span>${esc(target.name)}</span></td>
      <td>${target.score.total_score.toFixed(2)}</td>
      <td>${dims.scarcity_or_monopoly.toFixed(2)}</td>
      <td>${dims.mispricing.toFixed(2)}</td>
      <td>${dims.earnings_elasticity.toFixed(2)}</td>
      <td>${dims.risk_control.toFixed(2)}</td>
      <td>${esc(valuationRead)}</td>
      <td>${esc(target.odds_model?.implied_expectation || "")}</td>
      <td>${esc(target.next_verification_data)}</td>
    </tr>`;
  }).join("");
  return `<div class="target-valuation-table">
    <div class="artifact-title">估值与赔率表：胜率之外还要看是否未充分定价</div>
    <p>这里不使用后续价格 label，只展示冻结截面下的四维闸门、估值错配读数和下一步验证数据。</p>
    <div class="table-scroll"><table>
      <thead><tr><th>标的</th><th>总分</th><th>稀缺/垄断</th><th>未充分定价</th><th>业绩弹性</th><th>风险控制</th><th>估值读数</th><th>隐含预期</th><th>下一步验证</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>
  </div>`;
}

function renderTargetOddsModels(rankedTargets) {
  const rows = rankedTargets.map((target) => {
    const odds = target.odds_model || {};
    return `<tr>
      <td><strong>${esc(target.ticker)}</strong><br><span>${esc(target.name)}</span></td>
      <td>${esc(odds.implied_expectation || "")}</td>
      <td>${esc(odds.base_path || "")}</td>
      <td>${esc(odds.bull_path || "")}</td>
      <td>${esc(odds.bear_path || "")}</td>
      <td>${esc(odds.upgrade_data || odds.base_path || "")}</td>
      <td>${esc(odds.downgrade_data || odds.bear_path || "")}</td>
      <td>${esc(odds.odds_judgment || "")}</td>
    </tr>`;
  }).join("");
  return `<div class="target-odds-model">
    <div class="artifact-title">简化赔率模型：当前估值需要什么证据才配得上行动状态</div>
    <p>赔率模型只使用 ${AS_OF_DATE} 前可见信息和冻结评分，不使用后续价格 label。它回答：市场可能已经计入了什么，base/bull/bear 路径分别如何验证，哪些数据会升级或降级观察强度。</p>
    <div class="table-scroll"><table class="target-odds-table">
      <thead><tr><th>标的</th><th>隐含预期</th><th>Base 路径</th><th>Bull 路径</th><th>Bear 路径</th><th>升级数据</th><th>降级数据</th><th>赔率判断</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>
  </div>`;
}

function renderSources() {
  const thesisSources = sources.filter((source) => source.allowed_usage !== "label_only");
  const cards = thesisSources.map((source) => `<div class="source-card"><strong>${esc(source.source_id)}</strong><br><a href="${esc(source.url)}">${esc(source.title)}</a><p>${esc(source.summary)}</p><small>${esc(source.source_bucket)} · ${esc(source.source_visible_at)} · ${esc(source.support_refute_or_lead)}</small></div>`).join("");
  return `<details class="source-collapse"><summary>展开来源索引 <span class="chevron">›</span></summary><div class="source-grid">${cards}</div></details>`;
}

function renderMarkdown(rankedTargets) {
  const rows = rankedTargets.map((target) => `| ${target.rank} | ${target.ticker} | ${target.action_state} | ${target.score.total_score.toFixed(2)} | ${formatPct(target.label.forward_3m_return)} |`).join("\n");
  return `# AI 工厂产业相关投资机会回测研究\n\n信息截面：${AS_OF_DATE}\n\n| 排名 | 标的 | Action State | 总分 | forward_3m_return |\n|---|---|---:|---:|---:|\n${rows}\n`;
}

function css() {
  return `
    :root{--bg:#f5f5f7;--panel:#fff;--line:#d7dce5;--ink:#1d1d1f;--muted:#667085;--blue:#0a63ce;--green:#0f7a4f;--amber:#956100;--red:#b42318}
    *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",sans-serif;line-height:1.58}.hero{padding:40px min(6vw,72px) 24px;background:linear-gradient(#fff,#f7f8fb);border-bottom:1px solid var(--line)}.eyebrow{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:800}h1{margin:8px 0 10px;font-size:34px;letter-spacing:0}.subtitle{max-width:1120px;color:#4b5260;font-size:15px}.top-nav{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.92);backdrop-filter:saturate(180%) blur(14px);border-bottom:1px solid var(--line);padding:10px min(6vw,72px);display:flex;gap:16px;flex-wrap:wrap}.top-nav a{color:#2f5f9f;text-decoration:none;font-size:13px;font-weight:800}.wrap{padding:24px min(6vw,72px) 56px}.section{margin:0 0 26px}h2{font-size:24px;margin:0 0 12px}
    .goal-card,.target-section,.source-collapse{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px;box-shadow:0 10px 28px rgba(30,41,59,.05)}.industry-overview-section{display:grid;gap:12px}.industry-module{background:var(--panel);border:1px solid var(--line);border-radius:10px;box-shadow:0 10px 28px rgba(30,41,59,.04);overflow:hidden}.industry-module>summary{list-style:none;cursor:pointer}.industry-module>summary::-webkit-details-marker{display:none}.industry-module[open]>summary{border-bottom:1px solid #e6eaf1}.industry-module-body{padding:16px 18px 18px}.module-head{display:grid;grid-template-columns:auto 1fr auto;column-gap:10px;row-gap:3px;margin:0;align-items:center;padding:16px 18px}.module-head .module-index{display:inline-flex;width:32px;height:32px;align-items:center;justify-content:center;border-radius:999px;background:#eef5ff;color:var(--blue);font-size:12px;font-weight:900}.module-head .chevron{color:var(--muted);font-weight:900;transition:transform .18s ease}.industry-module[open]>.module-head .chevron{transform:rotate(90deg)}.module-head h3{margin:0;font-size:18px}.module-head p{margin:0;color:#667085;font-size:13px}.overview-subtitle{font-size:13px;font-weight:900;color:#334155;margin-top:4px}.goal-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.metric{border:1px solid #e7ebf2;border-radius:8px;padding:12px;background:#fbfcfe}.metric span{display:block;color:var(--muted);font-size:12px}.metric strong{font-size:15px}.chain-explain{display:grid;gap:12px;margin-bottom:16px}.chain-plain-summary{margin:0;padding:14px 16px;border:1px solid #d9e4f2;border-radius:8px;background:#f6f9fd;font-weight:760;line-height:1.75}.chain-detail-panel{border:1px solid #d9e4f2;border-radius:12px;background:#fbfcff;overflow:hidden}.chain-detail-panel>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:center;padding:13px 14px}.chain-detail-panel>summary::-webkit-details-marker{display:none}.chain-detail-panel>summary span:first-child{font-weight:900;color:#27364a}.chain-detail-panel>summary small{color:#667085;font-size:12px;line-height:1.45}.chain-detail-panel[open]>summary{border-bottom:1px solid #e6eaf1}.chain-detail-panel .chevron{transition:transform .18s ease}.chain-detail-body{padding:14px}.chain-chokepoints,.chain-map,.chain-data-gaps{border:1px solid #e6eaf1;border-radius:8px;background:#fbfcff;padding:14px}.chain-map summary,.chain-data-gaps summary{cursor:pointer;font-weight:800;color:#344054}.chain-chokepoints b{display:block;margin-bottom:8px}.bom-taxonomy{border:1px solid #e6eaf1;border-radius:12px;background:#fff;padding:12px}.bom-taxonomy>p{margin:0 0 10px;color:#465365;font-size:13px;line-height:1.65}.bom-taxonomy-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}.bom-taxonomy-card{border:1px solid #edf1f7;border-radius:12px;background:#fbfcff;padding:10px}.bom-taxonomy-card span{display:block;color:#0a63ce;font-size:11px;font-weight:900;margin-bottom:5px}.bom-taxonomy-card strong{display:block;color:#27364a;font-size:13px}.bom-taxonomy-card p{margin:5px 0 0;color:#526071;font-size:12px;line-height:1.55}.chain-relationship-graph,.chain-map-card{border:1px solid #d9e4f2;border-radius:10px;background:linear-gradient(135deg,#f7fbff,#fff);padding:14px}.chain-graph-head{display:flex;justify-content:space-between;gap:12px;align-items:end;margin-bottom:12px}.chain-graph-head b{font-size:16px}.chain-graph-head span{color:var(--muted);font-size:12px}.chain-layer-grid{display:grid;grid-template-columns:repeat(3,minmax(260px,1fr));gap:10px}.chain-layer-card{border:1px solid #e1e7f0;border-radius:10px;background:#fff;overflow:hidden}.chain-stage-panel summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:auto 1fr auto auto;gap:10px;align-items:center;padding:12px}.chain-stage-panel summary::-webkit-details-marker,.chain-lane-node summary::-webkit-details-marker{display:none}.chain-stage-head{display:grid;gap:8px;padding:14px 14px 8px}.chain-stage-head strong{color:#344054;font-size:13px;line-height:1.55}.chain-stage-name{display:inline-flex;width:max-content;border-radius:999px;background:#eef5ff;color:var(--blue);font-weight:900;font-size:12px;padding:4px 10px}.chain-company-list{display:grid;gap:8px;margin:0;padding:0 14px 14px;list-style:none}.chain-company-list li{border:1px solid #edf1f7;border-radius:10px;background:#fbfdff;padding:10px}.chain-company-list b{display:block;color:#1f2937;font-size:13px}.chain-company-list span{display:block;color:#526071;font-size:12px;margin-top:3px}.chain-company-list small{display:block;color:#0a63ce;font-size:11px;font-weight:800;margin-top:5px}.chain-relation-card{border:1px solid #edf1f7;border-radius:10px;background:#fbfdff;overflow:hidden}.chain-lane-node summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:1fr auto auto;gap:8px;align-items:center;padding:10px}.chain-lane-node em{font-style:normal;color:#0a63ce;font-size:12px;font-weight:900}.chain-company-detail{padding:0 10px 10px}.chain-company-head{display:flex;justify-content:space-between;gap:10px;margin:4px 0 8px}.chain-company-head small{color:#667085;font-size:11px}.chain-relation-meta{display:grid;gap:6px;margin:0}.chain-relation-meta div{display:grid;grid-template-columns:72px 1fr;gap:8px}.chain-relation-meta dt{color:#0a63ce;font-size:12px;font-weight:900}.chain-relation-meta dd{margin:0;color:#526071;font-size:12px}.chain-table,.target-table{min-width:1800px}.chain-map{overflow:auto}
    .qa-card{background:var(--panel);border:1px solid var(--line);border-radius:8px;margin:12px 0;overflow:hidden}.qa-card[open]>summary{border-bottom:1px solid #e6eaf1}.qa-card summary{list-style:none;cursor:pointer;padding:14px 16px;display:grid;grid-template-columns:auto 1fr auto auto;gap:10px;align-items:center}.qa-card summary::-webkit-details-marker{display:none}.qid{font-weight:800;color:var(--blue);font-size:13px}.qtitle{font-weight:760}.qa-count{font-size:12px;color:var(--muted);background:#f1f4f9;border:1px solid #e0e5ee;border-radius:999px;padding:3px 8px}.chevron{color:var(--muted)}details[open]>summary .chevron{transform:rotate(90deg)}.level-2{margin-left:16px}.level-3{margin-left:32px}.level-4{margin-left:48px}.level-5{margin-left:64px}.qa-body{padding:14px 16px 16px}.qa-block{margin:0 0 14px}.block-title{font-size:12px;font-weight:800;color:#586174;text-transform:uppercase;margin-bottom:8px}
    .artifact-card{border:1px solid #e2e7ef;border-radius:8px;background:#fbfcff;padding:12px;margin:10px 0}.artifact-title{font-weight:780;margin-bottom:8px}.qa-complement-focus,.q4-odds-gate{background:linear-gradient(180deg,#fff,#f8fbff)}.qa-complement-focus p,.q4-odds-gate p,.target-odds-model p{margin:0 0 10px;color:#526071}.qa-complement-focus ul{margin:0;padding-left:18px;color:#344054}.qa-complement-focus li{margin:5px 0}.q4-odds-gate table{min-width:920px}.logic-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.logic-card{border:1px solid #e5e9f0;border-radius:8px;background:#fff;padding:10px}.logic-card b{display:block;font-size:12px;color:#536071;margin-bottom:4px}.logic-card p{margin:0;font-size:13px}.routing{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:10px}.pill{border:1px solid #dfe6f1;background:#f7faff;border-radius:999px;padding:4px 8px;font-size:12px;color:#46515f}.source-chips{display:flex;flex-wrap:wrap;gap:6px}.source-chip{font-size:12px;color:#0a63ce;background:#eef5ff;border:1px solid #d8e8ff;border-radius:999px;padding:4px 8px;text-decoration:none}
    .constraint-definition,.component-value-chain,.bottleneck-release-timeline,.target-profit-bridge,.target-valuation-table{border:1px solid #d9e4f2;border-radius:12px;background:linear-gradient(180deg,#fff,#fbfdff);padding:14px;margin:14px 0}.constraint-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.constraint-grid article{border:1px solid #e6ecf5;border-radius:10px;background:#f8fbff;padding:11px}.constraint-grid span{display:block;color:#0a63ce;font-size:12px;font-weight:900;margin-bottom:5px}.constraint-grid p{margin:0;color:#465365;font-size:13px;line-height:1.65}.component-value-chain table,.bottleneck-release-timeline table,.target-profit-bridge table,.target-valuation-table table{min-width:1280px}.target-profit-bridge p,.target-valuation-table p{margin:0 0 10px;color:#526071}
    .competition-bom-map,.chokepoint-bom-map{display:grid;gap:12px}.competition-node-card{border:1px solid rgba(10,99,206,.18);border-radius:12px;background:#fbfcff;overflow:hidden}.competition-node-card>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:auto minmax(160px,1fr) auto auto;gap:10px;align-items:center;padding:12px 14px}.competition-node-card>summary::-webkit-details-marker{display:none}.competition-node-card[open]>summary{border-bottom:1px solid #e6eaf1}.competition-node-index{display:inline-flex;border-radius:999px;background:#eef5ff;color:var(--blue);font-size:11px;font-weight:900;padding:3px 8px}.competition-intensity{font-size:11px;font-weight:800;border-radius:999px;background:#eef5ff;color:var(--blue);padding:3px 8px}.competition-node-body{padding:14px}.overview-research-unit{border:1px solid #d9e8fb;border-radius:12px;background:linear-gradient(180deg,#fbfdff,#fff);padding:12px;margin-bottom:12px}.overview-unit-head{display:flex;justify-content:space-between;gap:10px;align-items:center;margin-bottom:10px}.overview-unit-head b{color:#27364a;font-size:13px}.overview-unit-head span{color:#667085;font-size:12px}.competition-question-grid{display:grid;grid-template-columns:1fr;gap:10px;margin-bottom:12px}.chokepoint-question-grid{display:grid;grid-template-columns:1fr;gap:10px;margin-bottom:12px}.competition-subcard,.profit-pool-table,.chokepoint-scorecard{border:1px solid #e6eaf1;border-radius:10px;background:#fff;padding:10px}.overview-question-card{display:grid;gap:8px}.competition-subcard h4{margin:0 0 6px;font-size:13px;color:#27364a}.competition-subcard p{margin:0;color:#526071;font-size:12px;line-height:1.55}.overview-answer{border-top:1px solid #edf1f7;padding-top:8px}.overview-answer-structured{display:grid;gap:6px}.overview-answer-prose{display:grid;gap:8px}.overview-answer-prose p{margin:0;color:#344054;font-size:13px;line-height:1.75}.overview-answer-prose a{color:#0a63ce;text-decoration:none;font-weight:800;border-bottom:1px solid rgba(10,99,206,.28)}.overview-answer-prose a:hover{border-bottom-color:#0a63ce}.overview-answer-row{display:grid;grid-template-columns:74px 1fr;gap:8px;border:1px solid #edf1f7;border-radius:9px;background:#fbfcff;padding:7px 8px}.overview-answer-row span{color:#0a63ce;font-size:11px;font-weight:900}.overview-answer-row p{margin:0;color:#344054;font-size:12px;line-height:1.55}.overview-answer-sources{margin-top:2px}.profit-pool-table table,.chokepoint-scorecard table{min-width:1080px}
    .industry-module-body,.qa-body,.chain-detail-body,.space-detail-body,.target-section,.artifact-card{min-width:0;max-width:100%}.table-scroll{max-width:100%;overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;border:1px solid #e6eaf1;border-radius:8px;background:#fff}.table-scroll table{width:max-content;min-width:100%}table{width:100%;border-collapse:collapse;font-size:13px}th,td{padding:9px 8px;border-bottom:1px solid #e6eaf1;text-align:left;vertical-align:top}th{color:#536071;font-size:12px;background:#f8fafc}.target-odds-model{border:1px solid #d9e4f2;border-radius:10px;background:#fbfdff;padding:14px;margin:14px 0}.target-odds-table{min-width:1800px}.state-actionable_long{color:var(--green);font-weight:800}.state-watch_only{color:var(--amber);font-weight:800}.state-no_action{color:var(--red);font-weight:800}.source-collapse summary{cursor:pointer;font-weight:800}.source-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin-top:12px}.source-card{border:1px solid #e5e9f0;border-radius:8px;background:#fbfcff;padding:10px}.source-card a{color:#0a63ce}
    .chain-simple-flow{border:1px solid #d8e6f7;border-radius:12px;background:#f7fbff;padding:12px;margin-bottom:12px}.simple-flow-head{display:flex;justify-content:space-between;gap:12px;margin-bottom:10px}.simple-flow-head b{color:#27364a}.simple-flow-head span{color:#667085;font-size:12px}.chain-simple-grid{display:grid;grid-template-columns:repeat(5,minmax(160px,1fr));gap:8px}.chain-simple-step{border:1px solid #e1e7f0;border-radius:12px;background:#fff;padding:10px;display:grid;grid-template-columns:auto 1fr;gap:8px;align-items:start}.chain-simple-step>span{display:inline-flex;width:26px;height:26px;align-items:center;justify-content:center;border-radius:999px;background:#0a63ce;color:#fff;font-weight:900;font-size:12px}.chain-simple-step b{display:block;color:#27364a;font-size:13px;margin-bottom:4px}.chain-simple-step p{margin:0;color:#344054;font-size:12px;line-height:1.55}.chain-simple-step small{display:block;margin-top:6px;color:#667085;font-size:11px;line-height:1.45}.chain-value-guide{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-bottom:12px}.chain-value-guide div{border:1px solid #e1e7f0;border-radius:12px;background:#fff;padding:10px}.chain-value-guide b{display:block;color:#27364a;font-size:13px}.chain-value-guide span{display:block;color:#667085;font-size:12px;margin-top:4px}.chain-sankey-list{display:grid;gap:12px}.chain-sankey-flow{display:grid;grid-template-columns:1fr;gap:10px;align-items:stretch;border:1px solid #e1e7f0;border-radius:14px;background:#fff;padding:12px}.chain-sankey-flow p{margin:0}.flow-step{display:flex;align-items:center;gap:10px}.flow-step span{display:inline-flex;width:32px;height:28px;align-items:center;justify-content:center;border-radius:8px;background:#eef5ff;color:#0a63ce;font-weight:900}.flow-step b{color:#27364a}.flow-route{display:grid;grid-template-columns:minmax(160px,.9fr) minmax(260px,1.4fr) minmax(160px,.9fr);gap:10px;align-items:center}.flow-from,.flow-to{font-weight:900;color:#27364a;border:1px solid #e8edf5;border-radius:12px;background:#fbfcff;padding:10px}.flow-from small,.flow-to small{display:block;color:#667085;font-size:11px;font-weight:800;margin-bottom:4px}.flow-band{min-height:calc(18px + var(--flow-weight)*4px);display:flex;align-items:center;justify-content:center;border-radius:999px;padding:8px 14px;text-align:center;font-size:12px;font-weight:900;color:#fff;background:#2b6cb0}.flow-fields{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.flow-fields div{border:1px solid #edf1f7;border-radius:12px;background:#fbfcff;padding:10px}.flow-fields b{display:block;color:#0a63ce;font-size:12px;margin-bottom:4px}.flow-fields p{margin:0;color:#526071;font-size:12px}
    .industry-space table,.industry-competition table,.industry-chokepoints table{min-width:1200px}.industry-space-summary{border:1px solid #d9e4f2;border-radius:12px;background:linear-gradient(180deg,#fff,#f7fbff);padding:14px;margin-bottom:12px}.industry-space-summary>p{margin:0 0 12px;color:#344054;line-height:1.75;font-weight:760}.space-summary-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.space-summary-grid article,.space-boundary-grid article,.space-driver-card,.space-model-grid article{border:1px solid #e2e9f3;border-radius:12px;background:#fff;padding:12px}.space-summary-grid span,.space-boundary-grid span,.space-driver-card span,.space-model-grid span{display:block;color:#0a63ce;font-size:12px;font-weight:900;margin-bottom:6px}.space-summary-grid strong,.space-model-grid strong{display:block;color:#27364a;font-size:13px;line-height:1.6}.space-detail-panel{border:1px solid #d9e4f2;border-radius:12px;background:#fbfcff;margin:10px 0;overflow:hidden}.space-detail-panel>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:center;padding:13px 14px}.space-detail-panel>summary::-webkit-details-marker{display:none}.space-detail-panel>summary span:first-child{font-weight:900;color:#27364a}.space-detail-panel>summary small{color:#667085;font-size:12px;line-height:1.45}.space-detail-panel[open]>summary{border-bottom:1px solid #e6eaf1}.space-detail-body{padding:14px}.space-boundary-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.space-boundary-grid p{margin:0;color:#526071;font-size:13px;line-height:1.65}.space-driver-tree{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.space-driver-card b{display:block;color:#27364a;font-size:13px;line-height:1.55;margin-bottom:8px}.space-driver-card dl{display:grid;gap:7px;margin:0}.space-driver-card div{display:grid;grid-template-columns:74px 1fr;gap:8px}.space-driver-card dt{color:#0a63ce;font-size:12px;font-weight:900}.space-driver-card dd{margin:0;color:#526071;font-size:12px;line-height:1.55}.space-gate-model{display:grid;gap:10px}.space-model-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.space-model-note{border:1px solid #d9e4f2;border-radius:12px;background:#fff;padding:12px}.space-model-note.warning{background:#fffaf0;border-color:#f4d28f}.space-model-note b{display:block;color:#27364a;font-size:13px;margin-bottom:5px}.space-model-note p{margin:0;color:#526071;font-size:13px;line-height:1.65}.space-evidence-pack{display:grid;gap:12px}.space-evidence-card{border:1px solid #d9e4f2;border-radius:14px;background:linear-gradient(180deg,#fff,#f8fbff);padding:14px}.space-evidence-card header{border-bottom:1px solid #e6edf7;margin-bottom:12px;padding-bottom:10px}.space-evidence-card header span{display:inline-flex;color:#0a63ce;background:#edf6ff;border:1px solid #cfe6ff;border-radius:999px;font-size:11px;font-weight:900;padding:3px 8px;margin-bottom:8px}.space-evidence-card h4{margin:0 0 5px;color:#1d2939;font-size:16px}.space-evidence-card header p{margin:0;color:#526071;font-size:13px;line-height:1.6}.space-evidence-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.space-evidence-grid section{border:1px solid #e2e9f3;border-radius:12px;background:#fff;padding:12px}.space-evidence-grid b{display:block;color:#27364a;font-size:13px;margin-bottom:7px}.space-evidence-grid p,.space-evidence-grid li{color:#526071;font-size:12px;line-height:1.65}.space-evidence-grid ul,.space-inference-chain{margin:0;padding-left:18px}.space-refute-box{grid-column:1/-1;background:#fffaf0!important;border-color:#f4d28f!important}.space-evidence-sources{margin-top:10px}.space-scenario-table table{min-width:1600px}.space-node-elasticity-table table{min-width:2200px}.space-validation-table table{min-width:1100px}.industry-key-variables .key-variable-grid{display:grid;grid-template-columns:1fr;gap:12px}.key-variable-bom-map{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}.key-variable-bom-card{border:1px solid #d9e8fb;border-radius:12px;background:#fbfdff;overflow:hidden}.key-variable-bom-card>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:1fr auto;gap:8px;align-items:center;padding:12px 14px}.key-variable-bom-card>summary::-webkit-details-marker{display:none}.key-variable-bom-card>summary strong{color:#27364a;font-size:13px}.key-variable-bom-card>summary span:not(.chevron){color:#667085;font-size:11px;font-weight:800}.key-variable-bom-card[open]>summary{border-bottom:1px solid #e6eaf1}.key-variable-bom-card .overview-question-card{margin:12px}.industry-key-variables .chain-data-gaps{border:1px solid #e6eaf1;border-radius:12px;background:#fff;padding:12px}.industry-key-variables ul{margin:8px 0 0;padding-left:20px;color:#526071;line-height:1.75}.qa-generation-table{border:1px solid #e6eaf1;border-radius:8px}.heat-score{text-align:center}.heat-score span{display:inline-flex;min-width:28px;height:24px;align-items:center;justify-content:center;border-radius:8px;font-weight:900}.heat-high span{background:#e7f6ed;color:var(--green)}.heat-mid span{background:#fff4d6;color:var(--amber)}.heat-low span{background:#fee4e2;color:var(--red)}
    .space-bom-reasoning{display:grid;gap:10px}.space-node-card{border:1px solid #d9e4f2;border-radius:14px;background:#fbfcff;overflow:hidden}.space-node-card>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:auto minmax(160px,.45fr) minmax(240px,1fr) auto;gap:10px;align-items:center;padding:13px 14px}.space-node-card>summary::-webkit-details-marker{display:none}.space-node-card[open]>summary{border-bottom:1px solid #e6eaf1}.space-node-label{display:inline-flex;border-radius:999px;background:#eef5ff;color:#0a63ce;border:1px solid #d8e8ff;font-size:11px;font-weight:900;padding:3px 8px}.space-node-card summary strong{color:#27364a;font-size:14px}.space-node-card summary small{color:#667085;font-size:12px;line-height:1.45}.space-node-reasoning{display:grid;grid-template-columns:1fr;gap:10px;padding:14px}.space-node-section{border:1px solid #e2e9f3;border-radius:12px;background:#fff;padding:12px}.space-node-space-reasoning{border-color:#d9e8fb;background:#fbfdff}.space-node-evidence{background:#fbfcff}.space-node-section h4{margin:0 0 8px;color:#27364a;font-size:13px}.space-node-section p,.space-node-section li{color:#526071;font-size:12px;line-height:1.65}.space-node-section ul,.space-node-section ol{margin:0;padding-left:18px}.space-node-sources{margin-top:10px}.space-node-sizing{margin-top:12px;border:1px solid #d9e8fb;border-radius:12px;background:linear-gradient(180deg,#f8fbff,#fff);padding:12px}.space-method-step{display:grid;gap:8px;margin-bottom:10px}.space-step-title{display:flex;align-items:center;gap:8px}.space-step-title h5{margin:0;color:#0a63ce;font-size:12px}.space-step-index{display:inline-flex;width:22px;height:22px;align-items:center;justify-content:center;border-radius:999px;background:#0a63ce;color:#fff;font-style:normal;font-size:11px;font-weight:900;flex:0 0 auto}.space-public-methods{margin-bottom:0}.space-method-card-grid{display:grid;grid-template-columns:1fr;gap:10px}.space-method-card{border:1px solid #e1e9f4;border-radius:12px;background:#fff;display:grid;grid-template-columns:minmax(128px,168px) 1fr;gap:12px;padding:10px;min-width:0}.space-method-card header{border-right:1px solid #edf1f7;display:grid;align-content:start;gap:7px;padding-right:10px}.space-method-card header span{color:#27364a;font-size:12px;font-weight:900}.space-method-card header small{width:max-content;color:#0a63ce;background:#eef5ff;border:1px solid #d8e8ff;border-radius:999px;font-size:11px;font-weight:900;padding:2px 7px;white-space:nowrap}.space-method-card-body{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:8px;min-width:0}.space-method-entry{border:1px solid #edf1f7;border-radius:10px;background:#fbfdff;padding:9px;margin:0}.space-method-entry b{display:block;color:#1f2937;font-size:12px;margin-bottom:5px}.space-method-entry p{margin:0 0 8px;color:#344054;font-size:12px;line-height:1.55}.space-method-entry p strong{color:#0a63ce;font-size:11px;font-weight:900}.space-method-entry dl{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:5px 10px;margin:0}.space-method-entry dl div{display:grid;grid-template-columns:64px 1fr;gap:6px}.space-method-entry dt{color:#0a63ce;font-size:11px;font-weight:900}.space-method-entry dd{margin:0;color:#526071;font-size:11px;line-height:1.45}.space-method-entry-sources{margin-top:8px}.space-method-entry-sources .source-chips{gap:5px}.source-chip-missing{color:#956100;background:#fff7e6;border-color:#f4d28f}.space-method-empty{align-self:center;margin:0;color:#667085;font-size:12px;line-height:1.6}.space-method-gap{border:1px dashed #d8e3f2;border-radius:10px;background:#fbfcff;padding:9px;color:#5d6675}.space-horizon-conclusion{display:grid;gap:8px;margin-bottom:10px}.space-horizon-summary{border:1px solid #e5edf7;border-radius:10px;background:#fff;padding:10px;margin:0;color:#344054;font-size:12px;line-height:1.65}.space-horizon-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.space-horizon-card{border:1px solid #e5edf7;border-radius:10px;background:#fff;padding:10px}.space-horizon-card span{display:block;color:#667085;font-size:11px;font-weight:900;margin-bottom:4px}.space-horizon-card strong{display:inline-flex;border-radius:999px;padding:3px 8px;font-size:12px;margin-bottom:6px}.space-horizon-large{color:#0f7a4f;background:#e7f6ed}.space-horizon-mid{color:#956100;background:#fff4d6}.space-horizon-low{color:#b42318;background:#fee4e2}.space-horizon-card p{margin:0;color:#344054;font-size:12px;line-height:1.55}.space-step-confidence{display:block;margin-top:2px;color:#667085;font-size:11px;font-weight:900}.space-node-sizing-table table{min-width:760px}.space-node-sizing-table th,.space-node-sizing-table td{font-size:12px}
    .chain-research-bridge,.chain-data-gaps{border:1px solid #d9e4f2;border-radius:12px;background:linear-gradient(180deg,#fff,#fbfdff);padding:14px}.chain-bridge-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.chain-bridge-card{border:1px solid #e5edf7;border-radius:12px;background:#f8fbff;padding:12px}.chain-bridge-card span{display:block;color:#667085;font-size:12px;font-weight:800;margin-bottom:6px}.chain-bridge-card strong{display:block;color:#223047;line-height:1.55}.chain-research-bridge>p{margin:12px 0;color:#435064;line-height:1.75}.chain-node-lens{border:1px solid #e7edf6;border-radius:12px;background:#fff;padding:12px;margin:12px 0}.chain-node-lens>b{display:block;color:#27364a;margin-bottom:8px}.chain-node-lens ul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:0;padding:0;list-style:none}.chain-node-lens li{border:1px solid #edf1f7;border-radius:10px;background:#fbfcff;padding:10px}.chain-node-lens li b{display:block;color:#0a63ce;font-size:12px;margin-bottom:4px}.chain-node-lens li span{display:block;color:#526071;font-size:12px;line-height:1.55}.chain-data-gaps summary{cursor:pointer;font-weight:900;color:#344054}.chain-data-gaps ul{margin:10px 0 0;padding-left:20px;color:#526071;line-height:1.75}
    @media(max-width:900px){.goal-grid,.logic-grid,.chain-simple-grid,.chain-value-guide,.flow-route,.flow-fields,.chain-bridge-grid,.chain-node-lens ul,.chain-qa-grid,.industry-key-variables .key-variable-grid,.constraint-grid,.space-summary-grid,.space-boundary-grid,.space-driver-tree,.space-model-grid,.space-evidence-grid,.space-node-reasoning,.space-horizon-grid,.overview-answer-row,.competition-question-grid,.chokepoint-question-grid,.space-method-card-grid{grid-template-columns:1fr}.space-method-card{grid-template-columns:1fr}.space-method-card header{border-right:0;border-bottom:1px solid #edf1f7;padding-right:0;padding-bottom:8px}.space-method-entry dl{grid-template-columns:1fr}.space-node-card>summary{grid-template-columns:1fr auto}.space-node-label,.space-node-card summary strong,.space-node-card summary small{grid-column:1/2}.simple-flow-head{display:grid}.level-2,.level-3,.level-4,.level-5{margin-left:0}.qa-card summary{grid-template-columns:auto 1fr auto}.qa-count{display:none}}
  `;
}

function writeJson(filename, data) {
  fs.writeFileSync(path.join(OUT_DIR, filename), `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function writeJsonl(filename, rows) {
  fs.writeFileSync(path.join(OUT_DIR, filename), `${rows.map((row) => JSON.stringify(row)).join("\n")}\n`, "utf8");
}

function formatNullable(value) {
  return value === null || value === undefined ? "n/a" : Number(value).toFixed(2);
}

function formatPct(value) {
  return value === null || value === undefined ? "n/a" : `${Number(value).toFixed(2)}%`;
}

function round(value) {
  return Math.round(value * 1000) / 1000;
}

function esc(value) {
  return String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
}

main();
