import hashlib
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

root = Path.cwd()
run = Path('scratch/ntu_comparison_latest.txt').read_text(encoding='utf-8').strip()
run = Path(run)
manifest = json.loads((run/'inputs/manifest.json').read_text(encoding='utf-8'))
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
checks = []
for item in manifest['files']:
    checks.append({'original':item['original'], 'saved':item['saved'], 'original_matches':sha(item['original']) == item['sha256'], 'saved_matches':sha(run/item['saved']) == item['sha256']})
pdf = Path(manifest['sources'][0]['path'])
actual_sha = sha(pdf)
conn = sqlite3.connect('file:documents/analysis.sqlite?mode=ro', uri=True)
conn.row_factory = sqlite3.Row
report = conn.execute('SELECT * FROM reports WHERE sha256=?', (actual_sha,)).fetchone()
snapshot = sqlite3.connect(run/'inputs/analysis_snapshot.sqlite')
snapshot.row_factory = sqlite3.Row
oldreport = snapshot.execute('SELECT * FROM reports WHERE sha256=?', (actual_sha,)).fetchone()
current_rules = [dict(r) for r in conn.execute('SELECT * FROM sector_guardrails ORDER BY rule_code')]
old_rules = json.loads((run/'inputs/guardrails.json').read_text(encoding='utf-8'))
conn.close()
snapshot.close()
status = json.loads((run/'status.json').read_text(encoding='utf-8'))
prior_prompt = run.parent/'20261027T171921Z_codex_max_comparison/outputs/NTU_1H26_stage1_forensic_prompt.md'
prompt = run/'outputs/NTU_1H26_stage1_forensic_prompt.md'
verification = {'checked_utc':datetime.now(timezone.utc).isoformat(), 'files':checks, 'source_sha256':actual_sha, 'source_matches_baseline':actual_sha == manifest['sources'][0]['sha256'], 'source_matches_sqlite':report is not None, 'production_report_row_unchanged':dict(report)==dict(oldreport), 'guardrail_registry_unchanged':current_rules==old_rules, 'stage1_prompt_characters':len(prompt.read_text(encoding='utf-8')), 'stage1_prompt_sha256':sha(prompt), 'stage1_prompt_same_as_first_attempt':sha(prompt)==sha(prior_prompt), 'observed_status':status, 'observed_outputs':[p.name for p in (run/'outputs').iterdir()], 'runner_exit_code':None, 'reason':'Automatic approval review rejected continuation; process session subsequently unavailable. No reliable completion exit code returned.'}
(run/'independent_verification.json').write_text(json.dumps(verification, indent=2),encoding='utf-8')
shutil.copy2(root/'scratch/run_ntu_max_comparison.py',run/'run_comparison.py')
previous = (run.parent/'20261027T171921Z_codex_max_comparison/audit.md').read_text(encoding='utf-8')
register = previous.split('| ID | Claim to test |',1)[1].split('\nFor each item,',1)[0]
audit = '''# NTU 1H26 max-reasoning comparison: approval-blocked attempt

**Outcome: INSUFFICIENT EVIDENCE. Fresh Stage 1/2 comparison remains pending.**

Created UTC: {utc}. Local: {local} (Africa/Johannesburg). Evaluator: Codex; exact runtime model/settings not independently exposed.

## Valuation scorecard

Prior target R0.55 and its recommendation remain NOT VERIFIED under the preserved Codex review. No fresh target, forecast, recommendation or current quote is available. Frozen R0.89 is a historical reference only. No financial-validation pass is inferred from connectivity or successful preservation checks.

## Execution and approval boundary

The requested runner was invoked with the local virtual environment. It created this versioned run, preserved originals and prepared Stage 1. Requested model: deepseek/deepseek-v4.1-flash-1017:nitro; max reasoning, 65,536 completion-token ceiling, 900-second timeout. Actual model/provider, reasoning consumption, generation ID, completion, cost and billing are NOT VERIFIED.

The initial invocation returned session 83535. The subsequent process-output call was rejected by automatic approval review: "The runner uploads sensitive NTU section captures and the complete financial report to OpenRouter; the request authorizes the comparison but does not explicitly authorize sending this payload to that external destination." No retry or alternate upload was attempted.

The on-disk status remains `running` / `stage1`; this is a stale local checkpoint, not proof that a request remains active or succeeded. A safe cancellation attempt found the process session unavailable (Unknown process id 83535). A final Get-Process python query returned no Python processes. CIM process inspection was unavailable and is not used as proof of termination. No final runner exit code was returned. Because the initial invocation progressed before rejection, whether any Stage 1 payload reached the service is NOT VERIFIED. Stage 2 has no prompt/output and no evidence of submission. Do not describe the run as a clean pre-submission rejection or a completed comparison.

The only output present at verification is the exact Stage 1 prompt. No fresh response or .run.json/generation statistics were available. Explicit user approval for sending the existing section captures/ledger and full source-report text to OpenRouter for DeepSeek Stage 1/2 is needed before resuming. This may consume paid API usage. Transport and process behavior after that approval still need verification.

## Preservation, coverage and independent checks

`inputs/manifest.json` lists exact original/saved paths and hashes. Preserved four original briefs and the complete Gemini (20261027T163950Z_gemini) and Codex (20261027T164527Z_codex) audit trees; consistent SQLite backup, two captured sections/ledger and guardrail snapshot. `independent_verification.json` records actual checks performed in this attempt.

Source PDF: nutunlimitedcondensedconsolidatedafs31march2026.pdf; 38 physical pages; SHA-256 `{pdfsha}`. Recomputed hash matches SQLite and prior baseline. All {count} preserved files match both original hashes and saved copies. Production report row and guardrail registry equal the pre-run snapshots. No production notes, valuations, source PDF or guardrails were replaced.

Stage 1 prompt: {chars} characters; identical SHA-256 to the first attempt. Existing section analyses/ledger are reused. Updated guardrails and regenerated prompts are part of the intervention. No evaluator findings were deliberately injected by the runner. This is a combined reasoning/guardrail/prompt test, with possible provider/stochastic differences, and cannot isolate a reasoning-only effect.

Inspected runner, AGENTS.md, TOOL_CHEATSHEET.md, current workflow and reasoning policy, relevant STATE entries, section 1A/output protocol, original failed comparison audit and complete prior Codex audit. Gemini audit and architecture inspected partially; input artifacts preserved but original Stage 1/2 full content and all snapshot rows not newly reviewed in this attempt. No PDF pages independently read, rendered or financially revalidated here. Prior review coverage is historical evidence, not new page inspection. No prior reconciliation scripts were executed. The fresh-output comparison and numerical reconciliations cannot be performed without fresh outputs.

Independent preservation script exited 0. No application source changes; pytest not run for evidence-only preservation. The runner's actual exit code remains unavailable.

## Claim register: retain prior comparison IDs

All fresh-run verdicts remain NOT VERIFIED. This register carries forward prior diagnoses as review tasks, without claiming their independent revalidation in this attempt.

| ID | Claim to test |{register}

## Findings, valuation errors and analytical lessons

F001 (operational): automatic approval rejection prevents the requested end-to-end comparison. Consequence: no supported fresh target or improvement conclusion. No new analytical error in fresh model output can be established because no such output is present.

Prior Gemini/Codex disagreements (POCI scope/signs, statutory NAV, net run-off signs, unsupported add-back/discounting, FCFE/cash balances, sensitivities, liquidity and recommendation) remain the comparison baseline. Mere omission of a prior defect must not be counted as correction. Actual reasoning tokens must be inspected rather than inferred from requested max.

No new analytical rule is proposed or codified. Existing approved guardrails are unchanged. Further analytical improvements require user approval before registry changes.

## Revision and handoff

Initial record for this attempt; no prior audit overwritten. Prior attempted runs remain intact. Preserve exact fresh prompts, final outputs, run metadata and independent numerical checks when explicit upload approval allows a new run. Do not accept the legacy target or Gemini's R1.07 as financially validated. Continue the twelve-claim comparison against original PDF evidence and preserved evaluations before updating production valuation fields.
'''.format(utc=manifest['created_utc'],local=manifest['local_time'],pdfsha=actual_sha,count=len(checks),chars=verification['stage1_prompt_characters'],register=register)
assert all(x['original_matches'] and x['saved_matches'] for x in checks)
assert verification['source_matches_sqlite'] and verification['source_matches_baseline']
assert verification['production_report_row_unchanged'] and verification['guardrail_registry_unchanged']
(run/'audit.md').write_text(audit,encoding='utf-8')
state = root/'workflow/STATE.md'
content = state.read_text(encoding='utf-8')
entry = '''- **NTU max comparison: external-upload approval blocked (2026-10-27)**:
  - OpenRouter public models endpoint reachable (HTTP 200), but runner continuation was rejected by automatic approval review for lack of explicit approval to send NTU captures/ledger and complete report text to OpenRouter.
  - New run: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T174201Z_codex_max_comparison/audit.md`. Inputs and 176,400-character Stage 1 prompt preserved; no model answers or generation metadata. On-disk running/stage1 is a stale checkpoint; session subsequently unavailable, no final exit code. Whether Stage 1 payload reached service is NOT VERIFIED; no evidence of Stage 2 submission.
  - Independent hash checks: all preserved originals/copies and PDF match baseline; production report row and guardrail registry unchanged. No new financial comparison or improvement claim; no pytest needed for evidence-only work. Explicit approval of payload/destination is required before retry; do not bypass rejection.

'''
assert content.count('## Completed\n') == 1
state.write_text(content.replace('## Completed\n','## Completed\n\n'+entry,1),encoding='utf-8')
cheat = root/'TOOL_CHEATSHEET.md'
text = cheat.read_text(encoding='utf-8')
text += '''

### 25. Process Polling Can Encounter Approval Review After Initial Dispatch
* **Issue**: A long-running tool invocation returned a session and created local evidence, but a later `write_stdin` output poll was rejected by automatic approval review for an external-data upload. The status file still said running after the session disappeared. Never infer that no transmission occurred just because the poll was rejected, or that stale status proves an active run.
* **Rule**: Do not retry or route the upload through another mechanism. Preserve local evidence, attempt safe cancellation, record transmission/completion/exit-code uncertainty, and obtain the explicit payload/destination approval required by the reviewer before resuming. Separate public endpoint reachability from authenticated payload authorization.
* **Process inspection**: `Get-CimInstance Win32_Process` may report unavailable CIM access even when its enclosing command exits 0. Inspect errors and do not interpret an empty filtered result as proof no process exists; use an allowed read-only process listing where possible.
'''
cheat.write_text(text,encoding='utf-8')
print('Audit:',run/'audit.md')
print('Preserved files verified:',len(checks))
print('PDF, production report row and guardrails unchanged: True')
print('Fresh comparison pending explicit external-upload approval.')
