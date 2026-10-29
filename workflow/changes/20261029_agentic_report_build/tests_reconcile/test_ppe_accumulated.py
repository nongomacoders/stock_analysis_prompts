"""Note 7 PPE carrying amounts (PAN physical page 28).

Closes the PPE bridge: cost (p.27 closing) less accumulated depreciation (p.28 closing)
equals the carrying amount, and both year-end carrying amounts tie the balance sheet.

Note on row widths: movement rows carry 14 values while the balance and carrying-amount
rows also carry 14 once a leading four-digit year is returned to the label. Filtering on a
modal width, as the generic note parser does, silently discards the balance rows - which is
why this page needed its own extractor.
"""
from __future__ import annotations

from decimal import Decimal

import pytest

REGION = "note_p28"


def _rows(report_db):
    out = {}
    for ri, lab, col, num in report_db.execute(
            "SELECT row_index, row_label, column_index, value_num FROM cells "
            "WHERE table_region=? ORDER BY row_index, column_index", (REGION,)):
        out.setdefault(ri, {"label": lab, "cells": {}})["cells"][col] = Decimal(str(num or 0))
    return {ri: (v["label"], v["cells"]) for ri, v in out.items()}


def _by_label(rows, prefix):
    hits = [(lab, cells) for lab, cells in rows.values() if lab.startswith(prefix)]
    assert hits, f"no row starting '{prefix}' on p.28"
    return hits


@pytest.mark.parametrize("expected,fy", [("824450", "FY25"), ("1196474", "FY26")])
def test_carrying_amount_ties_balance_sheet(report_db, expected, fy):
    """The 'As at 30 June' carrying-amount rows tie the balance-sheet PPE line, both years."""
    rows = _rows(report_db)
    label = f"As at 30 June {'2026' if fy == 'FY26' else '2025'}"
    hits = _by_label(rows, label)
    cells = hits[0][1]
    total = cells[max(cells)]
    bs = Decimal(str(report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='primary_balance_sheet_assets' "
        "AND physical_page=17 AND row_label='Property, plant and equipment' "
        "AND fiscal_year=?", (fy,)).fetchone()[0]))
    assert total == bs, f"{fy}: p.28 carrying {total} != balance sheet {bs}"
    assert total == Decimal(expected)


def test_cost_less_accumulated_depreciation(report_db):
    """PPE cost 1,536,566 (p.27 closing) less accumulated depreciation 340,092 = 1,196,474."""
    rows = _rows(report_db)
    accdep = _by_label(rows, "Balance as at 30 June 2026")[0][1]
    accdep_total = accdep[max(accdep)]
    assert accdep_total == Decimal("-340092"), accdep_total

    cost_row = report_db.execute(
        "SELECT value_num FROM cells WHERE table_region='note_p27' "
        "AND row_label='Balance as at 30 June 2026' AND column_index=13").fetchone()
    assert cost_row is not None
    cost = Decimal(str(cost_row[0]))
    assert cost == Decimal("1536566")

    carrying = _by_label(rows, "As at 30 June 2026")[0][1]
    assert cost + accdep_total == carrying[max(carrying)]


def test_accumulated_depreciation_block_present(report_db):
    """The accumulated-depreciation block is present with its three balance rows."""
    rows = _rows(report_db)
    bal = [ri for ri, (lab, _c) in rows.items() if lab.startswith("Balance as at")]
    assert len(bal) == 3
    assert len(rows) == 16
