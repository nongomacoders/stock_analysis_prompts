# Codex review of Gemini: NTU 1H26

**Conclusion: CORRECTIONS REQUIRED in Gemini's evaluation; INSUFFICIENT EVIDENCE for a validated target or recommendation.**

Gemini identified real errors, particularly cumulative POCI gains mistaken for loss coverage, share capital mistaken for NAV, and duplicate valuation discounts. However, it retained an unsupported asset add-back when describing R1.07 as the corrected SOTP and endorsed STRONG SELL despite rejecting the target that generates that rating. It missed material forecast cash-flow defects. Correct the accounting baseline and rebuild the forecast before accepting either R0.55 or R1.07.

## 1. Inputs, identity, and coverage

- Company: Nutun Limited, NTU; consumer_lending; six months ended 31 March 2026.
- Evaluator: Codex. Exact runtime model identifier/settings are not exposed; no inferred version.
- Run timestamp: directory name and `inputs/manifest.json` contain UTC execution time. Local timezone: Africa/Johannesburg (UTC+02:00).
- Subject: Gemini's `20261027T163950Z_gemini/audit.md`, its manifest, calculation script/output, and the unchanged DeepSeek Stage 1 and Stage 2 outputs.
- Source: `nutunlimitedcondensedconsolidatedafs31march2026.pdf`, 38 physical pages, SHA-256 `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`. Independently matches the read-only SQLite reports baseline.
- All four Gemini input artifact hashes match both its saved inputs and the current corresponding company briefs. Original model outputs, the entire Gemini audit directory, and a read-only guardrail snapshot are preserved in `inputs/`. See `inputs/manifest.json` for exact paths and hashes.
- Extracted all 38 PDF pages programmatically; extraction is not equivalent to inspecting every page. Relevant text inspected: physical pages 3, 5, 8, 9, 12-16, 18-19, 21, 23-24, 26, 28-29, 31, 36. Page 27 was only partially visible in tool output and is not relied upon. Visually inspected rendered pages 23 and 31. Rendered images and extracted text are saved in `calculations/`.
- Inspected the complete Stage 2 note and Gemini's findings/reconciliations/proposals; inspected relevant Stage 1 passages and targeted captured-section/ledger evidence embedded in the Stage 1 prompt. The entire Stage 1 prompt and all section records were not independently reviewed. Stage 2 prompt preserved, not fully reviewed. Raw SQLite section records were not queried.
- No independently timestamped market quote was obtained. R0.90 is Gemini's asserted quote, used only for conditional arithmetic. This review does not validate a current market recommendation. Future facility utilisation, covenant availability, refinancing, and post-March liquidity are not established by the supplied interim report.
- No valuation regenerated, no original model output amended, and no guardrail/database changed.

## 2. Verification register

PASS below means the specific claim is supported within its stated scope, not that the overall valuation passes.

| ID | Claim under review and origin | Classification | Primary evidence / independent check | Verdict and consequence |
| --- | --- | --- | --- | --- |
| C001 | Gemini C001/C002: EBITDA R790m, statutory OCF -R111m; difference R901m | Historical / derived | PDF pp.12,31: -63-29+68+597+1+216=790; -50+3-225+2+182-23=-111 | PASS for reported values and difference; causal EBITDA-to-cash bridge NOT VERIFIED |
| C002 | Gemini C003/C004: principal gross collections R773m, purchases R382m; total purchases R410m | Historical | PDF p.13: principal purchases382 + other28=410; collection footnote773-45=728 | PASS |
| C003 | Gemini F002: R431m is cumulative impairment gain, not conventional loss-coverage reserve | Accounting / historical | PDF pp.13,23-24: 3414+431=3845; 598-167=431; historical loss191 offset by new gain24 | PASS with terminology qualification: source itself calls the column an ECL allowance |
| C004 | Gemini F003: NAV is about R1.70, not R6.90 | Historical / derived | PDF pp.8,16: equity1329/net shares780.651033=1.7024; share-capital5410/shares=6.9301 | PASS. Statutory NAV is not a market fair-value estimate |
| C005 | Gemini F004: amortisation footnote is a net run-off calculation | Accounting / derived | PDF pp.13,31; (728-383+167)+(116-30)=598 vs reported597 | PASS for sign correction; exact R1m residual/rounding explanation NOT VERIFIED |
| C006 | Gemini F005: cost-change brackets represent adverse movements | Historical presentation | PDF p.3: costs820 vs865 shown +5%; international479 vs470 shown (2%) | PASS as an interpretation consistent with table; not independently an accounting error |
| C007 | Gemini F001: 25% applied twice and additional 31.5% haircut | Derived | Stage2 section4: 1114.55/780.7=1.4276; once=1.0707; twice=.8030; then .55 | PASS for arithmetic diagnosis |
| C008 | Gemini F001: R1479m add-back is unsupported and consistent with a book-equity plug | Derived / inference | Stage2 sections3-4: net other assets1315-765=550; unexplained excess929; 4035.55-4400+1479=1114.55 | PASS for mismatch; deliberate intent to force book equity is an inference, not proven intent |
| C009 | Gemini F001/section6: true single-discount SOTP is R1.07 | Derived / valuation conclusion | Same calculation retains disputed1479 add-back | FAIL as validated valuation; PASS only as arithmetic conditional on unsupported inputs |
| C010 | Gemini F006: static SELL differs from STRONG SELL under published bands | Derived | Stage2 JSON: sell ceiling .65; reference .89 and asserted .90 exceed .65 | PASS for internal mismatch; bands' economic validity NOT VERIFIED |
| C011 | Gemini section6: STRONG SELL robustly supported | Valuation conclusion | Invalid target, rejected add-back, erroneous FCFE; no rebuilt valuation | FAIL as validated recommendation; risk evidence can support caution without validating price-based rating |
| C012 | Gemini C011/C012: R809m is proven near-term funding gap | Derived / assumption | PDF pp.5,14:1396-112-475=809; management claims total undrawn~800; no facility roll-forward | PASS arithmetic; NOT VERIFIED as actual funding shortfall/default evidence |
| C013 | DeepSeek FCFE accurately reflects collections/acquisitions; Gemini does not flag it | Forecast / derived | Stage2 section3 deducts principal collections1200 while amortisation add-back1200 cancels it | FAIL. Cash collections are inflows; CODM amortisation must first be reconciled to IFRS profit |
| C014 | DeepSeek forecast cash balances reconcile; Gemini does not flag them | Forecast / derived | Stage2 section3: FY27 opening100 + stated change(-815)=-715, not closing95 | FAIL; unexplained FY27 cash bridge810m |
| C015 | DeepSeek sensitivity matrix follows SOTP; Gemini does not flag it | Derived | Stage2 sections4-5: .05 PBD multiple step implies .18469/share after one25% discount, vs table~.07 | FAIL under stated SOTP mechanics; requires full disclosed transformation to reconcile |
| C016 | DeepSeek: UK+US represents72% of group revenue; Gemini does not flag denominator | Historical / derived | PDF p.36 UK303+US212=515; 515/711 services revenue=72.4%; 515/1599 CODM total=32.2% | FAIL as unqualified group mix; explain IFRS services-only versus CODM denominator |
| C017 | DeepSeek lifetime ECL understatement is established from rolling12-month model wording | Accounting allegation | PDF pp.13,21: lifetime-change policy plus rolling12-month valuation wording | NOT VERIFIED. A question about valuation horizon is supported; definite understatement and direction are not established |
| C018 | Gemini cash-flow table reconciles PBD adjustment188 to reported182 | Derived | Audit section3.2:844-410-246=188, not182 | FAIL as complete reconciliation; unexplained6m remains |
| C019 | Gemini POCI claim covers all purchased book debts | Accounting scope | PDF pp.13,28: principal3845 at amortised cost; other644 at FVTPL | FAIL if read as entire4489 book under identical ECL treatment; separate categories |
| C020 | Gemini's liquidity inputs are exhaustive and 100% of all assets encumbered | Historical / inference | PDF pp.8,15,28: selected assets pledged; other investments81 comprise money-market investments | NOT VERIFIED. Availability/restrictions of81m require checking; do not equate pledged principal book with every asset pledged |
| C021 | Short stop-loss R0.65 protects short entered around reference R0.89 | Trading statement | Stage2 section6, reference .89 and stated short stop .65 | FAIL as described loss-limiting stop; below-entry level lies in profitable direction for a short |
| C022 | Gemini earliest origin for POCI/NAV/footnote errors is Stage1 | Provenance | Stage1 prompt embedded section analysis: lines1661/1733 coverage,1713 NAV,1769 footnote; ledger95/1804 NAV | FAIL as earliest observed origin; errors already appear in captured working papers/ledger |
| C023 | Gemini C010: 19.2% versus18.5% creates a70bps rate difference | Historical / interpretation | PDF pp.21,26 supports both rates and additional risk adjustment to cash flows | PASS for difference; valuation misstatement NOT VERIFIED merely from rate difference |

## 3. Independent numerical reconciliations

Executed `calculations/reconcile.py` using local `.venv/Scripts/python.exe`, exit code 0. Actual results are in `calculations/reconciliations_output.json`. Extraction/preservation script also exited 0. No application code changed; no pytest suite was warranted. Gemini's calculation script was inspected but not executed: it contains hard-coded writes back to its original evaluation files, including its script. Re-executing it would alter the preserved evaluation.

### SOTP: arithmetic repair cannot validate unsupported inputs

All figures Rm except shares in millions and per-share ZAR:

- Components:3845*.55 +644*.70 +250*3 +180*4 =4035.55.
- Net debt:3850+310+335-95=4400. Equity before add-back=-364.45.
- Disputed add-back1479 gives1114.55; model's own net other assets=1315-765=550. Difference929 is unexplained.
- Retaining1479:1114.55/780.7=R1.4276; once25% discount=R1.0707; twice=R.8030; additional haircut to.55=31.5104%; overall haircut=61.4746% (multiplicative, not additive percentages).
- Replacing1479 mechanically with550 gives onlyR.1783 after one25% discount. Omitting the add-back gives negative residual arithmetic. Neither is a proposed fair value: supporting asset valuation, operating-asset overlap, equity optionality, and debt assumptions remain unresolved.
- Gemini's R1.07 therefore cannot be adopted as a corrected target. Its suggested0.32x NAV is an alternative assumption requiring justification, not validation of an already chosenR.55. Its suggestion to lower the PBD multiple must likewise be economically supported rather than reverse-engineered to fit the target.

### Cash flow and cash balances

Statutory OCF reconciles:-50+3-225+2+182-23=-111. Subtract PPE17, intangibles13, lease principal30 to obtain -171 before net borrowing and other investment/financing flows. Interest is already included; do not subtract it again. This is a historical cash measure, not a validated forecast FCFE.

DeepSeek FY27 adds1200 CODM amortisation and deducts1200 labelled principal collections. Cash principal receipts are inflows, not outflows. Moreover, the starting PAT is IFRS while this amortisation is taken from the CODM reconciliation: establish what IFRS PAT already includes before making any add-back. Do not fix this by a blind sign flip. A mechanical sign flip alone moves -880 to+1520, demonstrating sensitivity to the defect, not a corrected cash forecast.

| Period | Opening cash | Stated change | Implied closing | Stated closing | Unexplained reconciling inflow |
| --- | ---: | ---: | ---: | ---: | ---: |
| FY26E |106|-538|-432|100|532|
| FY27E |100|-815|-715|95|810|
| FY28E |95|-845|-750|90|840|

These gaps require financing/disposals/other cash movements and matching balance-sheet entries, not an unexplained positive cash row. FY26 calculation uses the model balance-sheet opening106; statutory cash-flow opening107 includes1 held-for-sale cash. That small scope difference cannot explain the gap.

Gemini's historical PBD calculation188 versus182 leaves6m unexplained. It must be shown as a residual, not described as fully reconciled. Its597-versus598 amortisation residual is plausibly rounding, but unrounded inputs were unavailable.

### Liquidity and accounting scope

R809m is a static comparison of1396 maturing debt against112 cash and475 disclosed undrawn overdrafts at31 March. It is not a time-phased cash forecast. Management discloses approximately800 total undrawn facilities;325 beyond the overdraft figure remains unreconciled, not disproved. If that800 were all available on comparable terms, the same static difference would be484, before future operations and refinancing. Money-market investments81 are another possible resource whose restrictions/availability need checking. Do not stack these illustrative scenarios or assume their availability.

The report explicitly describes lifetime ECL changes and also refers to rolling12-month modelling. The latter warrants clarification about terminal/tail value and methodology. It does not establish the amount or direction of a misstatement. AASB9 paragraphs5.5.13-14 reproduce the POCI lifetime-change approach; its definition of credit-adjusted effective interest rate incorporates expected credit losses at inception. Source headings such as ECL allowance are not themselves wrong; the economic sign and baseline matter.

### Sensitivities and denominator checks

Holding debt, shares, other components and a single25% discount fixed, a.05 change in principal-book multiple moves price by3845*.05*.75/780.7=R.18469. A.5x change in International multiple moves it by180*.5*.75/780.7=R.08646. The published matrix uses roughly.07 and.05, respectively, and does not reproduce its stated central SOTP. Any additional haircut must be explicitly included in the sensitivity formula.

UK+US revenue515 is72.4% of711 IFRS service revenue, but32.2% of1599 CODM total revenue on p.36. The model's group concentration statement needs its denominator labelled; neither basis should be silently substituted for the other.

## 4. Assessment of Gemini's six findings

| Gemini ID | Codex assessment | Required revision |
| --- | --- | --- |
| F001 | Partly supported | Keep duplicate-discount/add-back findings; withdraw R1.07 as validated fair value; label circular intent inference |
| F002 | Supported with scope qualification | Principal-book gain is not conventional loss coverage; preserve actual ECL-allowance table label; separate FVTPL assets |
| F003 | Supported | R1.70 statutory NAV; identify earlier captured-section/ledger origin |
| F004 | Partly supported | Net run-off signs correct; R1m residual plausible rounding, not exact proven reconciliation; origin precedes Stage1 |
| F005 | Supported within inspected table | Explain favourable/adverse reporting convention rather than claim sign error |
| F006 | Supported only as internal inconsistency | Published bands map to STRONG SELL, but bands inherit unsupported target; withhold validated rating |

Additional evaluator defects: unqualified strong-sell endorsement; undisclosed6m cash-bridge residual; overstated scope of asset encumbrance/POCI classification; missing provenance tracing. Its snapshot files and hashes are useful and verified. Its broad claim that every primary input was checked against SQLite is stronger than the demonstrated baseline: PDF baseline was independently checked here; model files are preserved/hash-matched, not thereby financially validated. Original execution transcripts and raw timestamped quote responses were not saved, so full-page inspection and live-quote retrieval cannot be independently proved from the package.

## 5. Lessons, guardrail review, and proposed improvements

Gemini moved toward evidence-based auditing but still repaired selected errors without invalidating their dependent conclusion. Improve DeepSeek at the earliest observable stage: captured-section and ledger classifications for POCI, NAV and footnote signs; Stage1 must reopen and verify them; Stage2 must use a reconciled cash model. Additional generic guardrails alone will not solve propagation.

### Review existing proposals first

1. `ALL-SOTP-DISCOUNT-AND-PLUG-ARITHMETIC` substantially overlaps existing `ALL-SOTP-ARITHMETIC-AND-NO-DOUBLE-COUNT` and `ALL-DCF-REPRODUCIBILITY`. Amend coverage/tests instead of duplicating a rule. Distinct discounts may be legitimate if separate risks and compounded effects are explicit; prohibit duplicate application of the same risk, not every multi-factor valuation. Gemini's R1.07 pass example tests arithmetic only and retains the unsupported add-back.
2. `CONSUMER-LENDING-POCI-GAIN-VS-ECL-RESERVE` is useful with scope/sign qualification. Require note/table sign, acquisition baseline, principal versus FVTPL scope, and lifecycle movement. Preserve source terminology and do not prohibit calling the reported column an ECL allowance. Passing example:3414+431=3845,431 cumulative gain; failing example:431/3414 proves conventional loss coverage. Implement section prompts, ledger and Stage1. It does not duplicate an exact enabled rule in the inspected snapshot, but complements the existing consumer-lending book rule.
3. `ALL-EQUITY-NAV-VS-CONTRIBUTED-CAPITAL` is useful for statutory ordinary NAV. Require parent ordinary equity excluding NCI/preference claims divided by relevant net shares at the measurement date; label adjusted/tangible NAV and reconcile adjustments instead of banning legitimate NAV variants. Pass:1329/780.651033=1.7024 statutory NAV; fail:5410/shares labelled NAV. Implement section prompts and Stage1/2. No exact equivalent enabled rule was found.
4. Existing `CONSUMER-LENDING-PBD-AMORTISATION-EBITDA-ADD-BACK` needs clarification: its blanket prohibition on a non-cash amortisation add-back is too broad for all possible starting metrics. Require a signed IFRS-PAT-to-cash reconciliation, collection inflows, portfolio acquisition outflows and no double counting. An indirect bridge can reverse an actual non-cash expense where appropriate; CODM amortisation must not be assumed to be an IFRS PAT expense. Pass:documented net collections less acquisitions with consistent accounting adjustments; fail:add1200 and deduct1200 collections as an outflow. Implement capture, Stage1 and Stage2 plus evaluator checks. Do not add a duplicate rule before reviewing this wording.

### Proposed new rule: ALL-CASH-ROLLFORWARD-CONSISTENCY

- Sector:all. Title:Forecast cash and financing must reconcile.
- Mandate:For each period, reconcile opening cash plus operating, investing, financing and separately identified FX/scope movements to closing cash on the forecast balance sheet. Reconcile new financing to debt/equity and dilution; unresolved material residuals fail validation.
- Confirmed failure:FY27 model implies closing-715 while reporting95, residual810.
- Trigger:any forecast cash-flow and balance-sheet pair. Inputs:both tables, cash definition, borrowing/equity movements and FX/scope adjustments.
- Exceptions:rounding within a stated tolerance, restricted versus unrestricted cash or held-for-sale changes only with explicit bridges. Avoid double counting overdrafts classified inside cash equivalents.
- Pass example:opening100 + OCF20 - capex10 + financing5=closing115. Fail example:100-815=95 without810 reconciliation.
- Implementation:Stage2 prompt and numeric evaluator validation; include deliberate inconsistent-cash fixtures when implemented.
- Duplicate review:existing cash-flow classification rule covers subtotal definitions, not this cross-statement identity; no exact equivalent found in enabled snapshot.

### Proposed new rule: ALL-SENSITIVITY-REPRODUCIBILITY

- Sector:all. Title:Sensitivity cells must recalculate the valuation.
- Mandate:Generate each cell from the same documented base valuation, changing only named inputs. Central case must reproduce the base target within a declared rounding tolerance; preserve debt, shares, discounts, and all valuation bridges unless explicitly varied.
- Confirmed failure:NTU matrix derivatives/base do not match the stated SOTP.
- Trigger:any sensitivity table. Inputs:base formula and every adjusted parameter.
- Exceptions:nonlinear valuation is permitted when the actual nonlinear formula is used; no requirement for constant derivatives. Avoid imposing a derivative from one methodology on a differently disclosed model.
- Pass example:under this SOTP, moving PBD multiple by.05 changes equity value by192.25 before discount, price by.18469 after one25% discount. Fail example:same inputs produce.07 without disclosed transformation.
- Implementation:Stage2 generation and evaluator numeric checks. Existing SOTP rule overlaps arithmetic generally; extend it rather than add a separate rule if preferred.

## 6. Decision, revision record, and handoff

- Independent outcome:Gemini's review requires correction; target and rating remain NOT VERIFIED. Negative reported OCF, losses, impaired-portfolio judgement, and refinancing exposure are supported risks; they do not alone establish an equity price target or STRONG SELL threshold.
- R0.55/referenceR0.89 implies-38.20% conditionally; R0.55/GeminiR0.90 implies-38.89% conditionally. Neither is validated forecast return; forward zero dividend is a model assumption, while no current-period dividend is a historical disclosure.
- Next:correct captured evidence/ledger and Stage1; reconstruct portfolio cash/forecast financing; rebuild SOTP and sensitivities; then regenerate Stage2 and evaluate Gemini again. No rerun performed during this review.
- Retain all original findings and this review as separate versions. No substantive conclusion was silently reversed in this run. The calculation draft contained a duplicate sensitivity dictionary key; it was corrected to separate PBD/International labels and rerun before delivery. Actual output is authoritative for what executed.
- New/proposed rule changes are not codified. User review is required under the repository codification gate.
- Handoff: `inputs/manifest.json`, preserved Gemini directory and DeepSeek briefs, `calculations/reconcile.py`, `calculations/reconciliations_output.json`, `calculations/source_pages.txt`, and rendered physical pages23/31.

External primary accounting reference inspected: https://standards.aasb.gov.au/aasb-9-feb-2025 (paragraphs5.5.13-14; definition of credit-adjusted effective interest rate). Original IFRS-hosted full-standard PDF redirected to a subscription page; AASB's published equivalent was used. Company's online report search corroborated availability, but opening it failed; numerical financial evidence above comes from the hash-verified local PDF.