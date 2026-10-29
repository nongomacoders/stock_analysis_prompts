import sqlite3,pathlib,subprocess,random,json,sys
sys.stdout.reconfigure(encoding='utf-8')
p=pathlib.Path('reviews/p4_review_pack/codex_evidence');db='workflow/changes/20261029_agentic_report_build/build/report.sqlite';c=sqlite3.connect(f'file:{db}?mode=ro',uri=True);c.row_factory=sqlite3.Row
print('DOCUMENT',list(map(tuple,c.execute('select document,count(*) from cells group by 1'))));print('QUESTIONS',list(map(tuple,c.execute('select question_id,status from questions'))))
samples=random.Random(20261029).sample(c.execute('select * from cells order by id').fetchall(),5)
(p/'samples.json').write_text(json.dumps([dict(r) for r in samples],indent=2),encoding='utf-8');print('SAMPLES',json.dumps([dict(r) for r in samples],ensure_ascii=False))
print('CASH FLOWS',json.dumps([dict(r) for r in c.execute("select id,physical_page,row_label,fiscal_year,value_raw,value_num from cells where table_region='primary_cash_flows'")],ensure_ascii=False))
counts={}
for rev in ['8dc69c6','71124ab']:
 data=subprocess.run(['git','show',f'{rev}:{db}'],capture_output=True,check=True).stdout
 path=p/f'{rev}.sqlite';path.write_bytes(data);con=sqlite3.connect(f'file:{path.as_posix()}?mode=ro',uri=True);counts[rev]=dict(con.execute('select table_region,count(*) from cells group by 1'));con.close()
(p/'history_counts.json').write_text(json.dumps(counts,indent=2),encoding='utf-8');print('HISTORY',json.dumps(counts));print('SHRANK',[(k,v,counts['71124ab'].get(k,0)) for k,v in counts['8dc69c6'].items() if counts['71124ab'].get(k,0)<v])
print('MISSING GLYPHS',list(map(tuple,c.execute("select physical_page,row_label,value_raw from cells where (physical_page=34 and value_num in (11879,160097,86,6427,12796,-133,-1515)) or (physical_page=35 and value_num in (-21206,2833))"))))
c.close()
