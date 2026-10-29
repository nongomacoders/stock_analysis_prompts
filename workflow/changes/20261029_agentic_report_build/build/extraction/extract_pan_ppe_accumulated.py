"""Note 7 PPE continuation (PAN physical page 28): accumulated depreciation and the
carrying-amount table.

The page mixes two row widths: movement rows carry 14 values, while the opening/closing
balance rows and the carrying-amount rows carry 15 (an extra column). Filtering on the
modal width therefore discarded exactly the rows that matter. This extractor keeps the
longest trailing run of value tokens on each line, whatever its width.
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
EXTRACTION_COMMIT = "p1_ppe_accumulated_v2"
PAGE = 28
REGION = "note_p28"
MIN_RUN = 8

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
        if len(rest) < MIN_RUN:
            continue
        if all(VALUE_RE.fullmatch(t) for t in rest):
            label = " ".join(tokens[:k]).strip()
            # A leading four-digit year ('Balance as at 1 July 2024') belongs to the label,
            # not to the figures.
            while rest and re.fullmatch(r"20\d{2}", rest[0]):
                label = f"{label} {rest[0]}".strip()
                rest = rest[1:]
            if len(rest) < MIN_RUN:
                continue
            return label, rest
    return None


def run():
    rows = []
    for raw in text_lines():
        parsed = longest_run(raw)
        if parsed:
            label, values = parsed
            # Two rows arrive as wrapped tails; their heads sit lines above.
            label = {"losses)": "Impairment losses (accumulated)",
                     "movement": "Foreign currency translation reserve movement"}.get(label, label)
            rows.append((label, values))
    print(f"p{PAGE}: {len(rows)} rows, widths {sorted({len(v) for _l, v in rows})}",
          file=sys.stderr)

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
        print(f"Inserted {n} cells over {len(rows)} rows. Total in DB: "
              f"{con.execute('SELECT COUNT(*) FROM cells').fetchone()[0]}")
        for label, values in rows:
            print(f"  {label[:46]:<46} n={len(values):>2} total={values[-1]}")
    finally:
        con.close()


if __name__ == "__main__":
    run()
