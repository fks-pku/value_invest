const fs = require("fs");
const path = require("path");

const generatedAt = "2026-05-29T00:00:00+08:00";
const base = path.join("research", "bom", "pop_mart_related_opportunities");
fs.mkdirSync(base, { recursive: true });

const urls = {
  popAnnual:
    "https://www.hkexnews.hk/listedco/listconews/sehk/2026/0325/2026032500285.pdf",
  popQ1:
    "https://www.scmp.com/business/china-business/article/3310251/pop-marts-overseas-revenue-falls-despite-labubu-craze-amid-us-china-trade-war",
  popReuters:
    "https://www.reuters.com/world/china/chinas-pop-mart-expects-2026-revenue-top-20-billion-yuan-chairman-says-2026-03-27/",
  popSony:
    "https://www.reuters.com/business/media-telecom/sony-develop-labubu-feature-film-deadline-reports-2026-05-09/",
  minisoAnnual:
    "https://filecache.investorroom.com/mr5ir_miniso/368/Annual%20Report%202025%20HK.pdf",
  minisoQuarter:
    "https://ir.miniso.com/news-releases/news-release-details/miniso-announces-march-quarter-2026-unaudited-financial-results",
  bloksAnnual:
    "https://www.hkexnews.hk/listedco/listconews/sehk/2026/0327/2026032701144.pdf",
  dreamAnnual:
    "https://www.hkexnews.hk/listedco/listconews/sehk/2026/0408/2026040802047.pdf",
  sanrioStats: "https://stockanalysis.com/quote/tyo/8136/financials/",
  bandaiResults: "https://www.bandainamco.co.jp/en/ir/library/result.html",
  funkoResults:
    "https://investor.funko.com/news-and-events/press-releases/Press-Releases/2026/Funko-Reports-2025-Fourth-Quarter-Full-Year-Financial-Results-Provides-Full-Year-Outlook-for-2026/default.aspx",
  mattelResults:
    "https://investors.mattel.com/news-releases/news-release-details/mattel-reports-fourth-quarter-and-full-year-2025-financial",
  popStats: "https://stockanalysis.com/quote/hkg/9992/statistics/",
  bloksStats: "https://stockanalysis.com/quote/hkg/0325/statistics/",
  minisoStats: "https://stockanalysis.com/stocks/mnso/statistics/",
  sanrioRatios: "https://stockanalysis.com/quote/tyo/8136/financials/ratios/",
  fnkoStats: "https://stockanalysis.com/stocks/fnko/statistics/",
  counterfeit:
    "https://www.tomshardware.com/3d-printing/bambu-lab-and-printables-vr-face-lawsuit-from-pop-mart-over-labubu-3d-models-the-makerworld-platform-owner-has-been-sued-in-california-along-with-several-other-companies"
};

const evidence = [
  {
    id: "ev_pop_2025_annual_results",
    source_name: "Pop Mart 2025 annual results announcement",
    source_type: "company announcement",
    information_category: "evidence",
    published_at: "2026-03-25",
    reliability: "high",
    support_refute_or_lead: "support",
    tickers: ["9992.HK"],
    summary:
      "泡泡玛特 2025 年收入 RMB37.120B，同比+184.7%；毛利 RMB26.765B，同比+207.4%；经营利润 RMB16.890B，同比+306.6%；归母利润 RMB12.776B，同比+308.8%；Non-IFRS adjusted net profit RMB13.084B，同比+284.5%。",
    url: urls.popAnnual,
    used_in: ["q1-1-1-pop-demand", "q2-1-1-ip-engine", "q4-1-1-target-ranking"]
  },
  {
    id: "ev_pop_2025_ip_region_mix",
    source_name: "Pop Mart 2025 IP and region mix",
    source_type: "company announcement",
    information_category: "evidence",
    published_at: "2026-03-25",
    reliability: "high",
    support_refute_or_lead: "support",
    tickers: ["9992.HK"],
    summary:
      "THE MONSTERS 收入 RMB14.161B，占 38.1%；SKULLPANDA RMB3.540B；CRYBABY RMB2.929B；MOLLY RMB2.897B；海外区域中美洲收入 RMB6.806B，同比+748.4%，欧洲及其他 RMB1.451B，同比+506.3%。",
    url: urls.popAnnual,
    used_in: ["q1-1-1-pop-demand", "q2-1-1-ip-engine", "q3-1-1-labubu-risk"]
  },
  {
    id: "ev_pop_2025_product_mix",
    source_name: "Pop Mart 2025 product mix",
    source_type: "company announcement",
    information_category: "evidence",
    published_at: "2026-03-25",
    reliability: "high",
    support_refute_or_lead: "support",
    tickers: ["9992.HK"],
    summary:
      "2025 年 plush toys 收入 RMB18.708B，占 50.4%，同比+560.6%；figure toys RMB12.023B，占 32.4%。Labubu/搪胶毛绒从收藏玩具扩展为可穿戴/社交展示品。",
    url: urls.popAnnual,
    used_in: ["q2-1-2-product-supply", "q3-1-1-labubu-risk"]
  },
  {
    id: "ev_pop_q1_2026_update",
    source_name: "Pop Mart Q1 2026 business update / SCMP coverage",
    source_type: "news with company update",
    information_category: "message",
    published_at: "2026-05-12",
    reliability: "medium",
    support_refute_or_lead: "lead",
    tickers: ["9992.HK"],
    summary:
      "媒体引用 2026Q1 业务更新称整体收入同比+75%-80%，中国+100%-105%，亚太+25%-30%，美洲+55%-60%，欧洲及其他+60%-65%；但也指出海外环比转弱，暴露海外用户积累不足。",
    url: urls.popQ1,
    used_in: ["q1-1-1-pop-demand", "q3-1-2-overseas-risk"]
  },
  {
    id: "ev_pop_reuters_2026_target",
    source_name: "Reuters coverage of Pop Mart revenue aspiration",
    source_type: "news",
    information_category: "message",
    published_at: "2026-03-27",
    reliability: "medium",
    support_refute_or_lead: "lead",
    tickers: ["9992.HK"],
    summary:
      "Reuters 报道泡泡玛特董事长预计 2026 年收入超过 RMB20B 的说法；相较 2025 年实际收入 RMB37.1B，这类管理层表述需要结合公司公告、口径和后续更新核验。",
    url: urls.popReuters,
    used_in: ["q3-1-3-guidance-valuation"]
  },
  {
    id: "ev_pop_sony_labubu_film",
    source_name: "Reuters / Deadline on Sony Labubu film",
    source_type: "news",
    information_category: "message",
    published_at: "2026-05-09",
    reliability: "medium",
    support_refute_or_lead: "lead",
    tickers: ["9992.HK", "SONY"],
    summary:
      "媒体报道 Sony 正在开发 Labubu 电影。若后续落地，说明 Pop Mart 试图把角色从玩具 IP 扩展为内容 IP；当前只能作为线索，不能直接强化财务判断。",
    url: urls.popSony,
    used_in: ["q2-2-1-content-licensing", "q4-1-1-target-ranking"]
  },
  {
    id: "ev_miniso_2025_annual",
    source_name: "MINISO 2025 annual report",
    source_type: "company annual report",
    information_category: "evidence",
    published_at: "2026-04-28",
    reliability: "high",
    support_refute_or_lead: "support",
    tickers: ["MNSO", "9896.HK"],
    summary:
      "名创优品 2025 年收入 RMB21.444B，同比+26.2%；MINISO brand RMB19.525B，同比+22.0%；TOP TOY RMB1.916B，同比+94.8%；毛利率 45.0%。TOP TOY 覆盖手办、3D 积木、vinyl plush 等潮玩品类。",
    url: urls.minisoAnnual,
    used_in: ["q1-2-1-adjacent-demand", "q2-1-3-retail-channel", "q4-1-1-target-ranking"]
  },
  {
    id: "ev_miniso_q1_2026",
    source_name: "MINISO March quarter 2026 results",
    source_type: "company earnings release",
    information_category: "evidence",
    published_at: "2026-05-15",
    reliability: "high",
    support_refute_or_lead: "support",
    tickers: ["MNSO", "9896.HK"],
    summary:
      "名创优品 2026 年 3 月季度公告显示收入继续增长，TOP TOY 仍是重要增长线索；用于验证潮玩零售相邻需求而非直接替代泡泡玛特。",
    url: urls.minisoQuarter,
    used_in: ["q1-2-1-adjacent-demand", "q4-1-1-target-ranking"]
  },
  {
    id: "ev_bloks_2025_annual",
    source_name: "Bloks Group 2025 annual report",
    source_type: "company annual report",
    information_category: "evidence",
    published_at: "2026-03-27",
    reliability: "high",
    support_refute_or_lead: "support",
    tickers: ["0325.HK"],
    summary:
      "布鲁可 2025 年收入 RMB2.913B，同比+30.0%；adjusted profit RMB674.9M，同比+15.5%；profit RMB633.7M，扭亏为盈；拥有近 550 个专利组合和 Bloks System 标准化，IP 包括奥特曼、变形金刚、迪士尼等授权 IP。",
    url: urls.bloksAnnual,
    used_in: ["q1-2-1-adjacent-demand", "q2-1-4-licensed-ip", "q4-1-1-target-ranking"]
  },
  {
    id: "ev_dream_2025_annual",
    source_name: "Dream International 2025 annual report",
    source_type: "company annual report",
    information_category: "evidence",
    published_at: "2026-04-08",
    reliability: "high",
    support_refute_or_lead: "refute",
    tickers: ["1126.HK"],
    summary:
      "Dream International 2025 年收入 HK$5.974B，同比+9.6%；毛利率 20.2%，低于 2024 年 23.0%；归母利润 HK$692.9M，同比下降；plush stuffed toys HK$3.264B，占 54.6%，同比+18.0%；四个客户各超过 10% 收入。",
    url: urls.dreamAnnual,
    used_in: ["q2-1-2-product-supply", "q4-1-1-target-ranking"]
  },
  {
    id: "ev_sanrio_financial_snapshot",
    source_name: "Sanrio financial snapshot",
    source_type: "third-party financial data",
    information_category: "research_report",
    published_at: "2026-05-28",
    reliability: "medium",
    support_refute_or_lead: "support",
    tickers: ["8136.T"],
    summary:
      "Sanrio FY2025 revenue JPY144.904B，同比+44.93%；operating income JPY51.806B；net income JPY41.731B；TTM revenue JPY183.312B。多角色授权模型证明全球角色 IP 可持续放大，但需统一官方年报和估值口径。",
    url: urls.sanrioStats,
    used_in: ["q1-2-1-adjacent-demand", "q2-2-1-content-licensing", "q4-1-1-target-ranking"]
  },
  {
    id: "ev_bandai_ip_synergy",
    source_name: "Bandai Namco IR materials",
    source_type: "company IR library",
    information_category: "evidence",
    published_at: "2026-05-08",
    reliability: "high",
    support_refute_or_lead: "support",
    tickers: ["7832.T"],
    summary:
      "Bandai Namco 以 Gundam 等长周期 IP 为核心，横跨玩具、模型、卡牌、游戏和娱乐内容。它是成熟 IP synergy 的对照标的，说明角色 IP 变现可跨品类，但和泡泡玛特的年轻潮玩路径并不完全相同。",
    url: urls.bandaiResults,
    used_in: ["q2-2-1-content-licensing", "q4-1-1-target-ranking"]
  },
  {
    id: "ev_funko_2025_results",
    source_name: "Funko 2025 results",
    source_type: "company earnings release",
    information_category: "evidence",
    published_at: "2026-03-05",
    reliability: "high",
    support_refute_or_lead: "refute",
    tickers: ["FNKO"],
    summary:
      "Funko 2025 年 net sales $908.2M，低于 2024 年 $1.05B；gross margin 38.7%，低于 41.4%；net loss $67.4M。Funko 是收藏玩具热度退潮、库存和授权组合风险的反面样本。",
    url: urls.funkoResults,
    used_in: ["q1-2-1-adjacent-demand", "q3-1-1-labubu-risk", "q4-1-1-target-ranking"]
  },
  {
    id: "ev_mattel_2025_results",
    source_name: "Mattel 2025 results",
    source_type: "company earnings release",
    information_category: "evidence",
    published_at: "2026-02-04",
    reliability: "high",
    support_refute_or_lead: "lead",
    tickers: ["MAT"],
    summary:
      "Mattel 2025 年 Dolls gross billings $2.056B，同比-7%；Vehicles gross billings $1.995B，同比+11%。说明传统玩具 IP 组合内部也会分化，单一角色或品类不可线性外推。",
    url: urls.mattelResults,
    used_in: ["q1-2-1-adjacent-demand", "q3-1-1-labubu-risk"]
  },
  {
    id: "ev_pop_counterfeit_ip_enforcement",
    source_name: "Tom's Hardware coverage of Pop Mart IP enforcement lawsuit",
    source_type: "news",
    information_category: "message",
    published_at: "2026-05-20",
    reliability: "medium",
    support_refute_or_lead: "lead",
    tickers: ["9992.HK"],
    summary:
      "媒体报道泡泡玛特在美国对 Labubu 3D 模型相关平台和公司提起诉讼。它说明 IP 保护和盗版/仿品治理已成为全球化后的重要变量。",
    url: urls.counterfeit,
    used_in: ["q3-1-2-overseas-risk"]
  },
  {
    id: "ev_valuation_snapshot_pop_related",
    source_name: "StockAnalysis valuation snapshots",
    source_type: "third-party market data",
    information_category: "message",
    published_at: "2026-05-28",
    reliability: "medium",
    support_refute_or_lead: "lead",
    tickers: ["9992.HK", "0325.HK", "MNSO", "8136.T", "FNKO"],
    summary:
      "估值快照显示 9992.HK PE 约 15.15、forward PE 约 13.22、P/S 约 5.16；0325.HK P/S 约 4.34；MNSO、8136.T、FNKO 等需统一日期、股本、净现金和 forward estimates 后再做赔率判断。第三方数据只能作为 lead。",
    url: urls.popStats,
    used_in: ["q3-2-1-valuation", "q4-1-1-target-ranking"]
  }
];

const evidenceMap = Object.fromEntries(evidence.map((e) => [e.id, e]));

const sourceExtractions = [
  {
    extraction_id: "ext_pop_annual_q1_1_1_ds_20260529",
    l3_question_id: "q1-1-1-pop-demand",
    source_id: "ev_pop_2025_annual_results",
    source_title: "泡泡玛特 2025 年业绩摘录",
    source_bucket: "evidence/research_report/opinion/message",
    parser: "deepseek_delegate",
    parser_status: "ok",
    key_facts: [
      "2025年收入371.20亿元，同比增长184.7%",
      "毛利267.65亿元，同比增长207.4%",
      "经营利润168.90亿元，同比增长306.6%",
      "归母利润127.76亿元，同比增长308.8%",
      "Non-IFRS调整净利润130.84亿元，同比增长284.5%",
      "THE MONSTERS收入141.61亿元，占总收入38.1%",
      "毛绒玩具收入187.08亿元，占总收入50.4%，同比增长560.6%",
      "手办收入120.23亿元，占总收入32.4%"
    ],
    inference: [
      "THE MONSTERS贡献超38%收入，显示单一IP具有极强变现能力",
      "毛绒玩具品类爆发式增长，表明IP衍生形态创新能提升财务转化",
      "利润增速显著高于收入增速，说明IP运营具有经营杠杆"
    ],
    support_refute_or_lead: "support",
    affected_qa_node: "q1-1-1-pop-demand",
    uncertainties: ["高增速是否可持续", "THE MONSTERS单一IP占比过高", "毛绒玩具爆发是短期还是长期趋势"],
    follow_up_data: ["各IP历史收入趋势", "用户复购率", "海外收入占比", "销售渠道构成"],
    created_at: generatedAt
  },
  {
    extraction_id: "ext_miniso_toptoy_q1_2_1_ds_20260529",
    l3_question_id: "q1-2-1-adjacent-demand",
    source_id: "ev_miniso_2025_annual",
    source_title: "MINISO 2025 annual report & March quarter 2026 results",
    source_bucket: "evidence",
    parser: "deepseek_delegate",
    parser_status: "ok",
    key_facts: [
      "MINISO 2025全年总收入214.44亿元人民币，同比增长26.2%",
      "MINISO品牌收入195.25亿元，同比增长22.0%",
      "TOP TOY收入19.16亿元，同比增长94.8%",
      "整体毛利率45.0%",
      "TOP TOY覆盖模型手办、3D积木、vinyl plush等潮玩品类",
      "2026年3月季度收入继续增长，TOP TOY仍是重要增长线索"
    ],
    inference: [
      "TOP TOY增速远超MINISO主品牌，显示潮玩品类需求强劲",
      "TOP TOY品类覆盖与泡泡玛特存在重叠，表明潮玩需求有相邻扩散迹象",
      "高毛利率和持续增长验证潮玩市场消费韧性"
    ],
    support_refute_or_lead: "support",
    affected_qa_node: "q1-2-1-adjacent-demand",
    uncertainties: ["TOP TOY与泡泡玛特用户画像、价格带、IP来源重叠程度未明确", "无法判断增长是新用户还是分流"],
    follow_up_data: ["TOP TOY与泡泡玛特品类和价格带对比", "用户调研", "潮玩行业第三方规模"],
    created_at: generatedAt
  },
  {
    extraction_id: "ext_bloks_q2_1_4_ds_20260529",
    l3_question_id: "q2-1-4-licensed-ip",
    source_id: "ev_bloks_2025_annual",
    source_title: "Bloks Group 2025 annual report",
    source_bucket: "evidence",
    parser: "deepseek_delegate",
    parser_status: "ok",
    key_facts: [
      "收入 RMB2.913B，同比+30.0%",
      "adjusted profit RMB674.9M，同比+15.5%",
      "profit RMB633.7M，扭亏为盈",
      "近550个专利组合和Bloks System标准化",
      "主要是拼搭角色类玩具",
      "IP包括奥特曼、变形金刚、迪士尼等授权IP"
    ],
    inference: [
      "授权IP拼搭角色类玩具商业模式具有可行性",
      "专利和Bloks System显示标准化产品系统积累",
      "当前模式以授权IP为主，而非自有IP"
    ],
    support_refute_or_lead: "lead",
    affected_qa_node: "q2-1-4-licensed-ip",
    uncertainties: ["授权IP续约风险和成本变化未披露", "标准化产品系统与泡泡玛特模式的异同需进一步对比"],
    follow_up_data: ["授权IP合同期限和续约条件", "自有IP开发和收入占比", "拼搭角色类玩具市场竞争格局"],
    created_at: generatedAt
  },
  {
    extraction_id: "ext_dream_q2_1_2_ds_20260529",
    l3_question_id: "q2-1-2-product-supply",
    source_id: "ev_dream_2025_annual",
    source_title: "Dream International 2025 annual report",
    source_bucket: "evidence",
    parser: "deepseek_delegate",
    parser_status: "ok",
    key_facts: [
      "收入 HK$5.974B，同比+9.6%",
      "毛利率20.2%（2024为23.0%），归母利润同比下降",
      "Plush stuffed toys 收入 HK$3.264B，占54.6%，同比+18.0%",
      "plastic figures 收入 HK$2.352B，占39.4%",
      "客户集中，四个客户各超过10%收入",
      "产能分布在中国、越南、印尼"
    ],
    inference: [
      "毛绒玩具是最大品类且增长较快，可能受益于潮玩需求，但无法确认泡泡玛特是否为四大客户之一",
      "毛利率下降和利润下滑表明公司可能面临成本压力或定价权不足",
      "供应链即使捕获需求，也未必能捕获主要利润"
    ],
    support_refute_or_lead: "lead",
    affected_qa_node: "q2-1-2-product-supply",
    uncertainties: ["泡泡玛特是否为客户及收入占比未知", "毛利率下降原因不明", "plastic figures中潮玩品类占比未知"],
    follow_up_data: ["前四大客户名称及收入占比", "plastic figures分品类收入", "毛利率下降驱动因素"],
    created_at: generatedAt
  },
  {
    extraction_id: "ext_funko_mattel_q3_1_1_ds_20260529",
    l3_question_id: "q3-1-1-labubu-risk",
    source_id: "ev_funko_2025_results",
    source_title: "Funko 和 Mattel 2025 年业绩材料摘录",
    source_bucket: "evidence",
    parser: "deepseek_delegate",
    parser_status: "ok",
    key_facts: [
      "Funko 2025 年净销售额 9.082 亿美元，同比下降约 13.5%",
      "Funko 2025 年毛利率 38.7%，低于 2024 年的 41.4%",
      "Funko 2025 年净亏损 6740 万美元",
      "Mattel 2025 年娃娃类总开票额 20.56 亿美元，同比下降 7%",
      "Mattel 2025 年车辆类总开票额 19.95 亿美元，同比增长 11%",
      "Barbie 下滑，Hot Wheels 增长"
    ],
    inference: [
      "收藏玩具模式可能面临需求疲软和盈利压力",
      "传统玩具品类内部明显分化，IP生命周期管理很关键",
      "Funko 可作为泡泡玛特海外扩张的潜在风险参照，但两者IP来源和渠道结构不同"
    ],
    support_refute_or_lead: "lead",
    affected_qa_node: "q3-1-1-labubu-risk",
    uncertainties: ["Funko困境是公司问题还是行业趋势不确定", "Mattel娃娃品类与泡泡玛特目标客群可比性有限"],
    follow_up_data: ["泡泡玛特分地区收入", "泡泡玛特库存周转", "全球潮玩市场规模", "Funko与泡泡玛特IP来源和渠道对比"],
    created_at: generatedAt
  }
];

const leafSourceReviews = [
  {
    review_id: "rev_pop_annual_q1_1_1_20260529",
    extraction_id: "ext_pop_annual_q1_1_1_ds_20260529",
    l3_question_id: "q1-1-1-pop-demand",
    source_id: "ev_pop_2025_annual_results",
    gpt_verification_status: "verified_with_corrections",
    adopted_facts: sourceExtractions[0].key_facts,
    corrections: [
      "source_bucket corrected from placeholder string to evidence",
      "DeepSeek inference that multiple IPs lower single-IP risk is only partially accepted; THE MONSTERS 38.1% remains a concentration risk"
    ],
    rejected_claims: ["Do not conclude IP matrix risk is low without 2026 IP-by-IP follow-up data"],
    final_bucket: "evidence",
    final_support_refute_or_lead: "support",
    allowed_to_strengthen_conclusion: true,
    created_at: generatedAt
  },
  {
    review_id: "rev_miniso_toptoy_q1_2_1_20260529",
    extraction_id: "ext_miniso_toptoy_q1_2_1_ds_20260529",
    l3_question_id: "q1-2-1-adjacent-demand",
    source_id: "ev_miniso_2025_annual",
    gpt_verification_status: "verified_with_boundary",
    adopted_facts: sourceExtractions[1].key_facts,
    corrections: ["45.0% gross margin is company-level, not proven TOP TOY-only"],
    rejected_claims: ["Do not infer TOP TOY directly substitutes or displaces Pop Mart demand"],
    final_bucket: "evidence",
    final_support_refute_or_lead: "support",
    allowed_to_strengthen_conclusion: true,
    created_at: generatedAt
  },
  {
    review_id: "rev_bloks_q2_1_4_20260529",
    extraction_id: "ext_bloks_q2_1_4_ds_20260529",
    l3_question_id: "q2-1-4-licensed-ip",
    source_id: "ev_bloks_2025_annual",
    gpt_verification_status: "verified_as_lead",
    adopted_facts: sourceExtractions[2].key_facts,
    corrections: ["Keep support_refute_or_lead as lead because licensed-IP economics require more evidence on authorization cost and self-owned IP"],
    rejected_claims: [],
    final_bucket: "evidence",
    final_support_refute_or_lead: "lead",
    allowed_to_strengthen_conclusion: false,
    created_at: generatedAt
  },
  {
    review_id: "rev_dream_q2_1_2_20260529",
    extraction_id: "ext_dream_q2_1_2_ds_20260529",
    l3_question_id: "q2-1-2-product-supply",
    source_id: "ev_dream_2025_annual",
    gpt_verification_status: "verified_as_boundary_evidence",
    adopted_facts: sourceExtractions[3].key_facts,
    corrections: ["Final use is refuting/boundary evidence for supplier value capture, not support for Dream as a high-priority target"],
    rejected_claims: ["Do not assume Pop Mart is one of the disclosed major customers"],
    final_bucket: "evidence",
    final_support_refute_or_lead: "refute",
    allowed_to_strengthen_conclusion: true,
    created_at: generatedAt
  },
  {
    review_id: "rev_funko_mattel_q3_1_1_20260529",
    extraction_id: "ext_funko_mattel_q3_1_1_ds_20260529",
    l3_question_id: "q3-1-1-labubu-risk",
    source_id: "ev_funko_2025_results",
    gpt_verification_status: "verified_as_refuting_boundary",
    adopted_facts: sourceExtractions[4].key_facts,
    corrections: ["Final use is a refuting boundary for collectible-toy cycles; not direct proof Pop Mart will follow Funko"],
    rejected_claims: [],
    final_bucket: "evidence",
    final_support_refute_or_lead: "refute",
    allowed_to_strengthen_conclusion: true,
    created_at: generatedAt
  }
];

const scoreSchema = {
  total: 100,
  dimensions: [
    ["demand_flow", "需求流入", 18],
    ["ip_control", "IP 控制/不可替代", 20],
    ["distribution", "渠道与全球化触达", 14],
    ["product_supply", "产品迭代与供应链", 12],
    ["financial_conversion", "财务转化", 16],
    ["valuation_odds", "估值赔率", 12],
    ["monitorability", "可跟踪性/反证清晰度", 8]
  ],
  downgrade_rules: [
    "单一 IP 收入占比继续上升但新 IP 无法接力：IP 控制分不升反降。",
    "海外增长环比或同店连续转弱：渠道全球化分下调。",
    "毛利率/经营利润率连续两个季度下行且收入仍高增：财务转化分下调。",
    "第三方估值数据未统一口径：估值赔率不得上调为强。"
  ]
};

const chokepoints = [
  ["原创 IP 运营", "9992.HK, 8136.T", 88, "角色心智、社群、稀缺发售、跨品类复购", "THE MONSTERS 占比高，热度周期和盗版风险"],
  ["全球 DTC 与零售渠道", "9992.HK, MNSO/9896.HK", 78, "门店/线上/海外渠道能把 IP 热度转成收入", "海外用户沉淀不足、关税和本地竞争"],
  ["授权 IP 与标准化积木/玩具系统", "0325.HK, 7832.T", 72, "授权 IP + 产品系统降低单一原创 IP 风险", "授权成本、IP 到期、差异化弱于原创角色"],
  ["毛绒/手办供应链", "1126.HK", 54, "直接承接 plush/figure 需求", "客户集中、毛利率下行、议价权弱"],
  ["内容化与影视授权", "9992.HK, SONY, DIS, 7832.T", 62, "角色从玩具走向内容可延长生命周期", "项目不确定、财务贡献滞后、内容成功率低"]
];

const targets = [
  {
    rank: 1,
    ticker: "9992.HK",
    name: "泡泡玛特",
    class: "核心原创 IP 平台",
    node: "原创 IP 运营 + 全球渠道 + 产品供应",
    chokepoint_score: 86,
    win_probability: "中高",
    payoff_odds: "中高但波动大",
    strength: "A-/B+",
    score: "IP 19/20, 需求 18/18, 渠道 12/14, 财务 15/16, 估值 9/12",
    odds_model:
      "隐含预期：市场相信 Labubu 后仍有 IP 接力。Base：收入高增放缓但利润率维持；Bull：海外复购和新 IP 接力；Bear：THE MONSTERS 热度回落且海外环比走弱。",
    rationale:
      "最直接的受益标的，拥有原创角色、稀缺发售、DTC 渠道和高毛利财务转化。2025 年增长和利润质量极强，但单一 IP 贡献和海外持续性是核心折扣。",
    downgrade:
      "THE MONSTERS 占比继续上升但新 IP 不接力；海外季度环比/同店转弱；毛利或经营利润率被促销、渠道、盗版治理拖累。",
    next_data:
      "2026 半年报分 IP/区域/渠道收入、海外同店、会员复购、库存、毛利率、经营利润率。",
    source_ids: ["ev_pop_2025_annual_results", "ev_pop_2025_ip_region_mix", "ev_pop_q1_2026_update", "ev_valuation_snapshot_pop_related"]
  },
  {
    rank: 2,
    ticker: "8136.T",
    name: "Sanrio",
    class: "多角色授权 IP 对照",
    node: "角色授权 + 全球化",
    chokepoint_score: 82,
    win_probability: "中高",
    payoff_odds: "未统一估值，暂中性",
    strength: "B+",
    score: "IP 20/20, 需求 15/18, 渠道 11/14, 财务 14/16, 估值 6/12",
    odds_model:
      "隐含预期：多角色授权增长可持续。Base：授权和海外增长维持；Bull：角色组合继续扩张；Bear：估值过高或授权热度降温。",
    rationale:
      "Sanrio 是最好的“泡泡玛特未来形态”参照：多角色、授权、全球化、轻资产利润。但它不是 Labubu 链条直接受益，需要按独立 IP 公司估值。",
    downgrade:
      "角色热度下降、授权收入增速放缓、官方年报不支持第三方快照增长。",
    next_data:
      "FY2026 官方年报、区域授权收入、商品化授权利润率、估值分位。",
    source_ids: ["ev_sanrio_financial_snapshot", "ev_valuation_snapshot_pop_related"]
  },
  {
    rank: 3,
    ticker: "MNSO / 9896.HK",
    name: "名创优品 / TOP TOY",
    class: "渠道型潮玩零售",
    node: "全球零售渠道 + 潮玩品类",
    chokepoint_score: 73,
    win_probability: "中",
    payoff_odds: "中",
    strength: "B+",
    score: "IP 9/20, 需求 15/18, 渠道 14/14, 财务 12/16, 估值 8/12",
    odds_model:
      "隐含预期：TOP TOY 高增能与名创全球渠道协同。Base：TOP TOY 继续高增但占比仍小；Bull：自有/授权 IP 出圈；Bear：只成为渠道流量而非 IP 资产。",
    rationale:
      "TOP TOY 证明相邻潮玩需求存在，名创渠道强，但 IP 控制力弱于泡泡玛特。适合作为相关消费/渠道标的，而不是原创 IP 替代。",
    downgrade:
      "TOP TOY 增速放缓、毛利率下行、海外门店扩张带不来同店增长。",
    next_data:
      "TOP TOY 单独门店数、同店、毛利率、自有 IP 占比、海外扩张。",
    source_ids: ["ev_miniso_2025_annual", "ev_miniso_q1_2026"]
  },
  {
    rank: 4,
    ticker: "0325.HK",
    name: "布鲁可",
    class: "授权 IP 拼搭玩具",
    node: "授权 IP + 标准化产品系统",
    chokepoint_score: 69,
    win_probability: "中",
    payoff_odds: "中性偏观察",
    strength: "B",
    score: "IP 11/20, 需求 13/18, 渠道 9/14, 财务 12/16, 估值 8/12",
    odds_model:
      "隐含预期：授权角色积木化增长可持续。Base：收入保持中高增；Bull：Bloks System 形成平台；Bear：授权费用和同质化压缩利润。",
    rationale:
      "和泡泡玛特同属角色玩具消费，但路径是授权 IP + 标准化积木系统。财务已转正，适合观察中国潮玩/积木化需求扩散。",
    downgrade:
      "授权 IP 成本上升、核心 IP 到期、增长低于估值要求。",
    next_data:
      "IP 授权结构、复购、渠道库存、毛利率、现金流和估值口径。",
    source_ids: ["ev_bloks_2025_annual", "ev_valuation_snapshot_pop_related"]
  },
  {
    rank: 5,
    ticker: "7832.T",
    name: "Bandai Namco",
    class: "成熟 IP 协同平台",
    node: "IP synergy + 玩具/模型/娱乐",
    chokepoint_score: 74,
    win_probability: "中高",
    payoff_odds: "未统一估值",
    strength: "B",
    score: "IP 18/20, 需求 13/18, 渠道 10/14, 财务 13/16, 估值 5/12",
    odds_model:
      "隐含预期：成熟 IP 组合稳健增长。Base：模型/卡牌/玩具维持；Bull：新内容周期；Bear：老 IP 增长放缓。",
    rationale:
      "更像成熟参照和分散型 IP 标的，不是泡泡玛特主题的直接弹性标的。",
    downgrade:
      "核心 IP 周期走弱、玩具/爱好业务利润率下滑。",
    next_data:
      "FY2026 分部收入利润、Gundam/卡牌/模型增长、估值分位。",
    source_ids: ["ev_bandai_ip_synergy"]
  },
  {
    rank: 6,
    ticker: "1126.HK",
    name: "Dream International",
    class: "OEM/供应链线索",
    node: "毛绒/手办制造",
    chokepoint_score: 54,
    win_probability: "中",
    payoff_odds: "低到中",
    strength: "B-/Lead",
    score: "IP 3/20, 需求 11/18, 渠道 3/14, 财务 8/16, 估值 8/12",
    odds_model:
      "隐含预期：毛绒/手办需求带动订单。Base：收入增长但毛利承压；Bull：大客户订单放量；Bear：客户集中和价格压力继续侵蚀利润。",
    rationale:
      "能承接行业订单，但议价权弱。2025 年 plush 增长但毛利率下降，说明供应链不是主要价值捕获者。",
    downgrade:
      "毛利率继续下行、大客户集中度升高、应收/库存恶化。",
    next_data:
      "客户结构、订单能见度、越南/印尼产能、毛利率和现金流。",
    source_ids: ["ev_dream_2025_annual"]
  },
  {
    rank: 7,
    ticker: "FNKO",
    name: "Funko",
    class: "反面样本/低优先线索",
    node: "授权收藏玩具",
    chokepoint_score: 45,
    win_probability: "低到中",
    payoff_odds: "高波动",
    strength: "C/Lead",
    score: "IP 6/20, 需求 5/18, 渠道 8/14, 财务 4/16, 估值 7/12",
    odds_model:
      "隐含预期：库存和需求修复。Base：2026 低个位数增长；Bull：周转改善；Bear：收藏热度继续退潮。",
    rationale:
      "Funko 更重要的价值是提醒：授权收藏玩具可以很快从热潮变成库存和亏损问题。",
    downgrade:
      "收入继续下降、毛利率不修复、库存和现金流恶化。",
    next_data:
      "2026 net sales、gross margin、inventory、EBITDA。",
    source_ids: ["ev_funko_2025_results", "ev_valuation_snapshot_pop_related"]
  }
];

function ids(...args) {
  return args.flat();
}

function dispatch(taskFamily, skill, materials, schema, status = "used as protocol", fallback = "none") {
  return {
    task_family: taskFamily,
    selected_skill: skill,
    concrete_materials: materials,
    extraction_schema: schema,
    source_plan:
      "primary company filings/results first; third-party market data and news are lead/boundary checks; every support source has a refuting source plan",
    skill_output_status: status,
    fallback_used: fallback,
    gpt_verification_status:
      "GPT verified key facts against source links where available; low-reliability current/news items were marked lead or message"
  };
}

const nodes = [
  {
    id: "goal",
    layer: "L0",
    title: "当前研究目标",
    question: "泡泡玛特相关公司在 2026-2028 年有哪些值得跟踪的投资机会？",
    conclusion:
      "当前判断：泡泡玛特相关机会不是“盲盒玩具”单点，而是中国原创角色 IP 全球化、情绪消费、渠道稀缺发售、授权/内容化和供应链承接的组合。最强主线仍是拥有原创 IP 与全球 DTC 渠道的泡泡玛特；第二层是 Sanrio、名创/TOP TOY、布鲁可等相邻 IP/渠道标的；供应链标的更多是订单线索而非价值捕获核心。最大不确定性是 Labubu/THE MONSTERS 热度是否能转化为多 IP 组合与海外复购，而不是一次性潮流周期。",
    evidence_ids: ids("ev_pop_2025_annual_results", "ev_pop_2025_ip_region_mix", "ev_miniso_2025_annual", "ev_bloks_2025_annual", "ev_sanrio_financial_snapshot"),
    children: ["q1", "q2", "q3", "q4"],
    gaps: ["需要统一 2026 年中报、海外同店/复购、估值分位和 forward estimates。"]
  },
  {
    id: "q1",
    layer: "L1",
    title: "Q1 需求真实度：泡泡玛特热度是否代表一个可持续的 IP 消费赛道？",
    conclusion:
      "需求是真的，但不能直接线性外推。泡泡玛特 2025 年收入和利润爆发，海外区域尤其美洲/欧洲增长极强；名创 TOP TOY、布鲁可、Sanrio、Bandai 等也证明角色 IP 和潮玩/爱好消费有扩散性。反面样本是 Funko 和 Mattel 内部分化，说明收藏玩具热潮若没有持续 IP 管理和渠道纪律，会快速转为库存、折扣和利润压力。",
    evidence_ids: ids("ev_pop_2025_annual_results", "ev_pop_2025_ip_region_mix", "ev_miniso_2025_annual", "ev_bloks_2025_annual", "ev_funko_2025_results", "ev_mattel_2025_results"),
    children: ["q1-1", "q1-2"],
    gaps: ["需要 2026H1 的会员复购、海外同店、库存和二级市场溢价数据。"]
  },
  {
    id: "q1-1",
    layer: "L2",
    title: "Q1.1 泡泡玛特自身需求是否仍在兑现？",
    conclusion:
      "泡泡玛特 2025 年收入、毛利、经营利润和调整净利同时高增，是最强一手证据；但 THE MONSTERS 单一 IP 收入占 38.1%，说明增长质量必须看新 IP 接力和海外复购。",
    evidence_ids: ids("ev_pop_2025_annual_results", "ev_pop_2025_ip_region_mix", "ev_pop_2025_product_mix", "ev_pop_q1_2026_update"),
    children: ["q1-1-1-pop-demand"],
    gaps: ["需要把海外收入拆成新店、同店、线上、复购和一次性抢购。"]
  },
  {
    id: "q1-1-1-pop-demand",
    layer: "L3",
    title: "Q1.1.1 泡泡玛特 2025-2026 的数字证明了什么？",
    materiality: "决定 9992.HK 是核心标的还是短期热度交易。",
    source_plan: "优先年报/业绩公告；Q1 业务更新和媒体报道只作为 lead；反证看海外环比、IP 集中和毛利率。",
    dispatch: dispatch(
      "financial statement / news parsing",
      "financial-statement-analysis + news-event-analysis",
      ["Pop Mart 2025 annual results", "Q1 2026 business update coverage"],
      "extract revenue, gross profit, operating profit, adjusted profit, IP mix, region mix, product mix, support/refute stance"
    ),
    fact:
      "2025 年收入 RMB37.120B，同比+184.7%；归母利润 RMB12.776B，同比+308.8%；THE MONSTERS 收入 RMB14.161B，占 38.1%；plush toys 收入 RMB18.708B，占 50.4%，同比+560.6%。2026Q1 媒体引用业务更新称整体收入同比+75%-80%。",
    inference:
      "泡泡玛特的需求已经从盲盒扩展到毛绒、挂件、社交展示和海外零售，收入不是小基数概念炒作。",
    judgment:
      "需求真实度强，但判断必须折扣单一 IP 集中和海外持续性。若新 IP 和海外复购接不上，2025 的高利润可能被市场当作峰值。",
    gap: "缺少 2026H1 分 IP、同店、会员复购和渠道库存。",
    trigger:
      "THE MONSTERS 占比下降但总收入仍高增是正触发；海外收入环比/同店连续走弱或毛利率下滑是负触发。",
    evidence_ids: ids("ev_pop_2025_annual_results", "ev_pop_2025_ip_region_mix", "ev_pop_2025_product_mix", "ev_pop_q1_2026_update")
  },
  {
    id: "q1-2",
    layer: "L2",
    title: "Q1.2 相邻公司是否证明赛道不是泡泡玛特单点？",
    conclusion:
      "相邻证据支持赛道存在：TOP TOY 高增、布鲁可扭亏、Sanrio 多角色授权高成长、Bandai 成熟 IP 协同。但 Funko 下滑和 Mattel 品类分化说明这个赛道不是普涨，胜负关键是 IP 管理、渠道纪律和库存控制。",
    evidence_ids: ids("ev_miniso_2025_annual", "ev_bloks_2025_annual", "ev_sanrio_financial_snapshot", "ev_bandai_ip_synergy", "ev_funko_2025_results", "ev_mattel_2025_results"),
    children: ["q1-2-1-adjacent-demand"],
    gaps: ["需要统一各公司的同店、库存、授权费率和估值口径。"]
  },
  {
    id: "q1-2-1-adjacent-demand",
    layer: "L3",
    title: "Q1.2.1 名创、布鲁可、Sanrio、Bandai、Funko/Mattel 给出什么边界？",
    materiality: "决定研究范围是只看泡泡玛特，还是扩展到 IP/潮玩相关公司。",
    source_plan: "公司年报/业绩为支持；Funko/Mattel 作为反证样本；第三方快照只作 lead。",
    dispatch: dispatch(
      "financial statement / industry comparison",
      "financial-statement-analysis + industry-report-analysis",
      ["MINISO 2025 annual report", "Bloks 2025 annual report", "Sanrio data", "Bandai IR", "Funko/Mattel results"],
      "extract comparable growth, margin, IP model, refuting cases"
    ),
    fact:
      "TOP TOY 2025 年收入 RMB1.916B，同比+94.8%；布鲁可 2025 年收入 RMB2.913B，同比+30.0%且扭亏；Sanrio TTM/FY 数据高增；Funko 2025 年销售下降并亏损，Mattel Dolls 下滑、Vehicles 增长。",
    inference:
      "角色 IP/潮玩/爱好消费是真赛道，但公司间的 value capture 差异很大：原创角色和授权生态优于单纯 OEM，成熟 IP 组合优于单一热款。",
    judgment:
      "相关公司应分层，而不是一篮子买主题：原创 IP 平台优先，其次多 IP 授权和渠道平台，供应链/授权收藏玩具只是线索。",
    gap: "缺少可比口径下的会员复购、IP 集中度、库存周转和广告/渠道费用。",
    trigger:
      "若相邻公司在收入增长同时毛利/现金流转弱，应说明主题扩散没有形成利润捕获。",
    evidence_ids: ids("ev_miniso_2025_annual", "ev_bloks_2025_annual", "ev_sanrio_financial_snapshot", "ev_bandai_ip_synergy", "ev_funko_2025_results", "ev_mattel_2025_results")
  },
  {
    id: "q2",
    layer: "L1",
    title: "Q2 价值捕获瓶颈：谁能把 IP 热度转成利润？",
    conclusion:
      "价值捕获主要来自五个节点：原创 IP 运营、全球 DTC/零售渠道、授权 IP/标准化产品系统、毛绒/手办供应链、内容化与授权。评分最高的是原创 IP 运营，因为它同时控制角色心智、稀缺发售、产品定价和粉丝复购；供应链虽然受益订单，但毛利率和客户集中度显示议价权弱。",
    evidence_ids: ids("ev_pop_2025_ip_region_mix", "ev_pop_2025_product_mix", "ev_dream_2025_annual", "ev_miniso_2025_annual", "ev_bloks_2025_annual", "ev_pop_sony_labubu_film"),
    children: ["q2-1", "q2-2"],
    gaps: ["需要按公司披露 IP/渠道/供应链利润池，而非只看收入。"],
    artifact: { type: "chokepoint_scorecard", rows: chokepoints }
  },
  {
    id: "q2-1",
    layer: "L2",
    title: "Q2.1 原创 IP、渠道和供应链分别有什么瓶颈属性？",
    conclusion:
      "原创 IP 与 DTC 渠道是高分节点；供应链是低分节点。泡泡玛特高毛利和 THE MONSTERS 外溢证明它不是普通玩具零售，Dream International 毛利率下行说明 OEM 很难保留主要利润池。",
    evidence_ids: ids("ev_pop_2025_annual_results", "ev_pop_2025_product_mix", "ev_dream_2025_annual", "ev_miniso_2025_annual"),
    children: ["q2-1-1-ip-engine", "q2-1-2-product-supply", "q2-1-3-retail-channel", "q2-1-4-licensed-ip"],
    gaps: ["需要泡泡玛特不同 IP 的生命周期曲线、渠道毛利和库存数据。"]
  },
  {
    id: "q2-1-1-ip-engine",
    layer: "L3",
    title: "Q2.1.1 原创 IP 运营为什么是最高价值节点？",
    materiality: "决定泡泡玛特是否显著优于渠道商和供应链商。",
    source_plan: "使用泡泡玛特 IP/区域/产品收入和 Sanrio 参照；反证看 Funko 热度退潮。",
    dispatch: dispatch("industry report / financial parsing", "industry-report-analysis + financial-statement-analysis", ["Pop Mart annual results", "Sanrio snapshot", "Funko results"], "extract IP revenue concentration, repeatability, margin and refuting fad cases"),
    fact:
      "THE MONSTERS 单一 IP 2025 年收入 RMB14.161B，占 38.1%；泡泡玛特毛利率约 72.1%；Sanrio 多角色授权高利润增长；Funko 则在授权收藏玩具退潮时销售下降并亏损。",
    inference:
      "原创 IP 的价值在于控制角色、审美、社区、稀缺发售和产品延展，不是单纯卖玩具。",
    judgment:
      "原创 IP 是最高价值节点，但单一 IP 占比越高，生命周期风险越大。强结论需要看到新 IP 接力和海外复购。",
    gap: "各 IP 的复购、会员重合度、二级市场溢价和生命周期长度缺失。",
    trigger: "新 IP 收入占比上升且毛利稳定则强化；THE MONSTERS 退潮拖累总收入则降级。",
    evidence_ids: ids("ev_pop_2025_ip_region_mix", "ev_sanrio_financial_snapshot", "ev_funko_2025_results")
  },
  {
    id: "q2-1-2-product-supply",
    layer: "L3",
    title: "Q2.1.2 毛绒和手办供应链能否捕获主要利润？",
    materiality: "决定是否把 Dream International 等供应商列入高优先级。",
    source_plan: "比较 Pop Mart 产品 mix 与 Dream 毛绒/手办收入、毛利率和客户集中。",
    dispatch: dispatch("financial statement parsing", "financial-statement-analysis", ["Pop Mart product mix", "Dream International annual report"], "extract product demand, supplier revenue, gross margin, customer concentration"),
    fact:
      "泡泡玛特 plush toys 2025 年收入 RMB18.708B，同比+560.6%；Dream plush stuffed toys 收入 HK$3.264B，同比+18.0%，但公司毛利率从 23.0% 降至 20.2%，四个客户各占收入超过 10%。",
    inference:
      "供应链能受益订单，但毛利和客户集中显示议价权弱，容易被品牌方和大客户压价。",
    judgment:
      "供应链是跟踪线索，不是最高价值捕获节点。除非出现产能稀缺、独家工艺或客户结构改善，否则观察强度低于 IP 平台。",
    gap: "缺少 Dream 与泡泡玛特直接客户关系、订单占比和分客户利润率。",
    trigger: "若毛利率回升且客户集中下降，供应链强度上调；反之只保留 lead。",
    evidence_ids: ids("ev_pop_2025_product_mix", "ev_dream_2025_annual")
  },
  {
    id: "q2-1-3-retail-channel",
    layer: "L3",
    title: "Q2.1.3 全球零售渠道是否构成瓶颈？",
    materiality: "决定名创优品/TOP TOY 是否是相关公司中的重要标的。",
    source_plan: "用 MINISO/TOP TOY 增长、泡泡玛特海外增长和 Q1 海外边界共同判断。",
    dispatch: dispatch("financial statement / news parsing", "financial-statement-analysis + news-event-analysis", ["MINISO annual/quarter results", "Pop Mart region mix and Q1 update"], "extract store/channel growth, overseas momentum, support/refute boundary"),
    fact:
      "TOP TOY 2025 年收入同比+94.8%；泡泡玛特美洲/欧洲 2025 年高增；但 2026Q1 媒体指出海外业务虽同比快增、环比转弱。",
    inference:
      "渠道触达是 IP 全球化的必要条件，但渠道本身不能替代原创 IP。名创强在门店网络，弱在 IP 控制。",
    judgment:
      "渠道是中高分节点。MINISO/TOP TOY 值得观察，但强度应低于泡泡玛特和 Sanrio 这类 IP 控制方。",
    gap: "缺少 TOP TOY 单独同店、海外占比和自有 IP 收入。",
    trigger: "TOP TOY 继续高增且自有 IP 占比提升则上调；若只靠渠道流量则维持中性。",
    evidence_ids: ids("ev_miniso_2025_annual", "ev_miniso_q1_2026", "ev_pop_q1_2026_update")
  },
  {
    id: "q2-1-4-licensed-ip",
    layer: "L3",
    title: "Q2.1.4 授权 IP 和标准化玩具系统是否能替代原创 IP？",
    materiality: "决定布鲁可/Bandai 等是否成为第二层机会。",
    source_plan: "用 Bloks 业绩、专利系统和 Bandai IP synergy 对照，反证授权成本和差异化不足。",
    dispatch: dispatch("financial statement / industry parsing", "financial-statement-analysis + industry-report-analysis", ["Bloks annual report", "Bandai IR"], "extract growth, profit, patent/system, licensed IP dependency"),
    fact:
      "布鲁可 2025 年收入 RMB2.913B，同比+30.0%，adjusted profit RMB674.9M；拥有近 550 个专利组合和 Bloks System；Bandai Namco 是成熟 IP 协同平台。",
    inference:
      "授权 IP + 产品系统能降低单一原创 IP 失败风险，但授权方和渠道方分走利润，价值捕获通常低于原创 IP 所有人。",
    judgment:
      "布鲁可是第二层验证型机会；Bandai 是成熟对照和分散标的，不是泡泡玛特主题的直接高弹性标的。",
    gap: "缺少授权费率、核心 IP 到期和自有 IP 占比。",
    trigger: "自有系统/IP 占比提升是上调信号；授权成本上行或核心 IP 到期是降级信号。",
    evidence_ids: ids("ev_bloks_2025_annual", "ev_bandai_ip_synergy")
  },
  {
    id: "q2-2",
    layer: "L2",
    title: "Q2.2 内容化和授权能否打开第二增长曲线？",
    conclusion:
      "内容化是可选增量，不是当前估值的主证据。Sony/Labubu 电影线索说明泡泡玛特想从玩具 IP 走向内容 IP，但影视项目成功率和财务贡献都需要等实际立项、上映、授权和衍生品反馈。",
    evidence_ids: ids("ev_pop_sony_labubu_film", "ev_sanrio_financial_snapshot", "ev_bandai_ip_synergy"),
    children: ["q2-2-1-content-licensing"],
    gaps: ["缺少合同条款、授权费、项目时间表和 IP 影视化 KPI。"]
  },
  {
    id: "q2-2-1-content-licensing",
    layer: "L3",
    title: "Q2.2.1 Labubu 影视化/授权化能否改变估值框架？",
    materiality: "决定是否把泡泡玛特从玩具公司重估为内容 IP 公司。",
    source_plan: "Sony 电影新闻作为 lead；Sanrio/Bandai 作为成熟 IP 内容化参照；不得直接转成估值上调。",
    dispatch: dispatch("news / opinion boundary parsing", "news-event-analysis + industry-report-analysis", ["Sony Labubu film news", "Sanrio snapshot", "Bandai IR"], "classify lead, identify confirmation data, avoid unsupported valuation uplift"),
    fact:
      "媒体报道称 Sony 开发 Labubu 电影。Sanrio 和 Bandai 证明成熟角色 IP 可跨授权、内容、商品和娱乐，但它们用了长期 IP 组合和内容生态。",
    inference:
      "如果内容化成功，泡泡玛特可降低单品玩具周期风险；但影视化从新闻到利润兑现存在长链条。",
    judgment:
      "目前只能作为看涨期权，不能作为核心投资证据。核心仍是角色商品化和复购数据。",
    gap: "没有官方项目公告、上映计划、投资金额、授权收入和衍生品预期。",
    trigger: "官方确认项目、内容上线、授权商品收入披露是上调；项目搁置或口碑失败则不计入估值。",
    evidence_ids: ids("ev_pop_sony_labubu_film", "ev_sanrio_financial_snapshot", "ev_bandai_ip_synergy")
  },
  {
    id: "q3",
    layer: "L1",
    title: "Q3 反证与赔率：哪些风险会证伪泡泡玛特相关机会？",
    conclusion:
      "最关键的风险不是“热度下降”四个字，而是可量化为四类反证：单一 IP 集中、海外复购不足、盗版/仿品和贸易摩擦、估值对峰值利润的折价或错误定价。Funko 是反面样本；Dream 毛利下行说明供应链不能自动分享高景气。",
    evidence_ids: ids("ev_funko_2025_results", "ev_mattel_2025_results", "ev_pop_q1_2026_update", "ev_pop_counterfeit_ip_enforcement", "ev_valuation_snapshot_pop_related"),
    children: ["q3-1", "q3-2"],
    gaps: ["需要同一估值日、forward estimates、库存和复购数据。"]
  },
  {
    id: "q3-1",
    layer: "L2",
    title: "Q3.1 基本面反证：热度、海外、盗版和库存如何降级？",
    conclusion:
      "如果 THE MONSTERS 不能让位于多 IP 组合，或海外增长从抢购转为环比下滑，泡泡玛特会从 IP 平台叙事退回单品爆款叙事。相关公司也要看库存和毛利，Funko 证明收藏热潮退去后利润修复很难。",
    evidence_ids: ids("ev_pop_2025_ip_region_mix", "ev_pop_q1_2026_update", "ev_funko_2025_results", "ev_pop_counterfeit_ip_enforcement"),
    children: ["q3-1-1-labubu-risk", "q3-1-2-overseas-risk"],
    gaps: ["缺少官方库存、折扣率、二级市场价格和仿品渗透率。"]
  },
  {
    id: "q3-1-1-labubu-risk",
    layer: "L3",
    title: "Q3.1.1 Labubu/THE MONSTERS 集中度是否会变成反证？",
    materiality: "决定 9992.HK 的估值能否看多 IP 平台，而不是单品周期。",
    source_plan: "使用 Pop Mart IP mix、Funko/Mattel 反证和下一季新 IP 数据。",
    dispatch: dispatch("financial statement / refuting case analysis", "financial-statement-analysis + industry-report-analysis", ["Pop Mart IP mix", "Funko/Mattel results"], "extract concentration, comparable fad risk, downgrade triggers"),
    fact:
      "THE MONSTERS 2025 年收入占泡泡玛特总收入 38.1%；Funko 2025 年销售下降并亏损；Mattel Dolls 下滑而 Vehicles 增长。",
    inference:
      "单一角色爆发既证明 IP 运营能力，也提高未来比较基数和生命周期风险。",
    judgment:
      "如果新 IP 接力成功，Labubu 是平台验证；如果接力失败，它就是周期峰值风险。",
    gap: "缺少各 IP 2026Q1/Q2 的收入占比、复购和用户重合。",
    trigger: "THE MONSTERS 占比降而总收入不降是平台化正证据；占比升且总增速放缓是负证据。",
    evidence_ids: ids("ev_pop_2025_ip_region_mix", "ev_funko_2025_results", "ev_mattel_2025_results")
  },
  {
    id: "q3-1-2-overseas-risk",
    layer: "L3",
    title: "Q3.1.2 海外增长、盗版和贸易摩擦如何影响机会？",
    materiality: "决定海外增长能否支撑长期空间和高估值。",
    source_plan: "Q1 海外更新为 lead；IP enforcement 新闻为 lead；公司公告优先，媒体只做风险线索。",
    dispatch: dispatch("news-event analysis", "news-event-analysis", ["Q1 business update coverage", "IP enforcement lawsuit coverage"], "classify overseas growth, counterfeit risk, trade/risk trigger"),
    fact:
      "媒体称 2026Q1 海外区域同比仍增长，但环比下降暴露海外用户积累不足；另有美国 IP enforcement 诉讼报道。",
    inference:
      "海外增长既是空间来源，也是最大波动源。盗版/仿品越多，说明 IP 热度强，但也会稀释品牌、渠道和价格。",
    judgment:
      "海外需要用同店、会员、复购和库存验证，不能只看区域同比。",
    gap: "缺少海外门店同店、复购、库存、仿品治理成本和关税影响。",
    trigger: "海外连续环比/同店走弱、诉讼/仿品扩散或促销加剧则降级。",
    evidence_ids: ids("ev_pop_q1_2026_update", "ev_pop_counterfeit_ip_enforcement")
  },
  {
    id: "q3-2",
    layer: "L2",
    title: "Q3.2 估值赔率：市场是在定价峰值利润还是长期 IP 平台？",
    conclusion:
      "泡泡玛特表观 PE/forward PE 不高，但这可能不是便宜的充分条件：如果 2025 利润被视为峰值，低 PE 是周期折价；如果多 IP 和海外复购被证明，则低 PE 反而给出赔率。其他标的如 Sanrio、Bloks、MINISO 需要统一估值口径后比较。",
    evidence_ids: ids("ev_valuation_snapshot_pop_related", "ev_pop_2025_annual_results", "ev_funko_2025_results"),
    children: ["q3-2-1-valuation"],
    gaps: ["需要统一 date、market cap、net cash、forward EPS/FCF 和历史分位。"]
  },
  {
    id: "q3-2-1-valuation",
    layer: "L3",
    title: "Q3.2.1 当前估值快照如何影响观察强度？",
    materiality: "决定基本面强度如何转换为赔率强度。",
    source_plan: "第三方估值只作为 lead；需后续用 valuation-analysis 做统一口径 reverse DCF。",
    dispatch: dispatch("valuation / priced-in expectations", "valuation-analysis", ["StockAnalysis valuation snapshots", "company financial facts"], "extract PE/P/S, identify implied expectation, mark unverified fields"),
    fact:
      "第三方快照显示 9992.HK PE 约 15.15、forward PE 约 13.22、P/S 约 5.16；0325.HK P/S 约 4.34。数据口径、日期和 forward estimates 需要统一。",
    inference:
      "泡泡玛特如果能保持 2025 利润质量和多 IP 接力，表观赔率不差；若 2025 是峰值，则低 PE 不是安全边际。",
    judgment:
      "估值目前只能把 9992.HK 从“纯高景气贵股”降为“需验证利润耐久的赔率机会”；不能直接输出买卖结论。",
    gap: "缺 forward estimates、FCF、净现金和历史估值分位。",
    trigger: "若 2026H1 EPS/FCF 继续上修且估值未扩张，则赔率上调；若盈利下修，低 PE 失效。",
    evidence_ids: ids("ev_valuation_snapshot_pop_related", "ev_pop_2025_annual_results")
  },
  {
    id: "q4",
    layer: "L1",
    title: "Q4 标的观察：哪些证券应进入跟踪清单？",
    conclusion:
      "观察排序应遵循“IP 控制 > 渠道/授权系统 > 供应链/OEM > 反面样本”。核心是 9992.HK；第二层是 Sanrio、MINISO/TOP TOY、Bloks、Bandai；Dream 是供应链线索；Funko 是低优先/反面样本。",
    evidence_ids: targets.flatMap((t) => t.source_ids),
    children: ["q4-1"],
    gaps: ["需要为每个标的补统一估值和未来两季验证计划。"]
  },
  {
    id: "q4-1",
    layer: "L2",
    title: "Q4.1 研究优先级和降级规则如何排序？",
    conclusion:
      "最终推荐是研究观察清单，不是买卖指令。排名同时考虑 chokepoint 分、未来空间、估值赔率、证据质量和反证可监控性。",
    evidence_ids: targets.flatMap((t) => t.source_ids),
    children: ["q4-1-1-target-ranking"],
    gaps: ["后续每季应按同一评分表回写。"],
    artifact: { type: "target_table", rows: targets }
  },
  {
    id: "q4-1-1-target-ranking",
    layer: "L3",
    title: "Q4.1.1 每个标的的强度、赔率和降级触发器是什么？",
    materiality: "把前面 QA 的结论落到可跟踪证券。",
    source_plan: "使用公司公告和估值 lead；Q4 只输出观察强度和验证数据，不输出交易指令。",
    dispatch: dispatch("target observation / recommendation", "target-recommendation-analysis + valuation-analysis", ["all verified evidence and valuation leads"], "rank target observation by chokepoint score, future space, valuation odds, evidence quality, risk triggers"),
    fact:
      "9992.HK 是唯一直接同时覆盖原创 IP、渠道和产品供应的标的；Sanrio/Bandai 是成熟 IP 参照；MINISO/Bloks 是相邻消费和授权系统；Dream 是供应链；Funko 是反面样本。",
    inference:
      "相关公司不是同质篮子，应按价值捕获位置和可验证财务指标排序。",
    judgment:
      "核心观察 9992.HK；高优先对照 Sanrio、MINISO/TOP TOY、Bloks；Bandai 为成熟 IP 参照；Dream/Funko 仅作为线索或反证。",
    gap: "统一估值口径和下一季 KPI。",
    trigger: "每个标的按 target table 的 next_data 和 downgrade 字段回写。",
    evidence_ids: targets.flatMap((t) => t.source_ids)
  }
];

const extractionIdsByNode = {};
const reviewIdsByNode = {};
for (const extraction of sourceExtractions) {
  extractionIdsByNode[extraction.l3_question_id] = extractionIdsByNode[extraction.l3_question_id] || [];
  extractionIdsByNode[extraction.l3_question_id].push(extraction.extraction_id);
}
for (const review of leafSourceReviews) {
  reviewIdsByNode[review.l3_question_id] = reviewIdsByNode[review.l3_question_id] || [];
  reviewIdsByNode[review.l3_question_id].push(review.review_id);
}
for (const node of nodes) {
  if (node.layer === "L3") {
    node.source_extraction_ids = extractionIdsByNode[node.id] || [];
    node.leaf_source_review_ids = reviewIdsByNode[node.id] || [];
  }
}

function bucketCounts(ids) {
  const counts = { evidence: 0, research_report: 0, message: 0, opinion: 0 };
  for (const id of ids || []) {
    const item = evidenceMap[id];
    if (item) counts[item.information_category] += 1;
  }
  return `证/研/消/观 ${counts.evidence}/${counts.research_report}/${counts.message}/${counts.opinion}`;
}

function esc(x) {
  return String(x ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function slug(id) {
  return String(id).replace(/[^a-zA-Z0-9_-]/g, "-");
}

function sourceChips(ids) {
  const unique = [...new Set(ids || [])].filter((id) => evidenceMap[id]);
  const first = unique.slice(0, 7);
  const rest = unique.length - first.length;
  return `<div class="source-chips">${first
    .map((id) => {
      const e = evidenceMap[id];
      const label = e.information_category === "evidence" ? "证据" : e.information_category === "research_report" ? "研报/数据" : e.information_category === "message" ? "消息" : "观点";
      return `<a class="source-chip" href="#src-${slug(id)}"><span>${label}</span>${esc(e.source_name)}</a>`;
    })
    .join("")}${rest > 0 ? `<span class="more-chip">+${rest} 来源</span>` : ""}</div>`;
}

function nodeById(id) {
  return nodes.find((n) => n.id === id);
}

function logicCards(n) {
  if (n.layer === "L3") {
    return `<div class="logic-grid">
      <div class="logic-card"><span>事实</span><p>${esc(n.fact)}</p></div>
      <div class="logic-card"><span>推理</span><p>${esc(n.inference)}</p></div>
      <div class="logic-card"><span>判断</span><p>${esc(n.judgment)}</p></div>
    </div>`;
  }
  return `<div class="logic-grid"><div class="logic-card"><span>判断</span><p>${esc(n.conclusion)}</p></div></div>`;
}

function renderArtifact(n) {
  if (!n.artifact) return "";
  if (n.artifact.type === "chokepoint_scorecard") {
    return `<div class="artifact-card"><div class="artifact-head"><span>瓶颈评分公式</span><strong>100 分制</strong></div>
      <p class="muted">权重：${scoreSchema.dimensions.map((d) => `${d[1]} ${d[2]}%`).join(" / ")}</p>
      <div class="table-wrap"><table><thead><tr><th>节点</th><th>代表公司</th><th>分数</th><th>价值捕获理由</th><th>主要反证</th></tr></thead><tbody>
      ${n.artifact.rows.map((r) => `<tr><td>${esc(r[0])}</td><td>${esc(r[1])}</td><td><b>${esc(r[2])}</b></td><td>${esc(r[3])}</td><td>${esc(r[4])}</td></tr>`).join("")}
      </tbody></table></div></div>`;
  }
  if (n.artifact.type === "target_table") {
    return `<div class="artifact-card"><div class="artifact-head"><span>Q4 标的研究优先级</span><strong>${targets.length} 个标的</strong></div>${targetTable()}</div>`;
  }
  return "";
}

function renderNode(id) {
  const n = nodeById(id);
  const level = n.layer === "L1" ? "level-1" : n.layer === "L2" ? "level-2" : "level-3";
  const titleTag = n.layer === "L1" ? "h3" : n.layer === "L2" ? "h4" : "h5";
  const childHtml = (n.children || []).map(renderNode).join("");
  return `
    <details class="qa-card ${level}" id="${slug(n.id)}" ${n.layer !== "L3" ? "open" : ""}>
      <summary><${titleTag}>${esc(n.title)}</${titleTag}><span class="qa-count">${bucketCounts(n.evidence_ids)}</span><span class="chevron">›</span></summary>
      <div class="qa-body">
        <div class="qa-block conclusion"><div class="block-title">1. 当前结论呈现</div>${logicCards(n)}${renderArtifact(n)}<p>${esc(n.layer === "L3" ? `事实：${n.fact} 推理：${n.inference} 判断：${n.judgment}` : n.conclusion)}</p>${sourceChips(n.evidence_ids)}</div>
        <div class="qa-block expansion"><div class="block-title">2. 问题展开（子 QA）</div>${childHtml || `<p class="leaf-note">本节点是 L3 叶子问题，资料、事实、推论和判断已在当前结论中呈现。</p>`}</div>
        <div class="qa-block remaining"><div class="block-title">3. 待补充的问题</div><ul class="gap-list">${(n.gaps || [n.gap || "继续补充可量化数据、反证来源、估值口径和下一季验证触发器。"]).map((g) => `<li>${esc(g)}</li>`).join("")}${n.trigger ? `<li><b>触发器</b>：${esc(n.trigger)}</li>` : ""}</ul></div>
      </div>
    </details>`;
}

function targetTable() {
  return `<div class="table-wrap"><table class="target-table"><thead><tr>
    <th>排名</th><th>标的</th><th>类别 / 节点</th><th>瓶颈分</th><th>胜率</th><th>赔率</th><th>强度</th><th>评分拆解</th><th>简版赔率模型</th><th>推荐理由</th><th>降级风险</th><th>下一步验证</th>
  </tr></thead><tbody>${targets
    .map(
      (t) => `<tr><td>${t.rank}</td><td><b>${esc(t.ticker)}</b><p>${esc(t.name)}</p></td><td>${esc(t.class)}<p>${esc(t.node)}</p></td><td><b>${esc(t.chokepoint_score)}</b></td><td>${esc(t.win_probability)}</td><td>${esc(t.payoff_odds)}</td><td><strong>${esc(t.strength)}</strong></td><td>${esc(t.score)}</td><td>${esc(t.odds_model)}</td><td>${esc(t.rationale)}</td><td>${esc(t.downgrade)}</td><td>${esc(t.next_data)}</td></tr>`
    )
    .join("")}</tbody></table></div>`;
}

const project = {
  project_id: "pop_mart_related_opportunities",
  object_type: "industry_theme",
  object_id: "pop_mart_related_companies",
  meta_question: "泡泡玛特相关公司在 2026-2028 年有哪些值得跟踪的投资机会？",
  framework: "research_goal_qa",
  report_contract: "research_report_contract",
  research_type: "industry/theme opportunity",
  created_at: generatedAt,
  boundary: "研究观察清单，不构成买卖建议。"
};

const qMap = {
  Q1: "需求真实度：泡泡玛特热度是否代表可持续 IP 消费赛道",
  Q2: "价值捕获瓶颈：原创 IP、渠道、供应链、授权/内容化谁留住利润",
  Q3: "反证和赔率：Labubu 集中、海外、盗版、库存和估值如何证伪",
  Q4: "标的观察清单：具体证券的强度、赔率、验证数据和降级触发器"
};

const questionPlan = {
  generated_at: generatedAt,
  planning_mode: "research_goal_qa_with_domain_playbook",
  research_type_adaptation: {
    selected_type: "industry/theme opportunity",
    reason: "用户询问泡泡玛特相关公司投资机会，属于 IP/潮玩主题的相关标的研究，而非单家公司更新。",
    q_map: qMap
  },
  score_schema: scoreSchema,
  l1: nodes.filter((n) => n.layer === "L1").map((n) => ({ id: n.id, title: n.title, children: n.children })),
  specialty_dispatch: {
    question_architecture: "investment-question-architect protocol",
    source_planning: "research-source-planner protocol",
    financials: "financial-statement-analysis",
    valuation: "valuation-analysis",
    news: "news-event-analysis",
    industry: "industry-report-analysis",
    target: "target-recommendation-analysis",
    long_reading: "leaf-research-deepseek attempted; empty response; GPT fallback"
  }
};

const qaTree = {
  generated_at: generatedAt,
  framework: "research_goal_qa",
  report_contract: "research_report_contract",
  research_type: "industry/theme opportunity",
  q_map: qMap,
  nodes
};

const workbench = {
  generated_at: generatedAt,
  project,
  research_type_adaptation: questionPlan.research_type_adaptation,
  score_schema: scoreSchema,
  chokepoint_scorecard: chokepoints,
  target_observation_list: targets,
  source_parsing_pipeline: {
    source_extractions_path: "source_extractions.jsonl",
    leaf_source_reviews_path: "leaf_source_reviews.jsonl",
    extraction_count: sourceExtractions.length,
    review_count: leafSourceReviews.length,
    default_parser: "deepseek_delegate",
    rule: "DeepSeek/source parsers read small source-L3 bundles first; GPT verifies and writes final QA answers."
  },
  specialty_skill_trace: [
    { task_family: "question architecture", selected_skill: "investment-question-architect", status: "used as framework protocol" },
    { task_family: "source planning", selected_skill: "research-source-planner", status: "used as framework protocol" },
    { task_family: "financial parsing", selected_skill: "financial-statement-analysis", status: "used as protocol" },
    { task_family: "valuation", selected_skill: "valuation-analysis", status: "used as protocol; third-party data marked lead" },
    { task_family: "long source reading", selected_skill: "leaf-research-deepseek", status: "initial large bundle returned empty; small source-L3 extraction succeeded" },
    { task_family: "target ranking", selected_skill: "target-recommendation-analysis", status: "used as protocol" },
    { task_family: "HTML", selected_skill: "frontend-design", status: "used as protocol with canonical report contract" }
  ],
  deepseek_attempt: {
    status: "initial_empty_then_small_chunk_success",
    note: "The first large bundle prompt returned an empty response. The pipeline was upgraded to small L3/source parsing jobs and produced persisted records in source_extractions.jsonl, with GPT reviews in leaf_source_reviews.jsonl."
  }
};

function sourceIndex() {
  return `<details class="source-collapse" id="sources"><summary><span class="chevron">›</span><h3>4 / 来源索引</h3><span class="source-total">${evidence.length} 条来源</span></summary><div class="source-grid">${evidence
    .map(
      (e) => `<div class="source-card" id="src-${slug(e.id)}"><div class="source-meta"><span>${esc(e.information_category)}</span><span>${esc(e.support_refute_or_lead)}</span><span>${esc(e.reliability)}</span></div><h4><a href="${esc(e.url)}" target="_blank">${esc(e.source_name)}</a></h4><p>${esc(e.summary)}</p><code>${esc(e.id)}</code></div>`
    )
    .join("")}</div></details>`;
}

const css = `:root{--bg:#f5f7fa;--surface:#fff;--surface2:#fbfcff;--text:#354153;--heading:#243142;--muted:#758195;--line:#dde5ef;--blue:#1f6fd1;--blueSoft:#edf5ff;--accent:#5f7fa5;--green:#2f7d65;--amber:#9a6d24;--shadow:0 22px 70px rgba(45,63,86,.08);--soft:0 10px 30px rgba(45,63,86,.055)}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:linear-gradient(180deg,#fbfcfe 0,#f5f7fa 280px,#eef3f8 100%);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue","Microsoft YaHei",Arial,sans-serif;line-height:1.68;font-size:15px}a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}.page{max-width:1280px;margin:0 auto;padding:34px 24px 76px}.hero{padding:34px 0 26px;border-bottom:1px solid rgba(96,116,140,.16)}.hero:after{content:"";display:block;width:100%;height:1px;margin-top:26px;background:linear-gradient(90deg,#6f8cac 0 18%,#cad6e4 18% 42%,#edf1f6 42% 100%)}.eyebrow{margin:0 0 10px;color:#7a8492;font-size:12px;font-weight:760;letter-spacing:.08em;text-transform:uppercase}.hero h1{margin:0;font-size:46px;line-height:1.06;font-weight:780;color:var(--heading);letter-spacing:0}.subtitle{max-width:920px;margin:18px 0 0;color:#536274;font-size:18px;line-height:1.65}.top-nav{position:sticky;top:0;z-index:10;display:flex;gap:8px;flex-wrap:wrap;margin:18px -8px 30px;padding:11px 8px;background:rgba(245,247,250,.9);backdrop-filter:blur(18px);border-bottom:1px solid rgba(96,116,140,.14)}.top-nav a{padding:8px 13px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.86);color:#43536a;font-size:13px;font-weight:700}.section{margin:34px 0}.section>h2{font-size:32px;line-height:1.15;margin:0 0 18px;color:var(--heading)}.goal-card,.target-section,.source-collapse{background:linear-gradient(180deg,#fff 0,#fbfcfe 100%);border:1px solid var(--line);border-radius:24px;box-shadow:var(--shadow);padding:28px}.goal-card h2{margin:0 0 12px;font-size:28px;line-height:1.22;color:var(--heading)}.goal-card p{margin:0;color:#46576a}.goal-grid{display:grid;grid-template-columns:1.4fr repeat(3,1fr);gap:12px;margin-top:22px}.metric{background:var(--surface2);border:1px solid #e5ebf3;border-radius:16px;padding:16px}.metric span{display:block;color:#788497;font-size:12px;font-weight:760}.metric strong{display:block;margin-top:6px;font-size:24px;line-height:1.1;color:#34465d}.metric small{display:block;margin-top:6px;color:#7d8796;font-size:12px}.qa-card{position:relative;background:var(--surface);border:1px solid var(--line);border-radius:20px;margin:15px 0;box-shadow:var(--soft);overflow:hidden}.qa-card:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:#d4deea}.qa-card.level-1{border-color:#c9d6e4;box-shadow:var(--shadow)}.qa-card.level-1:before{background:var(--accent)}.qa-card.level-2{margin-left:22px}.qa-card.level-2:before{background:#2f74c8}.qa-card.level-3{margin-left:42px;border-radius:16px;box-shadow:none;background:#fbfcfe}.qa-card.level-3:before{background:#b3bfce;width:3px}.qa-card>summary{list-style:none;display:grid;grid-template-columns:auto 1fr auto auto;gap:12px;align-items:center;cursor:pointer;padding:18px 20px 18px 22px}.qa-card>summary::-webkit-details-marker{display:none}.qa-card>summary:before{content:"L";display:inline-flex;align-items:center;justify-content:center;width:34px;height:26px;border-radius:999px;background:#f0f4f8;color:#536276;font-size:12px;font-weight:800}.level-1>summary:before{content:"L1";background:#e8f0f8;color:#45698f;border:1px solid #c8d8ea}.level-2>summary:before{content:"L2";background:#edf6ff;color:#2166b9;border:1px solid #cfe4fb}.level-3>summary:before{content:"L3";background:#f3f6fa;color:#66758a;border:1px solid #dfe6ef}.qa-card h3,.qa-card h4,.qa-card h5{margin:0;color:var(--heading);line-height:1.35}.qa-card h3{font-size:22px;font-weight:760}.qa-card h4{font-size:18px;font-weight:740}.qa-card h5{font-size:16px;font-weight:720}.qa-count{color:#66758a;font-size:12px;white-space:nowrap;background:#f5f8fb;border:1px solid #e2e8f1;border-radius:999px;padding:5px 9px}.chevron{display:inline-block;font-size:24px;color:#8793a2;transition:transform .18s}.qa-card[open]>summary .chevron,.source-collapse[open]>summary .chevron{transform:rotate(90deg)}.qa-body{border-top:1px solid var(--line);padding:0 22px 22px;background:linear-gradient(180deg,rgba(248,250,253,.78),rgba(255,255,255,.98))}.qa-block{padding:18px 0;border-bottom:1px solid #edf1f6}.qa-block:last-child{border-bottom:none}.block-title{margin-bottom:11px;font-size:13px;font-weight:820;color:#48617c;background:#eef4fa;border:1px solid #dbe6f2;border-radius:999px;display:inline-flex;padding:5px 11px}.qa-block p{margin:0;color:#405066;line-height:1.72}.logic-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-bottom:12px}.logic-card{border:1px solid #e2e8f1;border-radius:14px;padding:13px;background:#fff}.logic-card span{display:block;margin-bottom:7px;font-size:12px;font-weight:820;color:#647187}.logic-card p{font-size:14px;color:#435065}.source-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}.source-chip,.more-chip{display:inline-flex;align-items:center;gap:6px;padding:7px 10px;border-radius:999px;background:#f4f8ff;border:1px solid #dce8fb;font-size:12px;font-weight:680}.source-chip span{color:#63738b}.gap-list{margin:0;padding-left:18px}.gap-list li{margin:6px 0;color:#465365}.leaf-note,.muted{color:#7b8490!important}.artifact-card{margin-top:16px;border:1px solid #dce6f0;background:#fff;border-radius:18px;padding:16px;box-shadow:0 8px 24px rgba(45,63,86,.045)}.artifact-head{display:flex;justify-content:space-between;gap:12px;margin-bottom:10px}.artifact-head span{font-weight:820;color:#3e5875}.artifact-head strong{background:#eef5ff;color:#315f91;border:1px solid #c8d8ef;border-radius:999px;padding:4px 9px;font-size:12px}.table-wrap{overflow:auto;border:1px solid #e2e8f1;border-radius:15px;background:#fff}table{width:100%;border-collapse:separate;border-spacing:0;min-width:1180px}th,td{padding:12px 13px;border-bottom:1px solid #edf1f6;text-align:left;vertical-align:top;font-size:13px;line-height:1.55;color:#405066}th{position:sticky;top:0;background:#f7f9fc;color:#596578;font-weight:780;z-index:1}tbody tr:nth-child(even) td{background:#fcfdff}td p{margin:4px 0 0!important;color:#7a8492!important;font-size:12px}td span,td small{color:#7a8492;font-size:12px}.target-section{padding:26px}.target-section>h2{font-size:34px}.target-summary{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px}.target-summary>div{border:1px solid #e2e8f1;border-radius:16px;background:#fbfcfe;padding:15px}.target-summary strong{font-size:14px;color:#38495f}.target-summary p{margin:7px 0 0;color:#526071}.target-table td:nth-child(4) b{display:block;font-size:20px;color:#315f91}.target-table td:nth-child(7) strong{display:inline-flex;align-items:center;justify-content:center;min-width:42px;padding:4px 8px;border-radius:999px;background:#eef5ff;color:#315f91;border:1px solid #c8d8ef;font-size:12px}.source-collapse{padding:0;overflow:hidden}.source-collapse>summary{list-style:none;display:flex;align-items:center;gap:12px;cursor:pointer;padding:18px 20px}.source-collapse>summary::-webkit-details-marker{display:none}.source-collapse h3{margin:0;font-size:20px;color:var(--heading)}.source-total{margin-left:auto;color:#7b8490;font-size:13px;background:#f4f7fb;border:1px solid #e2e8f1;border-radius:999px;padding:5px 9px}.source-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;border-top:1px solid var(--line);padding:18px;background:#fbfcfe}.source-card{border:1px solid #e2e8f1;border-radius:16px;padding:14px;background:#fff}.source-meta{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}.source-meta span{font-size:11px;color:#63738b;background:#eef3f9;border-radius:999px;padding:3px 7px}.source-card h4{margin:0 0 8px;font-size:15px;line-height:1.35;color:var(--heading)}.source-card p{margin:0 0 10px;color:#465365;font-size:13px;line-height:1.58}.source-card code{font-size:11px;color:#7a8492;word-break:break-all}.report-note{margin-top:18px;color:#7b8490;font-size:13px}@media(max-width:900px){.page{padding:26px 14px 54px}.hero h1{font-size:34px}.subtitle{font-size:16px}.goal-grid,.logic-grid,.source-grid,.target-summary{grid-template-columns:1fr}.qa-card.level-2,.qa-card.level-3{margin-left:0}.qa-card>summary{grid-template-columns:auto 1fr auto}.qa-count{grid-column:2/-1;justify-self:start}.section>h2,.target-section>h2{font-size:28px}}`;

const html = `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>泡泡玛特相关公司投资机会研究</title><style>${css}</style></head><body><div class="page"><header class="hero"><p class="eyebrow">Research Goal QA</p><h1>泡泡玛特相关公司投资机会研究</h1><p class="subtitle">按“需求是否真实、价值捕获节点在哪里、什么会证伪、哪些标的具备更好胜率与赔率”逐层下钻。只输出研究观察，不给买卖、仓位或目标价指令。</p></header><nav class="top-nav"><a href="#goal">当前研究目标</a><a href="#qa">问题下钻</a><a href="#targets">最终标的推荐</a><a href="#sources">来源索引</a></nav><section class="section" id="goal"><div class="goal-card"><p class="eyebrow">1 / 当前研究目标</p><h2>${esc(nodeById("goal").question)}</h2><p>${esc(nodeById("goal").conclusion)}</p><div class="goal-grid"><div class="metric"><span>研究类型</span><strong>行业/主题机会</strong><small>角色 IP / 潮玩 / 全球化消费。</small></div><div class="metric"><span>问题数量</span><strong>${nodes.length}</strong><small>L1=4 / L2=${nodes.filter((n) => n.layer === "L2").length} / L3=${nodes.filter((n) => n.layer === "L3").length}</small></div><div class="metric"><span>来源数量</span><strong>${evidence.length}</strong><small>证/研/消/观 ${bucketCounts(evidence.map((e) => e.id)).replace("证/研/消/观 ","")}</small></div><div class="metric"><span>评分体系</span><strong>100 分</strong><small>瓶颈分 + 赔率模型。</small></div></div></div></section><section class="section" id="qa"><p class="eyebrow">2 / 问题下钻</p><h2>按 QA 树展开研究结论</h2>${["q1", "q2", "q3", "q4"].map(renderNode).join("")}</section><section class="section target-section" id="targets"><p class="eyebrow">3 / 最终标的推荐</p><h2>具体证券观察清单</h2><div class="target-summary"><div><strong>当前排序逻辑</strong><p>优先原创 IP 控制和全球 DTC，其次多角色授权和渠道平台，供应链/OEM 只作为订单线索。</p></div><div><strong>边界</strong><p>这是研究观察清单，不是买卖建议；强度由瓶颈分、未来空间、估值赔率、证据质量和降级触发器共同决定。</p></div></div>${targetTable()}</section><section class="section">${sourceIndex()}</section><p class="report-note">生成时间：${generatedAt}。低可靠度消息只作为研究线索，不能单独强化投资结论。</p></div></body></html>`;

const md = `# 泡泡玛特相关公司投资机会研究

生成时间：${generatedAt}

## 当前研究目标

${nodeById("goal").conclusion}

## 问题下钻

${nodes
  .filter((n) => n.layer !== "L0")
  .map((n) => `### ${n.title}\n\n${n.layer === "L3" ? `事实：${n.fact}\n\n推理：${n.inference}\n\n判断：${n.judgment}\n\n缺口：${n.gap}\n\n触发器：${n.trigger}` : n.conclusion}\n\n证据：${(n.evidence_ids || []).map((id) => `[${id}](${evidenceMap[id]?.url || ""})`).join("，")}`)
  .join("\n\n")}

## 最终标的推荐

| 排名 | 标的 | 强度 | 瓶颈分 | 理由 | 降级风险 |
|---|---|---:|---:|---|---|
${targets.map((t) => `| ${t.rank} | ${t.ticker} ${t.name} | ${t.strength} | ${t.chokepoint_score} | ${t.rationale} | ${t.downgrade} |`).join("\n")}

## 来源索引

${evidence.map((e) => `- ${e.id}: ${e.source_name} (${e.information_category}, ${e.support_refute_or_lead}) [source](${e.url})`).join("\n")}
`;

const todo = `# 泡泡玛特相关公司投资机会研究待办

更新时间：2026-05-29

## 当前状态

- 报告主文件：\`professional_report.html\`
- Markdown 备份：\`professional_report.md\`
- QA 树：\`qa_tree.json\`
- 证据库：\`evidence.jsonl\`
- DeepSeek/source parser 初读：\`source_extractions.jsonl\`
- GPT 校验层：\`leaf_source_reviews.jsonl\`
- 工作底稿：\`investment_workbench.json\`
- 展示契约：四段式最终 HTML：当前研究目标、问题下钻、最终标的推荐、来源索引。

## 已完成

- [x] 按行业/主题机会适配 Q1-Q4。
- [x] 建立原创 IP、渠道、授权/积木系统、供应链、内容化五个价值捕获节点。
- [x] 写入 100 分 chokepoint 评分公式和降级规则。
- [x] 输出具体证券观察清单：9992.HK、8136.T、MNSO/9896.HK、0325.HK、7832.T、1126.HK、FNKO。
- [x] 低可靠度消息保留为 lead，不用于单独强化结论。
- [x] 新增 source parsing 中间层：5 条 DeepSeek 小粒度初读 + 5 条 GPT review。
- [x] 最终 HTML 不展示过程痕迹；解析痕迹保存在 JSONL 内部文件。

## 后续更新

- [ ] 补 2026H1 泡泡玛特分 IP、分区域、同店、复购、库存和毛利率。
- [ ] 统一 Pop Mart / Sanrio / MINISO / Bloks / Bandai / Dream / Funko 的估值日期、股本、净现金和 forward estimates。
- [ ] 对 9992.HK 做 reverse DCF，区分“峰值利润折价”和“多 IP 平台低估”。
- [ ] 补国内 A 股/IP 玩具和供应链候选标的筛选。
`;

for (const [file, data] of [
  ["project.json", project],
  ["question_plan.json", questionPlan],
  ["qa_tree.json", qaTree],
  ["investment_workbench.json", workbench]
]) {
  fs.writeFileSync(path.join(base, file), JSON.stringify(data, null, 2), "utf8");
}
fs.writeFileSync(path.join(base, "evidence.jsonl"), evidence.map((e) => JSON.stringify(e)).join("\n") + "\n", "utf8");
fs.writeFileSync(path.join(base, "source_extractions.jsonl"), sourceExtractions.map((e) => JSON.stringify(e)).join("\n") + "\n", "utf8");
fs.writeFileSync(path.join(base, "leaf_source_reviews.jsonl"), leafSourceReviews.map((e) => JSON.stringify(e)).join("\n") + "\n", "utf8");
fs.writeFileSync(path.join(base, "professional_report.html"), html, "utf8");
fs.writeFileSync(path.join(base, "professional_report.md"), md, "utf8");
fs.writeFileSync(path.join(base, "TODO.md"), todo, "utf8");

console.log(JSON.stringify({ generated: base, evidence: evidence.length, nodes: nodes.length, targets: targets.length, source_extractions: sourceExtractions.length, leaf_source_reviews: leafSourceReviews.length }, null, 2));
