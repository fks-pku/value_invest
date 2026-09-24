"""Read-only public progress projection; never serve raw worker logs or reasoning."""
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, urlunsplit


def safe_text(value, limit=1800):
    value = str(value or "")
    if re.search(r"(?i)(api[_ -]?key|authorization|bearer\s|password|cookie|access[_ -]?token|sk-[a-z0-9])", value):
        return "该条记录含内部字段，未公开展示。"
    value = re.sub(r"```[\s\S]*?```", "[执行细节省略]", value)
    value = re.sub(r"(?:/Users/|/private/|/var/folders/)[^\s\"'，。；]+", "[本地路径]", value)
    value = re.sub(r"https?://[^\s<>\])，。]+", lambda m: safe_url(m[0]), value)
    return value[:limit]


def safe_url(value):
    try:
        parsed = urlsplit(str(value or ""))
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
            return ""
        # Queries/fragments may carry provider or session credentials.
        return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
    except ValueError:
        return ""


def load(root, name, lines=False):
    root = root.resolve()
    path = root / name
    if any((root / Path(*Path(name).parts[:i])).is_symlink() for i in range(1, len(Path(name).parts) + 1)):
        return [] if lines else {}
    try:
        with path.open("rb") as stream:
            content = stream.read(8_000_001)
        if len(content) > 8_000_000:
            return [] if lines else {}
        if not lines:
            return json.loads(content)
        result = []
        for line in content.splitlines():
            try:
                row = json.loads(line)
                if isinstance(row, dict):
                    result.append(row)
            except (ValueError, UnicodeError):
                continue  # A worker may currently be appending the final line.
        return result
    except (OSError, ValueError, UnicodeError):
        return [] if lines else {}


def research_process_snapshot(job):
    if not job:
        return {"job_id": None, "nodes": [], "updates": []}
    stage = Path(job["workspace"]) / "project"
    audit = Path(job["audit_dir"])
    if job["status"] == "updated" and (audit / "after").is_dir():
        stage = audit / "after"
    events = load(audit, "engine.jsonl", lines=True)
    updates, searches_done, commands_done = [], 0, 0
    for event in events:
        item = event.get("item", {})
        if event.get("type") != "item.completed" or not isinstance(item, dict):
            continue
        kind = item.get("type")
        if kind == "agent_message" and isinstance(item.get("text"), str):
            updates.append({"sequence": len(updates) + 1, "text": safe_text(item["text"])})
        elif kind in {"web_search", "web_search_call"}:
            searches_done += 1
        elif kind == "command_execution" and item.get("status") == "completed":
            commands_done += 1
    def fresh(name):
        return [r for r in load(stage, name, lines=True) if r.get("revision_id") == job["id"]]
    searches = fresh("search_runs.jsonl")
    extracts = fresh("source_extractions.jsonl")
    reviews = fresh("source_reviews.jsonl")
    source_rows = load(stage, "sources.jsonl", lines=True)
    sources = {s.get("source_id"): s for s in source_rows}
    tree = load(stage, "question_tree_report.json")
    drafts = {n.get("id"): n for n in tree.get("nodes", []) if isinstance(n, dict)} if isinstance(tree, dict) else {}
    proposal = job["proposal"]
    by_id = {n["id"]: n for n in proposal["tree"]["nodes"]}
    nodes = []
    for node in proposal["tree"]["nodes"]:
        nid = node["id"]
        if nid not in proposal["affected_ids"]:
            continue
        ancestor = node
        while ancestor.get("level", 3) > 3 and ancestor.get("parent_id") in by_id:
            ancestor = by_id[ancestor["parent_id"]]
        step = {}
        if re.fullmatch(r"[A-Za-z0-9_.-]+", ancestor["id"]):
            name = f"l3_research_plans/{ancestor['id']}/research_plan.json"
            plan, old_plan = load(stage, name), load(audit / "before", name)
            if isinstance(plan, dict) and isinstance(old_plan, dict) and plan.get("plan_id") and plan.get("plan_id") != old_plan.get("plan_id"):
                step = next((s for s in plan.get("steps", []) if s.get("question_node_id") == nid and s.get("question") == node["question"]), {})
        xs = {r.get("extraction_id"): r for r in extracts if r.get("question_node_id") == nid and r.get("extraction_id")}
        rs = {r.get("review_id"): r for r in reviews if r.get("question_node_id") == nid and r.get("review_id")}
        runs = {r.get("search_run_id") for r in searches if r.get("question_node_id") == nid and r.get("search_run_id")}
        # Never project an old answer under a new question.
        draft = drafts.get(nid, {})
        if (draft.get("revision_id") != job["id"] or draft.get("question") != node["question"]
                or draft.get("conclusion") == node.get("conclusion")):
            draft = {}
        materials = []
        for sid in dict.fromkeys(r.get("source_id") for r in xs.values()):
            source = sources.get(sid)
            if source:
                materials.append({"title": safe_text(source.get("title"), 200), "url": safe_url(source.get("url")),
                                  "date": safe_text(source.get("published_at"), 30)})
        nodes.append({"id": nid, "question": node["question"], "role": "leaf" if nid in proposal["research_ids"] else "rollup",
                      "search_runs": len(runs), "extractions": len(xs), "reviews": len(rs), "sources": materials[:12],
                      "data_required": [safe_text(t, 300) for t in step.get("required_data", [])[:6]],
                      "analysis_plan": [safe_text(t, 300) for t in step.get("analysis_plan", [])[:6]],
                      "conclusion": safe_text(draft.get("conclusion")),
                      "gaps": [safe_text(t, 300) for t in draft.get("gaps", [])[:6]],
                      "passed": draft.get("passed") if draft else None})
    try:
        last_activity = datetime.fromtimestamp((audit / "engine.jsonl").stat().st_mtime, timezone.utc).isoformat()
    except OSError:
        last_activity = job.get("updated_at")
    return {"job_id": job["id"], "status": job["status"], "created_at": job.get("created_at"),
            "last_activity_at": last_activity, "web_searches": searches_done, "execution_steps": commands_done,
            "updates": updates[-12:], "nodes": nodes,
            "note": "进展摘要是执行器公开的工作汇报；草稿及数量不代表证据门禁通过。原始命令、内部推理和日志不展示。"}
