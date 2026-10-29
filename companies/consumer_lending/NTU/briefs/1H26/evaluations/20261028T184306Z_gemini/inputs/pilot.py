"""Five independent affected captures;Fireworks-only,no paid repairs or global writes."""
from datetime import datetime,timezone
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sqlite3
import sys
import pdfplumber
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT));sys.stdout.reconfigure(encoding='utf-8')
spec=importlib.util.spec_from_file_location('transport',ROOT/'workflow/changes/20261028_ntu_default_run/rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
from section_capture import packages,question_ledger as ledger
from section_capture.pdf_source import extract_structured_text
BASE=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations'
NTU=BASE/'20261028T171901Z_ntu_refined_sections';PAIRED=BASE/'20261028T163642Z_section_prompt_paired_pilot'
POINTER=HERE/'pilot_run.txt'
PROVIDER=dict(only=['fireworks'],allow_fallbacks=False,require_parameters=True)

def prepare():
    run=BASE/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_native_extraction_pilot')
    run.mkdir()
    for folder in ['inputs','outputs','requests','receipts','gemini']:(run/folder).mkdir()
    c=m.ro(ROOT/'documents/analysis.sqlite');tables=m.snap(c);c.close()
    c=m.ro(NTU/'experiment.sqlite');c.row_factory=sqlite3.Row
    cases=[]
    for label,index in [('ntu_prose',9),('ntu_assets',15),('ntu_headers',16),('ntu_fx',17)]:
        r=dict(c.execute('SELECT * FROM sections WHERE section_number=?',(index,)).fetchone())
        before=m.read(NTU/'inputs'/f'section_{index:02d}_ledger_before.json')
        cases.append(dict(case=label,ticker='NTU',sector='consumer_lending',manifest=json.loads(r['manifest_json']),questions=before,
            baseline=str(NTU/'outputs'/f'section_{index:02d}.md')))
    c.close()
    pan=m.read(PAIRED/'inputs/pan_operations.json')
    cases.append(dict(case='pan_dense',ticker='PAN',sector='mining',manifest=pan['manifest'],questions=pan['questions'],baseline=str(PAIRED/'outputs/pan_operations_new.md')))
    documents={};preserved=[];summary=[]
    for item in cases:
        label=item['case'];manifest=copy.deepcopy(item['manifest'])
        source=ROOT/('companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf' if item['ticker']=='NTU'
            else 'companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf')
        assert m.sha(source)==manifest['source']['sha256']
        documents[manifest['source']['sha256']]=dict(path=str(source),sha256=m.sha(source))
        texts=[]
        with pdfplumber.open(source) as doc:
            for selection in manifest['selections']:
                assert selection['selection_mode']=='area'
                page=doc.pages[selection['physical_page']-1]
                text=extract_structured_text(page.within_bbox(tuple(selection['bbox'])))
                assert text.strip();selection['text']=text;texts.append(text)
        manifest['ledger_contract']=1;manifest['sector']=item['sector']
        manifest['stored_questions']=ledger.render_prompt(item['questions'],context=manifest) if item['questions'] else ''
        manifest.setdefault('capture_coverage',{})['source_characters']=sum(len(text) for text in texts)
        item.update(manifest=manifest,texts=texts,source=str(source))
        m.save(run/'inputs'/f'{label}.json',item)
        prompt=packages.build_prompt(manifest,texts,sector=item['sector']);m.text(run/'inputs'/f'{label}_prompt.md',prompt)
        baseline=Path(item['baseline']);shutil.copy2(baseline,run/'inputs'/f'{label}_baseline.md')
        preserved.append(dict(path=str(baseline),sha256=m.sha(baseline)))
        summary.append(dict(case=label,ticker=item['ticker'],pages=[s['physical_page'] for s in manifest['selections']],prompt_chars=len(prompt)))
    for path in [ROOT/'section_capture/pdf_source.py',ROOT/'section_capture/question_ledger.py',Path(__file__),HERE/'before_pdf_source.py',HERE/'before_question_ledger.py']:
        dest=run/'inputs'/path.name;shutil.copy2(path,dest);preserved.append(dict(path=str(path),sha256=m.sha(path)))
    plan=dict(created_utc=m.utc(),authorization='User approved minimal extraction fix,offline affected NTU/PAN tests,and a small Fireworks sample after passing checks.',
        cases=summary,planned_calls=5,model=m.MODEL,provider=PROVIDER,reasoning='none/exclude=true',max_tokens=16384,
        documents=list(documents.values()),original_files=preserved,production_table_hashes=tables,
        retry_policy='One generation per independent case,no repairs/resubmissions/provider fallback;stop on incomplete API response. Ledger rejection retained for diagnosis.',
        comparison='Same NTU capture bounds and incoming ledger states as section trial. Extraction and short-anchor instruction both changed. PAN baseline predates three small prompt refinements;not isolated causal comparison. Not a full chronological run.',
        production_writes=False)
    m.save(run/'plan.json',plan);m.save(run/'status.json',dict(status='prepared',calls=0))
    m.text(POINTER,str(run));m.preserve(run)
    print(json.dumps(dict(run=str(run),cases=summary),indent=2))

def execute():
    run=Path(POINTER.read_text(encoding='utf-8').strip());plan=m.read(run/'plan.json')
    assert m.read(HERE/'full_test_result.json')['exit_code']==0,'Offline gate not passed'
    build=m.request_payload;m.request_payload=lambda prompt,budget:dict(build(prompt,budget),provider=PROVIDER,reasoning={'effort':'none','exclude':True})
    checks=[];failure=None
    try:
        for case in plan['cases']:
            label=case['case'];item=m.read(run/'inputs'/f'{label}.json');manifest=item['manifest'];sha=manifest['source']['sha256']
            answer,r=m.call(run,label,(run/'inputs'/f'{label}_prompt.md').read_text(encoding='utf-8'),16384)
            assert 'fireworks' in r['provider'].lower()
            r.update(reasoning_controls_sent=True,reasoning_effort_requested='none',provider_requested=PROVIDER);m.save(run/'receipts'/f'{label}.json',r)
            c=sqlite3.connect(':memory:');c.executescript(ledger.SCHEMA+'CREATE TABLE reports (sha256 TEXT,parent_report_sha256 TEXT);')
            for q in item['questions']:ledger.store(c,sha,sha,q,None,m.utc())
            before=ledger.records(c,sha);_,errors=ledger.apply_delta(c,sha,manifest['package_id'],manifest,answer,m.utc());after=ledger.records(c,sha);c.close()
            if errors:assert before==after
            check=dict(case=label,ledger_valid=not errors,errors=errors,questions_before=before,questions_after=after)
            m.save(run/'outputs'/f'{label}.validation.json',check);checks.append(check);m.save(run/'validations.json',checks)
            print('LEDGER',label,'valid',not errors,flush=True)
    except Exception as exc:
        failure=type(exc).__name__;print('STOP',failure,flush=True)
    finally:
        m.summarize(run);metrics=m.read(run/'metrics.json');metrics['reasoning']='none/exclude=true';m.save(run/'metrics.json',metrics);m.preserve(run)
        status=m.read(run/'status.json');status.update(status='incomplete' if failure else 'pilot_complete_pending_review',completed_utc=m.utc(),error_type=failure);m.save(run/'status.json',status)
        print(json.dumps(dict(status=status['status'],valid_ledgers=sum(x['ledger_valid'] for x in checks),totals=metrics['totals'])),flush=True)
    if failure:raise SystemExit(2)

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='execute':execute()
