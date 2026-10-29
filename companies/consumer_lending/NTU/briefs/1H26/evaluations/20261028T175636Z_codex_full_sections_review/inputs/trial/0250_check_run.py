"""Post-run accounting,chronology and coverage checks;metadata reads only,no completions."""
from collections import Counter
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('trial',HERE/'ntu_sections.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
m=t.m;run=Path(t.POINTER.read_text(encoding='utf-8').strip());plan=m.read(run/'plan.json')
assert m.read(run/'status.json')['status']=='sections_complete_pending_review'
from section_capture.openrouter import get_openrouter_api_key
key=get_openrouter_api_key()
for p in (run/'receipts').glob('*.json'):
    r=m.read(p)
    if r.get('metadata_status')!='retrieved':
        (run/'inputs/pre_refresh_receipts').mkdir(exist_ok=True);shutil.copy2(p,run/'inputs/pre_refresh_receipts'/p.name)
        m.metadata(run,r['label'],r,key);m.save(p,r)
del key
m.summarize(run);metrics=m.read(run/'metrics.json');metrics['reasoning']='none;exclude=true,verified exact requests';m.save(run/'metrics.json',metrics)
assert metrics['calls']==metrics['successful_generations']==22
assert len(set(r['generation_id'] for r in metrics['rows']))==22
checks=m.read(run/'coverage.json');assert len(checks)==22
assert [p for x in plan['units'] for p in x['pages']]==list(range(1,39))
last=[];runtimes=[]
for check in checks:
    label=check['label'];before=m.read(run/'inputs'/f'{label}_ledger_before.json');after=m.read(run/'outputs'/f'{label}_ledger_after.json')
    assert before==last,'Chronological ledger mismatch:'+label
    if not check['ledger_valid']:assert before==after
    payload=m.read(run/'requests'/f'{label}.json');receipt=m.read(run/'receipts'/f'{label}.json')
    assert payload['provider']==t.PROVIDER and payload['reasoning']=={'effort':'none','exclude':True} and payload['max_tokens']==16384
    assert receipt['success'] and receipt['finish_reason']=='stop' and receipt['generation_metadata']['provider_name']=='Fireworks'
    assert abs(receipt['cost_usd']-receipt['generation_metadata']['total_cost'])<1e-9
    assert receipt['reasoning_controls_sent'] and receipt['reasoning_effort_requested']=='none'
    last=after
assert last==m.read(run/'outputs/final_ledger.json')
c=m.ro(run/'experiment.sqlite')
rows=c.execute('SELECT manifest_json,llm_response FROM sections ORDER BY section_number').fetchall()
assert len(rows)==24 and sum(bool(r[1]) for r in rows)==22
assert all(not r[1] for r in rows if json.loads(r[0])['analysis_role']=='navigation_only')
c.close();m.preserve(run)

# Selected arithmetic from source inputs previously independently viewed/verified;
# no new PDF-image review is claimed for this live experiment.
arithmetic=dict(principal_close=3975+382-728+383-167,other_close=702+28-116+30,
    principal_prior_half=3831+265-566+333-173,other_prior_half=672+7-90+74,
    historical_full_year_loss=77+182,trade_net=374-5,trade_loss_rate_pct=5/374*100,
    portfolio_net_cash=728+116-382-28,portfolio_income=383-167+30,
    carrying_decline=4677-4489,statutory_residual=(728+116-382-28)-(383-167+30)-182,
    amortisation_components=728-383+167+116-30,nav=1329/(780651033/1e6))
assert arithmetic['principal_close']==3845 and arithmetic['other_close']==644 and arithmetic['statutory_residual']==6
assert arithmetic['historical_full_year_loss']==259
m.save(run/'outputs/independent_calculations.json',dict(values=arithmetic,
    source_basis='Previously independently viewed identical-hash NTU source:physical8,12,13,24,25,31. No new PDF images inspected this run;no forecast/valuation validation.'))

# Preserve raw ledger proposals from rejected outputs for reviewer access;do not apply.
rejected=[];proposed=0
for check in checks:
    answer=(run/'outputs'/f'{check["label"]}.md').read_text(encoding='utf-8')
    prose=re.sub(r'```json.*?```','',answer,flags=re.S|re.I)
    m.text(run/'outputs'/f'{check["label"]}.prose.md',prose)
    blocks=[json.loads(b) for b in re.findall(r'```json\s*\n(.*?)```',answer,re.S|re.I)]
    delta=next(x for x in blocks if x.get('ledger_version')==1);proposed+=len(delta['new_questions'])
    if not check['ledger_valid']:rejected.append(dict(label=check['label'],pages=check['pages'],errors=check['errors'],unapplied_delta=delta))
m.save(run/'outputs/rejected_ledger_deltas.json',rejected)
summary=dict(captured_units=24,analysis_generations=22,navigation_units=2,captured_physical_pages=38,
    all_physical_pages_once=True,empty_initial_ledger=True,chronology_verified=True,
    valid_ledgers=sum(x['ledger_valid'] for x in checks),rejected_ledgers=len(rejected),
    proposed_new_questions_including_rejected=proposed,persistent_questions=len(last),question_statuses=dict(Counter(q['status'] for q in last)),
    cost_and_tokens=metrics['totals'],first_dispatch_to_last_accounting_seconds=metrics['observed_first_dispatch_to_last_accounting_seconds'],
    all_costs_metadata_corroborated=True,production_preservation=m.read(run/'preservation.json'),no_paid_repairs=True,
    note='Rejected deltas were not applied;their new questions/answers remain in raw briefs and rejected_ledger_deltas.json,not in persistent downstream ledger. Coverage is not semantic correctness.')
m.save(run/'verification.json',summary)
table=['| Pages | Section | Ledger |','|---|---|---|']
for check in checks:table.append(f'| {", ".join(map(str,check["pages"]))} | {check["heading"]} | {"valid" if check["ledger_valid"] else "REJECTED;raw retained"} |')
m.text(run/'RUN_SUMMARY.md','# NTU1H26 — refined section-only chronological trial\n\n'
    '22 financial sections completed through Fireworks;24 retained captures cover38 physical pages once. Ledger started empty;only previously validated states feed later prompts. Standard shared prompt/sector notes,none reasoning,16384 cap;no company-specific seed/lessons,no Stage1/2,no paid repairs.\n\n'
    +'```json\n'+json.dumps(summary,ensure_ascii=False,indent=2)+'\n```\n\n'+'\n'.join(table)+'\n\n'
    'Generation completion,literal ledger validation and financial interpretation are separate. Rejected deltas remain unapplied and need review;raw financial briefs remain available. This is not a full financial audit or valuation. Different prompts/providers/seed state prevent controlled comparisons to prior full runs.\n')
m.text(run/'gemini/PROMPT.md',f'''Review the refined NTU1H26 chronological section-only trial in Antigravity.
Run:{run}
Read AGENTS.md,workflow/WORKFLOW.md and docs/STOCK_EVALUATION_FORMAT.md section1A. Save a new UTC-versioned Gemini audit with exact inputs/hashes,primary-page coverage,independent calculations,claims/findings and limitations. No paid API calls or production/guardrail writes. Codex will independently review it.
Start RUN_SUMMARY.md,verification.json,plan.json,coverage.json,calls.csv,exact requests/outputs/receipts and outputs/final_ledger.json. All38 pages retained in24 captures;22 financial calls,2 navigation captures. Empty initial ledger;later prompts use only earlier validated state. No Stage1/2 or valuation. New generic wording:equation/operator/unit consistency,cautious first-time comparisons and POCI applicability without a blanket disclosure ban. Actual production prompt assembly,Fireworks only,reasoning none,16384 cap.
Check rejected deltas separately in outputs/rejected_ledger_deltas.json:these answers/new questions were not applied to the persistent ledger. Do not count raw proposed closures as accepted. Judge useful first-pass coverage and question evolution,not perfection. Verify semantic closures,reopened/duplicate questions,missing secondary topics and period/units/signs. Inspect p13 both portfolio rolls and ledger/prose consistency,POCI applicability,p24 prior-year historical loss259,p25 currency risk and cautious zero-rate/first-time interpretation,p31 signed amortisation and6 residual scope. Reconcile arithmetic independently against original PDFs referenced/hash-verified in plan.json;record actual physical pages inspected.
Compare cautiously with old reviewed24-unit run;provider,prompt and initial seed state differ. Earlier paired4-capture pilot is the narrower comparison. Do not invent issuer explanations,rounding plugs or faults. No target or investment recommendation requested. Prior Gemini/Codex corrections are preserved in inputs;do not repeat unsupported zero-default explanations or nonexistent model claims.
''')
print(json.dumps(summary,ensure_ascii=False,indent=2))
