---
report_scope: bom-node
project_id: ai_factory_industry_scurve_timeslice_20260328__bom__powerCooling
bom_node_id: powerCooling
run_mode: historical_backtest
as_of_date: 2026-03-28
---

# AI 工厂 · 电力 / 液冷 / 数据中心基础设施 BOM 节点研究

[返回 AI 工厂产业总览](../../professional_report.md)

> 研究截面：2026-03-28。本报告只研究 电力 / 液冷 / 数据中心基础设施，不把其他 BOM 的结论提前扩散到本节点。

## 1. 当前研究的问题

判断 电力 / 液冷 / 数据中心基础设施 是否处在可投资的 S 曲线阶段，并识别需求、供给、控制权、财务兑现、市场定价和反证的证据边界。

| 节点边界 | 内容 |
| --- | --- |
| 接受什么 | 高功率机柜密度、热负载、电力容量和项目工程要求。 |
| 生产什么 | UPS、配电、热管理、液冷、现场工程和服务。 |
| 提供给谁 | 云厂商、数据中心运营方、系统集成项目。 |
| 代表公司 | Vertiv、数据中心工程商、电力/热管理供应商 |
| 验证指标 | orders、backlog、organic growth、project margin、cash conversion。 |

## 2. 行业概况

### 电力 / 液冷 / 数据中心基础设施

高功率机柜必须接入电力并散热，否则算力不能上线。

**研究账本说明：** 六问是稳定逻辑坐标；材料按市场可见时间追加到 `BOM × 六问 × 时间` 账本。本报告只展示结论、真实变化和可审计材料，不展示搜索词、解析提示或工具过程。

### Q1 · 当前 BOM 的需求是否会被 S 曲线放大拉动？

**结论强度：** 待验证  
**最近材料：** 2026-02-11

#### 基本理解思路

- **专业模型：** S 曲线传导与弹性模型
- **研究目的：** 判断终端 AI 需求是否真实传导到当前 BOM，并且是否具备大于终端需求的弹性。
- **判断规则：** 可投资需求 = 真实工作负载增长 × 客户预算/订单兑现 × 电力 / 液冷 / 数据中心基础设施 直接拉动 × 单位用量或单位价值量弹性。
- **理解提示：** 由本节点 playbook 提供。

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

GPU/ASIC 和 rack-scale 系统功耗提升后，数据中心必须新增电力、UPS、PDU、液冷和热管理能力；高功率机柜提高每 rack 的电力和散热需求，抬升 UPS、配电、液冷 CDU、管路、现场工程和服务价值量。

**支持机制：** 需求可持续的第一性原理是：AI 工作负载、用户任务、上下文长度、多模态和 agent 步数提高总计算/基础设施需求，并通过客户预算进入 电力 / 液冷 / 数据中心基础设施。

**最大反证：** 若 AI 应用 ROI 不足、模型效率提升快于工作负载增长、客户 capex 下修或订单取消，需求趋势就不可持续。

**对标的的影响：** 本问决定 电力 / 液冷 / 数据中心基础设施 相关标的是否有足够大的收入天花板和增长斜率。若需求链条不能从工作负载穿透到订单、收入和 BOM 弹性，即使公司质量好，也只能保留观察；若需求强成立，后续才值得继续评估供给稀缺、控制者和定价。

**关键来源：** [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)；[Dell'Oro Group Data Center Liquid Cooling Forecast](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html)；[Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | GPU/ASIC 和 rack-scale 系统功耗提升后，数据中心必须新增电力、UPS、PDU、液冷和热管理能力；高功率机柜提高每 rack 的电力和散热需求，抬升 UPS、配电、液冷 CDU、管路、现场工程和服务价值量。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 事实 / 支持 | GPU/ASIC 和 rack-scale 系统功耗提升后，数据中心必须新增电力、UPS、PDU、液冷和热管理能力；高功率机柜提高每 rack 的电力和散热需求，抬升 UPS、配电、液冷 CDU、管路、现场工程和服务价值量。 |
| 2026-01-08 | [Dell'Oro Group Data Center Liquid Cooling Forecast](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html) | 事实 / 支持 | GPU/ASIC 和 rack-scale 系统功耗提升后，数据中心必须新增电力、UPS、PDU、液冷和热管理能力；高功率机柜提高每 rack 的电力和散热需求，抬升 UPS、配电、液冷 CDU、管路、现场工程和服务价值量。 |
| 2026-02-11 | [Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/) | 事实 / 支持 | GPU/ASIC 和 rack-scale 系统功耗提升后，数据中心必须新增电力、UPS、PDU、液冷和热管理能力；高功率机柜提高每 rack 的电力和散热需求，抬升 UPS、配电、液冷 CDU、管路、现场工程和服务价值量。 |



#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-02-11 | [Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | GPU/ASIC 和 rack-scale 系统功耗提升后，数据中心必须新增电力、UPS、PDU、液冷和热管理能力；高功率机柜提高每 rack 的电力和散热需求，抬升 UPS、配电、液冷 CDU、管路、现场工程和服务价值量。 | 未结构化 | 未结构化 |
| 2026-01-08 | [Dell'Oro Group Data Center Liquid Cooling Forecast](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | GPU/ASIC 和 rack-scale 系统功耗提升后，数据中心必须新增电力、UPS、PDU、液冷和热管理能力；高功率机柜提高每 rack 的电力和散热需求，抬升 UPS、配电、液冷 CDU、管路、现场工程和服务价值量。 | 未结构化 | 未结构化 |
| 2024-07-17 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | GPU/ASIC 和 rack-scale 系统功耗提升后，数据中心必须新增电力、UPS、PDU、液冷和热管理能力；高功率机柜提高每 rack 的电力和散热需求，抬升 UPS、配电、液冷 CDU、管路、现场工程和服务价值量。 | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 2024-07-17 | 2026-02-11 | 单向覆盖，缺反证 |

### Q2 · 供给能否跟上？

**结论强度：** 待验证  
**最近材料：** 2026-02-11

#### 基本理解思路

- **专业模型：** 产能 / 良率 / 周期 / 认证模型
- **研究目的：** 判断有效供给释放速度是否慢于需求斜率。
- **判断规则：** 有效供给 = 名义产能 × 良率 × 客户认证 × 设备/材料可得性 × 交付周期；若有效供给斜率低于需求斜率，电力 / 液冷 / 数据中心基础设施 才具备稀缺性。
- **理解提示：** 由本节点 playbook 提供。

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

约束来自工程交付、项目周期、电力接入、现场可靠性、液冷方案认证和供应链交付能力。

**支持机制：** 供给约束可持续来自产能、良率、认证、交期、工程交付和客户锁定慢于需求斜率。

**最大反证：** 若扩产、良率、替代供应商和客户认证同步释放，短缺会转为价格和毛利压力。

**对标的的影响：** 本问决定 电力 / 液冷 / 数据中心基础设施 是否具备 chokepoint 属性。供给跟不上时，控制有效产能和认证资源的公司才可能获得价格、毛利和 backlog 弹性；如果供给快速释放，标的推荐应从“稀缺溢价”降为“行业 beta”。

**关键来源：** [Dell'Oro Group Data Center Liquid Cooling Forecast](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html)；[Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 约束来自工程交付、项目周期、电力接入、现场可靠性、液冷方案认证和供应链交付能力。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2026-01-08 | [Dell'Oro Group Data Center Liquid Cooling Forecast](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html) | 事实 / 支持 | 约束来自工程交付、项目周期、电力接入、现场可靠性、液冷方案认证和供应链交付能力。 |
| 2026-02-11 | [Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/) | 事实 / 支持 | 约束来自工程交付、项目周期、电力接入、现场可靠性、液冷方案认证和供应链交付能力。 |



#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-02-11 | [Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | 约束来自工程交付、项目周期、电力接入、现场可靠性、液冷方案认证和供应链交付能力。 | 未结构化 | 未结构化 |
| 2026-01-08 | [Dell'Oro Group Data Center Liquid Cooling Forecast](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | 约束来自工程交付、项目周期、电力接入、现场可靠性、液冷方案认证和供应链交付能力。 | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2026-01-08 | 2026-02-11 | 单向覆盖，缺反证 |

### Q3 · 谁控制供给？

**结论强度：** 待验证  
**最近材料：** 2026-02-11

#### 基本理解思路

- **专业模型：** 份额 / 壁垒 / 替代 / 客户锁定模型
- **研究目的：** 判断稀缺供给是否被少数公司控制，并能转成利润池。
- **判断规则：** 控制权 = 份额集中度 + 资格/认证壁垒 + 技术/IP/生态壁垒 + 客户锁定 - 替代与多供速度。
- **理解提示：** 由本节点 playbook 提供。

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

Vertiv、Schneider、Eaton 和数据中心工程/液冷供应商控制关键供给。

**支持机制：** 控制权可持续来自技术门槛、生态锁定、客户资格、长期协议、规模经验和不可替代交付能力。

**最大反证：** 若客户多供应商策略成功、替代技术成熟、标准化降低切换成本，控制权就会被稀释。

**对标的的影响：** 本问决定推荐应落到哪些具体公司。只有能控制合格供给、客户资格、生态或交付能力的公司，才可能把 电力 / 液冷 / 数据中心基础设施 的需求增长转成超额利润；份额分散或替代加速时，不应把整个节点的增长平均分配给所有玩家。

**关键来源：** [Dell'Oro Group Data Center Liquid Cooling Forecast](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html)；[Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | Vertiv、Schneider、Eaton 和数据中心工程/液冷供应商控制关键供给。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2026-01-08 | [Dell'Oro Group Data Center Liquid Cooling Forecast](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html) | 事实 / 支持 | Vertiv、Schneider、Eaton 和数据中心工程/液冷供应商控制关键供给。 |
| 2026-02-11 | [Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/) | 事实 / 支持 | Vertiv、Schneider、Eaton 和数据中心工程/液冷供应商控制关键供给。 |



#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-02-11 | [Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | Vertiv、Schneider、Eaton 和数据中心工程/液冷供应商控制关键供给。 | 未结构化 | 未结构化 |
| 2026-01-08 | [Dell'Oro Group Data Center Liquid Cooling Forecast](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html) | 第三方权威 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | Vertiv、Schneider、Eaton 和数据中心工程/液冷供应商控制关键供给。 | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2026-01-08 | 2026-02-11 | 单向覆盖，缺反证 |

### Q4 · 是否已经财务兑现？

**结论强度：** 待验证  
**最近材料：** 2026-02-11

#### 基本理解思路

- **专业模型：** 收入 / 毛利 / backlog / 现金流模型
- **研究目的：** 判断产业逻辑是否已经进入公司财务，而不是停留在叙事或订单新闻。
- **判断规则：** 财务兑现 = 收入增长 + backlog/RPO 可见度 + 毛利/ASP 改善 + 经营现金流质量 - 库存/应收/取消风险。
- **理解提示：** 由本节点 playbook 提供。

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

Vertiv organic orders +252% YoY、backlog $15.0B，是物理瓶颈财务化最清楚的证据之一。

**支持机制：** 财务兑现可持续需要 电力 / 液冷 / 数据中心基础设施 的收入、订单、backlog、毛利率和现金流沿同一方向改善。

**最大反证：** 若收入增长依赖低毛利订单、应收/库存上升或 backlog 转收入变慢，财务兑现质量会下降。

**对标的的影响：** 本问决定标的确定性。收入、毛利、backlog 和现金流已经兑现的公司可进入更高置信候选；只有订单新闻、没有利润和现金兑现的公司，需要降低推荐强度并提高监控频率。

**关键来源：** [Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | Vertiv organic orders +252% YoY、backlog $15.0B，是物理瓶颈财务化最清楚的证据之一。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2026-02-11 | [Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/) | 事实 / 支持 | Vertiv organic orders +252% YoY、backlog $15.0B，是物理瓶颈财务化最清楚的证据之一。 |



#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-02-11 | [Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/) | 公司官方材料 / 历史 / 手动导入 | 事实 / 支持 | 材料发现 | Vertiv organic orders +252% YoY、backlog $15.0B，是物理瓶颈财务化最清楚的证据之一。 | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2026-02-11 | 2026-02-11 | 单向覆盖，缺反证 |

### Q5 · 市场是否已定价？

**结论强度：** 待验证  
**最近材料：** 2026-02-11

#### 基本理解思路

- **专业模型：** 估值 / 预期差 / 盈利上修模型
- **研究目的：** 判断好产业是否仍是好赔率。
- **判断规则：** 赔率 = 未来盈利上修空间 ÷ 已定价增长与风险溢价；产业强度必须超过市场隐含预期才有推荐价值。
- **理解提示：** 由本节点 playbook 提供。

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

市场已开始识别电力/液冷，但相对 GPU 平台可能仍更容易出现预期差。

**支持机制：** 错价可持续来自市场低估增长持续期、盈利弹性、利润率上行或风险下降。

**最大反证：** 若估值已经把高增长、高毛利和低风险全部计入，基本面继续强也可能没有足够赔率。

**对标的的影响：** 本问直接决定 action state。即使 电力 / 液冷 / 数据中心基础设施 是正确节点，如果估值和盈利预期已经充分反映，推荐只能是 watch_only；只有基本面继续超预期且估值未完全定价，才可能进入 actionable_long。

**关键来源：** [Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 市场已开始识别电力/液冷，但相对 GPU 平台可能仍更容易出现预期差。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2026-02-11 | [Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/) | 估值 / 支持 | 市场已开始识别电力/液冷，但相对 GPU 平台可能仍更容易出现预期差。 |



#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-02-11 | [Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/) | 公司官方材料 / 历史 / 手动导入 | 估值 / 支持 | 材料发现 | 市场已开始识别电力/液冷，但相对 GPU 平台可能仍更容易出现预期差。 | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 2026-02-11 | 2026-02-11 | 有材料，结构不完整 |

### Q6 · 反证是什么？

**结论强度：** 待验证  
**最近材料：** 2026-02-11

#### 基本理解思路

- **专业模型：** 触发器 / 阈值 / 降级动作模型
- **研究目的：** 把反证从泛泛风险变成可监控的降级纪律。
- **判断规则：** 反证强度 = 领先触发器变化 × 对需求/供给/控制权/财务/定价链条的破坏程度 × 可持续性。
- **理解提示：** 由本节点 playbook 提供。

理解提示只用于建立方向，不是材料准入清单；新材料发现的变量、观点和反证可直接进入本问。

#### 当前结论

客户 capex 下修、电力接入延迟、项目毛利低于预期、backlog 取消或转收入慢、液冷渗透率低于预期。

**支持机制：** 有效反证应比财报恶化更早出现：价格、交期、订单、客户预算、供给释放或替代路线先发生变化。

**最大反证：** 如果反证指标连续出现并穿透到收入、毛利、现金流或估值预期，应从观察名单降级。

**对标的的影响：** 本问定义推荐纪律。电力 / 液冷 / 数据中心基础设施 相关标的必须绑定可观察降级触发器；当需求、供给、控制权、财务兑现或定价任一核心反证触发时，推荐强度应自动下调，而不是事后解释。

**关键来源：** [Dell'Oro Group Data Center Liquid Cooling Forecast](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html)；[Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/)

#### 相较上一截面的变化

这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。

| 记录时间 | 类型 | 原判断 | 当前判断 | 变化说明 |
| --- | --- | --- | --- | --- |
| 2026-03-28 | 基线 | 无历史快照 | 客户 capex 下修、电力接入延迟、项目毛利低于预期、backlog 取消或转收入慢、液冷渗透率低于预期。 | 这是时间账本的基线快照；此前未保存结构化研究快照，不反向编造历史结论。 |

#### 时间演化

材料按首次对市场可见的时间排列。材料出现不等于研究结论自动改变。

| 发布时间 | 材料 | 类型 / 立场 | 观点或数据 |
| --- | --- | --- | --- |
| 2026-01-08 | [Dell'Oro Group Data Center Liquid Cooling Forecast](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html) | 反证 / 反证 | 客户 capex 下修、电力接入延迟、项目毛利低于预期、backlog 取消或转收入慢、液冷渗透率低于预期。 |
| 2026-02-11 | [Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/) | 反证 / 反证 | 客户 capex 下修、电力接入延迟、项目毛利低于预期、backlog 取消或转收入慢、液冷渗透率低于预期。 |



#### 映射材料

| 发布时间 | 材料 | 材料分类 / 进入方式 | 类型 / 立场 | 主题 | 观点或数据 | 实际期间 | 预测期间 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-02-11 | [Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/) | 公司官方材料 / 历史 / 手动导入 | 反证 / 反证 | 材料发现 | 客户 capex 下修、电力接入延迟、项目毛利低于预期、backlog 取消或转收入慢、液冷渗透率低于预期。 | 未结构化 | 未结构化 |
| 2026-01-08 | [Dell'Oro Group Data Center Liquid Cooling Forecast](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html) | 第三方权威 / 历史 / 手动导入 | 反证 / 反证 | 材料发现 | 客户 capex 下修、电力接入延迟、项目毛利低于预期、backlog 取消或转收入慢、液冷渗透率低于预期。 | 未结构化 | 未结构化 |

#### 信息覆盖

| 实际 | 预测 | 观点 | 消息 | 估值 | 反证 | 支持 | 冲突 | 最早 | 最新 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 | 2026-01-08 | 2026-02-11 | 有材料，结构不完整 |

### S 曲线汇总

当前节点的产业逻辑已形成，但仍有 6 个问题未达到高置信。特别是市场定价未闭环时，不能把产业胜率直接写成证券买入赔率。

## 3. 标的推荐

以下只保留映射到当前 BOM 的标的。产业逻辑强不等于证券价格便宜。

| 标的 | 公司 | BOM 节点 | 候选状态 | 最终状态 | 核心理由 | 未来空间 / 赔率 | 主要风险 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VRT | Vertiv | 电力 / 液冷 / 数据中心基础设施 | actionable_long | no_action | AI 工厂物理瓶颈已经体现为 orders 和 backlog，空间大、财务兑现直接、反证可监控。 | 1.5 | backlog 毛利低质量、云厂 capex 下修、项目交付延迟。 |

## 4. 来源索引

| ID | 来源 | 类别 | 市场可见时间 | 用途摘要 |
| --- | --- | --- | --- | --- |
| SRC-VRT-Q4-2025 | [Vertiv Q4 2025 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/) | evidence | 2026-02-11 | Vertiv Q4 2025 organic orders rose about 252% YoY and backlog reached $15.0B, reflecting robust AI infrastructure demand. |
| SRC-SA-GB200-BOM-2024 | [SemiAnalysis GB200 Hardware Architecture Component Supply Chain and BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) | research_report | 2024-07-17 | SemiAnalysis mapped GB200 rack-scale architecture and component implications, including that many data centers cannot support very high rack density without direct-to-chip liquid cooling. |
| SRC-DO-LIQUID-COOLING-20260108 | [Dell'Oro Group Data Center Liquid Cooling Forecast](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html) | research_report | 2026-01-08 | Dell'Oro Group forecast data-center liquid-cooling manufacturer revenue near $3B in 2025 and approaching $7B by 2029, with hyperscalers anchoring demand and direct liquid cooling leading adoption. |
