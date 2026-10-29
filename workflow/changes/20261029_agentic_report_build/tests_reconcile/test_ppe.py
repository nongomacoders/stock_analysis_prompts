"""Note 7 Property, plant and equipment (PAN physical page 27).

The PPE table is the widest in the document: 14 printed columns covering land, buildings,
plant and the environmental rehabilitation asset, plus the total carrying amount. The text
layer lists each row as label followed by all 14 values, so the modal-width parser handles
it without coordinate snapping.

Checks:
  R1  each annual movement block reconciles per column (opening + movements = closing)
  R2  the FY26 closing total carrying amount ties the balance sheet PPE line
"""
from __future__ import annotations

from decimal import Decimal

import pytest

REGION = "note_p27"


def _rows(report_db):
    out = {}
    for ri, lab, col, num in report_db.execute(
            "SELECT row_index, row_label, column_index, value_num FROM cells "
            "WHERE table_region=? ORDER BY row_index, column_index", (REGION,)):
        out.setdefault(ri, {"label": lab, "cells": {}})["cells"][col] = Decimal(str(num or 0))
    # dict keyed by row_index still carries the label seen first
    return {ri: (v["label"], v["cells"]) for ri, v in out.items()}


def _balance_rows(rows):
    return sorted(ri for ri, (lab, _c) in rows.items() if lab.lower().startswith("balance"))


@pytest.mark.parametrize("which", [0, 1], ids=["FY25", "FY26"])
def test_ppe_roll_forward(report_db, which):
    """Opening + every movement line = closing, column by column."""
    rows = _rows(report_db)
    bal = _balance_rows(rows)
    assert len(bal) == 3, f"expected three balance rows (FY24 opening, FY25, FY26), got {len(bal)}"
    a, b = bal[which], bal[which + 1]
    mids = [ri for ri in sorted(rows) if a < ri < b]
    assert len(mids) >= 5, f"only {len(mids)} movement rows between {a} and {b}"
    width = max(rows[a][1])
    for col in range(width + 1):
        moved = sum(rows[ri][1].get(col, Decimal(0)) for ri in mids)
        delta = rows[b][1].get(col, Decimal(0)) - rows[a][1].get(col, Decimal(0))
        assert moved == delta, (
            f"{rows[a][0]} -> {rows[b][0]} col{col}: movements {moved} != closing-opening {delta}")


def test_ppe_cost_total_printed(report_db):
    """The FY26 closing row's rightmost column is total cost: 1,536,566.

    The carrying amount (1,196,474 on the balance sheet) is NOT on this page - it prints in
    the continuation on physical p.28, which is still deferred (see WORKPLAN_APM.md). So the
    closing cost total is asserted here and the carrying-amount tie is explicitly reported
    as not yet possible rather than approximated.
    """
    rows = _rows(report_db)
    last = _balance_rows(rows)[-1]
    label, cells = rows[last]
    assert label == "Balance as at 30 June 2026"
    assert cells[max(cells)] == Decimal("1536566")
    bs = Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_balance_sheet_assets' "
        "AND physical_page=17 AND row_label='Property, plant and equipment' "
        "AND fiscal_year='FY26'").fetchone()[0]))
    assert bs == Decimal("1196474")
    assert bs not in cells.values(), (
        "carrying amount unexpectedly present on p.27; if this fires, the p.28 rows have "
        "been extracted and a real tie can be asserted")
    carried = report_db.execute(
        "SELECT COUNT(*) FROM cells WHERE table_region='note_p28'").fetchone()[0]
    assert carried == 0, "p.28 now extracted - replace this test with a real carrying-amount tie"
