# Gemini Independent Audit: Single-Pass vs. Three-Pass Workflow Evaluation

**Evaluator:** Gemini 3.8 Flash (Antigravity Environment)  
**Evaluation Timestamp:** UTC 2026-10-29T12:02:40Z | Local Time: Africa/Johannesburg (UTC+02:00) 2026-10-29 14:02:40  
**Scope & Mandate:** Formal independent audit following `docs/STOCK_EVALUATION_FORMAT.md` Section 1A. Evaluation of the completed small one-pass versus three-pass experiment across Nutun Limited (`NTU` 1H26) and Pan African Resources PLC (`PAN` FY26), incorporating the continuation run `20261029T114212Z_three_pass_pan_resume` and original experiment `20261029T112944Z_three_pass_experiment`.  
**Final Decision:** **CORRECTIONS REQUIRED; INSUFFICIENT EVIDENCE FOR THREE-PASS ADOPTION (DO NOT ADOPT).**

---

## 1. Executive Summary & Core Verdict

The hypothesis that splitting single section analysis into a three-pass sequential chain (**Pass 1: Accounting Meanings & Terms** → **Pass 2: Calculations & Percentage Movements** → **Pass 3: Synthesized Brief, Question Closure & Ledger Updates**) improves analytical robustness is **refuted within this experimental sample**.

1. **Robustness vs. Clarity:** Three passes improve layout structure, descriptive granularity, and produce well-verified percentage movements (NTU). However, **robustness is not improved**:
   - In NTU, the three-pass final stage inherited an early scope narrowing from Pass 1, repeatedly asserted that PBD was restricted to R3,845m (ignoring the R644m fair-value component explicitly recognized within PBD), and accepted an unsupported question closure (`Q-08aa5c3f257440ab`) into the in-memory ledger.
   - In PAN, Pass 1 generated unsound, generic accounting definitions (asserting capex reduces profit and treating revenue/EBITDA as cash inflows), while Pass 2 preserved double-counting ambiguity around the FY25 Group production sum (197,608 vs 196,527 oz).
   - Neither single-pass nor three-pass detected a blatant **10,000 oz primary source typographical error** on PAN p.49 (Barberton total printed as 94,929 oz vs components summing to 84,929 oz, causing total-operation columns to sum to 282,310 oz vs Group 272,310 oz).
2. **Validator Conflation:** The single-pass NTU run was rejected by the ledger validator solely due to string length (`3 414` < 8 characters), not factual hallucination. The three-pass run passed syntax validation, creating a false impression of superiority while admitting a semantically invalid closure.
3. **Economics & Latency:** The three-pass workflow costs **2.24x (NTU)** to **2.39x (PAN)** as much as single-pass, increases elapsed request time by **1.62x to 1.80x**, and triples API transport exposure (as evidenced by the HTTP 429 rate-limit failure in the initial PAN run).

**Recommendation:** Retain the single-pass architecture. Do not deploy the three-pass workflow. Robustness must be achieved via explicit guardrails and semantic closure constraints, not token-inflating chained calls.

---

## 2. Experimental Control, Coverage & Input Verification

All inputs, source PDFs, and outputs were verified with SHA-256 hashes against original manifests before analysis. No paid API calls, code edits, or SQLite production writes were executed during this evaluation.

### A. Primary Source Documents Inspected
- **NTU Source PDF:** `companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf`  
  - SHA-256: `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc` (Matches manifest)  
  - Physical pages examined: **p.21, p.22, p.23** (Capture scope); **p.13** (Note 1 roll-forward inspected for confirmation).
- **PAN Source PDF:** `companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf`  
  - SHA-256: `62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd` (Matches manifest)  
  - Physical pages examined: **p.48, p.49, p.50** (Group Production Summary).

### B. Execution Accounting & Comparative Metrics

| Dimension | NTU Single-Pass | NTU Three-Pass | PAN Single-Pass | PAN Three-Pass |
| :--- | :---: | :---: | :---: | :---: |
| **Model** | `deepseek-v4.1-flash` | `deepseek-v4.1-flash` | `deepseek-v4.1-flash` | `deepseek-v4.1-flash` |
| **Provider / Reasoning** | Fireworks / None | Fireworks / None | Fireworks / None | Fireworks / None |
| **Calls Dispatched** | 1 | 3 | 1 | 3 |
| **API Cost (USD)** | **$0.004702** | **$0.010517** (2.24x) | **$0.004671** | **$0.011184** (2.39x) |
| **Prompt Tokens** | 8,675 | 27,675 | 11,107 | 35,391 |
| **Completion Tokens** | 3,429 | 5,602 | 2,904 | 4,845 |
| **Request Latency (s)** | 18.457 s | 29.956 s (1.62x) | 16.914 s | 30.421 s (1.80x) |
| **Ledger Syntax Valid** | No (`3 414` < 8 chars) | **Yes** | **Yes** | **Yes** |
| **Semantic Closure Valid** | **No** (Premature) | **No** (Premature) | N/A (No active Qs) | N/A (No active Qs) |
| **Total Experiment Cost** | \multicolumn{4}{c|}{Known successful calls: **$0.031074 USD** (Failed HTTP 429 cost unknown)} |

---

## 3. Independent Reconciliations & Primary Evidence Findings

### A. Nutun Limited (NTU 1H26, pp. 21–23)
1. **Instrument & Measurement Basis:** Confirmed on p.21 that Purchased Book Debts (PBDs) are classified as **POCI (Stage 3) on initial recognition**, measured at amortised cost via a rolling 12-month net cash flow model discounted at a credit-adjusted effective interest rate (**CAEIR 19.2%** at 31 Mar 2026; 17.9% Mar 2025; 18.4% Sep 2025). Generic contractual-cash-flow ECL does not apply; favourable changes in lifetime ECL are recognized in P&L as impairment gains.
2. **The R4,489m Scope & Fair-Value Mischaracterization:**
   - On p.21, the disclosure explicitly states: *"Other financial assets, recognised within the purchase book debts, include a receivables balance measured at fair value."*
   - On p.22, carrying values are: Principal book portfolio **R3,845m** (Gross 3,414 + POCI gain 431) + Other financial assets **R644m** = **R4,489m**.
   - Note 1 (p.13) confirms total PBD is exactly **R4,489m** (3,178 non-current + 1,311 current).
   - **Evaluator Critique:** Both single-pass and three-pass models treated R3,845m as the entire PBD balance and stated that R4,489m was an unresolved discrepancy. The three-pass dictionary pass codified this narrowing, which persisted through movement and final passes.
3. **Question Closure Audit (`Q-08aa5c3f257440ab`):**
   - The question required: *"PBD measurement basis and applicable ECL model stated and reconciled to the carrying value, or confirmed not disclosed."*
   - Because R644m was not reconciled to the R4,489m carrying value referenced in the question ledger, the closure condition was **not met**. Proposing `status: resolved` was a semantic error in both arms. The three-pass arm accepted this invalid closure into its memory ledger.
4. **Sign Convention Verification:** On p.22, the POCI impairment gain of R431m is **added** to gross carrying value (R3,414m + R431m = R3,845m). A reduction from R598m (Sep 2025) to R431m is a **reduction in cumulative gains**, representing an **impairment loss of R167m** (-27.93%). Both models correctly identified the sign direction, confirming the effectiveness of the recent prompt clarification.

### B. Pan African Resources (PAN FY26, pp. 48–50)
1. **The 10,000 oz Primary Typographical Error on p.49:**
   - In the table *Gold produced – total* (p.49), Barberton Mines total is printed as **94,929 oz**.
   - However, Barberton mining operations produced **71,997 oz** and BTRP produced **12,932 oz** (71,997 + 12,932 = **84,929 oz**). The printed total is overstated by exactly **10,000 oz**.
   - Consequently, summing the printed total-operation columns (Barberton total 94,929 + Evander total 103,330 + MTR total 51,927 + Tennant total 32,124) yields **282,310 oz**, exceeding the printed Group Total (**272,310 oz**) by **10,000 oz**.
   - If the true component sum (84,929 oz) is used, the total operations sum equals **272,310 oz** exactly.
   - **Evaluator Critique:** Neither model detected this discrepancy. The single-pass model verified that Mining total (118,853) + Surface total (153,458) = 272,311 oz (1 oz rounding), but did not cross-check the total-operation columns. The three-pass model also missed it.
2. **Disjoint FY25 Production vs. Overlap Double-Count:**
   - On p.48, FY25 gold produced by disjoint category: Underground 92,643 oz + Surface 2,654 oz + Tailings 98,636 oz + Third-party buy-in 1,081 oz + Surface feedstock 1,513 oz = **196,527 oz** (matches printed Group total).
   - In the movement pass, the model took Evander total-column underground production (**93,724 oz**, which already includes 1,081 oz buy-in) and added buy-in again, producing **197,608 oz** and asserting an unresolved 1,081 oz double-count risk. The staging failed to resolve this straightforward table overlap.
3. **MTR Tailings vs. Total Operations Gap (5,763 oz):**
   - On p.48, FY25 MTR tailings produced shows **25,043 oz** in the leaf column, but **30,806 oz** in the Total operations MTR total column (diff: **5,763 oz**).
   - 5,763 oz is the exact third-party buy-in volume processed by MTR in FY26.
   - Both single-pass and three-pass models correctly flagged this mismatch and formulated high-priority questions to verify if FY25 MTR total included buy-in feedstock not broken out in the leaf row.
4. **Outlier Verification (Tennant & Elikhulu Costs):**
   - **Tennant FY25 All-In Cost (1,584,835 A$/kg / 32,041 US$/oz):** Cross-checked against p.50. Total all-in cost of production was A$58.1m on sales of 1,179 oz (36.67 kg) → A$58.1m / 0.03667 kg = **1,584,358 A$/kg**, confirming the printed figure (1,584,835) is arithmetically consistent with the tiny ramp-up sales base, not a typo.
   - **Elikhulu FY25 All-In Cost (68,843 ZAR/kg):** On p.50, Elikhulu all-in cost was ZAR 1,130.9m on sales of 53,092 oz (1,651.35 kg). Expected cost: 1,130.9m / 1,651.35 kg = **684,835 ZAR/kg**. The printed figure of **68,843** is an unmistakable issuer typo (omitted digit '4'). Both models correctly flagged this outlier.
5. **Cost Definitions & Propagation of Generic Errors:**
   - In `pan_dense_meaning.md`, the model asserted: *"Costs and capex are outflows (reduce profit/assets); revenue and EBITDA inflows."*
   - This conflates cash flow accounting with accrual accounting and capital expenditure capitalization under IAS 16.

---

## 4. Evaluator Findings Register Summary

Detailed finding records are preserved in `findings.json`.

| ID | Origin | Classification | Severity | Summary |
| :--- | :--- | :--- | :---: | :--- |
| **F001** | NTU Movement Pass | Confirmed Benefit | Low | Generated accurate signed % movements with correct denominators. |
| **F002** | NTU Final Outputs | Confirmed Error | High | Premature closure of `Q-08aa5c3f257440ab` without total carrying value reconciliation; accepted by three-pass in memory. |
| **F003** | NTU Meaning Pass | Confirmed Error | Medium | Excluded R644m fair-value assets from PBD scope; error propagated across passes. |
| **F004** | NTU Single Pass | Engineering Artifact | Medium | Validator rejected single pass on string length (`3 414` < 8 chars), conflating syntax with semantic quality. |
| **F005** | PAN Meaning Pass | Confirmed Error | Medium | Generated unsound accounting definitions (capex reduces profit; revenue/EBITDA are cash inflows). |
| **F006** | PAN Movement Pass | Confirmed Error | Low | Perpetuated 1,081 oz overlap confusion and ignored 1 oz source rounding residual. |
| **F007** | PAN Transport | Operational Risk | Low | Chained pipeline failed on HTTP 429; exposes multi-call fragility. |
| **F008** | Primary PAN Source | Source Defect | High | PAN p.49 contains 10,000 oz internal typo (Barberton total 94,929 vs 84,929); missed by both arms. |
| **F009** | Both PAN Arms | Verified Quality | Low | Correctly detected 5,763 oz MTR discrepancy and framed targeted questions. |
| **F010** | Overall Experiment | Evaluator Conclusion | High | Three-pass increases cost (2.3x) and latency without improving robustness; refutes adoption. |

---

## 5. Decision & Proposed Guardrails

### A. Decision Gate: Do Not Adopt Three-Pass Workflow
The three-pass experiment demonstrates that sequential prompt chaining does not cure underlying model limitations (such as premature question closure or overlooking cross-table reconciliation gaps). Instead, it introduces **error propagation**, where early mischaracterizations (e.g., restricting PBD scope or synthesizing flawed accounting definitions) are treated as authoritative context by downstream passes. Combined with a 2.3x cost multiplier and operational rate-limit exposure, **the three-pass workflow should not be adopted**.

### B. Proposed Testable Guardrails (For Future Codification Review)

1. **Rule: `GUARD_SEMANTIC_CLOSURE_TOTAL_RECONCILIATION`**
   - **Sector:** All Sectors (`COMMON`)
   - **Trigger:** Model proposes `status: resolved` for an open question that specifies a carrying value or total balance sheet figure.
   - **Mandate:** The update must provide an explicit numerical bridge matching the target figure (e.g. R4,489m) or confirm that components (e.g. R3,845m + R644m) explain the entire balance. If any component is unverified or segregated, status must remain `partial`.
   - **Implementation Point:** `section_capture/ledger_validator.py` / Evaluation prompt.

2. **Rule: `GUARD_DISJOINT_ROW_COLUMN_CROSSCHECK`**
   - **Sector:** `MINING` / Multi-segment operations
   - **Trigger:** Mining production tables containing both operation totals (columns) and category totals (rows).
   - **Mandate:** Before reporting a discrepancy between category sums and group totals, verify whether intermediate sub-totals (e.g., total-operation columns) match the sum of their individual mining and surface components. Flag column-level arithmetic errors as primary disclosure anomalies.
   - **Implementation Point:** `12-analyst-reading-brief/v1.1.0` Mining prompt instructions.

---

## 6. Audit Preservation & Handoff

All execution records, calculation scripts, input verification manifests, rendered source pages, and claims registers have been compiled and preserved in:
`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261029T114800Z_antigravity_gemini_stage_review/`

- `audit.md` (This document)
- `claims.json` (Structured claim verification register C001–C010)
- `findings.json` (Structured findings register F001–F010)
- `calculations.json` (Executable calculation outputs)
- `input_manifest.json` (Complete SHA-256 file manifest)
- `input_checks.json` (Byte-identity and prompt containment verification)
- `source_pages/` (Rendered PNG and extracted TXT pages for NTU 13, 21–23 and PAN 48–50)

This audit is ready for Codex retrospective review against primary evidence.
