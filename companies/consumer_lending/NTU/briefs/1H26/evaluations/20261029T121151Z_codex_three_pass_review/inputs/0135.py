import sqlite3, hashlib, json

db = sqlite3.connect("documents/analysis.sqlite")
c = db.cursor()
tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
hashes = {t: hashlib.sha256(repr(c.execute(f"SELECT * FROM {t}").fetchall()).encode("utf-8")).hexdigest() for t in sorted(tables)}
print(json.dumps(hashes, indent=2))
