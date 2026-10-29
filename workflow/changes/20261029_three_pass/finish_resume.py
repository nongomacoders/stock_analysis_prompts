"""Read-only accounting refresh and complete two-company Gemini handoff."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,shutil
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('resume',HERE/'resume_pan.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
m=s.m;run=Path(s.POINTER.read_text(encoding='utf-8').strip());plan=m.read(run/'plan.json');old=Path(plan['previous_run'])
from section_capture.openrouter import get_openrouter_api_key
key=None;raw=run/'receipts_before_refresh';raw.mkdir(exist_ok=True)
for p in sorted((run/'receipts').glob('*.json')):
    r=m.read(p)
    if r.get('metadata_status')=='retrieved':continue
    shutil.copy2(p,raw/p.name)
    if r.get('id'):
        if key is None:key=get_openrouter_api_key()
        m.metadata(run,r['label'],r,key);m.save(p,r)
        print('METADATA',r['label'],r.get('metadata_status'),flush=True)
m.summarize(run);metrics=m.read(run/'metrics.json');metrics['reasoning']='none/exclude=true'
metrics['notes']=[n for n in metrics['notes'] if not n.startswith('Provider/account routing')]+['Fireworks only, none reasoning explicitly requested.','New continuation accounting only; earlier reused passes and original429 tracked separately.']
m.save(run/'metrics.json',metrics)
accepted=m.read(run/'accepted_attempts.json');assert set(accepted)=={'pan_dense_why','pan_dense_single'}
assert metrics['calls']==metrics['successful_generations']==2
events=m.read(run/'attempts.json');assert all(e['attempt']==1 and e['outcome']=='complete' for e in events)
oldmetrics=m.read(old/'metrics.json');previous={r['label']:r for r in oldmetrics['rows']};current={r['label']:r for r in metrics['rows']}
three=[previous['pan_dense_meaning'],previous['pan_dense_movement'],current[accepted['pan_dense_why']]]
single=current[accepted['pan_dense_single']]
def totals(rows):return {k:sum(r[k] for r in rows) for k in ['cost_usd','prompt_tokens','completion_tokens','elapsed_seconds']}
pan=dict(single=totals([single]),three_pass=totals(three),single_ledger_valid=m.read(run/'outputs/pan_dense_single.validation.json')['ledger_valid'],three_pass_ledger_valid=m.read(run/'outputs/pan_dense_why.validation.json')['ledger_valid'],quality_verdict='Pending independent Gemini review; literal validation is not financial validation.')
prior=m.read(old/'comparison.json');known=oldmetrics['totals']['cost_usd']+metrics['totals']['cost_usd']
comparison=dict(ntu=prior['ntu'],pan=pan,incremental=metrics['totals'],incremental_wall_seconds=metrics['observed_first_dispatch_to_last_accounting_seconds'],combined_known_cost_usd=known,original_failed_request_cost='unknown',new_attempts=events,reused=['PAN meaning/movement','NTU complete pair'],limitations='One fresh sample per arm; extra calls/context/budget for three-pass. Continuation uses same exact previously failed PAN final request; single prompt unchanged. Interruption/elapsed time/cache differences prevent causal speed/cost benchmark.')
m.save(run/'combined_comparison.json',comparison)
# Flat copies keep original NTU comparison available in the new evidence pack.
for folder in ['outputs','receipts']:
    for p in (old/folder).glob('ntu_assets*'):
        if p.is_file():shutil.copy2(p,run/'inputs'/f'previous_{folder}_{p.name}')
for name in ['findings.json','claims.json','calculations.json','closure_comparison.json','plan.json']:
    shutil.copy2(old/name,run/'inputs'/f'previous_{name}')
nt=prior['ntu']
report=f'''# Completed single-pass versus three-pass comparison

PAN continuation is complete. Both pending calls succeeded on their first new attempt;
the authorized three-attempt exponential-backoff policy (15s,30s,Retry-After respected)
was configured but no wait/retry was needed. PAN meaning and movement were reused unchanged.

| Case | One-pass cost | Three-pass total cost | One-pass request seconds | Three-pass summed request seconds | Ledger valid: one / three |
|---|---:|---:|---:|---:|---|
| NTU | ${nt['single']['cost_usd']:.6f} | ${nt['three_pass']['cost_usd']:.6f} | {nt['single']['request_seconds']:.3f} | {nt['three_pass']['request_seconds']:.3f} | No / Yes |
| PAN | ${pan['single']['cost_usd']:.6f} | ${pan['three_pass']['cost_usd']:.6f} | {pan['single']['elapsed_seconds']:.3f} | {pan['three_pass']['elapsed_seconds']:.3f} | Yes / Yes |

New PAN requests: USD{metrics['totals']['cost_usd']:.10f},input{metrics['totals']['prompt_tokens']},completion{metrics['totals']['completion_tokens']},reasoning{metrics['totals']['reasoning_tokens']},cached{metrics['totals']['cached_prompt_tokens']}. Continuation dispatch-to-last-accounting{metrics['observed_first_dispatch_to_last_accounting_seconds']:.3f}s. Combined known experiment subtotalUSD{known:.10f}; original429billing remains unavailable, so this is not a verified complete bill.

All eight planned successful outputs are now available across the two runs. There was
also the original failed429request, preserved separately. No successful analysis was
regenerated. No production data or app prompts changed. NTU's prior semantic-closure
concerns remain; PAN financial quality awaits Gemini. Ledger validation checks literal
evidence/structure, not full accounting accuracy. This small, unreplicated comparison
does not establish which workflow is more robust.
'''
m.text(run/'comparison.md',report)
audit=f'''# PAN continuation: operational audit and handoff

Evaluator Codex; recorded UTC{datetime.now(timezone.utc).isoformat()},local timezone Africa/Johannesburg(UTC+02:00).
Decision: **GENERATION COMPLETE; FINANCIAL QUALITY PENDING INDEPENDENT GEMINI REVIEW**.

User authorized PAN redo with exponential backoff,three attempts. Preserved previous failed429,exact request,all successful earlier stages and NTU comparison. Original PAN final request reproduced byte-for-byte as structured payload before dispatch; single prompt unchanged. Per pending call retry at most3attempts for HTTP429/500/502/503/504 before generation ID/content/usage; waits15/30seconds and respectRetry-After. Other/incomplete-generation failures stop. Both calls succeeded first new attempt, so retry behavior was not exercised live.

{report}

Read actual request/receipt/settings,attempt log,canonical outputs and independent in-memory validation records. No full financial-content review or new PDF rendering this continuation: Gemini receives exact source text,earlier intermediate answers,previous findings/calculations and original PDFs by verified path/hash. Original NTU/PAN source evidence remains unchanged; prior source reviews/renders are available in20261028T191648Z_codex_native_extraction_review/source_pages. This operational audit does not adopt/reject PAN's numerical/causal conclusions. Valuation/forecast/current quote NOT APPLICABLE; no target/recommendation.

Source SHA verified before packaging and after completion. Plan originals/copies and all production table contents unchanged(preservation.json). No app/prompt edits,SQL guardrails or Stage1/2, no Gemini API. Successful generation exit0; metadata/handoff exit0. No regression repeat for standalone continuation scripts and no test-created temporary folders. Previous full232/targeted27 offline passes retained. No policy/permission/shell/encoding failure; original transport429quota source unknown.

Claims: C001(PASS) both pending calls complete first new attempt,linked exact receipts/attempts;C002(PASS) both final PAN deltas validate in isolated memory;C003(NOT VERIFIED) financial correctness and workflow superiority,pending Gemini;C004(NOT VERIFIED) original failed-request billing. Further financial findings should be recorded by Gemini against original source,not inferred from call/validator success.
'''
m.text(run/'audit.md',audit)
prompt=f'''Review the completed small one-pass versus three-pass experiment in Antigravity. Read AGENTS.md,workflow/STATE.md,workflow/WORKFLOW.md and docs/STOCK_EVALUATION_FORMAT.md section1A. Save a new versioned Gemini audit,claim/findings registers,independent calculations,input hashes and actual inspected/unread coverage. No paid model calls,code/prompt edits,production SQLite writes or rewriting raw outputs.

NEW COMPLETED PAN CONTINUATION:
{run}
ORIGINAL EXPERIMENT (complete NTU pair and original PAN meaning/movement):
{old}

Read new comparison.md,combined_comparison.json,audit.md,plan.json,preservation.json,metrics,attempts,accepted_attempts,requests/receipts,inputs and canonical outputs/pan_dense_why.md plus pan_dense_single.md with validation records. Inputs include unchanged reused PAN meaning/movement,original failed request,previous NTU outputs/receipts and prior findings/calculations/closure records. Original run has full frozen inputs and source context. Do not count canonical response copies or metadata refreshes as extra generations. Both new requests succeeded first new attempt; configured backoff did not run. Original429cost/usage unknown.

Compare complete fresh NTU single vs meaning/movement/why and complete PAN single vs reused meaning/movement plus new finalwhy. Identical report captures,incoming questions,model/provider/reasoning/settings; three-pass has more calls/context/total token budget,not isolated causal proof. One sample per arm,not replicated/randomized. Separate arithmetic/sign/measurement accuracy,percentage usefulness,source scope and ambiguity,explanations/hypotheses,question quality,semantic closure,literal validation,time and cost.

Inspect original PDFs from plan.json with SHA verification: physical NTU21–23,PAN48–50. Prior source renders/review: companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T191648Z_codex_native_extraction_review/source_pages. Trace any wrong dictionary meaning through later passes; check original closure ofQ-08aa5c3f257440ab rather than accepting status labels. Critique previous Codex assessments too. PAN points to verify: disjoint FY25production196527vs overlap197608; MTR25043vs30806 source conflict; FY26Barberton94929vs71997+12932=84929,total-operation sum282310vs272310; retain1oz differences. Check capex/cash/profit definitions,APM scope and unproved typo/causal claims. Do not assume these numerical prompts establish which source figure to replace.

Conclude whether three passes improve robustness,only clarity,or neither within coverage. Identify remaining errors and smallest useful next experiment/change; do not implement or rerun it. No valuation requested. Preserve successful outputs and exact evidence for Codex's later review.
'''
m.text(run/'gemini/review_prompt.md',prompt)
# This user-facing pointer intentionally supersedes the old incomplete handoff.
m.text(HERE/'gemini_prompt.md',prompt)
m.save(run/'input_manifest.json',[dict(path=str(p),sha256=m.sha(p)) for d in ['inputs','outputs','requests','receipts','receipts_before_refresh'] for p in (run/d).glob('*') if p.is_file()])
m.preserve(run);status=m.read(run/'status.json');status.update(status='complete_gemini_pack_ready',reviewed_utc=m.utc());m.save(run/'status.json',status)
m.save(run/'execution.json',dict(generation_exit_code=0,handoff_exit_code=0,new_calls=2,backoff_exercised=False))
print(json.dumps(dict(new_cost=metrics['totals']['cost_usd'],wall_seconds=metrics['observed_first_dispatch_to_last_accounting_seconds'],combined_known_cost=known,pan_ledger_valid=[pan['single_ledger_valid'],pan['three_pass_ledger_valid']]),ensure_ascii=False))
