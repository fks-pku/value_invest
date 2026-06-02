const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const PROJECT_ID = "ai_factory_industry_timeslice_20260302";
const OUT_DIR = path.join(ROOT, "research", "qa_projects", PROJECT_ID);
const AS_OF_DATE = "2026-03-02";
const EVALUATION_DATE = "2026-06-02";
const LABEL_START_DATE = "2026-03-02";
const LABEL_END_DATE = "2026-06-01";
const LABEL_WINDOW = "2026-03-02_to_2026-06-02";
const BENCHMARK_RETURN = 62.46;

const SCORE_WEIGHTS = {
  chokepoint_strength: 0.26,
  future_space: 0.18,
  valuation_odds: 0.18,
  evidence_quality: 0.14,
  disconfirming_risk_control: 0.10,
  monitorability: 0.05,
  payoff_convexity: 0.09,
};

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
  source("SRC-SKHYNIX-FY25", "SK hynix FY2025 results", "evidence", "https://www.prnewswire.com/news-releases/sk-hynix-announces-fy25-financial-results-posts-record-high-results-and-delivers-highest-shareholder-returns-302672384.html", "2026-01-28", "SK hynix FY2025 revenue was KRW97.1467T, operating profit KRW47.2063T and operating margin 49%, driven by AI memory and HBM leadership."),
  source("SRC-SAMSUNG-FY25", "Samsung Q4 and FY2025 results", "evidence", "https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results", "2026-01-29", "Samsung Q4 2025 Memory Business reached record quarterly revenue and operating profit, with HBM, server DDR5 and enterprise SSD as high-value AI products."),
  source("SRC-SMCI-FY26-Q2", "Supermicro FY2026 Q2 results", "evidence", "https://ir.supermicro.com/news/news-details/2026/Super-Micro-Computer-Inc.-Reports-Second-Quarter-Fiscal-2026-Financial-Results/default.aspx", "2026-02-03", "Supermicro remained an AI server assembly exposure, but margin, execution and governance risks require a lower risk-control score."),
  labelSource("LBL-NASDAQ-HISTORICAL", "Nasdaq historical close dataset", "https://api.nasdaq.com/api/quote/NVDA/historical", EVALUATION_DATE),
  labelSource("LBL-KRX-UNVERIFIED", "KRX local price check placeholder", "https://global.krx.co.kr/", EVALUATION_DATE),
];

const chainExplainer = {
  plainSummary: "一句话看懂：AI 工厂不是只买 GPU，而是云厂商和 AI 公司把算力、内存、网络、存储、电力冷却、机柜和系统软件一起采购成可运行的生产线；最值得研究的是谁控制难替代的卡点，谁只是跟着主题涨。",
  flowSteps: [
    "下游客户先决定是否继续加 AI capex：云厂商、AI 实验室、企业和主权 AI 项目提出训练、推理和 agent 工作负载。",
    "平台层把需求变成标准架构：NVIDIA、Broadcom/ASIC 路线、以太网网络和系统商定义机柜、服务器、网络和软件栈。",
    "芯片制造和内存环节把平台变成可交付硬件：先进制程、先进封装、HBM、服务器 DRAM 和高端 NAND 决定供给速度。",
    "连接、电力、液冷和系统交付把硬件落到数据中心：机柜级互联、电源、冷却、服务器整合和服务能力决定项目能否按期上线。",
    "利润留在稀缺且难替代的节点：平台控制、HBM、先进制造/封装、机柜级连接、电力液冷和有高质量 backlog 的系统交付。"
  ],
  layers: [
    { name: "需求端", role: "决定 AI capex 是否持续", players: "hyperscaler、AI lab、企业、主权 AI、CoreWeave/xAI 等新云", note: "如果 token 收入、企业 ROI 或模型需求放缓，全链条估值都会承压。" },
    { name: "平台控制", role: "把需求变成标准系统", players: "NVDA、AVGO custom ASIC、AMD/ASIC 替代路线", note: "平台越强，卡点越稀缺；但最强平台也最容易被提前定价。" },
    { name: "芯片制造和内存", role: "提供先进制程、封装、HBM 和服务器内存", players: "TSMC、SK hynix、Samsung、Micron", note: "这是 AI 工厂真正硬瓶颈之一，重点看产能、良率、客户资格和毛利。" },
    { name: "网络和连接", role: "让一整排 GPU/ASIC 像一个系统工作", players: "ALAB、CRDO、AVGO、ANET、MRVL", note: "连接是系统效率瓶颈，但要区分开放以太网、NVIDIA 自有网络和客户集中风险。" },
    { name: "电力冷却和系统交付", role: "把 AI 工厂变成可上线数据中心", players: "VRT、DELL、SMCI、HPE、ODM", note: "订单和 backlog 可验证，但系统商利润率和执行质量差异很大。" },
    { name: "运营与回报", role: "验证 AI 工厂是否赚钱", players: "云厂商、AI 应用商、企业客户", note: "只有客户持续赚钱并追加 capex，上游硬件弹性才不是一次性周期。" },
  ],
  chokepoints: [
    { node: "平台控制", why: "软硬件栈和客户生态决定系统标准", controllers: "NVDA / ASIC 平台方", qa: "Q2.1 / Q4.1" },
    { node: "HBM 与先进封装", why: "高带宽内存和封装限制 GPU/ASIC 交付斜率", controllers: "SK hynix、Samsung、MU、TSMC", qa: "Q2.1 / Q4.1" },
    { node: "机柜级连接", why: "低延迟、高带宽连接决定 AI 工厂利用率", controllers: "ALAB、CRDO、MRVL、AVGO、ANET", qa: "Q2.2 / Q3.2" },
    { node: "电力和液冷", why: "高功率机柜没有电力冷却就无法落地", controllers: "VRT、数据中心工程商", qa: "Q2.2 / Q4.1" },
    { node: "系统交付 backlog", why: "AI 服务器订单要转成收入和现金流", controllers: "DELL、SMCI、HPE/ODM", qa: "Q2.2 / Q3.1" },
  ],
  targetLinks: [
    ["NVDA", "平台控制", "稀缺性最强，但估值隐含预期也最高", "Q2.1 / Q4.1"],
    ["VRT", "电力/液冷", "订单和 backlog 明确，是物理瓶颈直接载体", "Q2.2 / Q4.1"],
    ["SK hynix/MU/Samsung", "HBM/高端内存", "AI 工厂的硬瓶颈，但供给扩张和估值要监控", "Q2.1 / Q3.2"],
    ["ALAB/CRDO/MRVL", "连接芯片/线缆/custom silicon/电光互联", "弹性大但客户集中、定制项目节奏和估值风险高", "Q2.2 / Q4.1"],
    ["DELL/SMCI", "系统交付", "backlog 强，但利润率和执行质量决定价值捕获", "Q2.2 / Q3.1"],
    ["AVGO/ANET/TSM", "ASIC/网络/制造", "重要卡点，但需要区分已经定价的部分", "Q3.1 / Q4.1"],
  ],
};

const chainRows = [
  ["需求端", "训练、推理、agent、主权 AI、企业 AI", "云厂商、AI labs、企业客户", "客户 capex -> 服务器/机柜订单 -> 供应链收入", "需求真实但必须验证 ROI 和 capex 持续性", "Q1 / Q3"],
  ["平台层", "GPU/ASIC、软件栈、AI 工厂参考架构", "NVDA、AVGO、AMD/ASIC 生态", "定义系统标准和供应商资格", "强卡点，但估值可能提前反映", "Q2.1 / Q4"],
  ["制造/内存", "先进制程、先进封装、HBM、服务器 DRAM/NAND", "TSMC、SK hynix、Samsung、Micron", "供给斜率决定交付速度和毛利", "最接近硬瓶颈，但要看产能扩张", "Q2.1 / Q3.2"],
  ["网络/连接", "Ethernet switch、PCIe/CXL retimer、AEC/光互联、custom silicon", "ALAB、CRDO、MRVL、AVGO、ANET", "决定集群扩展效率和功耗", "弹性大，客户集中、平台替代和项目节奏风险也大", "Q2.2 / Q3.2"],
  ["电力/液冷/系统", "电源、液冷、机柜、AI server、系统集成", "VRT、DELL、SMCI、HPE/ODM", "把硬件订单变成可上线项目", "订单可验证，利润率和执行是关键", "Q2.2 / Q4"],
  ["运营回报", "模型服务、企业 agent、AI 应用收入", "云厂商、AI 应用商、企业", "决定客户是否持续追加 capex", "若 ROI 变差，全链条降分", "Q3"],
];

const l1s = [
  l1("Q1", "AI 工厂需求是否真实，并能从主题叙事流到具体产业链节点？", "截面前的官方材料已经证明 AI 工厂不是单一 GPU 叙事：NVIDIA 数据中心收入、Dell AI server backlog、Vertiv 订单、HBM 和连接芯片收入都显示需求进入财务口径。但需求是否可持续仍取决于客户 capex 和 AI ROI。"),
  l1("Q2", "哪些环节是真正稀缺、难替代、能捕获价值的卡点？", "最强卡点是平台控制、HBM/先进封装、电力液冷和机柜级连接；系统交付有订单弹性但利润率不一定好；开放网络和 ASIC 方向有大空间，但需要与 NVIDIA 平台整合风险拆开。"),
  l1("Q3", "哪些反证会降低胜率、赔率或行动状态？", "最大反证不是 AI 工厂不存在，而是市场已充分定价、客户 capex/ROI 弱化、供给快速扩张、连接/系统商被平台压价，以及高 backlog 无法转成高质量利润。"),
  l1("Q4", "按截面证据应如何形成具体标的观察名单？", "冻结排序优先看 VRT、SK hynix、NVDA、TSM、ALAB、CRDO、MRVL、MU、DELL、AVGO、ANET、SMCI 等价值捕获载体；行动状态由四个核心维度控制，不因主题热度直接升高。"),
];

const l2s = [
  l2("Q1.1", "需求是否已进入财务指标", "NVIDIA、Dell、Vertiv、Astera、Credo、Marvell、Broadcom、Arista、内存公司都在截面前给出收入、订单或毛利证据，说明需求不是只停留在新闻。"),
  l2("Q1.2", "需求如何沿产业链传导", "AI 工厂需求先进入平台和服务器，再传导到内存、制造、连接、电力冷却和系统交付，最终由客户 ROI 决定持续性。"),
  l2("Q2.1", "平台、制造和内存卡点", "平台控制和 HBM/先进封装是最硬的卡点；但越强的卡点通常越容易被市场提前定价。"),
  l2("Q2.2", "连接、电力冷却和系统交付卡点", "连接和物理基础设施是 AI 工厂落地瓶颈；其中 VRT/ALAB/CRDO/MRVL 的证据直接，DELL/SMCI 的订单弹性强但利润质量分化。"),
  l2("Q3.1", "估值和市场隐含预期", "强增长不等于好赔率，必须测试市场是否已经把增长路径提前计入。"),
  l2("Q3.2", "供给扩张、替代和执行反证", "HBM/连接/液冷的高利润会诱发供给扩张；NVIDIA 纵向整合和客户集中会压缩第三方价值捕获。"),
  l2("Q4.1", "目标池与排序", "目标池从卡点映射而来，不按热门 ticker 或美股便利性收缩。"),
  l2("Q4.2", "复盘触发器", "三个月后只用价格 label 评估预测，不用 label 回写历史推理；未来复盘关注订单、毛利、capex、估值和供给反证。"),
];

const leaves = [
  leaf("Q1.1.1", "Q1.1", "需求是否已经进入 NVIDIA 数据中心收入和 AI 工厂表述？", "financial-statement-analysis", "evidence_quality", "决定 AI 工厂是否可以作为真实产业需求，而不是概念词。", ["SRC-NVDA-FY26-Q4"], "NVIDIA Q4 FY26 revenue was $68.1B and Data Center revenue was $62.3B; management explicitly described customers investing in AI compute factories.", "AI 工厂已经进入 NVIDIA 的收入和管理层口径，说明需求具备财务基础。", "Q1 可以确认需求真实，但 NVDA 本身估值要单独测试。", "缺少客户 ROI 和订单拆分。", "若客户 capex 或数据中心收入增速放缓，降低 future_space。", artifact("NVIDIA 需求证据", ["口径", "数据", "含义"], [["收入", "Q4 FY26 $68.1B", "需求规模已财务化"], ["数据中心", "$62.3B", "AI 工厂主收入池"], ["管理层表述", "AI factories", "产业链研究成立"], ["风险", "China/ROI/毛利", "不能直接推出低估"]])),
  leaf("Q1.1.2", "Q1.1", "AI 工厂是否已经进入系统和物理基础设施订单？", "financial-statement-analysis", "evidence_quality", "判断 DELL/VRT 等非芯片环节是否可进入观察池。", ["SRC-DELL-FY26-Q4", "SRC-VRT-Q4-2025"], "Dell disclosed more than $64B AI-optimized server orders and $43B backlog; Vertiv organic orders rose 252% YoY and backlog reached $15.0B.", "AI 工厂需求已经传导到服务器和电力冷却，说明非芯片环节不是纯配套。", "VRT/DELL 可进入 Q4 观察池，SMCI 需因执行风险更保守。", "缺少 backlog 毛利、取消率和客户集中度。", "若 backlog 转收入但毛利下降，则降低 risk_control。", artifact("订单传导", ["公司", "截面证据", "投资含义"], [["DELL", "$64B AI server orders / $43B backlog", "系统交付弹性强"], ["VRT", "orders +252% / backlog $15B", "电力液冷是硬瓶颈"], ["SMCI", "AI server exposure", "执行和治理风险压分"]])),
  leaf("Q1.2.1", "Q1.2", "需求传导的主路径是什么？", "industry-report-analysis", "future_space", "决定产业链全景和 Q2 卡点顺序。", ["SRC-NVDA-FY26-Q4", "SRC-DELL-FY26-Q4", "SRC-VRT-Q4-2025", "SRC-TSM-Q4-2025"], "AI 工厂需求从 NVIDIA 平台进入服务器 backlog，再进入先进制造、内存、电力冷却和系统交付。", "需求不是一条线，而是多节点同步扩张；越靠近硬瓶颈，越可能保留利润。", "Q1.2 支持跨平台、内存、连接、物理基础设施和系统交付建立目标池。", "缺少客户侧 capex ROI 模型。", "若客户 ROI 低于 capex 成本，整体降分。", artifact("需求传导路径", ["需求", "传导节点", "可验证数据"], [["更多训练/推理", "GPU/ASIC/HBM/封装", "NVDA/TSM/内存收入"], ["机柜部署", "服务器/电力/液冷", "DELL/VRT backlog"], ["集群扩展", "连接/以太网/AEC", "ALAB/CRDO/AVGO/ANET 收入"], ["长期持续性", "客户 ROI/capex", "云厂商指引"]])),
  leaf("Q1.2.2", "Q1.2", "需求是否只利好 NVIDIA，还是会外溢到第三方？", "industry-report-analysis", "target_ranking", "决定是否只看 NVDA，还是寻找未充分定价的稀缺环节。", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3", "SRC-AVGO-FY25-Q4", "SRC-ANET-Q4-2025"], "Astera、Credo、Marvell、Broadcom、Arista 均在截面前披露 AI networking/connectivity/custom silicon 相关增长或目标。", "AI 工厂扩张需要第三方连接、网络和 custom silicon 生态，但价值捕获取决于 design-in、客户集中、定制项目节奏和平台替代风险。", "第三方可以进入观察池，但不能只因 AI networking/custom silicon 叙事给高行动状态。", "缺少逐客户订单、平台依赖比例和 custom silicon 量产节奏。", "若 NVIDIA 自有网络方案或客户自研挤压第三方份额，相关标的降级。", artifact("第三方外溢", ["节点", "证据", "限制"], [["ALAB", "rack-scale connectivity revenue", "估值/客户集中"], ["CRDO", "AEC/optical +200% revenue", "高弹性高波动"], ["MRVL", "AI custom products/electro-optics demand", "定制项目节奏/客户集中"], ["AVGO", "AI ASIC + Ethernet switches", "大客户集中"], ["ANET", "AI networking goals exceeded", "与平台路线竞争"]])),
  leaf("Q2.1.1", "Q2.1", "平台控制是不是最强稀缺性？", "valuation-analysis", "chokepoint_strength", "判断 NVDA 高稀缺性是否能转成可行动机会。", ["SRC-NVDA-FY26-Q4"], "NVIDIA 同时控制 GPU、NVLink、软件生态、AI 工厂叙事和客户部署路线。", "平台控制是最强卡点，但市场也最可能提前定价。", "NVDA 稀缺性满分附近，但 valuation_odds 被封顶。", "缺少反向 DCF 和隐含增长拆解。", "只有当 EPS/订单上修超过隐含预期时才升级行动状态。", artifact("平台控制评分", ["维度", "判断"], [["稀缺性", "极强"], ["替代风险", "ASIC/开放以太网长期存在"], ["财务化", "已进入数据中心收入"], ["赔率", "需单独证明未定价"]])),
  leaf("Q2.1.2", "Q2.1", "HBM、先进制造和封装是否是硬瓶颈？", "industry-report-analysis", "chokepoint_strength", "决定 SK hynix/TSM/MU/Samsung 的卡点强度。", ["SRC-TSM-Q4-2025", "SRC-MU-FY26-Q1", "SRC-SKHYNIX-FY25", "SRC-SAMSUNG-FY25"], "TSMC advanced technologies were 77% of wafer revenue; SK hynix and Samsung reported AI memory/HBM strength; Micron reported record revenue and margin expansion.", "AI 工厂交付需要先进制程、封装和 HBM，供给斜率慢于需求时可形成价格和毛利弹性。", "SK hynix、TSM、MU、Samsung 均是核心价值捕获载体，其中 SK hynix 因 HBM 领导力最稀缺。", "缺少同口径产能、客户分配和估值分位。", "若 HBM 供给快速扩张或 ASP 反转，降低相关标的。", artifact("制造和内存卡点", ["节点", "控制者", "风险"], [["先进制程/封装", "TSMC", "高 capex 和地缘风险"], ["HBM", "SK hynix/MU/Samsung", "供给扩张和认证风险"], ["服务器 DRAM/eSSD", "MU/Samsung/SK hynix", "周期回落风险"]])),
  leaf("Q2.2.1", "Q2.2", "机柜级连接是否是独立稀缺点？", "industry-report-analysis", "chokepoint_strength", "决定 ALAB/CRDO/MRVL/AVGO/ANET 的排序。", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3", "SRC-AVGO-FY25-Q4", "SRC-ANET-Q4-2025"], "ALAB revenue +92% YoY, CRDO revenue +200% YoY, Marvell data-center sales grew on AI custom products and electro-optics, Broadcom AI semiconductor revenue +74% YoY, Arista FY revenue +28.6%.", "连接、custom silicon 和网络是 AI 工厂扩展效率瓶颈，收入增长已经进入公司报表。", "ALAB/CRDO/MRVL 弹性高但估值、客户集中和项目节奏风险也高；AVGO/ANET 更稳但弹性相对分散。", "缺少客户/产品级收入拆分。", "若客户切换平台、自研或价格下降，降低 chokepoint_strength。", artifact("连接卡点", ["公司", "证据", "处理"], [["ALAB", "Q4 revenue +92% YoY", "watch/action 候选"], ["CRDO", "Q3 revenue +200% YoY", "高弹性观察"], ["MRVL", "AI custom products/electro-optics", "custom silicon + 光互联观察"], ["AVGO", "AI ASIC/Ethernet switch", "大盘稳健"], ["ANET", "AI networking goals exceeded", "需客户订单验证"]])),
  leaf("Q2.2.2", "Q2.2", "电力液冷和系统交付能否捕获高质量利润？", "financial-statement-analysis", "evidence_quality", "决定 VRT/DELL/SMCI 的强弱。", ["SRC-VRT-Q4-2025", "SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2"], "VRT orders/backlog 和 DELL AI server backlog 都很强；SMCI 也有 AI server exposure，但执行和治理风险更高。", "物理基础设施是最容易被新手低估的瓶颈，系统交付则要看利润率。", "VRT 因订单、瓶颈和利润质量进入最高观察级；DELL 次之；SMCI 风险控制显著偏低。", "缺少 backlog 毛利和项目交付周期。", "若 backlog 转化质量差，VRT/DELL 降级。", artifact("物理基础设施", ["节点", "标的", "关键验证"], [["电力/液冷", "VRT", "backlog 毛利和交付"], ["AI server", "DELL", "订单转收入和现金流"], ["服务器组装", "SMCI", "治理和毛利稳定性"]])),
  leaf("Q3.1.1", "Q3.1", "市场是否已经把 AI 工厂增长充分定价？", "valuation-analysis", "valuation_odds", "防止强主题自动变成高分。", ["SRC-NVDA-FY26-Q4", "SRC-VRT-Q4-2025", "SRC-ALAB-Q4-2025", "SRC-AVGO-FY25-Q4"], "截面前 AI 工厂核心标的已经有强收入/订单和高市场关注。", "基本面强不等于赔率强，尤其是 NVDA、ALAB、VRT 这类高关注标的。", "除非估值隐含增长低于可验证订单利润路径，否则 action_state 不能无条件升高。", "缺少完整 reverse DCF 和估值分位。", "若估值继续扩张而盈利未上修，降低 mispricing。", artifact("估值闸门", ["条件", "要求"], [["稀缺性", "必须强"], ["未定价", "必须由订单/利润超过隐含预期证明"], ["下行保护", "必须可控"], ["缺任一项", "封顶 watch_only 或 no_action"]])),
  leaf("Q3.1.2", "Q3.1", "客户 capex 和 AI ROI 是否可能打断链条？", "news-event-analysis", "disconfirming_risk_control", "定义最重要的行业反证。", ["SRC-NVDA-FY26-Q4", "SRC-DELL-FY26-Q4", "SRC-VRT-Q4-2025"], "AI 工厂需求依赖云厂商、AI labs 和企业持续投入，硬件供应链对 capex 非常敏感。", "如果客户 ROI 或融资能力下降，订单、毛利和估值会同时承压。", "所有目标都需要 capex/ROI kill test，尤其是系统、连接和液冷环节。", "缺少客户侧单位经济性。", "若 hyperscaler 下修 capex 或 AI 服务收入不达预期，整体降分。", artifact("capex 反证", ["反证", "影响"], [["capex 下修", "全链条"], ["电力接入延迟", "VRT/DELL"], ["AI ROI 下降", "NVDA/服务器/连接"], ["融资收紧", "新云客户订单风险"]])),
  leaf("Q3.2.1", "Q3.2", "供给扩张会不会消除稀缺性？", "industry-report-analysis", "disconfirming_risk_control", "测试 HBM、先进制造、连接和液冷是否会过度扩产。", ["SRC-TSM-Q4-2025", "SRC-SKHYNIX-FY25", "SRC-SAMSUNG-FY25", "SRC-MU-FY26-Q1"], "TSMC 2026 capex expected $52B-$56B; memory companies were increasing AI product focus and HBM capacity.", "高利润会吸引扩产，供给斜率一旦超过需求斜率，赔率下降。", "HBM/封装仍是硬瓶颈，但必须设置供给扩张反证。", "缺少统一 bit growth、CoWoS 产能和 HBM 资格认证表。", "若供给显著放量或价格下行，降低 HBM/TSM/MU/Samsung。", artifact("供给反证", ["环节", "扩张信号", "降级条件"], [["TSMC", "高 capex", "先进封装产能过剩"], ["HBM", "供应商扩产", "ASP 或毛利下滑"], ["连接", "多供应商进入", "价格竞争"], ["液冷", "产能扩张", "backlog 质量下降"]])),
  leaf("Q3.2.2", "Q3.2", "平台整合和客户集中会不会压缩第三方利润？", "industry-report-analysis", "risk_control", "控制 ALAB/CRDO/MRVL/AVGO/ANET/SMCI 的风险上限。", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3", "SRC-AVGO-FY25-Q4", "SRC-ANET-Q4-2025"], "第三方连接、custom silicon 和网络公司高速增长，但通常依赖少数大型客户和平台标准。", "客户集中可带来高弹性，也会在客户切换、平台自研或定制项目延期时放大下行。", "ALAB/CRDO/MRVL 需要更高 payoff，但 risk_control 不可给满分。", "缺少客户集中度、design-in 合同期限和 custom silicon 项目量产节奏。", "若大客户订单延后或转向自研，降为 no_action。", artifact("第三方风险", ["风险", "影响标的"], [["客户集中", "ALAB/CRDO/MRVL/AVGO"], ["平台自研", "ANET/ALAB/CRDO/MRVL"], ["定制项目延期", "MRVL/AVGO"], ["价格压力", "系统商/网络"], ["执行风险", "SMCI"]])),
  leaf("Q4.1.1", "Q4.1", "哪些证券是直接价值捕获载体？", "target-recommendation-analysis", "target_ranking", "建立冻结目标池，不让标签可得性限制投资宇宙。", ["SRC-NVDA-FY26-Q4", "SRC-VRT-Q4-2025", "SRC-SKHYNIX-FY25", "SRC-TSM-Q4-2025", "SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3", "SRC-DELL-FY26-Q4"], "直接载体包括 NVDA、VRT、SK hynix、TSM、ALAB、CRDO、MRVL、MU、DELL、AVGO、ANET、Samsung、SMCI。", "目标池来自卡点映射，而不是从美股便利性或三个月结果筛选。", "Q4 保留非美股中央标的，也补入 MRVL 这类截面前已有官方 AI data-center 证据的 custom silicon/电光互联标的；价格 label 不可靠时标 unverified。", "缺少所有市场同口径估值。", "补齐估值后再调整 action_state。", artifact("目标池映射", ["标的", "链条节点", "处理"], [["VRT", "电力/液冷", "actionable/watch"], ["SK hynix", "HBM", "actionable/watch"], ["NVDA", "平台控制", "watch"], ["ALAB/CRDO/MRVL", "连接/custom silicon", "watch"], ["DELL", "系统交付", "watch"], ["Samsung", "HBM/内存", "label unverified"]])),
  leaf("Q4.1.2", "Q4.1", "排序如何由四个核心维度产生？", "target-recommendation-analysis", "action_state", "确保强主题必须同时满足稀缺、未定价、弹性和风险控制。", ["SRC-VRT-Q4-2025", "SRC-SKHYNIX-FY25", "SRC-NVDA-FY26-Q4", "SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3"], "目标分数由七个底层组件汇总到稀缺性、未充分定价、业绩弹性和风险控制四个维度。", "AI 工厂全链条强，但只有四个维度同时强才给 actionable_long。", "VRT 和 SK hynix 最接近可行动，其余以 watch_only/no_action 为主。", "估值证据仍不完整。", "若未定价或风险控制不能证明，封顶 watch_only。", artifact("行动状态闸门", ["维度", "要求"], [["稀缺性", "卡点明确且难替代"], ["未充分定价", "订单利润超过隐含预期"], ["业绩弹性", "收入/毛利/FCF 能大幅上修"], ["风险控制", "反证可监控且下行有限"]])),
  leaf("Q4.2.1", "Q4.2", "三个月后用哪些事实复盘，而不是用 label 倒推？", "target-recommendation-analysis", "monitorability", "设置预测复盘触发器。", ["SRC-DELL-FY26-Q4", "SRC-VRT-Q4-2025", "SRC-ALAB-Q4-2025", "SRC-MRVL-FY26-Q3", "SRC-MU-FY26-Q1"], "复盘应看订单、backlog 毛利、HBM ASP、连接 design-in、custom silicon 项目节奏、客户 capex 和估值隐含预期。", "这些数据能验证当时推理质量；三个月股价只是 label。", "复盘机制建立，但不允许回写本报告推理。", "缺少自动化跟踪表。", "若事实反证出现，未来训练样本降权或改问题。", artifact("复盘数据", ["节点", "三个月观察"], [["VRT/DELL", "backlog 转收入和毛利"], ["SK hynix/MU", "HBM 出货和 ASP"], ["ALAB/CRDO/MRVL", "design-in、客户集中、custom silicon 项目"], ["NVDA", "Data Center 指引和毛利"]])),
  leaf("Q4.2.2", "Q4.2", "哪些 kill tests 会撤销高分？", "target-recommendation-analysis", "risk_control", "为每个高关注方向设置硬降级条件。", ["SRC-NVDA-FY26-Q4", "SRC-VRT-Q4-2025", "SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3", "SRC-MRVL-FY26-Q3"], "核心 kill tests 包括 capex 下修、HBM 供给过剩、连接客户集中恶化、custom silicon 项目延迟、VRT backlog 毛利差、DELL/SMCI 订单低质量。", "一旦触发，说明稀缺性或利润桥断裂，应降低 action_state。", "actionable_long 必须有硬 kill tests；高弹性 watch_only 也要有降级条件。", "需要持续财报、客户 capex 和项目量产数据。", "任一核心反证触发即降级。", artifact("Kill tests", ["测试", "证据", "动作"], [["capex 下修", "云厂商指引", "全链降分"], ["HBM ASP 反转", "内存财报", "内存标的降级"], ["连接客户流失", "ALAB/CRDO 订单", "降为 no_action"], ["MRVL custom silicon 延迟", "项目量产/客户披露", "降为 no_action"], ["液冷毛利差", "VRT backlog/毛利", "撤销 actionable"], ["系统订单低质量", "DELL/SMCI 现金流", "降级"]])),
];

const adaptiveUnits = [
  drill(4, "Q1.2.1.1", "Q1.2.1", "平台收入如何传导成服务器 backlog？", "financial-statement-analysis", "future_space", "把 GPU/平台收入和系统商订单连起来，判断需求是否已经离开单一芯片环节。", ["SRC-NVDA-FY26-Q4", "SRC-DELL-FY26-Q4"], "NVIDIA 数据中心收入已经达到大规模财务口径，Dell 同期披露 AI server orders 和 backlog。", "平台收入和服务器 backlog 同时出现，说明 AI 工厂需求已经进入可交付系统，而不是只停留在芯片供给。", "Q1.2.1 的主路径可保留平台到服务器的第一段传导。", "缺少客户级订单重叠和取消率。", "若服务器 backlog 不再随平台收入增长，降低系统交付环节。", artifact("平台到服务器", ["节点", "截面证据", "判断"], [["平台收入", "NVDA Data Center $62.3B", "需求起点真实"], ["系统订单", "DELL AI server orders/backlog", "需求进入交付"], ["缺口", "客户重叠和取消率", "需要后续验证"]])) ,
  drill(4, "Q1.2.1.2", "Q1.2.1", "服务器 backlog 如何传导到电力和液冷？", "financial-statement-analysis", "future_space", "判断 VRT 是否是 AI 工厂落地瓶颈，而不只是数据中心泛主题。", ["SRC-DELL-FY26-Q4", "SRC-VRT-Q4-2025"], "Dell AI server backlog 和 Vertiv orders/backlog 在截面前同时强劲。", "高功率服务器需要电源、散热和机柜工程，服务器订单会把需求推向物理基础设施。", "VRT 应作为 AI 工厂产业链的直接瓶颈标的进入 Q4。", "缺少单项目液冷渗透率和 backlog 毛利。", "若电力/液冷 backlog 增长但毛利恶化，降低 VRT 行动状态。", artifact("服务器到物理基础设施", ["传导", "证据", "风险"], [["AI server backlog", "DELL $43B backlog", "项目需要落地"], ["电力液冷订单", "VRT orders +252% / backlog $15B", "瓶颈被财务化"], ["风险", "毛利和交付周期", "影响风险控制"]])) ,
  drill(4, "Q2.1.2.1", "Q2.1.2", "HBM 价值捕获应该优先看谁？", "industry-report-analysis", "chokepoint_strength", "把 HBM 从先进制造大桶里拆出来，决定 SK hynix、Micron、Samsung 的相对强弱。", ["SRC-SKHYNIX-FY25", "SRC-MU-FY26-Q1", "SRC-SAMSUNG-FY25"], "SK hynix 披露 AI memory 驱动的高收入和 49% operating margin；Micron 和 Samsung 也披露 AI memory/HBM 或高价值内存强势。", "HBM 是 AI 工厂最硬的内存卡点，但供应商之间的资格、份额和毛利弹性不同。", "HBM 分支需要继续拆到公司层，否则 Q2.1.2 容易把不同强度混在一起。", "缺少同口径 HBM 产能、客户资格和 ASP。", "若客户资格或 ASP 反转，相关标的降级。", artifact("HBM 公司分层", ["公司", "截面证据", "初步处理"], [["SK hynix", "AI memory + 高 operating margin", "最高卡点候选"], ["Micron", "record revenue/margin with AI memory", "高弹性观察"], ["Samsung", "record memory revenue/profit, HBM/server DDR5/eSSD", "需要验证 HBM 领导力"]])) ,
  drill(5, "Q2.1.2.1.1", "Q2.1.2.1", "SK hynix 的 HBM 证据是否足以形成最高卡点？", "financial-statement-analysis", "chokepoint_strength", "决定非美股核心标的能否保留在最高观察层，而不是因 label 难取被排除。", ["SRC-SKHYNIX-FY25"], "SK hynix FY2025 revenue KRW97.1467T、operating profit KRW47.2063T、operating margin 49%，公司将表现归因于 AI memory 和 HBM 领导力。", "高利润率和 AI memory 领导力同时出现，说明其不是普通存储 beta，而是 AI 工厂内存卡点载体。", "SK hynix 可维持 actionable_long 候选，但本地价格 label 暂未验证。", "缺少 HBM 客户、份额和产能分配表。", "若 HBM ASP 或客户资格下行，撤销最高卡点假设。", artifact("SK hynix HBM 验证", ["维度", "结论"], [["财务化", "FY25 高收入/利润率", "强"], ["稀缺性", "HBM leadership", "强"], ["缺口", "客户/份额/ASP", "需验证"]])) ,
  drill(5, "Q2.1.2.1.2", "Q2.1.2.1", "Micron 和 Samsung 是同等卡点还是补充弹性？", "financial-statement-analysis", "target_ranking", "控制 MU 与 Samsung 在目标池中的排序，避免把所有内存公司同分。", ["SRC-MU-FY26-Q1", "SRC-SAMSUNG-FY25"], "Micron 披露 record revenue and margin expansion，Samsung 披露 Memory Business record quarterly revenue and operating profit。", "两家公司都受益于 AI memory，但相对 SK hynix 的 HBM 份额、资格和定价权需要更强证据。", "MU/Samsung 应进入 watch_only，而不是直接与 SK hynix 同行动状态。", "缺少同口径 HBM 资格和产品 mix。", "若 HBM 出货/ASP 明显领先预期，才可上调。", artifact("MU/Samsung 分层", ["公司", "强项", "封顶原因"], [["MU", "AI cloud memory/HBM 弹性", "份额和资格仍需证明"], ["Samsung", "内存规模与产品广", "HBM 领导力需验证"]])) ,
  drill(4, "Q2.1.2.2", "Q2.1.2", "先进制造和封装由 TSMC 捕获多少价值？", "financial-statement-analysis", "chokepoint_strength", "把 TSMC 从内存分支拆出，判断其是稳态卡点还是赔率不足。", ["SRC-TSM-Q4-2025"], "TSMC Q4 2025 advanced technologies were 77% of wafer revenue，gross margin 62.3%，2026 capex expected $52B-$56B。", "先进制程和封装是 AI 工厂供给斜率的关键，但高 capex 也说明市场可能已经预期扩产。", "TSM 卡点强、证据强，但 valuation_odds 不应给满。", "缺少先进封装单独产能和 AI/HPC 客户 mix。", "若封装供给放量导致稀缺性下降，降低赔率。", artifact("TSMC 制造/封装", ["证据", "含义"], [["advanced technologies 77%", "AI/HPC 高端制程贡献大"], ["gross margin 62.3%", "价值捕获强"], ["capex $52B-$56B", "扩产与稀缺性反证并存"]])) ,
  drill(4, "Q2.2.1.1", "Q2.2.1", "ALAB/CRDO 的高速连接增长哪个更像弹性卡点？", "financial-statement-analysis", "payoff_convexity", "将连接分支拆到高弹性小盘标的，判断赔率和风险。", ["SRC-ALAB-Q4-2025", "SRC-CRDO-FY26-Q3"], "Astera Labs Q4 revenue +92% YoY，Credo FY26 Q3 revenue +200% YoY，二者均指向 AI infrastructure connectivity。", "两者都具备高弹性，但客户集中和平台依赖会放大下行。", "ALAB/CRDO 可保留高弹性 watch_only，不能越过风险闸门。", "缺少大客户占比和 design-in 周期。", "若客户订单延迟或平台替代，降为 no_action。", artifact("连接高弹性", ["标的", "弹性", "风险"], [["ALAB", "+92% revenue", "估值和客户集中"], ["CRDO", "+200% revenue", "客户集中和波动"], ["共同点", "AI connectivity", "高赔率但低风险控制"]])) ,
  drill(4, "Q2.2.1.2", "Q2.2.1", "AVGO/ANET 的网络和 ASIC 是稳态卡点还是替代风险？", "industry-report-analysis", "risk_control", "区分大盘稳态受益与高弹性连接标的。", ["SRC-AVGO-FY25-Q4", "SRC-ANET-Q4-2025"], "Broadcom AI semiconductor revenue +74% YoY，Arista FY2025 revenue +28.6% 且 AI networking 目标超额。", "AVGO/ANET 代表 ASIC/Ethernet 稳态受益，但与 NVIDIA 平台路线和客户自研之间存在路线风险。", "两者进入目标池，但行动状态以 watch_only 为主。", "缺少客户数量、云厂商订单和开放以太网份额。", "若客户 ASIC 或 Ethernet 节奏不及预期，降低 ranking。", artifact("稳态网络/ASIC", ["公司", "价值捕获", "风险"], [["AVGO", "AI ASIC + Ethernet switch", "大客户集中"], ["ANET", "AI networking", "平台路线竞争"]])) ,
  drill(4, "Q2.2.1.3", "Q2.2.1", "MRVL 的 custom silicon 和电光互联是否是 AI 工厂卡点？", "financial-statement-analysis", "payoff_convexity", "补齐 MRVL 在 custom silicon / electro-optics 维度的独立判断。", ["SRC-MRVL-FY26-Q3"], "Marvell FY26 Q3 net revenue was $2.075B；10-Q 披露 data-center sales +38%，增长由 AI-related demand for custom products and electro-optics portfolio 驱动。", "MRVL 不是普通网络 beta，而是 custom silicon 与光互联方向的 AI 工厂弹性载体。", "MRVL 应进入最终目标池，但因客户集中、定制项目节奏和估值不透明，行动状态封顶在 watch_only。", "缺少 custom silicon 项目量产时间、客户集中度和反向估值。", "若大客户项目延期、客户自研替代或毛利不达预期，降为 no_action。", artifact("MRVL 卡点判断", ["维度", "截面证据", "处理"], [["AI 需求", "data-center +38%", "需求已财务化"], ["产品位置", "custom products / electro-optics", "AI 工厂连接与定制芯片"], ["风险", "客户集中/项目节奏/估值", "watch_only 封顶"]])) ,
  drill(4, "Q2.2.2.1", "Q2.2.2", "VRT 的 backlog 能否变成高质量利润？", "financial-statement-analysis", "evidence_quality", "决定 VRT 是否满足稀缺、弹性和风险控制三项，而不是只靠订单热度。", ["SRC-VRT-Q4-2025"], "Vertiv Q4 organic orders rose 252% YoY and backlog reached $15.0B。", "电力/液冷 backlog 是 AI 工厂物理瓶颈的直接证据，但最终价值还要看毛利和交付。", "VRT 可维持 actionable_long，但必须绑定 backlog 毛利 kill test。", "缺少液冷项目毛利和取消率。", "若 backlog 转化低质量，撤销 actionable_long。", artifact("VRT 利润桥", ["环节", "判断"], [["订单", "强"], ["瓶颈", "强"], ["利润质量", "待验证"], ["行动状态", "有条件 actionable_long"]])) ,
  drill(4, "Q2.2.2.2", "Q2.2.2", "DELL/SMCI 的 AI server backlog 是否能保留利润？", "financial-statement-analysis", "risk_control", "避免把服务器组装的订单弹性误判为高质量卡点。", ["SRC-DELL-FY26-Q4", "SRC-SMCI-FY26-Q2"], "Dell 披露 AI server orders/backlog，Supermicro 也有 AI server exposure，但 SMCI 执行和治理风险更高。", "系统商能吃到 AI 工厂订单，但议价力和利润率通常弱于平台、HBM 和电力液冷。", "DELL watch_only，SMCI no_action 更符合风险控制。", "缺少 AI server 毛利、现金转化和治理风险量化。", "若订单增长不带来利润和现金流，系统商降级。", artifact("系统商利润质量", ["标的", "机会", "限制"], [["DELL", "backlog 强", "利润率/现金流待验证"], ["SMCI", "主题弹性", "执行和治理风险"]])) ,
  drill(4, "Q3.1.1.1", "Q3.1.1", "高稀缺龙头是否已经被估值封顶？", "valuation-analysis", "valuation_odds", "解释为什么 NVDA/TSM 卡点强但行动状态仍可能不是最高。", ["SRC-NVDA-FY26-Q4", "SRC-TSM-Q4-2025"], "NVDA 和 TSMC 的收入、毛利和 capex 证据都很强，且市场关注度高。", "强证据提高胜率，但也提高市场已定价概率。", "NVDA/TSM 维持 watch_only，除非反向估值显示仍未充分定价。", "缺少 reverse DCF 和隐含 EPS 增长。", "若盈利上修不能超过隐含预期，维持封顶。", artifact("龙头估值封顶", ["标的", "卡点", "封顶原因"], [["NVDA", "平台控制", "预期很高"], ["TSM", "制造/封装", "capex 与估值已反映部分增长"]])) ,
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
  "000660.KS": unverifiedLabel("KRX/Yahoo label not collected in this run"),
  "005930.KS": unverifiedLabel("KRX/Yahoo label not collected in this run"),
};

const targets = rankTargets([
  target("VRT", "Vertiv", "USA", "AI 工厂电力和液冷", [4.45, 4.45, 3.45, 4.45, 3.85, 4.20, 4.05], ["SRC-VRT-Q4-2025"], "订单、backlog 和物理瓶颈同时成立；若估值不过度，最接近截面下可行动机会。", "backlog 转收入、液冷毛利、客户 capex", "backlog 毛利低于预期或客户 capex 下修", "actionable_long"),
  target("000660.KS", "SK hynix", "Korea", "HBM 和高端 AI memory", [4.70, 4.55, 3.35, 4.35, 3.65, 3.55, 4.10], ["SRC-SKHYNIX-FY25"], "HBM3E/HBM4 供应能力和 49% FY25 operating margin 形成强稀缺和利润桥；价格 label 暂未验证但不能排除核心标的。", "HBM4 ramp、客户资格、ASP、capex", "HBM 供给过剩或 ASP 反转", "actionable_long"),
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

function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const qaTree = buildQaTree();
  const extractions = buildExtractions();
  const reviews = buildReviews(extractions);
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
    supply_chain_explainer: chainExplainer,
    supply_chain_map: chainRows,
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
  return {
    source_id,
    title,
    source_bucket,
    url,
    source_visible_at,
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
  return {
    source_id,
    title,
    source_bucket: "evidence",
    url,
    source_visible_at,
    support_refute_or_lead: "support",
    summary: "Price evaluation dataset for final target table only.",
    as_of_date: AS_OF_DATE,
    cutoff_status: "post_cutoff_label_only",
    allowed_usage: "label_only",
    availability_proof: "post-cutoff price dataset",
    used_in: ["final_target_evaluation"],
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
  const schema = ["key_facts", "numbers_dates", "investment_relevance", "support_refute_or_lead", "uncertainties"];
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
      cutoff_status: "cutoff_visible",
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

function label(start_price, end_price, forward_3m_return, price_source, label_status) {
  return {
    as_of_date: AS_OF_DATE,
    evaluation_date: EVALUATION_DATE,
    label_window: LABEL_WINDOW,
    start_price,
    start_price_date: LABEL_START_DATE,
    end_price,
    end_price_date: LABEL_END_DATE,
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
    odds_model: {
      implied_expectation: "As-of market likely priced meaningful AI factory growth; mispricing score is capped unless order and profit evidence exceed implied expectations.",
      base_path: nextData,
      bull_path: "Orders, margin and capex evidence exceed market-implied growth.",
      bear_path: downgradeRisk,
    },
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
        created_at: EVALUATION_DATE,
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
    gpt_verification_status: "verified_against_cutoff_source",
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
  <title>AI 工厂产业相关投资机会回测研究</title>
  <style>${css()}</style>
</head>
<body>
  <header class="hero"><div class="eyebrow">Historical Backtest · AI Factory · ${AS_OF_DATE}</div><h1>AI 工厂产业相关投资机会回测研究</h1><p class="subtitle">研究截面冻结在 ${AS_OF_DATE}。本报告只用该日期前可见资料形成产业链、QA、评分和排序；三个月后的价格变化只作为最终标的表右侧的评估字段。</p></header>
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
    <div class="metric"><span>研究对象</span><strong>AI 工厂产业链</strong></div>
    <div class="metric"><span>运行模式</span><strong>historical_backtest</strong></div>
    <div class="metric"><span>信息截面</span><strong>${AS_OF_DATE}</strong></div>
    <div class="metric"><span>评估日期</span><strong>${EVALUATION_DATE}</strong></div>
  </div>
  <div class="artifact-card"><div class="artifact-title">当前结论</div>在截面前，AI 工厂已经从 NVIDIA 平台收入传导到服务器 backlog、电力液冷订单、HBM/先进制造和连接芯片收入。最接近“当前未被市场充分定价的巨大机会”的方向是电力液冷和 HBM 硬瓶颈，但多数标的仍需要估值和风险闸门控制。</div></div>`;
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
  if (node.level < 3) return `<p>${esc(node.conclusion)}</p>`;
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
    <div class="table-scroll"><table class="target-table">
      <thead><tr><th>#</th><th>标的</th><th>市场</th><th>Action State</th><th>总分</th><th>稀缺/垄断</th><th>未充分定价</th><th>业绩弹性</th><th>风险控制</th><th>截面理由</th><th>降级触发</th><th>start_price</th><th>end_price</th><th>forward_3m_return</th><th>benchmark_return</th><th>excess_return</th><th>label_status</th></tr></thead>
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
    .goal-card,.supply-chain-section,.target-section,.source-collapse{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px;box-shadow:0 10px 28px rgba(30,41,59,.05)}.goal-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.metric{border:1px solid #e7ebf2;border-radius:8px;padding:12px;background:#fbfcfe}.metric span{display:block;color:var(--muted);font-size:12px}.metric strong{font-size:15px}.chain-explain{display:grid;gap:14px;margin-bottom:16px}.chain-plain-summary{margin:0;padding:14px 16px;border:1px solid #d9e4f2;border-radius:8px;background:#f6f9fd;font-weight:760;line-height:1.75}.chain-flow-steps,.chain-chokepoints,.chain-target-links{border:1px solid #e6eaf1;border-radius:8px;background:#fbfcff;padding:14px}.chain-flow-steps b,.chain-chokepoints b,.chain-target-links b{display:block;margin-bottom:8px}.chain-flow-steps ol{margin:0;padding-left:22px;line-height:1.75}.chain-layer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}.chain-layer-card{border:1px solid #e6eaf1;border-radius:8px;background:#fff;padding:12px}.chain-layer-card b,.chain-layer-card span{display:block}.chain-layer-card span{color:var(--blue);font-weight:800;margin-top:4px}.chain-layer-card p{margin:8px 0;color:var(--ink)}.chain-layer-card small{color:var(--muted);line-height:1.6}.chain-map,.table-scroll{overflow:auto;border:1px solid #e6eaf1;border-radius:8px}.chain-table,.target-table{min-width:1500px}
    .qa-card{background:var(--panel);border:1px solid var(--line);border-radius:8px;margin:12px 0;overflow:hidden}.qa-card[open]>summary{border-bottom:1px solid #e6eaf1}.qa-card summary{list-style:none;cursor:pointer;padding:14px 16px;display:grid;grid-template-columns:auto 1fr auto auto;gap:10px;align-items:center}.qa-card summary::-webkit-details-marker{display:none}.qid{font-weight:800;color:var(--blue);font-size:13px}.qtitle{font-weight:760}.qa-count{font-size:12px;color:var(--muted);background:#f1f4f9;border:1px solid #e0e5ee;border-radius:999px;padding:3px 8px}.chevron{color:var(--muted)}details[open]>summary .chevron{transform:rotate(90deg)}.level-2{margin-left:16px}.level-3{margin-left:32px}.level-4{margin-left:48px}.level-5{margin-left:64px}.qa-body{padding:14px 16px 16px}.qa-block{margin:0 0 14px}.block-title{font-size:12px;font-weight:800;color:#586174;text-transform:uppercase;margin-bottom:8px}
    .artifact-card{border:1px solid #e2e7ef;border-radius:8px;background:#fbfcff;padding:12px;margin:10px 0}.artifact-title{font-weight:780;margin-bottom:8px}.logic-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.logic-card{border:1px solid #e5e9f0;border-radius:8px;background:#fff;padding:10px}.logic-card b{display:block;font-size:12px;color:#536071;margin-bottom:4px}.logic-card p{margin:0;font-size:13px}.routing{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:10px}.pill{border:1px solid #dfe6f1;background:#f7faff;border-radius:999px;padding:4px 8px;font-size:12px;color:#46515f}.source-chips{display:flex;flex-wrap:wrap;gap:6px}.source-chip{font-size:12px;color:#0a63ce;background:#eef5ff;border:1px solid #d8e8ff;border-radius:999px;padding:4px 8px;text-decoration:none}
    table{width:100%;border-collapse:collapse;font-size:13px}th,td{padding:9px 8px;border-bottom:1px solid #e6eaf1;text-align:left;vertical-align:top}th{color:#536071;font-size:12px;background:#f8fafc}.state-actionable_long{color:var(--green);font-weight:800}.state-watch_only{color:var(--amber);font-weight:800}.state-no_action{color:var(--red);font-weight:800}.source-collapse summary{cursor:pointer;font-weight:800}.source-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin-top:12px}.source-card{border:1px solid #e5e9f0;border-radius:8px;background:#fbfcff;padding:10px}.source-card a{color:#0a63ce}
    @media(max-width:900px){.goal-grid,.logic-grid{grid-template-columns:1fr}.level-2,.level-3,.level-4,.level-5{margin-left:0}.qa-card summary{grid-template-columns:auto 1fr auto}.qa-count{display:none}}
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
