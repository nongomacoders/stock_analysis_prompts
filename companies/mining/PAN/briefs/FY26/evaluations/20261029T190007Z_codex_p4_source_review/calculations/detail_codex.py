import sqlite3,sys
sys.stdout.reconfigure(encoding='utf-8');c=sqlite3.connect('file:workflow/changes/20261029_agentic_report_build/build/report.sqlite?mode=ro',uri=True)
for pg in [24,36]:
 print('PAGE',pg)
 for r in c.execute('select id,row_index,row_label,fiscal_year,column_index,column_label,value_raw,value_num from cells where physical_page=? order by id',(pg,)):
  if pg==36 or r[0]>=3216: print(r)
print('p29 totals',c.execute("select id,row_label,value_raw from cells where physical_page=29 and value_num in (21832,202163,223995,11626,156283,167909,12639,27442,40081)").fetchall())
c.close()
