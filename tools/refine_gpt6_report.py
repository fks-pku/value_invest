"""Apply the authored first-principles revision without rewriting prior evidence.

Research prose lives in first_principles_revision.json. This migration preserves
prior reports/plans, records the changed question separately, and reuses the
canonical HTML template. It does not search or invent research findings.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

from gpt6_impact_research import PROJECT, append_unique, read_lines, record_question, render_plan, write_json
from gpt6_question_tree_view import build_question_tree_view
from render_gpt6_impact_report import EventHtmlReportRenderer, EventMarkdownReportRenderer
from value_invest_research.adapters.outbound.filesystem_research_plan import FileSystemResearchPlanRepository
from value_invest_research.application.use_cases.research_plan_execution import ValidateResearchPlanExecution
from value_invest_research.domain.l3_research_plan import build_l3_research_plan
from value_invest_research.domain.report_view_model import ReportViewModel
from value_invest_research.framework_contracts import validate_report_contract_html, validate_report_contract_markdown

REVISION = PROJECT / "first_principles_revision.json"


def read(name):
    return json.loads((PROJECT / name).read_text(encoding="utf-8"))


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def archive_before(folder):
    if (folder / "before_manifest.json").exists():
        return
    before = folder / "before"
    before.mkdir(parents=True, exist_ok=True)
    for path in PROJECT.iterdir():
        if path.is_file() and path.suffix in {".json", ".jsonl", ".md", ".html"}:
            shutil.copy2(path, before / path.name)
    shutil.copy2(PROJECT / "l3_research_plans/index.json", before / "l3_plan_index.json")
    files = [*PROJECT.glob("*.jsonl"), *PROJECT.glob("ledger/*.jsonl"),
             *PROJECT.glob("inbox/*.jsonl"), *PROJECT.glob("l3_research_plans/*/research_step_events.jsonl")]
    write_json(folder / "before_manifest.json", {str(p.relative_to(PROJECT)): {
        "bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in files})


def refresh_report():
    project, qa, chapters, syn = (read(n) for n in ("project.json", "qa_tree.json", "research_chapters.json", "report_synthesis.json"))
    states = {s["question_id"]: s for s in read_lines(PROJECT / "ledger/node_states.jsonl")}
    vm = ReportViewModel(project={**project, "synthesis": syn}, goal={"topic": project["meta_question"]},
                         supply_chain={"scope": "event_transmission_not_full_bom", "chain": syn["causal_chain"]},
                         qa_roots=chapters, targets=read("target_gates.json"), sources=read_lines(PROJECT / "sources.jsonl"))
    tree = build_question_tree_view(vm, qa, states, read("research_brief.json"), read_lines(PROJECT / "source_extractions.jsonl"))
    vm.project.update(presentation_profile="question-tree-v1", question_tree=tree)
    html, md = EventHtmlReportRenderer().render(vm), EventMarkdownReportRenderer().render(vm)
    validation = {"existing_html_contract": validate_report_contract_html(html),
                  "markdown_contract": validate_report_contract_markdown(md),
                  "presentation_profile": "question-tree-v1",
                  "visual_review": "not_performed_this_revision; existing local-file browser policy restriction",
                  "html_compatibility_note": "共享四节问题树模板；结构通过不等于研究完成。"}
    for surface in ("existing_html_contract", "markdown_contract"):
        if not validation[surface]["ok"]:
            raise ValueError(validation[surface]["issues"])
    write_json(PROJECT / "question_tree_report.json", tree)
    write_json(PROJECT / "report_view_model.json", vm.to_dict())
    EventHtmlReportRenderer().write(PROJECT, vm)
    EventMarkdownReportRenderer().write(PROJECT, vm)
    render_plan(qa, project)
    write_json(PROJECT / "presentation_validation.json", validation)
    print(json.dumps(validation["existing_html_contract"], ensure_ascii=False))


def apply_revision():
    revision = read(REVISION.name)
    rid = revision["revision_id"]
    folder = PROJECT / "research_revisions" / rid
    completion = folder / "completed.json"
    if completion.exists():
        if json.loads(completion.read_text())["input_sha256"] != digest(revision):
            raise ValueError("This revision is immutable; create a new revision before changing its input")
        refresh_report()
        return
    archive_before(folder)
    # Always derive a retry from the preserved input, not from partially updated files.
    baseline = lambda name: json.loads((folder / "before" / name).read_text())
    project, brief, qa, parent, index = (baseline(n) for n in (
        "project.json", "research_brief.json", "qa_tree.json", "research_plan.json", "l3_plan_index.json"))
    prior_states = {s["question_id"]: s for s in read_lines(PROJECT / "ledger/node_states.jsonl") if s.get("revision_id") != rid}
    now = datetime.now(timezone.utc).isoformat()
    renamed = revision["display_questions"]
    scope = revision["scope_change"]
    nodes = {n["id"]: n for n in qa["nodes"]}
    nodes["Q1"].update(question=revision["root_question"], next_question_ids=[g["id"] for g in revision["groups"]])
    for group in revision["groups"]:
        nodes[group["id"]] = {**nodes.get(group["id"], {}), "id": group["id"], "level": 2,
                               "parent_id": "Q1", "question": group["question"], "next_question_ids": group["children"]}
        for child in group["children"]:
            nodes[child]["parent_id"] = group["id"]
    for nid, question in renamed.items():
        nodes[nid]["display_question"] = question
    nodes[scope["question_id"]].update(question=scope["question"], required_data=scope["data"],
        required_materials=scope["data"], analysis_plan=[scope["analysis"]], decision_use=scope["analysis"],
        support_evidence="同口径净增收入与成本证明事件增量利润", refute_evidence=scope["refute"])
    # Existing IDs and actual gap-created descendants survive the regrouping.
    ordered = []
    def visit(nid):
        ordered.append(nodes[nid])
        for child in nodes[nid].get("next_question_ids", []):
            visit(child)
    visit("Q1")
    qa["nodes"] = ordered
    qa["revision_id"] = rid
    qa["planner_rationale"] = "四个第一性原理主问题；保留已实际取证的终端问题与缺口触发的 L4，不预生成新分支。"
    brief.update(meta_question=revision["root_question"], groups=[{"id": g["id"], "question": g["question"]} for g in revision["groups"]],
                 revised_on=revision["revised_on"], question_design_revision=rid)
    for q in brief["questions"]:
        q.update(parent_id=nodes[q["id"]]["parent_id"], display_question=renamed[q["id"]])
        if q["id"] == scope["question_id"]:
            q.update(question=scope["question"], data=scope["data"], analysis=scope["analysis"], refute=scope["refute"])
    parent["previous_plan_id"] = parent["plan_id"]
    parent["revision_id"] = rid
    parent["research_goal"]["topic"] = revision["root_question"]
    parent["question_architecture"]["planner_rationale"] = qa["planner_rationale"]
    parent["display_questions"] = renamed
    parent["mechanism_groups"] = revision["groups"]
    parent["unchanged_child_plan_policy"] = "Existing child plans retain their immutable creation-parent provenance; active membership is specified by this parent and index. Only Q1.3.1 changes research scope."
    for step in parent["steps"]:
        if step["question_node_id"] == scope["question_id"]:
            step.update(question=scope["question"], decision_use=scope["analysis"], required_materials=scope["data"], refuting_source_plan=[scope["refute"]])
    parent["plan_id"] = "rp_fp_" + digest({k: v for k, v in parent.items() if k != "plan_id"})[:16]
    repo = FileSystemResearchPlanRepository(PROJECT)
    changed_plan = build_l3_research_plan(node=nodes[scope["question_id"]], parent_plan_id=parent["plan_id"],
        research_goal=parent["research_goal"], source_universe=project["source_universe"])
    changed_plan.update(previous_plan_id=next(p["l3_plan_id"] for p in index["plans"] if p["l3_node_id"] == scope["question_id"]),
                        revision_reason="从投资观察边界改为事件利润兑现；旧通过状态不继承。")
    index["parent_research_plan_id"] = parent["plan_id"]
    for row in index["plans"]:
        if row["l3_node_id"] == scope["question_id"]:
            row["l3_plan_id"] = changed_plan["plan_id"]
    repo.save_plan(parent)
    repo.save_l3_research_plans(index, [changed_plan])
    qa["research_plan_id"] = parent["plan_id"]
    qa["research_goal"] = deepcopy(parent["research_goal"])
    nodes[scope["question_id"]].update(research_step_id=changed_plan["steps"][0]["step_id"],
        source_plan=changed_plan["steps"][0]["source_plan"], minimum_evidence_gate=changed_plan["steps"][0]["minimum_evidence_gate"])
    repo.save_question_architecture(qa)
    write_json(PROJECT / "research_brief.json", brief)
    append_unique(PROJECT / "research_events.jsonl", [{"event_id": rid + "_scope", "event_type": "scope_changed",
        "recorded_at": now, "as_of_date": revision["as_of_date"], "previous_plan_id": parent["previous_plan_id"],
        "research_plan_id": parent["plan_id"], "reason": revision["reason"], "reuse_policy": revision["reuse_policy"],
        "question_changes": scope, "display_questions": renamed}], "event_id")

    source = {**revision["new_source"], "ingestion_channel": "question_search", "retrieved_on": revision["revised_on"]}
    sources = baseline("source_catalog.json") + [source]
    write_json(PROJECT / "source_catalog.json", sources)
    append_unique(PROJECT / "sources.jsonl", [source], "source_id")
    append_unique(PROJECT / "material_intake/documents.jsonl", [{**source, "document_id": "document_S14",
        "original_local_path": "", "storage_note": "web original; limited question-specific extraction only",
        "question_node_id": "Q1.1.2.2", "intake_role": "selected_for_task_cost_refutation"}], "document_id")
    chapters = baseline("research_chapters.json")
    for i, row in enumerate(chapters):
        row["display_question"] = renamed[row["id"]]
        if row["id"] == scope["question_id"]:
            chapters[i] = deepcopy(revision["profit_chapter"])
            continue
        addition = revision["leaf_additions"].get(row["id"])
        if addition:
            row["analysis"].insert(0, deepcopy(addition))
        if row["id"] == "Q1.2.2.1":
            for section in row["analysis"]:
                section["paragraphs"] = [p.replace("C 应包含内部推理、重试、工具关联推理和必要安全监控", "C 应包含单次尝试的内部推理、工具关联推理和必要安全监控；已计入 N 的重试不再计入 C") for p in section["paragraphs"]]
        if row["id"] == "Q1.1.2.2":
            row["evidence"].append(deepcopy(revision["cost_evidence"]))
            row["analysis"].append(deepcopy(revision["cost_addition"]))
            row["refutation"] += "；新增 S14 同等四舍五入评分但账单更高的特定代码升级反例，不外推为全部任务。"
    write_json(PROJECT / "research_chapters.json", chapters)
    # Only these questions receive new source attachments. Historical unchanged
    # pairs remain linked to their original extraction/review, not re-labelled.
    cost = deepcopy(next(c for c in chapters if c["id"] == "Q1.1.2.2"))
    cost["evidence"] = [revision["cost_evidence"]]
    cost["searches"] = ["GPT-6 Astra SPFx 98% 2.49 1.03 cost September 9 2026; developer.microsoft.com",
                        "针对 Q1.1.2.2 单独核读 Microsoft Developer 9 月 9 日正文的匹配测试、运行次数及 GitHub Copilot 计价边界。"]
    for chapter in (cost, next(c for c in chapters if c["id"] == scope["question_id"])):
        record_question(chapter, "first_principles_leaf", performed_on=revision["revised_on"])
    by_source = {s["source_id"]: s for s in sources}
    envelopes = []
    for claim in read_lines(PROJECT / "ledger/claims.jsonl"):
        if "_first_principles_leaf_" not in claim["claim_id"]:
            continue
        src = by_source[claim["source_id"]]
        envelopes.append({"claim_id": claim["claim_id"], "published_at": src["published_at"],
            "effective_period": src["effective_period"], "target_period": src.get("target_period", ""),
            "ingested_at": claim["ingested_at"], "publication_date_status": src["publication_date_status"],
            "as_of_date": revision["as_of_date"], "visibility_proof": src["publication_date_source"]})
    append_unique(PROJECT / "ledger/claim_temporal_envelopes.jsonl", envelopes, "claim_id")
    syn = baseline("report_synthesis.json")
    syn.update(root_conclusion=revision["root_conclusion"], root_paragraphs=revision["root_paragraphs"], nodes=revision["rollups"],
        headline="先看真实需求，再看算力与利润", deck="第一性原理问题树 · 原截面修订",
        causal_chain=[["实际能力与任务全成本", "局部改善、有适用边界"], ["客户净增付费", "未验证"],
                      ["净算力与设备采购", "未归因"], ["公司增量利润", "未验证"]])
    syn["boundary"] += " 本次按新问题设计规则修订，修订日为 2026-09-11，事实截止日不变；不构成新市场截面。"
    write_json(PROJECT / "report_synthesis.json", syn)
    rows = {r["id"]: r for r in chapters + syn["nodes"]}
    states = []
    def state(nid):
        child_states = [state(c) for c in nodes[nid].get("next_question_ids", [])]
        row = rows.get(nid, {})
        gaps = list(dict.fromkeys(list(row.get("gaps", [])) + [g for c in child_states for g in c["gaps"]]))
        passed = bool(row.get("passed", False)) and all(c["passed"] for c in child_states)
        value = {"state_id": f"state_{nid}_{rid}", "question_id": nid, "as_of_date": revision["as_of_date"],
            "recorded_at": now, "revision_id": rid, "conclusion": row.get("conclusion", syn["root_conclusion"]),
            "passed": passed, "status": "answered" if passed else ("expanded" if child_states else "blocked"),
            "children": nodes[nid].get("next_question_ids", []), "gaps": gaps,
            "prior_state_id": prior_states.get(nid, {}).get("state_id", ""),
            "revision_type": "question_design_and_evidence_review", "revision_reason": revision["reuse_policy"],
            "state_basis": "direct child synthesis" if child_states else "question-specific evidence and renewed sufficiency assessment"}
        states.append(value)
        return value
    state("Q1")
    append_unique(PROJECT / "ledger/node_states.jsonl", states, "state_id")
    append_unique(PROJECT / "research_events.jsonl", [{"event_id": rid + "_analysis", "event_type": "analysis_revised",
        "recorded_at": now, "revision_id": rid, "as_of_date": revision["as_of_date"],
        "analysis_artifact": "first_principles_revision.json", "input_sha256": digest(revision),
        "new_evidence_questions": ["Q1.1.2.2", "Q1.3.1"],
        "unchanged_evidence_questions": [c["id"] for c in chapters if c["id"] not in {"Q1.1.2.2", "Q1.3.1"}],
        "calculation_correction": "C excludes retry attempts already counted in N; scenario values unchanged"}], "event_id")
    project.update(meta_question=revision["root_question"], current_judgment=syn["root_conclusion"],
        groups=brief["groups"], questions=brief["questions"], research_status="partial_research", revised_on=revision["revised_on"],
        source_note=revision["source_note"], research_revision_id=rid,
        biggest_uncertainty="客户净付费、事件采购和公司增量利润尚未形成同口径闭环。")
    write_json(PROJECT / "project.json", project)
    validation = ValidateResearchPlanExecution(repo).execute()
    if not validation["ok"]:
        raise ValueError(validation["issues"])
    write_json(PROJECT / "plan_validation.json", validation)
    run = baseline("research_run.json")
    run.update(revision_id=rid, revised_on=revision["revised_on"], summary=validation["summary"]["nested"],
        unanswered_leaf_ids=[c["id"] for c in chapters if not c["passed"]], source_count=len(sources),
        claim_count=len(read_lines(PROJECT / "ledger/claims.jsonl")),
        reproduce="PYTHONPATH=src <Python 3.10+> tools/refine_gpt6_report.py",
        revision_note="Same historical cutoff; new cost refutation and independently reviewed profit question; no new L4/L5.")
    write_json(PROJECT / "research_run.json", run)
    refresh_report()
    for name, entry in json.loads((folder / "before_manifest.json").read_text()).items():
        if hashlib.sha256((PROJECT / name).read_bytes()[:entry["bytes"]]).hexdigest() != entry["sha256"]:
            raise ValueError(f"Append-only history was changed: {name}")
    write_json(completion, {"revision_id": rid, "recorded_at": now, "input_sha256": digest(revision),
        "append_only_prefixes_verified": True, "plan_validation": validation["summary"]["nested"]})


if __name__ == "__main__":
    apply_revision()
