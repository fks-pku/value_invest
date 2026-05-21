from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any

from value_invest_research.models import EvidenceRecord, ValidationError
from value_invest_research.runlog import RunLog, RunStatus


TICKER_ALIASES = {"APPL": "AAPL"}

FOUNDATION_SECTIONS = [
    {
        "id": "source_origin",
        "label": "Source and origin",
        "keywords": ["found", "origin", "mission", "ipo", "prospectus", "profile", "dna", "wedge"],
        "default_gap": "Need primary sources for founding context, original customer wedge, and company DNA.",
    },
    {
        "id": "history",
        "label": "Company history",
        "keywords": ["history", "milestone", "ipo", "listing", "acquisition", "restructuring", "capital allocation"],
        "default_gap": "Need dated milestones for business, governance, financing, M&A, and capital allocation.",
    },
    {
        "id": "current_business",
        "label": "Current business",
        "keywords": [
            "revenue",
            "gross profit",
            "profit",
            "income",
            "segment",
            "shipment",
            "deliver",
            "mau",
            "cash flow",
            "margin",
            "asp",
        ],
        "default_gap": "Need segment revenue, customers, demand drivers, margins, and cash conversion evidence.",
    },
    {
        "id": "value_chain",
        "label": "Value chain position",
        "keywords": [
            "supplier",
            "supply",
            "component",
            "memory",
            "channel",
            "store",
            "inventory",
            "manufacturing",
            "capex",
        ],
        "default_gap": "Need supplier, channel, customer, substitute, and bargaining-power evidence.",
    },
    {
        "id": "competition",
        "label": "Competitive landscape",
        "keywords": [
            "share",
            "rank",
            "ranking",
            "competition",
            "competitor",
            "market",
            "shipments",
            "nev",
            "smartphone",
        ],
        "default_gap": "Need peer ranking, share trend, market structure, and competition-intensity evidence.",
    },
    {
        "id": "strategy",
        "label": "Strategy analysis",
        "keywords": ["strategy", "r&d", "ai", "chip", "ev", "capital expenditure", "resource allocation", "initiative"],
        "default_gap": "Need mission, corporate strategy, competitive strategy, functional strategy, and resource allocation.",
    },
    {
        "id": "governance",
        "label": "Organization, culture, and governance",
        "keywords": ["management", "board", "governance", "voting", "wvr", "control", "founder", "ceo", "chairman"],
        "default_gap": "Need leadership, incentives, ownership/control, board quality, and culture evidence.",
    },
    {
        "id": "risk_sweep",
        "label": "Risk sweep",
        "keywords": [
            "risk",
            "recall",
            "regulator",
            "regulatory",
            "lawsuit",
            "decline",
            "decrease",
            "loss",
            "debt",
            "liability",
            "safety",
        ],
        "default_gap": "Need business, financial, accounting, legal, technology, capital-allocation, governance, and valuation risks.",
    },
]

BUSINESS_NODE_RULES = [
    {
        "id": "smartphone",
        "label": "Smartphone platform",
        "role": "User acquisition and ecosystem anchor",
        "keywords": ["smartphone", "iphone", "phone", "shipment", "asp", "handset"],
        "kpis": ["shipments", "ASP", "share", "gross margin", "replacement cycle"],
    },
    {
        "id": "iot",
        "label": "IoT and connected devices",
        "role": "Cross-category expansion and ecosystem lock-in",
        "keywords": ["iot", "connected", "home", "wearable", "aiot", "device"],
        "kpis": ["connected devices", "multi-device users", "gross margin", "repeat purchase"],
    },
    {
        "id": "services",
        "label": "Internet and services profit pool",
        "role": "High-margin monetization layer",
        "keywords": ["service", "services", "advertising", "game", "mau", "subscription", "app store"],
        "kpis": ["MAU", "ARPU", "gross margin", "take rate", "retention"],
    },
    {
        "id": "smart_ev",
        "label": "Smart EV and mobility platform",
        "role": "Second growth curve with manufacturing and safety obligations",
        "keywords": ["ev", "vehicle", "auto", "car", "su7", "yu7", "nev", "delivery", "deliveries", "assisted driving"],
        "kpis": ["deliveries", "ASP", "vehicle gross margin", "capex", "warranty cost", "recalls"],
    },
    {
        "id": "supply_chain",
        "label": "Supply chain and manufacturing system",
        "role": "Cost, availability, and quality-control constraint",
        "keywords": ["supplier", "supply", "component", "memory", "inventory", "manufacturing", "capex", "factory"],
        "kpis": ["inventory days", "BOM inflation", "capacity utilization", "quality cost"],
    },
    {
        "id": "capital_allocation",
        "label": "Capital allocation and cash engine",
        "role": "Funds reinvestment, buybacks, dividends, and balance-sheet resilience",
        "keywords": ["cash", "operating cash", "free cash", "buyback", "repurchase", "dividend", "capex", "equity", "debt"],
        "kpis": ["operating cash flow", "free cash flow", "net cash", "capex", "ROIC"],
    },
    {
        "id": "governance_control",
        "label": "Governance and control structure",
        "role": "Management quality, incentives, and minority-shareholder constraint",
        "keywords": ["management", "board", "governance", "voting", "wvr", "founder", "ceo", "chairman", "control"],
        "kpis": ["voting control", "incentives", "related-party risk", "capital-allocation discipline"],
    },
    {
        "id": "group_financials",
        "label": "Group financial model",
        "role": "Revenue quality, margin structure, cash conversion, and balance sheet",
        "keywords": ["revenue", "gross profit", "income", "profit", "assets", "liabilities", "equity", "margin"],
        "kpis": ["revenue", "gross margin", "operating margin", "net profit", "cash conversion"],
    },
]

QUESTION_TRANSLATIONS = {
    "Is the smartphone baseline stable, or is share/margin deterioration changing the platform thesis?": "手机基本盘是否稳定，还是份额/毛利恶化正在改变平台逻辑？",
    "Is shipment weakness active portfolio control, component shortage, price elasticity, or real demand loss?": "出货疲弱到底是主动控货、部件短缺、价格弹性，还是需求真实下滑？",
    "Does smartphone share pressure weaken service and IoT user acquisition?": "手机份额压力是否会削弱服务和 IoT 的用户入口？",
    "Does IoT create real ecosystem lock-in and profit quality, or only hardware volume?": "IoT 是真实生态锁定和利润质量，还是单纯硬件放量？",
    "Are multi-device users increasing because of genuine lock-in or because of discount-driven category expansion?": "多设备用户增长来自真实锁定，还是折扣驱动的品类扩张？",
    "Is the service profit pool durable, or exposed to platform, traffic, and regulatory pressure?": "互联网服务利润池是否可持续，还是暴露于平台、流量和监管压力？",
    "Is high service margin protected by user behavior, platform control, or temporary ad-cycle strength?": "高服务毛利是由用户行为和平台控制保护，还是广告周期的阶段性结果？",
    "Can Smart EV become a repeatable profit pool after safety, warranty, capex, and price competition?": "智能 EV 在安全、质保、资本开支和价格竞争之后，能否成为可重复利润池？",
    "Is vehicle gross margin sustainable after launch mix, price competition, warranty, recall, and service costs?": "剔除上市初期 mix、价格竞争、质保、召回和服务成本后，整车毛利是否可持续？",
    "Does safety and assisted-driving performance change customer trust or regulatory cost?": "安全和辅助驾驶表现是否会改变用户信任或监管成本？",
    "Can the company pass through component inflation and preserve quality while scaling?": "公司能否在规模扩张中传导部件通胀并保持质量？",
    "Can cash flows fund the next growth curve without weakening returns or minority-shareholder economics?": "现金流能否支持下一增长曲线，同时不削弱回报和少数股东利益？",
    "Is reinvestment earning adequate returns after capex, working capital, and shareholder dilution?": "考虑资本开支、营运资本和摊薄后，再投资回报是否足够？",
    "Does founder/control structure improve long-term execution or create governance discount risk?": "创始人/控制权结构是提升长期执行，还是带来治理折价？",
    "Are control rights being used for patient compounding or for unaccountable capital allocation?": "控制权是在服务长期复利，还是导致缺乏约束的资本配置？",
    "Which segment is actually driving gross profit, cash conversion, and durable value creation?": "到底哪个分部在驱动毛利、现金转化和可持续价值创造？",
    "Which fresh evidence would most quickly falsify the current baseline?": "哪类新增证据能最快证伪当前基线？",
}

DISPLAY_TRANSLATIONS = {
    "research_ready_with_specific_gaps": "可研究，但仍有明确缺口",
    "complete": "完整",
    "incomplete": "未完成",
    "evidenced": "证据充分",
    "partial": "部分证据",
    "missing": "缺证据",
    "open": "开放",
    "needs_data": "需要补数据",
    "primary": "一手",
    "baseline_update": "基线更新",
    "strengthening": "强化线索",
    "weakening": "削弱/反证",
    "research_lead": "研究线索",
    "high": "高",
    "medium_high": "中高",
    "medium": "中",
    "low": "低",
    "Company baseline quality before message-flow analysis.": "消息流分析前的公司基础画像质量。",
    "Eight-section framework coverage with local evidence.": "八步框架中已有本地证据覆盖的部分。",
    "Highest-priority questions that should drive the next evidence search.": "下一轮证据搜索应优先围绕这些问题展开。",
    "No local fact evidence yet.": "当前没有映射到本节的本地事实证据。",
    "No inference until evidence is added.": "补充证据前不做推论。",
    "No judgment until evidence is added.": "补充证据前不做判断。",
    "No material gap flagged.": "当前未标记重大缺口。",
    "No evidence mapped": "未映射证据",
    "No local fact evidence yet": "当前没有映射到本节的本地事实证据",
    "No disconfirming condition mapped.": "尚未映射反证条件。",
    "No required evidence mapped.": "尚未映射下一步数据。",
    "No update trigger mapped.": "尚未映射更新触发器。",
    "needs data": "需要数据",
    "Do not use this section to strengthen a thesis until primary or high-reliability evidence is added.": "在补充一手或高可靠证据前，本节不能用于强化结论。",
    "Source and origin has a local evidence baseline, but any thesis change still requires message-flow testing.": "源头溯源已有本地证据基线，但任何结论变化仍需经过消息流检验。",
    "Company history has a local evidence baseline, but any thesis change still requires message-flow testing.": "公司历史已有本地证据基线，但任何结论变化仍需经过消息流检验。",
    "Current business has a local evidence baseline, but any thesis change still requires message-flow testing.": "当下生意已有本地证据基线，但任何结论变化仍需经过消息流检验。",
    "Value chain position has a local evidence baseline, but any thesis change still requires message-flow testing.": "产业链定位已有本地证据基线，但任何结论变化仍需经过消息流检验。",
    "Competitive landscape has a local evidence baseline, but any thesis change still requires message-flow testing.": "竞争格局已有本地证据基线，但任何结论变化仍需经过消息流检验。",
    "Strategy analysis has a local evidence baseline, but any thesis change still requires message-flow testing.": "战略分析已有本地证据基线，但任何结论变化仍需经过消息流检验。",
    "Organization, culture, and governance has a local evidence baseline, but any thesis change still requires message-flow testing.": "组织、文化与治理已有本地证据基线，但任何结论变化仍需经过消息流检验。",
    "Risk sweep has a local evidence baseline, but any thesis change still requires message-flow testing.": "风险排雷已有本地证据基线，但任何结论变化仍需经过消息流检验。",
    "Treat source and origin as partially evidenced for baseline work.": "源头溯源可作为部分证据基线使用。",
    "Treat company history as partially evidenced for baseline work.": "公司历史可作为部分证据基线使用。",
    "Treat current business as well evidenced for baseline work.": "当下生意可作为证据较充分的基线使用。",
    "Treat value chain position as well evidenced for baseline work.": "产业链定位可作为证据较充分的基线使用。",
    "Treat competitive landscape as well evidenced for baseline work.": "竞争格局可作为证据较充分的基线使用。",
    "Treat strategy analysis as well evidenced for baseline work.": "战略分析可作为证据较充分的基线使用。",
    "Treat organization, culture, and governance as partially evidenced for baseline work.": "组织、文化与治理可作为部分证据基线使用。",
    "Treat risk sweep as well evidenced for baseline work.": "风险排雷可作为证据较充分的基线使用。",
    "High-quality evidence can update the baseline, but only through linked assumptions and disconfirming tests.": "高质量证据可以更新基线，但必须通过关联假设和反证测试处理。",
    "Evidence seeds or refreshes the baseline; compare with prior period and consensus expectations before thesis change.": "该证据用于播种或刷新基线；改变结论前，需要与上一期数据和市场预期比较。",
    "Use as a research lead; require primary or high-reliability confirmation before changing thesis strength.": "仅作为研究线索；改变结论强度前，需要一手或高可靠证据确认。",
    "Potential negative update; test whether it is transient noise or structural baseline damage.": "潜在负面更新；需要检验这是短期噪音还是结构性基线受损。",
    "Update baseline, then test whether the change is already priced and durable.": "先更新基线，再检验变化是否已被定价且是否可持续。",
    "Escalate as a disconfirming test and search for primary follow-up evidence.": "提升为反证测试，并继续寻找一手后续证据。",
    "Queue for confirmation and attach to open questions; do not strengthen thesis from this item alone.": "进入待确认队列并挂到开放问题；不能仅凭该项强化结论。",
    "The phone base often feeds user scale, channels, services, and ecosystem attachment.": "手机基盘通常决定用户规模、渠道、服务变现和生态粘性。",
    "The same shipment decline has very different margin and ecosystem implications depending on cause.": "同样的出货下滑，原因不同，对毛利和生态价值的含义完全不同。",
    "IoT can be either a durable ecosystem layer or a capital-light-looking but low-return hardware mix.": "IoT 可能是可持续生态层，也可能只是看似轻资产但回报不高的硬件组合。",
    "Service margins can dominate profit quality even when revenue share is small.": "即便收入占比不高，服务毛利也可能主导集团利润质量。",
    "EV can re-rate the company or absorb cash and introduce safety liabilities.": "EV 既可能推动重估，也可能消耗现金并引入安全责任。",
    "EV growth can be value-accretive or value-destructive depending on post-launch unit economics.": "EV 增长是否创造价值，取决于上市初期之后的单车经济性。",
    "Input-cost and quality-control shocks can reverse margin and delivery narratives quickly.": "投入成本和质量控制冲击会快速逆转毛利与交付叙事。",
    "Capital allocation determines whether growth translates into per-share value.": "资本配置决定增长能否转化为每股价值。",
    "Control rights affect strategic patience, accountability, and valuation discount.": "控制权结构会影响战略耐心、问责机制和估值折价。",
    "Segment mix can hide whether growth improves or dilutes long-term returns.": "分部结构可能掩盖增长是在提升还是稀释长期回报。",
    "Share losses persist for two or more quarters": "份额连续两个或更多季度流失",
    "ASP and gross margin decline together": "ASP 与毛利率同时下降",
    "Inventory builds while shipments fall": "出货下降但库存上升",
    "Volume falls while inventory rises": "销量下降但库存增加",
    "Low-end mix deteriorates despite price cuts": "降价后低端机型结构仍恶化",
    "Growth requires discounts": "增长依赖折扣",
    "Gross margin falls as scale rises": "规模扩大但毛利率下降",
    "Connected-device users do not improve service monetization": "连接设备用户增长没有改善服务变现",
    "MAU growth slows while monetization falls": "MAU 增速放缓且变现下降",
    "Regulatory changes reduce ads or app distribution economics": "监管变化削弱广告或应用分发生态收益",
    "High-margin revenue mix shrinks": "高毛利收入占比收缩",
    "Vehicle gross margin falls after launch cycle": "上市初期后整车毛利率下降",
    "Price cuts outpace cost-down": "降价幅度超过降本幅度",
    "Recall, warranty, or safety costs rise faster than deliveries": "召回、质保或安全成本增速快于交付",
    "Gross margin falls with higher deliveries": "交付增加但毛利率下降",
    "Recall or warranty costs rise faster than revenue": "召回或质保成本增速快于收入",
    "BOM inflation cannot be passed through": "BOM 成本通胀无法传导",
    "Supply constraints reduce high-margin mix": "供给约束压低高毛利产品结构",
    "Quality incidents rise with production scale": "产量扩大时质量事件增加",
    "Free cash flow weakens despite reported profit": "会计利润增长但自由现金流转弱",
    "Capex rises without operating leverage": "资本开支上升但经营杠杆没有兑现",
    "Financing dilutes while returns remain unproven": "融资带来摊薄，但回报尚未证明",
    "Major capital allocation lacks minority-shareholder discipline": "重大资本配置缺乏少数股东约束",
    "Related-party risk increases": "关联交易风险上升",
    "Board independence weakens": "董事会独立性下降",
    "Revenue grows while cash conversion and margin quality weaken": "收入增长但现金转化和毛利质量下降",
    "One segment masks deterioration elsewhere": "单一分部增长掩盖其他业务恶化",
    "Quarterly shipments by region": "分区域季度出货",
    "ASP and gross margin bridge": "ASP 与毛利率桥接",
    "Channel inventory and component-cost commentary": "渠道库存和部件成本说明",
    "Shipments by price band": "分价格带出货",
    "Channel inventory": "渠道库存",
    "Component availability": "关键部件供给",
    "Category revenue and gross margin": "分品类收入和毛利率",
    "Multi-device user cohort retention": "多设备用户分群留存",
    "Attach-rate and repeat-purchase data": "附着率与复购数据",
    "MAU by region": "分区域 MAU",
    "ARPU and ad/gaming/service mix": "ARPU 与广告/游戏/服务结构",
    "Regulatory and platform policy updates": "监管和平台政策更新",
    "Deliveries, order backlog, and wait time": "交付、订单积压和等待周期",
    "Vehicle gross margin bridge": "整车毛利率桥接",
    "Warranty, recall, safety, and service-cost data": "质保、召回、安全和服务成本数据",
    "Warranty accrual": "质保计提",
    "Recall cost": "召回成本",
    "Price changes": "价格变化",
    "Key component pricing": "关键部件价格",
    "Inventory days": "库存天数",
    "Supplier concentration and capacity commitments": "供应商集中度和产能承诺",
    "Operating cash flow": "经营现金流",
    "Capex by business line": "分业务资本开支",
    "Buyback/dividend/financing decisions": "回购、分红和融资决策",
    "Voting-control disclosures": "投票权控制披露",
    "Board composition": "董事会构成",
    "Related-party and capital-allocation history": "关联交易和资本配置历史",
    "Segment revenue": "分部收入",
    "Segment gross profit": "分部毛利",
    "Operating cash flow and working-capital bridge": "经营现金流和营运资本桥接",
    "Need primary sources for founding context, original customer wedge, and company DNA.": "需要一手资料说明创立背景、原始客户切口和公司基因。",
    "Need dated milestones for business, governance, financing, M&A, and capital allocation.": "需要带日期的业务、治理、融资、并购和资本配置里程碑。",
    "Need segment revenue, customers, demand drivers, margins, and cash conversion evidence.": "需要分部收入、客户、需求驱动、利润率和现金转化证据。",
    "Need supplier, channel, customer, substitute, and bargaining-power evidence.": "需要供应商、渠道、客户、替代品和议价权证据。",
    "Need peer ranking, share trend, market structure, and competition-intensity evidence.": "需要同行排名、份额趋势、市场结构和竞争强度证据。",
    "Need mission, corporate strategy, competitive strategy, functional strategy, and resource allocation.": "需要使命、公司战略、竞争战略、职能战略和资源配置证据。",
    "Need leadership, incentives, ownership/control, board quality, and culture evidence.": "需要领导层、激励、所有权/控制权、董事会质量和文化证据。",
    "Need business, financial, accounting, legal, technology, capital-allocation, governance, and valuation risks.": "需要业务、财务、会计、法律、技术、资本配置、治理和估值风险证据。",
}

SECTION_LABEL_ZH = {
    "Source and origin": "源头溯源",
    "Company history": "公司历史",
    "Current business": "当下生意",
    "Value chain position": "产业链定位",
    "Competitive landscape": "竞争格局",
    "Strategy analysis": "战略分析",
    "Organization, culture, and governance": "组织、文化与治理",
    "Risk sweep": "风险排雷",
}

SECTION_ID_TO_PAGE = {
    "source_origin": "source_origin.html",
    "history": "history.html",
    "current_business": "current_business.html",
    "value_chain": "value_chain.html",
    "competition": "competition.html",
    "strategy": "strategy.html",
    "governance": "governance.html",
    "risk_sweep": "risk_sweep.html",
}

INFO_CATEGORY_ORDER = ["evidence", "research_report", "opinion", "message"]
SOURCE_ORIGIN_INFO_ORDER = ["evidence", "research_report", "message", "opinion"]
INFO_CATEGORY_LABEL_ZH = {
    "evidence": "证据",
    "research_report": "研报",
    "opinion": "观点",
    "message": "消息",
}
INFO_CATEGORY_EXPLANATION_ZH = {
    "evidence": "官方文件、财报、公告、监管文件等一手或准一手资料。",
    "research_report": "第三方研究报告、行业数据和结构化研究材料。",
    "opinion": "网上或特定个体观点，只能作为待验证角度。",
    "message": "公开发布但未证实或未充分交叉验证的信息。",
}
STANCE_LABEL_ZH = {
    "support": "支撑",
    "refute": "反证",
    "context": "补充背景",
    "lead": "研究线索",
}

SECTION_KEY_QUESTIONS = {
    "source_origin": [
        "公司为什么在那个时间点出现，原始痛点是什么？",
        "第一产品楔子、第一批用户和渠道切口是什么？",
        "创始团队的能力能否解释原始模型形成？",
        "早期基因今天是优势、约束，还是需要重新验证？",
    ],
    "history": [
        "公司历史中哪些节点真正改变了商业模型或资本配置？",
        "增长主要来自内生能力、并购扩张，还是周期/融资环境？",
        "历史上的战略转折有没有留下治理、财务或组织约束？",
    ],
    "current_business": [
        "当前收入、毛利、现金流分别由哪些业务驱动？",
        "客户是谁，需求来自刚需、替换、生态绑定还是促销？",
        "利润质量是否能转化为现金和可重复回报？",
    ],
    "value_chain": [
        "公司在产业链中掌握哪一段价值，哪一段被供应商/渠道/客户拿走？",
        "上游供给、关键部件和产能是否会改变毛利与交付？",
        "渠道和售后体系是否足以支撑当前业务复杂度？",
    ],
    "competition": [
        "公司真实竞争对手是谁，竞争发生在价格、产品、渠道还是生态？",
        "份额变化是结构性优势、周期波动，还是补贴/价格战结果？",
        "竞争强度是否会侵蚀毛利、现金流或品牌定位？",
    ],
    "strategy": [
        "公司战略是否从源头能力自然延伸，还是跨越了能力边界？",
        "资源配置是否与最重要利润池和风险点匹配？",
        "战略投入能否被 KPI 和阶段性证据验证？",
    ],
    "governance": [
        "创始人、控制权和管理层结构是否提升长期执行？",
        "激励、董事会和少数股东保护是否足以约束资本配置？",
        "组织文化是复利资产，还是会放大盲区和路径依赖？",
    ],
    "risk_sweep": [
        "哪些风险足以改变公司基础画像，而不只是短期噪音？",
        "财务、会计、法律、监管、技术和治理风险分别如何验证？",
        "哪类新增证据能最快证伪当前判断？",
    ],
}

L1_FRAMEWORK_QUESTIONS = {
    "source_origin": "源头溯源：公司是怎么来的",
    "history": "发展历史：公司的发展关键节点是什么",
    "current_business": "当下的生意：当前业务板块下探",
    "value_chain": "产业链定位：上下游分析",
    "competition": "竞争格局：真实竞争对手和竞争强度是什么",
    "strategy": "战略分析：过去、现在、未来",
    "governance": "组织管理：管理层、治理和组织能力分析",
    "risk_sweep": "风险暴露：哪些风险会改变基础画像",
}

SOURCE_NAME_ZH = {
    "Xiaomi IR Company Profile": "小米 IR 公司简介",
    "Xiaomi Global IR Prospectus Overview": "小米全球 IR 招股概要",
    "WIPO Xiaomi IP Advantage Case": "WIPO 小米创新案例",
    "Xiaomi 2021 Annual Report Hardware Margin Pledge": "小米 2021 年报硬件净利率承诺",
    "Xiaomi Corporation 2025 Annual Report": "小米集团 2025 年报",
    "Xiaomi Corporation 2025 Annual Results Announcement": "小米集团 2025 年度业绩公告",
    "Xiaomi IR Management": "小米 IR 管理层",
    "Xiaomi 2025 Annual Report WVR and Board Disclosure": "小米 2025 年报不同投票权与董事会披露",
    "Xiaomi IR Quarterly Results Page": "小米 IR 季度业绩页面",
    "Sina Xiaomi Phone Launch Transcript": "新浪科技小米手机发布会实录",
    "Jingzhun Research Xiaomi Deep Report 2018": "精准研究小米 2018 深度报告",
    "Guosheng Securities Xiaomi Deep Report 2021": "国盛证券小米 2021 深度报告",
    "Yongxing Securities Xiaomi Deep Report 2025": "甬兴证券小米 2025 深度报告",
    "Shenwan Hongyuan Xiaomi Deep Report Summary 2024": "申万宏源小米 2024 深度报告摘要",
    "IDC Smartphone Market Insights Q1 2026": "IDC 2026 Q1 智能手机市场数据",
    "Counterpoint Q1 2026 Smartphone Shipment Monitor via Gadgets360": "Counterpoint 2026 Q1 智能手机出货跟踪",
    "CnEVPost CPCA 2025 China NEV Share": "CnEVPost / 乘联会 2025 中国新能源车份额",
    "SAMR Xiaomi SU7 Recall Notice": "国家市场监督管理总局小米 SU7 召回公告",
    "Xiaomi Corporation 2018 Global Offering Prospectus": "小米集团 2018 全球发售招股书",
    "SEC XBRL Revenue": "SEC XBRL 收入",
    "SEC XBRL Net income": "SEC XBRL 净利润",
    "SEC XBRL Operating income": "SEC XBRL 经营利润",
    "SEC XBRL Gross profit": "SEC XBRL 毛利",
    "SEC XBRL Assets": "SEC XBRL 资产",
    "SEC XBRL Liabilities": "SEC XBRL 负债",
    "SEC XBRL Stockholders equity": "SEC XBRL 股东权益",
    "SEC XBRL Cash and cash equivalents": "SEC XBRL 现金及现金等价物",
}


@dataclass(frozen=True)
class ResearchSystemResult:
    ticker: str
    foundation_graph_path: str
    qa_tree_path: str
    question_graph_path: str
    message_flow_path: str
    dashboard_path: str
    foundation_status: str
    sections_covered: int
    questions: int
    messages: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "ticker": self.ticker,
            "foundation_graph_path": self.foundation_graph_path,
            "qa_tree_path": self.qa_tree_path,
            "question_graph_path": self.question_graph_path,
            "message_flow_path": self.message_flow_path,
            "dashboard_path": self.dashboard_path,
            "foundation_status": self.foundation_status,
            "sections_covered": self.sections_covered,
            "questions": self.questions,
            "messages": self.messages,
        }


def build_research_system(root: Path, ticker: str) -> dict[str, Any]:
    """Build the stock research operating-system layer from local evidence."""
    normalized = normalize_ticker(ticker)
    stock_dir = root / "stocks" / normalized
    if not stock_dir.exists():
        raise ValueError(f"stock folder not found: {stock_dir}")

    evidence = _load_evidence(stock_dir)
    research_dir = stock_dir / "research_system"
    research_dir.mkdir(parents=True, exist_ok=True)

    foundation_graph = _build_foundation_graph(normalized, evidence)
    qa_tree = _build_qa_tree(normalized, foundation_graph, evidence)
    question_rows: list[dict[str, Any]] = []
    message_rows: list[dict[str, Any]] = []

    foundation_path = research_dir / "foundation_graph.json"
    qa_tree_path = research_dir / "qa_tree.json"
    question_path = research_dir / "question_graph.jsonl"
    message_path = research_dir / "message_flow.jsonl"
    dashboard_path = research_dir / "research_dashboard.html"
    pages_dir = research_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    _write_json(foundation_path, foundation_graph)
    _write_json(qa_tree_path, qa_tree)
    _write_jsonl(question_path, question_rows)
    _write_jsonl(message_path, message_rows)
    _write_text(dashboard_path, _render_dashboard(normalized, foundation_graph, question_rows, message_rows, qa_tree))
    for section in foundation_graph["sections"]:
        page_name = SECTION_ID_TO_PAGE.get(section["id"], f"{section['id']}.html")
        page_html = _render_foundation_qa_page(normalized, foundation_graph, evidence, section["id"])
        _write_text(pages_dir / page_name, page_html)
        for node in _l2_nodes_for_section(qa_tree, section["id"]):
            l2_path = pages_dir / _l2_question_page_path(section["id"], node["id"])
            l2_path.parent.mkdir(parents=True, exist_ok=True)
            _write_text(l2_path, _render_l2_question_page(normalized, section, node, qa_tree, evidence))

    covered = sum(1 for section in foundation_graph["sections"] if section["status"] != "missing")
    RunLog(stock_dir / "logs").append(
        "research_system",
        RunStatus.SUCCESS,
        tickers=[normalized],
        records_fetched=len(evidence),
        records_new=len(foundation_graph["sections"]),
    )

    return ResearchSystemResult(
        ticker=normalized,
        foundation_graph_path=str(foundation_path),
        qa_tree_path=str(qa_tree_path),
        question_graph_path=str(question_path),
        message_flow_path=str(message_path),
        dashboard_path=str(dashboard_path),
        foundation_status=foundation_graph["foundation_status"],
        sections_covered=covered,
        questions=len(question_rows),
        messages=len(message_rows),
    ).to_dict()


def normalize_ticker(ticker: str) -> str:
    normalized = ticker.strip().upper()
    return TICKER_ALIASES.get(normalized, normalized)


def _load_evidence(stock_dir: Path) -> list[EvidenceRecord]:
    evidence_path = stock_dir / "evidence.jsonl"
    if not evidence_path.exists():
        return []

    records: list[EvidenceRecord] = []
    for line_number, line in enumerate(evidence_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(EvidenceRecord.from_dict(json.loads(line)))
        except (json.JSONDecodeError, ValidationError) as exc:
            raise ValueError(f"{evidence_path}:{line_number}: {exc}") from exc
    return records


def _build_foundation_graph(ticker: str, evidence: list[EvidenceRecord]) -> dict[str, Any]:
    sections = [_build_section(section, evidence) for section in FOUNDATION_SECTIONS]
    business_nodes = _detect_business_nodes(evidence)
    kpis = _build_kpis(evidence, business_nodes)
    assumptions = _build_assumptions(ticker, business_nodes, sections)
    risks = _build_risks(evidence, business_nodes, sections)

    missing = sum(1 for section in sections if section["status"] == "missing")
    evidenced = sum(1 for section in sections if section["status"] == "evidenced")
    if missing >= 3:
        foundation_status = "incomplete"
    elif missing or evidenced < len(sections):
        foundation_status = "research_ready_with_specific_gaps"
    else:
        foundation_status = "complete"

    return {
        "schema_version": "1.0",
        "ticker": ticker,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "foundation_status": foundation_status,
        "coverage": {
            "sections_total": len(sections),
            "sections_evidenced": evidenced,
            "sections_partial": sum(1 for section in sections if section["status"] == "partial"),
            "sections_missing": missing,
        },
        "sections": sections,
        "business_nodes": business_nodes,
        "kpis": kpis,
        "assumptions": assumptions,
        "risks": risks,
        "research_boundary": "Foundation graph is not a trading instruction. Message-flow work must test marginal change against this baseline.",
    }


def _build_qa_tree(ticker: str, foundation_graph: dict[str, Any], evidence: list[EvidenceRecord]) -> dict[str, Any]:
    """Build the interactive question tree used by foundation drill-down pages."""
    root_id = "company.foundation"
    section_question_nodes: list[dict[str, Any]] = []
    section_child_ids: dict[str, list[str]] = {}
    for section in foundation_graph.get("sections", []):
        child_nodes = _qa_nodes_for_section(ticker, section, evidence)
        section_question_nodes.extend(child_nodes)
        section_child_ids[section.get("id", "")] = [
            node["id"]
            for node in child_nodes
            if node.get("parent_id") == f"foundation.{section.get('id', '')}"
        ]

    section_nodes: list[dict[str, Any]] = []
    for section in foundation_graph.get("sections", []):
        section_id = section.get("id", "")
        node_id = f"foundation.{section_id}"
        section_nodes.append(
            {
                "id": node_id,
                "level": 1,
                "parent_id": root_id,
                "section_id": section_id,
                "question": _foundation_section_question(section),
                "current_answer": _foundation_section_answer(section),
                "evidence_buckets": _qa_buckets_from_section(section),
                "synthesis": _qa_synthesis_from_section(section),
                "rollup_to_parent": _foundation_section_rollup(section),
                "next_question_ids": section_child_ids.get(section_id, []),
                "status": section.get("status", "missing"),
            }
        )

    nodes = [
        {
            "id": root_id,
            "level": 0,
            "parent_id": None,
            "section_id": "foundation",
            "question": "这家公司应该先用哪组基础问题建立认知？",
            "current_answer": "先用八步框架建立公司基础画像，再对每个板块逐层下钻；所有结论必须能回到证据、研报、消息和观点四类信息。",
            "evidence_buckets": _qa_empty_buckets(),
            "synthesis": {
                "facts": [],
                "inferences": ["八步框架是最外层问题集合，不是最终报告结构。"],
                "judgment": "当前系统默认用三层问题树承载研究：八步框架、板块重点问题、进一步下钻问题。",
                "gaps": ["交互追问目前先作为本地问题节点草稿，后续需要接入证据搜索和持久化更新。"],
                "confidence": "medium",
            },
            "rollup_to_parent": "",
            "next_question_ids": [node["id"] for node in section_nodes],
            "status": foundation_graph.get("foundation_status", "incomplete"),
        },
        *section_nodes,
        *section_question_nodes,
    ]
    return {
        "schema_version": "1.0",
        "ticker": ticker,
        "generated_at": foundation_graph.get("generated_at"),
        "default_depth": 3,
        "default_active_node_id": "foundation.history",
        "interaction_contract": {
            "node_model": "Every research step is a question node with parent, level, evidence buckets, synthesis, rollup, and next questions.",
            "information_categories": SOURCE_ORIGIN_INFO_ORDER,
            "new_question_behavior": "Attach a new question to the active node, then search evidence and update synthesis before rolling conclusions up to the parent.",
        },
        "nodes": nodes,
    }


def _l2_nodes_for_section(qa_tree: dict[str, Any], section_id: str) -> list[dict[str, Any]]:
    parent_id = f"foundation.{section_id}"
    return [
        node
        for node in qa_tree.get("nodes", [])
        if node.get("section_id") == section_id and node.get("parent_id") == parent_id and node.get("level") == 2
    ]


def _l2_question_page_path(section_id: str, node_id: str) -> Path:
    return Path(section_id) / f"{_safe_id(node_id)}.html"


def _l2_question_href(section_id: str, node_id: str) -> str:
    return str(_l2_question_page_path(section_id, node_id)).replace("\\", "/")


SECTION_QA_PARENT_IDS = {
    "current_business": ["profit-cash", "customer-demand", "profit-quality"],
    "value_chain": ["value-capture", "supply-constraint", "channel-service"],
    "competition": ["real-peers", "share-quality", "competition-intensity"],
    "strategy": ["capability-boundary", "resource-allocation", "kpi-validation"],
    "governance": ["founder-control", "capital-discipline", "culture-blindspot"],
    "risk_sweep": ["material-risk", "risk-verification", "falsification-trigger"],
}

SECTION_QA_DRILLDOWNS = {
    "current_business": {
        "profit-cash": [
            ("segment-profit-pool", "哪个业务真正贡献毛利和现金，而不只是贡献收入？", "需要分部毛利、费用分摊、经营现金流和营运资本桥接。"),
            ("ev-unit-economics", "EV/AI 新业务的单车经济是否已经足以单独成立？", "需要单车收入、单车毛利、质保计提、售后成本和价格调整。"),
        ],
        "customer-demand": [
            ("demand-source", "需求来自真实替换/生态绑定，还是促销与新品周期？", "需要订单、等待周期、库存、价格变化和用户留存数据。"),
            ("user-entry", "手机入口变化是否影响 IoT 和互联网服务变现？", "需要手机份额、MIUI MAU、多设备用户和服务 ARPU。"),
        ],
        "profit-quality": [
            ("cash-conversion", "利润能否稳定转化为现金？", "需要经营现金流、应收应付、库存和资本开支桥接。"),
            ("margin-sustainability", "高毛利业务的持续性来自结构优势还是阶段性周期？", "需要分业务毛利率、价格、成本和行业周期对照。"),
        ],
    },
    "value_chain": {
        "value-capture": [
            ("supplier-power", "上游供应商是否拿走关键经济性？", "需要关键部件价格、供应商集中度、账期和采购承诺。"),
            ("customer-channel-power", "渠道、客户和售后体系是否侵蚀利润？", "需要渠道结构、营销费用、售后网络和退换/维修成本。"),
        ],
        "supply-constraint": [
            ("component-bottleneck", "关键部件短缺或涨价会不会改变交付和毛利？", "需要内存、芯片、电池、座舱和智能驾驶硬件价格数据。"),
            ("capacity-quality", "产能爬坡是否会带来质量和成本压力？", "需要产能利用率、交付周期、缺陷率、召回和质保数据。"),
        ],
        "channel-service": [
            ("offline-service", "线下渠道和售后能力是否匹配汽车业务复杂度？", "需要门店、服务中心、维修能力和用户投诉数据。"),
            ("inventory-risk", "库存和渠道压货是否会掩盖真实需求？", "需要库存天数、渠道库存、价格折扣和出货/零售差异。"),
        ],
    },
    "competition": {
        "real-peers": [
            ("phone-peer-map", "手机业务到底和谁竞争，竞争维度是什么？", "需要全球和区域份额、价格带、产品周期和渠道数据。"),
            ("ev-peer-map", "EV 业务的真实竞品是传统车企、新势力还是生态型科技公司？", "需要价格带、车型定位、交付、毛利和智能化能力对照。"),
        ],
        "share-quality": [
            ("share-vs-profit", "份额增长是否伴随利润质量改善？", "需要份额、ASP、毛利率、补贴和库存数据。"),
            ("regional-mix", "份额变化来自区域结构、产品结构还是真实竞争力？", "需要中国、印度、欧洲等区域拆分和价格带数据。"),
        ],
        "competition-intensity": [
            ("price-war", "价格战是否会持续压缩毛利和现金流？", "需要竞品价格、促销、BOM 成本和毛利弹性。"),
            ("brand-position", "品牌定位能否支撑中高端化，而不是只靠性价比？", "需要高端机占比、复购、用户画像和价格带份额。"),
        ],
    },
    "strategy": {
        "capability-boundary": [
            ("transferable-capability", "哪些能力能从手机/AIoT 迁移到汽车？", "需要用户体验、软件、生态连接、渠道和品牌流量证据。"),
            ("new-capability", "哪些能力必须重新建设，不能从旧业务外推？", "需要制造、质量、安全、售后、监管和供应链证据。"),
        ],
        "resource-allocation": [
            ("capital-priority", "资源是否投向最重要利润池和最大约束点？", "需要研发、资本开支、人员、产能和营销投入拆分。"),
            ("cash-discipline", "战略投入是否会削弱现金回报和少数股东经济性？", "需要自由现金流、回购/分红、融资和股权激励数据。"),
        ],
        "kpi-validation": [
            ("stage-kpi", "每个战略阶段应该用哪些 KPI 验证？", "需要交付、毛利、MAU、多设备用户、服务 ARPU 和质量成本。"),
            ("trigger-map", "什么数据触发战略判断上修或下修？", "需要季度业绩、交付、价格调整、监管公告和份额变化。"),
        ],
    },
    "governance": {
        "founder-control": [
            ("patient-capital", "创始人控制权是否带来长期战略耐心？", "需要长期投入、产品周期、研发和重大项目复盘。"),
            ("minority-risk", "控制权是否放大少数股东治理折价？", "需要 WVR、董事会、关联交易和重大投资披露。"),
        ],
        "capital-discipline": [
            ("approval-constraint", "重大资本配置是否有足够约束？", "需要董事会审批、投资回报披露、回购分红和融资记录。"),
            ("incentive-alignment", "激励机制是否和每股价值创造一致？", "需要股权激励、考核指标、摊薄和管理层持股。"),
        ],
        "culture-blindspot": [
            ("complexity-management", "组织是否能处理手机、IoT、服务和汽车的复杂度？", "需要管理层分工、汽车团队、质量体系和跨业务协同。"),
            ("path-dependence", "早期互联网效率文化是否会在汽车业务上形成盲区？", "需要安全、质量、售后和监管响应案例。"),
        ],
    },
    "risk_sweep": {
        "material-risk": [
            ("phone-base-risk", "手机基本盘弱化是否会改变整个生态基础？", "需要连续季度份额、出货、ASP、毛利和库存。"),
            ("ev-safety-risk", "EV 安全、召回和质保风险是否会改变转型质量？", "需要召回、事故、投诉、质保计提和保险成本。"),
        ],
        "risk-verification": [
            ("financial-risk", "资本开支和营运资本是否会压低现金回报？", "需要自由现金流、现金资源、债务、资本开支和库存。"),
            ("regulatory-risk", "监管、数据、安全和产品责任风险如何验证？", "需要监管公告、诉讼、召回、处罚和整改进度。"),
        ],
        "falsification-trigger": [
            ("fastest-trigger", "哪类新增证据最快证伪当前基础判断？", "需要价格、份额、交付、毛利、召回和现金流触发器。"),
            ("monitoring-cadence", "这些风险应该按什么频率更新？", "需要季度业绩、月度交付、监管公告和行业数据更新节奏。"),
        ],
    },
}


def _qa_nodes_for_section(ticker: str, section: dict[str, Any], evidence: list[EvidenceRecord]) -> list[dict[str, Any]]:
    section_id = section.get("id", "")
    parent_node_id = f"foundation.{section_id}"
    questions = _qa_parent_questions_for_section(ticker, section)
    drilldowns = _qa_drilldowns_for_section(ticker, section, questions)
    nodes: list[dict[str, Any]] = []
    for question in questions:
        node_id = f"{section_id}.{question['id']}"
        child_ids = [f"{node_id}.{child['id']}" for child in drilldowns.get(question["id"], [])]
        nodes.append(_qa_node_from_question(node_id, 2, parent_node_id, section_id, question, evidence, child_ids))
        for child in drilldowns.get(question["id"], []):
            child_node_id = f"{node_id}.{child['id']}"
            nodes.append(_qa_node_from_question(child_node_id, 3, node_id, section_id, child, evidence, []))
    return nodes


def _qa_parent_questions_for_section(ticker: str, section: dict[str, Any]) -> list[dict[str, Any]]:
    section_id = section.get("id", "")
    if section_id == "source_origin":
        return _source_origin_questions(ticker)
    if section_id == "history":
        return _history_questions(ticker)

    questions: list[dict[str, Any]] = []
    ids = SECTION_QA_PARENT_IDS.get(section_id, [])
    for index, question_text in enumerate(section.get("key_questions", []), start=1):
        question_id = ids[index - 1] if index <= len(ids) else f"q{index}"
        rows = _section_rows_for_question(section, question_text)
        info = _info_from_section_rows(rows)
        questions.append(
            {
                "id": question_id,
                "question": question_text,
                "answer": _section_question_answer(section, question_text, rows),
                "gap": _section_question_gap(section, question_text, rows),
                "rollup": _section_question_rollup(section, rows),
                "confidence": _section_question_confidence(rows),
                "status": "open" if rows else "needs_data",
                "info": info,
            }
        )
    return questions


def _qa_drilldowns_for_section(
    ticker: str,
    section: dict[str, Any],
    questions: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    section_id = section.get("id", "")
    if section_id == "history":
        return _history_drilldown_questions(ticker)
    if section_id == "source_origin":
        return _source_origin_drilldown_questions(ticker, questions)

    drilldowns: dict[str, list[dict[str, Any]]] = {}
    blueprints = SECTION_QA_DRILLDOWNS.get(section_id, {})
    for question in questions:
        parent_info = question.get("info", _qa_empty_buckets())
        rows = []
        for category in SOURCE_ORIGIN_INFO_ORDER:
            rows.extend(parent_info.get(category, []))
        child_questions: list[dict[str, Any]] = []
        for child_id, child_question, child_gap in blueprints.get(question["id"], []):
            child_questions.append(
                {
                    "id": child_id,
                    "question": child_question,
                    "answer": _child_question_answer(question, child_question, rows),
                    "gap": child_gap,
                    "rollup": _child_question_rollup(child_question),
                    "confidence": "medium" if rows else "low",
                    "status": "open" if rows else "needs_data",
                    "info": parent_info,
                }
            )
        drilldowns[question["id"]] = child_questions
    return drilldowns


def _source_origin_drilldown_questions(ticker: str, questions: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    drilldowns: dict[str, list[dict[str, Any]]] = {}
    for question in questions:
        proof_rollup = _source_origin_primary_proof_rollup(question)
        boundary_rollup = _source_origin_boundary_rollup(question)
        drilldowns[question["id"]] = [
            {
                "id": "primary-proof",
                "question": "这个回答最需要哪条一手证据验证？",
                "answer": proof_rollup,
                "gap": question.get("gap", "需要补充一手证据。"),
                "rollup": proof_rollup,
                "confidence": question.get("confidence", "medium"),
                "status": "open",
                "info": question.get("info", _qa_empty_buckets()),
            },
            {
                "id": "today-boundary",
                "question": "这个源头基因今天还能解释什么，不能解释什么？",
                "answer": boundary_rollup,
                "gap": "需要把早期能力逐项映射到今天的业务节点和反证条件。",
                "rollup": boundary_rollup,
                "confidence": "medium",
                "status": "open",
                "info": question.get("info", _qa_empty_buckets()),
            },
        ]
    return drilldowns


def _source_origin_primary_proof_rollup(question: dict[str, Any]) -> str:
    ids = _question_info_ids(question, ("evidence", "message"))
    if ids:
        return f"当前回答优先由 {', '.join(ids[:3])} 验证；仍需确认这些材料能直接证明问题起点，而不是事后叙事。"
    return "当前回答还没有一手证据锚定，不能向上形成稳定公司基因判断。"


def _source_origin_boundary_rollup(question: dict[str, Any]) -> str:
    answer = _truncate_text(question.get("answer", ""), 100)
    if answer:
        return f"该源头问题向上提供的能力边界是：{answer}"
    return "源头溯源的输出不是故事，而是后续业务分析的能力边界。"


def _question_info_ids(question: dict[str, Any], categories: tuple[str, ...]) -> list[str]:
    ids: list[str] = []
    for category in categories:
        for item in question.get("info", {}).get(category, []):
            evidence_id = item.get("evidence_id", "")
            if evidence_id and evidence_id not in ids:
                ids.append(evidence_id)
    return ids


def _section_rows_for_question(section: dict[str, Any], question_text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for category in SOURCE_ORIGIN_INFO_ORDER:
        for row in section.get("information_by_category", {}).get(category, []):
            if row.get("linked_question") == question_text:
                rows.append(row)
    if rows:
        return rows

    for category in SOURCE_ORIGIN_INFO_ORDER:
        rows.extend(section.get("information_by_category", {}).get(category, []))
    return rows[:4]


def _info_from_section_rows(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, str]]]:
    info: dict[str, list[dict[str, str]]] = _qa_empty_buckets()
    for row in rows:
        category = row.get("source_category") or row.get("information_category")
        if category not in info:
            category = row.get("category")
        if category not in info:
            category = "evidence"
        info[category].append(
            _foundation_info(
                row.get("evidence_id", ""),
                STANCE_LABEL_ZH.get(row.get("stance", ""), row.get("stance", "信息")),
                _section_row_point(row),
            )
        )
    return info


def _section_row_point(row: dict[str, Any]) -> str:
    point = row.get("claim") or row.get("summary", "")
    for prefix in ("支撑：", "反证：", "待验证线索：", "补充背景："):
        if point.startswith(prefix):
            return point[len(prefix) :]
    return point


def _section_question_answer(section: dict[str, Any], question_text: str, rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "当前证据不足，先保持开放问题，不向上一层输出稳定判断。"
    support = [row for row in rows if row.get("stance") == "support"]
    refute = [row for row in rows if row.get("stance") == "refute"]
    leads = [row for row in rows if row.get("stance") == "lead"]
    first = rows[0]
    evidence_phrase = f"当前已映射 {len(rows)} 条信息"
    if refute:
        return f"{evidence_phrase}，其中存在反证或边界条件；本问题不能只按正向叙事处理，需要优先验证：{_zh_text(refute[0].get('summary', refute[0].get('claim', '')))}"
    if support:
        return f"{evidence_phrase}，正向证据主要支持该问题已有基础判断；但仍需把事实拆到具体 KPI 和业务节点。核心证据是：{_zh_text(first.get('summary', first.get('claim', '')))}"
    if leads:
        return f"{evidence_phrase}，但主要是研究线索，不能单独强化结论；需要寻找一手或高可靠证据确认。"
    return f"{evidence_phrase}，可作为背景信息，但还不足以形成强判断。"


def _section_question_gap(section: dict[str, Any], question_text: str, rows: list[dict[str, Any]]) -> str:
    if not rows:
        return section.get("gaps", [f"需要补充能直接回答“{question_text}”的一手资料。"])[0]
    if any(row.get("stance") == "refute" for row in rows):
        return "需要补充反证后的量化影响、持续时间、管理层应对和后续更新触发器。"
    if any(row.get("stance") == "lead" for row in rows):
        return "需要把研究线索升级为一手证据或高可靠第三方数据。"
    return "需要补充时间序列、同业对照和分业务 KPI，避免只停留在单点事实。"


def _section_question_rollup(section: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    section_label = SECTION_LABEL_ZH.get(section.get("label", ""), section.get("label", "本板块"))
    if not rows:
        return f"{section_label}还不能向上一层输出稳定结论。"
    if any(row.get("stance") == "refute" for row in rows):
        return f"{section_label}存在需要优先处理的反证或边界条件。"
    return f"{section_label}已有可用研究起点，但上抛结论仍需经过下钻问题验证。"


def _section_question_confidence(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "low"
    if any(row.get("reliability") in {"primary", "high"} for row in rows):
        return "medium"
    return "low"


def _child_question_answer(parent: dict[str, Any], child_question: str, rows: list[dict[str, Any]]) -> str:
    if rows:
        return f"该问题从父节点证据出发继续下钻。当前不能直接合并为结论，需要单独补充能回答“{child_question}”的数据。"
    return "该下钻问题还没有专门证据，先作为下一轮信息搜集任务。"


def _child_question_rollup(child_question: str) -> str:
    return f"完成“{child_question}”后，再决定是否修正父问题判断。"


def _foundation_section_question(section: dict[str, Any]) -> str:
    labels = {
        "source_origin": "源头溯源：公司为什么出现，原始问题是什么？",
        "history": "公司历史：哪些节点真正改变了商业模型、治理或资本配置？",
        "current_business": "当下生意：公司今天靠什么赚钱，利润和现金流质量如何？",
        "value_chain": "产业链定位：公司在哪些环节捕获或丢失经济性？",
        "competition": "竞争格局：公司真实竞争地位和竞争强度如何？",
        "strategy": "战略分析：战略是否沿着能力边界扩展，并能被数据验证？",
        "governance": "组织、文化与治理：控制权、激励和组织能力是否支持长期复利？",
        "risk_sweep": "风险排雷：哪些风险足以改变公司基础画像？",
    }
    return labels.get(section.get("id", ""), SECTION_LABEL_ZH.get(section.get("label", ""), section.get("label", "")))


def _foundation_section_answer(section: dict[str, Any]) -> str:
    facts = section.get("facts", [])
    if facts:
        return _zh_text(facts[0].get("statement", ""))
    gaps = section.get("gaps", [])
    if gaps:
        return _zh_text(gaps[0])
    return "当前证据不足，需要先补充一手或高可靠信息。"


def _foundation_section_rollup(section: dict[str, Any]) -> str:
    facts = [
        _zh_text(fact.get("statement", ""))
        for fact in section.get("facts", [])
        if fact.get("statement")
    ]
    if facts:
        return "；".join(_truncate_text(fact, 110) for fact in facts[:2])
    inferences = [_zh_text(item) for item in section.get("inferences", []) if item]
    if inferences:
        return "；".join(_truncate_text(item, 110) for item in inferences[:2])
    judgments = section.get("judgments", [])
    if judgments:
        return _zh_text(judgments[0])
    return "该板块尚不能向上一层输出稳定结论。"


def _qa_synthesis_from_section(section: dict[str, Any]) -> dict[str, Any]:
    return {
        "facts": [
            f"{_zh_text(fact.get('statement', ''))} [{fact.get('evidence_id', '')}]"
            for fact in section.get("facts", [])
        ],
        "inferences": [_zh_text(item) for item in section.get("inferences", [])],
        "judgment": _zh_text(section.get("judgments", [""])[0]) if section.get("judgments") else "",
        "gaps": [_zh_text(item) for item in section.get("gaps", [])],
        "confidence": "high" if section.get("status") == "evidenced" else "medium" if section.get("status") == "partial" else "low",
    }


def _qa_buckets_from_section(section: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    buckets = _qa_empty_buckets()
    groups = section.get("information_by_category", {})
    for category in SOURCE_ORIGIN_INFO_ORDER:
        for row in groups.get(category, []):
            buckets[category].append(
                {
                    "evidence_id": row.get("evidence_id", ""),
                    "relation": STANCE_LABEL_ZH.get(row.get("stance", ""), row.get("stance", "")),
                    "point": row.get("claim", ""),
                    "source_name": SOURCE_NAME_ZH.get(row.get("source_name", ""), row.get("source_name", "")),
                    "url": row.get("url", ""),
                    "summary": _zh_text(row.get("summary", "")),
                    "reliability": row.get("reliability", ""),
                    "materiality": row.get("materiality", ""),
                }
            )
    return buckets


def _qa_node_from_question(
    node_id: str,
    level: int,
    parent_id: str,
    section_id: str,
    question: dict[str, Any],
    evidence: list[EvidenceRecord],
    child_ids: list[str],
) -> dict[str, Any]:
    facts = _qa_fact_lines(question)
    return {
        "id": node_id,
        "level": level,
        "parent_id": parent_id,
        "section_id": section_id,
        "question": question["question"],
        "current_answer": question["answer"],
        "evidence_buckets": _qa_buckets_from_question(question, evidence),
        "synthesis": {
            "facts": facts,
            "inferences": [question["answer"]],
            "judgment": question.get("rollup", question["answer"]),
            "gaps": [question["gap"]],
            "confidence": question.get("confidence", "medium"),
        },
        "rollup_to_parent": question.get("rollup", question["answer"]),
        "next_question_ids": child_ids,
        "status": question.get("status", "open"),
    }


def _qa_fact_lines(question: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for items in question.get("info", {}).values():
        for item in items:
            lines.append(f"{item.get('relation', '信息')}：{item.get('point', '')} [{item.get('evidence_id', '')}]")
    return lines


def _qa_buckets_from_question(question: dict[str, Any], evidence: list[EvidenceRecord]) -> dict[str, list[dict[str, Any]]]:
    buckets = _qa_empty_buckets()
    by_id = {record.id: record for record in evidence}
    for category in SOURCE_ORIGIN_INFO_ORDER:
        for item in question.get("info", {}).get(category, []):
            record = by_id.get(item.get("evidence_id", ""))
            if record is None:
                buckets[category].append(_unresolved_question_info_item(item))
            else:
                buckets[category].append(
                    {
                        "evidence_id": record.id,
                        "relation": item.get("relation", ""),
                        "point": item.get("point", ""),
                        "source_name": SOURCE_NAME_ZH.get(record.source_name, record.source_name),
                        "url": record.url,
                        "summary": _zh_text(record.summary),
                        "reliability": record.reliability,
                        "materiality": record.materiality,
                        "missing_record": False,
                    }
                )
    return buckets


def _qa_empty_buckets() -> dict[str, list[dict[str, Any]]]:
    return {category: [] for category in SOURCE_ORIGIN_INFO_ORDER}


def _unresolved_question_info_item(item: dict[str, Any]) -> dict[str, Any]:
    evidence_id = item.get("evidence_id", "")
    return {
        "evidence_id": evidence_id,
        "relation": item.get("relation", ""),
        "point": item.get("point", ""),
        "source_name": f"待补入库：{evidence_id}" if evidence_id else "待补入库",
        "url": "",
        "summary": "该信息索引已在研究问题中声明，但本地 evidence.jsonl 尚未找到完整来源记录。",
        "reliability": "unresolved",
        "materiality": "unknown",
        "missing_record": True,
    }


def _build_section(section_rule: dict[str, Any], evidence: list[EvidenceRecord]) -> dict[str, Any]:
    evidence_ids = _evidence_ids_for_keywords(evidence, section_rule["keywords"])
    status = _coverage_status(evidence_ids)
    summaries = _summaries_for_ids(evidence, evidence_ids, limit=4)
    key_questions = SECTION_KEY_QUESTIONS.get(section_rule["id"], [])
    facts = [
        {
            "statement": summary,
            "evidence_id": evidence_id,
        }
        for evidence_id, summary in summaries
    ]
    if status == "missing":
        inferences: list[str] = []
        judgments = ["Do not use this section to strengthen a thesis until primary or high-reliability evidence is added."]
        gaps = [section_rule["default_gap"]]
    else:
        inferences = [
            f"{section_rule['label']} has a local evidence baseline, but any thesis change still requires message-flow testing."
        ]
        judgments = [
            f"Treat {section_rule['label'].lower()} as {'well evidenced' if status == 'evidenced' else 'partially evidenced'} for baseline work."
        ]
        gaps = [] if status == "evidenced" else [f"Add at least one more independent source for {section_rule['label'].lower()}."]

    page_name = SECTION_ID_TO_PAGE.get(section_rule["id"], f"{section_rule['id']}.html")
    return {
        "id": section_rule["id"],
        "label": section_rule["label"],
        "status": status,
        "evidence_ids": evidence_ids,
        "detail_page": f"pages/{page_name}",
        "key_questions": key_questions,
        "information_by_category": _section_information_by_category(section_rule, evidence, evidence_ids, key_questions),
        "facts": facts,
        "inferences": inferences,
        "judgments": judgments,
        "gaps": gaps,
    }


def _coverage_status(evidence_ids: list[str]) -> str:
    if len(evidence_ids) >= 2:
        return "evidenced"
    if len(evidence_ids) == 1:
        return "partial"
    return "missing"


def _section_information_by_category(
    section_rule: dict[str, Any],
    evidence: list[EvidenceRecord],
    evidence_ids: list[str],
    key_questions: list[str],
) -> dict[str, list[dict[str, Any]]]:
    by_id = {record.id: record for record in evidence}
    rows: dict[str, list[dict[str, Any]]] = {category: [] for category in INFO_CATEGORY_ORDER}
    for evidence_id in evidence_ids:
        record = by_id.get(evidence_id)
        if record is None:
            continue
        category = record.information_category
        rows.setdefault(category, []).append(
            {
                "evidence_id": record.id,
                "information_category": category,
                "source_name": record.source_name,
                "source_type": record.source_type,
                "url": record.url,
                "summary": record.summary,
                "reliability": record.reliability,
                "materiality": record.materiality,
                "stance": _information_stance(record),
                "linked_question": _linked_section_question(section_rule["id"], record, key_questions),
                "claim": _section_claim(section_rule["id"], record),
                "explanation": _information_explanation(section_rule["id"], record),
            }
        )
    return rows


def _information_stance(record: EvidenceRecord) -> str:
    text = _record_text(record)
    if record.information_category in {"opinion", "message"} or record.reliability == "low":
        return "lead"
    if _matches_any(text, ["recall", "decline", "decrease", "loss", "risk", "safety", "liability", "pressure", "shortage"]):
        return "refute"
    if record.information_category in {"evidence", "research_report"}:
        return "support"
    return "context"


def _linked_section_question(section_id: str, record: EvidenceRecord, key_questions: list[str]) -> str:
    if not key_questions:
        return "该板块需要先定义关键问题。"
    text = _record_text(record)
    if section_id == "risk_sweep":
        return key_questions[-1]
    if _matches_any(text, ["recall", "risk", "safety", "governance", "wvr", "control"]):
        return key_questions[-1]
    if _matches_any(text, ["revenue", "gross profit", "cash", "margin", "profit"]):
        return key_questions[0]
    if len(key_questions) > 1 and _matches_any(text, ["share", "rank", "competition", "shipment", "peer"]):
        return key_questions[1]
    return key_questions[0]


def _section_claim(section_id: str, record: EvidenceRecord) -> str:
    claims = {
        "source_origin": "公司源头基因是否能解释今天的业务结构和能力边界。",
        "history": "关键历史节点是否改变了公司的商业模型、治理结构或资本配置。",
        "current_business": "当前生意是否具备可重复的收入、利润和现金转化质量。",
        "value_chain": "公司是否在产业链中占据能持续捕获经济性的环节。",
        "competition": "竞争地位是否足以抵抗价格战、份额流失和利润率压缩。",
        "strategy": "战略投入是否沿着公司能力边界扩展，并能被阶段性数据验证。",
        "governance": "管理层、控制权和激励结构是否提升长期复利而非放大治理折价。",
        "risk_sweep": "当前风险是否足以改变基础画像或成为反证条件。",
    }
    base_claim = claims.get(section_id, "该信息是否改变本板块的基础判断。")
    if _information_stance(record) == "refute":
        return f"反证：{base_claim}"
    if _information_stance(record) == "lead":
        return f"待验证线索：{base_claim}"
    return f"支撑：{base_claim}"


def _information_explanation(section_id: str, record: EvidenceRecord) -> str:
    category = INFO_CATEGORY_LABEL_ZH.get(record.information_category, record.information_category)
    stance = STANCE_LABEL_ZH.get(_information_stance(record), _information_stance(record))
    return f"{category}信息当前被标记为“{stance}”，用于回答本板块问题；改变判断前仍需回到原文链接和证据质量。"


def _detect_business_nodes(evidence: list[EvidenceRecord]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    for rule in BUSINESS_NODE_RULES:
        evidence_ids = _evidence_ids_for_keywords(evidence, rule["keywords"])
        if not evidence_ids:
            continue
        nodes.append(
            {
                "id": rule["id"],
                "label": rule["label"],
                "role": rule["role"],
                "evidence_ids": evidence_ids,
                "key_kpis": rule["kpis"],
                "status": "active",
                "open_question": _main_question_for_node(rule["id"], rule["label"]),
            }
        )

    if not nodes:
        nodes.append(
            {
                "id": "core_business",
                "label": "Core business",
                "role": "Fallback node until business-line evidence is added",
                "evidence_ids": [record.id for record in evidence],
                "key_kpis": ["revenue", "margin", "cash conversion", "competitive position"],
                "status": "needs_mapping",
                "open_question": "What are the actual business lines, profit pools, and constraints?",
            }
        )
    return nodes


def _build_kpis(evidence: list[EvidenceRecord], business_nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    business_by_evidence: dict[str, list[str]] = {}
    for node in business_nodes:
        for evidence_id in node["evidence_ids"]:
            business_by_evidence.setdefault(evidence_id, []).append(node["id"])

    kpis: list[dict[str, Any]] = []
    for record in evidence:
        snippets = _numeric_snippets(record.summary)
        if not snippets:
            continue
        for index, snippet in enumerate(snippets[:4], start=1):
            kpis.append(
                {
                    "id": f"kpi_{_safe_id(record.id)}_{index}",
                    "label": _kpi_label(record),
                    "value_snippet": snippet,
                    "evidence_id": record.id,
                    "business_node_ids": business_by_evidence.get(record.id, []),
                    "reliability": record.reliability,
                    "why_it_matters": _kpi_why(record),
                }
            )
    return kpis


def _build_assumptions(ticker: str, business_nodes: list[dict[str, Any]], sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    assumptions: list[dict[str, Any]] = []
    for node in business_nodes:
        assumptions.append(
            {
                "id": f"assumption_{node['id']}_001",
                "ticker": ticker,
                "statement": _assumption_for_node(node["id"], node["label"]),
                "linked_business_node_ids": [node["id"]],
                "linked_foundation_sections": _sections_for_node(node["id"]),
                "supporting_evidence_ids": node["evidence_ids"][:5],
                "disconfirming_signals": _disconfirming_signals_for_node(node["id"]),
                "status": "open",
            }
        )

    for section in sections:
        if section["status"] == "missing":
            assumptions.append(
                {
                    "id": f"assumption_gap_{section['id']}",
                    "ticker": ticker,
                    "statement": f"{section['label']} is not research-ready because local evidence is missing.",
                    "linked_business_node_ids": [],
                    "linked_foundation_sections": [section["id"]],
                    "supporting_evidence_ids": [],
                    "disconfirming_signals": [section["gaps"][0]],
                    "status": "needs_data",
                }
            )
    return assumptions


def _build_risks(
    evidence: list[EvidenceRecord],
    business_nodes: list[dict[str, Any]],
    sections: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    risk_rows: list[dict[str, Any]] = []
    for record in evidence:
        text = _record_text(record)
        if not _matches_any(text, ["risk", "recall", "decline", "decrease", "loss", "debt", "liability", "regulator", "safety"]):
            continue
        risk_rows.append(
            {
                "id": f"risk_{_safe_id(record.id)}",
                "statement": _risk_statement(record),
                "evidence_id": record.id,
                "severity": "high" if record.materiality in {"high", "thesis_change"} else "medium",
                "linked_business_node_ids": [
                    node["id"] for node in business_nodes if record.id in node.get("evidence_ids", [])
                ],
                "monitoring_tests": _risk_monitoring_tests(record),
            }
        )

    for section in sections:
        if section["status"] == "missing":
            risk_rows.append(
                {
                    "id": f"risk_missing_{section['id']}",
                    "statement": f"{section['label']} lacks local evidence; conclusions that depend on it should stay needs_review.",
                    "evidence_id": None,
                    "severity": "medium",
                    "linked_business_node_ids": [],
                    "monitoring_tests": section["gaps"],
                }
            )
    return risk_rows


def _build_question_graph(ticker: str, foundation_graph: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for node in foundation_graph["business_nodes"]:
        parent_id = f"q_{ticker.lower()}_{node['id']}_main"
        assumption_ids = _assumption_ids_for_node(foundation_graph["assumptions"], node["id"])
        rows.append(
            {
                "id": parent_id,
                "ticker": ticker,
                "level": 0,
                "parent_id": None,
                "priority": "P0",
                "status": "open",
                "question": _main_question_for_node(node["id"], node["label"]),
                "why_it_matters": _why_question_matters(node["id"]),
                "linked_foundation_sections": _sections_for_node(node["id"]),
                "linked_business_node_ids": [node["id"]],
                "linked_assumption_ids": assumption_ids,
                "time_frame": _time_frame_for_node(node["id"]),
                "evidence_ids": node["evidence_ids"][:5],
                "required_evidence": _required_evidence_for_node(node["id"]),
                "disconfirming_signals": _disconfirming_signals_for_node(node["id"]),
                "decision_rule": _decision_rule_for_node(node["id"]),
            }
        )
        for child_index, child in enumerate(_child_questions_for_node(node["id"]), start=1):
            rows.append(
                {
                    "id": f"{parent_id}_d{child_index}",
                    "ticker": ticker,
                    "level": 1,
                    "parent_id": parent_id,
                    "priority": child["priority"],
                    "status": "open",
                    "question": child["question"],
                    "why_it_matters": child["why_it_matters"],
                    "linked_foundation_sections": child["sections"],
                    "linked_business_node_ids": [node["id"]],
                    "linked_assumption_ids": assumption_ids,
                    "time_frame": child["time_frame"],
                    "evidence_ids": node["evidence_ids"][:3],
                    "required_evidence": child["required_evidence"],
                    "disconfirming_signals": child["disconfirming_signals"],
                    "decision_rule": child["decision_rule"],
                }
            )

    for section in foundation_graph["sections"]:
        if section["status"] != "missing":
            continue
        rows.append(
            {
                "id": f"q_{ticker.lower()}_gap_{section['id']}",
                "ticker": ticker,
                "level": 0,
                "parent_id": None,
                "priority": "P1",
                "status": "needs_data",
                "question": f"What primary evidence is needed to make {section['label']} research-ready?",
                "why_it_matters": "A missing foundation section can make later message-flow conclusions look more certain than they are.",
                "linked_foundation_sections": [section["id"]],
                "linked_business_node_ids": [],
                "linked_assumption_ids": [f"assumption_gap_{section['id']}"],
                "time_frame": "T0 foundation",
                "evidence_ids": [],
                "required_evidence": section["gaps"],
                "disconfirming_signals": ["Do not strengthen a thesis until the missing foundation section is evidenced."],
                "decision_rule": "Keep the foundation status incomplete or needs_review until primary or high-reliability evidence is added.",
            }
        )
    return rows


def _build_message_flow(
    ticker: str,
    evidence: list[EvidenceRecord],
    foundation_graph: dict[str, Any],
    questions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    messages: list[dict[str, Any]] = []
    for record in evidence:
        affected_nodes = [
            node["id"] for node in foundation_graph["business_nodes"] if record.id in node.get("evidence_ids", [])
        ]
        affected_sections = [
            section["id"] for section in foundation_graph["sections"] if record.id in section.get("evidence_ids", [])
        ]
        affected_assumptions = [
            assumption["id"]
            for assumption in foundation_graph["assumptions"]
            if record.id in assumption.get("supporting_evidence_ids", [])
        ]
        related_questions = [
            question["id"]
            for question in questions
            if set(question.get("linked_business_node_ids", [])) & set(affected_nodes)
            or set(question.get("linked_foundation_sections", [])) & set(affected_sections)
        ][:8]
        messages.append(
            {
                "id": f"mf_{_safe_id(record.id)}",
                "ticker": ticker,
                "evidence_id": record.id,
                "message_fact": record.summary,
                "source_name": record.source_name,
                "source_type": record.source_type,
                "information_category": record.information_category,
                "reliability": record.reliability,
                "materiality": record.materiality,
                "prior_baseline": _prior_baseline(record, affected_nodes, affected_sections),
                "marginal_change": _marginal_change(record),
                "affected_foundation_sections": affected_sections,
                "affected_business_node_ids": affected_nodes,
                "affected_kpis": _affected_kpis(record, foundation_graph["kpis"]),
                "affected_assumption_ids": affected_assumptions,
                "fenghe": _fenghe_classification(record, affected_nodes),
                "impact": _message_impact(record),
                "certainty": _message_certainty(record),
                "follow_up_question_ids": related_questions,
                "follow_up_questions": _question_texts(questions, related_questions[:3]),
                "research_action": _research_action(record),
            }
        )
    return messages


def _evidence_ids_for_keywords(evidence: list[EvidenceRecord], keywords: list[str]) -> list[str]:
    evidence_ids: list[str] = []
    for record in evidence:
        if _matches_any(_record_text(record), keywords):
            evidence_ids.append(record.id)
    return evidence_ids


def _record_text(record: EvidenceRecord) -> str:
    return " ".join(
        [
            record.source_type,
            record.source_name,
            record.summary,
            " ".join(record.themes),
        ]
    ).lower()


def _matches_any(text: str, keywords: list[str]) -> bool:
    return any(keyword.lower() in text for keyword in keywords)


def _summaries_for_ids(evidence: list[EvidenceRecord], evidence_ids: list[str], limit: int) -> list[tuple[str, str]]:
    by_id = {record.id: record for record in evidence}
    return [(evidence_id, by_id[evidence_id].summary) for evidence_id in evidence_ids[:limit] if evidence_id in by_id]


def _numeric_snippets(text: str) -> list[str]:
    pattern = re.compile(
        r"(?:(?:RMB|USD|\$)\s*)?\d+(?:,\d{3})*(?:\.\d+)?\s*(?:B|M|billion|million|%|units|vehicles|shares|台|辆)?",
        re.IGNORECASE,
    )
    snippets: list[str] = []
    for match in pattern.finditer(text):
        start = max(0, match.start() - 42)
        end = min(len(text), match.end() + 42)
        snippet = text[start:end].strip(" .;")
        if snippet and snippet not in snippets:
            snippets.append(snippet)
    return snippets


def _kpi_label(record: EvidenceRecord) -> str:
    name = record.source_name.lower()
    summary = record.summary.lower()
    if "margin" in summary or "gross profit" in name:
        return "Margin / gross profit"
    if "revenue" in name or "revenue" in summary:
        return "Revenue"
    if "cash" in name or "cash" in summary:
        return "Cash flow / liquidity"
    if "shipment" in summary or "share" in summary:
        return "Market share / shipments"
    if "delivery" in summary or "deliveries" in summary:
        return "Deliveries"
    if "profit" in name or "income" in name or "profit" in summary:
        return "Profitability"
    return "Evidence metric"


def _kpi_why(record: EvidenceRecord) -> str:
    text = _record_text(record)
    if "cash" in text:
        return "Cash conversion determines whether growth can fund itself."
    if "share" in text or "shipment" in text:
        return "Share and shipment trends test competitive position and demand quality."
    if "margin" in text or "gross profit" in text:
        return "Margins translate operating change into earnings revisions."
    if "ev" in text or "vehicle" in text or "auto" in text:
        return "EV metrics test whether the second curve is financially repeatable."
    return "The metric helps convert narrative evidence into a testable baseline."


def _assumption_for_node(node_id: str, label: str) -> str:
    assumptions = {
        "smartphone": "The smartphone platform remains stable enough to anchor users, channels, and downstream monetization.",
        "iot": "IoT scale creates repeat purchase and ecosystem lock-in rather than only low-margin hardware volume.",
        "services": "Service monetization is durable after platform, regulatory, and ad-cycle effects.",
        "smart_ev": "Smart EV can become a repeatable profit pool after capex, warranty, safety, and price competition.",
        "supply_chain": "The company can manage component inflation, supply constraints, and manufacturing quality without destroying margins.",
        "capital_allocation": "Cash generation and balance-sheet strength can fund reinvestment without weakening shareholder economics.",
        "governance_control": "Control structure and leadership quality improve long-term execution more than they raise minority-shareholder risk.",
        "group_financials": "Reported growth converts into durable margin and cash-flow quality.",
    }
    return assumptions.get(node_id, f"{label} is material to the company baseline and needs explicit evidence testing.")


def _main_question_for_node(node_id: str, label: str) -> str:
    questions = {
        "smartphone": "Is the smartphone baseline stable, or is share/margin deterioration changing the platform thesis?",
        "iot": "Does IoT create real ecosystem lock-in and profit quality, or only hardware volume?",
        "services": "Is the service profit pool durable, or exposed to platform, traffic, and regulatory pressure?",
        "smart_ev": "Can Smart EV become a repeatable profit pool after safety, warranty, capex, and price competition?",
        "supply_chain": "Can the company pass through component inflation and preserve quality while scaling?",
        "capital_allocation": "Can cash flows fund the next growth curve without weakening returns or minority-shareholder economics?",
        "governance_control": "Does founder/control structure improve long-term execution or create governance discount risk?",
        "group_financials": "Which segment is actually driving gross profit, cash conversion, and durable value creation?",
    }
    return questions.get(node_id, f"What are the decisive value drivers and fragility points inside {label}?")


def _why_question_matters(node_id: str) -> str:
    reasons = {
        "smartphone": "The phone base often feeds user scale, channels, services, and ecosystem attachment.",
        "iot": "IoT can be either a durable ecosystem layer or a capital-light-looking but low-return hardware mix.",
        "services": "Service margins can dominate profit quality even when revenue share is small.",
        "smart_ev": "EV can re-rate the company or absorb cash and introduce safety liabilities.",
        "supply_chain": "Input-cost and quality-control shocks can reverse margin and delivery narratives quickly.",
        "capital_allocation": "Capital allocation determines whether growth translates into per-share value.",
        "governance_control": "Control rights affect strategic patience, accountability, and valuation discount.",
        "group_financials": "Segment mix can hide whether growth improves or dilutes long-term returns.",
    }
    return reasons.get(node_id, "It identifies whether the local evidence changes the company baseline.")


def _sections_for_node(node_id: str) -> list[str]:
    mapping = {
        "smartphone": ["current_business", "competition", "value_chain"],
        "iot": ["current_business", "value_chain", "strategy"],
        "services": ["current_business", "strategy", "risk_sweep"],
        "smart_ev": ["current_business", "value_chain", "competition", "strategy", "risk_sweep"],
        "supply_chain": ["value_chain", "risk_sweep"],
        "capital_allocation": ["current_business", "strategy", "risk_sweep"],
        "governance_control": ["governance", "risk_sweep"],
        "group_financials": ["current_business", "risk_sweep"],
    }
    return mapping.get(node_id, ["current_business", "risk_sweep"])


def _time_frame_for_node(node_id: str) -> str:
    if node_id in {"smartphone", "supply_chain"}:
        return "T1/T2"
    if node_id in {"smart_ev", "iot", "services", "capital_allocation"}:
        return "T2/T3"
    return "T3"


def _required_evidence_for_node(node_id: str) -> list[str]:
    mapping = {
        "smartphone": ["Quarterly shipments by region", "ASP and gross margin bridge", "Channel inventory and component-cost commentary"],
        "iot": ["Category revenue and gross margin", "Multi-device user cohort retention", "Attach-rate and repeat-purchase data"],
        "services": ["MAU by region", "ARPU and ad/gaming/service mix", "Regulatory and platform policy updates"],
        "smart_ev": ["Deliveries, order backlog, and wait time", "Vehicle gross margin bridge", "Warranty, recall, safety, and service-cost data"],
        "supply_chain": ["Key component pricing", "Inventory days", "Supplier concentration and capacity commitments"],
        "capital_allocation": ["Operating cash flow", "Capex by business line", "Buyback/dividend/financing decisions"],
        "governance_control": ["Voting-control disclosures", "Board composition", "Related-party and capital-allocation history"],
        "group_financials": ["Segment revenue", "Segment gross profit", "Operating cash flow and working-capital bridge"],
    }
    return mapping.get(node_id, ["Primary filings", "Management commentary", "Independent industry data"])


def _disconfirming_signals_for_node(node_id: str) -> list[str]:
    mapping = {
        "smartphone": ["Share losses persist for two or more quarters", "ASP and gross margin decline together", "Inventory builds while shipments fall"],
        "iot": ["Growth requires discounts", "Gross margin falls as scale rises", "Connected-device users do not improve service monetization"],
        "services": ["MAU growth slows while monetization falls", "Regulatory changes reduce ads or app distribution economics", "High-margin revenue mix shrinks"],
        "smart_ev": ["Vehicle gross margin falls after launch cycle", "Price cuts outpace cost-down", "Recall, warranty, or safety costs rise faster than deliveries"],
        "supply_chain": ["BOM inflation cannot be passed through", "Supply constraints reduce high-margin mix", "Quality incidents rise with production scale"],
        "capital_allocation": ["Free cash flow weakens despite reported profit", "Capex rises without operating leverage", "Financing dilutes while returns remain unproven"],
        "governance_control": ["Major capital allocation lacks minority-shareholder discipline", "Related-party risk increases", "Board independence weakens"],
        "group_financials": ["Revenue grows while cash conversion and margin quality weaken", "One segment masks deterioration elsewhere"],
    }
    return mapping.get(node_id, ["New primary evidence contradicts the current baseline."])


def _decision_rule_for_node(node_id: str) -> str:
    mapping = {
        "smartphone": "Upgrade the baseline only if share, ASP, margin, and inventory evidence improve together; otherwise keep the issue open.",
        "iot": "Treat IoT as a quality profit pool only if scale comes with stable margins and measurable ecosystem retention.",
        "services": "Treat services as durable only if MAU, ARPU, and regulatory evidence support repeatability.",
        "smart_ev": "Do not strengthen the EV thesis unless deliveries, margin, safety, warranty, and capex evidence all remain consistent.",
        "supply_chain": "Classify component shocks as structural only if they persist across price, volume, and margin evidence.",
        "capital_allocation": "Strengthen only when cash conversion and reinvestment returns are visible, not just when accounting profit rises.",
        "governance_control": "Apply a governance discount if control rights enable capital allocation that lacks evidence-backed return discipline.",
        "group_financials": "Prefer segment-level cash and margin proof over group revenue growth.",
    }
    return mapping.get(node_id, "Keep the question open until evidence can support and disconfirm the assumption.")


def _child_questions_for_node(node_id: str) -> list[dict[str, Any]]:
    common = {
        "priority": "P1",
        "time_frame": "T2",
        "sections": ["current_business"],
        "required_evidence": ["Primary company data", "Independent industry data"],
        "disconfirming_signals": ["Evidence conflicts with the current baseline."],
        "decision_rule": "Do not close the question until at least one primary or high-reliability source tests it.",
    }
    templates: dict[str, list[dict[str, Any]]] = {
        "smartphone": [
            {
                **common,
                "priority": "P0",
                "question": "Is shipment weakness active portfolio control, component shortage, price elasticity, or real demand loss?",
                "why_it_matters": "The same shipment decline has very different margin and ecosystem implications depending on cause.",
                "sections": ["current_business", "competition", "value_chain"],
                "required_evidence": ["Shipments by price band", "Channel inventory", "Component availability", "ASP and gross margin bridge"],
                "disconfirming_signals": ["Volume falls while inventory rises", "Low-end mix deteriorates despite price cuts"],
                "decision_rule": "Separate supply, demand, and mix before updating the company baseline.",
            },
            {
                **common,
                "question": "Does smartphone share pressure weaken service and IoT user acquisition?",
                "why_it_matters": "Platform value depends on the phone base feeding higher-margin layers.",
                "sections": ["current_business", "strategy"],
                "required_evidence": ["MAU trend", "Device attach rate", "Services revenue by region"],
                "disconfirming_signals": ["MAU or attach rate stalls after phone share loss"],
                "decision_rule": "Only treat share loss as contained if ecosystem metrics remain stable.",
            },
        ],
        "smart_ev": [
            {
                **common,
                "priority": "P0",
                "question": "Is vehicle gross margin sustainable after launch mix, price competition, warranty, recall, and service costs?",
                "why_it_matters": "EV growth can be value-accretive or value-destructive depending on post-launch unit economics.",
                "sections": ["current_business", "risk_sweep"],
                "required_evidence": ["Vehicle gross margin bridge", "Warranty accrual", "Recall cost", "Price changes", "Capacity utilization"],
                "disconfirming_signals": ["Gross margin falls with higher deliveries", "Recall or warranty costs rise faster than revenue"],
                "decision_rule": "Require unit-economics proof before treating EV as a durable profit pool.",
            },
            {
                **common,
                "question": "Does safety and assisted-driving performance change customer trust or regulatory cost?",
                "why_it_matters": "Automotive safety incidents can impair both economics and brand permission.",
                "sections": ["value_chain", "risk_sweep"],
                "required_evidence": ["Regulator notices", "Recall completion", "Insurance and accident data", "Customer complaints"],
                "disconfirming_signals": ["New safety notices", "Higher insurance costs", "Delivery slowdown after incidents"],
                "decision_rule": "Treat safety evidence as a gating item for EV thesis strength.",
            },
        ],
        "iot": [
            {
                **common,
                "question": "Are multi-device users increasing because of genuine lock-in or because of discount-driven category expansion?",
                "why_it_matters": "Lock-in supports durable services and pricing; discounts only create hardware churn.",
                "sections": ["current_business", "strategy"],
                "required_evidence": ["Multi-device cohorts", "Repeat purchase", "Category margin by product", "Promotion intensity"],
                "disconfirming_signals": ["Connected devices rise but margins or retention fall"],
                "decision_rule": "Require retention and margin proof before calling IoT a moat.",
            }
        ],
        "services": [
            {
                **common,
                "question": "Is high service margin protected by user behavior, platform control, or temporary ad-cycle strength?",
                "why_it_matters": "Services can dominate profit quality but is vulnerable to traffic and regulation.",
                "sections": ["current_business", "risk_sweep"],
                "required_evidence": ["MAU", "ARPU", "Ads/games/value-added mix", "Regulatory changes"],
                "disconfirming_signals": ["MAU grows but ARPU falls", "Regulation reduces monetization channels"],
                "decision_rule": "Separate user-scale durability from ad-cycle cyclicality.",
            }
        ],
        "capital_allocation": [
            {
                **common,
                "question": "Is reinvestment earning adequate returns after capex, working capital, and shareholder dilution?",
                "why_it_matters": "Growth only matters if it converts into per-share value.",
                "sections": ["strategy", "risk_sweep"],
                "required_evidence": ["Capex by segment", "Operating cash flow bridge", "ROIC by business", "Financing and buyback disclosures"],
                "disconfirming_signals": ["Capex rises without cash-flow improvement", "Equity issuance funds low-return expansion"],
                "decision_rule": "Tie every growth claim to cash conversion and reinvestment return.",
            }
        ],
        "governance_control": [
            {
                **common,
                "question": "Are control rights being used for patient compounding or for unaccountable capital allocation?",
                "why_it_matters": "Founder control can be a strategic asset or a minority-shareholder risk.",
                "sections": ["governance", "risk_sweep"],
                "required_evidence": ["Voting rights", "Board independence", "Capital-allocation track record", "Related-party disclosures"],
                "disconfirming_signals": ["Large strategic spending lacks return evidence", "Minority protections weaken"],
                "decision_rule": "Governance should remain a discount unless control improves measurable execution.",
            }
        ],
    }
    return templates.get(
        node_id,
        [
            {
                **common,
                "question": "Which fresh evidence would most quickly falsify the current baseline?",
                "why_it_matters": "A professional research system should name the next falsification test explicitly.",
            }
        ],
    )


def _assumption_ids_for_node(assumptions: list[dict[str, Any]], node_id: str) -> list[str]:
    return [
        assumption["id"]
        for assumption in assumptions
        if node_id in assumption.get("linked_business_node_ids", [])
    ]


def _prior_baseline(record: EvidenceRecord, affected_nodes: list[str], affected_sections: list[str]) -> str:
    if not affected_nodes and not affected_sections:
        return "No mapped baseline yet; use this evidence to seed the foundation graph."
    nodes = ", ".join(affected_nodes) if affected_nodes else "no business node"
    sections = ", ".join(affected_sections) if affected_sections else "no foundation section"
    return f"Before this message, local baseline for {nodes} / {sections} should be treated as priced or unresolved."


def _marginal_change(record: EvidenceRecord) -> str:
    text = _record_text(record)
    if record.reliability in {"primary", "high"} and record.materiality in {"high", "thesis_change"}:
        return "High-quality evidence can update the baseline, but only through linked assumptions and disconfirming tests."
    if record.reliability in {"low", "medium"}:
        return "Use as a research lead; require primary or high-reliability confirmation before changing thesis strength."
    if _matches_any(text, ["decline", "decrease", "recall", "loss", "risk", "safety"]):
        return "Potential negative update; test whether it is transient noise or structural baseline damage."
    return "Evidence seeds or refreshes the baseline; compare with prior period and consensus expectations before thesis change."


def _affected_kpis(record: EvidenceRecord, kpis: list[dict[str, Any]]) -> list[str]:
    return [kpi["id"] for kpi in kpis if kpi["evidence_id"] == record.id]


def _fenghe_classification(record: EvidenceRecord, affected_nodes: list[str]) -> dict[str, str]:
    text = _record_text(record)
    if "governance_control" in affected_nodes or _matches_any(text, ["management", "board", "governance", "voting", "wvr", "founder"]):
        return {"cycle": "management and capital-allocation cycle", "change": "control, incentive, or governance evidence", "certainty": _message_certainty(record), "dominant_d": "D1", "five_m": "M5", "time_frame": "T3"}
    if record.source_type in {"company_ir", "ipo_prospectus"}:
        return {"cycle": "company foundation baseline", "change": "origin, model, or strategic-positioning evidence", "certainty": _message_certainty(record), "dominant_d": "D1", "five_m": "M4", "time_frame": "T3"}
    if "smart_ev" in affected_nodes or _matches_any(text, ["ev", "vehicle", "recall", "assisted driving"]):
        return {"cycle": "EV adoption / safety validation cycle", "change": "new manufacturing or safety evidence", "certainty": _message_certainty(record), "dominant_d": "D2", "five_m": "M3/M4/M5", "time_frame": "T1/T2"}
    if "smartphone" in affected_nodes or _matches_any(text, ["smartphone", "shipment", "share"]):
        return {"cycle": "device replacement and component-cost cycle", "change": "share, shipment, or pricing evidence", "certainty": _message_certainty(record), "dominant_d": "D2", "five_m": "M2/M3", "time_frame": "T1/T2"}
    if "services" in affected_nodes:
        return {"cycle": "platform monetization cycle", "change": "MAU, ARPU, or mix evidence", "certainty": _message_certainty(record), "dominant_d": "D1", "five_m": "M4", "time_frame": "T2/T3"}
    if _matches_any(text, ["price", "valuation", "market cap"]):
        return {"cycle": "sentiment and valuation cycle", "change": "price or valuation evidence", "certainty": _message_certainty(record), "dominant_d": "D3", "five_m": "M4", "time_frame": "T1"}
    return {"cycle": "business baseline refresh", "change": "new evidence should be mapped to affected assumptions", "certainty": _message_certainty(record), "dominant_d": "D1", "five_m": "M4", "time_frame": "T2"}


def _message_impact(record: EvidenceRecord) -> str:
    text = _record_text(record)
    if record.reliability in {"low", "medium"} and record.materiality != "high":
        return "research_lead"
    if _matches_any(text, ["recall", "decline", "decrease", "loss", "risk", "safety", "liability", "pressure"]):
        return "weakening"
    if _matches_any(text, ["increase", "growth", "profit", "record", "positive", "improve", "cash generated"]):
        return "strengthening"
    return "baseline_update"


def _message_certainty(record: EvidenceRecord) -> str:
    if record.reliability == "primary":
        return "high"
    if record.reliability == "high":
        return "medium_high"
    if record.reliability == "medium":
        return "medium"
    return "low"


def _question_texts(questions: list[dict[str, Any]], question_ids: list[str]) -> list[str]:
    by_id = {question["id"]: question["question"] for question in questions}
    return [by_id[question_id] for question_id in question_ids if question_id in by_id]


def _research_action(record: EvidenceRecord) -> str:
    if record.reliability in {"low", "medium"}:
        return "Queue for confirmation and attach to open questions; do not strengthen thesis from this item alone."
    if _message_impact(record) == "weakening":
        return "Escalate as a disconfirming test and search for primary follow-up evidence."
    return "Update baseline, then test whether the change is already priced and durable."


def _risk_statement(record: EvidenceRecord) -> str:
    return f"{record.source_name}: {record.summary}"


def _risk_monitoring_tests(record: EvidenceRecord) -> list[str]:
    text = _record_text(record)
    if "recall" in text or "safety" in text:
        return ["Recall completion", "New regulator notices", "Warranty and insurance costs", "Customer complaints"]
    if "decline" in text or "decrease" in text:
        return ["Next period same KPI", "Management explanation", "Peer trend", "Pricing and inventory evidence"]
    if "debt" in text or "liability" in text:
        return ["Net cash/debt", "Interest coverage", "Maturity schedule", "Operating cash flow"]
    return ["Primary follow-up evidence", "Peer comparison", "Management commentary"]


def _safe_id(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    return re.sub(r"_+", "_", cleaned).strip("_")


def _write_json(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _write_text(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as file:
        file.write(text)


def _apple_research_css() -> str:
    return """
    :root {
      --ink: #1d1d1f;
      --muted: #6e6e73;
      --paper: #f5f5f7;
      --panel: #ffffff;
      --panel-soft: #fbfbfd;
      --line: #d2d2d7;
      --blue: #0066cc;
      --green: #248a3d;
      --amber: #a86600;
      --red: #d70015;
      --shadow: 0 18px 50px rgba(0, 0, 0, .08);
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      color: var(--ink);
      background: var(--paper);
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.55;
    }
    header {
      padding: clamp(52px, 8vw, 104px) clamp(20px, 6vw, 86px) 34px;
      color: var(--ink);
      background: linear-gradient(180deg, #fff 0%, #f8f8fa 72%, var(--paper) 100%);
      border-bottom: 1px solid rgba(0, 0, 0, .06);
    }
    h1 { max-width: 1080px; margin: 0; font-size: clamp(44px, 7vw, 86px); font-weight: 700; line-height: .98; letter-spacing: 0; }
    h2 { margin: 0 0 12px; font-size: clamp(28px, 4vw, 48px); font-weight: 700; letter-spacing: 0; }
    h3 { margin: 0 0 10px; font-size: clamp(21px, 2.2vw, 29px); font-weight: 700; letter-spacing: 0; }
    p { margin: 0 0 10px; }
    a { color: var(--blue); text-decoration: none; }
    a:hover { text-decoration: underline; }
    .subtitle { max-width: 940px; margin-top: 18px; color: var(--muted); font-size: clamp(18px, 2.1vw, 24px); line-height: 1.45; }
    .nav, nav {
      position: sticky;
      top: 0;
      z-index: 10;
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding: 11px clamp(16px, 5vw, 70px);
      background: rgba(245, 245, 247, .82);
      border-bottom: 1px solid rgba(0, 0, 0, .08);
      backdrop-filter: saturate(180%) blur(20px);
    }
    .nav a, nav a {
      flex: 0 0 auto;
      padding: 7px 12px;
      color: var(--ink);
      text-decoration: none;
      border: 1px solid rgba(0, 0, 0, .08);
      background: rgba(255, 255, 255, .74);
      border-radius: 999px;
      font-size: 13px;
      font-weight: 500;
    }
    main { width: min(1180px, calc(100% - 32px)); margin: 26px auto 72px; }
    section {
      margin: 18px 0;
      padding: clamp(24px, 4vw, 44px);
      background: rgba(255, 255, 255, .9);
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      box-shadow: 0 1px 0 rgba(255, 255, 255, .7) inset;
    }
    .layer-label, .eyebrow { margin: 0 0 12px; color: var(--blue); font-size: 13px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
    .summary-grid, .summary-strip { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 18px; }
    .summary-card, .metric {
      padding: 16px;
      background: rgba(255, 255, 255, .88);
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      min-width: 0;
      box-shadow: 0 10px 30px rgba(0, 0, 0, .05);
      color: var(--ink);
    }
    .summary-card span, .metric span { display: block; color: var(--muted); font-size: 12px; font-weight: 600; letter-spacing: .04em; text-transform: none; }
    .summary-card strong, .metric strong { display: block; margin-top: 8px; font-size: clamp(20px, 2.2vw, 30px); font-weight: 700; line-height: 1.1; overflow-wrap: anywhere; }
    .summary-card p { margin: 9px 0 0; color: var(--muted); font-size: 13px; }
    .foundation-grid, .grid, .lead-grid, .info-grid, .reference-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; align-items: start; }
    .foundation-card, .card, .question-card, .history-card {
      padding: clamp(18px, 3vw, 28px);
      background: var(--panel);
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      min-width: 0;
      box-shadow: var(--shadow);
    }
    .foundation-card { border-left: 0; }
    .foundation-card.partial, .foundation-card.missing { border-left: 0; }
    .detail-link {
      display: inline-flex;
      margin-top: 12px;
      padding: 8px 13px;
      color: #fff;
      background: var(--blue);
      text-decoration: none;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 600;
    }
    .detail-link:hover { background: #005bb5; text-decoration: none; }
    .answer-box, .rule-box {
      padding: 16px;
      background: #f5f8ff;
      border: 1px solid #d6e6ff;
      border-radius: 8px;
      margin: 14px 0 16px;
    }
    .info-box {
      padding: 14px;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      background: var(--panel-soft);
      min-width: 0;
    }
    .info-box h4 { margin: 0 0 10px; font-size: 13px; font-weight: 700; color: var(--muted); letter-spacing: .04em; }
    .info-box ul { display: grid; gap: 12px; margin: 0; padding: 0; list-style: none; }
    .info-box li { margin: 0; padding-top: 12px; border-top: 1px solid rgba(0, 0, 0, .07); }
    .info-box li:first-child { padding-top: 0; border-top: 0; }
    .info-box.evidence { background: #f5f9ff; }
    .info-box.research_report { background: #f4fbf7; }
    .info-box.message { background: #fff9ef; }
    .info-box.opinion { background: #f6f6f7; }
    .timeline { display: grid; gap: 12px; margin-top: 16px; }
    .timeline-row { display: grid; grid-template-columns: 120px 1fr; gap: 16px; padding: 16px; border: 1px solid rgba(0, 0, 0, .08); border-radius: 8px; background: var(--panel); }
    .timeline-year { color: var(--blue); font-weight: 700; }
    .field { margin-top: 12px; }
    .field b { display: block; margin-bottom: 5px; color: var(--muted); font-size: 12px; font-weight: 700; letter-spacing: .04em; text-transform: none; }
    .note { color: var(--muted); font-size: 13px; }
    .chip {
      display: inline-flex;
      max-width: 100%;
      margin: 0 4px 7px 0;
      padding: 3px 7px;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 999px;
      background: rgba(255, 255, 255, .76);
      color: #424245;
      font-family: "SF Mono", ui-monospace, SFMono-Regular, Consolas, monospace;
      font-size: 11px;
      overflow-wrap: anywhere;
    }
    .status-evidenced { color: var(--green); font-weight: 800; }
    .status-partial { color: var(--amber); font-weight: 800; }
    .status-missing, .impact-weakening { color: var(--red); font-weight: 800; }
    .impact-strengthening { color: var(--green); font-weight: 800; }
    .impact-research_lead { color: var(--amber); font-weight: 800; }
    table { width: 100%; border-collapse: separate; border-spacing: 0; background: #fff; font-size: 14px; border: 1px solid rgba(0, 0, 0, .08); border-radius: 8px; overflow: hidden; }
    th, td { padding: 13px; border-bottom: 1px solid rgba(0, 0, 0, .08); vertical-align: top; text-align: left; }
    tr:last-child td { border-bottom: 0; }
    th { color: var(--muted); font-size: 12px; font-weight: 700; letter-spacing: .04em; background: #f5f5f7; text-transform: none; }
    ul { margin: 8px 0 0; padding-left: 20px; }
    li { margin: 5px 0; }
    @media (max-width: 880px) {
      .summary-grid, .summary-strip, .foundation-grid, .grid, .lead-grid, .info-grid, .reference-grid, .timeline-row { grid-template-columns: 1fr; }
      table { font-size: 13px; }
      header { padding-top: 42px; }
    }
    """


def _qa_explorer_css() -> str:
    return """
    .qa-shell {
      display: grid;
      grid-template-columns: minmax(230px, .78fr) minmax(0, 1.45fr) minmax(300px, .95fr);
      gap: 16px;
      align-items: start;
    }
    .qa-full-research {
      width: min(1180px, calc(100% - 32px));
      margin: 26px auto 24px;
    }
    .qa-full-research .thesis-card {
      margin: 14px 0 16px;
      border-radius: 8px;
      border-left: 0;
      background: #111820;
      box-shadow: var(--shadow);
    }
    .qa-full-research table {
      margin: 12px 0 24px;
    }
    .qa-full-research .question-card {
      margin: 16px 0;
    }
    .level-frame {
      scroll-margin-top: 70px;
    }
    .l2-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-top: 14px;
    }
    .l2-card {
      padding: clamp(18px, 2.5vw, 26px);
      background: #fff;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      box-shadow: var(--shadow);
      min-width: 0;
    }
    .l2-card h3 {
      font-size: clamp(20px, 2vw, 27px);
    }
    .research-unit-card {
      display: grid;
      gap: 12px;
    }
    .decision-panel {
      margin-top: 12px;
      padding: 14px;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      background: linear-gradient(180deg, #ffffff 0%, #f8f8fa 100%);
    }
    .decision-head {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
      margin-bottom: 12px;
    }
    .decision-head b {
      color: var(--ink);
      font-size: 13px;
      letter-spacing: .04em;
    }
    .decision-head span {
      flex: 0 0 auto;
      padding: 4px 8px;
      border-radius: 999px;
      background: #eef5ff;
      color: var(--blue);
      font-size: 12px;
      font-weight: 700;
    }
    .decision-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }
    .decision-box {
      min-width: 0;
      padding: 12px;
      border: 1px solid rgba(0, 0, 0, .07);
      border-radius: 8px;
      background: rgba(255, 255, 255, .84);
    }
    .decision-box.judgment {
      background: #111820;
      color: #fff;
    }
    .decision-box.judgment h4,
    .decision-box.judgment p {
      color: #fff;
    }
    .decision-box h4,
    .next-step-box b {
      margin: 0 0 8px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .04em;
    }
    .decision-box ul {
      margin: 0;
      padding-left: 18px;
    }
    .decision-box li {
      margin: 4px 0;
      font-size: 13px;
    }
    .evidence-score strong {
      font-size: 20px;
      color: var(--ink);
    }
    .next-step-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      margin-top: 12px;
    }
    .next-step-box {
      min-width: 0;
      padding: 12px;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      background: #fff9ef;
    }
    .next-step-box p {
      margin: 0;
      font-size: 13px;
    }
    .l3-info-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
      margin-top: 8px;
    }
    .l3-info-box {
      min-width: 0;
      padding: 10px;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      background: var(--panel-soft);
    }
    .l3-info-box.evidence { background: #f5f9ff; }
    .l3-info-box.research_report { background: #f4fbf7; }
    .l3-info-box.message { background: #fff9ef; }
    .l3-info-box.opinion { background: #f6f6f7; }
    .l3-info-box h4 {
      margin: 0 0 8px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .04em;
    }
    .l3-info-box ul {
      display: grid;
      gap: 8px;
      margin: 0;
      padding: 0;
      list-style: none;
    }
    .l3-info-box li {
      margin: 0;
      padding: 9px 0 0 10px;
      border-top: 1px solid rgba(0, 0, 0, .07);
      border-left: 3px solid #8e8e93;
    }
    .l3-info-box li:first-child {
      padding-top: 0;
      border-top: 0;
    }
    .l3-info-box li.stance-support { border-left-color: var(--green); }
    .l3-info-box li.stance-refute { border-left-color: var(--red); }
    .l3-info-box li.stance-lead { border-left-color: var(--amber); }
    .stance-pill,
    .quality-pill {
      display: inline-flex;
      margin: 0 5px 7px 0;
      padding: 3px 7px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
    }
    .stance-pill {
      background: #f5f5f7;
      color: var(--ink);
    }
    .quality-pill {
      background: #eef5ff;
      color: var(--blue);
    }
    .qa-panel {
      min-width: 0;
      background: rgba(255, 255, 255, .92);
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }
    .qa-tree-panel, .qa-evidence-panel {
      position: sticky;
      top: 62px;
      max-height: calc(100vh - 84px);
      overflow: auto;
      padding: 16px;
    }
    .qa-main-panel { padding: clamp(22px, 3vw, 34px); }
    .qa-kicker {
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .04em;
      margin-bottom: 10px;
    }
    .qa-tree-group { margin: 0 0 16px; }
    .qa-tree-title {
      margin: 12px 0 8px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
    }
    .qa-node-button {
      width: 100%;
      display: block;
      margin: 5px 0;
      padding: 9px 10px;
      color: var(--ink);
      background: transparent;
      border: 1px solid transparent;
      border-radius: 8px;
      text-align: left;
      font: inherit;
      cursor: pointer;
    }
    .qa-node-button:hover { background: #f5f5f7; }
    .qa-node-button.active {
      background: #f5f8ff;
      border-color: #c9ddff;
      color: var(--blue);
      font-weight: 700;
    }
    .qa-node-level {
      display: inline-flex;
      margin-right: 6px;
      color: var(--muted);
      font-size: 11px;
      font-weight: 700;
    }
    .qa-level-2 { padding-left: 20px; }
    .qa-level-3 { padding-left: 36px; }
    .qa-level-4 { padding-left: 52px; }
    .qa-toolbar {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      margin-bottom: 14px;
    }
    .qa-badge {
      display: inline-flex;
      padding: 4px 8px;
      border-radius: 999px;
      background: #f5f5f7;
      color: var(--muted);
      font-size: 12px;
      font-weight: 600;
    }
    .qa-question-title { margin-bottom: 14px; }
    .qa-rollup {
      margin: 14px 0;
      padding: 14px;
      border: 1px solid #d6e6ff;
      border-radius: 8px;
      background: #f5f8ff;
    }
    .qa-rollup strong { color: var(--blue); }
    .qa-synthesis-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin-top: 14px;
    }
    .qa-synthesis-box {
      padding: 14px;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      background: var(--panel-soft);
    }
    .qa-synthesis-box h4, .qa-child-list h4, .qa-bucket h4 {
      margin: 0 0 9px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
      letter-spacing: .04em;
    }
    .qa-child-list { margin-top: 16px; }
    .qa-child-list button {
      display: block;
      width: 100%;
      margin: 7px 0;
      padding: 11px 12px;
      text-align: left;
      color: var(--ink);
      background: #fff;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      font: inherit;
      cursor: pointer;
    }
    .qa-child-list button:hover { border-color: #c9ddff; color: var(--blue); }
    .qa-bucket {
      margin-bottom: 12px;
      padding: 14px;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      background: var(--panel-soft);
    }
    .qa-bucket.evidence { background: #f5f9ff; }
    .qa-bucket.research_report { background: #f4fbf7; }
    .qa-bucket.message { background: #fff9ef; }
    .qa-bucket.opinion { background: #f6f6f7; }
    .qa-evidence-item {
      padding: 11px 0;
      border-top: 1px solid rgba(0, 0, 0, .07);
    }
    .qa-evidence-item:first-of-type { border-top: 0; padding-top: 0; }
    .qa-empty { color: var(--muted); font-size: 13px; }
    .qa-ask textarea {
      width: 100%;
      min-height: 92px;
      resize: vertical;
      padding: 12px;
      border: 1px solid rgba(0, 0, 0, .12);
      border-radius: 8px;
      font: inherit;
      background: #fff;
    }
    .draft-question textarea {
      width: 100%;
      min-height: 92px;
      resize: vertical;
      padding: 12px;
      border: 1px solid rgba(0, 0, 0, .12);
      border-radius: 8px;
      font: inherit;
      background: #fff;
    }
    .qa-ask-actions {
      display: flex;
      gap: 8px;
      margin-top: 10px;
    }
    .qa-ask button {
      padding: 8px 12px;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 999px;
      font: inherit;
      cursor: pointer;
      background: #fff;
    }
    .qa-ask button.primary {
      color: #fff;
      background: var(--blue);
      border-color: var(--blue);
      font-weight: 700;
    }
    .draft-question button {
      padding: 8px 12px;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 999px;
      font: inherit;
      cursor: pointer;
      background: #fff;
    }
    .draft-question button.primary {
      color: #fff;
      background: var(--blue);
      border-color: var(--blue);
      font-weight: 700;
    }
    .qa-static-index {
      width: min(1180px, calc(100% - 32px));
      margin: 22px auto 72px;
    }
    .qa-static-card {
      margin: 12px 0;
      padding: 16px;
      background: #fff;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, .05);
    }
    .qa-static-card h3 {
      display: flex;
      gap: 8px;
      align-items: baseline;
      margin-bottom: 8px;
      font-size: 19px;
    }
    .qa-static-card span {
      flex: 0 0 auto;
      color: var(--blue);
      font-size: 12px;
      font-weight: 800;
    }
    .qa-static-card ul {
      display: grid;
      gap: 6px;
      margin-top: 10px;
      padding-left: 0;
      list-style: none;
    }
    .qa-static-card li {
      display: flex;
      gap: 8px;
      margin: 0;
      padding: 8px 10px;
      background: #f5f5f7;
      border-radius: 8px;
    }
    @media (max-width: 1080px) {
      .qa-shell { grid-template-columns: 1fr; }
      .l2-grid, .l3-info-grid, .decision-grid, .next-step-grid { grid-template-columns: 1fr; }
      .qa-tree-panel, .qa-evidence-panel { position: static; max-height: none; }
      .qa-synthesis-grid { grid-template-columns: 1fr; }
    }
    """


def _render_dashboard(
    ticker: str,
    foundation_graph: dict[str, Any],
    questions: list[dict[str, Any]],
    messages: list[dict[str, Any]],
    qa_tree: dict[str, Any],
) -> str:
    section_cards = "\n".join(_render_l0_framework_card(section, qa_tree) for section in foundation_graph["sections"])
    current_question = "公司基础框架：这家公司应该先用哪组基础问题建立认知？"
    l0_summary = _foundation_l0_summary(ticker, foundation_graph)
    add_question_box = _render_add_question_box(f"{ticker}:l0", "L0 公司基础框架")

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(ticker)} 公司基础画像</title>
  <style>
    :root {{
      --ink: #17202a;
      --muted: #66717d;
      --line: #d8ddd8;
      --paper: #f7f5ee;
      --panel: #ffffff;
      --green: #1f7a5c;
      --amber: #b66a18;
      --red: #b2473e;
      --blue: #2d5d8f;
      --charcoal: #111820;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background:
        linear-gradient(90deg, rgba(23,32,42,.05) 1px, transparent 1px),
        linear-gradient(0deg, rgba(23,32,42,.04) 1px, transparent 1px),
        var(--paper);
      background-size: 38px 38px;
      font-family: "Avenir Next", "Gill Sans", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.55;
    }}
    header {{
      padding: 42px clamp(18px, 5vw, 62px) 28px;
      color: #fff;
      background: var(--charcoal);
      border-bottom: 7px solid var(--green);
    }}
    h1 {{
      margin: 0;
      font-size: clamp(34px, 5.8vw, 68px);
      line-height: 1;
      letter-spacing: 0;
    }}
    h2 {{ margin: 0 0 14px; font-size: clamp(22px, 3vw, 34px); letter-spacing: 0; }}
    h3 {{ margin: 0 0 8px; font-size: 16px; }}
    .subtitle {{ max-width: 980px; color: #d6dedc; font-size: 18px; }}
    nav {{
      position: sticky;
      top: 0;
      z-index: 10;
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding: 10px clamp(14px, 4vw, 54px);
      background: rgba(247,245,238,.95);
      border-bottom: 1px solid var(--line);
      backdrop-filter: blur(10px);
    }}
    nav a {{
      flex: 0 0 auto;
      padding: 7px 10px;
      color: var(--ink);
      text-decoration: none;
      border: 1px solid var(--line);
      background: #fff;
      border-radius: 999px;
      font-size: 13px;
    }}
    main {{ width: min(1200px, calc(100% - 28px)); margin: 22px auto 58px; }}
    section {{ margin: 16px 0; padding: clamp(18px, 3vw, 30px); background: rgba(255,255,255,.93); border: 1px solid var(--line); }}
    .layer-label {{ color: var(--green); font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: .08em; }}
    .summary-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }}
    .summary-card {{ padding: 16px; border: 1px solid var(--line); background: var(--panel); min-width: 0; }}
    .summary-card span {{ display: block; color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .06em; }}
    .summary-card strong {{ display: block; margin-top: 7px; font-size: clamp(22px, 2.6vw, 34px); line-height: 1.05; }}
    .summary-card p {{ margin: 9px 0 0; color: var(--muted); font-size: 13px; }}
    .committee {{
      display: grid;
      grid-template-columns: 1.1fr .9fr;
      gap: 14px;
      margin-top: 14px;
    }}
    .committee-panel {{ padding: 18px; background: #fff; border: 1px solid var(--line); }}
    .committee-panel strong {{ color: var(--ink); }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .card {{ padding: 14px; border: 1px solid var(--line); background: #fff; }}
    .foundation-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .foundation-card {{ padding: 16px; border: 1px solid var(--line); background: #fff; border-left: 5px solid var(--green); min-width: 0; }}
    .foundation-card.partial {{ border-left-color: var(--amber); }}
    .foundation-card.missing {{ border-left-color: var(--red); }}
    .field {{ margin-top: 9px; }}
    .field b {{ display: block; margin-bottom: 3px; font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: .06em; }}
    .field p {{ margin: 0; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; font-size: 14px; }}
    th, td {{ padding: 10px; border-bottom: 1px solid var(--line); vertical-align: top; text-align: left; }}
    th {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .06em; background: #f0f3f0; }}
    .chip {{ display: inline-flex; padding: 2px 7px; border-radius: 999px; background: #edf3f1; color: #2a5146; font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; }}
    .detail-link {{ display: inline-flex; margin-top: 8px; padding: 7px 10px; color: #fff; background: var(--charcoal); text-decoration: none; border-radius: 6px; font-size: 13px; font-weight: 700; }}
    .detail-link:hover {{ background: var(--green); }}
    .status-evidenced {{ color: var(--green); font-weight: 700; }}
    .status-partial {{ color: var(--amber); font-weight: 700; }}
    .status-missing, .impact-weakening {{ color: var(--red); font-weight: 700; }}
    .impact-strengthening {{ color: var(--green); font-weight: 700; }}
    .impact-research_lead {{ color: var(--amber); font-weight: 700; }}
    .question {{ border-left: 5px solid var(--blue); }}
    .question h3 {{ font-size: 18px; }}
    .note {{ color: var(--muted); font-size: 13px; }}
    ul {{ margin: 8px 0 0; padding-left: 20px; }}
    li {{ margin: 5px 0; }}
    @media (max-width: 880px) {{
      .summary-grid, .grid, .foundation-grid, .committee {{ grid-template-columns: 1fr; }}
      table {{ font-size: 13px; }}
    }}
  </style>
  <style>{_apple_research_css()}</style>
</head>
<body>
  <header>
    <p class="eyebrow">L0 / 公司基础框架</p>
    <h1>{escape(ticker)} 公司基础框架</h1>
    <p class="subtitle">当前页面只保留问题结构：当前要研究的问题、L1 子问题、子结构汇总结论和详情页跳转。</p>
  </header>
  <nav>
    <a href="#current-question">当前问题</a>
    <a href="#foundation">子问题</a>
    <a href="#add-question">新增问题</a>
  </nav>
  <main>
    <section id="current-question">
      <div class="layer-label">当前要研究的问题</div>
      <h2>{escape(current_question)}</h2>
      <div class="rule-box"><p>{escape(l0_summary)}</p></div>
    </section>

    <section id="foundation">
      <div class="layer-label">子问题列表</div>
      <h2>L1 子问题</h2>
      <div class="foundation-grid">{section_cards}</div>
    </section>

    {add_question_box}
  </main>
  <script>{_draft_question_js()}</script>
</body>
</html>
"""


def _render_foundation_detail_page(
    ticker: str,
    section: dict[str, Any],
    evidence: list[EvidenceRecord],
) -> str:
    section_label = SECTION_LABEL_ZH.get(section["label"], section["label"])
    status_label = _zh_text(section["status"])
    key_questions = _render_statement_list(section.get("key_questions", []), "尚未定义本板块关键问题。")
    facts = _render_statement_list(
        [
            f"{_zh_text(fact['statement'])} [{fact['evidence_id']}]"
            for fact in section.get("facts", [])
        ],
        "No local fact evidence yet.",
    )
    inferences = _render_statement_list(section.get("inferences", []), "No inference until evidence is added.")
    judgments = _render_statement_list(section.get("judgments", []), "No judgment until evidence is added.")
    gaps = _render_statement_list(section.get("gaps", []), "No material gap flagged.")
    information_tables = _render_information_category_tables(section)
    evidence_records = _records_for_ids(evidence, section.get("evidence_ids", []))
    evidence_rows = "\n".join(_render_evidence_record_row(record) for record in evidence_records)
    evidence_rows = evidence_rows or '<tr><td colspan="6" class="note">当前没有可展示证据。</td></tr>'

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(ticker)} {escape(section_label)}</title>
  <style>
    :root {{
      --ink: #17202a;
      --muted: #62707c;
      --paper: #f6f3ea;
      --panel: #fffdfa;
      --line: #d9ded8;
      --green: #1f7a5c;
      --amber: #b66a18;
      --red: #b2473e;
      --blue: #2d5d8f;
      --charcoal: #121a22;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; color: var(--ink); background: var(--paper); font-family: "Avenir Next", "Gill Sans", "PingFang SC", "Microsoft YaHei", sans-serif; line-height: 1.62; }}
    header {{ padding: 34px clamp(18px, 5vw, 64px) 26px; color: #fff; background: var(--charcoal); border-bottom: 7px solid var(--green); }}
    h1 {{ margin: 0; font-size: clamp(34px, 5.4vw, 62px); line-height: 1; letter-spacing: 0; }}
    h2 {{ margin: 0 0 12px; font-size: clamp(22px, 3vw, 34px); letter-spacing: 0; }}
    h3 {{ margin: 0 0 8px; font-size: 18px; }}
    p {{ margin: 0 0 10px; }}
    a {{ color: var(--blue); }}
    .subtitle {{ max-width: 980px; margin-top: 14px; color: #d8e1dd; font-size: 17px; }}
    .nav {{ position: sticky; top: 0; z-index: 10; display: flex; gap: 8px; overflow-x: auto; padding: 10px clamp(14px, 4vw, 54px); background: rgba(246,243,234,.96); border-bottom: 1px solid var(--line); backdrop-filter: blur(10px); }}
    .nav a {{ flex: 0 0 auto; padding: 7px 10px; color: var(--ink); text-decoration: none; border: 1px solid var(--line); background: #fff; border-radius: 999px; font-size: 13px; font-weight: 700; }}
    main {{ width: min(1160px, calc(100% - 28px)); margin: 22px auto 58px; }}
    section {{ margin: 16px 0; padding: clamp(18px, 3vw, 30px); background: rgba(255,253,250,.95); border: 1px solid var(--line); }}
    .summary-strip {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin-top: 18px; }}
    .metric {{ padding: 14px; background: #fff; border: 1px solid var(--line); min-width: 0; color: var(--ink); }}
    .metric span {{ display: block; color: var(--muted); font-size: 12px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; }}
    .metric strong {{ display: block; margin-top: 6px; font-size: clamp(21px, 2.4vw, 32px); line-height: 1.08; }}
    .lead-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; align-items: start; }}
    .field {{ margin-top: 12px; }}
    .field b {{ display: block; margin-bottom: 4px; color: var(--muted); font-size: 12px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; }}
    .note {{ color: var(--muted); font-size: 13px; }}
    .chip {{ display: inline-flex; max-width: 100%; margin: 2px 4px 2px 0; padding: 2px 7px; border-radius: 999px; background: #edf3f1; color: #2a5146; font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; overflow-wrap: anywhere; }}
    .status-evidenced {{ color: var(--green); font-weight: 800; }}
    .status-partial {{ color: var(--amber); font-weight: 800; }}
    .status-missing {{ color: var(--red); font-weight: 800; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; font-size: 14px; margin-bottom: 16px; }}
    th, td {{ padding: 10px; border-bottom: 1px solid var(--line); vertical-align: top; text-align: left; }}
    th {{ color: var(--muted); font-size: 12px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; background: #eef2ee; }}
    ul {{ margin: 8px 0 0; padding-left: 20px; }}
    li {{ margin: 5px 0; }}
    @media (max-width: 880px) {{ .summary-strip, .lead-grid {{ grid-template-columns: 1fr; }} table {{ font-size: 13px; }} }}
  </style>
  <style>{_apple_research_css()}</style>
</head>
<body>
  <header>
    <h1>{escape(ticker)} {escape(section_label)}</h1>
    <p class="subtitle">该页是八步框架的独立研究单元：先定义关键问题，再把证据、研报、观点和消息分别映射到支撑/反证关系。</p>
    <div class="summary-strip">
      <div class="metric"><span>本节状态</span><strong class="status-{escape(section['status'])}">{escape(status_label)}</strong></div>
      <div class="metric"><span>关键问题</span><strong>{len(section.get("key_questions", []))}</strong></div>
      <div class="metric"><span>信息条目</span><strong>{len(section.get("evidence_ids", []))}</strong></div>
    </div>
  </header>
  <nav class="nav">
    <a href="../research_dashboard.html#foundation">返回总览</a>
    <a href="#questions">关键问题</a>
    <a href="#info-map">四类信息</a>
    <a href="#judgment">判断与缺口</a>
    <a href="#records">信息索引</a>
  </nav>
  <main>
    <section id="questions">
      <h2>这个子板块最关键的问题</h2>
      {key_questions}
    </section>
    <section id="info-map">
      <h2>四类信息如何支撑或反证论点</h2>
      {information_tables}
    </section>
    <section id="judgment">
      <h2>事实、推论、判断、缺口</h2>
      <div class="lead-grid">
        <div>
          <div class="field"><b>事实</b>{facts}</div>
          <div class="field"><b>推论</b>{inferences}</div>
        </div>
        <div>
          <div class="field"><b>判断</b>{judgments}</div>
          <div class="field"><b>缺口</b>{gaps}</div>
        </div>
      </div>
    </section>
    <section id="records">
      <h2>信息索引</h2>
      <table>
        <thead><tr><th>信息 ID</th><th>类别</th><th>来源</th><th>日期</th><th>可靠性 / 重要性</th><th>摘要</th></tr></thead>
        <tbody>{evidence_rows}</tbody>
      </table>
    </section>
  </main>
</body>
</html>
"""


def _render_foundation_qa_page(
    ticker: str,
    foundation_graph: dict[str, Any],
    evidence: list[EvidenceRecord],
    section_id: str,
) -> str:
    section = _foundation_section_by_id(foundation_graph, section_id)
    section_label = SECTION_LABEL_ZH.get(section["label"], section["label"])
    qa_tree = _build_qa_tree(ticker, foundation_graph, evidence)
    section_node_count = sum(1 for node in qa_tree["nodes"] if node.get("section_id") == section_id)
    status_label = _zh_text(section["status"])
    step_index = next(
        (index for index, rule in enumerate(FOUNDATION_SECTIONS, start=1) if rule["id"] == section_id),
        0,
    )
    current_question = _foundation_section_question(section)
    current_summary = _foundation_section_rollup(section)
    l1_overview = _render_l1_overview(section, qa_tree)
    add_question_box = _render_add_question_box(f"{ticker}:l1:{section_id}", f"L1 {section_label}")

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(ticker)} {escape(section_label)} QA Explorer</title>
  <style>{_apple_research_css()}{_qa_explorer_css()}</style>
</head>
<body>
  <header>
    <p class="eyebrow">L1 子页面 / 八步框架第 {step_index} 步</p>
    <h1>{escape(ticker)} L1：{escape(section_label)}</h1>
    <p class="subtitle">本页只保留当前问题、L2 子问题汇总结论、子问题列表、详情页跳转和新增问题框。</p>
    <div class="summary-strip">
      <div class="metric"><span>本节状态</span><strong class="status-{escape(section['status'])}">{escape(status_label)}</strong></div>
      <div class="metric"><span>当前层级</span><strong>L1</strong></div>
      <div class="metric"><span>问题节点</span><strong>{section_node_count}</strong></div>
      <div class="metric"><span>子页面</span><strong>L2</strong></div>
    </div>
  </header>
  <nav class="nav">
    <a href="../research_dashboard.html#foundation">返回总览</a>
    <a href="#current-question">当前问题</a>
    <a href="#l1-questions">子问题</a>
    <a href="#add-question">新增问题</a>
  </nav>
  <main class="qa-full-research">
    <section id="current-question" class="level-frame">
      <p class="eyebrow">当前要研究的问题</p>
      <h2>{escape(current_question)}</h2>
      <div class="rule-box"><p>{escape(_zh_text(current_summary))}</p></div>
    </section>
    {l1_overview}
    {add_question_box}
  </main>
  <script>{_draft_question_js()}</script>
</body>
</html>
"""


def _render_l1_overview(section: dict[str, Any], qa_tree: dict[str, Any]) -> str:
    section_id = section.get("id", "")
    section_label = SECTION_LABEL_ZH.get(section.get("label", ""), section.get("label", ""))
    l2_nodes = _l2_nodes_for_section(qa_tree, section_id)
    nodes_by_id = {node.get("id"): node for node in qa_tree.get("nodes", [])}
    l2_cards = "\n".join(_render_l2_entry_card(section_id, node, nodes_by_id) for node in l2_nodes)
    if not l2_cards:
        l2_cards = '<p class="qa-empty">当前板块尚未生成 L2 问题。</p>'
    return f"""
  <section id="l1-questions" class="qa-full-research level-frame">
    <p class="eyebrow">子问题列表 / {escape(section_label)}</p>
    <h2>L2 子问题</h2>
    <div class="l2-grid">{l2_cards}</div>
  </section>
"""


def _render_l2_entry_card(section_id: str, node: dict[str, Any], nodes_by_id: dict[str, dict[str, Any]]) -> str:
    href = _l2_question_href(section_id, node.get("id", "question"))
    child_nodes = [nodes_by_id[child_id] for child_id in node.get("next_question_ids", []) if child_id in nodes_by_id]
    summary = _truncate_text(_children_summary(child_nodes, nodes_by_id) or _node_summary(node), 230)
    child_items = _render_child_question_list(node, nodes_by_id)
    gap_items = _render_child_gap_list(child_nodes)
    return (
        '<article class="l2-card">'
        '<p class="eyebrow">L2 问题</p>'
        f"<h3>{escape(node.get('question', ''))}</h3>"
        f"<div class=\"field\"><b>子结构汇总结论</b><p>{escape(summary)}</p></div>"
        f"<div class=\"field\"><b>子问题列表</b>{child_items}</div>"
        f"<div class=\"field\"><b>高优先级缺口</b>{gap_items}</div>"
        f"<a class=\"detail-link\" href=\"{escape(href)}\">打开 L2 问题页</a>"
        "</article>"
    )


def _node_summary(node: dict[str, Any]) -> str:
    rollup = _zh_text(node.get("rollup_to_parent", ""))
    answer = _zh_text(node.get("current_answer", ""))
    return rollup or answer or "当前没有形成汇总结论。"


def _children_summary(children: list[dict[str, Any]], nodes_by_id: dict[str, dict[str, Any]]) -> str:
    del nodes_by_id
    summaries: list[str] = []
    for child in children:
        summary = _node_summary(child)
        if not summary or summary == "当前没有形成汇总结论。":
            continue
        question = _truncate_text(child.get("question", ""), 34)
        item = f"{question}：{summary}" if question else summary
        if item not in summaries:
            summaries.append(item)
    return "；".join(_truncate_text(summary, 90) for summary in summaries[:3])


def _render_child_gap_list(children: list[dict[str, Any]]) -> str:
    gaps: list[str] = []
    for child in children:
        for gap in child.get("synthesis", {}).get("gaps", []):
            text = _truncate_text(_zh_text(gap), 82)
            if text and text not in gaps:
                gaps.append(text)
    if not gaps:
        return '<p class="note">暂无明确缺口。</p>'
    return "<ul>" + "".join(f"<li>{escape(gap)}</li>" for gap in gaps[:3]) + "</ul>"


def _section_evidence_summary(section: dict[str, Any]) -> str:
    facts = [
        _zh_text(fact.get("statement", ""))
        for fact in section.get("facts", [])
        if fact.get("statement")
    ]
    if facts:
        return "；".join(_truncate_text(fact, 110) for fact in facts[:2])
    inferences = [_zh_text(item) for item in section.get("inferences", []) if item]
    if inferences:
        return "；".join(_truncate_text(item, 110) for item in inferences[:2])
    return _zh_text(_foundation_section_rollup(section))


def _render_child_question_list(node: dict[str, Any], nodes_by_id: dict[str, dict[str, Any]] | None = None) -> str:
    child_ids = node.get("next_question_ids", [])
    if not child_ids:
        return '<p class="note">暂无子问题，可在下方新增问题。</p>'
    items = []
    for child_id in child_ids:
        child = nodes_by_id.get(child_id) if nodes_by_id else None
        question = child.get("question", child_id) if child else child_id.split(".")[-1]
        items.append(f"<li>{escape(question)}</li>")
    return "<ul>" + "".join(items) + "</ul>"


def _truncate_text(value: str, limit: int) -> str:
    return value if len(value) <= limit else value[: limit - 1] + "…"


def _same_research_text(left: str, right: str) -> bool:
    return re.sub(r"\s+", "", _zh_text(left or "")) == re.sub(r"\s+", "", _zh_text(right or ""))


def _rollup_box_html(label: str, answer: str, rollup: str) -> str:
    if not rollup or _same_research_text(answer, rollup):
        return ""
    return f"<div class=\"qa-rollup\"><strong>{escape(label)}</strong><p>{escape(_zh_text(rollup))}</p></div>"


def _render_l2_question_page(
    ticker: str,
    section: dict[str, Any],
    node: dict[str, Any],
    qa_tree: dict[str, Any],
    evidence: list[EvidenceRecord],
) -> str:
    del evidence
    section_id = section.get("id", "")
    section_label = SECTION_LABEL_ZH.get(section.get("label", ""), section.get("label", ""))
    nodes_by_id = {item.get("id"): item for item in qa_tree.get("nodes", [])}
    l3_nodes = [nodes_by_id[node_id] for node_id in node.get("next_question_ids", []) if node_id in nodes_by_id]
    l3_cards = "\n".join(_render_l3_question_card(child) for child in l3_nodes)
    if not l3_cards:
        l3_cards = '<p class="qa-empty">当前 L2 问题尚未生成 L3 追问。</p>'
    synthesis = node.get("synthesis", {})
    summary = _node_summary(node)
    decision_panel = _render_node_decision_panel(node, title="本层研究判断")
    gap_panel = _render_node_next_steps(node)
    add_question_box = _render_add_question_box(f"{ticker}:l2:{node.get('id', '')}", "L2 问题")
    section_page = f"../{SECTION_ID_TO_PAGE.get(section_id, f'{section_id}.html')}"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(ticker)} L2 {escape(node.get("question", ""))}</title>
  <style>{_apple_research_css()}{_qa_explorer_css()}</style>
</head>
<body>
  <header>
    <p class="eyebrow">L2 问题展开 / {escape(section_label)}</p>
    <h1>{escape(node.get("question", ""))}</h1>
    <p class="subtitle">本页按投研下钻单元展示：当前判断、事实依据、推导逻辑、反证边界、下一步数据和 L3 追问。</p>
    <div class="summary-strip">
      <div class="metric"><span>所属 L1</span><strong>{escape(section_label)}</strong></div>
      <div class="metric"><span>L3 追问</span><strong>{len(l3_nodes)}</strong></div>
      <div class="metric"><span>节点状态</span><strong>{escape(node.get("status", "open"))}</strong></div>
      <div class="metric"><span>置信度</span><strong>{escape(synthesis.get("confidence", "unknown"))}</strong></div>
    </div>
  </header>
  <nav class="nav">
    <a href="../../research_dashboard.html#foundation">返回 L0</a>
    <a href="{escape(section_page)}#l1-questions">返回 L1</a>
    <a href="#current-question">当前问题</a>
    <a href="#l3">子问题</a>
    <a href="#add-question">新增问题</a>
  </nav>
  <main class="qa-full-research">
    <section id="current-question" class="level-frame">
      <p class="eyebrow">当前要研究的问题</p>
      <h2>{escape(node.get("question", ""))}</h2>
      <div class="rule-box"><p>{escape(summary)}</p></div>
      {decision_panel}
      {gap_panel}
    </section>
    <section id="l3" class="level-frame">
      <p class="eyebrow">子问题列表</p>
      <h2>L3 子问题</h2>
      <div class="l2-grid">{l3_cards}</div>
    </section>
    {add_question_box}
  </main>
  <script>{_draft_question_js()}</script>
</body>
</html>
"""


def _render_l2_information_bucket(category: str, items: list[dict[str, Any]]) -> str:
    label = INFO_CATEGORY_LABEL_ZH.get(category, category)
    if not items:
        body = '<p class="qa-empty">暂无映射信息。</p>'
    else:
        rows = []
        for item in items:
            link = ""
            if item.get("url"):
                link = f"<p><a href=\"{escape(item.get('url', ''))}\">{escape(item.get('source_name', '打开来源'))}</a></p>"
            rows.append(
                "<div class=\"qa-evidence-item\">"
                f"<span class=\"chip\">{escape(item.get('evidence_id', ''))}</span>"
                f"<p><strong>{escape(item.get('relation', '信息'))}：</strong>{escape(item.get('point', ''))}</p>"
                f"{link}"
                f"<p class=\"note\">{escape(_zh_text(item.get('summary', '')))}</p>"
                "</div>"
            )
        body = "".join(rows)
    return f"<div class=\"qa-bucket {escape(category)}\"><h4>{escape(label)}</h4>{body}</div>"


def _render_l3_question_card(node: dict[str, Any]) -> str:
    summary = _truncate_text(_node_summary(node), 180)
    decision_panel = _render_node_decision_panel(node, title="研究判断")
    next_steps = _render_node_next_steps(node)
    info_index = _render_l3_information_index(node)
    return (
        '<article class="l2-card research-unit-card">'
        '<p class="eyebrow">L3 子问题</p>'
        f"<h3>{escape(node.get('question', ''))}</h3>"
        f"<div class=\"field\"><b>子结构汇总结论</b><p>{escape(summary)}</p></div>"
        f"{decision_panel}"
        f"{next_steps}"
        f"<div class=\"field\"><b>四类信息索引 / 证据矩阵</b>{info_index}</div>"
        "</article>"
    )


def _render_l3_information_index(node: dict[str, Any]) -> str:
    buckets = node.get("evidence_buckets", {})
    boxes = []
    for category in SOURCE_ORIGIN_INFO_ORDER:
        label = INFO_CATEGORY_LABEL_ZH.get(category, category)
        items = buckets.get(category, [])
        if not items:
            body = '<p class="note">暂无，不能用这一类信息强化判断。</p>'
        else:
            rows = []
            for item in items[:4]:
                point = _truncate_text(item.get("point", ""), 78)
                source_name = _truncate_text(item.get("source_name", "打开来源"), 34)
                link = (
                    f"<a href=\"{escape(item.get('url', ''))}\">{escape(source_name)}</a>"
                    if item.get("url")
                    else escape(source_name)
                )
                missing_note = '<p class="note">来源记录未入库，先作为待补索引保留。</p>' if item.get("missing_record") else ""
                relation = item.get("relation", "信息")
                stance_class = _evidence_stance_class(relation)
                quality = _evidence_quality_label(item)
                rows.append(
                    f"<li class=\"stance-{escape(stance_class)}\">"
                    f"<span class=\"chip\">{escape(item.get('evidence_id', ''))}</span>"
                    f"<span class=\"stance-pill\">{escape(relation)}</span>"
                    f"<span class=\"quality-pill\">{escape(quality)}</span>"
                    f"<p>{escape(point)}</p>"
                    f"<p class=\"note\">{link}</p>"
                    f"{missing_note}"
                    "</li>"
                )
            body = "<ul>" + "".join(rows) + "</ul>"
        boxes.append(f"<div class=\"l3-info-box {escape(category)}\"><h4>{escape(label)}</h4>{body}</div>")
    return f"<div class=\"l3-info-grid\">{''.join(boxes)}</div>"


def _render_node_decision_panel(node: dict[str, Any], title: str) -> str:
    synthesis = node.get("synthesis", {})
    facts = _render_research_list(synthesis.get("facts", []), "暂无关键事实。", limit=3)
    inference = _render_research_list(synthesis.get("inferences", []), "暂无推导逻辑。", limit=2)
    judgment = _zh_text(synthesis.get("judgment", "")) or _node_summary(node)
    confidence = synthesis.get("confidence", "unknown")
    support_count, refute_count, lead_count = _node_evidence_counts(node)
    return (
        '<div class="decision-panel">'
        f"<div class=\"decision-head\"><b>{escape(title)}</b><span>{escape(_confidence_label(confidence))}</span></div>"
        '<div class="decision-grid">'
        f"<div class=\"decision-box judgment\"><h4>当前判断</h4><p>{escape(judgment)}</p></div>"
        f"<div class=\"decision-box\"><h4>关键事实</h4>{facts}</div>"
        f"<div class=\"decision-box\"><h4>推导逻辑</h4>{inference}</div>"
        '<div class="decision-box evidence-score">'
        "<h4>证据结构</h4>"
        f"<p><strong>{support_count}</strong> 支持 / <strong>{refute_count}</strong> 反证 / <strong>{lead_count}</strong> 线索</p>"
        "</div>"
        "</div>"
        "</div>"
    )


def _render_node_next_steps(node: dict[str, Any]) -> str:
    gaps = node.get("synthesis", {}).get("gaps", [])
    gap_text = _zh_text(gaps[0]) if gaps else "暂无明确缺口。"
    next_data = _normalize_next_data(gap_text)
    triggers = _node_update_triggers(node)
    return (
        '<div class="next-step-grid">'
        f"<div class=\"next-step-box\"><b>最大缺口</b><p>{escape(gap_text)}</p></div>"
        f"<div class=\"next-step-box\"><b>下一步数据</b><p>{escape(next_data)}</p></div>"
        f"<div class=\"next-step-box\"><b>更新触发器</b><p>{escape(triggers)}</p></div>"
        "</div>"
    )


def _render_research_list(items: list[str], empty: str, limit: int) -> str:
    values = [_truncate_text(_zh_text(item), 120) for item in items if item]
    if not values:
        return f"<p class=\"note\">{escape(empty)}</p>"
    return "<ul>" + "".join(f"<li>{escape(value)}</li>" for value in values[:limit]) + "</ul>"


def _node_evidence_counts(node: dict[str, Any]) -> tuple[int, int, int]:
    support = refute = lead = 0
    for items in node.get("evidence_buckets", {}).values():
        for item in items:
            relation = item.get("relation", "")
            stance = _evidence_stance_class(relation)
            if stance == "refute":
                refute += 1
            elif stance == "lead":
                lead += 1
            else:
                support += 1
    return support, refute, lead


def _evidence_stance_class(relation: str) -> str:
    if any(token in relation for token in ("反证", "边界", "约束")):
        return "refute"
    if any(token in relation for token in ("线索", "待验证")):
        return "lead"
    return "support"


def _evidence_quality_label(item: dict[str, Any]) -> str:
    if item.get("missing_record"):
        return "待补来源"
    reliability = _zh_text(item.get("reliability", "")) or "未标可靠性"
    materiality = _zh_text(item.get("materiality", "")) or "未标重要性"
    return f"{reliability} / {materiality}"


def _confidence_label(confidence: str) -> str:
    labels = {"high": "高置信", "medium": "中置信", "low": "低置信", "unknown": "未评级"}
    return labels.get(confidence, confidence)


def _normalize_next_data(gap_text: str) -> str:
    text = gap_text.strip()
    for prefix in ("需要补充", "需要补", "需要"):
        if text.startswith(prefix):
            text = text[len(prefix) :].strip("：:，,。 ")
            break
    return text or "等待进一步证据。"


def _node_update_triggers(node: dict[str, Any]) -> str:
    text = f"{node.get('section_id', '')} {node.get('question', '')} {_node_summary(node)}"
    if any(token in text for token in ("EV", "汽车", "交付", "单车", "召回", "安全")):
        return "季度业绩、月度交付、价格调整、召回/监管公告、质保和售后成本披露。"
    if any(token in text for token in ("手机", "MAU", "IoT", "用户", "服务")):
        return "季度业绩、手机份额/出货、MIUI MAU、多设备用户、互联网服务 ARPU。"
    if any(token in text for token in ("治理", "控制权", "管理层", "资本配置", "董事会")):
        return "年报、董事会/股权激励公告、回购分红、重大投资和关联交易披露。"
    if any(token in text for token in ("竞争", "份额", "价格战", "毛利")):
        return "同行业绩、行业份额、价格带变化、促销强度和分业务毛利率。"
    return "季度业绩、重大公告、行业数据、监管公告和高可靠第三方研究更新。"


def _render_add_question_box(scope_id: str, label: str) -> str:
    return f"""
    <section id="add-question" class="level-frame draft-question" data-question-scope="{escape(scope_id)}">
      <p class="eyebrow">可交互 / 新增问题</p>
      <h2>新增下钻问题</h2>
      <form class="draft-question-form">
        <textarea class="draft-question-input" placeholder="输入一个新的下钻问题"></textarea>
        <div class="qa-ask-actions">
          <button class="primary" type="submit">加入本层问题列表</button>
          <button class="draft-question-clear" type="button">清空本层新增</button>
        </div>
      </form>
      <div class="field"><b>{escape(label)}新增问题</b><ul class="draft-question-list"></ul></div>
    </section>
"""


def _draft_question_js() -> str:
    return r"""
    (() => {
      function esc(value) {
        return String(value == null ? "" : value).replace(/[&<>"']/g, (char) => ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        }[char]));
      }
      function read(key) {
        try {
          return JSON.parse(localStorage.getItem(key) || "[]");
        } catch (_error) {
          return [];
        }
      }
      function write(key, value) {
        try {
          localStorage.setItem(key, JSON.stringify(value));
        } catch (_error) {
        }
      }
      document.querySelectorAll("[data-question-scope]").forEach((box) => {
        const key = `draft-layer-questions:${box.dataset.questionScope || "default"}`;
        const form = box.querySelector(".draft-question-form");
        const input = box.querySelector(".draft-question-input");
        const list = box.querySelector(".draft-question-list");
        const clear = box.querySelector(".draft-question-clear");
        const render = () => {
          const items = read(key);
          list.innerHTML = items.length
            ? items.map((item) => `<li>${esc(item)}</li>`).join("")
            : '<li class="note">暂无新增问题。</li>';
        };
        form.addEventListener("submit", (event) => {
          event.preventDefault();
          const value = input.value.trim();
          if (!value) return;
          write(key, [...read(key), value]);
          input.value = "";
          render();
        });
        clear.addEventListener("click", () => {
          write(key, []);
          render();
        });
        render();
      });
    })();
    """


def _render_foundation_complete_research(ticker: str, section: dict[str, Any], evidence: list[EvidenceRecord]) -> str:
    section_id = section.get("id", "")
    if section_id == "source_origin":
        return _render_source_origin_complete_research(ticker, evidence)
    return _render_section_complete_research(ticker, section, evidence)


def _render_section_complete_research(ticker: str, section: dict[str, Any], evidence: list[EvidenceRecord]) -> str:
    section_label = SECTION_LABEL_ZH.get(section.get("label", ""), section.get("label", ""))
    facts = _render_statement_list(
        [
            f"{_zh_text(fact.get('statement', ''))} [{fact.get('evidence_id', '')}]"
            for fact in section.get("facts", [])
        ],
        "当前没有足够事实证据。",
    )
    inferences = _render_statement_list(section.get("inferences", []), "当前不输出推论。")
    judgments = _render_statement_list(section.get("judgments", []), "当前不输出判断。")
    gaps = _render_statement_list(section.get("gaps", []), "当前没有记录重大缺口。")
    questions = _qa_parent_questions_for_section(ticker, section)
    question_cards = "\n".join(_render_foundation_research_question_card(question, evidence) for question in questions)
    information_tables = _render_information_category_tables(section)
    history_block = ""
    if section.get("id") == "history":
        history_block = f"""
    <h2>关键历史阶段</h2>
    <div class="timeline">{_render_history_timeline(ticker, evidence)}</div>
"""
    return f"""
  <section id="full-research" class="qa-full-research">
    <p class="eyebrow">完整研究 / {escape(section_label)}</p>
    <h2>{escape(section_label)}：先给出可上抛结论，再保留证据缺口。</h2>
    <div class="lead-grid">
      <div>
        <div class="field"><b>事实</b>{facts}</div>
        <div class="field"><b>推论</b>{inferences}</div>
      </div>
      <div>
        <div class="field"><b>判断</b>{judgments}</div>
        <div class="field"><b>缺口</b>{gaps}</div>
      </div>
    </div>
    {history_block}
    <h2>本板块关键问题</h2>
    <p class="note">每个问题均按四类信息映射到证据、研报、消息和观点；无法被信息支撑的问题保留为待验证项。</p>
    {question_cards}
    <h2>四类信息映射</h2>
    {information_tables}
  </section>
"""


def _render_foundation_research_question_card(question: dict[str, Any], evidence: list[EvidenceRecord]) -> str:
    bucket_html = "\n".join(
        _render_foundation_info_bucket(category, question.get("info", {}).get(category, []), evidence)
        for category in SOURCE_ORIGIN_INFO_ORDER
    )
    return (
        f"<article class=\"question-card\" id=\"complete-{escape(question['id'])}\">"
        f"<h3>{escape(question['question'])}</h3>"
        f"<div class=\"answer-box\"><strong>当前回答</strong><p>{escape(question['answer'])}</p></div>"
        f"<div class=\"info-grid\">{bucket_html}</div>"
        f"<p class=\"note\"><strong>待验证：</strong>{escape(question['gap'])}</p>"
        "</article>"
    )


def _render_source_origin_complete_research(ticker: str, evidence: list[EvidenceRecord]) -> str:
    if ticker != "XIAOMI":
        return ""
    question_cards_html = _render_source_origin_question_cards(ticker, evidence)
    phase_rows = _render_source_origin_phase_rows(ticker, evidence)
    mechanism_rows = _render_source_origin_mechanism_rows(ticker, evidence)
    return f"""
  <section id="full-research" class="qa-full-research">
    <p class="eyebrow">完整研究 / 源头溯源</p>
    <h2>小米的源头不是“硬件公司成立”，而是用户参与的软件入口、低毛利硬件放大和生态服务变现的组合。</h2>
    {_render_source_origin_thesis(ticker, evidence)}
    <div class="lead-grid">
      <div class="rule-box">
        <h3>当前核心判断</h3>
        <ul>
          <li>事实层：小米 2010 年成立，早期先有 MIUI 私测和米粉社区，再以手机硬件放大用户入口；招股概要把模型拆成硬件、新零售、互联网服务三支柱。</li>
          <li>推论层：小米最初解决的不是单一低价问题，而是“体验、迭代、渠道效率、价格可承受”同时不够好的结构性问题。</li>
          <li>判断层：源头能力可以解释用户体验、产品定义、渠道效率、IoT 生态扩张，但不能直接证明 EV 毛利和安全责任可持续。</li>
        </ul>
      </div>
      <div class="rule-box">
        <h3>主要反证边界</h3>
        <ul>
          <li>硬件净利率承诺说明硬件是获客与信任机制，不应被直接视为高利润池。</li>
          <li>手机基本盘、MIUI/用户规模和互联网服务变现如果持续弱化，源头飞轮会被削弱。</li>
          <li>汽车业务的安全、质量、召回、售后和资本开支责任，需要独立证据，不能由手机时代效率外推。</li>
        </ul>
      </div>
    </div>
    <h2>源头因果链</h2>
    <table>
      <thead><tr><th>阶段</th><th>事实</th><th>研究含义</th><th>证据</th></tr></thead>
      <tbody>{phase_rows}</tbody>
    </table>
    <h2>研究机制拆解</h2>
    <table>
      <thead><tr><th>问题</th><th>当前回答</th><th>为什么重要</th><th>证据</th></tr></thead>
      <tbody>{mechanism_rows}</tbody>
    </table>
    <h2>八个问题的完整研究卡片</h2>
    <p class="note">每张卡片都按“问题、当前回答、证据/研报/消息/观点、待验证缺口”组织；低可靠来源只作为研究线索，不单独强化结论。</p>
    {question_cards_html}
  </section>
"""


def _render_qa_static_index(qa_tree: dict[str, Any], root_node_id: str) -> str:
    nodes = {node["id"]: node for node in qa_tree.get("nodes", [])}
    root = nodes.get(root_node_id)
    if root is None:
        return '<p class="qa-empty">当前板块没有生成子层级。</p>'

    cards: list[str] = []
    for child_id in root.get("next_question_ids", []):
        child = nodes.get(child_id)
        if child is None:
            continue
        grandchildren = [nodes[grand_id] for grand_id in child.get("next_question_ids", []) if grand_id in nodes]
        grandchild_items = "".join(
            f"<li><span>L3</span>{escape(grandchild.get('question', ''))}</li>"
            for grandchild in grandchildren
        )
        if not grandchild_items:
            grandchild_items = '<li><span>L3</span>暂无下钻问题。</li>'
        cards.append(
            '<article class="qa-static-card">'
            f"<h3><span>L2</span>{escape(child.get('question', ''))}</h3>"
            f"<p>{escape(child.get('current_answer', ''))}</p>"
            f"<ul>{grandchild_items}</ul>"
            "</article>"
        )
    if not cards:
        return '<p class="qa-empty">当前板块没有生成子层级。</p>'
    return "\n".join(cards)


def _render_history_page(
    ticker: str,
    foundation_graph: dict[str, Any],
    evidence: list[EvidenceRecord],
) -> str:
    return _render_foundation_qa_page(ticker, foundation_graph, evidence, "history")


def _json_for_script(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")


def _qa_explorer_js() -> str:
    return r"""
    (() => {
      const categoryLabels = { evidence: "证据", research_report: "研报", message: "消息", opinion: "观点" };
      const baseTree = JSON.parse(document.getElementById("qa-data").textContent);
      const configElement = document.getElementById("qa-page-config");
      const pageConfig = JSON.parse(configElement ? configElement.textContent : "{}");
      const pageSectionId = pageConfig.section_id || "history";
      const pageRootId = pageConfig.root_node_id || `foundation.${pageSectionId}`;
      const storageKey = `qa-tree:${baseTree.ticker}:${pageSectionId}`;
      let tree = loadTree();
      let activeId = initialActiveId();

      function cloneBaseTree() {
        return typeof structuredClone === "function" ? structuredClone(baseTree) : JSON.parse(JSON.stringify(baseTree));
      }

      function storageGet() {
        try {
          return localStorage.getItem(storageKey);
        } catch (_error) {
          return null;
        }
      }

      function storageSet(value) {
        try {
          localStorage.setItem(storageKey, value);
        } catch (_error) {
        }
      }

      function storageRemove() {
        try {
          localStorage.removeItem(storageKey);
        } catch (_error) {
        }
      }

      function loadTree() {
        try {
          const saved = JSON.parse(storageGet() || "null");
          if (
            saved &&
            Array.isArray(saved.nodes) &&
            saved.generated_at === baseTree.generated_at &&
            saved.schema_version === baseTree.schema_version &&
            saved.nodes.some((node) => node.id === pageRootId)
          ) {
            return saved;
          }
        } catch (_error) {
        }
        storageRemove();
        return cloneBaseTree();
      }

      function saveTree() {
        storageSet(JSON.stringify(tree));
      }

      function initialActiveId() {
        const hash = decodeURIComponent(window.location.hash || "");
        if (hash.startsWith("#node=")) return hash.slice(6);
        return pageConfig.default_active_node_id || pageRootId || tree.default_active_node_id || "foundation.history";
      }

      function nodeById(id) {
        return tree.nodes.find((node) => node.id === id);
      }

      function childrenOf(id) {
        const node = nodeById(id);
        const ids = node && Array.isArray(node.next_question_ids) ? node.next_question_ids : [];
        return ids.map(nodeById).filter(Boolean);
      }

      function descendantsOf(id) {
        const result = [];
        const walk = (nodeId) => {
          childrenOf(nodeId).forEach((child) => {
            result.push(child);
            walk(child.id);
          });
        };
        walk(id);
        return result;
      }

      function esc(value) {
        return String(value == null ? "" : value).replace(/[&<>"']/g, (char) => ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        }[char]));
      }

      function setActive(id, updateHash = true) {
        if (!nodeById(id)) id = pageConfig.default_active_node_id || pageRootId || tree.default_active_node_id || "foundation.history";
        activeId = id;
        if (updateHash) history.replaceState(null, "", `#node=${encodeURIComponent(id)}`);
        render();
      }

      function renderTreeButtons(container, nodes) {
        container.innerHTML = nodes.map((node) => {
          const activeClass = node.id === activeId ? " active" : "";
          const levelClass = ` qa-level-${Math.min(node.level, 4)}`;
          return `<button class="qa-node-button${activeClass}${levelClass}" data-node-id="${esc(node.id)}"><span class="qa-node-level">L${esc(node.level)}</span>${esc(node.question)}</button>`;
        }).join("");
        container.querySelectorAll("button[data-node-id]").forEach((button) => {
          button.addEventListener("click", () => setActive(button.dataset.nodeId));
        });
      }

      function renderTree() {
        renderTreeButtons(
          document.getElementById("framework-tree"),
          tree.nodes.filter((node) => node.level === 1)
        );
        renderTreeButtons(
          document.getElementById("section-tree"),
          [nodeById(pageRootId), ...descendantsOf(pageRootId)].filter(Boolean)
        );
      }

      function renderList(items, emptyText) {
        if (!items || !items.length) return `<p class="qa-empty">${esc(emptyText)}</p>`;
        return `<ul>${items.map((item) => `<li>${esc(item)}</li>`).join("")}</ul>`;
      }

      function renderSynthesis(node) {
        const synthesis = node.synthesis || {};
        const boxes = [
          ["事实", synthesis.facts || [], "暂无事实。"],
          ["推论", synthesis.inferences || [], "暂无推论。"],
          ["判断", synthesis.judgment ? [synthesis.judgment] : [], "暂无判断。"],
          ["缺口", synthesis.gaps || [], "暂无缺口。"],
        ];
        document.getElementById("active-synthesis").innerHTML = boxes.map(([title, items, emptyText]) => (
          `<div class="qa-synthesis-box"><h4>${esc(title)}</h4>${renderList(items, emptyText)}</div>`
        )).join("");
      }

      function renderChildren(node) {
        const children = childrenOf(node.id);
        const container = document.getElementById("active-children");
        if (!children.length) {
          container.innerHTML = '<p class="qa-empty">暂无下钻问题。可以在右侧继续追问。</p>';
          return;
        }
        container.innerHTML = children.map((child) => (
          `<button data-node-id="${esc(child.id)}"><span class="qa-node-level">L${esc(child.level)}</span>${esc(child.question)}</button>`
        )).join("");
        container.querySelectorAll("button[data-node-id]").forEach((button) => {
          button.addEventListener("click", () => setActive(button.dataset.nodeId));
        });
      }

      function renderBuckets(node) {
        const buckets = node.evidence_buckets || {};
        const order = (tree.interaction_contract && tree.interaction_contract.information_categories) || ["evidence", "research_report", "message", "opinion"];
        document.getElementById("active-buckets").innerHTML = order.map((category) => {
          const items = buckets[category] || [];
          const body = items.length ? items.map((item) => (
            `<div class="qa-evidence-item">
              <span class="chip">${esc(item.evidence_id)}</span>
              <p><strong>${esc(item.relation || "信息")}：</strong>${esc(item.point || "")}</p>
              ${item.url ? `<p><a href="${esc(item.url)}">${esc(item.source_name || "打开来源")}</a></p>` : ""}
              <p class="note">${esc(item.summary || "")}</p>
            </div>`
          )).join("") : '<p class="qa-empty">暂无映射信息。</p>';
          return `<div class="qa-bucket ${esc(category)}"><h4>${esc(categoryLabels[category] || category)}</h4>${body}</div>`;
        }).join("");
      }

      function renderActive() {
        const node = nodeById(activeId) || nodeById(pageRootId) || nodeById(tree.default_active_node_id);
        if (!node) return;
        document.getElementById("active-level").textContent = `L${node.level}`;
        document.getElementById("active-status").textContent = node.status || "open";
        document.getElementById("active-question").textContent = node.question;
        document.getElementById("active-answer").textContent = node.current_answer || "待研究。";
        document.getElementById("active-rollup").textContent = node.rollup_to_parent || "当前节点尚未形成可上抛结论。";
        renderSynthesis(node);
        renderChildren(node);
        renderBuckets(node);
      }

      function render() {
        renderTree();
        renderActive();
      }

      document.getElementById("ask-form").addEventListener("submit", (event) => {
        event.preventDefault();
        const input = document.getElementById("ask-input");
        const question = input.value.trim();
        if (!question) return;
        const parent = nodeById(activeId) || nodeById(tree.default_active_node_id);
        const id = `draft.${parent.id}.${Date.now()}`;
        const node = {
          id,
          level: parent.level + 1,
          parent_id: parent.id,
          section_id: parent.section_id || "history",
          question,
          current_answer: "待研究：需要先搜集四类信息，再形成事实、推论、判断和缺口。",
          evidence_buckets: { evidence: [], research_report: [], message: [], opinion: [] },
          synthesis: {
            facts: [],
            inferences: [],
            judgment: "本地追问草稿，尚未形成判断。",
            gaps: ["需要补充证据、研报、消息或观点后再上抛结论。"],
            confidence: "low"
          },
          rollup_to_parent: "待上抛：该追问尚未完成信息搜集。",
          next_question_ids: [],
          status: "draft"
        };
        parent.next_question_ids = Array.from(new Set([...(parent.next_question_ids || []), id]));
        tree.nodes.push(node);
        input.value = "";
        saveTree();
        setActive(id);
      });

      document.getElementById("clear-drafts").addEventListener("click", () => {
        storageRemove();
        tree = cloneBaseTree();
        activeId = pageConfig.default_active_node_id || pageRootId || tree.default_active_node_id || "foundation.history";
        history.replaceState(null, "", "#workspace");
        render();
      });

      render();
    })();
    """


def _render_history_timeline(ticker: str, evidence: list[EvidenceRecord]) -> str:
    rows = _history_timeline_rows(ticker)
    return "\n".join(
        '<div class="timeline-row">'
        f'<div class="timeline-year">{escape(row["period"])}</div>'
        "<div>"
        f'<h3>{escape(row["title"])}</h3>'
        f'<p>{escape(row["meaning"])}</p>'
        f'<p>{_chips(row["evidence_ids"], evidence)}</p>'
        "</div>"
        "</div>"
        for row in rows
    )


def _history_timeline_rows(ticker: str) -> list[dict[str, Any]]:
    if ticker == "XIAOMI":
        return [
            {
                "period": "2010-2011",
                "title": "创立、MIUI 与第一代小米手机",
                "meaning": "历史起点是软件体验、用户参与和线上高性价比硬件的组合，而不是单纯硬件制造。",
                "evidence_ids": ["ev_xiaomi_company_profile_20260518", "ev_xiaomi_profile", "ev_xiaomi_mi1_launch_transcript_20110816"],
            },
            {
                "period": "2013-2018",
                "title": "手机规模化、IoT 生态与港股上市",
                "meaning": "手机入口开始外溢为智能硬件、IoT 平台和互联网服务，并在 2018 年上市时固化为公开公司叙事和 WVR 治理结构。",
                "evidence_ids": ["ev_xiaomi_ipo_prospectus_20180625", "ev_xiaomi_jingzhun_deep_report_20181105"],
            },
            {
                "period": "2019-2021",
                "title": "手机 x AIoT 与智能电动车战略启动",
                "meaning": "公司从消费电子平台向更复杂的智能制造和长期资本投入方向延伸，历史问题转向能力迁移是否成立。",
                "evidence_ids": ["ev_xiaomi_guosheng_deep_report_20211117", "ev_xiaomi_yongxing_deep_report_20250228"],
            },
            {
                "period": "2024-2025",
                "title": "EV 进入交付和财务报表",
                "meaning": "智能 EV 不再只是战略叙事，而开始影响收入结构、毛利结构、资本开支和风险责任。",
                "evidence_ids": ["ev_xiaomi_2025_results_announcement_20260324", "ev_xiaomi_segments", "ev_xiaomi_cnevpost_nev_share_20260112"],
            },
            {
                "period": "2025-2026",
                "title": "集团规模扩大，手机基本盘承压",
                "meaning": "历史主线需要同时看第二曲线和基本盘：EV 放量不能掩盖手机出货、份额、毛利与服务入口的变化。",
                "evidence_ids": ["ev_xiaomi_2025_annual_report_20260428", "ev_xiaomi_idc_q1_2026_smartphone_20260512", "ev_xiaomi_smartphone_share"],
            },
            {
                "period": "2025",
                "title": "SU7 召回暴露新业务责任边界",
                "meaning": "汽车业务把公司带入安全、监管、质保、售后和召回成本的历史阶段，不能再按轻互联网逻辑外推。",
                "evidence_ids": ["ev_xiaomi_samr_su7_recall_20250919", "ev_xiaomi_recall"],
            },
        ]
    return [
        {
            "period": "待补",
            "title": "尚未形成可验证历史阶段",
            "meaning": "需要先补充创立、融资、上市、业务转型和重大资本配置证据。",
            "evidence_ids": [],
        }
    ]


def _render_history_question_cards(ticker: str, evidence: list[EvidenceRecord]) -> str:
    return "\n".join(_render_history_question_card(question, evidence) for question in _history_questions(ticker))


def _render_history_question_card(question: dict[str, Any], evidence: list[EvidenceRecord]) -> str:
    bucket_html = "\n".join(
        _render_foundation_info_bucket(category, question.get("info", {}).get(category, []), evidence)
        for category in SOURCE_ORIGIN_INFO_ORDER
    )
    return (
        f"<article class=\"history-card question-card\" id=\"{escape(question['id'])}\">"
        f"<h3>{escape(question['question'])}</h3>"
        f"<div class=\"answer-box\"><strong>当前回答</strong><p>{escape(question['answer'])}</p></div>"
        f"<div class=\"info-grid\">{bucket_html}</div>"
        f"<p class=\"note\"><strong>待验证：</strong>{escape(question['gap'])}</p>"
        "</article>"
    )


def _history_questions(ticker: str) -> list[dict[str, Any]]:
    if ticker == "XIAOMI":
        return [
            {
                "id": "h1-model-shift",
                "question": "哪些历史节点真正改变了商业模型？",
                "answer": "当前可识别的模型拐点是：MIUI/手机入口、IoT 生态、互联网服务变现、智能 EV。每个节点都应验证是否改变利润池，而不是只看收入规模。",
                "gap": "需要补每个阶段的分部收入、毛利、用户规模、现金流和再投资数据。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_ipo_prospectus_20180625", "支撑", "招股书定义手机、智能硬件和 IoT 平台连接的原始模型。"),
                        _foundation_info("ev_xiaomi_2025_results_announcement_20260324", "支撑", "FY2025 业绩公告显示手机 x AIoT 与 EV/AI 新业务已经分部化。"),
                        _foundation_info("ev_xiaomi_segments", "支撑", "测试样本：提供手机、IoT、服务和 EV 规模数据。"),
                    ],
                    "research_report": [
                        _foundation_info("ev_xiaomi_jingzhun_deep_report_20181105", "支撑", "研报把手机硬件、IoT 生态和互联网变现放在同一模型里。"),
                        _foundation_info("ev_xiaomi_yongxing_deep_report_20250228", "支撑", "研报把人车家生态连接到当前业务构成。"),
                    ],
                    "message": [
                        _foundation_info("ev_xiaomi_mi1_launch_transcript_20110816", "支撑", "早期发布会实录可验证第一产品阶段。"),
                    ],
                    "opinion": [],
                },
            },
            {
                "id": "h2-growth-source",
                "question": "历史增长主要来自内生能力、融资环境，还是跨品类扩张？",
                "answer": "当前判断是三者叠加：早期依靠产品和渠道效率，上市后通过公开资本市场和生态扩品类增强资源，2021 年后 EV 使增长更多依赖长期资本投入和制造执行。",
                "gap": "需要补融资节奏、现金资源、资本开支、研发投入、回购/分红和 EV 投入回报序列。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_ipo_prospectus_20180625", "支撑", "招股书确认上市融资和 WVR 风险披露。"),
                        _foundation_info("ev_xiaomi_2025_annual_report_20260428", "支撑", "年报提供 FY2025 收入、利润、现金资源和经营现金流。"),
                        _foundation_info("ev_xiaomi_annual", "支撑", "测试样本：提供收入、利润、现金流和资本开支。"),
                    ],
                    "research_report": [
                        _foundation_info("ev_xiaomi_guosheng_deep_report_20211117", "支撑", "研报将 2021 年进入智能电动车纳入阶段化演进。"),
                        _foundation_info("ev_xiaomi_yongxing_deep_report_20250228", "支撑", "研报把新业务与当前生态结构连接。"),
                    ],
                    "message": [],
                    "opinion": [],
                },
            },
            {
                "id": "h3-governance-capital",
                "question": "治理结构如何影响历史资本配置？",
                "answer": "小米历史上采用不同投票权结构，创始人控制权提高战略耐心，但也要求投资者持续验证重大投入是否受足够约束，尤其是 EV 这类高资本强度业务。",
                "gap": "需要补董事会变化、股权激励、回购分红、重大投资审批和少数股东保护资料。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_board_wvr_20260428", "支撑/约束", "年报披露 WVR 和雷军投票权。"),
                        _foundation_info("ev_xiaomi_governance", "支撑/约束", "测试样本：披露雷军投票权和少数股东治理风险。"),
                        _foundation_info("ev_xiaomi_management_20260518", "支撑", "管理层页面确认核心创始人与高管结构。"),
                    ],
                    "research_report": [
                        _foundation_info("ev_xiaomi_guosheng_deep_report_20211117", "研究线索", "研报阶段复盘可辅助定位治理与战略转向节点。"),
                    ],
                    "message": [],
                    "opinion": [],
                },
            },
            {
                "id": "h4-ev-transition",
                "question": "EV 转型是能力延伸，还是能力跃迁？",
                "answer": "EV 是从手机/AIoT 用户体验和生态能力出发的延伸，但在制造、质量、安全、售后和监管责任上属于能力跃迁，不能用早期互联网效率直接证明。",
                "gap": "需要补 EV 研发投入、产能爬坡、单车经济、售后成本、质保计提和召回成本。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_2025_results_announcement_20260324", "支撑", "业绩公告显示 EV 已进入收入和交付结构。"),
                        _foundation_info("ev_xiaomi_samr_su7_recall_20250919", "反证/边界", "召回公告验证 EV 安全和监管责任边界。"),
                        _foundation_info("ev_xiaomi_recall", "反证/边界", "测试样本：召回信息验证新业务风险边界。"),
                    ],
                    "research_report": [
                        _foundation_info("ev_xiaomi_yongxing_deep_report_20250228", "支撑", "研报把早期手机/AIoT 基因与 EV 和人车家生态连接。"),
                    ],
                    "message": [],
                    "opinion": [],
                },
            },
            {
                "id": "h5-disconfirming-history",
                "question": "哪些历史风险会反证当前叙事？",
                "answer": "需要重点盯三类反证：手机基本盘持续弱化、EV 放量但单车经济和安全成本恶化、控制权结构导致资本配置缺乏约束。",
                "gap": "需要把季度手机份额、EV 交付/毛利、召回/质保、现金流和资本开支串成持续监控表。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_idc_q1_2026_smartphone_20260512", "反证/边界", "IDC 数据显示 Q1 2026 手机出货和份额承压。"),
                        _foundation_info("ev_xiaomi_smartphone_share", "反证/边界", "测试样本：显示手机出货同比下滑。"),
                        _foundation_info("ev_xiaomi_samr_su7_recall_20250919", "反证/边界", "召回公告提示 EV 安全成本可能改变历史叙事。"),
                        _foundation_info("ev_xiaomi_board_wvr_20260428", "约束", "控制权结构要求持续验证资本配置纪律。"),
                    ],
                    "research_report": [
                        _foundation_info("ev_xiaomi_shenwan_deep_report_20241118", "研究线索", "低可靠报告摘要只能提示阶段变化，不能作为结论证据。"),
                    ],
                    "message": [],
                    "opinion": [],
                },
            },
        ]
    return [
        {
            "id": "h1-model-shift",
            "question": "哪些历史节点真正改变了商业模型？",
            "answer": "当前证据不足。需要先补齐创立、融资、上市、业务转型和重大资本配置证据。",
            "gap": "补充公司年报、招股书、重大公告、研报和行业数据。",
            "info": {"evidence": [], "research_report": [], "message": [], "opinion": []},
        }
    ]


def _history_drilldown_questions(ticker: str) -> dict[str, list[dict[str, Any]]]:
    if ticker != "XIAOMI":
        return {}
    return {
        "h1-model-shift": [
            {
                "id": "profit-pool",
                "question": "每次历史转型是否真的改变利润池？",
                "answer": "手机和 IoT 更像用户入口与生态扩张，互联网服务承担高毛利变现，EV 仍需验证上市初期之后的单车经济。",
                "gap": "需要按阶段补分部毛利、互联网服务收入结构、EV 单车毛利和售后成本。",
                "rollup": "历史转型不能只看收入规模，必须验证利润池是否迁移。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_2025_results_announcement_20260324", "支撑", "业绩公告提供手机、IoT、MAU、EV 交付和新业务收入。"),
                        _foundation_info("ev_xiaomi_segments", "支撑", "测试样本：提供手机、IoT、互联网服务和 EV 规模指标。"),
                    ],
                    "research_report": [
                        _foundation_info("ev_xiaomi_jingzhun_deep_report_20181105", "支撑", "研报把硬件放量、IoT 生态和互联网变现放在同一模型里。"),
                    ],
                    "message": [],
                    "opinion": [],
                },
            },
            {
                "id": "model-breakpoints",
                "question": "哪些节点只是规模扩大，哪些节点是模型切换？",
                "answer": "MIUI/手机、IoT、互联网服务、EV 是模型相关节点；单纯销量、发布会或短期热点不能自动视为模型切换。",
                "gap": "需要建立事件到业务模型的映射表，剔除不改变经济性的事件。",
                "rollup": "历史节点需要按模型影响分级，而不是按新闻热度排序。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_ipo_prospectus_20180625", "支撑", "招股书定义原始模型。"),
                    ],
                    "research_report": [
                        _foundation_info("ev_xiaomi_yongxing_deep_report_20250228", "支撑", "研报把当前人车家生态连接到业务构成。"),
                    ],
                    "message": [
                        _foundation_info("ev_xiaomi_mi1_launch_transcript_20110816", "支撑", "早期发布会验证第一产品节点。"),
                    ],
                    "opinion": [],
                },
            },
        ],
        "h2-growth-source": [
            {
                "id": "capital-allocation",
                "question": "历史增长消耗了多少资本，回报是否足够？",
                "answer": "现有年报能看到集团现金和利润，但还不足以判断 EV 及新业务投入的长期回报。",
                "gap": "需要补分业务资本开支、研发投入、经营现金流桥接、回购分红和新业务亏损/毛利。",
                "rollup": "增长质量必须从资本消耗和回报验证，不能只看收入增速。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_2025_annual_report_20260428", "支撑", "年报提供集团收入、利润、现金资源和经营现金流。"),
                        _foundation_info("ev_xiaomi_annual", "支撑", "测试样本：提供资本开支线索。"),
                    ],
                    "research_report": [
                        _foundation_info("ev_xiaomi_yongxing_deep_report_20250228", "研究线索", "研报提示新业务和人车家生态扩张。"),
                    ],
                    "message": [],
                    "opinion": [],
                },
            },
            {
                "id": "internal-vs-external",
                "question": "增长来自公司能力，还是行业周期和融资窗口？",
                "answer": "早期更依赖产品和渠道效率，上市后资本市场资源增强，EV 阶段更受行业竞争、资本开支和制造能力约束。",
                "gap": "需要加入行业周期、同行份额、融资环境和资本成本的对照。",
                "rollup": "历史增长来源应拆为内生能力、外部窗口和资本投入三部分。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_ipo_prospectus_20180625", "支撑", "招股书确认上市窗口与原始业务模型。"),
                    ],
                    "research_report": [
                        _foundation_info("ev_xiaomi_guosheng_deep_report_20211117", "支撑", "研报将 2021 年进入智能电动车纳入阶段化演进。"),
                    ],
                    "message": [],
                    "opinion": [],
                },
            },
        ],
        "h3-governance-capital": [
            {
                "id": "control-discipline",
                "question": "创始人控制权提高战略耐心，还是放大资本配置风险？",
                "answer": "WVR 结构能支持长期投入，但对少数股东而言，关键在重大资本配置是否有足够披露、约束和回报验证。",
                "gap": "需要补董事会独立性、重大投资审批、股权激励、回购分红和关联交易历史。",
                "rollup": "治理结构本身不是结论，必须落到资本配置纪律上验证。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_board_wvr_20260428", "支撑/约束", "年报披露 WVR 与雷军投票权。"),
                        _foundation_info("ev_xiaomi_governance", "支撑/约束", "测试样本：披露少数股东治理风险。"),
                    ],
                    "research_report": [],
                    "message": [],
                    "opinion": [],
                },
            },
            {
                "id": "management-evolution",
                "question": "管理层演进是否匹配业务复杂度上升？",
                "answer": "管理层已覆盖手机、国际、中国区、财务、研发和技术委员会等职能，但 EV 后还需要验证汽车制造和安全管理能力。",
                "gap": "需要补汽车业务核心团队、质量管理、售后体系和激励机制资料。",
                "rollup": "组织能力是否升级，要与业务复杂度同步验证。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_management_20260518", "支撑", "管理层页面确认高管结构。"),
                    ],
                    "research_report": [
                        _foundation_info("ev_xiaomi_yongxing_deep_report_20250228", "研究线索", "研报提示人车家生态对组织能力的要求。"),
                    ],
                    "message": [],
                    "opinion": [],
                },
            },
        ],
        "h4-ev-transition": [
            {
                "id": "transferable-capabilities",
                "question": "手机/AIoT 的哪些能力可以迁移到 EV？",
                "answer": "用户体验、生态连接、软件迭代、品牌流量和供应链组织可以部分迁移，但只能解释获客和体验，不能直接证明汽车利润。",
                "gap": "需要补订单结构、用户来源、软件使用、渠道触点和复购/转介绍证据。",
                "rollup": "EV 可迁移能力主要在用户体验和生态入口，不等于制造能力已验证。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_2025_results_announcement_20260324", "支撑", "业绩公告显示 EV 已形成交付规模。"),
                    ],
                    "research_report": [
                        _foundation_info("ev_xiaomi_yongxing_deep_report_20250228", "支撑", "研报连接手机/AIoT 基因与人车家生态。"),
                    ],
                    "message": [],
                    "opinion": [],
                },
            },
            {
                "id": "non-transferable-capabilities",
                "question": "哪些能力不能从手机时代直接迁移？",
                "answer": "汽车安全、质量冗余、售后服务、召回处置和监管响应不能从互联网效率直接迁移，必须重新建立证据。",
                "gap": "需要补质量事故、召回成本、售后网络、质保计提和监管公告序列。",
                "rollup": "EV 的不可迁移能力是历史分析中的关键反证边界。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_samr_su7_recall_20250919", "反证/边界", "召回公告验证安全和监管责任边界。"),
                        _foundation_info("ev_xiaomi_recall", "反证/边界", "测试样本：召回信息验证新业务风险边界。"),
                    ],
                    "research_report": [],
                    "message": [],
                    "opinion": [],
                },
            },
            {
                "id": "unit-economics",
                "question": "EV 单车经济是否已经证明模型成立？",
                "answer": "当前只能证明 EV 已经进入收入和交付结构，不能证明上市初期之后单车毛利、质保和售后成本可持续。",
                "gap": "需要补单车收入、单车毛利、价格调整、订单等待周期、产能利用率和售后成本。",
                "rollup": "EV 历史转型要等单车经济穿越初期交付阶段后再判断。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_2025_results_announcement_20260324", "支撑", "业绩公告提供 EV 收入和交付规模。"),
                    ],
                    "research_report": [
                        _foundation_info("ev_xiaomi_yongxing_deep_report_20250228", "研究线索", "研报提示 EV 与人车家生态的连接。"),
                    ],
                    "message": [],
                    "opinion": [],
                },
            },
        ],
        "h5-disconfirming-history": [
            {
                "id": "phone-base",
                "question": "手机基本盘弱化会不会反证生态叙事？",
                "answer": "如果手机份额、出货和毛利持续承压，用户入口和服务变现基础可能弱化，需要作为历史叙事的反证。",
                "gap": "需要连续季度手机出货、份额、ASP、毛利、库存和服务 MAU/ARPU 数据。",
                "rollup": "手机基本盘仍是历史叙事的关键底座。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_idc_q1_2026_smartphone_20260512", "反证/边界", "IDC 数据显示 Q1 2026 手机出货和份额承压。"),
                        _foundation_info("ev_xiaomi_smartphone_share", "反证/边界", "测试样本：显示手机出货同比下滑。"),
                    ],
                    "research_report": [],
                    "message": [],
                    "opinion": [],
                },
            },
            {
                "id": "safety-cost",
                "question": "召回和安全成本是否会改变 EV 历史叙事？",
                "answer": "召回本身不一定否定 EV 转型，但如果质保、召回、保险和品牌信任成本随交付放大，会改变转型质量。",
                "gap": "需要补召回完成率、成本计提、事故/投诉、保险费用和用户满意度。",
                "rollup": "安全成本是 EV 转型能否成为正向历史节点的关键反证条件。",
                "info": {
                    "evidence": [
                        _foundation_info("ev_xiaomi_samr_su7_recall_20250919", "反证/边界", "召回公告提示安全和监管成本。"),
                    ],
                    "research_report": [],
                    "message": [],
                    "opinion": [],
                },
            },
        ],
    }


def _history_evidence_ids(ticker: str) -> list[str]:
    if ticker == "XIAOMI":
        return [
            "ev_xiaomi_company_profile_20260518",
            "ev_xiaomi_profile",
            "ev_xiaomi_ipo_prospectus_20180625",
            "ev_xiaomi_mi1_launch_transcript_20110816",
            "ev_xiaomi_jingzhun_deep_report_20181105",
            "ev_xiaomi_guosheng_deep_report_20211117",
            "ev_xiaomi_yongxing_deep_report_20250228",
            "ev_xiaomi_shenwan_deep_report_20241118",
            "ev_xiaomi_2025_annual_report_20260428",
            "ev_xiaomi_annual",
            "ev_xiaomi_2025_results_announcement_20260324",
            "ev_xiaomi_segments",
            "ev_xiaomi_board_wvr_20260428",
            "ev_xiaomi_governance",
            "ev_xiaomi_idc_q1_2026_smartphone_20260512",
            "ev_xiaomi_smartphone_share",
            "ev_xiaomi_samr_su7_recall_20250919",
            "ev_xiaomi_recall",
        ]
    return []


def _foundation_info(evidence_id: str, relation: str, point: str) -> dict[str, str]:
    return {"evidence_id": evidence_id, "relation": relation, "point": point}


def _render_source_origin_page(
    ticker: str,
    foundation_graph: dict[str, Any],
    evidence: list[EvidenceRecord],
) -> str:
    section = _foundation_section_by_id(foundation_graph, "source_origin")
    evidence_by_id = {record.id: record for record in evidence}
    section_records = [evidence_by_id[eid] for eid in section.get("evidence_ids", []) if eid in evidence_by_id]
    primary_records = section_records or evidence[:4]
    company_name = "小米" if ticker == "XIAOMI" else ticker
    question_cards_html = _render_source_origin_question_cards(ticker, evidence)
    fact_items = [
        f"{_zh_text(fact['statement'])} [{fact['evidence_id']}]"
        for fact in section.get("facts", [])
    ]
    facts = _render_statement_list(fact_items, "No local fact evidence yet.")
    inferences = _render_statement_list(section.get("inferences", []), "No inference until evidence is added.")
    judgments = _render_statement_list(section.get("judgments", []), "No judgment until evidence is added.")
    gaps = _render_statement_list(
        section.get("gaps", [])
        + [
            "补充早期 MIUI / 社区 / 首批用户资料，验证最初获客不是事后叙事。",
            "补充早期硬件毛利、互联网服务变现和现金转换资料，判断原始模型的经济性。",
            "把早期互联网效率基因与今天 EV 的制造、安全、售后责任分开验证。",
        ],
        "No material gap flagged.",
    )
    evidence_rows = "\n".join(_render_evidence_record_row(record) for record in primary_records)
    evidence_rows = evidence_rows or '<tr><td colspan="6" class="note">当前没有可展示证据。</td></tr>'

    status_label = _zh_text(section["status"])
    evidence_count = len(section.get("evidence_ids", []))
    generated_at = escape(foundation_graph.get("generated_at", ""))

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(ticker)} 源头溯源</title>
  <style>
    :root {{
      --ink: #1d1d1f;
      --muted: #6e6e73;
      --paper: #f5f5f7;
      --panel: #ffffff;
      --panel-soft: #fbfbfd;
      --line: #d2d2d7;
      --blue: #0066cc;
      --green: #248a3d;
      --amber: #a86600;
      --red: #d70015;
      --shadow: 0 18px 50px rgba(0, 0, 0, .08);
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: var(--paper);
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.55;
    }}
    header {{
      padding: clamp(52px, 8vw, 104px) clamp(20px, 6vw, 86px) 34px;
      color: var(--ink);
      background:
        linear-gradient(180deg, #fff 0%, #f8f8fa 72%, var(--paper) 100%);
      border-bottom: 1px solid rgba(0, 0, 0, .06);
    }}
    .eyebrow {{ margin: 0 0 12px; color: var(--blue); font-size: 13px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }}
    h1 {{ max-width: 980px; margin: 0; font-size: clamp(46px, 7vw, 86px); font-weight: 700; line-height: .98; letter-spacing: 0; }}
    h2 {{ margin: 0 0 12px; font-size: clamp(28px, 4vw, 48px); font-weight: 700; letter-spacing: 0; }}
    h3 {{ margin: 0 0 10px; font-size: clamp(22px, 2.3vw, 30px); font-weight: 700; letter-spacing: 0; }}
    p {{ margin: 0 0 10px; }}
    a {{ color: var(--blue); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .subtitle {{ max-width: 900px; margin-top: 18px; color: var(--muted); font-size: clamp(18px, 2.1vw, 24px); line-height: 1.45; }}
    .nav {{
      position: sticky;
      top: 0;
      z-index: 10;
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding: 11px clamp(16px, 5vw, 70px);
      background: rgba(245, 245, 247, .82);
      border-bottom: 1px solid rgba(0, 0, 0, .08);
      backdrop-filter: saturate(180%) blur(20px);
    }}
    .nav a {{
      flex: 0 0 auto;
      padding: 7px 12px;
      color: var(--ink);
      text-decoration: none;
      border: 1px solid rgba(0, 0, 0, .08);
      background: rgba(255, 255, 255, .74);
      border-radius: 999px;
      font-size: 13px;
      font-weight: 500;
    }}
    main {{ width: min(1180px, calc(100% - 32px)); margin: 26px auto 72px; }}
    section {{
      margin: 18px 0;
      padding: clamp(24px, 4vw, 44px);
      background: rgba(255, 255, 255, .9);
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      box-shadow: 0 1px 0 rgba(255, 255, 255, .7) inset;
    }}
    .summary-strip {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 30px; max-width: 1040px; }}
    .metric {{ padding: 16px; background: rgba(255, 255, 255, .86); border: 1px solid rgba(0, 0, 0, .08); border-radius: 8px; min-width: 0; box-shadow: 0 10px 30px rgba(0, 0, 0, .05); }}
    .metric span {{ display: block; color: var(--muted); font-size: 12px; font-weight: 600; letter-spacing: .04em; }}
    .metric strong {{ display: block; margin-top: 8px; font-size: clamp(20px, 2.2vw, 30px); font-weight: 700; line-height: 1.1; overflow-wrap: anywhere; }}
    .lead-grid {{ display: grid; grid-template-columns: .95fr 1.05fr; gap: 16px; align-items: start; }}
    .question-list {{ margin: 0; padding-left: 20px; }}
    .question-list li {{ margin: 7px 0; }}
    .question-card {{
      position: relative;
      padding: clamp(22px, 3vw, 32px);
      background: var(--panel);
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 8px;
      margin: 16px 0;
      box-shadow: var(--shadow);
    }}
    .question-card h3 {{ padding-right: 52px; }}
    .question-card::before {{
      content: "";
      position: absolute;
      top: 26px;
      right: 26px;
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: var(--blue);
      box-shadow: 0 0 0 7px rgba(0, 102, 204, .1);
    }}
    .answer-box {{ padding: 16px; background: #f5f8ff; border: 1px solid #d6e6ff; border-radius: 8px; margin: 14px 0 16px; }}
    .answer-box strong {{ display: block; margin-bottom: 6px; color: var(--blue); font-size: 13px; font-weight: 700; letter-spacing: .04em; }}
    .answer-box p {{ margin-bottom: 0; font-size: 16px; }}
    .info-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .info-box {{ padding: 14px; border: 1px solid rgba(0, 0, 0, .08); border-radius: 8px; background: var(--panel-soft); min-width: 0; }}
    .info-box h4 {{ margin: 0 0 10px; font-size: 13px; font-weight: 700; color: var(--muted); letter-spacing: .04em; }}
    .info-box ul {{ display: grid; gap: 12px; margin: 0; padding: 0; list-style: none; }}
    .info-box li {{ margin: 0; padding-top: 12px; border-top: 1px solid rgba(0, 0, 0, .07); }}
    .info-box li:first-child {{ padding-top: 0; border-top: 0; }}
    .info-box.evidence {{ background: #f5f9ff; }}
    .info-box.research_report {{ background: #f4fbf7; }}
    .info-box.message {{ background: #fff9ef; }}
    .info-box.opinion {{ background: #f6f6f7; }}
    .field {{ margin-top: 14px; }}
    .field b {{ display: block; margin-bottom: 6px; color: var(--muted); font-size: 12px; font-weight: 700; letter-spacing: .04em; }}
    .note {{ color: var(--muted); font-size: 13px; }}
    .chip {{
      display: inline-flex;
      max-width: 100%;
      margin: 0 4px 7px 0;
      padding: 3px 7px;
      border: 1px solid rgba(0, 0, 0, .08);
      border-radius: 999px;
      background: rgba(255, 255, 255, .76);
      color: #424245;
      font-family: "SF Mono", ui-monospace, SFMono-Regular, Consolas, monospace;
      font-size: 11px;
      overflow-wrap: anywhere;
    }}
    .status-evidenced {{ color: var(--green); font-weight: 800; }}
    .status-partial {{ color: var(--amber); font-weight: 800; }}
    .status-missing {{ color: var(--red); font-weight: 800; }}
    table {{ width: 100%; border-collapse: separate; border-spacing: 0; background: #fff; font-size: 14px; border: 1px solid rgba(0, 0, 0, .08); border-radius: 8px; overflow: hidden; }}
    th, td {{ padding: 13px; border-bottom: 1px solid rgba(0, 0, 0, .08); vertical-align: top; text-align: left; }}
    tr:last-child td {{ border-bottom: 0; }}
    th {{ color: var(--muted); font-size: 12px; font-weight: 700; letter-spacing: .04em; background: #f5f5f7; }}
    .thesis-card {{ padding: 18px; background: #111820; color: #fff; border-left: 7px solid var(--green); }}
    .thesis-card p {{ color: #d8e1dd; }}
    .reference-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .reference-card {{ padding: 15px; background: #fff; border: 1px solid var(--line); border-top: 4px solid var(--blue); }}
    .reference-card p {{ color: var(--muted); }}
    .stage {{ color: var(--green); font-weight: 800; white-space: nowrap; }}
    ul {{ margin: 8px 0 0; padding-left: 20px; }}
    li {{ margin: 5px 0; }}
    .rule-box {{ padding: 18px; background: #f5f8ff; border: 1px solid #d6e6ff; border-radius: 8px; }}
    @media (max-width: 880px) {{
      .summary-strip, .lead-grid, .info-grid, .reference-grid {{ grid-template-columns: 1fr; }}
      table {{ font-size: 13px; }}
      header {{ padding-top: 42px; }}
      .question-card h3 {{ padding-right: 34px; }}
      .question-card::before {{ right: 20px; }}
    }}
  </style>
</head>
<body>
  <header>
    <p class="eyebrow">八步框架 / 第一步</p>
    <h1>{escape(ticker)} 源头溯源</h1>
    <p class="subtitle">这一页只解决“公司从哪里来、为什么能起来、哪些基因还能解释今天”这组问题。它不是公司历史流水账，也不是创始人故事；它是后续生意、战略、竞争和消息流分析的边界条件。</p>
    <div class="summary-strip">
      <div class="metric"><span>本节状态</span><strong class="status-{escape(section['status'])}">{escape(status_label)}</strong></div>
      <div class="metric"><span>证据数量</span><strong>{evidence_count}</strong></div>
      <div class="metric"><span>输出要求</span><strong>事实 / 推论 / 判断 / 缺口</strong></div>
      <div class="metric"><span>生成时间</span><strong>{generated_at[:10] or "未记录"}</strong></div>
    </div>
  </header>
  <nav class="nav">
    <a href="../research_dashboard.html#foundation">返回总览</a>
    <a href="#question-map">8 个问题</a>
    <a href="#judgment">当前判断</a>
    <a href="#records">信息索引</a>
  </nav>
  <main>
    <section id="question-map">
      <h2>{escape(company_name)}源头溯源：8 个核心问题</h2>
      <p class="note">阅读顺序固定为：先看问题，再看当前回答，最后看四类信息如何支撑或反证。这里的“证据”指官方文件、财报、招股书、监管公告等一手材料。</p>
      {question_cards_html}
    </section>

    <section id="judgment">
      <h2>当前判断</h2>
      <div class="lead-grid">
        <div>
          <div class="field"><b>事实</b>{facts}</div>
          <div class="field"><b>推论</b>{inferences}</div>
        </div>
        <div>
          <div class="field"><b>判断</b>{judgments}</div>
          <div class="field"><b>缺口</b>{gaps}</div>
        </div>
      </div>
    </section>

    <section id="gaps">
      <h2>下一步下钻</h2>
      <div class="rule-box">
        <p><strong>研究规则：</strong>源头溯源页不直接输出投资结论。它只定义基础画像的第一层边界：哪些事实已被证据支持，哪些推论仍需验证，哪些早期基因可以迁移，哪些不能迁移。后续消息流必须挂到具体问题、假设和业务节点上。</p>
        <p class="note">如果只有创立日期、公司口号或创始人履历，本节仍应维持“部分证据”或“缺证据”状态。</p>
      </div>
    </section>

    <section id="records">
      <h2>信息索引</h2>
      <table>
        <thead><tr><th>信息 ID</th><th>类别</th><th>来源</th><th>日期</th><th>可靠性 / 重要性</th><th>摘要</th></tr></thead>
        <tbody>{evidence_rows}</tbody>
      </table>
    </section>
  </main>
</body>
</html>
"""


def _render_source_origin_question_cards(ticker: str, evidence: list[EvidenceRecord]) -> str:
    questions = _source_origin_questions(ticker)
    return "\n".join(_render_source_origin_question_card(question, evidence) for question in questions)


def _source_origin_questions(ticker: str) -> list[dict[str, Any]]:
    if ticker == "XIAOMI":
        return [
            {
                "id": "q1-era",
                "question": "时代背景是什么？",
                "answer": "小米出现于智能手机和移动互联网快速普及窗口，早期机会不是单纯卖硬件，而是在用户体验、系统迭代、线上渠道和硬件效率之间寻找结构性差异。",
                "gap": "还需要补充 2010-2012 年中国智能手机渗透率、安卓生态成熟度、运营商渠道和线上零售变化的数据。",
                "info": {
                    "evidence": [
                        _source_origin_info("ev_xiaomi_company_profile_20260518", "支撑", "确认 2010 年成立、智能手机和 IoT 平台定位。"),
                        _source_origin_info("ev_xiaomi_global_ir_triathlon_20180503", "支撑", "招股概要直接把公司定义为互联网公司，并披露 MIUI、米粉和 IoT 平台早期数据。"),
                        _source_origin_info("ev_xiaomi_profile", "支撑", "测试样本：确认成立时间和公司定位。"),
                        _source_origin_info("ev_xiaomi_ipo_prospectus_20180625", "支撑", "招股书给出早期使命、自我定义和原始业务模型。"),
                    ],
                    "research_report": [
                        _source_origin_info("ev_xiaomi_wipo_origin_miui_20211101", "支撑", "WIPO 资料确认 2010 年 8 月 MIUI 私测这一软件入口。"),
                        _source_origin_info("ev_xiaomi_jingzhun_deep_report_20181105", "支撑", "第三方报告把 MIUI、手机硬件、IoT 与互联网变现放在同一模型里分析。"),
                        _source_origin_info("ev_xiaomi_guosheng_deep_report_20211117", "支撑", "第三方报告按阶段写出 2010-2021 年业务演进。"),
                    ],
                    "message": [
                        _source_origin_info("ev_xiaomi_mi1_launch_transcript_20110816", "支撑", "早期发布会实录可作为原始产品切口的一手近似材料。"),
                    ],
                    "opinion": [],
                },
            },
            {
                "id": "q2-original-problem",
                "question": "原始问题是什么？",
                "answer": "原始问题可以概括为：用户需要更好用、更快迭代、价格可承受的智能手机体验；小米用软件体验和用户参与先建立信任，再用硬件放大用户入口。",
                "gap": "需要补早期用户反馈、MIUI 活跃社区数据、首批用户画像和竞品体验差距，避免把后来的成功倒推成起点。",
                "info": {
                    "evidence": [
                        _source_origin_info("ev_xiaomi_ipo_prospectus_20180625", "支撑", "招股书描述使命、互联网公司自我定义与智能手机/智能硬件模型。"),
                        _source_origin_info("ev_xiaomi_global_ir_triathlon_20180503", "支撑", "招股概要把用户、硬件、新零售和互联网服务放进同一个商业模型。"),
                    ],
                    "research_report": [
                        _source_origin_info("ev_xiaomi_wipo_origin_miui_20211101", "支撑", "WIPO 资料确认 MIUI 是手机硬件前的早期软件入口。"),
                        _source_origin_info("ev_xiaomi_jingzhun_deep_report_20181105", "支撑", "研报把用户参与和硬件放量作为商业模型的源头机制。"),
                    ],
                    "message": [
                        _source_origin_info("ev_xiaomi_mi1_launch_transcript_20110816", "支撑", "发布会实录显示 MIUI、发烧友、1999 元手机和线上销售是早期表达。"),
                    ],
                    "opinion": [],
                },
            },
            {
                "id": "q3-incumbent-gap",
                "question": "旧方案为什么不够好？",
                "answer": "旧方案的弱点不是单一价格高，而是软硬件体验、迭代速度、渠道效率和用户参与不足。小米早期切入点是把这些差异合成一个高性价比和高反馈速度的产品体系。",
                "gap": "需要竞品同期价格、配置、渠道加价、系统更新频率和用户满意度对比，才能把“旧方案不足”从叙事变成证据。",
                "info": {
                    "evidence": [
                        _source_origin_info("ev_xiaomi_ipo_prospectus_20180625", "支撑", "招股书可验证小米对自身互联网效率和硬件平台的定义。"),
                        _source_origin_info("ev_xiaomi_hardware_margin_pledge_2021_ar", "支撑/边界", "硬件净利率承诺说明“诚实定价”既是获客机制，也是硬件利润率约束。"),
                    ],
                    "research_report": [
                        _source_origin_info("ev_xiaomi_jingzhun_deep_report_20181105", "支撑", "研报提供商业模式和效率差的第三方归纳。"),
                        _source_origin_info("ev_xiaomi_shenwan_deep_report_20241118", "研究线索", "低可靠报告摘要可作为阶段写法参考，不能单独强化判断。"),
                    ],
                    "message": [
                        _source_origin_info("ev_xiaomi_mi1_launch_transcript_20110816", "支撑", "早期公开表达可验证当时强调的产品、价格和渠道差异。"),
                    ],
                    "opinion": [],
                },
            },
            {
                "id": "q4-product-wedge",
                "question": "第一产品楔子是什么？",
                "answer": "第一产品楔子不是孤立的手机硬件，而是 MIUI 社区迭代形成的用户信任，加上 1999 元小米手机把这种信任放大为可规模化入口。",
                "gap": "需要补 MIUI 版本节奏、论坛用户增长、首批销量、供货节奏和退换货/口碑数据。",
                "info": {
                    "evidence": [
                        _source_origin_info("ev_xiaomi_ipo_prospectus_20180625", "支撑", "招股书确认早期模型以智能手机和智能硬件为核心。"),
                        _source_origin_info("ev_xiaomi_global_ir_triathlon_20180503", "支撑", "招股概要披露 MIUI 月活、论坛月活和多设备用户，能验证用户楔子。"),
                        _source_origin_info("ev_xiaomi_management_20260518", "支撑", "管理层页面确认创始团队和产品/技术相关组织角色。"),
                    ],
                    "research_report": [
                        _source_origin_info("ev_xiaomi_wipo_origin_miui_20211101", "支撑", "WIPO 资料确认 MIUI 私测时间点早于手机硬件放量。"),
                        _source_origin_info("ev_xiaomi_jingzhun_deep_report_20181105", "支撑", "研报把 MIUI 用户参与和手机放量作为同一源头模型。"),
                    ],
                    "message": [
                        _source_origin_info("ev_xiaomi_mi1_launch_transcript_20110816", "支撑", "发布会实录直接对应 MIUI、发烧友和 1999 元手机。"),
                    ],
                    "opinion": [],
                },
            },
            {
                "id": "q5-first-customers",
                "question": "第一批客户是谁？",
                "answer": "当前判断是：早期核心客户更接近对体验敏感、愿意参与反馈、同时重视价格性能比的手机发烧友和线上用户，而不是泛化大众客群。",
                "gap": "需要补首批预约用户、论坛用户画像、地域和渠道结构、复购与口碑传播证据。",
                "info": {
                    "evidence": [
                        _source_origin_info("ev_xiaomi_ipo_prospectus_20180625", "支撑", "招股书可验证原始用户入口和平台模型。"),
                        _source_origin_info("ev_xiaomi_global_ir_triathlon_20180503", "支撑", "招股概要披露米粉、MIUI 论坛和多设备用户，能具体化早期用户。"),
                    ],
                    "research_report": [
                        _source_origin_info("ev_xiaomi_jingzhun_deep_report_20181105", "支撑", "研报将发烧友用户参与纳入商业模型源头。"),
                    ],
                    "message": [
                        _source_origin_info("ev_xiaomi_mi1_launch_transcript_20110816", "支撑", "早期发布会材料直接指向发烧友和线上用户切口。"),
                    ],
                    "opinion": [],
                },
            },
            {
                "id": "q6-early-advantage",
                "question": "早期优势来自哪里？",
                "answer": "早期优势来自产品定义、快速迭代、用户组织、供应链整合和线上渠道效率的组合，而不是单一低价。这个判断会影响后续分析：优势能否跨品类迁移，必须拆成能力项验证。",
                "gap": "需要补早期组织分工、供应链账期、渠道费用率、硬件毛利和研发投入资料。",
                "info": {
                    "evidence": [
                        _source_origin_info("ev_xiaomi_global_ir_triathlon_20180503", "支撑", "招股概要将早期优势拆成创新、效率、新零售、IoT 和互联网服务。"),
                        _source_origin_info("ev_xiaomi_hardware_margin_pledge_2021_ar", "支撑/边界", "硬件净利率承诺验证低硬件利润与用户信任之间的制度化绑定。"),
                        _source_origin_info("ev_xiaomi_management_20260518", "支撑", "管理层资料帮助验证创始团队和职能能力结构。"),
                        _source_origin_info("ev_xiaomi_ipo_prospectus_20180625", "支撑", "招股书是检验原始模型和业务结构的核心证据。"),
                    ],
                    "research_report": [
                        _source_origin_info("ev_xiaomi_guosheng_deep_report_20211117", "支撑", "研报提供阶段化能力演进视角。"),
                        _source_origin_info("ev_xiaomi_yongxing_deep_report_20250228", "支撑", "研报把早期手机/AIoT 基因连接到当前人车家生态。"),
                    ],
                    "message": [
                        _source_origin_info("ev_xiaomi_mi1_launch_transcript_20110816", "支撑", "早期公开材料可验证当时强调的产品和渠道打法。"),
                    ],
                    "opinion": [],
                },
            },
            {
                "id": "q7-flywheel",
                "question": "早期飞轮如何形成？",
                "answer": "可工作的飞轮应是：手机入口积累用户规模，IoT 和智能硬件增加触点，互联网服务承担较高毛利变现层，再反哺生态扩张。每一环都要用分部收入、毛利、用户规模和现金流验证。",
                "gap": "需要补早期到当前的用户规模、IoT 连接设备、多设备用户、互联网服务毛利和硬件利润率序列。",
                "info": {
                    "evidence": [
                        _source_origin_info("ev_xiaomi_ipo_prospectus_20180625", "支撑", "招股书描述手机、智能硬件和 IoT 平台连接的原始模型。"),
                        _source_origin_info("ev_xiaomi_global_ir_triathlon_20180503", "支撑", "招股概要明确三支柱模型：硬件、新零售、互联网服务。"),
                        _source_origin_info("ev_xiaomi_hardware_margin_pledge_2021_ar", "支撑/边界", "硬件净利率上限解释硬件负责获客、服务负责利润质量的模型边界。"),
                        _source_origin_info("ev_xiaomi_2025_results_announcement_20260324", "支撑", "FY2025 业绩公告提供手机、IoT、MAU 和 EV 的现阶段规模数据。"),
                        _source_origin_info("ev_xiaomi_segments", "支撑", "测试样本：提供手机、IoT、服务和 EV 规模数据。"),
                    ],
                    "research_report": [
                        _source_origin_info("ev_xiaomi_jingzhun_deep_report_20181105", "支撑", "研报把硬件放量、IoT 生态和互联网变现放在一个商业模型里。"),
                        _source_origin_info("ev_xiaomi_yongxing_deep_report_20250228", "支撑", "研报将源头模型延展到人车家生态。"),
                    ],
                    "message": [],
                    "opinion": [],
                },
            },
            {
                "id": "q8-dna-today",
                "question": "源头基因今天是否仍有效？",
                "answer": "源头基因仍能解释小米在用户体验、生态连接和多品类扩张上的优势，但不能直接证明 EV 利润可持续。汽车业务引入制造质量、安全冗余、质保、召回和售后责任，必须单独验证。",
                "gap": "需要补 EV 单车收入、单车毛利、订单等待周期、产能利用率、质保计提、召回成本和用户满意度。",
                "info": {
                    "evidence": [
                        _source_origin_info("ev_xiaomi_global_ir_triathlon_20180503", "支撑", "招股概要中的三支柱模型仍能解释今天的人车家生态入口。"),
                        _source_origin_info("ev_xiaomi_2025_results_announcement_20260324", "支撑", "业绩公告显示 EV 已进入财务级业务结构。"),
                        _source_origin_info("ev_xiaomi_segments", "支撑", "测试样本：提供 EV 和手机/IoT 规模数据。"),
                        _source_origin_info("ev_xiaomi_hardware_margin_pledge_2021_ar", "反证/边界", "硬件净利率承诺提示硬件规模并不等于高利润池。"),
                        _source_origin_info("ev_xiaomi_samr_su7_recall_20250919", "反证/边界", "召回公告提醒汽车安全和监管责任不能由互联网效率直接外推。"),
                        _source_origin_info("ev_xiaomi_recall", "反证/边界", "测试样本：召回信息验证 EV 风险边界。"),
                    ],
                    "research_report": [
                        _source_origin_info("ev_xiaomi_yongxing_deep_report_20250228", "支撑", "研报把手机/AIoT 基因与汽车、IoT、互联网服务当前结构相连接。"),
                        _source_origin_info("ev_xiaomi_shenwan_deep_report_20241118", "研究线索", "低可靠报告摘要只能用于提示进一步验证方向。"),
                    ],
                    "message": [],
                    "opinion": [],
                },
            },
        ]
    return [
        {
            "id": "q1-era",
            "question": "时代背景是什么？",
            "answer": "当前证据不足。需要先确认公司创立时的技术、需求、供给、渠道和资本市场环境。",
            "gap": "补充创立年份前后的行业数据、招股书、创始人公开材料和早期产品发布材料。",
            "info": {"evidence": [], "research_report": [], "message": [], "opinion": []},
        },
        {
            "id": "q2-original-problem",
            "question": "原始问题是什么？",
            "answer": "当前证据不足。需要定义公司最早解决了哪个客户问题，而不是只写公司成立经过。",
            "gap": "补充第一产品、第一客户、早期替代方案和用户痛点证据。",
            "info": {"evidence": [], "research_report": [], "message": [], "opinion": []},
        },
        {
            "id": "q3-incumbent-gap",
            "question": "旧方案为什么不够好？",
            "answer": "当前证据不足。需要说明公司替代了什么旧方案，以及旧方案的成本、体验、效率或供给缺陷。",
            "gap": "补充竞品同期产品、价格、渠道、性能、客户满意度或监管变化资料。",
            "info": {"evidence": [], "research_report": [], "message": [], "opinion": []},
        },
        {
            "id": "q4-product-wedge",
            "question": "第一产品楔子是什么？",
            "answer": "当前证据不足。需要确认公司最早靠什么产品、渠道或场景进入客户心智。",
            "gap": "补充首款产品资料、发布材料、销售/用户增长和渠道切口。",
            "info": {"evidence": [], "research_report": [], "message": [], "opinion": []},
        },
        {
            "id": "q5-first-customers",
            "question": "第一批客户是谁？",
            "answer": "当前证据不足。需要把早期客户具体到人群、场景、渠道和购买理由。",
            "gap": "补充客户画像、早期订单、用户社区、渠道分布和复购数据。",
            "info": {"evidence": [], "research_report": [], "message": [], "opinion": []},
        },
        {
            "id": "q6-early-advantage",
            "question": "早期优势来自哪里？",
            "answer": "当前证据不足。需要拆分技术、产品、渠道、成本、组织和资本等能力来源。",
            "gap": "补充早期团队、技术路线、供应链、渠道、单位经济和竞争对比。",
            "info": {"evidence": [], "research_report": [], "message": [], "opinion": []},
        },
        {
            "id": "q7-flywheel",
            "question": "早期飞轮如何形成？",
            "answer": "当前证据不足。需要说明获客、留存、复购、利润和再投资之间是否形成闭环。",
            "gap": "补充用户增长、留存、毛利、现金流和再投资数据。",
            "info": {"evidence": [], "research_report": [], "message": [], "opinion": []},
        },
        {
            "id": "q8-dna-today",
            "question": "源头基因今天是否仍有效？",
            "answer": "当前证据不足。需要验证早期能力哪些能迁移到今天，哪些已经成为路径依赖或风险边界。",
            "gap": "补充当前业务分部、竞争格局、管理层策略和风险事件证据。",
            "info": {"evidence": [], "research_report": [], "message": [], "opinion": []},
        },
    ]


def _source_origin_info(evidence_id: str, relation: str, point: str) -> dict[str, str]:
    return {"evidence_id": evidence_id, "relation": relation, "point": point}


def _render_source_origin_question_card(question: dict[str, Any], evidence: list[EvidenceRecord]) -> str:
    bucket_html = "\n".join(
        _render_foundation_info_bucket(category, question.get("info", {}).get(category, []), evidence)
        for category in SOURCE_ORIGIN_INFO_ORDER
    )
    return (
        f"<article class=\"question-card\" id=\"{escape(question['id'])}\">"
        f"<h3>{escape(question['question'])}</h3>"
        f"<div class=\"answer-box\"><strong>当前回答</strong><p>{escape(question['answer'])}</p></div>"
        f"<div class=\"info-grid\">{bucket_html}</div>"
        f"<p class=\"note\"><strong>待验证：</strong>{escape(question['gap'])}</p>"
        "</article>"
    )


def _render_foundation_info_bucket(
    category: str,
    items: list[dict[str, str]],
    evidence: list[EvidenceRecord],
) -> str:
    label = INFO_CATEGORY_LABEL_ZH.get(category, category)
    by_id = {record.id: record for record in evidence}
    rows: list[str] = []
    for item in items:
        record = by_id.get(item["evidence_id"])
        if record is None:
            continue
        source_name = SOURCE_NAME_ZH.get(record.source_name, record.source_name)
        summary = _zh_text(record.summary)
        if len(summary) > 115:
            summary = summary[:112] + "..."
        rows.append(
            "<li>"
            f"<span class=\"chip\">{escape(record.id)}</span>"
            f"<div><strong>{escape(item['relation'])}：</strong>{escape(item['point'])}</div>"
            f"<div><a href=\"{escape(record.url)}\">{escape(source_name)}</a></div>"
            f"<div class=\"note\">{escape(summary)}</div>"
            "</li>"
        )
    if not rows:
        rows.append("<li class=\"note\">暂无映射信息；不能用这一类材料强化当前回答。</li>")
    return f"<div class=\"info-box {escape(category)}\"><h4>{escape(label)}</h4><ul>{''.join(rows)}</ul></div>"


def _render_professional_report_cards(records: list[EvidenceRecord]) -> str:
    if not records:
        return (
            '<article class="reference-card">'
            "<h3>本地证据库尚未纳入外部专业报告</h3>"
            "<p>生成器会先保留方法论层级；补充券商深度报告或招股书后，再把阶段复盘和商业模型拆解写实。</p>"
            "</article>"
        )
    cards: list[str] = []
    for record in records[:4]:
        source_name = SOURCE_NAME_ZH.get(record.source_name, record.source_name)
        cards.append(
            '<article class="reference-card">'
            f"<h3>{escape(source_name)}</h3>"
            f"<p>{escape(_zh_text(record.summary))}</p>"
            f"<p><span class=\"chip\">{escape(record.id)}</span> <a href=\"{escape(record.url)}\">打开来源</a></p>"
            "</article>"
        )
    return "\n".join(cards)


def _render_source_origin_thesis(ticker: str, evidence: list[EvidenceRecord]) -> str:
    if ticker == "XIAOMI":
        chips = _chips(
            [
                "ev_xiaomi_ipo_prospectus_20180625",
                "ev_xiaomi_mi1_launch_transcript_20110816",
                "ev_xiaomi_jingzhun_deep_report_20181105",
                "ev_xiaomi_2025_results_announcement_20260324",
                "ev_xiaomi_samr_su7_recall_20250919",
            ],
            evidence,
        )
        return (
            '<div class="thesis-card">'
            "<h3>源头不是“硬件公司成立”，而是“用户参与的软件入口 + 高效率硬件放大 + 生态服务变现”的组合。</h3>"
            "<p>小米最早的有效切口是 MIUI 和发烧友用户参与，随后用高性价比手机把用户规模做大，再把手机作为智能硬件、IoT 和互联网服务的入口。这个源头解释了小米长期的优势：产品定义快、渠道效率高、用户反馈强、生态扩展能力强；也解释了它的边界：硬件利润率天然受价格承诺约束，业务越往汽车和智能制造延伸，质量、安全、售后和资本开支就越不能再按轻互联网模型外推。</p>"
            f"<p>{chips}</p>"
            "</div>"
        )
    chips = _chips([record.id for record in evidence[:4]], evidence)
    return (
        '<div class="thesis-card">'
        "<h3>本页先形成源头假设，再由证据和消息流持续修正。</h3>"
        "<p>当前公司还没有专门写实的源头结论；需要补充创立背景、第一产品、第一批用户、渠道切口和早期商业模型证据。</p>"
        f"<p>{chips}</p>"
        "</div>"
    )


def _render_source_origin_phase_rows(ticker: str, evidence: list[EvidenceRecord]) -> str:
    if ticker != "XIAOMI":
        return _generic_phase_rows(evidence)
    rows = [
        (
            "2010-2011",
            "从 MIUI 和发烧友用户切入，再发布小米手机。",
            "第一步不是泛硬件铺货，而是先用软件迭代和用户参与找到高信任用户，再用手机硬件放大入口。",
            ["ev_xiaomi_mi1_launch_transcript_20110816", "ev_xiaomi_ipo_prospectus_20180625"],
        ),
        (
            "2012-2018",
            "手机规模化后，扩展到智能硬件、IoT 生态和互联网服务，并在 2018 年港股上市。",
            "源头飞轮开始成形：手机获客，硬件扩品类，IoT 增加触点，互联网服务尝试把用户规模变成利润池。",
            ["ev_xiaomi_jingzhun_deep_report_20181105", "ev_xiaomi_ipo_prospectus_20180625"],
        ),
        (
            "2019-2023",
            "手机 x AIoT 和高端化成为核心命题，渠道、供应链、品牌和组织能力被持续补课。",
            "这阶段决定早期“性价比效率”能否升级为中高端品牌力和全球化经营能力。",
            ["ev_xiaomi_guosheng_deep_report_20211117", "ev_xiaomi_yongxing_deep_report_20250228"],
        ),
        (
            "2024-2026",
            "人车家生态和智能 EV 成为财务级增长曲线，同时引入制造、安全、质保和售后责任。",
            "早期互联网/手机能力能迁移到 EV 的用户体验和生态入口，但不能自动迁移到汽车安全、产能、召回和生命周期成本。",
            ["ev_xiaomi_2025_results_announcement_20260324", "ev_xiaomi_samr_su7_recall_20250919", "ev_xiaomi_yongxing_deep_report_20250228"],
        ),
    ]
    return "\n".join(_render_phase_row(row, evidence) for row in rows)


def _render_source_origin_mechanism_rows(ticker: str, evidence: list[EvidenceRecord]) -> str:
    if ticker != "XIAOMI":
        return _generic_mechanism_rows(evidence)
    rows = [
        (
            "原始痛点是什么？",
            "智能手机普及早期，用户需要更好用、更快迭代且价格可承受的软硬件体验。",
            "这决定小米不是从单一硬件利润池出发，而是从用户入口和效率差出发。",
            ["ev_xiaomi_mi1_launch_transcript_20110816", "ev_xiaomi_jingzhun_deep_report_20181105"],
        ),
        (
            "第一产品楔子是什么？",
            "先用 MIUI 和发烧友共创建立产品反馈闭环，再用小米手机放大用户规模。",
            "源头能力是产品迭代和用户组织，不只是低价硬件。",
            ["ev_xiaomi_mi1_launch_transcript_20110816", "ev_xiaomi_management_20260518"],
        ),
        (
            "原始飞轮如何运转？",
            "手机入口带来用户规模，智能硬件和 IoT 增加触点，互联网服务承担高毛利变现层。",
            "后续所有业务分析都要拆开验证：用户规模、硬件毛利、服务变现和生态留存是否互相加强。",
            ["ev_xiaomi_ipo_prospectus_20180625", "ev_xiaomi_2025_results_announcement_20260324"],
        ),
        (
            "哪些基因可以迁移？",
            "用户体验、产品定义、供应链组织和生态连接能力可以迁移到人车家场景。",
            "这解释 EV/AI 为什么能成为第二曲线的研究问题，但不能直接证明利润可持续。",
            ["ev_xiaomi_yongxing_deep_report_20250228", "ev_xiaomi_2025_results_announcement_20260324"],
        ),
        (
            "哪些基因不能直接迁移？",
            "汽车业务需要安全冗余、监管响应、售后体系、召回成本和产能质量管理。",
            "这是源头页必须留下的反证边界：互联网效率不能替代汽车工业责任。",
            ["ev_xiaomi_samr_su7_recall_20250919"],
        ),
    ]
    return "\n".join(_render_mechanism_row(row, evidence) for row in rows)


def _generic_phase_rows(evidence: list[EvidenceRecord]) -> str:
    return _render_phase_row(
        (
            "待补",
            "尚未把公司历史拆成可验证阶段。",
            "需要补充创立背景、第一产品、关键融资/上市和业务模型变迁证据。",
            [record.id for record in evidence[:3]],
        ),
        evidence,
    )


def _generic_mechanism_rows(evidence: list[EvidenceRecord]) -> str:
    return _render_mechanism_row(
        (
            "原始问题是什么？",
            "当前证据不足，不能可靠回答。",
            "没有原始痛点和第一产品楔子，后续竞争优势分析会变成空泛叙事。",
            [record.id for record in evidence[:3]],
        ),
        evidence,
    )


def _render_phase_row(row: tuple[str, str, str, list[str]], evidence: list[EvidenceRecord]) -> str:
    stage, event, implication, evidence_ids = row
    return (
        "<tr>"
        f"<td><span class=\"stage\">{escape(stage)}</span></td>"
        f"<td>{escape(event)}</td>"
        f"<td>{escape(implication)}</td>"
        f"<td>{_chips(evidence_ids, evidence)}</td>"
        "</tr>"
    )


def _render_mechanism_row(row: tuple[str, str, str, list[str]], evidence: list[EvidenceRecord]) -> str:
    question, answer, why, evidence_ids = row
    return (
        "<tr>"
        f"<td><strong>{escape(question)}</strong></td>"
        f"<td>{escape(answer)}</td>"
        f"<td>{escape(why)}</td>"
        f"<td>{_chips(evidence_ids, evidence)}</td>"
        "</tr>"
    )


def _chips(evidence_ids: list[str], evidence: list[EvidenceRecord]) -> str:
    available = {record.id for record in evidence}
    chips = [
        f"<span class=\"chip\">{escape(evidence_id)}</span>"
        for evidence_id in evidence_ids
        if evidence_id in available
    ]
    return " ".join(chips) or '<span class="note">需要补证据</span>'


def _foundation_section_by_id(foundation_graph: dict[str, Any], section_id: str) -> dict[str, Any]:
    for section in foundation_graph.get("sections", []):
        if section.get("id") == section_id:
            return section
    return {
        "id": section_id,
        "label": section_id,
        "status": "missing",
        "evidence_ids": [],
        "facts": [],
        "inferences": [],
        "judgments": ["Do not use this section to strengthen a thesis until primary or high-reliability evidence is added."],
        "gaps": ["Need primary sources for founding context, original customer wedge, and company DNA."],
    }


def _records_matching(evidence: list[EvidenceRecord], keywords: list[str], limit: int) -> list[EvidenceRecord]:
    matched_ids = _evidence_ids_for_keywords(evidence, keywords)
    by_id = {record.id: record for record in evidence}
    return [by_id[evidence_id] for evidence_id in matched_ids[:limit] if evidence_id in by_id]


def _render_source_origin_evidence_card(title: str, purpose: str, records: list[EvidenceRecord]) -> str:
    if records:
        chips = " ".join(f"<span class=\"chip\">{escape(record.id)}</span>" for record in records[:5])
        summaries = "<ul>" + "".join(
            f"<li>{escape(_zh_text(record.summary))}</li>" for record in records[:3]
        ) + "</ul>"
    else:
        chips = '<span class="note">当前没有映射证据</span>'
        summaries = '<p class="note">需要补充一手或高可靠来源后再判断。</p>'
    return (
        '<article class="evidence-card">'
        f"<h3>{escape(title)}</h3>"
        f"<p>{escape(purpose)}</p>"
        f"<div>{chips}</div>"
        f"{summaries}"
        "</article>"
    )


def _render_information_category_tables(section: dict[str, Any]) -> str:
    groups = section.get("information_by_category", {})
    tables: list[str] = []
    for category in INFO_CATEGORY_ORDER:
        rows = groups.get(category, [])
        label = INFO_CATEGORY_LABEL_ZH.get(category, category)
        explanation = INFO_CATEGORY_EXPLANATION_ZH.get(category, "")
        if not rows:
            body = '<tr><td colspan="5" class="note">当前没有映射信息。</td></tr>'
        else:
            body = "\n".join(_render_information_map_row(row) for row in rows)
        tables.append(
            f"<h3>{escape(label)}</h3>"
            f"<p class=\"note\">{escape(explanation)}</p>"
            "<table>"
            "<thead><tr><th>信息</th><th>关系</th><th>对应问题</th><th>支撑 / 反证的论点</th><th>说明</th></tr></thead>"
            f"<tbody>{body}</tbody>"
            "</table>"
        )
    return "\n".join(tables)


def _render_information_map_row(row: dict[str, Any]) -> str:
    source_name = SOURCE_NAME_ZH.get(row.get("source_name", ""), row.get("source_name", ""))
    stance = STANCE_LABEL_ZH.get(row.get("stance", ""), row.get("stance", ""))
    summary = _zh_text(row.get("summary", ""))
    if len(summary) > 130:
        summary = summary[:127] + "..."
    return (
        "<tr>"
        f"<td><span class=\"chip\">{escape(row.get('evidence_id', ''))}</span><br><a href=\"{escape(row.get('url', ''))}\">{escape(source_name)}</a><br><span class=\"note\">{escape(summary)}</span></td>"
        f"<td>{escape(stance)}</td>"
        f"<td>{escape(row.get('linked_question', ''))}</td>"
        f"<td>{escape(row.get('claim', ''))}</td>"
        f"<td>{escape(row.get('explanation', ''))}</td>"
        "</tr>"
    )


def _records_for_ids(evidence: list[EvidenceRecord], evidence_ids: list[str]) -> list[EvidenceRecord]:
    by_id = {record.id: record for record in evidence}
    return [by_id[evidence_id] for evidence_id in evidence_ids if evidence_id in by_id]


def _render_evidence_record_row(record: EvidenceRecord) -> str:
    source_name = SOURCE_NAME_ZH.get(record.source_name, record.source_name)
    date = record.published_at[:10] if record.published_at else f"抓取 {record.fetched_at[:10]}"
    reliability = f"{_zh_text(record.reliability)} / {_zh_text(record.materiality)}"
    category = INFO_CATEGORY_LABEL_ZH.get(record.information_category, record.information_category)
    return (
        "<tr>"
        f"<td><span class=\"chip\">{escape(record.id)}</span></td>"
        f"<td>{escape(category)}</td>"
        f"<td><a href=\"{escape(record.url)}\">{escape(source_name)}</a></td>"
        f"<td>{escape(date)}</td>"
        f"<td>{escape(reliability)}</td>"
        f"<td>{escape(_zh_text(record.summary))}</td>"
        "</tr>"
    )


def _committee_summary(
    ticker: str,
    foundation_graph: dict[str, Any],
    p0_questions: list[dict[str, Any]],
    messages: list[dict[str, Any]],
) -> dict[str, Any]:
    driver_counts: dict[str, int] = {}
    weakening = 0
    research_leads = 0
    for message in messages:
        driver = message.get("fenghe", {}).get("dominant_d", "D1")
        driver_counts[driver] = driver_counts.get(driver, 0) + 1
        if message.get("impact") == "weakening":
            weakening += 1
        if message.get("impact") == "research_lead":
            research_leads += 1

    dominant_driver = max(driver_counts, key=driver_counts.get) if driver_counts else "D1"
    max_uncertainty = (
        _display_question(p0_questions[0]["question"])
        if p0_questions
        else "No P0 question has been generated yet; add evidence and rebuild the research system."
    )

    disconfirming: list[str] = []
    for question in p0_questions:
        for signal in question.get("disconfirming_signals", []):
            translated_signal = _zh_text(signal)
            if translated_signal not in disconfirming:
                disconfirming.append(translated_signal)
            if len(disconfirming) >= 5:
                break
        if len(disconfirming) >= 5:
            break
    if not disconfirming:
        disconfirming = ["Fresh primary evidence contradicts the current company foundation baseline."]

    status = foundation_graph["foundation_status"]
    coverage = foundation_graph["coverage"]
    key_conclusion = (
        f"{ticker} 的公司基础画像尚未完成，当前不能进入强化结论阶段。"
        if status == "incomplete"
        else f"{ticker} 已有可用的基础画像，但投研工作应先围绕 P0 问题和反证测试推进，再考虑强化任何结论。"
    )
    if weakening:
        key_conclusion += f" 当前消息流中有 {weakening} 条削弱/反证信号，下一步应做针对性验证，而不是扩写叙事。"

    return {
        "key_conclusion": key_conclusion,
        "max_uncertainty": max_uncertainty,
        "dominant_driver": f"{dominant_driver}：当前消息流主要集中在这个驱动上；在新证据改变结构前，将其视为活跃主驱动。",
        "disconfirming": disconfirming,
        "cards": [
            {
                "label": "基础画像状态",
                "value": _zh_text(status),
                "detail": "Company baseline quality before message-flow analysis.",
            },
            {
                "label": "八步覆盖度",
                "value": f"{coverage['sections_evidenced']}/{coverage['sections_total']}",
                "detail": "Eight-section framework coverage with local evidence.",
            },
            {
                "label": "P0 问题",
                "value": str(len(p0_questions)),
                "detail": "Highest-priority questions that should drive the next evidence search.",
            },
            {
                "label": "消息风险",
                "value": f"{weakening} 条削弱",
                "detail": f"{research_leads} 条研究线索仍需确认。",
            },
        ],
    }


def _render_foundation_section_card(section: dict[str, Any]) -> str:
    facts = _render_statement_list(
        [
            f"{_zh_text(fact['statement'])} [{fact['evidence_id']}]"
            for fact in section.get("facts", [])[:3]
        ],
        "No local fact evidence yet.",
    )
    inferences = _render_statement_list(section.get("inferences", [])[:2], "No inference until evidence is added.")
    judgments = _render_statement_list(section.get("judgments", [])[:2], "No judgment until evidence is added.")
    gaps = _render_statement_list(section.get("gaps", [])[:2], "No material gap flagged.")
    evidence = " ".join(f"<span class=\"chip\">{escape(eid)}</span>" for eid in section["evidence_ids"][:4])
    evidence_html = evidence or f'<span class="note">{_zh_text("No evidence mapped")}</span>'
    card_class = f"foundation-card {escape(section['status'])}"
    section_label = SECTION_LABEL_ZH.get(section["label"], section["label"])
    status_label = _zh_text(section["status"])
    detail_page = section.get("detail_page", f"pages/{section.get('id', 'section')}.html")
    detail_link = f'<a class="detail-link" href="{escape(detail_page)}">打开详情页</a>'
    questions = _render_statement_list(section.get("key_questions", [])[:2], "尚未定义本板块关键问题。")
    return (
        f"<article class=\"{card_class}\">"
        f"<h3>{escape(section_label)} <span class=\"status-{escape(section['status'])}\">{escape(status_label)}</span></h3>"
        f"<p>{evidence_html}</p>"
        f"<div class=\"field\"><b>关键问题</b>{questions}</div>"
        f"<div class=\"field\"><b>事实</b>{facts}</div>"
        f"<div class=\"field\"><b>推论</b>{inferences}</div>"
        f"<div class=\"field\"><b>判断</b>{judgments}</div>"
        f"<div class=\"field\"><b>缺口</b>{gaps}</div>"
        f"{detail_link}"
        "</article>"
    )


def _render_l0_framework_card(section: dict[str, Any], qa_tree: dict[str, Any]) -> str:
    section_id = section.get("id", "")
    section_label = SECTION_LABEL_ZH.get(section.get("label", ""), section.get("label", ""))
    l1_question = L1_FRAMEWORK_QUESTIONS.get(section_id, _foundation_section_question(section))
    status_label = _zh_text(section.get("status", "missing"))
    detail_page = section.get("detail_page", f"pages/{section_id}.html")
    nodes_by_id = {node.get("id"): node for node in qa_tree.get("nodes", [])}
    l2_nodes = _l2_nodes_for_section(qa_tree, section_id)
    rollup = _children_summary(l2_nodes, nodes_by_id) or _section_evidence_summary(section)
    child_items = _render_statement_list(section.get("key_questions", []), "暂无子问题。")
    gap_items = _render_child_gap_list(l2_nodes)
    return (
        f"<article class=\"foundation-card {escape(section.get('status', 'missing'))}\">"
        f"<p class=\"eyebrow\">L1 / {escape(section_label)}</p>"
        f"<h3>{escape(l1_question)}</h3>"
        f"<div class=\"field\"><b>子结构汇总结论</b><p>{escape(_zh_text(rollup))}</p></div>"
        f"<div class=\"field\"><b>子问题列表</b>{child_items}</div>"
        f"<div class=\"field\"><b>高优先级缺口</b>{gap_items}</div>"
        f"<a class=\"detail-link\" href=\"{escape(detail_page)}\">进入 L1 子页面</a>"
        f"<p class=\"note\">状态：<span class=\"status-{escape(section.get('status', 'missing'))}\">{escape(status_label)}</span></p>"
        "</article>"
    )


def _foundation_l0_summary(ticker: str, foundation_graph: dict[str, Any]) -> str:
    if ticker == "XIAOMI":
        return (
            "小米当前基础画像的主线是：源头来自 MIUI/手机用户入口和高效率硬件放大，发展历史从手机、AIoT 延伸到智能 EV，"
            "当下核心研究矛盾集中在手机基本盘、IoT/互联网服务变现、EV 单车经济和汽车安全/售后责任。"
            "因此后续下钻优先级应放在 EV 毛利与质量成本、手机份额与 MAU、硬件低利润承诺对利润池的约束，以及创始人控制权下的资本配置纪律。"
        )
    rollups = []
    for section in foundation_graph.get("sections", []):
        rollup = _foundation_section_rollup(section)
        if rollup and rollup not in rollups:
            rollups.append(_zh_text(rollup))
    return "；".join(rollups[:4]) or "当前基础框架还没有足够证据形成上抛总结。"


def _render_statement_list(items: list[str], empty: str) -> str:
    if not items:
        return f"<p class=\"note\">{escape(_zh_text(empty))}</p>"
    return "<ul>" + "".join(f"<li>{escape(_zh_text(item))}</li>" for item in items) + "</ul>"


def _render_section_row(section: dict[str, Any]) -> str:
    evidence = " ".join(f"<span class=\"chip\">{escape(eid)}</span>" for eid in section["evidence_ids"][:4])
    evidence_html = evidence or '<span class="note">none</span>'
    gap_or_judgment = "; ".join(section["gaps"] or section["judgments"])
    status_class = f"status-{section['status']}"
    return (
        "<tr>"
        f"<td>{escape(SECTION_LABEL_ZH.get(section['label'], section['label']))}</td>"
        f"<td class=\"{status_class}\">{escape(_zh_text(section['status']))}</td>"
        f"<td>{evidence_html}</td>"
        f"<td>{escape(_zh_text(gap_or_judgment))}</td>"
        "</tr>"
    )


def _render_question_card(question: dict[str, Any]) -> str:
    evidence = " ".join(f"<span class=\"chip\">{escape(eid)}</span>" for eid in question["evidence_ids"][:4])
    evidence_html = evidence or '<span class="note">needs data</span>'
    current_judgment = _current_judgment_for_question(question)
    question_text = _display_question(question["question"])
    disconfirming = _render_statement_list(question["disconfirming_signals"][:4], "No disconfirming condition mapped.")
    required = _render_statement_list(question["required_evidence"][:4], "No required evidence mapped.")
    triggers = _render_statement_list(_update_triggers_for_question(question), "No update trigger mapped.")
    return (
        "<div class=\"card question\">"
        f"<h3>问题：{escape(question_text)}</h3>"
        f"<p class=\"note\">{escape(question['priority'])} · {escape(question['time_frame'])} · {escape(_zh_text(question['why_it_matters']))}</p>"
        f"<div class=\"field\"><b>当前判断</b><p>{escape(current_judgment)}</p></div>"
        f"<div class=\"field\"><b>支持证据</b><p>{evidence_html}</p></div>"
        f"<div class=\"field\"><b>反证证据 / 条件</b>{disconfirming}</div>"
        f"<div class=\"field\"><b>下一步数据</b>{required}</div>"
        f"<div class=\"field\"><b>更新触发器</b>{triggers}</div>"
        "</div>"
    )


def _current_judgment_for_question(question: dict[str, Any]) -> str:
    if question["status"] == "needs_data":
        return "需要先补证据；当前不能用于强化结论。"
    if question["evidence_ids"]:
        return "需要验证；已有证据足以提出问题，但不足以关闭问题。"
    return "需要验证；当前问题尚未绑定有效证据。"


def _update_triggers_for_question(question: dict[str, Any]) -> list[str]:
    joined = " ".join(question.get("linked_business_node_ids", []) + question.get("linked_foundation_sections", []))
    if "smart_ev" in joined:
        return ["Q1/Q2 业绩", "月度交付和订单等待周期", "监管公告和召回进展", "价格调整和促销强度"]
    if "smartphone" in joined:
        return ["季度出货和份额数据", "ASP 和毛利率", "渠道库存", "内存和关键部件价格"]
    if "services" in joined:
        return ["MAU / ARPU 更新", "广告和游戏收入结构", "监管或平台政策变化"]
    if "iot" in joined:
        return ["连接设备数", "多设备用户数", "品类毛利率", "复购和促销数据"]
    if "governance" in joined:
        return ["年报治理披露", "董事会和投票权变化", "重大资本配置公告"]
    return ["公司正式业绩", "管理层指引", "高可靠行业数据", "监管公告"]


def _display_question(question: str) -> str:
    return QUESTION_TRANSLATIONS.get(question, question)


def _zh_text(text: str) -> str:
    if text in DISPLAY_TRANSLATIONS:
        return DISPLAY_TRANSLATIONS[text]

    bracket = ""
    body = text
    match = re.search(r"\s(\[[^\]]+\])$", text)
    if match:
        bracket = match.group(1)
        body = text[: match.start()]

    exact = {
        "Xiaomi was founded in April 2010, listed on HKEX on July 9, 2018, and describes itself as a consumer electronics and smart manufacturing company centered on smartphones and smart hardware connected by an IoT platform.": "小米成立于 2010 年 4 月，2018 年 7 月 9 日在港交所上市，并将自身定位为以智能手机和智能硬件为核心、由 IoT 平台连接的消费电子与智能制造公司。",
        "FY2025 revenue was RMB457.3B, gross profit RMB101.8B, profit for the year RMB41.6B, adjusted net profit RMB39.2B, total assets RMB508.1B, total equity RMB266.3B, operating cash flow RMB34.1B, and cash resources RMB232.6B.": "FY2025 收入为人民币 4573 亿元，毛利为 1018 亿元，年度利润为 416 亿元，经调整净利润为 392 亿元，总资产为 5081 亿元，总权益为 2663 亿元，经营现金流为 341 亿元，现金资源为 2326 亿元。",
        "The FY2025 announcement provides segment data: Smartphone x AIoT revenue RMB351.2B, Smart EV/AI/new initiatives revenue RMB106.1B, smartphone shipments 165.2M, global MAU 754.1M, connected IoT devices 1,079.2M, and EV deliveries 411,082.": "FY2025 业绩公告披露分部数据：手机 x AIoT 收入 3512 亿元，智能 EV/AI/新业务收入 1061 亿元，智能手机出货 1.652 亿台，全球 MAU 7.541 亿，已连接 IoT 设备 10.792 亿台，EV 交付 411,082 辆。",
        "Management page identifies Lei Jun as founder, chairman and CEO; Lin Bin as co-founder and vice chairman; Lu Weibing as partner and president; and lists senior executives across smartphone, international, China region, finance, R&D and technology committee roles.": "管理层页面显示，雷军为创始人、董事长兼 CEO；林斌为联合创始人、副董事长；卢伟冰为合伙人兼总裁；高管团队覆盖手机、国际业务、中国区、财务、研发和技术委员会等职能。",
        "The annual report states Xiaomi is controlled through weighted voting rights: each Class A share has 10 votes and each Class B share has one vote; Lei Jun held about 61.0% of voting rights and Lin Bin about 6.7% for non-reserved matters as of December 31, 2025.": "年报显示，小米采用不同投票权结构：每股 A 类股份有 10 票，每股 B 类股份有 1 票；截至 2025 年 12 月 31 日，雷军对非保留事项拥有约 61.0% 投票权，林斌拥有约 6.7%。",
        "As of May 18, 2026, Xiaomi's quarterly results page shows 2025 Q1-Q4 results and does not yet show a 2026 Q1 official result announcement.": "截至 2026 年 5 月 18 日，小米季度业绩页面显示 2025 年 Q1-Q4 业绩，尚未显示 2026 年 Q1 正式业绩公告。",
        "IDC preliminary Q1 2026 data shows global smartphone shipments down 2.9% YoY to 293.8M units; Xiaomi shipped 33.8M units, held 11.5% share, ranked third, and declined 19.1% YoY amid memory constraints and portfolio actions.": "IDC 2026 年 Q1 初步数据显示，全球智能手机出货同比下降 2.9% 至 2.938 亿台；小米出货 3380 万台，份额 11.5%，排名第三，并在内存约束和产品组合调整下同比下降 19.1%。",
        "Counterpoint's Q1 2026 smartphone monitor, as reported by Gadgets360, estimated global smartphone shipments fell 6% YoY and Xiaomi retained third place with about 12% share, pressured by memory shortages and entry-level exposure.": "Gadgets360 引述 Counterpoint 2026 年 Q1 智能手机监测称，全球智能手机出货同比下降 6%，小米以约 12% 份额保持第三名，但受内存短缺和入门价位敞口影响承压。",
        "CnEVPost, citing CPCA, reports Xiaomi EV 2025 China passenger NEV retail sales of 411,837 units, ranking tenth with 3.2% share; BYD led with 27.2% and Tesla China ranked fifth with 4.9%.": "CnEVPost 引述乘联会数据称，小米 EV 2025 年中国乘用新能源车零售 411,837 辆，排名第十，份额 3.2%；比亚迪以 27.2% 领先，特斯拉中国以 4.9% 排名第五。",
        "SAMR notice states Xiaomi Auto recalled 116,887 SU7 Standard EVs produced from February 6, 2024 to August 30, 2025 because L2 highway assisted driving could be insufficient in recognizing, warning or handling extreme scenarios, increasing collision risk if drivers do not intervene promptly.": "国家市场监督管理总局公告显示，小米汽车召回 116,887 辆 2024 年 2 月 6 日至 2025 年 8 月 30 日生产的 SU7 标准版，原因是 L2 高速领航辅助驾驶在极端场景识别、预警或处置上可能不足，如驾驶员未及时干预会增加碰撞风险。",
        "The 2018 prospectus describes Xiaomi's mission, internet-company self-definition, April 2010 founding, Hong Kong offering timetable, WVR risks, and original model centered on smartphones and smart hardware connected by an IoT platform.": "2018 年招股书描述了小米的使命、互联网公司自我定义、2010 年 4 月创立、香港发行安排、不同投票权风险，以及以智能手机和智能硬件为核心并由 IoT 平台连接的原始模型。",
    }
    if body in exact:
        return f"{exact[body]} {bracket}".strip()

    section_names = {
        "source and origin": "源头溯源",
        "company history": "公司历史",
        "current business": "当下生意",
        "value chain position": "产业链定位",
        "competitive landscape": "竞争格局",
        "strategy analysis": "战略分析",
        "organization, culture, and governance": "组织、文化与治理",
        "risk sweep": "风险排雷",
    }
    well_evidenced = re.fullmatch(r"Treat (.+) as well evidenced for baseline work\.", body)
    if well_evidenced:
        name = section_names.get(well_evidenced.group(1), well_evidenced.group(1))
        return f"{name}可作为证据较充分的基线使用。 {bracket}".strip()
    partial_evidenced = re.fullmatch(r"Treat (.+) as partially evidenced for baseline work\.", body)
    if partial_evidenced:
        name = section_names.get(partial_evidenced.group(1), partial_evidenced.group(1))
        return f"{name}可作为部分证据基线使用。 {bracket}".strip()
    add_source = re.fullmatch(r"Add at least one more independent source for (.+)\.", body)
    if add_source:
        name = section_names.get(add_source.group(1), add_source.group(1))
        return f"为{name}至少补充一个独立来源。 {bracket}".strip()

    translated = body
    replacements = [
        ("Revenue was", "收入为"),
        ("Net income was", "净利润为"),
        ("Operating income was", "经营利润为"),
        ("Gross profit was", "毛利为"),
        ("Assets was", "资产为"),
        ("Liabilities was", "负债为"),
        ("Stockholders equity was", "股东权益为"),
        ("Cash and cash equivalents was", "现金及现金等价物为"),
        ("USD for period ending", "美元，期间截止日"),
        ("in 10-Q.", "，来自 10-Q。"),
        ("for period ending", "，期间截止日"),
        ("Add at least one more independent source for source and origin.", "为源头溯源至少补充一个独立来源。"),
        ("Add at least one more independent source for organization, culture, and governance.", "为组织、文化与治理至少补充一个独立来源。"),
    ]
    for old, new in replacements:
        translated = translated.replace(old, new)
    return f"{translated} {bracket}".strip()


def _render_kpi_row(kpi: dict[str, Any]) -> str:
    return (
        "<tr>"
        f"<td>{escape(kpi['label'])}</td>"
        f"<td>{escape(kpi['value_snippet'])}</td>"
        f"<td><span class=\"chip\">{escape(kpi['evidence_id'])}</span></td>"
        f"<td>{escape(kpi['why_it_matters'])}</td>"
        "</tr>"
    )


def _render_message_row(message: dict[str, Any]) -> str:
    questions = "<br>".join(escape(_display_question(question)) for question in message["follow_up_questions"][:3])
    fenghe = message["fenghe"]
    fenghe_text = f"主驱动 {fenghe['dominant_d']} · 5M {fenghe['five_m']} · 时间框架 {fenghe['time_frame']}"
    impact_class = f"impact-{message['impact']}"
    nodes = _display_business_nodes(message.get("affected_business_node_ids", [])[:4])
    assumptions = _display_assumptions(message.get("affected_assumption_ids", [])[:3])
    message_fact = _zh_text(message["message_fact"])
    if len(message_fact) > 210:
        message_fact = message_fact[:207] + "..."
    source_name = SOURCE_NAME_ZH.get(message["source_name"], message["source_name"])
    research_action = _zh_text(message["research_action"])
    category = INFO_CATEGORY_LABEL_ZH.get(message.get("information_category", ""), message.get("information_category", ""))
    return (
        "<tr>"
        f"<td><span class=\"chip\">{escape(message['evidence_id'])}</span><br><strong>{escape(source_name)}</strong><br><span class=\"note\">{escape(category)} · {escape(message_fact)}</span></td>"
        f"<td class=\"{impact_class}\">{escape(_zh_text(message['impact']))}<br><span class=\"note\">{escape(fenghe_text)}</span></td>"
        f"<td><strong>业务节点</strong><br>{escape(nodes)}<br><strong>假设</strong><br>{escape(assumptions)}</td>"
        f"<td>{questions or escape(research_action)}</td>"
        f"<td>{escape(_zh_text(message['marginal_change']))}</td>"
        "</tr>"
    )


def _display_business_nodes(node_ids: list[str]) -> str:
    labels = {
        "smartphone": "手机平台",
        "iot": "IoT 与互联设备",
        "services": "互联网服务",
        "smart_ev": "智能 EV",
        "supply_chain": "供应链与制造",
        "capital_allocation": "资本配置",
        "governance_control": "治理与控制权",
        "group_financials": "集团财务模型",
    }
    if not node_ids:
        return "未映射"
    return "、".join(labels.get(node_id, node_id) for node_id in node_ids)


def _display_assumptions(assumption_ids: list[str]) -> str:
    labels = {
        "assumption_smartphone_001": "手机基盘假设",
        "assumption_iot_001": "IoT 生态假设",
        "assumption_services_001": "互联网服务利润池假设",
        "assumption_smart_ev_001": "智能 EV 利润池假设",
        "assumption_supply_chain_001": "供应链与制造假设",
        "assumption_capital_allocation_001": "资本配置假设",
        "assumption_governance_control_001": "治理与控制权假设",
        "assumption_group_financials_001": "集团财务模型假设",
    }
    if not assumption_ids:
        return "未关联假设"
    return "、".join(labels.get(assumption_id, assumption_id) for assumption_id in assumption_ids)


def _render_risk_row(risk: dict[str, Any]) -> str:
    tests = "; ".join(risk["monitoring_tests"][:4])
    evidence = risk["evidence_id"] or "foundation_gap"
    return (
        "<tr>"
        f"<td>{escape(risk['statement'])}</td>"
        f"<td>{escape(risk['severity'])}</td>"
        f"<td><span class=\"chip\">{escape(evidence)}</span></td>"
        f"<td>{escape(tests)}</td>"
        "</tr>"
    )
