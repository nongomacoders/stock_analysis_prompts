"""Note 20 continuation (PAN physical page 37): financial instruments.

Same treatment as p.28 - longest trailing run of value tokens per line, no modal-width
filter (that filter is what discarded the p.28 balance rows).
"""
from __future__ import annotations

import pathlib
import re
import sqlite3
import sys

DB_PATH = pathlib.Path(__file__).resolve().parent.parent / "report.sqlite"
PDF_PATH = pathlib.Path(
    r"companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")
EXPECTED_SHA = "62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd"
EXTRACTION_COMMIT = "p1_note20_p37_v1"
PAGE = 37
REGION = "note_p37"
MIN_RUN = 2

VALUE_RE = re.compile(r"\(?[\d,]+(?:\.\d+)?\)?|[–—\-]")
DASH_RE = re.compile(r"^[–—\-]$")


def text_lines():
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(PDF_PATH))
    try:
        raw = doc[PAGE - 1].get_textpage().get_text_range()
    finally:
        doc.close()
    return [ln.strip() for ln in raw.splitlines() if ln.strip()]


def longest_run(raw):
    tokens = raw.split()
    for k in range(len(tokens)):
        rest = tokens[k:]
        if len(rest) < MIN_RUN or not all(VALUE_RE.fullmatch(t) for t in rest):
            continue
        label = " ".join(tokens[:k]).strip()
        while rest and re.fullmatch(r"20\d{2}", rest[0]):
            label = f"{label} {rest[0]}".strip()
            rest = rest[1:]
        if len(rest) < MIN_RUN or not label or label.endswith(","):
            continue
        return label, rest
    return None


def run():
    rows = []
    for raw in text_lines():
        parsed = longest_run(raw)
        if parsed and not raw.startswith(("NOTES", "for the year", "PAN AFRICAN", "Summarised")):
            rows.append(parsed)
    print(f"p{PAGE}: {len(rows)} rows", file=sys.stderr)
    for label, values in rows:
        print(f"  {label[:58]:<58} n={len(values):>2} " + " ".join(values[:3]))
    if not rows:
        print("nothing parsed - leaving region absent", file=sys.stderr)
        return

    con = sqlite3.connect(str(DB_PATH))
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM cells WHERE table_region = ?", (REGION,))
        n = 0
        for idx, (label, values) in enumerate(rows, start=1):
            for col, raw in enumerate(values):
                val = None
                if not DASH_RE.match(raw):
                    s = raw.replace(",", "")
                    val = -float(s[1:-1]) if s.startswith("(") else float(s)
                cur.execute(
                    """INSERT INTO cells (document, physical_page, table_region, row_label,
                       fiscal_year, unit, column_label, column_index, value_raw, value_num,
                       row_index, extraction_commit)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (EXPECTED_SHA, PAGE, REGION, label, None, "US$ thousand",
                     f"col{col}", col, raw, val, idx, EXTRACTION_COMMIT))
                n += 1
        con.commit()
        print(f"Inserted {n} cells. Total in DB: "
              f"{con.execute('SELECT COUNT(*) FROM cells').fetchone()[0]}")
    finally:
        con.close()


if __name__ == "__main__":
    run()
