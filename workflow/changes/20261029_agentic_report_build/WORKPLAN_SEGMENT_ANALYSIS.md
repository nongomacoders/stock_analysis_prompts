# WORKPLAN: Segment Analysis (Note 3, PAN physical pp.21–24)

**Target Section**: Section S007 (Note 3 Segment Analysis, physical pages 21, 22, 23, 24).  
**Source Document**: `companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` (`62b10bcd...`).  
**Reporting Currency & Units**: US$ thousand (`US$ '000`).  

---

### 1. Scope & Segment Analysis Layout

Note 3 presents Pan African's operating and financial results disaggregated across 10 operational and corporate segments plus subtotals and Group total:

1. **Columns (Segments)**:
   - `col0`: Barberton Mines
   - `col1`: Evander Mines
   - `col2`: Solar projects
   - `col3`: MTR operation
   - `col4`: Tennant Mines
   - `col5`: **Mining operations subtotal**
   - `col6`: Exploration assets
   - `col7`: Agricultural ESG projects
   - `col8`: Corporate
   - `col9`: Funding Company
   - `col10`: **Group total**

2. **Pages Structure**:
   - **Page 21 (FY26 Segment Profitability & Cost Breakdown)**:
     - Revenue (contracts with customers + total).
     - Cost of production and 14 detailed cost lines (Salaries and wages, Mining, Processing & metallurgy, Engineering, Electricity, Security, Reagents & consumables, Refining & freight, Other operating costs, Buy-in feedstock).
     - Depletion, depreciation & amortisation.
     - Net finance costs, Royalty costs.
   - **Page 22 (FY26 Segment Balance Sheet, Capex & EBITDA Reconciliation)**:
     - Segment assets (total assets excluding goodwill) $\rightarrow$ ties to $1,589,637\text{k}$ (plus goodwill $18,438\text{k} = 1,608,075\text{k}$).
     - Segment liabilities $\rightarrow$ ties to $572,078\text{k}$ ($349,328\text{k} + 222,750\text{k} = 572,078\text{k}$).
     - Net assets (excluding goodwill) $\rightarrow$ $1,017,559\text{k}$ (plus goodwill $18,438\text{k} = 1,035,997\text{k}$ Total Equity).
     - Capital expenditure $\rightarrow$ $223,995\text{k}$.
     - Adjusted EBITDA reconciliation per segment $\rightarrow$ ties to Group Adjusted EBITDA.
   - **Page 23 (FY25 Segment Profitability & Cost Breakdown)**:
     - Prior year comparative for all revenue and detailed cost lines.
   - **Page 24 (FY25 Segment Balance Sheet, Capex & EBITDA Reconciliation)**:
     - Prior year comparative for segment assets, liabilities, net assets, capex, and EBITDA.

---

### 2. Core Reconciliation Invariants for P2

1. **Horizontal Mining Subtotal Ties**:
   $$\text{col0 (Barberton)} + \text{col1 (Evander)} + \text{col2 (Solar)} + \text{col3 (MTR)} + \text{col4 (Tennant)} == \text{col5 (Mining operations)}$$
2. **Horizontal Group Total Ties**:
   $$\text{col5 (Mining ops)} + \text{col6 (Exploration)} + \text{col7 (ESG)} + \text{col8 (Corporate)} + \text{col9 (Funding)} == \text{col10 (Group total)}$$
3. **Cross-Section Primary Statement Ties (S006 p.18 vs Note 3 p.21)**:
   - Primary Statement Revenue ($1,156,451\text{k}$) == Note 3 Group total Revenue ($1,156,451\text{k}$).
   - Primary Statement Cost of Production ($(514,297\text{k})$) == Note 3 Group total Cost of Production ($(514,297\text{k})$).
   - Primary Statement Operating Profit ($545,838\text{k}$) == Note 3 Operating Profit ($545,838\text{k}$).
4. **Cross-Section Balance Sheet Ties (S006 p.17 vs Note 3 p.22)**:
   - Segment Assets ($1,589,637\text{k}$) + Goodwill ($18,438\text{k}$) == Primary Statement Total Assets ($1,608,075\text{k}$).
   - Segment Liabilities ($572,078\text{k}$) == Primary Statement Total Liabilities ($349,328\text{k} + 222,750\text{k} = 572,078\text{k}$).
   - Net Assets ($1,017,559\text{k}$) + Goodwill ($18,438\text{k}$) == Primary Statement Total Equity ($1,035,997\text{k}$).
5. **Cross-Section Segmental Revenue Resolution (`Q-a0b503d7ac044eee`)**:
   - Mining operations subtotal revenue ($1,155,857\text{k}$) + Corporate revenue ($594\text{k}$) = Group total ($1,156,451\text{k}$).
   - Reconciles D009 segmental revenue with IFRS revenue down to the dollar and segment.

---

### 3. P0 Acceptance Checklist

- [x] Scope bounded to Note 3 physical pages 21, 22, 23, 24.
- [x] Source document SHA-256 confirmed (`62b10bcd...`).
- [x] 11-column segmental matrix identified.
- [x] Core horizontal and cross-statement mathematical identities formulated.
- [x] Covenants respected: printed values preserved, no formulas, code-driven referee.
