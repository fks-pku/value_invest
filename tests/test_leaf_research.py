import json
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.helpers import project_tmp_dir
from value_invest_research.leaf_research import (
    build_leaf_research_tasks,
    import_leaf_research_results,
    rollup_research_answers,
    run_leaf_research,
    synthesize_leaf_answers,
)
from value_invest_research.research_system import build_research_system
from value_invest_research.scaffold import init_stock


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class _FakeHttpResponse:
    def __init__(self, body: dict):
        self._body = json.dumps(body, ensure_ascii=False).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self) -> bytes:
        return self._body


def _evidence_record(record_id: str, summary: str) -> dict:
    return {
        "id": record_id,
        "research_object": "stocks/XIAOMI",
        "source_type": "annual_report",
        "source_name": "Xiaomi Annual Report",
        "url": "https://example.com/xiaomi-annual-report",
        "published_at": "2026-04-28T00:00:00Z",
        "fetched_at": "2026-05-23T00:00:00+08:00",
        "hash": f"sha256:{record_id}",
        "tickers": ["XIAOMI"],
        "sectors": [],
        "themes": [],
        "summary": summary,
        "reliability": "primary",
        "materiality": "high",
        "used_in": [],
    }


class LeafResearchTests(unittest.TestCase):
    def _seed_xiaomi(self, root: Path) -> Path:
        stock_dir = init_stock(root, "XIAOMI", "Xiaomi Corporation")
        evidence = [
            _evidence_record(
                "ev_xiaomi_profile",
                "Xiaomi was founded in 2010 and operates consumer electronics, smartphone, IoT, internet services, and EV businesses.",
            ),
            _evidence_record(
                "ev_xiaomi_financials",
                "FY2025 revenue, gross margin, operating cash flow, capex, smartphone shipments, EV deliveries, and internet services MAU are disclosed.",
            ),
        ]
        (stock_dir / "evidence.jsonl").write_text(
            "\n".join(json.dumps(row, ensure_ascii=False) for row in evidence) + "\n",
            encoding="utf-8",
        )
        return stock_dir

    def test_build_leaf_research_tasks_from_stock_qa_tree(self):
        with project_tmp_dir("leaf_tasks") as tmp:
            stock_dir = self._seed_xiaomi(tmp)

            result = build_leaf_research_tasks(tmp, "XIAOMI", limit=2)

            research_dir = stock_dir / "research_system"
            task_path = research_dir / "leaf_research_tasks.jsonl"
            tasks = _read_jsonl(task_path)
            self.assertEqual(result["ticker"], "XIAOMI")
            self.assertEqual(result["tasks"], 2)
            self.assertEqual(result["task_path"], str(task_path))
            self.assertEqual(len(tasks), 2)
            self.assertEqual(tasks[0]["ticker"], "XIAOMI")
            self.assertEqual(tasks[0]["company_name"], "Xiaomi Corporation")
            self.assertTrue(tasks[0]["task_id"].startswith("leaf_"))
            self.assertIn("node_id", tasks[0])
            self.assertIn("question", tasks[0])
            self.assertIn("parent_question", tasks[0])
            self.assertIn("framework_context", tasks[0])
            self.assertIn("required_evidence", tasks[0])
            self.assertIn("disconfirming_signals", tasks[0])
            self.assertIn("decision_rule", tasks[0])
            self.assertEqual(tasks[0]["information_categories"], ["evidence", "research_report", "message", "opinion"])
            self.assertEqual(tasks[0]["refresh_policy"], "skip_if_complete")

    def test_run_leaf_research_with_mock_provider_writes_raw_and_results(self):
        with project_tmp_dir("leaf_mock") as tmp:
            stock_dir = self._seed_xiaomi(tmp)

            result = run_leaf_research(tmp, "XIAOMI", provider="mock", limit=1)

            research_dir = stock_dir / "research_system"
            result_path = research_dir / "leaf_research_results.jsonl"
            raw_dir = research_dir / "leaf_research_raw"
            rows = _read_jsonl(result_path)
            self.assertEqual(result["ticker"], "XIAOMI")
            self.assertEqual(result["provider"], "mock")
            self.assertEqual(result["results"], 1)
            self.assertEqual(result["result_path"], str(result_path))
            self.assertTrue(raw_dir.exists())
            self.assertEqual(len(list(raw_dir.glob("*.json"))), 1)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["provider"], "mock")
            self.assertEqual(rows[0]["provider_model"], "mock-leaf-research-v1")
            self.assertEqual(rows[0]["sources"][0]["information_category"], "research_report")
            self.assertIn("Mock answer", rows[0]["answer"])
            self.assertTrue(rows[0]["raw_response_path"].endswith(".json"))

    def test_perplexity_provider_requires_api_key(self):
        with project_tmp_dir("leaf_perplexity_key") as tmp:
            self._seed_xiaomi(tmp)

            with patch.dict("os.environ", {}, clear=True):
                with self.assertRaisesRegex(ValueError, "PERPLEXITY_API_KEY"):
                    run_leaf_research(tmp, "XIAOMI", provider="perplexity", limit=1)

    def test_openai_compatible_provider_requires_generic_api_key(self):
        with project_tmp_dir("leaf_openai_compatible_key") as tmp:
            self._seed_xiaomi(tmp)

            with patch.dict("os.environ", {}, clear=True):
                with self.assertRaisesRegex(ValueError, "LEAF_RESEARCH_API_KEY"):
                    run_leaf_research(tmp, "XIAOMI", provider="openai_compatible", limit=1)

    def test_exa_provider_requires_api_key(self):
        with project_tmp_dir("leaf_exa_key") as tmp:
            self._seed_xiaomi(tmp)

            with patch.dict("os.environ", {}, clear=True):
                with self.assertRaisesRegex(ValueError, "EXA_API_KEY"):
                    run_leaf_research(tmp, "XIAOMI", provider="exa", limit=1)

    def test_run_leaf_research_with_perplexity_provider_writes_cited_results(self):
        with project_tmp_dir("leaf_perplexity") as tmp:
            stock_dir = self._seed_xiaomi(tmp)
            captured = {}
            provider_json = {
                "answer": "Perplexity answer: supplier power should be tested with official filings and third-party margin data.",
                "facts": ["Perplexity fact: the cited filing is primary evidence."],
                "inferences": ["Perplexity inference: supplier power affects margin durability."],
                "judgment": "Perplexity judgment: provisional until more source categories are collected.",
                "supporting_evidence": ["SEC filing supports the baseline."],
                "refuting_evidence": [],
                "research_leads": ["Search for customer and supplier concentration."],
                "gaps": ["Need supplier concentration and purchase commitment data."],
                "confidence": "medium",
                "sources": [
                    {
                        "url": "https://www.sec.gov/Archives/example/xiaomi-filing.htm",
                        "title": "Xiaomi Filing",
                        "publisher": "SEC",
                        "published_at": "2026-05-01",
                        "source_type": "annual_report",
                        "information_category": "evidence",
                        "reliability": "primary",
                        "materiality": "high",
                        "summary": "Official filing summary.",
                        "quoted_or_extracted_points": ["Revenue and cash-flow data."],
                    }
                ],
            }
            response = {
                "id": "sonar-test",
                "model": "sonar-pro",
                "choices": [{"message": {"content": json.dumps(provider_json, ensure_ascii=False)}}],
                "search_results": [
                    {
                        "title": "Xiaomi Filing",
                        "url": "https://www.sec.gov/Archives/example/xiaomi-filing.htm",
                        "date": "2026-05-01",
                    }
                ],
                "citations": ["https://www.sec.gov/Archives/example/xiaomi-filing.htm"],
            }

            def fake_urlopen(request, timeout=0):
                captured["url"] = request.full_url
                captured["headers"] = dict(request.header_items())
                captured["payload"] = json.loads(request.data.decode("utf-8"))
                captured["timeout"] = timeout
                return _FakeHttpResponse(response)

            with patch.dict("os.environ", {"PERPLEXITY_API_KEY": "test-key"}, clear=True):
                with patch("value_invest_research.adapters.outbound.research_search_providers.urllib.request.urlopen", side_effect=fake_urlopen):
                    result = run_leaf_research(tmp, "XIAOMI", provider="perplexity", limit=1)

            research_dir = stock_dir / "research_system"
            rows = _read_jsonl(research_dir / "leaf_research_results.jsonl")
            self.assertEqual(result["provider"], "perplexity")
            self.assertEqual(result["results"], 1)
            self.assertEqual(captured["url"], "https://api.perplexity.ai/chat/completions")
            self.assertEqual(captured["payload"]["model"], "sonar-pro")
            self.assertIn("messages", captured["payload"])
            self.assertEqual(rows[0]["provider"], "perplexity")
            self.assertEqual(rows[0]["provider_model"], "sonar-pro")
            self.assertIn("Perplexity answer", rows[0]["answer"])
            self.assertEqual(rows[0]["sources"][0]["information_category"], "evidence")
            self.assertTrue((research_dir / "leaf_research_raw" / f"{rows[0]['task_id']}.json").exists())

    def test_run_leaf_research_with_openai_compatible_provider_uses_generic_config(self):
        with project_tmp_dir("leaf_openai_compatible") as tmp:
            stock_dir = self._seed_xiaomi(tmp)
            captured = {}
            provider_json = {
                "answer": "Generic compatible answer: source-backed answer from a configurable search model.",
                "facts": ["Generic fact: the source is cited."],
                "inferences": ["Generic inference: provider specifics stay outside the core schema."],
                "judgment": "Generic judgment: provider-agnostic pipeline is usable.",
                "supporting_evidence": ["Generic source supports the answer."],
                "refuting_evidence": [],
                "research_leads": [],
                "gaps": ["Need live provider verification."],
                "confidence": "medium",
                "sources": [
                    {
                        "url": "https://research.example.com/xiaomi-source",
                        "title": "Generic Search Source",
                        "publisher": "Research Example",
                        "published_at": "2026-05-01",
                        "source_type": "research_report",
                        "information_category": "research_report",
                        "reliability": "high",
                        "materiality": "medium",
                        "summary": "Generic search source summary.",
                        "quoted_or_extracted_points": ["Provider-agnostic evidence point."],
                    }
                ],
            }
            response = {
                "id": "compatible-test",
                "model": "search-model",
                "choices": [{"message": {"content": json.dumps(provider_json, ensure_ascii=False)}}],
            }

            def fake_urlopen(request, timeout=0):
                captured["url"] = request.full_url
                captured["headers"] = dict(request.header_items())
                captured["payload"] = json.loads(request.data.decode("utf-8"))
                captured["timeout"] = timeout
                return _FakeHttpResponse(response)

            env = {
                "LEAF_RESEARCH_API_KEY": "generic-key",
                "LEAF_RESEARCH_BASE_URL": "https://search.example.com/v1",
                "LEAF_RESEARCH_MODEL": "search-model",
                "LEAF_RESEARCH_PROVIDER_NAME": "custom_search",
            }
            with patch.dict("os.environ", env, clear=True):
                with patch("value_invest_research.adapters.outbound.research_search_providers.urllib.request.urlopen", side_effect=fake_urlopen):
                    result = run_leaf_research(tmp, "XIAOMI", provider="openai_compatible", limit=1)

            rows = _read_jsonl(stock_dir / "research_system" / "leaf_research_results.jsonl")
            self.assertEqual(result["provider"], "openai_compatible")
            self.assertEqual(captured["url"], "https://search.example.com/v1/chat/completions")
            self.assertEqual(captured["payload"]["model"], "search-model")
            self.assertEqual(rows[0]["provider"], "custom_search")
            self.assertEqual(rows[0]["provider_model"], "search-model")
            self.assertIn("Generic compatible answer", rows[0]["answer"])
            self.assertEqual(rows[0]["sources"][0]["information_category"], "research_report")

    def test_run_leaf_research_with_exa_provider_writes_source_discovery_results(self):
        with project_tmp_dir("leaf_exa") as tmp:
            stock_dir = self._seed_xiaomi(tmp)
            captured = {}
            response = {
                "requestId": "exa-test",
                "results": [
                    {
                        "title": "Micron HBM Outlook",
                        "url": "https://investors.micron.com/news-releases/news-release-details/micron-hbm-outlook",
                        "publishedDate": "2026-01-08T00:00:00.000Z",
                        "author": "Micron",
                        "text": "Micron described HBM demand, product ramps, and data center memory growth.",
                        "highlights": ["HBM demand and data center memory growth are increasing."],
                    }
                ],
            }

            def fake_urlopen(request, timeout=0):
                captured["url"] = request.full_url
                captured["headers"] = {key.lower(): value for key, value in request.header_items()}
                captured["payload"] = json.loads(request.data.decode("utf-8"))
                captured["timeout"] = timeout
                return _FakeHttpResponse(response)

            env = {
                "EXA_API_KEY": "test-exa-key",
                "EXA_NUM_RESULTS": "2",
                "EXA_SEARCH_TYPE": "auto",
            }
            with patch.dict("os.environ", env, clear=True):
                with patch("value_invest_research.adapters.outbound.research_search_providers.urllib.request.urlopen", side_effect=fake_urlopen):
                    result = run_leaf_research(tmp, "XIAOMI", provider="exa", limit=1)

            rows = _read_jsonl(stock_dir / "research_system" / "leaf_research_results.jsonl")
            self.assertEqual(result["provider"], "exa")
            self.assertEqual(captured["url"], "https://api.exa.ai/search")
            self.assertEqual(captured["headers"]["x-api-key"], "test-exa-key")
            self.assertEqual(captured["payload"]["type"], "auto")
            self.assertEqual(captured["payload"]["numResults"], 2)
            self.assertIn("contents", captured["payload"])
            self.assertEqual(rows[0]["provider"], "exa")
            self.assertEqual(rows[0]["provider_model"], "exa-search-auto")
            self.assertIn("source discovery", rows[0]["answer"].lower())
            self.assertEqual(rows[0]["sources"][0]["information_category"], "evidence")
            self.assertEqual(rows[0]["sources"][0]["publisher"], "investors.micron.com")
            self.assertIn("HBM demand", rows[0]["sources"][0]["quoted_or_extracted_points"][0])

    def test_import_leaf_research_results_normalizes_manual_rows(self):
        with project_tmp_dir("leaf_manual") as tmp:
            stock_dir = self._seed_xiaomi(tmp)
            task_result = build_leaf_research_tasks(tmp, "XIAOMI", limit=1)
            task = _read_jsonl(Path(task_result["task_path"]))[0]
            manual_path = tmp / "manual_leaf_results.jsonl"
            manual_row = {
                "provider": "manual",
                "provider_model": "analyst-note",
                "task_id": task["task_id"],
                "node_id": task["node_id"],
                "query": task["question"],
                "answer": "Manual answer: Xiaomi profit quality depends on segment margins and cash conversion.",
                "facts": ["Manual fact: annual report discloses revenue and operating cash flow."],
                "inferences": ["Manual inference: cash conversion is a required validation bridge."],
                "judgment": "Manual judgment: provisional until segment margin details are verified.",
                "supporting_evidence": ["Annual report supports the cash-flow baseline."],
                "refuting_evidence": [],
                "research_leads": ["Search for segment-level margin bridges."],
                "gaps": ["Need supplier and channel bargaining-power data."],
                "confidence": "medium",
                "sources": [
                    {
                        "url": "https://example.com/manual-source",
                        "title": "Manual Source",
                        "publisher": "Example Research",
                        "author": "Analyst",
                        "published_at": "2026-05-01T00:00:00Z",
                        "source_type": "research_report",
                        "information_category": "research_report",
                        "reliability": "high",
                        "materiality": "medium",
                        "summary": "Manual summary of the source.",
                        "quoted_or_extracted_points": ["Segment margin bridge is required."],
                    }
                ],
            }
            manual_path.write_text(json.dumps(manual_row, ensure_ascii=False) + "\n", encoding="utf-8")

            result = import_leaf_research_results(tmp, "XIAOMI", manual_path)

            research_dir = stock_dir / "research_system"
            rows = _read_jsonl(research_dir / "leaf_research_results.jsonl")
            self.assertEqual(result["ticker"], "XIAOMI")
            self.assertEqual(result["records"], 1)
            self.assertEqual(result["sources"], 1)
            self.assertEqual(result["result_path"], str(research_dir / "leaf_research_results.jsonl"))
            self.assertEqual(rows[0]["provider"], "manual")
            self.assertEqual(rows[0]["sources"][0]["url"], "https://example.com/manual-source")
            self.assertIn("executed_at", rows[0])

    def test_import_deduplicates_sources_and_preserves_node_bindings(self):
        with project_tmp_dir("leaf_sources") as tmp:
            stock_dir = self._seed_xiaomi(tmp)
            task_result = build_leaf_research_tasks(tmp, "XIAOMI", limit=2)
            tasks = _read_jsonl(Path(task_result["task_path"]))
            shared_url = "https://example.com/shared-source"
            manual_path = tmp / "manual_duplicate_sources.jsonl"
            rows = []
            for task in tasks:
                rows.append(
                    {
                        "provider": "manual",
                        "provider_model": "analyst-note",
                        "task_id": task["task_id"],
                        "node_id": task["node_id"],
                        "query": task["question"],
                        "answer": f"Manual answer for {task['node_id']}",
                        "facts": [f"Fact for {task['node_id']}"],
                        "inferences": ["Inference from shared source."],
                        "judgment": "Judgment remains provisional.",
                        "supporting_evidence": ["Shared source supports the baseline."],
                        "refuting_evidence": [],
                        "research_leads": [],
                        "gaps": ["Need direct company filings."],
                        "confidence": "medium",
                        "sources": [
                            {
                                "url": shared_url,
                                "title": "Shared Source",
                                "publisher": "Example Research",
                                "published_at": "2026-05-01T00:00:00Z",
                                "source_type": "research_report",
                                "information_category": "research_report",
                                "reliability": "high",
                                "materiality": "medium",
                                "summary": "Shared source summary.",
                                "quoted_or_extracted_points": ["Shared source point."],
                            }
                        ],
                    }
                )
            manual_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")

            import_leaf_research_results(tmp, "XIAOMI", manual_path)

            sources = _read_jsonl(stock_dir / "research_system" / "leaf_research_sources.jsonl")
            self.assertEqual(len(sources), 1)
            self.assertEqual(sources[0]["url"], shared_url)
            self.assertEqual(sorted(sources[0]["node_ids"]), sorted([task["node_id"] for task in tasks]))
            self.assertEqual(sources[0]["result_count"], 2)

    def test_synthesize_leaf_answers_preserves_facts_inferences_judgment(self):
        with project_tmp_dir("leaf_answers") as tmp:
            stock_dir = self._seed_xiaomi(tmp)

            run_leaf_research(tmp, "XIAOMI", provider="mock", limit=1)
            result = synthesize_leaf_answers(tmp, "XIAOMI")

            research_dir = stock_dir / "research_system"
            answers = _read_jsonl(research_dir / "leaf_answers.jsonl")
            self.assertEqual(result["answers"], 1)
            self.assertEqual(result["answer_path"], str(research_dir / "leaf_answers.jsonl"))
            self.assertEqual(len(answers), 1)
            self.assertIn("facts", answers[0])
            self.assertIn("inferences", answers[0])
            self.assertIn("judgment", answers[0])
            self.assertIn("supporting_evidence", answers[0])
            self.assertIn("refuting_evidence", answers[0])
            self.assertIn("research_leads", answers[0])
            self.assertEqual(answers[0]["source"], "leaf_research")
            self.assertEqual(answers[0]["source_balance"], "证据 0 / 研报 1 / 消息 0 / 观点 0")
            self.assertIn("Mock answer", answers[0]["answer"])

    def test_leaf_batches_accumulate_results_and_answers_without_losing_prior_nodes(self):
        with project_tmp_dir("leaf_accumulate") as tmp:
            stock_dir = self._seed_xiaomi(tmp)
            research_dir = stock_dir / "research_system"

            run_leaf_research(tmp, "XIAOMI", provider="mock", limit=1)
            synthesize_leaf_answers(tmp, "XIAOMI")
            first_results = _read_jsonl(research_dir / "leaf_research_results.jsonl")
            first_answers = _read_jsonl(research_dir / "leaf_answers.jsonl")

            run_leaf_research(tmp, "XIAOMI", provider="mock", limit=1)
            synthesize_leaf_answers(tmp, "XIAOMI")

            results = _read_jsonl(research_dir / "leaf_research_results.jsonl")
            answers = _read_jsonl(research_dir / "leaf_answers.jsonl")
            self.assertEqual(len(first_results), 1)
            self.assertEqual(len(first_answers), 1)
            self.assertEqual(len(results), 2)
            self.assertEqual(len(answers), 2)
            self.assertIn(first_results[0]["node_id"], {row["node_id"] for row in results})
            self.assertIn(first_answers[0]["node_id"], {row["node_id"] for row in answers})
            self.assertEqual(len({row["node_id"] for row in results}), 2)

    def test_build_research_system_applies_leaf_answers_and_rolls_up_parent(self):
        with project_tmp_dir("leaf_bind") as tmp:
            stock_dir = self._seed_xiaomi(tmp)

            run_leaf_research(tmp, "XIAOMI", provider="mock", limit=1)
            synthesize_leaf_answers(tmp, "XIAOMI")
            build_research_system(tmp, "XIAOMI")

            qa_tree = json.loads((stock_dir / "research_system" / "qa_tree.json").read_text(encoding="utf-8"))
            answers = _read_jsonl(stock_dir / "research_system" / "leaf_answers.jsonl")
            target_node = answers[0]["node_id"]
            node = next(item for item in qa_tree["nodes"] if item["id"] == target_node)
            parent = next(item for item in qa_tree["nodes"] if item["id"] == node["parent_id"])
            self.assertEqual(node["professional_answer"]["source"], "leaf_research")
            self.assertEqual(node["metadata"]["synthesis_override"]["source"], "leaf_research")
            self.assertIn("Mock answer", node["professional_answer"]["answer"])
            self.assertIn("leaf_research", parent["metadata"]["rollup_sources"])
            self.assertIn("Mock answer", parent["professional_answer"]["answer"])

    def test_leaf_research_sources_are_visible_in_qa_tree_and_l3_html(self):
        with project_tmp_dir("leaf_source_render") as tmp:
            stock_dir = self._seed_xiaomi(tmp)

            run_leaf_research(tmp, "XIAOMI", provider="mock", limit=1)
            synthesize_leaf_answers(tmp, "XIAOMI")
            build_research_system(tmp, "XIAOMI")

            research_dir = stock_dir / "research_system"
            qa_tree = json.loads((research_dir / "qa_tree.json").read_text(encoding="utf-8"))
            answer = _read_jsonl(research_dir / "leaf_answers.jsonl")[0]
            node = next(item for item in qa_tree["nodes"] if item["id"] == answer["node_id"])
            leaf_sources = node["professional_answer"]["leaf_sources"]
            html = "\n".join(path.read_text(encoding="utf-8") for path in (research_dir / "pages").rglob("*.html"))

            self.assertEqual(len(leaf_sources), 1)
            self.assertEqual(leaf_sources[0]["url"], answer["source_index"][0]["url"])
            self.assertEqual(leaf_sources[0]["information_category"], "research_report")
            self.assertIn("Leaf 深研来源", html)
            self.assertIn("Mock source for", html)
            self.assertIn(leaf_sources[0]["url"], html)

    def test_rollup_research_answers_writes_parent_rollups(self):
        with project_tmp_dir("leaf_rollup") as tmp:
            stock_dir = self._seed_xiaomi(tmp)

            run_leaf_research(tmp, "XIAOMI", provider="mock", limit=1)
            synthesize_leaf_answers(tmp, "XIAOMI")
            result = rollup_research_answers(tmp, "XIAOMI")

            rollups = _read_jsonl(stock_dir / "research_system" / "rollup_answers.jsonl")
            self.assertEqual(result["rollup_path"], str(stock_dir / "research_system" / "rollup_answers.jsonl"))
            self.assertGreater(result["rollups"], 0)
            self.assertTrue(any("leaf_research" in row.get("rollup_sources", []) for row in rollups))
            self.assertTrue(all("node_id" in row and "answer" in row for row in rollups))


if __name__ == "__main__":
    unittest.main()
