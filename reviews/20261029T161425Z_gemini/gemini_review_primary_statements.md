# Gemini-Role Review: Primary Financial Statements Extension (PAN Section S006)

**Evaluation Run**: `reviews/20261029T161425Z_gemini/gemini_review_primary_statements.md`  
**Review Target**: Commits `469aaa0` through `191ac00` on branch `agentic-report-build`.  
**Review Subject**:  
- `workflow/changes/20261029_agentic_report_build/WORKPLAN_PRIMARY_STATEMENTS.md` (P0)
- `workflow/changes/20261029_agentic_report_build/build/extraction/extract_pan_primary_statements.py` (P1)
- `workflow/changes/20261029_agentic_report_build/tests_reconcile/test_primary_statements.py` (P2)
- `workflow/changes/20261029_agentic_report_build/READING_BRIEF_PRIMARY_STATEMENTS.md` (P4)
- `workflow/changes/20261029_agentic_report_build/build/report_view.xlsx` (4-tab Excel workbook)
- `workflow/changes/20261029_agentic_report_build/build/report.sqlite` (1,388 cells total)

---

### 1. Scope & Verification of Non-Negotiable Covenants

| Covenant | Standard | Finding | Verdict |
|---|---|---|---|
| **Covenant 1: Never replace a printed source figure** | Conflicts must be recorded as data; no silent "corrections" of printed figures in SQLite or prose. | Verified: All 192 extracted primary statement figures match printed text on physical pp.17-18 verbatim (`value_raw`). Negative figures in brackets e.g. `(514,297)` are stored verbatim and converted to negative floats in `value_num`. Comparative figures for reciprocal dividends are preserved as printed. Zero figures altered or rounded. | **SATISFIED (PASS)** |
| **Covenant 2: All arithmetic executes in code** | All totals, deltas, and cross-checks must be computed by code, never asserted from model memory. | Verified: Balance sheet equalities, income statement roll-downs, cash roll-forwards, and cross-statement cash ties are executed in `test_primary_statements.py`. Excel workbook contains static values only (verified 0 formulas across all 4 sheets). | **SATISFIED (PASS)** |
| **Covenant 3: Lineage on every cell** | Every cell carries page, source hash, and extraction commit. | Verified: All 192 cells carry physical page (17, 18), source document SHA-256 (`62b10bcd...`), and extraction commit (`p1_primary_statements_v1`). Renders for pages 17 & 18 are tracked with SHA-256 hashes in `pages` table. | **SATISFIED (PASS)** |
| **Covenant 4: Ledger independence** | Arithmetic proof does not fake-close accounting ambiguities. | `Q-a0b503d7ac044eee` (revenue & cost bridge) is enriched with verified mathematical deltas (ZAR 2,294.9m bridge) but remains properly **OPEN** for detailed Note 3 segmental review. | **SATISFIED (PASS)** |

---

### 2. Primary Accounting Invariants & Statement Ties

1. **Balance Sheet Fundamental Equation**:
   - FY26: Total Assets ($1,608,075\text{k}$) == Total Equity and Liabilities ($1,608,075\text{k}$). Exact tie ($0.0\text{ variance}$).
   - FY25: Total Assets ($1,004,509\text{k}$) == Total Equity and Liabilities ($1,004,509\text{k}$). Exact tie ($0.0\text{ variance}$).
   - Non-current assets ($1,279,570\text{k}$) + Current assets ($328,505\text{k}$) == Total Assets ($1,608,075\text{k}$).
   - Total equity ($1,035,997\text{k}$) + Non-current liabilities ($349,328\text{k}$) + Current liabilities ($222,750\text{k}$) == Total Equity & Liabilities ($1,608,075\text{k}$).

2. **Income Statement Roll-Down**:
   - Revenue ($1,156,451\text{k}$) + Cost of Production ($(514,297\text{k})$) == Gross Profit ($642,154\text{k}$).
   - Operating Profit ($545,838\text{k}$) + Finance Income ($5,848\text{k}$) + Finance Costs ($(17,318\text{k})$) == Profit Before Tax ($534,368\text{k}$).
   - Profit Before Tax ($534,368\text{k}$) + Income Tax ($(177,457\text{k})$) == Profit for the Period ($356,911\text{k}$).

3. **Cash Flow Statement Roll-Forward**:
   - Operating ($556,991\text{k}$) + Investing ($(352,144\text{k})$) + Financing ($(155,874\text{k})$) == Net Increase ($48,973\text{k}$).
   - Opening Cash ($49,532\text{k}$) + Net Increase ($48,973\text{k}$) + FX ($9,807\text{k}$) == Closing Cash ($108,312\text{k}$).

4. **Cross-Statement Cash Tie (Balance Sheet vs Cash Flow Statement)**:
   - Balance Sheet Cash and cash equivalents (p.17): **US$108,312k**.
   - Cash Flow Statement Closing Cash (p.18): **US$108,312k**.
   - Comparative FY25: **US$49,532k == US$49,532k**.

5. **Cross-Section Revenue Bridge (IFRS p.18 vs Segmental p.50)**:
   - IFRS Consolidated Revenue: **US$1,156,451k** ($1,156.451\text{m}$).
   - Converted at average exchange rate 16.90 US$/ZAR (p.50): **ZAR 19,544.02m**.
   - Segmental Mining Revenue (p.50): **ZAR 17,249.10m**.
   - Bridge delta: **ZAR 2,294.92m**, providing an exact numerical anchor for ledger question `Q-a0b503d7ac044eee`.

---

### 3. Reviewer Verdict

**ACCEPT WITHOUT AMENDMENT**.  
The extension from Section D009 (Group Production Summary) to Section S006 (Primary Financial Statements) cleanly upholds all agentic build covenants. Reconciliations are mathematically complete, cross-statement ties are exact, and zero model inference was used for arithmetic.
