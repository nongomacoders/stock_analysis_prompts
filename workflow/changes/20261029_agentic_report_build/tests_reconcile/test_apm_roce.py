"""p.47 ratios: return on capital employed, and the per-share history rows.

ROCE is rebuilt from printed inputs and its two denominators are traced to other sections:
average equity to the balance sheet, average borrowings to the p.44 net debt reconciliation.
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

import pytest

ROCE = "apm_roce"
PS = "apm_per_share_history"

NET = "Net income before finance income and finance costs"
EQUITY = "Average equity"
BORROWINGS = "Average borrowings"
RATIO = "Return on capital employed"


def _t(report_db, region, label, fy):
    row = report_db.execute(
        "SELECT value_num FROM cells WHERE table_region=? AND row_label=? AND fiscal_year=?",
        (region, label, fy)).fetchone()
    assert row is not None, f"missing {region} '{label}' {fy}"
    return Decimal(str(row[0] or 0))


@pytest.mark.parametrize("fy,expected", [("FY26", "59.8"), ("FY25", "35.1")])
def test_roce_rebuild(report_db, fy, expected):
    """ROCE = earnings before finance costs and tax / (average equity + average borrowings)."""
    net = _t(report_db, ROCE, NET, fy)
    equity = _t(report_db, ROCE, EQUITY, fy)
    borrowings = _t(report_db, ROCE, BORROWINGS, fy)
    printed = _t(report_db, ROCE, RATIO, fy)
    pct = (net / (equity + borrowings)) * Decimal(100)
    assert pct.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP) == printed
    assert printed == Decimal(expected)


def test_roce_numerator_ties_income_statement(report_db):
    """The ROCE numerator is the operating profit printed on the face of the income statement."""
    net = _t(report_db, ROCE, NET, "FY26")
    p18 = Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_income_statement' "
        "AND physical_page=18 AND row_label='Profit before finance income and finance costs' "
        "AND fiscal_year='FY26'").fetchone()[0]))
    assert (p18 / Decimal(1000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP) == net


def test_average_equity_ties_balance_sheet(report_db):
    """Average equity = mean of the two printed year-end total equity figures, in US$m."""
    eq26 = Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_balance_sheet_equity_liab' "
        "AND physical_page=17 AND row_label='Total equity' AND fiscal_year='FY26'").fetchone()[0]))
    eq25 = Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_balance_sheet_equity_liab' "
        "AND physical_page=17 AND row_label='Total equity' AND fiscal_year='FY25'").fetchone()[0]))
    avg = ((eq26 + eq25) / Decimal(2) / Decimal(1000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    assert avg == _t(report_db, ROCE, EQUITY, "FY26") == Decimal("791.3")


def test_average_borrowings_tie_net_debt_table(report_db):
    """Average borrowings = mean of the two borrowings figures in the p.44 net debt table."""
    b26 = Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='apm_net_debt' AND row_label='Borrowings' "
        "AND fiscal_year='FY26'").fetchone()[0]))
    b25 = Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='apm_net_debt' AND row_label='Borrowings' "
        "AND fiscal_year='FY25'").fetchone()[0]))
    avg = ((b26 + b25) / Decimal(2)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    assert avg == _t(report_db, ROCE, BORROWINGS, "FY26") == Decimal("120.8")


def test_per_share_history_rows(report_db):
    """Earnings and dividends per share print across five years in cents and pence."""
    for label, fy26_cents in (("Earnings per share", "298.12"), ("Dividends per share", "77.00")):
        value = _t(report_db, PS, label, "FY26")
        assert value == Decimal(fy26_cents), label
        n = report_db.execute(
            "SELECT COUNT(*) FROM cells WHERE table_region=? AND row_label=?", (PS, label)).fetchone()[0]
        assert n == 10, f"{label}: expected 10 printed columns, got {n}"
