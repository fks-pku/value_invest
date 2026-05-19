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
        with path.open("w", encoding="utf-8", newline="\n") as file:
            file.write(content)


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

## 0. Current View
- View: Needs Review
- Confidence: Low
- Last Updated:
- Foundation Status: Not Started
- Company Foundation Summary:
- FengHe Message-Flow Summary:
- Most Important Uncertainty:

## 1. Company Foundation Analysis

### 1.1 Source And Origin
- Founding context:
- Original problem solved:
- Early wedge:
- Company DNA:

### 1.2 Company History
- Business milestones:
- Governance milestones:
- Financing and capital-allocation milestones:
- M&A or restructuring history:

### 1.3 Current Business
- Business model:
- Segments:
- Customers:
- Demand drivers:
- Pricing:
- Revenue quality:
- Margin structure:
- Cash conversion:

### 1.4 Value Chain Position
- Suppliers:
- Channels:
- Customers:
- Substitutes:
- Bargaining power:
- Where economics are captured or lost:

### 1.5 Competitive Landscape
- Market structure:
- Key peers:
- Ranking or share:
- Differentiation:
- Barriers to entry:
- Competition intensity:

### 1.6 Strategy Analysis
- Mission:
- Corporate strategy:
- Competitive strategy:
- Functional strategy:
- Resource allocation:

### 1.7 Organization, Culture, And Governance
- Leadership:
- Incentives:
- Ownership and control:
- Board or governance quality:
- Culture and execution system:

### 1.8 Risk Sweep
- Business risks:
- Financial risks:
- Accounting risks:
- Legal and regulatory risks:
- Customer or supplier concentration:
- Technology or disruption risks:
- Capital-allocation risks:
- Governance risks:
- Valuation risks:

## 2. FengHe Message-Flow Analysis

### 2.1 3C: Cycle, Change, Certainty
- Cycle:
- Change:
- Certainty:

### 2.2 3D Price Drivers
- D1 ROE / intrinsic value:
- D2 marginal change / catalyst:
- D3 sentiment / valuation:
- Dominant driver:

### 2.3 5M Change Map
- M1 market size:
- M2 market share:
- M3 margin:
- M4 model:
- M5 management:
- Key value driver:
- Key defect risk:

### 2.4 3T Time Frame
- T1 0-3 months:
- T2 3-15 months:
- T3 15+ months:
- Active time frame:

### 2.5 Certainty, Risk, And Disconfirming Evidence
- Evidence that supports certainty:
- Thesis breakers:
- Disconfirming tests:

## 3. Valuation And Risk/Reward
- Normalized earnings or FCF:
- Conservative assumptions:
- Downside case:
- Base case:
- Upside case:
- Margin of safety:

## 4. Evidence Log

## 5. Human Review Questions
"""


def event_brief_template(event_date: str, event_name: str) -> str:
    return f"""# {event_name} Event Brief

- Date Opened: {event_date}
- Status: Active Research
- Goal: Identify candidates for foundation-first stock-level research.

## Confirmed Facts

## Unconfirmed Claims

## FengHe 3C Event Read
- Cycle context:
- Change:
- Certainty:

## Transmission Questions

## Source Log
"""


def transmission_map_template(event_name: str) -> str:
    return f"""# {event_name} Transmission Map

## Primary Shock

## FengHe 3C
- Cycle:
- Change:
- Certainty:

## Transmission Channels

## Affected Sectors

## Candidate Company Mechanisms

## Dominant 3D Drivers

## Disconfirming Paths
"""


def candidate_screen_template(event_name: str) -> str:
    return f"""# {event_name} Candidate Screen

## Tier 1: Immediate Deep Research

## Tier 2: Watchlist

## Tier 3: Evidence Too Weak

## Negative Watch

## Candidate Fields
- Ticker:
- FengHe message-flow 3C:
- Dominant 3D driver:
- Strongest 5M factor:
- Weakest 5M factor:
- 3T time frame:
- Disconfirming tests:
"""
