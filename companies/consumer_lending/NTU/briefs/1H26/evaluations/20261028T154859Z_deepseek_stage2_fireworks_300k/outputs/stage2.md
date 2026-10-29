```json
{
  "ticker": "NTU",
  "company_name": "Nutun Limited",
  "sector": "consumer_lending",
  "jse_sector_code": "JS3020",
  "jse_sector_name": "Consumer Lending",
  "reference_price_zar": 0.89,
  "valuation_status": "WITHHELD",
  "blocking_issues": [
    "Funding, liquidity and covenant headroom NOT VERIFIED: facility-by-facility limits/drawn/undrawn, maturity dates, covenant definitions and compliance calculations, restricted/pledged cash, conditions, security, renewal terms and a dated cash forecast are not disclosed. Evidence: p.5 ~R0.8bn unutilised facilities; p.14 undrawn overdrafts R475m, total interest-bearing liabilities R4,016m, within-12-month maturity R1,396m; p.35 historical renewal commitment. Consequence: no dated funding runway or covenant-headroom conclusion; valuation withheld.",
    "PBD forecast and amortisation methodology NOT FULLY VERIFIED: explicit signed amortisation formula, portfolio-level ERC basis, collection curves/tail methodology, collection-cost assumptions and CAEIR/market-discount sensitivities are not disclosed. Evidence: p.13 principal and FVTPL rolls tie; p.21 CAEIR 19.2% and rolling 12-month net cash flow methodology; p.31 R597m component list; ERC R8,366m. Consequence: forecast PBD revenue, amortisation and cash conversion require explicit supported assumptions; valuation withheld."
  ],
  "valuation_checks": [
    {
      "check_id": "historical_cash_flow",
      "material": true,
      "verdict": "PASS",
      "evidence": "H1 2026 statutory cash-flow arithmetic and cash/overdraft reconciliation verified from pp.8, 10 and 12. This is not FCFE: statutory operating cash flow includes interest and tax and is before capex, lease principal and financing. Cash definition includes R1m HFS cash.",
      "reconciliations": [
        {"label": "H1 2026 closing cash Rm: opening 107 + net increase 6 + FX 0", "expected": 113, "actual": 113, "tolerance": 0},
        {"label": "H1 2026 balance-sheet cash plus HFS cash Rm: 112 + 1", "expected": 113, "actual": 113, "tolerance": 0},
        {"label": "H1 2026 closing overdraft Rm: opening 364 + drawdown 3178 - settlement 3269", "expected": 273, "actual": 273, "tolerance": 0}
      ]
    },
    {
      "check_id": "forecast_cash_and_debt",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "No dated forecast cash flow, facility-by-facility schedule, covenant headroom, restricted-cash schedule or conditions are disclosed. Static maturity minus cash/facilities is not a dated funding shortfall. Forecast cash/debt schedule not performed.",
      "reconciliations": []
    },
    {
      "check_id": "portfolio_rollforward",
      "material": true,
      "verdict": "PASS",
      "evidence": "Principal POCI and other FVTPL portfolios reconcile separately from p.13 and p.22. Principal POCI is Stage 3/POCI from inception; R431m is a signed cumulative impairment gain, not conventional loss coverage. Other FVTPL is separate and not ECL. H1 2026 impairment R167m is a six-month movement.",
      "reconciliations": [
        {"label": "Principal POCI H1 2026 Rm: 3975 + 382 - 728 + 383 - 167", "expected": 3845, "actual": 3845, "tolerance": 0},
        {"label": "Other FVTPL H1 2026 Rm: 702 + 28 - 116 + 30", "expected": 644, "actual": 644, "tolerance": 0},
        {"label": "Combined purchased book debts Rm: 3845 + 644", "expected": 4489, "actual": 4489, "tolerance": 0},
        {"label": "Principal POCI gross plus cumulative gain Rm: 3414 + 431", "expected": 3845, "actual": 3845, "tolerance": 0}
      ]
    },
    {
      "check_id": "valuation_bridge",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "Valuation bridge not performed because material liquidity/covenant and PBD forecast dependencies are unresolved. No target price, rating, upside, yield, TSR or rating bands are published.",
      "reconciliations": []
    },
    {
      "check_id": "sensitivity",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "Sensitivity matrix not performed because no base valuation is published and PBD collection/CAEIR and financing assumptions are not supported.",
      "reconciliations": []
    },
    {
      "check_id": "earnings_and_shares",
      "material": true,
      "verdict": "PASS",
      "evidence": "EPS, NAV, tax sign and share count arithmetic verified from pp.9, 16 and 18. Tax is a credit of R29m on loss before tax R92m; core reconciliation labels tax expense R(29)m to remove the credit. NAV uses closing net shares, not weighted-average EPS denominator.",
      "reconciliations": [
        {"label": "Net shares m: 784.313242 - 3.662209", "expected": 780.651033, "actual": 780.651033, "tolerance": 0},
        {"label": "NAV per share ZAR: 1329 / 780.651033", "expected": 1.70, "actual": 1.70, "tolerance": 0.01},
        {"label": "H1 2026 basic loss per share cents: -63 / 782.1 * 100", "expected": -8.1, "actual": -8.1, "tolerance": 0.1},
        {"label": "H1 2026 tax credit rate on pre-tax loss pct: 29 / 92 * 100", "expected": 31.5, "actual": 31.5, "tolerance": 0.1}
      ]
    },
    {
      "check_id": "financing_and_terminal",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "Financing and terminal policy cannot be set without facility-by-facility limits, covenant definitions/headroom, restricted cash, conditions, renewal terms and a dated cash forecast. Historical debt roll has an immaterial R3m unexplained residual and lease roll an immaterial R11m non-cash/other residual; neither is plugged. No terminal debt policy is published.",
      "reconciliations": []
    }
  ],
  "target_price_zar": null,
  "recommendation": null,
  "rating_bands": null,
  "implied_upside_pct": null,
  "forward_dividend_yield_pct": null,
  "projected_12m_tsr_pct": null
}
```

### Source Documents & Disclosures Considered
| # | Document Filename | Document Type | Pages | Period / Date | Primary Analytical Role & Key Evidence Considered |
| :---: | :--- | :---: | :---: | :---: | :--- |
| 1 | nutunlimitedcondensedconsolidatedafs31march2026.pdf | Condensed consolidated AFS | 38 | Half year ended 31 March 2026 | Primary source for H1 2026 financial position, income statement, cash flow, PBD/POCI and other FVTPL rolls, ECL, debt, shares, segments, going concern and fair value notes. |

### Valuation Summary Card
| Metric | Determination | Basis & Key Commentary |
| :--- | :---: | :--- |
| Sector | Consumer Lending (JS3020 / ICB 30201020) | Nutun is a PBD/RTC purchaser and agency collector in South Africa plus a BPO/customer-engagement and collections services provider internationally. |
| Current Reference Share Price | R0.89 | Frozen comparison reference only; not a current market quote. |
| Valuation Status | WITHHELD | Material liquidity/covenant and PBD forecast dependencies unresolved. |
| Blocking Issue 1 | Funding, liquidity and covenant headroom NOT VERIFIED | Facility-by-facility limits, covenant calculations, restricted cash, conditions, security, renewal terms and dated cash forecast are not disclosed. |
| Blocking Issue 2 | PBD forecast and amortisation methodology NOT FULLY VERIFIED | Explicit signed amortisation formula, ERC tail/collection curves, collection-cost assumptions and CAEIR sensitivities are not disclosed. |
| Verified Historical Anchors | PBD rolls tie; EPS/NAV arithmetic ties; cash/overdraft roll ties | Principal POCI 3,975 + 382 - 728 + 383 - 167 = 3,845; other FVTPL 702 + 28 - 116 + 30 = 644; net shares 780.651m; NAV R1.70. |
| Not Performed | Target price, rating, upside, yield, TSR, rating bands | Not published while WITHHELD. No illustrative scenario is used as a headline valuation. |

### Schedule Build Status
| Schedule | Status | Evidence |
| :--- | :---: | :--- |
| Portfolio rollforward | Built and tied | p.13, p.22 |
| Cash/overdraft roll | Built and tied | p.8, p.10, p.12 |
| Earnings/shares/NAV | Built and tied | p.9, p.16, p.18 |
| Forecast cash/debt | Not performed | Missing facility/covenant/dated forecast |
| Valuation bridge | Not performed | No target while WITHHELD |
| Sensitivity | Not performed | No base valuation |

### 1. Research Summary & Conditional Valuation
Nutun is not an originator lender. It is a principal PBD/RTC purchaser and agency collector in South Africa plus a BPO/customer-engagement and collections services provider internationally. Originator NIM/CLR, general-model Stage 1/2/3 staging for the POCI principal book and ABS terms are not applicable unless specifically established. The relevant metrics are PBD gross/net collections, acquisitions, CAEIR, signed ECL adjustments, ERC, FVTPL movements, cash conversion, facility headroom and segment EBITDA.

H1 2026 reported economics: statutory revenue R711m versus R745m; IFRS operating loss R79m; loss before tax R92m; income tax credit R29m; continuing and total loss R63m. Core EBITDA R790m is a non-IFRS CODM measure, not free cash flow. PBD/RTC carrying value is R4,489m, comprising principal POCI R3,845m and other FVTPL purchased book debts R644m. ERC is R8,366m. The principal roll ties: 3,975 + 382 additions - 728 net collections + 383 CAEIR - 167 impairment = 3,845. Other FVTPL roll ties: 702 + 28 - 116 + 30 = 644. The R431m positive cumulative balance is a cumulative impairment gain, not conventional loss coverage. The R167m current impairment loss is a six-month movement, not an annual figure.

Liquidity: cash R112m plus R1m HFS cash = R113m; bank overdrafts R273m; simple net cash R161m negative. Interest-bearing debt excluding overdrafts R3,743m; total interest-bearing liabilities including overdrafts R4,016m; lease liabilities R345m. Maturity within 12 months R1,396m. Only R475m undrawn overdraft facilities are explicitly disclosed; management refers to approximately R0.8bn unutilised facilities but no full facility schedule, covenant calculations, restricted-cash amount, conditions or dated cash forecast is supplied. A static maturity-minus-cash calculation is not a dated funding shortfall. Directors' going-concern statement is management evidence, not assurance.

The material unresolved issues are forward liquidity/covenant support and PBD forecast/amortisation methodology. No target, rating, upside, dividend yield, TSR or rating bands are produced. R0.89 is a frozen comparison reference only and is not used as a current quote.

Structural headwinds and tailwinds: PBD collections improved 28% to R773m, supported by R382m principal acquisitions and R28m other FVTPL acquisitions; CAEIR is 19.2%. Nutun International billable seats grew 20% to 2,491, but revenue fell 1% and EBITDA fell 15%, with adverse FX impacts of R27m on revenue and R46m on EBITDA. AI/automation and cost optimisation are potential margin supports. Dividends remain suspended. Trade receivables: balance-sheet R497m bridges to financial receivables R390m plus non-financial prepayments/VAT/deposits R107m; the matrix shows gross R374m, allowance R5m, net R369m. Simplified lifetime ECL policy is not explicit; zero short-dated ELRs prove neither adequacy nor manipulation, and no SICR allegation is made.

### 2. Detailed Operational & Segment Forecast (FY27E & FY28E)
| Metric | H1 2026A | H1 2025A | FY27E | FY28E | Basis |
| :--- | ---: | ---: | :---: | :---: | :--- |
| Revenue and other income Rm | 1,610 | 1,480 | WITHHELD | WITHHELD | p.3; forecast not performed |
| Nutun South Africa EBITDA Rm | 710 | 522 | WITHHELD | WITHHELD | p.3 |
| Nutun International EBITDA Rm | 80 | 93 | WITHHELD | WITHHELD | p.3 |
| Group core EBITDA Rm | 790 | 615 | WITHHELD | WITHHELD | p.3; non-IFRS |
| PBD/RTC amortisation Rm | 597 | 422 | WITHHELD | WITHHELD | p.3; six-month |
| Net interest cost Rm | 216 | 233 | WITHHELD | WITHHELD | p.3 |
| Core continuing loss Rm | (63) | (71) | WITHHELD | WITHHELD | p.3 |
| PBD/RTC carrying value Rm | 4,489 | 4,353 | WITHHELD | WITHHELD | p.3 |
| ERC Rm | 8,366 | 7,808 | WITHHELD | WITHHELD | p.3 |
| Billable seats | 2,491 | 2,069 | WITHHELD | WITHHELD | p.3 |

No FY27E/FY28E operational forecast is published. PBD collection curves, CAEIR, acquisition pipeline, facility schedule, covenant headroom and dated cash forecast are not supported. The R597m PBD amortisation APM is not fully reproduced: p.31 lists CAEIR R383m, impairment R167m, net collections R728m, FV movements R30m and other cash collections R116m, but the exact signed operator bridge is not explicit. This is not by itself a defect; Stage 2 does not model a signed formula without supported methodology.

### 3. Consolidated Financial Statements & FCFE Bridge
PBD net income components:
| Rm | H1 2026A | H1 2025A | FY25A |
| :--- | ---: | ---: | ---: |
| CAEIR imputed interest revenue | 383 | 333 | 683 |
| Interest expense | (177) | (181) | (354) |
| Impairment loss on principal book portfolios | (167) | (173) | (199) |
| Fair value movements on other financial assets | 30 | 74 | 114 |
| Net income from purchased book debts | 69 | 53 | 244 |

Income statement summary:
| Rm | H1 2026A | H1 2025A | FY25A |
| :--- | ---: | ---: | ---: |
| Revenue | 711 | 745 | 1,435 |
| Cost of revenue | (385) | (352) | (732) |
| Gross profit from provision of services | 326 | 393 | 703 |
| Net income from purchased book debts | 69 | 53 | 244 |
| Operating costs | (445) | (560) | (1,063) |
| Net finance charge | (39) | (52) | (91) |
| Net other income | 11 | 41 | 69 |
| Equity accounted loss | (1) | (43) | (48) |
| Operating loss | (79) | (168) | (186) |
| Non-operating (loss)/profit | (13) | 7 | 38 |
| Loss before tax | (92) | (161) | (148) |
| Income tax credit | 29 | 39 | 35 |
| Loss from continuing operations | (63) | (122) | (113) |
| Discontinued operations | 0 | 58 | (125) |
| Loss for the period | (63) | (64) | (238) |

Cash-flow bridge H1 2026:
| Rm | Amount | Check |
| :--- | ---: | :--- |
| Cash utilised by operations | (50) | |
| Interest received | 3 | |
| Interest paid | (225) | |
| Income taxes refunded | 2 | |
| Operating cash before working capital | (270) | -50 + 3 - 225 + 2 = -270 |
| Decrease in operating assets | 182 | |
| Changes in working capital | (23) | |
| Net cash utilised by operating activities | (111) | -270 + 182 - 23 = -111 |
| Net cash utilised by investing activities | (61) | |
| Net cash generated by financing activities | 178 | |
| Net increase in cash | 6 | -111 - 61 + 178 = 6 |
| Opening cash | 107 | |
| FX on cash | 0 | |
| Closing cash | 113 | 107 + 6 + 0 = 113 |

Statutory operating cash flow is not FCFE. PBD amortisation is not added back as a non-cash item; portfolio acquisitions are reinvestment. FCFE forecast is not published because forecast cash/debt and facility schedule are not verified. Historical debt roll: opening R3,443m + proceeds R1,145m - settlement R842m = R3,746m versus actual R3,743m, an immaterial R3m unexplained residual. Lease liabilities fell from R364m to R345m versus R30m repayment, an immaterial R11m non-cash/other residual. Neither is plugged.

Earnings, shares and NAV:
| Metric | H1 2026A | Basis |
| :--- | ---: | :--- |
| Ordinary equity Rm | 1,329 | p.8 |
| Net shares m | 780.651033 | p.16 |
| NAV per share ZAR | 1.70 | 1,329 / 780.651033 |
| Weighted average shares m | 782.1 | p.16 |
| Continuing basic loss per share cents | (8.1) | -63 / 782.1 * 100 |
| Tax credit Rm | 29 | p.9 |
| Loss before tax Rm | (92) | p.9 |
| Tax credit rate pct | 31.5 | 29 / 92 * 100 |

### 4. Institutional Valuation Table
| Item | Status | Basis |
| :--- | :---: | :--- |
| Valuation methodology | Not applied | Material liquidity/covenant and PBD forecast dependencies unresolved. |
| Target price | WITHHELD | No target published. |
| Recommendation | WITHHELD | No rating published. |
| Rating bands | WITHHELD | No bands published. |
| Implied upside | WITHHELD | No target. |
| Forward dividend yield | WITHHELD | Dividends suspended; no forecast. |
| Projected 12-month TSR | WITHHELD | No target or yield. |
| Reference price | R0.89 | Frozen comparison reference only; not a current quote. |

### 5. Forward Valuation Multiples & Sensitivity Matrix
| Sensitivity | Status | Reason |
| :--- | :---: | :--- |
| PBD CAEIR +/-100bp | Not performed | No supported collection curves/tail methodology. |
| PBD acquisition pace | Not performed | No pipeline/valuation support. |
| Funding cost +/-100bp | Not performed | No facility schedule/covenant headroom. |
| FX GBP/USD +/-10% | Not performed | No constant-currency forecast bridge. |
| Terminal multiple | Not performed | No base valuation. |

### 6. Actionable Portfolio Monitoring Triggers & Catalysts
Red lines: facility-by-facility limits, covenant definitions and headroom, restricted/pledged cash, conditions, security and renewal terms must be disclosed before a dated funding runway can be assessed. PBD collection curves, ERC tail methodology, CAEIR sensitivity, acquisition pipeline and collection-cost assumptions must be supported before PBD revenue, amortisation and cash conversion can be forecast. Trade receivables simplified lifetime ECL policy should be clarified; zero short-dated ELR is not proof of adequacy or manipulation. Directors' going-concern statements remain management evidence, not assurance.

Catalysts: FY26 audited results for year-end 30 September 2026 and any JSE SENS on facilities, covenants, PBD acquisitions, ERC, CAEIR, BPO FX/DTI incentives, AI/automation cost benefits and dividend policy. Monitor PBD gross collections, net collections after collection costs, principal and other FVTPL acquisitions, cumulative impairment gain movement, cash conversion, overdraft utilisation, undrawn facilities, debt maturities and lease movements. No target, rating, upside, yield, TSR or rating bands are published while valuation is WITHHELD.