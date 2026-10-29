"""Three independent same-input cases; prompt-only comparison, no production writes."""
from pathlib import Path
from datetime import datetime,timezone
import copy,importlib.util,json,sqlite3,shutil,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('transport',ROOT/'workflow/changes/20261028_ntu_default_run/rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
from section_capture import packages,question_ledger as ledger
BASE=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations'
OLD=BASE/'20261028T182010Z_native_extraction_pilot';POINTER=HERE/'pilot_run.txt'
PROVIDER=dict(only=['fireworks'],allow_fallbacks=False,require_parameters=True)
build=m.request_payload
m.request_payload=lambda prompt,budget:dict(build(prompt,budget),provider=PROVIDER,reasoning={'effort':'none','exclude':True})
def prepare():
    assert m.read(HERE/'test_result.json')['exit_code']==0
    run=BASE/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_prompt_clarification_pilot');run.mkdir()
    for d in ['inputs','outputs','requests','receipts','gemini']:(run/d).mkdir()
    oldplan=m.read(OLD/'plan.json');cases=[];preserved=[]
    for label in ['ntu_headers','ntu_assets','pan_dense']:
        src=OLD/'inputs'/f'{label}.json';item=m.read(src)
        # Preserve original texts, capture bounds, questions and source identities.
        manifest=copy.deepcopy(item['manifest']);texts=item['texts']
        prompt=packages.build_prompt(manifest,texts,sector=item['sector'])
        assert prompt!=(OLD/'inputs'/f'{label}_prompt.md').read_text(encoding='utf-8')
        previous=m.read(OLD/'requests'/f'{label}.json');current=m.request_payload(prompt,16384)
        assert {k:v for k,v in previous.items() if k!='messages'}=={k:v for k,v in current.items() if k!='messages'}
        for source,dest in [(src,run/'inputs'/f'{label}.json'),(OLD/'inputs'/f'{label}_prompt.md',run/'inputs'/f'{label}_baseline_prompt.md'),(OLD/'outputs'/f'{label}.md',run/'inputs'/f'{label}_baseline.md'),(OLD/'outputs'/f'{label}.validation.json',run/'inputs'/f'{label}_baseline.validation.json')]:
            shutil.copy2(source,dest);preserved.append(dict(path=str(source),sha256=m.sha(source)))
        m.text(run/'inputs'/f'{label}_prompt.md',prompt)
        cases.append(dict(case=label,pages=[s['physical_page'] for s in manifest['selections']],prompt_chars=len(prompt),baseline_prompt_chars=len((OLD/'inputs'/f'{label}_prompt.md').read_text(encoding='utf-8'))))
    for source in [ROOT/'prompts/common/12-analyst-reading-brief/v1.1.0/prompt.md',ROOT/'prompts/consumer_lending/12-analyst-reading-brief/v1.1.0/prompt.md',ROOT/'section_capture/question_ledger.py',ROOT/'section_capture/pdf_source.py',Path(__file__)]:
        dest=run/'inputs'/('common_prompt.md' if source.parts[-4]=='common' else 'consumer_prompt.md' if source.parts[-4]=='consumer_lending' else source.name)
        shutil.copy2(source,dest);preserved.append(dict(path=str(source),sha256=m.sha(source)))
    c=m.ro(ROOT/'documents/analysis.sqlite');tables=m.snap(c);c.close()
    plan=dict(created_utc=m.utc(),authorization='User proceed after proposed small affected-case comparison,2026-10-29.',cases=cases,planned_calls=3,model=m.MODEL,provider=PROVIDER,reasoning='none/exclude=true',max_tokens=16384,documents=oldplan['documents'],original_files=preserved,production_table_hashes=tables,production_writes=False,comparison='Same exact extracted text, manifest and incoming questions as native extraction pilot. Only prompt wording changes. Three independent cases, one fresh call each, old saved answers as baseline; not randomized or replicated.',retry_policy='No paid repairs/resubmissions/fallback. Stop on incomplete or transport error.')
    m.save(run/'plan.json',plan);m.save(run/'status.json',dict(status='prepared',calls=0));m.text(POINTER,str(run));m.preserve(run)
    print(str(run),flush=True)
def execute():
    run=Path(POINTER.read_text(encoding='utf-8').strip());plan=m.read(run/'plan.json')
    assert not list((run/'receipts').glob('*.json')),'Do not resubmit an existing run'
    checks=[];failure=None
    try:
        for case in plan['cases']:
            label=case['case'];item=m.read(run/'inputs'/f'{label}.json');manifest=item['manifest'];sha=manifest['source']['sha256']
            answer,r=m.call(run,label,(run/'inputs'/f'{label}_prompt.md').read_text(encoding='utf-8'),16384)
            assert 'fireworks' in r['provider'].lower()
            r.update(reasoning_controls_sent=True,reasoning_effort_requested='none',provider_requested=PROVIDER);m.save(run/'receipts'/f'{label}.json',r)
            c=sqlite3.connect(':memory:')
            try:
                c.executescript(ledger.SCHEMA+'CREATE TABLE reports (sha256 TEXT,parent_report_sha256 TEXT);')
                for q in item['questions']:ledger.store(c,sha,sha,q,None,m.utc())
                before=ledger.records(c,sha);_,errors=ledger.apply_delta(c,sha,manifest['package_id'],manifest,answer,m.utc());after=ledger.records(c,sha)
            finally:c.close()
            if errors:assert before==after
            check=dict(case=label,ledger_valid=not errors,errors=errors,questions_before=before,questions_after=after)
            m.save(run/'outputs'/f'{label}.validation.json',check);checks.append(check);m.save(run/'validations.json',checks)
            print('LEDGER',label,'valid',not errors,flush=True)
    except Exception as exc:
        failure=type(exc).__name__;print('STOP',failure,flush=True)
    finally:
        m.summarize(run);metrics=m.read(run/'metrics.json');metrics['reasoning']='none/exclude=true';m.save(run/'metrics.json',metrics);m.preserve(run)
        status=m.read(run/'status.json');status.update(status='incomplete' if failure else 'complete_pending_review',error_type=failure,completed_utc=m.utc());m.save(run/'status.json',status)
        print(json.dumps(dict(status=status['status'],totals=metrics['totals'])),flush=True)
    if failure:raise SystemExit(2)
if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='execute':execute()
