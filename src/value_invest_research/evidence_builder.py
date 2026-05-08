from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from value_invest_research.models import EvidenceRecord
from value_invest_research.runlog import RunLog, RunStatus


SEC_METRICS = {
    "RevenueFromContractWithCustomerExcludingAssessedTax": ("revenue", "Revenue"),
    "NetIncomeLoss": ("net_income", "Net income"),
    "OperatingIncomeLoss": ("operating_income", "Operating income"),
    "GrossProfit": ("gross_profit", "Gross profit"),
    "Assets": ("assets", "Assets"),
    "Liabilities": ("liabilities", "Liabilities"),
    "StockholdersEquity": ("equity", "Stockholders equity"),
    "CashAndCashEquivalentsAtCarryingValue": ("cash", "Cash and cash equivalents"),
    "FreeCashFlow": ("free_cash_flow", "Free cash flow"),
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _date_to_timestamp(value: str | None) -> str | None:
    if not value:
        return None
    return f"{value}T00:00:00Z"


def _stable_hash(data: dict[str, Any]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _local_url(path: Path) -> str:
    return "local://" + path.as_posix()


def _read_existing_keys(evidence_path: Path) -> tuple[set[str], set[str]]:
    if not evidence_path.exists():
        return set(), set()

    ids: set[str] = set()
    hashes: set[str] = set()
    for line in evidence_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        data = json.loads(line)
        if data.get("id"):
            ids.add(data["id"])
        if data.get("hash"):
            hashes.add(data["hash"])
    return ids, hashes


def _append_unique_records(evidence_path: Path, records: list[EvidenceRecord]) -> int:
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.touch(exist_ok=True)
    known_ids, known_hashes = _read_existing_keys(evidence_path)

    new_records = [
        record
        for record in records
        if record.id not in known_ids and record.hash not in known_hashes
    ]
    if not new_records:
        return 0

    with evidence_path.open("a", encoding="utf-8", newline="\n") as fh:
        for record in new_records:
            fh.write(json.dumps(record.to_dict(), sort_keys=True) + "\n")
    return len(new_records)


def _latest_usd_fact(sec_facts: dict[str, Any], tag: str) -> dict[str, Any] | None:
    fact = sec_facts.get("facts", {}).get("us-gaap", {}).get(tag, {})
    units = fact.get("units", {})
    for unit in ("USD", "USD/shares", "shares"):
        entries = units.get(unit, [])
        if entries:
            return sorted(entries, key=lambda item: (item.get("end", ""), item.get("filed", "")))[-1] | {"unit": unit}
    return None


def _build_sec_fact_records(root: Path, ticker: str, fetched_at: str) -> list[EvidenceRecord]:
    stock_dir = root / "stocks" / ticker
    sec_facts_path = stock_dir / "data" / "sec_facts.json"
    if not sec_facts_path.exists():
        return []

    sec_facts = json.loads(sec_facts_path.read_text(encoding="utf-8"))
    records: list[EvidenceRecord] = []
    for tag, (slug, label) in SEC_METRICS.items():
        latest = _latest_usd_fact(sec_facts, tag)
        if not latest:
            continue

        period_end = latest.get("end", "")
        period_key = period_end.replace("-", "") or "unknown_period"
        value = latest.get("val")
        form = latest.get("form", "unknown form")
        unit = latest.get("unit", "unknown unit")
        source = {
            "ticker": ticker,
            "tag": tag,
            "value": value,
            "unit": unit,
            "period_end": period_end,
            "filed": latest.get("filed"),
            "form": form,
        }
        record = EvidenceRecord.from_dict({
            "id": f"ev_{ticker.lower()}_sec_{slug}_{period_key}",
            "research_object": f"stocks/{ticker}",
            "source_type": "sec_fact",
            "source_name": f"SEC XBRL {label}",
            "url": _local_url(sec_facts_path),
            "published_at": _date_to_timestamp(latest.get("filed")),
            "fetched_at": fetched_at,
            "hash": _stable_hash(source),
            "tickers": [ticker],
            "sectors": [],
            "themes": [],
            "summary": f"{label} was {value} {unit} for period ending {period_end} in {form}.",
            "reliability": "primary",
            "materiality": "medium",
            "used_in": [],
        })
        records.append(record)
    return records


def _get_field(row: dict[str, str], name: str) -> str:
    wanted = name.lower()
    for key, value in row.items():
        if key.lower() == wanted:
            return value
    return ""


def _build_price_records(root: Path, ticker: str, fetched_at: str) -> list[EvidenceRecord]:
    stock_dir = root / "stocks" / ticker
    prices_path = stock_dir / "data" / "prices.csv"
    if not prices_path.exists():
        return []

    rows = [
        row
        for row in csv.DictReader(prices_path.read_text(encoding="utf-8").splitlines())
        if row
    ]
    if not rows:
        return []

    latest = rows[-1]
    previous = rows[-2] if len(rows) > 1 else None
    latest_date = _get_field(latest, "date") or latest.get("Date", "")
    latest_close = _get_field(latest, "close")
    summary = f"{ticker} closed at {latest_close} on {latest_date}."
    materiality = "low"

    if previous:
        previous_close = _get_field(previous, "close")
        try:
            latest_value = float(latest_close)
            previous_value = float(previous_close)
            if previous_value:
                pct_change = (latest_value / previous_value - 1) * 100
                summary = f"{ticker} closed at {latest_close} on {latest_date}, {pct_change:.2f}% versus the prior row."
                if abs(pct_change) >= 5:
                    materiality = "medium"
        except ValueError:
            pass

    source = {"ticker": ticker, "date": latest_date, "close": latest_close, "summary": summary}
    return [
        EvidenceRecord.from_dict({
            "id": f"ev_{ticker.lower()}_price_{latest_date.replace('-', '') or 'latest'}",
            "research_object": f"stocks/{ticker}",
            "source_type": "market_price",
            "source_name": "Price history",
            "url": _local_url(prices_path),
            "published_at": _date_to_timestamp(latest_date),
            "fetched_at": fetched_at,
            "hash": _stable_hash(source),
            "tickers": [ticker],
            "sectors": [],
            "themes": [],
            "summary": summary,
            "reliability": "high",
            "materiality": materiality,
            "used_in": [],
        })
    ]


def build_stock_evidence(root: Path, ticker: str) -> dict[str, Any]:
    normalized = ticker.strip().upper()
    stock_dir = root / "stocks" / normalized
    if not stock_dir.exists():
        raise ValueError(f"stock folder not found: {stock_dir}")

    fetched_at = _utc_now()
    records = [
        *_build_sec_fact_records(root, normalized, fetched_at),
        *_build_price_records(root, normalized, fetched_at),
    ]
    evidence_path = stock_dir / "evidence.jsonl"
    records_new = _append_unique_records(evidence_path, records)

    log = RunLog(stock_dir / "logs")
    log.append(
        "build_evidence",
        RunStatus.SUCCESS,
        tickers=[normalized],
        records_fetched=len(records),
        records_new=records_new,
    )

    return {
        "ticker": normalized,
        "evidence_path": str(evidence_path),
        "records_fetched": len(records),
        "records_new": records_new,
    }
