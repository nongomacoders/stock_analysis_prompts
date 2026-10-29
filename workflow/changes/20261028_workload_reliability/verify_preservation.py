"""Read-only logical comparison when SQLite file headers/sequences have changed."""
import hashlib
import json
from pathlib import Path
import sqlite3

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
plan=json.loads((HERE/'comparison_plan.json').read_text(encoding='utf-8'))
baseline=Path(plan['companies'][0]['run'])/'inputs/production_snapshot.sqlite'

def snapshot(path):
    conn=sqlite3.connect(path.resolve().as_uri()+'?mode=ro',uri=True)
    try:
        names=[r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        tables={}
        for name in names:
            rows=conn.execute('SELECT * FROM "'+name.replace('"','""')+'"').fetchall()
            tables[name]=dict(count=len(rows),sha256=hashlib.sha256(json.dumps(sorted(rows,key=repr),ensure_ascii=False,default=repr).encode()).hexdigest())
        sequences=conn.execute('SELECT * FROM sqlite_sequence').fetchall()
        return tables,sequences
    finally:
        conn.close()

old,old_seq=snapshot(baseline)
new,new_seq=snapshot(ROOT/'documents/analysis.sqlite')
changed=[name for name in set(old)|set(new) if old.get(name)!=new.get(name)]
result=dict(changed_tables=sorted(changed),baseline_sequences=old_seq,current_sequences=new_seq,
            reports_unchanged=old['reports']==new['reports'],sections_unchanged=old['sections']==new['sections'],
            guardrails_unchanged=old['sector_guardrails']==new['sector_guardrails'],baseline_tables=old,current_tables=new)
(HERE/'production_preservation_check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in {'baseline_tables','current_tables'}},indent=2))
