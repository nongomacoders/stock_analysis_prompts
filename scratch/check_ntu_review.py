import json, sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
run = Path('scratch/ntu_gemini_review_latest.txt').read_text().strip()
c = sqlite3.connect(Path(run, 'inputs/experiment_snapshot.sqlite').as_uri()+'?mode=ro', uri=True)
for name, sql in c.execute("select name,sql from sqlite_master where type='table'"):
    print(name, sql[:1200])
print('QUESTION EXAMPLE', c.execute('select question_json from ledger_questions limit 1').fetchone())
print('EVENT EXAMPLE', c.execute('select event_json from ledger_events limit 1').fetchone())
metrics=json.loads(Path(run,'inputs/comparison_metrics.json').read_text())
print('METRIC KEYS',list(metrics))
for k,v in metrics.items():
    if k not in ['sections','captures']: print(k,str(v)[:2000])
from collections import Counter
attempts=c.execute('select id,package_id,validation_status,errors_json from section_response_attempts').fetchall()
print('ERRORS',json.dumps(attempts,ensure_ascii=True))
pages=json.loads(Path(run,'source_pages.json').read_text(encoding='utf-8'))
for p in pages:
    if p['physical_page'] in [35,36]: print('PAGE',p)
