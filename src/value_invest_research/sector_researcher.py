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
        _load_skill_file("frameworks/research_goal_qa.md"),
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
        f"Analyze this {sector_type} with the single Research Goal QA framework and produce ALL of the following:",
        "",
        "### 1. Current Research Goal",
        "- Research object, investment relevance, time frame, decision boundary, current constrained judgment, and biggest uncertainty.",
        "",
        "### 2. Research Execution Plan",
        "- For L0/L1/L2/L3, state what questions to ask, how to collect information, how to connect information into reasoning, and how to present it.",
        "",
        "### 3. QA Drilldown",
        "- Use at most three layers: Q1, Q1.1, Q1.1.1.",
        "- Each L3 must include fact, inference, judgment, gap, trigger, and source links.",
        "",
        "### 4. Four-Bucket Information Table",
        "- Classify every input as evidence, research_report, opinion, or message.",
        "- Mark support/refute/lead and attach links.",
        "",
        "### 5. Specific Target Observation List",
        "Map conclusions to specific securities or assets:",
        "```yaml",
        "targets:",
        "  - ticker: ...",
        "    name: ...",
        "    bottleneck_or_thesis_node: ...",
        "    reason: ...",
        "    strength: A | B | C | D",
        "    required_verification_data:",
        "      - ...",
        "    catalysts:",
        "      - ...",
        "    risks:",
        "      - ...",
        "    source_links:",
        "      - ...",
        "```",
        "",
        "### 6. Human Review Actions",
        "List specific actions for the human reviewer.",
        "",
        "IMPORTANT RULES:",
        "- Separate facts, inferences, judgments, and gaps.",
        "- Low-reliability messages are research leads only.",
        "- Do not issue buy/sell instructions.",
        "- Every target must include ticker/name, thesis node, reason, strength, verification data, catalysts, risks, and source links.",
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
            f"## 1. Current Research Goal\n\n"
            f"## 2. Research Execution Plan\n\n"
            f"## 3. QA Drilldown\n\n"
            f"## 4. Four-Bucket Information Table\n\n"
            f"## 5. Evidence-Linked Synthesis\n\n"
            f"## 6. Specific Target Observation List\n\n",
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
