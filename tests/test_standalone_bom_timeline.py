import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from value_invest_research.adapters.outbound.filesystem_standalone_bom_timeline import (
    FileSystemStandaloneBomTimelineRepository,
)
from value_invest_research.adapters.outbound.filesystem_research_artifacts import (
    FileSystemResearchArtifactRepository,
)
from value_invest_research.adapters.outbound.standalone_bom_markdown_renderer import (
    StandaloneBomMarkdownRenderer,
)
from value_invest_research.adapters.outbound.standalone_bom_html_renderer import (
    StandaloneBomHtmlRenderer,
)
from value_invest_research.application.use_cases.refresh_standalone_bom_timeline import (
    apply_standalone_bom_updates,
)
from value_invest_research.framework_contracts import (
    validate_report_contract_html,
    validate_report_contract_markdown,
)


class StandaloneBomTimelineTests(unittest.TestCase):
    def test_legacy_qa_artifacts_are_not_required_for_standalone_bom(self):
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

            artifacts = FileSystemResearchArtifactRepository(
                project_dir
            ).load_research_artifacts()

            self.assertEqual(artifacts.load_issues, [])

    def test_applies_reviewed_claim_and_rebuilds_five_lens_report(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            project = {
                "title": "GPU / ASIC 实时跟踪",
                "report_scope": "standalone-bom",
                "bom_node_id": "gpu_asic",
            }
            profile = {
                "lenses": [
                    {
                        "lens_id": lens_id,
                        "logic_chain": f"{lens_id} logic",
                        "baseline_conclusion": f"{lens_id} baseline",
                    }
                    for lens_id in (
                        "demand",
                        "supply",
                        "technology",
                        "valuation",
                        "esg",
                    )
                ]
            }
            (project_dir / "project.json").write_text(
                json.dumps(project),
                encoding="utf-8",
            )
            (project_dir / "timeline_profile.json").write_text(
                json.dumps(profile),
                encoding="utf-8",
            )
            intake_dir = project_dir / "material_intake"
            inbox_dir = project_dir / "inbox"
            intake_dir.mkdir()
            inbox_dir.mkdir()
            material = {
                "source_id": "SRC-IMA-1",
                "mapping_status": "pending_question_parse",
                "publication_date_status": "verified",
                "publication_date_source": "pdf_cover",
                "publication_date_locator": "第1页",
            }
            (intake_dir / "documents.jsonl").write_text(
                json.dumps(material) + "\n",
                encoding="utf-8",
            )
            (inbox_dir / "materials.jsonl").write_text(
                json.dumps(material) + "\n",
                encoding="utf-8",
            )
            (inbox_dir / "parse_tasks.jsonl").write_text(
                "".join(
                    json.dumps(
                        {
                            "task_id": f"PARSE-{number}",
                            "source_id": "SRC-IMA-1",
                            "question_number": number,
                            "status": "pending",
                        }
                    )
                    + "\n"
                    for number in range(1, 6)
                ),
                encoding="utf-8",
            )
            result = apply_standalone_bom_updates(
                repository=FileSystemStandaloneBomTimelineRepository(project_dir),
                renderer=StandaloneBomMarkdownRenderer(project_dir=project_dir),
                html_renderer=StandaloneBomHtmlRenderer(project_dir=project_dir),
                raw_claims=[
                    {
                        "lens_id": "demand",
                        "source_id": "SRC-IMA-1",
                        "published_at": "2026-07-23",
                        "material_class": "sell_side_research",
                        "ingestion_channel": "knowledge_base_scan",
                        "source_title": "GPU demand report",
                        "source_url": "source/ima/2026/07/23/report.pdf",
                        "source_location": "第 3 页",
                        "statement": "机构上调未来两年 AI 加速器出货预测。",
                    },
                    {
                        "lens_id": "demand",
                        "source_id": "SRC-IMA-1",
                        "published_at": "2026-07-23",
                        "material_class": "sell_side_research",
                        "ingestion_channel": "knowledge_base_scan",
                        "source_title": "GPU demand report",
                        "source_url": "source/ima/2026/07/23/report.pdf",
                        "source_location": "第 8 页",
                        "statement": "机构同时上调云厂商 ASIC 出货预测。",
                    }
                ],
                raw_conclusions=[
                    {
                        "lens_id": "demand",
                        "conclusion": "需求预期继续上修，但需要订单兑现。",
                        "source_ids": ["SRC-IMA-1"],
                    }
                ],
                as_of_date="2026-07-24",
            )

            markdown = Path(result["markdown_report_path"]).read_text(
                encoding="utf-8"
            )
            validation = validate_report_contract_markdown(markdown)
            self.assertTrue(validation["ok"], validation["issues"])
            self.assertIn("机构上调未来两年 AI 加速器出货预测", markdown)
            self.assertIn("机构同时上调云厂商 ASIC 出货预测", markdown)
            self.assertIn(
                "• **观点 1（第 3 页）**："
                "机构上调未来两年 AI 加速器出货预测。",
                markdown,
            )
            self.assertIn(
                "<br>• **观点 2（第 8 页）**："
                "机构同时上调云厂商 ASIC 出货预测。",
                markdown,
            )
            self.assertEqual(markdown.count("GPU demand report"), 1)
            self.assertIn("| 时间 | 信息类型 | Source | 观点列表 |", markdown)
            self.assertNotIn("需求预期继续上修", markdown)
            conclusions = [
                json.loads(line)
                for line in (project_dir / "ledger/conclusions.jsonl").read_text(
                    encoding="utf-8"
                ).splitlines()
            ]
            self.assertEqual(
                conclusions[0]["conclusion"],
                "需求预期继续上修，但需要订单兑现。",
            )
            self.assertIn(
                (
                    f"](<{project_dir.resolve() / 'source/ima/2026/07/23/report.pdf'}>)"
                ),
                markdown,
            )
            self.assertEqual(result["applied_claims"], 2)
            sources = [
                json.loads(line)
                for line in (project_dir / "sources.jsonl").read_text(
                    encoding="utf-8"
                ).splitlines()
            ]
            self.assertEqual(sources[0]["source_id"], "SRC-IMA-1")
            self.assertEqual(sources[0]["source_bucket"], "research_report")
            self.assertEqual(
                sources[0]["availability_proof"],
                {
                    "proof_type": "pdf_cover",
                    "proof_value": "2026-07-23",
                    "locator": "第1页",
                },
            )
            tasks = [
                json.loads(line)
                for line in (inbox_dir / "parse_tasks.jsonl").read_text(
                    encoding="utf-8"
                ).splitlines()
            ]
            self.assertEqual({row["status"] for row in tasks}, {"completed"})
            self.assertEqual(tasks[0]["claim_count"], 2)
            self.assertEqual(tasks[1]["claim_count"], 0)
            documents = [
                json.loads(line)
                for line in (intake_dir / "documents.jsonl").read_text(
                    encoding="utf-8"
                ).splitlines()
            ]
            self.assertEqual(documents[0]["mapping_status"], "mapped")
            self.assertEqual(result["finalized_parse_tasks"], 5)
            self.assertEqual(result["finalized_documents"], 1)
            self.assertEqual(
                result["report_path"],
                result["html_report_path"],
            )
            html = Path(result["html_report_path"]).read_text(encoding="utf-8")
            html_validation = validate_report_contract_html(
                html,
                mode="live_prediction",
            )
            self.assertTrue(
                html_validation["ok"],
                html_validation["issues"],
            )
            self.assertIn('data-report-scope="standalone-bom"', html)
            self.assertEqual(html.count('class="lens-section"'), 5)
            self.assertEqual(html.count('class="timeline-table"'), 5)
            self.assertEqual(html.count("<th scope=\"col\">时间</th>"), 5)
            self.assertEqual(html.count("<th scope=\"col\">信息类型</th>"), 5)
            self.assertEqual(html.count("<th scope=\"col\">报告</th>"), 5)
            self.assertEqual(html.count("<th scope=\"col\">观点列表</th>"), 5)
            self.assertEqual(html.count('class="source-row"'), 1)
            self.assertIn('class="claim-list"', html)
            self.assertIn("观点 01", html)
            self.assertIn(
                'href="source/ima/2026/07/23/report.pdf"',
                html,
            )
            self.assertNotIn(
                'href="source/ima/2026/07/23/report.pdf" target="_blank"',
                html,
            )
            self.assertNotIn(f'href="{project_dir.resolve()}', html)

    def test_rejects_claim_from_material_with_unverified_publication_date(self):
        with TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            (project_dir / "project.json").write_text(
                json.dumps(
                    {
                        "title": "GPU / ASIC 实时跟踪",
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
                                "logic_chain": "demand logic",
                                "baseline_conclusion": "baseline",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            intake_dir = project_dir / "material_intake"
            intake_dir.mkdir(parents=True)
            (intake_dir / "documents.jsonl").write_text(
                json.dumps(
                    {
                        "source_id": "SRC-IMA-UNDATED",
                        "published_at": "",
                        "publication_date_status": "needs_pdf_verification",
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "must be verified"):
                apply_standalone_bom_updates(
                    repository=FileSystemStandaloneBomTimelineRepository(
                        project_dir
                    ),
                    renderer=StandaloneBomMarkdownRenderer(),
                    raw_claims=[
                        {
                            "lens_id": "demand",
                            "source_id": "SRC-IMA-UNDATED",
                            "published_at": "2026-07-24",
                            "material_class": "sell_side_research",
                            "ingestion_channel": "knowledge_base_scan",
                            "source_title": "Undated report",
                            "source_url": "source/ima/report.pdf",
                            "source_location": "第1页",
                            "statement": "AI ASIC demand rises.",
                        }
                    ],
                    raw_conclusions=[],
                    as_of_date="2026-07-24",
                )
