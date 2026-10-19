"""Unit tests for the 2-Year Analyst Forecast & Valuation Engine."""

from __future__ import annotations

import pytest
from forecast.data_loader import load_fy26_baseline, FY26Baseline
from forecast.macro_deck import MacroDeck, Scenario
from forecast.two_year_model import TwoYearModel, ConsolidatedForecast
from forecast.multiples_valuation import ValuationEngine
from forecast.report import generate_analyst_report
import companies.PAN.models.data_loader as pan_loader
import companies.PAN.models.run as pan_run



def test_baseline_data_loader():
    base = load_fy26_baseline()
    assert isinstance(base, FY26Baseline)
    assert base.gold_sold_total_oz == 272_373.0
    assert base.realized_gold_price_usd_per_oz == 4_235.0
    assert base.group_adjusted_ebitda_usdm == 609.431
    assert base.net_debt_usdm == pytest.approx(-185.605, rel=1e-3)
    assert base.shares_in_issue_diluted_m == 2_027.3
    assert len(base.assets) == 6
    assert "mtr" in base.assets
    assert "elikhulu" in base.assets
    assert "tennant" in base.assets


def test_macro_deck_scenarios():
    base_deck = MacroDeck.create(Scenario.BASE)
    assert base_deck.fy27.gold_price_usd_per_oz == 5_050.0
    assert base_deck.fy28.gold_price_usd_per_oz == 5_750.0
    assert base_deck.fy27.cash_tax_rate == 0.208
    assert base_deck.fy28.cash_tax_rate == 0.275

    bear_deck = MacroDeck.create(Scenario.BEAR)
    assert bear_deck.fy27.gold_price_usd_per_oz == 3_750.0

    bull_deck = MacroDeck.create(Scenario.BULL)
    assert bull_deck.fy28.gold_price_usd_per_oz == 7_000.0


def test_two_year_model_footings():
    model = TwoYearModel()
    forecast = model.run()

    assert isinstance(forecast, ConsolidatedForecast)
    assert forecast.scenario == Scenario.BASE

    for yr in [forecast.fy27, forecast.fy28]:
        # Production volume check
        assert yr.gold_sold_oz >= 300_000.0

        # P&L Footings
        calc_gp = round(yr.revenue_usdm - yr.cost_of_production_usdm - yr.royalties_usdm, 1)
        assert yr.gross_profit_usdm == pytest.approx(calc_gp, abs=0.2)

        calc_ebitda = round(yr.gross_profit_usdm - yr.corporate_overhead_usdm - yr.other_divisions_usdm, 1)
        assert yr.adjusted_ebitda_usdm == pytest.approx(calc_ebitda, abs=0.2)

        calc_ebit = round(yr.adjusted_ebitda_usdm - yr.depreciation_amortisation_usdm, 1)
        assert yr.operating_profit_ebit_usdm == pytest.approx(calc_ebit, abs=0.2)

        calc_pbt = round(yr.operating_profit_ebit_usdm + yr.net_finance_income_usdm, 1)
        assert yr.profit_before_tax_usdm == pytest.approx(calc_pbt, abs=0.2)

        calc_pat = round(yr.profit_before_tax_usdm - yr.income_tax_expense_usdm, 1)
        assert yr.profit_after_tax_pat_usdm == pytest.approx(calc_pat, abs=0.2)

        # Capex & Cash Flow
        assert yr.total_capex_usdm == pytest.approx(yr.sustaining_capex_usdm + yr.expansion_capex_usdm, abs=0.1)
        assert yr.free_cash_flow_to_equity_usdm > 500.0  # Massive cash generation
        assert yr.closing_net_cash_usdm > yr.free_cash_flow_to_equity_usdm * 0.5


def test_valuation_multiples():
    model = TwoYearModel()
    forecast = model.run()
    engine = ValuationEngine(forecast)
    multiples = engine.evaluate(target_ev_ebitda=3.5)

    assert multiples.fy26_actual.ev_to_ebitda > 0
    assert multiples.fy27_forward.ev_to_ebitda < multiples.fy26_actual.ev_to_ebitda
    assert multiples.fy28_forward.ev_to_ebitda < multiples.fy27_forward.ev_to_ebitda
    assert multiples.target_price_12m_zar > 25.0
    assert multiples.target_price_12m_gb_pence > 100.0
    assert multiples.implied_upside_pct > 0

    grid = engine.sensitivity_grid(currency="ZAR")
    assert len(grid) == 5
    assert "$5050/oz" in grid
    assert "R16.5" in grid["$5050/oz"]
    assert grid["$5050/oz"]["R16.5"] == pytest.approx(32.51, abs=0.5)


def test_report_generation():
    report = generate_analyst_report(Scenario.BASE)
    assert "# Institutional 2-Year Analyst Forecast Report" in report
    assert "Mogale Tailings Retreatment" in report
    assert "EV / Adjusted EBITDA" in report


def test_pan_company_models():
    base = pan_loader.load_fy26_baseline()
    assert base.gold_sold_total_oz == 272_373.0
    report = pan_run.generate_analyst_report()
    assert "# Institutional 2-Year Analyst Forecast Report" in report
    assert "Mogale Tailings Retreatment" in report


def test_interactive_notebooks(tmp_path):
    import json
    from pathlib import Path
    from new_company import generate_company_notebook

    # 1. PAN Sandbox exists and is valid JSON
    pan_nb = Path("companies/mining/PAN/models/pan_sandbox.ipynb")
    assert pan_nb.exists()
    with open(pan_nb, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["nbformat"] == 4
    assert len(data["cells"]) >= 6

    # 2. Scaffolding tool generates valid sandboxes for mining and retail
    out_nb = tmp_path / "test_sandbox.ipynb"
    generate_company_notebook("TEST", "Test Mining Ltd", "mining", out_nb)
    assert out_nb.exists()
    with open(out_nb, "r", encoding="utf-8") as f:
        test_data = json.load(f)
    assert test_data["nbformat"] == 4
    assert len(test_data["cells"]) >= 4

    out_retail_nb = tmp_path / "retail_sandbox.ipynb"
    generate_company_notebook("LEW", "Lewis Group Ltd", "retail", out_retail_nb)
    assert out_retail_nb.exists()
    with open(out_retail_nb, "r", encoding="utf-8") as f:
        retail_data = json.load(f)
    assert retail_data["nbformat"] == 4
    assert "MERCHANDISE_GROWTH_PCT" in json.dumps(retail_data)

