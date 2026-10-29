"""Remediation pass 1: normalise lineage, re-extract p.34 keeping note-reference columns.

Fixes:
  * `document` held a Windows file path for the 1,196 D009 cells and a SHA-256 for the rest.
    Normalised to the SHA-256 everywhere.
  * p.34 Note 18 (Emmerson acquisition) rows were discarded by a modal-width filter: their
    "extra" leading token was a note reference (14, 7), not contamination.
"""
from __future__ import annotations

import pathlib
import re
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

DB = pathlib.Path(r"workflow/changes/20261029_agentic_report_build/build/report.sqlite")
PDF = pathlib.Path(
    r"companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")
SHA = "62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd"
VALUE_RE = re.compile(r"\(?[\d,]+(?:\.\d+)?\)?|[–—\-]")
DASH_RE = re.compile(r"^[–—\-]$")

con = sqlite3.connect(str(DB))
cur = con.cursor()

# ---- 1. normalise document to the SHA-256 -------------------------------------------
before = cur.execute(
    "SELECT COUNT(*) FROM cells WHERE document <> ?", (SHA,)).fetchone()[0]
cur.execute("UPDATE cells SET document = ? WHERE document <> ?", (SHA, SHA))
con.commit()
print(f"1. document normalised: {before} cells rewritten to the SHA-256")
print("   distinct now:", cur.execute(
    "SELECT COUNT(DISTINCT document) FROM cells").fetchone()[0])


# ---- 2. re-extract p.34 keeping note-reference columns ------------------------------
def lines(page):
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(PDF))
    try:
        raw = doc[page - 1].get_textpage().get_text_range()
    finally:
        doc.close()
    return [ln.strip() for ln in raw.splitlines() if ln.strip()]


def split_ref(raw):
    """label, note_ref(optional), values - keeps a leading integer as a note reference."""
    toks = raw.split()
    for k in range(len(toks)):
        rest = toks[k:]
        if len(rest) < 2 or not all(VALUE_RE.fullmatch(t) for t in rest):
            continue
        label = " ".join(toks[:k]).strip()
        if not label or label.endswith(","):
            continue
        ref = None
        if len(rest) >= 2 and re.fullmatch(r"\d{1,2}", rest[0]) and re.search(r"[,.]", rest[1]):
            ref, rest = rest[0], rest[1:]
        return label, ref, rest
    return None


P34 = "note_p34"
rows = []
for raw in lines(34):
    if raw.startswith(("NOTES TO", "for the year", "PAN AFRICAN", "Summarised")):
        continue
    parsed = split_ref(raw)
    if parsed and len(parsed[2]) >= 1:
        rows.append(parsed)

cur.execute("DELETE FROM cells WHERE table_region = ?", (P34,))
n = 0
for idx, (label, ref, values) in enumerate(rows, start=1):
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
            (SHA, 34, P34, (f"[{ref}] " if ref else "") + label, None, "US$ thousand",
             f"col{col}", col, raw, val, idx, "p1_note17_18_p34_v2"))
        n += 1
con.commit()
print(f"2. p.34 re-extracted: {n} cells over {len(rows)} rows")
for label, ref, values in rows:
    print(f"   {'[' + ref + '] ' if ref else ''}{label[:56]:<58} n={len(values):>2} "
          + " ".join(values[:3]))

# ---- 3. what the new tests can assert --------------------------------------------
print("\n3. discovery for the new assertions")
for region, needle in (("note_p29", "%"), ("note_p33", "%"), ("note_p34", "%")):
    print(f"   -- {region}")
    for lab, col, raw in cur.execute(
            "SELECT row_label, column_index, value_raw FROM cells "
            "WHERE table_region=? ORDER BY row_index, column_index", (region,)):
        if any(k in lab.lower() for k in ("sustaining", "expansion", "total", "balance",
                                          "expense", "payment", "capex", "capital")):
            print(f"      {lab[:56]:<56} col{col} = {raw}")
con.close()
