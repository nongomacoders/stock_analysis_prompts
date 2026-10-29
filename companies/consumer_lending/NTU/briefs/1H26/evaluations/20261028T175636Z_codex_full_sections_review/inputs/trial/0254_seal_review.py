"""Limited primary-source review and closure of authorized section-only trial."""
from datetime import datetime,timezone,timedelta
import importlib.util
import json
from pathlib import Path
import shutil
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('trial',HERE/'ntu_sections.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
m=t.m;ROOT=t.ROOT;run=Path(t.POINTER.read_text(encoding='utf-8').strip())
v=m.read(run/'verification.json');now=datetime.now(timezone.utc)
unapplied=sum(len(item['unapplied_delta']['new_questions']) for item in m.read(run/'outputs/rejected_ledger_deltas.json'))
assert unapplied==7,'Recompute rejected-question counts before closure'
math=dict(correct_financial_assets=5+390+3845+644,merged_cell_model_sum=5390+3845+644,
    false_assets_gap=(5390+3845+644)-4884,
    correct_ebitda=-63-29+68+597+1+216,wrong_positive_tax=-63+29+68+597+1+216,
    false_ebitda_gap=(-63+29+68+597+1+216)-790,
    possible_signed_amortisation=728-383+167+116-30,printed_amortisation=597,
    amortisation_residual=(728-383+167+116-30)-597,
    principal_net=3414+431,gain_change=431-598,
    historical_fy25_loss=77+182,
    fx_usd_closing_march2026=17.2,fx_usd_closing_march2025=18.4,fx_usd_closing_sept2025=17.3)
assert math['correct_financial_assets']==4884 and math['correct_ebitda']==790 and math['false_ebitda_gap']==58
assert math['possible_signed_amortisation']==598 and math['historical_fy25_loss']==259
m.save(run/'outputs/source_spotcheck_calculations.json',dict(values=math,
    evidence='Original identical-hash PDF physically viewed this turn:13,22,24,25,31. Equations are independent checks;the amortisation598 bridge is conditional signed reconstruction with1 residual,not an issuer-confirmed formula.'))
findings=[
 dict(id='F001',classification='SUPPORTED WITHIN RUN',earliest_stage='section_analysis',finding='All22 Fireworks generations completed;38 captured pages once,24 units including2 navigation units. Fresh ledger chronology proven;18 validated deltas and4 rejected/unapplied. No repair calls. Structural coverage does not prove semantic correctness.'),
 dict(id='F002',classification='CONFIRMED LEDGER RELIABILITY LIMIT',earliest_stage='ledger_validation',finding='Income/equity pp9–11,purchased debt p13,EPS pp18–19,and current segment pp30–31 deltas failed literal-quote checks. Entire deltas were held out as existing app behavior;7 proposed new questions across those responses were not persisted. Raw answers and unapplied deltas retained;these are not accepted closures.'),
 dict(id='F003',classification='SUPPORTED WITH LIMITS',earliest_stage='section_analysis',finding='p13 prose uses both correct signed portfolio rolls and explicitly excludes ordinary POCI Stage1/2 SICR migration demands. p25 includes currency-risk start/p26 dependency,flags exchange-rate unit-label conflict and avoids asserting a cause for zero rates. p13 ledger was rejected,so prose correctness is not an accepted ledger improvement;no causal guarantee from a single run.'),
 dict(id='F004',classification='CONFIRMED CAPTURE/INTERPRETATION FAILURE',earliest_stage='section_capture_and_section_analysis',finding='p22 other-loan5 and net trade-receivable390 cells were read as5390 in section15,leading to false sum9879 versus4884. Original table is5+390+3845+644=4884. Model also tried conventional gross−431 before recognizing printed gross+431=3845;the cumulative gain is explained by POCI. Preserve original headers/cell boundaries;do not call this a company defect.'),
 dict(id='F005',classification='CONFIRMED ATTRIBUTION/SIGN ERRORS',earliest_stage='section_analysis',finding='p24 model calls first column Debt review and third unlabelled. Original columns are Banking&specialised lending–Unsecured,Debt review,Retail,Banking–Secured. The−241 movement belongs to Unsecured;Debt review is+69. Model says reduced cumulative gain increases net carrying value;at fixed gross,3414+gain means a gain decline reduces net,not increases it.'),
 dict(id='F006',classification='CONFIRMED PERIOD MAPPING ERROR',earliest_stage='section_analysis',finding='p25 prose assigns USD18.4/GBP23.9 closing comparatives to September2025 and17.3/23.2 to March2025. Source dates are the reverse:March2025=18.4/23.9,September2025=17.3/23.2. Currency-topic coverage did not guarantee date/value alignment.'),
 dict(id='F007',classification='CONFIRMED FALSE RECONCILIATION FLAGS',earliest_stage='section_analysis',finding='p31 model adds tax29 instead of retaining printed−29 and alleges58 EBITDA discrepancy. Correct−63−29+68+597+1+216=790. It also invents an all-positive identity for a footnote component list,getting1424 versus597;source footnote does not supply those operators. Conditional signed collections/income bridge gives598 versus597,leaving1 without an asserted issuer explanation. No company defect established.'),
 dict(id='F008',classification='NOT VERIFIED',earliest_stage='review_scope',finding='Full-report semantic question closure,duplicates/reopening,all remaining section facts,forecast and valuation consequences are not independently audited. Stable IDs/literal quotes are not proof of correct economic interpretation. Only1 persistent question is resolved;15 partial,15 open,1 contradicted. No investment target/recommendation produced.')]
m.save(run/'findings.json',findings)
claims=[dict(id=f'C{i:03d}',claim=f['finding'],classification=f['classification'],origin=f['earliest_stage'],
    evidence='plan.json,coverage.json,exact outputs/validation files;source_pages/NTU_13/22/24/25/31.png where financial',
    verdict='NOT VERIFIED' if f['classification']=='NOT VERIFIED' else ('PASS' if i in [1,3] else 'FAIL'),linked_finding=f['id'],
    consequence='Review-only;no valuation impact quantified;see source_spotcheck_calculations.json') for i,f in enumerate(findings,1)]
m.save(run/'claims.json',claims)
audit=f'''# NTU1H26 — refined chronological section trial:limited Codex review

UTC:{now.isoformat()};local:{now.astimezone(timezone(timedelta(hours=2))).isoformat()}.
Decision:**section-only execution complete;ledger and financial interpretation corrections remain required**.

Implemented exactly the three authorized prompt refinements:sign/unit consistency,conditional POCI applicability and cautious first-time comparative interpretation. No PDF split,ledger-schema or stage-policy redesign. Shared prompt and sector note versions preserved in inputs with hashes;pre-change prompts also preserved. No company-specific lesson block or seed questions. Actual normal section settings:Fireworks-only,reasoning none,16384 ceiling.

## Execution and accounting

22/22 completed generations,zero provider fallback/repair calls.24 captured units cover38 physical pages exactly once;22 financial analyses and2 retained navigation captures. TotalUSD0.0702026388;input151251,completion51535,reasoning0,cached input23564. Summed request208.174s;first-dispatch-to-last-accounting340.451335s (5m40.45s). All22 costs corroborated by generation metadata. Metadata waits and wrapper time are included in wall time;client elapsed is not provider latency.

Ledger started empty. Each next prompt's before-state matches the previous persisted after-state;rejected deltas did not change it.18 valid,4 rejected.32 persistent records:15partial,15open,1contradicted,1resolved.39 proposed new questions include7 in rejected deltas. All raw briefs and unapplied changes remain saved;downstream persistent ledger does not include those7. This is not22 successful ledger updates. Different prompts/provider/initial seed state prevent controlled quality/cost comparison to older full runs.

## Source coverage and independent calculations

Original PDF SHA verified before export and after completion. Complete physical PDF pages13,22,24,25,31 independently rendered and viewed this turn;images/text retained in source_pages. Other physical pages were supplied to DeepSeek but not independently visually audited in this turn. All38 captured-page presence is distinct from content verification. Audit inputs preserve prior versions,requests,receipts and raw outputs;production tables and prior files verified unchanged.

check_run.py and outputs/independent_calculations.json reproduce selected historical arithmetic;source_spotcheck_calculations.json reproduces independently viewed source-based checks. In particular:5+390+3845+644=4884;−63−29+68+597+1+216=790;gross3414+gain431=3845. Conditional signed amortisation728−383+167+116−30=598 differs1 from printed597;source formula not asserted. Claim IDs and findings are saved separately.

## Findings

'''+''.join(f'**{f["id"]} — {f["classification"]}**\n\n{f["finding"]}\n\n' for f in findings)+'''## Handoff and boundaries

Use the simpler prompt as a first-pass brief,not a validated financial report. Main remaining issues are table-header/cell preservation,sign/period interpretation and reliable literal quote anchors. No additional code/prompt repairs or financial guardrails implemented after observing this run. Existing specific instructions do not prove improved behavior in every section. The observed model errors are not company errors.

Stage1/2,forecast/DCF,current quote,EPS/valuation model,rating and full financing audit:NOT APPLICABLE to this section-only trial. No prior valuation replaced or published. Gemini review remains manual in Antigravity;gemini/PROMPT.md identifies rejected deltas and limits. No Gemini API calls. Source filenames/hashes and before/after ledger states are preserved in plan/inputs/outputs.

Targeted offline checks27 passed in15.64s,exit0. Last full suite226 passed exit0 from prior implementation;not repeated for this two-prompt wording change. Test windows/process disposed by test completion;temporary test folder cleaned after preserving result. Tool retrospective:no policy/permission errors;one attempt to read an in-flight output before it existed returned a nonzero shell code. Check readiness before reading live outputs. All actual model/verification command exit codes0. No automatic follow-on paid work.
'''
m.text(run/'audit.md',audit)
with (run/'RUN_SUMMARY.md').open('a',encoding='utf-8',newline='') as f:
    f.write('\nLimited source review (physical13,22,24,25,31) found remaining table-cell/header mapping,sign interpretation and FX-date errors;see audit.md/findings.json. All22 completed is not financial validation. Four rejected deltas contain7 proposed new questions not in the persistent ledger. No paid corrections.\n')
with (run/'gemini/PROMPT.md').open('a',encoding='utf-8',newline='') as f:
    f.write('\nCodex limited source findings are in findings.json and audit.md. Independently verify p22 merged5/390→5390,false9879 total;p24 header identities and sign of reduced cumulative gain;p25 March/Sep closing FX mapping;p31 tax−29 and invented all-positive footnote operators. No source correction is authorized;do not count rejected raw closures as applied. Rendered original pages13,22,24,25,31 are available,but record your own inspection coverage.\n')
for name in ['ntu_sections.py','preserve.py','check_run.py','inspect_sources.py','seal_review.py']:shutil.copy2(HERE/name,run/'inputs'/name)
status=m.read(run/'status.json');status.update(status='section_trial_complete_with_review_findings',review_completed_utc=m.utc());m.save(run/'status.json',status)
m.preserve(run)
m.save(run/'completion_record.json',dict(completed_utc=m.utc(),status=status['status'],analysis_generations=22,paid_repairs=0,gemini_calls=0,
    test_exit_code=0,live_exit_code=0,accounting_verification_exit_code=0,ledger_valid=18,ledger_rejected=4,
    preservation=m.read(run/'preservation.json'),primary_pages_viewed=[13,22,24,25,31],financial_validation='Corrections required within limited review;full semantic review pending'))
print(json.dumps(dict(run=str(run),findings=len(findings),complete=True,preservation=m.read(run/'preservation.json'))))
