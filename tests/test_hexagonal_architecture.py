import ast
import json
import tempfile
import unittest
from pathlib import Path

from value_invest_research.adapters.outbound.filesystem_research_artifacts import (
    FileSystemReportDocumentRepository,
    FileSystemResearchArtifactRepository,
    FileSystemSourceParsingArtifactWriter,
    FileSystemSourceListRepository,
)
from value_invest_research.adapters.outbound.filesystem_leaf_research import (
    FileSystemLeafResearchArtifactRepository,
    FileSystemLeafResearchResultRepository,
    FileSystemRawProviderResponseStore,
)
from value_invest_research.application.use_cases.audit_time_slice import AuditTimeSlice
from value_invest_research.application.use_cases.build_leaf_research_tasks_from_tree import BuildLeafResearchTasksFromTree
from value_invest_research.application.use_cases.execute_leaf_research_tasks import ExecuteLeafResearchTasks
from value_invest_research.application.use_cases.leaf_research_artifacts import (
    LoadCompletedLeafNodeIds,
    LoadLeafResearchResults,
    LoadLeafResearchTasks,
    PersistLeafAnswers,
    PersistLeafResearchTasks,
    PersistRollupAnswers,
)
from value_invest_research.application.use_cases.leaf_research_workflow import (
    BuildLeafResearchTasks,
    ImportLeafResearchResults,
    RollupResearchAnswers,
    RunLeafResearch,
    SynthesizeLeafAnswers,
)
from value_invest_research.application.use_cases.build_report_view_model import BuildReportViewModel
from value_invest_research.application.use_cases.persist_leaf_research_results import PersistLeafResearchResults
from value_invest_research.application.use_cases.persist_source_parsing import PersistSourceParsingArtifacts
from value_invest_research.application.use_cases.parse_l3_source_materials import ParseL3SourceMaterials
from value_invest_research.application.use_cases.plan_research_goal import PlanResearchGoal
from value_invest_research.application.use_cases.render_research_project_report import RenderResearchProjectReport
from value_invest_research.application.use_cases.score_targets import ScoreTargets
from value_invest_research.application.use_cases.synthesize_leaf_research_answers import (
    BuildRollupResearchAnswers,
    SynthesizeLeafResearchAnswers,
)
from value_invest_research.application.use_cases.validate_report_contract import ValidateReportContract
from value_invest_research.application.use_cases.validate_research_project import ValidateResearchProject
from value_invest_research.application.use_cases.write_professional_report import (
    WriteMetaQaProfessionalReport,
    WriteStockProfessionalReport,
)
from value_invest_research.adapters.outbound.canonical_html_report_renderer import CanonicalHtmlReportRenderer
from value_invest_research.adapters.outbound.filesystem_research_project import FileSystemResearchProjectRepository
from value_invest_research.adapters.outbound.source_material_parsers import (
    PassThroughSourceExtractionReviewer,
    SummarySourceMaterialParser,
)
from value_invest_research.framework_contracts import validate_report_contract_html
from value_invest_research.domain.leaf_research_tasks import build_leaf_tasks_from_tree
from value_invest_research.domain.research_artifacts import ReportDocument, ResearchArtifacts, SourceList
from value_invest_research.domain.research_goal import ResearchGoal


class _InMemoryArtifactRepository:
    project_dir_label = "memory://research-project"

    def __init__(self, artifacts: ResearchArtifacts):
        self._artifacts = artifacts

    def load_research_artifacts(self) -> ResearchArtifacts:
        return self._artifacts


class _InMemoryReportRepository:
    report_path_label = "memory://professional_report.html"

    def __init__(self, document: ReportDocument):
        self._document = document

    def load_report_document(self) -> ReportDocument:
        return self._document


class _InMemorySourceListRepository:
    source_path_label = "memory://sources.jsonl"

    def __init__(self, source_list: SourceList):
        self._source_list = source_list

    def load_sources(self) -> SourceList:
        return self._source_list


class _InMemoryResearchProjectRepository:
    project_dir_label = "memory://research-project"

    def __init__(self, project: dict, qa_tree: dict, sources: list[dict], targets: list[dict]):
        self.project = project
        self.qa_tree = qa_tree
        self.sources = sources
        self.targets = targets

    def load_project(self) -> dict:
        return self.project

    def load_qa_tree(self) -> dict:
        return self.qa_tree

    def load_sources_for_report(self) -> list[dict]:
        return self.sources

    def load_targets_for_report(self) -> list[dict]:
        return self.targets


class _FakeCanonicalRenderer:
    def __init__(self):
        self.writes: list[tuple[Path, str, int]] = []

    def render(self, view_model) -> str:
        return "<html></html>"

    def write(self, project_dir: Path, view_model, *, filename: str = "professional_report.html") -> dict:
        self.writes.append((project_dir, filename, len(view_model.qa_roots)))
        return {"project_id": view_model.project["project_id"], "report_path": str(project_dir / filename)}


class _FakeProfessionalReportRenderer:
    def __init__(self):
        self.calls: list[tuple[str, str]] = []

    def write_stock_report(self, root: Path, ticker: str, client=None) -> dict:
        self.calls.append(("stock", ticker))
        return {
            "ticker": ticker,
            "report_mode": "deterministic",
            "leaf_questions": 1,
            "professional_report_path": str(root / "stock.html"),
            "professional_report_md_path": str(root / "stock.md"),
        }

    def write_meta_qa_report(self, root: Path, project_id: str, client=None) -> dict:
        self.calls.append(("meta_qa", project_id))
        return {
            "project_id": project_id,
            "report_mode": "deterministic",
            "leaf_questions": 1,
            "professional_report_path": str(root / "meta.html"),
            "professional_report_md_path": str(root / "meta.md"),
        }


class _InMemorySourceParsingWriter:
    def __init__(self):
        self.source_extractions: list[dict] = []
        self.leaf_source_reviews: list[dict] = []

    def append_source_extractions(self, records: list[dict]) -> None:
        self.source_extractions.extend(records)

    def append_leaf_source_reviews(self, records: list[dict]) -> None:
        self.leaf_source_reviews.extend(records)


class _FakeLeafProvider:
    def search(self, task: dict) -> dict:
        return {
            "provider": "fake",
            "provider_model": "fake-model",
            "task_id": task["task_id"],
            "node_id": task["node_id"],
            "query": task["question"],
            "answer": "Fake provider answer.",
            "facts": ["Fake fact."],
            "inferences": ["Fake inference."],
            "judgment": "Fake judgment.",
            "sources": [
                {
                    "url": "https://example.com/source",
                    "title": "Fake Source",
                    "source_type": "research_report",
                    "information_category": "research_report",
                    "summary": "Fake source summary.",
                }
            ],
            "_raw_provider_response": {"raw": "payload"},
        }


class _InMemoryRawStore:
    raw_dir_label = "memory://raw"

    def __init__(self):
        self.payloads: list[tuple[str, dict]] = []

    def save_raw_response(self, task_id: str, payload: dict) -> str:
        self.payloads.append((task_id, payload))
        return f"memory://raw/{task_id}.json"


class _InMemoryLeafResultRepository:
    result_path_label = "memory://leaf_research_results.jsonl"
    source_path_label = "memory://leaf_research_sources.jsonl"

    def __init__(self):
        self.rows: list[dict] = []

    def save_results(self, rows: list[dict]) -> dict[str, int]:
        self.rows.extend(rows)
        source_count = sum(len(row.get("sources", [])) for row in rows)
        return {"results": len(rows), "sources": source_count}


class _InMemoryLeafArtifactRepository:
    task_path_label = "memory://leaf_research_tasks.jsonl"
    result_path_label = "memory://leaf_research_results.jsonl"
    answer_path_label = "memory://leaf_answers.jsonl"
    rollup_path_label = "memory://rollup_answers.jsonl"

    def __init__(self):
        self.tasks = [{"task_id": "task1"}]
        self.results = [{"node_id": "node1"}]
        self.answers: list[dict] = [{"node_id": "done"}]
        self.rollups: list[dict] = []

    def load_completed_leaf_node_ids(self) -> set[str]:
        return {str(row["node_id"]) for row in self.answers if row.get("node_id")}

    def save_tasks(self, rows: list[dict]) -> int:
        self.tasks = list(rows)
        return len(rows)

    def load_tasks(self) -> list[dict]:
        return self.tasks

    def load_results(self) -> list[dict]:
        return self.results

    def save_leaf_answers(self, rows: list[dict]) -> int:
        self.answers = list(rows)
        return len(rows)

    def save_rollup_answers(self, rows: list[dict]) -> int:
        self.rollups = list(rows)
        return len(rows)


class _FakeLeafResearchWorkflow:
    def __init__(self):
        self.calls: list[tuple] = []

    def build_tasks(self, root: Path, ticker: str, *, limit=None, include_completed=False) -> dict:
        self.calls.append(("build_tasks", ticker, limit, include_completed))
        return {"ticker": ticker, "tasks": limit or 1}

    def run_research(self, root: Path, ticker: str, *, provider: str, input_path=None, limit=None) -> dict:
        self.calls.append(("run_research", ticker, provider, input_path, limit))
        return {"ticker": ticker, "provider": provider, "results": limit or 1}

    def import_results(self, root: Path, ticker: str, path: Path) -> dict:
        self.calls.append(("import_results", ticker, path))
        return {"ticker": ticker, "records": 1}

    def synthesize_answers(self, root: Path, ticker: str) -> dict:
        self.calls.append(("synthesize_answers", ticker))
        return {"ticker": ticker, "answers": 1}

    def rollup_answers(self, root: Path, ticker: str) -> dict:
        self.calls.append(("rollup_answers", ticker))
        return {"ticker": ticker, "rollups": 1}


class HexagonalArchitectureTests(unittest.TestCase):
    def test_validate_research_project_use_case_accepts_repository_port(self):
        fixture_dir = Path(__file__).parent / "fixtures" / "research_quality_gold"
        artifacts = ResearchArtifacts(
            qa_tree=json.loads((fixture_dir / "qa_tree.json").read_text(encoding="utf-8")),
            source_extractions=_read_jsonl(fixture_dir / "source_extractions.jsonl"),
            leaf_source_reviews=_read_jsonl(fixture_dir / "leaf_source_reviews.jsonl"),
            targets=json.loads((fixture_dir / "investment_workbench.json").read_text(encoding="utf-8"))["scoring_worksheet"],
        )

        result = ValidateResearchProject(_InMemoryArtifactRepository(artifacts)).execute(require_l3=True)

        self.assertTrue(result.ok, result.issues)
        self.assertEqual(result.project_dir, "memory://research-project")
        self.assertEqual(result.qa_nodes, 13)
        self.assertEqual(result.leaf_source_reviews, 4)

    def test_validate_report_contract_use_case_accepts_repository_port(self):
        fixture_dir = Path(__file__).parent / "fixtures" / "research_quality_gold"
        document = ReportDocument(html=(fixture_dir / "professional_report.html").read_text(encoding="utf-8"))

        result = ValidateReportContract(_InMemoryReportRepository(document)).execute(require_l3=True)

        self.assertTrue(result.ok, result.issues)
        self.assertEqual(result.path, "memory://professional_report.html")
        self.assertEqual(result.level1_cards, 4)
        self.assertEqual(result.level3_cards, 4)

    def test_audit_time_slice_use_case_accepts_repository_port(self):
        sources = SourceList(
            sources=[
                {
                    "source_id": "visible",
                    "source_visible_at": "2026-02-20",
                    "allowed_usage": "thesis",
                    "used_in": ["q1"],
                    "availability_proof": {"proof_type": "publisher_date", "proof_value": "2026-02-20"},
                }
            ]
        )

        result = AuditTimeSlice(_InMemorySourceListRepository(sources)).execute(as_of_date="2026-02-28")

        self.assertTrue(result.ok, result.issues)
        self.assertEqual(result.path, "memory://sources.jsonl")
        self.assertEqual(result.sources, 1)

    def test_score_targets_use_case_runs_domain_scoring(self):
        fixture_dir = Path(__file__).parent / "fixtures" / "research_quality_gold"
        target = json.loads((fixture_dir / "investment_workbench.json").read_text(encoding="utf-8"))["scoring_worksheet"][0]

        result = ScoreTargets().execute([target])

        self.assertTrue(result.ok, result.issues)
        self.assertEqual(result.ranked_targets[0]["ticker"], "MU")
        self.assertIn(result.ranked_targets[0]["score"]["action_state"], {"watch_only", "no_action", "actionable_long"})

    def test_write_professional_report_use_cases_depend_on_renderer_port(self):
        renderer = _FakeProfessionalReportRenderer()
        stock_result = WriteStockProfessionalReport(renderer).execute(Path("/tmp/project"), "AAPL")
        meta_result = WriteMetaQaProfessionalReport(renderer).execute(Path("/tmp/project"), "ai_theme")

        self.assertEqual(stock_result["ticker"], "AAPL")
        self.assertEqual(meta_result["project_id"], "ai_theme")
        self.assertEqual(renderer.calls, [("stock", "AAPL"), ("meta_qa", "ai_theme")])

    def test_plan_research_goal_uses_domain_playbook(self):
        goal = ResearchGoal(
            topic="存储行业投资机会",
            research_type="industry",
            domain_hint="memory_industry",
        )

        architecture = PlanResearchGoal().execute(goal)

        self.assertEqual(architecture.playbook.playbook_id, "memory_industry")
        self.assertEqual([node.id for node in architecture.nodes if node.level == 1], ["Q1", "Q2", "Q3", "Q4"])
        self.assertGreater(len([node for node in architecture.nodes if node.level == 3]), 4)
        q2_leaf_questions = [node.question for node in architecture.nodes if node.id.startswith("Q2.") and node.level == 3]
        self.assertTrue(any("HBM" in question for question in q2_leaf_questions))

    def test_plan_research_goal_uses_event_conference_playbook_for_gtc(self):
        goal = ResearchGoal(
            topic="GTC Taipei 2026 大会投资机会",
            research_type="event",
            domain_hint="gtc_taipei_2026",
            run_mode="live_prediction",
        )

        architecture = PlanResearchGoal().execute(goal)

        self.assertEqual(architecture.playbook.playbook_id, "event_conference")
        self.assertEqual([node.id for node in architecture.nodes if node.level == 1], ["Q1", "Q2", "Q3", "Q4"])
        leaf_skills = {
            node.preferred_specialty_skill
            for node in architecture.nodes
            if node.level == 3
        }
        self.assertIn("event-to-investment-analysis", leaf_skills)
        self.assertIn("conference-transcript-analysis", leaf_skills)
        self.assertIn("company-exposure-analysis", leaf_skills)
        self.assertIn("target-ranking-analysis", leaf_skills)

    def test_research_goal_defaults_to_historical_backtest(self):
        goal = ResearchGoal(topic="光模块产业投资机会", research_type="industry")

        self.assertEqual(goal.run_mode, "historical_backtest")

    def test_build_report_view_model_uses_project_repository_port(self):
        project, qa_tree, sources, targets = _minimal_project_artifacts()
        repository = _InMemoryResearchProjectRepository(project, qa_tree, sources, targets)

        view_model = BuildReportViewModel(repository).execute()

        self.assertEqual(view_model.project["project_id"], "memory-test")
        self.assertEqual(len(view_model.qa_roots), 4)
        self.assertEqual(view_model.qa_roots[0]["children"][0]["children"][0]["source_index"][0]["source_id"], "SRC1")
        self.assertEqual(view_model.targets[0]["ticker"], "MU")

    def test_build_report_view_model_defaults_to_historical_backtest_when_mode_missing(self):
        project, qa_tree, sources, targets = _minimal_project_artifacts()
        project.pop("run_mode", None)
        qa_tree.pop("run_mode", None)

        view_model = BuildReportViewModel(_InMemoryResearchProjectRepository(project, qa_tree, sources, targets)).execute()

        self.assertEqual(view_model.project["run_mode"], "historical_backtest")

    def test_canonical_renderer_outputs_valid_contract_html(self):
        project, qa_tree, sources, targets = _minimal_project_artifacts()
        view_model = BuildReportViewModel(_InMemoryResearchProjectRepository(project, qa_tree, sources, targets)).execute()

        html = CanonicalHtmlReportRenderer().render(view_model)
        result = validate_report_contract_html(html, require_l3=True)

        self.assertTrue(result["ok"], result["issues"])
        self.assertEqual(result["summary"]["level1_cards"], 4)
        self.assertEqual(result["summary"]["interactive_level3_cards"], 4)

    def test_canonical_renderer_outputs_backtest_label_columns(self):
        project, qa_tree, sources, targets = _minimal_project_artifacts()
        project["run_mode"] = "historical_backtest"
        qa_tree["run_mode"] = "historical_backtest"
        targets[0]["label"] = {
            "as_of_date": "2026-03-01",
            "evaluation_date": "2026-06-01",
            "start_price": 100.0,
            "end_price": 128.26,
            "forward_3m_return": 0.2826,
            "label_status": "verified",
        }

        view_model = BuildReportViewModel(_InMemoryResearchProjectRepository(project, qa_tree, sources, targets)).execute()
        html = CanonicalHtmlReportRenderer().render(view_model)

        self.assertIn("三个月涨幅", html)
        self.assertIn("2026-03-01 → 2026-06-01", html)
        self.assertIn("28.3%", html)
        self.assertIn("verified", html)

    def test_render_research_project_report_uses_repository_and_renderer_ports(self):
        project, qa_tree, sources, targets = _minimal_project_artifacts()
        repository = _InMemoryResearchProjectRepository(project, qa_tree, sources, targets)
        renderer = _FakeCanonicalRenderer()

        result = RenderResearchProjectReport(repository, renderer).execute(filename="custom.html")

        self.assertEqual(result["project_id"], "memory-test")
        self.assertEqual(renderer.writes, [(Path("memory://research-project"), "custom.html", 4)])

    def test_persist_source_parsing_use_case_uses_writer_port(self):
        writer = _InMemorySourceParsingWriter()

        result = PersistSourceParsingArtifacts(writer).execute(
            source_extractions=[{"extraction_id": "ex1"}],
            leaf_source_reviews=[{"review_id": "rv1"}],
        )

        self.assertEqual(result, {"source_extractions": 1, "leaf_source_reviews": 1})
        self.assertEqual(writer.source_extractions, [{"extraction_id": "ex1"}])
        self.assertEqual(writer.leaf_source_reviews, [{"review_id": "rv1"}])

    def test_parse_l3_source_materials_use_case_uses_parser_reviewer_and_writer_ports(self):
        writer = _InMemorySourceParsingWriter()
        job = {
            "extraction_id": "EX1",
            "review_id": "RV1",
            "l3_question_id": "Q1.1.1",
            "source": {
                "source_id": "SRC1",
                "title": "Source",
                "source_bucket": "evidence",
                "support_refute_or_lead": "support",
                "summary": "Source says revenue grew.",
            },
            "extraction_schema": {"schema": "test_schema", "revenue": ""},
        }

        result = ParseL3SourceMaterials(
            SummarySourceMaterialParser(),
            PassThroughSourceExtractionReviewer(),
            writer,
        ).execute([job])

        self.assertEqual(result, {"source_extractions": 1, "leaf_source_reviews": 1, "jobs": 1})
        self.assertEqual(writer.source_extractions[0]["extraction_id"], "EX1")
        self.assertEqual(writer.source_extractions[0]["schema_fields"]["schema"], "test_schema")
        self.assertEqual(writer.leaf_source_reviews[0]["review_id"], "RV1")
        self.assertTrue(writer.leaf_source_reviews[0]["allowed_to_strengthen_conclusion"])

    def test_execute_leaf_research_tasks_use_case_normalizes_provider_results(self):
        raw_store = _InMemoryRawStore()
        task = {"task_id": "task1", "node_id": "node1", "question": "What matters?"}

        result = ExecuteLeafResearchTasks(_FakeLeafProvider(), raw_store).execute([task])

        self.assertEqual(result["results"], 1)
        self.assertEqual(result["raw_dir"], "memory://raw")
        self.assertEqual(raw_store.payloads, [("task1", {"raw": "payload"})])
        row = result["rows"][0]
        self.assertEqual(row["provider"], "fake")
        self.assertEqual(row["raw_response_path"], "memory://raw/task1.json")
        self.assertEqual(row["sources"][0]["information_category"], "research_report")

    def test_persist_leaf_research_results_use_case_uses_repository_port(self):
        repository = _InMemoryLeafResultRepository()
        rows = [
            {
                "task_id": "task1",
                "node_id": "node1",
                "sources": [{"url": "https://example.com/source", "title": "Source"}],
            }
        ]

        result = PersistLeafResearchResults(repository).execute(rows)

        self.assertEqual(result["result_path"], "memory://leaf_research_results.jsonl")
        self.assertEqual(result["source_path"], "memory://leaf_research_sources.jsonl")
        self.assertEqual(result["results"], 1)
        self.assertEqual(result["sources"], 1)
        self.assertEqual(repository.rows, rows)

    def test_leaf_research_artifact_use_cases_use_repository_port(self):
        repository = _InMemoryLeafArtifactRepository()

        task_result = PersistLeafResearchTasks(repository).execute([{"task_id": "new_task"}])
        tasks = LoadLeafResearchTasks(repository).execute()
        results = LoadLeafResearchResults(repository).execute()
        answer_result = PersistLeafAnswers(repository).execute([{"node_id": "node1"}])
        completed = LoadCompletedLeafNodeIds(repository).execute()
        rollup_result = PersistRollupAnswers(repository).execute([{"node_id": "parent"}])

        self.assertEqual(task_result, {"task_path": "memory://leaf_research_tasks.jsonl", "tasks": 1})
        self.assertEqual(tasks, [{"task_id": "new_task"}])
        self.assertEqual(results, [{"node_id": "node1"}])
        self.assertEqual(answer_result, {"answer_path": "memory://leaf_answers.jsonl", "answers": 1})
        self.assertEqual(completed, {"node1"})
        self.assertEqual(rollup_result, {"rollup_path": "memory://rollup_answers.jsonl", "rollups": 1})
        self.assertEqual(repository.rollups, [{"node_id": "parent"}])

    def test_build_leaf_tasks_from_tree_is_domain_pure(self):
        qa_tree = _leaf_qa_tree()

        tasks = build_leaf_tasks_from_tree(
            qa_tree,
            ticker="TEST",
            company_name="Test Co",
            completed_node_ids=set(),
        )

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["node_id"], "Q1.1.1")
        self.assertEqual(tasks[0]["selected_skill"], "financial-statement-analysis")
        self.assertEqual(tasks[0]["skill_dispatch_trace"]["skill_output_status"], "pending")

    def test_leaf_task_and_answer_use_cases_have_ports(self):
        repository = _InMemoryLeafArtifactRepository()
        repository.tasks = []
        repository.results = [
            {
                "task_id": "task1",
                "node_id": "Q1.1.1",
                "query": "财报是否支持？",
                "answer": "答案",
                "facts": ["事实"],
                "inferences": ["推论"],
                "judgment": "判断",
                "gaps": ["缺口"],
                "sources": [
                    {
                        "url": "https://example.com/source",
                        "title": "Source",
                        "information_category": "evidence",
                        "reliability": "primary",
                        "summary": "Source summary.",
                    }
                ],
            }
        ]
        qa_tree = _leaf_qa_tree()

        task_result = BuildLeafResearchTasksFromTree(repository).execute(
            qa_tree,
            ticker="TEST",
            company_name="Test Co",
        )
        answer_result = SynthesizeLeafResearchAnswers(repository).execute()
        rollup_result = BuildRollupResearchAnswers(repository).execute(_leaf_qa_tree_with_rollup())

        self.assertEqual(task_result["tasks"], 1)
        self.assertEqual(answer_result["answers"], 1)
        self.assertEqual(repository.answers[0]["source"], "leaf_research")
        self.assertEqual(rollup_result["rollups"], 1)
        self.assertEqual(repository.rollups[0]["source"], "leaf_research_rollup")

    def test_leaf_research_workflow_use_cases_depend_on_workflow_port(self):
        workflow = _FakeLeafResearchWorkflow()
        root = Path("/tmp/project")
        input_path = Path("/tmp/input.jsonl")

        build_result = BuildLeafResearchTasks(workflow).execute(root, "XIAOMI", limit=2, include_completed=True)
        run_result = RunLeafResearch(workflow).execute(root, "XIAOMI", provider="mock", input_path=input_path, limit=1)
        import_result = ImportLeafResearchResults(workflow).execute(root, "XIAOMI", input_path)
        synthesize_result = SynthesizeLeafAnswers(workflow).execute(root, "XIAOMI")
        rollup_result = RollupResearchAnswers(workflow).execute(root, "XIAOMI")

        self.assertEqual(build_result["tasks"], 2)
        self.assertEqual(run_result["provider"], "mock")
        self.assertEqual(import_result["records"], 1)
        self.assertEqual(synthesize_result["answers"], 1)
        self.assertEqual(rollup_result["rollups"], 1)
        self.assertEqual(
            workflow.calls,
            [
                ("build_tasks", "XIAOMI", 2, True),
                ("run_research", "XIAOMI", "mock", input_path, 1),
                ("import_results", "XIAOMI", input_path),
                ("synthesize_answers", "XIAOMI"),
                ("rollup_answers", "XIAOMI"),
            ],
        )

    def test_filesystem_artifact_repository_is_an_outbound_adapter(self):
        fixture_dir = Path(__file__).parent / "fixtures" / "research_quality_gold"
        repository = FileSystemResearchArtifactRepository(fixture_dir)

        artifacts = repository.load_research_artifacts()

        self.assertFalse(artifacts.load_issues)
        self.assertEqual(len(artifacts.source_extractions), 4)
        self.assertEqual(len(artifacts.leaf_source_reviews), 4)
        self.assertEqual(len(artifacts.targets), 1)

    def test_filesystem_report_repository_is_an_outbound_adapter(self):
        fixture_dir = Path(__file__).parent / "fixtures" / "research_quality_gold"
        repository = FileSystemReportDocumentRepository(fixture_dir / "professional_report.html")

        document = repository.load_report_document()

        self.assertIn("当前研究的问题", document.html)
        self.assertFalse(document.load_issues)

    def test_filesystem_source_list_repository_is_an_outbound_adapter(self):
        with tempfile.TemporaryDirectory() as tmp:
            source_path = Path(tmp) / "sources.jsonl"
            source_path.write_text(
                json.dumps(
                    {
                        "source_id": "visible",
                        "source_visible_at": "2026-02-20",
                        "allowed_usage": "thesis",
                        "used_in": ["q1"],
                        "availability_proof": {"proof_type": "publisher_date", "proof_value": "2026-02-20"},
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            repository = FileSystemSourceListRepository(source_path)

            source_list = repository.load_sources()

            self.assertEqual(len(source_list.sources), 1)
            self.assertFalse(source_list.load_issues)

    def test_filesystem_source_parsing_writer_is_an_outbound_adapter(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            writer = FileSystemSourceParsingArtifactWriter(project_dir)

            PersistSourceParsingArtifacts(writer).execute(
                source_extractions=[{"extraction_id": "ex1"}],
                leaf_source_reviews=[{"review_id": "rv1"}],
            )

            self.assertEqual(_read_jsonl(project_dir / "source_extractions.jsonl"), [{"extraction_id": "ex1"}])
            self.assertEqual(_read_jsonl(project_dir / "leaf_source_reviews.jsonl"), [{"review_id": "rv1"}])

    def test_filesystem_research_project_repository_loads_report_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            project, qa_tree, sources, targets = _minimal_project_artifacts()
            (project_dir / "project.json").write_text(json.dumps(project), encoding="utf-8")
            (project_dir / "qa_tree.json").write_text(json.dumps(qa_tree), encoding="utf-8")
            (project_dir / "sources.jsonl").write_text(
                "\n".join(json.dumps(source) for source in sources) + "\n",
                encoding="utf-8",
            )
            (project_dir / "investment_workbench.json").write_text(
                json.dumps({"scoring_worksheet": targets}),
                encoding="utf-8",
            )

            repository = FileSystemResearchProjectRepository(project_dir)

            self.assertEqual(repository.load_project()["project_id"], "memory-test")
            self.assertEqual(len(repository.load_qa_tree()["nodes"]), 12)
            self.assertEqual(repository.load_sources_for_report()[0]["source_id"], "SRC1")
            self.assertEqual(repository.load_targets_for_report()[0]["ticker"], "MU")

    def test_filesystem_raw_provider_response_store_is_an_outbound_adapter(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FileSystemRawProviderResponseStore(Path(tmp))

            path = store.save_raw_response("task1", {"raw": "payload"})

            self.assertEqual(store.raw_dir_label, tmp)
            self.assertEqual(json.loads(Path(path).read_text(encoding="utf-8")), {"raw": "payload"})

    def test_filesystem_leaf_research_artifact_repository_persists_tasks_answers_and_rollups(self):
        with tempfile.TemporaryDirectory() as tmp:
            repository = FileSystemLeafResearchArtifactRepository(Path(tmp))

            PersistLeafResearchTasks(repository).execute([{"task_id": "task1"}])
            PersistLeafAnswers(repository).execute([{"node_id": "node1"}])
            PersistRollupAnswers(repository).execute([{"node_id": "parent"}])
            (Path(tmp) / "leaf_research_results.jsonl").write_text(json.dumps({"node_id": "node1"}) + "\n", encoding="utf-8")

            self.assertEqual(LoadLeafResearchTasks(repository).execute(), [{"task_id": "task1"}])
            self.assertEqual(LoadLeafResearchResults(repository).execute(), [{"node_id": "node1"}])
            self.assertEqual(LoadCompletedLeafNodeIds(repository).execute(), {"node1"})
            self.assertEqual(_read_jsonl(Path(tmp) / "rollup_answers.jsonl"), [{"node_id": "parent"}])

    def test_filesystem_leaf_research_result_repository_merges_results_and_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            repository = FileSystemLeafResearchResultRepository(Path(tmp))
            first_row = {
                "task_id": "task1",
                "node_id": "node1",
                "provider": "mock",
                "query": "old question",
                "sources": [
                    {
                        "url": "https://example.com/source",
                        "title": "Shared Source",
                        "information_category": "research_report",
                    }
                ],
                "answer": "old",
            }
            replacement_row = {
                **first_row,
                "query": "new question",
                "answer": "new",
            }
            second_row = {
                "task_id": "task2",
                "node_id": "node2",
                "provider": "mock",
                "query": "second question",
                "sources": [
                    {
                        "url": "https://example.com/source",
                        "title": "Shared Source",
                        "information_category": "research_report",
                    }
                ],
                "answer": "second",
            }

            PersistLeafResearchResults(repository).execute([first_row])
            result = PersistLeafResearchResults(repository).execute([replacement_row, second_row])

            saved_results = _read_jsonl(Path(tmp) / "leaf_research_results.jsonl")
            saved_sources = _read_jsonl(Path(tmp) / "leaf_research_sources.jsonl")

            self.assertEqual(result["results"], 2)
            self.assertEqual(result["sources"], 1)
            self.assertEqual([row["answer"] for row in saved_results], ["new", "second"])
            self.assertEqual(saved_sources[0]["node_ids"], ["node1", "node2"])
            self.assertEqual(saved_sources[0]["result_count"], 2)

    def test_inner_layers_do_not_import_outer_layers(self):
        src_root = Path(__file__).resolve().parents[1] / "src" / "value_invest_research"
        forbidden = {
            "domain": (
                "value_invest_research.application",
                "value_invest_research.adapters",
                "value_invest_research.ports",
            ),
            "application": (
                "value_invest_research.adapters",
            ),
            "ports": (
                "value_invest_research.application",
                "value_invest_research.adapters",
            ),
        }

        violations = []
        for layer, prefixes in forbidden.items():
            for path in (src_root / layer).rglob("*.py"):
                for imported in _imports(path):
                    if imported.startswith(prefixes):
                        violations.append(f"{path.relative_to(src_root)} imports {imported}")

        self.assertEqual([], violations)

    def test_adapters_do_not_use_legacy_names(self):
        adapters_root = Path(__file__).resolve().parents[1] / "src" / "value_invest_research" / "adapters"
        violations = []
        for path in adapters_root.rglob("*.py"):
            if path.name.startswith("legacy_"):
                violations.append(str(path.relative_to(adapters_root)))
                continue
            source = path.read_text(encoding="utf-8")
            if "class Legacy" in source or "Legacy" in source:
                violations.append(str(path.relative_to(adapters_root)))

        self.assertEqual([], violations)

    def test_leaf_research_compatibility_module_has_no_network_provider_code(self):
        source = (Path(__file__).resolve().parents[1] / "src" / "value_invest_research" / "leaf_research.py").read_text(encoding="utf-8")

        self.assertNotIn("urllib.request", source)
        self.assertNotIn("chat/completions", source)
        self.assertNotIn("def provider_user_prompt", source)


def _minimal_project_artifacts() -> tuple[dict, dict, list[dict], list[dict]]:
    project = {
        "project_id": "memory-test",
        "title": "存储行业投资机会研究",
        "run_mode": "live_prediction",
        "report_date": "2026-06-01",
        "domain_playbook": "memory_industry",
        "decision_boundary": "research observation, not trading instruction",
        "supply_chain": {
            "plain_summary": "先确认需求如何传导到存储 BOM，再判断哪一段能捕获利润。",
            "flow_steps": [
                "云厂商训练和推理需求提高服务器内存带宽要求。",
                "高带宽需求传导到 HBM 与高端 DRAM 订单。",
                "存储厂商通过价格、mix 和毛利率兑现需求。",
            ],
            "layers": [
                {
                    "stage": "上游",
                    "node": "设备和材料",
                    "demand_input": "存储厂商扩产需求。",
                    "supply_input": "设备、材料和工艺能力。",
                    "produces": "关键制造能力。",
                    "players": "设备商",
                    "financial_metrics": "订单和 backlog。",
                    "value_flow": "决定供给释放速度。",
                    "qa_link": "Q2",
                },
                {
                    "stage": "中游",
                    "node": "HBM / 高端 DRAM",
                    "demand_input": "AI GPU 和加速卡需求。",
                    "supply_input": "晶圆产能、封装和良率。",
                    "produces": "HBM 与高端 DRAM。",
                    "players": "Micron",
                    "financial_metrics": "收入、ASP、毛利率。",
                    "value_flow": "核心利润池。",
                    "qa_link": "Q1/Q2",
                },
                {
                    "stage": "下游",
                    "node": "云厂商",
                    "demand_input": "AI 训练和推理工作负载。",
                    "supply_input": "GPU、HBM、服务器和网络。",
                    "produces": "capex、订单和使用率反馈。",
                    "players": "云厂商",
                    "financial_metrics": "capex、RPO、利用率。",
                    "value_flow": "验证需求持续性。",
                    "qa_link": "Q3",
                },
            ],
            "component_value_chain": [
                {
                    "subsystem": "HBM / 高端 DRAM",
                    "component": "高带宽内存",
                    "companies": "Micron",
                    "input": "AI 加速器需求与先进封装。",
                    "recipient": "GPU/服务器平台。",
                    "metric": "收入、ASP、毛利率。",
                    "qa": "Q1.1.1",
                }
            ],
            "industry_space_evidence_pack": [
                {
                    "node": "HBM / 高端 DRAM",
                    "coreQuestion": "AI 服务器需求是否继续放大高端内存空间？",
                    "facts": ["测试来源披露 HBM 需求仍在扩张。"],
                    "inferenceChain": ["若 AI 服务器 mix 提升，高端内存单机价值量上升。"],
                    "sourceIds": ["SRC1"],
                    "publicSizingMethods": {
                        "methods": [
                            {
                                "sourceType": "公司指引",
                                "organization": "Micron",
                                "guidanceContent": "管理层指引 HBM 需求增长。",
                                "bomNode": "HBM / 高端 DRAM",
                                "timeframe": "未来 12-24 个月",
                                "verificationMetric": "收入、ASP、毛利率。",
                                "confidence": "中",
                                "sourceIds": ["SRC1"],
                            }
                        ],
                        "sourceSearchPlan": {
                            "company_guidance": {
                                "status": "found",
                                "search_query": "Micron HBM guidance revenue gross margin",
                                "expected_fields": ["period", "guidance", "metric"],
                                "allowed_usage": "historical_thesis",
                                "preferred_parser_skill": "financial-statement-analysis",
                                "priority_sources": [{"id": "company_ir", "name": "Company IR"}],
                                "directed_queries": [{"source_id": "company_ir", "query": "Micron HBM guidance site:investors.micron.com before 2026-03-01"}],
                                "sourceIds": ["SRC1"],
                            },
                            "company_tam": {
                                "status": "gap",
                                "search_query": "Micron HBM TAM investor presentation",
                                "expected_fields": ["scope", "period", "tam"],
                                "allowed_usage": "lead_only",
                                "preferred_parser_skill": "industry-report-analysis",
                                "priority_sources": [{"id": "semianalysis", "name": "SemiAnalysis"}],
                                "directed_queries": [{"source_id": "semianalysis", "query": "site:semianalysis.com HBM TAM before 2026-03-01"}],
                                "gap_reason": "最小 fixture 未提供公司 TAM 来源。",
                            },
                            "customer_guidance": {
                                "status": "gap",
                                "search_query": "cloud capex HBM demand guidance",
                                "expected_fields": ["customer", "capex", "period"],
                                "allowed_usage": "lead_only",
                                "preferred_parser_skill": "financial-statement-analysis",
                                "priority_sources": [{"id": "customer_ir", "name": "Customer IR"}],
                                "directed_queries": [{"source_id": "customer_ir", "query": "cloud capex HBM demand before 2026-03-01"}],
                                "gap_reason": "最小 fixture 未提供客户侧来源。",
                            },
                            "third_party": {
                                "status": "gap",
                                "search_query": "HBM market sizing forecast",
                                "expected_fields": ["forecast", "method", "scope"],
                                "allowed_usage": "lead_only",
                                "preferred_parser_skill": "industry-report-analysis",
                                "priority_sources": [{"id": "trendforce", "name": "TrendForce"}],
                                "directed_queries": [{"source_id": "trendforce", "query": "site:trendforce.com HBM forecast before 2026-03-01"}],
                                "gap_reason": "最小 fixture 未提供第三方拆法来源。",
                            },
                            "financial_evidence": {
                                "status": "gap",
                                "search_query": "Micron HBM revenue margin reported",
                                "expected_fields": ["revenue", "margin", "period"],
                                "allowed_usage": "lead_only",
                                "preferred_parser_skill": "financial-statement-analysis",
                                "priority_sources": [{"id": "company_ir", "name": "Company IR"}],
                                "directed_queries": [{"source_id": "company_ir", "query": "site:investors.micron.com HBM revenue margin before 2026-03-01"}],
                                "gap_reason": "最小 fixture 未提供财务兑现来源。",
                            },
                        },
                        "alignment": "公司指引只作为方向性空间证据。",
                        "sanityCheck": "用收入、ASP 和毛利率验证。",
                        "conclusion": "高端内存具备继续扩张的待验证空间。",
                        "confidence": "中",
                    },
                }
            ],
        },
    }
    nodes: list[dict] = []
    for index, qid in enumerate(["Q1", "Q2", "Q3", "Q4"], start=1):
        nodes.extend(
            [
                {
                    "id": qid,
                    "level": 1,
                    "question": f"{qid} 一级问题",
                    "conclusion": f"{qid} 父层结论",
                    "parent_id": "",
                    "next_question_ids": [f"{qid}.1"],
                },
                {
                    "id": f"{qid}.1",
                    "level": 2,
                    "question": f"{qid}.1 机制问题",
                    "conclusion": f"{qid}.1 机制结论",
                    "parent_id": qid,
                    "next_question_ids": [f"{qid}.1.1"],
                },
                {
                    "id": f"{qid}.1.1",
                    "level": 3,
                    "question": f"{qid}.1.1 叶子问题",
                    "conclusion": f"{qid}.1.1 叶子结论",
                    "parent_id": f"{qid}.1",
                    "next_question_ids": [],
                    "decision_use": "影响父节点结论和最终标的强度。",
                    "score_component": "future_space" if qid != "Q4" else "target_ranking",
                    "fact": f"{qid} fact",
                    "inference": f"{qid} inference",
                    "judgment": f"{qid} judgment",
                    "gap": f"{qid} gap",
                    "trigger": f"{qid} trigger",
                    "source_links": ["SRC1"],
                    "skill_dispatch": {
                        "selected_skill": "financial-statement-analysis",
                        "gpt_verification_status": "verified",
                    },
                },
            ]
        )
    qa_tree = {
        "project_id": "memory-test",
        "run_mode": "live_prediction",
        "report_date": "2026-06-01",
        "domain_playbook": "memory_industry",
        "nodes": nodes,
    }
    sources = [
        {
            "source_id": "SRC1",
            "source_bucket": "evidence",
            "support_refute_or_lead": "support",
            "title": "Test Source",
            "summary": "测试来源摘要。",
            "url": "https://example.com/source",
        }
    ]
    targets = [
        {
            "rank": index,
            "ticker": ticker,
            "name": name,
            "action_state": action_state,
            "strength": strength,
            "chokepoint_node": "HBM/high-end DRAM",
            "rationale": "瓶颈、财务弹性和估值赔率共同支持进入观察清单。",
            "future_space": "未来空间来自 AI cloud memory mix 提升。",
            "risks": "ASP 反转、供给扩张和客户 capex 放缓。",
        }
        for index, (ticker, name, action_state, strength) in enumerate(
            [
                ("MU", "Micron Technology", "actionable_long", "高"),
                ("WDC", "Western Digital", "watch_only", "中"),
                ("SIMO", "Silicon Motion", "no_action", "低"),
            ],
            start=1,
        )
    ]
    return project, qa_tree, sources, targets


def _leaf_qa_tree() -> dict:
    return {
        "default_depth": 3,
        "ticker": "TEST",
        "nodes": [
            {
                "id": "Q1",
                "level": 1,
                "question": "一级问题",
                "parent_id": "",
                "next_question_ids": ["Q1.1"],
            },
            {
                "id": "Q1.1",
                "level": 2,
                "question": "父问题",
                "parent_id": "Q1",
                "next_question_ids": ["Q1.1.1"],
            },
            {
                "id": "Q1.1.1",
                "level": 3,
                "question": "财报是否支持增长？",
                "parent_id": "Q1.1",
                "next_question_ids": [],
                "required_evidence": ["收入和毛利率"],
            },
        ],
    }


def _leaf_qa_tree_with_rollup() -> dict:
    qa_tree = _leaf_qa_tree()
    qa_tree["nodes"][1] = {
        **qa_tree["nodes"][1],
        "metadata": {"rollup_sources": ["leaf_research"]},
        "professional_answer": {
            "answer": "父层答案",
            "facts": ["事实"],
            "inferences": ["推论"],
            "judgment": "判断",
            "gaps": ["缺口"],
            "source_balance": "证据 1 / 研报 0 / 消息 0 / 观点 0",
            "supporting_evidence": ["支撑"],
            "refuting_evidence": [],
            "research_leads": [],
            "rollup": "上抛结论",
        },
    }
    return qa_tree


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return imports


if __name__ == "__main__":
    unittest.main()
