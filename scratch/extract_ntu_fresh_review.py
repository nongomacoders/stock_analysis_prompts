from pathlib import Path
import hashlib,json,shutil,sys
import pypdfium2 as pdfium
sys.stdout.reconfigure(encoding='utf-8')
root=Path.cwd()
r=Path(Path('scratch/ntu_latest_codex_review.txt').read_text().strip())
v=json.loads((r/'independent_verification.json').read_text(encoding='utf-8'))
doc=pdfium.PdfDocument(v['pdf_path'])
texts=[]
for i in range(len(doc)):
 page=doc[i];tp=page.get_textpage();texts.append(f'--- PHYSICAL PAGE {i+1} ---\n'+tp.get_text_range());tp.close();page.close()
doc.close()
(r/'calculations/source_pages.txt').write_text('\n\n'.join(texts),encoding='utf-8')
for n in [3,23,24,31,36]: print(texts[n-1])
shutil.copy2('scratch/reconcile_ntu_fresh_review.py',r/'calculations/reconcile.py')
shutil.copy2('scratch/prepare_ntu_fresh_review.py',r/'calculations/preserve_inputs.py')
