"""Offline checks before the paid pilot; no API or production writes."""
import importlib.util
from pathlib import Path
import sqlite3
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('trial',HERE/'trial.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
m=t.m;run=Path(t.POINTER.read_text(encoding='utf-8').strip())
c=m.ro(run/'experiment.sqlite');p=m.ro(run/'pilot/experiment.sqlite')
assert m.snap(c)==m.snap(p),'Pilot must begin from the same fresh ledger as the full run'
rows=c.execute('SELECT manifest_json,llm_response FROM sections ORDER BY section_number').fetchall()
manifests=[m.json.loads(r[0]) for r in rows]
assert len(rows)==24 and all(not r[1] for r in rows)
assert sum(x['analysis_role']=='navigation_only' for x in manifests)==2
assert [s['physical_page'] for x in manifests for s in x['selections']]==list(range(1,39))
assert all(len(x['selections'])<=3 for x in manifests)
assert set(m.request_payload('offline check',None))=={'model','messages','temperature','stream'}
assert c.execute('SELECT count(*) FROM ledger_questions').fetchone()[0]==10
c.close();p.close();m.preserve(run)
m.save(run/'inputs/plan_checks.json',dict(passed=True,checks=['38 pages once','24 units/22 analytical/2 navigation','max3 pages',
 'fresh10-question ledger','pilot and full databases initially identical','token/reasoning/routing overrides absent','production and original hashes unchanged'],paid_calls=0))
print('Seven plan/transport/preservation checks passed; no model calls.')
