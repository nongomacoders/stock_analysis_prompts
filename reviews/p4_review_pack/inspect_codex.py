import sys,sqlite3,hashlib,json,pathlib
sys.stdout.reconfigure(encoding='utf-8')
p=pathlib.Path('reviews/p4_review_pack/codex_evidence');p.mkdir(exist_ok=True)
c=sqlite3.connect('file:workflow/changes/20261029_agentic_report_build/build/report.sqlite?mode=ro',uri=True)
for n,s in c.execute("select name,sql from sqlite_master where type='table'"): print(n,s)
print('REGIONS',c.execute('select table_region,count(*) from cells group by 1').fetchall())
import pypdfium2 as pdfium
pdf=pathlib.Path('companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf')
print('SHA',hashlib.sha256(pdf.read_bytes()).hexdigest())
d=pdfium.PdfDocument(str(pdf));print('PAGES',len(d))
for i in range(17,51):
 pg=d[i-1];tp=pg.get_textpage();txt=tp.get_text_range();(p/f'p{i}.txt').write_text(txt,encoding='utf-8');tp.close();pg.close()
from PySide6.QtGui import QImage
for i in [18,21,22,23,24,29,33,34,35,44,46]:
 pg=d[i-1];bm=pg.render(scale=1.8);im=QImage(bm.buffer,bm.width,bm.height,bm.stride,QImage.Format.Format_RGB32);im.save(str(p/f'p{i}.png'));bm.close();pg.close()
d.close()
for i in [29,33,34,35]:
 print('\nDB PAGE',i)
 for r in c.execute('select id,row_index,row_label,column_label,value_raw,value_num from cells where physical_page=? order by table_region,row_index,column_index',(i,)):print(r)
c.close()
