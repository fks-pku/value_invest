from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from value_invest_research.adapters.outbound.filesystem_standalone_bom_timeline import (  # noqa: E402
    FileSystemStandaloneBomTimelineRepository,
)
from value_invest_research.adapters.outbound.standalone_bom_html_renderer import (  # noqa: E402
    StandaloneBomHtmlRenderer,
)
from value_invest_research.adapters.outbound.standalone_bom_markdown_renderer import (  # noqa: E402
    StandaloneBomMarkdownRenderer,
)
from value_invest_research.application.use_cases.refresh_standalone_bom_timeline import (  # noqa: E402
    apply_standalone_bom_engine_updates,
)


PROJECT_DIR = ROOT / "research" / "bom" / "gpu_asic_bom_live"
AS_OF_DATE = "2026-07-26"

SOURCE_PRIMARY_ENTITY = {
    "SRC-IMA-FE7454F3DF16C357": "Alphabet / Google",
    "SRC-IMA-827BE491E1696C16": "AMD",
    "SRC-IMA-C4EDEF5E7C92F00A": "AMD",
    "SRC-IMA-A5FCCF63DEA5C3D1": "Meta",
    "SRC-IMA-2C763AC67DEE7166": "Intel",
}

ENTITY_ALIASES = (
    ("NVIDIA", "NVIDIA"),
    ("AMD", "AMD"),
    ("Google", "Alphabet / Google"),
    ("Alphabet", "Alphabet / Google"),
    ("Meta", "Meta"),
    ("Intel", "Intel"),
    ("Broadcom", "Broadcom"),
    ("TSMC", "TSMC"),
    ("Cerebras", "Cerebras"),
    ("Anthropic", "Anthropic"),
    ("OpenAI", "OpenAI"),
    ("Apollo", "Apollo"),
    ("Blackstone", "Blackstone"),
    ("Hyperion", "Hyperion"),
)

CLAIM_ENTITY_ADDITIONS = {
    "CLM-2FCA37B08631953FF8E8": ["ODM / 系统集成商", "数据中心客户"],
    "CLM-3E7460F2A3D35C9FDAFA": ["ODM / 系统集成商", "数据中心客户"],
    "CLM-950B9880914086B2A9A7": ["AI 服务器供应链"],
    "CLM-CD9B632F3F50073264CD": ["数据中心客户"],
}


PRIMARY_NODE_BY_CLAIM = {
    "CLM-00A882B6A935DB1AD17C": "technology.performance_tco",
    "CLM-04304923D2785F9BF2C7": "technology.performance_tco",
    "CLM-0B3E2E9EB9DEDC6245A8": "supply.datacenter_readiness",
    "CLM-0E8D46A33F9AFFC501B9": "technology.customer_adoption",
    "CLM-27AE5D21D4CA5D0D6A34": "esg.financing_commitments",
    "CLM-2999CB0EFFD274CE0102": "technology.platform_competition",
    "CLM-2FCA37B08631953FF8E8": "supply.system_integration",
    "CLM-3299416765848FBD4433": "technology.workload_fit",
    "CLM-331820090F3D099DA91C": "valuation.fundamental_earnings",
    "CLM-362C7794A9620035732B": "valuation.payoff_asymmetry",
    "CLM-37D521EEFB9F6F857B90": "valuation.fundamental_earnings",
    "CLM-3B9E77E0B8E40A72381D": "demand.order_visibility",
    "CLM-3E7460F2A3D35C9FDAFA": "supply.system_integration",
    "CLM-43CB35FDBE246ED347F4": "demand.workload_growth",
    "CLM-49B61F48DADBB4E2D4A5": "supply.advanced_wafer_capacity",
    "CLM-4EE690D37026A9F4F629": "technology.platform_competition",
    "CLM-54378941F4A5AC439E53": "supply.packaging_memory_capacity",
    "CLM-66D93C0EA2341E353EB1": "demand.order_visibility",
    "CLM-731F3BD43FD809B651CC": "technology.platform_competition",
    "CLM-758FDB710004C39CAA81": "valuation.payoff_asymmetry",
    "CLM-888C30A8BD05EBFB8AB2": "esg.governance_capital_allocation",
    "CLM-8A417690E3B553306297": "supply.datacenter_readiness",
    "CLM-8E71C85C38AE2536FF3A": "esg.financing_commitments",
    "CLM-950B9880914086B2A9A7": "supply.packaging_memory_capacity",
    "CLM-B6B6B9DC62A5A02A8765": "demand.order_visibility",
    "CLM-C445906A5E5A3E6A6EEB": "technology.software_ecosystem",
    "CLM-C93ECE27840E4B067671": "valuation.payoff_asymmetry",
    "CLM-CD9B632F3F50073264CD": "demand.order_visibility",
    "CLM-D460E5E49BA33730A77F": "demand.customer_compute_budget",
    "CLM-DB7DAE742B4540F5C0AF": "demand.revenue_realization",
    "CLM-E5D537CA626A12E986E9": "valuation.payoff_asymmetry",
    "CLM-E76EE87775EBB9FD1B35": "demand.workload_growth",
    "CLM-EA56BA91F0944557927A": "valuation.payoff_asymmetry",
}

SECONDARY_NODES_BY_CLAIM = {
    "CLM-0B3E2E9EB9DEDC6245A8": ["esg.financing_commitments"],
    "CLM-2FCA37B08631953FF8E8": ["technology.customer_adoption"],
    "CLM-27AE5D21D4CA5D0D6A34": ["demand.customer_compute_budget"],
    "CLM-331820090F3D099DA91C": [
        "esg.governance_capital_allocation",
        "valuation.payoff_asymmetry",
    ],
    "CLM-37D521EEFB9F6F857B90": [
        "valuation.consensus_expectation",
        "valuation.implied_expectation",
    ],
    "CLM-362C7794A9620035732B": [
        "valuation.consensus_expectation",
        "valuation.implied_expectation",
    ],
    "CLM-43CB35FDBE246ED347F4": ["demand.compute_intensity"],
    "CLM-4EE690D37026A9F4F629": ["technology.workload_fit"],
    "CLM-66D93C0EA2341E353EB1": ["demand.customer_compute_budget"],
    "CLM-731F3BD43FD809B651CC": ["technology.customer_adoption"],
    "CLM-758FDB710004C39CAA81": ["valuation.implied_expectation"],
    "CLM-8A417690E3B553306297": ["esg.financing_commitments"],
    "CLM-950B9880914086B2A9A7": ["supply.shippable_system"],
    "CLM-B6B6B9DC62A5A02A8765": ["technology.customer_adoption"],
    "CLM-C93ECE27840E4B067671": [
        "valuation.consensus_expectation",
        "valuation.implied_expectation",
    ],
    "CLM-CD9B632F3F50073264CD": ["supply.shippable_system"],
    "CLM-D460E5E49BA33730A77F": ["valuation.consensus_expectation"],
    "CLM-E5D537CA626A12E986E9": [
        "valuation.consensus_expectation",
        "valuation.implied_expectation",
    ],
    "CLM-EA56BA91F0944557927A": [
        "valuation.consensus_expectation",
        "valuation.implied_expectation",
    ],
}


STATE_SPEC = {
    "demand.workload_growth": (
        "strengthening",
        "AI 任务需求已有应用侧和公司 TAM 两类信号：Meta 商业 AI 对话快速增长，AMD 将长期加速器 TAM 大幅上调；但当前材料仍以单一应用指标和公司/投行预测为主，尚不足以证明全市场任务量。",
        ["CLM-E76EE87775EBB9FD1B35", "CLM-43CB35FDBE246ED347F4"],
        [],
        ["缺少跨应用的调用量、付费率和 token 历史序列。"],
        "补充云平台、模型服务商和代码 agent 的连续使用量及付费数据。",
    ),
    "demand.compute_intensity": (
        "weak",
        "训练、推理和 agent 被认为会扩大算力需求，但现有材料没有把单位任务计算量与效率改善放在同一口径比较，需求弹性尚未被量化。",
        ["CLM-43CB35FDBE246ED347F4"],
        [],
        ["缺少单位任务 token、延迟、模型规模和硬件效率的可比序列。"],
        "建立单位任务计算量与每 token 成本的同口径历史。",
    ),
    "demand.customer_compute_budget": (
        "strengthening",
        "Meta 2026 年资本开支指引和更高的 2027-2028 年机构估计显示客户预算仍在扩大，外部 TPU 与合作方融资也在增加可用资本；但后续年份主要是分析师情景。",
        ["CLM-D460E5E49BA33730A77F", "CLM-66D93C0EA2341E353EB1"],
        [],
        ["缺少主要云厂商同口径 capex、采购承诺和 AI 收入回报表。"],
        "按季度比较云厂 capex 指引、采购承诺、FCF 与 AI 变现。",
    ),
    "demand.order_visibility": (
        "strengthening",
        "AMD Helios 和外部 TPU 已出现客户、GW、backlog 与交付窗口等可见性线索，但相当一部分数字来自投行模型或供应商计划，仍需客户采购承诺与实际发货交叉验证。",
        [
            "CLM-3B9E77E0B8E40A72381D",
            "CLM-66D93C0EA2341E353EB1",
            "CLM-B6B6B9DC62A5A02A8765",
            "CLM-CD9B632F3F50073264CD",
        ],
        [],
        ["缺少客户侧不可取消订单、实际验收和订单去重。"],
        "验证 2026 年第四季度 Helios 发货、外部 TPU 合同与客户机房进度。",
    ),
    "demand.revenue_realization": (
        "weak",
        "Intel DCAI 的相邻收入增长说明 AI 基础设施支出在扩散，但它不能替代 GPU/ASIC 分部收入、增量毛利和现金流证据；当前材料尚未完成节点到核心公司盈利的闭环。",
        ["CLM-DB7DAE742B4540F5C0AF"],
        [],
        ["缺少 NVIDIA、Broadcom、AMD 可比 AI 收入、毛利和现金流桥。"],
        "补齐核心公司连续季度 AI 收入、订单、毛利与现金流兑现。",
    ),
    "supply.advanced_wafer_capacity": (
        "weak",
        "Intel 上调资本开支表明供给正在响应，但材料没有直接量化 GPU/ASIC 先进晶圆的现有缺口、TSMC 分配和良率，因此不能断言晶圆是当前最强约束。",
        ["CLM-49B61F48DADBB4E2D4A5"],
        [],
        ["缺少先进节点产能、客户分配和主要产品良率。"],
        "获取代工厂产能、先进节点利用率和客户预付款变化。",
    ),
    "supply.packaging_memory_capacity": (
        "strengthening",
        "投行材料同时把 CoWoS、内存、基板和先进逻辑列为持续约束；Intel EMIB-T 的替代路线仍处于较低良率和小批量阶段，说明短期封装与相关输入仍可能限制供给。",
        ["CLM-54378941F4A5AC439E53", "CLM-950B9880914086B2A9A7"],
        [],
        ["缺少 HBM 与先进封装逐季产能、良率、价格和交期。"],
        "追踪 CoWoS/HBM 扩产、交期和替代封装量产节奏。",
    ),
    "supply.system_integration": (
        "strengthening",
        "Helios 的分阶段发货明确把 ODM 调试、制造和客户机房对齐列为爬坡条件，说明有效供给单位已经从单颗芯片转为可验收机架系统。",
        ["CLM-2FCA37B08631953FF8E8", "CLM-3E7460F2A3D35C9FDAFA"],
        [],
        ["缺少 ODM 实际机架产能、一次验收率和交付周期。"],
        "核验第三、第四季度机架发货和 ODM 调试进度。",
    ),
    "supply.datacenter_readiness": (
        "weak",
        "Meta 容量扩张和外部 TPU 的多主体交付结构显示电力、机房与融资会影响上线节奏；但现有材料以项目情景为主，尚未形成可用容量与延期的统一数据。",
        ["CLM-0B3E2E9EB9DEDC6245A8", "CLM-8A417690E3B553306297"],
        [],
        ["缺少客户可用 GW、通电时间和延期项目清单。"],
        "按客户追踪已通电容量、在建容量、预计上线和延期。",
    ),
    "supply.shippable_system": (
        "strengthening",
        "多项输入仍受约束，且 Helios 交付依赖系统与机房同步，因此最终可交付供给短期仍偏紧；不过当前缺少端到端交期、价格和库存序列，证据仍不足。",
        ["CLM-950B9880914086B2A9A7", "CLM-CD9B632F3F50073264CD"],
        [],
        ["缺少系统交期、渠道库存、利用率和实际发货量。"],
        "建立芯片到机架交付的月度交期、价格和库存监控。",
    ),
    "technology.workload_fit": (
        "strengthening",
        "定制 ASIC 在稳定推理和推荐任务上具有明确适配场景，GPU 则仍受益于快速变化的训练和通用任务；现有证据支持分工而非单一路线全面替代。",
        ["CLM-3299416765848FBD4433", "CLM-4EE690D37026A9F4F629"],
        [],
        ["缺少同一客户内训练、推理和推荐任务的实际硬件组合。"],
        "获取生产客户按工作负载划分的 GPU/ASIC 使用结构。",
    ),
    "technology.performance_tco": (
        "weak",
        "AMD 和 TPU 路线均给出成本或性能优势，但分别来自厂商展示和分析师模型，且参数口径不可完全比较；当前不能据此确认端到端 TCO 领先。",
        ["CLM-00A882B6A935DB1AD17C", "CLM-04304923D2785F9BF2C7"],
        [],
        ["缺少独立同模型、同精度、同延迟和同利用率基准。"],
        "用独立生产基准比较每 token 成本、延迟、功耗和利用率。",
    ),
    "technology.software_ecosystem": (
        "strengthening",
        "ROCm 发布节奏和公司展示性能明显改善，表明 AMD 软件追赶加速；但仍缺少开发者采用、迁移时间和生产稳定性的第三方证据。",
        ["CLM-C445906A5E5A3E6A6EEB"],
        [],
        ["缺少第三方开发者、框架兼容和生产故障数据。"],
        "验证主要模型框架、客户迁移周期和生产利用率。",
    ),
    "technology.customer_adoption": (
        "weak",
        "Helios 已进入量产计划，AMD 与 Cerebras 方案及外部 TPU 商业模式拓宽了客户选择；但采用仍多是计划、演示和带激励的生态扩张，复购尚未验证。",
        [
            "CLM-0E8D46A33F9AFFC501B9",
            "CLM-2FCA37B08631953FF8E8",
            "CLM-731F3BD43FD809B651CC",
            "CLM-B6B6B9DC62A5A02A8765",
        ],
        [],
        ["缺少生产客户复购、无补贴订单和部署利用率。"],
        "追踪 2027 年客户量产、复购和认股权证之外的商业订单。",
    ),
    "technology.platform_competition": (
        "strengthening",
        "定制 ASIC 正从内部自用向外部销售扩展，GPU 份额可能下降但绝对市场仍增长；Intel 先进代工尚未形成外部规模，当前更可能是 NVIDIA 平台主导下的多路线增量竞争。",
        [
            "CLM-2999CB0EFFD274CE0102",
            "CLM-4EE690D37026A9F4F629",
            "CLM-731F3BD43FD809B651CC",
        ],
        [],
        ["缺少同口径数据中心 AI 加速器收入与出货份额。"],
        "补齐 merchant GPU、云厂 ASIC 和其他加速器的同口径份额。",
    ),
    "valuation.fundamental_earnings": (
        "weak",
        "外部 TPU 情景可能大幅提高 Alphabet 收入和毛利，但资本开支也可能压低自由现金流；AMD 收入增长还可能被客户认股权证稀释。现有材料揭示盈利桥的两端，却没有形成可复现的公司模型。",
        ["CLM-37D521EEFB9F6F857B90"],
        ["CLM-331820090F3D099DA91C"],
        ["缺少公司分部收入、增量毛利、资本开支、稀释和 FCF 的统一桥。"],
        "为 NVIDIA、Broadcom、AMD、Alphabet 分别建立收入到每股价值桥。",
    ),
    "valuation.consensus_expectation": (
        "strengthening",
        "多家投行已在目标价和长期情景中计入 AI 加速器、TPU、Meta 算力和 AMD 产品改善，说明主题并非未被市场发现；但公司间看法分化显著。",
        [
            "CLM-37D521EEFB9F6F857B90",
            "CLM-362C7794A9620035732B",
            "CLM-C93ECE27840E4B067671",
            "CLM-D460E5E49BA33730A77F",
            "CLM-E5D537CA626A12E986E9",
            "CLM-EA56BA91F0944557927A",
        ],
        [],
        ["缺少更广泛的一致预期分布及历史修正序列。"],
        "收集同一截面多家机构收入、EPS、目标价与核心假设。",
    ),
    "valuation.implied_expectation": (
        "weak",
        "AMD 的现价高于两份机构目标价，Alphabet 和 Meta 则仍有目标价上行空间；但目标价不是股价隐含预期，当前尚无反向 DCF 或隐含份额路径。",
        ["CLM-E5D537CA626A12E986E9", "CLM-EA56BA91F0944557927A"],
        ["CLM-362C7794A9620035732B", "CLM-C93ECE27840E4B067671", "CLM-758FDB710004C39CAA81"],
        ["缺少截面价格下的隐含收入、利润率和份额路径。"],
        "按同一截面为候选公司建立反向 DCF 和隐含增长模型。",
    ),
    "valuation.revision_momentum": (
        "unresolved",
        "现有报告包含单次目标价和模型调整，但没有连续历史序列，无法判断盈利上修是否持续快于估值扩张。",
        [],
        [],
        ["缺少至少六个季度的收入、EPS、目标价和估值修正历史。"],
        "建立逐周/逐季一致预期修正与股价反应序列。",
    ),
    "valuation.payoff_asymmetry": (
        "weak",
        "机构对 Alphabet、Meta 仍给出约三成目标价空间，而 AMD 的报告股价显著高于两家机构目标价；这提示赔率应按公司而非按主题判断。由于缺少统一盈利桥、反向估值和概率情景，当前只支持观察。",
        ["CLM-E5D537CA626A12E986E9", "CLM-EA56BA91F0944557927A"],
        ["CLM-362C7794A9620035732B", "CLM-C93ECE27840E4B067671", "CLM-758FDB710004C39CAA81", "CLM-331820090F3D099DA91C"],
        ["缺少统一时点的基本、乐观、悲观情景及概率。"],
        "完成公司盈利桥、反向估值和量化 kill tests 后再决定动作。",
    ),
    "esg.energy_water": (
        "unresolved",
        "当前材料没有直接量化 GPU/ASIC 部署的能源、水和许可约束，不能形成结论。",
        [],
        [],
        ["缺少项目级电力、水耗、PUE、许可与延期数据。"],
        "补充主要客户数据中心资源效率与许可进度。",
    ),
    "esg.export_market_access": (
        "unresolved",
        "当前材料没有覆盖出口管制、受限收入和替代产品影响，不能形成结论。",
        [],
        [],
        ["缺少官方规则、公司受限收入、库存损失和许可进展。"],
        "建立出口规则事件账本并映射公司收入和产品。",
    ),
    "esg.concentration": (
        "unresolved",
        "现有材料提及 Google、Broadcom、TSMC 及少数大型客户，但没有系统量化供应商、客户和地区集中度。",
        [],
        [],
        ["缺少前五客户、单一代工、地区收入和替代供应数据。"],
        "补齐核心公司客户、供应与地区集中度。",
    ),
    "esg.governance_capital_allocation": (
        "confirmed",
        "AMD 以客户认股权证推动采用被投行视为高额获客费用，可能显著稀释 GPU 业务未来利润；这是已识别但尚未量化到每股价值的治理风险。",
        [],
        ["CLM-888C30A8BD05EBFB8AB2", "CLM-331820090F3D099DA91C"],
        ["缺少认股权证完全摊薄、对应订单和增量利润的量化桥。"],
        "把客户激励的完全摊薄成本与实际订单毛利逐项比较。",
    ),
    "esg.financing_commitments": (
        "strengthening",
        "TPU 和 Meta 扩产越来越依赖 SPV、合作方融资、采购承诺与潜在担保。结构可释放资本，但风险承担和资产利用率透明度下降，应视为需求融资能力与尾部风险的共同变量。",
        ["CLM-27AE5D21D4CA5D0D6A34", "CLM-8E71C85C38AE2536FF3A"],
        [],
        ["缺少 SPV 合同、担保、租赁义务和闲置资产归属。"],
        "穿透主要 SPV 与合作融资的现金流、担保和利用率条款。",
    ),
}


def _read_claims() -> list[dict]:
    return [
        json.loads(line)
        for line in (PROJECT_DIR / "ledger" / "claims.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]


def _node_index(profile: dict) -> dict[str, dict]:
    return {
        str(node["logic_node_id"]): node
        for lens in profile["lenses"]
        for node in lens["logic_nodes"]
    }


def _mapping_rows(claims: list[dict], profile: dict) -> list[dict]:
    claims_by_id = {str(row["claim_id"]): row for row in claims}
    missing = set(claims_by_id) - set(PRIMARY_NODE_BY_CLAIM)
    extra = set(PRIMARY_NODE_BY_CLAIM) - set(claims_by_id)
    if missing or extra:
        raise ValueError(f"Claim mapping drift: missing={missing}, extra={extra}")
    nodes = _node_index(profile)
    support_pairs = {
        (claim_id, node_id)
        for node_id, spec in STATE_SPEC.items()
        for claim_id in spec[2]
    }
    refute_pairs = {
        (claim_id, node_id)
        for node_id, spec in STATE_SPEC.items()
        for claim_id in spec[3]
    }
    rows = []
    for claim_id, primary_node_id in PRIMARY_NODE_BY_CLAIM.items():
        claim = claims_by_id[claim_id]
        for role, node_id in [
            ("primary", primary_node_id),
            *[
                ("secondary", item)
                for item in SECONDARY_NODES_BY_CLAIM.get(claim_id, [])
            ],
        ]:
            stance = str(claim.get("stance") or "neutral")
            direction = (
                "support"
                if (claim_id, node_id) in support_pairs
                else "refute"
                if (claim_id, node_id) in refute_pairs
                else "support"
                if stance == "support"
                else "refute"
                if stance == "refute"
                else "neutral"
            )
            claim_type = str(claim.get("claim_type") or "opinion")
            evidence_nature = (
                "fact"
                if claim_type
                in {"reported_metric", "production_ramp", "reported_pipeline"}
                else "forecast"
                if any(
                    token in claim_type
                    for token in ("forecast", "estimate", "scenario", "model")
                )
                else "opinion"
            )
            materiality = (
                "high"
                if direction == "refute"
                or node_id
                in {
                    "demand.order_visibility",
                    "valuation.payoff_asymmetry",
                    "valuation.fundamental_earnings",
                }
                else "medium"
            )
            rows.append(
                {
                    "claim_id": claim_id,
                    "logic_node_id": node_id,
                    "mapping_role": role,
                    "direction": direction,
                    "evidence_nature": evidence_nature,
                    "directness": (
                        "direct"
                        if claim_type
                        in {"reported_metric", "production_ramp", "reported_pipeline"}
                        else "indirect"
                    ),
                    "novelty": "new",
                    "materiality": materiality,
                    "rationale": (
                        f"该原子观点用于回答“{nodes[node_id]['question']}”；"
                        "仅改变该逻辑节点的证据状态，不直接等同于最终投资动作。"
                    ),
                    "entities": _entities(claim),
                    "metric_id": claim_type,
                    "expectation_delta": (
                        "positive"
                        if direction == "support"
                        else "negative"
                        if direction == "refute"
                        else "neutral"
                    ),
                    "downstream_impacts": nodes[node_id].get(
                        "downstream_node_ids", []
                    ),
                    "review_status": "gpt_verified",
                }
            )
    return rows


def _state_rows() -> list[dict]:
    return [
        {
            "logic_node_id": node_id,
            "as_of_date": AS_OF_DATE,
            "state": spec[0],
            "conclusion": spec[1],
            "previous_state": "",
            "change_summary": "首个结构化截面，只建立基线，不虚构相较上一期的变化。",
            "support_claim_ids": spec[2],
            "refute_claim_ids": spec[3],
            "evidence_gaps": spec[4],
            "next_validation": spec[5],
            "review_status": "gpt_verified",
        }
        for node_id, spec in STATE_SPEC.items()
    ]


def _entity_state_rows(
    mappings: list[dict],
    claims: list[dict],
    profile: dict,
) -> list[dict]:
    claims_by_id = {str(row["claim_id"]): row for row in claims}
    nodes = _node_index(profile)
    grouped: dict[tuple[str, str], list[dict]] = {}
    for mapping in mappings:
        node_id = str(mapping["logic_node_id"])
        for entity_name in mapping.get("entities") or ["行业 / 多主体"]:
            grouped.setdefault((node_id, str(entity_name)), []).append(mapping)

    rows = []
    for (node_id, entity_name), entity_mappings in sorted(grouped.items()):
        support_ids = list(
            dict.fromkeys(
                str(row["claim_id"])
                for row in entity_mappings
                if str(row.get("direction") or "") == "support"
            )
        )
        refute_ids = list(
            dict.fromkeys(
                str(row["claim_id"])
                for row in entity_mappings
                if str(row.get("direction") or "") == "refute"
            )
        )
        neutral_ids = list(
            dict.fromkeys(
                str(row["claim_id"])
                for row in entity_mappings
                if str(row.get("direction") or "") == "neutral"
            )
        )
        if support_ids and refute_ids:
            effect = "mixed"
            direction_text = "多空并存"
        elif support_ids:
            effect = "positive"
            direction_text = "正向"
        elif refute_ids:
            effect = "negative"
            direction_text = "负向"
        else:
            effect = "unclear"
            direction_text = "尚不明确"
        claim_ids = list(
            dict.fromkeys(
                str(row["claim_id"]) for row in entity_mappings
            )
        )
        claim_summaries = [
            _compact_statement(str(claims_by_id[claim_id]["statement"]))
            for claim_id in claim_ids[:2]
        ]
        assessment = (
            f"{entity_name}在“{nodes[node_id]['title']}”下，"
            "当前最重要的信息是："
            f"{'；'.join(claim_summaries)}"
            f"。综合这些材料，该实体对本节点的截面影响为{direction_text}；"
            "方向可由下方支持与反证观点逐项核对。"
        )
        rows.append(
            {
                "logic_node_id": node_id,
                "entity_name": entity_name,
                "as_of_date": AS_OF_DATE,
                "assessment": assessment,
                "change_summary": (
                    "首个实体级结构化截面，只建立基线，不虚构相较上一期的变化。"
                ),
                "investment_effect": effect,
                "support_claim_ids": support_ids,
                "refute_claim_ids": refute_ids,
                "evidence_gaps": STATE_SPEC[node_id][4],
                "next_validation": (
                    f"围绕 {entity_name} 验证：{STATE_SPEC[node_id][5]}"
                ),
                "review_status": "gpt_verified",
                "neutral_claim_ids": neutral_ids,
            }
        )
    return rows


def _revision_rows() -> list[dict]:
    return [
        {
            "revision_type": "baseline",
            "logic_node_id": node_id,
            "as_of_date": AS_OF_DATE,
            "previous_state": "",
            "new_state": spec[0],
            "change_direction": "unchanged",
            "magnitude": "low",
            "rationale": "首次把既有材料迁移到结构化逻辑账本，建立可供后续比较的基线。",
            "trigger_claim_ids": list(dict.fromkeys([*spec[2], *spec[3]])),
            "conflicting_claim_ids": spec[3],
            "downstream_impacts": [],
            "next_validation": spec[5],
            "review_status": "gpt_verified",
        }
        for node_id, spec in STATE_SPEC.items()
    ]


def _investment_snapshot() -> list[dict]:
    return [
        {
            "as_of_date": AS_OF_DATE,
            "action_state": "watch_only",
            "summary": "GPU/ASIC 的需求、替代路线和交付可见性正在增强，但当前证据主要来自五份投行材料，尚未完成官方财务兑现、公司盈利桥、反向估值和量化风险控制。产业逻辑可继续跟踪，证券层面暂不支持统一做多。",
            "fundamental_delta": "任务、客户预算、Helios/TPU 订单与系统交付线索偏正面；公司级收入、毛利和现金流闭环仍弱。",
            "consensus_delta": "投行已普遍计入 AI 加速器高增长、ASIC 份额提升和平台竞争，主题本身不再是低共识。",
            "priced_in_delta": "AMD 在两份报告的截面价格高于目标价；Alphabet、Meta 尚有目标价空间，但并非纯 GPU/ASIC 敞口。",
            "positive_node_ids": [
                "demand.workload_growth",
                "demand.customer_compute_budget",
                "demand.order_visibility",
                "supply.packaging_memory_capacity",
                "supply.system_integration",
                "technology.platform_competition",
            ],
            "negative_node_ids": [
                "valuation.fundamental_earnings",
                "valuation.implied_expectation",
                "valuation.payoff_asymmetry",
                "esg.governance_capital_allocation",
            ],
            "company_impacts": [
                {
                    "company": "AMD",
                    "ticker": "AMD",
                    "exposure": "MI450/Helios GPU 与 ROCm 平台直接受益于替代需求。",
                    "earnings_bridge": "2026 年第三季度末开始交付、第四季度与 2027 年爬坡；利润弹性需扣除客户认股权证和研发投入。",
                    "priced_in": "两份投行报告均为中性，报告股价显著高于 385/410 美元目标价。",
                    "conclusion": "产品与订单方向改善，但赔率和股东可得利润尚未通过。",
                    "source_ids": [
                        "SRC-IMA-827BE491E1696C16",
                        "SRC-IMA-C4EDEF5E7C92F00A",
                    ],
                    "action_state": "watch_only",
                },
                {
                    "company": "Alphabet",
                    "ticker": "GOOGL",
                    "exposure": "TPU 自用并可能通过外部所有权/SPV 模式扩大 merchant 市场。",
                    "earnings_bridge": "高情景可提升 TPU 收入与毛利，但巨额资本开支可能使自由现金流转负。",
                    "priced_in": "巴克莱 425 美元目标价相对报告股价约有 34% 空间，关键假设仍是外部 TPU 商业化。",
                    "conclusion": "潜在预期差较 AMD 更有吸引力，但资本强度与合同真实性尚待验证。",
                    "source_ids": ["SRC-IMA-FE7454F3DF16C357"],
                    "action_state": "watch_only",
                },
                {
                    "company": "Meta",
                    "ticker": "META",
                    "exposure": "AI 广告、商业 agent、自研 MTIA/Iris 与大规模算力采购的综合受益者。",
                    "earnings_bridge": "广告回报可覆盖部分投入，但 2027-2028 年 capex、合作方融资和第三方云收入高度不确定。",
                    "priced_in": "德银 800 美元目标价相对报告股价约有 32% 空间。",
                    "conclusion": "应用变现提供缓冲，但它不是纯硬件敞口，需穿透资本承诺。",
                    "source_ids": ["SRC-IMA-A5FCCF63DEA5C3D1"],
                    "action_state": "watch_only",
                },
                {
                    "company": "Intel",
                    "ticker": "INTC",
                    "exposure": "AI 服务器 CPU、先进代工和 EMIB-T 替代封装的间接受益者。",
                    "earnings_bridge": "DCAI 收入增长和 capex 上调提供邻近验证，但外部先进代工收入占比仍低。",
                    "priced_in": "当前材料没有提供同截面可复现估值。",
                    "conclusion": "供给侧可选项存在，尚无足够外部客户规模与估值证据。",
                    "source_ids": ["SRC-IMA-2C763AC67DEE7166"],
                    "action_state": "watch_only",
                },
            ],
            "gate_results": {
                "logic_coverage": True,
                "company_financial_bridge": False,
                "valuation": False,
                "refutation": True,
                "risk_control": False,
            },
            "kill_tests": [
                {
                    "metric": "Helios 量产与客户交付",
                    "threshold": "2026 年第四季度仍未形成可验证发货和客户验收",
                    "cadence": "quarterly",
                    "downgrade_action": "下调 AMD 订单与技术采用节点，并停止以 2027 年爬坡为基线。"
                },
                {
                    "metric": "客户 AI capex 与采购承诺",
                    "threshold": "主要云厂商连续两个季度下修 AI 基础设施指引或取消订单",
                    "cadence": "quarterly",
                    "downgrade_action": "下调需求预算和订单可见性节点。"
                },
                {
                    "metric": "AMD 客户认股权证完全摊薄成本",
                    "threshold": "稀释与获客成本吞噬预计 GPU 增量利润的大部分",
                    "cadence": "event_driven",
                    "downgrade_action": "维持或下调 no_action，不以收入增长替代股东回报。"
                }
            ],
            "next_catalysts": [
                "Helios 2026 年第三季度末首批交付及第四季度量产进度",
                "外部 TPU 采购合同、SPV 条款与实际交付",
                "核心公司下一轮收入、毛利、capex 与现金流指引",
                "同一截面反向估值和一致预期修正序列"
            ],
            "review_status": "gpt_verified"
        }
    ]


def _entities(claim: dict) -> list[str]:
    statement = str(claim.get("statement") or "")
    source_id = str(claim.get("source_id") or "")
    claim_id = str(claim.get("claim_id") or "")
    entities = [SOURCE_PRIMARY_ENTITY.get(source_id, "")]
    entities.extend(
        canonical
        for token, canonical in ENTITY_ALIASES
        if token in statement
    )
    entities.extend(CLAIM_ENTITY_ADDITIONS.get(claim_id, []))
    resolved = list(dict.fromkeys(item for item in entities if item))
    return resolved or ["行业 / 多主体"]


def _compact_statement(statement: str, limit: int = 118) -> str:
    compact = " ".join(statement.split())
    if len(compact) <= limit:
        return compact
    return compact[:limit].rstrip("，。； ") + "…"


def _write_input(name: str, rows: list[dict]) -> Path:
    path = PROJECT_DIR / "inbox" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path


def main() -> None:
    claims = _read_claims()
    profile = json.loads(
        (PROJECT_DIR / "timeline_profile.json").read_text(encoding="utf-8")
    )
    mappings = _mapping_rows(claims, profile)
    states = _state_rows()
    entity_states = _entity_state_rows(mappings, claims, profile)
    revisions = _revision_rows()
    snapshots = _investment_snapshot()
    _write_input("reviewed_claim_mappings_20260726.jsonl", mappings)
    _write_input("reviewed_logic_states_20260726.jsonl", states)
    _write_input("reviewed_entity_states_20260726.jsonl", entity_states)
    _write_input("reviewed_thesis_revisions_20260726.jsonl", revisions)
    _write_input("reviewed_investment_snapshot_20260726.jsonl", snapshots)
    repository = FileSystemStandaloneBomTimelineRepository(PROJECT_DIR)
    result = apply_standalone_bom_engine_updates(
        repository=repository,
        renderer=StandaloneBomMarkdownRenderer(project_dir=PROJECT_DIR),
        html_renderer=StandaloneBomHtmlRenderer(project_dir=PROJECT_DIR),
        raw_mappings=mappings,
        raw_logic_states=states,
        raw_entity_states=entity_states,
        raw_revisions=revisions,
        raw_investment_snapshots=snapshots,
        as_of_date=AS_OF_DATE,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
