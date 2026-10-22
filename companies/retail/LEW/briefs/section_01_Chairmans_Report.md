# Section 01: Chairmans Report

> **Package**: `section-52ffedecd51c47679c05798ee29108b7`  
> **Model**: `deepseek/deepseek-v4.1-flash-1017`  
> **Execution Time**: 21.04s  
> **Cost**: $0.0004  
> **Tokens**: 8,198 total (5,230 prompt / 2,968 completion)  

### 1. Answers to Stored Questions for This Section
*(No stored questions were supplied — this is the first captured section. Proceeding to footnote/qualification unpacking and new question generation.)*

### 2. Footnote & Qualification Deep-Dive
No formal footnote markers (`[^1]`, `*`, note references) appear in the supplied D002 evidence on pp. 7–8. However, several embedded qualifications and forward-looking claims require unpacking and verification:

- **"Increased revenue by 11.1%… expanded both gross and operating profit margins… grew the debtors book by 15.2%"** `[D002, physical PDF p. 7]` — No absolute revenue, gross margin %, or operating margin % figures are given here. The debtors book growth (15.2%) outpacing revenue growth (11.1%) is a critical credit-risk signal: it implies either (a) credit sales mix expansion, (b) slower collections, or (c) book inflation from arrears. Must be reconciled against debtor cost %, impairment allowance (ECL), and satisfactory-paid customer % in D004/D005/D006.
- **"18.3% increase in headline earnings per share to 1 753 cents"** `[D002, p. 7]` — Implies prior-year HEPS ≈ 1 482 cents (1 753 ÷ 1.183). No share count, WANS, or diluted HEPS given; buybacks (R2.3bn returned over 5 years includes repurchases) will affect comparability.
- **"Total dividend… increased by 12.1% to 897 cents per share"** `[D002, p. 7]` — Implied prior DPS ≈ 800 cents (897 ÷ 1.121). Implied payout ratio = 897 ÷ 1 753 = **51.2%**, which is *below* the stated "55% or higher" floor. This is a mathematical tension: either the payout ratio is calculated on a different earnings base (e.g., diluted HEPS, or attributable earnings rather than headline), or the "55% or higher" claim refers to a policy ceiling/historical average rather than the current year. **Flag as verification question.**
- **"Dividend represents an attractive yield of 11.4% at the date of the declaration"** `[D002, p. 7]` — Implies declaration-date share price ≈ 897 ÷ 0.114 ≈ **R78.68**. Useful for market-cap and valuation cross-checks; verify against D005/D006 share data.
- **"Six of its seven financial and operating targets… operating costs being the only metric outside the targeted range"** `[D002, p. 7]` — The seven targets and their actual values are not disclosed here. Must be located (likely D004 CFO Report) to assess cost growth vs revenue growth and the revised operating profit margin target.
- **"Operating profit margin target… increased… to reflect expected performance"** `[D002, p. 7]` — No quantum given. Forward-looking guidance; verify new target % in D004.
- **"Return on equity improved to 16.2% from 15.4%… from 8.7% three years ago"** `[D002, p. 8]` — No equity base disclosed. Verify opening/closing equity in D005 statement of changes in equity (p. 55 sighting).
- **Five-year cash flow summary** `[D002, p. 8]`: "R6.3bn cash after income tax and interest, R3.7bn invested in expanding debtors book, R2.3bn returned to shareholders (dividends + buybacks), R368m capex." — Capex of only R368m over five years is remarkably low relative to a store network with >10 900 employees; implies either heavily leased/franchised footprint or under-investment. Must reconcile against IFRS 16 right-of-use additions, store count changes, and refurbishment capex in D005/D006. Also note the R3.7bn debtors book investment is the dominant cash absorber — confirms credit-led growth model.
- **"More than 10 900 employees in South Africa and the neighbouring countries"** `[D002, p. 8]` — Confirms cross-border (Southern Africa) operations; segmental revenue split by geography must be verified in D004/D005.
- **"Mholi Shandu… director of Monarch Insurance Company Limited, the Group's insurance subsidiary"** `[D002, p. 8]` — Confirms an in-house insurance underwriting operation. This is material for revenue decomposition: credit life insurance premiums/underwriting profit may sit in "other/financial services revenue" and affect gross vs operating profit classification. Verify in D005/D006 segment notes.
- **Board diversity figures** `[D002, p. 8]`: black representation 44% (2025: 38%), female 33% (2025: 38%) — Governance only; no forecast impact, but note female representation *declined*.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D002, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q1 | High | D004 (CFO Report, pp. 48–50) | Dividend payout ratio: 897c ÷ 1 753c HEPS = 51.2%, below stated "55% or higher" floor `[D002, p. 7]` | Locate stated payout ratio and its denominator (HEPS vs diluted HEPS vs attributable earnings); reconcile to 897c DPS | Dividend sustainability and forward payout assumption in model |
| Q2 | High | D004 (CFO Report) | Debtors book grew 15.2% vs revenue +11.1% `[D002, p. 7]` | Extract gross debtors, debtor costs %, impairment allowance (ECL) %, satisfactory-paid customer %, collection rate %, write-offs | Credit book health is the core earnings-risk driver; determines provisioning forecast |
| Q3 | High | D004 (CFO Report) | "Six of seven targets met; operating costs the only miss" `[D002, p. 7]` | Obtain the seven targets table with actuals; extract operating cost growth % vs revenue growth %; new operating profit margin target % | Cost inflation is the key margin risk; revised target anchors forward margin |
| Q4 | High | D004 / D005 | Revenue +11.1%, gross & operating margins "expanded" — no absolute figures `[D002, p. 7]` | Extract total revenue, merchandise sales, other/financial services revenue, gross margin %, operating margin % | Baseline for revenue decomposition and margin bridge |
| Q5 | Medium | D005 / D006 | Five-year capex only R368m vs >10 900 employees `[D002, p. 8]` | Reconcile capex to store count changes, refurbishments, IFRS 16 right-of-use additions, lease liabilities | Tests whether footprint is leased/franchised; affects depreciation, lease finance charges, future capex forecast |
| Q6 | Medium | D005 / D006 | Monarch Insurance subsidiary — underwriting profit classification `[D002, p. 8]` | Check segment note: is insurance premium/underwriting profit in revenue, other income, or gross profit? | Revenue decomposition and gross vs operating profit treatment |
| Q7 | Medium | D005 (p. 55 changes in equity) | ROE 16.2% (2025: 15.4%) — no equity base `[D002, p. 8]` | Extract opening/closing total equity; recompute ROE = headline earnings ÷ average equity | Validates ROE and capital efficiency trend |
| Q8 | Medium | D004 / D005 | HEPS 1 753c (+18.3%); buybacks within R2.3bn returns `[D002, p. 7–8]` | Extract WANS, diluted WANS, shares repurchased, treasury shares | EPS comparability and per-share forecast |
| Q9 | Low | D004 / D005 | Dividend yield 11.4% implies share price ≈ R78.68 `[D002, p. 7]` | Confirm declaration-date share price and market cap | Valuation cross-check |
| Q10 | Low | D004 / D005 | Cross-border "neighbouring countries" operations `[D002, p. 8]` | Extract segmental revenue/profit by geography (South Africa vs rest of Southern Africa) | Regional growth and currency exposure in forecast |
| Q11 | Low | D004 | "Iran/Gulf conflict… higher fuel prices… supply chain costs" `[D002, p. 7]` | Check whether management quantifies fuel/freight cost impact in margin bridge | Cost-of-sales inflation assumption |

### 4. Updated Open Questions Ledger (Copy to App)

```markdown
## OPEN QUESTIONS LEDGER — after D002 (Chairman's Report, pp. 7–8)

### Pending: D004 (CFO Report, pp. 48–50)
- Q1 [HIGH] Payout ratio: 897c DPS ÷ 1 753c HEPS = 51.2%, below stated "55% or higher" floor. Verify stated payout ratio and its denominator (HEPS vs diluted vs attributable earnings).
- Q2 [HIGH] Debtors book +15.2% vs revenue +11.1%. Extract gross debtors, debtor costs %, ECL/impairment allowance %, satisfactory-paid customer %, collection rate %, write-offs.
- Q3 [HIGH] "Six of seven targets met; operating costs the only miss." Obtain seven-target table with actuals; operating cost growth % vs revenue growth %; new operating profit margin target %.
- Q4 [HIGH] Revenue +11.1%, gross & operating margins "expanded" — no absolutes. Extract total revenue, merchandise sales, other/financial services revenue, gross margin %, operating margin %.
- Q8 [MED] HEPS 1 753c (+18.3%); buybacks within R2.3bn returns. Extract WANS, diluted WANS, shares repurchased, treasury shares.
- Q9 [LOW] Dividend yield 11.4% implies share price ≈ R78.68. Confirm declaration-date share price and market cap.
- Q10 [LOW] Cross-border "neighbouring countries" operations. Extract segmental revenue/profit by geography.
- Q11 [LOW] Iran/Gulf conflict fuel & supply chain cost impact — check if quantified in margin bridge.

### Pending: D005 (Primary Financial Statements, pp. 54–82)
- Q4 [HIGH] (also D005) Revenue decomposition and gross margin absolutes.
- Q5 [MED] Five-year capex only R368m vs >10 900 employees. Reconcile capex to store count changes, refurbishments, IFRS 16 right-of-use additions, lease liabilities.
- Q6 [MED] Monarch Insurance subsidiary — check segment note: insurance premium/underwriting profit in revenue, other income, or gross profit?
- Q7 [MED] ROE 16.2% (2025: 15.4%) — extract opening/closing total equity from statement of changes in equity (p. 55); recompute ROE.
- Q8 [MED] (also D005) WANS, diluted WANS, treasury shares.
- Q9 [LOW] (also D005) Share price / market cap cross-check.
- Q10 [LOW] (also D005) Geographic segment split.

### Pending: D006 (Corporate Information, p. 83)
- Q5 [MED] (also D006) Store network / lease commitments / IFRS 16 detail if disclosed.
- Q6 [MED] (also D006) Insurance subsidiary disclosure.
```

### 5. Baseline Forecast Inputs Captured Here

| Metric | Value | Source |
| --- | --- | --- |
| Revenue growth | +11.1% | `[D002, p. 7]` |
| Gross margin | "expanded" (no % given) | `[D002, p. 7]` |
| Operating margin | "expanded" (no % given) | `[D002, p. 7]` |
| Debtors book growth | +15.2% | `[D002, p. 7]` |
| HEPS | 1 753 cents (+18.3%) | `[D002, p. 7]` |
| Implied prior HEPS | ≈ 1 482 cents | derived |
| DPS (total) | 897 cents (+12.1%) | `[D002, p. 7]` |
| Implied prior DPS | ≈ 800 cents | derived |
| Implied payout ratio | 51.2% (vs stated ≥55% floor) | derived — flag |
| Dividend yield (declaration date) | 11.4% | `[D002, p. 7]` |
| Implied share price | ≈ R78.68 | derived |
| 5-yr average dividend yield | 10.7% | `[D002, p. 7]` |
| ROE | 16.2% (2025: 15.4%; 3-yr-ago: 8.7%) | `[D002, p. 8]` |
| 5-yr cumulative cash after tax & interest | R6.3bn | `[D002, p. 8]` |
| 5-yr debtors book investment | R3.7bn | `[D002, p. 8]` |
| 5-yr shareholder returns (div + buyback) | R2.3bn | `[D002, p. 8]` |
| 5-yr capex | R368m | `[D002, p. 8]` |
| Employees | >10 900 (SA + neighbouring countries) | `[D002, p. 8]` |
| Targets met | 6 of 7 (operating costs missed) | `[D002, p. 7]` |
| Board: black representation | 44% (2025: 38%) | `[D002, p. 8]` |
| Board: female representation | 33% (2025: 38%) | `[D002, p. 8]` |
| Macro: SA unemployment Q1 2026 | 32.7% (~8.1m unemployed) | `[D002, p. 7]` |

### 6. Next Section to Capture
**D004 (CFO Report, physical pp. 48–50)** — resolves Q1, Q2, Q3, Q4, Q8, Q9, Q10, Q11 (the highest-priority credit-book, margin, cost, and payout-ratio questions). If D004 is unavailable, capture **D005 (Primary Financial Statements, pp. 54–82)** next to resolve Q4–Q10 via the income statement, balance sheet, and statement of changes in equity (p. 55).