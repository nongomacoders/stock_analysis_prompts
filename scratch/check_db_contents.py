import sqlite3
import json
from pathlib import Path

db_path = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/experiment.sqlite")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Check question status inside question_json
rows = cur.execute("SELECT question_id, question_json FROM ledger_questions").fetchall()
status_counts = {}
for qid, qjson in rows:
    data = json.loads(qjson)
    st = data.get("status", "unknown")
    status_counts[st] = status_counts.get(st, 0) + 1
print("Question statuses inside question_json:", status_counts)

# Check validation statuses in section_response_attempts
att_status = cur.execute("SELECT validation_status, count(*) FROM section_response_attempts GROUP BY validation_status").fetchall()
print("Validation status counts in section_response_attempts:", att_status)

# Check sample error messages in section_response_attempts
err_rows = cur.execute("SELECT package_id, validation_status, errors_json FROM section_response_attempts WHERE validation_status != 'valid' LIMIT 10").fetchall()
print("\n--- Sample validation errors ---")
for pid, vst, ej in err_rows:
    print(f"Package: {pid}, Status: {vst}")
    try:
        errs = json.loads(ej)
        print(f"  Errors: {errs[:3]}")
    except Exception:
        print(f"  Raw: {ej[:200]}")

conn.close()
