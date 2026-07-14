from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class BomLogicStage:
    """One causal link inside a BOM question judgment model."""

    stage_id: str
    title: str
    decision_question: str
    role: str
    primary_metric: str
    cross_check_metrics: tuple[str, ...]
    refutation_metric: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage_id": self.stage_id,
            "title": self.title,
            "decision_question": self.decision_question,
            "role": self.role,
            "primary_metric": self.primary_metric,
            "cross_check_metrics": list(self.cross_check_metrics),
            "refutation_metric": self.refutation_metric,
        }


@dataclass(frozen=True)
class BomQuestionPlaybook:
    """Domain-owned question model. It contains no run-specific evidence or verdict."""

    question_id: str
    question_number: int
    question: str
    model_name: str
    purpose: str
    formula: str
    conclusion_rule: str
    stages: tuple[BomLogicStage, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "question_id": self.question_id,
            "question_number": self.question_number,
            "question": self.question,
            "model_name": self.model_name,
            "purpose": self.purpose,
            "formula": self.formula,
            "conclusion_rule": self.conclusion_rule,
            "stages": [stage.to_dict() for stage in self.stages],
        }


@dataclass(frozen=True)
class BomNodePlaybook:
    """Canonical research definition for one BOM node."""

    node_id: str
    public_name: str
    description: str
    exclusions: tuple[str, ...]
    receives: str
    produces: str
    supplies_to: str
    representative_companies: tuple[str, ...]
    financial_validation_metrics: tuple[str, ...]
    master_equations: tuple[str, ...]
    questions: tuple[BomQuestionPlaybook, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "public_name": self.public_name,
            "description": self.description,
            "exclusions": list(self.exclusions),
            "receives": self.receives,
            "produces": self.produces,
            "supplies_to": self.supplies_to,
            "representative_companies": list(self.representative_companies),
            "financial_validation_metrics": list(self.financial_validation_metrics),
            "master_equations": list(self.master_equations),
            "questions": [question.to_dict() for question in self.questions],
        }


def compute_node_playbook() -> BomNodePlaybook:
    """Return the data-center GPU/ASIC playbook used by AI-factory research."""

    questions = (
        _question(
            "compute_q1_demand",
            1,
            "当前 BOM 的需求是否会被 S 曲线放大拉动？",
            "AI 算力需求传导与弹性模型",
            "验证真实工作负载是否经过客户预算、订单和交付，最终放大为 GPU/ASIC 数量与平台价值。",
            "GPU/ASIC 需求 = AI 工作负载 x 单任务计算量 / 有效吞吐与利用率；市场价值 = accelerator 数量 x 混合 ASP + 软件/平台附着价值。",
            "工作负载、客户资本承诺、交付订单和平台收入至少四层同向，且效率提升未抵消增量计算，需求才可判为强成立。",
            (
                _stage("workload_volume", "真实 AI 工作负载", "付费用户、token、agent/coding 等真实任务是否持续增长？", "这是算力需求的业务起点，必须区别于主题热度。", "AI 用户/调用/token/任务量", ("付费席位与企业客户", "AI 编码或 agent 使用量"), "使用量、付费转化或任务频率放缓"),
                _stage("compute_intensity", "单任务计算强度", "推理、reasoning 和 agent loop 是否提高每个任务所需计算量？", "它决定任务增长能否被放大成更快的算力增长。", "每任务 token/步骤/推理时长", ("模型服务成本", "单位任务所需 GPU 时间"), "效率提升快于任务复杂度上升"),
                _stage("capacity_commitment", "客户算力资本承诺", "云厂和企业是否把工作负载转成 capex、RPO 或长期容量承诺？", "资本和合同承诺把潜在需求变成可采购需求。", "AI/数据中心 capex 与 RPO/backlog", ("PPE purchases", "云业务收入/客户预付款"), "capex 指引、RPO 或云需求下修"),
                _stage("accelerator_orders", "GPU/ASIC 与系统订单", "客户承诺是否继续形成 accelerator、AI server 和 rack-scale 订单？", "这是从预算到实物需求的关键转换。", "accelerator/AI server orders 与 backlog", ("系统出货", "供应排期/交期"), "订单取消、backlog 下行或交期缩短"),
                _stage("market_value", "平台收入与市场价值", "订单是否转成 GPU、custom ASIC 和平台收入？", "收入是需求链条可投资化的最终结果。", "Data Center/AI semiconductor revenue", ("AI processor spending", "平台收入指引"), "收入增速和指引连续下修"),
            ),
        ),
        _question(
            "compute_q2_supply",
            2,
            "供给能否跟上？",
            "GPU/ASIC 合格供给漏斗模型",
            "把设计名义产能逐层折算为同时具备先进 die、封装、HBM、板卡和平台资格的可交付算力。",
            "有效 accelerator 供给 = 合格 advanced-node die x advanced-packaging throughput x HBM allocation x board/rack yield x customer qualification。",
            "只要最慢漏斗环节低于需求斜率，供给仍偏紧；晶圆投片或单一组件扩产不能直接等同于可上线算力。",
            (
                _stage("advanced_die", "先进制程合格 die", "先进节点 wafer 和良率能否支持 accelerator 放量？", "GPU/ASIC 首先受先进节点产出约束。", "advanced-node wafer output/yield", ("先进制程收入占比", "foundry capex"), "先进节点闲置或 lead time 快速下降"),
                _stage("advanced_packaging", "先进封装吞吐", "CoWoS 类封装能否把逻辑 die 与 HBM 组合成交付芯片？", "封装是从合格 die 到高带宽 accelerator 的必要关口。", "advanced-packaging qualified capacity", ("package yield", "客户 allocation"), "封装产能显著快于订单释放"),
                _stage("memory_allocation", "HBM 配套供给", "每颗 accelerator 所需 HBM 是否按时通过资格并获得分配？", "缺少合格 HBM 时，逻辑 die 不能形成完整产品。", "qualified HBM allocation per platform", ("HBM sold-out/price-volume agreements", "HBM qualification"), "HBM 交期和 ASP 快速下降"),
                _stage("platform_ramp", "板卡、系统与平台量产", "新架构能否从样品按计划爬坡到板卡和 rack-scale 量产？", "新平台复杂度会带来电源、散热、互联和系统集成风险。", "platform volume-ramp and shipment timing", ("board/rack yield", "cloud availability"), "平台延期、返工或系统良率恶化"),
                _stage("qualified_delivery", "最终合格交付", "供应链约束后，客户真正收到并上线的算力是否仍低于需求？", "只有可上线交付才是经济供给。", "qualified shipments/lead time/sold-out status", ("AI server shipments", "客户 supply-constraint disclosure"), "交期快速缩短、库存积压或折价销售"),
            ),
        ),
        _question(
            "compute_q3_control",
            3,
            "谁控制供给？",
            "平台控制权与替代速度模型",
            "识别谁控制的不只是芯片份额，还包括软件生态、系统规格、客户资格和规模交付。",
            "有效控制权 = 合格收入/出货份额 + 软件生态 + 性能/TCO + 客户/平台锁定 - 可行替代与迁移速度。",
            "份额必须与生态、TCO、客户部署和替代路线交叉验证；PC GPU 份额不能冒充数据中心 accelerator 份额。",
            (
                _stage("qualified_share", "数据中心 AI 供给份额", "GPU、custom ASIC 和其他 accelerator 的经济份额如何分布？", "份额给出控制权结果，但必须统一数据中心口径。", "AI accelerator revenue/shipment share", ("Data Center/AI semiconductor revenue", "cloud accelerator deployment"), "龙头份额连续明显下降"),
                _stage("software_ecosystem", "软件与开发者生态", "CUDA、编译器、库和部署工具是否提高迁移成本？", "软件生态把硬件领先延伸为持续控制权。", "开发者/应用/软件栈 adoption", ("框架兼容性", "软件下载/活跃开发者"), "主流工作负载无成本迁移到开放栈"),
                _stage("performance_tco", "性能与总体拥有成本", "客户是否因性能、功耗、利用率和服务成本继续选择该平台？", "客户最终购买有效 token/训练吞吐而不是峰值规格。", "cost per token / training throughput / utilization", ("performance per watt", "cluster-scale efficiency"), "替代平台在真实负载 TCO 上持续领先"),
                _stage("customer_lock", "客户与系统规格锁定", "云厂、AI labs 和 OEM 是否围绕平台形成多年部署和 rack 规格？", "系统和资本沉没成本会延长平台控制期。", "cloud/OEM/customer platform commitments", ("rack/system design wins", "multi-year supply commitments"), "大客户削减份额或快速转向自研 ASIC"),
                _stage("substitution", "替代者与迁移速度", "AMD、TPU、Trainium 和其他 custom ASIC 能否在关键负载赶超？", "替代速度决定龙头控制权和利润池的持续时间。", "alternative accelerator revenue/deployment growth", ("second-source qualification", "workload migration share"), "替代者量产与客户迁移停滞"),
            ),
        ),
        _question(
            "compute_q4_financial",
            4,
            "是否已经财务兑现？",
            "GPU/ASIC 价量到利润现金流模型",
            "验证算力稀缺是否已经进入收入、产品 mix、利润率、订单可见度和自由现金流。",
            "财务兑现 = shipments x blended ASP + platform/software attach -> revenue -> gross/operating profit -> operating cash flow/FCF。",
            "收入、利润和现金流至少两层同步改善且指引仍有可见度，才可把产业需求上调为公司盈利结论。",
            (
                _stage("revenue", "AI accelerator 收入", "GPU 与 custom ASIC 收入是否持续快于公司其他业务？", "收入验证数量、ASP 和 mix 的综合兑现。", "Data Center/AI semiconductor revenue", ("AI server shipments", "segment growth"), "收入增速连续下修"),
                _stage("price_mix", "ASP 与平台 mix", "高端平台、rack-scale 和软件附着是否继续提高单位价值？", "单位价值决定收入弹性是否高于出货量。", "blended ASP / high-end platform mix", ("system content", "software/service attach"), "价格折让或高端 mix 下滑"),
                _stage("margin", "毛利与经营杠杆", "收入增长是否转成毛利和经营利润？", "供给控制必须最终表现为利润率和经营杠杆。", "gross margin / operating margin", ("operating income growth", "incremental margin"), "毛利连续下降且费用增长更快"),
                _stage("visibility", "订单与指引可见度", "订单、backlog 与下一季度指引是否支持继续增长？", "可见度区分一次性确认与持续兑现。", "orders/backlog/revenue guidance", ("customer prepayments", "supply commitments"), "指引下修或 backlog 取消"),
                _stage("cash_flow", "现金流质量", "会计利润是否转成经营现金流和自由现金流？", "现金流排除库存、应收和高资本占用造成的虚假兑现。", "operating cash flow / FCF", ("inventory/receivables", "cash conversion"), "FCF 恶化或营运资本占用上升"),
            ),
        ),
        _question(
            "compute_q5_pricing",
            5,
            "市场是否已定价？",
            "市场隐含算力路径与预期差模型",
            "从研究截面估值反推市场已经计入的 GPU/ASIC 增长、份额和利润率路径。",
            "赔率 = 研究情景下收入/利润/FCF 路径 - 市场隐含增长、份额、margin 与终值路径。",
            "没有 cutoff 截面价格、盈利基数和可解释的隐含路径时，不得用产业强度替代定价判断。",
            (
                _stage("asof_valuation", "研究截面估值", "截至 cutoff 的 P/E、EV/Sales、FCF yield 和市值是多少？", "这是所有赔率计算的起点。", "as-of valuation multiples", ("market cap/EV", "FCF yield"), "估值扩张而盈利预期不再上修"),
                _stage("implied_path", "市场隐含增长与利润路径", "当前价格要求收入、份额和利润率维持多久？", "反推隐含路径才能判断市场预期是否高于研究情景。", "implied revenue growth/share/margin", ("reverse DCF", "terminal margin"), "隐含路径已高于可验证行业上限"),
                _stage("expectation_revision", "盈利预期与上修空间", "公司指引和一致预期是否仍有上修空间？", "持续超预期是高估值标的继续重估的必要条件。", "revenue/EPS estimate revisions", ("guidance surprise", "consensus dispersion"), "上修停止或转为下修"),
                _stage("scenario_odds", "情景胜率与赔率", "悲观、基准和乐观情景的收益/下行是否对称？", "情景分布把产业胜率和证券赔率分开。", "scenario-implied return/downside", ("probability-weighted value", "kill-test drawdown"), "基准上行不足且悲观下行过大"),
            ),
        ),
        _question(
            "compute_q6_refutation",
            6,
            "反证是什么？",
            "GPU/ASIC 触发器、阈值与降级动作模型",
            "为工作负载、效率、替代、供应/监管、财务和估值分别保存真实逆向证据与可执行阈值。",
            "反证 = 已观察逆向来源 + 指向的因果环节 + 可量化阈值 + 检查频率 + 降级动作。",
            "泛化风险清单不算反证；至少要有真实逆向来源，并能说明它破坏六问中的哪一环。",
            (
                _stage("workload_roi", "工作负载与 ROI 反证", "AI 使用量或客户 ROI 是否不足以支持继续扩容？", "需求起点和经济回报转弱会先破坏 capex。", "AI usage/ROI/capex revision", ("cloud growth", "RPO/backlog"), "使用、ROI 与 capex 同时下修"),
                _stage("efficiency", "软件效率反证", "推理效率改善是否抵消工作负载和复杂度增长？", "更低 cost per token 可能降低单位算力需求，也可能刺激更多使用，需观察净效应。", "compute per task / cost per token", ("tokens per watt", "accelerator utilization"), "单位任务计算量持续下降且总任务增速不足"),
                _stage("custom_asic", "custom ASIC 替代反证", "TPU、Trainium 和其他 ASIC 是否削弱通用 GPU 份额和定价权？", "行业 S 曲线可以继续，但利润池可能从 GPU 龙头迁移。", "custom ASIC deployment/revenue share", ("alternative accelerator shipments", "customer workload migration"), "custom ASIC 份额连续上升并压低 GPU 增速"),
                _stage("regulatory_supply", "监管与供应反证", "出口限制、客户集中或平台延期是否削弱可服务市场？", "限制可售区域或交付时点会直接损害收入路径。", "restricted-market revenue / shipment delay", ("export-control charges", "platform availability"), "限制扩大或平台延期跨越两个季度"),
                _stage("financial_valuation", "财务与估值反证", "收入、margin、FCF 或盈利上修是否先于行业 TAM 转弱？", "证券价格通常先对增速和预期差变化反应。", "growth/margin/FCF/revision/valuation trigger", ("inventory/receivables", "guidance surprise"), "增长和上修转负而估值仍高"),
            ),
        ),
    )
    playbook = BomNodePlaybook(
        node_id="compute",
        public_name="计算加速器 / GPU / ASIC",
        description="面向数据中心训练、推理与 agent 工作负载的 GPU、custom AI ASIC/ASSP 及其平台软件；本节点不混入存储、制造、外部网络或整机集成。",
        exclusions=("HBM/DRAM", "先进晶圆制造与封装", "外部 AI 网络", "服务器/机柜系统集成"),
        receives="AI 工作负载与客户预算、芯片设计、先进制程/封装、HBM、平台软件和客户资格。",
        produces="数据中心 GPU、custom AI ASIC/ASSP、accelerator 模组和平台软件。",
        supplies_to="云厂商、AI labs、服务器/机柜系统与企业 AI 基础设施。",
        representative_companies=("NVIDIA", "AMD", "Broadcom custom ASIC", "云厂自研 ASIC"),
        financial_validation_metrics=("Data Center/AI semiconductor revenue", "orders/backlog", "gross/operating margin", "platform guidance", "OCF/FCF"),
        master_equations=(
            "所需算力 = 工作负载数量 x 单任务计算量 / 有效吞吐与利用率",
            "accelerator 需求 = 所需算力 / 单颗有效算力 x 冗余与集群系数",
            "市场价值 = accelerator 数量 x 混合 ASP + 软件/平台附着价值",
            "有效供给 = 合格先进 die x 先进封装吞吐 x HBM allocation x 系统良率 x 客户资格",
            "投资赔率 = 研究情景下盈利路径 - 市场隐含盈利路径",
        ),
        questions=questions,
    )
    validate_bom_node_playbook(playbook)
    return playbook


def hbm_node_playbook() -> BomNodePlaybook:
    """Return the HBM-only playbook used by AI-factory BOM research."""

    questions = (
        _question(
            "hbm_q1_demand",
            1,
            "当前 BOM 的需求是否会被 S 曲线放大拉动？",
            "HBM 需求传导与含量弹性模型",
            "判断 accelerator 需求是否传到 HBM，并被单颗容量、堆叠层数和高端代际占比进一步放大。",
            "HBM 需求 = accelerator 出货量 x HBM attach rate x 单颗 accelerator HBM 容量；HBM 市场价值 = HBM bit 需求 x HBM ASP。",
            "只有 accelerator 数量、单位 HBM 含量和总 HBM bit/value 三条证据同时向上，需求才可判为强成立。",
            (
                _stage("accelerator_volume", "AI accelerator 数量", "GPU/ASIC 出货或交付是否仍在增长？", "这是 HBM 的数量底座；没有 accelerator 放量，HBM 不可能仅靠规格升级长期增长。", "AI accelerator 出货/交付量", ("AI server orders/backlog", "accelerator 平台收入"), "accelerator 指引或订单下修"),
                _stage("hbm_content", "单颗 accelerator 的 HBM 容量", "每颗 accelerator 配置的 HBM GB 是否代际提升？", "这是当前节点的单位含量弹性，决定 HBM 需求是否快于 accelerator 数量。", "每颗 accelerator 的 HBM GB", ("HBM bandwidth", "HBM stack 数与层数"), "单位 HBM GB 或带宽停止提升"),
                _stage("generation_mix", "高端 HBM 代际与堆叠占比", "HBM3E 12-high、HBM4 等高价值产品的占比是否提升？", "代际和堆叠升级同时影响 bit、良率、ASP 和价值量。", "高端代际/12-high/HBM4 占比", ("客户认证进度", "单 stack 容量"), "客户回退到成熟代际或延后平台"),
                _stage("total_demand_value", "总 HBM bit 与市场价值", "数量和单位含量合并后，行业总 bit/value 是否仍有大空间？", "这是需求链的最终汇总，防止只用单一平台规格代替全市场需求。", "HBM bit growth / TAM", ("HBM value share of DRAM", "供应商 HBM revenue"), "TAM/bit forecast 连续下修"),
            ),
        ),
        _question(
            "hbm_q2_supply",
            2,
            "供给能否跟上？",
            "HBM 有效供给漏斗模型",
            "把名义 DRAM 产能逐层折算成完成堆叠、封装、测试和客户认证的合格 HBM 供给。",
            "HBM 有效供给 = DRAM wafer 投入 x die yield x stacking yield x packaging/test throughput x qualification pass rate。",
            "只要任一关键漏斗环节慢于需求斜率，HBM 仍是瓶颈；名义扩产不能直接等同于有效供给。",
            (
                _stage("wafer_allocation", "先进 DRAM wafer 分配", "可用于 HBM 的先进 DRAM wafer 是否足够？", "HBM 与 server/mobile DRAM 争夺先进 wafer，且 HBM 的 wafer trade ratio 更高。", "HBM wafer/TSV capacity", ("DRAM wafer starts", "HBM 与 DDR5 wafer value"), "先进 wafer 大规模释放或需求转弱"),
                _stage("die_yield", "DRAM die 良率", "更大 die 和更先进制程能否稳定产出合格 HBM die？", "低 die yield 会在堆叠前损失供给，并抬高单位成本。", "HBM die yield / stable yield signal", ("die size", "process-node ramp"), "良率快速改善并消除成本溢价"),
                _stage("stacking_packaging", "TSV、堆叠与封装吞吐", "后端 TSV/stacking/packaging 是否成为最慢环节？", "合格 die 仍要经过多层堆叠、测试与先进封装才能交付。", "TSV/stacking/packaging capacity", ("12-high/16-high mix", "CoWoS integration capacity"), "后端产能快于需求释放"),
                _stage("qualification", "客户认证", "新代际 HBM 是否按时通过 GPU/ASIC 客户认证？", "认证决定名义产品能否进入特定 accelerator 平台，是有效供给的最后门槛。", "qualification / commercial shipment status", ("re-sampling count", "customer count"), "认证提前完成或客户大规模多供"),
                _stage("qualified_delivery", "合格交付与合同覆盖", "最终可交付 HBM 是否仍低于客户锁定需求？", "价格、售罄、长期价量协议和交期共同验证供需平衡。", "sold-out / price-volume agreement coverage", ("HBM ASP", "shipment lead time"), "未售罄、交期缩短或 ASP 下行"),
            ),
        ),
        _question(
            "hbm_q3_control",
            3,
            "谁控制供给？",
            "合格份额与代际控制权模型",
            "识别谁控制的不是普通 DRAM wafer，而是特定代际、特定客户已经认证并能按期交付的 HBM 供给。",
            "有效控制权 = 合格出货份额 + 代际领先 + 客户认证/合同锁定 + yield/time-to-volume - second-source 速度。",
            "份额必须与资格、量产和合同交叉验证；未经认证的名义产能不算控制权。",
            (
                _stage("qualified_share", "合格出货份额", "三家供应商实际可交付 HBM 的份额如何分布？", "这是控制权的结果指标，但必须区分 bit、revenue、shipment 和单客户口径。", "HBM bit/revenue/shipment share", ("DRAM share", "NVIDIA procurement share"), "龙头份额持续下降"),
                _stage("generation_lead", "代际与客户资格领先", "谁先通过 HBM3E/HBM4 关键客户认证？", "新代际领先决定高 ASP 产品和首批 allocation。", "HBM4 qualification / shipment timing", ("HBM3E 12-high qualification", "customer platform coverage"), "竞争者先认证或龙头重新送样"),
                _stage("time_to_volume", "良率与量产速度", "谁能把样品最快转成稳定大规模交付？", "控制权最终来自稳定量产，而不是发布会规格。", "mass-production / volume-shipment status", ("stable yield", "TSV capacity"), "量产延迟或 yield 不达标"),
                _stage("contract_lock", "客户与合同锁定", "客户是否通过价量协议、采购分配或长期合作锁定供给？", "合同会降低短期可替代性，并提高收入可见度。", "price-volume agreements / sold-out status", ("customer count", "allocation share"), "客户转向三供或合同重谈"),
                _stage("second_source", "替代与 second source", "Samsung/Micron 能否削弱 SK hynix 的控制权？", "多供是客户降低单一供应商风险的自然动作，也是利润池变化的核心变量。", "second-source qualification and share change", ("HBM4 share forecast", "customer reallocation"), "替代进度停滞"),
            ),
        ),
        _question(
            "hbm_q4_financial",
            4,
            "是否已经财务兑现？",
            "HBM 价量 mix 到利润现金流模型",
            "验证 HBM 稀缺是否已经进入供应商收入、产品 mix、利润率、资本开支和现金流。",
            "HBM 财务兑现 = shipment x ASP -> HBM revenue/mix -> gross/operating margin -> operating cash flow/FCF，扣除 capex 与库存占用。",
            "只有收入、利润率和现金流至少两层同步改善，才能把 HBM 产业逻辑上调为公司财务结论。",
            (
                _stage("price_volume", "HBM 价量", "HBM shipment 和 ASP 是否共同向上？", "价量共同增长比单纯价格周期更可靠。", "HBM shipment/revenue growth", ("HBM ASP", "sold-out coverage"), "shipment 或 ASP 转弱"),
                _stage("revenue_mix", "HBM 收入与产品 mix", "HBM 是否成为公司收入和高价值产品 mix 的重要部分？", "这是节点需求向公司敞口的桥梁。", "HBM/high-value memory revenue mix", ("data-center revenue", "DRAM revenue"), "高端 mix 停止提升"),
                _stage("margin", "毛利与营业利润率", "HBM 稀缺是否转成利润率提升？", "利润率能检验供应商是否真正捕获稀缺价值。", "gross/operating margin", ("operating profit", "ASP-cost spread"), "毛利率连续下行"),
                _stage("capital_inventory", "资本开支与库存", "扩产是否需要吞噬过多资本或累积库存？", "高 capex 和库存会降低表面利润的质量。", "capex / inventory", ("capacity plan", "inventory days"), "库存增速显著快于收入"),
                _stage("cash_flow", "现金流兑现", "利润是否转成经营现金流和自由现金流？", "现金流是排除会计利润和周期性补库存噪声的最后验证。", "operating cash flow / FCF", ("customer prepayments", "net cash/debt"), "FCF 恶化或应收库存占用上升"),
            ),
        ),
        _question(
            "hbm_q5_pricing",
            5,
            "市场是否已定价？",
            "市场隐含 HBM 路径与预期差模型",
            "把研究截面的估值、盈利预测和 HBM 利润桥还原成市场已经计入的增长路径。",
            "赔率 = 研究情景下的 HBM 收入/利润路径 - 市场隐含的 HBM 份额、ASP、margin 与终值路径。",
            "缺少研究截面的估值和一致预期时，本问必须保持未完成，不能用产业强度替代赔率判断。",
            (
                _stage("asof_valuation", "研究截面估值", "截至 cutoff 的 EV、P/E、P/B、FCF yield 是多少？", "这是赔率计算的起点，必须与回测日期严格对齐。", "as-of valuation multiples", ("market cap/EV", "FCF yield"), "估值继续扩张而盈利不变"),
                _stage("implied_hbm_path", "市场隐含 HBM 路径", "当前估值隐含了多高的 HBM 收入、份额和 margin？", "只有和隐含路径比较，才能识别预期差。", "implied HBM revenue/margin/share", ("reverse DCF", "terminal margin"), "隐含路径已高于研究情景"),
                _stage("earnings_revisions", "盈利上修", "卖方/公司盈利预期是否仍在上修？", "上修速度决定强基本面能否继续超预期。", "revenue/EPS estimate revisions", ("guidance surprises", "target-price revisions"), "上修停止或转为下修"),
                _stage("scenario_odds", "情景赔率", "悲观、基准、乐观情景的收益与下行是否对称？", "情景分布把胜率和赔率分开。", "scenario-implied return and downside", ("probability-weighted value", "drawdown/kill tests"), "下行大于上行且缺少催化"),
            ),
        ),
        _question(
            "hbm_q6_refutation",
            6,
            "反证是什么？",
            "HBM 触发器、阈值与降级动作模型",
            "为需求、单位含量、供给、控制权、财务和定价分别定义可观测反证。",
            "反证 = 已观察到的逆向证据 + 可量化阈值 + 检查频率 + 对结论/标的的降级动作。",
            "风险清单不是反证；必须保存真实反向来源，并说明它破坏六问中的哪一环。",
            (
                _stage("demand_trigger", "需求反证", "accelerator/HBM 需求是否开始下修？", "需求下修会直接破坏 HBM S 曲线底座。", "accelerator/HBM demand forecast revisions", ("AI server backlog", "customer capex"), "连续两个季度下修"),
                _stage("content_trigger", "单位含量反证", "每颗 accelerator 的 HBM 容量是否停止提升？", "单位含量失速会显著降低 HBM 相对 accelerator 的弹性。", "HBM GB per accelerator generation", ("bandwidth per GPU", "stack count"), "新代际 HBM GB 不增或下降"),
                _stage("supply_trigger", "供给反证", "新增合格供给是否快于需求？", "供给释放会压缩 ASP、交期和稀缺溢价。", "qualified capacity / HBM S-D ratio", ("ASP", "lead time"), "S-D 转松且 ASP 下行"),
                _stage("control_trigger", "控制权反证", "龙头是否因竞争者认证而失去份额？", "second source 会改变利润池归属，即使行业仍增长。", "qualified share change", ("HBM4 qualification", "customer allocation"), "龙头份额连续明显下降"),
                _stage("financial_pricing_trigger", "财务与定价反证", "利润兑现或赔率是否先于行业需求恶化？", "毛利、库存、FCF 和估值往往比行业 TAM 更早暴露问题。", "margin/inventory/FCF/valuation trigger", ("earnings revisions", "price reaction"), "毛利下行、库存上升且估值仍拥挤"),
            ),
        ),
    )
    playbook = BomNodePlaybook(
        node_id="memory",
        public_name="HBM",
        description="面向 AI accelerator 的高带宽堆叠 DRAM；本节点不混入 server DDR5 或 enterprise SSD。",
        exclusions=("server DDR5", "enterprise SSD"),
        receives="GPU/ASIC 平台规格、先进 DRAM die、TSV/堆叠封装能力、客户认证和价量协议。",
        produces="HBM3E、HBM4 及后续高带宽堆叠内存。",
        supplies_to="GPU/ASIC 平台方、先进封装与 AI server 系统。",
        representative_companies=("SK hynix", "Micron", "Samsung"),
        financial_validation_metrics=("HBM shipment/revenue", "HBM ASP", "HBM mix", "gross/operating margin", "capex", "inventory", "FCF"),
        master_equations=(
            "HBM 需求 = accelerator 出货量 x HBM attach rate x 单颗 accelerator HBM 容量",
            "HBM 市场价值 = HBM bit 需求 x HBM ASP",
            "HBM 有效供给 = wafer 投入 x die yield x stacking yield x packaging/test throughput x qualification pass rate",
            "投资赔率 = 研究情景下盈利路径 - 市场隐含盈利路径",
        ),
        questions=questions,
    )
    validate_bom_node_playbook(playbook)
    return playbook


def get_bom_node_playbook(node_id: str) -> BomNodePlaybook:
    """Resolve a canonical BOM playbook without exposing adapter details."""

    factories = {
        "compute": compute_node_playbook,
        "memory": hbm_node_playbook,
    }
    try:
        factory = factories[str(node_id).strip()]
    except KeyError as exc:
        raise KeyError(f"No BOM node playbook registered for {node_id!r}") from exc
    return factory()


def validate_bom_node_playbook(playbook: BomNodePlaybook) -> None:
    required_identity_fields = {
        "node_id": playbook.node_id,
        "public_name": playbook.public_name,
        "description": playbook.description,
        "receives": playbook.receives,
        "produces": playbook.produces,
        "supplies_to": playbook.supplies_to,
    }
    missing_identity_fields = [
        name for name, value in required_identity_fields.items() if not str(value).strip()
    ]
    if missing_identity_fields:
        raise ValueError(
            "A BOM playbook must define its node boundary; missing="
            + ",".join(missing_identity_fields)
        )
    if not playbook.representative_companies:
        raise ValueError("A BOM playbook must define representative companies")
    if not playbook.exclusions:
        raise ValueError("A BOM playbook must define explicit scope exclusions")
    if not playbook.financial_validation_metrics:
        raise ValueError("A BOM playbook must define financial validation metrics")
    if not playbook.master_equations:
        raise ValueError("A BOM playbook must define node-specific master equations")
    if len(playbook.questions) != 6:
        raise ValueError("A BOM S-curve playbook must contain exactly six questions")
    expected_numbers = list(range(1, 7))
    actual_numbers = [question.question_number for question in playbook.questions]
    if actual_numbers != expected_numbers:
        raise ValueError(f"BOM question numbers must be {expected_numbers}, got {actual_numbers}")
    question_ids = [question.question_id for question in playbook.questions]
    if len(question_ids) != len(set(question_ids)):
        raise ValueError("BOM question IDs must be unique")
    for question in playbook.questions:
        if not 4 <= len(question.stages) <= 7:
            raise ValueError(f"{question.question_id} must contain 4-7 causal stages")
        stage_ids = [stage.stage_id for stage in question.stages]
        if len(stage_ids) != len(set(stage_ids)):
            raise ValueError(f"{question.question_id} stage IDs must be unique")
        for stage in question.stages:
            if not stage.primary_metric or not stage.refutation_metric:
                raise ValueError(f"{question.question_id}/{stage.stage_id} must define primary and refutation metrics")
            if not 1 <= len(stage.cross_check_metrics) <= 2:
                raise ValueError(f"{question.question_id}/{stage.stage_id} must define one or two cross-check metrics")


def validate_bom_playbook_registry(
    canonical_node_ids: tuple[str, ...],
    playbooks: tuple[BomNodePlaybook, ...],
) -> None:
    """Require exact one-to-one coverage between the BOM registry and playbooks."""

    normalized_node_ids = tuple(str(node_id).strip() for node_id in canonical_node_ids)
    if not normalized_node_ids or any(not node_id for node_id in normalized_node_ids):
        raise ValueError("The canonical BOM registry must contain non-empty node IDs")
    if len(normalized_node_ids) != len(set(normalized_node_ids)):
        raise ValueError("The canonical BOM registry contains duplicate node IDs")

    playbook_node_ids = tuple(playbook.node_id for playbook in playbooks)
    if len(playbook_node_ids) != len(set(playbook_node_ids)):
        raise ValueError("The BOM playbook registry contains duplicate node IDs")

    expected = set(normalized_node_ids)
    actual = set(playbook_node_ids)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValueError(
            f"BOM playbook coverage drift; missing={missing}, extra={extra}"
        )

    for playbook in playbooks:
        validate_bom_node_playbook(playbook)


def _question(
    question_id: str,
    question_number: int,
    question: str,
    model_name: str,
    purpose: str,
    formula: str,
    conclusion_rule: str,
    stages: tuple[BomLogicStage, ...],
) -> BomQuestionPlaybook:
    return BomQuestionPlaybook(
        question_id=question_id,
        question_number=question_number,
        question=question,
        model_name=model_name,
        purpose=purpose,
        formula=formula,
        conclusion_rule=conclusion_rule,
        stages=stages,
    )


def _stage(
    stage_id: str,
    title: str,
    decision_question: str,
    role: str,
    primary_metric: str,
    cross_check_metrics: tuple[str, ...],
    refutation_metric: str,
) -> BomLogicStage:
    return BomLogicStage(
        stage_id=stage_id,
        title=title,
        decision_question=decision_question,
        role=role,
        primary_metric=primary_metric,
        cross_check_metrics=cross_check_metrics,
        refutation_metric=refutation_metric,
    )
