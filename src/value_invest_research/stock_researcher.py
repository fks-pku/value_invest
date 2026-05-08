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
        f"# FengHe Stock Research: {ticker}",
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
        "Produce a complete FengHe Stock Research report. Do not update the memo directly.",
        "",
        "Required markdown sections:",
        "",
        "1. Executive conclusion",
        "2. 3C: Cycle, Change, Certainty",
        "3. 3D: D1 ROE/intrinsic value, D2 marginal change/catalyst, D3 sentiment/valuation, and dominant_driver",
        "4. 5M: M1 market size, M2 market share, M3 margin, M4 model, M5 management",
        "5. 3T: T1 0-3 months, T2 3-15 months, T3 15+ months, and active time frame",
        "6. Disconfirming tests and thesis breakers",
        "7. Human review actions",
        "",
        "End the report with a fenced JSON block named `fenghe_signal` in this exact shape:",
        "",
        "```json",
        "{",
        '  "ticker": "...",',
        '  "view": "watch | attractive | expensive | avoid | needs_review",',
        '  "confidence": "low | medium | high",',
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

        report_path = report_dir / f"{timestamp}_fenghe_research.md"
        report_path.write_text(response_text, encoding="utf-8")

        signal = _extract_signal_json(response_text)
        if not signal:
            signal = {
                "ticker": normalized,
                "view": "needs_review",
                "confidence": "low",
                "error": "No valid fenghe_signal JSON block found in LLM response.",
            }
        signal.setdefault("ticker", normalized)

        signal_path = report_dir / f"{timestamp}_fenghe_signal.json"
        signal_path.write_text(json.dumps(signal, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        log.append("stock_research", RunStatus.SUCCESS, tickers=[normalized], records_fetched=1, records_new=1)

        return {
            "ticker": normalized,
            "timestamp": timestamp,
            "report_path": str(report_path),
            "signal_path": str(signal_path),
            "response_length": len(response_text),
        }
