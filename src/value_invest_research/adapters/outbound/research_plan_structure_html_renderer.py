from __future__ import annotations

from html import escape
from typing import Any, Iterable

from value_invest_research.domain.research_plan import (
    validate_research_plan_execution,
)


STATUS_LABELS = {
    "pending": "待研究",
    "in_progress": "研究中",
    "review_pending": "待复核",
    "blocked": "证据不足",
    "completed": "已回答",
}


class ResearchPlanStructureHtmlRenderer:
    """Render a concise, reader-safe view of the current research scope."""

    def render(
        self,
        *,
        project: dict[str, Any],
        bundle: dict[str, Any],
    ) -> str:
        active_lens_ids = _active_lens_ids(project)
        plans = [
            row
            for row in bundle.get("plans") or []
            if isinstance(row, dict)
            and (
                not active_lens_ids
                or str(row.get("lens_id") or "") in active_lens_ids
            )
        ]
        events_by_node = dict(bundle.get("events_by_node") or {})
        plan_views = [
            _plan_view(
                plan,
                list(events_by_node.get(str(plan.get("l3_node_id") or ""), [])),
            )
            for plan in plans
        ]
        current_questions = [
            leaf
            for view in plan_views
            for leaf in view["leaves"]
            if leaf["status"] != "completed"
        ]
        next_question_id = (
            str(current_questions[0]["question_id"])
            if current_questions
            else ""
        )
        attempted = sum(bool(view["events"]) for view in plan_views)
        source_ids = {
            str(source_id)
            for view in plan_views
            for event in view["events"]
            for source_id in event.get("source_ids") or []
            if str(source_id).strip()
        }
        expanded = sum(bool(view["root"].get("children")) for view in plan_views)
        title = str(project.get("title") or "GPU / ASIC BOM 研究")
        as_of_date = str(project.get("as_of_date") or project.get("report_date") or "")
        cards = "\n".join(
            _render_plan_card(view, position, next_question_id=next_question_id)
            for position, view in enumerate(plan_views, start=1)
        )
        chain = _render_chain(plan_views)
        next_question = current_questions[0] if current_questions else {}
        paused = list(
            (project.get("active_research_scope") or {}).get("paused_lens_ids")
            or []
        )
        scope_reason = str(
            (project.get("active_research_scope") or {}).get("reason") or ""
        )

        return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} · 需求侧研究结构</title>
  <style>{_css()}</style>
</head>
<body data-view="research-plan-structure" data-active-lenses="{escape(','.join(active_lens_ids))}">
  <header class="hero">
    <div class="eyebrow">GPU / ASIC · DYNAMIC RESEARCH MAP</div>
    <div class="hero-grid">
      <div>
        <p class="section-no">01 / 当前范围</p>
        <h1>先把需求<br><em>研究清楚</em></h1>
        <p class="deck">从 L3 直接搜集和分析。能回答就停止；证据不足，才沿着具体缺口向下一层生长。</p>
      </div>
      <aside class="scope-note">
        <span class="scope-dot" aria-hidden="true"></span>
        <div>
          <strong>当前只执行：需求侧</strong>
          <p>{escape(scope_reason or '其它研究视角暂缓，不进入当前执行。')}</p>
          <small>暂停视角 {len(paused)} 个 · 底层历史保留</small>
        </div>
      </aside>
    </div>
    <div class="metrics" aria-label="研究进度">
      <div><strong>{len(plan_views)}</strong><span>需求侧 L3</span></div>
      <div><strong>{attempted}</strong><span>已启动 L3</span></div>
      <div><strong>{expanded}</strong><span>动态下钻分支</span></div>
      <div><strong>{len(source_ids)}</strong><span>已挂接官方来源</span></div>
      <div><strong>{len(current_questions)}</strong><span>当前终端问题</span></div>
      <div><strong>{escape(as_of_date)}</strong><span>研究截面</span></div>
    </div>
  </header>

  <main>
    <section class="logic-section">
      <div class="section-heading">
        <div><p class="section-no">02 / 问题层级</p><h2>研究结构</h2></div>
        <p>Q1、Q2 是证据视图；真正的需求主链从工作负载开始，一直追到收入和现金流。</p>
      </div>
      <div class="levels">
        <div class="level-row"><span>L1</span><strong>GPU / ASIC 的需求增长是否真实、持续，并最终实现商业兑现？</strong></div>
        <div class="level-row accent"><span>L2</span><strong>需求侧：工作负载如何转化为算力、预算、订单与利润？</strong></div>
      </div>
      {chain}
    </section>

    <section class="status-section">
      <div class="section-heading">
        <div><p class="section-no">03 / 已发生的研究</p><h2>Q1 已跑过一轮</h2></div>
        <p>不是空计划：第一轮读取了 4 份官方申报材料；答案仍不足，因此按证据缺口生成了 3 个 L4。</p>
      </div>
      <div class="runline" aria-label="第一轮研究过程">
        <span class="done">L3 搜集</span><i></i>
        <span class="done">4 份官方材料</span><i></i>
        <span class="warn">证据门未通过</span><i></i>
        <span class="done">生成 3 个 L4</span><i></i>
        <span class="active">下一步逐题搜集</span>
      </div>
      <div class="next-action">
        <span>NEXT</span>
        <div>
          <small>下一条唯一执行问题</small>
          <strong>{escape(str(next_question.get('question') or '当前需求侧问题已完成'))}</strong>
        </div>
      </div>
    </section>

    <section class="tree-section">
      <div class="section-heading compact">
        <div><p class="section-no">04 / L3 研究队列</p><h2>逐项展开查看</h2></div>
        <div class="controls"><button type="button" data-action="open">全部展开</button><button type="button" data-action="close">全部收起</button></div>
      </div>
      <div class="tree">{cards}</div>
    </section>
  </main>

  <footer>
    <p>当前页面只展示需求侧执行结构。材料必须从当前最深问题发起；不得用宽泛材料池批量完成多个问题。</p>
    <span>Research structure · {escape(as_of_date)}</span>
  </footer>
  <script>{_script()}</script>
</body>
</html>
"""


def _active_lens_ids(project: dict[str, Any]) -> list[str]:
    scope = project.get("active_research_scope") or {}
    return [
        str(item).strip()
        for item in scope.get("lens_ids") or []
        if str(item).strip()
    ]


def _plan_view(plan: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    execution = validate_research_plan_execution(plan, events)
    statuses = {
        str(row.get("step_id") or ""): str(row.get("status") or "pending")
        for row in execution.get("step_states") or []
    }
    root = dict(plan.get("question_tree") or {})
    leaves = []
    for leaf in _terminal_nodes(root):
        question_id = str(leaf.get("question_id") or "")
        leaves.append(
            {
                **leaf,
                "status": statuses.get(f"question:{question_id}", "pending"),
            }
        )
    latest_answer = next(
        (
            str(event.get("answer") or "")
            for event in reversed(events)
            if str(event.get("answer") or "").strip()
        ),
        "",
    )
    latest_gaps = next(
        (
            list(event.get("gaps") or [])
            for event in reversed(events)
            if event.get("gaps")
        ),
        [],
    )
    return {
        "plan": plan,
        "root": root,
        "leaves": leaves,
        "events": events,
        "execution": execution,
        "latest_answer": latest_answer,
        "latest_gaps": latest_gaps,
    }


def _terminal_nodes(node: dict[str, Any]) -> Iterable[dict[str, Any]]:
    children = [row for row in node.get("children") or [] if isinstance(row, dict)]
    if not children:
        yield node
        return
    for child in children:
        yield from _terminal_nodes(child)


def _render_chain(plan_views: list[dict[str, Any]]) -> str:
    evidence_views = plan_views[:2]
    backbone = plan_views[2:]
    evidence = "".join(
        f'<span><b>D{index}</b>{escape(str(view["plan"].get("l3_title") or ""))}</span>'
        for index, view in enumerate(evidence_views, start=1)
    )
    causal = "<i aria-hidden=\"true\">→</i>".join(
        f'<span><b>D{index + 2}</b>{escape(str(view["plan"].get("l3_title") or ""))}</span>'
        for index, view in enumerate(backbone)
    )
    return f"""
      <div class="chain-board">
        <div class="chain-label">派生证据视图</div>
        <div class="evidence-chain">{evidence}</div>
        <div class="chain-label">第一性原理主链</div>
        <div class="causal-chain">{causal}</div>
      </div>"""


def _render_plan_card(
    view: dict[str, Any],
    position: int,
    *,
    next_question_id: str,
) -> str:
    plan = view["plan"]
    root = view["root"]
    leaves = view["leaves"]
    has_events = bool(view["events"])
    expanded = bool(root.get("children"))
    state = "in_progress" if expanded else "pending"
    if not expanded and view["execution"].get("summary", {}).get("status") == "completed":
        state = "completed"
    state_label = "已研究 · 动态下钻" if expanded else STATUS_LABELS.get(state, state)
    answer_block = ""
    if view["latest_answer"]:
        gaps = "".join(
            f"<li>{escape(str(gap))}</li>" for gap in view["latest_gaps"]
        )
        answer_block = f"""
        <div class="attempt">
          <div><span>第一轮答案</span><p>{escape(view['latest_answer'])}</p></div>
          <div><span>未通过的原因</span><ul>{gaps}</ul></div>
        </div>"""
    leaf_cards = "".join(
        _render_leaf(leaf, next_question_id=next_question_id)
        for leaf in leaves
    )
    open_attribute = " open" if position == 1 else ""
    return f"""
        <details class="l3-card"{open_attribute}>
          <summary>
            <span class="node-index">D{position}</span>
            <span class="summary-copy"><small>L3 · {escape(str(plan.get('l3_title') or ''))}</small><strong>{escape(str(plan.get('l3_question') or ''))}</strong></span>
            <span class="state state-{escape(state)}">{escape(state_label)}</span>
            <span class="chevron" aria-hidden="true">＋</span>
          </summary>
          <div class="l3-body">
            {answer_block}
            <div class="leaf-grid">{leaf_cards}</div>
            <p class="stop-rule">分支停止条件：当前最深问题证据门通过；否则只按已记录缺口继续下钻，最多到 L5。</p>
          </div>
        </details>"""


def _render_leaf(leaf: dict[str, Any], *, next_question_id: str) -> str:
    question_id = str(leaf.get("question_id") or "")
    level = int(leaf.get("level") or 3)
    status = str(leaf.get("status") or "pending")
    is_next = question_id == next_question_id
    data = "".join(
        f"<li>{escape(str(item))}</li>" for item in leaf.get("required_data") or []
    )
    analysis = "".join(
        f"<li>{escape(str(item))}</li>" for item in leaf.get("analysis_plan") or []
    )
    return f"""
      <article class="leaf{' next' if is_next else ''}" data-question-id="{escape(question_id)}">
        <div class="leaf-top"><span>L{level}</span><small>{'下一步' if is_next else escape(STATUS_LABELS.get(status, status))}</small></div>
        <h3>{escape(str(leaf.get('title') or '当前问题'))}</h3>
        <p class="leaf-question">{escape(str(leaf.get('question') or ''))}</p>
        <div class="leaf-work"><div><b>搜集什么</b><ul>{data}</ul></div><div><b>怎么分析</b><ul>{analysis}</ul></div></div>
      </article>"""


def _css() -> str:
    return """
:root{--ink:#18252d;--muted:#667176;--paper:#f3f0e8;--card:#fbfaf5;--line:#c9c4b6;--blue:#123f5a;--blue2:#0d6a7a;--red:#c94f36;--yellow:#e7bd62;--shadow:0 24px 70px rgba(25,37,45,.10)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:var(--paper);font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;line-height:1.65;background-image:linear-gradient(rgba(24,37,45,.035) 1px,transparent 1px);background-size:100% 32px}
.hero{background:var(--blue);color:#f8f1df;padding:44px max(5vw,32px) 0;position:relative;overflow:hidden}.hero:after{content:"DEMAND";position:absolute;right:-18px;top:-68px;font:800 170px/1 Georgia,serif;letter-spacing:-10px;color:rgba(255,255,255,.035);pointer-events:none}.eyebrow,.section-no{margin:0 0 18px;font-size:11px;letter-spacing:.19em;text-transform:uppercase;font-weight:700}.eyebrow{color:#9ed4d7}.hero-grid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(280px,.65fr);gap:60px;align-items:end;max-width:1240px;margin:auto}.hero h1{font:700 clamp(48px,7vw,92px)/.96 "Songti SC","STSong",Georgia,serif;letter-spacing:-.05em;margin:0}.hero h1 em{color:var(--yellow);font-style:normal}.deck{max-width:690px;color:#c8d6d6;font-size:17px;margin:28px 0 0}.scope-note{display:flex;gap:15px;border-top:1px solid rgba(255,255,255,.3);padding:22px 0 4px}.scope-note strong{font-size:18px}.scope-note p{color:#c8d6d6;margin:6px 0}.scope-note small{color:#8fb2b6}.scope-dot{width:10px;height:10px;border-radius:50%;background:var(--yellow);box-shadow:0 0 0 6px rgba(231,189,98,.14);margin-top:7px;flex:none}.metrics{max-width:1240px;margin:42px auto 0;border-top:1px solid rgba(255,255,255,.18);display:grid;grid-template-columns:repeat(6,1fr)}.metrics div{padding:23px 16px;border-right:1px solid rgba(255,255,255,.12)}.metrics div:first-child{padding-left:0}.metrics div:last-child{border:0}.metrics strong{display:block;font:600 25px/1.1 Georgia,"Songti SC",serif}.metrics span{display:block;color:#91b4b8;font-size:11px;margin-top:7px;letter-spacing:.05em}
main{max-width:1240px;margin:auto;padding:70px max(3vw,24px) 90px}.section-heading{display:grid;grid-template-columns:1fr minmax(280px,520px);align-items:end;gap:50px;margin-bottom:30px}.section-heading h2{font:700 38px/1.1 "Songti SC","STSong",serif;margin:0}.section-heading>p{margin:0;color:var(--muted)}.section-heading.compact{margin-top:80px}.levels{border-top:2px solid var(--ink);margin-bottom:28px}.level-row{display:grid;grid-template-columns:78px 1fr;gap:20px;padding:18px 0;border-bottom:1px solid var(--line)}.level-row span{font:700 13px Georgia,serif;color:var(--red)}.level-row.accent strong{color:var(--blue2)}.chain-board{background:var(--card);border:1px solid var(--line);box-shadow:var(--shadow);padding:26px;margin-top:26px}.chain-label{font-size:10px;letter-spacing:.16em;color:var(--muted);text-transform:uppercase;margin:4px 0 12px}.evidence-chain,.causal-chain{display:flex;align-items:stretch;gap:10px;overflow:auto;padding-bottom:6px}.evidence-chain{margin-bottom:22px}.evidence-chain span,.causal-chain span{min-width:170px;flex:1;border:1px solid var(--line);background:#fff;padding:17px 16px;font-weight:650}.evidence-chain span{border-left:4px solid var(--yellow)}.causal-chain span{border-left:4px solid var(--blue2)}.evidence-chain b,.causal-chain b{display:block;color:var(--muted);font:700 11px Georgia,serif;margin-bottom:6px}.causal-chain i{align-self:center;font-style:normal;color:var(--red);font-size:20px}
.status-section{margin-top:80px}.runline{display:flex;align-items:center;background:var(--ink);color:#fff;padding:22px;overflow:auto}.runline span{white-space:nowrap;font-size:12px;border:1px solid rgba(255,255,255,.2);padding:9px 13px}.runline i{width:28px;height:1px;background:rgba(255,255,255,.28);flex:none}.runline .done{color:#a8d8cd}.runline .warn{color:#ffd081}.runline .active{background:var(--red);border-color:var(--red)}.next-action{display:grid;grid-template-columns:86px 1fr;background:var(--yellow);padding:24px 28px;gap:20px}.next-action>span{font:700 12px Georgia,serif;letter-spacing:.15em}.next-action small{display:block;color:#725b2a}.next-action strong{display:block;margin-top:5px;font-family:"Songti SC","STSong",serif;font-size:20px}.controls{display:flex;gap:8px;justify-content:flex-end}.controls button{border:1px solid var(--ink);background:transparent;color:var(--ink);padding:8px 13px;cursor:pointer;font:inherit;font-size:12px}.controls button:hover{background:var(--ink);color:#fff}
.tree{border-top:2px solid var(--ink)}.l3-card{background:var(--card);border-bottom:1px solid var(--line)}.l3-card summary{list-style:none;display:grid;grid-template-columns:64px 1fr auto 34px;gap:18px;align-items:center;padding:23px 18px;cursor:pointer}.l3-card summary::-webkit-details-marker{display:none}.node-index{font:700 18px Georgia,serif;color:var(--red)}.summary-copy small{display:block;color:var(--muted);margin-bottom:4px}.summary-copy strong{font-family:"Songti SC","STSong",serif;font-size:18px}.state{font-size:11px;border-radius:999px;padding:6px 10px;background:#e5e2d9;color:var(--muted)}.state-in_progress{background:#d8ece7;color:#175c51}.state-completed{background:#d8ece7;color:#175c51}.chevron{font-size:22px;color:var(--muted);transition:transform .2s}.l3-card[open] .chevron{transform:rotate(45deg)}.l3-body{border-top:1px dashed var(--line);padding:24px 28px 30px}.attempt{display:grid;grid-template-columns:1.25fr .75fr;gap:26px;background:#eef0eb;border-left:4px solid var(--red);padding:22px;margin-bottom:22px}.attempt span{font-size:11px;letter-spacing:.12em;color:var(--red);font-weight:700}.attempt p,.attempt ul{margin:8px 0 0;color:#3e4a50;font-size:13px}.leaf-grid{display:grid;gap:12px}.leaf{border:1px solid var(--line);background:#fff;padding:20px}.leaf.next{border:2px solid var(--red);box-shadow:0 12px 30px rgba(201,79,54,.12)}.leaf-top{display:flex;justify-content:space-between}.leaf-top span{font:700 12px Georgia,serif;color:var(--red)}.leaf-top small{color:var(--muted)}.leaf.next .leaf-top small{color:var(--red);font-weight:700}.leaf h3{font:700 19px "Songti SC","STSong",serif;margin:12px 0 5px}.leaf-question{margin:0;color:#34434a}.leaf-work{display:grid;grid-template-columns:1fr 1fr;gap:28px;border-top:1px dashed var(--line);margin-top:17px;padding-top:16px}.leaf-work b{font-size:12px;color:var(--blue2)}.leaf-work ul{margin:7px 0 0;padding-left:18px;color:var(--muted);font-size:12px}.stop-rule{margin:18px 0 0;color:var(--muted);font-size:11px}.section-no{color:var(--red);margin-bottom:8px}
footer{border-top:1px solid var(--line);padding:28px max(5vw,32px);display:flex;justify-content:space-between;gap:30px;color:var(--muted);font-size:11px}footer p{margin:0}footer span{white-space:nowrap}
@media(max-width:850px){.hero-grid,.section-heading,.attempt{grid-template-columns:1fr}.metrics{grid-template-columns:repeat(3,1fr)}.metrics div:first-child{padding-left:16px}.hero{padding-left:24px;padding-right:24px}.l3-card summary{grid-template-columns:48px 1fr 28px}.state{grid-column:2}.chevron{grid-column:3;grid-row:1}.leaf-work{grid-template-columns:1fr}.section-heading{gap:16px}.controls{justify-content:flex-start}.section-heading.compact{align-items:start}.causal-chain i{transform:rotate(90deg)}.causal-chain{flex-direction:column}.causal-chain span{width:100%}footer{flex-direction:column}}
@media(max-width:520px){.metrics{grid-template-columns:repeat(2,1fr)}.hero h1{font-size:48px}.scope-note{margin-top:20px}.next-action{grid-template-columns:1fr}.l3-body{padding:18px 14px}.state{display:none}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.chevron{transition:none}}
"""


def _script() -> str:
    return """
document.querySelector('[data-action="open"]').addEventListener('click',()=>document.querySelectorAll('.l3-card').forEach(item=>item.open=true));
document.querySelector('[data-action="close"]').addEventListener('click',()=>document.querySelectorAll('.l3-card').forEach(item=>item.open=false));
"""
