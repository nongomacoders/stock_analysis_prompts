# NTU 1H26 max-reasoning comparison: approved OpenRouter run, telemetry blocked

**Independent outcome: INSUFFICIENT EVIDENCE for a fresh comparison. Preserved baseline still requires corrections.**

Created UTC: 2026-10-27T17:47:28.077337+00:00; local: 2026-10-27T19:47:28.077352+02:00 (Africa/Johannesburg). Evaluator: Codex; exact runtime model identifier/settings not independently exposed. This version supplements, and does not overwrite, the original DeepSeek, Gemini and Codex records.

## 1. Scorecard and execution

| Metric / check | Result | Basis |
| --- | --- | --- |
| Fresh Stage 1 | NOT VERIFIED | Exact prompt prepared; no final response or generation metadata saved |
| Fresh Stage 2 | NOT VERIFIED | No prompt/answer or evidence of submission |
| Prior R0.55 target / recommendation | NOT VERIFIED | Material baseline valuation/cash-flow defects remain |
| Reference price | R0.89, historical/frozen | Not a current quote |
| Current quote / rating / dividend forecast | NOT VERIFIED | No quote fetched; no validated new valuation |
| Source PDF / original preservation | PASS | Independent SHA-256 and SQLite baseline checks |
| Production report row / guardrails | PASS for unchanged | Equal to pre-run snapshots |

The user explicitly authorized NTU captures, question ledger and complete report text to OpenRouter, including paid API calls. Requested settings: `deepseek/deepseek-v4.1-flash-1017:nitro`, reasoning max, 65,536 completion-token ceiling, 900-second timeout. Actual provider/model execution, achieved reasoning tokens, generation ID, usage, cost and billing remain NOT VERIFIED. Max is a request, not evidence of achieved effort or quality.

The unguarded approved run (174426Z) was rejected at output polling over an unspecified telemetry destination. Static inspection of the runner and client found only OpenRouter completion/statistics requests; GitHub is an HTTP header. The session later became unavailable. A safer launcher restricted network connections to the approved service. Its first attempt (174621Z) exited **1** because the required environment-owned localhost HTTPS proxy was not allowed. A following startup assertion exited **1** because proxy ports vary between tool invocations; no new comparison directory was created by that assertion failure.

This final run retains the exact managed loopback proxy and restricts external request URLs to OpenRouter. Its output poll was nevertheless rejected by automatic approval review: **"The guarded run still triggers an external Visual Studio telemetry connection, a separate destination not covered by the user's OpenRouter approval and with unknown payload."** This is the reviewer's reported finding; the telemetry endpoint and payload were not independently exposed to the assistant. Do not attribute it to the financial application without evidence.

No subsequent model request was made. The final local process listing found no Python processes; output inventory contains only Stage 1 prompt. `status.json` retains `running`/`stage1`, a stale checkpoint, not successful completion. **The final runner exit code is unavailable.** Because initial execution progressed before the rejected poll, whether a Stage 1 payload reached OpenRouter is NOT VERIFIED. No fresh answer, complete execution transcript, run JSON or billing record is present. See `execution_events.json` for transcribed events and limitations.

## 2. Inputs, preservation and coverage

PDF: `companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf`, 38 physical pages. Recomputed SHA-256: `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`; matches SQLite and prior baseline. All **50** files listed in `inputs/manifest.json` match their original hashes and saved copies. The four original briefs and complete Gemini (163950Z) / Codex (164527Z) trees are preserved, alongside a consistent SQLite backup, two captured sections/ledger and guardrail registry. `independent_verification.json` confirms unchanged production report row and registry.

Exact prepared Stage 1 prompt is **176,400 characters**, SHA-identical to the first failed attempt. Evaluator conclusions were not deliberately injected. Section analyses are reused, not rerun. This tests max reasoning plus updated guardrails, regenerated prompts and possible provider/stochastic variation. No reasoning-only causal improvement can be inferred, even after future successful generation.

Actually inspected: AGENTS.md, TOOL_CHEATSHEET.md, workflow/WORKFLOW.md, current relevant STATE entries, architecture introduction, section 1A/output protocol, runner/transport code, full original Stage 1 and Stage 2 responses, full Gemini audit in bounded reads, full prior Codex audit and first comparison audit. Prior evaluation scripts were not executed. Original prompts and snapshot contents were preserved but not read end to end. Archived STATE/architecture passages outside the current task were not fully inspected.

Extracted all 38 PDF pages with physical page markers into `calculations/source_pages.txt`; extraction is not full-page inspection. Text actually inspected: physical **3,4,5,8,9,12,13,14,15,16,18,19,20,21,23,24,25,26,27,28,29,30,31,36**. Rendered 8,12,13,23,25,31; visually inspected **23 and31**, confirming signed allowance/table layout and amortisation footnote. Other rendered pages not visually reviewed. Other PDF pages not relied on. Public AASB equivalent of IFRS 9 paragraphs 5.5.13-15 inspected as an accounting reference; no new live quote or company announcement search.

## 3. Claim register and independent baseline checks

All fresh-run verdicts below remain NOT VERIFIED because no new answer exists. These stable C001-C012 IDs retain the original comparison checklist; the prior observations are independently tested as described immediately after the table. Corrections versus omissions/persistence/new defects cannot yet be scored.

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


### Reproduced baseline evidence and calculations

Executed `calculations/baseline_reconcile.py` using local .venv; exit **0**. Actual inputs, formulas, substitutions, results and residuals in `calculations/baseline_reconciliations.json`. Preservation/extraction scripts each exited **0**. No application code changed; pytest not run for evidence-only work. No original evaluator calculation script replayed.

| Claims | Independent source/check | Baseline verdict and consequence |
| --- | --- | --- |
| C001 | PDF pp13,21,23-24:3414+431=3845;598+24-191=431 | PASS for gain classification; FAIL for original conventional coverage interpretation. Preserve source label ECL allowance; separate644 FVTPL assets. Deterioration versus acquisition base-case does not establish a conventional reserve shortfall. |
| C002 | pp8,16:1329/780.651033=R1.702425;5410/shares=R6.930113 | PASS statutory NAV correction; FAIL original R6.90 NAV. No independent market-fair-value conclusion. |
| C003 | pp13,31:(728-383+167)+(116-30)=598 vs597 | FAIL original positive-sum allegation; signs correct under run-off interpretation. Exact R1m residual NOT VERIFIED, plausible rounding only. |
| C004 | Original Stage2 section4:EV4035.55;net debt4400;add1479 yields1114.55;one25% discount=R1.070722;twice=R0.803041;extra31.51% to0.55 | FAIL original target derivation. Add-back1479 vs own net other assets550 leaves929 unexplained. R1.07 is conditional arithmetic, not validated fair value. Intent to force book equity is an inference. |
| C005 | Original Stage2 section3 deducts principal collections as outflow and adds CODM amortisation to IFRS PAT; source pp12-13,30-31 | FAIL forecast cash classification. No blind sign-flip repair; reconcile starting metric and actual noncash expenses. Historical OCF=-111;after PPE17,intangibles13,lease principal30=-171 before other flows. Interest already included. This is not validated forecast FCFE. |
| C006 | Original Stage2 section3:106-538=-432 vs100;100-815=-715 vs95;95-845=-750 vs90 | FAIL forecast cash bridges;unexplained532/810/840m. Source p12 full historical cash bridge does reconcile:-111-61+178=6;107+6=113 including1 held-for-sale cash. |
| C007 | Original section5 versus section4 formula:3845*.05*.75/780.7=.184690;180*.5*.75/780.7=.086461 | FAIL sensitivity derivation under stated formula; published increments approx.07/.05 and base0.55 not supported by single-discount SOTP. Full economic sensitivities NOT VERIFIED. |
| C008 | p36:UK303+US212=515;515/711=72.43%;515/1599=32.21% | FAIL unqualified72% group concentration; denominator/scope must be labelled. |
| C009 | pp5,8,14-15,28:4016 debt;3904 net ex-leases;4249 including345 leases;475 undrawn overdrafts;management approx800 total undrawn | PASS disclosed balances;NOT VERIFIED actual future liquidity deficit.809=1396-112-475 is partial/static. Other investments81, restrictions, other facilities, future operating cash and refinancing not resolved. No all-assets-encumbered conclusion. |
| C010 | pp13,20-21 state lifetime ECL changes plus rolling12-month net-cash modelling;pp13 also show recoveries after12months | NOT VERIFIED amount/direction of under-provisioning. Clarify tail value/methodology; do not assert statutory breach merely from horizon wording. |
| C011 | Original JSON thresholds:.42<.48<.58<.65;reference.89>.65;short stop.65<entry.89 | PASS internal monotonicity only;FAIL static SELL/band mismatch and short loss-stop direction. Target/rating economics/current price NOT VERIFIED. |
| C012 | Original Stage1 trade-receivable SICR allegation;source pp20,25 and accounting reference below | Additional unresolved policy/scope error identified; see C013/F003. Fresh new errors remain unavailable. |

C013 (additional baseline dependency, historical/accounting assertion): Original Stage1 section2.2 says zero displayed ECL through61-90days proves no Stage2 provisioning until90+days. **FAIL as an established policy conclusion**: p25 is an age/expected-loss-rate table and does not establish staging mechanics; p20 says standard30-day terms. The relevant simplified lifetime-ECL approach must be assessed for trade receivables without a significant financing component. Actual company policy application, unrounded losses and adequacy remain NOT VERIFIED. A printed0.00% does warrant challenge and comparison to Sep25 rates, but does not alone prove a relaxed SICR policy. Financial impact unquantified. Gemini did not identify this issue; the previous Codex register did not specifically test it.

Primary accounting reference: [AASB9 Chapter5, paragraphs5.5.13-15](https://standards.aasb.gov.au/node/3451), inspected27October2026. The published IFRS-equivalent provisions distinguish cumulative lifetime-ECL changes for POCI from the simplified lifetime-loss treatment for qualifying trade receivables. This supports scope qualification, not a finding that Nutun's reported ECL is adequate or inadequate.

## 4. Findings, evaluator comparison and valuation lessons

- **F001: execution/telemetry blocker**, linked all fresh claims, severity operational/material to this task. No fresh answers or measurable improvement. Earliest observed point is tool approval review, not demonstrated application telemetry. Explicit OpenRouter approval is retained; distinct reported Visual Studio telemetry remains outside it.
- **F002: baseline corrections remain required**, linked C001-C011, critical. Independent calculations confirm material original errors. Gemini's POCI/NAV findings are supported with scope/sign qualifications; amortisation finding partly supported with1m residual; duplicate-discount/add-back diagnosis supported, intentional plug only inferred. Gemini's R1.07 and unqualified STRONG SELL conclusions remain unsupported. Its188vs182 cash-bridge residual remains6m. Its reported current quote was not independently checked. Prior Codex misses on FCFE/cash/sensitivities/denominator/short-stop are reproduced here. No new target is validated.
- **F003: trade-receivable staging inference unsupported**, linked C012/C013, medium (unquantified valuation impact). Earliest directly inspected origin is original Stage1 section2.2; captured-section origin not traced in this attempt. Revise allegation to an evidence request about applicable impairment approach, exact loss rates and policy. Gemini and prior Codex did not resolve this claim.

Lessons: test reconciliations and dependent conclusions, not prose sophistication; reported POCI allowance signs must reconcile; statutory NAV is not share capital; forecasts must close; do not treat a repaired discount calculation as validation of unsupported inputs. ECL framework must match instrument/scope before alleging a staging breach.

No new reusable guardrail is proposed or codified during this blocked comparison. Do not amend SQLite/default guardrails or production notes without approval. The instrument-scope issue is recorded as a future review question, not implemented as a new rule.

## 5. Decision, revisions and handoff

Conclusion: **INSUFFICIENT EVIDENCE for fresh model comparison; CORRECTIONS REQUIRED in preserved baseline.** Usable conclusions are limited to independently supported historical figures and baseline defects above. No fresh valuation, live recommendation, guardrail effectiveness score or max-reasoning quality improvement established.

Revision log: user explicitly approved OpenRouter payload/cost after initial approval gate. Subsequent gate concerned a different destination. Two safe transport restrictions were tried; proxy failure corrected while retaining required managed proxy. The final reviewer still reported Visual Studio telemetry. No further model run attempted. Original financial findings are not overwritten; C013 adds an unresolved baseline claim. All prior evaluations retained.

Next authorized work requires resolving the reported telemetry gate (disable the connection at its source or obtain explicit approval for the reported destination/payload uncertainty), then create a new versioned runner attempt. Do not bypass the gate or conflate endpoint reachability with upload authorization. Preserve fresh prompts/answers/metadata, verify actual provider and reasoning consumption, apply C001-C013 to both fresh stages, compare with both evaluators and independently reconcile forecasts/SOTP/sensitivities before changing any production valuation fields.
