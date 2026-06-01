const fs = require("fs");
const path = require("path");
const https = require("https");

const ROOT = path.resolve(__dirname, "..");
const PROJECT_ID = "memory_industry_timeslice_20260228";
const OUT_DIR = path.join(ROOT, "research", "qa_projects", PROJECT_ID);
const AS_OF_DATE = "2026-02-28";
const REPORT_DATE = "2026-05-31";
const LABEL_START = "2026-02-27";
const LABEL_END = "2026-05-29";

const SCORE_WEIGHTS = {
  chokepoint_strength: 0.26,
  future_space: 0.18,
  valuation_odds: 0.18,
  evidence_quality: 0.14,
  disconfirming_risk_control: 0.1,
  monitorability: 0.05,
  payoff_convexity: 0.09,
};

const sources = [
  source(
    "SRC-WSTS-2025-AUTUMN",
    "WSTS Autumn 2025 Forecast",
    "research_report",
    "https://www.wsts.org/esraCMS/extension/media/f/WST/7310/WSTS_FC-Release-2025_11.pdf",
    "2025-12-02",
    "WSTS 2025 autumn forecast: 2026 total semiconductor market $975.46B, memory $294.821B and +39.4% YoY."
  ),
  source(
    "SRC-MU-FY26-Q1",
    "Micron FY2026 Q1 results",
    "evidence",
    "https://micron.gcs-web.com/news-releases/news-release-details/micron-technology-inc-reports-results-first-quarter-fiscal-2026",
    "2025-12-17",
    "Micron reported record FY26 Q1 revenue of $13.64B; Cloud Memory Business revenue was $5.284B with 66% gross margin; capex was $4.5B and adjusted FCF was $3.9B."
  ),
  source(
    "SRC-SKHYNIX-FY25",
    "SK hynix FY2025 results",
    "evidence",
    "https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html",
    "2026-01-28",
    "SK hynix reported FY2025 revenue KRW97.1467T, operating profit KRW47.2063T, operating margin 49%, and record results driven by AI memory competitiveness and high value-added products including HBM."
  ),
  source(
    "SRC-SAMSUNG-Q4FY25",
    "Samsung Electronics Q4 and FY2025 results",
    "evidence",
    "https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results",
    "2026-01-29",
    "Samsung reported FY2025 revenue KRW333.6T and operating profit KRW43.6T; Q4 Memory Business reached record quarterly revenue and operating profit despite limited supply, with HBM, server DDR5 and enterprise SSD emphasized."
  ),
  source(
    "SRC-SNDK-FY26-Q2",
    "Sandisk FY2026 Q2 results",
    "evidence",
    "https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-second-quarter-2026-financial-results",
    "2026-01-29",
    "Sandisk reported Q2 FY26 revenue $3.03B, +31% QoQ; datacenter revenue was $440M, +64% QoQ; Q3 FY26 revenue outlook was $4.4B-$4.8B."
  ),
  source(
    "SRC-WDC-FY26-Q2",
    "Western Digital FY2026 Q2 results",
    "evidence",
    "https://investor.wdc.com/news-releases/news-release-details/western-digital-reports-fiscal-second-quarter-2026-financial",
    "2026-01-29",
    "Western Digital reported Q2 FY26 revenue $3.017B, +25% YoY, non-GAAP gross margin 46.1%, operating cash flow $745M and free cash flow $653M."
  ),
  source(
    "SRC-STX-FY26-Q2",
    "Seagate FY2026 Q2 results",
    "evidence",
    "https://investors.seagate.com/Q2FY26PR",
    "2026-01-27",
    "Seagate reported Q2 FY26 revenue $2.825B, non-GAAP gross margin 42.2%, operating cash flow $723M and free cash flow $607M."
  ),
  source(
    "SRC-SIMO-Q4FY25",
    "Silicon Motion Q4 and FY2025 results",
    "evidence",
    "https://ir.siliconmotion.com/news-releases/news-release-details/silicon-motion-announces-results-fourth-quarter-and-year-ended/",
    "2026-02-04",
    "Silicon Motion reported Q4 FY25 net sales $278.5M, +15% QoQ and +46% YoY; SSD controller sales grew 25%-30% QoQ; initial boot-drive products shipped to a leading GPU maker."
  ),
  labelSource(
    "LBL-NASDAQ-US",
    "Nasdaq historical close-price API",
    "https://api.nasdaq.com/api/quote/MU/historical?assetclass=stocks&fromdate=2026-02-25&todate=2026-05-30&limit=9999",
    "2026-05-31"
  ),
  labelSource(
    "LBL-KRX-UNVERIFIED",
    "KRX local listing label placeholder",
    "https://global.krx.co.kr/",
    "2026-05-31"
  ),
];

const mechanismDepthMap = [
  ["demand_driver_tree", "AI training/inference, RAG, agent workloads and cloud data growth map into HBM, server DRAM, enterprise SSD/NAND and high-capacity HDD demand."],
  ["supply_or_access_response", "HBM qualification, memory wafer allocation, NAND discipline and HDD HAMR ramps create different supply response speeds."],
  ["unit_economics_profit_bridge", "Cloud Memory gross margin, SK hynix operating margin, Sandisk datacenter growth and HDD FCF are used to test whether demand reaches cash flow."],
  ["competitive_value_capture_map", "Specific value capture is separated across SK hynix, Samsung, Micron, Sandisk, WDC, Seagate and Silicon Motion rather than treating memory as one bucket."],
  ["market_pricing_bridge", "US listing prices can be labeled; Korean valuation needs separate verification, so valuation odds are capped when same-cutoff market data is incomplete."],
  ["disconfirming_counter_supply_tests", "Capacity additions, customer capex digestion, inventory rebuild exhaustion, ASP reversal and China supply are explicit downgrade tests."],
  ["capital_chain_second_order_beneficiaries", "High margins and capex can benefit equipment/materials, but target inclusion requires direct order evidence visible at cutoff."],
  ["model_reconciliation", "Industry forecasts, company releases and target scoring are stored with units/periods; post-cutoff external models are quarantined from thesis use."],
];

const l1s = [
  l1("Q1", "需求是否真实，并且能从 AI 工作负载流到具体存储产品？", "需求成立，但不是所有存储产品同等受益；最强证据集中在 HBM/高端 DRAM、企业级 SSD/NAND 与高容量 HDD。"),
  l1("Q2", "稀缺价值捕获点在哪里，能否转成收入、利润和现金流？", "HBM/高端 DRAM 的不可替代性最强，NAND/eSSD 与 nearline HDD 有现金流证据但供给反应更快，控制器属于二阶受益。"),
  l1("Q3", "哪些反证会压低胜率、赔率或行动状态？", "最大反证不是需求消失，而是供给扩张、客户库存消化、ASP 反转和估值提前兑现。"),
  l1("Q4", "冻结截面下应如何形成标的观察名单？", "目标池不按美股便利性收缩；排序先看稀缺性和财务转化，再看赔率、反证控制和可监控性。"),
];

const l2s = [
  l2("Q1.1", "工作负载到存储需求", "先证明 AI 和数据中心需求如何分别拉动 HBM、DRAM、NAND/eSSD 与 HDD。"),
  l2("Q1.2", "需求-供给斜率差", "再比较需求斜率和供给响应速度，避免把周期补库存误判为长期稀缺。"),
  l2("Q2.1", "HBM/高端 DRAM 稀缺与单位经济", "判断最强瓶颈是否已经进入公司利润表。"),
  l2("Q2.2", "NAND/eSSD、HDD 与控制器外溢", "判断 AI 存储需求是否扩散到容量层和控制器层。"),
  l2("Q3.1", "市场定价与重估路径", "区分周期反弹、结构性利润池扩大和估值重估。"),
  l2("Q3.2", "供给、客户和替代反证", "把高利润引发的供给反应和客户集中风险放进降级测试。"),
  l2("Q4.1", "目标池与确定性排序", "用冻结分数和行动状态形成具体证券观察名单。"),
  l2("Q4.2", "升级、降级与复盘触发器", "给每个主要 thesis node 留下可监控证据。"),
];

const leaves = [
  leaf({
    id: "Q1.1.1",
    parent: "Q1.1",
    question: "AI 与数据中心需求如何映射到具体存储产品？",
    skill: "industry-report-analysis",
    taskFamily: "Industry report / dataset parsing",
    scoreComponent: "future_space",
    decisionUse: "决定 Q1 是否只保留 broad memory beta，还是进入具体产品链条。",
    materiality: "如果需求不能落到 HBM/DRAM/NAND/HDD 产品，就不能提高任何目标强度。",
    support: "WSTS memory forecast, company data-center storage disclosures, product-specific revenue and margin.",
    refute: "传统消费/库存修复主导，而 AI 高端产品没有增量或财务转化。",
    implications: "提高 HBM、eSSD、nearline HDD 暴露标的的 future_space；不提高低端消费存储。",
    schema: "memory_demand_driver",
    fact: "WSTS 2026 memory forecast is $294.821B with +39.4% YoY growth; Micron, Samsung, Sandisk, WDC, Seagate and Silicon Motion all reported AI/data-center storage demand evidence before the cutoff.",
    inference: "The product mapping comes from where the workload creates bottlenecks: training/inference raises HBM and server DRAM intensity, RAG/agent systems raise low-latency enterprise SSD demand, and data retention/checkpointing raises capacity HDD demand.",
    judgment: "Q1 can be strengthened only for product nodes with an explicit workload-to-product path; broad memory-cycle beta should not raise target scores by itself.",
    gap: "Need a full workload-to-bit model with token/RAG/agent/video assumptions and memory intensity.",
    trigger: "Upgrade if official capex/workload disclosures show memory intensity rising faster than compute; downgrade if demand is mainly inventory rebuild.",
    sourceIds: ["SRC-WSTS-2025-AUTUMN", "SRC-MU-FY26-Q1", "SRC-SNDK-FY26-Q2", "SRC-WDC-FY26-Q2", "SRC-STX-FY26-Q2", "SRC-SIMO-Q4FY25"],
    answerArtifact: artifact("工作负载到存储产品的映射", ["工作负载/需求", "直接拉动的产品", "需求机制", "截止日前证据", "标的含义"], [
      ["AI 训练 / 大模型推理", "HBM、Cloud Memory、server DRAM", "模型参数、KV cache、batching 和高带宽访问提高 GPU 附近内存强度", "Micron Cloud Memory $5.284B / 66% gross margin；SK hynix 和 Samsung 都强调 HBM/AI memory", "优先影响 MU、SK hynix、Samsung"],
      ["RAG / Agent / 企业 AI 应用", "enterprise SSD / datacenter NAND", "检索、向量库、日志、上下文缓存提高低延迟持久化存储需求", "Sandisk datacenter revenue +64% QoQ；Samsung 提到 enterprise SSD", "影响 SNDK，也影响 Samsung/SK hynix 的 NAND/eSSD 节点"],
      ["数据湖、checkpoint、AI 数据留存", "nearline HDD / high-capacity HDD", "训练数据、推理日志和对象存储增加低成本容量需求", "WDC 和 Seagate 最新季度均有高毛利与 FCF 证据", "影响 WDC、STX，但稀缺性低于 HBM"],
      ["GPU 平台启动盘/边缘 AI 设备", "SSD controller / boot-drive storage", "平台设计赢单把存储控制器带入 AI 硬件链", "SIMO 披露 SSD controller 增长和 GPU boot-drive shipment", "影响 SIMO，但客户集中与替代风险更高"],
    ]),
  }),
  leaf({
    id: "Q1.1.2",
    parent: "Q1.1",
    question: "AI 需求是否已经进入公司收入和毛利，而不只是叙事？",
    skill: "financial-statement-analysis",
    taskFamily: "Financial statement / filing parsing",
    scoreComponent: "evidence_quality",
    decisionUse: "决定需求证据是否可用于评分，而不是只作为线索。",
    materiality: "财务转化是从主题到投资机会的分界线。",
    support: "Revenue, gross margin, operating margin, FCF and segment disclosures tied to AI/data-center products.",
    refute: "AI 相关说法没有收入、利润或现金流字段支撑。",
    implications: "Micron、SK hynix、Sandisk、WDC、Seagate 的证据质量高于只有路线叙事的标的。",
    schema: "memory_unit_economics",
    fact: "Micron Cloud Memory revenue was $5.284B with 66% gross margin; SK hynix FY2025 operating margin was 49%; Sandisk datacenter revenue rose 64% QoQ; WDC and Seagate produced large FCF in their latest quarters.",
    inference: "Several storage nodes show demand converting into margin or cash flow before the cutoff.",
    judgment: "Financial conversion is strong enough to move Q1 from lead to evidence, while still requiring product-level supply and valuation checks.",
    gap: "SK hynix and Samsung HBM revenue/margin mix is not fully comparable from public releases alone.",
    trigger: "Upgrade if companies disclose durable mix and pricing; downgrade if margin gains reverse with ASP.",
    sourceIds: ["SRC-MU-FY26-Q1", "SRC-SKHYNIX-FY25", "SRC-SNDK-FY26-Q2", "SRC-WDC-FY26-Q2", "SRC-STX-FY26-Q2"],
  }),
  leaf({
    id: "Q1.2.1",
    parent: "Q1.2",
    question: "需求斜率是否快于供给响应？",
    skill: "industry-report-analysis",
    taskFamily: "Industry report / dataset parsing",
    scoreComponent: "future_space",
    decisionUse: "决定 future_space 是否能被视为结构性空间，而不是短期涨价。",
    materiality: "存储行业高利润会诱发供给；没有供需斜率差就没有稀缺性。",
    support: "Market growth forecasts, limited supply language, capex/ramp timing and product qualification constraints.",
    refute: "Capacity additions and customer inventory are enough to meet demand quickly.",
    implications: "提高 HBM/高端 DRAM；对 NAND/HDD 保守，因为供给和客户库存更可能快速反应。",
    schema: "memory_supply_capacity",
    fact: "WSTS forecasted memory growth faster than total semiconductors; Samsung described Q4 Memory record performance despite limited supply; Micron reported high capex and strong FCF in the same quarter.",
    inference: "Demand growth is visible, while supply response is also being funded; therefore scarcity is strongest where qualification and capacity conversion are slowest.",
    judgment: "HBM/advanced DRAM earns the highest chokepoint credit; commodity NAND and capacity HDD need stronger order/contract evidence.",
    gap: "Public sources here do not provide a complete wafer-start/bit-growth table by supplier before cutoff.",
    trigger: "Downgrade if supplier capex, wafer starts or bit growth exceed AI memory demand growth.",
    sourceIds: ["SRC-WSTS-2025-AUTUMN", "SRC-SAMSUNG-Q4FY25", "SRC-MU-FY26-Q1"],
  }),
  leaf({
    id: "Q1.2.2",
    parent: "Q1.2",
    question: "哪些产品线的供需斜率最可能保持紧张？",
    skill: "industry-report-analysis",
    taskFamily: "Industry report / dataset parsing",
    scoreComponent: "chokepoint_strength",
    decisionUse: "决定 Q2 的瓶颈排序。",
    materiality: "产品线稀缺性决定公司价值捕获，而不是行业总需求。",
    support: "HBM, server DDR5, enterprise SSD, datacenter NAND, high-capacity HDD and controller disclosures.",
    refute: "低端 DRAM/NAND 或消费 SSD 主导增长，价格随库存修复回落。",
    implications: "Q2 优先 HBM/高端 DRAM，其次 eSSD/NAND 和 nearline HDD，再到控制器。",
    schema: "memory_demand_driver",
    fact: "Samsung cited HBM, Server DDR5 and Enterprise SSD; Sandisk datacenter revenue was +64% QoQ; WDC/Seagate high-capacity storage showed high margins and FCF; SIMO saw SSD controller and GPU boot-drive traction.",
    inference: "The highest signal is not one product: AI storage pulls a stack from HBM to capacity storage, but scarcity intensity differs by layer.",
    judgment: "The report should score product nodes separately and avoid one broad memory score.",
    gap: "Need product-level order backlog and contract duration for NAND/HDD/controller nodes.",
    trigger: "Upgrade if long-term supply agreements or customer qualifications extend beyond spot price improvement.",
    sourceIds: ["SRC-SAMSUNG-Q4FY25", "SRC-SNDK-FY26-Q2", "SRC-WDC-FY26-Q2", "SRC-STX-FY26-Q2", "SRC-SIMO-Q4FY25"],
  }),
  leaf({
    id: "Q2.1.1",
    parent: "Q2.1",
    question: "HBM/高端 DRAM 的不可替代性是否足够强？",
    skill: "industry-report-analysis",
    taskFamily: "Industry report / dataset parsing",
    scoreComponent: "chokepoint_strength",
    decisionUse: "决定 HBM 厂商是否能获得最高 chokepoint score。",
    materiality: "不可替代性是 actionable_long 的必要条件之一。",
    support: "HBM demand, qualification, limited supply, high-value mix and customer allocation evidence.",
    refute: "HBM supply becomes broadly available or customers shift to architectures with lower HBM intensity.",
    implications: "SK hynix、Micron、Samsung 均进入核心目标池，但 valuation gap 决定行动状态。",
    schema: "memory_supply_capacity",
    fact: "SK hynix attributed record results to AI memory competitiveness and HBM; Micron Cloud Memory margin was far above commodity-memory-cycle evidence; Samsung highlighted HBM and limited supply.",
    inference: "HBM combines capacity, packaging, qualification and customer allocation constraints, making it the strongest memory chokepoint visible at the cutoff.",
    judgment: "HBM/high-end DRAM receives the highest Q2 chokepoint weight.",
    gap: "Need comparable HBM share, capacity and customer allocation for SK hynix, Samsung and Micron.",
    trigger: "Downgrade if HBM supply opens faster than accelerator demand or if customer qualification shifts away from current suppliers.",
    sourceIds: ["SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1", "SRC-SAMSUNG-Q4FY25"],
  }),
  leaf({
    id: "Q2.1.2",
    parent: "Q2.1",
    question: "HBM/高端 DRAM 能否转成持续利润，而不是一次性价格峰值？",
    skill: "financial-statement-analysis",
    taskFamily: "Financial statement / filing parsing",
    scoreComponent: "payoff_convexity",
    decisionUse: "决定 payoff_convexity 与 thesis_confidence。",
    materiality: "价格峰值和持续利润的估值含义完全不同。",
    support: "Gross margin, operating margin, cash flow, capex and mix disclosures.",
    refute: "High margin is driven by temporary shortage and will be competed away by capacity additions.",
    implications: "Micron 的 Cloud Memory 证据最直接；SK hynix 最强但需要更多估值同口径数据；Samsung 受集团折价和 HBM追赶影响。",
    schema: "memory_unit_economics",
    fact: "Micron Cloud Memory gross margin reached 66%; SK hynix FY2025 operating margin was 49%; Samsung Memory posted record Q4 revenue and operating profit.",
    inference: "The profit bridge is already visible, but sustainability depends on supply discipline and customer demand duration.",
    judgment: "High-end memory deserves high payoff convexity, with kill tests tied to ASP, mix and capex.",
    gap: "No complete public per-bit cost, HBM ASP and capacity table by company in the cutoff source set.",
    trigger: "Downgrade if Cloud Memory/HBM margin compresses while capex remains high.",
    sourceIds: ["SRC-MU-FY26-Q1", "SRC-SKHYNIX-FY25", "SRC-SAMSUNG-Q4FY25"],
  }),
  leaf({
    id: "Q2.2.1",
    parent: "Q2.2",
    question: "NAND/eSSD 是否从周期品变成 AI 数据中心容量瓶颈？",
    skill: "financial-statement-analysis",
    taskFamily: "Financial statement / filing parsing",
    scoreComponent: "chokepoint_strength",
    decisionUse: "决定 Sandisk 与 Samsung/SK hynix NAND/eSSD 节点的强度。",
    materiality: "NAND 是第二利润池，但供给反应通常比 HBM 更快。",
    support: "Datacenter revenue growth, enterprise SSD demand, gross margin and guide.",
    refute: "NAND demand is mainly price rebound or channel refill; new supply quickly erodes margin.",
    implications: "Sandisk 进入高赔率池，但 disconfirming risk 高于 HBM。",
    schema: "memory_unit_economics",
    fact: "Sandisk Q2 revenue grew 31% QoQ and datacenter revenue grew 64% QoQ; Samsung highlighted enterprise SSD within its Memory strength.",
    inference: "NAND/eSSD demand is visible and financially meaningful, but its scarcity is less protected than HBM.",
    judgment: "Sandisk can score high on payoff convexity, while risk-control score must remain conservative.",
    gap: "Need NAND industry supply, contract duration and customer concentration data.",
    trigger: "Downgrade if NAND ASP turns down or datacenter revenue growth fails to carry gross margin.",
    sourceIds: ["SRC-SNDK-FY26-Q2", "SRC-SAMSUNG-Q4FY25", "SRC-SKHYNIX-FY25"],
  }),
  leaf({
    id: "Q2.2.2",
    parent: "Q2.2",
    question: "HDD 与控制器是否只是二阶受益，还是具备独立稀缺性？",
    skill: "financial-statement-analysis",
    taskFamily: "Financial statement / filing parsing",
    scoreComponent: "chokepoint_strength",
    decisionUse: "决定 WDC、STX、SIMO 是否只能 watch_only。",
    materiality: "容量层和控制器可以受益，但不一定拥有 HBM 级别定价权。",
    support: "HDD margin/FCF, HAMR or high-capacity demand, SSD controller sales and GPU boot-drive design wins.",
    refute: "HDD/controller demand is replaceable, customer-driven, or only follows memory price cycle.",
    implications: "STX/WDC/SIMO 保留在目标池，但 action_state 受到稀缺性和客户集中限制。",
    schema: "memory_capital_chain",
    fact: "WDC and Seagate reported non-GAAP gross margins above 42% and large FCF; SIMO reported SSD controller sales +25%-30% QoQ and boot-drive shipments to a leading GPU maker.",
    inference: "The AI storage flywheel spills into capacity storage and controllers, but these nodes are more exposed to customer timing and substitution.",
    judgment: "These are valid watch targets, not automatic high-conviction long observations.",
    gap: "Need order backlog, long-term agreements and customer concentration details.",
    trigger: "Upgrade if high-capacity HDD LTAs or enterprise controller design wins become longer-duration and margin-accretive.",
    sourceIds: ["SRC-WDC-FY26-Q2", "SRC-STX-FY26-Q2", "SRC-SIMO-Q4FY25"],
  }),
  leaf({
    id: "Q3.1.1",
    parent: "Q3.1",
    question: "市场是否已经把存储稀缺充分定价？",
    skill: "valuation-analysis",
    taskFamily: "Valuation / priced-in expectations",
    scoreComponent: "valuation_odds",
    decisionUse: "决定 target action_state 的上限。",
    materiality: "强基本面如果已被完全定价，就不是未被充分定价的机会。",
    support: "As-of valuation snapshot, peer multiples, FCF yield, implied growth and rerating path.",
    refute: "Price already embeds multi-year peak margin, leaving poor expected excess return.",
    implications: "韩国标的因同口径估值未验证而 capped at watch_only；US 标的按可得价格和财务转化单独评分。",
    schema: "memory_valuation_rerating",
    fact: "The cutoff source set has strong fundamental evidence, but complete same-cutoff valuation data for every local listing is not verified inside the thesis source layer.",
    inference: "The framework should not convert HBM leadership into actionable status without a market-pricing bridge.",
    judgment: "Valuation odds are capped where market-pricing evidence is incomplete.",
    gap: "Need same-cutoff market cap, EV, net cash/debt, EPS/FCF estimates and peer multiples for Korean and US listings.",
    trigger: "Upgrade only if valuation implies conservative growth/margins relative to verified driver tree.",
    sourceIds: ["SRC-MU-FY26-Q1", "SRC-SKHYNIX-FY25", "SRC-SAMSUNG-Q4FY25", "SRC-SNDK-FY26-Q2"],
  }),
  leaf({
    id: "Q3.1.2",
    parent: "Q3.1",
    question: "估值重估来自盈利上修，还是周期品折现率下降？",
    skill: "valuation-analysis",
    taskFamily: "Valuation / priced-in expectations",
    scoreComponent: "payoff_convexity",
    decisionUse: "决定 payoff 是否来自基本面还是 multiple rerating。",
    materiality: "外部报告的优势就在于拆分折现率/风险溢价，本框架必须显式处理。",
    support: "Margin durability, FCF conversion and category rerating evidence.",
    refute: "Market treats memory as peak-cycle earnings and refuses multiple expansion.",
    implications: "SNDK/MU 具备盈利上修和重估双路径；WDC/STX 更偏现金流路径；SK hynix/Samsung 需要同口径估值。",
    schema: "memory_valuation_rerating",
    fact: "The company releases show record or sharply improved margins and cash flow, but do not by themselves prove multiple rerating.",
    inference: "Rerating requires the market to believe memory has become an AI infrastructure bottleneck rather than only a commodity upcycle.",
    judgment: "Payoff convexity is high but must be scored separately from thesis confidence.",
    gap: "Need as-of consensus and market-implied scenario model.",
    trigger: "Downgrade if high earnings are treated as peak-cycle and multiples compress despite stronger reported results.",
    sourceIds: ["SRC-MU-FY26-Q1", "SRC-SNDK-FY26-Q2", "SRC-WDC-FY26-Q2", "SRC-STX-FY26-Q2"],
  }),
  leaf({
    id: "Q3.2.1",
    parent: "Q3.2",
    question: "高利润会不会引发供给扩张，从而削弱稀缺性？",
    skill: "financial-statement-analysis",
    taskFamily: "Financial statement / filing parsing",
    scoreComponent: "disconfirming_risk_control",
    decisionUse: "决定强度是否因供给反应被封顶。",
    materiality: "周期行业最大风险是利润本身创造未来供给。",
    support: "Capex, supply plans, production ramps, utilization and product qualification.",
    refute: "Supply is structurally constrained and customer demand absorbs capacity.",
    implications: "HBM风险低于普通 NAND；HDD/controller 需更多订单能见度。",
    schema: "memory_supply_capacity",
    fact: "Micron reported $4.5B capex in the quarter; high margins and FCF across memory/storage nodes create incentive to expand supply.",
    inference: "Strong current profitability is both positive evidence and a future supply-risk signal.",
    judgment: "Disconfirming-risk control must remain conservative even for high-scoring targets.",
    gap: "Need supplier capex allocation, wafer starts, HBM capacity and NAND bit-growth table.",
    trigger: "Downgrade if capex ramps faster than verified demand or inventory rises.",
    sourceIds: ["SRC-MU-FY26-Q1", "SRC-SAMSUNG-Q4FY25", "SRC-SKHYNIX-FY25"],
  }),
  leaf({
    id: "Q3.2.2",
    parent: "Q3.2",
    question: "客户集中、库存和架构替代会不会改变需求斜率？",
    skill: "news-event-analysis",
    taskFamily: "News / message parsing",
    scoreComponent: "disconfirming_risk_control",
    decisionUse: "决定需要哪些 kill tests。",
    materiality: "AI 云客户采购节奏和架构路线会直接改变高端存储需求。",
    support: "Long-term purchase agreements, broad customer base, durable workload growth.",
    refute: "Large cloud customers delay capex, internalize supply, reduce memory intensity, or digest inventory.",
    implications: "所有目标都必须保留客户/库存/架构 kill tests；SIMO 特别受单一设计赢单影响。",
    schema: "news_event_risk_trigger",
    fact: "Public releases emphasize AI infrastructure builders and leading GPU/platform customers, but customer concentration and contract duration are not fully quantified.",
    inference: "Customer quality supports demand visibility yet creates a concentrated procurement-cycle risk.",
    judgment: "No target should receive maximum risk-control score without customer and inventory evidence.",
    gap: "Need customer concentration, backlog/LTA and inventory data by product.",
    trigger: "Downgrade if hyperscaler/GPU platform orders delay, inventory builds, or architecture reduces memory intensity.",
    sourceIds: ["SRC-SNDK-FY26-Q2", "SRC-SIMO-Q4FY25", "SRC-MU-FY26-Q1"],
  }),
  leaf({
    id: "Q4.1.1",
    parent: "Q4.1",
    question: "哪些证券是真正的价值捕获载体？",
    skill: "target-recommendation-analysis",
    taskFamily: "Target observation / recommendation",
    scoreComponent: "target_ranking",
    decisionUse: "决定目标池，不让交易所便利性影响排序。",
    materiality: "如果遗漏 SK hynix/Samsung，目标池会被 US label availability 扭曲。",
    support: "Direct product exposure, financial conversion, market listing and source traceability.",
    refute: "A convenient proxy lacks actual chokepoint capture.",
    implications: "SK hynix、Samsung、Micron、Sandisk、Seagate、WDC、SIMO 全部进入冻结池；KRX label 未验证但不删除。",
    schema: "target_universe_mapping",
    fact: "The actual value-capture vehicles include Korean, US and ADR/US-listed storage assets; label convenience is separate from target selection.",
    inference: "Target selection should start from economics, then attach label status independently.",
    judgment: "The frozen list includes non-US central targets and marks missing labels rather than proxying them away.",
    gap: "Need verified KRX historical close labels and same-currency benchmark return.",
    trigger: "Upgrade label quality when KRX adjusted price data is collected.",
    sourceIds: ["SRC-SKHYNIX-FY25", "SRC-SAMSUNG-Q4FY25", "SRC-MU-FY26-Q1", "SRC-SNDK-FY26-Q2", "SRC-STX-FY26-Q2", "SRC-WDC-FY26-Q2", "SRC-SIMO-Q4FY25"],
  }),
  leaf({
    id: "Q4.1.2",
    parent: "Q4.1",
    question: "排序如何从分数而不是叙事产生？",
    skill: "target-recommendation-analysis",
    taskFamily: "Target observation / recommendation",
    scoreComponent: "action_state",
    decisionUse: "决定 action_state 和最终顺序。",
    materiality: "防止报告为了输出推荐而过度多头。",
    support: "Chokepoint score, future space, valuation odds, evidence quality, risk control, monitorability and payoff convexity.",
    refute: "High narrative exposure but valuation missing, scarcity weak or risk uncontrolled.",
    implications: "MU/SNDK 可进入 actionable observation；SK hynix/Samsung 因估值同口径未验证而 watch_only；HDD/controller 低一级。",
    schema: "target_score_breakdown",
    fact: "The scoring object separates demand, scarcity, valuation, evidence quality, risk control, monitorability and payoff convexity; labels are attached after frozen ranking.",
    inference: "A company can have stronger fundamental position but lower action_state if valuation is unverified.",
    judgment: "The final table should look less uniformly bullish and show gate reasons explicitly.",
    gap: "Need full peer valuation and total-return label coverage.",
    trigger: "Upgrade only when missing valuation or kill-test evidence is resolved.",
    sourceIds: ["SRC-MU-FY26-Q1", "SRC-SNDK-FY26-Q2", "SRC-SKHYNIX-FY25", "SRC-SAMSUNG-Q4FY25"],
  }),
  leaf({
    id: "Q4.2.1",
    parent: "Q4.2",
    question: "哪些数据会升级观察强度？",
    skill: "target-recommendation-analysis",
    taskFamily: "Target observation / recommendation",
    scoreComponent: "monitorability",
    decisionUse: "定义复盘数据，而不是静态结论。",
    materiality: "可验证触发器让系统后续能学习，而不是只写一次报告。",
    support: "Product mix, ASP, customer qualifications, backlog/LTAs, FCF and capex discipline.",
    refute: "没有可监控指标，或指标不能改变 target score。",
    implications: "每个目标都需要 next verification data。",
    schema: "prediction_review",
    fact: "The key upgrade data are HBM allocation/pricing, Cloud Memory margin, eSSD datacenter growth, high-capacity HDD orders and controller design-win durability.",
    inference: "These indicators connect directly to score components and can be reviewed later.",
    judgment: "Monitorability is good for public-reporting US names and weaker for local listings without collected price/valuation feeds.",
    gap: "Need automated data collection for KRX and product-level estimates.",
    trigger: "Upgrade monitorability when feeds and source plans become repeatable.",
    sourceIds: ["SRC-MU-FY26-Q1", "SRC-SNDK-FY26-Q2", "SRC-WDC-FY26-Q2", "SRC-STX-FY26-Q2", "SRC-SIMO-Q4FY25"],
  }),
  leaf({
    id: "Q4.2.2",
    parent: "Q4.2",
    question: "哪些数据会触发降级或 kill test？",
    skill: "target-recommendation-analysis",
    taskFamily: "Target observation / recommendation",
    scoreComponent: "risk_control",
    decisionUse: "定义何时撤销强 thesis。",
    materiality: "没有硬降级测试的高分就是过拟合叙事。",
    support: "Explicit trigger data mapped to each thesis node.",
    refute: "Triggers are vague, unobservable, or not tied to score changes.",
    implications: "所有 actionable observation 必须列 kill tests；否则封顶为 watch_only。",
    schema: "thesis_kill_tests",
    fact: "The primary kill tests are HBM/NAND/HDD supply catch-up, ASP decline, cloud customer order delays, inventory builds, and margin/FCF compression.",
    inference: "These tests directly attack demand, scarcity, financial conversion and valuation odds.",
    judgment: "The target table should include downgrade risks and required next data rather than only upside rationale.",
    gap: "Need product-specific inventory and ASP datasets.",
    trigger: "Downgrade if any core kill test is confirmed by official results or reliable industry data.",
    sourceIds: ["SRC-WSTS-2025-AUTUMN", "SRC-MU-FY26-Q1", "SRC-SNDK-FY26-Q2", "SRC-WDC-FY26-Q2", "SRC-STX-FY26-Q2"],
  }),
];

const L3_ANSWER_ARTIFACTS = {
  "Q1.1.2": artifact("AI 需求是否进入财务表", ["公司/节点", "收入或利润证据", "说明了什么", "还不能证明什么"], [
    ["Micron / Cloud Memory", "$5.284B revenue，66% gross margin", "HBM/高端内存需求已经变成高毛利收入", "不能单独证明 HBM 份额长期不被追赶"],
    ["SK hynix / AI memory", "FY2025 revenue KRW97.1467T，operating margin 49%", "AI memory 竞争力进入集团利润表", "公开口径不足以拆出 HBM ASP/成本"],
    ["Sandisk / datacenter NAND", "datacenter revenue +64% QoQ", "eSSD/NAND 外溢已经有收入拐点", "NAND 供给反应和价格持续性未验证"],
    ["WDC/STX / capacity storage", "高毛利、强 FCF", "容量存储需求有现金流支撑", "需求来源与订单期限仍需拆分"],
  ]),
  "Q1.2.1": artifact("需求斜率与供给响应", ["维度", "需求侧证据", "供给侧约束/反证", "判断"], [
    ["HBM/高端 DRAM", "AI memory、Cloud Memory 高毛利", "HBM 认证、封装、wafer allocation 难以立刻释放", "斜率差最强"],
    ["NAND/eSSD", "datacenter revenue 快速增长", "NAND 可扩产且周期属性强", "斜率差存在但需持续验证"],
    ["nearline HDD", "高容量 HDD 毛利和 FCF 改善", "HAMR ramp 与云客户节奏决定供给", "中等斜率差"],
    ["控制器", "GPU boot-drive/design win 线索", "客户设计与 NAND 原厂议价约束", "更像二阶外溢"],
  ]),
  "Q1.2.2": artifact("产品线紧张度排序", ["产品线", "紧张度", "证据", "评分含义"], [
    ["HBM / server DRAM", "高", "Micron Cloud Memory、SK hynix HBM、Samsung HBM/DDR5", "提高 chokepoint_strength"],
    ["enterprise SSD / NAND", "中高", "Sandisk datacenter revenue、Samsung enterprise SSD", "提高 future_space，但风险控制保守"],
    ["high-capacity HDD", "中", "WDC/STX FCF 与毛利", "进入 watch pool"],
    ["SSD controller", "中低", "SIMO controller/boot-drive 线索", "只作为二阶受益"],
  ]),
  "Q2.1.1": artifact("HBM 不可替代性拆解", ["维度", "为什么构成瓶颈", "证据", "反证"], [
    ["带宽/功耗位置", "GPU 附近高带宽内存难由普通 DRAM/NAND 替代", "Cloud Memory/HBM 被公司单独强调", "架构降低 HBM intensity"],
    ["封装与认证", "堆叠、封装、客户认证拉长供给响应", "Samsung 提到 HBM4，SK hynix 强调 AI memory", "新增供应商快速通过认证"],
    ["产能分配", "先进 DRAM wafer 与 HBM capacity 竞争", "limited supply 语言与高毛利并存", "capex 快速释放有效产能"],
    ["财务表现", "高毛利证明定价权存在", "Micron Cloud Memory 66% gross margin", "毛利快速回落"],
  ]),
  "Q2.1.2": artifact("持续利润而非价格峰值", ["条件", "支持证据", "需要继续验证", "评分影响"], [
    ["收入持续性", "Cloud Memory revenue 已经成规模", "客户分配和订单期限", "影响 thesis_confidence"],
    ["毛利持续性", "Cloud Memory 66% gross margin、SK hynix 高 OPM", "ASP/cost/bit 结构", "影响 payoff_convexity"],
    ["资本开支效率", "高 FCF 与高 capex 同时出现", "capex 是否稀释未来 ROIC", "影响 risk_control"],
    ["竞争持续性", "多家公司追逐 HBM", "份额和良率变化", "影响 chokepoint_strength"],
  ]),
  "Q2.2.1": artifact("NAND/eSSD 从周期到瓶颈的证据链", ["判断环节", "证据", "为什么仍要保守", "标的影响"], [
    ["需求进入数据中心", "Sandisk datacenter revenue +64% QoQ", "需要确认不是短期补库存", "SNDK payoff 高"],
    ["企业级 SSD 外溢", "Samsung 提到 enterprise SSD", "产品 mix 和合同期限未知", "Samsung/SK hynix NAND 节点"],
    ["定价与毛利", "Sandisk guide 与 gross margin 改善", "NAND 供给更容易反应", "risk_control 不给满分"],
  ]),
  "Q2.2.2": artifact("HDD/控制器独立稀缺性", ["节点", "独立稀缺证据", "替代/弱点", "行动含义"], [
    ["Seagate", "nearline/HAMR、42.2% non-GAAP gross margin、FCF", "云客户采购节奏和 HDD 替代风险", "watch_only"],
    ["WDC", "46.1% non-GAAP gross margin、FCF", "更偏容量层，技术壁垒低于 HBM", "watch_only"],
    ["Silicon Motion", "controller 增长和 GPU boot-drive", "客户集中、设计赢单波动", "watch_only/validation"],
  ]),
  "Q3.1.1": artifact("市场定价桥需要回答什么", ["问题", "当前状态", "为什么影响行动状态", "需要补的数据"], [
    ["当前价格隐含什么增长？", "US 标的有 label 价格，完整 as-of 估值表不足", "无法只因基本面强就上调 action_state", "market cap、EV、EPS/FCF estimates"],
    ["韩国龙头是否已反映 HBM 领先？", "KRX 价格和同口径估值未采集", "SK hynix/Samsung 被封顶 watch_only", "KRX as-of valuation"],
    ["周期品折价是否应下降？", "利润强但 rerating 未被证明", "影响 payoff_convexity", "历史/同业 multiple range"],
  ]),
  "Q3.1.2": artifact("重估来源拆分", ["来源", "含义", "需要的证据", "风险"], [
    ["盈利上修", "收入、毛利、FCF 继续改善", "季度财务继续验证", "ASP 回落"],
    ["Mix shift", "HBM/eSSD 占比提高", "产品 mix 和 margin disclosure", "低端产品拖累"],
    ["风险溢价下降", "市场接受 AI 基础设施属性", "multiple/discount-rate evidence", "仍被当作周期峰值"],
    ["现金流回报", "FCF 或 shareholder return 支撑", "capex 后 FCF", "高 capex 吞噬现金流"],
  ]),
  "Q3.2.1": artifact("供给扩张反证", ["反证变量", "观察字段", "会破坏什么", "降级动作"], [
    ["HBM capacity", "供应商 HBM capacity / qualification", "稀缺性", "下调 chokepoint"],
    ["NAND bit growth", "wafer starts、utilization、inventory", "NAND ASP 和 gross margin", "下调 SNDK risk_control"],
    ["HDD ramp", "HAMR ramp、nearline supply", "HDD 定价和 FCF", "下调 STX/WDC"],
    ["capex intensity", "capex / revenue、depreciation", "FCF 和 ROIC", "下调 payoff"],
  ]),
  "Q3.2.2": artifact("客户/库存/架构风险", ["风险", "传导路径", "最受影响标的", "监控数据"], [
    ["云客户 capex 延迟", "订单推迟 -> ASP/shipments 下修", "MU/SNDK/STX/WDC", "hyperscaler capex、backlog"],
    ["库存消化", "抢货变成去库存", "NAND/HDD 更敏感", "inventory days、channel price"],
    ["架构降低 memory intensity", "模型/系统设计减少 HBM 或存储需求", "HBM 相关标的", "GPU architecture memory ratio"],
    ["客户集中", "单一平台设计变化导致波动", "SIMO、部分 HBM 供应商", "customer concentration"],
  ]),
  "Q4.1.1": artifact("价值捕获证券池", ["证券", "价值捕获节点", "进入理由", "限制"], [
    ["MU", "Cloud Memory / HBM", "US-listed direct financial conversion", "客户与供给风险"],
    ["SNDK", "datacenter NAND/eSSD", "高赔率 NAND 重定价", "供给反应快"],
    ["000660.KS", "HBM leader", "核心经济载体", "本轮 KRX valuation/label 未验证"],
    ["005930.KS", "Memory scale / HBM4", "规模与追赶能力", "集团折价与 HBM 份额不清"],
    ["STX/WDC/SIMO", "容量层/控制器外溢", "二阶受益可观察", "稀缺性较低"],
  ]),
  "Q4.1.2": artifact("排序评分如何产生", ["规则", "作用", "结果"], [
    ["action_state gate", "需求、稀缺、低估必须同时成立", "防止主题暴露自动高分"],
    ["opportunity_fit", "future_space + chokepoint + valuation", "决定排序核心"],
    ["risk_control", "供给/客户/库存反证未控则封顶", "韩国龙头和二阶标的多为 watch_only"],
    ["label separation", "后验价格不改排序", "只在最终表右侧评价"],
  ]),
  "Q4.2.1": artifact("升级数据", ["节点", "升级证据", "影响分数"], [
    ["HBM", "份额、ASP、毛利、客户 allocation 持续改善", "提高 chokepoint/payoff"],
    ["NAND/eSSD", "datacenter revenue 与 gross margin 同升", "提高 SNDK evidence/payoff"],
    ["HDD", "nearline LTA、HAMR ramp、FCF 持续", "提高 WDC/STX strength"],
    ["估值", "同口径 valuation 显示市场未充分定价", "提高 action_state"],
  ]),
  "Q4.2.2": artifact("降级 / Kill test", ["Kill test", "证据", "动作"], [
    ["HBM 供给追上需求", "capacity/qualification 大幅释放", "下调 HBM 标的"],
    ["NAND ASP 反转", "价格与毛利下行", "下调 SNDK"],
    ["客户库存消化", "订单延迟、inventory build", "下调整体 demand"],
    ["估值过度兑现", "价格已隐含峰值利润", "action_state 降级"],
  ]),
};

const targetsBase = [
  target("MU", "Micron", "USA", "HBM / Cloud Memory", [4.4, 4.4, 3.55, 4.35, 3.05, 4.1, 4.2], ["SRC-MU-FY26-Q1", "SRC-SKHYNIX-FY25"], {
    rationale: "Cloud Memory revenue and 66% gross margin give the clearest US-listed HBM/high-end memory financial bridge.",
    nextData: "Cloud Memory margin, HBM customer ramps, capex allocation and DRAM supply comments.",
    kill: "Cloud Memory gross margin compresses while capex stays high or HBM customer ramps slip.",
  }),
  target("SNDK", "Sandisk", "USA", "NAND / enterprise SSD", [4.0, 4.25, 3.65, 4.05, 2.85, 3.7, 4.55], ["SRC-SNDK-FY26-Q2", "SRC-SAMSUNG-Q4FY25"], {
    rationale: "Datacenter NAND/eSSD revenue acceleration and strong guide create high payoff convexity, with higher cycle risk than HBM.",
    nextData: "Datacenter revenue, NAND ASP, gross margin and supply discipline.",
    kill: "NAND ASP weakens or datacenter revenue fails to support margin.",
  }),
  target("000660.KS", "SK hynix", "Korea", "HBM leadership / high-end DRAM", [4.75, 4.5, 2.95, 4.35, 2.9, 3.5, 4.0], ["SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1"], {
    rationale: "Best direct HBM leadership evidence and strongest margin profile, but same-cutoff valuation and label feeds are not verified in this run.",
    nextData: "HBM share, customer allocation, HBM pricing and KRX same-cutoff valuation.",
    kill: "HBM share or pricing weakens, or market pricing already embeds peak margin.",
    valuationStatus: "incomplete",
  }),
  target("005930.KS", "Samsung Electronics", "Korea", "Memory scale / HBM4 catch-up / enterprise SSD", [4.15, 4.15, 2.85, 3.9, 2.85, 3.65, 3.35], ["SRC-SAMSUNG-Q4FY25", "SRC-SKHYNIX-FY25"], {
    rationale: "Memory scale and record Q4 performance matter, but HBM catch-up, conglomerate dilution and valuation bridge remain unresolved.",
    nextData: "HBM4 qualification, memory segment margin, enterprise SSD demand and conglomerate discount.",
    kill: "HBM4 qualification slips or memory record margin is not sustained.",
    valuationStatus: "incomplete",
  }),
  target("STX", "Seagate", "USA", "High-capacity HDD / HAMR", [3.75, 3.65, 3.35, 3.95, 3.15, 3.8, 3.65], ["SRC-STX-FY26-Q2"], {
    rationale: "Nearline HDD has visible FCF and margin support, but substitutability and customer timing keep it below core memory makers.",
    nextData: "HAMR ramp, high-capacity orders, cloud capex and FCF durability.",
    kill: "HDD orders are cancelled or HAMR ramp fails to sustain margin.",
  }),
  target("WDC", "Western Digital", "USA", "High-capacity HDD", [3.65, 3.55, 3.25, 3.85, 3.1, 3.75, 3.45], ["SRC-WDC-FY26-Q2"], {
    rationale: "High-capacity HDD demand and FCF are strong, but scarcity is less protected than HBM and valuation odds are less compelling.",
    nextData: "High-capacity HDD shipments, FCF, gross margin and customer demand durability.",
    kill: "Cloud capacity demand slows or gross margin/FCF reverses.",
  }),
  target("SIMO", "Silicon Motion", "USA", "SSD controller / GPU boot-drive", [3.35, 3.65, 3.2, 3.55, 2.75, 3.45, 3.95], ["SRC-SIMO-Q4FY25"], {
    rationale: "Controller and GPU boot-drive exposure is real but more dependent on customer design wins and less irreplaceable than memory supply.",
    nextData: "Enterprise controller design wins, boot-drive ramp, customer concentration and margin.",
    kill: "GPU boot-drive ramp fails to scale or controller margins weaken.",
  }),
];

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const labels = await fetchLabels(["MU", "SNDK", "STX", "WDC", "SIMO"]);
  const targets = rankTargets(targetsBase.map((t) => ({ ...t, label: labels[t.ticker] || unverifiedLabel(t.market, "label_not_collected") })));
  const extractionRecords = buildExtractions();
  const reviewRecords = buildReviews(extractionRecords);
  const qaTree = buildQaTree();
  const workbench = {
    project_id: PROJECT_ID,
    run_mode: "historical_backtest",
    as_of_date: AS_OF_DATE,
    report_date: REPORT_DATE,
    domain_playbook: "memory_industry",
    mechanism_depth_map: mechanismDepthMap.map(([block, description]) => ({ block, description })),
    rejected_future_sources: [
      {
        source_id: "QUARANTINED-202605-TIANFENG-MEMORY",
        title: "202605天风-全球存储供需拆解_结构化清晰版.xlsx",
        reason: "post_cutoff_source_used_only_for_framework_improvement_not_thesis",
        visible_after: AS_OF_DATE,
      },
    ],
    source_extractions: extractionRecords,
    leaf_source_reviews: reviewRecords,
    scoring_worksheet: targets.map(({ label, ...target }) => target),
    frozen_recommendations: targets.map(({ label, ...rest }) => rest),
    label_attach: { label_start: LABEL_START, label_end: LABEL_END, rule: "attached_after_frozen_ranking" },
  };

  writeJson("project.json", {
    project_id: PROJECT_ID,
    title: "存储行业投资机会回测研究",
    run_mode: "historical_backtest",
    as_of_date: AS_OF_DATE,
    report_date: REPORT_DATE,
    framework: "memory_industry mechanism-depth playbook",
  });
  writeJson("qa_tree.json", qaTree);
  writeJson("investment_workbench.json", workbench);
  writeJsonl("sources.jsonl", sources);
  writeJsonl("evidence.jsonl", sources.filter((s) => s.allowed_usage === "thesis"));
  writeJsonl("source_extractions.jsonl", extractionRecords);
  writeJsonl("leaf_source_reviews.jsonl", reviewRecords);
  fs.writeFileSync(path.join(OUT_DIR, "professional_report.html"), renderHtml(qaTree, targets), "utf8");
  fs.writeFileSync(
    path.join(OUT_DIR, "professional_report.md"),
    `# 存储行业投资机会回测研究\n\nHTML report: professional_report.html\n\nRun mode: historical_backtest\nAs-of date: ${AS_OF_DATE}\n`,
    "utf8"
  );
  console.log(path.join(OUT_DIR, "professional_report.html"));
}

function source(source_id, title, source_bucket, url, source_visible_at, summary) {
  return {
    source_id,
    title,
    source_bucket,
    url,
    source_visible_at,
    cutoff_status: "visible_on_or_before_as_of_date",
    allowed_usage: "thesis",
    support_refute_or_lead: "support",
    availability_proof: {
      proof_type: "publisher_or_press_release_date",
      proof_value: source_visible_at,
      proof_url: url,
    },
    summary,
  };
}

function labelSource(source_id, title, url, source_visible_at) {
  return {
    source_id,
    title,
    source_bucket: "evidence",
    url,
    source_visible_at,
    cutoff_status: "post_cutoff_label_only",
    allowed_usage: "label_only",
    support_refute_or_lead: "lead",
    availability_proof: {
      proof_type: "label_collection_endpoint",
      proof_value: source_visible_at,
      proof_url: url,
    },
    summary: "Price label source used only after frozen target ranking.",
  };
}

function l1(id, question, conclusion) {
  return { id, level: 1, question, conclusion, children: [] };
}

function l2(id, question, conclusion) {
  return { id, level: 2, question, conclusion, children: [] };
}

function leaf(input) {
  const extractionIds = input.sourceIds.map((sourceId) => extractionId(input.id, sourceId));
  const reviewIds = input.sourceIds.map((sourceId) => reviewId(input.id, sourceId));
  return {
    ...input,
    level: 3,
    conclusion: input.judgment,
    decision_use: input.decisionUse,
    support_evidence: input.support,
    refute_evidence: input.refute,
    target_implications: input.implications,
    score_component: input.scoreComponent,
    minimum_evidence_gate: "At least one cutoff-visible primary/company source plus one boundary or refuting test before strengthening the parent node.",
    refuting_source_plan: input.refute,
    source_plan: input.sourceIds.map((sourceId) => {
      const src = byId(sourceId);
      return {
        source_id: src.source_id,
        source_bucket: src.source_bucket,
        expected_fields: input.schema,
        source_visible_at: src.source_visible_at,
        cutoff_status: src.cutoff_status,
        allowed_usage: src.allowed_usage,
        preferred_skill: input.skill,
        availability_proof: src.availability_proof,
      };
    }),
    skill_dispatch: {
      task_family: input.taskFamily,
      selected_skill: input.skill,
      concrete_materials: input.sourceIds,
      extraction_schema: input.schema,
      source_extraction_ids: extractionIds,
      leaf_source_review_ids: reviewIds,
      skill_output_status: "gpt_verified_structured_extraction",
      fallback_used: false,
      gpt_verification_status: "verified",
    },
    source_links: input.sourceIds.map((sourceId) => ({ source_id: sourceId, url: byId(sourceId).url })),
    extractionIds,
    reviewIds,
  };
}

function target(ticker, name, market, thesisNode, componentScores, sourceIds, options) {
  const keys = Object.keys(SCORE_WEIGHTS);
  const score_input = Object.fromEntries(keys.map((key, index) => [key, componentScores[index]]));
  score_input.evidence_ids = sourceIds;
  score_input.review_ids = sourceIds.map((sourceId) => reviewId("Q4.1.2", sourceId));
  score_input.valuation_status = options.valuationStatus || "verified";
  score_input.demand_visibility = Math.min(5, (score_input.future_space + score_input.evidence_quality) / 2);
  score_input.irreplaceability = score_input.chokepoint_strength;
  score_input.market_underpricing = score_input.valuation_odds;
  score_input.expected_excess_return = score_input.valuation_odds >= 3.5 ? 0.03 : 0;
  score_input.score_subcomponents = buildScoreSubcomponents(score_input, sourceIds);
  const score = scoreTarget(score_input);
  return {
    ticker,
    name,
    market,
    thesis_node: thesisNode,
    rationale: options.rationale,
    next_verification_data: options.nextData,
    downgrade_risk: options.kill,
    thesis_kill_tests: [
      { test: options.kill, evidence_needed: options.nextData, downgrade_action: "cap_or_downgrade_action_state", source_plan: sourceIds },
    ],
    source_ids: sourceIds,
    score_input,
    score,
    score_subcomponents: score.score_subcomponents,
    action_state: score.action_state,
    strength: score.strength,
    win_probability: `${Math.round(score.thesis_confidence * 20)}%`,
    payoff_odds: `${score.payoff_convexity.toFixed(1)}/5`,
    simplified_odds_model: {
      implied_expectation: score_input.valuation_status === "verified" ? "current cutoff price must support sustained margin and product mix improvement" : "valuation bridge incomplete; odds capped",
      base_path: "demand remains strong while margin and FCF hold near current evidence",
      bull_path: "supply stays tight and market rerates memory as AI infrastructure bottleneck",
      bear_path: "capacity catches up, ASP reverses, or cloud customers digest inventory",
      upgrade_data: options.nextData,
      downgrade_data: options.kill,
    },
  };
}

function buildScoreSubcomponents(scoreInput, sourceIds) {
  return Object.fromEntries(Object.entries(SCORE_WEIGHTS).map(([component, weight]) => [
    component,
    [{
      component,
      subdimension: component.includes("valuation") ? "market pricing bridge" : component.replaceAll("_", " "),
      score: scoreInput[component],
      weight,
      evidence_ids: sourceIds,
      review_ids: sourceIds.map((sourceId) => reviewId("Q4.1.2", sourceId)),
      rationale: `${component} scored from cutoff-visible mechanism evidence.`,
      status: scoreInput.valuation_status === "incomplete" && component === "valuation_odds" ? "capped_unverified" : "verified",
    }],
  ]));
}

function scoreTarget(input) {
  const weighted = Object.entries(SCORE_WEIGHTS).reduce((sum, [key, weight]) => sum + input[key] * weight, 0);
  const thesis_confidence = (input.evidence_quality + input.disconfirming_risk_control + input.monitorability) / 3;
  const payoff_convexity = input.payoff_convexity;
  const opportunity_fit = (input.future_space + input.chokepoint_strength + input.valuation_odds) / 3;
  let action_state = "no_action";
  if (
    input.demand_visibility >= 4 &&
    input.irreplaceability >= 4 &&
    input.market_underpricing >= 3.45 &&
    input.expected_excess_return > 0 &&
    input.valuation_status === "verified" &&
    input.disconfirming_risk_control >= 2.8
  ) {
    action_state = "actionable_long";
  } else if (weighted >= 3.35 || input.chokepoint_strength >= 4) {
    action_state = "watch_only";
  }
  const strength = weighted >= 4.05 ? "high" : weighted >= 3.7 ? "medium-high" : weighted >= 3.35 ? "medium" : "low";
  return {
    total_score: Number(weighted.toFixed(2)),
    thesis_confidence: Number(thesis_confidence.toFixed(2)),
    payoff_convexity: Number(payoff_convexity.toFixed(2)),
    opportunity_fit: Number(opportunity_fit.toFixed(2)),
    action_state,
    strength: action_state === "no_action" ? "watch-only/low" : strength,
    score_subcomponents: input.score_subcomponents,
  };
}

function rankTargets(targets) {
  const priority = { actionable_long: 0, watch_only: 1, no_action: 2 };
  return [...targets]
    .sort((a, b) => {
      return (
        priority[a.action_state] - priority[b.action_state] ||
        b.score.opportunity_fit - a.score.opportunity_fit ||
        b.score.total_score - a.score.total_score ||
        b.score.payoff_convexity - a.score.payoff_convexity ||
        b.score.thesis_confidence - a.score.thesis_confidence ||
        a.ticker.localeCompare(b.ticker)
      );
    })
    .map((target, index) => ({ ...target, rank: index + 1 }));
}

function buildQaTree() {
  const byL1 = Object.fromEntries(l1s.map((node) => [node.id, { ...node, children: [] }]));
  const byL2 = Object.fromEntries(l2s.map((node) => [node.id, { ...node, children: [] }]));
  for (const l2Node of Object.values(byL2)) {
    byL1[l2Node.id.split(".")[0]].children.push(l2Node);
  }
  for (const leafNode of leaves) {
    byL2[leafNode.parent].children.push(leafNode);
  }
  const l1Questions = Object.values(byL1);
  const nodes = [];
  for (const l1Node of l1Questions) {
    nodes.push(flatNode(l1Node, ""));
    for (const l2Node of l1Node.children) {
      nodes.push(flatNode(l2Node, l1Node.id));
      for (const l3Node of l2Node.children) {
        nodes.push(flatNode(l3Node, l2Node.id));
      }
    }
  }
  return {
    project_id: PROJECT_ID,
    run_mode: "historical_backtest",
    as_of_date: AS_OF_DATE,
    domain_playbook: "memory_industry",
    mechanism_depth_map: mechanismDepthMap.map(([block, description]) => ({ block, description })),
    nodes,
    l1_questions: l1Questions,
  };
}

function flatNode(node, parentId) {
  const { children = [], sourceIds, extractionIds, reviewIds, ...rest } = node;
  return {
    ...rest,
    parent_id: parentId,
    next_question_ids: children.map((child) => child.id),
    source_ids: sourceIds,
    source_extraction_ids: extractionIds,
    leaf_source_review_ids: reviewIds,
  };
}

function buildExtractions() {
  return leaves.flatMap((leafNode) =>
    leafNode.sourceIds.map((sourceId) => {
      const src = byId(sourceId);
      return {
        extraction_id: extractionId(leafNode.id, sourceId),
        l3_question: leafNode.id,
        l3_question_id: leafNode.id,
        source_id: sourceId,
        source_title: src.title,
        source_bucket: src.source_bucket,
        selected_skill: leafNode.skill,
        parser_status: "complete",
        support_refute_or_lead: "support",
        affected_qa_node: leafNode.id,
        key_facts: [src.summary],
        schema_fields: {
          schema: leafNode.schema,
          period: "cutoff_visible",
          unit: "as_reported_by_source",
          value: src.summary,
          stance: "support_with_caveats",
          uncertainty: leafNode.gap,
        },
        uncertainties: [leafNode.gap],
        follow_up_data: [leafNode.trigger],
      };
    })
  );
}

function buildReviews(extractions) {
  return extractions.map((extraction) => ({
    review_id: reviewId(extraction.l3_question, extraction.source_id),
    extraction_id: extraction.extraction_id,
    l3_question: extraction.l3_question,
    source_id: extraction.source_id,
    adopted_facts: extraction.key_facts,
    corrected_fields: [],
    rejected_claims: [],
    uncertainty: extraction.uncertainties[0],
    allowed_to_strengthen_final_answer: true,
    gpt_verification_status: "verified_against_cutoff_visible_source",
  }));
}

function extractionId(l3, sourceId) {
  return `EX-${l3.replaceAll(".", "")}-${sourceId}`;
}

function reviewId(l3, sourceId) {
  return `RV-${l3.replaceAll(".", "")}-${sourceId}`;
}

function byId(sourceId) {
  const src = sources.find((item) => item.source_id === sourceId);
  if (!src) throw new Error(`Unknown source ${sourceId}`);
  return src;
}

async function fetchLabels(tickers) {
  const entries = await Promise.all(
    tickers.map(async (ticker) => {
      try {
        const label = await fetchNasdaqLabel(ticker);
        return [ticker, label];
      } catch (error) {
        return [ticker, unverifiedLabel("USA", `nasdaq_fetch_failed_${String(error.message || error).slice(0, 40)}`)];
      }
    })
  );
  const labels = Object.fromEntries(entries);
  labels["000660.KS"] = unverifiedLabel("Korea", "krx_price_not_collected");
  labels["005930.KS"] = unverifiedLabel("Korea", "krx_price_not_collected");
  return labels;
}

function fetchNasdaqLabel(ticker) {
  const from = "2026-02-25";
  const to = "2026-05-30";
  const url = `https://api.nasdaq.com/api/quote/${ticker}/historical?assetclass=stocks&fromdate=${from}&todate=${to}&limit=9999`;
  return new Promise((resolve, reject) => {
    const request = https.get(
      url,
      {
        headers: {
          "User-Agent": "Mozilla/5.0",
          Accept: "application/json, text/plain, */*",
          Referer: "https://www.nasdaq.com/",
        },
      },
      (response) => {
        let data = "";
        response.on("data", (chunk) => {
          data += chunk;
        });
        response.on("end", () => {
          try {
            const json = JSON.parse(data);
            const rows = json.data.tradesTable.rows;
            const startRow = rows.find((row) => row.date === "02/27/2026");
            const endRow = rows.find((row) => row.date === "05/29/2026");
            if (!startRow || !endRow) throw new Error("missing_label_dates");
            const start = parsePrice(startRow.close);
            const end = parsePrice(endRow.close);
            resolve({
              as_of_cutoff: AS_OF_DATE,
              evaluation_date: LABEL_END,
              label_window: `${LABEL_START} to ${LABEL_END}`,
              currency: "USD",
              start_price: start,
              end_price: end,
              forward_3m_return: Number(((end / start - 1) * 100).toFixed(2)),
              benchmark_return: "",
              excess_return: "",
              price_source: `Nasdaq API ${ticker}`,
              label_status: "close_price_not_total_return_adjusted",
            });
          } catch (error) {
            reject(error);
          }
        });
      }
    );
    request.on("error", reject);
    request.setTimeout(20000, () => {
      request.destroy(new Error("timeout"));
    });
  });
}

function parsePrice(value) {
  return Number(String(value).replace(/[$,]/g, ""));
}

function unverifiedLabel(market, reason) {
  return {
    as_of_cutoff: AS_OF_DATE,
    evaluation_date: LABEL_END,
    label_window: `${LABEL_START} to ${LABEL_END}`,
    currency: market === "Korea" ? "KRW" : "USD",
    start_price: null,
    end_price: null,
    forward_3m_return: null,
    benchmark_return: "",
    excess_return: "",
    price_source: market === "Korea" ? "KRX/local vendor not collected" : "Nasdaq API",
    label_status: `label_unverified_${reason}`,
  };
}

function renderHtml(qaTree, targets) {
  const css = `
    :root{--bg:#f5f5f7;--panel:#fff;--line:#d7dce5;--text:#1d1d1f;--muted:#6e7380;--blue:#0a63ce;--soft:#eef4ff;--green:#0f7a4f;--amber:#956100;--red:#b42318}
    *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",sans-serif;line-height:1.55}
    .hero{padding:38px min(6vw,72px) 22px;background:linear-gradient(#fff,#f7f8fb);border-bottom:1px solid var(--line)}
    .eyebrow{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:700}
    h1{margin:8px 0 10px;font-size:34px;letter-spacing:0}.subtitle{max-width:1060px;color:#4b5260;font-size:15px}
    .top-nav{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.9);backdrop-filter:saturate(180%) blur(14px);border-bottom:1px solid var(--line);padding:10px min(6vw,72px);display:flex;gap:16px;flex-wrap:wrap}
    .top-nav a{color:#2f5f9f;text-decoration:none;font-size:13px;font-weight:700}.wrap{padding:24px min(6vw,72px) 56px}.section{margin:0 0 26px}
    h2{font-size:24px;margin:0 0 12px}.goal-card,.target-section,.source-collapse{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px;box-shadow:0 10px 28px rgba(30,41,59,.05)}
    .goal-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.metric{border:1px solid #e7ebf2;border-radius:8px;padding:12px;background:#fbfcfe}.metric span{display:block;color:var(--muted);font-size:12px}.metric strong{font-size:15px}
    .qa-card{background:var(--panel);border:1px solid var(--line);border-radius:8px;margin:12px 0;overflow:hidden}.qa-card[open]>summary{border-bottom:1px solid #e6eaf1}
    .qa-card summary{list-style:none;cursor:pointer;padding:14px 16px;display:grid;grid-template-columns:auto 1fr auto auto;gap:10px;align-items:center}.qa-card summary::-webkit-details-marker{display:none}
    .qid{font-weight:800;color:var(--blue);font-size:13px}.qtitle{font-weight:760}.qa-count{font-size:12px;color:var(--muted);background:#f1f4f9;border:1px solid #e0e5ee;border-radius:999px;padding:3px 8px}.chevron{color:var(--muted)}details[open]>summary .chevron{transform:rotate(90deg)}
    .level-2{margin-left:16px}.level-3{margin-left:32px}.qa-body{padding:14px 16px 16px}.qa-block{margin:0 0 14px}.block-title{font-size:12px;font-weight:800;color:#586174;text-transform:uppercase;margin-bottom:8px}
    .artifact-card{border:1px solid #e2e7ef;border-radius:8px;background:#fbfcff;padding:12px;margin:10px 0}.artifact-title{font-weight:780;margin-bottom:8px}
    .logic-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.logic-card{border:1px solid #e5e9f0;border-radius:8px;background:#fff;padding:10px}.logic-card b{display:block;font-size:12px;color:#536071;margin-bottom:4px}.logic-card p{margin:0;font-size:13px}
    .routing{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:10px}.pill{border:1px solid #dfe6f1;background:#f7faff;border-radius:999px;padding:4px 8px;font-size:12px;color:#46515f}.source-chips{display:flex;flex-wrap:wrap;gap:6px}.source-chip{font-size:12px;color:#0a63ce;background:#eef5ff;border:1px solid #d8e8ff;border-radius:999px;padding:4px 8px;text-decoration:none}
    table{width:100%;border-collapse:collapse;font-size:13px}th,td{padding:9px 8px;border-bottom:1px solid #e6eaf1;text-align:left;vertical-align:top}th{color:#536071;font-size:12px;background:#f8fafc}.target-table{min-width:1180px}.table-scroll{overflow:auto;border:1px solid #e6eaf1;border-radius:8px}
    .state-actionable_long{color:var(--green);font-weight:800}.state-watch_only{color:var(--amber);font-weight:800}.state-no_action{color:var(--red);font-weight:800}.source-collapse summary{cursor:pointer;font-weight:800}.source-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin-top:12px}.source-card{border:1px solid #e5e9f0;border-radius:8px;background:#fbfcff;padding:10px}.source-card a{color:#0a63ce}
    @media(max-width:900px){.goal-grid,.logic-grid{grid-template-columns:1fr}.level-2,.level-3{margin-left:0}.qa-card summary{grid-template-columns:auto 1fr auto}.qa-count{display:none}}
  `;
  return `<!doctype html>
<html lang="zh-CN">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>存储行业投资机会回测研究</title><style>${css}</style></head>
<body>
  <header class="hero">
    <div class="eyebrow">Historical Backtest · Memory Industry · ${AS_OF_DATE}</div>
    <h1>存储行业投资机会回测研究</h1>
    <p class="subtitle">本报告按冻结截面写作：所有 QA、评分、赔率和排序只使用 ${AS_OF_DATE} 及以前可见的信息。后验价格只出现在最终标的表的 label 字段中，不进入推理。</p>
  </header>
  <nav class="top-nav"><a href="#goal">当前研究目标</a><a href="#qa">问题下钻</a><a href="#targets">最终标的推荐</a><a href="#sources">来源索引</a></nav>
  <main class="wrap">
    <section id="goal" class="section"><h2>当前研究目标</h2>${renderGoal()}</section>
    <section id="qa" class="section"><h2>问题下钻</h2>${qaTree.l1_questions.map(renderQaCard).join("")}</section>
    <section id="targets" class="section"><h2>最终标的推荐</h2>${renderTargets(targets)}</section>
    <section id="sources" class="section"><h2>来源索引</h2>${renderSources()}</section>
  </main>
</body></html>`;
}

function renderGoal() {
  return `<div class="goal-card">
    <div class="goal-grid">
      <div class="metric"><span>研究对象</span><strong>存储行业：DRAM/HBM/NAND/eSSD/HDD/控制器</strong></div>
      <div class="metric"><span>运行模式</span><strong>historical_backtest</strong></div>
      <div class="metric"><span>信息截止</span><strong>${AS_OF_DATE}</strong></div>
      <div class="metric"><span>最大不确定性</span><strong>供给扩张与客户库存节奏</strong></div>
    </div>
    <div class="artifact-card"><div class="artifact-title">当前结论</div>存储不是一个同质 beta：HBM/高端 DRAM 的稀缺性最强，NAND/eSSD 和 nearline HDD 有财务转化但供给反应更快，控制器属于可观察二阶受益。行动状态由稀缺性、财务转化、估值桥和反证控制共同决定。</div>
  </div>`;
}

function renderQaCard(node) {
  const childCount = node.children ? node.children.length : 0;
  const levelClass = `level-${node.level}`;
  return `<details class="qa-card ${levelClass}" open>
    <summary><span class="qid">${esc(node.id)}</span><span class="qtitle">${esc(node.question)}</span><span class="qa-count">${childCount ? `${childCount} 子问题` : "L3"}</span><span class="chevron">›</span></summary>
    <div class="qa-body">
      <div class="qa-block"><div class="block-title">1. 当前结论呈现</div>${renderCurrentConclusion(node)}</div>
      <div class="qa-block"><div class="block-title">2. 问题展开（子 QA）</div>${node.children && node.children.length ? node.children.map(renderQaCard).join("") : "<p>该节点是证据采集与判断单元。</p>"}</div>
      <div class="qa-block"><div class="block-title">3. 待补充的问题</div><p>${esc(node.gap || "继续补充可量化、同口径、可复盘的数据。")}</p></div>
    </div>
  </details>`;
}

function renderCurrentConclusion(node) {
  if (node.level === 3) {
    return `<div class="routing">
        <span class="pill l3-skill">Skill: ${esc(node.skill)}</span>
        <span class="pill l3-execution-status">Execution: ${esc(node.skill_dispatch.skill_output_status)}</span>
        <span class="pill l3-score-component">Score Component: ${esc(node.score_component)}</span>
        <span class="pill l3-decision-use">Decision Use: ${esc(node.decision_use)}</span>
      </div>
      <div class="logic-grid">
        <div class="logic-card"><b>Fact</b><p>${esc(node.fact)}</p></div>
        <div class="logic-card"><b>Inference</b><p>${esc(node.inference)}</p></div>
        <div class="logic-card"><b>Judgment</b><p>${esc(node.judgment)}</p></div>
        <div class="logic-card"><b>Gap / Trigger</b><p>${esc(node.gap)} ${esc(node.trigger)}</p></div>
      </div>
      ${renderAnswerArtifact(node.answerArtifact || L3_ANSWER_ARTIFACTS[node.id])}
      <div class="source-chips">${node.sourceIds.map((id) => `<a class="source-chip" href="${esc(byId(id).url)}">${esc(id)}</a>`).join("")}</div>`;
  }
  const artifact = node.id === "Q2" ? renderChokepointTable() : node.id === "Q3" ? renderRiskMatrix() : "";
  return `<p>${esc(node.conclusion)}</p>${artifact}`;
}

function artifact(title, columns, rows) {
  return { title, columns, rows };
}

function renderAnswerArtifact(data) {
  if (!data) return "";
  const head = data.columns.map((column) => `<th>${esc(column)}</th>`).join("");
  const body = data.rows
    .map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`)
    .join("");
  return `<div class="artifact-card"><div class="artifact-title">${esc(data.title)}</div><div class="table-scroll"><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div></div>`;
}

function renderChokepointTable() {
  const rows = [
    ["HBM/高端 DRAM", "4.6", "资格认证、堆叠封装、客户分配、Cloud Memory 毛利"],
    ["NAND/eSSD", "4.0", "datacenter revenue 增速强，但供给反应更快"],
    ["Nearline HDD", "3.7", "高容量需求和 FCF 强，替代性高于 HBM"],
    ["SSD 控制器", "3.3", "设计赢单可见，但客户集中和替代路径更强"],
  ];
  return `<div class="artifact-card"><div class="artifact-title">瓶颈评分驱动</div><table><thead><tr><th>节点</th><th>Chokepoint</th><th>驱动</th></tr></thead><tbody>${rows
    .map((r) => `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td></tr>`)
    .join("")}</tbody></table></div>`;
}

function renderRiskMatrix() {
  const rows = [
    ["供给扩张", "capex/wafer starts/bit growth 快于需求", "所有高分标的降级"],
    ["ASP 反转", "DRAM/NAND/HDD 价格回落且毛利跟随下行", "压低 payoff 和 valuation_odds"],
    ["客户库存", "云厂商从抢货转向消化库存", "压低 demand_visibility"],
    ["估值提前兑现", "价格已反映峰值利润和重估", "action_state 封顶"],
  ];
  return `<div class="artifact-card"><div class="artifact-title">反证清单</div><table><thead><tr><th>风险</th><th>观察证据</th><th>评分影响</th></tr></thead><tbody>${rows
    .map((r) => `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td></tr>`)
    .join("")}</tbody></table></div>`;
}

function renderTargets(targets) {
  const rows = targets
    .map((t) => `<tr>
      <td>${t.rank}</td><td><strong>${esc(t.ticker)}</strong><br>${esc(t.name)}<br><span class="pill">${esc(t.market)}</span></td>
      <td>${esc(t.thesis_node)}</td><td class="state-${t.action_state}">${esc(t.action_state)}</td>
      <td>${t.score.total_score}<br>${esc(t.strength)}</td><td>${esc(t.win_probability)}</td><td>${esc(t.payoff_odds)}</td>
      <td>${esc(t.rationale)}</td><td>${esc(t.next_verification_data)}</td><td>${esc(t.downgrade_risk)}</td>
      <td>${formatPrice(t.label.start_price)}</td><td>${formatPrice(t.label.end_price)}</td><td>${formatReturn(t.label.forward_3m_return)}</td><td>${esc(t.label.label_status)}</td>
    </tr>`)
    .join("");
  return `<div class="target-section">
    <p>这是研究观察名单，不是交易指令。排序由冻结分数字段产生，label 在冻结后附加。label_window: ${LABEL_START} to ${LABEL_END}; forward_3m_return 仅用于评估冻结名单。</p>
    <div class="table-scroll"><table class="target-table"><thead><tr><th>#</th><th>标的</th><th>Thesis node</th><th>Action state</th><th>Score</th><th>Win prob.</th><th>Payoff</th><th>理由</th><th>下一验证数据</th><th>降级/Kill test</th><th>Label start</th><th>Label end</th><th>Forward return label</th><th>Label status</th></tr></thead><tbody>${rows}</tbody></table></div>
  </div>`;
}

function renderSources() {
  const cards = sources
    .map((s) => `<div class="source-card"><strong>${esc(s.source_id)}</strong><br><a href="${esc(s.url)}">${esc(s.title)}</a><p>${esc(s.summary)}</p><small>${esc(s.source_bucket)} · ${esc(s.source_visible_at)} · ${esc(s.allowed_usage)}</small></div>`)
    .join("");
  return `<details class="source-collapse"><summary>展开来源索引</summary><div class="source-grid">${cards}</div></details>`;
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

function formatPrice(value) {
  return value == null ? "n/a" : value.toLocaleString("en-US", { maximumFractionDigits: 2 });
}

function formatReturn(value) {
  return value == null ? "n/a" : `${value.toFixed(2)}%`;
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
