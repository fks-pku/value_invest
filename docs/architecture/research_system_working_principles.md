# 投研系统架构工作原理

这份文档是给人读的架构说明。它不追求覆盖每一个类，而是解释当前系统为什么这样拆、一次研究如何跑完、以后改某个模块时应该动哪里。

当前系统的核心目标是：

```text
提出一个研究目标
  -> 自动形成专业问题树
  -> 按 L3 问题收集和解析资料
  -> GPT 验证并上抛结论
  -> 形成标的观察清单
  -> 渲染成统一 HTML 报告
```

设计原则是六边形架构：研究规则在中心，文件、模型、HTML、搜索、DeepSeek 等都在外层。这样未来改一个能力时，不会把整个系统牵动。

## 1. 一句话架构

当前系统分成五类职责：

```text
Domain：研究怎么想
Application：研究怎么跑
Ports：系统需要哪些外部能力
Adapters：这些外部能力现在怎么实现
Files/Models：真实文件、HTML、模型、外部搜索和未来数据库
```

最重要的依赖规则：

```text
Domain 不知道文件、HTML、DeepSeek、CLI 的存在。
Application 只调 Domain 和 Ports，不直接碰具体文件或模型。
Adapters 实现 Ports，负责文件系统、HTML、外部模型和兼容旧模块。
CLI 只是入口，不应该拥有研究逻辑。
```

如果以后某个功能改动影响了很多层，通常说明边界放错了。

## 2. 各层负责什么

### Domain：研究含义层

Domain 放“研究本身的规则”，它应该是纯 Python 逻辑。

典型文件：

- `src/value_invest_research/domain/research_goal.py`
- `src/value_invest_research/domain/domain_playbooks.py`
- `src/value_invest_research/domain/question_architecture.py`
- `src/value_invest_research/domain/leaf_research_tasks.py`
- `src/value_invest_research/domain/leaf_answer_synthesis.py`
- `src/value_invest_research/domain/report_view_model.py`
- `src/value_invest_research/domain/target_scoring.py`
- `src/value_invest_research/domain/quality_gates.py`

它回答的问题是：

- 这个研究目标属于什么类型？
- Q1-Q4 应该怎么定义？
- L2/L3 应该问什么问题？
- 一个 L3 leaf task 应该需要什么资料？
- provider 结果如何变成 leaf answer？
- 子问题结论如何上抛？
- 标的如何评分和排序？
- 报告 ViewModel 应该包含哪些研究内容？

它不应该做的事：

- 读写文件
- 调 DeepSeek、Perplexity、OpenAI
- 生成 HTML
- 解析 CLI 参数
- 依赖具体本地目录结构

### Application：用例和编排层

Application 放“系统怎么一步步执行”。它负责串联 Domain 和 Ports。

典型文件：

- `src/value_invest_research/application/use_cases/plan_research_goal.py`
- `src/value_invest_research/application/use_cases/build_leaf_research_tasks_from_tree.py`
- `src/value_invest_research/application/use_cases/execute_leaf_research_tasks.py`
- `src/value_invest_research/application/use_cases/parse_l3_source_materials.py`
- `src/value_invest_research/application/use_cases/synthesize_leaf_research_answers.py`
- `src/value_invest_research/application/use_cases/build_report_view_model.py`
- `src/value_invest_research/application/use_cases/render_research_project_report.py`
- `src/value_invest_research/application/orchestration/research_orchestrator.py`

它回答的问题是：

- 先生成问题，还是先读资料？
- 一个 L3 source job 交给哪个 parser？
- provider 返回结果后，如何持久化？
- 什么时候生成 leaf answer？
- 什么时候生成 parent rollup？
- 什么时候渲染报告？

它不应该做的事：

- 自己设计行业问题
- 自己拼 HTML
- 自己知道文件路径细节
- 自己调用某个具体模型 SDK

### Ports：接口层

Ports 是 Application 对外部世界的“需求声明”。它只说“我需要什么能力”，不说“现在谁来实现”。

典型文件：

- `src/value_invest_research/ports/repositories.py`
- `src/value_invest_research/ports/renderers.py`
- `src/value_invest_research/ports/source_parsers.py`
- `src/value_invest_research/ports/research_workflows.py`

例如：

- `ResearchProjectRepository`：需要加载 project、qa_tree、sources、targets。
- `CanonicalReportRenderer`：需要把 ViewModel 渲染成报告。
- `LeafResearchProvider`：需要针对一个 leaf task 返回研究结果。
- `SourceMaterialParser`：需要把一个具体 source 解析成 `source_extractions.jsonl` 记录。
- `SourceExtractionReviewer`：需要验证 parser output 是否能加强结论。

这层的价值是：未来本地 JSONL 换数据库，DeepSeek 换另一个模型，HTML 换 React，都不应该改 Application 的核心用例。

### Adapters：外部实现层

Adapters 是当前基础设施的具体实现。

典型文件：

- `src/value_invest_research/adapters/outbound/filesystem_research_project.py`
- `src/value_invest_research/adapters/outbound/filesystem_leaf_research.py`
- `src/value_invest_research/adapters/outbound/stock_leaf_research_service.py`
- `src/value_invest_research/adapters/outbound/research_search_providers.py`
- `src/value_invest_research/adapters/outbound/source_material_parsers.py`
- `src/value_invest_research/adapters/outbound/canonical_html_report_renderer.py`

它负责：

- 从本地项目目录读写 JSON/JSONL。
- 调 provider 或模型。
- 保存 raw response。
- 渲染 HTML。
- 兼容旧模块。

它可以知道文件路径、HTML class、模型 endpoint、环境变量。Domain 和 Application 不应该知道这些。

## 3. 一次研究如何跑完

下面用当前存储行业投资机会报告举例：

```text
research/bom/storage_memory_opportunities_live_20260601/
  project.json
  qa_tree.json
  research_plan.json
  research_plan_history/<plan_id>.json
  research_step_events.jsonl
  sources.jsonl
  source_extractions.jsonl
  leaf_source_reviews.jsonl
  investment_workbench.json
  professional_report.html
```

### Step 1：用户提出研究目标

用户目标是：

```text
研究存储行业投资机会
```

系统先抽象成 `ResearchGoal`：

```text
topic = 存储行业投资机会研究
research_type = industry_theme
run_mode = live_prediction
domain_hint = memory_industry
```

关键文件：

- `domain/research_goal.py`
- `application/use_cases/plan_research_goal.py`

这一步的产物不是报告，而是一个可执行的研究目标对象。

### Step 2：选择领域 playbook

系统根据 `domain_hint=memory_industry` 选择存储行业 playbook。

关键文件：

- `domain/domain_playbooks.py`

这个 playbook 决定：

```text
Q1：需求是否真实，并且能从 AI 工作负载流到具体存储产品？
Q2：哪些存储环节最可能捕获增量利润？
Q3：哪些反证、估值或供给数据会推翻当前机会？
Q4：哪些具体资产值得进入观察名单？
```

这里是未来“研究视角变化”的主要落点。

例如你觉得存储行业应该更重视：

- HBM 良率
- NAND 周期
- HDD 供给纪律
- 企业 SSD 控制器
- 云厂商 capex ROI

应该改 playbook，而不是改 HTML。

### Step 3：生成三层 QA 架构

`QuestionArchitecture` 把 Q1-Q4 拆成 L1/L2/L3。

例子：

```text
Q2 哪些存储环节最可能捕获增量利润？
  Q2.1 HBM/高端 DRAM 瓶颈
    Q2.1.1 HBM/高端 DRAM 谁真正拥有稀缺性和定价权？
    Q2.1.2 扩产速度会不会迅速消除 HBM 和高端内存瓶颈？
  Q2.2 NAND/eSSD/HDD/控制器瓶颈
    Q2.2.1 NAND/eSSD 和近线 HDD 是否也具备瓶颈属性？
    Q2.2.2 SSD controller/固件环节能否独立捕获价值？
```

关键文件：

- `domain/question_architecture.py`
- `domain/domain_playbooks.py`

每个 L3 都必须是一个“决策单元”，不能只是文章小标题。它要带：

- `decision_use`
- `support_evidence`
- `refute_evidence`
- `target_implications`
- `score_component`
- `source_plan`
- `skill_dispatch`

这保证研究不会只停留在泛泛叙述。

### Step 3A：把每个 L3 变成独立、可执行的深度研究计划

QA 树回答“应该问什么”。根 `ResearchPlan` 只索引 L3；每个 L3 必须在
`l3_research_plans/<l3_node_id>/` 拥有独立计划，再下钻为 L4 研究维度和 L5
最细叶子。只有 L5 会变成可执行步骤：

```text
leaf:Q2.1.1:actual
  问题：HBM/高端 DRAM 谁真正拥有稀缺性和定价权？
  前置步骤：Q1 的需求验证步骤
  资料计划：财报/公告、公司口径、行业数据、消息、反方观点
  完成门槛：source -> extraction -> GPT review -> answer -> refutation result
  下一步：通过门禁后才允许上卷到 Q2
```

根计划写入 `research_plan.json`，L3 计划分别写入自己的目录；每个
`plan_id` 的不可变副本保存在相邻 `research_plan_history/`。执行过程不修改历史记录，而是向
`research_step_events.jsonl` 追加 `collection_started`、
`evidence_attached`、`answer_recorded`、`gate_evaluated` 等事件。

当前状态由事件账本投影出来。材料搜集必须由一个最细 L5 叶子发起，并携带
L3 计划、L4、L5、步骤和 `search_run_id`。IMA 日归档或宽泛材料池只能形成
候选，不能先堆材料再批量映射成多个问题的证据。一个来源若服务多个叶子，
必须分别创建叶子附件、提取和 GPT 复核。缺数据时必须记录 `step_blocked`、
具体缺口和下一项验证，不能把“搜过”当成“答完”。

### Step 4：构建产业链全景

报告在 QA 前必须先有产业链全景。

对存储行业，系统需要说明：

```text
上游：设备、材料、封装资源
中游：HBM、DRAM、NAND、HDD、SSD controller
下游：云厂商、AI 服务器、企业存储、终端设备
价值流：谁向谁采购，利润在哪里，瓶颈在哪里
候选 chokepoint：HBM、高端 DRAM、enterprise SSD、nearline HDD、controller
```

关键文件：

- `domain/domain_playbooks.py`
- `domain/report_view_model.py`
- `adapters/outbound/canonical_html_report_renderer.py`

产业链全景不是装饰，它会影响：

- Q2 的瓶颈定位
- Q4 的标的排序
- 最终推荐的胜率/赔率判断

### Step 5：L3 source parsing

每个 L3 问题需要具体资料。

例如：

```text
Q1.1.1 AI 训练/推理是否继续把需求推向 HBM 和高端 DRAM？
```

它可能需要读：

- Micron FY26 Q2 results
- SK hynix Q1 2026 results
- Samsung Q1 2026 results

这些 source 会先进入 parser：

```text
SourceMaterialParser
  -> source_extractions.jsonl
SourceExtractionReviewer
  -> leaf_source_reviews.jsonl
```

关键文件：

- `ports/source_parsers.py`
- `application/use_cases/parse_l3_source_materials.py`
- `adapters/outbound/source_material_parsers.py`
- `adapters/outbound/filesystem_research_artifacts.py`

当前已有两个 adapter 形态：

- `SummarySourceMaterialParser`：用于已经有摘要的资料。
- `DelegatingSourceMaterialParser`：给 DeepSeek MCP 或未来模型 parser 接入。

未来接 DeepSeek 的位置就在这里，不应该塞进报告渲染或 QA playbook。

### Step 6：Leaf research

如果一个 L3 需要外部 provider 搜索或读取资料，会生成 leaf task。

链路是：

```text
qa_tree.json
  -> domain.leaf_research_tasks
  -> BuildLeafResearchTasksFromTree
  -> leaf_research_tasks.jsonl
  -> LeafResearchProvider
  -> ExecuteLeafResearchTasks
  -> leaf_research_results.jsonl
```

关键文件：

- `domain/leaf_research_tasks.py`
- `application/use_cases/build_leaf_research_tasks_from_tree.py`
- `application/use_cases/execute_leaf_research_tasks.py`
- `adapters/outbound/research_search_providers.py`
- `adapters/outbound/filesystem_leaf_research.py`

provider 目前包括：

- mock provider
- Perplexity provider
- OpenAI-compatible provider

未来 DeepSeek 作为 source parser 更适合接在 `SourceMaterialParser`，如果要作为 leaf provider，也可以实现 `LeafResearchProvider`。

### Step 7：Leaf answer 和父节点上抛

provider 或 parser 结果不能直接变成最终结论。系统会先做 leaf answer：

```text
leaf_research_results.jsonl
  -> domain.leaf_answer_synthesis
  -> SynthesizeLeafResearchAnswers
  -> leaf_answers.jsonl
```

然后生成父节点 rollup：

```text
enriched qa_tree
  -> BuildRollupResearchAnswers
  -> rollup_answers.jsonl
```

关键文件：

- `domain/leaf_answer_synthesis.py`
- `application/use_cases/synthesize_leaf_research_answers.py`

它的作用是：

- 分离 fact / inference / judgment / gap / trigger。
- 区分高可靠 source 和 low reliability lead。
- 把 L3 子问题结论上抛给 L2/L1。

### Step 8：标的评分和推荐

最终标的不应该靠主题热度排序，而是要结合：

- 稀缺性 / chokepoint
- 未来空间
- 估值赔率
- 盈利弹性
- 反证风险控制
- 证据质量
- 可监控性

关键文件：

- `domain/target_scoring.py`
- `application/use_cases/score_targets.py`
- `investment_workbench.json`

当前存储报告里的标的排序来自 `investment_workbench.json`，报告只是展示这个结果。

也就是说，报告 renderer 不决定谁排第一。排序应该在 scoring/workbench 层完成。

### Step 9：生成 ReportViewModel

最终报告不是直接从一堆 JSONL 拼 HTML。

系统先生成 ViewModel：

```text
FileSystemResearchProjectRepository
  -> BuildReportViewModel
  -> ReportViewModel
```

关键文件：

- `adapters/outbound/filesystem_research_project.py`
- `application/use_cases/build_report_view_model.py`
- `domain/report_view_model.py`

ViewModel 是报告数据的稳定中间层。它让 HTML renderer 不需要理解所有项目文件细节。

### Step 10：渲染 HTML 报告

最后才进入 HTML：

```text
ReportViewModel
  -> CanonicalHtmlReportRenderer
  -> professional_report.html
```

关键文件：

- `ports/renderers.py`
- `adapters/outbound/canonical_html_report_renderer.py`
- `application/use_cases/render_research_project_report.py`

HTML renderer 只负责展示，不负责研究判断。

当前报告契约固定为：

```text
当前研究目标
产业链全景
问题下钻
最终标的推荐
来源索引
```

如果以后你说“页面太丑”，应该主要改 `CanonicalHtmlReportRenderer`。

如果你说“问题不够深”，应该主要改 `DomainPlaybook` 和 QA architecture。

## 4. 当前最重要的三条主链路

### 链路 A：新研究目标到 QA 树

```text
ResearchGoal
  -> PlanResearchGoal
  -> DomainPlaybook
  -> QuestionArchitecture
  -> qa_tree.json
  -> BuildResearchPlan
  -> research_plan.json
```

例子：

```text
研究目标：存储行业投资机会
领域 playbook：memory_industry
结果：Q1 需求、Q2 瓶颈、Q3 反证、Q4 标的观察
```

改动位置：

- 想改问题深度：改 `domain_playbooks.py`
- 想改研究类型：改 `research_goal.py`
- 想改 QA 生成规则：改 `question_architecture.py`
- 想改步骤依赖和完成门禁：改 `research_plan.py`

### 链路 A2：研究计划到逐步可追溯答案

```text
research_plan.json
  -> question-specific collection
  -> source_id
  -> source_extraction_id
  -> source_review_id
  -> step answer + refutation result
  -> gate_evaluated
  -> research_step_events.jsonl
```

计划本身不等于完成。只有来源、逐来源提取、GPT 复核、回答、反证检索结果
和前置步骤全部闭合，步骤状态才会投影为 `completed`。

### 链路 B：资料到可用结论

```text
source material
  -> SourceMaterialParser
  -> source_extractions.jsonl
  -> SourceExtractionReviewer
  -> leaf_source_reviews.jsonl
  -> L3 answer
  -> parent rollup
```

例子：

```text
Micron FY26 Q2 results
  -> 抽取收入、Cloud Memory、毛利率、指引
  -> GPT verification 标记 verified_with_caveats
  -> Q1.1.1 判断 HBM/高端 DRAM 需求已进入财务结果
```

改动位置：

- 想接 DeepSeek：实现 `SourceMaterialParser`
- 想改 GPT 审核标准：实现/替换 `SourceExtractionReviewer`
- 想改 JSONL 存储：实现 `SourceParsingArtifactWriter`

### 链路 C：研究工件到 HTML

```text
project.json / qa_tree.json / sources.jsonl / investment_workbench.json
  -> ResearchProjectRepository
  -> BuildReportViewModel
  -> CanonicalHtmlReportRenderer
  -> professional_report.html
```

例子：

```text
storage_memory_opportunities_live_20260601
  -> ReportViewModel
  -> 五段式 HTML 报告
```

改动位置：

- 想改报告结构：改 report contract + renderer
- 想改审美：改 renderer CSS/HTML
- 想换存储：改 repository adapter
- 想换成前端服务：新增 renderer adapter

## 5. 为什么这样拆

### 问题 1：为什么不直接从 HTML 模板开始？

因为 HTML 模板很容易把研究逻辑写死。

错误方向：

```text
报告模板里写：
Q1 是需求
Q2 是瓶颈
Q3 是反证
Q4 是标的
```

这样研究单家公司、政策事件、技术路线时就会变形。

现在的方向：

```text
DomainPlaybook 决定 Q1-Q4 的含义。
Report contract 只规定展示层级。
```

所以“展示形式通用，问题内容自适应”。

### 问题 2：为什么 source parser 和 leaf research 要分开？

因为它们职责不同。

`SourceMaterialParser` 是“读一个具体材料”：

```text
读 Micron 财报
抽取 revenue / margin / capex / guidance
```

`LeafResearchProvider` 是“围绕一个 L3 问题做搜索或研究”：

```text
围绕 HBM 定价权搜集资料和来源
```

前者适合 DeepSeek 长上下文精读，后者适合搜索型 provider。

如果混在一起，系统会分不清：

- 哪些是资料里的事实？
- 哪些是搜索 agent 的综合判断？
- 哪些能强化结论？
- 哪些只是线索？

### 问题 3：为什么要有 ReportViewModel？

因为 HTML 不应该直接理解所有底层文件。

没有 ViewModel 时：

```text
HTML renderer 需要知道 qa_tree、sources、workbench、score、source links 的所有细节。
```

这会导致报告样式一改，研究数据结构也被迫动。

有 ViewModel 后：

```text
研究数据 -> ReportViewModel -> HTML
```

renderer 只关心“我要展示哪些字段”，不关心这些字段怎么来的。

## 6. 常见改动应该动哪里

### 改研究问题深度

场景：

```text
AI 应用投资机会的问题不够专业。
```

应该改：

- `domain/domain_playbooks.py`
- 未来可以拆到独立 domain playbook 文件

不应该改：

- HTML renderer
- source parser
- CLI

### 接入 DeepSeek 读研报/财报

场景：

```text
每个 L3 的具体材料由 DeepSeek 仔细阅读并初步解析。
```

应该新增或替换：

- `SourceMaterialParser` adapter
- `SourceExtractionReviewer` adapter

可复用：

- `ParseL3SourceMaterials`
- `SourceParsingArtifactWriter`
- `source_extractions.jsonl`
- `leaf_source_reviews.jsonl`

不应该改：

- `DomainPlaybook`
- `CanonicalHtmlReportRenderer`
- `target_scoring`

### 改报告审美

场景：

```text
报告字体、颜色、卡片、折叠交互要调整。
```

应该改：

- `adapters/outbound/canonical_html_report_renderer.py`
- `skills/value_invest_research/frameworks/research_report_contract.md`

不应该改：

- QA tree
- source parser
- target scoring

### 改标的排序逻辑

场景：

```text
最终推荐要更强调赔率和胜率。
```

应该改：

- `domain/target_scoring.py`
- `target-recommendation-analysis` skill
- `investment_workbench.json` 生成逻辑

不应该改：

- HTML renderer 的排序

renderer 只能展示排序，不应该决定排序。

### 从本地文件换数据库

场景：

```text
项目文件以后不想放 JSONL，想放数据库。
```

应该新增：

- `ResearchProjectRepository` 的数据库 adapter
- `LeafResearchArtifactRepository` 的数据库 adapter
- `SourceParsingArtifactWriter` 的数据库 adapter

不应该改：

- `BuildReportViewModel`
- `ParseL3SourceMaterials`
- `CanonicalHtmlReportRenderer`

## 7. 当前还保留的兼容模块

系统已经有清晰边界，但不是全仓库都纯六边形。

当前兼容模块：

- `leaf_research.py`：只剩兼容 wrapper。
- `report_synthesis.py`：旧报告生成仍在，后续新报告应继续迁到 ViewModel + renderer。
- `research_system.py`：仍较大，包含 QA tree、source binding、dashboard/report 生成等历史逻辑。
- `information_collection.py`：仍较大，包含 source planning、搜索、fetch、source binding 等历史逻辑。
- `meta_qa_research.py`：仍有旧 generic QA 构建逻辑。

这些不是当前新架构的核心阻塞，但后续继续拆会让系统更干净。

## 8. 当前判断：解耦是否足够

当前已经足够支撑未来迭代：

- 改研究视角：有 DomainPlaybook。
- 改 QA 生成：有 QuestionArchitecture。
- 改研究执行顺序和门禁：有 ResearchPlan / append-only step events。
- 改 source parsing：有 SourceMaterialParser / SourceExtractionReviewer。
- 改 leaf provider：有 LeafResearchProvider。
- 改报告样式：有 CanonicalReportRenderer。
- 改文件存储：有 Repository ports。
- 改评分：有 target_scoring。
- 改验证规则：有 quality_gates / framework_contracts。

还不完美的地方：

- `research_system.py` 和 `information_collection.py` 还没有拆完。
- `report_synthesis.py` 还承担旧报告路径。
- DeepSeek MCP 还缺一个真正的 runtime adapter。
- CLI 仍是一个大入口文件，未来可以拆成 inbound adapters。

但这些已经是“继续精细化”的问题，不是“架构耦合导致没法扩展”的问题。

## 9. 验证命令

每次继续拆模块后，至少跑：

```bash
PYTHONPATH=src python3 -m unittest
PYTHONPATH=src python3 -m unittest tests.test_hexagonal_architecture
PYTHONPATH=src python3 -m value_invest_research validate-report-contract research/bom/storage_memory_opportunities_live_20260601/professional_report.html --require-l3
PYTHONPATH=src python3 -m value_invest_research validate-research-artifacts research/bom/storage_memory_opportunities_live_20260601 --require-l3
PYTHONPATH=src python3 -m value_invest_research validate-research-plan research/bom/storage_memory_opportunities_live_20260601
git diff --check
```

如果改了报告前端，还需要检查：

- QA card 是否仍是 `<details class="qa-card ...">`
- Q1-Q4 是否仍在 `问题下钻`
- `最终标的推荐` 是否仍是独立 section
- `来源索引` 是否默认折叠
- final HTML 是否没有过程日志和升级说明
