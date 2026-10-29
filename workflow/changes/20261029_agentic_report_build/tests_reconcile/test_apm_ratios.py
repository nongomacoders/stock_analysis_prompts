"""APM ratio tables on PAN physical page 46: NAV per share, levered free cash flow and
cash flow yield per share.

These are the definitions behind the report's per-share metrics, and they close a chain
from Note 3 / p.45 Adjusted EBITDA down to a cash-flow yield: each step below is executed
here in code against printed cells.
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

import pytest

NAV = "apm_nav_per_share"
LFCF = "apm_levered_free_cash_flow"
YIELD = "apm_cash_flow_yield"


def _t(report_db, region, label, fy):
    row = report_db.execute(
        "SELECT value_num FROM cells WHERE table_region=? AND row_label=? AND fiscal_year=?",
        (region, label, fy)).fetchone()
    assert row is not None, f"missing {region} '{label}' {fy}"
    return Decimal(str(row[0] or 0))


@pytest.mark.parametrize("fy,expected", [("FY26", "51.10"), ("FY25", "26.94")])
def test_nav_per_share(report_db, fy, expected):
    """Total equity / (shares in issue - treasury shares), printed in US cents."""
    equity = _t(report_db, NAV, "Total equity US$ million", fy)
    shares = _t(report_db, NAV, "Shares in issue million", fy)
    treasury = _t(report_db, NAV, "Treasury shares million", fy)
    printed = _t(report_db, NAV, "Net asset value per share US cents", fy)

    nav_cents = (equity / (shares + treasury)) * Decimal(100)
    assert nav_cents.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) == printed
    assert printed == Decimal(expected)


@pytest.mark.parametrize("fy,expected", [("FY26", "2027.3"), ("FY25", "2029.3")])
def test_total_shares(report_db, fy, expected):
    """Total number of shares = shares in issue less treasury shares."""
    shares = _t(report_db, LFCF, "Shares in issue number million", fy)
    treasury = _t(report_db, LFCF, "Treasury shares number million", fy)
    total = _t(report_db, LFCF, "Total number of shares number million", fy)
    assert shares + treasury == total
    assert total == Decimal(expected)


@pytest.mark.parametrize("fy", ["FY26", "FY25"])
def test_levered_free_cash_flow_build(report_db, fy):
    """Adjusted EBITDA less cash costs, plus working capital, less capex, plus net debt flows."""
    def g(label):
        return _t(report_db, LFCF, label, fy)

    built = (g("Adjusted EBITDA US$ million")
             + g("Finance costs paid US$ million")
             + g("Income tax paid US$ million")
             + g("Net working capital movement US$ million")
             + g("Capital expenditure US$ million")
             + g("Proceeds from borrowings US$ million")
             + g("Repayment of borrowings US$ million"))
    printed = g("Levered free cash flow US$ million")
    assert built == printed, f"{fy}: built {built} vs printed {printed}"


@pytest.mark.parametrize("fy", ["FY26", "FY25"])
def test_cash_flow_per_share_and_yield(report_db, fy):
    """Levered FCF / total shares -> cents per share; cents per share / price -> yield %."""
    lfcf = _t(report_db, LFCF, "Levered free cash flow US$ million", fy)
    total = _t(report_db, LFCF, "Total number of shares number million", fy)
    printed_cps = _t(report_db, LFCF, "Attributable cash flow per share US cents per share", fy)

    cps = (lfcf / total) * Decimal(100)
    assert cps.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) == printed_cps

    assert printed_cps == _t(report_db, YIELD, "Attributable cash flow per share US cents per share", fy)
    price = _t(report_db, YIELD, "Last traded price per Pan African share1 US cents per share", fy)
    printed_yield = _t(report_db, YIELD, "Cash flow yield per share %", fy)

    yield_pct = (cps / price) * Decimal(100)
    assert yield_pct.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) == printed_yield


def test_levered_free_cash_flow_ebitda_ties_note3(report_db):
    """The p.46 Adjusted EBITDA input (609.4 US$m) equals Note 3 p.22 Group Adjusted EBITDA.

    Cross-section tie: the APM ratio table starts from the same measure Note 3 reconciles
    (609,431 US$k), confirming the two presentations share one definition.
    """
    lfcf_ebitda = _t(report_db, LFCF, "Adjusted EBITDA US$ million", "FY26")
    note3 = Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='note3_segment_analysis' "
        "AND physical_page=22 AND row_label='Adjusted EBITDA3' AND fiscal_year='FY26' "
        "AND column_index=10").fetchone()[0]))
    assert lfcf_ebitda == Decimal("609.4")
    assert (note3 / Decimal(1000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP) == lfcf_ebitda
