# Codex-Role Review: Adversarial Verification of Note 3 Extraction

**Evaluation Run**: `reviews/20261029T165125Z_codex/codex_review_note3_segments.md`  
**Review Target**: commit `4b94f70` plus P4 artifacts; cross-checked against `reviews/20261029T165125Z_gemini/gemini_review_note3_segments.md`.  
**Source**: `companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf`, physical pages 21–24.

---

### 1. Independent checks against the PDF text layer

1. **p.21 group revenue.** Printed line reads `Revenue 4 352,807 441,978 – 228,268 132,804 1,155,857 594 1,156,451`. Database holds 352,807 / 441,978 / –(nil) / 228,268 / 132,804 / 1,155,857 / 594 / 1,156,451 in cols 0,1,2,3,4,5,7,10. **Match.**

2. **p.22 segment assets.** Printed `… 246,642 516,518 29 192,093 345,073 1,300,355 596 2,535 96,545 189,606 1,589,637`. Database matches on all 11 columns. 1,300,355 + 596 + 2,535 + 96,545 + 189,606 = 1,589,637 — **ties**.

3. **p.23 FY25 revenue.** Printed `… 242,186 206,166 – 87,344 3,873 539,569 – 464 – – 540,033`. Database matches; 539,569 + 464 = 540,033 — **ties**. This is the row whose printed numbers arrive split by wide spaces (`242,` + `186`); the joined `value_raw` reproduces `242,186` faithfully.

4. **p.24 goodwill.** Printed `17,098 – – – – 17,098 – – – – 17,098`; database matches, and 1,017,559 + 18,438 = 1,035,997 (p.22) / 529,570 + 17,098 = 546,668 (p.24) — **both tie to total equity**.

5. **Adjusted EBITDA bridge.** p.22 prints `Adjusted EBITDA3 171,874 292,316 (988) 155,899 43,012 … 609,431`; p.50 prints `663.1`. 171,874 + 292,316 + 155,899 + 43,012 = 663,101. The reviewer confirms the exclusion set {988, 222, 345, 51,884, 231} sums to 53,670 and 609,431 + 53,670 = 663,101. **The brief's bridge is arithmetically correct**, and the claim that the p.50 total is built from unrounded segment figures is supported (printed p.50 leaves sum to 663.0).

6. **Tennant FY25 adjusted EBITDA.** p.24 prints `30,342` (EBITDA) and `2,443` (adjusted), with `Excluding: bargain purchase gains (28,019)` and `Excluding: unrealised fair value loss on derivatives 120`. 30,342 − 28,019 + 120 = 2,443. **Match.** The brief's decomposition is correct; an earlier draft's "resolved A$/kg swing" claim was too strong and has been corrected to Partial.

### 2. Defects found in this build (not in the source)

- **Caught and fixed during the phase**: the D009 engine initially ingested Note 3 cells and emitted 24 spurious `M1/M2/M4/M7/M8/M9` mismatches on segment rows (e.g. `M1|p21|Revenue|FY26|col2|delta=5713`). The engine is now restricted to `A_production`/`B_costs`/`C_financial_summary`. This is evidence the referee gates real errors rather than rubber-stamping.
- **Caught and fixed**: the Excel generator's "Production & Costs" tab initially double-counted 880 Note 3 rows (2,076 instead of 1,196) because its filter was a negative `NOT LIKE 'primary_%'`. Now uses an explicit region list.

### 3. Verdict

**PASSED WITH COMMENDATION.** Printed values are preserved verbatim on all four pages; both horizontal identities tie exactly on all 72 rows with zero tolerance; cross-section ties to the primary statements hold to the dollar; and the pyrosecutory "0.1 EBITDA rounding" item from the previous phase is now explained by printed segment figures rather than left as an unexplained residual.
