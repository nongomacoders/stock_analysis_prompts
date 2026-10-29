"""Preserve NTU review inputs and extract source evidence; no model calls or DB writes."""
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import sys
from datetime import datetime, timezone, timedelta

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.stdout.reconfigure(encoding='utf-8')
BASE=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations'
GEMINI=BASE/'20261028T092500Z_gemini'
SUBJECT=BASE/'20261028T081850Z_codex_workload_comparison'
RUN=BASE/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_codex_review')
RUN.mkdir(exist_ok=False)
(RUN/'inputs').mkdir()
(RUN/'calculations').mkdir()
(RUN/'renders').mkdir()

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path,obj): path.write_bytes((json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))

manifest=dict(created_utc=datetime.now(timezone.utc).isoformat(),local_time=datetime.now(timezone(timedelta(hours=2))).isoformat(),
              ticker='NTU',period='1H26',evaluator='Codex',runtime_model='Not independently exposed',files=[],sources=[])
shutil.copytree(GEMINI,RUN/'inputs/gemini')
for original in GEMINI.rglob('*'):
    if original.is_file():
        manifest['files'].append(dict(original=str(original),saved=str((RUN/'inputs/gemini'/original.relative_to(GEMINI)).relative_to(RUN)),sha256=sha(original)))
for folder in ['outputs','requests']:
    shutil.copytree(SUBJECT/folder,RUN/'inputs/subject'/folder)
    for original in (SUBJECT/folder).glob('*'):
        if original.is_file():
            manifest['files'].append(dict(original=str(original),saved=str((RUN/'inputs/subject'/folder/original.name).relative_to(RUN)),sha256=sha(original)))
for name in ['comparison_metrics.json','status.json']:
    original=SUBJECT/name
    shutil.copy2(original,RUN/'inputs'/name)
    manifest['files'].append(dict(original=str(original),saved='inputs/'+name,sha256=sha(original)))
conn=sqlite3.connect((SUBJECT/'experiment.sqlite').resolve().as_uri()+'?mode=ro',uri=True)
snapshot=sqlite3.connect(RUN/'inputs/experiment_snapshot.sqlite')
try:
    conn.backup(snapshot)
finally:
    snapshot.close();conn.close()
source=ROOT/'companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf'
digest=sha(source)
conn=sqlite3.connect((ROOT/'documents/analysis.sqlite').resolve().as_uri()+'?mode=ro',uri=True)
conn.row_factory=sqlite3.Row
try:
    report=dict(conn.execute('SELECT * FROM reports WHERE sha256=?',(digest,)).fetchone())
    rules=[dict(r) for r in conn.execute('SELECT * FROM sector_guardrails ORDER BY rule_code')]
finally: conn.close()
save(RUN/'inputs/production_report_and_guardrails.json',dict(report=report,guardrails=rules))
assert digest=='9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc'
manifest['sources'].append(dict(path=str(source),sha256=digest,sqlite_match=True))
gemini_manifest=json.loads((GEMINI/'inputs/manifest.json').read_text(encoding='utf-8'))
checks=[]
for item in gemini_manifest['preserved_trial_outputs']:
    original=SUBJECT/item['original_rel_path']
    copied=GEMINI/item['saved_path'].replace('\\','/')
    checks.append(dict(path=item['original_rel_path'],declared_hash=item['sha256'],
                       original_match=sha(original)==item['sha256'],gemini_copy_match=sha(copied)==item['sha256']))
assert all(c['original_match'] and c['gemini_copy_match'] for c in checks)
save(RUN/'inputs/gemini_input_verification.json',checks)

import pypdfium2 as pdfium
from PySide6.QtGui import QImage
document=pdfium.PdfDocument(str(source))
pages=[]
render_pages={3,8,9,12,13,14,15,16,17,18,21,22,24,25,28,31,36}
try:
    for index in range(len(document)):
        page=document[index]
        textpage=page.get_textpage()
        try:
            pages.append(dict(physical_page=index+1,text=textpage.get_text_range()))
            if index+1 in render_pages:
                bitmap=page.render(scale=1.5,rev_byteorder=True)
                try:
                    fmt=QImage.Format.Format_RGB888 if bitmap.n_channels==3 else QImage.Format.Format_RGBA8888
                    image=QImage(bitmap.buffer,bitmap.width,bitmap.height,bitmap.stride,fmt).copy()
                    assert image.save(str(RUN/'renders'/f'p{index+1:02d}.png'))
                finally: bitmap.close()
        finally:
            textpage.close();page.close()
finally: document.close()
save(RUN/'source_pages.json',pages)
save(RUN/'inputs/manifest.json',manifest)
shutil.copy2(Path(__file__),RUN/'calculations/prepare_review.py')
(ROOT/'scratch/ntu_gemini_review_latest.txt').write_text(str(RUN),encoding='utf-8')
print(json.dumps(dict(run=str(RUN),preserved_files=len(manifest['files']),source_hash_verified=True,gemini_input_hash_checks=len(checks),rendered_pages=sorted(render_pages))))
