"""Synthetic progress records: no model calls or real research mutations."""
import json

from value_invest_research.adapters.outbound.filesystem_interactive_research import write, atomic
from value_invest_research.adapters.outbound.research_process_snapshot import research_process_snapshot, safe_url, safe_text


def setup_job(tmp_path):
    stage, audit = tmp_path / "work/project", tmp_path / "audit"
    stage.mkdir(parents=True); audit.mkdir()
    node = {"id": "F1.1.2", "question": "技术能力怎样变化？", "conclusion": "等待重新研究", "data_required": ["同任务测评"]}
    job = {"id": "test-run", "status": "running", "workspace": str(stage.parent), "audit_dir": str(audit),
           "proposal": {"tree": {"nodes": [node]}, "affected_ids": [node["id"]], "research_ids": [node["id"]]},
           "updated_at": "2026-09-24T09:00:00Z"}
    return job, stage, audit


def ledger(path, values):
    atomic(path, ("\n".join(json.dumps(v, ensure_ascii=False) for v in values) + "\n").encode())


def test_empty_progress_does_not_claim_completed_research(tmp_path):
    assert research_process_snapshot(None)["job_id"] is None
    job, _, _ = setup_job(tmp_path)
    progress = research_process_snapshot(job)
    assert progress["web_searches"] == 0 and progress["updates"] == []
    assert progress["nodes"][0]["conclusion"] == ""
    assert progress["nodes"][0]["passed"] is None


def test_public_messages_only_and_tolerates_incomplete_event(tmp_path):
    job, _, audit = setup_job(tmp_path)
    ledger(audit / "engine.jsonl", [
        {"type": "item.completed", "item": {"type": "reasoning", "text": "PRIVATE_THOUGHT"}},
        {"type": "item.completed", "item": {"type": "command_execution", "status": "completed", "command": "PRIVATE_COMMAND", "aggregated_output": "PRIVATE_OUTPUT"}},
        {"type": "item.completed", "item": {"type": "agent_message", "text": "已核对原文，样本限制仍需说明。"}},
        {"type": "item.started", "item": {"type": "web_search"}},
        {"type": "item.completed", "item": {"type": "web_search", "query": "PRIVATE_QUERY"}},
    ])
    atomic(audit / "engine.jsonl", (audit / "engine.jsonl").read_bytes() + b'{"partial":')
    result = research_process_snapshot(job)
    assert result["web_searches"] == 1 and result["execution_steps"] == 1
    assert result["updates"][0]["text"] == "已核对原文，样本限制仍需说明。"
    assert "PRIVATE_" not in json.dumps(result)
    assert str(tmp_path) not in json.dumps(result)


def test_counts_and_materials_are_question_and_revision_specific(tmp_path):
    job, stage, _ = setup_job(tmp_path)
    trace = {"revision_id": "test-run", "question_node_id": "F1.1.2"}
    ledger(stage / "search_runs.jsonl", [{**trace, "search_run_id": "search-1"}])
    ledger(stage / "source_extractions.jsonl", [{**trace, "extraction_id": "x1", "source_id": "s1"},
           {**trace, "revision_id": "old", "extraction_id": "old", "source_id": "old"}])
    ledger(stage / "source_reviews.jsonl", [{**trace, "review_id": "r1"}])
    ledger(stage / "sources.jsonl", [{"source_id": "s1", "title": "评测原文", "url": "https://example.com/report?secret=abc", "published_at": "2026-09-03"}])
    node = research_process_snapshot(job)["nodes"][0]
    assert (node["search_runs"], node["extractions"], node["reviews"]) == (1, 1, 1)
    assert node["sources"][0]["url"] == "https://example.com/report"
    assert node["conclusion"] == ""


def test_only_revised_matching_plan_is_shown(tmp_path):
    job, stage, audit = setup_job(tmp_path)
    plan = {"plan_id": "old-plan", "steps": [{"question_node_id": "F1.1.2", "question": "技术能力怎样变化？",
            "required_data": ["新数据目标"], "analysis_plan": ["同任务比较"]}]}
    name = "l3_research_plans/F1.1.2/research_plan.json"
    write(stage / name, plan); write(audit / "before" / name, plan)
    assert research_process_snapshot(job)["nodes"][0]["analysis_plan"] == []
    plan["plan_id"] = "new-plan"
    write(stage / name, plan)
    node = research_process_snapshot(job)["nodes"][0]
    assert node["data_required"] == ["新数据目标"] and node["analysis_plan"] == ["同任务比较"]


def test_old_draft_hidden_but_current_conclusion_visible(tmp_path):
    job, stage, _ = setup_job(tmp_path)
    draft = {**job["proposal"]["tree"]["nodes"][0], "revision_id": "old", "conclusion": "新发现", "passed": False, "gaps": ["缺复测"]}
    write(stage / "question_tree_report.json", {"nodes": [draft]})
    assert research_process_snapshot(job)["nodes"][0]["conclusion"] == ""
    draft["revision_id"] = job["id"]
    write(stage / "question_tree_report.json", {"nodes": [draft]})
    current = research_process_snapshot(job)["nodes"][0]
    assert current["conclusion"] == "新发现" and current["passed"] is False
    job["status"] = "updated"
    assert research_process_snapshot(job)["nodes"][0]["conclusion"] == "新发现"


def test_progress_never_follows_worker_symlinks(tmp_path):
    job, stage, _ = setup_job(tmp_path)
    secret = tmp_path / "private.json"
    write(secret, {"nodes": [{"id": "F1.1.2", "revision_id": "test-run", "conclusion": "SECRET"}]})
    (stage / "question_tree_report.json").symlink_to(secret)
    assert research_process_snapshot(job)["nodes"][0]["conclusion"] == ""


def test_published_progress_survives_temp_workspace_cleanup(tmp_path):
    job, _, audit = setup_job(tmp_path)
    job["status"] = "updated"
    draft = {**job["proposal"]["tree"]["nodes"][0], "revision_id": job["id"], "conclusion": "已归档结论", "passed": False}
    write(audit / "after/question_tree_report.json", {"nodes": [draft]})
    job["workspace"] = str(tmp_path / "no-longer-exists")
    assert research_process_snapshot(job)["nodes"][0]["conclusion"] == "已归档结论"


def test_sensitive_fields_and_unsafe_links_are_not_exposed():
    assert "secret-value" not in safe_text("api_key=secret-value")
    assert "/Users/" not in safe_text("文件 /Users/test/private.json 已读取")
    assert "secret=value" not in safe_text("查看 https://example.com/test?secret=value")
    for url in ["javascript:alert(1)", "file:///Users/test/private", "https://user:password@example.com/x"]:
        assert safe_url(url) == ""
