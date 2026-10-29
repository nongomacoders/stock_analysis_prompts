# Gemini Independent Evidence Audit: Section Reading Prompt Paired Pilot (NTU & PAN)

**Evaluation Verdict:** **SUPPORTED FOR FULL NTU TRIAL — SPECIFIC FIRST-PASS IMPROVEMENTS CONFIRMED; TARGETED REUSABLE PROMPT TWEAKS IDENTIFIED**  
**Evaluation Timestamp (UTC):** `2026-10-28T17:00:32Z`  
**Evaluation Local Time:** `2026-10-28T19:00:32+02:00` (Africa/Johannesburg)  
**Evaluator:** Gemini (`Gemini 3.8 Flash (High)`, executing locally in Antigravity)  
**Subject Evaluated:** Paired section-reading prompt comparison pilot (`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot/`)  
**Primary Source Documents:**  
1. Nutun Limited 1H26 Condensed Consolidated Interim Financial Statements (`nutunlimitedcondensedconsolidatedafs31march2026.pdf`, SHA-256 `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`)  
2. Pan African Resources PLC FY2026 Year-End Results SENS Announcement (`Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf`, SHA-256 `62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`)  
**Audit Path:** `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T170032Z_gemini/audit.md`  
**Supporting Calculations Script:** `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T170032Z_gemini/calculations/reconciliations.py` (Outputs in `calculations/reconciliation_output.json`)

---

## 1. Operating Protocol & Executive Scorecard

### Section-Reading Prompt Paired Pilot — Operational Scorecard

**Pilot Status:** [✓ `PASSED`] &nbsp;|&nbsp; **Sectors Tested:** `consumer_lending` (NTU), `mining` (PAN) &nbsp;|&nbsp; **Valuation Status:** `N/A (Section Brief Pilot)`

| Metric | Pilot Determination | Baseline Comparison & Basis |
| :--- | :---: | :--- |
| **Total Calls Completed** | **8 / 8 (100%)** | 4 paired identical captures on Fireworks (`deepseek-v4.1-flash-1017`, `reasoning: none`) |
| **Ledger Syntax / Literal Pass Rate** | **4 / 4 (100.0%)** | Old prompt: 3 / 4 (75.0%); old NTU shared-page failed strict literal quote validation |
| **Proposed Verification Questions** | **12 questions** | Old prompt: 26 questions (**-53.8% reduction** in ledger question clutter) |
| **Prompt Template Size** | **90,892 characters** | Old prompt: 109,642 characters (**-17.1% character reduction**) |
| **Completion Tokens Generated** | **9,165 tokens** | Old prompt: 13,655 tokens (**-32.9% token reduction**) |
| **Summed Generation Latency** | **39.280s** | Old prompt: 55.522s (**-29.3% elapsed wall-time reduction**) |
| **Summed Generation Cost** | **US$0.012841** | Old prompt: US$0.017169 (**-25.2% cost reduction**, corroborated by metadata) |
| **Secondary Topic Coverage** | **Preserved (100%)** | NTU p.25 Note 6.2 currency risk captured and linked to `Pending: p.26` |
| **Forecast / Target Price** | **`N/A`** | No forecast, DCF, or valuation was attempted in this first-pass reading pilot |

---

### Forensic Audit Checks

| Check Code | Check Description | Result | Details / Observations |
| :--- | :--- | :---: | :--- |
| **`CHK-PRICE-SYNC`** | Market Price & Upside Alignment | **[N/A]** | Section-reading prompt pilot only; no valuation note or target price generated. |
| **`CHK-BANDS-MONO`** | Rating Bands Monotonicity | **[N/A]** | No rating bands generated in this pilot. |
| **`CHK-SOTP-MATH`** | SOTP Vertical Arithmetic & Sign Integrity | **[N/A]** | SOTP not applicable to section reading briefs. |
| **`CHK-GUARDRAILS`** | Active Sector Guardrails Compliance | **[⚠️ FLAG]** | Sector note successfully eliminated NIM/ABS/originator noise, but DeepSeek still raised a POCI ECL staging question (`Q-b332e6c7ddfc4e8d`). |
| **`CHK-TEXT-CLEAN`** | LLM Stutter & Format Cleanliness | **[✓ PASS]** | Clean 4-part markdown structure; no markdown table pipe corruption, HTML tags, or token repetition loops. |
| **`CHK-PROMPT-REDUCTION`**| Prompt & Token Compression | **[✓ PASS]** | Prompt characters reduced by 17.10%; completion tokens reduced by 32.88%; elapsed time reduced by 29.25%. |
| **`CHK-LEDGER-VALID`** | Strict JSON Ledger Quote Verification | **[✓ PASS]** | 4/4 valid ledgers under revised prompt vs 3/4 under old prompt (which failed on a non-literal quote). |

---

## 2. Scope, Evidence Preservation, and Methodology

### 2.1 Preserved Inputs and Document Hashes
The pilot evaluated four paired captures across two companies and two sectors using identical text extractions and stored question conditions:
1. **NTU Physical Page 13 (`ntu_portfolio`)**: Note 1 (Purchased book debts), covering principal book portfolios and other financial assets at FVTPL.
2. **NTU Physical Page 25 (`ntu_shared_page`)**: Note 6.1 (Credit risk: trade receivables ECL matrix) and the beginning of Note 6.2 (Currency risk).
3. **PAN Physical Pages 38–39 (`pan_apm`)**: Alternative Performance Measures (APMs) definitions and Group all-in sustaining costs (AISC) table.
4. **PAN Physical Pages 48–50 (`pan_operations`)**: Group production summary table across mining and surface operations.

**Primary PDF Documents Verified:**
- NTU: `nutunlimitedcondensedconsolidatedafs31march2026.pdf` (38 pages, SHA-256: `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`).
- PAN: `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` (54 pages, SHA-256: `62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`).
- Both PDF hashes match the SQLite production records and stored plan manifests. Original PDFs were verified read-only and untouched.

**Physical Pages Independently Examined by Evaluator:**
- Nutun Limited: **Physical pages 13 and 25** (PDF page indices 12 and 24).
- Pan African Resources: **Physical pages 38, 39, 48, 49, and 50** (PDF page indices 37, 38, 47, 48, and 49).

**Preserved Evaluation Artifacts:**
All 36 input, prompt, request, receipt, and output files from the paired pilot were copied and preserved under `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T170032Z_gemini/inputs/` with complete SHA-256 verification in `inputs/manifest.json`.

---

## 3. Claim Verification Register (C001 – C015)

| Claim ID | Claim and Origin | Classification | Primary Evidence | Independent Check & Method | Verdict | Consequence & Impact |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **C001** | NTU p.13: Principal book portfolio reconciles: `3,975 + 382 additions - 728 net collections + 383 CAEIR - 167 impairment = 3,845` | Historical Result | NTU PDF p.13, Note 1.1; H1 FY26 (Rm) | `3975 + 382 - 728 + 383 - 167 = 3845`. Split: non-current 2,688 + current 1,157 = 3,845. Verified in `reconciliations.py`. | **`PASS`** | Carrying amount ties exactly to balance sheet Note 1. |
| **C002** | NTU p.13: Other financial assets prose reconciles: `702 + 28 additions - 116 collections + 30 fair value = 644` | Historical Result | NTU PDF p.13, Note 1.2; H1 FY26 (Rm) | `702 + 28 - 116 + 30 = 644`. Split: non-current 490 + current 154 = 644. Total book debts = 3,845 + 644 = 4,489. | **`PASS`** | Prose vertical roll-forward ties exactly to primary financial statements. |
| **C003** | NTU p.13: Revised ledger JSON answer states: `702 + 28 - 116 - 30 FV gain = 644` | Model Calculation | NTU `outputs/ntu_portfolio_new.validation.json` | Executed arithmetic: `702 + 28 - 116 - 30 = 584`. Discrepancy of -60m vs claimed 644. Verified in `reconciliations.py`. | **`FAIL`** | **Confirmed Model Error (F002)**: Model wrote a minus sign for FV movement in the ledger string while labeling it "gain" and equating to 644. |
| **C004** | NTU p.13: Model questions `Q-b332e6c7ddfc4e8d` demanding "ECL staging table and coverage ratios" for principal book | Model Assumption | NTU `outputs/ntu_portfolio_new.validation.json` | NTU PDF p.13 Note 1: Principal book consists of POCI written-off consumer debts at deep discount carried at amortised cost under IFRS 9. | **`FAIL`** | **Unsupported Applicability (F003)**: POCI assets do not have 12-month Stage 1 vs Lifetime Stage 2 staging. Sector note warning was unheeded. |
| **C005** | NTU p.25: Trade receivables gross 374, allowance (5), net 369; total loss rate 1.34%; >90 DPD 100.00% (5/5) | Historical Result | NTU PDF p.25, Note 6.1; Rm, 31 Mar 2026 | `374 - 5 = 369`. Loss rate `5 / 374 = 1.3369% ≈ 1.34%`. Current 339, 30d 25, 61-90d 5, >90d 5. | **`PASS`** | Model accurately captured all aging brackets, balances, and loss rates. |
| **C006** | NTU p.25: Model asserts 31 Mar 2025 comparative "limits trend reliability" as a "newly constructed comparative" | Model Assumption | NTU `outputs/ntu_shared_page_new.prose.md` | NTU PDF p.25 Footnote `**`: "The comparative disclosure for 31 March 2025 has been presented for the first time to enhance overall disclosure." | **`FAIL`** | **Unsupported Assertion (F004)**: Standard interim presentation of newly introduced IFRS 7 disclosure does not denote an unverified restatement. |
| **C007** | NTU p.25: Model asserts 0.00% loss rates on current / <=90 DPD buckets is a "material shift in provisioning assumption" | Model Assumption | NTU `outputs/ntu_shared_page_new.prose.md` | NTU PDF p.25: 31 Mar 2026 current gross 339 (allowance -); 30d 25 (-); 61-90d 5 (-); 30 Sep 2025 allowance <1m (<0.2%). | **`FAIL`** | **Unsupported Assertion (F004)**: On corporate trade debtors under simplified ECL, balances <R1m round to dashes; not an unevidenced policy change. |
| **C008** | NTU p.25: Note 6.2 Currency risk introduction captured, noting USD/GBP contracts and cross-referencing `Pending: p.26` | Historical Result | NTU PDF p.25, Note 6.2 | Inspected p.25 bottom section: Currency risk begins with exchange rate table and hedging narrative; continues on p.26. | **`PASS`** | Revised prompt successfully identified secondary shared-page topic without prompt engineering or separate extraction. |
| **C009** | PAN pp.38–39: FY26 AISC lower-cost US$420.686m + higher-cost US$87.718m = stated Group US$508.405m (+0.001 rounding) | Historical Result | PAN PDF p.39, AISC table | `420.686 + 87.718 = 508.404` vs stated `508.405` (0.001m / US$1,000 rounding diff). Ounces: `247,219 + 25,154 = 272,373` (exact). | **`PASS`** | Vertical addition and minor rounding residual verified in `reconciliations.py`. |
| **C010** | PAN pp.38–39: FY26 AISC/oz: Lower-cost US$1,702/oz, Higher-cost US$3,487/oz, Group US$1,867/oz | Derived Calculation | PAN PDF p.39, AISC table | Lower: `420,686,000 / 247,219 = 1,701.67 ≈ 1,702`. Higher: `87,718,000 / 25,154 = 3,487.24 ≈ 3,487`. Group: `508,405,000 / 272,373 = 1,866.58 ≈ 1,867`. | **`PASS`** | Unit costs match published figures exactly. |
| **C011** | PAN pp.38–39: YoY Group AISC/oz up +16.7% (+US$267/oz) while gold sold rose +38.3% (+75,446 oz) | Derived Calculation | PAN PDF p.39, AISC table | AISC: `(1867 - 1600) / 1600 = +16.6875% ≈ +16.7%`. Gold sold: `(272373 - 196927) / 196927 = +38.3116% ≈ +38.3%`. | **`PASS`** | YoY dynamics correctly computed and flagged in revised question `Q-9b071fccf19d4465`. |
| **C012** | PAN pp.48–50: FY26 Total gold produced 272,310 oz reconciles across all 5 operational components | Historical Result | PAN PDF pp.48–49, Production summary | `105,478 (underground) + 2,428 (Barberton surface) + 113,613 (tailings) + 18,667 (buy-in) + 32,124 (Tennant) = 272,310 oz`. | **`PASS`** | Component sum exactly equals published Group total (272,310 oz). |
| **C013** | PAN pp.48–50: FY25 Total gold produced 196,527 oz reconciles across all 5 operational components | Historical Result | PAN PDF pp.48–49, Production summary | `92,643 (underground clean) + 2,654 (Barberton surface) + 98,636 (tailings) + 1,081 (buy-in) + 1,513 (Tennant) = 196,527 oz`. | **`PASS`** | Verified exact component reconciliation in `reconciliations.py`. |
| **C014** | PAN pp.48–50: DeepSeek's claimed "1,573 oz gap" in text and "1,081 oz excess" in ledger question `Q-99e93be7ca7c4594` | Model Calculation | PAN `outputs/pan_operations_new.md` | Primary table analysis: PDF row underground total 93,724 oz already includes 1,081 buy-in (`92,643 + 1,081 = 93,724`). Adding 1,081 buy-in again double-counts it. Double-count (1,081) and missed Barberton surface (2,654): `2,654 - 1,081 = 1,573 oz`. | **`FAIL`** | **Forensic Attribution Resolution (F005)**: The discrepancy is caused by tabular extraction column collapse and model double-counting, NOT company error. |
| **C015** | Prompt Performance: 4/4 valid ledgers, 12 proposed questions, 17.1% shorter prompt, 29.3% faster execution | Model Benchmark | Comparison summary files (`comparison.json`, `calls.csv`) | Checked all 8 API receipt tokens, costs, runtimes, and regex validation passes. Corroborated with `reconciliations.py`. | **`PASS`** | Revised prompt demonstrated superior operational efficiency and adherence to ledger schema. |

---

## 4. Findings and Evaluator Revisions (F001 – F006)

### **F001 — SUPPORTED WITHIN SAMPLE: Operational and Syntactic Superiority of Revised Prompt**
- **Observation:** The revised prompt achieved a 100% (4/4) valid ledger extraction rate compared to 75% (3/4) for the old prompt. The old prompt failed in `ntu_shared_page` because DeepSeek truncated the verbatim quote (`'credit risk is managed by reference to past default experience of the debtor and analysis of the deb'`), triggering a strict rejection by `ledger_verifier.py`. The new prompt produced clean, exact verbatim quotes in all four cases.
- **Efficiency Gains:** Prompt length was reduced from 109,642 to 90,892 characters (-17.10%); completion tokens were compressed from 13,655 to 9,165 (-32.88%); proposed questions were reduced from 26 to 12 (-53.85%); summed latency dropped from 55.522s to 39.280s (-29.25%); and total cost dropped from $0.01717 to $0.01284 (-25.21%).
- **Evaluation Verdict:** **SUPPORTED WITHIN SAMPLE**.

---

### **F002 — CONFIRMED ERROR: Sign Inversion in NTU p.13 Ledger Equation String**
- **Earliest Observable Stage:** Section Analysis (`outputs/ntu_portfolio_new.validation.json`).
- **Description:** In the prose section of `ntu_portfolio_new.prose.md`, DeepSeek correctly performed the signed calculation:  
  `Other FA H1 FY26: 702 + 28 − 116 + 30 = 644 ✓`  
  However, in the structured JSON ledger update for `Q-PILOT-ntu_portfolio`, DeepSeek wrote:  
  `"Other FA H1 FY26: 702 + 28 - 116 - 30 FV gain = 644"`  
- **Mathematical Impact:** Evaluating `702 + 28 - 116 - 30` yields **584**, an arithmetic discrepancy of **-60m** versus the stated 644. DeepSeek inverted the sign of the fair-value adjustment in the equation text while labeling it "FV gain" and asserting equality to 644.
- **Required Correction:** Require signed vertical roll-forward expressions inside ledger `answer` text to undergo strict sign-consistency verification before submission.
- **Evaluation Verdict:** **CONFIRMED ERROR**.

---

### **F003 — UNSUPPORTED APPLICABILITY: Inappropriate Demand for POCI Loan Staging**
- **Earliest Observable Stage:** Section Analysis (`outputs/ntu_portfolio_new.validation.json`).
- **Description:** Question `Q-b332e6c7ddfc4e8d` asks:  
  *"What ECL staging, coverage and vintage/collection-performance disclosure supports the R167m impairment loss on the principal book portfolio in H1 FY26...?"*  
  And demands:  
  *"ECL staging table, coverage ratios, collection-rate assumptions..."*
- **Accounting Ground Truth:** Note 1 explicitly explains that the principal book consists of purchased credit-impaired (POCI) written-off consumer debts purchased at deep discount. Under IFRS 9, POCI financial assets are measured at amortised cost using a credit-adjusted effective interest rate (CAEIR); they do NOT have conventional Stage 1 (12-month ECL) or Stage 2 (SICR) staging classifications.
- **Root Cause:** DeepSeek retains a default reflex to demand commercial bank / originator retail lending staging disclosures on debt-collection portfolios, despite the concise sector note warning: *"Establish instrument and measurement basis before applying staging, coverage... do not treat signed POCI gains or FVTPL changes as conventional ECL reserves."*
- **Evaluation Verdict:** **UNSUPPORTED APPLICABILITY**.

---

### **F004 — UNSUPPORTED ASSERTIONS: Overinterpreting First-Time Interim Comparatives & Rounding**
- **Earliest Observable Stage:** Section Analysis (`outputs/ntu_shared_page_new.prose.md`).
- **Description:** In `ntu_shared_page`, DeepSeek asserts:  
  1. Footnote `**` presenting the 31 March 2025 comparative for the first time *"limits trend reliability — the March 2025 column is a newly constructed comparative, not previously reported."*  
  2. The 0.00% loss rates on Current, 30-day, and 61–90 day trade receivables represent a *"material shift in provisioning assumption"* versus 30 September 2025 (where rates were 0.06%, 0.19%, and 6.67%).
- **Evidence Reality:** Presenting an interim comparative for the first time when a new disclosure format is adopted under IFRS 7 / IAS 34 is standard accounting compliance, not a restatement or sign of poor reporting. Furthermore, on corporate trade receivables of R374m, non-defaulting brackets incurred zero actual defaults; at year-end, the 0.06% and 0.19% allowances represented <R1m of provision, which rounded to dashes (`-`) in the interim reporting table.
- **Evaluation Verdict:** **UNSUPPORTED ASSERTIONS**.

---

### **F005 — RESOLVED FORENSIC ISSUE: Multi-Column Extraction Collapse in PAN Operations**
- **Earliest Observable Stage:** Section Capture / Text Extraction (`inputs/pan_operations.json`).
- **Description:** In `outputs/pan_operations_new.md`, DeepSeek noted a discrepancy where FY25 gold produced components summed to 194,954 oz vs stated 196,527 oz (a 1,573 oz gap), and subsequently raised `Q-99e93be7ca7c4594` stating that summing components gave 197,608 oz (an excess of 1,081 oz).
- **Independent Forensic Determination:** Inspection of PAN PDF pages 48–49 reveals that the 14-column layout caused `extract_structured_text` to concatenate multiple columns and subtotals:
  - Row "Gold produced – underground", column "Group total" states **93,724 oz**. This total already includes 92,643 oz of underground mining plus **1,081 oz of Evander third-party buy-in feedstock** (`92,643 + 1,081 = 93,724 oz`).
  - The extraction also separated "Gold production – surface operations" (Barberton surface) of **2,654 oz**.
  - When DeepSeek added: `93,724 + 2,654 + 98,636 (tailings) + 1,081 (buy-in) + 1,513 (Tennant) = 197,608 oz`, it double-counted the 1,081 oz buy-in feedstock!
  - `197,608 - 196,527 = 1,081 oz excess`.
  - When DeepSeek initially missed the Barberton surface line (2,654 oz), the net difference was: `2,654 - 1,081 = 1,573 oz gap`.
- **Verdict:** The company's published production figures are mathematically exact (`92,643 + 2,654 + 98,636 + 1,081 + 1,513 = 196,527 oz`). DeepSeek appropriately added an attribution warning about shifted extraction columns, but its question misattributed an extraction/subtotal artifact to company reporting error.
- **Evaluation Verdict:** **RESOLVED FORENSIC ATTRIBUTION (EXTRACTION ARTIFACT)**.

---

### **F006 — SUPPORTED USABILITY: Clean 4-Part Structure and Secondary-Topic Continuity**
- **Observation:** The revised prompt structure (1. Key facts and figures; 2. Footnotes, qualifications and reconciliations; 3. Questions answered and next evidence; 4. Updated Open Questions Ledger) eliminates narrative essays while preserving critical analytical context.
- **Secondary Topic Awareness:** On NTU physical page 25, the prompt successfully detected the beginning of Note 6.2 (Currency risk), extracted the relevant USD/GBP exchange rate and hedging facts, and established the appropriate cross-section dependency (`Pending: p.26`), avoiding premature closure or dropped evidence.
- **Evaluation Verdict:** **SUPPORTED WITHIN SAMPLE**.

---

## 5. Answers to Mandatory Review Inquiries

### Inquiry 1: Is the simpler prompt suitable for a full NTU section-sequence trial?
**YES.** The simpler prompt is thoroughly suitable for an end-to-end chronological trial across all sections of Nutun 1H26. 
- It achieves a **100% valid ledger pass rate** on strict literal quote checking, eliminating the fragile quote-repair failures observed under the old template.
- It compresses prompt token overhead by **17.1%** and reduces completion length by **32.9%**, significantly mitigating the risk of downstream completion token exhaustion.
- It slashes question volume by **53.8%** (from 26 to 12 proposed questions in this 4-capture sample), prioritizing high-impact economic drivers (pledge covenants, fair-value techniques, AISC inflation) over trivial checklist noise.
- It successfully identifies and tags secondary topics starting lower on shared pages (e.g. Note 6.2 currency risk).

---

### Inquiry 2: What improved, regressed, or remained unchanged?

| Dimension | Pilot Performance Assessment | Evidence & Metrics |
| :--- | :--- | :--- |
| **Improved** | **Ledger Quote Verification:** 4/4 valid ledgers (100%) vs 3/4 (75%). | Old prompt failed strict quote checking on `ntu_shared_page`; new prompt passed all 4 cases without repair. |
| **Improved** | **Question Prioritization & Clutter Reduction:** 12 questions vs 26 (-53.8%). | Dropped trivial inquiries (e.g. 0.3% non-gold revenue on gold mining APM); focused on group AISC inflation (+16.7%) and debt covenants. |
| **Improved** | **Prompt & Response Compactness:** Prompt chars -17.1%; completion tokens -32.9%. | Eliminated redundant narrative commentary and long checklists; enforced strict 4-section format. |
| **Improved** | **Speed and Cost:** Wall time -29.25% (39.28s vs 55.52s); cost -25.21% ($0.0128 vs $0.0172). | Corroborated across all 8 generation receipts on Fireworks. |
| **Regressed** | **Ledger Equation String Sign Inversion:** Wrote `702 + 28 - 116 - 30 = 644`. | In NTU p.13, prose used correct `+30`, but ledger answer string inverted the sign to `-30` (evaluating to 584). |
| **Unchanged** | **POCI Staging Reflex:** Model still asked for ECL staging on POCI assets. | DeepSeek generated `Q-b332e6c7ddfc4e8d` requesting ECL staging tables on purchased written-off debt despite sector note warning. |
| **Unchanged** | **Tabular Multi-Column Extraction Collapse:** Shifts in complex 14-column tables. | PAN production summary tables with merged headers and subtotals remain distorted in Markdown crops; prompt cannot resolve upstream extraction layout. |

---

### Inquiry 3: What are the smallest reusable changes needed before that trial?

To maximize robustness across companies without introducing company-specific hacks or adding processing layers, the following three minimal, reusable prompt refinements should be applied to the shared prompt template (`prompts/common/12-analyst-reading-brief/v1.1.0/prompt.md`) and consumer lending sector note:

1. **Explicit Equation Sign Consistency Mandate (Shared Prompt Section 2 & 4):**
   - *Prompt Instruction:* "When stating reconciliations or vertical roll-forwards in prose or ledger answer strings, ensure every signed operator (`+` or `-`) matches the economic direction and mathematically evaluates exactly to the stated total (e.g. `opening + additions - collections + fair_value_gain = closing`)."
   - *Rationale:* Directly prevents the confirmed error observed in F002 (`702 + 28 - 116 - 30 = 644`).

2. **Explicit POCI Staging Prohibition (Consumer Lending Sector Note):**
   - *Sector Note Clarification:* "Under IFRS 9, Purchased or Originated Credit-Impaired (POCI) financial assets do NOT have Stage 1 (12-month ECL) or Stage 2 (SICR) staging. Never request ECL staging tables, stage migrations, or conventional ECL coverage ratios for POCI portfolios."
   - *Rationale:* Eliminates the repeated misconception verified in F003 / `Q-b332e6c7ddfc4e8d`.

3. **Standard Interim Comparative Context (Shared Prompt Section 2):**
   - *Prompt Instruction:* "Do not treat standard first-time presentation of comparative disclosures in interim reports as restatements or evidence of unreliable reporting unless an explicit error or prior-period adjustment is stated by management."
   - *Rationale:* Prevents the false alarms verified in F004 regarding NTU's 31 March 2025 comparative figures.

---

## 6. Audit Trail and Preservation Verification

- **Preservation Status:** All original files in `companies/consumer_lending/NTU/sources/completed/1H26/`, `companies/mining/PAN/sources/`, and production SQLite database `documents/analysis.sqlite` were verified unchanged.
- **No Paid API Calls:** No new paid OpenRouter or Fireworks API calls were executed during this evaluation turn.
- **No Production Code Alterations:** No modifications were made to production application code, prompt templates, or SQLite `sector_guardrails`.
- **Handoff for Codex Review:** This audit record and its supporting calculation outputs in `calculations/reconciliation_output.json` are preserved and ready for independent review by Codex.
