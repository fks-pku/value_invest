"""Presentation-neutral contract for the versioned dynamic-research reading template."""
from __future__ import annotations

import re
from html.parser import HTMLParser
from urllib.parse import urlsplit

PROFILE = "question-tree-v1"
SECTIONS = ("scope", "data", "analysis", "conclusion")
LEAF_TITLES = ("研究问题与口径", "核心数据与原始证据", "分析正文", "结论与充分性判断")
PARENT_TITLES = ("汇总问题与口径", "下层结论与汇总依据", "综合分析", "结论与充分性判断")


def safe_link(url: str) -> bool:
    """Local artifact links and HTTPS/HTTP originals only; no executable protocols."""
    url = str(url).strip()
    parts = urlsplit(url)
    return bool(url) and not any(ord(c) < 32 for c in url) and not url.startswith(("//", "\\")) and parts.scheme.lower() in {"", "https", "http"}


def validate_question_tree_report(report: dict) -> list[str]:
    errors = []
    nodes = report.get("nodes", [])
    by_id = {n.get("id"): n for n in nodes}
    if report.get("template_version") != PROFILE:
        errors.append("template_version must be question-tree-v1")
    if not report.get("title") or not nodes or len(nodes) != len(by_id):
        errors.append("title and nonempty uniquely identified nodes are required")
    roots = [n for n in nodes if not n.get("parent_id")]
    if len(roots) != 1 or roots[0].get("level") != 1:
        errors.append("exactly one L1 root is required")
    sources = {s.get("source_id"): s for s in report.get("sources", [])}
    for source in sources.values():
        if not safe_link(source.get("url", "")):
            errors.append(f"unsafe source URL: {source.get('source_id')}")
    for link in report.get("attachments", []):
        if not safe_link(link.get("href", "")):
            errors.append("unsafe attachment URL")
    for node in nodes:
        nid = str(node.get("id", ""))
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]*", nid):
            errors.append(f"unsafe node id: {nid}")
        for field in ("question", "what", "acceptance_rule", "conclusion"):
            if not str(node.get(field, "")).strip():
                errors.append(f"{nid}: missing {field}")
        for field in ("data_required", "analysis", "next_actions", "reasons"):
            if not isinstance(node.get(field), list) or not node[field]:
                errors.append(f"{nid}: missing {field}")
        if not isinstance(node.get("passed"), bool):
            errors.append(f"{nid}: passed must be boolean")
        if not node.get("passed") and not node.get("gaps"):
            errors.append(f"{nid}: unpassed node must retain gaps")
        level = node.get("level", 0)
        if not isinstance(level, int) or not 1 <= level <= 5:
            errors.append(f"{nid}: depth must be L1-L5")
        parent = by_id.get(node.get("parent_id"))
        if node.get("parent_id") and (not parent or level != parent.get("level", -1) + 1):
            errors.append(f"{nid}: invalid parent or level")
        children = [c for c in nodes if c.get("parent_id") == nid]
        if node.get("mode") != ("rollup" if children else "leaf"):
            errors.append(f"{nid}: mode must match actual child structure")
        if children and node.get("evidence"):
            errors.append(f"{nid}: parent cannot masquerade as fresh leaf evidence")
        if children and node.get("passed") and any(not c.get("passed") for c in children):
            errors.append(f"{nid}: parent cannot pass with an unpassed mandatory child")
        if not children and node.get("passed") and not node.get("evidence"):
            errors.append(f"{nid}: passed leaf requires evidence")
        for item in node.get("evidence", []):
            if item.get("source") not in sources or not item.get("locator") or not item.get("fact") or not item.get("boundary"):
                errors.append(f"{nid}: evidence needs source, locator, fact and boundary")
        for section in node.get("analysis", []):
            if not section.get("heading") or not section.get("paragraphs"):
                errors.append(f"{nid}: analysis requires titled paragraphs")
    return errors


class _TemplateParser(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.nodes = []
        self.links = []
        self.ids = []
        self.current = None
        self.heading = False
        self.runtime_fetch = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "a":
            self.links.append(a)
        if tag == "article" and "node-detail" in a.get("class", "").split():
            self.current = {**a, "sections": [], "rollups": [], "tables": [], "titles": []}
            self.nodes.append(self.current)
        if self.current and tag == "section" and a.get("data-section"):
            self.current["sections"].append(a["data-section"])
        if self.current and a.get("data-child-id"):
            self.current["rollups"].append(a["data-child-id"])
        if self.current and tag == "table":
            self.current["tables"].append(a.get("class", ""))
        if self.current and tag == "h3":
            self.heading = True
        if tag == "script" and a.get("src"):
            self.runtime_fetch = True

    def handle_endtag(self, tag):
        if tag == "h3":
            self.heading = False
        if tag == "article":
            self.current = None

    def handle_data(self, data):
        if self.heading and self.current:
            self.current["titles"].append(data)


def validate_question_tree_html(html: str, *, mode="historical_backtest") -> dict:
    parsed = _TemplateParser(html)
    issues = []
    def fail(code, message):
        issues.append({"severity": "error", "code": code, "message": message})
    if len(parsed.ids) != len(set(parsed.ids)):
        fail("duplicate_ids", "Template IDs must be unique")
    if not parsed.nodes or "question-tree" not in parsed.ids or "detail-pane" not in parsed.ids:
        fail("missing_tree_shell", "Template needs a tree, detail pane and pre-rendered nodes")
    node_ids = {n.get("id") for n in parsed.nodes}
    tree_ids = [a.get("data-node-link") for a in parsed.links if a.get("data-node-link")]
    if len(tree_ids) != len(node_ids) or set(tree_ids) != node_ids:
        fail("tree_coverage", "Navigation must cover each node exactly once")
    roots = [n for n in parsed.nodes if not n.get("data-parent-id")]
    if len(roots) != 1:
        fail("root_coverage", "Template must have one root")
    for node in parsed.nodes:
        if node["sections"] != list(SECTIONS):
            fail("node_section_order", f"{node.get('id')} must render exactly scope/data/analysis/conclusion")
        children = [n for n in parsed.nodes if n.get("data-parent-id") == node.get("id")]
        if node["titles"] != list(PARENT_TITLES if children else LEAF_TITLES):
            fail("node_section_titles", "The four section headings are fixed, not project-specific")
        if node.get("data-kind") != ("rollup" if children else "leaf"):
            fail("node_mode", "Parent and leaf structures must match the tree")
        if children and set(node["rollups"]) != {c.get("id") for c in children}:
            fail("rollup_coverage", "Parent must show all direct children and their states")
        if children and node.get("data-passed") == "true" and any(c.get("data-passed") != "true" for c in children):
            fail("false_parent_completion", "Parent cannot pass while required children remain unpassed")
        if not children and "evidence-table" not in node["tables"]:
            fail("missing_evidence_table", "Leaf must show evidence or an explicit empty state")
    for link in parsed.links:
        url = link.get("href", "")
        if not safe_link(url):
            fail("unsafe_link", url)
        if url.startswith("#") and url[1:] not in parsed.ids:
            fail("broken_anchor", url)
    if parsed.runtime_fetch or "fetch(" in html:
        fail("runtime_evidence_fetch", "All content must be pre-rendered into a self-contained file")
    return {"ok": not issues, "issues": issues, "summary": {"mode": mode, "presentation_profile": PROFILE,
            "nodes": len(parsed.nodes), "parents": sum(n.get("data-kind") == "rollup" for n in parsed.nodes),
            "leaves": sum(n.get("data-kind") == "leaf" for n in parsed.nodes)}}
