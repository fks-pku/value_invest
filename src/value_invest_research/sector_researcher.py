from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from value_invest_research.llm import LlmClient
from value_invest_research.runlog import RunLog, RunStatus

SKILLS_DIR = Path(__file__).resolve().parent.parent.parent / "skills" / "value_invest_research"


def _load_skill_file(relative_path: str) -> str:
    path = SKILLS_DIR / relative_path
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _build_system_prompt() -> str:
    parts = [
        _load_skill_file("SKILL.md"),
        _load_skill_file("frameworks/sector_research.md"),
        _load_skill_file("checklists/evidence_quality.md"),
    ]
    return "\n\n---\n\n".join(p for p in parts if p)


def _build_user_prompt(
    sector_name: str,
    sector_type: str,
    research_focus: str,
    existing_memo: str | None = None,
    tickers_to_include: list[str] | None = None,
) -> str:
    sections = [
        f"# {'Sector' if sector_type == 'sector' else 'Theme'} Research: {sector_name}",
        "",
        "## Research Focus",
        research_focus,
        "",
    ]

    if tickers_to_include:
        sections.extend([
            "## Companies to Analyze",
            ", ".join(tickers_to_include),
            "",
        ])

    if existing_memo:
        sections.extend([
            "## Existing Memo",
            existing_memo,
            "",
        ])

    sections.extend([
        "## Instructions",
        "",
        f"Analyze this {sector_type} and produce ALL of the following:",
        "",
        "### 1. Current Sector/Theme View",
        "- Attractiveness (high/medium/low)",
        "- Cycle position",
        "- Key thesis",
        "- Confidence level",
        "",
        "### 2. Industry Structure",
        "- Value chain (upstream → midstream → downstream)",
        "- Profit pools (where is value captured?)",
        "- Competitive dynamics",
        "- Barriers to entry",
        "",
        "### 3. Demand Drivers",
        "- End markets",
        "- Secular growth trends",
        "- Cyclical factors",
        "- Key metrics to watch",
        "",
        "### 4. Company Map",
        "Categorize companies into:",
        "- **Leaders**: Dominant market position, competitive advantage",
        "- **Challengers**: Growing share, credible threat",
        "- **Niche Compounders**: Small but high-quality operators",
        "- **Cyclical Candidates**: Attractive at the right cycle point",
        "- **Avoid/Watch**: Overvalued, poor quality, or high risk",
        "",
        "### 5. Cross-Company Comparison",
        "Compare key companies on:",
        "- Quality (margins, returns, cash conversion)",
        "- Growth (revenue, earnings trajectory)",
        "- Balance sheet (leverage, cash position)",
        "- Valuation (relative, not absolute)",
        "- Key risks",
        "",
        "### 6. Candidate Companies for Stock-Level Research",
        "```yaml",
        "candidates:",
        "  - ticker: ...",
        "    category: leader | challenger | niche_compounder | cyclical",
        "    reason: ...",
        "    key_research_questions:",
        "      - ...",
        "    priority: high | medium | low",
        "```",
        "",
        "### 7. Human Review Actions",
        "List specific actions for the human reviewer.",
        "",
        "IMPORTANT RULES:",
        "- Base analysis on verifiable industry structure, not predictions.",
        "- Separate structural trends from cyclical effects.",
        "- Every candidate recommendation must cite a specific reason.",
        "- Include disconfirming evidence for bullish conclusions.",
        "- If data is insufficient for a conclusion, explicitly state the gap.",
    ])

    return "\n".join(sections)


def _ensure_sector_dir(root: Path, sector_type: str, sector_slug: str) -> Path:
    from value_invest_research.scaffold import slugify

    slug = slugify(sector_slug)
    base_dir = root / "research" / ("sectors" if sector_type == "sector" else "themes") / slug
    for subdir in [base_dir / "data", base_dir / "raw", base_dir / "logs"]:
        subdir.mkdir(parents=True, exist_ok=True)

    memo_path = base_dir / "sector_memo.md" if sector_type == "sector" else base_dir / "theme_memo.md"
    if not memo_path.exists():
        memo_path.write_text(
            f"# {sector_slug} {'Sector' if sector_type == 'sector' else 'Theme'} Memo\n\n"
            f"## 1. Current {'Sector' if sector_type == 'sector' else 'Theme'} View\n\n"
            f"## 2. Industry Structure\n\n"
            f"## 3. Demand Drivers\n\n"
            f"## 4. Company Map\n\n"
            f"## 5. Cross-Company Comparison\n\n"
            f"## 6. Signals To Individual Stocks\n\n"
            f"## 7. Evidence Log\n",
            encoding="utf-8",
        )

    return base_dir


class SectorResearcher:
    def __init__(self, client: LlmClient) -> None:
        self._client = client

    def run_sector_research(
        self,
        root: Path,
        sector_name: str,
        sector_type: str,
        research_focus: str,
        tickers_to_include: list[str] | None = None,
    ) -> dict[str, Any]:
        if sector_type not in ("sector", "theme"):
            raise ValueError("sector_type must be 'sector' or 'theme'")

        sector_dir = _ensure_sector_dir(root, sector_type, sector_name)

        existing_memo = None
        memo_path = sector_dir / ("sector_memo.md" if sector_type == "sector" else "theme_memo.md")
        memo_content = memo_path.read_text(encoding="utf-8")
        if len(memo_content.strip()) > 200:
            existing_memo = memo_content

        system_prompt = _build_system_prompt()
        user_prompt = _build_user_prompt(sector_name, sector_type, research_focus, existing_memo, tickers_to_include)

        log = RunLog(sector_dir / "logs")

        try:
            response_text = self._client.chat(system_prompt, user_prompt)
        except Exception as exc:
            log.append("sector_research", RunStatus.FAILURE, error=str(exc))
            raise

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        analysis_path = sector_dir / f"{timestamp}_{sector_type}_analysis.md"
        analysis_path.write_text(response_text, encoding="utf-8")

        log.append("sector_research", RunStatus.SUCCESS, records_fetched=1, records_new=1)

        return {
            "sector_name": sector_name,
            "sector_type": sector_type,
            "sector_dir": str(sector_dir),
            "analysis_path": str(analysis_path),
            "response_length": len(response_text),
        }
