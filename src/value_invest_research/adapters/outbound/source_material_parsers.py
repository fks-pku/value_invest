from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable


class SummarySourceMaterialParser:
    """Deterministic parser adapter for already-summarized source materials."""

    def parse(self, job: dict[str, Any]) -> dict[str, Any]:
        source = job.get("source") if isinstance(job.get("source"), dict) else {}
        schema = job.get("extraction_schema") if isinstance(job.get("extraction_schema"), dict) else {}
        schema_fields = {key: "" for key in schema}
        schema_fields.update(schema)
        if "schema" in schema:
            schema_fields["schema"] = schema["schema"]
        summary = str(source.get("summary") or source.get("title") or "")
        for field in schema_fields:
            if field != "schema" and not schema_fields[field]:
                schema_fields[field] = summary
        return {
            "extraction_id": job.get("extraction_id", ""),
            "source_id": source.get("source_id") or source.get("id") or job.get("source_id", ""),
            "source_title": source.get("title", ""),
            "source_bucket": source.get("source_bucket") or source.get("information_category") or job.get("source_bucket", ""),
            "l3_question_id": job.get("l3_question_id", ""),
            "research_step_id": job.get("research_step_id") or f"step:{job.get('l3_question_id', '')}",
            "parser": job.get("parser", "summary-source-material-parser"),
            "parser_status": "complete",
            "key_facts": [summary] if summary else [],
            "inference": job.get("inference", ""),
            "support_refute_or_lead": job.get("support_refute_or_lead") or source.get("support_refute_or_lead") or "lead",
            "uncertainties": list(job.get("uncertainties") or []),
            "follow_up_data": list(job.get("follow_up_data") or []),
            "schema_fields": schema_fields,
            "created_at": job.get("created_at") or _now_iso(),
        }


class DelegatingSourceMaterialParser:
    """Adapter shell for DeepSeek/MCP or other external parsers.

    The callable is injected by the runtime boundary, keeping application use
    cases independent from a concrete MCP client implementation.
    """

    def __init__(self, delegate: Callable[[dict[str, Any]], dict[str, Any]], *, parser_name: str = "delegating-source-parser"):
        self.delegate = delegate
        self.parser_name = parser_name

    def parse(self, job: dict[str, Any]) -> dict[str, Any]:
        record = dict(self.delegate(job))
        record.setdefault("parser", self.parser_name)
        record.setdefault("parser_status", "complete")
        return record


class PassThroughSourceExtractionReviewer:
    """Deterministic reviewer for parser outputs already verified by the caller."""

    def review(self, extraction: dict[str, Any], job: dict[str, Any]) -> dict[str, Any]:
        return {
            "review_id": job.get("review_id", ""),
            "extraction_id": extraction.get("extraction_id", ""),
            "source_id": extraction.get("source_id", ""),
            "l3_question_id": extraction.get("l3_question_id", ""),
            "research_step_id": extraction.get("research_step_id", ""),
            "gpt_verification_status": job.get("gpt_verification_status", "verified_with_caveats"),
            "allowed_to_strengthen_conclusion": bool(job.get("allowed_to_strengthen_conclusion", True)),
            "final_bucket": job.get("final_bucket") or extraction.get("source_bucket") or "research_report",
            "final_support_refute_or_lead": job.get("final_support_refute_or_lead")
            or extraction.get("support_refute_or_lead")
            or "lead",
            "adopted_facts": list(extraction.get("key_facts") or []),
            "corrections": list(job.get("corrections") or []),
            "rejected_claims": list(job.get("rejected_claims") or []),
        }


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
