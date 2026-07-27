import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from value_invest_research.adapters.outbound.filesystem_material_intake import (
    FileSystemMaterialIntakeRepository,
)
from value_invest_research.adapters.outbound.ima_archive_material_feed import (
    ImaArchiveMaterialFeed,
)
from value_invest_research.adapters.outbound.pdf_publication_date_extractor import (
    PdfPublicationDateExtractor,
)
from value_invest_research.application.use_cases.ingest_materials import (
    scan_knowledge_base_directory_materials,
)


class ImaArchiveMaterialFeedTests(unittest.TestCase):
    def test_routes_relevant_archive_pdf_into_reset_bom_project(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive_root = root / "source" / "ima"
            day_dir = archive_root / "2026" / "07" / "26"
            day_dir.mkdir(parents=True)
            relevant_name = "摩根大通-AMD AI accelerator update-260724.pdf"
            irrelevant_name = "高盛-中国乳制品行业-260724.pdf"
            (day_dir / relevant_name).write_bytes(b"%PDF-1.4 archive relevant")
            (day_dir / irrelevant_name).write_bytes(b"%PDF-1.4 archive irrelevant")
            manifest = [
                {
                    "record_id": "IMA-1",
                    "provider": "ima",
                    "external_id": "report-1",
                    "title": relevant_name,
                    "directory_date": "2026-07-26",
                    "directory_path": "2026/07/26",
                    "directory_mapping_status": "verified",
                    "status": "available",
                    "local_path": (
                        day_dir / relevant_name
                    ).relative_to(root).as_posix(),
                    "content_type": "application/pdf",
                },
                {
                    "record_id": "IMA-2",
                    "provider": "ima",
                    "external_id": "report-2",
                    "title": irrelevant_name,
                    "directory_date": "2026-07-26",
                    "directory_path": "2026/07/26",
                    "directory_mapping_status": "verified",
                    "status": "available",
                    "local_path": (
                        day_dir / irrelevant_name
                    ).relative_to(root).as_posix(),
                    "content_type": "application/pdf",
                },
            ]
            (archive_root / "archive_manifest.jsonl").write_text(
                "".join(
                    json.dumps(row, ensure_ascii=False) + "\n"
                    for row in manifest
                ),
                encoding="utf-8",
            )

            project_dir = root / "research" / "bom" / "gpu"
            project_dir.mkdir(parents=True)
            (project_dir / "project.json").write_text(
                json.dumps(
                    {
                        "report_scope": "standalone-bom",
                        "bom_node_id": "gpu_asic",
                    }
                ),
                encoding="utf-8",
            )
            (project_dir / "timeline_profile.json").write_text(
                json.dumps(
                    {
                        "lenses": [
                            {
                                "lens_id": "demand",
                                "logic_chain": "logic",
                                "baseline_conclusion": "old conclusion",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            old_claims = project_dir / "ledger" / "claims.jsonl"
            old_claims.parent.mkdir(parents=True)
            old_claims.write_text('{"claim_id":"old"}\n', encoding="utf-8")

            repository = FileSystemMaterialIntakeRepository(project_dir)
            repository.reset_research_state()
            result = scan_knowledge_base_directory_materials(
                feed=ImaArchiveMaterialFeed(
                    workspace_root=root,
                    archive_root=archive_root,
                ),
                repository=repository,
                knowledge_base_id="central-archive",
                bom_node_id="gpu_asic",
                relevance_profile={
                    "direct_terms": ["GPU", "ASIC", "AI accelerator"],
                    "entity_terms": ["AMD"],
                    "context_terms": ["AI", "半导体"],
                    "supply_terms": ["CoWoS"],
                    "exclude_terms": ["乳制品"],
                },
                known_bom_node_ids=["gpu_asic"],
                mode="live_prediction",
                as_of_date="2026-07-26",
                start_date="2026-07-26",
                end_date="2026-07-26",
                discovered_at="2026-07-27",
                question_ids_by_node={
                    "gpu_asic": {
                        1: "demand",
                        2: "supply",
                        3: "technology",
                        4: "valuation",
                        5: "esg",
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
                fetch_originals=True,
                publication_date_extractor=PdfPublicationDateExtractor(),
            )

            self.assertEqual(result["directory_scan"]["candidate_count"], 2)
            self.assertEqual(result["directory_scan"]["relevant_count"], 1)
            self.assertEqual(result["parse_tasks"], 5)
            self.assertFalse(old_claims.exists())
            copied = list(
                (project_dir / "source" / "ima" / "2026" / "07" / "24").glob(
                    "*.pdf"
                )
            )
            self.assertEqual([path.name for path in copied], [relevant_name])
            profile = json.loads(
                (project_dir / "timeline_profile.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertNotIn(
                "baseline_conclusion",
                profile["lenses"][0],
            )


if __name__ == "__main__":
    unittest.main()
