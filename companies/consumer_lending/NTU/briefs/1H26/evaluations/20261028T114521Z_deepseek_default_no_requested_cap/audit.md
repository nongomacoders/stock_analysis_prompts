# NTU1H26 — no requested token cap: preliminary Codex evidence audit

**Execution supported within stated coverage; financial corrections/materiality review required.** Outstanding section, refreshed Stage1 and full Stage2 all completed. Stage2's analytical decision is **VALUATION WITHHELD**; no forecast, DCF or target was produced. This differs from the parent run's token-exhaustion failure. A completed withheld report is not a validated valuation model.

Evaluator: Codex; exact runtime model/settings not independently exposed. Run created2026-10-28T11:45:21Z (13:45:21 SAST). Actual model requested `deepseek/deepseek-v4.1-flash-1017`; provider metadata identifies Fireworks for the capture and DigitalOcean for refreshed Stage1/Stage2. No Nitro, provider order/sort, priority tier, reasoning override, max_tokens or max_completion_tokens was sent. Catalog defaults were saved; thinking defaults enabled/high. Provider/model/account limits remain applicable.

## Inputs, preservation and coverage

Source: `companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf`,38 physical pages, SHA256 `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`. Source hash matched the registered original and remains unchanged. No new PDF images were inspected here. Primary tables pp.8,9,12,13,16,22,24,31 had already been visually inspected against this exact hash in the prior Codex review `20261028T093647Z_codex_review/audit.md`; selected historical arithmetic below reuses that verified source basis. Model ingestion of38 pages is not a claim of fresh independent full-PDF inspection.

Inspected new Stage1, the Stage2 opening JSON/readiness contract and relevant historical/scope sections, publication assessment, source/ledger coverage and all three receipts/request settings programmatically. Parent outputs were preserved and selected claims compared. Other parent section outputs were retained but not all independently reread line by line. The underlying complete forecast/DCF cannot be inspected because none was built. No current quote, underlying portfolio model, loan contract/covenant certificate, tax schedule or companion filing was obtained.

Exact new subjects were copied without changes into `inputs/review_subject/` before any correction; hashes and original/preserved paths in `inputs/review_subject_manifest.json`. Reused parent outputs copied into `inputs/parent_outputs/`; `inputs/audit_manifest.json`, `plan.json` and parent preserved input files identify exact requests/outputs/source and baseline hashes. No original model answers were edited. Production all-table hashes, source PDF and enumerated parent originals passed final preservation checks. Financial checks are preliminary; manual Gemini/Codex independent review remains required.

## Claim register and independent checks

H=historical disclosure; D=derived calculation/process; A=analytical assumption/assertion. Financial figures consolidated NTU Rm unless labelled per-share, percentages or prior-year periods.

| ID | Origin and claim | Class | Evidence and independent check | Verdict/consequence |
|---|---|---|---|---|
| C001 | No requested completion cap/default thinking/normal routing | D | Three saved request JSON payloads checked for omitted cap/reasoning/provider/service-tier fields and exact base model | PASS request settings; not an infinite provider budget. |
| C002 | Outstanding capture and both stages completed | D | Three receipts finish_reason=stop; accepted capture coverage10/10 after reusing nine prior analyses | PASS execution; source38/38 pages. No ledger repair in this continuation. |
| C003 | CostUSD0.04537836 | D | Three usage costs each match generation total_cost within1e-9; exact Decimal sum | PASS accounting. Prior capped costUSD0.1893089364, combinedUSD0.2346872964, not billed twice. |
| C004 | Removal of cap alone caused success | A | New completion counts11,728/12,770/14,000 all below prior32,768/49,152/65,536; refreshed context and providers differ | NOT VERIFIED causal claim. F001 medium: retain run variability/settings/context qualifications. |
| C005 | New Stage1/Stage2 signed POCI and portfolio balances | H/D | pp.13,22:3,414+431=3,845; principal3,975+382−728+383−167=3,845; other702+28−116+30=644 | PASS historical arithmetic only; does not establish collection forecasts or fair value. |
| C006 | Combined PBD decline188 versus statutory182 leaves6 | H/D | pp.12–13: net cash728+116−382−28=434; accounting income383−167+30=246;434−246=188;188−182=6 | PASS scoped arithmetic. Remaining6 unexplained; no invented FX/rounding plug. Valuation materiality NOT VERIFIED. |
| C007 | Gross/net residual107 and ETR+31.5% | H/D | pp.8,9,22:497−(395−5)=107; signed tax expense−29/PBT−92=+31.52% | PASS. Precise residual composition/tax/DTA support not independently established. |
| C008 | FY25 historical-book loss259 | H/D | p.24: first-half77+second-half182=259; current half191 | PASS period arithmetic. Vintage/FX cause NOT VERIFIED. |
| C009 | Signed amortisation/NAV/cash rollforward | H/D | pp.13,31:728−383+167+116−30=598 versus printed597; pp.8,16:NAV1,329/780.651033=1.7024; p.12:107−111−61+178=113 | PASS within stated source/rounding coverage; no FCFE or target validation. |
| C010 | Static maturity gap means proven cash shortfall | A | pp.8,13–15,35: undrawn overdrafts475, management facilities~800, maturities1,396; timing/conditions/renewals needed | FAIL as a proven deficit inference; new outputs correctly avoid it. Forward financing path NOT VERIFIED. |
| C011 | Simplified ECL scope established automatically | A | pp.20,25 short trade terms/matrix; explicit application/policy not confirmed | NOT VERIFIED. New output correctly keeps policy conditional and avoids automatic SICR/zero-ELR manipulation claims. |
| C012 | Stage2 historical portfolio PASS validates forecast portfolio rollforward | A | Stage2 PASS evidence covers historical amounts only; no forecast schedule | NOT APPLICABLE to absent forecast; historical PASS must not imply forecast readiness. F002 medium. |
| C013 | Every listed uncertainty/residual is a material valuation blocker | A | Stage2 includes residual6, trade-policy uncertainty/allowance5 and historical vintage attribution; no quantified valuation sensitivity | NOT VERIFIED proportionality. F003 medium: distinguish dependencies, analytical limitations and proven material blockers. |
| C014 | Full forecast/DCF/sensitivity defects repaired | A | Stage2 explicitly states not performed and null target/rating/returns | NOT APPLICABLE; no model available to retest. Publication withholding is separately PASS. |

Executed `workflow/changes/20261028_ntu_default_run/check_uncapped_results.py`, final exit0, actual output in `outputs/independent_checks.json`; exact script copied to `inputs/`. Inputs are source-transcribed figures, not accepted because a model printed them. Checks verify arithmetic, request omission, three complete responses, billing agreement, null price fields, no incomplete active captures and preservation. These checks do not certify fair value or semantic ledger closure.

## Results, findings and revisions

Incremental costUSD0.04537836; input89,445; completion38,498 including reasoning29,835; cached input0. Client request elapsed39.189s/61.727s/51.560s, sum152.476s. First dispatch to last accounting168.801433s, including metadata lookup/orchestration. All billing metadata retrieved; no missing cost fields. Reasoning is a completion subset, not added again.

Compared with parent, this continuation resolves the outstanding section generation and updates downstream source/ledger context. Stage1/Stage2 now explicitly carry the scoped6 residual; preserve the correct107 receivables bridge, positive conventional ETR and259 prior-year historical loss; and keep simplified ECL conditional. Improvements within this evidence coverage are supported. Broader modeling improvement is untested because Stage2 withholds rather than producing forecasts/DCF/sensitivity. No forecast or target is introduced by this audit.

F001: provider/context/generation differences and successful outputs below old caps prevent a causal “cap omission alone fixed it” conclusion. F002: numerical historical portfolio/cash PASS checks do not validate unperformed future schedules. F003: several listed blockers need a materiality/forecast-consequence assessment; an unresolved disclosure or small residual should not automatically become a valuation prohibition. These findings require reviewer judgment, not automatic weakening of the publication gate.

Revision history preserves the parent capped run and its four failures rather than replacing them. User explicitly authorized this separate no-requested-cap continuation. Nine accepted captures were reused; only the outstanding capture plus refreshed Stage1/Stage2 were paid generations. No new production guardrail was added. The original PDF and production valuations remain unchanged.

## Handoff and limits

Stage2 completed with WITHHELD status and null derived fields; no target/recommendation is supportable from unperformed valuation work. Missing material forecast, debt/financing, tax/POCI assumptions still require evidence-supported treatment; do not invent a company failure from missing inputs. The app assessment is a readiness check, not independent financial validation. All12 ledger records persist:3 resolved,3 partial,6 open; inherited and new validation history1 rejected/10 valid. Closure semantics are not fully audited here.

Manual Gemini handoff is `gemini/PROMPT.md`, including exact source path/hash, comparison scope, missing inputs, required claim/calculation records and proportionality checks. Gemini should independently inspect PDF images and every consequential assumption, then Codex reviews its saved audit. Gemini API calls0. No current market quote; referenceR0.89 is historical/frozen only.

Terminal retrospective: uncapped prepare, live execute, metadata refresh, finalization, result checker and exact-subject preservation all exited0. The earlier capped live exits1 were real preserved incompletions. Missing metadata404 was resolved by later read-only lookup; no paid billing-recovery retries. No new shell/encoding/edit failure occurred; TOOL_CHEATSHEET.md section32 records the relevant accounting/default-setting pattern. No application defaults or production prompts were changed; no full pytest suite was needed for this isolated continuation.
