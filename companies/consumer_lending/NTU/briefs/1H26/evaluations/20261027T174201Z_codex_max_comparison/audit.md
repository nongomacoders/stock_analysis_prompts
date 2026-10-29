# NTU 1H26 max-reasoning comparison: approval-blocked attempt

**Outcome: INSUFFICIENT EVIDENCE. Fresh Stage 1/2 comparison remains pending.**

Created UTC: 2026-10-27T17:42:01.772311+00:00. Local: 2026-10-27T19:42:01.772325+02:00 (Africa/Johannesburg). Evaluator: Codex; exact runtime model/settings not independently exposed.

## Valuation scorecard

Prior target R0.55 and its recommendation remain NOT VERIFIED under the preserved Codex review. No fresh target, forecast, recommendation or current quote is available. Frozen R0.89 is a historical reference only. No financial-validation pass is inferred from connectivity or successful preservation checks.

## Execution and approval boundary

The requested runner was invoked with the local virtual environment. It created this versioned run, preserved originals and prepared Stage 1. Requested model: deepseek/deepseek-v4.1-flash-1017:nitro; max reasoning, 65,536 completion-token ceiling, 900-second timeout. Actual model/provider, reasoning consumption, generation ID, completion, cost and billing are NOT VERIFIED.

The initial invocation returned session 83535. The subsequent process-output call was rejected by automatic approval review: "The runner uploads sensitive NTU section captures and the complete financial report to OpenRouter; the request authorizes the comparison but does not explicitly authorize sending this payload to that external destination." No retry or alternate upload was attempted.

The on-disk status remains `running` / `stage1`; this is a stale local checkpoint, not proof that a request remains active or succeeded. A safe cancellation attempt found the process session unavailable (Unknown process id 83535). A final Get-Process python query returned no Python processes. CIM process inspection was unavailable and is not used as proof of termination. No final runner exit code was returned. Because the initial invocation progressed before rejection, whether any Stage 1 payload reached the service is NOT VERIFIED. Stage 2 has no prompt/output and no evidence of submission. Do not describe the run as a clean pre-submission rejection or a completed comparison.

The only output present at verification is the exact Stage 1 prompt. No fresh response or .run.json/generation statistics were available. Explicit user approval for sending the existing section captures/ledger and full source-report text to OpenRouter for DeepSeek Stage 1/2 is needed before resuming. This may consume paid API usage. Transport and process behavior after that approval still need verification.

## Preservation, coverage and independent checks

`inputs/manifest.json` lists exact original/saved paths and hashes. Preserved four original briefs and the complete Gemini (20261027T163950Z_gemini) and Codex (20261027T164527Z_codex) audit trees; consistent SQLite backup, two captured sections/ledger and guardrail snapshot. `independent_verification.json` records actual checks performed in this attempt.

Source PDF: nutunlimitedcondensedconsolidatedafs31march2026.pdf; 38 physical pages; SHA-256 `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`. Recomputed hash matches SQLite and prior baseline. All 50 preserved files match both original hashes and saved copies. Production report row and guardrail registry equal the pre-run snapshots. No production notes, valuations, source PDF or guardrails were replaced.

Stage 1 prompt: 176400 characters; identical SHA-256 to the first attempt. Existing section analyses/ledger are reused. Updated guardrails and regenerated prompts are part of the intervention. No evaluator findings were deliberately injected by the runner. This is a combined reasoning/guardrail/prompt test, with possible provider/stochastic differences, and cannot isolate a reasoning-only effect.

Inspected runner, AGENTS.md, TOOL_CHEATSHEET.md, current workflow and reasoning policy, relevant STATE entries, section 1A/output protocol, original failed comparison audit and complete prior Codex audit. Gemini audit and architecture inspected partially; input artifacts preserved but original Stage 1/2 full content and all snapshot rows not newly reviewed in this attempt. No PDF pages independently read, rendered or financially revalidated here. Prior review coverage is historical evidence, not new page inspection. No prior reconciliation scripts were executed. The fresh-output comparison and numerical reconciliations cannot be performed without fresh outputs.

Independent preservation script exited 0. No application source changes; pytest not run for evidence-only preservation. The runner's actual exit code remains unavailable.

## Claim register: retain prior comparison IDs

All fresh-run verdicts remain NOT VERIFIED. This register carries forward prior diagnoses as review tasks, without claiming their independent revalidation in this attempt.

| ID | Claim to test | Prior observation / expected evidence | Fresh verdict |
| --- | --- | --- | --- |
| C001 | POCI gain versus ECL reserve classification | Prior Codex C003: 3414+431=3845; 431 is cumulative gain, preserve source allowance label and amortised-cost/FVTPL scope; PDF pp.13,23-24 | NOT VERIFIED |
| C002 | Statutory ordinary NAV | Prior C004: 1329/780.651033 approximately R1.70; contributed capital alone is not NAV; pp.8,16 | NOT VERIFIED |
| C003 | Net run-off footnote signs | Prior C005: (728-383+167)+(116-30)=598 versus597; explain remaining1 rather than assert exact reconciliation; pp.13,31 | NOT VERIFIED |
| C004 | Valuation bridge and repeated discounts | Prior C007-C009: unsupported1479 add-back and repeated discounts; rebuild inputs rather than adopt Gemini R1.07 | NOT VERIFIED |
| C005 | FCFE accounting and collection signs | Prior C013: collection inflows, purchase outflows, consistent IFRS-versus-CODM starting point; no blind sign flip | NOT VERIFIED |
| C006 | Forecast cash roll-forward | Prior C014: FY26/FY27/FY28 unexplained532/810/840; every forecast period needs financing and balance-sheet reconciliation | NOT VERIFIED |
| C007 | Sensitivity reproduction | Prior C015: matrix must use exact base valuation formula and reproduce central target | NOT VERIFIED |
| C008 | Revenue denominator and scope | Prior C016: UK+US515/711=72.4% of IFRS services;515/1599=32.2% CODM total; p.36 | NOT VERIFIED |
| C009 | Liquidity claims and available facilities | Prior C012/C020:809 is partial static comparison, not a proven future shortfall; facilities and restrictions unresolved | NOT VERIFIED |
| C010 | Lifetime versus12-month ECL allegation | Prior C017: clarification warranted, understatement not established | NOT VERIFIED |
| C011 | Rating bands and trading-stop direction | Prior C010/C011/C021: economic target first; monotonic bands do not validate it; short stop must limit losses in correct direction | NOT VERIFIED |
| C012 | New errors or omissions | Check all fresh material dependencies, beyond this baseline checklist | NOT VERIFIED |


## Findings, valuation errors and analytical lessons

F001 (operational): automatic approval rejection prevents the requested end-to-end comparison. Consequence: no supported fresh target or improvement conclusion. No new analytical error in fresh model output can be established because no such output is present.

Prior Gemini/Codex disagreements (POCI scope/signs, statutory NAV, net run-off signs, unsupported add-back/discounting, FCFE/cash balances, sensitivities, liquidity and recommendation) remain the comparison baseline. Mere omission of a prior defect must not be counted as correction. Actual reasoning tokens must be inspected rather than inferred from requested max.

No new analytical rule is proposed or codified. Existing approved guardrails are unchanged. Further analytical improvements require user approval before registry changes.

## Revision and handoff

Initial record for this attempt; no prior audit overwritten. Prior attempted runs remain intact. Preserve exact fresh prompts, final outputs, run metadata and independent numerical checks when explicit upload approval allows a new run. Do not accept the legacy target or Gemini's R1.07 as financially validated. Continue the twelve-claim comparison against original PDF evidence and preserved evaluations before updating production valuation fields.
