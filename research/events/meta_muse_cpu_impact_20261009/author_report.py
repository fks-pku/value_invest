"""GPT-authored research content and evidence; rendered with the shared repository template."""
import json, math
from pathlib import Path

P=Path(__file__).resolve().parent
if json.loads((P/'project.json').read_text()).get('interactive_revision'):
    raise ValueError('本项目已有交互修改，不能用初稿覆盖。请使用本地研究器。')
sources=[]
def src(i,title,url,date,publisher,kind='official_company',period='',note=''):
    sources.append(dict(source_id=i,title=title,url=url,published_at=date,publisher=publisher,material_class=kind,effective_period=period,note=note,publication_date_status='verified' if date else 'undated_live_documentation',publication_date_source='原网页标题/日期或原始文件；无日期文档不编造发布日期',retrieved_at='2026-10-09',ingestion_channel='question_search'))
src('S01','Introducing Muse: Personal AI Agent','https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/','2026-09-08','Meta',note='网页更新至 2026-09-30；不把更新内容追溯为发布日已知事实。')
src('S02','How We Built Safety Into Muse','https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse','2026-09-08','Meta Research',note='官方发布架构；未披露 CPU 供应商份额、物理核绑定和休眠策略。')
src('S03','The Future Is for Everyone: Muse for Small Business','https://about.fb.com/news/2026/09/introducing-muse-small-business/','2026-09-29','Meta',note='网页更新至 2026-10-08；美国、加拿大与商家工具可用范围以该更新网页为准。')
src('S04','Meta Q2 2026 Results','https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Second-Quarter-2026-Results/default.aspx','2026-07-29','Meta IR','official_filing','2026Q2；2026 全年指引')
src('S05','AMD and Meta Expanded Strategic Partnership','https://newsroom.amd.com/news/amd-and-meta-announce-expanded-strategic-partnersh/','2026-02-24','AMD',note='6GW 是 GPU 合作规模，不是 CPU 数量或 Muse 订单。')
src('S06','AMD Q2 2026 Financial Results','https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results','2026-08-04','AMD IR','official_filing','2026Q2')
src('S07','Meta Builds AI Infrastructure With NVIDIA','https://nvidianews.nvidia.com/news/meta-builds-ai-infrastructure-with-nvidia','2026-02-17','NVIDIA',note='既有 Grace 独立部署；2027 年大规模 Vera 是可能计划。')
src('S08','NVIDIA Launches Vera CPU, Purpose-Built for Agentic AI','https://nvidianews.nvidia.com/news/nvidia-launches-vera-cpu-purpose-built-for-agentic-ai','2026-03-16','NVIDIA',note='规格和性能描述为厂商声明，不是 Muse 同条件比较。')
src('S09','NVIDIA Q2 FY2027 Financial Results','https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2027/','2026-08-26','NVIDIA IR','official_filing','截至 2026-07-26 的财季')
src('S10','Arm expands compute platform to silicon products','https://newsroom.arm.com/news/arm-agi-cpu-launch','2026-03-24','Arm',note='Meta 为主合作方和共同开发方；不等于 Muse 指定供货。')
src('S11','Arm Q1 FYE2027 Shareholder Letter / Form 6-K','https://investors.arm.com/node/8356/html','2026-07-29','Arm IR','official_filing','截至 2026-06-30 的财季')
src('S12','Intel Q2 2026 Financial Results','https://www.intc.com/news-events/press-releases/detail/1776/intel-reports-second-quarter-2026-financial-results','2026-07-23','Intel IR','official_filing','截至 2026-06-27 的财季')
src('S13','Intel Q2 2026 Form 10-Q','https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-26-000157/intc-20260627.htm','2026-07-24','Intel IR','official_filing','2026Q2；同比 2025Q2')
src('S14','Extended Component Lead Times Weigh on General Server Growth','https://www.trendforce.com/presscenter/news/20260415-13013.html','2026-04-15','TrendForce','authoritative_third_party','2026 全年预测',note='研究机构自身公开预测；4 月预测仅作为发布前基线，不冒充 10 月最新预测。')
src('S15','CPU options for Amazon EC2 instances','https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html','','AWS',note='截至抓取日的动态技术文档；解释 vCPU 概念，不证明 Meta 使用 AWS。')
src('S16','Amazon EC2 M7a Instances','https://aws.amazon.com/ec2/instance-types/m7a/','','AWS',note='动态规格；用于证明 vCPU 映射因实例类型而异，不作为 Meta 部署事实。')
src('S17','Firecracker: Lightweight Virtualization for Serverless Applications','https://www.usenix.org/system/files/nsdi20-paper-agache.pdf','2020-02','USENIX / AWS authors','authoritative_third_party','NSDI 2020',note='原始系统论文；说明隔离可与复用并存，不能据此给 Muse 指定超售比例。')
src('S18','Introducing Muse Glimmer: An Open Agentic Model That Runs on Your Device','https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model','2026-08-10','Meta Research',note='本地模型是替代技术路径，不是 9 月 Muse 云服务全面本地化。')
src('S19','AMD EPYC 9965 specifications','https://www.amd.com/en/products/processors/server/epyc/9005-series/amd-epyc-9965.html','','AMD',note='动态规格页；产品于 2024-10-10 发布，但本页当前规格/售价的更新日未知；不采用标价作 Meta 成交价。')
src('S20','Meta’s Muse Tops 3 Million Weekly Users','https://www.theinformation.com/briefings/exclusive-metas-muse-tops-3-million-weekly-users','2026-09-30','The Information','market_news',note='独家报道的内部数据；未获公司正式确认。只使用极短的规模线索，不作为 CPU 测算输入。')
src('S21','Geekbench 7 results and independent Muse run','https://www.tomshardware.com/tech-industry/artificial-intelligence/geekbench-7-results-suggest-openais-dots-agent-runs-on-nine-core-amd-epyc-vms-with-nearly-10gb-of-memory-newest-runs-score-about-six-times-meta-muse-in-multi-core','2026-09-30',"Tom's Hardware",'authoritative_third_party',note='仅采用作者亲自跑分这一原始观察及其局限；不采用文章其他人的使用量和 fleet 外推。')
src('S22','Arm Q1 FYE2027 Financial Statements and Business Model','https://investors.arm.com/node/8361/html','2026-07-29','Arm IR','official_filing','截至 2026-06-30；2026 年底产量预期')

nodes=[]
def e(source,fact,locator,boundary,effect='support',run=None,period='',target=''):
    return dict(source=source,fact=fact,locator=locator,boundary=boundary,effect=effect,search_run_id=run,effective_period=period,target_period=target)
def a(heading,*paragraphs,tables=None):
    d=dict(heading=heading,paragraphs=list(paragraphs))
    if tables:d['tables']=tables
    return d
def node(i,parent,q,why,conclusion,analysis,evidence,passed,gaps,next_actions,refutation,required=None):
    nodes.append(dict(id=i,parent_id=parent,level=1 if parent is None else 2 if parent=='MUSE' else 3,question=q,short=q,why_it_matters=why,what=q,conclusion=conclusion,analysis=analysis,evidence=evidence,passed=passed,gaps=gaps,next_actions=next_actions,refutation=refutation,data_required=required or ['问题计划中的官方事实、量化口径与反向材料'],acceptance_rule='核心事实可追溯、口径可比、反证已处理，重大缺口不得改变所声明的本题答案。',reasons=['已验证本题限定结论；不代表销量或投资门禁通过。'] if passed else ['已有条件性判断，但记录的关键缺口仍会改变幅度、兑现时间或公司收益。'],mode='leaf'))

node('O1','O','Muse 发布了什么，目前谁能使用？','确认事件对象与商业可达范围。',
'研究对象是 9 月 8 日发布的个人智能体 Muse；截至本次截止日，官方材料已覆盖美国、加拿大和小企业工具，但可用范围不等于已形成大规模持续付费负载。',[
a('从回答问题转向代办任务','Muse 由 Muse Spark 提供模型能力，但 9 月事件的新增对象是能够执行任务、保留个人状态的智能体产品。发布公告明确其运行在专属云端 VM；这比单次问答多出了一条执行环境的需求链。[S01]','9 月 29 日的小企业公告进一步确认美国、加拿大的可用性，并扩展商家账户和办公工具连接。免费入口有利于试用，但批准动作、有效完成率、成本限额和付费留存决定长期资源消费；上架或可触达人口不能代替这些数据。[S03]'),
a('采用证据的上限','The Information 9 月 30 日报道提示周活跃规模超过 300 万。[S20] 这只是早期采用线索，未获公司正式确认；它不是并发执行人数，也不适合直接进入采购模型。本文不使用媒体互相转述的注册量、日活和周活混合计算增长率。','发布与区域扩围已经足以确认事件发生，所以本题在这一边界内停止。留存、任务时长和 CPU 实际消耗仍交给需求测算问题处理；当前不能声称采用 S 曲线已经获得连续季度验证。')],
[e('S01','2026-09-08 推出个人智能体 Muse，运行于 Muse Secure VM，由 Muse Spark 驱动。','发布日期；Takeaways；How It Works','网页后续有更新；仅将原始发布事项放在 9 月 8 日。',run='O1_01'),e('S03','官方后续材料确认美国、加拿大可用，并新增小企业连接与工作场景。','2026-09-29 / 更新 10-08；Takeaways；首段','官方功能描述，不是留存或客户付费证明。','boundary','O1_01'),e('S20','媒体报道：周活跃规模超过 300 万。','2026-09-30 标题与导语','公司未正式确认；未用于资源模型。','boundary','O1_02')],True,[],['后续按相同活跃定义核验留存与任务完成量。'],'地区扩围和媒体活跃数都不能证明每用户持续占用硬件。')

node('O2','O','Muse 为什么需要云端 CPU？','建立任务、资源和成本之间的第一条因果链。',
'CPU 主要承接浏览器、代码、连接器、状态和权限控制等任务执行；模型推理可经独立接口离开用户 VM。执行环境增长与模型计算增长是互补关系。',[
a('用户交付的是一项工作','一次“处理文件并发出邮件”的任务，可拆成模型决定下一步、CPU 执行工具、读写数据、等待外部服务，再回到模型。Meta 描述的 Linux VM 包含浏览器、编译工具、子智能体和定时任务；官方还说明推理通过受约束接口访问外部基础设施。[S02] 因而 CPU 需求会随任务数、每任务调用次数和每次执行成本增长，不能仅从模型参数量判断。','这是分析推断：同样一条用户指令，若需要多轮浏览、代码执行或安全检查，会产生比简单聊天更多的通用计算；若主要时间用来等待模型、网页或人工批准，墙钟时间增加却不代表 CPU 同幅度忙碌。'),
a('专属环境与独占硬件是两件事','官方的专属 VM 表述说明隔离和个人状态的归属，未给出物理核心绑定、CPU 保底占用或内存常驻的服务承诺。把专属环境直接换算成两个常年满载物理核，缺少调度证据。','经济性应看每个成功完成任务的总成本：推理、CPU 时间、内存驻留、存储、网络和失败重试。免费或订阅是用户支付方式，不是 Meta 生产成本。本题可以确认 CPU 的角色；尚不能算出 Muse 单用户服务成本或盈亏平衡点。')],
[e('S02','个人 Linux VM 执行浏览器、编译、并发子智能体及定时任务；推理代理连接外部基础设施。','An agent in your own cloud computer；Muse Secure VM；inference proxies','可证明执行与推理路径区分；未证明模型全部在 GPU，也未披露固定物理配额。',run='O2_01'),e('S02','需要人工审批时，执行停在批准环节。','Human in the Loop','等待可以延长 VM 生存期；不能据此量化 CPU 忙碌时间。','boundary','O2_02')],True,[],['用实测执行时间与内存驻留时间补充单位任务成本。'],'多步任务也可能大部分时间在等待；执行增多不保证 CPU 利用率同比增长。')

scenario=[]
for name,p,r in [('间歇执行',.01,.01),('较高并发',.10,.10),('高驻留压力',.50,1.0)]:
    cpu=math.ceil(1_000_000*p*2*.5*1.15/(.7*256))
    mem=math.ceil(1_000_000*r*8/(.85*2048))
    hosts=max(cpu,mem)
    scenario.append(dict(name=name,U=1_000_000,p_cpu=p,r_mem=r,cpu_hosts=cpu,memory_hosts=mem,hosts=hosts,sockets=hosts*2))

node('D1','I','用户增长会变成多少 CPU 需求？','把用户与硬件建立可审计的数量关系。',
'不能从用户数直接得到 CPU 销量。CPU 同时执行比例和内存驻留比例是两个不同的瓶颈；在相同用户数下，假设变化足以让服务器需求跨越数十倍。',[
a('先审计“二核、8GB”','媒体作者报告了 Muse 的亲自跑分，所观察实例内存约 7.75GB；这是有价值的小样本观察。[S21] 本文并未取得带租户、地区及调度规则的全量部署证明，因此下面的 2 个 vCPU、8GiB 都只是便于检查的情景输入，尤其 8GiB 是近似假设，不能被写成 Meta 全部用户的物理保障。','AWS 的官方文档说明，很多实例的 vCPU 对应 SMT 线程；M7a 则采用一个 vCPU 对应一个物理核心。[S15][S16] 所以既不能一律把 vCPU 当物理核，也不能一律除以二。Firecracker 原始论文展示了隔离 VM 与资源复用可以并存，但其技术和负载不同，不足以给 Muse 套用一个超售比例。[S17]'),
a('把 CPU 时间与内存驻留分开','以 U=100 万个需要服务的用户环境做归一化示例，并非预测 Muse 当前用户数。令 p 为设计时点同时执行任务的比例，v=2 为每个运行环境配置的 vCPU 数，b=50% 为执行期间忙碌度，h=1.15 为开销系数，u=70% 为物理 CPU 目标利用率，e=1 为每物理核心的有效 vCPU 吞吐换算。假设双路服务器共 K=256 个物理核，则 H_CPU=向上取整(U×p×v×b×h÷(e×u×K))。e 需要真实工作负载测试，不能用 SMT 线程数直接替代。','令 r 为同时驻留内存的环境比例，每个驻留环境 m=8GiB，每台服务器 M=2048GiB，内存可用率 u_m=85%，则 H_RAM=向上取整(U×r×m÷(M×u_m))。CPU 和 RAM 放在同一池时，最低服务器数取 max(H_CPU,H_RAM)；表中未计存储 IOPS、峰值尾部、故障域和网络，因此不是完整采购清单。',tables=[{'caption':'纯假设敏感性：每 100 万用户环境；所有调度与主机参数均未获 Meta 验证，无概率权重。','headers':['情景','CPU 同时执行 p','内存驻留 r','CPU 限制台数','内存限制台数','取大后服务器','两路 CPU 颗数'],'rows':[[x['name'],f"{x['p_cpu']:.0%}",f"{x['r_mem']:.0%}",f"{x['cpu_hosts']:,}",f"{x['memory_hosts']:,}",f"{x['hosts']:,}",f"{x['sockets']:,}"] for x in scenario]}]),
a('为什么更多用户不必同幅度增加 CPU 颗数','本例从间歇执行到高驻留压力，所需服务器由 65 台变成 4,596 台，约相差 71 倍。它揭示需要补的数据，并不说明任何情景更接近真实。若低 CPU 忙碌度却保留大量内存，需求可能先反映为更大 DIMM、更多内存通道及不同核数配置，而不是追求最多 CPU 核。','另一个独立的压力算式是 1 亿用户×2 个独占物理核÷128 核/颗=156.25 万颗。算术成立，但隐含所有用户永久占有两个物理核、没有复用、没有现有容量等条件，不能把这一结果称为 Muse 订单。','本文算的是特定设计点下的容量存量。年度新增采购还要扣除可用余量、原计划扩容及被替代负载，并考虑部署节奏。缺口是实际调度和资源遥测，不是再增加一层抽象问题；因此保留 L3 未充分。')],
[e('S21','作者提供 Muse 亲自跑分结果，并报告观察实例的内存约 7.75GB。','正文 Muse’s runs / Our independent run，2026-09-30','小样本；无全量硬件、常驻率、专属核或采购数量证明。','boundary','D1_03'),e('S15','许多 EC2 实例把一个 SMT 线程表示为一个 vCPU。','CPU options 首段','AWS 概念示例；不能倒推 Meta 的 e 参数。','boundary','D1_04'),e('S16','M7a 的每个 vCPU 对应一个物理核心，未使用 SMT。','vCPU to physical processor core mapping','说明映射必须逐平台核验。','refute','D1_04'),e('S17','原始论文讨论 microVM 的资源复用与软分配。','Overhead and Density；Soft Allocation','不是 Muse 系统，不移植其复用倍率。','refute','D1_04')],False,['Muse 的物理核/虚拟核映射、峰值并发、CPU 忙碌度、内存驻留和闲置回收政策未公开。','缺少现有服务器余量与容量利用率，不能从容量计算跳到新增订单。'],['优先取得每活跃用户每日物理核秒、GiB 小时、峰值并发及池化策略。'],'用户账户、长期保存的文件和 24 小时可响应，都不等于 24 小时占满 CPU。')

node('D2','I','Muse 对服务器 CPU 市场的增量有多大？','区分事件增量与已经存在的 CPU 景气。',
'方向上增加执行需求，规模和新增采购尚不能可靠归因。发布前 CPU 市场已经增长并受供应约束；Muse 更像新增需求来源的验证点，目前不足以单独解释全行业涨价。',[
a('没有 Muse，CPU 需求也不是静止的','TrendForce 在 4 月已预测 2026 年服务器出货增长 13%，并讨论关键组件交期对通用服务器的限制。[S14] 这只是发布前背景预测，不是 10 月最新市场总量。Intel 的 Q2 披露更直接：服务器量同比增 9%、ASP 增 48%，其中 ASP 提升主要来自高端产品组合，价格调整贡献较小；这些都发生在 9 月事件以前。[S13]','Meta 7 月给出的全年资本开支指引为 1,300–1,450 亿美元，包含融资租赁本金。[S04] 这是整家公司基础设施支出，不能乘一个未经披露的 CPU 占比，或把预算上修全部算作 Muse。即使项目此前已为 Muse 准备容量，也需要采购归因证据，才能区分筹备需求与发布后新增需求。'),
a('增量要经过三道扣除','从某个未来时点的 Muse 所需容量出发，要先扣原有闲置容量，再扣替代掉的聊天、搜索、人工桌面或其他云端任务，最后扣没有 Muse 时也会发生的硬件更新。只有超过这些反事实容量的部分，才接近事件驱动的新采购。供应商之间转单能改变份额，却不一定增加全市场 CPU 数量。','若任务总量增长快于每任务 CPU 成本下降，长期总核时会增长；若调度优化、更多核/颗和内存扩容吸收需求，CPU 颗数增长会弱于核时增长。在供给紧张时又可能先表现为采购优先级、ASP 或产品组合，不能预设每个环节同幅增长。'),
a('能判方向，不能给精确份额','截至本轮已核验公开资料，未获得单列 Muse 的 CPU 订单、厂商份额、CPU 净售价或行业一致口径出货绝对量。因此不提供“Muse 拉动市场 X%”这样的伪精确数字，也不以未读取的付费数据库代替证据。短期看采购披露和利用率，中期看留存及任务强度，长期看行业采用是否跨客户复制。')],
[e('S14','4 月预测 2026 年总体服务器出货增长 13%，并提示组件交期约束。','2026-04-15 标题及结论段','旧预测；服务器不是 CPU 颗数，不能与虚拟核相除。','boundary','D2_02',target='2026'),e('S13','Q2 服务器量同比增长 9%、ASP 增长 48%；高端产品组合是 ASP 增长主因。','MD&A Operating Segment Revenue Summary，原报告 p.30；网页 L1479–1480','供应商口径；不能当全市场同幅涨价。','refute','D2_03',period='2026Q2'),e('S13','服务器需求超过可供给量，受内部产能限制；部分行业组件约束预计延续至下一年。','MD&A p.30，server paragraph；p.33 constraints','区别 CCPG 与 DCAI，不能把客户端约束缓解误读为服务器全部缓解。','constraint','D2_03',period='2026Q2',target='2027'),e('S04','发布前全年资本开支指引已为 1,300–1,450 亿美元。','CFO Outlook Commentary','全公司支出，含融资租赁本金；不是 Muse 或 CPU 预算。','refute','D2_03',target='2026')],False,['未披露 Muse 可归因 CPU 采购、当前利用率和被替代负载。','缺少一致口径的当期 CPU 市场绝对基线，不能输出占比。'],['核验下一期资本开支与 CPU 订单中是否单列智能体容量及供应商。'],'发布前增长、产品高端化、闲置容量复用及其他 AI 项目均能解释部分观察变化。')

node('T1','I','哪些 CPU 路线和终端会受益或被替代？','确定受影响的具体市场与技术边界。',
'最直接的是云端通用执行计算；x86 与 Arm 都可参与。竞争变量是每成功任务的总成本、兼容性和交付，而非仅比核数。没有证据证明 Muse 令 CPU 普遍替代模型加速器或驱动 PC 全面换机。',[
a('上游芯片—中游执行池—下游任务','本研究的产业边界很窄：下游消费者和商家的任务改变中游智能体执行池的核时与内存需求，再传到上游 CPU 和服务器配置。GPU/其他加速器承担的模型服务仍在另一条资源链上，不能把执行 VM 没有 GPU 推导成模型完全由 CPU 运行。Meta 的推理代理架构支持这种区分。[S02]','CPU 价值取决于串行响应、并行任务密度、内存容量/带宽、虚拟化与软件可用性。AMD 的 9965 规格页列示 192 核、384 线程及 12 个内存通道；这说明核数与线程数需分清，但它既不是 Muse 主机型号证明，也不是实际 CPU 采购配置。[S19]'),
a('Arm 已经是实际竞争路线','NVIDIA 与 Meta 2 月的 Grace-only 合作、Arm 3 月与 Meta 共同开发 AGI CPU 的公告，说明 Arm 在 Meta 的通用计算规划里已有实质位置。[S07][S10] 因此一次 x86 样本不能证明长期独占。另一方面，移植、二进制依赖、性能验证和运维成熟度会产生切换成本；本文没有同负载 TCO 数据，无法认定哪种指令集普遍最优。','若 CPU 工作增长，厂商可能获得更多核、更高价值配置或新客户，但以更高密度 CPU 替换旧机器也可能减少插槽数。内存容量先成为约束时，最大核数型号未必最经济。'),
a('端侧是一条反向路径','Meta 8 月发布的 Muse Glimmer 是可在消费级单 GPU 的 Mac/PC 上运行的 300 亿参数本地智能体模型。[S18] 它证明存在本地执行替代方案，却不是 9 月 Muse 服务已经迁到端侧的证据。长期本地处理、专用加速、缓存和批处理都可压低云端每任务 CPU 用量；PC/手机销量还需新增设备需求证据。','可确认的是云端 CPU 角色与多架构竞争；对具体最优型号、全球市场份额和客户端换机幅度保留判断。以此边界结束本题，具体公司收入仍需独立核验。')],
[e('S02','用户 VM 通过推理代理连接外部基础设施。','Muse Secure VM；inference proxies','CPU 执行与模型推理不同；未公开完整 GPU/ASIC 分配。','refute','T1_02'),e('S19','EPYC 9965 规格列示 192 物理核、384 线程、12 个 DDR5 通道。','General Specifications；Connectivity','厂商规格；未用作 Muse 实际主机或竞品性能排名。','boundary','T1_01'),e('S07','Meta 与 NVIDIA 已合作部署独立 Grace CPU。','Expanded NVIDIA CPU Deployment','早于 Muse 发布；不是 Muse 专属采购。','boundary','T1_02'),e('S10','Meta 是 Arm AGI CPU 的主要合作及共同开发方。','Meta partner paragraph','不能等同于 Muse 已完成全量迁移。','boundary','T1_02'),e('S18','Muse Glimmer 为可本地运行的 30B 开放模型，支持消费级单 GPU 设备。','开篇；local agent workflows','不同产品；不证明 CPU 单独高效运行全部大模型。','refute','T1_01')],True,[],['以同一任务成功率、延迟与功耗测试比较 x86/Arm；关注实际云端/端侧分流。'],'本地推理、内存瓶颈及高密度整合均可降低 CPU 插槽需求弹性。')

node('C0','C','哪些公司有可验证的业务敞口？','从 CPU 业务关系筛选真实研究对象。',
'AMD、NVIDIA、Arm 有 Meta 的 CPU 伙伴证据；Intel 有服务器 CPU 市场敞口，但本轮未找到 Muse 指定供货证明。四家公司值得分别看，不能把 GPU 协议或生态合作写成 Muse CPU 订单。',[
a('按合作性质筛选','AMD 公告将 EPYC 既有部署与未来 Venice/Verano 合作单独列出；NVIDIA 公告将独立 Grace 与潜在 Vera 部署单独列出；Arm 直接点名 Meta 共同开发 AGI CPU。[S05][S07][S10] 这三条都足以建立 CPU 业务关联，尚不足以分配 Muse 的采购份额。','Intel 财报提供 DCAI 业务与 Xeon 产品证据，因此是行业竞争者，而不是在缺乏供货证明时被删去。其行业受益与 Meta/Muse 直接受益必须分开。[S12] 本轮据此追加四个真实公司问题；没有把候选筛选结论当作公司财务研究已经完成。')],
[e('S05','AMD 与 Meta 合作明确包含 EPYC CPU。','EPYC partnership paragraph','6GW 属于 Instinct GPU，不直接转换 CPU 量。','boundary','C0_02'),e('S07','Meta 合作明确包括 Grace-only 及潜在 Vera。','Expanded NVIDIA CPU Deployment','并未将订单分配给 Muse。','boundary','C0_02'),e('S10','Meta 为 Arm AGI CPU 主要合作和共同开发方。','Meta partner paragraph','生态合作不等于 Muse 收入确认。','boundary','C0_02'),e('S12','Intel 披露 DCAI 业务和 Xeon 智能体基础设施进展。','Business Unit Summary；Product Momentum','证明行业敞口；无 Muse 订单。','boundary','C0_02')],True,[],['进入四个公司问题，分别验证收入桥和反证。'],'CPU 合作早于发布；不按合作标题推导 Muse 独家份额。')

node('AMD','C','AMD 的 CPU 收入能否因 Muse 增长？','检验 EPYC 执行需求能否转成净新增收入。',
'AMD 具备已验证的 EPYC 客户基础，是直接跟踪对象；但 Muse 的增量 CPU 收入无法单列，且 Meta 已布局其他架构，不能从主机线索推导独占或确定利润增幅。',[
a('业务桥是真实的，增量归因仍缺一环','2 月合作公告称 Meta 已部署数百万颗 EPYC，并将成为 Venice 与 Verano 的主要客户；这说明客户关系和部署基础都存在。[S05] 其经济价值首先是降低新增执行负载采用 EPYC 的门槛，而不是自动证明所有 Muse VM 都会变成新买的 EPYC。','AMD Q2 数据中心收入为 67 亿美元、同比增长 107%，披露同时包含 EPYC 和 Instinct。[S06] 这是发布前的混合业务基线，不能把增长率当成 CPU 增长率，也不能把未来 GPU 合同规模划给 CPU。'),
a('应怎样连接到利润','合理的收入桥是：可归因于 Muse 的新增 CPU 颗数×AMD 可得份额×合同净售价，再扣被替代的既有 CPU 收入；利润还要考虑产品毛利、部署节奏和成本。高密度提升会同时提高每颗价值并减少完成同量任务所需颗数，净结果不能只看核数。','NVIDIA Grace 与 Arm AGI CPU 的合作是“AMD 长期独占”的实质反证。[S07][S10] 若 Meta 新执行池转向 Arm，AMD 可能受益于总需求却丢失相对份额。本题停在已验证业务桥与待验证收益之间，不输出 EPS 或买入判断。')],
[e('S05','Meta 已有数百万颗 EPYC 部署，并为 Venice/Verano 主要客户。','EPYC partnership 段落','跨代全球部署存量；不是 Muse 新增 CPU 数量。','support','AMD_02'),e('S06','Q2 数据中心收入 67 亿美元，同比增长 107%，由 EPYC 和 Instinct 驱动。','Segment Summary','CPU 与 GPU 混合口径；发生于 Muse 发布前。','boundary','AMD_01',period='2026Q2'),e('S07','Meta 已有独立 Grace CPU 合作。','Expanded CPU Deployment','对长期 CPU 排他性的反证，不证明 Muse 当前已迁移。','refute','AMD_02'),e('S10','Meta 与 Arm 共同开发 AGI CPU。','Meta partner paragraph','另一供应路线，份额未披露。','refute','AMD_02')],False,['未披露 Muse 对应 EPYC 订单、净售价、替代比例及增量毛利。'],['核验 EPYC 专项出货/收入、客户执行池中 AMD 份额，而非只看数据中心总收入。'],'既有 EPYC 存量、GPU 混合财务、Arm 竞争都会削弱 Muse 到 EPS 的直接推导。')

node('INTC','C','Intel 会受益于增量需求还是承受份额压力？','区分总市场扩张与本公司份额变化。',
'Intel 可受益于服务器 CPU 的既有需求和供给紧张，但 Muse 直接供货尚未核实。新增需求与份额压力可能同时发生，收入改善不等于 Muse 带来的新增订单。',[
a('发布前已有销量和价格改善','Intel Q2 DCAI 收入 63 亿美元、同比增 59%。[S12] 更接近 CPU 的 10-Q 拆分显示，服务器量同比增 9%、ASP 增 48%，而其他 DCAI 业务也包含 ASIC。这证明不能拿 DCAI 总增长率代替 CPU 颗数增长。[S13]','高端组合是 ASP 增长主因，需求定价贡献较小；服务器内部供给限制以及部分行业组件约束仍存在。[S13] 因而更多需求有可能提升可售量和组合，也可能由于交付瓶颈被竞争者承接。上述变化均先于 Muse 发布，不能追认成事件业绩。'),
a('怎样推翻“需求增长就必然赢”','Intel 的收入应拆为市场规模×份额×净售价。若总体服务器市场扩张，但新执行池转向其他 x86 厂商或 Arm，Intel 的绝对收入仍可增长而相对地位下降。缺乏同负载交付与成本数据时，本文既不宣布其必然受损，也不把它列为已确认的 Muse 供应商。','检索官方 Intel、Meta 工程与财报材料未找到 Muse 指定供货及采购量。下一步应核验 CPU 量、扣除组合后的净价格和客户定点；公司估值、晶圆代工损益与资产负债约束未纳入本次行业影响研究，不能据此提出买卖结论。')],
[e('S12','Q2 DCAI 收入 63 亿美元，同比增长 59%。','Business Unit Revenue and Trends','包含 CPU 以外产品；不是 Muse 收入。','support','INTC_01',period='2026Q2'),e('S13','服务器量同比增 9%、ASP 增 48%；其他 DCAI 收入受 ASIC 需求驱动。','MD&A p.30，DCAI revenue paragraphs','ASP 主要是高端组合，不代表同款普涨 48%。','boundary','INTC_02',period='2026Q2'),e('S13','服务器可供给量受内部产能限制，行业组件约束可能延续。','MD&A p.30 与 p.33','是公司供应与行业组件风险；不能推广为所有 CPU 供应商均同幅短缺。','constraint','INTC_01',period='2026Q2',target='2027')],False,['未核实 Muse/Meta 新执行池的 Xeon 定点与份额。','缺少收入到增量利润的 CPU 独立口径。'],['跟踪 Xeon 定点、服务器量和同款净售价；未取得供货证据前保持行业竞争者定位。'],'市场扩大可伴随 Intel 份额下降；高 ASP 也可能来自产品组合而非事件定价权。')

node('ARM','C','Arm 如何通过 CPU 与授权获得收入？','分别核算 IP 和自有 CPU 两种收入路径。',
'Arm 已有 Meta 共同开发的 AGI CPU 路线，且保留 IP 授权与版税模式。它是结构性竞争变量，但生产爬坡与 Muse 采购分配仍缺证据，不能把所有 Arm 服务器销售额都算成 Arm 收入。',[
a('不再只是一个抽象指令集受益者','3 月公告显示 Arm 进入自有数据中心 CPU 产品，Meta 是主要伙伴和共同开发方。[S10] 因而 Arm 的事件敞口既可能来自自己的芯片销售，也可能来自其他 Arm 架构芯片的 IP 收费，两者的收入、毛利和现金需求完全不同。','7 月披露的 Q1 FYE2027 收入为 12.89 亿美元，其中版税 7.15 亿、授权及其他 5.74 亿。[S11] 另一份同期文件仍预计自有 AGI CPU 在 2026 年底投入生产。[S22] 因此不能将早期样品、路线图或合作声明写成已经发生的大规模量产收入。'),
a('增量收入要避免重复计算','自有 CPU 的收入桥是交付颗数×净售价；IP 业务则是合同许可收入与按芯片出货计提的版税。NVIDIA 或其他厂商基于 Arm 架构的整颗芯片收入属于相应供应商，不能再全额计入 Arm，否则重复计算价值链收入。','自有芯片增加直接收入空间，也增加设计、制造采购与供货执行责任。未获得 Muse 订单、量产爬坡和净毛利前，只能确认技术与商业模式敞口，不能确认最终收益幅度，更不能使用传统纯 IP 利润率去套整个新芯片业务。')],
[e('S10','Arm 推出自有 AGI CPU，Meta 为主要伙伴及共同开发方。','A new era；Meta partner paragraph','不是 Muse 已确认订单。','support','ARM_01'),e('S11','Q1 FYE2027 收入 12.89 亿美元；版税 7.15 亿、授权及其他 5.74 亿。','Exhibit 99.2；Q1 Financial Overview','三者为公司总口径；不代表数据中心或 Muse 单项。','boundary','ARM_02',period='2026-04-01/2026-06-30'),e('S22','业务文件预计自有 AGI CPU 于 2026 年底生产；IP 仍按许可与芯片版税收费。','Our Business Model，原文 p.31','管理层未来预期，不是截至研究日已量产事实。','constraint','ARM_03',target='2026年底')],False,['未披露 Muse 的 AGI CPU 采购规模、量产收入与净利润。'],['核验量产交付与自有芯片收入分类；把 IP 版税和芯片销售分开跟踪。'],'合作、样品与潜在需求不等于量产收入；自有芯片也改变成本和现金流风险。')

node('NVDA','C','NVIDIA 能否从 Muse 的 CPU 需求中受益？','核验其独立 CPU 业务，而非仅看 GPU。',
'NVIDIA 在 Meta 已有独立 CPU 合作，CPU 需求上升并不自然构成其损失。但 Grace/Vera 的 Muse 份额和独立收入未披露，不能把整个数据中心增长视为 CPU 盈利弹性。',[
a('NVIDIA 已经跨进执行计算','2 月双方公告明确独立 Grace 部署，并提出 2027 年可能大规模部署 Vera。[S07] Vera 官方定位包含编译、运行时、分析与智能体编排，列示 88 个核心及相关内存设计。[S08] 这些材料足以说明 NVIDIA 有执行侧产品路线，不能继续用“CPU 利好等于 GPU 龙头利空”的单线叙事。','但发布时间早于 Muse，厂商特定性能口径也不等于 Muse 环境的每成功任务成本。潜在的 2027 年部署不是研究日已经确认的 Muse 新订单。'),
a('财务规模反而要求更严格的归因','NVIDIA 截至 2026-07-26 财季的数据中心收入为 890 亿美元。[S09] 其中不能单列出 Muse 或独立 CPU 的贡献。CPU 增量即使对产品战略有意义，也未必足以改变这么大规模业务的利润轨迹；需要单独的颗数、售价、毛利及 GPU/网络配套变化。','未来若执行池由独立 CPU 更高效承接，GPU 的单位任务等待可能减少，这既可能减少浪费，也可能提高整个服务的经济性并促进任务增长。没有成本弹性与采用数据时，两种效应的净值无法确定。本题只确认双侧供给能力，不宣布 Muse 对其估值已形成确定增量。')],
[e('S07','Meta 独立 Grace 部署已获双方披露，Vera 大规模部署潜在时点为 2027 年。','Expanded NVIDIA CPU Deployment，网页 L60–64','既有合作；2027 是可能规划而非完成事实。','support','NVDA_03',target='2027'),e('S08','Vera 产品定位涵盖智能体执行，规格列示 88 核。','Designed for Agentic Scaling','厂商规格，不能与其他 CPU 只按核数比较。','boundary','NVDA_02'),e('S09','Q2 FY2027 数据中心收入 890 亿美元。','Financial Highlights / Data Center','不是 CPU 独立收入，且早于 Muse 发布。','boundary','NVDA_02',period='截至2026-07-26财季')],False,['Muse 的 Grace/Vera 份额与 CPU 独立收入未披露。'],['跟踪 Grace/Vera 的独立量产、客户定点和每任务成本，不用全数据中心收入替代。'],'其他 CPU 路线竞争及 CPU 在总业务中的占比，可能限制事件对整体利润的影响。')

node('O','MUSE','Muse 是什么，发生了什么变化？','建立产品事实和资源机制。',
'Muse 将个人智能体与云端执行环境结合；发布与后续扩围已核实，实际资源强度仍未公开。',[
a('从产品变化连接到硬件','O1 确认发生了什么、谁能用，O2 解释为什么需要 CPU。两题结合，能够确认任务执行是一条独立需求路径，但功能存在、使用增加与硬件增购仍是不同的命题。模型更强只可能提高任务采用，不能替代执行数据。')],[],True,[],['下一步检验每用户核时与内存驻留。'],'免费入口与专属 VM 不能证明持续满载。')
node('I','MUSE','它怎样影响 CPU 市场？','将需求数量、市场增量与技术竞争连接起来。',
'条件性利好服务器 CPU 和内存配置；影响更可能先落在有效核时与执行池容量，CPU 颗数、ASP 和市场份额仍需分别验证。',[
a('三条判断必须同时成立','D1 表明用户到硬件的换算取决于并发与驻留，D2 表明即使出现采购也要剔除既有增长和替代，T1 则表明同一需求可以被不同 CPU 架构承接。三者不能压缩成“用户数×两核”。','短期发布增强对执行计算的关注，但业绩确认取决于已有容量；中期若任务量和留存持续，执行池容量才会扩张；长期若单位任务成本下降更快、或迁往端侧，云端 CPU 的增长会低于简单用户外推。'),
a('用可观测条件推动下一判断','下表是研究者设定的后续判别条件，不是公司承诺或已观察数据；不据此创建自动监控或交易。',tables=[{'caption':'条件与反证：以未来披露或同口径实测为触发','headers':['检查点','量化/可执行判别','频率','对判断的处理'],'rows':[['真实负载','CPU 核时比值=活跃用户比值×每用户任务比值×每任务核时比值；连续两次≤1','月度可比快照','撤回 CPU 负载加速假设'],['新增采购','事件负载超过可用余量及无事件扩容，且采购归因有原文','季度/采购公告','才上调实际新增订单判断'],['部署路线','新执行池有≥2 家供应商官方定点','事件披露','否定单一供应商独占论'],['盈利兑现','连续两个财报期仍无 CPU 独立量、价或客户桥','季度','保留收益未验证，不升为买入'],['经济性','在相同成功率与延迟下，每成功任务总成本持续下降','每次同口径复测','重算资源弹性，不以核数增加替代成本改善']]}])],[],False,['D1 未知资源强度；D2 未知净新增采购和可比市场分母。'],['优先补资源遥测及采购归因，再重算情景。'],'技术优化和已有容量可能吸收任务增长，供给紧张也早已存在。')
node('C','MUSE','具体影响哪些公司？','按业务事实分配潜在收益和风险。',
'AMD、NVIDIA、Arm 有 Meta CPU 合作，Intel 是行业竞争者；目前四家公司都没有通过 Muse 增量收益验证，本文不做证券推荐。',[
a('需求增量与份额分配同时研究','C0 提供候选筛选，四个公司问题分别检查已确认业务、财务口径和竞争反证。AMD 的 EPYC 客户基础更直接，NVIDIA 同时有执行与模型侧产品，Arm 兼具自有 CPU 和 IP 路径，Intel 的结果取决于供给执行及份额。这个排序是证据路径的差异，不是预期收益率排名。','四家公司最新已核验财报都早于 Muse 发布，不能用这些业绩证明发布后的财务兑现。没有价格、预期利润和风险收益比较，也就没有错误定价证明。本文只保留行业观察；证券行动状态为 no_action，而非把行业方向偷换为买入结论。')],[],False,['四家公司的 Muse 增量订单、CPU 净售价和利润均未单列；估值不在本次行业影响任务内。'],['取得直接订单或同口径执行池部署证据后，再开展公司估值研究。'],'合作关系不等于新增利润，行业利好不等于市场尚未定价。')
node('MUSE',None,'Meta Muse 发布将怎样影响 CPU 市场？','回答行业影响，而非直接生成买卖建议。',
'Muse 强化了“个人智能体需要云端执行计算”的需求逻辑，条件性利好服务器 CPU；但“专属 VM”不足以证明独占物理核，当前也不能确认 CPU 销量暴增或某家厂商独占受益。',[
a('最重要的变化是增加任务执行','研究对象分支确认了发布和 VM 机制，市场分支把它转成资源与采购约束，公司分支检验谁能取得收入。方向成立依赖于实际任务执行持续增长；幅度成立还需要并发、驻留、闲置容量和订单证据。当前前半段证据较完整，后半段仍缺关键数据。','因此本次最有用的判断是：服务器 CPU 的需求来源在扩展，而不是已经获得一个可精确计量的 Muse 出货订单。未来更高的任务量、更长的后台执行以及小企业工作流可能放大需求；同样，调度复用、内存约束、端侧分流和单位任务效率提升也可能显著压低 CPU 颗数弹性。'),
a('怎样阅读与使用结果','先看研究对象，再看用户到资源的敏感性测算，最后看公司章节。所有测算均将事实与假设分开；CPU 的容量存量不被当作年度新增销量，发布前采购与业绩不被当作发布后兑现。报告形成于 2026-10-09，属于有明确缺口的实时事件研究，而不是回测收益或买卖建议。')],[],False,['缺少用户资源遥测、可归因采购、供应商份额和公司增量利润。'],['下一优先证据是 Muse 每活跃用户核秒/GiB 小时及 Meta 的执行池采购拆分。'],'CPU 使用增长可能被复用和效率提升抵消；已存在的 CPU 周期不是 Muse 独有增量。')

by={n['id']:n for n in nodes}
ordered=[]
def visit(i):
    n=by[i];children=[c for c in nodes if c['parent_id']==i];n['mode']='rollup' if children else 'leaf';ordered.append(n)
    for c in children:visit(c['id'])
visit('MUSE')
report=dict(template_version='question-tree-v1',title='Meta Muse 发布对 CPU 市场的影响',subtitle='实时事件研究｜2026-09-08 发布，证据截至 2026-10-09｜服务器 CPU 为主，检验端侧替代｜方向可判断，销量与收益未充分',as_of_date='2026-10-09',status_label='PARTIAL RESEARCH · 非证券推荐',nodes=ordered,sources=sources,source_note='来源在每个叶子独立抽取和 GPT 复核。官方披露与预测、记者原始观察、媒体线索分开处理。动态文档保留真实日期空值；无 IMA 镜像可用，未声称完成 IMA 扫描。',attachments=[{'label':'研究计划','href':'research_plan.md'},{'label':'Markdown 审计副本','href':'professional_report.md'}])
report['attachments'].insert(0, {'label':'交互编辑研究问题（需本地服务）','href':'http://127.0.0.1:8765/#MUSE'})
(P/'question_tree_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(P/'scenario_calculations.json').write_text(json.dumps({'type':'hypothetical_sensitivity_not_forecast','assumptions':{'v':2,'b':.5,'h':1.15,'u':.7,'e':1,'K_cores_per_host':256,'m_GiB_per_resident':8,'M_GiB_per_host':2048,'memory_utilization':.85},'rows':scenario},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'nodes':len(ordered),'leaves':sum(n['mode']=='leaf' for n in ordered),'sources':len(sources),'scenario':scenario},ensure_ascii=False))
