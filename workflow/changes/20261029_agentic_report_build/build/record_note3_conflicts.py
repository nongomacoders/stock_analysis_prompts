"""Record Note 3 (Segment Analysis) ambiguity conflicts into report.sqlite.

Both rows are recorded as `ambiguity` (measured scope/structuring differences),
never as corrections: the printed figures stay untouched (CHARTER covenant 1).
"""
from __future__ import annotations

import json
import pathlib
import sqlite3

DB = pathlib.Path(__file__).resolve().parent.parent / "build" / "report.sqlite"

CONFLICTS = [
    dict(
        check_id="N3_APM_SCOPE|p22|Adjusted EBITDA|FY26|delta=53.669",
        kind="ambiguity",
        physical_page=22,
        ledger_question_id="Q-c1e6100f7a674873",
        description=(
            "Adjusted EBITDA is printed twice with different scope: Note 3 p.22 Group total "
            "609,431 US$ thousand (US$609.4m) versus Group production summary p.50 "
            "663.1 US$m (delta US$53.669m). Note 3 reconciles operating profit 545,838 + "
            "D&A 60,288 + other D&A 2,179 = EBITDA 608,305, then +781 disposal loss +345 "
            "impairment = 609,431, i.e. it carries the Corporate (-52,429) and Funding (-231) "
            "columns. The p.50 figure is the operating-segment measure. Neither printed value "
            "is replaced; the scope difference is recorded and the APM definition question "
            "stays open."
        ),
    ),
    dict(
        check_id="N3_INTRA_GROUP|p21|Revenue|FY26|separate_block",
        kind="ambiguity",
        physical_page=21,
        ledger_question_id="Q-a0b503d7ac044eee",
        description=(
            "p.21/p.23 print a second, differently-structured block below the segment table "
            "('Revenue ... excluding intra-Group transactions', 'Cost of production', "
            "'Elimination of dividends received from/(paid to) fellow Group companies'). "
            "Its columns are not the segment columns, so it is extracted into the separate "
            "region note3_intra_group and is excluded from the segment horizontal identities. "
            "Printed values preserved verbatim; grouping left open for the segment note review."
        ),
    ),
]


def main():
    con = sqlite3.connect(str(DB))
    try:
        cur = con.cursor()
        cur.executemany(
            """INSERT INTO conflicts (check_id, description, kind, physical_page,
               evidence_path, ledger_question_id, status)
               VALUES (:check_id, :description, :kind, :physical_page,
                       'extract_pan_note3_segments.py', :ledger_question_id, 'open')""",
            CONFLICTS)
        con.commit()
        receipt = {
            "note3_cells": con.execute(
                "SELECT COUNT(*) FROM cells WHERE table_region LIKE 'note3_%'").fetchone()[0],
            "note3_rows": con.execute(
                "SELECT COUNT(*) FROM (SELECT 1 FROM cells WHERE table_region='note3_segment_analysis' "
                "GROUP BY physical_page, fiscal_year, row_index)").fetchone()[0],
            "note3_by_page": dict(con.execute(
                "SELECT physical_page, COUNT(*) FROM cells WHERE table_region LIKE 'note3_%' "
                "GROUP BY physical_page").fetchall()),
            "total_cells": con.execute("SELECT COUNT(*) FROM cells").fetchone()[0],
            "total_conflicts": con.execute("SELECT COUNT(*) FROM conflicts").fetchone()[0],
            "note3_conflicts": con.execute(
                "SELECT COUNT(*) FROM conflicts WHERE check_id LIKE 'N3_%'").fetchone()[0],
        }
        print(json.dumps(receipt, indent=2))
        out = pathlib.Path(__file__).resolve().parent.parent / "build" / "receipts_note3_p1.json"
        out.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    finally:
        con.close()


if __name__ == "__main__":
    main()
