from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,sys,importlib.util
import pdfplumber,pypdfium2 as pdfium
from PySide6.QtGui import QImage
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT))
BASE=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations'
G=BASE/'20261029T114800Z_antigravity_gemini_stage_review';O=BASE/'20261029T112944Z_three_pass_experiment';R=BASE/'20261029T114212Z_three_pass_pan_resume'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
spec=importlib.util.spec_from_file_location('transport',ROOT/'workflow/changes/20261028_ntu_default_run/rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
run=BASE/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_codex_three_pass_review');run.mkdir()
for d in ['inputs','source_pages','calculations']:(run/d).mkdir()
(HERE/'run.txt').write_text(str(run),encoding='utf-8')
paths=[p for directory in [G,O,R] for p in directory.rglob('*') if p.is_file()]
manifest=[]
for p in sorted(set(paths)):
    dest=run/'inputs'/f'{len(manifest):04d}{p.suffix}';shutil.copy2(p,dest);manifest.append(dict(original_path=str(p),preserved_path=str(dest),sha256=sha(p)))
save(run/'inputs/manifest.json',manifest)
checks=[]
for entry in read(G/'input_manifest.json')['files']:
    path=Path(entry['path']);path=path if path.is_absolute() else ROOT/path
    checks.append(dict(path=str(path),match=sha(path)==entry['sha256']))
assert all(e['match'] for e in checks);save(run/'gemini_manifest_checks.json',checks)
plan=read(R/'plan.json');sources=[]
for source in plan['documents']:
    path=Path(source['path']);assert sha(path)==source['sha256']
    ticker='NTU' if 'nutun' in path.name else 'PAN';pages=[13,21,22,23] if ticker=='NTU' else [48,49,50]
    sources.append(dict(path=str(path),sha256=sha(path),pages=pages))
    with pdfplumber.open(path) as pdf:
        for n in pages:(run/'source_pages'/f'{ticker}_{n}.txt').write_text(pdf.pages[n-1].extract_text() or '',encoding='utf-8')
    doc=pdfium.PdfDocument(path)
    try:
        for n in pages:
            page=doc[n-1];bitmap=page.render(scale=1.5,rev_byteorder=True)
            fmt=QImage.Format.Format_RGB888 if bitmap.n_channels==3 else QImage.Format.Format_RGBA8888
            im=QImage(bitmap.buffer,bitmap.width,bitmap.height,bitmap.stride,fmt).copy();assert im.save(str(run/'source_pages'/f'{ticker}_{n}.png'))
            bitmap.close();page.close()
    finally:doc.close()
c=m.ro(ROOT/'documents/analysis.sqlite');tables=m.snap(c);c.close()
save(run/'baseline.json',dict(sources=sources,production_table_hashes=tables,pilot_tables_match=tables==plan['production_table_hashes']))
print(json.dumps(dict(run=str(run),preserved_files=len(manifest),gemini_manifest_entries=len(checks),source_pages=7,production_matches_pilot=tables==plan['production_table_hashes'])))
