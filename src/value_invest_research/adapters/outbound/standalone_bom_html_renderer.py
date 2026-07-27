from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any


MATERIAL_LABELS = {
    "official_filing": "官方财报",
    "official_company": "官方公司",
    "sell_side_research": "研报",
    "authoritative_third_party": "第三方权威",
    "market_news": "市场消息",
    "expert_opinion": "专家观点",
    "other": "其他",
}


class StandaloneBomHtmlRenderer:
    """Render one standalone BOM timeline as the default local reading view."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir.resolve()

    def render(self, view: dict[str, Any]) -> str:
        title = str(view.get("title") or "BOM 投资研究")
        lenses = list(view.get("lenses") or [])
        claims = [
            claim
            for lens in lenses
            for claim in lens.get("claims") or []
        ]
        source_count = len(
            {
                str(claim.get("source_id") or "")
                for claim in claims
                if str(claim.get("source_id") or "")
            }
        )
        nav = "".join(
            (
                f'<a href="#lens-{escape(str(lens["lens_id"]))}">'
                f'{index:02d} {escape(str(lens["label"]))}</a>'
            )
            for index, lens in enumerate(lenses, start=1)
        )
        sections = "\n".join(
            self._render_lens(lens, index)
            for index, lens in enumerate(lenses, start=1)
        )
        return "\n".join(
            [
                "<!doctype html>",
                '<html lang="zh-CN">',
                "<head>",
                '<meta charset="utf-8">',
                '<meta name="viewport" content="width=device-width, initial-scale=1">',
                f"<title>{escape(title)}</title>",
                f"<style>{_report_css()}</style>",
                "</head>",
                (
                    '<body data-report-scope="standalone-bom" '
                    f'data-bom-node-id="{escape(str(view.get("bom_node_id") or ""))}">'
                ),
                '<header class="report-header">',
                '  <div class="report-header-inner">',
                '    <div class="report-label">VALUE INVEST · BOM RESEARCH</div>',
                f"    <h1>{escape(title)}</h1>",
                (
                    '    <p class="report-deck">以材料发布时间组织证据，'
                    "把需求、供给、技术、估值与治理放在同一研究截面内。</p>"
                ),
                '    <div class="report-meta" aria-label="报告元数据">',
                (
                    '      <div><span>研究截面</span>'
                    f'<strong>{escape(str(view.get("as_of_date") or ""))}</strong></div>'
                ),
                f"      <div><span>研究视角</span><strong>{len(lenses)}</strong></div>",
                f"      <div><span>映射材料</span><strong>{source_count}</strong></div>",
                f"      <div><span>原子观点</span><strong>{len(claims)}</strong></div>",
                "    </div>",
                "  </div>",
                "</header>",
                '<nav class="top-nav" aria-label="报告章节">',
                f'  <div class="top-nav-inner">{nav}</div>',
                "</nav>",
                '<main class="report-main">',
                sections,
                "</main>",
                '<footer class="report-footer">',
                "  <p>本报告由结构化材料账本生成；事实、预测和观点按原文位置保留。</p>",
                "</footer>",
                f"<script>{_report_script()}</script>",
                "</body>",
                "</html>",
                "",
            ]
        )

    def _render_lens(self, lens: dict[str, Any], index: int) -> str:
        lens_id = escape(str(lens.get("lens_id") or ""))
        label = escape(str(lens.get("label") or ""))
        logic = escape(str(lens.get("logic_chain") or "当前逻辑链尚未定义。"))
        conclusion = escape(str(lens.get("conclusion") or "当前尚不能形成结论。"))
        trend = escape(str(lens.get("trend") or "当前为首个研究截面。"))
        groups = _group_claims_by_source(list(lens.get("claims") or []))
        source_rows = "\n".join(
            self._render_source_row(group)
            for group in groups
        )
        if not source_rows:
            source_rows = (
                '<tr><td class="empty-state" colspan="4">'
                "尚无经过问题化解析和复核的材料。</td></tr>"
            )
        claim_count = sum(len(group.get("claims") or []) for group in groups)
        return f"""
<details id="lens-{lens_id}" class="lens-section" open>
  <summary class="lens-heading">
    <span class="lens-number">{index:02d}</span>
    <div>
      <p>RESEARCH LENS</p>
      <h2>{label}</h2>
    </div>
    <span class="lens-count">{len(groups)} 份材料 · {claim_count} 条观点</span>
    <span class="lens-chevron" aria-hidden="true"></span>
  </summary>
  <div class="lens-body">
    <section class="logic-note" aria-labelledby="logic-{lens_id}">
      <h3 id="logic-{lens_id}">简单逻辑链</h3>
      <p>{logic}</p>
    </section>

    <section class="timeline" aria-labelledby="timeline-{lens_id}">
      <div class="section-heading">
        <div>
          <span>01</span>
          <h3 id="timeline-{lens_id}">信息时间线</h3>
        </div>
        <p>按市场可见日期由近及远</p>
      </div>
      <div class="timeline-table-wrap" role="region" aria-label="{label}信息时间线" tabindex="0">
        <table class="timeline-table">
          <colgroup>
            <col class="col-date">
            <col class="col-type">
            <col class="col-report">
            <col class="col-claims">
          </colgroup>
          <thead>
            <tr>
              <th scope="col">时间</th>
              <th scope="col">信息类型</th>
              <th scope="col">报告</th>
              <th scope="col">观点列表</th>
            </tr>
          </thead>
          <tbody>
            {source_rows}
          </tbody>
        </table>
      </div>
    </section>

    <section class="conclusion-panel" aria-labelledby="conclusion-{lens_id}">
      <div class="section-heading">
        <div>
          <span>02</span>
          <h3 id="conclusion-{lens_id}">最新结论与趋势</h3>
        </div>
      </div>
      <p class="conclusion-text">{conclusion}</p>
      <div class="trend-line">
        <strong>趋势变化</strong>
        <p>{trend}</p>
      </div>
    </section>
  </div>
</details>
"""

    def _render_source_row(self, group: dict[str, Any]) -> str:
        title = escape(
            str(group.get("source_title") or group.get("source_id") or "来源")
        )
        published_at = escape(str(group.get("published_at") or ""))
        material_class = str(group.get("material_class") or "other")
        material_label = escape(MATERIAL_LABELS.get(material_class, "其他"))
        source_url = _rendered_source_url(
            str(group.get("source_url") or ""),
            project_dir=self.project_dir,
        )
        source_link = title
        if source_url:
            escaped_url = escape(source_url, quote=True)
            if source_url.startswith(("http://", "https://")):
                source_link = (
                    f'<a href="{escaped_url}" target="_blank" rel="noopener">'
                    f'{title}<span aria-hidden="true">↗</span></a>'
                )
            else:
                source_link = (
                    f'<a href="{escaped_url}">{title}'
                    '<span aria-hidden="true">PDF</span></a>'
                )
        bullets = "\n".join(
            _render_claim(claim, index)
            for index, claim in enumerate(group.get("claims") or [], start=1)
        )
        return f"""
<tr class="source-row">
  <td class="source-date"><time datetime="{published_at}">{published_at}</time></td>
  <td class="source-type"><span class="material-tag">{material_label}</span></td>
  <td class="source-report">{source_link}</td>
  <td class="source-claims">
    <ul class="claim-list">
      {bullets}
    </ul>
  </td>
</tr>
"""


def _render_claim(claim: dict[str, Any], index: int) -> str:
    location = escape(str(claim.get("source_location") or "原文位置未标注"))
    statement = escape(str(claim.get("statement") or ""))
    return f"""
<li>
  <div class="claim-heading">
    <span class="claim-index">观点 {index:02d}</span>
    <span class="claim-location">{location}</span>
  </div>
  <p>{statement}</p>
</li>
"""


def _group_claims_by_source(
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for claim in claims:
        source_id = str(claim.get("source_id") or "")
        if source_id not in grouped:
            grouped[source_id] = {
                "source_id": source_id,
                "published_at": claim.get("published_at"),
                "material_class": claim.get("material_class"),
                "source_title": claim.get("source_title"),
                "source_url": claim.get("source_url"),
                "claims": [],
            }
            order.append(source_id)
        grouped[source_id]["claims"].append(claim)
    return [grouped[source_id] for source_id in order]


def _rendered_source_url(url: str, *, project_dir: Path) -> str:
    if not url:
        return ""
    if url.startswith(("http://", "https://")):
        return url
    path = Path(url)
    if path.is_absolute():
        try:
            return path.resolve().relative_to(project_dir).as_posix()
        except ValueError:
            return ""
    return path.as_posix()


def _report_css() -> str:
    return """
:root {
  color-scheme: light;
  --page: #f3f5f7;
  --surface: #ffffff;
  --surface-soft: #eef3f7;
  --ink: #273342;
  --muted: #697887;
  --line: #d9e0e6;
  --line-strong: #bdc8d2;
  --blue: #245f83;
  --blue-soft: #e7f0f5;
  --rust: #a95e46;
  --green: #39705d;
  --shadow: 0 12px 32px rgba(36, 55, 72, 0.08);
}

* { box-sizing: border-box; }

html {
  scroll-behavior: smooth;
  background: var(--page);
}

body {
  margin: 0;
  background: var(--page);
  color: var(--ink);
  font-family: "Avenir Next", "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", sans-serif;
  font-size: 16px;
  line-height: 1.75;
  letter-spacing: 0;
}

a { color: var(--blue); }

.report-header {
  background: var(--surface);
  border-bottom: 1px solid var(--line);
}

.report-header-inner,
.top-nav-inner,
.report-main,
.report-footer {
  width: min(1180px, calc(100% - 48px));
  margin: 0 auto;
}

.report-header-inner {
  padding: 62px 0 42px;
}

.report-label {
  color: var(--rust);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.12em;
}

h1 {
  max-width: 860px;
  margin: 12px 0 10px;
  color: #18364d;
  font-family: "Baskerville", "Songti SC", serif;
  font-size: clamp(36px, 5vw, 62px);
  font-weight: 600;
  line-height: 1.08;
  letter-spacing: 0;
}

.report-deck {
  max-width: 780px;
  margin: 0;
  color: var(--muted);
  font-size: 18px;
}

.report-meta {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  max-width: 760px;
  margin-top: 34px;
  border-top: 1px solid var(--line);
}

.report-meta div {
  min-width: 0;
  padding: 16px 20px 0 0;
}

.report-meta span {
  display: block;
  color: var(--muted);
  font-size: 12px;
}

.report-meta strong {
  display: block;
  margin-top: 2px;
  color: #24445c;
  font-size: 19px;
  font-weight: 650;
}

.top-nav {
  position: sticky;
  z-index: 30;
  top: 0;
  overflow-x: auto;
  border-bottom: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: saturate(140%) blur(14px);
}

.top-nav-inner {
  display: flex;
  min-width: max-content;
}

.top-nav a {
  padding: 14px 18px;
  border-bottom: 2px solid transparent;
  color: var(--muted);
  font-size: 13px;
  font-weight: 650;
  text-decoration: none;
  transition: color 160ms ease, border-color 160ms ease;
}

.top-nav a:first-child { padding-left: 0; }
.top-nav a:hover,
.top-nav a.is-active {
  border-color: var(--blue);
  color: var(--blue);
}

.report-main { padding: 24px 0 80px; }

.lens-section {
  border-bottom: 1px solid var(--line-strong);
  background: transparent;
}

.lens-heading {
  display: grid;
  grid-template-columns: 58px minmax(0, 1fr) auto 18px;
  gap: 18px;
  align-items: center;
  padding: 34px 0;
  cursor: pointer;
  list-style: none;
}

.lens-heading::-webkit-details-marker { display: none; }

.lens-number {
  color: var(--rust);
  font-family: "Baskerville", serif;
  font-size: 28px;
}

.lens-heading p {
  margin: 0 0 2px;
  color: var(--muted);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.12em;
}

.lens-heading h2 {
  margin: 0;
  color: #1d4967;
  font-size: 26px;
  line-height: 1.2;
  letter-spacing: 0;
}

.lens-count {
  color: var(--muted);
  font-size: 13px;
}

.lens-chevron {
  width: 10px;
  height: 10px;
  border-right: 2px solid var(--blue);
  border-bottom: 2px solid var(--blue);
  transform: rotate(45deg);
  transition: transform 180ms ease;
}

.lens-section:not([open]) .lens-chevron { transform: rotate(-45deg); }

.lens-body {
  padding: 0 0 56px 76px;
  animation: reveal 220ms ease both;
}

@keyframes reveal {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

.logic-note {
  max-width: 920px;
  padding: 20px 24px;
  border-left: 3px solid var(--rust);
  background: var(--surface);
  box-shadow: var(--shadow);
}

.logic-note h3,
.logic-note p { margin: 0; }

.logic-note h3 {
  color: var(--rust);
  font-size: 12px;
  font-weight: 750;
}

.logic-note p {
  margin-top: 7px;
  color: #455565;
}

.timeline,
.conclusion-panel {
  margin-top: 42px;
}

.section-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.section-heading > div {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.section-heading span {
  color: var(--rust);
  font-size: 11px;
  font-weight: 750;
}

.section-heading h3 {
  margin: 0;
  color: #264a64;
  font-size: 19px;
  letter-spacing: 0;
}

.section-heading > p {
  margin: 0;
  color: var(--muted);
  font-size: 12px;
}

.timeline-table-wrap {
  width: 100%;
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--surface);
  box-shadow: 0 4px 18px rgba(36, 55, 72, 0.045);
  scrollbar-color: #aebdc8 transparent;
  scrollbar-width: thin;
}

.timeline-table-wrap:focus-visible {
  outline: 2px solid var(--blue);
  outline-offset: 3px;
}

.timeline-table {
  width: 100%;
  min-width: 980px;
  border-collapse: collapse;
  table-layout: fixed;
}

.timeline-table .col-date { width: 118px; }
.timeline-table .col-type { width: 112px; }
.timeline-table .col-report { width: 260px; }
.timeline-table .col-claims { width: auto; }

.timeline-table th {
  padding: 12px 16px;
  border-bottom: 1px solid var(--line-strong);
  background: #edf2f5;
  color: #526575;
  font-size: 11px;
  font-weight: 760;
  text-align: left;
  vertical-align: bottom;
}

.timeline-table td {
  padding: 18px 16px;
  border-bottom: 1px solid var(--line);
  color: #3c4b5a;
  font-size: 14px;
  text-align: left;
  vertical-align: top;
}

.timeline-table tbody tr:last-child td { border-bottom: 0; }

.timeline-table tbody tr:hover { background: #f9fbfc; }

.source-date time {
  color: #315a75;
  font-size: 13px;
  font-weight: 720;
}

.source-report {
  font-weight: 680;
  line-height: 1.55;
  overflow-wrap: anywhere;
}

.material-tag {
  display: inline-block;
  padding: 1px 7px;
  border: 1px solid #c9d8e2;
  border-radius: 4px;
  background: var(--blue-soft);
  color: var(--blue);
  font-size: 11px;
  font-weight: 700;
}

.source-report a {
  text-decoration: none;
}

.source-report a:hover { text-decoration: underline; }
.source-report a span {
  margin-left: 6px;
  color: var(--rust);
  font-size: 10px;
  font-weight: 760;
}

.claim-list {
  margin: 0;
  padding-left: 18px;
  list-style: disc;
}

.claim-list li {
  padding: 0 0 14px 3px;
}

.claim-list li:last-child { padding-bottom: 0; }

.claim-list li::marker { color: var(--rust); }

.claim-heading {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 10px;
  align-items: baseline;
  margin-bottom: 4px;
}

.claim-index {
  color: var(--rust);
  font-size: 12px;
  font-weight: 760;
}

.claim-location {
  color: var(--green);
  font-size: 12px;
  font-weight: 680;
}

.claim-list p {
  margin: 0;
  color: #3c4b5a;
  font-size: 14px;
}

.conclusion-panel {
  padding: 26px 28px;
  border-top: 3px solid var(--blue);
  background: var(--blue-soft);
}

.conclusion-panel .section-heading { margin-bottom: 12px; }

.conclusion-text {
  margin: 0;
  color: #28475e;
  font-size: 16px;
  font-weight: 520;
}

.trend-line {
  display: grid;
  grid-template-columns: 90px minmax(0, 1fr);
  gap: 16px;
  margin-top: 18px;
  padding-top: 16px;
  border-top: 1px solid #c6d8e3;
}

.trend-line strong {
  color: var(--rust);
  font-size: 12px;
}

.trend-line p {
  margin: 0;
  color: #526777;
  font-size: 14px;
}

.empty-state {
  padding: 24px;
  color: var(--muted);
  text-align: center;
}

.report-footer {
  padding: 26px 0 40px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 12px;
}

.report-footer p { margin: 0; }

@media (max-width: 760px) {
  .report-header-inner,
  .top-nav-inner,
  .report-main,
  .report-footer {
    width: min(100% - 28px, 1180px);
  }

  .report-header-inner { padding: 38px 0 28px; }
  h1 { font-size: 38px; }
  .report-deck { font-size: 16px; }
  .report-meta { grid-template-columns: repeat(2, minmax(0, 1fr)); }

  .lens-heading {
    grid-template-columns: 42px minmax(0, 1fr) 16px;
    gap: 12px;
    padding: 26px 0;
  }

  .lens-count {
    grid-column: 2;
    grid-row: 2;
  }

  .lens-chevron {
    grid-column: 3;
    grid-row: 1 / span 2;
  }

  .lens-body { padding: 0 0 42px; }
  .timeline-table { min-width: 880px; }
  .section-heading { align-items: flex-start; flex-direction: column; }
  .trend-line { grid-template-columns: 1fr; gap: 4px; }
}

@media print {
  .top-nav { display: none; }
  .report-main { padding-top: 0; }
  .lens-section { break-inside: avoid; }
  .timeline-table-wrap { overflow: visible; box-shadow: none; }
  .timeline-table { min-width: 0; }
}
"""


def _report_script() -> str:
    return """
const navLinks = Array.from(document.querySelectorAll('.top-nav a'));
const sections = Array.from(document.querySelectorAll('.lens-section'));
const linkById = new Map(navLinks.map((link) => [link.hash.slice(1), link]));
const observer = new IntersectionObserver((entries) => {
  const visible = entries
    .filter((entry) => entry.isIntersecting)
    .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
  if (!visible) return;
  navLinks.forEach((link) => link.classList.remove('is-active'));
  linkById.get(visible.target.id)?.classList.add('is-active');
}, { rootMargin: '-18% 0px -72% 0px', threshold: [0.05, 0.2, 0.5] });
sections.forEach((section) => observer.observe(section));
"""
