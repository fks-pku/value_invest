from __future__ import annotations

from pathlib import Path

try:
    import yfinance as yf
except ModuleNotFoundError:
    class _MissingYFinance:
        def Ticker(self, ticker: str):
            raise RuntimeError("yfinance package is required for price ingestion; install value-invest-research[ingest]")

    yf = _MissingYFinance()

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
