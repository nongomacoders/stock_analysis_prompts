"""Two frozen captures: fresh one-call baseline versus meaning/movement/why passes."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,sys,sqlite3,json,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('transport',ROOT/'workflow/changes/20261028_ntu_default_run/rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
from section_capture import packages,question_ledger as ledger
BASE=ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations'
OLD=BASE/'20261029T070527Z_prompt_clarification_pilot';POINTER=HERE/'run.txt'
PROVIDER=dict(only=['fireworks'],allow_fallbacks=False,require_parameters=True)
build=m.request_payload;m.request_payload=lambda prompt,budget:dict(build(prompt,budget),provider=PROVIDER,reasoning={'effort':'none','exclude':True})
TASK1='''EXPERIMENT PASS 1 OF 3: ESTABLISH ACCOUNTING MEANING.
Return a compact evidence-grounded dictionary of consequential terms in THIS capture:
term, meaning in this disclosure, instrument/measurement basis, period/unit/scope,
and how its sign affects assets or profit where established. Identify ambiguous
headers and overlapping subtotals. Cite physical pages and short source anchors.
Definitions are provisional, not established by a familiar label alone. State what
is unknown. Do not calculate movement percentages, explain drivers, create ledger
updates or produce the final reading brief. Normally <=400 words.
'''
TASK2='''EXPERIMENT PASS 2 OF 3: MEASURE MOVEMENTS.
Using the original evidence, produce a compact calculation sheet: material opening
and closing values, signed absolute changes, meaningful percentage changes, formula,
units/period/scope, and relevant reconciliations. Mark percentage comparisons with
zero/negative/incomparable bases as unsuitable when appropriate. Check overlaps
before summing. Verify and correct the provisional dictionary rather than inheriting
it blindly. Preserve unresolved source inconsistencies. No causal explanations,
ledger updates or final brief. Normally <=650 words.
'''
TASK3='''EXPERIMENT PASS 3 OF 3: INVESTIGATE AND COMPLETE THE BRIEF.
Use the original source to challenge the earlier model notes and correct any errors.
For material unusual movements, distinguish management's stated explanation from
supported deductions, tentative hypotheses and causes not established. Do not invent
a reason to answer "why". Ask specific evidence questions for unresolved causes.
An outsized percentage on a tiny base alone does not prove a problem. Incorporate
useful verified meanings/calculations into the normal final reading brief and ledger
contract below; only this final pass proposes ledger updates. Do not repeat the full
intermediate dictionary or worksheet. Retain partial status if closure is incomplete.
'''
def prepare():
    assert m.read(ROOT/'workflow/changes/20261029_prompt_clarifications/test_result.json')['exit_code']==0
    run=BASE/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_three_pass_experiment');run.mkdir()
    for d in ['inputs','outputs','requests','receipts','gemini']:(run/d).mkdir()
    preserved=[];cases=[]
    for name in ['ntu_assets','pan_dense']:
        item=m.read(OLD/'inputs'/f'{name}.json')
        prompt=packages.build_prompt(item['manifest'],item['texts'],sector=item['sector'])
        assert prompt==(OLD/'inputs'/f'{name}_prompt.md').read_text(encoding='utf-8')
        m.save(run/'inputs'/f'{name}.json',item);m.text(run/'inputs'/f'{name}_base.md',prompt)
        # Same source context, selected questions and shared guidance; no interim JSON contract.
        guidance=prompt.split('Use only the supplied evidence.',1)[1].split('Keep the brief concise',1)[0]
        context='CAPTURE CONTEXT'+prompt.split('CAPTURE CONTEXT',1)[1]
        m.text(run/'inputs'/f'{name}_interim_context.md','Use only the supplied evidence.'+guidance+'\n\n'+context)
        source=OLD/'inputs'/f'{name}.json';preserved.append(dict(path=str(source),sha256=m.sha(source)))
        cases.append(dict(case=name,pages=[s['physical_page'] for s in item['manifest']['selections']]))
    for p in [ROOT/'section_capture/pdf_source.py',ROOT/'section_capture/question_ledger.py',ROOT/'prompts/common/12-analyst-reading-brief/v1.1.0/prompt.md',ROOT/'prompts/consumer_lending/12-analyst-reading-brief/v1.1.0/prompt.md',Path(__file__)]:
        dest=run/'inputs'/f'code_{len(preserved)}{p.suffix}';shutil.copy2(p,dest);preserved.append(dict(path=str(p),sha256=m.sha(p)))
    oldplan=m.read(OLD/'plan.json');c=m.ro(ROOT/'documents/analysis.sqlite');tables=m.snap(c);c.close()
    order=['ntu_assets_single','ntu_assets_meaning','ntu_assets_movement','ntu_assets_why','pan_dense_meaning','pan_dense_movement','pan_dense_why','pan_dense_single']
    plan=dict(created_utc=m.utc(),authorization='User requested small experiment comparing three-pass meanings/calculations/why approach.',cases=cases,planned_calls=8,order=order,model=m.MODEL,provider=PROVIDER,reasoning='none/exclude=true',max_tokens_per_call=16384,temperature=0.1,documents=oldplan['documents'],original_files=preserved,production_table_hashes=tables,production_writes=False,
      rubric=['Accounting meaning and signed interpretation','Signed calculations and meaningful percentages','Disjoint scopes/no invented source corrections','Unusual movement explanations separated from hypotheses','Existing closure conditions respected','Literal/structural delta valid'],
      limitations='Two selected cases, one generation per arm/pass; not replicated/randomized. Counterbalanced arm order. Three-pass has more calls,total budget and evolving prompts, so no isolated causal claim about staging. Intermediate answers are not ledger updates.',retry_policy='No paid retries/repairs/provider fallback. Stop on incomplete/error. No Stage1/2 company valuation.')
    m.save(run/'plan.json',plan);m.save(run/'status.json',dict(status='prepared',calls=0));m.text(POINTER,str(run));m.preserve(run);print(str(run),flush=True)
def validate(run,case,label,answer):
    item=m.read(run/'inputs'/f'{case}.json');manifest=item['manifest'];sha=manifest['source']['sha256'];c=sqlite3.connect(':memory:')
    try:
        c.executescript(ledger.SCHEMA+'CREATE TABLE reports (sha256 TEXT,parent_report_sha256 TEXT);')
        for q in item['questions']:ledger.store(c,sha,sha,q,None,m.utc())
        before=ledger.records(c,sha);_,errors=ledger.apply_delta(c,sha,manifest['package_id'],manifest,answer,m.utc());after=ledger.records(c,sha)
    finally:c.close()
    if errors:assert before==after
    m.save(run/'outputs'/f'{label}.validation.json',dict(case=case,arm='single' if label.endswith('single') else 'three_pass',ledger_valid=not errors,errors=errors,questions_before=before,questions_after=after))
    print('LEDGER',label,not errors,flush=True)
def execute():
    run=Path(POINTER.read_text(encoding='utf-8').strip());plan=m.read(run/'plan.json')
    assert not list((run/'receipts').glob('*.json')),'No resubmission of an existing experiment'
    failure=None
    try:
        for label in plan['order']:
            case,stage=label.rsplit('_',1);base=(run/'inputs'/f'{case}_base.md').read_text(encoding='utf-8');context=(run/'inputs'/f'{case}_interim_context.md').read_text(encoding='utf-8')
            if stage=='single':prompt=base
            elif stage=='meaning':prompt=TASK1+'\n'+context
            elif stage=='movement':prompt=TASK2+'\n'+context+'\n\nPROVISIONAL MODEL DICTIONARY (untrusted; verify against source):\n'+(run/'outputs'/f'{case}_meaning.md').read_text(encoding='utf-8')
            else:
                prompt=TASK3+'\n'+base+'\n\nPROVISIONAL MODEL NOTES (untrusted; original source takes precedence):\n'
                for prior in ['meaning','movement']:prompt+='\n'+prior.upper()+'\n'+(run/'outputs'/f'{case}_{prior}.md').read_text(encoding='utf-8')
            answer,r=m.call(run,label,prompt,16384);assert 'fireworks' in r['provider'].lower()
            r.update(reasoning_controls_sent=True,reasoning_effort_requested='none',provider_requested=PROVIDER);m.save(run/'receipts'/f'{label}.json',r)
            if stage in ['single','why']:validate(run,case,label,answer)
    except Exception as exc:failure=type(exc).__name__;print('STOP',failure,flush=True)
    finally:
        m.summarize(run);metrics=m.read(run/'metrics.json');metrics['reasoning']='none/exclude=true';m.save(run/'metrics.json',metrics);m.preserve(run)
        status=m.read(run/'status.json');status.update(status='incomplete' if failure else 'complete_pending_review',error_type=failure,completed_utc=m.utc());m.save(run/'status.json',status)
        print(json.dumps(dict(status=status['status'],totals=metrics['totals'])),flush=True)
    if failure:raise SystemExit(2)
if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='execute':execute()
