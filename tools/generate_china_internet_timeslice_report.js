const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const OUT_DIR = path.join(ROOT, "research", "qa_projects", "china_internet_timeslice_20260228");
const AS_OF_DATE = "2026-02-28";
const REPORT_DATE = "2026-05-30";

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
  {
    source_id: "SRC-NBS-ONLINE-2025",
    title: "National Bureau of Statistics: Total Retail Sales of Consumer Goods in December 2025",
    url: "https://www.stats.gov.cn/english/PressRelease/202601/t20260120_1962354.html",
    source_visible_at: "2026-01-20",
    source_bucket: "evidence",
    support_refute_or_lead: "support",
    allowed_usage: "thesis",
    used_in: ["Q1.1.1", "Q3.1.1"],
    summary: "2025 China online retail sales reached RMB15,972.2bn, up 8.6%; physical-goods online retail reached RMB13,092.3bn, up 5.2%.",
  },
  {
    source_id: "SRC-NBS-COMMUNIQUE-2025",
    title: "Statistical Communique of the People's Republic of China on 2025 National Economic and Social Development",
    url: "https://www.stats.gov.cn/english/PressRelease/202602/t20260228_1962661.html",
    source_visible_at: "2026-02-28",
    source_bucket: "evidence",
    support_refute_or_lead: "support",
    allowed_usage: "thesis",
    used_in: ["Q1.1.1", "Q1.2.1"],
    summary: "Physical-goods online retail was 26.1% of total retail sales; services retail grew faster than goods retail.",
  },
  {
    source_id: "SRC-TENCENT-Q3-2025",
    title: "Tencent Announces 2025 Third Quarter Results",
    url: "https://static.www.tencent.com/uploads/2025/11/13/a33b6f19738615834787623f17d20ba3.pdf",
    source_visible_at: "2025-11-13",
    source_bucket: "evidence",
    support_refute_or_lead: "support",
    allowed_usage: "thesis",
    used_in: ["Q1.2.1", "Q2.1.1", "Q3.2.1", "Q4.1.1"],
    summary: "3Q25 revenue RMB192.9bn, up 15%; marketing services up 21%; fintech/business services up 10%; non-IFRS operating profit up 18%.",
  },
  {
    source_id: "SRC-ALIBABA-SEP-2025",
    title: "Alibaba Group Announces September Quarter 2025 Results",
    url: "https://www.alibabagroup.com/en-US/document-1929990445136347136",
    source_visible_at: "2025-11-25",
    source_bucket: "evidence",
    support_refute_or_lead: "support",
    allowed_usage: "thesis",
    used_in: ["Q1.2.2", "Q2.2.1", "Q4.1.2"],
    summary: "September-quarter results were visible before cutoff; company narrative focused on AI + Cloud and consumption investment.",
  },
  {
    source_id: "SRC-JD-Q3-2025",
    title: "JD.com Announces Third Quarter 2025 Results",
    url: "https://ir.jd.com/news-releases/news-release-details/jdcom-announces-third-quarter-2025-results",
    source_visible_at: "2025-11-13",
    source_bucket: "evidence",
    support_refute_or_lead: "support",
    allowed_usage: "thesis",
    used_in: ["Q2.2.2", "Q3.2.2", "Q4.1.2"],
    summary: "3Q25 net revenue RMB299.1bn, up 14.9%; JD Retail operating margin 5.9%; group investment in new businesses compressed consolidated profit.",
  },
  {
    source_id: "SRC-MEITUAN-Q3-2025",
    title: "Meituan 2025 Third Quarter Results Announcement",
    url: "https://www.meituan.com/en-US/investor/results",
    source_visible_at: "2025-11-28",
    source_bucket: "evidence",
    support_refute_or_lead: "support",
    allowed_usage: "thesis",
    used_in: ["Q2.1.2", "Q3.1.2", "Q4.1.2"],
    summary: "Meituan reported Q3 revenue of about RMB95.5bn and annual transacting users above 800m; competition and investment intensity remain key boundaries.",
  },
  {
    source_id: "SRC-PDD-Q3-2025",
    title: "PDD Holdings Announces Third Quarter 2025 Unaudited Financial Results",
    url: "https://investor.pddholdings.com/news-releases/news-release-details/pdd-holdings-announces-third-quarter-2025-unaudited-financial",
    source_visible_at: "2025-11-18",
    source_bucket: "evidence",
    support_refute_or_lead: "refute",
    allowed_usage: "thesis",
    used_in: ["Q3.1.2", "Q4.1.2"],
    summary: "Revenue grew 9%; management flagged moderating growth, competitive changes, external uncertainty, and future ecosystem investments.",
  },
  {
    source_id: "SRC-BAIDU-Q4-2025",
    title: "Baidu Announces Fourth Quarter and Fiscal Year 2025 Results",
    url: "https://ir.baidu.com/news-releases/news-release-details/baidu-announces-fourth-quarter-and-fiscal-year-2025-results/",
    source_visible_at: "2026-02-26",
    source_bucket: "evidence",
    support_refute_or_lead: "lead",
    allowed_usage: "thesis",
    used_in: ["Q1.2.2", "Q2.2.1", "Q3.2.2", "Q4.1.2"],
    summary: "AI Cloud Infra FY2025 revenue was about RMB20bn, up 34%; Q4 AI accelerator infrastructure subscription revenue up 143%; legacy business still weighed on reported results.",
  },
  {
    source_id: "SRC-NETEASE-Q4-2025",
    title: "NetEase Announces Fourth Quarter and Fiscal Year 2025 Unaudited Financial Results",
    url: "https://ir.netease.com/node/15256",
    source_visible_at: "2026-02-11",
    source_bucket: "evidence",
    support_refute_or_lead: "support",
    allowed_usage: "thesis",
    used_in: ["Q2.1.1", "Q3.2.2", "Q4.1.2"],
    summary: "Q4 net revenue RMB27.5bn, up 3.0%; games and related value-added services revenue RMB22.0bn, up 3.4%.",
  },
  {
    source_id: "SRC-TRIP-Q4-2025",
    title: "Trip.com Group Reports Unaudited Fourth Quarter and Full Year 2025 Financial Results",
    url: "https://investors.trip.com/news-releases/news-release-details/tripcom-group-limited-reports-unaudited-fourth-quarter-and-5",
    source_visible_at: "2026-02-25",
    source_bucket: "evidence",
    support_refute_or_lead: "support",
    allowed_usage: "thesis",
    used_in: ["Q1.1.2", "Q2.1.2", "Q4.1.2"],
    summary: "Q4 accommodation revenue grew 21%; FY2025 attributable net income was RMB33.3bn versus RMB17.1bn in 2024.",
  },
  {
    source_id: "SRC-KUAISHOU-Q3-2025",
    title: "Kuaishou Technology Announces Third Quarter 2025 Unaudited Financial Results",
    url: "https://ir.kuaishou.com/news-releases/news-release-details/kuaishou-technology-announces-third-quarter-2025-unaudited/",
    source_visible_at: "2025-11-19",
    source_bucket: "evidence",
    support_refute_or_lead: "lead",
    allowed_usage: "thesis",
    used_in: ["Q1.2.1", "Q2.1.2", "Q4.1.2"],
    summary: "Q3 DAU 416.2m, MAU 731.1m, e-commerce GMV RMB385.0bn, revenue RMB35.6bn, adjusted EBITDA RMB7.7bn.",
  },
  {
    source_id: "LBL-NASDAQ-ADR",
    title: "Nasdaq historical quote API for ADR close prices",
    url: "https://api.nasdaq.com/api/quote/BABA/historical?assetclass=stocks&fromdate=2026-02-25&todate=2026-05-30&limit=9999",
    source_visible_at: "2026-05-28",
    source_bucket: "evidence",
    support_refute_or_lead: "lead",
    allowed_usage: "label_only",
    used_in: ["final_label"],
    summary: "Close-price data used only for final outcome columns.",
  },
  {
    source_id: "LBL-STOCKANALYSIS-HK",
    title: "StockAnalysis historical pages for Hong Kong close prices",
    url: "https://stockanalysis.com/quote/hkg/0700/history/",
    source_visible_at: "2026-05-29",
    source_bucket: "evidence",
    support_refute_or_lead: "lead",
    allowed_usage: "label_only",
    used_in: ["final_label"],
    summary: "Close-price data used only for final outcome columns.",
  },
];

const qaNodes = [
  node("Q1", 1, null, "Q1 需求是否足够真实且仍有增量空间？",
    "结论：行业需求不是单一高增长故事，而是存量互联网入口、线上零售、服务消费和 AI 应用四条线分化。值得研究的不是泛互联网 beta，而是能把既有入口或交易网络迁移到高频新需求的公司。",
    "待验证：AI 应用活跃用户是否能稳定转化为付费或广告库存；服务消费复苏是否能抵消商品电商增速下台阶。",
    ["Q1.1", "Q1.2"],
    "互联网普及与线上零售显示需求基座仍大，但增速不支持无差别多头。"
  ),
  node("Q1.1", 2, "Q1", "Q1.1 消费互联网的总需求基座还有多大？",
    "结论：线上零售和服务消费仍是大盘，但增速已经进入中速区间；这要求投资逻辑从“渗透率提升”转向“入口稀缺、服务密度和变现效率”。",
    "待验证：服务零售口径下，本地生活和旅行的结构性弹性是否持续。",
    ["Q1.1.1", "Q1.1.2"],
    "大盘数据决定是否能给行业普遍高分。"
  ),
  leaf("Q1.1.1", "Q1.1", "线上零售需求是否仍能支撑电商平台高增长？",
    "电商需求仍大但增速不再稀缺。",
    "NBS 披露 2025 年网上零售额 RMB15,972.2bn，同比 +8.6%；实物商品网上零售 RMB13,092.3bn，同比 +5.2%，占社零 26.1%。",
    "线上零售仍是巨量市场，但实物电商的增速和渗透率意味着竞争更多来自存量份额和商业化效率。",
    "电商平台不能只因总市场大而高分，必须证明自身具备不可替代的低成本流量、供给组织或物流效率。",
    "缺少各平台 2025 全年 GMV 同口径、获客成本和广告货币化率。",
    "若实物线上零售增速连续低于社零或补贴依赖上升，电商 beta 继续降权。",
    ["SRC-NBS-ONLINE-2025", "SRC-NBS-COMMUNIQUE-2025"]
  ),
  leaf("Q1.1.2", "Q1.1", "服务消费和旅行是否提供更好的结构性需求？",
    "服务消费比商品电商更像结构性机会，但周期和可选消费属性更强。",
    "2025 年服务零售增速高于商品零售；Trip.com 在截至 2025 年的披露中，Q4 住宿预订收入同比 +21%，全年归母净利润显著高于 2024 年。",
    "旅行需求仍在恢复和出境链条重建，平台价值来自供给覆盖、品牌信任和跨境履约。",
    "旅行平台有较清晰需求弹性，但对宏观消费、航班供给和汇率敏感，不能自动视为高胜率。",
    "缺少实时酒店间夜、出境航班和营销获客成本数据。",
    "若住宿收入增速回落且 take-rate 或利润率走弱，旅行平台降为普通周期股。",
    ["SRC-NBS-COMMUNIQUE-2025", "SRC-TRIP-Q4-2025"]
  ),
  node("Q1.2", 2, "Q1", "Q1.2 新需求是否集中在 AI、内容和广告效率？",
    "结论：AI 需求是真实增量，但多数互联网公司还处在投入或早期货币化阶段；腾讯广告、阿里云、百度 AI Infra、快手 Kling AI 是可跟踪线索。",
    "待验证：AI 需求究竟提高了毛利率和留存，还是只提高了资本开支和研发费用。",
    ["Q1.2.1", "Q1.2.2"],
    "AI 是最大叙事，但也是最容易高估的叙事。"
  ),
  leaf("Q1.2.1", "Q1.2", "内容平台的广告和商业化是否出现效率改善？",
    "腾讯和快手显示广告/商业化改善，但字节系竞争仍是边界。",
    "腾讯 3Q25 营销服务收入同比 +21%；快手 3Q25 线上营销服务收入同比 +14%，总 DAU 和 MAU 小幅增长。",
    "用户时长和内容推荐可带来广告效率，但稀缺性只在封闭社交关系、交易闭环或差异化内容生态中成立。",
    "腾讯因社交关系链和视频号/小程序的复合入口更强；快手增长不错但替代性较高。",
    "缺少平台间广告 load、CPM、ROI 和用户时长同口径数据。",
    "若广告收入增长来自 ad load 而非 ROI 改善，估值应降权。",
    ["SRC-TENCENT-Q3-2025", "SRC-KUAISHOU-Q3-2025"]
  ),
  leaf("Q1.2.2", "Q1.2", "AI Cloud / AI Infra 是否已能构成可投资需求？",
    "AI Infra 有明确增速，但可投资性取决于谁拥有客户、算力供应和模型生态的组合稀缺性。",
    "百度 FY2025 AI Cloud Infra 约 RMB20bn，同比 +34%；Q4 AI accelerator infrastructure subscription revenue 同比 +143%。阿里在 2025 年披露继续加码 AI 基础设施与云。",
    "AI 基础设施需求在上升，但互联网公司未必都能把它转成高 ROIC；资本开支、芯片供给和价格竞争会稀释回报。",
    "阿里云和百度 AI Infra 是线索，不足以单独越过稀缺性和估值门槛。",
    "缺少 AI 云毛利率、GPU 利用率、客户续约和单位经济数据。",
    "若 AI 云收入高增但现金流、毛利率或传统业务继续恶化，AI 权重降档。",
    ["SRC-ALIBABA-SEP-2025", "SRC-BAIDU-Q4-2025"]
  ),

  node("Q2", 1, null, "Q2 谁掌握真正不可替代的价值捕获瓶颈？",
    "结论：最强瓶颈仍是腾讯的社交关系链、游戏 IP/发行和微信商业化入口；其次是阿里云/电商资产组合、携程旅行供给网络、京东供应链履约。其他公司更多是效率型或周期型资产。",
    "待验证：各瓶颈是否能维持定价权，而不是被补贴、监管或流量平台竞争吸走。",
    ["Q2.1", "Q2.2"],
    "本框架的核心不是找数据最多的公司，而是找市场尚未充分定价的稀缺性。"
  ),
  node("Q2.1", 2, "Q2", "Q2.1 入口和网络效应是否构成稀缺瓶颈？",
    "结论：社交流量入口优于普通内容流量，交易履约网络优于单纯 GMV 规模；腾讯最强，携程和美团局部成立，快手需要更多证明。",
    "待验证：视频号、小程序、旅行供给、即时零售和短视频电商的商业化效率是否可持续。",
    ["Q2.1.1", "Q2.1.2"],
    "入口稀缺决定是否能越过行动门槛。"
  ),
  leaf("Q2.1.1", "Q2.1", "腾讯的社交入口是否仍是中国互联网最稀缺资产？",
    "腾讯具备最高稀缺性，但需要估值和监管风险共同约束分数。",
    "3Q25 腾讯收入和利润同步增长，营销服务、游戏、金融科技及企业服务均增长；管理层把 AI 用于广告定向、内容创作和生产力。",
    "微信生态把社交关系、支付、小程序、视频号和游戏发行连接起来，替代难度明显高于单一 APP 流量。",
    "这是中国互联网里少数同时满足“巨大需求流入 + 不可替代入口 + 多场景变现”的资产。",
    "缺少微信生态交易额、视频号广告库存和 AI 投入回报的公开同口径数据。",
    "若广告增长放缓、游戏 pipeline 断层或监管限制商业化，腾讯目标强度下调。",
    ["SRC-TENCENT-Q3-2025"]
  ),
  leaf("Q2.1.2", "Q2.1", "本地生活、旅行和短视频电商的网络效应是否足够硬？",
    "局部网络效应存在，但比微信社交入口更容易被价格战或流量迁移削弱。",
    "美团披露年交易用户超过 8 亿；Trip.com 住宿预订收入增长；快手电商 GMV 同比 +15.2%。",
    "本地生活和旅行依赖供需密度、履约、商户覆盖和信任；短视频电商依赖内容流量和供给组织。",
    "携程的供给和品牌信任更稀缺；美团有强履约密度但面对即时零售和内容平台竞争；快手电商不是不可替代入口。",
    "缺少商户留存、补贴强度、订单利润率和重复购买数据。",
    "若补贴重新成为增长主因，网络效应分数要下修。",
    ["SRC-MEITUAN-Q3-2025", "SRC-TRIP-Q4-2025", "SRC-KUAISHOU-Q3-2025"]
  ),
  node("Q2.2", 2, "Q2", "Q2.2 供给、技术和履约壁垒是否能转成定价权？",
    "结论：阿里云、京东物流和百度 AI Infra 都有壁垒线索，但能否转成超额收益仍未充分证明。",
    "待验证：AI 云和履约体系的资本强度是否被更高毛利和客户锁定覆盖。",
    ["Q2.2.1", "Q2.2.2"],
    "技术或履约壁垒必须落到 ROIC，而不是只落到规模。"
  ),
  leaf("Q2.2.1", "Q2.2", "阿里云和百度 AI Infra 的技术壁垒是否足够稀缺？",
    "存在可观察技术壁垒，但估值中需要打折，因为 AI Infra 资本强度和竞争格局还不清晰。",
    "阿里披露 AI + Cloud 是核心投资方向；百度 AI Cloud Infra FY2025 约 RMB20bn，同比增长 34%。",
    "云厂商如果拥有客户、模型、算力调度和生态工具，可能形成高价值瓶颈；但若硬件供给受限或价格竞争激烈，回报会被稀释。",
    "阿里优于百度的地方是云和消费生态组合更完整；百度的 AI 增速更醒目但 legacy 拖累更大。",
    "缺少分部毛利、资本开支回收期和云客户集中度。",
    "若 AI 云增长不能转化为现金流和 margin，AI 线索降为观察项。",
    ["SRC-ALIBABA-SEP-2025", "SRC-BAIDU-Q4-2025"]
  ),
  leaf("Q2.2.2", "Q2.2", "京东供应链履约是否是稀缺瓶颈？",
    "京东供应链是有价值壁垒，但在本研究时点更像防守质量而非巨大未定价机会。",
    "JD Retail 3Q25 收入 RMB250.6bn、经营利润率 5.9%；集团为新业务增加营销和履约投入，压低综合利润。",
    "履约网络能提升用户体验和品类扩张能力，但重资产和新业务投入会降低短期赔率。",
    "京东适合作为质量观察项，不适合作为稀缺性优先的第一梯队。",
    "缺少即时零售投资回收期和物流外部客户利润率。",
    "若新业务投入继续压低集团利润且无法形成订单密度，强度下调。",
    ["SRC-JD-Q3-2025"]
  ),

  node("Q3", 1, null, "Q3 哪些风险足以否决多头结论？",
    "结论：反证最强的是行业增速下台阶、流量价格战、AI 投入回报不确定、监管和海外业务不确定。除腾讯外，多数公司存在至少一个未越过的门槛。",
    "待验证：若未来披露显示高质量现金流改善，而非仅靠收入增长，部分观察项可升级。",
    ["Q3.1", "Q3.2"],
    "风险控制决定是否必须把分数封顶。"
  ),
  node("Q3.1", 2, "Q3", "Q3.1 增长质量和竞争格局是否足以压低胜率？",
    "结论：是。电商、本地生活和内容平台都存在价格战或流量迁移风险；PDD 和美团的反证尤其明确。",
    "待验证：补贴率、商户 ROI、履约费用率、广告 load 是否恶化。",
    ["Q3.1.1", "Q3.1.2"],
    "没有可控反证，不能给高分。"
  ),
  leaf("Q3.1.1", "Q3.1", "宏观和线上零售增速是否让行业 beta 降权？",
    "行业 beta 应降权。",
    "2025 年社零同比 +3.7%，实物商品网上零售同比 +5.2%，已不是高速渗透阶段。",
    "增速降档会放大平台间份额竞争，导致获客、补贴和广告效率成为核心变量。",
    "行业大盘不是否定因素，但不足以支撑普遍高分。",
    "缺少分行业服务零售和线上广告预算数据。",
    "若线上零售和服务消费重新加速，需求评分可上调。",
    ["SRC-NBS-ONLINE-2025"]
  ),
  leaf("Q3.1.2", "Q3.1", "竞争是否会削弱 PDD、美团、快手的价值捕获？",
    "竞争风险足以把 PDD、美团和快手从行动名单中剔除或降为观察。",
    "PDD 管理层提示收入增长放缓、竞争格局和外部不确定性演化；美团和快手虽有大用户/GMV，但都需要持续投入抵御竞争。",
    "当增长依赖补贴、商家支持或流量购买，稀缺性会被费用端吞噬。",
    "这些资产不能只因规模大而高分，需要等待利润率与增长同时证明。",
    "缺少平台补贴率、商家佣金、广告 ROI 和海外监管成本。",
    "若竞争投入下降而订单/GMV仍保持增长，可重新评估。",
    ["SRC-PDD-Q3-2025", "SRC-MEITUAN-Q3-2025", "SRC-KUAISHOU-Q3-2025"]
  ),
  node("Q3.2", 2, "Q3", "Q3.2 财务质量和估值赔率是否支持行动？",
    "结论：腾讯质量最稳；阿里和京东赔率线索存在但商业转折仍需证据；百度、网易、携程更依赖特定业务线或周期位置。",
    "待验证：自由现金流、回购、分部利润、AI 资本开支回报。",
    ["Q3.2.1", "Q3.2.2"],
    "同样的稀缺性，只有在市场未充分定价时才是投资机会。"
  ),
  leaf("Q3.2.1", "Q3.2", "腾讯是否同时具备质量和赔率？",
    "腾讯质量强，赔率可接受但不是无约束高分。",
    "3Q25 腾讯毛利和非 IFRS 经营利润增速高于收入；多业务线增长降低单点风险。",
    "高利润质量提高下行保护，社交入口提高需求可见度；但若估值已充分反映质量，收益率仍可能不理想。",
    "腾讯是唯一可越过稀缺性行动门槛的候选，但仍需用广告、游戏和监管触发器约束。",
    "缺少 as-of 同口径估值与回购收益率细表。",
    "若利润增长低于收入或核心业务增长同步放缓，降为 watch_only。",
    ["SRC-TENCENT-Q3-2025"]
  ),
  leaf("Q3.2.2", "Q3.2", "其他候选的赔率为何不足以直接行动？",
    "其他候选多是“有线索、门槛不全”。",
    "京东新业务投入压低集团利润；百度 FY2025 总收入同比下降且存在资产减值；网易游戏增长低个位数；携程周期质量较好但需求弹性和估值需约束。",
    "这些公司不是没有价值，而是缺少“巨大未定价稀缺性”同时成立的证据。",
    "框架应把它们放入观察，而不是为了凑推荐强行给高分。",
    "缺少逐家公司 as-of EV/FCF、分部利润和资本配置数据。",
    "若后续披露证实自由现金流和回购收益率显著改善，可升级观察等级。",
    ["SRC-JD-Q3-2025", "SRC-BAIDU-Q4-2025", "SRC-NETEASE-Q4-2025", "SRC-TRIP-Q4-2025"]
  ),

  node("Q4", 1, null, "Q4 冻结时点应如何形成标的观察名单？",
    "结论：冻结名单不应广泛看多。腾讯通过行动门槛；阿里、携程、京东、网易为观察；PDD、百度、美团、快手因稀缺性、赔率或反证未过关而不行动。",
    "待验证：每个观察项都需要后续披露来证明稀缺性或赔率改善。",
    ["Q4.1", "Q4.2"],
    "Q4 是审计链条，不包含任何后验收益信息。"
  ),
  node("Q4.1", 2, "Q4", "Q4.1 标的排序如何由稀缺性门槛决定？",
    "结论：排序由需求可见度、不可替代性、市场低估、证据质量和反证控制共同决定；默认状态是不行动，只有门槛全过才行动。",
    "待验证：分数不是买卖建议，只是研究观察强度。",
    ["Q4.1.1", "Q4.1.2"],
    "这一步防止报告天然偏多。"
  ),
  leaf("Q4.1.1", "Q4.1", "哪家公司能越过行动门槛？",
    "仅腾讯越过行动门槛。",
    "腾讯同时具备社交入口稀缺性、广告/游戏/支付多线需求和较好利润质量。",
    "稀缺性和需求可见度足够高，市场低估假设虽需估值数据继续验证，但未明显低于门槛。",
    "冻结时点可把腾讯列为 actionable_long 观察项，但仍不是交易指令。",
    "缺少完整 as-of 估值快照与回购收益率。",
    "若估值安全边际消失或核心增长放缓，动作状态应回到 watch_only。",
    ["SRC-TENCENT-Q3-2025"]
  ),
  leaf("Q4.1.2", "Q4.1", "哪些公司应被限制为观察或不行动？",
    "阿里、携程、京东、网易可以观察；PDD、百度、美团、快手不应强行推荐。",
    "阿里有云/AI 与消费生态线索但稀缺性证明不足；携程质量较好但周期性较强；京东质量防守但投入压制赔率；网易需求不够大。PDD、百度、美团、快手至少一个关键门槛未过。",
    "当稀缺性、赔率或风险控制不完整，分数必须封顶。",
    "这使系统能输出“没有足够好机会”的判断，而不是永远偏多。",
    "缺少所有公司同口径估值、FCF 和资本配置数据。",
    "如果后续披露证明低估与高质量增长同时成立，可升级。",
    ["SRC-ALIBABA-SEP-2025", "SRC-JD-Q3-2025", "SRC-MEITUAN-Q3-2025", "SRC-PDD-Q3-2025", "SRC-BAIDU-Q4-2025", "SRC-NETEASE-Q4-2025", "SRC-TRIP-Q4-2025", "SRC-KUAISHOU-Q3-2025"]
  ),
  node("Q4.2", 2, "Q4", "Q4.2 后续跟踪触发器是什么？",
    "结论：跟踪触发器应围绕稀缺性变强或变弱，而不是只看收入增长。",
    "待验证：触发器需要在后续训练样本里和表现标签分离存储。",
    ["Q4.2.1", "Q4.2.2"],
    "触发器让研究可复盘、可迭代。"
  ),
  leaf("Q4.2.1", "Q4.2", "升级触发器是什么？",
    "升级触发器是“稀缺性变强且现金流证明”。",
    "可观察指标包括腾讯视频号/广告 ROI、阿里云 AI 客户续约和毛利、携程出境供给恢复、京东新业务 unit economics。",
    "只有当需求和价值捕获同时改善，才升级动作状态。",
    "这能避免单纯追逐主题热度。",
    "缺少公开同口径仪表盘。",
    "若后续披露提供清晰 FCF 和 ROIC 证据，可重评分。",
    ["SRC-TENCENT-Q3-2025", "SRC-ALIBABA-SEP-2025", "SRC-JD-Q3-2025", "SRC-TRIP-Q4-2025"]
  ),
  leaf("Q4.2.2", "Q4.2", "降级触发器是什么？",
    "降级触发器是“稀缺性被竞争或费用吞噬”。",
    "需要关注广告增长放缓、游戏内容断层、云价格战、外卖/即时零售补贴、PDD 商家支持投入扩大、AI 资本开支回报不明。",
    "如果增长需要越来越高的补贴或 capex，稀缺性就没有转成股东回报。",
    "这类触发器直接压低胜率和赔率。",
    "缺少平台补贴和 AI capex 回收期。",
    "若费用率持续上升而收入增速放缓，降级。",
    ["SRC-PDD-Q3-2025", "SRC-MEITUAN-Q3-2025", "SRC-BAIDU-Q4-2025", "SRC-KUAISHOU-Q3-2025"]
  ),
];

const targets = [
  target(1, "0700.HK", "Tencent", "微信生态 + 游戏/广告/支付复合入口", {
    chokepoint_strength: 4.4, future_space: 3.8, valuation_odds: 3.4, evidence_quality: 4.2,
    disconfirming_risk_control: 3.2, monitorability: 4.5, payoff_convexity: 3.4,
    demand_visibility: 4.0, irreplaceability: 4.5, market_underpricing: 3.3,
    valuation_tolerance: 3.2, downside_fragility: 2.8, catalyst_proximity: 3.4,
    expected_excess_return: 0.08, valuation_status: "verified",
  }, "多业务线增长和社交入口稀缺性同时成立，是唯一越过行动门槛的观察项。", "广告 ROI、游戏 pipeline、监管与估值安全边际", ["SRC-TENCENT-Q3-2025"], label("HKD", 518.0, "2026-02-27", 427.2, "2026-05-29", "StockAnalysis HKG 0700")),
  target(2, "BABA", "Alibaba", "AI Cloud + 电商生态组合", {
    chokepoint_strength: 3.6, future_space: 4.0, valuation_odds: 3.5, evidence_quality: 3.4,
    disconfirming_risk_control: 2.9, monitorability: 4.0, payoff_convexity: 3.8,
    demand_visibility: 4.1, irreplaceability: 3.6, market_underpricing: 3.6,
    valuation_tolerance: 3.5, downside_fragility: 3.2, catalyst_proximity: 3.2,
    expected_excess_return: 0.05, valuation_status: "verified",
  }, "云和消费生态有期权，但电商竞争和 AI 回报不确定使稀缺性未过门槛。", "AI 云毛利、淘天份额、即时商业投入回报", ["SRC-ALIBABA-SEP-2025"], label("USD", 144.11, "2026-02-27", 126.16, "2026-05-28", "Nasdaq BABA")),
  target(3, "TCOM", "Trip.com", "旅行供给网络与品牌信任", {
    chokepoint_strength: 3.8, future_space: 3.7, valuation_odds: 3.1, evidence_quality: 3.7,
    disconfirming_risk_control: 3.0, monitorability: 3.7, payoff_convexity: 3.2,
    demand_visibility: 3.8, irreplaceability: 3.8, market_underpricing: 3.1,
    valuation_tolerance: 3.0, downside_fragility: 3.0, catalyst_proximity: 3.1,
    expected_excess_return: 0.03, valuation_status: "verified",
  }, "服务消费和出行复苏质量较好，但赔率和周期风险不足以直接行动。", "出境供给、住宿增速、营销费用和 take-rate", ["SRC-TRIP-Q4-2025"], label("USD", 52.62, "2026-02-27", 47.08, "2026-05-28", "Nasdaq TCOM")),
  target(4, "JD", "JD.com", "自营零售 + 供应链履约", {
    chokepoint_strength: 3.4, future_space: 3.4, valuation_odds: 3.5, evidence_quality: 3.6,
    disconfirming_risk_control: 2.8, monitorability: 3.9, payoff_convexity: 3.0,
    demand_visibility: 3.5, irreplaceability: 3.2, market_underpricing: 3.5,
    valuation_tolerance: 3.6, downside_fragility: 3.3, catalyst_proximity: 2.8,
    expected_excess_return: 0.04, valuation_status: "verified",
  }, "履约和零售质量存在，但新业务投入压制集团赔率，稀缺性不足。", "新业务 unit economics、零售利润率、服务收入增长", ["SRC-JD-Q3-2025"], label("USD", 26.53, "2026-02-27", 29.14, "2026-05-28", "Nasdaq JD")),
  target(5, "NTES", "NetEase", "游戏 IP 与内容研发", {
    chokepoint_strength: 3.6, future_space: 3.0, valuation_odds: 3.3, evidence_quality: 3.8,
    disconfirming_risk_control: 3.1, monitorability: 3.6, payoff_convexity: 2.9,
    demand_visibility: 3.0, irreplaceability: 3.6, market_underpricing: 3.3,
    valuation_tolerance: 3.4, downside_fragility: 3.0, catalyst_proximity: 2.8,
    expected_excess_return: 0.03, valuation_status: "verified",
  }, "现金流和游戏能力可观察，但未来空间不够大，适合防守观察。", "新游戏 pipeline、版号、游戏收入增速", ["SRC-NETEASE-Q4-2025"], label("USD", 114.97, "2026-02-27", 124.02, "2026-05-28", "Nasdaq NTES")),
  target(6, "PDD", "PDD Holdings", "低价电商 + 跨境平台", {
    chokepoint_strength: 2.8, future_space: 3.8, valuation_odds: 3.0, evidence_quality: 3.3,
    disconfirming_risk_control: 2.4, monitorability: 2.7, payoff_convexity: 3.6,
    demand_visibility: 3.8, irreplaceability: 2.8, market_underpricing: 3.0,
    valuation_tolerance: 3.1, downside_fragility: 3.8, catalyst_proximity: 2.8,
    expected_excess_return: 0.0, valuation_status: "verified",
  }, "利润强但管理层已提示增速放缓与竞争外部不确定；稀缺性不足。", "商家支持投入、跨境监管、收入增速和现金转化", ["SRC-PDD-Q3-2025"], label("USD", 103.73, "2026-02-27", 83.03, "2026-05-28", "Nasdaq PDD")),
  target(7, "BIDU", "Baidu", "AI Infra + 搜索/自动驾驶", {
    chokepoint_strength: 3.0, future_space: 3.7, valuation_odds: 3.2, evidence_quality: 3.5,
    disconfirming_risk_control: 2.3, monitorability: 3.1, payoff_convexity: 3.4,
    demand_visibility: 3.7, irreplaceability: 3.0, market_underpricing: 3.2,
    valuation_tolerance: 3.2, downside_fragility: 3.7, catalyst_proximity: 3.0,
    expected_excess_return: 0.0, valuation_status: "verified",
  }, "AI Infra 增速亮眼，但 legacy 业务和资产减值削弱胜率。", "AI 云毛利、legacy 下滑、Apollo Go 商业化", ["SRC-BAIDU-Q4-2025"], label("USD", 124.44, "2026-02-27", 132.05, "2026-05-28", "Nasdaq BIDU")),
  target(8, "3690.HK", "Meituan", "本地生活履约网络", {
    chokepoint_strength: 3.4, future_space: 3.7, valuation_odds: 2.9, evidence_quality: 3.2,
    disconfirming_risk_control: 2.4, monitorability: 3.0, payoff_convexity: 3.1,
    demand_visibility: 3.7, irreplaceability: 3.4, market_underpricing: 2.9,
    valuation_tolerance: 2.9, downside_fragility: 3.9, catalyst_proximity: 2.8,
    expected_excess_return: 0.0, valuation_status: "verified",
  }, "用户和履约密度强，但竞争投入和本地生活价格战使赔率不足。", "外卖/即时零售补贴、订单利润、商户 ROI", ["SRC-MEITUAN-Q3-2025"], label("HKD", 81.15, "2026-02-27", 73.45, "2026-05-29", "StockAnalysis HKG 3690")),
  target(9, "1024.HK", "Kuaishou", "短视频社区 + 电商 + Kling AI", {
    chokepoint_strength: 3.1, future_space: 3.4, valuation_odds: 2.8, evidence_quality: 3.3,
    disconfirming_risk_control: 2.6, monitorability: 3.1, payoff_convexity: 3.4,
    demand_visibility: 3.4, irreplaceability: 3.1, market_underpricing: 2.8,
    valuation_tolerance: 2.9, downside_fragility: 3.8, catalyst_proximity: 3.0,
    expected_excess_return: 0.0, valuation_status: "verified",
  }, "经营改善可见，但内容流量和电商供给替代性较高，尚不是未定价稀缺机会。", "DAU/MAU、GMV 增速、Kling AI 变现、广告 ROI", ["SRC-KUAISHOU-Q3-2025"], label("HKD", 62.85, "2026-02-27", 45.54, "2026-05-29", "StockAnalysis HKG 1024")),
];

targets.forEach((row) => {
  row.score = scoreTarget(row.score_input);
  row.action_state = row.score.action_state;
  row.strength = row.score.strength;
});

function node(id, level, parent_id, question, conclusion, gaps, next_question_ids, materiality) {
  return {
    id, level, parent_id, question, conclusion, gaps, next_question_ids, materiality,
    source_plan: "使用 cutoff 前可见的官方财报、统计数据和公司公告；每个结论至少保留支持/反证材料。",
    skill_dispatch: "investment-question-architect -> research-source-planner -> financial-statement-analysis / valuation-analysis -> GPT verification",
    fact: conclusion,
    inference: conclusion,
    judgment: conclusion,
    gap: gaps,
    trigger: gaps,
    source_links: [],
  };
}

function leaf(id, parent_id, question, conclusion, fact, inference, judgment, gap, trigger, source_links) {
  return {
    id,
    level: 3,
    parent_id,
    question,
    conclusion,
    gaps: gap,
    next_question_ids: [],
    materiality: "该叶子答案会改变父节点结论、标的强度、赔率或风险控制。",
    source_plan: "优先使用 cutoff 前官方披露、统计数据和公司 IR；同时记录反证或边界条件。",
    skill_dispatch: "leaf-research-deepseek first-pass source extraction; GPT verified against source links before final synthesis",
    fact,
    inference,
    judgment,
    gap,
    trigger,
    source_links,
  };
}

function target(rank, ticker, name, thesis_node, score_input, rationale, downgrade_risk, source_ids, priceLabel) {
  return {
    rank, ticker, name, thesis_node, score_input, rationale, downgrade_risk, source_ids,
    next_verification_data: downgrade_risk,
    odds_model: "Base: 需求与稀缺性维持；Bull: 价值捕获效率提升且估值未充分反映；Bear: 竞争/投入吞噬现金流。",
    review_trigger: downgrade_risk,
    label: priceLabel,
  };
}

function label(currency, start_price, start_date, end_price, end_date, price_source) {
  return {
    as_of_cutoff: AS_OF_DATE,
    evaluation_date: end_date,
    label_window: `${start_date} to ${end_date}`,
    currency,
    start_price,
    end_price,
    forward_3m_return: Number((((end_price / start_price) - 1) * 100).toFixed(2)),
    benchmark_return: "",
    excess_return: "",
    price_source,
    label_status: "close_price_not_total_return_adjusted",
  };
}

function scoreTarget(input) {
  const components = {};
  for (const key of Object.keys(SCORE_WEIGHTS)) {
    components[key] = clamp(input[key] ?? 0);
  }
  const raw_total_score = round(Object.entries(SCORE_WEIGHTS).reduce((acc, [key, weight]) => acc + components[key] * weight, 0));
  const thesis_confidence = round(
    components.chokepoint_strength * 0.30 +
    components.future_space * 0.15 +
    components.valuation_odds * 0.10 +
    components.evidence_quality * 0.25 +
    components.disconfirming_risk_control * 0.15 +
    components.monitorability * 0.05
  );
  const payoff_convexity = round(
    components.payoff_convexity * 0.45 +
    clamp(input.valuation_tolerance ?? 0) * 0.20 +
    (6 - clamp(input.downside_fragility ?? 0)) * 0.20 +
    clamp(input.catalyst_proximity ?? 0) * 0.15
  );
  const demand_visibility = clamp(input.demand_visibility ?? components.future_space);
  const irreplaceability = clamp(input.irreplaceability ?? components.chokepoint_strength);
  const market_underpricing = clamp(input.market_underpricing ?? components.valuation_odds);
  const opportunity_fit = round(demand_visibility * 0.30 + irreplaceability * 0.40 + market_underpricing * 0.30);
  const gate_reasons = [];
  let max_total_score = 5.0;
  if (demand_visibility < 3.5) {
    gate_reasons.push("future_demand_below_gate");
    max_total_score = Math.min(max_total_score, 3.49);
  }
  if (irreplaceability < 3.8) {
    gate_reasons.push("scarcity_or_irreplaceability_below_gate");
    max_total_score = Math.min(max_total_score, irreplaceability < 3.0 ? 2.69 : 3.49);
  }
  if (market_underpricing < 3.2) {
    gate_reasons.push("market_underpricing_below_gate");
    max_total_score = Math.min(max_total_score, market_underpricing < 2.5 ? 2.69 : 3.49);
  }
  if (components.evidence_quality < 2.5) {
    gate_reasons.push("evidence_quality_below_gate");
    max_total_score = Math.min(max_total_score, 3.49);
  }
  if (components.disconfirming_risk_control < 2.5) {
    gate_reasons.push("disconfirming_risk_control_below_gate");
    max_total_score = Math.min(max_total_score, 3.49);
  }
  if (["missing", "stale", "unverified", "incomplete"].includes(String(input.valuation_status || "").toLowerCase())) {
    gate_reasons.push("valuation_unverified");
    max_total_score = Math.min(max_total_score, 3.49);
  }
  if (input.expected_excess_return !== undefined && Number(input.expected_excess_return) <= 0) {
    gate_reasons.push("expected_excess_return_not_positive");
    max_total_score = Math.min(max_total_score, 2.69);
  }
  const total_score = round(Math.min(raw_total_score, max_total_score));
  let action_state = "watch_only";
  if (max_total_score <= 2.69 || opportunity_fit < 3.0) action_state = "no_action";
  else if (gate_reasons.length) action_state = "watch_only";
  else if (opportunity_fit >= 3.8 && thesis_confidence >= 3.5 && payoff_convexity >= 3.2) action_state = "actionable_long";
  const strength = total_score >= 4.2 && thesis_confidence >= 4.0 ? "A" :
    total_score >= 3.5 && (thesis_confidence >= 3.3 || payoff_convexity >= 4.0) ? "B" :
    total_score >= 2.7 ? "C" : "D";
  return { score_components: components, weights: SCORE_WEIGHTS, raw_total_score, total_score, thesis_confidence, payoff_convexity, opportunity_fit, action_state, gate_reasons, strength };
}

function clamp(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) return 0;
  return Math.max(0, Math.min(5, number));
}

function round(value) {
  return Number(value.toFixed(3));
}

function childNodes(parentId) {
  return qaNodes.filter((item) => item.parent_id === parentId);
}

function sourceLink(id) {
  const source = sources.find((item) => item.source_id === id);
  if (!source) return `<span class="source-chip">${id}</span>`;
  return `<a class="source-chip" href="${source.url}" target="_blank" rel="noreferrer">${id}</a>`;
}

function renderQaCard(item) {
  const children = childNodes(item.id);
  const childHtml = children.length
    ? children.map(renderQaCard).join("\n")
    : `<p class="muted">无下级问题。</p>`;
  const leafMeta = item.level === 3 ? `
      <div class="logic-grid">
        <div class="logic-card"><b>Fact</b><span>${escapeHtml(item.fact)}</span></div>
        <div class="logic-card"><b>Inference</b><span>${escapeHtml(item.inference)}</span></div>
        <div class="logic-card"><b>Judgment</b><span>${escapeHtml(item.judgment)}</span></div>
        <div class="logic-card"><b>Gap / Trigger</b><span>${escapeHtml(item.gap)} ${escapeHtml(item.trigger)}</span></div>
      </div>
      <div class="source-chips">${(item.source_links || []).map(sourceLink).join("")}</div>` : "";
  const artifact = item.id === "Q2.1" ? renderChokepointScorecard() : item.id === "Q4.1" ? renderQ4MiniTable() : "";
  const headingLevel = Math.min(2 + item.level, 5);
  const idText = item.id.toLowerCase().replaceAll(".", "-");
  return `
    <details class="qa-card level-${item.level}" id="${idText}" open>
      <summary>
        <span class="qa-id">${item.id}</span>
        <h${headingLevel}>${escapeHtml(item.question)}</h${headingLevel}>
        <span class="qa-count">${children.length ? `${children.length} 子节点` : "叶子"}</span>
        <span class="chevron">›</span>
      </summary>
      <div class="qa-body">
        <section class="qa-block">
          <h4 class="block-title">1. 当前结论呈现</h4>
          <p>${escapeHtml(item.conclusion)}</p>
          ${artifact}
          ${leafMeta}
        </section>
        <section class="qa-block">
          <h4 class="block-title">2. 问题展开（子 QA）</h4>
          ${childHtml}
        </section>
        <section class="qa-block">
          <h4 class="block-title">3. 待补充的问题</h4>
          <p>${escapeHtml(item.gaps)}</p>
        </section>
      </div>
    </details>`;
}

function renderChokepointScorecard() {
  const rows = [
    ["腾讯", "4.5", "社交关系链、支付、小程序、视频号、游戏发行复合入口。"],
    ["阿里", "3.6", "云与消费生态组合强，但电商竞争和 AI 回报仍需验证。"],
    ["携程", "3.8", "旅行供给与品牌信任较强，周期属性限制分数。"],
    ["京东", "3.2", "履约壁垒可见，但重投入降低赔率。"],
    ["PDD", "2.8", "低价心智强，但平台可替代性和外部不确定高。"],
  ];
  return `<div class="artifact-card">
    <h5>瓶颈评分 schema</h5>
    <p>需求流入 30%，不可替代性 40%，市场未充分定价 30%；低于门槛时自动封顶。</p>
    <table><thead><tr><th>资产</th><th>不可替代性</th><th>驱动</th></tr></thead><tbody>${rows.map((row) => `<tr><td>${row[0]}</td><td>${row[1]}</td><td>${row[2]}</td></tr>`).join("")}</tbody></table>
  </div>`;
}

function renderQ4MiniTable() {
  return `<div class="artifact-card">
    <h5>冻结排序摘要</h5>
    <table><thead><tr><th>Rank</th><th>标的</th><th>action_state</th><th>分数</th><th>门槛说明</th></tr></thead><tbody>
    ${targets.slice(0, 6).map((row) => `<tr><td>${row.rank}</td><td>${row.ticker}</td><td>${row.action_state}</td><td>${row.score.total_score.toFixed(2)}</td><td>${formatGateReasons(row.score.gate_reasons)}</td></tr>`).join("")}
    </tbody></table>
  </div>`;
}

function renderTargetTable() {
  return `<section class="target-section" id="targets">
    <div class="section-kicker">Final Observation Rollup</div>
    <h2>最终标的推荐</h2>
    <p class="target-summary">这是冻结时点的研究观察名单，不是买卖指令。动作状态默认是不行动，只有“巨大需求、不可替代性、未充分定价”同时过门槛才进入 actionable_long。</p>
    <table class="target-table">
      <thead>
        <tr>
          <th>Rank</th><th>标的</th><th>action_state</th><th>强度</th><th>总分</th><th>稀缺性</th><th>需求</th><th>赔率</th><th>核心理由</th><th>风险触发器</th>
          <th>as_of_cutoff</th><th>evaluation_date</th><th>label_window</th><th>start_price</th><th>end_price</th><th>forward_3m_return<br><span>三个月股价变化</span></th><th>price_source</th><th>label_status</th>
        </tr>
      </thead>
      <tbody>
        ${targets.map((row) => `<tr>
          <td>${row.rank}</td>
          <td><b>${row.ticker}</b><br><span>${row.name}</span></td>
          <td><span class="state ${row.action_state}">${row.action_state}</span></td>
          <td>${row.strength}</td>
          <td>${row.score.total_score.toFixed(2)}</td>
          <td>${row.score.score_components.chokepoint_strength.toFixed(1)}</td>
          <td>${row.score.score_components.future_space.toFixed(1)}</td>
          <td>${row.score.score_components.valuation_odds.toFixed(1)}</td>
          <td>${escapeHtml(row.rationale)}<br><span class="muted">Gate: ${formatGateReasons(row.score.gate_reasons)}</span></td>
          <td>${escapeHtml(row.downgrade_risk)}</td>
          <td>${row.label.as_of_cutoff}</td>
          <td>${row.label.evaluation_date}</td>
          <td>${row.label.label_window}</td>
          <td>${row.label.currency} ${row.label.start_price.toFixed(2)}</td>
          <td>${row.label.currency} ${row.label.end_price.toFixed(2)}</td>
          <td class="${row.label.forward_3m_return >= 0 ? "pos" : "neg"}">${row.label.forward_3m_return.toFixed(2)}%</td>
          <td>${row.label.price_source}</td>
          <td>${row.label.label_status}</td>
        </tr>`).join("\n")}
      </tbody>
    </table>
  </section>`;
}

function renderSources() {
  return `<details class="source-collapse" id="sources">
    <summary>来源索引</summary>
    <div class="source-grid">
      ${sources.map((source) => `<article class="source-card">
        <h3><a href="${source.url}" target="_blank" rel="noreferrer">${escapeHtml(source.source_id)}</a></h3>
        <p>${escapeHtml(source.title)}</p>
        <dl><dt>visible_at</dt><dd>${source.source_visible_at}</dd><dt>bucket</dt><dd>${source.source_bucket}</dd><dt>usage</dt><dd>${source.allowed_usage}</dd><dt>stance</dt><dd>${source.support_refute_or_lead}</dd></dl>
        <p class="muted">${escapeHtml(source.summary)}</p>
      </article>`).join("\n")}
    </div>
  </details>`;
}

function htmlReport() {
  const l1 = qaNodes.filter((item) => item.level === 1);
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>中国互联网公司投资机会回测研究</title>
  <style>${css()}</style>
</head>
<body>
  <header class="hero">
    <nav class="top-nav"><a href="#goal">研究目标</a><a href="#qa">问题下钻</a><a href="#targets">标的表</a><a href="#sources">来源</a></nav>
    <div>
      <p class="eyebrow">Historical backtest · information cutoff ${AS_OF_DATE}</p>
      <h1>中国互联网公司投资机会研究</h1>
      <p>以稀缺性优先：只寻找当前未被市场充分定价、未来需求巨大且不可替代性足够强的机会。</p>
    </div>
  </header>
  <main>
    <section class="goal-card" id="goal">
      <div class="section-kicker">Goal</div>
      <h2>当前研究目标</h2>
      <p><b>研究对象：</b>中国互联网平台公司，覆盖电商、本地生活、游戏、广告、云/AI、旅行与内容社区。</p>
      <p><b>冻结边界：</b>研究、推理、评分、排序只使用 ${AS_OF_DATE} 当日及以前可见材料；后续价格只在最终标的表右侧作为结果字段显示。</p>
      <p><b>当前判断：</b>不做行业普遍多头。腾讯是唯一通过行动门槛的稀缺性观察项；阿里、携程、京东、网易需要更多估值或现金流证据；PDD、百度、美团、快手至少一个关键门槛未过。</p>
      <p><b>最大不确定性：</b>AI 和本地服务投入能否转化为高质量自由现金流，而不是被资本开支、补贴和竞争重新吞噬。</p>
    </section>
    <section id="qa">
      <div class="section-kicker">QA Drilldown</div>
      <h2>问题下钻</h2>
      ${l1.map(renderQaCard).join("\n")}
    </section>
    ${renderTargetTable()}
    ${renderSources()}
  </main>
</body>
</html>`;
}

function css() {
  return `
:root { color-scheme: light; --bg:#f5f7fb; --card:#fff; --ink:#172033; --muted:#687386; --line:#dce2ea; --blue:#2563eb; --green:#078458; --red:#c24132; }
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,"Noto Sans SC",sans-serif; background:var(--bg); color:var(--ink); line-height:1.55; letter-spacing:0; }
a { color:var(--blue); text-decoration:none; }
main { width:min(1320px, calc(100% - 32px)); margin:0 auto 56px; }
.hero { min-height:310px; padding:24px max(24px, calc((100vw - 1320px)/2)) 42px; display:flex; flex-direction:column; justify-content:space-between; background:linear-gradient(180deg,#ffffff 0%,#edf3fb 100%); border-bottom:1px solid var(--line); }
.top-nav { display:flex; gap:10px; flex-wrap:wrap; }
.top-nav a { color:#344054; border:1px solid var(--line); background:rgba(255,255,255,.72); padding:8px 12px; border-radius:8px; font-size:13px; }
.eyebrow,.section-kicker { color:#526077; text-transform:uppercase; font-size:12px; font-weight:700; letter-spacing:.06em; }
h1 { font-size:clamp(34px, 6vw, 64px); max-width:920px; margin:8px 0 12px; line-height:1.04; letter-spacing:0; }
h2 { font-size:28px; margin:4px 0 18px; letter-spacing:0; }
h3,h4,h5 { letter-spacing:0; }
.goal-card, .qa-card, .target-section, .source-collapse { background:var(--card); border:1px solid var(--line); border-radius:8px; margin:18px 0; box-shadow:0 12px 36px rgba(15,23,42,.04); }
.goal-card, .target-section, .source-collapse { padding:22px; }
.qa-card { padding:0; overflow:hidden; }
.qa-card.level-1 { border-left:4px solid #2563eb; }
.qa-card.level-2 { margin-left:18px; border-left:3px solid #7aa2f7; background:#fbfdff; }
.qa-card.level-3 { margin-left:18px; border-left:2px solid #b7c7e6; background:#fff; }
.qa-card>summary { list-style:none; display:grid; grid-template-columns:auto 1fr auto auto; gap:12px; align-items:center; cursor:pointer; padding:16px; }
.qa-card>summary::-webkit-details-marker { display:none; }
.qa-card>summary h3,.qa-card>summary h4,.qa-card>summary h5 { margin:0; font-size:18px; line-height:1.35; }
.qa-id { flex:0 0 auto; min-width:54px; padding:4px 8px; border:1px solid var(--line); border-radius:8px; color:#334155; background:#f8fafc; font-size:12px; text-align:center; }
.qa-count { color:#66758a; font-size:12px; white-space:nowrap; background:#f5f8fb; border:1px solid #e2e8f1; border-radius:999px; padding:5px 9px; }
.chevron { display:inline-block; font-size:22px; color:#8793a2; transition:transform .18s ease; }
.qa-card[open]>summary .chevron { transform:rotate(90deg); }
.qa-body { border-top:1px solid var(--line); padding:0 16px 16px; display:grid; gap:12px; }
.qa-block { border-top:1px solid #eef2f7; padding-top:12px; }
.block-title { font-size:14px; color:#334155; margin:0 0 8px; }
p { margin:0 0 10px; }
.muted { color:var(--muted); font-size:13px; }
.logic-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin-top:10px; }
.logic-card, .artifact-card { border:1px solid var(--line); background:#f8fafc; border-radius:8px; padding:10px; }
.logic-card b { display:block; font-size:12px; color:#526077; margin-bottom:4px; }
.logic-card span { font-size:13px; }
.source-chips { display:flex; gap:8px; flex-wrap:wrap; margin-top:10px; }
.source-chip { border:1px solid var(--line); background:#fff; border-radius:999px; padding:4px 9px; font-size:12px; }
table { width:100%; border-collapse:collapse; table-layout:auto; }
th,td { border-bottom:1px solid var(--line); padding:9px 8px; text-align:left; vertical-align:top; font-size:13px; }
th { color:#475569; background:#f8fafc; font-weight:700; position:sticky; top:0; z-index:1; }
.target-table { min-width:1680px; }
.target-section { overflow-x:auto; }
.target-summary { max-width:980px; color:#475569; }
.state { display:inline-flex; white-space:nowrap; padding:3px 8px; border-radius:999px; font-size:12px; border:1px solid var(--line); }
.state.actionable_long { color:#075985; background:#e0f2fe; border-color:#bae6fd; }
.state.watch_only { color:#854d0e; background:#fef3c7; border-color:#fde68a; }
.state.no_action { color:#475569; background:#f1f5f9; }
.pos { color:var(--green); font-weight:700; }
.neg { color:var(--red); font-weight:700; }
.source-collapse summary { cursor:pointer; font-weight:700; font-size:22px; }
.source-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:12px; margin-top:16px; }
.source-card { border:1px solid var(--line); border-radius:8px; padding:12px; background:#fbfdff; }
.source-card h3 { margin:0 0 6px; font-size:14px; }
.source-card dl { display:grid; grid-template-columns:92px 1fr; gap:4px 8px; margin:8px 0; font-size:12px; }
.source-card dt { color:#64748b; }
.source-card dd { margin:0; }
@media (max-width: 720px) {
  main { width:min(100% - 20px, 1320px); }
  .hero { min-height:260px; padding:18px 14px 28px; }
  .logic-grid { grid-template-columns:1fr; }
  .qa-card.level-2,.qa-card.level-3 { margin-left:0; }
}`;
}

function markdownReport() {
  return `# 中国互联网公司投资机会回测研究

- as_of_date: ${AS_OF_DATE}
- report_date: ${REPORT_DATE}
- mode: historical_backtest

## 当前研究目标

只寻找当前未被市场充分定价、未来需求巨大且不可替代性足够强的机会。研究和排序使用 cutoff 前资料；后续价格只在最终标的表作为结果字段。

## 冻结结论

腾讯是唯一通过行动门槛的观察项；阿里、携程、京东、网易为观察；PDD、百度、美团、快手不行动。

## 最终标的推荐

| Rank | Ticker | Action | Score | Return Field |
| --- | --- | --- | ---: | ---: |
${targets.map((row) => `| ${row.rank} | ${row.ticker} | ${row.action_state} | ${row.score.total_score.toFixed(2)} | ${row.label.forward_3m_return.toFixed(2)}% |`).join("\n")}
`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function formatGateReasons(reasons) {
  if (!reasons || reasons.length === 0) return "passed";
  const labels = {
    future_demand_below_gate: "future demand below gate",
    scarcity_or_irreplaceability_below_gate: "scarcity below gate",
    market_underpricing_below_gate: "underpricing below gate",
    evidence_quality_below_gate: "evidence quality below gate",
    disconfirming_risk_control_below_gate: "risk control below gate",
    valuation_unverified: "valuation unverified",
    expected_excess_return_not_positive: "expected return not positive",
  };
  return reasons.map((reason) => labels[reason] || reason.replaceAll("_", " ")).join(", ");
}

function writeJson(file, value) {
  fs.writeFileSync(path.join(OUT_DIR, file), `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.writeFileSync(path.join(OUT_DIR, "professional_report.html"), htmlReport(), "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "professional_report.md"), markdownReport(), "utf8");
  writeJson("project.json", {
    project_id: "china_internet_timeslice_20260228",
    title: "中国互联网公司投资机会回测研究",
    mode: "historical_backtest",
    as_of_date: AS_OF_DATE,
    report_date: REPORT_DATE,
    report_path: "professional_report.html",
  });
  writeJson("qa_tree.json", { as_of_date: AS_OF_DATE, nodes: qaNodes });
  writeJson("investment_workbench.json", {
    as_of_date: AS_OF_DATE,
    scoring_worksheet: targets.map((row) => ({
      ticker: row.ticker,
      rank: row.rank,
      score_input: row.score_input,
      score: row.score,
      rationale: row.rationale,
      downgrade_risk: row.downgrade_risk,
      source_ids: row.source_ids,
    })),
    frozen_recommendations: targets.map(({ label: _label, ...row }) => row),
    label_attach: targets.map((row) => ({ ticker: row.ticker, label: row.label })),
    rejected_future_sources: sources.filter((source) => source.allowed_usage === "label_only"),
    deepseek_note: "DeepSeek parsed provided source snippets only; GPT verified and synthesized final judgments.",
  });
  fs.writeFileSync(
    path.join(OUT_DIR, "evidence.jsonl"),
    sources.map((source) => JSON.stringify(source)).join("\n") + "\n",
    "utf8"
  );
  console.log(`wrote ${OUT_DIR}`);
}

main();
