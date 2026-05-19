from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from value_invest_research.llm import LlmClient, LlmConfig
from value_invest_research.runlog import RunLog, RunStatus

SKILLS_DIR = Path(__file__).resolve().parent.parent.parent / "skills" / "value_invest_research"


def _load_skill_file(relative_path: str) -> str:
    path = SKILLS_DIR / relative_path
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _load_stock_context(stock_dir: Path) -> dict[str, Any]:
    context: dict[str, Any] = {}

    memo_path = stock_dir / "investment_memo.md"
    if memo_path.exists():
        context["memo"] = memo_path.read_text(encoding="utf-8")

    evidence_path = stock_dir / "evidence.jsonl"
    if evidence_path.exists():
        lines = evidence_path.read_text(encoding="utf-8").splitlines()
        context["evidence"] = [json.loads(line) for line in lines if line.strip()]

    fundamentals_path = stock_dir / "data" / "fundamentals.json"
    if fundamentals_path.exists():
        content = fundamentals_path.read_text(encoding="utf-8")
        if content.strip():
            context["fundamentals"] = json.loads(content)

    prices_path = stock_dir / "data" / "prices.csv"
    if prices_path.exists():
        lines = prices_path.read_text(encoding="utf-8").strip().splitlines()
        if len(lines) > 1:
            last_lines = lines[-min(30, len(lines)):]
            context["recent_prices"] = "\n".join(last_lines)

    sec_facts_path = stock_dir / "data" / "sec_facts.json"
    if sec_facts_path.exists():
        content = sec_facts_path.read_text(encoding="utf-8")
        if content.strip():
            facts = json.loads(content)
            us_gaap = facts.get("facts", {}).get("us-gaap", {})
            key_metrics = {}
            for tag in [
                "RevenueFromContractWithCustomerExcludingAssessedTax",
                "NetIncomeLoss",
                "OperatingIncomeLoss",
                "GrossProfit",
                "Assets",
                "Liabilities",
                "StockholdersEquity",
                "CashAndCashEquivalentsAtCarryingValue",
                "FreeCashFlow",
            ]:
                if tag in us_gaap:
                    units = us_gaap[tag].get("units", {})
                    for unit_key in ["USD", "USD/shares"]:
                        if unit_key in units:
                            entries = units[unit_key]
                            if entries:
                                last = entries[-1]
                                key_metrics[tag] = {
                                    "value": last.get("val"),
                                    "end": last.get("end"),
                                    "form": last.get("form"),
                                }
                            break
            context["key_financial_metrics"] = key_metrics

    return context


def _build_system_prompt() -> str:
    parts = [
        _load_skill_file("SKILL.md"),
        _load_skill_file("frameworks/company_foundation.md"),
        _load_skill_file("frameworks/fenghe_3c3d5m3t.md"),
        _load_skill_file("checklists/evidence_quality.md"),
        _load_skill_file("checklists/company_foundation_review.md"),
        _load_skill_file("checklists/fenghe_research_review.md"),
        _load_skill_file("checklists/disconfirming_evidence.md"),
    ]
    return "\n\n---\n\n".join(p for p in parts if p)


def _build_user_prompt(ticker: str, context: dict[str, Any]) -> str:
    sections = [
        f"# Update Stock Memo: {ticker}",
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
        "Based on the data above, produce:",
        "",
        "1. **Memo Update Summary**: A brief description of what changed and why.",
        "2. **Foundation Baseline Impact**: Which of the eight company-foundation sections changed, improved, or still lacks evidence.",
        "3. **FengHe Message-Flow Analysis**: Apply 3C, 3D, 5M, and 3T only after stating the foundation baseline.",
        "4. **Proposed Section Updates**: Provide markdown for each memo section that should change.",
        "5. **Stock Signal** (YAML format):",
        "```yaml",
        "ticker: ...",
        "date: ...",
        "view: watch | attractive | expensive | avoid | needs_review",
        "confidence: low | medium | high",
        "foundation_status: complete | incomplete | needs_review",
        "foundation_gaps:",
        "  - ...",
        "signal_strength: -3 to 3",
        "time_horizon: short_term | medium_term | long_term",
        "changed_since_last_run: true | false",
        "cycle_state: ...",
        "change_type: structural | cyclical | mixed | unclear",
        "certainty_level: low | medium | high",
        "dominant_driver: D1 | D2 | D3 | unclear",
        "m_scores:",
        "  M1_market_size: positive | negative | mixed | unclear",
        "  M2_market_share: positive | negative | mixed | unclear",
        "  M3_margin: positive | negative | mixed | unclear",
        "  M4_model: positive | negative | mixed | unclear",
        "  M5_management: positive | negative | mixed | unclear",
        "drivers:",
        "  - type: positive | negative | mixed | neutral",
        "    item: ...",
        "    evidence_id: ...",
        "disconfirming_tests:",
        "  - ...",
        "action_for_human:",
        "  - ...",
        "```",
        "",
        "IMPORTANT RULES:",
        "- Every material claim MUST cite an evidence ID or data source.",
        "- For stock-level work, use company foundation analysis first; use FengHe as the message-flow and change-analysis layer.",
        "- Do not use FengHe categories as a substitute for the eight-section company foundation baseline.",
        "- Low-reliability evidence creates open questions only, NOT thesis changes.",
        "- Search for disconfirming evidence BEFORE strengthening any thesis.",
        "- Separate facts from inferences from judgments clearly.",
        "- If data is insufficient to form a view, say so explicitly.",
    ])

    return "\n".join(sections)


class MemoUpdater:
    def __init__(self, client: LlmClient) -> None:
        self._client = client

    def update_stock_memo(self, root: Path, ticker: str) -> dict[str, Any]:
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
            log.append("memo_update", RunStatus.FAILURE, tickers=[normalized], error=str(exc))
            raise

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        proposal_dir = stock_dir / "proposals"
        proposal_dir.mkdir(parents=True, exist_ok=True)
        proposal_path = proposal_dir / f"{timestamp}_memo_update.md"
        proposal_path.write_text(response_text, encoding="utf-8")

        log.append("memo_update", RunStatus.SUCCESS, tickers=[normalized], records_fetched=1, records_new=1)

        return {
            "ticker": normalized,
            "timestamp": timestamp,
            "proposal_path": str(proposal_path),
            "response_length": len(response_text),
        }
