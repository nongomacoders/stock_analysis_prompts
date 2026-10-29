## 1. Research Summary & Conditional Valuation (Target Only When READY)

```json
{
  "ticker": "DCP",
  "company_name": "Dis-Chem Pharmacies Limited",
  "sector": "retail",
  "jse_sector_code": "JS4041",
  "jse_sector_name": "Retailers",
  "recommendation": null,
  "reference_price_zar": 28.08,
  "target_price_zar": null,
  "implied_upside_pct": null,
  "forward_dividend_yield_pct": null,
  "projected_12m_tsr_pct": null,
  "valuation_status": "WITHHELD",
  "blocking_issues": [
    "U1: Merchandise vs customer financial services revenue split not disclosed; Note 7 p.31 and Note 8 p.32 leave R150.703m FY2026 / R146.209m FY2025 other income unlisted.",
    "N2: Gross margin bridge incomplete; no rand split of rebates between COGS and inventory, no shrinkage rate, no Better Rewards discount cost, no R330m/R115m line items; Note 8 other expenses leaves ~R592.7m unlisted.",
    "N3: Debtor ECL adequacy not supported; gross trade receivables +18.4%, coverage flat at 1.18%, 60-90 day bucket +160% with ECL rate falling to 1.7%, other receivables/accrued income ~R1.72bn unaged.",
    "N4: Store portfolio/trading space/capex split/pipeline not reconciled; 358 stores verified, but trading space and trading density not disclosed; FY2027 pipeline inconsistent (34 stores p.23, 35 stores p.28, 34 stores/31,198m2 p.19).",
    "N5: IFRS 16 lease structure incomplete; escalation rates, average remaining term, optional renewals and ROU depreciation split not disclosed.",
    "N6: Covenant headroom/liquidity runway not quantified; Group gearing 2.8x per Note 29 p.79, not 2.6x as in Stage 1; no thresholds or headroom in Rm/x; Standard Bank bullet matures 31 May 2027.",
    "N7: Post-year-end SENS/trading/S189/final dividend not verified; Note 31 does not quantify S189 cost/saving; presentation p.19 says 545 affected, not 505; final dividend not in Note 31.",
    "N8: Cash conversion/FCF/dividend sustainability not verified; OCF R1,792.711m is after finance costs, tax and dividends; working capital inflow R125.820m driven by payables +R663.918m; SCF payables R965m in trade payables.",
    "N9: Interim DPS/share-count bridge fails; R254.268m interim at 29.41734c implies ~864.3m shares vs 860.084m issued; final R137m reconciles to ~860.6m.",
    "N10: Tax/DTA/unrecognised losses not entity-analysed; DTA on tax losses R69.290m; unrecognised assessed losses R202m vs R88m; no FY2027 ETR.",
    "N11: Goodwill CGU headroom not disclosed; goodwill R948.385m; Baby R343.957m + Pure Pharmacy R255.890m = 63.2%; no headroom sensitivity.",
    "N12: Dis-Chem Life preference shares/impairment not disclosed; R189m preference shares; Company carrying R344.940m; Group equity-accounted R265.323m; share of loss R50.186m.",
    "N13: SCF payables/covenant treatment not disclosed; R965m SCF payables in trade payables; no covenant inclusion/exclusion or reclassification sensitivity.",
    "N14: JIBAR/ZARONIA/refinancing not quantified; no JIBAR-linked debt quantum, margin calibration or facility-by-facility fallback status.",
    "N15: Inventory adequacy/shrinkage not disclosed; inventory R7,908.461m; obsolete provision R3m; write-offs R15m vs R49m; no shrinkage rate.",
    "N16: Wholesale p.21 table requires correction; Stage 1 misread customer counts as revenue. Primary p.21 shows customer counts 316/280/1,325 and revenue R27,811m/R2,892m/R3,341m; FY2026 sums to R34,044m and reconciles to AFS, but FY2025 revenue sums to R29,585m vs AFS R30,099m, a R514m gap.",
    "N17: TLC store/clinic counts inconsistent; 280 pharmacies; clinics 218 vs 193; no reconciliation.",
    "N18: Non-audit fee discrepancy; audit committee p.7 says R230,000; Note 8 p.32 says R315k; R85k difference unresolved.",
    "N19: Gearing definition undisclosed; Group gearing 2.8x per Note 29 p.79 (2025: 2.3x); Company 2.3x (2025: 2.5x); cannot reconcile to net debt/equity or net debt/EBITDA.",
    "N20: Better Rewards cost/liability not quantified; Stage 1 R1,126.9m is not supported; presentation p.16 shows cumulative discount value since launch of R761.2m; annual cost and liability still not disclosed.",
    "N21: X/bigly labs and S189 not separately quantified; R330m X/bigly labs and R115m non-recurring disclosed narratively; S189 545 affected per presentation p.19, not 505; no AFS line items or provision.",
    "N22: Final dividend not in Note 31; 15.91872c approved 28 May 2026; ~R137m; not disclosed as subsequent event in Note 31."
  ],
  "valuation_checks": [
    {
      "check_id": "historical_cash_flow",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "AFS Note 27 pp.60-62: OCF R1,792.711m is after finance costs, tax and dividends; cash from trading operations R3,124.134m; working capital inflow R125.820m driven by trade payables +R663.918m; capex R1,103.588m; lease principal R691.992m; net overdraft R1,166.964m. No management FCF definition or normalised working capital reconciliation.",
      "reconciliations": []
    },
    {
      "check_id": "forecast_cash_and_debt",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "No FY2027/FY2028 cash and debt roll-forward can be completed because covenant headroom, facility drawn/undrawn status, SCF covenant treatment, R500m bullet drawdown terms, JIBAR/ZARONIA quantum and S189 cost/saving are not disclosed.",
      "reconciliations": []
    },
    {
      "check_id": "portfolio_rollforward",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "Store count 358 verified (316 pharmacy + 42 Baby City) from IAR p.3 and CFO report p.104; trading space m2, trading density, capex split by new store/refit/IT/maintenance and signed vs pipeline status are not disclosed. Presentation p.25 total 355 is a typo; p.23 says 34 stores planned for FY2027, p.28 says 35, p.19 table shows 34 stores/31,198m2.",
      "reconciliations": []
    },
    {
      "check_id": "valuation_bridge",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "No valuation bridge is published. IFRS 16 basis not selected; net debt definition unresolved; SCF payables treatment unresolved; no normalised FCF; no target multiple or WACC/terminal growth support.",
      "reconciliations": []
    },
    {
      "check_id": "sensitivity",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "No sensitivity cells are published because no base valuation exists. Historical HEPS sensitivity can be computed, but fair value per share sensitivity cannot be reproduced without a valuation bridge.",
      "reconciliations": []
    },
    {
      "check_id": "earnings_and_shares",
      "material": true,
      "verdict": "PASS",
      "evidence": "AFS Note 11 p.36: weighted-average basic shares 857,006,527; diluted 857,817,750; basic HEPS 113.7c; diluted HEPS 113.6c; headline earnings R974.821m. Basic EPS 114.2c. Continuing HEPS equals 113.7c because no discontinued operations.",
      "reconciliations": [
        {"label": "FY26 basic HEPS cents", "expected": 113.7, "actual": 113.7, "tolerance": 0.1},
        {"label": "FY26 diluted HEPS cents", "expected": 113.6, "actual": 113.6, "tolerance": 0.1},
        {"label": "FY26 weighted-average basic shares m", "expected": 857.006527, "actual": 857.006527, "tolerance": 0.000001},
        {"label": "FY26 diluted weighted-average shares m", "expected": 857.817750, "actual": 857.817750, "tolerance": 0.000001},
        {"label": "FY26 headline earnings Rm", "expected": 974.821, "actual": 974.821, "tolerance": 0.001}
      ]
    },
    {
      "check_id": "financing_and_terminal",
      "material": true,
      "verdict": "NOT VERIFIED",
      "evidence": "Borrowing, leases, refinancing, equity dilution and terminal debt policy cannot be reconciled. Group gearing 2.8x per Note 29 p.79; no covenant thresholds/headroom; Standard Bank bullet matures 31 May 2027; R500m post-year-end bullet at 3M JIBAR+1.3%; JIBAR/ZARONIA quantum not disclosed; lease optional renewals not quantified.",
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
| 1 | `1780031707-FY2026AnnualFinancialStatements.pdf` | [AR] General Annual Report (AR) | 87 | FY26 | Audited Group and Company AFS: primary statements, Notes 1-31, auditor's report, directors' report, audit committee report, segmental note, revenue, other income/expenses, debtors ECL, inventory, leases, loans, cash flow, tax, goodwill, related parties, subsequent events. |
| 2 | `1780031786-FY2026AnalystPresentation.pdf` | [PRES] Results Presentation (PRES) | 40 | FY26 | FY2026 results presentation: group financial summary, revenue/total income tables, operating profit, HEPS/EPS, working capital, cash management, capex, retail/wholesale trading, Better Rewards, X/bigly labs, store pipeline, outlook, segmental information, definitions. |
| 3 | `1785744572-DIS-CHEMIR2026INTERACTIVE.pdf` | [IAR] Integrated Annual Report (IAR) | 132 | FY26 | Integrated Annual Report: strategy, risks, governance, remuneration, CEO/CFO reports, summary consolidated financial information, shareholder analysis, AGM notice, definitions, corporate information. |

No SENS notices were supplied. SENS-dependent items remain NOT VERIFIED.

### Valuation Summary Card

| Metric | Determination | Basis & Key Commentary |
| :--- | :---: | :--- |
| **Sector** | Retail (Retailers — JS4041 / ICB 404010) | JSE sector code JS4041; retail pharmacy and wholesale. |
| **Current Reference Share Price** | R28.08 | Frozen stored baseline for comparison; not a verified current quote. |
| **Valuation Status** | WITHHELD | Material issues unresolved; no target, rating, upside, dividend yield, TSR or recommendation published. |
| **Blocking Issues** | U1, N2-N22 | See JSON and Section 1.5; key blockers include CFS revenue split, gross-margin bridge, ECL adequacy, store/trading space, IFRS 16 lease structure, covenant headroom, FCF, dividend bridge, tax, goodwill, Dis-Chem Life, SCF, JIBAR/ZARONIA, inventory, wholesale table, TLC counts, non-audit fees, gearing definition, Better Rewards, X/bigly labs/S189, final dividend. |
| **Rating Bands** | Not published | rating_bands is null while valuation is withheld. |

### Core Institutional Thesis, Headwinds and Tailwinds

No investment conclusion is produced. The verified operating picture is: revenue growth +9.3% to R42.826bn, gross margin -50bps to 21.97%, operating profit -11.9% to R1.853bn, HEPS -17.3% to 113.7c, net overdraft R1.167bn, lease liabilities R2.943bn. The equity story cannot be adjudicated until the blockers are resolved.

Structural tailwinds include defensive healthcare spend, dispensary mix, store rollout, wholesale scale, early Better Rewards traction and the integrated healthcare ecosystem. Structural headwinds include consumer pressure, margin dilution from wholesale mix, ecosystem investment, higher finance costs, working capital payables stretch, ECL opacity, lease commitments, regulatory pricing (SEP/dispensing fees), competition and execution complexity. The key debate is whether FY2026 earnings decline is a temporary investment year or a structural margin/cost problem; the AFS do not provide enough granularity to decide.

### Stage 1 Reopen: Verified, Refined, Contradicted

| Stage 1 Claim | Primary Evidence | Stage 2 Determination |
| :--- | :--- | :--- |
| Auditor opinion unmodified; only KAM rebates and advertising agreements; no going-concern material uncertainty. | AFS independent auditor's report pp.9-11. | VERIFIED. Unmodified opinion; KAM is rebates and advertising agreements (Note 3.6, 8, 16); no going-concern material uncertainty paragraph. |
| HEPS reconciliation "18 324" is R18k FY2026 and R324k FY2025, not R18.324m. | AFS Note 11 p.36; arithmetic 978,894 - 294 + 18 - 5,283 + 1,486 = 974,821. | VERIFIED. Basic HEPS 113.7c; diluted 113.6c; weighted-average shares 857,006,527; diluted 857,817,750. |
| Group gearing 2.6x (2025: 2.3x) excluding finance leases. | AFS Note 29 p.79 says Group gearing 2.8x (2025: 2.3x); Company Note 29 p.82 says 2.3x (2025: 2.5x). | CONTRADICTED. Use Group 2.8x, not 2.6x. Definition still undisclosed. |
| S189 restructuring affected 505 employees. | Presentation p.19 says 545 employees affected; AFS Note 31 p.83 does not quantify. | REFINED. Use 545 affected per presentation; still unaudited and no rand cost/saving/provision. |
| FY2027 pipeline: p.23 13 new stores / 24,000m². | Presentation p.23 says 34 retail pharmacy stores planned for FY2027 (eight already trading); p.19 table shows FY2027 total 34 stores / 31,198m²; commentary p.28 says 35 stores. | CONTRADICTED. Stage 1 13/24,000 is not supported. Use 34-35 stores / 31,198m², with inconsistency. |
| p.21 wholesale table internally inconsistent: R316m + R280m + R1,329m = R1,925m vs printed R2,911m. | Presentation p.21: 316/280/1,325 are customer counts; revenue row is R27,811m/R2,892m/R3,341m. FY2026 sums to R34,044m and reconciles to AFS total wholesale revenue R34,044,309k. FY2025 revenue sums to R29,585m vs AFS R30,099m, a R514m gap. | CONTRADICTED/REFINED. Stage 1 misread customer counts as revenue. FY2026 reconciles; FY2025 has R514m gap. |
| Better Rewards cumulative discount value R1,126.9m. | Presentation p.16 total discount value since launch is R761.2m (components 541.4 + 57.5 + 54.5 + 95.4 + 12.5 = 761.3m). | CONTRADICTED. Use R761.2m cumulative since launch; annual cost/liability still not disclosed. |
| p.4 "163,000m²" likely trading space. | Presentation p.4 and p.19 say pipeline at 163,000m². | REFINED. It is pipeline, not trading space. Trading space still not disclosed. |
| Presentation p.25 total stores 355. | IAR p.3 and CFO report p.104 say 358 (316 pharmacy + 42 Baby City). | PRIMARY INCONSISTENCY. Use 358; p.25 table has typo 355. |
| Presentation p.25 new stores total 31. | CFO report p.104: gross openings 33, closures (2) pharmacy and (3) Baby City, net pharmacy +31, total net +28. | PRIMARY INCONSISTENCY. Use gross 33, net pharmacy +31, total net +28. |

### Unresolved Material Dependencies U1-U22

| ID | Material FAIL / NOT VERIFIED Claim | Source Pages | Evidence Needed to Close | Stage 2 Treatment |
| :--- | :--- | :--- | :--- | :--- |
| U1 | Merchandise vs customer financial services revenue split not disclosed. | Note 7 p.31; Note 8 p.32. | Note 7 disaggregation with finance charges, initiation fees, monthly service fees, credit life insurance; complete Note 8 other-income breakdown. | VALUATION WITHHELD. |
| N2 | Gross margin bridge incomplete. | Note 16 p.47; Note 8 p.32; Note 3.6 p.20. | Rand split of rebates between COGS/inventory; shrinkage; Better Rewards discount cost; R330m/R115m line items; complete Note 8 other-expenses. | VALUATION WITHHELD. |
| N3 | Debtor ECL adequacy not supported. | Note 17 pp.48-49; Note 29 pp.76-77. | Satisfactory-paid %, collection rate, ECL staging, forward-looking assumptions, ageing of other receivables/accrued income, post-year-end collections/SENS. | VALUATION WITHHELD. |
| N4 | Store portfolio/trading space/capex split/pipeline not reconciled. | p.19; p.23; p.25; p.27; p.29; p.100; p.104. | Store portfolio table with m², trading density, net openings/closures; PPE additions split by new store/refit/IT/maintenance; signed vs pipeline status; footnote [^45]. | VALUATION WITHHELD. Stage 1 13/24,000 corrected to 34-35 stores/31,198m². |
| N5 | IFRS 16 lease structure incomplete. | Note 22 p.55; Note 27.6 p.62; Note 9 p.33. | Escalation rates, average remaining term, optional renewal commitments, ROU depreciation, lease term assumptions, FY2025 release explanation. | VALUATION WITHHELD. |
| N6 | Covenant headroom/liquidity runway not quantified. | Note 29 p.79; Note 23 p.56; Note 31 p.83. | Covenant thresholds, actual ratios at Feb 2026/Aug 2025, headroom in Rm/x, committed/uncommitted facility status, drawn/undrawn split, R500m drawdown/purpose/interest. | VALUATION WITHHELD. Group gearing 2.8x per Note 29 p.79, not 2.6x. |
| N7 | Post-year-end SENS/trading/S189/final dividend not verified. | Note 31 p.83; directors' report p.4; Note 21 p.54; presentation p.29. | SENS announcements, trading update, Note 31 full text, S189 cost/saving/provision, R500m drawdown terms, final dividend DWT/cash impact. | VALUATION WITHHELD. S189 545 affected per presentation p.19, not 505. |
| N8 | Cash conversion/FCF/dividend sustainability not verified. | Note 27 pp.60-62; Note 24 p.57; Note 29 p.79. | Management FCF definition; normalised working capital; SCF covenant treatment; capex/lease/finance-cost bridge; dividend policy target and record-date share counts. | VALUATION WITHHELD. |
| N9 | Interim DPS/share-count bridge fails. | Directors' report p.4; Note 21 p.54; Note 11 p.36. | Dividend record-date share counts, treasury-share treatment, exact interim dividend amount/DPS, SENS declaration. | VALUATION WITHHELD. |
| N10 | Tax/DTA/unrecognised losses not entity-analysed. | Note 14 p.45; tax note p.35. | Entity-level DTA/unrecognised losses; FY2027 taxable income/ETR; 80% assessed-loss cap utilisation. | VALUATION WITHHELD. |
| N11 | Goodwill CGU headroom not disclosed. | Note 13 p.44. | CGU-level recoverable amount, headroom, discount-rate build-up, terminal-growth sensitivity. | VALUATION WITHHELD. |
| N12 | Dis-Chem Life preference shares/impairment not disclosed. | Note 4 p.25; Note 15 p.46; Note 18 p.50; Note 28 p.64. | Preference share terms, redemption, dividend rate, conversion, impairment assessment, SENS. | VALUATION WITHHELD. |
| N13 | SCF payables/covenant treatment not disclosed. | Note 24 p.57; Note 29 p.79. | Covenant definitions, SCF inclusion/exclusion, reclassification sensitivity, facility terms. | VALUATION WITHHELD. |
| N14 | JIBAR/ZARONIA/refinancing not quantified. | Note 23 p.56; Note 29 p.78. | JIBAR-linked debt quantum, facility-by-facility fallback status, margin calibration, refinancing term sheet. | VALUATION WITHHELD. |
| N15 | Inventory adequacy/shrinkage not disclosed. | Note 16 p.47. | Inventory ageing, shrinkage rate, write-down policy, stock-out risk, provision adequacy. | VALUATION WITHHELD. |
| N16 | Wholesale p.21 table requires correction. | Presentation p.21; AFS segmental note p.35. | Note 7/segmental reconciliation of wholesale external vs intergroup; corrected p.21 table. | VALUATION WITHHELD. Stage 1 misread customer counts as revenue; FY2026 revenue reconciles, FY2025 has R514m gap. |
| N17 | TLC store/clinic counts inconsistent. | p.15; p.27; p.99. | TLC network table with pharmacies, clinics, ownership/consolidation status. | VALUATION WITHHELD. |
| N18 | Non-audit fee discrepancy. | Audit committee p.7; Note 8 p.32. | Auditor fee note reconciliation. | VALUATION WITHHELD. |
| N19 | Gearing definition undisclosed. | Note 29 p.79. | Gearing numerator/denominator definition and reconciliation. | VALUATION WITHHELD. Group 2.8x, Company 2.3x. |
| N20 | Better Rewards cost/liability not quantified. | Presentation pp.15-16; Note 26 p.59. | Annual Better Rewards discount cost, launch date, breakage, supplier funding split, Note 8/16 reconciliation. | VALUATION WITHHELD. Stage 1 R1,126.9m corrected to R761.2m cumulative since launch. |
| N21 | X/bigly labs and S189 not separately quantified. | p.27; p.98; Note 31 p.83. | Capex/opex split, FY2027 return guidance, S189 cost/saving/provision. | VALUATION WITHHELD. S189 545 affected per presentation p.19, not 505. |
| N22 | Final dividend not in Note 31. | Directors' report p.4; Note 21 p.54; Note 31 p.83. | Note 31 subsequent-event disclosure or SENS; DWT treatment; FY2027 opening cash outflow. | VALUATION WITHHELD. |

## 2. Detailed Operational Forecast (Historical Base Period + FY26A, FY27E & FY28E)

FY26E in the prompt is treated as FY26A because audited FY2026 results are available. FY27E and FY28E are not published because the material dependencies above prevent a defensible forecast.

| Driver | FY25A | FY26A | FY27E | FY28E | Source / Status |
| :--- | ---: | ---: | :---: | :---: | :--- |
| Retail external revenue (R'm) | 33,569.780 | 36,592.332 | WITHHELD | WITHHELD | AFS Note 6 p.29; CFS split not disclosed. |
| Wholesale external revenue (R'm) | 5,602.567 | 6,233.445 | WITHHELD | WITHHELD | AFS Note 6 p.29. |
| Intergroup wholesale revenue (R'm) | 24,496.539 | 27,810.864 | WITHHELD | WITHHELD | AFS Note 6 p.29; eliminated. |
| Total revenue (R'm) | 39,172.347 | 42,825.777 | WITHHELD | WITHHELD | AFS p.13. |
| Merchandise vs CFS revenue split | n/d | n/d | WITHHELD | WITHHELD | Note 7 p.31; U1. |
| Credit vs cash mix | n/d | n/d | WITHHELD | WITHHELD | Note 7/29; N3. |
| Gross margin % | 22.47% | 21.97% | WITHHELD | WITHHELD | AFS p.13; bridge incomplete N2. |
| Total income margin % | 31.01% | 30.84% | WITHHELD | WITHHELD | AFS p.13; Note 8 unlisted R592.7m. |
| Debtor cost % | n/d | n/d | WITHHELD | WITHHELD | Note 17/29; N3. |
| Store count (pharmacy + Baby City) | 285+45=330 | 316+42=358 | WITHHELD | WITHHELD | IAR p.3; CFO report p.104; presentation p.25 typo 355. |
| Net pharmacy openings | n/d | +31 | WITHHELD | WITHHELD | CFO report p.104; gross 33, closures 2. |
| Baby City closures | n/d | -3 | WITHHELD | WITHHELD | CFO report p.104. |
| Trading space m² | n/d | n/d | WITHHELD | WITHHELD | p.25 table CID-encoded; N4. |
| Trading density (sales/m²) | n/d | n/d | WITHHELD | WITHHELD | N4. |
| Capex (R'm) | 1,402.144 | 1,103.588 | WITHHELD | WITHHELD | AFS Note 27 p.60. |
| Maintenance capex (R'm) | 941.548 | 373.968 | WITHHELD | WITHHELD | AFS Note 27 p.60. |
| Expansion capex (R'm) | 460.596 | 729.620 | WITHHELD | WITHHELD | AFS Note 27 p.60. |
| IFRS 16 lease liability (R'm) | 2,663.849 | 2,943.233 | WITHHELD | WITHHELD | AFS Note 22 p.55; N5. |
| Lease interest (R'm) | 253.250 | 252.413 | WITHHELD | WITHHELD | AFS Note 9 p.33. |
| Lease principal repayment (R'm) | 641.172 | 691.992 | WITHHELD | WITHHELD | AFS Note 27.6 p.62. |
| New leases (R'm) | 824.373 | 992.172 | WITHHELD | WITHHELD | AFS Note 27.6 p.62. |
| SCF payables (R'm) | 784 | 965 | WITHHELD | WITHHELD | AFS Note 24 p.57; N13. |
| Net overdraft (R'm) | 732.283 | 1,166.964 | WITHHELD | WITHHELD | AFS Note 27.5 p.61. |
| Group gearing (excl. finance leases) | 2.3x | 2.8x | WITHHELD | WITHHELD | AFS Note 29 p.79; Stage 1 2.6x corrected. |
| S189 affected employees | n/a | 545 | WITHHELD | WITHHELD | Presentation p.19; Note 31 p.83 does not quantify; N21. |
| Better Rewards cumulative discount value | n/a | R761.2m since launch | WITHHELD | WITHHELD | Presentation p.16; Stage 1 R1,126.9m corrected. |
| X/bigly labs investment | nil | R330m | WITHHELD | WITHHELD | Commentary p.27; no AFS line. |
| Non-recurring Benefit Points/Better Rewards cost | n/d | R115m | WITHHELD | WITHHELD | Commentary p.27; no AFS line. |

## 3. Consolidated Financial Statements & Cash Flow Bridge

| Line Item | FY25A | FY26A | FY27E | FY28E | Source / Status |
| :--- | ---: | ---: | :---: | :---: | :--- |
| Revenue from contracts with customers | 39,172.347 | 42,825.777 | WITHHELD | WITHHELD | AFS p.13. |
| Cost of sales | (30,371.972) | (33,416.598) | WITHHELD | WITHHELD | AFS p.13. |
| Gross profit | 8,800.375 | 9,409.179 | WITHHELD | WITHHELD | AFS p.13. |
| Other income | 3,347.467 | 3,797.149 | WITHHELD | WITHHELD | AFS p.13. |
| Total income | 12,147.842 | 13,206.328 | WITHHELD | WITHHELD | AFS p.13. |
| Other expenses | (10,043.744) | (11,353.214) | WITHHELD | WITHHELD | AFS p.13. |
| Operating profit | 2,104.098 | 1,853.114 | WITHHELD | WITHHELD | AFS p.13. |
| Net finance costs | (490.605) | (506.568) | WITHHELD | WITHHELD | AFS p.13. |
| Finance income | 30.400 | 47.498 | WITHHELD | WITHHELD | AFS p.13. |
| Finance costs | (521.005) | (554.066) | WITHHELD | WITHHELD | AFS p.13. |
| Profit from associates/JVs | 20.207 | 48.179 | WITHHELD | WITHHELD | AFS p.13. |
| PBT | 1,633.700 | 1,394.725 | WITHHELD | WITHHELD | AFS p.13. |
| Taxation | (414.462) | (359.107) | WITHHELD | WITHHELD | AFS p.13. |
| PAT continuing | 1,219.238 | 1,035.618 | WITHHELD | WITHHELD | AFS p.13. |
| Discontinued operations | nil | nil | WITHHELD | WITHHELD | AFS p.13. |
| PAT total | 1,219.238 | 1,035.618 | WITHHELD | WITHHELD | AFS p.13. |
| Attributable to parent | 1,179.809 | 978.894 | WITHHELD | WITHHELD | AFS p.13. |
| NCI | 39.429 | 56.724 | WITHHELD | WITHHELD | AFS p.13. |
| Weighted-average shares (m) | 857.356337 | 857.006527 | WITHHELD | WITHHELD | AFS Note 11 p.36. |
| Continuing HEPS (cents) | 137.5 | 113.7 | WITHHELD | WITHHELD | AFS Note 11 p.36. |
| Diluted HEPS (cents) | 137.4 | 113.6 | WITHHELD | WITHHELD | AFS Note 11 p.36. |
| FCFE | NOT VERIFIED | NOT VERIFIED | WITHHELD | WITHHELD | OCF is not FCFE; N8. |

Historical vertical arithmetic check: 42,825.777 - 33,416.598 = 9,409.179; 9,409.179 + 3,797.149 = 13,206.328; 13,206.328 - 11,353.214 = 1,853.114; 1,853.114 - 506.568 + 48.179 = 1,394.725; 1,394.725 - 359.107 = 1,035.618.

PAT-to-HEPS reconciliation: 978.894 - 294 + 18 - 5.283 + 1.486 = 974.821; 974.821 / 857.006527 = 113.7c. The "18" is R18k, not R18.324m.

| Cash Flow Line | FY25A | FY26A | FY27E | FY28E | Source / Status |
| :--- | ---: | ---: | :---: | :---: | :--- |
| Cash inflow from trading operations | 3,222.535 | 3,124.134 | WITHHELD | WITHHELD | AFS Note 27.1 p.60. |
| Working capital movement | (923.746) | 125.820 | WITHHELD | WITHHELD | AFS Note 27.2 p.60. |
| Finance income received | 24.060 | 28.492 | WITHHELD | WITHHELD | AFS p.17. |
| Finance costs paid | (515.516) | (559.644) | WITHHELD | WITHHELD | AFS p.17. |
| Taxation paid | (430.648) | (401.870) | WITHHELD | WITHHELD | AFS p.17. |
| Dividends paid | (471.989) | (524.221) | WITHHELD | WITHHELD | AFS p.17. |
| OCF | 904.696 | 1,792.711 | WITHHELD | WITHHELD | AFS p.17; not FCFE. |
| Maintenance capex | (941.548) | (373.968) | WITHHELD | WITHHELD | AFS p.17. |
| Expansion capex | (460.596) | (729.620) | WITHHELD | WITHHELD | AFS p.17. |
| Proceeds on disposal | 37.173 | 14.883 | WITHHELD | WITHHELD | AFS p.17. |
| Acquisitions/JV | (155.940) | (212.475) | WITHHELD | WITHHELD | AFS p.17; includes R189m JV and R23.475m business combination. |
| Lease principal repayment | (641.172) | (691.992) | WITHHELD | WITHHELD | AFS p.17. |
| Net bank loans | 488.393 | (220.142) | WITHHELD | WITHHELD | AFS p.17; receipts less repayments. |
| Treasury shares | (32.604) | (60.432) | WITHHELD | WITHHELD | AFS p.17. |
| NCI/ownership change | 10.746 | (22.011) | WITHHELD | WITHHELD | AFS p.17. |
| Net cash movement | (766.952) | (429.221) | WITHHELD | WITHHELD | AFS p.17. |
| Closing cash/overdraft | (732.283) | (1,166.964) | WITHHELD | WITHHELD | AFS Note 27.5 p.61. |

Statutory OCF includes dividends paid and finance costs; it is not FCFE. A rough pre-dividend operating cash figure is OCF + dividends paid = R2,316.932m; after capex R1,103.588m and lease principal R691.992m, residual is ~R521.352m before net borrowings/other investing. This is not a formal FCFE and is not reconciled to management's definition.

## 4. Valuation Multiples & DCF Table

| Metric | FY25A | FY26A | FY27E | FY28E | Status |
| :--- | ---: | ---: | :---: | :---: | :--- |
| Forward P/E | n/a | n/a | WITHHELD | WITHHELD | No target/forecast HEPS published. |
| EV/EBITDA | n/a | n/a | WITHHELD | WITHHELD | IFRS 16 basis and net debt definition unresolved. |
| Dividend yield | n/a | n/a | WITHHELD | WITHHELD | No forward DPS published. |
| Per-share equity value | n/a | n/a | WITHHELD | WITHHELD | No valuation bridge. |
| DCF | n/a | n/a | WITHHELD | WITHHELD | WACC, terminal growth, normalised FCF, lease basis, net debt and share count unresolved. |

No DCF is run. No EV-to-equity bridge is published. No target price is published.

## 5. Sensitivity Matrix

| Sales Growth \ Debtor Cost % | -50 bps | Base | +50 bps | +100 bps |
| :--- | :---: | :---: | :---: | :---: |
| -200 bps | WITHHELD | WITHHELD | WITHHELD | WITHHELD |
| Base | WITHHELD | WITHHELD | WITHHELD | WITHHELD |
| +200 bps | WITHHELD | WITHHELD | WITHHELD | WITHHELD |
| +400 bps | WITHHELD | WITHHELD | WITHHELD | WITHHELD |

No sensitivity cells are published because no base valuation exists. The table is intentionally blank to avoid fabricating a target.

Historical HEPS rule-of-thumb sensitivity, not a valuation:

| Variable | Base | Change | Pre-tax Impact (R'm) | After-tax Impact (R'm) | HEPS Impact (cents) | Fair Value Impact (R/share) |
| :--- | :--- | :--- | ---: | ---: | ---: | :---: |
| Gross margin | FY26A revenue R42,825.777m | +75 bps | 321.193 | 234.471 | 27.4 | WITHHELD |
| Gross margin | FY26A revenue | -75 bps | (321.193) | (234.471) | (27.4) | WITHHELD |
| Debtor cost % | Gross trade receivables R1,897.879m | +100 bps | (18.979) | (13.855) | (1.6) | WITHHELD |
| Debtor cost % | Gross trade receivables | +200 bps | (37.958) | (27.709) | (3.2) | WITHHELD |
| Interest rate | Net debt excl. leases R3,194.542m | +100 bps | (31.945) | (23.320) | (2.7) | WITHHELD |
| Interest rate | Net debt incl. leases R6,137.775m | +100 bps | (61.378) | (44.806) | (5.2) | WITHHELD |
| SCF reclassification | R965m into borrowings | +100 bps | (9.650) | (7.045) | (0.8) | WITHHELD |
| Working capital | R500m outflow | one-off | n/a | n/a | n/a | WITHHELD |

## 6. Actionable Portfolio Monitoring Triggers & Catalysts

### Operational & Financial Red Lines

- Covenant headroom: if net leverage or interest cover headroom is disclosed below 10%, or if SCF payables are reclassified to borrowings, de-rating risk rises. R965m SCF reclassification adds R965m net debt, or ~0.31x net debt/EBITDA on FY26A EBITDA of R3,160.979m.
- Debtor ECL: if the 60-90 day bucket continues to grow above 50% YoY or coverage falls below 1.0%, increase debtor cost. A +100 bps debtor cost on gross trade receivables R1,897.879m is ~R18.979m pre-tax, ~1.6c HEPS.
- Gross margin: if gross margin falls below 21.5% or the rebate split reveals structural leakage. A 75 bps swing on FY26A revenue is ~R321.193m pre-tax, ~27.4c HEPS.
- Working capital: if trade payables stretch reverses or inventory days rise above 90, cash conversion deteriorates. A R500m working capital outflow is a R500m cash drag; at 8% cost, ~R40m pre-tax, ~3.4c HEPS.
- Store rollout/capex: if FY2027 openings fall below 30 or capex per store exceeds R12,500/m², returns risk rises. R100m extra capex at a 10% pre-tax hurdle is ~R10m annual pre-tax, ~0.95c HEPS.
- Liquidity: if net overdraft exceeds R1.5bn or undrawn facilities fall below R500m, refinancing risk rises. A +R500m overdraft at 10% is ~R50m pre-tax, ~4.3c HEPS.

### Quantified Sensitivity Impacts

- Every 75 bps swing in gross margin alters FY26A HEPS by ~27.4c; fair value impact is withheld because no target multiple or DCF is published.
- Every 100 bps swing in debtor cost on gross trade receivables alters FY26A HEPS by ~1.6c; fair value impact is withheld.
- Every 100 bps swing in interest rates on net debt excluding leases alters FY26A HEPS by ~2.7c; including leases, ~5.2c; fair value impact is withheld.
- Reclassifying R965m SCF payables to borrowings adds ~0.31x net debt/EBITDA and ~0.8c HEPS at +100 bps; fair value impact is withheld.

### Re-Rating Catalysts

- SENS with covenant thresholds, actual ratios and headroom in Rm/x, plus facility-by-facility drawn/undrawn status.
- Note 7 CFS revenue split and complete Note 8 other income/expense breakdown.
- ECL staging, satisfactory-paid %, collection rate and ageing of other receivables/accrued income.
- Store portfolio table with m², trading density, capex split and signed vs pipeline status.
- Lease escalation, average term, optional renewals and ROU depreciation.
- S189 cost/saving/provision and R500m bullet drawdown terms.
- Final dividend DWT/cash impact and interim DPS/share-count reconciliation.
- Entity-level DTA/unrecognised losses and FY2027 ETR.
- Goodwill CGU headroom sensitivity.
- Dis-Chem Life preference share terms and impairment assessment.
- JIBAR/ZARONIA quantum and margin calibration.
- Inventory ageing/shrinkage.
- Better Rewards annual cost/liability and X/bigly labs capex/opex split.

### Upcoming Milestones & Reporting Dates

| Date | Event | Relevance |
| :--- | :--- | :--- |
| 22 June 2026 | FY2026 final dividend payment | ~R137m cash outflow before DWT; confirm DWT treatment. |
| 31 July 2026 | AGM | NED fees, auditor reappointment, remuneration policy, financial assistance authority. |
| 30 October 2026 | Interim results to 31 August 2026 | First FY2027 trading and margin read; Better Rewards and Health Hub progress. |
| February 2027 | Festive season trading update | Consumer demand, Better Rewards traction, wholesale momentum. |
| 28 May 2027 | FY2027 full-year results | IAR has a typo showing 28 May 2026; use 28 May 2027. |
| 31 December 2026 | JIBAR cessation | ZARONIA transition and margin calibration. |
| 31 May 2027 | Standard Bank bullet maturity | Refinancing risk and interest-cost impact. |
| 1H27 | S189 conclusion expected | Cost/saving/provision and operating-model impact. |

## 7. Guardrail Compliance Registry

| Rule Code | Status | Evidence |
| :--- | :---: | :--- |
| ALL-IFRS16-EV-BRIDGE | Not applicable | Valuation withheld; no EV-to-equity bridge published. |
| ALL-PNL-VERTICAL-ARITHMETIC | Pass historical | Historical P&L sums vertically; forecast withheld. |
| ALL-CROSS-SECTION-METRIC-SYNC | Not applicable | No target, HEPS forecast or multiple published in summary. |
| ALL-RATING-BANDS-MONOTONIC | Not applicable | rating_bands is null. |
| ALL-SHARE-COUNT-ANCHOR | Pass | Basic 857.006527m; diluted 857.817750m; HEPS 113.7c. |
| ALL-HISTORICAL-BASE-COLUMN | Pass | FY25A and FY26A included in Sections 2 and 3. |
| ALL-PAT-HEPS-RECONCILIATION | Pass historical | 978.894 - 294 + 18 - 5.283 + 1.486 = 974.821; /857.006527 = 113.7c. |
| ALL-SOTP-ARITHMETIC-AND-NO-DOUBLE-COUNT | Not applicable | No SOTP or DCF published. |
| ALL-TREASURY-SHARE-DIVIDEND-BRIDGE | Partially verified | Gross issued 860.084m; treasury 3.974m; net 856.109m; interim DPS bridge still fails. |
| ALL-ENTITY-ACRONYM-DISAMBIGUATION | Pass | CJ Pharmaceutical, CJ Distribution and TLC distinguished. |
| ALL-DCF-REPRODUCIBILITY | Not applicable | No DCF published. |
| ALL-CASHFLOW-CLASSIFICATION-BRIDGE | Pass historical | OCF is not labelled FCFE; capex, lease principal and finance costs shown separately. |
| ALL-CASH-ROLLFORWARD-CONSISTENCY | Not applicable | Forecast withheld. |
| ALL-SENSITIVITY-REPRODUCIBILITY | Not applicable | No sensitivity cells published. |
| ALL-EQUITY-NAV-VS-CONTRIBUTED-CAPITAL | Not used | NAV per share from presentation is 664.43c WANOS / 662.05c actual; not used in valuation. |
| ALL-MATERIAL-ISSUES-VALUATION-WITHHOLD | Pass | Valuation withheld; all derived valuation fields null. |
| RETAIL-IFRS16-HEADLEASE-SUBLEASE | Not applicable | No evidence of head-lease/sublease netting. |
| RETAIL-ECL-CASHFLOW-VS-ALLOWANCE | Pass historical | ECL movement reconciles to R3.540m cash-flow add-back. |
| RETAIL-APM-OPERATING-MARGIN | Pass | Statutory operating margin 4.33% distinguished from APM adjusted metrics. |
| RETAIL-HIDDEN-ARREARS-AUDIT | Not verified | ECL adequacy unresolved; satisfactory-paid % and collection rate not disclosed. |
| RETAIL-WORKING-CAPITAL-PAYABLE-STRETCH | Pass | Working capital inflow driven by payables +R663.918m; normalised FCF not verified. |

## 8. Bottom Line

VALUATION WITHHELD - MATERIAL ISSUES UNRESOLVED. The historical forensic work is preserved and corrected where primary evidence contradicts Stage 1. No target price, rating, upside, dividend yield, TSR, rating bands or investment recommendation is published. The next step is to obtain the evidence listed in U1-U22, reconcile the cash/debt/portfolio/valuation bridges, and only then rerun the 2-year forecast and valuation.