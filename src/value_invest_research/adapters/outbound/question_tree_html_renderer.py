"""Shared AI-factory-style template. This adapter renders; it never researches or scores."""
from __future__ import annotations

from html import escape
from pathlib import Path
import re
from string import Template

from value_invest_research.domain.question_tree_report import (
    LEAF_TITLES, PARENT_TITLES, LEAF_SECTIONS, PARENT_SECTIONS, validate_question_tree_report,
)

ASSETS = Path(__file__).parent / "report_templates"
EFFECTS = {"support": "支持", "refute": "反证", "boundary": "边界", "constraint": "约束", "unresolved": "待验证", "conflict": "冲突", "neutral": "背景", "new_branch": "新分支"}
MATERIALS = {"official_company": "公司披露", "official_filing": "官方财报", "authoritative_third_party": "权威第三方", "sell_side_research": "机构研报", "market_news": "市场消息", "expert_opinion": "专家观点"}


class QuestionTreeHtmlRenderer:
    def render(self, view_model) -> str:
        report = view_model.project["question_tree"]
        errors = validate_question_tree_report(report)
        if errors:
            raise ValueError("Invalid question-tree report: " + "; ".join(errors))
        nodes = {n["id"]: n for n in report["nodes"]}
        sources = {s["source_id"]: s for s in report["sources"]}
        root = next(n for n in nodes.values() if not n.get("parent_id"))

        def children(node):
            return [n for n in nodes.values() if n.get("parent_id") == node["id"]]

        def link(source_id, label=None):
            source = sources[source_id]
            url = source["url"]
            external = ' target="_blank" rel="noopener noreferrer"' if url.startswith(("https://", "http://")) else ""
            return f'<a href="{escape(url, quote=True)}"{external}>{escape(label or source_id)}</a>'

        def text(value):
            escaped = escape(str(value))
            return re.sub(r"\[([A-Za-z0-9_.-]+)\]", lambda m: f'<cite class="inline-cite">{link(m[1])}</cite>' if m[1] in sources else m[0], escaped)

        def paragraphs(items):
            return ''.join(f'<p>{text(p)}</p>' for p in items)

        def status(node):
            return "通过 · 限本题" if node["passed"] else "未充分"

        def tree(branch):
            return '<ul class="tree-list">' + ''.join(
                f'<li><a class="tree-item" href="#{n["id"]}" data-node-link="{n["id"]}">'
                f'<span class="tree-level">L{n["level"]}</span><span class="tree-question">{text(n.get("short") or n["question"])}'
                f'{" ↳" if n.get("was_expanded") else ""}</span><span class="tree-status{"" if n["passed"] else " waiting"}" aria-label="{status(n)}"></span></a>'
                + (tree(children(n)) if children(n) else '') + '</li>' for n in branch) + '</ul>'

        def table(headers, rows, cls, caption=""):
            return '<div class="table-scroll" role="region" tabindex="0" aria-label="横向滚动数据表"><table class="' + cls + '">' + (f'<caption>{text(caption)}</caption>' if caption else '') + '<thead><tr>' + ''.join(f'<th scope="col">{text(h)}</th>' for h in headers) + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'

        def evidence(node):
            if node["mode"] == "rollup":
                rows = []
                for child in children(node):
                    gap = f'<span class="child-gap">未作为已验证结论：{text("；".join(child["gaps"]))}</span>' if not child["passed"] else ''
                    rows.append(f'<div data-child-summary="{child["id"]}"><dt><a href="#{child["id"]}">{text(child["question"])}</a><small>{status(child)}</small></dt><dd>{text(child["conclusion"])}{gap}</dd></div>')
                return '<dl class="child-findings">' + ''.join(rows) + '</dl>'
            rows = []
            for item in node.get("evidence", []):
                source = sources[item["source"]]
                date = item.get("published_at") or source.get("published_at") or "未披露发布日期"
                rows.append('<tr><td>' + f'<span class="source-date">{text(date)}</span><span class="source-title">{link(item["source"], source["title"])}</span><span class="source-meta">{text(MATERIALS.get(source.get("material_class"), source.get("material_class", "资料")))} · {text(source.get("publisher", ""))}</span><span class="locator">定位：{text(item["locator"])}</span>' + '</td><td>' + text(item["fact"]) + '</td><td><span class="effect ' + escape(item.get("effect", "boundary"), quote=True) + '">' + text(EFFECTS.get(item.get("effect"), "边界")) + '</span></td><td>' + text(item["boundary"]) + '</td></tr>')
            if not rows:
                rows = ['<tr><td colspan="4">尚无可展示的本题证据；不据此认定问题已经回答。</td></tr>']
            return table(["材料与原文定位", "抽取的关键数据 / 事实", "作用", "口径限制与反向解释"], rows, "evidence-table", f'{node["id"]} · 逐问题证据')

        def article(node):
            nid = node["id"]
            child_nodes = children(node)
            titles = PARENT_TITLES if child_nodes else LEAF_TITLES
            parts = PARENT_SECTIONS if child_nodes else LEAF_SECTIONS
            path = [node]
            while path[0].get("parent_id"):
                path.insert(0, nodes[path[0]["parent_id"]])
            crumb = '<p class="breadcrumb">' + ''.join(f'<a href="#{n["id"]}">L{n["level"]} · {text(n.get("short") or n["question"])}</a>' for n in path) + '</p>'
            child_links = '<ol class="research-questions">' + ''.join(
                f'<li data-child-id="{n["id"]}"><a href="#{n["id"]}">{text(n["question"])}</a><p data-child-purpose="{n["id"]}">{text(n["why_it_matters"])}</p></li>' for n in child_nodes) + '</ol>'
            viewpoint = f'<div class="article-copy"><p class="answer">{text(node["conclusion"])}</p></div>'
            analysis = '<div class="article-copy">'
            if child_nodes:
                analysis += evidence(node) + '<h4>综合判断</h4>' + f'<p class="answer">{text(node["conclusion"])}</p>'
            analysis += paragraphs([node["what"]]) if node["what"] != node["question"] else ''
            supplements = []
            for section in node["analysis"]:
                content = f'<h4>{text(section["heading"])}</h4>' + paragraphs(section["paragraphs"])
                for t in section.get("tables", []):
                    rows = ['<tr>' + ''.join(f'<td>{text(c)}</td>' for c in row) + '</tr>' for row in t["rows"]]
                    content += table(t["headers"], rows, "analysis-table", t.get("caption", ""))
                if section.get("supplementary", False):
                    supplements.append(content)
                else:
                    analysis += content
            for t in node.get("tables", []):
                rows = ['<tr>' + ''.join(f'<td>{text(c)}</td>' for c in row) + '</tr>' for row in t["rows"]]
                analysis += table(t["headers"], rows, "analysis-table", t.get("caption", ""))
            if node.get("parent_bridge"):
                analysis += '<p class="parent-bridge">对父问题的贡献：' + text(node["parent_bridge"]) + '</p>'
            if supplements:
                analysis += '<details class="supplementary-analysis"><summary>补充测算与方法说明</summary>' + ''.join(supplements) + '</details>'
            conclusion = '<div class="node-assessment">' + paragraphs([("充分性：通过（限本题边界）。" if node["passed"] else "充分性：未通过。") + "；".join(node["reasons"])])
            if node.get("gaps"):
                conclusion += '<p class="gap-note">缺口：' + text("；".join(node["gaps"])) + '</p>'
            if child_nodes:
                missing_children = [c for c in child_nodes if not c["passed"]]
                if not node.get("gaps") and not missing_children:
                    conclusion += paragraphs(["本题边界内暂无已记录的重大缺口。"])
                for child in missing_children:
                    conclusion += f'<div class="child-gap" data-child-gap="{child["id"]}"><a href="#{child["id"]}">{text(child["question"])}</a>'
                    conclusion += paragraphs(["缺口：" + "；".join(child["gaps"]), "下一步：" + "；".join(child["next_actions"])]) + '</div>'
            if node.get("refutation"):
                conclusion += '<p class="boundary-note">反向证据与边界：' + text(node["refutation"]) + '</p>'
            conclusion += paragraphs(["下一步：" + "；".join(node["next_actions"])]) + '</div>'
            if child_nodes:
                sections = [child_links, analysis + '</div>', '<div class="article-copy">' + conclusion + '</div>']
            else:
                sections = [viewpoint, analysis + conclusion + '</div>', '<div class="article-copy">' + evidence(node) + '</div>']
            # Keep old section bookmarks valid without restoring old visible panels.
            aliases = f'<span id="scope-{nid}" class="anchor-alias"></span>'
            if child_nodes:
                # Existing data/conclusion bookmarks point into the corresponding modules.
                sections[1] = f'<span id="data-{nid}" class="anchor-alias"></span>' + sections[1]
                sections[2] = f'<span id="conclusion-{nid}" class="anchor-alias"></span>' + sections[2]
            body = ''.join(f'<section class="chapter-section" id="{part}-{nid}" data-section="{part}"><div class="section-heading"><span class="section-number">{i:02d}</span><h3>{text(title)}</h3></div>{content}</section>' for i, (part, title, content) in enumerate(zip(parts, titles, sections), 1))
            return f'<article class="node-detail" id="{nid}" data-kind="{node["mode"]}" data-level="{node["level"]}" data-parent-id="{node.get("parent_id") or ""}" data-passed="{str(node["passed"]).lower()}">{crumb}<div class="detail-title-row"><div><p class="node-id">{nid}</p><h2 class="detail-title">{text(node["question"])}</h2></div><span class="status-badge{"" if node["passed"] else " waiting"}">{status(node)}</span></div>{aliases}{body}</article>'

        ordered = []
        def visit(node):
            ordered.append(article(node))
            for child in children(node):
                visit(child)
        visit(root)
        source_html = paragraphs([report.get("source_note", "来源按项目登记；引用保留逐题原文定位。")])
        for sid, source in sources.items():
            source_html += f'<div class="source-entry" id="source-{escape(sid, quote=True)}">{link(sid, sid + " · " + source["title"])}' + paragraphs([f'{source.get("published_at") or "无固定发布日期"}｜{source.get("publisher", "")}｜{source.get("material_class", "")}。{source.get("effective_period", "")}。{source.get("note", "")}']) + '</div>'
        return Template((ASSETS / "question_tree_v1.html").read_text()).substitute(
            title=escape(report["title"]), root_id=root["id"],
            subtitle=text(report.get("subtitle", "左侧选择问题；非叶子查看子问题、核心结论与欠缺方向，叶子查看核心观点、关键论证与数据列表。")),
            css=(ASSETS / "question_tree_v1.css").read_text(), javascript=(ASSETS / "question_tree_v1.js").read_text(),
            metadata=''.join(f'<span>{text(s)}</span>' for s in ["AS OF " + report.get("as_of_date", ""), f'{len(nodes)} NODES · {len(sources)} SOURCES', report.get("status_label", "")]),
            tree=tree([root]), articles='\n'.join(ordered), sources=source_html, source_count=len(sources),
            attachments=''.join(f'<a href="{escape(a["href"], quote=True)}">{text(a["label"])}</a>' for a in report.get("attachments", [])))
