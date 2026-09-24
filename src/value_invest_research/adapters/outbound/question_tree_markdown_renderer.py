"""Portable audit view of the exact shared question-tree article data."""
import re
from html import escape

from value_invest_research.domain.question_tree_report import LEAF_TITLES, PARENT_TITLES, validate_question_tree_report


class QuestionTreeMarkdownRenderer:
    def render(self, vm):
        tree = vm.project["question_tree"]
        errors = validate_question_tree_report(tree)
        if errors:
            raise ValueError(errors)
        sources = {s["source_id"]: s for s in tree["sources"]}
        lines = ["---", "report_scope: research-project", f"project_id: {vm.project.get('project_id', '')}",
                 f"run_mode: {vm.project.get('run_mode', 'historical_backtest')}",
                 f"as_of_date: {tree.get('as_of_date', '')}", "---", "", f"# {tree['title']}", ""]

        def text(value):
            def link(m):
                s = sources.get(m[1])
                return f"[{m[1]} · {s['title']}]({s['url']})" if s else m[0]
            return re.sub(r"\[([A-Za-z0-9_.-]+)\]", link, str(value))

        def p(value):
            lines.extend([text(value), ""])

        def table(headers, rows, caption=""):
            if caption:
                p(caption)
            clean = lambda v: text(v).replace("|", "\\|").replace("\n", "<br>")
            lines.extend(["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"])
            lines.extend("| " + " | ".join(clean(v) for v in row) + " |" for row in rows)
            lines.append("")

        def article(node):
            children = [n for n in tree["nodes"] if n.get("parent_id") == node["id"]]
            titles = PARENT_TITLES if children else LEAF_TITLES
            p(f'<a id="{escape(node["id"], quote=True)}"></a>')
            p(f"### {node['id']} · {node['question']}")
            p("#### 1. " + titles[0])
            if children:
                for child in children:
                    p(f"- [{child['question']}](#{child['id']})")
                    p(child["why_it_matters"])
            else:
                p(node["conclusion"])
            p("#### 2. " + titles[1])
            if children:
                for child in children:
                    p(f"- [{child['question']}](#{child['id']})：{child['conclusion']}")
                    p(("通过 · 限本题" if child["passed"] else "未充分") + "；" + "；".join(child["gaps"]))
                p("综合判断：" + node["conclusion"])
            if node["what"] != node["question"]:
                p(node["what"])
            for supplementary in (False, True):
                parts = [a for a in node["analysis"] if a.get("supplementary", False) == supplementary]
                if supplementary and parts:
                    p("##### 补充测算与方法说明")
                for part in parts:
                    p("##### " + part["heading"])
                    for paragraph in part["paragraphs"]:
                        p(paragraph)
                    for t in part.get("tables", []):
                        table(t["headers"], t["rows"], t.get("caption", ""))
                if not supplementary:
                    for t in node.get("tables", []):
                        table(t["headers"], t["rows"], t.get("caption", ""))
                    if node.get("parent_bridge"):
                        p("对父问题的贡献：" + node["parent_bridge"])
            if children:
                p("#### 3. " + titles[2])
            p(("充分性：通过（限本题）。" if node["passed"] else "充分性：未通过。") + "；".join(node["reasons"]))
            p("缺口：" + ("；".join(node["gaps"]) or "本题边界内暂无已记录的重大缺口。"))
            for child in children:
                if not child["passed"]:
                    p(f"- [{child['question']}](#{child['id']})：" + "；".join(child["gaps"] + child["next_actions"]))
            if node.get("refutation"):
                p("反向证据与边界：" + node["refutation"])
            p("下一步：" + "；".join(node["next_actions"]))
            if not children:
                p("#### 3. " + titles[2])
                table(["材料、日期与原文定位", "关键数据与事实", "作用", "口径限制与反向解释"],
                      [[f"[{e['source']}] · {e.get('published_at') or sources[e['source']].get('published_at', '')} · {e['locator']}",
                        e["fact"], e.get("effect", "boundary"), e["boundary"]] for e in node.get("evidence", [])])
                if not node.get("evidence"):
                    p("尚无可展示的本题证据；不据此认定问题已经回答。")
            for child in children:
                article(child)

        root = next(n for n in tree["nodes"] if not n.get("parent_id"))
        p("## 1. 当前研究的问题")
        p(root["question"])
        p(tree.get("subtitle", ""))
        p("## 2. 行业概况")
        article(root)
        p("## 3. 标的推荐")
        p("投资判断及其边界以问题树对应公司章节为准；研究回答充分不等于投资门禁通过。")
        p("## 4. 来源索引")
        for sid, source in sources.items():
            p(f"[{sid}] · {source.get('published_at', '')} · {source.get('material_class', '')}")
        return "\n".join(lines)
