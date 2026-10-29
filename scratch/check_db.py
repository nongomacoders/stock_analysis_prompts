import sqlite3
from pathlib import Path

db_path = Path("companies/retail/DCP/briefs/FY26/evaluations/20261028T081850Z_codex_workload_comparison/experiment.sqlite")
print(f"DB exists: {db_path.exists()}, size: {db_path.stat().st_size}")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Tables:", [t[0] for t in tables])

for table in [t[0] for t in tables]:
    cnt = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"Table {table}: {cnt} rows")

# Let's inspect questions table if present
if ("questions",) in tables:
    cols = [d[0] for d in cur.execute("PRAGMA table_info(questions)").fetchall()]
    print("Questions columns:", cols)
    # Check statuses
    statuses = cur.execute("SELECT status, count(*) FROM questions GROUP BY status").fetchall()
    print("Questions by status:", statuses)

conn.close()
