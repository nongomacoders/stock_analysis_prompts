"""Seal partial experiment, refresh accounting only, and save independent assessment."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import importlib.util,json,re,shutil
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('trial',HERE/'experiment.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
m=t.m;run=Path(t.POINTER.read_text(encoding='utf-8').strip());plan=m.read(run/'plan.json')
from section_capture.openrouter import get_openrouter_api_key
key=None;preserved=run/'receipts_before_review';preserved.mkdir(exist_ok=True)
for p in sorted((run/'receipts').glob('*.json')):
    r=m.read(p);dest=preserved/p.name
    if not dest.exists():shutil.copy2(p,dest)
    request=m.read(run/'requests'/p.name)
    assert request['reasoning']=={'effort':'none','exclude':True} and request['provider']==t.PROVIDER
    r.update(reasoning_controls_sent=True,reasoning_effort_requested='none',provider_requested=t.PROVIDER)
    if r.get('id') and r.get('metadata_status')!='retrieved':
        if key is None:key=get_openrouter_api_key()
        m.metadata(run,r['label'],r,key);print('METADATA',r['label'],r.get('metadata_status'),flush=True)
    m.save(p,r)
m.summarize(run);metrics=m.read(run/'metrics.json');metrics['reasoning']='none/exclude=true'
metrics['notes']=[n for n in metrics['notes'] if not n.startswith('Provider/account routing')]+['Fireworks only requested, no provider fallback, none reasoning explicitly sent.','PAN final HTTP429 had no generation ID/usage/cost; failed-call billing unknown, known subtotal is not verified complete bill.','PAN fresh single not dispatched after stop; compare complete NTU arms only.']
m.save(run/'metrics.json',metrics)
assert metrics['calls']==7 and metrics['successful_generations']==6
failed=m.read(run/'receipts/pan_dense_why.json');assert failed['error_type']=='HTTPError' and '429' in failed['error']
assert not (run/'receipts/pan_dense_single.json').exists()
rows={r['label']:r for r in metrics['rows']}
def arm(labels):return dict(calls=len(labels),cost_usd=sum(rows[n]['cost_usd'] for n in labels),prompt_tokens=sum(rows[n]['prompt_tokens'] for n in labels),completion_tokens=sum(rows[n]['completion_tokens'] for n in labels),request_seconds=sum(rows[n]['elapsed_seconds'] for n in labels))
single=arm(['ntu_assets_single']);staged=arm(['ntu_assets_'+s for s in ['meaning','movement','why']])
valsingle=m.read(run/'outputs/ntu_assets_single.validation.json');valstaged=m.read(run/'outputs/ntu_assets_why.validation.json')
assert not valsingle['ledger_valid'] and valstaged['ledger_valid'];assert valsingle['questions_before']==valsingle['questions_after']
def delta(label):return json.loads(re.search(r'```json\s*(.*?)\s*```',(run/'outputs'/f'{label}.md').read_text(encoding='utf-8'),re.S).group(1))
target='Q-08aa5c3f257440ab'
closure={label:next(u for u in delta(label)['updates'] if u['question_id']==target) for label in ['ntu_assets_single','ntu_assets_why']}
m.save(run/'closure_comparison.json',dict(question=next(q for q in m.read(run/'inputs/ntu_assets.json')['questions'] if q['question_id']==target),updates=closure,assessment='Both propose resolved without total-scope reconciliation. Single delta rejected; three-pass accepted in memory. Production unchanged.'))
comparison=dict(ntu=dict(single=single,three_pass=staged,cost_ratio=staged['cost_usd']/single['cost_usd'],request_time_ratio=staged['request_seconds']/single['request_seconds'],single_ledger_valid=valsingle['ledger_valid'],three_pass_ledger_valid=valstaged['ledger_valid'],semantic_closure='Both fail; three-pass literal-valid closure is still unsupported.'),pan=dict(status='incomplete',completed=['meaning','movement'],failed='why,HTTP429',not_dispatched='fresh single',comparison_verdict='NOT EVALUABLE'),known_total_cost=metrics['totals']['cost_usd'],overall_seconds=metrics['observed_first_dispatch_to_last_accounting_seconds'],failed_request_cost='unknown',planned_calls=8,dispatched=7,complete=6)
m.save(run/'comparison.json',comparison)
calc={}
for name,start,end in [('ntu_net_h1',3975,3845),('ntu_net_yoy',3690,3845),('ntu_gain_h1',598,431),('ntu_unsecured_net',2950,2598),('ntu_debt_review_net',865,1092),('pan_produced',196527,272310),('pan_capex',163.6,214.9)]:calc[name]=dict(start=start,end=end,change=end-start,percent=100*(end-start)/start)
calc.update(ntu_book=dict(expression='3414+431',result=3414+431),ntu_movement=dict(expression='37-167',result=37-167),pan_disjoint=dict(expression='92643+2654+98636+1081+1513',result=92643+2654+98636+1081+1513,reported=196527),pan_overlap=dict(expression='93724+2654+98636+1081+1513',result=93724+2654+98636+1081+1513,reported=196527),pan_barberton_component=dict(expression='71997+12932',result=71997+12932,printed_total=94929),pan_total_operations=dict(expression='94929+103330+51927+32124',result=94929+103330+51927+32124,reported=272310))
m.save(run/'calculations.json',calc)
findings=[
 dict(id='F001',verdict='SUPPORTED WITHIN NTU SAMPLE',origin='movement pass/final answer',finding='Three-pass worksheet provides correct net -130(-3.3%),cumulative gain -167(-27.9%),Unsecured net-352(-11.9%),Debt review net+227(+26.2%). Final retains useful percentages.',limit='Single also gets sign and principal sums right. Extra detail is not proof of staging superiority.'),
 dict(id='F002',verdict='FAIL BOTH ARMS',origin='NTU question closure',finding='Single and staged final both propose resolvedQ-08aa5c3f257440ab while total4489scope is deferred. Three-pass valid delta accepts unsupported semantic closure in memory; single rejection prevents its application.',earliest_stage='Meaning says partially resolved; movement upgrades to resolved; final inherits.',correction='Check original closure evidence, not earlier status. No production status changed.'),
 dict(id='F003',verdict='FAIL THREE-PASS SCOPE',origin='meaning pass propagated to movement/final',finding='Meaning calls PBD-only net3845 while acknowledging other fair-value assets within PBD and unresolved4489scope. Movement and final repeat this narrowing; later passes do not fully challenge it.',correction='Use principal-book3845, distinguish other assets644 and leave totalPBD scope pending rather than assert PBD-only.'),
 dict(id='F004',verdict='PARTIAL PROCESS BENEFIT',origin='NTU literal validation',finding='Single rejected for5-character3 414quote; three-pass final passes literal validation. This does not establish financial correctness or semantic closure.'),
 dict(id='F005',verdict='FAIL PAN INTERIM MEANING',origin='meaning pass',finding='Defines costs/capex as outflows reducing profit/assets and revenue/EBITDA as inflows. Capex generally exchanges cash for a capital asset rather than immediately reducing profit; revenue/EBITDA are not cash inflows. AISC definitions are provisional because source definitions absent.',correction='Avoid generic unsupported definitions; separate cash,asset recognition,expense and performance metrics. PAN final unavailable, cannot judge correction.'),
 dict(id='F006',verdict='FAIL/UNRESOLVED PAN INTERIM',origin='movement pass',finding='Worksheet reproduces197608vs196527 FY25 overlap and leaves risk unresolved; dictionary correction71997=65233+2428+4337 actually sums71998, a1oz source difference must be retained.',correction='Disjoint reported underground92643 yields196527 using printed tailings subtotal, whose leaf consistency remains unresolved.'),
 dict(id='F007',verdict='NOT EVALUABLE',origin='transport',finding='PAN why request HTTP429Too Many Requests,no output/ID/usage; PAN fresh single not dispatched. No paid retries. Specific router/provider/account quota cause unknown.'),
 dict(id='F008',verdict='SOURCE UNCERTAINTY',origin='independent source spot-check,not model-discovered',finding='PAN49 prints FY26Barberton total94929; mining71997+BTRP12932=84929. Printed total-operation columns sum282310vsGroup272310, difference10000. Source inconsistency visible in original render and extracted capture; correct replacement/cause not established.',correction='Retain source values and alternatives; previous exact-Group conclusions did not validate these totals. Not a demonstrated effect of staging.')]
m.save(run/'findings.json',findings)
m.save(run/'claims.json',[dict(id=f'C{i:03d}',claim=f['finding'],classification='Historical source/model/transport assessment',primary_evidence='NTU21–23,PAN48–50; exact requests/receipts as applicable',independent_check='See calculations.json,closure_comparison.json and raw pass outputs',verdict='PASS' if f['verdict'].startswith('SUPPORTED') else 'NOT VERIFIED' if f['verdict'] in ['NOT EVALUABLE','SOURCE UNCERTAINTY'] else 'FAIL',finding_id=f['id']) for i,f in enumerate(findings,1)])
now=datetime.now(timezone.utc)
report=f'''# Small three-pass experiment: partial results

**Decision: clearer calculation output in NTU, but robust accuracy improvement not demonstrated. PAN comparison incomplete.**

| NTU comparison | One pass | Three passes combined |
|---|---:|---:|
| API-reported cost | ${single['cost_usd']:.6f} | ${staged['cost_usd']:.6f} |
| Summed request seconds | {single['request_seconds']:.3f} | {staged['request_seconds']:.3f} |
| Prompt tokens | {single['prompt_tokens']} | {staged['prompt_tokens']} |
| Completion tokens | {single['completion_tokens']} | {staged['completion_tokens']} |
| Ledger format/evidence accepted | No | Yes |
| Original question closed with sufficient evidence | No | No |

Three-pass NTU costs{staged['cost_usd']/single['cost_usd']:.2f}times as much in this sample. It shows useful percentage movements, but an early scope mistake survives and the final answer still closes a question whose total reconciliation is pending. The single-pass answer also gets the impairment direction right. A valid ledger is not a correct answer.

PAN completed its dictionary and calculation passes, then its why pass failed HTTP429Too Many Requests. The planned fresh single-pass PAN call was not dispatched. Do not compare an unfinished pipeline against historical answers as if it were a complete controlled pair.

Seven requests dispatched, six completed, one rate-limited; eight planned. Known API cost subtotal **${metrics['totals']['cost_usd']:.8f}**, failed-call cost unavailable. Overall dispatch-to-last-accounting **{metrics['observed_first_dispatch_to_last_accounting_seconds']:.2f}s**. Stop occurred as planned; no paid retry. The failed request supplies no evidence of which specific quota caused429.

**Recommendation:** keep this as an experiment. First review whether a source-grounded term table and final closure check can prevent earlier model mistakes being inherited. Do not adopt three calls across the app or treat more detailed prose as verified analysis. Manual Gemini handoff in gemini/review_prompt.md; no further paid calls made.
'''
m.text(run/'comparison.md',report)
audit=f'''# Independent audit: meaning, movements, why experiment

Evaluator Codex. UTC{now.isoformat()}; Africa/Johannesburg{now.astimezone(timezone(timedelta(hours=2))).isoformat()}.
Decision: **INSUFFICIENT EVIDENCE FOR THREE-PASS ADOPTION; CORRECTIONS REQUIRED IN COMPLETE NTU PAIR.**

## Experimental scope
Two frozen captures NTU21–23/PAN48–50 from prior clarification pilot. Fresh current production-template single pass versus meaning dictionary, calculation worksheet, final why/brief/ledger. Same source text, incoming questions, model{plan['model']},Fireworks only,none reasoning/excluded,temp0.1,max16384percall. Original source remains available every pass; earlier outputs explicitly untrusted. No company-specific answer seeds. Three-pass has extra total budget/calls and different task wording; counterbalanced arm order but no randomization/replication. Effects cannot be isolated to staging. Only final outputs apply to isolated in-memory ledgers, no interim application.

## Coverage and evidence
Read all six completed outputs, two NTU ledger records, incoming Q-08aa5c3f257440ab closure, exact prompts and receipts. Source PDF SHA verified against prior plan before preparation and at completion. Visually rechecked NTU22 and PAN49 using preserved renders from verified originals; prior review20261028T191648Z rendered/viewed NTU21–25 andPAN48–50. Current selected text inspected; no new full financial audit of remaining pages or cost definitions. Source render paths workflow/changes/20261028_table_extraction/renders/NTU_22.png andPAN_49.png. Baselines/code preserved in inputs; hashes in input_manifest.json and plan.json. Previous model outputs unchanged. No Gemini API or raw reasoning collected.

## Outcomes
{report}

## Independent errors and lessons
findings.json covers both engineering outcomes and financial correctness. NTU calculation worksheet correctly computes -130/3975=-3.27%,-167/598=-27.93% and selected segment movements; single answer also gets signed gain reduction correct. Three-pass accepted literal delta nevertheless resolves the original basis/carrying-value question while total4489scope remains pending. Meaning initially says partially resolved, movement says resolved, final follows. Meaning's PBD-only3845 oversimplification also survives, despite acknowledgement of fair-value assets within PBD. More passes can propagate errors.

PAN dictionary includes misleading generic cash/profit definitions, unsupported full AISC description, and speculative possible typo. Worksheet contains useful movements but retains FY25double-count197608risk without completing disjoint196527reconciliation. It corrects some grouping, but claims71997=65233+2428+4337, actually71998; source has1oz differences. No final PAN interpretation exists to judge correction. No cross-company robustness conclusion.

Independent additional source observation PAN49: FY26Barberton total94929 differs from71997+12932=84929; total-operation columns94929+103330+51927+32124=282310versus272310Group. Difference10000 remains unresolved; no replacement value or issuer cause established. Original PDF render/captured text agree; this is separate from model experiment outcomes. Prior review did not check all such subtotals. Preserve source uncertainty rather than force a reconciliation.

## Accounting and preservation
Generation command exit1 from HTTP429, not shell/permissions. Metadata refresh/review command exit0. Successful receipts account for six completions; failed receipt has no ID/usage/cost. Normalize derived reasoning_controls_sent from exact requests after preserving originals. All production tables,source PDFs,baseline files and code snapshots checked unchanged; no code/prompt edits in the app, no SQL guardrails/new valuation/Stage1/2. No regression suite rerun for standalone experiment scripts, no pytest temporary folders. Last targeted27passed,full232passed offline. Source/cost forecasts,market quote,target/recommendation NOT APPLICABLE to this section-only experiment.

## Next evaluator
Gemini should independently evaluate intermediate error propagation, whether final question closure truly satisfies original condition, and arithmetic/measurement claims. Definitions must be source-grounded and revisable; generic glossary output is not validation. Proposals remain unimplemented. No additional model calls authorized by this saved review itself.
'''
m.text(run/'audit.md',audit)
prompt=f'''Independently review the small three-pass experiment in Antigravity. Read AGENTS.md, workflow/STATE.md and docs/STOCK_EVALUATION_FORMAT.md section1A. Preserve originals and save a new versioned Gemini audit,claims/findings,input hashes,coverage and executable independent calculations. No paid API calls,code/prompt changes,production SQLite writes or corrected model-output overwrites.

Directory: {run}
Read plan.json,comparison.md,audit.md,findings.json,claims.json,calculations.json,comparison.json,closure_comparison.json,metrics.json,status.json,preservation.json,all inputs,requests,receipts and six raw outputs. Prior source review/renders: companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T191648Z_codex_native_extraction_review/source_pages. Verify original PDF SHA from plan.json; physical NTU21–23,PAN48–50.

Only NTU has a complete fresh single-versus-three-pass pair. PAN meaning/movement complete; why failed429,no answer/usage/ID,and fresh single not dispatched. Do not invent missing output or infer exact quota/zero failed-call billing. No retries. Same evidence/questions/settings; three-pass has more calls/total budget. Two selected cases not replicated/randomized.

Judge source meanings,sign conventions,percentage arithmetic,scope,unusual movement explanations and original closure compliance separately from ledger validity. Trace NTU PBD-only3845 and resolved status through meaning/movement/final; both finals still defer4489scope. Three-pass literal-valid closure may still be wrong. Check PAN dictionary's cash/profit/capex definitions,APM certainty,worksheet overlap and1oz arithmetic. Independently verify newly noticed PAN49Barberton94929 versus71997+12932=84929 and total-operation sum282310vsGroup272310,without assuming which source value to replace. Critique Codex findings and identify missed mistakes. No valuation requested. Recommend smallest next step,not automatic adoption or full run.
'''
m.text(run/'gemini/review_prompt.md',prompt);m.text(HERE/'gemini_prompt.md',prompt)
m.save(run/'input_manifest.json',[dict(path=str(p),sha256=m.sha(p)) for d in ['inputs','outputs','requests','receipts','receipts_before_review'] for p in (run/d).glob('*') if p.is_file()])
m.preserve(run)
status=m.read(run/'status.json');status.update(status='partial_experiment_reviewed_rate_limited',reviewed_utc=m.utc(),pending=['pan_dense_why (failed429)','pan_dense_single (not dispatched)']);m.save(run/'status.json',status)
m.save(run/'execution.json',dict(generation_exit_code=1,reason='HTTP429,stop-on-error plan',review_exit_code=0,paid_retries=0))
print(json.dumps(comparison))
