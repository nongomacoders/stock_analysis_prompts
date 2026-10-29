```json
{
  "ticker": "NTU",
  "company_name": "Nutun Limited",
  "sector": "consumer_lending",
  "jse_sector_code": "JS3020",
  "jse_sector_name": "Consumer Lending",
  "valuation_status": "WITHHELD",
  "reference_price_zar": 0.89,
  "recommendation": null,
  "target_price_zar": null,
  "implied_upside_pct": null,
  "forward_dividend_yield_pct": null,
  "projected_12m_tsr_pct": null,
  "rating_bands": null,
  "blocking_issues": [
    "Liquidity/facility/covenant headroom: only R475m undrawn overdraft facilities are quantified (p.14), while management cites approximately R0.8bn unutilised facilities (p.5) and R1,396m of interest-bearing liabilities mature within 12 months (p.14). Needed: facility-by-facility maturities, covenant ratios, conditions, security, restricted cash and a dated cash forecast.",
    "POCI lifetime/tail methodology: the R3,845m principal POCI portfolio reconciles arithmetically, but the rolling 12-month cash-flow, lifetime and tail assumptions are not disclosed (pp.19,21,24). Needed: methodological support, collection assumptions and sensitivity.",
    "PBD cash-flow classification: POCI and other FVTPL portfolios reconcile separately, but total PBD carrying decrease of R188m versus the statutory operating-asset movement of R182m leaves an unbridged R6m residual (pp.12-13,29,31). Needed: cash-flow statement mapping of collections, acquisitions, CAEIR, impairment and collection costs.",
    "Trade-receivable simplified ECL policy and nonfinancial bridge: financial trade/other receivables are net R390m, with a R107m nonfinancial residual to balance-sheet trade and other receivables of R497m; simplified lifetime ECL and significant-financing-component policy are not established (pp.20,22,25). Needed: policy confirmation, aging/loss experience and forward-looking support.",
    "Tax/DTA recoverability: signed ETR computes to 31.5%, but the DTA R173m and DTL R513m recoverability and temporary-difference note is not captured (pp.8-9). Needed: DTA recoverability assumptions, temporary differences and tax-rate reconciliation.",
    "Historical-book vintage/FX attribution: dated ECL arithmetic is available, but vintage and FX breakdowns are absent (pp.24,35). Needed before attributing H1 FY26 historical-book loss of R191m to credit deterioration versus mix or FX."
  ],
  "valuation_checks": [
    {
      "check_id": "historical_cash_flow",
      "material": true,
      "verdict": "PASS",
      "evidence": "H1 2026 statutory cash-flow statement reconciles on p.12: operating -111, investing -61, financing 178; opening 107 plus net 6 plus FX 0 equals closing 113; balance-sheet cash 112 plus held-for-sale cash 1 equals 113. Debt/lease and PBD classification residuals are recorded separately and block forecast cash/debt readiness.",
      "reconciliations": [
        {"label": "H1 2026 net cash flow Rm: operating -111 + investing -61 + financing 178", "expected": 6, "actual": 6, "tolerance": 1},
        {"label": "H1 2026 closing cash Rm: opening 107 + net 6 + FX 0", "expected": 113, "actual": 113, "tolerance": 1},
        {"label": "31 Mar 2026 cash Rm: balance-sheet cash 112 + held-for-sale cash 1", "expected": 113, "actual": 113, "tolerance": 1}
      ]
    },
    {
      "check_id": "forecast_cash_and_debt",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "No dated forecast cash/debt schedule is built. Only R475m undrawn overdraft facilities are quantified (p.14); management's approximately R0.8bn unutilised facilities (p.5) is unscoped; R1,396m matures within 12 months (p.14). Facility-by-facility maturities, covenants, conditions, restricted cash and a dated cash forecast are missing.",
      "reconciliations": []
    },
    {
      "check_id": "portfolio_rollforward",
      "material": true,
      "verdict": "PASS",
      "evidence": "Arithmetic rollforwards for the two portfolios reconcile on pp.13,21-24,29. POCI: gross 3,414 plus cumulative impairment gain 431 equals net 3,845; opening 3,975 plus additions 382 less net collections 728 plus CAEIR 383 less impairment 167 equals 3,845. Other FVTPL: 702 plus additions 28 less collections 116 plus FV gains 30 equals 644. Combined PBD: 4,677 plus 410 plus 383 plus 30 less 167 less 844 equals 4,489. The POCI lifetime/tail methodology remains a separate NOT VERIFIED blocker.",
      "reconciliations": [
        {"label": "31 Mar 2026 POCI net carrying Rm: gross 3,414 + cumulative impairment gain 431", "expected": 3845, "actual": 3845, "tolerance": 1},
        {"label": "H1 2026 POCI net rollforward Rm: 3,975 + 382 - 728 + 383 - 167", "expected": 3845, "actual": 3845, "tolerance": 1},
        {"label": "H1 2026 other FVTPL rollforward Rm: 702 + 28 - 116 + 30", "expected": 644, "actual": 644, "tolerance": 1},
        {"label": "H1 2026 combined PBD rollforward Rm: 4,677 + 410 + 383 + 30 - 167 - 844", "expected": 4489, "actual": 4489, "tolerance": 1}
      ]
    },
    {
      "check_id": "valuation_bridge",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "Not performed because valuation is withheld. No EV-to-equity, DCF/SOTP bridge, target price, recommendation, rating bands, upside, dividend yield or TSR is published.",
      "reconciliations": []
    },
    {
      "check_id": "sensitivity",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "Not performed because no base valuation is published. No sensitivity cells are created to avoid a mechanically forced target.",
      "reconciliations": []
    },
    {
      "check_id": "earnings_and_shares",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "Historical H1 2026 earnings, NAV and share-count arithmetic is verified, but FY27E/FY28E forecast earnings and weighted-average shares are not built because the forecast is withheld. Historical anchors: PBT -92, tax credit 29, signed tax expense -29, signed ETR 31.5%; NAV 1,329 / 780.651033 shares = R1.70; basic LPS -63 / 782.1m = -8.06c versus reported -8.1c.",
      "reconciliations": []
    },
    {
      "check_id": "financing_and_terminal",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "No forecast borrowing, lease, refinancing or terminal debt policy is built. Historical debt bridge leaves R3m unexplained (interest-bearing debt increased R300m versus net proceeds R303m), lease liabilities fell R19m versus R30m repayment leaving R11m unexplained, and PBD cash-flow classification leaves R6m unbridged (pp.12-15,29,31).",
      "reconciliations": []
    }
  ]
}
```

### Source Documents & Disclosures Considered
| # | Document Filename | Document Type | Pages | Period / Date | Primary Analytical Role & Key Evidence Considered |
| :---: | :--- | :---: | :---: | :---: | :--- |
| 1 | `nutunlimitedcondensedconsolidatedafs31march2026.pdf` | Condensed consolidated AFS | 38 | 1H26 ended 31 March 2026 | Unaudited interim financial statements, PBD and ECL notes, cash-flow statement, segment report, tax/NAV/share data, liquidity disclosures and going-concern statement. No current market quote or post-period SENS supplied. |

### Valuation Summary Card
| Metric | Determination | Basis & Key Commentary |
| :--- | :---: | :--- |
| Sector | Consumer Lending (JS3020 / ICB 30201020) | Consumer lending sector classification; Nutun is a principal NPL purchaser and collections/BPO services group, not a conventional originator. |
| Current Reference Share Price | R0.89 | Frozen stored comparison reference only; not a verified current quote. |
| Valuation Status | WITHHELD | Material liquidity, POCI methodology, PBD cash-flow classification, trade ECL, tax and forecast dependencies remain unresolved. |
| 12-Month JSE Target Price | null | Not published while WITHHELD. |
| Implied Capital Upside / (Downside) | null | Not published while WITHHELD. |
| Forward Dividend Yield (FY27E) | null | Not published while WITHHELD; cash dividends are suspended. |
| Projected 12-Month TSR | null | Not published while WITHHELD. |
| Institutional Recommendation | null | Not published while WITHHELD. |
| Dynamic Rating Bands | null | Not published while WITHHELD. |

### Publication Decision and Conditional View
The valuation is withheld under the material-issue gate. Nutun South Africa is classified as a principal purchaser of unsecured NPL portfolios with a separate agent collections/recovery business; Nutun International is a BPO and collections/recovery services provider. Corporate services are not treated as a lending portfolio. Therefore originator NIM/CLR, general-model staging and ABS terms are not applied absent evidence.

The H1 2026 statutory result is a R63m loss. NAV is R1,329m, or R1.70 per share on 780.651m closing shares. The principal POCI portfolio reconciles arithmetically: gross R3,414m plus cumulative impairment gain R431m equals net R3,845m. The R431m cumulative impairment gain is not conventional loss coverage. Other FVTPL purchased book debt separately reconciles to R644m. No target, rating, upside, dividend yield or TSR is published.

### Verified Historical Reconciliations and Arithmetic
POCI principal book: opening net R3,975m plus additions R382m less net collections R728m plus CAEIR R383m less impairment R167m equals R3,845m. Gross R3,414m plus cumulative impairment gain R431m equals R3,845m.

Other FVTPL purchased book debt: opening R702m plus additions R28m less cash collections R116m plus fair-value gains R30m equals R644m.

Combined PBD arithmetic: opening R4,677m plus additions R410m plus CAEIR R383m plus FV R30m less impairment R167m less net cash collections R844m equals R4,489m. The combined carrying decrease is R188m versus the statutory purchased-book-debt operating-asset movement of R182m, leaving an unbridged R6m classification residual.

Historical ECL rollforward, read as dated intervals: 30 September 2024 to 31 March 2025 total impairment loss R173m equals acquired loss R96m plus historical loss R77m. 31 March 2025 to 30 September 2025 total impairment loss R26m equals acquired gain R156m less historical loss R182m. FY25 historical loss is R77m plus R182m equals R259m; FY25 total impairment loss is R173m plus R26m equals R199m. H1 FY26 total impairment loss R167m equals acquired gain R24m less historical loss R191m.

Statutory cash flow: operating R(111)m plus investing R(61)m plus financing R178m equals net R6m. Opening cash R107m plus net R6m plus FX nil equals closing R113m. Balance-sheet cash R112m plus held-for-sale cash R1m equals R113m. Debt bridge: interest-bearing debt increased R300m versus net proceeds of R303m, leaving R3m unexplained. Overdrafts fell R91m and net draw/settlement was R(91)m, reconciling. Lease liabilities fell R19m versus R30m repayment, leaving R11m unexplained.

Tax, NAV and shares: PBT is R(92)m; the tax line is a R29m credit, so signed tax expense is R(29)m. Signed ETR is (-29)/(-92) equals 31.5%. Parent ordinary equity R1,329m divided by 780.651033m closing shares equals R1.70 per share. Basic LPS is -63/782.1m times 100 equals -8.06c, consistent with reported -8.1c. Share capital R5,410m is not NAV.

Segment anchors: H1 2026 revenue and other income R1,610m versus R1,480m; EBITDA R790m versus R615m; PBD amortisation R597m versus R422m; net interest cost R216m versus R233m; core loss R63m versus R71m. Nutun South Africa EBITDA R710m versus R522m; Nutun International EBITDA R80m versus R93m.

### Seven-Check Readiness Contract Summary
| Check ID | Verdict | Consequence |
| :--- | :---: | :--- |
| historical_cash_flow | PASS | Statutory H1 2026 cash-flow arithmetic reconciles; no FCFE definition is selected because valuation is withheld. |
| forecast_cash_and_debt | NOT VERIFIED | Blocks forecast and valuation; facility, covenant, restricted-cash and dated cash-flow evidence missing. |
| portfolio_rollforward | PASS | POCI, other FVTPL and combined PBD arithmetic reconcile; POCI lifetime/tail methodology remains a separate blocker. |
| valuation_bridge | NOT VERIFIED | No target or bridge is published. |
| sensitivity | NOT VERIFIED | No sensitivity cells are produced without a base valuation. |
| earnings_and_shares | NOT VERIFIED | Historical arithmetic verified, but forecast earnings and forecast share count are not built. |
| financing_and_terminal | NOT VERIFIED | Borrowing, lease, refinancing and terminal policies cannot be forecast while liquidity and classification issues remain open. |

### Numerical Reconciliations for PASS Checks
| Check | Label | Expected | Actual | Tolerance |
| :--- | :--- | ---: | ---: | ---: |
| historical_cash_flow | H1 2026 net cash flow Rm: operating -111 + investing -61 + financing 178 | 6 | 6 | 1 |
| historical_cash_flow | H1 2026 closing cash Rm: opening 107 + net 6 + FX 0 | 113 | 113 | 1 |
| historical_cash_flow | 31 Mar 2026 cash Rm: balance-sheet cash 112 + held-for-sale cash 1 | 113 | 113 | 1 |
| portfolio_rollforward | 31 Mar 2026 POCI net carrying Rm: gross 3,414 + cumulative impairment gain 431 | 3845 | 3845 | 1 |
| portfolio_rollforward | H1 2026 POCI net rollforward Rm: 3,975 + 382 - 728 + 383 - 167 | 3845 | 3845 | 1 |
| portfolio_rollforward | H1 2026 other FVTPL rollforward Rm: 702 + 28 - 116 + 30 | 644 | 644 | 1 |
| portfolio_rollforward | H1 2026 combined PBD rollforward Rm: 4,677 + 410 + 383 + 30 - 167 - 844 | 4489 | 4489 | 1 |

### Forecast, Valuation and Sensitivity: Not Performed
No FY27E or FY28E operational forecast is published because material dependencies remain unsupported. No linked cash/debt forecast is built. No consolidated forecast income statement, balance sheet or FCFE bridge is published. No DCF, SOTP, EV-to-equity bridge, target price, rating bands, sensitivity matrix, dividend forecast or TSR is published. Historical verified arithmetic is preserved above.

### Actionable Monitoring Triggers and Catalysts
Liquidity: obtain a facility-by-facility schedule, covenant compliance, renewal conditions, security, restricted cash, maturity dates and a dated cash forecast covering the R1,396m within 12 months and the claimed approximately R0.8bn unutilised facilities.

POCI methodology: obtain rolling 12-month collection, lifetime and tail assumptions for the R3,845m POCI portfolio, including vintage and portfolio-segment sensitivity.

PBD classification: obtain a cash-flow statement mapping of collections, acquisition spend, CAEIR, impairment and collection costs to resolve the R6m carrying-value versus statutory operating-asset movement residual.

Trade receivables: confirm simplified lifetime ECL applicability, significant-financing-component policy, aging/loss experience and forward-looking support for zero matrix rates; reconcile the R107m nonfinancial residual.

Tax and DTA: obtain DTA recoverability assumptions, temporary differences and tax-rate reconciliation for DTA R173m and DTL R513m.

Historical-book credit trend: obtain vintage and FX attribution before treating the H1 FY26 historical-book loss of R191m as pure credit deterioration.

Market quote: R0.89 is a frozen comparison reference only. No current quote or subsequent SENS is supplied, so no market-return conclusion is published.