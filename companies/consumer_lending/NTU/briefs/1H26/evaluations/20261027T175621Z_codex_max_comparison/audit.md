# INDEPENDENT EVALUATION AUDIT RECORD — NUTUN LIMITED (NTU) 1H26
## Fresh DeepSeek Stage 1 & Stage 2 Max-Reasoning Comparison Evaluation

**Document ID:** `NTU-1H26-EVAL-20261027T175621Z-GEMINI-AUDIT`  
**Run Directory:** `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T175621Z_codex_max_comparison`  
**Evaluator:** Gemini (`Gemini 3.8 Flash High`)  
**Evaluation Timestamps:** Created UTC: `2026-10-27T18:12:00Z` | Local: `2026-10-27T20:12:00+02:00` (Africa/Johannesburg)  
**Target Entity:** Nutun Limited (`NTU.JO` / Sector: Consumer Lending `JS3020`)  
**Reporting Period:** `1H26` (Six months ended 31 March 2026)  
**Intervention Type:** Combined intervention — DeepSeek `reasoning_effort: max` (ceiling 65,536 tokens, timeout 900s) PLUS 4 newly codified sector guardrails (`ALL-CASH-ROLLFORWARD-CONSISTENCY`, `ALL-SENSITIVITY-REPRODUCIBILITY`, `CONSUMER-LENDING-POCI-GAIN-VS-ECL-RESERVE`, `ALL-EQUITY-NAV-VS-CONTRIBUTED-CAPITAL`) and regenerated prompts using existing section captures/ledger. Improvements cannot and must not be attributed solely to reasoning effort.

---

## 1. Scorecard and Execution Summary

| Metric / Check | Fresh Output Determination | Independent Audit Verdict | Basis & Evidence |
| :--- | :---: | :---: | :--- |
| **Stage 1 Generation** | Completed (`stop`, 145.18s) | **PASS** | 26,937 chars, 22,576 reasoning tokens, no truncation. Saved in `outputs/NTU_1H26_stage1_response.md`. |
| **Stage 2 Generation** | Completed (`stop`, 211.44s) | **PASS** | 20,112 chars, 37,211 reasoning tokens, no truncation. Saved in `outputs/NTU_1H26_stage2_response.md`. |
| **Total Reasoning Tokens** | 59,787 tokens | **PASS** | Stage 1: 22,576 (75.1% of completion); Stage 2: 37,211 (85.5% of completion). High reasoning achieved. |
| **Combined Token Usage & Cost** | 154,238 tokens / \$0.099366 | **PASS** | OpenRouter generation stats verified: Stage 1 \$0.036330, Stage 2 \$0.063037. Provider: `Together`. |
| **Source PDF Preservation** | SHA-256 match | **PASS** | `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc` matches SQLite `reports.sha256`. |
| **Production Baseline Preservation** | Unaltered | **PASS** | SQLite `reports` (R0.55 / SELL) and 36 `sector_guardrails` completely untouched. |
| **Target Price (Published)** | **R0.95** | **CORRECTIONS REQUIRED** | Stated SOTP yields R0.95, but includes an invalid +R276m operating working capital add-back. |
| **Adjusted Forensic Target** | **R0.64** | **SUPPORTED** | Excluding operating working capital add-back yields R0.64 (implied -28.1% vs R0.89 reference). |
| **Reference Price** | R0.89 | **PASS** | Frozen baseline reference price in note. |
| **Dynamic Recommendation** | **HOLD** (at R0.89 / R0.90) | **HOLD for published R0.95; SELL for adjusted R0.64** | Published bands: Strong Buy ≤ 0.73, Buy ≤ 0.83, Hold ≤ 1.00, Sell ≤ 1.12. Matches static HOLD. |
| **Rating Bands Monotonicity** | Strictly monotonic | **PASS** | 0.73 < 0.83 < 1.00 < 1.12. JSON aligns with prose recommendation. |

---

## 2. Inputs, Preservation, and Source Page Inspection Coverage

### 2.1 Cryptographic Verification of Dossier Inputs
All 50 baseline artifacts and original company files in `inputs/manifest.json` were cryptographically re-verified via SHA-256 in `independent_verification.json`:
- **Source PDF:** `companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf` (38 physical pages, SHA-256: `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`) — **VERIFIED MATCH**.
- **Preserved Original Briefs:**
  - Original Stage 1 response (`9487e50a4dd...`) — **VERIFIED**.
  - Original Stage 2 note (`3ebf5454d04...`) — **VERIFIED**.
  - Original Stage 1 prompt (`c52f4c07224...`) & Stage 2 prompt (`2807744b985...`) — **VERIFIED**.
- **Preserved Prior Independent Audits:**
  - Gemini Evaluation `20261027T163950Z_gemini` (all 3 files) — **VERIFIED**.
  - Codex Review `20261027T164527Z_codex` (all 43 files) — **VERIFIED**.
- **Database & Prompt Snapshot:** `inputs/analysis_snapshot.sqlite`, `inputs/sections_and_ledger.json`, `inputs/guardrails.json` (36 rules) — **VERIFIED**.

### 2.2 Inspection Log & Physical PDF Coverage
- **Total Physical Pages in Source Report:** 38 pages.
- **Physical Pages Examined Directly:**
  - `pp. 1–5`: Cover, table of contents, highlights, operational review, and liquidity commentary.
  - `pp. 6–7`: Basis of preparation (IAS 34 unaudited/unreviewed status).
  - `p. 8`: Balance sheet (Condensed statement of financial position at 31 March 2026).
  - `pp. 9–10`: Income statement (Condensed statement of comprehensive income).
  - `p. 11`: Statement of changes in equity (treasury shares and retained loss).
  - `p. 12`: Statement of cash flows (operating, investing, and financing cash flows).
  - `p. 13`: Note 1 — Purchased Book Debts (Principal book, other financial assets, additions, collections).
  - `pp. 14–15`: Note 2 — Interest-bearing liabilities, overdrafts, maturity profile, facility pledges.
  - `p. 16`: Note 3 — Ordinary share capital and treasury share transactions.
  - `p. 17`: Note 4 — Revenue disaggregation by geography and service line.
  - `pp. 18–19`: Note 5 — Basic, diluted, and headline loss per share reconciliations.
  - `pp. 20–25`: Note 6.1 — Financial risk management, credit risk, POCI valuation, trade receivables ECL.
  - `pp. 26–28`: Note 6.2 & 6.3 — Currency risk and fair value disclosures (18.50% discount rate).
  - `pp. 28–29`: Note 6.4 — Level 3 fair value hierarchy reconciliation.
  - `pp. 30–36`: Note 7 — Segment reporting (Nutun SA CODM vs IFRS, Nutun International).
  - `p. 36`: Notes 8 & 9 — Going concern and subsequent events.
- **Rendered Physical Pages in `calculations/`:** Pages 8, 12, 13, 23, 25, 31 (saved as 1.7x PNGs).
- **Primary Accounting Standards Consulted:** IFRS 9 / AASB 9 paragraphs 5.5.13–15 (POCI accounting and simplified lifetime-ECL approach for trade receivables).

---

## 3. Claim Verification Register (Retaining Stable Comparison IDs C001–C013)

| Claim ID | Claim Under Review & Origin | Classification | Primary Evidence Citation | Independent Re-Verification Performed | Fresh Verdict | Comparison with Baseline, Gemini, & Codex |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **C001** | POCI gain vs ECL reserve classification | Accounting / Historical | PDF pp. 13, 21, 23–24 (Notes 1 & 6.1) | Note 6.1 confirms gross carrying value R3,414m + cumulative gain R431m = net R3,845m. The R431m is an IFRS 9 cumulative outperformance gain, not loss coverage. | **PASS** | **RESOLVED.** Fresh Stage 1 §1.3 & §2.1 and Stage 2 §1 fully adopted the corrected POCI accounting. Corrects original DeepSeek error; supports Gemini's finding with Codex's terminology qualifications. |
| **C002** | Statutory ordinary NAV vs contributed share capital | Accounting / Derived | PDF pp. 8, 16 (Balance sheet & Note 3) | Total equity R1,329m / 780.651033m shares = R1.7024/share. Gross share capital R5,410m / 780.651m = R6.9301/share is contributed capital, ignoring R4,111m retained loss. | **PASS** | **RESOLVED.** Fresh Stage 1 §1.2 & §2.8 and Stage 2 §1 anchor statutory NAV at R1.70/share and explicitly distinguish contributed capital. Corrects original DeepSeek error; supports Gemini and Codex. |
| **C003** | Net run-off amortisation footnote signs | Accounting / Derived | PDF pp. 13, 31 (Note 1 & Note 7 footnote) | Net run-off calculation: (728 - 383 + 167) + (116 - 30) = 512 + 86 = R598m (matches reported R597m within R1m rounding). | **PASS** | **RESOLVED.** Fresh Stage 1 §1.3 & §2.7 recognizes the net run-off signs and confirms the footnote reconciles. Eliminates the false arithmetic failure allegation. |
| **C004** | Valuation bridge, repeated discounts, and circular plug | Valuation Model | Fresh Stage 2 §4 Table 4.1 vs PDF p. 8 | Reconstructed SOTP: PBD (3,268) + Other fin (547) + BPO (680) + Agency (500) = TEV 4,995. Less Net Debt (4,168), Net DTL (340), Other Liab (16), plus Inv (87), Loans (5), Net WC (276) = 839. Less 12% discount = 738 / 780.651m = R0.95. | **PASS for elimination of plug/double discount; FLAG on WC add-back** | **SUBSTANTIALLY IMPROVED.** Completely eliminated the arbitrary R1,479m plug and the repeated 25%+25%+31.5% discounts. However, adding back R276m operating working capital introduces a new distortion (see C012). |
| **C005** | FCFE accounting and collection signs | Cash Flow Forecast | Fresh Stage 2 §3 Table 3.3 vs PDF pp. 12–13 | Table 3.3 explicitly adds cash collections (FY26E 1,714; FY27E 1,660; FY28E 1,710) and subtracts PBD acquisitions (-782; -950; -1,000). Prohibits PBD amortisation add-back. | **PASS** | **RESOLVED.** Fully corrects the catastrophic error identified by Codex in C013 where collections were deducted as outflows. |
| **C006** | Forecast cash roll-forward and balance sheet closes | Financial Statement Integration | Fresh Stage 2 Tables 3.2 & 3.3 | Opening cash + net cash change = closing cash across all periods (106->112->120->130->140). All 5 balance sheet years balance to 0 (Assets == Liab + Equity). Stated FCFE vertical sums match exactly. | **PASS (with minor debt residual)** | **RESOLVED.** Eliminates the unclosed R532m, R810m, and R840m gaps flagged by Codex in C014. Minor residual of R7m to R10m noted between FCFE debt repayment and balance sheet debt/lease reductions. |
| **C007** | Sensitivity matrix reproducibility | Valuation Arithmetic | Fresh Stage 2 §5 Tables 5.1 & 5.2 | Target price formula: `[(4,489 × (1 - hc) + bpo × 170 + 500 + 87 + 276 + 5 - 4,168 - 340 - 16) × 0.88] / 780.651`. All 9 cells in Table 5.1 match the stated formula within R0.01. Central case reproduces R0.95 exactly. | **PASS** | **RESOLVED.** Fully corrects Codex's C015 finding where sensitivity cells did not calculate from the SOTP formula. |
| **C008** | Revenue denominator and geographic scope | Presentation Scope | PDF p. 36 (Note 7) vs fresh reports | UK+US revenue of R515m is 72.4% of IFRS service revenue (R711m), but only 32.2% of CODM total revenue (R1,599m). Fresh Stage 1 and Stage 2 completely omitted the erroneous "72% of group revenue" claim. | **OMITTED DISCUSSION** | **OMITTED, NOT EXPLICITLY RECONCILED.** DeepSeek dropped the misleading claim, avoiding the error, but did not provide the explicit denominator reconciliation requested by Codex. |
| **C009** | Liquidity claims and available facilities | Liquidity Risk | PDF pp. 5, 8, 14–15 (Note 2) | R1,396m matures within 12 months against R475m confirmed undrawn overdraft and R112m cash. 100% PBD principal book pledged. Management claim of ~R0.8bn unutilised facilities is uncorroborated. | **PASS** | **SUPPORTED.** Both fresh stages accurately highlight the maturity wall, encumbrance, and uncorroborated nature of management's ~R0.8bn facility claim. |
| **C010** | Lifetime vs 12-month ECL allegation | Accounting Allegation | PDF pp. 13, 20–21 (Note 6.1) | POCI assets require lifetime ECL under IFRS 9. Nutun models on a rolling 12-month horizon. Fresh Stage 1 characterizes this as a "methodological concern" and marks lifetime adequacy as NOT VERIFIED. | **PASS** | **RESOLVED.** Adopts Codex's qualified phrasing from C017/C010 rather than asserting an unproven statutory breach. |
| **C011** | Rating bands and trading-stop direction | Trading & Recommendation | Fresh Stage 2 JSON & §1 vs §6 | Rating bands (Strong Buy ≤ 0.73, Buy ≤ 0.83, Hold ≤ 1.00, Sell ≤ 1.12, Strong Sell > 1.12) are strictly monotonic and mathematically anchored to R0.95. Dynamic rating at R0.89 is HOLD, matching static note. Inverted short stop removed. | **PASS** | **RESOLVED.** Eliminates rating divergence flagged by Gemini (F006) and the inverted short stop flagged by Codex (C021). |
| **C012** | New errors or omissions in fresh outputs | Valuation Modeling / Integration | Fresh Stage 2 §4 Table 4.1 | DeepSeek added back +R276m Net Trade Working Capital to Enterprise Value in Table 4.1. In EV/EBITDA multiples, operating working capital is embedded in EV. Adding it back treats trade debtors as surplus cash, inflating target by R0.31. | **FAIL (Material Valuation Defect)** | **NEW DEFECT IDENTIFIED.** Double-counts operating working capital in the SOTP equity bridge. Removing it adjusts target price from R0.95 to R0.64. |
| **C013** | Trade-receivable staging inference | Accounting Policy | PDF pp. 20, 25 (Note 6.1) & AASB 9 / IFRS 9 | Fresh Stage 1 §2.1 notes the 90-DPD provisioning threshold as a "lenient policy flag", but refrains from alleging a breach of Stage 2 SICR rules, acknowledging the small book balance (R374m gross, R5m provision). | **PASS as qualified observation** | **RESOLVED WITH RESERVATION.** Softened from original dogmatic allegation, but still does not explicitly recognize the IFRS 9 simplified approach under paragraph 5.5.15. |

---

## 4. Required Independent Reconciliations

### 4.1 Sum-of-the-Parts (SOTP) Reconstruction & Forensic Diagnosis of the Working Capital Add-Back
We independently re-calculated DeepSeek's Table 4.1 SOTP model:

$$\begin{aligned}
\text{PBD Principal Book} &= \text{R}3,845\text{m} \times (1 - 0.15) = \text{R}3,268.25\text{m} \quad (\text{Table: R}3,268\text{m}) \\
\text{Other Financial Assets} &= \text{R}644\text{m} \times (1 - 0.15) = \text{R}547.40\text{m} \quad (\text{Table: R}547\text{m}) \\
\text{Nutun International BPO} &= \text{R}170\text{m (FY27E EBITDA)} \times 4.0\text{x} = \text{R}680.00\text{m} \\
\text{Nutun SA Agency Platform} &= \text{R}100\text{m (FY27E EBITDA)} \times 5.0\text{x} = \text{R}500.00\text{m} \\
\hline
\mathbf{\text{Total Enterprise Value (TEV)}} &= 3,268 + 547 + 680 + 500 = \mathbf{\text{R}4,995.00\text{m}}
\end{aligned}$$

**Bridge from Enterprise Value to Equity Value:**
$$\begin{aligned}
\text{Add: Equity Accounted Investments (BS p. 8)} &= +\text{R}87.00\text{m} \\
\text{Add: Other Loans Receivable (BS p. 8)} &= +\text{R}5.00\text{m} \\
\text{Add: Net Trade Working Capital (Receivables 497 - Payables 221)} &= +\text{R}276.00\text{m} \quad \mathbf{[\text{DEFECT: Double-Count}]} \\
\text{Less: Net Debt (Borrowings 3,743 + Overdraft 273 + Leases 345 - Cash 112 - Inv 81)} &= -\text{R}4,168.00\text{m} \\
\text{Less: Net Deferred Tax Liabilities (DTL 513 - DTA 173)} &= -\text{R}340.00\text{m} \\
\text{Less: Other Liabilities (Current Tax 5 + Derivatives 9 + Net Held-for-Sale 2)} &= -\text{R}16.00\text{m} \\
\hline
\mathbf{\text{Equity Value Before Liquidity Discount}} &= \mathbf{\text{R}839.00\text{m}} \\
\text{Less: 12\% Liquidity / Refinancing Discount} &= -\text{R}100.68\text{m} \quad (\text{Table rounds to } -\text{R}101\text{m}) \\
\mathbf{\text{Equity Value After Discount}} &= \mathbf{\text{R}738.00\text{m}} \\
\text{Ordinary Shares in Issue (Net of 3.662m Treasury Shares)} &= 780.651033\text{m} \\
\mathbf{\text{Published SOTP Target Price}} &= \text{R}738.00\text{m} / 780.651033\text{m} = \mathbf{\text{R}0.9454 \approx \text{R}0.95}
\end{aligned}$$

#### Forensic Analysis of Claim C012 (Working Capital Double-Count):
- In corporate finance theory, when an operating business (BPO and Agency) is valued via an **EV/EBITDA multiple**, the enterprise value already encompasses the necessary working capital required to generate that EBITDA.
- Trade receivables of R497m are operational receivables from agency debt collection and BPO clients. They are not excess cash.
- Adding back Net Trade Working Capital (+R276m) treats working capital as non-operating surplus cash, double-counting the asset.
- **Counterfactual SOTP Target Price (Excluding Operating Working Capital):**
  $$\text{Adjusted Pre-Discount Equity} = \text{R}839.00\text{m} - \text{R}276.00\text{m} = \text{R}563.00\text{m}$$
  $$\text{Adjusted Post-12\% Discount Equity} = \text{R}563.00\text{m} \times 0.88 = \text{R}495.44\text{m}$$
  $$\mathbf{\text{Adjusted Target Price}} = \text{R}495.44\text{m} / 780.651033\text{m} = \mathbf{\text{R}0.6346 \approx \text{R}0.64}$$
- The working capital add-back artificially elevates the target price from **R0.64** to **R0.95** (+R0.31 per share). At R0.64, the stock would be rated **SELL** (implied downside of -28.1% vs R0.89 reference, or -28.9% vs R0.90 live).

---

### 4.2 Sensitivity Matrix & SOTP Formula Reproducibility
We verified the sensitivity formula documented in Table 5.2:
$$\text{Target Price} = \frac{\left[4,489 \times (1 - \text{Haircut}) + \text{Multiple} \times 170 + 500 + 87 + 276 + 5 - 4,168 - 340 - 16\right] \times 0.88}{780.651}$$

| PBD Haircut | BPO Multiple 3.0x | BPO Multiple 4.0x | BPO Multiple 5.0x | Recomputed Central Case | Published Central Case |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **10%** | R1.01 | R1.20 | R1.39 | — | — |
| **15%** | R0.75 | **R0.95** | R1.14 | **R0.9454 (R0.95)** | **R0.95** |
| **20%** | R0.50 | R0.69 | R0.89 | — | — |

All 9 cells calculate directly from the formula and match the published table within R0.01 rounding tolerance. The central case reproduces the R0.95 target exactly.

---

### 4.3 DCF Cross-Check Mathematical Verification
We verified the DCF schedule presented in Table 4.2:
$$\text{Terminal Value at FY28E} = \frac{\text{R}330\text{m} \times (1 + 0.02)}{0.18 - 0.02} = \frac{\text{R}336.60\text{m}}{0.16} = \mathbf{\text{R}2,103.75\text{m}} \quad (\text{Table: R}2,104\text{m})$$
$$\text{PV of FY27E FCFE} = \frac{\text{R}260\text{m}}{1.18^1} = \mathbf{\text{R}220.34\text{m}} \quad (\text{Table: R}220\text{m})$$
$$\text{PV of FY28E FCFE} = \frac{\text{R}330\text{m}}{1.18^2} = \frac{\text{R}330\text{m}}{1.3924} = \mathbf{\text{R}237.00\text{m}} \quad (\text{Table: R}237\text{m})$$
$$\text{PV of Terminal Value} = \frac{\text{R}2,103.75\text{m}}{1.18^2} = \mathbf{\text{R}1,510.88\text{m}} \quad (\text{Table: R}1,511\text{m})$$
$$\text{Total Equity Value} = 220.34 + 237.00 + 1,510.88 = \mathbf{\text{R}1,968.22\text{m}} \quad (\text{Table: R}1,968\text{m})$$
$$\mathbf{\text{DCF Value Per Share (at 18\% Cost of Equity)}} = \text{R}1,968.22\text{m} / 780.651\text{m} = \mathbf{\text{R}2.52}$$
- At 25% Cost of Equity: $\text{TV} = \text{R}1,463.48\text{m}$; $\text{Equity} = \text{R}1,355.83\text{m}$; $\mathbf{\text{Per Share}} = \mathbf{\text{R}1.74}$ (matches table).
- At 30% Cost of Equity: $\text{TV} = \text{R}1,202.14\text{m}$; $\text{Equity} = \text{R}1,106.59\text{m}$; $\mathbf{\text{Per Share}} = \mathbf{\text{R}1.42}$ (matches table).
The DCF arithmetic is 100% reproducible and internally consistent.

---

### 4.4 Cash Flow and Balance Sheet Closed Bridges
- **FCFE Bridge (Table 3.3):** Vertical summation confirmed exact across all columns:
  - 1H26A: $-63 + 68 + 167 - 383 - 30 + 844 - 410 - 30 - 23 = \text{R}140\text{m}$ (Stated: R140m).
  - FY26E: $-100 + 140 + 337 - 763 - 55 + 1,714 - 782 - 50 - 245 = \text{R}196\text{m}$ (Stated: R196m).
  - FY27E: $-15 + 140 + 280 - 680 - 30 + 1,660 - 950 - 50 - 95 = \text{R}260\text{m}$ (Stated: R260m).
  - FY28E: $75 + 140 + 250 - 620 - 30 + 1,710 - 1,000 - 50 - 145 = \text{R}330\text{m}$ (Stated: R330m).
- **Cash Equivalents Rollforward:** Opening + Net change = Closing cash across all forecast periods:
  - FY26E: $112 + 8 = 120$ (Matches balance sheet R120m).
  - FY27E: $120 + 10 = 130$ (Matches balance sheet R130m).
  - FY28E: $130 + 10 = 140$ (Matches balance sheet R140m).
- **Balance Sheet Equality (Table 3.2):** Total Assets == Total Liabilities + Total Equity across all 5 columns:
  - FY25A: $6,604 = 5,208 + 1,396 \implies \text{Diff} = 0$.
  - 1H26A: $6,444 = 5,115 + 1,329 \implies \text{Diff} = 0$.
  - FY26E: $6,169 = 4,940 + 1,229 \implies \text{Diff} = 0$.
  - FY27E: $5,924 = 4,710 + 1,214 \implies \text{Diff} = 0$.
  - FY28E: $5,699 = 4,410 + 1,289 \implies \text{Diff} = 0$.

---

## 5. Findings and Evaluator Comparison

### 5.1 Evaluator Revisions and Cross-Model Benchmark
1. **Gemini Findings Assessed Against Fresh Outputs:**
   - Gemini F001 (Double-discounting & plug): **REMEDIATED BY DEEPSEEK**. The arbitrary plug and double discounts were eliminated. However, Gemini's proposed alternative target of R1.07 was rejected because it retained the original R1,479m plug.
   - Gemini F002 (POCI cumulative gain vs ECL reserve): **SUPPORTED & ADOPTED**. DeepSeek corrected the accounting treatment in Stage 1 and Stage 2.
   - Gemini F003 (NAV vs contributed capital): **SUPPORTED & ADOPTED**. DeepSeek correctly established R1.70 statutory NAV.
   - Gemini F004 (Amortisation footnote signs): **SUPPORTED & ADOPTED**. DeepSeek confirmed the footnote reconciles as net run-off.
   - Gemini F006 (Rating band mismatch): **SUPPORTED & RESOLVED**. Monotonic bands and JSON now perfectly align with the note's HOLD recommendation.
2. **Codex Review Findings Assessed Against Fresh Outputs:**
   - Codex C013 (Collection signs in FCFE): **REMEDIATED BY DEEPSEEK**. Collections are now properly added as inflows and acquisitions subtracted as reinvestment.
   - Codex C014 (Cash roll-forward gaps): **REMEDIATED BY DEEPSEEK**. Cash balances now roll forward cleanly without unexplained R532m/R810m/R840m gaps.
   - Codex C015 (Sensitivity reproduction): **REMEDIATED BY DEEPSEEK**. Sensitivity matrix now calculates directly from the base SOTP formula.
   - Codex C016 (Revenue denominator scope): **OMITTED DISCUSSION**. DeepSeek omitted the erroneous 72% claim rather than explaining the denominator.
   - Codex C021 (Inverted short stop): **REMEDIATED BY DEEPSEEK**. The inverted stop was removed.
   - Codex C013/F003 (Trade receivable staging inference): **REVISED BY DEEPSEEK**. Softened from an alleged breach to a "lenient policy flag".

### 5.2 Summary of Findings in the Fresh Run
- **F001 (Operational / Execution): PASS.** Both stages completed cleanly via OpenRouter (`Together` provider) with high reasoning token usage (59,787 tokens) and zero truncation.
- **F002 (Accounting Baseline Remediation): PASS.** Massive improvement over the preserved baseline; all 4 codified guardrails were respected.
- **F003 (SOTP Working Capital Double-Count): FAIL / MATERIAL DEFECT.** Adding back +R276m operating working capital in Table 4.1 inflates the target price by R0.31 per share (R0.95 vs R0.64).
- **F004 (Forecast Debt Rollforward Residuals): MINOR OBSERVATION.** A small residual of R7m to R10m per period remains between stated FCFE debt repayment and balance sheet debt/lease reductions.

---

## 6. Decision and Handoff

### Independent Conclusion: **CORRECTIONS REQUIRED**
While the fresh DeepSeek max-reasoning run repaired virtually all previous accounting and financial modeling failures (eliminating the circular plug, double discounts, sign errors, cash roll-forward gaps, and unclosed balance sheets), the published target price of **R0.95** cannot be validated without correcting the **+R276m Net Trade Working Capital double-count** in the SOTP schedule. 

- **Published Target Price:** R0.95 (HOLD at reference price R0.89 / +6.7% upside).
- **Forensically Corrected Target Price:** **R0.64** (-28.1% downside vs R0.89 reference, or -28.9% vs R0.90 live -> dynamic band evaluates to **SELL**).
- **Recommendation:** Do not synchronize SQLite `reports` or codify new guardrails at this stage. Codex should independently review this audit record, verify the working capital double-count in Table 4.1, and determine whether a final rerun is warranted.

### Preserved Artifacts for Codex Independent Review:
- Run Directory: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T175621Z_codex_max_comparison/`
- Audit Record: `audit.md` (this file)
- Stage 1 Output: `outputs/NTU_1H26_stage1_response.md`
- Stage 1 Metadata: `outputs/NTU_1H26_stage1_response.run.json` & `outputs/stage1_generation_stats.json`
- Stage 2 Output: `outputs/NTU_1H26_stage2_response.md`
- Stage 2 Metadata: `outputs/NTU_1H26_stage2_response.run.json` & `outputs/stage2_generation_stats.json`
- Verification Record: `independent_verification.json`
- Calculation Script & Output: `calculations/reconciliations.py` & `calculations/reconciliations_output.json`
- Rendered Primary Pages: `calculations/page_08.png`, `page_12.png`, `page_13.png`, `page_23.png`, `page_25.png`, `page_31.png`
