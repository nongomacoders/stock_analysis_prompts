"""Tests reconciling PAN Primary Financial Statements (Section S006, physical pages 17-18).

Governed by CHARTER covenants:
  - Covenant 1: Never replace a printed source figure. Mismatches are recorded data.
  - Covenant 2: All arithmetic executes in code, never asserted in prose.
  - Covenant 3: Every cell carries physical page, document hash, and extraction commit.
  - Fixture covenant: ground truth scoring fixtures are never read by test code.
"""
from __future__ import annotations

import pathlib
import pytest
from decimal import Decimal


def _get_val(report_db, page: int, region: str, label: str, fy: str) -> Decimal:
    """Helper to query a single cell as Decimal."""
    row = report_db.execute(
        "SELECT value_num FROM cells WHERE physical_page=? AND table_region=? AND row_label=? AND fiscal_year=?",
        (page, region, label, fy)
    ).fetchone()
    assert row is not None, f"Missing cell: p.{page} {region} '{label}' {fy}"
    assert row[0] is not None, f"Cell is nil/None: p.{page} {region} '{label}' {fy}"
    return Decimal(str(row[0]))


# ------------------------------------------------------------- 1. Balance Sheet Checks
@pytest.mark.parametrize("fy", ["FY26", "FY25"])
def test_balance_sheet_assets_subtotals(report_db, fy):
    """Non-current assets + Current assets == Total assets."""
    nc = _get_val(report_db, 17, "primary_balance_sheet_assets", "Total non-current assets", fy)
    ca = _get_val(report_db, 17, "primary_balance_sheet_assets", "Total current assets", fy)
    ta = _get_val(report_db, 17, "primary_balance_sheet_assets", "Total assets", fy)
    assert nc + ca == ta


@pytest.mark.parametrize("fy", ["FY26", "FY25"])
def test_balance_sheet_equity_liabilities_subtotals(report_db, fy):
    """Total equity + Total non-current liabilities + Total current liabilities == Total equity and liabilities."""
    eq = _get_val(report_db, 17, "primary_balance_sheet_equity_liab", "Total equity", fy)
    ncl = _get_val(report_db, 17, "primary_balance_sheet_equity_liab", "Total non-current liabilities", fy)
    cl = _get_val(report_db, 17, "primary_balance_sheet_equity_liab", "Total current liabilities", fy)
    tot = _get_val(report_db, 17, "primary_balance_sheet_equity_liab", "Total equity and liabilities", fy)
    assert eq + ncl + cl == tot


@pytest.mark.parametrize("fy", ["FY26", "FY25"])
def test_balance_sheet_fundamental_identity(report_db, fy):
    """Fundamental accounting equation: Total assets == Total equity and liabilities."""
    ta = _get_val(report_db, 17, "primary_balance_sheet_assets", "Total assets", fy)
    tel = _get_val(report_db, 17, "primary_balance_sheet_equity_liab", "Total equity and liabilities", fy)
    assert ta == tel
    if fy == "FY26":
        assert ta == Decimal("1608075")
    else:
        assert ta == Decimal("1004509")


# -------------------------------------------------------- 2. Income Statement Checks
@pytest.mark.parametrize("fy", ["FY26", "FY25"])
def test_income_statement_gross_profit(report_db, fy):
    """Revenue + Cost of production (negative) == Gross profit."""
    rev = _get_val(report_db, 18, "primary_income_statement", "Revenue", fy)
    cop = _get_val(report_db, 18, "primary_income_statement", "Cost of production", fy)
    gp = _get_val(report_db, 18, "primary_income_statement", "Gross profit", fy)
    assert rev + cop == gp


@pytest.mark.parametrize("fy", ["FY26", "FY25"])
def test_income_statement_profit_before_tax(report_db, fy):
    """Profit before finance + Finance income + Finance costs (negative) == Profit before tax."""
    pbf = _get_val(report_db, 18, "primary_income_statement", "Profit before finance income and finance costs", fy)
    fi = _get_val(report_db, 18, "primary_income_statement", "Finance income", fy)
    fc = _get_val(report_db, 18, "primary_income_statement", "Finance costs", fy)
    pbt = _get_val(report_db, 18, "primary_income_statement", "Profit before tax", fy)
    assert pbf + fi + fc == pbt


@pytest.mark.parametrize("fy", ["FY26", "FY25"])
def test_income_statement_profit_for_period(report_db, fy):
    """Profit before tax + Income tax expense (negative) == Profit for the period."""
    pbt = _get_val(report_db, 18, "primary_income_statement", "Profit before tax", fy)
    tax = _get_val(report_db, 18, "primary_income_statement", "Income tax expense", fy)
    prof = _get_val(report_db, 18, "primary_income_statement", "Profit for the period", fy)
    assert pbt + tax == prof


# ----------------------------------------------------------- 3. Cash Flow Checks
@pytest.mark.parametrize("fy", ["FY26", "FY25"])
def test_cash_flows_net_change_in_cash(report_db, fy):
    """Operating + Investing + Financing cash flows == Net increase in cash and cash equivalents."""
    cfo = _get_val(report_db, 18, "primary_cash_flows", "Net cash generated from operating activities", fy)
    cfi = _get_val(report_db, 18, "primary_cash_flows", "Net cash used in investing activities", fy)
    cff = _get_val(report_db, 18, "primary_cash_flows", "Net cash (used in)/from financing activities", fy)
    net_inc = _get_val(report_db, 18, "primary_cash_flows", "Net increase in cash and cash equivalents", fy)
    assert cfo + cfi + cff == net_inc


@pytest.mark.parametrize("fy", ["FY26", "FY25"])
def test_cash_flows_roll_forward(report_db, fy):
    """Opening cash (1 July) + Net increase + FX changes == Closing cash (30 June)."""
    open_cash = _get_val(report_db, 18, "primary_cash_flows", "Cash and cash equivalents as at 1 July", fy)
    net_inc = _get_val(report_db, 18, "primary_cash_flows", "Net increase in cash and cash equivalents", fy)
    fx = _get_val(report_db, 18, "primary_cash_flows", "Effect of foreign exchange rate changes", fy)
    close_cash = _get_val(report_db, 18, "primary_cash_flows", "Cash and cash equivalents as at 30 June", fy)
    assert open_cash + net_inc + fx == close_cash


# --------------------------------------------------------- 4. Cross-Statement Ties
@pytest.mark.parametrize("fy", ["FY26", "FY25"])
def test_cross_statement_cash_tie(report_db, fy):
    """Balance Sheet Cash (p.17) == Cash Flow Statement Closing Cash (p.18)."""
    bs_cash = _get_val(report_db, 17, "primary_balance_sheet_assets", "Cash and cash equivalents", fy)
    cf_cash = _get_val(report_db, 18, "primary_cash_flows", "Cash and cash equivalents as at 30 June", fy)
    assert bs_cash == cf_cash
    if fy == "FY26":
        assert bs_cash == Decimal("108312")
    else:
        assert bs_cash == Decimal("49532")


def test_cross_section_revenue_consistency(report_db):
    """Section S006 IFRS Revenue vs Section D009 segmental revenue.

    D009 p.50 prints Revenue in ZAR million: 17,249.1 ZARm.
    Primary p.18 prints Revenue in US$ thousand: 1,156,451 US$k ($1,156.451m).
    Average exchange rate on p.50 is 16.90 US$/ZAR.
    Implied IFRS revenue in ZARm is 1,156.451 * 16.90 = 19,544.0 ZARm.
    The difference (19,544.0 - 17,249.1 = 2,294.9 ZARm) connects to open ledger question
    Q-a0b503d7ac044eee and reflects non-mining / group consolidation items.
    """
    ifrs_rev_usdk = _get_val(report_db, 18, "primary_income_statement", "Revenue", "FY26")
    d009_rev_zarm = report_db.execute(
        "SELECT value_num FROM cells WHERE physical_page=50 AND row_label='Revenue' AND fiscal_year='FY26' AND column_index=13"
    ).fetchone()[0]
    rate = report_db.execute(
        "SELECT value_num FROM cells WHERE physical_page=50 AND row_label='Average exchange rate' AND fiscal_year='FY26' AND unit='US$/ZAR' AND column_index=0"
    ).fetchone()[0]

    assert ifrs_rev_usdk == Decimal("1156451")
    assert Decimal(str(d009_rev_zarm)) == Decimal("17249.1")
    assert Decimal(str(rate)) == Decimal("16.9")

    # Proves the calculation in code (Covenant 2)
    implied_zarm = (ifrs_rev_usdk / Decimal("1000")) * Decimal(str(rate))
    delta_zarm = implied_zarm - Decimal(str(d009_rev_zarm))
    assert round(delta_zarm, 1) == Decimal("2294.9")
