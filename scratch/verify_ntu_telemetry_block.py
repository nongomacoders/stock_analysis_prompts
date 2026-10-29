import sys, json, hashlib, sqlite3, shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta
sys.stdout.reconfigure(encoding='utf-8')
root=Path.cwd()
run=Path(Path('scratch/ntu_comparison_latest.txt').read_text(encoding='utf-8').strip())
calc=run/'calculations'
calc.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
m=json.loads((run/'inputs/manifest.json').read_text(encoding='utf-8'))
files=[{**f,'original_matches':sha(f['original'])==f['sha256'],'saved_matches':sha(run/f['saved'])==f['sha256']} for f in m['files']]
source=Path(m['sources'][0]['path'])
pdfsha=sha(source)
conn=sqlite3.connect('file:documents/analysis.sqlite?mode=ro',uri=True)
conn.row_factory=sqlite3.Row
old=sqlite3.connect(run/'inputs/analysis_snapshot.sqlite')
old.row_factory=sqlite3.Row
report=dict(conn.execute('SELECT * FROM reports WHERE sha256=?',(pdfsha,)).fetchone())
previous=dict(old.execute('SELECT * FROM reports WHERE sha256=?',(pdfsha,)).fetchone())
rules=[dict(x) for x in conn.execute('SELECT * FROM sector_guardrails ORDER BY rule_code')]
oldrules=json.loads((run/'inputs/guardrails.json').read_text(encoding='utf-8'))
conn.close();old.close()
prompt=run/'outputs/NTU_1H26_stage1_forensic_prompt.md'
verify={'checked_utc':datetime.now(timezone.utc).isoformat(),'files':files,'source_sha256':pdfsha,'source_baseline_matches':pdfsha==m['sources'][0]['sha256'],'source_sqlite_matches':report['sha256']==pdfsha,'report_row_unchanged':report==previous,'guardrails_unchanged':rules==oldrules,'prompt_characters':len(prompt.read_text(encoding='utf-8')),'prompt_same_as_first_attempt':sha(prompt)==sha(run.parent/'20261027T171921Z_codex_max_comparison/outputs/NTU_1H26_stage1_forensic_prompt.md'),'output_files':[p.name for p in (run/'outputs').iterdir()],'runner_exit_code':None,'observed_status':json.loads((run/'status.json').read_text(encoding='utf-8'))}
assert all(f['original_matches'] and f['saved_matches'] for f in files)
assert verify['source_baseline_matches'] and verify['source_sqlite_matches'] and verify['report_row_unchanged'] and verify['guardrails_unchanged']
(run/'independent_verification.json').write_text(json.dumps(verify,indent=2),encoding='utf-8')
shutil.copy2('scratch/run_ntu_openrouter_only.py',run/'network_guard_runner.py')
shutil.copy2('scratch/run_ntu_max_comparison.py',run/'run_comparison.py')
shutil.copy2('scratch/inspect_ntu_comparison_sources.py',calc/'extract_source.py')
print('Main run:',run.name)
print('Preservation: all',len(files),'originals/copies match; PDF/report/guardrails unchanged')
print('Fresh answers: absent; final runner exit code unavailable')
