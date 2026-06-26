from __future__ import annotations

from typing import Any

from value_invest_research.adapters.outbound.report_sections.base import ReportRenderContext
from value_invest_research.adapters.outbound.report_sections.shared import _e


def render_hero(data: dict[str, Any]) -> str:
    return _render_hero(data)


class CurrentGoalSection:
    section_id = "goal"

    def render(self, context: ReportRenderContext) -> str:
        return _render_goal(context.data)


def _render_hero(data: dict[str, Any]) -> str:
    project = data["project"]
    title = project.get("title") or data["goal"].get("topic") or "专业投研报告"
    report_date = project.get("report_date") or ""
    run_mode = project.get("run_mode") or ""
    return f"""
<header class="hero">
  <nav class="top-nav" aria-label="报告导航">
    <a href="#goal">当前研究的问题</a>
    <a href="#overview">行业概况</a>
    <a href="#qa">下钻 QA</a>
    <a href="#targets">标的推荐</a>
    <a href="#sources">来源索引</a>
  </nav>
  <div class="hero-inner">
    <p class="eyebrow">Research Goal QA</p>
    <h1>{_e(str(title))}</h1>
    <p class="hero-subtitle">先判断新技术是否进入 S 曲线，再看产业空间和技术链，最后形成标的观察清单。</p>
    <div class="hero-meta">
      <span>{_e(str(report_date))}</span>
      <span>{_e(str(run_mode))}</span>
    </div>
  </div>
</header>
""".strip()


def _render_goal(data: dict[str, Any]) -> str:
    goal = data["goal"]
    constraint = _render_constraint_definition(goal.get("constraint_definition") or goal.get("key_constraint") or {})
    return f"""
<main>
<section id="goal" class="section goal-section">
  <div class="section-heading">
    <span class="section-kicker">01</span>
    <h2>当前研究的问题</h2>
  </div>
  <div class="goal-card">
    <div>
      <p class="label">研究对象</p>
      <p class="goal-main">{_e(str(goal.get("topic", "")))}</p>
    </div>
    <div>
      <p class="label">当前结论</p>
      <p>{_e(str(goal.get("current_judgment", "")))}</p>
    </div>
    <div>
      <p class="label">最大不确定性</p>
      <p>{_e(str(goal.get("biggest_uncertainty", "")))}</p>
    </div>
    <div>
      <p class="label">边界</p>
      <p>{_e(str(goal.get("decision_boundary", "")))}</p>
    </div>
    {constraint}
  </div>
</section>
""".strip()


def _render_constraint_definition(item: dict[str, Any]) -> str:
    if not isinstance(item, dict) or not item:
        item = {
            "theme": "先把研究主题翻译成精确定义的约束，再判断哪些公司能把约束转成财务价值。",
            "precise_constraint": "待补充：核心瓶颈、边界、替代路线和验证周期。",
            "why_now": "待补充：为什么现在进入投资观察窗口。",
            "scope": "待补充：研究范围和不纳入范围。",
            "route_conflict": "待补充：关键技术路线、商业路线或竞争路线冲突。",
            "adoption_horizon": "待补充：验证周期和降级节奏。",
        }
    rows = [
        ("主题边界", item.get("theme", "")),
        ("精确定义", item.get("precise_constraint") or item.get("preciseConstraint") or item.get("constraint", "")),
        ("为什么现在", item.get("why_now") or item.get("whyNow") or ""),
        ("研究范围", item.get("scope", "")),
        ("路线冲突", item.get("route_conflict") or item.get("routeConflict") or ""),
        ("验证周期", item.get("adoption_horizon") or item.get("adoptionHorizon") or ""),
    ]
    cards = "\n".join(
        f"<article><span>{_e(label)}</span><p>{_e(str(value))}</p></article>" for label, value in rows
    )
    return f"""
    <div class="constraint-definition">
      <p class="artifact-title">关键约束定义</p>
      <div class="constraint-grid">{cards}</div>
    </div>
""".strip()
