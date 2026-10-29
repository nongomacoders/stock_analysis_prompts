"""APM Adjusted EBITDA reconciliation (PAN physical page 45).

The page is the definition layer behind D009 p.50 and Note 3 p.22: it repeats the
operation grid (13 value columns) in US$ million and reconciles each column from net
income/(cost) before finance to Adjusted EBITDA.

Checks:
  V1  column roll-forward (net income -> EBITDA -> Adjusted EBITDA)
  H1  mining subtotal            H2  tailings subtotal
  H3  total-operations build     H4  group total
  X1  cell-by-cell comparison with D009 p.50
"""
from __future__ import annotations

from decimal import Decimal

import pytest

REGION = "apm_adjusted_ebitda"
PAGE = 45
MINING_TOTAL, TAILINGS_TOTAL, GROUP = 2, 7, 12
BARBERTON_TOTAL, EVANDER_TOTAL, MTR_TOTAL, TENNANT_TOTAL = 8, 9, 10, 11

# p.45 column -> D009 p.50 column (p.50 has an extra blank visual column at 4)
P50 = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13]

NET_INCOME = "Net income/(cost) before finance income and finance costs"
DEPRECIATION = "Mining depreciation and amortisation"
DISPOSAL = "(Profit)/loss on disposal of plant and equipment"
ADJUSTED = "Adjusted EBITDA"
EBITDA = "EBITDA"
DERIVATIVES = "Unrealised fair value loss on financial derivatives"
BARGAIN = "Bargain gains on purchase"


def _rows(report_db, fy):
    out = {}
    for label, col, num in report_db.execute(
            "SELECT row_label, column_index, value_num FROM cells "
            "WHERE table_region=? AND fiscal_year=?", (REGION, fy)):
        out.setdefault(label, {})[col] = Decimal(str(num or 0))
    return out


@pytest.mark.parametrize("fy", ["FY26", "FY25"])
def test_v1_column_roll_forward(report_db, fy):
    """Each column reconciles from net income to Adjusted EBITDA using the printed lines.

    The table prints every cell to one decimal, so a column can miss its own printed build
    by 0.1. Deviations are bounded at 0.1 here and each non-zero one is recorded in
    `conflicts` (see record_apm_rounding.py); a larger miss still fails.
    """
    rows = _rows(report_db, fy)
    assert ADJUSTED in rows, f"no Adjusted EBITDA row for {fy}"
    tol = Decimal("0.1")
    for col in range(13):
        net = rows[NET_INCOME].get(col, Decimal(0))
        dep = rows[DEPRECIATION].get(col, Decimal(0))
        adj = rows[ADJUSTED].get(col, Decimal(0))
        if fy == "FY26":
            disp = rows[DISPOSAL].get(col, Decimal(0))
            built = net + dep + disp
        else:
            ebitda = rows[EBITDA].get(col, Decimal(0))
            assert abs((net + dep) - ebitda) <= tol, f"{fy} col{col} EBITDA build"
            built = ebitda + rows[DERIVATIVES].get(col, Decimal(0)) + rows[BARGAIN].get(col, Decimal(0))
        assert abs(adj - built) <= tol, f"{fy} col{col}: adjusted {adj} vs build {built}"


@pytest.mark.parametrize("fy", ["FY26", "FY25"])
def test_horizontal_builds(report_db, fy):
    """Mining, tailings, total-operations and group builds, on every row of the page."""
    tol = Decimal("0.1")
    for label, cells in _rows(report_db, fy).items():
        g = lambda i: cells.get(i, Decimal(0))
        for name, built, printed in (
            ("mining", g(0) + g(1), g(MINING_TOTAL)),
            ("tailings", g(3) + g(4) + g(5) + g(6), g(TAILINGS_TOTAL)),
            ("barberton", g(0) + g(3), g(BARBERTON_TOTAL)),
            ("evander", g(1) + g(4), g(EVANDER_TOTAL)),
            ("mtr", g(5), g(MTR_TOTAL)),
            ("tennant", g(6), g(TENNANT_TOTAL)),
            ("group", g(8) + g(9) + g(10) + g(11), g(GROUP)),
        ):
            assert abs(built - printed) <= tol, f"{fy} '{label}' {name}: {built} vs {printed}"


def test_rounding_deviations_are_all_recorded(report_db):
    """Every non-zero 0.1 deviation on this page must exist as a recorded conflict."""
    tol = Decimal("0.1")
    found = []
    for fy in ("FY26", "FY25"):
        rows = _rows(report_db, fy)
        for col in range(13):
            net = rows[NET_INCOME].get(col, Decimal(0))
            dep = rows[DEPRECIATION].get(col, Decimal(0))
            adj = rows[ADJUSTED].get(col, Decimal(0))
            if fy == "FY26":
                built = net + dep + rows[DISPOSAL].get(col, Decimal(0))
            else:
                built = (rows[EBITDA].get(col, Decimal(0))
                         + rows[DERIVATIVES].get(col, Decimal(0))
                         + rows[BARGAIN].get(col, Decimal(0)))
            if adj != built:
                found.append(f"V1|{fy}|col{col}|delta={adj - built}")
        for label, cells in rows.items():
            g = lambda i: cells.get(i, Decimal(0))
            for name, built, printed in (
                ("mining", g(0) + g(1), g(MINING_TOTAL)),
                ("tailings", g(3) + g(4) + g(5) + g(6), g(TAILINGS_TOTAL)),
                ("group", g(8) + g(9) + g(10) + g(11), g(GROUP)),
            ):
                if built != printed:
                    found.append(f"H|{fy}|{name}|{label}|delta={printed - built}")

    assert found, "expected the page's 0.1 rounding deviations to be present"
    for fingerprint in found:
        assert abs(Decimal(fingerprint.split("delta=")[1])) <= tol, fingerprint
        recorded = report_db.execute(
            "SELECT COUNT(*) FROM conflicts WHERE check_id = ?", (fingerprint,)).fetchone()[0]
        assert recorded == 1, f"unrecorded rounding deviation: {fingerprint}"


def _apm_row(report_db, fy, label):
    return {c: Decimal(str(v or 0)) for c, v in report_db.execute(
        "SELECT column_index, value_num FROM cells WHERE table_region=? "
        "AND fiscal_year=? AND row_label=?", (REGION, fy, label))}


def _p50_row(report_db, fy):
    return {c: Decimal(str(v or 0)) for c, v in report_db.execute(
        "SELECT column_index, value_num FROM cells WHERE physical_page=50 "
        "AND row_label='Adjusted EBITDA US$' AND fiscal_year=?", (fy,))}


@pytest.mark.parametrize("fy,expected_diffs", [
    ("FY26", {0}),                      # Barberton mining only: 142.5 vs 142.4
    ("FY25", {0, 1, 8, 9}),             # 71.1/71.0, 16.2/16.3, 93.9/93.8, 97.7/97.8
])
def test_x1_apm_versus_d009_p50(report_db, fy, expected_diffs):
    """The APM table and D009 p.50 agree cell-by-cell except at the recorded 0.1 cells.

    This is the code verification of the finding that the D009 0.1 EBITDA residual comes
    from p.45 printing 142.5 where p.50 prints 142.4. Both values stay in the database.
    """
    apm = _apm_row(report_db, fy, ADJUSTED)
    p50 = _p50_row(report_db, fy)
    diffs = set()
    for a_col, p_col in enumerate(P50):
        if apm.get(a_col, Decimal(0)) != p50.get(p_col, Decimal(0)):
            diffs.add(a_col)
    assert diffs == expected_diffs, f"{fy} differing columns {sorted(diffs)} != {sorted(expected_diffs)}"

    # Group total agrees in both tables
    assert apm[GROUP] == p50[13]


def test_x1_resolves_the_d009_leaf_sum_gap(report_db):
    """p.50's printed leaves sum to 663.0 because its Barberton cell prints 142.4.

    Substituting the APM table's printed 142.5 (same cell, same period, other page) makes
    the D009 leaves reach the D009 printed Group total exactly. This is recorded as
    conditional: the anchor is a printed figure from another table, not a correction.
    """
    p50 = _p50_row(report_db, "FY26")
    leaves = [p50[c] for c in (0, 1, 3, 5, 6, 7)]
    assert sum(leaves) == Decimal("663.0")          # printed leaves, as printed
    assert p50[13] == Decimal("663.1")              # printed group total

    apm = _apm_row(report_db, "FY26", ADJUSTED)
    substituted = sum(leaves) - p50[0] + apm[0]     # 142.4 -> 142.5
    assert substituted == p50[13]                   # conditional agreement only
