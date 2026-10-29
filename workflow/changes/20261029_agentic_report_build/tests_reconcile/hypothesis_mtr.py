"""Hypothesis evaluation: MTR FY25 leaf vs Total Operations delta (5,763 oz).

CHARTER COVENANT 1:
  "Never replace a printed source figure. Conflicts are data (conflicts table + ledger),
   not bugs to fix."

Hypothesis A (Embedded Buy-in):
  The delta between FY25 MTR leaf tailings (25,043 oz, col6) and MTR Total Operations
  (30,806 oz, col11) is exactly 5,763 oz.
  In FY26, MTR third-party buy-in feedstock is printed as 5,763 oz (col6 and col11).
  In FY25, MTR third-party buy-in feedstock prints as nil ('–') in col6 and col11.
  Does 25,043 + 5,763 == 30,806?
  Does this arithmetic tie prove valid closure of ledger question Q-3e8730dbd1994205?
"""
from __future__ import annotations

import pathlib
import sys
from decimal import Decimal

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here.parent / "tests_reconcile"))
from reconcile_engine import Engine

DB_PATH = here.parent / "build" / "report.sqlite"


def evaluate_mtr_hypothesis():
    eng = Engine(str(DB_PATH))

    # Page 48 Gold produced – tailings
    leaf_fy25 = eng._row(48, "Gold produced – tailings", "FY25")[6]   # 25,043 oz
    total_fy25 = eng._row(48, "Gold produced – tailings", "FY25")[11] # 30,806 oz
    delta_fy25 = total_fy25 - leaf_fy25                                # 5,763 oz

    # Page 48 Gold produced – third-party buy-in feedstock
    buyin_fy25_col6 = eng._row(48, "Gold produced – third-party buy-in feedstock", "FY25")[6]   # None / nil
    buyin_fy25_col11 = eng._row(48, "Gold produced – third-party buy-in feedstock", "FY25")[11] # None / nil
    buyin_fy26_col6 = eng._row(48, "Gold produced – third-party buy-in feedstock", "FY26")[6]   # 5,763 oz
    buyin_fy26_col11 = eng._row(48, "Gold produced – third-party buy-in feedstock", "FY26")[11] # 5,763 oz

    # Tailings row horizontal sum check
    # col8 (Total surface ops tailings) = col3 (15,224) + col5 (52,606) + col6 (25,043) = 92,873 vs printed 98,636
    # 98,636 - 92,873 = 5,763
    printed_tailings_surface_total = eng._row(48, "Gold produced – tailings", "FY25")[8] # 98,636
    component_tailings_sum = (eng._row(48, "Gold produced – tailings", "FY25")[3] +
                              eng._row(48, "Gold produced – tailings", "FY25")[5] +
                              leaf_fy25) # 15,224 + 52,606 + 25,043 = 92,873
    delta_tailings_total = printed_tailings_surface_total - component_tailings_sum # 5,763

    ties_arithmetic = (leaf_fy25 + delta_fy25 == total_fy25) and (delta_fy25 == buyin_fy26_col6)
    ties_surface_total = (component_tailings_sum + delta_fy25 == printed_tailings_surface_total)

    result = {
        "mtr_leaf_fy25": str(leaf_fy25),
        "mtr_total_ops_fy25": str(total_fy25),
        "mtr_gap_fy25": str(delta_fy25),
        "buyin_printed_fy25": str(buyin_fy25_col6),
        "buyin_printed_fy26": str(buyin_fy26_col6),
        "arithmetic_decomposition_ties": ties_arithmetic,
        "tailings_surface_total_ties_with_delta": ties_surface_total,
        "covenant_verdict": (
            "ARITHMETIC CONSISTENCY PROVED, BUT CAUSAL CLOSURE UNPROVED. "
            "The 5,763 oz gap exactly matches the FY26 MTR buy-in figure and accounts for the "
            "difference between component tailings sum (92,873 oz) and printed total (98,636 oz). "
            "However, Pan African's text does not confirm whether FY25 had 5,763 oz buy-in mistakenly "
            "printed under Total Operations or whether FY26 buy-in was retroactively shifted. "
            "Per Covenant 4 and prior review corrections, this ledger question Q-3e8730dbd1994205 remains OPEN."
        ),
    }
    return result


if __name__ == "__main__":
    res = evaluate_mtr_hypothesis()
    for k, v in res.items():
        print(f"{k}: {v}")
