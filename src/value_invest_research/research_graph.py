from __future__ import annotations

import json
from html import escape
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from value_invest_research.models import EvidenceRecord, ValidationError
from value_invest_research.runlog import RunLog, RunStatus


TICKER_ALIASES = {"APPL": "AAPL"}
STAGE_ORDER = {
    "consensus": 1,
    "questions": 2,
    "hypotheses": 3,
    "tests": 4,
    "report": 5,
}

TIME_FRAMES = [
    {"id": "T1", "label": "T1 0-3 months", "focus": "near-term catalyst, event reaction, or sentiment move"},
    {"id": "T2", "label": "T2 3-15 months", "focus": "earnings revision, margin/share inflection, or cycle confirmation"},
    {"id": "T3", "label": "T3 15+ months", "focus": "durable ROE, business model proof, and long-cycle compounding"},
]

DIMENSIONS = [
    {
        "id": "3c_cycle",
        "component": "3C",
        "label": "Cycle",
        "driver": "D2",
        "probe": "cycle evidence changes direction",
        "why": "Cycle shifts can make yesterday's consensus stale.",
    },
    {
        "id": "3c_change",
        "component": "3C",
        "label": "Change",
        "driver": "D2",
        "probe": "a marginal operating or industry change becomes observable",
        "why": "FengHe research starts with observable change.",
    },
    {
        "id": "3c_certainty",
        "component": "3C",
        "label": "Certainty",
        "driver": "D1",
        "probe": "evidence quality improves or deteriorates",
        "why": "Certainty controls whether a thesis can be strengthened.",
    },
    {
        "id": "d1_intrinsic_value",
        "component": "3D",
        "label": "D1 ROE / intrinsic value",
        "driver": "D1",
        "probe": "ROE, cash generation, or book value compounding changes",
        "why": "D1 captures durable value creation.",
    },
    {
        "id": "d2_marginal_change",
        "component": "3D",
        "label": "D2 marginal change / catalyst",
        "driver": "D2",
        "probe": "a catalyst changes expectations faster than consensus updates",
        "why": "D2 is where forward expectation gaps usually appear.",
    },
    {
        "id": "d3_sentiment_valuation",
        "component": "3D",
        "label": "D3 sentiment / valuation",
        "driver": "D3",
        "probe": "valuation, crowding, or market emotion changes",
        "why": "D3 separates price dislocation from business change.",
    },
    {
        "id": "m1_market_size",
        "component": "5M",
        "label": "M1 market size",
        "driver": "D2",
        "probe": "the addressable market or demand cycle changes",
        "why": "Market size sets the runway for value creation.",
    },
    {
        "id": "m2_market_share",
        "component": "5M",
        "label": "M2 market share",
        "driver": "D2",
        "probe": "competitive share or distribution power changes",
        "why": "Share shifts can revise growth and margin expectations.",
    },
    {
        "id": "m3_margin",
        "component": "5M",
        "label": "M3 margin",
        "driver": "D2",
        "probe": "gross margin, operating leverage, pricing, or cost evidence changes",
        "why": "Margins convert operating change into earnings revisions.",
    },
    {
        "id": "m4_model",
        "component": "5M",
        "label": "M4 model",
        "driver": "D1",
        "probe": "cash conversion, reinvestment need, or capital intensity changes",
        "why": "The model explains the durability of ROE.",
    },
    {
        "id": "m5_management",
        "component": "5M",
        "label": "M5 management",
        "driver": "D1",
        "probe": "capital allocation, incentives, or execution evidence changes",
        "why": "Management affects whether value creation is repeatable.",
    },
]

EVIDENCE_HINTS = {
    "3c_cycle": ["revenue", "income", "price"],
    "3c_change": ["revenue", "income", "margin", "price"],
    "3c_certainty": ["sec", "10-q", "10-k", "xbrl"],
    "d1_intrinsic_value": ["income", "assets", "equity", "cash", "liabilities", "profit"],
    "d2_marginal_change": ["revenue", "income", "margin", "price"],
    "d3_sentiment_valuation": ["price", "valuation", "close"],
    "m1_market_size": ["revenue", "sales"],
    "m2_market_share": ["share", "revenue"],
    "m3_margin": ["gross profit", "operating income", "margin", "income"],
    "m4_model": ["cash", "assets", "liabilities", "equity", "free cash flow"],
    "m5_management": ["management", "capital allocation", "buyback", "dividend"],
}


@dataclass
class GraphNode:
    id: str
    type: str
    label: str
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "label": self.label,
            "properties": self.properties,
        }


@dataclass
class GraphEdge:
    source: str
    target: str
    relation: str
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "relation": self.relation,
            "properties": self.properties,
        }


class ResearchGraph:
    def __init__(self) -> None:
        self._nodes: dict[str, GraphNode] = {}
        self._edges: dict[tuple[str, str, str], GraphEdge] = {}

    def add_node(self, node: GraphNode) -> None:
        self._nodes[node.id] = node

    def add_edge(self, edge: GraphEdge) -> None:
        self._edges[(edge.source, edge.target, edge.relation)] = edge

    def nodes(self) -> list[GraphNode]:
        return [self._nodes[key] for key in sorted(self._nodes)]

    def edges(self) -> list[GraphEdge]:
        return [self._edges[key] for key in sorted(self._edges)]


def normalize_ticker(ticker: str) -> str:
    normalized = ticker.strip().upper()
    return TICKER_ALIASES.get(normalized, normalized)


def run_research_graph_stage(root: Path, ticker: str, stage: str = "report") -> dict[str, Any]:
    normalized = normalize_ticker(ticker)
    if stage not in STAGE_ORDER:
        raise ValueError(f"stage must be one of {sorted(STAGE_ORDER)}")

    stock_dir = root / "stocks" / normalized
    if not stock_dir.exists():
        raise ValueError(f"stock folder not found: {stock_dir}")

    evidence = _load_evidence(stock_dir)
    graph = ResearchGraph()
    _add_framework_nodes(graph, normalized)
    _add_evidence_nodes(graph, evidence, normalized)

    stage_rank = STAGE_ORDER[stage]
    if stage_rank >= STAGE_ORDER["consensus"]:
        _add_consensus_nodes(graph, normalized, evidence)
    if stage_rank >= STAGE_ORDER["questions"]:
        _add_question_nodes(graph, normalized)
    if stage_rank >= STAGE_ORDER["hypotheses"]:
        _add_hypothesis_nodes(graph, normalized)
    if stage_rank >= STAGE_ORDER["tests"]:
        _add_assumption_test_nodes(graph, normalized, evidence)

    graph_dir = stock_dir / "research_graph"
    graph_dir.mkdir(parents=True, exist_ok=True)
    nodes_path = graph_dir / "nodes.jsonl"
    edges_path = graph_dir / "edges.jsonl"
    _write_jsonl(nodes_path, [node.to_dict() for node in graph.nodes()])
    _write_jsonl(edges_path, [edge.to_dict() for edge in graph.edges()])

    report_path = ""
    if stage_rank >= STAGE_ORDER["report"]:
        report_path = str(_write_forward_report(graph_dir, normalized, graph, evidence))

    RunLog(stock_dir / "logs").append(
        f"research_graph_{stage}",
        RunStatus.SUCCESS,
        tickers=[normalized],
        records_fetched=len(evidence),
        records_new=len(graph.nodes()),
    )

    return {
        "ticker": normalized,
        "stage": stage,
        "nodes": len(graph.nodes()),
        "edges": len(graph.edges()),
        "nodes_path": str(nodes_path),
        "edges_path": str(edges_path),
        "report_path": report_path,
    }


def _load_evidence(stock_dir: Path) -> list[EvidenceRecord]:
    evidence_path = stock_dir / "evidence.jsonl"
    if not evidence_path.exists():
        return []

    records: list[EvidenceRecord] = []
    for line_number, line in enumerate(evidence_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(EvidenceRecord.from_dict(json.loads(line)))
        except (json.JSONDecodeError, ValidationError) as exc:
            raise ValueError(f"{evidence_path}:{line_number}: {exc}") from exc
    return records


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8", newline="\n")


def _stock_node_id(ticker: str) -> str:
    return f"stock_{ticker.lower()}"


def _dimension_node_id(dimension_id: str) -> str:
    return f"dim_{dimension_id}"


def _time_frame_node_id(time_frame: str) -> str:
    return f"tf_{time_frame.lower()}"


def _driver_node_id(driver: str) -> str:
    return f"driver_{driver.lower()}"


def _consensus_node_id(ticker: str, dimension_id: str) -> str:
    return f"c_{ticker.lower()}_{dimension_id}"


def _question_node_id(ticker: str, dimension_id: str, time_frame: str) -> str:
    return f"q_{ticker.lower()}_{dimension_id}_{time_frame.lower()}_001"


def _hypothesis_node_id(ticker: str, dimension_id: str, time_frame: str) -> str:
    return f"h_{ticker.lower()}_{dimension_id}_{time_frame.lower()}_001"


def _assumption_node_id(ticker: str, dimension_id: str, time_frame: str) -> str:
    return f"a_{ticker.lower()}_{dimension_id}_{time_frame.lower()}_001"


def _add_framework_nodes(graph: ResearchGraph, ticker: str) -> None:
    graph.add_node(GraphNode(_stock_node_id(ticker), "stock", ticker, {"ticker": ticker}))
    for driver in ["D1", "D2", "D3"]:
        graph.add_node(GraphNode(_driver_node_id(driver), "price_driver", driver, {"framework_component": "3D"}))
    for time_frame in TIME_FRAMES:
        graph.add_node(GraphNode(
            _time_frame_node_id(time_frame["id"]),
            "time_frame",
            time_frame["label"],
            {"focus": time_frame["focus"]},
        ))
    for dimension in DIMENSIONS:
        dim_id = _dimension_node_id(dimension["id"])
        graph.add_node(GraphNode(dim_id, "framework_dimension", dimension["label"], dimension))
        graph.add_edge(GraphEdge(_stock_node_id(ticker), dim_id, "analyzed_through"))
        graph.add_edge(GraphEdge(dim_id, _driver_node_id(dimension["driver"]), "maps_to_driver"))


def _add_evidence_nodes(graph: ResearchGraph, evidence: list[EvidenceRecord], ticker: str) -> None:
    for record in evidence:
        graph.add_node(GraphNode(
            record.id,
            "evidence",
            record.source_name,
            {
                "summary": record.summary,
                "reliability": record.reliability,
                "materiality": record.materiality,
                "source_type": record.source_type,
                "url": record.url,
            },
        ))
        graph.add_edge(GraphEdge(record.id, _stock_node_id(ticker), "belongs_to"))


def _evidence_ids_for_dimension(evidence: list[EvidenceRecord], dimension_id: str) -> list[str]:
    hints = EVIDENCE_HINTS.get(dimension_id, [])
    matches = []
    for record in evidence:
        text = f"{record.source_type} {record.source_name} {record.summary}".lower()
        if any(hint in text for hint in hints):
            matches.append(record.id)
    return matches


def _add_consensus_nodes(graph: ResearchGraph, ticker: str, evidence: list[EvidenceRecord]) -> None:
    for dimension in DIMENSIONS:
        evidence_ids = _evidence_ids_for_dimension(evidence, dimension["id"])
        status = "baseline_evidenced" if evidence_ids else "needs_evidence"
        statement = (
            f"Local evidence creates a current baseline for {dimension['label']}; "
            "treat it as reflected in price until a change hypothesis is supported."
            if evidence_ids
            else f"No local evidence yet establishes the consensus baseline for {dimension['label']}."
        )
        node_id = _consensus_node_id(ticker, dimension["id"])
        graph.add_node(GraphNode(
            node_id,
            "consensus",
            f"{ticker} {dimension['label']} consensus baseline",
            {
                "ticker": ticker,
                "dimension": dimension["id"],
                "framework_component": dimension["component"],
                "linked_driver": dimension["driver"],
                "status": status,
                "statement": statement,
                "price_baseline_assumption": "Known facts and market-facing consensus are presumed priced until tested otherwise.",
                "evidence_ids": evidence_ids,
            },
        ))
        graph.add_edge(GraphEdge(_stock_node_id(ticker), node_id, "has_consensus"))
        graph.add_edge(GraphEdge(node_id, _dimension_node_id(dimension["id"]), "maps_to_dimension"))
        for evidence_id in evidence_ids:
            graph.add_edge(GraphEdge(evidence_id, node_id, "supports_baseline"))


def _add_question_nodes(graph: ResearchGraph, ticker: str) -> None:
    for dimension in DIMENSIONS:
        for time_frame in TIME_FRAMES:
            tf = time_frame["id"]
            node_id = _question_node_id(ticker, dimension["id"], tf)
            question = (
                f"What would make {ticker}'s {dimension['label']} baseline change over {time_frame['label']}?"
            )
            graph.add_node(GraphNode(
                node_id,
                "question",
                question,
                {
                    "ticker": ticker,
                    "dimension": dimension["id"],
                    "time_frame": tf,
                    "linked_driver": dimension["driver"],
                    "question": question,
                    "why_it_matters": dimension["why"],
                    "status": "open",
                },
            ))
            graph.add_edge(GraphEdge(_consensus_node_id(ticker, dimension["id"]), node_id, "raises_question"))
            graph.add_edge(GraphEdge(node_id, _time_frame_node_id(tf), "scoped_to"))
            graph.add_edge(GraphEdge(node_id, _driver_node_id(dimension["driver"]), "linked_to_driver"))


def _add_hypothesis_nodes(graph: ResearchGraph, ticker: str) -> None:
    for dimension in DIMENSIONS:
        for time_frame in TIME_FRAMES:
            tf = time_frame["id"]
            node_id = _hypothesis_node_id(ticker, dimension["id"], tf)
            hypothesis = (
                f"If {dimension['probe']} over {tf}, {ticker}'s {dimension['label']} view may change through "
                f"{dimension['driver']}."
            )
            graph.add_node(GraphNode(
                node_id,
                "hypothesis",
                hypothesis,
                {
                    "ticker": ticker,
                    "dimension": dimension["id"],
                    "time_frame": tf,
                    "dominant_driver": dimension["driver"],
                    "hypothesis": hypothesis,
                    "mechanism": f"{dimension['probe']} -> {dimension['label']} revision -> {dimension['driver']}",
                    "prior_probability": "medium",
                    "status": "untested",
                },
            ))
            graph.add_edge(GraphEdge(_question_node_id(ticker, dimension["id"], tf), node_id, "frames_hypothesis"))


def _add_assumption_test_nodes(graph: ResearchGraph, ticker: str, evidence: list[EvidenceRecord]) -> None:
    for dimension in DIMENSIONS:
        evidence_ids = _evidence_ids_for_dimension(evidence, dimension["id"])
        for time_frame in TIME_FRAMES:
            tf = time_frame["id"]
            verdict = "evidence_seeded" if evidence_ids else "needs_evidence"
            node_id = _assumption_node_id(ticker, dimension["id"], tf)
            graph.add_node(GraphNode(
                node_id,
                "assumption_test",
                f"Test {ticker} {dimension['label']} {tf} assumption",
                {
                    "ticker": ticker,
                    "dimension": dimension["id"],
                    "time_frame": tf,
                    "assumption": (
                        f"The data can distinguish a new {dimension['label']} change from consensus already in price."
                    ),
                    "test": (
                        f"Compare fresh primary evidence, management commentary, market data, and disconfirming signals for "
                        f"{dimension['label']} over {tf}."
                    ),
                    "supporting_evidence_ids": evidence_ids,
                    "disconfirming_evidence_ids": [],
                    "verdict": verdict,
                },
            ))
            graph.add_edge(GraphEdge(_hypothesis_node_id(ticker, dimension["id"], tf), node_id, "depends_on"))
            for evidence_id in evidence_ids:
                graph.add_edge(GraphEdge(evidence_id, node_id, "tests_with"))


def _write_forward_report(
    graph_dir: Path,
    ticker: str,
    graph: ResearchGraph,
    evidence: list[EvidenceRecord],
) -> Path:
    report_path = graph_dir / "forward_report.html"
    nodes = [node.to_dict() for node in graph.nodes()]
    consensus_nodes = [node for node in nodes if node["type"] == "consensus"]
    question_nodes = [node for node in nodes if node["type"] == "question"]
    assumption_nodes = [node for node in nodes if node["type"] == "assumption_test"]
    generated_at = datetime.now(timezone.utc).isoformat()
    primary_evidence_count = sum(1 for item in evidence if item.reliability == "primary")

    html = _render_forward_report_html(
        ticker=ticker,
        generated_at=generated_at,
        graph=graph,
        evidence=evidence,
        consensus_nodes=consensus_nodes,
        question_nodes=question_nodes,
        assumption_nodes=assumption_nodes,
        primary_evidence_count=primary_evidence_count,
    )
    report_path.write_text(html, encoding="utf-8", newline="\n")
    return report_path


def _render_forward_report_html(
    ticker: str,
    generated_at: str,
    graph: ResearchGraph,
    evidence: list[EvidenceRecord],
    consensus_nodes: list[dict[str, Any]],
    question_nodes: list[dict[str, Any]],
    assumption_nodes: list[dict[str, Any]],
    primary_evidence_count: int,
) -> str:
    seeded_tests = sum(1 for node in assumption_nodes if node["properties"]["verdict"] == "evidence_seeded")
    consensus_html = "\n".join(_render_consensus_row(node) for node in consensus_nodes)
    question_html = "\n".join(_render_question_section(time_frame, question_nodes) for time_frame in ["T1", "T2", "T3"])
    assumption_html = "\n".join(_render_assumption_row(node) for node in assumption_nodes)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(ticker)} Forward Research Graph Report</title>
  <style>
    :root {{
      --paper: #f7f4ee;
      --ink: #1d2321;
      --muted: #65706b;
      --line: #c9c3b7;
      --panel: #fffdf8;
      --accent: #0f6b57;
      --amber: #9b5c16;
      --risk: #9a3022;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: var(--paper);
      font-family: Georgia, "Times New Roman", "Noto Serif SC", serif;
      line-height: 1.55;
    }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 40px 28px 64px; }}
    .hero {{ border-bottom: 3px solid var(--ink); padding-bottom: 22px; margin-bottom: 24px; }}
    .eyebrow, .meta, .status, .evidence-chip, .node-id, th {{
      font-family: "Lucida Console", Consolas, monospace;
      letter-spacing: 0;
    }}
    .eyebrow {{ color: var(--accent); font-size: 12px; text-transform: uppercase; }}
    h1 {{ font-size: 46px; line-height: 1.04; margin: 10px 0 12px; max-width: 820px; }}
    h2 {{ font-size: 24px; margin: 34px 0 14px; padding-bottom: 8px; border-bottom: 1px solid var(--line); }}
    h3 {{ font-size: 18px; margin: 0 0 10px; }}
    .meta {{ display: flex; flex-wrap: wrap; gap: 10px; color: var(--muted); font-size: 12px; }}
    .notice {{
      margin-top: 18px;
      border-left: 4px solid var(--risk);
      padding: 10px 14px;
      background: rgba(154, 48, 34, 0.08);
      font-family: "Lucida Console", Consolas, monospace;
      font-size: 12px;
    }}
    .metrics {{ display: grid; grid-template-columns: repeat(4, minmax(150px, 1fr)); gap: 12px; margin: 24px 0; }}
    .metric, .question-band, .panel, .table-wrap {{ background: var(--panel); border: 1px solid var(--line); }}
    .metric {{ padding: 14px; }}
    .metric strong {{ display: block; font-size: 26px; line-height: 1; }}
    .metric span {{ color: var(--muted); font-family: "Lucida Console", Consolas, monospace; font-size: 11px; }}
    .table-wrap {{ overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; min-width: 840px; font-size: 14px; }}
    th, td {{ border-bottom: 1px solid var(--line); padding: 12px; text-align: left; vertical-align: top; }}
    th {{ background: #ece6da; font-size: 11px; text-transform: uppercase; }}
    .status {{ display: inline-block; padding: 3px 8px; border: 1px solid var(--line); font-size: 11px; white-space: nowrap; }}
    .status.ok {{ color: var(--accent); border-color: rgba(15,107,87,0.45); }}
    .status.gap {{ color: var(--amber); border-color: rgba(155,92,22,0.45); }}
    .evidence-chip {{
      display: inline-block;
      margin: 2px 4px 2px 0;
      padding: 2px 7px;
      border: 1px solid rgba(15,107,87,0.35);
      background: rgba(15,107,87,0.08);
      color: #0d5848;
      font-size: 11px;
      white-space: nowrap;
    }}
    .questions {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }}
    .question-band, .panel {{ padding: 16px; }}
    .question-band ol {{ margin: 0; padding-left: 20px; }}
    .question-band li {{ margin: 0 0 10px; }}
    .node-id {{ color: var(--muted); font-size: 11px; }}
    .synthesis {{ display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(260px, 0.8fr); gap: 18px; align-items: start; }}
    .panel ul {{ margin: 0; padding-left: 20px; }}
    @media (max-width: 860px) {{
      main {{ padding: 28px 16px 48px; }}
      h1 {{ font-size: 34px; }}
      .metrics, .questions, .synthesis {{ grid-template-columns: 1fr; }}
    }}
    @media print {{
      body {{ background: white; }}
      main {{ max-width: none; padding: 18px; }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <div class="eyebrow">FengHe Research Graph</div>
      <h1>{escape(ticker)} Forward Research Graph Report</h1>
      <div class="meta">
        <span>Generated At: {escape(generated_at)}</span>
        <span>Output: HTML</span>
        <span>Graph: nodes.jsonl + edges.jsonl</span>
      </div>
      <div class="notice">Do not treat this as a trading instruction. Baseline rule: assume known facts and market consensus are already reflected in price until a change hypothesis survives evidence testing.</div>
    </section>

    <section class="metrics">
      <div class="metric"><strong>{len(graph.nodes())}</strong><span>graph nodes</span></div>
      <div class="metric"><strong>{len(graph.edges())}</strong><span>graph edges</span></div>
      <div class="metric"><strong>{len(evidence)}</strong><span>evidence records</span></div>
      <div class="metric"><strong>{seeded_tests}</strong><span>evidence-seeded tests</span></div>
    </section>

    <section>
      <h2>市场共识基线</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Dimension</th><th>Status</th><th>Baseline Statement</th><th>Evidence</th></tr></thead>
          <tbody>{consensus_html}</tbody>
        </table>
      </div>
    </section>

    <section>
      <h2>Forward Questions By 3T</h2>
      <div class="questions">{question_html}</div>
    </section>

    <section>
      <h2>Hypothesis And Assumption Tests</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Assumption</th><th>Frame</th><th>Verdict</th><th>Evidence</th></tr></thead>
          <tbody>{assumption_html}</tbody>
        </table>
      </div>
    </section>

    <section class="synthesis">
      <div class="panel">
        <h2>FengHe Synthesis</h2>
        <ul>
          <li>3C: Cycle, Change, and Certainty remain research questions until the graph gains fresher evidence and disconfirming tests.</li>
          <li>Dominant D driver: D2 candidate for forward work, because the graph is organized around change versus priced consensus; confidence is low until assumptions are tested.</li>
          <li>Key 5M focus: M3 margin and M4 model are the first local evidence-backed checks when SEC operating and balance sheet facts exist.</li>
          <li>Active 3T time frame: T2 candidate, because earnings revision and margin/share confirmation usually need 3-15 months of evidence.</li>
          <li>Evidence base: {len(evidence)} records loaded, including {primary_evidence_count} primary records.</li>
        </ul>
      </div>
      <div class="panel">
        <h2>Disconfirming Tests</h2>
        <ul>
          <li>Fresh primary filings fail to confirm the assumed direction of change.</li>
          <li>Management commentary contradicts the mechanism behind the hypothesis.</li>
          <li>Market data shows the expected change was already priced before the evidence arrived.</li>
          <li>A competing 5M defect explains the observed data better than the favored hypothesis.</li>
        </ul>
        <h2>Human Review Actions</h2>
        <ul>
          <li>Add fresh price, valuation, estimate, and transcript evidence before strengthening any conclusion.</li>
          <li>Attach explicit disconfirming evidence IDs when a hypothesis is rejected.</li>
          <li>Promote only hypotheses with a clear dominant D driver, matching 3T frame, and tested assumptions.</li>
        </ul>
      </div>
    </section>
  </main>
</body>
</html>
"""


def _render_evidence_chips(evidence_ids: list[str]) -> str:
    if not evidence_ids:
        return '<span class="status gap">needs_evidence</span>'
    return " ".join(
        f'<span class="evidence-chip">{escape(evidence_id)}</span>'
        for evidence_id in evidence_ids
    )


def _status_class(status: str) -> str:
    return "ok" if status in {"baseline_evidenced", "evidence_seeded"} else "gap"


def _render_consensus_row(node: dict[str, Any]) -> str:
    props = node["properties"]
    status = props["status"]
    return (
        "<tr>"
        f"<td><strong>{escape(node['label'])}</strong><br><span class=\"node-id\">{escape(node['id'])}</span></td>"
        f"<td><span class=\"status {_status_class(status)}\">{escape(status)}</span></td>"
        f"<td>{escape(props['statement'])}</td>"
        f"<td>{_render_evidence_chips(props['evidence_ids'])}</td>"
        "</tr>"
    )


def _render_question_section(time_frame: str, question_nodes: list[dict[str, Any]]) -> str:
    items = []
    for node in question_nodes:
        props = node["properties"]
        if props["time_frame"] != time_frame:
            continue
        items.append(
            "<li>"
            f"{escape(props['question'])} "
            f"<span class=\"node-id\">{escape(node['id'])} / Driver: {escape(props['linked_driver'])}</span>"
            "</li>"
        )
    return (
        '<div class="question-band">'
        f"<h3>{escape(time_frame)}</h3>"
        f"<ol>{''.join(items)}</ol>"
        "</div>"
    )


def _render_assumption_row(node: dict[str, Any]) -> str:
    props = node["properties"]
    verdict = props["verdict"]
    return (
        "<tr>"
        f"<td>{escape(props['assumption'])}<br><span class=\"node-id\">{escape(node['id'])}</span></td>"
        f"<td>{escape(props['time_frame'])}<br>{escape(props['dimension'])}</td>"
        f"<td><span class=\"status {_status_class(verdict)}\">{escape(verdict)}</span></td>"
        f"<td>{_render_evidence_chips(props['supporting_evidence_ids'])}</td>"
        "</tr>"
    )
