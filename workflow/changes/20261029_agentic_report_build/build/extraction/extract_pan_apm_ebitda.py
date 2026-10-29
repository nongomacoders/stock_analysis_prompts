"""Extract the APM Adjusted EBITDA reconciliation (PAN physical page 45).

Why this page matters: it repeats the Group production summary operation grid
(13 printed value columns) in US$ million and reconciles every column from
net income/(cost) before finance and finance costs to Adjusted EBITDA. It is the
formal definition layer behind D009 p.50 and Note 3 p.22.

Three traps learned on this page (see WORKPLAN_APM.md):
  1. numbers split as '81' + '.5' and '51' + '.8' - the fragment regex must accept a
     leading dot, and fragments are merged before column assignment;
  2. labels wrap *around* the value line ('...plant and' / values / 'equipment'), so
     labels are taken from the PDF text layer (logical reading order) and matched to
     geometry rows by their leading values - not by row position;
  3. the first value column ends at x1 ~ 203.6, so a higher value-band floor would
     silently drop the Barberton column.

Printed glyphs are preserved verbatim in value_raw; nothing is corrected.
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
EXTRACTION_COMMIT = "p1_apm_ebitda_v2"
REGION = "apm_adjusted_ebitda"
PAGE = 45

# '81', '81.5', '.5', '(28.0)', '1,196,474' - a leading dot is a legitimate fragment
NUM_RE = re.compile(r"^\(?(?:\d[\d,]*(?:\.\d*)?|\.\d+)\)?$")
DASH_RE = re.compile(r"^[–—\-]$")
VALUE_X1_MIN = 198.0
LABEL_X1_MAX = 178.0
EDGE_TOL = 5.0
EDGE_MIN_COUNT = 3
SNAP_TOL = 8.0
LINE_TOL = 3.2
FRAG_GAP = 12.0

COLUMN_LABELS = [
    "Barberton Mines", "Evander Mines", "Total", "BTRP", "Elikhulu",
    "MTR operation", "Tennant Mines", "Total", "Barberton Mines total",
    "Evander Mines total", "MTR operation total", "Tennant Mines total",
    "Group total",
]


class Tok:
    __slots__ = ("text", "x0", "x1", "y0")

    def __init__(self, text, x0, x1, y0):
        self.text, self.x0, self.x1, self.y0 = text, x0, x1, y0


def text_lines() -> list[str]:
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(PDF_PATH))
    try:
        raw = doc[PAGE - 1].get_textpage().get_text_range()
    finally:
        doc.close()
    return [ln.strip() for ln in raw.splitlines() if ln.strip()]


def label_rows() -> list[tuple[str, list[str]]]:
    """(label, printed values) per data line, in reading order.

    Wrapped labels print their first half on the preceding text line and the remainder
    after it, so a data line whose label starts with a lowercase word takes the previous
    text line as its head.
    """
    lines = text_lines()
    out = []
    for i, raw in enumerate(lines):
        m = re.match(r"^(.*?)\s*((?:\(?[\d,]+(?:\.\d+)?\)?|[–—\-])(?:\s+(?:\(?[\d,]+(?:\.\d+)?\)?|[–—\-])){5,})$", raw)
        if not m:
            continue
        label = m.group(1).strip()
        values = re.findall(r"\(?[\d,]+(?:\.\d+)?\)?|[–—\-]", m.group(2))
        if not label or len(values) < 10:
            continue
        if label[0].islower() and i > 0:
            label = f"{lines[i - 1]} {label}"
        out.append((re.sub(r"\s+", " ", label).strip(), values))
    return out


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
                    and w.x0 - prev.x1 <= FRAG_GAP):
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


def norm(raw: str) -> str:
    return raw.replace(",", "").strip()


def run():
    ws = words.extract_words(PDF_PATH.read_bytes(), PAGE)
    body = [w for w in ws if 150.0 < w.y0 < 420.0]
    lines = [merge_fragments(l) for l in group_lines(body)]
    edges = derive_edges(lines)
    print(f"p{PAGE}: {len(edges)} value-column edges: {edges}")
    if len(edges) != 13:
        raise RuntimeError(f"expected 13 value columns, got {len(edges)}")

    fy = None
    geo = []
    for line in lines:
        text = " ".join(t.text for t in line).strip()
        if text in ("FY26", "FY25"):
            fy = text
            continue
        cells = {}
        for t in line:
            if t.x1 < VALUE_X1_MIN:
                continue
            if not (NUM_RE.match(t.text) or DASH_RE.match(t.text)):
                continue
            idx = min(range(13), key=lambda i: abs(edges[i] - t.x1))
            if abs(edges[idx] - t.x1) <= SNAP_TOL:
                cells[idx] = t.text
        if cells and fy:
            geo.append({"fy": fy, "cells": cells})

    labels = label_rows()
    print(f"geometry rows: {len(geo)}, text-layer data rows: {len(labels)}")

    # Match labels to geometry rows by leading values (reading order both sides),
    # never by row count.
    assigned, cursor = [], 0
    for row in geo:
        first = norm(row["cells"][min(row["cells"])])
        match = None
        for j in range(cursor, len(labels)):
            vals = [norm(v) for v in labels[j][1]]
            if vals and vals[0] == first:
                match = (j, labels[j][0])
                break
        if match:
            cursor = match[0] + 1
            assigned.append((row["fy"], match[1], row["cells"]))
        else:
            assigned.append((row["fy"], f"UNMATCHED_LABEL_{row['fy']}_{min(row['cells'])}", row["cells"]))

    con = sqlite3.connect(str(DB_PATH))
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM cells WHERE table_region = ?", (REGION,))
        n = 0
        for idx, (year, label, cells) in enumerate(assigned, start=1):
            for col, raw in sorted(cells.items()):
                val = None
                if not DASH_RE.match(raw):
                    s = raw.replace(",", "")
                    val = -float(s[1:-1]) if s.startswith("(") else float(s)
                cur.execute(
                    """INSERT INTO cells (document, physical_page, table_region, row_label,
                       fiscal_year, unit, column_label, column_index, value_raw, value_num,
                       row_index, extraction_commit)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (EXPECTED_SHA, PAGE, REGION, label, year, "US$ million",
                     COLUMN_LABELS[col], col, raw, val, idx, EXTRACTION_COMMIT))
                n += 1
        con.commit()
        print(f"Inserted {n} APM cells over {len(assigned)} rows. Total in DB: "
              f"{con.execute('SELECT COUNT(*) FROM cells').fetchone()[0]}")
        for year, label, cells in assigned:
            vals = " ".join(f"{cells[i]:>8}" if i in cells else f"{'-':>8}" for i in range(13))
            print(f"  {year} {label[:54]:<54} {vals}")
    finally:
        con.close()


if __name__ == "__main__":
    run()
