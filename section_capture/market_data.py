"""Market Data integration for JSE equities via yfinance."""
from __future__ import annotations

from datetime import datetime, timezone
import logging
from pathlib import Path
from typing import Any

from PySide6.QtCore import QObject, QThread, Signal
import yfinance as yf

from section_capture.db import connect_db, resolve_db_path

logger = logging.getLogger(__name__)


def to_jse_symbol(ticker: str) -> str:
    """Normalizes a company ticker to a Yahoo Finance JSE symbol (<TICKER>.JO)."""
    t = ticker.strip().upper()
    if t.endswith(".JO"):
        return t
    return f"{t}.JO"


def fetch_jse_quote(ticker: str) -> dict[str, Any] | None:
    """Fetches the latest live market quote for a JSE equity symbol using yfinance."""
    sym = to_jse_symbol(ticker)
    clean_ticker = ticker.strip().upper().removesuffix(".JO")
    try:
        t = yf.Ticker(sym)
        fast = t.fast_info
        raw_price = getattr(fast, "last_price", None)
        prev_close = getattr(fast, "previous_close", None)
        currency = getattr(fast, "currency", None) or "ZAc"

        if raw_price is None:
            hist = t.history(period="1d")
            if not hist.empty:
                raw_price = float(hist["Close"].iloc[-1])

        if raw_price is None:
            return None

        # JSE prices on Yahoo Finance are quoted in South African Cents (ZAc)
        if currency.upper() == "ZAC":
            price_zar = raw_price / 100.0
            prev_close_zar = (prev_close / 100.0) if prev_close else None
        else:
            price_zar = raw_price
            prev_close_zar = prev_close

        change_pct = (
            ((price_zar - prev_close_zar) / prev_close_zar * 100.0)
            if (price_zar is not None and prev_close_zar)
            else None
        )

        return {
            "ticker": clean_ticker,
            "symbol": sym,
            "price_zar": round(price_zar, 2),
            "prev_close_zar": round(prev_close_zar, 2) if prev_close_zar is not None else None,
            "raw_price": raw_price,
            "currency": currency,
            "change_pct": round(change_pct, 2) if change_pct is not None else None,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        logger.warning(f"Error fetching quote for {sym}: {exc}")
        return None


def fetch_all_jse_quotes(tickers: list[str]) -> dict[str, dict[str, Any]]:
    """Batch-fetches quotes for multiple JSE equities."""
    quotes: dict[str, dict[str, Any]] = {}
    if not tickers:
        return quotes

    clean_tickers = [t.strip().upper().removesuffix(".JO") for t in tickers if t]
    symbols = [to_jse_symbol(t) for t in clean_tickers]

    try:
        multi = yf.Tickers(" ".join(symbols))
        for t_clean, sym in zip(clean_tickers, symbols):
            try:
                t_obj = multi.tickers.get(sym)
                if not t_obj:
                    continue
                fast = t_obj.fast_info
                raw_price = getattr(fast, "last_price", None)
                prev_close = getattr(fast, "previous_close", None)
                currency = getattr(fast, "currency", None) or "ZAc"

                if raw_price is None:
                    single = fetch_jse_quote(t_clean)
                    if single:
                        quotes[t_clean] = single
                    continue

                if currency.upper() == "ZAC":
                    price_zar = raw_price / 100.0
                    prev_close_zar = (prev_close / 100.0) if prev_close else None
                else:
                    price_zar = raw_price
                    prev_close_zar = prev_close

                change_pct = (
                    ((price_zar - prev_close_zar) / prev_close_zar * 100.0)
                    if (price_zar is not None and prev_close_zar)
                    else None
                )

                quotes[t_clean] = {
                    "ticker": t_clean,
                    "symbol": sym,
                    "price_zar": round(price_zar, 2),
                    "prev_close_zar": round(prev_close_zar, 2) if prev_close_zar is not None else None,
                    "raw_price": raw_price,
                    "currency": currency,
                    "change_pct": round(change_pct, 2) if change_pct is not None else None,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
            except Exception as exc:
                logger.warning(f"Error extracting quote for {sym}: {exc}")
    except Exception as exc:
        logger.warning(f"Batch fetch error for {symbols}: {exc}")
        for t_clean in clean_tickers:
            q = fetch_jse_quote(t_clean)
            if q:
                quotes[t_clean] = q

    return quotes


def save_market_quotes(quotes: dict[str, dict[str, Any]], db_path: Path | str | None = None) -> None:
    """Persists quotes into the market_quotes table in SQLite."""
    if not quotes:
        return
    resolved = resolve_db_path(db_path)
    with connect_db(resolved) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS market_quotes (
                ticker TEXT PRIMARY KEY,
                price_zar REAL NOT NULL,
                prev_close_zar REAL,
                currency TEXT NOT NULL,
                raw_price REAL NOT NULL,
                change_pct REAL,
                updated_at TEXT NOT NULL
            )
            """
        )
        for ticker, q in quotes.items():
            if q.get("price_zar") is not None:
                conn.execute(
                    """
                    INSERT INTO market_quotes (ticker, price_zar, prev_close_zar, currency, raw_price, change_pct, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(ticker) DO UPDATE SET
                        price_zar = excluded.price_zar,
                        prev_close_zar = excluded.prev_close_zar,
                        currency = excluded.currency,
                        raw_price = excluded.raw_price,
                        change_pct = excluded.change_pct,
                        updated_at = excluded.updated_at
                    """,
                    (
                        ticker.upper(),
                        q["price_zar"],
                        q.get("prev_close_zar"),
                        q.get("currency", "ZAc"),
                        q.get("raw_price", q["price_zar"]),
                        q.get("change_pct"),
                        q.get("updated_at", datetime.now(timezone.utc).isoformat()),
                    ),
                )
        conn.commit()


def load_market_quotes(
    tickers: list[str] | None = None,
    db_path: Path | str | None = None,
) -> dict[str, dict[str, Any]]:
    """Loads cached quotes from SQLite."""
    resolved = resolve_db_path(db_path)
    if not resolved.exists():
        return {}
    with connect_db(resolved) as conn:
        cur = conn.cursor()
        table_exists = cur.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='market_quotes'"
        ).fetchone()
        if not table_exists:
            return {}
        if tickers:
            placeholders = ",".join("?" for _ in tickers)
            rows = cur.execute(
                f"SELECT ticker, price_zar, prev_close_zar, currency, raw_price, change_pct, updated_at "
                f"FROM market_quotes WHERE ticker IN ({placeholders})",
                [t.upper() for t in tickers],
            ).fetchall()
        else:
            rows = cur.execute(
                "SELECT ticker, price_zar, prev_close_zar, currency, raw_price, change_pct, updated_at FROM market_quotes"
            ).fetchall()

        return {
            r["ticker"]: {
                "ticker": r["ticker"],
                "symbol": to_jse_symbol(r["ticker"]),
                "price_zar": r["price_zar"],
                "prev_close_zar": r["prev_close_zar"],
                "currency": r["currency"],
                "raw_price": r["raw_price"],
                "change_pct": r["change_pct"],
                "updated_at": r["updated_at"],
            }
            for r in rows
        }


class MarketQuoteWorker(QThread):
    """Asynchronous worker to fetch market quotes via yfinance without blocking the UI."""

    quote_received = Signal(str, dict)
    all_quotes_ready = Signal(dict)
    fetch_failed = Signal(str)

    def __init__(self, tickers: list[str], db_path: Path | str | None = None, parent: QObject | None = None):
        super().__init__(parent)
        self.tickers = tickers
        self.db_path = db_path

    def run(self):
        try:
            quotes = fetch_all_jse_quotes(self.tickers)
            if quotes:
                save_market_quotes(quotes, self.db_path)
                for t, q in quotes.items():
                    self.quote_received.emit(t, q)
                self.all_quotes_ready.emit(quotes)
            else:
                self.all_quotes_ready.emit({})
        except Exception as exc:
            logger.exception("Error in MarketQuoteWorker")
            self.fetch_failed.emit(str(exc))
