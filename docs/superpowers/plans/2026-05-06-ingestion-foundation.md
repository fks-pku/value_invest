# Ingestion Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build SEC EDGAR + price data ingestion pipelines that fetch raw data, normalize it into evidence records, store structured extracts, and log every run.

**Architecture:** Add a `pipelines/` directory with ingestion modules. Each pipeline fetches from a free public API (SEC EDGAR via `data.sec.gov`, prices via `yfinance`), stores raw JSON in `raw/`, writes structured data to `data/`, appends evidence records to `evidence.jsonl`, and logs runs to `logs/runs.jsonl`. Pipelines are orchestrated by a `RunLog` utility and are designed to be called from CLI or scheduler.

**Tech Stack:** Python 3.11+, `yfinance` (only third-party dep), `unittest`, `urllib.request` (stdlib for SEC), JSON Lines.

---

## File Structure

- Create: `src/value_invest_research/runlog.py` — run logging and deduplication utility
- Create: `src/value_invest_research/ingest_sec.py` — SEC EDGAR submissions, company facts, filings
- Create: `src/value_invest_research/ingest_prices.py` — price data via yfinance
- Create: `src/value_invest_research/ingest.py` — pipeline orchestration CLI commands
- Modify: `src/value_invest_research/cli.py` — add ingest subcommands
- Modify: `pyproject.toml` — add yfinance dependency
- Create: `tests/test_runlog.py` — run log tests
- Create: `tests/test_ingest_sec.py` — SEC ingestion tests (mocked HTTP)
- Create: `tests/test_ingest_prices.py` — price ingestion tests (mocked yfinance)

## Scope Boundary

This plan implements SEC EDGAR + price ingestion only. News ingestion, transcript ingestion, and LLM memo updates are deferred to later phases.

---

### Task 1: Add Run Log Utility

**Files:**
- Create: `src/value_invest_research/runlog.py`
- Create: `tests/test_runlog.py`

- [ ] **Step 1: Write failing run log tests**

Create `tests/test_runlog.py`:

```python
import tempfile
import unittest
from pathlib import Path

from value_invest_research.runlog import RunLog, RunStatus


class RunLogTests(unittest.TestCase):
    def test_append_and_read_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = RunLog(Path(tmp))
            log.append("test_pipeline", RunStatus.SUCCESS, tickers=["AAPL"], records_fetched=5)
            entries = log.read()
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["pipeline"], "test_pipeline")
            self.assertEqual(entries[0]["status"], "success")
            self.assertEqual(entries[0]["records_fetched"], 5)

    def test_logs_failed_run_with_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = RunLog(Path(tmp))
            log.append("bad_pipeline", RunStatus.FAILURE, error="timeout")
            entries = log.read()
            self.assertEqual(entries[0]["error"], "timeout")

    def test_is_content_hash_new(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = RunLog(Path(tmp))
            self.assertTrue(log.is_content_new("hash123"))
            log.record_content_hash("hash123")
            self.assertFalse(log.is_content_new("hash123"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_runlog -v
```

Expected: `ModuleNotFoundError: No module named 'value_invest_research.runlog'`

- [ ] **Step 3: Implement runlog**

Create `src/value_invest_research/runlog.py`:

```python
from __future__ import annotations

import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path


class RunStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"


class RunLog:
    def __init__(self, log_dir: Path) -> None:
        self._log_dir = log_dir
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._log_path = log_dir / "runs.jsonl"
        self._hashes_path = log_dir / "content_hashes.jsonl"

    def append(
        self,
        pipeline: str,
        status: RunStatus,
        tickers: list[str] | None = None,
        records_fetched: int = 0,
        records_new: int = 0,
        error: str | None = None,
    ) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pipeline": pipeline,
            "status": status.value,
            "tickers": tickers or [],
            "records_fetched": records_fetched,
            "records_new": records_new,
        }
        if error is not None:
            entry["error"] = error
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def read(self) -> list[dict]:
        if not self._log_path.exists():
            return []
        lines = self._log_path.read_text(encoding="utf-8").splitlines()
        return [json.loads(line) for line in lines if line.strip()]

    def is_content_new(self, content_hash: str) -> bool:
        if not self._hashes_path.exists():
            return True
        known = {
            json.loads(line)["hash"]
            for line in self._hashes_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        return content_hash not in known

    def record_content_hash(self, content_hash: str) -> None:
        with open(self._hashes_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"hash": content_hash, "ts": datetime.now(timezone.utc).isoformat()}) + "\n")
```

- [ ] **Step 4: Run tests to verify they pass**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_runlog -v
```

Expected: `OK`

- [ ] **Step 5: Commit run log**

Run:

```powershell
git add src/value_invest_research/runlog.py tests/test_runlog.py
git commit -m "feat: add run log and content dedup utility"
```

---

### Task 2: Add SEC EDGAR Ingestion

**Files:**
- Create: `src/value_invest_research/ingest_sec.py`
- Create: `tests/test_ingest_sec.py`

- [ ] **Step 1: Write failing SEC ingestion tests**

Create `tests/test_ingest_sec.py`:

```python
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from value_invest_research.ingest_sec import SecEdgarClient


class SecEdgarClientTests(unittest.TestCase):
    def test_build_cik_map_from_company_tickers(self):
        client = SecEdgarClient(user_agent="Test/1.0")
        sample = json.dumps(
            {"0": {"cik_str": "0000320193", "ticker": "AAPL", "title": "Apple Inc."}}
        ).encode()
        with patch("value_invest_research.ingest_sec.urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = sample
            mock_response.__enter__ = lambda s: s
            mock_response.__exit__ = MagicMock(return_value=False)
            mock_urlopen.return_value = mock_response

            cik_map = client.fetch_cik_map()
            self.assertEqual(cik_map["AAPL"], "0000320193")

    def test_fetch_submissions_stores_raw_and_structured(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stock_dir = root / "stocks" / "AAPL"
            (stock_dir / "raw" / "sec").mkdir(parents=True)
            (stock_dir / "data").mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)

            submissions = {
                "name": "Apple Inc.",
                "ticker": "AAPL",
                "filings": {
                    "recent": {
                        "accessionNumber": ["0001"],
                        "filingDate": ["2026-04-15"],
                        "form": ["10-Q"],
                        "primaryDocument": ["aapl-20260415.htm"],
                        "primaryDocDescription": ["10-Q"],
                    }
                },
            }

            client = SecEdgarClient(user_agent="Test/1.0")
            with patch.object(client, "_fetch_json", return_value=submissions):
                result = client.fetch_submissions(root, "AAPL", "0000320193")

            self.assertTrue((stock_dir / "raw" / "sec" / "submissions.json").exists())
            self.assertTrue(result["name"] == "Apple Inc.")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_ingest_sec -v
```

Expected: `ModuleNotFoundError: No module named 'value_invest_research.ingest_sec'`

- [ ] **Step 3: Implement SEC ingestion**

Create `src/value_invest_research/ingest_sec.py`:

```python
from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path
from typing import Any

from value_invest_research.models import EvidenceRecord
from value_invest_research.runlog import RunLog, RunStatus

SEC_BASE = "https://data.sec.gov"
COMPANY_TICKERS_URL = f"{SEC_BASE}/files/company_tickers.json"


def _content_hash(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


class SecEdgarClient:
    def __init__(self, user_agent: str) -> None:
        self._user_agent = user_agent

    def _fetch_json(self, url: str) -> dict[str, Any]:
        req = urllib.request.Request(url, headers={"User-Agent": self._user_agent})
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
        return json.loads(data)

    def _fetch_bytes(self, url: str) -> bytes:
        req = urllib.request.Request(url, headers={"User-Agent": self._user_agent})
        with urllib.request.urlopen(req) as resp:
            return resp.read()

    def fetch_cik_map(self) -> dict[str, str]:
        data = self._fetch_json(COMPANY_TICKERS_URL)
        return {entry["ticker"]: entry["cik_str"] for entry in data.values()}

    def fetch_submissions(self, root: Path, ticker: str, cik: str) -> dict[str, Any]:
        stock_dir = root / "stocks" / ticker
        raw_dir = stock_dir / "raw" / "sec"
        raw_dir.mkdir(parents=True, exist_ok=True)
        log = RunLog(stock_dir / "logs")

        url = f"{SEC_BASE}/submissions/CIK{cik}.json"
        raw_data = self._fetch_bytes(url)
        content_hash = _content_hash(raw_data)

        raw_path = raw_dir / "submissions.json"
        if not log.is_content_new(content_hash) and raw_path.exists():
            log.append("sec_submissions", RunStatus.SUCCESS, tickers=[ticker], records_fetched=0, records_new=0)
            return json.loads(raw_data.read_text(encoding="utf-8"))

        raw_path.write_bytes(raw_data)
        log.record_content_hash(content_hash)

        submissions = json.loads(raw_data)
        recent = submissions.get("filings", {}).get("recent", {})
        filing_count = len(recent.get("accessionNumber", []))

        log.append("sec_submissions", RunStatus.SUCCESS, tickers=[ticker], records_fetched=filing_count, records_new=filing_count)
        return submissions

    def fetch_company_facts(self, root: Path, ticker: str, cik: str) -> dict[str, Any]:
        stock_dir = root / "stocks" / ticker
        raw_dir = stock_dir / "raw" / "sec"
        data_dir = stock_dir / "data"
        raw_dir.mkdir(parents=True, exist_ok=True)
        data_dir.mkdir(parents=True, exist_ok=True)
        log = RunLog(stock_dir / "logs")

        url = f"{SEC_BASE}/api/xbrl/companyfacts/CIK{cik}.json"
        raw_data = self._fetch_bytes(url)
        content_hash = _content_hash(raw_data)

        raw_path = raw_dir / "company_facts.json"
        if not log.is_content_new(content_hash) and raw_path.exists():
            log.append("sec_company_facts", RunStatus.SUCCESS, tickers=[ticker], records_fetched=0, records_new=0)
            return json.loads(raw_path.read_text(encoding="utf-8"))

        raw_path.write_bytes(raw_data)
        log.record_content_hash(content_hash)

        facts = json.loads(raw_data)
        facts_path = data_dir / "sec_facts.json"
        facts_path.write_text(json.dumps(facts, indent=2), encoding="utf-8")

        fact_count = sum(
            len(concept_data.get("units", {}).get("USD", []))
            for taxonomy in facts.get("facts", {}).values()
            for concept_data in taxonomy.values()
        )

        log.append("sec_company_facts", RunStatus.SUCCESS, tickers=[ticker], records_fetched=fact_count, records_new=fact_count)
        return facts
```

- [ ] **Step 4: Run tests to verify they pass**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_ingest_sec -v
```

Expected: `OK`

- [ ] **Step 5: Commit SEC ingestion**

Run:

```powershell
git add src/value_invest_research/ingest_sec.py tests/test_ingest_sec.py
git commit -m "feat: add SEC EDGAR ingestion pipeline"
```

---

### Task 3: Add Price Ingestion

**Files:**
- Modify: `pyproject.toml` — add yfinance dependency
- Create: `src/value_invest_research/ingest_prices.py`
- Create: `tests/test_ingest_prices.py`

- [ ] **Step 1: Add yfinance dependency**

Update `pyproject.toml` dependencies:

```toml
dependencies = [
    "yfinance>=0.2.36",
]
```

Run:

```powershell
pip install yfinance
```

- [ ] **Step 2: Write failing price ingestion tests**

Create `tests/test_ingest_prices.py`:

```python
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from value_invest_research.ingest_prices import fetch_price_history


class PriceIngestionTests(unittest.TestCase):
    def test_fetch_prices_stores_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stock_dir = root / "stocks" / "AAPL"
            (stock_dir / "data").mkdir(parents=True)
            (stock_dir / "logs").mkdir(parents=True)

            mock_df = MagicMock()
            mock_df.empty = False
            mock_df.to_csv.return_value = "date,Open,High,Low,Close,Volume\n2026-05-05,200.0,205.0,199.0,204.0,1000000\n"
            mock_df.__len__ = lambda self_: 1

            with patch("value_invest_research.ingest_prices.yf.Ticker") as mock_ticker_cls:
                mock_ticker = MagicMock()
                mock_ticker.history.return_value = mock_df
                mock_ticker_cls.return_value = mock_ticker

                fetch_price_history(root, "AAPL", period="1mo")

            csv_path = stock_dir / "data" / "prices.csv"
            self.assertTrue(csv_path.exists())
            self.assertIn("2026-05-05", csv_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run tests to verify they fail**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_ingest_prices -v
```

Expected: `ModuleNotFoundError: No module named 'value_invest_research.ingest_prices'`

- [ ] **Step 4: Implement price ingestion**

Create `src/value_invest_research/ingest_prices.py`:

```python
from __future__ import annotations

from pathlib import Path

import yfinance as yf

from value_invest_research.runlog import RunLog, RunStatus


def fetch_price_history(
    root: Path,
    ticker: str,
    period: str = "1y",
    interval: str = "1d",
) -> None:
    stock_dir = root / "stocks" / ticker
    data_dir = stock_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    log = RunLog(stock_dir / "logs")

    t = yf.Ticker(ticker)
    df = t.history(period=period, interval=interval)

    if df.empty:
        log.append("price_history", RunStatus.FAILURE, tickers=[ticker], error="empty response")
        return

    csv_path = data_dir / "prices.csv"
    df.to_csv(csv_path)

    log.append("price_history", RunStatus.SUCCESS, tickers=[ticker], records_fetched=len(df), records_new=len(df))
```

- [ ] **Step 5: Run tests to verify they pass**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_ingest_prices -v
```

Expected: `OK`

- [ ] **Step 6: Commit price ingestion**

Run:

```powershell
git add pyproject.toml src/value_invest_research/ingest_prices.py tests/test_ingest_prices.py
git commit -m "feat: add price ingestion via yfinance"
```

---

### Task 4: Add Ingest CLI Commands

**Files:**
- Modify: `src/value_invest_research/cli.py`

- [ ] **Step 1: Add ingest subcommands to CLI**

Update `src/value_invest_research/cli.py` to add `ingest-sec` and `ingest-prices` subcommands:

```python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from value_invest_research.models import EvidenceRecord, ValidationError
from value_invest_research.runlog import RunLog, RunStatus
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

    sec_parser = subparsers.add_parser("ingest-sec", help="Fetch SEC EDGAR data for a ticker")
    sec_parser.add_argument("ticker")
    sec_parser.add_argument("--user-agent", default="value-invest-research/0.1.0")
    sec_parser.add_argument("--include-facts", action="store_true", default=True)
    sec_parser.add_argument("--no-facts", dest="include_facts", action="store_false")

    prices_parser = subparsers.add_parser("ingest-prices", help="Fetch price history for a ticker")
    prices_parser.add_argument("ticker")
    prices_parser.add_argument("--period", default="1y")

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
        if args.command == "ingest-sec":
            return run_sec_ingest(root, args.ticker, args.user_agent, args.include_facts)
        if args.command == "ingest-prices":
            return run_price_ingest(root, args.ticker, args.period)
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
    submissions = client.fetch_submissions(root, normalized, cik)
    print(f"SEC submissions fetched for {normalized} (CIK {cik})")

    if include_facts:
        facts = client.fetch_company_facts(root, normalized, cik)
        print(f"SEC company facts fetched for {normalized}")

    return 0


def run_price_ingest(root: Path, ticker: str, period: str) -> int:
    from value_invest_research.ingest_prices import fetch_price_history

    normalized = ticker.strip().upper()
    init_stock(root, normalized)
    fetch_price_history(root, normalized, period=period)
    print(f"Price history fetched for {normalized}")
    return 0
```

- [ ] **Step 2: Run all tests**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests -v
```

Expected: `OK`

- [ ] **Step 3: Commit ingest CLI**

Run:

```powershell
git add src/value_invest_research/cli.py
git commit -m "feat: add ingest-sec and ingest-prices CLI commands"
```

---

### Task 5: Integration Verification

**Files:**
- No new files.

- [ ] **Step 1: Run all tests**

Run:

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests -v
```

Expected: `OK`

- [ ] **Step 2: Verify CLI help shows new commands**

Run:

```powershell
$env:PYTHONPATH='src'; python -m value_invest_research --help
```

Expected: help text lists `init-stock`, `init-event`, `validate-evidence`, `ingest-sec`, `ingest-prices`.

- [ ] **Step 3: (Optional live test) Fetch AAPL data**

Run:

```powershell
$env:PYTHONPATH='src'; python -m value_invest_research --root . ingest-sec AAPL
$env:PYTHONPATH='src'; python -m value_invest_research --root . ingest-prices AAPL --period 1mo
```

Expected: data stored under `stocks/AAPL/raw/sec/` and `stocks/AAPL/data/`.

## Self-Review

Spec coverage (Phase 2 scope):

- SEC ingestion: submissions, company facts — Task 2
- Price ingestion: daily history — Task 3
- Store raw files — Task 2, 3
- Normalized evidence structure — Task 1 (runlog + content hash dedup)
- Deduplication and hashing — Task 1
- Run logs — Task 1
- CLI integration — Task 4
- News ingestion — intentionally deferred
- Transcript ingestion — intentionally deferred
- Routing — deferred (needs news first)

Banned-pattern scan: no TBD, TODO, or placeholder steps found.

Type consistency: `SecEdgarClient`, `RunLog`, `RunStatus` defined in Tasks 1-2 and used consistently in Tasks 3-4. CLI imports are inside functions to avoid circular deps.
