from __future__ import annotations

from typing import Any

from value_invest_research.adapters.outbound.report_sections.base import ReportRenderContext
from value_invest_research.adapters.outbound.report_sections.shared import _e


class SourcesSection:
    section_id = "sources"

    def render(self, context: ReportRenderContext) -> str:
        return _render_sources(context.data["sources"])


def _render_sources(sources: list[dict[str, Any]]) -> str:
    rows = "\n".join(_source_row(source) for source in sources)
    if not rows:
        rows = '<tr><td colspan="5">暂无来源记录。</td></tr>'
    return f"""
<section id="sources" class="section source-section">
  <div class="section-heading">
    <span class="section-kicker">05</span>
    <h2>来源索引</h2>
  </div>
  <details class="source-collapse">
    <summary>展开来源索引</summary>
    <table class="source-table">
      <thead><tr><th>ID</th><th>类别</th><th>立场</th><th>摘要</th><th>链接</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </details>
</section>
</main>
""".strip()


def _source_row(source: dict[str, Any]) -> str:
    url = str(source.get("url", ""))
    link = f'<a href="{_e(url)}" target="_blank" rel="noreferrer">打开</a>' if url else ""
    return f"""
<tr>
  <td>{_e(str(source.get("source_id") or source.get("id") or ""))}</td>
  <td>{_e(str(source.get("source_bucket") or source.get("information_category") or ""))}</td>
  <td>{_e(str(source.get("support_refute_or_lead") or ""))}</td>
  <td>{_e(str(source.get("summary") or source.get("title") or ""))}</td>
  <td>{link}</td>
</tr>
""".strip()
