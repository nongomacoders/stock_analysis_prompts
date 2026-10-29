"""Metadata refresh, offline checks and versioned manual Gemini handoff."""
import importlib.util
import json
from pathlib import Path
import shutil
import sqlite3
import sys

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('fireworks_trial',HERE/'stage2_fireworks.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
m=t.m;ROOT=t.ROOT
run=Path(t.POINTER.read_text(encoding='utf-8').strip())
r=m.read(run/'receipts/stage2.json')
assert r.get('completed_utc'), 'Still active; do not review'
assert m.read(run/'requests/stage2.json')==dict(m.read(t.PREVIOUS/'requests/stage2.json'),provider=t.PROVIDER)
assert m.read(run/'metrics.json')['calls']==1
if r.get('id'):
    from section_capture.openrouter import get_openrouter_api_key
    refreshed=dict(r)
    m.metadata(run,'stage2',refreshed,get_openrouter_api_key())
    m.save(run/'outputs/generation_metadata_refresh.json',dict(checked_utc=m.utc(),metadata_status=refreshed.get('metadata_status'),generation_metadata=refreshed.get('generation_metadata')))
    g=refreshed.get('generation_metadata') or r.get('generation_metadata') or {}
else:g={}
def offline(event,args):
    if event in {'socket.connect','socket.getaddrinfo','socket.sendto'}:raise RuntimeError('Offline checks: no network')
sys.addaudithook(offline)
u=r.get('usage') or {}
provider=g.get('provider_name',r.get('provider'))
if provider:assert 'fireworks' in provider.lower(), 'Unexpected provider'
row=dict(provider=provider,model=g.get('model',r.get('model')),generation_id=r.get('id'),
    success=r['success'],finish_reason=r.get('finish_reason',g.get('finish_reason')),
    native_finish_reason=g.get('native_finish_reason'),elapsed_seconds=r['elapsed_seconds'],
    time_to_first_content_seconds=r.get('time_to_first_content_seconds'),
    prompt_tokens=u.get('prompt_tokens',g.get('native_tokens_prompt')),
    completion_tokens=u.get('completion_tokens',g.get('native_tokens_completion')),
    reasoning_tokens=(u.get('completion_tokens_details') or {}).get('reasoning_tokens',g.get('native_tokens_reasoning')),
    cost_usd=g.get('total_cost',r.get('cost_usd')),original_receipt_cost_usd=r.get('cost_usd'),api_error=r.get('api_error'))
row['nonreasoning_tokens']=(row['completion_tokens']-row['reasoning_tokens']) if row['completion_tokens'] is not None and row['reasoning_tokens'] is not None else None
c=m.ro(ROOT/'documents/analysis.sqlite');dest=sqlite3.connect(run/'inputs/evaluator_snapshot.sqlite')
c.backup(dest);c.close();dest.close()
from evaluate_stock import StockEvaluator
e=StockEvaluator('NTU',period='1H26',db_path=run/'inputs/evaluator_snapshot.sqlite')
e.fetch_market_quote=lambda:dict(price_zar=None,source='No current quote requested; frozen comparison reference only')
note=run/'outputs/stage2.md'
result=e.audit(note_path=note)
m.save(run/'outputs/preliminary_evaluator.json',dict(result=result,network_disabled=True,scope='Preliminary script checks only; no financial validation'))
arithmetic=dict(principal_close=3975+382-728+383-167,other_close=702+28-116+30,
    portfolio_net_cash=728+116-382-28,portfolio_income=383-167+30,carrying_decline=4677-4489,
    statutory_cash_movement=182,residual=(728+116-382-28)-(383-167+30)-182)
assert arithmetic['residual']==6
m.save(run/'outputs/independent_calculations.json',dict(values=arithmetic,basis='Re-executed source inputs previously verified against identical-hash primary PDF pp12–13; no new PDF image inspection. Forecast/DCF not verified.'))
if note.exists():
    shutil.copy2(note,run/'inputs/stage2_review_subject.md')
    m.save(run/'inputs/output_manifest.json',dict(path=str(note),sha256=m.sha(note)))
    answer=note.read_text(encoding='utf-8')
    m.save(run/'outputs/limited_text_flags.json',dict(
        mentions_370='370' in answer,mentions_withheld='WITHHELD' in answer,
        scope='Text-presence flags are not financial or attribution checks; inspect original answer.'))
    print('Answer preserved; chars',len(answer))
assessment=m.read(run/'outputs/publication_assessment.json') if (run/'outputs/publication_assessment.json').exists() else {'valuation_status':'NOT_PUBLISHED_PROCESS_INCOMPLETE'}
comparison=dict(only_request_change='provider.only=fireworks;allow_fallbacks=false;require_parameters=true',
    reasoning='omitted controls; provider defaults may differ',max_tokens=300000,
    previous=m.read(t.PREVIOUS/'metrics.json')['rows'][0],current=row,
    publication_assessment=assessment,independent_financial_verdict='INSUFFICIENT EVIDENCE; forecasts/valuation not independently verified')
m.save(run/'comparison.json',comparison)
m.preserve(run)
shutil.copy2(Path(__file__),run/'inputs/review_driver.py')
summary=('# NTU1H26 — Fireworks-only Stage2 test\n\n'
    'One authorized attempt. Exact Relace300k request retained except provider selection; Fireworks only, fallback disabled, supported parameters required. Default reasoning controls omitted,300000 combined reasoning/final-answer token ceiling. Actual provider and all measured results below. No original outputs,source PDF,production data or app defaults changed. No paid retry.\n\n'
    '```json\n'+json.dumps(row,indent=2)+'\n```\n\n'
    'Publication assessment: '+assessment['valuation_status']+'. Script status is not financial validation. No output promoted to production. Known inherited Stage1 R370m discrepancy is unsupported; re-executed historical bridge leavesR6m unexplained. Exact input unchanged for provider comparison. Forecast/DCF/financing/current market checks NOT VERIFIED. No new financial guardrails.\n\n'
    'Preservation and isolated preliminary evaluator checks passed,offline review exit0. No full pytest rerun: application code unchanged. Versioned audit:audit.md; exact comparison:comparison.json; manual Gemini handoff:gemini/PROMPT.md.\n')
m.text(run/'RUN_SUMMARY.md',summary)
m.text(run/'gemini/PROMPT.md',f'''Review NTU1H26 DeepSeek Stage2 Fireworks experiment in Antigravity. Read AGENTS.md,workflow/WORKFLOW.md and docs/STOCK_EVALUATION_FORMAT.md section1A. Save a new timestamped Gemini audit with exact inputs/hashes,primary-evidence coverage,executed independent calculations,findings and limitations. Codex will review Gemini afterward. No paid model calls or production/guardrail writes.
Run:{run}
Start RUN_SUMMARY.md,comparison.json,receipts/stage2.json,requests/stage2.json,outputs/stage2.md if present,publication_assessment.json and audit.md. Original messages/Stage1 unchanged from reviewed-logical run and Relace300k; only Fireworks provider selection changed. Completion is not accuracy. Missing Stage2 is NOT VERIFIED,not PASS. No current quote supplied.
Known Stage1 regression: allegedR370m portfolio cash difference is unsupported. Previously verified primary pp12–13:434 net cash−246 accounting income=188 carrying decline; statutory182 leaves6 unexplained. Independently check this and whether Stage2 repeats/corrects it; don't infer causation of provider failures. Verify original PDF/source hash in plan.json. Review all forecast/cash/debt/valuation schedules if supplied; source text availability does not mean every PDF page was independently inspected. Check target/readiness/material blockers; no unsupported replacement target. Distinguish provider completeness,cost,time and financial accuracy. No automatic guardrail codification.
Prior source review:{t.OLD.parent/'20261028T145027Z_codex_logical_trial_review/audit.md'}
''')
with (run/'audit.md').open('a',encoding='utf-8',newline='') as f:
    f.write('\nOffline review: request differs solely by explicit provider object;one generation;actual provider checked if returned;source/production/original files preserved. Preliminary StockEvaluator on explicit experimental path and copied DB with network denied. Historical arithmetic re-executed:434−246=188,minus statutory182=6 unexplained. New forecast/valuation dependencies NOT VERIFIED. Manual Gemini prompt saved;no Gemini API. Final measured results:\n```json\n'+json.dumps(row,indent=2)+'\n```\n')
state=ROOT/'workflow/STATE.md';body=state.read_text(encoding='utf-8');marker='## Completed\n';assert body.count(marker)==1
entry=f'''\n- **NTU Fireworks-only Stage2 experiment (2026-10-28)**:
  - User requested Fireworks. Exact Relace300k input retained;only provider object changed,Fireworks only/no fallback/require supported parameters. One attempt,default thinking,300000 cap. Run:`{run.relative_to(ROOT).as_posix()}`.
  - Provider:{provider};generation complete:{r['success']};finish:{row['finish_reason']};elapsed:{row['elapsed_seconds']}s;reported costUSD:{row['cost_usd']};input:{row['prompt_tokens']};completion:{row['completion_tokens']};reasoning subset:{row['reasoning_tokens']}. API error:{row['api_error']}. Publication assessment:{assessment['valuation_status']};not independent financial validation.
  - Preserved exact original request/Stage1/Relace receipt/source hashes,recorded costs/tokens/timing/provider,versioned audit and manual Gemini prompt. Preliminary evaluator on copied DB/explicit new path;offline checks exit0. All production tables/source/originals unchanged. Known inherited Stage1 R370m error retained for comparison;historical bridge leaves6 unexplained. No new app defaults,financial guardrails,Gemini API calls or automatic paid retry. Full pytest not rerun for isolated live test.
\n'''
m.text(run/'outputs/state_update_candidate.md',body.replace(marker,marker+entry,1))
m.save(run/'closure_checks.json',dict(checked_utc=m.utc(),request_only_provider_changed=True,one_generation=True,
    offline_review_exit_code=0,dispatch_tool_exit_code=int(sys.argv[1]) if len(sys.argv)>1 else None,
    preservation=m.read(run/'preservation.json'),financial_validation='NOT VERIFIED',retry_submitted=False))
print(json.dumps(dict(run=str(run),result=row,publication=assessment,preliminary=result,preservation=m.read(run/'preservation.json')),indent=2))
