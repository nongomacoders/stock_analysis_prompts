"""Record the APM (p.45) observation as an open ambiguity conflict.

The p.45 Adjusted EBITDA grid is NOT extracted yet (see WORKPLAN_APM.md). This row
therefore records an observation from the PDF text layer, explicitly flagged as
not code-verified, so that nothing is claimed as proved before the extractor exists.
"""
from __future__ import annotations

import pathlib
import sqlite3

DB = pathlib.Path(__file__).resolve().parent.parent / "build" / "report.sqlite"

CHECK_ID = "APM_EBITDA_BARBERTON|p45|Adjusted EBITDA|FY26|col0|delta=0.1"

DESCRIPTION = (
    "Printed cross-table difference, NOT yet code-verified (p.45 grid not extracted; "
    "see WORKPLAN_APM.md). Physical p.45 APM reconciliation prints the FY26 Adjusted "
    "EBITDA row as 142.5, 120.9, 263.4, 29.4, 171.4, 155.9, 43.0, 399.7, 171.9, 292.3, "
    "155.9, 43.0, 663.1; physical p.50 Group production summary prints the same row with "
    "Barberton mining at 142.4. Every other cell and the Group total 663.1 agree. Each "
    "table is internally consistent on its own terms (p.45: 131.1 net income + 11.4 "
    "mining D&A = 142.5 and its leaves sum to 663.1; p.50: printed leaves sum to 663.0 "
    "against its own printed 663.1). This is the probable root cause of the 0.1 EBITDA "
    "residual carried open since D009 P2, but it stays open until an extractor "
    "reproduces the p.45 row in code. No printed value replaced."
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
            (CHECK_ID, DESCRIPTION, "WORKPLAN_APM.md (P0, extraction deferred)",
             "Q-c1e6100f7a674873"))
        con.commit()
        print("conflicts:", con.execute("SELECT COUNT(*) FROM conflicts").fetchone()[0])
        print("cells:", con.execute("SELECT COUNT(*) FROM cells").fetchone()[0])
    finally:
        con.close()


if __name__ == "__main__":
    main()
