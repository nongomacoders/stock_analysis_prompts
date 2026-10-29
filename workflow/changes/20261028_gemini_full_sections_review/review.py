"""Independent evidence preservation and diagnostics;no application/model changes."""
from datetime import datetime,timezone
import difflib
import hashlib
import json
from pathlib import Path
import re
import shutil
import sqlite3
import sys
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT));sys.stdout.reconfigure(encoding='utf-8')
BASE=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations'
GEMINI=BASE/'20261028T174829Z_gemini';TRIAL=BASE/'20261028T171901Z_ntu_refined_sections'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return re.sub(r'\s+',' ',s).strip()
def offline(event,args):
    if event in {'socket.connect','socket.getaddrinfo','socket.sendto'}:raise RuntimeError('Offline Codex review')
sys.addaudithook(offline)
run=BASE/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_codex_full_sections_review')
run.mkdir();(run/'inputs').mkdir();(run/'calculations').mkdir();(run/'source_pages').mkdir()
manifest=[]
for origin,label in [(GEMINI,'gemini'),(TRIAL,'trial')]:
    for path in origin.rglob('*'):
        if not path.is_file():continue
        dest=run/'inputs'/label/(f'{len(manifest):04d}_'+path.name);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
        assert sha(dest)==sha(path)
        manifest.append(dict(original=str(path),saved=str(dest.relative_to(run)),sha256=sha(path)))
from section_capture import question_ledger
normalizer_source=Path(question_ledger.__file__).read_text(encoding='utf-8')
assert "re.sub(r'\\s+', ' ', text).strip()" in normalizer_source
plan=read(TRIAL/'plan.json');source=plan['documents'][0];assert sha(Path(source['path']))==source['sha256']
cases=[]
for rejected in read(TRIAL/'outputs/rejected_ledger_deltas.json'):
    label=rejected['label'];before=read(TRIAL/'inputs'/f'{label}_ledger_before.json')
    request=read(TRIAL/'requests'/f'{label}.json')['messages'][0]['content']
    after=read(TRIAL/'outputs'/f'{label}_ledger_after.json');assert before==after
    # Current selected evidence,not normalized PDF prose or an altered verifier.
    c=sqlite3.connect((TRIAL/'experiment.sqlite').as_uri()+'?mode=ro',uri=True)
    raw=next(r[0] for r in c.execute('SELECT manifest_json FROM sections ORDER BY section_number') if
        [s['physical_page'] for s in json.loads(r[0])['selections']]==rejected['pages'])
    c.close();capture=json.loads(raw)
    quotes=[]
    for update in rejected['unapplied_delta']['updates']:
        for ev in update['evidence']:
            texts=[s['text'] for s in capture['selections'] if s['physical_page']==ev['physical_page']]
            quote=ev['quote'];full=norm('\n'.join(texts));q=norm(quote)
            literal=q in full
            candidate=difflib.get_close_matches(q,[norm(line) for text in texts for line in text.splitlines()],n=1,cutoff=.1)
            # Diagnostic only;never apply pipe stripping to accepted production evidence.
            stripped=norm(quote.replace('|',' '))
            strip_match=any(stripped in norm(text.replace('|',' ')) for text in texts)
            quotes.append(dict(question_id=update['question_id'],page=ev['physical_page'],quote=quote,
                literal_after_existing_whitespace_normalization=literal,match_after_diagnostic_pipe_removal=strip_match,
                nearest_line=candidate[0] if candidate else None))
    resolutions=[]
    for update in rejected['unapplied_delta']['updates']:
        if update['status']=='resolved':
            original=next(q for q in before if q['question_id']==update['question_id'])
            resolutions.append(dict(original=original,proposed=update))
    cases.append(dict(label=label,pages=rejected['pages'],quotes=quotes,proposed_resolutions=resolutions))
save(run/'calculations/quote_diagnostics.json',cases)
selected={'Q-08aa5c3f257440ab','Q-e4497d9112cd4e9d','Q-d22e0c2b395a427e','Q-f6689319fb3a49ff','Q-86df863491ca4eae','Q-4de5fe06ec4d4f67','Q-8612694a3a674266'}
questions=[q for q in read(TRIAL/'outputs/final_ledger.json') if q['question_id'] in selected]
save(run/'calculations/question_scope_comparison.json',questions)
import pypdfium2 as pdfium
from PySide6.QtGui import QImage
doc=pdfium.PdfDocument(source['path'])
for number in [12,13,22,24,25,31]:
    page=doc[number-1];b=page.render(scale=1.8,rev_byteorder=True)
    fmt=QImage.Format.Format_RGB888 if b.n_channels==3 else QImage.Format.Format_RGBA8888
    image=QImage(b.buffer,b.width,b.height,b.stride,fmt).copy()
    assert image.save(str(run/'source_pages'/f'NTU_{number}.png'))
    text=page.get_textpage();(run/'source_pages'/f'NTU_{number}.txt').write_bytes(text.get_text_range().encode('utf-8'));text.close()
    b.close();page.close()
doc.close()
c=sqlite3.connect((ROOT/'documents/analysis.sqlite').as_uri()+'?mode=ro',uri=True);tables={}
for name, in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    rows=c.execute('SELECT * FROM "'+name.replace('"','""')+'"').fetchall();tables[name]=hashlib.sha256(repr(sorted(rows,key=repr)).encode()).hexdigest()
c.close()
save(run/'inputs/manifest.json',dict(files=manifest,source=source,production_table_hashes=tables))
(HERE/'review_run.txt').write_text(str(run),encoding='utf-8')
shutil.copy2(Path(__file__),run/'calculations/prepare_diagnostics.py')
print(json.dumps(dict(run=str(run),quote_cases=[dict(label=c['label'],failed=[dict(qid=q['question_id'],quote=q['quote'],pipe_removal_match=q['match_after_diagnostic_pipe_removal'],nearest_line=q['nearest_line']) for q in c['quotes'] if not q['literal_after_existing_whitespace_normalization']],resolutions=c['proposed_resolutions']) for c in cases],question_scope=questions),indent=2)[:17000])
