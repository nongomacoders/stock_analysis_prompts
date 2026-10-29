# One-pass versus three-pass: OpenCode (Gemini-role) comparative review

Date: 2026-10-29 (UTC 12:36Z). Reviewer: OpenCode agent, Gemini role, per `gemini_prompt.md`. Versioned audit record: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261029T123636Z_open_code_three_pass_review/` (this analysis = audit.md's narrative; registers: `claims.json`, `findings.json`; independent calculations: `calculations/reconciliations.py`, 33/33 checks OK, exit 0, output `reconciliations.json`).

No paid model calls, no code/prompt edits, no production SQLite writes, and no raw outputs were rewritten. Prior reviewers' records (Gemini `gemini_review.md`, Codex `20261029T121151Z_codex_three_pass_review`) were read and re-verified against primary evidence; corrections to them are explicit below.

## 1. Inputs and integrity

- Both PDFs match plan.json SHA-256: NTU `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`; PAN `62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`. All 86 input-manifest entries across the three relevant run directories verify (0 problems) — original experiment 47, PAN resume 39.
- PAN resume integrity: why request byte-identical to the originally failed 429 request; single request identical to `pan_dense_base.md`; production tables unchanged (`preservation.json` all-true); generation/handoff exit 0; 2 new calls, both succeeded first attempt, backoff (15s/30s) configured but never exercised, 2.23x/2.39x cost ratios unchanged from the original pairing.
- I rendered the source pages fresh from the hashed PDFs and read digits visually: NTU pp.21–23 (trial evidence) and pp.8, 13 (independent confirmation only — never supplied to the trial models); PAN pp.48–50 at scale 3.0.

Model/settings constant across both arms and both cases: `deepseek/deepseek-v4.1-flash-1017`, Fireworks only, reasoning excluded, temp 0.1, max_tokens 16,384.

## 2. Accuracy (arithmetic, signs, measurements) — verified independently

**NTU staged arm (all PASS):** gain −167 (−27.9% vs Sep25), net −130 (−3.27%), YoY +155 (+4.2%), unsecured −352 (−11.9%), Debt review +227 (+26.2%). Column sums on p.22 re-add correctly (gross 4,458; carrying 4,884; Mar25 4,859; Sep25 5,059). p.13 Note 1 (independent confirmation) ties: 3,975+382−728+383−167=3,845 and 702+28−116+30=644; total 3,845+644=4,489=3,178+1,311.

**PAN verified figures:** FY25 disjoint build 92,643+2,654+98,636+1,081+1,513 = **196,527 exactly**; overlapping build 197,608. Evander FY25 26,748+1,081=27,829 and Group-UG 92,643+1,081=93,724 show the 1,081 buy-in is already inside those columns. FY26 Barberton total prints 94,929 vs components 71,997+12,932=84,929 (**Δ10,000**); leaf-column operations sum 94,929+103,330+51,927+32,124=**282,310** vs printed Group **272,310**; substituting 84,929 gives exactly 272,310. MTR FY25 leaf 25,043 vs "Total operations" 30,806 (Δ**5,763** = FY26 MTR buy-in; FY25 buy-in row nil for MTR; FY25 check 15,224+52,606+25,043=98,636 exact). 1-oz differences confirmed: leaf-sum 71,998 vs printed 71,997; 105,479 vs 105,478; 118,852 vs 118,853 — real but tiny, cause not proved.

**Cost/time reproduced:** staged 2.2367x (NTU) / 2.3943x (PAN) cost and 1.6230x / 1.7986x summed request seconds; combined known subtotal $0.0310742712. The original failed-429 billing remains unknown (not a verified complete bill).

## 3. Percentage usefulness

The staged movement pass is clearer (per-basis deltas with positive denominators). Spot percentage checks in the PAN finals are all accurate (38.6/54.8/5.5/16.7/77.5/859.3/781.3). The single's "(0.1 rounding) ✓" on Adjusted EBITDA leaf-sum 663.0 vs printed 663.1 is a false pass on a literal mismatch (FAIL — F007).

## 4. Source scope and ambiguity

- The 10,000-oz conflict and the MTR 5,763 conflict are genuine printed-source conflicts, not model mistakes. Both arms treat them at hypothesis level; **neither establishes which value to replace**. FY25's opsum rows reconcile exactly on printed values (83,773+80,435+30,806+1,513=196,527), so "the pattern says substitute X" is unsafe; the FY26 culprit is case-specific.
- Elikhulu FY25 68,843 ZAR/kg: rebuilding from 1,130.9 ZARm and ~5,309.2 kg sold implies ~684,8xx — consistent with an omitted-digit order-of-magnitude error, but not proved. Tennant FY25 A$1,584,835/kg and US$32,041/oz are mutually consistent with the tiny oz base (~1,584,3xx rebuilt — not obviously a typo). Neither arm demonstrates internal consistency here; Codex's critique on these points verified.
- Group FY26 build works exactly with the printed Group-UG 105,478 column (not the Minning 105,479), so the printed table does contain a consistent column set — which does not tell us which Barberton total is intended.

## 5. Explanations / hypotheses

- Staged PAN final why asserts "the US$ cost increase is largely FX": FX/ZAR roll-up explains ~+13.4pp of the +16.7% Group US$ AISC rise; the rest is consistent with Tennant mix (~11.8% weight) but unreconciled — an over-claim, present only in the staged why.
- Both PAN finals (and the single) put "inventory timing" forward as the produced-vs-sold-open cause without any reconciliation (hypothesis stated as driver both arms).
- The single's false closure check "272,310 = 118,853+153,458 (surface) ✓" (actual 272,311) is a model error, not a source one; and the single mislabels Evander totals 46,855/27,829 as "underground".

## 6. Question quality

- Single PAN: 4 questions, including the unique MTR gap question Q-3e8730dbd1994205 (medium) and a tight AISC-resolution question (high). Staged PAN: 5 questions (Q-1f48aa6d4b884f09, Q-e8c872e6edc94d18, Q-f1a4ce3647724ed9, Q-ced8d2566db6459c, Q-c1e6100f7a674873), **no MTR entry** — the conflict its own source contains never reached its ledger.
- NTU: only the staged arm's final ledger was validated (single's rejected for a non-literal quote), but the staged set also opened a clean reconciliation question (3,845 vs 4,489) it then couldn't answer in-supply. Staged questions are more numerous and better targeted; single questions are sharper on cost/APM scope.

## 7. Semantic closure

- **Q-08aa5c3f257440ab (NTU):** the staged final marked it resolved on p.21/p.22 basis quotes — the closure condition (state the basis *and reconcile to carrying value*) was never performed: 3,845+644=4,489 was computed by neither arm, and the printed p.13 total was out of pack. The literal validator accepted the resolution (numbers were not checked, only literal quote format). The single's attempted closure was rejected as non-literal, so the question stayed open in its in-memory ledger. Original closure from `closure_comparison.json` stands: open with roll-forward pending — neither arm has earned the status change.
- Staged reuse integrity: the movement pass said the dictionary was reused verbatim and hadn't yet been committed; the final why's key-facts table covers largely the same ground as the single's — the extra passes' clarity artifacts do not materially surface in the final reading.

## 8. Literal validation

The validator's functional gap: it rejected the single for a quote-formatting imperfection (`3 414` with spaces) while accepting the staged arm's resolution that lacked required reconciliation. Quote-format literalism without number-checked closure currently allows premature semantic closure in the staged arm — the highest-leverage single fix identified by this review.

## 9. Time and cost

Three-pass costs 2.24x–2.39x more per case and 1.62x–1.80x more in summed request seconds. Nothing in the final outputs' accuracy within the supplied evidence suggests that extra spend was converted into error-catching: every error the extra passes could have caught (71,997/71,998; MTR 5,763; 197,608 vs 196,527; false dictionary entries) was carried through all three passes instead.

## 10. Verdict on three passes

**Within this coverage: three passes improve clarity, not robustness.** Concretely:
- Genuine wins: staged dictionary/worksheet clarity; verified percentages; the only in-memory-accepted literal-valid ledger (NTU); uniquely-last — nothing else in the final deltas beats the single arm.
- Real losses: three-fold propagation of the same false identity (F003); silent drop of the MTR conflict the single flags (F005); FY25 196,527 left unresolved though resolvable from the same table (F004); validator-passed but unperformed closure (F002); wrong dictionary meanings carried to the why (F003).
- Both arms carry their own distinct error sets (`F007` single; `F003/F005/F002` staged), so "average error mass" did not drop.
- **Not isolated causal proof:** n=1 per arm per case, no randomization/replication, arm-order and wording differ. Failing here does not disprove staging in general.

## 11. Errors found in prior reviewers' records

- **Gemini (`gemini_review.md` lines 78–81 and F009 row):** "Both single-pass and three-pass models correctly flagged this mismatch and formulated high-priority questions" — **refuted**: no staged-pass output mentions 25,043/5,763/30,806 (grep-verified across both run dirs); no high-priority MTR question exists in either arm (single's is medium). Gemini's ten-thousand-oz/EBITDA handling (line 24 context) and other findings stand.
- **Codex (`20261029T121151Z_codex_three_pass_review`):** point 5's first clause "Both PAN prose identify MTR5763 gap" is unsupported; its second clause (only the single preserves the question, staged omits, single's priority medium, single-uniqueness not a victory for staging) is correct. Its remaining error critiques (F002/F006/F007 handling, Elikhulu, Tennant) verify.
- Everything else material in both prior reviews survives re-checking; nothing in their raw output files was altered.

## 12. Smallest useful next change (proposed, NOT implemented)

Before more samples, test the mechanism this review isolated: change the ledger contract for both arms so "resolved" requires the closure condition's arithmetic *shown and tying to the final printed value* (for NTU: 3,845+644=4,489), and make the validator check that arithmetic, not just quote literalness. Re-run the cheap in-source recon case (PAN meaning+why, reusing the unchanged movement) under identical settings against the already-preserved outputs. Prediction to test (F011): in-source-completable questions (FY25 disjoint 196,527; 71,998 leaf-sum; MTR 25,043+5,763) get resolved in-pass, and repeated wrong identities get corrected by the source-rechallenge pass. If not, the extra passes' marginal information is genuinely zero and the conclusion hardens.
