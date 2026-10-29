"""Hypothesis evaluation: Barberton Total Operations FY26 printed value.

CHARTER COVENANT 1:
  "Never replace a printed source figure. Conflicts are data (conflicts table + ledger),
   not bugs to fix. Conditional agreement (e.g. substituting 84,929 makes a PAN opsum tie
   exactly) is recorded as a hypothesis with its conditional check, never as a correction
   — this is the documented 2026-10-29 trap."

Hypothesis A (Conditional Substitution):
  If the printed Barberton Total Operations gold produced (94,929 oz, col9) was 84,929 oz
  (matching component sum 71,997 + 12,932 oz), does the leaf-column operations sum tie
  the printed Group total (272,310 oz)?

Hypothesis B (Disjoint Component Interpretation):
  Does the 10,000 oz represent an omitted surface/tailings contribution not shown in col0 or col3,
  or an independent rounding/accounting adjustment?
"""
from __future__ import annotations

import pathlib
import sys
from decimal import Decimal

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here.parent / "tests_reconcile"))
from reconcile_engine import Engine

DB_PATH = here.parent / "build" / "report.sqlite"


def evaluate_barberton_hypothesis():
    eng = Engine(str(DB_PATH))
    r = eng._row(49, "Gold produced – total", "FY26")

    col0_barberton_min = r[0]   # 71,997 oz
    col3_btrp_surface = r[3]    # 12,932 oz
    col9_barberton_total = r[9] # 94,929 oz
    col10_evander_total = r[10] # 103,330 oz
    col11_mtr_total = r[11]     # 51,927 oz
    col12_tennant_total = r[12] # 32,124 oz
    col13_group_total = r[13]   # 272,310 oz

    # Baseline printed checks
    component_sum = col0_barberton_min + col3_btrp_surface  # 84,929
    delta_barberton = col9_barberton_total - component_sum   # +10,000

    printed_opsum = col9_barberton_total + col10_evander_total + col11_mtr_total + col12_tennant_total
    delta_opsum = printed_opsum - col13_group_total          # +10,000

    # Conditional substitution check
    hypothetical_b_total = component_sum  # 84,929
    conditional_opsum = hypothetical_b_total + col10_evander_total + col11_mtr_total + col12_tennant_total
    ties_group = (conditional_opsum == col13_group_total)

    result = {
        "printed_barberton_total": str(col9_barberton_total),
        "barberton_components_sum": str(component_sum),
        "barberton_components_delta": str(delta_barberton),
        "printed_opsum": str(printed_opsum),
        "printed_group_total": str(col13_group_total),
        "opsum_delta": str(delta_opsum),
        "conditional_opsum_with_84929": str(conditional_opsum),
        "conditional_agreement_holds": ties_group,
        "covenant_verdict": (
            "CONDITIONAL AGREEMENT ONLY. Substituting 84,929 oz makes opsum tie exactly (272,310 oz), "
            "but under Covenant 1 printed 94,929 oz is preserved in report.sqlite. "
            "Ledger question Q-1f48aa6d4b884f09 remains OPEN."
        ),
    }
    return result


if __name__ == "__main__":
    res = evaluate_barberton_hypothesis()
    for k, v in res.items():
        print(f"{k}: {v}")
