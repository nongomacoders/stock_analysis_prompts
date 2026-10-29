"""Extract the all-in cost reconciliations (PAN physical pages 40-43).

Four tables, all using the same 13-column operation grid as p.45:

  p.40  FY26  US$ million   apm_aisc_fy26_usd
  p.41  FY25  US$ million   apm_aisc_fy25_usd
  p.42  FY26  Unit          apm_aisc_fy26_unit
  p.43  FY25  Unit          apm_aisc_fy25_unit

As on p.44, the PDF text layer already lists each row as label followed by its values in
printed column order, so rows come from the text layer and no coordinate snapping is
used. A label that starts lowercase is the wrapped tail of the previous label line and is
joined back to it.

A trailing unit token ('kg', 'oz', 'ZAR million', 'ZAR/kg', 'A$/kg', 'US$/oz',
'US$/ZAR', 'A$ million') is split off the label into the unit column.
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
EXTRACTION_COMMIT = "p1_apm_aisc_v1"

VALUE_RE = re.compile(r"\(?[\d,]+(?:\.\d+)?\)?|[–—\-]")
ROW_RE = re.compile(r"^(.*?)\s*((?:\(?[\d,]+(?:\.\d+)?\)?|[–—\-])"
                    r"(?:\s+(?:\(?[\d,]+(?:\.\d+)?\)?|[–—\-])){10,})$")
DASH_RE = re.compile(r"^[–—\-]$")
NCOLS = 13

PAGES = [
    (40, "apm_aisc_fy26_usd", "FY26", "US$ million"),
    (41, "apm_aisc_fy25_usd", "FY25", "US$ million"),
    (42, "apm_aisc_fy26_unit", "FY26", "unit basis"),
    (43, "apm_aisc_fy25_unit", "FY25", "unit basis"),
]

COLUMN_LABELS = [
    "Barberton Mines", "Evander Mines", "Total", "BTRP", "Elikhulu",
    "MTR operation", "Tennant Mines", "Total", "Barberton Mines total",
    "Evander Mines total", "MTR operation total", "Tennant Mines total",
    "Group total",
]

UNIT_SUFFIX = re.compile(
    r"^(.*?)\s+((?:ZAR|US\$|A\$)\s?(?:million|/kg|/oz|/t|/ZAR|/A\$)|kg|oz|%|million)$")

SKIP_PREFIX = ("ALTERNATIVE PERFORMANCE", "ALL-IN COSTS", "Mining operations Tailings",
               "US$ million", "FY26", "FY25", "PAN AFRICAN", "Summarised audited",
               "This includes", "which relate", "operations and", "and US$ per ounce",
               "equivalent is", "Group’s operational", "a ratio of", "The following",
               "IFRS Accounting", "30 June 2026", "The equivalent", "production table",
               "1 A$ per", "AISC and AIC", "Total operations", "Barberton", "Evander",
               "Mines", "MTR", "operation", "Tennant", "Total", "Bar-", "berton",
               "Group", "total", "Solar", "projects", "US$", "Unit", "Notes")


def text_lines(page):
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(PDF_PATH))
    try:
        raw = doc[page - 1].get_textpage().get_text_range()
    finally:
        doc.close()
    return [ln.strip() for ln in raw.splitlines() if ln.strip()]


def split_row(raw):
    """Split a text line into (label, values) by token scanning.

    A plain regex fails here because labels routinely carry a footnote digit
    ('Cash cost1', 'All-in sustaining costs1'), which the lazy label match swallowed as
    the first value. Scanning instead for the first position where exactly NCOLS value
    tokens run to the end of the line is unambiguous.
    """
    tokens = raw.split()
    for k in range(len(tokens)):
        rest = tokens[k:]
        if len(rest) != NCOLS:
            continue
        if all(VALUE_RE.fullmatch(t) for t in rest):
            label = " ".join(tokens[:k]).strip()
            if not label:
                return None
            return label, rest
    return None


def strip_footnote(label):
    m = re.match(r"^(.*[^\d\s])\d$", label)
    return m.group(1) if m else label


def split_unit(label):
    m = UNIT_SUFFIX.match(label)
    if m:
        return m.group(1).strip(), m.group(2).replace(" ", "")
    return label, None


def run():
    con = sqlite3.connect(str(DB_PATH))
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM cells WHERE table_region LIKE 'apm_aisc_%'")
        total = 0
        for page, region, fy, default_unit in PAGES:
            rows, prev_text = [], ""
            for raw in text_lines(page):
                parsed = split_row(raw)
                if not parsed:
                    prev_text = raw
                    continue
                label, values = parsed
                if label[0].islower() or label.startswith("("):
                    label = f"{prev_text} {label}"      # wrapped label tail
                label = strip_footnote(label)
                label, unit = split_unit(label)
                label = re.sub(r"\s+", " ", label).strip()
                rows.append((label, unit or default_unit, values))
                prev_text = raw

            print(f"p{page} {region} ({fy}): {len(rows)} rows", file=sys.stderr)
            for idx, (label, unit, values) in enumerate(rows, start=1):
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
                        (EXPECTED_SHA, page, region, label, fy, unit,
                         COLUMN_LABELS[col], col, raw, val, idx, EXTRACTION_COMMIT))
                    total += 1
            for label, unit, values in rows[:3]:
                print(f"    {label[:44]:<44} {unit:<12} " + " ".join(f"{v:>9}" for v in values[:4]),
                      file=sys.stderr)
        con.commit()
        print(f"Inserted {total} cells. Total in DB: "
              f"{con.execute('SELECT COUNT(*) FROM cells').fetchone()[0]}")
        print("rows per region:", dict(con.execute(
            "SELECT table_region, COUNT(DISTINCT row_index) FROM cells "
            "WHERE table_region LIKE 'apm_aisc_%' GROUP BY table_region").fetchall()))
    finally:
        con.close()


if __name__ == "__main__":
    run()
