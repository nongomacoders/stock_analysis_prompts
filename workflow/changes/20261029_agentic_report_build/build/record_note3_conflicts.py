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
        check_id="N3_APM_SCOPE|p22|Adjusted EBITDA|FY26|delta=53.670",
        kind="ambiguity",
        physical_page=22,
        ledger_question_id="Q-c1e6100f7a674873",
        description=(
            "Adjusted EBITDA prints at two scopes. Note 3 p.22 Group total = 609,431 US$k; "
            "Group production summary p.50 = 663.1 US$m. Bridge proved in code: the D009 figure "
            "equals Note 3 operating segments only (Barberton 171,874 + Evander 292,316 + "
            "MTR 155,899 + Tennant 43,012 = 663,101 -> 663.1), i.e. it excludes Solar (-988), "
            "Exploration (-222), ESG (-345), Corporate (-51,884) and Funding (-231), which sum "
            "to -53,670. FY25 reproduces identically (93,798 + 97,761 + 51,763 + 2,443 = "
            "245,765 -> 245.8 vs Note 3 Group 226,584). This also closes the 0.1 residual left "
            "open at D009 P2: the p.50 Group total is the sum of unrounded segment figures while "
            "the printed p.50 leaves are each rounded to one decimal. Neither printed value is "
            "replaced; the APM definition question stays open."
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
        cur.execute("DELETE FROM conflicts WHERE check_id LIKE 'N3_%'")
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
