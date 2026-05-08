from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path
from typing import Any

from value_invest_research.runlog import RunLog, RunStatus

SEC_BASE = "https://data.sec.gov"
COMPANY_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"


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
        return {entry["ticker"]: str(entry["cik_str"]).zfill(10) for entry in data.values()}

    @staticmethod
    def _cik_url(cik: str) -> str:
        padded = str(cik).zfill(10)
        return f"CIK{padded}.json"

    def fetch_submissions(self, root: Path, ticker: str, cik: str) -> dict[str, Any]:
        stock_dir = root / "stocks" / ticker
        raw_dir = stock_dir / "raw" / "sec"
        raw_dir.mkdir(parents=True, exist_ok=True)
        log = RunLog(stock_dir / "logs")

        url = f"{SEC_BASE}/submissions/{self._cik_url(cik)}"
        raw_data = self._fetch_bytes(url)
        chash = _content_hash(raw_data)

        raw_path = raw_dir / "submissions.json"
        if not log.is_content_new(chash) and raw_path.exists():
            log.append("sec_submissions", RunStatus.SUCCESS, tickers=[ticker], records_fetched=0, records_new=0)
            return json.loads(raw_path.read_text(encoding="utf-8"))

        raw_path.write_bytes(raw_data)
        log.record_content_hash(chash)

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

        url = f"{SEC_BASE}/api/xbrl/companyfacts/{self._cik_url(cik)}"
        raw_data = self._fetch_bytes(url)
        chash = _content_hash(raw_data)

        raw_path = raw_dir / "company_facts.json"
        if not log.is_content_new(chash) and raw_path.exists():
            log.append("sec_company_facts", RunStatus.SUCCESS, tickers=[ticker], records_fetched=0, records_new=0)
            return json.loads(raw_path.read_text(encoding="utf-8"))

        raw_path.write_bytes(raw_data)
        log.record_content_hash(chash)

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
