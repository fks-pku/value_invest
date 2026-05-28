from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:
    yaml = None  # type: ignore[assignment]

from value_invest_research.llm import LlmClient
from value_invest_research.runlog import RunLog, RunStatus
from value_invest_research.scaffold import init_event

SKILLS_DIR = Path(__file__).resolve().parent.parent.parent / "skills" / "value_invest_research"


def _load_skill_file(relative_path: str) -> str:
    path = SKILLS_DIR / relative_path
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _load_playbook(root: Path, playbook_name: str) -> dict[str, Any]:
    playbooks_path = root / "config" / "event_playbooks.yaml"
    if playbooks_path.exists():
        if yaml is None:
            raise RuntimeError("pyyaml package is required to load event playbooks; install value-invest-research[research]")
        all_playbooks = yaml.safe_load(playbooks_path.read_text(encoding="utf-8"))
        return all_playbooks.get(playbook_name, {})
    return {}


def _dump_context(data: dict[str, Any]) -> str:
    if yaml is not None:
        return yaml.dump(data, default_flow_style=False)
    return json.dumps(data, indent=2, sort_keys=True)


def _build_system_prompt() -> str:
    parts = [
        _load_skill_file("SKILL.md"),
        _load_skill_file("frameworks/research_goal_qa.md"),
    ]
    return "\n\n---\n\n".join(p for p in parts if p)


def _build_user_prompt(
    event_name: str,
    event_date: str,
    event_description: str,
    playbook: dict[str, Any] | None = None,
    existing_brief: str | None = None,
) -> str:
    sections = [
        f"# Event Research: {event_name}",
        f"Date: {event_date}",
        "",
        "## Event Description",
        event_description,
        "",
    ]

    if playbook:
        sections.extend([
            "## Applicable Playbook",
            "```yaml",
            _dump_context(playbook),
            "```",
            "",
        ])

    if existing_brief:
        sections.extend([
            "## Existing Event Brief",
            existing_brief,
            "",
        ])

    sections.extend([
        "## Instructions",
        "",
        "Analyze this event with the single Research Goal QA framework and produce ALL of the following:",
        "",
        "### 1. Current Research Goal",
        "Define the research object, investment relevance, time frame, decision boundary, current constrained judgment, and biggest uncertainty.",
        "",
        "### 2. Research Execution Plan",
        "For L0/L1/L2/L3, state what questions to ask, how to collect information, how to connect the information into reasoning, and how to present it.",
        "",
        "### 3. QA Drilldown",
        "Use at most three layers: Q1, Q1.1, Q1.1.1. Each L3 must include fact, inference, judgment, gap, trigger, and source links.",
        "",
        "### 4. Four-Bucket Information Table",
        "Classify every input as evidence, research_report, opinion, or message. Mark support/refute/lead and attach links.",
        "",
        "### 5. Specific Target Observation List",
        "If there are investment implications, map conclusions to specific securities or assets:",
        "```yaml",
        "- ticker: ...",
        "  name: ...",
        "  bottleneck_or_thesis_node: ...",
        "  reason: ...",
        "  strength: A | B | C | D",
        "  required_verification_data:",
        "    - ...",
        "  catalysts:",
        "    - ...",
        "  risks:",
        "    - ...",
        "  source_links:",
        "    - ...",
        "```",
        "",
        "### 6. Human Review Actions",
        "List specific actions the human reviewer should take.",
        "",
        "IMPORTANT RULES:",
        "- Separate facts, inferences, judgments, and gaps.",
        "- Low-reliability messages are research leads only.",
        "- Do not issue buy/sell instructions.",
        "- Every promoted candidate must include ticker/name, thesis node, reason, strength, verification data, catalysts, risks, and source links.",
        "- If the event impact is unclear, say so rather than speculating.",
    ])

    return "\n".join(sections)


class EventResearcher:
    def __init__(self, client: LlmClient) -> None:
        self._client = client

    def run_event_research(
        self,
        root: Path,
        event_date: str,
        event_name: str,
        event_description: str,
        playbook_name: str | None = None,
    ) -> dict[str, Any]:
        event_dir = init_event(root, event_date, event_name)

        existing_brief = None
        brief_path = event_dir / "event_brief.md"
        if brief_path.exists():
            content = brief_path.read_text(encoding="utf-8")
            if len(content.strip()) > 100:
                existing_brief = content

        playbook = None
        if playbook_name:
            playbook = _load_playbook(root, playbook_name)

        system_prompt = _build_system_prompt()
        user_prompt = _build_user_prompt(event_name, event_date, event_description, playbook, existing_brief)

        log = RunLog(event_dir / "logs")

        try:
            response_text = self._client.chat(system_prompt, user_prompt)
        except Exception as exc:
            log.append("event_research", RunStatus.FAILURE, error=str(exc))
            raise

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

        analysis_path = event_dir / f"{timestamp}_event_analysis.md"
        analysis_path.write_text(response_text, encoding="utf-8")

        updated_brief = brief_path.read_text(encoding="utf-8")
        if "## Confirmed Facts" not in updated_brief or updated_brief.count("\n") < 10:
            brief_sections = response_text.split("### 2. Unconfirmed Claims")[0] if "### 2. Unconfirmed Claims" in response_text else response_text[:2000]
            brief_path.write_text(
                f"# {event_name} Event Brief\n\n"
                f"- Date Opened: {event_date}\n"
                f"- Status: Active Research\n\n"
                f"{brief_sections}",
                encoding="utf-8",
            )

        log.append("event_research", RunStatus.SUCCESS, records_fetched=1, records_new=1)

        return {
            "event_name": event_name,
            "event_date": event_date,
            "event_dir": str(event_dir),
            "analysis_path": str(analysis_path),
            "response_length": len(response_text),
        }
