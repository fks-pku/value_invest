from __future__ import annotations

import argparse
from datetime import date, timedelta
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

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

    report_contract_parser = subparsers.add_parser(
        "validate-report-contract",
        help="Validate a final Markdown or compatibility HTML report against the locked contract",
    )
    report_contract_parser.add_argument("path")
    report_contract_parser.add_argument("--mode", choices=["live_prediction", "historical_backtest"], default="historical_backtest")
    report_contract_parser.add_argument("--require-l3", action="store_true")

    time_slice_parser = subparsers.add_parser(
        "audit-time-slice",
        help="Audit source visibility against a historical backtest as-of date",
    )
    time_slice_parser.add_argument("path")
    time_slice_parser.add_argument("--as-of-date", required=True)

    research_artifacts_parser = subparsers.add_parser(
        "validate-research-artifacts",
        help="Validate QA, source-extraction, and target-observation internal contracts for a research project",
    )
    research_artifacts_parser.add_argument("project_dir")
    research_artifacts_parser.add_argument("--require-l3", action="store_true")

    material_intake_parser = subparsers.add_parser(
        "validate-material-intake",
        help="Validate material classification, BOM routing, parse tasks, and cutoff isolation",
    )
    material_intake_parser.add_argument("project_dir")

    standalone_engine_validation_parser = subparsers.add_parser(
        "validate-standalone-bom-engine",
        help=(
            "Validate the five-lens playbook, claim mappings, logic states, "
            "thesis revisions, and gated investment snapshot"
        ),
    )
    standalone_engine_validation_parser.add_argument("project_dir")
    standalone_engine_validation_parser.add_argument("--as-of-date", default=None)

    project_schema_parser = subparsers.add_parser(
        "validate-project-schema",
        help="Validate project.json against the four-stage pipeline schema",
    )
    project_schema_parser.add_argument("project_dir")

    industry_overview_parser = subparsers.add_parser(
        "validate-industry-overview",
        help="Validate that industry overview data is populated before Stage 3",
    )
    industry_overview_parser.add_argument("project_dir")

    render_project_report_parser = subparsers.add_parser(
        "render-research-report",
        help="Render a research project through the canonical ViewModel and report renderer",
    )
    render_project_report_parser.add_argument("project_dir")
    render_project_report_parser.add_argument("--filename", default="professional_report.md")

    search_bom_materials_parser = subparsers.add_parser(
        "search-bom-materials",
        help="Search one BOM x six-question coordinate and route sources into its parse inbox",
    )
    search_bom_materials_parser.add_argument("project_dir")
    search_bom_materials_parser.add_argument("--bom-node-id", required=True)
    search_bom_materials_parser.add_argument(
        "--question-number",
        required=True,
        type=int,
        choices=range(1, 7),
    )
    search_bom_materials_parser.add_argument("--query", required=True)
    search_bom_materials_parser.add_argument(
        "--provider",
        default="exa",
        choices=["exa", "perplexity", "openai_compatible"],
    )
    search_bom_materials_parser.add_argument("--max-sources", type=int, default=8)
    search_bom_materials_parser.add_argument("--discovered-at", default=None)

    scan_ima_materials_parser = subparsers.add_parser(
        "scan-ima-materials",
        help="Scan an IMA knowledge base and queue question-specific report parsing",
    )
    scan_ima_materials_parser.add_argument("project_dir")
    scan_ima_materials_parser.add_argument("--knowledge-base-id", default=None)
    scan_ima_materials_parser.add_argument("--knowledge-base-name", default=None)
    scan_ima_materials_parser.add_argument(
        "--config",
        default="config/material_feeds.json",
    )
    scan_ima_materials_parser.add_argument(
        "--bom-node-id",
        action="append",
        default=None,
    )
    scan_ima_materials_parser.add_argument("--max-results-per-query", type=int, default=None)
    scan_ima_materials_parser.add_argument("--discovered-at", default=None)
    scan_ima_materials_parser.add_argument("--start-date", default=None)
    scan_ima_materials_parser.add_argument("--end-date", default=None)
    scan_ima_materials_parser.add_argument(
        "--root-folder-pattern",
        default=None,
    )
    scan_ima_materials_parser.add_argument(
        "--skip-originals",
        action="store_true",
        help="Keep metadata only instead of downloading accessible original reports",
    )

    archive_ima_day_parser = subparsers.add_parser(
        "archive-ima-day",
        help=(
            "Legacy OpenAPI archive command; disabled when "
            "config archive_method=ui_click"
        ),
    )
    archive_ima_day_parser.add_argument("--date", required=True, dest="archive_date")
    archive_ima_day_parser.add_argument("--knowledge-base-id", default=None)
    archive_ima_day_parser.add_argument("--knowledge-base-name", default=None)
    archive_ima_day_parser.add_argument(
        "--config",
        default="config/ima_daily_archive.json",
    )
    archive_ima_day_parser.add_argument("--archive-root", default=None)
    archive_ima_day_parser.add_argument("--scanned-at", default=None)
    archive_ima_day_parser.add_argument("--root-folder-pattern", default=None)

    archive_ima_ui_day_parser = subparsers.add_parser(
        "archive-ima-ui-day",
        help=(
            "Register PDFs downloaded by visible IMA UI clicks into "
            "source/ima/YYYY/MM/DD"
        ),
    )
    archive_ima_ui_day_parser.add_argument(
        "--date",
        required=True,
        dest="archive_date",
    )
    archive_ima_ui_day_parser.add_argument("--candidate-list", required=True)
    archive_ima_ui_day_parser.add_argument("--download-dir", required=True)
    archive_ima_ui_day_parser.add_argument("--download-marker", default=None)
    archive_ima_ui_day_parser.add_argument(
        "--config",
        default="config/ima_daily_archive.json",
    )
    archive_ima_ui_day_parser.add_argument("--archive-root", default=None)
    archive_ima_ui_day_parser.add_argument("--scanned-at", default=None)

    archive_ima_daily_parser = subparsers.add_parser(
        "archive-ima-daily",
        help=(
            "Legacy OpenAPI daily archive; disabled when "
            "config archive_method=ui_click"
        ),
    )
    archive_ima_daily_parser.add_argument("--end-date", default=None)
    archive_ima_daily_parser.add_argument("--lookback-days", type=int, default=None)
    archive_ima_daily_parser.add_argument("--knowledge-base-id", default=None)
    archive_ima_daily_parser.add_argument("--knowledge-base-name", default=None)
    archive_ima_daily_parser.add_argument(
        "--config",
        default="config/ima_daily_archive.json",
    )
    archive_ima_daily_parser.add_argument("--archive-root", default=None)
    archive_ima_daily_parser.add_argument("--scanned-at", default=None)
    archive_ima_daily_parser.add_argument("--root-folder-pattern", default=None)

    validate_ima_archive_parser = subparsers.add_parser(
        "validate-ima-archive",
        help="Validate central IMA archive manifests, paths, hashes, and counts",
    )
    validate_ima_archive_parser.add_argument(
        "--config",
        default="config/ima_daily_archive.json",
    )
    validate_ima_archive_parser.add_argument("--archive-root", default=None)

    route_ima_archive_parser = subparsers.add_parser(
        "route-ima-archive-to-bom",
        help=(
            "Screen one central IMA archive day, copy relevant originals into "
            "a BOM project, and queue question-specific parsing"
        ),
    )
    route_ima_archive_parser.add_argument("project_dir")
    route_ima_archive_parser.add_argument(
        "--date",
        required=True,
        dest="archive_date",
    )
    route_ima_archive_parser.add_argument(
        "--archive-root",
        default="source/ima",
    )
    route_ima_archive_parser.add_argument("--discovered-at", default=None)
    route_ima_archive_parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear existing project materials, ledgers, conclusions, and report first",
    )

    refresh_standalone_parser = subparsers.add_parser(
        "refresh-standalone-bom-report",
        help=(
            "Rebuild a five-lens standalone BOM HTML report and Markdown audit "
            "sidecar from its timeline ledger"
        ),
    )
    refresh_standalone_parser.add_argument("project_dir")
    refresh_standalone_parser.add_argument("--as-of-date", default=None)

    apply_standalone_parser = subparsers.add_parser(
        "apply-standalone-bom-updates",
        help=(
            "Validate reviewed claim/conclusion JSONL and rebuild the standalone "
            "BOM HTML report plus Markdown audit sidecar"
        ),
    )
    apply_standalone_parser.add_argument("project_dir")
    apply_standalone_parser.add_argument("--claims", required=True)
    apply_standalone_parser.add_argument("--conclusions", required=True)
    apply_standalone_parser.add_argument("--as-of-date", default=None)

    apply_engine_parser = subparsers.add_parser(
        "apply-standalone-bom-engine-updates",
        help=(
            "Validate reviewed claim mappings, logic states, thesis revisions, "
            "and investment snapshots before rebuilding the standalone BOM report"
        ),
    )
    apply_engine_parser.add_argument("project_dir")
    apply_engine_parser.add_argument("--mappings", required=True)
    apply_engine_parser.add_argument("--logic-states", required=True)
    apply_engine_parser.add_argument("--entity-states", required=True)
    apply_engine_parser.add_argument("--revisions", required=True)
    apply_engine_parser.add_argument("--investment-snapshots", required=True)
    apply_engine_parser.add_argument("--as-of-date", default=None)

    publication_date_parser = subparsers.add_parser(
        "review-material-publication-date",
        help="Record a verified or unresolved source publication date and propagate it to intake artifacts",
    )
    publication_date_parser.add_argument("project_dir")
    publication_date_parser.add_argument("--source-id", required=True)
    publication_date_parser.add_argument("--published-at", default="")
    publication_date_parser.add_argument(
        "--status",
        required=True,
        choices=[
            "verified",
            "inferred_from_title",
            "needs_pdf_verification",
        ],
    )
    publication_date_parser.add_argument(
        "--source",
        required=True,
        choices=[
            "provider_published_at",
            "source_visible_at",
            "title_suffix",
            "pdf_cover",
            "manual_verification",
            "unknown",
        ],
    )
    publication_date_parser.add_argument("--locator", default="")

    directory_location_parser = subparsers.add_parser(
        "review-material-directory-location",
        help="Record or clear an IMA year/month/day archive location and move the local original",
    )
    directory_location_parser.add_argument("project_dir")
    directory_location_parser.add_argument("--source-id", required=True)
    directory_location_parser.add_argument("--directory-date", default="")
    directory_location_parser.add_argument("--directory-path", default="")
    directory_location_parser.add_argument(
        "--status",
        required=True,
        choices=["verified", "pending_directory_reconciliation"],
    )

    scan_active_ima_parser = subparsers.add_parser(
        "scan-active-ima-materials",
        help="Scan IMA for every enabled live research project in one registry",
    )
    scan_active_ima_parser.add_argument(
        "--config",
        default="config/active_research_feeds.json",
    )
    scan_active_ima_parser.add_argument("--discovered-at", default=None)
    scan_active_ima_parser.add_argument("--start-date", default=None)
    scan_active_ima_parser.add_argument("--end-date", default=None)
    scan_active_ima_parser.add_argument(
        "--full-backfill",
        action="store_true",
        help="Scan from each project's configured backfill_start_date",
    )
    scan_active_ima_parser.add_argument("--skip-originals", action="store_true")

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
    stock_pipeline_parser.add_argument("--leaf-research-provider", default=None, choices=["mock", "manual", "perplexity", "exa", "openai_compatible"])
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
    run_leaf_parser.add_argument("--provider", default="mock", choices=["mock", "manual", "perplexity", "exa", "openai_compatible"])
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
        if args.command == "validate-report-contract":
            return run_validate_report_contract_cmd(root, args)
        if args.command == "audit-time-slice":
            return run_audit_time_slice_cmd(root, args)
        if args.command == "validate-research-artifacts":
            return run_validate_research_artifacts_cmd(root, args)
        if args.command == "validate-material-intake":
            return run_validate_material_intake_cmd(root, args)
        if args.command == "validate-standalone-bom-engine":
            return run_validate_standalone_bom_engine_cmd(root, args)
        if args.command == "validate-project-schema":
            return run_validate_project_schema_cmd(root, args)
        if args.command == "validate-industry-overview":
            return run_validate_industry_overview_cmd(root, args)
        if args.command == "render-research-report":
            return run_render_research_report_cmd(root, args)
        if args.command == "search-bom-materials":
            return run_search_bom_materials_cmd(root, args)
        if args.command == "scan-ima-materials":
            return run_scan_ima_materials_cmd(root, args)
        if args.command == "archive-ima-day":
            return run_archive_ima_day_cmd(root, args)
        if args.command == "archive-ima-ui-day":
            return run_archive_ima_ui_day_cmd(root, args)
        if args.command == "archive-ima-daily":
            return run_archive_ima_daily_cmd(root, args)
        if args.command == "validate-ima-archive":
            return run_validate_ima_archive_cmd(root, args)
        if args.command == "route-ima-archive-to-bom":
            return run_route_ima_archive_to_bom_cmd(root, args)
        if args.command == "refresh-standalone-bom-report":
            return run_refresh_standalone_bom_report_cmd(root, args)
        if args.command == "apply-standalone-bom-updates":
            return run_apply_standalone_bom_updates_cmd(root, args)
        if args.command == "apply-standalone-bom-engine-updates":
            return run_apply_standalone_bom_engine_updates_cmd(root, args)
        if args.command == "review-material-publication-date":
            return run_review_material_publication_date_cmd(root, args)
        if args.command == "review-material-directory-location":
            return run_review_material_directory_location_cmd(root, args)
        if args.command == "scan-active-ima-materials":
            return run_scan_active_ima_materials_cmd(root, args)
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


def run_validate_report_contract_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_research_artifacts import FileSystemReportDocumentRepository
    from value_invest_research.application.use_cases.validate_report_contract import ValidateReportContract

    path = _resolve_cli_path(root, args.path)
    result = ValidateReportContract(FileSystemReportDocumentRepository(path)).execute(
        mode=args.mode,
        require_l3=args.require_l3,
    )
    status = "OK" if result.ok else "FAILED"
    print(
        f"Report contract validation {status}: "
        f"path={path}, "
        f"mode={result.mode}, "
        f"level1_cards={result.level1_cards}, "
        f"level2_cards={result.level2_cards}, "
        f"level3_cards={result.level3_cards}, "
        f"issues={len(result.issues)}"
    )
    for issue in result.issues[:10]:
        print(f"{issue.get('severity', 'error')}:{issue.get('code', '')}: {issue.get('message', '')}")
    return 0 if result.ok else 1


def run_audit_time_slice_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_research_artifacts import FileSystemSourceListRepository
    from value_invest_research.application.use_cases.audit_time_slice import AuditTimeSlice

    path = _resolve_cli_path(root, args.path)
    result = AuditTimeSlice(FileSystemSourceListRepository(path)).execute(as_of_date=args.as_of_date)
    status = "OK" if result.ok else "FAILED"
    print(
        f"Time-slice audit {status}: "
        f"path={path}, "
        f"as_of_date={result.as_of_date}, "
        f"sources={result.sources}, "
        f"post_cutoff_non_label_count={result.post_cutoff_non_label_count}, "
        f"label_only_count={result.label_only_count}, "
        f"quarantined_count={result.quarantined_count}, "
        f"issues={len(result.issues)}"
    )
    for issue in result.issues[:10]:
        print(f"{issue.get('severity', 'error')}:{issue.get('code', '')}: {issue.get('message', '')}")
    return 0 if result.ok else 1


def run_validate_research_artifacts_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_bom_project_layout import (
        FileSystemBomProjectLayoutRepository,
    )
    from value_invest_research.adapters.outbound.filesystem_research_artifacts import (
        FileSystemResearchArtifactRepository,
    )
    from value_invest_research.application.use_cases.validate_bom_project_layout import ValidateBomProjectLayout
    from value_invest_research.application.use_cases.validate_material_intake import ValidateMaterialIntake
    from value_invest_research.application.use_cases.validate_research_project import ValidateResearchProject
    from value_invest_research.adapters.outbound.filesystem_material_intake import (
        FileSystemMaterialIntakeValidationRepository,
    )

    project_dir = _resolve_cli_path(root, args.project_dir)
    result = ValidateResearchProject(FileSystemResearchArtifactRepository(project_dir)).execute(require_l3=args.require_l3)
    layout_result = ValidateBomProjectLayout(FileSystemBomProjectLayoutRepository(project_dir)).execute()
    intake_result = (
        ValidateMaterialIntake(
            FileSystemMaterialIntakeValidationRepository(project_dir)
        ).execute()
        if (
            (project_dir / "boms" / "manifest.json").is_file()
            or (project_dir / "material_intake").exists()
        )
        else {
            "ok": True,
            "issues": [],
            "summary": {
                "documents": 0,
                "parse_tasks": 0,
                "bom_inboxes": 0,
                "quarantined_documents": 0,
            },
        }
    )
    ok = result.ok and layout_result["ok"] and intake_result["ok"]
    status = "OK" if ok else "FAILED"
    print(
        f"Research artifact validation {status}: "
        f"project_dir={project_dir}, "
        f"qa_nodes={result.qa_nodes}, "
        f"source_extractions={result.source_extractions}, "
        f"leaf_source_reviews={result.leaf_source_reviews}, "
        f"targets={result.targets}, "
        f"bom_children={layout_result.get('summary', {}).get('child_projects', 0)}, "
        f"intake_documents={intake_result.get('summary', {}).get('documents', 0)}, "
        f"pending_parse_tasks={intake_result.get('summary', {}).get('parse_tasks', 0)}, "
        f"issues={len(result.issues) + len(layout_result.get('issues', [])) + len(intake_result.get('issues', []))}"
    )
    for issue in [
        *result.issues,
        *layout_result.get("issues", []),
        *intake_result.get("issues", []),
    ][:10]:
        print(f"{issue.get('severity', 'error')}:{issue.get('code', '')}: {issue.get('message', '')}")
    return 0 if ok else 1


def run_validate_material_intake_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_material_intake import (
        FileSystemMaterialIntakeValidationRepository,
    )
    from value_invest_research.application.use_cases.validate_material_intake import (
        ValidateMaterialIntake,
    )

    project_dir = _resolve_cli_path(root, args.project_dir)
    result = ValidateMaterialIntake(
        FileSystemMaterialIntakeValidationRepository(project_dir)
    ).execute()
    status = "OK" if result["ok"] else "FAILED"
    summary = result.get("summary") or {}
    print(
        f"Material intake validation {status}: "
        f"project_dir={project_dir}, "
        f"documents={summary.get('documents', 0)}, "
        f"parse_tasks={summary.get('parse_tasks', 0)}, "
        f"bom_inboxes={summary.get('bom_inboxes', 0)}, "
        f"quarantined={summary.get('quarantined_documents', 0)}, "
        f"issues={len(result.get('issues', []))}"
    )
    for issue in result.get("issues", [])[:10]:
        print(
            f"{issue.get('severity', 'error')}:{issue.get('code', '')}: "
            f"{issue.get('message', '')}"
        )
    return 0 if result["ok"] else 1


def run_validate_project_schema_cmd(root: Path, args: argparse.Namespace) -> int:
    import json
    from value_invest_research.framework_contracts import validate_project_schema
    project_file = root / args.project_dir / "project.json"
    if not project_file.exists():
        print(json.dumps({"ok": False, "issues": [{"severity": "error", "code": "missing_project_json", "message": str(project_file) + " not found"}], "summary": {}}, ensure_ascii=False))
        return 1
    with open(project_file) as fh:
        project = json.load(fh)
    result = validate_project_schema(project)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


def run_validate_industry_overview_cmd(root: Path, args: argparse.Namespace) -> int:
    from value_invest_research.framework_contracts import validate_industry_overview
    project_dir = root / args.project_dir
    result = validate_industry_overview(str(project_dir))
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


def run_render_research_report_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.canonical_html_report_renderer import CanonicalHtmlReportRenderer
    from value_invest_research.adapters.outbound.canonical_markdown_report_renderer import CanonicalMarkdownReportRenderer
    from value_invest_research.adapters.outbound.filesystem_research_project import FileSystemResearchProjectRepository
    from value_invest_research.application.use_cases.render_research_project_report import RenderResearchProjectReport

    project_dir = _resolve_cli_path(root, args.project_dir)
    renderer = (
        CanonicalHtmlReportRenderer()
        if str(args.filename).lower().endswith(".html")
        else CanonicalMarkdownReportRenderer()
    )
    result = RenderResearchProjectReport(
        FileSystemResearchProjectRepository(project_dir),
        renderer,
    ).execute(filename=args.filename)
    print(
        f"Research report rendered: "
        f"project_id={result['project_id']}, "
        f"qa_roots={result['qa_roots']}, "
        f"targets={result['targets']}, "
        f"sources={result['sources']}, "
        f"report={result['report_path']}"
    )
    return 0


def run_search_bom_materials_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_material_intake import (
        FileSystemMaterialIntakeRepository,
    )
    from value_invest_research.adapters.outbound.research_search_providers import (
        provider_for_name,
    )
    from value_invest_research.application.use_cases.ingest_materials import (
        ingest_question_search_result,
    )

    project_dir = _resolve_cli_path(root, args.project_dir)
    context = _load_material_project_context(project_dir)
    if args.bom_node_id not in context["known_bom_node_ids"]:
        raise ValueError(f"Unknown BOM node: {args.bom_node_id}")
    question_ids = context["question_ids_by_node"].get(args.bom_node_id) or {}
    question_id = question_ids.get(args.question_number) or (
        f"{args.bom_node_id}_q{args.question_number}"
    )
    provider = provider_for_name(args.provider)
    search_result = provider.search(
        {
            "task_id": f"{question_id}_material_search",
            "node_id": question_id,
            "question": args.query,
            "parent_question": _six_question_label(args.question_number),
            "required_evidence": [
                "actual facts",
                "forward expectations",
                "contradicting evidence",
            ],
            "information_categories": [
                "evidence",
                "research_report",
                "message",
                "opinion",
            ],
            "source_search_plan": [
                {
                    "source_bucket": "evidence",
                    "source_type": "primary and authoritative sources",
                    "expected_fields": "facts, dates, metrics, and source locators",
                },
                {
                    "source_bucket": "research_report",
                    "source_type": "sell-side and authoritative third party",
                    "expected_fields": "forecast, assumptions, and disagreement",
                },
            ],
            "max_sources": args.max_sources,
        }
    )
    result = ingest_question_search_result(
        search_result=search_result,
        repository=FileSystemMaterialIntakeRepository(project_dir),
        provider=args.provider,
        bom_node_id=args.bom_node_id,
        question_number=args.question_number,
        known_bom_node_ids=context["known_bom_node_ids"],
        mode=context["mode"],
        as_of_date=context["as_of_date"],
        discovered_at=args.discovered_at,
        question_ids_by_node=context["question_ids_by_node"],
    )
    event = result["scan_event"]
    print(
        "BOM material search completed: "
        f"node={args.bom_node_id}, "
        f"question={args.question_number}, "
        f"provider={args.provider}, "
        f"new_documents={event['discovered_count']}, "
        f"quarantined={event['quarantined_count']}, "
        f"parse_tasks={event['parse_task_count']}"
    )
    return 0


def run_scan_ima_materials_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_material_intake import (
        FileSystemMaterialIntakeRepository,
    )
    from value_invest_research.adapters.outbound.ima_knowledge_base_feed import (
        ImaKnowledgeBaseFeed,
    )
    from value_invest_research.adapters.outbound.pdf_publication_date_extractor import (
        PdfPublicationDateExtractor,
    )
    from value_invest_research.application.use_cases.ingest_materials import (
        scan_knowledge_base_directory_materials,
    )

    project_dir = _resolve_cli_path(root, args.project_dir)
    context = _load_material_project_context(project_dir)
    config_path = _resolve_cli_path(root, args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    ima_config = config.get("ima") or {}
    node_ids = list(context["known_bom_node_ids"])
    if args.bom_node_id:
        selected = set(args.bom_node_id)
        unknown = sorted(selected - set(node_ids))
        if unknown:
            raise ValueError(f"Unknown BOM nodes: {unknown}")
        node_ids = [node_id for node_id in node_ids if node_id in selected]
    feed = ImaKnowledgeBaseFeed()
    publication_date_extractor = PdfPublicationDateExtractor()
    knowledge_base_id = (
        args.knowledge_base_id
        or os.environ.get("IMA_KNOWLEDGE_BASE_ID", "")
    ).strip()
    if not knowledge_base_id:
        knowledge_base_name = str(
            args.knowledge_base_name
            or ima_config.get("knowledge_base_name")
            or ""
        ).strip()
        if not knowledge_base_name:
            raise ValueError(
                "IMA knowledge base requires --knowledge-base-id, "
                "IMA_KNOWLEDGE_BASE_ID, or --knowledge-base-name"
            )
        knowledge_base_id = feed.resolve_knowledge_base_id(
            knowledge_base_name
        )
    end_date = args.end_date or args.discovered_at or date.today().isoformat()
    start_date = args.start_date or end_date
    results = [
        scan_knowledge_base_directory_materials(
            feed=feed,
            repository=FileSystemMaterialIntakeRepository(project_dir),
            knowledge_base_id=knowledge_base_id,
            bom_node_id=node_id,
            relevance_profile=context["relevance_profiles_by_node"].get(
                node_id,
                {},
            ),
            known_bom_node_ids=context["known_bom_node_ids"],
            mode=context["mode"],
            as_of_date=context["as_of_date"],
            start_date=start_date,
            end_date=end_date,
            discovered_at=args.discovered_at,
            root_folder_pattern=(
                args.root_folder_pattern
                or str(
                    ima_config.get("root_folder_pattern")
                    or r"^\d{4}年国际顶级投行研报$"
                )
            ),
            question_ids_by_node=context["question_ids_by_node"],
            question_labels_by_node=context["question_labels_by_node"],
            fetch_originals=not args.skip_originals,
            publication_date_extractor=publication_date_extractor,
        )
        for node_id in node_ids
    ]
    content_results = [
        row
        for result in results
        for row in result.get("content_results") or []
    ]
    print(
        "IMA dated-directory scan completed: "
        f"bom_nodes={len(results)}, "
        f"candidates={sum(result['directory_scan']['candidate_count'] for result in results)}, "
        f"relevant={sum(result['directory_scan']['relevant_count'] for result in results)}, "
        f"new_documents={sum(result['new_documents'] for result in results)}, "
        f"quarantined={sum(result['quarantined_documents'] for result in results)}, "
        f"parse_tasks={sum(result['parse_tasks'] for result in results)}, "
        f"originals={sum(row.get('status') == 'available' for row in content_results)}, "
        f"original_gaps={sum(row.get('status') != 'available' for row in content_results)}, "
        f"pdf_verified_dates={sum(row.get('publication_date_status') == 'verified' for row in content_results)}, "
        f"title_inferred_dates={sum(row.get('publication_date_status') == 'inferred_from_title' for row in content_results)}, "
        f"publication_date_gaps={sum(row.get('status') == 'available' and row.get('publication_date_status') == 'needs_pdf_verification' for row in content_results)}"
    )
    return 0


def run_archive_ima_day_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_ima_archive import (
        FileSystemImaArchiveRepository,
    )
    from value_invest_research.adapters.outbound.ima_knowledge_base_feed import (
        ImaKnowledgeBaseFeed,
    )
    from value_invest_research.application.use_cases.archive_ima_daily import (
        archive_ima_day,
    )

    config_path = _resolve_cli_path(root, args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    feed_config = config.get("ima") or config
    if str(feed_config.get("archive_method") or "") == "ui_click":
        raise ValueError(
            "Central IMA archiving is configured for visible UI clicks. "
            "Use ima-single-day-bom-scan and archive-ima-ui-day; "
            "OpenAPI downloading is disabled."
        )
    feed = ImaKnowledgeBaseFeed()
    knowledge_base_id = (
        args.knowledge_base_id
        or os.environ.get("IMA_KNOWLEDGE_BASE_ID", "")
    ).strip()
    if not knowledge_base_id:
        knowledge_base_name = str(
            args.knowledge_base_name
            or feed_config.get("knowledge_base_name")
            or ""
        ).strip()
        if not knowledge_base_name:
            raise ValueError(
                "IMA archive requires --knowledge-base-id, "
                "IMA_KNOWLEDGE_BASE_ID, or --knowledge-base-name"
            )
        knowledge_base_id = feed.resolve_knowledge_base_id(knowledge_base_name)
    archive_root = _resolve_cli_path(
        root,
        str(
            args.archive_root
            or feed_config.get("archive_root")
            or "source/ima"
        ),
    )
    result = archive_ima_day(
        feed=feed,
        repository=FileSystemImaArchiveRepository(
            workspace_root=root,
            archive_root=archive_root,
        ),
        knowledge_base_id=knowledge_base_id,
        archive_date=args.archive_date,
        scanned_at=args.scanned_at,
        root_folder_pattern=str(
            args.root_folder_pattern
            or feed_config.get("root_folder_pattern")
            or r"^\d{4}年国际顶级投行研报$"
        ),
    )
    event = result["scan_event"]
    print(json.dumps(event, ensure_ascii=False))
    return 0 if event["status"] == "complete" else 2


def run_archive_ima_ui_day_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_ima_archive import (
        FileSystemImaArchiveRepository,
    )
    from value_invest_research.application.use_cases.archive_ima_ui import (
        archive_ima_ui_downloads,
        load_ui_candidate_inventory,
    )

    config_path = _resolve_cli_path(root, args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    feed_config = config.get("ima") or config
    inventory_path = _resolve_cli_path(root, args.candidate_list)
    candidates, directory_path = load_ui_candidate_inventory(
        inventory_path,
        archive_date=args.archive_date,
    )
    download_dir = Path(args.download_dir).expanduser()
    download_marker = (
        Path(args.download_marker).expanduser()
        if args.download_marker
        else None
    )
    result = archive_ima_ui_downloads(
        repository=FileSystemImaArchiveRepository(
            workspace_root=root,
            archive_root=_resolve_cli_path(
                root,
                str(
                    args.archive_root
                    or feed_config.get("archive_root")
                    or "source/ima"
                ),
            ),
        ),
        archive_date=args.archive_date,
        candidates=candidates,
        download_dir=download_dir,
        scanned_at=args.scanned_at,
        download_marker=download_marker,
        directory_path=directory_path,
    )
    event = result["scan_event"]
    print(json.dumps(event, ensure_ascii=False))
    return 0 if event["status"] == "complete" else 2


def run_archive_ima_daily_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_ima_archive import (
        FileSystemImaArchiveRepository,
    )
    from value_invest_research.adapters.outbound.ima_knowledge_base_feed import (
        ImaKnowledgeBaseFeed,
    )
    from value_invest_research.application.use_cases.archive_ima_daily import (
        archive_ima_day,
    )

    config_path = _resolve_cli_path(root, args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    feed_config = config.get("ima") or config
    if str(feed_config.get("archive_method") or "") == "ui_click":
        raise ValueError(
            "Central IMA archiving is configured for visible UI clicks. "
            "Use ima-single-day-bom-scan and archive-ima-ui-day; "
            "OpenAPI downloading is disabled."
        )
    schedule = feed_config.get("schedule") or {}
    lookback_days = int(
        args.lookback_days
        or schedule.get("retry_lookback_days")
        or 3
    )
    if lookback_days < 1:
        raise ValueError("lookback_days must be positive")
    end_date = date.fromisoformat(
        args.end_date
        or (date.today() - timedelta(days=1)).isoformat()
    )
    feed = ImaKnowledgeBaseFeed()
    knowledge_base_id = (
        args.knowledge_base_id
        or os.environ.get("IMA_KNOWLEDGE_BASE_ID", "")
    ).strip()
    if not knowledge_base_id:
        knowledge_base_name = str(
            args.knowledge_base_name
            or feed_config.get("knowledge_base_name")
            or ""
        ).strip()
        if not knowledge_base_name:
            raise ValueError(
                "IMA archive requires --knowledge-base-id, "
                "IMA_KNOWLEDGE_BASE_ID, or --knowledge-base-name"
            )
        knowledge_base_id = feed.resolve_knowledge_base_id(knowledge_base_name)
    repository = FileSystemImaArchiveRepository(
        workspace_root=root,
        archive_root=_resolve_cli_path(
            root,
            str(
                args.archive_root
                or feed_config.get("archive_root")
                or "source/ima"
            ),
        ),
    )
    results = []
    for days_before in range(lookback_days - 1, -1, -1):
        archive_date = (end_date - timedelta(days=days_before)).isoformat()
        results.append(
            archive_ima_day(
                feed=feed,
                repository=repository,
                knowledge_base_id=knowledge_base_id,
                archive_date=archive_date,
                scanned_at=args.scanned_at,
                root_folder_pattern=str(
                    args.root_folder_pattern
                    or feed_config.get("root_folder_pattern")
                    or r"^\d{4}年国际顶级投行研报$"
                ),
            )["scan_event"]
        )
    summary = {
        "status": (
            "complete"
            if all(row["status"] == "complete" for row in results)
            else "partial"
        ),
        "start_date": results[0]["archive_date"],
        "end_date": results[-1]["archive_date"],
        "days": results,
        "candidate_count": sum(row["candidate_count"] for row in results),
        "available_count": sum(row["available_count"] for row in results),
        "downloaded_count": sum(row["downloaded_count"] for row in results),
        "reused_count": sum(row["reused_count"] for row in results),
        "unavailable_count": sum(row["unavailable_count"] for row in results),
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["status"] == "complete" else 2


def run_validate_ima_archive_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_ima_archive import (
        FileSystemImaArchiveRepository,
    )
    from value_invest_research.application.use_cases.validate_ima_archive import (
        validate_ima_archive,
    )

    config_path = _resolve_cli_path(root, args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    feed_config = config.get("ima") or config
    archive_root = _resolve_cli_path(
        root,
        str(
            args.archive_root
            or feed_config.get("archive_root")
            or "source/ima"
        ),
    )
    result = validate_ima_archive(
        repository=FileSystemImaArchiveRepository(
            workspace_root=root,
            archive_root=archive_root,
        )
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["ok"] else 1


def run_route_ima_archive_to_bom_cmd(root: Path, args) -> int:
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

    project_dir = _resolve_cli_path(root, args.project_dir)
    context = _load_material_project_context(project_dir)
    if len(context["known_bom_node_ids"]) != 1:
        raise ValueError(
            "Central IMA archive routing currently requires exactly one BOM project"
        )
    node_id = context["known_bom_node_ids"][0]
    repository = FileSystemMaterialIntakeRepository(project_dir)
    reset_result = repository.reset_research_state() if args.reset else {}
    result = scan_knowledge_base_directory_materials(
        feed=ImaArchiveMaterialFeed(
            workspace_root=root,
            archive_root=_resolve_cli_path(root, args.archive_root),
        ),
        repository=repository,
        knowledge_base_id="central-ima-archive",
        bom_node_id=node_id,
        relevance_profile=context["relevance_profiles_by_node"].get(node_id, {}),
        known_bom_node_ids=context["known_bom_node_ids"],
        mode=context["mode"],
        as_of_date=context["as_of_date"],
        start_date=args.archive_date,
        end_date=args.archive_date,
        discovered_at=args.discovered_at,
        question_ids_by_node=context["question_ids_by_node"],
        question_labels_by_node=context["question_labels_by_node"],
        fetch_originals=True,
        publication_date_extractor=PdfPublicationDateExtractor(),
    )
    content_results = result.get("content_results") or []
    summary = {
        "project_dir": str(project_dir),
        "bom_node_id": node_id,
        "archive_date": args.archive_date,
        "reset": reset_result,
        "candidate_count": result["directory_scan"]["candidate_count"],
        "relevant_count": result["directory_scan"]["relevant_count"],
        "needs_review_count": result["directory_scan"]["needs_review_count"],
        "not_relevant_count": result["directory_scan"]["not_relevant_count"],
        "new_documents": result["new_documents"],
        "parse_tasks": result["parse_tasks"],
        "copied_originals": sum(
            row.get("status") == "available" for row in content_results
        ),
        "copy_failures": sum(
            row.get("status") != "available" for row in content_results
        ),
        "verified_publication_dates": sum(
            row.get("publication_date_status") == "verified"
            for row in content_results
        ),
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["copy_failures"] == 0 else 2


def run_scan_active_ima_materials_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_material_intake import (
        FileSystemMaterialIntakeRepository,
    )
    from value_invest_research.adapters.outbound.ima_knowledge_base_feed import (
        ImaKnowledgeBaseFeed,
    )
    from value_invest_research.adapters.outbound.pdf_publication_date_extractor import (
        PdfPublicationDateExtractor,
    )
    from value_invest_research.application.use_cases.ingest_materials import (
        scan_knowledge_base_directory_materials,
    )

    config_path = _resolve_cli_path(root, args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    feed_config = config.get("ima") or {}
    feed = ImaKnowledgeBaseFeed()
    publication_date_extractor = PdfPublicationDateExtractor()
    knowledge_base_id = str(
        os.environ.get("IMA_KNOWLEDGE_BASE_ID", "")
    ).strip()
    if not knowledge_base_id:
        knowledge_base_id = feed.resolve_knowledge_base_id(
            str(feed_config.get("knowledge_base_name") or "").strip()
        )
    results = []
    for entry in config.get("projects") or []:
        if not isinstance(entry, dict) or not entry.get("enabled", True):
            continue
        project_dir = _resolve_cli_path(root, str(entry.get("project_dir") or ""))
        context = _load_material_project_context(project_dir)
        end_date = (
            args.end_date
            or args.discovered_at
            or date.today().isoformat()
        )
        if args.start_date:
            start_date = args.start_date
        elif args.full_backfill:
            start_date = str(
                entry.get("backfill_start_date")
                or feed_config.get("backfill_start_date")
                or end_date
            )
        else:
            lookback_days = int(
                entry.get("lookback_days")
                or feed_config.get("lookback_days")
                or 3
            )
            start_date = (
                date.fromisoformat(end_date) - timedelta(days=lookback_days - 1)
            ).isoformat()
        for node_id in context["known_bom_node_ids"]:
            result = scan_knowledge_base_directory_materials(
                feed=feed,
                repository=FileSystemMaterialIntakeRepository(project_dir),
                knowledge_base_id=knowledge_base_id,
                bom_node_id=node_id,
                relevance_profile=context["relevance_profiles_by_node"].get(
                    node_id,
                    {},
                ),
                known_bom_node_ids=context["known_bom_node_ids"],
                mode=context["mode"],
                as_of_date=context["as_of_date"],
                start_date=start_date,
                end_date=end_date,
                discovered_at=args.discovered_at,
                root_folder_pattern=str(
                    entry.get("root_folder_pattern")
                    or feed_config.get("root_folder_pattern")
                    or r"^\d{4}年国际顶级投行研报$"
                ),
                question_ids_by_node=context["question_ids_by_node"],
                question_labels_by_node=context["question_labels_by_node"],
                fetch_originals=not args.skip_originals,
                publication_date_extractor=publication_date_extractor,
            )
            results.append(
                {
                    "project_dir": str(project_dir),
                    "bom_node_id": node_id,
                    "candidates": result["directory_scan"]["candidate_count"],
                    "relevant": result["directory_scan"]["relevant_count"],
                    "new_documents": result["new_documents"],
                    "parse_tasks": result["parse_tasks"],
                    "originals": sum(
                        row.get("status") == "available"
                        for row in result.get("content_results") or []
                    ),
                    "original_gaps": sum(
                        row.get("status") != "available"
                        for row in result.get("content_results") or []
                    ),
                    "pdf_verified_dates": sum(
                        row.get("publication_date_status") == "verified"
                        for row in result.get("content_results") or []
                    ),
                    "title_inferred_dates": sum(
                        row.get("publication_date_status")
                        == "inferred_from_title"
                        for row in result.get("content_results") or []
                    ),
                    "publication_date_gaps": sum(
                        row.get("status") == "available"
                        and row.get("publication_date_status")
                        == "needs_pdf_verification"
                        for row in result.get("content_results") or []
                    ),
                }
            )
    print(
        json.dumps(
            {
                "projects": results,
                "candidates": sum(row["candidates"] for row in results),
                "relevant": sum(row["relevant"] for row in results),
                "new_documents": sum(row["new_documents"] for row in results),
                "parse_tasks": sum(row["parse_tasks"] for row in results),
                "originals": sum(row["originals"] for row in results),
                "original_gaps": sum(row["original_gaps"] for row in results),
                "pdf_verified_dates": sum(
                    row["pdf_verified_dates"] for row in results
                ),
                "title_inferred_dates": sum(
                    row["title_inferred_dates"] for row in results
                ),
                "publication_date_gaps": sum(
                    row["publication_date_gaps"] for row in results
                ),
            },
            ensure_ascii=False,
        )
    )
    return 0


def run_refresh_standalone_bom_report_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_standalone_bom_timeline import (
        FileSystemStandaloneBomTimelineRepository,
    )
    from value_invest_research.adapters.outbound.standalone_bom_html_renderer import (
        StandaloneBomHtmlRenderer,
    )
    from value_invest_research.adapters.outbound.standalone_bom_markdown_renderer import (
        StandaloneBomMarkdownRenderer,
    )
    from value_invest_research.application.use_cases.refresh_standalone_bom_timeline import (
        refresh_standalone_bom_report,
    )

    project_dir = _resolve_cli_path(root, args.project_dir)
    result = refresh_standalone_bom_report(
        repository=FileSystemStandaloneBomTimelineRepository(project_dir),
        renderer=StandaloneBomMarkdownRenderer(project_dir=project_dir),
        html_renderer=StandaloneBomHtmlRenderer(project_dir=project_dir),
        as_of_date=args.as_of_date,
    )
    print(
        "Standalone BOM report refreshed: "
        f"path={result['report_path']}, "
        f"as_of_date={result['as_of_date']}, "
        f"claims={result['claims']}"
    )
    return 0


def run_validate_standalone_bom_engine_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_standalone_bom_timeline import (
        FileSystemStandaloneBomTimelineRepository,
    )
    from value_invest_research.domain.standalone_bom_investment_engine import (
        validate_standalone_bom_investment_bundle,
    )

    project_dir = _resolve_cli_path(root, args.project_dir)
    repository = FileSystemStandaloneBomTimelineRepository(project_dir)
    project = repository.load_project()
    as_of_date = (
        args.as_of_date
        or str(project.get("as_of_date") or "")
        or date.today().isoformat()
    )
    result = validate_standalone_bom_investment_bundle(
        project=project,
        profile=repository.load_profile(),
        claims=repository.load_claims(),
        claim_mappings=repository.load_claim_mappings(),
        logic_states=repository.load_logic_states(),
        entity_states=repository.load_entity_states(),
        thesis_revisions=repository.load_thesis_revisions(),
        investment_snapshots=repository.load_investment_snapshots(),
        as_of_date=as_of_date,
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["ok"] else 1


def run_apply_standalone_bom_updates_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_standalone_bom_timeline import (
        FileSystemStandaloneBomTimelineRepository,
    )
    from value_invest_research.adapters.outbound.standalone_bom_html_renderer import (
        StandaloneBomHtmlRenderer,
    )
    from value_invest_research.adapters.outbound.standalone_bom_markdown_renderer import (
        StandaloneBomMarkdownRenderer,
    )
    from value_invest_research.application.use_cases.refresh_standalone_bom_timeline import (
        apply_standalone_bom_updates,
    )

    project_dir = _resolve_cli_path(root, args.project_dir)
    claims = _read_jsonl(_resolve_cli_path(root, args.claims))
    conclusions = _read_jsonl(_resolve_cli_path(root, args.conclusions))
    result = apply_standalone_bom_updates(
        repository=FileSystemStandaloneBomTimelineRepository(project_dir),
        renderer=StandaloneBomMarkdownRenderer(project_dir=project_dir),
        html_renderer=StandaloneBomHtmlRenderer(project_dir=project_dir),
        raw_claims=claims,
        raw_conclusions=conclusions,
        as_of_date=args.as_of_date,
    )
    print(
        "Standalone BOM updates applied: "
        f"path={result['report_path']}, "
        f"claims={result['applied_claims']}, "
        f"conclusions={result['applied_conclusions']}, "
        f"finalized_parse_tasks={result['finalized_parse_tasks']}, "
        f"finalized_documents={result['finalized_documents']}"
    )
    return 0


def run_apply_standalone_bom_engine_updates_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_standalone_bom_timeline import (
        FileSystemStandaloneBomTimelineRepository,
    )
    from value_invest_research.adapters.outbound.standalone_bom_html_renderer import (
        StandaloneBomHtmlRenderer,
    )
    from value_invest_research.adapters.outbound.standalone_bom_markdown_renderer import (
        StandaloneBomMarkdownRenderer,
    )
    from value_invest_research.application.use_cases.refresh_standalone_bom_timeline import (
        apply_standalone_bom_engine_updates,
    )

    project_dir = _resolve_cli_path(root, args.project_dir)
    result = apply_standalone_bom_engine_updates(
        repository=FileSystemStandaloneBomTimelineRepository(project_dir),
        renderer=StandaloneBomMarkdownRenderer(project_dir=project_dir),
        html_renderer=StandaloneBomHtmlRenderer(project_dir=project_dir),
        raw_mappings=_read_jsonl(_resolve_cli_path(root, args.mappings)),
        raw_logic_states=_read_jsonl(
            _resolve_cli_path(root, args.logic_states)
        ),
        raw_entity_states=_read_jsonl(
            _resolve_cli_path(root, args.entity_states)
        ),
        raw_revisions=_read_jsonl(_resolve_cli_path(root, args.revisions)),
        raw_investment_snapshots=_read_jsonl(
            _resolve_cli_path(root, args.investment_snapshots)
        ),
        as_of_date=args.as_of_date,
    )
    print(
        "Standalone BOM investment engine updated: "
        f"path={result['report_path']}, "
        f"mappings={result['applied_mappings']}, "
        f"logic_states={result['applied_logic_states']}, "
        f"entity_states={result['applied_entity_states']}, "
        f"revisions={result['applied_revisions']}, "
        f"investment_snapshots={result['applied_investment_snapshots']}"
    )
    return 0


def run_review_material_publication_date_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_material_intake import (
        FileSystemMaterialIntakeRepository,
    )

    project_dir = _resolve_cli_path(root, args.project_dir)
    repository = FileSystemMaterialIntakeRepository(project_dir)
    repository.update_publication_date(
        source_id=args.source_id,
        published_at=args.published_at,
        publication_date_status=args.status,
        publication_date_source=args.source,
        publication_date_locator=args.locator,
    )
    print(
        "Material publication date reviewed: "
        f"source_id={args.source_id}, "
        f"published_at={args.published_at or '<pending>'}, "
        f"status={args.status}, source={args.source}"
    )
    return 0


def run_review_material_directory_location_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.filesystem_material_intake import (
        FileSystemMaterialIntakeRepository,
    )

    project_dir = _resolve_cli_path(root, args.project_dir)
    repository = FileSystemMaterialIntakeRepository(project_dir)
    local_path = repository.update_directory_location(
        source_id=args.source_id,
        directory_date=args.directory_date,
        directory_path=args.directory_path,
        directory_mapping_status=args.status,
    )
    print(
        "Material directory location reviewed: "
        f"source_id={args.source_id}, "
        f"directory_date={args.directory_date or '<pending>'}, "
        f"status={args.status}, local_path={local_path or '<not-downloaded>'}"
    )
    return 0


def _load_material_project_context(project_dir: Path) -> dict[str, Any]:
    from value_invest_research.domain.bom_node_playbooks import (
        get_bom_node_playbook,
    )

    project = json.loads(
        (project_dir / "project.json").read_text(encoding="utf-8")
    )
    standalone_node_id = (
        str(project.get("bom_node_id") or "").strip()
        if project.get("report_scope") == "standalone-bom"
        else ""
    )
    if standalone_node_id:
        known_nodes = [standalone_node_id]
    else:
        manifest = json.loads(
            (project_dir / "boms" / "manifest.json").read_text(encoding="utf-8")
        )
        known_nodes = [
            str(item.get("node_id") or "")
            for item in manifest.get("nodes") or []
            if str(item.get("node_id") or "").strip()
        ]
    question_ids_by_node: dict[str, dict[int, str]] = {}
    question_labels_by_node: dict[str, dict[int, str]] = {}
    for node_id in known_nodes:
        if standalone_node_id:
            labels = [
                str(label)
                for label in project.get("question_labels") or []
                if str(label).strip()
            ]
            question_ids_by_node[node_id] = {
                number: f"{node_id}_{_question_slug(label)}"
                for number, label in enumerate(labels, start=1)
            }
            question_labels_by_node[node_id] = {
                number: label
                for number, label in enumerate(labels, start=1)
            }
            continue
        try:
            playbook = get_bom_node_playbook(node_id)
        except KeyError:
            question_ids_by_node[node_id] = {
                number: f"{node_id}_q{number}" for number in range(1, 7)
            }
            continue
        question_ids_by_node[node_id] = {
            question.question_number: question.question_id
            for question in playbook.questions
        }
        question_labels_by_node[node_id] = {
            question.question_number: question.question
            for question in playbook.questions
        }
    return {
        "known_bom_node_ids": known_nodes,
        "question_ids_by_node": question_ids_by_node,
        "question_labels_by_node": question_labels_by_node,
        "relevance_profiles_by_node": (
            {
                standalone_node_id: (
                    project.get("material_relevance_profile") or {}
                )
            }
            if standalone_node_id
            else {
                str(node_id): profile
                for node_id, profile in (
                    project.get("material_relevance_profiles") or {}
                ).items()
                if isinstance(profile, dict)
            }
        ),
        "mode": str(
            project.get("mode")
            or project.get("run_mode")
            or "historical_backtest"
        ),
        "as_of_date": str(project.get("as_of_date") or ""),
    }


def _question_slug(value: str) -> str:
    aliases = {
        "需求侧": "demand",
        "供给侧": "supply",
        "技术侧": "technology",
        "估值侧": "valuation",
        "ESG": "esg",
    }
    return aliases.get(value, re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower())


def _six_question_label(question_number: int) -> str:
    labels = {
        1: "当前 BOM 的需求是否会被 S 曲线放大拉动？",
        2: "供给能否跟上？",
        3: "谁控制供给？",
        4: "是否已经财务兑现？",
        5: "市场是否已定价？",
        6: "反证是什么？",
    }
    return labels[question_number]


def _resolve_cli_path(root: Path, path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else root / path


def _read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line_number}: JSONL rows must be objects")
        rows.append(row)
    return rows


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
    from value_invest_research.adapters.outbound.leaf_research_workflow import LeafResearchWorkflowAdapter
    from value_invest_research.application.use_cases.leaf_research_workflow import BuildLeafResearchTasks

    result = BuildLeafResearchTasks(LeafResearchWorkflowAdapter()).execute(
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
    from value_invest_research.adapters.outbound.leaf_research_workflow import LeafResearchWorkflowAdapter
    from value_invest_research.application.use_cases.leaf_research_workflow import RunLeafResearch

    result = RunLeafResearch(LeafResearchWorkflowAdapter()).execute(
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
    from value_invest_research.adapters.outbound.leaf_research_workflow import LeafResearchWorkflowAdapter
    from value_invest_research.application.use_cases.leaf_research_workflow import ImportLeafResearchResults

    result = ImportLeafResearchResults(LeafResearchWorkflowAdapter()).execute(root, args.ticker, Path(args.path))
    print(
        f"Leaf research results imported for {result['ticker']}: "
        f"records={result['records']}, "
        f"sources={result['sources']}, "
        f"results_path={result['result_path']}, "
        f"sources_path={result['source_path']}"
    )
    return 0


def run_synthesize_leaf_answers_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.leaf_research_workflow import LeafResearchWorkflowAdapter
    from value_invest_research.application.use_cases.leaf_research_workflow import SynthesizeLeafAnswers

    result = SynthesizeLeafAnswers(LeafResearchWorkflowAdapter()).execute(root, args.ticker)
    print(
        f"Leaf answers synthesized for {result['ticker']}: "
        f"answers={result['answers']}, "
        f"answers_path={result['answer_path']}, "
        f"source_results={result['source_result_path']}, "
        f"report={result['report_path']}"
    )
    return 0


def run_rollup_research_answers_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.leaf_research_workflow import LeafResearchWorkflowAdapter
    from value_invest_research.application.use_cases.leaf_research_workflow import RollupResearchAnswers

    result = RollupResearchAnswers(LeafResearchWorkflowAdapter()).execute(root, args.ticker)
    print(
        f"Leaf research rollups written for {result['ticker']}: "
        f"rollups={result['rollups']}, "
        f"path={result['rollup_path']}, "
        f"report={result['report_path']}"
    )
    return 0


def run_write_professional_report_cmd(root: Path, args) -> int:
    from value_invest_research.adapters.outbound.professional_report_renderer import ProfessionalReportRendererAdapter
    from value_invest_research.application.use_cases.write_professional_report import WriteStockProfessionalReport

    client = _get_llm_client(args.api_key, args.base_url, args.model) if args.use_llm else None
    result = WriteStockProfessionalReport(ProfessionalReportRendererAdapter()).execute(root, args.ticker, client=client)
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
    from value_invest_research.adapters.outbound.professional_report_renderer import ProfessionalReportRendererAdapter
    from value_invest_research.application.use_cases.write_professional_report import WriteMetaQaProfessionalReport

    client = _get_llm_client(args.api_key, args.base_url, args.model) if args.use_llm else None
    result = WriteMetaQaProfessionalReport(ProfessionalReportRendererAdapter()).execute(root, args.project_id, client=client)
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
