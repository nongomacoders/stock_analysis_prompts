# OpenCode (Gemini-role) independent review: one-pass versus three-pass experiment

Evaluator: OpenCode agent (Gemini role), model GLM-5.3-Flash via OpenCode; recorded UTC 2026-10-29T12:36:36Z (Africa/Johannesburg 2026-10-29T14:36:36+02:00).
Decision: **CLARITY BENEFIT REAL; ROBUSTNESS IMPROVEMENT NOT DEMONSTRATED WITHIN COVERAGE; PREMATURE-CLOSURE CORRECTIONS REQUIRED. NO PROMPT/CODE/PRODUCTION CHANGES.**

## Authority and scope
Executed `workflow/changes/20261029_three_pass/gemini_prompt.md` (identical to `20261029T114212Z_three_pass_pan_resume/gemini/review_prompt.md`), output saved to `workflow/changes/20261029_three_pass/open_code_comparision.md` (user-specified filename spelling). Gemini-role review of DeepSeek experiment outputs; prior Codex review of Gemini (`20261029T121151Z_codex_three_pass_review`) examined as a prior reviewer whose claims were re-verified. No paid model calls, no code/prompt edits, no production SQLite writes, no rewriting of raw outputs, no valuation.

## Preservation and inspected coverage
- Verified both source PDFs against plan.json SHA-256:
  - NTU `nutunlimitedcondensedconsolidatedafs31march2026.pdf` = `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`
  - PAN `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` = `62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`
- Verified all 86 input-manifest entries across the two experiment runs (39 resume + 47 original): 0 problems.
- Built this run's own manifest of 42 inspected primary files (`input_manifest.json`, script `calculations/build_manifest.py`): both PDFs, both runs' plan/audit/calculations/claims/findings/metrics/preservation/status/execution/attempts/closure records, all eight canonical outputs (NTU 3 + validations; PAN meaning/movement; PAN why/single + validations), resume requests (why_attempt1 .md), both runs' input manifests, `combined_comparison.json`, `comparison.md`, prior Codex audit/findings/pan_question_comparison.json, `gemini_prompt.md`, `gemini_review.md`.
- Source inspection was on independent renders from the SHA-verified PDFs at `C:\Users\diond\AppData\Local\Temp\opencode\opencode_review_renders\`: NTU_21.png, NTU_22.png, NTU_23.png, NTU_08_hi.png, NTU_13_hi.png, PAN_48_hi.png, PAN_49_hi.png, PAN_50_hi.png (2.5x–3.0x scale; visual digit-level reading).
- Pages actually inspected: NTU physical pp.21, 22, 23 (trial evidence set) plus NTU pp.8 and 13 and PAN pp.48, 49, 50 as independent confirmation only (NOT supplied to the trial models).
- Grep-level absence/presence checks on all staged-pass outputs (25,043|5,763|30,806) for the MTR finding.

## Unread coverage (honest accounting)
Not read line-by-line this turn: original run's individual receipt JSONs and receipts_before_refresh (covered structurally via the 86-entry manifest hash verification and metrics.json), original run requests/ntu_assets_*.json payloads (read .md forms earlier only for single; movement/meaning requests hashed but not re-read), PAN .json request payloads, codex gemini_manifest_checks.json/revision_log/baseline/gemini_finding_assessments full bodies (findings.json and audit.md point 5 were read and re-verified). No valuation-stage files needed.

## Independent calculations
`calculations/reconciliations.py` — 33/33 checks OK, exit 0; outputs `reconciliations.json`. Spans: NTU p.22 column sums (4,458/4,884/4,241/4,859/4,471/5,059) and rows (3,414+431=3,845; concentration 2,371+951+46+46=3,414; 227+141+51+12=431); NTU deltas/percentages (−130/−3.27%, −167/−27.93%, +155/+4.2%, −352/−11.9%, +227/+26.2%); NTU p.13 Note 1 roll-forward 3,975+382−728+383−167=3,845 and 702+28−116+30=644; 3,845+644=4,489=3,178+1,311; PAN FY25 disjoint 92,643+2,654+98,636+1,081+1,513=196,527 vs overlap 197,608; Evander 26,748+1,081=27,829; Group-UG 92,643+1,081=93,724; PAN FY26 65,233+2,428+4,337=71,998 (print 71,997); 40,246+6,609=46,855; 71,997+12,932=84,929 vs print 94,929 (Δ10,000); opsum 282,310 vs 272,310 (with 84,929 → exact 272,310); Group build with 105,478 = exactly 272,310, with 105,479 residual 1 oz; Minning 118,853; single false check 118,853+153,458=272,311; MTR 15,224+52,606+25,043=98,636 (exact) and 25,043+5,763=30,806, 46,164+5,763=51,927; FY25 opsum 83,773+80,435+30,806+1,513=196,527 exact; Elikhulu implied ~684,8xx vs print 68,843; Tennant implied ~1,584,3xx A$/kg and 32,041 US$/oz consistency; p.50 sums (revenue/capex exact; EBITDA leaf-sum 663.0 vs print 663.1); spot percentages (38.6/54.8/5.5/16.7/77.5/859.3/781.3 all verified); FX-only explained ~+13.4pp of the +16.7% US$ AISC rise; full cost/time accounting (ratios 2.2367x/2.3943x cost, 1.6230x/1.7986x time; combined known subtotal $0.0310742712).

## Cost/time summary (independent, complete-bill caveat)
Three-pass: NTU $0.01051743 (29.956s), PAN $0.0111837432 (30.421s); single: NTU $0.00470211 (18.457s), PAN $0.004670988 (16.914s). Resume incremental $0.0094843224 / 24,747 prompt / 5,379 completion / 32.149s. Combined known subtotal $0.0310742712. The original failed-429 request's billing/usage remains unknown; this is not a verified complete bill.

## Key verified model-evidence facts (registers in claims.json / findings.json)
1. NTU staged finals correct on all key deltas/percentages; only in-memory-accepted literal-valid ledger (single rejected on non-literal quote, question stayed open). Both arms failed semantic closure of Q-08aa5c3f257440ab: staged marked resolved via basis quotes without performing 3,845+644=4,489; single never applied closure.
2. PAN staged propagates the false identity 71,997 = 65,233+2,428+4,337 (actual 71,998) through all three passes, and reuses unrevised wrong dictionary entries (capex/revenue-as-cash-flow); why adds unreconciled "largely FX" attribution (≈13.4pp of 16.7pp explicable by FX).
3. MTR 5,763 conflict absent from all staged outputs; only the single raises Q-3e8730dbd1994205 (medium). Gemini and Codex point 5 first clause both refuted on this.
4. FY25 196,527 resolves in-table via disjoint decomposition; neither arm performs it; staged keeps Q-1f48aa6d4b884f09 open.
5. 10,000-oz Barberton/opsum conflict real but unresolved by both arms; conditional agreement with 84,929 does not pick the culprit; single adds a false 272,311≈272,310 "✓" and a false "(0.1 rounding)" on 663.0 vs 663.1; both finals state "inventory timing" as hypothesis-level driver.

## Limitations
- n=1 per arm per case, no randomization/replication, different task wording between arms: cannot isolate staging causally; failure to demonstrate the benefit is not disproof.
- Evidence packs were pp.21–23 (NTU) and pp.48–50 (PAN) only; my p.13/p.8 confirmation never reached the trial models, so "they could have performed it" is limited to what was in-supplied (NTU staged did quote the 3,845/644 rows and 4,489 was in incoming questions).
- Failed-429 cost unknown. Single complete-bill not verified.
- Model identity across arms: deepseek/deepseek-v4.1-flash-1017, Fireworks only, reasoning none/exclude=true, max_tokens 16,384, temp 0.1; constant, so arm-order/dwording effects remain.

## Decision
1. Retain the single-pass production workflow. Three-pass adoption is not justified by this evidence.
2. The demonstrated three-pass weaknesses are propagation of unverified stage artifacts and premature/unperformed-verb closure, not stage count per se. Proposed (not implemented): F011's minimal rule change + one PAN rerun as smallest useful next experiment.
3. Corrections to prior reviewers' records required only on the MTR "both flagged/high-priority" claims (F009); remaining Codex critiques verified.

## Codex handoff
All outputs preserved in place; original experiment outputs untouched; production unchanged (preservation.json true in original/resume runs). Next reviewer (Codex) should start from `input_manifest.json` (42 entries) here, re-verify the MTR grep evidence (F005/F009), the reconciliations.json checks, and the validator-dependent F002 asymmetry, then assess this Gemini-role review against the primary evidence.
