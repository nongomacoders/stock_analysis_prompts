# NTU 1H26 — Refined Chronological Section Trial: Gemini Independent Evidence Audit

**Evaluator:** Gemini (Google Antigravity IDE)  
**Evaluator Model & Settings:** Gemini 3.8 Flash (High)  
**Evaluation Timestamps:** UTC: `2026-10-28T17:48:29Z` | Local (Africa/Johannesburg): `2026-10-28T19:48:29+02:00`  
**Evaluated Run Path:** [`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T171901Z_ntu_refined_sections`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T171901Z_ntu_refined_sections)  
**Audit Save Location:** [`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T174829Z_gemini/audit.md`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T174829Z_gemini/audit.md)  
**Audit Decision:** **CORRECTIONS REQUIRED (SECTION-ONLY TRIAL; VALUATION NOT REQUESTED / NOT APPLICABLE)**

---

## 1. Operating Protocol & Scope Alignment

This independent evaluation is conducted strictly pursuant to:
1. `AGENTS.md` (Continuity & Evidence Rules: Gemini reviews DeepSeek, Codex reviews Gemini, no paid API calls or production guardrail writes during review).
2. `workflow/WORKFLOW.md` (Section reading prompt flow, empty initial ledger, validated delta propagation, Fireworks provider constraints).
3. `docs/STOCK_EVALUATION_FORMAT.md` Section 1A (Mandatory independent evaluation record, SHA-256 verification, claim verification register, reproducible reconciliations).
4. [`gemini/PROMPT.md`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T171901Z_ntu_refined_sections/gemini/PROMPT.md) operating instructions.

### Run Configuration & Scope
- **Subject:** Nutun Limited (JSE: NTU) — 1H26 Condensed Consolidated Interim Financial Statements for the six months ended 31 March 2026.
- **Trial Nature:** Chronological section-by-section analysis across all 38 physical pages partitioned into 24 captured units (22 analytical financial calls, 2 navigation/contacts captures).
- **Prompt Architecture:** Refined 4-part common section-reading prompt with concise conditional sector notes (`consumer_lending`), incorporating strict equation/unit consistency, conditional POCI accounting applicability without blanket disclosure bans, and cautious first-time comparative interpretation.
- **Provider & Model:** Fireworks API (`provider.only=["fireworks"]`), `deepseek/deepseek-v4.1-flash-1017`, `reasoning.effort=none`, 16,384 maximum completion tokens.
- **Seed State:** Completely empty initial ledger (`reports.questions_ledger` initialized to `[]`). No company-specific seed questions, historical lessons, or pre-loaded answers.
- **Stage 1 / Stage 2 / Valuation Status:** Not executed. This run is an isolated Tier 1 section-reading trial. Per instructions, no valuation target, rating bands, or investment recommendation were requested or produced.

---

## 2. Evidence Preservation & Source Verification

### Source Document Verification
- **Source PDF:** `nutunlimitedcondensedconsolidatedafs31march2026.pdf`
- **Location:** `companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf`
- **Verified SHA-256:** `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc` (Exact match against stored manifest in `plan.json` and production database).
- **Physical Page Count:** 38 physical pages. All 38 pages are retained across the 24 capture units with zero dropped pages.

### Preserved Input Manifest
All 116 files from the evaluated run—including run plans, summary metrics, raw model outputs, extracted prose, validation records, ledger transition states, and rendered source pages—have been immutably preserved in [`inputs/`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T174829Z_gemini/inputs/) with complete SHA-256 checksums documented in [`inputs/manifest.json`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T174829Z_gemini/inputs/manifest.json).

### Physical Source Inspection Coverage
- **Direct Visual & Textual Inspection:** Physical pages **13, 22, 24, 25, and 31** were rendered, visually audited via high-resolution PNGs, and cross-examined against verbatim text extracts in `source_pages/`.
- **Structural Coverage:** Physical pages **1 through 38** were verified across the 24 capture units in `coverage.json`.
- **Excluded Tools:** No live OpenRouter or paid external API calls were made. No production database tables or `sector_guardrails` rows were modified.

---

## 3. Claim Verification Register

| Claim ID | Claim Statement & Origin | Classification | Primary Evidence | Independent Verification & Method | Verdict | Consequence & Linked Finding |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **C001** | All 22 Fireworks calls completed; 38 pages covered once across 24 units; empty initial ledger; 18 validated deltas, 4 rejected deltas; zero repairs. | Pipeline execution / Historical result | `calls.csv`, `plan.json`, `coverage.json`, `verification.json` | Verified 22 call receipts, token totals (151,251 prompt, 51,535 completion, 0 reasoning), $0.0702 cost, and 340.5s wall time. | **PASS** | Operational pipeline completed cleanly with zero provider fallback. ([`F001`](#f001---supported-within-run-operational-pipeline-success)) |
| **C002** | Literal-quote validation failures rejected 4 deltas (pp.9-11, 13, 18-19, 30-31), holding back 7 proposed new questions and 2 valid resolutions. | System validation check | `rejected_ledger_deltas.json`, `coverage.json`, `section_*.validation.json` | Audited rejection errors: minor whitespace/newline differences rejected entire deltas, blocking Q-e4497d9112cd4e9d and Q-b18d8ce6d4804a50. | **PASS** | Confirmed ledger update brittleness; 18.2% delta rejection rate. ([`F002`](#f002---confirmed-ledger-reliability-limit-literal-quote-brittleness)) |
| **C003** | Physical p.13 prose correctly computes both portfolio rolls (principal 3,845; other 644; total 4,489) and excludes ordinary Stage 1/2 SICR migration under POCI framework. | Derived calculation / Accounting interpretation | `source_pages/NTU_13.txt`, `outputs/section_09.prose.md` | Recomputed: 3,975 + 382 - 728 + 383 - 167 = 3,845; 702 + 28 - 116 + 30 = 644; total = 4,489. Verified POCI explanation. | **PASS** | Prompt refinement succeeded in prose, but ledger update was blocked by validation filter. ([`F003`](#f003---supported-with-limits-p13-portfolio-rolls--poci-prose-accuracy)) |
| **C004** | Physical p.22 other-loan (5) and net trade-receivable (390) cells were merged into 5390, yielding false sum 9,879 vs printed 4,884. | Model assumption / OCR extraction failure | `source_pages/NTU_22.txt`, `outputs/section_15.prose.md` | Recomputed primary table row: 5 + 390 + 3,845 + 644 = 4,884 exact. Model evaluated 5,390 + 3,845 + 644 = 9,879 (delta 4,995). | **FAIL** | Confirmed model/extraction failure; false asset inflation of R4,995m flagged against issuer. ([`F004`](#f004---confirmed-ocr--capture-failure-p22-merged-cells--false-9879-sum)) |
| **C005** | Physical p.24 model scrambled 4 column headers, assigned -241 to Debt review instead of Unsecured, and inverted economic direction of cumulative gain reduction; FY25 full year loss is 259. | Table interpretation / Arithmetic / Direction | `source_pages/NTU_24.txt`, `outputs/section_16.prose.md` | Verified headers: Unsecured, Debt review, Retail, Secured. Verified movements: -241 is Unsecured, +69 is Debt review. FY25 loss: 77 + 182 = 259. | **FAIL** | Confirmed model column attribution error and accounting sign inversion. ([`F005`](#f005---confirmed-attribution--sign-errors-p24-ecl-reconciliation)) |
| **C006** | Physical p.25 prose swapped 31 March 2025 and 30 September 2025 closing exchange rate comparatives. | Comparative period mapping | `source_pages/NTU_25.txt`, `outputs/section_17.prose.md` | Verified Note 6.2 columns: Col 5 is 31 Mar 2025 (USD 18.4 / GBP 23.9); Col 6 is 30 Sep 2025 (USD 17.3 / GBP 23.2). Model wrote reverse. | **FAIL** | Confirmed comparative date inversion by model. ([`F006`](#f006---confirmed-period-mapping-error-p25-closing-fx-comparatives)) |
| **C007** | Physical p.31 model added tax 29 as +29 in core EBITDA bridge alleging false 58 gap, and invented all-positive sum (1,424 vs 597) for footnote components. | Accounting bridge arithmetic / Footnote interpretation | `source_pages/NTU_31.txt`, `outputs/section_20.prose.md` | Verified printed subtotal foots exactly: -63 - 29 + 68 + 597 + 1 + 216 = 790. Reconstructed signed footnote gives 598 (1 residual vs 597). | **FAIL** | Confirmed false accounting defect allegations by model. ([`F007`](#f007---confirmed-false-reconciliation-flags-p31-tax-sign--footnote-math)) |
| **C008** | Persistent ledger contains 32 questions (15 partial, 15 open, 1 contradicted, 1 resolved) with scope overlaps and duplications. | Ledger state & semantic evolution | `final_ledger.json`, `section_*.prose.md` | Audited all 32 questions. Q-8612694a3a674266 correctly contradicted; Q-08aa5c3f257440ab resolved while duplicate Q-e4497d9112cd4e9d stayed partial. | **PASS** | Question evolution confirmed; deduplication mechanism required. ([`F008`](#f008---supported-question-evolution-with-semantic-duplication)) |
| **C009** | Combined portfolio net cash of R434m less portfolio income of R246m equals carrying decline of R188m, leaving an unexplained R6m residual vs statutory cash flow amortisation of R182m. | Cash flow & balance sheet reconciliation | NTU 1H26 AFS pp.8, 12, 13; `independent_calculations.json` | Executed cash bridge: (773 + 116) - (382 + 28) - 45 = 434; income: (383 - 167) + 30 = 246; carrying decline: 434 - 246 = 188. Statutory CF: 182; residual: 6. | **PASS** | Verified mathematical truth of R6m statutory cash flow residual. ([`F009`](#f009---confirmed-portfolio-cash-vs-carrying-decline-reconciliation)) |

---

## 4. Independent Mathematical Reconciliations

All independent calculations were executed and verified via [`calculations/reconciliations.py`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T174829Z_gemini/calculations/reconciliations.py). Outputs are stored in [`calculations/reconciliation_output.json`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T174829Z_gemini/calculations/reconciliation_output.json).

### 4.1 Physical Page 13: Purchased Book Debts Roll-Forwards (H1 2026)
- **Principal Book Portfolio (Note 1.1, Amortised Cost POCI):**
  $$\text{Closing Balance} = \text{Opening} (3,975) + \text{Additions} (382) - \text{Net Collections} (728) + \text{CAEIR Accretion} (383) - \text{Impairment Loss} (167) = \mathbf{3,845\text{ Rm}}$$
  $$\text{Net Collections} = \text{Gross Collections} (773) - \text{Collection Costs} (45) = \mathbf{728\text{ Rm}}$$
- **Other Financial Assets (Note 1.2, Non-Title / Non-SPPI at FVTPL):**
  $$\text{Closing Balance} = \text{Opening} (702) + \text{Additions} (28) - \text{Cash Collections} (116) + \text{Fair Value Gain} (30) = \mathbf{644\text{ Rm}}$$
- **Total Purchased Book Debts:**
  $$\text{Total PBD} = 3,845 + 644 = \mathbf{4,489\text{ Rm}}$$
  $$\text{Maturity Split} = \text{Non-Current (>12m)} (2,688 + 490 = 3,178) + \text{Current (<12m)} (1,157 + 154 = 1,311) = \mathbf{4,489\text{ Rm}}$$
- **Conclusion:** Reconciles 100% to primary source text. Both roll-forwards foot without discrepancy.

### 4.2 Physical Page 22: Financial Assets Subject to Risk Table
- **Primary Source Values (Row: Carrying value of financial assets at 31 March 2026):**
  $$\text{Other Loans Receivable} = 5\text{ Rm}$$
  $$\text{Trade and Other Receivables (Net of 5 Rm impairment)} = 390\text{ Rm}$$
  $$\text{Principal Book Portfolio (Net of 431 Rm cumulative gain)} = 3,845\text{ Rm}$$
  $$\text{Other Financial Assets} = 644\text{ Rm}$$
  $$\text{Total Carrying Value} = 5 + 390 + 3,845 + 644 = \mathbf{4,884\text{ Rm}}$$
- **Model Error Decomposition:**
  The capture/OCR collapsed the text of column 1 ("5") and column 2 ("390") into a single token "5 390", which the model read as 5,390 Rm.
  $$\text{Model Calculation} = 5,390 + 3,845 + 644 = \mathbf{9,879\text{ Rm}}$$
  $$\text{False Discrepancy Flagged} = 9,879 - 4,884 = \mathbf{4,995\text{ Rm}}$$
- **Conclusion:** The primary source table foots perfectly. The alleged 4,995 Rm non-footing is purely an OCR/column-collapse defect introduced by upstream capture.

### 4.3 Physical Page 24: ECL Allowance on Principal Book Portfolios
- **Audited Balance at 30 September 2025:**
  $$\text{Unsecured} (468) + \text{Debt Review} (72) + \text{Retail} (47) + \text{Secured} (11) = \mathbf{598\text{ Rm}}$$
- **H1 2026 Movements:**
  $$\text{Unsecured: Acquired } 1 + \text{Historical } (242) = \mathbf{-241\text{ Rm}}$$
  $$\text{Debt Review: Acquired } 23 + \text{Historical } 46 = \mathbf{+69\text{ Rm}}$$
  $$\text{Retail: Acquired } 0 + \text{Historical } 4 = \mathbf{+4\text{ Rm}}$$
  $$\text{Secured: Acquired } 0 + \text{Historical } 1 = \mathbf{+1\text{ Rm}}$$
  $$\text{Total Movement} = -241 + 69 + 4 + 1 = \mathbf{-167\text{ Rm}}$$
- **Unaudited Balance at 31 March 2026:**
  $$\text{Unsecured} (468 - 241 = 227) + \text{Debt Review} (72 + 69 = 141) + \text{Retail} (47 + 4 = 51) + \text{Secured} (11 + 1 = 12) = \mathbf{431\text{ Rm}}$$
- **Historical Full-Year FY2025 Book Loss Audit:**
  $$\text{1H25 Historical Loss} = 77\text{ Rm}$$
  $$\text{2H25 Historical Loss} = 182\text{ Rm}$$
  $$\text{Full Year FY25 Historical Loss} = 77 + 182 = \mathbf{259\text{ Rm}}$$
- **Accounting Direction Check:**
  The cumulative allowance is an impairment *gain* (contra-asset). Net carrying value equals gross carrying value plus cumulative gain ($3,414 + 431 = 3,845$). When the cumulative gain falls from 598 to 431 (-167), net carrying value *declines*, contrary to the model's assertion that a reduction in gain increases carrying value.

### 4.4 Physical Page 25: Trade Receivables ECL & Currency Risk Mapping
- **Trade Receivables Loss Rate:**
  $$\text{Gross Carrying Amount} = 339\text{ (Current)} + 25\text{ (30d)} + 5\text{ (61-90d)} + 5\text{ (>90d)} = \mathbf{374\text{ Rm}}$$
  $$\text{Loss Allowance} = 0 + 0 + 0 + 5\text{ (>90d)} = \mathbf{5\text{ Rm}}$$
  $$\text{Net Carrying Amount} = 374 - 5 = \mathbf{369\text{ Rm}}$$
  $$\text{Overall Loss Rate} = \frac{5}{374} = \mathbf{1.3369\%} \approx \mathbf{1.34\%}$$
  $$\text{>90 Days Overdue Loss Rate} = \frac{5}{5} = \mathbf{100.00\%}$$
- **Closing Exchange Rate Comparative Mapping (Note 6.2):**
  - Primary Column 4: 31 March 2026 $\rightarrow$ USD 17.2 | GBP 22.7
  - Primary Column 5: 31 March 2025 $\rightarrow$ USD 18.4 | GBP 23.9
  - Primary Column 6: 30 September 2025 $\rightarrow$ USD 17.3 | GBP 23.2
  - Model transposition: Model reported USD 18.4 / GBP 23.9 for 30 Sep 2025 and USD 17.3 / GBP 23.2 for 31 Mar 2025, exactly reversing the interim and year-end comparatives.

### 4.5 Physical Page 31: Core EBITDA Reconciliation & Footnote Decomposition
- **Group Core EBITDA Subtotal Check (H1 2026):**
  $$\text{Continuing Loss} = -63\text{ Rm}$$
  $$\text{Tax Expense Credit Reversal} = -29\text{ Rm (printed in parentheses as } (29)\text{)}$$
  $$\text{Depreciation and Amortisation} = +68\text{ Rm}$$
  $$\text{PBD Amortisation} = +597\text{ Rm}$$
  $$\text{Equity Accounted Loss} = +1\text{ Rm}$$
  $$\text{Net Finance Charge} = +216\text{ Rm}$$
  $$\text{Group Core EBITDA} = -63 - 29 + 68 + 597 + 1 + 216 = \mathbf{790\text{ Rm}}$$
  *Segment sums: Nutun SA (710) + Nutun International (80) = 790 Rm exact.*
- **Model Sign Inversion Error:**
  The model added tax as $+29$ instead of subtracting $(29)$:
  $$\text{Model Sum} = -63 + 29 + 68 + 597 + 1 + 216 = \mathbf{848\text{ Rm}}$$
  $$\text{False EBITDA Discrepancy} = 848 - 790 = \mathbf{58\text{ Rm}}$$
- **Footnote 1 Signed Amortisation Reconstruction:**
  Footnote text: *"Amortisation of purchased book debts is calculated as CAEIR imputed interest revenue of R383 million, impairment loss of R167 million and net cash collections of R728 million per note 1.1 and fair value movements of R30 million and cash collections of R116 million per note 1.2."*
  $$\text{Note 1.1 Net Cash Generated} = \text{Net Collections } (728) - \text{Accounting Income } (383 - 167 = 216) = 512\text{ Rm}$$
  $$\text{Note 1.2 Net Cash Generated} = \text{Collections } (116) - \text{Fair Value Gain } (30) = 86\text{ Rm}$$
  $$\text{Signed Amortisation} = 512 + 86 = \mathbf{598\text{ Rm}}$$
  $$\text{Residual vs Stated Amortisation} = 598 - 597 = \mathbf{1\text{ Rm}}$$
  *The model mechanically summed all numbers as positive ($383 + 167 + 728 + 30 + 116 = 1,424$) and claimed an 827 Rm discrepancy.*

### 4.6 Statutory Cash Flow vs Carrying Decline Bridge & R6m Residual
- **Portfolio Net Cash Generated:**
  $$\text{Gross Collections } (773 + 116 = 889) - \text{Additions } (382 + 28 = 410) - \text{Direct Costs } (45) = \mathbf{434\text{ Rm}}$$
- **Portfolio Accounting Income Recognized:**
  $$\text{CAEIR Accretion } (383) - \text{Impairment Loss } (167) + \text{FV Gain } (30) = \mathbf{246\text{ Rm}}$$
- **Carrying Value Decline (Balance Sheet):**
  $$\text{Net Cash Generated } (434) - \text{Accounting Income } (246) = \mathbf{188\text{ Rm}}$$
  $$\text{Opening Total PBD } (4,677) - \text{Closing Total PBD } (4,489) = \mathbf{188\text{ Rm (Exact)}}$$
- **Statutory Cash Flow Amortisation Line:**
  $$\text{Statutory Cash Flow Subtotal} = \mathbf{182\text{ Rm}}$$
  $$\text{Residual Unexplained Difference} = 188 - 182 = \mathbf{6\text{ Rm}}$$
- **Conclusion:** As established by Codex, this 6 Rm difference is an unexplained statutory reporting residual. It must not be masked by rounding plugs or assumed FX translations.

---

## 5. Forensic Ledger Audit & Question Evolution

### 5.1 Final Ledger Status Distribution
The persistent ledger ended with **32 active questions**:
- **Partial:** 15
- **Open:** 15
- **Contradicted:** 1 (`Q-8612694a3a674266`)
- **Resolved:** 1 (`Q-08aa5c3f257440ab`)

### 5.2 Forensic Review of the 4 Rejected Deltas
The strict verbatim quote validation rejected 4 complete section updates:
1. **Section 07 (pp.9-11):** Quote for `Q-e4497d9112cd4e9d` failed literal match due to trailing space/pipe layout (`'Imputed interest revenue, calculated using the credit-adjusted effective interest rate | 383 |  |  |'`).
   - *Impact:* Held back 6 partial updates and 3 new proposed questions (operating loss -69 residual bridge, PBD measurement basis & roll-forward, headline earnings bridge).
2. **Section 09 (p.13):** Quote for `Q-86ab4a63039b4d7e` failed literal match due to a newline split in the source text (`'Accordingly, these purchased book debts are measured on a fair value basis. Refer to note 6.3.'`).
   - *Impact:* **Blocked the valid resolution of `Q-e4497d9112cd4e9d`** (which had full roll-forward and POCI basis verified in prose), held back 2 partial updates, and blocked 3 new proposed questions (gross vs net impairment direction, other financial assets FV drop, pledged covenant headroom).
3. **Section 13 (pp.18-19):** Quote for `Q-b18d8ce6d4804a50` failed literal match (`'Loss for the purposes of basic and diluted loss per share | Rm (63) |  |  | (64) | (238)'`).
   - *Impact:* **Blocked the valid resolution of `Q-b18d8ce6d4804a50`** (basic-to-headline bridge with nil headline adjustments in H1 26) and 1 partial update.
4. **Section 20 (pp.30-31):** Quote for `Q-e4497d9112cd4e9d` failed literal match (`'In terms of IFRS reporting, collections are taken into account in the movement of the amortised cost'`).
   - *Impact:* Held back 6 partial updates and 1 new proposed question (reconciliation of p.31 EBITDA bridge and footnote components).

**Key Takeaway:** The entire delta rejection mechanism operates as an all-or-nothing gate. A single formatting imperfection in one quote blocks all valid question answers and newly proposed questions in that capture. This created an artificial bottleneck where 7 valid analyst questions were unapplied, and questions that were thoroughly answered in the analyst's prose (`Q-e4497d9112cd4e9d`, `Q-b18d8ce6d4804a50`) were forced to remain `partial` or `open`.

### 5.3 Semantic Duplication & Scope Overlap
Despite starting from an empty ledger, question duplication emerged as the trial progressed:
- **PBD Measurement & Roll-Forward:** 
  - `Q-e4497d9112cd4e9d` (proposed in section 06) asked for PBD measurement basis and full roll-forward.
  - `Q-08aa5c3f257440ab` (proposed in section 14) asked for the exact same PBD measurement basis and POCI classification. In section 15, the model resolved `Q-08aa5c3f257440ab` while leaving `Q-e4497d9112cd4e9d` open/partial.
  - `Q-d22e0c2b395a427e` (proposed in section 15) and `Q-f6689319fb3a49ff` (proposed in section 19) duplicated the same roll-forward and FVTPL-vs-amortised cost reconciliation requests.
- **Exceptional Items Subtotal:**
  - `Q-4de5fe06ec4d4f67` (proposed in section 21) questioned whether exceptional items (51) is a subtotal of transaction costs, tax, and associate impairment.
  - `Q-86df863491ca4eae` (proposed in section 22) asked the exact same question for the FY2025 table.

### 5.4 Legitimate Contradiction
In Section 10 (pp.14-15), the model successfully identified that stored question `Q-8612694a3a674266` contained an invalid premise ("What drove bank overdrafts from R364m to R2,273m...?"). Note 2 proved that bank overdrafts at 31 March 2026 were R273m (falling R91m from R364m at 30 Sep 2025). The model correctly marked the question `contradicted` and cited verbatim evidence.

---

## 6. Comparison with Prior Trials

| Metric / Dimension | Old 24-Unit Reviewed Trial (`20261028T141038Z`) | Paired 4-Capture Pilot (`20261028T163642Z`) | Current Refined 24-Unit Trial (`20261028T171901Z`) |
| :--- | :---: | :---: | :---: |
| **Model & Provider** | DeepSeek Flash / Relace | DeepSeek Flash / Fireworks | DeepSeek Flash / Fireworks |
| **Reasoning Setting** | Default Thinking (High) | None (`reasoning.effort=none`) | None (`reasoning.effort=none`) |
| **Prompt Architecture** | 8 Bespoke Sector Reading Templates | Simplified Common 4-Part + Concise Notes | Refined Common 4-Part + 3 Authorized Tweaks |
| **Seed State** | Pre-loaded pilot seed questions | Empty initial ledger | Completely empty initial ledger |
| **Completion Rate** | 22/22 sections; Stage 2 failed (131k cap) | 4/4 captures completed | 22/22 sections completed; 0 fallbacks/repairs |
| **Ledger Acceptance Rate** | 22/22 valid (older validation logic) | 4/4 valid (100%) | 18/22 valid (81.8% accepted, 4 rejected) |
| **Total Section Cost (USD)** | $0.2445 (Sections + Stage 1) | $0.0128 (Revised pair) | **$0.0702 (Full 22 sections)** |
| **Average Cost / Call** | ~$0.0106 / call | ~$0.0032 / call | **$0.0032 / call (-69.8% vs older run)** |
| **Reasoning Tokens** | 284,949 tokens | 0 tokens | **0 tokens** |
| **Wall-Clock Time** | 19m 12s | 39.3s (summed calls) | **5m 40.5s (340.5s total wall time)** |
| **p.13 Equation Sign** | Not audited in isolation | Failed (`702+28-116-30=644`, delta -60) | **PASSED in prose (both portfolio rolls exact)** |
| **POCI Guidance Compliance** | Demanded ordinary SICR staging | Demanded ordinary SICR staging | **PASSED in prose (correctly excluded SICR)** |
| **Secondary Topic Coverage** | Dropped currency risk start on p.25 | Preserved currency risk start | **PASSED (Note 6.2 identified & linked to p.26)** |

---

## 7. Findings Register

### F001 — SUPPORTED WITHIN RUN: Operational Pipeline Success
- **Earliest Stage:** `section_analysis`
- **Classification:** SUPPORTED WITHIN RUN
- **Severity:** Low
- **Detail:** All 22 Fireworks API calls completed without error, timeout, or provider fallback. 24 capture units covered all 38 physical pages once. Total execution cost was $0.0702 ($0.0032/call), completing in 340.5s wall time.
- **Affected Downstream Outputs:** `calls.csv`, `metrics.json`, `coverage.json`.

### F002 — CONFIRMED LEDGER RELIABILITY LIMIT: Literal-Quote Brittleness
- **Earliest Stage:** `ledger_validation`
- **Classification:** CONFIRMED LEDGER RELIABILITY LIMIT
- **Severity:** High
- **Detail:** Strict character-by-character quote matching failed on 4 captures due to line breaks and pipe formatting in the PDF extraction. Entire deltas were rejected, preventing 7 new analytical questions from entering the persistent ledger and leaving 2 validly answered questions (`Q-e4497d9112cd4e9d`, `Q-b18d8ce6d4804a50`) open/partial.
- **Affected Downstream Outputs:** `final_ledger.json`, `rejected_ledger_deltas.json`.

### F003 — SUPPORTED WITH LIMITS: P13 Portfolio Rolls & POCI Prose Accuracy
- **Earliest Stage:** `section_analysis`
- **Classification:** SUPPORTED WITH LIMITS
- **Severity:** Medium
- **Detail:** In section 09 (p.13), the model correctly executed both portfolio roll-forward equations in prose (3,975 + 382 - 728 + 383 - 167 = 3,845; 702 + 28 - 116 + 30 = 644; total 4,489) and adhered to the POCI sector guidance by explicitly excluding ordinary Stage 1/2 SICR migration. However, this progress was not reflected in the persistent ledger due to the quote-match rejection in F002.
- **Affected Downstream Outputs:** `outputs/final_ledger.json`, `Q-e4497d9112cd4e9d`.

### F004 — CONFIRMED OCR / CAPTURE FAILURE: P22 Merged Cells & False 9,879 Sum
- **Earliest Stage:** `section_capture_and_section_analysis`
- **Classification:** CONFIRMED CAPTURE / OCR INTERPRETATION FAILURE
- **Severity:** High
- **Detail:** On p.22, table extraction collapsed column 1 ("5") and column 2 ("390") into "5 390". The model interpreted this as 5,390 Rm, summed 5,390 + 3,845 + 644 = 9,879 Rm, and alleged a 4,995 Rm discrepancy against the printed total of 4,884 Rm. The primary source table foots perfectly ($5 + 390 + 3,845 + 644 = 4,884$). This is a capture defect, not an issuer accounting error.
- **Affected Downstream Outputs:** `section_15.prose.md`, `Q-29ba2f276efb4af2`.

### F005 — CONFIRMED ATTRIBUTION & SIGN ERRORS: P24 ECL Reconciliation
- **Earliest Stage:** `section_analysis`
- **Classification:** CONFIRMED ATTRIBUTION / SIGN ERRORS
- **Severity:** High
- **Detail:** On p.24, the model misattributed table headers, conflating Unsecured and Retail into "Unsecured Retail" and leaving column 3 unlabelled. It attributed the -241 Rm loss to Debt review rather than Unsecured (+69 Rm). It also asserted that reducing the cumulative impairment gain increases net carrying value, which inverts accounting logic. Full year 2025 historical book loss is independently verified at 77 + 182 = 259 Rm.
- **Affected Downstream Outputs:** `section_16.prose.md`, `Q-2a8672f28c4140e8`, `Q-51278219e10b4cd4`.

### F006 — CONFIRMED PERIOD MAPPING ERROR: P25 Closing FX Comparatives
- **Earliest Stage:** `section_analysis`
- **Classification:** CONFIRMED PERIOD MAPPING ERROR
- **Severity:** Medium
- **Detail:** On p.25, the model transposed the comparative closing exchange rate columns, assigning USD 18.4 / GBP 23.9 to 30 September 2025 and USD 17.3 / GBP 23.2 to 31 March 2025. Primary evidence demonstrates that 31 March 2025 is 18.4 / 23.9 and 30 September 2025 is 17.3 / 23.2.
- **Affected Downstream Outputs:** `section_17.prose.md`, `Q-dab8ef060f454ad6`.

### F007 — CONFIRMED FALSE RECONCILIATION FLAGS: P31 Tax Sign & Footnote Math
- **Earliest Stage:** `section_analysis`
- **Classification:** CONFIRMED FALSE RECONCILIATION FLAGS
- **Severity:** High
- **Detail:** On p.31, the model treated tax expense (29) as +29 in the core EBITDA bridge, calculating -63 + 29 + 68 + 597 + 1 + 216 = 848 and alleging a false 58 Rm EBITDA discrepancy against the printed 790 Rm (which foots exactly: -63 - 29 + 68 + 597 + 1 + 216 = 790). It also summed descriptive footnote components as all-positive (1,424 vs 597 Rm), alleging an 827 Rm error; signed reconstruction yields 598 Rm (1 Rm residual).
- **Affected Downstream Outputs:** `section_20.prose.md`, `rejected_ledger_deltas.json`, `Q-e0ca727b62be46df`.

### F008 — SUPPORTED QUESTION EVOLUTION WITH SEMANTIC DUPLICATION
- **Earliest Stage:** `section_analysis_and_ledger`
- **Classification:** SUPPORTED QUESTION EVOLUTION & DUPLICATION
- **Severity:** Medium
- **Detail:** The evolving ledger successfully contradicted an erroneous historical premise (`Q-8612694a3a674266`), but allowed semantic duplications across PBD measurement/roll-forward (`Q-e4497d9112cd4e9d`, `Q-08aa5c3f257440ab`, `Q-d22e0c2b395a427e`) and exceptional item layouts (`Q-4de5fe06ec4d4f67`, `Q-86df863491ca4eae`), inflating the ledger to 32 questions.
- **Affected Downstream Outputs:** `final_ledger.json`.

### F009 — CONFIRMED PORTFOLIO CASH VS CARRYING DECLINE RECONCILIATION
- **Earliest Stage:** `section_analysis_and_financial_statements`
- **Classification:** CONFIRMED PORTFOLIO CASH VS CARRYING VALUE RESIDUAL
- **Severity:** Low
- **Detail:** Independent reconciliation establishes net portfolio cash of 434 Rm less portfolio income of 246 Rm equals carrying decline of 188 Rm (tying to 4,677 - 4,489 = 188). This leaves an unexplained 6 Rm residual against the statutory cash flow amortisation subtotal of 182 Rm.
- **Affected Downstream Outputs:** `independent_calculations.json`.

---

## 8. Testable Improvements & Recommendations for Codex

1. **Quote Validation Resilience (High Priority):**
   - *Problem:* 4 out of 22 section deltas were rejected entirely due to minor whitespace or multiline PDF line-wrap mismatches in literal evidence quotes.
   - *Recommendation:* Normalize whitespace (collapse multiple spaces, tabs, and newlines to a single space) and strip markdown table pipes before performing verbatim quote substring verification.
2. **Partial Delta Acceptance / Decoupling (High Priority):**
   - *Problem:* A single failed quote on one question rejects the entire delta, throwing away valid question answers and newly proposed questions.
   - *Recommendation:* Process question updates and new questions independently so that valid answers and additions persist even if an unrelated quote fails verification.
3. **Table Extraction Delimiters (High Priority):**
   - *Problem:* Merged numeric cells on p.22 (`5` and `390` $\rightarrow$ `5 390`) caused a false R4,995m asset inflation allegation.
   - *Recommendation:* Enforce strict column delimiter preservation (`|`) in `section_capture` to prevent adjacent numerical cells from merging into pseudo-integers.
4. **Accounting Sign & Footnote Operators (High Priority):**
   - *Problem:* DeepSeek inverted tax credit signs in EBITDA bridges (+29 vs -29) and invented all-positive additions for footnote component lists.
   - *Recommendation:* Enhance prompt guidance to explicitly instruct that parenthesized figures `(x)` represent negative numbers or reductions in accounting reconciliations, and that narrative footnote component lists should not be mechanically summed without verifying their algebraic relationship.
5. **Ledger Question Deduplication Filter (Medium Priority):**
   - *Problem:* Proliferation of duplicate questions asking for PBD roll-forwards and measurement bases under multiple distinct question IDs.
   - *Recommendation:* Implement a semantic similarity check against existing open/partial question text before appending a newly proposed question to the ledger.

---

## 9. Final Decision & Handoff

- **Audit Determination:** **CORRECTIONS REQUIRED (SECTION-ONLY TRIAL; VALUATION NOT REQUESTED / NOT APPLICABLE)**.
- **Operational Assessment:** The refined section-reading prompt executed with outstanding operational efficiency ($0.0702 total cost, zero reasoning tokens, 340.5s wall time across all 38 pages) and demonstrated marked improvements in prose accuracy (p.13 portfolio rolls and POCI framing).
- **Core Deficiencies Identified:** 
  1. Ledger validation brittleness (18.2% delta rejection rate).
  2. OCR cell-merging on p.22 creating false R4,995m asset flags.
  3. Header misattribution and sign inversion on p.24.
  4. Comparative period swapping on p.25.
  5. Accounting sign inversion on tax (-29 treated as +29) and invented footnote summation formulas on p.31.
- **Codex Handoff:** All 116 review inputs, calculation scripts, execution logs, and rendered source pages are preserved and ready for independent Codex review. No production guardrails or database records were modified during this turn.
