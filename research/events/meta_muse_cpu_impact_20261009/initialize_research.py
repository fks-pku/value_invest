"""Initialize the Muse event study using shared L3 plan contracts; no research facts generated."""
import json
from pathlib import Path
from datetime import datetime, timezone
from value_invest_research.domain.l3_research_plan import build_l3_research_plan_set, upgrade_parent_plan_for_l3_plans
from value_invest_research.adapters.outbound.filesystem_source_universe import FileSystemSourceUniverseRepository

P = Path(__file__).resolve().parent
if (P / 'project.json').exists() and json.loads((P / 'project.json').read_text()).get('interactive_revision'):
    raise ValueError('本项目已有交互修改，不能重新初始化覆盖。请使用本地研究器。')
ROOT = P.parents[2]
NOW = datetime.now(timezone.utc).isoformat()
def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')
def append(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a') as f: f.write(json.dumps(obj, ensure_ascii=False)+'\n')

specs = [
 ('O1','O','Muse 发布了什么，目前谁能使用？','核实事件对象、可用性和采用，避免把模型更新当作个人智能体发布。',['发布及更新日期、地区、定价','用户留存、任务次数、活跃付费使用披露'],['对比发布与后续实质扩围','区分可触达用户、注册用户和活跃使用']),
 ('O2','O','Muse 为什么需要云端 CPU？','确认 CPU 负责什么以及资源成本边界。',['官方 VM、浏览器、工具和推理架构','资源配额、调度、休眠、存储与计费口径'],['分开模型推理与执行环境','查证专属 VM 是否意味着独占物理核心']),
 ('D1','I','用户增长会变成多少 CPU 需求？','把用户规模转为可检查的计算模型，避免按用户数直接乘核心数。',['活跃率、运行时长、并发、CPU 忙碌比例','物理核与 vCPU、SMT、CPU/内存约束'],['建立物理核心、内存与服务器三重瓶颈模型','情景敏感性不充当销量预测']),
 ('D2','I','Muse 对服务器 CPU 市场的增量有多大？','与没有 Muse 的既有增长比较，检查供给与价格传导。',['发布前服务器 CPU 需求与市场份额基线','Meta 采购、资本开支、CPU 供给及 ASP 变化'],['区分市场新增、供应商份额转移和采购提前','检查是否有归因于 Muse 的订单及供给瓶颈']),
 ('T1','I','哪些 CPU 路线和终端会受益或被替代？','区分高密度服务器 x86、Arm、GPU 与端侧处理器。',['x86 与 Arm 的软件、性能功耗、内存及安全条件','Muse 本地执行与云端部署边界','GPU offload 与无事件替代方案'],['按任务比较总成本和兼容性','检验 CPU 替代 GPU、PC 换机等相反解释']),
 ('C0','C','哪些公司有可验证的业务敞口？','先筛选真实供应与竞争关系，再决定需要独立研究的公司。',['Meta 与 CPU 供应商官方合作','厂商产品收入拆分与既有竞争关系'],['区分已确认供货、部署线索和潜在候选','禁止把 AMD GPU 协议直接作为 CPU 订单']),
]

goal = {'research_object':'Meta Muse personal agent release and CPU market impact','mode':'live','run_mode':'live','as_of_date':'2026-10-09','report_date':'2026-10-09','event_date':'2026-09-08','investment_decision':'行业方向、条件规模与公司敞口；不作买卖建议','scope':'全球服务器 CPU 为主；端侧仅检验替代边界。事件研究，不扩展完整行业链或 standalone-BOM 项目。','biggest_uncertainty':'每活跃用户的真实 CPU/内存驻留时间及其增量采购转化','counterfactual':'无 Muse 时已有云服务、AI 执行环境与服务器更新需求','maximum_depth':5}
nodes=[{'id':i,'parent_id':p,'level':3,'question':q,'why_it_matters':why,'required_materials':data,'indicators':data,'analysis_plan':a,'support_rule':'当前问题的原始材料直接支持限定结论','refute_rule':'存在相反部署、成本或需求证据，或关键量化变量尚未披露','update_cadence':'event_driven'} for i,p,q,why,data,a in specs]
project={'project_id':P.name,'title':'Meta Muse 发布对 CPU 市场的影响','research_type':'event_cpu_market','domain_playbook':'ai_factory','presentation_profile':'question-tree-v1','report_scope':'research-project','run_mode':'live','as_of_date':'2026-10-09','research_goal':goal,'research_status':'in_progress','scope_note':goal['scope']}
universe=FileSystemSourceUniverseRepository(ROOT/'config/source_universes.json').resolve_for_research(project)
write(P/'source_universe.json', universe)
write(P/'project.json',project)
write(P/'research_goal.json',goal)
write(P/'question_design.json',{'review':'可执行','rationale':'研究对象—CPU 市场传导—真实公司；范围限定事件对 CPU 市场影响，非完整产业链','initial_depth':3,'nodes':nodes,'delegation':'DeepSeek MCP 不可用；投资分析、来源复核与本地操作由 GPT 执行。'})
base={'plan_id':'muse_cpu_initial','research_goal':goal,'steps':[]}
for j,n in enumerate(nodes,1):
    base['steps'].append({'step_id':'rollup:'+n['id'],'question_node_id':n['id'],'stage_id':n['parent_id'],'sequence':j,'question':n['question'],'decision_use':n['why_it_matters'],'depends_on_step_ids':[],'freshness_requirement':'资料发布日期不晚于 2026-10-09；当前网页记录抓取日与更新日。','refuting_source_plan':[n['refute_rule']],'answer_contract':{'required_fields':['answer','supporting_findings','refuting_findings','gaps','next_actions']},'traceability_contract':{'required_references':['source_ids','source_extraction_ids','source_review_ids']}})
parent=upgrade_parent_plan_for_l3_plans(base)
index, plans=build_l3_research_plan_set(l3_nodes=nodes,parent_plan_id=parent['plan_id'],research_goal=goal,source_universe=universe)
write(P/'research_plan.json',parent)
write(P/'research_plan_history'/f"{parent['plan_id']}.json",parent)
write(P/'l3_research_plans/index.json',index)
for plan in plans:
    n=next(n for n in nodes if n['id']==plan['l3_node_id'])
    # Enrich before any execution; retain domain-created IDs and contracts.
    plan['steps'][0]['analysis_plan']=n['analysis_plan']
    plan['steps'][0]['refuting_source_plan']=[n['refute_rule']]
    plan['question_tree']['analysis_plan']=n['analysis_plan']
    d=P/'l3_research_plans'/n['id']
    write(d/'research_plan.json',plan)
    write(d/'research_plan_history'/f"{plan['plan_id']}.json",plan)
    append(P/'research_events.jsonl',{'event_type':'question_created','recorded_at':NOW,'question_id':n['id'],'level':3,'question':n['question'],'plan_id':plan['plan_id']})
write(P/'qa_tree.json',{'schema_version':'4.0','project_id':P.name,'root':{'id':'MUSE','level':1,'question':'Meta Muse 发布将怎样影响 CPU 市场？','children':[{'id':i,'level':2,'question':q,'children':[n for n in nodes if n['parent_id']==i]} for i,q in [('O','Muse 是什么，发生了什么变化？'),('I','它怎样影响 CPU 市场？'),('C','具体影响哪些公司？')]]}})
print(json.dumps({'project':str(P),'plans':[{k:v for k,v in p.items() if k in ['plan_id','l3_node_id']} for p in plans]},ensure_ascii=False))
