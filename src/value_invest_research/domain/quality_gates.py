from __future__ import annotations

from value_invest_research.domain.research_artifacts import (
    ReportContractValidationResult,
    ReportDocument,
    ResearchArtifacts,
    ResearchArtifactValidationResult,
    SourceList,
    TimeSliceAuditResult,
)
from value_invest_research.domain.bom_research_readiness import validate_bom_research_decision_gates
from value_invest_research.framework_contracts import (
    audit_time_slice_sources,
    validate_backtest_leakage_controls,
    validate_industry_space_source_search_pipeline,
    validate_report_contract_html,
    validate_report_contract_markdown,
    validate_leaf_source_review_schema,
    validate_qa_tree_schema,
    validate_source_extraction_schema,
    validate_target_observation_contract,
)


def validate_research_artifacts(
    artifacts: ResearchArtifacts,
    *,
    project_dir: str,
    require_l3: bool = False,
) -> ResearchArtifactValidationResult:
    """Validate research artifacts without knowing how they were loaded."""
    qa_result = (
        validate_qa_tree_schema(artifacts.qa_tree, require_l3=require_l3)
        if artifacts.qa_tree
        else {"ok": False, "issues": [], "summary": {}}
    )
    extraction_result = (
        validate_source_extraction_schema(artifacts.source_extractions, artifacts.qa_tree)
        if artifacts.qa_tree and artifacts.source_extractions
        else {"ok": False, "issues": [], "summary": {}}
    )
    review_result = (
        validate_leaf_source_review_schema(
            artifacts.leaf_source_reviews,
            artifacts.source_extractions,
            artifacts.qa_tree,
        )
        if artifacts.qa_tree and artifacts.source_extractions and artifacts.leaf_source_reviews
        else {"ok": False, "issues": [], "summary": {}}
    )
    target_result = (
        validate_target_observation_contract(artifacts.targets)
        if artifacts.targets
        else {"ok": False, "issues": [], "summary": {}}
    )
    leakage_result = validate_backtest_leakage_controls(
        artifacts.qa_tree,
        artifacts.source_extractions,
        artifacts.leaf_source_reviews,
        artifacts.targets,
        artifacts.sources,
    ) if artifacts.qa_tree else {"ok": False, "issues": [], "summary": {}}
    industry_space_source_search_result = (
        validate_industry_space_source_search_pipeline(artifacts.workbench)
        if artifacts.workbench
        else {"ok": True, "issues": [], "summary": {}}
    )
    bom_decision_gate_result = validate_bom_research_decision_gates(
        artifacts.workbench,
        artifacts.targets,
    )

    all_issues = (
        list(artifacts.load_issues)
        + list(qa_result.get("issues", []))
        + list(extraction_result.get("issues", []))
        + list(review_result.get("issues", []))
        + list(target_result.get("issues", []))
        + list(leakage_result.get("issues", []))
        + list(industry_space_source_search_result.get("issues", []))
        + list(bom_decision_gate_result.get("issues", []))
    )
    ok = not any(issue.get("severity") == "error" for issue in all_issues)
    return ResearchArtifactValidationResult(
        ok=ok,
        project_dir=project_dir,
        qa_nodes=int(qa_result.get("summary", {}).get("nodes", 0) or 0),
        source_extractions=int(extraction_result.get("summary", {}).get("source_extractions", 0) or 0),
        leaf_source_reviews=int(review_result.get("summary", {}).get("leaf_source_reviews", 0) or 0),
        targets=int(target_result.get("summary", {}).get("targets", 0) or 0),
        issues=all_issues,
    )


def validate_report_contract(
    document: ReportDocument,
    *,
    path: str,
    mode: str = "historical_backtest",
    require_l3: bool = False,
) -> ReportContractValidationResult:
    """Validate public report content without knowing its presentation adapter."""
    if document.markdown:
        result = validate_report_contract_markdown(
            document.markdown,
            mode=mode,
            require_l3=require_l3,
        )
    elif document.html:
        result = validate_report_contract_html(
            document.html,
            mode=mode,
            require_l3=require_l3,
        )
    else:
        result = {"ok": False, "issues": [], "summary": {"mode": mode}}
    all_issues = list(document.load_issues) + list(result.get("issues", []))
    ok = not any(issue.get("severity") == "error" for issue in all_issues)
    summary = result.get("summary", {})
    return ReportContractValidationResult(
        ok=ok,
        path=path,
        mode=str(summary.get("mode") or mode),
        level1_cards=int(summary.get("level1_cards", 0) or 0),
        level2_cards=int(summary.get("level2_cards", 0) or 0),
        level3_cards=int(summary.get("level3_cards", 0) or 0),
        issues=all_issues,
    )


def audit_source_time_slice(
    source_list: SourceList,
    *,
    path: str,
    as_of_date: str,
) -> TimeSliceAuditResult:
    """Audit source cutoff visibility without knowing how sources were loaded."""
    result = audit_time_slice_sources(source_list.sources, as_of_date=as_of_date)
    all_issues = list(source_list.load_issues) + list(result.get("issues", []))
    ok = not any(issue.get("severity") == "error" for issue in all_issues)
    summary = result.get("summary", {})
    return TimeSliceAuditResult(
        ok=ok,
        path=path,
        as_of_date=str(summary.get("as_of_date") or as_of_date),
        sources=int(summary.get("sources", 0) or 0),
        post_cutoff_non_label_count=int(summary.get("post_cutoff_non_label_count", 0) or 0),
        label_only_count=int(summary.get("label_only_count", 0) or 0),
        quarantined_count=int(summary.get("quarantined_count", 0) or 0),
        issues=all_issues,
    )
