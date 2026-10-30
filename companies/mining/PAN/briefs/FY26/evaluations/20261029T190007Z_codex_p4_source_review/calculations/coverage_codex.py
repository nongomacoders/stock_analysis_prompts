import sqlite3,sys,pathlib
sys.stdout.reconfigure(encoding='utf-8');c=sqlite3.connect('file:workflow/changes/20261029_agentic_report_build/build/report.sqlite?mode=ro',uri=True)
for pg in [24,36]:
 print('PAGE',pg)
 print(c.execute('select row_label,column_index,value_raw from cells where physical_page=?',(pg,)).fetchall()[-24:])
for n in [911962,365207,480,1277649,740819,155716,445,896980]: print('GEO',n,c.execute('select id,physical_page,row_label from cells where value_num=?',(n,)).fetchall())
print('CONFLICT',c.execute("select id,description from conflicts where physical_page in (24,29,34,35,36)").fetchall())
for pg in range(17,51):
 txt=pathlib.Path(f'reviews/p4_review_pack/codex_evidence/p{pg}.txt').read_text(encoding='utf-8'); lines=[l for l in txt.splitlines() if l.strip()];print('PAGE',pg,' | '.join(lines[:4]))
c.close()
