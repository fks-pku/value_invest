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

    sec_parser = subparsers.add_parser("ingest-sec", help="Fetch SEC EDGAR data for a ticker")
    sec_parser.add_argument("ticker")
    sec_parser.add_argument("--user-agent", default="value-invest-research/0.1.0 research@example.com")
    sec_parser.add_argument("--include-facts", action="store_true", default=True)
    sec_parser.add_argument("--no-facts", dest="include_facts", action="store_false")

    prices_parser = subparsers.add_parser("ingest-prices", help="Fetch price history for a ticker")
    prices_parser.add_argument("ticker")
    prices_parser.add_argument("--period", default="1y")

    memo_parser = subparsers.add_parser("update-memo", help="Run LLM memo update for a ticker")
    memo_parser.add_argument("ticker")
    memo_parser.add_argument("--api-key", default=None)
    memo_parser.add_argument("--base-url", default="https://api.z.ai/api/coding/paas/v4")
    memo_parser.add_argument("--model", default="glm-5.1")

    event_research_parser = subparsers.add_parser("research-event", help="Run LLM event research")
    event_research_parser.add_argument("event_date")
    event_research_parser.add_argument("event_name")
    event_research_parser.add_argument("--description", required=True)
    event_research_parser.add_argument("--playbook", default=None)
    event_research_parser.add_argument("--api-key", default=None)
    event_research_parser.add_argument("--base-url", default="https://api.z.ai/api/coding/paas/v4")
    event_research_parser.add_argument("--model", default="glm-5.1")

    sector_research_parser = subparsers.add_parser("research-sector", help="Run LLM sector or theme research")
    sector_research_parser.add_argument("sector_name")
    sector_research_parser.add_argument("--type", choices=["sector", "theme"], default="sector")
    sector_research_parser.add_argument("--focus", required=True)
    sector_research_parser.add_argument("--tickers", nargs="*", default=None)
    sector_research_parser.add_argument("--api-key", default=None)
    sector_research_parser.add_argument("--base-url", default="https://api.z.ai/api/coding/paas/v4")
    sector_research_parser.add_argument("--model", default="glm-5.1")

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
        if args.command == "update-memo":
            return run_memo_update(root, args.ticker, args.api_key, args.base_url, args.model)
        if args.command == "research-event":
            return run_event_research_cmd(root, args)
        if args.command == "research-sector":
            return run_sector_research_cmd(root, args)
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
    client.fetch_submissions(root, normalized, cik)
    print(f"SEC submissions fetched for {normalized} (CIK {cik})")

    if include_facts:
        client.fetch_company_facts(root, normalized, cik)
        print(f"SEC company facts fetched for {normalized}")

    return 0


def run_price_ingest(root: Path, ticker: str, period: str) -> int:
    from value_invest_research.ingest_prices import fetch_price_history

    normalized = ticker.strip().upper()
    init_stock(root, normalized)
    fetch_price_history(root, normalized, period=period)
    print(f"Price history fetched for {normalized}")
    return 0


def run_memo_update(root: Path, ticker: str, api_key: str | None, base_url: str, model: str) -> int:
    import os

    from value_invest_research.llm import LlmClient, LlmConfig
    from value_invest_research.memo_updater import MemoUpdater

    key = api_key or os.environ.get("LLM_API_KEY", "")
    if not key:
        print("error: API key required (set LLM_API_KEY or pass --api-key)", file=sys.stderr)
        return 2

    config = LlmConfig(api_key=key, base_url=base_url, model=model)
    client = LlmClient(config)
    updater = MemoUpdater(client)

    result = updater.update_stock_memo(root, ticker)
    print(f"Memo update proposal saved: {result['proposal_path']}")
    print(f"Ticker: {result['ticker']}, Length: {result['response_length']} chars")
    return 0


def _get_llm_client(api_key: str | None, base_url: str, model: str) -> "LlmClient":
    import os

    from value_invest_research.llm import LlmClient, LlmConfig

    key = api_key or os.environ.get("LLM_API_KEY", "")
    if not key:
        print("error: API key required (set LLM_API_KEY or pass --api-key)", file=sys.stderr)
        raise SystemExit(2)
    return LlmClient(LlmConfig(api_key=key, base_url=base_url, model=model))


def run_event_research_cmd(root: Path, args) -> int:
    from value_invest_research.event_researcher import EventResearcher

    client = _get_llm_client(args.api_key, args.base_url, args.model)
    researcher = EventResearcher(client)

    result = researcher.run_event_research(
        root, args.event_date, args.event_name,
        event_description=args.description,
        playbook_name=args.playbook,
    )
    print(f"Event research saved: {result['analysis_path']}")
    print(f"Event: {result['event_name']}, Dir: {result['event_dir']}, Length: {result['response_length']} chars")
    return 0


def run_sector_research_cmd(root: Path, args) -> int:
    from value_invest_research.sector_researcher import SectorResearcher

    client = _get_llm_client(args.api_key, args.base_url, args.model)
    researcher = SectorResearcher(client)

    result = researcher.run_sector_research(
        root, args.sector_name,
        sector_type=args.type,
        research_focus=args.focus,
        tickers_to_include=args.tickers,
    )
    print(f"Sector research saved: {result['analysis_path']}")
    print(f"Sector: {result['sector_name']} ({result['sector_type']}), Dir: {result['sector_dir']}, Length: {result['response_length']} chars")
    return 0
