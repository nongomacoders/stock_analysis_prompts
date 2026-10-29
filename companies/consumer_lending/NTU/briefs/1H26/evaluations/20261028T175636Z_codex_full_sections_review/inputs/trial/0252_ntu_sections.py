"""Authorized source-order NTU section-only trial using actual shared prompt assembly."""
from datetime import datetime,timezone
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sqlite3
import sys

ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT));sys.stdout.reconfigure(encoding='utf-8')
spec=importlib.util.spec_from_file_location('transport',ROOT/'workflow/changes/20261028_ntu_default_run/rerun.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
from section_capture import db,packages,question_ledger as ledger
PARENT=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T141038Z_deepseek_reviewed_logical'
AUDIT=PARENT.parent/'20261028T170734Z_codex_gemini_section_review'
POINTER=HERE/'ntu_run.txt'
PROVIDER=dict(only=['fireworks'],allow_fallbacks=False,require_parameters=True)

def prepare():
    run=PARENT.parent/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_ntu_refined_sections')
    run.mkdir()
    for name in ['inputs','outputs','requests','receipts','gemini']:(run/name).mkdir()
    prior=m.read(PARENT/'plan.json');source=prior['documents'][0]
    assert m.sha(Path(source['path']))==m.SHA==source['sha256']
    c=m.ro(ROOT/'documents/analysis.sqlite');tables=m.snap(c);c.close()
    src=m.ro(PARENT/'experiment.sqlite');dest=sqlite3.connect(run/'experiment.sqlite');src.backup(dest);src.close()
    for table in ['ledger_questions','ledger_events','section_response_attempts']:dest.execute('DELETE FROM '+table)
    columns=[r[1] for r in dest.execute('PRAGMA table_info(reports)')]
    clear=[x for x in columns if x.startswith(('stage1_','stage2_')) or x in {'target_price_zar','reference_price_zar','recommendation','upside_pct','dividend_yield_pct','tsr_pct','monitoring_triggers','valuation_summary_json'}]
    dest.execute('UPDATE reports SET '+','.join('"'+x+'"=NULL' for x in clear)+",questions_ledger=''")
    dest.execute('UPDATE reports SET parent_report_sha256=NULL WHERE sha256=?',(m.SHA,))
    rows=dest.execute('SELECT package_id,manifest_json FROM sections ORDER BY section_number').fetchall()
    pages=[];units=[]
    for pid,raw in rows:
        manifest=json.loads(raw)
        assert manifest['source']['sha256']==m.SHA
        pages.extend(s['physical_page'] for s in manifest['selections'])
        manifest['stored_questions']='';manifest['ledger_contract']=1
        manifest['review']=dict(model_brief='not_run',source_verification='not_reviewed')
        manifest.setdefault('prompt',{}).update(template_sha256=m.sha(packages.get_prompt_path('consumer_lending')),
            common_template_sha256=m.sha(packages.COMMON_PROMPT_PATH))
        dest.execute('UPDATE sections SET llm_response=NULL,prompt=?,stored_questions_snapshot=NULL,manifest_json=? WHERE package_id=?',
            ('',json.dumps(manifest,ensure_ascii=False),pid))
        units.append(dict(package_id=pid,heading=manifest['heading'],pages=[s['physical_page'] for s in manifest['selections']],role=manifest['analysis_role']))
    assert pages==list(range(1,39)) and len(units)==24
    assert sum(u['role']=='financial_analysis' for u in units)==22
    assert dest.execute('SELECT count(*) FROM ledger_questions').fetchone()[0]==0
    dest.commit();dest.close()
    preserved=[]
    paths=[AUDIT/'audit.md',AUDIT/'findings.json',AUDIT/'proposed_prompt_changes.json',PARENT/'REVIEWED_PLAN.md',
        packages.COMMON_PROMPT_PATH,packages.get_prompt_path('consumer_lending'),ROOT/'section_capture/packages.py',
        ROOT/'section_capture/question_ledger.py',ROOT/'workflow/changes/20261028_ntu_default_run/rerun.py',Path(__file__)]
    paths+=list((HERE).glob('before_*.md'))
    for i,path in enumerate(paths):
        name=f'{i:02d}_'+path.name;shutil.copy2(path,run/'inputs'/name)
        preserved.append(dict(path=str(path),saved='inputs/'+name,sha256=m.sha(path)))
    # Preserve prior answers/requests/receipts with flat names to avoid Windows nested-path limits.
    for folder in ['outputs','requests','receipts']:
        for path in (PARENT/folder).glob('*'):
            if not path.is_file():continue
            destpath=run/'inputs'/('baseline_'+folder+'_'+path.name)
            shutil.copy2(path,destpath);preserved.append(dict(path=str(path),saved='inputs/'+destpath.name,sha256=m.sha(path)))
    plan=dict(created_utc=m.utc(),ticker='NTU',period='1H26',model=m.MODEL,
        authorization='User said proceed after Codex recommendation:three small prompt refinements then full NTU section sequence.',
        documents=[source],original_files=preserved,production_table_hashes=tables,units=units,planned_calls=22,
        max_tokens=16384,reasoning_effort='none',provider=PROVIDER,stage1_calls=0,stage2_calls=0,
        initial_ledger='Empty;no pilot/later-section answers or company-specific seed questions imported.',
        retry_policy='One generation per financial capture,no paid repairs/resubmission or provider fallback. Stop on incomplete transport. Rejected ledger deltas remain rejected;preserve raw brief and carry last validated state as the app does.',
        design='Existing reviewed24-unit plan reused unchanged.22 financial sections in source order,2 navigation-only. Tests actual common+sector prompt assembly and persistent ledger in isolated DB. Different provider/prompts/seeds from old full run;not controlled causal benchmark.',
        production_writes=False)
    m.save(run/'plan.json',plan);m.save(run/'status.json',dict(status='prepared',calls=0))
    m.text(POINTER,str(run));m.preserve(run)
    print(json.dumps(dict(run=str(run),captures=24,financial_calls=22,pages=38,ledger_questions=0,stage1_calls=0,stage2_calls=0)),flush=True)

def execute():
    run=Path(POINTER.read_text(encoding='utf-8').strip());database=run/'experiment.sqlite';db.DB_PATH=database
    plan=m.read(run/'plan.json');sections=db.list_sections(m.SHA,database)
    build=m.request_payload
    m.request_payload=lambda prompt,budget:dict(build(prompt,budget),provider=PROVIDER,reasoning={'effort':'none','exclude':True})
    summarize=m.summarize
    def accurate_summary(path):
        summarize(path);metrics=m.read(path/'metrics.json');metrics['reasoning']='none;exclude=true,actual section setting';m.save(path/'metrics.json',metrics)
    m.summarize=accurate_summary
    failure=None;checks=[]
    try:
        for index,sec in enumerate(sections,1):
            manifest=copy.deepcopy(sec.manifest)
            if manifest['analysis_role']=='navigation_only':continue
            manifest['stored_questions']=db.prepare_question_ledger(m.SHA,db_path=database,for_prompt=True,context=manifest)
            texts=packages.extract_selection_texts(manifest,sec.selected_text,sec.prompt)
            assert all(text.strip() for text in texts)
            prompt=packages.build_prompt(manifest,texts,sector='consumer_lending')
            manifest['prompt']['submitted_candidate_sha256']=packages.sha256_text(prompt)
            with db.connect_db(database) as c:
                before=ledger.records(c,m.SHA)
                c.execute('UPDATE sections SET prompt=?,stored_questions_snapshot=?,manifest_json=? WHERE package_id=?',
                    (prompt,manifest['stored_questions'],json.dumps(manifest,ensure_ascii=False),sec.package_id))
            label=f'section_{index:02d}'
            m.save(run/'inputs'/f'{label}_ledger_before.json',before)
            answer,r=m.call(run,label,prompt,16384)
            assert (r.get('provider') or '').lower().startswith('fireworks')
            r.update(reasoning_controls_sent=True,reasoning_effort_requested='none',provider_requested=PROVIDER)
            m.save(run/'receipts'/f'{label}.json',r)
            saved,_=db.save_section_llm_response(sec.package_id,answer,model=m.MODEL,tokens=r['usage'],
                response_time_seconds=r['elapsed_seconds'],cost_usd=r['cost_usd'],db_path=database)
            review=saved.manifest['review'];valid=review['ledger_validation']=='valid'
            with db.connect_db(database) as c:after=ledger.records(c,m.SHA)
            if not valid:assert before==after,'Rejected delta changed persistent ledger'
            check=dict(label=label,pages=[s['physical_page'] for s in manifest['selections']],heading=manifest['heading'],
                ledger_valid=valid,errors=review['ledger_errors'],questions_before=len(before),questions_after=len(after))
            m.save(run/'outputs'/f'{label}.validation.json',check)
            m.save(run/'outputs'/f'{label}_ledger_after.json',after)
            checks.append(check);m.save(run/'coverage.json',checks)
            m.summarize(run)
            print('SECTION',label,'ledger_valid',valid,'questions',len(after),flush=True)
    except Exception as exc:
        failure=type(exc).__name__;print('STOP',failure,flush=True)
    finally:
        m.summarize(run);m.preserve(run)
        status=m.read(run/'status.json');status.update(status='incomplete' if failure else 'sections_complete_pending_review',completed_utc=m.utc(),error_type=failure)
        m.save(run/'status.json',status)
        with db.connect_db(database) as c:questions=ledger.records(c,m.SHA)
        m.save(run/'outputs/final_ledger.json',questions);m.text(run/'outputs/final_ledger.md',ledger.render(questions))
        print(json.dumps(dict(status=status['status'],sections=len(checks),valid_ledgers=sum(c['ledger_valid'] for c in checks),questions=len(questions),totals=m.read(run/'metrics.json')['totals'])),flush=True)
    if failure:raise SystemExit(2)

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='execute':execute()
