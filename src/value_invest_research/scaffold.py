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
