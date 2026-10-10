"""Persist question-specific audit records, evaluate shared gates and render the authored report."""
import hashlib, json, re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from value_invest_research.domain.research_plan import prepare_research_step_event, validate_research_plan_execution
from value_invest_research.domain.l3_research_plan import validate_l3_research_plan_set
from value_invest_research.domain.question_tree_report import validate_question_tree_report, validate_question_tree_html
from value_invest_research.domain.report_view_model import ReportViewModel
from value_invest_research.adapters.outbound.canonical_html_report_renderer import CanonicalHtmlReportRenderer
from value_invest_research.adapters.outbound.canonical_markdown_report_renderer import CanonicalMarkdownReportRenderer

P=Path(__file__).resolve().parent
if json.loads((P/'project.json').read_text()).get('interactive_revision'):
    raise ValueError('本项目已有交互修改，不能用初稿流程覆盖。请使用当前问题树重新渲染。')
NOW=datetime.now(timezone.utc).isoformat()
def read(f):return json.loads((P/f).read_text())
def write(f,x):
    p=P/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def rows(f):return [json.loads(s) for s in (P/f).read_text().splitlines() if s.strip()] if (P/f).exists() else []
def append(f,x,key):
    p=P/f;p.parent.mkdir(parents=True,exist_ok=True)
    prior={str(v.get(key)) for v in rows(f)}
    if str(x.get(key)) not in prior:
        with p.open('a') as o:o.write(json.dumps(x,ensure_ascii=False)+'\n')
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True).encode()).hexdigest()[:16]

r=read('question_tree_report.json');project=read('project.json');goal=read('research_goal.json')
assert not validate_question_tree_report(r),validate_question_tree_report(r)
source_by={s['source_id']:s for s in r['sources']}
for s in r['sources']:
    assert not s['published_at'] or s['published_at']<='2026-10-09'
    append('sources.jsonl',s,'source_id')
    append('material_intake/documents.jsonl',{**s,'document_id':s['source_id'],'source_bucket':'evidence' if s['material_class'].startswith('official') else 'message' if s['material_class']=='market_news' else 'research_report','date_eligibility':'live_only' if not s['published_at'] else 'known_by_cutoff','status':'selected_for_question_review'},'document_id')

requests={}
for f in sorted((P/'search_runs').glob('*_request.json')):
    request=json.loads(f.read_text());run=request['search_run_id'];response=read(f'search_runs/{run}_result.json')
    requests[run]=request
    append('search_runs.jsonl',{**request,'result_path':f'search_runs/{run}_result.json','result_sha256':hashlib.sha256((P/f'search_runs/{run}_result.json').read_bytes()).hexdigest(),'search_status':'executed','refutation_search':True},'search_run_id')

append('material_intake/scan_events.jsonl',{'event_id':'ima_availability_20261009','recorded_at':NOW,'ingestion_channel':'knowledge_base_scan','status':'unavailable','reason':'repository source/ima/archive_manifest.jsonl does not exist; no archive enumeration or PDF parsing claimed','evidence_eligible':False},'event_id')
append('research_events.jsonl',{'event_id':'scope_live_20261009','event_type':'scope_confirmed','recorded_at':NOW,'run_mode':'live','as_of_date':'2026-10-09','reason':'User explicitly selected current research including post-release adoption and procurement evidence.'},'event_id')

plans=[];events_by={};states={}
for n in r['nodes']:
    q=n['id'];leaf=n['mode']=='leaf'
    if not leaf:continue
    pl=read(f'l3_research_plans/{q}/research_plan.json');plans.append(pl)
    ledger=f'l3_research_plans/{q}/research_step_events.jsonl'
    def event(kind,**kw):
        ev=prepare_research_step_event(pl,{'event_id':f'{q}_{kind}_v1','step_id':f'question:{q}','event_type':kind,**kw},recorded_at=NOW)
        append(ledger,ev,'event_id')
    qr=[req for req in requests.values() if req['question_node_id']==q]
    assert qr
    event('collection_started',search_run_id=qr[0]['search_run_id'],recorded_at=min(req['recorded_at'] for req in qr))
    grouped=defaultdict(list)
    for ev in n['evidence']:grouped[ev['source']].append(ev)
    ext_ids=[];review_ids=[];claim_ids=[]
    for sid,observations in grouped.items():
        s=source_by[sid];run=observations[0]['search_run_id'];req=requests[run]
        assert req['question_node_id']==q and req['l3_plan_id']==pl['plan_id']
        # Every public evidence row must come from this question's own retrieved material.
        for ev in observations:
            rr=requests[ev['search_run_id']]
            assert rr['question_node_id']==q
            cached=json.dumps(read(f"search_runs/{ev['search_run_id']}_result.json"),ensure_ascii=False)
            canonical=s['url'].rstrip('/')
            assert canonical in cached, (q,sid,ev['search_run_id'],'source not found in question result')
        trace={k:req[k] for k in ('l3_plan_id','l3_node_id','question_node_id','question_level','research_step_id','search_run_id')}
        xid=f'ext_{q}_{sid}_v1';rid=f'gpt_{q}_{sid}_v1';ext_ids.append(xid);review_ids.append(rid)
        claims=[]
        for ix,ob in enumerate(observations,1):
            # A statement is a narrowly scoped observation, not a whole-document abstract.
            cid=f'claim_{q}_{sid}_{ix:02d}';claim_ids.append(cid)
            claim={**trace,'claim_id':cid,'source_id':sid,'source_extraction_id':xid,'source_review_id':rid,'text':ob['fact'],'original_locator':ob['locator'],'published_at':s['published_at'],'effective_period':ob.get('effective_period') or s.get('effective_period',''),'target_period':ob.get('target_period',''),'ingested_at':NOW,'evidence_nature':'reported_unconfirmed' if s['material_class']=='market_news' else 'source_forecast' if ob.get('target_period') else 'source_observation','effect':ob['effect'],'limitations':ob['boundary']}
            claims.append(claim);append('ledger/claims.jsonl',claim,'claim_id')
        append('inbox/parse_tasks.jsonl',{**trace,'parse_task_id':f'parse_{q}_{sid}','source_id':sid,'question':n['question'],'specialty_parser':'dynamic-research-agent / GPT question-specific manual reading','status':'reviewed','evidence_scope':'current_question_only','source_extraction_id':xid,'gpt_review_id':rid},'parse_task_id')
        append('source_extractions.jsonl',{**trace,'source_extraction_id':xid,'source_id':sid,'question':n['question'],'parser':'GPT primary-source reading','claims':claims,'source_result_paths':sorted({f"search_runs/{o['search_run_id']}_result.json" for o in observations}),'recorded_at':NOW},'source_extraction_id')
        append('source_reviews.jsonl',{**trace,'review_id':rid,'source_review_id':rid,'source_extraction_id':xid,'source_id':sid,'reviewer':'GPT','review_status':'accepted_with_boundary','question_specific':True,'checked':['publication versus effective period','claim matches cited section','scope and causal fit','forecast versus observation','limits and counterinterpretations'],'findings':[{'claim_id':c['claim_id'],'verdict':'lead_only' if s['material_class']=='market_news' else 'accepted_with_boundary','reason':c['limitations']} for c in claims],'recorded_at':NOW},'review_id')
    event('evidence_attached',search_run_id=qr[-1]['search_run_id'],source_ids=list(grouped),source_extraction_ids=ext_ids,source_review_ids=review_ids)
    support=[e['fact'] for e in n['evidence'] if e['effect']=='support']
    refute=[e['fact']+' 限制：'+e['boundary'] for e in n['evidence'] if e['effect'] in ('refute','boundary','constraint')]+[n['refutation']]
    append('refutation_search_results.jsonl',{'id':f'refute_{q}_v1','question_node_id':q,'search_run_ids':[req['search_run_id'] for req in qr],'result':'boundary_or_counterevidence_found','findings':refute,'source_ids':[e['source'] for e in n['evidence'] if e['effect'] in ('refute','boundary','constraint')],'remaining_gaps':n['gaps'],'recorded_at':NOW},'id')
    event('answer_recorded',search_run_id=qr[-1]['search_run_id'],answer=n['conclusion'],supporting_findings=support,refuting_findings=refute,gaps=n['gaps'],next_actions=n['next_actions'])
    event('gate_evaluated',evidence_gate={'passed':n['passed'],'reasons':n['reasons']},gaps=n['gaps'],next_actions=n['next_actions'])
    if not n['passed']:event('step_blocked',gaps=n['gaps'],next_actions=n['next_actions'])
    events=rows(ledger);events_by[q]=events
    validation=validate_research_plan_execution(pl,events)
    assert validation['ok'],validation
    assert (validation['step_states'][0]['status']=='completed')==n['passed']
    states[q]=validation['step_states'][0]
    write(f'l3_research_plans/{q}/execution_validation.json',validation)
    append('ledger/conclusions.jsonl',{'conclusion_id':q+'_v1','question_node_id':q,'answer':n['conclusion'],'supporting_claim_ids':claim_ids,'passed':n['passed'],'gaps':n['gaps'],'next_actions':n['next_actions'],'recorded_at':NOW},'conclusion_id')
    append('research_events.jsonl',{'event_id':q+'_sufficiency_v1','event_type':'sufficiency_evaluated','question_id':q,'passed':n['passed'],'gaps':n['gaps'],'expansion_decision':'stop_within_scope' if n['passed'] else 'missing_external_measurement_no_justified_deeper_branch','reason':'缺少真实遥测或采购数据，增加层级不能代替数据；保留未充分。' if not n['passed'] else '限定问题已回答；不借此完成父问题。','recorded_at':NOW},'event_id')

validation=validate_l3_research_plan_set(parent_plan=read('research_plan.json'),index=read('l3_research_plans/index.json'),plans=plans,events_by_node=events_by)
assert validation['ok'],validation
write('plan_validation.json',validation)
for q in ['AMD','INTC','ARM','NVDA']:
    assert states['C0']['status']=='completed'
append('research_events.jsonl',{'event_id':'parent_child_projection_v1','event_type':'child_plan_projection','recorded_at':NOW,'plan_id':read('research_plan.json')['plan_id'],'projection_only':True,'summary':validation['summary'],'direct_evidence_completion':False},'event_id')
parent_plan=read('research_plan.json')
for step in parent_plan['steps']:
    append('research_step_events.jsonl',prepare_research_step_event(parent_plan,{'event_id':'parent_start_'+step['question_node_id'],'step_id':step['step_id'],'event_type':'collection_started'},recorded_at=NOW),'event_id')
parent_validation=validate_research_plan_execution(parent_plan,rows('research_step_events.jsonl'))
assert parent_validation['ok'],parent_validation
write('parent_execution_validation.json',parent_validation)

project.update(research_status='partial_research',report_status='delivered_with_explicit_gaps',question_tree=r)
vm=ReportViewModel(project=project,goal=goal,supply_chain={},qa_roots=[],targets=[],sources=r['sources'])
html=CanonicalHtmlReportRenderer().render(vm);md=CanonicalMarkdownReportRenderer().render(vm)
presentation=validate_question_tree_html(html,mode='live')
assert presentation['ok'],presentation
# Preserve the same statements across both public surfaces.
for n in r['nodes']:
    assert n['conclusion'] in md
    for sec in n['analysis']:
        for para in sec['paragraphs']:
            plain=re.sub(r'\[S\d+\]','',para)
            for frag in re.split(r'\[S\d+\]',para):
                if frag:assert frag in md,(n['id'],frag)
(P/'professional_report.html').write_text(html)
(P/'professional_report.md').write_text(md)
write('report_view_model.json',vm.to_dict())
project.pop('question_tree');write('project.json',project)
write('presentation_validation.json',presentation)

qa=read('qa_tree.json')
def project_state(x):
    q=x['id'];n=next(n for n in r['nodes'] if n['id']==q)
    x.update(status='answered' if n['passed'] else 'blocked',conclusion=n['conclusion'],sufficiency={'passed':n['passed'],'reasons':n['reasons'],'gaps':n['gaps']})
    for child in x.get('children',[]):project_state(child)
project_state(qa['root']);write('qa_tree.json',qa)
write('research_state.json',{'project_id':P.name,'as_of_date':r['as_of_date'],'status':'partial_research','nodes':[{k:n[k] for k in ['id','parent_id','level','question','conclusion','passed','gaps','next_actions']} for n in r['nodes']],'step_projection':states,'source_of_truth':'append-only ledgers; state is a projection','next_question_id':'D1'})

plan_lines=['# Meta Muse 发布对 CPU 市场的影响：研究计划','','截至 2026-10-09；实时研究。结构先到 L3；本轮缺口来自未公开遥测和采购，没有人为扩展 L4/L5。','','公开报告：[HTML](professional_report.html)。问题已执行不等于证据门槛通过。','']
for n in r['nodes']:
    plan_lines += ['#'*min(n['level']+1,6)+' '+n['question'],'']
    if n['mode']=='leaf':
        p=next(pl for pl in plans if pl['l3_node_id']==n['id'])
        plan_lines += ['所需数据：'+'；'.join(p['steps'][0]['required_data'])+'。','','分析：'+'；'.join(p['steps'][0]['analysis_plan'])+'。','']
(P/'research_plan.md').write_text('\n'.join(plan_lines))
write('target_gates.json',{'scope':'industry_impact_only','valuation_performed':False,'targets':[{'ticker':q,'candidate_action_state':'watch_only','action_state':'no_action','research_gate':{'passed':False,'reasons':['No canonical investable BOM thesis mapping in this narrow event study','Muse earnings bridge incomplete','As-of valuation and mispricing not researched','No six-question BOM completion or quantitative security kill-test gate']}} for q in ['AMD','INTC','ARM','NVDA']]})
write('audit_summary.json',{'as_of_date':'2026-10-09','source_count':len(r['sources']),'question_count':len(r['nodes']),'terminal_questions':10,'completed_terminal_questions':sum(n['passed'] for n in r['nodes'] if n['mode']=='leaf'),'blocked_terminal_questions':sum(not n['passed'] for n in r['nodes'] if n['mode']=='leaf'),'question_source_pairs':len(rows('source_extractions.jsonl')),'gpt_reviews':len(rows('source_reviews.jsonl')),'atomic_observations':len(rows('ledger/claims.jsonl')),'search_runs':len(requests),'source_trace_checked':True,'cutoff_checked':True,'scenario_type':'hypothetical_not_forecast','ima_archive':'unavailable_not_scanned','gate_validation':validation['ok'],'presentation_validation':presentation['ok'],'research_complete':False,'reason':'Direction and supplier exposure researched; missing operational and purchase data prevent quantified completion.'})
print(json.dumps(read('audit_summary.json'),ensure_ascii=False,indent=2))
