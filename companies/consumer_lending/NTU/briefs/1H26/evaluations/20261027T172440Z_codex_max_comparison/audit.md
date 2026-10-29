# NTU 1H26: resumed max-reasoning comparison

Conclusion: **INSUFFICIENT EVIDENCE - FRESH GENERATION BLOCKED**.

Evaluator: Codex (runtime model identifier not exposed). Run started UTC 2026-10-27T17:24:40Z; local 2026-10-27T19:24:40+02:00. Audit saved local 2026-10-27T19:26:06.888410+02:00.

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

`inputs/manifest.json` records exact paths and SHA-256 of the four original DeepSeek briefs and full Gemini (`20261027T163950Z_gemini`) / Codex (`20261027T164527Z_codex`) audit trees. Exact originals were copied before submission. A consistent SQLite backup, two captured sections with ledger, and guardrail registry were preserved. `integrity_checks.json` independently confirms every listed original and saved snapshot matches its hash after the run. The Stage 1 prompt is byte-identical to the preceding failed attempt; its SHA-256 is `d3429a17b544e5e4f47e1f32afa4435342cff5060e6b2e79e1b09037e850ab7a`.

Original PDF: `companies/consumer_lending/NTU/sources/` (exact nested path in manifest), `nutunlimitedcondensedconsolidatedafs31march2026.pdf`, 38 physical pages. SHA-256 `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc` matches SQLite, prior baseline, and post-run bytes. No PDF modified. No new PDF pages extracted, read or visually inspected during this attempt; runner stopped before its Stage 2 extraction. No financial reconciliations independently rerun here. Prior audit calculations are preserved, not newly validated.

Actually inspected: runner source; failed prior comparison audit; required project instructions/workflow and current relevant state; original Gemini and Codex evaluation claims through bounded tool reads (some long combined output was truncated); OpenRouter policy/retry excerpts; new manifest/status and computed integrity evidence. The full prompts, original model outputs, prior calculation scripts, section records, guardrail registry and SQLite snapshot are preserved but not fully independently reviewed in this attempt. Source primary evidence is supplied but unread. A comparison cannot be performed without fresh outputs; the prior register below remains pending.

## Experimental design and boundaries

Same two existing captures/ledger, fresh Stage 1/Stage 2 intended under current guardrails, with full primary report extraction intended for Stage 2 and frozen R0.89 reference. Evaluator conclusions were not injected. This tests max reasoning plus updated guardrails/regenerated prompts and provider/stochastic variation; it cannot isolate reasoning as the cause of any future improvement. No fresh section analysis was requested. Production notes, valuation fields, source locations and guardrails were not changed. No `evaluate_stock.py --rerun` was used because it writes production outputs. Preliminary valuation checks were not rerun: they cannot validate absent experimental outputs.

## Claim verification register


The baseline diagnoses below come from the preserved Codex audit; this attempt does not revalidate those diagnoses. Every fresh-run verdict is **NOT VERIFIED** because no answer was returned. Preserve these IDs in the next comparison.

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

For each item, record Stage 1 treatment, Stage 2 treatment, primary-page evidence, independent calculations, severity, and whether the defect was corrected, persisted, newly introduced, or remains unverified. Distinguish correction from mere omission. Review Gemini's supported/partly supported findings and Codex-identified misses separately. Count only tested claims, and do not interpret more words or more reasoning tokens as proof of quality.


## Findings, errors and lessons

F001 (execution blocker; linked C001-C012): same DNS failure recurred before a final response; severity blocking for this experiment. All fresh analytical checks remain NOT VERIFIED. Financial effect unquantified because no fresh model exists. Required next action is working OpenRouter access for this runner, followed by both stages and independent primary-source reconciliations.

No new financial error, corrected claim or analytical improvement is established by this attempt. Previous baseline lessons remain attributed to the preserved reviews: distinguish POCI gains from loss coverage and equity NAV from contributed capital; rebuild consistent cash flows, financing roll-forwards and valuation sensitivities. Gemini's R1.07 and dependent recommendations remain unvalidated by the preserved Codex review. None of these prior diagnoses was independently revalidated here.

No newly discovered reusable rule is proposed and no guardrail was codified. The user's approval gate remains in effect.

## Decision and handoff

**Insufficient evidence.** Completed: execution attempt, input snapshots, PDF/database hash match, post-run original/snapshot integrity, exact-prompt comparison and failure record. Material missing evidence: both fresh final answers, actual generation metadata, all fresh financial reconciliations and comparative primary-page verification. Do not publish a new target/rating or claim quality improvement.

Resume from repository root using the same runner once OpenRouter DNS resolves; it creates another versioned run. After successful generation, test every pending claim in both stages against the preserved original DeepSeek outputs, Gemini findings and Codex qualifications; reopen all material new dependencies, not only the checklist. Preserve raw final answers and actual metadata and keep them separate from production until reviewed.

No application source changed; pytest not run for this evidence/execution-only attempt. Integrity script exited 0 (actual result recorded after execution in the turn). No temporary pytest directory or Qt window created. Tool retrospective: oversized combined reads were truncated; relevant current state and execution policy were reread with bounded output. This is the existing TOOL_CHEATSHEET section 19 pattern; no new shell, encoding or editing error pattern discovered. Prior audit scripts were not executed.

Revision log: initial record for this distinct retry. Previous failed audit and all earlier model evaluations retained unchanged.
