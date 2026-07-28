import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from value_invest_research.adapters.outbound.filesystem_ima_archive import (
    FileSystemImaArchiveRepository,
)
from value_invest_research.application.use_cases.archive_ima_daily import (
    archive_ima_day,
)
from value_invest_research.application.use_cases.archive_ima_ui import (
    archive_ima_ui_downloads,
)
from value_invest_research.application.use_cases.validate_ima_archive import (
    validate_ima_archive,
)


class FakeDailyImaFeed:
    provider_name = "ima"

    def __init__(self):
        self.fetches: list[str] = []

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
                "title": "英伟达 GPU 行业更新.pdf",
                "directory_date": start_date,
                "directory_path": "2026年国际顶级投行研报/7月/7.24",
                "directory_mapping_status": "verified",
            },
            {
                "external_id": "health-report",
                "title": "日本医疗保健行业更新.pdf",
                "directory_date": start_date,
                "directory_path": "2026年国际顶级投行研报/7月/7.24",
                "directory_mapping_status": "verified",
            },
        ]

    def fetch_media_content(self, *, media_id, title=""):
        self.fetches.append(media_id)
        return {
            "content": f"%PDF-1.4 {media_id}".encode(),
            "content_type": "application/pdf",
            "filename": title,
        }


class ImaDailyArchiveTests(unittest.TestCase):
    def test_archives_every_pdf_without_bom_relevance_filter(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            feed = FakeDailyImaFeed()
            result = archive_ima_day(
                feed=feed,
                repository=FileSystemImaArchiveRepository(
                    workspace_root=root,
                    archive_root=root / "source" / "ima",
                ),
                knowledge_base_id="private-kb-id",
                archive_date="2026-07-24",
                scanned_at="2026-07-25",
            )

            self.assertEqual(result["scan_event"]["candidate_count"], 2)
            self.assertEqual(result["scan_event"]["downloaded_count"], 2)
            self.assertEqual(
                sorted(feed.fetches),
                ["gpu-report", "health-report"],
            )
            day_dir = root / "source" / "ima" / "2026" / "07" / "24"
            self.assertEqual(len(list(day_dir.glob("*.pdf"))), 2)
            manifest = [
                json.loads(line)
                for line in (
                    root / "source" / "ima" / "archive_manifest.jsonl"
                ).read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(len(manifest), 2)
            self.assertNotIn("private-kb-id", json.dumps(manifest))

    def test_repeated_scan_reuses_existing_originals(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            feed = FakeDailyImaFeed()
            repository = FileSystemImaArchiveRepository(
                workspace_root=root,
                archive_root=root / "source" / "ima",
            )
            archive_ima_day(
                feed=feed,
                repository=repository,
                knowledge_base_id="private-kb-id",
                archive_date="2026-07-24",
                scanned_at="2026-07-25",
            )
            second = archive_ima_day(
                feed=feed,
                repository=repository,
                knowledge_base_id="private-kb-id",
                archive_date="2026-07-24",
                scanned_at="2026-07-26",
            )

            self.assertEqual(len(feed.fetches), 2)
            self.assertEqual(second["scan_event"]["downloaded_count"], 0)
            self.assertEqual(second["scan_event"]["reused_count"], 2)
            validation = validate_ima_archive(repository=repository)
            self.assertTrue(validation["ok"], validation["issues"])
            self.assertEqual(validation["available_count"], 2)

    def test_imports_visible_ui_downloads_without_provider_api(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            downloads = root / "Downloads"
            downloads.mkdir()
            marker = root / "download-start.marker"
            marker.touch()
            (downloads / "英伟达 GPU 行业更新.pdf").write_bytes(
                b"%PDF-1.4 ui-download"
            )
            repository = FileSystemImaArchiveRepository(
                workspace_root=root,
                archive_root=root / "source" / "ima",
            )

            result = archive_ima_ui_downloads(
                repository=repository,
                archive_date="2026-07-27",
                scanned_at="2026-07-28",
                candidates=[
                    {"title": "英伟达 GPU 行业更新.pdf"},
                    {"title": "未成功下载的报告.pdf"},
                ],
                download_dir=downloads,
                download_marker=marker,
                directory_path="2026年国际顶级投行研报/7月/7.27",
            )

            self.assertEqual(result["scan_event"]["candidate_count"], 2)
            self.assertEqual(result["scan_event"]["downloaded_count"], 1)
            self.assertEqual(result["scan_event"]["unavailable_count"], 1)
            self.assertEqual(result["scan_event"]["status"], "partial")
            record = result["records"][0]
            self.assertEqual(record["archive_method"], "ui_click")
            self.assertTrue(
                (root / record["local_path"]).is_file(),
                record["local_path"],
            )
            validation = validate_ima_archive(repository=repository)
            self.assertTrue(validation["ok"], validation["issues"])

    def test_ui_import_reconciles_existing_api_record_by_date_and_title(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            repository = FileSystemImaArchiveRepository(
                workspace_root=root,
                archive_root=root / "source" / "ima",
            )
            existing = {
                "record_id": "IMA-PDF-existing",
                "provider": "ima",
                "external_id": "provider-media-id",
                "title": "伯恩斯坦-全球存储行业.pdf",
                "directory_date": "2026-07-27",
                "directory_path": "2026年国际顶级投行研报/7月/7.27",
                "directory_mapping_status": "verified",
                "archived_at": "2026-07-28",
                "status": "unavailable",
                "error": "provider quota exhausted",
            }
            repository.persist_archive_record(existing)
            downloads = root / "Downloads"
            downloads.mkdir()
            (downloads / "伯恩斯坦-全球存储行业 (1).pdf").write_bytes(
                b"%PDF-1.4 clicked"
            )

            result = archive_ima_ui_downloads(
                repository=repository,
                archive_date="2026-07-27",
                scanned_at="2026-07-29",
                candidates=[{"title": "伯恩斯坦-全球存储行业.pdf"}],
                download_dir=downloads,
            )

            record = result["records"][0]
            self.assertEqual(record["record_id"], "IMA-PDF-existing")
            self.assertEqual(record["external_id"], "provider-media-id")
            self.assertEqual(record["status"], "available")
            self.assertNotIn("error", record)
            self.assertEqual(result["scan_event"]["downloaded_count"], 1)


if __name__ == "__main__":
    unittest.main()
