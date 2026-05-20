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

SOURCE_NAME_ZH = {
    "Xiaomi IR Company Profile": "小米 IR 公司简介",
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
    question_rows = _build_question_graph(normalized, foundation_graph)
    message_rows = _build_message_flow(normalized, evidence, foundation_graph, question_rows)

    foundation_path = research_dir / "foundation_graph.json"
    question_path = research_dir / "question_graph.jsonl"
    message_path = research_dir / "message_flow.jsonl"
    dashboard_path = research_dir / "research_dashboard.html"
    pages_dir = research_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    _write_json(foundation_path, foundation_graph)
    _write_jsonl(question_path, question_rows)
    _write_jsonl(message_path, message_rows)
    _write_text(dashboard_path, _render_dashboard(normalized, foundation_graph, question_rows, message_rows))
    _write_text(pages_dir / "source_origin.html", _render_source_origin_page(normalized, foundation_graph, evidence))

    covered = sum(1 for section in foundation_graph["sections"] if section["status"] != "missing")
    RunLog(stock_dir / "logs").append(
        "research_system",
        RunStatus.SUCCESS,
        tickers=[normalized],
        records_fetched=len(evidence),
        records_new=len(question_rows) + len(message_rows) + len(foundation_graph["sections"]),
    )

    return ResearchSystemResult(
        ticker=normalized,
        foundation_graph_path=str(foundation_path),
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


def _build_section(section_rule: dict[str, Any], evidence: list[EvidenceRecord]) -> dict[str, Any]:
    evidence_ids = _evidence_ids_for_keywords(evidence, section_rule["keywords"])
    status = _coverage_status(evidence_ids)
    summaries = _summaries_for_ids(evidence, evidence_ids, limit=4)
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

    return {
        "id": section_rule["id"],
        "label": section_rule["label"],
        "status": status,
        "evidence_ids": evidence_ids,
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


def _render_dashboard(
    ticker: str,
    foundation_graph: dict[str, Any],
    questions: list[dict[str, Any]],
    messages: list[dict[str, Any]],
) -> str:
    p0_questions = [question for question in questions if question["priority"] == "P0"]
    section_cards = "\n".join(_render_foundation_section_card(section) for section in foundation_graph["sections"])
    question_cards = "\n".join(_render_question_card(question) for question in p0_questions[:10])
    message_rows = "\n".join(_render_message_row(message) for message in messages[:14])
    summary = _committee_summary(ticker, foundation_graph, p0_questions, messages)
    summary_cards = "\n".join(
        f"<div class=\"summary-card\"><span>{escape(_zh_text(item['label']))}</span><strong>{escape(_zh_text(item['value']))}</strong><p>{escape(_zh_text(item['detail']))}</p></div>"
        for item in summary["cards"]
    )
    disconfirming_items = "\n".join(f"<li>{escape(item)}</li>" for item in summary["disconfirming"])

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(ticker)} 四层投研工作台</title>
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
</head>
<body>
  <header>
    <h1>{escape(ticker)} 四层投研工作台</h1>
    <p class="subtitle">投委会摘要、公司基础画像、关键问题下钻、消息流更新区。每个判断都回到证据、假设和反证条件，而不是停留在静态报告段落。</p>
  </header>
  <nav>
    <a href="#committee">投委会摘要</a>
    <a href="#foundation">公司基础画像</a>
    <a href="#questions">关键问题下钻</a>
    <a href="#message-flow">消息流更新区</a>
  </nav>
  <main>
    <section id="committee">
      <div class="layer-label">第一层</div>
      <h2>一页投委会摘要</h2>
      <div class="summary-grid">{summary_cards}</div>
      <div class="committee">
        <div class="committee-panel">
          <h3>最关键结论</h3>
          <p>{escape(summary["key_conclusion"])}</p>
        </div>
        <div class="committee-panel">
          <h3>最大不确定性</h3>
          <p><strong>{escape(summary["max_uncertainty"])}</strong></p>
          <p class="note">该问题必须先下钻，不能被总量收入或单条新闻掩盖。</p>
        </div>
        <div class="committee-panel">
          <h3>主驱动</h3>
          <p>{escape(summary["dominant_driver"])}</p>
        </div>
        <div class="committee-panel">
          <h3>反证条件</h3>
          <ul>{disconfirming_items}</ul>
        </div>
      </div>
    </section>

    <section id="foundation">
      <div class="layer-label">第二层</div>
      <h2>公司基础画像：八步框架，每节拆成事实、推论、判断、缺口</h2>
      <div class="foundation-grid">{section_cards}</div>
    </section>

    <section id="questions">
      <div class="layer-label">第三层</div>
      <h2>关键问题下钻：问题树</h2>
      <div class="grid">{question_cards}</div>
    </section>

    <section id="message-flow">
      <div class="layer-label">第四层</div>
      <h2>消息流更新区：消息流冲击分析挂到问题、假设和业务节点</h2>
      <table>
        <thead><tr><th>消息 / 证据</th><th>影响</th><th>挂载节点</th><th>关联问题</th><th>边际变化</th></tr></thead>
        <tbody>{message_rows}</tbody>
      </table>
      <p class="note">边界：该页面不是交易指令。低可靠证据只生成研究线索；任何强化结论的输出仍需说明主导 D 驱动、3T 时间框架和反证测试。</p>
    </section>
  </main>
</body>
</html>
"""


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
    professional_records = _records_matching(evidence, ["professional_report", "sell_side_report", "sell_side_report_summary"], 6)
    professional_cards_html = _render_professional_report_cards(professional_records)
    thesis_html = _render_source_origin_thesis(ticker, evidence)
    phase_rows = _render_source_origin_phase_rows(ticker, evidence)
    mechanism_rows = _render_source_origin_mechanism_rows(ticker, evidence)

    question_items = [
        "公司为什么会在那个时间点出现？当时的技术、渠道、用户和成本条件是什么？",
        "公司最早解决的原始痛点是什么？第一批用户为什么愿意迁移？",
        "最初的产品切口、渠道切口和价格切口分别是什么？",
        "创始团队的能力结构为什么适合这个问题？哪些能力是后来可迁移的？",
        "早期商业模型如何形成飞轮：获客、复购、生态扩展、利润池各自在哪里？",
        "这些早期基因今天仍是优势，还是已经变成组织、治理或业务边界约束？",
    ]
    question_html = "".join(f"<li>{escape(item)}</li>" for item in question_items)

    granularity_rows = [
        (
            "事实层",
            "精确到日期、主体、产品、渠道、融资/上市文件和一手出处。",
            "创立时间、创始人/联合创始人、早期产品、公司自我定义、招股书/年报/IR 页面。",
            "只写“公司成立于某年”不够，必须能回到证据 ID。",
        ),
        (
            "机制层",
            "把事实连成因果链，而不是堆公司历史。",
            "原始痛点 -> 产品切口 -> 获客方式 -> 成本/价格优势 -> 可扩展利润池。",
            "只写使命、口号、创始人履历不够，要说明为什么这套机制成立。",
        ),
        (
            "迁移层",
            "判断早期能力能否迁移到今天的新业务。",
            "手机入口、IoT 连接、互联网服务、智能制造、EV 安全责任之间的能力迁移和断点。",
            "不能直接把早期成功外推到 EV、AI 或其他新业务。",
        ),
        (
            "边界层",
            "明确哪些问题还不能回答，以及后续消息流要验证什么。",
            "缺失的一手访谈、早期用户数据、早期毛利/现金流、组织激励、质量事件和售后成本。",
            "缺口要进入问题树，而不是在报告里用模糊措辞掩盖。",
        ),
    ]
    granularity_html = "".join(
        "<tr>"
        f"<td><strong>{escape(level)}</strong></td>"
        f"<td>{escape(answer_depth)}</td>"
        f"<td>{escape(evidence_need)}</td>"
        f"<td>{escape(not_enough)}</td>"
        "</tr>"
        for level, answer_depth, evidence_need, not_enough in granularity_rows
    )

    evidence_cards = [
        _render_source_origin_evidence_card(
            "创立时点与公司定位",
            "确认公司从哪里来、最初把自己定义成什么、上市文件如何描述原始业务模型。",
            _records_matching(evidence, ["found", "founded", "profile", "prospectus", "ipo", "mission", "launch"], 5) or primary_records[:2],
        ),
        _render_source_origin_evidence_card(
            "第一产品楔子",
            "专业报告不会只写创始人履历，而会追问最早凭什么获得用户：产品体验、价格、渠道、社区还是供给变化。",
            _records_matching(evidence, ["miui", "xiaomi phone", "launch", "first users", "wedge", "founding_context"], 5),
        ),
        _render_source_origin_evidence_card(
            "原始模型与飞轮",
            "把早期手机、智能硬件、IoT 平台和互联网服务放在同一机制里看，判断其是否形成可复用增长逻辑。",
            _records_matching(evidence, ["prospectus", "business_model", "original model", "smart hardware connected", "iot platform", "internet-company"], 5),
        ),
        _render_source_origin_evidence_card(
            "今日延伸与边界",
            "检验早期效率、用户和生态基因延伸到智能制造、EV 和 AI 时，是否遇到安全、资本开支、质量控制和售后责任的新边界。",
            _records_matching(evidence, ["smart ev", "vehicle", "auto", "recall", "safety", "capex", "manufacturing", "new initiatives", "human_car_home"], 5),
        ),
    ]
    evidence_cards_html = "\n".join(evidence_cards)

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
    evidence_rows = evidence_rows or '<tr><td colspan="5" class="note">当前没有可展示证据。</td></tr>'

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
    body {{
      margin: 0;
      color: var(--ink);
      background:
        linear-gradient(90deg, rgba(18,26,34,.045) 1px, transparent 1px),
        linear-gradient(0deg, rgba(18,26,34,.035) 1px, transparent 1px),
        var(--paper);
      background-size: 36px 36px;
      font-family: "Avenir Next", "Gill Sans", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.62;
    }}
    header {{
      padding: 34px clamp(18px, 5vw, 64px) 26px;
      color: #fff;
      background: var(--charcoal);
      border-bottom: 7px solid var(--green);
    }}
    .eyebrow {{ margin: 0 0 8px; color: #a7c8bd; font-size: 13px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }}
    h1 {{ margin: 0; font-size: clamp(34px, 5.4vw, 62px); line-height: 1; letter-spacing: 0; }}
    h2 {{ margin: 0 0 12px; font-size: clamp(22px, 3vw, 34px); letter-spacing: 0; }}
    h3 {{ margin: 0 0 8px; font-size: 18px; }}
    p {{ margin: 0 0 10px; }}
    a {{ color: var(--blue); }}
    .subtitle {{ max-width: 980px; margin-top: 14px; color: #d8e1dd; font-size: 17px; }}
    .nav {{
      position: sticky;
      top: 0;
      z-index: 10;
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding: 10px clamp(14px, 4vw, 54px);
      background: rgba(246,243,234,.96);
      border-bottom: 1px solid var(--line);
      backdrop-filter: blur(10px);
    }}
    .nav a {{
      flex: 0 0 auto;
      padding: 7px 10px;
      color: var(--ink);
      text-decoration: none;
      border: 1px solid var(--line);
      background: #fff;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 700;
    }}
    main {{ width: min(1160px, calc(100% - 28px)); margin: 22px auto 58px; }}
    section {{ margin: 16px 0; padding: clamp(18px, 3vw, 30px); background: rgba(255,253,250,.95); border: 1px solid var(--line); }}
    .summary-strip {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-top: 18px; }}
    .metric {{ padding: 14px; background: #fff; border: 1px solid var(--line); min-width: 0; }}
    .metric span {{ display: block; color: var(--muted); font-size: 12px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; }}
    .metric strong {{ display: block; margin-top: 6px; font-size: clamp(21px, 2.4vw, 32px); line-height: 1.08; }}
    .lead-grid {{ display: grid; grid-template-columns: .95fr 1.05fr; gap: 14px; align-items: start; }}
    .question-list {{ margin: 0; padding-left: 20px; }}
    .question-list li {{ margin: 7px 0; }}
    .evidence-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .evidence-card {{ padding: 16px; background: #fff; border: 1px solid var(--line); border-left: 5px solid var(--green); min-width: 0; }}
    .evidence-card p {{ color: var(--muted); }}
    .field {{ margin-top: 12px; }}
    .field b {{ display: block; margin-bottom: 4px; color: var(--muted); font-size: 12px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; }}
    .note {{ color: var(--muted); font-size: 13px; }}
    .chip {{ display: inline-flex; max-width: 100%; margin: 2px 4px 2px 0; padding: 2px 7px; border-radius: 999px; background: #edf3f1; color: #2a5146; font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; overflow-wrap: anywhere; }}
    .status-evidenced {{ color: var(--green); font-weight: 800; }}
    .status-partial {{ color: var(--amber); font-weight: 800; }}
    .status-missing {{ color: var(--red); font-weight: 800; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; font-size: 14px; }}
    th, td {{ padding: 10px; border-bottom: 1px solid var(--line); vertical-align: top; text-align: left; }}
    th {{ color: var(--muted); font-size: 12px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; background: #eef2ee; }}
    .thesis-card {{ padding: 18px; background: #111820; color: #fff; border-left: 7px solid var(--green); }}
    .thesis-card p {{ color: #d8e1dd; }}
    .reference-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .reference-card {{ padding: 15px; background: #fff; border: 1px solid var(--line); border-top: 4px solid var(--blue); }}
    .reference-card p {{ color: var(--muted); }}
    .stage {{ color: var(--green); font-weight: 800; white-space: nowrap; }}
    ul {{ margin: 8px 0 0; padding-left: 20px; }}
    li {{ margin: 5px 0; }}
    .rule-box {{ padding: 16px; background: #f0f4f1; border-left: 5px solid var(--blue); }}
    @media (max-width: 880px) {{
      .summary-strip, .lead-grid, .evidence-grid, .reference-grid {{ grid-template-columns: 1fr; }}
      table {{ font-size: 13px; }}
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
    <a href="#calibration">专业写法</a>
    <a href="#thesis">源头结论</a>
    <a href="#phases">阶段复盘</a>
    <a href="#mechanism">机制拆解</a>
    <a href="#questions">要回答什么</a>
    <a href="#granularity">回答粒度</a>
    <a href="#evidence">当前证据</a>
    <a href="#judgment">当前判断</a>
    <a href="#gaps">缺口</a>
  </nav>
  <main>
    <section id="calibration">
      <h2>专业报告写法校准</h2>
      <p>我重新按公开深度报告的写法整理本页：源头不是“公司简介”，而是要解释一个投资命题的起点。专业报告通常先给阶段化历史，再抽出产品楔子、用户/渠道机制、商业模型闭环，最后说明这些早期基因怎样影响今天。</p>
      <div class="reference-grid">{professional_cards_html}</div>
    </section>

    <section id="thesis">
      <h2>{escape(company_name)}源头结论</h2>
      {thesis_html}
    </section>

    <section id="phases">
      <h2>阶段复盘：把历史写成因果链</h2>
      <table>
        <thead><tr><th>阶段</th><th>发生了什么</th><th>投研含义</th><th>证据</th></tr></thead>
        <tbody>{phase_rows}</tbody>
      </table>
    </section>

    <section id="mechanism">
      <h2>机制拆解：源头如何影响今天</h2>
      <table>
        <thead><tr><th>问题</th><th>当前回答</th><th>为什么重要</th><th>证据 / 下一步</th></tr></thead>
        <tbody>{mechanism_rows}</tbody>
      </table>
    </section>

    <section id="questions">
      <div class="lead-grid">
        <div>
          <h2>这一页要回答什么</h2>
          <p>源头溯源的目的，是把公司最早的“问题-能力-模型”找清楚。后续任何关于护城河、管理层、第二曲线或估值弹性的讨论，都应先回到这里校验。</p>
        </div>
        <ol class="question-list">{question_html}</ol>
      </div>
    </section>

    <section id="granularity">
      <h2>回答到什么粒度</h2>
      <table>
        <thead><tr><th>层级</th><th>需要回答到的深度</th><th>最低证据要求</th><th>什么不够</th></tr></thead>
        <tbody>{granularity_html}</tbody>
      </table>
    </section>

    <section id="evidence">
      <h2>{escape(company_name)}当前证据</h2>
      <div class="evidence-grid">{evidence_cards_html}</div>
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
      <h2>证据索引</h2>
      <table>
        <thead><tr><th>证据 ID</th><th>来源</th><th>日期</th><th>可靠性 / 重要性</th><th>摘要</th></tr></thead>
        <tbody>{evidence_rows}</tbody>
      </table>
    </section>
  </main>
</body>
</html>
"""


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


def _render_evidence_record_row(record: EvidenceRecord) -> str:
    source_name = SOURCE_NAME_ZH.get(record.source_name, record.source_name)
    date = record.published_at[:10] if record.published_at else f"抓取 {record.fetched_at[:10]}"
    reliability = f"{_zh_text(record.reliability)} / {_zh_text(record.materiality)}"
    return (
        "<tr>"
        f"<td><span class=\"chip\">{escape(record.id)}</span></td>"
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
    detail_link = ""
    if section.get("id") == "source_origin":
        detail_link = '<a class="detail-link" href="pages/source_origin.html">打开详情页</a>'
    return (
        f"<article class=\"{card_class}\">"
        f"<h3>{escape(section_label)} <span class=\"status-{escape(section['status'])}\">{escape(status_label)}</span></h3>"
        f"<p>{evidence_html}</p>"
        f"<div class=\"field\"><b>事实</b>{facts}</div>"
        f"<div class=\"field\"><b>推论</b>{inferences}</div>"
        f"<div class=\"field\"><b>判断</b>{judgments}</div>"
        f"<div class=\"field\"><b>缺口</b>{gaps}</div>"
        f"{detail_link}"
        "</article>"
    )


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
    return (
        "<tr>"
        f"<td><span class=\"chip\">{escape(message['evidence_id'])}</span><br><strong>{escape(source_name)}</strong><br><span class=\"note\">{escape(message_fact)}</span></td>"
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
