"""Extract PAN Note 3 Segment Analysis (physical pages 21-24).

Layout: 11 printed numeric columns, right-aligned, identical grid on all four pages.

  col0 Barberton Mines        col6 Exploration assets
  col1 Evander Mines          col7 Agricultural ESG projects
  col2 Solar projects         col8 Corporate
  col3 MTR operation          col9 Funding Company
  col4 Tennant Mines          col10 Group total
  col5 Mining operations (subtotal)

Column edges are derived from the page itself (clusters of numeric right edges),
never hardcoded; printed column labels come from the header band of the page.

Some printed numbers arrive split into two or three tokens because the typesetter
used a wide space after a comma ('242,' + '186'). Fragments are re-joined before
column assignment and the glyphs are kept verbatim in value_raw.
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
EXTRACTION_COMMIT = "p1_note3_segments_v2"
REGION = "note3_segment_analysis"
REGION_INTRA = "note3_intra_group"

NUM_RE = re.compile(r"^\(?[\d,]+(?:\.\d+)?\)?$")
DASH_RE = re.compile(r"^[–—\-]$")
NOTE_COL_MAX_X0 = 265.0
LABEL_X0_MAX = 240.0
EDGE_TOL = 5.0
EDGE_MIN_COUNT = 4
SNAP_TOL = 6.0
LINE_TOL = 4.0
FRAG_GAP = 12.0          # tokens closer than this on one line are one printed number
BODY_TOP = 470.0
BODY_BOTTOM = 90.0
INTRA_SPLIT_Y = 145.0

COLUMN_LABELS = [
    "Barberton Mines", "Evander Mines", "Solar projects", "MTR operation",
    "Tennant Mines", "Mining operations", "Exploration assets",
    "Agricultural ESG projects", "Corporate", "Funding Company", "Group total",
]


class Tok:
    __slots__ = ("text", "x0", "x1", "y0", "y1", "anchor")

    def __init__(self, text, x0, x1, y0, y1):
        self.text, self.x0, self.x1, self.y0, self.y1 = text, x0, x1, y0, y1
        self.anchor = x1


def group_lines(ws, tol=LINE_TOL):
    ws = sorted(ws, key=lambda w: (-w.y0, w.x0))
    lines = []
    for w in ws:
        for l in lines:
            if abs(l[0].y0 - w.y0) <= tol:
                l.append(w)
                break
        else:
            lines.append([w])
    for l in lines:
        l.sort(key=lambda w: w.x0)
    lines.sort(key=lambda l: -l[0].y0)
    return lines


def merge_fragments(line):
    """Join numeric tokens printed as fragments of one number (small x gap)."""
    merged = []
    for w in line:
        prev = merged[-1] if merged else None
        if (prev is not None and NUM_RE.match(prev.text) and NUM_RE.match(w.text)
                and w.x0 - prev.x1 <= FRAG_GAP):
            merged[-1] = Tok(prev.text + w.text, prev.x0, w.x1, prev.y0, prev.y1)
            continue
        merged.append(Tok(w.text, w.x0, w.x1, w.y0, w.y1))
    return merged


def derive_edges(lines):
    anchors = sorted(t.anchor for line in lines for t in line
                     if NUM_RE.match(t.text) and t.x0 > NOTE_COL_MAX_X0)
    clusters = []
    for a in anchors:
        if clusters and a - clusters[-1][-1] <= EDGE_TOL:
            clusters[-1].append(a)
        else:
            clusters.append([a])
    kept = [c for c in clusters if len(c) >= EDGE_MIN_COUNT]
    return [round(mean(c), 2) for c in kept]


def extract_page(pdf_bytes, page_num):
    ws = words.extract_words(pdf_bytes, page_num)
    body = [w for w in ws if BODY_BOTTOM < w.y0 < BODY_TOP]
    lines = [merge_fragments(l) for l in group_lines(body)]

    edges = derive_edges(lines)
    if len(edges) != 11:
        raise RuntimeError(f"p{page_num}: expected 11 numeric column edges, got {len(edges)}: {edges}")

    rows_main, rows_intra, buffer = [], [], []
    for line in lines:
        label = " ".join(t.text for t in line
                         if t.x0 < LABEL_X0_MAX and not NUM_RE.match(t.text)
                         and not DASH_RE.match(t.text)).strip()

        cells = {}
        for t in line:
            if t.x0 <= NOTE_COL_MAX_X0:
                continue
            if not (NUM_RE.match(t.text) or DASH_RE.match(t.text)):
                continue
            idx = min(range(11), key=lambda i: abs(edges[i] - t.anchor))
            if abs(edges[idx] - t.anchor) <= SNAP_TOL:
                cells[idx] = t.text

        if not cells:
            frag = " ".join(t.text for t in line if t.x0 < LABEL_X0_MAX).strip()
            if frag and not any(h in frag for h in
                                ("US$", "FY26", "FY25", "Notes", "Note", "SEGMENT ANALYSIS",
                                 "segment results", "presented as follows", "continued")):
                buffer.append(frag)
            continue

        full = (" ".join(buffer) + " " + label).strip() if buffer else label
        buffer = []
        full = re.sub(r"\s+", " ", full).strip()
        if not full:
            continue
        row = {"label": full, "y": line[0].y0, "cells": cells}
        (rows_intra if line[0].y0 < INTRA_SPLIT_Y else rows_main).append(row)

    return rows_main, rows_intra, edges


def parse_num(raw):
    s = raw.strip()
    if not s or DASH_RE.match(s):
        return None
    s2 = s.replace(",", "")
    if s2.startswith("(") and s2.endswith(")"):
        return -float(s2[1:-1])
    return float(s2)


def run():
    pdf_bytes = PDF_PATH.read_bytes()
    con = sqlite3.connect(str(DB_PATH))
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM cells WHERE table_region IN (?, ?)", (REGION, REGION_INTRA))

        total = 0
        for page in (21, 22, 23, 24):
            rows_main, rows_intra, edges = extract_page(pdf_bytes, page)
            fy = "FY26" if page in (21, 22) else "FY25"
            print(f"p{page} ({fy}): {len(rows_main)} main rows, {len(rows_intra)} intra-group rows")

            for region, rows in ((REGION, rows_main), (REGION_INTRA, rows_intra)):
                for r_idx, row in enumerate(rows, start=1):
                    for col_idx, raw in sorted(row["cells"].items()):
                        cur.execute(
                            """INSERT INTO cells (document, physical_page, table_region, row_label,
                               fiscal_year, unit, column_label, column_index, value_raw, value_num,
                               row_index, extraction_commit)
                               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                            (EXPECTED_SHA, page, region, row["label"], fy, "US$ thousand",
                             COLUMN_LABELS[col_idx], col_idx, raw, parse_num(raw), r_idx,
                             EXTRACTION_COMMIT))
                        total += 1

        con.commit()
        print(f"Inserted {total} Note 3 cells. Total cells in DB: "
              f"{con.execute('SELECT COUNT(*) FROM cells').fetchone()[0]}")
    finally:
        con.close()


if __name__ == "__main__":
    run()
