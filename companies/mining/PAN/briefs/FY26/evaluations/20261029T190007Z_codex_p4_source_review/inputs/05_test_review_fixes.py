"""Assertions added after the independent review (reviews/p4_review_pack/INDEPENDENT_REVIEW.md).

Every figure the consolidated brief cites now has an executed assertion, or is gone from the
brief. Also closes the lineage defect (document must be the SHA-256) and restores the p.34
Note 18 acquisition rows that a modal-width filter had discarded.
"""
from __future__ import annotations

import re
from decimal import Decimal

import pytest

SHA = "62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd"


def _one(report_db, sql, args=()):
    row = report_db.execute(sql, args).fetchone()
    assert row is not None and row[0] is not None, f"no value for: {sql}"
    return Decimal(str(row[0]))


# ------------------------------------------------------------------ lineage (finding 3a)
def test_document_is_always_the_sha256(report_db):
    """Covenant 3: `document` must identify the source, not a local path.

    The review found 1,196 D009 cells storing a Windows path while the rest stored the hash.
    """
    distinct = [r[0] for r in report_db.execute(
        "SELECT DISTINCT document FROM cells").fetchall()]
    assert distinct == [SHA], f"expected one SHA-256, found {len(distinct)}: {distinct[:3]}"
    assert re.fullmatch(r"[0-9a-f]{64}", SHA)


# ------------------------------------------------------- p.34 Note 18 acquisition (finding 5)
def test_emmerson_acquisition_rows_present(report_db):
    """p.34 Note 18 rows survive with their note reference, not as 'caption fragments'.

    Ordinary shares to be issued 148,218 (note 14) and PPE acquired 142,436 (note 7) are the
    two rows an earlier modal-width filter discarded.
    """
    shares = _one(report_db,
                  "SELECT value_num FROM cells WHERE table_region='note_p34' "
                  "AND row_label LIKE '%Ordinary shares to be issued%'")
    ppe = _one(report_db,
               "SELECT value_num FROM cells WHERE table_region='note_p34' "
               "AND row_label LIKE '%Property, plant and equipment%'")
    assert shares == Decimal("148218")
    assert ppe == Decimal("142436")

    # 148,218 also prints on the balance sheet as 'Shares to be issued'
    bs = _one(report_db,
              "SELECT value_num FROM cells WHERE table_region='primary_balance_sheet_equity_liab' "
              "AND physical_page=17 AND row_label='Shares to be issued' AND fiscal_year='FY26'")
    assert bs == shares

    # 142,436 is the Note 7 'additions through acquisitions' total for FY26
    note7 = _one(report_db,
                 "SELECT value_num FROM cells WHERE table_region='note_p27' "
                 "AND row_label LIKE 'Additions through acquisitions%' "
                 "AND column_index=13 ORDER BY row_index DESC LIMIT 1")
    assert note7 == ppe


# ------------------------------------------------ earnings per share, comprehensive income
@pytest.mark.parametrize("fy,eps", [("FY26", "17.60"), ("FY25", "7.16")])
def test_earnings_per_share(report_db, fy, eps):
    """The brief cites basic and diluted EPS; nothing asserted it before."""
    printed = _one(report_db,
                   "SELECT value_num FROM cells WHERE table_region='primary_income_statement' "
                   "AND physical_page=18 AND row_label LIKE 'Basic and diluted earnings per share%' "
                   "AND fiscal_year=?", (fy,))
    assert printed == Decimal(eps)


@pytest.mark.parametrize("fy,tci,profit,oci", [
    ("FY26", "400965", "356911", "44054"),
    ("FY25", "155554", "140605", "14949"),
])
def test_total_comprehensive_income_cascade(report_db, fy, tci, profit, oci):
    """Profit for the period plus other comprehensive income equals total comprehensive income.

    The brief claimed this cascade; the test now executes it as well as asserting the printed
    total.
    """
    p = _one(report_db,
             "SELECT value_num FROM cells WHERE table_region='primary_income_statement' "
             "AND physical_page=18 AND row_label='Profit for the period' AND fiscal_year=?", (fy,))
    o = _one(report_db,
             "SELECT value_num FROM cells WHERE table_region='primary_income_statement' "
             "AND physical_page=18 AND row_label LIKE 'Other comprehensive income for the period%' "
             "AND fiscal_year=?", (fy,))
    t = _one(report_db,
             "SELECT value_num FROM cells WHERE table_region='primary_income_statement' "
             "AND physical_page=18 AND row_label='Total comprehensive income for the period' "
             "AND fiscal_year=?", (fy,))
    assert (p, o, t) == (Decimal(profit), Decimal(oci), Decimal(tci))
    assert p + o == t


# ------------------------------------------------------- APM printed totals (finding 2)
@pytest.mark.parametrize("region,label,expected", [
    ("apm_levered_free_cash_flow", "Levered free cash flow US$ million", "201.8"),
    ("apm_net_debt", "Net (cash)/debt", "-185.7"),
    ("apm_net_senior_debt", "Net (cash)/senior debt", "-194.7"),
])
def test_apm_printed_totals(report_db, region, label, expected):
    """Formula relations were tested; the printed totals themselves were not."""
    printed = _one(report_db,
                   "SELECT value_num FROM cells WHERE table_region=? AND row_label=? "
                   "AND fiscal_year='FY26'", (region, label))
    assert printed == Decimal(expected)


# ------------------------------------------------------- segment constants (finding 2)
@pytest.mark.parametrize("col,expected", [
    (0, "352807"), (1, "441978"), (2, "0"), (3, "228268"), (4, "132804"),
    (5, "1155857"), (7, "594"), (10, "1156451"),
])
def test_segment_revenue_constants(report_db, col, expected):
    """Individual segment revenue cells, not just the row sums (nil prints as a dash)."""
    if expected == "0":
        v = report_db.execute(
            "SELECT value_raw, value_num FROM cells WHERE table_region='note3_segment_analysis' "
            "AND physical_page=21 AND row_label='Revenue' AND fiscal_year='FY26' "
            "AND column_index=?", (col,)).fetchone()
        assert v is not None and v[0] == "–" and v[1] is None, v
        return
    printed = _one(report_db,
                   "SELECT value_num FROM cells WHERE table_region='note3_segment_analysis' "
                   "AND physical_page=21 AND row_label='Revenue' AND fiscal_year='FY26' "
                   "AND column_index=?", (col,))
    assert printed == Decimal(expected)


# ------------------------------------------------- Note 17.1 share-based roll-forward
def test_share_based_payment_roll_forward(report_db):
    """p.33 share-based payment obligation: opening + movements = closing, both years."""
    rows = {}
    for ri, lab, col, num in report_db.execute(
            "SELECT row_index, row_label, column_index, value_num FROM cells "
            "WHERE table_region='note_p33' ORDER BY row_index, column_index"):
        rows.setdefault(ri, {"label": lab, "cells": {}})["cells"][col] = Decimal(str(num or 0))
    rows = {ri: (v["label"], v["cells"]) for ri, v in rows.items()}

    bal = sorted(ri for ri, (lab, _c) in rows.items() if lab.startswith("Balance as at"))
    assert len(bal) >= 2, f"expected share-based balance rows, found {len(bal)}"
    a, b = bal[0], bal[1]
    mids = [ri for ri in sorted(rows) if a < ri < b]
    assert mids, "no movement rows between the share-based payment balances"
    for col in (0, 1):
        moved = sum(rows[ri][1].get(col, Decimal(0)) for ri in mids)
        delta = rows[b][1].get(col, Decimal(0)) - rows[a][1].get(col, Decimal(0))
        assert moved == delta, f"col{col}: movements {moved} != {delta}"
