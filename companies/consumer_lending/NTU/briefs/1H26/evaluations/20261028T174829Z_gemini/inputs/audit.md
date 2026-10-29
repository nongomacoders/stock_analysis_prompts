# NTU1H26 — refined chronological section trial:limited Codex review

UTC:2026-10-28T17:31:45.572392+00:00;local:2026-10-28T19:31:45.572392+02:00.
Decision:**section-only execution complete;ledger and financial interpretation corrections remain required**.

Implemented exactly the three authorized prompt refinements:sign/unit consistency,conditional POCI applicability and cautious first-time comparative interpretation. No PDF split,ledger-schema or stage-policy redesign. Shared prompt and sector note versions preserved in inputs with hashes;pre-change prompts also preserved. No company-specific lesson block or seed questions. Actual normal section settings:Fireworks-only,reasoning none,16384 ceiling.

## Execution and accounting

22/22 completed generations,zero provider fallback/repair calls.24 captured units cover38 physical pages exactly once;22 financial analyses and2 retained navigation captures. TotalUSD0.0702026388;input151251,completion51535,reasoning0,cached input23564. Summed request208.174s;first-dispatch-to-last-accounting340.451335s (5m40.45s). All22 costs corroborated by generation metadata. Metadata waits and wrapper time are included in wall time;client elapsed is not provider latency.

Ledger started empty. Each next prompt's before-state matches the previous persisted after-state;rejected deltas did not change it.18 valid,4 rejected.32 persistent records:15partial,15open,1contradicted,1resolved.39 proposed new questions include7 in rejected deltas. All raw briefs and unapplied changes remain saved;downstream persistent ledger does not include those7. This is not22 successful ledger updates. Different prompts/provider/initial seed state prevent controlled quality/cost comparison to older full runs.

## Source coverage and independent calculations

Original PDF SHA verified before export and after completion. Complete physical PDF pages13,22,24,25,31 independently rendered and viewed this turn;images/text retained in source_pages. Other physical pages were supplied to DeepSeek but not independently visually audited in this turn. All38 captured-page presence is distinct from content verification. Audit inputs preserve prior versions,requests,receipts and raw outputs;production tables and prior files verified unchanged.

check_run.py and outputs/independent_calculations.json reproduce selected historical arithmetic;source_spotcheck_calculations.json reproduces independently viewed source-based checks. In particular:5+390+3845+644=4884;−63−29+68+597+1+216=790;gross3414+gain431=3845. Conditional signed amortisation728−383+167+116−30=598 differs1 from printed597;source formula not asserted. Claim IDs and findings are saved separately.

## Findings

**F001 — SUPPORTED WITHIN RUN**

All22 Fireworks generations completed;38 captured pages once,24 units including2 navigation units. Fresh ledger chronology proven;18 validated deltas and4 rejected/unapplied. No repair calls. Structural coverage does not prove semantic correctness.

**F002 — CONFIRMED LEDGER RELIABILITY LIMIT**

Income/equity pp9–11,purchased debt p13,EPS pp18–19,and current segment pp30–31 deltas failed literal-quote checks. Entire deltas were held out as existing app behavior;7 proposed new questions across those responses were not persisted. Raw answers and unapplied deltas retained;these are not accepted closures.

**F003 — SUPPORTED WITH LIMITS**

p13 prose uses both correct signed portfolio rolls and explicitly excludes ordinary POCI Stage1/2 SICR migration demands. p25 includes currency-risk start/p26 dependency,flags exchange-rate unit-label conflict and avoids asserting a cause for zero rates. p13 ledger was rejected,so prose correctness is not an accepted ledger improvement;no causal guarantee from a single run.

**F004 — CONFIRMED CAPTURE/INTERPRETATION FAILURE**

p22 other-loan5 and net trade-receivable390 cells were read as5390 in section15,leading to false sum9879 versus4884. Original table is5+390+3845+644=4884. Model also tried conventional gross−431 before recognizing printed gross+431=3845;the cumulative gain is explained by POCI. Preserve original headers/cell boundaries;do not call this a company defect.

**F005 — CONFIRMED ATTRIBUTION/SIGN ERRORS**

p24 model calls first column Debt review and third unlabelled. Original columns are Banking&specialised lending–Unsecured,Debt review,Retail,Banking–Secured. The−241 movement belongs to Unsecured;Debt review is+69. Model says reduced cumulative gain increases net carrying value;at fixed gross,3414+gain means a gain decline reduces net,not increases it.

**F006 — CONFIRMED PERIOD MAPPING ERROR**

p25 prose assigns USD18.4/GBP23.9 closing comparatives to September2025 and17.3/23.2 to March2025. Source dates are the reverse:March2025=18.4/23.9,September2025=17.3/23.2. Currency-topic coverage did not guarantee date/value alignment.

**F007 — CONFIRMED FALSE RECONCILIATION FLAGS**

p31 model adds tax29 instead of retaining printed−29 and alleges58 EBITDA discrepancy. Correct−63−29+68+597+1+216=790. It also invents an all-positive identity for a footnote component list,getting1424 versus597;source footnote does not supply those operators. Conditional signed collections/income bridge gives598 versus597,leaving1 without an asserted issuer explanation. No company defect established.

**F008 — NOT VERIFIED**

Full-report semantic question closure,duplicates/reopening,all remaining section facts,forecast and valuation consequences are not independently audited. Stable IDs/literal quotes are not proof of correct economic interpretation. Only1 persistent question is resolved;15 partial,15 open,1 contradicted. No investment target/recommendation produced.

## Handoff and boundaries

Use the simpler prompt as a first-pass brief,not a validated financial report. Main remaining issues are table-header/cell preservation,sign/period interpretation and reliable literal quote anchors. No additional code/prompt repairs or financial guardrails implemented after observing this run. Existing specific instructions do not prove improved behavior in every section. The observed model errors are not company errors.

Stage1/2,forecast/DCF,current quote,EPS/valuation model,rating and full financing audit:NOT APPLICABLE to this section-only trial. No prior valuation replaced or published. Gemini review remains manual in Antigravity;gemini/PROMPT.md identifies rejected deltas and limits. No Gemini API calls. Source filenames/hashes and before/after ledger states are preserved in plan/inputs/outputs.

Targeted offline checks27 passed in15.64s,exit0. Last full suite226 passed exit0 from prior implementation;not repeated for this two-prompt wording change. Test windows/process disposed by test completion;temporary test folder cleaned after preserving result. Tool retrospective:no policy/permission errors;one attempt to read an in-flight output before it existed returned a nonzero shell code. Check readiness before reading live outputs. All actual model/verification command exit codes0. No automatic follow-on paid work.
