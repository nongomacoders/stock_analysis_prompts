import sys, json, hashlib
from pathlib import Path
from datetime import datetime, timezone, timedelta
sys.stdout.reconfigure(encoding='utf-8')
root=Path.cwd()
base=root/'companies/consumer_lending/NTU/briefs/1H26/evaluations'
old=base/'20261027T171921Z_codex_max_comparison'
run=base/'20261027T172440Z_codex_max_comparison'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((run/'inputs/manifest.json').read_text('utf-8'))
checks=[]
for item in manifest['files']:
    checks.append({'original':item['original'],'saved':item['saved'],'expected_sha256':item['sha256'],'original_matches':digest(Path(item['original']))==item['sha256'],'snapshot_matches':digest(run/item['saved'])==item['sha256']})
prompt='outputs/NTU_1H26_stage1_forensic_prompt.md'
check={'checked_utc':datetime.now(timezone.utc).isoformat(),'baseline_files':checks,'all_originals_and_snapshots_match':all(c['original_matches'] and c['snapshot_matches'] for c in checks),'stage1_prompt_sha256':digest(run/prompt),'prior_attempt_stage1_prompt_sha256':digest(old/prompt),'prompt_identical_to_prior_attempt':digest(run/prompt)==digest(old/prompt),'sources':[{'path':s['path'],'expected_sha256':s['sha256'],'current_sha256':digest(Path(s['path'])),'matches':digest(Path(s['path']))==s['sha256']} for s in manifest['sources']],'runner_exit_code':1,'fresh_stage1_output_exists':(run/'outputs/NTU_1H26_stage1_response.md').exists(),'fresh_stage2_output_exists':(run/'outputs/NTU_1H26_stage2_response.md').exists()}
(run/'integrity_checks.json').write_text(json.dumps(check,indent=2),encoding='utf-8')
(run/'execution_log.txt').write_text('Command: .venv/Scripts/python.exe -u scratch/run_ntu_max_comparison.py\nPDF hash verified. Captured sections: 2 Stage 1 prompt characters: 176400\nSubmitting stage1 model deepseek/deepseek-v4.1-flash-1017:nitro with max reasoning\nRUN FAILED: RuntimeError OpenRouter connection error (deepseek/deepseek-v4.1-flash-1017): <urlopen error [Errno 11001] getaddrinfo failed>\nActual process exit code: 1\n',encoding='utf-8')
# Retain stable comparison claims from the prior attempt, explicitly attributed rather than revalidated.
prior=(old/'audit.md').read_text('utf-8')
claims=prior.split('## Claim register and comparison checklist',1)[1].split('## Valuation errors and analytical lessons',1)[0]
now=datetime.now(timezone(timedelta(hours=2))).isoformat()
audit=f'''# NTU 1H26: resumed max-reasoning comparison

Conclusion: **INSUFFICIENT EVIDENCE - FRESH GENERATION BLOCKED**.

Evaluator: Codex (runtime model identifier not exposed). Run started UTC 2026-10-27T17:24:40Z; local 2026-10-27T19:24:40+02:00. Audit saved local {now}.

## Valuation scorecard

| Metric | Result | Basis |
| --- | --- | --- |
| Fresh Stage 1 / Stage 2 | Neither returned | Stage 1 request failed; Stage 2 not submitted |
| Preserved original target | R0.55, NOT VERIFIED | Prior DeepSeek output, not a validated fair value |
| Gemini alternative | R1.07, NOT VERIFIED | Prior Codex review identifies unsupported retained add-back |
| Experimental reference | R0.89 | Frozen prior-note reference; not a current quote |
| Current quote / rating / TSR | NOT VERIFIED | No fresh quote requested or obtained; no validated target |

## Execution and actual metadata

Executed the authorized `.venv/Scripts/python.exe -u scratch/run_ntu_max_comparison.py`; actual exit code **1**. Requested configured `deepseek/deepseek-v4.1-flash-1017:nitro`, reasoning `max`, maximum combined reasoning/final-answer tokens 65,536, HTTP timeout 900 seconds. Client retries and base-model fallback ended with `OpenRouter connection error (deepseek/deepseek-v4.1-flash-1017): <urlopen error [Errno 11001] getaddrinfo failed>`.

The user's expected network change did not restore OpenRouter name resolution in this execution environment. Current tool configuration still reports restricted network and unavailable sandbox approval. This demonstrates a local name-resolution failure, not a verified OpenRouter outage. No permission escalation or alternative execution route was attempted.

No provider response, generation ID, finish reason, actual model/provider, usage, achieved reasoning tokens, cost, or final answer was returned. Actual execution metadata is `status.json`; successful `.run.json` and generation-statistics files do not exist. Completion/billing are not verified. No claim of achieved max reasoning or improved financial quality is possible. See `execution_log.txt` for observed terminal output.

## Preservation and coverage

`inputs/manifest.json` records exact paths and SHA-256 of the four original DeepSeek briefs and full Gemini (`20261027T163950Z_gemini`) / Codex (`20261027T164527Z_codex`) audit trees. Exact originals were copied before submission. A consistent SQLite backup, two captured sections with ledger, and guardrail registry were preserved. `integrity_checks.json` independently confirms every listed original and saved snapshot matches its hash after the run. The Stage 1 prompt is byte-identical to the preceding failed attempt; its SHA-256 is `{check['stage1_prompt_sha256']}`.

Original PDF: `companies/consumer_lending/NTU/sources/` (exact nested path in manifest), `nutunlimitedcondensedconsolidatedafs31march2026.pdf`, 38 physical pages. SHA-256 `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc` matches SQLite, prior baseline, and post-run bytes. No PDF modified. No new PDF pages extracted, read or visually inspected during this attempt; runner stopped before its Stage 2 extraction. No financial reconciliations independently rerun here. Prior audit calculations are preserved, not newly validated.

Actually inspected: runner source; failed prior comparison audit; required project instructions/workflow and current relevant state; original Gemini and Codex evaluation claims through bounded tool reads (some long combined output was truncated); OpenRouter policy/retry excerpts; new manifest/status and computed integrity evidence. The full prompts, original model outputs, prior calculation scripts, section records, guardrail registry and SQLite snapshot are preserved but not fully independently reviewed in this attempt. Source primary evidence is supplied but unread. A comparison cannot be performed without fresh outputs; the prior register below remains pending.

## Experimental design and boundaries

Same two existing captures/ledger, fresh Stage 1/Stage 2 intended under current guardrails, with full primary report extraction intended for Stage 2 and frozen R0.89 reference. Evaluator conclusions were not injected. This tests max reasoning plus updated guardrails/regenerated prompts and provider/stochastic variation; it cannot isolate reasoning as the cause of any future improvement. No fresh section analysis was requested. Production notes, valuation fields, source locations and guardrails were not changed. No `evaluate_stock.py --rerun` was used because it writes production outputs. Preliminary valuation checks were not rerun: they cannot validate absent experimental outputs.

## Claim verification register
{claims}
## Findings, errors and lessons

F001 (execution blocker; linked C001-C012): same DNS failure recurred before a final response; severity blocking for this experiment. All fresh analytical checks remain NOT VERIFIED. Financial effect unquantified because no fresh model exists. Required next action is working OpenRouter access for this runner, followed by both stages and independent primary-source reconciliations.

No new financial error, corrected claim or analytical improvement is established by this attempt. Previous baseline lessons remain attributed to the preserved reviews: distinguish POCI gains from loss coverage and equity NAV from contributed capital; rebuild consistent cash flows, financing roll-forwards and valuation sensitivities. Gemini's R1.07 and dependent recommendations remain unvalidated by the preserved Codex review. None of these prior diagnoses was independently revalidated here.

No newly discovered reusable rule is proposed and no guardrail was codified. The user's approval gate remains in effect.

## Decision and handoff

**Insufficient evidence.** Completed: execution attempt, input snapshots, PDF/database hash match, post-run original/snapshot integrity, exact-prompt comparison and failure record. Material missing evidence: both fresh final answers, actual generation metadata, all fresh financial reconciliations and comparative primary-page verification. Do not publish a new target/rating or claim quality improvement.

Resume from repository root using the same runner once OpenRouter DNS resolves; it creates another versioned run. After successful generation, test every pending claim in both stages against the preserved original DeepSeek outputs, Gemini findings and Codex qualifications; reopen all material new dependencies, not only the checklist. Preserve raw final answers and actual metadata and keep them separate from production until reviewed.

No application source changed; pytest not run for this evidence/execution-only attempt. Integrity script exited 0 (actual result recorded after execution in the turn). No temporary pytest directory or Qt window created. Tool retrospective: oversized combined reads were truncated; relevant current state and execution policy were reread with bounded output. This is the existing TOOL_CHEATSHEET section 19 pattern; no new shell, encoding or editing error pattern discovered. Prior audit scripts were not executed.

Revision log: initial record for this distinct retry. Previous failed audit and all earlier model evaluations retained unchanged.
'''
(run/'audit.md').write_text(audit,encoding='utf-8')
state=root/'workflow/STATE.md'
text=state.read_text('utf-8')
entry='''- **NTU max comparison resumed; DNS still blocked (2026-10-27)**:
  - Ran the authorized saved runner again; actual exit code 1. New evidence run: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T172440Z_codex_max_comparison/audit.md`.
  - PDF hash matches SQLite/prior baseline. All copied original briefs and Gemini/Codex audit artifacts rechecked unchanged; exact Stage 1 prompt is identical to prior attempt (176,400 characters).
  - Max/65,536/900s Stage 1 retries/base fallback again failed with `[Errno 11001] getaddrinfo failed`. No final answer or generation metadata; Stage 2 not submitted. No fresh comparison or quality improvement can be established. Network access to OpenRouter remains unusable from this runner.
  - Saved manifest, SQLite/capture/guardrail snapshots, actual status/terminal output and independent hash checks. No production notes, valuation fields, source PDFs or guardrails changed. No pytest run (execution/evidence-only); no new tooling-error pattern beyond existing oversized-read guidance.

'''
assert text.count('## Completed\n')==1
state.write_text(text.replace('## Completed\n','## Completed\n\n'+entry,1),encoding='utf-8')
print(json.dumps({'audit':str(run/'audit.md'),'all_originals_and_snapshots_match':check['all_originals_and_snapshots_match'],'prompt_identical_to_prior_attempt':check['prompt_identical_to_prior_attempt'],'source_matches':all(s['matches'] for s in check['sources'])},indent=2))