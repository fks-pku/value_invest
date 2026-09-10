"""Event-study presentation adapters implementing the existing canonical renderer port.

Both public surfaces consume one ReportViewModel; HTML uses the shared question-tree template.
No questions, source selection, financial analysis or conclusions originate here.
"""
from __future__ import annotations

from html import escape
import re

from value_invest_research.adapters.outbound.canonical_html_report_renderer import CanonicalHtmlReportRenderer
from value_invest_research.adapters.outbound.canonical_markdown_report_renderer import CanonicalMarkdownReportRenderer


def blocks(vm):
    syn = vm.project["synthesis"]
    result = []
    def add(kind, **fields):
        result.append({"kind": kind, **fields})
    add("heading", level=2, id="overview", text="1. 当前研究的问题")
    add("paragraph", text=vm.goal["topic"], style="question")
    add("paragraph", text=syn["root_conclusion"], style="lead")
    for p in syn["root_paragraphs"]:
        add("paragraph", text=p)
    add("chain", items=syn["causal_chain"])
    add("paragraph", text=syn["boundary"], style="note")
    add("paragraph", text=syn["research_limit"], style="note")
    add("heading", level=2, id="industry", text="2. 行业概况")
    by_id = {r["id"]: r for r in vm.qa_roots}
    groups = {r["id"]: r for r in syn["nodes"]}
    order = ["Q1.1", "Q1.1.1", "Q1.1.2", "Q1.1.2.1", "Q1.1.2.2", "Q1.2", "Q1.2.1", "Q1.2.2", "Q1.2.2.1", "Q1.2.2.2", "Q1.2.3", "Q1.3", "Q1.3.1"]
    for qid in order:
        if qid in groups:
            row = groups[qid]
            add("heading", level=3, id=qid, text=row["title"], qid=qid, rollup=True)
            add("paragraph", text=row["conclusion"], style="lead")
            for p in row["paragraphs"]:
                add("paragraph", text=p)
            continue
        row = by_id[qid]
        add("heading", level=4, id=qid, text=row["title"], qid=qid, passed=row["passed"])
        add("paragraph", text=row["question"], style="question")
        add("paragraph", text=row["conclusion"], style="conclusion")
        add("evidence", pairs=row["evidence"])
        for part in row["analysis"]:
            add("heading", level=5, text=part["heading"])
            for p in part["paragraphs"]:
                add("paragraph", text=p)
        if row.get("scenario_table"):
            add("table", **row["scenario_table"])
        add("paragraph", text="反向证据与边界：" + row["refutation"], style="note")
        add("paragraph", text=("充分性：通过（限本题边界）。" if row["passed"] else "充分性：未通过。") + row["gate_reason"], style="gate" if row["passed"] else "gap")
        if row["gaps"]:
            add("paragraph", text="缺口：" + "；".join(row["gaps"]), style="gap")
        add("paragraph", text="下一步：" + "；".join(row["next_actions"]), style="note")
    add("heading", level=2, id="targets", text="3. 标的推荐")
    add("paragraph", text=syn["target_boundary"], style="lead")
    add("table", headers=["观察对象／状态", "已验证的业务敞口", "升级判断前必须验证", "反向风险"], rows=[
        [f"{t['company']} · {t['ticker']} / no_action", t["exposure"], t["needed"], t["risk"]] for t in vm.targets])
    add("paragraph", text=syn["next_validation"], style="note")
    add("heading", level=2, id="sources", text="4. 来源索引")
    add("paragraph", text="下列均为本轮实际打开并核读的来源。S04、S05 为评测作者原文；其他为官方资料或厂商刊载客户案例。事实、研究者推导与假设情景分别表述；来源链接会随网站更新，摘录、定位与逐题复核记录保存在项目审计文件中。", style="note")
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
    return [[f'[{p["source"]}] · {p.get("published_at") or sources[p["source"]]["published_at"] or "读取日 2026-09-10"}',
             p["fact"], p["boundary"] + " 原文定位：" + p["locator"]] for p in pairs]


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
                lines.extend(["#" * block["level"] + " " + (block.get("qid", "") + " · " if block.get("qid") else "") + block["text"], ""])
            elif kind == "paragraph":
                lines.extend([f(block["text"]), ""])
            elif kind in {"table", "evidence"}:
                heads = ["资料／日期", "关键数据与事实", "口径、限制与原文定位"] if kind == "evidence" else block["headers"]
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
