"""All-in cost reconciliations (PAN pp.40-43): AISC and AIC builds.

Two US$ million tables (FY26 p.40, FY25 p.41) and two unit tables (p.42, p.43).
Checks the definition chain: cash cost = gold cost of production; AISC = cash cost plus
the sustaining items; AIC = AISC plus the growth items. Printed cells only.
"""
from __future__ import annotations

from decimal import Decimal

import pytest

FY26 = "apm_aisc_fy26_usd"
FY25 = "apm_aisc_fy25_usd"
UNIT26 = "apm_aisc_fy26_unit"
UNIT25 = "apm_aisc_fy25_unit"

SUSTAINING = [
    "Royalties",
    "Community cost related to gold operations",
    "By-products credits",
    "Corporate general and administrative costs",
    "Reclamation and remediation – accretion and amortisation (operating sites)",
    "Sustaining capital – development",
    "Sustaining capital – maintenance",
]


def _rows(report_db, region):
    out = {}
    for ri, label, col, num in report_db.execute(
            "SELECT row_index, row_label, column_index, value_num FROM cells "
            "WHERE table_region=? ORDER BY row_index, column_index", (region,)):
        out.setdefault(label, {})[col] = Decimal(str(num or 0))
    return out


def _get(rows, label, col=12):
    assert label in rows, f"missing row '{label}'"
    return rows[label].get(col, Decimal(0))


@pytest.mark.parametrize("region", [FY26, FY25], ids=["FY26", "FY25"])
def test_cash_cost_equals_gold_cost_of_production(report_db, region):
    """The table's first two lines are the same measure, per the definition text."""
    rows = _rows(report_db, region)
    for col in range(13):
        assert _get(rows, "Cash cost", col) == _get(rows, "Gold cost of production", col), col


@pytest.mark.parametrize("region", [FY26, FY25], ids=["FY26", "FY25"])
def test_aisc_build(report_db, region):
    """AISC = cash cost + royalties + community + by-products + corporate + reclamation
    + sustaining capital (development and maintenance).

    FY26 misses by 0.1 (508.5 built vs 508.4 printed), a single-decimal artefact recorded
    in `conflicts`; FY25 ties exactly. The deviation set is asserted so nothing else drifts.
    """
    rows = _rows(report_db, region)
    deviations = {}
    for col in range(13):
        built = _get(rows, "Cash cost", col) + sum(_get(rows, lab, col) for lab in SUSTAINING)
        printed = _get(rows, "All-in sustaining costs", col)
        if built != printed:
            deviations[col] = printed - built
    if region == FY26:
        assert deviations == {0: Decimal("-0.1"), 2: Decimal("-0.1"),
                              8: Decimal("-0.1"), 12: Decimal("-0.1")}, deviations
    else:
        assert deviations == {}, deviations


@pytest.mark.parametrize("region", [FY26, FY25], ids=["FY26", "FY25"])
def test_aic_build(report_db, region):
    """AIC = AISC + voluntary severance (when printed) + expansion capital."""
    rows = _rows(report_db, region)
    severance = ("Voluntary severance package/retrenchment (non-sustaining)"
                 if region == FY25 else None)
    deviations = {}
    for col in range(13):
        built = _get(rows, "All-in sustaining costs", col) + _get(rows, "Expansion capital – capital expenditure", col)
        if severance:
            built += _get(rows, severance, col)
        printed = _get(rows, "All-in costs", col)
        if built != printed:
            deviations[col] = printed - built
    if region == FY26:
        assert deviations == {3: Decimal("-0.1"), 8: Decimal("-0.1")}, deviations
    else:
        assert deviations == {}, deviations


def test_group_gold_sold_ties_d009(report_db):
    """Group gold sold in the unit table ties the D009 p.49 'Gold sold - total' row.

    FY26 ties exactly (272,373 oz). FY25 prints 196,927 oz on p.43 against 196,926 oz on
    D009 p.49 - a one-ounce difference between two tables in the same document for the same
    measure. It is asserted here rather than smoothed, and recorded in `conflicts`.
    """
    expected = {"FY26": (Decimal("272373"), Decimal("272373")),
                "FY25": (Decimal("196927"), Decimal("196926"))}
    for fy, region in (("FY26", UNIT26), ("FY25", UNIT25)):
        row = report_db.execute(
            "SELECT value_num FROM cells WHERE table_region=? AND row_label='Gold sold' "
            "AND unit='oz' AND column_index=12", (region,)).fetchone()
        assert row is not None, f"no group oz gold sold row in {region}"
        group_oz = Decimal(str(row[0]))
        d009 = Decimal(str(report_db.execute(
            "SELECT value_num FROM cells WHERE physical_page=49 AND row_label='Gold sold – total' "
            "AND fiscal_year=? AND column_index=13", (fy,)).fetchone()[0]))
        assert (group_oz, d009) == expected[fy], f"{fy}: {group_oz} vs {d009}"
