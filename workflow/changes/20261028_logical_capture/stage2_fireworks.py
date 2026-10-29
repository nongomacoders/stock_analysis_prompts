"""Single authorized Fireworks-only Stage2 experiment; no provider fallback/retry."""
from datetime import datetime, timezone
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import urllib.request

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('prior_comparison',HERE/'stage2_300k.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
m=t.m;ROOT=t.ROOT;OLD=t.OLD
PREVIOUS=OLD.parent/'20261028T153201Z_deepseek_stage2_300k'
POINTER=HERE/'stage2_fireworks_run.txt'
PROVIDER={'only':['fireworks'],'allow_fallbacks':False,'require_parameters':True}

def prepare():
    run=OLD.parent/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_deepseek_stage2_fireworks_300k')
    run.mkdir()
    for name in ['inputs','outputs','requests','receipts','gemini']:(run/name).mkdir()
    with urllib.request.urlopen(m.BASE+'models/'+m.MODEL+'/endpoints',timeout=30) as response:
        catalog=json.load(response)
    endpoints=[e for e in catalog['data']['endpoints'] if e.get('provider_name')=='Fireworks']
    assert endpoints and all(e['max_completion_tokens']>=300000 for e in endpoints)
    m.save(run/'inputs/fireworks_endpoints.json',dict(retrieved_utc=m.utc(),endpoints=endpoints))
    original=m.read(PREVIOUS/'requests/stage2.json')
    payload=dict(copy.deepcopy(original),provider=PROVIDER)
    assert set(original)=={'model','messages','temperature','stream','max_tokens'}
    assert original['max_tokens']==300000
    assert {k:v for k,v in payload.items() if k!='provider'}==original
    originals=[]
    for path,name in [(OLD/'requests/stage2.json','original_stage2_request.json'),
        (PREVIOUS/'requests/stage2.json','relace_300k_request.json'),
        (PREVIOUS/'receipts/stage2.json','relace_300k_receipt.json'),
        (OLD/'outputs/stage1.md','stage1.md'),(OLD/'inputs/source_pages.json','source_pages.json'),
        (OLD/'plan.json','previous_plan.json'),(t.ENGINE,'transport_engine.py'),
        (HERE/'stage2_300k.py','prior_comparison_driver.py'),(Path(__file__),'fireworks_driver.py')]:
        shutil.copy2(path,run/'inputs'/name)
        originals.append(dict(path=str(path),sha256=m.sha(path),saved='inputs/'+name))
    c=m.ro(ROOT/'documents/analysis.sqlite');tables=m.snap(c);c.close()
    plan=m.read(OLD/'plan.json')
    plan.update(created_utc=m.utc(),original_files=originals,production_table_hashes=tables,
        authorization='User explicitly requested trying Fireworks after Relace300k failure.',
        planned_calls=1,budgets={'stage2':300000},provider=PROVIDER,comparison_parent=str(PREVIOUS),
        comparison='Only provider object differs from Relace300k request; exact messages/model/temperature/stream/max_tokens retained. Omitted reasoning controls preserve provider default; implementations may differ.',
        known_input_error='Original Stage1 R370m discrepancy claim unsupported; prior independently executed reconciliation leavesR6m. Input retained unchanged to compare providers; not financial validation.',
        retry_policy='One paid attempt; no fallback providers or automatic resubmission.',production_writes=False)
    m.save(run/'plan.json',plan);m.save(run/'status.json',dict(status='prepared',calls=0))
    m.save(run/'requests/stage2.json',payload)
    m.text(POINTER,str(run));m.preserve(run)
    print(json.dumps(dict(run=str(run),offline_checks='PASS: only provider differs; ceiling supported; originals/source/production preserved')))

def execute():
    run=Path(POINTER.read_text(encoding='utf-8').strip())
    payload=m.read(run/'requests/stage2.json')
    assert payload==dict(m.read(PREVIOUS/'requests/stage2.json'),provider=PROVIDER)
    original_builder=m.request_payload
    def build(prompt,budget):return dict(original_builder(prompt,budget),provider=PROVIDER)
    m.request_payload=build
    prompt=payload['messages'][0]['content']
    assert m.request_payload(prompt,300000)==payload
    failure=None
    try:
        answer,receipt=m.call(run,'stage2',prompt,300000)
        assert 'fireworks' in str(receipt.get('provider','')).lower(), 'Unexpected provider'
        from section_capture.valuation_policy import assess_valuation_publication
        m.save(run/'outputs/publication_assessment.json',assess_valuation_publication(answer))
    except Exception as exc:
        failure=type(exc).__name__
    finally:
        m.preserve(run);m.summarize(run)
        status=m.read(run/'status.json')
        status.update(status='incomplete' if failure else 'generation_complete_pending_review',completed_utc=m.utc(),error_type=failure)
        m.save(run/'status.json',status)
        m.text(run/'audit.md','# NTU1H26 Fireworks Stage2 provider experiment\n\n'
            'Decision: insufficient evidence for financial validation. One generation, pinned Fireworks, fallback disabled,300000 combined reasoning/final-answer tokens, default thinking controls omitted. Same exact input as Relace300k; only provider object changed. No production writes or other paid calls. Exact preserved input model outputs and request/engine/driver hashes:plan.json. Source PDF referenced by original path/SHA;no new PDF inspection.\n\n'
            'Known inherited Stage1 error: allegedR370m portfolio discrepancy is unsupported; prior verified arithmetic leavesR6m unexplained. No input correction made for this provider comparison. Forecast/DCF/shares/financing/current market checks NOT VERIFIED pending independent review; no target/recommendation promoted. No new sector guardrails proposed. Prior primary-source Codex review:../20261028T145027Z_codex_logical_trial_review/audit.md.\n\n'
            'Transport/accounting metrics:\n```json\n'+json.dumps(m.read(run/'metrics.json'),indent=2)+'\n```\n')
        print(json.dumps(dict(run=str(run),status=status['status'],totals=m.read(run/'metrics.json')['totals'])),flush=True)
    if failure:raise SystemExit(2)

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='execute':execute()
    else:raise ValueError(sys.argv[1])
