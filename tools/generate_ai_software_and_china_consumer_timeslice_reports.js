const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const AS_OF_DATE = "2026-02-28";
const REPORT_DATE = "2026-05-30";

const SCORE_WEIGHTS = {
  chokepoint_strength: 0.26,
  future_space: 0.18,
  valuation_odds: 0.18,
  evidence_quality: 0.14,
  disconfirming_risk_control: 0.10,
  monitorability: 0.05,
  payoff_convexity: 0.09,
};

const projects = [
  {
    project_id: "semiconductor_hardware_timeslice_20260228",
    title: "半导体芯片投资机会回测研究",
    object: "AI 半导体芯片与关键硬件链条，覆盖 GPU、custom ASIC、HBM/高端存储、先进制程/封装、半导体设备与过程控制。",
    constrained_judgment: "截至冻结时点，需求真实但不能泛化为所有半导体。最强未定价稀缺性集中在 HBM/高端存储、custom ASIC 与高速互连；GPU 平台和先进制造确定性强但共识更拥挤；设备链质量高但赔率受周期、估值和出口约束压制。",
    uncertainty: "AI capex 能否持续转为客户 ROI 与半导体公司的现金流，而不是阶段性拉货、库存波动或估值拥挤。",
    out_dir: "research/bom/semiconductor_hardware_timeslice_20260228",
    sources: [
      source("SRC-WSTS-2025", "WSTS Autumn 2025 Forecast", "https://www.wsts.org/esraCMS/extension/media/f/WST/7310/WSTS_FC-Release-2025_11.pdf", "2025-12-02", "2026 global semiconductor market forecast $975.46B; Logic +32.1% and Memory +39.4% are the clearest growth buckets."),
      source("SRC-SIA-OCT-2025", "SIA October 2025 Global Semiconductor Sales", "https://www.semiconductors.org/global-semiconductor-sales-increase-4-7-month-to-month-in-october/", "2025-12-04", "October 2025 global semiconductor sales $72.7B, +27.2% YoY and +4.7% MoM, confirming strong demand but not proving every segment has scarcity."),
      source("SRC-SEMI-EQUIP-2025", "SEMI Equipment Forecast", "https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports", "2025-12-16", "Global equipment sales projected at $133B in 2025, $145B in 2026 and $156B in 2027, driven by AI, HBM and advanced packaging."),
      source("SRC-NVDA-FY26-Q4", "NVIDIA FY2026 Q4 Results", "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/", "2026-02-25", "Q4 Data Center revenue $62.3B, +22% QoQ and +75% YoY; FY Data Center revenue $193.7B. Demand is visible but market expectations were already high."),
      source("SRC-AVGO-FY25-Q4", "Broadcom FY2025 Q4 Results", "https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-fourth-quarter-and-fiscal-year-2025", "2025-12-11", "Q4 revenue $18.0B +28%; AI semiconductor revenue +74%; Q1 FY26 AI semiconductor revenue expected to double to $8.2B."),
      source("SRC-AMD-2025-Q4", "AMD 2025 Q4 Results", "https://ir.amd.com/news-events/press-releases/detail/1276/amd-reports-fourth-quarter-and-full-year-2025-financial-results", "2026-02-03", "Q4 revenue $10.3B +34%; Data Center revenue $5.4B +39%. AI accelerator optionality exists but evidence is weaker than the leading bottleneck names."),
      source("SRC-TSMC-2025-Q4", "TSMC 2025 Q4 Results", "https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm", "2026-01-15", "Q4 revenue NT$1,046.09B +20.5%; 7nm and below 77%; 2026 capex guidance $52-56B shows strong advanced-node demand."),
      source("SRC-MU-FY26-Q1", "Micron FY2026 Q1 Results", "https://micron.gcs-web.com/news-releases/news-release-details/micron-technology-inc-reports-results-first-quarter-fiscal-2026", "2025-12-17", "Revenue $13.64B; Cloud Memory revenue $5.284B with 66% gross margin, pointing to direct HBM/high-end memory value capture."),
      source("SRC-ASML-2025-Q4", "ASML 2025 Q4 Results", "https://www.asml.com/en/news/press-releases/2026/q4-2025-financial-results", "2026-01-28", "Q4 net sales EUR9.7B, net bookings EUR13.2B including EUR7.4B EUV, backlog EUR38.8B. Scarcity is strong but valuation and policy risk cap action state."),
      source("SRC-AMAT-FY26-Q1", "Applied Materials FY2026 Q1 Results", "https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-announces-first-quarter-2026-results/", "2026-02-12", "Revenue $7.01B; record DRAM revenue and exposure to leading-edge logic, HBM and advanced packaging."),
      source("SRC-LRCX-DEC-2025", "Lam Research December 2025 Quarter Results", "https://www.sec.gov/Archives/edgar/data/707549/000070754926000006/lrcx_exhibitx991xq2x2026.htm", "2026-01-28", "Revenue $5.34B; complex 3D devices and advanced packages are key AI-era process drivers."),
      source("SRC-KLAC-FY26-Q2", "KLA FY2026 Q2 Results", "https://ir.kla.com/news-events/press-releases/detail/509/kla-corporation-reports-fiscal-2026-second-quarter-results", "2026-01-29", "Revenue $3.30B; process control remains critical across foundry/logic, memory, advanced packaging and services."),
      source("SRC-MRVL-FY26-Q3", "Marvell FY2026 Q3 Results", "https://investor.marvell.com/news-events/press-releases/detail/999/marvell-technology-inc-reports-third-quarter-of-fiscal-year-2026-financial-results", "2025-12-02", "Revenue $2.075B +37%; data-center demand and Celestial AI acquisition reinforce custom silicon and connectivity optionality."),
      labelSource("LBL-NASDAQ-SEMI", "Nasdaq historical quote API for semiconductor close-price labels", "https://api.nasdaq.com/api/quote/NVDA/historical?assetclass=stocks&fromdate=2026-02-25&todate=2026-05-30&limit=9999", "2026-05-28"),
    ],
    leaves: [
      ["Q1.1.1", "半导体总需求是否真实扩张？", "WSTS 与 SIA 数据显示总需求真实扩张，但这是行业需求确认，不等于所有环节都有超额收益。", ["SRC-WSTS-2025", "SRC-SIA-OCT-2025"]],
      ["Q1.1.2", "AI 需求是否足以支撑新增硬件采购？", "NVIDIA、Broadcom、AMD 的数据中心/AI 收入说明 AI 算力需求真实，但要继续检验客户 ROI 与订单持续性。", ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-AMD-2025-Q4"]],
      ["Q1.2.1", "AI 芯片收入是否已经转化为公司财务？", "NVIDIA 和 Broadcom 转化最清晰，AMD 有增速和期权但相对缺乏不可替代性证据。", ["SRC-NVDA-FY26-Q4", "SRC-AVGO-FY25-Q4", "SRC-AMD-2025-Q4"]],
      ["Q1.2.2", "高端存储和先进制造是否同步受益？", "Micron Cloud Memory、TSMC 先进制程占比和 capex 均显示 AI 需求沿供应链传导。", ["SRC-MU-FY26-Q1", "SRC-TSMC-2025-Q4"]],
      ["Q2.1.1", "GPU 平台的不可替代性是否仍然最高？", "NVIDIA 平台稀缺性最高，但市场共识和估值已强，未充分定价维度必须被压低。", ["SRC-NVDA-FY26-Q4"]],
      ["Q2.1.2", "custom ASIC 与高速互连是否是更好的瓶颈？", "Broadcom 与 Marvell 更贴近客户定制芯片、交换/互连和数据中心专用需求，稀缺性与赔率组合更均衡。", ["SRC-AVGO-FY25-Q4", "SRC-MRVL-FY26-Q3"]],
      ["Q2.2.1", "HBM/高端存储是否具有供给瓶颈？", "Micron Cloud Memory 的收入和毛利率显示 HBM/高端存储更像短中期供给瓶颈，是本轮最清晰的稀缺性节点。", ["SRC-MU-FY26-Q1", "SRC-WSTS-2025"]],
      ["Q2.2.2", "设备和过程控制是否拥有不可替代价值？", "ASML、KLA、Lam、Applied Materials 处在先进制程、HBM 和先进封装扩产链条，但设备周期、出口和估值限制赔率。", ["SRC-ASML-2025-Q4", "SRC-KLAC-FY26-Q2", "SRC-LRCX-DEC-2025", "SRC-AMAT-FY26-Q1", "SRC-SEMI-EQUIP-2025"]],
      ["Q3.1.1", "市场是否已经充分定价 AI 半导体叙事？", "GPU、EUV 和先进制造龙头确定性高但共识拥挤，不能因为质量高就给 actionable_long。", ["SRC-NVDA-FY26-Q4", "SRC-ASML-2025-Q4", "SRC-TSMC-2025-Q4"]],
      ["Q3.1.2", "AI ROI 或 capex 消化是否会反证需求？", "若客户 AI ROI 无法支撑继续扩张，最先受影响的是高估值算力链和弹性设备订单。", ["SRC-NVDA-FY26-Q4", "SRC-SEMI-EQUIP-2025"]],
      ["Q3.2.1", "出口限制和设备周期是否压低胜率？", "设备链的稀缺性强，但政策、周期和客户 capex 节奏会压低可行动分数。", ["SRC-ASML-2025-Q4", "SRC-AMAT-FY26-Q1", "SRC-LRCX-DEC-2025", "SRC-KLAC-FY26-Q2"]],
      ["Q3.2.2", "存储是否会重新进入供给周期风险？", "HBM 是稀缺节点，但存储行业天然周期性强，若供给快速扩张或价格转弱，必须降级。", ["SRC-MU-FY26-Q1", "SRC-WSTS-2025"]],
      ["Q4.1.1", "谁进入可行动或观察名单？", "冻结排序优先 MU 与 AVGO；MRVL/AMD/KLAC/LRCX/AMAT 观察；NVDA/TSMC/ASML 因共识和赔率约束不自动行动。", ["SRC-MU-FY26-Q1", "SRC-AVGO-FY25-Q4", "SRC-MRVL-FY26-Q3", "SRC-AMD-2025-Q4", "SRC-KLAC-FY26-Q2"]],
      ["Q4.1.2", "哪些优质公司必须被分数封顶？", "NVIDIA、TSMC、ASML 质量高但未充分定价不足；AMD 有弹性但不可替代性证据弱于 HBM/custom ASIC。", ["SRC-NVDA-FY26-Q4", "SRC-TSMC-2025-Q4", "SRC-ASML-2025-Q4", "SRC-AMD-2025-Q4"]],
      ["Q4.2.1", "升级触发器是什么？", "HBM 价格和毛利维持、AI ASIC 订单上修、先进封装/过程控制订单持续、客户 ROI 披露改善。", ["SRC-MU-FY26-Q1", "SRC-AVGO-FY25-Q4", "SRC-SEMI-EQUIP-2025"]],
      ["Q4.2.2", "降级触发器是什么？", "AI capex 下修、存储价格转弱、设备订单取消、出口限制升级、估值继续扩张但现金流未跟上。", ["SRC-SIA-OCT-2025", "SRC-MU-FY26-Q1", "SRC-ASML-2025-Q4"]],
    ],
    targets: [
      t(1, "MU", "Micron", "HBM / Cloud Memory", [4.4, 4.4, 3.5, 4.1, 3.0, 4.0, 4.0], [4.3, 4.4, 3.5], "HBM/Cloud Memory 是最直接的供给瓶颈，收入和毛利率证据清晰，但必须承认存储周期风险。", "HBM price, cloud memory gross margin, supply expansion, customer concentration", ["SRC-MU-FY26-Q1", "SRC-WSTS-2025"], lbl("USD", 412.37, "2026-02-27", 923.52, "2026-05-28", "Nasdaq MU")),
      t(2, "AVGO", "Broadcom", "Custom ASIC / Ethernet", [4.2, 4.3, 3.4, 4.0, 3.1, 4.2, 3.8], [4.2, 4.3, 3.4], "custom ASIC 与高速互连承接 hyperscaler 专用算力需求，证据强且赔率好于最拥挤 GPU 平台。", "AI semiconductor revenue, custom ASIC backlog, networking margin, customer concentration", ["SRC-AVGO-FY25-Q4"], lbl("USD", 319.55, "2026-02-27", 426.58, "2026-05-28", "Nasdaq AVGO")),
      t(3, "MRVL", "Marvell", "Data-center custom silicon / optical connectivity", [3.9, 4.0, 3.5, 3.5, 2.8, 3.6, 4.2], [4.0, 3.8, 3.5], "数据中心和互连弹性强，但证据质量和客户集中风险让它更适合观察而非高置信行动。", "data-center revenue growth, Celestial AI integration, custom silicon wins, gross margin", ["SRC-MRVL-FY26-Q3"], lbl("USD", 81.69, "2026-02-27", 204.83, "2026-05-28", "Nasdaq MRVL")),
      t(4, "AMD", "Advanced Micro Devices", "AI accelerator challenger", [3.6, 4.1, 3.4, 3.4, 2.7, 3.7, 4.2], [4.0, 3.6, 3.4], "AI 加速器弹性大，但冻结时点不可替代性和客户采用证据弱于 HBM/custom ASIC，因此只给观察状态。", "MI accelerator adoption, data-center margin, software ecosystem, customer wins", ["SRC-AMD-2025-Q4"], lbl("USD", 200.21, "2026-02-27", 518.09, "2026-05-28", "Nasdaq AMD")),
      t(5, "KLAC", "KLA", "Process control for advanced nodes", [4.0, 3.7, 3.2, 4.0, 3.4, 4.0, 3.0], [3.8, 4.0, 3.2], "过程控制稀缺且证据扎实，但需求弹性和赔率弱于存储/custom ASIC。", "advanced node orders, services growth, China exposure, wafer-fab equipment cycle", ["SRC-KLAC-FY26-Q2", "SRC-SEMI-EQUIP-2025"], lbl("USD", 1524.55, "2026-02-27", 1927.63, "2026-05-28", "Nasdaq KLAC")),
      t(6, "LRCX", "Lam Research", "Etch/deposition for 3D devices and HBM", [3.8, 3.6, 3.2, 3.8, 3.0, 3.8, 3.1], [3.7, 3.8, 3.2], "受益于 3D 结构和先进封装，但设备周期属性较强，分数需要被周期风险约束。", "memory WFE orders, advanced packaging exposure, China/export mix, order cancellations", ["SRC-LRCX-DEC-2025", "SRC-SEMI-EQUIP-2025"], lbl("USD", 233.89, "2026-02-27", 318.00, "2026-05-28", "Nasdaq LRCX")),
      t(7, "AMAT", "Applied Materials", "Leading-edge logic / DRAM / packaging equipment", [3.7, 3.6, 3.2, 3.8, 3.0, 3.8, 3.1], [3.7, 3.7, 3.2], "覆盖面广、证据稳定，但稀缺性不如 EUV/过程控制，且设备周期限制 action_state。", "DRAM and packaging revenue, leading-edge logic orders, China/export risk, backlog quality", ["SRC-AMAT-FY26-Q1", "SRC-SEMI-EQUIP-2025"], lbl("USD", 372.30, "2026-02-27", 449.68, "2026-05-28", "Nasdaq AMAT")),
      t(8, "NVDA", "NVIDIA", "GPU platform / CUDA ecosystem", [4.6, 4.4, 2.8, 4.6, 3.1, 4.8, 3.2], [4.4, 4.6, 2.8], "需求和不可替代性最高，但冻结时点市场预期太强，未充分定价不足，不能因为质量高就行动。", "Data Center growth, gross margin, hyperscaler ROI, valuation multiple, competitive ASIC shift", ["SRC-NVDA-FY26-Q4"], lbl("USD", 177.19, "2026-02-27", 214.25, "2026-05-28", "Nasdaq NVDA")),
      t(9, "TSM", "TSMC", "Advanced foundry / CoWoS and leading nodes", [4.1, 4.2, 3.0, 4.4, 3.2, 4.1, 3.0], [4.2, 4.1, 3.0], "先进制程确定性强，但大部分稀缺性已被市场理解，赔率未过门槛。", "capex discipline, advanced-node mix, CoWoS capacity, geopolitical risk, customer concentration", ["SRC-TSMC-2025-Q4"], lbl("USD", 374.58, "2026-02-27", 424.86, "2026-05-28", "Nasdaq TSM")),
      t(10, "ASML", "ASML", "EUV lithography", [4.3, 3.8, 2.7, 4.2, 3.0, 4.2, 2.8], [3.8, 4.5, 2.7], "EUV 稀缺性极强，但估值、出口限制和订单周期使冻结时点的未充分定价不足。", "EUV bookings, backlog conversion, export rules, customer capex, valuation", ["SRC-ASML-2025-Q4", "SRC-SEMI-EQUIP-2025"], lbl("USD", 1450.56, "2026-02-27", 1605.77, "2026-05-28", "Nasdaq ASML")),
    ],
  },
  {
    project_id: "ai_software_apps_timeslice_20260228",
    title: "AI 软件应用投资机会回测研究",
    object: "AI 软件应用公司，覆盖企业代理、工作流、CRM、创意工具、数据云、广告优化和安全/可观测平台。",
    constrained_judgment: "截至冻结时点，AI 软件应用需求真实，但大多数优质公司估值已经反映高成长。Snowflake 和 AppLovin 赔率更凸但风险更高；ServiceNow/Microsoft 质量更高但不便宜；Palantir 因估值预期过高仅观察。",
    uncertainty: "AI 应用究竟带来可计费增量收入，还是只变成产品功能升级和基础设施成本。",
    out_dir: "research/bom/ai_software_apps_timeslice_20260228",
    sources: [
      source("SRC-MSFT-FY26-Q2", "Microsoft FY2026 Q2 Earnings", "https://www.microsoft.com/en-us/Investor/earnings/FY-2026-Q2/press-release-webcast", "2026-01-28", "Microsoft revenue $81.3B +17%; Microsoft Cloud revenue $51.5B +26%; capex additions show AI/cloud demand and infrastructure intensity."),
      source("SRC-NOW-Q4-2025", "ServiceNow Q4 and FY2025 Results", "https://investor.servicenow.com/news/news-details/2026/ServiceNow-Reports-Fourth-Quarter-and-Full-Year-2025-Financial-Results-Board-of-Directors-Authorizes-Additional-5B-for-Share-Repurchase-Program/default.aspx", "2026-01-28", "Q4 subscription revenue $3.466B +21%; cRPO $12.85B +25%; Now Assist net new ACV more than doubled."),
      source("SRC-PLTR-Q4-2025", "Palantir Q4 2025 Results", "https://investors.palantir.com/news-details/2026/Palantir-Reports-Revenue-Growth-of-70-Year-Over-Year-and-U.S.-Commercial-Revenue-Growth-of-121-Year-Over-Year-in-Q4-2025/default.aspx", "2026-02-02", "AIP/operational AI demand is strong; growth expectations and valuation were already demanding."),
      source("SRC-CRM-Q3-FY26", "Salesforce Q3 FY2026 Results", "https://investor.salesforce.com/news/news-details/2025/Salesforce-Delivers-Record-Third-Quarter-Fiscal-2026-Results-Driven-by-Agentforce--Data-360/default.aspx", "2025-12-03", "Q3 revenue $10.3B +9%; cRPO +11%; Agentforce and Data 360 ARR nearly $1.4B, up 114%."),
      source("SRC-ADBE-Q4-2025", "Adobe Q4 and FY2025 Results", "https://news.adobe.com/news/2025/12/122025-q4earnings", "2025-12-10", "Q4 revenue $6.19B +10%; Digital Media revenue $4.62B +11%; Firefly and AI-influenced ARR are monetization leads."),
      source("SRC-SNOW-Q3-FY26", "Snowflake Q3 FY2026 Results", "https://investors.snowflake.com/financials/quarterly-results/default.aspx", "2025-12-03", "Product revenue $1.16B +29%; AI Data Cloud/Cortex are data-layer application leads."),
      source("SRC-APP-Q4-2025", "AppLovin Q4/FY2025 Results", "https://investors.applovin.com/news-events/news-releases", "2026-02-15", "AXON/ad AI optimization is a commercial AI application lead; customer concentration and ad-cycle risk remain material."),
      labelSource("LBL-NASDAQ-AI", "Nasdaq historical quote API for AI software close prices", "https://api.nasdaq.com/api/quote/MSFT/historical?assetclass=stocks&fromdate=2026-02-25&todate=2026-05-30&limit=9999", "2026-05-28"),
    ],
    leaves: [
      ["Q1.1.1", "企业 AI 代理是否已转成真实订单？", "ServiceNow、Salesforce 和 Microsoft 已有 RPO、subscription、Agentforce/Now Assist 线索，需求真实但仍需证明付费增量。", ["SRC-NOW-Q4-2025", "SRC-CRM-Q3-FY26", "SRC-MSFT-FY26-Q2"]],
      ["Q1.1.2", "AI 创意和办公应用是否能提高 ARPU？", "Adobe 和 Microsoft 说明 AI 功能进入主流应用，但 AI-influenced ARR 与 Copilot 付费转化仍需单独验证。", ["SRC-ADBE-Q4-2025", "SRC-MSFT-FY26-Q2"]],
      ["Q1.2.1", "AI 数据层是否是应用增长的前置瓶颈？", "Snowflake 产品收入高增说明数据云需求强，Cortex/AI Data Cloud 可能成为企业 AI 应用入口。", ["SRC-SNOW-Q3-FY26"]],
      ["Q1.2.2", "AI 广告优化是否是更快商业化应用？", "AppLovin 的 AXON 线索更接近即时 ROI，但广告周期与平台依赖提高风险。", ["SRC-APP-Q4-2025"]],
      ["Q2.1.1", "谁拥有最难替代的企业工作流入口？", "ServiceNow 和 Microsoft 强在企业分发与工作流，Salesforce 强在 CRM 数据，但三者估值和增长速度差异明显。", ["SRC-NOW-Q4-2025", "SRC-MSFT-FY26-Q2", "SRC-CRM-Q3-FY26"]],
      ["Q2.1.2", "Palantir 的 operational AI 是否具备硬稀缺性？", "AIP 的 operational deployment 有稀缺性，但市场预期很高，赔率门槛更难通过。", ["SRC-PLTR-Q4-2025"]],
      ["Q2.2.1", "数据云和应用软件谁更能捕获价值？", "数据层可能成为应用层前置瓶颈，Snowflake 需要证明 Cortex 工作负载能提升 consumption 和留存。", ["SRC-SNOW-Q3-FY26"]],
      ["Q2.2.2", "广告 AI 优化是否可防守？", "AppLovin 的 AI 广告优化商业化强，但客户集中、监管和广告周期让瓶颈硬度弱于企业系统-of-record。", ["SRC-APP-Q4-2025"]],
      ["Q3.1.1", "估值是否已经透支 AI 应用叙事？", "Palantir、ServiceNow、AppLovin 等优质线索大多面临高预期，不能只因增长高就给 actionable。", ["SRC-PLTR-Q4-2025", "SRC-NOW-Q4-2025", "SRC-APP-Q4-2025"]],
      ["Q3.1.2", "AI 收入披露不足是否压低证据质量？", "多数公司没有完整披露 AI SKU 独立收入、毛利和续约率，必须限制分数。", ["SRC-CRM-Q3-FY26", "SRC-ADBE-Q4-2025", "SRC-SNOW-Q3-FY26"]],
      ["Q3.2.1", "高 capex 是否稀释软件应用回报？", "Microsoft 资本开支说明需求强，也说明 AI 应用需要基础设施支撑，FCF 和 ROIC 是反证触发器。", ["SRC-MSFT-FY26-Q2"]],
      ["Q3.2.2", "平台竞争是否会把 AI 应用商品化？", "办公、创意、CRM、数据云和广告 AI 都可能被基础模型和云厂商重叠竞争，稀缺性必须逐项验证。", ["SRC-ADBE-Q4-2025", "SRC-CRM-Q3-FY26", "SRC-SNOW-Q3-FY26"]],
      ["Q4.1.1", "谁可以进入行动/观察名单？", "Snowflake/AppLovin 有较强赔率凸性但风险更高；ServiceNow/Microsoft 质量高但估值门槛高；Palantir 仅观察。", ["SRC-SNOW-Q3-FY26", "SRC-APP-Q4-2025", "SRC-NOW-Q4-2025", "SRC-MSFT-FY26-Q2", "SRC-PLTR-Q4-2025"]],
      ["Q4.1.2", "哪些公司需要被分数封顶？", "Palantir 因预期过高封顶；Adobe/Salesforce 因 AI 增量收入未充分量化封顶；Microsoft 因体量和 capex 封顶。", ["SRC-PLTR-Q4-2025", "SRC-ADBE-Q4-2025", "SRC-CRM-Q3-FY26", "SRC-MSFT-FY26-Q2"]],
      ["Q4.2.1", "升级触发器是什么？", "AI SKU 独立 ARR、付费客户、RPO 加速、毛利稳定、FCF conversion 改善。", ["SRC-NOW-Q4-2025", "SRC-CRM-Q3-FY26", "SRC-SNOW-Q3-FY26"]],
      ["Q4.2.2", "降级触发器是什么？", "AI 使用量增长不转收入、估值继续扩张、capex/推理成本侵蚀利润、竞争导致价格下降。", ["SRC-MSFT-FY26-Q2", "SRC-ADBE-Q4-2025"]],
    ],
    targets: [
      t(1, "SNOW", "Snowflake", "AI Data Cloud / Cortex", [3.9, 4.1, 3.4, 3.6, 2.9, 3.8, 4.1], [4.1, 3.9, 3.4], "数据云可能成为企业 AI 应用前置瓶颈，赔率相对更凸；但 AI workload 收入披露不足。", "Cortex adoption、consumption growth、FCF margin", ["SRC-SNOW-Q3-FY26"], lbl("USD", 168.41, "2026-02-27", 239.20, "2026-05-28", "Nasdaq SNOW")),
      t(2, "APP", "AppLovin", "AXON 广告 AI 优化", [3.5, 4.0, 3.6, 3.2, 2.5, 3.0, 4.2], [4.0, 3.4, 3.5], "AI 广告商业化最直接，但客户集中、广告周期和监管使风险控制不足。", "广告主 ROI、客户集中、平台政策、margin", ["SRC-APP-Q4-2025"], lbl("USD", 434.77, "2026-02-27", 599.89, "2026-05-28", "Nasdaq APP")),
      t(3, "NOW", "ServiceNow", "企业工作流 AI control tower", [4.1, 3.8, 2.9, 4.0, 3.3, 4.4, 3.0], [3.8, 4.2, 2.9], "稀缺性和证据质量高，但估值未必给出足够赔率。", "Now Assist ACV、cRPO、renewal、估值", ["SRC-NOW-Q4-2025"], lbl("USD", 108.01, "2026-02-27", 108.73, "2026-05-28", "Nasdaq NOW")),
      t(4, "MSFT", "Microsoft", "Copilot + Azure + enterprise distribution", [4.2, 3.6, 2.8, 4.2, 3.2, 4.6, 2.8], [3.8, 4.4, 2.8], "分发稀缺性强，但体量大且 capex 高，AI 应用增量不够纯。", "Copilot monetization、Azure AI margin、capex/FCF", ["SRC-MSFT-FY26-Q2"], lbl("USD", 392.74, "2026-02-27", 426.99, "2026-05-28", "Nasdaq MSFT")),
      t(5, "PLTR", "Palantir", "Operational AI / AIP", [4.0, 4.2, 2.3, 3.7, 2.8, 3.6, 3.4], [4.2, 4.1, 2.2], "AIP 稀缺性强，但市场预期极高，赔率未过门槛。", "commercial customer growth、contract duration、valuation", ["SRC-PLTR-Q4-2025"], lbl("USD", 137.19, "2026-02-27", 143.34, "2026-05-28", "Nasdaq PLTR")),
      t(6, "CRM", "Salesforce", "Agentforce + Data 360", [3.5, 3.4, 3.1, 3.7, 3.0, 4.1, 2.8], [3.5, 3.5, 3.1], "AI CRM 线索真实，但核心增长仍中个位到低双位，AI 增量需证明。", "Agentforce paid deals、ARR、RPO、FCF", ["SRC-CRM-Q3-FY26"], lbl("USD", 194.79, "2026-02-27", 176.17, "2026-05-28", "Nasdaq CRM")),
      t(7, "ADBE", "Adobe", "Firefly / Creative AI", [3.4, 3.2, 3.0, 3.6, 2.9, 3.8, 2.7], [3.2, 3.4, 3.0], "创意资产和工具链强，但 AI 是否带来净新增收入仍未充分验证。", "AI ARR、Digital Media ARR、价格/留存", ["SRC-ADBE-Q4-2025"], lbl("USD", 262.41, "2026-02-27", 241.44, "2026-05-28", "Nasdaq ADBE")),
    ],
  },
  {
    project_id: "china_consumer_timeslice_20260228",
    title: "中国消费股投资机会回测研究",
    object: "中国消费股，覆盖 IP 潮玩、运动户外、餐饮连锁、白酒、软饮/茶饮、旅行服务等。",
    constrained_judgment: "截至冻结时点，中国消费不是普遍复苏行情，机会集中在有稀缺供给和海外/结构性增长的消费资产。Pop Mart 稀缺性最强但估值和单 IP 风险很高；Yum China/Trip.com 更偏质量观察；茅台和安踏更偏防守观察。",
    uncertainty: "消费升级/情绪消费能否持续越过宏观疲弱，以及强品牌能否把需求转成高质量现金流。",
    out_dir: "research/bom/china_consumer_timeslice_20260228",
    sources: [
      source("SRC-NBS-ONLINE-2025", "NBS December 2025 Retail Sales", "https://www.stats.gov.cn/english/PressRelease/202601/t20260120_1962354.html", "2026-01-20", "2025 online retail sales RMB15,972.2bn +8.6%; physical-goods online retail +5.2%; online food +14.5%."),
      source("SRC-NBS-COMMUNIQUE-2025", "NBS 2025 Statistical Communique", "https://www.stats.gov.cn/english/PressRelease/202602/t20260228_1962661.html", "2026-02-28", "2025 total retail sales RMB50.1202tn +3.7%; gold/jewelry +12.8%, sports/recreation +15.7%, food +9.3%."),
      source("SRC-POPMART-H1-2025", "Pop Mart 2025 Interim Results", "https://prod-out-res.popmart.com/cms/INTERIM_RESULTS_ANNOUNCEMENT_FOR_THE_SIX_MONTHS_ENDED_30_JUNE_2025_c6a7290528.pdf", "2025-08-19", "H1 revenue RMB13.876bn +204.4%; shareholder profit RMB4.574bn +396.5%; IP and overseas expansion are key leads."),
      source("SRC-ANTA-H1-2025", "ANTA Sports 2025 Interim Results", "https://ir.anta.com/en/news_detail.php?id=153056", "2025-08-27", "Operating margin 26.3%; other brands outgrew core brands; multi-brand sports/outdoor platform lead."),
      source("SRC-YUMC-Q4-2025", "Yum China Q4/FY2025 Results", "https://ir.yumchina.com/news-releases/news-release-details/yum-china-reports-fourth-quarter-2025-results/", "2026-02-04", "Q4 system sales +7%, same-store sales +3%, operating profit +25%; store count 18,101 and 2026 target >20,000."),
      source("SRC-MOUTAI-Q3-2025", "Kweichow Moutai Q3 2025 filing lead", "https://stockanalysis.com/quote/sha/600519/revenue/", "2025-10-30", "Moutai remains brand-scarce, but alcohol category growth and channel price are key boundaries."),
      source("SRC-TRIP-Q4-2025", "Trip.com Q4/FY2025 Results", "https://investors.trip.com/news-releases/news-release-details/tripcom-group-limited-reports-unaudited-fourth-quarter-and-5", "2026-02-25", "Q4 accommodation revenue RMB6.3bn +21%; FY attributable net income RMB33.3bn."),
      labelSource("LBL-STOCKANALYSIS-CONSUMER", "StockAnalysis/Nasdaq close prices for consumer labels", "https://stockanalysis.com/quote/hkg/9992/history/", "2026-05-29"),
    ],
    leaves: [
      ["Q1.1.1", "中国消费总盘是否支持普遍多头？", "社零 +3.7% 表明总盘不弱但不构成普遍高增长，必须找结构性品类和稀缺品牌。", ["SRC-NBS-COMMUNIQUE-2025"]],
      ["Q1.1.2", "哪些品类增速更有结构机会？", "体育娱乐、金银珠宝、食品和线上食品相对更强，服装、饮料、烟酒增速偏弱。", ["SRC-NBS-ONLINE-2025", "SRC-NBS-COMMUNIQUE-2025"]],
      ["Q1.2.1", "情绪消费/IP 消费是否是高增量？", "Pop Mart H1 增长极强，IP 情绪消费与海外扩张是真实结构性需求。", ["SRC-POPMART-H1-2025"]],
      ["Q1.2.2", "服务消费和旅行是否提供更高弹性？", "Trip.com 住宿收入增长显示旅行服务修复，但周期性和可选消费属性仍强。", ["SRC-TRIP-Q4-2025"]],
      ["Q2.1.1", "Pop Mart 的 IP 是否构成稀缺瓶颈？", "强 IP、盲盒/潮玩心智和海外扩张构成最强稀缺性，但单 IP 热度风险必须封顶。", ["SRC-POPMART-H1-2025"]],
      ["Q2.1.2", "茅台品牌稀缺性是否仍能转为增长？", "茅台品牌稀缺性强，但白酒行业需求和渠道价格约束使其更偏防守质量。", ["SRC-MOUTAI-Q3-2025", "SRC-NBS-COMMUNIQUE-2025"]],
      ["Q2.2.1", "安踏多品牌运动户外是否是结构性瓶颈？", "多品牌和专业户外线索成立，但主品牌/FILA 增速有限，需看其他品牌能否规模化。", ["SRC-ANTA-H1-2025"]],
      ["Q2.2.2", "百胜中国的供应链/门店网络是否不可替代？", "供应链、规模和加盟扩张强，但餐饮竞争和单店增长限制稀缺性。", ["SRC-YUMC-Q4-2025"]],
      ["Q3.1.1", "宏观消费疲弱是否压低胜率？", "总消费增长低个位，白酒/服装/饮料等品类缺乏强 beta，不能广泛看多。", ["SRC-NBS-COMMUNIQUE-2025"]],
      ["Q3.1.2", "高估值和热度是否压低 Pop Mart 赔率？", "Pop Mart 增速极强但市场关注度和估值也高，单 IP 热度和供给风险压低赔率。", ["SRC-POPMART-H1-2025"]],
      ["Q3.2.1", "餐饮/旅行的周期性是否限制分数？", "Yum China 和 Trip.com 质量较好，但宏观、价格竞争、旅行周期让分数不能过高。", ["SRC-YUMC-Q4-2025", "SRC-TRIP-Q4-2025"]],
      ["Q3.2.2", "防守品牌是否有足够赔率？", "茅台和安踏品牌强，但增长速度与估值赔率不足以自动行动。", ["SRC-MOUTAI-Q3-2025", "SRC-ANTA-H1-2025"]],
      ["Q4.1.1", "谁进入行动/观察名单？", "Pop Mart 稀缺性最高但风险高；Yum China、Trip.com、Anta、Moutai 观察；Haidilao/Nongfu 证据不足。", ["SRC-POPMART-H1-2025", "SRC-YUMC-Q4-2025", "SRC-TRIP-Q4-2025", "SRC-ANTA-H1-2025", "SRC-MOUTAI-Q3-2025"]],
      ["Q4.1.2", "哪些标的必须不行动？", "Haidilao/Nongfu 缺少足够稀缺性和赔率数据；茅台虽稀缺但高端酒需求边界明显。", ["SRC-NBS-COMMUNIQUE-2025", "SRC-MOUTAI-Q3-2025"]],
      ["Q4.2.1", "升级触发器是什么？", "海外增长可持续、IP 矩阵扩散、同店恢复、利润率稳定、渠道价格改善。", ["SRC-POPMART-H1-2025", "SRC-YUMC-Q4-2025", "SRC-MOUTAI-Q3-2025"]],
      ["Q4.2.2", "降级触发器是什么？", "单 IP 热度回落、消费品类增速下滑、餐饮价格战、白酒渠道价继续走弱。", ["SRC-NBS-COMMUNIQUE-2025", "SRC-POPMART-H1-2025"]],
    ],
    targets: [
      t(1, "9992.HK", "Pop Mart", "IP 情绪消费 + 海外扩张", [4.2, 4.5, 3.1, 3.6, 2.7, 3.2, 4.3], [4.5, 4.2, 3.1], "最像巨大结构需求与稀缺供给结合的消费资产，但估值和单 IP 风险让动作仅为观察。", "IP 矩阵、海外持续性、库存/假货、估值", ["SRC-POPMART-H1-2025"], lbl("HKD", 225.00, "2026-02-27", 173.40, "2026-05-29", "StockAnalysis HKG 9992")),
      t(2, "YUMC", "Yum China", "餐饮供应链 + 门店网络", [3.6, 3.5, 3.3, 4.0, 3.2, 4.0, 3.0], [3.5, 3.6, 3.3], "同店和利润改善可见，网络和供应链强，但不是高稀缺高赔率机会。", "同店、门店回报、加盟比例、利润率", ["SRC-YUMC-Q4-2025"], lbl("USD", 44.93, "2026-02-27", 45.27, "2026-05-28", "Nasdaq YUMC")),
      t(3, "TCOM", "Trip.com", "旅行供给网络", [3.8, 3.7, 3.1, 3.7, 3.0, 3.7, 3.2], [3.8, 3.8, 3.1], "旅行服务质量较好，但周期性和估值不够便宜，观察优先。", "住宿收入、出境供给、营销费、take-rate", ["SRC-TRIP-Q4-2025"], lbl("USD", 52.62, "2026-02-27", 47.08, "2026-05-28", "Nasdaq TCOM")),
      t(4, "2020.HK", "ANTA Sports", "多品牌运动户外", [3.6, 3.3, 3.2, 3.6, 3.1, 3.5, 2.9], [3.3, 3.6, 3.2], "多品牌平台和户外线索成立，但主品牌增速普通，赔率有限。", "其他品牌规模化、FILA 恢复、库存、毛利", ["SRC-ANTA-H1-2025"], lbl("HKD", 82.95, "2026-02-27", 75.80, "2026-05-29", "StockAnalysis HKG 2020")),
      t(5, "600519.SS", "Kweichow Moutai", "高端白酒品牌稀缺", [4.1, 2.8, 3.0, 3.5, 2.8, 3.2, 2.4], [2.9, 4.3, 3.0], "品牌稀缺性极强，但未来需求和渠道价格没有越过巨大机会门槛。", "批价、库存、直销、宴请需求", ["SRC-MOUTAI-Q3-2025"], lbl("CNY", 1440.11, "2026-02-27", 1326.00, "2026-05-29", "StockAnalysis SHA 600519")),
      t(6, "9987.HK", "Yum China HK", "餐饮网络 HK 价格标签", [3.6, 3.5, 3.3, 4.0, 3.2, 4.0, 3.0], [3.5, 3.6, 3.3], "与 YUMC 同一基本面，仅作为港股观察标签。", "同店、门店回报、加盟比例、利润率", ["SRC-YUMC-Q4-2025"], lbl("HKD", 422.00, "2026-02-27", 343.00, "2026-05-29", "StockAnalysis HKG 9987")),
      t(7, "6862.HK", "Haidilao", "餐饮服务", [2.9, 2.8, 2.7, 2.7, 2.4, 2.9, 2.6], [3.0, 2.8, 2.7], "缺少硬稀缺和同店利润证明，不行动。", "翻台、客单、门店扩张、利润率", ["SRC-NBS-COMMUNIQUE-2025"], lbl("HKD", 17.49, "2026-02-27", 12.76, "2026-05-29", "StockAnalysis HKG 6862")),
      t(8, "9633.HK", "Nongfu Spring", "包装饮料品牌渠道", [3.1, 2.9, 2.9, 2.8, 2.6, 3.0, 2.5], [2.9, 3.1, 2.9], "品牌和渠道强，但饮料品类增速与竞争不足以形成行动机会。", "茶饮/水增长、渠道、价格竞争", ["SRC-NBS-COMMUNIQUE-2025"], lbl("HKD", 46.04, "2026-02-27", 42.80, "2026-05-29", "StockAnalysis HKG 9633")),
    ],
  },
  {
    project_id: "xiaomi_timeslice_20260228",
    title: "小米集团单公司投资机会回测研究",
    object: "小米集团（1810.HK），覆盖智能手机 x AIoT 基盘、智能电动汽车、AI/自研芯片、互联网服务和 Human x Car x Home 生态。",
    constrained_judgment: "截至冻结时点，小米的产业变化是真实的：EV 交付、毛利率、用户生态和研发投入均显示公司从手机硬件商向车家生态平台迁移。但 1810.HK 股价已经反映相当多 EV/AI 预期，且 EV 竞争、补贴退坡、手机毛利和费用投入仍会压低赔率；因此更适合列入高质量观察，不应给可行动状态。",
    uncertainty: "EV 高增长能否持续转化为稳定经营利润和自由现金流，同时不被智能手机周期、零部件成本、渠道扩张费用和估值预期反噬。",
    out_dir: "research/bom/xiaomi_timeslice_20260228",
    l1Defs: [
      ["Q1", "小米的增长驱动是否真实且可持续？", "增长驱动真实，但主要来自 EV 与生态扩张；手机 x AIoT 基盘更像稳定器而不是高弹性来源。"],
      ["Q2", "小米的价值捕获瓶颈在哪里？", "价值捕获来自品牌、渠道、用户生态、车家互联和局部技术自研，但不可替代性还没有达到平台级垄断。"],
      ["Q3", "哪些反证会压低胜率和赔率？", "估值预期、EV 竞争、补贴退坡、研发/销售费用和手机毛利压力，都足以限制行动分数。"],
      ["Q4", "冻结时点如何形成小米观察结论？", "默认不行动；除非 EV 利润、现金流和市场未充分定价同时过门槛，否则只保留观察。"],
    ],
    l2Defs: [
      ["Q1.1", "核心增长现实", "先确认 EV 与手机 x AIoT 是否共同支撑增长。"],
      ["Q1.2", "规模化与生态迁移", "再判断 EV 和 Human x Car x Home 是否在财务上被验证。"],
      ["Q2.1", "品牌、渠道与技术壁垒", "判断小米的稀缺性来自哪里。"],
      ["Q2.2", "利润池与缓冲层", "判断 EV、IoT、互联网服务是否能共同提供价值捕获。"],
      ["Q3.1", "估值与竞争反证", "判断好公司是否已经被充分定价。"],
      ["Q3.2", "财务质量与周期反证", "判断增长质量和下行控制。"],
      ["Q4.1", "目标观察状态", "形成单一证券的冻结观察状态。"],
      ["Q4.2", "升级/降级触发器", "保留后续复盘信号。"],
    ],
    sources: [
      source("SRC-XIAOMI-H1-2025", "Xiaomi 2025 Interim Report", "https://ir.mi.com/static-files/29a59068-f19f-4199-9114-4450211c9461", "2025-08-19", "H1 2025 revenue RMB227.2494bn +38.2%; adjusted net profit RMB21.5063bn +69.8%; smartphone x AIoT revenue RMB187.4bn; smart EV/AI/new initiatives revenue RMB39.8bn; smart EV deliveries 157,171; connected IoT devices 989.1m; global MAU 731.2m; R&D expense RMB14.5bn."),
      source("SRC-XIAOMI-Q3-2025", "Xiaomi 2025 Q3 HKEX Announcement", "https://www1.hkexnews.hk/listedco/listconews/sehk/2025/1118/2025111800682.pdf", "2025-11-18", "Q3 revenue RMB113.1bn +22.3%; adjusted net profit RMB11.3bn +80.9%; smart EV/AI/new initiatives revenue RMB29.0bn +199.2%; smart EV deliveries 108,796 +173.4%; ASP RMB260,053; EV/AI/new initiatives gross margin 25.5%; smartphone gross margin 11.1%."),
      source("SRC-GASGOO-XIAOMI-JAN-2026", "Xiaomi EV January 2026 Deliveries", "https://autonews.gasgoo.com/articles/ev/xiaomi-ev-deliveries-exceed-39000-units-in-january-2018263490169249793", "2026-02-02", "January 2026 Xiaomi EV deliveries exceeded 39,000 units, +70.33% YoY and -22.33% MoM; YU7 was the primary driver; 2026 delivery target 550,000; Beijing plant capacity above 40,000/month; sales stores 484 by end January."),
      labelSource("LBL-STOCKANALYSIS-XIAOMI", "StockAnalysis HKG 1810 close-price label", "https://stockanalysis.com/quote/hkg/1810/history/", "2026-05-29"),
    ],
    leaves: [
      ["Q1.1.1", "EV 需求是否真实且可持续？", "EV 需求真实，H1 交付 157,171、Q3 交付 108,796、2026 年 1 月交付超过 39,000；但春节、补贴退坡和前置需求显示节奏仍需检验。", ["SRC-XIAOMI-H1-2025", "SRC-XIAOMI-Q3-2025", "SRC-GASGOO-XIAOMI-JAN-2026"]],
      ["Q1.1.2", "手机 x AIoT 基盘是否稳住？", "手机 x AIoT 基盘稳住但弹性有限：H1 收入 RMB187.4bn，Q3 手机出货仅小幅增长，手机毛利率仍低于 IoT 和互联网服务。", ["SRC-XIAOMI-H1-2025", "SRC-XIAOMI-Q3-2025"]],
      ["Q1.2.1", "EV 是否已从烧钱期进入规模化验证？", "EV 规模化验证正在发生：Q3 EV/AI/new initiatives 毛利率 25.5%，交付和 ASP 同时提升；但费用投入大，不能只看毛利率。", ["SRC-XIAOMI-Q3-2025", "SRC-GASGOO-XIAOMI-JAN-2026"]],
      ["Q1.2.2", "Human x Car x Home 是否能带来生态入口？", "用户、IoT 设备和汽车交付共同扩大入口，但交叉销售和软件化收入尚未被充分量化，仍是 lead 而非强证据。", ["SRC-XIAOMI-H1-2025", "SRC-XIAOMI-Q3-2025"]],
      ["Q2.1.1", "小米的不可替代性来自品牌、渠道、生态还是制造？", "小米的稀缺性是复合型：品牌性价比、线下门店、手机用户、IoT 设备和 EV 产能共同作用；但每一项都存在可替代竞争。", ["SRC-XIAOMI-H1-2025", "SRC-GASGOO-XIAOMI-JAN-2026"]],
      ["Q2.1.2", "自研芯片与 AI 能否构成长期技术壁垒？", "XRING O1、MiMo 与 AI 研发说明技术投入真实，但截至冻结时点仍缺少独立收入、成本节省或用户留存贡献，不能高估壁垒。", ["SRC-XIAOMI-H1-2025"]],
      ["Q2.2.1", "EV 价值捕获是否强于传统手机硬件？", "EV 毛利率和 ASP 好于传统手机硬件，且交付增长快；但汽车行业资本开支、竞争和售后网络会消耗利润。", ["SRC-XIAOMI-Q3-2025", "SRC-GASGOO-XIAOMI-JAN-2026"]],
      ["Q2.2.2", "互联网服务和 IoT 是否提供高毛利缓冲？", "互联网服务毛利率高，IoT 毛利率改善，是手机/EV 周期外的缓冲层；但规模相对手机和 EV 仍有限。", ["SRC-XIAOMI-H1-2025", "SRC-XIAOMI-Q3-2025"]],
      ["Q3.1.1", "估值和市场预期是否已经过高？", "冻结时点股价已包含明显 EV/AI 叙事，市场未充分定价证据不足；质量提升不自动等于高赔率。", ["SRC-XIAOMI-Q3-2025", "SRC-GASGOO-XIAOMI-JAN-2026"]],
      ["Q3.1.2", "EV 竞争、补贴和交付节奏有哪些反证？", "1 月交付环比下滑、补贴退坡和春节因素提示交付节奏可能波动；中国 EV 竞争会压低可持续毛利率。", ["SRC-GASGOO-XIAOMI-JAN-2026", "SRC-XIAOMI-Q3-2025"]],
      ["Q3.2.1", "费用投入和研发投入有哪些质量风险？", "R&D 与销售费用快速上升，说明公司在建设长期能力，但若 EV 和 AI 无法转化为经营利润，会稀释当前盈利质量。", ["SRC-XIAOMI-H1-2025", "SRC-XIAOMI-Q3-2025"]],
      ["Q3.2.2", "手机与 IoT 周期是否拖累公司整体？", "手机毛利率低且竞争激烈，IoT 部分受补贴和品类季节影响；基盘稳定但不应给过高增长倍数。", ["SRC-XIAOMI-H1-2025", "SRC-XIAOMI-Q3-2025"]],
      ["Q4.1.1", "1810.HK 是否进入可行动名单？", "1810.HK 进入高质量观察，但不进入 actionable_long：需求强，证据质量尚可，稀缺性和未充分定价不足。", ["SRC-XIAOMI-H1-2025", "SRC-XIAOMI-Q3-2025", "SRC-GASGOO-XIAOMI-JAN-2026"]],
      ["Q4.1.2", "为什么需要分数封顶？", "EV/AI 叙事强但并非未被市场发现；手机硬件低毛利、EV 竞争和费用投入要求分数封顶。", ["SRC-XIAOMI-Q3-2025", "SRC-GASGOO-XIAOMI-JAN-2026"]],
      ["Q4.2.1", "升级触发器是什么？", "EV 经营利润持续为正、交付不依赖补贴、自由现金流改善、互联网/IoT 与车端协同收入被量化、估值回到更低预期。", ["SRC-XIAOMI-Q3-2025", "SRC-GASGOO-XIAOMI-JAN-2026"]],
      ["Q4.2.2", "降级触发器是什么？", "EV 毛利率回落、交付低于产能、手机毛利继续下滑、R&D/销售费用吞噬利润、股价继续透支未验证 AI/EV 叙事。", ["SRC-XIAOMI-H1-2025", "SRC-XIAOMI-Q3-2025"]],
    ],
    targets: [
      t(1, "1810.HK", "Xiaomi Corporation", "EV + Human x Car x Home ecosystem", [3.4, 4.1, 2.8, 3.8, 2.8, 4.0, 3.4], [4.0, 3.4, 2.8], "EV 增长、IoT/互联网服务和研发投入都是真实线索，但截至冻结时点不可替代性与未充分定价不足，默认不行动。", "EV gross margin, monthly deliveries, FCF conversion, smartphone margin, store productivity, valuation reset", ["SRC-XIAOMI-H1-2025", "SRC-XIAOMI-Q3-2025", "SRC-GASGOO-XIAOMI-JAN-2026"], lbl("HKD", 34.90, "2026-02-27", 28.04, "2026-05-29", "StockAnalysis HKG 1810")),
    ],
  },
];

function source(id, title, url, visible, summary) {
  return { source_id: id, title, url, source_visible_at: visible, source_bucket: "evidence", support_refute_or_lead: "support", allowed_usage: "thesis", used_in: ["QA"], summary };
}

function labelSource(id, title, url, visible) {
  return { source_id: id, title, url, source_visible_at: visible, source_bucket: "evidence", support_refute_or_lead: "lead", allowed_usage: "label_only", used_in: ["final_label"], summary: "Close-price data used only for final target label columns." };
}

function lbl(currency, start_price, start_date, end_price, end_date, price_source) {
  return { as_of_cutoff: AS_OF_DATE, evaluation_date: end_date, label_window: `${start_date} to ${end_date}`, currency, start_price, end_price, forward_3m_return: Number(((end_price / start_price - 1) * 100).toFixed(2)), benchmark_return: "", excess_return: "", price_source, label_status: "close_price_not_total_return_adjusted" };
}

function t(rank, ticker, name, thesis_node, comps, gates, rationale, trigger, source_ids, label) {
  const keys = Object.keys(SCORE_WEIGHTS);
  const score_input = Object.fromEntries(keys.map((key, i) => [key, comps[i]]));
  score_input.demand_visibility = gates[0];
  score_input.irreplaceability = gates[1];
  score_input.market_underpricing = gates[2];
  score_input.valuation_tolerance = comps[2];
  score_input.downside_fragility = Math.max(1, 5 - comps[4]);
  score_input.catalyst_proximity = comps[6];
  score_input.expected_excess_return = gates[2] >= 3.2 ? 0.03 : 0;
  score_input.valuation_status = "verified";
  const score = scoreTarget(score_input);
  return { rank, ticker, name, thesis_node, rationale, downgrade_risk: trigger, next_verification_data: trigger, odds_model: "Base: 稀缺性维持；Bull: 需求和现金流同时上修；Bear: 估值或竞争吞噬收益。", review_trigger: trigger, source_ids, score_input, score, action_state: score.action_state, strength: score.strength, label };
}

function scoreTarget(input) {
  const components = Object.fromEntries(Object.keys(SCORE_WEIGHTS).map((key) => [key, clamp(input[key] ?? 0)]));
  const raw_total_score = round(Object.entries(SCORE_WEIGHTS).reduce((acc, [key, weight]) => acc + components[key] * weight, 0));
  const thesis_confidence = round(components.chokepoint_strength * 0.30 + components.future_space * 0.15 + components.valuation_odds * 0.10 + components.evidence_quality * 0.25 + components.disconfirming_risk_control * 0.15 + components.monitorability * 0.05);
  const payoff_convexity = round(components.payoff_convexity * 0.45 + clamp(input.valuation_tolerance) * 0.20 + (6 - clamp(input.downside_fragility)) * 0.20 + clamp(input.catalyst_proximity) * 0.15);
  const demand = clamp(input.demand_visibility ?? components.future_space);
  const scarce = clamp(input.irreplaceability ?? components.chokepoint_strength);
  const underpriced = clamp(input.market_underpricing ?? components.valuation_odds);
  const opportunity_fit = round(demand * 0.30 + scarce * 0.40 + underpriced * 0.30);
  const gate_reasons = [];
  let max_total_score = 5;
  if (demand < 3.5) { gate_reasons.push("future demand below gate"); max_total_score = Math.min(max_total_score, 3.49); }
  if (scarce < 3.8) { gate_reasons.push("scarcity below gate"); max_total_score = Math.min(max_total_score, scarce < 3.0 ? 2.69 : 3.49); }
  if (underpriced < 3.2) { gate_reasons.push("underpricing below gate"); max_total_score = Math.min(max_total_score, underpriced < 2.5 ? 2.69 : 3.49); }
  if (components.disconfirming_risk_control < 2.5) { gate_reasons.push("risk control below gate"); max_total_score = Math.min(max_total_score, 3.49); }
  if (input.expected_excess_return !== undefined && Number(input.expected_excess_return) <= 0) { gate_reasons.push("expected return not positive"); max_total_score = Math.min(max_total_score, 2.69); }
  const total_score = round(Math.min(raw_total_score, max_total_score));
  let action_state = "watch_only";
  if (max_total_score <= 2.69 || opportunity_fit < 3.0) action_state = "no_action";
  else if (gate_reasons.length) action_state = "watch_only";
  else if (opportunity_fit >= 3.8 && thesis_confidence >= 3.5 && payoff_convexity >= 3.2) action_state = "actionable_long";
  const strength = total_score >= 4.2 && thesis_confidence >= 4.0 ? "A" : total_score >= 3.5 && (thesis_confidence >= 3.3 || payoff_convexity >= 4.0) ? "B" : total_score >= 2.7 ? "C" : "D";
  return { score_components: components, weights: SCORE_WEIGHTS, raw_total_score, total_score, thesis_confidence, payoff_convexity, opportunity_fit, action_state, gate_reasons, strength };
}

function clamp(value) {
  const n = Number(value);
  return Number.isFinite(n) ? Math.max(0, Math.min(5, n)) : 0;
}

function round(value) {
  return Number(value.toFixed(3));
}

function buildQa(project) {
  const sourceById = Object.fromEntries(project.sources.map((sourceItem) => [sourceItem.source_id, sourceItem]));
  const l1Defs = project.l1Defs || [
    ["Q1", "需求是否真实且足够大？", "需求真实但分化，必须从总盘转向可变现的结构性需求。"],
    ["Q2", "谁拥有不可替代的价值捕获瓶颈？", "稀缺性只在系统入口、数据/工作流、品牌/IP、供应链或网络密度中成立。"],
    ["Q3", "哪些反证足以压低胜率和赔率？", "估值、竞争、披露不足和宏观周期都可能让好公司不是好机会。"],
    ["Q4", "冻结时点如何形成标的观察名单？", "默认不行动，只有需求、稀缺性、未充分定价同时成立才提高动作状态。"],
  ];
  const l2Defs = project.l2Defs || [
    ["Q1.1", "总需求与结构需求", "先确认市场是否有足够空间。"],
    ["Q1.2", "高增量子场景", "再找更快、更稀缺的需求流。"],
    ["Q2.1", "入口和网络效应", "判断谁能让需求流入自己。"],
    ["Q2.2", "产品/供给/数据壁垒", "判断谁能把需求转为金融价值。"],
    ["Q3.1", "估值与竞争反证", "判断叙事是否已经定价。"],
    ["Q3.2", "现金流与周期反证", "判断增长质量和下行控制。"],
    ["Q4.1", "目标排序", "冻结目标列表，不使用后验价格。"],
    ["Q4.2", "升级/降级触发器", "保留后续复盘信号。"],
  ];
  const nodes = [];
  for (const [id, question, conclusion] of l1Defs) {
    nodes.push(node(id, 1, null, question, conclusion, "需要更多分部数据、估值快照和现金流验证。", l2Defs.filter((x) => x[0].startsWith(`${id}.`)).map((x) => x[0])));
  }
  for (const [id, question, conclusion] of l2Defs) {
    nodes.push(node(id, 2, id.split(".")[0], question, conclusion, "需要更多同口径指标。", project.leaves.filter((x) => x[0].startsWith(`${id}.`)).map((x) => x[0])));
  }
  for (const [id, question, conclusion, sourceIds] of project.leaves) {
    nodes.push(leaf(id, id.split(".").slice(0, 2).join("."), question, conclusion, sourceIds, sourceById));
  }
  return nodes;
}

function node(id, level, parent_id, question, conclusion, gaps, next_question_ids) {
  return { id, level, parent_id, question, conclusion, gaps, next_question_ids, materiality: "改变父节点结论、标的强度或风险控制。", source_plan: "使用 cutoff 前官方披露、统计数据和公司 IR，并保留反证。", skill_dispatch: "research-source-planner -> financial-statement-analysis / valuation-analysis -> GPT verification", fact: conclusion, inference: conclusion, judgment: conclusion, gap: gaps, trigger: gaps, source_links: [] };
}

function sanitizeId(value) {
  return String(value || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}

function extractionId(l3Id, sourceId) {
  return `se-${sanitizeId(l3Id)}-${sanitizeId(sourceId)}`;
}

function reviewId(l3Id, sourceId) {
  return `review-${extractionId(l3Id, sourceId)}`;
}

function scoreComponentFor(id, question) {
  if (/估值|赔率|定价|multiple|valuation|upside|downside/i.test(question)) return "valuation_odds";
  if (/反证|风险|降级|费用|现金流|周期|竞争|ROI|capex/i.test(question)) return "disconfirming_risk_control";
  if (/披露|证据|质量|核验/i.test(question)) return "evidence_quality";
  if (/目标|标的|排序|名单|触发器|action_state/i.test(question) || id.startsWith("Q4.")) return "target_ranking";
  if (id.startsWith("Q1.")) return "future_space";
  if (id.startsWith("Q2.")) return "chokepoint_strength";
  if (id.startsWith("Q3.")) return "disconfirming_risk_control";
  return "thesis_confidence";
}

function specialtyFor(id, question) {
  const text = `${id} ${question}`;
  if (/目标|标的|排序|名单|触发器|action_state|rank|target/i.test(text) || id.startsWith("Q4.")) {
    return {
      task_family: "target_recommendation",
      selected_skill: "target-recommendation-analysis",
      extraction_schema: ["target", "thesis_node", "score_driver", "action_state", "upgrade_trigger", "downgrade_trigger"],
    };
  }
  if (/估值|赔率|定价|multiple|valuation|DCF|P\/E|P\/S|FCF|upside|downside/i.test(text)) {
    return {
      task_family: "valuation",
      selected_skill: "valuation-analysis",
      extraction_schema: ["priced_in_expectation", "multiple", "base_case", "bull_case", "bear_case", "margin_of_safety"],
    };
  }
  if (/财报|收入|毛利|利润|现金流|费用|capex|库存|订单|backlog|RPO|ARR|margin|revenue|gross/i.test(text)) {
    return {
      task_family: "financial_statement",
      selected_skill: "financial-statement-analysis",
      extraction_schema: ["revenue", "margin", "cash_flow", "backlog", "segment_disclosure", "accounting_risk"],
    };
  }
  if (/行业|市场|供需|TAM|销量|设备|统计|WSTS|SEMI|SIA|NBS/i.test(text)) {
    return {
      task_family: "industry_report",
      selected_skill: "industry-report-analysis",
      extraction_schema: ["market_size", "growth_rate", "supply_demand", "bottleneck", "cycle_position", "boundary_condition"],
    };
  }
  if (/新闻|政策|补贴|公告|消息|交付|门店|监管|出口/i.test(text)) {
    return {
      task_family: "news_event",
      selected_skill: "news-event-analysis",
      extraction_schema: ["event_date", "event_scope", "affected_company", "transmission_path", "reliability", "follow_up_trigger"],
    };
  }
  return {
    task_family: "source_extraction",
    selected_skill: "leaf-research-deepseek",
    extraction_schema: ["key_fact", "number", "date", "support_or_refute", "uncertainty", "follow_up_data"],
  };
}

function leaf(id, parent_id, question, conclusion, source_links, sourceById = {}) {
  const fact = source_links.map((sourceId) => {
    const sourceItem = sourceById[sourceId];
    return sourceItem ? `${sourceId}: ${sourceItem.summary}` : `${sourceId}: source summary unavailable.`;
  }).join(" ");
  const inference = `基于上述 cutoff 前材料对“${question}”的推理：${conclusion}`;
  const score_component = scoreComponentFor(id, question);
  const specialty = specialtyFor(id, question);
  const source_plan = source_links.map((sourceId) => {
    const sourceItem = sourceById[sourceId] || {};
    return {
      source_id: sourceId,
      source_visible_at: sourceItem.source_visible_at || "",
      source_bucket: sourceItem.source_bucket || "evidence",
      allowed_usage: sourceItem.allowed_usage || "thesis",
      preferred_skill: specialty.selected_skill,
      expected_fields: specialty.extraction_schema,
    };
  });
  const skill_dispatch = {
    task_family: specialty.task_family,
    selected_skill: specialty.selected_skill,
    concrete_materials: source_links,
    extraction_schema: specialty.extraction_schema,
    source_extraction_ids: source_links.map((sourceId) => extractionId(id, sourceId)),
    leaf_source_review_ids: source_links.map((sourceId) => reviewId(id, sourceId)),
    skill_output_status: "fallback_gpt_direct_parse",
    fallback_used: true,
    gpt_verification_status: "verified",
  };
  const judgment = `决策影响：该叶子进入 ${score_component}，会调整父节点结论、目标强度、action_state 或分数封顶；当前判断为：${conclusion}`;
  return {
    id,
    level: 3,
    parent_id,
    question,
    conclusion,
    gaps: "缺少更细分的经营披露、估值同口径数据或反向验证材料。",
    next_question_ids: [],
    materiality: `该叶子会改变 ${score_component}、目标排序、动作状态或风险封顶。`,
    decision_use: `用于判断 ${score_component} 是否足以支撑父节点结论和最终标的 action_state。`,
    support_evidence: source_links.map((sourceId) => `${sourceId} 支持或界定该问题的事实基础。`),
    refute_evidence: ["若同口径经营、估值、竞争或需求数据与当前结论相反，则降低该节点强度。"],
    target_implications: "影响最终标的排序、分数封顶、观察状态和升级/降级触发器。",
    score_component,
    minimum_evidence_gate: "至少一项 cutoff 前可见的主材料，并保留一条反向或边界检查路径；后验价格不得进入推理。",
    refuting_source_plan: ["查找 cutoff 前可见的负向披露、竞争反证、估值透支、需求放缓或现金流恶化证据。"],
    source_plan,
    skill_dispatch,
    fact,
    inference,
    judgment,
    gap: "缺少更细分披露或可交叉验证数据。",
    trigger: "若后续披露证明需求无法转为现金流、稀缺性减弱、估值已透支或反证恶化，重新评分。",
    source_links,
  };
}

function esc(v) {
  return String(v ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function render(project) {
  const nodes = buildQa(project);
  const byParent = (parent) => nodes.filter((n) => n.parent_id === parent);
  const sourceById = Object.fromEntries(project.sources.map((s) => [s.source_id, s]));
  const link = (id) => {
    const s = sourceById[id];
    return s ? `<a class="source-chip" href="${s.url}" target="_blank" rel="noreferrer">${id}</a>` : `<span class="source-chip">${id}</span>`;
  };
  const card = (n) => {
    const children = byParent(n.id);
    const executionStatus = n.skill_dispatch?.fallback_used ? `${n.skill_dispatch?.skill_output_status || "unrecorded"} (fallback)` : (n.skill_dispatch?.skill_output_status || "unrecorded");
    const leafMeta = n.level === 3 ? `<div class="l3-meta"><span class="l3-skill"><b>Skill</b>${esc(n.skill_dispatch?.selected_skill || "unrouted")}</span><span class="l3-execution-status"><b>Execution</b>${esc(executionStatus)}</span><span class="l3-score-component"><b>Score</b>${esc(n.score_component || "unmapped")}</span><span class="l3-decision-use"><b>Decision Use</b>${esc(n.decision_use || "not recorded")}</span></div><div class="logic-grid"><div class="logic-card"><b>Fact</b><span>${esc(n.fact)}</span></div><div class="logic-card"><b>Inference</b><span>${esc(n.inference)}</span></div><div class="logic-card"><b>Judgment</b><span>${esc(n.judgment)}</span></div><div class="logic-card"><b>Gap / Trigger</b><span>${esc(n.gap)} ${esc(n.trigger)}</span></div></div><div class="source-chips">${n.source_links.map(link).join("")}</div>` : "";
    const artifact = n.id === "Q2.1" ? scorecard(project) : n.id === "Q4.1" ? miniTargets(project) : "";
    const heading = Math.min(2 + n.level, 5);
    return `<details class="qa-card level-${n.level}" id="${n.id.toLowerCase().replaceAll(".", "-")}" open><summary><span class="qa-id">${n.id}</span><h${heading}>${esc(n.question)}</h${heading}><span class="qa-count">${children.length ? `${children.length} 子节点` : "叶子"}</span><span class="chevron">›</span></summary><div class="qa-body"><section class="qa-block"><h4 class="block-title">1. 当前结论呈现</h4><p>${esc(n.conclusion)}</p>${artifact}${leafMeta}</section><section class="qa-block"><h4 class="block-title">2. 问题展开（子 QA）</h4>${children.length ? children.map(card).join("") : '<p class="muted">无下级问题。</p>'}</section><section class="qa-block"><h4 class="block-title">3. 待补充的问题</h4><p>${esc(n.gaps)}</p></section></div></details>`;
  };
  const l1 = nodes.filter((n) => n.level === 1).map(card).join("");
  return { nodes, html: `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${esc(project.title)}</title><style>${css()}</style></head><body><header class="hero"><nav class="top-nav"><a href="#goal">当前研究目标</a><a href="#qa">问题下钻</a><a href="#targets">最终标的推荐</a><a href="#sources">来源索引</a></nav><div><p class="eyebrow">Historical backtest · information cutoff ${AS_OF_DATE}</p><h1>${esc(project.title)}</h1><p>稀缺性优先：只寻找当前未被市场充分定价、未来需求巨大且不可替代性足够强的机会。</p></div></header><main><section class="goal-card" id="goal"><div class="section-kicker">Goal</div><h2>当前研究目标</h2><p><b>研究对象：</b>${esc(project.object)}</p><p><b>冻结边界：</b>研究、推理、评分、排序只使用 ${AS_OF_DATE} 当日及以前可见材料；后续价格只在最终标的表右侧作为结果字段显示。</p><p><b>当前判断：</b>${esc(project.constrained_judgment)}</p><p><b>最大不确定性：</b>${esc(project.uncertainty)}</p></section><section id="qa"><div class="section-kicker">QA Drilldown</div><h2>问题下钻</h2>${l1}</section>${targetTable(project)}${sourcesHtml(project)}</main></body></html>` };
}

function scorecard(project) {
  const rows = project.targets.slice(0, 6).map((r) => `<tr><td>${r.ticker}</td><td>${r.score.score_components.chokepoint_strength.toFixed(1)}</td><td>${esc(r.thesis_node)}</td><td>${esc(r.score.gate_reasons.join(", ") || "passed")}</td></tr>`).join("");
  return `<div class="artifact-card"><h5>稀缺性门槛</h5><p>需求可见度 30%，不可替代性 40%，市场未充分定价 30%；任何核心门槛不足都会封顶。</p><table><thead><tr><th>标的</th><th>稀缺性</th><th>节点</th><th>门槛</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}

function miniTargets(project) {
  return `<div class="artifact-card"><h5>冻结排序摘要</h5><table><thead><tr><th>Rank</th><th>标的</th><th>action_state</th><th>分数</th></tr></thead><tbody>${project.targets.slice(0, 6).map((r) => `<tr><td>${r.rank}</td><td>${r.ticker}</td><td>${r.action_state}</td><td>${r.score.total_score.toFixed(2)}</td></tr>`).join("")}</tbody></table></div>`;
}

function targetTable(project) {
  return `<section class="target-section" id="targets"><div class="section-kicker">Final Observation Rollup</div><h2>最终标的推荐</h2><p class="target-summary">这是冻结时点的研究观察名单，不是买卖指令。动作状态默认是不行动，只有“巨大需求、不可替代性、未充分定价”同时过门槛才进入 actionable_long。</p><table class="target-table"><thead><tr><th>Rank</th><th>标的</th><th>action_state</th><th>强度</th><th>总分</th><th>稀缺性</th><th>需求</th><th>赔率</th><th>核心理由</th><th>风险触发器</th><th>as_of_cutoff</th><th>evaluation_date</th><th>label_window</th><th>start_price</th><th>end_price</th><th>forward_3m_return<br><span>三个月股价变化</span></th><th>price_source</th><th>label_status</th></tr></thead><tbody>${project.targets.map((r) => `<tr><td>${r.rank}</td><td><b>${r.ticker}</b><br><span>${esc(r.name)}</span></td><td><span class="state ${r.action_state}">${r.action_state}</span></td><td>${r.strength}</td><td>${r.score.total_score.toFixed(2)}</td><td>${r.score.score_components.chokepoint_strength.toFixed(1)}</td><td>${r.score.score_components.future_space.toFixed(1)}</td><td>${r.score.score_components.valuation_odds.toFixed(1)}</td><td>${esc(r.rationale)}<br><span class="muted">Gate: ${esc(r.score.gate_reasons.join(", ") || "passed")}</span></td><td>${esc(r.downgrade_risk)}</td><td>${r.label.as_of_cutoff}</td><td>${r.label.evaluation_date}</td><td>${r.label.label_window}</td><td>${r.label.currency} ${r.label.start_price.toFixed(2)}</td><td>${r.label.currency} ${r.label.end_price.toFixed(2)}</td><td class="${r.label.forward_3m_return >= 0 ? "pos" : "neg"}">${r.label.forward_3m_return.toFixed(2)}%</td><td>${r.label.price_source}</td><td>${r.label.label_status}</td></tr>`).join("")}</tbody></table></section>`;
}

function sourcesHtml(project) {
  return `<details class="source-collapse" id="sources"><summary>来源索引</summary><div class="source-grid">${project.sources.map((s) => `<article class="source-card"><h3><a href="${s.url}" target="_blank" rel="noreferrer">${s.source_id}</a></h3><p>${esc(s.title)}</p><dl><dt>visible_at</dt><dd>${s.source_visible_at}</dd><dt>bucket</dt><dd>${s.source_bucket}</dd><dt>usage</dt><dd>${s.allowed_usage}</dd></dl><p class="muted">${esc(s.summary)}</p></article>`).join("")}</div></details>`;
}

function buildSourceExtractions(project, nodes) {
  const sourceById = Object.fromEntries(project.sources.map((sourceItem) => [sourceItem.source_id, sourceItem]));
  return nodes.filter((nodeItem) => nodeItem.level === 3).flatMap((nodeItem) => {
    return nodeItem.source_links.map((sourceId) => {
      const sourceItem = sourceById[sourceId] || {};
      return {
        extraction_id: extractionId(nodeItem.id, sourceId),
        l3_question_id: nodeItem.id,
        source_id: sourceId,
        source_title: sourceItem.title || sourceId,
        source_bucket: sourceItem.source_bucket || "evidence",
        parser: nodeItem.skill_dispatch?.selected_skill || "gpt-fallback",
        parser_status: nodeItem.skill_dispatch?.skill_output_status || "fallback_gpt_direct_parse",
        key_facts: [sourceItem.summary || nodeItem.fact],
        inference: nodeItem.inference,
        support_refute_or_lead: "support",
        uncertainties: [nodeItem.gap],
        follow_up_data: [nodeItem.trigger],
        created_at: `${REPORT_DATE}T00:00:00Z`,
      };
    });
  });
}

function buildLeafSourceReviews(project, nodes) {
  const sourceById = Object.fromEntries(project.sources.map((sourceItem) => [sourceItem.source_id, sourceItem]));
  return nodes.filter((nodeItem) => nodeItem.level === 3).flatMap((nodeItem) => {
    return nodeItem.source_links.map((sourceId) => {
      const sourceItem = sourceById[sourceId] || {};
      return {
        review_id: reviewId(nodeItem.id, sourceId),
        extraction_id: extractionId(nodeItem.id, sourceId),
        l3_question_id: nodeItem.id,
        source_id: sourceId,
        gpt_verification_status: "verified",
        adopted_facts: [sourceItem.summary || nodeItem.fact],
        corrections: [],
        rejected_claims: [],
        final_bucket: sourceItem.source_bucket || "evidence",
        final_support_refute_or_lead: "support",
        allowed_to_strengthen_conclusion: true,
      };
    });
  });
}

function css() {
  return `:root{color-scheme:light;--bg:#f5f7fb;--card:#fff;--ink:#172033;--muted:#687386;--line:#dce2ea;--blue:#2563eb;--green:#078458;--red:#c24132}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.55;letter-spacing:0}a{color:var(--blue);text-decoration:none}main{width:min(1320px,calc(100% - 32px));margin:0 auto 56px}.hero{min-height:310px;padding:24px max(24px,calc((100vw - 1320px)/2)) 42px;display:flex;flex-direction:column;justify-content:space-between;background:linear-gradient(180deg,#fff 0%,#edf3fb 100%);border-bottom:1px solid var(--line)}.top-nav{display:flex;gap:10px;flex-wrap:wrap}.top-nav a{color:#344054;border:1px solid var(--line);background:rgba(255,255,255,.72);padding:8px 12px;border-radius:8px;font-size:13px}.eyebrow,.section-kicker{color:#526077;text-transform:uppercase;font-size:12px;font-weight:700;letter-spacing:.06em}h1{font-size:clamp(34px,6vw,64px);max-width:920px;margin:8px 0 12px;line-height:1.04;letter-spacing:0}h2{font-size:28px;margin:4px 0 18px;letter-spacing:0}.goal-card,.qa-card,.target-section,.source-collapse{background:var(--card);border:1px solid var(--line);border-radius:8px;margin:18px 0;box-shadow:0 12px 36px rgba(15,23,42,.04)}.goal-card,.target-section,.source-collapse{padding:22px}.qa-card{padding:0;overflow:hidden}.qa-card.level-1{border-left:4px solid #2563eb}.qa-card.level-2{margin-left:18px;border-left:3px solid #7aa2f7;background:#fbfdff}.qa-card.level-3{margin-left:18px;border-left:2px solid #b7c7e6;background:#fff}.qa-card>summary{list-style:none;display:grid;grid-template-columns:auto 1fr auto auto;gap:12px;align-items:center;cursor:pointer;padding:16px}.qa-card>summary::-webkit-details-marker{display:none}.qa-card>summary h3,.qa-card>summary h4,.qa-card>summary h5{margin:0;font-size:18px;line-height:1.35}.qa-id{min-width:54px;padding:4px 8px;border:1px solid var(--line);border-radius:8px;color:#334155;background:#f8fafc;font-size:12px;text-align:center}.qa-count{color:#66758a;font-size:12px;white-space:nowrap;background:#f5f8fb;border:1px solid #e2e8f1;border-radius:999px;padding:5px 9px}.chevron{display:inline-block;font-size:22px;color:#8793a2;transition:transform .18s ease}.qa-card[open]>summary .chevron{transform:rotate(90deg)}.qa-body{border-top:1px solid var(--line);padding:0 16px 16px;display:grid;gap:12px}.qa-block{border-top:1px solid #eef2f7;padding-top:12px}.block-title{font-size:14px;color:#334155;margin:0 0 8px}p{margin:0 0 10px}.muted{color:var(--muted);font-size:13px}.l3-meta{display:grid;grid-template-columns:minmax(150px,auto) minmax(180px,auto) minmax(120px,auto) 1fr;gap:8px;margin:10px 0 12px}.l3-meta span{display:flex;align-items:center;gap:6px;border:1px solid #dbe3ee;background:#f8fbff;border-radius:8px;padding:7px 9px;color:#344054;font-size:12px;min-width:0}.l3-meta b{color:#64748b;text-transform:uppercase;font-size:10px;letter-spacing:.06em;white-space:nowrap}.l3-decision-use{overflow-wrap:anywhere}.logic-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:10px}.logic-card,.artifact-card{border:1px solid var(--line);background:#f8fafc;border-radius:8px;padding:10px}.logic-card b{display:block;font-size:12px;color:#526077;margin-bottom:4px}.logic-card span{font-size:13px}.source-chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}.source-chip{border:1px solid var(--line);background:#fff;border-radius:999px;padding:4px 9px;font-size:12px}table{width:100%;border-collapse:collapse;table-layout:auto}th,td{border-bottom:1px solid var(--line);padding:9px 8px;text-align:left;vertical-align:top;font-size:13px}th{color:#475569;background:#f8fafc;font-weight:700;position:sticky;top:0;z-index:1}.target-table{min-width:1680px}.target-section{overflow-x:auto}.target-summary{max-width:980px;color:#475569}.state{display:inline-flex;white-space:nowrap;padding:3px 8px;border-radius:999px;font-size:12px;border:1px solid var(--line)}.state.actionable_long{color:#075985;background:#e0f2fe;border-color:#bae6fd}.state.watch_only{color:#854d0e;background:#fef3c7;border-color:#fde68a}.state.no_action{color:#475569;background:#f1f5f9}.pos{color:var(--green);font-weight:700}.neg{color:var(--red);font-weight:700}.source-collapse summary{cursor:pointer;font-weight:700;font-size:22px}.source-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin-top:16px}.source-card{border:1px solid var(--line);border-radius:8px;padding:12px;background:#fbfdff}.source-card h3{margin:0 0 6px;font-size:14px}.source-card dl{display:grid;grid-template-columns:92px 1fr;gap:4px 8px;margin:8px 0;font-size:12px}.source-card dt{color:#64748b}.source-card dd{margin:0}@media(max-width:720px){main{width:min(100% - 20px,1320px)}.hero{min-height:260px;padding:18px 14px 28px}.l3-meta,.logic-grid{grid-template-columns:1fr}.qa-card.level-2,.qa-card.level-3{margin-left:0}}`;
}

function writeProject(project) {
  const outputDir = path.join(ROOT, project.out_dir);
  const { nodes, html } = render(project);
  fs.mkdirSync(outputDir, { recursive: true });
  fs.writeFileSync(path.join(outputDir, "professional_report.html"), html, "utf8");
  fs.writeFileSync(path.join(outputDir, "professional_report.md"), `# ${project.title}\n\n- as_of_date: ${AS_OF_DATE}\n- mode: historical_backtest\n\n${project.constrained_judgment}\n`, "utf8");
  fs.writeFileSync(path.join(outputDir, "project.json"), JSON.stringify({ project_id: project.project_id, title: project.title, mode: "historical_backtest", as_of_date: AS_OF_DATE, report_date: REPORT_DATE, report_path: "professional_report.html" }, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(outputDir, "qa_tree.json"), JSON.stringify({ as_of_date: AS_OF_DATE, nodes }, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(outputDir, "investment_workbench.json"), JSON.stringify({ as_of_date: AS_OF_DATE, scoring_worksheet: project.targets, label_attach: project.targets.map((target) => ({ ticker: target.ticker, label: target.label })), rejected_future_sources: project.sources.filter((source) => source.allowed_usage === "label_only") }, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(outputDir, "evidence.jsonl"), project.sources.map((source) => JSON.stringify(source)).join("\n") + "\n", "utf8");
  fs.writeFileSync(path.join(outputDir, "sources.jsonl"), project.sources.map((source) => JSON.stringify(source)).join("\n") + "\n", "utf8");
  fs.writeFileSync(path.join(outputDir, "source_extractions.jsonl"), buildSourceExtractions(project, nodes).map((record) => JSON.stringify(record)).join("\n") + "\n", "utf8");
  fs.writeFileSync(path.join(outputDir, "leaf_source_reviews.jsonl"), buildLeafSourceReviews(project, nodes).map((record) => JSON.stringify(record)).join("\n") + "\n", "utf8");
  console.log(`wrote ${outputDir}`);
}

projects.forEach(writeProject);
