# Gemini Independent Evidence Audit: Nutun Limited (NTU) 1H26

**Evaluation Verdict:** **VALUATION WITHHELD — MATERIAL ISSUES UNRESOLVED; CORRECTIONS REQUIRED FOR MODEL PIPELINE**  
**Evaluation Timestamp (UTC):** `2026-10-28T09:25:00Z`  
**Evaluation Local Time:** `2026-10-28T11:25:00+02:00` (Africa/Johannesburg)  
**Evaluator:** Gemini (`Gemini 3.8 Flash (High)`, executing locally in Antigravity)  
**Subject Run Evaluated:** `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T081850Z_codex_workload_comparison`  
**Primary Source Document:** `nutunlimitedcondensedconsolidatedafs31march2026.pdf` (38 physical pages; SHA-256 `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`)  
**Stage 2 Result Classification:** `WITHHELD_RECOVERY_BRIEF_FULL_VALUATION_INCOMPLETE`  
**Audit Path:** `C:/Users/diond/Desktop/Projects/stock_analysis_prompts/companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T092500Z_gemini/audit.md`  
**Supporting Calculations:** `C:/Users/diond/Desktop/Projects/stock_analysis_prompts/companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T092500Z_gemini/calculations/reconciliations.py` (Outputs in `calculations/reconciliations.json`)

---

## 1. Executive Summary & Operating Scorecard

### NTU — Institutional Valuation Scorecard (1H26)

**Audit Status:** ⚠️ `WARNINGS_FOUND` &nbsp;|&nbsp; **Sector:** `consumer_lending` &nbsp;|&nbsp; **Valuation Status:** **`WITHHELD`** &nbsp;|&nbsp; **Dynamic Rating:** **`WITHHELD`**

| Metric | Valuation Determination | Live Market Comparison & Basis |
| :--- | :---: | :--- |
| **Live JSE Price (`NTU.JO`)** | **R0.89** | Frozen stored baseline reference (not a verified live quote) |
| **Note Reference Price** | R0.89 | Baseline reference price in valuation note |
| **12-Month Target Price** | **`null` (WITHHELD)** | Target withheld under `ALL-MATERIAL-ISSUES-VALUATION-WITHHOLD` |
| **Live Implied Upside** | **`null`** | Valuation withheld pending material refinancing/covenant resolution |
| **Forward Dividend Yield** | **`null`** | Cash dividends suspended since FY2023; forward yield unmodeled |
| **12-Month Expected TSR** | **`null`** | Derived return metrics withheld |
| **Recommendation** | **`WITHHELD`** | Note static: `null` (Dynamic Bands: `null`) |
| **Dynamic Rating Bands** | Strong Buy: `null` \| Buy: `null` \| Hold: `null` \| Sell: `null` \| Strong Sell: `null` | Rating bands cleared under publication gate |

---

### Forensic Audit Checks

| Check Code | Check Description | Result | Details / Observations |
| :--- | :--- | :---: | :--- |
| **`CHK-PRICE-SYNC`** | Market Price & Upside Alignment | **[⚠️ FLAG]** | Reference price R0.89 frozen; upside is null because valuation is withheld. |
| **`CHK-BANDS-MONO`** | Rating Bands Monotonicity | **[✓ PASS]** | Null bands emitted under the mandatory withholding contract. |
| **`CHK-SOTP-MATH`** | SOTP Vertical Arithmetic & Sign Integrity | **[✓ PASS]** | SOTP target is withheld; no unverified working-capital additions or double discounts. |
| **`CHK-GUARDRAILS`** | Active Sector Guardrails Compliance | **[✓ PASS]** | Fully complies with `ALL-MATERIAL-ISSUES-VALUATION-WITHHOLD`, `ALL-SHARE-COUNT-ANCHOR`, and `CONSUMER-LENDING-POCI-GAIN-VS-ECL-RESERVE`. |
| **`CHK-TEXT-CLEAN`** | LLM Stutter & Format Cleanliness | **[✓ PASS]** | Output markdown is clean; no token loops, repetitive phrasing, `<br>`, or `<span>` tags. |

---

## 2. Scope, Preservation, and Execution Audit

### 2.1 Evaluated Scope and Physical Page Coverage
The evaluated DeepSeek trial processed all 38 physical pages of the Nutun Limited Condensed Consolidated Financial Statements for the half-year ended 31 March 2026 across 9 captured sections:
- Section 1 (`section_9a19b3b4_001`): Remainder coverage (physical pp. 1–2).
- Section 2 (`section_9a19b3b4_002`): Highlights part 1 (physical pp. 3–6).
- Section 3 (`section_9a19b3b4_003`): Highlights part 2 (physical p. 7).
- Section 4 (`section_9a19b3b4_004`): Primary financial statements part 1 (physical pp. 8–15).
- Section 5 (`section_9a19b3b4_005`): Primary financial statements part 2 (physical pp. 16–21).
- Section 6 (`section_9a19b3b4_006`): Primary financial statements part 3 (physical pp. 22–27).
- Section 7 (`section_9a19b3b4_007`): Primary financial statements part 4 (physical pp. 28–33).
- Section 8 (`section_9a19b3b4_008`): Primary financial statements part 5 (physical pp. 34–37).
- Section 9 (`section_9a19b3b4_009`): Remainder coverage (physical p. 38).

Independent physical pages inspected in this review: **pp. 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 31, 34, 35, 36, 38**.

### 2.2 Stage 2 Execution Reality: Token Exhaustion vs Withheld Recovery Brief
The trial attempted a full institutional 2-year forecast and valuation model in Stage 2 (`requests/stage2.md`). 
- **Attempt 1:** Exhausted the completion limit at 65,536 tokens (`outputs/stage2_incomplete_attempt.json`).
- **Attempt 2 (Headroom Retry):** Exhausted the completion limit again at 98,304 tokens (`outputs/execution_status_before_handoff.json`, `IncompleteCompletionError`, `finish_reason: length`).
- **Recovery Fallback:** Because the full valuation failed to complete within its token budgets, the comparison runner invoked a separate recovery prompt (`requests/stage2_withheld_brief.md`), directing DeepSeek to produce a concise (<2500 words) research brief with `valuation_status: "WITHHELD"` and null valuation fields.
- **Critical Analytical Distiction:** The resulting `outputs/stage2_withheld_brief.md` is a **separately commanded recovery brief**, NOT an autonomous full valuation that completed a forecast model and then decided to withhold. DeepSeek correctly recognized in Stage 1 that the valuation should be withheld, but its full Stage 2 valuation attempt exhausted 98,304 tokens and failed to produce a final answer.

### 2.3 Questions Ledger Integrity & Local Open-Only Fallbacks
In `experiment.sqlite`, the new workload reliability infrastructure enforced strict quote verification on ledger JSON delta updates:
- **Attempts:** 24 response attempts were evaluated; **15 were rejected** and 9 were valid.
- **Rejection Causes:** DeepSeek repeatedly hallucinated markdown formatting inside `evidence.quote` (e.g. inserting markdown table pipes `|`, modifying whitespace, or truncating clauses) or emitted malformed JSON syntax.
- **Local Fallbacks Triggered:** 5 sections (`section_9a19b3b4_004`, `005`, `006`, `008`, `008`) triggered `local_open_only_fallback`. In these sections, DeepSeek's proposed resolutions and updates were discarded, and questions were forcibly kept OPEN.
- **Ledger State:** Out of 69 question records in the suite, **68 remained open**. The only question resolved was `Q-47cc084806ec463d` (confirming page 38 is corporate administration information only).
- **Integrity Assessment:** The ledger validation software successfully protected database integrity by rejecting unverified closures. However, DeepSeek's inability to quote verbatim without markdown artifacts prevented legitimate evidence updates from resolving open questions.

---

## 3. Claim Verification Register (C001 – C025)

The register below preserves stable IDs from prior reviews and extends them for this workload comparison trial.  
*Classifications:* `H` = Historical result; `M` = Management explanation; `G` = Forward guidance; `A` = Model assumption; `D` = Derived calculation.

| Claim ID | Claim Origin & Statement | Class | Primary Evidence & Location | Independent Check / Calculation | Verdict | Consequence & Finding ID |
| :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| **C001** | Stage 1 §1/§2.2, S2 brief: R431m is a cumulative impairment gain on POCI assets, not a loss reserve; 12.6% is gain/gross. | `H`/`D` | PDF p. 13 (Note 1), p. 22 (Note 6.2). Gross R3,414m + Gain R431m = Net R3,845m. | `431 / 3414 = 12.624%`. Positive gain added to gross. Script `reconciliations.py`. | **PASS** | Corrected from early baselines. Substantive improvement maintained. Linked: **F005**. |
| **C002** | Stage 1 §1/§2.8, S2 brief: Statutory NAV is R1.70 per share, based on equity R1,329m / 780.651m net shares. | `H`/`D` | PDF p. 8 (SoFP equity R1,329m), p. 16 (Note 4 stated capital; net shares 780,651,033). | `1329 / 780.651033 = R1.7024`. Distinct from contributed capital R5,410m (R6.93/sh). | **PASS** | Corrected from early baselines; prevents contributed capital confusion. Linked: **F005**. |
| **C003** | Stage 1 §2.3, S2 brief: CODM amortisation R597m footnote (p. 31) reconciles by rounding to 598. | `D` | PDF p. 13 (Note 1.1), p. 31 (Note 7 footnote). Components: 728, 383, 167, 116, 30. | `728 - 383 + 167 + 116 - 30 = 598`. Delta to printed 597 is R1m rounding. | **PASS** | Correct signed formula verified; old false allegation of -R366m eliminated. Linked: **F005**. |
| **C004** | Stage 2 withheld brief: Arbitrary valuation plugs and double discounts eliminated. | `A`/`D` | `stage2_withheld_brief.md`, `stage2_publication.md`. Target is withheld. | No ungrounded EV plug or unverified multiples asserted. | **PASS** | Replaced unverified valuation with clean withholding. Linked: **F006**. |
| **C005** | Stage 1 §2.6, S2 brief: Cash flow statement PBD movement of R182m does not reconcile to Note 1.1 net collections less additions (R346m). | `H`/`D` | PDF p. 12 (SoCF PBD R182m), p. 13 (Note 1.1: collections R728m - additions R382m = R346m). | `346 - 182 = R164m` unexplained cash flow bridge discrepancy. Script verified. | **PASS** (as gap flag) | Valid gap identification; company disclosure lacks an explicit bridge. Linked: **F005**, **F006**. |
| **C006** | Stage 1 §2.6, S2 brief: Historical cash roll-forward passes (opening R107m + net increase R6m = closing R113m; matches SoFP R112m + R1m HFS). | `H`/`D` | PDF p. 8 (cash R112m, HFS cash R1m), p. 12 (opening R107m, change +R6m, closing R113m). | `-111 (OCF) - 61 (ICF) + 178 (FCF) = +6`. `107 + 6 = 113`. `112 + 1 = 113`. Ties exactly. | **PASS** | Historical cash ties; no ungrounded forecast roll-forward asserted. Linked: **F005**. |
| **C007** | Stage 2 withheld brief: Sensitivity matrix and valuation targets omitted. | `A`/`D` | `stage2_withheld_brief.md`. JSON valuation fields are null. | Verified null fields in `stage2_withheld_brief.json` and `publication_assessment.json`. | **PASS** | Complies with mandatory withholding contract. Linked: **F006**. |
| **C008** | Stage 1 §2.8: Services revenue is R711m (72.4% from International), while CODM total revenue R1,599m includes PBD gross revenue R888m. | `H`/`D` | PDF p. 9 (IFRS revenue R711m), p. 17 (geography: SA R159m, Intl R552m), p. 31 (CODM R1,599m). | `552 / 711 = 77.6%` (ex-SA). DeepSeek distinguishes IFRS revenue from CODM gross revenue. | **PASS** | Distinguishes statutory revenue from management aggregations. |
| **C009** | Stage 1 §2.5, S2 brief: R1,396m interest-bearing debt due within 12m vs R112m cash and R475m undrawn overdraft; ~R0.8bn management claim unreconciled. | `H`/`M` | PDF p. 5 (outlook commentary), p. 8 (cash R112m), p. 14 (Note 2 debt maturity & overdrafts). | `1396 - (112 + 475) = R809m` net deficit. Disclosed undrawn R475m leaves R325m unreconciled. | **PASS** | Confirms critical refinancing dependency and unsupported management claim. Linked: **F005**, **F006**. |
| **C010** | Stage 1 §2.2: 12-month rolling ECL horizon vs lifetime POCI modeling. | `H`/`A` | PDF p. 13 (Note 1 lifetime ECL), pp. 20–21 (Note 6.1 model description). | Principal book is POCI Stage 3 lifetime; rolling 12m applies to collection estimation. | **NOT VERIFIED** | Direction of lifetime misstatement remains unproven without vintage loss curves. |
| **C011** | Stage 2 brief: Rating bands and static recommendation withheld; inverted short stop removed. | `D` | `stage2_withheld_brief.md`, `publication_assessment.json`. | All dynamic bands and recommendations are null. No inverted short stop. | **PASS** | Inverted recommendation logic permanently removed. Linked: **F006**. |
| **C012** | SOTP EV-to-Equity Working Capital Add-back (+R276m) from prior run. | `A`/`D` | Prior trial `20261027T175621Z` added +R276m WC. Current trial withholds SOTP. | SOTP omitted; no R276m working capital double-count added in this trial. | **PASS** | Prior defect not repeated in current trial. Linked: **F005**. |
| **C013** | Stage 1 §2.2, S2 brief: Trade receivables 0% ELR on 30+ days is an unverified relaxation of 30-DPD SICR staging. | `H`/`A` | PDF p. 25 (Note 6.1 ECL allowance table for trade receivables). | Trade receivables apply IFRS 9 simplified lifetime ECL model (no SICR or 30-DPD backstop). | **FAIL** | Conflates simplified provision matrix with 3-stage loan staging. Linked: **F003**. |
| **C014** | Highlights Table Percentage Signs: Management percentage signs on p. 3 were errors. | `H`/`D` | PDF p. 3 (Key highlights). Opex 820 vs 865 (+5% favorable), Amortisation 597 vs 422 ((41%) adverse). | DeepSeek completely omitted the old false sign allegation from Stage 1 and Stage 2. | **PASS** | Prior false allegation successfully dropped. Linked: **F005**. |
| **C015** | Forecast portfolio roll-forward residuals from prior run. | `A`/`D` | Prior trial had 40m/50m residuals. Current trial has no forward forecast model. | No unintegrated forward portfolio schedules asserted. | **NOT APPLICABLE** | Forward model not completed due to token exhaustion. Linked: **F001**. |
| **C016** | Forecast working capital and debt repayment bridges. | `A`/`D` | Prior trial had unitemized 245/95/145 WC lines. Current trial has no forecast model. | Forward model omitted under withholding. | **NOT APPLICABLE** | Forward forecast omitted. Linked: **F001**. |
| **C017** | DCF equity cross-check and lease/debt policy consistency. | `A`/`D` | Prior trial discounted flows before repayments. Current trial has no DCF model. | No forward DCF asserted. | **NOT APPLICABLE** | DCF omitted under withholding. Linked: **F001**. |
| **C018** | Stage 2 Withheld Recovery Brief correctly applies `ALL-MATERIAL-ISSUES-VALUATION-WITHHOLD`. | `D` | `stage2_withheld_brief.md`, `publication_assessment.json`. | 7 valuation checks marked `NOT VERIFIED`; target, upside, TSR, rating are null. | **PASS** | Correct execution of publication withholding contract. Linked: **F006**. |
| **C019** | Monotonic rating bands and recommendation thresholds. | `D` | `stage2_withheld_brief.md`. Rating bands null. | Rating bands cleared under withholding gate. | **PASS** | Monotonicity satisfied vacuously via null fields. Linked: **F006**. |
| **C020** | Tangible NAV definition: Excludes goodwill vs all intangibles. | `H`/`D` | PDF p. 8 (equity R1,329m, goodwill R511m, intangibles R67m). | `(1329 - 511) / 780.651 = R1.05`. `(1329 - 511 - 67) / 780.651 = R0.96`. | **PASS** | Stage 1 focuses on statutory NAV R1.70; avoids erroneous tangible label. |
| **C021** | Stage 1 §2.6, S2 brief: Cash flow statement line "Net cash generated/(utilised) by investing activities R178m" on p. 12 is mislabelled and represents financing activities. | `H`/`D` | PDF p. 12 (Statement of cash flows, financing section subtotal). | Line sums proceeds (1145) - settlements (842) + OD draw (3178) - OD settle (3269) - leases (30) - treasury (4) = +178. | **PASS** | Genuine company mislabelling correctly identified and verified. Linked: **F005**. |
| **C022** | Stage 1 §2.9, S2 brief: NCA fee/rate caps and ABS securitisation triggers are missing disclosures. | `A` | `stage1.md` §2.9, `stage2_withheld_brief.md` blocking issues #10. | Nutun is a debt purchaser/BPO provider using bank credit lines, not an NCA credit originator or ABS SPV. | **FAIL** | Demands non-applicable statutory and structural disclosures. Linked: **F004**. |
| **C023** | Section responses: Ledger update JSON deltas contain non-literal quotes and trigger open-only fallbacks. | `D` | `experiment.sqlite` (`section_response_attempts`), `status.json`. | 15 of 24 attempts rejected due to non-literal quotes/pipes. 5 local fallbacks; 68 of 69 questions open. | **PASS** (as defect finding) | Systemic model generation failure on strict quote contracts. Linked: **F002**. |
| **C024** | Full Stage 2 valuation exhausted completion token budgets (65,536 and 98,304 tokens). | `D` | `stage2_incomplete_attempt.json`, `execution_status_before_handoff.json`, `status.json`. | DeepSeek flash generated >98,304 tokens without completing final answer (`finish_reason: length`). | **PASS** (as process failure) | Critical completion exhaustion identified. Linked: **F001**. |
| **C025** | The Stage 2 withheld recovery brief is a separately prompted narrow task, not a completed full valuation. | `D` | `requests/stage2_withheld_brief.md`, `outputs/stage2_withheld_brief.md`, `gemini/README.md`. | Recovery prompt explicitly directed <2500 words and null fields following budget exhaustion. | **PASS** | Evaluator distinction confirmed; not an autonomous model model completion. Linked: **F001**. |

---

## 4. Required Independent Reconciliations

All calculations independently executed in `calculations/reconciliations.py` and saved in `calculations/reconciliations.json`.

### 4.1 Valuation & Publication Gate Check
- **Model Valuation Target:** `null` (WITHHELD).
- **Static & Dynamic Recommendation:** `null` (WITHHELD).
- **Rating Bands:** `null` (WITHHELD).
- **Execution Basis:** The full Stage 2 prompt exhausted 65,536 and 98,304 token budgets. The separately prompted recovery brief emitted the mandatory JSON contract with 7 `NOT VERIFIED` valuation checks.
- **Independent Verdict:** **PASS (Withholding Supported)**. Withholding is mandatory under `ALL-MATERIAL-ISSUES-VALUATION-WITHHOLD` due to material unresolved liquidity, refinancing, and cash flow bridge issues.

### 4.2 Cash Flow Statement Reconciliation (Physical Page 12)
- **Statutory Cash Flow from Operations:**
  $$\text{Cash utilised before WC, int, tax} = -50$$
  $$\text{Finance income received} = +3$$
  $$\text{Finance costs paid} = -225$$
  $$\text{Tax refunded} = +2$$
  $$\text{Purchased book debts (operating asset decrease)} = +182$$
  $$\text{Changes in working capital} = -23$$
  $$\text{Statutory OCF} = -50 + 3 - 225 + 2 + 182 - 23 = -111\text{ Rm}$$
  *Stated OCF = -111 Rm (ties exactly).*
- **Capex and Lease Cash Outflows:**
  $$\text{Capex (PPE R17m + Intangibles R13m)} = -30\text{ Rm}$$
  $$\text{Operating cash flow after capex} = -111 - 30 = -141\text{ Rm}$$
  $$\text{Lease liability principal repayments (financing)} = -30\text{ Rm}$$
  $$\text{Cash flow after capex and leases} = -141 - 30 = -171\text{ Rm}$$
- **Financing Activities (Mislabeled on p. 12 as Investing):**
  $$\text{Borrowings proceeds} = +1,145$$
  $$\text{Borrowings repayments} = -842$$
  $$\text{Overdraft draw-downs} = +3,178$$
  $$\text{Overdraft settlements} = -3,269$$
  $$\text{Net borrowing proceeds} = 1,145 - 842 + 3,178 - 3,269 = +212\text{ Rm}$$
  $$\text{Lease principal repayment} = -30$$
  $$\text{Acquisition of treasury shares} = -4$$
  $$\text{Net financing cash flow} = 212 - 30 - 4 = +178\text{ Rm}$$
  *Stated line on p. 12 = +178 Rm (ties exactly).*
- **Investing Activities:**
  $$\text{Capex} = -30$$
  $$\text{Dividends from equity accounted investment} = +6$$
  $$\text{Deposits into other investments} = -37$$
  $$\text{Net investing cash flow} = -30 + 6 - 37 = -61\text{ Rm}$$
  *Stated investing line = -61 Rm (ties exactly).*
- **Cash Roll-Forward & Balance Sheet Reconciliation:**
  $$\text{Net cash change} = -111 (\text{OCF}) - 61 (\text{ICF}) + 178 (\text{FCF}) = +6\text{ Rm}$$
  $$\text{Opening cash} = 107\text{ Rm}$$
  $$\text{Closing cash} = 107 + 6 + 0 (\text{FX}) = 113\text{ Rm}$$
  $$\text{SoFP cash (p. 8)} = 112 (\text{unrestricted}) + 1 (\text{held-for-sale}) = 113\text{ Rm (ties exactly)}.$$
- **Unreconciled PBD Operating Cash Flow Gap:**
  $$\text{Note 1.1 Net Cash Collections} = 728\text{ Rm}$$
  $$\text{Note 1.1 Additions} = 382\text{ Rm}$$
  $$\text{Note 1.1 Net Cash Generated from PBD} = 728 - 382 = 346\text{ Rm}$$
  $$\text{SoCF line 'Purchased book debts'} = 182\text{ Rm}$$
  $$\text{Unexplained gap} = 346 - 182 = 164\text{ Rm (NOT VERIFIED)}.$$

### 4.3 Debt and Liquidity Runway Reconciliation (Physical pp. 5, 8, 14–15)
- **Total Interest-Bearing Liabilities:**
  $$\text{Senior liabilities} = 3,547\text{ Rm}$$
  $$\text{Subordinated liabilities} = 196\text{ Rm}$$
  $$\text{Bank overdrafts} = 273\text{ Rm}$$
  $$\text{Total interest-bearing debt} = 3,547 + 196 + 273 = 4,016\text{ Rm}$$
  *Stated total debt = 4,016 Rm (ties exactly).*
- **Short-Term Debt Maturity Wall (Within 12 Months):**
  $$\text{Senior debt due <12m} = 927\text{ Rm}$$
  $$\text{Subordinated debt due <12m} = 196\text{ Rm}$$
  $$\text{Bank overdrafts} = 273\text{ Rm}$$
  $$\text{Total short-term debt payable <12m} = 927 + 196 + 273 = 1,396\text{ Rm}$$
- **Disclosed Available Liquidity:**
  $$\text{Cash on balance sheet} = 112\text{ Rm}$$
  $$\text{Total overdraft facilities} = 748\text{ Rm}$$
  $$\text{Drawn overdraft} = 273\text{ Rm}$$
  $$\text{Disclosed undrawn overdrafts} = 748 - 273 = 475\text{ Rm}$$
  $$\text{Total disclosed liquid resources} = 112 + 475 = 587\text{ Rm}$$
- **Liquidity Deficit & Unreconciled Management Claim:**
  $$\text{12-Month Refinancing Shortfall} = 1,396 - 587 = \mathbf{-809\text{ Rm (Deficit)}}$$
  $$\text{Management claimed unutilised facilities (p. 5)} \approx 800\text{ Rm}$$
  $$\text{Unreconciled facility gap} = 800 - 475 = 325\text{ Rm (NOT VERIFIED)}.$$
- **Encumbrance Check:** 100% of the principal book portfolio (R3,845m), trade receivables, and cash are pledged to secure credit facilities (Notes 1 and 2.1). Unencumbered collateral buffer is negligible.

### 4.4 PBD Portfolio & Impairment Accounting Reconciliation (Physical pp. 13, 22, 24)
- **Principal Book Roll-Forward (Note 1.1, p. 13):**
  $$\text{Opening balance} = 3,975\text{ Rm}$$
  $$\text{Additions} = +382\text{ Rm}$$
  $$\text{Net cash collections} = -728\text{ Rm}$$
  $$\text{CAEIR imputed interest} = +383\text{ Rm}$$
  $$\text{Net impairment loss} = -167\text{ Rm}$$
  $$\text{Closing principal book} = 3,975 + 382 - 728 + 383 - 167 = 3,845\text{ Rm (ties exactly)}.$$
- **Other Financial Assets Roll-Forward (Note 1.2, p. 13):**
  $$\text{Opening} = 702 + \text{Additions} = 28 - \text{Collections} = 116 + \text{FV movement} = 30 = 644\text{ Rm (ties exactly)}.$$
  $$\text{Total PBD carrying value} = 3,845 + 644 = 4,489\text{ Rm (ties p. 3 Key highlights)}.$$
- **POCI Gain Reconciliation (Note 6.2, p. 22):**
  $$\text{Gross carrying amount} = 3,414\text{ Rm}$$
  $$\text{Cumulative impairment gain} = +431\text{ Rm}$$
  $$\text{Net carrying amount} = 3,414 + 431 = 3,845\text{ Rm (ties exactly)}.$$
  $$\text{Gain percentage of gross} = \frac{431}{3,414} = 12.624\% \quad (\text{Gain/Gross, NOT loss coverage reserve}).$$
- **Impairment Loss Decomposition (Note 6.1, p. 24):**
  $$\text{Acquired book impairment gain} = +24\text{ Rm}$$
  $$\text{Historical book impairment loss} = -191\text{ Rm}$$
  $$\text{Net P&L impairment loss} = 24 - 191 = -167\text{ Rm (ties exactly)}.$$
  *Critical observation:* The H1 FY26 historical book loss (-R191m) exceeds the full-year FY25 historical loss (-R182m), confirming accelerating deterioration on back-book collections.
- **Estimated Remaining Collections (ERC, p. 3):**
  $$\text{Stated ERC} = 8,366\text{ Rm}$$
  $$\text{ERC Multiple of Carrying Value} = \frac{8,366}{4,489} = 1.8637\times$$
  $$\text{Annualised gross collections} = 773 \times 2 = 1,546\text{ Rm/year}$$
  $$\text{Implied straight-line run-off} = \frac{8,366}{1,546} \approx 5.41\text{ years (indicative only; collection curve NOT VERIFIED)}.$$

### 4.5 Earnings, Shares, and NAV Reconciliation (Physical pp. 8, 16, 18)
- **Net Shares in Issue (Note 4, p. 16):**
  $$\text{Issued ordinary shares} = 784,313,242$$
  $$\text{Less: Treasury shares} = -3,662,209$$
  $$\text{Net shares in issue} = 780,651,033$$
- **Statutory Net Asset Value (NAV) per Share (p. 8):**
  $$\text{Total equity} = 1,329,000,000\text{ ZAR}$$
  $$\text{Statutory NAV per share} = \frac{1,329,000,000}{780,651,033} = \mathbf{R1.7024} \quad (\mathbf{R1.70/share}).$$
  *Contributed stated capital per share:*
  $$\text{Stated capital} = 5,410,000,000\text{ ZAR} \implies \frac{5,410,000,000}{780,651,033} = \mathbf{R6.9301} \quad (\mathbf{R6.93/share}).$$
- **Continuing Headline Loss per Share (Note 5, p. 18):**
  $$\text{Continuing headline loss} = -63,000,000\text{ ZAR}$$
  $$\text{Weighted average shares} = 782,143,767 \quad (782.1\text{m})$$
  $$\text{Continuing HEPS} = \frac{-63,000,000}{782,143,767} \times 100 = \mathbf{-8.0548\text{ cents}} \quad (\mathbf{-8.1\text{ cents}}).$$

### 4.6 CODM Amortisation Footnote Reconciliation (Physical p. 31)
$$\text{Net collections (principal)} = 728$$
$$\text{CAEIR imputed interest} = -383$$
$$\text{Net impairment loss} = +167$$
$$\text{Cash collections (other assets)} = +116$$
$$\text{Fair value movements (other assets)} = -30$$
$$\text{Calculated CODM amortisation} = 728 - 383 + 167 + 116 - 30 = \mathbf{598\text{ Rm}}$$
*Stated CODM amortisation = 597 Rm (ties within R1m rounding).*

### 4.7 IFRS Income Statement Vertical Summation (Physical p. 9)
$$\text{Revenue} = 711$$
$$\text{Cost of revenue} = -385$$
$$\text{Gross profit from services} = 711 - 385 = 326\text{ Rm (ties)}$$
$$\text{Net income from PBD} = 383 (\text{CAEIR}) - 177 (\text{Funding int}) - 167 (\text{Impairment}) + 30 (\text{FV}) = 69\text{ Rm (ties)}$$
$$\text{Operating costs} = -445$$
$$\text{Net finance charge} = -39$$
$$\text{Net other income} = +11$$
$$\text{Loss from associate} = -1$$
$$\text{Operating loss} = 326 + 69 - 445 - 39 + 11 - 1 = -79\text{ Rm (ties)}$$
$$\text{Non-operating loss} = -13$$
$$\text{Loss before taxation} = -79 - 13 = -92\text{ Rm (ties)}$$
$$\text{Taxation credit} = +29$$
$$\text{Loss from continuing operations} = -92 + 29 = -63\text{ Rm (ties)}.$$

---

## 5. Findings and Evaluator Revisions

| Finding ID | Linked Claims | Severity | Description & Root Cause | Required Correction & Downstream Effect |
| :--- | :--- | :---: | :--- | :--- |
| **F001** | `C024`, `C025` | **Critical** | **Stage 2 Completion Budget Exhaustion:** DeepSeek Flash hit 65,536 and 98,304 completion token limits without completing the full Stage 2 prompt. The subsequent recovery brief was a separately commanded, narrow task (<2500 words) with pre-set null fields. | Decouple the quantitative valuation tables from exhaustive prose generation in the Stage 2 prompt to enforce strict token budgeting. Never treat the withheld brief as an autonomous full valuation completion. |
| **F002** | `C023` | **High** | **Ledger Delta Quote Hallucinations & Open-Only Fallbacks:** DeepSeek repeatedly failed literal quote checks (15 rejections in 24 attempts) by inserting markdown table syntax `|` or formatting spaces into `evidence.quote`. This triggered 5 local open-only fallbacks, leaving 68 of 69 questions open. | Instruct DeepSeek in the section prompt that evidence quotes must be exact verbatim substrings without markdown pipes or added spaces. Provide clean text excerpts for tabular quotes. |
| **F003** | `C013` | **Medium** | **Repeated Trade Receivables Simplified ECL Misconception:** DeepSeek repeatedly alleged that 0.00% ELR on 30+ day overdue receivables was an unverified relaxation of the 30-DPD SICR staging threshold under IFRS 9. Corporate trade receivables apply the IFRS 9.5.5.15 simplified approach (lifetime ECL provision matrix) and do not track SICR or 30-DPD backstops. | Codify analytical guardrail preventing models from demanding SICR/30-DPD loan staging on trade receivables using the simplified approach. |
| **F004** | `C022` | **Medium** | **Unsubstantiated Missing Disclosure Demands:** DeepSeek demanded NCA fee/rate caps and ABS securitisation trigger disclosures, treating their absence as a missing disclosure. Nutun acquires written-off NPLs and provides BPO services financed by bank credit lines, not consumer credit origination or ABS SPVs. | Refine consumer lending sector prompts to distinguish unsecured debt buyers/servicers from bank lenders and securitisation issuers. |
| **F005** | `C001`–`C003`, `C014`, `C021` | **Low (Positive)** | **Demonstrated Substantive Accounting Improvements:** DeepSeek correctly maintained the POCI cumulative gain interpretation (+R431m), statutory NAV per share (R1.70), CODM amortisation arithmetic (598 ≈ 597), dropped the false management percentage-sign allegation, and identified the company's p. 12 investing/financing label error. | Retain these verified accounting principles across future prompts and evaluation baselines. |
| **F006** | `C004`, `C018` | **Low (Positive)** | **Valuation Withholding Mandate Complied With:** DeepSeek strictly adhered to `ALL-MATERIAL-ISSUES-VALUATION-WITHHOLD` by refusing to issue an unverified target price or recommendation in the presence of an R809m short-term liquidity deficit, 100% asset pledge, and unbridged cash flow gaps. | Retain the publication withholding gate as a permanent architectural standard. |

---

## 6. Valuation Errors Found & Analytical Lessons Learned

### 1. Errors Found in the Valuation / Model:
* **Stage 2 Completion Exhaustion (Process Defect):** DeepSeek failed to finish the full institutional valuation prompt within 65,536 and 98,304 token limits, necessitating a recovery prompt.
* **Ledger Quote Formatting Hallucination (Operational Defect):** DeepSeek repeatedly inserted markdown formatting (`|` pipes and spacing) into JSON delta quote fields, causing 15 validator rejections and 5 local open-only fallbacks, leaving 68 questions unresolved in the database.
* **Simplified Lifetime ECL vs 3-Stage Loan Staging Conflation (Analytical Defect):** The model repeatedly demanded a 30-DPD SICR rebuttable presumption disclosure for trade receivables governed by the IFRS 9 simplified approach.
* **Non-Applicable Regulatory & Structural Demands (Analytical Defect):** The model demanded NCA origination fee/rate caps and ABS securitisation triggers for a debt purchaser financed via syndicated bank facilities.

### 2. Analytical Lessons Learned:
* **Token Budget Management for Reasoning Models:** When requesting exhaustive financial research notes with high reasoning allocations, decouple the structured JSON data contract and core financial schedules from narrative generation to prevent completion limit truncation.
* **Strict Verbatim Extraction Contracts:** LLMs default to converting table data into markdown syntax. Prompting must explicitly enforce that table evidence quotes must be extracted as continuous text or exact cell substrings without markdown formatting characters.
* **IFRS 9 Simplified Approach Boundaries:** In consumer lending companies that also provide corporate BPO or agency services, always separate corporate trade receivables (IFRS 9.5.5.15 simplified lifetime ECL) from consumer lending advances or purchased credit-impaired assets (POCI Stage 3).

### 3. Proposed New Guardrails:

#### Proposed Guardrail 1: Trade Receivables Simplified Approach
- **Rule Code:** `CONSUMER-LENDING-TRADE-RECEIVABLES-SIMPLIFIED-ECL`
- **Sector:** `consumer_lending` (or `all`)
- **Title:** **Trade Receivables IFRS 9 Simplified Approach (No SICR / 30-DPD Staging Demand)**
- **Rule Text:** *Do not demand Stage 1/Stage 2/Stage 3 ECL migration, 30-DPD rebuttable presumption, or SICR disclosures for corporate trade receivables that apply the IFRS 9 simplified approach (provision matrix). Verify whether the entity applies the simplified lifetime ECL model under IFRS 9.5.5.15 before asserting that staging policies or 30-DPD backstops are missing.*
- **Confirmed Failure Addressed:** DeepSeek repeatedly flagging absence of 30-DPD SICR thresholds for trade receivables in Section 6, Stage 1, and Stage 2 withheld brief.
- **Trigger:** Any trade receivables note applying a provision matrix / maturity loss rate table.
- **Example Failing:** Claiming that a 0% expected loss rate on 30-day overdue trade receivables violates IFRS 9 Stage 2 rules because management failed to disclose a 30-DPD SICR rebuttable presumption.
- **Example Passing:** Noting that under the IFRS 9 simplified provision matrix, 0% ELR on 30-day overdue receivables reflects management's historical loss experience and forward-looking economic adjustment, without demanding a 3-stage SICR framework.
- **Implementation Point:** Section capture prompt and Stage 1 forensic prompt.

---

## 7. Actionable Recommendation & Decision Gate

* **Current Dynamic Recommendation:** **`WITHHELD`** (No published rating or target price).
* **Rerun Action Required?**:
  - **No rerun recommended at this time.** The company's underlying disclosures contain material unresolved dependencies: an R809m short-term refinancing shortfall, unverified ~R0.8bn facility claims, 100% asset pledge, and an unbridged R164m PBD cash flow movement. Withholding valuation is the economically and institutionally correct outcome.
* **Guardrail Database Codification Gate:**
  > *"Would you like me to codify the newly discovered guardrail (`CONSUMER-LENDING-TRADE-RECEIVABLES-SIMPLIFIED-ECL`) into the `sector_guardrails` database to permanently enforce this standard across all future valuations?"*

---

## 8. Handoff for Codex Review

This audit record, supporting calculations, and preserved input outputs are saved under:
- **Audit Absolute Path:** `C:/Users/diond/Desktop/Projects/stock_analysis_prompts/companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T092500Z_gemini/audit.md`
- **Calculations Absolute Path:** `C:/Users/diond/Desktop/Projects/stock_analysis_prompts/companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T092500Z_gemini/calculations/reconciliations.json`
- **Input Manifest Absolute Path:** `C:/Users/diond/Desktop/Projects/stock_analysis_prompts/companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T092500Z_gemini/inputs/manifest.json`

Original model outputs, source PDFs, and SQLite database guardrails have been preserved completely unchanged.
