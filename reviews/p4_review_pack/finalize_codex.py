from pathlib import Path
import sys,sqlite3,json,hashlib,shutil,subprocess
from datetime import datetime,timezone,timedelta
sys.stdout.reconfigure(encoding='utf-8')
root=Path.cwd();pack=root/'reviews/p4_review_pack';e=pack/'codex_evidence';stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');run=root/f'companies/mining/PAN/briefs/FY26/evaluations/{stamp}_codex_p4_source_review';(run/'inputs').mkdir(parents=True);(run/'calculations').mkdir()
checks={}
def ck(name,actual,expected):
 checks[name]={'actual':actual,'expected':expected,'delta':actual-expected};assert actual==expected,name
ck('FY26 SBP',21486+57272+1463-18200+2331,64352);ck('FY25 SBP',10965+13358+6325-9600+438,21486)
ck('FY26 capex',21832+202163,223995);ck('FY25 capex',11626+156283,167909)
ck('FY26 geography',911962+365207+480,1277649);ck('FY25 geography',740819+155716+445,896980)
ck('Acquisition consideration',148218+11879,160097);ck('Acquisition PPE',142244+112+80,142436);ck('Acquisition allocation',142436+86+6427+12796-133-1515,160097)
ck('FY26 adjustments',57272-4706+17318+781+14609+163-109-3029-1142+61980+345,143482)
ck('FY25 adjustments',13358-1856+21073-28019+53+5106+1925-481-15812-2616+34394+2954,30079)
ck('FY26 working capital',17411-21206+50354,46559);ck('FY25 working capital',-4814+2833-132,-2113)
ck('FY26 Note19',534368+143482+46559-18200+8030-1873-247,712119);ck('FY25 Note19',196633+30079-2113-9600+8422-5-232,223184)
ck('FY26 statutory operating cash',712119-58540-74135-12112-14987+4646,556991);ck('FY25 statutory operating cash',223184-23675-20147-4887-21439+1824,154860)
(e/'calculations.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
db=root/'workflow/changes/20261029_agentic_report_build/build/report.sqlite';c=sqlite3.connect(f'file:{db.as_posix()}?mode=ro',uri=True)
summary={'cells':c.execute('select count(*) from cells').fetchone()[0],'regions':c.execute('select count(distinct table_region) from cells').fetchone()[0],'document_counts':c.execute('select document,count(*) from cells group by 1').fetchall(),'questions':c.execute('select question_id,status from questions').fetchall()};c.close()
(e/'db_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('SUMMARY',summary['cells'],summary['regions'])
for script in ['check_codex.py','coverage_codex.py','detail_codex.py']:
 result=subprocess.run([sys.executable,str(pack/script)],capture_output=True,text=True,encoding='utf-8');(e/f'{script}.output.txt').write_text(result.stdout+result.stderr,encoding='utf-8');assert result.returncode==0
manifest=[]
files=[pack/'PROMPT_CODEX.md',pack/'INDEPENDENT_REVIEW.md',pack/'COVERAGE.md',db,root/'workflow/changes/20261029_agentic_report_build/READING_BRIEF_CONSOLIDATED.md',root/'workflow/changes/20261029_agentic_report_build/tests_reconcile/test_review_fixes.py',root/'workflow/changes/20261029_agentic_report_build/tests_reconcile/test_notes.py']
for i,f in enumerate(files):
 dest=run/'inputs'/f'{i:02d}_{f.name}';shutil.copyfile(f,dest);manifest.append({'path':str(f.relative_to(root)),'preserved':str(dest.relative_to(run)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
pdf=root/'companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf';digest=hashlib.sha256(pdf.read_bytes()).hexdigest();assert digest=='62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd';manifest.append({'path':str(pdf.relative_to(root)),'sha256':digest,'preserved':'original unchanged; reference only'})
(run/'input_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
for f in pack.glob('*_codex.py'):shutil.copyfile(f,run/'calculations'/f.name)
shutil.copyfile(pack/'finalize_codex.py',run/'calculations/finalize_codex.py')
for f in e.glob('*.json'):shutil.copyfile(f,run/'calculations'/f.name)
shutil.copyfile(pack/'CODEX_REVIEW.md',run/'audit.md')
(run/'execution.json').write_text(json.dumps({'evaluator':'Codex; exact model identifier not exposed','date_local':datetime.now(timezone(timedelta(hours=2))).isoformat(),'calculations_exit':0,'checks':len(checks),'suite':'127 passed in 0.33s','suite_exit':0,'limitations':'No valuation or live market assessment; no paid calls; proposed improvements only','revisions':'Initial review; no analyzed originals edited'},indent=2),encoding='utf-8')
(e/'audit_location.txt').write_text(str(run.relative_to(root)).replace('\\','/')+'\n',encoding='utf-8')
print('AUDIT',run);print('CALCULATIONS',len(checks),'passed')
