"""Independent review of Gemini; no paid calls or execution of evaluator scripts."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import importlib.util,json,re,sys,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT))
run=Path((HERE/'run.txt').read_text(encoding='utf-8').strip());B=run.parent
G=B/'20261029T114800Z_antigravity_gemini_stage_review';O=B/'20261029T112944Z_three_pass_experiment';R=B/'20261029T114212Z_three_pass_pan_resume'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def text(p):return p.read_text(encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def delta(p):return json.loads(re.search(r'```json\s*(.*?)\s*```',text(p),re.S).group(1))
gf=read(G/'findings.json');gc=read(G/'claims.json')
all_receipts=[read(p) for d in [O,R] for p in (d/'receipts').glob('*.json')]
assert len(all_receipts)==9 and sum(bool(x.get('success')) for x in all_receipts)==8
assert sum(not bool(x.get('success')) for x in all_receipts)==1
def total(labels):
    rows=[r for r in all_receipts if r['label'] in labels];assert len(rows)==len(labels)
    return dict(cost_usd=sum(r['cost_usd'] for r in rows),request_seconds=sum(r['elapsed_seconds'] for r in rows),prompt_tokens=sum(r['usage']['prompt_tokens'] for r in rows),completion_tokens=sum(r['usage']['completion_tokens'] for r in rows))
arms={
 'ntu_single':total(['ntu_assets_single']),
 'ntu_three':total(['ntu_assets_meaning','ntu_assets_movement','ntu_assets_why']),
 'pan_single':total(['pan_dense_single_attempt1']),
 'pan_three':total(['pan_dense_meaning','pan_dense_movement','pan_dense_why_attempt1'])}
ratios={c:dict(cost=arms[c+'_three']['cost_usd']/arms[c+'_single']['cost_usd'],summed_request_duration=arms[c+'_three']['request_seconds']/arms[c+'_single']['request_seconds']) for c in ['ntu','pan']}
kg_per_oz=31.1034768/1000
calc=dict(arms=arms,ratios=ratios,known_cost_usd=sum(r['cost_usd'] for r in all_receipts if r.get('cost_usd') is not None),failed_request_cost='unknown',
 ntu=dict(principal=3414+431,total_pbd=3845+644,net_change=3845-3975,net_percent=100*(3845-3975)/3975,gain_change=431-598,gain_percent=100*(431-598)/598),
 pan=dict(disjoint=92643+2654+98636+1081+1513,overlap=93724+2654+98636+1081+1513,barberton_components=71997+12932,printed_barberton=94929,printed_operations_sum=94929+103330+51927+32124,printed_group=272310,conditional_corrected_sum=84929+103330+51927+32124,one_oz_actual_sum=65233+2428+4337,mtr_gap=30806-25043),
 tennant=dict(rounded_cost_A_m=58.1,sold_oz=1179,sold_kg=1179*kg_per_oz,derived_cost_per_kg=58.1e6/(1179*kg_per_oz),printed_cost_per_kg=1584835,assessment='Consistent within rounded cost disclosure; audit denominator0.03667kg is a unit transcription error, should36.67kg.'),
 elikhulu=dict(rounded_cost_ZAR_m=1130.9,sold_oz=53092,sold_kg=53092*kg_per_oz,derived_cost_per_kg=1130.9e6/(53092*kg_per_oz),printed_cost_per_kg=68843,assessment='Printed rate and cost/volume do not reconcile under same basis; exact corrected figure and omitted-digit cause not independently confirmed.'),
 illustrative_value=dict(expression='10000*4235',result=10000*4235,assessment='Arithmetic illustration only; not demonstrated revenue misstatement, Group total/revenue unaltered.'))
save(run/'calculations/reconciliations.json',calc)
pan_deltas={k:delta(R/'outputs'/f'pan_dense_{k}.md') for k in ['single','why']}
questions={k:[dict(priority=q['priority'],question=q['question']) for q in d['new_questions']] for k,d in pan_deltas.items()}
save(run/'pan_question_comparison.json',questions)
assert any('MTR' in q['question'] for q in questions['single'])
assert not any('MTR' in q['question'] for q in questions['why'])
target='Q-08aa5c3f257440ab'
updates={k:next(u for u in delta(O/'outputs'/f'ntu_assets_{k}.md')['updates'] if u['question_id']==target) for k in ['single','why']}
save(run/'ntu_closure_comparison.json',dict(question=next(q for q in read(O/'inputs/ntu_assets.json')['questions'] if q['question_id']==target),updates=updates))
assert all(u['status']=='resolved' for u in updates.values())
assessments=[
 ('F001','supported','NTU signed movements/percentages reproduce; useful clarity/precision, not standalone proof of workflow superiority.'),
 ('F002','supported','Both raw NTU deltas resolve original question without completing total4489scope; staged literal-valid update accepted only in isolated memory. Do not strengthen original closure into a universal mandatory SoFP reconciliation.'),
 ('F003','partly supported','Staged meaning/movement/final repeat PBD-only3845 despite acknowledging fair-value assets. Fresh single explicitly identifies mixed measurement and644withinPBD; Gemini audit incorrectly extends same scope exclusion to both arms. Copying suggests propagation but causation versus repeated model bias not isolated.'),
 ('F004','partly supported','Literal5char3 414 fails minimum8; atomic rejection confirmed. This does not make rejected analysis financially valid. Actual function is question_ledger.apply_delta; proposed ledger_validator.py does not exist.'),
 ('F005','supported','PAN meaning conflates capex/profit and revenue/EBITDA/cash; provisional AISC definitions lack supplied definitions. Final does not repeat all generic errors, so final-stage propagation not established merely from interim error.'),
 ('F006','supported','PAN worksheet and final three-pass retain197608vs196527overlap; one-oz identity71997vs71998 is false exact equality. Rounding plausible, not proven cause. Single identifies1081scope more directly; its own other arithmetic errors remain.'),
 ('F007','partly supported','429and successful continuation confirmed;3times calls means more requests, not measured3times failure probability or demonstrated cause of429. Failed billing remains unknown.'),
 ('F008','partly supported','Original PAN49 contains confirmed10000oz subtotal inconsistency,missed by both outputs.84929 restores additive agreement conditionally; no definitive issuer typo/correct replacement or42.35m revenue overstatement established.'),
 ('F009','partly supported','Both PAN prose mentionMTR5763gap. Only single has a dedicated MTR ledger question,prioritymedium; staged final five authoritative questions omit it. Claim both preserve targeted high-priority MTR questions is false.'),
 ('F010','partly supported','Observed cost/request-duration ratios confirmed and adoption not justified. Two unreplicated captures neither establish universal failure nor refute staging. Longer summed durations are not full wall latency. Both correct sign is not isolated proof of prior prompt effectiveness.')]
save(run/'gemini_finding_assessments.json',[dict(gemini_id=i,assessment=v,evidence=e) for i,v,e in assessments])
findings=[
 dict(id='F001',origin='Gemini inference',severity='medium',finding='Refuted/zero robustness gain and categorical architectural claims exceed tiny unreplicated sample.',correction='Retain do-not-adopt-yet decision; distinguish failure to demonstrate benefit from disproving an approach.'),
 dict(id='F002',origin='DeepSeek staged output; Gemini characterization',severity='high',finding='NTU scope narrowing and premature closure confirmed. Fresh single acknowledges644withinPBD; do not attribute identical scope failure to both.',correction='Judge each claim/arm independently. Preserve partial until original evidence condition met, not blanket external semantic engine.'),
 dict(id='F003',origin='Gemini source certainty',severity='medium',finding='PAN10000oz difference real; typo/corrected output and revenue effect not proved. Elikhulu cost/volume implies684835ZAR/kg versusprinted68843, but exact missing-digit explanation unconfirmed.',correction='Preserve original and conditional reconstruction; do not change company figures or infer revenue impact.'),
 dict(id='F004',origin='Gemini arithmetic notation',severity='low',finding='Tennant audit writes58.1m/0.03667kg yet result uses36.67kg.',correction='1179oz=36.671kg; derived1584358A$/kg broadly agrees with1584835 given rounded cost,not exact confirmation.'),
 dict(id='F005',origin='Gemini question-quality finding',severity='medium',finding='Both PAN prose flagMTR but staged ledger drops dedicatedMTRquestion. Gemini parity/high-priority question claim contradicted by JSON.',correction='Evaluate authoritative questions as well as narrative mentions; carry material uncertainty into ledger if it matters.'),
 dict(id='F006',origin='DeepSeek PAN single; missed by Gemini',severity='medium',finding='Single asserts272310=118853+153458 withcheckmark; actual272311. Elsewhere explicitly notes some1oz source differences.',correction='Do not mark false exact identity correct; label1oz residual and unknown cause.'),
 dict(id='F007',origin='DeepSeek PAN final; missed/understated by Gemini',severity='medium',finding='Both finals assert produced/sold difference reflects inventory timing without inventory reconciliation; single labels46855vs27829 as Evander underground, but those are total-produced values. Single also treats FY26UG total40246as46855when explaining consistency.',correction='Separate totals/underground and observed production-sales difference from unverified inventory cause. Staged final is more cautious on Tennant costs than single likely-error wording.'),
 dict(id='F008',origin='Gemini implementation proposal',severity='low',finding='ledger_validator.py proposed path absent; proposed rules lack full exception/duplicate checking and add blanket balance-sheet closure requirements.',correction='Actualvalidator question_ledger.apply_delta. Existing prompts already require closure/scope; no new SQL rules or semantic engine authorized.'),
 dict(id='F009',origin='prior Codex terminology',severity='low',finding='Earlier reviews can sound like accepting every supplied paragraph or ledger-valid output validates accounting. Current experiment confirms distinction.',correction='Read-only protocol checks and arithmetic do not establish all definitions/forecasts; retain supplied-but-unread coverage and limits.')]
save(run/'findings.json',findings)
save(run/'claims.json',[dict(id=f'C{i:03d}',origin='Gemini findings.json '+gid,claim=next(f['finding'] for f in gf if f['id']==gid),classification='Evaluator assessment of historical source and experiment',primary_evidence='OriginalNTU13,21–23;PAN48–50;exact model files/receipts as specified',independent_check=evidence,verdict='PASS' if verdict=='supported' else 'NOT VERIFIED',assessment=verdict) for i,(gid,verdict,evidence) in enumerate(assessments,1)])
now=datetime.now(timezone.utc)
audit=f'''# Codex independent review: Gemini one-pass versus three-pass audit

**Decision: RETAIN CURRENT APP WORKFLOW; THREE-PASS ADOPTION NOT JUSTIFIED BY THIS TEST. Gemini detailed conclusions require corrections.**
UTC{now.isoformat()}; Africa/Johannesburg{now.astimezone(timezone(timedelta(hours=2))).isoformat()}. Evaluator Codex. Gemini self-reported3.8Flash; not independently verified. Source review directory20261029T114800Z_antigravity_gemini_stage_review.

## Preservation and scope
Preserved155 exact files from Gemini and both experiment runs,flat numbered inputs with original paths/SHA. Verified all146 Gemini input-manifest entries. Independently rendered/viewed complete original NTU13,21,22,23 andPAN48,49,50; original PDF SHA matches experiment plans. Read Gemini audit/claims/findings/calculations as data,all completed model passes/finals and authoritative ledger JSON,requests/receipts,original question closure. No Gemini scripts executed. NTU13 used as independent confirmation only,it was not supplied to the trial models. Other source pages,companion reports,current quote,forecast and valuation NOT VERIFIED/NOT APPLICABLE. No target or recommendation.

## What Gemini gets right
NTU principal3414+431=3845 and totalPBD3845+644=4489 confirmed. Movement-130/3975=-3.27%,gain-167/598=-27.93%; staged worksheet more explicit. Both fresh finals interpret cumulative-gain decline as loss. Both prematurely propose resolvedQ-08aa5c3f257440ab with scope unresolved; staged valid delta accepts it in memory,single rejected for5char quote below8. Source/capture ambiguity does not license closure. PAN interim dictionary confuses cash/profit/capex; worksheet retains197608overlap and false71997=71998identity. Four final ledgers are not four financially validated answers.

Known successful-call subtotalUSD{calc['known_cost_usd']:.10f}. Independent exact receipts reproduce NTU cost ratio{ratios['ntu']['cost']:.4f},summed request duration ratio{ratios['ntu']['summed_request_duration']:.4f};PAN{ratios['pan']['cost']:.4f}/{ratios['pan']['summed_request_duration']:.4f}. Original429usage/cost unknown;8successfulcalls plus1failed. PAN continuation first new attempts both succeeded; configured backoff not exercised. These durations exclude some orchestration/metadata overhead and are not full end-to-end latency. More calls increase request count,not an established3xfailure probability or proven cause of429.

## Corrections to Gemini
1. Two selected,unreplicated cases do not refute staging. Extra context/call budget,task wording,cache/order and interruption differ. We have no demonstrated robust overall gain sufficient for adoption,not proof no staged approach can help. Correct sign in these samples also does not establish causal effectiveness of earlier prompt changes.
2. Staged NTU meaning/movement/final repeat PBD-only3845 while recognising fair-value assets elsewhere,an inconsistent narrowing. Fresh single explicitly explains mixed measurement and fair-value644withinPBD; Gemini audit wrongly attributes identical exclusion to both. Both closure errors remain. Copying is consistent with propagation,not controlled proof that copied text rather than repeated model bias caused it.
3. PAN10000oz source inconsistency confirmed:71997+12932=84929,printed94929;printed operations sum282310versusGroup272310. Replacing94929with84929 restores aggregate agreement conditionally. This does not prove which source value is correct,typographical cause or42.35m revenue overstatement.10000*4235=42.35m is only an illustrative multiplication;Group/revenue figures were not shown misstated. Do not alter original report or model valuation.
4. New Elikhulu cost check useful:ZAR1130.9m/(53092oz*31.1034768/1000)={calc['elikhulu']['derived_cost_per_kg']:.3f}ZAR/kg,versusprinted68843. Confirms cost/rate/volume inconsistency under matched basis. Exact missing-digit4 and corrected rate not independently confirmed from rounded data. Tennant58.1m/(1179oz*31.1034768/1000)={calc['tennant']['derived_cost_per_kg']:.3f}A$/kg,close toprinted1584835. Gemini writes denominator0.03667kg instead of36.67kg; result uses the latter. Round disclosure limits exact confirmation and causal ramp-up explanation.
5. Both PAN prose identifyMTR5763gap,but only single preserves a dedicatedMTRledger question(prioritymedium). Staged final's five questions omit it. Gemini'sboth-high-priority-questions claim is contradicted. Literal-valid JSON can still lose a material narrative uncertainty.
6. PAN single falsely marks272310=118853+153458correct (actual272311),and mislabels total-producedEvander46855/27829asunderground. Both finals assert production-sales gap is inventory timing without reconciliation. Gemini misses/understates these. Three-pass final is more cautious than single about Tennant cost causes,which deserves credit despite its other errors.
7. Actualvalidator issection_capture/question_ledger.py:apply_delta,not nonexistentledger_validator.py. Gemini proposed rules strengthen closure to mandatoryprimarySoFPbeyondoriginalcondition and lackfull exceptions/duplicate checking. Common prompt already requires matching scopes/closure; no code/guardrail adoption authorized by review.

## Recommendation
Keep the current app workflow. The user's meaning->movement->why order is useful for readability,but three paid calls should remain experimental. Next smallest candidate is to check a short source-grounded meaning/scope statement and final question-closure evidence explicitly within current output,with independent arithmetic checks where practical. Do not expand to a semantic engine or long rule checklist on this evidence. No new prompt,code,SQLguardrail or paid comparison implemented. Any further experiment needs user instruction.

Detailed assessments for all10Gemini findings,9Codex findings,claims,question/closure comparisons and independent calculations saved. Production table contents,original PDFs,Gemini/model files and flat copies verified unchanged. Last full232/targeted27offline tests retained;no application changes or regression rerun,no temporarypytestfolders. Review/preparation commands exit0;no paid calls. Versioned record preserves rather than rewrites Gemini's conclusions.
'''
(run/'audit.md').write_text(audit,encoding='utf-8')
save(run/'revision_log.json',[dict(origin='Gemini audit',revised='No demonstrated robust gain sufficient for adoption;not refuted in general.',evidence='Unreplicated two-case design'),dict(origin='Gemini F008/source causes',revised='Confirmed source inconsistencies;conditional reconstructions,not proven issuer correction or revenue impact.',evidence='Original table/calculations'),dict(origin='Gemini F009',revised='Only single preserves dedicatedMTRledgerquestion.',evidence='pan_question_comparison.json')])
spec=importlib.util.spec_from_file_location('transport',ROOT/'workflow/changes/20261028_ntu_default_run/rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
baseline=read(run/'baseline.json');c=m.ro(ROOT/'documents/analysis.sqlite');tables=m.snap(c);c.close()
preserved=dict(production_tables_unchanged=tables==baseline['production_table_hashes'],sources_unchanged=all(sha(Path(x['path']))==x['sha256'] for x in baseline['sources']),originals_and_copies_unchanged=all(sha(Path(x['original_path']))==x['sha256']==sha(Path(x['preserved_path'])) for x in read(run/'inputs/manifest.json')))
assert all(preserved.values());save(run/'preservation.json',preserved)
save(run/'execution.json',dict(command='.venv/Scripts/python.exe workflow/changes/20261029_three_pass_review/review.py',exit_code=0,paid_calls=0,gemini_scripts_executed=False,application_changes=False))
print(json.dumps(dict(audit=str(run/'audit.md'),gemini_findings_assessed=len(assessments),preservation=preserved,elikhulu_rate=calc['elikhulu']['derived_cost_per_kg'],tennant_rate=calc['tennant']['derived_cost_per_kg'])))
