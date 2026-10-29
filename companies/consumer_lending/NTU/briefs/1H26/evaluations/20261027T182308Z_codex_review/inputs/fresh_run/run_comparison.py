import sys, json, hashlib, shutil, sqlite3, time, traceback
from pathlib import Path
from datetime import datetime, timezone, timedelta
sys.path.insert(0, str(Path.cwd()))
sys.stdout.reconfigure(encoding='utf-8')
from workflow.export_stage1 import build_stage1_prompt_content
from workflow.generate_stage2 import build_stage2_prompt_content
from section_capture.openrouter import query_openrouter, get_openrouter_model, fetch_generation_stats, STAGE_ANALYSIS_OPTIONS
import pypdfium2 as pdfium
ROOT = Path.cwd()
BRIEFS = ROOT / 'companies/consumer_lending/NTU/briefs/1H26'
RUN = BRIEFS / 'evaluations' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_codex_max_comparison')
RUN.mkdir()
(RUN/'inputs').mkdir()
(RUN/'outputs').mkdir()
(ROOT/'scratch/ntu_comparison_latest.txt').write_text(str(RUN), encoding='utf-8')
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, value): p.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')
manifest = {'created_utc': datetime.now(timezone.utc).isoformat(), 'local_time': datetime.now(timezone(timedelta(hours=2))).isoformat(), 'ticker':'NTU', 'period':'1H26', 'design':'Fresh Stage 1 and Stage 2, existing section captures/ledger, current guardrails. No evaluator findings injected. Combined intervention, not reasoning-only experiment.', 'files':[], 'sources':[], 'requested_options':STAGE_ANALYSIS_OPTIONS, 'reference_price_zar':0.89, 'reference_basis':'Frozen prior-note reference; not a current quote.'}
for p in BRIEFS.glob('*.md'):
    dest = RUN/'inputs'/p.name
    shutil.copy2(p, dest)
    manifest['files'].append({'original':str(p), 'saved':str(dest.relative_to(RUN)), 'sha256':digest(p)})
for name in ['20261027T163950Z_gemini', '20261027T164527Z_codex']:
    source = BRIEFS/'evaluations'/name
    target = RUN/'inputs'/name
    shutil.copytree(source, target)
    for p in source.rglob('*'):
        if p.is_file(): manifest['files'].append({'original':str(p), 'saved':str((target/p.relative_to(source)).relative_to(RUN)), 'sha256':digest(p)})
snapshot = RUN/'inputs/analysis_snapshot.sqlite'
source_conn = sqlite3.connect('file:documents/analysis.sqlite?mode=ro', uri=True)
backup_conn = sqlite3.connect(snapshot)
source_conn.backup(backup_conn)
backup_conn.close()
source_conn.close()
conn = sqlite3.connect(snapshot)
conn.row_factory = sqlite3.Row
pdfs = sorted((ROOT/'companies/consumer_lending/NTU/sources').rglob('*.pdf'))
assert len(pdfs)==1, 'Unexpected NTU PDF inventory; inspect before running'
pdf = pdfs[0]
sha = digest(pdf)
report = conn.execute('SELECT * FROM reports WHERE sha256=?', (sha,)).fetchone()
assert report is not None, 'PDF SHA256 does not match database'
assert sha=='9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc'
sections = conn.execute('SELECT * FROM sections WHERE report_sha256=? ORDER BY section_number,id', (sha,)).fetchall()
assert sections, 'No captured sections'
linked = conn.execute('SELECT filename FROM reports WHERE parent_report_sha256=?', (sha,)).fetchall()
assert not linked, 'Unexpected companion documents; inspect'
save(RUN/'inputs/sections_and_ledger.json', {'sections':[dict(s) for s in sections], 'report':dict(report)})
save(RUN/'inputs/guardrails.json', [dict(r) for r in conn.execute('SELECT * FROM sector_guardrails ORDER BY rule_code')])
conn.close()
manifest['sources'].append({'path':str(pdf), 'sha256':sha, 'sqlite_match':True, 'physical_pages':report['physical_page_count']})
save(RUN/'inputs/manifest.json', manifest)
prompt = build_stage1_prompt_content(sections=sections, company_title='Nutun Limited', ticker='NTU', detected_sector='consumer_lending', filename=pdf.name, final_questions_ledger=report['questions_ledger'], compact=True, db_path=snapshot)
(RUN/'outputs/NTU_1H26_stage1_forensic_prompt.md').write_text(prompt, encoding='utf-8')
model = get_openrouter_model()
status = {'status':'prepared', 'model':model, 'run':str(RUN)}
save(RUN/'status.json', status)
print('Run directory:', RUN, flush=True)
print('PDF hash verified. Captured sections:', len(sections), 'Stage 1 prompt characters:', len(prompt), flush=True)
def execute(stage, text):
    status.update(status='running', stage=stage)
    save(RUN/'status.json', status)
    start=time.monotonic()
    print('Submitting',stage,'model',model,'with max reasoning',flush=True)
    response, stats=query_openrouter(prompt=text, model=model, return_details=True, **STAGE_ANALYSIS_OPTIONS)
    stats.update(elapsed_seconds=round(time.monotonic()-start,2), prompt_sha256=hashlib.sha256(text.encode()).hexdigest(), experimental=True)
    dest=RUN/'outputs'/f'NTU_1H26_{stage}_response.md'
    dest.write_text(response,encoding='utf-8')
    save(dest.with_suffix('.run.json'),stats)
    extra=fetch_generation_stats(stats.get('generation_id',''))
    if extra:
        allowed={k:extra.get(k) for k in ['id','model','provider_name','total_cost','tokens_prompt','tokens_completion','native_tokens_reasoning','finish_reason','generation_time','latency'] if k in extra}
        save(RUN/'outputs'/f'{stage}_generation_stats.json',allowed)
    print(stage,'saved:', len(response),'characters. Usage:',stats['total_tokens'],'Reasoning:',stats.get('reasoning_tokens'),flush=True)
    return response
try:
    stage1 = execute('stage1',prompt)
    doc=pdfium.PdfDocument(str(pdf))
    pages=[]
    for i in range(len(doc)):
        page=doc[i]
        tp=page.get_textpage()
        pages.append(f'--- [{pdf.name} | Page {i+1} of {len(doc)}] ---\n'+tp.get_text_range())
        tp.close(); page.close()
    doc.close()
    source_text='\n\n'.join(pages)
    (RUN/'inputs/source_pages.txt').write_text(source_text,encoding='utf-8')
    base=build_stage2_prompt_content(stage1_content=stage1,company_title='Nutun Limited',ticker='NTU',detected_sector='consumer_lending',reference_price_zar=0.89,source_documents=[{'filename':pdf.name,'doc_type':report['doc_type'],'period':'1H26','page_count':len(pages)}],db_path=snapshot)
    full=base+'\n\n---\n\n# COMPLETE PRIMARY SOURCE FINANCIAL REPORT DISCLOSURES & AUDITED NOTES\n**Source Documents:** '+pdf.name+'\n\n'+source_text
    (RUN/'outputs/NTU_1H26_stage2_valuation_prompt.md').write_text(full,encoding='utf-8')
    execute('stage2',full)
    status.update(status='completed',stage='stage2',completed_utc=datetime.now(timezone.utc).isoformat())
except Exception as exc:
    status.update(status='failed',error_type=type(exc).__name__,error=str(exc))
    print('RUN FAILED:', type(exc).__name__, str(exc), flush=True)
finally:
    status['baseline_files_unchanged']=all(digest(Path(f['original']))==f['sha256'] for f in manifest['files'])
    status['source_unchanged']=digest(pdf)==sha
    save(RUN/'status.json',status)
    shutil.copy2(ROOT/'scratch/run_ntu_max_comparison.py',RUN/'run_comparison.py')
if status['status']=='failed': sys.exit(1)