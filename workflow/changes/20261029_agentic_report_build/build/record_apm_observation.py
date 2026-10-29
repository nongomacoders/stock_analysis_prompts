"""Record the p.45 vs p.50 Barberton EBITDA difference as a conflict.

VERIFIED IN CODE by tests_reconcile/test_apm_ebitda.py::test_x1_apm_versus_d009_p50
after the p.45 grid was extracted (130 cells, extraction p1_apm_ebitda_v2).
Recorded as conditional agreement only: 142.5 is a printed figure from another table on
another page, not a correction of p.50's 142.4.
"""
from __future__ import annotations

import pathlib
import sqlite3

DB = pathlib.Path(__file__).resolve().parent.parent / "build" / "report.sqlite"

CHECK_ID = "APM_EBITDA_BARBERTON|p45|Adjusted EBITDA|FY26|col0|delta=0.1"

DESCRIPTION = (
    "VERIFIED IN CODE (test_x1_apm_versus_d009_p50). Physical p.45 APM reconciliation "
    "prints the FY26 Adjusted EBITDA row as 142.5, 120.9, 263.4, 29.4, 171.4, 155.9, 43.0, "
    "399.7, 171.9, 292.3, 155.9, 43.0, 663.1; physical p.50 Group production summary prints "
    "Barberton mining at 142.4 with every other cell and Group total 663.1 identical. p.45 "
    "is internally consistent on its own terms (131.1 net income + 11.4 mining D&A = 142.5) "
    "and its leaves sum to 663.1, while p.50's printed leaves sum to 663.0 against its own "
    "printed 663.1. This is the root cause of the 0.1 EBITDA residual carried open since "
    "D009 P2: a two-table rounding-boundary difference, proved cell-by-cell in code. "
    "Recorded as conditional agreement only - 142.5 is a printed figure from another table, "
    "never a correction of p.50. No printed value replaced."
)


def main():
    con = sqlite3.connect(str(DB))
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM conflicts WHERE check_id = ?", (CHECK_ID,))
        cur.execute(
            """INSERT INTO conflicts (check_id, description, kind, physical_page,
               evidence_path, ledger_question_id, status)
               VALUES (?, ?, 'ambiguity', 45, ?, ?, 'open')""",
            (CHECK_ID, DESCRIPTION, "tests_reconcile/test_apm_ebitda.py", "Q-c1e6100f7a674873"))
        con.commit()
        print("conflicts:", con.execute("SELECT COUNT(*) FROM conflicts").fetchone()[0])
        print("cells:", con.execute("SELECT COUNT(*) FROM cells").fetchone()[0])
    finally:
        con.close()


if __name__ == "__main__":
    main()
