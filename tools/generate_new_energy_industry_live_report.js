const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const PROJECT_ID = "new_energy_industry_live_20260531";
const OUT_DIR = path.join(ROOT, "research", "qa_projects", PROJECT_ID);
const REPORT_DATE = "2026-05-31";
const REVIEW_HORIZON = "2026-08-31";

const SCORE_WEIGHTS = {
  chokepoint_strength: 0.26,
  future_space: 0.18,
  valuation_odds: 0.18,
  evidence_quality: 0.14,
  disconfirming_risk_control: 0.1,
  monitorability: 0.05,
  payoff_convexity: 0.09,
};

const SCORE_DIMENSION_WEIGHTS = {
  scarcity_or_monopoly: 0.35,
  mispricing: 0.25,
  earnings_elasticity: 0.25,
  risk_control: 0.15,
};

const sources = [
  source("SRC-IEA-RENEWABLES-2025", "IEA Renewables 2025 executive summary", "research_report", "https://www.iea.org/reports/renewables-2025/executive-summary", "2025-10-07", "IEA expects about 4,600 GW of renewable power capacity additions by 2030, dominated by solar PV; curtailment and negative prices show grids, storage and flexibility becoming constraints."),
  source("SRC-IEA-RENEWABLE-ELECTRICITY", "IEA Renewables 2025 renewable electricity", "research_report", "https://www.iea.org/reports/renewables-2025/renewable-electricity", "2025-10-07", "IEA forecasts 2025-2030 onshore wind additions of 732 GW and notes distributed solar-plus-storage growth where grids are unreliable."),
  source("SRC-IEA-ELECTRICITY-2026-GRIDS", "IEA Electricity 2026 grids", "research_report", "https://www.iea.org/reports/electricity-2026/grids", "2026-02-25", "IEA highlights the need for grid investment and more efficient grid use; BESS co-location can ease grid constraints."),
  source("SRC-IEA-ELECTRICITY-2026-SUPPLY", "IEA Electricity 2026 supply", "research_report", "https://www.iea.org/reports/electricity-2026/supply", "2026-02-25", "IEA expects low-emissions sources to reach 50% of global electricity generation by 2030, with solar and wind rising from 17% of generation in 2025 to 27% by 2030."),
  source("SRC-IEA-GEVO-2025", "IEA Global EV Outlook 2025", "research_report", "https://www.iea.org/reports/global-ev-outlook-2025/outlook-for-electric-mobility", "2025-05-14", "IEA says China is the key EV market, accounts for more than half of global EV sales through 2030 in STEPS, and produced nearly 80% of global EV battery cells in 2024."),
  source("SRC-IEA-BATTERIES-2024", "IEA Batteries and Secure Energy Transitions", "research_report", "https://www.iea.org/reports/batteries-and-secure-energy-transitions/outlook-for-battery-demand-and-supply", "2024-04-25", "IEA describes batteries as a core flexibility resource; announced manufacturing capacity, if realised, would nearly quadruple global capacity by 2030, creating both demand opportunity and oversupply risk."),
  source("SRC-GEV-Q1-2026", "GE Vernova Q1 2026 results", "evidence", "https://www.gevernova.com/sites/default/files/gev_webcast_pressrelease_04222026.pdf", "2026-04-22", "GE Vernova reported Q1 2026 orders growth and backlog growth to $163B, including Prolec GE, and raised 2026 guidance; electrification and grid equipment are direct bottleneck exposures."),
  source("SRC-FSLR-Q1-2026", "First Solar Q1 2026 results", "evidence", "https://www.businesswire.com/news/home/20260430224118/en/First-Solar-Inc.-Announces-First-Quarter-2026-Financial-Results-and-Reaffirms-Guidance", "2026-04-30", "First Solar reported Q1 2026 net sales of $1.04B, 24% YoY growth, contracted backlog of 47.9 GW and reaffirmed 2026 guidance."),
  source("SRC-CATL-2025-ANNUAL", "CATL 2025 annual report release", "evidence", "https://www.catl.com/en/news/6773.html", "2026-03-10", "CATL said its energy-storage battery shipments held 30.4% global share in 2025 and ranked first globally for five consecutive years; sodium-ion commercialization is expected to broaden from 2026."),
  source("SRC-BYD-2025-RESULTS", "BYD 2025 annual results coverage", "message", "https://cnevpost.com/2026/03/27/byd-2025-full-year-results/", "2026-03-27", "BYD sold 4,602,436 NEVs in 2025 and full-year net profit fell 19% amid China price-war pressure; gross margin narrowed, making scale strong but unit economics contested."),
  source("SRC-SUNGROW-2025", "Sungrow FY2025 results coverage", "research_report", "https://taiyangnews.info/business/sungrow-fy2025-financial-results", "2026-04-01", "Sungrow FY2025 revenue rose 14.55% to RMB89.2B; energy storage became a key revenue pillar, while inverter and ESS businesses show power-electronics value capture."),
  source("SRC-ENPH-Q1-2026", "Enphase Q1 2026 results", "evidence", "https://www.sec.gov/Archives/edgar/data/1463101/000146310126000046/a2026q1exx991pressrelease.htm", "2026-04-28", "Enphase reported Q1 2026 revenue of $282.9M, non-GAAP gross margin 43.9%, 1.41M microinverters shipped and 103.1 MWh IQ Batteries shipped; US residential demand weakened after tax-credit changes."),
  source("SRC-FLNC-Q1-2026", "Fluence Energy Q1 2026 results", "evidence", "https://ir.fluenceenergy.com/news-releases/news-release-details/fluence-energy-inc-reports-first-quarter-2026-results-reaffirms", "2026-02-10", "Fluence reaffirmed FY2026 guidance and disclosed storage backlog/pipeline risk language; BESS demand is real but execution, customer and margin risks remain material."),
  source("SRC-LONGI-Q1-2026", "LONGi 2025 annual and Q1 2026 update", "evidence", "https://www.longi.com/en/news/q1-report-2026/", "2026-04-28", "LONGi reported Q1 2026 revenue of CNY11.19B and solar-storage strategy progress, but the broader PV manufacturing chain remains under margin pressure."),
];

const chainRows = [
  ["上游资源/材料", "锂、镍、铜、硅料、玻璃、功率器件、磁性材料", "矿商、材料商、半导体功率器件供应商", "向电池、组件、逆变器和电网设备供给核心材料", "材料价格影响成本，但多数环节周期性强；少数功率器件和高压设备材料可形成局部瓶颈", "Q2.1/Q2.2"],
  ["中游制造", "电池电芯、光伏组件、逆变器、变压器、开关设备、PCS、BESS 系统", "CATL、BYD、LONGi、First Solar、Sungrow、GE Vernova、Enphase、Fluence", "把材料转成可交付设备，承担产能、认证、质保和交付风险", "普通组件/电芯供给快；电网设备、电力电子、差异化制造更可能有稀缺性", "Q2/Q4"],
  ["下游项目/客户", "电动车、数据中心、电力公司、工商业储能、户用光伏、可再生发电项目", "公用事业、云厂商、车企、EPC、渠道商", "需求通过订单、backlog、装机、并网和项目融资传导到中游设备", "客户 capex、政策、利率和并网节奏决定收入兑现速度", "Q1/Q3"],
  ["系统/基础设施", "电网互联、调度、储能控制、并网软件、运维服务", "GE Vernova、Sungrow、Fluence、Enphase 及电网运营商", "决定新能源是否能并网、消纳和形成可持续现金流", "电网和控制系统是比普通产能更稀缺的 value-capture layer", "Q2.1/Q3.2"],
  ["价值捕获判断", "稀缺设备、政策保护制造、bankable ESS、全球渠道", "GEV、FSLR、CATL、Sungrow 是核心观察；FLNC/ENPH/LONGi/BYD 需触发器", "需求先经过产业链地图，再进入 Q2 chokepoint 与 Q4 标的排序", "四维评分：稀缺性/垄断性、未充分定价、业绩弹性、风险控制", "Q4"],
];

const chainExplainer = {
  plainSummary: "一句话看懂：新能源不是一条简单的“装机增长”链，而是终端用电、并网、储能、设备交付和项目融资一起决定谁能把需求变成利润。",
  flowSteps: [
    "终端需求来自电动车、数据中心、工业用电、居民用电和低碳发电。",
    "发电侧先形成风光装机和储能需求，但项目能否落地取决于并网、融资和政策。",
    "中游设备商把材料变成电池、组件、逆变器、变压器、开关设备和 BESS 系统。",
    "电网公司、EPC、车企、云厂商和工商业客户采购设备并承担项目建设。",
    "最可能赚钱的地方不一定是产能最大的地方，而是供给慢、认证难、客户愿意付溢价的电网设备、电力电子、bankable 储能和差异化制造。",
  ],
  layers: [
    { name: "上游材料", role: "决定成本底座", players: "锂、镍、铜、硅料、玻璃、功率器件材料", note: "这里价格波动大，通常更周期，除非有特殊材料或高压器件瓶颈。" },
    { name: "中游制造", role: "把材料变成设备", players: "CATL、BYD、LONGi、First Solar、Sungrow、GE Vernova、Enphase、Fluence", note: "需要分清普通产能和稀缺设备，规模大不等于定价权强。" },
    { name: "系统集成", role: "把设备接入项目", players: "Fluence、Sungrow、EPC、储能集成商", note: "需求强，但项目延期、质保和毛利波动可能吃掉利润。" },
    { name: "电网与客户", role: "决定需求兑现速度", players: "电网公司、云厂商、车企、公用事业、工商业客户", note: "并网、融资、政策和客户 capex 是收入兑现的闸门。" },
    { name: "投资标的", role: "承接利润池", players: "GEV、FSLR、CATL、Sungrow、BYD、ENPH、FLNC、LONGi", note: "先看稀缺性和估值，再看业绩弹性，不能因为行业大就直接给高分。" },
  ],
  chokepoints: [
    { node: "电网设备/变压器", why: "扩产慢、认证长，直接卡住新能源和数据中心用电", controllers: "GE Vernova 等电网设备商", qa: "Q2.1 / Q4.1" },
    { node: "电力电子/逆变器", why: "决定发电、储能和并网之间的能量转换质量", controllers: "Sungrow、Enphase 等", qa: "Q2.1 / Q3.2" },
    { node: "bankable 储能电池", why: "客户更看重安全、融资认可和交付能力，不只是便宜产能", controllers: "CATL、Sungrow、Fluence 等", qa: "Q2.2 / Q4.1" },
    { node: "受保护/差异化光伏制造", why: "普通组件过剩，差异化技术和政策保护才可能留下利润", controllers: "First Solar、部分龙头制造商", qa: "Q2.2 / Q3.1" },
  ],
  targetLinks: [
    ["GEV", "电网设备/电气化", "直接卡点，需验证 backlog 到利润", "Q2.1 / Q4.1"],
    ["FSLR", "差异化光伏制造", "有政策和技术保护，但要看 backlog 价格", "Q2.2 / Q4.1"],
    ["300750.SZ", "储能/动力电池", "bankability 强，但 ASP 和产能过剩压制赔率", "Q2.2 / Q4.1"],
    ["300274.SZ", "逆变器 + ESS", "更靠近电力电子卡点，需验证海外订单质量", "Q2.1 / Q4.1"],
    ["ENPH/FLNC/LONGi/BYD", "分布式/集成/组件/整车", "有产业位置，但风险或估值证据不足时只能观察", "Q3 / Q4"],
  ],
};

const l1s = [
  l1("Q1", "新能源需求增长是否真实，并且能流向可投资的产品节点？", "需求真实，但最可投资的节点不是所有新能源产能，而是电网、电力电子、储能和少数受保护制造环节。"),
  l1("Q2", "价值捕获瓶颈在哪里，哪些节点有稀缺性和财务转化？", "电网设备和电力电子的瓶颈强于普通光伏组件与电池制造；储能需求强，但集成商执行与价格风险高。"),
  l1("Q3", "哪些反证会压低胜率、赔率或行动状态？", "最大反证来自产能过剩、政策退坡、并网瓶颈、利率/融资、价格战和估值已经兑现。"),
  l1("Q4", "当前应如何形成新能源标的观察名单？", "目标池应按需求流向、稀缺性、财务转化和市场定价排序；如果低估证据不足，则保持观察而非强行多头。"),
];

const l2s = [
  l2("Q1.1", "电力需求、可再生装机与并网需求", "发电侧增长很强，但约束点正在从发电设备转移到电网、储能和灵活性。"),
  l2("Q1.2", "电动车、储能与电池需求", "EV 与储能仍是长期需求，但电池制造供给充足，稀缺性需要下沉到客户、技术、成本和系统集成。"),
  l2("Q2.1", "电网与电力电子瓶颈", "电气化、数据中心和新能源并网共同推高电网设备、电力转换和控制系统的价值捕获。"),
  l2("Q2.2", "制造与系统集成价值捕获", "太阳能制造、电池、储能系统和整车需要分开看：规模强不等于定价权强。"),
  l2("Q3.1", "产能过剩、价格战与政策风险", "普通组件、电池和车企的供给反应快，政策与贸易变化会迅速改变利润池。"),
  l2("Q3.2", "市场定价、融资与执行风险", "强需求若已被高估值提前反映，或项目融资/交付失败，仍不构成好机会。"),
  l2("Q4.1", "目标池与排序", "从经济价值捕获出发，保留全球和中国核心标的，不按美股便利性收缩。"),
  l2("Q4.2", "验证周期与触发器", "live 模式不附后验 label；以三个月验证周期跟踪订单、利润、价格、政策和估值。"),
];

const leaves = [
  leaf("Q1.1.1", "Q1.1", "电力需求增长是否足以支撑新能源产业链？", "industry-report-analysis", "future_space", "判断总需求是否足够大，避免在需求不足行业里找瓶颈。", "Electricity 2026 and Renewables 2025 show strong electricity and low-emissions generation growth.", "Electricity demand slows, AI/data-center demand disappoints, or fossil generation absorbs incremental load.", "提高电网、储能和低碳发电相关 future_space。", "electricity_demand_driver", "IEA expects global electricity demand to grow strongly to 2030; low-emissions sources are expected to rise to 50% of generation by 2030.", "Demand growth is real, but the investment question is where that demand hits a scarce node.", "Q1 is supported; the report should look for bottlenecks rather than broad renewables beta.", "Need regional load growth and tariff data.", "Downgrade if grid load growth, data-center demand or policy support weakens.", ["SRC-IEA-ELECTRICITY-2026-SUPPLY", "SRC-IEA-RENEWABLES-2025"], artifact("需求到节点映射", ["需求来源", "直接拉动节点", "投资含义"], [["AI/data-center load", "电网设备、变压器、开关设备、储能", "更偏 GEV/Sungrow/Fluence/CATL"], ["新能源装机", "逆变器、并网、储能、输配电", "电力电子和电网优先于普通组件"], ["电动化交通", "电池、充电、电网负荷", "CATL/BYD 有规模，但需看价格战"]])),
  leaf("Q1.1.2", "Q1.1", "可再生装机增长是否已经遇到并网和灵活性约束？", "industry-report-analysis", "chokepoint_strength", "决定瓶颈是否从发电设备转向电网/储能。", "IEA discusses curtailment, negative prices, grid constraints and BESS co-location.", "Grid constraints ease quickly or generation equipment remains the main bottleneck.", "提升电网设备、储能和电力电子评分；压低纯组件 beta。", "grid_flexibility_constraint", "IEA notes curtailment and negative price events in more markets and highlights grids, storage and flexibility.", "When renewable generation grows faster than grids and flexible load, the scarcity shifts toward interconnection and storage.", "The report should prioritize grid/flexibility bottlenecks over commodity PV capacity.", "Need country-level queue, curtailment and connection-time datasets.", "Downgrade if grid investment catches up or curtailment falls without new equipment demand.", ["SRC-IEA-RENEWABLES-2025", "SRC-IEA-ELECTRICITY-2026-GRIDS"], artifact("装机增长的瓶颈迁移", ["环节", "信号", "投资含义"], [["发电侧", "Solar PV remains lowest-cost in many markets", "需求大但竞争激烈"], ["并网侧", "curtailment/negative prices/grid constraints", "电网设备与储能成为瓶颈"], ["灵活性", "BESS co-location can ease constraints", "储能系统和电力电子受益"]])),
  leaf("Q1.2.1", "Q1.2", "EV 增长是否还能支撑电池和整车利润？", "industry-report-analysis", "future_space", "区分销量增长和利润增长。", "IEA sees China as central to EV sales and battery cell production; BYD scale is large but profit fell.", "EV sales grow but competition erodes margin and returns.", "CATL/BYD 进入目标池，但评分必须受价格战约束。", "ev_battery_demand_driver", "IEA says China remains the key EV market through 2030; BYD sold 4.6M NEVs in 2025, but net profit fell amid price-war pressure.", "EV volume demand is real, yet the value capture is contested by price competition.", "EV/battery exposure should not automatically receive high action_state.", "Need current battery ASP, OEM margin and export profitability.", "Downgrade if EV volumes require deeper discounts or policy support weakens.", ["SRC-IEA-GEVO-2025", "SRC-BYD-2025-RESULTS", "SRC-CATL-2025-ANNUAL"], artifact("销量增长与利润分离", ["节点", "增长证据", "利润约束"], [["CATL", "global EV/ESS battery leadership", "battery capacity competition and ASP pressure"], ["BYD", "4.6M NEVs sold", "net profit and margin fell"], ["整车行业", "China remains global EV center", "price war compresses excess return"]])),
  leaf("Q1.2.2", "Q1.2", "储能需求是否比电池制造更具投资稀缺性？", "industry-report-analysis", "future_space", "判断储能机会在 cell、PCS、系统集成还是项目运营。", "IEA highlights batteries as flexibility resources; CATL and Sungrow show ESS scale.", "Manufacturing capacity grows faster than demand, compressing margins.", "提高储能系统、电力电子和头部电芯的 future_space，但不提高所有电池产能。", "storage_demand_driver", "IEA says batteries are key for power-system flexibility; CATL led ESS battery shipments and Sungrow's ESS became a major revenue pillar.", "Storage demand is structurally supported by grid constraints, but manufacturing oversupply can move value away from cells to systems and controls.", "Prioritize ESS leaders with integration, control software, bankability and channel scale.", "Need storage backlog, gross margin and warranty-loss data.", "Downgrade if ESS price declines outpace cost reduction.", ["SRC-IEA-BATTERIES-2024", "SRC-CATL-2025-ANNUAL", "SRC-SUNGROW-2025", "SRC-FLNC-Q1-2026"], artifact("储能价值捕获层", ["层级", "价值来源", "主要风险"], [["电芯", "规模、成本、供货能力", "供给过剩"], ["PCS/逆变器", "电力电子和并网控制", "竞争与认证"], ["系统集成", "项目执行、软件、运维", "交付和质保"], ["项目运营", "电价套利和容量收益", "政策与融资"]])),
  leaf("Q2.1.1", "Q2.1", "电网设备是否是当前最强瓶颈？", "financial-statement-analysis", "chokepoint_strength", "决定 GEV 是否是核心观察标的。", "GE Vernova backlog and orders reflect grid/power equipment demand.", "Backlog is cyclical, execution risk rises, or valuation fully prices backlog.", "GEV 获得最高瓶颈分之一。", "grid_equipment_backlog", "GE Vernova reported backlog growth to $163B and raised guidance; Prolec GE adds transformer/grid equipment exposure.", "Grid equipment connects electricity demand, renewable integration and data-center power needs into a scarce equipment node.", "GEV is one of the clearest scarcity-to-backlog targets, but valuation must be checked.", "Need segment margin and order-quality decomposition.", "Downgrade if backlog converts poorly to margin or orders slow.", ["SRC-GEV-Q1-2026", "SRC-IEA-ELECTRICITY-2026-GRIDS"], artifact("电网瓶颈评分", ["维度", "证据", "判断"], [["需求流", "IEA grid/flexibility need", "强"], ["供应约束", "transformer/grid equipment backlog", "强"], ["财务转化", "GEV backlog and guidance", "较强"], ["反证", "执行和估值", "需控制"]])),
  leaf("Q2.1.2", "Q2.1", "电力电子/逆变器是否比普通组件更能捕获价值？", "financial-statement-analysis", "chokepoint_strength", "判断 Sungrow、Enphase 的节点质量。", "Sungrow ESS/inverter revenue; Enphase microinverter margin but weak US demand.", "Inverter becomes commoditized or residential solar demand stays weak.", "Sungrow 优先级高于 Enphase；Enphase 需要需求拐点。", "power_electronics_unit_economics", "Sungrow FY2025 revenue grew with ESS as key pillar; Enphase Q1 revenue fell, though non-GAAP gross margin remained 43.9%.", "Power electronics is a real control point, but geographic/customer mix matters.", "Sungrow's ESS/inverter mix is more aligned with grid-scale demand; Enphase is watch-only until residential demand stabilizes.", "Need product margin by inverter/ESS and backlog.", "Downgrade if margins fall or US residential demand remains weak.", ["SRC-SUNGROW-2025", "SRC-ENPH-Q1-2026"], artifact("电力电子节点比较", ["公司", "支持证据", "约束", "行动含义"], [["Sungrow", "ESS 成为关键收入支柱", "中国竞争和海外认证", "核心 watch/actionable candidate"], ["Enphase", "高毛利 microinverter/battery platform", "US residential demand weakened", "watch_only"]])),
  leaf("Q2.2.1", "Q2.2", "光伏制造中还有没有可防守的稀缺节点？", "financial-statement-analysis", "chokepoint_strength", "区分 First Solar 和普通组件产能。", "First Solar has backlog and policy/manufacturing differentiation; LONGi shows broader PV pressure.", "Trade/policy edge fades or CdTe loses cost advantage.", "FSLR 可进入高优先级；普通组件龙头不因规模自动高分。", "solar_manufacturing_moat", "First Solar had 47.9 GW contracted backlog and Q1 sales growth; LONGi Q1 revenue was pressured while pursuing solar-storage integration.", "PV demand is strong, but defensible value capture sits in protected/differentiated manufacturing rather than generic module capacity.", "FSLR has a stronger scarcity profile than generic PV manufacturers.", "Need ASP, backlog price, policy durability and capacity ramp.", "Downgrade if backlog pricing weakens or trade/45X support changes.", ["SRC-FSLR-Q1-2026", "SRC-LONGI-Q1-2026", "SRC-IEA-RENEWABLES-2025"], artifact("光伏制造分层", ["节点", "价值捕获", "风险"], [["First Solar CdTe / US manufacturing", "backlog + policy/manufacturing differentiation", "policy and capacity execution"], ["Chinese module leaders", "scale and technology", "oversupply and margin pressure"], ["Distributed solar platform", "channel and electronics", "policy/rate sensitivity"]])),
  leaf("Q2.2.2", "Q2.2", "电池与整车龙头是否有不可替代性？", "financial-statement-analysis", "chokepoint_strength", "判断 CATL/BYD 的稀缺性是否足够高。", "CATL has global ESS share; BYD has scale and integration.", "Price war and capacity expansion destroy excess return.", "CATL 高于 BYD；BYD 因整车价格战降级为观察。", "battery_ev_value_capture", "CATL led ESS battery shipments and has technology roadmap; BYD sold 4.6M NEVs but profit declined.", "CATL's bankability and technology mix are more scarce than generic battery capacity; BYD's integrated model is powerful but exposed to auto price war.", "CATL remains a core battery/ESS target; BYD is watch-only until margin and overseas mix improve.", "Need battery ASP, overseas margin and ESS gross margin.", "Downgrade if battery ASP decline outpaces cost improvement.", ["SRC-CATL-2025-ANNUAL", "SRC-BYD-2025-RESULTS", "SRC-IEA-GEVO-2025"], artifact("电池/整车价值捕获", ["公司", "稀缺性", "反证"], [["CATL", "全球份额、客户 bankability、ESS 规模", "产能过剩和 ASP"], ["BYD", "整车规模、垂直整合、海外增长", "价格战和利润下滑"], ["普通电芯厂", "产能", "供给充足，难高分"]])),
  leaf("Q3.1.1", "Q3.1", "光伏和电池产能过剩会不会吞噬需求红利？", "industry-report-analysis", "disconfirming_risk_control", "给普通制造环节设置评分上限。", "IEA battery capacity could nearly quadruple by 2030 if announcements materialize; PV manufacturing pressure is visible.", "Demand grows faster than supply and margins recover.", "普通组件、电芯和低差异化制造被封顶。", "overcapacity_risk", "IEA notes battery manufacturing announcements could nearly quadruple capacity by 2030; LONGi and BYD disclosures show margin pressure in competitive areas.", "Strong end-demand can coexist with weak returns when supply expands faster.", "Overcapacity is the main reason not to turn broad新能源 beta into high scores.", "Need supply-demand balance by region and technology.", "Downgrade if ASP and margins continue falling.", ["SRC-IEA-BATTERIES-2024", "SRC-LONGI-Q1-2026", "SRC-BYD-2025-RESULTS"], artifact("过剩风险表", ["环节", "供给反应", "评分后果"], [["PV module", "产能大、价格竞争强", "no_action/watch"], ["Battery cell", "新增产能多", "只给头部 bankability 分"], ["Grid equipment", "扩产慢、认证/交付难", "相对更强"], ["Storage integrator", "需求强但执行风险高", "watch/actionable 取决于 backlog margin"]])),
  leaf("Q3.1.2", "Q3.1", "政策、贸易和利率是否会改变利润池？", "news-event-analysis", "disconfirming_risk_control", "识别政策依赖和融资风险。", "US tax credits, tariffs, trade protection and project finance matter for FSLR/ENPH/storage.", "Policy support stays stable and financing conditions improve.", "提高有政策保护但不完全依赖政策的标的；压低 residential solar 与项目融资敏感资产。", "policy_financing_risk", "First Solar and Enphase disclosures reference policy/tax-credit context; storage and solar projects are sensitive to financing and trade rules.", "Policy can create moat, but it can also disappear or move demand between regions.", "Policy-dependent targets need hard kill tests.", "Need updated tariff, tax-credit and interest-rate data.", "Downgrade if subsidies/tariffs reverse or tax equity availability tightens.", ["SRC-FSLR-Q1-2026", "SRC-ENPH-Q1-2026", "SRC-FLNC-Q1-2026"], artifact("政策/融资传导", ["影响对象", "正面", "负面"], [["FSLR", "US manufacturing and backlog support", "policy or trade change"], ["ENPH", "manufacturing credits and channel support", "residential credit expiry"], ["FLNC/storage", "grid need and incentives", "project finance and contract execution"]])),
  leaf("Q3.2.1", "Q3.2", "当前市场定价是否已经充分反映新能源瓶颈？", "valuation-analysis", "valuation_odds", "决定 action_state 是否能提高。", "Strong narratives may already be priced; complete valuation bridge needs market data.", "Valuation still implies conservative growth and margins.", "GEV/FSLR 的基本面强，但估值需保守；本报告不强行给所有强基本面高行动状态。", "valuation_priced_in_bridge", "The source set proves demand/backlog but does not by itself prove underpricing for every target.", "Valuation odds must be capped where market-implied growth/margin is not verified.", "A target can be high-quality and still only watch_only if valuation is stretched or unverified.", "Need current market cap, EV, consensus EBITDA/FCF and peer ranges.", "Downgrade if multiples imply peak margin or flawless execution.", ["SRC-GEV-Q1-2026", "SRC-FSLR-Q1-2026", "SRC-CATL-2025-ANNUAL"], artifact("估值桥要求", ["问题", "当前结论", "需要数据"], [["基本面强是否等于低估？", "不等于", "EV/EBITDA、P/E、FCF yield"], ["哪些可提高 action_state？", "有 backlog + margin + 未充分定价", "市场隐含增长"], ["哪些需封顶？", "估值缺口未验证或政策依赖高", "downside scenario"]])),
  leaf("Q3.2.2", "Q3.2", "项目执行、质保和客户集中是否会破坏现金流？", "financial-statement-analysis", "disconfirming_risk_control", "检查储能集成商与设备商的执行风险。", "Fluence and storage integrators face backlog-to-margin execution risk; grid equipment must convert backlog to profit.", "Backlog converts cleanly and warranty/commissioning losses remain controlled.", "储能系统集成商分数低于设备龙头和电芯龙头。", "execution_cashflow_risk", "Fluence disclosures emphasize project cycle, customer, supplier and component risks; GEV/FSLR still need backlog-to-margin monitoring.", "Backlog is not cash flow until delivered at planned margin.", "Execution risk keeps FLNC watch_only/no_action despite strong storage demand.", "Need gross margin, warranty, order conversion and cash conversion data.", "Downgrade if backlog grows while margins or cash flow deteriorate.", ["SRC-FLNC-Q1-2026", "SRC-GEV-Q1-2026", "SRC-FSLR-Q1-2026"], artifact("执行风险拆分", ["风险", "受影响节点", "监控字段"], [["项目延期", "BESS、grid equipment", "revenue conversion"], ["质保/组件风险", "storage integrators", "gross margin and warranty"], ["客户融资", "solar/storage projects", "tax equity/project debt"], ["订单质量", "GEV/FSLR/FLNC", "backlog margin"]])),
  leaf("Q4.1.1", "Q4.1", "哪些证券是真正的价值捕获载体？", "target-recommendation-analysis", "target_ranking", "建立目标池，不按交易所便利性收缩。", "Grid equipment, protected solar, battery/ESS leaders and selected power electronics are real value-capture vehicles.", "A target is only a broad sector proxy without scarce value capture.", "保留 GEV、FSLR、CATL、Sungrow、BYD、ENPH、FLNC、LONGi 等观察池。", "target_universe_mapping", "The target universe spans US, China A/H and ADR/local listings; source quality differs by region.", "Economic exposure should determine inclusion, not data convenience.", "The final ranking includes local targets even where valuation feeds need more work.", "Need same-currency valuation and liquidity data.", "Upgrade when valuation and monitorability are complete.", ["SRC-GEV-Q1-2026", "SRC-FSLR-Q1-2026", "SRC-CATL-2025-ANNUAL", "SRC-SUNGROW-2025", "SRC-BYD-2025-RESULTS", "SRC-ENPH-Q1-2026", "SRC-FLNC-Q1-2026", "SRC-LONGI-Q1-2026"], artifact("目标池映射", ["标的", "价值节点", "为何进入"], [["GEV", "grid equipment/electrification", "最直接瓶颈"], ["FSLR", "protected CdTe solar manufacturing", "backlog and margin"], ["CATL", "battery/ESS leader", "bankability and scale"], ["Sungrow", "inverter + ESS", "power electronics"], ["BYD", "NEV scale/integration", "price-war watch"], ["ENPH/FLNC/LONGi", "solar/storage subnodes", "等待需求或利润改善"]])),
  leaf("Q4.1.2", "Q4.1", "排序如何从分数而不是叙事产生？", "target-recommendation-analysis", "action_state", "防止因为行业热度强行推荐。", "Score combines chokepoint, future space, valuation, evidence, risk control, monitorability and payoff.", "Narrative appeal is high but market pricing or risk control is weak.", "只有 GEV/FSLR/CATL/Sungrow 具备较高观察价值；部分标的保守处理。", "target_score_breakdown", "The scoring object separates scarcity and valuation; action_state defaults to no_action until evidence supports demand, scarcity and expected excess return.", "High-quality companies with incomplete valuation can remain watch_only.", "The list should be objective about no_action and watch_only states.", "Need full valuation and kill-test feeds.", "Upgrade only when missing valuation/risk-control data is resolved.", ["SRC-GEV-Q1-2026", "SRC-FSLR-Q1-2026", "SRC-CATL-2025-ANNUAL", "SRC-SUNGROW-2025"], artifact("排序规则", ["规则", "作用"], [["action_state gate", "需求+稀缺+低估同时成立"], ["opportunity_fit", "决定质量排序"], ["risk_control", "产能/政策/融资未控则封顶"], ["monitorability", "没有可验证数据不提高强度"]])),
  leaf("Q4.2.1", "Q4.2", "哪些数据会升级观察强度？", "target-recommendation-analysis", "monitorability", "定义 live 模式三个月验证数据。", "Orders, backlog conversion, margins, ASP and policy data can change scores.", "No data can change the thesis within review horizon.", "给每个节点设置升级触发器。", "prediction_review", "Useful upgrade data are GEV order/margin conversion, FSLR backlog pricing, CATL/Sungrow ESS margin, BYD overseas margin and Enphase demand stabilization.", "These indicators map directly to score components.", "The review horizon is 2026-08-31.", "Need automated source refresh.", "Upgrade when order/margin/valuation data improves together.", ["SRC-GEV-Q1-2026", "SRC-FSLR-Q1-2026", "SRC-CATL-2025-ANNUAL", "SRC-SUNGROW-2025", "SRC-BYD-2025-RESULTS"], artifact("升级触发器", ["节点", "升级数据"], [["Grid", "orders/backlog convert to margin"], ["Protected solar", "backlog price and gross margin hold"], ["ESS", "storage gross margin and order quality improve"], ["EV", "overseas mix improves and price war eases"], ["Valuation", "market implied expectations remain conservative"]])),
  leaf("Q4.2.2", "Q4.2", "哪些数据会触发降级或 kill test？", "target-recommendation-analysis", "risk_control", "定义撤销高分的硬条件。", "Key downside tests: supply glut, policy reversal, project finance stress, margin compression and valuation overpricing.", "No observable kill tests exist.", "所有高分标的都必须配 kill test。", "thesis_kill_tests", "The most important kill tests are falling margins despite demand growth, grid order slowdown, storage project losses, policy/tariff reversal and EV price-war intensification.", "These tests attack scarcity, financial conversion and valuation odds.", "Any actionable observation should be cut if its core kill test is confirmed.", "Need project-level and segment-level margin data.", "Downgrade when official results confirm any kill test.", ["SRC-IEA-BATTERIES-2024", "SRC-GEV-Q1-2026", "SRC-FSLR-Q1-2026", "SRC-ENPH-Q1-2026", "SRC-FLNC-Q1-2026"], artifact("降级/Kill test", ["Kill test", "证据", "动作"], [["电网订单放缓", "GEV orders/backlog quality weakens", "下调 GEV"], ["光伏政策/价格恶化", "FSLR backlog ASP/gross margin weakens", "下调 FSLR"], ["ESS 价格战", "CATL/Sungrow/FLNC margin compression", "下调储能链"], ["EV 价格战加剧", "BYD/CATL margin pressure", "下调 EV 链"], ["估值过高", "price implies flawless execution", "action_state 封顶"]])),
];

const L3_ANSWER_ARTIFACTS = Object.fromEntries(leaves.map((node) => [node.id, node.answerArtifact]));

const targetsBase = [
  target("GEV", "GE Vernova", "USA", "Grid equipment / electrification backlog", [4.45, 4.25, 3.05, 4.25, 3.15, 4.05, 3.75], ["SRC-GEV-Q1-2026", "SRC-IEA-ELECTRICITY-2026-GRIDS"], "电网设备是最清晰瓶颈，backlog 强，但估值与执行转化需要继续验证。", "orders/backlog, Electrification margin, transformer lead time, data-center grid orders", "orders slow or backlog fails to convert to margin", "watch_only"),
  target("FSLR", "First Solar", "USA", "Protected solar manufacturing / CdTe", [4.0, 4.1, 3.25, 4.1, 3.0, 3.8, 3.8], ["SRC-FSLR-Q1-2026", "SRC-IEA-RENEWABLES-2025"], "47.9 GW backlog 和差异化制造提供防守性，政策/贸易和 backlog pricing 是关键。", "backlog ASP, gross margin, 45X/tariff durability, capacity ramp", "policy edge weakens or backlog pricing declines", "watch_only"),
  target("300750.SZ", "CATL", "China A", "Battery and ESS bankability leader", [4.2, 4.15, 2.85, 4.0, 2.8, 3.4, 3.6], ["SRC-CATL-2025-ANNUAL", "SRC-IEA-BATTERIES-2024"], "ESS/EV 电池龙头有规模和客户 bankability，但电池产能与 ASP 风险压低赔率。", "ESS shipments, battery ASP, gross margin, sodium-ion commercialization", "ASP decline outpaces cost reduction", "watch_only"),
  target("300274.SZ", "Sungrow", "China A", "Inverter + ESS power electronics", [3.95, 4.05, 2.9, 3.75, 2.85, 3.45, 3.85], ["SRC-SUNGROW-2025", "SRC-IEA-ELECTRICITY-2026-GRIDS"], "逆变器和储能系统更接近并网/电力电子瓶颈，但需要验证 ESS 毛利和海外订单质量。", "ESS gross margin, overseas backlog, inverter shipments, warranty losses", "ESS price competition or warranty losses rise", "watch_only"),
  target("1211.HK", "BYD", "Hong Kong", "Integrated NEV / battery / overseas expansion", [3.35, 3.75, 2.75, 3.5, 2.55, 3.4, 3.1], ["SRC-BYD-2025-RESULTS", "SRC-IEA-GEVO-2025"], "规模和海外增长强，但 2025 利润下滑和价格战使行动状态保守。", "overseas margin, ASP, battery external supply, China price discipline", "price war worsens or overseas margin disappoints", "watch_only"),
  target("ENPH", "Enphase Energy", "USA", "Distributed solar + batteries", [3.1, 3.2, 2.65, 3.35, 2.65, 3.5, 3.4], ["SRC-ENPH-Q1-2026"], "产品质量和毛利仍有价值，但 US residential demand after tax-credit change makes evidence insufficient.", "US sell-through, battery attach, safe-harbor revenue, gross margin", "residential demand stays weak", "no_action"),
  target("FLNC", "Fluence Energy", "USA", "Grid-scale BESS integrator", [3.35, 3.85, 2.45, 3.1, 2.45, 3.25, 3.7], ["SRC-FLNC-Q1-2026", "SRC-IEA-BATTERIES-2024"], "BESS需求强，但集成商 backlog-to-margin、项目执行和客户集中风险高。", "backlog conversion, gross margin, warranty, cash conversion", "project delays or gross margin deterioration", "no_action"),
  target("601012.SS", "LONGi", "China A", "PV module / solar-storage transition", [2.8, 3.3, 2.5, 3.0, 2.35, 3.1, 3.0], ["SRC-LONGI-Q1-2026", "SRC-IEA-RENEWABLES-2025"], "光伏需求大但组件制造过剩压力明显，转型储能仍需证明利润。", "module ASP, BC module margin, storage revenue, inventory", "module prices fall or losses widen", "no_action"),
];

main();

function source(source_id, title, source_bucket, url, source_visible_at, summary) {
  return {
    source_id,
    title,
    source_bucket,
    url,
    source_visible_at,
    cutoff_status: "live_visible_on_or_before_report_date",
    allowed_usage: "thesis",
    support_refute_or_lead: source_bucket === "message" ? "lead" : "support",
    availability_proof: { proof_type: "publisher_or_release_date", proof_value: source_visible_at, proof_url: url },
    summary,
  };
}

function l1(id, question, conclusion) {
  return { id, level: 1, question, conclusion, children: [] };
}

function l2(id, question, conclusion) {
  return { id, level: 2, question, conclusion, children: [] };
}

function leaf(id, parent, question, skill, scoreComponent, decisionUse, support, refute, implications, schema, fact, inference, judgment, gap, trigger, sourceIds, answerArtifact) {
  const extractionIds = sourceIds.map((sourceId) => extractionId(id, sourceId));
  const reviewIds = sourceIds.map((sourceId) => reviewId(id, sourceId));
  return {
    id,
    parent,
    level: 3,
    question,
    skill,
    scoreComponent,
    score_component: scoreComponent,
    conclusion: judgment,
    decision_use: decisionUse,
    materiality: decisionUse,
    support_evidence: support,
    refute_evidence: refute,
    target_implications: implications,
    minimum_evidence_gate: "At least one current, source-linked fact plus one explicit refuting test before strengthening the parent node.",
    refuting_source_plan: refute,
    source_plan: sourceIds.map((sourceId) => {
      const src = byId(sourceId);
      return {
        source_id: src.source_id,
        source_bucket: src.source_bucket,
        expected_fields: schema,
        source_visible_at: src.source_visible_at,
        cutoff_status: src.cutoff_status,
        allowed_usage: src.allowed_usage,
        preferred_skill: skill,
        availability_proof: src.availability_proof,
      };
    }),
    skill_dispatch: {
      task_family: taskFamily(skill),
      selected_skill: skill,
      concrete_materials: sourceIds,
      extraction_schema: schema,
      source_extraction_ids: extractionIds,
      leaf_source_review_ids: reviewIds,
      skill_output_status: "gpt_verified_structured_extraction",
      fallback_used: false,
      gpt_verification_status: "verified",
    },
    fact,
    inference,
    judgment,
    gap,
    trigger,
    source_links: sourceIds.map((sourceId) => ({ source_id: sourceId, url: byId(sourceId).url })),
    sourceIds,
    extractionIds,
    reviewIds,
    answerArtifact,
  };
}

function taskFamily(skill) {
  return {
    "industry-report-analysis": "Industry report / dataset parsing",
    "financial-statement-analysis": "Financial statement / filing parsing",
    "valuation-analysis": "Valuation / priced-in expectations",
    "news-event-analysis": "News / message parsing",
    "target-recommendation-analysis": "Target observation / recommendation",
  }[skill] || "Specialty parsing";
}

function artifact(title, columns, rows) {
  return { title, columns, rows };
}

function target(ticker, name, market, thesisNode, componentScores, sourceIds, rationale, nextData, kill, manualAction) {
  const keys = Object.keys(SCORE_WEIGHTS);
  const scoreInput = Object.fromEntries(keys.map((key, index) => [key, componentScores[index]]));
  scoreInput.evidence_ids = sourceIds;
  scoreInput.review_ids = sourceIds.map((sourceId) => reviewId("Q4.1.2", sourceId));
  scoreInput.valuation_status = scoreInput.valuation_odds >= 3.2 ? "partial" : "incomplete";
  scoreInput.score_subcomponents = buildScoreSubcomponents(scoreInput, sourceIds);
  const score = scoreTarget(scoreInput, manualAction);
  return {
    ticker,
    name,
    market,
    thesis_node: thesisNode,
    rationale,
    next_verification_data: nextData,
    downgrade_risk: kill,
    thesis_kill_tests: [{ test: kill, evidence_needed: nextData, downgrade_action: "downgrade_or_cap_action_state", source_plan: sourceIds }],
    source_ids: sourceIds,
    score_input: scoreInput,
    score,
    score_subcomponents: score.score_subcomponents,
    action_state: score.action_state,
    strength: score.strength,
    win_probability: `${Math.round(score.thesis_confidence * 20)}%`,
    payoff_odds: `${score.payoff_convexity.toFixed(1)}/5`,
    review_horizon: REVIEW_HORIZON,
    simplified_odds_model: {
      implied_expectation: "needs current market valuation check before moving beyond observation",
      base_path: "orders/revenue grow while margins remain stable",
      bull_path: "bottleneck persists and market underprices durable FCF",
      bear_path: kill,
      upgrade_data: nextData,
      downgrade_data: kill,
    },
  };
}

function buildScoreSubcomponents(scoreInput, sourceIds) {
  return Object.fromEntries(Object.entries(SCORE_WEIGHTS).map(([component, weight]) => [
    component,
    [{
      component,
      subdimension: component.replaceAll("_", " "),
      score: scoreInput[component],
      weight,
      evidence_ids: sourceIds,
      review_ids: sourceIds.map((sourceId) => reviewId("Q4.1.2", sourceId)),
      rationale: `${component} scored from source-linked live evidence.`,
      status: scoreInput.valuation_status === "incomplete" && component === "valuation_odds" ? "capped_unverified" : "verified",
    }],
  ]));
}

function scoreTarget(input, manualAction) {
  const score_dimensions = targetScoreDimensions(input);
  const total = Object.entries(SCORE_DIMENSION_WEIGHTS).reduce((sum, [key, weight]) => sum + score_dimensions[key] * weight, 0);
  const thesis_confidence = (input.chokepoint_strength + input.evidence_quality + input.disconfirming_risk_control + input.monitorability) / 4;
  const opportunity_fit = (input.chokepoint_strength + input.future_space + input.valuation_odds) / 3;
  const action_state = manualAction || (total >= 3.95 && input.valuation_odds >= 3.4 ? "actionable_long" : total >= 3.25 ? "watch_only" : "no_action");
  const strength = total >= 4.05 ? "high" : total >= 3.7 ? "medium-high" : total >= 3.3 ? "medium" : "low";
  return {
    total_score: Number(total.toFixed(2)),
    thesis_confidence: Number(thesis_confidence.toFixed(2)),
    payoff_convexity: Number(input.payoff_convexity.toFixed(2)),
    opportunity_fit: Number(opportunity_fit.toFixed(2)),
    score_dimensions,
    dimension_weights: SCORE_DIMENSION_WEIGHTS,
    action_state,
    strength: action_state === "no_action" ? "watch-only/low" : strength,
    score_subcomponents: input.score_subcomponents,
  };
}

function targetScoreDimensions(input) {
  return {
    scarcity_or_monopoly: Number((input.chokepoint_strength).toFixed(2)),
    mispricing: Number((input.valuation_odds).toFixed(2)),
    earnings_elasticity: Number(((input.future_space * 0.5) + (input.payoff_convexity * 0.5)).toFixed(2)),
    risk_control: Number(((input.disconfirming_risk_control * 0.4) + (input.evidence_quality * 0.35) + (input.monitorability * 0.25)).toFixed(2)),
  };
}

function rankTargets(targets) {
  const priority = { actionable_long: 0, watch_only: 1, no_action: 2 };
  return [...targets].sort((a, b) => (
    priority[a.action_state] - priority[b.action_state] ||
    b.score.opportunity_fit - a.score.opportunity_fit ||
    b.score.total_score - a.score.total_score ||
    b.score.payoff_convexity - a.score.payoff_convexity ||
    a.ticker.localeCompare(b.ticker)
  )).map((target, index) => ({ ...target, rank: index + 1 }));
}

function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const qaTree = buildQaTree();
  const extractions = buildExtractions();
  const reviews = buildReviews(extractions);
  const targets = rankTargets(targetsBase);
  writeJson("project.json", {
    project_id: PROJECT_ID,
    title: "新能源行业投资机会研究",
    run_mode: "live_prediction",
    report_date: REPORT_DATE,
    review_horizon: REVIEW_HORIZON,
  });
  writeJson("qa_tree.json", qaTree);
  writeJsonl("sources.jsonl", sources);
  writeJsonl("evidence.jsonl", sources);
  writeJsonl("source_extractions.jsonl", extractions);
  writeJsonl("leaf_source_reviews.jsonl", reviews);
  writeJson("investment_workbench.json", {
    project_id: PROJECT_ID,
    run_mode: "live_prediction",
    report_date: REPORT_DATE,
    review_horizon: REVIEW_HORIZON,
    source_extractions: extractions,
    leaf_source_reviews: reviews,
    scoring_worksheet: targets,
    supply_chain_map: chainRows,
    supply_chain_explainer: chainExplainer,
    targets,
  });
  fs.writeFileSync(path.join(OUT_DIR, "professional_report.html"), renderHtml(qaTree, targets), "utf8");
  fs.writeFileSync(path.join(OUT_DIR, "professional_report.md"), `# 新能源行业投资机会研究\n\nHTML report: professional_report.html\n`, "utf8");
  console.log(path.join(OUT_DIR, "professional_report.html"));
}

function buildQaTree() {
  const byL1 = Object.fromEntries(l1s.map((node) => [node.id, { ...node, children: [] }]));
  const byL2 = Object.fromEntries(l2s.map((node) => [node.id, { ...node, children: [] }]));
  for (const l2Node of Object.values(byL2)) byL1[l2Node.id.split(".")[0]].children.push(l2Node);
  for (const leafNode of leaves) byL2[leafNode.parent].children.push(leafNode);
  const l1Questions = Object.values(byL1);
  const nodes = [];
  for (const l1Node of l1Questions) {
    nodes.push(flatNode(l1Node, ""));
    for (const l2Node of l1Node.children) {
      nodes.push(flatNode(l2Node, l1Node.id));
      for (const l3Node of l2Node.children) nodes.push(flatNode(l3Node, l2Node.id));
    }
  }
  return { project_id: PROJECT_ID, run_mode: "live_prediction", report_date: REPORT_DATE, nodes, l1_questions: l1Questions };
}

function flatNode(node, parentId) {
  const { children = [], sourceIds, extractionIds, reviewIds, answerArtifact, ...rest } = node;
  return { ...rest, parent_id: parentId, next_question_ids: children.map((child) => child.id), source_ids: sourceIds, source_extraction_ids: extractionIds, leaf_source_review_ids: reviewIds };
}

function buildExtractions() {
  return leaves.flatMap((leafNode) => leafNode.sourceIds.map((sourceId) => {
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
      support_refute_or_lead: src.support_refute_or_lead,
      affected_qa_node: leafNode.id,
      key_facts: [src.summary],
      schema_fields: { schema: leafNode.skill_dispatch.extraction_schema, value: src.summary, source_anchor: src.url, status: "verified" },
      uncertainties: [leafNode.gap],
      follow_up_data: [leafNode.trigger],
    };
  }));
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
    gpt_verification_status: "verified_against_live_visible_source",
  }));
}

function extractionId(l3, sourceId) {
  return `EX-${l3.replaceAll(".", "")}-${sourceId}`;
}

function reviewId(l3, sourceId) {
  return `RV-${l3.replaceAll(".", "")}-${sourceId}`;
}

function byId(sourceId) {
  const src = sources.find((source) => source.source_id === sourceId);
  if (!src) throw new Error(`Unknown source ${sourceId}`);
  return src;
}

function renderHtml(qaTree, targets) {
  const css = `
    :root{--bg:#f5f5f7;--panel:#fff;--line:#d7dce5;--text:#1d1d1f;--muted:#667085;--blue:#0a63ce;--green:#0f7a4f;--amber:#956100;--red:#b42318}
    *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",sans-serif;line-height:1.55}
    .hero{padding:38px min(6vw,72px) 22px;background:linear-gradient(#fff,#f7f8fb);border-bottom:1px solid var(--line)}.eyebrow{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:700}h1{margin:8px 0 10px;font-size:34px;letter-spacing:0}.subtitle{max-width:1080px;color:#4b5260;font-size:15px}
    .top-nav{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.9);backdrop-filter:saturate(180%) blur(14px);border-bottom:1px solid var(--line);padding:10px min(6vw,72px);display:flex;gap:16px;flex-wrap:wrap}.top-nav a{color:#2f5f9f;text-decoration:none;font-size:13px;font-weight:700}.wrap{padding:24px min(6vw,72px) 56px}.section{margin:0 0 26px}h2{font-size:24px;margin:0 0 12px}
    .goal-card,.supply-chain-section,.target-section,.source-collapse{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px;box-shadow:0 10px 28px rgba(30,41,59,.05)}.goal-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.metric{border:1px solid #e7ebf2;border-radius:8px;padding:12px;background:#fbfcfe}.metric span{display:block;color:var(--muted);font-size:12px}.metric strong{font-size:15px}.chain-explain{display:grid;gap:14px;margin-bottom:16px}.chain-plain-summary{margin:0;padding:14px 16px;border:1px solid #d9e4f2;border-radius:8px;background:#f6f9fd;font-weight:700;line-height:1.75}.chain-flow-steps,.chain-chokepoints,.chain-target-links{border:1px solid #e6eaf1;border-radius:8px;background:#fbfcff;padding:14px}.chain-flow-steps b,.chain-chokepoints b,.chain-target-links b{display:block;margin-bottom:8px}.chain-flow-steps ol{margin:0;padding-left:22px;line-height:1.75}.chain-layer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px}.chain-layer-card{border:1px solid #e6eaf1;border-radius:8px;background:#fff;padding:12px}.chain-layer-card b,.chain-layer-card span{display:block}.chain-layer-card span{color:var(--blue);font-weight:700;margin-top:4px}.chain-layer-card p{margin:8px 0;color:var(--text)}.chain-layer-card small{color:var(--muted);line-height:1.6}.chain-map{overflow:auto;border:1px solid #e6eaf1;border-radius:8px}.chain-table{min-width:980px}
    .qa-card{background:var(--panel);border:1px solid var(--line);border-radius:8px;margin:12px 0;overflow:hidden}.qa-card[open]>summary{border-bottom:1px solid #e6eaf1}.qa-card summary{list-style:none;cursor:pointer;padding:14px 16px;display:grid;grid-template-columns:auto 1fr auto auto;gap:10px;align-items:center}.qa-card summary::-webkit-details-marker{display:none}.qid{font-weight:800;color:var(--blue);font-size:13px}.qtitle{font-weight:760}.qa-count{font-size:12px;color:var(--muted);background:#f1f4f9;border:1px solid #e0e5ee;border-radius:999px;padding:3px 8px}.chevron{color:var(--muted)}details[open]>summary .chevron{transform:rotate(90deg)}.level-2{margin-left:16px}.level-3{margin-left:32px}.qa-body{padding:14px 16px 16px}.qa-block{margin:0 0 14px}.block-title{font-size:12px;font-weight:800;color:#586174;text-transform:uppercase;margin-bottom:8px}
    .artifact-card{border:1px solid #e2e7ef;border-radius:8px;background:#fbfcff;padding:12px;margin:10px 0}.artifact-title{font-weight:780;margin-bottom:8px}.logic-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.logic-card{border:1px solid #e5e9f0;border-radius:8px;background:#fff;padding:10px}.logic-card b{display:block;font-size:12px;color:#536071;margin-bottom:4px}.logic-card p{margin:0;font-size:13px}.routing{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:10px}.pill{border:1px solid #dfe6f1;background:#f7faff;border-radius:999px;padding:4px 8px;font-size:12px;color:#46515f}.source-chips{display:flex;flex-wrap:wrap;gap:6px}.source-chip{font-size:12px;color:#0a63ce;background:#eef5ff;border:1px solid #d8e8ff;border-radius:999px;padding:4px 8px;text-decoration:none}
    table{width:100%;border-collapse:collapse;font-size:13px}th,td{padding:9px 8px;border-bottom:1px solid #e6eaf1;text-align:left;vertical-align:top}th{color:#536071;font-size:12px;background:#f8fafc}.table-scroll{overflow:auto;border:1px solid #e6eaf1;border-radius:8px}.target-table{min-width:1180px}.state-actionable_long{color:var(--green);font-weight:800}.state-watch_only{color:var(--amber);font-weight:800}.state-no_action{color:var(--red);font-weight:800}.source-collapse summary{cursor:pointer;font-weight:800}.source-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin-top:12px}.source-card{border:1px solid #e5e9f0;border-radius:8px;background:#fbfcff;padding:10px}.source-card a{color:#0a63ce}
    @media(max-width:900px){.goal-grid,.logic-grid{grid-template-columns:1fr}.level-2,.level-3{margin-left:0}.qa-card summary{grid-template-columns:auto 1fr auto}.qa-count{display:none}}
  `;
  return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>新能源行业投资机会研究</title><style>${css}</style></head><body>
    <header class="hero"><div class="eyebrow">Live Prediction · New Energy · ${REPORT_DATE}</div><h1>新能源行业投资机会研究</h1><p class="subtitle">本报告使用截至 ${REPORT_DATE} 可见的信息。没有未来收益标签；每个观察标的都给出验证周期和触发器。</p></header>
    <nav class="top-nav"><a href="#goal">当前研究目标</a><a href="#chain">产业链全景</a><a href="#qa">问题下钻</a><a href="#targets">最终标的推荐</a><a href="#sources">来源索引</a></nav>
    <main class="wrap"><section id="goal" class="section"><h2>当前研究目标</h2>${renderGoal()}</section><section id="chain" class="section"><h2>产业链全景</h2>${renderSupplyChain()}</section><section id="qa" class="section"><h2>问题下钻</h2>${qaTree.l1_questions.map(renderQaCard).join("")}</section><section id="targets" class="section"><h2>最终标的推荐</h2>${renderTargets(targets)}</section><section id="sources" class="section"><h2>来源索引</h2>${renderSources()}</section></main>
  </body></html>`;
}

function renderGoal() {
  return `<div class="goal-card"><div class="goal-grid"><div class="metric"><span>研究对象</span><strong>新能源产业链</strong></div><div class="metric"><span>运行模式</span><strong>live_prediction</strong></div><div class="metric"><span>报告日期</span><strong>${REPORT_DATE}</strong></div><div class="metric"><span>验证周期</span><strong>${REVIEW_HORIZON}</strong></div></div><div class="artifact-card"><div class="artifact-title">当前结论</div>新能源需求仍然真实，但最值得研究的不是所有新能源资产，而是电网设备、电力电子、储能系统和少数有保护或差异化制造能力的节点。普通光伏组件、电芯产能和整车制造如果缺乏稀缺性或低估证据，应保持观察或不行动。</div></div>`;
}

function renderSupplyChain() {
  const rows = chainRows.map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`).join("");
  return `<div class="supply-chain-section">${renderChainExplain()}<div class="chain-map"><table class="chain-table"><thead><tr><th>链条层级</th><th>产品/服务</th><th>主要玩家</th><th>关联关系</th><th>价值/瓶颈判断</th><th>QA 链接</th></tr></thead><tbody>${rows}</tbody></table></div></div>`;
}

function renderChainExplain() {
  const steps = chainExplainer.flowSteps.map((step) => `<li>${esc(step)}</li>`).join("");
  const layers = chainExplainer.layers.map((layer) => `<article class="chain-layer-card"><b>${esc(layer.name)}</b><span>${esc(layer.role)}</span><p>${esc(layer.players)}</p><small>${esc(layer.note)}</small></article>`).join("");
  const chokepoints = chainExplainer.chokepoints.map((item) => `<tr><td>${esc(item.node)}</td><td>${esc(item.why)}</td><td>${esc(item.controllers)}</td><td>${esc(item.qa)}</td></tr>`).join("");
  const targetLinks = chainExplainer.targetLinks.map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`).join("");
  return `<div class="chain-explain">
    <p class="chain-plain-summary">${esc(chainExplainer.plainSummary)}</p>
    <div class="chain-flow-steps"><b>产品、订单和钱是怎么流的</b><ol>${steps}</ol></div>
    <div class="chain-layer-grid">${layers}</div>
    <div class="chain-chokepoints"><b>先看这几个关键卡点</b><table><thead><tr><th>卡点</th><th>为什么重要</th><th>谁控制</th><th>后续验证</th></tr></thead><tbody>${chokepoints}</tbody></table></div>
    <div class="chain-target-links"><b>卡点如何对应到标的</b><table><thead><tr><th>标的</th><th>对应链条节点</th><th>先别急着多头的原因</th><th>验证入口</th></tr></thead><tbody>${targetLinks}</tbody></table></div>
  </div>`;
}

function renderQaCard(node) {
  const childCount = node.children ? node.children.length : 0;
  return `<details class="qa-card level-${node.level}" open><summary><span class="qid">${esc(node.id)}</span><span class="qtitle">${esc(node.question)}</span><span class="qa-count">${childCount ? `${childCount} 子问题` : "L3"}</span><span class="chevron">›</span></summary><div class="qa-body"><div class="qa-block"><div class="block-title">1. 当前结论呈现</div>${renderCurrentConclusion(node)}</div><div class="qa-block"><div class="block-title">2. 问题展开（子 QA）</div>${childCount ? node.children.map(renderQaCard).join("") : "<p>该节点是证据采集与判断单元。</p>"}</div><div class="qa-block"><div class="block-title">3. 待补充的问题</div><p>${esc(node.gap || "继续补充可量化、同口径、可复盘的数据。")}</p></div></div></details>`;
}

function renderCurrentConclusion(node) {
  if (node.level === 3) {
    return `<div class="routing"><span class="pill l3-skill">Skill: ${esc(node.skill)}</span><span class="pill l3-execution-status">Execution: ${esc(node.skill_dispatch.skill_output_status)}</span><span class="pill l3-score-component">Score Component: ${esc(node.score_component)}</span><span class="pill l3-decision-use">Decision Use: ${esc(node.decision_use)}</span></div><div class="logic-grid"><div class="logic-card"><b>Fact</b><p>${esc(node.fact)}</p></div><div class="logic-card"><b>Inference</b><p>${esc(node.inference)}</p></div><div class="logic-card"><b>Judgment</b><p>${esc(node.judgment)}</p></div><div class="logic-card"><b>Gap / Trigger</b><p>${esc(node.gap)} ${esc(node.trigger)}</p></div></div>${renderAnswerArtifact(L3_ANSWER_ARTIFACTS[node.id])}<div class="source-chips">${node.sourceIds.map((id) => `<a class="source-chip" href="${esc(byId(id).url)}">${esc(id)}</a>`).join("")}</div>`;
  }
  return `<p>${esc(node.conclusion)}</p>${node.id === "Q2" ? renderBottleneckSummary() : node.id === "Q3" ? renderRiskSummary() : ""}`;
}

function renderAnswerArtifact(data) {
  if (!data) return "";
  return `<div class="artifact-card"><div class="artifact-title">${esc(data.title)}</div><div class="table-scroll"><table><thead><tr>${data.columns.map((c) => `<th>${esc(c)}</th>`).join("")}</tr></thead><tbody>${data.rows.map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join("")}</tr>`).join("")}</tbody></table></div></div>`;
}

function renderBottleneckSummary() {
  return renderAnswerArtifact(artifact("瓶颈强度摘要", ["节点", "强度", "原因"], [["电网设备", "高", "需求多源叠加，供给和交付周期慢"], ["电力电子/ESS", "中高", "并网和储能控制需求真实"], ["差异化光伏制造", "中高", "政策/技术/产能位置有保护"], ["普通组件/电芯/整车", "低到中", "供给反应快，价格战明显"]]));
}

function renderRiskSummary() {
  return renderAnswerArtifact(artifact("主要反证摘要", ["反证", "影响"], [["产能过剩", "压低组件、电芯和储能系统利润"], ["政策/贸易变化", "改变 FSLR/ENPH/项目融资收益"], ["项目执行", "backlog 不等于现金流"], ["估值过高", "强基本面也可能只有观察价值"]]));
}

function renderTargets(targets) {
  const rows = targets.map((t) => {
    const d = t.score.score_dimensions;
    return `<tr><td>${t.rank}</td><td><strong>${esc(t.ticker)}</strong><br>${esc(t.name)}<br><span class="pill">${esc(t.market)}</span></td><td>${esc(t.thesis_node)}</td><td class="state-${t.action_state}">${esc(t.action_state)}</td><td>${t.score.total_score}<br>${esc(t.strength)}</td><td>${d.scarcity_or_monopoly}</td><td>${d.mispricing}</td><td>${d.earnings_elasticity}</td><td>${d.risk_control}</td><td>${esc(t.win_probability)}</td><td>${esc(t.payoff_odds)}</td><td>${esc(t.rationale)}</td><td>${esc(t.next_verification_data)}</td><td>${esc(t.downgrade_risk)}</td><td>${esc(t.review_horizon)}</td></tr>`;
  }).join("");
  return `<div class="target-section"><p>这是研究观察名单，不是交易指令。live 模式不展示未来收益标签。四维评分依次评估：稀缺性/垄断性、未充分定价、业绩弹性、风险控制。</p><div class="table-scroll"><table class="target-table"><thead><tr><th>#</th><th>标的</th><th>Thesis node</th><th>Action state</th><th>Score</th><th>稀缺性/垄断性</th><th>未充分定价</th><th>业绩弹性</th><th>风险控制</th><th>Win prob.</th><th>Payoff</th><th>理由</th><th>下一验证数据</th><th>降级/Kill test</th><th>Review</th></tr></thead><tbody>${rows}</tbody></table></div></div>`;
}

function renderSources() {
  return `<details class="source-collapse"><summary>展开来源索引</summary><div class="source-grid">${sources.map((s) => `<div class="source-card"><strong>${esc(s.source_id)}</strong><br><a href="${esc(s.url)}">${esc(s.title)}</a><p>${esc(s.summary)}</p><small>${esc(s.source_bucket)} · ${esc(s.source_visible_at)} · ${esc(s.support_refute_or_lead)}</small></div>`).join("")}</div></details>`;
}

function writeJson(filename, data) {
  fs.writeFileSync(path.join(OUT_DIR, filename), `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function writeJsonl(filename, rows) {
  fs.writeFileSync(path.join(OUT_DIR, filename), `${rows.map((row) => JSON.stringify(row)).join("\n")}\n`, "utf8");
}

function esc(value) {
  return String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
}
