from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from value_invest_research.domain.research_goal import ResearchGoal


SCORE_COMPONENTS = [
    "future_space",
    "chokepoint_strength",
    "valuation_odds",
    "evidence_quality",
    "disconfirming_risk_control",
    "monitorability",
    "target_ranking",
    "payoff_convexity",
    "risk_control",
]


@dataclass(frozen=True)
class QuestionTemplate:
    """Domain-specific L2 bucket and L3 leaf question design."""

    id: str
    question: str
    why_this_depth: str
    l3_questions: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class DomainPlaybook:
    """Research-type adapter owned by domain knowledge, not presentation code."""

    playbook_id: str
    research_type: str
    q_map: dict[str, str]
    mechanism_buckets: list[str]
    l2_templates: dict[str, list[QuestionTemplate]]
    supply_chain_layers: list[dict[str, str]] = field(default_factory=list)
    quality_rule: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "playbook_id": self.playbook_id,
            "research_type": self.research_type,
            "q_map": dict(self.q_map),
            "mechanism_buckets": list(self.mechanism_buckets),
            "l2_templates": {
                qid: [
                    {
                        "id": template.id,
                        "question": template.question,
                        "why_this_depth": template.why_this_depth,
                        "l3_questions": list(template.l3_questions),
                    }
                    for template in templates
                ]
                for qid, templates in self.l2_templates.items()
            },
            "supply_chain_layers": list(self.supply_chain_layers),
            "quality_rule": self.quality_rule,
        }


def resolve_domain_playbook(goal: ResearchGoal) -> DomainPlaybook:
    hint = goal.domain_hint.lower()
    topic = goal.topic.lower()
    if "memory" in hint or "storage" in hint or "存储" in goal.topic or "memory" in topic:
        return memory_industry_playbook(goal)
    if "optical" in hint or "optical" in topic or "光模块" in goal.topic or "光通信" in goal.topic:
        return optical_module_playbook(goal)
    if "semiconductor" in hint or "半导体" in goal.topic:
        return semiconductor_hardware_playbook(goal)
    return default_playbook(goal)


def memory_industry_playbook(goal: ResearchGoal) -> DomainPlaybook:
    q_map = {
        "Q1": "需求：AI、数据中心和终端需求如何转化为可持续的 bit、ASP 与产品 mix？",
        "Q2": "价值捕获：哪些存储环节具备稀缺性、定价权和财务转化能力？",
        "Q3": "反证与定价：哪些供给、价格、客户 capex 或估值信号会推翻机会？",
        "Q4": "标的：哪些具体资产同时具备稀缺性、赔率、业绩弹性和可监控风险？",
    }
    return DomainPlaybook(
        playbook_id="memory_industry",
        research_type=goal.normalized_type(),
        q_map=q_map,
        mechanism_buckets=[
            "workload_to_memory_demand",
            "demand_supply_slope_mismatch",
            "price_volume_mix_bridge",
            "product_unit_economics",
            "company_value_capture",
            "capital_chain_second_order",
            "valuation_and_rerating",
            "counter_supply_and_substitution",
            "target_mapping",
            "model_reconciliation",
        ],
        l2_templates={
            "Q1": [
                _l2(
                    "Q1.1",
                    "工作负载到产品需求的传导链",
                    "把训练、推理、RAG/Agent、数据库、数据湖和传统终端分别映射到 HBM、DDR5/LPDDR、enterprise SSD、NAND 与 nearline HDD，并区分一次性库存补货和可持续 workload 拉动。",
                    [
                        _memory_l3(
                            "AI 加速器平台的 HBM 容量/带宽强度是否继续上升，并如何传导到 HBM bit demand 和 mix？",
                            "future_space",
                            "industry-report-analysis",
                            required_materials=["GPU/ASIC 平台内存配置", "HBM bit demand 或 GB/accelerator 假设", "供应商 HBM 收入/mix 披露", "客户 capex/RPO/订单验证"],
                            refute_evidence="新一代加速器单位 HBM 强度下降、客户推迟 GPU/ASIC 订单、HBM 收入增长弱于加速器出货。",
                        ),
                        _memory_l3(
                            "推理、RAG、Agent 和数据湖是否拉动 eSSD、NAND 与 nearline HDD 的新增容量，而不只是库存回补？",
                            "future_space",
                            "industry-report-analysis",
                            required_materials=["hyperscaler 存储 capex 或采购口径", "eSSD/nearline HDD 出货与容量", "NAND/HDD ASP 与库存", "云厂商 workload 或对象存储需求证据"],
                            refute_evidence="eSSD/HDD 收入增长主要来自补库存或价格，客户新增容量和长期订单不足。",
                        ),
                        _memory_l3(
                            "PC、手机、消费电子和通用服务器需求会不会稀释 AI 存储主线？",
                            "disconfirming_risk_control",
                            "financial-statement-analysis",
                            required_materials=["终端 DRAM/NAND 出货", "渠道库存", "公司分产品收入/margin", "终端 OEM 指引"],
                            refute_evidence="消费端疲弱导致产能回流、价格压力或混合业务公司利润被低端产品拖累。",
                        ),
                    ],
                ),
                _l2(
                    "Q1.2",
                    "price / volume / mix / inventory 增长质量",
                    "把收入增长拆成 bit shipment、ASP、产品 mix、利用率和库存变化，避免把价格周期高点误判为长期成长。",
                    [
                        _memory_l3(
                            "当前收入和利润增长分别由 bit shipment、ASP、产品 mix、利用率还是库存回补驱动？",
                            "future_space",
                            "financial-statement-analysis",
                            required_materials=["分产品收入", "bit shipment", "ASP", "gross margin bridge", "inventory days"],
                            refute_evidence="收入增长主要由短期 ASP 和库存回补驱动，而 bit shipment 或高端 mix 没有同步改善。",
                        ),
                        _memory_l3(
                            "合约价、现货价、库存天数和客户预付款是否支持需求持续性？",
                            "monitorability",
                            "industry-report-analysis",
                            required_materials=["DRAM/NAND 合约价", "现货价", "库存天数", "客户预付款/长期协议", "渠道库存"],
                            refute_evidence="现货价先行转弱、库存天数回升、预付款减少或长期协议转短单。",
                        ),
                    ],
                ),
                _l2(
                    "Q1.3",
                    "需求斜率与供给斜率错配",
                    "比较 AI 存储需求增速与行业可增加 bit supply 的速度，判断机会来自长期错配还是短期补库。",
                    [
                        _memory_l3(
                            "AI/HBM/eSSD 需求斜率是否明显高于行业 bit supply、wafer starts 和产能转换斜率？",
                            "future_space",
                            "industry-report-analysis",
                            required_materials=["bit demand forecast", "wafer starts", "HBM capacity conversion", "NAND layer additions", "HDD exabyte capacity"],
                            refute_evidence="新增产能、良率提升或产品切换速度足以覆盖需求增量。",
                        ),
                        _memory_l3(
                            "客户 capex、RPO/backlog、GPU/ASIC 订单和服务器交付是否共同确认需求持续？",
                            "future_space",
                            "financial-statement-analysis",
                            required_materials=["hyperscaler capex", "RPO/backlog", "AI 服务器订单", "GPU/ASIC 交付", "存储供应商指引"],
                            refute_evidence="云厂商 capex 或 AI 服务器订单放缓，存储订单先于收入转弱。",
                        ),
                    ],
                ),
            ],
            "Q2": [
                _l2(
                    "Q2.1",
                    "HBM / 高端 DRAM 稀缺性",
                    "拆开客户认证、TSV/堆叠、先进封装、良率、代际迁移和长期协议，判断 HBM 是否是真瓶颈而非普通涨价。",
                    [
                        _memory_l3(
                            "HBM 供应商的客户认证、良率、TSV/堆叠和先进封装能力是否形成结构性壁垒？",
                            "chokepoint_strength",
                            "industry-report-analysis",
                            required_materials=["客户认证周期", "HBM 良率", "TSV/stacking 能力", "CoWoS/先进封装约束", "供应商份额"],
                            refute_evidence="认证周期缩短、封装瓶颈消失、竞争对手良率快速追平。",
                        ),
                        _memory_l3(
                            "HBM3E/HBM4 代际迁移是否改变 SK hynix、Micron、Samsung 的份额和毛利率？",
                            "chokepoint_strength",
                            "financial-statement-analysis",
                            required_materials=["HBM3E/HBM4 客户导入", "份额变化", "毛利率", "capex/ramp schedule", "客户集中度"],
                            refute_evidence="代际迁移让落后者快速追平，或领先者因良率/客户问题丢失份额。",
                        ),
                        _memory_l3(
                            "HBM 的预付款、长期协议、ASP 和毛利率是否证明定价权已经进入财务报表？",
                            "chokepoint_strength",
                            "financial-statement-analysis",
                            required_materials=["prepayment", "long-term agreement", "ASP", "gross margin", "segment revenue"],
                            refute_evidence="收入增长没有转化为毛利率和现金流，或客户议价压低 ASP。",
                        ),
                    ],
                ),
                _l2(
                    "Q2.2",
                    "NAND / eSSD / nearline HDD 周期与现金流",
                    "判断容量存储是结构性瓶颈、供给纪律带来的现金流机会，还是普通周期 beta。",
                    [
                        _memory_l3(
                            "eSSD / NAND 涨价能否转化为可持续毛利率、FCF 和资本回报？",
                            "payoff_convexity",
                            "financial-statement-analysis",
                            required_materials=["eSSD/NAND revenue", "ASP", "gross margin", "capex", "FCF", "inventory"],
                            refute_evidence="NAND 价格上行但库存、capex 或竞争导致 FCF 没有改善。",
                        ),
                        _memory_l3(
                            "nearline HDD 的供给纪律、客户长约和容量需求是否创造现金流型瓶颈？",
                            "chokepoint_strength",
                            "financial-statement-analysis",
                            required_materials=["exabyte shipments", "nearline ASP", "gross margin", "customer agreements", "FCF", "share repurchase/debt reduction"],
                            refute_evidence="HDD 需求只是补库存，客户转向 eSSD 或新增产能削弱价格。",
                        ),
                        _memory_l3(
                            "SSD controller、固件和 enterprise SSD 方案商能否独立捕获价值，还是会被 NAND 原厂和 hyperscaler 内部化？",
                            "chokepoint_strength",
                            "financial-statement-analysis",
                            required_materials=["controller revenue", "enterprise/customer mix", "design wins", "gross margin", "customer concentration"],
                            refute_evidence="原厂整合、客户自研或价格压力导致控制器环节利润被压缩。",
                        ),
                    ],
                ),
                _l2(
                    "Q2.3",
                    "产能、设备、材料与二阶受益链",
                    "识别扩产链条中谁是必要约束，谁只是跟随 capex 的二阶 beta。",
                    [
                        _memory_l3(
                            "存储扩产最受制于 wafer starts、cleanroom、EUV/沉积刻蚀、封装还是测试设备？",
                            "chokepoint_strength",
                            "industry-report-analysis",
                            required_materials=["capex plan", "equipment order", "lead time", "tool intensity", "HBM packaging/test bottleneck"],
                            refute_evidence="设备可得性充足，真正限制来自客户需求或供应商资本纪律。",
                        ),
                        _memory_l3(
                            "设备、材料和封装链的利润弹性是否强于存储原厂，还是只获得低弹性的 capex beta？",
                            "payoff_convexity",
                            "valuation-analysis",
                            required_materials=["order/backlog", "margin", "memory customer exposure", "capex sensitivity", "valuation"],
                            refute_evidence="订单不能转化为 margin/FCF，或估值已经充分反映 capex 上行。",
                        ),
                    ],
                ),
                _l2(
                    "Q2.4",
                    "公司价值捕获和财务转化",
                    "把产品瓶颈映射到具体公司的收入、毛利率、capex、库存、现金流和股东回报，而不是停留在产业链位置。",
                    [
                        _memory_l3(
                            "Micron、SK hynix、Samsung、SanDisk/WDC、STX、SIMO 分别暴露在哪个稀缺节点，财务弹性有多大？",
                            "target_ranking",
                            "financial-statement-analysis",
                            required_materials=["segment revenue", "gross margin", "capex", "inventory", "FCF", "product exposure"],
                            refute_evidence="稀缺节点在收入或利润中占比太低，无法改变公司整体业绩。",
                        ),
                        _memory_l3(
                            "哪些公司只是存储主题暴露，哪些公司真正具备稀缺性、定价权和利润弹性？",
                            "chokepoint_strength",
                            "target-recommendation-analysis",
                            required_materials=["scarcity score", "financial exposure", "valuation", "customer concentration", "kill tests"],
                            refute_evidence="公司虽处行业上行，但产品同质化、客户议价强或估值已透支。",
                        ),
                    ],
                ),
            ],
            "Q3": [
                _l2(
                    "Q3.1",
                    "供给响应和替代路径",
                    "将新增产能、HBM 转线、中国供给、客户自研和架构优化转化为可执行反证。",
                    [
                        _memory_l3(
                            "新增 wafer capacity、HBM 转线、良率改善和 NAND/HDD 供给释放何时会打破瓶颈？",
                            "disconfirming_risk_control",
                            "industry-report-analysis",
                            required_materials=["capacity additions", "wafer starts", "yield ramp", "conversion schedule", "bit supply growth"],
                            refute_evidence="供给释放快于需求，ASP 或预付款先行走弱。",
                        ),
                        _memory_l3(
                            "中国 DRAM/NAND 供给、客户自研和内存用量优化是否会削弱海外供应商定价权？",
                            "disconfirming_risk_control",
                            "news-event-analysis",
                            required_materials=["CXMT/YMTC ramp", "export controls", "customer qualification", "architecture optimization", "domestic substitution"],
                            refute_evidence="本土供给通过认证并进入高端客户，或客户架构减少单位存储强度。",
                        ),
                    ],
                ),
                _l2(
                    "Q3.2",
                    "价格、库存、客户 capex 和周期 kill tests",
                    "把存储周期最容易出错的价格、库存和客户预算信号做成季度阈值。",
                    [
                        _memory_l3(
                            "合约价、现货价、库存天数、book-to-bill 和客户订单出现什么组合时说明周期见顶？",
                            "disconfirming_risk_control",
                            "industry-report-analysis",
                            required_materials=["contract price", "spot price", "inventory days", "book-to-bill", "customer orders"],
                            refute_evidence="价格和订单同步转弱，库存回升，供应商指引低于市场预期。",
                        ),
                        _memory_l3(
                            "云厂商 AI capex ROI、GPU/ASIC 交付和服务器订单放缓会如何传导到存储订单？",
                            "monitorability",
                            "financial-statement-analysis",
                            required_materials=["hyperscaler capex", "cloud revenue/RPO", "GPU/ASIC shipment", "server backlog", "storage supplier guidance"],
                            refute_evidence="云厂商 capex 下修或 ROI 质疑导致存储订单推迟。",
                        ),
                    ],
                ),
                _l2(
                    "Q3.3",
                    "估值隐含预期和赔率",
                    "用市场价格反推需要兑现的收入、毛利率、FCF 和周期位置，防止产业逻辑强但赔率已经消失。",
                    [
                        _memory_l3(
                            "当前市值和估值倍数隐含了什么 bit growth、ASP、毛利率和 FCF 路径？",
                            "valuation_odds",
                            "valuation-analysis",
                            required_materials=["market cap/EV", "forward multiple", "consensus revenue/EPS/FCF", "gross margin assumption", "peer valuation"],
                            refute_evidence="隐含预期要求高峰利润长期化，缺少安全边际。",
                        ),
                        _memory_l3(
                            "如果利润回到中周期，哪些标的仍有安全垫，哪些只是周期高点交易？",
                            "risk_control",
                            "valuation-analysis",
                            required_materials=["mid-cycle margin", "mid-cycle FCF", "balance sheet", "multiple range", "bear case"],
                            refute_evidence="中周期利润下估值显著高估，downside 不可控。",
                        ),
                    ],
                ),
                _l2(
                    "Q3.4",
                    "季度监控和反证阈值",
                    "为每个核心 thesis node 定义红黄绿信号，方便下一次更新直接审计。",
                    [
                        _memory_l3(
                            "每个核心瓶颈节点应该跟踪哪些季度硬指标和降级阈值？",
                            "monitorability",
                            "target-recommendation-analysis",
                            required_materials=["node-level KPI", "threshold", "data source", "update frequency", "downgrade action"],
                            refute_evidence="无法找到稳定可更新指标的节点不能进入高强度观察。",
                        ),
                    ],
                ),
            ],
            "Q4": [
                _l2(
                    "Q4.1",
                    "投资 universe 与瓶颈映射",
                    "先列全可投资证券，再按稀缺节点、财务敞口、估值和交易可获得性筛选。",
                    [
                        _memory_l3(
                            "全球和本地市场有哪些具体证券映射到 HBM、eSSD、HDD、控制器、设备和材料瓶颈？",
                            "target_ranking",
                            "target-recommendation-analysis",
                            required_materials=["ticker list", "listing market", "node exposure", "liquidity", "financial exposure"],
                            refute_evidence="证券无法交易、敞口太低、业务混合度过高或数据不可验证。",
                        ),
                        _memory_l3(
                            "哪些标的只是主题暴露，不能因为行业热度进入行动清单？",
                            "action_state",
                            "target-recommendation-analysis",
                            required_materials=["scarcity score", "valuation odds", "earnings elasticity", "risk control", "kill tests"],
                            refute_evidence="缺少稀缺性、估值赔率、利润弹性或风险可监控性中的任一核心条件。",
                        ),
                    ],
                ),
                _l2(
                    "Q4.2",
                    "排序、赔率和行动状态",
                    "将 Q1-Q3 的 verified conclusions 量化到稀缺性、错定价、利润弹性和风险控制四个核心维度。",
                    [
                        _memory_l3(
                            "哪些标的同时满足稀缺性、错定价、利润弹性和风险可控，具备最高观察强度？",
                            "target_ranking",
                            "target-recommendation-analysis",
                            required_materials=["core score dimensions", "base/bull/bear path", "valuation", "thesis kill tests", "monitoring data"],
                            refute_evidence="任一核心维度缺失时上限只能是 watch_only 或 no_action。",
                        ),
                        _memory_l3(
                            "每个核心标的的 base/bull/bear 路径、上修触发器和降级触发器是什么？",
                            "payoff_convexity",
                            "valuation-analysis",
                            required_materials=["scenario assumptions", "implied growth", "margin path", "multiple path", "downgrade triggers"],
                            refute_evidence="缺少情景赔率或触发器的标的不能进入高强度观察。",
                        ),
                    ],
                ),
                _l2(
                    "Q4.3",
                    "复盘节奏和数据补缺",
                    "把最终推荐转化为下次更新可以执行的跟踪表，而不是一次性结论。",
                    [
                        _memory_l3(
                            "下一次复盘前必须补哪些数据，哪些事件会改变标的排序？",
                            "monitorability",
                            "target-recommendation-analysis",
                            required_materials=["missing data", "event calendar", "earnings dates", "price/valuation updates", "source plan"],
                            refute_evidence="无法补齐关键数据或无法定义排序变化规则时，降低结论强度。",
                        ),
                    ],
                )
            ],
        },
        supply_chain_layers=[
            {"layer": "上游设备/材料", "products": "EUV、沉积、刻蚀、量测、硅片、封装材料", "players": "ASML、LRCX、AMAT、KLAC、材料厂商", "value_flow": "决定扩产速度和良率，是二阶受益链。"},
            {"layer": "内存制造", "products": "HBM、DDR5/LPDDR、NAND wafer、企业 SSD", "players": "SK hynix、Micron、Samsung、Sandisk/Kioxia", "value_flow": "核心利润池，AI 高端产品能转成 ASP、毛利率和现金流。"},
            {"layer": "控制器/固件", "products": "SSD controller、enterprise SSD controller、GPU boot drive", "players": "Silicon Motion、Phison、Marvell", "value_flow": "轻资产弹性节点，但护城河需要逐单验证。"},
            {"layer": "存储设备", "products": "nearline HDD、enterprise SSD、存储系统", "players": "Western Digital、Seagate、Sandisk", "value_flow": "容量需求和供给纪律决定 FCF。"},
            {"layer": "下游客户", "products": "Hyperscaler、AI lab、服务器 OEM、终端厂商", "players": "AWS、Microsoft、Google、Meta、NVIDIA 生态", "value_flow": "客户 capex ROI 是最终需求验证器。"},
        ],
        quality_rule="memory research must model workload demand into bit/ASP/mix, compare demand slope with supply response, bridge product economics to company FCF, reverse market expectations, and bind every target to kill tests",
    )


def semiconductor_hardware_playbook(goal: ResearchGoal) -> DomainPlaybook:
    q_map = {
        "Q1": "AI 基础设施是否仍在真实拉动半导体硬件需求？",
        "Q2": "产业链哪些环节最可能捕获增量利润？",
        "Q3": "哪些反证和估值风险会推翻当前机会？",
        "Q4": "哪些具体证券值得进入观察名单？",
    }
    return DomainPlaybook(
        playbook_id="semiconductor_hardware",
        research_type=goal.normalized_type(),
        q_map=q_map,
        mechanism_buckets=["demand_driver", "chokepoint", "valuation_risk", "target_mapping"],
        l2_templates={
            qid: [_l2(f"{qid}.1", q_map[qid], "默认半导体硬件机制桶。", [_l3(q_map[qid], "target_ranking" if qid == "Q4" else "future_space", "industry-report-analysis")])]
            for qid in q_map
        },
        quality_rule="hardware research must connect demand to company revenue, margin, FCF, valuation, and downgrade triggers",
    )


def optical_module_playbook(goal: ResearchGoal) -> DomainPlaybook:
    q_map = {
        "Q1": "需求：AI 数据中心网络升级如何转化为 800G/1.6T 光模块真实需求？",
        "Q2": "价值捕获：光模块产业链哪些环节具备瓶颈、定价权和财务弹性？",
        "Q3": "反证与定价：哪些技术替代、供给扩张、客户 capex 或估值信号会推翻机会？",
        "Q4": "标的：哪些具体证券最能把光模块瓶颈转化为赔率和业绩弹性？",
    }
    return DomainPlaybook(
        playbook_id="optical_module",
        research_type=goal.normalized_type(),
        q_map=q_map,
        mechanism_buckets=[
            "ai_network_demand_driver",
            "speed_transition_800g_1_6t",
            "customer_capex_and_order_visibility",
            "laser_inp_silicon_photonics_bottleneck",
            "module_integration_yield_and_certification",
            "lpo_cpo_and_architecture_substitution",
            "company_financial_conversion",
            "valuation_and_priced_in_expectations",
            "target_mapping",
        ],
        l2_templates={
            "Q1": [
                _l2(
                    "Q1.1",
                    "AI 集群网络需求传导",
                    "从 GPU/ASIC 集群、scale-out/scale-up 网络、交换机端口和光模块 attach rate 推导真实模块需求。",
                    [
                        _optical_l3(
                            "AI 训练和推理集群的 GPU/ASIC 扩张是否继续推高 800G/1.6T 光模块端口需求？",
                            "future_space",
                            "industry-report-analysis",
                            required_materials=["AI capex", "GPU/ASIC cluster scale", "switch port count", "800G/1.6T attach rate", "module shipment forecast"],
                            refute_evidence="云厂商 capex 放缓、AI 集群网络架构降低外部光模块 attach rate，或订单低于供应商扩产预期。",
                        ),
                        _optical_l3(
                            "800G 到 1.6T 的速率升级是新增需求、产品 mix 提升，还是价格换代后的 ASP 下行？",
                            "future_space",
                            "industry-report-analysis",
                            required_materials=["800G/1.6T shipment", "ASP", "mix", "customer qualification", "product roadmap"],
                            refute_evidence="1.6T 放量伴随 ASP 快速下滑或只替代 800G，不扩大收入池。",
                        ),
                    ],
                ),
                _l2(
                    "Q1.2",
                    "订单质量与客户集中",
                    "区分真实长单、客户预付款/容量锁定、短期拉货和库存风险。",
                    [
                        _optical_l3(
                            "光模块供应商的高增长由长期订单、客户认证和容量锁定支撑，还是短期抢货？",
                            "evidence_quality",
                            "financial-statement-analysis",
                            required_materials=["backlog", "long-term agreement", "customer prepayment", "capacity reservation", "customer concentration"],
                            refute_evidence="收入增长来自短期拉货，客户集中度高且没有长单或预付款支撑。",
                        ),
                        _optical_l3(
                            "NVIDIA、云厂商和交换机平台的供应链锁定是否提高需求可见度？",
                            "monitorability",
                            "news-event-analysis",
                            required_materials=["NVIDIA investment/purchase agreement", "hyperscaler capex", "switch platform roadmap", "supplier qualification"],
                            refute_evidence="核心客户取消、推迟或重新分配订单，或者平台变化使既有供应商失去份额。",
                        ),
                    ],
                ),
            ],
            "Q2": [
                _l2(
                    "Q2.1",
                    "上游激光器、InP、硅光与关键组件瓶颈",
                    "判断真正瓶颈在 EML/InP laser、硅光、DSP/driver/TIA、光芯片还是封装测试。",
                    [
                        _optical_l3(
                            "EML/InP laser、硅光芯片和光电器件是否形成供应瓶颈和定价权？",
                            "chokepoint_strength",
                            "industry-report-analysis",
                            required_materials=["laser capacity", "InP wafer", "silicon photonics", "component shortage", "gross margin"],
                            refute_evidence="关键组件扩产充足，模块厂可轻松转移供应商，组件价格快速回落。",
                        ),
                        _optical_l3(
                            "DSP、driver、TIA 和高速电芯片是否把价值转移给芯片供应商，而不是模块厂？",
                            "chokepoint_strength",
                            "industry-report-analysis",
                            required_materials=["DSP supplier share", "linear drive/LPO architecture", "bill of materials", "supplier margins"],
                            refute_evidence="模块厂掌握集成与认证，芯片成本占比下降或供应商议价能力减弱。",
                        ),
                    ],
                ),
                _l2(
                    "Q2.2",
                    "模块集成、良率、认证和产能爬坡",
                    "分析模块厂是否凭借认证、规模制造、良率和交付稳定性捕获价值。",
                    [
                        _optical_l3(
                            "模块厂的客户认证、良率、热管理和交付能力是否构成难替代壁垒？",
                            "chokepoint_strength",
                            "financial-statement-analysis",
                            required_materials=["customer qualification", "yield", "capacity ramp", "gross margin", "delivery performance"],
                            refute_evidence="认证壁垒降低，二线厂快速进入核心客户，毛利率被价格竞争压缩。",
                        ),
                        _optical_l3(
                            "Fabrinet 等代工环节是否是产能瓶颈，还是只获得低弹性的制造 beta？",
                            "payoff_convexity",
                            "financial-statement-analysis",
                            required_materials=["manufacturing revenue", "capacity utilization", "customer mix", "gross margin", "capex"],
                            refute_evidence="代工利润率稳定但弹性有限，客户转单或自建产能削弱议价能力。",
                        ),
                    ],
                ),
                _l2(
                    "Q2.3",
                    "公司财务转化和竞争格局",
                    "把中际旭创、新易盛、Lumentum、Coherent、Fabrinet、天孚通信、剑桥科技等映射到具体利润池。",
                    [
                        _optical_l3(
                            "哪些公司把 800G/1.6T 需求转化成收入、毛利率、净利率和现金流？",
                            "target_ranking",
                            "financial-statement-analysis",
                            required_materials=["revenue growth", "gross margin", "net profit", "cash flow", "product mix"],
                            refute_evidence="收入高增但毛利率、现金流或资本开支消耗恶化。",
                        ),
                        _optical_l3(
                            "国内模块龙头和海外器件/制造龙头的价值捕获差异是什么？",
                            "chokepoint_strength",
                            "target-recommendation-analysis",
                            required_materials=["company exposure", "customer mix", "component ownership", "valuation", "capacity"],
                            refute_evidence="公司只具备主题暴露，缺少关键瓶颈控制或财务弹性。",
                        ),
                    ],
                ),
            ],
            "Q3": [
                _l2(
                    "Q3.1",
                    "技术替代和架构反证",
                    "评估 LPO、CPO、硅光、铜互连、OCS 和 scale-up 网络变化对可插拔光模块的影响。",
                    [
                        _optical_l3(
                            "LPO/CPO/硅光是否会提高部分供应商壁垒，还是削弱传统可插拔模块价值？",
                            "disconfirming_risk_control",
                            "industry-report-analysis",
                            required_materials=["LPO/CPO roadmap", "silicon photonics adoption", "pluggable share", "customer qualification"],
                            refute_evidence="CPO 或平台内置光 I/O 加速落地，使传统模块 ASP 或需求低于预期。",
                        ),
                        _optical_l3(
                            "铜互连、OCS 或网络架构优化会不会减少光模块数量或改变利润池？",
                            "disconfirming_risk_control",
                            "news-event-analysis",
                            required_materials=["copper reach", "OCS deployment", "network topology", "switch roadmap"],
                            refute_evidence="架构优化显著降低光模块端口数，或价值转向交换芯片/系统商。",
                        ),
                    ],
                ),
                _l2(
                    "Q3.2",
                    "供给扩张、价格和客户议价",
                    "跟踪新增产能、价格下降、客户集中和库存反转。",
                    [
                        _optical_l3(
                            "模块和上游器件扩产会不会在 800G/1.6T 放量后造成价格竞争和毛利率下行？",
                            "disconfirming_risk_control",
                            "industry-report-analysis",
                            required_materials=["capacity expansion", "ASP trend", "gross margin", "inventory", "customer bidding"],
                            refute_evidence="产能释放快于需求，ASP 下降，毛利率和订单可见度走弱。",
                        ),
                        _optical_l3(
                            "客户集中、贸易限制和地缘政治会不会压低龙头公司的可持续估值？",
                            "risk_control",
                            "news-event-analysis",
                            required_materials=["customer concentration", "export controls", "tariff", "geographic revenue", "compliance risk"],
                            refute_evidence="核心客户分散、长协稳定且地缘风险不影响关键交付。",
                        ),
                    ],
                ),
                _l2(
                    "Q3.3",
                    "估值隐含预期和监控阈值",
                    "反推市场已经定价的增长、利润率和持续时间，定义季度降级触发器。",
                    [
                        _optical_l3(
                            "当前估值是否已经把 800G/1.6T 高增长和高利润率充分定价？",
                            "valuation_odds",
                            "valuation-analysis",
                            required_materials=["market cap", "forward PE/EV EBITDA", "consensus revenue", "margin", "historical percentile"],
                            refute_evidence="估值要求多年高增和高毛利率，安全边际不足。",
                        ),
                        _optical_l3(
                            "季度跟踪哪些硬指标可以最快发现需求、价格或份额拐点？",
                            "monitorability",
                            "target-recommendation-analysis",
                            required_materials=["quarterly revenue", "gross margin", "backlog", "capex", "customer order", "ASP"],
                            refute_evidence="无法持续获得可监控数据的标的不能给高行动状态。",
                        ),
                    ],
                ),
            ],
            "Q4": [
                _l2(
                    "Q4.1",
                    "投资 universe 与瓶颈映射",
                    "列出 A 股、美股和海外主要标的，并映射到模块、激光器、器件、代工和交换/硅光节点。",
                    [
                        _optical_l3(
                            "哪些具体证券对应光模块、激光器/器件、代工制造和硅光/芯片节点？",
                            "target_ranking",
                            "target-recommendation-analysis",
                            required_materials=["ticker list", "node exposure", "listing market", "liquidity", "financial exposure"],
                            refute_evidence="敞口太低、估值不可验证或只是宽泛 AI 主题暴露。",
                        ),
                        _optical_l3(
                            "哪些标的只是主题热度或二阶 beta，不能进入高强度观察？",
                            "action_state",
                            "target-recommendation-analysis",
                            required_materials=["scarcity score", "valuation odds", "earnings elasticity", "risk control"],
                            refute_evidence="缺少稀缺性、错定价、利润弹性或可监控风险中的任一核心条件。",
                        ),
                    ],
                ),
                _l2(
                    "Q4.2",
                    "排序、赔率和复盘计划",
                    "把 Q1-Q3 结论转化为观察强度、赔率路径和降级触发器。",
                    [
                        _optical_l3(
                            "哪些标的同时满足稀缺性、错定价、利润弹性和风险可控？",
                            "target_ranking",
                            "target-recommendation-analysis",
                            required_materials=["core score dimensions", "valuation", "base/bull/bear path", "kill tests"],
                            refute_evidence="任一核心维度不足时只能 watch_only 或 no_action。",
                        ),
                        _optical_l3(
                            "下一次复盘前必须补哪些数据，哪些事件会改变排序？",
                            "monitorability",
                            "target-recommendation-analysis",
                            required_materials=["missing data", "earnings calendar", "customer order", "valuation update", "technology roadmap"],
                            refute_evidence="没有可执行复盘数据或排序规则时，降低结论强度。",
                        ),
                    ],
                ),
            ],
        },
        supply_chain_layers=[
            {"layer": "上游光芯片/电芯片", "products": "EML/InP laser、硅光、VCSEL、DSP、driver、TIA", "players": "Lumentum、Coherent、Marvell、Broadcom、MACOM", "value_flow": "决定高速模块性能、功耗和良率，是 800G/1.6T 的关键瓶颈候选。"},
            {"layer": "光器件与组件", "products": "TOSA/ROSA、AWG、透镜、连接器、隔离器、光引擎", "players": "天孚通信、Coherent、Lumentum、光迅科技等", "value_flow": "受益于速率升级和组件数量/精度提升，价值取决于客户认证和良率。"},
            {"layer": "模块集成", "products": "400G/800G/1.6T 可插拔光模块、LPO、硅光模块", "players": "中际旭创、新易盛、Coherent、Lumentum、剑桥科技", "value_flow": "直接承接 AI 数据中心订单，利润取决于认证、规模制造、交付和 ASP 下行速度。"},
            {"layer": "代工制造", "products": "光模块和通信设备制造服务", "players": "Fabrinet、部分 EMS/ODM 厂商", "value_flow": "获得产能爬坡 beta，但是否具备稀缺性取决于客户黏性和制造良率。"},
            {"layer": "下游客户/系统", "products": "AI 服务器、交换机、GPU/ASIC 集群、云网络", "players": "NVIDIA、Google、Microsoft、Amazon、Meta、交换机厂商", "value_flow": "客户 capex、网络架构和平台路线决定最终端口需求与订单可见度。"},
        ],
        quality_rule="optical module research must connect AI cluster network demand to port count, speed transition, component/module bottlenecks, customer qualification, price erosion, valuation odds, and target-specific kill tests",
    )


def default_playbook(goal: ResearchGoal) -> DomainPlaybook:
    q_map = goal.q_map()
    return DomainPlaybook(
        playbook_id="default",
        research_type=goal.normalized_type(),
        q_map=q_map,
        mechanism_buckets=["driver", "value_capture", "risk", "target_mapping"],
        l2_templates={
            qid: [_l2(f"{qid}.1", title, "默认机制桶，需由专业提问 agent 按领域进一步细化。", [_l3(title, "target_ranking" if qid == "Q4" else "future_space", "investment-question-architect")])]
            for qid, title in q_map.items()
        },
        quality_rule="custom research needs domain playbook before evidence collection",
    )


def _l2(node_id: str, question: str, why: str, l3_questions: list[dict[str, Any]]) -> QuestionTemplate:
    return QuestionTemplate(id=node_id, question=question, why_this_depth=why, l3_questions=l3_questions)


def _l3(question: str, score_component: str, skill: str) -> dict[str, Any]:
    return {
        "question": question,
        "decision_use": f"影响 {score_component}、父节点结论和最终标的强度。",
        "required_materials": ["一手财报/公告", "行业数据或研报", "反证材料", "估值或市场预期数据"],
        "support_evidence": "能直接支持该问题判断的收入、利润、订单、价格、客户或估值证据。",
        "refute_evidence": "能推翻该问题判断的反向数据、替代供应、价格反转或估值透支证据。",
        "target_implications": "决定相关标的是 actionable_long、watch_only 还是 no_action。",
        "preferred_specialty_skill": skill,
        "score_component": score_component if score_component in SCORE_COMPONENTS or score_component == "action_state" else "future_space",
    }


def _memory_l3(
    question: str,
    score_component: str,
    skill: str,
    *,
    required_materials: list[str],
    refute_evidence: str,
    support_evidence: str = "能用具体数字把该问题从产业叙事落到需求、供给、价格、利润、现金流或估值的证据。",
    target_implications: str = "决定相关标的是否具备稀缺性、错定价、利润弹性和风险可控性。",
) -> dict[str, Any]:
    leaf = _l3(question, score_component, skill)
    leaf.update(
        {
            "decision_use": f"影响 {score_component}、父节点结论、Q4 标的排序和行动状态。",
            "required_materials": required_materials,
            "support_evidence": support_evidence,
            "refute_evidence": refute_evidence,
            "target_implications": target_implications,
        }
    )
    return leaf


def _optical_l3(
    question: str,
    score_component: str,
    skill: str,
    *,
    required_materials: list[str],
    refute_evidence: str,
    support_evidence: str = "能用具体数据把 AI 网络需求、端口数、速率升级、组件供给、订单、利润率、现金流或估值连接起来的证据。",
    target_implications: str = "决定相关标的是否具备光模块产业链瓶颈敞口、未来空间、估值赔率和风险可控性。",
) -> dict[str, Any]:
    leaf = _l3(question, score_component, skill)
    leaf.update(
        {
            "decision_use": f"影响 {score_component}、父节点结论、Q4 标的排序和行动状态。",
            "required_materials": required_materials,
            "support_evidence": support_evidence,
            "refute_evidence": refute_evidence,
            "target_implications": target_implications,
        }
    )
    return leaf
