"""Seal paired prompt experiment, validate accounting and record limited content review."""
from decimal import Decimal
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('pilot_driver',HERE/'pilot.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
m=t.m;ROOT=t.ROOT
run=Path(t.POINTER.read_text(encoding='utf-8').strip());plan=m.read(run/'plan.json')
assert m.read(run/'status.json')['status']=='complete_pending_semantic_review'
from section_capture.openrouter import get_openrouter_api_key
key=get_openrouter_api_key()
originals=run/'inputs/transport_receipts_original';originals.mkdir(exist_ok=True)
for path in (run/'receipts').glob('*.json'):
    r=m.read(path);payload=m.read(run/'requests'/path.name)
    assert payload['provider']==plan['provider'] and payload['reasoning']=={'effort':'none','exclude':True}
    assert payload['max_tokens']==16384
    # Preserve inherited transport bookkeeping before deriving corrected controls.
    shutil.copy2(path,originals/path.name)
    m.metadata(run,r['label'],r,key)
    assert r['metadata_status']=='retrieved'
    assert r['generation_metadata']['provider_name']=='Fireworks'
    assert abs(r['cost_usd']-r['generation_metadata']['total_cost'])<1e-9
    r.update(reasoning_controls_sent=True,reasoning_effort_requested='none',provider_requested=plan['provider'],
        bookkeeping_correction='Inherited transport assumed omitted reasoning controls; exact saved requests prove none/exclude=true. Original receipt preserved in inputs/transport_receipts_original.')
    m.save(path,r)
del key
m.summarize(run)
metrics=m.read(run/'metrics.json');metrics['reasoning']='none; exclude=true, verified in all8 exact requests'
m.save(run/'metrics.json',metrics)
assert metrics['calls']==metrics['successful_generations']==8

def offline(event,args):
    if event in {'socket.connect','socket.getaddrinfo','socket.sendto'}:raise RuntimeError('Offline review')
sys.addaudithook(offline)
rows=[]
for case in plan['cases']:
    for version in ['old','new']:
        label=case['case']+'_'+version
        answer=(run/'outputs'/f'{label}.md').read_text(encoding='utf-8')
        blocks=[json.loads(b) for b in re.findall(r'```json\s*\n(.*?)```',answer,re.S|re.I)]
        delta=next(x for x in blocks if x.get('ledger_version')==1)
        val=m.read(run/'outputs'/f'{label}.validation.json')
        r=m.read(run/'receipts'/f'{label}.json');u=r['usage']
        prose=re.sub(r'```json.*?```','',answer,flags=re.S|re.I)
        m.text(run/'outputs'/f'{label}.prose.md',prose)
        rows.append(dict(case=case['case'],version=version,ledger_valid=val['ledger_valid'],errors=val['errors'],
            proposed_questions=len(delta['new_questions']),updates=len(delta['updates']),
            prompt_chars=len(m.read(run/'requests'/f'{label}.json')['messages'][0]['content']),
            completion_tokens=u['completion_tokens'],input_tokens=u['prompt_tokens'],cost_usd=r['cost_usd'],
            elapsed_seconds=r['elapsed_seconds'],cached_tokens=(u.get('prompt_tokens_details') or {}).get('cached_tokens',0)))
totals={}
for version in ['old','new']:
    subset=[r for r in rows if r['version']==version]
    totals[version]={k:sum(r[k] for r in subset) for k in ['proposed_questions','prompt_chars','completion_tokens','input_tokens','elapsed_seconds','cached_tokens']}
    totals[version]['cost_usd']=str(sum(Decimal(str(r['cost_usd'])) for r in subset))
    totals[version]['valid_ledgers']=sum(r['ledger_valid'] for r in subset)
comparison=dict(rows=rows,totals=totals,prompt_character_reduction_pct=(1-totals['new']['prompt_chars']/totals['old']['prompt_chars'])*100,
    limitations=['Four paired captures,one generation per arm,not a full chronological/company evaluation.',
        'Both arms use Fireworks and production section reasoning none; calls ordered old then new,not randomized;cache differences recorded.',
        'Old/current context assembly changes alongside the template. No universal financial-quality or speed claim.',
        'Source hashes verified;content review uses saved extracted evidence,not new PDF image inspection.'],
    accounting_correction='Original inherited receipts mislabeled reasoning controls absent; normalized receipts corrected from exact requests,originals preserved.')
m.save(run/'comparison.json',comparison)

calculations=dict(principal=3975+382-728+383-167,other_correct=702+28-116+30,
    other_wrong_sign_in_new_ledger=702+28-116-30,net_collections=773-45,
    gross_trade=339+25+5+5,net_trade=374-5,trade_loss_rate_pct=5/374*100,
    pan_aisc_cost_millions=420.686+87.718,pan_aisc_cost_difference=508.405-(420.686+87.718),
    pan_aisc_oz=247219+25154,pan_aisc_per_oz=508405000/272373,
    pan_output_production_components=105478+2428+113613+18667+32124)
assert calculations['principal']==3845 and calculations['other_correct']==644 and calculations['other_wrong_sign_in_new_ledger']==584
assert calculations['pan_output_production_components']==272310
m.save(run/'outputs/independent_calculations.json',dict(values=calculations,
    coverage='Selected arithmetic only. NTU p13/25 and PAN p38–39/48–50 extracted text supplied;no new image inspection. PAN cell-to-column ownership remains unverified. No forecast/valuation audit.'))
new=(run/'outputs/ntu_portfolio_new.md').read_text(encoding='utf-8')
assert '702 + 28 - 116 - 30' in new and '644' in new
findings=[
    dict(id='F001',verdict='SUPPORTED WITHIN SAMPLE',finding='All8 generations completed. Revised ledgers4/4 literal-validation passes versus3/4 old;old NTU shared-page quote nonliteral. This does not validate financial truth.'),
    dict(id='F002',verdict='CONFIRMED ERROR',finding='Revised NTU p13 prose correctly adds FV30,but its ledger answer writes702+28−116−30=644. Actual equation equals584,a60 difference. Correct sign gives644. Earliest observed in this section output;original retained,not repaired.'),
    dict(id='F003',verdict='UNSUPPORTED APPLICABILITY',finding='Revised NTU p13 warns against conventional staging then requests staging/coverage evidence for POCI. Conditional sector hints reduce rigid scope but do not reliably prevent irrelevant demands. Existing approved rules not changed.'),
    dict(id='F004',verdict='PARTLY SUPPORTED',finding='Both old and revised NTU p25 include currency-risk start and next-page dependency. Revised answer is shorter with fewer questions. No unique coverage improvement over this paired old answer can be claimed.'),
    dict(id='F005',verdict='UNSUPPORTED ASSERTION',finding='First-time comparative presentation does not itself prove a newly constructed/restated comparative or a provisioning-method change. Both NTU p25 answers overinterpret those points;methodology remains unverified.'),
    dict(id='F006',verdict='NOT VERIFIED',finding='Revised PAN operational answer flags shifted extraction columns and keeps mappings provisional. Cell/asset attribution and its prior-year component residual require original-table inspection. Prompt changes do not repair extraction layout.')]
m.save(run/'findings.json',findings)
m.preserve(run)
table=['| Case | Old/new ledger valid | Old/new questions | Old/new seconds |','|---|---|---:|---:|']
for case in plan['cases']:
    a,b=[r for r in rows if r['case']==case['case']]
    table.append(f'| {case["case"]} | {a["ledger_valid"]}/{b["ledger_valid"]} | {a["proposed_questions"]}/{b["proposed_questions"]} | {a["elapsed_seconds"]:.2f}/{b["elapsed_seconds"]:.2f} |')
report=('# Section reading prompt — paired pilot\n\n'
    'Implemented one shared four-part task with conditional notes for8 sectors;existing ledger schema/source references retained. No PDF split changes,Stage1/2 reruns,production SQLite writes or new financial guardrails.\n\n'
    +'\n'.join(table)+'\n\n```json\n'+json.dumps(totals,indent=2)+'\n```\n\n'
    +'All8 costs corroborated by generation metadata. TotalUSD'+str(sum(Decimal(v['cost_usd']) for v in totals.values()))
    +'. Full offline suite226 passed in104.57s,exit0. Initial targeted run52 passed/1 failed because a test loaded standalone sector templates;updated for shared assembly.\n\n'
    +'Decision: prompt simplification and basic operation supported within sample;financial correctness still requires review. Known revised-output error:wrong FV sign in NTU ledger (584 mathematically,not644);prose is correct. Inappropriate POCI staging question and unsupported interpretations remain. No model output corrected and no paid repair loop.\n\n'
    +'Coverage:NTU p13/p25;PAN p38–39/p48–50 selected extracted captures. Source PDFs hash-verified;no new PDF image review. No current price,forecast or valuation validation. Cache/order/provider-default limitations are in comparison.json. Original prompts/code preserved in inputs/driver_and_baseline;exact requests/outputs/receipts retained. Preliminary ledger checks are not financial validation.\n')
m.text(run/'RUN_SUMMARY.md',report)
m.text(run/'audit.md',report+'\n## Findings\n\n'+''.join(f'**{f["id"]} — {f["verdict"]}:** {f["finding"]}\n\n' for f in findings)
    +'## Unverified dependencies\n\nSemantic question closure,all table-cell attribution,full-report completeness,other sectors/companies,forecast/DCF and downstream Stage1/2 outcomes NOT VERIFIED. No target/recommendation created. No new sector_guardrails proposed or codified;this is a prompt pilot. Raw model answers remain review subjects.\n\nTool/accounting revision:normalized inherited receipt fields from exact saved request controls;original receipts preserved.\n')
m.text(run/'gemini/PROMPT.md',f'''Review the simplified section prompt paired pilot in Antigravity. Subject:{run}
Read docs/STOCK_EVALUATION_FORMAT.md section1A and AGENTS.md. Save a new UTC-versioned Gemini audit with exact inputs/hashes,coverage,independent calculations and findings. No paid API calls/production writes/guardrail codification. Codex will review your saved audit.
Start RUN_SUMMARY.md,comparison.json,findings.json,inputs/*json,old/new prompts and exact outputs/requests/receipts.8 calls compare4 identical captures/question states on Fireworks,reasoning none,16384 cap;old/new order not randomized,cache differs. Original templates preserved. Common prompt plus8 conditional sector notes is implemented;no PDF splitting changes. Source paths/SHA in plan.json. Reopen original PDF tables,especially PAN multi-column production,recording actual pages inspected. Code/quote-validation success is not financial truth.
Check NTU p13 ledger wrong FV sign despite correct prose;conditional POCI applicability,duplicate questions;NTU p25 trade ECL/currency start/continuation and unsupported policy/restatement claims;PAN APM definitions/cost units/rounding and operational source attribution/buy-in scope. Count material missed topics,irrelevant questions and semantic closures. Do not demand perfection or invent faults. Distinguish usefulness from accuracy;no universal claims from4 captures. Forecast/valuation not attempted.
''')
status=m.read(run/'status.json');status.update(status='complete_with_limited_review',review_completed_utc=m.utc());m.save(run/'status.json',status)
m.save(run/'closure_checks.json',dict(checked_utc=m.utc(),eight_unique_generations=len(set(r['generation_id'] for r in metrics['rows']))==8,
    all_costs_corroborated=True,production_and_source_preservation=m.read(run/'preservation.json'),financial_validation='LIMITED;individual output corrections required',offline_full_test_exit_code=0))
print(json.dumps(dict(run=str(run),totals=totals,prompt_character_reduction_pct=comparison['prompt_character_reduction_pct'],preservation=m.read(run/'preservation.json')),indent=2))
