"""Preserve pre-change templates and inspect candidate evidence without production writes."""
from pathlib import Path
import hashlib
import json
import sqlite3
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
originals=[]
for p in sorted((ROOT/'prompts').glob('*/12-analyst-reading-brief/v1.1.0/prompt.md')):
    if p.relative_to(ROOT).parts[1]=='common':continue
    dest=HERE/'before'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():dest.write_bytes(p.read_bytes())
    originals.append(dict(path=str(p.relative_to(ROOT)),sha256=digest(dest)))
for name in ['packages.py','question_ledger.py']:
    p=ROOT/'section_capture'/name;dest=HERE/'before'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():dest.write_bytes(p.read_bytes())
(HERE/'before_manifest.json').write_text(json.dumps(originals,indent=2),encoding='utf-8')
c=sqlite3.connect((ROOT/'documents/analysis.sqlite').as_uri()+'?mode=ro',uri=True)
c.row_factory=sqlite3.Row
rows=c.execute('SELECT package_id,heading,manifest_json,length(selected_text) AS chars FROM sections WHERE manifest_json LIKE ? ORDER BY section_number',('%PAN%',)).fetchall()
out=[]
for r in rows:
    d=dict(r);manifest=json.loads(d.pop('manifest_json'))
    if '/pan/' not in manifest.get('source',{}).get('original_path','').replace('\\','/').lower():continue
    d['pages']=[s.get('physical_page') for s in manifest.get('selections',[])];d['source']=manifest.get('source');out.append(d)
c.close()
(HERE/'pan_candidates.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps([dict(package_id=r['package_id'],heading=r['heading'],pages=r['pages'],chars=r['chars']) for r in out if r['chars'] and r['chars']<24000],ensure_ascii=True,indent=2)[:7500])
