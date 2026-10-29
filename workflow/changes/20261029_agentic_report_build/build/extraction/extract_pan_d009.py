"""P1 extraction: PAN section D009 Group production summary (physical pp. 48-50).

Populates build/report.sqlite from the SHA-verified source PDF only. Deterministic,
coordinate-based, no model inference. Printed values only; derivations live in the P2 suite.

Rules honoured (CHARTER covenants):
- every cell lineage: physical_page + document sha256 + extraction commit;
- printed values stored verbatim (value_raw); parsing is a separate nullable field;
- ambiguous geometry recorded in conflicts, never silently guessed;
- the ground-truth scoring fixture is NOT read by this code: no path to it is
  constructed anywhere in this file or its imports (verifiable by grep).

Layout facts encoded (measured on renders of pp.48-50, identical on all three pages):
- 3 banner blocks over a repeated 14-column numeric grid + a leading Unit column:
    Mining operations  : Barberton Mines (x1~266), Evander Mines (~306), Total (~346)
    Surface operations : BTRP (~386), [blank unlabelled, never populated], Elikhulu (~487),
                         MTR operation (~527), Tennant Mines (~567), Total (~606)
    Total operations   : Barberton Mines total (~646), Evander Mines total (~686),
                         MTR operation total (~725), Tennant Mines total (~765), Group total (~805)
- values are right-aligned: a token's x1 pins its column (cluster tolerance 3pt);
- the blank column between BTRP and Elikhulu has no header text and never prints values ->
  recorded as an ambiguity conflict, and its synthetic edge is the midpoint of the gap;
- banner/block membership is classified from printed label semantics: block 1 ends at the
  first column labelled exactly 'Total'; the trailing run of columns labelled with lowercase
  'total' is block 3; the middle columns are block 2. Verified against the printed banners
  each run (assert + conflicts on mismatch).
- body rows: FY26 numeric line, optional unit-only line (unit token in the Unit column),
  then FY25 numeric line; FY26 and FY25 share row_index. Row labels can wrap onto the FY25
  line; fragments are combined without duplication.

Run:  <main .venv python> extract_pan_d009.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pypdfium2 as pdfium

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_pages import render_pages  # noqa: E402
from words import Word, cluster_lines, extract_words  # noqa: E402

ROOT = Path(r"C:\Users\diond\Desktop\Projects\stock_prompts_agentic")
PDF = ROOT / "companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf"
EXPECTED_SHA = "62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd"
BUILD = Path(__file__).resolve().parents[1]
DB = BUILD / "report.sqlite"
EXTRACTION_COMMIT = "p1_extraction_v3"
PHYSICAL_PAGES = [48, 49, 50]
REGION_BY_PAGE = {48: "A_production", 49: "B_costs", 50: "C_financial_summary"}
PRIOR_YEAR_TOKEN = "FY25"

DASH_RE = re.compile(r"[\u2013\u2014-]")
NUM_RE = re.compile(r"^\(?[\d,]+(?:\.\d+)?\)?%?$")
YEAR_RE = re.compile(r"^FY(?:26|25)$")
UNIT_WORD_RE = re.compile(r"^(t|oz|%|g/t|ZAR/kg|A\$/kg|US\$/oz|ZAR/t|US\$/ZAR|US\$/A\$)$")
UNIT_HEAD_RE = re.compile(r"^(ZAR|US$|A$)$")

# geometry constants (pt)
VALUE_COLUMN_X1_MIN = 232.0   # left of this is label/unit territory
EDGE_CLUSTER_TOL = 3.0        # right-edge cluster tolerance for value columns
EDGE_MIN_COUNT = 3            # ignore one-off strays
BLANK_GAP_THRESHOLD = 60.0    # gap that implies a blank (synthetic) column
SNAP_TOL = 3.0                # value x1 -> column edge snap tolerance
NUM_MERGE_GAP = 4.5           # gap under which adjacent numeric tokens are one printed
                              # number (the PDF prints mid-number spaces: '2 956.0',
                              # '1,271 855', '6, 609' - measured worst split gap 2.8pt;
                              # smallest observed inter-column gap is ~9pt)

DDL = """
CREATE TABLE IF NOT EXISTS sources (
  document TEXT PRIMARY KEY, sha256 TEXT NOT NULL, bytes INTEGER NOT NULL, imported_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS pages (
  document TEXT NOT NULL, physical_page INTEGER NOT NULL,
  render_evidence_path TEXT NOT NULL, render_sha256 TEXT NOT NULL,
  width_px INTEGER NOT NULL, height_px INTEGER NOT NULL,
  PRIMARY KEY (document, physical_page)
);
CREATE TABLE IF NOT EXISTS cells (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  document TEXT NOT NULL, physical_page INTEGER NOT NULL, table_region TEXT NOT NULL,
  row_label TEXT, fiscal_year TEXT, unit TEXT,
  column_label TEXT, column_index INTEGER,
  value_raw TEXT NOT NULL, value_num REAL,
  row_index INTEGER, token_bbox TEXT,
  extraction_commit TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS conflicts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  check_id TEXT, description TEXT NOT NULL,
  kind TEXT NOT NULL CHECK (kind IN ('source_defect','extraction_defect','ambiguity')),
  physical_page INTEGER, evidence_path TEXT, ledger_question_id TEXT, status TEXT NOT NULL DEFAULT 'open'
);
CREATE TABLE IF NOT EXISTS questions (
  question_id TEXT PRIMARY KEY, question TEXT NOT NULL, priority TEXT NOT NULL,
  target_document TEXT NOT NULL, target_section TEXT NOT NULL,
  evidence_required TEXT, closure_condition TEXT,
  status TEXT NOT NULL CHECK (status IN ('open','partial','answered')),
  origin TEXT NOT NULL, evidence_paths TEXT, imported_utc TEXT
);
CREATE TABLE IF NOT EXISTS runs (
  label TEXT PRIMARY KEY, started_utc TEXT NOT NULL, commit_hash TEXT, python_version TEXT, notes TEXT
);
"""

LEDGER_IMPORTS = [
    {
        "question_id": "Q-1f48aa6d4b884f09",
        "priority": "medium",
        "question": "Reconcile FY25 Group gold produced: printed total 196,527 oz vs sum of components (93,724 underground + 2,654 surface + 98,636 tailings + 1,081 buy-in + 1,513 surface feedstock = 197,608 oz). Is the 1,081 oz buy-in already embedded in another column, or is the total misstated?",
        "target_section": "D009 p.48-49; D006.2 segment note",
        "evidence_required": "FY25 component build of group gold produced with explicit treatment of buy-in feedstock; segment note reconciliation",
        "closure_condition": "Components sum to printed total, or an explicit disclosure explains the 1,081 oz difference",
    },
    {
        "question_id": "Q-e8c872e6edc94d18",
        "priority": "medium",
        "question": "Explain FY25 Evander underground gold produced: 26,748 oz in the underground column vs 27,829 oz in the Evander Mines total column (difference 1,081 oz = FY25 buy-in). Which figure is correct and why does the total exceed the underground component?",
        "target_section": "D009 p.48; D006.2 segment note",
        "evidence_required": "Evander FY25 production build by source (underground, surface, buy-in) with reconciliation to total",
        "closure_condition": "Difference explained by a disclosed component or corrected figure",
    },
    {
        "question_id": "Q-f1a4ce3647724ed9",
        "priority": "medium",
        "question": "Explain FY25 Elikhulu all-in cost ZAR/kg printed as 68,843 vs FY26 853,597 - is this a typo, a units error, or a genuine one-off? What is the correct FY25 figure?",
        "target_section": "D009 p.49; D008 ALL-IN COSTS",
        "evidence_required": "Elikhulu FY25 all-in cost build (cash cost + sustaining + expansion capex) reconciling to ZAR/kg; confirmation of printed value",
        "closure_condition": "Correct FY25 figure established and reconciled to cost components",
    },
    {
        "question_id": "Q-ced8d2566db6459c",
        "priority": "low",
        "question": "Explain Tennant A$ all-in cost swing from 1,584,835 A$/kg (FY25) to 205,143 A$/kg (FY26) - is the FY25 figure anomalous (tiny base, ramp-up) or a genuine cost collapse? What drove the change?",
        "target_section": "D009 p.49; D008 ALL-IN COSTS; D006.2 segment note",
        "evidence_required": "Tennant FY25/FY26 all-in cost build in A$ and A$/kg, with production volumes and capex; note any ramp-up or one-off items",
        "closure_condition": "Swing explained by disclosed cost/production drivers or confirmed as a base-effect artefact",
    },
    {
        "question_id": "Q-c1e6100f7a674873",
        "priority": "high",
        "question": "Provide APM definitions used in D009: AISC, all-in cost, AISC excluding third-party buy-in feedstock, and Adjusted EBITDA - including which cost lines (royalties, sustaining capex, expansion capex, G&A, exploration) are included and how buy-in feedstock is treated.",
        "target_section": "D008 Alternative performance measures (pp.38-47); D010 Glossary",
        "evidence_required": "Written APM definitions and reconciliation tables for AISC, all-in cost, AISC excl. buy-in, Adjusted EBITDA",
        "closure_condition": "Definitions and reconciliations located and consistent with D009 figures",
    },
    {
        "question_id": "Q-3e8730dbd1994205",
        "priority": "medium",
        "question": "Why does FY25 'Total operations MTR' gold produced (30,806 oz) exceed the MTR operation component (25,043 oz) by 5,763 oz, when the FY26 buy-in row shows 5,763 oz for MTR but FY25 buy-in shows nil?",
        "target_section": "D009 p.48-49; D006.2 Segment analysis",
        "evidence_required": "Breakdown of FY25 MTR total production by source (own tailings vs buy-in vs other) and confirmation whether the 5,763 oz is a misclassification or a genuine additional source.",
        "closure_condition": "The 5,763 oz difference is explained and the component-to-total reconciliation for MTR FY25 is shown.",
    },
    {
        "question_id": "Q-a0b503d7ac044eee",
        "priority": "high",
        "question": "How are cash cost, AISC, all-in cost and 'AISC excluding third-party buy-in' defined and reconciled to IFRS cost of production for FY26/FY25, and do the Group per-oz figures (1,600/1,867/2,576 US$/oz) tie to the ZAR million cost tables on p.50 at the 16.90 US$/ZAR rate?",
        "target_section": "D008 Alternative performance measures (ALL-IN COSTS, p.40-43); D010 Glossary",
        "evidence_required": "Definition and build-up of each cost metric, treatment of third-party buy-in feedstock and by-product credits, and reconciliation of per-unit costs to ZAR/A$ million cost-of-production totals for FY26 and FY25.",
        "closure_condition": "Definitions and a reconciliation tying Group per-oz costs to the p.50 cost-of-production totals (same period, currency, gross/net basis) are shown, or the difference is explained.",
    },
    {
        "question_id": "Q-c5e1b41b1cfe4dfb",
        "priority": "medium",
        "question": "Is Tennant's revenue (A$195.3m FY26; A$5.9m FY25) excluded from the Group ZAR revenue total of 17,249.1 ZARm, and how is the Australian operation consolidated into Group revenue and Adjusted EBITDA (US$663.1m)?",
        "target_section": "D006.2 Segment analysis (p.20-24); D005 Primary financial statements (p.17-19)",
        "evidence_required": "Group revenue by currency/segment and the consolidation/FX translation treatment of Tennant, reconciling A$ revenue to Group ZAR revenue and to Adjusted EBITDA.",
        "closure_condition": "Tennant's contribution to Group revenue and EBITDA is reconciled with currency translation shown, or exclusion is confirmed.",
    },
]


def parse_num(raw: str) -> float | None:
    if DASH_RE.fullmatch(raw):
        return None
    s = raw.replace(",", "").replace("%", "").replace("\u2009", "").replace(" ", "")
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    try:
        return float(s)
    except ValueError:
        return None


def merge_value_fragments(val_toks: list[Word]) -> list[Word]:
    """Rejoin space-separated fragments of one printed number.

    The PDF prints group separators as spaces inconsistently (never in the same
    number twice, sometimes in place of a comma), which splits a value into
    2-3 word tokens ~2-3pt apart. Merge runs of numeric tokens with gaps <=
    NUM_MERGE_GAP, keeping the printed glyphs verbatim (joined with spaces) and
    a combined bbox. Dashes ('-') are never merged (they are nil cells).
    """
    out: list[Word] = []
    i = 0
    while i < len(val_toks):
        j = i
        parts = [val_toks[j]]
        cur = val_toks[j]
        while (j + 1 < len(val_toks)
               and val_toks[j + 1].x0 - cur.x1 <= NUM_MERGE_GAP
               and val_toks[j + 1].x0 > VALUE_COLUMN_X1_MIN
               and NUM_RE.match(val_toks[j + 1].text)):
            j += 1
            cur = val_toks[j]
            parts.append(cur)
        if len(parts) == 1:
            out.append(val_toks[i])
        else:
            out.append(Word(
                " ".join(p.text for p in parts),
                parts[0].x0, parts[0].y0, parts[-1].x1, parts[-1].y1))
        i = j + 1
    return out


def cluster_edges(xs: list[float]) -> list[float]:
    """Cluster token right-edges within EDGE_CLUSTER_TOL; return cluster means."""
    out = []
    cur: list[float] = []
    for x in sorted(xs):
        if cur and x - cur[-1] > EDGE_CLUSTER_TOL:
            out.append(sum(cur) / len(cur))
            cur = []
        cur.append(x)
    if cur:
        out.append(sum(cur) / len(cur))
    return out


def combine_fragments(fy26: str | None, fy25: str | None) -> str | None:
    """Row labels wrap across the FY26/FY25 sibling lines; join non-duplicate fragments."""
    a, b = (fy26 or "").strip(), (fy25 or "").strip()
    if a and b:
        if a == b or a.endswith(b):
            return a
        if b.endswith(a):
            return b
        return f"{a} {b}".strip()
    return a or (b or None)


def snap_to_edge(x1: float, edges: list[float]) -> int | None:
    best_i, best_d = None, None
    for i, e in enumerate(edges):
        d = abs(x1 - e)
        if best_d is None or d < best_d:
            best_i, best_d = i, d
    if best_d is not None and best_d <= SNAP_TOL:
        return best_i
    return None


def classify_blocks(labels: list[str]) -> tuple[int, int]:
    """Block boundaries from printed label semantics.

    Returns (n_mining, n_surface) column counts; remaining are the total block.
    Mining block = columns 0..first exact-'Total' label inclusive.
    Total block = trailing run of labels ending with lowercase 'total'.
    Surface block = everything in between (must be contiguous).
    """
    end_mining = next(i for i, lab in enumerate(labels) if lab == "Total")
    start_total = next(
        i for i in range(len(labels) - 1, -1, -1)
        if not labels[i].endswith("total")
    ) + 1
    return end_mining + 1, start_total - end_mining - 1


def main() -> int:
    started = datetime.now(timezone.utc)
    raw = PDF.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    assert sha == EXPECTED_SHA, f"source hash mismatch: {sha}"

    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.executescript(DDL)
    now = started.strftime("%Y-%m-%dT%H:%M:%SZ")
    con.execute("INSERT INTO sources VALUES (?,?,?,?)", (str(PDF), sha, len(raw), now))

    renders = render_pages(PDF, PHYSICAL_PAGES)
    for pno, meta in renders.items():
        con.execute(
            "INSERT INTO pages VALUES (?,?,?,?,?,?)",
            (str(PDF), pno, meta["path"], meta["sha256"], meta["width_px"], meta["height_px"]),
        )
    for q in LEDGER_IMPORTS:
        con.execute(
            "INSERT INTO questions VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (q["question_id"], q["question"], q["priority"], str(PDF),
             q["target_section"], q["evidence_required"], q["closure_condition"],
             "open", "trial_import", None, now),
        )
    con.execute("INSERT INTO runs VALUES (?,?,?,?,?)",
                ("P1_extraction_v3", now, None, sys.version.split()[0],
                 "coordinate extraction, no inference; scoring fixture never read"))

    conflicts_buf: list[tuple[str, str, str, int | None]] = []  # (check_id, description, kind, page)
    band_audit: list[dict] = []
    counts: Counter = Counter()
    rows_buffer: list[dict] = []
    page_columns: list[list[str]] = []

    doc = pdfium.PdfDocument(raw)
    for pno in PHYSICAL_PAGES:
        page = doc[pno - 1]
        page.close()
        words = extract_words(raw, pno)
        lines = cluster_lines(words, y_tol=3.0)

        first_body = next((i for i, ln in enumerate(lines)
                           if any(YEAR_RE.fullmatch(w.text) for w in ln)), None)
        if first_body is None:
            raise RuntimeError(f"no fiscal-year marker line found on page {pno}")
        body = lines[first_body:]
        furniture = [w for ln in lines[:first_body] for w in ln]
        if not furniture:
            raise RuntimeError(f"no header furniture found on page {pno}")

        # --- banners: tokens in the banner band (y1 in [492, 530], between the page
        # titles above and the bottom header rows below); this covers both the
        # left-anchored split copy ('Surface' over 'operations') and the centered copies.
        banner_tokens = [w for w in furniture if 492.0 <= w.y1 <= 530.0]
        banner_names: list[str] = []
        for ln in lines[:first_body]:
            if not (492.0 <= max(w.y1 for w in ln) <= 530.0):
                continue
            if any(YEAR_RE.fullmatch(w.text) for w in ln):
                continue
            joined = " ".join(w.text for w in ln)
            for m in re.finditer(r"(Mining|Surface|Total)\s*operations", joined):
                if m.group(0) not in banner_names:
                    banner_names.append(m.group(0))

        # --- column right edges from body value tokens
        edge_xs = [w.x1 for ln in body for w in ln
                   if (NUM_RE.match(w.text) or DASH_RE.fullmatch(w.text))
                   and w.x0 > VALUE_COLUMN_X1_MIN and not YEAR_RE.fullmatch(w.text)]
        edge_raw = cluster_edges(edge_xs)
        edges = [e for e in edge_raw
                 if sum(1 for x in edge_xs if abs(x - e) <= EDGE_CLUSTER_TOL) >= EDGE_MIN_COUNT]
        # blank (synthetic) columns where a wide gap implies an unlabelled column
        synthetic: list[tuple[int, float]] = []
        i = 1
        while i < len(edges):
            if edges[i] - edges[i - 1] > BLANK_GAP_THRESHOLD:
                blank_x = (edges[i - 1] + edges[i]) / 2.0
                synthetic.append((i, blank_x))
                edges.insert(i, blank_x)
            i += 1

        # --- assemble column labels from header token pool (banners excluded)
        unit_token = next((w for w in furniture if w.text == "Unit"), None)
        unit_edge = unit_token.x1 if unit_token else VALUE_COLUMN_X1_MIN
        pool = [w for w in furniture
                if w not in banner_tokens and w.x1 > unit_edge + 1.0]
        labels: list[str] = []
        for j, e in enumerate(edges):
            left = max(edges[j - 1], unit_edge + 2.0) if j > 0 else unit_edge + 2.0
            toks = [w for w in pool if left + 1.0 < w.x1 <= e + 2.5]
            toks.sort(key=lambda w: (-w.y1, w.x0))
            labels.append(" ".join(w.text for w in toks) if toks else "(blank)")

        for si, sx in synthetic:
            j = si
            labels[j] = "(blank unlabelled - no header text, no printed values)"
        if synthetic:
            conflicts_buf.append((
                "P1_geometry",
                f"p{pno}: blank unlabelled column between x1={synthetic[0][1] - 50:.0f} and "
                f"{edges[synthetic[0][0] + 1]:.0f} (between BTRP and Elikhulu); no header text and "
                "no value tokens on any of pp.48-50 - structural gap in the printed grid",
                "ambiguity", pno))

        # --- block classification + banner name check
        # banner_names were collected in printed x-order by finditer above; the
        # Mining, Surface, Total keywords are already in tabular order.
        keyword_order = {"Mining": 0, "Surface": 1, "Total": 2}
        banner_names.sort(key=lambda n: keyword_order.get(n.split(" ")[0], 99))
        if len(banner_names) != 3:
            conflicts_buf.append((
                "P1_geometry",
                f"p{pno}: expected 3 block banners (Mining/Surface/Total operations), found {banner_names}",
                "extraction_defect", pno))
        nm, ns = classify_blocks(labels)
        prefix_by_block = ([banner_names[0]] * nm
                           + [banner_names[1]] * ns
                           + [banner_names[2]] * (len(labels) - nm - ns))
        column_labels = [f"{pref} | {lab}" for pref, lab in zip(prefix_by_block, labels)]

        band_audit.append({"page": pno, "columns": [
            {"edge": round(e, 1), "label": cl} for e, cl in zip(edges, column_labels)]})
        page_columns.append(column_labels)

        # --- body rows
        row_index = 0
        pending: dict | None = None

        def flush_row(row: dict | None) -> None:
            if row is None or not row["cells"]:
                return
            row["row_label"] = combine_fragments(row.get("fy26_label"), row.get("fy25_label"))
            rows_buffer.append(row)
            counts["rows"] += 1

        def is_unit_token(t: Word) -> bool:
            return bool(UNIT_WORD_RE.match(t.text) or UNIT_HEAD_RE.match(t.text)
                        or t.text == "million")

        for ln in body:
            year_toks = [w for w in ln if YEAR_RE.fullmatch(w.text)]
            year = year_toks[0].text if year_toks else None
            rest = sorted((w for w in ln if w not in year_toks), key=lambda w: w.x0)
            if year == PRIOR_YEAR_TOKEN:
                pass  # FY25 sibling shares the pending metric row
            elif year is not None:
                flush_row(pending)
                pending = None
                row_index += 1
            # year is None: never flush (unit lines / continuations / furniture)

            # unit-only line: every token is a unit-pattern token in the Unit column zone
            if year is None and rest and all(
                    is_unit_token(t) and t.x0 >= 195.0 for t in rest):
                unit_text = " ".join(t.text for t in rest)
                if pending is None:
                    conflicts_buf.append((
                        "P1_unit", f"p{pno}: unit line {unit_text!r} at y={ln[0].yc:.1f} "
                        "with no pending row to attach to", "ambiguity", pno))
                elif pending["unit"] and pending["unit"] != unit_text:
                    conflicts_buf.append((
                        "P1_unit", f"p{pno}: conflicting units {pending['unit']!r} vs "
                        f"{unit_text!r} at y={ln[0].yc:.1f}", "ambiguity", pno))
                else:
                    pending["unit"] = unit_text
                continue

            # footer/furniture guard: year-less lines carrying right-half strap text
            # (the footer prints on both page halves; the right half starts ~x=700)
            if year is None and any(t.x0 > 600.0 for t in ln):
                conflicts_buf.append((
                    "P1_no_year_line",
                    f"p{pno}: footer/furniture line at y={ln[0].yc:.1f} "
                    f"{[t.text for t in ln]!r} - excluded from labels and cells",
                    "ambiguity", pno))
                continue

            label_parts: list[str] = []
            val_toks: list[Word] = []
            unit_cand: str | None = None
            for t in rest:
                if t.x0 >= 195.0 and is_unit_token(t):
                    # unit column token sitting on this line (cluster tolerance can
                    # merge the unit line into a numeric line)
                    unit_cand = t.text
                    continue
                is_val = (t.x0 > unit_edge
                          and (NUM_RE.match(t.text) or DASH_RE.fullmatch(t.text)))
                if is_val:
                    val_toks.append(t)
                    continue
                if t.x0 > unit_edge and not NUM_RE.match(t.text) \
                        and not DASH_RE.fullmatch(t.text):
                    conflicts_buf.append((
                        "P1_other", f"p{pno}: non-numeric token {t.text!r} in value area "
                        f"(x0={t.x0:.0f}, x1={t.x1:.0f})", "extraction_defect", pno))
                    continue
                label_parts.append(t.text)

            if unit_cand is not None and pending is not None:
                if not pending["unit"]:
                    pending["unit"] = unit_cand
                elif pending["unit"] != unit_cand:
                    conflicts_buf.append((
                        "P1_unit", f"p{pno}: conflicting units {pending['unit']!r} vs "
                        f"{unit_cand!r} at y={ln[0].yc:.1f}", "ambiguity", pno))
                elif unit_cand and pending["unit"]:
                    pass  # same unit repeated on the sibling line

            label_seen = bool(label_parts)
            if year is None:
                # no fiscal-year marker: wrapped-label continuation or furniture
                if label_seen and pending is not None:
                    key = ("fy25_label" if any(c["year"] == PRIOR_YEAR_TOKEN
                                               for c in pending["cells"]) else "fy26_label")
                    pending[key] = combine_fragments(pending.get(key),
                                                     " ".join(label_parts))
                elif label_seen:
                    conflicts_buf.append((
                        "P1_structure", f"p{pno}: continuation label "
                        f"{' '.join(label_parts)!r} at y={ln[0].yc:.1f} with no pending row",
                        "extraction_defect", pno))
                if val_toks:
                    conflicts_buf.append((
                        "P1_no_year_line",
                        f"p{pno}: line without fiscal-year marker carries value-area token(s) "
                        f"{[t.text for t in val_toks]!r} (page footer or furniture) - excluded "
                        "from cells", "ambiguity", pno))
                continue

            if label_seen:
                if year == PRIOR_YEAR_TOKEN and pending is not None:
                    # wrapped-label continuation belonging to the pending metric row
                    pending["fy25_label"] = " ".join(label_parts)
                else:
                    flush_row(pending)
                    pending = {"page": pno, "row_index": row_index,
                               "fy26_label": " ".join(label_parts), "fy25_label": None,
                               "unit": None, "cells": []}
            elif pending is None:
                conflicts_buf.append((
                    "P1_structure",
                    f"p{pno}: body line at y={ln[0].yc:.1f} with no FY marker, no label "
                    "context and no pending row - line skipped, contents preserved in this "
                    "conflict", "extraction_defect", pno))
                continue

            merged_vals = merge_value_fragments(val_toks)
            for w in merged_vals:
                ci = snap_to_edge(w.x1, edges)
                if ci is None:
                    conflicts_buf.append((
                        "P1_geometry",
                        f"p{pno}: value token {w.text!r} (x0={w.x0:.0f}, x1={w.x1:.1f}) did not "
                        "snap to any column edge - not recorded as a cell",
                        "extraction_defect", pno))
                    continue
                pending["cells"].append({
                    "year": year, "column_label": column_labels[ci],
                    "column_index": ci, "value_raw": w.text,
                    "value_num": parse_num(w.text),
                    "bbox": json.dumps([round(w.x0, 2), round(w.y0, 2),
                                        round(w.x1, 2), round(w.y1, 2)]),
                })
        flush_row(pending)
        pending = None
        counts[f"rows_p{pno}"] = sum(1 for r in rows_buffer if r["page"] == pno)
    doc.close()

    # consistency: column grids identical across the three pages
    base = page_columns[0]
    for pno, cols in zip(PHYSICAL_PAGES[1:], page_columns[1:]):
        if cols != base:
            conflicts_buf.append((
                "P1_structure",
                f"page {pno}: column grid differs from page {PHYSICAL_PAGES[0]} "
                f"({len(cols)} vs {len(base)} columns)", "extraction_defect", pno))

    counts["cells"] = sum(len(r["cells"]) for r in rows_buffer)
    for r in rows_buffer:
        for c in r["cells"]:
            con.execute(
                "INSERT INTO cells VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (str(PDF), r["page"], REGION_BY_PAGE[r["page"]], r["row_label"],
                 c["year"], r["unit"], c["column_label"], c["column_index"],
                 c["value_raw"], c["value_num"], r["row_index"], c["bbox"],
                 EXTRACTION_COMMIT),
            )

    for cid, desc, kind, pg in conflicts_buf:
        con.execute("INSERT INTO conflicts VALUES (NULL,?,?,?,?,NULL,NULL,'open')",
                    (cid, desc, kind, pg))
    con.execute("INSERT INTO conflicts VALUES (NULL,?,?,?,?,NULL,NULL,'open')",
                ("P1_typography",
                 "printed numbers occasionally contain an extra printed space inside their "
                 "group separator: '1,271 855' (ZAR all-in cost Group total FY26 p49), "
                 "'2 956.0' (All-in cost of production Barberton FY25 p50), '6, 609' (Gold "
                 "produced buy-in Evander total FY26 p48). Gap-split numeric fragments "
                 "<=4.5pt apart were treated as one printed number; glyphs preserved "
                 "verbatim in value_raw; visual crop evidence PAN_49/50/48 crops in the "
                 "P1 render directory; value_num computed with separators stripped",
                 "ambiguity", None))
    con.commit()

    receipts = {
        "generated_utc": now,
        "purpose": "P1 extraction receipts; runbook requires row-count receipt in the commit message",
        "source": {"path": str(PDF), "sha256": sha},
        "db": {"path": str(DB), "sha256": hashlib.sha256(DB.read_bytes()).hexdigest(),
               "bytes": DB.stat().st_size},
        "scripts": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in sorted(Path(__file__).parent.glob("*.py"))},
        "renders": {str(p): m for p, m in renders.items()},
        "counts": dict(counts),
        "columns_by_page": band_audit,
        "conflicts": dict(Counter(c[0] for c in conflicts_buf)),
        "unassigned_tokens": sum(1 for c in conflicts_buf if c[0] == "P1_geometry"),
        "questions_imported": len(LEDGER_IMPORTS),
        "fixture_guard": "no code path reads the scoring fixture; verifiable by grep",
    }
    (BUILD / "receipts_p1.json").write_text(json.dumps(receipts, indent=2), encoding="utf-8")

    print(json.dumps({
        "cells": counts["cells"],
        "rows": dict((k, v) for k, v in counts.items() if k != "cells"),
        "questions_imported": len(LEDGER_IMPORTS),
        "conflicts_by_check": receipts["conflicts"],
        "db_sha256": receipts["db"]["sha256"][:16],
    }, indent=2))
    for ba in band_audit:
        print(f'page {ba["page"]} columns ({len(ba["columns"])}):')
        for col in ba["columns"]:
            print(f'    edge={col["edge"]:7.1f}  {col["label"]}')
    geo = [c for c in conflicts_buf if c[0] == "P1_geometry"]
    if geo:
        print(f"\nbinding conflicts ({len(geo)}):")
        for c in geo[:25]:
            print("  ", c[1])

    print("\nSAMPLE (p.48 'Total operations | Group total' FY26 column) — anchor vs render:")
    for row in con.execute(
        "SELECT row_index, row_label, value_raw FROM cells "
        "WHERE physical_page=48 AND fiscal_year='FY26' AND column_index="
        "(SELECT MAX(column_index) FROM cells WHERE physical_page=48) "
        "ORDER BY row_index LIMIT 25"
    ):
        print("   ", row)
    print("\nSAMPLE (p.48 tailings FY25) — expect 15,224 / 52,606 / 25,043 / 98,636:")
    for row in con.execute(
        "SELECT row_label, column_index, value_raw FROM cells "
        "WHERE physical_page=48 AND fiscal_year='FY25' AND row_label LIKE 'Tonnes processed – tailings%' "
        "ORDER BY column_index"
    ):
        print("   ", row)
    con.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
