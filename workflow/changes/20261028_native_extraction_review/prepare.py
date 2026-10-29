"""Read-only review preparation: flat preservation, primary text and renders."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,sys,importlib.util
import pdfplumber,pypdfium2 as pdfium
from PySide6.QtGui import QImage
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT))
BASE=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations'
GEMINI=BASE/'20261028T184306Z_gemini';PILOT=BASE/'20261028T182010Z_native_extraction_pilot'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
spec=importlib.util.spec_from_file_location('transport',ROOT/'workflow/changes/20261028_ntu_default_run/rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
run=BASE/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_codex_native_extraction_review');run.mkdir()
for d in ['inputs','source_pages','calculations']:(run/d).mkdir()
(HERE/'run.txt').write_text(str(run),encoding='utf-8')
paths=list(GEMINI.rglob('*'))+list(PILOT.rglob('*'))
paths += [ROOT/p for p in ['section_capture/pdf_source.py','section_capture/question_ledger.py','prompts/common/12-analyst-reading-brief/v1.1.0/prompt.md','prompts/consumer_lending/12-analyst-reading-brief/v1.1.0/prompt.md']]
manifest=[]
for p in sorted(set(paths)):
    if not p.is_file():continue
    dest=run/'inputs'/f'{len(manifest):04d}{p.suffix}'
    shutil.copy2(p,dest)
    manifest.append(dict(original_path=str(p),preserved_path=str(dest),sha256=sha(p)))
save(run/'inputs/manifest.json',manifest)
checks=[]
for entry in read(GEMINI/'inputs/manifest.json'):
    original=Path(entry['original_path'])
    if not original.is_absolute():original=ROOT/original
    copy=Path(entry['preserved_path'])
    checks.append(dict(path=str(original),original_match=sha(original)==entry['sha256'],copy_match=sha(copy)==entry['sha256']))
save(run/'gemini_input_verification.json',checks)
assert all(c['original_match'] and c['copy_match'] for c in checks)
plan=read(PILOT/'plan.json');sources=[]
for source in plan['documents']:
    path=Path(source['path']);assert sha(path)==source['sha256']
    ticker='NTU' if 'nutun' in path.name else 'PAN';pages=[13,21,22,23,24,25] if ticker=='NTU' else [48,49,50]
    sources.append(dict(path=str(path),sha256=sha(path),pages=pages))
    with pdfplumber.open(path) as pdf:
        for number in pages:(run/'source_pages'/f'{ticker}_{number}.txt').write_text(pdf.pages[number-1].extract_text() or '',encoding='utf-8')
    doc=pdfium.PdfDocument(path)
    try:
        for number in pages:
            page=doc[number-1];bitmap=page.render(scale=1.5,rev_byteorder=True)
            fmt=QImage.Format.Format_RGB888 if bitmap.n_channels==3 else QImage.Format.Format_RGBA8888
            im=QImage(bitmap.buffer,bitmap.width,bitmap.height,bitmap.stride,fmt).copy()
            assert im.save(str(run/'source_pages'/f'{ticker}_{number}.png'))
            bitmap.close();page.close()
    finally:doc.close()
c=m.ro(ROOT/'documents/analysis.sqlite');tables=m.snap(c);c.close()
save(run/'baseline.json',dict(sources=sources,production_table_hashes=tables,pilot_tables_match=tables==plan['production_table_hashes'],preserved_files=len(manifest),gemini_manifest_entries=len(checks)))
print(json.dumps(dict(run=str(run),preserved_files=len(manifest),gemini_manifest_verified=len(checks),source_pages=9,production_matches_pilot=tables==plan['production_table_hashes'])))
