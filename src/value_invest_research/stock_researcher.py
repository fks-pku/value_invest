from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from value_invest_research.llm import LlmClient
from value_invest_research.memo_updater import _build_system_prompt, _load_stock_context
from value_invest_research.runlog import RunLog, RunStatus


def _build_user_prompt(ticker: str, context: dict[str, Any]) -> str:
    sections = [
        f"# Foundation-First Stock Research: {ticker}",
        "",
        "## Current Investment Memo",
        context.get("memo", "(no existing memo)"),
        "",
    ]

    if context.get("key_financial_metrics"):
        sections.append("## Key Financial Metrics (from SEC XBRL)")
        for tag, info in context["key_financial_metrics"].items():
            sections.append(f"- {tag}: {info['value']} (period ending {info.get('end', 'N/A')}, form {info.get('form', 'N/A')})")
        sections.append("")

    if context.get("recent_prices"):
        sections.append("## Recent Price Data (last ~30 days)")
        sections.append(context["recent_prices"])
        sections.append("")

    if context.get("evidence"):
        sections.append("## Evidence Records")
        for ev in context["evidence"]:
            sections.append(f"- [{ev.get('id')}] {ev.get('summary')} (reliability: {ev.get('reliability')}, materiality: {ev.get('materiality')})")
        sections.append("")

    sections.extend([
        "## Instructions",
        "",
        "Produce a complete foundation-first stock research report. Do not update the memo directly.",
        "Analyze the company foundation before applying FengHe message-flow analysis.",
        "",
        "Required markdown sections:",
        "",
        "1. Executive conclusion",
        "2. Company foundation analysis with all eight sections:",
        "   source/origin; company history; current business; value chain position; competitive landscape; strategy; organization/culture/governance; risk sweep",
        "3. Foundation evidence gaps and human verification needs",
        "4. FengHe message-flow analysis after the foundation baseline:",
        "   3C; 3D and dominant_driver; 5M change map; 3T active time frame",
        "5. Disconfirming tests and thesis breakers",
        "6. Human review actions",
        "",
        "End the report with a fenced JSON block named `stock_research_signal` in this exact shape:",
        "",
        "```json",
        "{",
        '  "ticker": "...",',
        '  "view": "watch | attractive | expensive | avoid | needs_review",',
        '  "confidence": "low | medium | high",',
        '  "foundation_status": "complete | incomplete | needs_review",',
        '  "foundation_gaps": ["..."],',
        '  "cycle_state": "...",',
        '  "change_type": "structural | cyclical | mixed | unclear",',
        '  "certainty_level": "low | medium | high",',
        '  "dominant_driver": "D1 | D2 | D3 | unclear",',
        '  "m_scores": {',
        '    "M1_market_size": "positive | negative | mixed | unclear",',
        '    "M2_market_share": "positive | negative | mixed | unclear",',
        '    "M3_margin": "positive | negative | mixed | unclear",',
        '    "M4_model": "positive | negative | mixed | unclear",',
        '    "M5_management": "positive | negative | mixed | unclear"',
        "  },",
        '  "time_frame": "T1 | T2 | T3 | unclear",',
        '  "disconfirming_tests": ["..."],',
        '  "human_review_actions": ["..."]',
        "}",
        "```",
        "",
        "Rules:",
        "- Every material claim MUST cite an evidence ID or data source.",
        "- If the eight-section company foundation is incomplete, keep view as needs_review unless evidence strongly supports otherwise.",
        "- FengHe is the message-flow layer; do not use it as a substitute for company foundation analysis.",
        "- If evidence is insufficient, use needs_review and explain what is missing.",
        "- Do not issue final trading instructions.",
    ])

    return "\n".join(sections)


def _extract_signal_json(response_text: str) -> dict[str, Any]:
    matches = re.findall(r"```json\s*(\{.*?\})\s*```", response_text, flags=re.DOTALL)
    if not matches:
        return {}
    try:
        return json.loads(matches[-1])
    except json.JSONDecodeError:
        return {}


class StockResearcher:
    def __init__(self, client: LlmClient) -> None:
        self._client = client

    def run_stock_research(self, root: Path, ticker: str) -> dict[str, Any]:
        normalized = ticker.strip().upper()
        stock_dir = root / "stocks" / normalized
        if not stock_dir.exists():
            raise ValueError(f"stock folder not found: {stock_dir}")

        context = _load_stock_context(stock_dir)
        system_prompt = _build_system_prompt()
        user_prompt = _build_user_prompt(normalized, context)
        log = RunLog(stock_dir / "logs")

        try:
            response_text = self._client.chat(system_prompt, user_prompt)
        except Exception as exc:
            log.append("stock_research", RunStatus.FAILURE, tickers=[normalized], error=str(exc))
            raise

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        report_dir = stock_dir / "research_reports"
        report_dir.mkdir(parents=True, exist_ok=True)

        report_path = report_dir / f"{timestamp}_stock_research.md"
        report_path.write_text(response_text, encoding="utf-8")

        signal = _extract_signal_json(response_text)
        if not signal:
            signal = {
                "ticker": normalized,
                "view": "needs_review",
                "confidence": "low",
                "foundation_status": "needs_review",
                "error": "No valid stock_research_signal JSON block found in LLM response.",
            }
        signal.setdefault("ticker", normalized)

        signal_path = report_dir / f"{timestamp}_stock_signal.json"
        signal_path.write_text(json.dumps(signal, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        log.append("stock_research", RunStatus.SUCCESS, tickers=[normalized], records_fetched=1, records_new=1)

        return {
            "ticker": normalized,
            "timestamp": timestamp,
            "report_path": str(report_path),
            "signal_path": str(signal_path),
            "response_length": len(response_text),
        }
