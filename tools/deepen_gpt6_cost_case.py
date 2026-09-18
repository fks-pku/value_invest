"""Apply one authored cost-case revision; calculation is separate from rendering.

No model benchmark is run here. Published matched examples remain observations;
labor and routing inputs remain explicitly hypothetical sensitivity parameters.
"""
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json

from gpt6_impact_research import PROJECT, append_unique, read_lines, record_question, write_json
from refine_gpt6_report import archive_before, digest, refresh_report
from value_invest_research.adapters.outbound.filesystem_research_plan import FileSystemResearchPlanRepository
from value_invest_research.adapters.outbound.filesystem_source_universe import FileSystemSourceUniverseRepository
from value_invest_research.application.use_cases.research_plan_execution import RecordResearchStepEvent, ValidateResearchPlanExecution

FOLDER = PROJECT / "research_revisions/20260918_cost_case"
INPUT = FOLDER / "cost_case_revision.json"


def calculate(revision):
    d = lambda value: Decimal(str(value))
    sample = revision["samples"][0]
    low, high = d(sample["sonnet_usd"]), d(sample["astra_usd"])
    premium = high - low
    assumptions = revision["assumptions"]
    return {
        "data_nature": "published matched example plus hypothetical sensitivity; not own benchmark or production forecast",
        "source_id": "S14", "premium_usd": float(premium), "price_multiple": float(high / low),
        "breakeven_minutes": {str(w): float(premium * 60 / d(w)) for w in assumptions["labor_usd_per_hour"]},
        "sensitivity": [{"saved_minutes": m, "labor_usd_per_hour": w,
                         "net_saving_usd": float(d(w) * d(m) / 60 - premium)}
                        for m in assumptions["saved_human_minutes"] for w in assumptions["labor_usd_per_hour"]],
        "routing_threshold": float((high - low) / high),
        "routing": [{"escalation_rate": q, "bill_usd": float(low + d(q) * high),
                     "saving_vs_all_astra_usd": float(high - low - d(q) * high)}
                    for q in assumptions["route_escalation_rates"]],
        "assumptions": assumptions,
        "unmeasured": ["human_minutes", "acceptance_rate", "error_loss", "implementation_cost", "conditional_escalation_cost"],
    }


def materialize_tables(revision, calc):
    analysis = deepcopy(revision["analysis"])
    for section in analysis:
        for i, table in enumerate(section.get("tables", [])):
            if table["kind"] == "observations":
                section["tables"][i] = {
                    "caption": "原文匹配样例 [S14]；美元/次，评分为四舍五入值，非五次均值或验收率。最后两列为研究者计算。",
                    "headers": ["任务 / 配置", "Sonnet 4.6：分数 / 账单", "Astra：分数 / 账单", "Astra 多付", "费用倍数"],
                    "rows": [[s["task"], f'{s["sonnet_score"]}% / ${s["sonnet_usd"]:.2f}',
                              f'{s["astra_score"]}% / ${s["astra_usd"]:.2f}',
                              f'${s["astra_usd"] - s["sonnet_usd"]:.2f}',
                              f'{s["astra_usd"] / s["sonnet_usd"]:.2f}×'] for s in revision["samples"]],
                }
            elif table["kind"] == "sensitivity":
                section["tables"][i] = {
                    "caption": "条件测算：每任务净节省（美元）；正数有利于 Astra。价差来自 S14，人工与其它成本条件均为假设，非实际 ROI。",
                    "headers": ["净省人工分钟"] + [f'人工 ${w}/小时' for w in revision["assumptions"]["labor_usd_per_hour"]],
                    "rows": [[str(m)] + [f'{r["net_saving_usd"]:+.2f}' for r in calc["sensitivity"] if r["saved_minutes"] == m]
                             for m in revision["assumptions"]["saved_human_minutes"]],
                }
            else:
                raise ValueError(f"Unknown authored table kind: {table['kind']}")
    return analysis


def verify_prefixes():
    for name, row in json.loads((FOLDER / "before_manifest.json").read_text()).items():
        if hashlib.sha256((PROJECT / name).read_bytes()[:row["bytes"]]).hexdigest() != row["sha256"]:
            raise ValueError(f"Append-only history changed: {name}")


def apply_revision():
    revision = json.loads(INPUT.read_text())
    complete = FOLDER / "completed.json"
    if complete.exists():
        if json.loads(complete.read_text())["input_sha256"] != digest(revision):
            raise ValueError("Applied revision inputs are immutable; create another revision")
        verify_prefixes()
        refresh_report()
        return
    archive_before(FOLDER)
    baseline = lambda name: json.loads((FOLDER / "before" / name).read_text())
    now = datetime.now(timezone.utc).isoformat()
    rid, qid = revision["revision_id"], revision["question_id"]
    project, chapters, synthesis = (baseline(n) for n in ("project.json", "research_chapters.json", "report_synthesis.json"))
    assert project["as_of_date"] == revision["as_of_date"] == "2026-09-10"
    calc = calculate(revision)
    write_json(FOLDER / "calculations.json", calc)
    universe = FileSystemSourceUniverseRepository(PROJECT.parents[2] / "config/source_universes.json")
    write_json(FOLDER / "source_selection.json", {
        "question_node_id": qid,
        "registry_universe": universe.resolve_for_research({"domain_playbook": "ai_factory"}),
        "selection_reason": "沿用注册表；窄任务采用开发者原始实验、评测作者和 METR 人工时间研究，不将硬件新闻当任务 ROI 证据。",
        "selected_source_ids": [e["source"] for e in revision["new_evidence"]],
        "cutoff": revision["as_of_date"], "actual_read_date": revision["revised_on"],
        "access_failures": ["S14 links: not-all-model-upgrades-are-upgrades / what-ai-benchmarks-are-not-telling-you / building-ax-evals-that-actually-work returned 403"],
        "raw_trial_data": "not_obtained; no mean, variance or significance claim",
    })
    new_sources = [{**s, "ingestion_channel": "question_search", "retrieved_on": revision["revised_on"]}
                   for s in revision["new_sources"]]
    append_unique(PROJECT / "sources.jsonl", new_sources, "source_id")
    append_unique(PROJECT / "material_intake/documents.jsonl", [{
        "document_id": "document_" + s["source_id"], **s,
        "intake_role": "selected for Q1.1.2.2 only; evidence requires separate extraction and review",
        "original_local_path": "", "storage_note": "web original; no copyrighted full-page mirror",
    } for s in new_sources], "document_id")
    catalog = baseline("source_catalog.json")
    catalog.extend(s for s in new_sources if s["source_id"] not in {c["source_id"] for c in catalog})
    write_json(PROJECT / "source_catalog.json", catalog)
    cost = next(c for c in chapters if c["id"] == qid)
    by_source = {e["source"]: e for e in revision["new_evidence"]}
    cost["evidence"] = [deepcopy(by_source.get(e["source"], e)) for e in cost["evidence"]]
    cost["evidence"].extend(deepcopy(e) for e in revision["new_evidence"] if e["source"] not in {p["source"] for p in cost["evidence"]})
    for key in ("conclusion", "gate_reason", "refutation", "next_actions", "searches"):
        cost[key] = deepcopy(revision[key])
    cost.update(analysis=materialize_tables(revision, calc), verification_scope="conditional_economics_not_realized_roi",
                support=["SPFx 匹配账单差额已核对", "人工门槛与路由条件由明确公式计算；未知量未填成实测"],
                pending_measurements=calc["unmeasured"])
    write_json(PROJECT / "research_chapters.json", chapters)
    child_repo = FileSystemResearchPlanRepository(PROJECT / "l3_research_plans" / revision["l3_id"])
    RecordResearchStepEvent(child_repo).execute({"event_id": rid + "_reopened", "event_type": "step_reopened",
        "step_id": "question:" + qid, "gaps": [], "next_actions": ["用户要求深化本叶子的案例测算；不改变问题范围或继承实际 ROI 已完成状态"]})
    selected = deepcopy(cost)
    selected["evidence"] = revision["new_evidence"]
    record_question(selected, "cost_case_leaf", performed_on=revision["revised_on"])
    sources = {s["source_id"]: s for s in read_lines(PROJECT / "sources.jsonl")}
    envelopes = []
    for claim in read_lines(PROJECT / "ledger/claims.jsonl"):
        if "_cost_case_leaf_" not in claim["claim_id"]:
            continue
        source = sources[claim["source_id"]]
        envelopes.append({"claim_id": claim["claim_id"], "published_at": source["published_at"],
            "effective_period": source["effective_period"], "target_period": "", "ingested_at": claim["ingested_at"],
            "publication_date_status": source["publication_date_status"], "as_of_date": revision["as_of_date"],
            "visibility_proof": source["publication_date_source"],
            "version_caveat": "Dated original reread 2026-09-18; no immutable September 10 webpage snapshot asserted"})
    append_unique(PROJECT / "ledger/claim_temporal_envelopes.jsonl", envelopes, "claim_id")
    for row in synthesis["nodes"]:
        if row["id"] in revision["parent_updates"]:
            row.update(deepcopy(revision["parent_updates"][row["id"]]))
    synthesis["root_paragraphs"].append(revision["root_addition"])
    synthesis["boundary"] += " 9 月 18 日仅深化任务成本叶子及必要上层汇总，仍使用原截止日前资料。"
    write_json(PROJECT / "report_synthesis.json", synthesis)
    # archive_before keeps nested ledgers by prefix hash, so take pre-revision states from the current append-only ledger.
    prior = {s["question_id"]: s for s in read_lines(PROJECT / "ledger/node_states.jsonl") if s.get("revision_id") != rid}
    rows = {c["id"]: c for c in [cost, *synthesis["nodes"]]}
    states = []
    for nid in (qid, "Q1.1.2", "Q1.1", "Q1"):
        value = deepcopy(prior[nid])
        value.update(state_id=f"state_{nid}_{rid}", prior_state_id=prior[nid]["state_id"], recorded_at=now,
            revision_id=rid, revision_type="single_leaf_empirical_case", revision_reason=revision["scope"],
            conclusion=rows[nid]["conclusion"] if nid in rows else synthesis["root_conclusion"])
        states.append(value)
    append_unique(PROJECT / "ledger/node_states.jsonl", states, "state_id")
    append_unique(PROJECT / "research_events.jsonl", [{"event_id": rid + "_analysis", "event_type": "analysis_revised",
        "recorded_at": now, "as_of_date": revision["as_of_date"], "revision_id": rid,
        "analysis_artifact": str(INPUT.relative_to(PROJECT)), "input_sha256": digest(revision),
        "new_evidence_questions": [qid], "rollup_questions": ["Q1.1.2", "Q1.1", "Q1"],
        "calculation_artifact": str((FOLDER / "calculations.json").relative_to(PROJECT)),
        "no_new_benchmark": True, "no_new_tree_nodes": True}], "event_id")
    project.update(revised_on=revision["revised_on"], research_revision_id=rid)
    project["source_note"] += " 9 月 18 日仅对 Q1.1.2.2 重读 S05/S14，另增 S15/S16 的人工时间边界证据。新增表格是公开匹配样例和条件测算，不是新跑测或实际 ROI；未取得完整逐次测试数据，也未重搜其它叶子。"
    write_json(PROJECT / "project.json", project)
    validation = ValidateResearchPlanExecution(FileSystemResearchPlanRepository(PROJECT)).execute()
    if not validation["ok"]:
        raise ValueError(validation["issues"])
    write_json(PROJECT / "plan_validation.json", validation)
    run = baseline("research_run.json")
    run.update(revision_id=rid, revised_on=revision["revised_on"], summary=validation["summary"]["nested"],
               source_count=len(sources), claim_count=len(read_lines(PROJECT / "ledger/claims.jsonl")),
               reproduce="PYTHONPATH=src python3 tools/deepen_gpt6_cost_case.py",
               revision_note=revision["scope"])
    write_json(PROJECT / "research_run.json", run)
    refresh_report()
    verify_prefixes()
    write_json(complete, {"revision_id": rid, "input_sha256": digest(revision), "recorded_at": now,
        "append_only_prefixes_verified": True, "research_status": "partial_research", "actual_roi_verified": False})


if __name__ == "__main__":
    apply_revision()
