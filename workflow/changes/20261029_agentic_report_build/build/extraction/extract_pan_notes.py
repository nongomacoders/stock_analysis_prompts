"""Extract the remaining financial-statement notes (PAN physical pages 25-37).

These notes are overwhelmingly two-column roll-forwards and listings under a
'US$ thousand FY26 FY25' header. The text layer already gives each row as label followed
by its values in printed column order, so the same token-scan approach used on pp.40-47
applies: a row is a label plus the maximal run of value tokens that reaches end-of-line.

Region naming keeps provenance obvious: `note_p25` .. `note_p37`, one per physical page.
Column semantics are NOT assumed here - column_index is the printed position, and the
checks that rely on meaning are written explicitly against the notes they belong to.
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
EXTRACTION_COMMIT = "p1_notes_generic_v1"
PAGES = list(range(25, 38))
MIN_VALUES, MAX_VALUES = 1, 8

VALUE_RE = re.compile(r"\(?[\d,]+(?:\.\d+)?\)?|[–—\-]")
DASH_RE = re.compile(r"^[–—\-]$")

# Lines that are page furniture or prose, never data rows.
SKIP_START = ("NOTES TO THE", "for the year ended", "PAN AFRICAN RESOURCES", "Summarised audited")


def text_lines(page):
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(PDF_PATH))
    try:
        raw = doc[page - 1].get_textpage().get_text_range()
    finally:
        doc.close()
    return [ln.strip() for ln in raw.splitlines() if ln.strip()]


def split_row(raw):
    """(label, values) if the line ends in a run of MIN..MAX value tokens."""
    tokens = raw.split()
    for k in range(len(tokens)):
        rest = tokens[k:]
        if not (MIN_VALUES <= len(rest) <= MAX_VALUES):
            continue
        if not all(VALUE_RE.fullmatch(t) for t in rest):
            continue
        # A single trailing number is almost always prose or a note reference.
        if len(rest) == 1:
            continue
        label = " ".join(tokens[:k]).strip()
        if label and not label.endswith(","):
            return label, rest
    return None


def run():
    con = sqlite3.connect(str(DB_PATH))
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM cells WHERE table_region LIKE 'note_p%'")
        total = 0
        for page in PAGES:
            region = f"note_p{page}"
            rows, prev = [], ""
            dropped = 0
            for raw in text_lines(page):
                if raw.startswith(SKIP_START):
                    continue
                parsed = split_row(raw)
                if not parsed:
                    prev = raw
                    continue
                label = parsed[0]
                if label[0].islower() or label.startswith("("):
                    label = f"{prev} {label}"
                label = re.sub(r"\s+", " ", label).strip()
                # Quality gate: legitimate labels carry at most two small numbers
                # ('Balance as at 1 July', 'General banking facility2'). Multi-column
                # tables interleave many numbers into the "label" - those are prose
                # fragments or PPE column bleed and are not stored.
                if len(re.findall(r"\d+", label)) >= 3:
                    dropped += 1
                    prev = raw
                    continue
                rows.append((label, parsed[1]))
                prev = raw
            if dropped and dropped > len(rows):
                print(f"  p{page}: DEFERRED - {dropped} contaminated rows vs {len(rows)} clean",
                      file=sys.stderr)
                continue
            for idx, (label, values) in enumerate(rows, start=1):
                ncols = len(values)
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
                        (EXPECTED_SHA, page, region, label, None, "US$ thousand",
                         f"col{col}", col, raw, val, idx, EXTRACTION_COMMIT))
                    total += 1
            print(f"  p{page}: {len(rows)} rows", file=sys.stderr)
        con.commit()
        print(f"Inserted {total} cells. Total in DB: "
              f"{con.execute('SELECT COUNT(*) FROM cells').fetchone()[0]}")
        for reg, cnt in con.execute(
                "SELECT table_region, COUNT(DISTINCT row_index) FROM cells "
                "WHERE table_region LIKE 'note_p%' GROUP BY table_region ORDER BY table_region"):
            print(f"  {reg}: {cnt} rows")
    finally:
        con.close()


if __name__ == "__main__":
    run()
