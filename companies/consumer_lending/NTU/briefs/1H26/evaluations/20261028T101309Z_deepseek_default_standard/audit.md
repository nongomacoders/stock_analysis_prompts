# NTU1H26 — capped default-thinking trial: preliminary Codex audit

**Decision: corrections required / insufficient evidence for a valuation. Full Stage2 generation incomplete.** This is a process failure, not a completed financial withholding decision. No target, rating, bands, upside, yield or TSR was published by this trial.

Evaluator: Codex, exact runtime model/settings not independently exposed. Run created2026-10-28T10:13:09Z (12:13:09 SAST). First generation10:13:20Z; last accounting10:33:15Z. Fifteen attempts costUSD0.1893089364; all15 costs corroborated by OpenRouter generation metadata. Four incomplete attempts costUSD0.109956488. Total input177,596; completion249,443 including reasoning222,525. First-dispatch-to-last-accounting1,195.334631 seconds includes pilot/revision pauses; summed request elapsed823.169 seconds. Neither is a measure of financial quality.

## Evidence inspected and preservation

Read actual Stage1, the first section and relevant financial section outputs, original/effective pilot ledger outputs, exact configuration/request scope and all generation receipts/usage via saved scripts. Request payloads checked programmatically for base model/default settings; not every prompt and section answer was independently audited line by line. Raw reasoning was not retained or reviewed. There is no Stage2 final answer to inspect.

Original source: `companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf`,38 physical pages, SHA256 `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`. Hash matched the registered source and remained unchanged. Source tables on pp.8,9,12,13,16,22,24,31 were independently inspected in the preserved prior Codex review `20261028T093647Z_codex_review/audit.md`; no new PDF image inspection is claimed here. Extracted source text was retained for the model; ingestion is not independent inspection of all38 pages. No new market quote, facility contracts, portfolio tape or companion filings were obtained. R0.89 remains a frozen reference only.

Exact originals/hashes are enumerated in `plan.json`; input source, questions, rules, lessons, production snapshot and prior requests/outputs were preserved in `inputs/`. New requests and answers are separate. All production table hashes, source PDF and enumerated originals match their starting state (`preservation.json`). Gemini was not called through any API. No production financial/guardrail data were modified.

## Claims and preliminary findings

All financial amounts below are consolidated NTU Rm, six months ended31March2026 unless explicitly described otherwise. H=historical; D=derived; A=analytical assertion/process observation. C/F IDs apply only to this audit.

| ID | Origin and claim | Class | Primary evidence/check | Verdict/consequence |
|---|---|---|---|---|
| C001 | Runtime default thinking/no Nitro | D | Exact payloads omit reasoning controls; base model slug; saved catalog default_enabled=true/default_effort=high | PASS requested settings. Actual provider routing varied Relace/Fireworks; no proof of an isolated speed effect. |
| C002 | All failed-call costs captured | D |15 receipts and metadata total_cost agree within1e-9; sumUSD0.1893089364 | PASS accounting, not financial correctness. |
| C003 | Full Stage2 completed | D | `receipts/stage2.json`: length,65,536 completion and65,536 reasoning, no delivered final content | FAIL. F001 high process/completeness failure. No valuation can be validated. |
| C004 | All section analyses completed | D | Nine accepted of10 active captures after split; pp.22–24 incomplete, raw source explicitly annexed to Stage1 | FAIL if claimed complete. Source coverage38/38 preserved; no synthetic accepted section answer or ledger closure. F001. |
| C005 | Stage1 POCI gain and NAV | H/D | pp.13,22:3,414+431=3,845; pp.8,16:1,329/780.651033=R1.7024 | PASS arithmetic within evidence coverage. |
| C006 | Stage1 gross/net receivables and ETR corrected | H/D | pp.8,22:497−(395−5)=107; p.9:(−29)/(−92)=+31.52% | PASS calculations; ETR pitfall prose still contradicts the positive calculation, F002 medium. |
| C007 | Stage1 historical-book period corrected | H/D | p.24: FY25 first-half77 + second-half182 = full-year259; current half191 | PASS period arithmetic; no proof of causal acceleration/vintage effect. |
| C008 | Stage1 portfolio/cash lesson fully applied | H/D | p.13 net cash728+116−382−28=434; accounting income383−167+30=246; decline434−246=188 versus p.12 statutory182 leaves6 | NOT VERIFIED as fully repaired. Stage1 drops the false164 comparison but does not complete this explicit bridge. F003 medium. |
| C009 | Stage1 no general-model trade staging applies although policy is not established | A | pp.20,25 policy/short terms/matrix; reviewed conditional ECL rule | NOT VERIFIED as categorical conclusion. Keep conditional, F004 medium. |
| C010 | Debt/lease residuals and ECL-policy uncertainty immaterial | A | pp.8,12–15; residual−3 debt and+11 lease; p.25 allowance5 | NOT VERIFIED materiality assertion without valuation sensitivity/basis. F005 medium; no automatic new blocker either. |
| C011 | Static809 is a forecast funding deficit | H/D | pp.8,13–15,35: stocks differ from dated flows; renewal/availability conditions not independently obtained | FAIL as a deficit inference; new Stage1 correctly avoids that conclusion. Actual funding path remains NOT VERIFIED. |
| C012 | Full DCF/forecast/sensitivity quality | A | No completed Stage2 | NOT APPLICABLE to absent schedules; cannot mark fixed/PASS. |

Selected checks executed by `workflow/changes/20261028_ntu_default_run/check_results.py`, final exit0, actual results in `outputs/independent_checks.json`. Inputs are source-transcribed figures, not extracted model assumptions. Cash−111−61+178=6, opening107 closes113 includingHFS1. Signed CODM components728−383+167+116−30=598 versus printed597, a1 presentation difference; no invented FX/rounding bridge for the separate6 residual. Principal3,975+382−728+383−167=3,845; other702+28−116+30=644. These historical checks do not validate cash-flow forecast classification, terminal financing or fair value.

## Revisions, lessons and handoff

Preserve original pilot failure and runner revision. Compact_v2 reduced section instructions/questions; split_v3 retained all evidence and split pages22–27 into22–24/25–27. One split remained incomplete; explicitly supplying its raw source to Stage1 is coverage recovery, not a successful section generation. No requested reasoning/routing change or caller ceiling escalation occurred within this capped trial. User subsequently explicitly authorized a separate continuation without a caller-set token cap; its results/costs belong in a separate run and must not overwrite these failures.

Confirmed improvement within stated coverage: correct signed POCI/NAV, gross/net residual107, ETR calculation, FY25 total259, conditional forecast assumptions and static-liquidity distinction. Remaining Stage1 errors/omissions F002–F005 require review. No full valuation or claim of exhaustive error detection is supportable. Continue with scoped questions and independently checked schedules rather than adding overlapping broad guardrails. No new SQLite rule is proposed/codified by this process audit.

Manual Gemini review instructions are in `gemini/PROMPT.md`. Gemini should reopen original PDF tables, judge semantic ledger closure and materiality, distinguish absent Stage2 from financial withholding, and save its own versioned audit/calculations. Current ledger12 questions:2 resolved,4 partial,6 open;10 recorded validation attempts include1 rejected and9 valid. Literal validity does not establish semantic closure.

Tool retrospective: seven offline orchestration checks exit0, result checker exit0, metadata refresh exit0 and finalizer exit0. Live invocations stopping on completion exhaustion exited1; these expected failures are preserved rather than labelled success. Immediate metadata404 was resolved by later read-only lookup; no paid resubmission was used to recover accounting. New patterns recorded in TOOL_CHEATSHEET.md section32. No pytest suite was run for this isolated experiment, and previously blocked temporary folders were not deleted.
