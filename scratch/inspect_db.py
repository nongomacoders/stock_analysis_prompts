import sys
import sqlite3

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

conn = sqlite3.connect('documents/analysis.sqlite')
cursor = conn.cursor()

sha = '9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc'
rows = cursor.execute('SELECT section_number, section_id, heading, subheading, length(selected_text), length(llm_response) FROM sections WHERE report_sha256 = ? ORDER BY section_number', (sha,)).fetchall()
print(f"Total captured sections for NTU: {len(rows)}")
for r in rows:
    print(r)

conn.close()
