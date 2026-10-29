import sqlite3
from pathlib import Path

db_path = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/experiment.sqlite")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

for t in ["ledger_questions", "ledger_events", "section_response_attempts"]:
    print(f"\n--- {t} schema ---")
    info = cur.execute(f"PRAGMA table_info({t})").fetchall()
    for col in info:
        print(f"  {col[1]} ({col[2]})")

conn.close()
