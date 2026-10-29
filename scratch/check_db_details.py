import sqlite3
from pathlib import Path

db_path = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/experiment.sqlite")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Check question status counts
q_status = cur.execute("SELECT status, count(*) FROM ledger_questions GROUP BY status").fetchall()
print("ledger_questions by status:", q_status)

# Check section_response_attempts
cols_att = [d[0] for d in cur.execute("PRAGMA table_info(section_response_attempts)").fetchall()]
print("section_response_attempts columns:", cols_att)
attempts = cur.execute("SELECT attempt_type, is_valid, count(*) FROM section_response_attempts GROUP BY attempt_type, is_valid").fetchall()
print("Attempts by type and validity:", attempts)

# Check why attempts were invalid
invalid_samples = cur.execute("SELECT section_id, attempt_number, validation_errors FROM section_response_attempts WHERE is_valid = 0 LIMIT 10").fetchall()
print("\n--- Sample validation errors ---")
for s in invalid_samples:
    print(f"Section {s[0]} attempt {s[1]}: {s[2]}")

conn.close()
