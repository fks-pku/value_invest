"""Materialize the authored 2026-09-22 research revision; never generate claims.

The JSON input owns questions, source-specific readings, judgments and prose.
Existing domain plans, append-only ledgers and canonical renderers own contracts.
"""
from datetime import datetime, timezone
import argparse
import hashlib
import json

from gpt6_impact_research import (PROJECT, ROOT, append_unique, read_lines, record_question,
    render_plan, write_json, ResearchGoal, DomainPlaybook, QuestionTemplate,
    QuestionNode, QuestionArchitecture, build_research_plan, enrich_question_architecture,
    build_l3_research_plan_set, FileSystemResearchPlanRepository,
    FileSystemSourceUniverseRepository, ValidateResearchPlanExecution, ReportViewModel)
from refine_gpt6_report import archive_before
from render_gpt6_impact_report import EventHtmlReportRenderer, EventMarkdownReportRenderer
from value_invest_research.framework_contracts import validate_report_contract_html, validate_report_contract_markdown
from value_invest_research.adapters.outbound.research_plan_markdown_renderer import ResearchPlanMarkdownRenderer

RID = "20260922_object_industry_company_execution"
INPUT = PROJECT / "object_industry_company_research.json"


def read(name):
    return json.loads((PROJECT / name).read_text())


def render_active_plan(project):
    repo = FileSystemResearchPlanRepository(PROJECT)
    bundle = repo.load_l3_research_plan_bundle()
    parents = {n["id"]: n.get("parent_id") for n in bundle["qa_tree"]["nodes"]}
    specifications = {q["id"]: q for q in read("research_brief.json")["questions"]}
    # Group the reading view by actual L2 parents, not the BOM-specific lens hint.
    bundle["plans"] = [{**p, "lens_id": parents[p["l3_node_id"]],
        "question_tree": {**p["question_tree"],
            "analysis_plan": [specifications[p["l3_node_id"]]["analysis"]]}}
        for p in bundle["plans"]]
    repo.write_research_plan_markdown(ResearchPlanMarkdownRenderer().render(project=project, bundle=bundle))


def include_target_boundary(tree, synthesis, targets):
    """Keep the Markdown target sidecar and HTML's company rollup claim-identical."""
    company = next(n for n in tree["nodes"] if n["id"] == "F1.3")
    if any(p["heading"] == "投资边界与观察对象" for p in company["analysis"]):
        return
    company["analysis"].append({"heading": "投资边界与观察对象",
        "paragraphs": [synthesis["target_boundary"], synthesis["next_validation"]],
        "tables": [{"caption": "研究观察清单，非推荐排名", "headers": ["公司／状态", "业务敞口", "待验证", "风险"],
            "rows": [[f"{t['company']} · {t['ticker']} / no_action", t["exposure"], t["needed"], t["risk"]] for t in targets]}]})


def initialize():
    if (PROJECT / "research_revisions" / RID / "completed.json").exists():
        raise ValueError("Research revision already materialized; use finish to reproduce, not init")
    data = read(INPUT.name)
    archive_before(PROJECT / "research_revisions" / RID)
    prior = read("project.json")
    brief = {k: v for k, v in prior.items() if k not in {"questions", "groups", "question_tree", "synthesis"}}
    brief.update(meta_question=data["question"], groups=data["groups"], questions=data["questions"],
                 framework_revision=RID, research_status="in_progress", research_performed_on="2026-09-22")
    goal = ResearchGoal(topic=data["question"], research_type="event", object_id=brief["project_id"],
        as_of_date=brief["as_of_date"], report_date=brief["report_date"],
        decision_boundary=brief["decision_boundary"], domain_hint="gpt6_launch_event")
    templates = [QuestionTemplate(id=g["id"], question=g["question"], why_this_depth=g["purpose"],
        l3_questions=[q for q in data["questions"] if q["parent_id"] == g["id"]]) for g in data["groups"]]
    playbook = DomainPlaybook(playbook_id="gpt6_object_industry_company", research_type="event_policy",
        q_map={"F1": data["question"]}, mechanism_buckets=[g["question"] for g in data["groups"]],
        l2_templates={"F1": templates}, quality_rule="研究对象→行业与BOM→具体公司；逐题取证，不继承旧问题通过状态。")
    nodes = [QuestionNode(id="F1", level=1, question=data["question"], next_question_ids=[g["id"] for g in data["groups"]])]
    for g in data["groups"]:
        nodes.append(QuestionNode(id=g["id"], level=2, parent_id="F1", question=g["question"],
            next_question_ids=[q["id"] for q in data["questions"] if q["parent_id"] == g["id"]]))
        for q in [q for q in data["questions"] if q["parent_id"] == g["id"]]:
            nodes.append(QuestionNode(id=q["id"], level=3, parent_id=g["id"], question=q["question"],
                required_materials=q["data"], decision_use=q["analysis"], support_evidence=q["support_rule"],
                refute_evidence=q["refute"], preferred_specialty_skill="dynamic-research-agent"))
    architecture = QuestionArchitecture(goal, playbook, "用户指定三部分主线；初始只到L3，按真实研究缺口扩展。", nodes)
    universe = FileSystemSourceUniverseRepository(ROOT / "config/source_universes.json").resolve_for_research({"domain_playbook": "ai_factory"})
    universe["event_supplement"] = ["dated OpenAI releases", "benchmark authors", "customer primary disclosures", "company IR and filings"]
    plan_obj = build_research_plan(architecture, source_universe=universe)
    plan = plan_obj.to_dict()
    repo = FileSystemResearchPlanRepository(PROJECT)
    index, children = build_l3_research_plan_set(l3_nodes=[n.to_dict() for n in nodes if n.level == 3],
        parent_plan_id=plan["plan_id"], research_goal=goal.to_dict(), source_universe=universe)
    repo.save_question_architecture(enrich_question_architecture(architecture, plan_obj))
    repo.save_plan(plan)
    repo.save_l3_research_plans(index, children)
    repo.bind_l3_plans_to_question_architecture(parent_plan=plan, index=index)
    brief["source_universe"] = universe
    write_json(PROJECT / "research_brief.json", brief)
    write_json(PROJECT / "project.json", brief)
    render_active_plan(brief)
    append_unique(PROJECT / "research_events.jsonl", [{"event_id": RID + "_plan_" + plan["plan_id"],
        "recorded_at": datetime.now(timezone.utc).isoformat(), "revision_id": RID,
        "event_type": "framework_activated", "question_ids": [q["id"] for q in data["questions"]],
        "as_of_date": brief["as_of_date"], "prior_evidence_policy": "candidate_only; no inherited passes"}], "event_id")
    print("Active L3 plans:", len(children))


def finish():
    if read("project.json").get("interactive_revision"):
        raise ValueError("This project has an interactive research revision; the legacy authored-input materializer cannot overwrite it. Use the local researcher or render the current question_tree_report.json.")
    data = {**read(INPUT.name), **read("object_industry_company_findings.json")}
    digest = hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    completion = PROJECT / "research_revisions" / RID / "completed.json"
    if completion.exists() and json.loads(completion.read_text())["input_sha256"] != digest:
        raise ValueError("Completed research input is immutable; create another revision to change claims")
    if completion.exists():
        vm = ReportViewModel(**read("report_view_model.json"))
        include_target_boundary(vm.project["question_tree"], vm.project["synthesis"], vm.targets)
        write_json(PROJECT / "question_tree_report.json", vm.project["question_tree"])
        vm.project["revised_on"] = "2026-09-22"
        write_json(PROJECT / "project.json", vm.project)
        write_json(PROJECT / "report_view_model.json", vm.to_dict())
        write_json(PROJECT / "source_catalog.json", vm.sources)
        run = read("research_run.json")
        run.update(visual_review="blocked_by_browser_local_file_url_policy; not_claimed",
                   market_price_analysis="9/10 unadjusted closes cross-checked; mechanical valuation scenarios only")
        write_json(PROJECT / "research_run.json", run)
        validation = read("presentation_validation.json")
        validation["visual_review"] = run["visual_review"]
        write_json(PROJECT / "presentation_validation.json", validation)
        EventHtmlReportRenderer().write(PROJECT, vm)
        EventMarkdownReportRenderer().write(PROJECT, vm)
        render_active_plan(vm.project)
        print("Re-rendered saved view model; evidence and states unchanged")
        return
    chapters, sources, syn = data["chapters"], data["sources"], data["synthesis"]
    qa, project = read("qa_tree.json"), read("project.json")
    expected = {n["id"] for n in qa["nodes"] if not n.get("next_question_ids")}
    assert expected == {r["id"] for r in chapters}, "Every current leaf must have authored research"
    for row in chapters:
        record_question(row, "leaf_20260922", performed_on="2026-09-22")
    append_unique(PROJECT / "sources.jsonl", sources, "source_id")
    append_unique(PROJECT / "material_intake/documents.jsonl", [dict(s, document_id="document_" + s["source_id"],
        intake_role="source registration only; evidence requires question-specific review") for s in sources], "document_id")
    source_map = {s["source_id"]: s for s in sources}
    claims = [c for c in read_lines(PROJECT / "ledger/claims.jsonl") if "_leaf_20260922_" in c["claim_id"]]
    append_unique(PROJECT / "ledger/claim_temporal_envelopes.jsonl", [dict(claim_id=c["claim_id"],
        published_at=source_map[c["source_id"]]["published_at"], effective_period=source_map[c["source_id"]]["effective_period"],
        target_period="", ingested_at=c["ingested_at"], as_of_date=project["as_of_date"],
        publication_date_status="verified", visibility_proof=source_map[c["source_id"]]["publication_date_source"])
        for c in claims], "claim_id")
    rows = {r["id"]: r for r in [*chapters, *syn["nodes"]]}
    specs = {q["id"]: q for q in data["questions"] + data["groups"]}
    nodes, states = [], []
    def gaps(nid):
        own = list(rows[nid]["gaps"])
        for child in [n for n in qa["nodes"] if n.get("parent_id") == nid]:
            own.extend(gaps(child["id"]))
        return list(dict.fromkeys(own))
    for q in qa["nodes"]:
        nid, row = q["id"], rows[q["id"]]
        children = q.get("next_question_ids", [])
        node = dict(id=nid, parent_id=q.get("parent_id") or "", level=q["level"], question=q["question"],
            short=q["question"], what=q["question"], mode="rollup" if children else "leaf",
            why_it_matters=specs.get(nid, {}).get("purpose", "回答元问题"),
            data_required=specs.get(nid, {}).get("data", ["直接子问题的结论与缺口"]),
            acceptance_rule="逐题事实可追溯；反证与边界明确；缺口影响主要答案则不通过。",
            conclusion=row["conclusion"], passed=row["passed"], analysis=row["analysis"],
            evidence=row.get("evidence", []), gaps=gaps(nid), reasons=[row["gate_reason"]],
            next_actions=row["next_actions"], refutation=row.get("refutation", ""), tables=[])
        nodes.append(node)
        states.append(dict(state_id=RID + "_" + nid, question_id=nid, as_of_date=project["as_of_date"],
            recorded_at=datetime.now(timezone.utc).isoformat(), revision_id=RID, conclusion=row["conclusion"],
            passed=row["passed"], gaps=node["gaps"], status="answered" if row["passed"] else "blocked",
            children=children, state_basis="child rollup" if children else "new question-specific research"))
    append_unique(PROJECT / "ledger/node_states.jsonl", states, "state_id")
    project.update(research_status="partial_research", current_judgment=rows["F1"]["conclusion"],
        source_note="本轮于2026-09-22逐题核读；仅使用截至2026-09-10已公开的有日期材料。动态网页可能更新，历史可见性以具日期原文为依据。基准不是生产财务结果；机制情景不是盈利预测。")
    tree = dict(template_version="question-tree-v1", title="GPT-6：研究对象、行业与BOM、具体公司", as_of_date=project["as_of_date"],
        subtitle="研究执行：2026-09-22 · 历史证据截面：2026-09-10 · 按问题逐题取证与分析",
        status_label=f"阶段性研究 · {sum(not n['passed'] and n['mode']=='leaf' for n in nodes)} 个叶子仍有缺口",
        nodes=nodes, sources=sources, source_note=project["source_note"],
        attachments=[{"label":"研究计划", "href":"research_plan.md"}, {"label":"完整 Markdown", "href":"professional_report.md"}])
    project.update(presentation_profile="question-tree-v1", question_tree=tree, synthesis=syn)
    include_target_boundary(tree, syn, data["targets"])
    vm = ReportViewModel(project=project, goal={"topic":data["question"]}, supply_chain={"scope":"event-study"},
        qa_roots=chapters, sources=sources, targets=data["targets"])
    html, md = EventHtmlReportRenderer().render(vm), EventMarkdownReportRenderer().render(vm)
    validation = {"html":validate_report_contract_html(html), "markdown":validate_report_contract_markdown(md)}
    assert all(v["ok"] for v in validation.values()), validation
    plan_validation = ValidateResearchPlanExecution(FileSystemResearchPlanRepository(PROJECT)).execute()
    assert plan_validation["ok"], plan_validation
    for name, content in {"project.json":project, "research_chapters.json":chapters, "report_synthesis.json":syn,
        "question_tree_report.json":tree, "report_view_model.json":vm.to_dict(), "target_gates.json":data["targets"],
        "source_catalog.json":sources,
        "plan_validation.json":plan_validation, "presentation_validation.json":validation,
        "research_run.json":{"status":"partial_research", "revision_id":RID, "as_of_date":project["as_of_date"],
            "performed_on":"2026-09-22", "unanswered_leaf_ids":[r["id"] for r in chapters if not r["passed"]],
            "source_count":len(sources), "claim_count":len(claims), "external_archive_scan":"not_performed",
            "visual_review":"blocked_by_browser_local_file_url_policy; not_claimed", "reproduce":"PYTHONPATH=src python3 tools/research_gpt6_new_framework.py finish"}}.items():
        write_json(PROJECT / name, content)
    EventHtmlReportRenderer().write(PROJECT, vm)
    EventMarkdownReportRenderer().write(PROJECT, vm)
    render_active_plan(project)
    write_json(completion, {"revision_id":RID,
        "input_sha256":digest, "status":"partial_research", "validation":validation})
    print(json.dumps(plan_validation["summary"], ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["init", "finish"])
    args = parser.parse_args()
    (initialize if args.action == "init" else finish)()
