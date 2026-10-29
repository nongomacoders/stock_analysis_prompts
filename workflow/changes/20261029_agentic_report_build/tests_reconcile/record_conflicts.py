"""Record reconciliation conflicts from the reconciliation engine into report.sqlite.

Governed by CHARTER covenants:
  - Covenant 1: Never replace a printed source figure. Mismatches are recorded data.
  - Covenant 2: All arithmetic executes in code.
  - Every conflict carries page citations and maps to existing ledger questions
    where relevant.
"""
from __future__ import annotations

import pathlib
import sqlite3
import sys
from decimal import Decimal

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from reconcile_engine import Engine

DB_PATH = pathlib.Path(__file__).resolve().parent.parent / "build" / "report.sqlite"

# Mapping from mismatch characteristics to ledger question IDs
# (imported as open questions at P1)
QUESTION_MAP = {
    # 10,000 oz Barberton FY26 anomaly
    ("Gold produced – total", "FY26"): "Q-1f48aa6d4b884f09",  # linked to group gold produced context
    # FY25 underground double-count / Evander 1,081 buy-in
    ("Gold produced – underground", "FY25"): "Q-e8c872e6edc94d18",
    # MTR FY25 leaf 25,043 vs total 30,806 (5,763 buy-in)
    ("Gold produced – tailings", "FY25"): "Q-3e8730dbd1994205",
    # Elikhulu FY25 all-in anomaly (68,843 printed)
    ("ZAR all-in cost", "FY25"): "Q-f1a4ce3647724ed9",
    # Tennant all-in swing / cross-currency
    ("A$ all-in cost", "FY25"): "Q-ced8d2566db6459c",
    ("A$ all-in cost", "FY26"): "Q-ced8d2566db6459c",
    # APM cost definitions (AISC / AISC excl. buy-in / cash cost cross-currency)
    ("ZAR all-in sustaining costs", "FY26"): "Q-c1e6100f7a674873",
    ("ZAR all-in sustaining costs", "FY25"): "Q-c1e6100f7a674873",
    ("ZAR cash cost", "FY26"): "Q-c1e6100f7a674873",
    ("Average ZAR gold price received – South African operations", "FY26"): "Q-a0b503d7ac044eee",
    ("Average ZAR gold price received – South African operations", "FY25"): "Q-a0b503d7ac044eee",
    ("Average A$ gold price received – Australian operations", "FY26"): "Q-c5e1b41b1cfe4dfb",
    ("Average A$ gold price received – Australian operations", "FY25"): "Q-c5e1b41b1cfe4dfb",
}


def classify_kind(res) -> str:
    """Classify mismatch as source_defect or ambiguity per charter schema."""
    d = abs(res.delta)
    # Known 1-oz rounding or 0.1 rounding printed quirks
    if d in (Decimal("1"), Decimal("0.1")):
        return "ambiguity"
    # Definite arithmetic / typography printed anomalies
    if res.row_label == "ZAR all-in cost" and res.fiscal_year == "FY25" and res.column == 5:
        return "source_defect"
    if res.check_id in ("M3", "M8") and d == Decimal("10000"):
        return "source_defect"
    if res.check_id in ("M2", "M5", "M9") and d == Decimal("5763"):
        return "source_defect"
    if res.check_id in ("M4", "M7", "M9") and d == Decimal("1081"):
        return "source_defect"
    # Cross-currency deviations and structural column shifts
    return "ambiguity"


def record_conflicts():
    eng = Engine(str(DB_PATH))
    results = eng.run_all()
    mismatches = [r for r in results if r.mismatch]

    con = sqlite3.connect(str(DB_PATH))
    try:
        cur = con.cursor()
        # Delete existing reconciliation conflicts (preserve P1 extraction conflicts)
        cur.execute("DELETE FROM conflicts WHERE check_id LIKE '%|%'")

        inserted = 0
        for m in mismatches:
            kind = classify_kind(m)
            qid = QUESTION_MAP.get((m.row_label, m.fiscal_year))
            desc = (f"[{m.family} {m.check_id}] {m.fiscal_year} col{m.column}: "
                    f"'{m.row_label}' printed={m.printed} vs computed={m.computed} "
                    f"(delta={m.delta}). {m.note}".strip())
            evidence = f"reconcile_engine:{m.check_id}:p{m.physical_page}:{m.fiscal_year}:col{m.column}"

            cur.execute("""
                INSERT INTO conflicts (
                    check_id, description, kind, physical_page,
                    evidence_path, ledger_question_id, status
                ) VALUES (?, ?, ?, ?, ?, ?, 'open')
            """, (m.fingerprint, desc, kind, m.physical_page, evidence, qid))
            inserted += 1

        con.commit()
        total_conflicts = con.execute("SELECT COUNT(*) FROM conflicts").fetchone()[0]
        print(f"Recorded {inserted} reconciliation conflicts into {DB_PATH}")
        print(f"Total conflicts in DB: {total_conflicts}")
    finally:
        con.close()


if __name__ == "__main__":
    record_conflicts()
