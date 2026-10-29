# NTU1H26 — Codex review of the logical-capture trial

**Decision: capture execution supported within stated coverage; CORRECTIONS REQUIRED for Stage1; Stage2 INCOMPLETE. No new valuation published.**

Evaluator: Codex; exact runtime model/settings not independently exposed. Review UTC 2026-10-28T14:50:27.375222+00:00; local SAST 2026-10-28T16:50:27.375222+02:00. Subject: `20261028T141038Z_deepseek_reviewed_logical`. DeepSeek base snapshot was requested without Nitro,reasoning controls,provider speed/order overrides or caller-set completion ceilings. Actual providers varied; default catalog thinking enabled/high is not proof of identical provider behavior.

## Preservation and evidence coverage

Exact new requests,raw/effective outputs and receipts for full and pilot phases were copied into this review before corrections; original paths/hashes are in `inputs/manifest.json`. A read-only SQLite backup preserves the full ledger and capture metadata. Earlier sources/model outputs remain unchanged. Source PDF: `companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf`,38 physical pages,SHA256 `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`; matched registered original. All production table fingerprints and enumerated source/original hashes matched initial state.

Inspected reviewed plan,source/capture coverage,request settings and all29 receipts programmatically; read the three pilot briefs,repair and scope recheck; read relevant full section briefs and Stage1 summary,portfolio/cash comparison,matrix and handoff. Other full section outputs are preserved but not all independently read line by line. No Stage2 final answer exists to read. No new full-PDF image inspection is claimed: relevant unchanged primary tables were inspected in prior Codex reviews against this identical hash; physical pp.12–13,22,24–25 are the key source basis here. Receiving38-page source text is not independent full-PDF verification. No current quote,companion reports,portfolio tapes,facility contracts or management forecast was obtained. R0.89 is a frozen reference only.

## Claim register

H=historical disclosure,D=derived arithmetic/process,A=analytical assertion. Financial figures are consolidated NTU Rm,H1FY26 unless labelled otherwise.

| ID | Claim/origin | Class | Evidence and actual check | Verdict/consequence |
|---|---|---|---|---|
| C001 | Reviewed source coverage | D |24 captured units,38 physical pages exactly once;22 financial units and2 navigation/contact units | PASS coverage,not semantic completeness. No synthetic navigation analyses. |
| C002 | Pilot fixed known accounting pitfalls | H/D | pp.21–25:3414+431=3845;FY25 historical77+182=259;trade374−5=369;conditional ECL | PASS within narrow checks. No target/forecast validity established. |
| C003 | Initial page25 pilot covered all material content | D | Raw pilot calls source trade-table-only despite currency note start on same supplied page | FAIL initial answer. Revised scope recheck and full page25 brief include currency/hedging/60-day terms and Pending p26; correction supported,F001. |
| C004 | Pilot/full ledgers independent | D | Pilot DB separate;full started with fresh10-question seed and ran in report order | PASS design. Intentional repeat of pilot captures in full is separately billed,not imported foreknowledge. |
| C005 |22 full section generations valid | D |22 complete responses,22 valid ledger attempts,zero repairs | PASS execution/literal presence;closure semantics remain reviewable. |
| C006 | Full workflow completed | D | Stage1 completed;Stage2 finish_reason length,131072 completion=131072 reported reasoning,no final content | FAIL end-to-end completion,F002. This is not a completed WITHHELD decision. |
| C007 | Costs complete | D |29 unique generation IDs;response cost equals generation total_cost;sumUSD0.2786526252 | PASS accounting. FullUSD0.2445611328,pilotUSD0.0340914924. No missing cost fields. |
| C008 | Stage1 portfolio cash differenceR370m | H/D | pp.12–13:4677−4489=188 decrease;statutory movement182;remaining188−182=6. Net cash434−accounting income246=188 | FAIL,F003. Unsupported sign/scope amount first observed in Stage1,not earlier section briefs. No issuer error or valuation impact inferred from unexplained6. |
| C009 | Stage1 historical POCI/net receivables/period anchors | H/D | pp.8,13,22,24–25:3414+431=3845;497−(395−5)=107;77+182=259 | PASS selected arithmetic only. Current half191 is not an annual result. |
| C010 | Static liquidity subtraction proves a funding shortfall | A | pp.8,13–15,35:stock comparison omits dated operating/replenishment/financing flows and conditions | FAIL as an inference;new Stage1 appropriately avoids that conclusion. Actual forecast funding path NOT VERIFIED. |
| C011 | Some matrix pitfalls were actual current-section claims | A | Raw source-question text requests correct NAV/FCF calculations;matrix phrases tested pitfalls as initial assertions | NOT VERIFIED attribution,F004. Label risks/prior-run errors separately from actual present assertions. |
| C012 | Forecast/DCF/sensitivity/rating defects repaired | A | No Stage2 answer or computed target/forecast schedules | NOT APPLICABLE. Cannot mark absent work PASS/fixed. |

## Independent calculations and preliminary checks

Executed `report_trial.py` and this review checker,actual exits0; source-transcribed historical results and accounting assertions saved in `calculations/actual_results.json` and preserved full `independent_calculations.json`. The preliminary `StockEvaluator.audit` ran against the explicit experimental note path on a DB copy with networking disabled; result MISSING_NOTE,as expected. It did not inspect a production/baseline valuation as if it were new and did not request a live quote. Script success is not financial validity.

Cash/portfolio: principal3975+382−728+383−167=3845;other702+28−116+30=644. Combined net cash728+116−382−28=434;portfolio income before funding383−167+30=246;434−246=188 carrying decline. Compare with statutory182 to leave6 unexplained; do not subtract a negative balance delta from a positive decrease to invent370. Source mapping/FX/scope still require evidence,not a plug. Historical closing cash107−111−61+178=113,includingHFS1 versus balance-sheet112. NAV1329/780.651033=R1.7024;tax expense−29/PBT−92=+31.52%;signed CODM components728−383+167+116−30=598 versus printed597. These do not reconstruct a forward valuation.

## Findings and dispositions

- **F001,medium,section coverage:** initial pilot omitted secondary currency content and recreated an answered POCI question. Original retained. Run-only secondary-heading list,resolved-ID index and shorter exact quote locators were added;scope recheck and full p25 output support correction. This does not prove every cross-page dependency/closure is correct.
- **F002,high,process:** upstream stopped Stage2 at131072 tokens,all reported reasoning. No cap was sent; which router/provider/account limit produced that threshold was not independently established. Generation took286.947s andcostUSD0.06803556. No completion escalation/recovery brief/extra paid retry followed. We cannot infer the internal reason for exhaustion or attribute it to F003,provider,prompt size or telemetry from these records.
- **F003,high,Stage1 regression:** unsupportedR370m versus scoped remaining6. Claimed amount differs by364,but that is not a quantified valuation misstatement. Correct Stage1 arithmetic before downstream use;original answer/request preserved. No Stage2 text exists to establish propagation.
- **F004,medium,attribution:** distinguish a tested pitfall or historical error from a claim made in this run. Avoid invented accusations in verification tables. Effect on valuation unquantified.

Full run:24 attempts,23 complete generations,zero section repairs;USD0.2445611328;193159 input,312161 completion including284949 reasoning;wall1152.42155s (19m12.42s),summed request1027.968s. Pilot:5 generations (3 captures,1 quote repair,1 scope recheck),USD0.0340914924;21717 input,36668 completion including32013 reasoning;wall359.508497s includes revision/review pause,summed request132.052s. Reasoning is already in completion totals. Providers,routes,groupings and prompt changes limit causal comparisons;do not claim lower cost or universally better accuracy.

## Handoff and next work

Capture execution improved within this run;global synthesis reliability and numerical checks remain unresolved. The full ledger has17 records:4 open,11 partial,2 resolved. Literal validation is not semantic closure. Full/first draft plan counts differ deliberately:30 automatic units→24 reviewed units,of which2 are navigation-only. These are source-specific review choices,not a universal fixed-page rule.

No new price/recommendation/returns are supportable because Stage2 is absent. No financial SQLite rule was added. Next engineering candidates are deterministic reconciliation of signed Stage1 tables before Stage2 and smaller linked Stage2 schedules;these are proposals,not implemented amendments or authorized new paid runs.

Manual Gemini instructions are in the subject run's `gemini/PROMPT.md`,including source path/hash,cost evidence,F003 and the absent Stage2 limitation. Gemini should review available section/Stage1 outputs independently,not invent a final valuation to evaluate. Codex then reviews Gemini's preserved audit. All original reports/model answers and production data remain preserved.

Tool retrospective: plan/transport/preservation checks exited0;pilot/scope check exited0;full live invocation exited1 solely on recorded incomplete Stage2;reporting and this checker exited0. One expected literal-quote repair retained. No shell/encoding/permission error or unexplained transmission occurred. No application model defaults changed,no paid Gemini calls,no temporary pytest directories created this turn. New prompt/ledger continuation lessons are recorded in TOOL_CHEATSHEET.md.

Finalization note: a multi-file documentation patch failed context verification before writing; bounded corrected hunks applied successfully. No policy/permission denial occurred. Pilot status was finalized from its saved last receipt and semantic gate; raw receipts/model outputs remained unchanged. Final manifest and production/source checks passed.
