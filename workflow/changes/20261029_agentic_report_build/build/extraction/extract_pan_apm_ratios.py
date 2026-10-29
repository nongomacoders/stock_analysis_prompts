"""Extract the p.46 APM tables: net asset value per share, levered free cash flow and
cash flow yield per share.

All three tables share one simple layout - label, FY26, FY25 - so the extractor derives
two value-column edges from the page and reads rows in order, using the PDF text layer for
labels and for the section state (which table a row belongs to).

Two of the labels repeat across tables ('Shares in issue', 'Treasury shares'), so the
table name is carried in table_region rather than inferred from the label.
"""
from __future__ import annotations

import pathlib
import re
import sqlite3
import sys
from statistics import mean

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here))
import words

DB_PATH = here.parent / "report.sqlite"
PDF_PATH = pathlib.Path(
    r"companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")
EXPECTED_SHA = "62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd"
EXTRACTION_COMMIT = "p1_apm_ratios_v1"
PAGE = 46

NUM_RE = re.compile(r"^\(?(?:\d[\d,]*(?:\.\d*)?|\.\d+)\)?$")
DASH_RE = re.compile(r"^[–—\-]$")
VALUE_X1_MIN = 380.0
EDGE_TOL = 5.0
EDGE_MIN_COUNT = 4
SNAP_TOL = 8.0
LINE_TOL = 3.2

SECTIONS = [
    # longest first: a shorter marker is a prefix of the longer one
    ("LEVERED FREE CASH FLOW YIELD PER SHARE", "apm_cash_flow_yield"),
    ("LEVERED FREE CASH FLOW", "apm_levered_free_cash_flow"),
    ("NET ASSET VALUE PER SHARE", "apm_nav_per_share"),
]
UNIT_BY_REGION = {
    "apm_nav_per_share": "million",
    "apm_levered_free_cash_flow": "million",
    "apm_cash_flow_yield": "per share",
}


class Tok:
    __slots__ = ("text", "x0", "x1", "y0")

    def __init__(self, text, x0, x1, y0):
        self.text, self.x0, self.x1, self.y0 = text, x0, x1, y0


def text_lines():
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(PDF_PATH))
    try:
        raw = doc[PAGE - 1].get_textpage().get_text_range()
    finally:
        doc.close()
    return [ln.strip() for ln in raw.splitlines() if ln.strip()]


def group_lines(ws):
    ws = sorted(ws, key=lambda w: (-w.y0, w.x0))
    lines = []
    for w in ws:
        for l in lines:
            if abs(l[0].y0 - w.y0) <= LINE_TOL:
                l.append(w)
                break
        else:
            lines.append([w])
    for l in lines:
        l.sort(key=lambda w: w.x0)
    lines.sort(key=lambda l: -l[0].y0)
    return lines


def merge_fragments(line):
    merged = []
    for w in line:
        if merged:
            prev = merged[-1]
            if (NUM_RE.match(prev.text) and NUM_RE.match(w.text)
                    and w.x0 - prev.x1 <= 12.0):
                merged[-1] = Tok(prev.text + w.text, prev.x0, w.x1, prev.y0)
                continue
        merged.append(Tok(w.text, w.x0, w.x1, w.y0))
    return merged


def derive_edges(lines):
    anchors = sorted(t.x1 for line in lines for t in line
                     if NUM_RE.match(t.text) and t.x1 >= VALUE_X1_MIN)
    clusters = []
    for a in anchors:
        if clusters and a - clusters[-1][-1] <= EDGE_TOL:
            clusters[-1].append(a)
        else:
            clusters.append([a])
    return [round(mean(c), 2) for c in clusters if len(c) >= EDGE_MIN_COUNT]


def norm(s):
    return s.replace(",", "").strip()


def run():
    ws = words.extract_words(PDF_PATH.read_bytes(), PAGE)
    lines = [merge_fragments(l) for l in group_lines(ws)]
    edges = derive_edges(lines)
    print(f"p{PAGE}: {len(edges)} value-column edges: {edges}")
    if len(edges) != 2:
        raise RuntimeError(f"expected 2 value columns, got {len(edges)}")

    # Labels in reading order from the text layer.
    labels = []
    for raw in text_lines():
        m = re.match(r"^(.*?)\s*((?:\(?[\d,]+(?:\.\d+)?\)?|[–—\-])(?:\s+(?:\(?[\d,]+(?:\.\d+)?\)?|[–—\-]))+)$", raw)
        if m and m.group(1).strip():
            labels.append((m.group(1).strip(), re.findall(r"\(?[\d,]+(?:\.\d+)?\)?|[–—\-]", m.group(2))))

    region, rows = None, []
    for line in lines:
        text = " ".join(t.text for t in line).strip()
        for marker, reg in SECTIONS:
            if marker in text:
                region = reg
                break
        cells = {}
        for t in line:
            if t.x1 < VALUE_X1_MIN:
                continue
            if not (NUM_RE.match(t.text) or DASH_RE.match(t.text)):
                continue
            idx = min(range(2), key=lambda i: abs(edges[i] - t.x1))
            if abs(edges[idx] - t.x1) <= SNAP_TOL:
                cells[idx] = t.text
        if region and len(cells) == 2:
            rows.append({"region": region, "cells": cells})

    print(f"geometry rows: {len(rows)}")
    used, out = set(), []
    for row in rows:
        first = norm(row["cells"][0])
        for i, (label, vals) in enumerate(labels):
            if i in used or not vals:
                continue
            if norm(vals[0]) == first:
                used.add(i)
                out.append((row["region"], label, row["cells"]))
                break
        else:
            out.append((row["region"], None, row["cells"]))

    con = sqlite3.connect(str(DB_PATH))
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM cells WHERE table_region IN (?,?,?)",
                    tuple(r for _, r in SECTIONS))
        n = 0
        for idx, (reg, label, cells) in enumerate(out, start=1):
            lab = label or f"UNLABELLED_{reg}_{idx}"
            for col, raw in sorted(cells.items()):
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
                    (EXPECTED_SHA, PAGE, reg, lab, fy, UNIT_BY_REGION[reg],
                     fy, col, raw, val, idx, EXTRACTION_COMMIT))
                n += 1
        con.commit()
        print(f"Inserted {n} cells over {len(out)} rows. Total in DB: "
              f"{con.execute('SELECT COUNT(*) FROM cells').fetchone()[0]}")
        for reg, label, cells in out:
            print(f"  {reg[:26]:<26} {(label or '??')[:46]:<46} "
                  f"{cells.get(0,'-'):>10} {cells.get(1,'-'):>10}")
    finally:
        con.close()


if __name__ == "__main__":
    run()
