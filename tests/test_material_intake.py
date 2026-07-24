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
from value_invest_research.adapters.outbound.pdf_publication_date_extractor import (
    PdfPublicationDateExtractor,
)
from value_invest_research.application.use_cases.ingest_materials import (
    ingest_material_batch,
    scan_knowledge_base_directory_materials,
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
from value_invest_research.domain.material_relevance import (
    classify_bom_material,
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

    def list_dated_materials(
        self,
        *,
        knowledge_base_id,
        start_date,
        end_date,
        root_folder_pattern,
    ):
        return [
            {
                "external_id": "gpu-report",
                "title": "高盛-英伟达 GPU 与 ASIC 产业更新-260724.pdf",
                "published_at": "2026-07-24",
                "directory_date": "2026-07-24",
                "directory_path": "2026年国际顶级投行研报/7月/7.24",
                "source_type": "sell_side_report",
                "provider": "ima",
            },
            {
                "external_id": "health-report",
                "title": "高盛-日本医疗保健行业更新-260724.pdf",
                "published_at": "2026-07-24",
                "directory_date": "2026-07-24",
                "directory_path": "2026年国际顶级投行研报/7月/7.24",
                "source_type": "sell_side_report",
                "provider": "ima",
            },
        ]

    def fetch_media_content(self, *, media_id, title=""):
        return {
            "content": b"%PDF-1.4 fake",
            "content_type": "application/pdf",
            "filename": title,
        }


class MaterialIntakeTests(unittest.TestCase):
    def test_bom_relevance_requires_direct_or_combined_semantic_match(self):
        profile = {
            "direct_terms": ["GPU", "ASIC"],
            "entity_terms": ["英伟达"],
            "context_terms": ["AI", "数据中心"],
            "supply_terms": ["CoWoS"],
            "exclude_terms": ["医疗"],
        }
        relevant = classify_bom_material(
            {
                "external_id": "a",
                "title": "英伟达数据中心路线更新.pdf",
                "directory_date": "2026-07-24",
            },
            bom_node_id="gpu_asic",
            profile=profile,
            scanned_at="2026-07-24",
        )
        unrelated = classify_bom_material(
            {
                "external_id": "b",
                "title": "日本医疗保健行业更新.pdf",
                "directory_date": "2026-07-24",
            },
            bom_node_id="gpu_asic",
            profile=profile,
            scanned_at="2026-07-24",
        )

        self.assertEqual(relevant["relevance_status"], "relevant")
        self.assertEqual(unrelated["relevance_status"], "not_relevant")

    def test_ima_directory_adapter_walks_year_month_day_and_paginates(self):
        feed = ImaKnowledgeBaseFeed(client_id="client", api_key="secret")

        def fake_post(endpoint, payload):
            self.assertEqual(endpoint, "get_knowledge_list")
            folder_id = payload.get("folder_id", "")
            rows = {
                "": [
                    {
                        "media_id": "year",
                        "media_type": 99,
                        "title": "2026年国际顶级投行研报",
                    }
                ],
                "year": [
                    {"media_id": "month", "media_type": 99, "title": "7月"}
                ],
                "month": [
                    {"media_id": "day", "media_type": 99, "title": "7.24"}
                ],
                "day": [
                    {
                        "media_id": "pdf-1",
                        "media_type": 1,
                        "title": "GPU 行业更新-260724.pdf",
                    }
                ],
            }[folder_id]
            return {
                "code": 0,
                "data": {
                    "knowledge_list": rows,
                    "is_end": True,
                    "next_cursor": "",
                },
            }

        with patch.object(feed, "_post", side_effect=fake_post):
            rows = feed.list_dated_materials(
                knowledge_base_id="kb-private",
                start_date="2026-07-24",
                end_date="2026-07-24",
                root_folder_pattern=r"^\d{4}年国际顶级投行研报$",
            )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["published_at"], "2026-07-24")
        self.assertEqual(rows[0]["directory_date"], "2026-07-24")
        self.assertEqual(rows[0]["directory_mapping_status"], "verified")
        self.assertEqual(
            rows[0]["directory_path"],
            "2026年国际顶级投行研报/7月/7.24",
        )

    def test_ima_directory_date_does_not_become_report_publication_date(self):
        feed = ImaKnowledgeBaseFeed(client_id="client", api_key="secret")

        def fake_post(endpoint, payload):
            folder_id = payload.get("folder_id", "")
            rows = {
                "": [
                    {
                        "media_id": "year",
                        "media_type": 99,
                        "title": "2026年国际顶级投行研报",
                    }
                ],
                "year": [
                    {"media_id": "month", "media_type": 99, "title": "7月"}
                ],
                "month": [
                    {"media_id": "day", "media_type": 99, "title": "7.24"}
                ],
                "day": [
                    {
                        "media_id": "pdf-undated",
                        "media_type": 1,
                        "title": "高盛_iPhone 与 AI ASIC 展望.pdf",
                        "create_time": "2026-07-24T08:00:00+08:00",
                    }
                ],
            }[folder_id]
            return {
                "code": 0,
                "data": {
                    "knowledge_list": rows,
                    "is_end": True,
                    "next_cursor": "",
                },
            }

        with patch.object(feed, "_post", side_effect=fake_post):
            rows = feed.list_dated_materials(
                knowledge_base_id="kb-private",
                start_date="2026-07-24",
                end_date="2026-07-24",
            )

        self.assertEqual(rows[0]["directory_date"], "2026-07-24")
        self.assertEqual(rows[0]["provider_created_at"], "2026-07-24")
        self.assertEqual(rows[0]["published_at"], "")
        self.assertEqual(
            rows[0]["directory_mapping_status"],
            "verified",
        )
        self.assertEqual(
            rows[0]["publication_date_status"],
            "needs_pdf_verification",
        )

    def test_directory_scan_audits_all_pdfs_but_ingests_only_relevant(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            (project_dir / "project.json").write_text(
                json.dumps(
                    {
                        "report_scope": "standalone-bom",
                        "bom_node_id": "gpu_asic",
                    }
                ),
                encoding="utf-8",
            )
            result = scan_knowledge_base_directory_materials(
                feed=FakeKnowledgeBaseFeed(),
                repository=FileSystemMaterialIntakeRepository(project_dir),
                knowledge_base_id="kb-private",
                bom_node_id="gpu_asic",
                relevance_profile={
                    "direct_terms": ["GPU", "ASIC"],
                    "entity_terms": ["英伟达"],
                    "context_terms": ["AI", "数据中心"],
                    "supply_terms": ["CoWoS"],
                    "exclude_terms": ["医疗"],
                },
                known_bom_node_ids=["gpu_asic"],
                mode="live_prediction",
                as_of_date="2026-07-24",
                start_date="2026-07-24",
                end_date="2026-07-24",
                discovered_at="2026-07-24",
                question_ids_by_node={
                    "gpu_asic": {
                        number: f"gpu_asic_q{number}"
                        for number in range(1, 6)
                    }
                },
                fetch_originals=False,
            )

            candidates = [
                json.loads(line)
                for line in (
                    project_dir
                    / "material_intake"
                    / "directory_candidates.jsonl"
                ).read_text(encoding="utf-8").splitlines()
            ]
            documents = [
                json.loads(line)
                for line in (
                    project_dir / "material_intake" / "documents.jsonl"
                ).read_text(encoding="utf-8").splitlines()
            ]

            self.assertEqual(result["directory_scan"]["candidate_count"], 2)
            self.assertEqual(result["directory_scan"]["relevant_count"], 1)
            self.assertEqual(len(candidates), 2)
            self.assertEqual(len(documents), 1)
            self.assertEqual(result["parse_tasks"], 5)

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

    def test_unknown_publication_date_blocks_claim_use_until_pdf_review(self):
        document = normalize_material_document(
            {
                "external_id": "ima-undated",
                "title": "高盛_iPhone 与 AI ASIC 展望.pdf",
                "source_type": "sell_side_report",
                "directory_date": "2026-07-24",
                "provider_created_at": "2026-07-24",
                "publication_date_status": "needs_pdf_verification",
                "publication_date_source": "unknown",
            },
            ingestion_channel="knowledge_base_scan",
            provider="ima",
            discovered_at="2026-07-24",
            default_bom_node_ids=["gpu_asic"],
            default_question_numbers=[1],
        )

        tasks = build_material_parse_tasks(document)

        self.assertEqual(document["published_at"], "")
        self.assertEqual(document["mapping_status"], "pending_publication_date")
        self.assertEqual(document["allowed_usage"], "date_verification_only")
        self.assertEqual(tasks[0]["status"], "pending_date_verification")

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

    def test_standalone_bom_scan_uses_five_lenses_and_root_inbox(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            (project_dir / "project.json").write_text(
                json.dumps(
                    {
                        "report_scope": "standalone-bom",
                        "bom_node_id": "gpu_asic",
                        "run_mode": "live_prediction",
                        "as_of_date": "2026-07-24",
                        "question_labels": [
                            "需求侧",
                            "供给侧",
                            "技术侧",
                            "估值侧",
                            "ESG",
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = scan_knowledge_base_materials(
                feed=FakeKnowledgeBaseFeed(),
                repository=FileSystemMaterialIntakeRepository(project_dir),
                knowledge_base_id="kb-test",
                bom_queries={"gpu_asic": ["GPU ASIC"]},
                known_bom_node_ids=["gpu_asic"],
                mode="live_prediction",
                as_of_date="2026-07-24",
                discovered_at="2026-07-24",
                question_ids_by_node={
                    "gpu_asic": {
                        1: "gpu_asic_demand",
                        2: "gpu_asic_supply",
                        3: "gpu_asic_technology",
                        4: "gpu_asic_valuation",
                        5: "gpu_asic_esg",
                    }
                },
                question_labels_by_node={
                    "gpu_asic": {
                        1: "需求侧",
                        2: "供给侧",
                        3: "技术侧",
                        4: "估值侧",
                        5: "ESG",
                    }
                },
            )

            tasks = [
                json.loads(line)
                for line in (
                    project_dir / "inbox" / "parse_tasks.jsonl"
                ).read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(result["parse_tasks"], 5)
            self.assertEqual([row["question_number"] for row in tasks], [1, 2, 3, 4, 5])
            self.assertEqual(tasks[0]["question_label"], "需求侧")
            validation = ValidateMaterialIntake(
                FileSystemMaterialIntakeValidationRepository(project_dir)
            ).execute()
            self.assertTrue(validation["ok"], validation["issues"])

    def test_ima_resolves_exact_knowledge_base_name(self):
        feed = ImaKnowledgeBaseFeed(client_id="client", api_key="secret")
        with patch.object(
            feed,
            "_post",
            return_value={
                "code": 0,
                "data": {
                    "info_list": [
                        {"id": "kb-1", "name": "环球研报直通车"},
                        {"id": "kb-2", "name": "其他知识库"},
                    ],
                    "is_end": True,
                },
            },
        ):
            knowledge_base_id = feed.resolve_knowledge_base_id("环球研报直通车")

        self.assertEqual(knowledge_base_id, "kb-1")

    def test_ima_resolves_live_knowledge_base_field_names(self):
        feed = ImaKnowledgeBaseFeed(client_id="client", api_key="secret")
        with patch.object(
            feed,
            "_post",
            return_value={
                "code": 0,
                "data": {
                    "info_list": [
                        {
                            "kb_id": "kb-live-1",
                            "kb_name": "环球研报直通车",
                            "base_type": "共享知识库",
                        },
                        {
                            "kb_id": "kb-live-2",
                            "kb_name": "其他知识库",
                        },
                    ],
                    "is_end": True,
                },
            },
        ):
            knowledge_base_id = feed.resolve_knowledge_base_id("环球研报直通车")

        self.assertEqual(knowledge_base_id, "kb-live-1")

    def test_original_material_is_persisted_and_attached_to_parse_tasks(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            (project_dir / "project.json").write_text(
                json.dumps(
                    {
                        "report_scope": "standalone-bom",
                        "bom_node_id": "gpu_asic",
                    }
                ),
                encoding="utf-8",
            )
            repository = FileSystemMaterialIntakeRepository(project_dir)
            result = ingest_material_batch(
                repository=repository,
                raw_documents=[
                    {
                        "external_id": "media-1",
                        "title": "GPU 深度报告",
                        "published_at": "2026-07-24",
                        "source_type": "sell_side_report",
                    }
                ],
                provider="ima",
                feed_id="feed-1",
                ingestion_channel="knowledge_base_scan",
                discovered_at="2026-07-24",
                known_bom_node_ids=["gpu_asic"],
                mode="live_prediction",
                as_of_date="2026-07-24",
                default_bom_node_ids=["gpu_asic"],
                question_ids_by_node={
                    "gpu_asic": {1: "gpu_asic_demand"}
                },
            )
            relative_path = repository.persist_material_content(
                document=result["documents"][0],
                content=b"%PDF-1.4 test",
                filename="GPU 深度报告.pdf",
                content_type="application/pdf",
            )

            tasks = [
                json.loads(line)
                for line in (
                    project_dir / "inbox" / "parse_tasks.jsonl"
                ).read_text(encoding="utf-8").splitlines()
            ]
            self.assertTrue((project_dir / relative_path).is_file())
            self.assertEqual(
                relative_path,
                "source/ima/2026/07/24/GPU 深度报告.pdf",
            )
            self.assertEqual(tasks[0]["source_content_path"], relative_path)

    def test_directory_review_moves_search_result_into_verified_ima_folder(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            (project_dir / "project.json").write_text(
                json.dumps(
                    {
                        "report_scope": "standalone-bom",
                        "bom_node_id": "gpu_asic",
                    }
                ),
                encoding="utf-8",
            )
            repository = FileSystemMaterialIntakeRepository(project_dir)
            result = ingest_material_batch(
                repository=repository,
                raw_documents=[
                    {
                        "external_id": "ima-search-hit",
                        "title": "高盛_iPhone 与 AI ASIC 展望.pdf",
                        "published_at": "2026-01-04",
                        "source_type": "sell_side_report",
                    }
                ],
                provider="ima",
                feed_id="search-feed",
                ingestion_channel="knowledge_base_scan",
                discovered_at="2026-07-24",
                known_bom_node_ids=["gpu_asic"],
                mode="live_prediction",
                as_of_date="2026-07-24",
                default_bom_node_ids=["gpu_asic"],
                default_question_numbers=[1],
            )
            document = result["documents"][0]
            unmapped_path = repository.persist_material_content(
                document=document,
                content=b"%PDF-1.4 report",
                filename="report.pdf",
                content_type="application/pdf",
            )

            verified_path = repository.update_directory_location(
                source_id=document["source_id"],
                directory_date="2026-03-26",
                directory_path="2026年国际顶级投行研报/3月/3.26",
                directory_mapping_status="verified",
            )

            self.assertEqual(
                unmapped_path,
                "source/ima/2026/01/04/report.pdf",
            )
            self.assertEqual(
                verified_path,
                "source/ima/2026/01/04/高盛_iPhone 与 AI ASIC 展望.pdf",
            )
            self.assertFalse((project_dir / unmapped_path).exists())
            self.assertTrue((project_dir / verified_path).is_file())
            task = json.loads(
                (
                    project_dir / "inbox" / "parse_tasks.jsonl"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(task["source_content_path"], verified_path)
            self.assertEqual(task["source_directory_date"], "2026-03-26")

    def test_publication_date_update_moves_original_by_report_date(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            (project_dir / "project.json").write_text(
                json.dumps(
                    {
                        "report_scope": "standalone-bom",
                        "bom_node_id": "gpu_asic",
                    }
                ),
                encoding="utf-8",
            )
            repository = FileSystemMaterialIntakeRepository(project_dir)
            result = ingest_material_batch(
                repository=repository,
                raw_documents=[
                    {
                        "external_id": "ima-archive-report",
                        "title": "GPU ASIC 展望.pdf",
                        "directory_date": "2026-07-24",
                        "directory_path": "2026年国际顶级投行研报/7月/7.24",
                        "source_type": "sell_side_report",
                    }
                ],
                provider="ima",
                feed_id="dated-directory",
                ingestion_channel="knowledge_base_scan",
                discovered_at="2026-07-24",
                known_bom_node_ids=["gpu_asic"],
                mode="live_prediction",
                as_of_date="2026-07-24",
                default_bom_node_ids=["gpu_asic"],
            )
            document = result["documents"][0]
            original_path = repository.persist_material_content(
                document=document,
                content=b"%PDF-1.4 report",
                filename="GPU ASIC 展望.pdf",
                content_type="application/pdf",
            )

            final_path = repository.update_publication_date(
                source_id=document["source_id"],
                published_at="2026-01-04",
                publication_date_status="verified",
                publication_date_source="pdf_cover",
                publication_date_locator="第1页：4 January 2026",
            )

            self.assertIn("/unmapped/", original_path)
            self.assertEqual(
                final_path,
                "source/ima/2026/01/04/GPU ASIC 展望.pdf",
            )
            self.assertFalse((project_dir / original_path).exists())
            self.assertTrue((project_dir / final_path).is_file())

    def test_pdf_publication_date_extractor_reads_cover_date(self):
        class FakePage:
            def extract_text(self):
                return "Global Technology Outlook\n4 January 2026 | 4:39PM HKT"

        class FakeReader:
            def __init__(self, *_args, **_kwargs):
                self.pages = [FakePage()]

        with patch(
            "value_invest_research.adapters.outbound."
            "pdf_publication_date_extractor.PdfReader",
            FakeReader,
        ):
            result = PdfPublicationDateExtractor().extract(
                content=b"%PDF-1.4",
                title="GPU outlook.pdf",
            )

        self.assertEqual(result["published_at"], "2026-01-04")
        self.assertEqual(result["publication_date_status"], "verified")
        self.assertEqual(result["publication_date_source"], "pdf_cover")
        self.assertIn("第1页", result["publication_date_locator"])

    def test_single_day_scan_archives_by_pdf_date_not_ima_directory_date(self):
        class FakeExtractor:
            def extract(self, *, content, title=""):
                return {
                    "published_at": "2026-07-23",
                    "publication_date_status": "verified",
                    "publication_date_source": "pdf_cover",
                    "publication_date_locator": "第1页：23 July 2026",
                }

        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            (project_dir / "project.json").write_text(
                json.dumps(
                    {
                        "report_scope": "standalone-bom",
                        "bom_node_id": "gpu_asic",
                    }
                ),
                encoding="utf-8",
            )
            repository = FileSystemMaterialIntakeRepository(project_dir)
            result = scan_knowledge_base_directory_materials(
                feed=FakeKnowledgeBaseFeed(),
                repository=repository,
                knowledge_base_id="kb-private",
                bom_node_id="gpu_asic",
                relevance_profile={
                    "direct_terms": ["GPU", "ASIC"],
                    "entity_terms": ["英伟达"],
                    "context_terms": ["AI", "数据中心"],
                    "supply_terms": ["CoWoS"],
                    "exclude_terms": ["医疗"],
                },
                known_bom_node_ids=["gpu_asic"],
                mode="live_prediction",
                as_of_date="2026-07-24",
                start_date="2026-07-24",
                end_date="2026-07-24",
                discovered_at="2026-07-24",
                fetch_originals=True,
                publication_date_extractor=FakeExtractor(),
            )

            self.assertEqual(result["directory_scan"]["candidate_count"], 2)
            self.assertEqual(result["directory_scan"]["relevant_count"], 1)
            self.assertEqual(
                result["content_results"][0]["local_content_path"],
                (
                    "source/ima/2026/07/23/"
                    "高盛-英伟达 GPU 与 ASIC 产业更新-260724.pdf"
                ),
            )
            document = json.loads(
                (
                    project_dir / "material_intake" / "documents.jsonl"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(document["directory_date"], "2026-07-24")
            self.assertEqual(document["published_at"], "2026-07-23")
            self.assertEqual(
                document["publication_date_source"],
                "pdf_cover",
            )

    def test_legacy_original_is_moved_into_project_source_tree(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            (project_dir / "project.json").write_text(
                json.dumps(
                    {
                        "report_scope": "standalone-bom",
                        "bom_node_id": "gpu_asic",
                    }
                ),
                encoding="utf-8",
            )
            source_id = "SRC-IMA-LEGACY"
            legacy_path = (
                project_dir
                / "material_intake"
                / "raw"
                / source_id
                / "legacy.pdf"
            )
            legacy_path.parent.mkdir(parents=True)
            legacy_path.write_bytes(b"%PDF-1.4 legacy")
            document = {
                "source_id": source_id,
                "title": "GPU ASIC 研报.pdf",
                "published_at": "2026-07-24",
                "directory_date": "2026-07-24",
                "local_content_path": legacy_path.relative_to(
                    project_dir
                ).as_posix(),
                "content_type": "application/pdf",
                "matched_bom_node_ids": ["gpu_asic"],
            }
            intake_dir = project_dir / "material_intake"
            intake_dir.mkdir(parents=True, exist_ok=True)
            (intake_dir / "documents.jsonl").write_text(
                json.dumps(document, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            inbox_dir = project_dir / "inbox"
            inbox_dir.mkdir(parents=True, exist_ok=True)
            reviewed_path = (
                inbox_dir / "reviewed_claims_20260724.jsonl"
            )
            reviewed_path.write_text(
                json.dumps(
                    {
                        "source_id": source_id,
                        "ingestion_channel": "knowledge_base_scan",
                        "source_url": document["local_content_path"],
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            repository = FileSystemMaterialIntakeRepository(project_dir)
            relative_path = repository.canonicalize_material_content(document)

            self.assertEqual(
                relative_path,
                "source/ima/2026/07/24/GPU ASIC 研报.pdf",
            )
            self.assertTrue((project_dir / relative_path).is_file())
            self.assertFalse(legacy_path.exists())
            reviewed = json.loads(
                reviewed_path.read_text(encoding="utf-8")
            )
            self.assertEqual(reviewed["source_url"], relative_path)

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
        ), patch(
            "value_invest_research.adapters.outbound.ima_knowledge_base_feed._read_secret",
            return_value="",
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
        self.assertEqual(rows[0]["published_at"], "")
        self.assertEqual(rows[0]["provider_created_at"], "2026-07-20")
        self.assertEqual(
            rows[0]["directory_mapping_status"],
            "pending_directory_reconciliation",
        )
        self.assertEqual(
            rows[0]["publication_date_status"],
            "needs_pdf_verification",
        )
        self.assertNotIn("knowledge_base_id", rows[0])

    def test_ima_search_infers_missing_publish_date_from_report_title(self):
        feed = ImaKnowledgeBaseFeed(client_id="client", api_key="secret")
        with patch.object(
            feed,
            "_post",
            return_value={
                "code": 0,
                "data": {
                    "info_list": [
                        {
                            "media_id": "media-title-date",
                            "title": "美银-英伟达：代理式 AI 路线之争-260722.pdf",
                            "media_type": 1,
                        }
                    ],
                    "is_end": True,
                },
            },
        ):
            rows = feed.search_materials(
                knowledge_base_id="private-kb-id",
                query="英伟达",
                max_results=10,
            )

        self.assertEqual(rows[0]["published_at"], "2026-07-22")
        self.assertEqual(
            rows[0]["publication_date_status"],
            "inferred_from_title",
        )
        self.assertEqual(rows[0]["publication_date_source"], "title_suffix")

    def test_publication_date_review_propagates_to_material_and_tasks(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            (project_dir / "project.json").write_text(
                json.dumps(
                    {
                        "report_scope": "standalone-bom",
                        "bom_node_id": "gpu_asic",
                    }
                ),
                encoding="utf-8",
            )
            repository = FileSystemMaterialIntakeRepository(project_dir)
            result = ingest_material_batch(
                repository=repository,
                raw_documents=[
                    {
                        "external_id": "undated-report",
                        "title": "高盛_iPhone 与 AI ASIC 展望.pdf",
                        "source_type": "sell_side_report",
                        "publication_date_status": "needs_pdf_verification",
                        "publication_date_source": "unknown",
                    }
                ],
                provider="ima",
                feed_id="feed-undated",
                ingestion_channel="knowledge_base_scan",
                discovered_at="2026-07-24",
                known_bom_node_ids=["gpu_asic"],
                mode="live_prediction",
                as_of_date="2026-07-24",
                default_bom_node_ids=["gpu_asic"],
                default_question_numbers=[1],
            )
            source_id = result["documents"][0]["source_id"]

            repository.update_publication_date(
                source_id=source_id,
                published_at="2026-01-04",
                publication_date_status="verified",
                publication_date_source="pdf_cover",
                publication_date_locator="第1页",
            )

            document = json.loads(
                (
                    project_dir / "material_intake" / "documents.jsonl"
                ).read_text(encoding="utf-8")
            )
            task = json.loads(
                (
                    project_dir / "inbox" / "parse_tasks.jsonl"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(document["published_at"], "2026-01-04")
            self.assertEqual(document["publication_date_source"], "pdf_cover")
            self.assertEqual(document["mapping_status"], "pending_question_parse")
            self.assertEqual(task["published_at"], "2026-01-04")
            self.assertEqual(task["status"], "pending")

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

    def test_material_validator_rejects_original_outside_project_source(self):
        from value_invest_research.domain.material_intake import (
            validate_material_intake_bundle,
        )

        document = normalize_material_document(
            {
                "external_id": "legacy-path",
                "title": "GPU report",
                "published_at": "2026-07-20",
                "source_type": "research_report",
            },
            ingestion_channel="knowledge_base_scan",
            provider="ima",
            discovered_at="2026-07-21",
            default_bom_node_ids=["gpu_asic"],
        )
        document["local_content_path"] = (
            "material_intake/raw/SRC-LEGACY/report.pdf"
        )

        result = validate_material_intake_bundle(
            {
                "project": {
                    "mode": "live_prediction",
                    "as_of_date": "2026-07-24",
                },
                "known_bom_node_ids": ["gpu_asic"],
                "documents": [document],
                "node_inboxes": {},
            }
        )

        self.assertFalse(result["ok"])
        self.assertIn(
            "material_original_outside_project_source",
            {issue["code"] for issue in result["issues"]},
        )


if __name__ == "__main__":
    unittest.main()
