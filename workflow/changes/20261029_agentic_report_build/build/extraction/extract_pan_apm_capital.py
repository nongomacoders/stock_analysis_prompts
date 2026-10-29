"""Extract p.44: capital expenditure by asset, and net debt / net senior debt.

The first geometry-driven attempt failed twice (see WORKPLAN_APM.md section 6). The
decisive observation is that the PDF text layer already lists each row as
label followed by its values *in printed column order*, so no coordinate snapping is
needed at all on this page: rows come from the text layer, and the section each row
belongs to comes from the headings.

Three sections:
  apm_capital_expenditure  12 rows x 6 values (Sustaining / Expansion / Total, FY26+FY25)
  apm_net_debt              8 rows x 2 values (FY26, FY25)
  apm_net_senior_debt       5 rows x 2 values
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
EXTRACTION_COMMIT = "p1_apm_capital_v3"
PAGE = 44

VALUE_RE = re.compile(r"\(?[\d,]+(?:\.\d+)?\)?|[–—\-]")
ROW_RE = re.compile(r"^(.*?)\s*((?:\(?[\d,]+(?:\.\d+)?\)?|[–—\-])"
                    r"(?:\s+(?:\(?[\d,]+(?:\.\d+)?\)?|[–—\-]))+)$")
DASH_RE = re.compile(r"^[–—\-]$")

CAP_REGION = "apm_capital_expenditure"
DEBT_REGION = "apm_net_debt"
SENIOR_REGION = "apm_net_senior_debt"

CAP_COLUMNS = [
    ("Sustaining capital", "FY26"), ("Sustaining capital", "FY25"),
    ("Expansion capital", "FY26"), ("Expansion capital", "FY25"),
    ("Total capital", "FY26"), ("Total capital", "FY25"),
]

HEADINGS = (
    ("NET (CASH)/SENIOR DEBT", SENIOR_REGION),
    ("NET (CASH)/DEBT", DEBT_REGION),
)

# The capital table starts at its own heading; everything before the first debt heading
# that carries six values is capital.
CAP_HEADING = "SUSTAINING CAPITAL"


def text_lines():
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(PDF_PATH))
    try:
        raw = doc[PAGE - 1].get_textpage().get_text_range()
    finally:
        doc.close()
    return [ln.strip() for ln in raw.splitlines() if ln.strip()]


def run():
    section = CAP_REGION
    rows = []
    for raw in text_lines():
        upper = raw.upper()
        if upper.startswith(CAP_HEADING):
            section = CAP_REGION
            continue
        for heading, region in HEADINGS:
            if upper.startswith(heading):
                section = region
                break
        m = ROW_RE.match(raw)
        if not m:
            prev_text = raw.strip()
            continue
        label = m.group(1).strip()
        values = VALUE_RE.findall(m.group(2))
        if not label:
            continue
        if label[0].islower() and prev_text:
            label = f"{prev_text} {label}"   # wrapped head, e.g. 'Agricultural ESG' + 'projects'
        expected = 6 if section == CAP_REGION else 2
        if len(values) != expected:
            continue
        rows.append((section, label, values))

    con = sqlite3.connect(str(DB_PATH))
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM cells WHERE table_region IN (?,?,?)",
                    (CAP_REGION, DEBT_REGION, SENIOR_REGION))
        n = 0
        counts = {}
        for idx, (region, label, values) in enumerate(rows, start=1):
            counts[region] = counts.get(region, 0) + 1
            for col, raw in enumerate(values):
                if region == CAP_REGION:
                    measure, fy = CAP_COLUMNS[col]
                else:
                    measure = ("Net (cash)/debt" if region == DEBT_REGION
                               else "Net (cash)/senior debt")
                    fy = "FY26" if col == 0 else "FY25"
                val = None
                if not DASH_RE.match(raw):
                    s = raw.replace(",", "")
                    val = -float(s[1:-1]) if s.startswith("(") else float(s)
                cur.execute(
                    """INSERT INTO cells (document, physical_page, table_region, row_label,
                       fiscal_year, unit, column_label, column_index, value_raw, value_num,
                       row_index, extraction_commit)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (EXPECTED_SHA, PAGE, region, label, fy, "US$ million",
                     measure, col, raw, val, idx, EXTRACTION_COMMIT))
                n += 1
        con.commit()
        print(f"Inserted {n} cells over {len(rows)} rows: {counts}")
        print(f"Total cells in DB: {con.execute('SELECT COUNT(*) FROM cells').fetchone()[0]}")
        for region, label, values in rows:
            print(f"  {region[:22]:<22} {label[:40]:<40} " + " ".join(f"{v:>9}" for v in values))
    finally:
        con.close()


if __name__ == "__main__":
    run()
