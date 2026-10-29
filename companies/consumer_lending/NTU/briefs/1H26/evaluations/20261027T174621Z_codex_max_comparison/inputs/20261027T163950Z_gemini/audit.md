# INDEPENDENT EVALUATION AUDIT RECORD — NUTUN LIMITED (NTU) 1H26
**Document ID:** `NTU-1H26-EVAL-20261027T163950Z-GEMINI`  
**Evaluator:** Gemini (`Gemini 3.8 Flash High`)  
**Evaluation Timestamp (UTC):** `2026-10-27T16:39:50Z`  
**Evaluation Timestamp (Local):** `2026-10-27T18:39:50+02:00` (Africa/Johannesburg)  
**Target Entity:** Nutun Limited (`NTU.JO` / JSE Sector: Consumer Lending `JS3020`)  
**Reporting Period:** `1H26` (Six months ended 31 March 2026)  
**Evaluation Subject:** DeepSeek Flash Section Capture, Stage 1 Forensic Audit & Stage 2 Valuation Note  

---

## 1. Inputs, Preservation, and Saved Handoff

### 1.1 Input Identification & Baseline Hash Verification
All primary inputs were verified against stored cryptographic baselines in `documents/analysis.sqlite` (`reports` table) prior to evaluation. Original PDF source files remain untouched.

| Input Document / Artifact | Original Workspace Path | SHA-256 Hash | File Size | Baseline Status |
| :--- | :--- | :--- | :---: | :---: |
| **Primary Source PDF** | `companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf` | `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc` | 1,719,316 bytes | **VERIFIED** (Exact match with SQLite `reports.sha256`) |
| **Stage 1 Forensic Audit** | `companies/consumer_lending/NTU/briefs/1H26/NTU_1H26_stage1_audit_response.md` | `9487e50a4dd12a3c33e23b3784498477cb691cef0c32a65c83db4e041b5c766e` | 22,119 bytes | **PRESERVED** in `inputs/` |
| **Stage 1 Prompt** | `companies/consumer_lending/NTU/briefs/1H26/NTU_1H26_stage1_forensic_prompt.md` | `c52f4c072248bc5e2423fb0eb9ba37d45819c18cc9ed69c4f5c763e6916783e5` | 173,617 bytes | **PRESERVED** in `inputs/` |
| **Stage 2 Valuation Note** | `companies/consumer_lending/NTU/briefs/1H26/NTU_1H26_stage2_valuation_note.md` | `3ebf5454d048ab3eb8ee4c37e748a219dfda45cbb84f8ff95b0e4ebb1fd4f74c` | 19,806 bytes | **PRESERVED** in `inputs/` |
| **Stage 2 Prompt** | `companies/consumer_lending/NTU/briefs/1H26/NTU_1H26_stage2_valuation_prompt.md` | `2807744b985483b0342b8b733046c9df954e6a4c9331aef8e79ad29eb651f6ff` | 36,610 bytes | **PRESERVED** in `inputs/` |

### 1.2 Inspection Log & Physical PDF Coverage
* **Total Physical Pages in Source PDF:** 38 pages.
* **Physical Pages Examined Directly:**
  - `p. 1–2`: Cover and Table of Contents.
  - `p. 3–5`: Key Highlights, Performance Review, and Operational Update / Liquidity Outlook.
  - `p. 6–7`: Basis of Preparation (unaudited/unreviewed IAS 34 status) and Non-IFRS Core Results Policy.
  - `p. 8`: Condensed Consolidated Statement of Financial Position (Balance Sheet).
  - `p. 9–10`: Condensed Consolidated Statement of Comprehensive Income (Income Statement).
  - `p. 11`: Condensed Consolidated Statement of Changes in Equity (Treasury share transactions).
  - `p. 12`: Condensed Consolidated Statement of Cash Flows (Operating, Investing, Financing).
  - `p. 13`: Note 1 — Purchased Book Debts (Principal books, Other financial assets, Additions, Collections).
  - `p. 14–15`: Note 2 — Interest-Bearing Liabilities and Bank Overdrafts (Maturity profile, Facilities, Pledges).
  - `p. 16`: Note 3 — Ordinary Share Capital and Treasury Share Buybacks.
  - `p. 17`: Note 4 — Revenue Disaggregation by Geography and Stream.
  - `p. 18–19`: Note 5 — Basic, Diluted, and Headline Loss Per Share Reconciliations.
  - `p. 20–25`: Note 6.1 — Financial Risk Management: Credit Risk, POCI Valuation, Concentration, ECL Reconciliation.
  - `p. 26`: Note 6.2 — Currency Risk (FX rates, balance sheet monetary assets/liabilities).
  - `p. 26–28`: Note 6.3 — Fair Value Disclosures (Amortised cost vs. Fair value, 18.50% market discount rate).
  - `p. 28–29`: Note 6.4 — Level 3 Fair Value Hierarchy Reconciliation.
  - `p. 30–36`: Note 7 — Segment Reporting (Nutun SA CODM vs. IFRS reconciliation, Nutun International).
  - `p. 36`: Note 8 & 9 — Going Concern Assessment and Subsequent Events.
  - `p. 37–38`: Corporate Information and Directory.
* **Supplied-but-Unread Files:** None.
* **Missing Inputs / Unavailable Tools:** None. Full local text extraction and programmatic execution available.
* **Saved Handoff Directory:** `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T163950Z_gemini/`
  - Input models preserved in `inputs/` with accompanying `manifest.json`.
  - Executable reconciliation script saved in `calculations/reconciliations.py` and actual output in `calculations/reconciliations_output.txt`.

---

## 2. Claim Verification Register

| Claim ID | Claim and Origin | Classification | Primary Evidence Citation | Independent Verification Performed | Verdict | Consequence / Impact |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **C001** | Core EBITDA grew +28.5% to R790m (`Stage 1, §1`) | Historical Result | PDF p. 3 (Highlights), p. 31 (Note 7) | Recomputed: (790 - 615) / 615 = +28.46%. Confirmed non-IFRS CODM metric. | **PASS** | Validates baseline non-IFRS figure. |
| **C002** | Operating cash flow was negative R(111)m, creating a R901m gap to EBITDA (`Stage 1, §1`) | Derived Calculation | PDF p. 12 (Cash flow statement) | Recomputed: Net cash utilised by operating activities is statutory R(111)m. 790 - (-111) = R901m gap. | **PASS** | Confirms severe cash conversion deficit. |
| **C003** | Gross collections rose +28% to R773m (`Stage 1, §1`) | Historical Result | PDF p. 4, p. 13 (Note 1.1 footnote **) | Recomputed: (773 - 604) / 604 = +27.98% on principal book. | **PASS** | Validates collections volume claim. |
| **C004** | PBD acquisitions in H1 were R382m on principal book and R410m total (`Stage 1, §1`) | Historical Result | PDF p. 3, p. 13 (Notes 1.1 & 1.2) | Note 1.1 additions R382m + Note 1.2 additions R28m = R410m total acquisitions. | **PASS** | Validates capital reinvestment pace. |
| **C005** | Total equity fell to R1,329m from R1,396m at Sep-25 (`Stage 1, §1`) | Historical Result | PDF p. 8 (Balance sheet), p. 11 | Balance sheet shows R1,329m (Mar-26) vs R1,396m (Sep-25) and R1,551m (Mar-25). | **PASS** | Confirms equity erosion trajectory. |
| **C006** | 100% of PBD portfolio (R3,845m) is pledged for R4,016m liabilities (`Stage 1, §1`) | Historical Result | PDF p. 13 (Note 1.1 *), p. 14 (Note 2), p. 15 (Note 2.1 *) | Confirmed full pledge of PBDs, trade receivables and cash against all senior/sub debt and overdrafts. | **PASS** | Proves near-total asset encumbrance. |
| **C007** | PBD portfolio is 100% POCI / Stage 3 under IFRS 9 (`Stage 1, §2.1`) | Accounting Rule | PDF p. 13 (Note 1), p. 21 (Note 6.1) | Verified irrevocable POCI classification at inception with no Stage 1/2 curing. | **PASS** | Confirms POCI accounting reality. |
| **C008** | ECL coverage collapsed from 20.4% to 12.6% on principal book (`Stage 1, §2.1`) | Derived Calculation | PDF p. 22–24 (Note 6.1) | Audited Note 6.1 table: R431m is a **cumulative impairment gain** (asset write-up), NOT a loss allowance reserve. DeepSeek calculated 431/3414=12.6%. | **FAIL** | **Accounting Misclassification**: Misinterprets cumulative outperformance gain as an ECL reserve. |
| **C009** | Note 7 amortisation footnote does not arithmetically reconcile (`Stage 1, §2.3`) | Model Assertion | PDF p. 31 (Note 7 footnote *) | DeepSeek summed 383+167+728+30+116 = 1,424. True net run-off signs: (728 - 383 + 167) + (116 - 30) = 512 + 86 = 598m (matches R597m). | **FAIL** | **False Allegation**: DeepSeek made a sign error; footnote reconciles accurately. |
| **C010** | Fair value market discount rate of 18.50% vs CAEIR 19.2% creates 70bps tension (`Stage 1, §2.3`) | Model Observation | PDF p. 21, p. 26 (Note 6.3) | Verified 18.50% market discount rate vs 19.20% CAEIR with unquantified risk adjustments. | **PASS** | Highlights valuation opacity on Level 3 assets. |
| **C011** | Near-term funding gap is R809m against R1,396m 12-month maturity wall (`Stage 1, §2.6`) | Derived Calculation | PDF p. 12, p. 14 (Note 2) | R112m cash + R475m verified undrawn overdraft = R587m liquid headroom vs R1,396m maturing debt = R809m gap. | **PASS** | Core liquidity vulnerability supported. |
| **C012** | Management claim of ~R0.8bn unutilised facilities is uncorroborated (`Stage 1, §2.6`) | Missing Disclosure Claim | PDF p. 5, p. 14–15 (Note 2) | Full inspection confirms only R475m undrawn overdraft is quantified; RCF facility limit is omitted. | **PASS** | Validates disclosure gap flag. |
| **C013** | Treasury shares were acquired at R1 vs ~R6.90 book value (`Stage 1, §1`, `Stage 2, §1`) | Derived Calculation | PDF p. 8, p. 11, p. 16 (Note 3.1) | Contributed share capital is R5,410m (R6.93/sh), but Net Total Equity is R1,329m = R1.70/sh. DeepSeek omitted R4.11bn retained loss. | **FAIL** | **Book Value Distortion**: Overstates true NAV by 4.1x by ignoring accumulated deficit. |
| **C014** | Page 3 Highlights table contains sign errors on percentage changes (`Stage 1, §4`) | Model Assertion | PDF p. 3 | Examined table: positive percentages indicate favorable P&L variances (cost savings); bracketed indicate adverse variances. | **FAIL** | **Management Reporting Misunderstanding**: Standard variance convention mistaken for errors. |
| **C015** | Pre-discount SOTP equity value of R1,115m yields R1.43/share (`Stage 2, §4`) | Derived Calculation | Stage 2 Table lines 190–194 | R1,115m / 780.7m shares = R1.428 (R1.43). Net debt deducted correctly in SOTP schedule. | **PASS** | Arithmetically consistent baseline. |
| **C016** | SOTP Fair Value per share after 25% discount is R1.07 (`Stage 2, §4`) | Derived Calculation | Stage 2 Table lines 190–194 | (1,115m - 279m) / 780.7m = 836m / 780.7m = R1.0708 (R1.07). | **PASS** | Correct per-share value after single 25% discount. |
| **C017** | Target price of R0.55 derived by deducting 25% again to get R0.80, then 31% haircut (`Stage 2, §4`) | Model Calculation | Stage 2 Table lines 195–197 | 1.07 × 0.75 = 0.8028. Deducted 25% twice. Then applied unmodeled 31.5% haircut from 0.803 to 0.55. | **FAIL** | **Double-Discounting & Unmodeled Haircut**: 61.5% cumulative discount from R1.43 without explicit modeling. |
| **C018** | SOTP adds R1,479m 'Other assets net of other liabilities' as a book value plug (`Stage 2, §4`) | Model Calculation | Stage 2 Table line 189 | DeepSeek's balance sheet has Other Assets R1,315m and Other Liab R765m (Net R550m). R1,479m is a circular plug. | **FAIL** | **Circular SOTP Plug**: Plugged 1,479m to force Adjusted Equity to equal Book Value (1,115m). |
| **C019** | Dynamic recommendation at R0.90 is STRONG SELL, while static note says SELL (`Stage 2, JSON`) | Market Comparison | Live market data (`NTU.JO`), Stage 2 JSON | Dynamic band: Strong Sell > R0.65. Live price R0.90 > 0.65, and reference R0.89 > 0.65. | **PASS** | Confirms static note recommendation divergence. |

---

## 3. Required Independent Reconciliations

### 3.1 Valuation Schedule, EV-to-Equity Bridge, and SOTP Breakdown
We independently reconstructed DeepSeek's Sum-of-the-Parts (SOTP) model:

$$\begin{aligned}
\text{SA PBD Book} &= \text{R}3,845\text{m} \times 0.55 = \text{R}2,114.75\text{m} \\
\text{SA Other Fin. Assets} &= \text{R}644\text{m} \times 0.70 = \text{R}450.80\text{m} \\
\text{SA Agency / RTC Franchise} &= \text{R}250\text{m (EBITDA)} \times 3.0\text{x} = \text{R}750.00\text{m} \\
\text{Nutun International BPO} &= \text{R}180\text{m (EBITDA)} \times 4.0\text{x} = \text{R}720.00\text{m} \\
\hline
\mathbf{\text{Total Enterprise Value (TEV)}} &= \mathbf{\text{R}4,035.55\text{m}} \quad (\text{Model reports R}4,036\text{m})
\end{aligned}$$

**Bridge to Equity:**
$$\begin{aligned}
\text{Less: FY27E Interest-Bearing Debt} &= (\text{R}3,850.00\text{m}) \\
\text{Less: FY27E Bank Overdrafts} &= (\text{R}310.00\text{m}) \\
\text{Less: FY27E Lease Liabilities} &= (\text{R}335.00\text{m}) \\
\text{Add: FY27E Cash} &= +\text{R}95.00\text{m} \\
\hline
\mathbf{\text{Net Debt}} &= (\mathbf{\text{R}4,400.00\text{m}}) \\
\mathbf{\text{Operating Equity Value (Pre-Adjustment)}} &= \mathbf{-\text{R}364.45\text{m}} \quad (\text{Model reports } -\text{R}364\text{m})
\end{aligned}$$

**Forensic Discovery of the Circular Balance Sheet Plug:**
DeepSeek added line 189: `"Add: Other assets net of other liabilities: 1,479 | Book values"`.
On DeepSeek's own forecast balance sheet (lines 143 & 148):
* Other Assets (PPE, intangibles, goodwill, DTA, equity-accounted) = R1,315m
* Other Liabilities (trade payables, provisions, DTL) = R765m
* Actual Net Other Assets = $\text{R}1,315\text{m} - \text{R}765\text{m} = \text{R}550\text{m}$.

Why did DeepSeek add R1,479m instead of R550m?
$$\text{Target Adjusted Equity} = \text{FY27E Book Equity} = \text{R}1,115\text{m}$$
$$\text{Plug Required} = \text{R}1,115\text{m} - (-\text{R}364.45\text{m}) = \mathbf{\text{R}1,479.45\text{m}}$$
DeepSeek inserted an arbitrary mathematical plug of R1,479m to force its SOTP Adjusted Equity Value to equal its forecast Book Equity of R1,115m. Furthermore, this plug adds back R511m of goodwill already capitalized from the acquisition of the operating businesses valued in the EBITDA multiples!

**Dissection of DeepSeek's Double-Discounting Arithmetic:**
$$\begin{aligned}
\text{Adjusted Equity Value} &= \text{R}1,114.55\text{m} \\
\text{Shares in Issue (Net of Treasury)} &= 780.7\text{m} \\
\text{Pre-Discount Per Share Value} &= \text{R}1,114.55\text{m} / 780.7\text{m} = \mathbf{\text{R}1.428\text{ (R1.43)}} \\
\text{Less: 25\% Corporate Governance/Liquidity Discount} &= -\text{R}278.64\text{m} \\
\text{Target Equity Value} &= \text{R}835.91\text{m} \\
\mathbf{\text{Per Share Value after 25\% Discount}} &= \text{R}835.91\text{m} / 780.7\text{m} = \mathbf{\text{R}1.071\text{ (R1.07)}}
\end{aligned}$$

In lines 195 and 197, DeepSeek committed two catastrophic errors:
1. It asserted: `"1.07 × (1 − 0.25) = 0.80"`, deducting 25% a **second time**:
$$\text{R}1.071 \times 0.75 = \mathbf{\text{R}0.803}$$
*(Note: DeepSeek claimed that R1.43 less 25% was R0.80, but $\text{R}1.428 \times 0.75 = \text{R}1.071$. It applied the discount to R1.07 instead of R1.43).*
2. It then applied an unmodeled, qualitative 31.5% haircut from R0.803 down to **R0.55**:
$$\text{Haircut} = 1 - \frac{\text{R}0.55}{\text{R}0.803} = \mathbf{31.5\%}$$
$$\text{Cumulative Discount from R1.43} = 1 - \frac{\text{R}0.55}{\text{R}1.428} = \mathbf{61.5\%}$$
DeepSeek hand-waved a 61.5% total deduction (25% + 25% + 31.5%) to anchor on R0.55, which happens to equal $0.38 \times \text{Book Value (R1.43)}$.

---

### 3.2 Statutory Cash Flow Reconciliations & PBD Amortisation
We independently reconciled the statutory Statement of Cash Flows (physical page 12):

| Statutory Cash Flow Line Item | H1 2026 (Rm) | H1 2025 (Rm) | Analytical Nature & Direct Evidence |
| :--- | :---: | :---: | :--- |
| **Cash utilised by operations** | **(50)** | **(103)** | Starting operating subtotal before finance/tax flows. |
| Interest received | 3 | 16 | Cash interest on bank balances. |
| Interest paid | (225) | (251) | Gross cash debt service cost. |
| Income taxes refunded / (paid) | 2 | (4) | Net tax refund received. |
| **Operating cash flow before asset/WC changes** | **(270)** | **(342)** | Statutory operating deficit. |
| **Decrease in operating assets: Purchased book debts** | **182** | **384** | **Net cash impact of PBDs**: Net collections (R844m) less acquisitions (R410m) less non-cash P&L income (R246m) = R188m (R182m reported). |
| (Increase) / decrease in trade receivables | (25) | (63) | Working capital absorption. |
| Increase / (decrease) in trade payables | 2 | (200) | Creditor movements. |
| **Net cash utilised by operating activities** | **(111)** | **(213)** | **Final Statutory Operating Cash Flow**. |

**Resolution of the Note 7 Footnote Arithmetic:**
DeepSeek alleged in Stage 1 §2.3 that the footnote on page 31 did not reconcile because $383 + 167 + 728 + 30 + 116 = 1,424 \ne 597$.
Our independent algebraic verification confirms that portfolio amortisation represents **net asset run-off** (Collections less Income):
$$\begin{aligned}
\text{Note 1.1 Net Run-off} &= \text{Net Collections (R728m)} - [\text{CAEIR Interest (R383m)} - \text{Impairment Loss (R167m)}] \\
&= 728 - 216 = \mathbf{\text{R}512\text{m}} \\
\text{Note 1.2 Net Run-off} &= \text{Cash Collections (R116m)} - \text{Fair Value Gain (R30m)} = \mathbf{\text{R}86\text{m}} \\
\hline
\mathbf{\text{Total Portfolio Amortisation}} &= 512 + 86 = \mathbf{\text{R}598\text{m}} \quad (\approx \text{R}597\text{m reported, within R1m rounding})
\end{aligned}$$
DeepSeek's claim was a failure to apply basic negative/positive accounting signs.

---

### 3.3 Debt, Maturity Wall, and Liquidity Breakdown
We audited Note 2 (physical pages 14–15):

| Debt Tranche / Facility | Balance (Rm) | Rate / Margin | Maturity Date | Collateral Pledged |
| :--- | :---: | :--- | :--- | :--- |
| **Notes (Senior Bullet)** | 671 | 3M JIBAR + 2.8% to 3.7% | 31/12/2026 to 31/03/2032 | 100% PBDs, trade receivables, cash |
| **Notes (Senior Amortising)** | 151 | 3M JIBAR + 3.0% to 3.1% | 29/09/2028 | 100% PBDs, trade receivables, cash |
| **Loans (Senior Amortising)** | 1,738 | 3M JIBAR + 2.85% to 5.2% | 30/06/2026 to 31/12/2030 | 100% PBDs, trade receivables, cash |
| **Loans (Senior Bullet)** | 690 | 3M JIBAR + 3.0% to 3.28% | 31/12/2026 to 28/06/2030 | 100% PBDs, trade receivables, cash |
| **Loans (Senior Revolving Facility)** | 297 | Prime − 0.25% to 0.35% | 30/09/2028 | 100% PBDs, trade receivables, cash |
| **Subordinated Debt (Amortising & Bullet)**| 196 | 3M JIBAR + 4.6% to 5.0% | 31/03/2027 to 29/09/2028 | Unsecured / Subordinated |
| **Bank Overdrafts** | 273 | Floating overdraft rates | On demand / Rolling | 100% PBDs, trade receivables, cash |
| **Total Gross Debt** | **4,016** | **~9.1% weighted average** | | **100% Floating Rate (0% Hedges)** |

**Refinancing Wall & Liquidity Gap Re-verification:**
* **Debt Payable Within 12 Months:** **R1,396m** (p. 14).
* **Liquid Resources Available:**
  - Cash and cash equivalents: R112m
  - Verified undrawn bank overdraft facilities: R475m
  - Total verified liquidity: **R587m**.
* **Near-Term Refinancing Gap:**
  $$\text{Gap} = \text{R}1,396\text{m} - \text{R}587\text{m} = \mathbf{\text{R}809\text{m}}$$
* **Management Liquidity Claim:** Commentary cites `"~R0.8 billion in unutilised facilities"`. Since only R475m of overdraft is confirmed in the notes, R325m remains uncorroborated.

---

### 3.4 Earnings, Share Count, and Net Asset Value (NAV)
* **Shares in Issue:** 784,313,242 gross ordinary shares (p. 16).
* **Treasury Shares Held:** 3,662,209 shares acquired in H1 2026 at R1.00/share for the Conditional Share Plan.
* **Net Outstanding Shares:** 780,651,033 shares (used as 780.7m in valuation note).
* **Weighted Average Ordinary Shares:** 782.1m (basic and headline LPS denominator).
* **True Book Value vs. Contributed Share Capital:**
  $$\text{Gross Ordinary Share Capital} = \text{R}5,410\text{m} \implies \text{R}5,410\text{m} / 780.65\text{m} = \mathbf{\text{R}6.93\text{/share}}$$
  $$\text{Retained Loss (Accumulated Deficit)} = -\text{R}4,111\text{m}$$
  $$\text{Other Reserves} = +\text{R}30\text{m}$$
  $$\mathbf{\text{Total Statutory Equity}} = \mathbf{\text{R}1,329\text{m}} \implies \text{R}1,329\text{m} / 780.65\text{m} = \mathbf{\text{R}1.70\text{/share}}$$
DeepSeek's claim that shares were bought at R1 vs "R6.90 book value" was a gross conceptual error: R6.90 is contributed capital before R4.1bn of accumulated losses!

---

### 3.5 Market Comparison & Dynamic Rating Thresholds
* **Reference Price in Note:** R0.89.
* **Live Market Price (`NTU.JO`):** **R0.90** (27 October 2026).
* **12-Month Target Price:** R0.55.
* **Target Implied Upside:**
  - Relative to Reference Price (R0.89): **-38.2%**.
  - Relative to Live Market Price (R0.90): **-38.9%**.
* **Forward Dividend Yield:** **0.0%** (suspended).
* **Expected 12M TSR:** **-38.9%**.
* **Monotonic Dynamic Rating Bands:**
  - Strong Buy: $\le \text{R}0.42$
  - Buy: $\le \text{R}0.48$
  - Hold: $\le \text{R}0.58$
  - Sell: $\le \text{R}0.65$
  - Strong Sell: $> \text{R}0.65$
* **Recommendation Divergence:**
  At live price **R0.90** (and at reference R0.89), the price is strictly above R0.65. The dynamic rating is **`STRONG SELL`**. DeepSeek's static JSON note stated `SELL`.

---

## 4. Findings and Evaluator Revisions

| Finding ID | Linked Claims | Original Statement in Analysis | Supported Correction / Forensic Determination | Severity | Quantified Impact | Earliest Origin |
| :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **F001** | C017, C018 | SOTP table deducts 25% discount, yields R1.07, then asserts 1.07*(1-0.25)=0.80, and slaps 31% haircut to R0.55 (`Stage 2, §4`) | **Double-Discounting and Unmodeled Haircut**: DeepSeek applied a 25% discount twice and added an unmodeled 31.5% haircut. Cumulative discount is 61.5% from R1.43. Additionally, a circular plug of R1,479m was inserted into SOTP to match book value. | **CRITICAL** | Target price is mathematically unanchored; True single-discount SOTP yields R1.07. Target of R0.55 represents 0.38x book value. | Stage 2 Model |
| **F002** | C008 | ECL coverage on principal book collapsed from 20.4% to 12.6% (`Stage 1, §2.1`) | **Accounting Misclassification of POCI Cumulative Gain**: R431m is an accumulated IFRS 9 outperformance gain above acquisition base case, NOT a conventional loan loss reserve. | **HIGH** | Conceptual credit error. Collections are deteriorating (gain shrinking by R167m), but coverage % math is false. | Stage 1 Audit |
| **F003** | C013 | Treasury shares bought at R1 vs ~R6.90 book value (`Stage 1, §1`, `Stage 2, §1`) | **Conflation of Contributed Capital with NAV**: R6.90 is gross share capital per share. True statutory book value per share is R1.70 after deducting R4,111m accumulated losses. | **MEDIUM** | Overstates book value anchor by 4.1x in narrative commentary. | Stage 1 Audit |
| **F004** | C009 | Note 7 amortisation footnote does not arithmetically reconcile (sums to 1,424m not 597m) (`Stage 1, §2.3`) | **Arithmetic Sign Error by Evaluator**: Footnote describes net run-off (Collections minus Income): $(728 - 383 + 167) + (116 - 30) = 512 + 86 = 598\text{m}$. Footnote is mathematically sound. | **MEDIUM** | Unjustified criticism of company accounting disclosures. | Stage 1 Audit |
| **F005** | C014 | Change % signs on page 3 are confirmed sign errors (`Stage 1, §4`) | **Misinterpretation of Management Variance Convention**: Positive percentages represent favorable P&L variances (cost savings); bracketed represent adverse variances. | **LOW** | Minor audit noise; does not affect valuation numbers. | Stage 1 Audit |
| **F006** | C019 | Note recommendation is static SELL while dynamic band evaluates to STRONG SELL (`Stage 2, JSON`) | **Rating Band Divergence**: At R0.89 and R0.90, price exceeds the R0.65 threshold, requiring STRONG SELL. | **LOW** | Discrepancy between static text and quantitative bands. | Stage 2 Model |

---

## 5. Testable Improvements and Proposed Guardrails

To prevent recurrence of these modeling errors across consumer credit, banking, and diversified financial valuations, we propose three institutional guardrails for user review and codification:

### Guardrail 1: Single-Tier SOTP Discounting & Anti-Plug Mandate
* **Rule Code:** `ALL-SOTP-DISCOUNT-AND-PLUG-ARITHMETIC`
* **Sector:** `all`
* **Title:** Single-Tier SOTP Discounting & Non-Operating Balance Sheet Reconciliation
* **Explicit Mandate:** 
  > *"When conducting a Sum-of-the-Parts (SOTP) valuation, corporate governance, liquidity, or conglomerate discounts must be applied strictly once (either at the aggregate equity value level or at the per-share level, never both). Analysts are forbidden from applying cascading percentage discounts or qualitative post-calculation haircuts without underlying DCF or multiple adjustments. Furthermore, non-operating balance sheet add-backs must explicitly tie to audited balance sheet lines and must never be used as a circular plug to force SOTP equity value to match book value."*
* **Confirmed Failure Addressed:** Nutun 1H26 SOTP applied 25% discount to equity, divided by shares to get R1.07, applied 25% again to get R0.80, and then took a 31.5% haircut to R0.55, alongside a R1,479m circular balance sheet plug.
* **Trigger:** SOTP valuation schedules containing percentage discounts or non-operating asset adjustments.
* **Pass Example:** Adjusted Equity R1,115m less 25% discount = Target Equity R836m / 780.7m shares = R1.07 Target Price.
* **Fail Example:** R1.43 per share less 25% = R1.07, then $1.07 \times 0.75 = \text{R}0.80$, then haircut to R0.55.
* **Implementation Point:** Evaluator `evaluate_stock.py` (`CHK-SOTP-MATH`) and Stage 2 Prompt (`workflow/generate_stage2.py`).

### Guardrail 2: POCI Accounting Distinction (Gain vs. Loss Reserve)
* **Rule Code:** `CONSUMER-LENDING-POCI-GAIN-VS-ECL-RESERVE`
* **Sector:** `consumer_lending`
* **Title:** POCI Financial Assets Cumulative Impairment Gain vs. ECL Allowance
* **Explicit Mandate:** 
  > *"For purchased credit-impaired (POCI) debt portfolios under IFRS 9, models must explicitly distinguish between cumulative impairment gains (favourable collections above acquisition pricing) and credit loss allowances. Analysts must not divide a cumulative impairment gain by gross carrying value to construct an artificial 'ECL coverage ratio', nor describe an unwinding gain as a 'coverage collapse' without disclosing that the asset is carried at a premium to amortised acquisition cost."*
* **Confirmed Failure Addressed:** DeepSeek treated Nutun's R431m cumulative impairment gain as an ECL loss allowance and calculated an invalid 12.6% coverage ratio.
* **Trigger:** Valuation or forensic audit of debt purchasers / POCI portfolios.
* **Pass Example:** Disclosing that cumulative impairment gains fell from R598m to R431m due to R191m deterioration in historical collections.
* **Fail Example:** Reporting that ECL coverage on the principal book collapsed from 20.4% to 12.6%.
* **Implementation Point:** Stage 1 Forensic Prompt (`workflow/export_stage1.py`) and Sector Guardrails.

### Guardrail 3: Statutory NAV vs. Contributed Share Capital
* **Rule Code:** `ALL-EQUITY-NAV-VS-CONTRIBUTED-CAPITAL`
* **Sector:** `all`
* **Title:** Net Asset Value (NAV) Attribution & Accumulated Deficit Recognition
* **Explicit Mandate:** 
  > *"When reporting Book Value per share or Net Asset Value (NAV), models must calculate the metric strictly as Total Equity attributable to parent ordinary shareholders divided by net shares in issue. Analysts are strictly forbidden from dividing gross contributed Share Capital alone by share count while ignoring Retained Losses or Accumulated Deficits."*
* **Confirmed Failure Addressed:** DeepSeek asserted that treasury shares were acquired at R1 vs "R6.90 book value" by dividing Share Capital alone (R5,410m) by shares, ignoring R4,111m of retained losses (true NAV was R1.70).
* **Trigger:** Valuation notes citing Book Value, NAV, or P/B ratios.
* **Pass Example:** Stating book value is R1.70/share ($\text{R}1,329\text{m} / 780.7\text{m}$).
* **Fail Example:** Stating book value is R6.90/share ($\text{R}5,410\text{m} / 784.3\text{m}$).
* **Implementation Point:** Evaluator checks and Stage 1 / Stage 2 prompts.

---

## 6. Decision and Saved Handoff to Codex

### 6.1 Evaluation Conclusion: `CORRECTIONS REQUIRED`
The independent forensic audit of Nutun Limited (`1H26`) concludes that **corrections are required**. While DeepSeek's high-level investment thesis (**SELL / STRONG SELL**, high-risk covenant-sensitive debt purchaser, negative operating cash flow, R809m near-term funding gap) is fully supported by the primary evidence, its quantitative valuation mechanics suffer from three critical defects:
1. **Double-discounting and qualitative haircutting** in the SOTP schedule (a cumulative 61.5% discount and R1,479m circular plug to force R0.55).
2. **Accounting misclassification of IFRS 9 POCI cumulative impairment gains** as conventional ECL coverage.
3. **Severe distortion of Net Asset Value** (conflating R6.90 share capital with R1.70 book value).

### 6.2 Target Price & Recommendation Status
* **Directional Recommendation:** **`STRONG SELL`** remains robustly supported by fundamental evidence (statutory operating cash flow of R(111)m, R1,396m maturing debt vs R587m liquid resources, 100% asset encumbrance, loss-making SA segment).
* **Target Price Reproducibility:** The target price of **R0.55** is an unmodeled distress anchor (0.38x book value). A single-discount SOTP yields **R1.07** (+18.9% upside vs R0.90 live). To support R0.55 rigorously, the valuation must either explicitly model the distressed PBD liquidation haircut directly in the asset multiple (e.g. 0.30x PBD multiple) rather than through arbitrary cascading discounts, or adopt an explicit distressed P/B multiple of 0.32x on statutory NAV (R1.70).

### 6.3 Handoff Package for Codex Review
The complete evaluation state has been preserved for Codex review:
1. **Audit Record:** `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T163950Z_gemini/audit.md`
2. **Preserved Inputs:** `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T163950Z_gemini/inputs/`
   - Manifest: `inputs/manifest.json`
   - Stage 1 Response: `inputs/NTU_1H26_stage1_audit_response.md`
   - Stage 2 Response: `inputs/NTU_1H26_stage2_valuation_note.md`
3. **Execution Scripts & Outputs:**
   - Calculation Script: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T163950Z_gemini/calculations/reconciliations.py`
   - Calculation Output: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T163950Z_gemini/calculations/reconciliations_output.txt`
