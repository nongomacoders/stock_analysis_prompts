"""Preserve Gemini/pilot evidence and render original pages read-only."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT));sys.stdout.reconfigure(encoding='utf-8')
BASE=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations'
GEMINI=BASE/'20261028T170032Z_gemini';PILOT=BASE/'20261028T163642Z_section_prompt_paired_pilot'
HERE=Path(__file__).resolve().parent
run=BASE/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_codex_gemini_section_review')
run.mkdir();(run/'inputs').mkdir();(run/'calculations').mkdir();(run/'source_pages').mkdir()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[]
for origin,label in [(GEMINI,'gemini'),(PILOT,'pilot')]:
    for p in origin.rglob('*'):
        if not p.is_file():continue
        dest=run/'inputs'/label/(f'{len(files):04d}_'+p.name);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
        assert digest(p)==digest(dest)
        files.append(dict(original=str(p),saved=str(dest.relative_to(run)),sha256=digest(p)))
plan=json.loads((PILOT/'plan.json').read_text(encoding='utf-8'))
sources=[]
import pypdfium2 as pdfium
from PySide6.QtGui import QImage
for source in plan['documents']:
    path=Path(source['path']);assert digest(path)==source['sha256']
    ticker='NTU' if 'nutun' in path.name.lower() else 'PAN'
    pages=[13,25] if ticker=='NTU' else [38,39,48,49,50]
    doc=pdfium.PdfDocument(str(path))
    for number in pages:
        page=doc[number-1];bitmap=page.render(scale=1.8,rev_byteorder=True)
        fmt=QImage.Format.Format_RGB888 if bitmap.n_channels==3 else QImage.Format.Format_RGBA8888
        image=QImage(bitmap.buffer,bitmap.width,bitmap.height,bitmap.stride,fmt).copy()
        assert image.save(str(run/'source_pages'/f'{ticker}_{number:02d}.png'))
        textpage=page.get_textpage();(run/'source_pages'/f'{ticker}_{number:02d}.txt').write_bytes(textpage.get_text_range().encode('utf-8'))
        textpage.close();bitmap.close();page.close()
    doc.close();sources.append(dict(**source,ticker=ticker,rendered_pages=pages))
c=sqlite3.connect((ROOT/'documents/analysis.sqlite').as_uri()+'?mode=ro',uri=True)
tables={}
for name, in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    rows=c.execute('SELECT * FROM "'+name.replace('"','""')+'"').fetchall()
    tables[name]=hashlib.sha256(repr(sorted(rows,key=repr)).encode('utf-8')).hexdigest()
c.close()
(run/'inputs/manifest.json').write_text(json.dumps(dict(files=files,sources=sources,production_table_hashes=tables),indent=2),encoding='utf-8')
(HERE/'review_run.txt').write_text(str(run),encoding='utf-8')
shutil.copy2(Path(__file__),run/'calculations/prepare.py')
print(json.dumps(dict(run=str(run),preserved_files=len(files),rendered_sources=sources),indent=2))
