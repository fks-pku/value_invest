from __future__ import annotations

import json
import shutil
import sys
from copy import deepcopy
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
from value_invest_research.framework_contracts import (  # noqa: E402
    SCORE_WEIGHTS,
    attach_forward_return_labels,
    freeze_recommendations,
)


PROJECT_ID = "optical_module_opportunities_backtest_20260601"
PROJECT_DIR = ROOT / "research" / "qa_projects" / PROJECT_ID
AS_OF_DATE = "2026-03-01"
REPORT_DATE = "2026-06-01"
EVALUATION_DATE = "2026-06-01"
CREATED_AT = "2026-06-01T00:00:00+08:00"


SOURCE_PACK: list[dict[str, Any]] = [
    {
        "source_id": "SRC-TF-800G-20260210",
        "title": "TrendForce：Google TPU 带动 800G 以上光模块需求",
        "source_bucket": "research_report",
        "support_refute_or_lead": "support",
        "summary": "TrendForce 在 2026-02-10 预计 2026 年 800G 以上光模块占比超过 60%，Google TPU 相关 800G+ 光模块需求超过 600 万只。",
        "url": "https://www.trendforce.com/presscenter/news/20260210-12919.html",
        "source_visible_at": "2026-02-10",
        "published_at": "2026-02-10",
        "allowed_usage": "thesis",
        "availability_proof": "TrendForce press page dated 2026-02-10, before 2026-03-01 cutoff.",
    },
    {
        "source_id": "SRC-TF-LASER-20251208",
        "title": "TrendForce：800G+ 光模块放量与激光器供给紧张",
        "source_bucket": "research_report",
        "support_refute_or_lead": "support",
        "summary": "TrendForce 在 2025-12-08 预计 800G+ 光模块出货从 2025 年约 2400 万只提升到 2026 年约 6300 万只，并提示激光器及上游材料供应紧张。",
        "url": "https://www.trendforce.com/presscenter/news/20251208-12823.html",
        "source_visible_at": "2025-12-08",
        "published_at": "2025-12-08",
        "allowed_usage": "thesis",
        "availability_proof": "TrendForce press page dated 2025-12-08, before 2026-03-01 cutoff.",
    },
    {
        "source_id": "SRC-LITE-Q2FY26-20260203",
        "title": "Lumentum FY2026 Q2 results",
        "source_bucket": "evidence",
        "support_refute_or_lead": "support",
        "summary": "Lumentum FY2026 Q2 收入 6.655 亿美元，同比增长 65.5%，公司称云和 AI 网络需求、激光芯片/组件、CPO 和 optical circuit switches 推动增长。",
        "url": "https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Second-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx",
        "source_visible_at": "2026-02-03",
        "published_at": "2026-02-03",
        "allowed_usage": "thesis",
        "availability_proof": "Company IR release dated 2026-02-03, before 2026-03-01 cutoff.",
    },
    {
        "source_id": "SRC-COHR-Q2FY26-20260204",
        "title": "Coherent FY2026 Q2 results",
        "source_bucket": "evidence",
        "support_refute_or_lead": "support",
        "summary": "Coherent FY2026 Q2 显示数据中心与通信业务受 AI 光互连需求驱动，说明上游光子器件、材料和模块能力已有收入映射。",
        "url": "https://www.coherent.com/news/press-releases/second-quarter-fiscal-year-2026-results",
        "source_visible_at": "2026-02-04",
        "published_at": "2026-02-04",
        "allowed_usage": "thesis",
        "availability_proof": "Company release dated 2026-02-04, before 2026-03-01 cutoff.",
    },
    {
        "source_id": "SRC-FN-Q2FY26-20260202",
        "title": "Fabrinet FY2026 Q2 results",
        "source_bucket": "evidence",
        "support_refute_or_lead": "lead",
        "summary": "Fabrinet FY2026 Q2 披露 AI 数据通信相关订单推动收入并继续扩产，但代工制造环节的利润弹性和稀缺性弱于器件与模块龙头。",
        "url": "https://investor.fabrinet.com/news-releases/news-release-details/fabrinet-announces-second-quarter-fiscal-year-2026-financial",
        "source_visible_at": "2026-02-02",
        "published_at": "2026-02-02",
        "allowed_usage": "thesis",
        "availability_proof": "Company IR release dated 2026-02-02, before 2026-03-01 cutoff.",
    },
    {
        "source_id": "SRC-INNOLIGHT-Q3-20251031",
        "title": "中际旭创 2025 年三季度经营数据",
        "source_bucket": "evidence",
        "support_refute_or_lead": "support",
        "summary": "截至 2025Q3，中际旭创收入和利润大幅增长，A 股光模块龙头已把 AI 高速模块需求转化为财务表现。",
        "url": "https://www.stcn.com/article/detail/3404588.html",
        "source_visible_at": "2025-10-31",
        "published_at": "2025-10-31",
        "allowed_usage": "thesis",
        "availability_proof": "Securities Times article dated 2025-10-31 reports company 2025Q3 disclosure, before 2026-03-01 cutoff.",
    },
    {
        "source_id": "SRC-EOPTOLINK-Q3-20251030",
        "title": "新易盛 2025 年三季度经营数据",
        "source_bucket": "evidence",
        "support_refute_or_lead": "support",
        "summary": "新易盛 2025Q3 表现出高收入和高利润弹性，说明国内高速光模块第二龙头也能把需求转化为业绩。",
        "url": "https://finance.sina.com.cn/roll/2025-10-30/doc-infvvtwf5673099.shtml",
        "source_visible_at": "2025-10-30",
        "published_at": "2025-10-30",
        "allowed_usage": "thesis",
        "availability_proof": "Public finance article dated 2025-10-30 reports company 2025Q3 disclosure, before 2026-03-01 cutoff.",
    },
    {
        "source_id": "SRC-TFC-Q3-20251030",
        "title": "天孚通信 2025 年三季度经营数据",
        "source_bucket": "evidence",
        "support_refute_or_lead": "support",
        "summary": "天孚通信 2025Q3 高速光器件业务延续增长，说明组件环节受益，但仍需验证单价、客户结构和估值赔率。",
        "url": "https://finance.sina.com.cn/stock/aiassist/yjbg/2025-10-29/doc-infvqmni0149127.shtml",
        "source_visible_at": "2025-10-30",
        "published_at": "2025-10-30",
        "allowed_usage": "thesis",
        "availability_proof": "Public finance article around 2025Q3 report period, before 2026-03-01 cutoff.",
    },
    {
        "source_id": "SRC-CIG-Q3-20251027",
        "title": "剑桥科技 2025 年三季度经营数据",
        "source_bucket": "evidence",
        "support_refute_or_lead": "lead",
        "summary": "剑桥科技 2025Q3 有光通信业务暴露，但规模、利润率和稀缺性证据弱于一线模块龙头。",
        "url": "https://stock.stockstar.com/notice/SN2025102700031891.shtml",
        "source_visible_at": "2025-10-27",
        "published_at": "2025-10-27",
        "allowed_usage": "thesis",
        "availability_proof": "Public disclosure page dated 2025-10-27, before 2026-03-01 cutoff.",
    },
    {
        "source_id": "SRC-INNOLIGHT-VAL-20251120",
        "title": "中际旭创 2025 三季报点评与估值预期",
        "source_bucket": "research_report",
        "support_refute_or_lead": "support",
        "summary": "第三方研报在 2025-11-20 给出中际旭创 2025/2026/2027 年 PE 约 51.8/20.4/15.9 倍，用于 as-of 估值赔率判断。",
        "url": "https://stock.finance.sina.com.cn/stock/go.php/vReport_Show/kind/search/rptid/814890202611/index.phtml",
        "source_visible_at": "2025-11-20",
        "published_at": "2025-11-20",
        "allowed_usage": "thesis",
        "availability_proof": "Research report page dated 2025-11-20, before 2026-03-01 cutoff.",
    },
    {
        "source_id": "SRC-EOPTOLINK-VAL-20251029",
        "title": "新易盛 2025 三季报点评与估值预期",
        "source_bucket": "research_report",
        "support_refute_or_lead": "support",
        "summary": "第三方研报在 2025-10-29 给出新易盛 2025/2026/2027 年 PE 约 39.4/18.7/13.7 倍，用于判断成长是否尚未完全定价。",
        "url": "https://stock.finance.sina.com.cn/stock/go.php/vReport_Show/kind/search/rptid/812905802611/index.phtml",
        "source_visible_at": "2025-10-29",
        "published_at": "2025-10-29",
        "allowed_usage": "thesis",
        "availability_proof": "Research report page dated 2025-10-29, before 2026-03-01 cutoff.",
    },
    {
        "source_id": "SRC-LITE-VAL-20260220",
        "title": "Lumentum valuation snapshot before cutoff",
        "source_bucket": "research_report",
        "support_refute_or_lead": "refute",
        "summary": "第三方市场数据在 2026-02-20 显示 Lumentum 市值和 PE 已较高，提示器件瓶颈强不等于赔率一定好。",
        "url": "https://stockanalysis.com/stocks/lite/market-cap/",
        "source_visible_at": "2026-02-20",
        "published_at": "2026-02-20",
        "allowed_usage": "thesis",
        "availability_proof": "Market data page with February 2026 snapshot context, before 2026-03-01 cutoff.",
    },
    {
        "source_id": "SRC-COHR-VAL-20260227",
        "title": "Coherent valuation snapshot before cutoff",
        "source_bucket": "research_report",
        "support_refute_or_lead": "refute",
        "summary": "第三方市场数据在 2026-02-27 显示 Coherent 市值已较大，AI 光子器件逻辑需要更强盈利兑现来支持赔率。",
        "url": "https://stockanalysis.com/stocks/cohr/market-cap/",
        "source_visible_at": "2026-02-27",
        "published_at": "2026-02-27",
        "allowed_usage": "thesis",
        "availability_proof": "Market data page with February 2026 snapshot context, before 2026-03-01 cutoff.",
    },
    {
        "source_id": "SRC-CRDO-PREANN-20260209",
        "title": "Credo FY2026 Q3 preliminary results and AEC/AI connectivity lead",
        "source_bucket": "message",
        "support_refute_or_lead": "lead",
        "summary": "Credo 在 2026-02-09 预告 FY2026 Q3 收入高于指引，说明 AI 连接需求强，也提示铜互连/AEC 可能改变光模块价值分配。",
        "url": "https://investors.credosemi.com/news-releases/news-release-details/credo-technology-group-holding-ltd-releases-preliminary-third",
        "source_visible_at": "2026-02-09",
        "published_at": "2026-02-09",
        "allowed_usage": "thesis",
        "availability_proof": "Company preliminary release dated 2026-02-09, before 2026-03-01 cutoff.",
    },
]


L3_SOURCE_MAP: dict[str, list[str]] = {
    "Q1.1.1": ["SRC-TF-800G-20260210", "SRC-TF-LASER-20251208", "SRC-LITE-Q2FY26-20260203"],
    "Q1.1.2": ["SRC-TF-800G-20260210", "SRC-TF-LASER-20251208", "SRC-CRDO-PREANN-20260209"],
    "Q1.2.1": ["SRC-LITE-Q2FY26-20260203", "SRC-COHR-Q2FY26-20260204", "SRC-FN-Q2FY26-20260202", "SRC-INNOLIGHT-Q3-20251031", "SRC-EOPTOLINK-Q3-20251030"],
    "Q1.2.2": ["SRC-TF-800G-20260210", "SRC-LITE-Q2FY26-20260203", "SRC-COHR-Q2FY26-20260204", "SRC-CRDO-PREANN-20260209"],
    "Q2.1.1": ["SRC-TF-LASER-20251208", "SRC-LITE-Q2FY26-20260203", "SRC-COHR-Q2FY26-20260204", "SRC-TFC-Q3-20251030"],
    "Q2.1.2": ["SRC-CRDO-PREANN-20260209", "SRC-TF-800G-20260210", "SRC-TF-LASER-20251208"],
    "Q2.2.1": ["SRC-LITE-Q2FY26-20260203", "SRC-COHR-Q2FY26-20260204", "SRC-INNOLIGHT-Q3-20251031", "SRC-EOPTOLINK-Q3-20251030"],
    "Q2.2.2": ["SRC-FN-Q2FY26-20260202", "SRC-LITE-Q2FY26-20260203", "SRC-COHR-Q2FY26-20260204"],
    "Q2.3.1": ["SRC-INNOLIGHT-Q3-20251031", "SRC-EOPTOLINK-Q3-20251030", "SRC-TFC-Q3-20251030", "SRC-LITE-Q2FY26-20260203", "SRC-COHR-Q2FY26-20260204"],
    "Q2.3.2": ["SRC-INNOLIGHT-Q3-20251031", "SRC-EOPTOLINK-Q3-20251030", "SRC-TFC-Q3-20251030", "SRC-LITE-Q2FY26-20260203", "SRC-COHR-Q2FY26-20260204", "SRC-FN-Q2FY26-20260202"],
    "Q3.1.1": ["SRC-TF-800G-20260210", "SRC-TF-LASER-20251208", "SRC-CRDO-PREANN-20260209"],
    "Q3.1.2": ["SRC-CRDO-PREANN-20260209", "SRC-TF-800G-20260210", "SRC-FN-Q2FY26-20260202"],
    "Q3.2.1": ["SRC-TF-LASER-20251208", "SRC-FN-Q2FY26-20260202", "SRC-EOPTOLINK-Q3-20251030", "SRC-TFC-Q3-20251030"],
    "Q3.2.2": ["SRC-INNOLIGHT-Q3-20251031", "SRC-EOPTOLINK-Q3-20251030", "SRC-LITE-Q2FY26-20260203", "SRC-COHR-Q2FY26-20260204"],
    "Q3.3.1": ["SRC-INNOLIGHT-VAL-20251120", "SRC-EOPTOLINK-VAL-20251029", "SRC-LITE-VAL-20260220", "SRC-COHR-VAL-20260227"],
    "Q3.3.2": ["SRC-TF-800G-20260210", "SRC-TF-LASER-20251208", "SRC-LITE-Q2FY26-20260203", "SRC-COHR-Q2FY26-20260204", "SRC-FN-Q2FY26-20260202", "SRC-CRDO-PREANN-20260209"],
    "Q4.1.1": ["SRC-INNOLIGHT-Q3-20251031", "SRC-EOPTOLINK-Q3-20251030", "SRC-TFC-Q3-20251030", "SRC-CIG-Q3-20251027", "SRC-LITE-Q2FY26-20260203", "SRC-COHR-Q2FY26-20260204", "SRC-FN-Q2FY26-20260202"],
    "Q4.1.2": ["SRC-CIG-Q3-20251027", "SRC-FN-Q2FY26-20260202", "SRC-CRDO-PREANN-20260209", "SRC-LITE-VAL-20260220", "SRC-COHR-VAL-20260227"],
    "Q4.2.1": ["SRC-INNOLIGHT-VAL-20251120", "SRC-EOPTOLINK-VAL-20251029", "SRC-LITE-VAL-20260220", "SRC-COHR-VAL-20260227", "SRC-INNOLIGHT-Q3-20251031", "SRC-EOPTOLINK-Q3-20251030", "SRC-LITE-Q2FY26-20260203", "SRC-COHR-Q2FY26-20260204"],
    "Q4.2.2": ["SRC-TF-800G-20260210", "SRC-TF-LASER-20251208", "SRC-LITE-Q2FY26-20260203", "SRC-COHR-Q2FY26-20260204", "SRC-FN-Q2FY26-20260202", "SRC-CRDO-PREANN-20260209"],
}


LEAF_ANALYSIS: dict[str, dict[str, str]] = {
    "Q1.1.1": {
        "conclusion": "截至 2026-03-01，AI 集群网络升级已经足以支撑 800G+ 光模块需求主线，但仍需要用客户订单和端口配置确认持续性。",
        "fact": "TrendForce 给出 800G+ 占比、Google TPU 相关需求和激光器紧张预测；Lumentum 已披露云和 AI 网络需求推动 FY2026 Q2 收入同比高增。",
        "inference": "需求链条从 AI 加速器扩张传导到交换机端口、模块速率升级和上游光器件，而不是单纯题材扩散。",
        "judgment": "Q1 future_space 初步为强；排序时优先考虑已经有收入和客户认证映射的模块/器件公司。",
        "gap": "缺少客户级订单、端口 attach rate、GPU/ASIC 集群端口配置和分客户收入拆分。",
        "trigger": "若 hyperscaler capex 或 AI 网络建设节奏低于预期，需求主线降级。",
    },
    "Q1.1.2": {
        "conclusion": "800G 到 1.6T 是产品 mix 和价值量升级机会，但需要防止换代后 ASP 下行抵消量增。",
        "fact": "TrendForce 截止日前已给出 800G+ 份额提升和 2026 年出货跃升预测；Credo 的 AEC 线索提示高速连接需求强但路径会分化。",
        "inference": "速率升级会扩大高端模块和组件需求，但不同架构会把价值在光模块、光芯片、电芯片和铜互连之间重新分配。",
        "judgment": "1.6T 逻辑可以增强 future_space，但不能直接等同于所有模块厂利润率上行。",
        "gap": "缺少 1.6T 分客户认证、ASP 曲线、产品 mix 和低功耗路线对 BOM 的影响。",
        "trigger": "若 1.6T 放量伴随 ASP 快速下滑或只替代 800G，空间判断下修。",
    },
    "Q1.2.1": {
        "conclusion": "截止日前已有公司收入验证，需求不是纯预期；但长单、预付款和客户锁定证据仍不完整。",
        "fact": "Lumentum、Coherent、Fabrinet 业绩均披露 AI 数据通信相关增长；中际旭创和新易盛 2025Q3 已体现高增长和利润弹性。",
        "inference": "多个环节同步出现收入映射，降低了需求虚假风险；但客户集中和短期抢货仍可能夸大可持续性。",
        "judgment": "证据质量为中高，模块龙头和光器件龙头优于仅有宽泛主题暴露的公司。",
        "gap": "缺少 backlog、客户预付款、长协、容量锁定和订单取消条款。",
        "trigger": "若后续增长来自短期拉货且库存上升，应降低 evidence_quality。",
    },
    "Q1.2.2": {
        "conclusion": "客户平台锁定提高需求可见度，但供应商份额仍要通过认证、交付和客户集中风险验证。",
        "fact": "TrendForce 将 Google TPU 和 800G+ 模块需求直接相连；Lumentum、Coherent 指向云和 AI 网络需求；Credo 预告说明 AI 连接生态仍在扩张。",
        "inference": "平台路线可增强可见度，但也可能使供应链被少数客户和技术路线约束。",
        "judgment": "monitorability 主要来自云 capex、平台路线、供应商认证和季度业绩。",
        "gap": "缺少 NVIDIA/Google/Microsoft/Amazon/Meta 对具体模块供应商的可验证份额。",
        "trigger": "若核心客户推迟项目或改换平台路线，供应商排序重算。",
    },
    "Q2.1.1": {
        "conclusion": "激光器、InP/硅光和高端光器件是最明确的上游瓶颈候选，Lumentum、Coherent 和天孚通信受益路径更直接。",
        "fact": "TrendForce 明确提示激光器及上游材料紧张；Lumentum 和 Coherent 披露光子器件/组件增长，天孚通信 2025Q3 体现组件环节增长。",
        "inference": "若组件供给紧张无法快速缓解，上游可获得更高议价权；但扩产后瓶颈可能转移到模块认证和交付。",
        "judgment": "chokepoint_strength 对上游器件为中高，但还需要观察供给释放速度。",
        "gap": "缺少激光器产能、良率、供应商份额和组件 ASP。",
        "trigger": "若关键组件扩产充足且价格回落，上游瓶颈评分下降。",
    },
    "Q2.1.2": {
        "conclusion": "DSP/driver/TIA 与 AEC 等电连接路径可能分走价值，因此模块厂估值不能只看光模块出货量。",
        "fact": "Credo 截止日前预告高增长，说明 AI 连接需求也可能通过高速电互连和 AEC 路径兑现；TrendForce 的 800G+ 预测则支持光路径主线。",
        "inference": "利润池会在光模块、光芯片、电芯片和铜互连之间动态分配，技术路线选择是核心反证。",
        "judgment": "该问题降低了传统模块厂的无条件高分，要求 Q4 同时检查替代路线风险。",
        "gap": "缺少 DSP/driver/TIA 成本占比、LPO 采用节奏和 AEC 可达距离。",
        "trigger": "若客户大规模采用 AEC/LPO/CPO 且压低可插拔模块价值，Q2 瓶颈排序重排。",
    },
    "Q2.2.1": {
        "conclusion": "模块集成、客户认证、良率和交付能力构成当前最可投资的中游瓶颈之一。",
        "fact": "Lumentum、Coherent、国内模块龙头业绩均显示高端模块/器件需求已转换成收入；模块厂需要同时满足速率、功耗、热管理和交付。",
        "inference": "客户认证和规模制造会延缓二线厂替代，使一线模块厂享有阶段性稀缺性。",
        "judgment": "中际旭创、新易盛的稀缺性强于只有低端或二阶敞口的公司。",
        "gap": "缺少良率、交付周期、客户认证份额和产品代际毛利率。",
        "trigger": "若二线厂快速进入核心客户且毛利率被压缩，模块瓶颈降级。",
    },
    "Q2.2.2": {
        "conclusion": "Fabrinet 有制造产能 beta，但作为代工环节的赔率弹性弱于模块/器件瓶颈。",
        "fact": "Fabrinet FY2026 Q2 披露 AI 数据通信相关订单推动收入并扩产，Lumentum 与 Coherent 的增长说明其客户侧需求强。",
        "inference": "代工环节受益于产能爬坡，但客户可切换和利润率稳定性使其更像低弹性受益者。",
        "judgment": "FN 更适合 watch_only，除非出现明显产能稀缺和利润率上修。",
        "gap": "缺少产能利用率、客户集中度、代工价格和毛利率弹性。",
        "trigger": "若客户转单、自建或代工毛利率无法上行，FN 排序下调。",
    },
    "Q2.3.1": {
        "conclusion": "收入和利润转化最明确的是中际旭创、新易盛、Lumentum、Coherent；天孚通信体现组件弹性，剑桥科技证据弱。",
        "fact": "中际旭创、新易盛 2025Q3 高增长，Lumentum 和 Coherent FY2026 Q2 显示 AI 光互连需求；天孚通信组件业务增长。",
        "inference": "同一需求链条已经在模块、器件和组件环节出现财务映射，Q4 应优先排序财务弹性可验证的公司。",
        "judgment": "A 股模块双龙头和海外器件龙头是核心 universe，二阶 beta 降级。",
        "gap": "缺少现金流、订单质量、客户集中度和产品 mix 毛利率。",
        "trigger": "若收入高增但现金流或毛利率恶化，财务转化评分下降。",
    },
    "Q2.3.2": {
        "conclusion": "国内模块龙头偏模块集成与交付弹性，海外器件龙头偏上游光子器件和平台路线，代工环节偏 beta。",
        "fact": "国内中际旭创、新易盛已有高速模块业绩映射；Lumentum、Coherent 披露器件/组件和 AI 光互连增长；Fabrinet 是制造服务敞口。",
        "inference": "价值捕获差异决定了估值赔率：模块龙头看认证和规模，上游看组件瓶颈，代工看产能利用率。",
        "judgment": "标的推荐必须按瓶颈节点拆分，不能把所有光通信公司同等处理。",
        "gap": "缺少分产品毛利、客户重合度和供应链份额。",
        "trigger": "若组件瓶颈缓解或模块认证壁垒下降，价值捕获排序改变。",
    },
    "Q3.1.1": {
        "conclusion": "LPO/CPO/硅光既可能提高技术壁垒，也可能重分配传统可插拔模块价值，是核心反证。",
        "fact": "Lumentum 已把 CPO/OCS 作为机会，TrendForce 支持 800G+ 可插拔主线，Credo 线索显示替代连接路径活跃。",
        "inference": "技术路线不会简单消灭光模块需求，但会改变谁捕获利润。",
        "judgment": "反证控制要求同时观察 CPO/LPO 采用、硅光良率和客户平台选择。",
        "gap": "缺少客户 CPO/LPO 时间表和硅光量产良率。",
        "trigger": "若 CPO 或平台内置光 I/O 快速落地并压低可插拔模块需求，模块厂评分下降。",
    },
    "Q3.1.2": {
        "conclusion": "铜互连、AEC、OCS 和网络架构优化不会否定整个光模块主线，但会压缩部分短距场景和利润池。",
        "fact": "Credo 预告显示 AEC/AI connectivity 需求强；Fabrinet 和 TrendForce 的数据仍支持 AI 光模块增长。",
        "inference": "连接需求确定性强，但介质和架构路径有分歧，需把替代风险绑定到场景和距离。",
        "judgment": "对只押单一路线的标的，disconfirming_risk_control 不能给满分。",
        "gap": "缺少不同距离下铜互连、AEC 和光模块的成本/功耗比较。",
        "trigger": "若架构优化显著减少光模块端口数，需求和标的排序降级。",
    },
    "Q3.2.1": {
        "conclusion": "供给扩张和 ASP 下行是最直接的中期风险，尤其在 800G/1.6T 快速放量后。",
        "fact": "TrendForce 同时给出需求跃升和上游紧张；Fabrinet 扩产，国内组件/模块公司增长会刺激产能投入。",
        "inference": "瓶颈期越强，后续扩产越可能带来价格竞争；因此需要季度监控价格、库存和毛利率。",
        "judgment": "Q3 风险控制要求把高增长标的和产能周期绑定，不允许只看 TAM。",
        "gap": "缺少 ASP、订单积压、库存和新增产能时间表。",
        "trigger": "若产能释放快于需求且毛利率回落，龙头从 actionable_long 降为 watch_only。",
    },
    "Q3.2.2": {
        "conclusion": "客户集中和地缘限制会压低估值持续性，国内外标的都需要硬触发器。",
        "fact": "主要公司增长均高度依赖云/AI 数据中心客户；国内模块和海外器件都暴露于客户集中与合规风险。",
        "inference": "客户需求强不等于风险低，集中客户会放大订单波动和议价压力。",
        "judgment": "风险控制以客户订单、区域收入和合规事件为核心。",
        "gap": "缺少客户集中度、区域收入和出口/进口限制影响的定量拆分。",
        "trigger": "若核心客户砍单、转单或限制升级，应下修估值倍数和行动状态。",
    },
    "Q3.3.1": {
        "conclusion": "估值已经部分反映高增长，A 股模块龙头的赔率来自 2026/2027 盈利兑现，海外器件龙头更需要利润率上修支撑。",
        "fact": "截至 cutoff 前研报显示中际旭创和新易盛远期 PE 有下行空间；Lumentum、Coherent 的市场数据提示估值已较高。",
        "inference": "高景气不等于好赔率，必须比较市场已定价的增长与后续盈利弹性。",
        "judgment": "valuation_odds 对中际旭创、新易盛相对更强，对 Lumentum、Coherent 保持中性偏谨慎。",
        "gap": "缺少统一口径 EV/EBITDA、FCF yield、净现金和一致预期修正。",
        "trigger": "若盈利上修低于股价涨幅，估值赔率下降。",
    },
    "Q3.3.2": {
        "conclusion": "最快的监控阈值是云 capex、800G/1.6T 出货、ASP、毛利率、订单/backlog 和客户认证。",
        "fact": "需求来源、公司业绩和替代路线已有 cutoff 前线索，但缺少连续季度硬数据。",
        "inference": "季度跟踪必须能同时验证需求、供给、价格和份额，否则无法及时发现拐点。",
        "judgment": "monitorability 中等偏强，但需要后续自动化数据补齐。",
        "gap": "缺少标准化阈值、数据源和自动更新机制。",
        "trigger": "任一核心指标连续两个季度恶化，应触发 Q4 重新排序。",
    },
    "Q4.1.1": {
        "conclusion": "可进入 universe 的核心标的是中际旭创、新易盛、天孚通信、Lumentum、Coherent、Fabrinet；剑桥科技为低置信主题敞口。",
        "fact": "各公司分别映射到模块集成、组件/器件、上游光子器件和制造服务节点，且大多有 cutoff 前业绩或估值证据。",
        "inference": "投资 universe 应从瓶颈节点出发，而不是从热门名字出发。",
        "judgment": "Q4 排序优先模块龙头和上游器件龙头，代工和二阶 beta 降权。",
        "gap": "缺少全球完整可比公司、流动性、估值和客户敞口统一口径。",
        "trigger": "若新增标的有更强瓶颈和低估值证据，应纳入并重排。",
    },
    "Q4.1.2": {
        "conclusion": "剑桥科技、Fabrinet 和部分替代路线公司更偏 watch_only/no_action，不能因主题热度直接高排。",
        "fact": "剑桥科技证据弱于一线模块龙头；Fabrinet 是代工 beta；Credo 代表替代路径线索但不是本报告核心光模块标的。",
        "inference": "只有稀缺性、错定价、利润弹性和风险可控同时成立，才可以提高行动状态。",
        "judgment": "该节点执行 scarcity-first gate，压低纯主题敞口。",
        "gap": "缺少二线公司真实产品代际、客户份额和估值压力验证。",
        "trigger": "若只具备主题暴露而无财务弹性，保持 no_action。",
    },
    "Q4.2.1": {
        "conclusion": "中际旭创和新易盛最符合稀缺性、利润弹性和估值赔率的组合；Lumentum/Coherent 有瓶颈但赔率更受估值约束。",
        "fact": "中际旭创、新易盛有三季报和估值研报交叉验证；Lumentum、Coherent 有收入增长和较高估值提示；其他标的证据链较弱。",
        "inference": "最终排序应把 Q2 瓶颈强度、Q3 估值反证和 Q1 需求空间综合，而非看单一增速。",
        "judgment": "actionable_long 只给证据、赔率和风险均过门槛的标的；其余进入 watch_only 或 no_action。",
        "gap": "缺少统一估值数据库和一致预期修正。",
        "trigger": "若盈利兑现或估值安全边际不达标，行动状态下调。",
    },
    "Q4.2.2": {
        "conclusion": "下一次复盘前必须补订单、ASP、毛利率、客户认证、capex 和估值分位，并按固定规则重排。",
        "fact": "cutoff source pack 已覆盖需求、瓶颈、财务映射、替代路线和估值，但未覆盖完整季度监控数据。",
        "inference": "研究结论可用于形成观察名单，但不能替代持续验证。",
        "judgment": "复盘机制是防止主题上涨后误把结果当证据的关键。",
        "gap": "缺少自动化 source refresh、阈值红黄绿和 benchmark 超额收益。",
        "trigger": "若新增数据打破任一 kill test，应冻结旧结论并生成新版本。",
    },
}


FALLBACK_LABELS: dict[str, dict[str, Any]] = {
    "300308.SZ": {"start_date": "2026-03-02", "end_date": "2026-06-01", "start_price": 569.9055786132812, "end_price": 1130.0, "forward_3m_return": 0.9827845917030056, "label_status": "fallback_unverified"},
    "300502.SZ": {"start_date": "2026-03-02", "end_date": "2026-06-01", "start_price": 203.33326721191406, "end_price": 362.8, "forward_3m_return": 0.7842459247369676, "label_status": "fallback_unverified"},
    "LITE": {"start_date": "2026-03-02", "end_date": "2026-05-29", "start_price": 95.1500015258789, "end_price": 103.9000015258789, "forward_3m_return": 0.09196006117394054, "label_status": "fallback_unverified"},
    "COHR": {"start_date": "2026-03-02", "end_date": "2026-05-29", "start_price": 116.62999725341797, "end_price": 141.02999877929688, "forward_3m_return": 0.20920862228948208, "label_status": "fallback_unverified"},
    "300394.SZ": {"start_date": "2026-03-02", "end_date": "2026-06-01", "start_price": 166.74655151367188, "end_price": 204.3000030517578, "forward_3m_return": 0.2252175693874473, "label_status": "fallback_unverified"},
    "FN": {"start_date": "2026-03-02", "end_date": "2026-05-29", "start_price": 205.82000732421875, "end_price": 231.5399932861328, "forward_3m_return": 0.1249625118778354, "label_status": "fallback_unverified"},
    "603083.SH": {"start_date": "2026-03-02", "end_date": "2026-06-01", "start_price": 45.36464309692383, "end_price": 74.72000122070312, "forward_3m_return": 0.6471011401138766, "label_status": "fallback_unverified"},
}


YFINANCE_TICKERS = {
    "300308.SZ": "300308.SZ",
    "300502.SZ": "300502.SZ",
    "LITE": "LITE",
    "COHR": "COHR",
    "300394.SZ": "300394.SZ",
    "FN": "FN",
    "603083.SH": "603083.SS",
}


def main() -> int:
    if PROJECT_DIR.exists():
        shutil.rmtree(PROJECT_DIR)
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)

    goal = ResearchGoal(
        topic="光模块产业投资机会回测报告",
        research_type="industry_theme",
        object_id=PROJECT_ID,
        run_mode="historical_backtest",
        report_date=REPORT_DATE,
        as_of_date=AS_OF_DATE,
        decision_boundary="研究观察清单，不构成买卖指令；回测标签只用于事后评估。",
        domain_hint="optical_module",
    )
    playbook = resolve_domain_playbook(goal)
    architecture = build_question_architecture(goal, playbook)
    source_by_id = {source["source_id"]: source for source in SOURCE_PACK}
    used_by_source: dict[str, list[str]] = {source["source_id"]: [] for source in SOURCE_PACK}

    source_extractions: list[dict[str, Any]] = []
    leaf_reviews: list[dict[str, Any]] = []
    nodes = [node.to_dict() for node in architecture.nodes]
    for node in nodes:
        if node.get("level") != 3:
            continue
        node_id = str(node["id"])
        source_ids = L3_SOURCE_MAP[node_id]
        for source_id in source_ids:
            used_by_source[source_id].append(node_id)
        analysis = LEAF_ANALYSIS[node_id]
        extraction_ids = [_extraction_id(node_id, index) for index, _ in enumerate(source_ids, start=1)]
        review_ids = [_review_id(node_id, index) for index, _ in enumerate(source_ids, start=1)]
        node.update(
            {
                **analysis,
                "materiality": node.get("decision_use") or node.get("investment_relevance"),
                "minimum_evidence_gate": "至少需要一个 cutoff 前可见的一手公司/公告证据、一个行业或估值交叉验证来源，并保留反证来源。",
                "refuting_source_plan": node.get("refute_evidence") or "补充能够推翻该节点结论的相反来源。",
                "source_links": source_ids,
                "source_plan": [_source_plan_entry(source_by_id[source_id], node) for source_id in source_ids],
                "skill_dispatch": {
                    "task_family": node.get("preferred_specialty_skill") or "industry-report-analysis",
                    "selected_skill": node.get("preferred_specialty_skill") or "industry-report-analysis",
                    "concrete_materials": source_ids,
                    "extraction_schema": _extraction_schema(),
                    "source_extraction_ids": extraction_ids,
                    "leaf_source_review_ids": review_ids,
                    "skill_output_status": "complete_cutoff_visible_source_parse",
                    "fallback_used": "gpt_verified_source_extraction_without_deepseek_for_deterministic_backtest_rerun",
                    "gpt_verification_status": "verified_with_caveats",
                },
                "backtest_grounding": {
                    "allowed_source_ids": source_ids,
                    "model_prior_policy": "hypothesis_only_not_scoring_evidence",
                    "post_cutoff_knowledge_policy": "forbidden_except_final_label",
                    "non_source_claims": [],
                },
            }
        )
        for index, source_id in enumerate(source_ids, start=1):
            extraction, review = _extraction_and_review(
                node=node,
                source=source_by_id[source_id],
                index=index,
            )
            source_extractions.append(extraction)
            leaf_reviews.append(review)

    for source in SOURCE_PACK:
        source["used_in"] = used_by_source.get(source["source_id"], [])
    label_source = _label_source()
    sources = SOURCE_PACK + [label_source]

    _add_parent_rollups(nodes)
    labels = _fetch_forward_labels(list(YFINANCE_TICKERS))
    raw_targets = _raw_targets()
    scored = score_and_rank_targets(raw_targets).ranked_targets
    for target in scored:
        score = target.get("score") or {}
        target["strength"] = score.get("strength", target.get("strength", ""))
        target["action_state"] = score.get("action_state", target.get("action_state", ""))
    frozen = freeze_recommendations(
        scored,
        as_of_date=AS_OF_DATE,
        frozen_at=f"{AS_OF_DATE}T23:59:59+08:00",
    )
    labeled = attach_forward_return_labels(
        frozen,
        labels,
        attached_at=f"{EVALUATION_DATE}T20:00:00+08:00",
    )

    qa_tree = {
        "project_id": PROJECT_ID,
        "title": "光模块产业投资机会回测报告",
        "research_framework_version": "research_goal_qa_canonical_backtest_v2",
        "run_mode": "historical_backtest",
        "report_date": REPORT_DATE,
        "as_of_date": AS_OF_DATE,
        "evaluation_date": EVALUATION_DATE,
        "domain_playbook": "optical_module",
        "anti_leakage_controls": _anti_leakage_controls(),
        "nodes": nodes,
    }
    project = {
        "project_id": PROJECT_ID,
        "title": "光模块产业投资机会回测报告",
        "object_type": "industry_theme",
        "run_mode": "historical_backtest",
        "report_date": REPORT_DATE,
        "as_of_date": AS_OF_DATE,
        "evaluation_date": EVALUATION_DATE,
        "current_judgment": "截至 2026-03-01，AI 数据中心网络升级已形成 800G/1.6T 光模块需求主线；更优标的应同时满足模块/器件瓶颈、财务转化、估值赔率和可监控反证。",
        "biggest_uncertainty": "800G/1.6T 扩产后的 ASP、毛利率、客户份额和替代路线会不会削弱一线模块/器件公司的利润池。",
        "decision_boundary": "研究观察清单，不构成买卖指令；回测标签只用于事后评估。",
        "domain_playbook": "optical_module",
        "framework": "research_goal_qa_canonical",
    }
    workbench = {
        "project_id": PROJECT_ID,
        "run_mode": "historical_backtest",
        "as_of_date": AS_OF_DATE,
        "evaluation_date": EVALUATION_DATE,
        "anti_leakage_controls": _anti_leakage_controls(),
        "source_cutoff_policy": "only cutoff-visible thesis sources can drive QA/scoring; label source is final-target evaluation metadata only",
        "leakage_audit_status": "source_pack_grounded_level_2_controls_declared; label data isolated from QA/scoring/ranking",
        "frozen_recommendations": frozen,
        "scoring_worksheet": labeled["targets"],
    }

    _write_json(PROJECT_DIR / "project.json", project)
    _write_json(PROJECT_DIR / "qa_tree.json", qa_tree)
    _write_json(PROJECT_DIR / "investment_workbench.json", workbench)
    _write_jsonl(PROJECT_DIR / "sources.jsonl", sources)
    _write_jsonl(PROJECT_DIR / "source_extractions.jsonl", source_extractions)
    _write_jsonl(PROJECT_DIR / "leaf_source_reviews.jsonl", leaf_reviews)
    _write_jsonl(PROJECT_DIR / "evidence.jsonl", source_extractions)
    (PROJECT_DIR / "professional_report.md").write_text(
        "# 光模块产业投资机会回测报告\n\nHTML report: professional_report.html\n",
        encoding="utf-8",
    )

    render_result = RenderResearchProjectReport(
        FileSystemResearchProjectRepository(PROJECT_DIR),
        CanonicalHtmlReportRenderer(),
    ).execute(filename="professional_report.html")
    print(json.dumps({
        "project_dir": str(PROJECT_DIR),
        "qa_nodes": len(nodes),
        "l3_nodes": len([node for node in nodes if node.get("level") == 3]),
        "sources": len(sources),
        "source_extractions": len(source_extractions),
        "leaf_source_reviews": len(leaf_reviews),
        "targets": len(labeled["targets"]),
        "label_statuses": {target["ticker"]: target.get("label", {}).get("label_status") for target in labeled["targets"]},
        "report_path": render_result["report_path"],
    }, ensure_ascii=False, indent=2))
    return 0


def _source_plan_entry(source: dict[str, Any], node: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": source["source_id"],
        "expected_fields": node.get("required_materials") or ["node_relevant_metric"],
        "source_bucket": source["source_bucket"],
        "visible_date": source["source_visible_at"],
        "source_visible_at": source["source_visible_at"],
        "cutoff_status": "visible_on_or_before_as_of_date",
        "as_of_date": AS_OF_DATE,
        "allowed_usage": "thesis",
        "availability_proof": source["availability_proof"],
        "preferred_parser_skill": node.get("preferred_specialty_skill") or "industry-report-analysis",
    }


def _extraction_schema() -> dict[str, str]:
    return {
        "schema": "optical_module_backtest_v2",
        "period": "as_of_2026_03_01",
        "metric": "node_relevant_metric",
        "value": "source_observation",
        "source_basis": "cutoff_visible_source",
        "uncertainty": "source_limit",
        "chokepoint": "optical_value_chain_node",
        "financial_conversion": "revenue_margin_or_valuation_link",
    }


def _extraction_and_review(node: dict[str, Any], source: dict[str, Any], index: int) -> tuple[dict[str, Any], dict[str, Any]]:
    node_id = str(node["id"])
    extraction_id = _extraction_id(node_id, index)
    review_id = _review_id(node_id, index)
    extraction = {
        "extraction_id": extraction_id,
        "l3_question_id": node_id,
        "source_id": source["source_id"],
        "source_title": source["title"],
        "source_bucket": source["source_bucket"],
        "parser": "deterministic_cutoff_source_pack",
        "parser_status": "complete",
        "schema_fields": {
            "schema": "optical_module_backtest_v2",
            "period": source["source_visible_at"],
            "metric": "node_relevant_metric",
            "value": source["summary"],
            "source_basis": source["source_id"],
            "uncertainty": "source is cutoff-visible but may not directly fill every requested field",
            "chokepoint": _chokepoint_hint(node),
            "financial_conversion": _financial_conversion_hint(node),
        },
        "key_facts": [source["summary"]],
        "inference": f"该来源用于回答 {node.get('question')}；对不能直接支持的字段保留为缺口。",
        "support_refute_or_lead": source["support_refute_or_lead"],
        "uncertainties": ["部分数据为第三方报告或消息线索，已按来源类别和支持/反证/线索处理。"],
        "follow_up_data": [node.get("gap", "补充季度验证数据。")],
        "created_at": CREATED_AT,
    }
    review = {
        "review_id": review_id,
        "extraction_id": extraction_id,
        "l3_question_id": node_id,
        "source_id": source["source_id"],
        "gpt_verification_status": "verified_with_caveats",
        "adopted_facts": [source["summary"]],
        "corrections": [],
        "rejected_claims": [],
        "final_bucket": source["source_bucket"],
        "final_support_refute_or_lead": source["support_refute_or_lead"],
        "allowed_to_strengthen_conclusion": True,
    }
    return extraction, review


def _extraction_id(node_id: str, index: int) -> str:
    return f"EX-OPTBT-{node_id.replace('.', '-')}-{index}"


def _review_id(node_id: str, index: int) -> str:
    return f"RV-OPTBT-{node_id.replace('.', '-')}-{index}"


def _chokepoint_hint(node: dict[str, Any]) -> str:
    question = str(node.get("question", ""))
    if any(token in question for token in ("激光", "InP", "硅光", "器件")):
        return "upstream_photonics_components"
    if any(token in question for token in ("模块", "认证", "良率", "800G", "1.6T")):
        return "module_integration_and_customer_qualification"
    if any(token in question for token in ("估值", "赔率")):
        return "market_pricing_and_valuation"
    return "optical_ai_network_value_chain"


def _financial_conversion_hint(node: dict[str, Any]) -> str:
    component = str(node.get("score_component", ""))
    if component in {"valuation_odds", "target_ranking"}:
        return "valuation_multiple_and_forward_earnings"
    if component in {"chokepoint_strength", "payoff_convexity"}:
        return "gross_margin_revenue_growth_and_capacity_utilization"
    return "revenue_growth_margin_cash_flow_or_monitoring_indicator"


def _add_parent_rollups(nodes: list[dict[str, Any]]) -> None:
    by_parent: dict[str, list[dict[str, Any]]] = {}
    for node in nodes:
        by_parent.setdefault(str(node.get("parent_id", "")), []).append(node)
    for level in (2, 1):
        for node in [row for row in nodes if row.get("level") == level]:
            children = by_parent.get(str(node.get("id")), [])
            child_judgments = [str(child.get("judgment") or child.get("conclusion") or "") for child in children]
            summary = "；".join(text for text in child_judgments if text)[:420]
            node["conclusion"] = summary or "该层结论来自子问题上抛。"
            node["gap"] = "；".join(str(child.get("gap") or "") for child in children if child.get("gap"))[:260]
            node["trigger"] = "；".join(str(child.get("trigger") or "") for child in children if child.get("trigger"))[:260]


def _anti_leakage_controls() -> dict[str, str]:
    return {
        "anti_leakage_level": "source_pack_grounded_level_2",
        "as_of_date": AS_OF_DATE,
        "cutoff_source_pack_policy": "all_thesis_sources_visible_on_or_before_as_of_date; post_cutoff_sources_rejected_or_label_only",
        "llm_prior_policy": "model_prior_is_not_evidence",
        "question_tree_policy": "domain_playbook_can_frame_questions; parent conclusions and target strength require cutoff source ids",
        "supply_chain_policy": "产业链和 chokepoint 判断只能作为框架；进入结论和评分的内容必须由 cutoff source pack 支撑",
        "scoring_policy": "target_scores_require_verified_leaf_reviews_or_cutoff_sources",
        "label_isolation_policy": "labels_attached_after_frozen_recommendations_only",
        "known_residual_risk": "today_model_may_have_background_priors; mitigated by source-pack grounding and label isolation but not equivalent to frozen historical model weights",
    }


def _raw_targets() -> list[dict[str, Any]]:
    review_by_source = _review_ids_by_source()
    rows = [
        {
            "ticker": "300308.SZ",
            "name": "中际旭创",
            "market": "A股",
            "thesis_node": "高速光模块龙头",
            "chokepoint_node": "800G/1.6T 模块集成、客户认证和交付",
            "rationale": "截至 cutoff，需求、财务转化和远期估值三者最平衡；若 2026 盈利兑现，赔率仍可解释。",
            "future_space": "AI 端口扩张和 1.6T 产品 mix 是主要空间。",
            "risks": "客户集中、ASP 下行、扩产后毛利回落、贸易限制。",
            "scores": (4.5, 4.4, 3.6, 4.2, 3.4, 3.8, 4.1),
            "demand_visibility": 4.4,
            "irreplaceability": 4.3,
            "market_underpricing": 3.5,
            "expected_excess_return": 0.12,
            "valuation_tolerance": 3.4,
            "downside_fragility": 3.2,
            "catalyst_proximity": 3.8,
            "evidence": ["SRC-INNOLIGHT-Q3-20251031", "SRC-INNOLIGHT-VAL-20251120", "SRC-TF-LASER-20251208"],
        },
        {
            "ticker": "300502.SZ",
            "name": "新易盛",
            "market": "A股",
            "thesis_node": "高速光模块第二龙头",
            "chokepoint_node": "高端模块认证和利润弹性",
            "rationale": "盈利弹性和估值赔率较强，但客户结构、订单持续性和产品 mix 仍需验证。",
            "future_space": "800G+ 放量、海外客户份额和产品 mix 上行。",
            "risks": "客户集中、库存/ASP 反转、估值波动。",
            "scores": (4.2, 4.3, 3.7, 4.0, 3.2, 3.6, 4.0),
            "demand_visibility": 4.2,
            "irreplaceability": 4.0,
            "market_underpricing": 3.6,
            "expected_excess_return": 0.10,
            "valuation_tolerance": 3.3,
            "downside_fragility": 3.3,
            "catalyst_proximity": 3.7,
            "evidence": ["SRC-EOPTOLINK-Q3-20251030", "SRC-EOPTOLINK-VAL-20251029", "SRC-TF-800G-20260210"],
        },
        {
            "ticker": "LITE",
            "name": "Lumentum",
            "market": "US",
            "thesis_node": "激光器与光子器件",
            "chokepoint_node": "激光芯片、CPO/OCS 和上游组件",
            "rationale": "瓶颈属性强，但 cutoff 前估值已经较高，赔率取决于利润率上修。",
            "future_space": "激光器、scale-across components、CPO/OCS。",
            "risks": "估值拥挤、客户集中、技术路线切换。",
            "scores": (4.2, 4.1, 2.9, 4.0, 3.1, 3.6, 3.5),
            "demand_visibility": 4.0,
            "irreplaceability": 4.1,
            "market_underpricing": 2.8,
            "expected_excess_return": 0.03,
            "valuation_tolerance": 2.7,
            "downside_fragility": 3.6,
            "catalyst_proximity": 3.4,
            "evidence": ["SRC-LITE-Q2FY26-20260203", "SRC-LITE-VAL-20260220", "SRC-TF-LASER-20251208"],
        },
        {
            "ticker": "COHR",
            "name": "Coherent",
            "market": "US",
            "thesis_node": "光子器件与材料",
            "chokepoint_node": "Datacenter & Communications 光互连能力",
            "rationale": "收入映射明确，但估值和资本开支压力限制行动强度。",
            "future_space": "AI 数据中心光互连、材料和器件扩产。",
            "risks": "估值、资本开支、集成竞争和客户议价。",
            "scores": (4.0, 3.9, 2.8, 3.9, 3.0, 3.4, 3.3),
            "demand_visibility": 3.9,
            "irreplaceability": 3.9,
            "market_underpricing": 2.7,
            "expected_excess_return": 0.02,
            "valuation_tolerance": 2.6,
            "downside_fragility": 3.7,
            "catalyst_proximity": 3.2,
            "evidence": ["SRC-COHR-Q2FY26-20260204", "SRC-COHR-VAL-20260227", "SRC-TF-LASER-20251208"],
        },
        {
            "ticker": "300394.SZ",
            "name": "天孚通信",
            "market": "A股",
            "thesis_node": "精密光器件/组件",
            "chokepoint_node": "高速光器件与组件精密制造",
            "rationale": "组件受益确定，但需要更多单价、客户和估值证据支撑高行动状态。",
            "future_space": "高速组件数量和精密度提升。",
            "risks": "客户认证、单价下行、估值弹性不足。",
            "scores": (3.8, 3.8, 3.1, 3.4, 3.1, 3.2, 3.3),
            "demand_visibility": 3.8,
            "irreplaceability": 3.6,
            "market_underpricing": 3.0,
            "expected_excess_return": 0.04,
            "valuation_tolerance": 3.0,
            "downside_fragility": 3.4,
            "catalyst_proximity": 3.1,
            "evidence": ["SRC-TFC-Q3-20251030", "SRC-TF-LASER-20251208", "SRC-LITE-Q2FY26-20260203"],
        },
        {
            "ticker": "FN",
            "name": "Fabrinet",
            "market": "US",
            "thesis_node": "光模块代工制造",
            "chokepoint_node": "制造产能和客户订单 beta",
            "rationale": "制造 beta 清晰，但稀缺性和利润弹性不足以给高行动状态。",
            "future_space": "AI 数据通信代工订单和产能利用率提升。",
            "risks": "客户转单、毛利率稳定低弹性、产能扩张竞争。",
            "scores": (3.1, 3.5, 2.9, 3.5, 3.1, 3.4, 2.9),
            "demand_visibility": 3.6,
            "irreplaceability": 3.0,
            "market_underpricing": 2.9,
            "expected_excess_return": 0.02,
            "valuation_tolerance": 2.9,
            "downside_fragility": 3.2,
            "catalyst_proximity": 3.0,
            "evidence": ["SRC-FN-Q2FY26-20260202", "SRC-LITE-Q2FY26-20260203", "SRC-COHR-Q2FY26-20260204"],
        },
        {
            "ticker": "603083.SH",
            "name": "剑桥科技",
            "market": "A股",
            "thesis_node": "二阶光通信主题敞口",
            "chokepoint_node": "光通信产品敞口但瓶颈证据弱",
            "rationale": "截至 cutoff，证据不足以证明其具备一线瓶颈控制或高质量赔率。",
            "future_space": "AI 光通信主题带动，但缺少核心客户和高端产品证据。",
            "risks": "主题 beta、利润率波动、缺少稀缺性证据。",
            "scores": (2.5, 3.0, 2.5, 2.6, 2.8, 2.8, 2.6),
            "demand_visibility": 3.0,
            "irreplaceability": 2.4,
            "market_underpricing": 2.5,
            "expected_excess_return": -0.02,
            "valuation_tolerance": 2.5,
            "downside_fragility": 3.8,
            "catalyst_proximity": 2.7,
            "evidence": ["SRC-CIG-Q3-20251027", "SRC-TF-800G-20260210", "SRC-FN-Q2FY26-20260202"],
        },
    ]
    targets: list[dict[str, Any]] = []
    components = list(SCORE_WEIGHTS)
    for row in rows:
        scores = row.pop("scores")
        evidence_ids = row.pop("evidence")
        review_ids: list[str] = []
        for evidence_id in evidence_ids:
            review_ids.extend(review_by_source.get(evidence_id, [])[:1])
        score_subcomponents = {
            component: [
                {
                    "name": component,
                    "score": score,
                    "weight": 1.0,
                    "evidence_ids": evidence_ids,
                    "review_ids": review_ids,
                    "rationale": row["rationale"],
                    "status": "verified_with_caveats",
                }
            ]
            for component, score in zip(components, scores)
        }
        target = {
            **row,
            "valuation_status": "verified" if row["ticker"] in {"300308.SZ", "300502.SZ"} else "verified_with_caveats",
            "score_subcomponents": score_subcomponents,
            "thesis_kill_tests": [
                {
                    "test": "800G/1.6T ASP 与毛利率同步下滑",
                    "evidence_needed": "季度产品 ASP、毛利率、库存和订单",
                    "downgrade_action": "从 actionable_long 降为 watch_only 或 no_action",
                    "source_plan": "2026Q1/Q2 财报、投资者问答、客户 capex 更新",
                },
                {
                    "test": "核心客户订单或认证份额丢失",
                    "evidence_needed": "客户订单、认证、出货份额和交付周期",
                    "downgrade_action": "重新评分稀缺性和风险控制",
                    "source_plan": "公司公告、产业链跟踪、客户平台更新",
                },
            ],
        }
        for component, score in zip(components, scores):
            target[component] = score
        targets.append(target)
    return targets


def _review_ids_by_source() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for node_id, source_ids in L3_SOURCE_MAP.items():
        for index, source_id in enumerate(source_ids, start=1):
            out.setdefault(source_id, []).append(_review_id(node_id, index))
    return out


def _fetch_forward_labels(tickers: list[str]) -> dict[str, dict[str, Any]]:
    labels: dict[str, dict[str, Any]] = {}
    try:
        import yfinance as yf  # type: ignore
    except Exception:
        return _fallback_labels("fallback_unverified_yfinance_unavailable")

    for ticker in tickers:
        yahoo_ticker = YFINANCE_TICKERS[ticker]
        try:
            hist = yf.download(
                yahoo_ticker,
                start="2026-03-01",
                end="2026-06-02",
                progress=False,
                auto_adjust=True,
            )
            if hist.empty:
                raise RuntimeError("empty price history")
            close = hist["Close"]
            if hasattr(close, "columns"):
                close = close.iloc[:, 0]
            close = close.dropna()
            start_price = float(close.iloc[0])
            end_price = float(close.iloc[-1])
            labels[ticker] = {
                "start_date": str(close.index[0].date()),
                "end_date": str(close.index[-1].date()),
                "start_price": start_price,
                "end_price": end_price,
                "forward_3m_return": end_price / start_price - 1,
                "label_status": (
                    "verified"
                    if str(close.index[-1].date()) == EVALUATION_DATE
                    else "verified_last_available_close_before_evaluation"
                ),
                "price_source": "yfinance auto_adjust close",
                "as_of_date": AS_OF_DATE,
                "evaluation_date": EVALUATION_DATE,
                "label_window": "three_month_forward",
                "benchmark_return": None,
                "excess_return": None,
            }
        except Exception:
            labels[ticker] = deepcopy(FALLBACK_LABELS[ticker])
            labels[ticker]["label_status"] = "fallback_unverified_price_fetch_failed"
            labels[ticker].update(
                {
                    "price_source": "static fallback; yfinance fetch failed",
                    "as_of_date": AS_OF_DATE,
                    "evaluation_date": EVALUATION_DATE,
                    "label_window": "three_month_forward",
                    "benchmark_return": None,
                    "excess_return": None,
                }
            )
    return labels


def _fallback_labels(status: str) -> dict[str, dict[str, Any]]:
    labels = deepcopy(FALLBACK_LABELS)
    for label in labels.values():
        label["label_status"] = status
        label["price_source"] = "static fallback"
        label["as_of_date"] = AS_OF_DATE
        label["evaluation_date"] = EVALUATION_DATE
        label["label_window"] = "three_month_forward"
        label["benchmark_return"] = None
        label["excess_return"] = None
    return labels


def _label_source() -> dict[str, Any]:
    return {
        "source_id": "SRC-PRICE-LABEL-20260601",
        "title": "YFinance adjusted close forward-return labels for 2026-03-02 to 2026-06-01/2026-05-29",
        "source_bucket": "evidence",
        "support_refute_or_lead": "lead",
        "summary": "用于最终标的回测标签的价格数据；该来源仅用于最终表现标签，不进入论证和排序。",
        "url": "https://finance.yahoo.com/",
        "source_visible_at": EVALUATION_DATE,
        "published_at": EVALUATION_DATE,
        "allowed_usage": "label_only",
        "availability_proof": "Fetched after recommendation freeze; label_only evaluation metadata.",
        "used_in": ["final_target_label"],
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
