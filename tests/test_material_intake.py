import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from value_invest_research.adapters.outbound.filesystem_material_intake import (
    FileSystemMaterialIntakeRepository,
    FileSystemMaterialIntakeValidationRepository,
)
from value_invest_research.adapters.outbound.ima_knowledge_base_feed import (
    ImaKnowledgeBaseFeed,
)
from value_invest_research.application.use_cases.ingest_materials import (
    ingest_material_batch,
    scan_knowledge_base_materials,
)
from value_invest_research.application.use_cases.validate_material_intake import (
    ValidateMaterialIntake,
)
from value_invest_research.domain.material_intake import (
    apply_time_slice_policy,
    build_material_parse_tasks,
    infer_material_class,
    normalize_material_document,
)


class FakeUrlResponse:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return self.payload


class FakeKnowledgeBaseFeed:
    provider_name = "ima"

    def search_materials(self, *, knowledge_base_id, query, max_results):
        return [
            {
                "external_id": "report-1",
                "title": "AI GPU 与 HBM 产业深度研报",
                "published_at": "2026-07-20",
                "source_type": "research_report_pdf",
                "summary": f"匹配查询：{query}",
                "knowledge_base_id": knowledge_base_id,
            }
        ][:max_results]


class MaterialIntakeTests(unittest.TestCase):
    def test_material_classification_is_more_granular_than_source_bucket(self):
        self.assertEqual(
            infer_material_class(
                {
                    "title": "Company FY2025 Annual Report",
                    "source_type": "annual_report",
                }
            ),
            "official_filing",
        )
        self.assertEqual(
            infer_material_class(
                {"title": "AI Hardware Equity Research", "source_type": "sell_side_report"}
            ),
            "sell_side_research",
        )
        self.assertEqual(
            infer_material_class(
                {"title": "Omdia AI Processor Forecast", "source_type": "industry_data"}
            ),
            "authoritative_third_party",
        )
        self.assertEqual(
            infer_material_class(
                {"title": "供应链最新消息", "source_type": "news"}
            ),
            "market_news",
        )

    def test_question_search_creates_only_one_question_parse_task(self):
        document = normalize_material_document(
            {
                "external_id": "exa-1",
                "title": "Micron HBM outlook",
                "published_at": "2026-03-01",
                "source_type": "company_ir",
            },
            ingestion_channel="question_search",
            provider="exa",
            discovered_at="2026-03-02",
            default_bom_node_ids=["memory"],
            default_question_numbers=[2],
        )

        tasks = build_material_parse_tasks(document)

        self.assertEqual(document["material_class"], "official_company")
        self.assertEqual(document["source_bucket"], "evidence")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["question_number"], 2)
        self.assertEqual(tasks[0]["preferred_parser"], "deepseek")

    def test_historical_project_quarantines_post_cutoff_material(self):
        document = normalize_material_document(
            {
                "external_id": "ima-new",
                "title": "Post-cutoff HBM research report",
                "published_at": "2026-07-20",
                "source_type": "research_report",
            },
            ingestion_channel="knowledge_base_scan",
            provider="ima",
            discovered_at="2026-07-21",
            default_bom_node_ids=["memory"],
        )

        quarantined = apply_time_slice_policy(
            document,
            mode="historical_backtest",
            as_of_date="2026-03-28",
        )

        self.assertEqual(
            quarantined["mapping_status"],
            "quarantined_post_cutoff",
        )
        self.assertEqual(quarantined["allowed_usage"], "quarantine_only")
        self.assertEqual(build_material_parse_tasks(quarantined), [])

    def test_ima_scan_routes_report_to_each_matching_bom_and_is_idempotent(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            for node_id in ("compute", "memory"):
                (project_dir / "boms" / node_id).mkdir(parents=True)
            (project_dir / "project.json").write_text(
                json.dumps(
                    {
                        "mode": "live_prediction",
                        "as_of_date": "2026-07-21",
                    }
                ),
                encoding="utf-8",
            )
            (project_dir / "boms" / "manifest.json").write_text(
                json.dumps(
                    {
                        "nodes": [
                            {"node_id": "compute"},
                            {"node_id": "memory"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            repository = FileSystemMaterialIntakeRepository(project_dir)
            kwargs = {
                "feed": FakeKnowledgeBaseFeed(),
                "repository": repository,
                "knowledge_base_id": "kb-test",
                "bom_queries": {
                    "compute": ["GPU"],
                    "memory": ["HBM"],
                },
                "known_bom_node_ids": ["compute", "memory"],
                "mode": "live_prediction",
                "as_of_date": "2026-07-21",
                "discovered_at": "2026-07-21",
                "max_results_per_query": 10,
            }

            first = scan_knowledge_base_materials(**kwargs)
            second = scan_knowledge_base_materials(**kwargs)

            documents = [
                json.loads(line)
                for line in (
                    project_dir / "material_intake" / "documents.jsonl"
                ).read_text(encoding="utf-8").splitlines()
            ]
            compute_tasks = [
                json.loads(line)
                for line in (
                    project_dir / "boms" / "compute" / "inbox" / "parse_tasks.jsonl"
                ).read_text(encoding="utf-8").splitlines()
            ]
            memory_tasks = [
                json.loads(line)
                for line in (
                    project_dir / "boms" / "memory" / "inbox" / "parse_tasks.jsonl"
                ).read_text(encoding="utf-8").splitlines()
            ]

            self.assertEqual(first["new_documents"], 2)
            self.assertEqual(first["parse_tasks"], 12)
            self.assertEqual(second["new_documents"], 0)
            self.assertEqual(len(documents), 1)
            self.assertEqual(
                set(documents[0]["matched_bom_node_ids"]),
                {"compute", "memory"},
            )
            self.assertEqual(len(compute_tasks), 6)
            self.assertEqual(len(memory_tasks), 6)
            persisted_text = (
                project_dir / "material_intake" / "feed_state.json"
            ).read_text(encoding="utf-8")
            self.assertNotIn("kb-test", persisted_text)
            self.assertNotIn("kb-test", json.dumps(documents))
            self.assertTrue(documents[0]["knowledge_base_ref"].startswith("ima_kb:"))

            validation = ValidateMaterialIntake(
                FileSystemMaterialIntakeValidationRepository(project_dir)
            ).execute()
            self.assertTrue(validation["ok"], validation["issues"])
            self.assertEqual(validation["summary"]["documents"], 1)
            self.assertEqual(validation["summary"]["parse_tasks"], 12)

    def test_persists_unparsed_documents_outside_temporal_claim_ledger(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            (project_dir / "boms" / "memory").mkdir(parents=True)
            repository = FileSystemMaterialIntakeRepository(project_dir)
            result = ingest_material_batch(
                repository=repository,
                raw_documents=[
                    {
                        "external_id": "report-2",
                        "title": "HBM sell-side research report",
                        "published_at": "2026-07-20",
                        "source_type": "sell_side_report",
                    }
                ],
                provider="ima",
                feed_id="kb:memory",
                ingestion_channel="knowledge_base_scan",
                discovered_at="2026-07-21",
                known_bom_node_ids=["memory"],
                mode="live_prediction",
                as_of_date="2026-07-21",
                default_bom_node_ids=["memory"],
            )

            self.assertEqual(result["scan_event"]["parse_task_count"], 6)
            self.assertTrue(
                (project_dir / "boms" / "memory" / "inbox" / "materials.jsonl").is_file()
            )
            self.assertFalse(
                (project_dir / "boms" / "memory" / "ledger" / "claims.jsonl").exists()
            )

    def test_ima_adapter_requires_runtime_credentials(self):
        with patch.dict(
            "os.environ",
            {
                "IMA_OPENAPI_CLIENTID": "",
                "IMA_OPENAPI_APIKEY": "",
            },
            clear=False,
        ):
            with self.assertRaisesRegex(ValueError, "IMA_OPENAPI_CLIENTID"):
                ImaKnowledgeBaseFeed()

    def test_ima_adapter_normalizes_search_response_without_persisting_kb_id(self):
        feed = ImaKnowledgeBaseFeed(
            client_id="client",
            api_key="secret",
        )
        response = {
            "retcode": 0,
            "data": {
                "info_list": [
                    {
                        "media_id": "media-1",
                        "title": "HBM 行业深度报告",
                        "media_type": 1,
                        "create_time": "2026-07-20T08:00:00+08:00",
                        "highlight_content": "供需与价格趋势",
                    }
                ],
                "is_end": True,
            },
        }
        with patch(
            "urllib.request.urlopen",
            return_value=FakeUrlResponse(response),
        ):
            rows = feed.search_materials(
                knowledge_base_id="private-kb-id",
                query="HBM",
                max_results=10,
            )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["external_id"], "media-1")
        self.assertEqual(rows[0]["published_at"], "2026-07-20")
        self.assertNotIn("knowledge_base_id", rows[0])

    def test_material_validator_rejects_parse_task_for_quarantined_source(self):
        document = normalize_material_document(
            {
                "external_id": "post-cutoff",
                "title": "Post-cutoff report",
                "published_at": "2026-07-20",
                "source_type": "research_report",
            },
            ingestion_channel="knowledge_base_scan",
            provider="ima",
            discovered_at="2026-07-21",
            default_bom_node_ids=["memory"],
        )
        document = apply_time_slice_policy(
            document,
            mode="historical_backtest",
            as_of_date="2026-03-28",
        )
        bad_task = {
            "task_id": "PARSE-memory-q1-post-cutoff",
            "source_id": document["source_id"],
            "bom_node_id": "memory",
            "question_number": 1,
            "material_class": document["material_class"],
            "source_bucket": document["source_bucket"],
            "ingestion_channel": document["ingestion_channel"],
        }
        from value_invest_research.domain.material_intake import (
            validate_material_intake_bundle,
        )

        result = validate_material_intake_bundle(
            {
                "project": {
                    "mode": "historical_backtest",
                    "as_of_date": "2026-03-28",
                },
                "known_bom_node_ids": ["memory"],
                "documents": [document],
                "node_inboxes": {
                    "memory": {
                        "materials": [document],
                        "parse_tasks": [bad_task],
                    }
                },
            }
        )

        self.assertFalse(result["ok"])
        self.assertIn(
            "quarantined_material_has_parse_task",
            {issue["code"] for issue in result["issues"]},
        )


if __name__ == "__main__":
    unittest.main()
