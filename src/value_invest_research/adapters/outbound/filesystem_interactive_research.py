"""Versioned job workspace, conservative evidence checks and recoverable publication."""
from datetime import date, datetime, timezone
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import uuid

from value_invest_research.domain.interactive_research import validate_researched_tree, validate_research_state
from value_invest_research.domain.report_view_model import ReportViewModel
from value_invest_research.domain.research_plan import validate_research_plan_execution
from value_invest_research.adapters.outbound.filesystem_research_plan import FileSystemResearchPlanRepository
from value_invest_research.application.use_cases.research_plan_execution import ValidateResearchPlanExecution
from value_invest_research.adapters.outbound.canonical_html_report_renderer import CanonicalHtmlReportRenderer
from value_invest_research.adapters.outbound.canonical_markdown_report_renderer import CanonicalMarkdownReportRenderer
from value_invest_research.framework_contracts import validate_report_contract_html, validate_report_contract_markdown


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode())


def atomic(path, data):
    """Same-directory replace; no partial file is ever visible to the report reader."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".research-write-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []


def project_files(folder):
    """No secrets, code, hidden directories, external symlinks, or provider archives."""
    result = {}
    for path in folder.rglob("*"):
        relative = path.relative_to(folder)
        if any(p.startswith(".") for p in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError("研究副本不支持符号链接。")
        if relative.as_posix() == "progress.json":
            # Worker progress is runtime-only, including workers using project/ as cwd.
            continue
        if path.is_file() and path.suffix in {".json", ".jsonl", ".md", ".html", ".pdf"}:
            result[relative.as_posix()] = path
    return result


def hashes(folder):
    return {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in project_files(folder).items()}


MUTABLE = {
    "project.json", "qa_tree.json", "research_plan.json", "research_plan.md", "research_brief.json",
    "question_tree_report.json", "report_view_model.json", "professional_report.html", "professional_report.md",
    "source_catalog.json", "research_run.json", "target_gates.json", "research_chapters.json", "report_synthesis.json",
    "plan_validation.json", "presentation_validation.json", "research_state.json",
}


def project_chapter_cache(chapters, tree, searches, job):
    """Keep legacy read-side chapter caches aligned with validated tree answers."""
    nodes = {n["id"]: n for n in tree["nodes"]}
    result = [c for c in chapters if c["id"] in nodes and nodes[c["id"]]["mode"] == "leaf"
              and c["id"] not in job["proposal"]["affected_ids"]]
    for nid in job["proposal"]["research_ids"]:
        node = nodes[nid]
        ancestor = node
        while ancestor["level"] > 3:
            ancestor = nodes[ancestor["parent_id"]]
        result.append({"id": nid, "l3_id": ancestor["id"],
                       **{k: node[k] for k in ("conclusion", "passed", "analysis", "evidence", "gaps", "refutation", "next_actions")},
                       "gate_reason": "；".join(node["reasons"]),
                       "support": [e["fact"] for e in node["evidence"] if e.get("effect") == "support"],
                       "searches": [q for s in searches if s.get("question_node_id") == nid
                                    and s.get("revision_id") == job["id"] for q in s.get("queries", [])]})
    order = {nid: i for i, nid in enumerate(nodes)}
    return sorted(result, key=lambda c: order[c["id"]])


class FileSystemInteractiveResearch:
    def __init__(self, project: Path):
        self.project = project.resolve()
        self.home = self.project / ".researcher"
        self.home.mkdir(exist_ok=True)
        self.recover()

    def tree(self):
        return read(self.project / "question_tree_report.json")

    def process(self):
        from value_invest_research.adapters.outbound.research_process_snapshot import research_process_snapshot
        return research_process_snapshot(self.current_job())

    def current_job(self):
        path = self.home / "current.json"
        return read(path) if path.exists() else None

    def save_job(self, job):
        job["updated_at"] = datetime.now(timezone.utc).isoformat()
        write(self.home / "jobs" / job["id"] / "job.json", job)
        write(self.home / "current.json", job)

    def prepare(self, proposal):
        identifier = "edit_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "_" + uuid.uuid4().hex[:8]
        folder = self.home / "jobs" / identifier
        folder.mkdir(parents=True)
        # Outside the original Git root, so workspace-write cannot grant writes to the original repository.
        workspace = Path(tempfile.mkdtemp(prefix="value-researcher-"))
        for name, path in project_files(self.project).items():
            for destination in (folder / "before" / name, workspace / "project" / name):
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)
        job = {"id": identifier, "status": "queued", "message": "等待研究执行",
               "created_at": datetime.now(timezone.utc).isoformat(), "workspace": str(workspace),
               "audit_dir": str(folder),
               "proposal": proposal, "baseline": hashes(self.project)}
        self.save_job(job)
        return job

    def validate_and_publish(self, job):
        stage = Path(job["workspace"]) / "project"
        before = self.home / "jobs" / job["id"] / "before"
        if hashes(self.project) != job["baseline"]:
            raise ValueError("研究期间原项目被其它操作修改。候选版本已保留，请刷新重试，避免覆盖。")
        files = project_files(stage)
        missing = set(job["baseline"]) - set(files)
        if missing:
            raise ValueError("候选版本删除了原研究文件，拒绝发布。")
        for name, path in files.items():
            original = before / name
            if original.exists() and path.read_bytes() == original.read_bytes():
                continue
            if path.suffix == ".jsonl":
                if original.exists() and not path.read_bytes().startswith(original.read_bytes()):
                    raise ValueError(f"历史账本被改写：{name}")
            elif "research_plan_history/" in name or name.startswith("research_revisions/"):
                if original.exists():
                    raise ValueError(f"不可变历史被修改：{name}")
            elif name not in MUTABLE and not (name.startswith("l3_research_plans/") and name.endswith(("/research_plan.json", "/index.json"))) and name != "l3_research_plans/index.json":
                raise ValueError(f"候选写入超出研究数据范围：{name}")
        tree = read(stage / "question_tree_report.json")
        validate_researched_tree(read(before / "question_tree_report.json"), job["proposal"], tree)
        if (stage / "research_state.json").exists():
            validate_research_state(read(stage / "research_state.json"), tree, job["id"])
        vm = ReportViewModel(**read(stage / "report_view_model.json"))
        if vm.project.get("question_tree") != tree or vm.sources != tree["sources"]:
            raise ValueError("HTML/Markdown 视图模型与问题树或来源不一致。")
        project = read(stage / "project.json")
        if project.get("question_tree") != tree:
            raise ValueError("project.json 的问题树未同步。")
        qa = {n["id"]: n for n in read(stage / "qa_tree.json")["nodes"]}
        if set(qa) != {n["id"] for n in tree["nodes"]} or any(
            any(qa[n["id"]].get(k) != n.get(k) for k in ("question", "parent_id", "level")) for n in tree["nodes"]):
            raise ValueError("研究 QA 与显示问题树不一致。")
        original_project = read(before / "project.json")
        for field in ("as_of_date", "run_mode", "project_id"):
            if vm.project.get(field) != original_project.get(field) or project.get(field) != original_project.get(field):
                raise ValueError("项目身份、模式或历史截面被改变。")
        if any(t.get("action_state") == "actionable_long" for t in vm.targets):
            raise ValueError("交互重研不能自动升级为 actionable_long。")
        self._validate_fresh_evidence(stage, before, job, tree)
        plan_result = ValidateResearchPlanExecution(FileSystemResearchPlanRepository(stage)).execute()
        if not plan_result["ok"]:
            write(Path(job["workspace"]) / "validation_failure.json", plan_result)
            raise ValueError("研究计划/证据事件校验未通过，候选与详细问题已保留，正式报告未变。")
        searches = rows(stage / "search_runs.jsonl")
        vm = replace(vm, qa_roots=project_chapter_cache(vm.qa_roots, tree, searches, job))
        if (stage / "research_chapters.json").exists():
            write(stage / "research_chapters.json", project_chapter_cache(read(stage / "research_chapters.json"), tree, searches, job))
        vm.project["interactive_revision"] = job["id"]
        project["interactive_revision"] = job["id"]
        write(stage / "project.json", project)
        write(stage / "report_view_model.json", vm.to_dict())
        html = CanonicalHtmlReportRenderer().render(vm)
        markdown = CanonicalMarkdownReportRenderer().render(vm)
        html_check, md_check = validate_report_contract_html(html), validate_report_contract_markdown(markdown)
        if not html_check["ok"] or not md_check["ok"]:
            write(Path(job["workspace"]) / "validation_failure.json", {"html": html_check, "markdown": md_check})
            raise ValueError("共享报告格式校验失败，未发布。")
        atomic(stage / "professional_report.html", html.encode())
        atomic(stage / "professional_report.md", markdown.encode())
        write(stage / "plan_validation.json", plan_result)
        write(stage / "presentation_validation.json", {"html": html_check, "markdown": md_check,
              "visual_review": "not_performed_by_background_worker", "full_legacy_audit": "not_claimed"})
        revision = stage / "research_revisions" / job["id"]
        write(revision / "edit.json", {"revision_id": job["id"], "edit": job["proposal"]["edit"],
              "affected_ids": job["proposal"]["affected_ids"], "research_ids": job["proposal"]["research_ids"],
              "rollup_ids": job["proposal"]["rollup_ids"], "removed_ids": job["proposal"]["removed_ids"],
              "created_at": job["created_at"], "as_of_date": tree["as_of_date"],
              "prior_tree_sha256": job["baseline"]["question_tree_report.json"]})
        atomic(revision / "before_question_tree.json", (before / "question_tree_report.json").read_bytes())
        self._publish(job, stage, before)

    def _validate_fresh_evidence(self, stage, before, job, tree):
        def fresh(name):
            old_count = len(rows(before / name))
            return rows(stage / name)[old_count:]
        searches = fresh("search_runs.jsonl")
        extracts = fresh("source_extractions.jsonl")
        reviews = fresh("source_reviews.jsonl")
        claims = fresh("ledger/claims.jsonl")
        sources = {}
        for source in rows(stage / "sources.jsonl"):
            sid = source["source_id"]
            if sid in sources and source != sources[sid]:
                raise ValueError("既有 source_id 不能被追加记录重新定义。")
            sources[sid] = source
        for source in tree["sources"]:
            if source != sources.get(source["source_id"]):
                raise ValueError("报告来源与来源账本不一致。")
        by_id = {n["id"]: n for n in tree["nodes"]}
        bundle = FileSystemResearchPlanRepository(stage).load_l3_research_plan_bundle()
        prior_bundle = FileSystemResearchPlanRepository(before).load_l3_research_plan_bundle()
        previous_plans = {p["l3_node_id"]: p for p in prior_bundle["plans"]}
        plans = {p["l3_node_id"]: p for p in bundle["plans"]}
        for nid in job["proposal"]["research_ids"]:
            node = by_id[nid]
            ancestor = node
            while ancestor["level"] > 3:
                ancestor = by_id[ancestor["parent_id"]]
            l3id = ancestor["id"]
            if node["level"] < 3 or l3id not in plans:
                raise ValueError(f"{nid} 需要先建立 L3 执行计划；请补全到 L3 后研究。")
            plan = plans[l3id]
            if previous_plans.get(l3id, {}).get("plan_id") == plan["plan_id"]:
                raise ValueError(f"{nid} 未创建本轮独立计划版本。")
            step = next((s for s in plan["steps"] if s["question_node_id"] == nid), None)
            if not step or step["question"] != node["question"]:
                raise ValueError(f"{nid} 的当前步骤问题未同步。")
            expected = {"revision_id": job["id"], "l3_plan_id": plan["plan_id"], "l3_node_id": l3id,
                        "question_node_id": nid, "question_level": node["level"], "research_step_id": step["step_id"]}
            matches = lambda row: all(row.get(k) == v for k, v in expected.items())
            runs = [s for s in searches if matches(s) and s.get("queries") and s.get("refutation_result")]
            if not runs:
                raise ValueError(f"{nid} 缺少本轮逐题检索及反向检索记录。")
            run_ids = {s["search_run_id"] for s in runs}
            for evidence in node.get("evidence", []):
                source = sources.get(evidence["source"], {})
                published = str(source.get("published_at", ""))[:10]
                try:
                    visible_date = date.fromisoformat(published)
                except ValueError:
                    raise ValueError(f"{nid} 的来源日期未经验证。")
                if visible_date > date.fromisoformat(tree["as_of_date"]):
                    raise ValueError(f"{nid} 存在无日期或超截面来源。")
                candidates = [e for e in extracts if matches(e) and e.get("search_run_id") in run_ids
                              and e.get("source_id") == evidence["source"] and e.get("fact") == evidence["fact"]
                              and e.get("locator") == evidence["locator"] and e.get("boundary")]
                verified = [(e, r) for e in candidates for r in reviews if matches(r) and r.get("search_run_id") == e["search_run_id"]
                           and r.get("source_id") == e["source_id"] and r.get("extraction_id") == e.get("extraction_id")
                           and r.get("review_id") and r.get("review") and r.get("decision") in {"verified", "verified_with_stated_boundary"}]
                if not verified:
                    raise ValueError(f"{nid} 的证据没有本轮逐题抽取及已核实复核。")
                if not any(c for e, r in verified for c in claims if c.get("question_node_id") == nid
                           and c.get("source_id") == e["source_id"] and c.get("extraction_id") == e["extraction_id"]
                           and c.get("review_id") == r["review_id"] and c.get("claim") == evidence["fact"]):
                    raise ValueError(f"{nid} 的证据缺少本轮原子观点账本关联。")
            state = validate_research_plan_execution(plan, bundle["events_by_node"].get(l3id, []))
            if node["passed"]:
                completed = next((s for s in state["step_states"] if s.get("step_id") == step["step_id"] and s.get("status") == "completed"), None)
                if not completed:
                    raise ValueError(f"{nid} 报告通过状态缺乏执行门禁支持。")
                if not set(completed["source_extraction_ids"]) <= {e["extraction_id"] for e in extracts if matches(e)} or not set(completed["source_review_ids"]) <= {r["review_id"] for r in reviews if matches(r)}:
                    raise ValueError(f"{nid} 完成事件引用了其它版本的证据。")

    def _publish(self, job, stage, before):
        files = project_files(stage)
        changed = [name for name, path in files.items() if not (before / name).exists() or path.read_bytes() != (before / name).read_bytes()]
        # The journal precedes writes. A failed/interrupted transaction rolls back from immutable before/.
        job.update(status="publishing", changed_files=changed, message="正在发布已校验的新版本")
        self.save_job(job)
        try:
            for name in changed:
                atomic(self.project / name, files[name].read_bytes())
            # Archive candidate and receipt before marking the transaction committed.
            shutil.copytree(stage, self.home / "jobs" / job["id"] / "after", dirs_exist_ok=True)
            write(self.home / "jobs" / job["id"] / "publication.json", {"committed": True, "files": changed})
        except Exception:
            self._rollback(job)
            raise ValueError("发布写入失败，已恢复上一个版本；候选文件保留。")

    def _rollback(self, job):
        before = self.home / "jobs" / job["id"] / "before"
        for name in job.get("changed_files", []):
            old, destination = before / name, self.project / name
            if old.exists():
                atomic(destination, old.read_bytes())
            elif destination.exists():
                # Only remove files listed in this transaction, which did not exist before.
                destination.unlink()

    def recover(self):
        job = self.current_job()
        if not job or job["status"] not in {"queued", "running", "validating", "publishing"}:
            return
        receipt = self.home / "jobs" / job["id"] / "publication.json"
        if receipt.exists() and read(receipt).get("committed"):
            job.update(status="updated", message="已恢复已发布版本。")
        else:
            if job["status"] == "publishing":
                self._rollback(job)
            job.update(status="failed", message="上次服务中断。正式报告保持原版，草稿保留；可重试。")
        self.save_job(job)
