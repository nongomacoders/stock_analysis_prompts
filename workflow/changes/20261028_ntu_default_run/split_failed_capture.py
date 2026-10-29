"""Split only the failed isolated capture; retain prior outputs/receipts and all source pages."""
import importlib.util
import json
from pathlib import Path
import shutil
import sqlite3
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('runner',HERE/'rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
run=Path(m.POINTER.read_text(encoding='utf-8').strip())
assert m.read(run/'receipts/section_06_compact_v2.json')['finish_reason']=='length'
plan=m.read(run/'plan.json');assert plan['section_prompt_revision']=='compact_v2'
shutil.copy2(run/'plan.json',run/'inputs/plan_v2.json')
shutil.copy2(run/'status.json',run/'inputs/pilot_v2_stop_status.json')
c=sqlite3.connect(run/'experiment.sqlite');c.row_factory=sqlite3.Row
row=dict(c.execute('SELECT * FROM sections WHERE section_number=6').fetchone())
m.save(run/'inputs/section06_before_split.json',row)
manifest=json.loads(row['manifest_json'])
original_pages={s['physical_page'] for s in manifest['selections']}
assert original_pages==set(range(22,28)),original_pages
before_texts=[s['text'] for s in manifest['selections']]
c.execute('BEGIN IMMEDIATE')
for number in [9,8,7]: c.execute('UPDATE sections SET section_number=? WHERE section_number=?',(number+1,number))
c.execute('DELETE FROM sections WHERE id=?',(row['id'],))
for part,(lo,hi) in enumerate([(22,24),(25,27)]):
    new=dict(row);new.pop('id')
    new['package_id']=row['package_id']+f'-split{part+1}'
    new['section_number']=6+part
    new['heading']=row['heading']+f' [physical pp.{lo}-{hi}]'
    piece=json.loads(row['manifest_json']);piece.pop('review',None)
    piece.update(package_id=new['package_id'],heading=new['heading'],stored_questions=None)
    piece['selections']=[s for s in piece['selections'] if lo<=s['physical_page']<=hi]
    piece['run_only_split']=dict(parent_package_id=row['package_id'],physical_pages=[lo,hi],reason='Reduce workload after completion exhaustion; all source text preserved.')
    new.update(selected_text='\n\n'.join(s['text'] for s in piece['selections']),manifest_json=json.dumps(piece,ensure_ascii=False),
               llm_response=None,prompt='',stored_questions_snapshot=None)
    c.execute('INSERT INTO sections ('+','.join(new)+') VALUES ('+','.join('?' for _ in new)+')',tuple(new.values()))
all_rows=c.execute('SELECT manifest_json FROM sections ORDER BY section_number').fetchall()
pages={s['physical_page'] for r in all_rows for s in json.loads(r[0])['selections']}
assert pages==set(range(1,39)) and len(all_rows)==10
split_texts=[s['text'] for r in all_rows for s in json.loads(r[0])['selections'] if s['physical_page'] in original_pages]
assert before_texts==split_texts
c.commit();c.close()
plan['section_prompt_revision']='split_v3';plan['questions_per_capture']=2;plan['planned_calls_after_split']=12
plan['revisions'].append(dict(utc=m.utc(),reason='Section6 exhausted32768 completion tokens;24710 reported reasoning; no final content delivered.',
 changes='Split original pages22-27 into pages22-24 and25-27, keep all text, two relevant questions per capture. Other completed analyses retained.',
 unchanged='Model, reasoning controls, routing and budgets unchanged. Raw prior attempts retained.'))
m.save(run/'plan.json',plan);shutil.copy2(HERE/'rerun.py',run/'runner_split_v3.py')
print('Split failed capture into two:10 captures,38/38 pages, all source text retained.')
