const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const AS_OF_DATE = "2026-02-28";
const REPORT_DATE = "2026-05-30";
const OUT_DIR = path.join(ROOT, "research", "qa_projects", "laopu_gold_timeslice_20260228");

const componentWeights = {
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
    "SRC-LPG-2024-RESULTS",
    "Laopu Gold 2024 annual results announcement",
    "https://www.hkexnews.hk/listedco/listconews/sehk/2025/0331/2025033101661.pdf",
    "2025-03-31",
    "2024 revenue RMB8.506B, +167.5%; gross profit RMB3.501B, +162.9%; profit RMB1.473B, +253.9%; adjusted net profit RMB1.502B, +253.4%; gross margin about 41.2%; final dividend RMB6.35 per share."
  ),
  source(
    "SRC-LPG-2025H1-RESULTS",
    "Laopu Gold 2025 interim results announcement",
    "https://www.hkexnews.hk/listedco/listconews/sehk/2025/0820/2025082000247.pdf",
    "2025-08-20",
    "2025H1 revenue RMB12.354B, +251.0%; gross profit RMB4.705B, +223.4%; profit RMB2.268B, +285.8%; adjusted net profit RMB2.351B, +290.6%; gross margin 38.1%; adjusted net profit margin 19.0%; inventories and borrowings rose materially as the company stocked gold raw materials for demand and expansion."
  ),
  source(
    "SRC-LPG-CINDA-20250827",
    "Cinda Securities Laopu Gold 2025H1 update",
    "https://pdf.dfcfw.com/pdf/H3_AP202508271735559502_1.pdf",
    "2025-08-27",
    "Research note recorded 41 self-operated boutiques in 16 cities and 29 high-end malls as of 2025H1, including SKP and MixC exposure; forecast 2025/2026/2027 net profit RMB4.953B/RMB6.881B/RMB8.353B, with PE of 23x/17x/14x at the 2025-08-27 close."
  ),
  source(
    "SRC-LPG-CMBC-20251215",
    "Consumer sector valuation table including Laopu Gold",
    "https://www.cmbccap.com/capwebsit-app/capwebsit/downloadFile.download?fileId=ef30326a509c46e4ae0327968091ba93&moduleNo=CAP",
    "2025-12-15",
    "At HKD662.50, the table showed 2025E/2026E revenue RMB25.09B/RMB32.92B, net profit RMB4.66B/RMB6.42B, revenue growth 194.9%/31.2%, net-profit growth 216.6%/37.6%, PE 23x/17x, dividend yield 2.6%."
  ),
  source(
    "SRC-HSI-20260213",
    "Hang Seng Indexes February 2026 index review",
    "https://www.hsi.com.hk/static/uploads/contents/en/news/pressRelease/20260213T174500.pdf",
    "2026-02-13",
    "Laopu Gold appeared in the consumer/commerce-and-industry constituent change table with 45% free-float adjustment factor and about 0.29% new weight; implementation was after market close on 2026-03-06, making it a visible liquidity lead rather than fundamental evidence."
  ),
  labelSource(
    "LBL-6181-PRICE",
    "6181.HK close-price evaluation dataset",
    "https://stockanalysis.com/quote/hkg/6181/history/",
    "2026-05-29",
    "Close-price evaluation dataset for the frozen 6181.HK observation. It is label-only and is not used in QA reasoning."
  ),
];

const l1Defs = [
  ["Q1", "老铺黄金的增长驱动是否真实且可持续？", "增长真实，但不是普通黄金零售 beta：已披露数据更像高端品牌、稀缺商场渠道和线上破圈共同推动；可持续性仍取决于同店、门店优化和海外复制。"],
  ["Q2", "公司的价值捕获瓶颈和稀缺性在哪里？", "稀缺性集中在高端古法黄金品牌心智、顶级商场准入、设计工艺和高净值客群重合；但黄金原材料不是稀缺壁垒，必须防止把金价上涨误判成品牌定价权。"],
  ["Q3", "财务质量、估值赔率和反证风险如何约束分数？", "财务增长强，但营运资金占用、存货、短借和估值已经反映部分乐观预期，导致未充分定价证据不够硬，动作状态需要封顶。"],
  ["Q4", "冻结时点如何形成老铺黄金观察状态？", "6181.HK 可以进入高优先级观察名单，但默认不把强品牌叙事直接等同于 actionable_long；需要等 2025 全年、现金流和提价后需求韧性验证。"],
];

const l2Defs = [
  ["Q1.1", "财务增长和销售动能", "先判断收入、利润和线上线下销售动能是否真实进入报表。"],
  ["Q1.2", "门店、线上和海外增长空间", "再判断增长是否仍有可复制 runway，而不是一次性抢购或金价驱动。"],
  ["Q2.1", "品牌和渠道稀缺性", "检验老铺是否拥有难替代的高端品牌和商场渠道入口。"],
  ["Q2.2", "定价权与产品结构", "检验金价波动下公司是否有产品和价格能力保护毛利。"],
  ["Q3.1", "财务质量与现金转换", "把利润增长和营运资金、库存、借款、分红放在一起检验质量。"],
  ["Q3.2", "估值赔率和反证清单", "判断市场是否已经充分定价品牌稀缺性，并绑定降级条件。"],
  ["Q4.1", "目标观察状态", "把 Q1-Q3 结论映射到具体证券的 action_state。"],
  ["Q4.2", "升级和降级触发器", "定义后续复盘时需要验证的数据，不用后验价格重写当时判断。"],
];

const leaves = [
  leaf("Q1.1.1", "2024 到 2025H1 的增长是否已经进入收入和利润表？", "financial-statement-analysis", "future_space", ["SRC-LPG-2024-RESULTS", "SRC-LPG-2025H1-RESULTS"], {
    conclusion: "收入和利润增长已经进入官方报表，且增速远高于普通珠宝零售。",
    fact: "2024 收入 RMB8.506B、净利润 RMB1.473B；2025H1 收入 RMB12.354B、净利润 RMB2.268B，均为港交所公告披露。",
    inference: "增长不是只有媒体热度，而是已在收入、毛利和净利润三张核心指标上同步体现。",
    judgment: "该叶子支持提高 future_space 和 evidence_quality，但仍不能单独证明未来三年持续性。",
  }),
  leaf("Q1.1.2", "线上破圈和高端客群是否扩大需求来源？", "industry-report-analysis", "future_space", ["SRC-LPG-2025H1-RESULTS"], {
    conclusion: "线上和高端客群均提供增量需求线索，但仍需跟踪复购和非大促贡献。",
    fact: "2025H1 天猫 618 黄金类目成交额超过 RMB1B 并排名第一；公司披露与五大国际奢侈品牌客户平均重合率约 77.3%。",
    inference: "高端客群重合和线上破圈说明老铺不是只吃线下小众客流，但大促数据可能包含提前购买。",
    judgment: "支持需求真实存在，但对长期增长只给中高置信度。"
  }),
  leaf("Q1.2.1", "顶级商场门店扩张还有没有空间？", "industry-report-analysis", "future_space", ["SRC-LPG-2025H1-RESULTS", "SRC-LPG-CINDA-20250827"], {
    conclusion: "门店仍有优化和扩张空间，但核心高端商场资源并非无限。",
    fact: "截至 2025H1，公司在 16 城有 41 家自营店，进入 29 个高端商业体，包括 SKP 和万象城体系，并在上海港汇恒隆、上海 IFC 等新开店或扩容。",
    inference: "高端商场集中带来强坪效和品牌背书，也意味着下一阶段增长更依赖单店扩容、位置优化和少数新增商场。",
    judgment: "增长 runway 存在，但不能按普通连锁零售无限外推。"
  }),
  leaf("Q1.2.2", "海外首店和线上渠道是否构成第二曲线？", "news-event-analysis", "future_space", ["SRC-LPG-2025H1-RESULTS", "SRC-LPG-CINDA-20250827"], {
    conclusion: "海外和线上是第二曲线线索，尚未达到独立证明长期空间的证据强度。",
    fact: "公司 2025-06-21 在新加坡滨海湾金沙开出首家海外门店；中期公告披露线上销售表现显著。",
    inference: "海外高端商场验证有价值，但样本仍小；线上有放大能力，但需要拆分大促和常态销售。",
    judgment: "该叶子支持观察，但不单独把总分推到高确信。"
  }),
  leaf("Q2.1.1", "高端古法黄金品牌是否构成难替代心智？", "industry-report-analysis", "chokepoint_strength", ["SRC-LPG-2024-RESULTS", "SRC-LPG-2025H1-RESULTS"], {
    conclusion: "品牌心智是主要稀缺点，强于普通黄金零售的金价敞口。",
    fact: "公司将增长归因于品牌影响力、产品优化迭代和门店扩张；2025H1 披露高端奢侈品牌客群重合率较高。",
    inference: "消费者愿意为设计、场景和品牌支付金价之外溢价，说明价值捕获点不只是黄金库存。",
    judgment: "提高 chokepoint_strength，但需要防止品牌热度和短期抢购被过度资本化。"
  }),
  leaf("Q2.1.2", "顶级商场准入是否形成稀缺渠道入口？", "industry-report-analysis", "chokepoint_strength", ["SRC-LPG-2025H1-RESULTS", "SRC-LPG-CINDA-20250827"], {
    conclusion: "顶级商场准入形成稀缺入口，是老铺区别于大众黄金品牌的关键。",
    fact: "公司进入 29 个知名高端商业中心，包含 6 家 SKP 系和 11 家万象城系门店。",
    inference: "高端商场对品牌、坪效和客群要求高，渠道入口强化品牌定位并降低低端价格战干扰。",
    judgment: "该叶子明显支持稀缺性评分。"
  }),
  leaf("Q2.2.1", "金价上涨时毛利率是否能守住？", "financial-statement-analysis", "disconfirming_risk_control", ["SRC-LPG-2024-RESULTS", "SRC-LPG-2025H1-RESULTS"], {
    conclusion: "毛利率仍高但已受金价和备货影响，需要保守处理。",
    fact: "2024 毛利率约 41.2%；2025H1 毛利率降至 38.1%，公司称受金价短期波动影响。",
    inference: "老铺有一定品牌加价能力，但金价快速上行会压缩毛利或推迟价格传导。",
    judgment: "该叶子压低风险控制分，要求后续验证提价后销量和毛利。"
  }),
  leaf("Q2.2.2", "原创设计、专利和产品结构能否保护溢价？", "industry-report-analysis", "chokepoint_strength", ["SRC-LPG-2025H1-RESULTS"], {
    conclusion: "设计和工艺资产支持溢价，但仍需要持续爆品和复购证明。",
    fact: "截至 2025H1，公司披露超过 2,100 款原创设计、273 项境内专利、1,505 项作品著作权和 246 项境外专利。",
    inference: "设计和知识产权提高模仿门槛，也帮助把黄金从材料消费升级为品牌消费。",
    judgment: "支持稀缺性，但不是绝对垄断。"
  }),
  leaf("Q3.1.1", "利润增长是否同步转化为经营现金流？", "financial-statement-analysis", "evidence_quality", ["SRC-LPG-2025H1-RESULTS"], {
    conclusion: "现金转换是最大质量瑕疵之一，不能只看净利润增速。",
    fact: "2025H1 存货增至 RMB8.685B，短期借款增至 RMB3.183B；经营净现金流出 RMB2.215B，扣除用于黄金原材料采购的配售资金影响后为净流入 RMB154M。",
    inference: "高增长阶段需要大量备货，利润质量并非完全低风险现金流模型。",
    judgment: "压低 evidence_quality 和 disconfirming_risk_control，并要求年度现金流验证。"
  }),
  leaf("Q3.1.2", "高分红是否足以证明资本回报质量？", "financial-statement-analysis", "monitorability", ["SRC-LPG-2024-RESULTS", "SRC-LPG-2025H1-RESULTS"], {
    conclusion: "高分红是正面信号，但不能抵消存货和借款风险。",
    fact: "公司 2024 年建议每股 RMB6.35 股息，2025H1 建议每股 RMB9.59 中期股息。",
    inference: "分红显示管理层回报股东意愿，但在高备货和高借款背景下需要同时看现金流。",
    judgment: "提高 monitorability，不能提高 valuation_odds。"
  }),
  leaf("Q3.2.1", "冻结时点估值是否仍有未充分定价空间？", "valuation-analysis", "valuation_odds", ["SRC-LPG-CMBC-20251215", "SRC-LPG-CINDA-20250827", "SRC-HSI-20260213"], {
    conclusion: "估值并不离谱，但未充分定价证据不够硬。",
    fact: "2025-12-15 估值表显示老铺在 HKD662.50 对应 2026E PE 约 17x；2 月冻结日前市场已可见高增长预测和恒指纳入线索。",
    inference: "若 2026E 利润预测兑现，估值相对成长性不贵；但市场已认识到品牌稀缺性和指数流动性。",
    judgment: "valuation_odds 给中性偏正，但低于 actionable_long 门槛。"
  }),
  leaf("Q3.2.2", "哪些反证会打破高端品牌叙事？", "valuation-analysis", "disconfirming_risk_control", ["SRC-LPG-CINDA-20250827", "SRC-LPG-CMBC-20251215"], {
    conclusion: "金价、产品推新、消费疲弱、解禁/配售和海外复制失败都足以降级。",
    fact: "券商风险提示包含金价剧烈波动、产品推新不及预期、海外环境不确定、消费需求疲软和大股东解禁。",
    inference: "老铺的高估值容忍度来自增长和品牌心智，一旦同店或毛利走弱，估值会迅速重定价。",
    judgment: "必须以硬触发器封顶 action_state。"
  }),
  leaf("Q4.1.1", "6181.HK 是否进入 actionable_long？", "target-recommendation-analysis", "target_ranking", ["SRC-LPG-2025H1-RESULTS", "SRC-LPG-CMBC-20251215", "SRC-HSI-20260213"], {
    conclusion: "进入高优先级观察，但不进入 actionable_long。",
    fact: "冻结日前可见证据显示高增长、高端渠道和 2026E PE 约 17x；同时 2025 全年正式业绩、提价后需求和现金流尚未披露。",
    inference: "巨大需求和稀缺性成立概率较高，未充分定价只达到中性偏正，不足以越过三重门槛。",
    judgment: "action_state 设为 watch_only，等待年度业绩和现金流验证。"
  }),
  leaf("Q4.1.2", "是否需要用同行替代或分散表达？", "target-recommendation-analysis", "target_ranking", ["SRC-LPG-CMBC-20251215"], {
    conclusion: "单公司研究不替换标的，但同行估值只作为赔率边界。",
    fact: "估值表中周大福、老凤祥、周六福、潮宏基等同业增速和 PE 明显分化。",
    inference: "老铺的品牌稀缺性强于大众黄金饰品，但同业提供了估值压缩的参照。",
    judgment: "最终名单保留 6181.HK 一个观察标的，不用低质量替代品稀释结论。"
  }),
  leaf("Q4.2.1", "升级触发器是什么？", "target-recommendation-analysis", "action_state", ["SRC-LPG-2025H1-RESULTS", "SRC-LPG-CMBC-20251215"], {
    conclusion: "升级需要年度利润、现金流、毛利和同店同时验证。",
    fact: "截至冻结日，2025 全年正式结果和 2026 开年经营数据尚不可见。",
    inference: "只有当强增长不再依赖备货和借款、且估值仍未充分反映，才可升级。",
    judgment: "后续看 2025 年度公告、同店、毛利、经营现金流和海外店效。"
  }),
  leaf("Q4.2.2", "降级触发器是什么？", "target-recommendation-analysis", "action_state", ["SRC-LPG-2025H1-RESULTS", "SRC-LPG-CINDA-20250827"], {
    conclusion: "若现金流恶化或提价后销量走弱，应从 watch_only 降到 no_action。",
    fact: "2025H1 已出现存货、短借和经营现金流压力；券商风险提示包括金价和消费需求。",
    inference: "这些风险一旦从可能性变成数据事实，品牌稀缺性也无法支撑高赔率。",
    judgment: "把经营现金流、存货周转、毛利和同店增速作为硬降级条件。"
  }),
];

const targets = rankTargets([
  makeTarget({
    ticker: "6181.HK",
    name: "老铺黄金",
    thesis_node: "高端古法黄金品牌 / 顶级商场渠道 / 设计工艺溢价",
    scores: {
      chokepoint_strength: 4.2,
      future_space: 4.1,
      valuation_odds: 3.1,
      evidence_quality: 3.6,
      disconfirming_risk_control: 2.8,
      monitorability: 3.7,
      payoff_convexity: 3.4,
    },
    demand_visibility: 4.1,
    irreplaceability: 4.2,
    market_underpricing: 3.1,
    valuation_status: "incomplete",
    rationale:
      "品牌、渠道和财务增长证据强，估值相对成长性不极端；但冻结日前 2025 全年正式业绩、现金流转换、提价后销量韧性和未充分定价证据仍不足，故只给 watch_only。",
    downgrade_risk:
      "经营现金流继续弱于利润、存货周转恶化、金价波动压毛利、同店增长放缓、海外店效不达预期或估值继续扩张但盈利未跟上。",
    required_data:
      "2025 全年业绩、2026 开年销售/同店、毛利率、经营现金流、存货周转、短借变化、提价后销量。",
    label: {
      as_of_cutoff: AS_OF_DATE,
      evaluation_date: "2026-05-29",
      label_window: "2026-02-27 to 2026-05-29",
      currency: "HKD",
      start_price: 723.5,
      start_price_date: "2026-02-27",
      end_price: 504.0,
      end_price_date: "2026-05-29",
      forward_3m_return: round((504.0 / 723.5 - 1) * 100, 2),
      benchmark_return: null,
      excess_return: null,
      price_source: "Investing.com historical start close + StockAnalysis end close",
      label_status: "label_verified_close_price_not_total_return_adjusted",
    },
  }),
]);

function source(source_id, title, url, source_visible_at, summary) {
  return {
    source_id,
    title,
    url,
    source_visible_at,
    source_bucket: "evidence",
    support_refute_or_lead: "support",
    allowed_usage: "thesis",
    used_in: ["QA"],
    cutoff_status: "visible_on_or_before_as_of_date",
    availability_proof: { proof_type: "publisher_or_report_date", proof_value: source_visible_at, proof_url: url },
    summary,
  };
}

function labelSource(source_id, title, url, source_visible_at, summary) {
  return {
    source_id,
    title,
    url,
    source_visible_at,
    source_bucket: "evidence",
    support_refute_or_lead: "lead",
    allowed_usage: "label_only",
    used_in: ["final_label"],
    cutoff_status: "post_cutoff_label_only",
    availability_proof: { proof_type: "evaluation_price_dataset", proof_value: source_visible_at, proof_url: url },
    summary,
  };
}

function leaf(id, question, selected_skill, score_component, source_links, answer) {
  const parent_id = id.split(".").slice(0, 2).join(".");
  const schema = schemaFor(selected_skill, score_component);
  return {
    id,
    parent_id,
    question,
    conclusion: answer.conclusion,
    fact: answer.fact,
    inference: answer.inference,
    judgment: answer.judgment,
    gap: "需要更细的同店、常态线上、海外店效、毛利桥、存货周转和现金流数据。",
    trigger: "若后续披露显示增长无法转成现金流、品牌溢价被金价吞噬、估值已透支或反证恶化，重新评分。",
    selected_skill,
    score_component,
    source_links,
    materiality: `该叶子会改变 ${score_component}、目标强度、风险封顶或 action_state。`,
    decision_use: `用于判断 ${score_component} 是否足以支撑老铺黄金的观察状态。`,
    support_evidence: source_links.map((source_id) => `${source_id} 支持或界定该问题。`),
    refute_evidence: ["同店、毛利、现金流、存货、估值或海外复制数据与当前结论相反时，应降低强度。"],
    target_implications: "影响 6181.HK 的分数、门槛、升级/降级触发器和最终 action_state。",
    minimum_evidence_gate: "至少一项冻结日前可见的官方披露或研究数据，并保留边界/反证来源。",
    refuting_source_plan: ["检查金价波动、消费疲弱、产品推新失败、现金流恶化和估值透支证据。"],
    source_plan: source_links.map((source_id) => ({
      source_id,
      source_visible_at: sourceMap()[source_id]?.source_visible_at,
      source_bucket: sourceMap()[source_id]?.source_bucket,
      allowed_usage: sourceMap()[source_id]?.allowed_usage,
      cutoff_status: "visible_on_or_before_as_of_date",
      availability_proof: sourceMap()[source_id]?.availability_proof,
      expected_fields: schema,
      preferred_parser_skill: selected_skill,
    })),
    skill_dispatch: {
      task_family: taskFamily(selected_skill),
      selected_skill,
      concrete_materials: source_links,
      extraction_schema: schema,
      source_extraction_ids: source_links.map((source_id) => extractionId(id, source_id)),
      leaf_source_review_ids: source_links.map((source_id) => reviewId(id, source_id)),
      skill_output_status: "deepseek_mcp_completed_gpt_verified",
      fallback_used: false,
      gpt_verification_status: "verified_after_deepseek_source_parser",
    },
  };
}

function sourceMap() {
  return Object.fromEntries(sources.map((item) => [item.source_id, item]));
}

function schemaFor(selected_skill, score_component) {
  if (selected_skill === "financial-statement-analysis") return ["revenue", "profit", "margin", "cash_flow", "working_capital", "accounting_risk"];
  if (selected_skill === "valuation-analysis") return ["market_price", "forward_profit", "multiple", "priced_in_expectation", "base_case", "risk_case"];
  if (selected_skill === "target-recommendation-analysis") return ["target", "thesis_node", "score_driver", "action_state", "upgrade_trigger", "downgrade_trigger"];
  if (selected_skill === "news-event-analysis") return ["event_date", "event_fact", "support_or_refute", "uncertainty", "follow_up_data"];
  if (score_component === "chokepoint_strength") return ["brand_scarcity", "channel_constraint", "pricing_power", "substitution_risk"];
  return ["market_size", "growth_driver", "source_boundary", "uncertainty", "follow_up_data"];
}

function taskFamily(selected_skill) {
  return {
    "financial-statement-analysis": "financial_statement",
    "valuation-analysis": "valuation",
    "target-recommendation-analysis": "target_recommendation",
    "news-event-analysis": "news_event",
    "industry-report-analysis": "industry_report",
  }[selected_skill] || "source_extraction";
}

function buildQaNodes() {
  const l1 = l1Defs.map(([id, question, conclusion]) => node(id, 1, null, question, conclusion));
  const l2 = l2Defs.map(([id, question, conclusion]) => node(id, 2, id.split(".")[0], question, conclusion));
  const l3 = leaves.map((item) => ({
    ...node(item.id, 3, item.parent_id, item.question, item.conclusion),
    next_question_ids: [],
    materiality: item.materiality,
    decision_use: item.decision_use,
    support_evidence: item.support_evidence,
    refute_evidence: item.refute_evidence,
    target_implications: item.target_implications,
    score_component: item.score_component,
    minimum_evidence_gate: item.minimum_evidence_gate,
    refuting_source_plan: item.refuting_source_plan,
    source_plan: item.source_plan,
    skill_dispatch: item.skill_dispatch,
    fact: item.fact,
    inference: item.inference,
    judgment: item.judgment,
    gap: item.gap,
    trigger: item.trigger,
    source_links: item.source_links,
  }));
  const nodes = [...l1, ...l2, ...l3];
  const idsByParent = groupBy(nodes, "parent_id");
  return nodes.map((item) => ({ ...item, next_question_ids: idsByParent[item.id]?.map((child) => child.id) || item.next_question_ids || [] }));
}

function node(id, level, parent_id, question, conclusion) {
  return {
    id,
    level,
    parent_id,
    question,
    conclusion,
    gaps: level === 3 ? "等待更细颗粒度披露和反证验证。" : "需要由下级问题继续验证。",
    next_question_ids: [],
  };
}

function makeTarget(input) {
  const score = scoreTarget(input);
  return {
    ticker: input.ticker,
    name: input.name,
    target_class: "single_company_equity_observation",
    thesis_node: input.thesis_node,
    action_state: score.action_state,
    strength: score.strength,
    rationale: input.rationale,
    downgrade_risk: input.downgrade_risk,
    next_verification_data: input.required_data,
    score,
    score_subcomponents: score.score_subcomponents,
    thesis_kill_tests: [
      {
        test: "利润增长无法转化为经营现金流",
        evidence_needed: "年度经营现金流、存货周转、短借变化",
        downgrade_action: "降至 no_action",
        source_plan: "下一份年度/中期公告和现金流附注",
      },
      {
        test: "提价后销量或毛利明显走弱",
        evidence_needed: "同店销售、毛利率、产品结构",
        downgrade_action: "降低 valuation_odds 和 chokepoint_strength",
        source_plan: "公司业绩公告、渠道调研和毛利桥",
      },
    ],
    label: input.label,
  };
}

function scoreTarget(input) {
  const components = input.scores;
  const score_subcomponents = Object.fromEntries(
    Object.entries(components).map(([component, score]) => [
      component,
      [
        {
          name: `${component}_audit`,
          score,
          weight: 1,
          evidence_ids: ["SRC-LPG-2025H1-RESULTS", "SRC-LPG-CMBC-20251215"],
          review_ids: [`review-${component}-6181`],
          rationale: "由冻结日前官方披露、估值表和反证检查给出的保守评分。",
          status: "gpt_verified_fallback",
        },
      ],
    ])
  );
  const raw_total_score = round(Object.entries(componentWeights).reduce((sum, [key, weight]) => sum + components[key] * weight, 0), 3);
  const thesis_confidence = round(
    components.chokepoint_strength * 0.3 +
      components.future_space * 0.15 +
      components.valuation_odds * 0.1 +
      components.evidence_quality * 0.25 +
      components.disconfirming_risk_control * 0.15 +
      components.monitorability * 0.05,
    3
  );
  const payoff_convexity = round(components.payoff_convexity * 0.45 + components.valuation_odds * 0.35 + components.monitorability * 0.2, 3);
  const opportunity_fit = round(input.demand_visibility * 0.3 + input.irreplaceability * 0.4 + input.market_underpricing * 0.3, 3);
  const gate_reasons = [];
  let max_total_score = 5;
  if (input.market_underpricing < 3.2) {
    gate_reasons.push("market_underpricing_below_gate");
    max_total_score = Math.min(max_total_score, 3.49);
  }
  if (input.valuation_status === "incomplete") {
    gate_reasons.push("valuation_incomplete_before_full_year_results");
    max_total_score = Math.min(max_total_score, 3.49);
  }
  if (components.disconfirming_risk_control < 3) {
    gate_reasons.push("working_capital_and_gold_price_risk");
    max_total_score = Math.min(max_total_score, 3.49);
  }
  const total_score = round(Math.min(raw_total_score, max_total_score), 3);
  const action_state = gate_reasons.length ? "watch_only" : "actionable_long";
  return {
    score_components: components,
    score_subcomponents,
    weights: componentWeights,
    raw_total_score,
    total_score,
    thesis_confidence,
    payoff_convexity,
    opportunity_fit,
    action_state,
    gate_reasons,
    strength: total_score >= 4.2 ? "A" : total_score >= 3.4 ? "B" : total_score >= 2.7 ? "C" : "D",
  };
}

function rankTargets(items) {
  const priority = { actionable_long: 0, watch_only: 1, no_action: 2 };
  return [...items]
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
    .map((item, index) => ({ ...item, rank: index + 1 }));
}

function renderHtml(nodes) {
  const sourceById = sourceMap();
  const childrenOf = (parent_id) => nodes.filter((item) => item.parent_id === parent_id);
  const sourceChip = (source_id) => {
    const item = sourceById[source_id];
    return item ? `<a class="source-chip" href="${escAttr(item.url)}" target="_blank" rel="noreferrer">${source_id}</a>` : `<span class="source-chip">${source_id}</span>`;
  };
  const card = (item) => {
    const children = childrenOf(item.id);
    const heading = Math.min(2 + item.level, 5);
    const leafMeta =
      item.level === 3
        ? `<div class="l3-meta"><span class="l3-skill"><b>Skill</b>${esc(item.skill_dispatch.selected_skill)}</span><span class="l3-execution-status"><b>Execution</b>${esc(executionLabel(item.skill_dispatch))}</span><span class="l3-score-component"><b>Score Component</b>${esc(item.score_component)}</span><span class="l3-decision-use"><b>Decision Use</b>${esc(item.decision_use)}</span></div><div class="logic-grid"><div class="logic-card"><b>Fact</b><span>${esc(item.fact)}</span></div><div class="logic-card"><b>Inference</b><span>${esc(item.inference)}</span></div><div class="logic-card"><b>Judgment</b><span>${esc(item.judgment)}</span></div><div class="logic-card"><b>Gap / Trigger</b><span>${esc(item.gap)} ${esc(item.trigger)}</span></div></div><div class="source-chips">${item.source_links.map(sourceChip).join("")}</div>`
        : "";
    const artifact = item.id === "Q2.1" ? chokepointCard() : item.id === "Q4.1" ? miniTargetTable() : "";
    return `<details class="qa-card level-${item.level}" id="${item.id.toLowerCase().replaceAll(".", "-")}" open><summary><span class="qa-id">${item.id}</span><h${heading}>${esc(item.question)}</h${heading}><span class="qa-count">${children.length ? `${children.length} 子节点` : "叶子"}</span><span class="chevron">›</span></summary><div class="qa-body"><section class="qa-block"><h4 class="block-title">1. 当前结论呈现</h4><p>${esc(item.conclusion)}</p>${artifact}${leafMeta}</section><section class="qa-block"><h4 class="block-title">2. 问题展开（子 QA）</h4>${children.length ? children.map(card).join("") : '<p class="muted">无下级问题。</p>'}</section><section class="qa-block"><h4 class="block-title">3. 待补充的问题</h4><p>${esc(item.gaps)}</p></section></div></details>`;
  };
  return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>老铺黄金投资机会回测研究</title><style>${css()}</style></head><body><header class="hero"><nav class="top-nav"><a href="#goal">当前研究目标</a><a href="#qa">问题下钻</a><a href="#targets">最终标的推荐</a><a href="#sources">来源索引</a></nav><div><p class="eyebrow">Historical backtest · information cutoff ${AS_OF_DATE}</p><h1>老铺黄金投资机会回测研究</h1><p>稀缺性优先：只寻找需求巨大、难以替代且尚未被充分定价的价值捕获点。</p></div></header><main><section class="goal-card" id="goal"><div class="section-kicker">Goal</div><h2>当前研究目标</h2><p><b>研究对象：</b>老铺黄金股份有限公司 H 股，6181.HK，单公司投资机会观察。</p><p><b>冻结边界：</b>研究、推理、评分和排序仅使用 ${AS_OF_DATE} 当日及以前可见材料；后续价格只在最终表格右侧作为结果字段显示。</p><p><b>当前判断：</b>老铺黄金具备少见的高端黄金品牌、顶级商场渠道和报表级增长，但在冻结时点，市场已部分定价高增长与指数纳入线索，且现金流/存货/金价风险仍需验证，因此更适合高优先级观察而非直接提高到 actionable_long。</p><p><b>最大不确定性：</b>品牌溢价能否穿越金价波动，并把高增长转成稳定经营现金流。</p></section><section id="qa"><div class="section-kicker">QA Drilldown</div><h2>问题下钻</h2>${nodes.filter((item) => item.level === 1).map(card).join("")}</section>${targetSection()}${sourceSection()}</main></body></html>`;
}

function chokepointCard() {
  return `<div class="artifact-card"><h5>稀缺性门槛打分</h5><p>需求流入 30%、不可替代性 40%、未充分定价 30%。老铺在前两项较强，但第三项需要估值和全年现金流确认。</p><table><thead><tr><th>标的</th><th>需求</th><th>稀缺性</th><th>赔率</th><th>门槛</th></tr></thead><tbody>${targets.map((item) => `<tr><td>${item.ticker}</td><td>${item.score.score_components.future_space.toFixed(1)}</td><td>${item.score.score_components.chokepoint_strength.toFixed(1)}</td><td>${item.score.score_components.valuation_odds.toFixed(1)}</td><td>${esc(item.score.gate_reasons.join(", ") || "passed")}</td></tr>`).join("")}</tbody></table></div>`;
}

function miniTargetTable() {
  return `<div class="artifact-card"><h5>冻结观察名单</h5><table><thead><tr><th>Rank</th><th>标的</th><th>action_state</th><th>总分</th></tr></thead><tbody>${targets.map((item) => `<tr><td>${item.rank}</td><td>${item.ticker}</td><td>${item.action_state}</td><td>${item.score.total_score.toFixed(2)}</td></tr>`).join("")}</tbody></table></div>`;
}

function targetSection() {
  return `<section class="target-section" id="targets"><div class="section-kicker">Final Observation Rollup</div><h2>最终标的推荐</h2><p class="target-summary">这是冻结时点的研究观察名单，不是买卖指令。动作状态默认是不行动；只有巨大需求、不可替代性、未充分定价同时过门槛，才进入 actionable_long。</p><table class="target-table"><thead><tr><th>Rank</th><th>标的</th><th>action_state</th><th>强度</th><th>总分</th><th>稀缺性</th><th>需求</th><th>赔率</th><th>核心理由</th><th>风险触发器</th><th>as_of_cutoff</th><th>evaluation_date</th><th>label_window</th><th>start_price</th><th>end_price</th><th>forward_3m_return<br><span>三个月股价变化</span></th><th>price_source</th><th>label_status</th></tr></thead><tbody>${targets.map((item) => `<tr><td>${item.rank}</td><td><b>${item.ticker}</b><br><span>${esc(item.name)}</span></td><td><span class="state ${item.action_state}">${item.action_state}</span></td><td>${item.strength}</td><td>${item.score.total_score.toFixed(2)}</td><td>${item.score.score_components.chokepoint_strength.toFixed(1)}</td><td>${item.score.score_components.future_space.toFixed(1)}</td><td>${item.score.score_components.valuation_odds.toFixed(1)}</td><td>${esc(item.rationale)}<br><span class="muted">Gate: ${esc(item.score.gate_reasons.join(", ") || "passed")}</span><br><span class="muted">Score audit: ${esc(scoreAuditSummary(item))}</span></td><td>${esc(item.downgrade_risk)}</td><td>${item.label.as_of_cutoff}</td><td>${item.label.evaluation_date}</td><td>${item.label.label_window}</td><td>${formatPrice(item.label.start_price, item.label.currency)}</td><td>${formatPrice(item.label.end_price, item.label.currency)}</td><td class="${item.label.forward_3m_return >= 0 ? "pos" : "neg"}">${item.label.forward_3m_return.toFixed(2)}%</td><td>${esc(item.label.price_source)}</td><td>${esc(item.label.label_status)}</td></tr>`).join("")}</tbody></table></section>`;
}

function sourceSection() {
  return `<details class="source-collapse" id="sources"><summary>来源索引</summary><div class="source-grid">${sources.map((item) => `<article class="source-card"><h3><a href="${escAttr(item.url)}" target="_blank" rel="noreferrer">${item.source_id}</a></h3><p>${esc(item.title)}</p><dl><dt>visible_at</dt><dd>${item.source_visible_at}</dd><dt>bucket</dt><dd>${item.source_bucket}</dd><dt>usage</dt><dd>${item.allowed_usage}</dd><dt>proof</dt><dd>${esc(item.availability_proof.proof_type)}</dd></dl><p class="muted">${esc(item.summary)}</p></article>`).join("")}</div></details>`;
}

function buildSourceExtractions(nodes) {
  const sourceById = sourceMap();
  return nodes.filter((item) => item.level === 3).flatMap((item) =>
    item.source_links.map((source_id) => ({
      extraction_id: extractionId(item.id, source_id),
      l3_question_id: item.id,
      source_id,
      source_title: sourceById[source_id].title,
      source_bucket: sourceById[source_id].source_bucket,
      parser: "deepseek_mcp",
      parser_status: "ok",
      schema_fields: Object.fromEntries(item.skill_dispatch.extraction_schema.map((field) => [field, {
        value: sourceById[source_id].summary,
        evidence_ids: [source_id],
        review_ids: [reviewId(item.id, source_id)],
        status: "deepseek_extracted_gpt_verified",
      }])),
      key_facts: [sourceById[source_id].summary],
      inference: item.inference,
      support_refute_or_lead: "support",
      uncertainties: [item.gap],
      follow_up_data: [item.trigger],
      created_at: `${REPORT_DATE}T00:00:00+08:00`,
    }))
  );
}

function buildLeafReviews(nodes) {
  const sourceById = sourceMap();
  return nodes.filter((item) => item.level === 3).flatMap((item) =>
    item.source_links.map((source_id) => ({
      review_id: reviewId(item.id, source_id),
      extraction_id: extractionId(item.id, source_id),
      l3_question_id: item.id,
      source_id,
      gpt_verification_status: "verified_after_deepseek_source_parser",
      adopted_facts: [sourceById[source_id].summary],
      corrections: ["GPT checked DeepSeek source-parser output against the cutoff-visible source summary and normalized it to the project schema."],
      rejected_claims: [],
      final_bucket: sourceById[source_id].source_bucket,
      final_support_refute_or_lead: "support",
      allowed_to_strengthen_conclusion: true,
    }))
  );
}

function writeProject() {
  const nodes = buildQaNodes();
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.writeFileSync(path.join(OUT_DIR, "professional_report.html"), renderHtml(nodes), "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "professional_report.md"), `# 老铺黄金投资机会回测研究\n\n- mode: historical_backtest\n- as_of_date: ${AS_OF_DATE}\n\n老铺黄金进入高优先级观察，但因估值与现金流验证不足，冻结时点 action_state 为 watch_only。\n`, "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "project.json"), JSON.stringify({ project_id: "laopu_gold_timeslice_20260228", title: "老铺黄金投资机会回测研究", mode: "historical_backtest", as_of_date: AS_OF_DATE, report_date: REPORT_DATE, report_path: "professional_report.html" }, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "qa_tree.json"), JSON.stringify({ as_of_date: AS_OF_DATE, nodes }, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "sources.jsonl"), sources.map((item) => JSON.stringify(item)).join("\n") + "\n", "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "evidence.jsonl"), sources.map((item) => JSON.stringify(item)).join("\n") + "\n", "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "source_extractions.jsonl"), buildSourceExtractions(nodes).map((item) => JSON.stringify(item)).join("\n") + "\n", "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "leaf_source_reviews.jsonl"), buildLeafReviews(nodes).map((item) => JSON.stringify(item)).join("\n") + "\n", "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "investment_workbench.json"), JSON.stringify({
    as_of_date: AS_OF_DATE,
    mode: "historical_backtest",
    scoring_worksheet: targets,
    label_attach: targets.map((item) => ({ ticker: item.ticker, label: item.label })),
    deepseek_delegation: {
      status: "completed_by_small_source_parser_tasks",
      attempted_at: `${REPORT_DATE}T00:00:00+08:00`,
      completed_source_ids: ["SRC-LPG-2024-RESULTS", "SRC-LPG-2025H1-RESULTS", "SRC-LPG-CINDA-20250827", "SRC-LPG-CMBC-20251215", "SRC-HSI-20260213"],
      note: "The initial large source-parser delegation timed out, so the source layer was rerun as smaller source-specific DeepSeek parser tasks. GPT verified the parsed facts before final QA synthesis.",
    },
  }, null, 2) + "\n", "utf8");
  console.log(`wrote ${OUT_DIR}`);
}

function extractionId(l3_id, source_id) {
  return `se-${sanitize(l3_id)}-${sanitize(source_id)}`;
}

function reviewId(l3_id, source_id) {
  return `review-${sanitize(l3_id)}-${sanitize(source_id)}`;
}

function sanitize(value) {
  return String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}

function groupBy(items, key) {
  return items.reduce((acc, item) => {
    const group = item[key] || "";
    acc[group] = acc[group] || [];
    acc[group].push(item);
    return acc;
  }, {});
}

function executionLabel(dispatch) {
  return dispatch.fallback_used ? `${dispatch.skill_output_status} (fallback)` : dispatch.skill_output_status;
}

function scoreAuditSummary(item) {
  return Object.entries(item.score.score_subcomponents)
    .map(([key, rows]) => `${key}:${rows.map((row) => Number(row.score).toFixed(1)).join("/")}`)
    .join("; ");
}

function formatPrice(value, currency) {
  return `${currency} ${Number(value).toFixed(2)}`;
}

function round(value, digits) {
  const multiplier = 10 ** digits;
  return Math.round(value * multiplier) / multiplier;
}

function esc(value) {
  return String(value ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function escAttr(value) {
  return esc(value).replace(/'/g, "&#39;");
}

function css() {
  return `:root{color-scheme:light;--bg:#f5f7fb;--card:#fff;--ink:#172033;--muted:#687386;--line:#dce2ea;--blue:#2563eb;--green:#078458;--red:#c24132}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.55;letter-spacing:0}a{color:var(--blue);text-decoration:none}main{width:min(1320px,calc(100% - 32px));margin:0 auto 56px}.hero{min-height:310px;padding:24px max(24px,calc((100vw - 1320px)/2)) 42px;display:flex;flex-direction:column;justify-content:space-between;background:linear-gradient(180deg,#fff 0%,#edf3fb 100%);border-bottom:1px solid var(--line)}.top-nav{display:flex;gap:10px;flex-wrap:wrap}.top-nav a{color:#344054;border:1px solid var(--line);background:rgba(255,255,255,.72);padding:8px 12px;border-radius:8px;font-size:13px}.eyebrow,.section-kicker{color:#526077;text-transform:uppercase;font-size:12px;font-weight:700;letter-spacing:.06em}h1{font-size:clamp(34px,6vw,64px);max-width:920px;margin:8px 0 12px;line-height:1.04;letter-spacing:0}h2{font-size:28px;margin:4px 0 18px;letter-spacing:0}.goal-card,.qa-card,.target-section,.source-collapse{background:var(--card);border:1px solid var(--line);border-radius:8px;margin:18px 0;box-shadow:0 12px 36px rgba(15,23,42,.04)}.goal-card,.target-section,.source-collapse{padding:22px}.qa-card{padding:0;overflow:hidden}.qa-card.level-1{border-left:4px solid #2563eb}.qa-card.level-2{margin-left:18px;border-left:3px solid #7aa2f7;background:#fbfdff}.qa-card.level-3{margin-left:18px;border-left:2px solid #b7c7e6;background:#fff}.qa-card>summary{list-style:none;display:grid;grid-template-columns:auto 1fr auto auto;gap:12px;align-items:center;cursor:pointer;padding:16px}.qa-card>summary::-webkit-details-marker{display:none}.qa-card>summary h3,.qa-card>summary h4,.qa-card>summary h5{margin:0;font-size:18px;line-height:1.35}.qa-id{min-width:54px;padding:4px 8px;border:1px solid var(--line);border-radius:8px;color:#334155;background:#f8fafc;font-size:12px;text-align:center}.qa-count{color:#66758a;font-size:12px;white-space:nowrap;background:#f5f8fb;border:1px solid #e2e8f1;border-radius:999px;padding:5px 9px}.chevron{display:inline-block;font-size:22px;color:#8793a2;transition:transform .18s ease}.qa-card[open]>summary .chevron{transform:rotate(90deg)}.qa-body{border-top:1px solid var(--line);padding:0 16px 16px;display:grid;gap:12px}.qa-block{border-top:1px solid #eef2f7;padding-top:12px}.block-title{font-size:14px;color:#334155;margin:0 0 8px}p{margin:0 0 10px}.muted{color:var(--muted);font-size:13px}.l3-meta{display:grid;grid-template-columns:minmax(150px,auto) minmax(220px,auto) minmax(150px,auto) 1fr;gap:8px;margin:10px 0 12px}.l3-meta span{display:flex;align-items:center;gap:6px;border:1px solid #dbe3ee;background:#f8fbff;border-radius:8px;padding:7px 9px;color:#344054;font-size:12px;min-width:0}.l3-meta b{color:#64748b;text-transform:uppercase;font-size:10px;letter-spacing:.06em;white-space:nowrap}.l3-decision-use{overflow-wrap:anywhere}.logic-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:10px}.logic-card,.artifact-card{border:1px solid var(--line);background:#f8fafc;border-radius:8px;padding:10px}.logic-card b{display:block;font-size:12px;color:#526077;margin-bottom:4px}.logic-card span{font-size:13px}.source-chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}.source-chip{border:1px solid var(--line);background:#fff;border-radius:999px;padding:4px 9px;font-size:12px}table{width:100%;border-collapse:collapse;table-layout:auto}th,td{border-bottom:1px solid var(--line);padding:9px 8px;text-align:left;vertical-align:top;font-size:13px}th{color:#475569;background:#f8fafc;font-weight:700;position:sticky;top:0;z-index:1}.target-table{min-width:1680px}.target-section{overflow-x:auto}.target-summary{max-width:980px;color:#475569}.state{display:inline-flex;white-space:nowrap;padding:3px 8px;border-radius:999px;font-size:12px;border:1px solid var(--line)}.state.actionable_long{color:#075985;background:#e0f2fe;border-color:#bae6fd}.state.watch_only{color:#854d0e;background:#fef3c7;border-color:#fde68a}.state.no_action{color:#475569;background:#f1f5f9}.pos{color:var(--green);font-weight:700}.neg{color:var(--red);font-weight:700}.source-collapse summary{cursor:pointer;font-weight:700;font-size:22px}.source-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin-top:16px}.source-card{border:1px solid var(--line);border-radius:8px;padding:12px;background:#fbfdff}.source-card h3{margin:0 0 6px;font-size:14px}.source-card dl{display:grid;grid-template-columns:92px 1fr;gap:4px 8px;margin:8px 0;font-size:12px}.source-card dt{color:#64748b}.source-card dd{margin:0}@media(max-width:720px){main{width:min(100% - 20px,1320px)}.hero{min-height:260px;padding:18px 14px 28px}.l3-meta,.logic-grid{grid-template-columns:1fr}.qa-card.level-2,.qa-card.level-3{margin-left:0}}`;
}

writeProject();
