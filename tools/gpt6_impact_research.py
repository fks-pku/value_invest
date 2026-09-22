"""Materialize this event study with existing plan contracts; never perform research in a renderer."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from value_invest_research.domain.research_goal import ResearchGoal
from value_invest_research.domain.domain_playbooks import DomainPlaybook, QuestionTemplate
from value_invest_research.domain.question_architecture import QuestionArchitecture, QuestionNode
from value_invest_research.domain.research_plan import build_research_plan, enrich_question_architecture
from value_invest_research.domain.l3_research_plan import build_l3_research_plan_set
from value_invest_research.adapters.outbound.filesystem_research_plan import FileSystemResearchPlanRepository
from value_invest_research.adapters.outbound.filesystem_source_universe import FileSystemSourceUniverseRepository
from value_invest_research.application.use_cases.research_plan_execution import RecordResearchStepEvent, ValidateResearchPlanExecution
from value_invest_research.application.use_cases.expand_l3_research_plan import ExpandL3ResearchPlan
from value_invest_research.domain.report_view_model import ReportViewModel

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "research/events/gpt6_ai_industry_impact_20260910"


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_unique(path, rows, key):
    path.parent.mkdir(parents=True, exist_ok=True)
    previous = {r[key]: r for r in read_lines(path)}
    with path.open("a", encoding="utf-8") as out:
        for row in rows:
            if row[key] not in previous:
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                previous[row[key]] = row


def read_lines(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()] if path.exists() else []


def record_question(row, stage, *, performed_on="2026-09-10"):
    """Persist explicitly authored question/source pairs, not a broad source-pool mapping."""
    l3 = row["l3_id"]
    repo = FileSystemResearchPlanRepository(PROJECT / "l3_research_plans" / l3)
    plan = repo.load_plan()
    step = next(s for s in plan["steps"] if s["question_node_id"] == row["id"])
    run = f"search_{row['id']}_{stage}"
    trace = dict(l3_plan_id=plan["plan_id"], l3_node_id=l3, question_node_id=row["id"],
                 question_level=step["level"], research_step_id=step["step_id"], search_run_id=run)
    now = datetime.now(timezone.utc).isoformat()
    append_unique(PROJECT / "search_runs.jsonl", [{**trace, "recorded_at": now,
        "performed_on": performed_on, "queries_or_selections": row["searches"],
        "refutation_search_result": row["refutation"], "timing_note": "从本次实际浏览记录登记；不伪造每次检索的精确时间。",
        "acquisition": "question_search_and_question_specific_source_selection",
        "external_archive_scan": "not_performed; no archive evidence claimed"}], "search_run_id")
    rec = RecordResearchStepEvent(repo)
    def event(kind, **kwargs):
        rec.execute(dict(event_id=f"event_{row['id']}_{stage}_{kind}", step_id=step["step_id"],
                         event_type=kind, search_run_id=run, **kwargs))
    event("collection_started")
    extracts, reviews, claims, tasks = [], [], [], []
    for i, pair in enumerate(row["evidence"], 1):
        xid = f"extract_{row['id']}_{stage}_{i:02d}"
        rid = f"review_{row['id']}_{stage}_{i:02d}"
        cid = f"claim_{row['id']}_{stage}_{i:02d}"
        tasks.append({**trace, "parse_task_id": f"parse_{row['id']}_{stage}_{i:02d}",
                      "source_id": pair["source"], "source_extraction_id": xid, "source_review_id": rid,
                      "parser": "GPT question-specific reading", "status": "reviewed", "recorded_at": now})
        extracts.append({**trace, "extraction_id": xid, "source_id": pair["source"],
                         "locator": pair["locator"], "fact": pair["fact"], "boundary": pair["boundary"],
                         "source_review_id": rid, "recorded_at": now})
        reviews.append({**trace, "review_id": rid, "extraction_id": xid, "source_id": pair["source"],
                        "reviewer": "GPT", "decision": "verified_with_stated_boundary", "review": pair["review"], "recorded_at": now})
        claims.append({**trace, "claim_id": cid, "source_id": pair["source"], "extraction_id": xid,
                       "review_id": rid, "claim": pair["fact"], "locator": pair["locator"],
                       "effect": pair["effect"], "boundary": pair["boundary"], "ingested_at": now})
    append_unique(PROJECT / "inbox/parse_tasks.jsonl", tasks, "parse_task_id")
    append_unique(PROJECT / "source_extractions.jsonl", extracts, "extraction_id")
    append_unique(PROJECT / "source_reviews.jsonl", reviews, "review_id")
    append_unique(PROJECT / "ledger/claims.jsonl", claims, "claim_id")
    event("evidence_attached", source_ids=list(dict.fromkeys(p["source"] for p in row["evidence"])),
          source_extraction_ids=[x["extraction_id"] for x in extracts], source_review_ids=[r["review_id"] for r in reviews])
    event("answer_recorded", answer=row["conclusion"], supporting_findings=row["support"],
          refuting_findings=[row["refutation"]], gaps=row["gaps"], next_actions=row["next_actions"])
    event("gate_evaluated", evidence_gate={"passed": row["passed"], "reasons": [row["gate_reason"]]},
          gaps=row["gaps"], next_actions=row["next_actions"])
    append_unique(PROJECT / "ledger/conclusions.jsonl", [{**trace, "conclusion_id": f"conclusion_{row['id']}_{stage}",
        "recorded_at": now, "as_of_date": "2026-09-10", "conclusion": row["conclusion"], "passed": row["passed"],
        "gaps": row["gaps"], "analysis": row.get("analysis", []), "source_review_ids": [r["review_id"] for r in reviews]}], "conclusion_id")


def expand_initial():
    journal = json.loads((PROJECT / "initial_findings.json").read_text())
    repo = FileSystemResearchPlanRepository(PROJECT)
    for row in journal:
        current = FileSystemResearchPlanRepository(PROJECT / "l3_research_plans" / row["l3_id"]).load_plan()
        if current["expansion_history"]:
            continue
        record_question(row, "initial")
        result = ExpandL3ResearchPlan(repo).execute(l3_node_id=row["l3_id"], parent_question_id=row["id"],
            child_questions=row["children"], evidence_gaps=row["gaps"],
            source_universe=json.loads((PROJECT / "project.json").read_text())["source_universe"])
        print(json.dumps(result, ensure_ascii=False))


def finish():
    chapters = json.loads((PROJECT / "research_chapters.json").read_text())
    catalog = json.loads((PROJECT / "source_catalog.json").read_text())
    synthesis = json.loads((PROJECT / "report_synthesis.json").read_text())
    for row in chapters:
        record_question(row, "leaf")
    sources = [{**s, "ingestion_channel": "question_search", "retrieved_on": "2026-09-10"} for s in catalog]
    append_unique(PROJECT / "sources.jsonl", sources, "source_id")
    append_unique(PROJECT / "material_intake/documents.jsonl", [
        {"document_id": f"document_{s['source_id']}", "source_id": s["source_id"], "url": s["url"],
         "material_class": s["material_class"], "ingestion_channel": "question_search",
         "published_at": s["published_at"], "publication_date_status": s["publication_date_status"],
         "original_local_path": "", "storage_note": "web original; no full copyrighted page mirrored",
         "intake_role": "source registration only; evidence requires question-specific parse and review"}
        for s in sources], "document_id")
    source_by_id = {s["source_id"]: s for s in sources}
    claims = read_lines(PROJECT / "ledger/claims.jsonl")
    times = []
    for c in claims:
        source = source_by_id[c["source_id"]]
        # Immutable claims keep their content; time envelopes are separate audit additions.
        published = source["published_at"]
        if c["source_id"] == "S01" and c["question_node_id"] == "Q1.1.2.2":
            published = "2026-08-21"
        times.append({"claim_id": c["claim_id"], "published_at": published,
                      "effective_period": source["effective_period"], "target_period": source.get("target_period", ""),
                      "ingested_at": c["ingested_at"], "publication_date_status": source["publication_date_status"],
                      "as_of_date": "2026-09-10", "visibility_proof": source["publication_date_source"]})
    append_unique(PROJECT / "ledger/claim_temporal_envelopes.jsonl", times, "claim_id")
    repo = FileSystemResearchPlanRepository(PROJECT)
    validation = ValidateResearchPlanExecution(repo).execute()
    write_json(PROJECT / "plan_validation.json", validation)
    if not validation["ok"]:
        raise ValueError(validation["issues"])
    project = json.loads((PROJECT / "project.json").read_text())
    project.update(research_status="partial_research", current_judgment=synthesis["root_conclusion"],
                   biggest_uncertainty="Astra 带来的新增企业付费与净算力采购尚不可归因。")
    write_json(PROJECT / "project.json", project)
    qa = json.loads((PROJECT / "qa_tree.json").read_text())
    rows = {r["id"]: r for r in [*chapters, *synthesis["nodes"]]}
    states = []
    def inherited_gaps(node_id):
        own = list(rows.get(node_id, {}).get("gaps", []))
        for child in [n for n in qa["nodes"] if n.get("parent_id") == node_id]:
            own.extend(inherited_gaps(child["id"]))
        return list(dict.fromkeys(own))
    for node in qa["nodes"]:
        row = rows.get(node["id"], {})
        conclusion = row.get("conclusion", synthesis["root_conclusion"])
        passed = row.get("passed", False)
        states.append({"state_id": f"state_{node['id']}_20260910_v2", "question_id": node["id"],
                       "as_of_date": "2026-09-10", "conclusion": conclusion, "passed": passed,
                       "status": ("answered" if passed else ("expanded" if node.get("next_question_ids") else "blocked")),
                       "children": node.get("next_question_ids", []), "gaps": inherited_gaps(node["id"]),
                       "state_basis": "leaf evidence and answerability gate" if node["id"] in {r["id"] for r in chapters} else "child conclusion synthesis",
                       "revision_type": "audit_correction", "prior_state_id": f"state_{node['id']}_20260910_v1",
                       "revision_reason": "显式继承子节点缺口，纠正已充分父节点的状态标签；无新增研究证据或时间变化。"})
    append_unique(PROJECT / "ledger/node_states.jsonl", states, "state_id")
    gates = [{**t, "candidate_action_state": "watch_only", "action_state": "no_action",
              "research_gate": {"passed": False, "reasons": ["未验证 canonical BOM 稀缺映射", "事件增量盈利未验证", "未做 as-of 估值与错定价分析"]}}
             for t in synthesis["targets"]]
    write_json(PROJECT / "target_gates.json", gates)
    # The view model contains already-researched content only; renderers do no research.
    vm = ReportViewModel(project={**project, "synthesis": synthesis}, goal={"topic": project["meta_question"]},
                         supply_chain={"scope": "event_transmission_not_full_bom", "chain": synthesis["causal_chain"]},
                         qa_roots=chapters, targets=gates, sources=sources)
    from gpt6_question_tree_view import build_question_tree_view
    tree = build_question_tree_view(vm, qa, {s["question_id"]: s for s in states},
        json.loads((PROJECT / "research_brief.json").read_text()), read_lines(PROJECT / "source_extractions.jsonl"))
    vm.project.update(presentation_profile="question-tree-v1", question_tree=tree)
    write_json(PROJECT / "question_tree_report.json", tree)
    write_json(PROJECT / "report_view_model.json", vm.to_dict())
    render_plan(qa, project)
    from render_gpt6_impact_report import EventHtmlReportRenderer, EventMarkdownReportRenderer
    EventHtmlReportRenderer().write(PROJECT, vm)
    EventMarkdownReportRenderer().write(PROJECT, vm)
    from value_invest_research.framework_contracts import validate_report_contract_html, validate_report_contract_markdown
    write_json(PROJECT / "presentation_validation.json", {
        "markdown_contract": validate_report_contract_markdown((PROJECT / "professional_report.md").read_text()),
        "existing_html_contract": validate_report_contract_html((PROJECT / "professional_report.html").read_text()),
        "html_compatibility_note": "使用 question-tree-v1 共享模板与对应严格结构校验；不适用全 BOM 报告样式门禁。",
        "event_static_tests": "tools/test_gpt6_impact_research.py: trace, dates, calculations, identical claims, headings, local links, no runtime fetch",
        "visual_review": "blocked_by_local_file_browser_policy; not claimed"
    })
    write_json(PROJECT / "research_run.json", {"status": "partial_research", "as_of_date": "2026-09-10",
        "summary": validation["summary"]["nested"], "scope": "event-study; not a full BOM investment run",
        "visual_review": "not_completed: local file navigation blocked by browser security policy",
        "external_archive_scan": "not_performed", "market_price_analysis": "not_performed",
        "unanswered_leaf_ids": [r["id"] for r in chapters if not r["passed"]],
        "source_count": len(sources), "claim_count": len(claims),
        "reproduce": "PYTHONPATH=src <Python 3.10+> tools/gpt6_impact_research.py"})
    print(json.dumps(validation["summary"], ensure_ascii=False))


def render_plan(qa, project):
    brief = json.loads((PROJECT / "research_brief.json").read_text())
    original = {q["id"]: q for q in brief["questions"]}
    lines = ["# GPT-6 Astra 发布影响｜动态研究计划", "", "> 截面 2026-09-10。初始止于 L3；现有 L4 均来自实际证据缺口。最多 L5。", ""]
    def visit(node):
        level = node["level"]
        indent = "  " * (level - 1)
        lines.extend([f"{indent}- L{level} · {node['id']}：{node.get('display_question') or node['question']}", ""])
        children = [n for n in qa["nodes"] if n.get("parent_id") == node["id"]]
        if not children:
            orig = original.get(node["id"], {})
            data = orig.get("data") or node.get("required_data") or node.get("required_materials") or []
            analysis = orig.get("analysis") or node.get("analysis_plan") or []
            if isinstance(analysis, str):
                analysis = [analysis]
            lines.extend([f"{indent}  - 数据：{'；'.join(data)}", "", f"{indent}  - 分析：{'；'.join(analysis)}", ""])
        for child in children:
            visit(child)
    for root in [n for n in qa["nodes"] if n["level"] == 1]:
        visit(root)
    (PROJECT / "research_plan.md").write_text("\n".join(lines), encoding="utf-8")


def render_existing():
    """Refresh presentation only; never append or alter research evidence/events."""
    if json.loads((PROJECT / "project.json").read_text()).get("framework_revision") == "20260922_object_industry_company_execution":
        from research_gpt6_new_framework import finish
        return finish()
    from gpt6_question_tree_view import build_question_tree_view
    from render_gpt6_impact_report import EventHtmlReportRenderer
    from value_invest_research.framework_contracts import validate_report_contract_html
    vm = ReportViewModel(**json.loads((PROJECT / "report_view_model.json").read_text()))
    tree = build_question_tree_view(vm, json.loads((PROJECT / "qa_tree.json").read_text()),
        {s["question_id"]: s for s in read_lines(PROJECT / "ledger/node_states.jsonl")},
        json.loads((PROJECT / "research_brief.json").read_text()), read_lines(PROJECT / "source_extractions.jsonl"))
    vm.project.update(presentation_profile="question-tree-v1", question_tree=tree)
    renderer = EventHtmlReportRenderer()
    validation = validate_report_contract_html(renderer.render(vm))
    if not validation["ok"]:
        raise ValueError(validation["issues"])
    write_json(PROJECT / "question_tree_report.json", tree)
    write_json(PROJECT / "report_view_model.json", vm.to_dict())
    renderer.write(PROJECT, vm)
    previous = json.loads((PROJECT / "presentation_validation.json").read_text())
    previous.update(existing_html_contract=validation, presentation_profile="question-tree-v1",
                    html_compatibility_note="采用共享 question-tree-v1 模板；非叶子与叶子分别按各自三模块校验，不套用全 BOM 报告样式门禁。")
    write_json(PROJECT / "presentation_validation.json", previous)
    print(json.dumps(validation, ensure_ascii=False))


def initialize():
    brief = json.loads((PROJECT / "research_brief.json").read_text())
    if (PROJECT / "research_plan.json").exists():
        return
    goal = ResearchGoal(topic=brief["meta_question"], research_type="event", object_id=brief["project_id"],
                        as_of_date=brief["as_of_date"], report_date=brief["report_date"],
                        decision_boundary=brief["decision_boundary"], domain_hint=brief["domain_playbook"])
    templates = [QuestionTemplate(id=g["id"], question=g["question"], why_this_depth="回答元问题的必要机制",
                 l3_questions=[q for q in brief["questions"] if q["parent_id"] == g["id"]]) for g in brief["groups"]]
    playbook = DomainPlaybook(playbook_id=brief["domain_playbook"], research_type="event_policy",
                             q_map={"Q1": brief["meta_question"]}, mechanism_buckets=[g["question"] for g in brief["groups"]],
                             l2_templates={"Q1": templates}, quality_rule="逐题搜集、分析、复核、充分性；不预生成 L4/L5；事件影响不等于因果归因。")
    nodes = [QuestionNode(id="Q1", level=1, question=brief["meta_question"], next_question_ids=[g["id"] for g in brief["groups"]])]
    for g in brief["groups"]:
        nodes.append(QuestionNode(id=g["id"], level=2, question=g["question"], parent_id="Q1",
                                  next_question_ids=[q["id"] for q in brief["questions"] if q["parent_id"] == g["id"]]))
    for q in brief["questions"]:
        nodes.append(QuestionNode(id=q["id"], level=3, question=q["question"], parent_id=q["parent_id"],
                    required_materials=q["data"], decision_use=q["analysis"], support_evidence="直接回答问题的可复核事实与有边界的推导",
                    refute_evidence=q["refute"], preferred_specialty_skill="dynamic-research-agent"))
    architecture = QuestionArchitecture(goal, playbook, "单一 L1 元问题，三类机制、六个初始终端 L3；只按实际缺口展开。", nodes)
    universe = FileSystemSourceUniverseRepository(ROOT / "config/source_universes.json").resolve_for_research({"domain_playbook": "ai_factory"})
    universe["event_supplement"] = ["OpenAI official release/docs", "benchmark authors", "competitor official docs", "customer/company IR", "primary adoption studies"]
    plan = build_research_plan(architecture, source_universe=universe).to_dict()
    index, children = build_l3_research_plan_set(l3_nodes=[n.to_dict() for n in nodes if n.level == 3],
                      parent_plan_id=plan["plan_id"], research_goal=goal.to_dict(), source_universe=universe)
    repo = FileSystemResearchPlanRepository(PROJECT)
    repo.save_question_architecture(enrich_question_architecture(architecture, build_research_plan(architecture, source_universe=universe)))
    repo.save_plan(plan)
    repo.save_l3_research_plans(index, children)
    repo.bind_l3_plans_to_question_architecture(parent_plan=plan, index=index)
    (PROJECT / "project.json").write_text(json.dumps({**brief, "research_status": "in_progress", "report_scope": "event-study", "source_universe": universe}, ensure_ascii=False, indent=2) + "\n")
    print(f"Initialized {len(children)} L3 plans under {PROJECT}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--render-only", action="store_true")
    if parser.parse_args().render_only:
        render_existing()
    elif (PROJECT / "research_revisions/20260911_first_principles/completed.json").exists():
        # A historical bootstrap must not overwrite a later, reviewed revision.
        from refine_gpt6_report import refresh_report
        refresh_report()
    else:
        initialize()
        if (PROJECT / "initial_findings.json").exists():
            expand_initial()
        if (PROJECT / "report_synthesis.json").exists():
            finish()
