"""Save Codex assessment of Gemini's full section review;no paid calls or app edits."""
from datetime import datetime,timezone,timedelta
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import sys
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
run=Path((HERE/'review_run.txt').read_text(encoding='utf-8'));BASE=run.parent
GEMINI=BASE/'20261028T174829Z_gemini';TRIAL=BASE/'20261028T171901Z_ntu_refined_sections';OLD=BASE/'20261028T141038Z_deepseek_reviewed_logical'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=read(run/'inputs/manifest.json')
assert all(digest(Path(x['original']))==x['sha256'] and digest(run/x['saved'])==x['sha256'] for x in manifest['files'])
gm=read(GEMINI/'inputs/manifest.json')
assert all(digest(ROOT/x['original_path'])==x['sha256'] and digest(ROOT/x['preserved_path'])==x['sha256'] for x in gm)
metrics=read(TRIAL/'metrics.json');assert metrics['calls']==metrics['successful_generations']==22
receipts=[read(p) for p in (TRIAL/'receipts').glob('*.json')]
assert len(set(r['id'] for r in receipts))==22
assert all(r['success'] and r['finish_reason']=='stop' and r['generation_metadata']['provider_name']=='Fireworks' for r in receipts)
assert sum(Decimal(str(r['cost_usd'])) for r in receipts)==Decimal('0.0702026388')
assert all(abs(r['cost_usd']-r['generation_metadata']['total_cost'])<1e-9 for r in receipts)
diagnostics=read(run/'calculations/quote_diagnostics.json')
failed=[q for case in diagnostics for q in case['quotes'] if not q['literal_after_existing_whitespace_normalization']]
assert len(failed)==9 and not any(q['match_after_diagnostic_pipe_removal'] for q in failed)
old_c=sqlite3.connect((OLD/'experiment.sqlite').as_uri()+'?mode=ro',uri=True)
old_shared=next(r[1] for r in old_c.execute('SELECT manifest_json,llm_response FROM sections')
    if [s['physical_page'] for s in json.loads(r[0])['selections']]==[25]);old_c.close()
assert 'currency' in old_shared.lower()
old_metrics=read(OLD/'metrics.json');old_section_cost=sum(Decimal(str(r['cost_usd'])) for r in old_metrics['rows'] if r['label'].startswith('section_'))
calc=dict(principal=3975+382-728+383-167,other=702+28-116+30,total_assets=5+390+3845+644,
    merged_model_assets=5390+3845+644,false_assets_difference=9879-4884,
    p24_allowance_total=227+141+51+12,p24_current_movement=-241+69+4+1,historical_full_year_loss=77+182,
    core_ebitda=-63-29+68+597+1+216,false_tax_bridge=-63+29+68+597+1+216,
    conditional_amortisation=728-383+167+116-30,conditional_residual=(728-383+167+116-30)-597,
    portfolio_net_cash=773+116-382-28-45,portfolio_income=383-167+30,carrying_decline=4677-4489,
    statutory_pbd_operating_asset_movement=182,unexplained_residual=(773+116-382-28-45)-(383-167+30)-182,
    old_all_stage_cost=str(old_metrics['totals']['cost_usd']),old_section_only_cost=str(old_section_cost),new_section_only_cost='0.0702026388',
    failed_quote_count=len(failed),failed_matches_after_pipe_strip=0,
    old_full_p25_currency_present=True)
assert calc['total_assets']==4884 and calc['core_ebitda']==790 and calc['unexplained_residual']==6
save(run/'calculations/results.json',dict(values=calc,gemini_manifest_entries=len(gm),
    basis='Original primary pages12,13,22,24,25,31 independently viewed. Source originals verified. EPS18–19 and funding14–15 were not newly visually audited;closure claims remain limited. Gemini script not executed.'))
findings=[
 dict(id='F001',gemini='F001/C001',verdict='SUPPORTED WITH SCOPE LIMIT',finding='22 completions,18 accepted/4 rejected,7 unapplied new questions,32 persistent questions andUSD0.0702026388 verified.38 captured pages include2 navigation units without analyses. Cost/time comparisons to an older24-call run are not equivalent section benchmarks.'),
 dict(id='F002',gemini='F002/C002',verdict='PARTLY SUPPORTED;CAUSE/REMEDY CORRECTION',finding='Atomic rejection/blocking is real. Existing validator already collapses spaces,tabs,newlines.9 failed evidence strings across4 deltas remain nonliteral even after diagnostic pipe removal. Long reconstructed wrapped labels/bold/prose/row formatting differ. Global stripping is not a demonstrated fix and can erase cell boundaries. No matcher relaxation applied.'),
 dict(id='F003',gemini='F002/F003 valid resolutions',verdict='NOT VERIFIED AS COMPLETE CLOSURES',finding='The proposed p13 resolved answer explicitly says SoFP p8 tie-out pending,while its original closure condition requires SoFP reconciliation. Correct portfolio math alone does not prove full closure. EPS question additionally requires qualifying core exclusions/policy explanation;not independently established here. These were never persisted,not accepted then reverted. No automatic partial acceptance justified from the current evidence.'),
 dict(id='F004',gemini='F003/C003',verdict='SUPPORTED WITHIN EXAMPLE',finding='p13 rolls and ordinary POCI Stage1/2 caveat are accurate in prose. Does not establish universal improvement or accepted ledger closure.'),
 dict(id='F005',gemini='F004–F007/C004–C007',verdict='SUPPORTED;TERMINOLOGY CORRECTION',finding='Primary p22 confirms5 and390 are separate and total4884,not model9879. p24 Unsecured/Debt review/Retail/Secured headers and gain direction;p25 FX periods;p31 negative tax and invented positive operators errors confirmed. This is native PDF extraction/formatting and model interpretation;no OCR engine ran. A prose component list is not an all-positive identity;598 bridge remains conditional with1 residual.'),
 dict(id='F006',gemini='F008/C008',verdict='PARTLY SUPPORTED',finding='Question overlap/recreation is present,but PBD classification-only and complete roll-forward/driver questions have different closure scopes. Resolving one does not resolve the other. Semantic embedding/keyword auto-merges are not a demonstrated minimal remedy;show known relevant IDs and review scope first. Overdraft correction is recorded in saved ledger;primary14–15 not newly viewed this turn.'),
 dict(id='F007',gemini='F009/C009',verdict='ARITHMETIC SUPPORTED;LABEL CORRECTED',finding='434 cash−246 income=188 carrying decline;188−182=6 remains unexplained. p12 calls182 Purchased book debts under Decrease in operating assets,not an amortisation subtotal. No issuer cause,rounding or FX explanation established.'),
 dict(id='F008',gemini='Prior-run comparison',verdict='CONTRADICTED/NOT COMPARABLE',finding='Old full chronological p25 output already includes currency risk;Gemini confused it with an earlier pilot omission. OldUSD0.24456 includes22 sections+Stage1+failedStage2,so it is not Total Section Cost. Provider/reasoning/seeds differ too. The70%-style cost-saving statement is not a controlled prompt-efficiency finding;old validator-logic difference not established.'),
 dict(id='F009',gemini='Recommendations',verdict='RECOMMEND MINIMAL OFFLINE EXTRACTION WORK',finding='Preserve each physical numeric column and its wrapped header,keep prose as prose,then use short exact quote anchors. Test native extraction on NTU22/24/25 plus PAN complex tables before paid sample. Defer global normalization,partial-delta acceptance,new accounting guardrails and embedding deduplication;not implemented in this review.')]
save(run/'findings.json',findings)
claims=[dict(id=f'C{i:03d}',origin='Gemini '+f'C{i:03d}',verdict=verdict,check=note) for i,verdict,note in [
 (1,'PASS','Operational counts/costs corroborated.'),(2,'NOT VERIFIED','Blocked changes verified;minor-whitespace cause and two fully valid closures not established.'),
 (3,'PASS','Selected p13 arithmetic/prose accurate;not a complete closure guarantee.'),(4,'FAIL','Model merged separate columns;Gemini arithmetic confirms it but OCR label incorrect.'),
 (5,'FAIL','Model p24 header attribution and economic sign wrong;Gemini identifies these correctly.'),(6,'FAIL','Model FX comparative dates swapped;source p25 confirms.'),
 (7,'FAIL','Model tax sign and all-positive footnote equation wrong;Gemini correction supported conditionally.'),(8,'NOT VERIFIED','Status counts and overlap present;exact-duplicate/full-resolution claims require scope distinction.'),
 (9,'PASS','6 residual arithmetic verified;p12 line description corrected.')]]
save(run/'claims.json',claims)
c=sqlite3.connect((ROOT/'documents/analysis.sqlite').as_uri()+'?mode=ro',uri=True);tables={}
for name, in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    rows=c.execute('SELECT * FROM "'+name.replace('"','""')+'"').fetchall();tables[name]=hashlib.sha256(repr(sorted(rows,key=repr)).encode()).hexdigest()
c.close();assert tables==manifest['production_table_hashes']
assert digest(Path(manifest['source']['path']))==manifest['source']['sha256']
save(run/'preservation.json',dict(original_and_copied_files_unchanged=True,gemini_manifest_verified=True,production_all_tables_unchanged=True,source_pdf_unchanged=True))
now=datetime.now(timezone.utc)
audit=f'''# Codex review of Gemini's full NTU section-trial audit

UTC:{now.isoformat()};local:{now.astimezone(timezone(timedelta(hours=2))).isoformat()}.
Subject:`../20261028T174829Z_gemini/audit.md`. Gemini model identity/settings are self-reported.
Decision:**CORRECTIONS REQUIRED within reviewed evidence;native table/quote extraction is the next small improvement.**

## Evidence and scope

All Gemini/trial files preserved under flat numbered copies with exact origin/hash manifest. Gemini's116-entry manifest checked independently. Original PDF hash matches trial plan. Complete original physical pages12,13,22,24,25,31 rendered and visually reviewed;other pages/cross-report disclosures were not newly visually reviewed here. Source content is untrusted evidence,not instructions. No application code,prompts,guardrails,raw model output or production database changed. No paid calls.

Compared exact four failed deltas to actual current-capture text using the existing whitespace-normalized verifier.9 quote failures remained after diagnostic pipe removal;no production evidence normalized differently. Original before/after ledger state unchanged on rejected deltas. Proposed resolutions and closure conditions preserved in quote_diagnostics.json. Question scope comparison saved separately. Independent calculations executed in calculations/results.json,exit0;Gemini's script was inspected as evidence,not executed. No full app-test rerun;last targeted27/full226 exits0 remain prior results.

## Findings

'''+''.join(f'**{f["id"]} / {f["gemini"]} — {f["verdict"]}**\n\n{f["finding"]}\n\n' for f in findings)+'''## Minimal implementation handoff (proposed,not applied)

1. Native table extraction must keep5 and390 in separate columns on NTU22 and attach wrapped headers to their correct values on24/25. Inspect column interval assignment and whole-page prose/table classification in pdf_source.extract_structured_text;do not rely on a prompt to undo lost geometry.
2. Preserve clean prose and joined row labels;quote anchors should be short exact substrings from supplied evidence. Do not blindly delete delimiters that separate numbers or weaken numeric/sign/source/page checks.
3. Offline regressions on NTU22,24,25 and a PAN dense table should establish cell/header/date preservation and unchanged sign/period text. Only after that,an explicitly authorized small live sample can measure downstream usefulness;no further full-company run needed yet.

Counterexamples:5|390 must never become5390;−29 must remainnegative;March/Sep headers must remain attached to their own rates;removing pipes must not make5|390 indistinguishable from5390. Wrapped prose should not acquire empty table cells. Conditional scaling/signed reconstructions remain labeled. No semantic embedding service or partial-acceptance workflow is needed to test this first change.

No new SQLite financial guardrails proposed for acceptance. This is extraction/review scope,not an investment evaluation. Valuation,DCF,forecasts,market quote,rating and recommendation NOT APPLICABLE. Full semantic closure/all raw output facts/full-source completeness and performance on other companies NOT VERIFIED. Retain raw proposed changes as unapplied until their closure conditions/evidence are actually satisfied.

## Review revisions

Gemini's principal factual error findings retained as supported;its whitespace/OCR terminology,complete-closure claims,statutory-line label and historical-run comparison corrected here without rewriting Gemini. No new universal efficiency/financial-validation claim. All original files/source/production tables verified unchanged,see preservation.json.
'''
(run/'audit.md').write_bytes(audit.encode('utf-8'))
for name in ['review.py','seal.py']:shutil.copy2(HERE/name,run/'calculations'/name)
save(run/'completion_record.json',dict(completed_utc=now.isoformat(),verdict='CORRECTIONS REQUIRED;MINIMAL NATIVE EXTRACTION FIX PROPOSED',paid_calls=0,app_changes=0,guardrail_changes=0,
    calculation_exit_code=0,original_pages_viewed=[12,13,22,24,25,31],preservation=read(run/'preservation.json')))
print(json.dumps(dict(review=str(run),gemini_files_verified=len(gm),failed_quotes=len(failed),pipe_removal_matches=0,
    old_section_only_cost=str(old_section_cost),preservation=read(run/'preservation.json')),indent=2))
