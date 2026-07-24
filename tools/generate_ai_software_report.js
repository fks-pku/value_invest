const fs = require("fs");
const path = require("path");

const generatedAt = "2026-05-29T00:00:00+08:00";
const base = path.join("research", "bom", "ai_software_opportunities");
fs.mkdirSync(base, { recursive: true });

const framework = {
  project_id: "ai_software_opportunities",
  object_type: "industry_theme",
  object_id: "ai_software",
  meta_question:
    "AI 软件方向在 2026-2028 年有哪些值得持续跟踪的投资机会，机会应如何沿需求兑现、价值捕获、反证条件和估值赔率筛选？",
  max_depth: 3,
  created_at: generatedAt,
  framework: "research_goal_qa",
  research_type: "industry/theme opportunity",
  boundary: "研究观察清单，不构成买卖建议。"
};

const source = {
  gartnerSpend:
    "https://www.gartner.com/en/newsroom/press-releases/2026-05-19-gartner-forecasts-worldwide-ai-spending-to-grow-47-percent-in-2026",
  gartnerCancel:
    "https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027",
  gartnerGovernance:
    "https://www.gartner.com/en/newsroom/press-releases/2026-05-26-gartner-says-applying-uniform-governance-across-ai-agents-will-lead-to-enterprise-ai-agent-failure",
  menlo:
    "https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/",
  msft:
    "https://www.microsoft.com/en-us/investor/earnings/FY-2026-Q3/press-release-webcast",
  msftPerformance:
    "https://www.microsoft.com/en-us/investor/earnings/fy-2026-q3/performance",
  crm:
    "https://investor.salesforce.com/news/news-details/2026/Salesforce-Delivers-Record-First-Quarter-Fiscal-2027-Results/default.aspx",
  now:
    "https://investor.servicenow.com/news/news-details/2026/ServiceNow-Reports-First-Quarter-2026-Financial-Results/default.aspx",
  pltrSec:
    "https://www.sec.gov/Archives/edgar/data/1321655/000132165526000026/a2026q1ex991pressrelease.htm",
  snowSec:
    "https://www.sec.gov/Archives/edgar/data/1640147/000164014726000027/fy2027q1earnings.htm",
  ddog:
    "https://investors.datadoghq.com/news-releases/news-release-details/datadog-announces-first-quarter-2026-financial-results/",
  ddogAi:
    "https://www.datadoghq.com/about/latest-news/press-releases/datadog-state-of-ai-engineering-report-2026/",
  crwd:
    "https://ir.crowdstrike.com/news-releases/news-release-details/crowdstrike-reports-fourth-quarter-and-fiscal-year-2026/",
  adbeSec:
    "https://www.sec.gov/Archives/edgar/data/796343/000079634326000048/adbeex991q126.htm",
  msftStats:
    "https://stockanalysis.com/stocks/msft/statistics/",
  crmStats:
    "https://stockanalysis.com/stocks/crm/statistics/",
  pltrRatios:
    "https://stockanalysis.com/stocks/pltr/financials/ratios/",
  nowRatios:
    "https://stockanalysis.com/stocks/now/financials/ratios/",
  snowRatios:
    "https://stockanalysis.com/stocks/snow/financials/ratios/",
  ddogRatios:
    "https://stockanalysis.com/stocks/ddog/financials/ratios/",
  crwdStats:
    "https://stockanalysis.com/stocks/crwd/statistics/"
};

const evidence = [
  {
    id: "ev_ai_sw_gartner_spending_20260519",
    research_object: "AI software",
    information_category: "research_report",
    source_type: "industry forecast",
    source_name: "Gartner",
    published_at: "2026-05-19",
    fetched_at: generatedAt,
    reliability: "high for market sizing; medium for forecasts",
    support_refute_or_lead: "support",
    materiality: "high",
    tickers: [],
    themes: ["AI software TAM", "AI cybersecurity", "AI models", "agentic workflows"],
    sectors: ["software", "cloud", "cybersecurity"],
    summary:
      "Gartner forecasts worldwide AI spending of $2.595T in 2026, up 47% YoY. AI Software is forecast at $453.209B in 2026 and $638.431B in 2027; AI Cybersecurity at $51.347B in 2026 and $85.997B in 2027; AI Models at $32.604B in 2026 and $59.161B in 2027. Gartner says enterprises are expanding embedded GenAI and agent workflows, but near-term use remains tactical efficiency rather than broad transformation.",
    used_in: ["q1_1_1_market_spend", "q2_1_3_security", "q3_1_1_governance_roi"],
    url: source.gartnerSpend
  },
  {
    id: "ev_ai_sw_menlo_enterprise_ai_2025",
    research_object: "AI software",
    information_category: "research_report",
    source_type: "survey and bottoms-up market model",
    source_name: "Menlo Ventures",
    published_at: "2025-12-09",
    fetched_at: generatedAt,
    reliability: "medium; useful for demand map, but venture report incentives require caution",
    support_refute_or_lead: "support",
    materiality: "high",
    tickers: [],
    themes: ["enterprise AI apps", "application layer", "startups", "coding", "departmental AI"],
    sectors: ["software"],
    summary:
      "Menlo estimates enterprise generative AI spending reached $37B in 2025, up 3.2x from 2024, with $19B going to user-facing products/software. It frames enterprise AI as one of the fastest-scaling software categories and highlights applications, coding, sales, support, HR, and vertical tools.",
    used_in: ["q1_1_1_market_spend", "q2_1_4_creative_vertical"],
    url: source.menlo
  },
  {
    id: "ev_ai_sw_msft_fy26q3_ai_cloud",
    research_object: "Microsoft",
    information_category: "evidence",
    source_type: "company earnings release",
    source_name: "Microsoft FY26 Q3 earnings",
    published_at: "2026-04-29",
    fetched_at: generatedAt,
    reliability: "high",
    support_refute_or_lead: "support",
    materiality: "high",
    tickers: ["MSFT"],
    themes: ["AI run-rate", "cloud", "Copilot", "agentic systems"],
    sectors: ["software", "cloud"],
    summary:
      "Microsoft reported FY26 Q3 revenue of $82.9B, up 18%, Microsoft Cloud revenue of $54.5B, up 29%, and AI business annual revenue run-rate above $37B, up 123% YoY. This is the strongest public incumbent evidence that AI software/cloud is already monetizing at scale.",
    used_in: ["q1_1_2_public_company_signals", "q2_1_1_suite_workflow", "q3_1_2_cost_margin", "q4_1_1_core_tracks"],
    url: source.msft
  },
  {
    id: "ev_ai_sw_msft_fy26q3_margin_pressure",
    research_object: "Microsoft",
    information_category: "evidence",
    source_type: "company performance discussion",
    source_name: "Microsoft FY26 Q3 performance",
    published_at: "2026-04-29",
    fetched_at: generatedAt,
    reliability: "high",
    support_refute_or_lead: "refute",
    materiality: "medium",
    tickers: ["MSFT"],
    themes: ["AI infrastructure cost", "gross margin", "Copilot usage"],
    sectors: ["software", "cloud"],
    summary:
      "Microsoft said gross margin percentage decreased because of continued investments in AI infrastructure and growing AI product usage, partly offset by cloud efficiency gains. This is an important reminder that AI software revenue can carry infrastructure drag.",
    used_in: ["q3_1_2_cost_margin"],
    url: source.msftPerformance
  },
  {
    id: "ev_ai_sw_crm_fy27q1_agentforce",
    research_object: "Salesforce",
    information_category: "evidence",
    source_type: "company earnings release",
    source_name: "Salesforce FY27 Q1 earnings",
    published_at: "2026-05-27",
    fetched_at: generatedAt,
    reliability: "high",
    support_refute_or_lead: "support",
    materiality: "high",
    tickers: ["CRM"],
    themes: ["Agentforce", "Data 360", "AI CRM", "agentic work units"],
    sectors: ["software"],
    summary:
      "Salesforce reported FY27 Q1 revenue of $11.1B, up 13%. Agentforce and Data 360 ARR reached nearly $3.4B, up over 200% YoY, including $1.2B Agentforce ARR, up 205% YoY, and 3.8B Agentic Work Units delivered.",
    used_in: ["q1_1_2_public_company_signals", "q2_1_1_suite_workflow", "q4_1_2_high_beta_tracks"],
    url: source.crm
  },
  {
    id: "ev_ai_sw_now_q1_2026_control_tower",
    research_object: "ServiceNow",
    information_category: "evidence",
    source_type: "company earnings release",
    source_name: "ServiceNow Q1 2026 earnings",
    published_at: "2026-04-22",
    fetched_at: generatedAt,
    reliability: "high",
    support_refute_or_lead: "support",
    materiality: "high",
    tickers: ["NOW"],
    themes: ["workflow automation", "AI control tower", "Now Assist", "cRPO"],
    sectors: ["software"],
    summary:
      "ServiceNow reported Q1 2026 subscription revenue of $3.671B, up 22%, cRPO of $12.64B, up 22.5%, and Now Assist customers spending over $1M ACV grew over 130% YoY.",
    used_in: ["q1_1_2_public_company_signals", "q2_1_1_suite_workflow", "q4_1_1_core_tracks"],
    url: source.now
  },
  {
    id: "ev_ai_sw_pltr_q1_2026_aip",
    research_object: "Palantir",
    information_category: "evidence",
    source_type: "SEC-filed earnings release",
    source_name: "Palantir Q1 2026 results",
    published_at: "2026-05-04",
    fetched_at: generatedAt,
    reliability: "high",
    support_refute_or_lead: "support",
    materiality: "high",
    tickers: ["PLTR"],
    themes: ["AI platform", "ontology", "US commercial", "Rule of 40"],
    sectors: ["software", "defense technology"],
    summary:
      "Palantir reported Q1 2026 revenue of $1.633B, up 85% YoY; U.S. commercial revenue of $595M, up 133%; and a Rule of 40 score of 145%. This is high-quality evidence that AI-native operational software can combine growth and profitability.",
    used_in: ["q1_1_2_public_company_signals", "q2_1_1_suite_workflow", "q4_1_1_core_tracks"],
    url: source.pltrSec
  },
  {
    id: "ev_ai_sw_snow_fy27q1_data_cloud",
    research_object: "Snowflake",
    information_category: "evidence",
    source_type: "SEC-filed earnings release",
    source_name: "Snowflake FY27 Q1 results",
    published_at: "2026-05-27",
    fetched_at: generatedAt,
    reliability: "high",
    support_refute_or_lead: "support",
    materiality: "high",
    tickers: ["SNOW"],
    themes: ["AI data cloud", "Cortex", "data platform", "RPO"],
    sectors: ["software"],
    summary:
      "Snowflake reported FY27 Q1 product revenue of $1.334B, up 34%, and RPO of $9.21B, up 38%. Public company materials and related earnings coverage indicate rising adoption of Snowflake AI/Cortex capabilities, making the data layer a key AI software control point.",
    used_in: ["q1_1_2_public_company_signals", "q2_1_2_data_observability", "q4_1_2_high_beta_tracks"],
    url: source.snowSec
  },
  {
    id: "ev_ai_sw_ddog_q1_2026_observability",
    research_object: "Datadog",
    information_category: "evidence",
    source_type: "company earnings release",
    source_name: "Datadog Q1 2026 earnings",
    published_at: "2026-05-07",
    fetched_at: generatedAt,
    reliability: "high",
    support_refute_or_lead: "support",
    materiality: "medium",
    tickers: ["DDOG"],
    themes: ["observability", "LLM operations", "GPU monitoring", "MCP Server"],
    sectors: ["software", "cloud infrastructure"],
    summary:
      "Datadog reported Q1 2026 revenue of $1.006B, up 32%, and launched MCP Server, Bits AI Security Agent, GPU Monitoring, and Experiments for general availability. This supports the thesis that production AI creates new observability and governance budgets.",
    used_in: ["q2_1_2_data_observability", "q3_1_2_cost_margin", "q4_1_2_high_beta_tracks"],
    url: source.ddog
  },
  {
    id: "ev_ai_sw_ddog_state_ai_engineering_2026",
    research_object: "AI operations",
    information_category: "research_report",
    source_type: "company telemetry report",
    source_name: "Datadog State of AI Engineering 2026",
    published_at: "2026-04-21",
    fetched_at: generatedAt,
    reliability: "medium; strong telemetry but vendor-incentivized framing",
    support_refute_or_lead: "support",
    materiality: "medium",
    tickers: ["DDOG"],
    themes: ["AI operations", "model request failures", "capacity limits", "LLM observability"],
    sectors: ["software", "cloud infrastructure"],
    summary:
      "Datadog reported that around 5% of AI model requests fail in production and nearly 60% of failures are caused by capacity limits. This strengthens the case for observability, routing, reliability, and governance software around AI systems.",
    used_in: ["q2_1_2_data_observability", "q3_1_1_governance_roi"],
    url: source.ddogAi
  },
  {
    id: "ev_ai_sw_crwd_fy26q4_ai_security",
    research_object: "CrowdStrike",
    information_category: "evidence",
    source_type: "company earnings release",
    source_name: "CrowdStrike FY26 Q4 results",
    published_at: "2026-03-03",
    fetched_at: generatedAt,
    reliability: "high",
    support_refute_or_lead: "support",
    materiality: "medium",
    tickers: ["CRWD"],
    themes: ["AI security", "Falcon Flex", "agent security", "ARR"],
    sectors: ["cybersecurity", "software"],
    summary:
      "CrowdStrike reported FY26 total revenue of $4.812B, up 22%, ending ARR above $5.25B, record Q4 net new ARR of $331M, and Falcon Flex ARR of $1.69B, up over 120% YoY. It frames AI as a new security surface from GPU to agent to prompt.",
    used_in: ["q2_1_3_security", "q4_1_2_high_beta_tracks"],
    url: source.crwd
  },
  {
    id: "ev_ai_sw_adbe_q1_2026_creative",
    research_object: "Adobe",
    information_category: "evidence",
    source_type: "SEC-filed earnings release",
    source_name: "Adobe Q1 FY2026 results",
    published_at: "2026-03-12",
    fetched_at: generatedAt,
    reliability: "high",
    support_refute_or_lead: "lead",
    materiality: "medium",
    tickers: ["ADBE"],
    themes: ["creative AI", "Firefly", "AI-first ARR", "subscription resilience"],
    sectors: ["software"],
    summary:
      "Adobe reported record Q1 FY2026 revenue of $6.40B, up 12%, subscription revenue growth of 13%, and AI-first ARR more than tripling YoY. This is evidence of AI monetization in creative workflows, but competitive disruption risk remains central.",
    used_in: ["q2_1_4_creative_vertical", "q4_1_2_high_beta_tracks"],
    url: source.adbeSec
  },
  {
    id: "ev_ai_sw_gartner_agentic_cancel_20250625",
    research_object: "agentic AI",
    information_category: "research_report",
    source_type: "industry forecast",
    source_name: "Gartner",
    published_at: "2025-06-25",
    fetched_at: generatedAt,
    reliability: "medium",
    support_refute_or_lead: "refute",
    materiality: "high",
    tickers: [],
    themes: ["agentic AI risk", "ROI", "governance", "project cancellation"],
    sectors: ["software"],
    summary:
      "Gartner predicts over 40% of agentic AI projects will be canceled by the end of 2027 due to escalating costs, unclear business value, or inadequate risk controls. This is the main top-down refutation risk for broad AI-agent software enthusiasm.",
    used_in: ["q3_1_1_governance_roi"],
    url: source.gartnerCancel
  },
  {
    id: "ev_ai_sw_gartner_agent_governance_20260526",
    research_object: "agentic AI governance",
    information_category: "research_report",
    source_type: "industry forecast",
    source_name: "Gartner",
    published_at: "2026-05-26",
    fetched_at: generatedAt,
    reliability: "medium",
    support_refute_or_lead: "refute",
    materiality: "medium",
    tickers: [],
    themes: ["AI agent governance", "production incident", "demotion/decommission"],
    sectors: ["software"],
    summary:
      "Gartner says applying uniform governance across agents can cause enterprise AI-agent failure and predicts that by 2027, 40% of enterprises will demote or decommission autonomous agents due to governance gaps identified after production incidents.",
    used_in: ["q3_1_1_governance_roi", "q2_1_3_security"],
    url: source.gartnerGovernance
  },
  {
    id: "ev_ai_sw_valuation_snapshot_stockanalysis_20260528",
    research_object: "AI software public equities",
    information_category: "message",
    source_type: "third-party market data snapshot",
    source_name: "StockAnalysis",
    published_at: "2026-05-27",
    fetched_at: generatedAt,
    reliability: "medium; current market data, not primary financial source",
    support_refute_or_lead: "lead",
    materiality: "high",
    tickers: ["MSFT", "CRM", "NOW", "PLTR", "SNOW", "DDOG", "CRWD"],
    themes: ["valuation", "priced-in expectations", "multiples"],
    sectors: ["software"],
    summary:
      "Valuation snapshots show a wide odds spread: MSFT around 24.6x trailing PE and 9.8x EV/Sales; CRM around 23x trailing PE and 3.7x P/S; PLTR around 62x EV/Sales; NOW around 6.5x EV/Sales in the available split-adjusted snapshot; SNOW around 12x P/S; DDOG around 20x P/S; CRWD around 26.6x P/S in one snapshot and higher in later price data. These numbers are leads for valuation work, not final fair-value estimates.",
    used_in: ["q3_1_3_valuation", "q4_1_1_core_tracks", "q4_1_2_high_beta_tracks"],
    url: source.msftStats
  }
];

const skillTrace = [
  {
    task_family: "research type adaptation",
    selected_skill: "value-invest-research",
    status: "used",
    output:
      "将本题分类为 industry/theme opportunity，Q1-Q4 映射为需求真实度、价值捕获瓶颈、反证与赔率、标的观察清单。"
  },
  {
    task_family: "financial statement / earnings parsing",
    selected_skill: "financial-statement-analysis",
    status: "used as protocol",
    output:
      "对公司财报/公告中的 revenue、ARR、RPO/cRPO、gross margin、FCF、Rule of 40 等字段做事实化摘录；未输出买卖建议。"
  },
  {
    task_family: "valuation / priced-in expectations",
    selected_skill: "valuation-analysis",
    status: "used as protocol",
    output:
      "把市场倍数快照降级为 lead，区分基本面强度与赔率强度；没有从倍数直接推出目标价。"
  },
  {
    task_family: "long source reading / L3 draft",
    selected_skill: "leaf-research-deepseek + deepseek_delegate",
    status: "attempted fallback",
    output:
      "本轮曾尝试让 DeepSeek 对 Q2 价值捕获做初稿，但工具返回空响应；最终 L3 答案由 GPT 基于可审计来源核验后完成，并在节点中记录 fallback。"
  },
  {
    task_family: "HTML/report interface",
    selected_skill: "frontend-design",
    status: "used as protocol",
    output:
      "HTML 使用轻量、低噪声、Apple-inspired 的研究页样式，所有表格和评分卡嵌在所属 QA 节点内。"
  }
];

function dispatch(taskFamily, selectedSkill, materials, schema, status = "used", fallback = "none") {
  return {
    task_family: taskFamily,
    selected_skill: selectedSkill,
    concrete_materials: materials,
    extraction_schema: schema,
    skill_output_status: status,
    fallback_used: fallback,
    gpt_verification_status:
      "verified against source links and downgraded unsupported or third-party market data to lead where appropriate"
  };
}

const nodes = [
  {
    id: "l0_goal",
    layer: "L0",
    title: "当前研究目标",
    question:
      "AI 软件方向在 2026-2028 年是否存在可持续的投资机会，哪些标的值得进入观察清单？",
    answer_summary:
      "当前判断：AI 软件不是单一主题，而是从模型、应用、数据、工作流、可观测性和安全治理向外扩散的预算迁移。机会存在，但应该优先跟踪能把 AI 用量转成可审计 ARR/RPO/现金流的公司；最大不确定性是企业 agent 项目的 ROI、治理事故和估值预期是否会让高倍数标的先于基本面回撤。",
    evidence_ids: ["ev_ai_sw_gartner_spending_20260519", "ev_ai_sw_menlo_enterprise_ai_2025"],
    next_question_ids: ["q1_demand", "q2_capture", "q3_risk", "q4_targets"]
  },
  {
    id: "q1_demand",
    layer: "Q1",
    title: "需求真实度",
    question: "Q1 需求：AI 软件需求是否已经从试点进入生产和预算？",
    answer_summary:
      "需求端的证据比 2024-2025 年更硬：Gartner/Menlo 的市场规模扩张是一层，Microsoft、Salesforce、ServiceNow、Palantir、Snowflake 等公司的 ARR/RPO/收入兑现是另一层。但需求仍分层：嵌入式 AI、工作流平台和数据/安全治理更像企业预算；纯粹 agent 项目仍可能卡在 ROI 和治理。",
    evidence_ids: [
      "ev_ai_sw_gartner_spending_20260519",
      "ev_ai_sw_menlo_enterprise_ai_2025",
      "ev_ai_sw_msft_fy26q3_ai_cloud",
      "ev_ai_sw_crm_fy27q1_agentforce",
      "ev_ai_sw_now_q1_2026_control_tower",
      "ev_ai_sw_pltr_q1_2026_aip",
      "ev_ai_sw_snow_fy27q1_data_cloud"
    ],
    next_question_ids: ["q1_1_budget_production"]
  },
  {
    id: "q1_1_budget_production",
    layer: "Q1.1",
    title: "预算与生产化",
    question: "Q1.1 哪些证据能证明企业已经把 AI 软件放进预算，而不是只做 PoC？",
    answer_summary:
      "最强证据不是宣传，而是三类数字：市场支出从应用层扩张，公司层面的 ARR/RPO/cRPO 增长，以及 AI 功能和基础产品之间的交叉销售。当前证据支持“预算迁移已经开始”，但不支持所有 AI 软件公司都能涨价或保利润。",
    evidence_ids: [
      "ev_ai_sw_gartner_spending_20260519",
      "ev_ai_sw_menlo_enterprise_ai_2025",
      "ev_ai_sw_msft_fy26q3_ai_cloud",
      "ev_ai_sw_crm_fy27q1_agentforce",
      "ev_ai_sw_now_q1_2026_control_tower",
      "ev_ai_sw_pltr_q1_2026_aip",
      "ev_ai_sw_snow_fy27q1_data_cloud"
    ],
    next_question_ids: ["q1_1_1_market_spend", "q1_1_2_public_company_signals"]
  },
  {
    id: "q1_1_1_market_spend",
    layer: "Q1.1.1",
    title: "市场规模证据",
    question: "Q1.1.1 第三方市场规模和企业调查是否支持 AI 软件预算扩张？",
    fact:
      "Gartner 预计 2026 年全球 AI 支出为 2.595 万亿美元，同比 47%；其中 AI Software 为 4532.09 亿美元，AI Cybersecurity 为 513.47 亿美元，AI Models 为 326.04 亿美元。Menlo 估算 2025 年企业生成式 AI 支出达到 370 亿美元，其中约 190 亿美元流向应用层。",
    inference:
      "AI 软件需求已不只是模型 API，应用层、嵌入式软件、数据层和安全治理都在吸收预算。Gartner 还强调企业短期更偏战术效率，这意味着能嵌入既有工作流、证明节省时间/成本的产品更容易成交。",
    judgment:
      "支持需求真实存在，但市场规模预测不能直接等同于个股收入。真正能上调观察强度的，是公司级 ARR、RPO、客户数和现金流同步兑现。",
    gap:
      "需要进一步拆分 AI Software 中应用、平台、安全、模型和服务的收入归属，并跟踪企业软件预算是否从传统 SaaS 转移而非增量扩张。",
    trigger:
      "若 Gartner/Menlo 后续报告继续上修应用层与安全治理支出，同时上市公司 AI ARR/RPO 同步提速，则 Q1 需求强度上调；若应用层支出被模型/API 或内部自建吸收，则下调。",
    evidence_ids: ["ev_ai_sw_gartner_spending_20260519", "ev_ai_sw_menlo_enterprise_ai_2025"],
    next_question_ids: [],
    dispatch: dispatch(
      "long source reading / market sizing",
      "leaf-research-deepseek plus GPT fallback",
      ["Gartner AI Spending forecast", "Menlo State of Generative AI in the Enterprise"],
      "extract market size, category split, time frame, support/refute stance",
      "deepseek empty; GPT final",
      "GPT source parsing"
    )
  },
  {
    id: "q1_1_2_public_company_signals",
    layer: "Q1.1.1",
    title: "公司兑现证据",
    question: "Q1.1.2 上市公司是否已经把 AI 软件需求转成收入、ARR、RPO 或客户扩张？",
    fact:
      "Microsoft AI business ARR 超过 370 亿美元、同比 123%；Salesforce Agentforce ARR 达 12 亿美元、同比 205%，Agentforce+Data 360 ARR 接近 34 亿美元；ServiceNow 订阅收入同比 22%、cRPO 同比 22.5%，Now Assist 百万美元 ACV 客户同比增超 130%；Palantir Q1 收入同比 85%、美国商业收入同比 133%；Snowflake 产品收入同比 34%、RPO 同比 38%。",
    inference:
      "需求从 PoC 走向生产的路径不是单点模型，而是嵌入在云、CRM、ITSM、数据云、运营系统中的 AI 功能。最有价值的证据来自续约/扩张型指标，而不是 token 用量或用户试用。",
    judgment:
      "支持“AI 软件需求已进入企业预算”的判断。强度最高的是 Microsoft、ServiceNow、Palantir，因为它们同时披露了规模、续约/订单或利润质量；Salesforce 和 Snowflake 需要继续看 AI ARR 是否带动整体 organic growth 与毛利。",
    gap:
      "不同公司对 AI ARR、AI revenue run-rate、agent work unit 的定义不同，可比性弱。需要把 AI 直接收入与核心业务增长拆开。",
    trigger:
      "下一季若 AI ARR/RPO 增速不再只是小基数，而能持续拉动整体订阅收入和现金流，需求判断继续增强；若 AI 指标高增但总收入不加速，则降为产品升级线索。",
    evidence_ids: [
      "ev_ai_sw_msft_fy26q3_ai_cloud",
      "ev_ai_sw_crm_fy27q1_agentforce",
      "ev_ai_sw_now_q1_2026_control_tower",
      "ev_ai_sw_pltr_q1_2026_aip",
      "ev_ai_sw_snow_fy27q1_data_cloud"
    ],
    next_question_ids: [],
    dispatch: dispatch(
      "financial statement / earnings parsing",
      "financial-statement-analysis",
      ["Microsoft FY26 Q3", "Salesforce FY27 Q1", "ServiceNow Q1 2026", "Palantir Q1 2026", "Snowflake FY27 Q1"],
      "extract revenue, ARR, RPO/cRPO, growth, margin/FCF quality, AI-specific metrics",
      "used as protocol",
      "none"
    )
  },
  {
    id: "q2_capture",
    layer: "Q2",
    title: "价值捕获瓶颈",
    question: "Q2 瓶颈：AI 软件价值会被哪些环节捕获？",
    answer_summary:
      "价值捕获不平均。当前最值得跟踪的利润池是：企业套件/工作流中的 AI 增购、AI-native 运营平台、数据云/语义层/可观测性、安全治理。模型 API 和通用助手增长快，但在公开市场上可投资暴露不完整，且利润可能被算力成本和价格竞争稀释。",
    evidence_ids: [
      "ev_ai_sw_msft_fy26q3_ai_cloud",
      "ev_ai_sw_crm_fy27q1_agentforce",
      "ev_ai_sw_now_q1_2026_control_tower",
      "ev_ai_sw_pltr_q1_2026_aip",
      "ev_ai_sw_snow_fy27q1_data_cloud",
      "ev_ai_sw_ddog_q1_2026_observability",
      "ev_ai_sw_crwd_fy26q4_ai_security",
      "ev_ai_sw_adbe_q1_2026_creative"
    ],
    next_question_ids: ["q2_1_nodes"]
  },
  {
    id: "q2_1_nodes",
    layer: "Q2.1",
    title: "利润池节点",
    question: "Q2.1 哪些 AI 软件节点有瓶颈属性、议价权和财务兑现？",
    answer_summary:
      "工作流系统拥有客户入口和权限边界；数据/可观测性系统拥有生产化后的运行事实；安全系统拥有风险预算；创意/垂直应用拥有专业工作流，但也最容易被模型能力和新入口冲击。评分上，工作流/运营系统与安全治理更稳，数据/可观测性更弹性，创意/垂直应用需要证明 AI 不侵蚀原有席位。",
    evidence_ids: [
      "ev_ai_sw_msft_fy26q3_ai_cloud",
      "ev_ai_sw_now_q1_2026_control_tower",
      "ev_ai_sw_pltr_q1_2026_aip",
      "ev_ai_sw_snow_fy27q1_data_cloud",
      "ev_ai_sw_ddog_q1_2026_observability",
      "ev_ai_sw_crwd_fy26q4_ai_security",
      "ev_ai_sw_adbe_q1_2026_creative"
    ],
    next_question_ids: [
      "q2_1_1_suite_workflow",
      "q2_1_2_data_observability",
      "q2_1_3_security",
      "q2_1_4_creative_vertical"
    ],
    scorecard: [
      ["企业套件/工作流", "MSFT, NOW, CRM, PLTR", "高", "入口、权限、流程、数据上下文", "AI 指标需转成核心订阅加速"],
      ["数据云/可观测性", "SNOW, DDOG", "中高", "生产 AI 离不开数据与运行状态", "消费模式波动、成本和竞争"],
      ["安全/治理", "CRWD, PANW, DDOG", "中高", "AI agent 扩大攻击面和合规需求", "预算优先级与平台竞争"],
      ["创意/垂直应用", "ADBE, INTU, DUOL, vertical SaaS", "中", "专业工作流和专有数据", "模型替代、价格压力、席位收缩"]
    ]
  },
  {
    id: "q2_1_1_suite_workflow",
    layer: "Q2.1.1",
    title: "套件与工作流平台",
    question: "Q2.1.1 企业套件和工作流平台为什么最容易捕获 AI 软件价值？",
    fact:
      "Microsoft、Salesforce、ServiceNow 和 Palantir 都披露了 AI 相关收入、ARR、cRPO 或高速增长。它们的共同点是 AI 不是孤立产品，而是嵌在 Office、CRM、ITSM、企业运营和数据本体工作流中。",
    inference:
      "企业愿意为“能在现有权限、数据和流程里完成任务”的 AI 付费，而不是为一个独立聊天入口长期付费。工作流平台越接近业务动作，越能把模型能力转化为可审计结果。",
    judgment:
      "这是 AI 软件公开市场里确定性最高的价值捕获层。MSFT 和 NOW 偏稳健，PLTR 偏高弹性，CRM 处在 Agentforce 能否带动整体增长再加速的验证期。",
    gap:
      "AI SKU 的净新增贡献、续约率、折扣率和毛利仍披露不足。尤其要确认 AI 用量是否拉高基础设施成本。",
    trigger:
      "观察 AI ARR/RPO 占比、核心订阅增速、客户扩张和毛利率。若 AI 高增长同时核心收入加速且毛利稳定，则上调。",
    evidence_ids: [
      "ev_ai_sw_msft_fy26q3_ai_cloud",
      "ev_ai_sw_crm_fy27q1_agentforce",
      "ev_ai_sw_now_q1_2026_control_tower",
      "ev_ai_sw_pltr_q1_2026_aip"
    ],
    next_question_ids: [],
    dispatch: dispatch(
      "financial statement / earnings parsing",
      "financial-statement-analysis",
      ["MSFT, CRM, NOW, PLTR earnings releases"],
      "extract AI monetization metric, subscription/RPO proxy, margin quality, follow-up triggers",
      "used as protocol",
      "none"
    )
  },
  {
    id: "q2_1_2_data_observability",
    layer: "Q2.1.1",
    title: "数据云与可观测性",
    question: "Q2.1.2 数据云、可观测性和 AI 运维为什么是生产化瓶颈？",
    fact:
      "Snowflake FY27 Q1 产品收入同比 34%、RPO 同比 38%；Datadog Q1 2026 收入同比 32%，同时推出 MCP Server、Bits AI Security Agent、GPU Monitoring 等产品。Datadog State of AI Engineering 指出约 5% 生产 AI 请求失败，近 60% 失败来自容量限制。",
    inference:
      "当 AI 从 demo 进入生产，企业问题从“模型能不能回答”变成“数据是否可用、调用是否稳定、成本是否可控、失败能否追踪”。因此数据治理、语义层、observability、LLM ops、GPU/agent monitoring 会成为第二波软件预算。",
    judgment:
      "数据/可观测性是弹性很高的中游控制点，但公司层面的利润质量差异大。SNOW 需要证明 AI 用量带来耐久消费，DDOG 需要证明新 AI 运维产品能扩大客户钱包而非只是功能补齐。",
    gap:
      "缺少 AI 工作负载在 SNOW/DDOG 收入中的直接占比；消费型模式在宏观压力下可能被优化。",
    trigger:
      "SNOW NRR、RPO、AI accounts 和 product revenue 同步上行，DDOG 大客户 ARR 和多产品采用率上行，则 Q2.1.2 强度上调。",
    evidence_ids: [
      "ev_ai_sw_snow_fy27q1_data_cloud",
      "ev_ai_sw_ddog_q1_2026_observability",
      "ev_ai_sw_ddog_state_ai_engineering_2026"
    ],
    next_question_ids: [],
    dispatch: dispatch(
      "long source reading / financial statement parsing",
      "financial-statement-analysis plus leaf-research-deepseek fallback",
      ["Snowflake FY27 Q1 earnings", "Datadog Q1 2026 earnings", "Datadog State of AI Engineering"],
      "extract product revenue, RPO, AI adoption, failure-rate evidence, affected thesis node",
      "used as protocol",
      "GPT source parsing"
    )
  },
  {
    id: "q2_1_3_security",
    layer: "Q2.1.1",
    title: "AI 安全与治理",
    question: "Q2.1.3 AI agent 会不会创造新的安全/治理软件预算？",
    fact:
      "Gartner 将 AI Cybersecurity 2026 支出预测为 513.47 亿美元，2027 年 859.97 亿美元。CrowdStrike FY26 结束 ARR 超过 52.5 亿美元，Falcon Flex ARR 16.9 亿美元、同比超 120%，并把 AI 风险描述为从 GPU、agent 到 prompt 的新攻击面。Gartner 同时警告统一治理会导致 agent 失败。",
    inference:
      "agent 增加了非人身份、工具调用、权限继承、prompt/agent interaction layer 和数据外泄风险。安全预算往往比生产力预算更刚性，因此 AI 治理、安全检测、身份和权限控制可能成为确定性较强的软件层。",
    judgment:
      "支持把 AI 安全/治理列为重点利润池。CRWD 是强相关标的，但估值拥挤；PANW、DDOG、MSFT Security 也应纳入横向比较。",
    gap:
      "AI 安全产品收入拆分仍少，当前更多是平台叙事和模块扩张，需看客户是否为 AI-specific module 单独付费。",
    trigger:
      "若 CRWD/PANW/MSFT 披露 AI security 模块 ARR、attach rate 或大客户扩张，安全节点上调；若治理事故导致项目收缩但安全预算未增，则下调。",
    evidence_ids: [
      "ev_ai_sw_gartner_spending_20260519",
      "ev_ai_sw_gartner_agent_governance_20260526",
      "ev_ai_sw_crwd_fy26q4_ai_security"
    ],
    next_question_ids: [],
    dispatch: dispatch(
      "long source reading / security thesis extraction",
      "leaf-research-deepseek plus GPT fallback",
      ["Gartner AI spending", "Gartner agent governance", "CrowdStrike FY26 Q4"],
      "extract security spend, AI-agent attack surface, ARR/module evidence, refute triggers",
      "deepseek empty; GPT final",
      "GPT source parsing"
    )
  },
  {
    id: "q2_1_4_creative_vertical",
    layer: "Q2.1.1",
    title: "创意与垂直应用",
    question: "Q2.1.4 创意/垂直应用是机会还是被 AI 侵蚀的对象？",
    fact:
      "Adobe Q1 FY2026 收入 64.0 亿美元，同比 12%，订阅收入同比 13%，AI-first ARR 同比超过三倍。Menlo 指出企业 AI 应用支出已扩展到 coding、sales、support、HR、healthcare、legal、creator tools 等多个函数和垂直场景。",
    inference:
      "创意和垂直应用具备专业工作流、模板、资产、合规和客户关系，但模型能力提升可能削弱传统席位价值。最优路径是 AI 增加使用量和新 SKU，而不是把既有订阅价格打穿。",
    judgment:
      "ADBE 是验证型观察，不是当前最强主线。垂直 AI 应用的公开标的分散，更多机会可能在私有公司或被大平台收购/嵌入。",
    gap:
      "缺少 AI-first ARR 的绝对规模、毛利影响、对总 ARR 的贡献和 churn 变化。",
    trigger:
      "若 Adobe AI-first ARR 继续高增且总 ARR 增速稳定/上行，创意应用节点升档；若订阅增长放缓、AI 只增加算力成本，则降档。",
    evidence_ids: ["ev_ai_sw_adbe_q1_2026_creative", "ev_ai_sw_menlo_enterprise_ai_2025"],
    next_question_ids: [],
    dispatch: dispatch(
      "financial statement / application layer reading",
      "financial-statement-analysis",
      ["Adobe Q1 FY2026 earnings", "Menlo enterprise AI report"],
      "extract revenue, subscription growth, AI-first ARR direction, competitive risk",
      "used as protocol",
      "none"
    )
  },
  {
    id: "q3_risk",
    layer: "Q3",
    title: "反证与赔率",
    question: "Q3 风险：哪些因素会证伪 AI 软件机会，当前价格是否已经反映太多？",
    answer_summary:
      "核心风险有三类：agent 项目取消或治理事故、AI 成本压低软件毛利、估值已经提前定价。结论要分开看：基本面强度最高的未必赔率最好；PLTR、CRWD、DDOG 等高弹性标的需要更高的持续超预期才能维持强观察。",
    evidence_ids: [
      "ev_ai_sw_gartner_agentic_cancel_20250625",
      "ev_ai_sw_gartner_agent_governance_20260526",
      "ev_ai_sw_msft_fy26q3_margin_pressure",
      "ev_ai_sw_ddog_state_ai_engineering_2026",
      "ev_ai_sw_valuation_snapshot_stockanalysis_20260528"
    ],
    next_question_ids: ["q3_1_tests"]
  },
  {
    id: "q3_1_tests",
    layer: "Q3.1",
    title: "反证测试",
    question: "Q3.1 哪些触发器会使当前 AI 软件观察强度降级？",
    answer_summary:
      "最重要的红灯不是个别模型发布，而是公司层面出现 AI ARR 高增但总收入不加速、RPO/cRPO 放缓、毛利率持续下行、客户 ROI 无法量化、估值倍数和增长质量不匹配。每个标的都应同时绑定基本面测试与赔率测试。",
    evidence_ids: [
      "ev_ai_sw_gartner_agentic_cancel_20250625",
      "ev_ai_sw_gartner_agent_governance_20260526",
      "ev_ai_sw_msft_fy26q3_margin_pressure",
      "ev_ai_sw_valuation_snapshot_stockanalysis_20260528"
    ],
    next_question_ids: ["q3_1_1_governance_roi", "q3_1_2_cost_margin", "q3_1_3_valuation"],
    risk_tests: [
      ["ROI/治理", "Agent 项目取消率、decommission、生产事故", "项目进入生产且 ROI 可量化", "Gartner 风险兑现，客户推迟部署"],
      ["财务质量", "AI ARR/RPO、总订阅增长、毛利、FCF", "AI 指标带动整体加速", "AI 指标强但收入/毛利/现金流转弱"],
      ["估值赔率", "EV/Sales、P/FCF、forward PE、增长/利润匹配", "高倍数对应持续上修", "倍数高而增速或毛利下修"]
    ]
  },
  {
    id: "q3_1_1_governance_roi",
    layer: "Q3.1.1",
    title: "ROI 与治理反证",
    question: "Q3.1.1 Agent 项目取消、ROI 不清晰和治理事故如何影响 AI 软件需求？",
    fact:
      "Gartner 预计 2027 年底前超过 40% agentic AI 项目会因成本上升、商业价值不清或风险控制不足被取消；另预计 2027 年 40% 企业会因生产事故后发现治理缺口而降级或弃用自主 agent。",
    inference:
      "这不是对所有 AI 软件的否定，而是把机会从“会做 agent 的产品”筛到“能治理、监控、审计、证明 ROI 的平台”。失败率越高，越有利于治理/observability/security，但不利于没有业务闭环的横向 agent 应用。",
    judgment:
      "这是本研究最重要的反证条件。若项目取消率上升但治理预算上升，则 DDOG/CRWD/NOW 反而受益；若取消率导致企业整体 AI 软件预算冻结，则整个主题降级。",
    gap:
      "需要企业实际 deployment、decommission、ROI 案例和预算调查，而不是只依赖预测。",
    trigger:
      "跟踪 Gartner/Forrester/Menlo 后续调查、软件公司客户案例、agent 生产事故、客户延期部署评论。",
    evidence_ids: [
      "ev_ai_sw_gartner_agentic_cancel_20250625",
      "ev_ai_sw_gartner_agent_governance_20260526",
      "ev_ai_sw_ddog_state_ai_engineering_2026"
    ],
    next_question_ids: [],
    dispatch: dispatch(
      "long source reading / disconfirming evidence",
      "leaf-research-deepseek plus GPT fallback",
      ["Gartner cancellation forecast", "Gartner governance release", "Datadog AI Engineering report"],
      "extract refute facts, affected node, follow-up data, support/refute stance",
      "deepseek empty; GPT final",
      "GPT source parsing"
    )
  },
  {
    id: "q3_1_2_cost_margin",
    layer: "Q3.1.1",
    title: "成本与毛利反证",
    question: "Q3.1.2 AI 软件收入会不会被算力成本和用量成本吞掉？",
    fact:
      "Microsoft FY26 Q3 明确提到公司和 Microsoft Cloud 毛利率下降，原因包括 AI infrastructure 投入和 AI product usage 增加。Datadog 报告指出生产 AI 请求失败中容量限制是主要原因之一，说明生产化 AI 有真实基础设施约束。",
    inference:
      "AI 软件的会计质量不能只看 ARR，需要看毛利、capex/云成本、gross margin trend、free cash flow conversion。如果 AI SKU 的价格不能覆盖推理/上下文/可靠性成本，收入增长可能并不等于价值捕获。",
    judgment:
      "对 MSFT 这类高现金流公司是可承受的利润率压力；对高倍数、GAAP 尚未盈利或消费模式公司则是更大风险。",
    gap:
      "多数公司没有披露 AI SKU 毛利和推理成本分摊，当前只能用公司总体毛利、云成本和非 GAAP 调整观察。",
    trigger:
      "若 AI usage 上升伴随毛利持续下降、capex 超预期、FCF 转换下降，则降低相关标的赔率强度。",
    evidence_ids: [
      "ev_ai_sw_msft_fy26q3_margin_pressure",
      "ev_ai_sw_ddog_q1_2026_observability",
      "ev_ai_sw_ddog_state_ai_engineering_2026"
    ],
    next_question_ids: [],
    dispatch: dispatch(
      "financial statement / margin quality",
      "financial-statement-analysis",
      ["Microsoft performance notes", "Datadog earnings and telemetry report"],
      "extract margin pressure, AI infrastructure cost, FCF and capacity-risk signals",
      "used as protocol",
      "none"
    )
  },
  {
    id: "q3_1_3_valuation",
    layer: "Q3.1.1",
    title: "估值与赔率反证",
    question: "Q3.1.3 当前估值是否已经把 AI 软件机会打满？",
    fact:
      "第三方快照显示 MSFT 约 24.6x trailing PE、约 9.8x EV/Sales；CRM 约 23x trailing PE、约 3.7x P/S；PLTR 约 62x EV/Sales；SNOW 约 12x P/S；DDOG 约 20x P/S；CRWD 至少约 26.6x P/S，且后续价格数据更高。NOW 的公开快照受拆股和日期影响，需复核最新一致口径。",
    inference:
      "赔率分层明显：MSFT/CRM 的估值更多反映成熟软件现金流和 AI option；PLTR/CRWD/DDOG 的估值要求持续高增长和利润扩张；SNOW 是 AI 数据云反转定价，但仍需证明 GAAP 盈利和消费耐久性。",
    judgment:
      "主题强不等于所有标的有好赔率。当前应把 PLTR、CRWD、DDOG 归为高基本面/高预期，MSFT/NOW 归为核心观察，CRM/SNOW/ADBE 归为验证型或赔率改善观察。",
    gap:
      "需要统一估值日、股本、净现金、forward estimates 和 AI revenue contribution，最好后续用 valuation-analysis 做 reverse DCF。",
    trigger:
      "若高倍数标的收入/RPO/FCF 连续上修可维持强观察；若一次下修或 AI 指标不再带动总收入，估值反证会很快生效。",
    evidence_ids: ["ev_ai_sw_valuation_snapshot_stockanalysis_20260528"],
    next_question_ids: [],
    dispatch: dispatch(
      "valuation / priced-in expectations",
      "valuation-analysis",
      ["StockAnalysis valuation snapshots for MSFT, CRM, PLTR, NOW, SNOW, DDOG, CRWD"],
      "extract market cap, EV/Sales, PE/forward PE, classify odds strength and required assumption",
      "used as protocol",
      "none"
    )
  },
  {
    id: "q4_targets",
    layer: "Q4",
    title: "标的观察清单",
    question: "Q4 标的：哪些具体证券应进入观察清单，强度、原因和风险是什么？",
    answer_summary:
      "本轮不输出买卖建议，只做观察强度。核心跟踪：MSFT、NOW、PLTR；高优先验证：CRM、SNOW、DDOG、CRWD；创意/垂直验证：ADBE；私有/间接观察：OpenAI、Anthropic、Databricks 等通过云、数据、安全和持股/合作链条观察。",
    evidence_ids: [
      "ev_ai_sw_msft_fy26q3_ai_cloud",
      "ev_ai_sw_now_q1_2026_control_tower",
      "ev_ai_sw_pltr_q1_2026_aip",
      "ev_ai_sw_crm_fy27q1_agentforce",
      "ev_ai_sw_snow_fy27q1_data_cloud",
      "ev_ai_sw_ddog_q1_2026_observability",
      "ev_ai_sw_crwd_fy26q4_ai_security",
      "ev_ai_sw_adbe_q1_2026_creative",
      "ev_ai_sw_valuation_snapshot_stockanalysis_20260528"
    ],
    next_question_ids: ["q4_1_observation_list"]
  },
  {
    id: "q4_1_observation_list",
    layer: "Q4.1",
    title: "观察强度分层",
    question: "Q4.1 如何把结论映射到具体证券和后续验证数据？",
    answer_summary:
      "强度排序不是买入排序，而是研究优先级。核心标准：能否把 AI 变成可审计收入；是否拥有工作流/数据/安全瓶颈；估值是否要求过多未来胜利；下一季有没有明确可验证指标。",
    evidence_ids: [
      "ev_ai_sw_msft_fy26q3_ai_cloud",
      "ev_ai_sw_now_q1_2026_control_tower",
      "ev_ai_sw_pltr_q1_2026_aip",
      "ev_ai_sw_crm_fy27q1_agentforce",
      "ev_ai_sw_snow_fy27q1_data_cloud",
      "ev_ai_sw_ddog_q1_2026_observability",
      "ev_ai_sw_crwd_fy26q4_ai_security",
      "ev_ai_sw_adbe_q1_2026_creative",
      "ev_ai_sw_valuation_snapshot_stockanalysis_20260528"
    ],
    next_question_ids: ["q4_1_1_core_tracks", "q4_1_2_high_beta_tracks"],
    target_table: [
      ["MSFT", "Microsoft", "企业 AI 套件/云/安全", "A-", "AI ARR 370 亿美元以上，云规模和现金流强", "AI 毛利、OpenAI/CapEx、Copilot 净新增", "Azure/Copilot/安全增长、RPO", "AI 基建拖累毛利"],
      ["NOW", "ServiceNow", "工作流 AI 控制塔", "A-", "cRPO 和 Now Assist 大客户扩张验证生产化", "AI ACV、续约率、客户扩张", "Now Assist 百万美元客户、cRPO", "估值和 SaaS 席位替代担忧"],
      ["PLTR", "Palantir", "AI-native 运营平台", "A-/B+", "收入、美国商业、Rule of 40 同时高增", "高估值是否被持续超预期支撑", "AIP 大单、商业客户、FCF", "EV/Sales 极高，政府/大客户集中"],
      ["CRM", "Salesforce", "AI CRM/Agentforce", "B+", "Agentforce ARR 和 Data 360 高增", "能否带动 organic revenue 重新加速", "Agentforce ARR、总收入、margin", "AI 指标高增但总增长仍中低双位数"],
      ["SNOW", "Snowflake", "AI 数据云", "B+", "产品收入/RPO 回升，AI 数据层位置重要", "AI 用量是否耐久、GAAP 盈利路径", "NRR、RPO、AI accounts、Cortex", "消费优化、亏损和估值"],
      ["DDOG", "Datadog", "AI observability/LLM ops", "B+", "生产 AI 失败率和容量限制创造需求", "AI 产品能否货币化为大客户 ARR", "ARR>100K 客户、多产品、AI module", "估值高、云优化周期"],
      ["CRWD", "CrowdStrike", "AI 安全治理", "B", "AI 扩大攻击面，Falcon Flex 动能强", "AI security 收入拆分和估值", "ARR、Flex、AI Detection Response", "高倍数和平台竞争"],
      ["ADBE", "Adobe", "创意 AI/内容生产", "B/Lead", "AI-first ARR 高增，核心订阅仍增长", "AI 是否增量而非替代席位", "AI-first ARR、Firefly 用量、churn", "模型替代与毛利压力"]
    ]
  },
  {
    id: "q4_1_1_core_tracks",
    layer: "Q4.1.1",
    title: "核心跟踪标的",
    question: "Q4.1.1 哪些公司是当前 AI 软件主线的核心跟踪标的？",
    fact:
      "MSFT 有最大 AI revenue run-rate 和云/套件入口；NOW 有工作流控制塔定位、cRPO 和 Now Assist 大客户扩张；PLTR 有 AI-native 平台、美国商业高增和 Rule of 40 高分。",
    inference:
      "核心跟踪标的应同时满足收入兑现、工作流位置、客户数据/权限壁垒和未来可验证指标。MSFT/NOW 偏确定性，PLTR 偏弹性。",
    judgment:
      "核心跟踪：MSFT、NOW、PLTR。观察强度分别为 A-、A-、A-/B+；PLTR 因估值极高需单独约束赔率。",
    gap:
      "需要统一估值口径和下一季 AI 直接收入/ARR 细分。",
    trigger:
      "若 AI ARR/RPO 与毛利同步改善，上调；若高估值标的出现任何增长/现金流下修，先降赔率而不是直接否定产业趋势。",
    evidence_ids: [
      "ev_ai_sw_msft_fy26q3_ai_cloud",
      "ev_ai_sw_now_q1_2026_control_tower",
      "ev_ai_sw_pltr_q1_2026_aip",
      "ev_ai_sw_valuation_snapshot_stockanalysis_20260528"
    ],
    next_question_ids: [],
    dispatch: dispatch(
      "financial statement plus valuation",
      "financial-statement-analysis then valuation-analysis",
      ["MSFT/NOW/PLTR earnings", "StockAnalysis valuation snapshots"],
      "normalize growth/RPO/ARR/FCF first, then classify valuation odds",
      "used as protocol chain",
      "none"
    )
  },
  {
    id: "q4_1_2_high_beta_tracks",
    layer: "Q4.1.1",
    title: "高优先验证标的",
    question: "Q4.1.2 哪些公司值得高优先验证，但需要更多证据？",
    fact:
      "CRM 的 Agentforce ARR 高增但需要证明总收入再加速；SNOW 的产品收入和 RPO 回升但仍需验证 AI 用量耐久；DDOG 的 AI observability 产品方向清晰但需要货币化证据；CRWD 把 AI 安全作为新攻击面但 AI-specific 收入披露有限；ADBE AI-first ARR 高增但面临模型替代风险。",
    inference:
      "这些标的更像“验证型机会”：若下一季指标延续，会从线索/高优先变成核心；若 AI 指标没有拉动总体收入或利润，会被估值反证快速压制。",
    judgment:
      "高优先验证：CRM、SNOW、DDOG、CRWD；创意/垂直验证：ADBE。它们应该进入观察清单，但不应和核心跟踪标的使用同一风险阈值。",
    gap:
      "缺少 AI SKU 直接毛利、AI-specific ARR、客户留存和价格实现。",
    trigger:
      "下一季重点看 CRM organic growth、SNOW NRR/RPO、DDOG 大客户和 AI module、CRWD AI security 模块、ADBE AI-first ARR 与 churn。",
    evidence_ids: [
      "ev_ai_sw_crm_fy27q1_agentforce",
      "ev_ai_sw_snow_fy27q1_data_cloud",
      "ev_ai_sw_ddog_q1_2026_observability",
      "ev_ai_sw_crwd_fy26q4_ai_security",
      "ev_ai_sw_adbe_q1_2026_creative",
      "ev_ai_sw_valuation_snapshot_stockanalysis_20260528"
    ],
    next_question_ids: [],
    dispatch: dispatch(
      "financial statement plus valuation",
      "financial-statement-analysis then valuation-analysis",
      ["CRM/SNOW/DDOG/CRWD/ADBE earnings", "StockAnalysis valuation snapshots"],
      "extract AI metric, total company translation, margin/valuation tests",
      "used as protocol chain",
      "none"
    )
  }
];

const questionPlan = {
  generated_at: generatedAt,
  planning_mode: "research_goal_qa_with_type_adapter_and_skill_dispatch",
  meta_question: framework.meta_question,
  research_type_adaptation: {
    selected_type: "industry/theme opportunity",
    reason:
      "用户问题是投资机会研究，不是单家公司、事件或技术路线，因此使用行业/主题机会映射。",
    q_map: {
      Q1: "需求真实度：企业是否真实把 AI 软件放入预算并进入生产",
      Q2: "价值捕获瓶颈：哪些软件层有入口、数据、工作流、治理或安全瓶颈",
      Q3: "反证和赔率：ROI、治理、毛利和估值是否会证伪",
      Q4: "标的观察清单：把结论映射到具体证券并列出验证数据"
    }
  },
  l1: nodes
    .filter((n) => n.layer === "Q1" || n.layer === "Q2" || n.layer === "Q3" || n.layer === "Q4")
    .map((n) => ({
      id: n.id,
      question: n.question,
      rationale: n.answer_summary,
      next_question_ids: n.next_question_ids
    })),
  specialty_dispatch_policy: {
    financial_statement: "financial-statement-analysis",
    valuation: "valuation-analysis",
    long_reading: "leaf-research-deepseek plus DeepSeek MCP",
    html: "frontend-design",
    final_judge: "GPT"
  }
};

const qaTree = {
  generated_at: generatedAt,
  framework: "research_goal_qa",
  research_type: "industry/theme opportunity",
  q_map: questionPlan.research_type_adaptation.q_map,
  nodes
};

const workbench = {
  generated_at: generatedAt,
  current_research_goal: nodes.find((n) => n.id === "l0_goal"),
  research_type_adaptation: questionPlan.research_type_adaptation,
  specialty_skill_trace: skillTrace,
  evidence_count: evidence.length,
  conclusions: [
    {
      id: "c1",
      statement:
        "AI 软件需求已经进入企业预算，但最可靠的证据来自 ARR/RPO/收入/现金流，而不是模型热度。",
      support: [
        "ev_ai_sw_gartner_spending_20260519",
        "ev_ai_sw_msft_fy26q3_ai_cloud",
        "ev_ai_sw_now_q1_2026_control_tower",
        "ev_ai_sw_pltr_q1_2026_aip"
      ],
      uncertainty: "AI 指标定义不可比，仍需拆分真实增量收入。"
    },
    {
      id: "c2",
      statement:
        "价值捕获优先级为工作流/套件、数据和可观测性、安全治理；创意和垂直应用属于验证型机会。",
      support: [
        "ev_ai_sw_crm_fy27q1_agentforce",
        "ev_ai_sw_snow_fy27q1_data_cloud",
        "ev_ai_sw_ddog_q1_2026_observability",
        "ev_ai_sw_crwd_fy26q4_ai_security",
        "ev_ai_sw_adbe_q1_2026_creative"
      ],
      uncertainty: "AI SKU 毛利、续约率、折扣和直接收入披露不足。"
    },
    {
      id: "c3",
      statement:
        "最大的反证不是模型退步，而是项目取消、治理事故、毛利被算力成本侵蚀以及估值过度提前反映。",
      support: [
        "ev_ai_sw_gartner_agentic_cancel_20250625",
        "ev_ai_sw_gartner_agent_governance_20260526",
        "ev_ai_sw_msft_fy26q3_margin_pressure",
        "ev_ai_sw_valuation_snapshot_stockanalysis_20260528"
      ],
      uncertainty: "需要统一估值日和 forward estimates 做 reverse DCF。"
    }
  ],
  target_observation_list: nodes.find((n) => n.id === "q4_1_observation_list").target_table
};

function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function mdLink(id) {
  const ev = evidence.find((e) => e.id === id);
  if (!ev) return id;
  return `[${id}](${ev.url})`;
}

function evidenceLinks(ids = []) {
  return ids.map(mdLink).join("，");
}

function l3Markdown(n) {
  return `### ${n.question}

- 事实：${n.fact}
- 推理：${n.inference}
- 判断：${n.judgment}
- 缺口：${n.gap}
- 触发器：${n.trigger}
- 证据：${evidenceLinks(n.evidence_ids)}
- Skill 调度：${n.dispatch ? `${n.dispatch.task_family} -> ${n.dispatch.selected_skill}；状态：${n.dispatch.skill_output_status}；GPT 验证：${n.dispatch.gpt_verification_status}` : "无"}
`;
}

const l3Nodes = nodes.filter((n) => n.layer.endsWith(".1"));
const targetTable = nodes.find((n) => n.id === "q4_1_observation_list").target_table;

const md = `# AI 软件方向投资机会研究

生成时间：${generatedAt}

边界：${framework.boundary}

## 1. 当前研究目标

${nodes.find((n) => n.id === "l0_goal").answer_summary}

## 2. 研究类型适配层与执行计划

- 研究类型：${questionPlan.research_type_adaptation.selected_type}
- 适配理由：${questionPlan.research_type_adaptation.reason}
- Q1：${questionPlan.research_type_adaptation.q_map.Q1}
- Q2：${questionPlan.research_type_adaptation.q_map.Q2}
- Q3：${questionPlan.research_type_adaptation.q_map.Q3}
- Q4：${questionPlan.research_type_adaptation.q_map.Q4}

执行计划：

1. Q1 先确认需求是否真实进入预算。收集 Gartner/Menlo 市场规模与公司 ARR/RPO/收入证据，用 financial-statement-analysis 规范化公司数字。
2. Q2 再定位价值捕获瓶颈。按工作流、数据/可观测性、安全治理、创意/垂直应用拆分，并把评分卡放在 Q2.1 内。
3. Q3 绑定反证。用 Gartner/Datadog/Microsoft/估值快照测试 ROI、治理、成本和价格预期。
4. Q4 输出具体标的观察清单。只给研究优先级，不给买卖建议。

## Q1 需求真实度

${nodes.find((n) => n.id === "q1_demand").answer_summary}

${l3Markdown(nodes.find((n) => n.id === "q1_1_1_market_spend"))}

${l3Markdown(nodes.find((n) => n.id === "q1_1_2_public_company_signals"))}

## Q2 价值捕获瓶颈

${nodes.find((n) => n.id === "q2_capture").answer_summary}

### Q2.1 瓶颈评分卡

| 节点 | 代表标的 | 强度 | 捕获理由 | 关键风险 |
|---|---|---:|---|---|
${nodes.find((n) => n.id === "q2_1_nodes").scorecard.map((r) => `| ${r.join(" | ")} |`).join("\n")}

${l3Markdown(nodes.find((n) => n.id === "q2_1_1_suite_workflow"))}

${l3Markdown(nodes.find((n) => n.id === "q2_1_2_data_observability"))}

${l3Markdown(nodes.find((n) => n.id === "q2_1_3_security"))}

${l3Markdown(nodes.find((n) => n.id === "q2_1_4_creative_vertical"))}

## Q3 反证与赔率

${nodes.find((n) => n.id === "q3_risk").answer_summary}

### Q3.1 反证测试

| 风险 | 监控数据 | 绿灯 | 红灯 |
|---|---|---|---|
${nodes.find((n) => n.id === "q3_1_tests").risk_tests.map((r) => `| ${r.join(" | ")} |`).join("\n")}

${l3Markdown(nodes.find((n) => n.id === "q3_1_1_governance_roi"))}

${l3Markdown(nodes.find((n) => n.id === "q3_1_2_cost_margin"))}

${l3Markdown(nodes.find((n) => n.id === "q3_1_3_valuation"))}

## Q4 标的观察清单

${nodes.find((n) => n.id === "q4_targets").answer_summary}

| Ticker | 名称 |  thesis node | 强度 | 原因 | 待验证数据 | 催化剂 | 风险 |
|---|---|---|---:|---|---|---|---|
${targetTable.map((r) => `| ${r.join(" | ")} |`).join("\n")}

${l3Markdown(nodes.find((n) => n.id === "q4_1_1_core_tracks"))}

${l3Markdown(nodes.find((n) => n.id === "q4_1_2_high_beta_tracks"))}

## Specialty Skill Trace

${skillTrace.map((s) => `- ${s.task_family}：${s.selected_skill}；状态：${s.status}；结果：${s.output}`).join("\n")}

## Source Index

${evidence.map((e) => `- ${e.id}：${e.source_name}，${e.information_category}，${e.support_refute_or_lead}，[source](${e.url})`).join("\n")}
`;

function renderEvidenceBadges(ids = []) {
  return `<div class="evidence-links">${ids
    .map((id) => {
      const ev = evidence.find((e) => e.id === id);
      return ev ? `<a href="${esc(ev.url)}" target="_blank">${esc(id)}</a>` : `<span>${esc(id)}</span>`;
    })
    .join("")}</div>`;
}

function renderL3(n) {
  return `<details class="l3">
    <summary><span>${esc(n.question)}</span><b>${esc(n.dispatch?.selected_skill || "GPT")}</b></summary>
    <div class="dispatch">
      <span>task_family: ${esc(n.dispatch?.task_family || "n/a")}</span>
      <span>skill: ${esc(n.dispatch?.selected_skill || "n/a")}</span>
      <span>status: ${esc(n.dispatch?.skill_output_status || "n/a")}</span>
      <span>fallback: ${esc(n.dispatch?.fallback_used || "none")}</span>
    </div>
    <div class="answer-grid">
      <div><h4>事实</h4><p>${esc(n.fact)}</p></div>
      <div><h4>推理</h4><p>${esc(n.inference)}</p></div>
      <div><h4>判断</h4><p>${esc(n.judgment)}</p></div>
      <div><h4>缺口</h4><p>${esc(n.gap)}</p></div>
      <div class="wide"><h4>触发器</h4><p>${esc(n.trigger)}</p></div>
    </div>
    ${renderEvidenceBadges(n.evidence_ids)}
  </details>`;
}

function renderRows(rows, headers) {
  return `<div class="table-wrap"><table><thead><tr>${headers
    .map((h) => `<th>${esc(h)}</th>`)
    .join("")}</tr></thead><tbody>${rows
    .map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join("")}</tr>`)
    .join("")}</tbody></table></div>`;
}

const html = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AI 软件方向投资机会研究</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f5f5f7;
      --panel: #ffffff;
      --panel-soft: #fbfbfd;
      --text: #1d1d1f;
      --muted: #6e6e73;
      --line: #d8d8df;
      --blue: #0066cc;
      --green: #1d7f46;
      --orange: #b05a00;
      --red: #b42318;
      --shadow: 0 18px 50px rgba(0,0,0,.06);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", "Microsoft YaHei", sans-serif;
      line-height: 1.58;
      letter-spacing: 0;
    }
    a { color: var(--blue); text-decoration: none; }
    a:hover { text-decoration: underline; }
    .topbar {
      position: sticky;
      top: 0;
      z-index: 20;
      border-bottom: 1px solid rgba(0,0,0,.08);
      background: rgba(245,245,247,.86);
      backdrop-filter: blur(18px);
    }
    .topbar-inner {
      max-width: 1180px;
      margin: 0 auto;
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
    }
    .brand { font-weight: 700; }
    nav { display: flex; gap: 12px; flex-wrap: wrap; }
    nav a { color: #424245; font-size: 13px; }
    header {
      max-width: 1180px;
      margin: 0 auto;
      padding: 56px 24px 30px;
    }
    .eyebrow {
      color: var(--blue);
      font-weight: 700;
      font-size: 14px;
      margin-bottom: 12px;
    }
    h1 {
      margin: 0;
      font-size: clamp(34px, 5vw, 64px);
      line-height: 1.04;
      letter-spacing: 0;
    }
    .subtitle {
      max-width: 900px;
      margin: 18px 0 0;
      color: var(--muted);
      font-size: 19px;
    }
    .hero-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-top: 28px;
    }
    .metric {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      box-shadow: var(--shadow);
    }
    .metric b { display: block; font-size: 22px; margin-bottom: 4px; }
    .metric span { color: var(--muted); font-size: 13px; }
    main { max-width: 1180px; margin: 0 auto; padding: 0 24px 64px; }
    section {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 28px;
      margin: 18px 0;
      box-shadow: var(--shadow);
    }
    h2 { margin: 0 0 14px; font-size: 28px; letter-spacing: 0; }
    h3 { margin: 22px 0 10px; font-size: 20px; }
    .lead { color: #424245; font-size: 16px; }
    .plan {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }
    .plan div, .trace-card, .source-card {
      background: var(--panel-soft);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }
    .plan b { display: block; margin-bottom: 6px; }
    .l3 {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel-soft);
      margin: 12px 0;
      overflow: clip;
    }
    .l3 summary {
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      padding: 15px 16px;
      font-weight: 700;
    }
    .l3 summary b {
      color: var(--blue);
      font-size: 12px;
      white-space: nowrap;
    }
    .dispatch {
      position: sticky;
      top: 46px;
      z-index: 5;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      padding: 10px 16px;
      border-top: 1px solid var(--line);
      border-bottom: 1px solid var(--line);
      background: rgba(251,251,253,.94);
      backdrop-filter: blur(10px);
    }
    .dispatch span, .tag {
      border: 1px solid var(--line);
      background: #fff;
      border-radius: 999px;
      padding: 4px 9px;
      color: #424245;
      font-size: 12px;
    }
    .answer-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      padding: 16px;
    }
    .answer-grid div {
      background: #fff;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }
    .answer-grid .wide { grid-column: 1 / -1; }
    .answer-grid h4 { margin: 0 0 6px; font-size: 14px; color: var(--muted); }
    .answer-grid p { margin: 0; }
    .evidence-links {
      padding: 0 16px 16px;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .evidence-links a {
      background: #eef5ff;
      border: 1px solid #c8ddff;
      border-radius: 999px;
      padding: 5px 9px;
      font-size: 12px;
    }
    .table-wrap {
      width: 100%;
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      margin: 14px 0;
    }
    table {
      width: 100%;
      min-width: 920px;
      border-collapse: collapse;
      font-size: 14px;
    }
    th, td {
      text-align: left;
      vertical-align: top;
      padding: 12px;
      border-bottom: 1px solid var(--line);
    }
    th {
      position: sticky;
      top: 46px;
      z-index: 2;
      background: #f7f7fa;
      color: #424245;
      font-size: 12px;
    }
    tr:last-child td { border-bottom: 0; }
    .trace-grid, .source-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }
    .source-card h4, .trace-card h4 { margin: 0 0 6px; }
    .source-card p, .trace-card p { margin: 0; color: var(--muted); font-size: 13px; }
    .badge-row { display: flex; gap: 8px; flex-wrap: wrap; margin: 14px 0; }
    .badge-row .support { color: var(--green); }
    .badge-row .refute { color: var(--red); }
    .badge-row .lead { color: var(--orange); }
    @media (max-width: 820px) {
      .topbar-inner { align-items: flex-start; flex-direction: column; }
      .hero-grid, .plan, .trace-grid, .source-grid, .answer-grid { grid-template-columns: 1fr; }
      .answer-grid .wide { grid-column: auto; }
      section { padding: 20px; }
      nav { gap: 8px; }
    }
  </style>
</head>
<body>
  <div class="topbar">
    <div class="topbar-inner">
      <div class="brand">AI Software Research</div>
      <nav>
        <a href="#goal">目标</a>
        <a href="#plan">适配层</a>
        <a href="#q1">Q1</a>
        <a href="#q2">Q2</a>
        <a href="#q3">Q3</a>
        <a href="#q4">Q4</a>
        <a href="#trace">Skill Trace</a>
        <a href="#sources">Sources</a>
      </nav>
    </div>
  </div>
  <header>
    <div class="eyebrow">Research Goal QA · ${esc(generatedAt)}</div>
    <h1>AI 软件方向投资机会研究</h1>
    <p class="subtitle">${esc(nodes.find((n) => n.id === "l0_goal").answer_summary)}</p>
    <div class="hero-grid">
      <div class="metric"><b>$453B</b><span>Gartner 2026 AI Software forecast</span></div>
      <div class="metric"><b>$37B</b><span>Menlo 2025 enterprise GenAI spend</span></div>
      <div class="metric"><b>${evidence.length}</b><span>evidence records</span></div>
      <div class="metric"><b>Q1-Q4</b><span>type-adapted QA tree</span></div>
    </div>
  </header>
  <main>
    <section id="goal">
      <h2>1. 当前研究目标</h2>
      <p class="lead">${esc(nodes.find((n) => n.id === "l0_goal").answer_summary)}</p>
      <div class="badge-row">
        <span class="tag">对象：AI 软件</span>
        <span class="tag">时间：2026-2028</span>
        <span class="tag">边界：观察清单，不是交易指令</span>
      </div>
    </section>
    <section id="plan">
      <h2>2. 研究类型适配层与执行计划</h2>
      <p class="lead">${esc(questionPlan.research_type_adaptation.reason)}</p>
      <div class="plan">
        ${Object.entries(questionPlan.research_type_adaptation.q_map)
          .map(([k, v]) => `<div><b>${esc(k)}</b><span>${esc(v)}</span></div>`)
          .join("")}
      </div>
    </section>
    <section id="q1">
      <h2>Q1 需求真实度</h2>
      <p class="lead">${esc(nodes.find((n) => n.id === "q1_demand").answer_summary)}</p>
      ${renderL3(nodes.find((n) => n.id === "q1_1_1_market_spend"))}
      ${renderL3(nodes.find((n) => n.id === "q1_1_2_public_company_signals"))}
    </section>
    <section id="q2">
      <h2>Q2 价值捕获瓶颈</h2>
      <p class="lead">${esc(nodes.find((n) => n.id === "q2_capture").answer_summary)}</p>
      <h3>Q2.1 瓶颈评分卡</h3>
      ${renderRows(nodes.find((n) => n.id === "q2_1_nodes").scorecard, ["节点", "代表标的", "强度", "捕获理由", "关键风险"])}
      ${renderL3(nodes.find((n) => n.id === "q2_1_1_suite_workflow"))}
      ${renderL3(nodes.find((n) => n.id === "q2_1_2_data_observability"))}
      ${renderL3(nodes.find((n) => n.id === "q2_1_3_security"))}
      ${renderL3(nodes.find((n) => n.id === "q2_1_4_creative_vertical"))}
    </section>
    <section id="q3">
      <h2>Q3 反证与赔率</h2>
      <p class="lead">${esc(nodes.find((n) => n.id === "q3_risk").answer_summary)}</p>
      <h3>Q3.1 反证测试</h3>
      ${renderRows(nodes.find((n) => n.id === "q3_1_tests").risk_tests, ["风险", "监控数据", "绿灯", "红灯"])}
      ${renderL3(nodes.find((n) => n.id === "q3_1_1_governance_roi"))}
      ${renderL3(nodes.find((n) => n.id === "q3_1_2_cost_margin"))}
      ${renderL3(nodes.find((n) => n.id === "q3_1_3_valuation"))}
    </section>
    <section id="q4">
      <h2>Q4 标的观察清单</h2>
      <p class="lead">${esc(nodes.find((n) => n.id === "q4_targets").answer_summary)}</p>
      ${renderRows(targetTable, ["Ticker", "名称", "thesis node", "强度", "原因", "待验证数据", "催化剂", "风险"])}
      ${renderL3(nodes.find((n) => n.id === "q4_1_1_core_tracks"))}
      ${renderL3(nodes.find((n) => n.id === "q4_1_2_high_beta_tracks"))}
    </section>
    <section id="trace">
      <h2>Specialty Skill Trace</h2>
      <div class="trace-grid">
        ${skillTrace
          .map(
            (s) => `<div class="trace-card"><h4>${esc(s.task_family)}</h4><p><b>${esc(s.selected_skill)}</b> · ${esc(s.status)}</p><p>${esc(s.output)}</p></div>`
          )
          .join("")}
      </div>
    </section>
    <section id="sources">
      <h2>Source Index</h2>
      <div class="source-grid">
        ${evidence
          .map(
            (e) => `<div class="source-card"><h4><a href="${esc(e.url)}" target="_blank">${esc(e.id)}</a></h4><p>${esc(e.source_name)} · ${esc(e.information_category)} · ${esc(e.support_refute_or_lead)}</p><p>${esc(e.summary)}</p></div>`
          )
          .join("")}
      </div>
    </section>
  </main>
</body>
</html>`;

const todo = `# AI 软件方向投资机会研究待办清单

更新时间：2026-05-29

## 当前状态

- 报告主文件：\`professional_report.html\`
- Markdown 备份：\`professional_report.md\`
- QA 树：\`qa_tree.json\`
- 证据库：\`evidence.jsonl\`
- 工作底稿：\`investment_workbench.json\`
- 当前框架：research_goal_qa，已加入研究类型适配层和 specialty skill dispatch trace。

## 已完成

- [x] 将研究类型识别为 industry/theme opportunity。
- [x] Q1-Q4 已按 AI 软件机会适配：需求真实度、价值捕获瓶颈、反证与赔率、标的观察清单。
- [x] 证据库覆盖 Gartner、Menlo、Microsoft、Salesforce、ServiceNow、Palantir、Snowflake、Datadog、CrowdStrike、Adobe 和估值快照。
- [x] L3 叶子问题均包含 fact / inference / judgment / gap / trigger。
- [x] L3 叶子问题均写入 skill dispatch trace。
- [x] HTML 使用轻量 Apple-inspired 研究页面，并把评分卡、风险表、标的表嵌入对应 QA 节点。

## 后续更新重点

- [ ] 统一估值日和 forward estimates，用 valuation-analysis 做 reverse DCF。
- [ ] 下一季逐家公司补充 AI-specific ARR、AI SKU 毛利、RPO/cRPO 和 FCF 转换。
- [ ] 增加 PANW、NET、MDB、INTU、DUOL、APP、ORCL 等候选对照，避免观察清单过窄。
- [ ] 若 DeepSeek MCP 恢复稳定，可重新分配长报告/财报阅读任务，补全 L3 source parser 输出。
`;

fs.writeFileSync(path.join(base, "project.json"), JSON.stringify(framework, null, 2), "utf8");
fs.writeFileSync(path.join(base, "question_plan.json"), JSON.stringify(questionPlan, null, 2), "utf8");
fs.writeFileSync(path.join(base, "qa_tree.json"), JSON.stringify(qaTree, null, 2), "utf8");
fs.writeFileSync(path.join(base, "investment_workbench.json"), JSON.stringify(workbench, null, 2), "utf8");
fs.writeFileSync(path.join(base, "evidence.jsonl"), evidence.map((e) => JSON.stringify(e)).join("\n") + "\n", "utf8");
fs.writeFileSync(path.join(base, "professional_report.md"), md, "utf8");
fs.writeFileSync(path.join(base, "professional_report.html"), html, "utf8");
fs.writeFileSync(path.join(base, "TODO.md"), todo, "utf8");

console.log(`Generated ${base}`);
console.log(
  JSON.stringify(
    {
      evidence_count: evidence.length,
      qa_nodes: nodes.length,
      html: path.join(base, "professional_report.html")
    },
    null,
    2
  )
);
