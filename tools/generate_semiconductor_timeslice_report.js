const fs = require("fs");
const path = require("path");

const base = path.join(
  "research",
  "qa_projects",
  "semiconductor_hardware_timeslice_20260228"
);

const generatedAt = "2026-05-29T00:00:00+08:00";
const asOfDate = "2026-02-28";
const asOfPriceDate = "2026-02-27";
const evaluationDate = "2026-05-29";
const evaluationPriceDate = "2026-05-28";
const benchmark = {
  ticker: "SMH",
  asOfPrice: 406.37,
  evaluationPrice: 599.83,
  forwardReturn: 47.61
};

const sources = [
  {
    id: "ev_wsts_2025_autumn",
    title: "WSTS Autumn 2025 Semiconductor Market Forecast",
    bucket: "research_report",
    stance: "support",
    visibleAt: "2025-12-02",
    url: "https://www.wsts.org/esraCMS/extension/media/f/WST/7310/WSTS_FC-Release-2025_11.pdf",
    note:
      "Forecasts 2026 global semiconductor market at $975.46B, with Logic +32.1% and Memory +39.4%."
  },
  {
    id: "ev_sia_oct_2025_sales",
    title: "SIA October 2025 Global Semiconductor Sales",
    bucket: "research_report",
    stance: "support",
    visibleAt: "2025-12-04",
    url:
      "https://www.semiconductors.org/global-semiconductor-sales-increase-4-7-month-to-month-in-october/",
    note:
      "October 2025 semiconductor sales were $72.7B, +27.2% YoY; SIA cites WSTS forecast near $1T in 2026."
  },
  {
    id: "ev_semi_equipment_2025",
    title: "SEMI Year-End Total Semiconductor Equipment Forecast",
    bucket: "research_report",
    stance: "support",
    visibleAt: "2025-12-16",
    url:
      "https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports",
    note:
      "Equipment sales forecast: $133B in 2025, $145B in 2026, $156B in 2027; AI, HBM and advanced packaging are named drivers."
  },
  {
    id: "ev_nvda_fy26_q4",
    title: "NVIDIA FY2026 Q4 Results",
    bucket: "evidence",
    stance: "support",
    visibleAt: "2026-02-25",
    url:
      "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/",
    note:
      "Q4 Data Center revenue was $62.3B, +22% QoQ and +75% YoY; FY Data Center revenue reached $193.7B."
  },
  {
    id: "ev_avgo_fy25_q4",
    title: "Broadcom FY2025 Q4 Results",
    bucket: "evidence",
    stance: "support",
    visibleAt: "2025-12-11",
    url:
      "https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-fourth-quarter-and-fiscal-year-2025",
    note:
      "Q4 revenue $18.0B, +28% YoY; AI semiconductor revenue +74% YoY; Q1 FY2026 AI semiconductor revenue expected to double to $8.2B."
  },
  {
    id: "ev_amd_2025_q4",
    title: "AMD 2025 Q4 and FY Results",
    bucket: "evidence",
    stance: "support",
    visibleAt: "2026-02-03",
    url:
      "https://ir.amd.com/news-events/press-releases/detail/1276/amd-reports-fourth-quarter-and-full-year-2025-financial-results",
    note:
      "Q4 revenue $10.3B, +34% YoY; Data Center revenue $5.4B, +39% YoY, driven by EPYC and Instinct GPU ramp."
  },
  {
    id: "ev_tsmc_2025_q4",
    title: "TSMC 2025 Q4 Results",
    bucket: "evidence",
    stance: "support",
    visibleAt: "2026-01-15",
    url:
      "https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm",
    note:
      "Q4 revenue NT$1,046.09B, +20.5% YoY; advanced technologies 7nm and below were 77% of wafer revenue; 2026 capex budget $52B-$56B."
  },
  {
    id: "ev_mu_fy26_q1",
    title: "Micron FY2026 Q1 Results",
    bucket: "evidence",
    stance: "support",
    visibleAt: "2025-12-17",
    url:
      "https://micron.gcs-web.com/news-releases/news-release-details/micron-technology-inc-reports-results-first-quarter-fiscal-2026",
    note:
      "Revenue $13.64B; Cloud Memory revenue $5.284B with 66% gross margin; management tied record results to AI demand acceleration."
  },
  {
    id: "ev_asml_2025_q4",
    title: "ASML 2025 Q4 Results",
    bucket: "evidence",
    stance: "support",
    visibleAt: "2026-01-28",
    url: "https://www.asml.com/en/news/press-releases/2026/q4-2025-financial-results",
    note:
      "Q4 net sales EUR9.7B, net bookings EUR13.2B including EUR7.4B EUV; backlog EUR38.8B."
  },
  {
    id: "ev_amat_fy26_q1",
    title: "Applied Materials FY2026 Q1 Results",
    bucket: "evidence",
    stance: "support",
    visibleAt: "2026-02-12",
    url:
      "https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-announces-first-quarter-2026-results/",
    note:
      "Revenue $7.01B; Semiconductor Systems had record DRAM revenue; management highlighted leading-edge logic, HBM and advanced packaging."
  },
  {
    id: "ev_lrcx_dec_2025",
    title: "Lam Research December 2025 Quarter Results",
    bucket: "evidence",
    stance: "support",
    visibleAt: "2026-01-28",
    url:
      "https://www.sec.gov/Archives/edgar/data/707549/000070754926000006/lrcx_exhibitx991xq2x2026.htm",
    note:
      "Revenue $5.34B; management highlighted smaller, more complex 3D devices and packages under AI acceleration."
  },
  {
    id: "ev_klac_fy26_q2",
    title: "KLA FY2026 Q2 Results",
    bucket: "evidence",
    stance: "support",
    visibleAt: "2026-01-29",
    url:
      "https://ir.kla.com/news-events/press-releases/detail/509/kla-corporation-reports-fiscal-2026-second-quarter-results",
    note:
      "Revenue $3.30B; management described process control as key for foundry/logic, memory, advanced packaging and services."
  },
  {
    id: "ev_mrvl_fy26_q3",
    title: "Marvell FY2026 Q3 Results",
    bucket: "evidence",
    stance: "support",
    visibleAt: "2025-12-02",
    url:
      "https://investor.marvell.com/news-events/press-releases/detail/999/marvell-technology-inc-reports-third-quarter-of-fiscal-year-2026-financial-results",
    note:
      "Revenue $2.075B, +37% YoY; strong demand from data center products; Celestial AI acquisition strengthens scale-up interconnect roadmap."
  },
  {
    id: "ev_msft_fy26_q2",
    title: "Microsoft FY2026 Q2 Results",
    bucket: "evidence",
    stance: "support",
    visibleAt: "2026-01-28",
    url: "https://www.microsoft.com/en-us/Investor/earnings/FY-2026-Q2/press-release-webcast",
    note:
      "Revenue $81.3B, +17% YoY; Microsoft Cloud revenue $51.5B, +26%; six-month additions to property and equipment $49.27B."
  },
  {
    id: "ev_meta_2025_q4",
    title: "Meta 2025 Q4 Results",
    bucket: "evidence",
    stance: "support",
    visibleAt: "2026-01-28",
    url:
      "https://www.sec.gov/Archives/edgar/data/1326801/000162828026003832/meta-12312025xexhibit991.htm",
    note:
      "2025 capex including finance leases was $72.22B; 2026 capex guidance was $115B-$135B."
  },
  {
    id: "ev_goog_2025_q4",
    title: "Alphabet 2025 Q4 Results",
    bucket: "evidence",
    stance: "support",
    visibleAt: "2026-02-04",
    url:
      "https://www.sec.gov/Archives/edgar/data/1652044/000165204426000012/googexhibit991q42025.htm",
    note:
      "Alphabet expected 2026 capex of $175B-$185B and said AI investments and infrastructure drove revenue and growth."
  },
  {
    id: "ev_amzn_2025_q4",
    title: "Amazon 2025 Q4 Results",
    bucket: "evidence",
    stance: "support",
    visibleAt: "2026-02-05",
    url:
      "https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Fourth-Quarter-Results/default.aspx",
    note:
      "AWS Q4 sales +24% YoY; Amazon noted chips business growing triple digits YoY and memory-chip supply volatility risk."
  },
  {
    id: "ev_nasdaq_price_labels",
    title: "Nasdaq Historical Close Price Data",
    bucket: "evidence",
    stance: "lead",
    visibleAt: "2026-05-29",
    url:
      "https://api.nasdaq.com/api/quote/NVDA/historical?assetclass=stocks&fromdate=2026-02-25&todate=2026-05-29&limit=9999",
    note:
      "Price data used only in the isolated target-table evaluation columns; not dividend-adjusted total return."
  }
];

const sourceMap = new Map(sources.map((s) => [s.id, s]));

const scoreSchema = [
  ["需求流向", 15, "AI 基建增量是否真实进入该节点。"],
  ["不可替代性", 15, "客户是否难以绕开该节点，迁移成本是否高。"],
  ["供给/访问约束", 15, "产能、认证、IP、工艺、封装或生态访问是否稀缺。"],
  ["定价权", 15, "是否能转化为价格、毛利、take rate 或 backlog 质量。"],
  ["财务兑现", 15, "是否已体现在收入、毛利、现金流、capex 或订单中。"],
  ["证据质量", 10, "一手财报、行业数据和可复核材料是否充分。"],
  ["市场定价", 10, "截至截面日是否已被明显拥挤定价，分数越高代表越未被充分反映。"],
  ["反证韧性", 5, "是否有清晰可监控反证，且当前未触发。"]
];

const chokepoints = [
  {
    node: "HBM / 高端存储",
    score: 86,
    grade: "A",
    drivers:
      "Memory 和 DRAM 设备增长、Micron Cloud Memory 高毛利、HBM 供给约束共同指向最强价格/产能瓶颈。",
    breakdown: "14/13/15/14/14/9/5/2",
    risks: "HBM 扩产过快、普通 DRAM 价格回落、客户认证或份额不及预期。",
    sources: ["ev_wsts_2025_autumn", "ev_semi_equipment_2025", "ev_mu_fy26_q1"]
  },
  {
    node: "Custom ASIC / Ethernet / 光互连",
    score: 84,
    grade: "A-",
    drivers:
      "Broadcom AI semiconductor 翻倍指引、Marvell 数据中心需求和 interconnect 路线，显示云厂商 ASIC 与网络是 GPU 之外的第二利润池。",
    breakdown: "14/13/12/14/13/8/7/3",
    risks: "客户集中、云厂商自研议价、NVIDIA 生态锁定或 ASIC 项目延期。",
    sources: ["ev_avgo_fy25_q4", "ev_mrvl_fy26_q3"]
  },
  {
    node: "先进制程 / Foundry / 先进封装",
    score: 81,
    grade: "A-",
    drivers:
      "TSMC 7nm 及以下收入占比 77%、2026 capex 520-560 亿美元，说明 AI 芯片需求必须经过先进制程和封装产能兑现。",
    breakdown: "14/14/13/13/13/9/3/2",
    risks: "CoWoS/先进封装扩产释放、客户砍单、capex 回报低于预期。",
    sources: ["ev_tsmc_2025_q4", "ev_semi_equipment_2025"]
  },
  {
    node: "工艺设备 / 过程控制",
    score: 79,
    grade: "B+",
    drivers:
      "SEMI 设备上行、ASML 高 backlog、AMAT/Lam/KLA 均显示 AI 驱动的先进逻辑、HBM、先进封装扩产。",
    breakdown: "13/14/13/12/13/9/3/2",
    risks: "WFE 订单放缓、出口限制、设备商交付能力改善后瓶颈溢价下降。",
    sources: [
      "ev_semi_equipment_2025",
      "ev_asml_2025_q4",
      "ev_amat_fy26_q1",
      "ev_lrcx_dec_2025",
      "ev_klac_fy26_q2"
    ]
  },
  {
    node: "GPU / 通用 AI 加速平台",
    score: 78,
    grade: "B+",
    drivers:
      "NVIDIA 数据中心收入规模最大、AMD 数据中心快速增长；但截至截面日，市场已充分拥挤定价，且中国/ROI/客户集中风险需要折扣。",
    breakdown: "15/14/11/13/15/9/0/1",
    risks: "云厂商 ROI 转弱、自研 ASIC 替代、出口限制、产品代际交付延迟。",
    sources: ["ev_nvda_fy26_q4", "ev_amd_2025_q4", "ev_meta_2025_q4", "ev_goog_2025_q4"]
  }
];

const targets = [
  {
    rank: 1,
    ticker: "MU",
    name: "Micron Technology",
    targetClass: "HBM / 高端存储",
    frozenScore: 82,
    winProbability: "高",
    payoffOdds: "A-",
    asOfPrice: 412.37,
    evalPrice: 923.52,
    forwardReturn: 123.95,
    thesis:
      "截至 2026-02-28，Memory 是 WSTS 2026 增速最高的大类之一；Micron FY26 Q1 Cloud Memory 收入 52.84 亿美元、毛利率 66%，说明 AI 需求已经进入财务兑现。",
    scoreBreakdown: "瓶颈86 / 空间85 / 赔率78 / 证据82 / 反证70 / 可监控75",
    oddsModel:
      "Base: HBM/DRAM 紧供给延续，毛利维持高位；Bull: HBM 份额和定价继续提升；Bear: HBM 扩产和普通 DRAM 回落压低毛利。",
    downgrade:
      "Cloud Memory 毛利率快速下滑、库存/应收显著恶化、下一季收入指引低于截至截面日的高增速预期。",
    sources: ["ev_wsts_2025_autumn", "ev_semi_equipment_2025", "ev_mu_fy26_q1"]
  },
  {
    rank: 2,
    ticker: "AVGO",
    name: "Broadcom",
    targetClass: "Custom ASIC / Ethernet",
    frozenScore: 80,
    winProbability: "高",
    payoffOdds: "B+",
    asOfPrice: 319.55,
    evalPrice: 426.58,
    forwardReturn: 33.49,
    thesis:
      "AI 半导体收入同比 +74%，并指引 Q1 FY2026 AI 半导体同比翻倍到 82 亿美元；custom AI accelerators 和 Ethernet AI switches 是云厂商 GPU 外的关键算力路径。",
    scoreBreakdown: "瓶颈84 / 空间82 / 赔率72 / 证据82 / 反证68 / 可监控78",
    oddsModel:
      "Base: 大客户 ASIC 项目继续放量；Bull: Ethernet AI switch 和 ASIC 双轮驱动；Bear: 客户集中或云厂商压价导致增长兑现但利润率回落。",
    downgrade:
      "AI semiconductor 收入增速显著降档、ASIC 客户项目延期、网络交换芯片毛利率下降。",
    sources: ["ev_avgo_fy25_q4", "ev_mrvl_fy26_q3"]
  },
  {
    rank: 3,
    ticker: "NVDA",
    name: "NVIDIA",
    targetClass: "GPU / AI 加速平台",
    frozenScore: 78,
    winProbability: "高",
    payoffOdds: "B",
    asOfPrice: 177.19,
    evalPrice: 214.25,
    forwardReturn: 20.92,
    thesis:
      "FY2026 Q4 Data Center 收入 623 亿美元，同比 +75%，规模和生态最强；但市场定价已极拥挤，且公司 Q1 FY2027 指引不假设中国 Data Center compute 收入。",
    scoreBreakdown: "瓶颈78 / 空间90 / 赔率60 / 证据90 / 反证62 / 可监控82",
    oddsModel:
      "Base: Blackwell/Rubin 需求延续；Bull: 推理需求和平台绑定继续扩大；Bear: 云厂商 ROI、出口限制或 ASIC 替代压缩增量估值。",
    downgrade: "Data Center 环比增速明显降档、客户 capex 下修、China/出口限制影响扩大。",
    sources: ["ev_nvda_fy26_q4", "ev_msft_fy26_q2", "ev_meta_2025_q4", "ev_goog_2025_q4"]
  },
  {
    rank: 4,
    ticker: "MRVL",
    name: "Marvell Technology",
    targetClass: "Custom silicon / scale-up interconnect",
    frozenScore: 74,
    winProbability: "中高",
    payoffOdds: "A",
    asOfPrice: 81.69,
    evalPrice: 204.83,
    forwardReturn: 150.74,
    thesis:
      "Q3 FY2026 收入 20.75 亿美元，同比 +37%，数据中心需求强；Celestial AI 收购把 scale-up interconnect 路线纳入版图，赔率高但执行和整合不确定性更高。",
    scoreBreakdown: "瓶颈84 / 空间82 / 赔率82 / 证据68 / 反证58 / 可监控70",
    oddsModel:
      "Base: 数据中心和 custom silicon 继续增长；Bull: 光互连/scale-up interconnect 被大客户采用；Bear: 项目节奏慢或并购整合拖累盈利质量。",
    downgrade: "数据中心收入放缓、non-GAAP 与 GAAP 利润差距扩大、Celestial AI 路线延迟。",
    sources: ["ev_mrvl_fy26_q3", "ev_avgo_fy25_q4"]
  },
  {
    rank: 5,
    ticker: "TSM",
    name: "TSMC ADR",
    targetClass: "先进制程 / Foundry",
    frozenScore: 73,
    winProbability: "高",
    payoffOdds: "B-",
    asOfPrice: 374.58,
    evalPrice: 424.86,
    forwardReturn: 13.42,
    thesis:
      "先进制程收入占比 77%，3nm/5nm 合计 63%，并给出 520-560 亿美元 capex；确定性强，但作为全产业共识核心，赔率被估值和大规模 capex 吸收。",
    scoreBreakdown: "瓶颈81 / 空间80 / 赔率58 / 证据86 / 反证65 / 可监控75",
    oddsModel:
      "Base: AI/HPC 需求支撑先进节点利用率；Bull: 先进封装/高端节点定价权继续增强；Bear: 客户订单递延或 capex 回报摊薄。",
    downgrade: "先进节点占比下降、capex 上修但毛利率指引不升、客户库存调整。",
    sources: ["ev_tsmc_2025_q4", "ev_nvda_fy26_q4", "ev_amd_2025_q4"]
  },
  {
    rank: 6,
    ticker: "KLAC",
    name: "KLA",
    targetClass: "过程控制 / 检测量测",
    frozenScore: 72,
    winProbability: "中高",
    payoffOdds: "B",
    asOfPrice: 1524.55,
    evalPrice: 1927.63,
    forwardReturn: 26.44,
    thesis:
      "KLA 管理层明确把 AI 生态受益拆到 foundry/logic、memory、advanced packaging、services；过程控制在先进节点良率中不可绕开。",
    scoreBreakdown: "瓶颈79 / 空间72 / 赔率64 / 证据78 / 反证67 / 可监控72",
    oddsModel:
      "Base: 先进节点和 HBM 良率要求提升；Bull: process control 份额和服务收入提高；Bear: WFE 订单放缓或客户延迟验收。",
    downgrade: "收入指引低于 WFE 增速、毛利率下滑、foundry/memory 客户订单放缓。",
    sources: ["ev_klac_fy26_q2", "ev_semi_equipment_2025"]
  },
  {
    rank: 7,
    ticker: "LRCX",
    name: "Lam Research",
    targetClass: "刻蚀/沉积 / 3D 器件",
    frozenScore: 70,
    winProbability: "中高",
    payoffOdds: "B",
    asOfPrice: 233.89,
    evalPrice: 318.0,
    forwardReturn: 35.96,
    thesis:
      "Lam 的刻蚀/沉积暴露在更复杂 3D 器件、先进封装和存储升级；财务兑现稳定，但截至截面日，收入增速不像 HBM 或 ASIC 那样尖锐。",
    scoreBreakdown: "瓶颈79 / 空间72 / 赔率66 / 证据74 / 反证65 / 可监控70",
    oddsModel:
      "Base: WFE 与 memory 设备支出继续增长；Bull: 先进封装和 3D 器件超预期；Bear: 中国/存储客户订单波动。",
    downgrade: "系统收入转弱、support revenue 不能抵消订单周期、出口限制升级。",
    sources: ["ev_lrcx_dec_2025", "ev_semi_equipment_2025"]
  },
  {
    rank: 8,
    ticker: "AMD",
    name: "Advanced Micro Devices",
    targetClass: "GPU/CPU challenger",
    frozenScore: 66,
    winProbability: "中",
    payoffOdds: "A",
    asOfPrice: 200.21,
    evalPrice: 518.09,
    forwardReturn: 158.77,
    thesis:
      "Data Center 收入同比 +39%，Instinct GPU ramp 和 EPYC 需求提供 AI 替代路径；但截至截面日，GPU 生态和软件护城河仍弱于 NVIDIA，故冻结分数较低。",
    scoreBreakdown: "瓶颈78 / 空间82 / 赔率80 / 证据66 / 反证55 / 可监控68",
    oddsModel:
      "Base: CPU+GPU 数据中心组合继续扩张；Bull: MI/Helios 平台获得更大云厂商份额；Bear: 软件生态和供给认证低于预期。",
    downgrade: "Instinct 收入披露弱、数据中心毛利未改善、客户集中或平台路线延期。",
    sources: ["ev_amd_2025_q4", "ev_nvda_fy26_q4"]
  },
  {
    rank: 9,
    ticker: "ASML",
    name: "ASML",
    targetClass: "EUV lithography",
    frozenScore: 69,
    winProbability: "中高",
    payoffOdds: "C+",
    asOfPrice: 1450.56,
    evalPrice: 1605.77,
    forwardReturn: 10.7,
    thesis:
      "EUV 是先进逻辑/DRAM 的最硬设备瓶颈，Q4 bookings 和 backlog 强；但截至截面日，市场对 ASML 垄断性认知充分，且中国销售/出口限制形成折价。",
    scoreBreakdown: "瓶颈79 / 空间70 / 赔率55 / 证据80 / 反证62 / 可监控68",
    oddsModel:
      "Base: EUV 销售随先进节点扩产增长；Bull: High-NA 或 EUV 订单继续超预期；Bear: 出口限制和交付节奏压低增长。",
    downgrade: "bookings 下降、backlog 转化慢、China/DUV 风险扩大。",
    sources: ["ev_asml_2025_q4", "ev_semi_equipment_2025"]
  },
  {
    rank: 10,
    ticker: "AMAT",
    name: "Applied Materials",
    targetClass: "材料工程 / DRAM / 先进封装",
    frozenScore: 68,
    winProbability: "中",
    payoffOdds: "B-",
    asOfPrice: 372.3,
    evalPrice: 449.68,
    forwardReturn: 20.78,
    thesis:
      "管理层明确指出 leading-edge logic、HBM、advanced packaging 是高增长方向；但 Q1 FY2026 总收入同比略降，财务兑现不如 HBM 或 ASIC 纯度高。",
    scoreBreakdown: "瓶颈79 / 空间70 / 赔率62 / 证据72 / 反证63 / 可监控68",
    oddsModel:
      "Base: calendar 2026 半导体设备业务增长超过 20%；Bull: DRAM/HBM 和先进封装投入超预期；Bear: 总收入恢复低于管理层预期。",
    downgrade: "Semiconductor Systems 增速不及 WFE、库存上升、服务/备件无法支撑毛利。",
    sources: ["ev_amat_fy26_q1", "ev_semi_equipment_2025"]
  }
];

const excludedWatchlist = [
  {
    ticker: "INTC",
    name: "Intel",
    asOfPrice: 45.61,
    evalPrice: 120.89,
    forwardReturn: 165.05,
    reason:
      "截至 2026-02-28 的硬件瓶颈证据未能把 Intel 直接映射到高置信价值捕获节点；后验涨幅提示框架可能低估了政策/代工转机/低估值弹性，但不能反向改写本次冻结推荐。"
  }
];

const priceLabels = targets.map((t) => ({
  ticker: t.ticker,
  as_of_date: asOfDate,
  as_of_price_date: asOfPriceDate,
  evaluation_date: evaluationDate,
  evaluation_price_date: evaluationPriceDate,
  label_window: `${asOfPriceDate} close to ${evaluationPriceDate} close`,
  start_price: t.asOfPrice,
  end_price: t.evalPrice,
  forward_3m_return: t.forwardReturn,
  benchmark: benchmark.ticker,
  benchmark_return: benchmark.forwardReturn,
  excess_return: Number((t.forwardReturn - benchmark.forwardReturn).toFixed(2)),
  price_source: "Nasdaq historical close API",
  label_status: "verified_close_only_not_total_return"
}));

const qaNodes = [
  {
    id: "q1",
    level: "level-1",
    title: "Q1 需求真实性：AI 基建是否真的进入半导体硬件订单？",
    conclusion:
      "截至 2026-02-28，需求不是单纯叙事：WSTS/SIA/SEMI 的行业数据、NVIDIA/Broadcom/AMD/Micron/TSMC 的收入兑现，以及 hyperscaler capex 指引共同支持 AI 硬件需求真实存在。但它不是“所有半导体都受益”，而是集中在 logic、memory、advanced packaging 和数据中心网络。",
    expansion:
      "Q1.1 看终端 capex，Q1.2 看半导体公司收入和毛利，Q1.3 看需求是否穿透到设备和制造。",
    gaps:
      "仍缺少每家云厂商按 GPU/ASIC/HBM/网络拆分的 capex 明细；ROI 回收速度在截面日仍是最大不确定性。",
    sources: [
      "ev_wsts_2025_autumn",
      "ev_sia_oct_2025_sales",
      "ev_semi_equipment_2025",
      "ev_nvda_fy26_q4",
      "ev_avgo_fy25_q4",
      "ev_amd_2025_q4",
      "ev_mu_fy26_q1",
      "ev_msft_fy26_q2",
      "ev_meta_2025_q4",
      "ev_goog_2025_q4",
      "ev_amzn_2025_q4"
    ],
    children: [
      {
        id: "q1-1",
        level: "level-2",
        title: "Q1.1 终端 capex 是否足以支撑芯片链收入？",
        conclusion:
          "Microsoft、Meta、Alphabet、Amazon 在截面日前已公开显示 AI 基建资本开支大幅上行，说明芯片需求有终端预算锚。",
        expansion:
          "Microsoft 六个月 PPE 增加额 492.7 亿美元；Meta 指引 2026 capex 1150-1350 亿美元；Alphabet 指引 1750-1850 亿美元；Amazon AWS 增长和 chips business 三位数增长形成终端验证。",
        gaps:
          "capex 转化为真实 AI 收入和自由现金流的速度仍需季度验证。",
        sources: ["ev_msft_fy26_q2", "ev_meta_2025_q4", "ev_goog_2025_q4", "ev_amzn_2025_q4"],
        children: [
          {
            id: "q1-1-1",
            level: "level-3",
            title: "Q1.1.1 云厂商是否已经把预算投向 AI 基建？",
            conclusion:
              "是。Microsoft、Meta、Alphabet 和 Amazon 在截面日前披露的资本开支、PPE 增加额或 AI 基建投入都显示预算已经进入硬件供给链。",
            expansion:
              "该叶子问题决定 Q1 是否能从需求叙事升级为终端预算证据；若没有 hyperscaler capex 锚，芯片公司收入增长容易被解释为短期拉货。",
            gaps:
              "仍缺少按 GPU、ASIC、网络、存储和数据中心土建拆分的预算结构。",
            sources: ["ev_msft_fy26_q2", "ev_meta_2025_q4", "ev_goog_2025_q4", "ev_amzn_2025_q4"]
          },
          {
            id: "q1-1-2",
            level: "level-3",
            title: "Q1.1.2 终端预算的主要反证是什么？",
            conclusion:
              "主要反证是 capex 上行没有同步转化为云收入、AI 产品收入或自由现金流改善；该反证在截面日尚未被充分验证。",
            expansion:
              "这决定需求证据的使用边界：capex 是订单锚，但不是 ROI 证明，因此 Q3 必须把 ROI 作为核心红灯。",
            gaps:
              "缺少 AI workload 利用率、单位推理成本、客户付费和 capex 回收期披露。",
            sources: ["ev_meta_2025_q4", "ev_goog_2025_q4", "ev_amzn_2025_q4"]
          }
        ]
      },
      {
        id: "q1-2",
        level: "level-2",
        title: "Q1.2 芯片公司收入是否已经兑现？",
        conclusion:
          "GPU、custom ASIC、CPU/GPU challenger、HBM 与 advanced foundry 均已有一手财务兑现，需求链条不是只停留在订单传闻。",
        expansion:
          "NVIDIA Data Center、Broadcom AI semiconductor、AMD Data Center、Micron Cloud Memory、TSMC advanced node share 同时增强。",
        gaps:
          "ASIC 客户集中度、HBM 份额、AI GPU 之外的平台生态披露仍不充分。",
        sources: [
          "ev_nvda_fy26_q4",
          "ev_avgo_fy25_q4",
          "ev_amd_2025_q4",
          "ev_mu_fy26_q1",
          "ev_tsmc_2025_q4"
        ],
        children: [
          {
            id: "q1-2-1",
            level: "level-3",
            title: "Q1.2.1 AI 计算芯片收入是否已兑现？",
            conclusion:
              "已兑现。NVIDIA Data Center、Broadcom AI semiconductor 和 AMD Data Center 都在截面日前显示收入增长，说明 AI 计算需求已穿透到芯片公司财务。",
            expansion:
              "这个叶子问题支撑 GPU、ASIC 和 challenger 路径进入 Q4 观察池，并为 Q2 的价值捕获评分提供财务兑现证据。",
            gaps:
              "仍缺少按客户和产品世代拆分的 AI 加速器收入、毛利和订单能见度。",
            sources: ["ev_nvda_fy26_q4", "ev_avgo_fy25_q4", "ev_amd_2025_q4"]
          },
          {
            id: "q1-2-2",
            level: "level-3",
            title: "Q1.2.2 存储与制造是否已同步兑现？",
            conclusion:
              "已同步。Micron Cloud Memory 和 TSMC advanced node share 显示 AI 需求不只停在 GPU，而是扩散到 HBM/高端存储和先进制造。",
            expansion:
              "这决定 Q2 不能只看 GPU 平台，而必须把 HBM、先进制程和先进封装列入高分瓶颈。",
            gaps:
              "缺少 HBM 代际份额、客户认证、CoWoS/先进封装产能和先进节点客户结构的更细数据。",
            sources: ["ev_mu_fy26_q1", "ev_tsmc_2025_q4"]
          }
        ]
      }
    ]
  },
  {
    id: "q2",
    level: "level-1",
    title: "Q2 价值捕获瓶颈：哪些节点能把需求变成利润？",
    conclusion:
      "最强瓶颈是 HBM/高端存储，其次是 custom ASIC/Ethernet、先进制程/封装、工艺设备/过程控制。GPU 平台最强但已被充分定价，设备链确定性高但赔率受周期和出口限制约束。",
    expansion:
      "用固定 100 分 chokepoint 公式评分，目标是把叙事变成可比较的需求流、不可替代性、供给约束、定价权、财务兑现和市场定价。",
    gaps:
      "封装产能、HBM 客户份额、ASIC 项目量产节奏和设备交期仍需要后续一手披露。",
    sources: [
      "ev_semi_equipment_2025",
      "ev_asml_2025_q4",
      "ev_amat_fy26_q1",
      "ev_lrcx_dec_2025",
      "ev_klac_fy26_q2",
      "ev_tsmc_2025_q4",
      "ev_mu_fy26_q1",
      "ev_avgo_fy25_q4",
      "ev_mrvl_fy26_q3"
    ],
    artifact: "chokepoint",
    children: [
      {
        id: "q2-1",
        level: "level-2",
        title: "Q2.1 HBM 是否是最高纯度瓶颈？",
        conclusion:
          "是。Memory 2026 增速、DRAM 设备支出、Micron Cloud Memory 毛利和 HBM/AI 需求共振，使高端存储成为截面日最高分瓶颈。",
        expansion:
          "HBM 的稀缺不只是 wafer，而是良率、堆叠、封装、客户认证和长期供货协议共同约束。",
        gaps: "缺少按客户和 HBM 代际拆分的收入/份额。",
        sources: ["ev_wsts_2025_autumn", "ev_semi_equipment_2025", "ev_mu_fy26_q1"],
        children: [
          {
            id: "q2-1-1",
            level: "level-3",
            title: "Q2.1.1 HBM 的需求流是否足够明确？",
            conclusion:
              "明确。WSTS 的 Memory 增长、SEMI 对 HBM/先进封装驱动的设备需求判断，以及 Micron Cloud Memory 的收入和毛利，共同指向 AI 训练/推理对高端存储的强需求流。",
            expansion:
              "该叶子决定 HBM 是否只是周期性 DRAM 反弹，还是 AI 硬件链条中的结构性瓶颈。",
            gaps:
              "需要客户级 HBM 订单、长期供货协议、代际切换和库存数据来确认持续性。",
            sources: ["ev_wsts_2025_autumn", "ev_semi_equipment_2025", "ev_mu_fy26_q1"]
          },
          {
            id: "q2-1-2",
            level: "level-3",
            title: "Q2.1.2 HBM 的价值捕获来自哪里？",
            conclusion:
              "价值捕获来自供给约束、客户认证、堆叠/封装复杂度和高毛利兑现，而不只是总位元需求增长。",
            expansion:
              "这个叶子决定 MU 在 Q4 中可以高于普通 memory beta，因为它承接的是高端存储瓶颈而非单纯行业价格弹性。",
            gaps:
              "仍缺少 HBM 具体毛利、客户集中度、产能扩张节奏和良率数据。",
            sources: ["ev_mu_fy26_q1", "ev_semi_equipment_2025"]
          }
        ]
      },
      {
        id: "q2-2",
        level: "level-2",
        title: "Q2.2 Custom ASIC 与网络是否构成第二利润池？",
        conclusion:
          "是，但客户集中和项目节奏风险高于 HBM。Broadcom 的 AI semiconductor 指引和 Marvell 的 data center/interconnect 路线说明云厂商自研和网络互连不是边缘机会。",
        expansion:
          "ASIC 与 Ethernet/光互连可以绕开部分 GPU 供给和成本压力，但会把议价权从通用 GPU 平台转到少数云厂商定制项目。",
        gaps: "缺少每个大客户 ASIC 的量产节点、毛利率和生命周期披露。",
        sources: ["ev_avgo_fy25_q4", "ev_mrvl_fy26_q3"],
        children: [
          {
            id: "q2-2-1",
            level: "level-3",
            title: "Q2.2.1 Custom ASIC 需求是否形成独立利润池？",
            conclusion:
              "形成。Broadcom 的 AI semiconductor 增长和指引显示 hyperscaler 定制芯片已成为 GPU 之外的独立利润池。",
            expansion:
              "该叶子支撑 AVGO 的高排序：它的优势不只是半导体 beta，而是直接承接云厂商 ASIC 定制需求。",
            gaps:
              "缺少客户数量、单客户项目寿命、产品代际和毛利率拆分。",
            sources: ["ev_avgo_fy25_q4"]
          },
          {
            id: "q2-2-2",
            level: "level-3",
            title: "Q2.2.2 网络与互连是否是放大器？",
            conclusion:
              "是。Marvell 数据中心需求和 scale-up interconnect 路线说明 AI 集群扩张会把价值从计算芯片扩展到互连和网络。",
            expansion:
              "该叶子支撑 MRVL 进入观察清单，但同时要求更高的执行折扣，因为互连路线、并购整合和客户节奏不如 HBM 证据直接。",
            gaps:
              "缺少 scale-up interconnect 量产客户、收入贡献、毛利和并购整合里程碑。",
            sources: ["ev_mrvl_fy26_q3"]
          }
        ]
      }
    ]
  },
  {
    id: "q3",
    level: "level-1",
    title: "Q3 反证与赔率：什么会证明这不是好机会？",
    conclusion:
      "主要反证来自四处：AI capex ROI 低于预期、HBM/DRAM 供给释放过快、设备订单和先进制程 capex 延后、出口限制或客户集中导致高毛利不可持续。估值上，高确定性龙头未必提供最高风险补偿。",
    expansion:
      "Q3 把行业风险绑定到 Q2 瓶颈和 Q4 标的：需求红灯、供给红灯、政策红灯、估值红灯会分别下调不同节点。",
    gaps:
      "截至截面日不能使用后续财报或价格表现确认风险是否发生；后续价格数据必须隔离在最终表格的标签列。",
    sources: [
      "ev_nvda_fy26_q4",
      "ev_asml_2025_q4",
      "ev_amat_fy26_q1",
      "ev_meta_2025_q4",
      "ev_goog_2025_q4",
      "ev_amzn_2025_q4"
    ],
    artifact: "risk",
    children: [
      {
        id: "q3-1",
        level: "level-2",
        title: "Q3.1 需求反证如何触发？",
        conclusion:
          "若云厂商 capex 上修但云收入、AI 产品收入或现金流没有同步改善，芯片链估值会首先受压。",
        expansion:
          "Meta、Alphabet、Amazon 的 capex 指引很大，本身既是需求证据，也是 ROI 风险来源。",
        gaps: "缺少 AI workload 利用率、单 token 成本、capex 回收期的一手披露。",
        sources: ["ev_meta_2025_q4", "ev_goog_2025_q4", "ev_amzn_2025_q4"],
        children: [
          {
            id: "q3-1-1",
            level: "level-3",
            title: "Q3.1.1 capex 是否可能先于收入过度扩张？",
            conclusion:
              "可能。Meta、Alphabet 和 Amazon 的 AI 基建投入很大，既支撑芯片需求，也抬高未来 ROI 证明门槛。",
            expansion:
              "该叶子定义需求反证：如果 capex 增长不能被云收入、AI 产品收入或现金流吸收，硬件链估值会承压。",
            gaps:
              "缺少 AI 工作负载利用率、客户付费转化和单位经济披露。",
            sources: ["ev_meta_2025_q4", "ev_goog_2025_q4", "ev_amzn_2025_q4"]
          },
          {
            id: "q3-1-2",
            level: "level-3",
            title: "Q3.1.2 哪些标的最受 ROI 反证影响？",
            conclusion:
              "高估值计算平台和 custom silicon 受影响更快，包括 NVDA、AMD、AVGO 和 MRVL；设备和制造链则更多受订单递延影响。",
            expansion:
              "该叶子把需求反证映射到 Q4 风险权重，而不是泛泛地说 AI 需求有风险。",
            gaps:
              "需要按客户 capex 调整、订单取消、云服务增长和 AI 产品收入来动态更新。",
            sources: ["ev_nvda_fy26_q4", "ev_amd_2025_q4", "ev_avgo_fy25_q4", "ev_mrvl_fy26_q3"]
          }
        ]
      },
      {
        id: "q3-2",
        level: "level-2",
        title: "Q3.2 供给反证如何触发？",
        conclusion:
          "HBM/DRAM 和设备订单如果快速扩张到供给过剩，MU/LRCX/AMAT 的赔率会比 NVDA/AVGO 更快受损。",
        expansion:
          "因此每个目标都绑定了毛利率、订单、backlog、capex 回报和客户认证触发器。",
        gaps: "需要 2026 后续季度按节点更新。",
        sources: ["ev_semi_equipment_2025", "ev_mu_fy26_q1", "ev_amat_fy26_q1", "ev_lrcx_dec_2025"],
        children: [
          {
            id: "q3-2-1",
            level: "level-3",
            title: "Q3.2.1 HBM/DRAM 供给释放会削弱什么？",
            conclusion:
              "会削弱 MU 的定价权和高毛利叙事，也会降低 memory 设备支出的瓶颈溢价。",
            expansion:
              "该叶子将 HBM 高分瓶颈绑定到可证伪触发器：扩产、良率改善、价格回落或客户认证不及预期。",
            gaps:
              "缺少 HBM 产能、良率、价格和客户认证的连续披露。",
            sources: ["ev_mu_fy26_q1", "ev_semi_equipment_2025"]
          },
          {
            id: "q3-2-2",
            level: "level-3",
            title: "Q3.2.2 WFE 订单转弱会影响哪些设备股？",
            conclusion:
              "AMAT、LRCX、KLAC、ASML 都会受影响，但影响机制不同：AMAT/LRCX 更受存储和工艺周期影响，KLAC 更贴近良率控制，ASML 受 EUV backlog 与出口限制共同影响。",
            expansion:
              "该叶子把设备链从一个整体拆成不同风险暴露，避免把所有 WFE 标的用同一个触发器处理。",
            gaps:
              "需要订单、backlog、交付周期、中国销售和先进封装相关收入更新。",
            sources: ["ev_amat_fy26_q1", "ev_lrcx_dec_2025", "ev_klac_fy26_q2", "ev_asml_2025_q4"]
          }
        ]
      }
    ]
  },
  {
    id: "q4",
    level: "level-1",
    title: "Q4 标的观察：冻结排序如何落到证券？",
    conclusion:
      "冻结排序优先选择 HBM/高端存储和 custom ASIC/Ethernet，其次是 GPU 平台、advanced foundry 与设备过程控制。排序只反映截面日前可见证据、瓶颈强度、赔率假设和反证可控性。",
    expansion:
      "推荐冻结发生在任何后续价格数据加入之前。Q4 只解释当时为什么把这些证券纳入观察清单，不评价后续表现。",
    gaps:
      "仍需更细的客户份额、订单、毛利和产能数据来区分强证据资产与高赔率资产。",
    sources: [
      "ev_mu_fy26_q1",
      "ev_avgo_fy25_q4",
      "ev_mrvl_fy26_q3",
      "ev_nvda_fy26_q4",
      "ev_tsmc_2025_q4",
      "ev_amd_2025_q4",
      "ev_semi_equipment_2025"
    ],
    children: [
      {
        id: "q4-1",
        level: "level-2",
        title: "Q4.1 哪些证券直接承接高分瓶颈？",
        conclusion:
          "高纯度瓶颈承接优先落在 MU、AVGO、MRVL 和 NVDA。MU 对应 HBM/高端存储，AVGO/MRVL 对应 custom ASIC、网络与互连，NVDA 对应 GPU 平台和生态控制。",
        expansion:
          "排序时先看 Q2 的瓶颈强度，再看公司收入暴露、毛利兑现、客户集中和估值拥挤程度；因此同样受益 AI，分数也会因价值捕获路径不同而分化。",
        gaps:
          "缺少 HBM 客户份额、ASIC 项目寿命、互连方案量产节奏和 GPU 平台客户集中度的更细披露。",
        sources: ["ev_mu_fy26_q1", "ev_avgo_fy25_q4", "ev_mrvl_fy26_q3", "ev_nvda_fy26_q4"],
        children: [
          {
            id: "q4-1-1",
            level: "level-3",
            title: "Q4.1.1 为什么 MU 是 HBM 直接承接标的？",
            conclusion:
              "MU 的 Cloud Memory 收入和高毛利让 HBM/高端存储瓶颈直接落到财务兑现上，因此在 as-of 排序中获得最高优先级。",
            expansion:
              "该叶子把 Q2 的 HBM 分数映射到证券：需求流、供给约束、定价权和财务兑现都能在 Micron 材料中找到支撑。",
            gaps:
              "需要 HBM 客户份额、代际结构、长期协议和普通 DRAM 周期风险的更细拆分。",
            sources: ["ev_mu_fy26_q1", "ev_wsts_2025_autumn", "ev_semi_equipment_2025"]
          },
          {
            id: "q4-1-2",
            level: "level-3",
            title: "Q4.1.2 为什么 AVGO/MRVL/NVDA 同属高分瓶颈但排序不同？",
            conclusion:
              "AVGO 和 MRVL 承接 ASIC/互连利润池，NVDA 承接最强 GPU 平台；差异来自证据质量、客户集中、执行不确定性和市场定价拥挤度。",
            expansion:
              "该叶子解释为什么高确定性不等于最高排序：NVDA 证据最强但拥挤定价更高，MRVL 赔率更高但执行证据较弱，AVGO 介于二者之间。",
            gaps:
              "缺少定制芯片客户明细、互连量产节奏和 GPU 平台客户集中度。",
            sources: ["ev_avgo_fy25_q4", "ev_mrvl_fy26_q3", "ev_nvda_fy26_q4"]
          }
        ]
      },
      {
        id: "q4-2",
        level: "level-2",
        title: "Q4.2 哪些证券承接制造与设备确定性？",
        conclusion:
          "TSM、KLAC、LRCX、ASML、AMAT 承接先进制程、先进封装、良率控制和 WFE 投入。它们的确定性强，但赔率更受资本开支周期、出口限制和市场预期吸收程度约束。",
        expansion:
          "TSM 是先进节点和封装的核心承接者；KLAC 的过程控制更贴近良率瓶颈；LRCX/AMAT 暴露于刻蚀、沉积、DRAM 和先进封装；ASML 的 EUV 稀缺性最高但共识也最充分。",
        gaps:
          "需要持续跟踪订单、backlog、交付周期、先进封装产能、客户 capex 兑现和出口限制变化。",
        sources: [
          "ev_tsmc_2025_q4",
          "ev_klac_fy26_q2",
          "ev_lrcx_dec_2025",
          "ev_asml_2025_q4",
          "ev_amat_fy26_q1",
          "ev_semi_equipment_2025"
        ],
        children: [
          {
            id: "q4-2-1",
            level: "level-3",
            title: "Q4.2.1 TSM 与 KLAC 的确定性来自哪里？",
            conclusion:
              "TSM 的先进节点/封装收入和 capex 计划给出制造确定性，KLAC 的过程控制暴露在良率瓶颈中，二者都比普通设备周期更接近 AI 结构性需求。",
            expansion:
              "该叶子把先进制造和过程控制从泛设备链中单独识别出来，解释它们为何进入中高置信观察清单。",
            gaps:
              "需要先进封装产能、良率控制投入、客户结构和 capex 回报数据。",
            sources: ["ev_tsmc_2025_q4", "ev_klac_fy26_q2"]
          },
          {
            id: "q4-2-2",
            level: "level-3",
            title: "Q4.2.2 ASML/LRCX/AMAT 为什么排序靠后？",
            conclusion:
              "ASML 稀缺性强但共识充分且受出口限制约束；LRCX/AMAT 受益存储、刻蚀、沉积和先进封装，但财务弹性和周期风险更混合。",
            expansion:
              "该叶子解释设备链排序：设备是必要瓶颈，但不是所有设备商都拥有同等未定价空间。",
            gaps:
              "需要 bookings、backlog、交付周期、中国销售和先进封装相关收入拆分。",
            sources: ["ev_asml_2025_q4", "ev_lrcx_dec_2025", "ev_amat_fy26_q1", "ev_semi_equipment_2025"]
          }
        ]
      },
      {
        id: "q4-3",
        level: "level-2",
        title: "Q4.3 哪些证券属于替代路径或高赔率观察？",
        conclusion:
          "AMD 属于 GPU/CPU challenger 路径，具备数据中心增长和平台替代空间，但截至截面日，软件生态、客户认证和毛利兑现仍弱于高分瓶颈资产。",
        expansion:
          "因此 AMD 可以进入观察清单，但冻结排序不能只因潜在弹性而越过证据更强、价值捕获更清晰的 HBM、ASIC、GPU 平台和先进制造节点。",
        gaps:
          "需要更多 Instinct 平台收入、客户采用、毛利率、软件生态和供给认证数据来提高排序置信度。",
        sources: ["ev_amd_2025_q4", "ev_nvda_fy26_q4"],
        children: [
          {
            id: "q4-3-1",
            level: "level-3",
            title: "Q4.3.1 AMD 进入观察清单的 as-of 证据是什么？",
            conclusion:
              "AMD Data Center 增长、EPYC 需求和 Instinct GPU ramp 说明它有 CPU+GPU 数据中心替代路径，可以进入观察清单。",
            expansion:
              "该叶子支撑 AMD 作为 challenger，而不是纯主题暴露；它的观察价值来自平台替代空间和数据中心财务兑现。",
            gaps:
              "缺少 Instinct 收入规模、客户采用、软件生态和毛利改善的更明确披露。",
            sources: ["ev_amd_2025_q4"]
          },
          {
            id: "q4-3-2",
            level: "level-3",
            title: "Q4.3.2 为什么 AMD 不能仅凭弹性排到最前？",
            conclusion:
              "截至截面日，AMD 的 GPU 软件生态、客户认证、供应链和毛利兑现仍弱于 NVIDIA 平台、HBM 和 ASIC 高分瓶颈，因此需要排序折扣。",
            expansion:
              "该叶子防止把潜在赔率误当成已验证价值捕获：没有足够证据前，challenger 弹性不能覆盖证据质量缺口。",
            gaps:
              "需要更多客户级采用、平台路线、软件生态和毛利率数据来上调置信度。",
            sources: ["ev_amd_2025_q4", "ev_nvda_fy26_q4"]
          }
        ]
      }
    ]
  }
];

function esc(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function pct(value) {
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
}

function sourceChips(ids) {
  return `<div class="source-chips">${ids
    .map((id) => {
      const source = sourceMap.get(id);
      if (!source) return "";
      const label =
        source.bucket === "evidence"
          ? "证据"
          : source.bucket === "research_report"
          ? "研报/数据"
          : source.bucket;
      return `<a class="source-chip" href="#src-${esc(source.id)}"><span>${esc(label)}</span>${esc(
        source.title
      )}</a>`;
    })
    .join("")}</div>`;
}

function renderScoreSchema() {
  return `<div class="artifact-card"><div class="artifact-head"><span>Chokepoint 评分公式</span><strong>100 分</strong></div><div class="table-wrap"><table><thead><tr><th>维度</th><th>权重</th><th>定义</th></tr></thead><tbody>${scoreSchema
    .map(
      ([name, weight, definition]) =>
        `<tr><td>${esc(name)}</td><td><strong>${weight}</strong></td><td>${esc(definition)}</td></tr>`
    )
    .join("")}</tbody></table></div><p>市场定价维度分数越高，代表截至 2026-02-28 越没有被充分反映；缺证据时保守计分。</p></div>`;
}

function renderChokepoints() {
  return `${renderScoreSchema()}<div class="artifact-card"><div class="artifact-head"><span>瓶颈评分卡</span><strong>冻结于 ${asOfDate}</strong></div><div class="table-wrap"><table><thead><tr><th>瓶颈节点</th><th>分数</th><th>核心驱动</th><th>评分拆解</th><th>降级触发器</th></tr></thead><tbody>${chokepoints
    .map(
      (c) =>
        `<tr><td><strong>${esc(c.node)}</strong><p>${sourceChips(c.sources)}</p></td><td><b>${c.score}</b><span>${esc(
          c.grade
        )}</span></td><td>${esc(c.drivers)}</td><td>${esc(c.breakdown)}</td><td>${esc(c.risks)}</td></tr>`
    )
    .join("")}</tbody></table></div></div>`;
}

function renderRiskMatrix() {
  const rows = [
    ["需求/ROI", "云厂商 capex 上修但云收入、AI 产品收入或 FCF 不改善", "NVDA/AMD/MRVL/AVGO 估值先收缩"],
    ["供给释放", "HBM/DRAM 价格回落或设备交付快速改善", "MU/LRCX/AMAT 弹性下调"],
    ["订单周期", "ASML bookings、KLA/Lam/AMAT 指引低于 WFE 增速", "设备链从瓶颈改为周期股"],
    ["政策/出口", "China compute 或设备出口限制扩大", "NVDA/ASML/LRCX/AMAT/KLAC 风险上升"],
    ["客户集中", "ASIC 大客户延期、议价或自研替代", "AVGO/MRVL 赔率下调"]
  ];
  return `<div class="artifact-card"><div class="artifact-head"><span>反证触发矩阵</span><strong>Q3</strong></div><div class="table-wrap"><table><thead><tr><th>风险</th><th>触发器</th><th>影响</th></tr></thead><tbody>${rows
    .map((r) => `<tr><td><strong>${esc(r[0])}</strong></td><td>${esc(r[1])}</td><td>${esc(r[2])}</td></tr>`)
    .join("")}</tbody></table></div></div>`;
}

function targetTable() {
  return `<div class="table-wrap"><table class="target-table"><thead><tr><th>冻结排名</th><th>标的</th><th>瓶颈/节点</th><th>冻结评分</th><th>As-of 推荐逻辑</th><th>赔率模型</th><th>降级触发</th><th>标签起点 ${asOfPriceDate}</th><th>标签终点 ${evaluationPriceDate}</th><th>股价变化标签</th><th>相对 SMH</th></tr></thead><tbody>${targets
    .map((t) => {
      const excess = t.forwardReturn - benchmark.forwardReturn;
      return `<tr><td><strong>#${t.rank}</strong></td><td><strong>${esc(t.ticker)}</strong><p>${esc(
        t.name
      )}</p></td><td>${esc(t.targetClass)}</td><td><b>${t.frozenScore}</b><span>${esc(
        t.winProbability
      )} / ${esc(t.payoffOdds)}</span><p>${esc(t.scoreBreakdown)}</p></td><td>${esc(t.thesis)}${sourceChips(
        t.sources
      )}</td><td>${esc(t.oddsModel)}</td><td>${esc(t.downgrade)}</td><td>${t.asOfPrice.toFixed(
        2
      )}</td><td>${t.evalPrice.toFixed(2)}</td><td><strong>${pct(t.forwardReturn)}</strong><p>close-only</p></td><td>${pct(
        excess
      )}</td></tr>`;
    })
    .join("")}</tbody></table></div>`;
}

function excludedTable() {
  return `<div class="artifact-card"><div class="artifact-head"><span>未纳入高优先推荐但用于校准的后验样本</span><strong>不反向改写</strong></div><div class="table-wrap"><table><thead><tr><th>标的</th><th>2/27</th><th>5/28</th><th>标签</th><th>为什么未提高冻结排名</th></tr></thead><tbody>${excludedWatchlist
    .map(
      (x) =>
        `<tr><td><strong>${esc(x.ticker)}</strong><p>${esc(x.name)}</p></td><td>${x.asOfPrice.toFixed(
          2
        )}</td><td>${x.evalPrice.toFixed(2)}</td><td><strong>${pct(
          x.forwardReturn
        )}</strong></td><td>${esc(x.reason)}</td></tr>`
    )
    .join("")}</tbody></table></div></div>`;
}

function renderNode(node) {
  const children = (node.children || []).map(renderNode).join("");
  const artifact =
    node.artifact === "chokepoint"
      ? renderChokepoints()
      : node.artifact === "risk"
      ? renderRiskMatrix()
      : node.artifact === "targets"
      ? `<div class="artifact-card"><div class="artifact-head"><span>Q4 冻结目标表</span><strong>仅展示 as-of 逻辑</strong></div>${targetTable()}</div>`
      : "";
  return `<details class="qa-card ${node.level}" id="${esc(node.id)}" open><summary><h3>${esc(
    node.title
  )}</h3><span class="qa-count">${(node.children || []).length} 子节点</span><span class="chevron">›</span></summary><div class="qa-body"><div class="qa-block"><div class="block-title">1. 当前结论呈现</div><p>${esc(
    node.conclusion
  )}</p>${artifact}${sourceChips(node.sources || [])}</div><div class="qa-block"><div class="block-title">2. 问题展开（子 QA）</div><p>${esc(
    node.expansion
  )}</p>${children}</div><div class="qa-block"><div class="block-title">3. 待补充的问题</div><p>${esc(
    node.gaps
  )}</p></div></div></details>`;
}

function sourceIndex() {
  return `<details class="source-collapse"><summary><h3>来源索引</h3><span class="source-total">${sources.length} sources</span><span class="chevron">›</span></summary><div class="source-grid">${sources
    .map(
      (s) =>
        `<div class="source-card" id="src-${esc(s.id)}"><div class="source-meta"><span>${esc(
          s.bucket
        )}</span><span>${esc(s.stance)}</span><span>visible ${esc(
          s.visibleAt
        )}</span><span>${s.visibleAt <= asOfDate ? "cutoff-ok" : "price-only"}</span></div><h4><a href="${esc(
          s.url
        )}" target="_blank" rel="noopener">${esc(s.title)}</a></h4><p>${esc(
          s.note
        )}</p><code>${esc(s.url)}</code></div>`
    )
    .join("")}</div></details>`;
}

const css = `:root{--bg:#f5f7fa;--surface:#fff;--surface2:#fbfcff;--text:#354153;--heading:#243142;--muted:#758195;--line:#dde5ef;--blue:#1f6fd1;--blueSoft:#edf5ff;--accent:#5f7fa5;--green:#2f7d65;--amber:#9a6d24;--red:#a54848;--shadow:0 22px 70px rgba(45,63,86,.08);--soft:0 10px 30px rgba(45,63,86,.055)}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:linear-gradient(180deg,#fbfcfe 0,#f5f7fa 280px,#eef3f8 100%);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue","Microsoft YaHei",Arial,sans-serif;line-height:1.68;font-size:15px}a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}.page{max-width:1280px;margin:0 auto;padding:34px 24px 76px}.hero{padding:34px 0 26px;border-bottom:1px solid rgba(96,116,140,.16)}.eyebrow{margin:0 0 10px;color:#7a8492;font-size:12px;font-weight:760;letter-spacing:.08em;text-transform:uppercase}.hero h1{margin:0;font-size:42px;line-height:1.08;font-weight:780;color:var(--heading);letter-spacing:0}.subtitle{max-width:970px;margin:18px 0 0;color:#536274;font-size:18px;line-height:1.65}.top-nav{position:sticky;top:0;z-index:10;display:flex;gap:8px;flex-wrap:wrap;margin:18px -8px 30px;padding:11px 8px;background:rgba(245,247,250,.9);backdrop-filter:blur(18px);border-bottom:1px solid rgba(96,116,140,.14)}.top-nav a{padding:8px 13px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.86);color:#43536a;font-size:13px;font-weight:700}.section{margin:34px 0}.section>h2{font-size:32px;line-height:1.15;margin:0 0 18px;color:var(--heading)}.goal-card,.target-section,.source-collapse{background:linear-gradient(180deg,#fff 0,#fbfcfe 100%);border:1px solid var(--line);border-radius:24px;box-shadow:var(--shadow);padding:28px}.goal-card h2{margin:0 0 12px;font-size:26px;line-height:1.25;color:var(--heading)}.goal-card p{margin:0;color:#46576a}.goal-grid{display:grid;grid-template-columns:1.2fr repeat(4,1fr);gap:12px;margin-top:22px}.metric{background:var(--surface2);border:1px solid #e5ebf3;border-radius:16px;padding:16px}.metric span{display:block;color:#788497;font-size:12px;font-weight:760}.metric strong{display:block;margin-top:6px;font-size:22px;line-height:1.1;color:#34465d}.metric small{display:block;margin-top:6px;color:#7d8796;font-size:12px}.qa-card{position:relative;background:var(--surface);border:1px solid var(--line);border-radius:20px;margin:15px 0;box-shadow:var(--soft);overflow:hidden}.qa-card:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:#d4deea}.qa-card.level-1{border-color:#c9d6e4;box-shadow:var(--shadow)}.qa-card.level-1:before{background:var(--accent)}.qa-card.level-2{margin-left:22px}.qa-card.level-2:before{background:#2f74c8}.qa-card.level-3{margin-left:44px;background:#fbfdff;border-color:#e6edf5}.qa-card.level-3:before{background:#79a3cf}.qa-card.level-3 h3{font-size:17px}.qa-card>summary{list-style:none;display:grid;grid-template-columns:1fr auto auto;gap:12px;align-items:center;cursor:pointer;padding:18px 20px 18px 22px}.qa-card>summary::-webkit-details-marker{display:none}.qa-card h3{margin:0;color:var(--heading);line-height:1.35;font-size:20px;font-weight:760}.qa-count{color:#66758a;font-size:12px;white-space:nowrap;background:#f5f8fb;border:1px solid #e2e8f1;border-radius:999px;padding:5px 9px}.chevron{display:inline-block;font-size:24px;color:#8793a2;transition:transform .18s}.qa-card[open]>summary .chevron,.source-collapse[open]>summary .chevron{transform:rotate(90deg)}.qa-body{border-top:1px solid var(--line);padding:0 22px 22px;background:linear-gradient(180deg,rgba(248,250,253,.78),rgba(255,255,255,.98))}.qa-block{padding:18px 0;border-bottom:1px solid #edf1f6}.qa-block:last-child{border-bottom:none}.block-title{margin-bottom:11px;font-size:13px;font-weight:820;color:#48617c;background:#eef4fa;border:1px solid #dbe6f2;border-radius:999px;display:inline-flex;padding:5px 11px}.qa-block p{margin:0;color:#405066;line-height:1.72}.source-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}.source-chip,.more-chip{display:inline-flex;align-items:center;gap:6px;padding:7px 10px;border-radius:999px;background:#f4f8ff;border:1px solid #dce8fb;font-size:12px;font-weight:680}.source-chip span{color:#63738b}.artifact-card{margin-top:16px;border:1px solid #dce6f0;background:#fff;border-radius:18px;padding:16px;box-shadow:0 8px 24px rgba(45,63,86,.045)}.artifact-head{display:flex;justify-content:space-between;gap:12px;margin-bottom:10px}.artifact-head span{font-weight:820;color:#3e5875}.artifact-head strong{background:#eef5ff;color:#315f91;border:1px solid #c8d8ef;border-radius:999px;padding:4px 9px;font-size:12px}.table-wrap{overflow:auto;border:1px solid #e2e8f1;border-radius:15px;background:#fff}table{width:100%;border-collapse:separate;border-spacing:0;min-width:1180px}th,td{padding:12px 13px;border-bottom:1px solid #edf1f6;text-align:left;vertical-align:top;font-size:13px;line-height:1.55;color:#405066}th{position:sticky;top:0;background:#f7f9fc;color:#596578;font-weight:780;z-index:1}tbody tr:nth-child(even) td{background:#fcfdff}td p{margin:4px 0 0!important;color:#7a8492!important;font-size:12px}td span,td small{color:#7a8492;font-size:12px}td b{display:block;font-size:20px;color:#315f91}.target-section{padding:26px}.target-section>h2{font-size:34px}.target-summary{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px}.target-summary>div{border:1px solid #e2e8f1;border-radius:16px;background:#fbfcfe;padding:15px}.target-summary strong{font-size:14px;color:#38495f}.target-summary p{margin:7px 0 0;color:#526071}.target-table td:nth-child(10) strong{color:var(--green);font-size:16px}.source-collapse{padding:0;overflow:hidden}.source-collapse>summary{list-style:none;display:flex;align-items:center;gap:12px;cursor:pointer;padding:18px 20px}.source-collapse>summary::-webkit-details-marker{display:none}.source-collapse h3{margin:0;font-size:20px;color:var(--heading)}.source-total{margin-left:auto;color:#7b8490;font-size:13px;background:#f4f7fb;border:1px solid #e2e8f1;border-radius:999px;padding:5px 9px}.source-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;border-top:1px solid var(--line);padding:18px;background:#fbfcfe}.source-card{border:1px solid #e2e8f1;border-radius:16px;padding:14px;background:#fff}.source-meta{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}.source-meta span{font-size:11px;color:#63738b;background:#eef3f9;border-radius:999px;padding:3px 7px}.source-card h4{margin:0 0 8px;font-size:15px;line-height:1.35;color:var(--heading)}.source-card p{margin:0 0 10px;color:#465365;font-size:13px;line-height:1.58}.source-card code{font-size:11px;color:#7a8492;word-break:break-all}.report-note{margin-top:18px;color:#7b8490;font-size:13px}@media(max-width:900px){.page{padding:26px 14px 54px}.hero h1{font-size:32px}.subtitle{font-size:16px}.goal-grid,.source-grid,.target-summary{grid-template-columns:1fr}.qa-card.level-2,.qa-card.level-3{margin-left:0}.qa-card>summary{grid-template-columns:1fr auto}.qa-count{grid-column:1/-1;justify-self:start}.section>h2,.target-section>h2{font-size:28px}}`;

const html = `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>半导体硬件投资机会研究 - 时间截面回测</title><style>${css}</style></head><body><div class="page"><header class="hero"><p class="eyebrow">Research Goal QA / Historical Training Mode</p><h1>半导体硬件投资机会研究</h1><p class="subtitle">本报告以 2026-02-28 为资料截止日，完整重做半导体硬件方向投资机会研究。所有研究判断只使用截止日前可见材料；后续评估字段仅在最终表格右侧隔离展示。</p></header><nav class="top-nav"><a href="#goal">当前研究目标</a><a href="#qa">问题下钻</a><a href="#targets">最终标的推荐</a><a href="#sources">来源索引</a></nav><section class="section" id="goal"><div class="goal-card"><p class="eyebrow">1 / 当前研究目标</p><h2>截至 2026-02-28，半导体硬件链条中哪些节点具备更强预测性投资机会？</h2><p>约束判断：需求真实，但机会应从泛半导体收敛到 HBM/高端存储、custom ASIC/Ethernet、先进制程/封装和工艺设备。本节和 QA 树只呈现当时可见证据形成的判断。</p><div class="goal-grid"><div class="metric"><span>运行模式</span><strong>历史训练</strong><small>严格避免未来函数。</small></div><div class="metric"><span>资料截止</span><strong>${asOfDate}</strong><small>仅采用此前可见材料。</small></div><div class="metric"><span>排序状态</span><strong>已冻结</strong><small>后续价格不参与排序。</small></div><div class="metric"><span>证据门槛</span><strong>cutoff-ok</strong><small>来源需通过可见日检查。</small></div><div class="metric"><span>评估字段</span><strong>最终表格</strong><small>不进入研究判断。</small></div></div></div></section><section class="section" id="qa"><p class="eyebrow">2 / 问题下钻</p><h2>按 QA 树展开研究结论</h2>${qaNodes
  .map(renderNode)
  .join("")}</section><section class="section target-section" id="targets"><p class="eyebrow">3 / 最终标的推荐</p><h2>冻结观察清单</h2><div class="target-summary"><div><strong>冻结排序逻辑</strong><p>先按 Q2 瓶颈强度，再按未来空间、赔率、证据质量、反证可控性和可监控性排序。排序在后续价格数据加入前完成。</p></div><div><strong>评估字段隔离</strong><p>后续评估字段只在表格右侧展示，不进入 As-of 推荐逻辑、评分、赔率模型或降级触发。</p></div></div>${targetTable()}</section><section class="section" id="sources"><p class="eyebrow">4 / 来源索引</p>${sourceIndex()}</section><p class="report-note">生成时间：${generatedAt}。后续价格数据仅作为隔离评估字段；本报告不构成买卖、仓位或目标价指令。</p></div></body></html>`;

const md = `# 半导体硬件投资机会研究 - 时间截面回测

运行模式：历史训练/回测。资料截止日：${asOfDate}。公开结论只使用截止日前可见材料。

## 当前研究目标

截至 ${asOfDate}，半导体硬件链条中哪些节点具备更强预测性投资机会？本报告只使用截止日前公开可见材料形成判断；后续评估字段只在最终表格右侧展示。

## 问题下钻摘要

- Q1：需求真实，但集中在 AI data center 相关 logic、memory、advanced packaging 和网络，不是泛半导体同步上行。
- Q2：最高分瓶颈是 HBM/高端存储，其次是 custom ASIC/Ethernet、先进制程/封装、工艺设备/过程控制、GPU 平台。
- Q3：主要反证来自 AI capex ROI、HBM 供给释放、WFE 订单下修、出口限制和客户集中。
- Q4：冻结排序优先 MU、AVGO、NVDA、MRVL、TSM、KLAC、LRCX、AMD、ASML、AMAT。
  - Q4.1：高纯度瓶颈承接优先落在 MU、AVGO、MRVL 和 NVDA。
  - Q4.2：制造与设备确定性主要落在 TSM、KLAC、LRCX、ASML、AMAT。
  - Q4.3：AMD 属于替代路径或高赔率观察，但排序仍受软件生态、客户认证和毛利兑现约束。

## 最终标的推荐

| 排名 | 标的 | 冻结评分 | ${asOfPriceDate} 收盘 | ${evaluationPriceDate} 收盘 | 股价变化标签 | 相对 SMH |
|---|---:|---:|---:|---:|---:|---:|
${targets
  .map(
    (t) =>
      `| ${t.rank} | ${t.ticker} | ${t.frozenScore} | ${t.asOfPrice.toFixed(2)} | ${t.evalPrice.toFixed(2)} | ${pct(t.forwardReturn)} | ${pct(t.forwardReturn - benchmark.forwardReturn)} |`
  )
  .join("\n")}

## 来源索引

${sources.map((s) => `- ${s.id}: ${s.title} (${s.visibleAt}) ${s.url}`).join("\n")}
`;

const project = {
  project_id: "semiconductor_hardware_timeslice_20260228",
  object_type: "industry_theme",
  object_id: "semiconductor_hardware",
  framework: "research_goal_qa",
  run_mode: "historical_training_backtest",
  as_of_date: asOfDate,
  evaluation_date: evaluationDate,
  boundary: "研究观察清单，不构成买卖建议。"
};

const questionPlan = {
  generated_at: generatedAt,
  planning_mode: "research_goal_qa_timeslice",
  run_mode: "historical_training_backtest",
  as_of_date: asOfDate,
  evaluation_date: evaluationDate,
  no_lookahead_rule:
    "All thesis evidence must have visibleAt <= as_of_date. Price labels are attached only after target ranking is frozen.",
  l1: qaNodes.map((n) => ({
    id: n.id,
    question: n.title,
    source_plan: (n.sources || []).map((id) => ({
      source_id: id,
      visible_at: sourceMap.get(id)?.visibleAt,
      cutoff_status: sourceMap.get(id)?.visibleAt <= asOfDate ? "accepted" : "label_only"
    })),
    children: (n.children || []).map((c) => ({
      id: c.id,
      question: c.title,
      source_plan: (c.sources || []).map((id) => ({
        source_id: id,
        visible_at: sourceMap.get(id)?.visibleAt,
        cutoff_status: sourceMap.get(id)?.visibleAt <= asOfDate ? "accepted" : "label_only"
      }))
    }))
  }))
};

const qaTree = {
  root: {
    id: "goal",
    question: "截至 2026-02-28，半导体硬件链条中哪些节点具备更强预测性投资机会？",
    run_mode: "historical_training_backtest",
    as_of_date: asOfDate,
    evaluation_date: evaluationDate
  },
  nodes: qaNodes
};

const workbench = {
  generated_at: generatedAt,
  run_mode: "historical_training_backtest",
  as_of_date: asOfDate,
  as_of_price_date: asOfPriceDate,
  evaluation_date: evaluationDate,
  evaluation_price_date: evaluationPriceDate,
  no_lookahead_controls: [
    "Accepted thesis sources require visibleAt <= 2026-02-28.",
    "Post-cutoff price labels use Nasdaq close data only after Q4 target ranking is frozen.",
    "No Q1 2026 company results published after 2026-02-28 were used in thesis formation.",
    "DeepSeek was used only for source-extraction drafts from supplied excerpts; GPT verified against source links and wrote the final synthesis."
  ],
  rejected_or_quarantined_examples: [
    "Company Q1 2026 results published after 2026-02-28.",
    "March-May 2026 news about follow-on orders, partnerships, analyst upgrades, or capex revisions.",
    "Post-cutoff price action except Nasdaq label rows."
  ],
  benchmark,
  score_schema: scoreSchema.map(([dimension, weight, definition]) => ({
    dimension,
    weight,
    definition
  })),
  chokepoints,
  targets,
  excluded_watchlist_for_calibration: excludedWatchlist,
  price_labels: priceLabels,
  sources
};

function writeJsonl(file, rows) {
  fs.writeFileSync(path.join(base, file), rows.map((row) => JSON.stringify(row)).join("\n") + "\n", "utf8");
}

fs.mkdirSync(base, { recursive: true });
fs.writeFileSync(path.join(base, "project.json"), JSON.stringify(project, null, 2), "utf8");
fs.writeFileSync(path.join(base, "question_plan.json"), JSON.stringify(questionPlan, null, 2), "utf8");
fs.writeFileSync(path.join(base, "qa_tree.json"), JSON.stringify(qaTree, null, 2), "utf8");
fs.writeFileSync(path.join(base, "investment_workbench.json"), JSON.stringify(workbench, null, 2), "utf8");
writeJsonl(
  "evidence.jsonl",
  sources.map((s) => ({
    id: s.id,
    title: s.title,
    information_category: s.bucket,
    support_refute_or_lead: s.stance,
    source_visible_at: s.visibleAt,
    cutoff_status: s.visibleAt <= asOfDate ? "accepted" : "label_only",
    url: s.url,
    summary: s.note
  }))
);
fs.writeFileSync(path.join(base, "professional_report.md"), md, "utf8");
fs.writeFileSync(path.join(base, "professional_report.html"), html, "utf8");

console.log(`Wrote ${base}`);
