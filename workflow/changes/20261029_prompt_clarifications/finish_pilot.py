"""Account and preserve the three-call comparison; no inference requests."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import importlib.util,json,re,shutil,hashlib
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('trial',HERE/'pilot.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
m=t.m;run=Path(t.POINTER.read_text(encoding='utf-8').strip());plan=m.read(run/'plan.json')
# Read-only metadata refresh is separate from generation. Keep original receipts.
from section_capture.openrouter import get_openrouter_api_key
key=None
for p in sorted((run/'receipts').glob('*.json')):
    receipt=m.read(p)
    if receipt.get('metadata_status')=='retrieved':continue
    dest=run/'receipts_before_refresh';dest.mkdir(exist_ok=True);shutil.copy2(p,dest/p.name)
    if key is None:key=get_openrouter_api_key()
    m.metadata(run,receipt['label'],receipt,key);m.save(p,receipt)
    print('METADATA',receipt['label'],receipt['metadata_status'],flush=True)
m.summarize(run);metrics=m.read(run/'metrics.json');metrics['reasoning']='none/exclude=true'
metrics['notes']=[n for n in metrics['notes'] if not n.startswith('Provider/account routing')]+['Fireworks only; no fallback; none reasoning explicitly requested.','Three same-input independent cases; saved baselines, not randomized or replicated. No causal certainty or cost/speed guarantee.']
m.save(run/'metrics.json',metrics)
checks=m.read(run/'validations.json');assert len(checks)==3
assert metrics['calls']==metrics['successful_generations']==3
assert len({r['generation_id'] for r in metrics['rows']})==3
old_metrics=m.read(t.OLD/'metrics.json')
baseline_rows=[r for r in old_metrics['rows'] if r['label'] in {c['case'] for c in plan['cases']}]
comparison=dict(before_ledger_valid=3,after_ledger_valid=sum(c['ledger_valid'] for c in checks),before_cost_usd=sum(r['cost_usd'] for r in baseline_rows),after_cost_usd=metrics['totals']['cost_usd'],same_text_and_incoming_questions=True,only_prompt_messages_changed=True,limitations='One saved baseline and one fresh generation per case; no randomized replication; costs/cache conditions not controlled.')
m.save(run/'comparison.json',comparison)
diagnostics=[];deltas={}
for c in checks:
    label=c['case'];item=m.read(run/'inputs'/f'{label}.json');answer=(run/'outputs'/f'{label}.md').read_text(encoding='utf-8')
    delta=json.loads(re.search(r'```json\s*(.*?)\s*```',answer,re.S).group(1));deltas[label]=delta
    for update in delta['updates']:
        for ev in update.get('evidence',[]):
            quote=ev.get('quote','');normalize=lambda text:re.sub(r'\s+',' ',text).strip()
            matches=any(normalize(quote) in normalize(s.get('text','')) for s in item['manifest']['selections'] if s['physical_page']==ev.get('physical_page'))
            if len(quote.strip())<8 or not matches:diagnostics.append(dict(case=label,question_id=update['question_id'],quote=quote,characters=len(quote.strip()),literal_match=matches,minimum_length=8,reason='below minimum' if len(quote.strip())<8 else 'not literal'))
    if not c['ledger_valid']:assert c['questions_before']==c['questions_after']
m.save(run/'quote_diagnostics.json',diagnostics)
target='Q-08aa5c3f257440ab'
proposed=next(u for u in deltas['ntu_assets']['updates'] if u['question_id']==target)
m.save(run/'closure_check.json',dict(question_id=target,proposed_status=proposed['status'],proposed_answer=proposed['answer'],persisted=False,reason='Whole delta rejected; essential total-scope reconciliation still pending.'))
calc=dict(ntu_movement=dict(expression='24-191',result=24-191,reported=-167),ntu_balance=dict(expression='598-167',result=598-167,reported=431),ntu_book=dict(expression='3414+431',result=3414+431,reported=3845),pan_reported_disjoint=dict(expression='92643+2654+98636+1081+1513',result=92643+2654+98636+1081+1513,reported=196527),pan_overlap=dict(expression='93724+2654+98636+1081+1513',result=93724+2654+98636+1081+1513,reported=196527),pan_mtr=dict(expression='30806-25043',result=30806-25043,reported=None))
m.save(run/'calculations.json',calc)
findings=[
 dict(id='F001',verdict='SUPPORTED WITHIN SAMPLE',origin='section answer,NTU24',finding='Headers case now correctly calls cumulative gain decrease167 an impairment loss, splits acquired+24/historical-191 and rejects reserve-release interpretation.',limit='Assets case still contradicts this sign; not a robust global correction.'),
 dict(id='F002',verdict='FAIL',origin='section answer and ledger,NTU21-23',finding='Assets case still proposes resolved for Q-08aa5c3f257440ab while4489scope remains pending; prose wrongly calls cumulative gain decline167 a net impairment gain.',correction='Retain partial and carry signed balance change correctly. Raw proposal was not persisted.'),
 dict(id='F003',verdict='FAIL',origin='ledger evidence anchor',finding='Assets delta rejected: quote3 414 is only5characters, below8 minimum; it is literal in source text. Validator reports not literal for both length and matching failures.',impact='Entire delta unapplied, before/after unchanged; no valid closure persisted.',correction='No validator softening; diagnose minimum-length versus match separately. No repair implemented.'),
 dict(id='F004',verdict='PARTLY SUPPORTED',origin='PAN48-50 aggregation',finding='New answer avoids prior explicit197608 allegation and leaves FY25 group/operation1081scope unresolved; it does not demonstrate the disjoint196527 reconciliation. It notices MTR25043vs30806 source inconsistency.',limit='Avoidance of erroneous sum is not correct complete reconciliation; grouped headers still imperfect.'),
 dict(id='F005',verdict='FAIL',origin='PAN model inference',finding='New PAN answer speculates column/scope error or missing digit in costs without source proof, and misstates FY26 MTR tailings total as51927: actual tailings row repeats46164;51927 is gold-produced-total including5763buy-in.',correction='Keep row/column scope separate; verify alleged source contradictions against original table, not adjacent row.',impact='New unsupported source-defect claims; no quantified valuation effect.'),
 dict(id='F006',verdict='NOT VERIFIED',origin='cross-case/overall robustness',finding='One fresh answer per case insufficient to claim repaired prompt robustness; two valid ledgers vs three baseline. Do not advance to full run on these metrics alone.',correction='Independent Gemini review in Antigravity; no further paid calls without user instruction.')]
m.save(run/'findings.json',findings)
claims=[dict(id=f'C{i:03d}',claim=f['finding'],classification='Model output assessment against historical source',primary_evidence='NTU24,NTU21–23,PAN48–50 as specified',independent_check=f.get('correction',f.get('limit','See calculations.json')),verdict='PASS' if f['verdict']=='SUPPORTED WITHIN SAMPLE' else 'NOT VERIFIED' if f['verdict'] in ['NOT VERIFIED','PARTLY SUPPORTED'] else 'FAIL',finding_id=f['id']) for i,f in enumerate(findings,1)]
m.save(run/'claims.json',claims)
now=datetime.now(timezone.utc)
audit=f'''# Three prompt clarifications: same-input affected-case comparison

Decision: **MIXED RESULTS; CORRECTIONS REQUIRED. No full chronological rerun recommended yet.**
Evaluator Codex; UTC {now.isoformat()}, Africa/Johannesburg {now.astimezone(timezone(timedelta(hours=2))).isoformat()}.

## Scope and measurements
Three independent cases: NTU24, NTU21–23 and PAN48–50. Exactly same saved extracted text, manifests, incoming questions and request controls as previous native-extraction pilot; new common/consumer/ledger wording only. Saved old answers, no new baseline generations. No randomized/replicated sampling; model variability/caching prevent strong causal or efficiency claims. All original baseline outputs preserved. Fireworks only,{plan['model']},none reasoning/excluded,16384cap,temp0.1,no fallback or paid repair. No Stage1/2.

All3 generations complete; {comparison['after_ledger_valid']}/3 valid deltas vs3/3 baseline. API-reported costUSD{metrics['totals']['cost_usd']:.10f}; prompt{metrics['totals']['prompt_tokens']},completion{metrics['totals']['completion_tokens']},reasoning{metrics['totals']['reasoning_tokens']},cached{metrics['totals']['cached_prompt_tokens']}. Summed request{metrics['totals']['elapsed_seconds']:.3f}s, first-dispatch-to-last-accounting{metrics['observed_first_dispatch_to_last_accounting_seconds']:.6f}s. Metrics/receipts record actual IDs,provider,finish,cost source and metadata status; accounting is not invoice verification.

## Evidence coverage
Read all three new answers and raw JSON/validation records, old same-case answers, incoming question and prompts. Verified source SHA from prior plan before preparation and after completion. Visually viewed preserved source renders of NTU24 and PAN48/49 from hash-verified originals; NTU21–23/PAN50 original-page review retained in prior Codex audit20261028T191648Z, with current supplied text read. No newly rendered pages this turn; other PDFs/pages, cost definitions and financial projections NOT VERIFIED. Source render paths remain workflow/changes/20261028_table_extraction/renders; prior review source_pages retains full9-page evidence. No market quote, target or recommendation: valuation NOT APPLICABLE.

## Findings and analytical lessons
NTU headers case improves: signed24-191=-167 and598-167=431, loss rather than release. However assets case calls the same decline a net impairment gain despite identifying positive cumulative-gain convention. That answer still proposes resolvedQ-08aa5c3f257440ab while deferring4489scope. Proposed resolution never persists because atomic delta rejects quote3 414 (5chars, minimum8). Diagnostic confirms it is literal; generic validator wording masks short-anchor cause. Do not count literal validity as financial validation or proposed closure as accepted.

PAN no longer alleges197608from double counting, but does not show correct disjoint FY25sum92643+2654+98636+1081+1513=196527. It leaves1081scope unresolved. This is partial improvement, not completed reconciliation. MTR FY25tailings25043vs30806 remains genuine source uncertainty; correct Group sum uses printed subtotal98636 and does not validate each leaf. New answer claims FY26tailings46164vs51927; source tailings is46164 in both asset/total columns, while51927 belongs gold-produced-total (=46164+5763buy-in). Unsupported cost typo/column explanations remain. Compare source rows before diagnosing issuer errors.

## Preservation, verification and next step
Source PDFs, all production tables, previous baseline files and code snapshots unchanged (preservation.json); in-memory ledger only, no new SQL guardrails or app/prompt changes during pilot. Prior prompt/ledger offline checks27passed,exit0; full app232passed earlier. No regression tests repeated for experiment scripts, no temporary pytest folders. Generation command exit0, all3 complete; this is operational success only. Findings,claims,quote diagnostics,calculations,originals/input hashes and manual Gemini prompt preserved. No paid repairs. Recommend independent Gemini review before another change; three wording clarifications have not demonstrated reliable overall correction.
'''
m.text(run/'audit.md',audit)
prompt=f'''Review this three-case prompt-only comparison in Antigravity. Read AGENTS.md and docs/STOCK_EVALUATION_FORMAT.md section1A; Gemini evaluates DeepSeek, then Codex evaluates Gemini. Save a new versioned Gemini audit with input hashes, inspected/unread coverage, claims, findings and independent calculations. Do not change code/prompts/SQLite or call paid models.

Run directory: {run}
Read plan.json,audit.md,findings.json,claims.json,comparison.json,calculations.json,quote_diagnostics.json,closure_check.json,metrics.json,preservation.json,all inputs and all raw outputs/validation records. Old same-case prompts/answers are preserved in inputs. Inspect exact requests/receipts. Only wording changed; source text/questions/settings identical. One generation per case is not proof of causality or robustness.

Check original source PDFs from plan.json,verify SHA,physical pages from1: NTU21–24;PAN48–50. Prior source renders/review: companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T191648Z_codex_native_extraction_review/source_pages. Judge each claimed improvement and regression against original evidence. Headers case now calls167loss; assets still calls decline167gain and resolvesQ-08aa5c3f257440ab with4489scope deferred. Assets delta rejected quote3 414: distinguish literal match from8char minimum, and preserve atomic rejection. PAN no longer shows197608but leaves FY25scope unresolved; test disjoint196527sum without validating inconsistent MTRleaf. Check claimed FY26MTR46164vs51927 against source: tailings46164bothcolumns, total51927includes5763buy-in. Examine remaining speculative cost/column/typo claims.

Separate financial correctness, semantic closure, literal validation and completed calls. Review Codex findings critically; identify evaluator mistakes and missed DeepSeek errors. No valuation requested. Recommend the next smallest useful step; avoid complex extraction or repetitive prompt growth. Do not implement proposed changes or rerun models.
'''
m.text(run/'gemini/review_prompt.md',prompt);m.text(HERE/'gemini_prompt.md',prompt)
files=[p for d in ['inputs','outputs','requests','receipts','receipts_before_refresh'] for p in (run/d).glob('*') if p.is_file()]
m.save(run/'input_manifest.json',[dict(path=str(p),sha256=m.sha(p)) for p in files])
m.preserve(run)
status=m.read(run/'status.json');status.update(status='complete_mixed_results_gemini_pending',reviewed_utc=m.utc());m.save(run/'status.json',status)
print(json.dumps(dict(cost=metrics['totals']['cost_usd'],wall_seconds=metrics['observed_first_dispatch_to_last_accounting_seconds'],ledger_valid=comparison['after_ledger_valid'],quote_failures=diagnostics,metadata=[(r['label'],r['metadata_status']) for r in metrics['rows']]),ensure_ascii=False))
