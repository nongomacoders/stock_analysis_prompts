# WORKPLAN: Primary Financial Statements (PAN Section S006, pp.17–18)

**Target Section**: Primary Financial Statements (Statement of Financial Position, Statement of Profit or Loss and Other Comprehensive Income, Statement of Cash Flows).  
**Source Document**: `companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf`  
**Document SHA-256**: `62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd` (verified).  
**Physical Pages**: **17, 18** (Printed page labels: 30, 31, 32, 33).  
**Reporting Currency & Units**: US$ thousand (`US$ '000`).  

---

### 1. Scope & Primary Statement Layout

Physical pages 17 and 18 are two landscape spreads, each housing two primary financial statements side-by-side:

1. **Physical Page 17**:
   - **Left Half (Printed p.30)**: *Summarised Consolidated Statement of Financial Position — Assets*
     - Non-current assets (PPE, Goodwill, Intangibles, Deferred tax, Long-term inventory, Investments, Rehabilitation fund, Restricted cash) $\rightarrow$ Total non-current assets ($1,279,570\text{k}$ FY26 / $899,052\text{k}$ FY25).
     - Current assets (Inventory, Other receivables, Current tax, Short-term investments, Cash) $\rightarrow$ Total current assets ($328,505\text{k}$ FY26 / $105,457\text{k}$ FY25).
     - **Total assets**: $1,608,075\text{k}$ FY26 / $1,004,509\text{k}$ FY25.
   - **Right Half (Printed p.31)**: *Summarised Consolidated Statement of Financial Position — Equity and Liabilities*
     - Equity (Share capital, Share premium, Shares to be issued, Retained earnings, Reserves, NCI) $\rightarrow$ Total equity ($1,035,997\text{k}$ FY26 / $546,668\text{k}$ FY25).
     - Non-current liabilities (Rehabilitation, Borrowings, Leases, Financial liabilities, Share-based payments, Deferred tax) $\rightarrow$ Total non-current liabilities ($349,328\text{k}$ FY26 / $281,970\text{k}$ FY25).
     - Current liabilities (Payables, Borrowings, Leases, Contract liability, Financial liabilities, Share-based payments, Tax) $\rightarrow$ Total current liabilities ($222,750\text{k}$ FY26 / $175,871\text{k}$ FY25).
     - **Total equity and liabilities**: $1,608,075\text{k}$ FY26 / $1,004,509\text{k}$ FY25.

2. **Physical Page 18**:
   - **Left Half (Printed p.32)**: *Summarised Consolidated Statement of Profit or Loss and Other Comprehensive Income*
     - Operating lines: Revenue ($1,156,451\text{k}$), Cost of production ($(514,297\text{k})$), Gross profit ($642,154\text{k}$), Other income/expenses, Impairments, Royalties $\rightarrow$ Profit before finance ($545,838\text{k}$).
     - Finance lines: Finance income ($5,848\text{k}$), Finance costs ($(17,318\text{k})$) $\rightarrow$ Profit before tax ($534,368\text{k}$).
     - Tax & Net profit: Income tax expense ($(177,457\text{k})$) $\rightarrow$ Profit for period ($356,911\text{k}$).
     - Other comprehensive income ($44,054\text{k}$) $\rightarrow$ Total comprehensive income ($400,965\text{k}$).
     - Attributable splits (Owners $357,215\text{k}$, NCI $(304\text{k})$) and EPS (17.60 US cents).
   - **Right Half (Printed p.33)**: *Summarised Consolidated Statement of Cash Flows*
     - Operating activities: Cash before dividend/tax ($712,119\text{k}$), Dividends paid ($(58,540\text{k})$), Tax paid ($(74,135\text{k})$), Royalties paid ($(12,112\text{k})$), Finance net $\rightarrow$ Net cash from operating ($556,991\text{k}$).
     - Investing activities: PPE capex ($(189,723\text{k})$), Exploration capex ($(26,030\text{k})$), Intangibles, M&A cash, Investments $\rightarrow$ Net cash used in investing ($(352,144\text{k})$).
     - Financing activities: Borrowings repayment ($(149,311\text{k})$), Leases, Buy-backs $\rightarrow$ Net cash used in financing ($(155,874\text{k})$).
     - Cash reconciliation: Opening cash ($49,532\text{k}$) + Net increase ($48,973\text{k}$) + FX ($9,807\text{k}$) = **Closing cash ($108,312\text{k}$)**.

---

### 2. Integration into Existing Schema

The existing schema in `build/report.sqlite` accommodates Section S006 directly:
- `cells`:
  - `table_region`: `statement_of_financial_position`, `statement_of_profit_or_loss`, `statement_of_cash_flows`.
  - `physical_page`: 17, 18.
  - `fiscal_year`: `FY26`, `FY25`.
  - `unit`: `US$ thousand` (and `US cents` for EPS).
  - `value_raw`: printed string preserving brackets and commas, e.g. `(514,297)`.
  - `value_num`: parsed signed real, e.g. `-514297.0`.
- `conflicts`: logs any arithmetic roll-down or cross-statement failures.
- `questions`: connects directly to open question `Q-a0b503d7ac044eee` (reconciliation of D009 production revenue/costs to primary statements).

---

### 3. Planned Reconciliation Checks

1. **Balance Sheet Invariant**: Total Assets == Total Equity and Liabilities ($1,608,075\text{k} == 1,608,075\text{k}$ for FY26; $1,004,509\text{k} == 1,004,509\text{k}$ for FY25).
2. **Asset Subtotals**: Non-current Assets + Current Assets == Total Assets ($1,279,570 + 328,505 = 1,608,075$).
3. **Liabilities & Equity Subtotals**: Total Equity + Non-current Liabilities + Current Liabilities == Total Equity and Liabilities ($1,035,997 + 349,328 + 222,750 = 1,608,075$).
4. **Profit & Loss Roll-Down**: Revenue - Cost of Production == Gross Profit ($1,156,451 - 514,297 = 642,154$).
5. **Operating Profit Roll-Down**: Gross Profit + Other Income - Other Expenses - Impairments - Royalties == Profit before Finance ($642,154 + 4,596 - 85,958 - 345 - 14,609 = 545,838$).
6. **Profit Before Tax Roll-Down**: Operating Profit + Finance Income - Finance Costs == Profit Before Tax ($545,838 + 5,848 - 17,318 = 534,368$).
7. **Cash Flow Roll-Forward**: Opening Cash + Net Increase + FX == Closing Cash ($49,532 + 48,973 + 9,807 = 108,312$).
8. **Operating + Investing + Financing Roll-Up**: Net Operating + Net Investing + Net Financing == Net Increase in Cash ($556,991 - 352,144 - 155,874 = 48,973$).
9. **Cross-Statement Cash Tie**: Balance Sheet Cash (p.17) == Cash Flow Statement Closing Cash (p.18) ($108,312\text{k} == 108,312\text{k}$).

---

### 4. P0 Acceptance Checklist

- [x] Scope bounded to Section S006 physical pp.17–18.
- [x] Source SHA-256 re-verified (`62b10bcd...`).
- [x] Primary statement layout analyzed (side-by-side spreads on landscape pages).
- [x] Core arithmetic invariants and cross-statement checks specified.
- [x] No extraction code written; no figures altered; covenants respected.
