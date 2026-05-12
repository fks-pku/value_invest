import json
import unittest
from pathlib import Path

from tests.helpers import project_tmp_dir
from value_invest_research.research_graph import run_research_graph_stage
from value_invest_research.scaffold import init_stock


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class ResearchGraphTests(unittest.TestCase):
    def _seed_aapl(self, root: Path) -> Path:
        stock_dir = init_stock(root, "AAPL", "Apple Inc.")
        evidence = {
            "id": "ev_aapl_sec_revenue_20260328",
            "research_object": "stocks/AAPL",
            "source_type": "sec_fact",
            "source_name": "SEC XBRL Revenue",
            "url": "local://stocks/AAPL/data/sec_facts.json",
            "published_at": "2026-05-01T00:00:00Z",
            "fetched_at": "2026-05-08T17:46:28+00:00",
            "hash": "sha256:test",
            "tickers": ["AAPL"],
            "sectors": [],
            "themes": [],
            "summary": "Revenue was 111184000000 USD for period ending 2026-03-28 in 10-Q.",
            "reliability": "primary",
            "materiality": "medium",
            "used_in": [],
        }
        (stock_dir / "evidence.jsonl").write_text(json.dumps(evidence) + "\n", encoding="utf-8")
        return stock_dir

    def test_full_research_graph_writes_nodes_edges_and_forward_report(self):
        with project_tmp_dir() as tmp:
            stock_dir = self._seed_aapl(tmp)

            result = run_research_graph_stage(tmp, "AAPL", "report")

            graph_dir = stock_dir / "research_graph"
            nodes = _read_jsonl(graph_dir / "nodes.jsonl")
            edges = _read_jsonl(graph_dir / "edges.jsonl")
            node_types = {node["type"] for node in nodes}
            edge_relations = {edge["relation"] for edge in edges}

            self.assertEqual(result["ticker"], "AAPL")
            self.assertTrue(result["report_path"].endswith("forward_report.html"))
            self.assertIn("consensus", node_types)
            self.assertIn("question", node_types)
            self.assertIn("hypothesis", node_types)
            self.assertIn("assumption_test", node_types)
            self.assertIn("evidence", node_types)
            self.assertIn("framework_dimension", node_types)
            self.assertIn("time_frame", node_types)
            self.assertIn("supports_baseline", edge_relations)
            self.assertIn("frames_hypothesis", edge_relations)
            self.assertIn("depends_on", edge_relations)
            self.assertIn("tests_with", edge_relations)

            report = (graph_dir / "forward_report.html").read_text(encoding="utf-8")
            self.assertIn("<!doctype html>", report.lower())
            self.assertIn("市场共识基线", report)
            self.assertIn("Dominant D driver", report)
            self.assertIn("ev_aapl_sec_revenue_20260328", report)
            self.assertIn("Do not treat this as a trading instruction", report)
            self.assertIn(".evidence-chip", report)

    def test_research_graph_stage_outputs_are_incremental(self):
        with project_tmp_dir() as tmp:
            stock_dir = self._seed_aapl(tmp)

            consensus = run_research_graph_stage(tmp, "AAPL", "consensus")
            consensus_nodes = _read_jsonl(stock_dir / "research_graph" / "nodes.jsonl")
            self.assertGreater(consensus["nodes"], 0)
            self.assertIn("consensus", {node["type"] for node in consensus_nodes})
            self.assertNotIn("question", {node["type"] for node in consensus_nodes})

            questions = run_research_graph_stage(tmp, "AAPL", "questions")
            question_nodes = _read_jsonl(stock_dir / "research_graph" / "nodes.jsonl")
            self.assertGreater(questions["nodes"], consensus["nodes"])
            self.assertIn("question", {node["type"] for node in question_nodes})

    def test_research_graph_accepts_common_aapl_typo(self):
        with project_tmp_dir() as tmp:
            self._seed_aapl(tmp)

            result = run_research_graph_stage(tmp, "APPL", "consensus")

            self.assertEqual(result["ticker"], "AAPL")


if __name__ == "__main__":
    unittest.main()
