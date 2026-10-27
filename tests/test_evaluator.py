"""Unit tests for evaluate_stock.py (StockEvaluator)."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from evaluate_stock import StockEvaluator


def test_evaluator_discovery_and_period():
    evaluator = StockEvaluator("PAN")
    assert evaluator.ticker == "PAN"
    assert evaluator.sector == "mining"
    assert evaluator.period == "FY26"
    assert evaluator.s2_note_file.exists()


def test_evaluator_audit_existing_companies():
    for ticker in ["PAN", "SSK", "CGR", "SPP"]:
        evaluator = StockEvaluator(ticker)
        res = evaluator.audit()
        assert res["ticker"] == ticker
        assert res["status"] in ("PASSED", "WARNINGS_FOUND")
        assert "checks" in res
        assert "CHK-PRICE-SYNC" in res["checks"]
        assert "CHK-BANDS-MONO" in res["checks"]
        assert "CHK-SOTP-MATH" in res["checks"]
        assert "CHK-GUARDRAILS" in res["checks"]
        assert "CHK-TEXT-CLEAN" in res["checks"]
        assert res["checks"]["CHK-BANDS-MONO"]["passed"] is True
        assert res["checks"]["CHK-SOTP-MATH"]["passed"] is True
        assert res["checks"]["CHK-TEXT-CLEAN"]["passed"] is True


def test_evaluator_detects_non_monotonic_bands(tmp_path):
    evaluator = StockEvaluator("PAN")
    # Mock invalid note with non-monotonic bands
    mock_note = (
        "```json\n"
        "{\n"
        '  "ticker": "PAN",\n'
        '  "target_price_zar": 30.0,\n'
        '  "reference_price_zar": 25.0,\n'
        '  "rating_bands": {\n'
        '    "strong_buy_max_zar": 25.0,\n'
        '    "buy_max_zar": 20.0,\n'  # non-monotonic (buy < strong_buy)
        '    "hold_max_zar": 35.0,\n'
        '    "sell_max_zar": 40.0,\n'
        '    "strong_sell_above_zar": 40.0\n'
        "  }\n"
        "}\n"
        "```\n"
    )
    fake_note_path = tmp_path / "mock_note.md"
    fake_note_path.write_text(mock_note, encoding="utf-8")
    evaluator.s2_note_file = fake_note_path

    res = evaluator.audit()
    assert res["checks"]["CHK-BANDS-MONO"]["passed"] is False
    assert any("Non-monotonic" in d for d in res["checks"]["CHK-BANDS-MONO"]["details"])


def test_evaluator_detects_blend_math_hallucination(tmp_path):
    evaluator = StockEvaluator("PAN")
    mock_note = (
        "```json\n"
        "{\n"
        '  "ticker": "PAN",\n'
        '  "target_price_zar": 35.0,\n'
        '  "reference_price_zar": 25.0,\n'
        '  "rating_bands": {\n'
        '    "strong_buy_max_zar": 26.0,\n'
        '    "buy_max_zar": 30.0,\n'
        '    "hold_max_zar": 36.0,\n'
        '    "sell_max_zar": 41.0,\n'
        '    "strong_sell_above_zar": 41.0\n'
        "  }\n"
        "}\n"
        "```\n\n"
        "## 4. Sum-of-the-Parts\n"
        "Blended Target Price: (0.5 * 20.0) + (0.5 * 20.0) = ZAR 35.00.\n"  # 10 + 10 = 20, but claims 35
    )
    fake_note_path = tmp_path / "mock_note.md"
    fake_note_path.write_text(mock_note, encoding="utf-8")
    evaluator.s2_note_file = fake_note_path

    res = evaluator.audit()
    assert res["checks"]["CHK-SOTP-MATH"]["passed"] is False
    assert any("Blend formula hallucination" in d for d in res["checks"]["CHK-SOTP-MATH"]["details"])


def test_evaluator_detects_html_and_unparsed_placeholders(tmp_path):
    evaluator = StockEvaluator("PAN")
    mock_note = (
        "```json\n"
        "{\n"
        '  "ticker": "PAN",\n'
        '  "target_price_zar": 30.0,\n'
        '  "reference_price_zar": 25.0\n'
        "}\n"
        "```\n\n"
        "Some text with <br> illegal HTML and [+/-0.0]% unparsed placeholder."
    )
    fake_note_path = tmp_path / "mock_note.md"
    fake_note_path.write_text(mock_note, encoding="utf-8")
    evaluator.s2_note_file = fake_note_path

    res = evaluator.audit()
    assert res["checks"]["CHK-TEXT-CLEAN"]["passed"] is False
    assert any("Illegal HTML" in d for d in res["checks"]["CHK-TEXT-CLEAN"]["details"])
    assert any("Unparsed template placeholders" in d for d in res["checks"]["CHK-TEXT-CLEAN"]["details"])


def test_evaluator_format_markdown():
    evaluator = StockEvaluator("SSK")
    res = evaluator.audit()
    md = evaluator.format_markdown(res)
    assert "### SSK — Institutional Valuation Scorecard" in md
    assert "CHK-PRICE-SYNC" in md
    assert "CHK-BANDS-MONO" in md
    assert "CHK-SOTP-MATH" in md
    assert "CHK-GUARDRAILS" in md
    assert "CHK-TEXT-CLEAN" in md
