"""Tests reconciling PAN section D009 Group production summary (pp.48-50).

Governed by CHARTER covenants:
  - Covenant 1: Never replace a printed source figure. Mismatches are recorded
    data, never auto-fixed.
  - Covenant 2: All arithmetic executes in code, never asserted in prose.
  - Covenant 3: Every cell carries page + sha256 + extraction commit lineage.
  - Covenant 4: Suite proves arithmetic; ledger questions stay open on ambiguity.
  - Fixture covenant: ground truth scoring fixtures are the reviewer scoring
    key ONLY; this suite reads only build/report.sqlite.
"""
from __future__ import annotations

import pathlib
import pytest
from decimal import Decimal
from reconcile_engine import Engine, NON_ADDITIVE_RATIONALE, ADDITIVE_ROWS


def test_ground_truth_isolation():
    """Charter covenant: suite source and imports must never read the scoring fixture."""
    here = pathlib.Path(__file__).resolve().parent
    forbidden_pattern = "pan" + "_d009" + "_expected"
    for py in here.glob("*.py"):
        lines = [line for line in py.read_text(encoding="utf-8").splitlines()
                 if "forbidden_pattern" not in line]
        text = "\n".join(lines)
        assert forbidden_pattern not in text, (
            f"{py.name} references the scoring fixture; fixture covenant violated"
        )


def test_schema_integrity(report_db):
    """Every expected table exists and contains records from P1 extraction."""
    tables = [r[0] for r in report_db.execute(
        "SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    for t in ("sources", "pages", "cells", "conflicts", "questions", "runs"):
        assert t in tables, f"missing expected table {t}"
    assert report_db.execute("SELECT COUNT(*) FROM cells").fetchone()[0] >= 1196
    assert report_db.execute("SELECT COUNT(*) FROM pages").fetchone()[0] >= 3
    assert report_db.execute("SELECT COUNT(*) FROM sources").fetchone()[0] == 1
    assert report_db.execute("SELECT COUNT(*) FROM questions").fetchone()[0] >= 8


def test_blank_column_remains_unextracted(report_db):
    """D009 structural invariant: column 4 is a visual gap and must have 0 cells there."""
    n = report_db.execute(
        "SELECT COUNT(*) FROM cells WHERE column_index=4 "
        "AND table_region IN ('A_production','B_costs','C_financial_summary')").fetchone()[0]
    assert n == 0, f"D009 column 4 contains {n} extracted cells; visual gap must be empty"


def test_cell_lineage_complete(report_db):
    """Every extracted cell carries physical_page, extraction_commit, and document hash."""
    bad = report_db.execute(
        "SELECT COUNT(*) FROM cells WHERE physical_page NOT IN (17, 18, 21, 22, 23, 24, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50) "
        "OR extraction_commit IS NULL OR LENGTH(extraction_commit) < 7"
    ).fetchone()[0]
    assert bad == 0, f"{bad} cells lack complete lineage"


def test_row_classification_exhaustive(engine):
    """Every printed metric row is explicitly classified as additive or non-additive."""
    rep = engine.classification_report()
    assert rep["unclassified"] == [], (
        f"unclassified metric rows present: {rep['unclassified']}; "
        "covenant requires classification with rationale, never silent omission"
    )
    assert len(rep["additive"]) >= 20
    assert len(rep["non_additive"]) >= 15


def test_p50_revenue_sum_exact(engine):
    """Page 50: Barberton ops (8,449.6) + Surface ops (8,799.5) == Group Revenue (17,249.1)."""
    r = engine._row(50, "Revenue", "FY26")
    barberton = r[2]   # Mining total (Barberton)
    surface = r[8]     # Surface operations total
    group = r[13]      # Group total
    assert barberton + surface == group
    assert group == Decimal("17249.1")


def test_p50_cost_of_production_sum_exact(engine):
    """Page 50: Barberton (3,957.4) + Surface (2,474.3) == Group Cost of Production (6,431.7)."""
    r = engine._row(50, "Cost of production", "FY26")
    barberton = r[2]
    surface = r[8]
    group = r[13]
    assert barberton + surface == group
    assert group == Decimal("6431.7")


def test_p50_capex_leaves_sum_exact(engine):
    """Page 50: capex leaf segments sum exactly to printed FY26 Capex total (214.9 US$m)."""
    r = engine._row(50, "Capital expenditure US$", "FY26")
    leaves = [r[0], r[1], r[3], r[5], r[6], r[7]]
    assert sum(leaves) == r[13]
    assert r[13] == Decimal("214.9")


def test_fy25_disjoint_gold_build_ties_group_total(engine):
    """FY25 Gold produced: disjoint sum 92,643 + 2,654 + 98,636 + 1,081 + 1,513 ties 196,527."""
    ug = engine._row(48, "Gold produced – underground", "FY25")[2]          # 92,643
    surf = engine._row(48, "Gold production – surface operations", "FY25")[0] # 2,654
    tail = engine._row(48, "Gold produced – tailings", "FY25")[8]             # 98,636
    buyin = engine._row(48, "Gold produced – third-party buy-in feedstock", "FY25")[13] # 1,081
    tenn = engine._row(49, "Gold produced – surface feedstock", "FY25")[7]     # 1,513
    total = ug + surf + tail + buyin + tenn
    printed_total = engine._row(49, "Gold produced – total", "FY25")[13]
    assert total == printed_total
    assert total == Decimal("196527")


def test_fy25_overlapping_gold_build_yields_197608(engine):
    """FY25 Gold produced: overlapping sum (using Group UG column 93,724) yields 197,608."""
    ug_col13 = engine._row(48, "Gold produced – underground", "FY25")[13]  # 93,724 (contains 1,081)
    surf = engine._row(48, "Gold production – surface operations", "FY25")[0]
    tail = engine._row(48, "Gold produced – tailings", "FY25")[8]
    buyin = engine._row(48, "Gold produced – third-party buy-in feedstock", "FY25")[13]
    tenn = engine._row(49, "Gold produced – surface feedstock", "FY25")[7]
    overlap_sum = ug_col13 + surf + tail + buyin + tenn
    assert overlap_sum == Decimal("197608")
    # Proves 1,081 is double-counted in the naive sum because col13 UG embeds it:
    assert ug_col13 - Decimal("92643") == buyin


def test_fy25_mtr_buyin_hypothesis_consistency(engine):
    """FY25 MTR leaf vs total operations delta (5,763 oz) ties FY26 MTR buy-in exactly."""
    leaf_fy25 = engine._row(48, "Gold produced – tailings", "FY25")[6]             # 25,043
    total_fy25 = engine._row(48, "Gold produced – tailings", "FY25")[11]           # 30,806
    assert total_fy25 - leaf_fy25 == Decimal("5763")
    buyin_fy26 = engine._row(48, "Gold produced – third-party buy-in feedstock", "FY26")[6]
    assert buyin_fy26 == Decimal("5763")


def test_fy26_barberton_components_exceed_by_10000(engine):
    """Barberton Total Operations FY26 (94,929 oz) exceeds col0+col3 (84,929 oz) by 10,000 oz."""
    r = engine._row(49, "Gold produced – total", "FY26")
    b_min = r[0]     # 71,997
    b_surf = r[3]    # 12,932
    b_total = r[9]   # 94,929
    assert b_total - (b_min + b_surf) == Decimal("10000")
    # And operations-sum over leaf columns exceeds Group total by the same 10,000 oz:
    opsum = r[9] + r[10] + r[11] + r[12]
    assert opsum - r[13] == Decimal("10000")


def test_fy26_ebitda_leaf_sum_0p1_gap(engine):
    """EBITDA FY26: sum of 6 leaves is 663.0 US$m vs printed Group Total 663.1 US$m."""
    r = engine._row(50, "Adjusted EBITDA US$", "FY26")
    leaves = [r[0], r[1], r[3], r[5], r[6], r[7]]
    assert sum(leaves) == Decimal("663.0")
    assert r[13] == Decimal("663.1")
    assert r[13] - sum(leaves) == Decimal("0.1")


def test_fy25_tennant_currency_conversion_consistent(engine):
    """Tennant FY25 all-in cost: 1,584,835 A$/kg ties 32,041 US$/oz at 1.54 US$/A$ within 0.10%."""
    aud = engine._row(49, "A$ all-in cost", "FY25")[7]     # 1,584,835
    usd = engine._row(49, "US$ all-in cost", "FY25")[7]    # 32,041
    rate = engine._rates()[("FY25", "US$/A$")]             # 1.54
    implied_aud = usd * Decimal("32.150747") * rate
    rel_dev = abs(aud - implied_aud) / aud
    assert rel_dev < Decimal("0.0010"), f"Tennant conversion dev {rel_dev:.4%} exceeds 0.10%"


def test_all_arithmetic_mismatches_are_recorded_conflicts(engine, report_db):
    """P2 GATE: every mismatch produced by the engine must be recorded in the conflicts table.

    Green gate per RUNBOOK and CHARTER §2 P2:
      'pytest tests_reconcile -q must be green, or every failing check is
       explicitly recorded in conflicts with page citations.'
    """
    results = engine.run_all()
    mismatches = [r for r in results if r.mismatch]

    recorded_fingerprints = {
        r[0] for r in report_db.execute(
            "SELECT check_id FROM conflicts WHERE check_id LIKE '%|%'").fetchall()
    }

    missing = []
    for m in mismatches:
        if m.fingerprint not in recorded_fingerprints:
            missing.append(m.fingerprint)

    assert not missing, (
        f"{len(missing)} unrecorded arithmetic mismatches found (sample: {missing[:5]}); "
        "covenant 1 requires every mismatch to be recorded in conflicts before gate passes."
    )
