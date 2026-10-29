"""Extract PAN Primary Financial Statements (physical pages 17 & 18).

Target Statements:
  - Physical Page 17 (left spread): Statement of Financial Position (Assets)
  - Physical Page 17 (right spread): Statement of Financial Position (Equity & Liabilities)
  - Physical Page 18 (left spread): Statement of Profit or Loss and Other Comprehensive Income
  - Physical Page 18 (right spread): Statement of Cash Flows

Extracted into report.sqlite cells table with:
  table_region, physical_page, row_label, fiscal_year, unit, column_index, column_label,
  value_raw, value_num, row_index, extraction_commit
"""
from __future__ import annotations

import pathlib
import re
import sqlite3
import sys

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here))
import words

DB_PATH = here.parents[0] / "report.sqlite"
PDF_PATH = pathlib.Path(r"companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")
EXPECTED_SHA = "62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd"
EXTRACTION_COMMIT = "p1_primary_statements_v1"

SPLIT_X = 420.0  # boundary separating left statement from right statement on both spreads


def parse_cell(raw: str):
    s = raw.strip()
    if not s or s in ("–", "—", "-"):
        return None
    s2 = s.replace(" ", "").replace(",", "")
    if s2.startswith("(") and s2.endswith(")"):
        return -float(s2[1:-1])
    return float(s2)


def is_valid_numeric_token(text: str) -> bool:
    """Check if token is a valid printed number or nil token."""
    s = text.strip()
    if s in ("–", "—", "-"):
        return True
    s2 = s.replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace(" ", "")
    return s2.isdigit()


def clean_label(label: str) -> str:
    """Normalize extracted statement line labels."""
    l = label.strip()
    # Remove section header prefixes that got prepended before the first row
    prefixes_to_strip = [
        "O F FI NANCIAL POSITI O N ASSETS Non-current assets",
        "ASSETS Non-current assets",
        "Non-current assets",
        "Current assets",
        "EQUITY AND LIABILITIES",
        "Non-current liabilities",
        "Current liabilities",
        "Cash flows from operating activities",
        "Cash flows from investing activities",
        "Cash flows from financing activities",
        "Other comprehensive income Items that may be reclassified to profit or loss",
        "Items that may be reclassified to profit or loss",
        "Items that may not be reclassified to profit or loss",
    ]
    for p in prefixes_to_strip:
        if l.startswith(p + " "):
            l = l[len(p) + 1:].strip()
        elif l == p:
            l = l
    return l


def extract_spread_rows(pdf_bytes: bytes, page_num: int, is_right: bool):
    """Extract metric rows from one half of a landscape spread."""
    all_words = words.extract_words(pdf_bytes, page_num)
    if is_right:
        ws = [w for w in all_words if w.x0 >= SPLIT_X and 70.0 <= w.y0 < 480.0]
        col_fy26_min, col_fy26_max = 710.0, 755.0
        col_fy25_min, col_fy25_max = 770.0, 815.0
        label_max = 670.0
    else:
        ws = [w for w in all_words if w.x0 < SPLIT_X and 70.0 <= w.y0 < 480.0]
        col_fy26_min, col_fy26_max = 290.0, 335.0
        col_fy25_min, col_fy25_max = 345.0, 395.0
        label_max = 250.0

    # Cluster words into lines by y0
    ws.sort(key=lambda w: (-w.y0, w.x0))
    lines = []
    for w in ws:
        matched = False
        for l in lines:
            if abs(l[0].y0 - w.y0) <= 3.2:
                l.append(w)
                matched = True
                break
        if not matched:
            lines.append([w])

    for l in lines:
        l.sort(key=lambda w: w.x0)

    rows = []
    pending_label_parts = []
    for l in lines:
        line_str = " ".join(w.text for w in l)
        # Skip headers / metadata lines
        if any(h in line_str for h in ("SUMMARISED", "STATEMENT", "for the year", "as at 30 June 2026", "thousand Notes", "thousand Note", "PAN AFRICAN", "audited results")):
            continue

        fy26_words = [w for w in l if col_fy26_min <= w.x0 <= col_fy26_max and is_valid_numeric_token(w.text)]
        fy25_words = [w for w in l if col_fy25_min <= w.x0 <= col_fy25_max and is_valid_numeric_token(w.text)]
        label_words = [w for w in l if w.x1 <= label_max]

        fy26_raw = "".join(w.text for w in fy26_words) if fy26_words else None
        fy25_raw = "".join(w.text for w in fy25_words) if fy25_words else None
        curr_label = " ".join(w.text for w in label_words).strip()

        if fy26_raw or fy25_raw:
            if pending_label_parts:
                full_label = (" ".join(pending_label_parts) + " " + curr_label).strip()
                pending_label_parts = []
            else:
                full_label = curr_label
            clean_lab = clean_label(full_label)
            rows.append({
                "y": l[0].y0,
                "label": clean_lab,
                "FY26": fy26_raw or "–",
                "FY25": fy25_raw or "–",
            })
        else:
            if curr_label:
                pending_label_parts.append(curr_label)

    return rows


def run_extraction():
    con = sqlite3.connect(str(DB_PATH))
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM cells WHERE table_region LIKE 'primary_%'")

        pdf_bytes = PDF_PATH.read_bytes()

        statements = [
            (17, False, "primary_balance_sheet_assets", "Statement of Financial Position - Assets"),
            (17, True, "primary_balance_sheet_equity_liab", "Statement of Financial Position - Equity & Liabilities"),
            (18, False, "primary_income_statement", "Statement of Profit or Loss and Other Comprehensive Income"),
            (18, True, "primary_cash_flows", "Statement of Cash Flows"),
        ]

        inserted_cells = 0
        for page_num, is_right, region, region_desc in statements:
            rows = extract_spread_rows(pdf_bytes, page_num, is_right)
            print(f"Extracted {len(rows)} metric rows for {region_desc} (p.{page_num}, right={is_right})")
            for r_idx, r in enumerate(rows, start=1):
                lab = r["label"]
                for cyc in ("FY26", "FY25"):
                    raw = r[cyc]
                    num = parse_cell(raw)
                    unit = "US cents" if "earnings per share" in lab.lower() else "US$ thousand"
                    cur.execute("""
                        INSERT INTO cells (
                            document, physical_page, table_region, row_label,
                            fiscal_year, unit, column_label, column_index,
                            value_raw, value_num, row_index, extraction_commit
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        EXPECTED_SHA, page_num, region, lab,
                        cyc, unit, cyc, 0 if cyc == "FY26" else 1,
                        raw, num, r_idx, EXTRACTION_COMMIT
                    ))
                    inserted_cells += 1

        con.commit()
        print(f"Successfully inserted {inserted_cells} cells for Primary Financial Statements.")
        total_cells = con.execute("SELECT COUNT(*) FROM cells").fetchone()[0]
        print(f"Total cells in report.sqlite: {total_cells}")
    finally:
        con.close()


if __name__ == "__main__":
    run_extraction()
