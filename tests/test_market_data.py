"""Unit tests for JSE market data integration via yfinance."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from section_capture.db import connect_db, get_analyzed_stocks, upsert_report
from section_capture.market_data import (
    MarketQuoteWorker,
    fetch_all_jse_quotes,
    fetch_jse_quote,
    load_market_quotes,
    save_market_quotes,
    to_jse_symbol,
)


def test_to_jse_symbol():
    assert to_jse_symbol("PAN") == "PAN.JO"
    assert to_jse_symbol("LEW.JO") == "LEW.JO"
    assert to_jse_symbol("cgr") == "CGR.JO"
    assert to_jse_symbol(" ORN ") == "ORN.JO"
    assert to_jse_symbol("ioc.jo") == "IOC.JO"


def test_fetch_jse_quote_zac_conversion():
    mock_fast_info = MagicMock()
    mock_fast_info.last_price = 2410.0
    mock_fast_info.previous_close = 2400.0
    mock_fast_info.currency = "ZAc"

    mock_ticker_obj = MagicMock()
    mock_ticker_obj.fast_info = mock_fast_info

    with patch("yfinance.Ticker", return_value=mock_ticker_obj):
        q = fetch_jse_quote("PAN")
        assert q is not None
        assert q["ticker"] == "PAN"
        assert q["symbol"] == "PAN.JO"
        assert q["price_zar"] == 24.10
        assert q["prev_close_zar"] == 24.00
        assert q["currency"] == "ZAc"
        assert q["change_pct"] == pytest.approx(0.42, 0.01)


def test_fetch_jse_quote_zar_currency():
    mock_fast_info = MagicMock()
    mock_fast_info.last_price = 45.50
    mock_fast_info.previous_close = 45.00
    mock_fast_info.currency = "ZAR"

    mock_ticker_obj = MagicMock()
    mock_ticker_obj.fast_info = mock_fast_info

    with patch("yfinance.Ticker", return_value=mock_ticker_obj):
        q = fetch_jse_quote("LEW")
        assert q is not None
        assert q["price_zar"] == 45.50
        assert q["prev_close_zar"] == 45.00
        assert q["currency"] == "ZAR"
        assert q["change_pct"] == pytest.approx(1.11, 0.01)


def test_market_quotes_persistence(tmp_path):
    test_db = tmp_path / "test_market.sqlite"
    with connect_db(test_db) as conn:
        pass

    quotes = {
        "PAN": {
            "ticker": "PAN",
            "symbol": "PAN.JO",
            "price_zar": 24.10,
            "prev_close_zar": 24.00,
            "currency": "ZAc",
            "raw_price": 2410.0,
            "change_pct": 0.42,
            "updated_at": "2026-10-23T16:00:00Z",
        },
        "LEW": {
            "ticker": "LEW",
            "symbol": "LEW.JO",
            "price_zar": 87.03,
            "prev_close_zar": 90.07,
            "currency": "ZAc",
            "raw_price": 8703.0,
            "change_pct": -3.38,
            "updated_at": "2026-10-23T16:00:00Z",
        },
    }

    save_market_quotes(quotes, db_path=test_db)

    loaded = load_market_quotes(db_path=test_db)
    assert len(loaded) == 2
    assert loaded["PAN"]["price_zar"] == 24.10
    assert loaded["PAN"]["currency"] == "ZAc"
    assert loaded["LEW"]["price_zar"] == 87.03
    assert loaded["LEW"]["change_pct"] == -3.38

    # Filtered load
    subset = load_market_quotes(tickers=["PAN"], db_path=test_db)
    assert len(subset) == 1
    assert "PAN" in subset


def test_get_analyzed_stocks_includes_live_quotes(tmp_path):
    test_db = tmp_path / "test_stocks.sqlite"
    with connect_db(test_db) as conn:
        pass

    # Upsert report and set target price R30.00
    upsert_report(
        sha256="sha_pan_123",
        filename="PAN_annual_report.pdf",
        original_path="companies/mining/PAN/sources/PAN_annual_report.pdf",
        db_path=test_db,
    )
    with connect_db(test_db) as conn:
        conn.execute(
            "UPDATE reports SET target_price_zar = 30.00, reference_price_zar = 20.00, recommendation = 'BUY' WHERE sha256 = 'sha_pan_123'"
        )

    # Save live market quote R24.00
    save_market_quotes(
        {
            "PAN": {
                "ticker": "PAN",
                "price_zar": 24.00,
                "prev_close_zar": 23.50,
                "currency": "ZAc",
                "raw_price": 2400.0,
                "change_pct": 2.13,
                "updated_at": "2026-10-23T17:00:00Z",
            }
        },
        db_path=test_db,
    )

    stocks = get_analyzed_stocks(test_db)
    assert len(stocks) == 1
    s = stocks[0]
    assert s["ticker"] == "PAN"
    assert s["reference_price_zar"] == 20.00
    assert s["target_price_zar"] == 30.00
    assert s["live_price_zar"] == 24.00
    assert s["live_price_change_pct"] == 2.13
    # Live upside = (30.00 - 24.00) / 24.00 * 100% = +25.0%
    assert s["live_upside_pct"] == 25.0


def test_market_quote_worker_signals(tmp_path, qapp):
    test_db = tmp_path / "test_worker.sqlite"
    with connect_db(test_db) as conn:
        pass

    mock_quotes = {
        "PAN": {
            "ticker": "PAN",
            "symbol": "PAN.JO",
            "price_zar": 24.10,
            "prev_close_zar": 24.00,
            "currency": "ZAc",
            "raw_price": 2410.0,
            "change_pct": 0.42,
            "updated_at": "2026-10-23T16:00:00Z",
        }
    }

    worker = MarketQuoteWorker(tickers=["PAN"], db_path=test_db)

    received = {}
    ready = {}

    worker.quote_received.connect(lambda t, q: received.update({t: q}))
    worker.all_quotes_ready.connect(lambda d: ready.update(d))

    with patch("section_capture.market_data.fetch_all_jse_quotes", return_value=mock_quotes):
        worker.run()

    assert "PAN" in received
    assert received["PAN"]["price_zar"] == 24.10
    assert "PAN" in ready

    # Verify saved in test_db
    loaded = load_market_quotes(db_path=test_db)
    assert "PAN" in loaded


def test_portfolio_view_columns(tmp_path, qapp):
    from section_capture.portfolio_view import PortfolioView

    test_db = tmp_path / "test_pv.sqlite"
    with connect_db(test_db) as conn:
        pass

    pv = PortfolioView(db_path=test_db)
    try:
        assert pv.table.columnCount() == 11
        headers = [pv.table.horizontalHeaderItem(i).text() for i in range(pv.table.columnCount())]
        assert "Latest JSE Price" in headers
        assert "Live Upside" in headers
        assert "Note Ref Price" not in headers
        assert "Note Upside" not in headers
        assert "12M Target" in headers
        assert hasattr(pv, "fetch_quotes_btn")
    finally:
        pv.deleteLater()
