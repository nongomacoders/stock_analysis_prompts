# Concise section reading brief

## Authorized refinements and full NTU section trial

After Codex reviewed Gemini's pilot findings,three small wording changes were
approved and applied:keep signed equations/units consistent in prose and ledger;
flag source-unit/number-format conflicts rather than silently rescale;distinguish
first-time comparative presentation from demonstrated error or policy change.
The consumer-lending note now explicitly excludes ordinary Stage1/2 SICR migration
demands for POCI while retaining relevant recovery/measurement/credit-risk questions.
No PDF splitting,ledger-schema or stage-setting changes were made.

Fresh NTU1H26 section-only trial:
`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T171901Z_ntu_refined_sections/`.
24 retained captures cover38 physical pages once,22 analysis calls completed through
Fireworks,ledger initially empty.18 deltas validated;4 rejected deltas remained
unapplied,including7 proposed new questions. Raw briefs and rejected changes remain
available;this is not22 accepted ledger updates.32 persistent questions:15open,
15partial,1contradicted,1resolved. No repair calls,Stage1/2 or valuation.

CostUSD0.0702026388,all22 costs corroborated by metadata. Input151251,completion51535,
reasoning0,cached input23564;request time208.174s,first-dispatch-to-last-accounting
340.451335s. Production section settings:none reasoning,16384 cap,Fireworks only.
Changed provider/prompt/seed state prevents controlled comparison with old full runs.

Limited original-page review13,22,24,25,31 found remaining header/cell merging,
POCI sign interpretation,FX-period mapping and invented reconciliation-operator
errors. Literal quote matching and source-page presence do not validate these
interpretations. The simpler first pass remains useful,but financial corrections
and manual review are still needed. See the run's audit.md and gemini/PROMPT.md.
Targeted offline checks27 passed in15.64s,exit0;test folder cleaned. Last full app
suite226 passed exit0 from the prior shared-prompt implementation.

The app assembles one shared task from
`prompts/common/12-analyst-reading-brief/v1.1.0/prompt.md`,then adds short sector
notes from the corresponding sector's `prompt.md`. These notes suggest relevant
drivers; they are not mandatory disclosure checklists. Original longer templates
are preserved under `workflow/changes/20261028_section_prompt/before/`.

The four outputs are material facts/figures;footnotes,qualifications and useful
reconciliations;answers/questions and next evidence;and ledger changes. A factual
summary is allowed. Keep periods,units,measurement bases and physical pages visible.
Questions should identify material evidence needs,allow benign explanations and
avoid unsupported allegations. No new question is required for every capture.

The common task applies across companies. Current sector notes cover mining,
retail,consumer lending,finance,REITs,IT,telcos and construction. New sectors retain
the onboarding requirement for dedicated sector files,which now hold concise
reading aids. The orientation templates and local PDF boundary planner are unchanged.

Captured evidence remains unchanged. Context includes the report map,selected
text,pages and existing questions;available native heading observations now expose
secondary note starts on shared pages. Page presence is not proof the model covered
every topic. Continuations remain Pending. Missing text is not a report omission.

Automatic captures use the existing JSON ledger schema with stable IDs and literal
current-capture evidence;manual/legacy captures keep their Markdown ledger.
Existing saved responses/prompts are not bulk migrated. New builds use the shared
task;source metadata records both common and sector template hashes. Ledger
validation checks evidence presence and structure,not the truth of an answer.

## Paired pilot,2026-10-28

Four captures were each run once with old and revised prompts through Fireworks,
fallback disabled,reasoning none and16384 completion cap,matching production
section settings. NTU:p13 andp25;PAN:p38–39 andp48–50. Source hashes verified;no new
PDF image inspection or full chronological rerun. Eight calls completed,total
USD0.0300091344,all costs corroborated by generation metadata.

Revised/old:4/4 versus3/4 valid ledgers;12 versus26 proposed questions;90892 versus
109642 prompt characters. Summed call times39.280 versus55.522 seconds and costs
USD0.0128405676 versus0.0171685668. Calls were not randomized and cached usage differed;
these sample measurements are not universal cost/speed/financial-quality guarantees.

Remaining errors include a copied FV sign error in a revised NTU ledger despite
correct prose,an inappropriate POCI staging question,and unsupported policy/change
interpretations. PAN column ownership still needs original-table inspection. All
outputs remain preserved and reviewable;no financial guardrails or valuations were
changed. This is a simpler first-pass brief,not a financial-validation gate.

Run/audit:
`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot/`.
Manual Gemini prompt is in that run's `gemini/PROMPT.md`;no Gemini API calls made.

### Native extraction follow-up

The native extractor now anchors columns on numeric body cells and native vertical
rules, places wrapped headers by overlap, and keeps broad prose out of table-column
inference. The ledger contract requests short literal cell/sentence anchors;
validation and atomic rejection remain unchanged. No company-specific branches.

The five-case follow-up (NTU13/21–23/24/25, PAN48–50) completed5/5 generations and
validated5/5 deltas for USD0.0199752336. NTU's5/390 cells and comparative FX dates
are correctly read. Impairment sign interpretation and PAN grouped-header/overlap
errors remain; literal validation is not semantic closure. This is selected-case
evidence, with extraction and anchor wording changed together, not universal
financial validation. Full offline suite232passed,exit0.

Audit and manual Gemini handoff:
`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T182010Z_native_extraction_pilot/`.

### Clarifications after independent review (2026-10-29)

The common task now explicitly checks overlapping subtotals before aggregation and
keeps partly answered questions partial when essential evidence is pending or
deferred. The structured ledger contract repeats that closure condition. Consumer
notes distinguish a decrease in a disclosed cumulative POCI gain added to book
value from a conventional reserve release, and separate acquired-book gains from
historical-book losses. These refine existing guidance; validation logic is unchanged.

Targeted offline checks27passed,exit0. Exact prior wording and implementation record:
`workflow/changes/20261029_prompt_clarifications/`. At implementation time, no paid
comparison had tested the new wording; improved model behavior remained unverified.

The subsequent three-case same-input comparison was mixed: all3 generations
complete,2/3 valid deltas,USD0.0130756248. NTU24 sign interpretation improved, but
NTU21–23 still inverted the gain movement and proposed premature closure; its delta
was rejected for literal quotes shorter than8characters. PAN avoided the old
double-counted sum without completing the reconciliation and introduced a row
mix-up. One generation per case does not demonstrate robust repair. Audit and
manual Gemini handoff:
`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261029T070527Z_prompt_clarification_pilot/`.
