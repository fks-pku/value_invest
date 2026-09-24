"""Synthetic fixtures only: never spend model quota or edit the user's research."""
from copy import deepcopy
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import threading
import shutil
import io
from urllib.request import Request, urlopen
from urllib.error import HTTPError

import pytest

from value_invest_research.domain.interactive_research import propose_edit, tree_version, validate_researched_tree
from value_invest_research.application.use_cases.interactive_research import InteractiveResearch
from value_invest_research.adapters.inbound.researcher_server import handler_for
from value_invest_research.adapters.outbound.filesystem_interactive_research import FileSystemInteractiveResearch, write, read, atomic, hashes, project_files
from value_invest_research.adapters.outbound.canonical_markdown_report_renderer import CanonicalMarkdownReportRenderer
from value_invest_research.domain.report_view_model import ReportViewModel
from value_invest_research.adapters.outbound.filesystem_research_plan import FileSystemResearchPlanRepository
from value_invest_research.application.use_cases.research_plan_execution import RecordResearchStepEvent
from value_invest_research.adapters.outbound.codex_research_runner import CodexResearchRunner

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "research/events/gpt6_ai_industry_impact_20260910"


@pytest.fixture
def tree():
    return read(PROJECT / "question_tree_report.json")


def change(tree, nid="F1.1.3", **kwargs):
    return {"node_id": nid, "operation": "edit", "question": "完成一个合格任务的总成本如何变化？", "version": tree_version(tree), **kwargs}


def state_snapshot(tree, revision_id):
    return {"revision_id": revision_id, "current_node_id": "F1.1.3", "research_status": "partial_research",
            "nodes": [{"question_id": n["id"],
                       **{k: n[k] for k in ("parent_id", "level", "question", "conclusion")},
                       "status": "answered" if n["passed"] else "blocked",
                       "sufficiency": {"passed": n["passed"], "gaps": n.get("gaps", [])}}
                      for n in tree["nodes"]]}


def test_leaf_edit_invalidates_only_branch_and_ancestors(tree):
    original = deepcopy(tree)
    edit = propose_edit(tree, change(tree))
    assert edit["research_ids"] == ["F1.1.3"]
    assert edit["rollup_ids"] == ["F1.1", "F1"]
    assert tree == original
    for node in edit["tree"]["nodes"]:
        if node["id"] in edit["affected_ids"]:
            assert not node["passed"] and not node["evidence"]
        else:
            assert node == next(n for n in tree["nodes"] if n["id"] == node["id"])


def test_parent_edit_reruns_descendant_leaves(tree):
    edit = propose_edit(tree, change(tree, "F1.1"))
    assert set(edit["research_ids"]) == {"F1.1.1", "F1.1.2", "F1.1.3"}
    assert "F1.2" not in edit["affected_ids"]


def test_add_and_remove_keep_auditable_scope(tree):
    edit = propose_edit(tree, change(tree, operation="add", reason="需要区分重试与人工复核成本"))
    assert edit["research_ids"] == ["F1.1.3.u1"]
    assert "F1.1.3" in edit["rollup_ids"]
    deleted = propose_edit(tree, change(tree, operation="remove"))
    assert deleted["removed_ids"] == ["F1.1.3"]
    assert set(deleted["research_ids"]) == {"F1.1.1", "F1.1.2"}


@pytest.mark.parametrize("patch", [
    {"node_id": "../escape"}, {"question": ""}, {"question": "a" * 501},
    {"operation": "shell"}, {"node_id": "F1", "operation": "remove"},
    {"operation": "add"}, {"operation": "add", "node_id": "F1", "reason": "new"},
])
def test_invalid_changes_rejected(tree, patch):
    with pytest.raises(ValueError):
        propose_edit(tree, change(tree, **patch))


def test_depth_limit(tree):
    l4 = propose_edit(tree, change(tree, operation="add", reason="specific gap"))["tree"]
    l5 = propose_edit(l4, change(l4, "F1.1.3.u1", operation="add", reason="deeper gap"))["tree"]
    with pytest.raises(ValueError, match="L5"):
        propose_edit(l5, change(l5, "F1.1.3.u1.u1", operation="add", reason="too deep"))


def test_research_result_cannot_change_siblings_or_cutoff(tree):
    proposal = propose_edit(tree, change(tree))
    candidate = deepcopy(proposal["tree"])
    for n in candidate["nodes"]:
        if n["id"] in proposal["affected_ids"]:
            n["conclusion"] = "本轮合成测试答案，仍有缺口。"
    validate_researched_tree(tree, proposal, candidate)
    candidate["as_of_date"] = "2026-09-24"
    with pytest.raises(ValueError, match="截面"):
        validate_researched_tree(tree, proposal, candidate)
    candidate["as_of_date"] = tree["as_of_date"]
    next(n for n in candidate["nodes"] if n["id"] == "F1.2")["conclusion"] = "unauthorized"
    with pytest.raises(ValueError, match="无关问题"):
        validate_researched_tree(tree, proposal, candidate)


class MemoryRepository:
    def __init__(self, tree):
        self.data, self.job, self.published = tree, None, False
    def tree(self): return self.data
    def current_job(self): return self.job
    def process(self): return {"job_id": None, "updates": [], "nodes": []}
    def prepare(self, proposal):
        self.job = {"id": "test", "status": "queued", "workspace": "/unused", "proposal": proposal}
        return self.job
    def save_job(self, job): self.job = deepcopy(job)
    def validate_and_publish(self, job):
        self.published = True
        self.data = job["proposal"]["tree"]


class ControlledRunner:
    def __init__(self, fail=False):
        self.entered, self.release, self.fail = threading.Event(), threading.Event(), fail
    def run(self, workspace, request, progress, cancelled):
        self.entered.set()
        assert self.release.wait(5)
        if self.fail:
            raise ValueError("Synthetic provider failure")


def test_background_success_and_conflict(tree):
    repository, runner = MemoryRepository(tree), ControlledRunner()
    service = InteractiveResearch(repository, runner)
    try:
        service.submit(change(tree))
        assert runner.entered.wait(2)
        with pytest.raises(ValueError, match="已有研究"):
            service.submit(change(tree))
        runner.release.set()
        service.pool.shutdown(wait=True)
        assert repository.job["status"] == "updated" and repository.published
        with pytest.raises(ValueError, match="刷新"):
            service.preview(change(tree))
    finally:
        runner.release.set()
        service.close()


@pytest.mark.parametrize("cancel", [False, True])
def test_failure_or_cancel_never_publishes(tree, cancel):
    repository, runner = MemoryRepository(tree), ControlledRunner(fail=not cancel)
    service = InteractiveResearch(repository, runner)
    service.submit(change(tree))
    assert runner.entered.wait(2)
    if cancel:
        service.cancel()
    runner.release.set()
    service.pool.shutdown(wait=True)
    assert repository.job["status"] == ("cancelled" if cancel else "failed")
    assert not repository.published and repository.data == tree
    service.close()


@pytest.fixture
def repository(tmp_path, tree, monkeypatch):
    project = tmp_path / "project"
    project.mkdir()
    write(project / "question_tree_report.json", tree)
    atomic(project / "professional_report.html", b"old report")
    # Keep synthetic task copies under the test temp root rather than leaving temp files behind.
    import tempfile
    original = tempfile.mkdtemp
    monkeypatch.setattr("value_invest_research.adapters.outbound.filesystem_interactive_research.tempfile.mkdtemp", lambda **kwargs: original(dir=tmp_path, **kwargs))
    return FileSystemInteractiveResearch(project)


def test_prepare_keeps_original_and_hides_runtime(repository):
    tree = repository.tree()
    baseline = hashes(repository.project)
    job = repository.prepare(propose_edit(tree, change(tree)))
    assert hashes(repository.project) == baseline
    assert not Path(job["workspace"]).is_relative_to(repository.project)
    assert (repository.home / "jobs" / job["id"] / "before/question_tree_report.json").exists()
    assert not any(".researcher" in name for name in project_files(repository.project))


def test_external_write_or_ledger_rewrite_rejected(repository):
    atomic(repository.project / "sources.jsonl", b'{"source_id":"test"}\n')
    job = repository.prepare(propose_edit(repository.tree(), change(repository.tree())))
    stage = Path(job["workspace"]) / "project"
    atomic(stage / "sources.jsonl", b'{"source_id":"forged"}\n')
    with pytest.raises(ValueError, match="历史账本"):
        repository.validate_and_publish(job)
    atomic(repository.project / "professional_report.html", b"externally changed")
    with pytest.raises(ValueError, match="其它操作"):
        repository.validate_and_publish(job)


def test_publish_and_restart_recovery(repository):
    job = repository.prepare(propose_edit(repository.tree(), change(repository.tree())))
    stage, before = Path(job["workspace"]) / "project", repository.home / "jobs" / job["id"] / "before"
    atomic(stage / "professional_report.html", b"validated synthetic new report")
    repository._publish(job, stage, before)
    assert (repository.project / "professional_report.html").read_bytes() == b"validated synthetic new report"
    recovered = FileSystemInteractiveResearch(repository.project)
    assert recovered.current_job()["status"] == "updated"


def test_interrupted_publish_rolls_back_only_transaction_files(repository):
    job = repository.prepare(propose_edit(repository.tree(), change(repository.tree())))
    job.update(status="publishing", changed_files=["professional_report.html", "new.json"])
    repository.save_job(job)
    atomic(repository.project / "professional_report.html", b"incomplete")
    write(repository.project / "new.json", {"test": True})
    recovered = FileSystemInteractiveResearch(repository.project)
    assert recovered.current_job()["status"] == "failed"
    assert (repository.project / "professional_report.html").read_bytes() == b"old report"
    assert not (repository.project / "new.json").exists()


def test_shared_markdown_preserves_every_paragraph(tree):
    vm = ReportViewModel(project={"presentation_profile":"question-tree-v1", "question_tree":tree}, goal={}, supply_chain={}, qa_roots=[], targets=[], sources=tree["sources"])
    markdown = CanonicalMarkdownReportRenderer().render(vm)
    for node in tree["nodes"]:
        assert node["question"] in markdown
        for part in node["analysis"]:
            assert part["heading"] in markdown
            for paragraph in part["paragraphs"]:
                # Citation expansion changes only bracketed source identifiers.
                assert paragraph.split("[S")[0] in markdown


def test_http_origin_token_traversal_and_preview(tree, tmp_path):
    repo, runner = MemoryRepository(tree), ControlledRunner()
    service = InteractiveResearch(repo, runner)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(service, tmp_path, "test-secret"))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f"http://127.0.0.1:{server.server_port}"
    def call(path, data=None, **headers):
        request = Request(origin + path, data=json.dumps(data).encode() if data is not None else None,
                          headers={"Content-Type":"application/json", "Origin":origin, "X-Research-Token":"test-secret", **headers})
        with urlopen(request, timeout=3) as response:
            return response.read()
    try:
        assert b"RESEARCH / WORKSPACE" in call("/")
        assert json.loads(call("/api/process")) == {"job_id": None, "updates": [], "nodes": []}
        assert json.loads(call("/api/preview", change(tree)))["research_ids"] == ["F1.1.3"]
        assert repo.current_job() is None  # Preview never consumes model quota.
        for headers in ({"Origin":"https://evil.example"}, {"X-Research-Token":"wrong"}, {"Host":"evil.example"}):
            with pytest.raises(HTTPError) as error:
                call("/api/research", change(tree), **headers)
            assert error.value.code == 403
        for path in ("/.researcher/current.json", "/source/../../project.json", "/assets/../../AGENTS.md"):
            with pytest.raises(HTTPError) as error:
                call(path)
            assert error.value.code == 404
    finally:
        server.shutdown(); server.server_close(); thread.join(); service.close()


@pytest.fixture
def candidate(tmp_path, monkeypatch):
    """A synthetic no-evidence update exercises real plan and publication validators."""
    project = tmp_path / "project"
    for name, path in project_files(PROJECT).items():
        dest = project / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
    import tempfile
    original = tempfile.mkdtemp
    monkeypatch.setattr("value_invest_research.adapters.outbound.filesystem_interactive_research.tempfile.mkdtemp", lambda **kwargs: original(dir=tmp_path, **kwargs))
    repository = FileSystemInteractiveResearch(project)
    proposal = propose_edit(repository.tree(), change(repository.tree()))
    job = repository.prepare(proposal)
    stage = Path(job["workspace"]) / "project"
    tree = deepcopy(proposal["tree"])
    for node in tree["nodes"]:
        if node["id"] in proposal["affected_ids"]:
            node["conclusion"] = "合成测试：未找到足够材料，保留缺口。"
    qa = read(stage / "qa_tree.json")
    next(n for n in qa["nodes"] if n["id"] == "F1.1.3")["question"] = proposal["edit"]["question"]
    write(stage / "qa_tree.json", qa)
    plan_repo = FileSystemResearchPlanRepository(stage)
    parent = plan_repo.load_plan()
    parent["plan_id"] = "rp_test_synthetic_revision"
    next(s for s in parent["steps"] if s["question_node_id"] == "F1.1.3")["question"] = proposal["edit"]["question"]
    plan_repo.save_plan(parent)
    child_repo = FileSystemResearchPlanRepository(stage / "l3_research_plans/F1.1.3")
    child = child_repo.load_plan()
    old_id = child["plan_id"]
    child = json.loads(json.dumps(child).replace(old_id, "l3rp_test_synthetic_revision"))
    child["question_tree"]["question"] = proposal["edit"]["question"]
    child["steps"][0]["question"] = proposal["edit"]["question"]
    child["steps"][0]["question_path"][0]["question"] = proposal["edit"]["question"]
    child_repo.save_plan(child)
    index = read(stage / "l3_research_plans/index.json")
    index["parent_research_plan_id"] = parent["plan_id"]
    next(p for p in index["plans"] if p["l3_node_id"] == "F1.1.3")["l3_plan_id"] = child["plan_id"]
    write(stage / "l3_research_plans/index.json", index)
    event = {"step_id":"question:F1.1.3", "event_type":"step_blocked", "search_run_id":"test_search",
             "gaps":["合成测试无证据"], "next_actions":["等待真实材料"]}
    RecordResearchStepEvent(child_repo).execute(event)
    search = {"revision_id":job["id"], "l3_plan_id":child["plan_id"], "l3_node_id":"F1.1.3", "question_node_id":"F1.1.3",
              "question_level":3, "research_step_id":"question:F1.1.3", "search_run_id":"test_search",
              "queries":["SYNTHETIC TEST ONLY"], "refutation_result":"合成测试，未找到数据"}
    with (stage / "search_runs.jsonl").open("a") as stream:
        stream.write(json.dumps(search) + "\n")
    write(stage / "question_tree_report.json", tree)
    vm = read(stage / "report_view_model.json")
    vm["project"]["question_tree"] = tree
    write(stage / "report_view_model.json", vm)
    write(stage / "project.json", vm["project"])
    if (stage / "research_state.json").exists():
        write(stage / "research_state.json", state_snapshot(tree, job["id"]))
    return repository, job, stage


def test_full_validated_publication_of_partial_research(candidate):
    repository, job, stage = candidate
    repository.validate_and_publish(job)
    assert repository.tree() == read(stage / "question_tree_report.json")
    assert "合成测试：未找到足够材料" in (repository.project / "professional_report.html").read_text()
    assert "合成测试：未找到足够材料" in (repository.project / "professional_report.md").read_text()
    assert read(repository.project / "presentation_validation.json")["html"]["ok"]
    current = {n["id"]: n for n in repository.tree()["nodes"]}
    caches = [read(repository.project / "research_chapters.json"), read(repository.project / "report_view_model.json")["qa_roots"]]
    for chapters in caches:
        chapter = next(c for c in chapters if c["id"] == "F1.1.3")
        for field in ("conclusion", "passed", "analysis", "evidence", "gaps"):
            assert chapter[field] == current["F1.1.3"][field]


def test_skill_state_snapshot_passes_full_publication(candidate):
    repository, job, stage = candidate
    state = state_snapshot(read(stage / "question_tree_report.json"), job["id"])
    write(stage / "research_state.json", state)
    write(stage / "progress.json", {"stage": "synthesizing", "node_id": "F1"})
    repository.validate_and_publish(job)
    assert read(repository.project / "research_state.json") == state
    receipt = read(repository.home / "jobs" / job["id"] / "publication.json")
    assert receipt["committed"] and "research_state.json" in receipt["files"]
    assert "progress.json" not in receipt["files"]
    assert not (repository.project / "progress.json").exists()


@pytest.mark.parametrize("fault", ["revision", "missing", "duplicate", "current", "complete",
                                   "question", "conclusion", "passed", "gaps", "status"])
def test_inconsistent_skill_state_never_publishes(candidate, fault):
    repository, job, stage = candidate
    baseline = hashes(repository.project)
    state = state_snapshot(read(stage / "question_tree_report.json"), job["id"])
    if fault == "revision": state["revision_id"] = "old"
    elif fault == "missing": state["nodes"].pop()
    elif fault == "duplicate": state["nodes"][-1] = deepcopy(state["nodes"][0])
    elif fault == "current": state["current_node_id"] = "missing"
    elif fault == "complete": state["research_status"] = "completed"
    elif fault == "passed": state["nodes"][0]["sufficiency"]["passed"] = True
    elif fault == "gaps": state["nodes"][0]["sufficiency"]["gaps"] = []
    elif fault == "status": state["nodes"][0]["status"] = "answered"
    else: state["nodes"][0][fault] = "contradictory state"
    write(stage / "research_state.json", state)
    with pytest.raises(ValueError, match="研究状态|充分性|节点状态"):
        repository.validate_and_publish(job)
    assert hashes(repository.project) == baseline


def test_unrecognized_output_still_rejected(candidate):
    repository, job, stage = candidate
    baseline = hashes(repository.project)
    write(stage / "unapproved_state.json", {"status": "completed"})
    with pytest.raises(ValueError, match="候选写入超出研究数据范围"):
        repository.validate_and_publish(job)
    assert hashes(repository.project) == baseline


def test_worker_prompt_specifies_source_and_claim_contract(tree):
    prompt = CodexResearchRunner(ROOT).prompt({"id": "test-contract"})
    assert "report_view_model.json.sources" in prompt
    assert "每个 source_id 只注册一次" in prompt
    assert "review_id,claim" in prompt
    assert "sufficiency.passed/gaps" in prompt


@pytest.mark.parametrize("location", ["progress.json", "project/progress.json"])
def test_engine_reads_progress_from_supported_locations(tmp_path, monkeypatch, tree, location):
    audit, work = tmp_path / "audit", tmp_path / "work"
    audit.mkdir(); work.mkdir()
    write(work / location, {"stage": "synthesizing", "node_id": "F1"})
    runner = CodexResearchRunner(ROOT)
    runner.executable = "/test/codex"
    def process(*args, **kwargs):
        kwargs["stdout"].write(json.dumps({"type": "item.completed", "item": {"type": "web_search"}}) + "\n")
        class FakeProcess:
            returncode = 0
            stdin = io.StringIO()
            polls = 0
            def poll(self):
                self.polls += 1
                return None if self.polls == 1 else 0
        return FakeProcess()
    monkeypatch.setattr("value_invest_research.adapters.outbound.codex_research_runner.subprocess.Popen", process)
    monkeypatch.setattr("value_invest_research.adapters.outbound.codex_research_runner.time.sleep", lambda *_: None)
    messages = []
    job = {"id": "test-progress", "audit_dir": str(audit), "proposal": propose_edit(tree, change(tree))}
    runner.run(str(work), job, messages.append, lambda: False)
    assert messages == ["正在汇总父问题与投资边界 · F1"]


def test_fresh_search_required_even_for_blocked_answer(candidate):
    repository, job, stage = candidate
    before = repository.home / "jobs" / job["id"] / "before"
    atomic(stage / "search_runs.jsonl", (before / "search_runs.jsonl").read_bytes())
    with pytest.raises(ValueError, match="逐题检索"):
        repository.validate_and_publish(job)


def test_changed_question_cannot_reuse_old_source_review(candidate):
    repository, job, stage = candidate
    before = repository.home / "jobs" / job["id"] / "before"
    tree = read(stage / "question_tree_report.json")
    old = next(n for n in read(before / "question_tree_report.json")["nodes"] if n["id"] == "F1.1.3")
    next(n for n in tree["nodes"] if n["id"] == "F1.1.3")["evidence"] = old["evidence"]
    vm = read(stage / "report_view_model.json")
    vm["project"]["question_tree"] = tree
    write(stage / "question_tree_report.json", tree)
    write(stage / "report_view_model.json", vm)
    write(stage / "project.json", vm["project"])
    with pytest.raises(ValueError, match="本轮逐题抽取"):
        repository.validate_and_publish(job)


@pytest.mark.parametrize("with_search", [False, True])
def test_engine_uses_stdin_sandbox_and_requires_real_search_transcript(tmp_path, monkeypatch, tree, with_search):
    audit = tmp_path / "private-audit"
    work = tmp_path / "worker"
    audit.mkdir(); work.mkdir()
    runner = CodexResearchRunner(ROOT)
    runner.executable = "/test/codex"
    captured = {}
    def process(command, **kwargs):
        captured.update(command=command, kwargs=kwargs)
        if with_search:
            kwargs["stdout"].write(json.dumps({"type":"item.completed", "item":{"type":"web_search", "query":"test only"}}) + "\n")
        class FakeProcess:
            returncode = 0
            stdin = io.StringIO()
            def poll(self): return 0
        return FakeProcess()
    monkeypatch.setattr("value_invest_research.adapters.outbound.codex_research_runner.subprocess.Popen", process)
    job = {"id":"synthetic", "audit_dir":str(audit), "proposal":propose_edit(tree, change(tree))}
    if with_search:
        runner.run(str(work), job, lambda *_: None, lambda: False)
    else:
        with pytest.raises(ValueError, match="没有完成的联网检索"):
            runner.run(str(work), job, lambda *_: None, lambda: False)
    command = captured["command"]
    assert command[-1] == "-" and "--ignore-user-config" in command
    assert command[command.index("--sandbox") + 1] == "workspace-write"
    assert captured["kwargs"].get("shell") is None
    assert not any(job["proposal"]["edit"]["question"] in arg for arg in command)
    assert (audit / "engine.jsonl").exists() and not (work / "engine.jsonl").exists()
