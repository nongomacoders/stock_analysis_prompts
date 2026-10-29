# Reading Brief: Pan African Resources (PAN) Primary Financial Statements (Section S006)

**Target Section**: Section S006 (Summarised Consolidated Financial Statements, physical pages 17 & 18, printed pages 30–33).  
**Source Document**: `companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` (`62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`).  
**Reporting Currency & Units**: US$ thousand (`US$ '000`) and US cents for EPS.  
**Artifact Lineage**: Generated strictly from `build/report.sqlite` (extraction commit `p1_primary_statements_v1`, reconciliation commit `826373c`). All calculations verified in `tests_reconcile/test_primary_statements.py`.

---

### 1. Key Facts and Figures

- **Statement of Financial Position (as at 30 June 2026, p.17)**:
  - **Total Assets**: US$1,608,075k (+60.1% YoY vs FY25 US$1,004,509k).
    - Non-current assets: US$1,279,570k (+42.3% YoY vs FY25 US$899,052k), dominated by Property, plant and equipment of US$1,196,474k (Note 7) and Environmental rehabilitation fund of US$34,617k.
    - Current assets: US$328,505k (+211.5% YoY vs FY25 US$105,457k), including Short-term investments of US$137,867k, Cash and cash equivalents of US$108,312k, Other receivables of US$41,654k, and Inventory of US$39,049k.
  - **Total Equity & Liabilities**: US$1,608,075k (ties Total Assets exactly).
    - Total Equity: US$1,035,997k (+89.5% YoY vs FY25 US$546,668k), comprising Retained earnings of US$1,027,194k, Shares to be issued of US$148,218k, Share capital of US$39,415k, and Reserves of $(176,192\text{k})$. Non-controlling interests: $(2,638\text{k})$.
    - Non-current liabilities: US$349,328k (+23.9% YoY vs FY25 US$281,970k), including Deferred tax liabilities of US$250,480k and Long-term borrowings of US$38,578k.
    - Current liabilities: US$222,750k (+26.7% YoY vs FY25 US$175,871k), including Trade and other payables of US$142,294k, Share-based payment obligations of US$43,969k, and Short-term borrowings of US$12,957k.

- **Statement of Profit or Loss and Other Comprehensive Income (year ended 30 June 2026, p.18)**:
  - **Revenue**: US$1,156,451k (+114.1% YoY vs FY25 US$540,033k).
  - **Cost of Production**: US$(514,297k) (+63.7% YoY vs FY25 US$(314,187k)).
  - **Gross Profit**: US$642,154k (+184.3% YoY vs FY25 US$225,846k). Gross margin expanded from 41.8% to 55.5%.
  - **Profit Before Finance**: US$545,838k (+152.9% YoY vs FY25 US$215,850k), after Other expenses of US$(85,958k), Royalty costs of US$(14,609k), and Other income of US$4,596k. Note: FY25 included US$28,019k of bargain purchase gains (nil in FY26).
  - **Finance Net**: Finance income US$5,848k less Finance costs US$(17,318k) = Net finance costs US$(11,470k).
  - **Profit Before Tax**: US$534,368k (+171.8% YoY vs FY25 US$196,633k).
  - **Income Tax Expense**: US$(177,457k) (effective tax rate 33.2% vs FY25 28.5%).
  - **Profit for the Period**: US$356,911k (+153.8% YoY vs FY25 US$140,605k), with US$357,215k attributable to owners of the Company.
  - **Total Comprehensive Income**: US$400,965k (includes US$42,726k foreign currency translation gains and US$1,897k FVTOCI adjustment less tax US$(569k)).
  - **Headline EPS**: 17.60 US cents (FY25: 7.16 US cents).

- **Statement of Cash Flows (year ended 30 June 2026, p.18)**:
  - **Cash Generated from Operating Activities**: US$556,991k (+259.7% YoY vs FY25 US$154,860k), after income tax paid of US$(74,135k), dividend paid of US$(58,540k), and finance costs paid of US$(14,987k).
  - **Cash Used in Investing Activities**: US$(352,144k) (+135.0% YoY vs FY25 US$(149,851k)), driven by PPE capex of US$(189,723k), Exploration capex of US$(26,030k), and net contributions to short-term investments of US$(136,586k) ($188,286\text{k} contributions less $51,700\text{k} withdrawals).
  - **Cash Used in Financing Activities**: US$(155,874k) (vs FY25 net cash from financing of US$17,457k), reflecting substantial net borrowings repayments of US$(149,311k).
  - **Cash Balance Roll-Forward**: Opening cash US$49,532k + Net increase US$48,973k + FX translation gain US$9,807k = **Closing cash US$108,312k**.

---

### 2. Footnotes, Qualifications and Reconciliations

Deterministic execution of statement-level checks in `tests_reconcile/test_primary_statements.py` proved all primary accounting identities:

1. **Fundamental Balance Sheet Invariant**:
   - Total Assets ($1,608,075\text{k}$) equals Total Equity and Liabilities ($1,608,075\text{k}$) for FY26.
   - For FY25, Total Assets ($1,004,509\text{k}$) equals Total Equity and Liabilities ($1,004,509\text{k}$). Both tie exactly with zero discrepancy.

2. **Cross-Statement Cash Tie (Balance Sheet vs Cash Flow Statement)**:
   - Balance Sheet Cash and cash equivalents (p.17, current assets): **US$108,312k**.
   - Cash Flow Statement Closing Cash (p.18, line 29): **US$108,312k**.
   - Identical tie confirmed for comparative FY25: **US$49,532k == US$49,532k**.

3. **Reciprocal Dividend Re-presentation (Footnote 1, physical p.18)**:
   - Footnote 1 notes: *"The Group changed the presentation of reciprocal dividend cash flows from gross to net during the current reporting period. The comparative figures have been re-presented accordingly."*
   - Dividend paid is presented as $(58,540\text{k})$ in FY26 and $(23,675\text{k})$ in FY25. The cash flow roll-forward ties the comparative exactly ($49,532\text{k} + 22,466\text{k} + 734\text{k} = 49,532\text{k}$), confirming the re-presentation is internal to financing lines.

4. **Cross-Section Revenue Bridge (IFRS p.18 vs Segmental Mining p.50, `Q-a0b503d7ac044eee`)**:
   - Primary Statement Revenue: **US$1,156,451k** ($1,156.451\text{m}$).
   - At the p.50 average exchange rate of $16.90\text{ US\$/ZAR}$, this implies $\text{ZAR } 19,544.0\text{m}$.
   - Group production summary (p.50) reports segmental mining revenue of $\text{ZAR } 17,249.1\text{m}$.
   - Delta of $\text{ZAR } 2,294.9\text{m}$ (US$135.8m) reflects Note 4 non-gold revenue, spot-to-average translation timing differences, and consolidation eliminations.

5. **Capex Tie (Cash Flow vs Segment Summary)**:
   - Cash flow payments for PPE ($189,723\text{k}$) + Exploration assets ($26,030\text{k}$) = **US$215,753k** ($215.8m).
   - This ties closely to the Section D009 segmental capex total of **US$214.9m** (p.50), with the $0.85m variance reflecting accruals and non-cash capital adjustments disclosed in Note 8.

---

### 3. Questions Answered and Next Evidence

- `Q-a0b503d7ac044eee` [high]: **Partial**. Mathematical bridge between IFRS consolidated revenue ($1,156.45\text{m US\$}$ / $\text{ZAR } 19,544.0\text{m}$) and segmental revenue ($\text{ZAR } 17,249.1\text{m}$) proved ($\Delta \text{ZAR } 2,294.9\text{m}$). Full breakdown requires Note 3 Segment Analysis (`Pending: S007/p.21–24`).
- `Q-c5e1b41b1cfe4dfb` [medium]: **Partial**. Note 4 disaggregation confirms Tennant gold revenue is consolidated in group US$ figures; currency translation impact across ZAR vs AUD requires Note 3 Australian segment review (`Pending: S007/p.22`).

**Next Evidence**: Section S007 (Note 3 Segment Analysis, physical pages 21–24) and Note 16 Borrowings (physical pages 32–33).
