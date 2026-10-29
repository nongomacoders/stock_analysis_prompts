"""Explicitly authorized PAN continuation with bounded exponential backoff."""
from pathlib import Path
from datetime import datetime,timezone
from email.utils import parsedate_to_datetime
import importlib.util,sys,shutil,time,json,urllib.error
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('trial',HERE/'experiment.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
m=t.m;OLD=Path(t.POINTER.read_text(encoding='utf-8').strip());POINTER=HERE/'pan_resume_run.txt'
def prepare():
    run=t.BASE/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_three_pass_pan_resume');run.mkdir()
    for d in ['inputs','outputs','requests','receipts','gemini']:(run/d).mkdir()
    originals=[]
    for source,dest in [(OLD/'inputs/pan_dense.json',run/'inputs/pan_dense.json'),(OLD/'inputs/pan_dense_base.md',run/'inputs/pan_dense_base.md'),(OLD/'requests/pan_dense_why.md',run/'inputs/pan_dense_why_prompt.md'),(OLD/'requests/pan_dense_why.json',run/'inputs/failed_request.json'),(OLD/'receipts/pan_dense_why.json',run/'inputs/original_failure.json'),(OLD/'outputs/pan_dense_meaning.md',run/'inputs/pan_dense_meaning.md'),(OLD/'outputs/pan_dense_movement.md',run/'inputs/pan_dense_movement.md'),(OLD/'comparison.json',run/'inputs/prior_comparison.json'),(OLD/'audit.md',run/'inputs/prior_audit.md'),(Path(__file__),run/'inputs/resume_pan.py')]:
        shutil.copy2(source,dest);originals.append(dict(path=str(source),sha256=m.sha(source)))
    prompt=(run/'inputs/pan_dense_why_prompt.md').read_text(encoding='utf-8')
    assert m.request_payload(prompt,16384)==m.read(run/'inputs/failed_request.json')
    oldplan=m.read(OLD/'plan.json');c=m.ro(t.ROOT/'documents/analysis.sqlite');tables=m.snap(c);c.close()
    plan=dict(created_utc=m.utc(),authorization='User explicitly requested redo PAN with exponential backoff,three attempts,then manual Gemini review.',previous_run=str(OLD),reuse=['PAN meaning','PAN movement','completed NTU comparison'],pending=['pan_dense_why','pan_dense_single'],max_attempts_per_pending_call=3,backoff_seconds=[15,30],respect_retry_after=True,retryable='HTTP429/500/502/503/504 before generation ID/content only; no retry after partial generation/usage or incomplete length.',documents=oldplan['documents'],original_files=originals,production_table_hashes=tables,model=m.MODEL,provider=t.PROVIDER,reasoning='none/exclude=true',max_tokens=16384,production_writes=False)
    m.save(run/'plan.json',plan);m.save(run/'status.json',dict(status='prepared',calls=0));m.text(POINTER,str(run));m.preserve(run);print(str(run),flush=True)
def pause(seconds):
    remaining=seconds
    while remaining>0:
        interval=min(15,remaining);time.sleep(interval);remaining-=interval
        if remaining>0:print('BACKOFF remaining_seconds',round(remaining,1),flush=True)
def execute():
    run=Path(POINTER.read_text(encoding='utf-8').strip());plan=m.read(run/'plan.json')
    assert not list((run/'receipts').glob('*.json')),'Do not restart or duplicate this continuation'
    events=[];failure=None;accepted={}
    try:
        for stage in ['why','single']:
            canonical='pan_dense_'+stage;source='pan_dense_why_prompt.md' if stage=='why' else 'pan_dense_base.md';prompt=(run/'inputs'/source).read_text(encoding='utf-8')
            for attempt in range(1,4):
                label=f'{canonical}_attempt{attempt}'
                try:
                    answer,r=m.call(run,label,prompt,16384)
                    assert 'fireworks' in r['provider'].lower()
                    r.update(reasoning_controls_sent=True,reasoning_effort_requested='none',provider_requested=t.PROVIDER);m.save(run/'receipts'/f'{label}.json',r)
                    shutil.copy2(run/'outputs'/f'{label}.md',run/'outputs'/f'{canonical}.md')
                    t.validate(run,'pan_dense',canonical,answer)
                    accepted[canonical]=label;events.append(dict(stage=stage,attempt=attempt,outcome='complete',label=label));m.save(run/'attempts.json',events);break
                except Exception as exc:
                    receipt_path=run/'receipts'/f'{label}.json';receipt=m.read(receipt_path) if receipt_path.exists() else {}
                    retryable=isinstance(exc,urllib.error.HTTPError) and exc.code in {429,500,502,503,504} and not receipt.get('id') and not receipt.get('stream_done') and not receipt.get('usage')
                    delay=15*2**(attempt-1)
                    if retryable and exc.headers:
                        value=exc.headers.get('Retry-After')
                        if value:
                            try:delay=max(delay,float(value))
                            except ValueError:
                                try:delay=max(delay,(parsedate_to_datetime(value)-datetime.now(timezone.utc)).total_seconds())
                                except (ValueError,TypeError):pass
                    event=dict(stage=stage,attempt=attempt,outcome='failed',label=label,error_type=type(exc).__name__,http_status=exc.code if isinstance(exc,urllib.error.HTTPError) else None,retryable=retryable,next_delay_seconds=delay if retryable and attempt<3 else None)
                    events.append(event);m.save(run/'attempts.json',events)
                    if not retryable or attempt==3:raise
                    print('RETRY',canonical,'after_seconds',delay,'next_attempt',attempt+1,flush=True);pause(delay)
            m.save(run/'accepted_attempts.json',accepted)
    except Exception as exc:failure=type(exc).__name__;print('STOP',failure,flush=True)
    finally:
        m.summarize(run);metrics=m.read(run/'metrics.json');metrics['reasoning']='none/exclude=true';m.save(run/'metrics.json',metrics);m.preserve(run)
        status=m.read(run/'status.json');status.update(status='incomplete' if failure else 'complete_pending_gemini',error_type=failure,completed_utc=m.utc());m.save(run/'status.json',status)
        print(json.dumps(dict(status=status['status'],accepted=accepted,totals=metrics['totals'])),flush=True)
    if failure:raise SystemExit(2)
if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='execute':execute()
