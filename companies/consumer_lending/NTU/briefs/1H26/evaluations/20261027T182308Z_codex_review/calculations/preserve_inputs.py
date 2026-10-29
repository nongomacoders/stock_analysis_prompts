from pathlib import Path
from datetime import datetime, timezone, timedelta
import hashlib,json,shutil,sqlite3,sys
sys.stdout.reconfigure(encoding='utf-8')
root=Path.cwd()
subject=root/'companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T175621Z_codex_max_comparison'
review=Path((root/'scratch/ntu_latest_codex_review.txt').read_text(encoding='utf-8').strip())
(review/'inputs').mkdir(parents=True,exist_ok=True)
(review/'calculations').mkdir(exist_ok=True)
(root/'scratch/ntu_latest_codex_review.txt').write_text(str(review),encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
manifest={'created_utc':datetime.now(timezone.utc).isoformat(),'local_time':datetime.now(timezone(timedelta(hours=2))).isoformat(),'subject':str(subject),'files':[],'evaluator':'Codex; exact runtime model/settings not independently exposed'}
for folder in ['outputs','calculations']:
 for p in (subject/folder).rglob('*'):
  if p.is_file():
   dest=review/'inputs/fresh_run'/p.relative_to(subject)
   dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
   manifest['files'].append({'original':str(p),'saved':str(dest.relative_to(review)),'sha256':sha(p)})
for name in ['audit.md','status.json','independent_verification.json','run_comparison.py','inputs/manifest.json','inputs/sections_and_ledger.json','inputs/guardrails.json','inputs/analysis_snapshot.sqlite']:
 p=subject/name
 if p.exists():
  dest=review/'inputs/fresh_run'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
  manifest['files'].append({'original':str(p),'saved':str(dest.relative_to(review)),'sha256':sha(p)})
base=json.loads((subject/'inputs/manifest.json').read_text(encoding='utf-8'))
original_checks=[]
for f in base['files']:
 p=Path(f['original']); saved=subject/f['saved']
 original_checks.append({'original':str(p),'expected':f['sha256'],'original_matches':sha(p)==f['sha256'],'prior_saved_matches':sha(saved)==f['sha256']})
 dest=review/'inputs/baseline'/Path(f['saved']).relative_to('inputs')
 dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(saved,dest)
 manifest['files'].append({'original':str(saved),'saved':str(dest.relative_to(review)),'sha256':sha(saved)})
pdf=Path(base['sources'][0]['path']);pdfsha=sha(pdf)
assert pdfsha=='9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc'
live=sqlite3.connect('file:documents/analysis.sqlite?mode=ro',uri=True);live.row_factory=sqlite3.Row
snap=sqlite3.connect(subject/'inputs/analysis_snapshot.sqlite');snap.row_factory=sqlite3.Row
report=dict(live.execute('SELECT * FROM reports WHERE sha256=?',(pdfsha,)).fetchone())
oldreport=dict(snap.execute('SELECT * FROM reports WHERE sha256=?',(pdfsha,)).fetchone())
rules=[dict(x) for x in live.execute('SELECT * FROM sector_guardrails ORDER BY rule_code')]
oldrules=json.loads((subject/'inputs/guardrails.json').read_text(encoding='utf-8'))
live.close();snap.close()
verification={'original_baseline_files':original_checks,'pdf_path':str(pdf),'pdf_sha256':pdfsha,'sqlite_match':report['sha256']==pdfsha,'production_report_equal_pre_run':report==oldreport,'guardrails_equal_pre_run':rules==oldrules,'production_target':report.get('target_price_zar'),'production_recommendation':report.get('recommendation'),'rules_count':len(rules),'prompt_checks':{}}
for stage in [1,2]:
 fn=f'NTU_1H26_stage{stage}_'+('forensic_prompt.md' if stage==1 else 'valuation_prompt.md')
 stats=json.loads((subject/f'outputs/NTU_1H26_stage{stage}_response.run.json').read_text(encoding='utf-8'))
 txt=(subject/'outputs'/fn).read_text(encoding='utf-8')
 verification['prompt_checks'][str(stage)]={'normalized_text_matches_request_hash':hashlib.sha256(txt.encode()).hexdigest()==stats['prompt_sha256'],'windows_write_translation_reversed_matches_request_hash':hashlib.sha256((subject/'outputs'/fn).read_bytes().decode('utf-8').replace('\r\n','\n').encode()).hexdigest()==stats['prompt_sha256'],'response_sha256':sha(subject/f'outputs/NTU_1H26_stage{stage}_response.md'),'finish_reason':stats['finish_reason']}
assert all(x['original_matches'] and x['prior_saved_matches'] for x in original_checks)
assert verification['production_report_equal_pre_run'] and verification['guardrails_equal_pre_run']
assert all(x['windows_write_translation_reversed_matches_request_hash'] for x in verification['prompt_checks'].values())
(review/'inputs/manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(review/'independent_verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
print('Review:',review)
print('Preserved review files:',len(manifest['files']))
print('Baseline originals checked:',len(original_checks))
print('PDF/SQLite/prompts/production/guardrails checks passed; production',verification['production_target'],verification['production_recommendation'])
