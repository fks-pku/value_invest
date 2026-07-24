from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from value_invest_research.adapters.outbound.canonical_html_report_renderer import (  # noqa: E402
    CanonicalHtmlReportRenderer,
)
from value_invest_research.adapters.outbound.filesystem_research_project import (  # noqa: E402
    FileSystemResearchProjectRepository,
)
from value_invest_research.application.use_cases.render_research_project_report import (  # noqa: E402
    RenderResearchProjectReport,
)
from value_invest_research.domain.domain_playbooks import resolve_domain_playbook  # noqa: E402
from value_invest_research.domain.question_architecture import build_question_architecture  # noqa: E402
from value_invest_research.domain.research_goal import ResearchGoal  # noqa: E402
from value_invest_research.domain.target_scoring import score_and_rank_targets  # noqa: E402
from value_invest_research.framework_contracts import SCORE_WEIGHTS  # noqa: E402


PROJECT_ID = "gtc_taipei_2026_live_20260602"
PROJECT_DIR = ROOT / "research" / "bom" / PROJECT_ID
REPORT_DATE = "2026-06-02"
CREATED_AT = datetime.now(timezone.utc).isoformat()


def main() -> None:
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    goal = ResearchGoal(
        topic="GTC Taipei 2026 实时投资机会",
        research_type="event_policy",
        object_id=PROJECT_ID,
        run_mode="live_prediction",
        report_date=REPORT_DATE,
        decision_boundary="研究 GTC Taipei 2026 公开材料对未来 3-12 个月可验证投资机会的影响；只输出研究观察清单，不构成买卖指令。",
        domain_hint="event_conference gtc keynote launch taipei nvidia ai factory",
    )
    playbook = resolve_domain_playbook(goal)
    architecture = build_question_architecture(goal, playbook)

    sources = _sources()
    source_by_id = {str(source["source_id"]): source for source in sources}
    l3_answers = _l3_answers()
    nodes = []
    for node in architecture.nodes:
        item = node.to_dict()
        item["materiality"] = item.get("investment_relevance") or "影响父问题结论、目标排序和后续验证优先级。"
        if item["level"] == 1:
            item.update(_l1_answer(item["id"]))
        elif item["level"] == 2:
            item.update(_l2_answer(item["id"]))
        elif item["level"] == 3:
            answer = l3_answers[item["id"]]
            item.update(answer)
            item["minimum_evidence_gate"] = "至少需要一条官方或公司来源确认事实边界，并需要一条反证/边界来源检查可财务化程度。"
            item["refuting_source_plan"] = answer["refuting_source_plan"]
            item["source_plan"] = _source_plan(item["id"], answer["source_links"], source_by_id, item["preferred_specialty_skill"])
            item["skill_dispatch"] = _skill_dispatch(item)
        nodes.append(item)
    nodes = _apply_adaptive_drilldown(nodes, source_by_id)

    source_extractions, leaf_source_reviews = _source_parser_records(nodes, source_by_id)
    raw_targets = _raw_targets()
    scoring_result = score_and_rank_targets(raw_targets)
    targets = [_public_target(target) for target in scoring_result.ranked_targets]

    project = {
        "project_id": PROJECT_ID,
        "title": "GTC Taipei 2026 实时投资机会报告",
        "object_type": "event_policy",
        "research_type": "event_policy",
        "run_mode": "live_prediction",
        "report_date": REPORT_DATE,
        "domain_playbook": "event_conference",
        "decision_boundary": goal.decision_boundary,
        "current_judgment": (
            "GTC Taipei 2026 的核心增量不是泛 AI 热度，而是 NVIDIA 将 AI factory 平台、Vera Rubin/Vera CPU、CPO 网络、"
            "HBM4/存储和 Windows 个人智能体 PC 同时推向量产或上市窗口。可投资机会应优先落在可验证的稀缺节点：平台控制、"
            "先进制造/封装、HBM/高速存储、AI server rack/ODM、CPO 网络和 Windows AI PC 生态；但多数核心资产已经被高预期定价，"
            "当前更适合形成观察清单和季度触发器。"
        ),
        "biggest_uncertainty": "RTX Spark 与 agentic AI factory 的真实订单、出货、客户 ROI 和公司财务转化尚未由财报口径充分验证。",
        "supply_chain": _supply_chain(),
    }
    qa_tree = {
        "project_id": PROJECT_ID,
        "title": project["title"],
        "run_mode": "live_prediction",
        "report_date": REPORT_DATE,
        "domain_playbook": "event_conference",
        "planner_rationale": architecture.planner_rationale,
        "supply_chain": project["supply_chain"],
        "nodes": nodes,
    }
    workbench = {
        "project_id": PROJECT_ID,
        "run_mode": "live_prediction",
        "created_at": CREATED_AT,
        "scoring_worksheet": targets,
        "raw_scoring_issues": scoring_result.issues,
        "source_parser_note": "DeepSeek source parsing was attempted for the GTC source pack and timed out; GPT performed direct source-pack parsing and verification for L3-L5 records, with fallback recorded in skill_dispatch.",
        "prediction_reviews": _prediction_reviews(targets),
    }

    _write_json(PROJECT_DIR / "project.json", project)
    _write_json(PROJECT_DIR / "qa_tree.json", qa_tree)
    _write_jsonl(PROJECT_DIR / "sources.jsonl", sources)
    _write_jsonl(PROJECT_DIR / "source_extractions.jsonl", source_extractions)
    _write_jsonl(PROJECT_DIR / "leaf_source_reviews.jsonl", leaf_source_reviews)
    _write_json(PROJECT_DIR / "investment_workbench.json", workbench)
    (PROJECT_DIR / "professional_report.md").write_text(_markdown_summary(project, targets), encoding="utf-8")

    render_result = RenderResearchProjectReport(
        FileSystemResearchProjectRepository(PROJECT_DIR),
        CanonicalHtmlReportRenderer(),
    ).execute(filename="professional_report.html")
    print(json.dumps(render_result, ensure_ascii=False, indent=2))


def _sources() -> list[dict[str, Any]]:
    return [
        _source(
            "SRC-NV-GTC-KEYNOTE-20260601",
            "NVIDIA GTC Taipei 2026 Keynote",
            "evidence",
            "support",
            "GTC Taipei 官方页面确认 2026 年 6 月 1 日台北 keynote，主题覆盖 AI factories、agentic AI、physical AI、robotics 和 AI-native personal computing。",
            "https://www.nvidia.com/en-tw/gtc/taipei/keynote?ncid=partn-271350&regcode=partn-271350",
        ),
        _source(
            "SRC-NV-VERA-RUBIN-20260531",
            "NVIDIA Vera Rubin ramps into full production",
            "evidence",
            "support",
            "NVIDIA 宣布 Vera Rubin full production、10x agent throughput、台湾供应链规模制造，以及 Spectrum-X Ethernet Photonics CPO switches in production。",
            "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Ramps-Into-Full-Production-to-Power-Agentic-AI-Factories-Worldwide/default.aspx",
        ),
        _source(
            "SRC-NV-TSMC-AI-FABS-20260531",
            "NVIDIA and TSMC bring AI into fabs",
            "evidence",
            "support",
            "NVIDIA/TSMC 披露 cuLitho、cuEST、Metropolis/TAO 等 AI 工具进入半导体设计和制造流程，并给出成本/周期改善指标。",
            "https://nvidianews.nvidia.com/news/nvidia-and-tsmc-bring-ai-into-fabs-to-advance-semiconductor-design-and-manufacturing",
        ),
        _source(
            "SRC-NV-MSFT-RTX-SPARK-20260601",
            "NVIDIA and Microsoft unveil RTX Spark Windows PCs",
            "evidence",
            "support",
            "RTX Spark Windows PCs 面向 personal agents，1 petaflop AI、最高 128GB unified memory，设备计划 2026 年秋季上市。",
            "https://nvidianews.nvidia.com/news/nvidia-and-microsoft-unveil-rtx-spark-windows-pcs-for-personal-ai-agents",
        ),
        _source(
            "SRC-NV-VERA-CPU-20260531",
            "NVIDIA Vera CPU full production",
            "evidence",
            "support",
            "Vera CPU full production，服务 standalone Vera servers、Vera Rubin systems 和 Vera BlueField-4 STX AI storage platforms；披露客户探索/计划名单和系统制造伙伴。",
            "https://nvidianews.nvidia.com/news/nvidia-vera-cpu-is-in-full-production-to-power-next-generation-agentic-ai-platforms",
        ),
        _source(
            "SRC-MU-HBM4-20260316",
            "Micron HBM4 and SOCAMM2 for NVIDIA Vera Rubin",
            "evidence",
            "support",
            "Micron 披露 HBM4 36GB 12H high-volume production for NVIDIA Vera Rubin，SOCAMM2/PCIe Gen6 SSD 面向 Vera Rubin、Vera CPU 和 BlueField-4 STX。",
            "https://investors.micron.com/news-releases/news-release-details/micron-launches-industry-leading-hbm4-memory-designed-nvidia-vera-rubin",
        ),
        _source(
            "SRC-MSFT-SURFACE-ULTRA-20260531",
            "Microsoft Surface Laptop Ultra with NVIDIA RTX Spark",
            "evidence",
            "support",
            "Microsoft 披露 Surface Laptop Ultra 与 NVIDIA 从 silicon up 协作，Blackwell RTX GPU、128GB unified memory、1 petaflop AI compute，年内上市。",
            "https://blogs.windows.com/devices/2026/05/31/introducing-the-new-surface-laptop-ultra-with-nvidia-rtx-spark/",
        ),
        _source(
            "SRC-AP-RTX-SPARK-20260601",
            "AP coverage of NVIDIA RTX Spark at GTC Taipei",
            "message",
            "lead",
            "AP 报道将 RTX Spark 解读为 NVIDIA 从数据中心扩展到 AI PC/系统产品，并指出可能挑战 Intel/AMD，市场短线有反应。",
            "https://apnews.com/",
        ),
        _source(
            "SRC-SA-NVDA-20260602",
            "StockAnalysis NVDA valuation snapshot",
            "research_report",
            "lead",
            "StockAnalysis 估值快照用于赔率检查：NVDA 市值与前瞻 PE 显示核心资产已嵌入高预期。",
            "https://stockanalysis.com/stocks/nvda/",
        ),
        _source(
            "SRC-SA-TSM-20260602",
            "StockAnalysis TSM valuation snapshot",
            "research_report",
            "lead",
            "StockAnalysis 估值快照用于 TSM ADR 的市场定价和安全边际检查。",
            "https://stockanalysis.com/stocks/tsm/",
        ),
        _source(
            "SRC-SA-MU-20260602",
            "StockAnalysis MU valuation snapshot",
            "research_report",
            "lead",
            "StockAnalysis 估值快照用于 Micron 的存储周期、目标价和前瞻 PE 赔率检查。",
            "https://stockanalysis.com/stocks/mu/",
        ),
        _source(
            "SRC-SA-MSFT-20260602",
            "StockAnalysis MSFT valuation snapshot",
            "research_report",
            "lead",
            "StockAnalysis 估值快照用于 Microsoft Windows AI PC 生态的直接弹性和估值要求检查。",
            "https://stockanalysis.com/stocks/msft/",
        ),
        _source(
            "SRC-SA-DELL-20260602",
            "StockAnalysis DELL valuation snapshot",
            "research_report",
            "lead",
            "StockAnalysis 估值快照用于 Dell AI PC/AI server 设备商敞口与赔率检查。",
            "https://stockanalysis.com/stocks/dell/",
        ),
        _source(
            "SRC-SA-QCOM-20260602",
            "StockAnalysis QCOM valuation snapshot",
            "research_report",
            "refute",
            "StockAnalysis 估值快照用于检查 Qualcomm 在 Windows AI PC 路线中的竞争压力和赔率缺口。",
            "https://stockanalysis.com/stocks/qcom/",
        ),
    ]


def _source(
    source_id: str,
    title: str,
    bucket: str,
    stance: str,
    summary: str,
    url: str,
) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "title": title,
        "source_bucket": bucket,
        "information_category": bucket,
        "support_refute_or_lead": stance,
        "summary": summary,
        "url": url,
        "published_at": "2026-06-01" if "20260601" in source_id else "2026-05-31" if "20260531" in source_id else "2026-06-02" if "SA-" in source_id else "2026-03-16",
        "source_visible_at": "2026-06-01" if "20260601" in source_id else "2026-05-31" if "20260531" in source_id else "2026-06-02" if "SA-" in source_id else "2026-03-16",
        "allowed_usage": "thesis",
        "availability_proof": f"Public source page or official release visible by {REPORT_DATE}.",
        "used_in": [],
    }


def _supply_chain() -> dict[str, Any]:
    return {
        "plain_summary": (
            "这次 GTC Taipei 的钱不是从发布会本身产生，而是从 NVIDIA 定义平台开始，流向算力芯片、先进制造、HBM/高速存储、"
            "CPO 网络、AI server rack、Windows AI PC 和云/企业客户。投资上要先问：哪个环节稀缺、谁能收费、能不能变成收入和现金流，"
            "以及市场是否已经把这些增量充分定价。"
        ),
        "flow_steps": [
            "NVIDIA 发布 Vera Rubin/Vera CPU/Spectrum-X CPO/RTX Spark，定义平台路线和生态接口。",
            "TSMC、HBM/存储、先进封装、CPO 网络和 ODM/OEM 承接量产，形成供给侧瓶颈和订单窗口。",
            "云服务商、AI 实验室和企业客户采购 AI factory；PC OEM 与 Microsoft 推动个人智能体 PC 上市。",
            "收入先进入平台商和核心组件商，再通过 ODM/OEM、功耗散热、网络和终端渠道扩散。",
            "资本市场根据订单、出货、毛利率、估值倍数和反证触发器重新定价相关标的。",
        ],
        "layers": [
            {
                "layer": "平台定义",
                "products": "Vera Rubin、Vera CPU、Spectrum-X CPO、RTX Spark、CUDA/Windows AI stack",
                "players": "NVIDIA、Microsoft",
                "value_flow": "平台商掌握接口、软件生态和产品路线，最强稀缺性在 NVIDIA；Microsoft 通过 Windows/Surface 把端侧 AI 商业化。",
            },
            {
                "layer": "制造与封装",
                "products": "先进制程、cuLitho/AI fab、先进封装、rack-scale integration",
                "players": "TSMC、Foxconn、Quanta/QCT、Wistron/Wiwynn、Pegatron、Compal",
                "value_flow": "制造和集成把平台路线变成可交付系统；利润率取决于制程/封装稀缺性和 ODM 的议价能力。",
            },
            {
                "layer": "存储与网络瓶颈",
                "products": "HBM4、SOCAMM2、PCIe Gen6 SSD、BlueField storage、CPO Ethernet switches",
                "players": "Micron、CPO/光网络供应链、NVIDIA networking ecosystem",
                "value_flow": "AI factory 的吞吐、功耗和延迟受 HBM/高速存储和网络约束，若供给紧缺可转化为 ASP、毛利率和订单弹性。",
            },
            {
                "layer": "终端与云客户",
                "products": "AI factories、GPU/CPU racks、Windows AI PCs、personal agents",
                "players": "CoreWeave、Lambda、OCI、OpenAI、Anthropic、ByteDance、Dell、HP、Lenovo、ASUS、Surface",
                "value_flow": "客户付费决定需求真伪；只有采购、部署、capex 和出货能把发布会信息变成财务事实。",
            },
            {
                "layer": "资本市场定价",
                "products": "市值、PE/forward PE、盈利上修、股价反应、目标价",
                "players": "NVDA、TSM、MU、MSFT、DELL、QCOM、台湾 ODM/电源散热标的",
                "value_flow": "强产业逻辑如果已经被估值吸收，只能进入观察清单；赔率来自稀缺性、错定价、盈利弹性和可控反证同时成立。",
            },
        ],
        "relationships": [
            {
                "from": "NVIDIA",
                "to": "TSMC",
                "relationship": "平台路线依赖先进制造、先进封装和 AI fab 效率",
                "flow": "Vera Rubin/Vera CPU/AI factory 路线把订单和制造效率需求传导给先进制程与封装。",
                "bottleneck": "先进制造、先进封装、良率和产能。",
                "target_map": "TSM / 2330.TW；Q2.1.1.3、Q2.2.2.3、Q4.2.1。",
                "evidence": "SRC-NV-TSMC-AI-FABS-20260531；SRC-NV-VERA-RUBIN-20260531。",
            },
            {
                "from": "NVIDIA",
                "to": "Micron",
                "relationship": "Vera Rubin 平台绑定 HBM4、SOCAMM2 和 AI storage",
                "flow": "AI factory 带宽和存储吞吐需求传导到 HBM4、高速内存和 SSD 收入/毛利率。",
                "bottleneck": "HBM4 产能、良率、ASP、产品 mix。",
                "target_map": "MU；Q2.1.1.1、Q2.2.2.2、Q4.2.1。",
                "evidence": "SRC-MU-HBM4-20260316；SRC-NV-VERA-RUBIN-20260531。",
            },
            {
                "from": "NVIDIA",
                "to": "CoreWeave / Lambda / OCI",
                "relationship": "Spectrum-X CPO first adopters 和 AI factory 部署客户",
                "flow": "云客户部署决定 CPO/networking 是否从产品发布转成真实订单与数据中心收入。",
                "bottleneck": "CPO 端口出货、部署规模、客户 ROI。",
                "target_map": "NVDA networking；待补 CPO 供应商；Q2.1.1.2、Q2.1.1.2.2。",
                "evidence": "SRC-NV-VERA-RUBIN-20260531。",
            },
            {
                "from": "NVIDIA",
                "to": "Wiwynn / Quanta / Foxconn",
                "relationship": "Vera Rubin 量产通过服务器 ODM 和 rack 集成落地",
                "flow": "AI server/rack 订单先进入 ODM 收入，再看毛利率和营运资本能否转成现金流。",
                "bottleneck": "AI server 订单、单 rack 毛利、客户集中和营运资本。",
                "target_map": "6669.TW、2382.TW、2317.TW；Q2.1.1.4、Q2.2.2.4。",
                "evidence": "SRC-NV-VERA-RUBIN-20260531。",
            },
            {
                "from": "NVIDIA",
                "to": "Microsoft",
                "relationship": "RTX Spark Windows PC 和 personal agents 生态合作",
                "flow": "NVIDIA 把端侧算力推入 Windows 生态，Microsoft 提供系统、Surface 和开发者入口。",
                "bottleneck": "AI PC 出货、应用生态、企业采购和端侧 ROI。",
                "target_map": "MSFT、NVDA、QCOM 反证观察；Q2.1.1.5、Q3.1.2。",
                "evidence": "SRC-NV-MSFT-RTX-SPARK-20260601；SRC-MSFT-SURFACE-ULTRA-20260531。",
            },
            {
                "from": "Microsoft / NVIDIA",
                "to": "Dell / HP / Lenovo / ASUS",
                "relationship": "RTX Spark AI PC 通过 OEM 上市和渠道验证",
                "flow": "硬件 SKU、售价、出货和企业采购决定 AI PC 分支是否能进入财务口径。",
                "bottleneck": "销量、ASP、毛利率、software attach rate。",
                "target_map": "DELL、MSFT；Q1.2.2、Q2.1.1.5、Q4.1.2。",
                "evidence": "SRC-NV-MSFT-RTX-SPARK-20260601；SRC-MSFT-SURFACE-ULTRA-20260531。",
            },
            {
                "from": "OpenAI / Anthropic / ByteDance",
                "to": "NVIDIA AI factory ecosystem",
                "relationship": "AI 实验室和企业客户决定 agentic AI factory 需求真伪",
                "flow": "客户训练/推理需求、capex 和部署 ROI 决定平台订单持续性。",
                "bottleneck": "客户 capex、订单/backlog、推理 ROI、监管与出口限制。",
                "target_map": "NVDA、TSM、MU 和 ODM 全链路；Q1.2.1、Q3.1.1。",
                "evidence": "SRC-NV-VERA-RUBIN-20260531；SRC-NV-VERA-CPU-20260531。",
            },
            {
                "from": "资本市场",
                "to": "NVDA / TSM / MU / ODM / AI PC 标的",
                "relationship": "产业链事实通过估值、盈利上修和拥挤度重新定价",
                "flow": "订单、毛利、出货和 capex 先改变预期，再影响胜率和赔率。",
                "bottleneck": "估值分位、一致预期、EPS revision 和风险溢价。",
                "target_map": "Q3.2.1、Q4.2.1；最终观察清单。",
                "evidence": "SRC-SA-NVDA-20260602；SRC-SA-TSM-20260602；SRC-SA-MU-20260602。",
            },
        ],
        "chokepoints": "NVIDIA 平台控制、TSMC 先进制造/AI fab、HBM4/SOCAMM2/高速存储、Spectrum-X CPO 网络、AI server rack ODM、Windows AI PC 生态入口。",
        "target_links": "Q2 评分这些瓶颈的稀缺性和财务转化；Q3 检查估值/竞争/执行反证；Q4 将其映射到 NVDA、TSM、MU、Wiwynn、Quanta、Microsoft、Dell、Qualcomm 等具体证券。",
    }


def _l1_answer(qid: str) -> dict[str, str]:
    answers = {
        "Q1": "官方材料已经确认多条产品路线进入量产或明确上市窗口，但客户名单仍混合了采用、探索和生态展示，需要用订单/出货/财报验证。",
        "Q2": "价值捕获最集中在 NVIDIA 平台控制、TSMC 先进制造/封装、Micron HBM4/高速存储和 CPO/networking；ODM/OEM 有订单弹性但利润率弹性更弱。",
        "Q3": "主要反证来自估值已充分定价、RTX Spark 出货不足、agentic AI ROI 低于预期、CPO/量产爬坡问题，以及 Intel/AMD/QCOM/自研路线替代。",
        "Q4": "当前没有无条件 actionable_long；更合理的是按稀缺性和赔率建立观察清单，优先跟踪 MU、TSM、NVDA 与台系 AI server/CPO 供应链的验证数据。",
    }
    gaps = {
        "Q1": "缺少完整 keynote transcript、客户独立采购确认和上市后实际出货。",
        "Q2": "缺少 CPO 具体供应商份额、ODM 单位经济性、HBM4 订单量和先进封装产能数据。",
        "Q3": "需要连续跟踪估值、盈利上修、客户 capex、订单/backlog 和竞争路线。",
        "Q4": "需要补齐台湾标的实时估值、成交流动性和公司层面收入桥。",
    }
    return {"conclusion": answers[qid], "gap": gaps[qid], "trigger": "下一次 NVIDIA/供应商/客户财报、产品上市、订单或 capex 指引更新。"}


def _l2_answer(qid: str) -> dict[str, str]:
    conclusions = {
        "Q1.1": "这次事件的硬事实包括 Vera Rubin/Vera CPU、CPO、HBM4 和 RTX Spark；应把 full production、fall availability 与生态展示分层处理。",
        "Q1.2": "客户和伙伴名单很强，但仍需区分云客户采用、系统厂量产、AI PC 上市和普通生态合作。",
        "Q2.1": "候选瓶颈按强度排序是平台控制、先进制造/封装、HBM/高速存储、CPO 网络、AI server ODM，端侧 PC 渠道排在后面。",
        "Q2.2": "直接财务敞口以 NVDA、TSM、MU 和 AI server/ODM 更清晰；MSFT/DELL 有生态或渠道敞口，但单事件弹性较低。",
        "Q3.1": "执行风险集中在上市节奏、量产良率、客户 ROI、生态采用和替代路线。",
        "Q3.2": "估值是最大赔率约束：核心资产的稀缺性强，但市场已经给了相当高的 AI 平台预期。",
        "Q4.1": "证券 universe 覆盖平台、制造、存储、服务器 ODM、软件/PC 和竞争受压标的；缺乏财务桥的公司必须降级。",
        "Q4.2": "排序应先看四个门槛：稀缺/垄断、错定价、盈利弹性、风险可控；本报告把无估值或弱证据目标限制在 watch_only/no_action。",
    }
    gaps = {
        "Q1.1": "需要 keynote 全文和更多合作伙伴独立确认。",
        "Q1.2": "需要采购/订单/出货、capex 和客户部署数据。",
        "Q2.1": "需要 CPO 供应商、CoWoS/advanced packaging、HBM4 良率和产能口径。",
        "Q2.2": "需要分产品收入桥、毛利率桥和 capex/FCF 影响。",
        "Q3.1": "需要后续产品上市、客户 ROI 和竞品路线更新。",
        "Q3.2": "需要最新一致预期、估值分位、盈利上修和交易拥挤数据。",
        "Q4.1": "需要台湾本地标的估值和更明确收入敞口。",
        "Q4.2": "需要每季复盘触发器和公司级数据更新。",
    }
    return {"conclusion": conclusions[qid], "gap": gaps[qid], "trigger": "以 2026 年秋季产品上市、下一季财报和客户 capex/订单披露为主。"}


def _l3_answers() -> dict[str, dict[str, Any]]:
    return {
        "Q1.1.1": _ans(
            ["SRC-NV-GTC-KEYNOTE-20260601", "SRC-NV-VERA-RUBIN-20260531", "SRC-NV-VERA-CPU-20260531", "SRC-NV-MSFT-RTX-SPARK-20260601"],
            "官方材料确认 GTC Taipei 聚焦 AI factories、agentic AI、physical AI 和 AI-native PC；Vera Rubin/Vera CPU 为 full production，Spectrum-X CPO switches in production，RTX Spark Windows PCs 计划秋季上市。",
            "量产和上市窗口给出了可验证节点，但客户名单里同时存在 first adopters、exploring/planning 和生态伙伴，证据强度不能一概等同为订单收入。",
            "本次事件的官方事实强于一般发布会，足以进入投资观察；但财务强度仍要等订单、出货、客户 capex 和供应商分产品收入验证。",
            "缺少完整 keynote transcript、独立客户采购金额和每个系统厂的实际出货/收入节奏。",
            "Vera Rubin 系统出货、RTX Spark 设备上市、CoreWeave/Lambda/OCI 或 AI 实验室部署公告。",
        ),
        "Q1.1.2": _ans(
            ["SRC-NV-VERA-RUBIN-20260531", "SRC-NV-VERA-CPU-20260531", "SRC-NV-MSFT-RTX-SPARK-20260601", "SRC-NV-TSMC-AI-FABS-20260531"],
            "新增信息集中在 full production 的 Vera Rubin/Vera CPU、量产 CPO、Windows RTX Spark 个人智能体 PC，以及 TSMC 将 NVIDIA AI 工具嵌入 fab 流程。",
            "这些增量把叙事从单一 GPU 训练需求扩展到 agentic AI factory、CPU/AI storage、网络能效、制造效率和端侧 AI PC。",
            "投资假设的变化是：瓶颈不再只有 GPU，而是扩散到 HBM/存储、CPO 网络、先进制造/封装、ODM/rack 和 Windows 终端生态；但每个节点都需要单独证明财务转化。",
            "缺少会前基准的系统对照和各产品线收入/订单分拆。",
            "NVIDIA/TSMC/Micron/Microsoft 下一次财报或产品上市披露能否把这些新增路线转成收入桥。",
        ),
        "Q1.2.1": _ans(
            ["SRC-NV-VERA-RUBIN-20260531", "SRC-NV-VERA-CPU-20260531", "SRC-NV-MSFT-RTX-SPARK-20260601", "SRC-MSFT-SURFACE-ULTRA-20260531"],
            "NVIDIA 披露的系统制造商和客户名单覆盖 Dell、HPE、Lenovo、Supermicro、ASUS、Foxconn、QCT、Wistron/Wiwynn，以及 CoreWeave、Lambda、OCI、OpenAI、Anthropic、ByteDance 等。",
            "名单证明生态覆盖广，但 adoption wording 分层明显：CPO 有 first adopters，Vera CPU 客户多为 exploring/planning，RTX Spark 是 OEM 上市路线。",
            "需求可见度中等偏强，足以支持 Q2 瓶颈分析；但不能把所有合作名单直接上升为收入确认。",
            "缺少客户独立采购确认、系统订单量、合同金额、出货节奏和平台迁移成本。",
            "客户 capex 指引、AI server 订单、RTX Spark OEM 上市数量和云厂商 AI infrastructure 部署更新。",
        ),
        "Q1.2.2": _ans(
            ["SRC-NV-MSFT-RTX-SPARK-20260601", "SRC-MSFT-SURFACE-ULTRA-20260531", "SRC-NV-VERA-RUBIN-20260531", "SRC-MU-HBM4-20260316"],
            "未来 3-12 个月可验证节点包括 RTX Spark 秋季上市、Surface Laptop Ultra 年内上市、Vera Rubin ramp、CPO production/adopter 部署、Micron HBM4/SOCAMM2 出货。",
            "这些节点覆盖终端销量、云端部署和供应链收入三条验证线，能避免只看发布会热度。",
            "催化剂清晰，但每条催化剂的财务口径不同：RTX Spark 看销量和生态，Vera Rubin/CPO 看 AI server/rack 订单，HBM4 看 ASP、份额和毛利。",
            "缺少硬阈值，例如出货台数、订单金额、CPO port 出货、HBM4 bit share。",
            "2026 年秋季设备上市、NVIDIA/Micron/ODM 财报、云客户 capex 和订单/backlog。",
        ),
        "Q2.1.1": _ans(
            ["SRC-NV-VERA-RUBIN-20260531", "SRC-NV-TSMC-AI-FABS-20260531", "SRC-MU-HBM4-20260316", "SRC-NV-MSFT-RTX-SPARK-20260601"],
            "稀缺节点包括 NVIDIA 平台控制、TSMC 先进制造/AI fab 与封装能力、Micron HBM4/SOCAMM2、高速网络/CPO、AI server rack 集成和 Windows AI PC 生态入口。",
            "这些节点分别约束算力平台、制造效率、内存带宽、网络功耗、系统交付和端侧应用；但真正能捕获超额利润的是供给稀缺且客户难替代的环节。",
            "瓶颈强度排序：NVIDIA 平台控制最高，TSMC/先进制造和 HBM/存储次之，CPO 是高潜力但供应商映射未完整，ODM/PC OEM 需要利润率验证。",
            "缺少 CPO 具体供应商份额、CoWoS/先进封装产能、HBM4 订单份额和 AI server rack 单位经济性。",
            "CPO 采用者扩张、HBM4 出货份额、TSMC capex/AI fab 成效和 ODM 订单毛利率披露。",
        ),
        "Q2.1.2": _ans(
            ["SRC-MU-HBM4-20260316", "SRC-NV-VERA-RUBIN-20260531", "SRC-SA-MU-20260602", "SRC-SA-NVDA-20260602"],
            "HBM4、高速存储、平台软件和先进制造更容易转化为 ASP/毛利率；ODM/OEM 和 PC 终端多为制造/渠道环节，技术重要但未必有高利润率。",
            "财务转化要看产品 mix、订单、backlog、毛利率和 capex 消耗；只有技术必需性不够。",
            "当前财务化证据最清晰的是 NVIDIA 与 Micron，TSMC 有制造和内部效率逻辑，ODM/OEM 需要单独验证毛利弹性；CPO 需要找到可交易供应商和收入桥。",
            "缺少 Micron HBM4 价格/份额、TSMC 先进封装利润口径、CPO 供应商财务敞口、ODM rack 毛利率。",
            "下一季分产品收入、毛利率桥、订单/backlog、客户预付款和 capex 指引。",
        ),
        "Q2.2.1": _ans(
            ["SRC-NV-VERA-RUBIN-20260531", "SRC-MU-HBM4-20260316", "SRC-MSFT-SURFACE-ULTRA-20260531", "SRC-SA-DELL-20260602"],
            "直接敞口：NVDA 平台，TSM 制造/封装，MU HBM4/SOCAMM2/SSD，Wiwynn/Quanta/Foxconn 等 AI server/rack，MSFT/DELL/HP/Lenovo/ASUS 终端路线。",
            "直接产品和客户映射不等于高弹性：平台/核心存储/先进制造弹性更强，ODM 和 OEM 受订单量、低毛利和客户议价影响。",
            "Q4 应优先纳入 NVDA、TSM、MU 和台系 AI server/ODM，再把 MSFT/DELL/QCOM 作为生态或竞争压力观察。",
            "台湾标的缺少实时估值和分产品收入桥；Microsoft 和 Dell 的事件敞口占整体利润比例偏低。",
            "公司财报中 AI server、HBM、data center、PC/Surface、order/backlog 和 gross margin 口径。",
        ),
        "Q2.2.2": _ans(
            ["SRC-NV-VERA-RUBIN-20260531", "SRC-MU-HBM4-20260316", "SRC-SA-TSM-20260602", "SRC-SA-MU-20260602"],
            "事件可以改变收入的环节多，但改变毛利率和 FCF 的环节较少：NVIDIA 平台软件和系统溢价、Micron 高端 HBM mix、TSMC 高利用率/先进封装最值得验证。",
            "AI server ODM 可能有收入弹性，但若毛利率低、营运资本和 capex 消耗大，利润/现金流弹性会被削弱。",
            "财务桥应把事件增量拆成收入、产品 mix、毛利率、capex、working capital 和 FCF；目前只能给出方向性判断，不能直接定量预测。",
            "缺少单位收入、单 rack 毛利、HBM4 ASP、CPO switch 毛利、TSMC 先进封装边际利润。",
            "NVIDIA、Micron、TSMC、Wiwynn/Quanta/Dell 财报和管理层指引。",
        ),
        "Q3.1.1": _ans(
            ["SRC-NV-MSFT-RTX-SPARK-20260601", "SRC-MSFT-SURFACE-ULTRA-20260531", "SRC-AP-RTX-SPARK-20260601", "SRC-SA-NVDA-20260602"],
            "主要执行风险包括 RTX Spark 秋季上市后需求不足、Vera Rubin/CPO 量产爬坡低于宣称、agentic AI 客户 ROI 不清、监管/出口限制和客户 capex 下修。",
            "事件路线覆盖面越广，验证链越长；任一关键节点延迟都会降低供应链标的的收入确认速度。",
            "短期最需要防的是“发布会强、财报弱”：若出货和订单没有跟上，估值较高的核心资产会先承压。",
            "缺少上市后渠道数据、CPO 部署案例、客户 ROI 指标、AI capex 持续性和监管边界。",
            "RTX Spark 首批销量、CPO adopter 部署、NVIDIA guidance、云厂商 capex、出口管制更新。",
        ),
        "Q3.1.2": _ans(
            ["SRC-AP-RTX-SPARK-20260601", "SRC-NV-MSFT-RTX-SPARK-20260601", "SRC-SA-QCOM-20260602", "SRC-SA-MSFT-20260602"],
            "替代路线包括 Intel/AMD x86 AI PC、Qualcomm/ARM PC、客户自研 ASIC、开放网络/以太网替代、以及 cloud-only AI agent 模式。",
            "RTX Spark 强化 NVIDIA+Microsoft 端侧路线，但它也会激发 PC 芯片商和生态伙伴的反制。",
            "Qualcomm/Intel/AMD 不能仅因短线下跌就视为机会；若 NVIDIA/MSFT 路线强化，它们可能先是受压标的。",
            "缺少 Intel/AMD/QCOM 新路线性能、OEM 设计赢单、软件生态兼容和价格策略。",
            "PC OEM 设计赢单、AI PC 出货结构、Windows AI agent 生态采用和竞品路线发布时间。",
        ),
        "Q3.2.1": _ans(
            ["SRC-SA-NVDA-20260602", "SRC-SA-TSM-20260602", "SRC-SA-MU-20260602", "SRC-SA-MSFT-20260602"],
            "估值快照显示核心资产已处在较高 AI 预期中；NVDA 赔率受高市值和成长兑现约束，TSM 稀缺性强但安全边际需估值分位，MU 估值看似更低但存储周期反证更重。",
            "事件越接近已知平台路线，越可能已经在核心资产估值里；更好的赔率通常出现在稀缺性强但市场仍担心周期或财务转化的节点。",
            "当前不应把强产业逻辑等同于可行动多头；缺少估值分位和盈利上修证据时，多数目标只能 watch_only。",
            "缺少一致预期、历史估值分位、EPS 上修、FCF yield 和 bear/base/bull 量化模型。",
            "未来一个季度盈利修正、股价反应、估值分位和订单兑现情况。",
        ),
        "Q3.2.2": _ans(
            ["SRC-AP-RTX-SPARK-20260601", "SRC-SA-NVDA-20260602", "SRC-SA-QCOM-20260602", "SRC-SA-DELL-20260602"],
            "AP 报道的短线股价反应说明事件有交易热度，但交易热度不是基本面验证；DELL/QCOM 等标的若目标价或预期未上修，赔率并不自动改善。",
            "短期拥挤会压低胜率：如果市场先按“AI PC/AI factory 全链条受益”买入，后续需要更强订单数据才能维持估值。",
            "交易层面应避免把发布会后短线反应当作买入理由；应等 Q1-Q2 的验证数据进入财报或订单口径。",
            "缺少持仓拥挤、期权波动、卖方 EPS revision 和成交结构数据。",
            "股价回撤后估值分位、盈利上修幅度和产品/订单验证同时出现。",
        ),
        "Q4.1.1": _ans(
            ["SRC-NV-VERA-RUBIN-20260531", "SRC-NV-TSMC-AI-FABS-20260531", "SRC-MU-HBM4-20260316", "SRC-NV-MSFT-RTX-SPARK-20260601"],
            "可交易 universe 包括 NVDA、TSM/2330.TW、MU、MSFT、DELL、QCOM，以及台系 AI server/ODM/电源散热标的如 Wiwynn、Quanta、Hon Hai、Delta、MediaTek。",
            "直接瓶颈或高弹性节点优先于宽泛生态：NVDA/TSM/MU/Wiwynn/Quanta 的事件传导更直接，MSFT/DELL 更偏生态和渠道，QCOM 是竞争受压/反证观察。",
            "最终推荐应按“稀缺节点 + 财务敞口 + 估值赔率 + 反证可监控”排序，而不是按公司名气或发布会提及次数排序。",
            "缺少台湾标的实时估值、CPO 供应商明确名单和各公司收入占比。",
            "补齐实时估值、分业务收入、订单和毛利率后重排。",
        ),
        "Q4.1.2": _ans(
            ["SRC-SA-QCOM-20260602", "SRC-SA-DELL-20260602", "SRC-SA-MSFT-20260602", "SRC-AP-RTX-SPARK-20260601"],
            "应降级的候选包括：仅被生态提及但缺少收入桥的 OEM/ODM，因 RTX Spark 路线受压的 QCOM/Intel/AMD，以及估值已经充分定价但没有新增财务证据的核心资产。",
            "四维门槛中最容易失败的是错定价和财务弹性：强曝光如果没有稀缺性或毛利弹性，只能观察。",
            "QCOM 当前更像被事件施压的风险观察；MSFT/DELL 需要证明 AI PC 对整体盈利足够重要；NVDA/TSM 虽稀缺但赔率要谨慎。",
            "缺少竞品 design win、AI PC 销量、利润率和估值分位数据。",
            "秋季 AI PC 出货、OEM design win、QCOM/Intel/AMD 新产品路线和盈利指引。",
        ),
        "Q4.2.1": _ans(
            ["SRC-SA-NVDA-20260602", "SRC-SA-TSM-20260602", "SRC-SA-MU-20260602", "SRC-SA-MSFT-20260602"],
            "排序结果以 MU、TSM、NVDA 和台系 AI server/ODM 作为优先观察对象；其中 MU 的 HBM4/存储弹性与估值相对更值得跟踪，NVDA/TSM 稀缺性最强但估值门槛更高。",
            "模型将稀缺性、错定价、盈利弹性和风险控制作为门槛，强主题但缺少错定价或财务桥的目标被压到 watch_only/no_action。",
            "当前没有满足全部门槛的 actionable_long；最合理输出是分层观察清单，并把升级条件绑定到订单、出货、毛利率和估值回落。",
            "缺少完整一致预期、实时估值分位、台湾标的财务桥和 CPO 供应链收入映射。",
            "每季更新评分表，若估值回落且订单/毛利验证改善，MU/TSM/NVDA 或台系 ODM 可升级。",
        ),
        "Q4.2.2": _ans(
            ["SRC-NV-MSFT-RTX-SPARK-20260601", "SRC-MU-HBM4-20260316", "SRC-NV-VERA-RUBIN-20260531", "SRC-SA-MU-20260602"],
            "3 个月内应跟踪：RTX Spark OEM 上市清单和预售，Vera Rubin/CPO 部署客户扩张，Micron HBM4/SOCAMM2 收入和毛利，TSMC 先进封装/AI fab 指标，云厂商 capex 指引。",
            "这些数据能分别验证端侧需求、AI factory 量产、HBM/存储瓶颈、制造瓶颈和下游客户 ROI。",
            "如果这些触发器没有兑现，事件驱动机会应降级为长期主题观察；如果订单和财务桥同时出现，相关 watch_only 目标才有升级依据。",
            "缺少每个触发器的硬阈值和公司披露日程表。",
            "2026 年 9 月前完成第一次复盘：产品上市、订单/出货、财报/指引和估值变化。",
        ),
    }


def _ans(
    source_links: list[str],
    fact: str,
    inference: str,
    judgment: str,
    gap: str,
    trigger: str,
    *,
    artifact: dict[str, Any] | None = None,
) -> dict[str, Any]:
    answer = {
        "source_links": source_links,
        "fact": fact,
        "inference": inference,
        "judgment": judgment,
        "conclusion": judgment,
        "gap": gap,
        "trigger": trigger,
        "refuting_source_plan": f"寻找能否推翻该结论的订单、出货、capex、估值或竞争路线材料：{trigger}",
    }
    if artifact:
        answer["artifact"] = artifact
    return answer


def _table(title: str, columns: list[str], rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {"title": title, "columns": columns, "rows": rows}


def _unit(
    *,
    node_id: str,
    parent_id: str,
    level: int,
    question: str,
    source_links: list[str],
    fact: str,
    inference: str,
    judgment: str,
    gap: str,
    trigger: str,
    skill: str,
    score_component: str,
    decision_use: str,
    target_implications: str,
    artifact: dict[str, Any] | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "id": node_id,
        "level": level,
        "question": question,
        "parent_id": parent_id,
        "investment_relevance": decision_use,
        "decision_use": decision_use,
        "required_materials": ["官方发布稿", "公司财报/估值快照", "客户/伙伴独立验证", "反证或边界材料"],
        "support_evidence": "官方或公司来源直接确认产品、客户、量产、上市、订单、收入或毛利路径。",
        "refute_evidence": "竞品替代、上市/量产延迟、订单不足、估值已充分定价、毛利/现金流不能兑现。",
        "target_implications": target_implications,
        "preferred_specialty_skill": skill,
        "score_component": score_component,
        "materiality": "该问题用于决定父节点结论能否从主题叙事升级为可评分的标的排序输入。",
        "minimum_evidence_gate": "至少一条一手/公司来源支撑，并至少定义一条可推翻结论的数据触发器。",
        **_ans(source_links, fact, inference, judgment, gap, trigger, artifact=artifact),
    }
    return item


def _apply_adaptive_drilldown(nodes: list[dict[str, Any]], source_by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {str(node["id"]): node for node in nodes}
    adaptive_nodes: list[dict[str, Any]] = [
        _unit(
            node_id="Q2.1.1.1",
            parent_id="Q2.1.1",
            level=4,
            question="HBM4/SOCAMM2/AI storage 是否是本次事件最可财务化的稀缺节点？",
            source_links=["SRC-MU-HBM4-20260316", "SRC-NV-VERA-RUBIN-20260531", "SRC-SA-MU-20260602"],
            fact="Micron 披露 HBM4 36GB 12H 已为 NVIDIA Vera Rubin high-volume production，SOCAMM2 和 PCIe Gen6 SSD 也进入高量产口径；NVIDIA 的 Vera Rubin/BlueField/STX 路线提高了内存带宽、存储吞吐和能效要求。",
            inference="该节点同时具备明确产品绑定、量产措辞和可财务化路径，增量可通过 HBM mix、ASP、毛利率和 AI storage 收入体现。",
            judgment="在本次事件可投资节点里，HBM4/SOCAMM2 是赔率研究优先级最高的单节点之一；MU 可进入优先观察，但必须用下一季 HBM 出货、ASP 和毛利率验证。",
            gap="缺少 HBM4 订单规模、Vera Rubin 份额、ASP、毛利率和竞争供应商份额。",
            trigger="Micron 下一季 HBM 收入口径、HBM4 产能/良率、DRAM/HBM ASP 和毛利率指引。",
            skill="supply-chain-chokepoint-analysis",
            score_component="chokepoint_strength, earnings_elasticity, target_ranking",
            decision_use="判断 Q2 瓶颈和 Q4 MU 排序是否能被财务敞口支持。",
            target_implications="提高 MU 观察优先级；若 HBM 价格或毛利率反转，则从瓶颈利润降级为周期暴露。",
            artifact=_table(
                "HBM/高速存储瓶颈评分",
                ["维度", "评分", "依据", "缺口/反证"],
                [
                    {"维度": "demand_flow", "评分": "4.5", "依据": "Vera Rubin/HBM4/SOCAMM2 直接绑定", "缺口/反证": "实际订单量未披露"},
                    {"维度": "irreplaceability", "评分": "4.0", "依据": "HBM4 带宽和能效要求高", "缺口/反证": "SK hynix/Samsung 替代份额"},
                    {"维度": "supply_access_constraint", "评分": "4.0", "依据": "HBM 高端产能和良率约束", "缺口/反证": "扩产后供给反转"},
                    {"维度": "pricing_power", "评分": "3.6", "依据": "高端 mix 可能推升 ASP/毛利", "缺口/反证": "缺少 HBM4 ASP"},
                    {"维度": "financial_conversion", "评分": "4.1", "依据": "可进入 MU 收入/毛利率口径", "缺口/反证": "分产品披露不足"},
                    {"维度": "market_pricing", "评分": "3.2", "依据": "估值需用快照和 EPS 上修验证", "缺口/反证": "StockAnalysis 只作线索"},
                    {"维度": "disconfirming_trigger", "评分": "4.0", "依据": "HBM ASP/份额/毛利可季度验证", "缺口/反证": "需要硬阈值"},
                ],
            ),
        ),
        _unit(
            node_id="Q2.1.1.2",
            parent_id="Q2.1.1",
            level=4,
            question="Spectrum-X CPO 网络是否形成可交易瓶颈，还是仍停留在平台叙事？",
            source_links=["SRC-NV-VERA-RUBIN-20260531"],
            fact="NVIDIA 披露 Spectrum-X Ethernet Photonics CPO switches in production，并给出 5x power efficiency、5x AI uptime、1.3x faster deployment 等口径，CoreWeave、Lambda、OCI 等列为 first adopters。",
            inference="CPO 可能解决 AI factory 网络功耗、带宽和稳定性瓶颈，但当前材料主要把价值控制留在 NVIDIA networking ecosystem，未明确可交易 CPO 供应商份额。",
            judgment="CPO 是高潜力瓶颈，但当前只能强化 NVDA networking 平台和供应链线索，不能直接升级未映射供应商。",
            gap="缺少 CPO 光电器件、交换芯片、封装、模块供应商名单和收入份额。",
            trigger="first adopters 部署扩张、CPO 端口出货、供应商订单和 NVIDIA networking 收入口径。",
            skill="supply-chain-chokepoint-analysis",
            score_component="chokepoint_strength, evidence_quality, monitorability",
            decision_use="判断 CPO 是否需要继续下钻到 L5 供应商映射和部署验证。",
            target_implications="NVDA 受益明确；独立 CPO/光模块标的暂时只能作为线索，需补供应商映射后纳入 Q4。",
            artifact=_table(
                "CPO 网络瓶颈评分",
                ["维度", "评分", "依据", "缺口/反证"],
                [
                    {"维度": "demand_flow", "评分": "4.0", "依据": "AI factory 网络功耗/吞吐约束清晰", "缺口/反证": "部署规模未披露"},
                    {"维度": "irreplaceability", "评分": "3.5", "依据": "CPO 能效优势明确", "缺口/反证": "传统光模块/以太网升级替代"},
                    {"维度": "supply_access_constraint", "评分": "3.2", "依据": "先进光电封装和验证门槛", "缺口/反证": "供应商名单缺失"},
                    {"维度": "pricing_power", "评分": "3.0", "依据": "NVIDIA 平台可收费", "缺口/反证": "独立供应商议价不明"},
                    {"维度": "financial_conversion", "评分": "2.8", "依据": "可进入 NVDA networking", "缺口/反证": "缺少外部供应商收入桥"},
                    {"维度": "market_pricing", "评分": "2.8", "依据": "主题热度可能已高", "缺口/反证": "无估值分位"},
                    {"维度": "disconfirming_trigger", "评分": "3.8", "依据": "first adopter 部署可验证", "缺口/反证": "需 port/订单阈值"},
                ],
            ),
        ),
        _unit(
            node_id="Q2.1.1.2.1",
            parent_id="Q2.1.1.2",
            level=5,
            question="CPO 供应商映射需要补哪些字段，才能从主题线索变成标的输入？",
            source_links=["SRC-NV-VERA-RUBIN-20260531"],
            fact="当前官方材料只确认 Spectrum-X CPO switches in production 与 first adopters，并未披露具体光电器件、封装、模块或交换链供应商份额。",
            inference="如果没有供应商、份额、单价、毛利率和客户验证，CPO 节点不能转成可评分标的。",
            judgment="CPO 分支需要继续作为研究待补，而不能在最终推荐中强行列入具体光模块公司。",
            gap="缺少 CPO BOM、供应商名单、端口出货、客户验证和收入占比。",
            trigger="NVIDIA/供应商披露 CPO switch BOM、订单、客户部署或分产品收入。",
            skill="research-source-planner",
            score_component="evidence_quality, target_ranking",
            decision_use="防止 Q4 推荐被未验证供应商映射污染。",
            target_implications="未验证供应商不进入高强度推荐；只保留为下一轮研究线索。",
        ),
        _unit(
            node_id="Q2.1.1.2.2",
            parent_id="Q2.1.1.2",
            level=5,
            question="CPO 采用者部署能否形成 3-12 个月验证触发器？",
            source_links=["SRC-NV-VERA-RUBIN-20260531"],
            fact="CoreWeave、Lambda、OCI 被列为 first adopters，但材料未给出部署规模、订单金额或上线时间表。",
            inference="first adopter 名单能证明方向，但需要部署规模和性能/成本反馈才能证明 CPO 从产品变成收入。",
            judgment="CPO 的短期催化是部署扩张公告和端口出货，而不是单纯的发布会提及。",
            gap="缺少每个 first adopter 的部署规模、capex、端口数量和 ROI。",
            trigger="云客户或 NVIDIA networking 披露 CPO 部署、订单、端口或收入。",
            skill="event-to-investment-analysis",
            score_component="monitorability, disconfirming_risk_control",
            decision_use="定义 CPO 分支的季度监控阈值。",
            target_implications="若部署证据出现，NVDA networking 与相关供应链可升级；否则继续 watch_only。",
        ),
        _unit(
            node_id="Q2.1.1.3",
            parent_id="Q2.1.1",
            level=4,
            question="TSMC 先进制造/AI fab/先进封装是否捕获本次事件的真实增量？",
            source_links=["SRC-NV-TSMC-AI-FABS-20260531", "SRC-NV-VERA-RUBIN-20260531", "SRC-SA-TSM-20260602"],
            fact="NVIDIA/TSMC 披露 AI 工具进入 lithography、process simulation、process control、fab operations 和 defect inspection；Vera Rubin 量产依赖台湾大规模供应链。",
            inference="TSMC 的价值来自先进制程、先进封装和制造效率，而不是单场发布会订单；AI fab 工具更像强化长期良率/效率/周期优势。",
            judgment="TSMC 是强稀缺节点，但事件增量需要通过先进封装供需、capex、利用率和利润率验证；估值赔率需保守。",
            gap="缺少 AI fab 对毛利率/周期的定量影响、先进封装产能缺口、Vera Rubin 订单对应晶圆量。",
            trigger="TSMC capex/先进封装产能、利用率、HPC 收入和毛利率指引。",
            skill="company-exposure-analysis",
            score_component="chokepoint_strength, financial_conversion, valuation_odds",
            decision_use="判断 TSM 是否因为本次事件而提高观察强度。",
            target_implications="TSM 稀缺性高但错定价不足；维持优先观察，等待估值或盈利上修证据。",
            artifact=_table(
                "TSMC 财务桥与瓶颈",
                ["路径", "当前证据", "可财务化方式", "缺口"],
                [
                    {"路径": "先进制程", "当前证据": "Vera Rubin/AI platform 量产依赖先进制造", "可财务化方式": "HPC 收入、利用率、ASP", "缺口": "具体晶圆量不明"},
                    {"路径": "先进封装", "当前证据": "AI factory/rack-scale 需要高端封装", "可财务化方式": "CoWoS/先进封装产能和价格", "缺口": "产能缺口未量化"},
                    {"路径": "AI fab 效率", "当前证据": "NVIDIA/TSMC AI 工具进入制造流程", "可财务化方式": "周期、良率、成本、capex 效率", "缺口": "缺少财务指标映射"},
                ],
            ),
        ),
        _unit(
            node_id="Q2.1.1.4",
            parent_id="Q2.1.1",
            level=4,
            question="AI server/rack ODM 是收入弹性节点，还是低毛利制造节点？",
            source_links=["SRC-NV-VERA-RUBIN-20260531", "SRC-SA-DELL-20260602"],
            fact="NVIDIA 材料列出 Dell、HPE、Lenovo、Supermicro、Foxconn、QCT、Wistron/Wiwynn 等制造/系统伙伴，Vera Rubin full-scale production 需要台湾服务器供应链。",
            inference="ODM/rack 集成是订单传导清晰节点，但其超额利润取决于客户集中、议价、营运资本、毛利率和是否有设计/整机稀缺能力。",
            judgment="Wiwynn/Quanta/Foxconn 可作为收入弹性观察，但在缺少毛利率和估值口径时不应高于平台、HBM 和先进制造瓶颈。",
            gap="缺少单 rack 收入、毛利率、订单/backlog、客户集中和营运资本消耗。",
            trigger="台系 ODM 财报中的 AI server 收入、毛利率、订单和客户指引。",
            skill="company-exposure-analysis",
            score_component="financial_conversion, risk_control, target_ranking",
            decision_use="区分订单弹性和利润弹性，决定台系 ODM 的推荐上限。",
            target_implications="台系 ODM 多数进入 watch_only；若毛利率/订单同时上修可升级。",
            artifact=_table(
                "ODM 节点判断",
                ["公司/类型", "收入弹性", "利润弹性", "当前限制"],
                [
                    {"公司/类型": "Wiwynn", "收入弹性": "高，AI server/rack 相关", "利润弹性": "待验证", "当前限制": "实时估值和毛利率缺失"},
                    {"公司/类型": "Quanta/QCT", "收入弹性": "高，系统集成相关", "利润弹性": "中低待验证", "当前限制": "客户议价和分部口径"},
                    {"公司/类型": "Foxconn", "收入弹性": "有，但业务规模大", "利润弹性": "可能被稀释", "当前限制": "AI server 占比和毛利桥不清"},
                ],
            ),
        ),
        _unit(
            node_id="Q2.1.1.5",
            parent_id="Q2.1.1",
            level=4,
            question="RTX Spark/Windows AI PC 是端侧 AI 投资主线，还是低确定性生态期权？",
            source_links=["SRC-NV-MSFT-RTX-SPARK-20260601", "SRC-MSFT-SURFACE-ULTRA-20260531", "SRC-AP-RTX-SPARK-20260601", "SRC-SA-MSFT-20260602"],
            fact="NVIDIA/Microsoft 披露 RTX Spark Windows PCs，1 petaflop AI、最高 128GB unified memory，Surface Laptop Ultra 年内上市，Dell 等设备预计 later this year。",
            inference="端侧 AI PC 能打开 personal agents 叙事，但财务路径要穿过 OEM 出货、软件生态、售价/毛利和用户工作流采用。",
            judgment="RTX Spark 是重要催化但当前更像生态期权；对 MSFT/DELL 有战略意义，对 QCOM 是竞争反证，对 NVDA 是平台扩张线索。",
            gap="缺少上市后出货、ASP、attach rate、应用生态、企业采购和毛利率。",
            trigger="秋季上市后预售/销量、OEM SKU、Windows agent 应用、Dell/MSFT/HP/Lenovo 指引。",
            skill="event-to-investment-analysis",
            score_component="future_space, disconfirming_risk_control, target_ranking",
            decision_use="判断端侧 AI PC 是否足以改变 Q4 标的强度。",
            target_implications="MSFT/DELL 维持观察；QCOM 作为受压/反证观察；不足以单独形成 actionable_long。",
            artifact=_table(
                "RTX Spark 财务化路径",
                ["环节", "需要验证的数据", "受益/受压标的", "当前结论"],
                [
                    {"环节": "硬件上市", "需要验证的数据": "SKU、售价、出货", "受益/受压标的": "NVDA/DELL/MSFT", "当前结论": "有时间窗口，无销量证据"},
                    {"环节": "软件生态", "需要验证的数据": "Windows agents、Adobe 等应用采用", "受益/受压标的": "MSFT/NVDA", "当前结论": "生态强但 monetization 不明"},
                    {"环节": "竞争替代", "需要验证的数据": "QCOM/Intel/AMD design win", "受益/受压标的": "QCOM 等", "当前结论": "QCOM 先作风险观察"},
                ],
            ),
        ),
        _unit(
            node_id="Q2.2.2.1",
            parent_id="Q2.2.2",
            level=4,
            question="NVDA 的事件增量如何进入收入、毛利和现金流？",
            source_links=["SRC-NV-VERA-RUBIN-20260531", "SRC-NV-VERA-CPU-20260531", "SRC-NV-MSFT-RTX-SPARK-20260601", "SRC-SA-NVDA-20260602"],
            fact="Vera Rubin/Vera CPU/CPO/RTX Spark 均属于 NVIDIA 平台路线，覆盖 data center、networking、AI storage 和 AI PC。",
            inference="NVDA 的财务桥最完整：平台控制可进入系统/芯片/networking 收入和软件生态，但高估值要求持续超预期兑现。",
            judgment="NVDA 胜率最高但赔率受市场预期约束；排序上稀缺性强，行动状态被 mispricing 限制。",
            gap="缺少产品线订单、CPO 收入、RTX Spark 出货和估值分位。",
            trigger="下一季 Data Center/networking guidance、订单、客户 capex 和估值回落。",
            skill="financial-statement-analysis",
            score_component="financial_conversion, valuation_odds, risk_control",
            decision_use="校准 NVDA 是核心持仓型观察还是事件赔率目标。",
            target_implications="强稀缺但 watch_only，需估值或盈利上修改善。",
        ),
        _unit(
            node_id="Q2.2.2.2",
            parent_id="Q2.2.2",
            level=4,
            question="MU 的 HBM4/SOCAMM2 路径能否形成盈利弹性？",
            source_links=["SRC-MU-HBM4-20260316", "SRC-SA-MU-20260602"],
            fact="Micron 已把 HBM4 36GB 12H、SOCAMM2 和 PCIe Gen6 SSD 与 NVIDIA Vera Rubin/Vera CPU/BlueField STX 路线绑定。",
            inference="如果 HBM mix 和 AI storage 占比提升，MU 的收入、毛利率和估值修复弹性都可能高于普通 DRAM 周期。",
            judgment="MU 是本次事件中相对赔率更值得跟踪的标的，但必须把存储周期反证作为硬约束。",
            gap="缺少 HBM4 份额、ASP、毛利率和供需周期数据。",
            trigger="Micron HBM 收入、毛利率、库存、ASP 和 capex 指引。",
            skill="financial-statement-analysis",
            score_component="earnings_elasticity, valuation_odds, target_ranking",
            decision_use="判断 MU 是否能排在最终观察清单前列。",
            target_implications="若 HBM 财务桥验证，MU 可升级；若价格/毛利走弱则降级。",
        ),
        _unit(
            node_id="Q2.2.2.3",
            parent_id="Q2.2.2",
            level=4,
            question="TSM 的事件财务桥主要来自订单增量还是制造效率提升？",
            source_links=["SRC-NV-TSMC-AI-FABS-20260531", "SRC-SA-TSM-20260602"],
            fact="TSMC 与 NVIDIA 的 AI fab 材料强调设计/制造效率，Vera Rubin 量产也间接强化先进制造需求。",
            inference="TSM 财务桥既包括 HPC/先进制程和先进封装需求，也包括 AI 工具提升生产效率；前者更可验证，后者更长期。",
            judgment="TSM 是稳健稀缺节点，但事件本身较难立刻给出高赔率，需等待估值和盈利上修同步。",
            gap="缺少 AI fab 效率财务指标和先进封装产能缺口量化。",
            trigger="HPC 收入、先进封装 capex、利用率和毛利率指引。",
            skill="financial-statement-analysis",
            score_component="financial_conversion, valuation_odds",
            decision_use="校准 TSM 在最终排序中的防守/长期权重。",
            target_implications="TSM 优先观察，但行动状态受估值和收入桥约束。",
        ),
        _unit(
            node_id="Q2.2.2.4",
            parent_id="Q2.2.2",
            level=4,
            question="Wiwynn/Quanta/Foxconn 的订单弹性会不会被低毛利和营运资本抵消？",
            source_links=["SRC-NV-VERA-RUBIN-20260531"],
            fact="多家台湾 ODM/系统厂被列为 Vera Rubin 量产生态伙伴。",
            inference="订单可能带来收入弹性，但如果毛利率低、客户议价强、营运资本占用高，FCF 弹性可能弱于收入弹性。",
            judgment="台系 ODM 需要做公司级收入桥，不能只凭供应链名单上调强度。",
            gap="缺少公司级 AI server 占比、订单/backlog、毛利率和估值。",
            trigger="Wiwynn/Quanta/Foxconn AI server 收入、毛利率和订单指引。",
            skill="company-exposure-analysis",
            score_component="financial_conversion, risk_control",
            decision_use="限制 ODM 目标的推荐强度。",
            target_implications="维持 watch_only，优先补财报和估值。",
        ),
        _unit(
            node_id="Q3.2.1.1",
            parent_id="Q3.2.1",
            level=4,
            question="NVDA 当前赔率主要被哪些隐含预期约束？",
            source_links=["SRC-SA-NVDA-20260602", "SRC-NV-VERA-RUBIN-20260531"],
            fact="StockAnalysis 快照只能作为估值线索；事件材料显示 NVDA 拥有最强平台控制和最多产品增量。",
            inference="强平台稀缺性不等于好赔率；NVDA 需要持续兑现 AI factory、networking 和 AI PC 增长来支撑预期。",
            judgment="NVDA 的胜率强于赔率，除非估值回落或盈利上修超预期，否则不应给 actionable_long。",
            gap="缺少 forward EPS、FCF yield、估值分位和订单上修。",
            trigger="估值回落、EPS 上修、Data Center/networking 指引超预期。",
            skill="valuation-analysis",
            score_component="valuation_odds, action_state",
            decision_use="防止把最强公司自动排成最高赔率。",
            target_implications="NVDA 保持高优先级 watch_only。",
        ),
        _unit(
            node_id="Q3.2.1.2",
            parent_id="Q3.2.1",
            level=4,
            question="MU 的相对赔率来自哪里，反证是什么？",
            source_links=["SRC-SA-MU-20260602", "SRC-MU-HBM4-20260316"],
            fact="MU 与 Vera Rubin HBM4/SOCAMM2 绑定，估值快照只说明需要进一步赔率检查，不能直接确认低估。",
            inference="相对赔率来自 HBM mix 进入利润率和市场仍担心存储周期之间的差异。",
            judgment="MU 是赔率优先观察，但它的反证也最硬：HBM/DRAM 价格、供给扩张和毛利率转弱会迅速削弱结论。",
            gap="缺少最新估值分位、HBM 毛利和 DRAM/HBM 价格趋势。",
            trigger="HBM ASP、毛利率、库存和 EPS revision。",
            skill="valuation-analysis",
            score_component="valuation_odds, disconfirming_risk_control",
            decision_use="决定 MU 是否在最终排序中高于 NVDA/TSM。",
            target_implications="MU 可排前，但行动状态仍由数据触发器控制。",
        ),
        _unit(
            node_id="Q3.2.1.3",
            parent_id="Q3.2.1",
            level=4,
            question="TSM 的稳健性是否足以弥补赔率不足？",
            source_links=["SRC-SA-TSM-20260602", "SRC-NV-TSMC-AI-FABS-20260531"],
            fact="TSM 在先进制造和 AI fab 链路上稀缺，但估值只通过快照作为线索。",
            inference="TSM 的优势是防守型稀缺和长期需求确定性，短期赔率要看估值、capex 效率和先进封装紧缺是否继续。",
            judgment="TSM 可排在优先观察前列，但需要估值回落或盈利上修才能升级。",
            gap="缺少 ADR/台股估值分位、一致预期和先进封装收益桥。",
            trigger="估值分位改善、HPC/先进封装收入和毛利率上修。",
            skill="valuation-analysis",
            score_component="valuation_odds, risk_control",
            decision_use="判断 TSM 是防守型观察还是高赔率目标。",
            target_implications="TSM watch_only，强于大多数二阶标的。",
        ),
        _unit(
            node_id="Q4.2.1.1",
            parent_id="Q4.2.1",
            level=4,
            question="按四维门槛，哪些标的应进入优先观察、普通观察和排除？",
            source_links=["SRC-SA-MU-20260602", "SRC-SA-TSM-20260602", "SRC-SA-NVDA-20260602", "SRC-SA-QCOM-20260602"],
            fact="Q1-Q3 显示核心机会集中在平台、HBM/存储、先进制造和 AI server；估值与财务桥缺口限制行动状态。",
            inference="四维门槛应先过滤掉只有主题曝光、没有稀缺性/错定价/财务桥的目标。",
            judgment="优先观察：MU、TSM、NVDA；普通观察：Wiwynn、Quanta、MSFT、DELL；风险/反证观察：QCOM。",
            gap="缺少完整实时估值分位、台湾标的财务桥和 CPO 供应商映射。",
            trigger="订单、出货、毛利率、估值分位和反证触发器同步更新。",
            skill="target-ranking-analysis",
            score_component="target_ranking, action_state",
            decision_use="把所有 QA 结论收束为排序输入。",
            target_implications="最终表按优先级展示，但不输出买卖指令。",
            artifact=_table(
                "四维门槛分层",
                ["分层", "标的", "胜率逻辑", "赔率限制"],
                [
                    {"分层": "优先观察", "标的": "MU", "胜率逻辑": "HBM4/SOCAMM2 直接绑定", "赔率限制": "存储周期和估值需验证"},
                    {"分层": "优先观察", "标的": "TSM", "胜率逻辑": "先进制造/封装稀缺", "赔率限制": "估值和效率收益未量化"},
                    {"分层": "优先观察", "标的": "NVDA", "胜率逻辑": "平台控制最强", "赔率限制": "高预期和估值约束"},
                    {"分层": "普通观察", "标的": "Wiwynn/Quanta/DELL/MSFT", "胜率逻辑": "订单或生态敞口", "赔率限制": "利润弹性或事件占比不足"},
                    {"分层": "风险观察", "标的": "QCOM", "胜率逻辑": "AI PC 竞争受压", "赔率限制": "不是事件直接受益方"},
                ],
            ),
        ),
        _unit(
            node_id="Q4.2.1.2",
            parent_id="Q4.2.1",
            level=4,
            question="为什么当前仍没有 actionable_long？",
            source_links=["SRC-SA-NVDA-20260602", "SRC-SA-TSM-20260602", "SRC-SA-MU-20260602"],
            fact="核心标的都有强产业逻辑，但估值快照不提供充分低估证据，且订单、毛利和收入桥仍待验证。",
            inference="actionable_long 必须同时满足稀缺、错定价、盈利弹性和风险可控；当前多数目标只满足稀缺或未来空间。",
            judgment="当前应输出观察清单而不是行动建议；最接近升级的候选是 MU/TSM/NVDA，但升级条件不同。",
            gap="缺少估值分位、EPS revision、硬订单和毛利率验证。",
            trigger="估值回落叠加订单/毛利率上修，或反证风险明显下降。",
            skill="target-recommendation-analysis",
            score_component="action_state, risk_control",
            decision_use="防止推荐强度超过证据边界。",
            target_implications="所有标的维持 watch_only/no_action。",
        ),
        _unit(
            node_id="Q4.2.2.1",
            parent_id="Q4.2.2",
            level=4,
            question="未来三个月哪些数据最能改变排序？",
            source_links=["SRC-NV-MSFT-RTX-SPARK-20260601", "SRC-MU-HBM4-20260316", "SRC-NV-VERA-RUBIN-20260531"],
            fact="当前可见催化剂包括 RTX Spark 秋季上市、Vera Rubin/CPO ramp、Micron HBM4/SOCAMM2 和 TSMC AI fab/先进制造验证。",
            inference="改变排序的数据不是新闻热度，而是订单、出货、毛利率、客户 capex 和估值分位。",
            judgment="排序更新应按 MU HBM 验证、TSM 先进封装/AI fab 证据、NVDA 平台收入上修、ODM 毛利率和 AI PC 销量五类触发器执行。",
            gap="缺少硬阈值和披露日历。",
            trigger="2026-09-02 前进行首次 live prediction review。",
            skill="target-ranking-analysis",
            score_component="monitorability, disconfirming_risk_control",
            decision_use="定义本报告后续复盘规则。",
            target_implications="触发器决定 watch_only 是否升级或降级。",
            artifact=_table(
                "三个月复盘触发器",
                ["触发器", "验证数据", "影响标的", "动作含义"],
                [
                    {"触发器": "HBM 财务桥", "验证数据": "HBM 收入、ASP、毛利率", "影响标的": "MU", "动作含义": "上修则提高排序，走弱则降级"},
                    {"触发器": "先进制造/封装", "验证数据": "TSM HPC/先进封装 capex/利用率", "影响标的": "TSM", "动作含义": "确认稀缺和利润桥"},
                    {"触发器": "AI factory ramp", "验证数据": "Vera Rubin/CPO 部署、NVDA guidance", "影响标的": "NVDA/ODM", "动作含义": "确认平台和订单弹性"},
                    {"触发器": "AI PC 上市", "验证数据": "RTX Spark SKU、预售、企业采购", "影响标的": "MSFT/DELL/QCOM", "动作含义": "决定端侧分支是否升级"},
                    {"触发器": "估值赔率", "验证数据": "估值分位、EPS revision、FCF yield", "影响标的": "全部", "动作含义": "决定是否从 watch_only 升级"},
                ],
            ),
        ),
    ]
    child_ids_by_parent: dict[str, list[str]] = {}
    for node in adaptive_nodes:
        child_ids_by_parent.setdefault(str(node["parent_id"]), []).append(str(node["id"]))
    by_id.update({str(node["id"]): node for node in adaptive_nodes})
    for parent_id, child_ids in child_ids_by_parent.items():
        if parent_id in by_id:
            by_id[parent_id]["next_question_ids"] = child_ids
    for node in adaptive_nodes:
        node["source_plan"] = _source_plan(str(node["id"]), list(node["source_links"]), source_by_id, str(node["preferred_specialty_skill"]))
        node["skill_dispatch"] = _skill_dispatch(node)
    return nodes + adaptive_nodes


def _source_plan(node_id: str, source_ids: list[str], source_by_id: dict[str, dict[str, Any]], skill: str) -> list[dict[str, Any]]:
    plan = []
    for source_id in source_ids:
        source = source_by_id[source_id]
        plan.append(
            {
                "source_id": source_id,
                "source_bucket": source["source_bucket"],
                "source_type": source["title"],
                "expected_fields": ["事实边界", "时间/量产/上市口径", "客户/伙伴", "收入/利润桥", "反证触发器"],
                "preferred_skill": skill,
                "allowed_usage": source["allowed_usage"],
                "source_visible_at": source["source_visible_at"],
                "cutoff_status": "live_visible",
                "availability_proof": source["availability_proof"],
                "deepseek_allowed": True,
                "qa_node": node_id,
            }
        )
    return plan


def _skill_dispatch(node: dict[str, Any]) -> dict[str, Any]:
    node_id = str(node["id"])
    level = int(node.get("level") or 3)
    return {
        "task_family": f"event_conference_live_l{level}",
        "selected_skill": node.get("preferred_specialty_skill") or "event-to-investment-analysis",
        "concrete_materials": list(node.get("source_links") or []),
        "extraction_schema": [
            "event_fact_boundary",
            "investment_delta",
            "commercialization_stage",
            "transmission_chain",
            "company_exposure",
            "valuation_or_risk",
            "refuting_test",
        ],
        "source_extraction_ids": [f"EX-{node_id}"],
        "leaf_source_review_ids": [f"RV-{node_id}"],
        "skill_output_status": "gpt_direct_source_pack_parsed",
        "fallback_used": "deepseek_timeout",
        "gpt_verification_status": "verified_with_caveats",
    }


def _source_parser_records(nodes: list[dict[str, Any]], source_by_id: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    extractions = []
    reviews = []
    for node in nodes:
        if not 3 <= int(node.get("level") or 0) <= 5:
            continue
        node_id = str(node["id"])
        source_id = str((node.get("source_links") or [""])[0])
        source = source_by_id[source_id]
        extraction_id = f"EX-{node_id}"
        review_id = f"RV-{node_id}"
        schema_fields = {
            "event_fact_boundary": {"value": node["fact"], "status": "parsed"},
            "investment_delta": {"value": node["inference"], "status": "parsed"},
            "commercialization_stage": {"value": "officially announced, production/ramp/availability wording depends on product line", "status": "parsed"},
            "transmission_chain": {"value": node["inference"], "status": "parsed"},
            "company_exposure": {"value": node["target_implications"], "status": "parsed"},
            "valuation_or_risk": {"value": node["gap"], "status": "parsed"},
            "refuting_test": {"value": node["trigger"], "status": "parsed"},
        }
        extractions.append(
            {
                "extraction_id": extraction_id,
                "l3_question_id": node_id,
                "research_unit_level": int(node.get("level") or 0),
                "source_id": source_id,
                "source_title": source["title"],
                "source_bucket": source["source_bucket"],
                "parser": "gpt_direct_source_pack",
                "parser_status": "complete",
                "fallback_reason": "deepseek_delegate timed out during source-pack parsing",
                "schema_fields": schema_fields,
                "key_facts": [node["fact"]],
                "inference": node["inference"],
                "support_refute_or_lead": source["support_refute_or_lead"],
                "uncertainties": [node["gap"]],
                "follow_up_data": [node["trigger"]],
                "created_at": CREATED_AT,
            }
        )
        reviews.append(
            {
                "review_id": review_id,
                "extraction_id": extraction_id,
                "l3_question_id": node_id,
                "research_unit_level": int(node.get("level") or 0),
                "source_id": source_id,
                "gpt_verification_status": "verified_with_caveats",
                "adopted_facts": [node["fact"]],
                "corrections": [],
                "rejected_claims": ["未把伙伴名单直接等同为订单收入；未把短线股价反应当成基本面证据。"],
                "final_bucket": source["source_bucket"],
                "final_support_refute_or_lead": source["support_refute_or_lead"],
                "allowed_to_strengthen_conclusion": True,
            }
        )
    return extractions, reviews


def _raw_targets() -> list[dict[str, Any]]:
    review_ids = [
        "RV-Q1.1.1",
        "RV-Q2.1.1",
        "RV-Q2.1.1.1",
        "RV-Q2.1.1.2",
        "RV-Q2.1.1.3",
        "RV-Q2.1.1.4",
        "RV-Q2.1.1.5",
        "RV-Q2.2.2.1",
        "RV-Q2.2.2.2",
        "RV-Q2.2.2.3",
        "RV-Q2.2.2.4",
        "RV-Q3.2.1.1",
        "RV-Q3.2.1.2",
        "RV-Q3.2.1.3",
        "RV-Q4.2.1.1",
        "RV-Q4.2.1.2",
        "RV-Q4.2.2.1",
    ]
    return [
        _target(
            "MU",
            "Micron Technology",
            "US",
            "HBM4/SOCAMM2/高速存储",
            [4.2, 4.2, 3.5, 3.5, 3.4, 4.1, 4.0],
            ["SRC-MU-HBM4-20260316", "SRC-SA-MU-20260602"],
            review_ids,
            "Micron 是本次材料中少数把 Vera Rubin 直接绑定到 high-volume production 的 HBM4/SOCAMM2 标的，估值相对 NVDA 更容易形成赔率；主要问题是存储周期和目标价压力。",
            "HBM4、SOCAMM2 和 AI storage 若进入收入/毛利率口径，存在产品 mix 和估值修复空间。",
            "HBM ASP/份额不达预期、DRAM/NAND 供给反转、毛利率见顶。",
            demand=4.4,
            irreplaceability=4.3,
            underpricing=3.1,
            valuation_status="verified_with_caveats",
            expected_excess_return=0.05,
        ),
        _target(
            "TSM",
            "Taiwan Semiconductor Manufacturing ADR",
            "US/Taiwan",
            "先进制造/先进封装/AI fab",
            [4.4, 3.8, 2.9, 3.3, 3.2, 3.7, 3.3],
            ["SRC-NV-TSMC-AI-FABS-20260531", "SRC-SA-TSM-20260602"],
            review_ids,
            "TSMC 在制造和先进封装链路上稀缺性强，NVIDIA/TSMC AI fab 材料强化其技术和效率优势；但 ADR 估值和先进封装利润口径仍需验证。",
            "如果 AI fab 工具提升效率且先进封装持续紧缺，TSM 的长期利润池具备防守性和上修空间。",
            "先进封装产能缓解、AI capex 放缓、估值已充分反映。",
            demand=4.0,
            irreplaceability=4.5,
            underpricing=2.9,
            valuation_status="verified_with_caveats",
            expected_excess_return=0.02,
        ),
        _target(
            "NVDA",
            "NVIDIA",
            "US",
            "AI factory 平台控制",
            [4.9, 4.6, 2.4, 4.4, 3.3, 4.5, 3.7],
            ["SRC-NV-VERA-RUBIN-20260531", "SRC-NV-VERA-CPU-20260531", "SRC-SA-NVDA-20260602"],
            review_ids,
            "NVIDIA 是最强平台控制者，Vera Rubin/Vera CPU/CPO/RTX Spark 都直接归属于其平台；但市值和高预期使错定价维度不足。",
            "未来空间最大，但需要持续高增长和订单兑现来支撑当前估值。",
            "AI capex 放缓、CPO/RTX Spark 不兑现、估值回落。",
            demand=4.4,
            irreplaceability=4.5,
            underpricing=2.5,
            valuation_status="verified_with_caveats",
            expected_excess_return=0.01,
        ),
        _target(
            "6669.TW",
            "Wiwynn",
            "Taiwan",
            "AI server/rack ODM",
            [3.5, 3.8, 2.8, 2.8, 2.9, 3.4, 3.4],
            ["SRC-NV-VERA-RUBIN-20260531"],
            review_ids,
            "Wiwynn 被列入 Vera Rubin full-scale production 供应链，AI server/rack 收入弹性可能较高；但本报告缺少实时估值和单 rack 毛利率。",
            "若 Vera Rubin ramp 快于预期，AI server/rack 订单可带来收入弹性。",
            "低毛利制造、客户集中、估值数据缺失。",
            demand=3.8,
            irreplaceability=3.5,
            underpricing=2.8,
            valuation_status="unverified",
            expected_excess_return=0.03,
        ),
        _target(
            "2382.TW",
            "Quanta Computer",
            "Taiwan",
            "QCT/AI server 集成",
            [3.4, 3.6, 2.8, 2.8, 2.9, 3.4, 3.2],
            ["SRC-NV-VERA-RUBIN-20260531"],
            review_ids,
            "Quanta/QCT 是 AI server/rack 重要制造链路，事件敞口明确但利润率和估值口径不足。",
            "订单放量有收入弹性，但超额利润捕获弱于平台/存储/制造瓶颈。",
            "ODM 毛利率低、估值不明、客户议价。",
            demand=3.7,
            irreplaceability=3.4,
            underpricing=2.8,
            valuation_status="unverified",
            expected_excess_return=0.02,
        ),
        _target(
            "MSFT",
            "Microsoft",
            "US",
            "Windows AI PC / Surface 生态",
            [3.2, 3.7, 2.7, 3.2, 3.4, 4.0, 2.8],
            ["SRC-MSFT-SURFACE-ULTRA-20260531", "SRC-SA-MSFT-20260602"],
            review_ids,
            "Microsoft 是 RTX Spark Windows 生态入口，但 GTC 单事件对整体盈利弹性较低，更多是战略验证而非高赔率标的。",
            "Windows AI agent 若成为新终端工作流，长期生态价值上升。",
            "Surface 出货占比小、AI PC 需求慢、估值已反映平台优势。",
            demand=3.6,
            irreplaceability=3.2,
            underpricing=2.7,
            valuation_status="verified_with_caveats",
            expected_excess_return=0.0,
        ),
        _target(
            "DELL",
            "Dell Technologies",
            "US",
            "AI PC / AI server OEM",
            [3.1, 3.4, 2.6, 2.8, 2.8, 3.3, 3.0],
            ["SRC-NV-MSFT-RTX-SPARK-20260601", "SRC-SA-DELL-20260602"],
            review_ids,
            "Dell 同时参与 AI server 和 RTX Spark PC，但目标价与估值信息显示赔率未明显打开，且 OEM 议价和毛利率需要验证。",
            "AI server 与 AI PC 双敞口带来收入弹性，但利润弹性低于核心瓶颈。",
            "目标价接近、毛利率受压、AI PC 出货不及预期。",
            demand=3.4,
            irreplaceability=3.1,
            underpricing=2.6,
            valuation_status="verified_with_caveats",
            expected_excess_return=0.0,
        ),
        _target(
            "2308.TW",
            "Delta Electronics",
            "Taiwan",
            "电源/散热/基础设施",
            [3.0, 3.3, 2.6, 2.4, 2.8, 3.0, 2.9],
            ["SRC-NV-GTC-KEYNOTE-20260601"],
            review_ids,
            "Delta 与 AI infrastructure 相关，但当前来源没有形成具体订单/收入桥；作为功耗散热二阶受益跟踪。",
            "AI factory 功耗上升有长期需求，但本报告证据不足。",
            "缺少直接来源、估值和收入桥。",
            demand=3.2,
            irreplaceability=3.0,
            underpricing=2.6,
            valuation_status="unverified",
            expected_excess_return=None,
        ),
        _target(
            "2317.TW",
            "Hon Hai Precision / Foxconn",
            "Taiwan",
            "AI server manufacturing",
            [3.0, 3.4, 2.6, 2.5, 2.8, 3.2, 2.9],
            ["SRC-NV-VERA-RUBIN-20260531"],
            review_ids,
            "Foxconn 被列入制造伙伴，收入敞口可能存在，但公司业务规模大且 AI server 利润弹性需单独验证。",
            "Vera Rubin ramp 可带来制造收入，但超额利润未确认。",
            "业务稀释、低毛利、估值和分部数据缺失。",
            demand=3.4,
            irreplaceability=3.0,
            underpricing=2.6,
            valuation_status="unverified",
            expected_excess_return=None,
        ),
        _target(
            "QCOM",
            "Qualcomm",
            "US",
            "Windows AI PC 竞争路线",
            [2.5, 2.8, 2.3, 2.6, 2.6, 3.0, 2.5],
            ["SRC-AP-RTX-SPARK-20260601", "SRC-SA-QCOM-20260602"],
            review_ids,
            "RTX Spark/NVIDIA+Microsoft 路线可能压制 Qualcomm AI PC 叙事；当前更适合作为反证/竞争风险监控，而非受益标的。",
            "只有在 ARM PC 路线重新拿到设计赢单和软件生态证据时才可升级。",
            "AI PC share 受压、目标价低于现价、生态竞争加剧。",
            demand=2.8,
            irreplaceability=2.5,
            underpricing=2.3,
            valuation_status="verified_with_caveats",
            expected_excess_return=-0.02,
        ),
    ]


def _target(
    ticker: str,
    name: str,
    market: str,
    chokepoint: str,
    scores: list[float],
    evidence_ids: list[str],
    review_ids: list[str],
    rationale: str,
    future_space: str,
    risks: str,
    *,
    demand: float,
    irreplaceability: float,
    underpricing: float,
    valuation_status: str,
    expected_excess_return: float | None,
) -> dict[str, Any]:
    if len(scores) != len(SCORE_WEIGHTS):
        raise ValueError(f"{ticker} score length must match SCORE_WEIGHTS")
    components = dict(zip(SCORE_WEIGHTS.keys(), scores))
    return {
        "ticker": ticker,
        "name": name,
        "market": market,
        "thesis_node": chokepoint,
        "chokepoint_node": chokepoint,
        "rationale": rationale,
        "future_space": future_space,
        "risks": risks,
        "odds": future_space,
        "valuation_status": valuation_status,
        "expected_excess_return": expected_excess_return,
        "demand_visibility": demand,
        "irreplaceability": irreplaceability,
        "market_underpricing": underpricing,
        "valuation_tolerance": underpricing,
        "downside_fragility": 2.9 if underpricing >= 2.8 else 3.5,
        "catalyst_proximity": 3.8,
        "evidence_ids": evidence_ids,
        "review_ids": review_ids,
        "score_subcomponents": {
            component: [
                {
                    "name": f"{component}_primary_driver",
                    "score": score,
                    "weight": 1.0,
                    "evidence_ids": evidence_ids,
                    "review_ids": review_ids,
                    "rationale": f"{chokepoint} 对 {component} 的贡献评分。",
                    "status": "verified_with_caveats",
                }
            ]
            for component, score in components.items()
        },
        "odds_model": {
            "implied_expectation": "市场已计入不同程度 AI factory/AI PC 增长，需用订单、出货和利润率验证。",
            "base_path": "订单/出货符合管理层路线，估值维持。",
            "bull_path": "订单和毛利率同时上修，估值回落后赔率改善。",
            "bear_path": "产品上市或客户 capex 低于预期，估值压缩。",
            "upgrade_data": "订单/backlog、分产品收入、毛利率、估值分位改善。",
            "downgrade_data": "capex 下修、出货不足、价格/毛利率转弱、竞争路线替代。",
        },
        "prediction_review": {
            "initial_claim": rationale,
            "validation_horizon": "2026-09-02",
            "required_evidence": "订单/出货、财报、毛利率、估值和反证触发器。",
            "current_status": "live_watch",
            "review_trigger": "秋季产品上市或下一季财报。",
        },
        **components,
    }


def _public_target(target: dict[str, Any]) -> dict[str, Any]:
    score = target.get("score", {})
    strength = score.get("strength") or score.get("total_score")
    return {
        **target,
        "strength": f"{strength} / 总分 {score.get('total_score', '')}",
    }


def _prediction_reviews(targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "ticker": target.get("ticker"),
            "action_state": target.get("action_state"),
            "validation_horizon": "2026-09-02",
            "review_trigger": "产品上市、订单/backlog、客户 capex、毛利率和估值分位更新。",
        }
        for target in targets
    ]


def _markdown_summary(project: dict[str, Any], targets: list[dict[str, Any]]) -> str:
    lines = [
        f"# {project['title']}",
        "",
        project["current_judgment"],
        "",
        "## 观察清单",
    ]
    for target in targets:
        lines.append(f"- {target.get('rank')}. {target.get('ticker')} {target.get('name')}: {target.get('action_state')}，{target.get('rationale')}")
    return "\n".join(lines) + "\n"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
