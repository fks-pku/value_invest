# 半导体硬件领域投资机会研究

## 当前研究目标

研究对象是 2026-2028 年半导体硬件产业链的可投资机会，重点不是“半导体整体景气”，而是 AI 算力需求传导下哪些硬件节点具有真实收入、供给瓶颈、议价能力和可验证财务敞口。

当前约束判断：第一优先级应放在 AI 加速器/custom ASIC、HBM/高端存储、先进制程与先进封装、关键设备；中国链条重点看设备国产替代、先进封装和内存接口。最大不确定性是 AI capex ROI、存储周期、出口管制和估值拥挤。

本报告是研究观察清单，不构成买卖建议。

## 研究执行计划

1. Q1 需求：确认 AI 基础设施是否仍在真实拉动芯片、存储、网络和设备需求。
2. Q2 瓶颈：拆分 AI 加速器、custom ASIC、HBM、先进封装、设备、内存接口等节点，判断谁能捕获利润。
3. Q3 定价与风险：检查市场是否已经过度定价，以及哪些证据会证伪机会。
4. Q4 标的：把结论映射到具体证券，标注强度、理由、验证数据、催化剂和风险。

报告展示必须只按 QA 树组织：Q1 需求、Q2 瓶颈、Q3 反证、Q4 标的。评分卡、详情页、反证清单、标的建议及理由表格，都是某个问题答案的呈现形式，必须嵌入对应 QA 节点内，不作为和 Q 并列的组件。

L3 执行协议：GPT 决定每个 L3 问题要搜集和阅读哪些材料，并定义提取 schema；DeepSeek MCP 负责逐条精读这些具体材料，产出 L3 阅读答案草稿，包括事实、推论、初步判断、缺口、触发器、来源链接和支撑/反证/线索关系；GPT 再验证来源、处理冲突并写入最终 L3 答案和上抛结论。本版已对 Gartner、SEMI、NVIDIA、Broadcom、TSMC、Micron、ASML、中国链条资料，TrendForce/Wells Fargo/Microsoft/Amazon capex/ROI 材料，Samsung/TrendForce/Micron HBM4、TSMC CoWoS/CoPoS、AMAT/LRCX/KLAC 设备链材料，Meta/Marvell capex 与 AI networking/custom silicon 材料，以及 Alphabet/Oracle 云收入、RPO 和客户预付款材料完成 L3 精读或初读，并把结论压回 Q1/Q2/Q3/Q4 节点。

## Q1.1.1 需求证据链

AI 硬件需求仍是半导体硬件最清晰的主线，但不能扩展成“所有半导体都受益”。NVIDIA Data Center 收入 752 亿美元，Broadcom AI revenue 84 亿美元，Micron Cloud Memory 和 Core Data Center BU 毛利率均为 74%，TSMC 2Q26 收入指引 390-402 亿美元，ASML 指出先进节点供给限制将延续到 2026 年以后。这些证据共同说明需求已经沿 GPU/ASIC、网络、内存、先进代工和设备链条扩散。

### Q1.1.2 云厂 capex 到底买了什么，能否证明真实硬件需求？

结论：云厂 capex 不能直接等同于半导体收入，但可以拆成六类可验证传导：GPU/加速器、自研 ASIC/custom silicon、网络/互联、服务器/数据中心/组件涨价、Cloud 收入和利润、RPO/backlog 与客户预付款。Microsoft 预计 calendar 2026 capex 约 1,900 亿美元，其中约 250 亿美元来自组件价格上涨，并预计至少到 2026 年保持 capacity constrained；Amazon 过去 12 个月部署 210 万颗以上 AI chips，其中超过一半是 Trainium，并宣布从 2026 年开始部署 100 万颗以上 NVIDIA GPUs；Meta Q1 capex 198.4 亿美元，主要投向 servers、data centers 和 network infrastructure，全年 capex 指引上调至 1,250-1,450 亿美元；Alphabet Q1 Google Cloud 收入 200.28 亿美元，Cloud operating income 65.98 亿美元，FY2026 capex 指引上调至 1,800-1,900 亿美元；Oracle Q3 FY2026 RPO 5,530 亿美元，同比增长 325%，大规模 AI 合同中多数设备由客户预付款帮助采购 GPU，或由客户自购 GPU 提供给 Oracle；Marvell FY2026 收入 81.95 亿美元，同比增长 42%，Q4 data center revenue 16.51 亿美元，占收入约 74%。

判断：真实硬件需求仍在扩张，而且证据强度已经从“capex 上修”升级到“Cloud 收入增长 + RPO/backlog + 客户预付款 + 供给约束”。但必须剔除组件涨价和数据中心土建对名义 capex 的放大效应。Q1 的“需求成立”只能作为进入研究的门槛，不能直接上抛为买入结论；真正决定机会强度的是 Q2 的瓶颈、Q3 的 ROI/估值反证和 Q4 的标的财务敞口。

## Q2.1.1 瓶颈验证结论

最有研究价值的机会不是需求端最热的主题，而是供应链中最窄、最难替代、最能体现财务弹性的节点：AI 加速器平台、custom ASIC 与网络、HBM、先进封装、先进制程设备和国产替代设备。GPU/ASIC/networking、HBM、先进代工/封装和光刻设备已经有较强官方证据；中国设备和接口芯片要从验证型节点继续下钻。前端算力链不能再用“GPU 需求强”概括，必须拆成 GPU 绝对利润池、custom ASIC 增量替代和 networking/interconnect 边际短板；中国设备要拆成收入、合同负债、存货、利润弹性和高端客户验证；内存接口/CXL/PCIe 已经有新产品收入和互连毛利率证据，但还需要证明规模试用转量产。

## Q2.1 回答呈现：瓶颈评分卡

评分不是目标价或交易评级，而是研究优先级。评分由需求传导、供给稀缺、替代难度、议价能力、财务敞口、证据强度和风险扣分组成。

| 瓶颈节点 | 分数 | 强度 | 相关标的 | 详情页 |
|---|---:|---|---|---|
| AI 加速器 / custom ASIC / 网络 | 85 | A | NVIDIA、Broadcom | [详情](bottlenecks/ai_accelerator_asic_network.html) |
| HBM / 高端存储 | 84 | A- | SK hynix、Micron | [详情](bottlenecks/hbm_memory.html) |
| 先进制程 / 先进封装 | 82 | A- | TSMC、长电科技 | [详情](bottlenecks/foundry_packaging.html) |
| 半导体设备 | 76 | B+ | ASML、AMAT/LRCX/KLAC | [详情](bottlenecks/equipment.html) |
| 中国设备国产替代 | 74 | B+ | 北方华创、中微公司 | [详情](bottlenecks/china_equipment_localization.html) |
| 内存接口 / CXL / PCIe | 70 | B+ | 澜起科技 | [详情](bottlenecks/memory_interface_cxl.html) |

### Q2.1.2 HBM/高端存储是否仍是硬瓶颈？

结论：HBM 不只是“存储周期上行”，而是 AI 加速器平台交付的直接约束。Samsung Q1 2026 DS 部门收入 81.7 万亿韩元、营业利润 53.7 万亿韩元，Memory Business 因 AI 高附加值需求、ASP 上升和供给有限创纪录，并开始面向 NVIDIA Vera Rubin 的 HBM4/SOCAMM2 量产销售。Micron FY2026 Q2 Cloud Memory 和 Core Data Center BU 毛利率均为 74%，Q3 毛利率指引约 81%，说明供给紧张已经传导到利润率；Micron 还披露已在 2026 年一季度开始批量出货为 NVIDIA Vera Rubin 设计的 HBM4 36GB 12H，带宽超过 2.8TB/s，并出货 HBM4 48GB 16H 样品。TrendForce 进一步指出 HBM4 需要 Samsung、SK hynix、Micron 三家共同供应，单一供应商无法完全满足 Rubin 需求。

判断：HBM 的投资含义要分成两层。第一层是短期供给不足支撑价格和毛利，第二层是 2026Q2-H2 HBM4/HBM4E 验证、良率、带宽/能效和量产节奏决定份额迁移。降级触发器是 HBM4 验证延迟、传统 DRAM 涨价使 HBM 相对利润优势收窄、三大厂扩产后 ASP 先于出货见顶、NVIDIA Rubin 或客户认证节奏延后。

### Q2.1.3 先进封装/CoWoS 的瓶颈到底在哪里？

结论：先进封装瓶颈不是“有没有封测产能”，而是大尺寸 CoWoS、reticle size、良率、客户协同和资本开支节奏。TSMC Q1 2026 法说称当前主供给仍是 large-sized CoWoS，同时开发 very large reticle packaging 和 CoPoS；公司还强调先进封装产能也非常紧，需要与 OSAT 伙伴扩产，并指出大尺寸封装存在 mechanical stress、warpage 和 thermal limitation。TSMC 2026 年 capex 已接近 560 亿美元高端，未来三年 capex 将显著高于过去三年 1010 亿美元。这说明 AI 芯片需求已经迫使先进封装和前道产能同步扩张，但产能扩张并非简单堆设备。

判断：TSMC 是先进封装瓶颈的核心承接方，长电科技属于中国链条的验证型敞口。降级触发器是 CoWoS 扩产快于订单、先进封装价格/毛利下行、客户转向替代封装方案、OSAT 分工稀释议价权、或封装 capex 提前进入消化阶段。

### Q2.1.4 设备链是瓶颈还是滞后受益？

结论：设备链不是单一方向，AMAT 偏材料工程/沉积/先进封装，LRCX 偏刻蚀/沉积，KLAC 偏过程控制/量测，ASML 偏光刻。AMAT FY2026 Q2 收入 79.1 亿美元、毛利率 49.9%，并预计 calendar 2026 半导体设备业务增长超过 30%；Lam 2026 年 3 月季收入 58.41 亿美元、6 月季指引 66 亿美元；KLA FY2026 Q3 收入 34.15 亿美元，其中 Semiconductor Process Control 收入 30.84 亿美元。设备链已经有收入和指引支撑，但估值和出口管制使赔率弱于产业位置。

判断：设备链捕获的是扩产周期利润，最适合用订单、backlog、区域收入、服务收入和毛利率验证。降级触发器是晶圆厂 capex 下修、China revenue 受限、订单转弱、客户从抢设备转向库存消化。

### Q2.1.5 AI 加速器、custom ASIC 和 networking 谁在捕获最前端瓶颈利润？

结论：前端算力链仍是第一梯队，但内部正在分化。NVIDIA FY2027 Q1 Data Center 收入 752 亿美元，同比增长 92%；旧口径下 Data Center compute 收入 604 亿美元，同比增长 77%，networking 收入 148 亿美元，同比增长 199%。这说明 GPU/系统平台仍是绝对利润池，但 networking 的边际增速更强。Broadcom FY2026 Q1 AI revenue 84 亿美元，同比增长 106%，并指引 Q2 AI semiconductor revenue 107 亿美元，证明 custom AI accelerators 和 AI networking 已经形成第二条可量化主线。Marvell FY2026 收入 81.95 亿美元，同比增长 42%，管理层预计 FY2027 同比收入增速逐季加快，data center bookings 继续创纪录，补充了 data center interconnect/custom silicon 的第二验证点。

| 链条 | 当前证据 | 利润捕获条件 | 降级触发器 |
|---|---|---|---|
| GPU / 系统平台 | NVIDIA Data Center compute 604 亿美元，Q2 指引 910 亿美元且不含中国 Data Center compute 收入 | 中国以外需求继续填补限制缺口，Blackwell/Rubin 平台保持供给紧张，gross margin 维持高位 | compute 环比转弱、毛利率下修、云厂从 capacity constrained 转向利用率优化 |
| custom ASIC | Broadcom AI revenue 84 亿美元，Marvell FY2026 收入 81.95 亿美元且 bookings 创纪录 | hyperscaler 继续扩大定制芯片项目，外部设计服务商保持 design win、IP、封装和制造协同优势 | 大客户完全内部自研、订单取消/延期、客户集中度上升、第三方 IP 或供应链交付延误 |
| networking / interconnect | NVIDIA networking 148 亿美元，同比增长 199%；Broadcom 将 AI networking 列为 AI revenue 驱动 | 集群规模扩大带动 scale-up/scale-out 网络、交换芯片、光/电互联和 silicon photonics 升级 | networking 增速回落至 compute 以下，CSP 网络预算被压缩，一次性升级后进入消化 |

上抛到 Q2 的判断：第一梯队保留 AI 加速器/custom ASIC/networking，但内部排序必须动态化。GPU 看绝对规模和平台绑定，networking 看边际短缺，ASIC 看客户项目和外部设计服务商是否能持续捕获利润。下一步要补 NVIDIA Hyperscale/ACIE 和 compute/networking 客户拆分、Broadcom AI accelerator 与 AI networking 分项收入和毛利率、Marvell data center 产品拆分与客户集中度，以及 CSP capex 在 GPU、ASIC、networking 和数据中心土建之间的分配。

### Q2.1.6 中国设备国产替代是真瓶颈，还是政策主题？

结论：中国设备国产替代不是纯政策主题，但也不能直接等同于全球 AI 链的硬瓶颈。北方华创 2025 年收入 393.53 亿元，同比增长 30.85%，集成电路设备收入同比超过 50%；2026Q1 收入 103.23 亿元，同比增长 25.80%，经营现金流转正至 7.48 亿元，但归母净利润仅增长 3.42%。中微公司 2025 年收入 123.85 亿元，同比增长 36.62%，薄膜设备累计出货突破 300 个反应台；2026Q1 收入 29.15 亿元，同比增长 34.13%，扣非净利润增长 60.09%，但经营现金流 -1.59 亿元，研发投入占收入 31.14%。

| 公司 | 支持瓶颈的证据 | 反证/边界 | 下一步数据 |
|---|---|---|---|
| 北方华创 | 平台型设备收入规模最大，集成电路设备收入高增，经营现金流改善 | Q1 利润增速仅约 3%，存货和合同负债规模大 | 分设备线收入、合同负债转收入、存货库龄、毛利率、先进客户导入 |
| 中微公司 | 刻蚀、薄膜和 MOCVD 具备关键工艺属性，反应台量产规模和扣非利润增长较强 | Q1 经营现金流转负，高研发强度和新品验证期可能拖累现金转换 | 新设备重复订单、客户量产线占比、现金流修复、研发投入回报 |

上抛到 Q2 的判断：中国设备可以作为国产替代链条中的真瓶颈继续跟踪，但它的强度来自“高端设备量产验证 + 订单质量 + 利润弹性”，不是来自政策叙事本身。

### Q2.1.7 内存接口 / CXL / PCIe 能否从验证型瓶颈升级为可财务兑现的瓶颈？

结论：内存接口/CXL/PCIe 已经从“产品线索”进入“部分财务兑现”，但还没有达到 HBM 或 CoWoS 的硬瓶颈强度。澜起科技 2026Q1 互连类芯片收入 14.17 亿元，同比增长 24.4%；MRCD/MDB、PCIe Retimer、CKD、CXL MXC 四款新产品合计收入 2.69 亿元，同比增长 93.8%，占互连类芯片收入 19.0%；互连类芯片毛利率 71.5%。这些数据说明 DDR5、MRCD/MDB、CKD、PCIe Retimer 和 CXL MXC 正在改善收入结构和毛利率。但第二子代 MRCD/MDB 与 CXL MXC 仍有产品处于规模试用阶段，PCIe Switch 仍待工程样片流片，CXL 商用化还需要量产订单验证。

| 产品线 | 当前阶段 | 财务含义 | 升级/降级触发器 |
|---|---|---|---|
| DDR5 RCD / MRCD / MDB / CKD | 新子代出货提升，四款新产品已贡献 2.69 亿元收入 | 短期收入和毛利率的主支撑 | 新产品占比突破 25%-30%、互连毛利率维持 70% 以上；若出货增速回落则降级 |
| PCIe Retimer / AEC | PCIe 6.x/CXL 3.x Retimer 送样，AEC 方案完成系统验证和互操作测试 | 从内存接口延伸到数据中心高速互连 | 客户平台量产导入；若长期只停留在送样和验证则降级 |
| CXL MXC | CXL 3.1 MXC 向主要客户送样测试，部分产品仍处规模试用 | 中期弹性，取决于 CXL 内存扩展和池化商业化节奏 | 获得量产订单、收入单列披露；若 CXL 商业化延后则降级 |

上抛到 Q2 的判断：该节点从 B 调整为 B+ 验证型瓶颈。短期看 DDR5/CKD/MRCD/MDB，弹性看 CXL MXC 与 PCIe Retimer 量产，强度仍低于 HBM 和 CoWoS。

### Q2.1.8 如何把 Q3 季度信号回写到瓶颈评分？

结论：瓶颈评分不能只停留在静态打分。每次季度更新应先填 Q3 底稿，再把信号回写到 Q2 的需求传导、供给稀缺、财务兑现和风险扣分四个维度。绿灯只允许小幅上调或维持，黄灯冻结上调并要求补证据，红灯优先增加风险扣分；如果红灯只来自估值，则只下调赔率强度，不直接否定产业瓶颈。

瓶颈评分回写规则：

| Q2 瓶颈节点 | 当前分 / 强度 | 回写信号 | 绿灯处理 | 黄灯处理 | 红灯处理 |
|---|---:|---|---|---|---|
| AI 加速器 / custom ASIC / 网络 | 85 / A | 云厂 capex、Data Center 指引、ASIC 项目数、networking 增速、客户集中度 | 需求和财务分维持高位；若 EPS/FCF 同步上修，可提高研究优先级 | 不再上调，等待 bookings、客户项目和 capex 分项 | 若订单/指引红灯，风险扣分 +2 至 +4；若仅估值红灯，只下调赔率强度 |
| HBM / 高端存储 | 84 / A- | HBM ASP、HBM4 认证、毛利率、库存周转、经营现金流 | 维持硬瓶颈，若 ASP 和 FCF 同步改善，可提高财务兑现分 | 维持 A-，但暂停上调，重点补 ASP 和库存 | 若 ASP/库存/认证红灯，至少下调至 B+，从瓶颈利润改为周期弹性 |
| 先进制程 / 先进封装 | 82 / A- | CoWoS 产能吸收、HPC/AI 收入、客户预付款、封装毛利率 | 维持 A-，若产能仍供不应求且毛利稳定，可小幅上调供给稀缺分 | 保留评分，但要求区分 TSMC 与 OSAT 的利润捕获 | 若 CoWoS 扩产快于订单或毛利下行，下调供给稀缺和议价能力分 |
| 全球设备链 | 76 / B+ | WFE 指引、订单/backlog、服务收入、China exposure、出口许可 | 只有订单/backlog 同步改善才允许上调，不因收入强单独上调 | 维持 B+，但标记为滞后兑现，等待订单数据 | 若订单连续转弱或许可影响交付，下调至 B 或 B- |
| 中国设备国产替代 | 74 / B+ | 合同负债、存货、经营现金流、扣非利润、高端设备验证、中标 | 收入、现金流、合同负债同步改善时，维持真瓶颈并可上调财务兑现分 | 保持验证型，要求补合同负债明细和存货库龄 | 若现金流持续背离利润或高端验证停滞，降为政策主题验证中 |
| 内存接口 / CXL / PCIe | 70 / B+ | 新品收入占比、互连毛利率、CXL MXC 量产订单、Retimer/AEC 导入 | 新品占比 25%-30% 以上且毛利率 70% 以上时，考虑从验证型上调 | 维持 B+，等待 CXL/Retimer 量产订单 | 若新品占比或毛利率跌破阈值，降为产品线索型跟踪 |

本期评分变化表：

| Q2 瓶颈节点 | 上一版口径 | 本期评分 | 本期动作 | 改动依据 | 下次更新优先项 |
|---|---|---:|---|---|---|
| AI 加速器 / custom ASIC / 网络 | A，前端算力合并处理 | 85 / A | 维持核心 | NVIDIA、Broadcom、Marvell 已把 GPU、custom ASIC 和 networking 拆成可量化收入链条；Q3 capex/RPO 仍支撑需求 | NVIDIA compute/networking 拆分、Broadcom AI 客户数、Marvell bookings/backlog |
| HBM / 高端存储 | A-，硬瓶颈 | 84 / A- | 维持核心 | Micron 和 Samsung 已验证毛利与利润弹性，但 HBM4 份额、ASP 和库存仍需下一季验证 | HBM ASP、HBM4/HBM4E 认证、三大厂份额、经营现金流 |
| 先进制程 / 先进封装 | A-，CoWoS/先进节点瓶颈 | 82 / A- | 维持核心 | TSMC 法说继续支持 CoWoS 和先进封装供给紧张，但高 capex 后的吸收能力仍是反证 | CoWoS 月产能、客户预付款、先进封装毛利、OSAT 分工 |
| 全球设备链 | B+，扩产周期受益 | 76 / B+ | 冻结上调 | AMAT/Lam/KLA 收入和毛利较强，但 Q3 底稿将设备订单列为基准黄灯，不能只因收入强而加分 | ASML 新订单、AMAT/LRCX/KLAC backlog、服务收入、WFE 指引 |
| 中国设备国产替代 | B+，国产替代验证 | 74 / B+ | 维持验证 | 北方华创收入和现金流较好，中微扣非利润较强，但利润弹性、现金流和存货仍给出边界 | 合同负债、存货库龄、新签订单、高端设备客户验证 |
| 内存接口 / CXL / PCIe | B，产品线索 | 70 / B+ | 上调一级 | 澜起新产品收入占比 19.0%、互连毛利率 71.5%，说明已从产品线索进入部分财务兑现 | 新品收入占比 25%-30%、CXL MXC 量产订单、Retimer/AEC 客户导入 |

上抛到 Q2 的判断：Q2 评分现在具备动态更新逻辑。产业瓶颈分由订单、价格、毛利和现金流决定，赔率强度由估值和 EPS/FCF 修正决定。后续季度更新时，不能只改 Q4 标的强度，也要同步回写 Q2 节点评分。

## Q3.1 回答呈现：反证条件

- 大型云厂商下修 AI capex，或 AI 推理 ROI 无法支撑继续扩张。
- HBM/DRAM 供给快速释放，价格和毛利率提前见顶。
- 先进封装扩产后瓶颈缓解，封测议价权弱化。
- 设备订单低于预期，或出口管制影响核心设备和中国需求。
- 高景气标的估值已经包含 2-3 年高增长，后续财报无法兑现。

### Q3.1.1 capex/ROI 触发器

capex 上修仍然是硬件链正证据，但不能直接等同于可投资赔率。TrendForce 预计九大 CSP 2026 年 capex 约 8,300 亿美元，Wells Fargo 指出四大 hyperscaler 2026 年 capex 超过 6,500 亿美元；同时，Microsoft 披露约 250 亿美元 capex 来自组件价格上涨，Amazon Q1 2026 的 TTM free cash flow 降至 12 亿美元。新增 Alphabet 和 Oracle 后，反证体系更清楚：需求强度要拆成真实算力增量、组件涨价、前置投资、Cloud/RPO/backlog 兑现和客户预付款锁定五部分。

| 反证触发器 | 观察数据 | 影响节点 |
|---|---|---|
| CSP 下修 capex 或 2027 年共识转弱 | Microsoft/Amazon/Google/Meta capex 指引 | GPU、ASIC、网络、HBM、设备 |
| capex 上修主要来自组件涨价 | 单位 GPU/ASIC/server 出货、组件价格 | HBM、GPU、网络、服务器 ODM |
| Cloud 收入或 RPO 无法继续承接 capex | Google Cloud revenue/margin、Oracle RPO 转收入、客户预付款 | GPU、ASIC、网络、HBM、TSMC、设备 |
| FCF 压力接近投资约束 | Amazon/Microsoft/Meta/Google FCF 与 PPE 购买 | 全硬件链订单 |
| 产能叙事从短缺转向消化 | 管理层措辞、云资源利用率、backlog | NVDA、AVGO、TSM、ASML |

### Q3.1.2 估值和盈利兑现压力

结论：当前核心风险不是“需求不存在”，而是“需求存在但市场已经要求连续超预期兑现”。StockAnalysis 快照显示，NVDA Forward PE 21.32、TSM Forward PE 22.12，AVGO Forward PE 31.53，ASML Forward PE 40.51，LRCX/KLAC forward PE 约 43/41.50，多数核心标的 FCF yield 低于 2.5%。在这种赔率结构下，收入继续增长只是维持强度的必要条件；真正的升级需要 EPS/FCF 上修快于估值扩张。

| 压力来源 | 降级触发器 | 升级触发器 |
|---|---|---|
| 估值已前置增长 | EPS 上修停止但估值不回落；FCF yield 继续偏低 | 收入和 FCF 连续超预期，使 forward PE 被动下降 |
| 客户 capex 兑现压力 | 云厂从 capacity constrained 转向 utilization/optimization；全年 capex 指引下调 | AI 收入、云 backlog、推理使用量和 FCF 同时改善 |
| custom silicon 项目波动 | 主要客户延后 tape-out、取消订单、自研替代供应商 | 新客户数量增加、data center revenue 占比提升且毛利率稳定 |
| 存储周期反转 | HBM/DRAM ASP 连续回落，客户认证延迟，库存周转恶化 | HBM4/HBM4E 验证顺利、ASP 稳定、现金流跟上利润 |

### Q3.1.3 反证如何绑定到具体瓶颈节点和标的？

结论：Q3 的反证应按节点执行，而不是按主题泛泛列风险。每一个 Q2 瓶颈都要有对应的降级数据、影响标的和强度修正规则：前端算力看 capex 分项、客户项目和 data center 指引；HBM 看 ASP、认证和库存；先进封装看 CoWoS 扩产、客户预付款和毛利；设备看订单/backlog、China exposure 和服务收入；中国设备看合同负债、存货、现金流和高端验证；CXL/PCIe 看新品收入占比、毛利率和规模试用转量产。

节点级反证绑定矩阵：

| 瓶颈节点 | 影响标的 | 主要正证据 | 降级/反证触发器 | 跟踪数据 |
|---|---|---|---|---|
| AI 加速器 / custom ASIC / networking | NVDA、AVGO、MRVL | [NVIDIA Data Center 收入 752 亿美元](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx)；[Broadcom Q2 AI semiconductor 指引 107 亿美元](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial)；[Marvell data center revenue 占 Q4 收入约 74%](https://www.sec.gov/Archives/edgar/data/1835632/000183563226000006/q426_8kx1312026ex-991.htm) | 云厂 capex 下修；ASIC 项目延期或取消；networking 增速低于 compute；客户集中度上升；gross margin 或 FCF 转弱 | Data Center compute/networking 拆分、ASIC 项目数、bookings、客户集中度、CSP capex 分项 |
| 云厂 capex / ROI 源头需求 | 全硬件链，优先影响 NVDA、AVGO、MRVL、HBM、TSMC、设备链 | [九大 CSP 2026 capex 约 8,300 亿美元](https://www.trendforce.com/presscenter/news/20260506-13033.html)；[Microsoft 预计 calendar 2026 capex 约 1,900 亿美元](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3)；[Oracle RPO 5,530 亿美元](https://www.oracle.com/news/announcement/q3fy26-earnings-release-2026-03-10/) | Cloud/RPO 转收入放慢；客户预付款退潮；管理层从 capacity constrained 转为 utilization/optimization；FCF 压力迫使 capex 延后 | Cloud revenue/margin、RPO 转收入、客户预付款、AI workload 利用率、FCF 与 PPE 购买 |
| HBM / 高端存储 | SK hynix、Samsung、Micron | [Micron Cloud Memory 和 Core Data Center BU 毛利率均为 74%](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-second-quarter-fiscal-2026)；Samsung Q1 2026 DS 部门收入 81.7 万亿韩元、营业利润 53.7 万亿韩元；[TrendForce 指出 HBM4 需要三大厂共同供应](https://www.trendforce.com/presscenter/news/20260213-12918.html) | HBM/DRAM ASP 回落；HBM4/HBM4E 认证延迟；库存周转恶化；传统 DRAM 利润挤压 HBM 产能配置；FCF 跟不上利润 | HBM ASP、HBM4 认证、客户份额、产能释放、库存周转、经营现金流 |
| 先进制程 / CoWoS / 先进封装 | TSMC、ASML、长电科技 | [TSMC 强调先进封装产能紧张、CoWoS 仍为主供给并开发 very large reticle packaging 和 CoPoS](https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-04/3cef85204275f94fd111485cfdf4adb3c0263c45/TSMC%201Q26%20Transcript.pdf)；2026 capex 接近 560 亿美元高端 | CoWoS 扩产快于订单；先进封装毛利下降；客户预付款或产能预订转弱；OSAT 分工稀释议价权；大尺寸封装良率/热/翘曲问题影响交付 | CoWoS 月产能、HPC/AI 收入、客户预付款、先进封装毛利率、长电先进封装收入占比 |
| 全球设备链 | ASML、AMAT、LRCX、KLAC | [AMAT FY2026 Q2 收入 79.1 亿美元、毛利率 49.9%](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-announces-second-quarter-2026-results)；[Lam March 2026 quarter 收入 58.41 亿美元](https://investor.lamresearch.com/2026-04-22-Lam-Research-Corporation-Reports-Financial-Results-for-the-Quarter-Ended-March-29%2C-2026?asPDF=)；[KLA FY2026 Q3 收入 34.15 亿美元](https://ir.kla.com/news-events/press-releases/detail/514/kla-corporation-reports-fiscal-2026-third-quarter-results) | 晶圆厂 capex 延后；新增订单/backlog 弱于收入；China exposure 受出口许可影响；服务收入或毛利率转弱 | 订单、backlog、区域收入、服务收入、WFE 指引、出口许可说明 |
| 中国设备国产替代 | 北方华创、中微公司 | [北方华创 2026Q1 收入 103.23 亿元、经营现金流 7.48 亿元](https://disc.static.szse.cn/disc/disk03/finalpage/2026-04-30/3d01114e-ca67-4e90-bad2-9534360f2db3.PDF)；[中微公司 2026Q1 收入 29.15 亿元、扣非净利润同比增长 60.09%](https://big5.sse.com.cn/site/cht/www.sse.com.cn/disclosure/listedinfo/announcement/c/new/2026-04-28/688012_20260428_O2GX.pdf) | 合同负债下降；存货周转恶化；收入增长不转化为扣非利润或现金流；高端设备验证慢于预期；本地晶圆厂 capex 放缓 | 合同负债、存货、经营现金流、扣非利润率、关键设备客户验证、中标数据 |
| 内存接口 / CXL / PCIe | 澜起科技 | [澜起科技 2026Q1 互连类收入 14.17 亿元，新品收入 2.69 亿元、同比增长 93.8%，互连毛利率 71.5%](https://sns.sseinfo.com/resources/images/upload/202604/202604301735012391174673.pdf) | 第二代 MRCD/MDB 或 CXL MXC 规模试用迟迟不能转量产；新品收入占比不能继续提升；互连毛利率跌回 70% 以下；海外客户订单不及预期 | 四款新品分项收入、新品收入占比、CXL MXC 量产订单、PCIe Retimer/AEC 客户导入、互连毛利率 |

上抛到 Q3 的判断：这张表把 Q3 从“风险提醒”变成了“节点级降级规则”。后续更新时，不应先问半导体硬件整体还能不能看，而应先看是哪一个瓶颈节点被证伪，再同步修正 Q2 瓶颈评分和 Q4 对应标的强度。

### Q3.1.4 哪些反证触发器应该量化成季度监控阈值？

结论：第一版阈值先采用绿/黄/红灯框架，不直接转成交易动作。绿灯表示节点强度维持或可上调，黄灯表示暂停上调并等待下一季验证，红灯表示对应 Q2 瓶颈分和 Q4 标的强度需要下修。阈值当前是研究监控口径，后续要用历史分位、连续披露和同行比较校准。

季度触发器阈值表：

| 监控变量 | 当前基准 | 绿灯 | 黄灯 | 红灯 | 强度修正 |
|---|---|---|---|---|---|
| 云厂 capex 与需求质量 | TrendForce 预计九大 CSP 2026 capex 约 8,300 亿美元；Microsoft、Alphabet、Meta、Oracle 仍显示高强度 AI 基础设施投入 | 核心 CSP 维持或上修 capex，且 Cloud 收入、RPO/backlog 或客户预付款同步改善 | capex 仍高，但增长主要来自组件涨价或数据中心土建，Cloud/RPO 兑现速度放慢 | 两个以上核心 CSP 下修全年 capex，或管理层从 capacity constrained 转为 digestion/optimization | 红灯时先下修前端算力、HBM、CoWoS 和设备链研究强度 |
| 前端算力订单与客户项目 | NVIDIA Data Center 收入 752 亿美元；Broadcom AI revenue 84 亿美元；Marvell Q4 data center revenue 占比约 74% | Data Center 指引继续上修，ASIC 项目数或 networking 收入继续增长，客户集中度未恶化 | 收入增长仍在，但 bookings、客户项目或 networking 增速开始放缓 | 主要 ASIC 项目延期/取消，Broadcom 或 Marvell data center 指引低于预期，或 NVIDIA gross margin/非中国需求承接转弱 | 红灯时下修 NVDA/AVGO/MRVL 对应节点，不直接否定 HBM/设备，需要看传导滞后 |
| HBM / 高端存储瓶颈利润 | Micron 数据中心相关 BU 毛利率 74%，Q3 毛利率指引约 81%；Samsung DS 利润和 HBM4/SOCAMM2 进展验证 AI memory 弹性 | HBM4/HBM4E 认证顺利，ASP 稳定或继续上行，毛利率和现金流同步改善 | 毛利率仍高但 ASP 上行放缓，库存或产能释放数据开始走弱 | HBM/DRAM ASP 连续两个季度下行，认证延迟，库存周转恶化，或经营现金流跟不上利润 | 红灯时把 HBM 从“瓶颈利润”降级为“周期弹性”，同步下修 MU/Samsung/SK hynix 强度 |
| CoWoS / 先进封装吸收能力 | TSMC 表示先进封装产能紧张，CoWoS 仍为主供给，并开发 very large reticle packaging 和 CoPoS | CoWoS 产能扩张被客户订单吸收，HPC/AI 收入、预付款和封装毛利率维持强势 | 产能扩张继续，但客户预付款、封装毛利率或交付周期开始边际走弱 | CoWoS 扩产快于订单，价格/毛利下行，或大尺寸封装良率、热、翘曲问题影响交付 | 红灯时下修 TSMC/先进封装节点，并检查是否传导到设备订单 |
| 全球设备订单与出口约束 | AMAT、Lam、KLA 已有收入、毛利和指引支撑；ASML 把出口管制纳入指引情景 | 订单/backlog、服务收入和 WFE 指引继续改善，区域收入未因许可明显受限 | 收入仍强，但订单/backlog 先于收入放缓，China exposure 或出口许可不确定性上升 | WFE 指引下修，新增订单连续两个季度转弱，或出口许可直接影响交付 | 红灯时优先下修 ASML/AMAT/LRCX/KLAC；若中国替代受益，也需同时检查国产设备订单质量 |
| 中国设备财务兑现 | 北方华创 2026Q1 收入 103.23 亿元、经营现金流 7.48 亿元；中微公司扣非净利润同比增长 60.09% 但经营现金流为负 | 收入、合同负债、扣非利润和经营现金流同步改善，存货周转没有恶化，高端验证继续推进 | 收入增长仍在，但合同负债下降、存货上升或现金流与利润背离 | 连续两个季度出现合同负债下降、存货周转恶化、经营现金流为负，且高端验证无新增进展 | 红灯时把国产设备从“真瓶颈”降为“政策主题验证中”，下修北方华创/中微强度 |
| 内存接口 / CXL / PCIe 量产兑现 | 澜起科技 2026Q1 四款新品收入 2.69 亿元，占互连收入 19.0%，互连毛利率 71.5% | 新品收入占比升至 25%-30% 以上，互连毛利率维持 70% 以上，CXL MXC 或 Retimer 获得量产订单 | 新品收入占比维持 15%-25%，毛利率仍高，但 CXL/PCIe 仍以送样、试用为主 | 新品收入占比跌破 15%，互连毛利率跌破 65%，或 CXL MXC 迟迟不能从规模试用转量产 | 红灯时把澜起/CXL 节点降为产品线索；绿灯时可从 B+ 验证型上调 |
| 估值与盈利修正 | 多数全球核心标的 forward PE 在 20-40 倍区间，部分标的 FCF yield 低于 2.5%；中国设备和接口芯片估值容错率偏低 | EPS/FCF 上修快于股价，forward PE 被动下降，FCF yield 改善 | 股价和估值先涨，EPS 上修有限，FCF yield 仍低 | EPS 上修停止或下修，同时 forward PE 继续扩张，FCF yield 继续低于 1.5% 或现金流恶化 | 红灯时即使产业趋势仍强，也只能下调赔率强度，不能提高观察等级 |

上抛到 Q3 的判断：本表把反证从“知道有哪些风险”推进到“每季如何更新”。任一红灯连续两个季度出现，或两个以上核心节点同季转红，应把本报告整体观察强度降一级；若三个以上核心节点维持绿灯且 EPS/FCF 同步上修，则提高对应节点的研究优先级。

### Q3.1.5 季度更新时应该如何填报和上抛结论？

结论：季度更新不能先改结论再找证据，应先填 Q3 底稿，再决定是否调整 Q2 瓶颈分和 Q4 标的强度。每个红灯或黄灯必须追溯到财报、公告、法说或行业数据，并明确它影响的是基本面强度、赔率强度，还是只是需要补证据。

季度更新底稿模板：

| 监控变量 | 当前基准读数 | 本期信号 | 证据链接/来源 | 影响节点 | 上抛动作 | 待补数据 |
|---|---|---|---|---|---|---|
| 云厂 capex 与需求质量 | 九大 CSP 2026 capex 约 8,300 亿美元；Microsoft/Alphabet/Oracle 仍显示 AI 基础设施约束和 RPO 支撑 | 基准绿 | [TrendForce](https://www.trendforce.com/presscenter/news/20260506-13033.html)、[Microsoft](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3)、[Oracle](https://www.oracle.com/news/announcement/q3fy26-earnings-release-2026-03-10/) | Q1 需求、Q2 前端算力/HBM/设备、Q4 全球链条 | 维持需求主线，但继续要求 Cloud/RPO/FCF 共同验证 | 2026Q2/Q3 capex 指引、AI 收入、RPO 转收入、客户预付款 |
| 前端算力订单与客户项目 | NVIDIA Data Center 752 亿美元；Broadcom AI revenue 84 亿美元；Marvell Q4 data center revenue 16.51 亿美元 | 基准绿 | [NVIDIA](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx)、[Broadcom](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial)、[Marvell](https://www.sec.gov/Archives/edgar/data/1835632/000183563226000006/q426_8kx1312026ex-991.htm) | Q2.1.5、Q4.1.5 | 维持 NVDA/AVGO/MRVL 前端链条优先级，MRVL 受估值和 FCF 约束 | NVIDIA compute/networking 拆分、Broadcom AI 客户数、Marvell bookings/backlog |
| HBM / 高端存储 | Micron 数据中心相关 BU 毛利率 74%，Q3 毛利率指引约 81%；Samsung DS 利润强 | 基准绿 | [Micron](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-second-quarter-fiscal-2026)、Samsung Q1 2026、[TrendForce HBM4](https://www.trendforce.com/presscenter/news/20260213-12918.html) | Q2.1.2、Q4 HBM 组合 | 维持 HBM 瓶颈利润判断，但用 ASP/库存/FCF 防止误判周期高点 | HBM ASP、HBM4/HBM4E 认证、三大厂客户份额、库存周转 |
| CoWoS / 先进封装 | TSMC 表示 CoWoS 仍为主供给且先进封装产能紧张；2026 capex 接近 560 亿美元高端 | 基准绿 | [TSMC Q1 2026 transcript](https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-04/3cef85204275f94fd111485cfdf4adb3c0263c45/TSMC%201Q26%20Transcript.pdf) | Q2.1.3、TSM/长电 | 维持先进封装为硬瓶颈，但长电仍只按验证型处理 | CoWoS 月产能、先进封装毛利、客户预付款、长电先进封装收入 |
| 全球设备订单 | AMAT/Lam/KLA 收入和毛利强，但设备订单天然滞后于晶圆厂 capex 周期 | 基准黄 | [AMAT](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-announces-second-quarter-2026-results)、[Lam](https://investor.lamresearch.com/2026-04-22-Lam-Research-Corporation-Reports-Financial-Results-for-the-Quarter-Ended-March-29%2C-2026?asPDF=)、[KLA](https://ir.kla.com/news-events/press-releases/detail/514/kla-corporation-reports-fiscal-2026-third-quarter-results) | Q2.1.4、设备组合 | 维持设备链 B+，但不因收入强直接上调，等待订单/backlog | ASML 新订单、AMAT/LRCX/KLAC backlog、服务收入、WFE 指引 |
| 中国设备财务兑现 | 北方华创收入和现金流较强；中微扣非利润强但经营现金流为负 | 基准黄 | [北方华创](https://disc.static.szse.cn/disc/disk03/finalpage/2026-04-30/3d01114e-ca67-4e90-bad2-9534360f2db3.PDF)、[中微公司](https://big5.sse.com.cn/site/cht/www.sse.com.cn/disclosure/listedinfo/announcement/c/new/2026-04-28/688012_20260428_O2GX.pdf) | Q2.1.6、Q4 中国设备 | 保持 B+ 验证型，不因国产替代叙事上调 | 合同负债、存货库龄、新签订单、高端设备客户验证、经营现金流 |
| 内存接口 / CXL / PCIe | 澜起四款新品收入 2.69 亿元、占互连收入 19.0%，互连毛利率 71.5% | 基准黄 | [澜起 2026Q1 投资者活动记录](https://sns.sseinfo.com/resources/images/upload/202604/202604301735012391174673.pdf) | Q2.1.7、澜起科技 | 维持 B+ 验证型，等待 CXL/Retimer 从试用转量产 | 四款新品分项收入、CXL MXC 量产订单、Retimer/AEC 客户导入 |
| 估值与盈利修正 | 多数核心标的估值不低，部分 FCF yield 低于 2.5%；中国设备/接口芯片估值容错率偏低 | 基准黄 | [StockAnalysis](https://stockanalysis.com/stocks/nvda/financials/ratios/)、A 股估值快照 | Q3.1.2、Q4.1.3、Q4.1.5 | 强度上调必须同时有 EPS/FCF 上修，不能只看产业趋势 | 一致预期 EPS 修正、历史估值分位、FCF yield、订单与收入 beat/miss |

填报规则：每次季度更新先填本表，再更新 Q2 瓶颈分和 Q4 标的强度。红灯必须写明证据链接、影响节点和动作性质；黄灯必须写清下一季需要补的关键数据；绿灯只提高研究优先级，不自动生成交易结论。

## Q4.1 回答呈现：标的观察清单

| 标的 | 瓶颈节点 | 强度 | 主要理由 | 关键风险 |
|---|---|---:|---|---|
| NVIDIA / NVDA | AI 加速器、系统平台、网络 | A | AI 硬件收入兑现最强，平台覆盖 GPU、网络、系统和软件生态 | 估值、出口限制、客户 capex ROI、ASIC 替代 |
| Broadcom / AVGO | custom AI ASIC、AI networking | A- | GPU 之外的第二条 AI silicon 主线，受益于 hyperscaler 自研 ASIC | 客户集中、项目收入波动 |
| Marvell / MRVL | custom silicon、AI data center interconnect、networking | B+ | FY2026 收入 81.95 亿美元，同比增长 42%；Q4 data center revenue 占收入约 74% | 客户集中、客户自研/垂直整合、订单取消或延期 |
| TSMC / TSM, 2330.TW | 先进制程、先进封装 | A | AI 芯片设计最终落到先进节点与 CoWoS/封装产能 | 地缘政治、客户集中、capex 回报 |
| ASML | EUV/DUV 光刻设备 | A- | 先进制程最关键设备瓶颈 | 出口管制、订单周期、中国收入结构 |
| SK hynix / 000660.KS | HBM、高端 DRAM | A- | HBM 是 AI 加速器出货核心约束之一 | 供给释放、竞争、存储周期 |
| Samsung Electronics / 005930.KS | HBM4、AI memory、foundry base-die | A- | Q1 2026 DS 部门利润和 HBM4/SOCAMM2 进展验证 AI memory 弹性 | HBM4 验证、foundry 亏损、与 SK hynix/Micron 竞争 |
| Micron / MU | HBM、数据中心 DRAM/eSSD | B+ | 存储周期修复叠加 HBM 增量，弹性强 | HBM 份额、价格周期、库存 |
| AMAT/LRCX/KLAC | 沉积、刻蚀、量测设备 | B+ | 若设备支出继续扩张，过程设备和量测控制受益 | capex 周期、出口限制 |
| 北方华创 / 002371.SZ | 国产半导体设备平台 | B+ | 2026Q1 收入 103.23 亿元、经营现金流转正，但利润增速明显低于收入 | PE 约 69.8x 下利润弹性不足、合同负债和存货 |
| 中微公司 / 688012.SH | 刻蚀、薄膜/MOCVD 设备 | B+ | 2026Q1 收入增长 34.13%，扣非净利润增长 60.09%，研发投入强 | 静态 PE 约 146x、经营现金流转负 |
| 长电科技 / 600584.SH | 封测与先进封装 | B | 2026Q1 利润增长 42.74%，成熟工厂订单较饱满 | 收入同比下降、存货上升、先进封装收入需验证 |
| 澜起科技 / 688008.SH | DDR5、PCIe/CXL、服务器接口 | B+ | 2026Q1 毛利率 69.8%，DDR5/CXL/PCIe 新品驱动增长 | 静态 PE 约 148.62x、扣非增速需匹配估值 |

### Q4.1.1 估值/赔率快照

估值层会改变观察顺序。NVDA 和 TSM 的基本面最强，远期 PE 已被盈利增长部分消化，赔率仍可跟踪；AVGO、ASML、LRCX、KLAC 的瓶颈地位很强，但当前估值对订单延续和盈利兑现要求更高；MU 的远期 PE 最低，但 FCF yield 偏低且存储周期反转风险大，不能只按低 forward PE 判断便宜。中国链条已补初步估值快照，但不同平台口径差异较大，只用于约束赔率。

| 标的 | 估值快照 | 赔率修正 |
|---|---|---|
| NVDA | PE 32.56；Forward PE 21.32；FCF yield 2.31% | 基本面 A，赔率 B+ |
| AVGO | PE 82.22；Forward PE 31.53；FCF yield 1.45% | 基本面 A-，赔率 B |
| TSM | PE 31.81；Forward PE 22.12；FCF yield 1.77% | 基本面 A，赔率 B+ |
| ASML | PE 53.23；Forward PE 40.51；FCF yield 1.69% | 基本面 A-，赔率 B- |
| MU | PE 43.67；Forward PE 9.85；FCF yield 0.98% | 基本面 B+，赔率 B+ |
| AMAT | PE 42.16；Forward PE 30.60；FCF yield 1.50% | 基本面 B+，赔率 B- |
| LRCX | PE 约 60；Forward PE 约 43；FCF yield 1.50% | 基本面 B+，赔率 C+ |
| KLAC | PE 55.40；Forward PE 41.50；FCF yield 1.57% | 基本面 B+，赔率 B- |
| 中国链条 | 北方华创 PE 约 69.8x；中微静态 PE 约 146x；长电 PE TTM 约 50-53x；澜起静态 PE 约 148.62x | 整体维持验证型，不能用国产替代跳过赔率约束 |

### Q4.1.2 标的档案如何从 Q2 瓶颈上抛？

| 标的组合 | 对应瓶颈 | 当前处理 | 必须继续验证 |
|---|---|---|---|
| NVDA / AVGO / MRVL | AI 加速器、custom ASIC、网络 | 强证据核心链，但必须用 capex ROI 和客户集中度修正 | 数据中心收入拆分、ASIC 项目数、data center revenue、云厂商 capex、gross margin |
| TSM / ASML | 先进制程、CoWoS、EUV/DUV | 瓶颈质量强，但 capex 和订单周期会影响赔率 | CoWoS 产能、先进节点需求、ASML order/backlog、出口许可 |
| SK hynix / Samsung / MU | HBM、数据中心内存、eSSD | 短期利润弹性最直接，但周期反转风险最高 | HBM4/HBM4E 验证、ASP、供给释放、客户份额、库存 |
| AMAT / LRCX / KLAC | 沉积、刻蚀、量测、过程控制 | 扩产周期受益组合，但估值要求订单继续兑现 | WFE 指引、订单、区域收入、服务收入、China exposure |
| 北方华创 / 中微公司 | 国产设备 | 中国链条最清晰的国产替代映射，但需要拆分收入、扣非利润、现金流和合同负债 | 高端设备收入、新签订单、客户导入、存货、合同负债、经营现金流 |
| 长电科技 / 澜起科技 | 先进封装、内存接口/CXL | 验证型机会，长电看先进封装能否重新拉动收入，澜起看 DDR5/CXL 新品能否持续放量 | AI/HPC 客户、先进封装毛利、CXL/DDR5 收入、平台导入、产品结构 |

### Q4.1.3 估值、EPS 和 FCF 敏感性会如何改变标的强度？

结论：Q4 不能只按产业地位排序，还要把每个标的拆成三列：趋势强度、财务兑现强度、赔率强度。MRVL 的 AI data center 敞口变强，但 PE 68.64、Forward PE 45.50、FCF yield 0.96%、EV/FCF 105.00，说明它需要 data center revenue、bookings、客户项目和 FCF 转换继续超预期。Samsung 和 SK hynix 的 forward PE 看起来更低，Samsung Forward PE 6.08，SK hynix 12m forecast PE 约 6.1/Forward P/E 约 5.87，但这不能直接等同于低估，因为市场正在用 HBM 周期高点给利润定价。

| 标的/组合 | 赔率证据 | 升级条件 | 降级条件 |
|---|---|---|---|
| MRVL | Forward PE 45.50；FCF yield 0.96%；EV/FCF 105.00 | data center revenue 和 bookings 继续超预期，FCF yield 改善 | 客户项目延期、订单取消、FCF 转换弱 |
| Samsung | Forward PE 6.08；FCF yield 2.90%；EV/EBITDA 12.91 | HBM4E 样品转量产，foundry 亏损收窄，FCF 改善 | HBM4 认证弱、foundry 拖累、DRAM ASP 见顶 |
| SK hynix | 12m forecast PE 约 6.1；P/FCF 33.68；EV/EBITDA 14.61 | HBM 份额维持领先，ASP 稳定，FCF 转换跟上利润 | HBM 供给释放快于需求，份额被侵蚀，P/FCF 继续高位 |
| MU | Forward PE 9.85；FCF yield 0.98% | HBM4 出货放量，毛利率保持高位，FCF yield 上行 | 存储价格反转，库存重建过快，HBM 份额不及预期 |
| NVDA / TSM | NVDA Forward PE 21.32、FCF yield 2.31%；TSM Forward PE 22.12、FCF yield 1.77% | EPS/FCF 上修快于股价，forward PE 被动下降 | 云厂 capex 放缓，毛利率下修，CoWoS/先进节点进入消化 |

上抛到 Q4 的判断：当前清单应从“产业链强弱排序”升级为“产业链强度 + 盈利兑现 + 赔率容错率”。MRVL、AVGO、ASML、设备链属于高质量但低容错率；Samsung/SK hynix/MU 属于低 forward PE 但高周期反证；NVDA/TSM 是基本面质量最强但仍需 EPS/FCF 上修延续。

### Q4.1.4 中国链条的财务兑现、订单质量和估值容错率如何修正强度？

结论：中国链条不能只用“国产替代”作为强度来源。北方华创和中微公司是国产设备主线，但一个问题是利润弹性弱于收入，另一个问题是经营现金流与利润背离；长电科技是先进封装验证线，但 Q1 收入没有增长，利润更多来自产能利用率和产品结构修复；澜起科技是 DDR5/CXL 接口芯片验证线，毛利率和产品结构最强，但估值容错率最低。

| 标的 | Q1 财务兑现 | 订单/运营质量 | 估值容错率 | 观察强度修正 |
|---|---|---|---|---|
| 北方华创 | 收入 103.23 亿元，同比 +25.80%；归母净利润同比 +3.42%；经营现金流转正至 7.48 亿元 | 合同负债约 42.03 亿元，存货约 286.03 亿元 | PE 约 69.8x，收入增长能解释部分溢价，但利润弹性不足 | B+ 维持，从平台龙头下钻为利润弹性待验证 |
| 中微公司 | 收入 29.15 亿元，同比 +34.13%；扣非净利润 4.78 亿元，同比 +60.09% | 经营现金流 -1.59 亿元；研发投入占收入 31.14%；超过 8300 个反应台量产 | 静态 PE 约 146x，要求高增长和现金流改善同时兑现 | B+ 维持，质量高但容错率低 |
| 长电科技 | 收入 91.71 亿元，同比 -1.76%；归母净利润 2.90 亿元，同比 +42.74% | 成熟工厂订单较饱满，产能利用率高位；存货升至 44.08 亿元 | PE TTM 约 50-53x，对收入未增长的封测公司不低 | B 维持，更像利润率修复而非需求放量 |
| 澜起科技 | 收入 14.61 亿元，同比 +19.5%；毛利率 69.8%；扣非净利润同比 +20.1% | DDR5 RCD、MRCD/MDB、PCIe Retimer、CKD、CXL MXC 新品放量 | 静态 PE 约 148.62x、PB 约 15.94x | B+ 维持，产品结构证据增强但赔率约束明显 |

上抛到 Q4 的判断：中国链条不再按一个篮子处理。北方华创和中微公司仍是国产设备主线，但需要订单和现金流继续证明；澜起科技的产品结构证据更强，但估值容错率最低；长电科技必须先证明先进封装能够重新拉动收入。

### Q4.1.5 如何把 Q3 红黄绿信号转成标的观察强度调整？

结论：Q4 的标的表不能是静态名单。每个标的组合都要绑定 Q3 的红黄绿触发器：绿灯只提高研究优先级，不等于交易指令；黄灯维持但不加分；红灯触发强度下修和证据复核。若某一标的组合对应的两个核心信号同季红灯，观察强度下修一级；若两个季度连续红灯，下修两级或移出核心观察。

标的强度动态调整表：

| 标的组合 | 当前强度 | 绑定 Q3 信号 | 上调条件 | 下调条件 | 下一步动作 |
|---|---|---|---|---|---|
| NVDA / AVGO / MRVL | A / A- / B+ | 云厂 capex、前端算力订单、ASIC 项目、networking 增速、估值与 FCF | Data Center 指引继续上修，ASIC 项目数增加，networking 增速维持，EPS/FCF 上修消化估值 | 两个以上 CSP 下修 capex，ASIC 项目延期或取消，Broadcom/Marvell data center 指引弱于预期，FCF yield 恶化 | NVDA 保持核心，AVGO/MRVL 用项目和 FCF 决定是否从高质量低容错降为观察型 |
| TSM / ASML | A / A- | CoWoS 吸收能力、先进节点需求、EUV/DUV 订单、出口许可、客户 capex | CoWoS 产能被客户订单吸收，HPC/AI 收入占比继续提高，ASML 订单/backlog 改善 | CoWoS 扩产快于订单，先进封装毛利下行，ASML 新订单转弱或出口许可影响交付 | TSM 看封装与先进节点双瓶颈，ASML 看订单周期；红灯时先下修赔率 |
| SK hynix / Samsung / MU | A- / A- / B+ | HBM ASP、HBM4/HBM4E 认证、客户份额、库存、经营现金流 | HBM4 认证顺利，ASP 稳定，毛利率和 FCF 同步改善，库存周转稳定 | HBM/DRAM ASP 连续两个季度下行，库存恶化，认证延迟，FCF 跟不上利润 | 绿灯时保留利润弹性组合；红灯时从瓶颈利润降为存储周期弹性 |
| AMAT / LRCX / KLAC | B+ | WFE 指引、订单/backlog、区域收入、服务收入、出口限制 | 订单/backlog 和服务收入继续改善，先进逻辑与存储扩产同时支撑设备需求 | WFE 指引下修，订单连续两个季度转弱，China exposure 受许可限制，毛利率回落 | 设备组合只在订单确认时上调；若收入强但订单弱，视为滞后兑现 |
| 北方华创 / 中微公司 | B+ | 合同负债、存货、经营现金流、扣非利润、高端设备验证、中标数据 | 收入、合同负债、扣非利润和经营现金流同步改善，高端设备验证推进 | 合同负债下降、存货周转恶化、现金流持续背离利润，高端验证无新增进展 | 绿灯时维持国产设备真瓶颈；红灯时降为政策主题验证中 |
| 长电科技 / 澜起科技 | B / B+ | 先进封装收入、AI/HPC 客户、DDR5/CXL/PCIe 新品收入、毛利率、估值消化 | 长电先进封装重新拉动收入；澜起新品收入占比升至 25%-30% 以上且互连毛利率维持 70% 以上 | 长电收入继续不增长或存货上升；澜起新品占比跌破 15%、互连毛利率跌破 65% 或 CXL 量产延后 | 长电先看收入修复，澜起先看新品兑现；红灯时从验证型机会降为线索型跟踪 |

上抛到 Q4 的判断：Q4 现在不只是给出标的清单，而是给出一套动态调仓前的研究强度调整机制。本报告仍不输出交易指令，但可以明确哪些数据会让某个标的组合升级、维持或降级。

## 来源

核心来源见 `evidence.jsonl`；HTML 报告中每个 QA 节点附有蓝色源链接。

## 本轮深化补充：TODO 四个核心节点

### Q4.1.6 标的研究优先级矩阵

这是研究覆盖优先级，不是买卖建议。排序依据是瓶颈暴露、财务兑现证据、赔率约束、主要反证和下一季必查数据。

| 覆盖优先级 | 标的/组合 | 瓶颈暴露 | 财务兑现证据 | 赔率约束 | 主要反证 | 下一季必查数据 |
|---|---|---|---|---|---|---|
| 核心跟踪 | NVDA、TSM | GPU/AI networking、先进制程、CoWoS/先进封装 | NVDA Data Center 收入、TSMC HPC/先进封装供给约束 | 估值、客户集中、CoWoS 扩产吸收、EPS/FCF 修正速度 | 云厂 capex 下修、CoWoS 毛利下行、Data Center 指引不及预期 | compute/networking 拆分、Blackwell/Rubin 交付、CoWoS 产能和 HPC/AI 收入占比 |
| 高优先级 | AVGO、ASML、HBM 组合 | custom ASIC、AI networking、光刻设备、HBM/HBM4 | AVGO AI revenue、ASML backlog、HBM 认证和毛利弹性 | 客户集中、订单波动、HBM ASP 和库存周期 | ASIC 项目延期、设备订单转弱、HBM ASP 连续下行 | AVGO AI 客户数、ASML net bookings、HBM ASP/份额/库存 |
| 验证型 | MRVL、AMAT/LRCX/KLAC、中国设备链、澜起科技 | AI interconnect、WFE、国产设备、DDR5/CXL/PCIe | MRVL data center 占比、设备收入与毛利、中国设备现金流、澜起新品收入 | 订单滞后、国产设备订单质量、澜起估值容错率 | backlog 不跟、现金流背离利润、CXL 量产延后 | MRVL bookings、设备 backlog、合同负债/存货库龄、CXL/Retimer 量产订单 |
| 线索型 | 长电科技 | 先进封装/OSAT | 产业位置成立，但近期收入和增长证据不足 | 收入修复、毛利率、客户结构 | 先进封装收入不放量、存货上升、毛利率承压 | AI/HPC 客户、先进封装订单、产能利用率和分项收入 |

### Q1.1.3 capex 质量拆分

| capex 类型 | 当前证据 | 对半导体硬件的含义 | 不能证明什么 | 下一季必查数据 |
|---|---|---|---|---|
| 真实算力硬件 | NVIDIA、Broadcom、Marvell、Oracle RPO/预付款 | 直接支撑 GPU、ASIC、networking、HBM、先进制程和封装需求 | 不能证明所有供应商利润率同步扩张，也不能证明估值合理 | GPU/ASIC 出货、AI 客户项目、RPO 转收入、客户预付款 |
| 组件涨价 | Microsoft 约 250 亿美元 capex 来自组件价格上涨，Meta 披露组件涨价压力 | 说明 HBM、服务器零部件和网络设备仍有供需紧张 | 名义 capex 增长不能等同于芯片数量增长 | price/volume 拆分、HBM ASP、GPU/ASIC 单价和出货量 |
| 数据中心土建/电力网络 | Meta servers/data centers/network infrastructure，Alphabet Cloud 容量约束 | 支持 AI 基础设施建设，但半导体弹性需二次拆分 | 不能直接证明 GPU/ASIC/HBM 收入同步增长 | 完工节奏、设备装机率、功率利用率和芯片配置 |
| RPO/backlog/客户预付款 | Oracle RPO 与 AI 合同采购 GPU 机制 | 比 capex 总额更接近真实需求质量 | RPO 仍需转收入，采购和交付存在风险 | RPO 转收入、预付款余额、GPU sourcing、合同延后 |
| 现金流压力 | Amazon FCF 压力和 PPE 购买净额增加 | AI 投资是真实现金支出 | 不能证明客户会长期不计 ROI 扩张 | FCF、capex intensity、AI 收入、利用率 |

### Q2.1.9 瓶颈节点详情页补强

| 节点 | 产业链位置 | 约束变量 | 谁捕获利润 | 财务科目映射 | 降级触发器 | 待补数据 |
|---|---|---|---|---|---|---|
| AI 加速器 / custom ASIC / networking | 算力集群前端芯片、ASIC、交换和互联 | GPU 供应、ASIC 客户项目、AI networking、封装产能 | NVDA、AVGO、MRVL | Data Center revenue、AI semiconductor revenue、bookings/backlog、gross margin | capex 下修、ASIC 延期、networking 放缓、客户集中恶化 | compute/networking 拆分、ASIC 项目数、客户订单和 backlog |
| HBM / 高端存储 | GPU/ASIC 配套高带宽内存 | HBM4/HBM4E 认证、良率、ASP、客户份额 | SK hynix、Samsung、Micron | HBM/DRAM revenue、gross margin、inventory、OCF | ASP 下行、库存恶化、认证延迟、FCF 跟不上利润 | HBM ASP、客户份额、库存周转、认证节奏 |
| CoWoS / 先进封装 | 先进代工和异构集成封装瓶颈 | CoWoS 月产能、客户预付款、良率和毛利 | TSM 为主，OSAT 单独验证 | HPC/AI revenue、advanced packaging capex、客户预付款、gross margin | 扩产快于订单、封装毛利下行、OSAT 收入不增长 | CoWoS 产能、客户吸收率、长电先进封装收入 |
| 全球设备链 | 光刻、刻蚀、沉积、量测检测 | WFE、订单/backlog、出口许可、先进节点扩产 | ASML、AMAT、LRCX、KLAC | equipment revenue、orders/backlog、service revenue、gross margin | 订单连续转弱、许可影响交付、收入强但 backlog 不跟 | ASML net bookings、设备 backlog、WFE 指引 |
| 中国设备 | 国产设备替代 | 客户验证、中标、新签订单、合同负债和存货 | 北方华创、中微公司 | 收入、扣非利润、合同负债、经营现金流、存货 | 现金流背离利润、合同负债下降、高端验证停滞 | 订单结构、合同负债明细、存货库龄、高端验证 |
| 内存接口 / CXL / PCIe | DDR5、MRCD/MDB、Retimer、CXL MXC | 平台认证、量产订单、客户导入、CXL 商业化 | 澜起科技 | 新品收入占比、互连毛利率、分项订单 | 新品占比回落、毛利率跌破阈值、CXL 量产延后 | CXL/Retimer 量产订单、四款新品分项收入 |

### Q3.1.6 反证执行清单

| 审计项 | 数据来源 | 绿灯标准 | 黄灯标准 | 红灯标准 | 影响 Q2 节点 | 影响 Q4 标的 |
|---|---|---|---|---|---|---|
| 云厂 capex 质量 | CSP 财报、法说、RPO、Cloud revenue、FCF | capex、Cloud/RPO、FCF 或收入转化同向改善 | capex 上修但 FCF 或 RPO 转化偏弱 | capex 下修或 RPO/Cloud 增长明显放缓 | 前端算力、HBM、CoWoS、设备 | NVDA、AVGO、MRVL、TSM、HBM 组合 |
| HBM ASP / 库存 | Micron、Samsung、SK hynix、TrendForce | ASP 稳定或上行，库存健康，认证推进 | ASP 边际转弱但认证仍推进 | ASP 连续下行、库存恶化或认证延迟 | HBM/高端存储 | HBM 组合 |
| 设备订单 / backlog | ASML、AMAT、LRCX、KLAC | 订单/backlog 与收入同步改善 | 收入强但订单弱 | 订单连续两季转弱或许可影响交付 | 全球设备链 | ASML、AMAT/LRCX/KLAC |
| 估值与 EPS/FCF 修正 | StockAnalysis、公司财报、卖方一致预期 | EPS/FCF 上修快于股价，估值被动消化 | 股价先涨，EPS 上修有限 | EPS 下修且估值扩张，FCF yield 继续偏低 | 赔率约束，不直接否定产业瓶颈 | 所有高估值观察标的 |
| 出口管制变更 | BIS、公司风险披露、许可和区域收入 | 限制未新增且替代需求可承接 | 限制增强但收入影响可控 | 新增限制直接影响核心产品交付 | 全球设备、GPU、中国设备 | ASML、NVDA、中国设备链 |
| 中国设备财务质量 | 公司季报、合同负债、存货、经营现金流 | 收入、扣非利润、现金流、合同负债同步改善 | 利润强但现金流或合同负债偏弱 | 现金流背离利润，合同负债下降，存货恶化 | 中国设备国产替代 | 北方华创、中微公司 |

## 本轮证据增强与交互优化验收

### 新增证据增强包

| evidence id | 类型 | 来源 | 绑定节点 | 用途 |
|---|---|---|---|---|
| ev_semi_hw_nvda_fy26q3_10q_compute_networking_customer_concentration | evidence / 10-Q | NVIDIA FY2026 Q3 10-Q | Q1.1.3、Q2.1.9、Q3.1.6、Q4.1.6 | 拆 compute/networking，并把客户集中度压入反证 |
| ev_semi_hw_semi_300mm_fab_outlook_20260401 | research_report / industry_data | SEMI 300mm Fab Outlook | Q2.1.9、Q3.1.6、Q4.1.6 | 验证设备链 capex 周期，并要求用订单/backlog 反证 |
| ev_semi_hw_mu_fq2_2026_business_unit_margin | evidence / results | Micron FY2026 Q2 | Q2.1.9、Q3.1.6、Q4.1.6 | 把 HBM/高端存储压入 BU 收入、毛利率和下一季指引 |
| ev_semi_hw_samsung_1q26_ai_memory_presentation | evidence / presentation | Samsung 1Q26 presentation | Q2.1.9、Q3.1.6、Q4.1.6 | 验证 HBM4/SOCAMM2、AI memory 和 foundry base-die 约束 |
| ev_semi_hw_bis_202601_advanced_computing_license_policy | evidence / regulation | BIS / Federal Register | Q3.1.6、Q4.1.6 | 把出口管制从方向性风险变成可执行审计项 |
| ev_semi_hw_asml_financial_results_monitor_20260415 | evidence / monitor lead | ASML financial results hub | Q2.1.9、Q3.1.6、Q4.1.6 | 作为 net bookings、backlog、EUV/DUV 交付和出口许可复核入口 |

### 视觉与交互优化

- L3 节点顶部 qa-meta 统一展示结论、证据数量、反证/触发器和下一步数据。
- qa-meta 设置为 sticky，在长表滚动时保持可见。
- HTML 来源索引新增“本轮证据增强包”表格。
- 关键表格继续保留横向滚动；过长表格仍归属对应 QA 节点，不作为独立 appendix。
