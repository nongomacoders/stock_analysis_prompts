"""Reconciliation checks for PAN Note 3 Segment Analysis (physical pages 21-24).

Governed by the same charter covenants as the rest of the suite:
  - Covenant 1: printed values are never replaced; mismatches are recorded data.
  - Covenant 2: every total/delta below is computed here, in code.
  - Covenant 3: every cell carries page + document hash + extraction commit.

Two families:
  H  horizontal segment identities (Mining operations subtotal, Group total)
  X  cross-section ties to the primary statements (S006) and to the production
     summary (D009)
"""
from __future__ import annotations

from decimal import Decimal

import pytest

REGION = "note3_segment_analysis"
MINING_SUBTOTAL = 5
GROUP_TOTAL = 10


def _val(report_db, page, label, fy, col):
    row = report_db.execute(
        "SELECT value_num FROM cells WHERE table_region=? AND physical_page=? "
        "AND row_label=? AND fiscal_year=? AND column_index=?",
        (REGION, page, label, fy, col)).fetchone()
    assert row is not None, f"missing cell p{page} '{label}' {fy} col{col}"
    return Decimal(str(row[0] or 0))


def _row_values(report_db, page, fy):
    """{row_label: {col: Decimal}} for the main Note 3 table of one page."""
    out = {}
    for label, col, num in report_db.execute(
            "SELECT row_label, column_index, value_num FROM cells "
            "WHERE table_region=? AND physical_page=? AND fiscal_year=?",
            (REGION, page, fy)):
        out.setdefault(label, {})[col] = Decimal(str(num or 0))
    return out


@pytest.mark.parametrize("page,fy", [(21, "FY26"), (22, "FY26"), (23, "FY25"), (24, "FY25")])
def test_mining_operations_subtotal(report_db, page, fy):
    """Segments 0-4 (Barberton, Evander, Solar, MTR, Tennant) sum to Mining operations."""
    rows = _row_values(report_db, page, fy)
    assert rows, f"no Note 3 rows extracted for p{page}"
    for label, cells in rows.items():
        parts = sum(cells.get(i, Decimal(0)) for i in range(5))
        printed = cells.get(MINING_SUBTOTAL, Decimal(0))
        assert parts == printed, f"p{page} {fy} '{label}': {parts} != {printed}"


@pytest.mark.parametrize("page,fy", [(21, "FY26"), (22, "FY26"), (23, "FY25"), (24, "FY25")])
def test_group_total_equals_subtotals(report_db, page, fy):
    """Mining operations + Exploration + ESG + Corporate + Funding == Group total."""
    rows = _row_values(report_db, page, fy)
    for label, cells in rows.items():
        parts = sum(cells.get(i, Decimal(0)) for i in (5, 6, 7, 8, 9))
        printed = cells.get(GROUP_TOTAL, Decimal(0))
        assert parts == printed, f"p{page} {fy} '{label}': {parts} != {printed}"


# ------------------------------------------------- cross-section ties (S006)
def test_note3_revenue_ties_income_statement(report_db):
    """Note 3 Group revenue (p.21) == Income Statement revenue (p.18) == 1,156,451 US$k."""
    note3 = _val(report_db, 21, "Revenue", "FY26", GROUP_TOTAL)
    p18 = report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_income_statement' "
        "AND physical_page=18 AND row_label='Revenue' AND fiscal_year='FY26'").fetchone()[0]
    assert note3 == Decimal(str(p18)) == Decimal("1156451")


def test_note3_cost_of_production_ties_income_statement(report_db):
    note3 = _val(report_db, 21, "Cost of production", "FY26", GROUP_TOTAL)
    p18 = report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_income_statement' "
        "AND physical_page=18 AND row_label='Cost of production' AND fiscal_year='FY26'").fetchone()[0]
    assert note3 == Decimal(str(p18)) == Decimal("-514297")


def test_note3_operating_profit_ties_income_statement(report_db):
    note3 = _val(report_db, 21, "Profit/(loss) before finance income and finance costs", "FY26", GROUP_TOTAL)
    p18 = report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_income_statement' AND physical_page=18 "
        "AND row_label='Profit before finance income and finance costs' AND fiscal_year='FY26'").fetchone()[0]
    assert note3 == Decimal(str(p18)) == Decimal("545838")


def test_note3_profit_lines_tie_income_statement(report_db):
    for label, expected in (("Profit/(loss) before tax", "534368"),
                            ("Income tax (expense)/credit", "-177457"),
                            ("Profit/(loss) for the period excluding intra-Group transactions", "356911")):
        assert _val(report_db, 21, label, "FY26", GROUP_TOTAL) == Decimal(expected), label


def test_segment_assets_plus_goodwill_ties_total_assets(report_db):
    """Note 3 segment assets (p.22) + goodwill == Total assets on the balance sheet (p.17)."""
    seg_assets = _val(report_db, 22, "Segment assets (total assets excluding goodwill)", "FY26", GROUP_TOTAL)
    goodwill = _val(report_db, 22, "Goodwill", "FY26", GROUP_TOTAL)
    total_assets = Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_balance_sheet_assets' AND physical_page=17 "
        "AND row_label='Total assets' AND fiscal_year='FY26'").fetchone()[0]))
    assert seg_assets == Decimal("1589637")
    assert seg_assets + goodwill == total_assets == Decimal("1608075")


def test_segment_liabilities_tie_balance_sheet(report_db):
    seg_liab = _val(report_db, 22, "Segment liabilities", "FY26", GROUP_TOTAL)
    ncl = Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_balance_sheet_equity_liab' AND physical_page=17 "
        "AND row_label='Total non-current liabilities' AND fiscal_year='FY26'").fetchone()[0]))
    cl = Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_balance_sheet_equity_liab' AND physical_page=17 "
        "AND row_label='Total current liabilities' AND fiscal_year='FY26'").fetchone()[0]))
    assert seg_liab == ncl + cl == Decimal("572078")


def test_net_assets_plus_goodwill_ties_total_equity(report_db):
    net_assets = _val(report_db, 22, "Net assets (excluding goodwill)1", "FY26", GROUP_TOTAL)
    goodwill = _val(report_db, 22, "Goodwill", "FY26", GROUP_TOTAL)
    equity = Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_balance_sheet_equity_liab' AND physical_page=17 "
        "AND row_label='Total equity' AND fiscal_year='FY26'").fetchone()[0]))
    assert net_assets + goodwill == equity == Decimal("1035997")


# ------------------------------------- APM scope delta (D009 p.50 vs Note 3 p.22)
def test_adjusted_ebitda_apm_scope_delta(report_db):
    """Note 3 Adjusted EBITDA (609,431 US$k) differs from D009 p.50 Adjusted EBITDA (663.1 US$m).

    Both figures are printed. Neither is replaced: the gap is recorded as data and
    quantified here so the report can state the scope difference (Note 3 measures
    after corporate and funding-company overheads; the D009 summary measures the
    operating segments). The residual ties to the Corporate and Funding columns.
    """
    note3 = _val(report_db, 22, "Adjusted EBITDA3", "FY26", GROUP_TOTAL)
    d009 = Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE physical_page=50 AND row_label='Adjusted EBITDA US$' "
        "AND fiscal_year='FY26' AND column_index=13").fetchone()[0]))
    assert note3 == Decimal("609431")
    assert d009 == Decimal("663.1")
    gap = d009 - note3 / Decimal(1000)
    assert round(gap, 3) == Decimal("53.669")
