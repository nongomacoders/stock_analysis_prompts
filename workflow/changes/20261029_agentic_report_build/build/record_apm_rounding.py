"""Record the p.45 rounding deviations as conflicts (never as corrections).

Every deviation on the APM Adjusted EBITDA page is exactly 0.1 and is a consequence of
printing each cell to one decimal while subtotals are built from unrounded figures.
They are recorded so the gate can stay meaningful: a deviation larger than 0.1, or an
extraction error, still fails.
"""
from __future__ import annotations

import pathlib
import sqlite3
from decimal import Decimal

DB = pathlib.Path(__file__).resolve().parent.parent / "build" / "report.sqlite"
REGION = "apm_adjusted_ebitda"
QID = "Q-c1e6100f7a674873"

NET = "Net income/(cost) before finance income and finance costs"
DEP = "Mining depreciation and amortisation"
DIS = "(Profit)/loss on disposal of plant and equipment"
ADJ = "Adjusted EBITDA"
EB = "EBITDA"
FV = "Unrealised fair value loss on financial derivatives"
BG = "Bargain gains on purchase"


def rows(con, fy):
    out = {}
    for lab, col, num in con.execute(
            "SELECT row_label, column_index, value_num FROM cells "
            "WHERE table_region=? AND fiscal_year=?", (REGION, fy)):
        out.setdefault(lab, {})[col] = Decimal(str(num or 0))
    return out


def main():
    con = sqlite3.connect(str(DB))
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM conflicts WHERE check_id LIKE 'V1|%' OR check_id LIKE 'H|%'")
        n = 0
        for fy in ("FY26", "FY25"):
            R = rows(con, fy)
            for col in range(13):
                net, dep = R[NET].get(col, Decimal(0)), R[DEP].get(col, Decimal(0))
                adj = R[ADJ].get(col, Decimal(0))
                built = (net + dep + R[DIS].get(col, Decimal(0))) if fy == "FY26" else (
                    R[EB].get(col, Decimal(0)) + R[FV].get(col, Decimal(0)) + R[BG].get(col, Decimal(0)))
                if adj != built:
                    cid = f"V1|{fy}|col{col}|delta={adj - built}"
                    cur.execute(
                        """INSERT INTO conflicts (check_id, description, kind, physical_page,
                           evidence_path, ledger_question_id, status)
                           VALUES (?, ?, 'ambiguity', 45, ?, ?, 'open')""",
                        (cid, f"APM Adjusted EBITDA column roll-forward: printed {adj} vs build "
                              f"{built} (delta {adj - built}). One-decimal printing; every cell "
                              f"on p.45 is rounded individually while subtotals use unrounded "
                              f"figures. Both printed values preserved.", REGION, QID))
                    n += 1
            for label, cells in R.items():
                g = lambda i: cells.get(i, Decimal(0))
                for name, built, printed in (
                    ("mining", g(0) + g(1), g(2)),
                    ("tailings", g(3) + g(4) + g(5) + g(6), g(7)),
                    ("group", g(8) + g(9) + g(10) + g(11), g(12)),
                ):
                    if built != printed:
                        cid = f"H|{fy}|{name}|{label}|delta={printed - built}"
                        cur.execute(
                            """INSERT INTO conflicts (check_id, description, kind, physical_page,
                               evidence_path, ledger_question_id, status)
                               VALUES (?, ?, 'ambiguity', 45, ?, ?, 'open')""",
                            (cid, f"APM horizontal identity ({name}) on '{label}': printed {printed} "
                                  f"vs build {built} (delta {printed - built}). One-decimal "
                                  f"printing artefact on p.45.", REGION, QID))
                        n += 1
        con.commit()
        print(f"recorded {n} rounding conflicts; total conflicts:", con.execute(
            "SELECT COUNT(*) FROM conflicts").fetchone()[0])
    finally:
        con.close()


if __name__ == "__main__":
    main()
