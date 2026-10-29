"""One authorized Stage2 repeat; only max_tokens changes. No automatic retry."""
from datetime import datetime, timezone
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding='utf-8')
ENGINE = ROOT/'workflow/changes/20261028_ntu_default_run/rerun.py'
spec = importlib.util.spec_from_file_location('transport', ENGINE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
OLD = ROOT/'companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T141038Z_deepseek_reviewed_logical'
POINTER = Path(__file__).with_name('stage2_300k_run.txt')

def prepare():
    run = OLD.parent/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_deepseek_stage2_300k')
    run.mkdir()
    for name in ['inputs', 'outputs', 'requests', 'receipts']:
        (run/name).mkdir()
    old = m.read(OLD/'requests/stage2.json')
    assert set(old) == {'model','messages','temperature','stream'}
    payload = copy.deepcopy(old)
    payload['max_tokens'] = 300000
    assert {k:v for k,v in payload.items() if k!='max_tokens'} == old
    assert len(payload['messages']) == 1 and payload['messages'][0]['role']=='user'
    originals=[]
    for path in [OLD/'requests/stage2.json', OLD/'receipts/stage2.json', OLD/'outputs/stage1.md',
                 OLD/'inputs/source_pages.json', OLD/'plan.json', ENGINE, Path(__file__)]:
        dest = run/'inputs'/path.name
        if dest.exists(): dest=run/'inputs'/('original_'+path.name)
        shutil.copy2(path,dest)
        originals.append(dict(path=str(path),sha256=m.sha(path),saved=str(dest.relative_to(run))))
    plan = m.read(OLD/'plan.json')
    c=m.ro(ROOT/'documents/analysis.sqlite')
    tables=m.snap(c);c.close()
    plan.update(created_utc=m.utc(),original_files=originals,production_table_hashes=tables,
        authorization='User requested one Stage2 rerun with hard300,000-token limit.',
        planned_calls=1,budgets={'stage2':300000},comparison_parent=str(OLD),
        comparison='Exact original Stage2 messages/model/temperature/stream; only max_tokens added. Routing is not pinned; compare actual provider.',
        known_input_error='Stage1 R370m portfolio difference is unsupported; prior independent reconciliation leaves R6m unexplained. Input retained unchanged for the cap experiment; no financial validation or publication.',
        retry_policy='One paid generation only; no retry or automatic escalation.',production_writes=False)
    m.save(run/'plan.json',plan)
    m.save(run/'status.json',dict(status='prepared',calls=0))
    m.save(run/'requests/stage2.json',payload)
    m.text(POINTER,str(run))
    m.preserve(run)
    print(json.dumps({'run':str(run),'offline_checks':'PASS: only max_tokens differs; one call; original source/table hashes verified'}))

def execute():
    run=Path(POINTER.read_text(encoding='utf-8').strip())
    payload=m.read(run/'requests/stage2.json')
    original=m.read(OLD/'requests/stage2.json')
    assert payload['max_tokens']==300000
    assert {k:v for k,v in payload.items() if k!='max_tokens'}==original
    prompt=payload['messages'][0]['content']
    assert m.request_payload(prompt,300000)==payload
    error=None
    try:
        answer,receipt=m.call(run,'stage2',prompt,300000)
        from section_capture.valuation_policy import assess_valuation_publication
        m.save(run/'outputs/publication_assessment.json',assess_valuation_publication(answer))
    except Exception as exc:
        error=type(exc).__name__
    finally:
        m.preserve(run)
        status=m.read(run/'status.json')
        status.update(status='incomplete' if error else 'generation_complete_pending_review',completed_utc=m.utc(),error_type=error)
        m.save(run/'status.json',status)
        m.summarize(run)
        metrics=m.read(run/'metrics.json')
        m.text(run/'audit.md','# NTU 1H26 — Stage2 300,000-token comparison\n\n'
            'Decision: insufficient evidence for financial validation. This is a completion-limit experiment.\n\n'
            'Exact saved Stage2 messages, model, temperature and streaming were retained. Only max_tokens=300000 was added. Default thinking and normal routing retained; provider may differ. One generation; no automatic paid retry. Original inputs preserved in inputs/ with SHA-256 manifest in plan.json. Source PDF and all production tables checked in preservation.json.\n\n'
            'Known inherited error: Stage1 claims R370m portfolio cash discrepancy; prior executed Codex reconciliation yields R6m unexplained. This run does not correct its input. No new primary PDF inspection or current market quote; forecast/valuation/financing calculations NOT VERIFIED. No target or recommendation promoted. Gemini review remains manual in Antigravity. No sector_guardrails changes.\n\n'
            'Prior evidence review: ../20261028T145027Z_codex_logical_trial_review/audit.md.\n\n'
            'Transport and accounting results:\n```json\n'+json.dumps(metrics,indent=2)+'\n```\n')
        print(json.dumps({'run':str(run),'status':status['status'],'totals':metrics['totals']}),flush=True)
    if error: raise SystemExit(2)

if __name__=='__main__':
    if sys.argv[1]=='prepare': prepare()
    elif sys.argv[1]=='execute': execute()
    else: raise ValueError(sys.argv[1])
