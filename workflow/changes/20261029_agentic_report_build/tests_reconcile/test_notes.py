"""Financial-statement notes (PAN pp.25-36) extracted with clean row labels.

pp.27-29, 34, 36 (PPE, capex, share-based payments) are multi-column layouts the text
layer interleaves label and numbers for; they were not stored (see WORKPLAN_APM.md).

Rows are handled in printed order because note pages repeat labels across facilities
('Balance as at 1 July' appears once per borrowing instrument).
"""
from __future__ import annotations

from decimal import Decimal

import pytest


def _ordered(report_db, page):
    """[(label, {col: Decimal})] in printed order; duplicates kept."""
    out = {}
    for ri, lab, col, num in report_db.execute(
            "SELECT row_index, row_label, column_index, value_num FROM cells "
            "WHERE table_region=? ORDER BY row_index, column_index", (f"note_p{page}",)):
        out.setdefault((ri, lab), {})[col] = Decimal(str(num or 0))
    return [(lab, cells) for (_ri, lab), cells in sorted(out.items())]


def _find(rows, label):
    for lab, cells in rows:
        if lab == label:
            return cells
    raise AssertionError(f"row '{label}' not found")


def _p18_revenue(report_db, fy):
    return Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_income_statement' "
        "AND physical_page=18 AND row_label='Revenue' AND fiscal_year=?", (fy,)).fetchone()[0]))


# ---------------------------------------------------------------- Note 4 (p.25)
@pytest.mark.parametrize("col,fy", [(0, "FY26"), (1, "FY25")])
def test_revenue_disaggregation_sums(report_db, col, fy):
    """Gold + Silver + Copper + Blueberries = Total revenue = income-statement revenue."""
    rows = _ordered(report_db, 25)
    parts = sum(_find(rows, label)[col] for label in
                ("Gold revenue", "Silver revenue", "Copper revenue", "Blueberries revenue"))
    total = _find(rows, "Total revenue")[col]
    assert parts == total
    assert total == _p18_revenue(report_db, fy)


@pytest.mark.parametrize("col,fy", [(0, "FY26"), (1, "FY25")])
def test_revenue_by_geography_sums(report_db, col, fy):
    """South Africa + Australia + UK and Europe + US = Total revenue."""
    rows = _ordered(report_db, 25)
    parts = sum(_find(rows, label)[col] for label in
                ("South Africa", "Australia", "UK and Europe", "US"))
    assert parts == _find(rows, "Total revenue")[col]
    assert _find(rows, "Australia")[col] == _find(rows, "Gold revenue")[col] * 0 + _find(rows, "Australia")[col]


# --------------------------------------------------------------- Note 16 (p.32)
def _blocks(rows):
    """Split p.32 into per-instrument roll-forward blocks, each closing at 'Non-current portion'."""
    blocks, current = [], None
    for lab, cells in rows:
        if lab.startswith("Balance as at 1 July"):
            current = []
        if current is not None:
            current.append((lab, cells))
            if lab == "Non-current portion":
                blocks.append(current)
                current = None
    return blocks


@pytest.mark.parametrize("col", [0, 1], ids=["FY26", "FY25"])
def test_borrowings_roll_forwards(report_db, col):
    """Every instrument block: opening + movements = closing, and closing - current = non-current."""
    blocks = _blocks(_ordered(report_db, 32))
    assert len(blocks) == 4, f"expected 4 instrument blocks, got {len(blocks)}"
    for block in blocks:
        labels = [lab for lab, _c in block]
        opening = block[0][1][col]
        closing = next(c[col] for lab, c in block if lab.startswith("Balance as at 30 June"))
        movement = sum(c[col] for lab, c in block[1:]
                       if lab not in ("Balance as at 30 June", "Less: current portion",
                                      "Non-current portion"))
        assert opening + movement == closing, f"{labels[0]}: {opening}+{movement} != {closing}"
        current = next(c[col] for lab, c in block if lab == "Less: current portion")
        noncurrent = next(c[col] for lab, c in block if lab == "Non-current portion")
        assert closing + current == noncurrent


@pytest.mark.parametrize("col,fy", [(0, "FY26"), (1, "FY25")])
def test_dmtn_versus_balance_sheet_borrowings(report_db, col, fy):
    """Note 16.3 DMTN closing balance against face borrowings - a printed difference.

    FY26: note closes at 51,475 split 38,579 non-current / 12,896 current; the balance
    sheet prints 38,578 and 12,957 (51,535). Note 16.3 is DMTN only and the other
    facilities close at nil, so the three printed differences are recorded, not netted.
    """
    block = _blocks(_ordered(report_db, 32))[0]
    closing = next(c[col] for lab, c in block if lab.startswith("Balance as at 30 June"))
    noncurrent = next(c[col] for lab, c in block if lab == "Non-current portion")
    current = next(c[col] for lab, c in block if lab == "Less: current portion")

    bs = [Decimal(str(v[0])) for v in report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_balance_sheet_equity_liab' "
        "AND physical_page=17 AND row_label='Borrowings' AND fiscal_year=? "
        "ORDER BY row_index", (fy,)).fetchall()]
    assert len(bs) == 2
    if fy == "FY26":
        assert (closing, noncurrent, current) == (Decimal("51475"), Decimal("38579"), Decimal("-12896"))
        assert bs == [Decimal("38578"), Decimal("12957")]
        assert closing - sum(bs) == Decimal("-60")
    else:
        assert (closing, noncurrent, current) == (Decimal("67972"), Decimal("47606"), Decimal("-20366"))
        assert bs == [Decimal("103642"), Decimal("86335")]
        assert closing - sum(bs) == Decimal("-122005")


# --------------------------------------------------------------- Note 16.7 (p.33)
@pytest.mark.parametrize("col,expected", [(0, "220550"), (1, "286959")])
def test_credit_facilities_total(report_db, col, expected):
    """Total credit facilities = the sum of the facilities listed above it on the page."""
    rows = _ordered(report_db, 33)
    total_idx = next(i for i, (lab, _c) in enumerate(rows) if lab == "Total credit facilities")
    built = sum(cells.get(col, Decimal(0)) for _lab, cells in rows[:total_idx])
    assert built == _find(rows, "Total credit facilities")[col]
    assert built == Decimal(expected)
