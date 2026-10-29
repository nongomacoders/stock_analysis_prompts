"""Extract p.47: return on capital employed, and the per-share history tables.

ROCE row set (2 values each, FY26 / FY25) plus two 10-column per-share history rows
(FY26..FY22, each in ZA cents and GB pence). Text-layer driven, as on pp.40-44.
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
EXTRACTION_COMMIT = "p1_apm_roce_v1"
PAGE = 47

VALUE_RE = re.compile(r"\(?[\d,]+(?:\.\d+)?\)?|[–—\-]")
DASH_RE = re.compile(r"^[–—\-]$")

ROCE_REGION = "apm_roce"
PER_SHARE_REGION = "apm_per_share_history"

PER_SHARE_COLUMNS = [
    ("FY26", "ZA cents"), ("FY26", "GB pence"),
    ("FY25", "ZA cents"), ("FY25", "GB pence"),
    ("FY24", "ZA cents"), ("FY24", "GB pence"),
    ("FY23", "ZA cents"), ("FY23", "GB pence"),
    ("FY22", "ZA cents"), ("FY22", "GB pence"),
]

ROCE_UNITS = {
    "Net income before finance income and finance costs": "US$ million",
    "Average equity": "US$ million",
    "Average borrowings": "US$ million",
    "Return on capital employed": "%",
}


def text_lines():
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(PDF_PATH))
    try:
        raw = doc[PAGE - 1].get_textpage().get_text_range()
    finally:
        doc.close()
    return [ln.strip() for ln in raw.splitlines() if ln.strip()]


def split_row(raw, ncols):
    tokens = raw.split()
    for k in range(len(tokens)):
        rest = tokens[k:]
        if len(rest) != ncols or not all(VALUE_RE.fullmatch(t) for t in rest):
            continue
        label = " ".join(tokens[:k]).strip()
        label = re.sub(r"\s*(?:US\$ million|%|per share)\s*$", "", label).strip()
        if label:
            return label, rest
    return None


def run():
    rows = []
    pending_ps = None
    for raw in text_lines():
        parsed = split_row(raw, 2)
        if parsed and parsed[0] in ROCE_UNITS:
            rows.append((ROCE_REGION, parsed[0], parsed[1]))
            continue
        if raw in ("Earnings", "Dividends"):
            pending_ps = "Earnings per share" if raw == "Earnings" else "Dividends per share"
            continue
        if raw.startswith("per share "):
            tokens = raw.split()
            values = tokens[-10:]
            if len(values) == 10 and all(VALUE_RE.fullmatch(t) for t in values):
                rows.append((PER_SHARE_REGION, pending_ps or "Per share", values))
                pending_ps = None

    con = sqlite3.connect(str(DB_PATH))
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM cells WHERE table_region IN (?,?)",
                    (ROCE_REGION, PER_SHARE_REGION))
        n = 0
        for idx, (region, label, values) in enumerate(rows, start=1):
            for col, raw in enumerate(values):
                if region == ROCE_REGION:
                    fy = "FY26" if col == 0 else "FY25"
                    unit = ROCE_UNITS[label]
                    collab = fy
                else:
                    fy, unit = PER_SHARE_COLUMNS[col]
                    collab = f"{fy} {unit}"
                    unit = unit
                val = None
                if not DASH_RE.match(raw):
                    s = raw.replace(",", "")
                    val = -float(s[1:-1]) if s.startswith("(") else float(s)
                cur.execute(
                    """INSERT INTO cells (document, physical_page, table_region, row_label,
                       fiscal_year, unit, column_label, column_index, value_raw, value_num,
                       row_index, extraction_commit)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (EXPECTED_SHA, PAGE, region, label, fy, unit, collab, col,
                     raw, val, idx, EXTRACTION_COMMIT))
                n += 1
        con.commit()
        print(f"Inserted {n} cells over {len(rows)} rows. Total in DB: "
              f"{con.execute('SELECT COUNT(*) FROM cells').fetchone()[0]}")
        for region, label, values in rows:
            print(f"  {region[:22]:<22} {label[:44]:<44} " + " ".join(f"{v:>9}" for v in values))
    finally:
        con.close()


if __name__ == "__main__":
    run()
