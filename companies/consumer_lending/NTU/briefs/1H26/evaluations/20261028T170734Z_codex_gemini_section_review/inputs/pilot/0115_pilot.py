"""Four paired captures, old/current prompts through Fireworks; no automatic repairs."""
from datetime import datetime, timezone
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
spec=importlib.util.spec_from_file_location('section_capture.previous_packages',HERE/'before/section_capture/packages.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
old.PROJECT_ROOT=ROOT
old.get_prompt_path=lambda sector:HERE/f'before/prompts/{sector}/12-analyst-reading-brief/v1.1.0/prompt.md'
from section_capture import packages,question_ledger as ledger
NTU=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T141038Z_deepseek_reviewed_logical'
POINTER=HERE/'pilot_run.txt'

def question(case,sha,filename):
    text={'ntu_portfolio':'Reconcile the principal and other purchased-debt portfolios separately; identify what further evidence is needed to compare their carrying change with statutory cash flow.',
          'ntu_shared_page':'What does this capture establish about trade-receivable credit losses and the applicable measurement basis? Keep unsupported policy conclusions open.'}.get(case)
    if not text:return []
    return [dict(question_id='Q-PILOT-'+case,question=text,priority='high',target_document=filename,
        target_section='Current captured note',evidence_required='Matching instrument,period,units and literal current-capture evidence.',
        closure_condition='Answer the stated question with the captured evidence; remain partial when a required policy or cash-flow bridge is absent.',
        status='open',answer='',evidence=[])]

def prepare():
    run=NTU.parent/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_section_prompt_paired_pilot')
    run.mkdir()
    for name in ['inputs','requests','outputs','receipts','gemini']:(run/name).mkdir()
    candidates=[]
    for case,pages in [('ntu_portfolio',[13]),('ntu_shared_page',[25])]:
        c=m.ro(NTU/'experiment.sqlite');c.row_factory=sqlite3.Row
        rows=c.execute('SELECT * FROM sections').fetchall();c.close()
        r=next(dict(r) for r in rows if [s['physical_page'] for s in json.loads(r['manifest_json'])['selections']]==pages)
        candidates.append((case,'NTU','consumer_lending',r))
    c=m.ro(ROOT/'documents/analysis.sqlite');c.row_factory=sqlite3.Row
    for case,pid in [('pan_apm','section-b40a9b163106463997e21665e978461b'),('pan_operations','section-30f5cc63683b4a5294d3f18a6a9042aa')]:
        candidates.append((case,'PAN','mining',dict(c.execute('SELECT * FROM sections WHERE package_id=?',(pid,)).fetchone())))
    tables=m.snap(c);c.close()
    cases=[];documents={}
    for case,ticker,sector,r in candidates:
        manifest=json.loads(r['manifest_json']);source=manifest['source'];sha=source['sha256']
        source_paths=[p for p in (ROOT/'companies').rglob(source['filename']) if p.suffix.lower()=='.pdf']
        resolved=next((p for p in source_paths if m.sha(p)==sha),None)
        assert resolved, 'Matching original source not found:'+source['filename']
        documents[sha]=dict(path=str(resolved),sha256=sha)
        texts=packages.extract_selection_texts(manifest,r['selected_text'],r['prompt'])
        assert len(texts)==len(manifest['selections']) and all(text.strip() for text in texts)
        questions=question(case,sha,source['filename'])
        manifest=copy.deepcopy(manifest);manifest['ledger_contract']=1;manifest['sector']=sector
        manifest['stored_questions']=ledger.render_prompt(questions,context=manifest) if questions else ''
        for selection,text in zip(manifest['selections'],texts):selection['text']=text
        item=dict(case=case,ticker=ticker,sector=sector,manifest=manifest,texts=texts,questions=questions,
            source_original_path=str(resolved),source_sha256=sha,existing_output=r.get('llm_response'))
        m.save(run/'inputs'/f'{case}.json',item)
        old_prompt=old.build_prompt(manifest,texts,sector=sector)
        new_prompt=packages.build_prompt(manifest,texts,sector=sector)
        for version,prompt in [('old',old_prompt),('new',new_prompt)]:m.text(run/'inputs'/f'{case}_{version}_prompt.md',prompt)
        cases.append(dict(case=case,ticker=ticker,pages=sorted(set(s['physical_page'] for s in manifest['selections'])),old_prompt_chars=len(old_prompt),new_prompt_chars=len(new_prompt)))
    plan=dict(created_utc=m.utc(),authorization='User approved simpler common section prompt and small NTU/non-lending Fireworks pilot.',
        cases=cases,planned_calls=8,model=m.MODEL,max_tokens=16384,reasoning='none,exclude=true to match production section analysis',
        provider=dict(only=['fireworks'],allow_fallbacks=False,require_parameters=True),
        comparison='Paired exact capture text and question state. Old complete app templates versus shared task/conditional notes/topic context. No full chronological rerun; sample does not establish universal robustness.',
        documents=list(documents.values()),original_files=[],production_table_hashes=tables,
        retry_policy='One call per case/version; no automatic repair/resubmission. Stop on incomplete transport; retain rejected ledger outputs for diagnosis.',production_writes=False)
    for path in list((HERE/'before').rglob('*'))+[Path(__file__)]:
        if path.is_file():
            dest=run/'inputs/driver_and_baseline'/path.relative_to(HERE)
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
            plan['original_files'].append(dict(path=str(path),sha256=m.sha(path)))
    m.save(run/'plan.json',plan);m.save(run/'status.json',dict(status='prepared',calls=0))
    m.text(POINTER,str(run));m.preserve(run)
    print(json.dumps(dict(run=str(run),cases=cases),indent=2))

def execute():
    run=Path(POINTER.read_text(encoding='utf-8').strip());plan=m.read(run/'plan.json')
    build=m.request_payload
    m.request_payload=lambda prompt,budget:dict(build(prompt,budget),provider=plan['provider'],reasoning={'effort':'none','exclude':True})
    failure=None;validations=[]
    try:
        for case in plan['cases']:
            item=m.read(run/'inputs'/f'{case["case"]}.json');manifest=item['manifest'];sha=manifest['source']['sha256']
            for version in ['old','new']:
                label=case['case']+'_'+version
                prompt=(run/'inputs'/f'{label}_prompt.md').read_text(encoding='utf-8')
                answer,r=m.call(run,label,prompt,16384)
                c=sqlite3.connect(':memory:');c.executescript(ledger.SCHEMA+'CREATE TABLE reports (sha256 TEXT,parent_report_sha256 TEXT);')
                for q in item['questions']:ledger.store(c,sha,sha,q,None,m.utc())
                result,errors=ledger.apply_delta(c,sha,manifest['package_id'],manifest,answer,m.utc())
                questions=ledger.records(c,sha);c.close()
                validation=dict(case=case['case'],version=version,ledger_valid=not errors,errors=errors,questions=questions)
                m.save(run/'outputs'/f'{label}.validation.json',validation);validations.append(validation)
                print('LEDGER',label,'valid',not errors,flush=True)
    except Exception as exc:
        failure=type(exc).__name__;print('STOP',failure,flush=True)
    finally:
        status=m.read(run/'status.json');status.update(status='incomplete' if failure else 'complete_pending_semantic_review',completed_utc=m.utc(),error_type=failure)
        m.save(run/'status.json',status);m.save(run/'validation_summary.json',validations);m.summarize(run);m.preserve(run)
        print(json.dumps(dict(status=status['status'],totals=m.read(run/'metrics.json')['totals'])),flush=True)
    if failure:raise SystemExit(2)

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='execute':execute()
