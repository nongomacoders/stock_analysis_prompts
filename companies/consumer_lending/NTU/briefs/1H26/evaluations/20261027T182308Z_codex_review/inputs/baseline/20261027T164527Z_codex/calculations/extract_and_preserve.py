from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, sqlite3, sys
import pypdfium2 as pdfium
sys.stdout.reconfigure(encoding='utf-8')
root = Path.cwd()
run = Path(sys.argv[1])
gem = root / 'companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T163950Z_gemini'
briefs = gem.parent.parent
inputs = run / 'inputs'
inputs.mkdir(exist_ok=True)
shutil.copytree(gem, inputs / 'gemini')
for name in ('NTU_1H26_stage1_audit_response.md','NTU_1H26_stage2_valuation_note.md','NTU_1H26_stage1_forensic_prompt.md','NTU_1H26_stage2_valuation_prompt.md'):
    shutil.copy2(briefs / name, inputs / name)
pdf = root / 'companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf'
digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
conn = sqlite3.connect('file:documents/analysis.sqlite?mode=ro', uri=True)
conn.row_factory = sqlite3.Row
row = conn.execute('SELECT sha256, filename, physical_page_count FROM reports WHERE filename = ?', (pdf.name,)).fetchall()
guardrails = [dict(r) for r in conn.execute('SELECT * FROM sector_guardrails')]
conn.close()
(run / 'inputs/guardrails_snapshot.json').write_text(json.dumps(guardrails,indent=2,default=str),encoding='utf-8')
manifest = {'ticker':'NTU','period':'1H26','evaluator':'Codex','model':'not exposed by runtime','timestamp_utc':datetime.now(timezone.utc).isoformat(),'source_pdf':{'path':str(pdf),'sha256':digest,'database_rows':[dict(x) for x in row]},'inputs':[]}
for p in inputs.rglob('*'):
    if p.is_file():
        manifest['inputs'].append({'snapshot':str(p.relative_to(run)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
(run / 'inputs/manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
doc = pdfium.PdfDocument(str(pdf))
texts=[]
for i in range(len(doc)):
    page=doc[i]; textpage=page.get_textpage()
    texts.append(f'\n===== PHYSICAL PAGE {i+1} =====\n'+textpage.get_text_range())
    textpage.close();page.close()
doc.close()
(run / 'calculations/source_pages.txt').write_text('\n'.join(texts),encoding='utf-8')
(root / 'tmp/ntu_codex_run_path.txt').write_text(str(run),encoding='utf-8')
print(json.dumps({'run':str(run),'pdf_sha256':digest,'baseline_match':any(x['sha256']==digest for x in row),'pages':len(texts),'input_files':len(manifest['inputs'])},indent=2))
for n in [3,5,8,9,12,13,14,15,16,21,22,23,24,31,36]:
    (run / f'calculations/page_{n:02}.txt').write_text(texts[n-1],encoding='utf-8')