"""Event-study presentation adapters implementing the existing canonical renderer port.

Both public surfaces consume one ReportViewModel; HTML uses the shared question-tree template.
No questions, source selection, financial analysis or conclusions originate here.
"""
from __future__ import annotations

from html import escape
import re

from value_invest_research.adapters.outbound.canonical_html_report_renderer import CanonicalHtmlReportRenderer
from value_invest_research.adapters.outbound.canonical_markdown_report_renderer import CanonicalMarkdownReportRenderer
from value_invest_research.domain.question_tree_report import LEAF_TITLES, PARENT_TITLES


def blocks(vm):
    syn = vm.project["synthesis"]
    result = []
    def add(kind, **fields):
        result.append({"kind": kind, **fields})
    tree = vm.project.get("question_tree", {}).get("nodes", [])
    if not tree:
        raise ValueError("Event Markdown requires the same question tree as HTML")
    def children(row):
        return [n for n in tree if n.get("parent_id") == row["id"]]

    def add_table(table):
        if table.get("caption"):
            add("paragraph", text=table["caption"])
        add("table", headers=table["headers"], rows=table["rows"])

    def argument(row):
        if row["what"] != row["question"]:
            add("paragraph", text=row["what"])
        main = [p for p in row["analysis"] if not p.get("supplementary", False)]
        supplements = [p for p in row["analysis"] if p.get("supplementary", False)]
        for supporting, parts in ((False, main), (True, supplements)):
            if supporting and parts:
                add("heading", level=6, text="补充测算与方法说明")
            for part in parts:
                add("heading", level=6, text=part["heading"])
                for p in part["paragraphs"]:
                    add("paragraph", text=p)
                for table in part.get("tables", []):
                    add_table(table)
            if not supporting:
                for table in row.get("tables", []):
                    add_table(table)
                if row.get("parent_bridge"):
                    add("paragraph", text="对父问题的贡献：" + row["parent_bridge"])

    def assessment(row):
        add("paragraph", text=("充分性：通过（限本题边界）。" if row["passed"] else "充分性：未通过。") + "；".join(row["reasons"]))
        if row["gaps"]:
            add("paragraph", text="缺口：" + "；".join(row["gaps"]), style="gap")
        missing = [c for c in children(row) if not c["passed"]]
        if children(row) and not row["gaps"] and not missing:
            add("paragraph", text="本题边界内暂无已记录的重大缺口。")
        for child in missing:
            add("child_gap", child=child)
        if row.get("refutation"):
            add("paragraph", text="反向证据与边界：" + row["refutation"], style="note")
        add("paragraph", text="下一步：" + "；".join(row["next_actions"]), style="note")

    def node_article(row):
        child_nodes = children(row)
        add("heading", level=min(row["level"] + 2, 4), id=row["id"], text=row["question"], qid=row["id"])
        titles = PARENT_TITLES if child_nodes else LEAF_TITLES
        add("heading", level=5, text="1. " + titles[0], module_node=row["id"])
        if child_nodes:
            for child in child_nodes:
                add("child_question", child=child)
        else:
            add("paragraph", text=row["conclusion"], style="conclusion")
        add("heading", level=5, text="2. " + titles[1], module_node=row["id"])
        if child_nodes:
            for child in child_nodes:
                add("child_finding", child=child)
            add("heading", level=6, text="综合判断")
            add("paragraph", text=row["conclusion"], style="lead")
        argument(row)
        if not child_nodes:
            assessment(row)
        add("heading", level=5, text="3. " + titles[2], module_node=row["id"])
        if child_nodes:
            assessment(row)
        else:
            add("evidence", pairs=row["evidence"])
            if not row["evidence"]:
                add("paragraph", text="尚无可展示的本题证据；不据此认定问题已经回答。")

    root = next(n for n in tree if not n.get("parent_id"))
    add("heading", level=2, id="overview", text="1. 当前研究的问题")
    node_article(root)
    add("heading", level=2, id="industry", text="2. 行业概况")
    def visit(row):
        for child in children(row):
            node_article(child)
            visit(child)
    visit(root)
    add("heading", level=2, id="targets", text="3. 标的推荐")
    add("paragraph", text=syn["target_boundary"], style="lead")
    add("table", headers=["观察对象／状态", "已验证的业务敞口", "升级判断前必须验证", "反向风险"], rows=[
        [f"{t['company']} · {t['ticker']} / no_action", t["exposure"], t["needed"], t["risk"]] for t in vm.targets])
    add("paragraph", text=syn["next_validation"], style="note")
    add("heading", level=2, id="sources", text="4. 来源索引")
    add("paragraph", text=vm.project.get("source_note") or "下列均为本轮实际打开并核读的来源。S04、S05 为评测作者原文；其他为官方资料或厂商刊载客户案例。事实、研究者推导与假设情景分别表述；来源链接会随网站更新，摘录、定位与逐题复核记录保存在项目审计文件中。", style="note")
    for s in vm.sources:
        add("source", source=s)
    return result


def link_tokens(text, sources, html=False):
    if html:
        text = escape(text)
    def substitute(match):
        sid = match.group(1)
        s = sources[sid]
        if html:
            return f'<a class="citation" href="{escape(s["url"], quote=True)}" target="_blank" rel="noopener noreferrer" title="{escape(s["title"], quote=True)}">{sid}</a>'
        return f'[{sid} · {s["title"]}]({s["url"]})'
    return re.sub(r"\[(S\d+)\]", substitute, text)


def evidence_rows(pairs, sources):
    return [[f'[{p["source"]}] · {p.get("published_at") or sources[p["source"]].get("published_at") or "未披露发布日期"}'
             + f' · {sources[p["source"]].get("material_class", "资料")} · {sources[p["source"]].get("publisher", "")}'
             + " 原文定位：" + p["locator"],
             p["fact"], p.get("effect", "boundary"), p["boundary"]] for p in pairs]


# HTML layout is owned by the shared, versioned repository template.
EventHtmlReportRenderer = CanonicalHtmlReportRenderer



class EventMarkdownReportRenderer(CanonicalMarkdownReportRenderer):
    def render(self, view_model):
        vm = view_model
        sources = {s["source_id"]: s for s in vm.sources}
        f = lambda text: link_tokens(text, sources)
        lines = ["---", "report_scope: event-study", f"project_id: {vm.project['project_id']}", "as_of_date: 2026-09-10", "run_mode: historical_backtest", "research_status: partial_research", "---", "", "# GPT-6 Astra 发布对 AI 行业的影响", ""]
        for block in blocks(vm):
            kind = block["kind"]
            if kind == "heading":
                if block.get("id"):
                    lines.extend([f'<a id="{escape(block["id"], quote=True)}"></a>', ""])
                lines.extend(["#" * block["level"] + " " + (block.get("qid", "") + " · " if block.get("qid") else "") + block["text"], ""])
            elif kind == "paragraph":
                lines.extend([f(block["text"]), ""])
            elif kind in {"child_question", "child_finding", "child_gap"}:
                c = block["child"]
                lines.extend([f'- [{c["question"]}](#{c["id"]})', ""])
                if kind == "child_question":
                    lines.extend([f(c["why_it_matters"]), ""])
                elif kind == "child_finding":
                    lines.extend([("通过 · 限本题" if c["passed"] else "未充分") + "。" + f(c["conclusion"]), ""])
                    if not c["passed"]:
                        lines.extend(["未作为已验证结论：" + f("；".join(c["gaps"])), ""])
                else:
                    lines.extend(["缺口：" + f("；".join(c["gaps"])), "", "下一步：" + f("；".join(c["next_actions"])), ""])
            elif kind in {"table", "evidence"}:
                heads = ["材料、日期与原文定位", "关键数据与事实", "作用", "口径限制与反向解释"] if kind == "evidence" else block["headers"]
                rows = evidence_rows(block["pairs"], sources) if kind == "evidence" else block["rows"]
                lines.extend(["| " + " | ".join(heads) + " |", "| " + " | ".join(["---"] * len(heads)) + " |"])
                lines.extend("| " + " | ".join(f(c).replace("|", "\\|").replace("\n", "<br>") for c in r) + " |" for r in rows)
                lines.append("")
            elif kind == "chain":
                lines.extend([" → ".join(f"{a}（{b}）" for a,b in block["items"]), ""])
            elif kind == "source":
                s = block["source"]
                lines.extend([f'[{s["source_id"]} · {s["title"]}]({s["url"]})', "", f'{s["published_at"] or "无固定发布日期；读取日 2026-09-10"}｜{s["publisher"]}｜{s["material_class"]}。{s["effective_period"]}。{s["note"]}', ""])
        return "\n".join(lines)
