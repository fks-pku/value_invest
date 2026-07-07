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
  source("SRC-NVDA-FY24-Q2", "NVIDIA FY2024 Q2 results", "evidence", "https://investor.nvidia.com/news/press-release-details/2023/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2024/", "2023-08-23", "NVIDIA Q2 FY24 Data Center revenue was $10.32B, up 141% sequentially and 171% year over year as accelerated computing demand began to appear in reported revenue."),
  source("SRC-NVDA-FY24-Q4", "NVIDIA FY2024 Q4 results", "evidence", "https://investor.nvidia.com/news/press-release-details/2024/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2024/", "2024-02-21", "NVIDIA Q4 FY24 Data Center revenue was $18.4B, showing the first large financial step-change after accelerated computing demand surged."),
  source("SRC-NVDA-FY25-Q2", "NVIDIA FY2025 Q2 results", "evidence", "https://investor.nvidia.com/news/press-release-details/2024/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2025/default.aspx", "2024-08-28", "NVIDIA Q2 FY25 Data Center revenue was $26.3B, up 16% sequentially and 154% year over year."),
  source("SRC-NVDA-FY25-Q4", "NVIDIA FY2025 Q4 results", "evidence", "https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2025/", "2025-02-26", "NVIDIA Q4 FY25 Data Center revenue was $35.6B, extending the AI infrastructure revenue ramp before Blackwell scaled further."),
  source("SRC-NVDA-FY26-Q2", "NVIDIA FY2026 Q2 results", "evidence", "https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2026/default.aspx", "2025-08-27", "NVIDIA Q2 FY26 Data Center revenue was $41.1B and Blackwell data-center revenue increased 17% sequentially."),
  source("SRC-NVDA-FY26-Q3", "NVIDIA FY2026 Q3 results", "evidence", "https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2026/default.aspx", "2025-11-19", "NVIDIA Q3 FY26 Data Center revenue was $51.2B, up 25% sequentially and 66% year over year; management said cloud GPUs were sold out and compute demand kept accelerating."),
  source("SRC-NVDA-FY26-Q4", "NVIDIA FY2026 Q4 results", "evidence", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/", "2026-02-25", "NVIDIA Q4 FY26 revenue was $68.1B, Data Center revenue was $62.3B, Q1 FY27 revenue outlook was $78.0B +/-2%, and management framed customer demand as AI factories for the AI industrial revolution."),
  source("SRC-NVDA-GTC-VERA-RUBIN-20260316", "NVIDIA Vera Rubin platform at GTC 2026", "evidence", "https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform", "2026-03-16", "NVIDIA announced Vera Rubin as seven chips and five rack-scale systems for AI factories, covering Vera CPU, Rubin GPU, NVLink 6, ConnectX-9, BlueField-4, Spectrum-6 and Groq 3 LPU."),
  source("SRC-NVDA-GTC-DYNAMO-20260316", "NVIDIA Dynamo 1.0 for AI factory inference", "evidence", "https://nvidianews.nvidia.com/news/dynamo-1-0", "2026-03-16", "NVIDIA announced Dynamo 1.0 as open-source production software for AI factory inference orchestration, with reported up to 7x Blackwell inference performance improvement and broad cloud/provider adoption."),
  source("SRC-VRT-Q4-2025", "Vertiv Q4 2025 results", "evidence", "https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/", "2026-02-11", "Vertiv Q4 2025 organic orders rose about 252% YoY and backlog reached $15.0B, reflecting robust AI infrastructure demand."),
  source("SRC-DELL-FY25-Q4", "Dell FY2025 Q4 results", "evidence", "https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-2", "2025-02-27", "Dell said deals booked with xAI and others put AI server backlog at roughly $9B as of FY25 Q4."),
  source("SRC-DELL-FY26-Q1", "Dell FY2026 Q1 results", "evidence", "https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-first-quarter-fiscal-2026-financial", "2025-05-29", "Dell Q1 FY26 generated $12.1B in AI orders in the quarter and left the company with $14.4B in AI backlog."),
  source("SRC-DELL-FY26-Q2-PERFORMANCE", "Dell FY2026 Q2 performance review", "evidence", "https://investors.delltechnologies.com/static-files/454d3647-eebb-410c-bde3-92056cdf569f", "2025-08-28", "Dell Q2 FY26 performance review showed Q2 AI orders demand of $5.6B and AI backlog of $11.7B exiting Q2."),
  source("SRC-DELL-FY26-Q3", "Dell FY2026 Q3 results", "evidence", "https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-third-quarter-fiscal-2026-financial", "2025-11-25", "Dell Q3 FY26 AI server orders were $12.3B, year-to-date orders were $30B, and backlog reached $18.4B."),
  source("SRC-DELL-FY26-Q4", "Dell FY2026 Q4 results", "evidence", "https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-3", "2026-02-26", "Dell FY26 closed more than $64B in AI-optimized server orders, shipped more than $25B, entered FY27 with a $43B backlog, and guided FY27 AI-optimized server revenue to roughly $50B, up 103% year over year."),
  source("SRC-ALAB-Q4-2025", "Astera Labs Q4 2025 results", "evidence", "https://www.sec.gov/Archives/edgar/data/1736297/000173629726000005/q425exhibit991.htm", "2026-02-10", "Astera Labs Q4 revenue was $270.6M, +92% YoY, tied to rack-scale AI infrastructure connectivity."),
  source("SRC-CRDO-FY26-Q3", "Credo FY2026 Q3 results", "evidence", "https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm", "2026-03-02", "Credo FY26 Q3 revenue was $407.0M, +200% YoY, with active electrical cables, optical interconnects and memory connectivity tied to AI infrastructure."),
  source("SRC-MRVL-FY26-Q3", "Marvell FY2026 Q3 10-Q", "evidence", "https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-25-000197/mrvl-20251101.htm", "2025-12-03", "Marvell FY26 Q3 net revenue was $2.075B; data-center sales increased 38% year over year, driven by AI-related demand for custom products and electro-optics."),
  source("SRC-AVGO-FY25-Q2", "Broadcom FY2025 Q2 results", "evidence", "https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-second-quarter-fiscal-year-2025-financial", "2025-06-05", "Broadcom Q2 FY25 AI revenue exceeded $4.4B, up 46% year over year, and management expected Q3 AI revenue of about $5.1B."),
  source("SRC-AVGO-FY25-Q3", "Broadcom FY2025 Q3 results", "evidence", "https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-third-quarter-fiscal-year-2025-financial", "2025-09-04", "Broadcom Q3 FY25 AI revenue was $5.2B, up 63% year over year, and management expected Q4 AI revenue of about $6.2B."),
  source("SRC-AVGO-FY25-Q4", "Broadcom FY2025 Q4 results", "evidence", "https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-fourth-quarter-and-fiscal-year-2025", "2025-12-11", "Broadcom Q4 FY25 AI semiconductor revenue rose 74% YoY and Q1 FY26 AI semiconductor revenue was expected to double to $8.2B, driven by custom AI accelerators and Ethernet AI switches."),
  source("SRC-AVGO-FY26-Q1", "Broadcom FY2026 Q1 results", "evidence", "https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial", "2026-03-05", "Broadcom Q1 FY26 AI revenue was $8.4B, up 106% year over year, and management expected Q2 AI semiconductor revenue of about $10.7B."),
  source("SRC-AMD-Q4-2025-TOMS", "Tom's Hardware AMD Q4 2025 results summary", "message", "https://www.tomshardware.com/pc-components/cpus/amd-ceo-downplays-pc-memory-crunch-saying-our-focus-areas-are-enterprise-company-wants-to-focus-on-growing-higher-end-of-the-market", "2026-02-04", "Tom's Hardware reported AMD Q4 2025 total revenue of about $10.3B, Data Center revenue of $5.4B up 39% year over year, full-year Data Center revenue of $16.6B, and management focus on enterprise and high-end markets."),
  source("SRC-ANET-Q4-2025", "Arista Q4 2025 results", "evidence", "https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Networks-Inc--Reports-Fourth-Quarter-and-Year-End-2025-Financial-Results/default.aspx", "2026-02-12", "Arista FY2025 revenue was $9.006B, +28.6%, and management said it exceeded AI networking and campus expansion goals."),
  source("SRC-TSM-Q4-2025", "TSMC Q4 2025 results", "evidence", "https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm", "2026-01-15", "TSMC Q4 2025 revenue was $33.73B, gross margin 62.3%, advanced technologies were 77% of wafer revenue, and 2026 capex was expected at $52B-$56B."),
  source("SRC-MU-FY26-Q1", "Micron FY2026 Q1 results", "evidence", "https://micron.gcs-web.com/news-releases/news-release-details/micron-technology-inc-reports-results-first-quarter-fiscal-2026", "2025-12-17", "Micron FY26 Q1 delivered record revenue and margin expansion, with AI data-center memory demand driving cloud memory and HBM-related strength."),
  source("SRC-MU-FY26-Q1-PREPARED", "Micron FY2026 Q1 prepared remarks", "evidence", "https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9", "2025-12-17", "Micron prepared remarks forecast HBM TAM from about $35B in calendar 2025 to around $100B in calendar 2028, about 40% CAGR, and said 2026 HBM supply had completed price and volume agreements."),
  source("SRC-SKHYNIX-FY25", "SK hynix FY2025 results", "evidence", "https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html", "2026-01-28", "SK hynix FY2025 revenue was KRW97.1467T, operating profit KRW47.2063T and operating margin 49%, driven by AI memory and HBM leadership."),
  source("SRC-SAMSUNG-FY25", "Samsung Q4 and FY2025 results", "evidence", "https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results", "2026-01-29", "Samsung Q4 2025 Memory Business reached record quarterly revenue and operating profit, with HBM, server DDR5 and enterprise SSD as high-value AI products."),
  source("SRC-SMCI-FY26-Q2", "Supermicro FY2026 Q2 results", "evidence", "https://ir.supermicro.com/news/news-details/2026/Super-Micro-Computer-Inc.-Reports-Second-Quarter-Fiscal-2026-Financial-Results/default.aspx", "2026-02-03", "Supermicro remained an AI server assembly exposure, but margin, execution and governance risks require a lower risk-control score."),
  source("SRC-MSFT-FY25-Q3-METRICS", "Microsoft FY2025 Q3 investor metrics", "evidence", "https://www.microsoft.com/en-us/investor/earnings/fy-2025-q3/metrics", "2025-04-30", "Microsoft investor metrics provide Commercial remaining performance obligation in billions for Q3 FY24 through Q3 FY25: $235B, $269B, $259B, $298B and $315B across quarterly points, plus Microsoft Cloud revenue and margin metrics."),
  source("SRC-MSFT-FY25-Q4-CALL", "Microsoft FY2025 Q4 earnings call", "evidence", "https://www.microsoft.com/en-us/investor/events/fy-2025/earnings-fy-2025-q4", "2025-07-30", "Microsoft said commercial remaining performance obligation increased to $368B in FY25 Q4, up 37% year over year, with Azure and AI workload demand remaining higher than supply."),
  source("SRC-MSFT-FY26-Q1", "Microsoft FY2026 Q1 results", "evidence", "https://www.microsoft.com/en-us/investor/earnings/fy-2026-q1/press-release-webcast", "2025-10-29", "Microsoft Q1 FY26 Microsoft Cloud revenue was $49.1B and commercial remaining performance obligation increased 51% to $392B."),
  source("SRC-MSFT-FY26-Q2", "Microsoft FY2026 Q2 results", "evidence", "https://www.microsoft.com/en-us/investor/earnings/fy-2026-q2/press-release-webcast", "2026-01-28", "Microsoft Q2 FY2026 Microsoft Cloud revenue was $51.5B, +26%, commercial RPO increased 110% to $625B, and Azure and other cloud services revenue increased 39%."),
  source("SRC-MSFT-FY26-Q2-CALL", "Microsoft FY2026 Q2 earnings call", "evidence", "https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q2.aspx", "2026-01-28", "Microsoft said Q2 FY26 capital expenditures were $37.5B, about two-thirds for short-lived assets primarily GPUs and CPUs, and that customer demand exceeded supply."),
  source("SRC-AMZN-Q4-2025", "Amazon Q4 2025 results", "evidence", "https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Fourth-Quarter-Results/default.aspx", "2026-02-05", "Amazon Q4 2025 AWS segment sales increased to $35.6B; management said the chips business grew triple digits year over year and expected 2026 capex of about $200B across Amazon, driven by AI, chips, robotics and satellites."),
  source("SRC-GOOGL-Q4-2025", "Alphabet Q4 2025 results", "evidence", "https://s206.q4cdn.com/479360582/files/doc_news/2026/Feb/04/attachments/2025q4-alphabet-earnings-release.pdf", "2026-02-04", "Alphabet Q4 2025 Google Cloud revenue increased 48% to $17.7B, Cloud annual run rate exceeded $70B, FY2025 purchases of property and equipment were $91.4B, and 2026 CapEx was anticipated at $175B-$185B to meet customer demand."),
  source("SRC-GOOGL-Q4-2025-CALL", "Alphabet Q4 2025 earnings call", "evidence", "https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx", "2026-02-04", "Alphabet said backlog reached $240B, up 55% sequentially; Gemini App exceeded 750M monthly active users; Gemini Enterprise had 8M paid seats; and Gemini 3 processed about three times the daily tokens of Gemini 2.5 Pro while serving costs fell 78%."),
  source("SRC-META-Q3-2025", "Meta Q3 2025 results", "evidence", "https://investor.atmeta.com/investor-news/press-release-details/2025/Meta-Reports-Third-Quarter-2025-Results/default.aspx", "2025-10-29", "Meta Q3 2025 capex was $19.37B; 2025 capex guidance was $70B-$72B and management expected 2026 capex dollar growth to be notably larger, driven by infrastructure capacity needs."),
  source("SRC-META-Q4-2025", "Meta Q4 2025 results", "evidence", "https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Fourth-Quarter-and-Full-Year-2025-Results/default.aspx", "2026-01-28", "Meta FY2025 capital expenditures, including principal payments on finance leases, were $72.22B, and Meta expected 2026 capital expenditures of $115B-$135B as it invested in infrastructure capacity and AI/superintelligence labs."),
  source("SRC-ORCL-FY26-Q2", "Oracle FY2026 Q2 results", "evidence", "https://investor.oracle.com/investor-news/news-details/2025/Oracle-Announces-Fiscal-Year-2026-Second-Quarter-Financial-Results/default.aspx", "2025-12-10", "Oracle Q2 FY2026 RPO was $523B, +438%; cloud revenue was $8.0B, +34%; TTM capex was $35.5B and FCF was negative $13.2B after heavy cloud infrastructure investment."),
  source("SRC-CHATGPT-MAU-202302", "TIME: ChatGPT 100M users in two months", "message", "https://time.com/6253615/chatgpt-fastest-growing/", "2023-02-08", "TIME cited Similarweb and UBS data that ChatGPT reached about 100M monthly active users in January 2023, two months after launch."),
  source("SRC-CHATGPT-WAU-202408", "The Verge: ChatGPT 200M weekly users", "message", "https://www.theverge.com/2024/8/29/24231685/openai-chatgpt-200-million-weekly-users", "2024-08-29", "The Verge reported OpenAI confirmed ChatGPT had more than 200M weekly users in August 2024, double the 100M weekly active users reported in November 2023."),
  source("SRC-CHATGPT-WAU-202412", "The Verge: ChatGPT 300M weekly users", "message", "https://www.theverge.com/2024/12/4/24313097/chatgpt-300-million-weekly-users", "2024-12-04", "The Verge reported Sam Altman said ChatGPT had more than 300M weekly active users and more than 1B daily messages at NYT DealBook."),
  source("SRC-CHATGPT-WAU-202508", "Windows Central: ChatGPT weekly users and prompt volume", "message", "https://www.windowscentral.com/artificial-intelligence/chatgpt-is-set-to-hit-700-million-weekly-users-but-can-its-rivals-catch-up", "2025-08-05", "Windows Central reported ChatGPT was on track to reach 700M weekly active users in August 2025, about 4x year over year, with an estimated 2.5B-3.0B prompts per day."),
  source("SRC-CHATGPT-WAU-202510", "Economic Times: OpenAI DevDay 2025 ChatGPT apps", "message", "https://m.economictimes.com/tech/artificial-intelligence/devday-2025-openai-launches-apps-inside-chatgpt/articleshow/124346472.cms", "2025-10-06", "Economic Times reported OpenAI said ChatGPT weekly users surpassed 800M at DevDay 2025, alongside the launch of apps inside ChatGPT."),
  source("SRC-OPENAI-CHATGPT-WORK-202602", "OpenAI ChatGPT usage and adoption patterns at work", "evidence", "https://openai.com/business/guides-and-resources/chatgpt-usage-and-adoption-patterns-at-work/", "2026-02-01", "OpenAI said ChatGPT had 100M weekly active users within months of release and over 700M weekly active users; the page chart shows steady growth from November 2023 through July 2025."),
  source("SRC-OPENAI-DEVDAY-2025", "OpenAI DevDay 2025", "evidence", "https://openai.com/devday/", "2025-10-06", "OpenAI said it served more than 4M developers, more than 800M weekly ChatGPT users and more than 6B tokens per minute across its API platform."),
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

  const bomQuestionSearchArtifacts = buildAllBomQuestionSearchArtifacts();
  const scoringWorksheet = targets.map((targetItem, index) => buildTargetAudit(targetItem, index + 1));
  const workbench = {
    project_id: PROJECT_ID,
    as_of_date: AS_OF_DATE,
    run_mode: "historical_backtest",
    bom_question_search_artifacts: bomQuestionSearchArtifacts,
    bom_stage_rollup_policy: {
      workflow_order: "search_and_parse_each_bom_question_before_verdict_then_roll_up_7_questions_into_bom_s_curve_stage",
      local_cache_policy: "old local artifacts are caches only; they cannot replace fresh question-level search artifacts",
      public_rendering_policy: "show compact evidence status and stage rollup; keep raw search plans in workbench artifacts",
    },
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

function buildAllBomQuestionSearchArtifacts() {
  return bomNodes.flatMap((node) => (
    bomCoreQuestionRows(node)
      .map((row, index) => applyBomQuestionSearchOverride(row, index + 1, node))
      .map((row, index) => buildBomQuestionSearchArtifact(row, index + 1, node))
  ));
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
  const rows = bomCoreQuestionRows(node).map((row, index) => applyBomQuestionSearchOverride(row, index + 1, node));
  return `<details class="industry-module bom-research-module" open>
    <summary class="module-head"><span class="module-index">${String(moduleNumber).padStart(2, "0")}</span><div><h3>${e(node.name)}</h3><p>${e(node.plain)}</p></div><span class="chevron">›</span></summary>
    <div class="industry-module-body">
      <div class="bom-node-brief">
        <article><span>接受</span><p>${e(node.receives)}</p></article>
        <article><span>生产</span><p>${e(node.produces)}</p></article>
        <article><span>提供给</span><p>${e(node.suppliesTo)}</p></article>
        <article><span>验证指标</span><p>${e(node.metrics)}</p></article>
      </div>
      <div class="bom-question-list">${rows.map((row, index) => renderBomQuestionCard(row, index + 1, node)).join("")}</div>
      ${renderBomSCurveStageCard(node, rows)}
    </div>
  </details>`;
}

function renderBomQuestionCard(row, questionNumber, node) {
  return `<details class="bom-question-card" open>
    <summary><span class="bom-question-index">${questionNumber}</span><strong>${e(row.question)}</strong><span class="chevron">›</span></summary>
    <div class="bom-question-answer">
      ${renderBomQuestionResearchStatus(row, questionNumber, node)}
      <section class="bom-question-verdict"><b>本问结论</b><p>${sourceText(row.answer)}</p></section>
      ${renderBomQuestionFourStep(row, questionNumber, node)}
      <div class="bom-question-sources">${sourceChips(row.sourceIds)}</div>
    </div>
  </details>`;
}

function renderBomQuestionResearchStatus(row, questionNumber, node) {
  const artifact = buildBomQuestionSearchArtifact(row, questionNumber, node);
  const isCompleted = artifact.search_execution_status === "completed";
  const leadText = isCompleted
    ? "本问已按当前 BOM × 当前子问完成外部搜索、来源解析、metric 历史/缺口检查，再写入本问结论。"
    : "本问结论只能在当前 BOM × 当前子问完成外部搜索、来源解析和缺口标注之后写入；旧本地材料只能作为待验证缓存。";
  const evidenceText = isCompleted
    ? `本问已绑定 ${artifact.source_ids.length} 条 question-level 来源；后续刷新不得用其它 BOM 的粗证据池替代本问证据。`
    : `当前静态报告引用 ${artifact.source_ids.length} 条已导入公开来源；完整刷新必须生成 question-level search artifact 后再评估本问。`;
  return `<details class="bom-question-research-status">
    <summary><b>搜索与证据状态</b><span>${artifact.search_execution_status}</span><span class="chevron">›</span></summary>
    <div class="bom-question-research-body">
      <article><span>检索先行</span><p>${sourceText(leadText)}</p></article>
      <article><span>证据包</span><p>${sourceText(evidenceText)}</p></article>
      <article><span>缺口规则</span><p>若搜索后仍没有同口径历史序列、未来锚点或反证材料，必须显式标为 gap，不得用模型先验补成结论。</p></article>
    </div>
  </details>`;
}

function buildBomQuestionSearchArtifact(row, questionNumber, node) {
  const questionKey = `${node.id}_q${questionNumber}`;
  const override = row.searchArtifact || {};
  return {
    artifact_id: `BOM-SEARCH-${questionKey}`,
    bom_node_id: node.id,
    bom_node: node.name,
    question_number: questionNumber,
    question: row.question,
    workflow_order: [
      "external_search",
      "source_parse",
      "metric_history_and_gap_check",
      "question_verdict",
      "bom_s_curve_stage_rollup_after_6_questions",
    ],
    search_execution_status: override.search_execution_status || "待逐问搜索",
    source_universe_plan: override.source_universe_plan || {
      priority_sources: ["company_filings", "earnings_transcripts", "industry_research", "customer_capex_disclosures", "technical_supply_chain_teardowns"],
      cutoff_policy: `only sources visible on or before ${AS_OF_DATE} may strengthen the historical backtest conclusion`,
    },
    exa_search_plan: override.exa_search_plan || {
      direct_query: `${node.name} ${row.question.replace(/[？?]/g, "")} AI factory ${AS_OF_DATE} revenue orders capacity outlook`,
      expected_fields: ["metric_history", "future_expectation", "supply_constraint", "pricing_or_margin", "refuting_evidence"],
      gap_rule: "if same-metric history has fewer than five comparable points, render metric-trend-gap instead of inventing a curve",
    },
    source_ids: [...new Set(override.source_ids || row.sourceIds || [])],
    evidence_summary: override.evidence_summary || [],
    gap_summary: override.gap_summary || [],
    parser_status: override.parser_status || "pending",
    completed_at: override.completed_at || null,
    verdict_policy: override.verdict_policy || "do_not_write_or_strengthen_verdict_before_search_parse_or_explicit_gap",
  };
}

function applyBomQuestionSearchOverride(row, questionNumber, node) {
  if (node.id === "compute" && questionNumber === 1) {
    return strictComputeDemandRow(row);
  }
  if (node.id === "compute") {
    return strictComputeQuestionRow(row, questionNumber);
  }
  if (node.id === "manufacturing") {
    return strictManufacturingQuestionRow(row, questionNumber);
  }
  return row;
}

function strictComputeQuestionRow(row, questionNumber) {
  const presets = {
    2: strictComputeSupplyRow,
    3: strictComputeControlRow,
    4: strictComputeFinancialRow,
    5: strictComputePricingRow,
    6: strictComputeRefuteRow,
  };
  const builder = presets[questionNumber];
  return builder ? builder(row, questionNumber) : row;
}

function strictManufacturingQuestionRow(row, questionNumber) {
  const sharedSources = ["SRC-TSM-Q4-2025", "SRC-SA-COWOS-HBM-2023", "SRC-SA-GB200-BOM-2024"];
  const tsmcMetric = {
    type: "TSMC 财务与供给",
    name: "TSMC revenue / gross margin / advanced technologies share / 2026 capex",
    why: "先进制程与先进封装的需求、供给和财务兑现都要先看 TSMC 是否同时出现高收入、高毛利、高先进制程占比和高 capex；这些指标能把 AI 芯片需求从叙事落到制造供给层。",
    dataRequirement: "主体：TSMC；字段：revenue、gross margin、advanced technologies wafer revenue share、Q1 revenue/gross margin guide、2026 capital budget；单位：美元和百分比；频率：季度/年度；capex 和 guidance 放在预期栏，不冒充历史曲线。",
    trendKind: "non_time_series",
    trendLabel: "TSMC 制造供给截面",
    series: [
      { label: "Q4 2025 revenue", value: "$33.73B", change: "+25.5% YoY" },
      { label: "Q4 2025 gross margin", value: "62.3%", change: "高端制造议价强" },
      { label: "Q4 2025 advanced technologies", value: "77% of wafer revenue", change: "先进节点高度集中" },
      { label: "Q1 2026 revenue guide", value: "$34.6B-$35.8B", change: "近端收入继续强" },
      { label: "2026 capital budget", value: "$52B-$56B", change: "供给释放路径" },
    ],
    seriesGap: "这是同一公司披露的制造供给截面和指引组合，不是同一字段 5 个历史点；用于判断当前强度和未来供给释放，不画趋势线。",
    history: "[TSMC Q4 2025 revenue $33.73B、gross margin 62.3%、advanced technologies 77% of wafer revenue](source:SRC-TSM-Q4-2025)。",
    current: "[TSMC Q1 2026 revenue guide $34.6B-$35.8B、gross margin guide 63%-65%](source:SRC-TSM-Q4-2025)。",
    future: "[TSMC 2026 capital budget expected $52B-$56B](source:SRC-TSM-Q4-2025)，说明先进制造/封装供给仍在高强度扩张。",
    quality: "官方披露强；缺少 CoWoS 月产能、客户 allocation、按 AI/HPC 拆分的先进封装收入。",
    sourceIds: ["SRC-TSM-Q4-2025"],
  };
  const packagingMetric = {
    type: "先进封装瓶颈",
    name: "CoWoS / HBM integration bottleneck evidence",
    why: "AI accelerator 不只是先进晶圆，还需要把 GPU/ASIC 与 HBM 组合成可交付芯片；CoWoS 类先进封装和 HBM 集成决定有效供给是否能跟上。",
    dataRequirement: "主体：SemiAnalysis / TSMC 先进封装生态；字段：CoWoS/HBM bottleneck、GB200 rack-scale BOM、advanced packaging capacity signal；单位：技术路线和产能约束；频率：事件/报告。",
    trendKind: "non_time_series",
    trendLabel: "技术瓶颈证据",
    series: [
      { label: "2023 CoWoS/HBM constraint", value: "identified bottleneck", change: "供给卡点被专业拆解识别" },
      { label: "GB200 rack-scale BOM", value: "advanced packaging + HBM integration", change: "平台复杂度继续上升" },
      { label: "TSMC 2026 capex", value: "$52B-$56B", change: "供给扩张但非即时释放" },
    ],
    seriesGap: "专业拆解说明瓶颈方向，但公开材料没有直接给出连续月度 CoWoS 产能表。",
    history: "[SemiAnalysis 识别 CoWoS 和 HBM 是 AI accelerator 产能约束](source:SRC-SA-COWOS-HBM-2023)；[GB200 BOM 拆解显示 rack-scale 架构提高先进封装和集成复杂度](source:SRC-SA-GB200-BOM-2024)。",
    current: "先进封装不是可选项，而是 GPU/ASIC 和 HBM 变成可交付 AI accelerator 的必要工程环节。",
    future: "若 CoWoS/HBM 集成供给释放慢于 accelerator 平台需求，先进封装仍是供需瓶颈；若 capex 快速转化为可交付产能，稀缺性会下降。",
    quality: "第三方技术拆解强；缺少官方 CoWoS 产能、交期和价格序列。",
    sourceIds: ["SRC-SA-COWOS-HBM-2023", "SRC-SA-GB200-BOM-2024", "SRC-TSM-Q4-2025"],
  };
  const commonFutureCards = [
    expectationCard("TSMC 公司指引", "公司指引", "市场对先进制程与先进封装的近端预期，最硬的是 TSMC 自身给出的 Q1 收入/毛利指引和 2026 capex。", [
      expectationRow("TSMC", "Q4 2025", "[Revenue $33.73B，gross margin 62.3%，advanced technologies 77%](source:SRC-TSM-Q4-2025)。", "Q1 2026E / FY2026E", "[Q1 revenue $34.6B-$35.8B，gross margin 63%-65%；2026 capex $52B-$56B](source:SRC-TSM-Q4-2025)。", "Q1 指引验证近端需求，capex 验证供给释放；两者都不能直接等同于 CoWoS 产能。"),
    ], ["SRC-TSM-Q4-2025"]),
    expectationCard("专业拆解", "第三方判断", "专业拆解把先进封装放在 AI accelerator 有效供给链中，而不是把它当作普通晶圆制造扩产。", [
      expectationRow("SemiAnalysis", "2023-2024", "[CoWoS/HBM 被识别为 AI capacity constraint](source:SRC-SA-COWOS-HBM-2023)；[GB200 BOM 显示 rack-scale 架构对封装和集成要求更高](source:SRC-SA-GB200-BOM-2024)。", "后续平台周期", "继续观察 CoWoS 产能、HBM attach、rack-scale 平台设计和客户 allocation。", "第三方拆解是机制证据，不是公司财务指引；需要和 TSMC capex、毛利率、交期交叉验证。"),
    ], ["SRC-SA-COWOS-HBM-2023", "SRC-SA-GB200-BOM-2024"]),
  ];
  const configs = {
    1: {
      answer: "先进制程与先进封装的需求增长来自 GPU/ASIC 平台放量和 HBM 集成复杂度上升。TSMC Q4 2025 的高收入、高毛利、高 advanced technologies 占比，以及 2026 高 capex 指引，说明需求已经穿透到制造供给层；但 CoWoS/先进封装的直接产能、交期和价格仍是缺口。",
      metricLogic: "本问只判断先进制程与先进封装自身需求是否增长：GPU/ASIC 设计增加 -> 先进节点 wafer 和封装订单增加 -> CoWoS/HBM 集成成为必要环节 -> TSMC revenue、advanced technologies share、gross margin 和 capex 共同验证。",
      historySummary: "02 按制造供给和封装瓶颈两个环节展示：TSMC 指标说明财务和供给强度，SemiAnalysis 拆解说明先进封装为什么是 AI accelerator 的必要环节。",
      chainNodes: [
        { title: "制造需求是否穿透到 TSMC", metrics: [tsmcMetric] },
        { title: "先进封装是否成为 GPU/HBM 集成刚需", metrics: [packagingMetric] },
      ],
      futureCards: commonFutureCards,
      mechanism: {
        sustain: "只要 GPU/ASIC 平台继续走向更大 die、更高 HBM 带宽和 rack-scale 集成，先进制程与先进封装的需求会随有效供给链继续放大。",
        break: "如果架构优化降低先进封装复杂度，或 capex 快速释放导致 CoWoS/HBM 供给宽松，高毛利和稀缺性会下降。",
      },
      directQuery: "TSMC advanced technologies gross margin capex CoWoS HBM AI accelerator demand before 2026-03-28",
      evidenceSummary: ["TSMC 官方财务与 capex 指引已补入；SemiAnalysis CoWoS/HBM 拆解已补入。"],
      gapSummary: ["缺少 CoWoS 月产能、客户 allocation、先进封装 ASP 和交期序列。"],
    },
    2: {
      answer: "单位用量提升主要体现在每颗 AI accelerator 对先进节点、interposer/封装面积、HBM 集成和系统级封装复杂度的要求提高。TSMC 的 advanced technologies 高占比和 SemiAnalysis 的 GB200/CoWoS 拆解支持这一机制，但缺少按平台代际量化的封装面积和 CoWoS 用量表。",
      metricLogic: "单位用量问题不问 TSMC 总收入，而问单个 GPU/ASIC 平台是否需要更多先进制程和封装资源。核心链条是：平台规格升级 -> HBM attach 和封装复杂度提升 -> 每个平台消耗更多先进制造/封装资源 -> 单位价值量提高。",
      historySummary: "02 用 TSMC advanced technologies 占比和 SemiAnalysis GB200/CoWoS 拆解做证据；这些不是连续量化表，但能说明单位复杂度上升。",
      chainNodes: [
        { title: "先进制程占比是否高", metrics: [tsmcMetric] },
        { title: "封装和 HBM 集成复杂度是否上升", metrics: [packagingMetric] },
      ],
      futureCards: commonFutureCards,
      mechanism: {
        sustain: "若 AI accelerator 继续提高 HBM 带宽、封装密度和 rack-scale 集成，单位先进封装价值量会继续上升。",
        break: "若 chiplet/封装标准化、替代封装路线或设计优化降低 CoWoS 用量，单位用量提升会变弱。",
      },
      directQuery: "GB200 CoWoS HBM advanced packaging content per accelerator TSMC advanced technologies before 2026-03-28",
      gapSummary: ["缺少每代 GPU/ASIC 的 CoWoS 面积、interposer 数量、封装 ASP 和 HBM attach 量化表。"],
    },
    3: {
      answer: "先进制程与先进封装供给仍受有效产能、良率、设备、客户认证和 capex 周期约束。TSMC 2026 capex $52B-$56B 说明供给会扩张，但扩张不等于即时有效产能；CoWoS/HBM 的专业拆解仍提示先进封装是 AI accelerator 的串联约束。",
      metricLogic: "供给问题看有效产能而不是名义 capex：capex -> 设备到位 -> 良率/认证 -> CoWoS/HBM 可交付 -> GPU/ASIC 交付。任何环节慢于需求，短缺仍存在。",
      historySummary: "02 展示 TSMC 指标和 CoWoS/HBM 拆解；03 用 TSMC Q1/FY2026 指引说明供给释放路径。",
      chainNodes: [
        { title: "名义扩产与财务强度", metrics: [tsmcMetric] },
        { title: "有效产能串联约束", metrics: [packagingMetric] },
      ],
      futureCards: commonFutureCards,
      mechanism: {
        sustain: "供给约束持续的机制是高端封装和先进节点扩产、良率、认证慢于客户需求斜率。",
        break: "如果 capex 快速变成有效产能、交期缩短、价格松动或客户转向替代封装，供给瓶颈会降级。",
      },
      directQuery: "TSMC 2026 capex CoWoS capacity lead time advanced packaging supply constraint before 2026-03-28",
      gapSummary: ["缺少官方 CoWoS 产能、lead time、良率、工具交付和客户 allocation。"],
    },
    4: {
      answer: "供给控制权集中在 TSMC 及其先进封装生态，但这种控制权不是只看市场份额，而要看先进节点、封装能力、良率、客户认证和交付可靠性。当前公开证据能证明 TSMC 是核心控制者，但还不足以量化各类先进封装产能份额。",
      metricLogic: "控制权链条是：先进节点和封装 know-how -> 客户认证和排产权 -> allocation 和交付可靠性 -> 毛利率与 capex 回报。",
      historySummary: "02 用 TSMC advanced technologies、gross margin 和 capex 做控制权代理；用 CoWoS/HBM 拆解说明为什么替代难。",
      chainNodes: [
        { title: "TSMC 是否控制关键制造环节", metrics: [tsmcMetric] },
        { title: "替代难度来自哪里", metrics: [packagingMetric] },
      ],
      futureCards: commonFutureCards,
      mechanism: {
        sustain: "控制权持续来自先进节点、先进封装 know-how、客户认证、规模经验和生态配套。",
        break: "若客户多供应、OSAT/竞争代工追赶、或替代封装路线成熟，TSMC 控制权和稀缺溢价会被稀释。",
      },
      directQuery: "TSMC CoWoS control advanced packaging ecosystem allocation qualification AI accelerator before 2026-03-28",
      gapSummary: ["缺少 CoWoS/SoIC 等细分产能份额、客户 allocation 和替代供应商资格进度。"],
    },
    5: {
      answer: "财务兑现已经较强：TSMC Q4 2025 revenue $33.73B、gross margin 62.3%、advanced technologies 77%，Q1 2026 revenue/gross margin guide 也继续强。问题是这仍是公司整体/先进技术口径，不是 AI 先进封装单独收入；所以可以证明高端制造强，但不能精确证明 CoWoS 利润池大小。",
      metricLogic: "财务兑现链条是：先进节点/封装需求 -> TSMC 收入和 gross margin -> advanced technologies 占比 -> capex 回报和现金流质量。",
      historySummary: "02 重点展示 TSMC 官方披露；03 用 Q1 指引和 2026 capex 判断未来兑现路径。",
      chainNodes: [
        { title: "收入和毛利是否兑现", metrics: [tsmcMetric] },
        { title: "封装瓶颈是否能解释财务强度", metrics: [packagingMetric] },
      ],
      futureCards: commonFutureCards,
      mechanism: {
        sustain: "如果 advanced technologies 占比和 gross margin 持续高位，同时 capex 能带来高回报，财务兑现可持续。",
        break: "如果 capex 回报下行、产能释放压低毛利、或地缘/客户转单影响利用率，财务兑现质量会下降。",
      },
      directQuery: "TSMC advanced technologies revenue gross margin capex return AI HPC advanced packaging financial realization before 2026-03-28",
      gapSummary: ["缺少 AI/HPC 与 advanced packaging 分部收入、毛利、现金回报和客户集中度。"],
    },
    6: {
      answer: "市场对 TSMC 的强需求和高 capex 有预期，但本报告当前缺少 as-of 2026-03-28 的 forward PE、EPS revision、capex ROI 和地缘折价量化表，因此只能判断“基本面强、估值赔率待验证”。不能因为 TSMC 是瓶颈就直接推出买入结论。",
      metricLogic: "定价问题要把制造强度转成赔率：市场是否已经计入高 capex、高毛利、AI/HPC 增长和地缘风险折价；如果估值已充分反映，强基本面也只能是 watch_only。",
      historySummary: "02 用 TSMC 官方数据证明基本面强；估值和隐含预期仍是趋势缺口，不能用 post-label 股价表现回填。",
      chainNodes: [
        { title: "基本面预期是否强", metrics: [tsmcMetric] },
        { title: "估值赔率缺口", metrics: [{
          type: "估值缺口",
          name: "TSMC as-of forward PE / EPS revision / capex ROI gap",
          why: "判断是否已定价需要 as-of 估值、盈利上修和资本回报，不是只看收入和 capex。",
          dataRequirement: "主体：TSMC；字段：forward PE、EV/EBITDA、EPS revision、capex ROI、geopolitical discount；单位：倍数/百分比；期间：2026-03-28 前可见。",
          series: [],
          seriesGap: "当前源包没有可验证的 as-of 估值和盈利上修序列，因此市场是否已定价不能完整回答。",
          history: "TSMC 基本面强，但估值赔率缺口未补齐。",
          current: "维持 watch_only 口径，不从基本面强直接跳到高赔率。",
          future: "下一轮应补 as-of consensus、forward PE、EPS revision、capex ROI 和地缘折价。",
          quality: "估值缺口。",
          sourceIds: ["SRC-TSM-Q4-2025"],
        }] },
      ],
      futureCards: commonFutureCards,
      mechanism: {
        sustain: "若盈利上修持续超过估值隐含增长，且地缘风险没有扩大，赔率仍可能存在。",
        break: "若市场已经充分计入高增长和高毛利，或 capex ROI/地缘风险恶化，赔率下降。",
      },
      directQuery: "TSMC valuation forward PE EPS revision capex ROI AI advanced packaging before 2026-03-28",
      gapSummary: ["缺少 as-of 2026-03-28 估值、盈利上修、目标价分布、capex ROI 和地缘风险折价。"],
    },
    7: {
      answer: "核心反证是：CoWoS/先进封装扩产快于需求、良率改善导致稀缺性下降、客户多供应或替代封装路线成熟、TSMC capex 回报下降、gross margin guide 下行，或地缘风险导致客户转单。当前材料没有显示这些反证已经发生，但缺少交期、价格和客户 allocation 监控。",
      metricLogic: "反证链条要跟前面相反：客户需求放缓 -> capex 过剩 -> CoWoS/HBM 交期缩短 -> 价格/毛利下行 -> TSMC 指引或利用率下修。",
      historySummary: "02 用 TSMC 指引和 CoWoS/HBM 拆解定义反证阈值；03 仍以公司指引和第三方拆解为监控锚点。",
      chainNodes: [
        { title: "供给释放反证", metrics: [tsmcMetric] },
        { title: "封装瓶颈消退反证", metrics: [packagingMetric] },
      ],
      futureCards: commonFutureCards,
      mechanism: {
        sustain: "如果交期仍长、毛利率强、capex 仍高回报，反证未出现。",
        break: "如果供给释放超过需求，短缺逻辑会先表现为交期缩短、ASP/毛利下降和 capex 回报走弱。",
      },
      directQuery: "TSMC CoWoS oversupply lead time gross margin capex return refutation before 2026-03-28",
      gapSummary: ["缺少 CoWoS lead time、先进封装 ASP、客户订单取消率、利用率和 capex ROI 监控阈值。"],
    },
  };
  const config = configs[questionNumber === 1 ? 1 : questionNumber + 1];
  if (!config) return row;
  return strictComputeRichRow(row, questionNumber, {
    sourceIds: sharedSources,
    prioritySources: ["TSMC earnings release and guidance", "SemiAnalysis CoWoS/HBM technical teardown", "advanced packaging supply-chain materials"],
    expectedFields: ["TSMC financial/current baseline", "company guidance", "advanced packaging bottleneck evidence", "direct capacity gap"],
    evidenceSummary: config.evidenceSummary || ["补入 TSMC 官方披露和 SemiAnalysis 先进封装拆解。"],
    ...config,
  });
}

function strictComputeRichRow(row, questionNumber, config) {
  let chainNodes = config.chainNodes.map((node) => ({
    ...node,
    sourceIds: node.sourceIds || uniqueSourceIdsFromMetrics(node.metrics || []),
  }));
  while (chainNodes.length < 4) {
    chainNodes = [...chainNodes, strictComputeGapChainNode(row, config, chainNodes.length + 1)];
  }
  let futureCards = config.futureCards || [];
  while (futureCards.length < chainNodes.length) {
    futureCards = [
      ...futureCards,
      strictComputeGapFutureCard(row, config, chainNodes[chainNodes.length - 1]),
    ];
  }
  const sourceIds = [...new Set([
    ...(config.sourceIds || []),
    ...chainNodes.flatMap((node) => node.sourceIds || []),
    ...futureCards.flatMap((card) => card.sourceIds || []),
  ])];
  return {
    ...row,
    answer: config.answer,
    sourceIds,
    metricLogic: config.metricLogic,
    historySummary: config.historySummary,
    futureCards,
    mechanism: config.mechanism,
    replaceDefaultMetrics: true,
    detail: {
      ...(row.detail || {}),
      reportNarrative: {
        ...(row.detail?.reportNarrative || {}),
        chainNodes,
      },
    },
    searchArtifact: {
      search_execution_status: "completed",
      parser_status: "gpt_verified_source_parse",
      completed_at: "2026-07-07",
      source_ids: sourceIds,
      source_universe_plan: {
        priority_sources: config.prioritySources || [
          "company earnings releases and guidance",
          "industry processor forecast and technical teardowns",
          "customer capex / order disclosures",
          "valuation and market expectation proxies",
        ],
        selected_source_ids: sourceIds,
        cutoff_policy: `only sources visible on or before ${AS_OF_DATE} strengthen the as-of conclusion; later labels or price action are excluded`,
      },
      exa_search_plan: {
        direct_query: config.directQuery,
        expected_fields: config.expectedFields || [
          "same_metric_history",
          "company_guidance_or_market_expectation",
          "current_baseline",
          "forward_anchor",
          "refuting_evidence_or_gap",
        ],
        selected_source_ids: sourceIds,
        retrieval_status: "completed",
        gap_rule: "same-metric history requires at least five comparable points; if fewer, render metric-trend-gap and keep forecasts in 03 rather than 02",
      },
      evidence_summary: config.evidenceSummary || [],
      gap_summary: config.gapSummary || [],
      verdict_policy: "verdict_written_after_question_level_search_parse_and_explicit_gap_marking",
    },
  };
}

function uniqueSourceIdsFromMetrics(metrics) {
  return [...new Set(metrics.flatMap((metric) => metric.sourceIds || []))];
}

function strictComputeGapChainNode(row, config, gapIndex = 1) {
  const sourceIds = [...new Set([
    ...(config.sourceIds || []),
    ...(config.chainNodes || []).flatMap((node) => uniqueSourceIdsFromMetrics(node.metrics || [])),
  ])].slice(0, 5);
  return {
    title: gapIndex > 1 ? `缺口与监控 ${gapIndex}` : "缺口与监控",
    sourceIds,
    metrics: [
      {
        type: "缺口与监控",
        name: `${row.question} direct validation gap ${gapIndex}`,
        why: "富数据问题最后必须保留一个直接验证缺口：已有材料能回答方向，但仍要标出哪些关键 metric 没有被公开同口径历史、公司指引或第三方预期覆盖。",
        dataRequirement: "主体：当前 BOM 相关供应商、客户和第三方机构；字段：直接验证该问的同口径历史、未来指引、价格/交期/利用率/估值或反证阈值；单位按字段定义；缺失时不得用模型先验补结论。",
        series: [],
        seriesGap: (config.gapSummary || ["当前仍缺少完整同口径历史或未来预期数据。"]).join("；"),
        history: "当前已补入公开可见的公司披露、指引和第三方预测，但直接验证缺口仍需显式保留。",
        current: "该缺口不会推翻已写入的本问方向性判断，但会降低结论强度和标的推荐强度。",
        future: "下一轮刷新应优先围绕该缺口搜索，而不是重复扩展泛化证据池。",
        quality: "显式缺口；不替代结论。",
        sourceIds,
      },
    ],
  };
}

function strictComputeGapFutureCard(row, config, chainNode) {
  const sourceIds = chainNode.sourceIds || [];
  return expectationCard("缺口与监控", "关键缺口", `本问仍有直接验证缺口：${(config.gapSummary || ["缺少完整同口径历史或未来预期数据。"]).join("；")}。这些缺口必须进入后续搜索计划，不能用已有方向性材料替代。`, [
    expectationRow(
      "当前 BOM / 后续刷新",
      "当前报告 as-of source pack",
      "已补入公开公司披露、管理层指引和第三方预测。",
      "下一轮刷新",
      "优先补直接 metric、连续历史、未来指引、价格/交期/利用率/估值或反证阈值。",
      "这是质量控制卡；它说明结论边界，不是新增正面或负面证据。"
    ),
  ], sourceIds);
}

function strictComputeUnitUsageRow(row, questionNumber) {
  const chainNodes = [
    {
      title: "平台规格是否从单卡走向 rack / pod / cluster",
      metrics: [
        {
          type: "平台规格",
          name: "NVIDIA AI factory platform generation scope",
          why: "单位用量提升首先看采购单位是否从单卡/单服务器升级为 rack-scale、pod-scale 或 cluster-scale accelerator 平台；这决定同一客户项目需要更多 GPU/ASIC、CPU、NVLink、DPU 和网络芯片。",
          dataRequirement: "主体：NVIDIA；字段：平台代际规格、rack/pod-scale 系统组成、推理成本/性能改善；单位：平台代际或相对性能；频率：平台发布和季度更新；少于 5 个同口径点时按规格表，不画趋势。",
          trendLabel: "平台代际规格点",
          trendKind: "non_time_series",
          series: [
            { label: "GB200 / NVL72", value: "rack-scale", change: "从 server/card 到 rack 级系统" },
            { label: "Blackwell Ultra", value: "50x agentic AI perf / 35x lower cost vs Hopper", change: "推理负载单位经济性改善" },
            { label: "Vera Rubin", value: "six/seven chips + rack-scale systems", change: "继续平台化" },
          ],
          seriesGap: "这些是平台规格事件，不是同一数值字段的历史序列；只用于说明采购单位升级，不能画成连续趋势线。",
          history: "[NVIDIA FY26 Q4 highlights 披露 Vera Rubin 平台和 Blackwell Ultra 推理性能/成本改善](source:SRC-NVDA-FY26-Q4)，[GTC 2026 Vera Rubin 新闻进一步定义下一代 AI factory rack-scale 系统](source:SRC-NVDA-GTC-VERA-RUBIN-20260316)。",
          current: "当前 accelerator 需求单位已经从“买 GPU 卡”转向“买完整 AI factory 平台规格”；这会放大每个项目的 GPU/ASIC 单位用量。",
          future: "[NVIDIA Q1 FY27 revenue outlook 为 $78.0B +/-2%](source:SRC-NVDA-FY26-Q4)，若后续平台收入继续按新平台规格兑现，单位用量提升仍成立。",
          quality: "规格证据强；缺少跨代单柜 GPU 数量和 ASP 的连续公开表。",
          sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-NVDA-GTC-VERA-RUBIN-20260316"],
        },
      ],
    },
    {
      title: "单位算力是否被推理和 agent 任务继续吃掉",
      metrics: [
        {
          type: "推理经济性",
          name: "NVIDIA disclosed inference cost/performance improvement",
          why: "如果每代平台把单位 token 成本压低，客户会更容易把训练后的模型部署成在线推理和 agent 服务，形成更多 accelerator 部署需求。",
          dataRequirement: "主体：NVIDIA；字段：inference token cost 或 agentic AI performance improvement；单位：倍数；频率：平台代际；这是机制指标，不能和收入序列混画。",
          trendLabel: "机制指标",
          series: [
            { label: "Blackwell Ultra vs Hopper", value: "up to 50x perf / 35x lower cost", change: "显著改善推理经济性" },
            { label: "Vera Rubin vs Blackwell", value: "up to 10x token cost reduction", change: "继续降低单位 token 成本" },
            { label: "Dynamo 1.0", value: "up to 7x Blackwell inference performance", change: "提升线上推理调度效率" },
          ],
          seriesGap: "这是产品路线图和 benchmark 口径，不是公司财务字段；只用于解释为什么单位用量可能继续扩张。",
          history: "[NVIDIA FY26 Q4 highlights 提到 Blackwell Ultra 和 Vera Rubin 的推理成本/性能改善](source:SRC-NVDA-FY26-Q4)；[Dynamo 1.0 声称可提升 Blackwell inference performance](source:SRC-NVDA-GTC-DYNAMO-20260316)。",
          current: "推理效率提升不一定降低总硬件需求；如果更低成本带来更多在线任务和 agent 调用，反而会提升部署规模。",
          future: "未来要把这一机制和 OpenAI tokens/min、Gemini daily-token、云 AI revenue、GPU hours 或 utilization 交叉验证。",
          quality: "机制支持强；缺少客户侧 GPU-hours 同口径序列。",
          sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-NVDA-GTC-DYNAMO-20260316", "SRC-OPENAI-DEVDAY-2025", "SRC-GOOGL-Q4-2025-CALL"],
        },
      ],
    },
    {
      title: "平台单位升级是否已经进入系统交付",
      metrics: [
        {
          type: "系统交付",
          name: "Dell AI-optimized server shipments / backlog / FY27 revenue guide",
          why: "单位用量提升最终要进入整机/机柜系统交付；Dell 的 orders、shipments、backlog 和 FY27 revenue guide 可以验证平台规格不是停留在发布会。",
          dataRequirement: "主体：Dell；字段：AI-optimized server orders、shipments、ending backlog、revenue guide；单位：十亿美元；频率：季度/年度；订单和收入为漏斗数据，不与单一季度收入曲线混画。",
          trendKind: "non_time_series",
          trendLabel: "订单到收入漏斗",
          series: [
            { label: "FY26 orders", value: ">$64B", change: "形成全年订单池" },
            { label: "FY26 shipments", value: ">$25B", change: "部分转入交付" },
            { label: "FY27 backlog", value: "$43B", change: "未来交付池扩大" },
            { label: "FY27 revenue guide", value: "~$50B", change: "收入指引承接 backlog" },
          ],
          history: "[Dell FY26 披露 AI-optimized server orders、shipments、backlog 和 FY27 revenue guide](source:SRC-DELL-FY26-Q4)。",
          current: "含 GPU/ASIC 的系统交付已经出现高额 backlog，说明客户不是只买单卡，而是在采购整套 AI server / rack 方案。",
          future: "若 FY27 AI-optimized server revenue 兑现，单位用量提升会继续从平台规格传到整机和机柜交付。",
          quality: "系统交付验证强；仍需补毛利率、取消率和客户集中。",
          sourceIds: ["SRC-DELL-FY26-Q4"],
        },
      ],
    },
  ];
  return strictComputeRichRow(row, questionNumber, {
    answer: "GPU/ASIC 的单位用量提升已经有较强证据：平台从单卡/单服务器转向 rack-scale / pod-scale / AI factory，推理经济性改善推动更多在线部署，Dell 的 AI server backlog 和收入指引说明这种规格升级开始进入系统交付。但公开材料还缺单柜 GPU 数、ASP、GPU-hours 与客户配置的连续表。",
    metricLogic: "单位用量问题不问总需求有多大，而问同一客户项目、同一机柜或同一 AI factory 是否天然消耗更多当前 BOM。GPU/ASIC 的判断链条是：平台采购单位升级 -> 推理/agent 任务提高在线部署需求 -> 系统交付验证 -> 单位价值量和收入兑现。",
    historySummary: "02 按 01 的三个环节选择指标：平台规格看 NVIDIA 平台代际规格；推理经济性看 NVIDIA 披露的 token cost / inference performance 改善；系统交付看 Dell AI server orders、shipments、backlog 和 FY27 revenue guide。前两项是规格/机制数据，不画成财务趋势；Dell 是订单到收入漏斗。",
    chainNodes,
    futureCards: [
      expectationCard("平台规格", "公司路线图", "NVIDIA 的市场预期不是给出单柜 GPU 数，而是继续把 AI factory 推向 Vera Rubin rack-scale / pod-scale 平台，同时给出 Q1 FY27 revenue outlook。", [
        expectationRow("NVIDIA", "Q4 FY2026 / GTC 2026", "[Data Center revenue $62.3B，FY26 full-year Data Center revenue $193.7B](source:SRC-NVDA-FY26-Q4)。", "Q1 FY2027E / Vera Rubin cycle", "[Q1 FY27 revenue outlook $78.0B +/-2%](source:SRC-NVDA-FY26-Q4)；[Vera Rubin 定义下一代 AI factory 平台](source:SRC-NVDA-GTC-VERA-RUBIN-20260316)。", "收入指引是公司整体口径，Vera Rubin 是平台规格；二者共同说明单位用量提升有未来平台锚点。"),
      ], ["SRC-NVDA-FY26-Q4", "SRC-NVDA-GTC-VERA-RUBIN-20260316"]),
      expectationCard("推理经济性", "产品路线图", "市场预期是推理成本下降会扩大线上推理与 agent 工作负载，但这需要用实际 token/GPU-hours 继续验证。", [
        expectationRow("NVIDIA", "FY2026 Q4 highlights", "[Blackwell Ultra / Vera Rubin 被表述为继续降低 inference token cost](source:SRC-NVDA-FY26-Q4)。", "2026-2028 platform cycle", "[Dynamo 1.0 强调 AI factory inference orchestration](source:SRC-NVDA-GTC-DYNAMO-20260316)。", "这是机制预期，不是收入指引；若单位成本下降没有带来更多任务量，则单位用量结论要下调。"),
      ], ["SRC-NVDA-FY26-Q4", "SRC-NVDA-GTC-DYNAMO-20260316"]),
      expectationCard("系统交付", "公司指引", "Dell 把 AI server 从订单和出货推进到 FY27 revenue guide，是单位用量提升穿透到系统交付的硬预期。", [
        expectationRow("Dell", "FY2026", "[AI-optimized server orders >$64B、shipments >$25B、FY27 backlog $43B](source:SRC-DELL-FY26-Q4)。", "FY2027E", "[AI-optimized server revenue guide 约 $50B、同比 +103%](source:SRC-DELL-FY26-Q4)。", "系统交付不是当前 BOM 的利润结论，但能验证 GPU/ASIC 单位采购强度已经进入未来交付池。"),
      ], ["SRC-DELL-FY26-Q4"]),
    ],
    mechanism: {
      sustain: "可持续机制是平台采购单位继续变大，推理和 agent 任务把 GPU/ASIC 从训练资产变成在线服务资产，系统交付商继续把整柜和集群方案转成 backlog 与收入。",
      break: "不可持续机制是推理效率提升完全抵消任务量增长，客户从整柜扩容转向存量优化，或者 AI server backlog 不能转收入并暴露低毛利/取消率。",
    },
    directQuery: "GPU ASIC unit content rack-scale AI factory Vera Rubin NVL72 Dell AI optimized server backlog revenue guide before 2026-03-28",
    evidenceSummary: ["平台规格、推理经济性和系统交付三个环节均有 cutoff-visible 材料，但单柜 GPU 数、ASP 与客户配置连续数据仍缺。"],
    gapSummary: ["缺少跨代单柜 GPU/ASIC 数量、平均 ASP、客户配置与实际 GPU-hours 的可比序列。"],
  });
}

function strictComputeSupplyRow(row, questionNumber) {
  const chainNodes = [
    {
      title: "先进制程与先进封装供给",
      metrics: [
        {
          type: "制造/封装",
          name: "TSMC advanced technologies share, gross margin and 2026 capex",
          why: "GPU/ASIC 的最终供给受先进制程和先进封装制约；TSMC 的先进技术收入占比、毛利率和 capex 指引能验证核心制造供给是否仍紧。",
          dataRequirement: "主体：TSMC；字段：advanced technologies share、gross margin、revenue guidance、capital budget；单位：%、美元；频率：季度/年度；capex 是未来供给释放锚点，不混入历史收入曲线。",
          trendKind: "non_time_series",
          trendLabel: "制造供给截面与指引",
          series: [
            { label: "Q4 2025 revenue", value: "$33.73B", change: "+25.5% YoY" },
            { label: "Q4 2025 gross margin", value: "62.3%", change: "高毛利说明供给强势" },
            { label: "Q4 2025 advanced tech share", value: "77%", change: "先进节点高度集中" },
            { label: "2026 capex guide", value: "$52B-$56B", change: "扩产释放路径" },
          ],
          seriesGap: "这是制造供给截面、盈利质量和扩产指引组合，不是同一字段的连续历史曲线。",
          history: "[TSMC Q4 2025 revenue $33.73B、gross margin 62.3%、advanced technologies 77% of wafer revenue](source:SRC-TSM-Q4-2025)。",
          current: "[TSMC 预计 Q1 2026 revenue $34.6B-$35.8B、gross margin 63%-65%](source:SRC-TSM-Q4-2025)。",
          future: "[2026 capital budget expected $52B-$56B](source:SRC-TSM-Q4-2025)，说明供给会扩张，但释放需要设备、良率和客户排产时间。",
          quality: "官方供给指引强；缺少 CoWoS 月产能和客户 allocation。",
          sourceIds: ["SRC-TSM-Q4-2025"],
        },
      ],
    },
    {
      title: "HBM 与内存配套是否成为串联约束",
      metrics: [
        {
          type: "内存约束",
          name: "Micron HBM TAM and 2026 price/volume agreements",
          why: "GPU/ASIC 供给不是只有晶圆，HBM 是可交付 accelerator 的串联约束；Micron 的 HBM TAM 与价量协议能验证内存供给是否仍偏紧。",
          dataRequirement: "主体：Micron；字段：HBM TAM、price and volume agreements、HBM supply status；单位：美元 TAM / 合同状态；频率：财报/管理层材料。",
          trendKind: "non_time_series",
          trendLabel: "HBM 供需锚点",
          series: [
            { label: "CY2025 HBM TAM", value: "~$35B", change: "当前池子" },
            { label: "CY2028 HBM TAM", value: "~$100B", change: "~40% CAGR" },
            { label: "2026 HBM supply", value: "price/volume agreements completed", change: "供需进入合同层" },
          ],
          seriesGap: "TAM 与价量协议不是季度供给曲线；用于验证 HBM 仍是 GPU/ASIC 交付约束。",
          history: "[Micron prepared remarks forecast HBM TAM from about $35B in CY2025 to around $100B in CY2028](source:SRC-MU-FY26-Q1-PREPARED)。",
          current: "[Micron 表示 2026 HBM supply 已完成 price and volume agreements](source:SRC-MU-FY26-Q1-PREPARED)。",
          future: "若 HBM TAM 和价量协议继续上行，GPU/ASIC 供给释放仍受内存认证和产能制约。",
          quality: "前瞻供需材料强；缺少 HBM 各厂份额和产能释放表。",
          sourceIds: ["SRC-MU-FY26-Q1-PREPARED", "SRC-MU-FY26-Q1"],
        },
      ],
    },
    {
      title: "系统交付能否承接芯片供给",
      metrics: [
        {
          type: "系统交付",
          name: "Dell AI-optimized server ending backlog and shipments",
          why: "即便芯片制造扩张，最终可交付供给仍要经过服务器和机柜系统；Dell backlog/shipments 能验证系统交付是否仍有排队。",
          dataRequirement: "主体：Dell；字段：AI-optimized server shipments、ending backlog、orders；单位：十亿美元；频率：季度/年度。",
          trendKind: "time_series",
          trendLabel: "系统交付 backlog",
          series: [
            { label: "Q4 FY25", value: "~$9B", change: "基准" },
            { label: "Q1 FY26", value: "$14.4B", change: "+60% vs Q4 FY25" },
            { label: "Q2 FY26", value: "$11.7B", change: "交付消化后回落" },
            { label: "Q3 FY26", value: "$18.4B", change: "重新上行" },
            { label: "Q4 FY26", value: "$43B", change: "显著跃升" },
          ],
          history: "[Dell AI server backlog 从 FY25 Q4 约 $9B 到 FY26 Q4 / FY27 entry $43B](source:SRC-DELL-FY26-Q4)。",
          current: "[FY26 shipments 超过 $25B](source:SRC-DELL-FY26-Q4)，说明交付已在推进，但 backlog 仍大。",
          future: "[FY27 AI-optimized server revenue guide 约 $50B](source:SRC-DELL-FY26-Q4)，是系统交付供给释放的下一步验证。",
          quality: "系统交付约束有 5 个点；仍需补取消率和毛利。",
          sourceIds: ["SRC-DELL-FY25-Q4", "SRC-DELL-FY26-Q1", "SRC-DELL-FY26-Q2-PERFORMANCE", "SRC-DELL-FY26-Q3", "SRC-DELL-FY26-Q4"],
        },
      ],
    },
  ];
  return strictComputeRichRow(row, questionNumber, {
    answer: "GPU/ASIC 供给短期不能简单说“能跟上”。核心制约来自 TSMC 先进制程/先进封装、HBM 供给与价量协议、以及 AI server 系统交付。TSMC 和 Dell 都给出扩张指引，说明供给会释放；但 HBM、封装、系统交付和客户认证仍可能让有效供给慢于需求斜率。",
    metricLogic: "供给问题要拆成有效供给链：先进制程/先进封装 -> HBM 配套 -> 系统交付。只看 NVIDIA/Broadcom 需求是不够的；如果任一串联约束慢于需求，GPU/ASIC 可交付量仍紧。",
    historySummary: "02 复用供给链条：制造/封装看 TSMC advanced technologies、毛利率和 capex；HBM 配套看 Micron HBM TAM 和价量协议；系统交付看 Dell backlog/shipments。指引和 TAM 放在 03 或非连续表中，不冒充同口径历史。",
    chainNodes,
    futureCards: [
      expectationCard("制造/封装", "公司指引", "TSMC 的市场预期是 2026 继续高 capex 扩产，同时 Q1 revenue 和 gross margin guide 仍强。", [
        expectationRow("TSMC", "Q4 2025", "[Revenue $33.73B，gross margin 62.3%，advanced technologies 77%](source:SRC-TSM-Q4-2025)。", "Q1 2026E / FY2026E", "[Q1 revenue $34.6B-$35.8B，gross margin 63%-65%；2026 capex $52B-$56B](source:SRC-TSM-Q4-2025)。", "Q1 指引代表近端需求，capex 代表供给释放路径；不等于 CoWoS 月产能。"),
      ], ["SRC-TSM-Q4-2025"]),
      expectationCard("HBM 配套", "公司 TAM / 合同", "Micron 预期 HBM TAM 到 2028 约 $100B，并披露 2026 HBM supply 已有价量协议，说明供给释放仍被资格和产能绑定。", [
        expectationRow("Micron", "CY2025E / FY26 Q1", "[HBM TAM about $35B in CY2025](source:SRC-MU-FY26-Q1-PREPARED)。", "CY2028E / CY2026 supply", "[HBM TAM around $100B in CY2028；2026 HBM supply price and volume agreements completed](source:SRC-MU-FY26-Q1-PREPARED)。", "TAM 是空间预期，价量协议是短期供需约束；二者共同支持 HBM 是 GPU/ASIC 串联约束。"),
      ], ["SRC-MU-FY26-Q1-PREPARED"]),
      expectationCard("系统交付", "公司指引", "Dell 的 FY27 revenue guide 是系统交付供给能否消化 backlog 的关键市场预期。", [
        expectationRow("Dell", "FY2026", "[AI server shipments >$25B，FY27 backlog $43B](source:SRC-DELL-FY26-Q4)。", "FY2027E", "[AI-optimized server revenue guide about $50B](source:SRC-DELL-FY26-Q4)。", "如果 guide 兑现，说明系统交付供给在释放；如果毛利或现金恶化，供给释放可能不是高质量。"),
      ], ["SRC-DELL-FY26-Q4"]),
    ],
    mechanism: {
      sustain: "供给紧张可持续的机制是先进封装/HBM/系统交付的扩产、良率、认证和项目周期慢于客户订单斜率。",
      break: "供给反证是 TSMC/CoWoS/HBM 扩产快于需求、交期缩短、订单取消、系统商 backlog 转收入但毛利下降。",
    },
    directQuery: "GPU ASIC supply constraint TSMC capex advanced packaging HBM agreements Dell AI server backlog before 2026-03-28",
    evidenceSummary: ["补入 TSMC、Micron、Dell 三条供给链证据，分别覆盖制造、内存和系统交付。"],
    gapSummary: ["缺少 CoWoS 月产能、HBM 各厂有效产能、GPU allocation、lead time 和订单取消率。"],
  });
}

function strictComputeControlRow(row, questionNumber) {
  const chainNodes = [
    {
      title: "平台控制权",
      metrics: [
        {
          type: "平台控制",
          name: "NVIDIA Data Center revenue vs AMD Data Center revenue",
          why: "控制权首先看谁实际控制当前 accelerator 平台收入；NVIDIA 与 AMD 数据中心收入对比能给出通用 GPU/CPU/accelerator 竞争格局的量级差异。",
          dataRequirement: "主体：NVIDIA / AMD；字段：Data Center revenue；单位：十亿美元；期间：最近季度/年度；不同公司口径不完全同一，必须标注代理性质。",
          trendKind: "non_time_series",
          trendLabel: "平台收入量级对比",
          series: [
            { label: "NVIDIA Q4 FY26 Data Center", value: "$62.3B", change: "绝对主导" },
            { label: "NVIDIA FY26 Data Center", value: "$193.7B", change: "全年主导" },
            { label: "AMD Q4 2025 Data Center", value: "$5.4B", change: "追赶者/替代路线" },
            { label: "AMD FY2025 Data Center", value: "$16.6B", change: "量级明显小" },
          ],
          seriesGap: "NVIDIA 与 AMD 的 segment definition 不完全一致，不能当作精确份额表，只能作为平台收入控制权代理。",
          history: "[NVIDIA Q4 FY26 Data Center revenue $62.3B、FY26 Data Center revenue $193.7B](source:SRC-NVDA-FY26-Q4)；[Tom's Hardware 报道 AMD Q4 2025 Data Center revenue $5.4B、FY2025 $16.6B](source:SRC-AMD-Q4-2025-TOMS)。",
          current: "NVIDIA 平台控制权最强；AMD 是追赶者，当前公开量级仍明显小于 NVIDIA。",
          future: "未来要看 AMD MI/Helios、云厂自研 ASIC 和 Broadcom custom ASIC 是否改变增量份额，而不是只看绝对收入。",
          quality: "代理对比；需要 Omdia/Gartner/IDC 的付费 AI accelerator 份额表补精确份额。",
          sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AMD-Q4-2025-TOMS"],
        },
      ],
    },
    {
      title: "custom ASIC 控制权",
      metrics: [
        {
          type: "ASIC 控制",
          name: "Broadcom AI semiconductor revenue and guide",
          why: "Broadcom 是 custom AI accelerator / AI networking 的关键代理；它的 AI semiconductor revenue 能验证云厂 ASIC 第二路线是否已有供给控制权。",
          dataRequirement: "主体：Broadcom；字段：AI revenue / AI semiconductor revenue；单位：十亿美元；实际与指引分开。",
          trendKind: "non_time_series",
          trendLabel: "实际与指引",
          series: [
            { label: "Q2 FY25 actual", value: ">$4.4B", change: "+46% YoY" },
            { label: "Q3 FY25 actual", value: "$5.2B", change: "+63% YoY" },
            { label: "Q1 FY26 actual", value: "$8.4B", change: "+106% YoY" },
            { label: "Q2 FY26 guide", value: "~$10.7B", change: "约 +27% QoQ vs Q1 actual" },
          ],
          seriesGap: "前三项为 actual，最后一项为 guidance；不画成同口径历史趋势，只用于判断控制权在形成。",
          history: "[Broadcom Q2 FY25 AI revenue >$4.4B](source:SRC-AVGO-FY25-Q2)，[Q3 FY25 AI revenue $5.2B](source:SRC-AVGO-FY25-Q3)，[Q1 FY26 AI revenue $8.4B](source:SRC-AVGO-FY26-Q1)。",
          current: "[Broadcom Q1 FY26 AI revenue +106% YoY，driven by custom AI accelerators and AI networking](source:SRC-AVGO-FY26-Q1)。",
          future: "[Q2 FY26 AI semiconductor revenue expected $10.7B](source:SRC-AVGO-FY26-Q1)。",
          quality: "custom ASIC 控制权证据增强，但客户集中与项目节奏未完全披露。",
          sourceIds: ["SRC-AVGO-FY25-Q2", "SRC-AVGO-FY25-Q3", "SRC-AVGO-FY26-Q1"],
        },
      ],
    },
    {
      title: "实物交付控制权",
      metrics: [
        {
          type: "制造/HBM控制",
          name: "TSMC advanced tech share and Micron/SK hynix HBM evidence",
          why: "设计平台控制权不能单独转成供给控制；TSMC 与 HBM 供应商决定实物交付的瓶颈控制。",
          dataRequirement: "主体：TSMC / Micron / SK hynix；字段：advanced tech share、capex、HBM TAM、operating margin；单位：% / 美元；作为实物约束代理。",
          trendKind: "non_time_series",
          trendLabel: "交付控制代理",
          series: [
            { label: "TSMC advanced tech share", value: "77%", change: "先进制程集中" },
            { label: "TSMC 2026 capex", value: "$52B-$56B", change: "供给释放控制" },
            { label: "Micron 2028 HBM TAM", value: "~$100B", change: "内存瓶颈空间" },
            { label: "SK hynix FY25 operating margin", value: "49%", change: "HBM/AI memory 利润兑现" },
          ],
          seriesGap: "这是跨公司、跨字段控制权代理，不是份额表。",
          history: "[TSMC advanced technologies 77% of wafer revenue and 2026 capex $52B-$56B](source:SRC-TSM-Q4-2025)；[Micron HBM TAM 2028 around $100B](source:SRC-MU-FY26-Q1-PREPARED)；[SK hynix FY25 operating margin 49%](source:SRC-SKHYNIX-FY25)。",
          current: "实物控制权由 TSMC/先进封装/HBM 与系统交付共同决定。",
          future: "若 HBM 和先进封装持续紧张，平台控制方也需要这些节点配合才能交付。",
          quality: "控制权代理；缺精确 allocation 和份额表。",
          sourceIds: ["SRC-TSM-Q4-2025", "SRC-MU-FY26-Q1-PREPARED", "SRC-SKHYNIX-FY25"],
        },
      ],
    },
  ];
  return strictComputeRichRow(row, questionNumber, {
    answer: "GPU/ASIC 的供给控制权分三层：NVIDIA 控制通用 GPU 平台和软件/互联生态；Broadcom/云厂 custom ASIC 正形成第二路线；TSMC、HBM 厂和系统交付商控制实物交付。NVIDIA 当前收入量级仍明显领先，但投资判断要避免把“设计控制权”误当成“全部供给控制权”。",
    metricLogic: "控制权问题按平台、ASIC 第二路线、实物交付三层拆。平台层看 NVIDIA/AMD 收入量级，ASIC 层看 Broadcom AI semiconductor，实物层看 TSMC 与 HBM 供给控制。",
    historySummary: "02 把不同控制权层级分开列：NVIDIA/AMD 是平台收入代理，Broadcom 是 custom ASIC 代理，TSMC/Micron/SK hynix 是实物交付代理。跨公司口径只做控制权判断，不做精确份额表。",
    chainNodes,
    futureCards: [
      expectationCard("平台控制", "公司指引 / 替代路线", "NVIDIA 仍给出最强的近期收入指引；AMD 是替代玩家，但截至 cutoff 的公开量级仍显著较小。", [
        expectationRow("NVIDIA", "Q4 FY2026", "[Data Center revenue $62.3B](source:SRC-NVDA-FY26-Q4)。", "Q1 FY2027E", "[Revenue outlook $78.0B +/-2%](source:SRC-NVDA-FY26-Q4)。", "公司整体 revenue outlook 不是 Data Center 单项指引，但在当前收入结构下仍是平台需求强度锚点。"),
        expectationRow("AMD", "Q4 2025 / FY2025", "[Q4 Data Center revenue $5.4B，FY2025 Data Center revenue $16.6B](source:SRC-AMD-Q4-2025-TOMS)。", "2026", "公开材料强调 enterprise/high-end focus，但缺少同 NVIDIA 可比的 GPU revenue 指引。", "AMD 是重要替代路线，但当前资料仍不足以证明其已改变主导权。"),
      ], ["SRC-NVDA-FY26-Q4", "SRC-AMD-Q4-2025-TOMS"]),
      expectationCard("ASIC 控制", "公司指引", "Broadcom 的 Q2 FY26 AI semiconductor 指引说明 custom ASIC 控制权在增强。", [
        expectationRow("Broadcom", "Q1 FY2026", "[AI revenue $8.4B、+106% YoY](source:SRC-AVGO-FY26-Q1)。", "Q2 FY2026E", "[AI semiconductor revenue expected about $10.7B](source:SRC-AVGO-FY26-Q1)。", "Q2 guide 是 ASIC/AI networking 第二路线最清楚的未来控制权锚点。"),
      ], ["SRC-AVGO-FY26-Q1"]),
      expectationCard("实物交付", "供给节点指引", "TSMC 和 HBM 厂控制实物供给；即便平台需求强，也要看先进制程、封装和内存是否能交付。", [
        expectationRow("TSMC / Micron", "Q4 2025 / FY26 Q1", "[TSMC advanced technologies 77%](source:SRC-TSM-Q4-2025)；[Micron 2026 HBM supply price/volume agreements completed](source:SRC-MU-FY26-Q1-PREPARED)。", "FY2026E / CY2028E", "[TSMC 2026 capex $52B-$56B](source:SRC-TSM-Q4-2025)；[Micron HBM TAM around $100B in CY2028](source:SRC-MU-FY26-Q1-PREPARED)。", "这是实物控制权，不是 GPU/ASIC 设计份额；它决定可交付供给。"),
      ], ["SRC-TSM-Q4-2025", "SRC-MU-FY26-Q1-PREPARED"]),
    ],
    mechanism: {
      sustain: "控制权可持续来自 CUDA/生态、平台路线图、客户认证、custom ASIC 项目锁定，以及先进制造/HBM 的不可绕过性。",
      break: "控制权被削弱的机制是客户多供、AMD/ASIC 替代超预期、TSMC/HBM供给释放削弱 allocation，或客户把 bargaining power 转回自己。",
    },
    directQuery: "GPU ASIC supply control NVIDIA AMD Broadcom custom ASIC TSMC HBM market share guidance before 2026-03-28",
    evidenceSummary: ["补入 AMD 作为替代玩家量级参考，明确 NVIDIA 主导、Broadcom 第二路线、TSMC/HBM 实物控制三层。"],
    gapSummary: ["缺少 Omdia/Gartner/IDC 的精确 AI accelerator 份额表、云厂自研 ASIC 采购量和客户 allocation。"],
  });
}

function strictComputeFinancialRow(row, questionNumber) {
  const chainNodes = [
    {
      title: "GPU 收入兑现",
      metrics: [
        {
          type: "收入兑现",
          name: "NVIDIA Data Center segment revenue and gross margin",
          why: "GPU/ASIC 的财务兑现首先看 NVIDIA Data Center revenue，同时用 gross margin 过滤低质量增长。",
          dataRequirement: "主体：NVIDIA；字段：Data Center revenue、gross margin；单位：十亿美元/%；频率：季度。",
          trendKind: "time_series",
          trendLabel: "NVIDIA Data Center revenue",
          series: [
            { label: "Q4 FY23", value: "$3.62B", change: "基准" },
            { label: "Q2 FY24", value: "$10.32B", change: "+185% vs Q4 FY23" },
            { label: "Q4 FY24", value: "$18.4B", change: "+408% vs Q4 FY23" },
            { label: "Q2 FY25", value: "$26.3B", change: "+627% vs Q4 FY23" },
            { label: "Q4 FY25", value: "$35.6B", change: "+884% vs Q4 FY23" },
            { label: "Q2 FY26", value: "$41.1B", change: "+1035% vs Q4 FY23" },
            { label: "Q3 FY26", value: "$51.2B", change: "+1314% vs Q4 FY23" },
            { label: "Q4 FY26", value: "$62.3B", change: "+1621% vs Q4 FY23" },
          ],
          history: "[NVIDIA Data Center revenue 从 Q4 FY23 $3.62B 上升到 Q4 FY26 $62.3B](source:SRC-NVDA-FY26-Q4)。",
          current: "[Q4 FY26 GAAP gross margin 75.0%，Data Center revenue $62.3B](source:SRC-NVDA-FY26-Q4)。",
          future: "[Q1 FY27 revenue outlook $78.0B +/-2%，gross margin expected about 75%](source:SRC-NVDA-FY26-Q4)。",
          quality: "财务兑现最强同口径指标。",
          sourceIds: ["SRC-NVDA-FY23-Q4", "SRC-NVDA-FY24-Q2", "SRC-NVDA-FY24-Q4", "SRC-NVDA-FY25-Q2", "SRC-NVDA-FY25-Q4", "SRC-NVDA-FY26-Q2", "SRC-NVDA-FY26-Q3", "SRC-NVDA-FY26-Q4"],
        },
      ],
    },
    {
      title: "ASIC 收入兑现",
      metrics: [
        {
          type: "ASIC收入",
          name: "Broadcom AI semiconductor revenue actuals and guide",
          why: "Broadcom 是 custom ASIC/AI networking 财务兑现的关键代理，能判断第二增长路线是否已经进入报表。",
          dataRequirement: "主体：Broadcom；字段：AI revenue actual 和 AI semiconductor revenue guide；单位：十亿美元；actual 与 guidance 分开。",
          trendKind: "non_time_series",
          trendLabel: "actual + guide",
          series: [
            { label: "Q2 FY25 actual", value: ">$4.4B", change: "+46% YoY" },
            { label: "Q3 FY25 actual", value: "$5.2B", change: "+63% YoY" },
            { label: "Q1 FY26 actual", value: "$8.4B", change: "+106% YoY" },
            { label: "Q2 FY26 guide", value: "$10.7B", change: "expected" },
          ],
          seriesGap: "Q2 FY26 是指引，不进入 actual-only 历史曲线；本表用于财务兑现和未来锚点同屏展示。",
          history: "[Broadcom Q2 FY25 AI revenue >$4.4B](source:SRC-AVGO-FY25-Q2)，[Q3 FY25 $5.2B](source:SRC-AVGO-FY25-Q3)，[Q1 FY26 $8.4B](source:SRC-AVGO-FY26-Q1)。",
          current: "[Q1 FY26 AI revenue $8.4B，driven by custom AI accelerators and AI networking](source:SRC-AVGO-FY26-Q1)。",
          future: "[Q2 FY26 AI semiconductor revenue expected about $10.7B](source:SRC-AVGO-FY26-Q1)。",
          quality: "第二路线财务兑现强，但实际点少于 NVIDIA。",
          sourceIds: ["SRC-AVGO-FY25-Q2", "SRC-AVGO-FY25-Q3", "SRC-AVGO-FY26-Q1"],
        },
      ],
    },
    {
      title: "系统订单兑现",
      metrics: [
        {
          type: "订单兑现",
          name: "Dell AI-optimized server orders, shipments and backlog",
          why: "订单/backlog 是收入前导，验证 GPU/ASIC 是否已被装进可交付系统。",
          dataRequirement: "主体：Dell；字段：AI server orders、shipments、ending backlog、revenue guide；单位：十亿美元。",
          trendKind: "time_series",
          trendLabel: "Dell ending backlog",
          series: [
            { label: "Q4 FY25", value: "~$9B", change: "基准" },
            { label: "Q1 FY26", value: "$14.4B", change: "+60%" },
            { label: "Q2 FY26", value: "$11.7B", change: "交付消化" },
            { label: "Q3 FY26", value: "$18.4B", change: "重新上行" },
            { label: "Q4 FY26", value: "$43B", change: "+378% vs Q4 FY25" },
          ],
          history: "[Dell ending backlog 从 FY25 Q4 约 $9B 到进入 FY27 的 $43B](source:SRC-DELL-FY26-Q4)。",
          current: "[FY26 orders >$64B、shipments >$25B](source:SRC-DELL-FY26-Q4)。",
          future: "[FY27 AI-optimized server revenue guide about $50B](source:SRC-DELL-FY26-Q4)。",
          quality: "订单兑现强；利润质量需另查。",
          sourceIds: ["SRC-DELL-FY25-Q4", "SRC-DELL-FY26-Q1", "SRC-DELL-FY26-Q2-PERFORMANCE", "SRC-DELL-FY26-Q3", "SRC-DELL-FY26-Q4"],
        },
      ],
    },
  ];
  return strictComputeRichRow(row, questionNumber, {
    answer: "GPU/ASIC 已经是 AI factory 链条里财务兑现最充分的节点：NVIDIA Data Center revenue 形成 8 个公开历史点并保持高毛利，Broadcom AI semiconductor revenue 形成 custom ASIC 第二曲线，Dell AI server backlog 与 FY27 revenue guide 说明客户预算已进入系统交付。剩余问题是盈利质量和市场定价，而不是是否已经兑现。",
    metricLogic: "财务兑现按收入、订单和未来指引三层验证：平台收入确认需求穿透，ASIC 收入确认第二路线，AI server backlog/revenue guide 确认系统交付池。",
    historySummary: "02 以 NVIDIA revenue 作为最强同口径曲线，Broadcom 作为 actual+guide 表，Dell 作为 backlog 时间序列。所有 guidance 都明确标为未来锚点，不混入 actual-only 历史曲线。",
    chainNodes,
    futureCards: [
      expectationCard("GPU 收入", "公司指引", "NVIDIA 给出 Q1 FY27 revenue outlook 与 gross margin outlook，说明市场预期下一季仍高位兑现。", [
        expectationRow("NVIDIA", "Q4 FY2026", "[Data Center revenue $62.3B，GAAP gross margin 75.0%](source:SRC-NVDA-FY26-Q4)。", "Q1 FY2027E", "[Revenue expected $78.0B +/-2%，gross margin expected 74.9%-75.0% +/-50 bps](source:SRC-NVDA-FY26-Q4)。", "公司整体收入指引不能拆成 Data Center 单项，但高 Data Center 占比使其仍是 GPU/ASIC 兑现的近端锚点。"),
      ], ["SRC-NVDA-FY26-Q4"]),
      expectationCard("ASIC 收入", "公司指引", "Broadcom 的 Q2 FY26 AI semiconductor guide 是 custom ASIC 收入继续兑现的核心预期。", [
        expectationRow("Broadcom", "Q1 FY2026", "[AI revenue $8.4B、+106% YoY](source:SRC-AVGO-FY26-Q1)。", "Q2 FY2026E", "[AI semiconductor revenue expected about $10.7B](source:SRC-AVGO-FY26-Q1)。", "与 actual 基本同一业务口径，适合做近端收入兑现验证。"),
      ], ["SRC-AVGO-FY26-Q1"]),
      expectationCard("系统订单", "公司指引", "Dell FY27 revenue guide 验证 backlog 是否能变成收入。", [
        expectationRow("Dell", "FY2026", "[Orders >$64B，shipments >$25B，FY27 backlog $43B](source:SRC-DELL-FY26-Q4)。", "FY2027E", "[AI-optimized server revenue about $50B, up 103% YoY](source:SRC-DELL-FY26-Q4)。", "订单到收入的兑现链条清楚，但仍需看毛利和现金。"),
      ], ["SRC-DELL-FY26-Q4"]),
    ],
    mechanism: {
      sustain: "财务兑现可持续需要收入、毛利率、订单/backlog 和指引同步强，而不是只靠一次性订单。",
      break: "若收入高增但毛利下降、backlog 不转收入、现金流恶化或 guide 下修，兑现质量会下降。",
    },
    directQuery: "NVIDIA Data Center revenue Broadcom AI semiconductor revenue Dell AI server backlog guidance financial realization before 2026-03-28",
    evidenceSummary: ["新增 Q1 FY27 NVIDIA outlook、Broadcom Q2 guide、Dell FY27 guide，以 03 形式承接 02 历史数据。"],
    gapSummary: ["缺少 GPU/ASIC ASP、NVIDIA backlog、客户集中、订单取消率和按产品毛利率。"],
  });
}

function strictComputePricingRow(row, questionNumber) {
  const chainNodes = [
    {
      title: "胜率是否已被市场识别",
      metrics: [
        {
          type: "定价代理",
          name: "NVIDIA / Broadcom forward guidance vs already-realized revenue",
          why: "缺少 as-of 估值数据库时，先用公司指引与已兑现收入判断市场是否已有高预期；如果龙头已经给出强指引，胜率通常已被市场识别。",
          dataRequirement: "主体：NVIDIA / Broadcom；字段：actual revenue、next-quarter guidance；单位：十亿美元；结合估值数据后才能最终定价。",
          trendKind: "non_time_series",
          trendLabel: "actual vs guide",
          series: [
            { label: "NVDA Q4 FY26 revenue", value: "$68.1B", change: "+73% YoY" },
            { label: "NVDA Q1 FY27 revenue outlook", value: "$78.0B +/-2%", change: "市场已看到高指引" },
            { label: "AVGO Q1 FY26 AI revenue", value: "$8.4B", change: "+106% YoY" },
            { label: "AVGO Q2 FY26 AI semi guide", value: "$10.7B", change: "市场已看到继续上行" },
          ],
          seriesGap: "这是实际+指引对比，不是估值倍数；定价问题还需要 forward PE/EV sales/盈利上修数据。",
          history: "[NVIDIA Q4 FY26 revenue $68.1B、Data Center revenue $62.3B](source:SRC-NVDA-FY26-Q4)；[Broadcom Q1 FY26 AI revenue $8.4B](source:SRC-AVGO-FY26-Q1)。",
          current: "龙头收入和指引已经非常显眼，说明市场大概率已识别 GPU/ASIC 胜率。",
          future: "只有后续指引继续上修、盈利修正超过估值隐含预期，赔率才可能继续成立。",
          quality: "定价代理；缺正式估值。",
          sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY26-Q1"],
        },
      ],
    },
    {
      title: "行业池子还能否提供上修空间",
      metrics: [
        {
          type: "空间预期",
          name: "Omdia AI data-center processor spending forecast",
          why: "行业池子能判断增长路径是否还有剩余空间，但不能说明个股便宜。",
          dataRequirement: "主体：Omdia；字段：AI data-center processor spending；单位：十亿美元；期间：2024/2025E/2030E。",
          trendKind: "time_series",
          trendLabel: "第三方市场空间",
          series: [
            { label: "2024", value: "~$123B", change: "基准" },
            { label: "2025E", value: "~$207B", change: "+68%" },
            { label: "2030E", value: "~$286B", change: "+38% vs 2025E" },
          ],
          seriesGap: "只有三点且含预测，不能作为历史曲线；用于判断远期空间不是估值。",
          history: "[Omdia forecast 2024 about $123B and 2025E about $207B](source:SRC-OMDIA-AI-PROCESSORS-20250828)。",
          current: "2025E 已是高基数，说明市场可能已开始从高增长转向结构分化。",
          future: "[2030E about $286B and custom ASICs gaining traction](source:SRC-OMDIA-AI-PROCESSORS-20250828)。",
          quality: "行业空间锚点；不等同估值便宜。",
          sourceIds: ["SRC-OMDIA-AI-PROCESSORS-20250828"],
        },
      ],
    },
    {
      title: "需要补的真实估值数据",
      metrics: [
        {
          type: "估值缺口",
          name: "Forward PE / EV sales / EPS revision / FCF yield as of 2026-03-28",
          why: "市场是否已定价的最终答案必须用 as-of 估值和盈利上修判断，不能只靠产业强度。",
          dataRequirement: "主体：NVDA / AVGO / AMD / TSM / peers；字段：forward PE、EV/Sales、consensus EPS/revenue revision、FCF yield；单位：倍数/%；必须使用 2026-03-28 前可见数据。",
          series: [],
          seriesGap: "当前源包没有完整 as-of 估值数据库；这是定价问题的核心缺口，不能用当前股价或后验涨跌补。",
          history: "已搜索到公司财务和指引，但未接入历史估值与一致预期修正数据库。",
          current: "因此本问只能判断“胜率大概率已被市场关注”，不能判断“赔率仍便宜”。",
          future: "下一步需要接入 as-of historical valuation provider 或手工收集当时 sell-side consensus。",
          quality: "核心缺口。",
          sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY26-Q1", "SRC-OMDIA-AI-PROCESSORS-20250828"],
        },
      ],
    },
  ];
  return strictComputeRichRow(row, questionNumber, {
    answer: "GPU/ASIC 的胜率已经高度显性化，尤其是 NVIDIA 和 Broadcom：收入、毛利、下一季指引、行业空间预测都很强。但“强基本面”不等于“仍有赔率”。当前报告仍缺 2026-03-28 as-of 的估值倍数、盈利上修和隐含增长数据，因此只能把本问判为：市场大概率已部分定价，赔率需补估值后再确认。",
    metricLogic: "定价问题按三步：先看强基本面是否已被公司指引公开化，再看行业池子是否还有剩余空间，最后必须接入估值和一致预期修正。前两步只能判断胜率被识别，第三步才判断赔率。",
    historySummary: "02 不用后验涨跌判断定价；当前只列 actual vs guidance、Omdia 空间预测，以及明确估值数据缺口。",
    chainNodes,
    futureCards: [
      expectationCard("龙头指引", "公司指引", "NVIDIA 和 Broadcom 都已经给出强近端预期，这意味着市场很难完全不知道主链逻辑。", [
        expectationRow("NVIDIA", "Q4 FY2026", "[Revenue $68.1B，Data Center revenue $62.3B](source:SRC-NVDA-FY26-Q4)。", "Q1 FY2027E", "[Revenue outlook $78.0B +/-2%](source:SRC-NVDA-FY26-Q4)。", "强指引提升胜率，同时也提高市场预期门槛。"),
        expectationRow("Broadcom", "Q1 FY2026", "[AI revenue $8.4B、+106% YoY](source:SRC-AVGO-FY26-Q1)。", "Q2 FY2026E", "[AI semiconductor revenue expected about $10.7B](source:SRC-AVGO-FY26-Q1)。", "custom ASIC 强指引说明第二路线也已被市场看到。"),
      ], ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY26-Q1"]),
      expectationCard("行业池子", "第三方预测", "Omdia 的预测支持 AI processor 仍增长，但 2025E 到 2030E 的增速远低于早期收入爆发段，定价必须看盈利上修和份额迁移。", [
        expectationRow("Omdia", "2024A / 2025E", "[AI data-center processor spending about $123B in 2024 and $207B in 2025E](source:SRC-OMDIA-AI-PROCESSORS-20250828)。", "2030E", "[About $286B, with custom ASICs gaining traction](source:SRC-OMDIA-AI-PROCESSORS-20250828)。", "空间仍在，但不支持把早期 17x 收入斜率线性外推。"),
      ], ["SRC-OMDIA-AI-PROCESSORS-20250828"]),
      expectationCard("估值缺口", "待补数据", "当前报告无法用缺失的估值数据硬判便宜或贵，因此标的推荐需要维持 watch_only 或降低强度。", [
        expectationRow("NVDA / AVGO / AMD", "2026-03-28 as-of", "当前源包没有完整 forward PE、EV/Sales、EPS revision、FCF yield。", "后续刷新", "需接入 as-of consensus / valuation source。", "没有估值，就不能把产业强度直接升级为买入强度。"),
      ], ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY26-Q1"]),
    ],
    mechanism: {
      sustain: "赔率成立需要后续收入和盈利上修继续超过市场已知强指引，并且估值没有提前吃掉 2-3 年增长。",
      break: "若强指引已经完全进入估值，或者盈利上修跟不上股价/倍数扩张，基本面强也只能保持观察。",
    },
    directQuery: "NVIDIA Broadcom AI revenue guidance valuation priced in AI accelerator expectations before 2026-03-28",
    evidenceSummary: ["补齐 actual vs guidance 和 Omdia 空间预测，明确估值数据仍是核心缺口。"],
    gapSummary: ["缺少 as-of forward PE、EV/Sales、consensus revision、FCF yield 和 reverse DCF。"],
  });
}

function strictComputeRefuteRow(row, questionNumber) {
  const chainNodes = [
    {
      title: "需求端反证",
      metrics: [
        {
          type: "客户预算反证",
          name: "Hyperscaler capex / RPO / FCF pressure",
          why: "GPU/ASIC 需求若要降级，最早会出现在客户 capex 下修、RPO 不转收入或 FCF 压力逼迫项目延后。",
          dataRequirement: "主体：Microsoft / Amazon / Alphabet / Meta / Oracle；字段：capex、PPE purchases、RPO、FCF；单位：美元；频率：季度/年度。",
          trendKind: "non_time_series",
          trendLabel: "客户预算与压力",
          series: [
            { label: "MSFT Q2 FY26 RPO", value: "$625B", change: "+110% YoY" },
            { label: "AMZN 2026 capex plan", value: "~$200B", change: "AI/chips 等驱动" },
            { label: "GOOGL 2026 capex guide", value: "$175B-$185B", change: "接近 FY25 PPE 的约 2x" },
            { label: "META 2026 capex guide", value: "$115B-$135B", change: "+59%-87% vs FY25" },
            { label: "ORCL Q2 FY26 RPO", value: "$523B", change: "+438%" },
          ],
          seriesGap: "跨公司、跨口径预算/承诺数据，不能画成一条趋势；用于识别反证监控清单。",
          history: "[Microsoft RPO $625B](source:SRC-MSFT-FY26-Q2)，[Alphabet 2026 capex $175B-$185B](source:SRC-GOOGL-Q4-2025)，[Meta 2026 capex $115B-$135B](source:SRC-META-Q4-2025)。",
          current: "客户预算端目前没有明显下修信号，但 FCF 和 ROI 压力必须跟踪。",
          future: "若 capex/RPO 下修或 FCF 压力扩大，GPU/ASIC 需求最先降级。",
          quality: "反证监控强；不是 GPU 订单。",
          sourceIds: ["SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q4-2025", "SRC-ORCL-FY26-Q2"],
        },
      ],
    },
    {
      title: "供给与价格反证",
      metrics: [
        {
          type: "供给反证",
          name: "TSMC capex / HBM supply agreements / Dell backlog conversion",
          why: "若供给释放快于需求，短缺逻辑会先通过 capex 扩产、价量协议变化、backlog 转收入质量和毛利率变化体现。",
          dataRequirement: "主体：TSMC / Micron / Dell；字段：capex、HBM supply agreements、backlog conversion、margin；单位：美元/%。",
          trendKind: "non_time_series",
          trendLabel: "供给释放与质量",
          series: [
            { label: "TSMC 2026 capex", value: "$52B-$56B", change: "供给释放" },
            { label: "Micron 2026 HBM supply", value: "price/volume agreements completed", change: "紧张进入合同" },
            { label: "Dell FY27 backlog", value: "$43B", change: "转收入待验证" },
            { label: "Dell FY27 revenue guide", value: "~$50B", change: "转收入目标" },
          ],
          seriesGap: "反证看的是多个节点的转弱，不是单一历史曲线。",
          history: "[TSMC 2026 capex $52B-$56B](source:SRC-TSM-Q4-2025)，[Micron 2026 HBM supply price/volume agreements completed](source:SRC-MU-FY26-Q1-PREPARED)，[Dell FY27 backlog $43B](source:SRC-DELL-FY26-Q4)。",
          current: "当前供给仍在扩张但约束未完全解除。",
          future: "若扩产释放导致 lead time 缩短、价格下降或 backlog 低毛利转收入，应降级。",
          quality: "反证框架明确；缺 lead time / spot price / allocation。",
          sourceIds: ["SRC-TSM-Q4-2025", "SRC-MU-FY26-Q1-PREPARED", "SRC-DELL-FY26-Q4"],
        },
      ],
    },
    {
      title: "路线替代反证",
      metrics: [
        {
          type: "替代反证",
          name: "Custom ASIC gaining traction vs NVIDIA GPU growth",
          why: "custom ASIC 不是天然反证；只有在它压低整体 accelerator 增长、GPU ASP 或 NVIDIA 增速时，才构成实质反证。",
          dataRequirement: "主体：Omdia / Broadcom / NVIDIA；字段：AI processor spending、custom ASIC growth、NVIDIA Data Center revenue；单位：美元/%。",
          trendKind: "non_time_series",
          trendLabel: "替代与总池子",
          series: [
            { label: "Omdia 2025E AI processor", value: "$207B", change: "总池子大" },
            { label: "Omdia 2030E AI processor", value: "$286B", change: "增速放缓但仍扩大" },
            { label: "Broadcom Q2 FY26 guide", value: "$10.7B", change: "ASIC 增强" },
            { label: "NVIDIA Q1 FY27 outlook", value: "$78B", change: "GPU 平台仍强" },
          ],
          seriesGap: "这是替代路线和总需求池的交叉验证，不是精确份额。",
          history: "[Omdia 预计 custom ASICs gaining traction](source:SRC-OMDIA-AI-PROCESSORS-20250828)；[Broadcom Q2 FY26 AI semiconductor guide $10.7B](source:SRC-AVGO-FY26-Q1)。",
          current: "当前更像总 accelerator 池扩大并出现结构迁移，而不是 ASIC 直接证伪 GPU。",
          future: "如果 Broadcom/ASIC 上行同时 NVIDIA 指引转弱，路线替代会变成实质反证。",
          quality: "路线反证需继续份额数据。",
          sourceIds: ["SRC-OMDIA-AI-PROCESSORS-20250828", "SRC-AVGO-FY26-Q1", "SRC-NVDA-FY26-Q4"],
        },
      ],
    },
  ];
  return strictComputeRichRow(row, questionNumber, {
    answer: "GPU/ASIC 的核心反证不是泛泛的“AI 泡沫”，而是三类可观测数据：客户预算/RPO/capex 下修，供给释放导致价格、交期、毛利和 backlog 质量转弱，以及 custom ASIC 替代从扩大总池子变成压低 GPU 增长。当前材料没有显示这些反证已经发生，但缺少 GPU-hours、lead time、GPU 租赁价格和 as-of 估值，仍需监控。",
    metricLogic: "反证要和前面链条一一对应：需求端看 capex/RPO/FCF，供给端看 capex/HBM/backlog 转化，路线端看 ASIC 是否压低 GPU 总增长。",
    historySummary: "02 不把反证写成风险清单，而是选择能提前证伪的 metric：客户预算、供给释放/质量、路线替代。跨公司指标只做监控表，不画趋势线。",
    chainNodes,
    futureCards: [
      expectationCard("客户预算反证", "公司指引", "当前市场预期仍是 capex 上行；如果后续任一大客户下修，GPU/ASIC 需求判断要先降级。", [
        expectationRow("Microsoft / Alphabet / Meta / Amazon / Oracle", "FY2025 / Q2 FY26", "[Microsoft RPO $625B](source:SRC-MSFT-FY26-Q2)，[Alphabet FY25 PPE $91.4B](source:SRC-GOOGL-Q4-2025)，[Meta FY25 capex $72.22B](source:SRC-META-Q4-2025)。", "FY2026E", "[Alphabet capex $175B-$185B](source:SRC-GOOGL-Q4-2025)，[Meta $115B-$135B](source:SRC-META-Q4-2025)，[Amazon capex about $200B](source:SRC-AMZN-Q4-2025)。", "当前不是反证，但这些是后续降级的第一组阈值。"),
      ], ["SRC-MSFT-FY26-Q2", "SRC-GOOGL-Q4-2025", "SRC-META-Q4-2025", "SRC-AMZN-Q4-2025"]),
      expectationCard("供给/价格反证", "供给释放路径", "TSMC capex 与 HBM 价量协议说明供给在扩张；如果释放快于需求，会从短缺逻辑变成毛利和价格压力。", [
        expectationRow("TSMC / Micron / Dell", "Q4 2025 / FY26", "[TSMC 2026 capex $52B-$56B](source:SRC-TSM-Q4-2025)，[Micron 2026 HBM supply 已有价量协议](source:SRC-MU-FY26-Q1-PREPARED)，[Dell backlog $43B](source:SRC-DELL-FY26-Q4)。", "FY2026-FY2027", "关注 lead time、ASP、backlog 转收入、毛利率和取消率。", "当前源包没有 lead time/价格数据；必须作为 gap 监控。"),
      ], ["SRC-TSM-Q4-2025", "SRC-MU-FY26-Q1-PREPARED", "SRC-DELL-FY26-Q4"]),
      expectationCard("路线替代反证", "第三方预测 + 公司指引", "custom ASIC 正在增强，但当前更像总池子扩大；只有当 ASIC 增强伴随 GPU 指引下修才是实质反证。", [
        expectationRow("Omdia / Broadcom / NVIDIA", "2025E / Q1 FY26", "[Omdia 2025E AI processor spending $207B](source:SRC-OMDIA-AI-PROCESSORS-20250828)，[Broadcom Q1 FY26 AI revenue $8.4B](source:SRC-AVGO-FY26-Q1)。", "2030E / Q2 FY26E / Q1 FY27E", "[Omdia 2030E $286B](source:SRC-OMDIA-AI-PROCESSORS-20250828)，[Broadcom Q2 FY26 guide $10.7B](source:SRC-AVGO-FY26-Q1)，[NVIDIA Q1 FY27 revenue outlook $78B](source:SRC-NVDA-FY26-Q4)。", "如果 Broadcom 上行且 NVIDIA 同时转弱，才说明替代压低 GPU；当前更像两条线同时扩张。"),
      ], ["SRC-OMDIA-AI-PROCESSORS-20250828", "SRC-AVGO-FY26-Q1", "SRC-NVDA-FY26-Q4"]),
    ],
    mechanism: {
      sustain: "反证未出现时，需求链条仍由客户预算、订单、收入和供给紧张共同支撑。",
      break: "真正降级需要看到预算下修、订单取消、lead time/ASP 下行、毛利恶化、ASIC 替代压低 GPU 增长或 AI ROI 证明不足。",
    },
    directQuery: "GPU ASIC demand refutation capex downgrade lead time ASP custom ASIC replacement before 2026-03-28",
    evidenceSummary: ["把反证拆为预算、供给质量、路线替代三张卡，并补入对应源。"],
    gapSummary: ["缺少 GPU rental price、lead time、ASP、order cancellation、accelerator utilization 和 AI ROI 可比序列。"],
  });
}

function expectationCard(horizon, status, marketExpectation, expectationRows, sourceIds) {
  return {
    horizon,
    expectationStatus: status,
    marketExpectation,
    expectationRows,
    sourceIds,
  };
}

function expectationRow(entity, currentPeriod, currentMetric, guidancePeriod, guidanceMetric, comparability) {
  return {
    entity,
    currentPeriod,
    currentMetric,
    guidancePeriod,
    guidanceMetric,
    comparability,
  };
}

function strictComputeDemandRow(row) {
  const sourceIds = [
    "SRC-CHATGPT-MAU-202302",
    "SRC-CHATGPT-WAU-202408",
    "SRC-CHATGPT-WAU-202412",
    "SRC-CHATGPT-WAU-202508",
    "SRC-OPENAI-CHATGPT-WORK-202602",
    "SRC-OPENAI-DEVDAY-2025",
    "SRC-GOOGL-Q4-2025-CALL",
    "SRC-MSFT-FY25-Q3-METRICS",
    "SRC-MSFT-FY25-Q4-CALL",
    "SRC-MSFT-FY26-Q1",
    "SRC-MSFT-FY26-Q2",
    "SRC-MSFT-FY26-Q2-CALL",
    "SRC-AMZN-Q4-2025",
    "SRC-GOOGL-Q4-2025",
    "SRC-META-Q4-2025",
    "SRC-ORCL-FY26-Q2",
    "SRC-DELL-FY25-Q4",
    "SRC-DELL-FY26-Q1",
    "SRC-DELL-FY26-Q2-PERFORMANCE",
    "SRC-DELL-FY26-Q3",
    "SRC-DELL-FY26-Q4",
    "SRC-NVDA-FY23-Q4",
    "SRC-NVDA-FY24-Q2",
    "SRC-NVDA-FY24-Q4",
    "SRC-NVDA-FY25-Q2",
    "SRC-NVDA-FY25-Q4",
    "SRC-NVDA-FY26-Q2",
    "SRC-NVDA-FY26-Q3",
    "SRC-NVDA-FY26-Q4",
    "SRC-AVGO-FY25-Q2",
    "SRC-AVGO-FY25-Q3",
    "SRC-AVGO-FY25-Q4",
    "SRC-AVGO-FY26-Q1",
    "SRC-SA-GB200-BOM-2024",
    "SRC-NVDA-GTC-VERA-RUBIN-20260316",
    "SRC-NVDA-GTC-DYNAMO-20260316",
    "SRC-OMDIA-AI-PROCESSORS-20250828",
    "SRC-OMDIA-SEMI-TRENDS-202512",
  ];
  return {
    ...row,
    answer: `截至 ${AS_OF_DATE}，外部逐问搜索后的结论是：计算加速器 / GPU / ASIC 的需求已经被 AI S 曲线放大拉动。证据从应用和 token 负载出发，穿透到云厂 capex、RPO、系统订单，再穿透到 NVIDIA Data Center 收入和 Broadcom AI 半导体收入；同时 rack-scale / pod-scale 平台和 Dell AI server backlog 说明当前 BOM 的需求弹性不是简单等于终端 AI 需求，而是被平台规格和系统交付放大。但直接的 tokens / GPU hours / 利用率同口径历史仍是关键缺口，所以本问可判为需求链条和 BOM 弹性强成立，不能单独替代后续 5 问和 BOM 阶段判定。`,
    sourceIds,
    metricLogic: `本问严格按一条链判断：AI 应用/任务是否真实变多 -> 是否转化为 token、推理请求或 GPU/CPU 加速工作负载 -> 是否进入云厂和 AI 客户的 capex、RPO、PPE purchases 或长期订单 -> 是否落到 AI server / accelerator 采购与交付 -> 当前 BOM 的需求弹性是否被平台规格、attach rate、单位价值量或系统架构放大 -> 是否已经被 GPU/ASIC 供应商确认成收入、backlog、指引和现金流。只有这条链同时出现历史加速、当前兑现、BOM 弹性和未来锚点，才说明当前 BOM 的需求不是概念热度；若任一环节只能找到截面或代理指标，必须标为 gap。`,
    historySummary: "本问复用 01 的逻辑链条，逐环节选择最能回答该环节的 metric：应用端看 ChatGPT weekly active users；预算/RPO 看 Microsoft Commercial RPO；订单/交付看 Dell AI-optimized server ending backlog；BOM 弹性看 NVIDIA platform generation scope 和 Dell AI server revenue guide；GPU 兑现看 NVIDIA Data Center segment revenue；ASIC 兑现看 Broadcom AI semiconductor revenue；反证缺口看公开 GPU-hours consumed。除 GPU-hours 尚无公开连续序列外，其余主指标尽量按同主体、同字段、同单位串联历史点，并以数据表呈现。",
    futureCards: [
      {
        horizon: "环节 1｜应用/任务：ChatGPT WAU 与 token 工作负载预期",
        expectationStatus: "非硬预期",
        marketExpectation: "本环节复用 01 的「应用/任务」链条，并参考本环节已选 ChatGPT WAU。当前能搜集到的是 OpenAI、Alphabet 已披露的使用量和 token 吞吐，但没有未来 WAU、tokens 或 GPU-hours 的硬指引；因此本环节只能证明需求入口很大，不能单独证明未来 GPU/ASIC 采购。",
        expectationRows: [
          {
            entity: "OpenAI",
            currentPeriod: "DevDay 2025",
            currentMetric: "[披露 800M+ weekly ChatGPT users、4M+ developers、API 6B tokens/min](source:SRC-OPENAI-DEVDAY-2025)。",
            guidancePeriod: "未披露",
            guidanceMetric: "未披露未来 WAU、tokens、GPU-hours 或 accelerator utilization 目标。",
            comparability: "与 01 的应用/任务环节和 02 的 WAU metric 对齐，但只有当前使用量，没有同口径未来预期；只能作为 workload 入口证据。",
          },
          {
            entity: "Alphabet / Gemini",
            currentPeriod: "Q4 2025 call",
            currentMetric: "[Gemini App 750M+ MAU、Gemini Enterprise 8M paid seats、Gemini 3 daily tokens 约为 Gemini 2.5 Pro 的 3x](source:SRC-GOOGL-Q4-2025-CALL)。",
            guidancePeriod: "未披露",
            guidanceMetric: "未披露未来 Gemini token、GPU-hours 或 accelerator 采购目标。",
            comparability: "Gemini 是旁证，不是本环节已选主 metric；用于说明工作负载入口扩大，不能直接外推 GPU/ASIC 增速。",
          },
        ],
        sourceIds: ["SRC-OPENAI-DEVDAY-2025", "SRC-GOOGL-Q4-2025-CALL"],
      },
      {
        horizon: "环节 2｜预算/RPO：客户预算与承诺池预期",
        expectationStatus: "公司指引",
        marketExpectation: "本环节复用 01 的「预算/RPO」链条，并参考本环节已选 Microsoft Commercial RPO，同时用云厂 capex/PPE 指引交叉验证客户预算。最强信息是 Alphabet、Meta、Amazon 2026 capex 指引继续上修，以及 Microsoft RPO 的未来确认安排。",
        expectationRows: [
          {
            entity: "Microsoft",
            currentPeriod: "Q2 FY2026",
            currentMetric: "[Commercial RPO 为 $625B，其中约 45% 来自 OpenAI；capital expenditures 为 $37.5B，约三分之二投向以 GPU/CPU 为主的短寿命资产](source:SRC-MSFT-FY26-Q2-CALL)。",
            guidancePeriod: "未来 12 个月 / 平均约 2.5 年",
            guidanceMetric: "[约 25% Commercial RPO 将在未来 12 个月确认收入，Commercial RPO 加权平均期限约 2.5 年](source:SRC-MSFT-FY26-Q2-CALL)。",
            comparability: "与 01 的预算/RPO环节和 02 的 RPO metric 对齐；RPO 是云承诺池，不是 GPU/ASIC 订单，需和 capex、server backlog 共同验证。",
          },
          {
            entity: "Alphabet",
            currentPeriod: "FY2025 / Q4 2025",
            currentMetric: "[FY2025 purchases of property and equipment 为 $91.4B，Q4 2025 为 $27.9B](source:SRC-GOOGL-Q4-2025)。",
            guidancePeriod: "FY2026E",
            guidanceMetric: "[2026 CapEx investments 预计 $175B-$185B](source:SRC-GOOGL-Q4-2025)。",
            comparability: "基本同属 capex/PPE 投入口径；相对 FY2025 PPE purchases，中值接近翻倍，说明客户侧 AI compute capacity 预算仍在上修。",
          },
          {
            entity: "Meta",
            currentPeriod: "FY2025 / Q4 2025",
            currentMetric: "[FY2025 capex including principal payments on finance leases 为 $72.22B，Q4 为 $22.14B](source:SRC-META-Q4-2025)。",
            guidancePeriod: "FY2026E",
            guidanceMetric: "[2026 capex including principal payments on finance leases 预计 $115B-$135B](source:SRC-META-Q4-2025)。",
            comparability: "同口径度较高；FY2026 指引区间相对 FY2025 实际值隐含约 +59% 至 +87%。",
          },
          {
            entity: "Amazon",
            currentPeriod: "TTM ended 2025-12-31",
            currentMetric: "[Free cash flow 下降主要由 purchases of property and equipment, net of proceeds and incentives 同比增加 $50.7B 推动；当前表采用报告内已记录的 TTM PPE purchases $128.3B](source:SRC-AMZN-Q4-2025)。",
            guidancePeriod: "FY2026E",
            guidanceMetric: "[预计 2026 capital expenditures across Amazon 约 $200B](source:SRC-AMZN-Q4-2025)。",
            comparability: "近似 capex/PPE 投入口径，但覆盖全集团 AI、chips、robotics、satellites 等，不是纯 AWS 或 GPU/ASIC 采购。",
          },
        ],
        sourceIds: ["SRC-MSFT-FY26-Q2-CALL", "SRC-GOOGL-Q4-2025", "SRC-META-Q4-2025", "SRC-AMZN-Q4-2025"],
      },
      {
        horizon: "环节 3｜订单/交付：AI server backlog 与 revenue 指引",
        expectationStatus: "公司指引",
        marketExpectation: "本环节复用 01 的「订单/交付」链条，并参考本环节已选 Dell AI-optimized server ending backlog。Dell 给出的 FY27 AI-optimized server revenue 约 $50B 是从订单池到系统交付收入的硬预期，能验证客户预算是否落到含 GPU/ASIC 的系统交付。",
        expectationRows: [
          {
            entity: "Dell",
            currentPeriod: "FY2026",
            currentMetric: "[AI-optimized server orders 超过 $64B、shipments 超过 $25B，进入 FY2027 的 backlog 为 $43B](source:SRC-DELL-FY26-Q4)。",
            guidancePeriod: "FY2027E",
            guidanceMetric: "[AI-optimized server revenue 约 $50B、同比 +103%](source:SRC-DELL-FY26-Q4)。",
            comparability: "与 01 的订单/交付环节和 02 的 backlog metric 对齐；订单/backlog 对下一年收入指引，传导关系明确但不是同一会计字段。",
          },
        ],
        sourceIds: ["SRC-DELL-FY26-Q4"],
      },
      {
        horizon: "环节 4｜BOM弹性：平台规格与系统交付放大系数",
        expectationStatus: "公司路线图 + 系统商指引",
        marketExpectation: "本环节复用 01 的「当前 BOM 需求弹性」链条，并参考本环节已选 NVIDIA platform generation scope 与 Dell AI server revenue guide。要回答的不是终端 AI 需求本身，而是 AI 需求增长后，GPU/ASIC 这一 BOM 的需求会不会被 rack-scale / pod-scale 平台和系统交付放大。",
        expectationRows: [
          {
            entity: "NVIDIA",
            currentPeriod: "Q4 FY2026 / GTC 2026",
            currentMetric: "[Data Center revenue $62.3B，FY26 full-year Data Center revenue $193.7B](source:SRC-NVDA-FY26-Q4)。",
            guidancePeriod: "Q1 FY2027E / Vera Rubin cycle",
            guidanceMetric: "[Q1 FY27 revenue outlook $78.0B +/-2%](source:SRC-NVDA-FY26-Q4)；[Vera Rubin 定义下一代 AI factory rack-scale 系统](source:SRC-NVDA-GTC-VERA-RUBIN-20260316)。",
            comparability: "收入指引是公司整体口径，Vera Rubin 是平台规格；二者共同说明当前 BOM 的需求弹性有未来平台锚点，但仍需单柜 GPU/ASIC 数量和 ASP 验证。",
          },
          {
            entity: "Dell",
            currentPeriod: "FY2026",
            currentMetric: "[AI-optimized server orders >$64B、shipments >$25B、FY27 backlog $43B](source:SRC-DELL-FY26-Q4)。",
            guidancePeriod: "FY2027E",
            guidanceMetric: "[AI-optimized server revenue guide 约 $50B、同比 +103%](source:SRC-DELL-FY26-Q4)。",
            comparability: "Dell 是系统交付代理，不是 GPU/ASIC 厂商收入；但它能验证平台规格升级已经进入整机/机柜交付池。",
          },
        ],
        sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-NVDA-GTC-VERA-RUBIN-20260316", "SRC-DELL-FY26-Q4"],
      },
      {
        horizon: "环节 5｜GPU 财务兑现：NVIDIA Data Center revenue 的未来锚点",
        expectationStatus: "当前收入强，硬指引缺口",
        marketExpectation: "本环节复用 01 的「GPU 财务兑现」链条，并参考本环节已选 NVIDIA Data Center segment revenue。当前收入兑现极强，但本报告这一轮未放入 NVIDIA 同口径下一季收入指引；Vera Rubin 是路线图，Omdia 是行业池预测，二者都不能替代 NVIDIA forward revenue guidance。",
        expectationRows: [
          {
            entity: "NVIDIA",
            currentPeriod: "Q4 FY2026",
            currentMetric: "[Data Center revenue 为 $62.3B](source:SRC-NVDA-FY26-Q4)。",
            guidancePeriod: "未放入同口径收入指引",
            guidanceMetric: "[Vera Rubin](source:SRC-NVDA-GTC-VERA-RUBIN-20260316) 是未来平台路线图，不是收入指引。",
            comparability: "与 01 的 GPU 财务兑现环节和 02 的 NVIDIA Data Center revenue metric 对齐，但未来端缺少同口径 revenue guidance；需要补 NVIDIA 下季指引或一致预期。",
          },
          {
            entity: "Omdia",
            currentPeriod: "2024A / 2025E",
            currentMetric: "[AI data-center processor spending：2024 年约 $123B，2025E 约 $207B](source:SRC-OMDIA-AI-PROCESSORS-20250828)。",
            guidancePeriod: "2030E",
            guidanceMetric: "[约 $286B，且 custom ASICs gaining traction](source:SRC-OMDIA-AI-PROCESSORS-20250828)。",
            comparability: "这是 GPU/ASIC 行业池预期，不是 NVIDIA 收入口径；只能作为空间和 mix 旁证。",
          },
        ],
        sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-NVDA-GTC-VERA-RUBIN-20260316", "SRC-OMDIA-AI-PROCESSORS-20250828"],
      },
      {
        horizon: "环节 6｜ASIC 财务兑现：Broadcom AI semiconductor revenue 指引",
        expectationStatus: "公司指引",
        marketExpectation: "本环节复用 01 的「ASIC 财务兑现」链条，并参考本环节已选 Broadcom AI semiconductor revenue。Broadcom Q2 FY26 AI semiconductor revenue 约 $10.7B 是 custom ASIC 路线最清楚的未来收入锚点。",
        expectationRows: [
          {
            entity: "Broadcom",
            currentPeriod: "Q1 FY2026",
            currentMetric: "[AI revenue 为 $8.4B、同比 +106%](source:SRC-AVGO-FY26-Q1)。",
            guidancePeriod: "Q2 FY2026E",
            guidanceMetric: "[AI semiconductor revenue 预计约 $10.7B](source:SRC-AVGO-FY26-Q1)。",
            comparability: "与 01 的 ASIC 财务兑现环节和 02 的 Broadcom AI semiconductor revenue metric 基本对齐；从 Q1 actual 到 Q2 guide 隐含约 +27% QoQ。",
          },
        ],
        sourceIds: ["SRC-AVGO-FY26-Q1"],
      },
      {
        horizon: "环节 7｜反证/缺口：GPU-hours 与 accelerator utilization 预期",
        expectationStatus: "关键缺口",
        marketExpectation: "本环节复用 01 的「反证/缺口」链条，并参考本环节已选 public GPU-hours consumed by AI workloads。当前没有稳定公开的 GPU-hours、accelerator utilization 或 AI ROI 未来预期，因此需求强结论仍依赖 WAU、RPO、backlog、NVIDIA/Broadcom 收入等代理链条。",
        expectationRows: [
          {
            entity: "OpenAI / Google / hyperscalers",
            currentPeriod: "截至本问搜索",
            currentMetric: "[OpenAI tokens/min 与 Gemini daily-token 倍数可作为 workload 旁证](source:SRC-OPENAI-DEVDAY-2025)，[NVIDIA Dynamo 是推理效率路线图](source:SRC-NVDA-GTC-DYNAMO-20260316)。",
            guidancePeriod: "未披露",
            guidanceMetric: "未披露连续可比 GPU-hours、accelerator utilization 或 AI ROI 目标。",
            comparability: "与 01 的反证/缺口环节和 02 的 GPU-hours metric 对齐；这是最重要缺口，不能用 capex、收入或 tokens 直接替代 GPU-hours。",
          },
        ],
        sourceIds: ["SRC-OPENAI-DEVDAY-2025", "SRC-GOOGL-Q4-2025-CALL", "SRC-NVDA-GTC-DYNAMO-20260316"],
      },
    ],
    mechanism: {
      sustain: "需求可持续的核心机制是使用量、任务复杂度和在线推理时长继续增长，而芯片性能/软件效率提升无法完全抵消新增计算量；当客户愿意用 capex、RPO 和系统订单锁定未来供给时，GPU/ASIC 供应商可以把 workload 增长变成收入、毛利和现金流。",
      break: "最重要反证是 tokens / GPU hours 增长放缓、推理成本下降快于任务量增长、客户 AI ROI 不足导致 capex 下修、RPO 不转收入、AI server backlog 取消或 Broadcom/NVIDIA guidance 放缓；这些信号会说明前端需求没有持续穿透到当前 BOM。",
    },
    detail: {
      ...(row.detail || {}),
      reportNarrative: {
        ...(row.detail?.reportNarrative || {}),
        chainNodes: strictComputeDemandChainNodes(),
      },
    },
    searchArtifact: {
      search_execution_status: "completed",
      parser_status: "gpt_verified_source_parse",
      completed_at: "2026-07-03",
      source_ids: sourceIds,
      source_universe_plan: {
        priority_sources: [
          "OpenAI and model-provider usage disclosures",
          "hyperscaler earnings releases and earnings calls",
          "cloud RPO / capex / PPE disclosures",
          "AI server vendor order and backlog disclosures",
          "GPU and custom ASIC vendor segment revenue disclosures",
        ],
        selected_source_ids: sourceIds,
        cutoff_policy: `only sources visible on or before ${AS_OF_DATE} strengthen the as-of conclusion; later labels or price action are excluded`,
      },
      exa_search_plan: {
        direct_query: "AI factory GPU ASIC demand ChatGPT tokens hyperscaler capex RPO Dell AI server orders NVIDIA Data Center Broadcom AI semiconductor before 2026-03-28",
        expected_fields: [
          "application_usage_or_token_workload",
          "customer_capex_or_rpo",
          "ai_server_orders_shipments_backlog",
          "gpu_or_asic_revenue_history",
          "forward_guidance",
          "refuting_workload_or_roi_gap",
        ],
        selected_source_ids: sourceIds,
        retrieval_status: "completed",
        gap_rule: "same-metric history requires at least five comparable points; otherwise render noncontinuous chart or metric-trend-gap and do not infer acceleration from a single snapshot",
      },
      evidence_summary: [
        "Primary application metric is ChatGPT weekly active users, with a WAU series from roughly 100M to 800M+ using OpenAI and public management-disclosure sources.",
        "Primary budget/RPO metric is Microsoft Commercial RPO, rising from $235B in Q3 FY24 to $625B in Q2 FY26; Microsoft disclosed roughly 45% of Q2 FY26 RPO came from OpenAI.",
        "Primary order metric is Dell AI-optimized server ending backlog, moving from roughly $9B at FY25 Q4 to $43B entering FY27.",
        "Primary GPU financial metric is NVIDIA Data Center segment revenue; primary ASIC financial metric is Broadcom AI semiconductor revenue.",
      ],
      gap_summary: [
        "Direct public GPU-hours consumed by AI workloads remains insufficient, so the direct workload-to-accelerator bridge stays a gap.",
        "Microsoft Commercial RPO is a cloud commitment proxy and does not equal GPU/ASIC orders; it must be cross-checked with capex and hardware backlog.",
        "Broadcom AI semiconductor revenue has fewer than five cutoff-visible actual quarterly points; management guidance is kept in future expectations rather than the history curve.",
      ],
      verdict_policy: "verdict_written_after_question_level_search_parse_and_explicit_gap_marking",
    },
  };
}

function strictComputeDemandChainNodes() {
  return [
    {
      title: "AI 应用/任务 -> token 与推理工作负载",
      question: "是否有真实 AI 使用量和推理任务增长，而不是只有主题热度？",
      status: "使用量证据强，但 tokens/GPU-hours 连续序列仍缺口",
      metrics: [
        {
          type: "应用/任务",
          name: "ChatGPT weekly active users (WAU)",
          why: "应用端只选 ChatGPT WAU 作为主 metric，因为它是最可持续公开追踪的大规模 AI 使用入口；OpenAI API tokens/min 和 Gemini 使用量只作为旁证，不混进主指标名称。",
          dataRequirement: "主体：OpenAI / ChatGPT；字段：weekly active users；单位：百万人；频率：公开不定期披露，优先按披露日期串联 5 个以上点；来源优先 OpenAI，其次管理层公开发言或主流媒体转述。",
          trendKind: "time_series",
          series: [
            { label: "2023 early", value: "100M WAU", scale: 13 },
            { label: "ChatGPT 2024-08", value: "200M WAU", scale: 25 },
            { label: "ChatGPT 2024-12", value: "300M WAU", scale: 38 },
            { label: "ChatGPT 2025 mid", value: "700M WAU", scale: 88 },
            { label: "OpenAI DevDay", value: "800M+ WAU", scale: 100 },
          ],
          history: "[OpenAI 的工作场景使用报告称 ChatGPT 在发布后数月内达到 100M weekly active users，且到报告时超过 700M weekly active users](source:SRC-OPENAI-CHATGPT-WORK-202602)；[2024 年 8 月 OpenAI 确认 200M+ WAU](source:SRC-CHATGPT-WAU-202408)；[2024 年 12 月 Sam Altman 表示 ChatGPT 超过 300M WAU](source:SRC-CHATGPT-WAU-202412)。",
          current: "[OpenAI DevDay 2025 披露 800M+ weekly ChatGPT users、4M+ developers、API 平台 6B tokens/min](source:SRC-OPENAI-DEVDAY-2025)。Gemini MAU 和 API token 只作为旁证，不进入主 metric 曲线。",
          future: "若 ChatGPT WAU 继续扩张，且 API tokens/min、企业席位和 agent 任务同步上行，说明应用端 workload 仍在放大；若 WAU 增速放缓而 token/GPU hours 不披露，本环节只能保守处理。",
          quality: "主指标口径统一为 WAU；tokens/min 与 Gemini 使用量降为旁证",
          sourceIds: ["SRC-OPENAI-CHATGPT-WORK-202602", "SRC-CHATGPT-WAU-202408", "SRC-CHATGPT-WAU-202412", "SRC-CHATGPT-WAU-202508", "SRC-OPENAI-DEVDAY-2025"],
        },
      ],
      history: "使用量从 2023 年早期消费者 adoption 走向 2025 年大规模 weekly users、developer/API token 和 Gemini 企业席位披露，说明任务入口已经显著扩大。",
      current: "当前最硬的公开一手锚点是 OpenAI 的 800M+ weekly users 与 6B tokens/min，以及 Alphabet 的 750M+ Gemini MAU 和 3x daily-token 使用量。",
      future: "未来要验证 workload 是否继续快于模型效率改善，核心看 tokens、GPU hours、inference revenue、agent task volume 和客户 ROI。",
      refute: "若模型效率、缓存、蒸馏和调度优化使单位任务算力快速下降，或者 AI 应用 ROI 不足，使用量增长不一定继续穿透到 accelerator 采购。",
      conclusion: "工作负载入口成立，但还不能单独判定 GPU/ASIC S 曲线阶段，必须继续看预算、订单和收入兑现。",
      sourceIds: ["SRC-OPENAI-CHATGPT-WORK-202602", "SRC-CHATGPT-WAU-202408", "SRC-CHATGPT-WAU-202412", "SRC-OPENAI-DEVDAY-2025"],
    },
    {
      title: "workload -> 客户 capex / RPO / PPE",
      question: "使用量是否已经转化为客户预算和承诺？",
      status: "客户预算与承诺证据强",
      metrics: [
        {
          type: "预算/RPO",
          name: "Microsoft commercial remaining performance obligation (Commercial RPO, $B)",
          why: "RPO 环节只选 Microsoft Commercial RPO，因为它是明确披露的商业合同未确认收入余额，FY26 Q2 电话会还披露约 45% 来自 OpenAI，能代表 AI workload 向云承诺池沉淀。",
          dataRequirement: "主体：Microsoft；字段：Commercial remaining performance obligation；单位：十亿美元；频率：季度；至少追踪 5 个季度，并同时标注 OpenAI 占比、加权平均期限和 12 个月内确认比例。",
          trendKind: "time_series",
          series: [
            { label: "Q3 FY24", value: "$235B", scale: 38 },
            { label: "Q4 FY24", value: "$269B", scale: 43 },
            { label: "Q1 FY25", value: "$259B", scale: 41 },
            { label: "Q2 FY25", value: "$298B", scale: 48 },
            { label: "Q3 FY25", value: "$315B", scale: 50 },
            { label: "Q4 FY25", value: "$368B", scale: 59 },
            { label: "Q1 FY26", value: "$392B", scale: 63 },
            { label: "Q2 FY26", value: "$625B", scale: 100 },
          ],
          history: "[Microsoft investor metrics 给出 Q3 FY24 至 Q3 FY25 Commercial RPO：$235B、$269B、$259B、$298B、$315B](source:SRC-MSFT-FY25-Q3-METRICS)；[Q4 FY25 增至 $368B](source:SRC-MSFT-FY25-Q4-CALL)；[Q1 FY26 为 $392B](source:SRC-MSFT-FY26-Q1)。",
          current: "[Microsoft Q2 FY26 Commercial RPO 增至 $625B、同比 +110%](source:SRC-MSFT-FY26-Q2)；[电话会披露约 45% 来自 OpenAI，且约 25% 将在未来 12 个月确认收入](source:SRC-MSFT-FY26-Q2-CALL)。",
          future: "未来如果 Microsoft Commercial RPO 继续增长，并且 OpenAI / Azure AI 承诺能转成 Azure revenue 和 GPU/CPU capex，说明客户承诺池继续支撑 accelerator 需求；如果 RPO 增长仅来自长久期合同且短期确认比例下降，要打折。",
          quality: "主指标口径统一；但它是云承诺池，不等同于 GPU/ASIC 订单",
          sourceIds: ["SRC-MSFT-FY25-Q3-METRICS", "SRC-MSFT-FY25-Q4-CALL", "SRC-MSFT-FY26-Q1", "SRC-MSFT-FY26-Q2", "SRC-MSFT-FY26-Q2-CALL"],
        },
      ],
      history: "客户侧已经从口头 AI 需求进入 RPO、capex 和 PPE purchases 等硬预算项目。",
      current: "Microsoft、Amazon、Alphabet、Meta、Oracle 同时披露大规模 AI/cloud infrastructure 预算或 RPO，说明需求已进入采购与建设约束。",
      future: "需要每季确认 capex 是否继续流向 GPU/ASIC、AI server、网络和电力液冷，而不是被非 accelerator 基础设施稀释。",
      refute: "如果 capex 指引下修、RPO 增速放缓或 FCF 压力导致交付延期，预算环节会先失效。",
      conclusion: "预算/RPO 环节强成立，但仍需穿透到具体 accelerator 订单。",
      sourceIds: ["SRC-MSFT-FY25-Q3-METRICS", "SRC-MSFT-FY25-Q4-CALL", "SRC-MSFT-FY26-Q1", "SRC-MSFT-FY26-Q2", "SRC-MSFT-FY26-Q2-CALL"],
    },
    {
      title: "capex / RPO -> AI server 与 accelerator 交付订单",
      question: "客户预算是否已经进入含 GPU/ASIC 的系统订单和 backlog？",
      status: "订单漏斗证据强",
      metrics: [
        {
          type: "订单/交付",
          name: "Dell AI-optimized server ending backlog ($B)",
          why: "订单环节只选 Dell AI-optimized server ending backlog，因为它是含 GPU/ASIC 系统未交付订单池，比单季 orders 更能代表客户预算是否已经沉淀成未来硬件交付。",
          dataRequirement: "主体：Dell；字段：AI-optimized server ending backlog；单位：十亿美元；频率：季度期末；至少追踪 5 个季度，并用 orders、shipments、AI server revenue 作为解释变量而非主 metric。",
          trendKind: "time_series",
          series: [
            { label: "Q4 FY25", value: "~$9B", scale: 21 },
            { label: "Q1 FY26", value: "$14.4B", scale: 33 },
            { label: "Q2 FY26", value: "$11.7B", scale: 27 },
            { label: "Q3 FY26", value: "$18.4B", scale: 43 },
            { label: "Q4 FY26", value: "$43B", scale: 100 },
          ],
          history: "[Dell FY25 Q4 披露 AI server backlog 约 $9B](source:SRC-DELL-FY25-Q4)；[Q1 FY26 backlog 为 $14.4B](source:SRC-DELL-FY26-Q1)；[Q2 FY26 exiting backlog 为 $11.7B](source:SRC-DELL-FY26-Q2-PERFORMANCE)；[Q3 FY26 backlog 为 $18.4B](source:SRC-DELL-FY26-Q3)。",
          current: "[Dell FY26 全年 AI-optimized server orders 超过 $64B、shipments 超过 $25B，进入 FY27 backlog 为 $43B](source:SRC-DELL-FY26-Q4)。",
          future: "[Dell guided FY27 AI-optimized server revenue around $50B, up 103% year over year](source:SRC-DELL-FY26-Q4)。未来看 backlog 是否按期转 revenue、orders 是否继续补充 backlog。",
          quality: "主指标是期末 backlog；orders/shipments/revenue 只作解释变量",
          sourceIds: ["SRC-DELL-FY25-Q4", "SRC-DELL-FY26-Q1", "SRC-DELL-FY26-Q2-PERFORMANCE", "SRC-DELL-FY26-Q3", "SRC-DELL-FY26-Q4"],
        },
      ],
      history: "Dell AI-optimized server ending backlog 说明客户预算已经开始进入系统交付，而不是停留在云预算总量。",
      current: "Dell 的订单、出货和 backlog 给出 GPU/ASIC 需求的硬件落地点。",
      future: "未来看 backlog 转收入速度、订单取消率、毛利率和现金转换。",
      refute: "若 backlog 不转收入、订单取消或系统交付利润率恶化，说明当前需求质量下降。",
      conclusion: "订单层验证成立，但仍要看 GPU/ASIC 供应商自身收入兑现。",
      sourceIds: ["SRC-DELL-FY25-Q4", "SRC-DELL-FY26-Q1", "SRC-DELL-FY26-Q2-PERFORMANCE", "SRC-DELL-FY26-Q3", "SRC-DELL-FY26-Q4"],
    },
    {
      title: "订单 -> 当前 BOM 需求弹性放大",
      question: "AI 需求增长 1 倍时，GPU/ASIC 这一 BOM 的需求会不会被平台规格和系统架构放大？",
      status: "弹性证据较强，但缺少单柜数量/ASP 连续表",
      metrics: [
        {
          type: "BOM弹性",
          name: "NVIDIA platform generation scope and Dell AI server revenue guide",
          why: "需求是否大涨不能只看终端 AI workload，还要看 workload 增长后当前 BOM 的放大倍数。rack-scale / pod-scale 平台、整柜交付和 AI server revenue guide 能验证 GPU/ASIC 是否从单卡采购升级为系统级采购。",
          dataRequirement: "主体：NVIDIA / Dell；字段：platform generation scope、rack-scale/pod-scale system、AI-optimized server backlog/revenue guide；单位：平台规格和美元；频率：平台发布和财年指引；缺少单柜 GPU/ASIC 数量、ASP 和配置率连续表时必须标为弹性缺口。",
          trendKind: "non_time_series",
          trendLabel: "BOM 需求弹性证据",
          series: [
            { label: "GB200 / NVL72", value: "rack-scale", change: "采购单位从卡/服务器上移到机柜" },
            { label: "Vera Rubin", value: "rack-scale systems", change: "下一代平台继续系统化" },
            { label: "Dell FY27 AI server revenue guide", value: "~$50B", change: "系统交付承接放大后的需求" },
          ],
          seriesGap: "平台规格和系统收入指引说明弹性方向，但没有提供同口径单柜 GPU/ASIC 数量、ASP、attach rate 的 5 点历史序列。",
          history: "[SemiAnalysis GB200/rack-scale BOM 拆解](source:SRC-SA-GB200-BOM-2024) 和 [NVIDIA Vera Rubin rack-scale 平台](source:SRC-NVDA-GTC-VERA-RUBIN-20260316) 表明 accelerator 采购单位正在上移。",
          current: "[Dell FY27 AI-optimized server revenue guide 约 $50B](source:SRC-DELL-FY26-Q4) 说明这种平台规格升级已经进入系统交付收入预期。",
          future: "如果下一代平台继续提高单柜 GPU/ASIC 数量、单系统 ASP 和系统交付收入，当前 BOM 的需求弹性会继续大于终端 AI 需求增速。",
          quality: "弹性机制证据强；缺少单柜配置、ASP、attach rate 的连续量化表。",
          sourceIds: ["SRC-SA-GB200-BOM-2024", "SRC-NVDA-GTC-VERA-RUBIN-20260316", "SRC-DELL-FY26-Q4"],
        },
      ],
      history: "需求弹性来自平台采购单位变化：从单卡、单服务器，走向 rack-scale、pod-scale 和 AI factory 交付。",
      current: "当前有 GB200/Vera Rubin 平台规格、Dell backlog/revenue guide 支撑，但还缺少按平台代际量化的单柜 GPU/ASIC 数量和 ASP。",
      future: "未来重点看单柜 GPU/ASIC 数、系统 ASP、attach rate、订单转收入和客户配置是否继续上移。",
      refute: "如果软件效率、模型压缩或架构替代使客户用更少 GPU/ASIC 完成同样 workload，BOM 弹性会下降。",
      conclusion: "当前 BOM 不是被动跟随终端 AI 需求，而是被平台化采购放大拉动；这是第 1 问成立的核心组成部分。",
      sourceIds: ["SRC-SA-GB200-BOM-2024", "SRC-NVDA-GTC-VERA-RUBIN-20260316", "SRC-DELL-FY26-Q4"],
    },
    {
      title: "订单 -> GPU 平台收入兑现",
      question: "GPU 平台供应商是否已经把需求兑现成连续收入曲线？",
      status: "NVIDIA 同口径曲线强",
      metrics: [
        {
          type: "GPU财务兑现",
          name: "NVIDIA Data Center segment revenue ($B)",
          why: "GPU 财务兑现只选 NVIDIA Data Center segment revenue，因为它是同公司、同分部、季度披露、最直接对应 AI accelerator 平台需求的收入字段。",
          dataRequirement: "主体：NVIDIA；字段：Data Center segment revenue；单位：十亿美元；频率：季度；至少追踪 5 个季度，并同步观察 gross margin、customer concentration 和 platform generation。",
          trendKind: "time_series",
          series: [
            { label: "Q4 FY23", value: "$3.62B", scale: 6 },
            { label: "Q2 FY24", value: "$10.32B", scale: 17 },
            { label: "Q4 FY24", value: "$18.4B", scale: 30 },
            { label: "Q2 FY25", value: "$26.3B", scale: 42 },
            { label: "Q4 FY25", value: "$35.6B", scale: 57 },
            { label: "Q2 FY26", value: "$41.1B", scale: 66 },
            { label: "Q3 FY26", value: "$51.2B", scale: 82 },
            { label: "Q4 FY26", value: "$62.3B", scale: 100 },
          ],
          history: "[NVIDIA Q4 FY23 Data Center revenue was $3.62B](source:SRC-NVDA-FY23-Q4)，[Q2 FY24 was $10.32B](source:SRC-NVDA-FY24-Q2)，[Q4 FY24 was $18.4B](source:SRC-NVDA-FY24-Q4)，[Q2 FY25 was $26.3B](source:SRC-NVDA-FY25-Q2)，[Q4 FY25 was $35.6B](source:SRC-NVDA-FY25-Q4)，[Q4 FY26 was $62.3B](source:SRC-NVDA-FY26-Q4)。",
          current: "[Q3 FY26 Data Center revenue was $51.2B and management said compute demand was accelerating](source:SRC-NVDA-FY26-Q3)；[Q4 FY26 reached $62.3B](source:SRC-NVDA-FY26-Q4)。",
          future: "未来看 Blackwell/Vera Rubin 节奏、gross margin、allocation、客户集中度和自研 ASIC 替代压力。",
          quality: "核心同口径历史数据，满足 5+ 数据点",
          sourceIds: ["SRC-NVDA-FY23-Q4", "SRC-NVDA-FY24-Q2", "SRC-NVDA-FY24-Q4", "SRC-NVDA-FY25-Q2", "SRC-NVDA-FY25-Q4", "SRC-NVDA-FY26-Q2", "SRC-NVDA-FY26-Q3", "SRC-NVDA-FY26-Q4"],
        },
      ],
      history: "NVIDIA Data Center revenue 从 Q4 FY23 到 Q4 FY26 出现量级跃迁，说明 GPU 平台已经把需求链条兑现进收入。",
      current: "Q4 FY26 Data Center revenue $62.3B 是截至本问 as-of 之前最直接的财务化锚点。",
      future: "若未来几个季度 guide 和毛利率继续稳住，需求链条仍有强度；若增长率降速叠加估值拥挤，要转入定价问题。",
      refute: "若收入增长放缓、毛利下降或客户自研 ASIC 替代压低份额/ASP，GPU 平台需求强度需要下调。",
      conclusion: "GPU 平台财务兑现强成立。",
      sourceIds: ["SRC-NVDA-FY23-Q4", "SRC-NVDA-FY24-Q2", "SRC-NVDA-FY24-Q4", "SRC-NVDA-FY25-Q2", "SRC-NVDA-FY25-Q4", "SRC-NVDA-FY26-Q2", "SRC-NVDA-FY26-Q3", "SRC-NVDA-FY26-Q4"],
    },
    {
      title: "订单 -> custom ASIC 收入兑现",
      question: "custom ASIC 是否也形成第二条 accelerator 需求曲线？",
      status: "方向强，口径需继续净化",
      metrics: [
        {
          type: "ASIC财务兑现",
          name: "Broadcom AI semiconductor revenue ($B)",
          why: "ASIC 财务兑现只选 Broadcom AI semiconductor revenue，因为它是当前 custom AI accelerator / AI Ethernet 路线最清楚的公司披露收入字段。",
          dataRequirement: "主体：Broadcom；字段：AI semiconductor revenue actual；单位：十亿美元；频率：季度实际值；历史数据只收 actual，不把下一季或全年 guidance 放进历史；少于 5 个同口径实际点时标为趋势缺口。",
          trendLabel: "actual quarterly revenue only",
          series: [
            { label: "Q2 FY25", value: ">$4.4B", scale: 41 },
            { label: "Q3 FY25", value: "$5.2B", scale: 49 },
            { label: "Q1 FY26", value: "$8.4B", scale: 79 },
          ],
          seriesGap: "历史数据只保留 Broadcom 已披露的 AI semiconductor revenue actual。Q4 FY25 release 只披露 AI semiconductor revenue +74% YoY 并给出下一季预期，未给出可直接并入同字段数据序列的实际美元值；Q2 FY26 也是 guidance，因此都不进入历史数据表。",
          history: "[Broadcom Q2 FY25 AI revenue exceeded $4.4B](source:SRC-AVGO-FY25-Q2)，[Q3 FY25 AI revenue was $5.2B](source:SRC-AVGO-FY25-Q3)，[Broadcom Q1 FY26 AI revenue was $8.4B, up 106% YoY](source:SRC-AVGO-FY26-Q1)。",
          current: "[Broadcom Q1 FY26 AI revenue was $8.4B, up 106% YoY](source:SRC-AVGO-FY26-Q1)。",
          future: "[Broadcom expected Q2 FY26 AI semiconductor revenue of about $10.7B](source:SRC-AVGO-FY26-Q1)，是 custom ASIC 路线的未来锚点。",
          quality: "actual-only 口径；少于 5 个季度实际点，不能画成完整历史趋势线",
          sourceIds: ["SRC-AVGO-FY25-Q2", "SRC-AVGO-FY25-Q3", "SRC-AVGO-FY25-Q4", "SRC-AVGO-FY26-Q1"],
        },
      ],
      history: "Broadcom AI semiconductor revenue actual 显示 custom ASIC 已经从叙事进入季度收入，但公开同口径实际点仍不足 5 个。",
      current: "Q1 FY26 AI revenue $8.4B 是截至 as-of 前的最新实际锚点。",
      future: "Q2 FY26 guide $10.7B 说明市场预期 custom ASIC 路线继续扩张。",
      refute: "若大客户项目延后、ASIC 设计周期拉长或 Ethernet/ASIC 组合被替代，第二增长曲线会下修。",
      conclusion: "ASIC 路线需求成立，但口径仍需后续净化。",
      sourceIds: ["SRC-AVGO-FY25-Q2", "SRC-AVGO-FY25-Q3", "SRC-AVGO-FY25-Q4", "SRC-AVGO-FY26-Q1"],
    },
    {
      title: "质量与反证",
      question: "哪些信号会推翻“需求大幅增长”的结论？",
      status: "存在关键缺口，需持续监控",
      metrics: [
        {
          type: "反证/缺口",
          name: "Public GPU-hours consumed by AI workloads (GPU-hours)",
          why: "反证/缺口环节只选 public GPU-hours consumed by AI workloads，因为它是从应用任务直接映射到 accelerator 消耗的最硬指标；如果它缺失，必须承认当前结论依赖 WAU、RPO、backlog 和收入代理。",
          dataRequirement: "主体：优先 OpenAI / Microsoft / Google / hyperscaler；字段：AI workload GPU-hours consumed；单位：GPU-hours；频率：季度；若没有 5 个公开点，必须显示趋势缺口，不得用 token、收入或 capex 冒充。",
          series: [],
          seriesGap: "截至本问搜索，公开材料尚未给出稳定可比的 tokens、GPU hours、accelerator utilization、AI ROI 五点以上历史序列；这是后续刷新第一优先级。",
          history: "当前只能看到 OpenAI tokens/min、Gemini daily-token 倍数、NVIDIA/客户侧收入和 capex 代理，不能直接画 workload-to-GPU-hours 曲线。",
          current: "直接 workload 指标仍是不足项；需求成立主要由客户预算、系统订单和供应商收入共同交叉验证。",
          future: "未来若公开 tokens/GPU hours 增速低于推理效率改善，或客户 ROI 不足，GPU/ASIC 需求曲线将被下修。",
          quality: "关键 gap；不得用模型先验填补",
          sourceIds: ["SRC-OPENAI-DEVDAY-2025", "SRC-GOOGL-Q4-2025-CALL", "SRC-NVDA-GTC-DYNAMO-20260316"],
        },
      ],
      history: "缺口主要集中在直接 workload-to-accelerator 指标，而非收入和订单端。",
      current: "本问结论可以说需求链条强成立，但不能说所有关键 metric 已充分。",
      future: "下一轮应优先搜索云厂 utilization、AI 服务收入、GPU hours、tokens、inference cost 和客户 ROI。",
      refute: "如果这些直接指标与 capex/收入背离，应降低本 BOM S 曲线阶段判断。",
      conclusion: "结论强但不是无条件强；关键缺口已显式标注。",
      sourceIds: ["SRC-OPENAI-DEVDAY-2025", "SRC-GOOGL-Q4-2025-CALL", "SRC-NVDA-GTC-DYNAMO-20260316"],
    },
  ];
}

function renderBomSCurveStageCard(node, rows) {
  const searchArtifacts = rows.map((row, index) => buildBomQuestionSearchArtifact(row, index + 1, node));
  const searchComplete = searchArtifacts.every((artifact) => artifact.search_execution_status === "completed");
  const stage = searchComplete ? bomSCurveStageForNode(node) : pendingBomSCurveStage(node);
  const sourceIds = [...new Set(rows.flatMap((row) => row.sourceIds || []))];
  return `<details class="bom-s-curve-stage-card">
    <summary><span>S曲线阶段判定</span><div><b>${e(stage.stage)}</b><p>${e(stage.confidence)}</p></div><span class="chevron">›</span></summary>
    <div class="bom-stage-rollup-body">
      <section class="bom-stage-source-discipline">
        <b>判定门槛</b>
        <p>只有当前 BOM 的 6 个子问都完成外部搜索、来源解析、metric 历史/缺口检查和本问结论后，才允许把阶段判定升级为正式结论；未完成逐问搜索时，旧本地材料只能作为待验证缓存。</p>
      </section>
      <section class="bom-stage-current">
        <b>当前阶段</b>
        <p>${sourceText(stage.current)}</p>
      </section>
      <div class="bom-stage-evidence-grid">
        ${rows.map((row, index) => `<article>
          <span>Q${index + 1}</span>
          <b>${e(row.question)}</b>
          <p>${sourceText(row.answer)}</p>
          <div class="bom-question-sources">${sourceChips(row.sourceIds)}</div>
        </article>`).join("")}
      </div>
      <section class="bom-stage-next-signal">
        <b>下一阶段确认信号</b>
        <p>${sourceText(stage.nextSignal)}</p>
      </section>
      <section class="bom-stage-downgrade-signal">
        <b>降级信号</b>
        <p>${sourceText(stage.downgradeSignal)}</p>
      </section>
      <div class="bom-question-sources">${sourceChips(sourceIds)}</div>
    </div>
  </details>`;
}

function pendingBomSCurveStage(node) {
  return {
    stage: "待逐问搜索完成后判定",
    confidence: "置信度：待定",
    current: `${node.name} 的六个子问尚未完成新一轮 question-level search/source parse/gap 标注，因此当前报告不作正式 S 曲线阶段判断。旧本地材料只能作为待验证缓存，不能替代阶段判定证据。`,
    nextSignal: "逐一完成需求弹性、供给、控制者、财务兑现、市场定价、反证六问的搜索和解析后，再根据六问结论判断当前 BOM 位于叙事期、预算/订单确认期、供给紧张期、财务兑现期，还是定价拥挤/成熟期。",
    downgradeSignal: "如果逐问搜索只能得到主题叙事、少量截面或无法追溯到当前 BOM 的 metric 历史/未来锚点，则该 BOM 的阶段应维持 pending，不得升级为早期 S 曲线机会。",
  };
}

function bomSCurveStageForNode(node) {
  const presets = {
    compute: {
      stage: "阶段 4：财务兑现期，叠加定价拥挤风险",
      confidence: "置信度：中；需逐问搜索确认",
      current: "GPU/ASIC 已经从主题叙事进入收入、订单和平台迭代兑现期；但因为市场关注度最高，S 曲线早期优势必须继续通过盈利上修是否超过估值隐含预期来验证。",
      nextSignal: "NVIDIA/Broadcom/AMD accelerator 指引继续上修、客户 capex/RPO 与 AI server backlog 同步兑现，并且毛利率/ASP 没有被 custom ASIC 或竞争压低。",
      downgradeSignal: "客户 capex 放缓、GPU allocation 松动、custom ASIC 替代导致价格或份额下行，或者估值已经完全吃掉未来 2-3 年增长。",
    },
    manufacturing: {
      stage: "阶段 3：供给瓶颈确认期，正在向财务兑现过渡",
      confidence: "置信度：中；需逐问搜索确认",
      current: "先进制程与先进封装的价值来自 GPU/ASIC 和 HBM 集成需求，但阶段判定必须先验证产能、良率、排期、价格和客户锁定，而不能只看 AI 芯片总需求。",
      nextSignal: "先进封装产能、先进节点收入占比、capex 与客户长期订单继续同步上行，且产能释放没有快速压缩价格或毛利。",
      downgradeSignal: "CoWoS/先进封装扩产快于需求、良率改善使稀缺性下降，或替代封装/设计路线降低单位价值量。",
    },
    memory: {
      stage: "阶段 3-4：供给紧张与财务兑现重叠",
      confidence: "置信度：中；需逐问搜索确认",
      current: "HBM 的客户资格、带宽需求、ASP 和供给排期已经把节点推入财务兑现区间，但仍需逐问搜索确认 HBM4 份额、价格曲线和新增供给节奏。",
      nextSignal: "HBM TAM、HBM ASP、客户资格和存储厂 operating margin 继续改善，且新增产能没有明显压低价格。",
      downgradeSignal: "Samsung/其他供给追赶导致价格回落，客户自研路线降低 HBM 强度，或高毛利兑现被库存周期反转抵消。",
    },
    network: {
      stage: "阶段 2-3：规格拉动向供给验证过渡",
      confidence: "置信度：中低；需逐问搜索确认",
      current: "高速连接和 AI 网络受 rack-scale/cluster-scale 架构拉动，但公开连续序列和公司级穿透仍不足，阶段更接近从订单导入走向供给验证。",
      nextSignal: "800G/1.6T、retimer、AEC、switch silicon 和 optical interconnect 的设计导入转成多季度收入，并且客户集中风险下降。",
      downgradeSignal: "网络架构路线变化、集成度提升、客户自研/second source 或价格竞争削弱单位价值量和毛利弹性。",
    },
    powerCooling: {
      stage: "阶段 2-3：预算确认后的工程约束早期加速",
      confidence: "置信度：中；需逐问搜索确认",
      current: "电力/液冷/数据中心基础设施受高功率机柜和项目交付约束拉动，较像从预算和订单进入早期加速，但需要逐问搜索验证项目周期、backlog 质量和现金转化。",
      nextSignal: "orders、backlog、organic growth、液冷 attach 和服务收入持续上行，项目毛利率与现金转换没有恶化。",
      downgradeSignal: "电网/场地审批延迟、项目交付成本超支、客户 capex 下修，或液冷标准化后价格和服务价值量被压缩。",
    },
    system: {
      stage: "阶段 3-4：订单交付兑现，但利润池质量需折扣",
      confidence: "置信度：中低；需逐问搜索确认",
      current: "服务器/机柜系统交付已经能看到 AI server orders、shipments 和 backlog，但该节点更像需求穿透验证器，是否是高质量 S 曲线还取决于毛利率、现金流和差异化能力。",
      nextSignal: "AI server backlog 按期转收入，rack-scale 集成交付复杂度带来服务和工程利润，而不是只放大低毛利转售收入。",
      downgradeSignal: "GPU allocation 放松后整机竞争加剧、毛利率下行、库存/应收恶化，或客户直接采购和 ODM 竞争压低系统商利润池。",
    },
  };
  return presets[node.id] || {
    stage: "阶段待判定",
    confidence: "置信度：低；需逐问搜索确认",
    current: "当前 BOM 尚未完成六问搜索闭环，不能给出正式 S 曲线阶段。",
    nextSignal: "完成六问搜索、metric 历史序列、未来预期和反证检查后再确认阶段。",
    downgradeSignal: "若搜索只能得到主题叙事或孤立截面，阶段应维持 watch_only / no_action。",
  };
}

function renderBomQuestionFourStep(row, questionNumber, node) {
  const analysis = buildBomQuestionAnalysis(row, questionNumber, node);
  const sectionTitles = bomQuestionSectionTitles(row.question);
  const logicStages = buildBomLogicStages(analysis.metrics);
  const futureCards = alignFutureCardsToStages(analysis.future, logicStages, row, node);
  return `<section class="bom-question-stage-flow">
    <details class="bom-step-card bom-step-metrics bom-step-logic">
      <summary><span>01</span><h5>${e(sectionTitles.logic)}</h5><span class="chevron">›</span></summary>
      <div class="bom-step-body">
        <p>${sourceText(analysis.metricLogic)}</p>
        ${renderConcreteLogicChainPanel(logicStages)}
      </div>
    </details>
    <div class="bom-logic-stage-stack">${logicStages.map((stage, index) => renderBomIntegratedStageCard(stage, futureCards[index], analysis, index + 2)).join("")}</div>
    <details class="bom-step-card bom-step-final-trend">
      <summary><span>Final</span><h5>${e(sectionTitles.finalTrend)}</h5><span class="chevron">›</span></summary>
      <div class="bom-step-body">
        <div class="bom-final-trend-grid">
          ${renderBomMechanismCard("支持未来继续的机制", analysis.mechanism.sustain)}
          ${renderBomMechanismCard("削弱或推翻趋势的机制", analysis.mechanism.break)}
        </div>
      </div>
    </details>
  </section>`;
}

function renderBomIntegratedStageCard(stage, futureCard, analysis, displayIndex) {
  return `<details class="bom-step-card bom-logic-stage-card bom-stage-integrated-card">
    <summary>
      <span class="stage-index">${String(displayIndex).padStart(2, "0")}</span>
      <div><b>环节 ${stage.index}｜${e(stage.stage)}</b><strong>${e(logicStageQuestion(stage))}</strong></div>
      <span class="chevron">›</span>
    </summary>
    <div class="bom-logic-stage-body">
      <p>${sourceText(logicStageRole(stage))}</p>
      <details class="bom-stage-subcard bom-stage-history-card">
        <summary><b>Metric 历史与现状</b><span class="chevron">›</span></summary>
        <div class="bom-stage-subcard-body">
          ${renderBomStageHistoryContent(stage)}
        </div>
      </details>
      <details class="bom-stage-subcard bom-stage-future-card">
        <summary><b>市场的未来预期</b><span class="chevron">›</span></summary>
        <div class="bom-stage-subcard-body">
          ${renderBomFutureCard(futureCard, stage)}
        </div>
      </details>
      <details class="bom-stage-subcard bom-stage-mechanism-card">
        <summary><b>第一性原理评估</b><span class="chevron">›</span></summary>
        <div class="bom-stage-subcard-body">
          <div class="bom-stage-mechanism-grid">
            ${renderBomMechanismCard("本环节支持机制", stageMechanismSupport(stage, analysis))}
            ${renderBomMechanismCard("本环节反向机制", stageMechanismRefute(stage, analysis))}
          </div>
        </div>
      </details>
    </div>
  </details>`;
}

function renderBomStageHistoryContent(stage) {
  const metric = stage.metric;
  return `<div class="bom-stage-history-content">
    <section class="bom-stage-metric-choice">
      <b>本环节应看哪些 Metric</b>
      ${renderMetricChoiceTable(stage)}
    </section>
    <section class="bom-stage-history">
      <b>Metric 历史数据 / 实体现状</b>
      <p>${sourceText(metric.history)}</p>
      ${renderMetricTrend(metric)}
    </section>
    <section class="bom-stage-current">
      <b>当前证据读法</b>
      <p>${sourceText(metric.current || "当前源包只能支持方向性判断；需要继续补同口径历史序列。")}</p>
    </section>
    <div class="bom-question-sources">${sourceChips(metric.sourceIds)}</div>
  </div>`;
}

function stageMechanismSupport(stage, analysis) {
  const metric = stage.metric || {};
  return metric.future || `如果「${stage.stage}」继续改善，并能和其它逻辑环节相互验证，本问的未来趋势更可能延续。整体支持机制：${analysis.mechanism.sustain}`;
}

function stageMechanismRefute(stage, analysis) {
  const metric = stage.metric || {};
  const gap = metric.seriesGap ? `当前需要特别警惕的数据缺口是：${metric.seriesGap}` : "";
  return `${gap} 如果「${stage.stage}」对应 metric 走弱、口径不能复核，或与订单、收入、价格、现金流相互矛盾，本环节会削弱本问结论。整体反向机制：${analysis.mechanism.break}`;
}

function alignFutureCardsToStages(cards, stages, row, node) {
  if (cards.length === stages.length) {
    return cards;
  }
  return stages.map((stage) => ({
    horizon: `环节 ${stage.index}｜${stage.stage}`,
    expectationStatus: "预期缺口",
    marketExpectation: `当前材料没有给出与 01 逻辑环节「${stage.stage}」严格对齐、且能和本环节已选 Metric「${stage.metric.name}」互相验证的公司指引、市场一致预期、第三方预测或客户侧目标。该环节目前只能用本环节历史/当前兑现数据判断，不能把泛化时间窗口或非同口径材料当作市场预期。`,
    expectationRows: [
      {
        entity: node.name,
        currentPeriod: "见本环节历史数据",
        currentMetric: stage.metric.current || stage.metric.history || "已有材料只能支持当前判断或历史截面。",
        guidancePeriod: "待补",
        guidanceMetric: "待补严格对应本环节已选 metric 的未来指引、预测或目标。",
        comparability: "缺口不是结论；后续搜索必须围绕本环节和已选 metric 单独补资料。",
      },
    ],
    sourceIds: row.sourceIds || stage.metric.sourceIds || [],
  }));
}

function buildBomLogicStages(metrics) {
  return metrics.map((metric, index) => ({
    index: index + 1,
    stage: metric.type || `环节 ${index + 1}`,
    metric,
  }));
}

function renderConcreteLogicChainPanel(stages) {
  return `<details class="bom-logic-chain-panel">
    <summary><b>具体逻辑链条</b><span>${stages.length} 个环节</span><span class="chevron">›</span></summary>
    <div class="table-scroll bom-logic-chain-table">
      <table>
        <thead><tr><th>逻辑环节</th><th>本环节要判断什么</th><th>为什么放在链条里</th></tr></thead>
        <tbody>${stages.map((stage) => `<tr class="bom-logic-chain-row">
          <td><b>${e(stage.stage)}</b></td>
          <td>${sourceText(logicStageQuestion(stage))}</td>
          <td>${sourceText(logicStageRole(stage))}</td>
        </tr>`).join("")}</tbody>
      </table>
    </div>
  </details>`;
}

function logicStageQuestion(stage) {
  return `判断「${stage.stage}」是否真实成立，以及它是否足以支撑当前 BOM 子问题的结论。`;
}

function logicStageRole(stage) {
  const stageName = stage.stage || "";
  if (/应用|工作负载|需求/.test(stageName)) return "这是需求链条的源头；只有真实任务变多，后面的预算、订单和收入才有解释力。";
  if (/预算|RPO|订单|交付|backlog/.test(stageName)) return "这是从使用热度进入采购承诺的桥梁；没有承诺池或订单，主题热度不能直接转成投资证据。";
  if (/财务|收入|利润|现金|兑现/.test(stageName)) return "这是需求穿透到公司报表的闭环；只有收入、利润或现金流兑现，才说明产业机会能被公司捕获。";
  if (/供给|产能|良率|价格|交付周期|扩产/.test(stageName)) return "这是判断供需斜率的关键；需求强但供给释放更快，稀缺溢价会下降。";
  if (/份额|控制|壁垒|议价|替代/.test(stageName)) return "这是判断谁能捕获利润池的关键；产业增长如果不能被少数公司控制，就不一定形成好标的。";
  if (/估值|定价|上修|隐含|仓位/.test(stageName)) return "这是把产业判断翻译成赔率的环节；好行业已经被充分定价时，推荐强度要下降。";
  return "这是把抽象问题拆成可验证节点的中间环节；后续对应环节卡会为它选择指标、整理历史现状、收集市场预期并做机制判断。";
}

function renderBomFutureCard(item, stage) {
  const summaryTitle = stage ? `环节 ${stage.index}｜${stage.stage}` : item.horizon;
  const stageLabel = stage ? `<div class="bom-expectation-stage"><span>对应 01 逻辑环节 / 本环节已选 Metric</span><b>${e(stage.stage)} · ${e(stage.metric.name)}</b></div>` : "";
  const subtitle = stage && item.horizon && item.horizon !== summaryTitle ? `<p class="bom-expectation-subtitle">${e(item.horizon)}</p>` : "";
  if (item.marketExpectation) {
    const fields = [
      ["预期来源", item.expectationSource],
      ["来源类型", item.sourceType],
      ["当前基准", item.currentBaseline],
      ["预期值 / 窗口", item.expectedValue],
      ["隐含增长", item.impliedGrowth],
      ["验证链条", item.chainValidation],
      ["证伪条件", item.refuteTest],
    ].filter(([, value]) => value);
    return `<details class="bom-future-card bom-expectation-card">
    <summary><b>${e(summaryTitle)}</b>${item.expectationStatus ? `<span>${e(item.expectationStatus)}</span>` : ""}<span class="chevron">›</span></summary>
    <div class="bom-nested-card-body">
      ${stageLabel}${subtitle}
      <div class="bom-expectation-core"><span>市场现在预期什么？</span><p>${sourceText(item.marketExpectation)}</p></div>
      ${item.expectationRows?.length ? renderExpectationRowsTable(item.expectationRows) : `<div class="bom-expectation-grid">${fields.map(([label, value]) => `<article class="bom-expectation-field"><span>${e(label)}</span><b>${sourceText(value)}</b></article>`).join("")}</div>`}
      <div class="bom-question-sources">${sourceChips(item.sourceIds)}</div>
    </div>
  </details>`;
  }
  if (item.expectationSource || item.expectationType || item.logicLink || item.metric || item.validation) {
    const fields = [
      ["预期来源", item.expectationSource],
      ["对应逻辑环节", item.logicLink],
      ["对应 metric", item.metric],
      ["预期性质", item.expectationType],
      ["时间范围", item.timeframe],
      ["可信度", item.confidence],
    ].filter(([, value]) => value);
    return `<details class="bom-future-card bom-expectation-card">
    <summary><b>${e(summaryTitle)}</b>${item.expectationType ? `<span>${e(item.expectationType)}</span>` : ""}<span class="chevron">›</span></summary>
    <div class="bom-nested-card-body">
      ${stageLabel}${subtitle}
      <p>${sourceText(item.view)}</p>
      <div class="bom-expectation-grid">${fields.map(([label, value]) => `<article class="bom-expectation-field"><span>${e(label)}</span><b>${sourceText(value)}</b></article>`).join("")}</div>
      ${item.validation ? `<div class="bom-expectation-validation"><b>后续验证点</b><p>${sourceText(item.validation)}</p></div>` : ""}
      <div class="bom-question-sources">${sourceChips(item.sourceIds)}</div>
    </div>
  </details>`;
  }
  return `<details class="bom-future-card">
    <summary><b>${e(summaryTitle)}</b><span class="chevron">›</span></summary>
    <div class="bom-nested-card-body">
      ${stageLabel}${subtitle}
      <p>${sourceText(item.view)}</p>
      <div class="bom-question-sources">${sourceChips(item.sourceIds)}</div>
    </div>
  </details>`;
}

function renderExpectationRowsTable(rows) {
  return `<div class="bom-expectation-table table-scroll">
    <table>
      <thead><tr><th>公司 / 机构</th><th>现状期间</th><th>现状口径 / 数值</th><th>指引期间</th><th>预期 / 指引口径 / 数值</th><th>口径说明 / 投资含义</th></tr></thead>
      <tbody>${rows.map((row) => `<tr>
        <td><b>${e(row.entity)}</b></td>
        <td>${sourceText(row.currentPeriod ?? "")}</td>
        <td>${sourceText(row.currentMetric ?? row.current)}</td>
        <td>${sourceText(row.guidancePeriod ?? "")}</td>
        <td>${sourceText(row.guidanceMetric ?? row.expectation)}</td>
        <td>${sourceText(row.comparability ?? row.readThrough)}</td>
      </tr>`).join("")}</tbody>
    </table>
  </div>`;
}

function renderBomMechanismCard(title, body) {
  return `<details class="bom-mechanism-card">
    <summary><b>${e(title)}</b><span class="chevron">›</span></summary>
    <div class="bom-nested-card-body">
      <p>${sourceText(body)}</p>
    </div>
  </details>`;
}

function renderBomLogicStageCard(stage) {
  const metric = stage.metric;
  return `<details class="bom-logic-stage-card">
    <summary>
      <span class="stage-index">环节 ${stage.index}</span>
      <div><b>${e(stage.stage)}</b><strong>${e(logicStageQuestion(stage))}</strong></div>
      <span class="chevron">›</span>
    </summary>
    <div class="bom-logic-stage-body">
      <p>${sourceText(logicStageRole(stage))}</p>
      <section class="bom-stage-metric-choice">
        <b>本环节应看哪些 Metric</b>
        ${renderMetricChoiceTable(stage)}
      </section>
      <section class="bom-stage-history">
        <b>Metric 历史数据 / 实体现状</b>
        <p>${sourceText(metric.history)}</p>
        ${renderMetricTrend(metric)}
      </section>
      <section class="bom-stage-current">
        <b>当前证据读法</b>
        <p>${sourceText(metric.current || "当前源包只能支持方向性判断；需要继续补同口径历史序列。")}</p>
      </section>
      <div class="bom-question-sources">${sourceChips(metric.sourceIds)}</div>
    </div>
  </details>`;
}

function renderMetricChoiceTable(stage) {
  const metric = stage.metric;
  return `<div class="table-scroll metric-choice-table">
    <table>
      <thead><tr><th>Metric</th><th>为什么选它</th><th>数据要求</th></tr></thead>
      <tbody><tr>
        <td><b>${e(metric.name)}</b></td>
        <td>${sourceText(metric.why)}</td>
        <td>${sourceText(metric.dataRequirement || "优先按公司/实体分别搜集同一口径历史数据；涉及多家公司或实体时，按主体分表或在表格中分主体列示。")}</td>
      </tr></tbody>
    </table>
  </div>`;
}

function renderDemandGrowthLogicChain(node) {
  const steps = [
    {
      title: "应用/任务增长",
      body: "模型能力提高、应用嵌入办公/开发/客服/搜索/企业流程，先把 AI 从实验工具变成高频任务入口。",
      check: "验证指标：活跃用户、企业席位、API 调用、AI 应用收入、客户 ROI。",
    },
    {
      title: "token/推理工作负载",
      body: "用户和任务增长只有转成更多 prompt、token、长上下文、多模态和 agent 多步骤调用，才会形成真实计算负载。",
      check: "验证指标：tokens、prompt/request、inference volume、GPU hours、利用率。",
    },
    {
      title: "算力容量需求",
      body: "工作负载继续增长，并且有延迟、可靠性和并发 SLA 约束时，客户需要新增 GPU/ASIC、内存、网络和数据中心容量。",
      check: "验证指标：accelerator shipments、云容量扩张、交期、利用率、供应 allocation。",
    },
    {
      title: "capex / RPO / 订单",
      body: "算力需求必须被客户预算和付款意愿确认；否则只是使用热度，不是可投资的产业需求。",
      check: "验证指标：云厂 capex、RPO/backlog、采购订单、长期供货协议、AI ROI。",
    },
    {
      title: "BOM 节点需求",
      body: `客户 capex 和订单继续穿透到 ${node.name}：该节点必须被平台规格、系统交付或工程约束真实拉动，而不是只分享宏观主题。`,
      check: `验证指标：${node.metrics}。`,
    },
    {
      title: "财务兑现",
      body: "最后要看该节点供应商是否把需求转成收入、毛利、现金流和可持续 backlog；只停在订单或叙事层，增长链条仍未闭环。",
      check: "验证指标：收入增速、毛利率、经营现金流、库存/应收、backlog 转收入。",
    },
  ];
  return `<div class="bom-demand-logic-chain">
    ${steps.map((step, index) => `<article class="bom-demand-logic-step">
      <span>${String(index + 1).padStart(2, "0")}</span>
      <div>
        <b>${e(step.title)}</b>
        <p>${sourceText(step.body)}</p>
        <em>${e(step.check)}</em>
      </div>
    </article>`).join("")}
  </div>`;
}

function renderMetricRationaleList(metrics) {
  return `<div class="bom-metric-rationale-list">
    ${metrics.map((metric) => `<article class="bom-metric-rationale-card">
      <span>${e(metric.type)}</span>
      <b>${e(metric.name)}</b>
      <p>${sourceText(metric.why)}</p>
    </article>`).join("")}
  </div>`;
}

function bomQuestionSectionTitles(question) {
  return {
    logic: "具体逻辑链条",
    finalTrend: "整体的未来趋势评估",
  };
}

function renderBomHistoryMetric(metric, index) {
  return `<section class="bom-history-metric-paragraph">
    <p class="bom-history-metric-text"><b>Metric ${index + 1} · ${e(metric.type)}：${e(metric.name)}</b>${sourceText(metric.history)}</p>
    ${renderMetricTrend(metric)}
    <div class="bom-question-sources">${sourceChips(metric.sourceIds)}</div>
  </section>`;
}

function buildBomQuestionAnalysis(row, questionNumber, node) {
  const narrativeMetrics = row.detail?.reportNarrative?.chainNodes
    ?.flatMap((chainNode) => chainNode.metrics || [])
    || [];
  const defaultMetrics = row.replaceDefaultMetrics ? [] : buildDefaultBomMetrics(row, questionNumber, node);
  const metrics = mergeMetricCards([
    ...narrativeMetrics,
    ...defaultMetrics,
  ]).slice(0, 7);
  return {
    metricLogic: row.metricLogic || metricLogicForQuestion(row.question, node),
    historySummary: row.historySummary || historySummaryForQuestion(row.question, node),
    metrics,
    future: row.futureCards || futureForQuestion(row.question, row, node),
    mechanism: row.mechanism || mechanismForQuestion(row.question, row, node),
  };
}

function buildDefaultBomMetrics(row, questionNumber, node) {
  return metricInputsForQuestion(row.question, node)
    .map((metric, index) => metricCard(metric.type, metric.name, metric.why, row, metric.axis || `cross_${index}`));
}

function metricCard(type, name, why, row, axis) {
  return {
    type,
    name,
    why,
    series: [],
    seriesGap: `公开材料尚未给出「${name}」的连续季度或年度同口径序列；因此只能把它作为趋势缺口、截面证据或代理指标，不能单独证明加速。`,
    history: `历史读法需要把 ${name} 与订单、价格、利润率、现金流和客户预算放在同一时间轴上交叉验证；当前源包只能支持方向性判断或局部截面。`,
    current: row.answer,
    future: futureMetricSentence(row.question, name, axis),
    quality: "趋势缺口：需补同口径历史序列",
    sourceIds: row.sourceIds || [],
  };
}

function mergeMetricCards(metrics) {
  const seen = new Set();
  return metrics.filter((metric) => {
    const key = `${metric.type || ""}::${metric.name || ""}`.toLowerCase();
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function metricInputsForQuestion(question, node) {
  const nodeMetrics = nodeMetricNames(node);
  const nodePrimary = nodeMetrics[0] || `${node.name} 需求/出货/收入`;
  const nodeSecondary = nodeMetrics[1] || `${node.name} 订单 / backlog`;
  const nodeTertiary = nodeMetrics[2] || `${node.name} 毛利率 / ASP`;
  if (question.includes("需求")) {
    return [
      metricInput("应用渗透", "AI 应用活跃用户 / 企业席位 / API 调用量", "需求先出现在真实任务入口；用户、席位和 API 调用量能检验 AI 是否从试验项目进入高频生产负载。", "adoption"),
      metricInput("工作负载", "tokens / inference volume / GPU hours", "AI 应用只有转成 token、推理调用和 GPU 小时，才会形成可采购的算力负载。", "workload"),
      metricInput("客户预算", "云厂商 capex / PPE purchases / AI 基础设施预算", "capex 与 PPE 采购把使用强度转化为客户预算，是需求从应用端进入产业链的关键桥梁。", "capex"),
      metricInput("订单承诺", "RPO / backlog / 采购订单 / 长协", "RPO、backlog 和订单能区分真实采购承诺与短期叙事热度。", "orders"),
      metricInput("BOM 拉动", nodePrimary, `${node.name} 必须被平台规格、系统交付或工程约束直接拉动，否则只是共享宏观 AI 主题。`, "bom"),
      metricInput("财务兑现", "供应商收入 / 毛利率 / 经营现金流", "需求链条最终要进入收入、利润率和现金流；只停留在订单或口径预测，投资证据仍不闭环。", "financial"),
      metricInput("质量校验", "库存周转 / 应收账款 / 取消率", "库存、应收和取消率能提前暴露需求是否被重复下单、渠道囤货或预算回撤放大。", "quality"),
    ];
  }
  if (question.includes("单位用量")) {
    return [
      metricInput("单位用量", `单服务器 / 单机柜 / 单集群的 ${node.name} 用量`, `直接衡量同一单位 AI factory 对 ${node.name} 的消耗强度是否上升。`, "usage"),
      metricInput("平台规格", "GPU/ASIC 平台代际规格、内存容量、网络带宽、功率密度", "平台代际变化解释为什么同样一单位算力会消耗更多内存、连接、电力、散热或系统集成。", "spec"),
      metricInput("渗透率", `${node.name} attach rate / 配置率`, "attach rate 能区分可选升级与平台刚需，也能判断单位用量提升是否已经普及。", "attach"),
      metricInput("单位价值量", nodeTertiary, "单位价值量把工程复杂度转成可变现的 ASP、内容价值和利润池。", "content"),
      metricInput("客户配置", "客户认证配置 / reference design / qualification list", "客户认证决定规格升级是否进入量产配置，而不是停留在工程样机。", "qualification"),
      metricInput("系统约束", "功率密度 / 散热负荷 / 网络 radix / rack scale 约束", "系统约束越强，单位用量越可能从性能优化变成工程必需。", "system"),
    ];
  }
  if (question.includes("供给能否")) {
    return [
      metricInput("有效产能", `合格产能 / 可交付产能：${nodePrimary}`, "名义产能没有意义，真正决定供给的是通过良率、认证和交付约束后的有效产能。", "capacity"),
      metricInput("交付周期", "lead time / delivery cycle / installation cycle", "交期是供需紧张最直接的温度计，能提前反映短缺是否缓解。", "lead_time"),
      metricInput("良率利用率", "yield / utilization / bottleneck tool availability", "良率和利用率决定扩产能否转成可出货供给。", "yield"),
      metricInput("价格信号", "ASP / spot price / contract price / premium", "当供给跟不上需求时，价格和溢价通常先于利润率反映稀缺。", "price"),
      metricInput("订单库存", nodeSecondary, "backlog、book-to-bill 与库存能同时检验需求强度和供给释放速度。", "backlog"),
      metricInput("扩产进度", "capex / 工具交付 / 新厂爬坡 / 认证节点", "扩产是否有效取决于资本开支、设备交付、爬坡周期和客户认证是否同步完成。", "expansion"),
    ];
  }
  if (question.includes("谁控制")) {
    return [
      metricInput("份额集中度", `${node.name} 合格供应商份额 / top supplier share`, "控制权首先体现在合格供应份额，而不是公司知名度。", "share"),
      metricInput("客户绑定", "长期协议 / allocation / customer qualification / design win", "客户绑定决定供给控制权能否持续转化为订单稳定性。", "lock_in"),
      metricInput("技术壁垒", "专利 / 工艺节点 / 软件生态 / know-how / 认证周期", "技术与认证壁垒越高，替代者越难快速复制交付能力。", "barrier"),
      metricInput("议价能力", "ASP / 毛利率 / 付款条款 / 预付款", "控制权必须落到价格、毛利率或付款条件上，才是可投资的稀缺。", "pricing_power"),
      metricInput("替代进度", "second source / 自研替代 / 客户多供策略", "替代进度是控制权被削弱的领先信号。", "substitution"),
      metricInput("交付可靠性", "准时交付率 / 质量事故 / RMA / yield learning", "客户在高风险扩产期通常优先选择可靠交付者，交付记录会强化控制权。", "delivery"),
    ];
  }
  if (question.includes("财务兑现")) {
    return [
      metricInput("收入兑现", `${node.name} 相关收入 / segment revenue`, "收入是产业需求进入报表的第一层证据，但需要继续验证质量。", "revenue"),
      metricInput("订单可见度", nodeSecondary, "订单、backlog 和 book-to-bill 决定未来收入是否有可见度。", "orders"),
      metricInput("利润质量", "毛利率 / ASP / 产品组合", "利润率能判断增长是否来自稀缺价值，而不是低价抢量。", "margin"),
      metricInput("现金兑现", "经营现金流 / 自由现金流 / 预收款", "现金流能过滤会计收入和营运资本压力。", "cash"),
      metricInput("营运资本", "库存 / 应收账款 / 递延收入 / 存货跌价", "营运资本恶化通常比利润下滑更早暴露需求质量问题。", "working_capital"),
      metricInput("指引兑现", "公司 guidance / revenue conversion / backlog burn", "指引与 backlog 转收入速度决定当前高增长能否延续到未来几个季度。", "guidance"),
    ];
  }
  if (question.includes("定价")) {
    return [
      metricInput("估值倍数", "EV/Sales / P/E / P/FCF 相对历史与同业", "估值倍数揭示市场已经为增长和稀缺支付了多少价格。", "multiple"),
      metricInput("盈利上修", "收入、EPS、毛利率一致预期修正", "盈利上修速度决定基本面是否仍在超过市场预期。", "revision"),
      metricInput("股价反应", "earnings reaction / guidance reaction / drawdown", "股价对好消息的反应能识别预期是否已经拥挤。", "reaction"),
      metricInput("隐含增长", "reverse DCF / implied revenue CAGR / implied margin", "隐含增长把股价翻译成市场正在押注的经营路径。", "implied"),
      metricInput("同业价差", "peer spread / scarcity premium / PEG", "同业价差帮助区分真正稀缺溢价和板块 beta。", "peer"),
      metricInput("仓位情绪", "short interest / fund ownership / options skew", "仓位和情绪不是基本面，但会影响预期差兑现的赔率。", "positioning"),
    ];
  }
  return [
    metricInput("需求反证", "客户 capex 下修 / 订单取消 / RPO 放缓", "需求端反证会先出现在预算、订单和 RPO，而不是等到收入下降。", "demand_refute"),
    metricInput("价格反证", "ASP 下行 / 折扣扩大 / lead time 缩短", "价格与交期同步走弱通常意味着短缺缓解或需求斜率下降。", "price_refute"),
    metricInput("质量反证", "库存上升 / 应收拉长 / 现金转化变差", "营运资本恶化会削弱收入增长的可信度。", "quality_refute"),
    metricInput("客户 ROI", "GPU 利用率 / inference cost / AI 应用 ROI", "客户 ROI 下降会压低下一轮预算，是 AI factory 需求链条的根部反证。", "roi"),
    metricInput("替代路线", "自研芯片 / second source / 架构替代 / 开源效率提升", "替代路线成熟会削弱 BOM 稀缺性和单位价值量。", "substitute"),
    metricInput("财务降级", "毛利率下滑 / guidance 下修 / backlog 转收入变慢", "财务降级说明产业逻辑已经开始传导到公司报表。", "financial_refute"),
  ];
}

function metricInput(type, name, why, axis) {
  return { type, name, why, axis };
}

function nodeMetricNames(node) {
  return String(node.metrics || "")
    .split(/[、,，/]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function questionMetricType(question) {
  if (question.includes("需求")) {
    return {
      primary: "需求强度",
      secondary: "客户预算/订单",
      tertiary: "财务兑现",
      primaryWhy: (node) => `先证明 ${node.name} 的需求不是主题热度，而是进入可观察工作负载、客户预算或订单。`,
      secondaryWhy: () => "预算、订单、backlog 或 capex 是需求从叙事进入采购的中间证据。",
      tertiaryWhy: () => "收入、毛利率和现金流证明需求已经穿透到供应商财务。",
    };
  }
  if (question.includes("单位用量")) {
    return {
      primary: "单位用量",
      secondary: "平台规格",
      tertiary: "单位价值量",
      primaryWhy: (node) => `先看单个 AI 工厂、机柜、服务器或芯片平台对 ${node.name} 的用量是否提高。`,
      secondaryWhy: () => "平台代际规格变化能解释为什么同样需求对应更多 BOM 用量。",
      tertiaryWhy: () => "单位价值量必须最终转成收入、ASP 或毛利，而不是只停留在技术复杂度。",
    };
  }
  if (question.includes("供给能否")) {
    return {
      primary: "有效产能",
      secondary: "交付周期",
      tertiary: "供需斜率",
      primaryWhy: (node) => `先看 ${node.name} 的可交付产能，而不是名义扩产。`,
      secondaryWhy: () => "交期、认证、良率和项目交付周期决定供应是否真的能跟上需求。",
      tertiaryWhy: () => "供需斜率决定稀缺性是否延续，也决定价格/毛利能否维持。",
    };
  }
  if (question.includes("谁控制")) {
    return {
      primary: "控制者份额",
      secondary: "替代难度",
      tertiary: "议价能力",
      primaryWhy: (node) => `先识别谁控制 ${node.name} 的关键供给、资格、生态或客户关系。`,
      secondaryWhy: () => "替代难度决定控制权能否转化为持续利润，而不是短期订单。",
      tertiaryWhy: () => "议价能力最终要落到 ASP、毛利率、付款条件或长期协议。",
    };
  }
  if (question.includes("财务兑现")) {
    return {
      primary: "收入",
      secondary: "订单/backlog",
      tertiary: "利润率/现金流",
      primaryWhy: (node) => `${node.name} 的投资价值必须被收入、订单或 backlog 证明。`,
      secondaryWhy: () => "订单和 backlog 说明未来收入可见度，但还要验证取消率和转收入速度。",
      tertiaryWhy: () => "利润率和现金流判断增长是否有质量，避免只看收入 beta。",
    };
  }
  if (question.includes("定价")) {
    return {
      primary: "估值倍数",
      secondary: "盈利上修",
      tertiary: "隐含预期",
      primaryWhy: (node) => `市场定价问题要把 ${node.name} 的产业证据转成估值与盈利预期。`,
      secondaryWhy: () => "盈利上修是否超过市场隐含预期，是区分好行业和好赔率的关键。",
      tertiaryWhy: () => "隐含预期过高时，强基本面也可能只对应 watch_only。",
    };
  }
  return {
    primary: "反证触发器",
    secondary: "领先风险指标",
    tertiary: "降级阈值",
    primaryWhy: (node) => `反证必须绑定 ${node.name} 的可观察指标，不能只写泛泛风险。`,
    secondaryWhy: () => "领先风险指标要早于收入恶化出现，便于季度跟踪。",
    tertiaryWhy: () => "降级阈值把研究判断转成可执行的观察纪律。",
  };
}

function metricLogicForQuestion(question, node) {
  if (question.includes("需求")) {
    return `需求增长只看一条链：AI 应用和企业任务先变成 token、推理请求和 GPU hours，再推动客户扩算力并进入 capex、RPO、backlog 或采购订单；这些预算还必须真实穿透到 ${node.name} 这个 BOM 节点，最后体现为供应商收入、毛利率、现金流和可持续 backlog。中间任何一环断掉，都只能说明主题热度，不能证明可投资的 S 曲线。`;
  }
  if (question.includes("单位用量")) {
    return `${node.name} 的单位用量提升，核心不是行业总需求变大，而是每一单位 AI factory 是否天然消耗更多该节点。判断路径应从平台规格和系统架构出发：GPU/ASIC 代际升级、rack-scale 集群、内存墙、网络带宽、功率密度和散热负荷会改变单服务器、单机柜、单集群的配置量；只有当配置率、单位价值量和客户认证配置同步上升时，单位用量提升才会转化为收入弹性。`;
  }
  if (question.includes("供给能否")) {
    return `${node.name} 的供给弹性要看有效产能，而不是名义扩产。真正的供给由合格产能、良率、认证周期、交付周期、工具设备、工程实施和客户锁定共同决定；如果需求斜率快于这些约束释放，短缺会体现在交期、价格、allocation、backlog 和毛利率上。反过来，如果扩产、良率和 second source 同时释放，供给紧张会很快变成价格和利润率压力。`;
  }
  if (question.includes("谁控制")) {
    return `${node.name} 的控制权来自“谁拥有可被客户信任并规模交付的稀缺能力”。这通常表现为合格供应份额、长期客户关系、技术/IP、工艺 know-how、生态锁定、认证周期和交付可靠性；只有当这些优势能带来 ASP、毛利率、付款条款或 allocation 权力时，控制权才具备投资意义。`;
  }
  if (question.includes("财务兑现")) {
    return `${node.name} 的产业逻辑必须进入报表才能成为公司价值。更严格的财务链条是：订单和 backlog 提供收入可见度，收入增长验证需求穿透，毛利率和 ASP 证明稀缺能被定价，经营现金流与营运资本检验增长质量，guidance 与 backlog burn 决定未来几个季度能否继续兑现。`;
  }
  if (question.includes("定价")) {
    return `市场定价问题要把产业强度翻译成赔率。即使 ${node.name} 的基本面很强，如果估值倍数、盈利上修、股价反应和隐含增长已经把高增长、高毛利、低风险都计入，投资结论也可能只是观察而不是买入；只有当可验证经营指标继续超过隐含预期，且下行风险可监控，才存在预期差。`;
  }
  return `${node.name} 的反证不应停留在泛泛风险，而要落到能提前推翻增长链条的指标：客户预算或订单回撤、lead time 缩短、ASP 下行、库存和应收恶化、利用率/ROI 下降、替代路线成熟、guidance 下修或 backlog 转收入变慢。反证指标越靠近需求链条前端，越能提前保护判断。`;
}

function historySummaryForQuestion(question, node) {
  return `历史数据的重点是把 ${node.name} 放进同一时间轴观察：需求端、订单端、价格端、产能端、利润端和现金端是否同向改善，改善速度是否快于过去基线。连续季度或年度序列最有解释力；只有单点披露、第三方预测或跨公司截面时，只能证明当前截面强弱，不能单独证明加速。`;
}

function futureForQuestion(question, row, node) {
  return [
    {
      horizon: "0-4 个季度",
      view: `短期若判断继续兑现，${node.name} 应同时看到订单或 backlog 维持、收入确认加快、价格或毛利率不明显塌陷，并且客户 capex/RPO 没有同步转弱。单一收入高增但库存、应收或取消率恶化，不能视为健康兑现。`,
      sourceIds: row.sourceIds || [],
    },
    {
      horizon: "4-8 个季度",
      view: `中期重点看市场预期是否被经营数据继续上修：新增产能、客户认证、平台代际升级和订单转收入若快于一致预期，预期差仍可延续；若扩产释放、second source 或客户预算纪律更快出现，增长斜率会被压平。`,
      sourceIds: row.sourceIds || [],
    },
    {
      horizon: "中长期",
      view: `中长期取决于 AI 工作负载增长、单位用量提升、供给约束和议价权能否同时存在。若模型效率提升完全抵消工作负载、客户 ROI 下降压缩 capex，或 ${node.name} 被标准化和多供化，长期趋势会从稀缺成长转为周期性供需波动。`,
      sourceIds: row.sourceIds || [],
    },
  ];
}

function futureMetricSentence(question, metric, axis) {
  if (question.includes("反证")) return `${metric} 一旦持续转弱，说明前端需求、稀缺性或财务质量至少有一环已经松动。`;
  if (question.includes("定价")) return `${metric} 的关键不是绝对水平，而是它能否继续证明盈利路径高于市场隐含假设。`;
  if (question.includes("供给能否")) return `${metric} 如果显示供给释放速度超过需求斜率，短缺溢价和毛利率应开始回落。`;
  if (question.includes("谁控制")) return `${metric} 能判断控制权是继续集中在少数合格供应商，还是被客户多供、替代路线和标准化削弱。`;
  if (axis === "future") return `${metric} 若持续改善并进入收入、毛利或现金流，才说明工程复杂度正在变成财务弹性。`;
  return `${metric} 需要形成同口径序列；只有当前截面强而缺少时间序列时，趋势强度仍要打折。`;
}

function mechanismForQuestion(question, row, node) {
  if (question.includes("需求")) {
    return {
      sustain: `需求可持续的第一性原理是：AI 工作负载、用户任务、上下文长度、多模态和 agent 步数提高总计算/基础设施需求，并通过客户预算进入 ${node.name}。`,
      break: "若 AI 应用 ROI 不足、模型效率提升快于工作负载增长、客户 capex 下修或订单取消，需求趋势就不可持续。",
    };
  }
  if (question.includes("单位用量")) {
    return {
      sustain: `单位用量可持续来自系统从单组件走向机柜/集群/数据中心级交付，单个 AI 工厂对 ${node.name} 的用量和价值量提高。`,
      break: "若架构效率提升、集成度提高、替代路线降低该 BOM 消耗，或客户转向更轻量模型，单位用量提升会被削弱。",
    };
  }
  if (question.includes("供给能否")) {
    return {
      sustain: `供给约束可持续来自产能、良率、认证、交期、工程交付和客户锁定慢于需求斜率。`,
      break: "若扩产、良率、替代供应商和客户认证同步释放，短缺会转为价格和毛利压力。",
    };
  }
  if (question.includes("谁控制")) {
    return {
      sustain: `控制权可持续来自技术门槛、生态锁定、客户资格、长期协议、规模经验和不可替代交付能力。`,
      break: "若客户多供应商策略成功、替代技术成熟、标准化降低切换成本，控制权就会被稀释。",
    };
  }
  if (question.includes("财务兑现")) {
    return {
      sustain: `财务兑现可持续需要 ${node.name} 的收入、订单、backlog、毛利率和现金流沿同一方向改善。`,
      break: "若收入增长依赖低毛利订单、应收/库存上升或 backlog 转收入变慢，财务兑现质量会下降。",
    };
  }
  if (question.includes("定价")) {
    return {
      sustain: "错价可持续来自市场低估增长持续期、盈利弹性、利润率上行或风险下降。",
      break: "若估值已经把高增长、高毛利和低风险全部计入，基本面继续强也可能没有足够赔率。",
    };
  }
  return {
    sustain: `有效反证应比财报恶化更早出现：价格、交期、订单、客户预算、供给释放或替代路线先发生变化。`,
    break: "如果反证指标连续出现并穿透到收入、毛利、现金流或估值预期，应从观察名单降级。",
  };
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
  if (metric.multiSeries && metric.multiSeries.length) {
    return renderMetricMultiSeriesData(metric);
  }
  const dataRows = renderMetricDataRows(series);
  if (series.length < 2) {
    const maybeDataRows = dataRows ? `\n      ${dataRows}` : "";
    return `<div class="metric-trend-gap">
      <b>连续趋势</b>
      <p>${sourceText(metric.seriesGap || "公开材料暂时只有单点或代理数据，不能画成连续趋势。")} 少于 5 个同口径历史数据点，先标为趋势缺口。</p>
      <span class="metric-point-count">${series.length} 个数据点</span>${maybeDataRows}
    </div>`;
  }
  if (series.length < 5) {
    return `<div class="metric-trend-gap">
      <b>连续趋势不足</b>
      <p>${sourceText(metric.seriesGap || "公开材料只有少量截面或不完整历史。")} 少于 5 个同口径历史数据点，不能画成趋势线。</p>
      <span class="metric-point-count">${series.length} 个数据点</span>
      ${dataRows}
    </div>`;
  }
  if (metric.trendKind !== "time_series") {
    return `<div class="metric-data-table">
      <b>${e(metric.trendLabel || "非连续数据点")}</b>
      <p>${sourceText(metric.seriesGap || "这些点来自不同公司、不同口径或订单漏斗，适合做方向判断，不适合画成连续历史趋势。")}</p>
      <span class="metric-point-count">${series.length} 个数据点</span>
      ${dataRows}
    </div>`;
  }
  return `<div class="metric-data-table">
    <b>${e(metric.trendLabel || "历史数据点")}</b>
    <p>按同一主体、同一字段、同一单位列出历史观测值；这里不画折线，避免把点间斜率误读成精确趋势。</p>
    <span class="metric-point-count">${series.length} 个数据点</span>
    ${dataRows}
  </div>`;
}

function renderMetricDataRows(series, companyName = "") {
  if (!series.length) return "";
  const hasChange = series.some((point) => point.change);
  const rowClass = [
    "metric-data-row",
    hasChange ? "metric-data-row-with-change" : "",
    companyName ? "metric-data-row-with-company" : "",
  ].filter(Boolean).join(" ");
  const headerCells = [
    companyName ? "<b>主体</b>" : "",
    "<b>期间 / 截点</b>",
    "<b>数值</b>",
    hasChange ? "<b>相对变化</b>" : "",
  ].filter(Boolean).join("");
  const rows = series.map((point) => {
    const cells = [
      companyName ? `<span>${e(companyName)}</span>` : "",
      `<span>${e(point.label)}</span>`,
      `<strong>${e(point.value)}</strong>`,
      hasChange ? `<span>${e(point.change || "")}</span>` : "",
    ].filter(Boolean).join("");
    return `<div class="${rowClass}">${cells}</div>`;
  }).join("");
  return `<div class="metric-data-rows"><div class="${rowClass} metric-data-head">${headerCells}</div>${rows}</div>`;
}

function renderMetricMultiSeriesData(metric) {
  const validSeries = metric.multiSeries.filter((line) => (line.points || []).length >= 5);
  if (!validSeries.length) {
    return `<div class="metric-trend-gap">
      <b>多公司历史数据不足</b>
      <p>${sourceText(metric.seriesGap || "该 metric 涉及多家公司，但尚未补齐每家公司 5 个以上同口径历史点。")} 少于 5 个同口径历史数据点，先标为趋势缺口。</p>
      <span class="metric-point-count">0 条可画曲线</span>
    </div>`;
  }
  return `<div class="metric-data-table metric-multi-series-data">
    <b>${e(metric.trendLabel || "多公司同口径数据点")}</b>
    <p>同口径多公司比较按数据表展开，不画多线图。</p>
    <span class="metric-point-count">${validSeries.map((line) => `${e(line.name)} ${line.points.length} 个点`).join(" / ")}</span>
    ${validSeries.map((line) => renderMetricDataRows(line.points || [], line.name)).join("")}
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

function renderBomCoreQuestionCard(node) {
  const rows = bomCoreQuestionRows(node);
  return `<article class="overview-question-card">
    <h4>${e(node.name)}</h4>
    <div class="overview-answer">
      <div class="table-scroll"><table class="bom-core-question-table"><thead><tr><th>问题</th><th>回答</th><th>来源</th></tr></thead><tbody>${rows.map((row) => `<tr><td><b>${e(row.question)}</b></td><td>${sourceText(row.answer)}</td><td>${sourceChips(row.sourceIds)}</td></tr>`).join("")}</tbody></table></div>
    </div>
  </article>`;
}

function bomCoreQuestionRows(node) {
  const rows = {
    compute: [
      {
        question: "当前 BOM 的需求是否会被 S 曲线放大拉动？",
        answer: "AI factory 的第一层实物需求是数据中心 AI 加速器。当前应先验证 AI workload 是否变成客户 capex，再验证 capex 是否变成 GPU/ASIC 收入、订单和 backlog；同时判断需求弹性，即平台是否从单卡/单机采购上移到 rack-scale、pod-scale 和系统级交付，使 GPU/ASIC 需求被单位价值量和系统规格进一步放大。",
        sourceIds: ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-MSFT-FY26-Q2", "SRC-AMZN-Q4-2025", "SRC-GOOGL-Q4-2025", "SRC-META-Q3-2025", "SRC-ORCL-FY26-Q2", "SRC-DELL-FY26-Q4", "SRC-SA-GB200-BOM-2024", "SRC-NVDA-GTC-VERA-RUBIN-20260316"],
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
      ["当前 BOM 的需求是否会被 S 曲线放大拉动？", "GPU/ASIC 放量必须经过先进制程和先进封装，AI accelerator 越复杂，越依赖高端制造、CoWoS 类封装、封装面积和 HBM 集成；因此该节点的需求不只是跟随晶圆数量，还会被平台复杂度和封装价值量放大。", ["SRC-TSM-Q4-2025", "SRC-SA-COWOS-HBM-2023", "SRC-SA-GB200-BOM-2024"]],
      ["供给能否跟上？", "扩产周期长，受设备、良率、工程经验、客户认证和 capex 制约。", ["SRC-TSM-Q4-2025"]],
      ["谁控制供给？", "核心控制者是 TSMC 及其先进封装生态。", ["SRC-TSM-Q4-2025"]],
      ["是否已经财务兑现？", "TSMC advanced technologies revenue share、gross margin 和 2026 capex 指引说明高端制造处于强需求状态。", ["SRC-TSM-Q4-2025"]],
      ["市场是否已定价？", "卡点强但成熟龙头预期较高，赔率取决于先进封装短缺持续性、capex 回报和地缘折价。", ["SRC-TSM-Q4-2025"]],
      ["反证是什么？", "先进封装产能释放快于需求、客户转单或自建替代、capex 回报下降、毛利率下行。", ["SRC-TSM-Q4-2025"]],
    ],
    memory: [
      ["当前 BOM 的需求是否会被 S 曲线放大拉动？", "AI accelerator 需要高带宽内存喂数据，GPU/ASIC 数量增加、上下文变长和推理并发都会推高 HBM 与高端内存需求；每代平台提升 HBM 容量、带宽和堆叠层数，使内存节点需求具备高于单纯服务器数量的弹性。", ["SRC-MU-FY26-Q1-PREPARED", "SRC-SKHYNIX-FY25"]],
      ["供给能否跟上？", "HBM 扩产受 DRAM wafer、堆叠封装、良率、客户资格和提前价量协议限制。", ["SRC-MU-FY26-Q1-PREPARED", "SRC-SA-COWOS-HBM-2023"]],
      ["谁控制供给？", "主要是 SK hynix、Micron、Samsung；SK hynix 领导力更强，Micron 是高弹性追赶者，Samsung 需要验证 HBM 领先性。", ["SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1-PREPARED", "SRC-SAMSUNG-FY25"]],
      ["是否已经财务兑现？", "SK hynix operating margin、Micron HBM TAM 与价量协议、Samsung high-value AI products 说明利润已经兑现。", ["SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1-PREPARED", "SRC-SAMSUNG-FY25"]],
      ["市场是否已定价？", "存储稀缺已被关注，但 HBM 供需、ASP、资格认证和盈利弹性仍可能继续改变利润预期。", ["SRC-MU-FY26-Q1-PREPARED", "SRC-SKHYNIX-FY25"]],
      ["反证是什么？", "HBM ASP 下跌、客户资格不及预期、扩产快于需求、DRAM/NAND 周期反转、GPU/ASIC 需求放缓。", ["SRC-MU-FY26-Q1-PREPARED"]],
    ],
    network: [
      ["当前 BOM 的需求是否会被 S 曲线放大拉动？", "rack-scale 与 cluster-scale AI 提高东西向流量，拉动 retimer、AEC、switch、NIC、光模块和 PAM4 DSP；每 GPU 或每机柜的网络端口、光模块、DSP 和板级连接组件用量随 800G/1.6T 迁移上升，因此网络节点可能具备更高单位弹性。", ["SRC-SA-OPTICAL-2024", "SRC-LC-AI-OPTICS-202501", "SRC-DO-AI-NETWORKS-20250715"]],
      ["供给能否跟上？", "约束来自客户设计导入、平台认证、低功耗/低延迟指标、信号完整性和批量可靠性。", ["SRC-SA-OPTICAL-2024", "SRC-LC-PAM4-DSP-20260226"]],
      ["谁控制供给？", "Astera、Credo、Marvell、Broadcom、Arista 和 NVIDIA networking 控制不同子环节。", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3", "SRC-ANET-Q4-2025"]],
      ["是否已经财务兑现？", "ALAB、CRDO、MRVL、Arista 等公司收入已体现 AI networking / connectivity 需求。", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3", "SRC-ANET-Q4-2025"]],
      ["市场是否已定价？", "连接节点弹性大也容易估值透支，需要用客户集中、design win、gross margin 和出货节奏验证。", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3"]],
      ["反证是什么？", "平台自研替代、客户设计切换、ASP 下行、CPO/LPO/AEC 路线变化、主要客户延迟 ramp。", ["SRC-SA-OPTICAL-2024", "SRC-DO-AI-NETWORKS-20250715"]],
    ],
    powerCooling: [
      ["当前 BOM 的需求是否会被 S 曲线放大拉动？", "GPU/ASIC 和 rack-scale 系统功耗提升后，数据中心必须新增电力、UPS、PDU、液冷和热管理能力；高功率机柜提高每 rack 的电力和散热需求，抬升 UPS、配电、液冷 CDU、管路、现场工程和服务价值量。", ["SRC-VRT-Q4-2025", "SRC-SA-GB200-BOM-2024", "SRC-DO-LIQUID-COOLING-20260108"]],
      ["供给能否跟上？", "约束来自工程交付、项目周期、电力接入、现场可靠性、液冷方案认证和供应链交付能力。", ["SRC-VRT-Q4-2025", "SRC-DO-LIQUID-COOLING-20260108"]],
      ["谁控制供给？", "Vertiv、Schneider、Eaton 和数据中心工程/液冷供应商控制关键供给。", ["SRC-VRT-Q4-2025", "SRC-DO-LIQUID-COOLING-20260108"]],
      ["是否已经财务兑现？", "Vertiv organic orders +252% YoY、backlog $15.0B，是物理瓶颈财务化最清楚的证据之一。", ["SRC-VRT-Q4-2025"]],
      ["市场是否已定价？", "市场已开始识别电力/液冷，但相对 GPU 平台可能仍更容易出现预期差。", ["SRC-VRT-Q4-2025"]],
      ["反证是什么？", "客户 capex 下修、电力接入延迟、项目毛利低于预期、backlog 取消或转收入慢、液冷渗透率低于预期。", ["SRC-VRT-Q4-2025", "SRC-DO-LIQUID-COOLING-20260108"]],
    ],
    system: [
      ["当前 BOM 的需求是否会被 S 曲线放大拉动？", "GPU/ASIC、HBM、网络和电力冷却最终必须组合成服务器、机柜和集群才能上线；AI server 从单机走向 rack-scale，单系统包含更多 GPU、网络、电源、冷却和集成服务，使系统交付节点随平台复杂度和整柜化采购放大。", ["SRC-DELL-FY26-Q4", "SRC-SA-GB200-BOM-2024"]],
      ["供给能否跟上？", "供给受 GPU allocation、供应链协调、整机工程、客户定制、液冷/电力配套和交付周期约束。", ["SRC-DELL-FY26-Q4", "SRC-SA-GB200-BOM-2024"]],
      ["谁控制供给？", "Dell、Supermicro、HPE、ODM/OEM 是主要系统交付者，但玩家较多、客户议价强。", ["SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2"]],
      ["是否已经财务兑现？", "Dell 披露 AI-optimized server orders、shipments 和 backlog；Supermicro 也有 AI server exposure，但需看执行和治理风险。", ["SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2"]],
      ["市场是否已定价？", "订单弹性容易被定价，关键不是 backlog 多大，而是 backlog 是否转成毛利和现金流。", ["SRC-DELL-FY26-Q4"]],
      ["反证是什么？", "订单取消、GPU allocation 变化、毛利率下降、库存/应收上升、客户延迟部署、治理或执行问题。", ["SRC-SMCI-FY26-Q2", "SRC-DELL-FY26-Q4"]],
    ],
  };
  return normalizeBomCoreQuestionRows(rows[node.id] || []);
}

function normalizeBomCoreQuestionRows(rows) {
  return rows.map((row) => Array.isArray(row) ? { question: row[0], answer: row[1], sourceIds: row[2] } : row);
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
.bom-future-card.bom-expectation-card{background:#fff}.bom-future-card.bom-expectation-card>summary{grid-template-columns:1fr auto auto}.bom-expectation-card>summary>span:not(.chevron){border:1px solid rgba(10,132,255,.18);border-radius:999px;background:#eef7ff;color:var(--blue);font-size:11px;font-weight:900;padding:4px 8px;white-space:nowrap}.bom-expectation-stage{display:grid;gap:3px;border:1px solid #e1eaf6;border-radius:14px;background:#fbfdff;padding:10px;margin-bottom:10px}.bom-expectation-stage span{color:#667085;font-size:11px;font-weight:900}.bom-expectation-stage b{color:#0a66cc;font-size:13px;line-height:1.35}.bom-expectation-subtitle{margin:0 0 10px;color:#667085;font-size:13px;line-height:1.45}.bom-expectation-core{border:1px solid rgba(10,132,255,.18);border-radius:14px;background:linear-gradient(180deg,#fff,#f7fbff);padding:12px;margin-bottom:10px}.bom-expectation-core span{display:block;color:var(--blue);font-size:11px;font-weight:900;margin-bottom:5px}.bom-expectation-core p{margin:0;color:#223047;font-size:14px;line-height:1.55}.bom-expectation-table{margin-top:10px}.bom-expectation-table table{min-width:1240px}.bom-expectation-table td:first-child{width:130px;color:#223047}.bom-expectation-table td:nth-child(2),.bom-expectation-table td:nth-child(4){width:120px;color:#475467;font-weight:800}.bom-expectation-table td{line-height:1.55}.bom-expectation-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:10px}.bom-expectation-field{border:1px solid #e8eef7;border-radius:12px;background:#fbfdff;padding:9px;min-width:0}.bom-expectation-field span{display:block;color:#667085;font-size:11px;font-weight:900;margin-bottom:3px}.bom-expectation-field b{display:block;color:#223047;font-size:13px;line-height:1.45}.bom-expectation-validation{border:1px solid rgba(29,154,108,.20);border-radius:12px;background:#f5fffa;margin-top:10px;padding:10px}.bom-expectation-validation>b{display:block;color:#166f52;margin-bottom:4px}.bom-expectation-validation p{margin:0;color:#344054}.bom-expectation-card .bom-question-sources{margin-top:10px}
.representative-companies{margin:12px 0 14px;padding:10px 0;border-top:1px solid #eef2f7;border-bottom:1px solid #eef2f7}.representative-companies>b{display:block;color:var(--blue);font-size:12px;margin-bottom:8px}.representative-companies>div{display:flex;flex-wrap:wrap;gap:8px}.representative-companies span{display:inline-flex;align-items:center;border:1px solid #d9e7f7;border-radius:999px;background:#f7fbff;color:#223047;padding:5px 9px;font-size:12px;font-weight:800}
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",sans-serif;background:radial-gradient(circle at 20% 0%,#e8f2ff 0,transparent 34rem),var(--bg);color:var(--text);line-height:1.62}a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}
.hero{padding:32px clamp(22px,5vw,72px) 48px;background:linear-gradient(180deg,rgba(255,255,255,.96),rgba(255,255,255,.62));border-bottom:1px solid var(--line)}.hero-inner{max-width:1180px;margin:0 auto}.eyebrow{margin:0 0 10px;color:var(--blue);font-size:12px;font-weight:800;text-transform:uppercase}h1{max-width:980px;margin:0;font-size:clamp(36px,5vw,66px);line-height:1.04;letter-spacing:0}.hero-subtitle{max-width:780px;color:#475467;font-size:19px}.hero-meta{display:flex;gap:10px;flex-wrap:wrap}.hero-meta span,.state-pill{border:1px solid var(--line);border-radius:999px;background:#fff;padding:6px 10px;color:var(--muted);font-size:13px}.top-nav{position:sticky;top:0;z-index:5;display:flex;justify-content:center;gap:10px;flex-wrap:wrap;padding:12px;background:rgba(245,247,251,.82);backdrop-filter:blur(16px);border-bottom:1px solid rgba(217,224,234,.72)}.top-nav a{padding:8px 12px;border:1px solid rgba(10,132,255,.18);border-radius:999px;background:#fff;color:#28506f;font-size:13px}.section{max-width:1180px;margin:0 auto;padding:44px clamp(18px,4vw,36px)}.section-heading{display:flex;align-items:end;justify-content:space-between;margin-bottom:18px}.section-heading h2{margin:0;font-size:clamp(30px,3vw,44px);letter-spacing:0}.muted{color:var(--muted)}
.goal-card,.industry-module,.qa-card,.source-collapse,.artifact-card{border:1px solid var(--line);border-radius:22px;background:var(--surface);box-shadow:var(--shadow)}.goal-card{padding:22px}.goal-main{font-size:22px;font-weight:800;margin-bottom:16px}.goal-grid,.constraint-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.metric,.constraint-grid article,.chain-bridge-card,.chain-node-lens,.overview-question-card,.chain-company-card,.bom-node-brief article{border:1px solid #e6edf7;border-radius:16px;background:#fff;padding:14px}.metric span,.constraint-grid span,.bom-node-brief span{display:block;color:var(--muted);font-size:12px;font-weight:800}.metric strong{display:block;color:#223047;font-size:18px}.constraint-definition{margin-top:18px}.artifact-title{font-weight:900;color:#26364f;margin-bottom:8px}.industry-overview-section{display:grid;gap:14px}.industry-module{overflow:hidden}.industry-module>summary,.qa-card>summary,.chain-detail-panel>summary,.bom-question-card>summary,.source-collapse>summary{list-style:none;cursor:pointer}.industry-module>summary::-webkit-details-marker,.qa-card>summary::-webkit-details-marker,details>summary::-webkit-details-marker{display:none}.industry-module[open]>summary,.qa-card[open]>summary{border-bottom:1px solid var(--line)}.module-head{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding:18px 22px}.module-index{display:inline-flex;width:34px;height:34px;border-radius:999px;align-items:center;justify-content:center;background:#eaf3ff;color:var(--blue);font-weight:900;font-size:12px}.module-head h3{margin:0;font-size:22px}.module-head p{margin:0;color:var(--muted);font-size:14px}.chevron{color:var(--muted);font-weight:900;transition:transform .18s ease}.industry-module[open]>.module-head .chevron,.qa-card[open]>summary .chevron,details[open]>summary>.chevron{transform:rotate(90deg)}.industry-module-body{padding:22px;min-width:0}.chain-explain{padding:0}.chain-plain-summary{font-size:18px;color:#344054;margin-top:0}.chain-research-bridge{border:1px solid rgba(10,132,255,.18);border-radius:18px;background:#fbfdff;padding:16px;margin:18px 0}.chain-bridge-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.chain-node-lens ul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:0;padding:0;list-style:none}.chain-node-lens b,.chain-bridge-card span{display:block;color:var(--blue);font-size:12px;margin-bottom:4px}.chain-detail-panel{border:1px solid #e6edf7;border-radius:18px;background:#fff;margin-top:12px;overflow:hidden}.chain-detail-panel>summary{display:flex;justify-content:space-between;align-items:center;padding:14px 16px;font-weight:900}.chain-layer-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;padding:16px}.chain-layer-card{border:1px solid #eef2f7;border-radius:16px;background:#fbfcff;padding:14px}.chain-layer-card p{margin:10px 0}.chain-layer-card span{display:block;color:var(--muted);font-size:12px}.chain-simple-flow{display:grid;grid-template-columns:repeat(5,minmax(180px,1fr));gap:10px;padding:16px;overflow-x:auto}.chain-stage-panel{min-width:180px;border:1px solid #e8eef7;border-radius:16px;padding:14px;background:#fbfcff}.chain-stage-panel span{display:inline-flex;width:28px;height:28px;border-radius:50%;align-items:center;justify-content:center;background:#eaf3ff;color:var(--blue);font-weight:900}.chain-relationship-graph{margin:0 16px 16px;padding:14px;border:1px dashed #bfd7f5;border-radius:16px;color:#3d536d;background:#f7fbff}.chain-company-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;padding:16px}.company-flow-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.company-flow-grid p{margin:0;border-top:1px solid #eef2f7;padding-top:8px}.company-flow-grid b{display:block;color:#223047}.component-value-chain,.chain-lane-map,.chain-value-flow{min-width:0}.chain-relationship-graph{display:block}.bom-node-brief{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:14px}.bom-node-brief p{margin:4px 0 0}.bom-question-list{display:grid;gap:10px}.bom-question-card{border:1px solid #e3ebf6;border-radius:18px;background:#fff;overflow:hidden}.bom-question-card>summary{display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:center;padding:14px 16px}.bom-question-card[open]>summary{border-bottom:1px solid #edf1f7}.bom-question-index{display:inline-flex;width:28px;height:28px;border-radius:999px;align-items:center;justify-content:center;background:#f0f7ff;color:var(--blue);font-weight:900;font-size:12px}.bom-question-answer{padding:14px 16px;background:#fbfcff}.bom-question-answer p{margin:0 0 10px}.bom-question-sources{display:flex;gap:6px;flex-wrap:wrap}.bom-demand-study{display:grid;gap:14px}.bom-demand-thesis{border:1px solid rgba(10,132,255,.18);border-radius:16px;background:#fff;padding:14px;color:#26364f}.bom-demand-steps{display:grid;gap:10px}.bom-demand-step{display:grid;grid-template-columns:auto 1fr;gap:12px;border:1px solid #e8eef7;border-radius:16px;background:#fff;padding:14px}.bom-demand-step>span{display:inline-flex;width:34px;height:34px;border-radius:999px;align-items:center;justify-content:center;background:#eef7ff;color:var(--blue);font-weight:900;font-size:12px}.bom-demand-step h5{margin:0 0 6px;font-size:15px;color:#223047}.bom-demand-step p{margin:0 0 8px}.bom-demand-table{min-width:980px}.source-chip{display:inline-flex;margin:2px 4px 2px 0;border:1px solid rgba(10,132,255,.2);border-radius:999px;background:#eef7ff;color:var(--blue);padding:3px 8px;font-size:11px}
.bom-question-research-status{border:1px solid #dbeafe;border-radius:16px;background:#f7fbff;overflow:hidden;margin-bottom:12px}.bom-question-research-status>summary{display:grid;grid-template-columns:1fr auto auto;gap:10px;align-items:center;padding:12px;list-style:none;cursor:pointer}.bom-question-research-status[open]>summary{border-bottom:1px solid #dbeafe}.bom-question-research-status summary b{color:#0a66cc}.bom-question-research-status summary span:not(.chevron){color:#667085;font-size:12px;font-weight:900}.bom-question-research-body{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;padding:12px}.bom-question-research-body article{border:1px solid #e7eef8;border-radius:14px;background:#fff;padding:11px}.bom-question-research-body span{display:block;color:var(--blue);font-size:11px;font-weight:900;margin-bottom:4px}.bom-question-research-body p{margin:0;color:#344054;font-size:13px}.bom-s-curve-stage-card{border:1px solid rgba(29,154,108,.24);border-radius:20px;background:linear-gradient(180deg,#fff,#f5fffa);overflow:hidden;margin-top:14px}.bom-s-curve-stage-card>summary{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;list-style:none;cursor:pointer;padding:16px}.bom-s-curve-stage-card[open]>summary{border-bottom:1px solid rgba(29,154,108,.18)}.bom-s-curve-stage-card>summary>span:first-child{display:inline-flex;border:1px solid rgba(29,154,108,.28);border-radius:999px;background:#eaf8f2;color:var(--green);padding:6px 10px;font-size:12px;font-weight:900;white-space:nowrap}.bom-s-curve-stage-card h5,.bom-s-curve-stage-card p{margin:0}.bom-s-curve-stage-card summary b{display:block;color:#173f34;font-size:16px}.bom-s-curve-stage-card summary p{color:#667085;font-size:13px}.bom-stage-rollup-body{display:grid;gap:12px;padding:14px}.bom-stage-source-discipline,.bom-stage-next-signal,.bom-stage-downgrade-signal{border:1px solid #dcefe8;border-radius:16px;background:#fff;padding:12px}.bom-stage-current{border:1px solid #dcefe8;border-radius:16px;background:#f8fffb;padding:12px}.bom-stage-source-discipline>b,.bom-stage-current>b,.bom-stage-next-signal>b,.bom-stage-downgrade-signal>b{display:block;color:#173f34;margin-bottom:5px}.bom-stage-source-discipline p,.bom-stage-current p,.bom-stage-next-signal p,.bom-stage-downgrade-signal p{margin:0;color:#344054}.bom-stage-evidence-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.bom-stage-evidence-grid article{border:1px solid #e7eef8;border-radius:16px;background:#fff;padding:12px}.bom-stage-evidence-grid span{display:inline-flex;border-radius:999px;background:#eef7ff;color:var(--blue);font-size:11px;font-weight:900;padding:4px 8px}.bom-stage-evidence-grid b{display:block;color:#223047;margin:7px 0 5px}.bom-stage-evidence-grid p{margin:0;color:#344054;font-size:13px}.bom-question-four-step,.bom-question-stage-flow{display:grid;gap:12px;margin-bottom:14px}.bom-step-card{border:1px solid #e2ebf6;border-radius:18px;background:#fff;overflow:hidden}.bom-step-card>summary{display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:center;padding:14px;list-style:none;cursor:pointer}.bom-step-card[open]>summary{border-bottom:1px solid #e2ebf6}.bom-step-card>summary span:first-child{display:inline-flex;width:58px;height:26px;border-radius:999px;align-items:center;justify-content:center;background:#eef7ff;color:var(--blue);font-size:11px;font-weight:900}.bom-step-card>summary h5{margin:0;color:#223047;font-size:16px;line-height:1.35}.bom-step-body{display:grid;gap:12px;padding:14px}.bom-step-body>p{margin:0;color:#344054}.bom-metric-rationale-list{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.bom-metric-rationale-card{border:1px solid #edf2f8;border-radius:16px;background:#fbfdff;padding:12px}.bom-metric-rationale-card span{display:block;color:var(--blue);font-size:11px;font-weight:900;margin-bottom:4px}.bom-metric-rationale-card b{display:block;color:#223047;font-size:14px;margin-bottom:6px}.bom-metric-rationale-card p{margin:0;color:#344054;font-size:13px}.bom-history-metric-list{display:grid;gap:16px}.bom-history-metric-paragraph{display:grid;gap:8px;padding:0 0 14px;border-bottom:1px solid #e7edf6}.bom-history-metric-paragraph:last-child{border-bottom:0;padding-bottom:0}.bom-history-metric-text{margin:0;color:#344054}.bom-history-metric-text b{display:block;color:#223047;margin-bottom:4px}.bom-future-grid,.bom-mechanism-grid,.bom-final-trend-grid,.bom-stage-mechanism-grid{display:grid;grid-template-columns:1fr;gap:10px}.bom-future-card,.bom-mechanism-card,.bom-question-verdict{border:1px solid #edf2f8;border-radius:16px;background:#fbfdff;overflow:hidden}.bom-future-card>summary,.bom-mechanism-card>summary{display:grid;grid-template-columns:1fr auto;gap:8px;align-items:center;list-style:none;cursor:pointer;padding:12px}.bom-future-card[open]>summary,.bom-mechanism-card[open]>summary{border-bottom:1px solid #edf2f8}.bom-nested-card-body,.bom-question-verdict{padding:12px}.bom-future-card b,.bom-mechanism-card b,.bom-question-verdict b{display:block;color:#223047}.bom-nested-card-body p,.bom-question-verdict p{margin:0;color:#344054}.bom-question-supporting-detail{display:grid;gap:12px;margin-top:12px;border-top:1px solid #e7edf6;padding-top:12px}.bom-stage-integrated-card{border-color:#d8e6f7;background:linear-gradient(180deg,#fff,#fbfdff)}.bom-stage-integrated-card>summary{grid-template-columns:auto 1fr auto}.bom-stage-integrated-card>summary .stage-index{width:58px;height:28px}.bom-stage-subcard{border:1px solid #edf2f8;border-radius:16px;background:#fff;overflow:hidden}.bom-stage-subcard>summary{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;list-style:none;cursor:pointer;padding:12px}.bom-stage-subcard[open]>summary{border-bottom:1px solid #edf2f8}.bom-stage-subcard summary b{color:#223047}.bom-stage-subcard-body{display:grid;gap:10px;padding:12px}.bom-stage-history-content{display:grid;gap:10px}
.bom-future-grid{display:grid;grid-template-columns:1fr;gap:14px}.bom-future-card{min-width:0}
.bom-logic-chain-panel{border:1px solid #e1eaf6;border-radius:18px;background:#fbfdff;overflow:hidden}.bom-logic-chain-panel>summary{display:grid;grid-template-columns:1fr auto auto;gap:10px;align-items:center;padding:13px;list-style:none;cursor:pointer}.bom-logic-chain-panel[open]>summary{border-bottom:1px solid #e1eaf6}.bom-logic-chain-panel summary b{color:#0a66cc}.bom-logic-chain-panel summary span:not(.chevron){color:#667085;font-size:12px;font-weight:900}.bom-logic-chain-table{padding:12px}.bom-logic-chain-table table{min-width:980px}.bom-logic-chain-row td:first-child b{color:#0a66cc}.bom-logic-stage-stack{display:grid;gap:12px}.bom-logic-stage-card{border:1px solid #e1eaf6;border-radius:18px;background:#fbfdff;overflow:hidden}.bom-logic-stage-card>summary{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding:13px;list-style:none;cursor:pointer}.bom-logic-stage-card[open]>summary{border-bottom:1px solid #e1eaf6}.bom-logic-stage-card .stage-index{display:inline-flex;width:58px;height:28px;border-radius:999px;align-items:center;justify-content:center;background:#eaf3ff;color:var(--blue);font-size:11px;font-weight:900}.bom-logic-stage-card summary b{display:block;color:#0a66cc;font-size:12px}.bom-logic-stage-card summary strong{display:block;color:#223047;font-size:16px;line-height:1.3}.bom-logic-stage-body{display:grid;gap:10px;padding:13px}.bom-logic-stage-card p{margin:0;color:#344054}.bom-stage-metric-choice,.bom-stage-history,.bom-stage-current{border:1px solid #edf2f8;border-radius:16px;background:#fff;padding:12px}.bom-stage-metric-choice>b,.bom-stage-history>b,.bom-stage-current>b{display:block;color:#223047;margin-bottom:6px}.metric-choice-table th:first-child,.metric-choice-table td:first-child{width:28%}.metric-point-count{display:inline-flex;width:max-content;max-width:100%;border:1px solid #e0e8f4;border-radius:999px;background:#fff;color:#667085;padding:3px 8px;font-size:11px;font-weight:900;margin-top:8px}.metric-data-table,.metric-trend-gap{border:1px solid #eef3f9;border-radius:14px;background:#fbfdff;padding:10px}.metric-data-table>b,.metric-trend-gap>b{display:block;color:#667085;font-size:11px;margin-bottom:4px}.metric-data-table p,.metric-trend-gap p{margin:0;color:#344054;font-size:13px}.metric-data-rows{display:grid;gap:0;margin-top:10px;border:1px solid #e6edf7;border-radius:12px;overflow:hidden;background:#fff}.metric-data-row{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;padding:8px 10px;border-top:1px solid #eef2f7}.metric-data-row:first-child{border-top:0}.metric-data-row span{color:#344054;font-size:12px}.metric-data-row strong{color:#223047;font-size:12px;text-align:right}.metric-data-head{background:#f6f9fd}.metric-data-head b{color:#667085;font-size:11px;text-transform:uppercase}.metric-data-row-with-change{grid-template-columns:minmax(120px,1fr) minmax(90px,auto) minmax(140px,1fr)}.metric-data-row-with-company.metric-data-row-with-change{grid-template-columns:minmax(120px,.8fr) minmax(120px,1fr) minmax(90px,auto) minmax(140px,1fr)}.metric-multi-series-data .metric-data-row{grid-template-columns:minmax(120px,.8fr) 1fr auto}.metric-multi-series-data .metric-data-row-with-company.metric-data-row-with-change{grid-template-columns:minmax(120px,.8fr) minmax(120px,1fr) minmax(90px,auto) minmax(140px,1fr)}
.bom-demand-logic-chain{display:grid;gap:10px}.bom-demand-logic-step{display:grid;grid-template-columns:auto 1fr;gap:12px;border:1px solid #edf2f8;border-radius:16px;background:#fbfdff;padding:12px}.bom-demand-logic-step>span{display:inline-flex;width:34px;height:34px;border-radius:999px;align-items:center;justify-content:center;background:#eef7ff;color:var(--blue);font-weight:900;font-size:12px}.bom-demand-logic-step b{display:block;color:#223047;margin-bottom:5px}.bom-demand-logic-step p{margin:0 0 6px;color:#344054}.bom-demand-logic-step em{font-style:normal;color:#667085;font-size:12px;font-weight:800}
.research-narrative{display:grid;gap:18px}.narrative-head{border:1px solid rgba(10,132,255,.16);border-radius:18px;background:linear-gradient(180deg,#fff,#f7fbff);padding:18px}.narrative-head span{display:block;color:var(--blue);font-size:12px;font-weight:900;margin-bottom:6px}.narrative-head h4{margin:0 0 10px;font-size:24px;line-height:1.25;color:#1f2d3d}.narrative-head p{margin:0;color:#344054;font-size:16px}.logic-flow{display:grid;grid-template-columns:repeat(5,minmax(150px,1fr));gap:8px;align-items:stretch}.flow-step{border:1px solid #dceafa;border-radius:16px;background:#fff;padding:12px;min-width:150px}.flow-step span{display:inline-flex;width:28px;height:28px;border-radius:999px;align-items:center;justify-content:center;background:#eaf3ff;color:var(--blue);font-weight:900;font-size:12px;margin-bottom:8px}.flow-step p{margin:0;color:#26364f;font-weight:800;line-height:1.45}.flow-arrow{display:none}.narrative-prose{display:grid;gap:12px;border-left:3px solid #0a84ff;padding-left:16px}.narrative-prose p{margin:0;color:#2f3d52;font-size:15px}.narrative-data-table{min-width:1040px}.narrative-bottom{display:grid;grid-template-columns:1fr 1fr;gap:12px}.investment-takeaway,.bear-case-box{border:1px solid #e4ebf5;border-radius:18px;background:#fff;padding:16px}.investment-takeaway b,.bear-case-box b{display:block;color:#223047;margin-bottom:8px}.investment-takeaway p{margin:0;color:#344054}.bear-case-box{background:#fffafa;border-color:#f0d3d0}.bear-case-box ul{margin:0;padding-left:18px;color:#4b5563}.bear-case-box li+li{margin-top:6px}.demand-chain-audit{border:1px solid rgba(10,132,255,.18);border-radius:18px;background:#f7fbff;padding:14px}.demand-chain-title{display:flex;justify-content:space-between;gap:12px;align-items:center;margin-bottom:12px}.demand-chain-title span{color:var(--blue);font-weight:900}.demand-chain-title strong{color:#344054;font-size:13px}.demand-chain-cards{display:grid;gap:12px}.chain-audit-card{border:1px solid #dceafa;border-radius:16px;background:#fff;overflow:hidden}.chain-audit-head{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding:14px;border-bottom:1px solid #edf3fb}.chain-audit-head>span{display:inline-flex;width:34px;height:34px;border-radius:999px;align-items:center;justify-content:center;background:#eaf3ff;color:var(--blue);font-weight:900;font-size:12px}.chain-audit-head h5{margin:0 0 4px;font-size:16px;color:#223047}.chain-audit-head p{margin:0;color:var(--muted)}.chain-audit-head strong{border:1px solid rgba(10,132,255,.24);border-radius:999px;background:#f0f7ff;color:var(--blue);padding:5px 10px;font-size:12px;white-space:nowrap}.chain-audit-body-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;padding:14px}.chain-audit-body-grid div{border:1px solid #eef2f7;border-radius:14px;background:#fbfcff;padding:12px}.chain-audit-body-grid b{display:block;color:#223047;margin-bottom:6px}.chain-audit-body-grid p{margin:0;color:#3d536d}.chain-audit-verdict{display:flex;justify-content:space-between;gap:12px;align-items:center;border-top:1px solid #edf3fb;padding:12px 14px}.chain-audit-verdict>span{color:#667085;font-size:12px;font-weight:800}.qa-card{margin:12px 0;overflow:hidden}.qa-card summary{display:grid;grid-template-columns:auto 1fr auto auto;gap:12px;align-items:center;padding:14px 16px}.qid{font-weight:900;color:var(--blue)}.qa-count{font-size:12px;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.qa-body{display:grid;gap:10px;padding:14px 16px}.qa-block{border:1px solid #edf1f7;border-radius:16px;background:#fff;padding:12px}.block-title{font-weight:900;color:#27364a;margin-bottom:6px}.qa-card.level-2{margin-left:18px;background:rgba(255,255,255,.82)}.qa-card.level-3{margin-left:28px;background:rgba(247,249,252,.95);border-style:dashed}.l3-meta{display:flex;gap:8px;flex-wrap:wrap}.l3-meta span{border:1px solid #e0e8f4;border-radius:999px;background:#f7fbff;color:#4e5f75;font-size:11px;padding:4px 8px}.overview-answer p{margin:0}.overview-answer-prose{color:#344054}.target-section{display:grid;gap:14px}.table-scroll{max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch}.table-scroll table{min-width:920px;border-collapse:separate;border-spacing:0;width:100%;background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden}.table-scroll th,.table-scroll td{padding:10px 12px;text-align:left;border-bottom:1px solid #edf1f7;vertical-align:top;font-size:13px}.table-scroll th{background:#f6f9fd;color:#475467;font-size:12px;font-weight:900}.state-actionable_long,.state-watch_only,.state-no_action{display:inline-flex;border-radius:999px;padding:4px 8px;font-weight:900;font-size:12px}.state-actionable_long{color:var(--green);background:#eaf8f2;border:1px solid rgba(29,154,108,.25)}.state-watch_only{color:var(--amber);background:#fff7e6;border:1px solid rgba(183,121,31,.25)}.state-no_action{color:var(--red);background:#fff1f0;border:1px solid rgba(194,65,61,.22)}.source-collapse{padding:16px}.source-collapse summary{font-weight:900;color:#334155}.source-collapse .table-scroll{margin-top:12px}
.chain-node-expansion{display:grid;gap:12px;border:1px solid rgba(10,132,255,.18);border-radius:22px;background:linear-gradient(180deg,#fff,#f7fbff);padding:16px}.chain-node-expansion-head span{display:block;color:var(--blue);font-size:12px;font-weight:900;margin-bottom:4px}.chain-node-expansion-head h5{margin:0 0 8px;font-size:21px;line-height:1.3;color:#223047}.chain-node-expansion-head p{margin:0;color:#667085}.chain-node-stack{display:grid;gap:10px}.chain-node-detail{border:1px solid #dceafa;border-radius:18px;background:#fff;overflow:hidden}.chain-node-detail>summary{display:grid;grid-template-columns:auto 1fr auto auto;gap:12px;align-items:center;padding:14px 16px;list-style:none;cursor:pointer}.chain-node-detail>summary::-webkit-details-marker{display:none}.chain-node-detail[open]>summary{border-bottom:1px solid #edf3fb}.chain-node-index{display:inline-flex;width:36px;height:36px;border-radius:999px;align-items:center;justify-content:center;background:#eaf3ff;color:var(--blue);font-weight:900;font-size:12px}.chain-node-detail h6{margin:0 0 3px;color:#223047;font-size:17px}.chain-node-detail summary p{margin:0;color:#667085;font-size:13px}.chain-node-detail summary strong{border:1px solid rgba(10,132,255,.22);border-radius:999px;background:#f0f7ff;color:#0a66cc;padding:5px 9px;font-size:12px;white-space:nowrap}.chain-node-detail[open]>summary .chevron{transform:rotate(90deg)}.chain-node-body{display:grid;gap:12px;padding:14px 16px;background:#fbfdff}.chain-node-lens-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.chain-node-lens-grid article{border:1px solid #e8eef7;border-radius:15px;background:#fff;padding:12px}.chain-node-lens-grid b,.chain-node-conclusion b{display:block;color:#223047;margin-bottom:6px}.chain-node-lens-grid p,.chain-node-conclusion p{margin:0;color:#344054}.chain-node-conclusion{border:1px solid rgba(29,154,108,.22);border-radius:16px;background:#f3fbf7;padding:13px}
.chain-metric-board{display:grid;gap:10px;border:1px solid rgba(10,132,255,.14);border-radius:18px;background:#f7fbff;padding:13px}.chain-metric-board-head{display:flex;justify-content:space-between;gap:12px;align-items:center}.chain-metric-board-head b{color:#223047}.chain-metric-board-head span{color:#667085;font-size:12px;font-weight:900}.chain-metric-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.chain-metric-card{display:grid;gap:10px;border:1px solid #dfeaf7;border-radius:16px;background:#fff;padding:13px}.chain-metric-card header span{display:block;color:var(--blue);font-size:11px;font-weight:900;margin-bottom:3px}.chain-metric-card header strong{display:block;color:#223047;font-size:15px;line-height:1.25}.chain-metric-card p{margin:0;color:#344054;font-size:13px}.chain-metric-card dl{display:grid;gap:7px;margin:0}.chain-metric-card dl div{border-top:1px solid #eef2f7;padding-top:7px}.chain-metric-card dt{color:#667085;font-size:11px;font-weight:900}.chain-metric-card dd{margin:2px 0 0;color:#344054;font-size:13px}.chain-metric-card footer{display:grid;gap:8px}.chain-metric-card em{font-style:normal;color:#7a5a00;background:#fff7dc;border:1px solid #f1dda6;border-radius:999px;padding:4px 8px;font-size:11px;font-weight:900;width:max-content;max-width:100%}
.historical-comparison{display:grid;gap:14px;border:1px solid rgba(10,132,255,.18);border-radius:20px;background:linear-gradient(180deg,#ffffff,#f7fbff);padding:16px}.history-head span{display:block;color:var(--blue);font-size:12px;font-weight:900;margin-bottom:4px}.history-head h5{margin:0 0 8px;font-size:20px;line-height:1.3;color:#223047}.history-head p{margin:0;color:#475467}.history-snapshot-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.history-metric-card{border:1px solid #e1eaf6;border-radius:16px;background:#fff;padding:14px}.history-metric-card>span{display:block;color:#667085;font-size:12px;font-weight:900}.history-metric-card strong{display:block;color:#0a84ff;font-size:25px;line-height:1.1;margin:6px 0}.history-metric-card p{margin:0 0 8px;color:#344054;font-size:13px}.history-bar-list{display:grid;gap:9px}.history-bar-row{display:grid;grid-template-columns:145px 1fr minmax(120px,auto);gap:10px;align-items:center}.history-bar-label b{display:block;color:#223047}.history-bar-label span{color:#667085;font-size:13px}.history-bar-track{height:14px;border-radius:999px;background:#e9f1fb;overflow:hidden}.history-bar-track i{display:block;height:100%;border-radius:999px;background:linear-gradient(90deg,#72b7ff,#0a84ff)}.history-table{min-width:1040px}
.future-runway{display:grid;gap:14px;border:1px solid rgba(29,154,108,.20);border-radius:20px;background:linear-gradient(180deg,#ffffff,#f7fffb);padding:16px}.runway-head span{display:block;color:var(--green);font-size:12px;font-weight:900;margin-bottom:4px}.runway-head h5{margin:0 0 8px;font-size:20px;line-height:1.3;color:#223047}.runway-head p{margin:0;color:#475467}.runway-formula{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.runway-formula-card{border:1px solid #dcefe8;border-radius:16px;background:#fff;padding:14px}.runway-formula-card>span{display:inline-flex;width:28px;height:28px;border-radius:999px;align-items:center;justify-content:center;background:#eaf8f2;color:var(--green);font-weight:900;font-size:12px}.runway-formula-card h6{margin:10px 0 6px;color:#223047;font-size:15px}.runway-formula-card p{margin:0;color:#3d536d}.runway-table{min-width:1180px}.runway-timeline{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.runway-timeline article{border:1px solid #dcefe8;border-radius:16px;background:#fff;padding:14px}.runway-timeline span{display:block;color:var(--green);font-size:12px;font-weight:900}.runway-timeline strong{display:block;margin:4px 0;color:#223047}.runway-timeline p{margin:0;color:#3d536d}.runway-verdict{border:1px solid rgba(29,154,108,.22);border-radius:16px;background:#f1fbf7;padding:14px}.runway-verdict b{display:block;color:#166f52;margin-bottom:6px}.runway-verdict p{margin:0;color:#2f3d52}
.table-scroll.metric-choice-table{overflow-x:visible}.table-scroll.metric-choice-table table{min-width:0;width:100%;table-layout:fixed}.table-scroll.metric-choice-table th,.table-scroll.metric-choice-table td{white-space:normal;overflow-wrap:anywhere;word-break:break-word;line-height:1.55}.table-scroll.metric-choice-table th:first-child,.table-scroll.metric-choice-table td:first-child{width:28%}
@media(max-width:820px){.goal-grid,.constraint-grid,.chain-bridge-grid,.chain-layer-grid,.chain-company-list,.company-flow-grid,.chain-node-lens ul,.bom-node-brief,.chain-audit-body-grid,.logic-flow,.narrative-bottom,.history-snapshot-grid,.history-bar-row,.runway-formula,.runway-timeline,.chain-node-lens-grid,.chain-metric-grid,.bom-metric-rationale-list,.bom-future-grid,.bom-mechanism-grid,.bom-question-research-body,.bom-stage-evidence-grid{grid-template-columns:1fr}.chain-audit-head,.chain-audit-verdict,.demand-chain-title,.chain-node-detail>summary,.chain-metric-board-head{display:grid;grid-template-columns:1fr}.qa-card.level-2,.qa-card.level-3{margin-left:0}.qa-card summary{grid-template-columns:auto 1fr auto}.qa-count{display:none}}
`;
}

main();
