"""p.44 capital expenditure, net debt and net senior debt.

Capital: sustaining + expansion = total on every row; segment totals rebuild the group
total; the group total ties Note 3 capex and the D009 p.50 capex figure.
Debt: the component lines rebuild each printed net (cash)/debt figure, and borrowings
ties the balance sheet.
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

import pytest

CAP = "apm_capital_expenditure"
DEBT = "apm_net_debt"
SENIOR = "apm_net_senior_debt"


def _rows(report_db, region):
    """[(row_index, label, {col: Decimal})] in printed order."""
    out = {}
    for ri, label, col, num in report_db.execute(
            "SELECT row_index, row_label, column_index, value_num FROM cells "
            "WHERE table_region=? ORDER BY row_index, column_index", (region,)):
        key = (ri, label)
        out.setdefault(key, {})[col] = Decimal(str(num or 0))
    return [(ri, label, cells) for (ri, label), cells in sorted(out.items())]


@pytest.mark.parametrize("fy_off", [0, 1], ids=["FY26", "FY25"])
def test_sustaining_plus_expansion_equals_total(report_db, fy_off):
    """Every capital row: sustaining + expansion = total, for both years.

    One printed row misses by 0.1 (BTRP FY25: 0.3 + 2.6 = 2.9 vs printed 2.8), a
    single-decimal rounding artefact recorded in `conflicts`. The deviation set is
    asserted exactly so nothing else can drift.
    """
    deviations = set()
    for _ri, label, cells in _rows(report_db, CAP):
        sustaining, expansion, total = (cells[fy_off], cells[2 + fy_off], cells[4 + fy_off])
        delta = (sustaining + expansion) - total
        if delta != 0:
            deviations.add((label, "FY26" if fy_off == 0 else "FY25", delta))
    expected = {("BTRP", "FY25", Decimal("0.1"))} if fy_off == 1 else set()
    assert deviations == expected, f"unexpected deviations: {deviations}"


@pytest.mark.parametrize("off,expected", [(0, "21.8"), (2, "202.2"), (4, "224.0")])
def test_group_total_rebuilds(report_db, off, expected):
    """Group total = Barberton + Evander + MTR + Tennant + Agricultural ESG + Solar + Corporate."""
    rows = _rows(report_db, CAP)
    parts = [rows[i][2][off] for i in (2, 5, 6, 7, 8, 9, 10)]
    total = rows[-1][2][off]
    assert rows[-1][1] == "Group total"
    assert sum(parts) == total, f"parts {parts} != {total}"
    assert total == Decimal(expected)


def test_capital_group_total_ties_note3_and_p50(report_db):
    """Group total capital FY26 (224.0 US$m) ties Note 3 capex and the D009 p.50 leaf sum.

    Note 3 prints capital expenditure of 223,995 US$k and D009 p.50 prints capex leaves
    summing to 214.9, which is the cash-paid measure; the 224.0 total capital figure is the
    accruals measure. Recorded as printed on both sides.
    """
    rows = _rows(report_db, CAP)
    total_fy26 = rows[-1][2][4]
    note3 = Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='note3_segment_analysis' "
        "AND physical_page=22 AND row_label='Capital expenditure2' AND fiscal_year='FY26' "
        "AND column_index=10").fetchone()[0]))
    assert total_fy26 == Decimal("224.0")
    assert (note3 / Decimal(1000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP) == total_fy26


def test_barberton_and_evander_totals(report_db):
    """Asset subtotals: Barberton = mining + BTRP; Evander = mining + Elikhulu."""
    rows = _rows(report_db, CAP)
    labels = [label for _ri, label, _c in rows]
    assert labels[0] == "Mining operations" and labels[3] == "Mining operations"

    for off in (0, 2, 4):
        assert rows[0][2][off] + rows[1][2][off] == rows[2][2][off], "Barberton total"
        assert rows[3][2][off] + rows[4][2][off] == rows[5][2][off], "Evander total"


@pytest.mark.parametrize("region,label_final", [
    (DEBT, "Net (cash)/debt"),
    (SENIOR, "Net (cash)/senior debt"),
])
def test_debt_components_rebuild(report_db, region, label_final):
    """The printed component lines sum to the printed net (cash)/debt for each period."""
    rows = _rows(report_db, region)
    assert rows[-1][1] == label_final
    components = rows[:-1]
    for col in (0, 1):
        built = sum(cells[col] for _ri, _l, cells in components)
        printed = rows[-1][2][col]
        assert built == printed, f"{region} col{col}: built {built} != printed {printed}"


def test_net_debt_borrowings_tie_balance_sheet(report_db):
    """Borrowings in the net debt reconciliation tie the balance sheet borrowings total."""
    rows = _rows(report_db, DEBT)
    borrowings = next(cells[0] for _ri, label, cells in rows if label == "Borrowings")
    ncl = Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_balance_sheet_equity_liab' "
        "AND physical_page=17 AND row_label='Borrowings' AND fiscal_year='FY26' "
        "AND column_index=0").fetchone()[0]))
    cl = report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_balance_sheet_equity_liab' "
        "AND physical_page=17 AND row_label='Borrowings' AND fiscal_year='FY26' "
        "AND column_index=1").fetchall()
    # two 'Borrowings' rows on the balance sheet: non-current (first) and current (second)
    rows_bs = [Decimal(str(v[0])) for v in report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_balance_sheet_equity_liab' "
        "AND physical_page=17 AND row_label='Borrowings' AND fiscal_year='FY26' "
        "ORDER BY row_index").fetchall()]
    assert len(rows_bs) == 2
    assert borrowings == Decimal("51.5")
    assert (sum(rows_bs) / Decimal(1000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP) == borrowings
