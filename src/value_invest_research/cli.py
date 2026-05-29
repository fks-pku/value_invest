from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from value_invest_research.models import EvidenceRecord, ValidationError
from value_invest_research.scaffold import init_event, init_stock


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="value-invest-research")
    parser.add_argument("--root", default=".", help="Workspace root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    stock_parser = subparsers.add_parser("init-stock", help="Create a stock research folder")
    stock_parser.add_argument("ticker")
    stock_parser.add_argument("--company-name")

    event_parser = subparsers.add_parser("init-event", help="Create an event research folder")
    event_parser.add_argument("event_date")
    event_parser.add_argument("event_name")

    evidence_parser = subparsers.add_parser("validate-evidence", help="Validate an evidence JSONL file")
    evidence_parser.add_argument("path")

    build_evidence_parser = subparsers.add_parser("build-evidence", help="Build evidence records from structured stock data")
    build_evidence_parser.add_argument("ticker")

    graph_parser = subparsers.add_parser("build-research-graph", help="Build the full message-flow research graph pipeline")
    graph_parser.add_argument("ticker")

    consensus_parser = subparsers.add_parser("build-consensus", help="Build priced-consensus baseline graph nodes")
    consensus_parser.add_argument("ticker")

    questions_parser = subparsers.add_parser("generate-questions", help="Generate 3T message-flow question graph nodes")
    questions_parser.add_argument("ticker")

    hypotheses_parser = subparsers.add_parser("build-hypotheses", help="Build hypothesis graph nodes from research questions")
    hypotheses_parser.add_argument("ticker")

    tests_parser = subparsers.add_parser("test-hypotheses", help="Build assumption-test graph nodes from hypotheses and evidence")
    tests_parser.add_argument("ticker")

    report_parser = subparsers.add_parser("write-forward-report", help="Write a forward research report from the graph")
    report_parser.add_argument("ticker")

    research_system_parser = subparsers.add_parser(
        "build-research-system",
        help="Build the layered QA research dashboard and report",
    )
    research_system_parser.add_argument("ticker")

    validate_qa_system_parser = subparsers.add_parser(
        "validate-qa-system",
        help="Validate that a stock layered QA system satisfies the research contract",
    )
    validate_qa_system_parser.add_argument("ticker")
    validate_qa_system_parser.add_argument("--require-professional-report", action="store_true")

    stock_pipeline_parser = subparsers.add_parser(
        "run-stock-qa-pipeline",
        help="Run the stock layered QA workflow from object to report",
    )
    stock_pipeline_parser.add_argument("ticker")
    stock_pipeline_parser.add_argument("--task-limit", type=int, default=None)
    stock_pipeline_parser.add_argument("--run-local-collection", action="store_true")
    stock_pipeline_parser.add_argument("--discover-candidates", action="store_true")
    stock_pipeline_parser.add_argument("--apply-candidates", action="store_true")
    stock_pipeline_parser.add_argument("--candidate-path", default=None)
    stock_pipeline_parser.add_argument("--search-results-path", default=None)
    stock_pipeline_parser.add_argument("--results-per-task", type=int, default=3)
    stock_pipeline_parser.add_argument("--candidate-min-score", type=int, default=4)
    stock_pipeline_parser.add_argument("--dry-run-candidates", action="store_true")
    stock_pipeline_parser.add_argument("--synthesize-answers", action="store_true")
    stock_pipeline_parser.add_argument("--synthesis-use-llm", action="store_true")
    stock_pipeline_parser.add_argument("--synthesis-api-key", default=None)
    stock_pipeline_parser.add_argument("--synthesis-base-url", default="https://api.z.ai/api/coding/paas/v4")
    stock_pipeline_parser.add_argument("--synthesis-model", default="glm-5.1")
    stock_pipeline_parser.add_argument("--write-professional-report", action="store_true")
    stock_pipeline_parser.add_argument("--professional-report-use-llm", action="store_true")
    stock_pipeline_parser.add_argument("--professional-report-api-key", default=None)
    stock_pipeline_parser.add_argument("--professional-report-base-url", default="https://api.z.ai/api/coding/paas/v4")
    stock_pipeline_parser.add_argument("--professional-report-model", default="glm-5.1")
    stock_pipeline_parser.add_argument("--leaf-research-provider", default=None, choices=["mock", "manual", "perplexity", "openai_compatible"])
    stock_pipeline_parser.add_argument("--leaf-research-input", default=None)
    stock_pipeline_parser.add_argument("--leaf-research-limit", type=int, default=None)
    stock_pipeline_parser.add_argument("--timeout", type=int, default=10)

    add_question_parser = subparsers.add_parser(
        "add-research-question",
        help="Persist a user-added layered QA question and rebuild the research system",
    )
    add_question_parser.add_argument("ticker")
    add_question_parser.add_argument("--parent-id", required=True)
    add_question_parser.add_argument("--question", required=True)
    add_question_parser.add_argument("--terminal", action="store_true")

    record_question_info_parser = subparsers.add_parser(
        "record-question-information",
        help="Record a collected source, attach it to a QA node, and rebuild the research system",
    )
    record_question_info_parser.add_argument("ticker")
    record_question_info_parser.add_argument("--node-id", required=True)
    record_question_info_parser.add_argument(
        "--category",
        required=True,
        choices=["evidence", "research_report", "message", "opinion"],
    )
    record_question_info_parser.add_argument("--source-type", required=True)
    record_question_info_parser.add_argument("--source-name", required=True)
    record_question_info_parser.add_argument("--url", required=True)
    record_question_info_parser.add_argument("--summary", required=True)
    record_question_info_parser.add_argument("--reliability", default="medium", choices=["primary", "high", "medium", "low"])
    record_question_info_parser.add_argument("--materiality", default="medium", choices=["low", "medium", "high", "thesis_change"])
    record_question_info_parser.add_argument("--published-at", default=None)

    collection_tasks_parser = subparsers.add_parser(
        "build-collection-tasks",
        help="Build actionable four-bucket collection tasks for a stock QA research system",
    )
    collection_tasks_parser.add_argument("ticker")
    collection_tasks_parser.add_argument("--include-matched", action="store_true")
    collection_tasks_parser.add_argument("--limit", type=int, default=None)

    run_collection_parser = subparsers.add_parser(
        "run-collection-tasks",
        help="Run stock collection tasks against the local evidence corpus and bind matched sources",
    )
    run_collection_parser.add_argument("ticker")
    run_collection_parser.add_argument("--include-matched", action="store_true")
    run_collection_parser.add_argument("--limit", type=int, default=None)
    run_collection_parser.add_argument("--min-score", type=int, default=4)
    run_collection_parser.add_argument("--max-sources-per-task", type=int, default=1)
    run_collection_parser.add_argument("--dry-run", action="store_true")

    discover_candidates_parser = subparsers.add_parser(
        "discover-source-candidates",
        help="Search or import candidate URLs for stock QA collection tasks",
    )
    discover_candidates_parser.add_argument("ticker")
    discover_candidates_parser.add_argument("--include-matched", action="store_true")
    discover_candidates_parser.add_argument("--limit", type=int, default=None)
    discover_candidates_parser.add_argument("--results-per-task", type=int, default=3)
    discover_candidates_parser.add_argument("--min-score", type=int, default=4)
    discover_candidates_parser.add_argument("--timeout", type=int, default=10)
    discover_candidates_parser.add_argument("--search-results-path", default=None)

    apply_candidates_parser = subparsers.add_parser(
        "apply-source-candidates",
        help="Fetch accepted stock source candidates and bind them to QA nodes",
    )
    apply_candidates_parser.add_argument("ticker")
    apply_candidates_parser.add_argument("--path", required=True)
    apply_candidates_parser.add_argument("--min-score", type=int, default=4)
    apply_candidates_parser.add_argument("--limit", type=int, default=None)
    apply_candidates_parser.add_argument("--timeout", type=int, default=10)
    apply_candidates_parser.add_argument("--dry-run", action="store_true")

    import_question_info_parser = subparsers.add_parser(
        "import-question-information",
        help="Batch-import collected stock QA sources from a JSONL file",
    )
    import_question_info_parser.add_argument("ticker")
    import_question_info_parser.add_argument("--path", required=True)

    stock_synthesis_tasks_parser = subparsers.add_parser(
        "build-synthesis-tasks",
        help="Build professional answer-synthesis tasks for stock QA nodes",
    )
    stock_synthesis_tasks_parser.add_argument("ticker")
    stock_synthesis_tasks_parser.add_argument("--all-nodes", dest="leaf_only", action="store_false", default=True)
    stock_synthesis_tasks_parser.add_argument("--limit", type=int, default=None)

    import_stock_synthesis_parser = subparsers.add_parser(
        "import-answer-synthesis",
        help="Batch-import synthesized professional stock QA answers from JSONL",
    )
    import_stock_synthesis_parser.add_argument("ticker")
    import_stock_synthesis_parser.add_argument("--path", required=True)

    run_stock_synthesis_parser = subparsers.add_parser(
        "run-answer-synthesis",
        help="Generate and optionally apply professional stock QA answers",
    )
    run_stock_synthesis_parser.add_argument("ticker")
    run_stock_synthesis_parser.add_argument("--all-nodes", dest="leaf_only", action="store_false", default=True)
    run_stock_synthesis_parser.add_argument("--limit", type=int, default=None)
    run_stock_synthesis_parser.add_argument("--no-apply", dest="apply", action="store_false", default=True)
    run_stock_synthesis_parser.add_argument("--use-llm", action="store_true")
    run_stock_synthesis_parser.add_argument("--api-key", default=None)
    run_stock_synthesis_parser.add_argument("--base-url", default="https://api.z.ai/api/coding/paas/v4")
    run_stock_synthesis_parser.add_argument("--model", default="glm-5.1")

    leaf_tasks_parser = subparsers.add_parser(
        "build-leaf-research-tasks",
        help="Build provider-agnostic leaf research tasks for terminal stock QA nodes",
    )
    leaf_tasks_parser.add_argument("ticker")
    leaf_tasks_parser.add_argument("--limit", type=int, default=None)
    leaf_tasks_parser.add_argument("--include-completed", action="store_true")

    run_leaf_parser = subparsers.add_parser(
        "run-leaf-research",
        help="Run leaf research tasks through a provider adapter",
    )
    run_leaf_parser.add_argument("ticker")
    run_leaf_parser.add_argument("--provider", default="mock", choices=["mock", "manual", "perplexity", "openai_compatible"])
    run_leaf_parser.add_argument("--input", default=None)
    run_leaf_parser.add_argument("--limit", type=int, default=None)

    import_leaf_parser = subparsers.add_parser(
        "import-leaf-research-results",
        help="Import provider-agnostic leaf research results from JSONL",
    )
    import_leaf_parser.add_argument("ticker")
    import_leaf_parser.add_argument("--path", required=True)

    leaf_answers_parser = subparsers.add_parser(
        "synthesize-leaf-answers",
        help="Write detailed leaf answers from normalized provider results",
    )
    leaf_answers_parser.add_argument("ticker")

    leaf_rollup_parser = subparsers.add_parser(
        "rollup-research-answers",
        help="Persist parent rollups after leaf answers are applied",
    )
    leaf_rollup_parser.add_argument("ticker")

    stock_professional_report_parser = subparsers.add_parser(
        "write-professional-report",
        help="Write a professional report from the stock layered QA tree",
    )
    stock_professional_report_parser.add_argument("ticker")
    stock_professional_report_parser.add_argument("--use-llm", action="store_true")
    stock_professional_report_parser.add_argument("--api-key", default=None)
    stock_professional_report_parser.add_argument("--base-url", default="https://api.z.ai/api/coding/paas/v4")
    stock_professional_report_parser.add_argument("--model", default="glm-5.1")

    apply_question_queue_parser = subparsers.add_parser(
        "apply-question-queue",
        help="Apply queued stock QA questions from JSONL/JSON and rebuild report/tasks",
    )
    apply_question_queue_parser.add_argument("ticker")
    apply_question_queue_parser.add_argument("--path", required=True)
    apply_question_queue_parser.add_argument("--no-build-tasks", dest="build_tasks", action="store_false", default=True)
    apply_question_queue_parser.add_argument("--run-local-collection", action="store_true")
    apply_question_queue_parser.add_argument("--limit", type=int, default=None)
    apply_question_queue_parser.add_argument("--min-score", type=int, default=4)
    apply_question_queue_parser.add_argument("--synthesize-answers", action="store_true")
    apply_question_queue_parser.add_argument("--synthesis-use-llm", action="store_true")
    apply_question_queue_parser.add_argument("--synthesis-api-key", default=None)
    apply_question_queue_parser.add_argument("--synthesis-base-url", default="https://api.z.ai/api/coding/paas/v4")
    apply_question_queue_parser.add_argument("--synthesis-model", default="glm-5.1")
    apply_question_queue_parser.add_argument("--write-professional-report", action="store_true")
    apply_question_queue_parser.add_argument("--professional-report-use-llm", action="store_true")
    apply_question_queue_parser.add_argument("--professional-report-api-key", default=None)
    apply_question_queue_parser.add_argument("--professional-report-base-url", default="https://api.z.ai/api/coding/paas/v4")
    apply_question_queue_parser.add_argument("--professional-report-model", default="glm-5.1")

    fetch_question_info_parser = subparsers.add_parser(
        "fetch-question-information-url",
        help="Fetch a URL, summarize it, bind it to a stock QA node, and rebuild",
    )
    fetch_question_info_parser.add_argument("ticker")
    fetch_question_info_parser.add_argument("--node-id", required=True)
    fetch_question_info_parser.add_argument(
        "--category",
        required=True,
        choices=["evidence", "research_report", "message", "opinion"],
    )
    fetch_question_info_parser.add_argument("--url", required=True)
    fetch_question_info_parser.add_argument("--source-type", default=None)
    fetch_question_info_parser.add_argument("--source-name", default=None)
    fetch_question_info_parser.add_argument("--summary", default=None)
    fetch_question_info_parser.add_argument("--reliability", default=None, choices=["primary", "high", "medium", "low"])
    fetch_question_info_parser.add_argument("--materiality", default=None, choices=["low", "medium", "high", "thesis_change"])
    fetch_question_info_parser.add_argument("--published-at", default=None)
    fetch_question_info_parser.add_argument("--timeout", type=int, default=10)

    meta_qa_parser = subparsers.add_parser(
        "build-meta-qa",
        help="Build a generic layered QA research project from one meta-question",
    )
    meta_qa_object_types = ["company", "industry", "event", "technology", "target_update", "custom"]
    meta_qa_parser.add_argument("--object-type", required=True, choices=meta_qa_object_types)
    meta_qa_parser.add_argument("--object-id", default="")
    meta_qa_parser.add_argument("--meta-question", required=True)
    meta_qa_parser.add_argument("--project-id", default=None)
    meta_qa_parser.add_argument("--max-depth", type=int, default=3)
    meta_qa_parser.add_argument("--planner-use-llm", action="store_true")
    meta_qa_parser.add_argument("--planner-api-key", default=None)
    meta_qa_parser.add_argument("--planner-base-url", default="https://api.z.ai/api/coding/paas/v4")
    meta_qa_parser.add_argument("--planner-model", default="glm-5.1")
    meta_qa_parser.add_argument("--force-plan", action="store_true")

    meta_qa_pipeline_parser = subparsers.add_parser(
        "run-meta-qa-pipeline",
        help="Run a generic layered QA workflow from one meta-question to report",
    )
    meta_qa_pipeline_parser.add_argument("--object-type", required=True, choices=meta_qa_object_types)
    meta_qa_pipeline_parser.add_argument("--object-id", default="")
    meta_qa_pipeline_parser.add_argument("--meta-question", required=True)
    meta_qa_pipeline_parser.add_argument("--project-id", default=None)
    meta_qa_pipeline_parser.add_argument("--max-depth", type=int, default=3)
    meta_qa_pipeline_parser.add_argument("--task-limit", type=int, default=None)
    meta_qa_pipeline_parser.add_argument("--run-local-collection", action="store_true")
    meta_qa_pipeline_parser.add_argument("--discover-candidates", action="store_true")
    meta_qa_pipeline_parser.add_argument("--apply-candidates", action="store_true")
    meta_qa_pipeline_parser.add_argument("--candidate-path", default=None)
    meta_qa_pipeline_parser.add_argument("--search-results-path", default=None)
    meta_qa_pipeline_parser.add_argument("--results-per-task", type=int, default=3)
    meta_qa_pipeline_parser.add_argument("--candidate-min-score", type=int, default=4)
    meta_qa_pipeline_parser.add_argument("--dry-run-candidates", action="store_true")
    meta_qa_pipeline_parser.add_argument("--planner-use-llm", action="store_true")
    meta_qa_pipeline_parser.add_argument("--planner-api-key", default=None)
    meta_qa_pipeline_parser.add_argument("--planner-base-url", default="https://api.z.ai/api/coding/paas/v4")
    meta_qa_pipeline_parser.add_argument("--planner-model", default="glm-5.1")
    meta_qa_pipeline_parser.add_argument("--force-plan", action="store_true")
    meta_qa_pipeline_parser.add_argument("--synthesize-answers", action="store_true")
    meta_qa_pipeline_parser.add_argument("--synthesis-use-llm", action="store_true")
    meta_qa_pipeline_parser.add_argument("--synthesis-api-key", default=None)
    meta_qa_pipeline_parser.add_argument("--synthesis-base-url", default="https://api.z.ai/api/coding/paas/v4")
    meta_qa_pipeline_parser.add_argument("--synthesis-model", default="glm-5.1")
    meta_qa_pipeline_parser.add_argument("--write-professional-report", action="store_true")
    meta_qa_pipeline_parser.add_argument("--professional-report-use-llm", action="store_true")
    meta_qa_pipeline_parser.add_argument("--professional-report-api-key", default=None)
    meta_qa_pipeline_parser.add_argument("--professional-report-base-url", default="https://api.z.ai/api/coding/paas/v4")
    meta_qa_pipeline_parser.add_argument("--professional-report-model", default="glm-5.1")
    meta_qa_pipeline_parser.add_argument("--timeout", type=int, default=10)

    plan_meta_qa_parser = subparsers.add_parser(
        "plan-meta-qa",
        help="Create or refresh the auditable question plan for a generic QA project",
    )
    plan_meta_qa_parser.add_argument("--object-type", required=True, choices=meta_qa_object_types)
    plan_meta_qa_parser.add_argument("--object-id", default="")
    plan_meta_qa_parser.add_argument("--meta-question", required=True)
    plan_meta_qa_parser.add_argument("--project-id", default=None)
    plan_meta_qa_parser.add_argument("--max-depth", type=int, default=3)
    plan_meta_qa_parser.add_argument("--force", action="store_true")
    plan_meta_qa_parser.add_argument("--use-llm", action="store_true")
    plan_meta_qa_parser.add_argument("--api-key", default=None)
    plan_meta_qa_parser.add_argument("--base-url", default="https://api.z.ai/api/coding/paas/v4")
    plan_meta_qa_parser.add_argument("--model", default="glm-5.1")

    add_meta_qa_parser = subparsers.add_parser(
        "add-meta-qa-question",
        help="Add a question to a generic layered QA project and rebuild it",
    )
    add_meta_qa_parser.add_argument("--project-id", required=True)
    add_meta_qa_parser.add_argument("--parent-id", required=True)
    add_meta_qa_parser.add_argument("--question", required=True)
    add_meta_qa_parser.add_argument("--terminal", action="store_true")

    record_meta_qa_parser = subparsers.add_parser(
        "record-meta-qa-information",
        help="Record a collected source for a generic QA project node",
    )
    record_meta_qa_parser.add_argument("--project-id", required=True)
    record_meta_qa_parser.add_argument("--node-id", required=True)
    record_meta_qa_parser.add_argument(
        "--category",
        required=True,
        choices=["evidence", "research_report", "message", "opinion"],
    )
    record_meta_qa_parser.add_argument("--source-type", required=True)
    record_meta_qa_parser.add_argument("--source-name", required=True)
    record_meta_qa_parser.add_argument("--url", required=True)
    record_meta_qa_parser.add_argument("--summary", required=True)
    record_meta_qa_parser.add_argument("--reliability", default="medium", choices=["primary", "high", "medium", "low"])
    record_meta_qa_parser.add_argument("--materiality", default="medium", choices=["low", "medium", "high", "thesis_change"])
    record_meta_qa_parser.add_argument("--published-at", default=None)

    meta_qa_tasks_parser = subparsers.add_parser(
        "build-meta-qa-collection-tasks",
        help="Build actionable four-bucket collection tasks for a generic QA project",
    )
    meta_qa_tasks_parser.add_argument("--project-id", required=True)
    meta_qa_tasks_parser.add_argument("--include-matched", action="store_true")
    meta_qa_tasks_parser.add_argument("--limit", type=int, default=None)

    run_meta_qa_tasks_parser = subparsers.add_parser(
        "run-meta-qa-collection-tasks",
        help="Run generic QA collection tasks against the project evidence corpus and bind matched sources",
    )
    run_meta_qa_tasks_parser.add_argument("--project-id", required=True)
    run_meta_qa_tasks_parser.add_argument("--include-matched", action="store_true")
    run_meta_qa_tasks_parser.add_argument("--limit", type=int, default=None)
    run_meta_qa_tasks_parser.add_argument("--min-score", type=int, default=4)
    run_meta_qa_tasks_parser.add_argument("--max-sources-per-task", type=int, default=1)
    run_meta_qa_tasks_parser.add_argument("--dry-run", action="store_true")

    discover_meta_candidates_parser = subparsers.add_parser(
        "discover-meta-qa-source-candidates",
        help="Search or import candidate URLs for generic QA collection tasks",
    )
    discover_meta_candidates_parser.add_argument("--project-id", required=True)
    discover_meta_candidates_parser.add_argument("--include-matched", action="store_true")
    discover_meta_candidates_parser.add_argument("--limit", type=int, default=None)
    discover_meta_candidates_parser.add_argument("--results-per-task", type=int, default=3)
    discover_meta_candidates_parser.add_argument("--min-score", type=int, default=4)
    discover_meta_candidates_parser.add_argument("--timeout", type=int, default=10)
    discover_meta_candidates_parser.add_argument("--search-results-path", default=None)

    apply_meta_candidates_parser = subparsers.add_parser(
        "apply-meta-qa-source-candidates",
        help="Fetch accepted generic QA source candidates and bind them to QA nodes",
    )
    apply_meta_candidates_parser.add_argument("--project-id", required=True)
    apply_meta_candidates_parser.add_argument("--path", required=True)
    apply_meta_candidates_parser.add_argument("--min-score", type=int, default=4)
    apply_meta_candidates_parser.add_argument("--limit", type=int, default=None)
    apply_meta_candidates_parser.add_argument("--timeout", type=int, default=10)
    apply_meta_candidates_parser.add_argument("--dry-run", action="store_true")

    import_meta_qa_parser = subparsers.add_parser(
        "import-meta-qa-information",
        help="Batch-import collected generic QA sources from a JSONL file",
    )
    import_meta_qa_parser.add_argument("--project-id", required=True)
    import_meta_qa_parser.add_argument("--path", required=True)

    meta_synthesis_tasks_parser = subparsers.add_parser(
        "build-meta-qa-synthesis-tasks",
        help="Build professional answer-synthesis tasks for generic QA nodes",
    )
    meta_synthesis_tasks_parser.add_argument("--project-id", required=True)
    meta_synthesis_tasks_parser.add_argument("--all-nodes", dest="leaf_only", action="store_false", default=True)
    meta_synthesis_tasks_parser.add_argument("--limit", type=int, default=None)

    import_meta_synthesis_parser = subparsers.add_parser(
        "import-meta-qa-answer-synthesis",
        help="Batch-import synthesized professional generic QA answers from JSONL",
    )
    import_meta_synthesis_parser.add_argument("--project-id", required=True)
    import_meta_synthesis_parser.add_argument("--path", required=True)

    run_meta_synthesis_parser = subparsers.add_parser(
        "run-meta-qa-answer-synthesis",
        help="Generate and optionally apply professional generic QA answers",
    )
    run_meta_synthesis_parser.add_argument("--project-id", required=True)
    run_meta_synthesis_parser.add_argument("--all-nodes", dest="leaf_only", action="store_false", default=True)
    run_meta_synthesis_parser.add_argument("--limit", type=int, default=None)
    run_meta_synthesis_parser.add_argument("--no-apply", dest="apply", action="store_false", default=True)
    run_meta_synthesis_parser.add_argument("--use-llm", action="store_true")
    run_meta_synthesis_parser.add_argument("--api-key", default=None)
    run_meta_synthesis_parser.add_argument("--base-url", default="https://api.z.ai/api/coding/paas/v4")
    run_meta_synthesis_parser.add_argument("--model", default="glm-5.1")

    meta_professional_report_parser = subparsers.add_parser(
        "write-meta-qa-professional-report",
        help="Write a professional report from a generic QA project",
    )
    meta_professional_report_parser.add_argument("--project-id", required=True)
    meta_professional_report_parser.add_argument("--use-llm", action="store_true")
    meta_professional_report_parser.add_argument("--api-key", default=None)
    meta_professional_report_parser.add_argument("--base-url", default="https://api.z.ai/api/coding/paas/v4")
    meta_professional_report_parser.add_argument("--model", default="glm-5.1")

    validate_meta_qa_parser = subparsers.add_parser(
        "validate-meta-qa-system",
        help="Validate that a generic meta-QA project satisfies the research contract",
    )
    validate_meta_qa_parser.add_argument("--project-id", required=True)
    validate_meta_qa_parser.add_argument("--require-professional-report", action="store_true")

    apply_meta_qa_queue_parser = subparsers.add_parser(
        "apply-meta-qa-question-queue",
        help="Apply queued generic QA questions from JSONL/JSON and rebuild report/tasks",
    )
    apply_meta_qa_queue_parser.add_argument("--project-id", required=True)
    apply_meta_qa_queue_parser.add_argument("--path", required=True)
    apply_meta_qa_queue_parser.add_argument("--no-build-tasks", dest="build_tasks", action="store_false", default=True)
    apply_meta_qa_queue_parser.add_argument("--run-local-collection", action="store_true")
    apply_meta_qa_queue_parser.add_argument("--limit", type=int, default=None)
    apply_meta_qa_queue_parser.add_argument("--min-score", type=int, default=4)
    apply_meta_qa_queue_parser.add_argument("--synthesize-answers", action="store_true")
    apply_meta_qa_queue_parser.add_argument("--synthesis-use-llm", action="store_true")
    apply_meta_qa_queue_parser.add_argument("--synthesis-api-key", default=None)
    apply_meta_qa_queue_parser.add_argument("--synthesis-base-url", default="https://api.z.ai/api/coding/paas/v4")
    apply_meta_qa_queue_parser.add_argument("--synthesis-model", default="glm-5.1")
    apply_meta_qa_queue_parser.add_argument("--write-professional-report", action="store_true")
    apply_meta_qa_queue_parser.add_argument("--professional-report-use-llm", action="store_true")
    apply_meta_qa_queue_parser.add_argument("--professional-report-api-key", default=None)
    apply_meta_qa_queue_parser.add_argument("--professional-report-base-url", default="https://api.z.ai/api/coding/paas/v4")
    apply_meta_qa_queue_parser.add_argument("--professional-report-model", default="glm-5.1")

    fetch_meta_qa_parser = subparsers.add_parser(
        "fetch-meta-qa-information-url",
        help="Fetch a URL, summarize it, bind it to a generic QA node, and rebuild",
    )
    fetch_meta_qa_parser.add_argument("--project-id", required=True)
    fetch_meta_qa_parser.add_argument("--node-id", required=True)
    fetch_meta_qa_parser.add_argument(
        "--category",
        required=True,
        choices=["evidence", "research_report", "message", "opinion"],
    )
    fetch_meta_qa_parser.add_argument("--url", required=True)
    fetch_meta_qa_parser.add_argument("--source-type", default=None)
    fetch_meta_qa_parser.add_argument("--source-name", default=None)
    fetch_meta_qa_parser.add_argument("--summary", default=None)
    fetch_meta_qa_parser.add_argument("--reliability", default=None, choices=["primary", "high", "medium", "low"])
    fetch_meta_qa_parser.add_argument("--materiality", default=None, choices=["low", "medium", "high", "thesis_change"])
    fetch_meta_qa_parser.add_argument("--published-at", default=None)
    fetch_meta_qa_parser.add_argument("--timeout", type=int, default=10)

    sec_parser = subparsers.add_parser("ingest-sec", help="Fetch SEC EDGAR data for a ticker")
    sec_parser.add_argument("ticker")
    sec_parser.add_argument("--user-agent", default="value-invest-research/0.1.0 research@example.com")
    sec_parser.add_argument("--include-facts", action="store_true", default=True)
    sec_parser.add_argument("--no-facts", dest="include_facts", action="store_false")

    prices_parser = subparsers.add_parser("ingest-prices", help="Fetch price history for a ticker")
    prices_parser.add_argument("ticker")
    prices_parser.add_argument("--period", default="1y")

    memo_parser = subparsers.add_parser("update-memo", help="Run LLM memo update for a ticker")
    memo_parser.add_argument("ticker")
    memo_parser.add_argument("--api-key", default=None)
    memo_parser.add_argument("--base-url", default="https://api.z.ai/api/coding/paas/v4")
    memo_parser.add_argument("--model", default="glm-5.1")

    stock_research_parser = subparsers.add_parser("research-stock", help="Run foundation-first stock research")
    stock_research_parser.add_argument("ticker")
    stock_research_parser.add_argument("--api-key", default=None)
    stock_research_parser.add_argument("--base-url", default="https://api.z.ai/api/coding/paas/v4")
    stock_research_parser.add_argument("--model", default="glm-5.1")

    event_research_parser = subparsers.add_parser("research-event", help="Run LLM event research")
    event_research_parser.add_argument("event_date")
    event_research_parser.add_argument("event_name")
    event_research_parser.add_argument("--description", required=True)
    event_research_parser.add_argument("--playbook", default=None)
    event_research_parser.add_argument("--api-key", default=None)
    event_research_parser.add_argument("--base-url", default="https://api.z.ai/api/coding/paas/v4")
    event_research_parser.add_argument("--model", default="glm-5.1")

    sector_research_parser = subparsers.add_parser("research-sector", help="Run LLM sector or theme research")
    sector_research_parser.add_argument("sector_name")
    sector_research_parser.add_argument("--type", choices=["sector", "theme"], default="sector")
    sector_research_parser.add_argument("--focus", required=True)
    sector_research_parser.add_argument("--tickers", nargs="*", default=None)
    sector_research_parser.add_argument("--api-key", default=None)
    sector_research_parser.add_argument("--base-url", default="https://api.z.ai/api/coding/paas/v4")
    sector_research_parser.add_argument("--model", default="glm-5.1")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path(args.root)

    try:
        if args.command == "init-stock":
            path = init_stock(root, args.ticker, args.company_name)
            print(path)
            return 0
        if args.command == "init-event":
            path = init_event(root, args.event_date, args.event_name)
            print(path)
            return 0
        if args.command == "validate-evidence":
            return validate_evidence_file(Path(args.path))
        if args.command == "build-evidence":
            return run_build_evidence(root, args.ticker)
        if args.command == "build-research-graph":
            return run_research_graph_cmd(root, args.ticker, "report")
        if args.command == "build-consensus":
            return run_research_graph_cmd(root, args.ticker, "consensus")
        if args.command == "generate-questions":
            return run_research_graph_cmd(root, args.ticker, "questions")
        if args.command == "build-hypotheses":
            return run_research_graph_cmd(root, args.ticker, "hypotheses")
        if args.command == "test-hypotheses":
            return run_research_graph_cmd(root, args.ticker, "tests")
        if args.command == "write-forward-report":
            return run_research_graph_cmd(root, args.ticker, "report")
        if args.command == "build-research-system":
            return run_research_system_cmd(root, args.ticker)
        if args.command == "validate-qa-system":
            return run_validate_qa_system_cmd(root, args)
        if args.command == "run-stock-qa-pipeline":
            return run_stock_qa_pipeline_cmd(root, args)
        if args.command == "add-research-question":
            return run_add_research_question_cmd(root, args)
        if args.command == "record-question-information":
            return run_record_question_information_cmd(root, args)
        if args.command == "build-collection-tasks":
            return run_build_collection_tasks_cmd(root, args)
        if args.command == "run-collection-tasks":
            return run_run_collection_tasks_cmd(root, args)
        if args.command == "discover-source-candidates":
            return run_discover_source_candidates_cmd(root, args)
        if args.command == "apply-source-candidates":
            return run_apply_source_candidates_cmd(root, args)
        if args.command == "import-question-information":
            return run_import_question_information_cmd(root, args)
        if args.command == "build-synthesis-tasks":
            return run_build_synthesis_tasks_cmd(root, args)
        if args.command == "import-answer-synthesis":
            return run_import_answer_synthesis_cmd(root, args)
        if args.command == "run-answer-synthesis":
            return run_answer_synthesis_cmd(root, args)
        if args.command == "build-leaf-research-tasks":
            return run_build_leaf_research_tasks_cmd(root, args)
        if args.command == "run-leaf-research":
            return run_leaf_research_cmd(root, args)
        if args.command == "import-leaf-research-results":
            return run_import_leaf_research_results_cmd(root, args)
        if args.command == "synthesize-leaf-answers":
            return run_synthesize_leaf_answers_cmd(root, args)
        if args.command == "rollup-research-answers":
            return run_rollup_research_answers_cmd(root, args)
        if args.command == "write-professional-report":
            return run_write_professional_report_cmd(root, args)
        if args.command == "apply-question-queue":
            return run_apply_question_queue_cmd(root, args)
        if args.command == "fetch-question-information-url":
            return run_fetch_question_information_url_cmd(root, args)
        if args.command == "build-meta-qa":
            return run_build_meta_qa_cmd(root, args)
        if args.command == "run-meta-qa-pipeline":
            return run_meta_qa_pipeline_cmd(root, args)
        if args.command == "plan-meta-qa":
            return run_plan_meta_qa_cmd(root, args)
        if args.command == "add-meta-qa-question":
            return run_add_meta_qa_question_cmd(root, args)
        if args.command == "record-meta-qa-information":
            return run_record_meta_qa_information_cmd(root, args)
        if args.command == "build-meta-qa-collection-tasks":
            return run_build_meta_qa_collection_tasks_cmd(root, args)
        if args.command == "run-meta-qa-collection-tasks":
            return run_run_meta_qa_collection_tasks_cmd(root, args)
        if args.command == "discover-meta-qa-source-candidates":
            return run_discover_meta_qa_source_candidates_cmd(root, args)
        if args.command == "apply-meta-qa-source-candidates":
            return run_apply_meta_qa_source_candidates_cmd(root, args)
        if args.command == "import-meta-qa-information":
            return run_import_meta_qa_information_cmd(root, args)
        if args.command == "build-meta-qa-synthesis-tasks":
            return run_build_meta_qa_synthesis_tasks_cmd(root, args)
        if args.command == "import-meta-qa-answer-synthesis":
            return run_import_meta_qa_answer_synthesis_cmd(root, args)
        if args.command == "run-meta-qa-answer-synthesis":
            return run_meta_qa_answer_synthesis_cmd(root, args)
        if args.command == "write-meta-qa-professional-report":
            return run_write_meta_qa_professional_report_cmd(root, args)
        if args.command == "validate-meta-qa-system":
            return run_validate_meta_qa_system_cmd(root, args)
        if args.command == "apply-meta-qa-question-queue":
            return run_apply_meta_qa_question_queue_cmd(root, args)
        if args.command == "fetch-meta-qa-information-url":
            return run_fetch_meta_qa_information_url_cmd(root, args)
        if args.command == "ingest-sec":
            return run_sec_ingest(root, args.ticker, args.user_agent, args.include_facts)
        if args.command == "ingest-prices":
            return run_price_ingest(root, args.ticker, args.period)
        if args.command == "update-memo":
            return run_memo_update(root, args.ticker, args.api_key, args.base_url, args.model)
        if args.command == "research-stock":
            return run_stock_research_cmd(root, args)
        if args.command == "research-event":
            return run_event_research_cmd(root, args)
        if args.command == "research-sector":
            return run_sector_research_cmd(root, args)
    except (ValueError, ValidationError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    parser.error(f"unknown command {args.command}")
    return 2


def validate_evidence_file(path: Path) -> int:
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            EvidenceRecord.from_dict(json.loads(line))
        except (json.JSONDecodeError, ValidationError) as exc:
            print(f"{path}:{line_number}: {exc}", file=sys.stderr)
            return 1
    return 0


def run_build_evidence(root: Path, ticker: str) -> int:
    from value_invest_research.evidence_builder import build_stock_evidence

    result = build_stock_evidence(root, ticker)
    print(
        f"Evidence built for {result['ticker']}: "
        f"records_fetched={result['records_fetched']}, "
        f"records_new={result['records_new']}, "
        f"path={result['evidence_path']}"
    )
    return 0


def run_research_graph_cmd(root: Path, ticker: str, stage: str) -> int:
    from value_invest_research.research_graph import run_research_graph_stage

    result = run_research_graph_stage(root, ticker, stage)
    print(
        f"Research graph built for {result['ticker']}: "
        f"stage={result['stage']}, "
        f"nodes={result['nodes']}, "
        f"edges={result['edges']}, "
        f"nodes_path={result['nodes_path']}, "
        f"edges_path={result['edges_path']}"
    )
    if result["report_path"]:
        print(f"Forward report saved: {result['report_path']}")
    return 0


def run_research_system_cmd(root: Path, ticker: str) -> int:
    from value_invest_research.research_system import build_research_system

    result = build_research_system(root, ticker)
    print(
        f"Research system built for {result['ticker']}: "
        f"foundation_status={result['foundation_status']}, "
        f"sections_covered={result['sections_covered']}, "
        f"questions={result['questions']}, "
        f"messages={result['messages']}, "
        f"dashboard={result['dashboard_path']}, "
        f"report={result['report_path']}, "
        f"information={result['information_collection_path']}"
    )
    return 0


def run_validate_qa_system_cmd(root: Path, args) -> int:
    from value_invest_research.qa_system_validation import validate_stock_qa_system

    result = validate_stock_qa_system(
        root,
        args.ticker,
        require_professional_report=args.require_professional_report,
    )
    _print_qa_validation_result("Stock QA validation", result)
    return 0 if result["ok"] else 1


def run_stock_qa_pipeline_cmd(root: Path, args) -> int:
    from value_invest_research.research_pipeline import run_stock_qa_pipeline

    synthesis_client = (
        _get_llm_client(args.synthesis_api_key, args.synthesis_base_url, args.synthesis_model)
        if args.synthesize_answers and args.synthesis_use_llm
        else None
    )
    professional_report_client = (
        _get_llm_client(args.professional_report_api_key, args.professional_report_base_url, args.professional_report_model)
        if args.write_professional_report and args.professional_report_use_llm
        else None
    )
    result = run_stock_qa_pipeline(
        root,
        args.ticker,
        task_limit=args.task_limit,
        run_local_collection=args.run_local_collection,
        discover_candidates=args.discover_candidates,
        apply_candidates=args.apply_candidates,
        candidate_path=Path(args.candidate_path) if args.candidate_path else None,
        search_results_path=Path(args.search_results_path) if args.search_results_path else None,
        results_per_task=args.results_per_task,
        candidate_min_score=args.candidate_min_score,
        dry_run_candidates=args.dry_run_candidates,
        synthesize_answers=args.synthesize_answers,
        synthesis_client=synthesis_client,
        write_professional_report=args.write_professional_report,
        professional_report_client=professional_report_client,
        leaf_research_provider=args.leaf_research_provider,
        leaf_research_input=Path(args.leaf_research_input) if args.leaf_research_input else None,
        leaf_research_limit=args.leaf_research_limit,
        timeout=args.timeout,
    )
    final = result["final"]
    print(
        f"Stock QA pipeline completed for {result['object_id']}: "
        f"stages={len(result['stages'])}, "
        f"report={final['report_path']}, "
        f"tasks={final['task_path']}, "
        f"synthesis_tasks={final['synthesis_task_path']}, "
        f"synthesis_mode={final['synthesis_mode']}, "
        f"leaf_results={final['leaf_research_result_path']}, "
        f"leaf_answers={final['leaf_answer_path']}, "
        f"leaf_rollups={final['rollup_answer_path']}, "
        f"professional_report={final['professional_report_path']}, "
        f"candidates={final['candidate_path']}, "
        f"run={Path(final['report_path']).parent / 'pipeline_run.json'}"
    )
    return 0


def run_add_research_question_cmd(root: Path, args) -> int:
    from value_invest_research.research_system import add_research_question

    result = add_research_question(root, args.ticker, args.parent_id, args.question, terminal=args.terminal)
    created = "created" if result["created"] else "existing"
    print(
        f"Research question {created} for {result['ticker']}: "
        f"question_id={result['question_id']}, "
        f"parent_id={result['parent_id']}, "
        f"terminal={args.terminal}, "
        f"custom_questions={result['custom_questions_path']}, "
        f"dashboard={result['dashboard_path']}, "
        f"report={result['report_path']}, "
        f"information={result['information_collection_path']}"
    )
    return 0


def run_record_question_information_cmd(root: Path, args) -> int:
    from value_invest_research.research_system import record_question_information

    result = record_question_information(
        root,
        args.ticker,
        args.node_id,
        args.category,
        args.source_type,
        args.source_name,
        args.url,
        args.summary,
        reliability=args.reliability,
        materiality=args.materiality,
        published_at=args.published_at,
    )
    action = "created" if result["created"] else "updated" if result["updated"] else "existing"
    print(
        f"Question information {action} for {result['ticker']}: "
        f"node_id={result['node_id']}, "
        f"category={result['category']}, "
        f"evidence_id={result['evidence_id']}, "
        f"evidence={result['evidence_path']}, "
        f"dashboard={result['dashboard_path']}, "
        f"report={result['report_path']}, "
        f"information={result['information_collection_path']}"
    )
    return 0


def run_build_collection_tasks_cmd(root: Path, args) -> int:
    from value_invest_research.information_collection import build_research_collection_tasks

    result = build_research_collection_tasks(
        root,
        args.ticker,
        include_matched=args.include_matched,
        limit=args.limit,
    )
    print(
        f"Collection tasks built for {result['ticker']}: "
        f"tasks={result['tasks']}, "
        f"leaf_questions={result['leaf_questions']}, "
        f"path={result['task_path']}, "
        f"information={result['information_collection_path']}"
    )
    return 0


def run_run_collection_tasks_cmd(root: Path, args) -> int:
    from value_invest_research.information_collection import run_research_collection_tasks

    result = run_research_collection_tasks(
        root,
        args.ticker,
        include_matched=args.include_matched,
        limit=args.limit,
        min_score=args.min_score,
        max_sources_per_task=args.max_sources_per_task,
        dry_run=args.dry_run,
    )
    mode = "dry-run" if result["dry_run"] else "applied"
    print(
        f"Collection tasks run for {result['ticker']}: "
        f"mode={mode}, "
        f"tasks={result['tasks']}, "
        f"matches={result['matches']}, "
        f"created={result['created']}, "
        f"updated={result['updated']}, "
        f"existing={result['existing']}, "
        f"results={result['result_path']}, "
        f"report={result['report_path']}"
    )
    return 0


def run_discover_source_candidates_cmd(root: Path, args) -> int:
    from value_invest_research.information_collection import discover_research_source_candidates

    result = discover_research_source_candidates(
        root,
        args.ticker,
        include_matched=args.include_matched,
        limit=args.limit,
        results_per_task=args.results_per_task,
        min_score=args.min_score,
        timeout=args.timeout,
        search_results_path=Path(args.search_results_path) if args.search_results_path else None,
    )
    print(
        f"Source candidates discovered for {result['ticker']}: "
        f"tasks={result['tasks']}, "
        f"candidates={result['candidates']}, "
        f"accepted={result['accepted_candidates']}, "
        f"path={result['candidate_path']}"
    )
    return 0


def run_apply_source_candidates_cmd(root: Path, args) -> int:
    from value_invest_research.information_collection import apply_research_source_candidates

    result = apply_research_source_candidates(
        root,
        args.ticker,
        Path(args.path),
        min_score=args.min_score,
        limit=args.limit,
        dry_run=args.dry_run,
        timeout=args.timeout,
    )
    mode = "dry-run" if result["dry_run"] else "applied"
    print(
        f"Source candidates applied for {result['ticker']}: "
        f"mode={mode}, "
        f"candidates={result['candidates']}, "
        f"applied={result['applied']}, "
        f"skipped={result['skipped']}, "
        f"results={result['result_path']}"
    )
    return 0


def run_import_question_information_cmd(root: Path, args) -> int:
    from value_invest_research.information_collection import import_question_information

    result = import_question_information(root, args.ticker, Path(args.path))
    print(
        f"Question information imported for {result['ticker']}: "
        f"records={result['records']}, "
        f"created={result['created']}, "
        f"updated={result['updated']}, "
        f"existing={result['existing']}, "
        f"report={result['report_path']}, "
        f"information={result['information_collection_path']}"
    )
    return 0


def run_build_synthesis_tasks_cmd(root: Path, args) -> int:
    from value_invest_research.answer_synthesis import build_stock_synthesis_tasks

    result = build_stock_synthesis_tasks(
        root,
        args.ticker,
        leaf_only=args.leaf_only,
        limit=args.limit,
    )
    scope = "leaf-only" if result["leaf_only"] else "all-nodes"
    print(
        f"Answer synthesis tasks built for {result['ticker']}: "
        f"scope={scope}, "
        f"tasks={result['synthesis_tasks']}, "
        f"path={result['synthesis_task_path']}, "
        f"report={result['report_path']}"
    )
    return 0


def run_import_answer_synthesis_cmd(root: Path, args) -> int:
    from value_invest_research.answer_synthesis import import_stock_answer_synthesis

    result = import_stock_answer_synthesis(root, args.ticker, Path(args.path))
    print(
        f"Answer synthesis imported for {result['ticker']}: "
        f"records={result['records']}, "
        f"applied_nodes={result['applied_nodes']}, "
        f"overrides={result['synthesis_override_path']}, "
        f"report={result['report_path']}, "
        f"information={result['information_collection_path']}"
    )
    return 0


def run_answer_synthesis_cmd(root: Path, args) -> int:
    from value_invest_research.answer_synthesis import run_stock_answer_synthesis

    client = _get_llm_client(args.api_key, args.base_url, args.model) if args.use_llm else None
    result = run_stock_answer_synthesis(
        root,
        args.ticker,
        leaf_only=args.leaf_only,
        limit=args.limit,
        apply=args.apply,
        client=client,
    )
    mode = "applied" if result["applied"] else "drafted"
    print(
        f"Answer synthesis {mode} for {result['ticker']}: "
        f"mode={result['synthesis_mode']}, "
        f"answers={result['synthesized_answers']}, "
        f"applied_nodes={result['applied_nodes']}, "
        f"answers_path={result['synthesized_answer_path']}, "
        f"tasks={result['synthesis_task_path']}, "
        f"report={result['report_path']}"
    )
    return 0


def run_build_leaf_research_tasks_cmd(root: Path, args) -> int:
    from value_invest_research.leaf_research import build_leaf_research_tasks

    result = build_leaf_research_tasks(
        root,
        args.ticker,
        limit=args.limit,
        include_completed=args.include_completed,
    )
    print(
        f"Leaf research tasks built for {result['ticker']}: "
        f"tasks={result['tasks']}, "
        f"leaf_questions={result['leaf_questions']}, "
        f"path={result['task_path']}, "
        f"report={result['report_path']}"
    )
    return 0


def run_leaf_research_cmd(root: Path, args) -> int:
    from value_invest_research.leaf_research import run_leaf_research

    result = run_leaf_research(
        root,
        args.ticker,
        provider=args.provider,
        input_path=Path(args.input) if args.input else None,
        limit=args.limit,
    )
    print(
        f"Leaf research run for {result['ticker']}: "
        f"provider={result['provider']}, "
        f"results={result['results']}, "
        f"sources={result['sources']}, "
        f"results_path={result['result_path']}, "
        f"sources_path={result['source_path']}"
    )
    return 0


def run_import_leaf_research_results_cmd(root: Path, args) -> int:
    from value_invest_research.leaf_research import import_leaf_research_results

    result = import_leaf_research_results(root, args.ticker, Path(args.path))
    print(
        f"Leaf research results imported for {result['ticker']}: "
        f"records={result['records']}, "
        f"sources={result['sources']}, "
        f"results_path={result['result_path']}, "
        f"sources_path={result['source_path']}"
    )
    return 0


def run_synthesize_leaf_answers_cmd(root: Path, args) -> int:
    from value_invest_research.leaf_research import synthesize_leaf_answers

    result = synthesize_leaf_answers(root, args.ticker)
    print(
        f"Leaf answers synthesized for {result['ticker']}: "
        f"answers={result['answers']}, "
        f"answers_path={result['answer_path']}, "
        f"source_results={result['source_result_path']}, "
        f"report={result['report_path']}"
    )
    return 0


def run_rollup_research_answers_cmd(root: Path, args) -> int:
    from value_invest_research.leaf_research import rollup_research_answers

    result = rollup_research_answers(root, args.ticker)
    print(
        f"Leaf research rollups written for {result['ticker']}: "
        f"rollups={result['rollups']}, "
        f"path={result['rollup_path']}, "
        f"report={result['report_path']}"
    )
    return 0


def run_write_professional_report_cmd(root: Path, args) -> int:
    from value_invest_research.report_synthesis import write_stock_professional_report

    client = _get_llm_client(args.api_key, args.base_url, args.model) if args.use_llm else None
    result = write_stock_professional_report(root, args.ticker, client=client)
    print(
        f"Professional report written for {result['ticker']}: "
        f"mode={result['report_mode']}, "
        f"leaf_questions={result['leaf_questions']}, "
        f"report={result['professional_report_path']}, "
        f"markdown={result['professional_report_md_path']}"
    )
    return 0


def run_apply_question_queue_cmd(root: Path, args) -> int:
    from value_invest_research.question_queue import apply_research_question_queue

    synthesis_client = (
        _get_llm_client(args.synthesis_api_key, args.synthesis_base_url, args.synthesis_model)
        if args.synthesize_answers and args.synthesis_use_llm
        else None
    )
    professional_report_client = (
        _get_llm_client(args.professional_report_api_key, args.professional_report_base_url, args.professional_report_model)
        if args.write_professional_report and args.professional_report_use_llm
        else None
    )
    result = apply_research_question_queue(
        root,
        args.ticker,
        Path(args.path),
        build_tasks=args.build_tasks,
        run_local_collection=args.run_local_collection,
        limit=args.limit,
        min_score=args.min_score,
        synthesize_answers=args.synthesize_answers,
        synthesis_client=synthesis_client,
        write_professional_report=args.write_professional_report,
        professional_report_client=professional_report_client,
    )
    print(
        f"Question queue applied for {result['ticker']}: "
        f"records={result['records']}, "
        f"created={result['created']}, "
        f"existing={result['existing']}, "
        f"tasks={result['tasks']}, "
        f"matches={result['matches']}, "
        f"report={result['report_path']}, "
        f"information={result['information_collection_path']}, "
        f"tasks_path={result['task_path']}, "
        f"synthesis_mode={result['synthesis_mode']}, "
        f"answers={result['synthesized_answers']}, "
        f"answers_path={result['synthesized_answer_path']}, "
        f"professional_report={result['professional_report_path']}"
    )
    return 0


def run_fetch_question_information_url_cmd(root: Path, args) -> int:
    from value_invest_research.information_collection import fetch_question_information_url

    result = fetch_question_information_url(
        root,
        args.ticker,
        args.node_id,
        args.category,
        args.url,
        source_type=args.source_type,
        source_name=args.source_name,
        summary=args.summary,
        reliability=args.reliability,
        materiality=args.materiality,
        published_at=args.published_at,
        timeout=args.timeout,
    )
    action = "created" if result["created"] else "updated" if result["updated"] else "existing"
    print(
        f"Question information URL fetched and {action} for {result['ticker']}: "
        f"node_id={result['node_id']}, "
        f"category={result['category']}, "
        f"source_name={result['source_name']}, "
        f"evidence_id={result['evidence_id']}, "
        f"fetched_log={result['fetched_log_path']}, "
        f"report={result['report_path']}"
    )
    return 0


def run_build_meta_qa_cmd(root: Path, args) -> int:
    from value_invest_research.meta_qa_research import build_meta_qa_research

    planner_client = (
        _get_llm_client(args.planner_api_key, args.planner_base_url, args.planner_model)
        if args.planner_use_llm
        else None
    )
    result = build_meta_qa_research(
        root,
        args.object_type,
        args.object_id,
        args.meta_question,
        project_id=args.project_id,
        max_depth=args.max_depth,
        planner_client=planner_client,
        force_plan=args.force_plan,
    )
    print(
        f"Meta QA research built: "
        f"project_id={result['project_id']}, "
        f"planning_mode={result['planning_mode']}, "
        f"nodes={result['nodes']}, "
        f"leaf_questions={result['leaf_questions']}, "
        f"plan={result['question_plan_path']}, "
        f"dashboard={result['dashboard_path']}, "
        f"report={result['report_path']}, "
        f"information={result['information_collection_path']}"
    )
    return 0


def run_meta_qa_pipeline_cmd(root: Path, args) -> int:
    from value_invest_research.research_pipeline import run_meta_qa_pipeline

    planner_client = (
        _get_llm_client(args.planner_api_key, args.planner_base_url, args.planner_model)
        if args.planner_use_llm
        else None
    )
    synthesis_client = (
        _get_llm_client(args.synthesis_api_key, args.synthesis_base_url, args.synthesis_model)
        if args.synthesize_answers and args.synthesis_use_llm
        else None
    )
    professional_report_client = (
        _get_llm_client(args.professional_report_api_key, args.professional_report_base_url, args.professional_report_model)
        if args.write_professional_report and args.professional_report_use_llm
        else None
    )
    result = run_meta_qa_pipeline(
        root,
        args.object_type,
        args.object_id,
        args.meta_question,
        project_id=args.project_id,
        max_depth=args.max_depth,
        task_limit=args.task_limit,
        run_local_collection=args.run_local_collection,
        discover_candidates=args.discover_candidates,
        apply_candidates=args.apply_candidates,
        candidate_path=Path(args.candidate_path) if args.candidate_path else None,
        search_results_path=Path(args.search_results_path) if args.search_results_path else None,
        results_per_task=args.results_per_task,
        candidate_min_score=args.candidate_min_score,
        dry_run_candidates=args.dry_run_candidates,
        planner_client=planner_client,
        force_plan=args.force_plan,
        synthesize_answers=args.synthesize_answers,
        synthesis_client=synthesis_client,
        write_professional_report=args.write_professional_report,
        professional_report_client=professional_report_client,
        timeout=args.timeout,
    )
    final = result["final"]
    print(
        f"Meta QA pipeline completed: "
        f"project_id={final['project_id']}, "
        f"planning_mode={final['planning_mode']}, "
        f"stages={len(result['stages'])}, "
        f"report={final['report_path']}, "
        f"tasks={final['task_path']}, "
        f"synthesis_tasks={final['synthesis_task_path']}, "
        f"synthesis_mode={final['synthesis_mode']}, "
        f"professional_report={final['professional_report_path']}, "
        f"candidates={final['candidate_path']}, "
        f"run={Path(final['project_dir']) / 'pipeline_run.json'}"
    )
    return 0


def run_plan_meta_qa_cmd(root: Path, args) -> int:
    from value_invest_research.meta_qa_research import plan_meta_qa_questions

    client = _get_llm_client(args.api_key, args.base_url, args.model) if args.use_llm else None
    result = plan_meta_qa_questions(
        root,
        args.object_type,
        args.object_id,
        args.meta_question,
        project_id=args.project_id,
        max_depth=args.max_depth,
        force=args.force,
        client=client,
    )
    action = "created" if result["created"] else "existing"
    print(
        f"Meta QA question plan {action}: "
        f"project_id={result['project_id']}, "
        f"planning_mode={result['planning_mode']}, "
        f"l1_questions={result['l1_questions']}, "
        f"leaf_questions={result['leaf_questions']}, "
        f"path={result['question_plan_path']}"
    )
    return 0


def run_add_meta_qa_question_cmd(root: Path, args) -> int:
    from value_invest_research.meta_qa_research import add_meta_qa_question

    result = add_meta_qa_question(root, args.project_id, args.parent_id, args.question, terminal=args.terminal)
    created = "created" if result["created"] else "existing"
    print(
        f"Meta QA question {created}: "
        f"project_id={result['project_id']}, "
        f"question_id={result['question_id']}, "
        f"terminal={args.terminal}, "
        f"dashboard={result['dashboard_path']}, "
        f"report={result['report_path']}, "
        f"information={result['information_collection_path']}"
    )
    return 0


def run_record_meta_qa_information_cmd(root: Path, args) -> int:
    from value_invest_research.meta_qa_research import record_meta_qa_information

    result = record_meta_qa_information(
        root,
        args.project_id,
        args.node_id,
        args.category,
        args.source_type,
        args.source_name,
        args.url,
        args.summary,
        reliability=args.reliability,
        materiality=args.materiality,
        published_at=args.published_at,
    )
    action = "created" if result["created"] else "updated" if result["updated"] else "existing"
    print(
        f"Meta QA information {action}: "
        f"project_id={result['project_id']}, "
        f"node_id={result['node_id']}, "
        f"category={result['category']}, "
        f"evidence_id={result['evidence_id']}, "
        f"evidence={result['evidence_path']}, "
        f"dashboard={result['dashboard_path']}, "
        f"report={result['report_path']}, "
        f"information={result['information_collection_path']}"
    )
    return 0


def run_build_meta_qa_collection_tasks_cmd(root: Path, args) -> int:
    from value_invest_research.information_collection import build_meta_qa_collection_tasks

    result = build_meta_qa_collection_tasks(
        root,
        args.project_id,
        include_matched=args.include_matched,
        limit=args.limit,
    )
    print(
        f"Meta QA collection tasks built: "
        f"project_id={result['project_id']}, "
        f"tasks={result['tasks']}, "
        f"leaf_questions={result['leaf_questions']}, "
        f"path={result['task_path']}, "
        f"information={result['information_collection_path']}"
    )
    return 0


def run_run_meta_qa_collection_tasks_cmd(root: Path, args) -> int:
    from value_invest_research.information_collection import run_meta_qa_collection_tasks

    result = run_meta_qa_collection_tasks(
        root,
        args.project_id,
        include_matched=args.include_matched,
        limit=args.limit,
        min_score=args.min_score,
        max_sources_per_task=args.max_sources_per_task,
        dry_run=args.dry_run,
    )
    mode = "dry-run" if result["dry_run"] else "applied"
    print(
        f"Meta QA collection tasks run: "
        f"project_id={result['project_id']}, "
        f"mode={mode}, "
        f"tasks={result['tasks']}, "
        f"matches={result['matches']}, "
        f"created={result['created']}, "
        f"updated={result['updated']}, "
        f"existing={result['existing']}, "
        f"results={result['result_path']}, "
        f"report={result['report_path']}"
    )
    return 0


def run_discover_meta_qa_source_candidates_cmd(root: Path, args) -> int:
    from value_invest_research.information_collection import discover_meta_qa_source_candidates

    result = discover_meta_qa_source_candidates(
        root,
        args.project_id,
        include_matched=args.include_matched,
        limit=args.limit,
        results_per_task=args.results_per_task,
        min_score=args.min_score,
        timeout=args.timeout,
        search_results_path=Path(args.search_results_path) if args.search_results_path else None,
    )
    print(
        f"Meta QA source candidates discovered: "
        f"project_id={result['project_id']}, "
        f"tasks={result['tasks']}, "
        f"candidates={result['candidates']}, "
        f"accepted={result['accepted_candidates']}, "
        f"path={result['candidate_path']}"
    )
    return 0


def run_apply_meta_qa_source_candidates_cmd(root: Path, args) -> int:
    from value_invest_research.information_collection import apply_meta_qa_source_candidates

    result = apply_meta_qa_source_candidates(
        root,
        args.project_id,
        Path(args.path),
        min_score=args.min_score,
        limit=args.limit,
        dry_run=args.dry_run,
        timeout=args.timeout,
    )
    mode = "dry-run" if result["dry_run"] else "applied"
    print(
        f"Meta QA source candidates applied: "
        f"project_id={result['project_id']}, "
        f"mode={mode}, "
        f"candidates={result['candidates']}, "
        f"applied={result['applied']}, "
        f"skipped={result['skipped']}, "
        f"results={result['result_path']}"
    )
    return 0


def run_import_meta_qa_information_cmd(root: Path, args) -> int:
    from value_invest_research.information_collection import import_meta_qa_information

    result = import_meta_qa_information(root, args.project_id, Path(args.path))
    print(
        f"Meta QA information imported: "
        f"project_id={result['project_id']}, "
        f"records={result['records']}, "
        f"created={result['created']}, "
        f"updated={result['updated']}, "
        f"existing={result['existing']}, "
        f"report={result['report_path']}, "
        f"information={result['information_collection_path']}"
    )
    return 0


def run_build_meta_qa_synthesis_tasks_cmd(root: Path, args) -> int:
    from value_invest_research.answer_synthesis import build_meta_qa_synthesis_tasks

    result = build_meta_qa_synthesis_tasks(
        root,
        args.project_id,
        leaf_only=args.leaf_only,
        limit=args.limit,
    )
    scope = "leaf-only" if result["leaf_only"] else "all-nodes"
    print(
        f"Meta QA answer synthesis tasks built: "
        f"project_id={result['project_id']}, "
        f"scope={scope}, "
        f"tasks={result['synthesis_tasks']}, "
        f"path={result['synthesis_task_path']}, "
        f"report={result['report_path']}"
    )
    return 0


def run_import_meta_qa_answer_synthesis_cmd(root: Path, args) -> int:
    from value_invest_research.answer_synthesis import import_meta_qa_answer_synthesis

    result = import_meta_qa_answer_synthesis(root, args.project_id, Path(args.path))
    print(
        f"Meta QA answer synthesis imported: "
        f"project_id={result['project_id']}, "
        f"records={result['records']}, "
        f"applied_nodes={result['applied_nodes']}, "
        f"overrides={result['synthesis_override_path']}, "
        f"report={result['report_path']}, "
        f"information={result['information_collection_path']}"
    )
    return 0


def run_meta_qa_answer_synthesis_cmd(root: Path, args) -> int:
    from value_invest_research.answer_synthesis import run_meta_qa_answer_synthesis

    client = _get_llm_client(args.api_key, args.base_url, args.model) if args.use_llm else None
    result = run_meta_qa_answer_synthesis(
        root,
        args.project_id,
        leaf_only=args.leaf_only,
        limit=args.limit,
        apply=args.apply,
        client=client,
    )
    mode = "applied" if result["applied"] else "drafted"
    print(
        f"Meta QA answer synthesis {mode}: "
        f"project_id={result['project_id']}, "
        f"mode={result['synthesis_mode']}, "
        f"answers={result['synthesized_answers']}, "
        f"applied_nodes={result['applied_nodes']}, "
        f"answers_path={result['synthesized_answer_path']}, "
        f"tasks={result['synthesis_task_path']}, "
        f"report={result['report_path']}"
    )
    return 0


def run_write_meta_qa_professional_report_cmd(root: Path, args) -> int:
    from value_invest_research.report_synthesis import write_meta_qa_professional_report

    client = _get_llm_client(args.api_key, args.base_url, args.model) if args.use_llm else None
    result = write_meta_qa_professional_report(root, args.project_id, client=client)
    print(
        f"Meta QA professional report written: "
        f"project_id={result['project_id']}, "
        f"mode={result['report_mode']}, "
        f"leaf_questions={result['leaf_questions']}, "
        f"report={result['professional_report_path']}, "
        f"markdown={result['professional_report_md_path']}"
    )
    return 0


def run_validate_meta_qa_system_cmd(root: Path, args) -> int:
    from value_invest_research.qa_system_validation import validate_meta_qa_system

    result = validate_meta_qa_system(
        root,
        args.project_id,
        require_professional_report=args.require_professional_report,
    )
    _print_qa_validation_result("Meta QA validation", result)
    return 0 if result["ok"] else 1


def run_apply_meta_qa_question_queue_cmd(root: Path, args) -> int:
    from value_invest_research.question_queue import apply_meta_qa_question_queue

    synthesis_client = (
        _get_llm_client(args.synthesis_api_key, args.synthesis_base_url, args.synthesis_model)
        if args.synthesize_answers and args.synthesis_use_llm
        else None
    )
    professional_report_client = (
        _get_llm_client(args.professional_report_api_key, args.professional_report_base_url, args.professional_report_model)
        if args.write_professional_report and args.professional_report_use_llm
        else None
    )
    result = apply_meta_qa_question_queue(
        root,
        args.project_id,
        Path(args.path),
        build_tasks=args.build_tasks,
        run_local_collection=args.run_local_collection,
        limit=args.limit,
        min_score=args.min_score,
        synthesize_answers=args.synthesize_answers,
        synthesis_client=synthesis_client,
        write_professional_report=args.write_professional_report,
        professional_report_client=professional_report_client,
    )
    print(
        f"Meta QA question queue applied: "
        f"project_id={result['project_id']}, "
        f"records={result['records']}, "
        f"created={result['created']}, "
        f"existing={result['existing']}, "
        f"tasks={result['tasks']}, "
        f"matches={result['matches']}, "
        f"report={result['report_path']}, "
        f"information={result['information_collection_path']}, "
        f"tasks_path={result['task_path']}, "
        f"synthesis_mode={result['synthesis_mode']}, "
        f"answers={result['synthesized_answers']}, "
        f"answers_path={result['synthesized_answer_path']}, "
        f"professional_report={result['professional_report_path']}"
    )
    return 0


def _print_qa_validation_result(label: str, result: dict) -> None:
    summary = result.get("summary", {})
    status = "OK" if result.get("ok") else "FAILED"
    print(
        f"{label} {status}: "
        f"object_id={result.get('object_id')}, "
        f"nodes={summary.get('nodes', 0)}, "
        f"leaf_questions={summary.get('leaf_questions', 0)}, "
        f"collection_rows={summary.get('collection_rows', 0)}, "
        f"errors={summary.get('errors', 0)}, "
        f"dashboard={summary.get('dashboard_path', '')}, "
        f"report={summary.get('report_path', '')}, "
        f"professional_report={summary.get('professional_report_path', '')}"
    )
    for issue in result.get("issues", [])[:10]:
        print(f"{issue.get('severity', 'error')}:{issue.get('code', '')}: {issue.get('message', '')}")


def run_fetch_meta_qa_information_url_cmd(root: Path, args) -> int:
    from value_invest_research.information_collection import fetch_meta_qa_information_url

    result = fetch_meta_qa_information_url(
        root,
        args.project_id,
        args.node_id,
        args.category,
        args.url,
        source_type=args.source_type,
        source_name=args.source_name,
        summary=args.summary,
        reliability=args.reliability,
        materiality=args.materiality,
        published_at=args.published_at,
        timeout=args.timeout,
    )
    action = "created" if result["created"] else "updated" if result["updated"] else "existing"
    print(
        f"Meta QA information URL fetched and {action}: "
        f"project_id={result['project_id']}, "
        f"node_id={result['node_id']}, "
        f"category={result['category']}, "
        f"source_name={result['source_name']}, "
        f"evidence_id={result['evidence_id']}, "
        f"fetched_log={result['fetched_log_path']}, "
        f"report={result['report_path']}"
    )
    return 0


def run_sec_ingest(root: Path, ticker: str, user_agent: str, include_facts: bool) -> int:
    from value_invest_research.ingest_sec import SecEdgarClient

    client = SecEdgarClient(user_agent=user_agent)
    cik_map = client.fetch_cik_map()
    normalized = ticker.strip().upper()
    if normalized not in cik_map:
        print(f"error: ticker {normalized} not found in SEC EDGAR", file=sys.stderr)
        return 2
    cik = cik_map[normalized]

    init_stock(root, normalized)
    client.fetch_submissions(root, normalized, cik)
    print(f"SEC submissions fetched for {normalized} (CIK {cik})")

    if include_facts:
        client.fetch_company_facts(root, normalized, cik)
        print(f"SEC company facts fetched for {normalized}")

    return 0


def run_price_ingest(root: Path, ticker: str, period: str) -> int:
    from value_invest_research.ingest_prices import fetch_price_history

    normalized = ticker.strip().upper()
    init_stock(root, normalized)
    fetch_price_history(root, normalized, period=period)
    print(f"Price history fetched for {normalized}")
    return 0


def run_memo_update(root: Path, ticker: str, api_key: str | None, base_url: str, model: str) -> int:
    import os

    from value_invest_research.llm import LlmClient, LlmConfig
    from value_invest_research.memo_updater import MemoUpdater

    key = api_key or os.environ.get("LLM_API_KEY", "")
    if not key:
        print("error: API key required (set LLM_API_KEY or pass --api-key)", file=sys.stderr)
        return 2

    config = LlmConfig(api_key=key, base_url=base_url, model=model)
    client = LlmClient(config)
    updater = MemoUpdater(client)

    result = updater.update_stock_memo(root, ticker)
    print(f"Memo update proposal saved: {result['proposal_path']}")
    print(f"Ticker: {result['ticker']}, Length: {result['response_length']} chars")
    return 0


def _get_llm_client(api_key: str | None, base_url: str, model: str) -> "LlmClient":
    import os

    from value_invest_research.llm import LlmClient, LlmConfig

    key = api_key or os.environ.get("LLM_API_KEY", "")
    if not key:
        print("error: API key required (set LLM_API_KEY or pass --api-key)", file=sys.stderr)
        raise SystemExit(2)
    return LlmClient(LlmConfig(api_key=key, base_url=base_url, model=model))


def run_event_research_cmd(root: Path, args) -> int:
    from value_invest_research.event_researcher import EventResearcher

    client = _get_llm_client(args.api_key, args.base_url, args.model)
    researcher = EventResearcher(client)

    result = researcher.run_event_research(
        root, args.event_date, args.event_name,
        event_description=args.description,
        playbook_name=args.playbook,
    )
    print(f"Event research saved: {result['analysis_path']}")
    print(f"Event: {result['event_name']}, Dir: {result['event_dir']}, Length: {result['response_length']} chars")
    return 0


def run_stock_research_cmd(root: Path, args) -> int:
    from value_invest_research.stock_researcher import StockResearcher

    client = _get_llm_client(args.api_key, args.base_url, args.model)
    researcher = StockResearcher(client)

    result = researcher.run_stock_research(root, args.ticker)
    print(f"Stock research saved: {result['report_path']}")
    print(f"Signal JSON saved: {result['signal_path']}")
    print(f"Ticker: {result['ticker']}, Length: {result['response_length']} chars")
    return 0


def run_sector_research_cmd(root: Path, args) -> int:
    from value_invest_research.sector_researcher import SectorResearcher

    client = _get_llm_client(args.api_key, args.base_url, args.model)
    researcher = SectorResearcher(client)

    result = researcher.run_sector_research(
        root, args.sector_name,
        sector_type=args.type,
        research_focus=args.focus,
        tickers_to_include=args.tickers,
    )
    print(f"Sector research saved: {result['analysis_path']}")
    print(f"Sector: {result['sector_name']} ({result['sector_type']}), Dir: {result['sector_dir']}, Length: {result['response_length']} chars")
    return 0
