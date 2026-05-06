# Research Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first usable foundation for the LLM investment research assistant: repository skeleton, research object templates, value-investing Skill files, evidence/signal schemas, and a CLI that initializes stock and event research folders.

**Architecture:** Use a file-system-first Python package with no runtime third-party dependencies. Markdown and JSON Lines files remain the source of truth; Python code provides validation and scaffolding so future ingestion and LLM workflows can rely on stable contracts.

**Tech Stack:** Python 3.11+, standard library, `unittest`, Markdown, JSON Lines, YAML configuration files treated as editable config documents in Phase 1.

---

## File Structure

- Create `pyproject.toml`: project metadata and test command conventions.
- Create `.gitignore`: Python and local run artifacts.
- Create `src/value_invest_research/__init__.py`: package exports.
- Create `src/value_invest_research/models.py`: evidence and stock-signal data contracts with validation.
- Create `src/value_invest_research/scaffold.py`: creates stock and event research folders from built-in templates.
- Create `src/value_invest_research/cli.py`: `init-stock`, `init-event`, and `validate-evidence` commands.
- Create `src/value_invest_research/__main__.py`: allows `python -m value_invest_research`.
- Create `tests/test_models.py`: schema validation tests.
- Create `tests/test_scaffold.py`: folder initialization tests.
- Create `tests/test_cli.py`: CLI behavior tests.
- Create `skills/value_invest_research/SKILL.md`: operating protocol for the investment research assistant.
- Create `skills/value_invest_research/frameworks/value_investing.md`: value-investing research framework.
- Create `skills/value_invest_research/frameworks/event_research.md`: rapid event research protocol.
- Create `skills/value_invest_research/frameworks/sector_research.md`: sector/theme research protocol.
- Create `skills/value_invest_research/checklists/evidence_quality.md`: evidence reliability and materiality rules.
- Create `skills/value_invest_research/checklists/disconfirming_evidence.md`: thesis-breaker checklist.
- Create `skills/value_invest_research/checklists/valuation_review.md`: valuation review checklist.
- Create `skills/value_invest_research/prompts/update_stock_memo.md`: stock memo update prompt contract.
- Create `skills/value_invest_research/prompts/run_event_research.md`: event research prompt contract.
- Create `skills/value_invest_research/prompts/run_sector_research.md`: sector/theme prompt contract.
- Create `config/watchlist.yaml`: editable first watchlist.
- Create `config/event_playbooks.yaml`: geopolitical conflict playbook.
- Create `config/source_priority.yaml`: source reliability defaults.
- Create `config/research_objects.yaml`: declared research object registry.

## Scope Boundary

This plan implements Phase 1 of the design spec. It deliberately excludes live SEC/news/price ingestion and LLM API calls. Those become testable Phase 2 and Phase 3 plans after the foundation exists.

---

### Task 1: Initialize Project Metadata

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`

- [ ] **Step 1: Initialize Git repository if needed**

Run:

```powershell
git rev-parse --is-inside-work-tree
```

Expected when this workspace is still uninitialized:

```text
fatal: not a git repository (or any of the parent directories): .git
```

Then run:

```powershell
git init
```

Expected:

```text
Initialized empty Git repository
```

- [ ] **Step 2: Create project metadata**

Create `pyproject.toml`:

```toml
[project]
name = "value-invest-research"
version = "0.1.0"
description = "File-system-first LLM investment research assistant foundation"
requires-python = ">=3.11"
dependencies = []

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]

[tool.coverage.run]
source = ["src"]
```

- [ ] **Step 3: Create ignore rules**

Create `.gitignore`:

```gitignore
__pycache__/
*.py[cod]
.pytest_cache/
.coverage
.venv/
venv/
build/
dist/
*.egg-info/
.env
.env.*
stocks/*/raw/
research/*/*/raw/
research/events/*/raw/
```

- [ ] **Step 4: Commit metadata**

Run:

```powershell
git add pyproject.toml .gitignore
git commit -m "chore: initialize research project metadata"
```

Expected:

```text
[main
```

---

### Task 2: Add Evidence And Signal Models

**Files:**
- Create: `src/value_invest_research/__init__.py`
- Create: `src/value_invest_research/models.py`
- Create: `tests/test_models.py`

- [ ] **Step 1: Write failing model tests**

Create `tests/test_models.py`:

```python
import unittest

from value_invest_research.models import (
    EvidenceRecord,
    SignalDriver,
    StockSignal,
    ValidationError,
)


class EvidenceRecordTests(unittest.TestCase):
    def test_valid_evidence_round_trips_to_dict(self):
        record = EvidenceRecord.from_dict(
            {
                "id": "ev_20260506_aapl_10q_001",
                "research_object": "stocks/AAPL",
                "source_type": "sec_filing",
                "source_name": "10-Q",
                "url": "https://www.sec.gov/example",
                "published_at": "2026-05-01T00:00:00Z",
                "fetched_at": "2026-05-06T08:00:00Z",
                "hash": "sha256:abc123",
                "tickers": ["AAPL"],
                "sectors": ["technology_hardware"],
                "themes": ["services_growth"],
                "summary": "Revenue and margin facts extracted from a filing.",
                "reliability": "primary",
                "materiality": "medium",
                "used_in": ["investment_memo.md"],
            }
        )

        self.assertEqual(record.to_dict()["id"], "ev_20260506_aapl_10q_001")
        self.assertEqual(record.to_dict()["tickers"], ["AAPL"])

    def test_rejects_low_reliability_thesis_change(self):
        with self.assertRaisesRegex(ValidationError, "low-reliability"):
            EvidenceRecord.from_dict(
                {
                    "id": "ev_20260506_aapl_rumor_001",
                    "research_object": "stocks/AAPL",
                    "source_type": "social_media",
                    "source_name": "Unattributed post",
                    "url": "https://example.com/rumor",
                    "published_at": None,
                    "fetched_at": "2026-05-06T08:00:00Z",
                    "hash": "sha256:def456",
                    "tickers": ["AAPL"],
                    "sectors": [],
                    "themes": [],
                    "summary": "Unverified claim.",
                    "reliability": "low",
                    "materiality": "thesis_change",
                    "used_in": [],
                }
            )

    def test_requires_material_claims_to_have_evidence(self):
        with self.assertRaisesRegex(ValidationError, "evidence_id"):
            StockSignal(
                ticker="AAPL",
                date="2026-05-06",
                view="watch",
                confidence="medium",
                signal_strength=2,
                time_horizon="long_term",
                changed_since_last_run=True,
                drivers=[SignalDriver(type="positive", item="FCF durability improved", evidence_id="")],
                action_for_human=["Review valuation assumptions"],
            ).validate()


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_models -v
```

Expected:

```text
ModuleNotFoundError: No module named 'value_invest_research'
```

- [ ] **Step 3: Implement models**

Create `src/value_invest_research/__init__.py`:

```python
"""Core package for the file-system-first investment research assistant."""

from value_invest_research.models import EvidenceRecord, SignalDriver, StockSignal, ValidationError

__all__ = ["EvidenceRecord", "SignalDriver", "StockSignal", "ValidationError"]
```

Create `src/value_invest_research/models.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


class ValidationError(ValueError):
    """Raised when a research record violates the evidence contract."""


RELIABILITY_LEVELS = {"primary", "high", "medium", "low"}
MATERIALITY_LEVELS = {"low", "medium", "high", "thesis_change"}
VIEWS = {"watch", "attractive", "expensive", "avoid", "needs_review"}
CONFIDENCE_LEVELS = {"low", "medium", "high"}


def _require_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{key} must be a non-empty string")
    return value.strip()


def _string_list(data: dict[str, Any], key: str) -> list[str]:
    value = data.get(key, [])
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValidationError(f"{key} must be a list of strings")
    return [item.strip() for item in value if item.strip()]


def _validate_datetime(value: str | None, key: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{key} must be an ISO timestamp or null")
    normalized = value.replace("Z", "+00:00")
    try:
        datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValidationError(f"{key} must be an ISO timestamp") from exc
    return value


@dataclass(frozen=True)
class EvidenceRecord:
    id: str
    research_object: str
    source_type: str
    source_name: str
    url: str
    published_at: str | None
    fetched_at: str
    hash: str
    tickers: list[str] = field(default_factory=list)
    sectors: list[str] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)
    summary: str = ""
    reliability: str = "medium"
    materiality: str = "low"
    used_in: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvidenceRecord":
        reliability = _require_string(data, "reliability")
        if reliability not in RELIABILITY_LEVELS:
            raise ValidationError(f"reliability must be one of {sorted(RELIABILITY_LEVELS)}")

        materiality = _require_string(data, "materiality")
        if materiality not in MATERIALITY_LEVELS:
            raise ValidationError(f"materiality must be one of {sorted(MATERIALITY_LEVELS)}")
        if reliability == "low" and materiality == "thesis_change":
            raise ValidationError("low-reliability evidence cannot trigger a thesis_change")

        return cls(
            id=_require_string(data, "id"),
            research_object=_require_string(data, "research_object"),
            source_type=_require_string(data, "source_type"),
            source_name=_require_string(data, "source_name"),
            url=_require_string(data, "url"),
            published_at=_validate_datetime(data.get("published_at"), "published_at"),
            fetched_at=_validate_datetime(_require_string(data, "fetched_at"), "fetched_at") or "",
            hash=_require_string(data, "hash"),
            tickers=_string_list(data, "tickers"),
            sectors=_string_list(data, "sectors"),
            themes=_string_list(data, "themes"),
            summary=_require_string(data, "summary"),
            reliability=reliability,
            materiality=materiality,
            used_in=_string_list(data, "used_in"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "research_object": self.research_object,
            "source_type": self.source_type,
            "source_name": self.source_name,
            "url": self.url,
            "published_at": self.published_at,
            "fetched_at": self.fetched_at,
            "hash": self.hash,
            "tickers": list(self.tickers),
            "sectors": list(self.sectors),
            "themes": list(self.themes),
            "summary": self.summary,
            "reliability": self.reliability,
            "materiality": self.materiality,
            "used_in": list(self.used_in),
        }


@dataclass(frozen=True)
class SignalDriver:
    type: str
    item: str
    evidence_id: str

    def validate(self) -> None:
        if self.type not in {"positive", "negative", "mixed", "neutral"}:
            raise ValidationError("driver type must be positive, negative, mixed, or neutral")
        if not self.item.strip():
            raise ValidationError("driver item must be non-empty")
        if not self.evidence_id.strip():
            raise ValidationError("signal drivers must include evidence_id")


@dataclass(frozen=True)
class StockSignal:
    ticker: str
    date: str
    view: str
    confidence: str
    signal_strength: int
    time_horizon: str
    changed_since_last_run: bool
    drivers: list[SignalDriver]
    action_for_human: list[str]

    def validate(self) -> None:
        if not self.ticker.strip():
            raise ValidationError("ticker must be non-empty")
        if self.view not in VIEWS:
            raise ValidationError(f"view must be one of {sorted(VIEWS)}")
        if self.confidence not in CONFIDENCE_LEVELS:
            raise ValidationError(f"confidence must be one of {sorted(CONFIDENCE_LEVELS)}")
        if not -3 <= self.signal_strength <= 3:
            raise ValidationError("signal_strength must be between -3 and 3")
        if not self.drivers:
            raise ValidationError("stock signal requires at least one driver")
        for driver in self.drivers:
            driver.validate()
        if not self.action_for_human:
            raise ValidationError("action_for_human must contain at least one review action")
```

- [ ] **Step 4: Run tests to verify they pass**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_models -v
```

Expected:

```text
OK
```

- [ ] **Step 5: Commit models**

Run:

```powershell
git add src tests/test_models.py
git commit -m "feat: add research evidence models"
```

Expected:

```text
[main
```

---

### Task 3: Add Research Folder Scaffolding

**Files:**
- Create: `src/value_invest_research/scaffold.py`
- Create: `tests/test_scaffold.py`

- [ ] **Step 1: Write failing scaffolding tests**

Create `tests/test_scaffold.py`:

```python
import tempfile
import unittest
from pathlib import Path

from value_invest_research.scaffold import init_event, init_stock, slugify


class ScaffoldTests(unittest.TestCase):
    def test_slugify_normalizes_event_names(self):
        self.assertEqual(slugify("US / Iran Conflict!"), "us_iran_conflict")

    def test_init_stock_creates_required_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_stock(root, "aapl", "Apple Inc.")

            stock_dir = root / "stocks" / "AAPL"
            self.assertTrue((stock_dir / "investment_memo.md").exists())
            self.assertTrue((stock_dir / "evidence.jsonl").exists())
            self.assertTrue((stock_dir / "data" / "fundamentals.json").exists())
            self.assertIn("Apple Inc.", (stock_dir / "company_profile.md").read_text(encoding="utf-8"))

    def test_init_event_creates_required_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_dir = init_event(root, "2026-05-06", "US Iran Conflict")

            self.assertEqual(event_dir.name, "2026-05-06_us_iran_conflict")
            self.assertTrue((event_dir / "event_brief.md").exists())
            self.assertTrue((event_dir / "candidate_screen.md").exists())
            self.assertTrue((event_dir / "tickers_to_review.yaml").exists())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_scaffold -v
```

Expected:

```text
ModuleNotFoundError: No module named 'value_invest_research.scaffold'
```

- [ ] **Step 3: Implement scaffolding**

Create `src/value_invest_research/scaffold.py`:

```python
from __future__ import annotations

import json
import re
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    return re.sub(r"_+", "_", slug).strip("_")


def _write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")


def init_stock(root: Path, ticker: str, company_name: str | None = None) -> Path:
    normalized_ticker = ticker.strip().upper()
    if not normalized_ticker:
        raise ValueError("ticker must be non-empty")

    display_name = company_name.strip() if company_name else normalized_ticker
    stock_dir = root / "stocks" / normalized_ticker
    for subdir in [
        stock_dir / "data",
        stock_dir / "raw" / "sec",
        stock_dir / "raw" / "earnings_calls",
        stock_dir / "raw" / "news",
        stock_dir / "logs",
    ]:
        subdir.mkdir(parents=True, exist_ok=True)

    _write_if_missing(
        stock_dir / "company_profile.md",
        f"# {normalized_ticker} Company Profile\n\n- Company: {display_name}\n- Ticker: {normalized_ticker}\n- Market: US equities\n",
    )
    _write_if_missing(stock_dir / "investment_memo.md", stock_memo_template(normalized_ticker))
    _write_if_missing(stock_dir / "hypotheses.md", f"# {normalized_ticker} Hypotheses\n\n## Active Hypotheses\n\n## Retired Hypotheses\n")
    _write_if_missing(stock_dir / "signals.md", f"# {normalized_ticker} Research Signals\n\n")
    _write_if_missing(stock_dir / "evidence.jsonl", "")
    _write_if_missing(stock_dir / "logs" / "runs.jsonl", "")
    _write_if_missing(stock_dir / "data" / "fundamentals.json", json.dumps({}, indent=2) + "\n")
    _write_if_missing(stock_dir / "data" / "sec_filings.json", json.dumps([], indent=2) + "\n")
    _write_if_missing(stock_dir / "data" / "news.jsonl", "")
    _write_if_missing(stock_dir / "data" / "prices.csv", "date,open,high,low,close,volume\n")
    return stock_dir


def init_event(root: Path, event_date: str, event_name: str) -> Path:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", event_date):
        raise ValueError("event_date must use YYYY-MM-DD")
    event_slug = slugify(event_name)
    if not event_slug:
        raise ValueError("event_name must contain letters or numbers")

    event_dir = root / "research" / "events" / f"{event_date}_{event_slug}"
    for subdir in [event_dir / "data", event_dir / "raw", event_dir / "logs"]:
        subdir.mkdir(parents=True, exist_ok=True)

    _write_if_missing(event_dir / "event_brief.md", event_brief_template(event_date, event_name))
    _write_if_missing(event_dir / "transmission_map.md", transmission_map_template(event_name))
    _write_if_missing(event_dir / "candidate_screen.md", candidate_screen_template(event_name))
    _write_if_missing(event_dir / "tickers_to_review.yaml", "tickers: []\n")
    _write_if_missing(event_dir / "evidence.jsonl", "")
    _write_if_missing(event_dir / "logs" / "runs.jsonl", "")
    return event_dir


def stock_memo_template(ticker: str) -> str:
    return f"""# {ticker} Investment Memo

## 1. Current View
- View: Needs Review
- Confidence: Low
- Last Updated:
- Key Thesis:
- Most Important Uncertainty:

## 2. Business Quality
- Business model:
- Revenue drivers:
- Customer value proposition:
- Competitive advantage:
- Durability:

## 3. Financial Quality
- Revenue growth:
- Margins:
- ROIC / ROE:
- Free cash flow:
- Balance sheet:
- Accounting quality:

## 4. Management & Capital Allocation
- Incentives:
- Buybacks and dividends:
- M&A:
- Shareholder communication:

## 5. Valuation
- Normalized earnings or FCF:
- Conservative assumptions:
- Downside case:
- Base case:
- Upside case:
- Margin of safety:

## 6. Risks & Disconfirming Evidence
- Thesis breakers:
- Competitive risks:
- Regulatory risks:
- Accounting concerns:
- Evidence that weakens the thesis:

## 7. Evidence Log

## 8. Open Questions
"""


def event_brief_template(event_date: str, event_name: str) -> str:
    return f"""# {event_name} Event Brief

- Date Opened: {event_date}
- Status: Active Research
- Goal: Identify investable candidates for deeper stock-level research.

## Confirmed Facts

## Unconfirmed Claims

## Immediate Questions

## Source Log
"""


def transmission_map_template(event_name: str) -> str:
    return f"""# {event_name} Transmission Map

## Primary Shock

## Transmission Channels

## Affected Sectors

## Candidate Company Mechanisms

## Disconfirming Paths
"""


def candidate_screen_template(event_name: str) -> str:
    return f"""# {event_name} Candidate Screen

## Tier 1: Immediate Deep Research

## Tier 2: Watchlist

## Tier 3: Evidence Too Weak

## Negative Watch
"""
```

- [ ] **Step 4: Run scaffolding tests**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_scaffold -v
```

Expected:

```text
OK
```

- [ ] **Step 5: Commit scaffolding**

Run:

```powershell
git add src/value_invest_research/scaffold.py tests/test_scaffold.py
git commit -m "feat: add research object scaffolding"
```

Expected:

```text
[main
```

---

### Task 4: Add Command Line Interface

**Files:**
- Create: `src/value_invest_research/cli.py`
- Create: `src/value_invest_research/__main__.py`
- Create: `tests/test_cli.py`

- [ ] **Step 1: Write failing CLI tests**

Create `tests/test_cli.py`:

```python
import tempfile
import unittest
from pathlib import Path

from value_invest_research.cli import main


class CliTests(unittest.TestCase):
    def test_init_stock_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            exit_code = main(["--root", tmp, "init-stock", "MSFT", "--company-name", "Microsoft Corporation"])
            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmp) / "stocks" / "MSFT" / "investment_memo.md").exists())

    def test_init_event_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            exit_code = main(["--root", tmp, "init-event", "2026-05-06", "US Iran Conflict"])
            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmp) / "research" / "events" / "2026-05-06_us_iran_conflict").exists())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_cli -v
```

Expected:

```text
ModuleNotFoundError: No module named 'value_invest_research.cli'
```

- [ ] **Step 3: Implement CLI**

Create `src/value_invest_research/cli.py`:

```python
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
```

Create `src/value_invest_research/__main__.py`:

```python
from value_invest_research.cli import main

raise SystemExit(main())
```

- [ ] **Step 4: Run CLI tests**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_cli -v
```

Expected:

```text
OK
```

- [ ] **Step 5: Run all Python tests**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests -v
```

Expected:

```text
OK
```

- [ ] **Step 6: Commit CLI**

Run:

```powershell
git add src/value_invest_research/cli.py src/value_invest_research/__main__.py tests/test_cli.py
git commit -m "feat: add research scaffold CLI"
```

Expected:

```text
[main
```

---

### Task 5: Add Value Investment Research Skill

**Files:**
- Create: `skills/value_invest_research/SKILL.md`
- Create: `skills/value_invest_research/frameworks/value_investing.md`
- Create: `skills/value_invest_research/frameworks/event_research.md`
- Create: `skills/value_invest_research/frameworks/sector_research.md`
- Create: `skills/value_invest_research/checklists/evidence_quality.md`
- Create: `skills/value_invest_research/checklists/disconfirming_evidence.md`
- Create: `skills/value_invest_research/checklists/valuation_review.md`
- Create: `skills/value_invest_research/prompts/update_stock_memo.md`
- Create: `skills/value_invest_research/prompts/run_event_research.md`
- Create: `skills/value_invest_research/prompts/run_sector_research.md`

- [ ] **Step 1: Create Skill directories**

Run:

```powershell
New-Item -ItemType Directory -Force skills\value_invest_research\frameworks,skills\value_invest_research\checklists,skills\value_invest_research\prompts
```

Expected:

```text
Directory:
```

- [ ] **Step 2: Create Skill entrypoint**

Create `skills/value_invest_research/SKILL.md`:

```markdown
---
name: value-invest-research
description: Use for US equity investment research workflows that collect evidence, update stock memos, run sector/theme research, or analyze sudden market events using a value-investing framework.
---

# Value Investment Research Skill

This Skill turns heterogeneous market information into auditable research artifacts. It supports three workflows:

1. `update_stock_memo`: update one company memo using the value-investing framework.
2. `run_sector_or_theme_research`: map an industry or theme and identify companies worth stock-level research.
3. `run_event_research`: analyze a sudden event, build transmission chains, and rank candidate tickers for human review.

## Non-Negotiable Rules

- Do not issue final trading instructions.
- Separate facts, inferences, and judgments.
- Cite evidence IDs for every material claim.
- Treat low-reliability sources as research leads only.
- Search for disconfirming evidence before strengthening a thesis.
- Preserve prior thesis history when updating a memo.
- Mark uncertainty directly instead of hiding it.

## Required Context Loading

Before analysis, load the relevant research object folder:

- Canonical memo.
- `evidence.jsonl`.
- Structured files under `data/`.
- Latest run logs under `logs/`.
- Related stock, sector, theme, or event objects named in the task.

## Workflow Routing

- Use `frameworks/value_investing.md` and `prompts/update_stock_memo.md` for individual companies.
- Use `frameworks/sector_research.md` and `prompts/run_sector_research.md` for industry or theme work.
- Use `frameworks/event_research.md` and `prompts/run_event_research.md` for sudden event research.
- Use `checklists/evidence_quality.md` for all workflows.
- Use `checklists/disconfirming_evidence.md` before any thesis-strengthening output.
- Use `checklists/valuation_review.md` before changing valuation conclusions.
```

- [ ] **Step 3: Create framework files**

Create `skills/value_invest_research/frameworks/value_investing.md`:

```markdown
# Value Investing Framework

Evaluate each company through:

1. Business quality: business model, revenue drivers, customer value, competitive advantage, durability.
2. Financial quality: growth, margins, ROIC or ROE, free cash flow, balance sheet, accounting quality.
3. Management and capital allocation: incentives, buybacks, dividends, M&A, shareholder communication.
4. Valuation: normalized earnings or free cash flow, downside/base/upside cases, margin of safety.
5. Risks and disconfirming evidence: thesis breakers, competition, regulation, accounting concerns.

Research views are `watch`, `attractive`, `expensive`, `avoid`, or `needs_review`.
Confidence levels are `low`, `medium`, and `high`.
```

Create `skills/value_invest_research/frameworks/event_research.md`:

```markdown
# Event Research Framework

Use this for sudden shocks such as geopolitical conflict, regulatory action, commodity disruption, product breakthroughs, or financial stress.

Process:

1. State confirmed facts.
2. Separate unconfirmed claims and rumors.
3. Build transmission chains from event to economic mechanism.
4. Map affected sectors, themes, and companies.
5. Screen candidates by direct exposure, financial sensitivity, balance sheet, valuation, and market pricing.
6. Rank candidates into Tier 1, Tier 2, Tier 3, and Negative Watch.
7. Promote only Tier 1 candidates with evidence-backed mechanisms into stock-level memo updates.

Do not jump directly from news headline to ticker conclusion.
```

Create `skills/value_invest_research/frameworks/sector_research.md`:

```markdown
# Sector And Theme Research Framework

Use this to understand an industry, theme, value chain, or cross-sector trend.

Process:

1. Define the research object and scope.
2. Map industry structure, value chain, profit pools, and barriers to entry.
3. Identify demand drivers, cycle variables, and key metrics.
4. Build a company map: leaders, challengers, niche compounders, cyclical candidates, and avoid/watch names.
5. Compare companies on quality, growth, balance sheet, valuation, and risks.
6. Output candidate companies for stock-level research.
```

- [ ] **Step 4: Create checklists**

Create `skills/value_invest_research/checklists/evidence_quality.md`:

```markdown
# Evidence Quality Checklist

Reliability levels:

- `primary`: SEC filings, company investor relations, official transcripts, audited financials.
- `high`: reputable financial press, exchange data, established data providers.
- `medium`: specialist blogs, expert commentary, industry newsletters.
- `low`: social media, unattributed rumors, unsourced summaries.

Materiality levels:

- `low`: background context.
- `medium`: affects a section of a memo.
- `high`: materially affects a candidate, risk, or estimate.
- `thesis_change`: can change current view or confidence.

Rules:

- Low-reliability evidence cannot trigger `thesis_change`.
- Uncited material claims must be rejected.
- Conflicting evidence must be recorded as a conflict, not averaged away.
```

Create `skills/value_invest_research/checklists/disconfirming_evidence.md`:

```markdown
# Disconfirming Evidence Checklist

Before strengthening a thesis, ask:

- What evidence would make this thesis wrong?
- Did margins, returns, cash conversion, or balance sheet quality move against the thesis?
- Is the market reaction explained by short-term sentiment instead of durable economics?
- Are competitors benefiting more?
- Is regulation, accounting quality, customer concentration, or capital allocation weakening?
- Is valuation already pricing the positive scenario?
```

Create `skills/value_invest_research/checklists/valuation_review.md`:

```markdown
# Valuation Review Checklist

Before changing valuation conclusions:

- Identify normalized earnings or free cash flow.
- Separate cyclical peak/trough effects from durable economics.
- Record downside, base, and upside assumptions.
- Compare current price to conservative value range.
- State margin of safety.
- State which assumption would most change the conclusion.
```

- [ ] **Step 5: Create prompt contracts**

Create `skills/value_invest_research/prompts/update_stock_memo.md`:

```markdown
# Update Stock Memo Prompt Contract

Inputs:

- Existing `investment_memo.md`.
- Existing `evidence.jsonl`.
- New evidence records.
- Structured data under `data/`.

Output:

1. Memo update summary.
2. Proposed markdown patch by section.
3. Stock signal YAML.
4. Human review actions.

Required checks:

- Every material claim cites evidence IDs.
- Current view changes require at least one primary or high-reliability evidence item.
- Low-reliability evidence creates open questions only.
```

Create `skills/value_invest_research/prompts/run_event_research.md`:

```markdown
# Run Event Research Prompt Contract

Inputs:

- Event brief.
- Event playbook.
- Evidence records.
- Existing sector, theme, and stock context when available.

Output:

1. Confirmed facts.
2. Unconfirmed claims.
3. Transmission map.
4. Candidate screen with Tier 1, Tier 2, Tier 3, and Negative Watch.
5. `tickers_to_review.yaml` content.
6. Human review actions.
```

Create `skills/value_invest_research/prompts/run_sector_research.md`:

```markdown
# Run Sector Or Theme Research Prompt Contract

Inputs:

- Sector or theme memo.
- Evidence records.
- Company map when available.

Output:

1. Updated industry or theme structure.
2. Key metrics.
3. Company map.
4. Cross-company comparison.
5. Candidate companies for stock-level research.
6. Human review actions.
```

- [ ] **Step 6: Commit Skill files**

Run:

```powershell
git add skills/value_invest_research
git commit -m "feat: add investment research skill"
```

Expected:

```text
[main
```

---

### Task 6: Add Config Templates

**Files:**
- Create: `config/watchlist.yaml`
- Create: `config/event_playbooks.yaml`
- Create: `config/source_priority.yaml`
- Create: `config/research_objects.yaml`

- [ ] **Step 1: Create config directory**

Run:

```powershell
New-Item -ItemType Directory -Force config
```

Expected:

```text
Directory:
```

- [ ] **Step 2: Create config files**

Create `config/watchlist.yaml`:

```yaml
market: US
stocks:
  - ticker: AAPL
    company_name: Apple Inc.
    status: research_seed
```

Create `config/event_playbooks.yaml`:

```yaml
geopolitical_conflict:
  first_questions:
    - What happened, and what is confirmed?
    - Which geographies, commodities, supply chains, or military systems are directly involved?
    - What is the plausible duration and escalation path?
  transmission_channels:
    - energy_prices
    - shipping_routes
    - insurance_costs
    - defense_spending
    - inflation_expectations
    - currency_safe_haven
  affected_sectors:
    potential_positive:
      - energy_producers
      - defense_contractors
      - shipping
      - commodity_infrastructure
    potential_negative:
      - airlines
      - chemicals
      - travel
      - import_dependent_retail
  mandatory_checks:
    - Does the company have direct exposure?
    - Is the impact material to earnings or free cash flow?
    - Is the move already priced in?
    - What evidence would falsify the event thesis?
```

Create `config/source_priority.yaml`:

```yaml
reliability:
  primary:
    - sec_filing
    - company_ir
    - official_transcript
    - audited_financials
  high:
    - exchange_data
    - established_market_data_provider
    - reputable_financial_press
  medium:
    - specialist_blog
    - expert_commentary
    - industry_newsletter
  low:
    - social_media
    - unattributed_rumor
    - unsourced_summary
```

Create `config/research_objects.yaml`:

```yaml
stocks:
  - stocks/AAPL
sectors: []
themes: []
events: []
```

- [ ] **Step 3: Commit config templates**

Run:

```powershell
git add config
git commit -m "feat: add research config templates"
```

Expected:

```text
[main
```

---

### Task 7: Seed Initial Research Objects

**Files:**
- Create through CLI: `stocks/AAPL/**`
- Create through CLI: `research/events/2026-05-06_us_iran_conflict/**`

- [ ] **Step 1: Initialize stock folder**

Run:

```powershell
$env:PYTHONPATH='src'; python -m value_invest_research --root . init-stock AAPL --company-name "Apple Inc."
```

Expected:

```text
stocks\AAPL
```

- [ ] **Step 2: Initialize event folder**

Run:

```powershell
$env:PYTHONPATH='src'; python -m value_invest_research --root . init-event 2026-05-06 "US Iran Conflict"
```

Expected:

```text
research\events\2026-05-06_us_iran_conflict
```

- [ ] **Step 3: Validate generated files exist**

Run:

```powershell
Test-Path stocks\AAPL\investment_memo.md
Test-Path research\events\2026-05-06_us_iran_conflict\candidate_screen.md
```

Expected:

```text
True
True
```

- [ ] **Step 4: Commit seed research objects**

Run:

```powershell
git add stocks research
git commit -m "chore: seed initial research objects"
```

Expected:

```text
[main
```

---

### Task 8: Final Verification

**Files:**
- No new files.

- [ ] **Step 1: Run all tests**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests -v
```

Expected:

```text
OK
```

- [ ] **Step 2: Validate empty evidence logs**

Run:

```powershell
$env:PYTHONPATH='src'; python -m value_invest_research --root . validate-evidence stocks\AAPL\evidence.jsonl
$env:PYTHONPATH='src'; python -m value_invest_research --root . validate-evidence research\events\2026-05-06_us_iran_conflict\evidence.jsonl
```

Expected:

```text

```

Both commands exit with code `0`.

- [ ] **Step 3: Review changed files**

Run:

```powershell
git status --short
```

Expected:

```text

```

Working tree is clean after all commits.

## Self-Review

Spec coverage:

- Repository skeleton and document templates: covered by Tasks 1, 3, 5, 6, and 7.
- Evidence and signal schemas: covered by Task 2.
- Skill protocol and framework files: covered by Task 5.
- Event playbook: covered by Task 6.
- Initialization of one stock and one event: covered by Task 7.
- Live SEC/news/price ingestion: intentionally deferred because the spec roadmap places ingestion after the foundation.
- LLM memo-update workflow: intentionally deferred until the Skill files and evidence contracts exist.

Banned-pattern scan:

- Passed for incomplete-step markers and unspecified implementation steps.

Type consistency:

- `EvidenceRecord`, `SignalDriver`, `StockSignal`, and `ValidationError` are defined in Task 2 and imported consistently in later tasks.
- `init_stock`, `init_event`, and `slugify` are defined in Task 3 and used consistently in Task 4.
- CLI command names are consistent across tests and final verification.
